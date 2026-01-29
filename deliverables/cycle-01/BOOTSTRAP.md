# BOOTSTRAP (cycle-01)

## Prompt interpretation
We need an improved STL of the **HORN_GRILL_HOLDSTER** object. Inputs:
- `HORN_GRILL_HOLDSTER_SCAN.stl`: a 3D scan mesh (likely noisy/faceted).
- `HORN_GRILL_HOLDSTER_IMAGE.png`: a photo reference.

Goal: produce a new STL that **more accurately represents the nice smooth curves of the top rim**, i.e., reduce scan artifacts and re-establish clean, manufacturable surface continuity (especially around the rim).

Constraints/assumptions:
- We only have the scan STL + a single photo; no CAD source.
- We should preserve functional geometry (fit/clearances) while smoothing the rim.
- The most realistic pipeline here is: **analyze mesh → isolate rim region → reconstruct/smooth rim surface → re-mesh and validate watertightness → export STL**.

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

## Suggested next-cycle prompts (human must choose one)
1. **Functional-fit refinement**: “Using the improved rim STL from cycle-01, add parametric allowances and test-fit features (clearance, wall thickness), and output a version optimized for 3D printing.”
2. **Aesthetic + manufacturability**: “Further redesign the rim with a CAD-quality fillet and consistent thickness, producing a ‘clean CAD remake’ STL while preserving the original’s mounting geometry.”
3. **Documentation & verification**: “Create a verification package: renders, cross-sections, dimensional report, and a step-by-step reproducible script so anyone can regenerate the improved STL from the scan.”
