from __future__ import annotations

import argparse
import os
from datetime import datetime, timedelta, timezone
from typing import List, Set

from receiver.types import NormalizedPacket
from semantic.semantic_rules import interpret_packet
from addressing.stable_ids import assign_event_id, raw_ref_sha256
from db.ttdb_writer import render_ttdb


def iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_demo_packets(start: datetime) -> List[NormalizedPacket]:
    tdeck = "node:tdeck-plus"
    unihiker = "node:unihiker-k10"
    esp32 = "node:esp32-field"

    pkts: List[NormalizedPacket] = []

    # Presence
    for i, n in enumerate([tdeck, unihiker, esp32]):
        pkts.append(
            NormalizedPacket(
                from_id=n,
                to_id="broadcast",
                channel="primary",
                text="PING",
                ts=iso(start + timedelta(minutes=i)),
                rssi=-90 - i,
                snr=7.0 - i * 0.5,
                hop_count=1 if n == tdeck else 0,
                transport="simulated",
            )
        )

    # Temperature readings
    temps = [17.1, 17.3, 17.2, 17.4, 17.6, 18.0, 18.4, 19.2, 20.1, 22.7]
    for j, v in enumerate(temps):
        pkts.append(
            NormalizedPacket(
                from_id=esp32,
                to_id="broadcast",
                channel="primary",
                text=f"TEMP {v}",
                ts=iso(start + timedelta(hours=1, minutes=10 * j)),
                rssi=-105,
                snr=5.5,
                hop_count=0,
                transport="simulated",
            )
        )

    # Sensor alert as bulletin
    pkts.append(
        NormalizedPacket(
            from_id=unihiker,
            to_id="broadcast",
            channel="primary",
            text="#broadcast TEMP ALERT threshold exceeded at node:esp32-field",
            ts=iso(start + timedelta(hours=3, minutes=5)),
            transport="simulated",
        )
    )

    # Logistics request + offer
    pkts.append(
        NormalizedPacket(
            from_id=tdeck,
            to_id="broadcast",
            channel="primary",
            text="LOGISTICS REQUEST bring water to ridge trailhead",
            ts=iso(start + timedelta(hours=4)),
            transport="simulated",
        )
    )
    pkts.append(
        NormalizedPacket(
            from_id=unihiker,
            to_id="broadcast",
            channel="primary",
            text="LOGISTICS OFFER can deliver in 30m",
            ts=iso(start + timedelta(hours=4, minutes=2)),
            transport="simulated",
        )
    )

    # Emergency + acknowledgement
    pkts.append(
        NormalizedPacket(
            from_id=tdeck,
            to_id="broadcast",
            channel="primary",
            text="HELP MEDICAL",
            ts=iso(start + timedelta(hours=6)),
            transport="simulated",
        )
    )
    pkts.append(
        NormalizedPacket(
            from_id=unihiker,
            to_id=tdeck,
            channel="primary",
            text="OK",
            ts=iso(start + timedelta(hours=6, minutes=1)),
            transport="simulated",
        )
    )

    # Bulletin thread + replies
    pkts.append(
        NormalizedPacket(
            from_id=unihiker,
            to_id="broadcast",
            channel="primary",
            text="#broadcast Trailhead closed after 18:00",
            ts=iso(start + timedelta(hours=8)),
            transport="simulated",
        )
    )
    pkts.append(
        NormalizedPacket(
            from_id=tdeck,
            to_id="broadcast",
            channel="primary",
            text="#reply thread:trailhead-closed Acknowledged",
            ts=iso(start + timedelta(hours=8, minutes=5)),
            transport="simulated",
        )
    )
    pkts.append(
        NormalizedPacket(
            from_id=esp32,
            to_id="broadcast",
            channel="primary",
            text="#reply thread:trailhead-closed Sensor node will switch to low power",
            ts=iso(start + timedelta(hours=8, minutes=7)),
            transport="simulated",
        )
    )

    # AI invocation
    pkts.append(
        NormalizedPacket(
            from_id=tdeck,
            to_id="node:AI",
            channel="primary",
            text="@AI summarize 6h",
            ts=iso(start + timedelta(hours=9)),
            transport="simulated",
        )
    )

    return pkts


def generate_outputs(out_dir: str, id_step_lat: float, id_step_lon: float) -> None:
    os.makedirs(out_dir, exist_ok=True)

    start = datetime(2026, 1, 27, 8, 0, 0, tzinfo=timezone.utc)
    packets = build_demo_packets(start)

    events = []
    existing_ids: Set[str] = set()
    for pkt in packets:
        ev, _topic_suffix = interpret_packet(pkt)
        ev.raw_ref = raw_ref_sha256(pkt)
        ev.event_id = assign_event_id(pkt, ev, existing_ids, id_step_lat=id_step_lat, id_step_lon=id_step_lon)
        existing_ids.add(ev.event_id)

        for ed in ev.edges:
            if ed.source == "":
                ed.source = ev.event_id

        events.append(ev)

    with open(os.path.join(out_dir, "topic_map.md"), "w", encoding="utf-8") as f:
        f.write(render_topic_map())

    with open(os.path.join(out_dir, "MyMentalPalaceDB.md"), "w", encoding="utf-8") as f:
        f.write(render_ttdb(events, id_step_lat=id_step_lat, id_step_lon=id_step_lon))

    # monitor.html is written as a static file by the Core worker under deliverables/cycle-01/generated/


def render_topic_map() -> str:
    return """# MQTT Topic Map (tte/)

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
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="deliverables/cycle-01/generated")
    ap.add_argument("--id-step-lat", type=float, default=0.0001)
    ap.add_argument("--id-step-lon", type=float, default=0.0001)
    args = ap.parse_args()

    generate_outputs(args.out, args.id_step_lat, args.id_step_lon)
    print(f"Wrote outputs to: {args.out}")
