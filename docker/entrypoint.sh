#!/bin/bash
set -e

# Đảm bảo sử dụng thư mục cache đã biên dịch sẵn của PyTorch/CUDA extensions
export TORCH_EXTENSIONS_DIR="${TORCH_EXTENSIONS_DIR:-/workspace/.cache/torch_extensions}"

# Nếu người dùng truyền lệnh khác từ terminal/bat (ví dụ: /bin/bash, python ...)
if [ "$#" -gt 0 ] && [ "$1" != "default" ]; then
    exec "$@"
fi

# Chế độ mặc định khi người dùng bấm nút "Run" trên Docker Desktop:
echo "======================================================================"
echo "    KHỞI CHẠY CONTAINER GSPLAT (TỰ ĐỘNG CHẠY TỪ DOCKER DESKTOP)"
echo "======================================================================"

# Kiểm tra trạng thái GPU NVIDIA
if command -v nvidia-smi &> /dev/null && nvidia-smi &> /dev/null; then
    echo "[+] GPU NVIDIA đã được kích hoạt thành công:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
else
    echo "[-] CẢNH BÁO: Container đang chạy ở chế độ CPU (chưa nhận GPU)!"
    echo "    -> Nguyên nhân: Bấm nút Run trực tiếp trên Docker Desktop mặc định chưa cấp quyền GPU."
    echo "    -> Khắc phục: Xem hướng dẫn cấu hình 'default-runtime': 'nvidia' trong Docker Desktop,"
    echo "                 hoặc khởi chạy bằng file run.bat."
fi

# Tự động thực thi kịch bản mô phỏng 3D Gaussian Splatting nếu có
if [ -f "/workspace/Docker/test_simulation.py" ]; then
    echo ""
    echo "[+] Đang tự động chạy bài kiểm tra mô phỏng test_simulation.py..."
    python /workspace/Docker/test_simulation.py || true
fi

echo ""
echo "======================================================================"
echo "[+] Container GSPLAT đang chạy ngầm ở chế độ phục vụ (Keep-Alive)."
echo "[+] Hướng dẫn tương tác:"
echo "    1. Tab 'Logs': Xem toàn bộ tiến trình và kết quả mô phỏng."
echo "    2. Tab 'Terminal': Mở cửa sổ lệnh bash để gõ lệnh trực tiếp."
echo "    3. Mở trình duyệt web tại http://localhost:8080 để xem kết quả."
echo "======================================================================"

# Giữ container luôn hoạt động bằng web server đơn giản trên port 8080
if [ -d "/workspace" ]; then
    cd /workspace
fi
exec python -m http.server 8080

