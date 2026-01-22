"""Procedural bonsai STL generator (cycle-01)

Goal: produce a 3D-printable, watertight-ish(see notes), cartoony platformer-world
bonsai (trunk + branches + canopy + pot/base) and export to STL.

This script avoids heavy deps (no trimesh). It writes a *binary STL* directly.

Modeling approach:
- Pot/base: simple cylinder with a top rim.
- Trunk/branches: swept tubes along polyline centerlines.
- Canopy: union of lobes (spheres). Instead of true boolean union (needs libs),
  we rely on heavy overlap and accept internal faces; most slicers tolerate this,
  but it's not ideal.

If you have mesh boolean tooling available later, you can post-process to a
single watertight solid.

Usage:
  python generate_bonsai.py --out ../output/bonsai_marioland_smooth.stl

"""

from __future__ import annotations

import argparse
import math
import os
import struct
from dataclasses import dataclass

import numpy as np


# --------------------------- STL writing ---------------------------

def write_binary_stl(path: str, triangles: np.ndarray) -> None:
    """Write triangles (N, 3, 3) float32/float64 to binary STL."""
    triangles = np.asarray(triangles, dtype=np.float32)
    n = triangles.shape[0]

    header = b"Toot-Toot Engineering bonsai (cycle-01)".ljust(80, b" ")
    with open(path, "wb") as f:
        f.write(header)
        f.write(struct.pack("<I", n))
        for tri in triangles:
            v1, v2, v3 = tri
            # normal (compute, but slicers don't really need it)
            nrm = np.cross(v2 - v1, v3 - v1)
            norm = float(np.linalg.norm(nrm))
            if norm > 1e-12:
                nrm = nrm / norm
            else:
                nrm = np.array([0.0, 0.0, 0.0], dtype=np.float32)
            f.write(struct.pack("<3f", *nrm.astype(np.float32)))
            f.write(struct.pack("<3f", *v1.astype(np.float32)))
            f.write(struct.pack("<3f", *v2.astype(np.float32)))
            f.write(struct.pack("<3f", *v3.astype(np.float32)))
            f.write(struct.pack("<H", 0))


# --------------------------- geometry utils ---------------------------

@dataclass
class Mesh:
    vertices: list[np.ndarray]
    faces: list[tuple[int, int, int]]

    def __init__(self):
        self.vertices = []
        self.faces = []

    def add_vertex(self, v: np.ndarray) -> int:
        self.vertices.append(np.asarray(v, dtype=np.float32))
        return len(self.vertices) - 1

    def add_tri(self, a: int, b: int, c: int) -> None:
        self.faces.append((a, b, c))

    def extend(self, other: "Mesh") -> None:
        base = len(self.vertices)
        self.vertices.extend(other.vertices)
        self.faces.extend([(a + base, b + base, c + base) for (a, b, c) in other.faces])

    def to_triangles(self) -> np.ndarray:
        v = np.stack(self.vertices, axis=0)
        tris = np.zeros((len(self.faces), 3, 3), dtype=np.float32)
        for i, (a, b, c) in enumerate(self.faces):
            tris[i, 0] = v[a]
            tris[i, 1] = v[b]
            tris[i, 2] = v[c]
        return tris


def normalize(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n < 1e-12:
        return v * 0.0
    return v / n


def rotation_matrix_from_z(direction: np.ndarray) -> np.ndarray:
    """Return 3x3 rotation matrix that maps +Z to 'direction'."""
    d = normalize(direction)
    z = np.array([0.0, 0.0, 1.0], dtype=np.float32)
    if np.linalg.norm(d - z) < 1e-6:
        return np.eye(3, dtype=np.float32)
    if np.linalg.norm(d + z) < 1e-6:
        # 180 deg flip around X
        return np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=np.float32)
    v = np.cross(z, d)
    s = float(np.linalg.norm(v))
    c = float(np.dot(z, d))
    vx = np.array(
        [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]], dtype=np.float32
    )
    r = np.eye(3, dtype=np.float32) + vx + (vx @ vx) * ((1 - c) / (s * s))
    return r.astype(np.float32)


# --------------------------- primitives ---------------------------

def make_cylinder(radius: float, height: float, segments: int = 64, z0: float = 0.0) -> Mesh:
    """Closed cylinder aligned to +Z with bottom at z0."""
    m = Mesh()
    # rings
    angles = np.linspace(0, 2 * math.pi, segments, endpoint=False)
    bottom = []
    top = []
    for a in angles:
        x = radius * math.cos(a)
        y = radius * math.sin(a)
        bottom.append(m.add_vertex(np.array([x, y, z0], dtype=np.float32)))
        top.append(m.add_vertex(np.array([x, y, z0 + height], dtype=np.float32)))
    # sides
    for i in range(segments):
        j = (i + 1) % segments
        m.add_tri(bottom[i], bottom[j], top[j])
        m.add_tri(bottom[i], top[j], top[i])
    # caps
    cbot = m.add_vertex(np.array([0, 0, z0], dtype=np.float32))
    ctop = m.add_vertex(np.array([0, 0, z0 + height], dtype=np.float32))
    for i in range(segments):
        j = (i + 1) % segments
        # bottom (clockwise when viewed from below)
        m.add_tri(cbot, bottom[j], bottom[i])
        # top
        m.add_tri(ctop, top[i], top[j])
    return m


def make_uv_sphere(center: np.ndarray, radius: float, u_segments: int = 40, v_segments: int = 24) -> Mesh:
    m = Mesh()
    u = np.linspace(0, 2 * math.pi, u_segments, endpoint=False)
    v = np.linspace(0, math.pi, v_segments + 1, endpoint=True)
    vid = [[None] * u_segments for _ in range(v_segments + 1)]
    for vi, vv in enumerate(v):
        for ui, uu in enumerate(u):
            x = radius * math.cos(uu) * math.sin(vv)
            y = radius * math.sin(uu) * math.sin(vv)
            z = radius * math.cos(vv)
            vid[vi][ui] = m.add_vertex(center + np.array([x, y, z], dtype=np.float32))
    for vi in range(v_segments):
        for ui in range(u_segments):
            uj = (ui + 1) % u_segments
            a = vid[vi][ui]
            b = vid[vi][uj]
            c = vid[vi + 1][uj]
            d = vid[vi + 1][ui]
            if vi != 0:
                m.add_tri(a, b, c)
            if vi != v_segments - 1:
                m.add_tri(a, c, d)
    return m


def make_tube_along_polyline(points: np.ndarray, radii: np.ndarray, segments: int = 28) -> Mesh:
    """Create a closed tube by connecting circles along polyline points.

    points: (K,3), radii: (K,)
    """
    m = Mesh()
    k = points.shape[0]
    angles = np.linspace(0, 2 * math.pi, segments, endpoint=False)

    rings: list[list[int]] = []
    for i in range(k):
        p = points[i]
        # tangent
        if i == 0:
            t = points[i + 1] - points[i]
        elif i == k - 1:
            t = points[i] - points[i - 1]
        else:
            t = points[i + 1] - points[i - 1]
        rmat = rotation_matrix_from_z(t)
        ring = []
        rad = float(radii[i])
        for a in angles:
            local = np.array([rad * math.cos(a), rad * math.sin(a), 0.0], dtype=np.float32)
            v = p + (rmat @ local)
            ring.append(m.add_vertex(v))
        rings.append(ring)

    # connect rings
    for i in range(k - 1):
        r0 = rings[i]
        r1 = rings[i + 1]
        for s in range(segments):
            sj = (s + 1) % segments
            m.add_tri(r0[s], r0[sj], r1[sj])
            m.add_tri(r0[s], r1[sj], r1[s])

    # cap ends
    c0 = m.add_vertex(points[0])
    c1 = m.add_vertex(points[-1])
    r0 = rings[0]
    r1 = rings[-1]
    for s in range(segments):
        sj = (s + 1) % segments
        # start cap
        m.add_tri(c0, r0[sj], r0[s])
        # end cap
        m.add_tri(c1, r1[s], r1[sj])

    return m


# --------------------------- bonsai generator ---------------------------

def generate_bonsai(
    seed: int = 1,
    total_height_mm: float = 90,
    base_diameter_mm: float = 55,
    base_height_mm: float = 22,
    trunk_base_radius_mm: float = 9,
    trunk_top_radius_mm: float = 5,
    branch_count: int = 5,
    branch_radius_mm: float = 3.0,
    canopy_lobe_count: int = 7,
) -> Mesh:
    rng = np.random.default_rng(seed)

    m = Mesh()

    # base pot
    base_r = base_diameter_mm * 0.5
    pot = make_cylinder(radius=base_r, height=base_height_mm, segments=96, z0=0.0)
    # rim as a thin larger cylinder section
    rim = make_cylinder(radius=base_r * 1.03, height=2.2, segments=96, z0=base_height_mm - 2.2)
    m.extend(pot)
    m.extend(rim)

    # trunk centerline (S-curve)
    trunk_h = total_height_mm - base_height_mm
    k = 9
    zs = np.linspace(0.0, trunk_h, k)
    xs = 6.5 * np.sin(zs / trunk_h * math.pi * 1.1)
    ys = 4.0 * np.sin(zs / trunk_h * math.pi * 0.7 + 0.6)
    pts = np.stack([xs, ys, zs + base_height_mm], axis=1).astype(np.float32)
    radii = np.linspace(trunk_base_radius_mm, trunk_top_radius_mm, k).astype(np.float32)
    trunk = make_tube_along_polyline(pts, radii, segments=32)
    m.extend(trunk)

    # branches
    for bi in range(branch_count):
        t = (bi + 1) / (branch_count + 1)
        idx = int(t * (k - 3)) + 1
        p0 = pts[idx]
        # direction: outward and up
        ang = float(rng.uniform(0, 2 * math.pi))
        out = np.array([math.cos(ang), math.sin(ang), 0.0], dtype=np.float32)
        up = np.array([0.0, 0.0, 1.0], dtype=np.float32)
        d = normalize(out * float(rng.uniform(0.8, 1.2)) + up * float(rng.uniform(0.9, 1.2)))
        length = float(rng.uniform(16, 26))
        p1 = p0 + d * (0.55 * length)
        p2 = p0 + d * length
        bpts = np.stack([p0, p1, p2], axis=0)
        br0 = max(branch_radius_mm, 2.0)
        br2 = max(branch_radius_mm * 0.72, 1.8)
        bradii = np.array([br0, (br0 + br2) * 0.5, br2], dtype=np.float32)
        branch = make_tube_along_polyline(bpts, bradii, segments=24)
        m.extend(branch)

    # canopy lobes near top
    canopy_center = pts[-1] + np.array([0.0, 0.0, 8.0], dtype=np.float32)
    for i in range(canopy_lobe_count):
        a = float(rng.uniform(0, 2 * math.pi))
        r = float(rng.uniform(0.0, 12.0))
        z = float(rng.uniform(-6.0, 8.0))
        offset = np.array([math.cos(a) * r, math.sin(a) * r, z], dtype=np.float32)
        rad = float(rng.uniform(10.0, 16.0))
        lobe = make_uv_sphere(canopy_center + offset, rad, u_segments=36, v_segments=20)
        m.extend(lobe)

    return m


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output STL path")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    mesh = generate_bonsai(seed=args.seed)
    triangles = mesh.to_triangles()

    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    write_binary_stl(out_path, triangles)

    print(f"Wrote {out_path}")
    print(f"Triangles: {triangles.shape[0]}")
    print("NOTE: This mesh is a stitched assembly of overlapping solids (no boolean union).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
