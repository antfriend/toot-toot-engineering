from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Callable, Set, Tuple

from receiver.types import NormalizedPacket
from semantic.types import SemanticEvent


def raw_ref_sha256(pkt: NormalizedPacket) -> str:
    h = hashlib.sha256()
    h.update((pkt.ts + "|" + pkt.from_id + "|" + pkt.to_id + "|" + pkt.text).encode("utf-8"))
    return "raw:sha256:" + h.hexdigest()


def assign_event_id(
    pkt: NormalizedPacket,
    ev: SemanticEvent,
    existing_ids: Set[str],
    id_step_lat: float = 0.0001,
    id_step_lon: float = 0.0001,
    base_latlon: Tuple[float, float] = (44.0, -116.0),
) -> str:
    """Assign a stable event_id.

    Prompt suggests lat/lon-like IDs with collision avoidance moving South-East.
    In this implementation, we derive a deterministic pseudo-lat/lon around a base,
    then apply the collision rule.
    """

    # deterministic offset from content
    seed = hashlib.sha256((ev.intent + "|" + pkt.from_id + "|" + pkt.ts).encode("utf-8")).digest()
    # map first bytes into small offsets (0..999) steps
    off_a = int.from_bytes(seed[0:2], "big") % 1000
    off_b = int.from_bytes(seed[2:4], "big") % 1000

    lat = base_latlon[0] + off_a * id_step_lat
    lon = base_latlon[1] + off_b * id_step_lon

    def fmt(lat_: float, lon_: float) -> str:
        return f"{lat_:.4f},{lon_:.4f}"

    candidate = fmt(lat, lon)
    while candidate in existing_ids:
        lat -= id_step_lat  # South
        lon += id_step_lon  # East
        candidate = fmt(lat, lon)

    return candidate

