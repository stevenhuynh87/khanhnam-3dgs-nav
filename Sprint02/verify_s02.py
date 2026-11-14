# -*- coding: utf-8 -*-
"""
Verification Script for Sprint 02 Definition of Done (Gate G1).
Checks all required deliverables according to advisor's checklist.
"""
import os
import sys
import subprocess

def check_file(path, desc):
    exists = os.path.isfile(path)
    size = os.path.getsize(path) if exists else 0
    status = "[V] PASS" if exists and size > 0 else "[-] FAIL"
    print(f" {status} | {desc:<35} | {path} ({size:,} bytes)")
    return exists and size > 0

def check_git_tag(tag_name):
    try:
        res = subprocess.run(["git", "tag", "-l", tag_name], capture_output=True, text=True, check=True)
        found = tag_name in res.stdout.strip().split()
        status = "[V] PASS" if found else "[-] FAIL"
        print(f" {status} | Git tag '{tag_name}' da tao              | Tag: {tag_name}")
        return found
    except Exception as e:
        print(f" [-] FAIL | Git tag '{tag_name}'                      | Error: {e}")
        return False

def count_lit_matrix(csv_path):
    if not os.path.isfile(csv_path):
        return 0
    with open(csv_path, "r", encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    return max(0, len(lines) - 1)

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    s02_dir = os.path.join(root, "Sprint02")
    docs_dir = os.path.join(root, "docs")
    results_dir = os.path.join(root, "results")

    print("\n" + "=" * 75)
    print("      KIEM CHUNG DINH NGHIA HOAN THANH (DEFINITION OF DONE) - SPRINT S02")
    print("      DE TAI: SEMANTIC 3DGS REAL-TIME PATH PLANNING")
    print("      Hoc vien: Do Hoang Khanh Nam  |  Co van: TS. Huynh Vo Trung Dung")
    print("=" * 75)

    print("\n--- [A] KIEM TRA NHIEM VU (TASKS) ---")
    n_papers = count_lit_matrix(os.path.join(docs_dir, "lit-matrix.csv"))
    lit_pass = n_papers >= 30
    print(f" {'[V] PASS' if lit_pass else '[-] FAIL'} | lit-matrix >= 30 bai             | Da co {n_papers} bai bao (muc tieu >= 30)")
    
    memo_pass = check_file(os.path.join(docs_dir, "positioning_memo.md"), "positioning memo (C1, C2)")
    pilot_pass = (os.path.isfile(os.path.join(results_dir, "room0.ply")) and 
                  os.path.isfile(os.path.join(results_dir, "office0.ply")))
    print(f" {'[V] PASS' if pilot_pass else '[-] FAIL'} | Pilot P2: train room0, office0   | Da co room0.ply va office0.ply")

    print("\n--- [B] KIEM TRA OUTPUT KIEM CHUNG (DEFINITION OF DONE) ---")
    out1_a = check_file(os.path.join(docs_dir, "positioning_memo.md"), "docs/positioning_memo.md")
    out1_b = check_file(os.path.join(docs_dir, "RQ_v1.md"), "docs/RQ_v1.md")
    out1_c = check_file(os.path.join(results_dir, "room0.ply"), "results/room0.ply (3DGS model)")
    out1_d = check_file(os.path.join(results_dir, "office0.ply"), "results/office0.ply (3DGS model)")
    out1_pass = out1_a and out1_b and out1_c and out1_d

    print("\n--- [C] KIEM TRA REPORT GATE G1 ---")
    out2_pass = check_file(os.path.join(docs_dir, "reports", "S02.md"), "docs/reports/S02.md (1-2 trang)")

    print("\n--- [D] KIEM TRA DEMO REVIEW 45 PHUT VA GIT TAG ---")
    out3_pass = check_file(os.path.join(s02_dir, "demo_s02.bat"), "demo_s02.bat (Review Demo Script)")
    out4_pass = check_git_tag("s02")

    print("\n" + "=" * 75)
    all_done = (lit_pass and memo_pass and pilot_pass and 
                out1_pass and out2_pass and out3_pass and out4_pass)

    if all_done:
        print("[V] TAT CA CAC MUC DEFINITION OF DONE CUA SPRINT S02 DA DAT (100% PASS)!")
        print("    San sang 100% de co van TS. Huynh Vo Trung Dung tick vao tat ca cac o.")
    else:
        print("[-] Can bo sung cac muc chua PASS truoc khi nghiem thu Gate G1.")
    print("=" * 75 + "\n")

    return 0 if all_done else 1

if __name__ == "__main__":
    sys.exit(main())

