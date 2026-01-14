# AGENTS

Workflow version: 3.4

## Roles
- Bootstrap: Interprets the prompt; proposes team composition, high-level objectives, and strategic modifications to roles or the default plan to improve outcomes; concludes with a retrospective recommending role/plan changes to prevent issues or enhance results, and offers to implement the Retrospective recommendations and reset the plan with a new prompt grounded in the latest deliveries. Always suggest 3 prompts for the next cycle that build on the previous cycle and require the human to choose one.
- Orchestrator: Builds the initial plan, roles, rules, and logging assets; optimizes the plan and can add or remove future steps; updates [`PLAN.md`](PLAN.md) to move to the next step.
- Core worker: Produces the primary solution artifacts for the task.
- Image producer: Generates or composes visual assets programmatically (e.g., Python rendering).
- PDF assembler: Builds print-ready PDFs from assets and layout specifications.
- Reviewer: Checks for correctness, gaps, and risks; ensures outputs are ready.
- Delivery packager: Assembles final assets and export notes.
- Retrospective: Summarizes what to change next time to prevent issues or improve outcomes.

## Role outputs (expected assets)
- Bootstrap: `deliverables/cycle-XX/BOOTSTRAP.md`
- Orchestrator: [`PLAN.md`](PLAN.md), [`AGENTS.md`](AGENTS.md), [`LOG.md`](LOG.md)
- Core worker: task-specific primary outputs (e.g., `deliverables/cycle-XX/SOLUTION.md`, `deliverables/cycle-XX/REPORT.md`, or source files).
- Image producer: `deliverables/cycle-XX/IMAGE_ASSETS.md` and generated art under `deliverables/cycle-XX/assets/`
- PDF assembler: `deliverables/cycle-XX/PRINT_PDF.md` and `deliverables/cycle-XX/output/`
- Reviewer: review notes and any required fixes (e.g., `deliverables/cycle-XX/REVIEW.md`).
- Delivery packager: `deliverables/cycle-XX/DELIVERY.md`, updates `RELEASES.md` with cycle deliverables.
- Retrospective: updates `deliverables/cycle-XX/BOOTSTRAP.md` with recommended plan changes.

## Rules
- If you haven't read the readme then read the readme.
- One step, one agent, one role.
- Each step produces named assets and updates [`PLAN.md`](PLAN.md).
- The Bootstrap role must propose 3 next-cycle prompts grounded in the previous cycle and require the human to select one.
- Deliverable outputs are always written under `deliverables/cycle-XX/`, where `XX` is the cycle number.
- Cycle folders track state; filenames remain stable within the cycle (e.g., `BOOTSTRAP.md`, `SOLUTION.md`).
- [`PLAN.md`](PLAN.md) records the deliverables path for each step that produces outputs.
- Cycle-specific artifacts stay within their `deliverables/cycle-XX/` folder unless explicitly promoted.
- Promoted artifacts intended for reuse are copied into `library/` or `standards/` with an updated name/version.
- [`PLAN.md`](PLAN.md) includes an "Inputs for this cycle" list of allowed references.
- Cycle-only files use a `-draft` or `-cycle` suffix to discourage cross-cycle reuse without promotion.
- Cycle 01 uses the prompt in [`README.md`](README.md); subsequent cycles define their prompt in that cycle's `BOOTSTRAP.md`.
- The bootstrap role proposes team composition and plan adjustments; the orchestrator finalizes them in [`PLAN.md`](PLAN.md).
- A step may not be marked complete in [`PLAN.md`](PLAN.md) if its output contains placeholders (e.g., `<to verify>`, `<source>`, `ƒ?`).
- Placeholder files are created at the step they are needed, not upfront.
- Final delivery requires review complete and all placeholders resolved.
- In revision cycles, each role updates existing assets in place rather than creating new versions.
- Use [`LOG.md`](LOG.md) to record decisions, changes, and open questions.
- Update `RELEASES.md` with cycle deliverables when they are produced (at least during Delivery packager).
- The human co-producer starts the run and is not normally needed between steps; agents proceed automatically unless feedback is required to continue.
- Agents proceed without soliciting human feedback between steps.
- Request human feedback only after the final plan step is completed.
- If the human requests a mid-cycle pause or review, comply.

## Logging
- Append to [`LOG.md`](LOG.md) at the end of each step. Also append any fixes or enhancements between steps.
- Include: step id, role, summary, decisions, open questions, and next step.
- If `LOG.md` is missing, create it with a `# LOG` header and a `## Entries` section.
### Entry template
```
- Step: <step id>
- Role: <role>
- Summary: <what was completed>
- Decisions: <key choices made>
- Open questions: <items to resolve later>
- Next step: <who goes next>
```
