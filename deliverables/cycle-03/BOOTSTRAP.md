# BOOTSTRAP (cycle-03)

## Prompt recap
Device-targeting:
- Write device-specific run/setup guides for Unihiker K10 and Lilygo T-Deck Plus
- Adapt the code to a MicroPython-friendly subset if needed
- Keep the same TTN message schema

## Team composition (roles)
- Bootstrap (this step)
- Storyteller
- Orchestrator
- Core worker
- Reviewer
- Delivery packager

## High-level objectives
1. Provide clear device-specific setup guidance for K10 and T-Deck Plus.
2. Add a MicroPython-friendly reference implementation.
3. Preserve the same TTN JSON schema across CPython and MicroPython.

## Recommended plan adjustments
- Add a device guide doc under `docs/`.
- Introduce a minimal `ttn_mpy/` folder for MicroPython devices.

## Target deliverables
- `docs/DEVICE_GUIDES.md`
- `ttn_mpy/` MicroPython-friendly code
- Updated README references

---

## Retrospective (cycle-03)
### What worked
- Separating MicroPython code into `ttn_mpy/` avoided touching the CPython runtime.
- Device guides reduced ambiguity about Wi-Fi/IP and config setup.

### What to improve next cycle
1. **Observability**
   - Add a simple monitor for group traffic and node activity.
2. **Automated demo harness**
   - Script a full end-to-end demo with automated checks.
3. **Interop test notes**
   - Provide a checklist for cross-device multicast vs peer-fanout behavior.

### Plan/role adjustments recommended
- Keep current roles; add a quick monitor doc step in future cycles.

## Next-cycle prompt candidates (human must choose one)
1. **Observability:** “Add a simple monitor (text UI) that subscribes to group traffic and shows message flow and node activity, with optional log export.”
2. **Automated demo harness:** “Create a script that starts three nodes, runs the demo scenario, and verifies receipt logs.”
3. **Interop test guide:** “Provide a concise device-to-device test checklist for multicast and peer-fanout behavior.”

## Done criteria for this step
- This file includes the retrospective and three next-cycle prompts grounded in cycle-03 deliverables.
