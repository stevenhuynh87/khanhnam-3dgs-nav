# HƯỚNG DẪN DỰNG DOCKER VÀ CHẠY MÔ PHỎNG GSPLAT

Tài liệu này hướng dẫn chi tiết cách chạy mô phỏng **3D Gaussian Splatting (gsplat)** trên máy tính của bạn với GPU **NVIDIA GeForce RTX 4050 Laptop (6GB VRAM)**, hỗ trợ cả 2 cách: Chạy qua file `.bat` và Chạy trực tiếp từ giao diện **Docker Desktop**.

---

## 1. Cấu hình hệ thống & Tối ưu hóa

- **GPU**: NVIDIA GeForce RTX 4050 Laptop GPU (Kiến trúc Ada Lovelace, Compute Capability `sm_89`, 6GB VRAM).
- **Base Image**: `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel`
- **Cache biên dịch CUDA**: Extension `gsplat_cuda` được lưu và tái sử dụng tại thư mục `D:\Cuda\.cache\torch_extensions`, giúp khởi chạy mô phỏng tức thì (~1 giây) mà không phải biên dịch lại.

---

## 2. Cách 1: Khởi chạy bằng file `run.bat` (Khuyên dùng)

Vào thư mục `D:\Cuda\Docker`, click đúp chuột vào file **`run.bat`**:

Menu điều khiển sẽ xuất hiện:
```text
======================================================================
          HỆ THỐNG MÔ PHỎNG 3D GAUSSIAN SPLATTING (GSPLAT)
              GPU: NVIDIA GeForce RTX 4050 Laptop (CUDA 12.4)
======================================================================

Chọn hành động bạn muốn thực hiện:

  [1] CHẠY MÔ PHỎNG GSPLAT (Tối ưu 50,000 hạt Gaussian và xuất ảnh/GIF)
  [2] MỞ TERMINAL LINUX TƯƠNG TÁC (/bin/bash)
  [3] CHẠY MÔ PHỎNG VÀ TỰ ĐỘNG MỞ THƯ MỤC KẾT QUẢ RESULTS
  [4] THOÁT
```

- **Lựa chọn [1]** *(Chỉ cần nhấn Enter)*: Tự động chạy ngay mô phỏng với GPU RTX 4050, in tiến trình và dừng màn hình để bạn xem kết quả.
- **Lựa chọn [2]**: Mở terminal Linux bash bên trong container để thao tác lệnh tự do.
- **Lựa chọn [3]**: Chạy mô phỏng xong tự động mở thư mục `results\` chứa file ảnh/GIF.

---

## 3. Cách 2: Khởi chạy bằng nút "Run" trên Docker Desktop

### Bước 1: Kích hoạt GPU cho nút Run trên Docker Desktop
Mặc định khi bấm nút Run trên Docker Desktop, Docker không tự cấp GPU NVIDIA. Bạn chỉ cần bật 1 lần duy nhất:
1. Mở **Docker Desktop**.
2. Bấm vào biểu tượng **Settings (Bánh răng)** ở góc trên bên phải.
3. Chọn thẻ **Docker Engine**.
4. Kiểm tra cấu hình JSON, thêm dòng `"default-runtime": "nvidia"`:
   ```json
   {
     "builder": {
       "gc": {
         "defaultKeepStorage": "20GB",
         "enabled": true
       }
     },
     "experimental": false,
     "default-runtime": "nvidia"
   }
   ```
5. Bấm nút **Apply & restart** ở góc dưới bên phải.

*(Hệ thống đã tự động ghi sẵn dòng cấu hình này vào máy bạn, bạn chỉ cần bấm nút Apply & restart trong Docker Desktop).*

### Bước 2: Bấm nút "Run" trên Docker Desktop
1. Vào mục **Images** trên Docker Desktop, tìm image **`gsplat-sim:latest`**.
2. Bấm nút **▶ Run**.
3. (Tùy chọn) Bấm vào **Optional settings**:
   - Host port: `8080`
   - Host path: chọn thư mục `D:\Cuda` -> Container path: `/workspace`
4. Bấm **Run**:
   - Container sẽ tự động chạy bài test mô phỏng `test_simulation.py` bằng GPU.
   - Container **KHÔNG BỊ TẮT** (luôn giữ trạng thái **Running** màu xanh).
   - Bạn chuyển sang tab **Logs** trong Docker Desktop để xem kết quả mô phỏng.
   - Bạn chuyển sang tab **Terminal** để gõ lệnh trực tiếp.
   - Bạn có thể mở trình duyệt vào `http://localhost:8080` để xem kết quả.

---

## 4. Xem kết quả mô phỏng

Mô phỏng sẽ tạo ra:
- `D:\Cuda\results\simulation_result.gif`: Ảnh động mô phỏng quá trình các hạt 3D Gaussian di chuyển, biến đổi màu và độ mờ để hội tụ khớp với ảnh mục tiêu.
- `D:\Cuda\results\target_vs_render.png`: Ảnh so sánh trực quan giữa ảnh mẫu và ảnh render sau khi tối ưu.
