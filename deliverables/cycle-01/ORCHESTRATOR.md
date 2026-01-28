# cycle-01 ORCHESTRATOR

## Goal of this step
Convert the prompt into an executable repo plan: confirm module layout, define concrete artifacts the Core worker must produce, and ensure the remaining steps can validate “definition of done”.

## Confirmed module / folder layout (to be created by Core worker)
Proposed project skeleton (Python 3.10):

```
.
├─ receiver/
│  ├─ __init__.py
│  ├─ types.py                  # NormalizedPacket dataclass/schema helpers
│  ├─ receiver_simulated.py     # feeds demo packets
│  ├─ receiver_meshtastic_serial.py
│  ├─ receiver_meshtastic_tcp.py
│  └─ receiver_meshtastic_ble.py (optional)
├─ semantic/
│  ├─ __init__.py
│  ├─ semantic_rules.py         # deterministic pattern rules (required)
│  └─ semantic_ai_enricher.py   # optional
├─ addressing/
│  ├─ __init__.py
│  └─ stable_ids.py             # assign_event_id + collision rule
├─ mqtt/
│  ├─ __init__.py
│  ├─ mqtt_client.py            # publish helpers + subscriptions
│  └─ topic_map.md              # generated/maintained topic taxonomy
├─ db/
│  ├─ __init__.py
│  └─ ttdb_writer.py            # writes MyMentalPalaceDB.md
├─ monitor/
│  ├─ monitor.html              # offline UI (generated or templated)
│  └─ monitor_build.py          # optional generator to embed CSS/JS
├─ ai_librarian/
│  ├─ __init__.py
│  └─ librarian_service.py
├─ demo/
│  ├─ simulate_day.py           # produces a day of NormalizedPackets and runs pipeline
│  └─ fixtures/                 # optional golden outputs
├─ gateway/
│  ├─ __init__.py
│  └─ run_gateway.py            # wires receiver->semantic->id->mqtt->db
├─ deliverables/cycle-01/
│  ├─ BOOTSTRAP.md
│  ├─ STORYTELLER.md
│  ├─ ORCHESTRATOR.md
│  ├─ CONFIG.md
│  ├─ REVIEW.md
│  ├─ DELIVERY.md
│  └─ generated/
│     ├─ topic_map.md
│     ├─ MyMentalPalaceDB.md
│     └─ monitor.html
└─ requirements.txt
```

Notes:
- The repo already contains workflow files; Core worker should add new folders at repo root.
- Place generated demo artifacts under `deliverables/cycle-01/generated/` so the cycle is self-contained.

## Concrete Core-worker deliverables (acceptance)
Core worker must produce at minimum:
1. **Schema docs / code**
   - `NormalizedPacket` structure (matching prompt fields)
   - `SemanticEvent` structure
2. **Rules engine**
   - Deterministic parsing for: presence, status_request, ack, temp reading, emergency medical, directed command, bulletin post, bulletin reply, logistics request/offer.
3. **Stable ID assignment**
   - Configurable `ID_STEP_LAT`, `ID_STEP_LON`
   - Collision rule: move SE until unique
4. **MQTT topic taxonomy**
   - Generate `deliverables/cycle-01/generated/topic_map.md` with topics + schemas + examples
5. **TTDB writer**
   - Generate `deliverables/cycle-01/generated/MyMentalPalaceDB.md` from demo
   - Include cursor section, records, typed edges glossary, umwelt+globe section
6. **Offline monitor**
   - Generate `deliverables/cycle-01/generated/monitor.html`
   - Must load MyMentalPalaceDB.md locally and render:
     - cursor panel
     - graph (dot-style acceptable)
     - filters (node, event_type, time range)
     - story trails highlighting via typed edges
7. **Demo generator**
   - `demo/simulate_day.py` runs end-to-end without hardware or MQTT broker (should have a “dry-run” mode that writes outputs to disk)
   - Optional “live” mode that publishes to MQTT if broker present

## Plan adjustments applied
- Removed SVG engineer step (prompt not SVG-centered).
- Added `deliverables/cycle-01/ORCHESTRATOR.md` and `deliverables/cycle-01/CONFIG.md`.
- Clarified that simulation must produce real generated artifacts in-cycle.

## CONFIG.md expectations
`deliverables/cycle-01/CONFIG.md` should define:
- MQTT host/port/topic prefix
- output paths for DB and monitor
- ID steps
- receiver selection and parameters

