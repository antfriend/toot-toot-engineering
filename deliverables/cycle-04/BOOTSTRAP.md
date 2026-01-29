# BOOTSTRAP (cycle-04)

## Prompt recap
Observability:
- Add a simple monitor (text UI) that subscribes to group traffic
- Show message flow and node activity
- Optional log export

## Team composition (roles)
- Bootstrap (this step)
- Storyteller
- Orchestrator
- Core worker
- Reviewer
- Delivery packager

## High-level objectives
1. Provide a lightweight monitor CLI for group traffic.
2. Track per-node activity and show periodic summaries.
3. Support optional log export in JSON lines.

## Recommended plan adjustments
- Add a new module `ttn/monitor.py` and wire it to the main CLI.
- Reuse structured logging so monitor output is consistent.

## Target deliverables
- Monitor implementation
- README updates for usage
- Cycle summary and delivery notes

---

## Retrospective (cycle-04)
### What worked
- Reusing the logging utility kept monitor output consistent with node logs.
- Summary intervals delivered “text UI” without terminal dependencies.

### What to improve next cycle
1. **Automated demo harness**
   - Turn the manual demo into a repeatable test script.
2. **Interop validation**
   - Add a checklist for multicast vs peer-fanout across device classes.
3. **Diagnostics bundle**
   - Offer a script that collects config + logs for debugging.

### Plan/role adjustments recommended
- Keep current roles; consider a test engineer role if automation is added.

## Next-cycle prompt candidates (human must choose one)
1. **Automated demo harness:** “Create a script that starts three nodes, runs the demo scenario, and verifies receipt logs.”
2. **Interop test guide:** “Provide a concise device-to-device test checklist for multicast and peer-fanout behavior.”
3. **Diagnostics bundle:** “Add a script that collects configs and recent logs into a debug bundle.”

## Done criteria for this step
- This file includes the retrospective and three next-cycle prompts grounded in cycle-04 deliverables.
