# BOOTSTRAP (cycle-01)

## Prompt interpretation
Build the canonical TTN + TTDB reference for six heterogeneous devices (Windows hub, UNIHIKER K10, three Heltec WiFi LoRa 32 V4 nodes, and LILYGO T-Deck). Deliver specs, working software/firmware for each device, deployment steps, and a full human guide for configuration and acceptance tests. The system is decentralized: each device maintains a local TTDB, stores peer knowledge, and syncs diffs until convergence.

## Team composition
- Bootstrap (done): interpret prompt, propose plan adjustments, identify risks.
- Storyteller: unify the narrative so the guide reads as a coherent, teachable build (network story + operator journey).
- SVG engineer: not required unless we introduce SVG diagrams later; keep optional.
- Orchestrator: structure the plan and establish deliverable paths and step rules.
- Core worker: produce specs, software/firmware artifacts, and deployment guides.
- Reviewer: check correctness vs prompt, RFCs, and specs; verify acceptance tests.
- Delivery packager: assemble final delivery notes and update `RELEASES.md`.
- Retrospective: capture improvements for the next cycle and offer plan reset.

## High-level objectives
- Define a clear, minimal but complete TTN + TTDB spec that aligns with RFCs and standards.
- Provide per-device software/firmware design and implementation notes that are realistic to build and run.
- Provide deployment steps for all six devices, including configuration, flashing, and network join.
- Provide a complete acceptance test guide that validates discovery, messaging, TTDB sync, and resilience.

## Strategic plan adjustments
- Add a dedicated "Specs" output before implementation details, to reduce ambiguity and allow review gating.
- Add a device-by-device matrix covering: role, interfaces, storage, runtime, constraints, and required tooling.
- Add a "TTDB sync protocol" section that explicitly references RFC guidance and the `TTE_PROMPT.md` rules.
- Add a "Risk & assumptions" section that makes hardware dependencies and firmware limitations explicit.
- Keep SVG engineer optional; only introduce if diagramming becomes necessary.

## Risks and unknowns
- Hardware/firmware specifics for Meshtastic and device SDKs could require clarification or substitution.
- K10 serial protocol details may vary by firmware version; treat CLI vs protobuf modes as fallbacks.
- TTDB compaction and diff exchange need concrete algorithms to avoid divergence.

## Retrospective recommendations (pre-cycle)
- If device-specific firmware details become blockers, split the Core worker step into two: "Spec + Interfaces" then "Implementation + Deployment" to allow early review.
- If acceptance tests expand, add a dedicated "Test authoring" step before Reviewer.
- Offer to implement these plan adjustments immediately if the Orchestrator confirms scope expansion.

## Next-cycle prompt options (choose one after cycle-01)
1. "Harden and document the TTDB sync protocol: add security, versioning, and backward compatibility, with tests and migration notes."
2. "Build a monitoring and visualization dashboard for the Windows hub that shows live node status, TTDB sync health, and message flows."
3. "Produce field-deployment packaging: enclosure notes, power management guidance, and reliability playbook for 30-day operation."

## Offer
I can apply the retrospective recommendations and reset the plan with the selected next-cycle prompt once cycle-01 deliverables are complete.

## Retrospective (post-cycle)
### What to change next time
- Add a dedicated “Firmware integration validation” step when Meshtastic modules are involved.
- Add a “UI implementation or parity check” step when LVGL screens are specified.
- Add an explicit “RFC container export” task if TTDB interchange files are required downstream.

### Offer to implement
If you choose a next-cycle prompt, I can immediately apply these changes, reset `PLAN.md`, and start the new cycle with the updated critical path.
