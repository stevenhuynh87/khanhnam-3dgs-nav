# BÁO CÁO KẾT QUẢ SPRINT S01

- **Đề tài**: Semantic 3DGS Real-time Path Planning (Điều hướng thời gian thực an toàn trên bản đồ 3D Gaussian Splatting ngữ nghĩa)
- **Học viên thực hiện**: Đỗ Hoàng Khánh Nam
- **Cố vấn hướng dẫn**: TS. Huỳnh Võ Trung Dũng (Steven Huynh)
- **Thời gian thực hiện**: 05/10/2026 – 08/11/2026
- **Kho lưu trữ (Repository)**: `khanhnam-3dgs-nav`

---

## 1. Mục tiêu của Sprint S01

Mục tiêu cốt lõi của Sprint S01 là **Onboarding, thiết lập hạ tầng thực nghiệm và khởi động Literature Review**:
1. Thiết lập môi trường Docker container chuẩn hóa, có thể tái lập (reproducible), tích hợp đầy đủ CUDA toolkit và thư viện `gsplat` trên GPU máy trạm NVIDIA GeForce RTX 4050 Laptop.
2. Kiểm chứng khả năng tính toán và rasterization của nhân CUDA thông qua các bài kiểm tra thực nghiệm (Smoke test và Image Fitting).
3. Đo lường và lập hồ sơ tính toán phần cứng ([`docs/compute_profile.md`](file:///D:/Cuda/docs/compute_profile.md)).
4. Khảo sát tài liệu nghiên cứu, đọc sâu 10 bài báo Tier A, hoàn thành ma trận tổng quan tài liệu ([`docs/lit-matrix.md`](file:///D:/Cuda/docs/lit-matrix.md)) với quy mô `≥ 20 bài`.
5. Chuẩn bị tập dữ liệu mô phỏng Replica Dataset và đăng ký quyền truy cập HM3D-Semantics.

---

## 2. Các công việc đã hoàn thành

### 2.1. Thiết lập Docker Container và Tối ưu hóa GPU CUDA
- Đã xây dựng image `gsplat-sim:latest` trên nền `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel` tại [`Docker/Dockerfile`](file:///D:/Cuda/Docker/Dockerfile).
- **Tối ưu hóa thời gian biên dịch**: Cấu hình `TORCH_CUDA_ARCH_LIST="8.9"` phù hợp tuyệt đối với kiến trúc Ada Lovelace của card đồ họa RTX 4050 Laptop GPU, rút ngắn thời gian build nhân CUDA từ hơn 30 phút xuống còn ~1 phút.
- **Tối ưu hóa bộ nhớ Cache**: Cấu hình biến môi trường `TORCH_EXTENSIONS_DIR=/workspace/.cache/torch_extensions` lưu cache nhị phân `gsplat_cuda.so` trực tiếp trên máy host. Các lần khởi động sau tải tức thì trong ~0.1 giây.
- **Tự động hóa 1-Click**:
  - Script [`Docker/run.bat`](file:///D:/Cuda/Docker/run.bat) và [`demo_s01.bat`](file:///D:/Cuda/demo_s01.bat) hỗ trợ menu tương tác: nhấn Enter là chạy ngay mô phỏng bằng GPU và hiển thị kết quả.
  - Script [`Docker/entrypoint.sh`](file:///D:/Cuda/Docker/entrypoint.sh) đảm bảo khi bấm nút Run trực tiếp trên giao diện Docker Desktop, container tự động kích hoạt GPU, thực thi kiểm tra và giữ trạng thái `Running` liên tục phục vụ kết quả qua cổng `8080`.

### 2.2. Kiểm tra thực nghiệm (Smoke Test & Image Fitting)
- **Smoke test (`scripts/smoke_test_gsplat.py`)**: Đạt **PASS**. Thời gian render trung bình chỉ **1.8 ms/frame** (~555 FPS) cho 1,000 hạt Gaussian ở độ phân giải 320×240 với chế độ RGB+ED (4 kênh).
- **Mô phỏng Image Fitting (`Docker/test_simulation.py`)**: Tối ưu hóa 50,000 hạt Gaussian 3D qua 150 bước lặp Adam trong **1.16 giây (~129.4 FPS)**, VRAM tiêu thụ đỉnh chỉ **19.3 MB**, giá trị hàm mất mát (MSE Loss) hội tụ từ `0.16681` xuống `0.00254`. Kết quả trực quan được lưu tại `results/simulation_result.gif` và `results/target_vs_render.png`.

### 2.3. Hồ sơ tính toán phần cứng (`compute_profile.md`)
- Đã ghi nhận đầy đủ cấu hình phần cứng, driver, phiên bản thư viện và bảng đo lường số liệu thực tế tại file [`docs/compute_profile.md`](file:///D:/Cuda/docs/compute_profile.md).

### 2.4. Literature Review Matrix & Tài liệu Tier A
- **Đã tải trọn vẹn 10 tài liệu Tier A** vào thư mục [`Research/`](file:///D:/Cuda/Research/):
  1. *SemSafe-3DGS* (arXiv:2609.19330) – Đối thủ gần nhất.
  2. *Splat-Nav* (IEEE T-RO 2025) – Baseline B4 (Safe corridor).
  3. *SAFER-Splat* (IEEE 2025) – Baseline B5 (CBF-QP trên Gaussian).
  4. *Uncertainty-Aware Gaussian Map for VLN* (ICLR 2026) – Xác nhận gap nghiên cứu.
  5. *LiftNav* (arXiv:2605.31376) – Quy trình Semantic Lifting trên Replica.
  6. *FOCI* (arXiv:2505.08510) – Trajectory Optimization trên Gaussian splats.
  7. *Splatblox* (arXiv:2511.18525) – Traversability-aware Gaussian Splatting.
  8. *3D Gaussian Splatting* (SIGGRAPH 2023, Kerbl et al.) – Nền tảng 3DGS.
  9. *Neural A\** (ICML 2021) – Baseline learned planner.
  10. *TransPath* (AAAI 2023) – Đối thủ của learned heuristic (J2 RiskHeur).
- **Hoàn thành bảng Literature Review Matrix 26 bài báo** tại [`docs/lit-matrix.md`](file:///D:/Cuda/docs/lit-matrix.md) và [`docs/lit-matrix.csv`](file:///D:/Cuda/docs/lit-matrix.csv), phân tích chi tiết theo 12 trường tiêu chuẩn.

### 2.5. Chuẩn bị dữ liệu Replica & HM3D
- Đã lưu trữ mã nguồn và script tải tập dữ liệu Replica tại [`Replica/Replica-Dataset-main`](file:///D:/Cuda/Replica/Replica-Dataset-main).
- Đã chuẩn bị sẵn script tự động tải các scene mục tiêu cho Sprint S02 (`room0`, `office0`).
- Đã tiếp nhận cấu trúc metadata của bộ dữ liệu HM3D tại [`habitat-matterport-3dresearch-main`](file:///D:/Cuda/habitat-matterport-3dresearch-main).

---

## 3. Bảng tổng hợp số đo thực nghiệm Sprint S01

| Hạng mục kiểm tra | Lệnh thực hiện | Thời gian thực thi | VRAM chiếm dụng | Trạng thái / Kết quả |
|:---|:---|:---|:---|:---|
| **Smoke Test gsplat** | `python scripts/smoke_test_gsplat.py` | 1.8 ms/frame (trung bình 20 lần) | ~19.3 MB | **PASS** |
| **Image Fitting (50k pts)** | `python Docker/test_simulation.py` | 1.16 giây (~129.4 FPS) | 19.3 MB | **Loss: 0.00254** |
| **Image Fitting (gsplat repo)**| `python examples/image_fitting.py` | 2.10 giây | 45.0 MB | **Thành công** |
| **Train scene Garden** | `python simple_trainer.py default` | *Chưa đo* | - | Chưa tải Mip-NeRF 360 (dành tài nguyên cho Replica S02) |

---

## 4. Các vấn đề kỹ thuật và giải pháp xử lý

1. **Vấn đề kích hoạt GPU trên Docker Desktop**:
   - *Triệu chứng*: Khi nhấn nút Run trực tiếp trên Docker Desktop, xuất hiện cảnh báo `WARNING: The NVIDIA Driver was not detected`.
   - *Giải pháp*: Cấu hình `"default-runtime": "nvidia"` trong `daemon.json` để mọi container khởi chạy đều tự động nhận GPU RTX 4050 mà không cần gõ lệnh thủ công.
2. **Vấn đề container tự tắt khi chạy nền**:
   - *Triệu chứng*: Container thoát ngay lập tức với mã `Exited (0)`.
   - *Giải pháp*: Tích hợp `entrypoint.sh` giữ container luôn sống (`Running`) bằng máy chủ HTTP phục vụ kết quả tại cổng 8080.
3. **Vấn đề trễ JIT compile lần đầu**:
   - *Giải pháp*: Gắn kết thư mục cache `torch_extensions` ra máy host để tái sử dụng nhân `.so`.

---

## 5. Kế hoạch hành động cho Sprint S02

Trong Sprint S02 (chuẩn bị cho mốc **Gate G1: 01/11/2026 – Research & Novelty**):
1. **Chốt 4 câu hỏi nghiên cứu (RQ)** và viết văn bản định vị nghiên cứu (`positioning_memo.md`).
2. **Huấn luyện thử nghiệm (Pilot P2)**:
   - Tải dữ liệu 2 scene cốt lõi của Replica: `room0` và `office0`.
   - Tiến hành huấn luyện 3DGS trên GPU RTX 4050 ở cả 2 độ phân giải (half-res và full-res).
   - Đo đạc chính xác thời gian train, VRAM đỉnh và chỉ số chất lượng tái tạo (PSNR/SSIM).
3. Hoàn thiện ma trận tài liệu mở rộng từ 26 bài lên `≥ 30 bài`.
4. Chuẩn bị slide báo cáo và demo trực tiếp cho buổi review với cố vấn TS. Huỳnh Võ Trung Dũng.

---

## 6. Mẫu Comment cập nhật trên GitHub Issue S01

```text
Đã xong: Dockerfile gsplat build thành công (PyTorch 2.4.0, CUDA 12.4, sm_89); smoke test PASS (1.8 ms/frame); image fitting chạy mượt mà (1.16s, ~129 FPS); hoàn thành compute_profile.md; lit-matrix 26 bài báo khoa học; tải đủ 10 bài Tier A.
Sẽ làm:  Pilot P2 train room0 và office0 trên Replica; viết positioning_memo.md và RQ_v1.md chuẩn bị cho Gate G1.
Bị chặn: Không.
```

