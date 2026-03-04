# BOOTSTRAP (cycle-03)

## Prompt interpretation
Create two SVG animation artifacts for the "One Drop" story:
1. `one_drop_portrait.svg`: a character portrait using only an opaque blue outline oval, a small white reflective bubble oval, and transparent blue infill.
2. `raining.svg`: a continuous POV fall through sky, cloud, fog, and into a mountain lake, with many surrounding raindrops and visible splashes.

## Prompt source decision
`RELEASES.md` references completed cycles 01 and 02, but corresponding cycle folders are not present in the workspace. To avoid blocking execution, this run uses `TTE_PROMPT.md` as the authoritative prompt source and records the mismatch in `LOG.md`.

## Proposed team composition
- Bootstrap
- Storyteller
- SVG engineer
- Orchestrator
- Core worker
- Reviewer
- Delivery packager
- Retrospective

Image producer and PDF assembler are omitted for this cycle because the prompt requests SVG animation deliverables directly.

## High-level objectives
- Deliver the two required SVG files in `deliverables/cycle-03/`.
- Maintain a single continuous narrative arc across both assets.
- Keep files self-contained and editable as source assets for future production cycles.
- Complete workflow documentation (`SOLUTION`, `REVIEW`, `DELIVERY`, `PLAN`, `LOG`, `RELEASES`).

## Plan adjustments
- Treat the SVG engineer step as mandatory (prompt is SVG-centric).
- Keep the critical path linear to preserve role discipline and fast completion.
- Use native SVG animation primitives for portability and easy iteration.

## Acceptance criteria for cycle-03
- `deliverables/cycle-03/one_drop_portrait.svg` exists and follows shape/color constraints.
- `deliverables/cycle-03/raining.svg` exists and depicts the full shot progression.
- `PLAN.md`, `LOG.md`, and `RELEASES.md` are updated with cycle-03 state.
- No placeholders remain in required cycle outputs.

## Retrospective update (step 8)
### What to improve next cycle
- Add a preflight check that validates cycle folder continuity against `RELEASES.md`.
- Add a render-validation script that confirms SVG files parse and include expected IDs/sections.
- Expand delivery packaging to include optional MP4/GIF export for non-SVG playback contexts.

### Recommended role/plan changes
- Insert an optional "Render QA" step between Core worker and Reviewer for animation timing checks.
- Add optional Image producer/PDF assembler steps only when the selected prompt requires non-SVG packaged media.

### Next-cycle prompt candidates (choose one)
1. **Prompt A: Cinematic Camera Pass**
Build `raining_v2.svg` with stronger depth cues (parallax layer groups, speed ramps, and perspective drift), plus a shot timing table in `deliverables/cycle-04/SOLUTION.md`.
2. **Prompt B: Multi-Weather Variants**
Create three alternate scene variants (`raining_dawn.svg`, `raining_storm.svg`, `raining_twilight.svg`) reusing the same story arc but with different color scripts and cloud/fog behaviors.
3. **Prompt C: Export Pipeline Cycle**
Keep current SVGs as source of truth and implement a reproducible export path that generates preview assets (GIF or MP4) with usage notes and quality constraints.

Select one prompt (1, 2, or 3) for the next cycle. I can then implement the retrospective changes and reset `PLAN.md` for that selected cycle prompt.
