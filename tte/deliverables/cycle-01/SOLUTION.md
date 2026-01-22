# SOLUTION (cycle-01)

## Deliverable
- `output/bonsai_marioland.stl`

This STL is a **single-piece**, Marioland-inspired bonsai: chunky pot + soil mound + root flare + twisting trunk + puffy/dimpled canopy.

## How it was generated (deterministic)
Source generator:
- `src/generate_bonsai.py`

Pipeline:
1. Construct a boolean **voxel occupancy** volume for the full model (pot + tree fused together).
2. Apply a few stylized texture motifs directly in the volume:
   - trunk bark grooves via radial sinus modulation
   - canopy “puff” blobs plus subtractive “dimple” cavities
3. Pad the volume and extract an isosurface via **marching cubes**.
4. Keep only the **largest connected component** (removes stray islands).
5. Export as **binary STL**.

All randomness is seeded (`--seed`, default `1337`) so the output is reproducible.

## Regeneration
From repo root:
```bash
python -m pip install -r tte/deliverables/cycle-01/src/requirements.txt
python tte/deliverables/cycle-01/src/generate_bonsai.py \
  --out tte/deliverables/cycle-01/output/bonsai_marioland.stl
```

Useful knobs:
- `--voxel 0.5` for slightly more detail (slower, bigger STL)
- `--voxel 0.7` for faster generation / chunkier look
- `--height 80` changes overall Z extent target
- `--seed <int>` changes the canopy blob layout while keeping style consistent

## Print notes (default FDM-friendly)
- Intended scale: ~74 mm tall by ~41 mm wide/deep (can be scaled).
- Orientation: print upright, pot on bed.
- The model is designed with **chunky features** so bark grooves and canopy dimples survive typical 0.4 mm nozzle printing.
- Suggested starting settings:
  - Layer height: 0.16–0.24 mm
  - Perimeters: 3+
  - Infill: 10–20% (gyroid/grid)
  - Supports: likely not required for the pot; canopy may benefit from organic supports depending on slicer/overhang tolerance.

## Validation
If `trimesh` is installed, the generator prints a quick manifoldness check after writing the STL.

Example output fields:
- bounds/size (mm)
- `trimesh: watertight=True` (goal)

