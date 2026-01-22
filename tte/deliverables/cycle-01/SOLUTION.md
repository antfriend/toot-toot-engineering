# SOLUTION (cycle-01) — Procedural bonsai STL

## What this delivers
- `deliverables/cycle-01/output/bonsai_marioland_smooth.stl`
- Generator source: `deliverables/cycle-01/source/generate_bonsai.py`

This is a cartoony, platformer-world-inspired bonsai (chunky pot + S-curve trunk + a few thick branches + puffy canopy lobes).

## How to regenerate
From repo root:

```bash
python deliverables/cycle-01/source/generate_bonsai.py \
  --out deliverables/cycle-01/output/bonsai_marioland_smooth.stl \
  --seed 1
```

### Parameters
The script currently exposes only `--seed` (for reproducibility). If we need variant sizes/shapes, the next iteration should add CLI params mirroring `STORYTELLER.md` defaults (height, pot diameter, branch count, canopy lobes, texture strength).

## Notes on mesh construction
This generator intentionally uses **no external mesh libraries** (e.g., `trimesh`) so it can run in a minimal environment. As a result:
- The final STL is an **assembly of overlapping closed solids** (pot + rim + trunk tube + branch tubes + sphere canopy lobes).
- There is **no boolean union**, so internal faces exist where shapes intersect.

Many slicers will still slice/print this successfully because the shell surfaces are closed; however, strict manifold tests may flag issues.

If you have tooling available later (Blender, Meshmixer, or Python + trimesh), a recommended post-process is to union/repair into a single watertight manifold.
