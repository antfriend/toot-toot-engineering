"""Procedurally generate a Marioland-inspired bonsai STL for 3D printing.

Approach (deterministic):
- Build an occupancy voxel field for: pot + soil mound + root flare + twisting trunk + canopy puffs.
- Extract a watertight surface using marching cubes (via scikit-image) from a *padded* volume.
- Keep the largest connected component.
- Write binary STL.

Dependencies (install):
  pip install numpy scikit-image

Optional validation:
  pip install trimesh

Usage:
  python generate_bonsai.py --out ../output/bonsai_marioland.stl
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Params:
    # Overall target size
    height_mm: float = 80.0

    # Voxel resolution controls detail and runtime
    voxel_size_mm: float = 0.6  # 0.5-0.8 is a good range

    # Bounding box padding
    pad_mm: float = 4.0

    # Pot
    pot_radius_mm: float = 18.0
    pot_height_mm: float = 18.0
    pot_wall_mm: float = 2.4
    pot_lip_mm: float = 2.0

    # Soil mound
    soil_height_mm: float = 6.0

    # Trunk
    trunk_base_radius_mm: float = 5.5
    trunk_top_radius_mm: float = 2.5
    trunk_height_mm: float = 42.0
    trunk_sway_mm: float = 9.0

    # Canopy
    canopy_center_height_mm: float = 60.0
    canopy_radius_mm: float = 18.0

    seed: int = 1337


def add_sphere(occ: np.ndarray, X, Y, Z, cx, cy, cz, r, soften=0.0):
    d2 = (X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2
    if soften <= 0:
        occ |= d2 <= r * r
    else:
        occ |= d2 <= (r + soften) ** 2


def add_cylinder_z(occ: np.ndarray, X, Y, Z, cx, cy, z0, z1, r):
    inside_z = (Z >= z0) & (Z <= z1)
    d2 = (X - cx) ** 2 + (Y - cy) ** 2
    occ |= inside_z & (d2 <= r * r)


def add_conical_trunk(occ: np.ndarray, X, Y, Z, p: Params, z0, z1, sway_x, sway_y):
    z = Z
    t = np.clip((z - z0) / (z1 - z0), 0.0, 1.0)
    cx = sway_x * np.sin(t * math.pi * 0.9)
    cy = sway_y * np.sin(t * math.pi * 0.7 + 0.6)

    r = (1.0 - t) * p.trunk_base_radius_mm + t * p.trunk_top_radius_mm

    # bark grooves: low-frequency radial modulation
    ang = np.arctan2(Y - cy, X - cx)
    grooves = 0.65 * np.sin(ang * 6.0 + t * 9.0) + 0.35 * np.sin(ang * 11.0 - t * 5.0)
    r_mod = r * (1.0 + 0.10 * grooves)

    inside_z = (z >= z0) & (z <= z1)
    d2 = (X - cx) ** 2 + (Y - cy) ** 2
    occ |= inside_z & (d2 <= r_mod * r_mod)


def largest_component_mask(occ: np.ndarray) -> np.ndarray:
    """Keep the largest 6-connected component in a boolean 3D volume."""
    from collections import deque

    filled = occ
    visited = np.zeros_like(filled, dtype=bool)

    dims = filled.shape
    neigh = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    best_count = 0
    best_voxels = None

    it = np.argwhere(filled)
    for (i, j, k) in it:
        if visited[i, j, k]:
            continue
        # BFS
        q = deque([(i, j, k)])
        visited[i, j, k] = True
        voxels = [(i, j, k)]
        while q:
            a, b, c = q.popleft()
            for di, dj, dk in neigh:
                ni, nj, nk = a + di, b + dj, c + dk
                if ni < 0 or nj < 0 or nk < 0 or ni >= dims[0] or nj >= dims[1] or nk >= dims[2]:
                    continue
                if visited[ni, nj, nk] or (not filled[ni, nj, nk]):
                    continue
                visited[ni, nj, nk] = True
                q.append((ni, nj, nk))
                voxels.append((ni, nj, nk))
        if len(voxels) > best_count:
            best_count = len(voxels)
            best_voxels = voxels

    out = np.zeros_like(filled, dtype=bool)
    if best_voxels is not None:
        ii, jj, kk = zip(*best_voxels)
        out[np.array(ii), np.array(jj), np.array(kk)] = True
    return out


def build_occupancy(p: Params):
    rng = np.random.default_rng(p.seed)

    max_r = max(p.pot_radius_mm + p.pad_mm, p.canopy_radius_mm + p.pad_mm)
    z_max = p.height_mm + p.pad_mm
    z_min = -p.pad_mm

    vx = p.voxel_size_mm
    xs = np.arange(-max_r, max_r + vx, vx)
    ys = np.arange(-max_r, max_r + vx, vx)
    zs = np.arange(z_min, z_max + vx, vx)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="xy")

    occ = np.zeros(X.shape, dtype=bool)

    # Pot shell
    outer_r = p.pot_radius_mm
    inner_r = max(outer_r - p.pot_wall_mm, 0.1)
    z0 = 0.0
    z1 = p.pot_height_mm

    add_cylinder_z(occ, X, Y, Z, 0.0, 0.0, z0, z1, outer_r)

    interior = np.zeros_like(occ)
    add_cylinder_z(interior, X, Y, Z, 0.0, 0.0, z0 + p.pot_wall_mm, z1 - p.pot_wall_mm, inner_r)
    occ &= ~interior

    # lip beads
    lip_z = z1 - p.pot_lip_mm * 0.5
    ring_r = (outer_r + inner_r) * 0.5
    bead_r = p.pot_lip_mm * 0.65
    for k in range(24):
        a = (k / 24.0) * 2.0 * math.pi
        cx = ring_r * math.cos(a)
        cy = ring_r * math.sin(a)
        add_sphere(occ, X, Y, Z, cx, cy, lip_z, bead_r, soften=0.2)

    # Soil mound
    mound_cz = z1 + p.soil_height_mm * 0.25
    mound_r = inner_r * 0.95
    add_sphere(occ, X, Y, Z, 0.0, 0.0, mound_cz, mound_r)

    # Root flare
    flare_z = z1 + p.soil_height_mm * 0.8
    for k in range(6):
        a = (k / 6.0) * 2.0 * math.pi
        rr = p.trunk_base_radius_mm * 1.25
        cx = (rr * 0.9) * math.cos(a)
        cy = (rr * 0.9) * math.sin(a)
        add_sphere(occ, X, Y, Z, cx, cy, flare_z, rr * 0.75, soften=0.4)

    # Trunk
    trunk_z0 = z1 + p.soil_height_mm * 0.6
    trunk_z1 = trunk_z0 + p.trunk_height_mm
    add_conical_trunk(
        occ,
        X,
        Y,
        Z,
        p,
        trunk_z0,
        trunk_z1,
        sway_x=p.trunk_sway_mm,
        sway_y=p.trunk_sway_mm * 0.5,
    )

    # Canopy puffs
    canopy_cz = p.canopy_center_height_mm
    canopy_r = p.canopy_radius_mm

    for _ in range(14):
        u = rng.uniform(0, 1)
        v = rng.uniform(0, 1)
        theta = 2 * math.pi * u
        phi = math.acos(2 * v - 1)
        rad = rng.uniform(0.35, 0.95) * canopy_r
        cx = rad * math.sin(phi) * math.cos(theta)
        cy = rad * math.sin(phi) * math.sin(theta)
        cz = canopy_cz + (rad * math.cos(phi)) * 0.55
        r = rng.uniform(5.5, 9.5)
        add_sphere(occ, X, Y, Z, cx, cy, cz, r, soften=0.4)

    add_sphere(occ, X, Y, Z, 3.0, 0.0, trunk_z1 + 2.0, 7.0, soften=0.4)
    add_sphere(occ, X, Y, Z, -2.5, 1.0, trunk_z1 - 2.0, 6.0, soften=0.4)

    # Canopy dimples: subtract cavities above trunk area
    cavities = np.zeros_like(occ)
    for _ in range(26):
        u = rng.uniform(0, 1)
        v = rng.uniform(0, 1)
        theta = 2 * math.pi * u
        phi = math.acos(2 * v - 1)
        rad = rng.uniform(0.45, 0.95) * canopy_r
        cx = rad * math.sin(phi) * math.cos(theta)
        cy = rad * math.sin(phi) * math.sin(theta)
        cz = canopy_cz + (rad * math.cos(phi)) * 0.55
        r = rng.uniform(2.0, 3.0)
        add_sphere(cavities, X, Y, Z, cx, cy, cz, r, soften=0.0)

    canopy_zone = Z >= (trunk_z1 - 6.0)
    occ &= ~(cavities & canopy_zone)

    # Keep only the largest connected component to remove any tiny detached islands.
    occ = largest_component_mask(occ)

    return occ, vx


def marching_cubes_mesh(occ: np.ndarray, voxel_size: float):
    from skimage import measure

    # Pad with empty voxels to avoid open surfaces when shapes touch the grid border.
    vol = np.pad(occ.astype(np.uint8), pad_width=2, mode="constant", constant_values=0)

    verts, faces, _normals, _ = measure.marching_cubes(vol, level=0.5, spacing=(voxel_size, voxel_size, voxel_size))

    # skimage returns coords in array order (row, col, plane) -> (y, x, z)
    verts = verts[:, [1, 0, 2]]

    # remove pad offset
    verts -= np.array([2 * voxel_size, 2 * voxel_size, 2 * voxel_size])
    return verts, faces


def write_binary_stl(path: Path, verts: np.ndarray, faces: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)

    header = b"toot-toot-engineering bonsai_marioland".ljust(80, b" ")
    tri_count = np.uint32(len(faces))

    with path.open("wb") as f:
        f.write(header)
        f.write(tri_count.tobytes())
        for face in faces:
            v0, v1, v2 = verts[face[0]], verts[face[1]], verts[face[2]]
            n = np.cross(v1 - v0, v2 - v0)
            norm = np.linalg.norm(n)
            if norm > 0:
                n = n / norm
            else:
                n = np.array([0.0, 0.0, 1.0], dtype=np.float32)
            f.write(np.asarray(n, dtype=np.float32).tobytes())
            f.write(np.asarray(v0, dtype=np.float32).tobytes())
            f.write(np.asarray(v1, dtype=np.float32).tobytes())
            f.write(np.asarray(v2, dtype=np.float32).tobytes())
            f.write(np.uint16(0).tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default=str(Path(__file__).resolve().parent.parent / "output" / "bonsai_marioland.stl"))
    ap.add_argument("--voxel", type=float, default=Params.voxel_size_mm)
    ap.add_argument("--height", type=float, default=Params.height_mm)
    ap.add_argument("--seed", type=int, default=Params.seed)
    args = ap.parse_args()

    p = Params(height_mm=float(args.height), voxel_size_mm=float(args.voxel), seed=int(args.seed))

    occ, vx = build_occupancy(p)
    verts, faces = marching_cubes_mesh(occ, vx)

    # center X/Y around origin; put base at Z=0
    verts[:, 0] -= np.mean(verts[:, 0])
    verts[:, 1] -= np.mean(verts[:, 1])
    verts[:, 2] -= np.min(verts[:, 2])

    out_path = Path(args.out)
    write_binary_stl(out_path, verts, faces)

    print(f"Wrote {out_path}")
    mins = verts.min(axis=0)
    maxs = verts.max(axis=0)
    print(f"Bounds (mm): min={mins}, max={maxs}, size={maxs-mins}")

    # Optional validation
    try:
        import trimesh

        m = trimesh.load_mesh(out_path, force="mesh")
        print("trimesh: watertight=", bool(m.is_watertight), " euler=", int(m.euler_number), " components=", len(m.split(only_watertight=False)))
    except Exception as e:
        print("Validation skipped (trimesh not available):", e)


if __name__ == "__main__":
    main()
