# BOOTSTRAP (cycle-01)

## Prompt (from README.md)
Create a minimally functional print in place gear box STL.

## Interpretation
We need a **single-file 3D printable gearbox** that prints assembled (“print-in-place”) and can transmit motion. Since this repo is plain-text and we may not have CAD kernels available, the safest path is to:
1) specify a **parametric OpenSCAD model** that exports to STL, and
2) provide **print guidance** (clearances, orientation, tolerances) and a simple **verification checklist**.

A “minimally functional” target: a 2-gear reduction inside a simple housing with a hand-turn input shaft and an output shaft, with enough clearance that it can be freed after printing.

## Proposed team composition (roles)
- Bootstrap (this doc)
- Storyteller: clarify what “minimal” means, define a simple success narrative/acceptance criteria.
- Orchestrator: tighten PLAN to match the actual outputs we can generate in-repo (OpenSCAD + STL export instructions), ensure logging and release entries.
- Core worker: implement the parametric gearbox in OpenSCAD and provide export steps.
- Reviewer: sanity-check geometry strategy, clearances, and print-in-place constraints.
- Delivery packager: assemble a clean delivery folder with model source, export notes, and logo inclusion.
- Retrospective: recommend next-cycle improvements (e.g., bearings, multi-stage, involute gears, test coupons).

## Objectives (cycle-01)
1. Deliver a **print-in-place gearbox design** as OpenSCAD source.
2. Provide **export instructions** to produce an STL locally.
3. Provide **print settings & post-processing** notes to free moving parts.
4. Include a **minimal validation plan** (what to check after print).

## Recommended plan adjustments
- Make the Core worker output explicit:
  - `deliverables/cycle-01/gearbox.scad`
  - `deliverables/cycle-01/SOLUTION.md` (explains parameters, export, print notes)
- Keep SVG engineer step optional (prompt is STL/3D, not SVG).
- Ensure Delivery packager updates `RELEASES.md` with delivered files.

## Acceptance criteria (definition of done)
- OpenSCAD file renders without errors.
- Model is a single printable assembly with **at least two intermeshing gears** and **input/output shafts**.
- Clearances are parameterized (default suitable for FDM, e.g., 0.3–0.5 mm depending on printer).
- `SOLUTION.md` documents:
  - how to export STL
  - suggested print orientation
  - recommended slicer settings (layer height, walls, supports off)
  - how to “free” the mechanism safely

## Risks / constraints
- True involute gears are complex; a minimal approach may use simplified tooth forms. We must label limitations.
- Print-in-place success depends heavily on tolerance calibration; we should include a small clearance test or at least guidance.

## 3 suggested prompts for next cycle (human must choose one)
1) "Improve the gearbox to use involute gears and add a 3:1 reduction stage, still print-in-place. Include a clearance test coupon."
2) "Add a ratchet or detent mechanism to prevent back-driving, and document failure modes and material choices."
3) "Design a print-in-place planetary gearbox with a simple housing and standardized shaft interface."

## Retrospective (cycle-01)
What to improve next time:
- Add a small **clearance test coupon** (multiple gaps) so users can calibrate `clearance` before printing the full gearbox.
- Consider switching to an **involute gear generator** (or a proven OpenSCAD gear library vendored into the repo) for smoother meshing.
- Add optional **mounting holes** and a standardized **output shaft interface** (e.g., 5 mm D-shaft) to make it easier to use in projects.
- Add a simple **backlash and torque** note so expectations match “minimal” gear geometry.

Bootstrap offer:
- If you choose one of the next-cycle prompts above, I can reset `PLAN.md` for cycle-02 and start the next run with that prompt.
