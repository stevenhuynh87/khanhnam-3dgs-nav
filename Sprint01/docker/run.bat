@echo off
title MO PHONG 3D GAUSSIAN SPLATTING (GSPLAT - CUDA)
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
cd /d "%SCRIPT_DIR%"
set "ROOT_DIR=%SCRIPT_DIR%\.."

echo ======================================================================
echo           HE THONG MO PHONG 3D GAUSSIAN SPLATTING (GSPLAT)
echo               GPU: NVIDIA GeForce RTX 4050 Laptop (CUDA 12.4)
echo ======================================================================
echo.
echo Chon hanh dong ban muon thuc hien:
echo.
echo   [1] CHAY MO PHONG GSPLAT (Toi uu 50,000 hat Gaussian va xuat anh/GIF)
echo   [2] MO TERMINAL LINUX TUONG TAC (/bin/bash)
echo   [3] CHAY MO PHONG VA TU DONG MO THU MUC KET QUA RESULTS
echo   [4] THOAT
echo.
set /p choice="Nhap lua chon cua ban [1-4] (Mac dinh nhan ENTER la 1): "

if "%choice%"=="" set choice=1
if "%choice%"=="4" goto :eof

if "%choice%"=="1" (
    echo.
    echo [+] Dang khoi chay container va thuc hien bai mo phong...
    docker run --gpus all --rm --ipc=host -e TORCH_EXTENSIONS_DIR=/workspace/.cache/torch_extensions -v "%ROOT_DIR%":/workspace -w /workspace gsplat-sim:latest python /workspace/Docker/test_simulation.py
    echo.
    echo ======================================================================
    echo [HOAN THANH] Ket qua mo phong da duoc luu tai thu muc: results\
    echo   - simulation_result.gif
    echo   - target_vs_render.png
    echo ======================================================================
    echo.
    pause
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo [+] Dang mo bash terminal tuong tac ben trong container (GPU enabled)...
    echo.
    docker run --gpus all -it --rm --ipc=host -e TORCH_EXTENSIONS_DIR=/workspace/.cache/torch_extensions -v "%ROOT_DIR%":/workspace -w /workspace -p 8080:8080 gsplat-sim:latest /bin/bash
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo [+] Dang khoi chay container va thuc hien bai mo phong...
    docker run --gpus all --rm --ipc=host -e TORCH_EXTENSIONS_DIR=/workspace/.cache/torch_extensions -v "%ROOT_DIR%":/workspace -w /workspace gsplat-sim:latest python /workspace/Docker/test_simulation.py
    echo.
    echo [+] Dang mo thu muc ket qua results...
    start "" "%ROOT_DIR%\results"
    pause
    goto :end
)

:end
