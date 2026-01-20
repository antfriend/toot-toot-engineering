# BOOTSTRAP (cycle-01)

## Prompt interpretation
Produce a 4-minute SVG slideshow that explains how to get started with Toot Toot Engineering, plus a 4-minute monologue to read during playback. If feasible, use `toot-toot-toolbox/MyMentalPalaceDB.db` for screenplay/storyboard storage (overwriting demo records). If feasible, use `time-foundry.svg` for aspect ratio, opening, and closing scenes.

## High-level objectives
- Define a clear narrative arc for a 4-minute onboarding slideshow (roughly 20-30 slides at 8-12 seconds each).
- Deliver a cohesive SVG slideshow file plus a timed monologue script aligned to slide beats.
- Reuse existing assets (`time-foundry.svg`, `toot-toot-logo.svg/png`) where feasible.
- Log decisions and constraints, including data-store feasibility.

## Team composition
- Storyteller: shape the narrative arc and beats, align slide flow to monologue pacing.
- SVG engineer: assess SVG constraints, layout strategy, and reuse of `time-foundry.svg`.
- Orchestrator: finalize plan steps, update `PLAN.md`, and ensure logging rules.
- Core worker: build the SVG slideshow and monologue assets; integrate any DB usage if feasible.
- Reviewer: verify narrative clarity, timing, and asset completeness.
- Delivery packager: assemble final deliverables and update `RELEASES.md`.
- Retrospective: note process improvements for future cycles.

## Feasibility notes and constraints
- `toot-toot-toolbox/MyMentalPalaceDB.db` is not present in the repo; only `toot-toot-toolbox/MyMentalPalaceDB.md` exists. Storing storyboard in a DB may require creating a new DB file or using the existing Markdown as a fallback.
- `time-foundry.svg` exists and can define aspect ratio and opening/closing scenes.
- Deliverables should include a small Toot Toot Engineering logo embedded or provided as a companion asset.

## Recommended plan adjustments
- Add a check to confirm whether a DB file exists or must be created; log the decision and any schema assumptions.
- Explicitly list the SVG slideshow filename and monologue filename in the Core worker step once the Orchestrator updates `PLAN.md`.
- Include a timing map (slide index -> timestamp) to ensure the 4-minute target is met.

## Risks to manage
- Timing drift between slideshow and monologue; mitigate with a structured timing map.
- Overly complex visuals; keep slides legible for non-vibe coders.
- Ambiguity around DB storage; decide early to avoid rework.

## Next-cycle prompts (choose one)
1) Create a concise “quick-start” one-pager PDF derived from the slideshow with a printable checklist.
2) Produce a narrated demo video script that walks through running the Human Monitor during a cycle.
3) Build a reusable SVG slide template pack themed around Mortal Engines for future cycles.

## Retrospective (initial)
To reduce ambiguity in future cycles, add a small “data-store decision” gate early in the plan (DB vs. Markdown) and a standard timing map artifact for any timed media. I can implement these recommendations and reset the plan with a new prompt grounded in the latest deliveries once this cycle completes.
