# MQTT Topic Map (tte/)

## Raw lanes
- `tte/raw/meshtastic` — raw inbound packets (JSON)

## State lanes
- `tte/state/node/<node_id>` — node online/offline and last-seen

## Event lanes (semantic)
- `tte/event/presence`
- `tte/event/sensor/temperature`
- `tte/event/emergency/medical`
- `tte/event/logistics/request`
- `tte/event/logistics/offer`
- `tte/event/bulletin/post`
- `tte/event/bulletin/reply`
- `tte/event/command/directed`
- `tte/event/status/request`

### Example payload (SemanticEvent)
```json
{
  "event_id": "44.0123,-115.9876",
  "event_type": "sensor",
  "intent": "sensor_reading.temperature",
  "confidence": 1.0,
  "ts": "2026-01-27T18:14:02Z",
  "reported_by": "node:esp32-field",
  "addressed_to": "broadcast",
  "mesh_meta": {"rssi": -112, "snr": 6.5, "hop_count": 2, "channel": "primary"},
  "entities": [{"type": "sensor", "id": "sensor:temp"}],
  "payload": {"value": 17.4, "unit": "C"},
  "edges": [{"edge_type": "reports_sensor", "source": "node:esp32-field", "target": "sensor:temp"}],
  "raw_ref": "raw:sha256:..."
}
```
