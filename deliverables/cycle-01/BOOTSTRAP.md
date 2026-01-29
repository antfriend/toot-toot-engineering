# BOOTSTRAP (cycle-01)

## Prompt interpretation
We need an improved STL of the **HORN_GRILL_HOLDSTER** object. Inputs:
- `HORN_GRILL_HOLDSTER_SCAN.stl`: a 3D scan mesh (likely noisy/faceted).
- `HORN_GRILL_HOLDSTER_IMAGE.png`: a photo reference.

Goal: produce a new STL that **more accurately represents the nice smooth curves of the top rim**, i.e., reduce scan artifacts and re-establish clean, manufacturable surface continuity (especially around the rim).

Constraints/assumptions:
- We only have the scan STL + a single photo; no CAD source.
- We should preserve functional geometry (fit/clearances) while smoothing the rim.
- The most realistic pipeline here is: **analyze mesh → isolate rim region → reconstruct/smooth rim surface → validate watertightness → export STL**.

## Proposed team composition (roles)
1. **Storyteller**: Translate the vague aesthetic goal (“nice smooth curves”) into concrete acceptance criteria and a crisp definition of “top rim” and “smooth”.
2. **Orchestrator**: Turn the criteria into an executable plan with tools, checks, file paths, and update `PLAN.md`/`LOG.md`.
3. **Core worker (Mesh/CAD)**: Perform mesh processing and rim reconstruction; output the improved STL and notes.
4. **Reviewer**: Validate geometry (watertight, manifold, no self-intersections), compare against scan/photo, and check rim smoothness/continuity.
5. **Delivery packager**: Package outputs, document how to reproduce, and update `RELEASES.md`.

Optional (only if needed):
- **Image producer**: generate quick renders/turntables of before/after for visual validation.

## High-level objectives (cycle-01)
- Create a revised STL with a noticeably smoother, cleaner top rim while maintaining overall dimensions.
- Provide a reproducible workflow (commands/tools/settings) so the rim can be iterated further.
- Provide visual evidence (renders/screenshots) and mesh validation results.

## Recommended plan adjustments
1. Add an explicit **Mesh Analysis + Acceptance Criteria** mini-step before heavy editing (can be part of Orchestrator or Core worker) that records:
   - How “top rim” is defined (height band / feature selection).
   - Target smoothness (e.g., curvature continuity, reduced faceting).
   - Allowed deviation tolerance from scan (e.g., max radial deviation).
2. Add an explicit **Validation artifact** requirement from Core worker/Reviewer:
   - manifold/watertight checks
   - triangle count (before/after)
   - bounding box (before/after)
3. Ensure the cycle produces at least one **production artifact** (the improved STL) plus optional renders.

## Risks / open questions
- Photo provides limited metrology; we may need to rely primarily on the scan for dimensions.
- If the rim in the scan is incomplete/occluded, reconstruction may require inferred geometry.
- Tooling availability: we may need to rely on Python-based mesh tools (`trimesh`, `open3d`, `pymeshlab`) if no GUI tools are assumed.

## Retrospective (end of cycle-01)
### What worked
- The workflow delivered a concrete production artifact (`HORN_GRILL_HOLDSTER_SMOOTH_RIM.stl`) plus reproducible notes and a review.
- Localizing edits to a defined rim band protected the rest of the scan geometry (non-rim vertices unchanged).
- Integrity checks (watertight/manifold) passed before and after.

### What didn’t / limitations
- The rim band selection is purely Z-threshold based; if the rim’s “design intent” extends deeper, a Z band can leave a visible transition.
- Mesh smoothing improves faceting but does not guarantee a truly CAD-like rim profile (e.g., a perfect fillet/arc).
- STL units are unknown (likely mm, but not confirmed), so “0.05 units” band height may not map cleanly to mm without additional context.

### Recommendations for future cycles
- Add (or promote) a small reusable script for generating:
  - cross-section plots at several Z heights
  - a curvature/facet metric proxy around the rim loop
  - a simple before/after render (headless)
- Consider a “surface fit / re-mesh rim” workflow if a truly smooth highlight line is required (fit a circle/ellipse to rim edge, rebuild rim faces, then blend).

## Suggested next-cycle prompts (human must choose one)
1. **Deepen + blend the rim band (mesh-first)**:
   “Starting from `deliverables/cycle-01/HORN_GRILL_HOLDSTER_SMOOTH_RIM.stl`, tune the rim band depth and smoothing parameters, and add a blended transition zone so the change is visually seamless. Output a v2 STL and comparison images.”
2. **CAD-quality rim reconstruction (surface-fit)**:
   “Using the scan STL and photo, reconstruct the top rim as a fitted circle/ellipse + fillet (CAD-like), re-mesh that region, and blend into the existing body while preserving mounting geometry. Output the new STL and a short method report.”
3. **Verification + print readiness package**:
   “Create a verification/print package for the smoothed STL: multiple cross-sections, dimensional/bounding-box report, manifold checks in at least two tools, and recommended slicer settings for a test print.”
