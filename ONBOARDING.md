# Mortal Engines Onboarding (Human-Friendly)

Welcome! This guide is for first-time humans who want to run a Mortal Engines cycle without knowing the internals.

## What you do (short version)
1. Read `README.md` to understand the current prompt.
2. Open `PLAN.md` to see the current step.
3. Say "go" to start the run.
- (Optional) see ['Human Monitor'](README.md#human-monitor) to livestream the progress
4. Wait while the agent completes steps automatically; respond only after the final step or if a blocking issue is raised.
5. Give feedback at the end of the plan before starting the next cycle.

## First run (exact phrases)
1. In chat, say: `go`
2. Wait while the agent completes the steps.
3. When asked for feedback, reply with a short sentence like: `this is excellent!`

## What the agent does
- Follows the roles and rules in `AGENTS.md`.
- Writes outputs into `deliverables/cycle-XX/`.
- Updates `PLAN.md` and `LOG.md` every step.
- Produces `deliverables/cycle-XX/STORYTELLER.md` when the Storyteller role is in the plan.
- Provides 3 suggested next-cycle prompts grounded in the latest deliveries and asks the human to choose one.
- If the prompt centers on SVG output, produces `deliverables/cycle-XX/SVG_ENGINEER.md` with SVG constraints and guidance.

## When to stop planning
- If the plan includes image generation or PDF assembly, the next cycle must execute those steps.
- Only start a new planning cycle if a blocker is logged in `LOG.md`.

## Example rule
- If a PDF builder is in the plan, the next cycle must produce a PDF or document the blocker.

## Files you should know
- `README.md` = the overview and cycle 01 prompt.
- `PLAN.md` = current step and critical path.
- `LOG.md` = decisions and handoffs.
- `RELEASES.md` = cycle summaries.
- `MORTAL-ENGINES-FRAMEWORK-RELEASES.md` = framework versions.

## Starting a new cycle
1. Decide a new prompt.
2. Put it in the next cycle's `deliverables/cycle-XX/BOOTSTRAP.md`.
3. Update `PLAN.md` to point to the new cycle and start at Bootstrap.

## New cycle checklist (paths and actions)
- Create `deliverables/cycle-XX/`.
- Add `deliverables/cycle-XX/BOOTSTRAP.md` with the new prompt and objectives.
- Update `PLAN.md` with the new cycle number and current step.
- Add a cycle entry to `RELEASES.md`.
- Update the cycle entry in `RELEASES.md` with deliverables as they are produced.

## Changing the prompt
1. For cycle 01, edit the prompt section in `README.md`.
2. For later cycles, update the `Prompt` section in that cycle’s `deliverables/cycle-XX/BOOTSTRAP.md`.
3. If you change the prompt mid-cycle, note it in `LOG.md`.

## How to check progress
- Open `monitor.html` via `./serve-monitor.sh`.
- Watch `PLAN.md` and `LOG.md` update live.

## Common pitfalls
- Skipping `PLAN.md` updates (the plan is the source of truth).
- Mixing cycle outputs in the wrong folder.
- Forgetting to update `LOG.md` after each step.

## When to ask for help
- If a step is unclear or blocked.
- If you want a different format (comic, storyboard, report).
- If you want to change the workflow rules.
