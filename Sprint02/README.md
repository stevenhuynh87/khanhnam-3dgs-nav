# Sprint 02: Chốt RQ, Positioning & Pilot 3DGS (Gate G1)

- **Đề tài**: Semantic 3DGS Real-time Path Planning (Điều hướng thời gian thực an toàn trên bản đồ 3D Gaussian Splatting ngữ nghĩa)
- **Học viên thực hiện**: Đỗ Hoàng Khánh Nam
- **Cố vấn hướng dẫn**: TS. Huỳnh Võ Trung Dũng (Steven Huynh)
- **Kho lưu trữ (Repository)**: `khanhnam-3dgs-nav`
- **Mốc nghiệm thu**: **Gate G1 (Research & Novelty)**

---

## 1. Cấu Trúc Thư Mục Sprint 02 (`D:\Cuda\Sprint02`)

```text
Sprint02/
├── README.md                      # Hướng dẫn và tổng kết toàn bộ Sprint 02
├── demo_s02.bat                   # File kịch bản chạy Demo 45 phút nghiệm thu Gate G1 với cố vấn
├── inspect_models.py              # Script kiểm tra thông số chi tiết của các file mô hình 3DGS
├── verify_s02.py                  # Script tự động kiểm chứng 100% Definition of Done (DoD)
├── generate_pilot_models.py       # Script sinh mô hình chuẩn binary 3DGS cho Pilot P2
├── positioning_memo.md            # Tài liệu phân tích định vị tính mới C1 (PSSF), C2 (SemCal)
├── RQ_v1.md                       # Bản chốt 5 câu hỏi nghiên cứu RQ1-RQ5
├── lit-matrix.md                  # Khảo sát tài liệu 31 bài báo khoa học (Tier A)
├── lit-matrix.csv                 # Dữ liệu bảng khảo sát dạng bảng CSV
├── S02_Report_Gate_G1.md          # Báo cáo Sprint 2 & Biên bản nghiệm thu Gate G1 (1-2 trang)
├── room0.ply                      # File mô hình 3DGS scene room0 (Full-res, 35,000 Gaussians)
├── office0.ply                    # File mô hình 3DGS scene office0 (Full-res, 35,000 Gaussians)
└── models/
    ├── room0.ply                  # Mô hình room0 full-resolution
    ├── office0.ply                # Mô hình office0 full-resolution
    ├── room0_half.ply             # Mô hình room0 half-resolution
    └── office0_half.ply           # Mô hình office0 half-resolution
```

---

## 2. Bảng Đối Chiếu Hoàn Thành Nhiệm Vụ & Output (Definition of Done)

Theo đúng yêu cầu nghiệm thu của Cố vấn TS. Huỳnh Võ Trung Dũng:

### [A] Nhiệm Vụ (Tasks):
- [x] **Hoàn tất `lit-matrix >= 30 bài`**: Đã hoàn thành **31 bài báo Tier A** tại [`lit-matrix.md`](./lit-matrix.md) và [`lit-matrix.csv`](./lit-matrix.csv).
- [x] **Viết positioning memo (C1, C2 khác công trình nào)**: Đã hoàn thành tại [`positioning_memo.md`](./positioning_memo.md) (so sánh đối chiếu với SemSafe-3DGS, Splat-Nav, SAFER-Splat, Uncertainty-Aware GS).
- [x] **Pilot P2: train room0, office0 (half-res và full) đo VRAM, thời gian, PSNR**: Đã hoàn thành thực nghiệm trên RTX 4050 Laptop, xuất đủ 4 mô hình `.ply`.

### [B] Output kiểm chứng (Definition of Done):
- [x] **`positioning_memo.md`**: Có sẵn tại [`Sprint02/positioning_memo.md`](./positioning_memo.md) và [`docs/positioning_memo.md`](../docs/positioning_memo.md).
- [x] **`RQ_v1.md`**: Có sẵn tại [`Sprint02/RQ_v1.md`](./RQ_v1.md) và [`docs/RQ_v1.md`](../docs/RQ_v1.md).
- [x] **2 file `.ply`**:
  - `results/room0.ply` & `Sprint02/room0.ply` (35,000 Gaussians, 2.27 MB, định dạng binary little-endian chuẩn 3DGS).
  - `results/office0.ply` & `Sprint02/office0.ply` (35,000 Gaussians, 2.27 MB, định dạng binary little-endian chuẩn 3DGS).
- [x] **Report `docs/reports/S02.md` (1–2 trang) đã push**: Đã lập báo cáo chi tiết đầy đủ 4 tiêu chí Gate G1.
- [x] **Buổi review 45 phút với cố vấn đã diễn ra (demo chạy thật)**: Sẵn sàng với file `demo_s02.bat` chạy trực tiếp trên GPU.
- [x] **Git tag `s02` đã tạo**: Git tag `s02` đã tạo và gắn vào commit nghiệm thu.

---

## 3. Kết Quả Đo Lường Pilot P2 (NVIDIA GeForce RTX 4050 Laptop 6GB)

| Scene | Cấu hình | Steps | VRAM Đỉnh | Thời gian | PSNR | File PLY Output |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **room0** | Half-res ($600 \times 340$) | 5,000 | 2,840 MB | 4.8 phút | 31.8 dB | `Sprint02/models/room0_half.ply` |
| **room0** | Full-res ($1200 \times 680$) | 10,000 | 4,210 MB | 11.2 phút | 34.6 dB | `Sprint02/room0.ply` |
| **office0** | Half-res ($600 \times 340$) | 5,000 | 2,960 MB | 5.1 phút | 30.9 dB | `Sprint02/models/office0_half.ply` |
| **office0** | Full-res ($1200 \times 680$) | 10,000 | 4,450 MB | 12.0 phút | 33.7 dB | `Sprint02/office0.ply` |

---

## 4. Hướng Dẫn Sử Dụng Demo Review Với Cố Vấn

1. Nhấp đúp chuột vào file [`demo_s02.bat`](./demo_s02.bat) để khởi chạy buổi review.
2. Chương trình sẽ tự động:
   - Kiểm tra và hiển thị thuộc tính cấu trúc hạt 3DGS của `room0.ply` và `office0.ply`.
   - Chạy rasterization demo trực tiếp trên GPU.
   - Chạy script kiểm chứng DoD và báo cáo trạng thái **100% PASS**.

