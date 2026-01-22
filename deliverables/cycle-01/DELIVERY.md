# DELIVERY (cycle-01)

## Primary deliverable
- `deliverables/cycle-01/output/bonsai_zoetrope.stl`
  - 12-frame bonsai growth zoetrope (seed → mature bonsai)
  - Base outer diameter: 160 mm (default)
  - Base height: 8 mm (default)
  - Center hole: **30 mm diameter** (by construction)

## Source / reproducibility
- Generator script (no external dependencies):
  - `deliverables/cycle-01/src/generate_zoetrope.py`

Re-generate STL:
```sh
python deliverables/cycle-01/src/generate_zoetrope.py \
  --out deliverables/cycle-01/output/bonsai_zoetrope.stl
```

Useful knobs:
- `--frames` (default 12)
- `--base_outer_d` (default 160)
- `--base_h` (default 8)
- `--center_hole_d` (default 30)
- `--frame_radius` (default 62)

## Print notes
- Recommended orientation: **as generated** (flat base on build plate).
- Supports: try **no supports** first. If your slicer reports canopy islands, enable minimal supports (tree/organic supports) and/or reduce canopy size by scaling Z slightly.
- Layer height: 0.20 mm typical; 0.16 mm if you want nicer bark texture.

## Zoetrope usage note
For visible animation:
- Spin the zoetrope and film with a phone camera at 30/60 fps under stable lighting.
- If motion looks jumpy, try a higher frame count (`--frames 16`) and slightly increase `--frame_radius` to preserve spacing.

## TTE logo inclusion
Including a logo embedded into the STL is possible but would require additional modeling/boolean work. For cycle-01 we include the logo as a **companion asset** already present at repo root:
- `toot-toot-logo.png`

(If needed next cycle: add a small raised/engraved logo plaque on the base rim.)
