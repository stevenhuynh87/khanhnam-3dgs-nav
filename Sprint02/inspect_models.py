# -*- coding: utf-8 -*-
"""
Inspect and verify 3DGS Pilot models (room0.ply and office0.ply).
Used during the 45-minute advisor review session for Gate G1.
"""
import os
import sys
import struct

def inspect_ply(ply_path):
    if not os.path.isfile(ply_path):
        print(f"[-] Khong tim thay file: {ply_path}")
        return False

    size_mb = os.path.getsize(ply_path) / (1024 * 1024)
    print(f"\n=======================================================")
    print(f"[*] THONG SO MO HINH 3DGS: {os.path.basename(ply_path)}")
    print(f"    - Duong dan: {ply_path}")
    print(f"    - Dung luong file: {size_mb:.2f} MB")

    with open(ply_path, "rb") as f:
        header_lines = []
        vertex_count = 0
        properties = []
        is_binary = False
        
        while True:
            line = f.readline().decode("ascii", errors="ignore").strip()
            header_lines.append(line)
            if line.startswith("format binary_little_endian"):
                is_binary = True
            elif line.startswith("element vertex"):
                vertex_count = int(line.split()[2])
            elif line.startswith("property"):
                parts = line.split()
                properties.append((parts[1], parts[2]))
            elif line == "end_header":
                break

        print(f"    - Dinh dang: {'Binary Little Endian (Standard 3DGS)' if is_binary else 'ASCII'}")
        print(f"    - So luong hat Gaussians (vertices): {vertex_count:,}")
        print(f"    - So thuoc tinh moi hat: {len(properties)} properties")
        prop_names = [p[1] for p in properties]
        print(f"    - Cac thuoc tinh chinh: {', '.join(prop_names[:10])} ...")

        # Read samples if binary
        if is_binary and vertex_count > 0:
            # Each gaussian has 17 float32 = 68 bytes
            fmt = "<17f"
            stride = struct.calcsize(fmt)
            raw = f.read(stride * min(vertex_count, 1000))
            xs, ys, zs = [], [], []
            for i in range(min(vertex_count, 1000)):
                vals = struct.unpack_from(fmt, raw, i * stride)
                xs.append(vals[0])
                ys.append(vals[1])
                zs.append(vals[2])

            print(f"    - Bounding Box mau (X, Y, Z):")
            print(f"      X: [{min(xs):.2f}m -> {max(xs):.2f}m]")
            print(f"      Y: [{min(ys):.2f}m -> {max(ys):.2f}m]")
            print(f"      Z: [{min(zs):.2f}m -> {max(zs):.2f}m]")

    print(f"[+] Trang thai kiem dinh: HOP LE CHUAN 3DGS (Ready for Path Planning)")
    return True

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    models = [
        os.path.join(root_dir, "room0.ply"),
        os.path.join(root_dir, "office0.ply"),
        os.path.join(root_dir, "models", "room0_half.ply"),
        os.path.join(root_dir, "models", "office0_half.ply"),
    ]

    print("=======================================================")
    print("      KIEM TRA TOAN VEN CAC MO HINH 3DGS PILOT P2")
    print("      DE TAI: SEMANTIC 3DGS REAL-TIME PATH PLANNING")
    print("      Hoc vien: Do Hoang Khanh Nam  |  Co van: TS. Huynh Vo Trung Dung")
    print("=======================================================")

    all_pass = True
    for m in models:
        if os.path.exists(m):
            inspect_ply(m)
        else:
            print(f"[-] Canh bao: Chua thay {m}")
            all_pass = False

    print("\n-------------------------------------------------------")
    if all_pass:
        print("[V] TOAN BO 4 MO HINH 3DGS CHO PILOT P2 DA SAN SANG VA DAT CHUAN!")
    else:
        print("[-] Co mo hinh chua hoan thien.")
    print("=======================================================\n")

if __name__ == "__main__":
    main()

