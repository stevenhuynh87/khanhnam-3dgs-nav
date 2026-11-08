@echo off
echo ====================================================
echo   CHAY MO PHONG GSPLAT BEN TRONG DOCKER (GPU)
echo ====================================================
cd /d "%~dp0"
docker run --gpus all --rm --ipc=host -e TORCH_EXTENSIONS_DIR=/workspace/.cache/torch_extensions -v "%~dp0..":/workspace -w /workspace gsplat-sim:latest python /workspace/Docker/test_simulation.py
if %errorlevel% equ 0 (
    echo.
    echo [XONG] Kiem tra ket qua anh va animation GIF tai thu muc: D:\Cuda\results
)
pause
