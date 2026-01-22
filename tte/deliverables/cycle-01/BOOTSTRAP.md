# BOOTSTRAP (cycle-01)

## Prompt (from `tte/README.md`)
Create an STL file suitable for 3D printing which depicts a lovely bonsai tree, grown in 3 dimensions, in the style of Marioland with surface texturing.

## Interpretation
We need a *printable* 3D model (STL) of a “lovely bonsai tree” with a playful, chunky, game-like aesthetic (“Marioland”) and some surface texturing.

Because this repo is plain-text-first and we can generate assets programmatically, the most reliable path is:
- author a parametric mesh generator (Python) that creates a stylized trunk + canopy + pot,
- export to STL,
- validate manifoldness and printability basics (watertight, normals, scale, minimum thickness),
- package with notes.

## Definition of done (cycle-01)
- `deliverables/cycle-01/output/bonsai_marioland.stl` exists.
- The STL is watertight/manifold (or best-effort with validation notes).
- Model is oriented for printing (flat base), with sane scale (e.g., 80–120 mm tall), and no razor-thin parts.
- Delivery notes explain how it was generated and how to tweak parameters.
- Includes a small Toot-Toot Engineering logo as a companion asset in the cycle folder (already available in `tte/toot-toot-logo.*`; delivery step will copy into cycle output).

## Proposed team (roles)
Required:
- **Orchestrator**: adjust plan to include a mesh-generation+STL export pipeline and validation.
- **Core worker** (with “procedural 3D modeling” focus): implement generator + produce STL.
- **Reviewer**: validate STL, check printability and prompt alignment.
- **Delivery packager**: assemble outputs + notes.

Optional / add if needed:
- **Image producer**: render preview images (PNG) from STL for quick review.

## Recommended plan adjustments
1. Add an explicit **“Validation + preview render”** sub-step before review (or as part of review) using `trimesh` (already typical in Python ecosystems) if available; otherwise implement a simple sanity report.
2. Ensure we produce not only an STL but also:
   - a parameter file (`PARAMS.json`) and
   - a short build script (`generate_bonsai.py`) in the cycle folder for reproducibility.
3. Constrain style translation (“Marioland”) into concrete geometry choices:
   - chunky silhouette, exaggerated roots, rounded blobs for foliage,
   - shallow noise/scale texture on trunk and canopy,
   - avoid micro-detail that won’t print.

## Open questions / assumptions
- “Marioland” is interpreted as *playful, rounded, high-contrast forms*; we will avoid copying any trademarked characters/logos.
- Printing assumptions: FDM-friendly (supports minimized); we will design a single-piece tree + pot with gentle overhangs.

## Next-cycle prompt suggestions (choose 1 after cycle-01 completes)
1. “Make three variant bonsai STLs (small/medium/large canopy) and arrange them on a single printable build plate STL.”
2. “Create a matching Marioland-style garden base (rocks + path) that the bonsai pot slots into, with keyed connectors.”
3. “Generate a ‘season set’ of four bonsai canopies (spring/summer/fall/winter) as swappable parts with a twist-lock joint.”
