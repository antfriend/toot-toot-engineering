import math
from pathlib import Path

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "assets" / "horngrill-cycle.stl"

WIDTH_MM = 112.0
HEIGHT_MM = 45.0
DEPTH_MM = 30.0
SUPERELLIPSE_N = 3.2
SAMPLES = 240


def superellipse_point(theta, a, b, n):
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    x = a * math.copysign(abs(cos_t) ** (2.0 / n), cos_t)
    y = b * math.copysign(abs(sin_t) ** (2.0 / n), sin_t)
    return (x, y)


def polygon_points(a, b, n, samples):
    return [
        superellipse_point(2.0 * math.pi * i / samples, a, b, n)
        for i in range(samples)
    ]


def normal_for_triangle(p1, p2, p3):
    ux, uy, uz = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    vx, vy, vz = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    nx = uy * vz - uz * vy
    ny = uz * vx - ux * vz
    nz = ux * vy - uy * vx
    length = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return (nx / length, ny / length, nz / length)


def write_ascii_stl(path, triangles, name="horngrill_cycle"):
    lines = [f"solid {name}"]
    for p1, p2, p3 in triangles:
        nx, ny, nz = normal_for_triangle(p1, p2, p3)
        lines.append(f"  facet normal {nx:.6f} {ny:.6f} {nz:.6f}")
        lines.append("    outer loop")
        lines.append(f"      vertex {p1[0]:.6f} {p1[1]:.6f} {p1[2]:.6f}")
        lines.append(f"      vertex {p2[0]:.6f} {p2[1]:.6f} {p2[2]:.6f}")
        lines.append(f"      vertex {p3[0]:.6f} {p3[1]:.6f} {p3[2]:.6f}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {name}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    a = WIDTH_MM / 2.0
    b = HEIGHT_MM / 2.0
    points_2d = polygon_points(a, b, SUPERELLIPSE_N, SAMPLES)

    top = [(x, y, DEPTH_MM) for x, y in points_2d]
    bottom = [(x, y, 0.0) for x, y in points_2d]

    triangles = []
    center_top = (0.0, 0.0, DEPTH_MM)
    center_bottom = (0.0, 0.0, 0.0)

    # Top face (counter-clockwise when viewed from above)
    for i in range(len(top)):
        p1 = top[i]
        p2 = top[(i + 1) % len(top)]
        triangles.append((center_top, p1, p2))

    # Bottom face (clockwise when viewed from above)
    for i in range(len(bottom)):
        p1 = bottom[i]
        p2 = bottom[(i + 1) % len(bottom)]
        triangles.append((center_bottom, p2, p1))

    # Side faces
    for i in range(len(top)):
        t1 = top[i]
        t2 = top[(i + 1) % len(top)]
        b1 = bottom[i]
        b2 = bottom[(i + 1) % len(bottom)]
        triangles.append((b1, t1, t2))
        triangles.append((b1, t2, b2))

    write_ascii_stl(OUTPUT_PATH, triangles)


if __name__ == "__main__":
    main()
