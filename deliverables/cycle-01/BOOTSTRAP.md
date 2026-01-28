# cycle-01 BOOTSTRAP

## Prompt (interpreted)
Build a minimal, complete system (Python 3.10 gateway) that bridges:
- Meshtastic text packets (from a T-Deck Plus acting as the only mesh node)
- plus two IP-only nodes (Unihiker K10 and an ESP32)
into:
- deterministic **typed semantic events** (TTN-aligned),
- published on an **MQTT** semantic bus,
- stored as a graph-like markdown DB (**MyMentalPalaceDB.md**, TTDB-aligned with umwelt+globe semantics),
- visualized by an **offline** `monitor.html`,
- and optionally served by an **AI librarian** that only transmits back to the mesh when explicitly invoked.

The system must include pluggable receivers (Meshtastic serial/TCP/BLE optional), a semantic rules engine, stable ID assignment with collision avoidance, a topic taxonomy with examples, a DB writer, an offline monitor, and a simulation that replays a “day on the mesh”.

Primary deliverables requested by the prompt:
- Repo-style project layout + modules
- Topic taxonomy (`topic_map.md`)
- DB schema + generated demo DB (`MyMentalPalaceDB.md`)
- Offline UI (`monitor.html`)
- Demo generator and runnable steps
- TTN deployment steps for Windows 11 PC + hybrid mesh/IP 3-node network

## Complexity & approach
This is a medium-sized systems integration + documentation + demo build. The critical path is to:
1) lock down schemas + topic taxonomy, 2) implement pipeline skeleton with a deterministic rules engine, 3) implement DB writer + monitor, 4) implement simulator to prove end-to-end.

We should keep hardware integration “pluggable” and make the demo runnable without hardware via simulation.

## Proposed team composition (roles)
- **Bootstrap** (this step): interpret prompt, propose roles, recommend plan adjustments.
- **Storyteller**: create a coherent narrative/mental model (“a day on the mesh”) that the monitor/DB makes legible; define the “story trails” concept.
- **Orchestrator**: finalize plan and repo scaffolding decisions; ensure step outputs align; update PLAN/LOG.
- **Core worker**: implement the Python gateway pipeline + simulator + monitor + DB writer; create module layout.
- **Reviewer**: verify prompt compliance, deterministic semantics, topic taxonomy completeness, and offline monitor behavior.
- **Delivery packager**: ensure all artifacts exist under `deliverables/cycle-01/`, update `RELEASES.md`, and write final run instructions.

Optional (only if time/need):
- **SVG engineer** not needed (prompt does not center on SVG output).
- **Image producer / PDF assembler** not needed.

## Recommended plan adjustments
1. **Add an explicit “Repo scaffold + module layout” sub-deliverable** early in the Core worker step.
2. **Add a “Config + settings” document** (e.g., `deliverables/cycle-01/CONFIG.md`) to centralize:
   - MQTT broker URL/topic prefix
   - ID_STEP_LAT/LON
   - receiver selection
   - file paths
3. Ensure the demo produces real files in-repo:
   - `deliverables/cycle-01/generated/MyMentalPalaceDB.md`
   - `deliverables/cycle-01/generated/monitor.html`
   - `deliverables/cycle-01/generated/topic_map.md`
4. Keep Meshtastic receiver implementations minimal stubs if hardware access is not possible in this environment; prioritize interface correctness and testability.

## Risks / open issues
- Meshtastic libraries and hardware transport details may vary by OS; mitigate by providing an interface and at least one tested “simulated receiver”.
- “TTN/TTDB aligned” is ambiguous; mitigate by using explicit field naming + typed edges glossary, and referencing RFCs for any LoRa-specific framing if later expanded.

## 3 suggested prompts for next cycle (human must choose 1)
1. **“Hardware-first integration”**: Implement and document a tested Meshtastic serial receiver on Windows 11 for the T-Deck Plus, including troubleshooting notes and a small live capture-to-MQTT demo.
2. **“AI librarian behavior pack”**: Expand the AI librarian with anomaly detection + mesh-compressed responses; add unit tests and a safety policy for “only speak when invoked.”
3. **“Monitor upgrade”**: Improve `monitor.html` with better graph layout (force-directed), search, and export, while keeping it fully offline and parsing `MyMentalPalaceDB.md`.

## Retrospective (cycle-01)
See `deliverables/cycle-01/RETROSPECTIVE.md` for detailed recommendations.

Updated next-cycle prompts (choose 1):
1. **Fix & harden**: Fix DB entity rendering and monitor edge parsing; add golden-output regression check; mark cycle-01 complete.
2. **MQTT + librarian**: Wire MQTT publishing/subscribing end-to-end and implement a minimal AI librarian that summarizes last N hours when invoked.
3. **Meshtastic serial integration**: Implement and document a working Meshtastic serial receiver on Windows 11 (T-Deck Plus → gateway), plus live capture → semantic events → MQTT.
