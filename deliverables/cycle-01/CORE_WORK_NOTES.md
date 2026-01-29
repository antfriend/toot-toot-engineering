# CORE_WORK_NOTES (cycle-01)

## Goal
Produce an STL which preserves the scanned HORN_GRILL_HOLDSTER geometry overall, while making the **top rim** read as a smoother, more intentional curve (reduced faceting/chatter), per `TTE_PROMPT.md` + Storyteller acceptance criteria.

## Tooling
- Python 3.13
- `trimesh==4.11.1`
- `numpy==2.3.3`
- `matplotlib==3.10.7` (optional, for before/after rim visualization)

## Input / output files
- Input (reference): `HORN_GRILL_HOLDSTER_SCAN.stl`
- Output (new STL): `deliverables/cycle-01/HORN_GRILL_HOLDSTER_SMOOTH_RIM.stl`
- Optional visual: `deliverables/cycle-01/assets/before_after_rim.png`

## Rim band definition (operational)
Because we only have a scan STL and a single photo, the rim was defined by a Z-height band at the very top of the mesh:
- Let `Zmax = max(vertex.z)`
- Rim band = all vertices with `z >= Zmax - band_height`
- Chosen `band_height = 0.05` (in the STL coordinate units)

Measured from the scan:
- `Zmin = -0.5959159732`
- `Zmax =  0.5959159732`
- Rim band Z-range: `[0.5459159732, 0.5959159732]`
- Rim band vertex count: `818 / 9266`

## Smoothing method
We used Taubin smoothing (volume-preserving-ish smoothing) via `trimesh.smoothing.filter_taubin`.

Key approach to keep the rest of the part unchanged:
1. Copy the original mesh.
2. Apply Taubin smoothing to the copy (entire mesh).
3. Replace **only** rim-band vertices in the original mesh with the smoothed positions.
4. Compensate for rim shrinkage in Z by shifting the rim-band vertices so that the **topmost Z** equals the original `Zmax`.

### Parameters
- `iterations = 50`
- `lamb = 0.5`
- `nu = -0.53`

### Reproducible command
```bat
python -c "import trimesh, numpy as np; from trimesh.smoothing import filter_taubin; orig=trimesh.load('HORN_GRILL_HOLDSTER_SCAN.stl', force='mesh'); z=orig.vertices[:,2]; zmax=z.max(); band=0.05; rim=z>=zmax-band; m2=orig.copy(); filter_taubin(m2, lamb=0.5, nu=-0.53, iterations=50); shift=float(zmax - m2.vertices[rim,2].max()); m2.vertices[rim,2]+=shift; v=orig.vertices.copy(); v[rim]=m2.vertices[rim]; out=trimesh.Trimesh(vertices=v, faces=orig.faces, process=False); out.export('deliverables/cycle-01/HORN_GRILL_HOLDSTER_SMOOTH_RIM.stl'); print('exported')"
```

## Validation metrics (before/after)
### Topology / integrity
- Before (scan STL):
  - Vertices: 9266
  - Faces: 18552
  - Watertight: `True`
  - Winding consistent: `True`
- After (smoothed rim STL):
  - Vertices: 9266
  - Faces: 18552
  - Watertight: `True`
  - Winding consistent: `True`

### Bounding box
- Before bounds:
  - min `[-0.497998, 0.0, -0.59591597]`
  - max `[ 0.497998, 0.42203698, 0.59591597]`
- After bounds:
  - min `[-0.497998, 0.0, -0.59591597]`
  - max `[ 0.497998, 0.42203698, 0.59591597]`

### Deviation (vertex displacement)
Computed as per-vertex Euclidean delta between before/after.
- Non-rim vertices: max delta `0.0` (unchanged)
- Rim-band vertices (band_height=0.05):
  - mean delta `~0.01707`
  - max delta `~0.04035`

## Notes / future improvements
- This pass deliberately kept the edit localized to the top Z-band. If the true rim feature extends deeper than `0.05` units, increase `band_height` and re-run.
- A more CAD-like rim (true arc/fillet) would require feature detection + surface fitting or a partial remesh workflow.
