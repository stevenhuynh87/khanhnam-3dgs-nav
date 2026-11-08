"""
Kịch bản kiểm tra mô phỏng 3D Gaussian Splatting (gsplat) trên GPU NVIDIA.
- Kiểm tra kết nối GPU và bộ nhớ VRAM.
- Khởi tạo 50,000 hạt Gaussian ngẫu nhiên trong không gian 3D.
- Thực hiện forward rasterization và backward pass bằng CUDA kernels của gsplat.
- Tối ưu hóa các hạt Gaussian để tái tạo ảnh mục tiêu.
- Lưu ảnh và animation GIF kết quả vào thư mục /workspace/results/.
"""

import math
import os
import time
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

try:
    import gsplat
    from gsplat import rasterization
except ImportError as e:
    print(f"[-] Lỗi import gsplat: {e}")
    print("Vui lòng đảm bảo gsplat đã được cài đặt chính xác trong môi trường container.")
    exit(1)


def check_gpu():
    print("=" * 60)
    print("  KIỂM TRA MÔI TRƯỜNG GPU VÀ GSPLAT")
    print("=" * 60)
    if not torch.cuda.is_available():
        print("[-] CẢNH BÁO: Không tìm thấy GPU CUDA! Docker cần được khởi chạy với '--gpus all'.")
        exit(1)

    device_name = torch.cuda.get_device_name(0)
    vram_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    cuda_ver = torch.version.cuda
    torch_ver = torch.__version__
    gsplat_ver = getattr(gsplat, "__version__", "installed")

    print(f"[+] Thiết bị GPU        : {device_name}")
    print(f"[+] Bộ nhớ VRAM         : {vram_total:.2f} GB")
    print(f"[+] Phiên bản PyTorch   : {torch_ver}")
    print(f"[+] CUDA Runtime        : {cuda_ver}")
    print(f"[+] Phiên bản gsplat    : {gsplat_ver}")
    print("=" * 60)


def create_target_image(height=256, width=256):
    """Tạo ảnh mục tiêu dạng đồ họa để mô phỏng fitting."""
    y, x = torch.meshgrid(torch.linspace(-1, 1, height), torch.linspace(-1, 1, width), indexing="ij")
    r1 = torch.sqrt((x + 0.3)**2 + (y + 0.3)**2)
    r2 = torch.sqrt((x - 0.3)**2 + (y - 0.3)**2)
    
    img = torch.zeros(height, width, 3)
    # Vòng tròn đỏ
    img[r1 < 0.4] = torch.tensor([0.9, 0.2, 0.2])
    # Vòng tròn xanh lục
    img[r2 < 0.4] = torch.tensor([0.1, 0.8, 0.3])
    # Nền gradient nhẹ
    img[..., 2] += (x * 0.2 + 0.2).clamp(0, 0.4)
    return img.clamp(0.0, 1.0)


def run_simulation(num_points=50000, iterations=150, H=256, W=256):
    device = torch.device("cuda:0")
    print(f"\n[+] Bắt đầu mô phỏng 3D Gaussian Splatting:")
    print(f"    - Số lượng hạt Gaussians: {num_points:,}")
    print(f"    - Độ phân giải ảnh      : {W}x{H}")
    print(f"    - Số vòng lặp tối ưu    : {iterations}")

    # Camera intrinsics (pinhole)
    fov_x = math.pi / 3.0
    focal = 0.5 * float(W) / math.tan(0.5 * fov_x)
    K = torch.tensor([
        [focal, 0.0, W / 2.0],
        [0.0, focal, H / 2.0],
        [0.0, 0.0, 1.0]
    ], device=device)[None]

    # Camera extrinsics (view matrix: lùi z = 3.0)
    viewmat = torch.tensor([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 3.0],
        [0.0, 0.0, 0.0, 1.0]
    ], device=device)[None]

    # Khởi tạo tham số cho các hạt Gaussian
    torch.manual_seed(42)
    means = (torch.rand(num_points, 3, device=device) - 0.5) * 2.0
    scales = torch.rand(num_points, 3, device=device) * 0.05
    rgbs = torch.rand(num_points, 3, device=device)

    # Quaternion đồng đều ngẫu nhiên
    u = torch.rand(num_points, 1, device=device)
    v = torch.rand(num_points, 1, device=device)
    w = torch.rand(num_points, 1, device=device)
    quats = torch.cat([
        torch.sqrt(1.0 - u) * torch.sin(2.0 * math.pi * v),
        torch.sqrt(1.0 - u) * torch.cos(2.0 * math.pi * v),
        torch.sqrt(u) * torch.sin(2.0 * math.pi * w),
        torch.sqrt(u) * torch.cos(2.0 * math.pi * w),
    ], dim=-1)
    opacities = torch.ones(num_points, device=device) * 0.5

    # Bật gradient cho các tham số cần học
    means.requires_grad = True
    scales.requires_grad = True
    quats.requires_grad = True
    rgbs.requires_grad = True
    opacities.requires_grad = True

    optimizer = torch.optim.Adam([
        {"params": [means], "lr": 0.005},
        {"params": [scales], "lr": 0.005},
        {"params": [quats], "lr": 0.001},
        {"params": [rgbs], "lr": 0.02},
        {"params": [opacities], "lr": 0.05},
    ])

    target = create_target_image(H, W).to(device)

    frames = []
    print("\n[+] Đang chạy vòng lặp tối ưu hóa:")
    start_total = time.time()

    for step in range(iterations):
        t0 = time.time()

        # Chuẩn hóa quaternion
        norm_quats = quats / quats.norm(dim=-1, keepdim=True)
        act_opacities = torch.sigmoid(opacities)
        act_rgbs = torch.sigmoid(rgbs)
        act_scales = torch.exp(scales) * 0.02

        # Gọi CUDA rasterization kernel của gsplat
        render_output = rasterization(
            means=means,
            quats=norm_quats,
            scales=act_scales,
            opacities=act_opacities,
            colors=act_rgbs,
            viewmats=viewmat,
            Ks=K,
            width=W,
            height=H,
            packed=False,
        )
        rendered_img = render_output[0][0]  # [H, W, 3]

        loss = F.mse_loss(rendered_img, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        torch.cuda.synchronize()

        step_time = (time.time() - t0) * 1000.0

        if (step + 1) % 25 == 0 or step == 0:
            vram_used = torch.cuda.memory_allocated(device) / (1024**2)
            print(f"    Bước {step + 1:3d}/{iterations} | Loss: {loss.item():.5f} | Thời gian: {step_time:6.2f} ms | VRAM: {vram_used:.1f} MB")

        if step % 5 == 0 or step == iterations - 1:
            frame_np = (rendered_img.detach().clamp(0, 1).cpu().numpy() * 255).astype(np.uint8)
            frames.append(frame_np)

    total_time = time.time() - start_total
    avg_fps = iterations / total_time
    print(f"\n[+] Mô phỏng hoàn thành trong {total_time:.2f}s (~{avg_fps:.1f} FPS)")

    # Lưu kết quả
    results_dir = "/workspace/results"
    os.makedirs(results_dir, exist_ok=True)

    gif_path = os.path.join(results_dir, "simulation_result.gif")
    pil_frames = [Image.fromarray(f) for f in frames]
    pil_frames[0].save(
        gif_path,
        save_all=True,
        append_images=pil_frames[1:],
        duration=50,
        loop=0
    )
    print(f"[+] Đã lưu ảnh GIF mô phỏng tại: {gif_path}")

    # Ghép ảnh Target và Render cuối cùng để so sánh
    final_render = frames[-1]
    target_np = (target.cpu().numpy() * 255).astype(np.uint8)
    comparison = np.concatenate([target_np, final_render], axis=1)
    cmp_path = os.path.join(results_dir, "target_vs_render.png")
    Image.fromarray(comparison).save(cmp_path)
    print(f"[+] Đã lưu ảnh đối chiếu (Target | Render) tại: {cmp_path}")
    print("\n>>> KIỂM TRA THÀNH CÔNG: CUDA rasterization và backward pass hoạt động hoàn hảo! <<<\n")


if __name__ == "__main__":
    check_gpu()
    run_simulation()
