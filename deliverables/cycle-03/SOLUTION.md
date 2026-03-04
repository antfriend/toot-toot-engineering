# SOLUTION (cycle-03)

## Primary outputs
- `deliverables/cycle-03/one_drop_portrait.svg`
- `deliverables/cycle-03/raining.svg`

## Implementation summary
- Built a minimalist character portrait with three visible oval primitives (outline, infill, highlight) and motion-driven personality.
- Built a continuous POV rainfall shot with staged environment transitions:
  - fade-in from black to sky
  - approach/entry through cloud volume
  - fog occlusion phase
  - mountain lake reveal and rapid scale-up
  - splash activity and sink-into-blue ending
- Added dozens of surrounding raindrops using a reusable symbol and varied timing/scale for depth.

## Notes for future cycles
- IDs and grouped layers are named to support iterative retiming and palette variants.
- SVG-native animation was chosen for portability and direct source control diffing.
