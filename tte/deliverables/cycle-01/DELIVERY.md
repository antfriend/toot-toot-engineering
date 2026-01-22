# DELIVERY (cycle-01) — Bonsai STL package

## Package contents
Deliverables root: `deliverables/cycle-01/`

### Primary deliverable
- `output/bonsai_marioland_smooth.stl`
  - Procedurally generated “platformer-world / Marioland-inspired” bonsai (pot + S-curve trunk + thick branches + canopy lobes)
  - Units: mm (see `PRINT_NOTES.md`)

### Regeneration / source
- `source/generate_bonsai.py`
- `SOLUTION.md` (how to run/regenerate; current parameters)

### Validation / review
- `REVIEW.md`
- `output/validation/` (notes/artifacts folder; currently minimal)

### Print guidance
- `PRINT_NOTES.md`

### Companion branding
- Repo logo assets (companion): `toot-toot-logo.png`, `toot-toot-logo.svg`
  - Note: STL itself does not embed a logo. For physical inclusion, add an embossed/engraved mark in a future revision.

## How to run
From repo root:

```bash
python deliverables/cycle-01/source/generate_bonsai.py \
  --out deliverables/cycle-01/output/bonsai_marioland_smooth.stl \
  --seed 1
```

## Known caveats (important)
1. **Overlapping solids / no boolean union**
   - The STL is an assembly of closed solids that intersect (pot, trunk, branches, canopy lobes).
   - Some slicers handle this fine; strict manifold tools may warn.
   - If you see issues, run a repair pass (e.g., Microsoft 3D Builder “Repair”, Blender 3D Print Toolbox).

2. **Surface texturing**
   - The prompt requested “surface texturing”; current deliverable is primarily smooth geometry.
   - Recommended follow-up: add subtle bark ridges on trunk and/or dimpled canopy noise (must keep minimum thickness safe).

## Suggested “repair to watertight” workflow (optional)
- Windows (GUI): **Microsoft 3D Builder**
  1) Open STL → accept “Repair?” → Save as a new STL
- Blender:
  - Import STL → run 3D Print Toolbox checks → attempt “Make Manifold” / Cleanup as needed → export STL

## What would make this package “stronger” in a follow-up cycle
- Provide a second STL that is explicitly repaired/unioned (watertight), if tooling is available.
- Add CLI parameters for height/pot size/branch count/canopy density.
- Implement low-amplitude texturing while preserving printability.
