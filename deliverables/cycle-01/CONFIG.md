# cycle-01 CONFIG

This file centralizes the runtime/config assumptions used by the Core worker implementation.

## Runtime
- Python: 3.10
- OS target (gateway): Windows 11

## MQTT
- Broker: `localhost`
- Port: `1883`
- Topic prefix: `tte/`

## Receivers
- Default for demo: `receiver_simulated`
- Meshtastic transports (optional, pluggable):
  - serial
  - TCP
  - BLE

## Stable event ID assignment (addressing)
- `ID_STEP_LAT`: `0.0001`
- `ID_STEP_LON`: `0.0001`
- Collision rule: if an `event_id` already exists in the DB, move **South-East** by one step repeatedly until unique.

## Output locations (cycle-scoped)
- Generated DB: `deliverables/cycle-01/generated/MyMentalPalaceDB.md`
- Generated topic map: `deliverables/cycle-01/generated/topic_map.md`
- Generated offline monitor: `deliverables/cycle-01/generated/monitor.html`

## Meshtastic radio profile note
- T-Deck Plus LoRa setting (Step 1 / field setup): **US LONG FAST** @ **906.875 MHz**.
