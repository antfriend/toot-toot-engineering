from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Literal


Channel = Literal["primary", "secondary"]


@dataclass(frozen=True)
class NormalizedPacket:
    """A normalized representation of an inbound message from any transport.

    Matches the prompt's requested JSON shape, but in Python.
    """

    from_id: str
    to_id: str
    channel: str
    text: str
    ts: str  # ISO-8601 string

    rssi: Optional[int] = None
    snr: Optional[float] = None
    hop_count: Optional[int] = None

    location: Optional[Dict[str, Any]] = None  # {lat, lon, alt}
    device_id: Optional[str] = None

    transport: str = "simulated"  # e.g., meshtastic_serial|meshtastic_tcp|ip_http|simulated

