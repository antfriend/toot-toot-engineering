# BOOTSTRAP (cycle-02)

## Prompt
Harden and document the TTDB sync protocol with security, versioning, and backward compatibility (including tests and migration notes), and build a Windows hub monitoring/visualization dashboard showing live node status, TTDB sync health, and message flows.

## Prompt interpretation
This cycle expands the TTDB sync into a documented, secure, versioned protocol with tests and migration guidance, and upgrades the Windows hub monitoring UI to show live node state, sync health, and message flow visibility. Outputs must align to TTN/TTDB RFCs and remain compatible with the cycle-01 reference build.

## Team composition
- Bootstrap (done): interpret prompt, propose plan adjustments.
- Storyteller: frame the dashboard and sync hardening as a coherent operator story.
- SVG engineer: optional (only if dashboard or protocol diagrams require SVG).
- Orchestrator: define plan and deliverable paths.
- Core worker: implement protocol spec updates, tests, and dashboard build.
- Reviewer: verify protocol security/versioning and dashboard correctness.
- Delivery packager: assemble deliverables and update `RELEASES.md`.
- Retrospective: capture improvements and propose next-cycle prompts.

## High-level objectives
- Define TTDB sync protocol versioning, compatibility rules, and security model.
- Provide migration notes for nodes running cycle-01 sync logic.
- Deliver tests that validate compatibility and sync correctness.
- Build a Windows hub monitoring dashboard with live node status, sync health, and message flow views.

## Strategic plan adjustments
- Add a dedicated "Protocol spec + versioning" deliverable before implementation.
- Add a "Tests and migration" section and artifacts.
- Keep dashboard scope focused on observability, not full admin control.

## Risks and unknowns
- Security model needs realistic assumptions for low-power and intermittent nodes.
- Backward compatibility may require dual-mode sync logic.

## Next-cycle prompt options (choose one after cycle-02)
1. "Add cryptographic identity and signature verification across TTN events and TTDB sync, with key management guidance."
2. "Extend the K10 console UI to LVGL parity with the specified screens, including sync controls and diagnostics."
3. "Create a deployment automation kit for the six-device build (scripts, flashing workflows, and network bootstrap)."

## Retrospective (post-cycle)
### What to change next time
- Add persistent sync health storage (so dashboards survive restarts).
- Add a client-side v2 sync implementation example to validate handshake and signatures end-to-end.
- Add explicit key management guidance (rotation, storage, revocation) when HMAC or signatures are required.

### Offer to implement
If you choose a next-cycle prompt, I can update `PLAN.md` and start the new cycle with these recommendations applied.
