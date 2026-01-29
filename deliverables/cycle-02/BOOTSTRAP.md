# BOOTSTRAP (cycle-02)

## Prompt recap
Hardening + packaging:
- Add robust CLI UX
- Add structured logging
- Make multicast fallback explicitly detectable and user-visible
- Keep zero external dependencies

## Team composition (roles)
- Bootstrap (this step)
- Storyteller
- Orchestrator
- Core worker
- Reviewer
- Delivery packager

## High-level objectives
1. Improve CLI UX with clearer subcommands and optional config introspection.
2. Introduce structured logging (text and JSON) with selectable log levels.
3. Make multicast capability and fallback behavior explicit in logs.
4. Preserve dependency-free, single-subnet UDP behavior.

## Recommended plan adjustments
- Add a small logging utility module for consistent output across commands.
- Extend `ttn.node` with a lightweight `info` command for quick config checks.
- Keep stdout-based logs to avoid external dependencies.

## Target deliverables
- Updated TTN runtime with structured logging and improved UX
- Documentation updates to describe new CLI flags and fallback visibility
- Cycle summary, review, and delivery notes

---

## Retrospective (cycle-02)
### What worked
- A shared logging utility made output consistent across send/listen/monitor flows.
- Explicit multicast status improved diagnosability without new dependencies.

### What to improve next cycle
1. **Device targeting guidance**
   - Provide device-specific setup/run notes for Unihiker K10 and Lilygo T-Deck Plus.
2. **MicroPython-friendly reference**
   - Add a minimal MicroPython-compatible implementation that preserves the TTN schema.
3. **Simple observability**
   - Add a lightweight monitor for group traffic and node activity.

### Plan/role adjustments recommended
- Keep current roles; add optional monitor documentation to reduce support load.

## Next-cycle prompt candidates (human must choose one)
1. **Device-targeting:** “Write device-specific run/setup guides for Unihiker K10 and Lilygo T-Deck Plus, and adapt the code to a MicroPython-friendly subset if needed, keeping the same TTN message schema.”
2. **Observability:** “Add a simple monitor (text UI) that subscribes to group traffic and shows message flow and node activity, with optional log export.”
3. **Automated demo harness:** “Create a script that starts three nodes, runs the demo scenario, and verifies receipt logs.”

## Done criteria for this step
- This file includes the retrospective and three next-cycle prompts grounded in cycle-02 deliverables.
