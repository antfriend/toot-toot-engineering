# CHECKLIST

## Step completion
- Required role assets are created/updated with no placeholders.
- Deliverable outputs are in `deliverables/cycle-XX/` and the cycle number matches the current plan.
- Promote any reusable artifacts into `library/` or `standards/` and ensure cycle-only files stay in `deliverables/cycle-XX/`.
- `PLAN.md` marks the current step complete and sets the next step.
- `LOG.md` includes a new entry for the step.
- `RELEASES.md` reflects current cycle deliverables and status.
- Files referenced in `README.md` and `PLAN.md` exist.
- Humans only need to start the run; agents proceed automatically unless feedback is required.
- Delivery gate: do not start a new cycle until the primary deliverable exists or a blocking issue is logged in `LOG.md`.
- When production steps exist (image/PDF), the cycle must produce at least one production artifact (e.g., PDF or image assets), not just documents.

## Consistency
- Workflow version is aligned across docs.
- Links in `README.md`, `WHAT.md`, and `PLAN.md` resolve.
