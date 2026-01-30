# BOOTSTRAP (cycle-01)

## Prompt interpretation
We are building a minimal, runnable **3-node TTN (Toot Toot Network) messaging system** on a single IP subnet, with:
- **Direct messages** node-to-node
- **Broadcast** messages to the group
- **User-configurable** `NODE_NAME`, `NODE_IP`, `NODE_PORT`, `GROUP_IP`, `GROUP_PORT`, and `NODE_PEERS`
- Clear end-user instructions for configuring names and (static/reserved) IPs
- A repo-style delivery including code, schema, demo script, and optional monitoring

Devices:
- Node A: Unihiker K10
- Node B: Lilygo T-Deck Plus
- Node C: Windows 11 PC
- Optional host: Windows 11 PC for simulation/testing/monitoring

### RFC alignment notes
- TTN is *transport agnostic* (TTN-RFC-0001), so choosing UDP/TCP/MQTT is allowed.
- TTN-RFC-0001 includes etiquette like “Explicit AI invocation only”; our deliverable is a **messaging network**, not autonomous AI chatter, so we keep the protocol neutral and do not add auto-AI behaviors.
- TTN-RFC-0003 suggests presence events and a registry for a “Minimal Viable Node”. We incorporate a lightweight presence/hello message and a basic peer registry (config list) without implementing full semantic mesh / TTDB.

## Transport recommendation
**UDP** for v1.
- Simplest, no broker.
- Works on a single subnet.
- Supports broadcast/multicast patterns.
- Code remains small and portable (including MicroPython/CircuitPython possibilities for constrained devices).

We will use:
- **UDP unicast** for direct messages.
- **UDP multicast** (preferred) or **UDP broadcast** (fallback) for group messages.

Implementation note applied during the cycle:
- For simplicity and reliability, the reference implementation enforces **single-port operation**: `GROUP_PORT == NODE_PORT`.

## Proposed team composition (roles)
1. **Storyteller**: Frame the project as a friendly “3-node workshop network” narrative and ensure docs are coherent and approachable.
2. **Orchestrator**: Convert this into a concrete repo layout under `deliverables/cycle-01/`, update PLAN/LOG, and ensure RFC references.
3. **Core worker**: Implement the Python 3.10 reference node + demo runner + schema.
4. **Reviewer**: Validate direct/broadcast flows, config instructions, and “non-expert” usability.
5. **Delivery packager**: Assemble final package, create zip, update RELEASES.

Optional (conditional):
- **SVG engineer**: Not needed unless we decide to add an SVG network diagram.
- **Image producer / PDF assembler**: Not required by the prompt.

## High-level objectives (cycle-01)
- Provide a working reference implementation in Python 3.10 that can run on Windows 11 and act as the baseline for porting.
- Provide device notes for Unihiker K10 and Lilygo T-Deck Plus (install/run constraints, suggested Python stacks), while keeping the runnable reference implementation on Windows.
- Provide a simple JSON message schema and robust logging.
- Provide a one-command demo scenario (or minimal steps) that shows:
  - A → B direct message
  - B → A reply
  - C → broadcast
  - all nodes log receipt

## Recommended plan adjustments
Current PLAN included an optional SVG engineer step. This prompt does **not** center on SVG output.
- Applied: Kept the step but marked as **skipped/not needed**.

Because the prompt explicitly requests “bundled in a zip”, we added a packaging artifact and built the zip.

## Risks / open questions
- **Unihiker K10 and Lilygo T-Deck Plus** may not support full CPython 3.10. We:
  - Keep the reference implementation on Windows.
  - Provide porting guidance (MicroPython-friendly structure).
- UDP multicast support can vary by network; provide broadcast fallback.
- Static IP vs DHCP reservation is router-specific; provide generic guidance and recommend DHCP reservations when possible.

## Retrospective (end-of-cycle recommendations)
What went well:
- Minimal dependency footprint (stdlib-only).
- Clear config story and CLI usage.
- Zip artifact produced early.

What to improve next cycle:
1. **Multicast vs broadcast robustness testing**
   - Add a small network self-test command that checks whether multicast packets are being received on the current LAN.
2. **Port to constrained device runtime**
   - Implement a MicroPython variant (poll loop, no threads) for the T-Deck Plus.
3. **Presence registry**
   - Add an in-memory registry (last-seen timestamps) and a `list-peers` command.

## Next-cycle prompt suggestions (human must choose one)
1. **“Port the TTN UDP node to MicroPython for ESP32-class devices (T-Deck Plus), including a minimal UI and config storage.”**
2. **“Add a monitor dashboard (HTML/JS) that listens to TTN messages and visualizes node presence and message flow in real time.”**
3. **“Add TTDB-style event logging to each node (append-only log file) and implement basic replay/sync on startup.”**
