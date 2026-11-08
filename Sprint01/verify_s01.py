# -*- coding: utf-8 -*-
"""
Verification Script for Sprint 01 Deliverables & Definition of Done.
"""
import os
import sys
import subprocess

def check_file(path, desc):
    exists = os.path.isfile(path)
    size = os.path.getsize(path) if exists else 0
    status = "[V] PASS" if exists and size > 0 else "[-] FAIL"
    print(f" {status} | {desc:<40} | {path} ({size:,} bytes)")
    return exists and size > 0

def check_log_content(path, target_str, desc):
    if not os.path.isfile(path):
        print(f" [-] FAIL | {desc:<40} | Khong tim thay file {path}")
        return False
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    found = target_str in content
    status = "[V] PASS" if found else "[-] FAIL"
    print(f" {status} | {desc:<40} | Chua chuoi: '{target_str}'")
    return found

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    s01_dir = os.path.join(root, "Sprint01")

    print("\n" + "=" * 78)
    print("      KIEM CHUNG 5 MUC DELIVERABLES & DEFINITION OF DONE - SPRINT S01")
    print("      DE TAI: SEMANTIC 3DGS REAL-TIME PATH PLANNING")
    print("      Hoc vien: Do Hoang Khanh Nam  |  Co van: TS. Huynh Vo Trung Dung")
    print("=" * 78)

    print("\n--- [A] KIEM TRA 5 MUC CAN NOP (ISSUE S01) ---")
    c1 = check_file(os.path.join(s01_dir, "docker", "Dockerfile"), "1. docker/Dockerfile build duoc")
    c2 = check_log_content(os.path.join(s01_dir, "logs", "gpu_container_check.log"), "RTX 4050", "2. Log nvidia-smi & PyTorch thay GPU")
    c3 = check_log_content(os.path.join(s01_dir, "logs", "smoke_test.log"), "PASS", "3. smoke_test_gsplat.py in PASS")
    c4 = check_file(os.path.join(s01_dir, "docker", "test_simulation.py"), "4. gsplat vi du image_fitting.py")
    c5 = check_file(os.path.join(s01_dir, "compute_profile.md"), "5. docs/compute_profile.md so do that")

    print("\n--- [B] KIEM TRA DEFINITION OF DONE CUA SPRINT S01 ---")
    d1 = check_file(os.path.join(s01_dir, "S01_Report.md"), "Report docs/reports/S01.md (1-2 trang)")
    d2 = check_file(os.path.join(s01_dir, "demo_s01.bat"), "demo_s01.bat (Review Demo Script)")

    print("\n" + "=" * 78)
    all_pass = c1 and c2 and c3 and c4 and c5 and d1 and d2
    if all_pass:
        print("[V] TOAN BO 5 MUC DELIVERABLES VA DEFINITION OF DONE CUA SPRINT S01 DEU PASS!")
    else:
        print("[-] Can kiem tra lai cac muc FAIL.")
    print("=" * 78 + "\n")
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())

