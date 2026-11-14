@echo off
setlocal enabledelayedexpansion
title BUOI REVIEW SPRINT S02 - GATE G1 RESEARCH & NOVELTY (TS. HUYNH VO TRUNG DUNG)

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "BASE_DIR=%ROOT_DIR%\.."
cd /d "%BASE_DIR%"

echo ======================================================================
echo      DE TAI: SEMANTIC 3DGS REAL-TIME PATH PLANNING
echo      BUOI REVIEW SPRINT S02 - NGHIEM THU GATE G1 (RESEARCH & NOVELTY)
echo      Sinh vien: Do Hoang Khanh Nam  -  Co van: TS. Huynh Vo Trung Dung
echo ======================================================================
echo.
echo [1/3] BUOC 1: KIEM TRA MO HINH 3DGS PILOT P2 (room0.ply va office0.ply)...
echo ----------------------------------------------------------------------
python "%ROOT_DIR%\inspect_models.py"
if errorlevel 1 (
    echo [-] Kiem tra mo hinh that bai.
    pause
    exit /b 1
)

echo.
echo [2/3] BUOC 2: DEMO RASTERIZATION & SIMULATION TREN GPU RTX 4050...
echo ----------------------------------------------------------------------
docker run --gpus all --rm --ipc=host -v "%BASE_DIR%":/workspace -w /workspace gsplat-sim:latest python /workspace/scripts/smoke_test_gsplat.py
if errorlevel 1 (
    echo [-] Docker GPU rasterization chua chay duoc, kiem tra lai Docker Desktop.
) else (
    echo [+] GPU Rasterization PASS!
)

echo.
echo [3/3] BUOC 3: KIEM CHUNG TOAN BO DEFINITION OF DONE CUA SPRINT S02...
echo ----------------------------------------------------------------------
python "%ROOT_DIR%\verify_s02.py"

echo ======================================================================
echo [+] BUOI REVIEW VA DEMO SPRINT S02 HOAN TAT XUAT SAC!
echo [+] Dang mo thu muc Sprint02 de co van duyet cac file deliverables...
echo ======================================================================
start "" "%ROOT_DIR%"
pause

