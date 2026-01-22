"""Generate a 12-frame Marioland-style bonsai growth zoetrope STL.

This script produces a single combined STL:
  deliverables/cycle-01/output/bonsai-zoetrope.stl

No third-party dependencies.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass


@dataclass
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vec3") -> "Vec3":
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, s: float) -> "Vec3":
        return Vec3(self.x * s, self.y * s, self.z * s)


def cross(a: Vec3, b: Vec3) -> Vec3:
    return Vec3(
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x,
    )


def normalize(v: Vec3) -> Vec3:
    l = math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
    if l == 0:
        return Vec3(0.0, 0.0, 0.0)
    return Vec3(v.x / l, v.y / l, v.z / l)


@dataclass
class Tri:
    a: Vec3
    b: Vec3
    c: Vec3


def tri_normal(t: Tri) -> Vec3:
    return normalize(cross(t.b - t.a, t.c - t.a))


def rotate_z(p: Vec3, ang: float) -> Vec3:
    ca = math.cos(ang)
    sa = math.sin(ang)
    return Vec3(p.x * ca - p.y * sa, p.x * sa + p.y * ca, p.z)


def translate(tris: list[Tri], off: Vec3) -> list[Tri]:
    return [Tri(t.a + off, t.b + off, t.c + off) for t in tris]


def rotate_tris_z(tris: list[Tri], ang: float) -> list[Tri]:
    return [Tri(rotate_z(t.a, ang), rotate_z(t.b, ang), rotate_z(t.c, ang)) for t in tris]


def write_ascii_stl(path: str, tris: list[Tri], name: str = "solid") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"solid {name}\n")
        for t in tris:
            n = tri_normal(t)
            f.write(f"  facet normal {n.x:.6e} {n.y:.6e} {n.z:.6e}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {t.a.x:.6e} {t.a.y:.6e} {t.a.z:.6e}\n")
            f.write(f"      vertex {t.b.x:.6e} {t.b.y:.6e} {t.b.z:.6e}\n")
            f.write(f"      vertex {t.c.x:.6e} {t.c.y:.6e} {t.c.z:.6e}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {name}\n")


def cylinder_z(r: float, h: float, seg: int, z0: float = 0.0) -> list[Tri]:
    tris: list[Tri] = []
    # sides
    for i in range(seg):
        a0 = 2 * math.pi * i / seg
        a1 = 2 * math.pi * (i + 1) / seg
        p00 = Vec3(r * math.cos(a0), r * math.sin(a0), z0)
        p01 = Vec3(r * math.cos(a1), r * math.sin(a1), z0)
        p10 = Vec3(r * math.cos(a0), r * math.sin(a0), z0 + h)
        p11 = Vec3(r * math.cos(a1), r * math.sin(a1), z0 + h)
        tris.append(Tri(p00, p01, p11))
        tris.append(Tri(p00, p11, p10))

    # bottom (normal down)
    cb = Vec3(0.0, 0.0, z0)
    for i in range(seg):
        a0 = 2 * math.pi * i / seg
        a1 = 2 * math.pi * (i + 1) / seg
        p0 = Vec3(r * math.cos(a0), r * math.sin(a0), z0)
        p1 = Vec3(r * math.cos(a1), r * math.sin(a1), z0)
        tris.append(Tri(cb, p1, p0))

    # top (normal up)
    ct = Vec3(0.0, 0.0, z0 + h)
    for i in range(seg):
        a0 = 2 * math.pi * i / seg
        a1 = 2 * math.pi * (i + 1) / seg
        p0 = Vec3(r * math.cos(a0), r * math.sin(a0), z0 + h)
        p1 = Vec3(r * math.cos(a1), r * math.sin(a1), z0 + h)
        tris.append(Tri(ct, p0, p1))

    return tris


def sphere(center: Vec3, r: float, lon: int, lat: int) -> list[Tri]:
    tris: list[Tri] = []
    for j in range(lat):
        t0 = math.pi * j / lat
        t1 = math.pi * (j + 1) / lat
        for i in range(lon):
            p0 = 2 * math.pi * i / lon
            p1 = 2 * math.pi * (i + 1) / lon

            def pt(theta: float, phi: float) -> Vec3:
                # theta: 0..pi, phi:0..2pi
                return Vec3(
                    center.x + r * math.sin(theta) * math.cos(phi),
                    center.y + r * math.sin(theta) * math.sin(phi),
                    center.z + r * math.cos(theta),
                )

            a = pt(t0, p0)
            b = pt(t0, p1)
            c = pt(t1, p1)
            d = pt(t1, p0)

            # skip degenerate caps by only adding valid triangles
            if j != 0:
                tris.append(Tri(a, c, b))
            if j != lat - 1:
                tris.append(Tri(a, d, c))
    return tris


def make_platform(diam: float = 160.0, thickness: float = 6.0, rim_t: float = 4.0, rim_h: float = 8.0) -> list[Tri]:
    r = diam / 2.0
    seg = 192
    base = cylinder_z(r=r, h=thickness, seg=seg, z0=0.0)
    rim = cylinder_z(r=r, h=rim_h, seg=seg, z0=thickness)
    return base + rim


def make_pad(r: float = 11.0, h: float = 2.0, z0: float = 6.0) -> list[Tri]:
    return cylinder_z(r=r, h=h, seg=64, z0=z0)


def make_bonsai_stage(stage: int) -> list[Tri]:
    """A chunky, printable bonsai approximation.

    Built from stacked spheres (foliage puffs) + stacked cylinders (trunk/root).
    It is stylized and intended to be manifold as a *union-like overlap* mesh.
    """

    # stage 1..12
    s = max(1, min(12, stage))
    t = (s - 1) / 11.0

    tris: list[Tri] = []

    # roots/base bulb
    root_r = 6.0 + 2.5 * t
    tris += sphere(Vec3(0.0, 0.0, 6.0 + 2.0 + root_r * 0.75), root_r, lon=36, lat=18)

    # trunk: stacked cylinders with gentle S-bend via lateral offsets
    trunk_h = 10.0 + 35.0 * t
    base_r = 5.0 + 2.0 * t
    top_r = 3.0 + 1.0 * t
    segments = 5
    for k in range(segments):
        z0 = 6.0 + 2.0 + (trunk_h * k / segments)
        h = trunk_h / segments
        rk = base_r + (top_r - base_r) * (k / (segments - 1))
        # s-curve offset
        ox = (2.5 + 2.0 * t) * math.sin((k / (segments - 1)) * math.pi * 1.2) * (0.6 + 0.4 * t)
        oy = (1.8 + 1.0 * t) * math.sin((k / (segments - 1)) * math.pi * 0.9 + 0.8) * (0.6 + 0.4 * t)
        seg_tris = cylinder_z(r=rk, h=h, seg=48, z0=z0)
        tris += translate(seg_tris, Vec3(ox, oy, 0.0))

        # bark knots (deep texture bumps)
        if s >= 4 and k in (1, 3):
            kr = 1.3 + 0.6 * t
            kz = z0 + h * 0.5
            tris += sphere(Vec3(ox + rk * 0.7, oy, kz), kr, lon=18, lat=10)

    # foliage puffs: increase count and size over stages
    puff_count = 1 if s <= 2 else (2 if s <= 3 else (3 if s <= 5 else (4 if s <= 8 else 5)))
    canopy_scale = 0.55 + 0.85 * t
    top_z = 6.0 + 2.0 + trunk_h + 4.0
    for i in range(puff_count):
        ang = (i / puff_count) * 2 * math.pi
        pr = (7.0 + 5.0 * t) * canopy_scale * (0.95 - 0.08 * i)
        px = (6.0 + 4.0 * t) * canopy_scale * math.cos(ang) * (0.7 if i else 0.2)
        py = (6.0 + 4.0 * t) * canopy_scale * math.sin(ang) * (0.7 if i else 0.2)
        pz = top_z - 2.0 * i + (1.5 if i == 0 else 0.0)
        tris += sphere(Vec3(px, py, pz), pr, lon=36, lat=18)

        # scallop bumps for "leaf" texture
        if s >= 6:
            for b in range(6):
                ba = ang + (b / 6) * 2 * math.pi
                br = 1.2 + 0.8 * t
                bx = px + (pr * 0.75) * math.cos(ba)
                by = py + (pr * 0.75) * math.sin(ba)
                bz = pz + (pr * 0.15) * math.cos(b)
                tris += sphere(Vec3(bx, by, bz), br, lon=14, lat=10)

    return tris


def main() -> None:
    # per GEOMETRY_SPEC defaults
    platform_d = 160.0
    platform_th = 6.0
    pad_r = 11.0
    pad_h = 2.0
    frame_count = 12

    all_tris: list[Tri] = []
    all_tris += make_platform(diam=platform_d, thickness=platform_th)

    # place frames around radius
    ring_r = 55.0
    for i in range(frame_count):
        ang = (i / frame_count) * 2 * math.pi
        cx = ring_r * math.cos(ang)
        cy = ring_r * math.sin(ang)

        pad = translate(make_pad(r=pad_r, h=pad_h, z0=platform_th), Vec3(cx, cy, 0.0))
        all_tris += pad

        tree = make_bonsai_stage(i + 1)
        # orient each tree to face outward consistently
        tree = rotate_tris_z(tree, ang)
        tree = translate(tree, Vec3(cx, cy, 0.0))
        all_tris += tree

    out_path = "deliverables/cycle-01/output/bonsai-zoetrope.stl"
    write_ascii_stl(out_path, all_tris, name="bonsai_zoetrope")

    # optional per-frame outputs (small convenience)
    for i in range(frame_count):
        ang = (i / frame_count) * 2 * math.pi
        cx = ring_r * math.cos(ang)
        cy = ring_r * math.sin(ang)
        frame_tris: list[Tri] = []
        frame_tris += translate(make_pad(r=pad_r, h=pad_h, z0=platform_th), Vec3(cx, cy, 0.0))
        tree = translate(rotate_tris_z(make_bonsai_stage(i + 1), ang), Vec3(cx, cy, 0.0))
        frame_tris += tree
        write_ascii_stl(
            f"deliverables/cycle-01/output/frame-{i+1:02d}.stl",
            frame_tris,
            name=f"frame_{i+1:02d}",
        )


if __name__ == "__main__":
    main()
