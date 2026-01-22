# PRINT_NOTES (cycle-01) — Bonsai STL

Target: FDM-friendly defaults (also prints well on resin).

## Scale / units
- The generator outputs coordinates in **millimeters**.
- Default total height is ~90 mm.

## Recommended orientation
- Print upright as generated (base flat on the build plate).

## Supports
- Likely required under some canopy lobes/branches depending on your slicer’s overhang threshold.
- Start with **supports from build plate only**; if canopy sags, switch to **everywhere** with a low density.

## Suggested FDM settings (0.4mm nozzle)
- Layer height: 0.16–0.20 mm
- Walls/perimeters: 3–4
- Infill: 10–15% (gyroid)
- Top/bottom: 4–6 layers
- Brim: 4–8 mm (optional, for extra stability)

## Material suggestions
- PLA is fine.
- For a “toy prop” look: sand/prime + paint.

## Known mesh caveat
This STL is built from overlapping solids without boolean union; if your slicer reports non-manifold regions:
- Try your slicer’s “repair” option, or
- Run the STL through a mesh repair tool (Meshmixer / Blender 3D Print Toolbox).
