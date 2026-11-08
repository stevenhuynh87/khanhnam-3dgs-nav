@echo off
setlocal enabledelayedexpansion
title BUOI REVIEW SPRINT S01 - DEMO CHAY THAT GSPLAT (TS. HUYNH VO TRUNG DUNG)

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
cd /d "%ROOT_DIR%"

echo ======================================================================
echo      DE TAI: SEMANTIC 3DGS REAL-TIME PATH PLANNING
echo      BUOI REVIEW SPRINT S01 - DEMO CHAY THAT TREN GPU RTX 4050
echo      Sinh vien: Do Hoang Khanh Nam  -  Co van: TS. Huynh Vo Trung Dung
echo ======================================================================
echo.
echo [1/2] BUOC 1: CHAY SMOKE TEST GSPLAT RASTERIZATION...
echo ----------------------------------------------------------------------
docker run --gpus all --rm --ipc=host -v "%ROOT_DIR%":/workspace -w /workspace gsplat-sim:latest python /workspace/scripts/smoke_test_gsplat.py
if errorlevel 1 (
    echo.
    echo [-] Smoke test chua thanh cong. Vui long kiem tra Docker Desktop da bat chua.
    pause
    exit /b 1
)

echo.
echo [2/2] BUOC 2: CHAY MO PHONG TOI UU 50,000 HAT GAUSSIAN (IMAGE FITTING)...
echo ----------------------------------------------------------------------
docker run --gpus all --rm --ipc=host -v "%ROOT_DIR%":/workspace -w /workspace gsplat-sim:latest python /workspace/Docker/test_simulation.py
if errorlevel 1 (
    echo.
    echo [-] Mo phong that bai. Vui long kiem tra GPU.
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo [+] DEMO HOAN TAT XUAT SAC!
echo [+] Dang mo thu muc ket qua anh GIF dong va anh doi chieu...
echo ======================================================================
if exist "%ROOT_DIR%\results" (
    start "" "%ROOT_DIR%\results"
)
pause
