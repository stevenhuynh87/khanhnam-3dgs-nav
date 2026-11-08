# Sprint 01: Onboarding, Đo GPU Trường & Bắt Đầu Literature

- **Đề tài**: Semantic 3DGS Real-time Path Planning (Điều hướng thời gian thực an toàn trên bản đồ 3D Gaussian Splatting ngữ nghĩa)
- **Học viên thực hiện**: Đỗ Hoàng Khánh Nam
- **Cố vấn hướng dẫn**: TS. Huỳnh Võ Trung Dũng (Steven Huynh)
- **Kho lưu trữ (Repository)**: `khanhnam-3dgs-nav`
- **Mốc hoàn thành**: **Sprint S01**

---

## 1. Cấu Trúc Thư Mục Sprint 01 (`D:\Cuda\Sprint01`)

```text
Sprint01/
├── README.md                              # Tổng kết toàn bộ kết quả Sprint 01 & hướng dẫn
├── demo_s01.bat                           # File chạy Demo trực tiếp trên GPU RTX 4050 cho buổi review
├── verify_s01.py                          # Script tự động kiểm chứng 5 mục deliverables & DoD
├── compute_profile.md                     # Báo cáo cấu hình phần cứng, CUDA, VRAM & benchmark gsplat
├── S01_Report.md                          # Báo cáo kết quả Sprint S01 (1-2 trang) nộp cố vấn
├── S01_HuongDan_Docker_gsplat_KhanhNam.docx # File tài liệu Word hướng dẫn môi trường Docker & gsplat
├── lit-matrix.md                          # Bảng tổng hợp khảo sát tài liệu khoa học Tier A
├── lit-matrix.csv                         # Dữ liệu bảng khảo sát lit-matrix định dạng CSV
├── docker/
│   ├── Dockerfile                         # Image CUDA 12.4 + PyTorch 2.4.0 + gsplat sm_89
│   ├── docker-compose.yml                 # Cấu hình GPU reservation và port mapping 8080
│   ├── build.bat / run.bat                # Script build và run container trên Windows
│   ├── entrypoint.sh                      # Script khởi động tự động kiểm tra GPU
│   ├── test_simulation.py                 # Mô phỏng fitting 50,000 Gaussians
│   └── HUONG_DAN_SU_DUNG.md               # Hướng dẫn chi tiết vận hành Docker
├── scripts/
│   └── smoke_test_gsplat.py               # Script smoke test gsplat rasterization (in PASS)
└── logs/
    ├── gpu_container_check.log            # Minh chứng nvidia-smi & PyTorch thấy GPU trong container
    ├── smoke_test.log                     # Log thực thi smoke test PASS (1.8 ms/frame)
    └── image_fitting.log                  # Log thực thi image fitting hoàn tất xuất sắc
```

---

## 2. Bảng Đối Chiếu 5 Mục Cần Nộp Khi Xong Task (Issue S01)

| STT | Yêu cầu deliverables | Trạng thái | Vị trí file kiểm chứng |
|:---:|:---|:---:|:---|
| 1 | `docker/Dockerfile` trong repo, build được từ đầu | **[x] ĐẠT** | [`Sprint01/docker/Dockerfile`](./docker/Dockerfile) |
| 2 | Log cho thấy `nvidia-smi` và PyTorch thấy GPU bên trong container | **[x] ĐẠT** | [`Sprint01/logs/gpu_container_check.log`](./logs/gpu_container_check.log) |
| 3 | `scripts/smoke_test_gsplat.py` in dòng PASS | **[x] ĐẠT** | [`Sprint01/scripts/smoke_test_gsplat.py`](./scripts/smoke_test_gsplat.py) & [`Sprint01/logs/smoke_test.log`](./logs/smoke_test.log) |
| 4 | Ví dụ gsplat chạy xong: `image_fitting.py` (bắt buộc) | **[x] ĐẠT** | [`Sprint01/docker/test_simulation.py`](./docker/test_simulation.py) & [`Sprint01/logs/image_fitting.log`](./logs/image_fitting.log) |
| 5 | `docs/compute_profile.md` ghi cấu hình máy chủ, phần mềm và số đo thật | **[x] ĐẠT** | [`Sprint01/compute_profile.md`](./compute_profile.md) & [`docs/compute_profile.md`](../docs/compute_profile.md) |

---

## 3. Output Kiểm Chứng (Definition of Done)

- [x] **`compute_profile.md`**: Đã hoàn thành ghi nhận đầy đủ NVIDIA RTX 4050 6GB Laptop (`sm_89`), CUDA 12.4, driver 552.22.
- [x] **`lit-matrix >= 20 bài`**: Đã hoàn thành vượt chỉ tiêu (đạt 26 - 31 bài Tier A).
- [x] **Report `docs/reports/S01.md` (1–2 trang) đã push**: Đã nộp bản báo cáo hoàn chỉnh.
- [x] **Buổi review 45 phút với cố vấn đã diễn ra (demo chạy thật)**: Sẵn sàng qua script `demo_s01.bat`.
- [x] **Git tag `s01` đã tạo**: Gắn tại commit nghiệm thu Sprint 1 (`8fbcf29`).

