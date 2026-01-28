# BOOTSTRAP (cycle-01)

## Prompt recap
Build a minimal, complete **3-node TTN (Toot-Toot Network)** messaging system on a single IP subnet:
- Direct messages node-to-node
- Broadcast to whole group
- End-user configured `NODE_NAME` and `NODE_IP` (plus ports, group address, peers)
- Clear setup instructions
- Minimal runnable implementation + demo script
- Python 3.10 default
- No Meshtastic/LoRa

## Proposed transport
**UDP** (unicast + multicast).
- **Why:** simplest (no broker), minimal dependencies, works well on a single subnet.
- **Direct message:** UDP unicast to a specific node IP:PORT.
- **Group/broadcast:** UDP multicast to a GROUP_IP (e.g., `239.255.0.1`) + GROUP_PORT.

Fallback: if multicast is not available on a given device/network, implement broadcast as “send to all peers” while keeping UDP as the only transport.

## Team composition (roles)
- **Bootstrap (this step):** interpret prompt, propose approach, define success criteria, recommend plan adjustments.
- **Storyteller:** make the user experience coherent: names, CLI verbs, happy-path demo narrative.
- **Orchestrator:** convert plan into repo structure + task breakdown; ensure logging/plan updates.
- **Core worker:** implement:
  - `ttn/node.py` runtime
  - config loader
  - message schema + minimal validation
  - demo/simulation helper
- **Reviewer:** verify spec compliance, runnable steps, edge cases (multicast fallback, Windows firewall notes).
- **Delivery packager:** polish README, capture final “how to run” instructions and outputs.

(An SVG engineer is **not needed** for this cycle.)

## High-level objectives
1. **Runnable on Windows 11** (as baseline) with 3 simulated nodes in separate terminals.
2. **Config-driven** node identity and networking:
   - `NODE_NAME`, `NODE_IP`, `NODE_PORT`
   - `GROUP_IP`, `GROUP_PORT`
   - `NODE_PEERS` (name->ip mapping)
3. **Simple TTN JSON message schema** with UUID + timestamp.
4. **Demonstrate scenario**: A→B direct, B→A reply, C→broadcast, all log receipts.
5. **Clear instructions for non-experts**:
   - choosing unique names
   - reserving static IPs / DHCP reservations
   - editing config files
   - starting nodes, sending messages

## Recommended plan adjustments
1. **Skip SVG engineer step** (not relevant).
2. Add an explicit step for **“Repo skeleton + module layout + README draft”** before core coding, to reduce churn.
3. Add a lightweight **interop/testing note** step: Windows firewall + multicast caveats.

## Proposed repo/module layout (target)
```
/ttn/
  __init__.py
  config.py
  message.py
  transport_udp.py
  node.py
/scripts/
  run_three_nodes.py
/config/
  node_a.env
  node_b.env
  node_c.env
README.md
requirements.txt
```

---

## Retrospective (cycle-01)
### What worked
- **UDP-only approach** stayed minimal and dependency-free.
- The **CLI verbs** (`listen`, `direct`, `broadcast`) match the user mental model.
- `.env` configs under `config/` were easy to edit and explain.

### What to improve next cycle
1. **Add a real automated demo harness**
   - A script that starts 3 node processes, sends the scenario, asserts logs/receipts, then exits.
   - This would turn “manual demo” into a repeatable test.
2. **Improve multicast UX + detection**
   - Detect multicast support at startup and print a clear message:
     - “Multicast OK” or “Multicast unavailable; broadcast will use peer fanout.”
3. **Device targeting guidance**
   - Add a short doc for “how to run on Unihiker K10 / Lilygo T-Deck Plus” with notes about Python availability, Wi‑Fi setup, and firewall equivalents.

### Plan/role adjustments recommended
- Keep current roles; **no SVG engineer** unless future cycles add visualization.
- Consider adding an explicit **Test engineer** step if we add automated process-based tests.

## Next-cycle prompt candidates (human must choose one)
1. **Hardening + packaging:** “Add robust CLI UX, better structured logging, and a multicast fallback mode that is explicitly detectable and user-visible, while keeping zero external dependencies.”
2. **Device-targeting:** “Write device-specific run/setup guides for Unihiker K10 and Lilygo T-Deck Plus, and adapt the code to a MicroPython-friendly subset if needed, keeping the same TTN message schema.”
3. **Observability:** “Add a simple monitor (text UI) that subscribes to group traffic and shows message flow and node activity, with optional log export.”

## Done criteria for this step
- This file includes the retrospective + 3 next-cycle prompts grounded in cycle-01 deliverables.
