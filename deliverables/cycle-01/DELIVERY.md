# DELIVERY (cycle-01)

Workflow version: 3.8

## What is being delivered
Primary deliverable (as generated):
- `deliverables/cycle-01/output/bonsai-zoetrope.stl`

Supporting deliverables:
- `deliverables/cycle-01/output/frame-01.stl` … `frame-12.stl`
- Source generator: `deliverables/cycle-01/bonsai_zoetrope.py`
- Spec + notes: `deliverables/cycle-01/GEOMETRY_SPEC.md`, `deliverables/cycle-01/SOLUTION.md`, `deliverables/cycle-01/REVIEW.md`

## Validation status
- **Per-frame STLs**: at least one spot-check (`frame-12.stl`) is **watertight**.
- **Combined STL (`bonsai-zoetrope.stl`)**: **NOT watertight** per Trimesh; this may fail “manifold/solid” requirements in some slicers and does not meet the strict acceptance criteria stated in `GEOMETRY_SPEC.md`.

## Recommended print approach (pragmatic)
Because the combined STL is non-manifold, the safest current print path is:
1. Print **individual frames** (`frame-01.stl` … `frame-12.stl`) for validation of geometry and supports.
2. If a single-piece zoetrope is required, run the combined STL through a mesh repair/union workflow before printing.

## Suggested repair workflows (choose one)
### Option A — Blender (most reliable, manual)
1. Import `bonsai-zoetrope.stl`.
2. Use **Voxel Remesh** (set voxel size appropriate to preserve texture; e.g., 0.3–0.6 mm).
3. Apply remesh and export as `bonsai-zoetrope_watertight.stl`.

### Option B — MeshLab (semi-manual)
1. Filters → Cleaning and Repairing → “Remove T-Vertices by Edge Flip”.
2. Filters → Cleaning and Repairing → “Remove Non Manifold Edges”.
3. Filters → Remeshing/Simplification → (optional) “Uniform Mesh Resampling”.

### Option C — Slicer repair (fastest, least controlled)
Some slicers (e.g., PrusaSlicer/OrcaSlicer) can auto-repair non-manifold STLs on import; verify preview for missing faces.

## Notes on scale
The combined model extents read ~160×160×74.46, which is consistent with a 160 mm platform diameter. Verify units in your slicer (treat as **mm**).

## Logo requirement
A Toot Toot Engineering logo is available in the repo (`toot-toot-logo.png` / `toot-toot-logo.svg`).
For an STL deliverable, the practical approach is to:
- include the logo as a **companion asset** (not embossed into geometry) unless we add a dedicated emboss step in a future cycle.

## Open questions / next actions
- Do we require a *single watertight unioned* `bonsai-zoetrope.stl` (per `GEOMETRY_SPEC.md`), or is “assembly STL + per-frame watertight STLs” acceptable?
- If strict watertightness is required, add a repair/boolean step to the pipeline in the next cycle and regenerate the combined STL.
