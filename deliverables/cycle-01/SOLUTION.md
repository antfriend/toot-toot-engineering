# SOLUTION (cycle-01)

## Executive summary
This delivers the canonical six-device TTN + TTDB reference build. Each device maintains a local TTDB as append-only JSON lines with periodic compaction, and gossip-style sync propagates missing records until convergence. Meshtastic handles the radio layer for the Heltec nodes and T-Deck, while the K10 is the serial gateway and UI console, and the Windows hub aggregates, visualizes, and optionally exposes MQTT.

## Specification

### TTN compliance and principles
- TTN compliance: TTN-Base for radio nodes, TTN-Gateway for K10 and Windows hub.
- Core principles: meaning over messages, offline-first, local sovereignty, transport-agnostic storage, explicit AI invocation only.
- Append-only TTDB with typed edges aligned to TTN taxonomy.
- Etiquette: no autonomous AI speech on mesh; only operator-initiated messages or explicit `@AI` invocation.

### Node identity model
- Primary `ttn_node_id`:
  - If GPS available: `gps:<lat>,<lon>` rounded to 6 decimals.
  - Else: `hw:<chip_family>:<mac>` for ESP32-class devices, `hw:windows:<host>` for hub.
- Meshtastic `node_num` stored as attribute in TTDB.

### TTDB storage and compaction
- Primary storage per device: JSON Lines (`ttdb.log`), one record per line.
- Compaction snapshot: `ttdb.snapshot.json` containing last N records and `compacted_at`.
- Hashing: SHA-256 over canonical JSON to support diff exchange.
- Export: optional RFC-compliant TTDB container for hub archival when required by downstream tooling.

### Record kinds (minimum)
- `node`, `presence`, `meshtastic_packet`, `message`, `edge`, `sync_diff`.
- Typed edges align with TTN taxonomy: `knows`, `seen_near`, `connected_over`, `mentions`, `derived_from`, `trusted_by`.

### Meshtastic → TTDB mapping
- NodeInfo → `node` record + `knows` edge.
- Position → `message` (position) + `seen_near` edge + `presence`.
- Telemetry → `message` (telemetry) + `observed` edge.
- Text → `message` (text) + `mentions` edge when `@` tokens are present.
- Any packet → `presence` of sender.

### Gossip sync protocol
- Each node serves recent hash lists and accepts missing records.
- Diff flow:
  - Request: `GET /sync/recent` -> hashes list.
  - Response: `POST /sync/hash_list` with peer hashes -> missing records.
  - Push: `POST /sync/push` with missing records.
- Transport options: Wi-Fi HTTP (primary), Meshtastic chunked text (fallback), USB serial transfer (fallback).

## Device matrix
- Windows Hub: Archivist; interfaces `wifi`, optional `mqtt`; stores full TTDB; runs HTTP sync and visualization.
- UNIHIKER K10: Operator; interfaces `usb`, `wifi`; runs serial gateway, TTDB, and console UI.
- Heltec WiFi LoRa 32 V4 (x3): Scouts; interface `lora`; runs Meshtastic with TTDB logging module.
- LILYGO T-Deck: Scribe; interfaces `lora`, `keyboard`, `display`; runs Meshtastic with TTDB logging module and UI.

## Software and firmware

### Common TTDB utilities (Python)
- File: `deliverables/cycle-01/src/common/ttdb.py`
- Provides JSONL append, hashing, diff, and compaction.

### Windows hub (Python)
- File: `deliverables/cycle-01/src/windows_hub/ttn_hub.py`
- Features: HTTP sync endpoints, TTDB append, health check.
- Optional: integrate MQTT by forwarding `message` records to a local broker.
- Visualization: `deliverables/cycle-01/src/windows_hub/monitor.html` served at `/monitor.html`.

### K10 gateway (Python)
- File: `deliverables/cycle-01/src/k10_gateway/k10_gateway.py`
- Features: serial Meshtastic ingest, TTDB append, presence and message mapping.
- Requires `meshtastic` Python package.

### K10 mesh console UI (LVGL spec)
- Screens: Inbox, Compose, Nodes, Map-lite, Sync, Diagnostics.
- Input model: 5-way navigation with soft keys; keyboard only on T-Deck.
- Storage: read from `ttdb.log` and `ttdb.snapshot.json` for fast pagination.
- Implementation note: this reference build provides a terminal-first UI on K10; the LVGL screen map above is the required layout for embedded UI parity.

### Heltec / T-Deck Meshtastic firmware (C++)
- Files:
  - `deliverables/cycle-01/src/meshtastic_ttndb/TTDBModule.h`
  - `deliverables/cycle-01/src/meshtastic_ttndb/TTDBModule.cpp`
- Features: minimal TTDB JSONL logging to LittleFS.
- Integration: add the module to a Meshtastic firmware build and wire callbacks for node info and packet receive.

## Deployment steps

### 1. Windows hub setup
1. Install Python 3.10+.
2. Create a venv and install dependencies if needed.
3. Run the hub:

```bash
cd deliverables/cycle-01/src
PYTHONPATH=. python windows_hub/ttn_hub.py
```

4. Confirm `GET http://<hub>:8080/health` returns `{"status":"ok"}`.
5. Open `http://<hub>:8080/monitor.html` to view nodes and recent messages.

### 2. K10 gateway setup
1. Install Python 3.10+ on the K10.
2. Install Meshtastic Python library:

```bash
pip install meshtastic
```

3. Connect K10 to Heltec #1 via USB.
4. Run the gateway:

```bash
cd deliverables/cycle-01/src
PYTHONPATH=. python k10_gateway/k10_gateway.py --port /dev/ttyACM0 --k10-id hw:k10
```

5. Verify `deliverables/cycle-01/src/data/ttdb.log` grows as messages are received.

### 3. Heltec and T-Deck firmware
1. Build Meshtastic firmware from source.
2. Add TTDB module files from `deliverables/cycle-01/src/meshtastic_ttndb/`.
3. Wire module callbacks into Meshtastic receive and NodeInfo handlers.
4. Flash Heltec #1, #2, #3, and T-Deck.
5. Configure each device with a unique long name and channel key.
6. Set region, channel name, and PSK consistently across all four radios.
7. Set role to “Client” on Heltecs and “Client Mute” on the T-Deck if using keyboard-only UI.

### 4. Wi-Fi sync (optional)
1. Ensure K10 and hub are on the same LAN.
2. On K10, run a periodic sync loop to exchange hashes with hub.
3. Store sync events as `sync_diff` records.

### 5. TTDB compaction
1. Schedule compaction on each device nightly or after N records.
2. Preserve the append-only log and emit `ttdb.snapshot.json`.

## Acceptance tests

1. K10 sends a text message; at least two radio nodes receive it.
   - Evidence: `message` records on K10 and `ttdb.log` entries on two nodes.
2. Windows hub displays all six nodes.
   - Evidence: `node` records for six devices and presence edges.
3. Power-cycle one Heltec; rediscovery occurs.
   - Evidence: new `presence` record after reboot.
4. TTDB compaction does not lose data.
   - Evidence: snapshot contains last N records and log retains prior lines.
5. Node without Wi-Fi learns about Windows hub via mesh diffs.
   - Evidence: `node` record for hub appears on a Heltec node after sync relay.

## Operator guide (quick)
- Start the hub first, then K10, then radios.
- Watch `ttdb.log` grow at each hop.
- Use the K10 console as the operator’s primary window.
- Run acceptance tests once all devices are online.

## Files produced in this cycle
- `deliverables/cycle-01/SOLUTION.md`
- `deliverables/cycle-01/src/common/ttdb.py`
- `deliverables/cycle-01/src/windows_hub/ttn_hub.py`
- `deliverables/cycle-01/src/windows_hub/monitor.html`
- `deliverables/cycle-01/src/k10_gateway/k10_gateway.py`
- `deliverables/cycle-01/src/meshtastic_ttndb/TTDBModule.h`
- `deliverables/cycle-01/src/meshtastic_ttndb/TTDBModule.cpp`
