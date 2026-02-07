# BOOTSTRAP (cycle-03)

## Prompt
Create a deployment automation kit for the six-device build (scripts, flashing workflows, and network bootstrap).

## Prompt interpretation
This cycle delivers practical automation for provisioning, flashing, and bootstrapping the six-device TTN build. Outputs should include scripts and repeatable workflows for Windows hub, K10 gateway, Heltec nodes, and T-Deck, plus a minimal network bootstrap sequence that operators can run reliably.

## Team composition
- Bootstrap (done): interpret prompt, propose plan adjustments.
- Storyteller: frame the automation kit as an operator-run playbook.
- SVG engineer: optional (only if diagrams are required).
- Orchestrator: define plan and deliverable paths.
- Core worker: implement scripts/workflows and documentation.
- Reviewer: validate workflows and risks.
- Delivery packager: assemble notes and update `RELEASES.md`.
- Retrospective: capture improvements and propose next-cycle prompts.

## High-level objectives
- Provide device-specific flashing and setup scripts where feasible.
- Provide a repeatable network bootstrap workflow (ordered steps, checks).
- Keep scripts minimal, inspectable, and reversible.

## Strategic plan adjustments
- Add a device automation matrix listing supported OS/tooling and fallbacks.
- Include dry-run and verification steps for each script.

## Risks and unknowns
- Hardware toolchains vary by platform and may require manual steps.
- Some devices may require GUI tools; document when automation cannot cover it.

## Next-cycle prompt options (choose one after cycle-03)
1. "Build an end-to-end client sync tool for TTDB v2 with CLI and logs."
2. "Ship a persistent sync health datastore and dashboard history view."
3. "Produce a reliability and maintenance guide for long-term field deployments."

## Retrospective (post-cycle)
### What to change next time
- Add device auto-discovery helpers (list serial ports, detect Meshtastic nodes).
- Add script bundling for Windows (single entrypoint with prompts and checks).
- Add a validation checklist that runs before flashing and before network bootstrap.

### Offer to implement
If you choose a next-cycle prompt, I can update `PLAN.md` and start the new cycle with these recommendations applied.
