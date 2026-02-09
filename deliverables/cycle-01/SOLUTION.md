# SOLUTION (cycle-01)

## Summary
Generated a printable STL based on the sketched horn-grill outline. The shape is approximated as a superellipse that matches the specified 112 mm x 45 mm footprint and is extruded to 30 mm height.

## Primary artifact
- `deliverables/cycle-01/assets/horngrill-cycle.stl`

## Generator script
- `deliverables/cycle-01/src/generate_stl-cycle.py`

## Dimensions
- Width: 112.0 mm
- Height: 45.0 mm
- Depth: 30.0 mm

## Assumptions
- The outline is approximated as a smooth superellipse to match the hand-drawn curvature.
- The extrusion is straight with no draft angle.

## How to regenerate
```bash
python3 deliverables/cycle-01/src/generate_stl-cycle.py
```
