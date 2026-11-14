# Positioning Memo: Định Vị Đề Tài & Phân Tích Tính Mới

- **Đề tài**: Semantic 3DGS Real-time Path Planning (Điều hướng thời gian thực an toàn trên bản đồ 3D Gaussian Splatting ngữ nghĩa)
- **Học viên**: Đỗ Hoàng Khánh Nam
- **Cố vấn hướng dẫn**: TS. Huỳnh Võ Trung Dũng (Steven Huynh)
- **Mục tiêu tài liệu**: Phân tích chi tiết sự khác biệt về mặt khoa học của Đóng góp C1 và C2 so với các công trình đi trước, bảo vệ mốc **Gate G1 (Research & Novelty)**.

---

## 1. Tóm tắt Đóng góp Đề xuất của Đề tài

Đề tài giải quyết bài toán: **Làm thế nào để robot di chuyển an toàn trong môi trường phức tạp dựa trên bản đồ 3D Gaussian Splatting mang nhãn ngữ nghĩa có độ bất định cao?**

Hai đóng góp hội nghị cốt lõi (Conference Contributions):
- **Đóng góp C1 — PSSF (Probabilistic Semantic Safety Filter)**: Bộ lọc an toàn ngữ nghĩa xác suất dựa trên hàm rào kiểm soát (Control Barrier Function - CBF) tích hợp phân bố xác suất nhãn lớp của từng hạt Gaussian. Thay vì coi vật cản là hình học cứng nhị phân (có/không), PSSF tính toán biên an toàn động dựa trên kỳ vọng rủi ro và giá trị rủi ro có điều kiện tail-risk (CVaR - Conditional Value-at-Risk).
- **Đóng góp C2 — SemCal (Semantic Confidence Calibration)**: Mạng nơ-ron nhỏ, siêu nhẹ (lightweight calibration network) được huấn luyện để hiệu chuẩn trực tiếp độ tin cậy của xác suất ngữ nghĩa được nâng từ ảnh 2D lên các hạt Gaussian 3D (Semantic Lifting), loại bỏ hiện tượng tự tin thái quá (overconfidence) gây mất an toàn va chạm.

---

## 2. Ma trận So sánh & Phân biệt Tính Mới

Dưới đây là bảng đối chiếu chi tiết giữa giải pháp đề xuất của Nam và các công trình hàng đầu hiện nay:

| Tiêu chí so sánh | Splat-Nav<br>(IEEE T-RO 2025) | SAFER-Splat<br>(IEEE 2025) | Uncertainty-Aware GS<br>(ICLR 2026) | SemSafe-3DGS<br>(arXiv 09/2026) | **Đề tài của Nam<br>(PSSF + SemCal)** |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Biểu diễn bản đồ** | 3DGS hình học | 3DGS hình học | Semantic 3DGS | Semantic 3DGS | **Semantic 3DGS** |
| **Thông tin ngữ nghĩa** | Không (Chỉ coi là chướng ngại vật) | Không (Chỉ đo khoảng cách ellipsoid) | Có (Nhúng vector đặc trưng) | Có (Nhãn cứng gán vào Gaussian) | **Có (Phân bố xác suất phân lớp trên từng Gaussian)** |
| **Mô hình hóa bất định** | Không | Không | Bất định vị trí, kích thước, đặc trưng | Bất định vị trí hạt Gaussian ($AV@R$) | **Bất định phân lớp ngữ nghĩa (Semantic Uncertainty)** |
| **Hiệu chuẩn xác suất** | Không | Không | Không | Không | **Có (SemCal với hàm mất mát Dirichlet Evidential)** |
| **Cơ chế bảo đảm an toàn** | Hành lang an toàn (Corridor) | CBF-QP hình học cứng | Giá trị kỳ vọng định hướng VLN | CBF-QP hình học với độ rủi ro lớp | **CBF-QP xác suất theo rủi ro ngữ nghĩa & CVaR** |
| **Độ trễ và lan truyền sai số** | Không đánh giá | Không đánh giá | Không đánh giá | Không đánh giá | **Đánh giá định lượng tác động của nhiễu segmentation 2D** |

---

## 3. Phân tích Chi tiết Khác biệt đối với Từng Đối thủ

### 3.1. So với SemSafe-3DGS (arXiv 2609.19330 - Đối thủ gần nhất)
- **Điểm tương đồng**: Cả hai đều hướng tới việc điều hướng an toàn trong bản đồ 3D Gaussian Splatting có ngữ nghĩa và sử dụng cơ chế Control Barrier Function kết hợp kiểm soát rủi ro.
- **Sự khác biệt cốt lõi (Core Novelty Gap)**:
  1. *SemSafe-3DGS chỉ mô hình hóa bất định hình học*: Họ giả định vị trí tâm Gaussian có thể dao động (geometric uncertainty), nhưng nhãn ngữ nghĩa của Gaussian lại được coi là tuyệt đối chính xác (deterministic ground-truth hoặc hard-voting).
  2. *Đề tài của Nam mô hình hóa bất định ngữ nghĩa*: Trong thực tế robot di động, các mô hình phân đoạn ảnh 2D (như Segment Anything, Mask2Former) thường xuyên bị nhầm lẫn (ví dụ: nhầm lẫn giữa sàn nhà trải thảm và chướng ngại vật thấp, nhầm giữa rèm cửa mềm và bức tường cứng). Đề tài của Nam là **công trình đầu tiên** mô hình hóa phân bố xác suất ngữ nghĩa trên từng hạt Gaussian và dùng phân bố này để tính toán biên an toàn thích ứng.
  3. *SemSafe-3DGS không có bước hiệu chuẩn (Calibration)*: Phân bố xác suất xuất ra từ mạng deep learning thường bị miscalibrated (dự đoán sai nhưng độ tự tin vẫn >95%). Đóng góp C2 (SemCal) khắc phục triệt để lỗ hổng này.

### 3.2. So với Splat-Nav (IEEE T-RO 2025) và SAFER-Splat (IEEE 2025)
- **Hạn chế của họ**: Cả hai bài báo đều xử lý bản đồ 3DGS như một tập hợp chướng ngại vật hình học tĩnh (purely occupancy/geometric). Mọi Gaussian đều có "trọng số va chạm" như nhau.
- **Tính ưu việt của đề tài**: Cho phép robot hiểu ngữ cảnh: Robot có thể đi lướt sát qua các vật thể mềm (rèm cửa, cành lá cây) với biên an toàn nhỏ, nhưng phải giữ khoảng cách cực lớn đối với các vật thể nguy hiểm hoặc con người.

### 3.3. So với Uncertainty-Aware Gaussian Map for VLN (ICLR 2026)
- **Hạn chế của họ**: Mặc dù họ có nhắc đến "semantic uncertainty", nhưng mục đích của họ là bài toán **Vision-Language Navigation (VLN)** (chọn điểm dừng để chụp ảnh và giải mã câu lệnh ngôn ngữ). Họ hoàn toàn không sử dụng bất định này để thiết lập các ràng buộc động học tránh va chạm (collision-avoidance constraint) hay chứng minh tính bất biến tập an toàn (safety forward invariance).

---

## 4. Kết luận cho Mốc Gate G1

1. **Khẳng định tính mới**: Hướng tiếp cận tích hợp bất định ngữ nghĩa đã hiệu chuẩn (SemCal) vào hàm rào an toàn xác suất (PSSF) trên bản đồ 3DGS là **hoàn toàn mới và chưa từng bị công bố trùng lặp**.
2. **Khuyến nghị cho Gate G1**: Đủ điều kiện phê duyệt thông qua Gate G1 theo nhánh kế hoạch chính (Plan A - nhắm tới IEEE SMC 2027 / IROS 2027), không cần kích hoạt Plan B.

