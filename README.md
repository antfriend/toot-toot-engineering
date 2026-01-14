# Mortal Engines
![Toot Toot Engineering logo](toot-toot-logo.svg)
Toot Toot Engineering

Workflow version: 3.5

## You, the reader,
are either a human or an agent.   
Welcome!
### You have entered the program.

We are all mortal engines here. 

### prompt:

    Create a beautiful, colorful, animated Toot Toot Engineering logo in SVG with CSS and named 'toot-toot-logo.svg'. Use the Mortal Engines framework for inspiration and include as much detail and metaphoric imagery as we can possibly do. Make the aspect ratio super cinematic.


## What this is
Like a factory that makes a factory to produce the desired product. There is production logging and monitoring and all the factory tools and assets as well as the final product in a local deliverables directory.
Literally a structured, role-based workflow for turning creative prompts into finished deliverables, with clear step handoffs, logging, and cycle tracking.

## Main features
- Critical-path plan in `PLAN.md` with step-by-step role handoff.
- Cycle-based deliverables under `deliverables/cycle-XX/`.
- Required logging in `LOG.md` for every step.
- (Optional) see ['Human Monitor'](/README.md#human-monitor) to livestream the progress
- Built-in review and delivery packaging steps.
- Human feedback captured after the final step.
- Cycle releases in `RELEASES.md`.
- Framework releases in `MORTAL-ENGINES-FRAMEWORK-RELEASES.md`.

## Delivery focus (definition of done)
A cycle is done only when the primary deliverable exists and is validated. For comics, that means:
- A print-ready PDF exists in the cycle output.
- Source assets and build notes exist alongside the PDF.
- Review confirms print specs (trim/bleed/safe area) and narrative coherence.
Do not start a new cycle unless the deliverable exists or a blocker is logged in `LOG.md`.

### prompt-continued:
We break the prompt down into the different roles and tasks of a critical path of all the steps in the process of building a solution. All the best roles of every appropriate type are engaged, and new ones added if needed, for excellent production value.

At a simple level, the framing is just about getting from point A to point B: from a prompt to a complete solution. The Bootstrapper estimates the complexity and the roles needed to build the team to complete the job with excellence.

Assets are generated in a single git repo (like this one!) in an iterative process following the critical path in [`PLAN.md`](PLAN.md). Iterations consist of a single step performed by a single agent in a single role. Deliverable outputs are stored under `deliverables/cycle-XX/`.

The default starting agent role is the bootstrap. They interpret the prompt and propose team composition, objectives, and plan adjustments. The orchestrator then builds the initial plan, [`PLAN.md`](PLAN.md), [`AGENTS.md`](AGENTS.md), role definitions, rules, and logging assets, and can optimize the critical path. Upon completion of that, they update the plan file to show the first step as complete and move the placeholder to start with the next agent role, for the next step. The plan file serves as an easy to read table of contents of what is to come and what has been done so far.

```
The user, that's you human, repo forker, can say "go", "proceed", "next", "I believe in you" or any similar AFFIRMATIVE to start the cycle. Agents proceed automatically between steps unless feedback is required to continue, then request human feedback at the end. If you ask for a mid-cycle pause or review, agents should comply.
```  

Different roles review each others work, make choices, revise the plan, and produce the assets used to move to the next step.

In this way the production value is enriched. Supporting details and source assets are generated for later steps as needed.

During each step, the human co-producer clicks the guardrail approval pop-ups, if any, in their development environment and at the end of a step, optionally commits the work to the repo.   

The plan is updated and revised as it progresses. The human co-producer can watch progress in the [`PLAN.md`](PLAN.md).md file and the [`LOG.md`](LOG.md). Humans can refer to the [Human Monitor](#human-monitor) section for running a live monitor.  Iteratively, step-by-step, the requested product is produced, reliably, repeatably, excellently. Deliverables land in `deliverables/cycle-XX/`.

In short, Mortal Engines takes a prompt, makes a plan, reviews the plan, updates and follows the plan, in a grand sequence of iterations until the final output is produced with EXCELLENCE!

This is a fork-able app. It is shared and propagated by forking. To create a variant, branch it or fork it.


## Plan file
- The plan file name is fixed: [`PLAN.md`](PLAN.md).
- [`PLAN.md`](PLAN.md) is the authoritative table of contents for the critical path and all generated deliverable assets.

## How it works
1. Provide a prompt (cycle 01 uses the prompt in this README; later cycles define the prompt in their `BOOTSTRAP.md`).
2. The bootstrap role creates `deliverables/cycle-XX/BOOTSTRAP.md` with team, objectives, recommended plan adjustments, and 3 suggested next-cycle prompts grounded in the latest deliveries (human chooses one).
3. The storyteller refines and elevates the central story or creative thread, producing `deliverables/cycle-XX/STORYTELLER.md`.
4. The orchestrator creates (or modifies) [`PLAN.md`](PLAN.md), [`AGENTS.md`](AGENTS.md), and [`LOG.md`](LOG.md), and optimizes the plan.
5. The core worker produces the primary solution assets.
6. The reviewer checks for correctness and gaps, producing `deliverables/cycle-XX/REVIEW.md`.
7. The delivery packager assembles final assets and export notes in `deliverables/cycle-XX/DELIVERY.md`.
8. The retrospective suggests role/plan changes to prevent issues or improve outcomes, and updates `deliverables/cycle-XX/BOOTSTRAP.md`.
9. The human co-producer approves guardrail pop-ups and commits changes, if desired after each step. Agents proceed automatically between steps unless feedback is required, and request feedback after the final step.

## Execution rule
Planning cycles are capped at 1. Once a production pipeline exists (e.g., image generation + PDF assembly), the next cycle must execute it unless a blocking issue is logged.


## Quality bar
- Factual claims include sources when relevant; uncertainties are labeled and deferred.
- Third-party assets include owner/source, status, and any usage constraints or substitutes.

## Quick start
1. Read [`README.md`](README.md) and [`WHAT.md`](WHAT.md) for intent and scope.
2. Open [`PLAN.md`](PLAN.md) to see the current step.
3. Create a `deliverables/cycle-XX/` folder for this cycle’s outputs.
4. Execute the current role using [`AGENTS.md`](AGENTS.md) and produce the named assets in `deliverables/cycle-XX/` unless exempted.
5. Complete the step using [`CHECKLIST.md`](CHECKLIST.md).
6. Append the entry in [`LOG.md`](LOG.md) (create it if missing, using the template in [`AGENTS.md`](AGENTS.md)) and hand off for commit.

## Human Monitor
1. Run `./serve-monitor.sh` in your terminal
2. open [`http://localhost:8000/monitor.html`](http://localhost:8000/monitor.html) to watch `PLAN.md` and `LOG.md` live.

## More
- See [`WHAT.md`](WHAT.md) for the conceptual overview.
- See [`AGENTS.md`](AGENTS.md) for expected asset names per role.
- See [`CHECKLIST.md`](CHECKLIST.md) for step completion and consistency checks.
- See [`RELEASES.md`](RELEASES.md) for cycle summaries.
- See [`MORTAL-ENGINES-FRAMEWORK-RELEASES.md`](MORTAL-ENGINES-FRAMEWORK-RELEASES.md) for framework releases.
- See [`ONBOARDING.md`](ONBOARDING.md) for a beginner-friendly guide.

## Easter eggs
- If the human literally says "AFFIRMATIVE" the agent should provide a snappy reply including themes from the project and the step.
- If the human literally says "you got this" the agent should proceed and continue to "go" through each step until the start of the next cycle.
