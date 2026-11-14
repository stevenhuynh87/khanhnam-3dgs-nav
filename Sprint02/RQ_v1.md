# Research Questions (RQ Version 1.0)

- **Đề tài**: Semantic 3DGS Real-time Path Planning
- **Sinh viên**: Đỗ Hoàng Khánh Nam
- **Cố vấn hướng dẫn**: TS. Huỳnh Võ Trung Dũng (Steven Huynh)
- **Mã tài liệu**: `docs/RQ_v1.md` (Gate G1 Deliverable)

---

## Danh Sách 5 Câu Hỏi Nghiên Cứu Chính Thức (RQ1 – RQ5)

### Nhóm câu hỏi cho Bài báo Hội nghị (Conference Paper - $\le$ 6 tháng):

#### RQ1 (Hiệu quả của Biên an toàn Ngữ nghĩa Xác suất - PSSF):
> *"Việc sử dụng biên an toàn động dựa trên phân bố xác suất ngữ nghĩa (kỳ vọng rủi ro và CVaR) trong bộ lọc an toàn PSSF có làm giảm đáng kể tỷ lệ vi phạm an toàn (Safety Violation Rate) so với các phương pháp gán nhãn cứng (hard-assignment) truyền thống khi bản đồ có nhiễu phân lớp hay không?"*
- **Giả thuyết khoa học**: PSSF sẽ giảm ít nhất 30% tỷ lệ va chạm trong các kịch bản có độ mập mờ ngữ nghĩa cao (ví dụ: mép thảm, bậc tam cấp, rèm cửa) mà không làm tăng độ dài quãng đường di chuyển quá 5%.
- **Thước đo kiểm chứng**: Violation Rate (%), Path Length (m), Clearance Distance (m).

#### RQ2 (Vai trò của Hiệu chuẩn Xác suất Ngữ nghĩa - SemCal):
> *"Mô hình hiệu chuẩn ngữ nghĩa nhẹ SemCal có giúp giảm thiểu sai số hiệu chuẩn kỳ vọng (ECE - Expected Calibration Error) trên các hạt Gaussian 3D và trực tiếp cải thiện độ an toàn của đường đi so với xác suất thô chưa hiệu chuẩn hoặc phương pháp Temperature Scaling tiêu chuẩn hay không?"*
- **Giả thuyết khoa học**: Mạng SemCal với hàm mất mát Dirichlet Evidential sẽ giảm ECE xuống dưới 5% trên toàn bộ tập dữ liệu Replica, loại bỏ các dự đoán sai nhưng mang độ tự tin cực đoan (overconfident misclassifications).
- **Thước đo kiểm chứng**: ECE (%), Brier Score, Negative Log-Likelihood (NLL).

#### RQ3 (Khả năng đáp ứng thời gian thực trong Simulation):
> *"Vòng lặp tính toán bộ lọc an toàn PSSF và giải bài toán tối ưu bậc hai CBF-QP trên bản đồ 3DGS có đạt tần số thời gian thực $\ge 20\text{ Hz}$ (tức thời gian trễ $P99 \le 50\text{ ms}$) trên GPU máy trạm phục vụ điều hướng tự hành hay không?"*
- **Giả thuyết khoa học**: Nhờ cấu trúc phân vùng không gian (Spatial Hashing) và lọc cục bộ các Gaussian lân cận robot, thời gian giải bài toán QP sẽ dao động từ 15–30 ms ($P99 < 50\text{ ms}$).
- **Thước đo kiểm chứng**: Latency P50, P95, P99 (ms), Tần số điều khiển (Hz).

---

### Nhóm câu hỏi mở rộng cho Bài báo Tạp chí (Journal Paper - $\le$ 12 tháng):

#### RQ4 (Độ bền vững với Trễ quan sát và Độ cũ của bản đồ - LA-PSSF):
> *"Biên an toàn bù trễ (Latency-Aware PSSF) có bảo đảm bằng toán học tính bất biến của tập an toàn (Forward Invariance) khi bản đồ 3DGS bị trễ cập nhật thời gian $\tau$ và các hạt Gaussian bị lệch vị trí theo thời gian hay không?"*
- **Giả thuyết khoa học**: Bằng cách bổ sung số hạng Lyapunov bù trừ sai số tích lũy $\dot{h}(x) \ge -\alpha(h(x)) - L_f \tau$, robot vẫn giữ được khoảng cách an toàn ngay cả khi dữ liệu cảm biến bị trễ tới 200 ms.
- **Thước đo kiểm chứng**: Forward Invariance Violation Count, Minimal Distance under Delay $\tau$.

#### RQ5 (Tối ưu tốc độ tái lập quỹ đạo bằng Heuristic Học được - RiskHeur):
> *"Hàm heuristic học được tích hợp kênh rủi ro ngữ nghĩa (RiskHeur) có làm giảm số lượng nút duyệt trong thuật toán A* khi tái lập quỹ đạo nhanh (replanning) mà không làm tăng rủi ro va chạm so với TransPath hay không?"*
- **Giả thuyết khoa học**: RiskHeur giúp giảm $\ge 40\%$ số nút mở rộng (expanded nodes) trong các môi trường mê cung có nhiều vật cản phức tạp.
- **Thước đo kiểm chứng**: Number of Expanded Nodes, Suboptimality Gap, Replanning Time (ms).

