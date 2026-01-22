# BOOTSTRAP (cycle-01)

## Prompt (from `tte/README.md`)
Create an STL file suitable for 3D printing which depicts a lovely bonsai tree, grown in 3 dimensions, in the style of Marioland with surface texturing.

## Interpretation
We need a *printable* 3D model (STL) of a “lovely bonsai tree” with a playful, chunky, game-like aesthetic (“Marioland”) and some surface texturing.

Because this repo is plain-text-first and we can generate assets programmatically, the most reliable path is:
- author a parametric mesh generator (Python) that creates a stylized trunk + canopy + pot,
- export to STL,
- validate basic manifoldness/printability,
- package with notes.

## Definition of done (cycle-01)
- `deliverables/cycle-01/output/bonsai_marioland.stl` exists.
- The STL is watertight/manifold (or best-effort with validation notes).
- Model is oriented for printing (flat base), with sane scale (e.g., 80–120 mm tall), and no razor-thin parts.
- Delivery notes explain how it was generated and how to tweak parameters.
- Includes a small Toot-Toot Engineering logo as a companion asset in the cycle folder.

## Proposed team (roles)
Required:
- **Orchestrator**: adjust plan to include a mesh-generation+STL export pipeline and validation.
- **Core worker** (with “procedural 3D modeling” focus): implement generator + produce STL.
- **Reviewer**: validate STL, check printability and prompt alignment.
- **Delivery packager**: assemble outputs + notes.

Optional / add if needed:
- **Image producer**: render preview images (PNG) from STL for quick review.

## Recommended plan adjustments
1. Add an explicit “Validation + preview render” sub-step before review (or as part of review) using `trimesh` if available; otherwise implement a simple sanity report.
2. Ensure we produce not only an STL but also:
   - a parameter file (`PARAMS.json`) and
   - a short build script (`generate_bonsai.py`) in the cycle folder for reproducibility.
3. Constrain style translation (“Marioland”) into concrete geometry choices:
   - chunky silhouette, exaggerated roots, rounded blobs for foliage,
   - shallow texture on trunk and canopy,
   - avoid micro-detail that won’t print.

## Open questions / assumptions
- “Marioland” is interpreted as *playful, rounded, high-contrast forms*; we avoid copying any trademarked characters/logos.
- Printing assumptions: FDM-friendly (supports minimized); we design a single-piece tree + pot with gentle overhangs.

---

## Retrospective (end of cycle-01)

### What went well
- Delivered a reproducible pipeline: `PARAMS.json` + generator script + generated STL.
- The model meets the prompt at a “toy-like game prop” level and includes shallow texture.
- Orientation/scale are sane for a small desk print (~99 mm tall).

### What didn’t / risks
- Geometry is assembled via intersecting primitives (concatenated triangle soups). This can introduce internal faces and non-manifold intersections. Many slicers repair this, but it’s not guaranteed.
- No preview renders were produced in-repo, so reviewers must load the STL in a slicer/mesh viewer.

### Recommended plan/role improvements for next cycle
1. Add a dedicated **Mesh validation & repair** step using `trimesh` (if available) and/or a Blender/MeshLab export pass to perform boolean union and ensure manifoldness.
2. Add an **Image producer** step to render 2–3 orthographic PNG previews for quick review.
3. Consider binary STL export (smaller and more conventional) once validation is in place.

## Next-cycle prompt suggestions (choose 1)
1. “Repair/boolean-union the generated bonsai into a strictly manifold mesh, export as binary STL, and add 3 preview renders.”
2. “Generate three variant bonsai STLs (small/medium/large canopy) and arrange them on a single printable build plate STL.”
3. “Create a ‘season set’ of four swappable canopies (spring/summer/fall/winter) with a simple twist-lock joint, plus a storage base.”
