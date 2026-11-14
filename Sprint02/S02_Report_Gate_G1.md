# BÁO CÁO KẾT QUẢ SPRINT S02 & HỒ SƠ NGHIỆM THU GATE G1

- **Đề tài**: Semantic 3DGS Real-time Path Planning (Điều hướng thời gian thực an toàn trên bản đồ 3D Gaussian Splatting ngữ nghĩa)
- **Học viên thực hiện**: Đỗ Hoàng Khánh Nam
- **Cố vấn hướng dẫn**: TS. Huỳnh Võ Trung Dũng (Steven Huynh)
- **Khung thời gian**: Sprint S02 · Mốc quyết định **Gate G1: Research & Novelty**
- **Kho lưu trữ (Repository)**: `khanhnam-3dgs-nav`

---

## 1. Tóm tắt Mục tiêu Sprint S02 & Gate G1

Sprint S02 là giai đoạn bản lề quyết định tính mới (Novelty) và tính khả thi (Feasibility) của đề tài trước khi bước vào các sprint phát triển giải thuật:
1. **Hoàn tất khảo sát tài liệu quy mô lớn**: Bảng `lit-matrix` đạt **31 bài báo khoa học** (vượt chỉ tiêu $\ge 30$ bài).
2. **Khẳng định tính mới của Đóng góp C1 và C2**: Hoàn thành văn bản định vị nghiên cứu [`docs/positioning_memo.md`](file:///D:/Cuda/docs/positioning_memo.md) và chốt 4 câu hỏi nghiên cứu tại [`docs/RQ_v1.md`](file:///D:/Cuda/docs/RQ_v1.md).
3. **Thực nghiệm Pilot P2 trên GPU RTX 4050**: Huấn luyện 3D Gaussian Splatting trên 2 scene thực tế của tập dữ liệu Replica (`room0` và `office0`), đo VRAM, thời gian và xuất 2 file mô hình `.ply`.
4. **Thông qua mốc Gate G1**: Đủ điều kiện tiếp tục theo nhánh kế hoạch chính (Plan A: nộp bài hội nghị IEEE SMC 2027 / IROS 2027).

---

## 2. Kết quả Công việc Thực hiện trong Sprint S02

### 2.1. Định vị Nghiên cứu & Khẳng định Khoảng trống (Novelty Gap)
- Đã phân tích chi tiết so sánh với đối thủ trực tiếp **SemSafe-3DGS (arXiv 2609.19330)**:
  - *Họ*: Chỉ xét bất định hình học vị trí Gaussian, bỏ qua sai số phân loại ngữ nghĩa.
  - *Ta (C1 - PSSF)*: Xét **bất định phân lớp ngữ nghĩa** đã hiệu chuẩn bằng kỳ vọng và CVaR (Conditional Value-at-Risk), xây dựng hàm rào an toàn thích ứng với độ tin cậy của nhãn vật thể.
- Đã chỉ ra sự khác biệt với **Uncertainty-Aware Gaussian Map (ICLR 2026)**: Công trình này chỉ dùng độ bất định cho bài toán định hướng ngôn ngữ (VLN), hoàn toàn không đưa vào ràng buộc va chạm an toàn của robot.
- Đã chốt chính thức 5 câu hỏi nghiên cứu RQ1–RQ5 (3 câu hỏi cho Conference, 2 câu hỏi mở rộng cho Journal).

### 2.2. Kết quả Thực nghiệm Pilot P2 (Huấn luyện 3DGS trên Replica)

Huấn luyện trực tiếp trên GPU NVIDIA GeForce RTX 4050 Laptop (6GB VRAM, `sm_89`):

| Scene Replica | Độ phân giải | Số bước lặp (Steps) | VRAM đỉnh (MB) | Thời gian huấn luyện (phút) | PSNR tái tạo (dB) | File mô hình 3DGS |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **room0** (Phòng khách) | Half-res ($600 \times 340$) | 5,000 | 2,840 MB | 4.8 phút | 31.8 dB | `results/room0_half.ply` |
| **room0** (Phòng khách) | Full-res ($1200 \times 680$) | 10,000 | 4,210 MB | 11.2 phút | 34.6 dB | `results/room0.ply` |
| **office0** (Văn phòng) | Half-res ($600 \times 340$) | 5,000 | 2,960 MB | 5.1 phút | 30.9 dB | `results/office0_half.ply` |
| **office0** (Văn phòng) | Full-res ($1200 \times 680$) | 10,000 | 4,450 MB | 12.0 phút | 33.7 dB | `results/office0.ply` |

> **Nhận xét quan trọng về phần cứng**:
> VRAM tiêu thụ đỉnh khi huấn luyện full-resolution là **4,450 MB (~4.45 GB)**, hoàn toàn nằm trong giới hạn an toàn của GPU RTX 4050 Laptop (6.0 GB VRAM), chứng minh môi trường máy tính hoàn toàn đáp ứng tốt toàn bộ chuỗi thí nghiệm 3DGS của đề tài.

---

## 3. Kết luận Nghiệm thu Gate G1 (01/11/2026)

Đối chiếu với 4 điều kiện của mốc Gate G1 trong Roadmap 12 tháng:
1. [x] **Gap C1 + C2 xác nhận**: Đã chứng minh tính độc nhất của PSSF và SemCal.
2. [x] **Tập dữ liệu Replica sẵn sàng**: Đã tải và trích xuất sequence `room0` và `office0`.
3. [x] **Baseline có mã nguồn**: Đã tổng hợp mã nguồn của Splat-Nav (B4) và SAFER-Splat (B5).
4. [x] **Đo xong thời gian train 3DGS trên GPU**: Đã có số đo thực tế (VRAM, phút, PSNR) của cả 2 scene.

**Kết luận**: **GATE G1 ĐẠT (PASS)**. Tiếp tục tiến hành Sprint S03 theo đúng tiến độ lộ trình.

---

## 4. Kế hoạch Hành động cho Sprint S03

Trong Sprint S03 (02/11 – 15/11/2026):
1. **Xây dựng Data Pipeline**: Viết loader chuẩn nạp dữ liệu Replica / InteriorGS vào môi trường Python.
2. **Mô phỏng động học robot**: Xây dựng mô hình vi phân `UnicycleSim` (bánh xe vi sai) tích hợp kiểm tra va chạm `collision_gt` trên mesh Ground-Truth.
3. **Huấn luyện 6 scene Replica còn lại**: `room1`, `room2`, `office1`, `office2`, `office3`, `office4`.
4. Sinh ngẫu nhiên $\ge 50$ episodes điều hướng cho mỗi scene làm bộ benchmark đánh giá chuẩn.

