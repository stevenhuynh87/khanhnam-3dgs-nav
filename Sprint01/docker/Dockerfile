# Base Image PyTorch 2.4.0 tích hợp CUDA 12.4 và cuDNN 9 (tối ưu cho RTX 40-series Ada Lovelace sm_89)
FROM pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_HOME=/usr/local/cuda \
    PATH=/usr/local/cuda/bin:${PATH} \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH} \
    TORCH_CUDA_ARCH_LIST="8.9" \
    FORCE_CUDA="1" \
    TCNN_CUDA_ARCHITECTURES="89" \
    TORCH_EXTENSIONS_DIR=/workspace/.cache/torch_extensions

# Cài đặt các gói hệ thống cần thiết cho biên dịch CUDA extension và xử lý đồ họa/video
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    ninja-build \
    cmake \
    curl \
    wget \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Nâng cấp pip và cài đặt các phụ thuộc cơ bản
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Cài đặt các thư viện bổ trợ cho gsplat và chạy các ví dụ mô phỏng
RUN pip install --no-cache-dir \
    ninja \
    numpy \
    jaxtyping \
    rich \
    tyro \
    pillow \
    matplotlib \
    imageio \
    imageio[ffmpeg] \
    tqdm \
    scipy \
    scikit-learn \
    plyfile \
    opencv-python-headless \
    viser

# Cài đặt gsplat (ưu tiên pre-built wheel pt24cu124 để build nhanh, fallback sang PyPI)
RUN pip install --no-cache-dir gsplat --index-url https://docs.gsplat.studio/whl/pt24cu124 || \
    pip install --no-cache-dir gsplat

# Tạo thư mục lưu kết quả mô phỏng
RUN mkdir -p /workspace/results

# Thêm thông báo hướng dẫn khi người dùng mở bash shell
RUN echo 'echo "=================================================================="' >> /root/.bashrc && \
    echo 'echo "  Chào mừng bạn đến với môi trường container GSPLAT (CUDA 12.4)!"' >> /root/.bashrc && \
    echo 'echo "  - Chạy mô phỏng Gaussian Splatting: python /workspace/Docker/test_simulation.py"' >> /root/.bashrc && \
    echo 'echo "  - Thoát khỏi container: gõ exit"' >> /root/.bashrc && \
    echo 'echo "=================================================================="' >> /root/.bashrc

# Copy và cấp quyền cho entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]
CMD ["default"]
