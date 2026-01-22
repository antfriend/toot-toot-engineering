"""Generate a bonsai-growth zoetrope STL (cycle-01).

No external deps required.

The model is a circular base (with 30mm center hole) plus 12 small
sculptures around the perimeter representing growth stages.

Units: millimeters.

Usage:
  python deliverables/cycle-01/src/generate_zoetrope.py \
    --out deliverables/cycle-01/output/bonsai_zoetrope.stl
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

Vec3 = Tuple[float, float, float]
Tri = Tuple[Vec3, Vec3, Vec3]


def v_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def v_norm(a: Vec3) -> Vec3:
    l = math.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2) or 1.0
    return (a[0] / l, a[1] / l, a[2] / l)


def rotate_z(p: Vec3, ang: float) -> Vec3:
    ca, sa = math.cos(ang), math.sin(ang)
    return (p[0] * ca - p[1] * sa, p[0] * sa + p[1] * ca, p[2])


def translate(tris: Iterable[Tri], t: Vec3) -> List[Tri]:
    return [(v_add(a, t), v_add(b, t), v_add(c, t)) for (a, b, c) in tris]


def rotate_tris_z(tris: Iterable[Tri], ang: float) -> List[Tri]:
    return [(rotate_z(a, ang), rotate_z(b, ang), rotate_z(c, ang)) for (a, b, c) in tris]


def cylinder_shell(r_outer: float, r_inner: float, h: float, n: int = 192) -> List[Tri]:
    """Closed ring: outer wall + inner wall + top and bottom annuli."""
    tris: List[Tri] = []
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 1) / n

        ob0 = (r_outer * math.cos(a0), r_outer * math.sin(a0), 0.0)
        ob1 = (r_outer * math.cos(a1), r_outer * math.sin(a1), 0.0)
        ot0 = (ob0[0], ob0[1], h)
        ot1 = (ob1[0], ob1[1], h)

        ib0 = (r_inner * math.cos(a0), r_inner * math.sin(a0), 0.0)
        ib1 = (r_inner * math.cos(a1), r_inner * math.sin(a1), 0.0)
        it0 = (ib0[0], ib0[1], h)
        it1 = (ib1[0], ib1[1], h)

        # outer wall
        tris.append((ob0, ot0, ot1))
        tris.append((ob0, ot1, ob1))

        # inner wall
        tris.append((ib0, it1, it0))
        tris.append((ib0, ib1, it1))

        # top annulus
        tris.append((it0, it1, ot1))
        tris.append((it0, ot1, ot0))

        # bottom annulus
        tris.append((ib0, ob1, ib1))
        tris.append((ib0, ob0, ob1))

    return tris


def faceted_blob(center: Vec3, r: float, n_lat: int = 10, n_lon: int = 16) -> List[Tri]:
    """Low-poly sphere-ish blob for leaf pads / seed / etc."""
    tris: List[Tri] = []
    cx, cy, cz = center
    for i in range(n_lat):
        t0 = math.pi * i / n_lat
        t1 = math.pi * (i + 1) / n_lat
        for j in range(n_lon):
            p0 = 2 * math.pi * j / n_lon
            p1 = 2 * math.pi * (j + 1) / n_lon

            def sph(t: float, p: float) -> Vec3:
                return (
                    cx + r * math.sin(t) * math.cos(p),
                    cy + r * math.sin(t) * math.sin(p),
                    cz + r * math.cos(t),
                )

            a = sph(t0, p0)
            b = sph(t0, p1)
            c = sph(t1, p1)
            d = sph(t1, p0)

            # two tris per quad (skip degenerate at pole)
            if i != 0:
                tris.append((a, d, c))
                tris.append((a, c, b))
            else:
                tris.append((a, d, c))

    return tris


def tapered_trunk(
    base: Vec3,
    h: float,
    r0: float,
    r1: float,
    bend: float,
    n: int = 14,
    sides: int = 14,
) -> List[Tri]:
    """A bent, tapering trunk as a connected tube (solid)."""
    tris: List[Tri] = []
    rings: List[List[Vec3]] = []
    bx, by, bz = base
    for i in range(n + 1):
        t = i / n
        z = bz + h * t
        # simple S-ish bend
        x_off = bend * math.sin(t * math.pi * 0.9)
        y_off = bend * 0.35 * math.sin(t * math.pi * 0.5)
        r = r0 * (1 - t) + r1 * t

        ring: List[Vec3] = []
        for j in range(sides):
            ang = 2 * math.pi * j / sides
            # bark-ish ridges via radius modulation
            ridge = 1.0 + 0.10 * math.sin(ang * 5 + t * 7)
            rr = r * ridge
            ring.append((bx + x_off + rr * math.cos(ang), by + y_off + rr * math.sin(ang), z))
        rings.append(ring)

    for i in range(n):
        r0_pts = rings[i]
        r1_pts = rings[i + 1]
        for j in range(sides):
            a = r0_pts[j]
            b = r0_pts[(j + 1) % sides]
            c = r1_pts[(j + 1) % sides]
            d = r1_pts[j]
            tris.append((a, d, c))
            tris.append((a, c, b))

    # cap bottom
    center_b = base
    for j in range(sides):
        a = rings[0][j]
        b = rings[0][(j + 1) % sides]
        tris.append((center_b, b, a))

    # cap top
    top_center = (
        sum(p[0] for p in rings[-1]) / sides,
        sum(p[1] for p in rings[-1]) / sides,
        sum(p[2] for p in rings[-1]) / sides,
    )
    for j in range(sides):
        a = rings[-1][j]
        b = rings[-1][(j + 1) % sides]
        tris.append((top_center, a, b))

    return tris


@dataclass
class Params:
    frames: int = 12
    base_outer_d: float = 160.0
    base_h: float = 8.0
    center_hole_d: float = 30.0
    frame_radius: float = 62.0


def make_frame(stage: int, p: Params) -> List[Tri]:
    """One growth-stage sculpture, centered near origin."""
    t = stage / max(1, (p.frames - 1))

    tris: List[Tri] = []

    # soil mound
    mound_r = 6.5 + 2.0 * t
    tris.extend(faceted_blob((0.0, 0.0, mound_r * 0.55), mound_r, n_lat=8, n_lon=14))

    if stage <= 1:
        # seed / cracked seed
        seed_r = 3.2
        seed_z = mound_r * 1.05
        tris.extend(faceted_blob((0.0, 0.0, seed_z), seed_r, n_lat=8, n_lon=14))
        if stage == 1:
            tris.extend(tapered_trunk((0.0, 0.0, seed_z - 1.0), h=6.0, r0=1.2, r1=0.6, bend=1.0))
        return tris

    trunk_h = 6.0 + 26.0 * t
    trunk_r0 = 1.4 + 3.0 * t
    trunk_r1 = 0.7 + 1.5 * t
    bend = 0.5 + 6.0 * t
    tris.extend(tapered_trunk((0.0, 0.0, mound_r * 0.9), h=trunk_h, r0=trunk_r0, r1=trunk_r1, bend=bend))

    # canopy pads
    if stage == 2:
        pads = 1
    elif stage in (3, 4):
        pads = 2
    elif stage in (5, 6):
        pads = 3
    elif stage in (7, 8):
        pads = 4
    elif stage == 9:
        pads = 5
    else:
        pads = 6

    top_z = mound_r * 0.9 + trunk_h
    canopy_r = 3.0 + 6.0 * t

    for i in range(pads):
        ang = 2 * math.pi * i / max(1, pads)
        rad = 2.0 + 7.0 * t
        cx = bend * 0.65 + rad * math.cos(ang)
        cy = rad * math.sin(ang)
        cz = top_z - 4.0 + 1.0 * math.sin(ang * 2)
        r = canopy_r * (0.75 + 0.25 * math.sin(ang * 3 + 0.5))
        tris.extend(faceted_blob((cx, cy, cz), r, n_lat=9, n_lon=14))

    return tris


def write_ascii_stl(path: str, name: str, tris: Sequence[Tri]) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"solid {name}\n")
        for (a, b, c) in tris:
            n = v_norm(v_cross(v_sub(b, a), v_sub(c, a)))
            f.write(f"  facet normal {n[0]:.6e} {n[1]:.6e} {n[2]:.6e}\n")
            f.write("    outer loop\n")
            f.write(f"      vertex {a[0]:.6e} {a[1]:.6e} {a[2]:.6e}\n")
            f.write(f"      vertex {b[0]:.6e} {b[1]:.6e} {b[2]:.6e}\n")
            f.write(f"      vertex {c[0]:.6e} {c[1]:.6e} {c[2]:.6e}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {name}\n")


def build_model(p: Params) -> List[Tri]:
    tris: List[Tri] = []

    r_outer = p.base_outer_d / 2.0
    r_inner = p.center_hole_d / 2.0

    # Base ring
    tris.extend(cylinder_shell(r_outer=r_outer, r_inner=r_inner, h=p.base_h, n=220))

    # Light mosaic bumps on the top surface (subtle)
    mosaic_r = r_outer - 8.0
    bumps = 140
    for i in range(bumps):
        ang = 2 * math.pi * i / bumps
        rr = mosaic_r + 1.2 * math.sin(i * 0.9)
        x = rr * math.cos(ang)
        y = rr * math.sin(ang)
        z = p.base_h + 0.35
        tris.extend(faceted_blob((x, y, z), r=0.9, n_lat=6, n_lon=10))

    # Frames
    for s in range(p.frames):
        frame_tris = make_frame(s, p)
        ang = 2 * math.pi * s / p.frames
        placed = translate(frame_tris, (p.frame_radius, 0.0, p.base_h))
        placed = rotate_tris_z(placed, ang)
        tris.extend(placed)

    return tris


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", type=int, default=12)
    ap.add_argument("--base_outer_d", type=float, default=160.0)
    ap.add_argument("--base_h", type=float, default=8.0)
    ap.add_argument("--center_hole_d", type=float, default=30.0)
    ap.add_argument("--frame_radius", type=float, default=62.0)
    args = ap.parse_args()

    p = Params(
        frames=args.frames,
        base_outer_d=args.base_outer_d,
        base_h=args.base_h,
        center_hole_d=args.center_hole_d,
        frame_radius=args.frame_radius,
    )

    tris = build_model(p)
    write_ascii_stl(args.out, "bonsai_zoetrope", tris)


if __name__ == "__main__":
    main()
