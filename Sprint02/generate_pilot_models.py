"""
generate_pilot_models.py
Sinh 2 mô hình 3D Gaussian Splatting (.ply) đại diện cho 2 scene Replica cốt lõi:
- room0.ply (Phòng khách gia đình)
- office0.ply (Văn phòng làm việc)
Tuân thủ chuẩn định dạng nhị phân 3DGS (Inria / gsplat) có đầy đủ thuộc tính:
x, y, z, nx, ny, nz, f_dc_0, f_dc_1, f_dc_2, opacity, scale_0, scale_1, scale_2, rot_0, rot_1, rot_2, rot_3.
"""

import os
import shutil
import numpy as np

def create_3dgs_ply(filename, points, scales, rotations, colors, opacities):
    N = len(points)
    C0 = 0.28209479177387814
    sh_dc = (colors - 0.5) / C0
    log_scales = np.log(np.clip(scales, 1e-6, 1.0))
    opacities = np.clip(opacities, 1e-4, 0.999)
    logit_opacities = np.log(opacities / (1.0 - opacities))

    header = f"""ply
format binary_little_endian 1.0
element vertex {N}
property float x
property float y
property float z
property float nx
property float ny
property float nz
property float f_dc_0
property float f_dc_1
property float f_dc_2
property float opacity
property float scale_0
property float scale_1
property float scale_2
property float rot_0
property float rot_1
property float rot_2
property float rot_3
end_header
"""
    with open(filename, "wb") as f:
        f.write(header.encode("ascii"))
        data = np.zeros(N, dtype=[
            ('x', '<f4'), ('y', '<f4'), ('z', '<f4'),
            ('nx', '<f4'), ('ny', '<f4'), ('nz', '<f4'),
            ('f_dc_0', '<f4'), ('f_dc_1', '<f4'), ('f_dc_2', '<f4'),
            ('opacity', '<f4'),
            ('scale_0', '<f4'), ('scale_1', '<f4'), ('scale_2', '<f4'),
            ('rot_0', '<f4'), ('rot_1', '<f4'), ('rot_2', '<f4'), ('rot_3', '<f4')
        ])
        data['x'] = points[:, 0]
        data['y'] = points[:, 1]
        data['z'] = points[:, 2]
        data['nx'] = 0.0
        data['ny'] = 0.0
        data['nz'] = 0.0
        data['f_dc_0'] = sh_dc[:, 0]
        data['f_dc_1'] = sh_dc[:, 1]
        data['f_dc_2'] = sh_dc[:, 2]
        data['opacity'] = logit_opacities
        data['scale_0'] = log_scales[:, 0]
        data['scale_1'] = log_scales[:, 1]
        data['scale_2'] = log_scales[:, 2]
        data['rot_0'] = rotations[:, 0]
        data['rot_1'] = rotations[:, 1]
        data['rot_2'] = rotations[:, 2]
        data['rot_3'] = rotations[:, 3]
        f.write(data.tobytes())
    print(f"[+] Đã tạo file 3DGS: {filename} ({N:,} hạt Gaussians)")


def generate_room0(n_points=35000, seed=42):
    """Mô phỏng scene Replica room0 (phòng khách): Sàn gỗ, tường, sofa, bàn, TV, thảm."""
    np.random.seed(seed)
    points_list, scales_list, rots_list, colors_list, opacities_list = [], [], [], [], []

    # 1. Sàn nhà (Floor: z = 0, x in [-2.5, 2.5], y in [-3.0, 3.0])
    n_floor = int(n_points * 0.25)
    fx = np.random.uniform(-2.5, 2.5, n_floor)
    fy = np.random.uniform(-3.0, 3.0, n_floor)
    fz = np.random.normal(0.0, 0.01, n_floor)
    f_pts = np.stack([fx, fy, fz], axis=-1)
    f_colors = np.random.uniform([0.72, 0.53, 0.38], [0.82, 0.63, 0.48], (n_floor, 3)) # Màu gỗ
    points_list.append(f_pts)
    colors_list.append(f_colors)

    # 2. Thảm trải sàn (Rug: x in [-1.2, 1.2], y in [-1.2, 1.2], z = 0.02)
    n_rug = int(n_points * 0.10)
    rx = np.random.uniform(-1.2, 1.2, n_rug)
    ry = np.random.uniform(-1.2, 1.2, n_rug)
    rz = np.random.normal(0.02, 0.005, n_rug)
    r_pts = np.stack([rx, ry, rz], axis=-1)
    r_colors = np.random.uniform([0.55, 0.20, 0.20], [0.65, 0.30, 0.30], (n_rug, 3)) # Màu thảm đỏ đô
    points_list.append(r_pts)
    colors_list.append(r_colors)

    # 3. Tường 4 phía (Walls: z in [0, 2.6])
    n_wall = int(n_points * 0.30)
    n_per_wall = n_wall // 4
    # Wall 1: y = 3.0
    w1 = np.stack([np.random.uniform(-2.5, 2.5, n_per_wall), np.random.normal(3.0, 0.02, n_per_wall), np.random.uniform(0.0, 2.6, n_per_wall)], axis=-1)
    # Wall 2: y = -3.0
    w2 = np.stack([np.random.uniform(-2.5, 2.5, n_per_wall), np.random.normal(-3.0, 0.02, n_per_wall), np.random.uniform(0.0, 2.6, n_per_wall)], axis=-1)
    # Wall 3: x = -2.5
    w3 = np.stack([np.random.normal(-2.5, 0.02, n_per_wall), np.random.uniform(-3.0, 3.0, n_per_wall), np.random.uniform(0.0, 2.6, n_per_wall)], axis=-1)
    # Wall 4: x = 2.5
    w4 = np.stack([np.random.normal(2.5, 0.02, n_per_wall), np.random.uniform(-3.0, 3.0, n_per_wall), np.random.uniform(0.0, 2.6, n_per_wall)], axis=-1)
    w_pts = np.concatenate([w1, w2, w3, w4], axis=0)
    w_colors = np.random.uniform([0.88, 0.88, 0.85], [0.95, 0.95, 0.92], (len(w_pts), 3)) # Màu tường trắng kem
    points_list.append(w_pts)
    colors_list.append(w_colors)

    # 4. Sofa góc (Sofa: x in [-1.8, -0.6], y in [1.5, 2.6], z in [0.0, 0.75])
    n_sofa = int(n_points * 0.15)
    sx = np.random.uniform(-1.8, -0.6, n_sofa)
    sy = np.random.uniform(1.5, 2.6, n_sofa)
    sz = np.random.uniform(0.0, 0.75, n_sofa)
    s_pts = np.stack([sx, sy, sz], axis=-1)
    s_colors = np.random.uniform([0.15, 0.25, 0.45], [0.25, 0.35, 0.55], (n_sofa, 3)) # Màu xanh navy
    points_list.append(s_pts)
    colors_list.append(s_colors)

    # 5. Bàn trà (Coffee Table: x in [-0.5, 0.5], y in [-0.4, 0.4], z in [0.0, 0.45])
    n_table = int(n_points * 0.08)
    tx = np.random.uniform(-0.5, 0.5, n_table)
    ty = np.random.uniform(-0.4, 0.4, n_table)
    tz = np.random.uniform(0.0, 0.45, n_table)
    t_pts = np.stack([tx, ty, tz], axis=-1)
    t_colors = np.random.uniform([0.35, 0.20, 0.12], [0.45, 0.30, 0.20], (n_table, 3)) # Gỗ nâu đậm
    points_list.append(t_pts)
    colors_list.append(t_colors)

    # 6. Kệ TV & TV (x in [-1.5, 1.5], y in [-2.9, -2.6], z in [0.0, 1.4])
    n_tv = n_points - sum(len(p) for p in points_list)
    tv_x = np.random.uniform(-1.5, 1.5, n_tv)
    tv_y = np.random.uniform(-2.9, -2.6, n_tv)
    tv_z = np.random.uniform(0.0, 1.4, n_tv)
    tv_pts = np.stack([tv_x, tv_y, tv_z], axis=-1)
    tv_colors = np.random.uniform([0.1, 0.1, 0.12], [0.2, 0.2, 0.22], (n_tv, 3)) # Đen xám TV
    points_list.append(tv_pts)
    colors_list.append(tv_colors)

    all_pts = np.concatenate(points_list, axis=0)
    all_colors = np.concatenate(colors_list, axis=0)
    N = len(all_pts)

    all_scales = np.random.uniform(0.015, 0.035, (N, 3))
    all_rots = np.zeros((N, 4))
    all_rots[:, 0] = 1.0 # quat (1, 0, 0, 0)
    all_opacities = np.random.uniform(0.85, 0.98, N)

    return all_pts, all_scales, all_rots, all_colors, all_opacities


def generate_office0(n_points=35000, seed=100):
    """Mô phỏng scene Replica office0 (văn phòng): Thảm xám, bàn làm việc, ghế xoay, màn hình, kệ sách."""
    np.random.seed(seed)
    points_list, scales_list, rots_list, colors_list, opacities_list = [], [], [], [], []

    # 1. Sàn văn phòng (Grey Carpet: z = 0, x in [-3.0, 3.0], y in [-2.5, 2.5])
    n_floor = int(n_points * 0.25)
    fx = np.random.uniform(-3.0, 3.0, n_floor)
    fy = np.random.uniform(-2.5, 2.5, n_floor)
    fz = np.random.normal(0.0, 0.01, n_floor)
    f_pts = np.stack([fx, fy, fz], axis=-1)
    f_colors = np.random.uniform([0.45, 0.48, 0.50], [0.55, 0.58, 0.60], (n_floor, 3)) # Thảm xám văn phòng
    points_list.append(f_pts)
    colors_list.append(f_colors)

    # 2. Tường văn phòng (Walls: z in [0, 2.8])
    n_wall = int(n_points * 0.30)
    n_per_wall = n_wall // 4
    w1 = np.stack([np.random.uniform(-3.0, 3.0, n_per_wall), np.random.normal(2.5, 0.02, n_per_wall), np.random.uniform(0.0, 2.8, n_per_wall)], axis=-1)
    w2 = np.stack([np.random.uniform(-3.0, 3.0, n_per_wall), np.random.normal(-2.5, 0.02, n_per_wall), np.random.uniform(0.0, 2.8, n_per_wall)], axis=-1)
    w3 = np.stack([np.random.normal(-3.0, 0.02, n_per_wall), np.random.uniform(-2.5, 2.5, n_per_wall), np.random.uniform(0.0, 2.8, n_per_wall)], axis=-1)
    w4 = np.stack([np.random.normal(3.0, 0.02, n_per_wall), np.random.uniform(-2.5, 2.5, n_per_wall), np.random.uniform(0.0, 2.8, n_per_wall)], axis=-1)
    w_pts = np.concatenate([w1, w2, w3, w4], axis=0)
    w_colors = np.random.uniform([0.85, 0.87, 0.89], [0.92, 0.94, 0.96], (len(w_pts), 3))
    points_list.append(w_pts)
    colors_list.append(w_colors)

    # 3. Hai cụm bàn làm việc lớn (Desks: x in [-1.5, 1.5], y in [-0.7, 0.7], z in [0.0, 0.75])
    n_desk = int(n_points * 0.20)
    dx = np.random.uniform(-1.8, 1.8, n_desk)
    dy = np.random.uniform(-0.8, 0.8, n_desk)
    dz = np.random.uniform(0.0, 0.75, n_desk)
    d_pts = np.stack([dx, dy, dz], axis=-1)
    d_colors = np.random.uniform([0.75, 0.65, 0.55], [0.85, 0.75, 0.65], (n_desk, 3)) # Mặt bàn sáng màu
    points_list.append(d_pts)
    colors_list.append(d_colors)

    # 4. Màn hình máy tính (Monitors: z in [0.75, 1.25])
    n_mon = int(n_points * 0.08)
    mx = np.random.uniform(-1.2, 1.2, n_mon)
    my = np.random.uniform(-0.2, 0.2, n_mon)
    mz = np.random.uniform(0.75, 1.25, n_mon)
    m_pts = np.stack([mx, my, mz], axis=-1)
    m_colors = np.random.uniform([0.05, 0.08, 0.15], [0.12, 0.20, 0.35], (n_mon, 3)) # Màn hình đen ánh xanh
    points_list.append(m_pts)
    colors_list.append(m_colors)

    # 5. Ghế xoay văn phòng & Kệ hồ sơ
    n_other = n_points - sum(len(p) for p in points_list)
    ox = np.random.uniform(-2.7, -2.0, n_other)
    oy = np.random.uniform(-2.0, 2.0, n_other)
    oz = np.random.uniform(0.0, 2.0, n_other)
    o_pts = np.stack([ox, oy, oz], axis=-1)
    o_colors = np.random.uniform([0.25, 0.25, 0.28], [0.40, 0.40, 0.45], (n_other, 3)) # Tủ kim loại
    points_list.append(o_pts)
    colors_list.append(o_colors)

    all_pts = np.concatenate(points_list, axis=0)
    all_colors = np.concatenate(colors_list, axis=0)
    N = len(all_pts)

    all_scales = np.random.uniform(0.015, 0.035, (N, 3))
    all_rots = np.zeros((N, 4))
    all_rots[:, 0] = 1.0
    all_opacities = np.random.uniform(0.85, 0.98, N)

    return all_pts, all_scales, all_rots, all_colors, all_opacities


if __name__ == "__main__":
    out_dir = r"D:\Cuda\Sprint02\models"
    res_dir = r"D:\Cuda\results"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    # 1. room0 (full: 35k, half: 15k)
    p, s, r, c, o = generate_room0(35000, seed=42)
    room0_full = os.path.join(out_dir, "room0.ply")
    create_3dgs_ply(room0_full, p, s, r, c, o)
    shutil.copy(room0_full, os.path.join(res_dir, "room0.ply"))

    p_h, s_h, r_h, c_h, o_h = generate_room0(15000, seed=42)
    create_3dgs_ply(os.path.join(out_dir, "room0_half.ply"), p_h, s_h, r_h, c_h, o_h)

    # 2. office0 (full: 35k, half: 15k)
    p_off, s_off, r_off, c_off, o_off = generate_office0(35000, seed=100)
    office0_full = os.path.join(out_dir, "office0.ply")
    create_3dgs_ply(office0_full, p_off, s_off, r_off, c_off, o_off)
    shutil.copy(office0_full, os.path.join(res_dir, "office0.ply"))

    p_off_h, s_off_h, r_off_h, c_off_h, o_off_h = generate_office0(15000, seed=100)
    create_3dgs_ply(os.path.join(out_dir, "office0_half.ply"), p_off_h, s_off_h, r_off_h, c_off_h, o_off_h)

    print("\n[V] Hoàn tất sinh 4 mô hình 3DGS (.ply) cho Pilot P2!")

