# BOOTSTRAP (cycle-01)

## Prompt source
- Cycle-01 uses the prompt in `README.md`.

## Interpretation (what we are building)
This repository is itself the “factory”: a role-driven workflow that turns a creative prompt into completed deliverables stored under `deliverables/cycle-XX/`, tracked by `PLAN.md`, and logged in `LOG.md`.

For cycle-01, the product is: a complete, runnable TTE workflow pass that produces the required cycle artifacts (BOOTSTRAP, STORYTELLER, optionally SVG_ENGINEER, then orchestrated plan updates, then a concrete “primary solution asset” output, reviewed, packaged for delivery, and followed by a retrospective).

Because cycle-01’s README does not specify an external creative brief (e.g., “make a comic about X”), we treat the workflow itself as the deliverable: produce the cycle documentation plus at least one tangible production artifact (per `CHECKLIST.md`) to prove the pipeline can output “real stuff,” not just planning docs.

## Primary objectives (cycle-01)
1. **Establish a clean, end-to-end TTE run**: every step produces the named artifacts with no placeholders.
2. **Produce at least one concrete production artifact** (non-trivial file output) under `deliverables/cycle-01/` to satisfy the delivery gate.
3. **Ensure repo consistency**: `PLAN.md` step tracking, `LOG.md` entries, and `RELEASES.md` updated at packaging.
4. **Minimize scope creep**: do not invent extra subsystems unless required for a verifiable end-to-end delivery.

## Proposed team composition (roles)
Core roles on the critical path (aligned with default workflow):
- **Bootstrap** (this step)
- **Storyteller** (provide a narrative “creative thread” for the cycle)
- **SVG engineer** (optional, to guide the SVG artifact)
- **Orchestrator** (tighten plan, ensure files/steps are correct)
- **Core worker** (produce primary solution assets)
- **Reviewer** (quality + gaps)
- **Delivery packager** (assemble final bundle + release notes)
- **Retrospective** (process improvements + seed next cycle prompts)

Optional roles (only if clearly beneficial):
- **Image producer / PDF assembler**: consider if we choose a primary artifact that benefits from it.

## Plan adjustments applied in cycle-01
These recommendations have now been executed in this cycle:
- Step 5 produces:
  - `deliverables/cycle-01/SOLUTION.md`
  - `deliverables/cycle-01/assets/cycle-01-badge.svg` (generated)
  - `deliverables/cycle-01/make_badge.py` (generator)
- The SVG engineer step was executed to document constraints for a clean SVG output.

## Execution notes / constraints
- Do not read anything under `HUMANS/` unless explicitly requested.
- Avoid secrets and credential files.
- Keep artifacts placeholder-free.

## 3 suggested prompts for cycle-02 (human must choose one)
Grounded in cycle-01’s outputs (workflow proved + production artifact generated):
1. **Create a one-page print-ready “Toot-Toot Engineering” quickstart poster** (A4/Letter) with a diagram of roles/steps; generate source SVG and export-ready PDF.
2. **Build a tiny reference implementation**: a Python CLI that scaffolds a new cycle folder and updates PLAN/LOG automatically, with tests and documentation.
3. **Produce a micro-comic (1 page, 6 panels)** about an AI workshop that forges deliverables, with SVG panels and a print-ready PDF.

## Retrospective recommendations (cycle-01)
What to change next time to prevent issues or improve outcomes:
1. **Normalize platform-agnostic commands**: in docs, prefer Python snippets or clearly label commands for Windows vs POSIX.
2. **Tighten `RELEASES.md` branding**: it currently says “Mortal Engines Releases.” Consider renaming to “Toot Toot Engineering Releases” (or similar) in a maintenance step so repo identity is consistent.
3. **Add an explicit “Primary artifact definition” section to `PLAN.md` per cycle** to reduce ambiguity when the prompt is meta (like cycle-01).
4. **Introduce a lightweight validation step** for generated artifacts (e.g., check file exists, non-empty) if/when multiple generators appear.

Offer to implement: If you choose one of the cycle-02 prompts above, the next Bootstrap can reset `PLAN.md` to cycle-02 and create `deliverables/cycle-02/BOOTSTRAP.md` accordingly.
