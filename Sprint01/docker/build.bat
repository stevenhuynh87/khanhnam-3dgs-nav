@echo off
echo ====================================================
echo   BUILD DOCKER IMAGE CHO GSPLAT MO PHONG (CUDA 12.4)
echo ====================================================
cd /d "%~dp0"
docker build -t gsplat-sim:latest -f Dockerfile .
if %errorlevel% neq 0 (
    echo [LOI] Qua trinh build Docker that bai. Vui long kiem tra Docker Desktop da chay chua!
) else (
    echo [THANH CONG] Build Docker image gsplat-sim:latest thanh cong!
)
pause
