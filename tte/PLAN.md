# PLAN

## Current cycle
- cycle-01

## Current step
- [ ] Step 4 (cycle-01): Core worker implements procedural model generation and produces the primary STL + source + print notes. (`deliverables/cycle-01/source/`, `deliverables/cycle-01/output/`)

## Inputs for this cycle
- `README.md` (cycle-01 prompt source)
- `WHAT.md`
- `AGENTS.md`
- `CHECKLIST.md`
- `RELEASES.md`
- `MORTAL-ENGINES-FRAMEWORK-RELEASES.md`
- `deliverables/cycle-01/BOOTSTRAP.md`
- `deliverables/cycle-01/STORYTELLER.md`

## Critical path
- [x] 1. Bootstrap interprets the prompt, proposes team composition, and recommends plan adjustments. (`deliverables/cycle-01/BOOTSTRAP.md`)
- [x] 2. Storyteller defines art direction + printable style constraints for the bonsai (silhouette, proportions, “platformer world” cues, minimum feature thickness). (`deliverables/cycle-01/STORYTELLER.md`)
- [x] 3. Orchestrator updates the plan for 3D/STL production, adds concrete validation + packaging artifacts, and marks any irrelevant steps as skipped. (`PLAN.md`)
- [ ] 4. Core worker implements procedural model generation and produces the primary STL + source + print notes.
  - Outputs:
    - `deliverables/cycle-01/source/` (generator code)
    - `deliverables/cycle-01/output/` (STL(s))
    - `deliverables/cycle-01/SOLUTION.md` (how to run/regenerate; parameters)
    - `deliverables/cycle-01/PRINT_NOTES.md` (recommended print settings)
- [ ] 5. Reviewer validates manifoldness/printability + style match; documents issues/fixes.
  - Outputs:
    - `deliverables/cycle-01/REVIEW.md`
    - `deliverables/cycle-01/output/validation/` (reports/screenshots if available)
- [ ] 6. Delivery packager assembles final assets and notes; updates `RELEASES.md`.
  - Outputs:
    - `deliverables/cycle-01/DELIVERY.md`
    - update `RELEASES.md`
- [ ] 7. Retrospective recommends workflow improvements and proposes next-cycle prompt selection. (update `deliverables/cycle-01/BOOTSTRAP.md`)

## Validation checklist (3D/STL-specific)
The Reviewer should be able to confirm at minimum:
- STL is readable by a slicer (opens without error).
- Mesh is watertight/manifold (or repair steps are documented and included).
- Units/scale are documented (mm) and model matches intended size (~90mm tall default).
- Minimum feature thickness targets met (>= 1.6mm for FDM defaults), especially branches.
- Model sits flat on base; no floating islands.

## Notes / skipped steps
- SVG engineer step is not applicable for an STL deliverable (skipped for cycle-01).

## Assets index
- `AGENTS.md`
- `LOG.md`
- `PLAN.md`
- `RELEASES.md`
- `MORTAL-ENGINES-FRAMEWORK-RELEASES.md`
- `deliverables/cycle-XX/`
