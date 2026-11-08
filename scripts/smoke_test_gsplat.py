"""scripts/smoke_test_gsplat.py : kiểm tra gsplat render được trên GPU.
Được chuẩn hóa theo tài liệu hướng dẫn Sprint S01 - TS. Huỳnh Võ Trung Dũng.
"""
import time
import torch
from gsplat import rasterization

assert torch.cuda.is_available(), "Không thấy GPU trong container"
device = torch.device("cuda")
torch.manual_seed(0)
N, W, H = 1000, 320, 240

means = torch.randn(N, 3, device=device)
means[:, 2] += 4.0                      # đặt các Gaussian phía trước camera
quats = torch.randn(N, 4, device=device)
scales = torch.rand(N, 3, device=device) * 0.1
opacities = torch.rand(N, device=device)
colors = torch.rand(N, 3, device=device)

viewmats = torch.eye(4, device=device)[None]   # camera ở gốc toạ độ, nhìn theo +z
Ks = torch.tensor(
    [[300.0, 0.0, W / 2], [0.0, 300.0, H / 2], [0.0, 0.0, 1.0]], device=device
)[None]


def render(**kw):
    return rasterization(means, quats, scales, opacities, colors,
                         viewmats, Ks, W, H, **kw)


print("=" * 60)
print("  KIỂM TRA SMOKE TEST GSPLAT RASTERIZATION")
print("=" * 60)
print(f"Thiết bị GPU: {torch.cuda.get_device_name(0)}")

t0 = time.time()
out, alphas, meta = render()
torch.cuda.synchronize()
print(f"Lần gọi đầu (có thể gồm biên dịch JIT): {time.time() - t0:.2f} s")

assert out.shape == (1, H, W, 3), out.shape
assert alphas.shape == (1, H, W, 1), alphas.shape
assert torch.isfinite(out).all()
assert "means2d" in meta and "radii" in meta

out_d, _, _ = render(render_mode="RGB+ED")      # RGB + độ sâu kỳ vọng: 4 kênh
assert out_d.shape == (1, H, W, 4), out_d.shape

t0 = time.time()
for _ in range(20):
    render()
torch.cuda.synchronize()
print(f"Trung bình 20 lần gọi sau: {(time.time() - t0) / 20 * 1000:.1f} ms")
print(f"Alpha trung bình: {alphas.mean().item():.3f}")
print("gsplat rasterization smoke test: PASS")

