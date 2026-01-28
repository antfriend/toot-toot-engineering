from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Iterable, List, Dict, Any

from semantic.types import SemanticEvent


EDGE_GLOSSARY = {
    "announces_presence": "Node announces it is online/present.",
    "reports_sensor": "Node reports a sensor reading.",
    "addresses": "A message is addressed to a specific node/service.",
    "responds_to": "This event is a response/reply to another event/thread reference.",
}


def render_ttdb(
    events: List[SemanticEvent],
    id_step_lat: float,
    id_step_lon: float,
    cursor_event_id: str | None = None,
) -> str:
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    cursor_event_id = cursor_event_id or (events[-1].event_id if events else "")

    # Collect nodes for umwelt
    nodes = sorted({ev.reported_by for ev in events})

    lines: List[str] = []
    lines.append("# MyMentalPalaceDB")
    lines.append("")
    lines.append("## Settings")
    lines.append(f"- Generated: {now}")
    lines.append(f"- ID_STEP_LAT: {id_step_lat}")
    lines.append(f"- ID_STEP_LON: {id_step_lon}")
    lines.append("- Collision rule: if event_id exists, move South-East by one step until unique")
    lines.append("")

    lines.append("## Cursor")
    lines.append(f"- current_event_id: {cursor_event_id}")
    lines.append("")

    lines.append("## Umwelt")
    lines.append("Librarian perspective: I observe typed events on the MQTT bus and preserve them as a navigable graph.")
    lines.append("Globe mapping: event_id is represented as a lat,lon-like coordinate; nearby points are conceptually related by time/story trails.")
    lines.append(f"Observed nodes: {', '.join(nodes) if nodes else '(none)'}")
    lines.append("")

    lines.append("## Typed edges glossary")
    for k, v in EDGE_GLOSSARY.items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("## Records")
    for ev in events:
        lines.append("")
        lines.append(f"### Event {ev.event_id}")
        lines.append(f"- ts: {ev.ts}")
        lines.append(f"- event_type: {ev.event_type}")
        lines.append(f"- intent: {ev.intent}")
        lines.append(f"- confidence: {ev.confidence}")
        lines.append(f"- reported_by: {ev.reported_by}")
        lines.append(f"- addressed_to: {ev.addressed_to}")
        lines.append(f"- raw_ref: {ev.raw_ref}")

        if ev.payload:
            lines.append(f"- payload: `{ev.payload}`")

        if ev.entities:
            ents = ", ".join([f"{e.type}:{e.id}" for e in ev.entities])
            lines.append(f"- entities: {ents}")

        if ev.edges:
            lines.append("- edges:")
            for ed in ev.edges:
                lines.append(f"  - {ed.edge_type}: {ed.source} -> {ed.target}")

        # mesh meta
        mm = {k: v for k, v in ev.mesh_meta.items() if v is not None}
        if mm:
            lines.append(f"- mesh_meta: `{mm}`")

    lines.append("")
    return "\n".join(lines)

