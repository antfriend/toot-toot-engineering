# CHECKLIST

## Step completion
- Required role assets are created/updated with no placeholders.
- When the Storyteller role is in the plan, `deliverables/cycle-XX/STORYTELLER.md` exists and reflects narrative refinements.
- If the prompt centers on SVG output, `deliverables/cycle-XX/SVG_ENGINEER.md` exists and documents SVG constraints and guidance.
- Deliverable outputs are in `deliverables/cycle-XX/` and the cycle number matches the current plan.
- Promote any reusable artifacts into `library/` or `standards/` and ensure cycle-only files stay in `deliverables/cycle-XX/`.
- `PLAN.md` marks the current step complete and sets the next step.
- `LOG.md` includes a new entry for the step.
- `RELEASES.md` reflects current cycle deliverables and status.
- Files referenced in `README.md` and `PLAN.md` exist.
- Humans only need to start the run; agents proceed automatically and only request feedback if blocked.
- Delivery gate: do not start a new cycle until the primary deliverable exists or a blocking issue is logged in `LOG.md`.
- When production steps exist (image/PDF), the cycle must produce at least one production artifact (e.g., PDF or image assets), not just documents.
- Final deliverables include a small Toot Toot Engineering logo appropriate for the media (embedded or as a companion asset based on `toot-toot-logo.png` or `toot-toot-logo.svg`).

## Consistency
- Workflow version is aligned across docs.
- Links in `README.md`, `WHAT.md`, and `PLAN.md` resolve.
