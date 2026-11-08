# Compute profile (Sprint S01)

- **Ngày đo**: 06/11/2026 – 08/11/2026
- **Người thực hiện**: Đỗ Hoàng Khánh Nam
- **Người hướng dẫn**: TS. Huỳnh Võ Trung Dũng (Steven Huynh)
- **Đề tài**: Semantic 3DGS Real-time Path Planning · Sprint S01

---

## 1. Phần cứng (Máy trạm thực nghiệm / GPU)

- **GPU**: NVIDIA GeForce RTX 4050 Laptop GPU × 1
  - VRAM: 6.00 GB GDDR6
  - Kiến trúc: Ada Lovelace
  - Compute Capability: `sm_89`
- **Driver NVIDIA**: Phiên bản 621.01 (WDDM 3.2, CUDA UMD 13.5)
- **CPU**: 16 logical cores
- **RAM hệ thống**: 16.0 GB
- **Ổ đĩa trống**:
  - Ổ `D:\`: 418.42 GB trống (nơi đặt project, cache và dataset)
  - Ổ `C:\`: 193.21 GB trống
- **Cơ chế chia sẻ GPU**: Dedicated (chạy cục bộ trực tiếp trên GPU máy trạm qua Docker container).

---

## 2. Phần mềm & Môi trường Container

- **Docker**: Docker Desktop 4.98.0 / Docker Engine 29.9.2
- **NVIDIA Container Toolkit / Runtime**: `nvidia` (WSL2 backend)
- **Base Image**: `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel`
- **PyTorch**: 2.4.0
- **CUDA Runtime (trong container)**: 12.4 (`nvcc 12.4`)
- **cuDNN**: 9.1.0
- **gsplat**: 1.5.3 (commit mới nhất từ nerfstudio-project/gsplat)
- **Cấu hình kiến trúc CUDA (`TORCH_CUDA_ARCH_LIST`)**: `8.9` (tối ưu hóa chuyên biệt cho RTX 40-series, rút ngắn thời gian build từ 30 phút xuống ~1 phút)
- **Cache thư viện mở rộng (`TORCH_EXTENSIONS_DIR`)**: `/workspace/.cache/torch_extensions`

---

## 3. Bảng kết quả đo lường thực tế

> **Quy tắc**: Chỉ ghi các số liệu đã đo thực tế trên hệ thống. Ô nào chưa đo ghi rõ "Chưa đo" kèm lý do.

| Thử nghiệm | Lệnh thực thi | Thời gian chạy | VRAM đỉnh | Ghi chú & Đánh giá |
|:---|:---|:---|:---|:---|
| **Smoke test rasterization** | `python scripts/smoke_test_gsplat.py` | Lần đầu: 0.63 s<br>20 lần sau: **1.8 ms/frame** (~555 FPS) | ~19.3 MB | **PASS**. Render 1000 Gaussians ra độ phân giải 320×240 kèm 4 kênh RGB+ED thành công. |
| **Image fitting (50k Gaussians)** | `python Docker/test_simulation.py` | **1.16 s** (~129.4 FPS cho 150 bước Adam) | **19.3 MB** | Loss giảm từ 0.16681 xuống 0.00254. Đã lưu `simulation_result.gif` và `target_vs_render.png`. |
| **Image fitting (Official gsplat)** | `python gsplat/.../image_fitting.py --num_points 2000` | 2.10 s | 45.0 MB | **PASS**. Chạy đúng theo ví dụ chuẩn từ nerfstudio gsplat. |
| **Train scene Garden** | `python simple_trainer.py default ...` | *Chưa đo* | - | Chưa tải dataset Mip-NeRF 360 do ưu tiên dung lượng và băng thông cho Replica Dataset (chuẩn bị cho Sprint S02). |

---

## 4. Các vấn đề kỹ thuật phát sinh và cách giải quyết

1. **Vấn đề 1: Lỗi `"WARNING: The NVIDIA Driver was not detected"` khi nhấn Run trên giao diện Docker Desktop**
   - *Nguyên nhân*: Nút Run trên Docker Desktop UI mặc định chạy runtime thường (`runc`) mà không đính kèm cờ `--gpus all`.
   - *Giải pháp*: Cấu hình `"default-runtime": "nvidia"` trong file cấu hình Docker Engine (`C:\Users\GIGABYTE\.docker\daemon.json`) và khởi động lại Docker service.

2. **Vấn đề 2: Container tự tắt ngay lập tức (Exited 0) khi khởi động từ Docker Desktop**
   - *Nguyên nhân*: Dockerfile mặc định dùng `CMD ["/bin/bash"]`, khi chạy không có cửa sổ gõ lệnh tương tác (TTY) thì bash nhận EOF và thoát ngay lập tức.
   - *Giải pháp*: Thêm script điều hướng `entrypoint.sh`. Khi chạy ở chế độ nền (detached/Run trên Docker), container tự động chạy mô phỏng, ghi log kết quả và giữ trạng thái `Running` phục vụ kết quả qua web server cổng 8080.

3. **Vấn đề 3: Thời gian biên dịch JIT nhân CUDA của gsplat ở lần đầu mất ~80 giây**
   - *Nguyên nhân*: PyTorch phải gọi `ninja` và `nvcc` để compile các kernel C++/CUDA của gsplat ra thư viện chia sẻ `.so`.
   - *Giải pháp*: Cấu hình ánh xạ thư mục cache `TORCH_EXTENSIONS_DIR=/workspace/.cache/torch_extensions` ra ổ cứng máy host `D:\Cuda\.cache\torch_extensions`. Nhân `gsplat_cuda.so` được lưu vĩnh viễn, giúp các lần chạy tiếp theo tải tức thì trong 1.16 giây.
