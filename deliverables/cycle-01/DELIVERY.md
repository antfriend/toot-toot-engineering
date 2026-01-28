# cycle-01 DELIVERY

## What was delivered (cycle-01)
This cycle delivers a simulator-first, minimal end-to-end pipeline that turns short field messages into typed semantic events, assigns stable IDs, stores them in a TTDB-like markdown DB, and renders them in an offline monitor.

### Deliverables root
- `deliverables/cycle-01/`

### Primary artifacts (generated)
- `deliverables/cycle-01/generated/MyMentalPalaceDB.md` — generated TTDB markdown graph memory
- `deliverables/cycle-01/generated/monitor.html` — offline browser UI that loads the DB markdown
- `deliverables/cycle-01/generated/topic_map.md` — MQTT topic taxonomy and example payload

### Source / implementation
- `receiver/types.py` — NormalizedPacket schema
- `semantic/types.py` — SemanticEvent schema
- `semantic/semantic_rules.py` — deterministic semantic interpreter
- `addressing/stable_ids.py` — stable event_id assignment + collision rule (SE stepping)
- `db/ttdb_writer.py` — TTDB markdown writer
- `demo/simulate_day.py` — “day on the mesh” generator that writes artifacts
- `mqtt/mqtt_client.py` — MQTT helper (stub; demo does not publish yet)
- `gateway/run_gateway.py` — gateway entry point that currently generates demo artifacts

## How to run the demo (no hardware required)
From repo root:

1) Generate outputs
```bash
python -m demo.simulate_day --out deliverables/cycle-01/generated
```

2) View the DB
- Open `deliverables/cycle-01/generated/MyMentalPalaceDB.md`

3) View the offline monitor
- Open `deliverables/cycle-01/generated/monitor.html` in a browser.
  - Note: Most browsers block `fetch()` for `file://` URLs.
  - Workaround: serve the folder with a tiny local HTTP server:

```bash
# from deliverables/cycle-01/generated
python -m http.server 8000
```
Then browse to `http://localhost:8000/monitor.html`.

## System architecture (as implemented in this cycle)
- Simulator generates `NormalizedPacket`s.
- Deterministic rules interpret them into `SemanticEvent`s.
- Stable IDs are assigned.
- TTDB markdown is generated.
- Offline monitor reads the markdown and renders a selectable list + dot-style graph text.

## Known limitations / follow-ups
- **Meshtastic receiver adapters not implemented** (serial/TCP/BLE) in this cycle.
- **MQTT publish/subscribe not wired in demo** (client helper exists).
- **AI librarian service not implemented** yet; only the “directed command” semantic event is generated.
- **Review-noted fixes recommended**:
  - entity IDs double-prefixed in DB output (cosmetic/graph readability)
  - monitor graph edge parsing likely needs adjustment to match DB edge formatting

## Windows 11 gateway deployment notes (outline)
- Install Mosquitto (or another MQTT broker) locally.
- Run the gateway Python process with a Meshtastic receiver transport (to be implemented next cycle).
- Configure T-Deck Plus radio profile: US LONG FAST @ 906.875 MHz.
- IP-only nodes (Unihiker/ESP32) can post structured events to the gateway over HTTP/UDP/MQTT and be normalized into the same semantic schema.

