# ORCHESTRATOR (cycle-01)

## Purpose
Stabilize the workflow assets and plan for a document-first delivery: a skimmable, link-rich hardware options summary with reference builds.

## Plan changes applied
- Normalized `PLAN.md` so the checked steps match produced assets.
- Removed the optional SVG engineer step from the critical path (not applicable to this prompt).
- Named the Core worker primary artifact explicitly:
  - `deliverables/cycle-01/HARDWARE_OPTIONS.md`

## Repo state checks
- `deliverables/cycle-01/` exists.
- `deliverables/cycle-01/BOOTSTRAP.md` exists.
- `deliverables/cycle-01/STORYTELLER.md` exists.
- `LOG.md` exists and contains entries for steps 1–2.
- `RELEASES.md` has a Cycle 01 section.

## Remaining critical path (from Step 3 onward)
1. Core worker: produce `deliverables/cycle-01/HARDWARE_OPTIONS.md` (tables + reference builds + pitfalls).
2. Reviewer: produce `deliverables/cycle-01/REVIEW.md` with corrections and gaps.
3. Delivery packager: produce `deliverables/cycle-01/DELIVERY.md` and update `RELEASES.md` primary artifacts.
4. Retrospective: capture improvements and propose next-cycle prompts selection.
