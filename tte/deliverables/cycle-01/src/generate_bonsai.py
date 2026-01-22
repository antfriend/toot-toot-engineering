"""Procedural Marioland-style bonsai STL generator.

Goal: Create a single-piece, FDM-friendly bonsai (pot + trunk + canopy) with chunky forms
and shallow surface texturing. Uses only the Python standard library.

Mesh strategy:
- Build simple analytic solids (surfaces of revolution + spheres) as triangle meshes.
- Combine by concatenating meshes (they may intersect internally; STL can still be printable).
- Validate basic sanity (triangle count, bbox). True manifold validation is deferred to Reviewer.

Usage:
  python generate_bonsai.py --params ../PARAMS.json --out ../output/bonsai_marioland.stl

All units are millimeters.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

Vec3 = Tuple[float, float, float]
Tri = Tuple[Vec3, Vec3, Vec3]


def v_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_scale(a: Vec3, s: float) -> Vec3:
    return (a[0] * s, a[1] * s, a[2] * s)


def v_cross(a: Vec3, b: Vec3) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def v_len(a: Vec3) -> float:
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def v_norm(a: Vec3) -> Vec3:
    l = v_len(a)
    if l == 0:
        return (0.0, 0.0, 0.0)
    return (a[0] / l, a[1] / l, a[2] / l)


def tri_normal(t: Tri) -> Vec3:
    a, b, c = t
    return v_norm(v_cross(v_sub(b, a), v_sub(c, a)))


def write_ascii_stl(path: str, tris: Sequence[Tri], solid_name: str = "bonsai") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"solid {solid_name}\n")
        for t in tris:
            n = tri_normal(t)
            f.write(f"  facet normal {n[0]:.7e} {n[1]:.7e} {n[2]:.7e}\n")
            f.write("    outer loop\n")
            for v in t:
                f.write(f"      vertex {v[0]:.7e} {v[1]:.7e} {v[2]:.7e}\n")
            f.write("    endloop\n")
            f.write("  endfacet\n")
        f.write(f"endsolid {solid_name}\n")


def revolve_profile(
    z_samples: Sequence[float],
    r_samples: Sequence[float],
    segments: int,
    center: Vec3 = (0.0, 0.0, 0.0),
) -> List[Tri]:
    """Surface of revolution around Z axis.

    Produces only the lateral surface; caps should be added separately.
    """
    assert len(z_samples) == len(r_samples)
    cx, cy, cz = center
    tris: List[Tri] = []
    for i in range(len(z_samples) - 1):
        z0 = cz + z_samples[i]
        z1 = cz + z_samples[i + 1]
        r0 = r_samples[i]
        r1 = r_samples[i + 1]
        for s in range(segments):
            a0 = 2 * math.pi * (s / segments)
            a1 = 2 * math.pi * ((s + 1) / segments)
            p00 = (cx + r0 * math.cos(a0), cy + r0 * math.sin(a0), z0)
            p01 = (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1), z0)
            p10 = (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0), z1)
            p11 = (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1), z1)
            # two triangles per quad
            tris.append((p00, p10, p11))
            tris.append((p00, p11, p01))
    return tris


def disk_cap(z: float, radius: float, segments: int, up: bool, center: Vec3 = (0.0, 0.0, 0.0)) -> List[Tri]:
    cx, cy, cz = center
    zc = cz + z
    c = (cx, cy, zc)
    tris: List[Tri] = []
    for s in range(segments):
        a0 = 2 * math.pi * (s / segments)
        a1 = 2 * math.pi * ((s + 1) / segments)
        p0 = (cx + radius * math.cos(a0), cy + radius * math.sin(a0), zc)
        p1 = (cx + radius * math.cos(a1), cy + radius * math.sin(a1), zc)
        tris.append((c, p0, p1) if up else (c, p1, p0))
    return tris


def sphere(center: Vec3, radius: float, rings: int, segments: int) -> List[Tri]:
    cx, cy, cz = center
    tris: List[Tri] = []
    for i in range(rings):
        t0 = math.pi * (i / rings)
        t1 = math.pi * ((i + 1) / rings)
        z0 = math.cos(t0)
        z1 = math.cos(t1)
        r0 = math.sin(t0)
        r1 = math.sin(t1)
        for s in range(segments):
            a0 = 2 * math.pi * (s / segments)
            a1 = 2 * math.pi * ((s + 1) / segments)
            p00 = (cx + radius * r0 * math.cos(a0), cy + radius * r0 * math.sin(a0), cz + radius * z0)
            p01 = (cx + radius * r0 * math.cos(a1), cy + radius * r0 * math.sin(a1), cz + radius * z0)
            p10 = (cx + radius * r1 * math.cos(a0), cy + radius * r1 * math.sin(a0), cz + radius * z1)
            p11 = (cx + radius * r1 * math.cos(a1), cy + radius * r1 * math.sin(a1), cz + radius * z1)
            tris.append((p00, p10, p11))
            tris.append((p00, p11, p01))
    return tris


def bbox(tris: Sequence[Tri]) -> Tuple[Vec3, Vec3]:
    xs, ys, zs = [], [], []
    for t in tris:
        for v in t:
            xs.append(v[0])
            ys.append(v[1])
            zs.append(v[2])
    return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def trunk_centerline(t: float, height: float, curve_amount: float) -> Vec3:
    # gentle S-curve in XZ plane
    x = curve_amount * 10.0 * math.sin(math.pi * (t - 0.15))
    y = curve_amount * 4.0 * math.sin(2 * math.pi * t)
    z = t * height
    return (x, y, z)


def make_pot(params: dict) -> List[Tri]:
    pot = params["pot"]
    seg = int(params["mesh"]["segments"])

    R = float(pot["outer_radius_mm"])
    H = float(pot["height_mm"])
    base_t = float(pot["base_thickness_mm"])
    lip_h = float(pot["lip_height_mm"])
    wall = float(pot["wall_thickness_mm"])

    r_inner = max(1.0, R - wall)

    # Outer wall profile: slight belly and lip
    z = [0.0, H - lip_h, H]
    r = [R * 0.98, R * 1.02, R * 1.00]
    tris = revolve_profile(z, r, seg)
    tris += disk_cap(0.0, R * 0.98, seg, up=False)  # bottom

    # Inner cavity wall (open at top): build lateral surface only
    z_in = [base_t, H - lip_h * 0.6, H]
    r_in = [r_inner * 0.85, r_inner * 1.00, r_inner * 1.00]
    inner = revolve_profile(z_in, r_in, seg)
    # flip inner wall winding so normals point inward; STL doesn't care much but helps
    tris += [(a, c, b) for (a, b, c) in inner]

    return tris


def make_trunk_and_roots(params: dict) -> List[Tri]:
    trunk = params["trunk"]
    style = params["style"]
    seg = int(params["mesh"]["segments"])
    seed = int(params["mesh"]["seed"])
    rnd = random.Random(seed)

    base_r = float(trunk["base_radius_mm"])
    top_r = float(trunk["top_radius_mm"])
    H = float(trunk["height_mm"])
    curve = float(trunk["curve_amount"])
    root_flare = float(trunk["root_flare"])
    tex = float(style["texture_depth_mm"])

    # sample along height
    steps = 18
    z_samples: List[float] = []
    r_samples: List[float] = []
    centers: List[Vec3] = []
    for i in range(steps + 1):
        t = i / steps
        c = trunk_centerline(t, H, curve)
        centers.append(c)
        z_samples.append(c[2])
        # taper + subtle bulges
        rr = (1 - t) * base_r + t * top_r
        rr *= 1.0 + 0.06 * math.sin(2 * math.pi * t) + 0.04 * math.sin(6 * math.pi * t)
        # root flare near base
        rr *= 1.0 + root_flare * max(0.0, (0.22 - t) / 0.22)
        r_samples.append(rr)

    # Build trunk as stacked rings with per-ring center offsets
    tris: List[Tri] = []
    for i in range(len(z_samples) - 1):
        c0 = centers[i]
        c1 = centers[i + 1]
        r0 = r_samples[i]
        r1 = r_samples[i + 1]
        for s in range(seg):
            a0 = 2 * math.pi * (s / seg)
            a1 = 2 * math.pi * ((s + 1) / seg)

            def bark_jitter(t01: float) -> float:
                # shallow printable bark: deterministic pseudo-noise via sin + small random
                return tex * (0.35 * math.sin(8 * a0 + 6 * t01) + 0.20 * math.sin(17 * a0 + 2 * t01) + 0.25 * (rnd.random() - 0.5))

            j0 = bark_jitter(i / steps)
            j1 = bark_jitter((i + 1) / steps)
            rr0 = max(0.8, r0 + j0)
            rr1 = max(0.6, r1 + j1)

            p00 = (c0[0] + rr0 * math.cos(a0), c0[1] + rr0 * math.sin(a0), c0[2])
            p01 = (c0[0] + rr0 * math.cos(a1), c0[1] + rr0 * math.sin(a1), c0[2])
            p10 = (c1[0] + rr1 * math.cos(a0), c1[1] + rr1 * math.sin(a0), c1[2])
            p11 = (c1[0] + rr1 * math.cos(a1), c1[1] + rr1 * math.sin(a1), c1[2])
            tris.append((p00, p10, p11))
            tris.append((p00, p11, p01))

    # Cap trunk top with a disk
    top_c = centers[-1]
    tris += disk_cap(top_c[2], r_samples[-1], seg, up=True, center=(top_c[0], top_c[1], 0.0))

    return tris


def make_canopy(params: dict, trunk_top: Vec3) -> List[Tri]:
    canopy = params["canopy"]
    style = params["style"]
    seg = int(params["mesh"]["segments"])
    tex = float(style["texture_depth_mm"])

    R = float(canopy["radius_mm"])
    lobes = int(canopy["lobes"])
    lobe_offset = float(canopy["lobe_offset_mm"])
    v_off = float(canopy["vertical_offset_mm"])

    # Main puff
    center = v_add(trunk_top, (0.0, 0.0, v_off))
    tris: List[Tri] = []
    tris += sphere(center, R, rings=max(10, seg // 6), segments=seg)

    # Lobe puffs around
    for i in range(lobes):
        ang = 2 * math.pi * (i / lobes)
        c = v_add(center, (lobe_offset * math.cos(ang), lobe_offset * math.sin(ang), -R * 0.15))
        tris += sphere(c, R * 0.68, rings=max(9, seg // 7), segments=seg)

    # Micro-bump texture: add a few small spheres (very shallow)
    bumps = 14
    for i in range(bumps):
        ang = 2 * math.pi * (i / bumps)
        c = v_add(center, (R * 0.55 * math.cos(ang), R * 0.55 * math.sin(ang), R * 0.15 * math.sin(2 * ang)))
        tris += sphere(c, tex * 1.6, rings=6, segments=max(12, seg // 3))

    return tris


def load_params(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    params = load_params(args.params)

    pot_tris = make_pot(params)
    trunk_tris = make_trunk_and_roots(params)

    # Find trunk top approx from bbox
    b0, b1 = bbox(trunk_tris)
    trunk_top = (0.0, 0.0, b1[2])
    canopy_tris = make_canopy(params, trunk_top)

    tris = pot_tris + trunk_tris + canopy_tris

    bb0, bb1 = bbox(tris)
    print(f"triangles: {len(tris)}")
    print(f"bbox min: {bb0}")
    print(f"bbox max: {bb1}")

    write_ascii_stl(args.out, tris, solid_name="bonsai_marioland")
    print(f"wrote: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
