# DELIVERY (cycle-01)

## What to deliver
Primary deliverable:
- `output/bonsai_marioland.stl` — 3D-printable, single-piece Marioland-inspired bonsai (pot + soil + roots + twist trunk + puffy/dimpled canopy).

Source + reproduction:
- `src/generate_bonsai.py` — deterministic generator (seeded) used to produce the STL
- `src/requirements.txt` — Python dependencies for regeneration

Companion branding asset (per TTE rules):
- `toot-toot-logo.svg`

## Quick start (regenerate STL)
From repo root:
```bash
python -m pip install -r tte/deliverables/cycle-01/src/requirements.txt
python tte/deliverables/cycle-01/src/generate_bonsai.py \
  --out tte/deliverables/cycle-01/output/bonsai_marioland.stl
```

## Print guidance (FDM-friendly defaults)
- Intended size: ~74 mm tall (scale as desired).
- Orientation: pot on the build plate.
- Supports: usually not required for the pot; canopy underside may benefit from organic/tree supports depending on slicer settings.
- Starting settings (0.4 mm nozzle): 0.16–0.24 mm layer height, 3+ perimeters, 10–20% infill.

## Validation notes
- Review confirmed via `trimesh` that the STL reports `is_watertight=True`.
- Recommendation: import into your slicer and check for any stray islands (unlikely, but worth a quick glance).

## Files checklist
- [x] `deliverables/cycle-01/output/bonsai_marioland.stl`
- [x] `deliverables/cycle-01/src/generate_bonsai.py`
- [x] `deliverables/cycle-01/src/requirements.txt`
- [x] `deliverables/cycle-01/SOLUTION.md`
- [x] `deliverables/cycle-01/REVIEW.md`
- [x] `deliverables/cycle-01/toot-toot-logo.svg`
