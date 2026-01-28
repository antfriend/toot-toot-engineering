from __future__ import annotations

import re
from typing import Dict, Tuple

from receiver.types import NormalizedPacket
from semantic.types import SemanticEdge, SemanticEntity, SemanticEvent


TEMP_RE = re.compile(r"^TEMP\s+(-?\d+(?:\.\d+)?)\s*$", re.IGNORECASE)
PING_RE = re.compile(r"^PING\s*$", re.IGNORECASE)
STATUS_RE = re.compile(r"^STATUS\?\s*$", re.IGNORECASE)
OK_RE = re.compile(r"^OK\s*$", re.IGNORECASE)
HELP_MEDICAL_RE = re.compile(r"^HELP\s+MEDICAL\s*$", re.IGNORECASE)
DIRECTED_RE = re.compile(r"^@(?P<node>[a-zA-Z0-9:_-]+)\s+(?P<cmd>.+)$")
BROADCAST_RE = re.compile(r"^#broadcast\s+(?P<msg>.+)$", re.IGNORECASE)
REPLY_RE = re.compile(r"^#reply\s+(?P<ref>[^\s]+)\s+(?P<msg>.+)$", re.IGNORECASE)
LOG_REQUEST_RE = re.compile(r"^LOGISTICS\s+REQUEST\s+(?P<msg>.+)$", re.IGNORECASE)
LOG_OFFER_RE = re.compile(r"^LOGISTICS\s+OFFER\s+(?P<msg>.+)$", re.IGNORECASE)


def _base_event(pkt: NormalizedPacket) -> Dict:
    return dict(
        event_id="",  # assigned later
        event_type="",
        intent="",
        confidence=1.0,
        ts=pkt.ts,
        reported_by=pkt.from_id,
        addressed_to=pkt.to_id if pkt.to_id else "broadcast",
        mesh_meta={
            "rssi": pkt.rssi,
            "snr": pkt.snr,
            "hop_count": pkt.hop_count,
            "channel": pkt.channel,
            "transport": pkt.transport,
        },
        raw_ref="",
        entities=[],
        payload={},
        edges=[],
        rationale=None,
    )


def interpret_packet(pkt: NormalizedPacket) -> Tuple[SemanticEvent, str]:
    """Deterministically interpret a NormalizedPacket into a SemanticEvent.

    Returns (event, category_topic_suffix) where suffix is used to map to MQTT topics.
    """

    text = (pkt.text or "").strip()

    # Presence
    if PING_RE.match(text):
        base = _base_event(pkt)
        base.update(
            event_type="presence",
            intent="presence_probe",
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            edges=[SemanticEdge(edge_type="announces_presence", source=pkt.from_id, target=pkt.from_id)],
            payload={"text": text},
        )
        return SemanticEvent(**base), "presence"

    # Status request
    if STATUS_RE.match(text):
        base = _base_event(pkt)
        base.update(
            event_type="status",
            intent="status_request",
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            payload={"text": text},
        )
        return SemanticEvent(**base), "status/request"

    # Acknowledgement
    if OK_RE.match(text):
        base = _base_event(pkt)
        base.update(
            event_type="ack",
            intent="acknowledgement",
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            payload={"text": text},
        )
        return SemanticEvent(**base), "ack"

    # Temperature
    m = TEMP_RE.match(text)
    if m:
        val = float(m.group(1))
        sensor_id = "sensor:temp"
        base = _base_event(pkt)
        base.update(
            event_type="sensor",
            intent="sensor_reading.temperature",
            entities=[
                SemanticEntity(type="node", id=pkt.from_id),
                SemanticEntity(type="sensor", id=sensor_id),
            ],
            edges=[SemanticEdge(edge_type="reports_sensor", source=pkt.from_id, target=sensor_id)],
            payload={"value": val, "unit": "C"},
        )
        return SemanticEvent(**base), "sensor/temperature"

    # Emergency medical
    if HELP_MEDICAL_RE.match(text):
        base = _base_event(pkt)
        base.update(
            event_type="emergency",
            intent="emergency_medical",
            confidence=0.98,
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            payload={"text": text},
        )
        return SemanticEvent(**base), "emergency/medical"

    # Directed command
    m = DIRECTED_RE.match(text)
    if m:
        node = m.group("node")
        cmd = m.group("cmd").strip()
        target = f"node:{node}" if not node.startswith("node:") else node
        base = _base_event(pkt)
        base.update(
            event_type="command",
            intent="directed_command",
            entities=[
                SemanticEntity(type="node", id=pkt.from_id),
                SemanticEntity(type="node", id=target),
            ],
            edges=[SemanticEdge(edge_type="addresses", source=pkt.from_id, target=target)],
            payload={"command": cmd, "target": target},
        )
        return SemanticEvent(**base), "command/directed"

    # Bulletin post
    m = BROADCAST_RE.match(text)
    if m:
        msg = m.group("msg").strip()
        base = _base_event(pkt)
        base.update(
            event_type="bulletin",
            intent="bulletin_post",
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            payload={"message": msg},
        )
        return SemanticEvent(**base), "bulletin/post"

    # Bulletin reply
    m = REPLY_RE.match(text)
    if m:
        ref = m.group("ref").strip()
        msg = m.group("msg").strip()
        base = _base_event(pkt)
        base.update(
            event_type="bulletin",
            intent="bulletin_reply",
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            edges=[SemanticEdge(edge_type="responds_to", source="", target=ref)],
            payload={"message": msg, "in_reply_to": ref},
        )
        return SemanticEvent(**base), "bulletin/reply"

    # Logistics
    m = LOG_REQUEST_RE.match(text)
    if m:
        msg = m.group("msg").strip()
        base = _base_event(pkt)
        base.update(
            event_type="logistics",
            intent="logistics_request",
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            payload={"request": msg},
        )
        return SemanticEvent(**base), "logistics/request"

    m = LOG_OFFER_RE.match(text)
    if m:
        msg = m.group("msg").strip()
        base = _base_event(pkt)
        base.update(
            event_type="logistics",
            intent="logistics_offer",
            entities=[SemanticEntity(type="node", id=pkt.from_id)],
            payload={"offer": msg},
        )
        return SemanticEvent(**base), "logistics/offer"

    # Fallback: unclassified
    base = _base_event(pkt)
    base.update(
        event_type="unclassified",
        intent="unclassified",
        confidence=0.5,
        entities=[SemanticEntity(type="node", id=pkt.from_id)],
        payload={"text": text},
    )
    return SemanticEvent(**base), "unclassified"
