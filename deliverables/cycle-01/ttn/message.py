from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional

ToField = str  # peer node name or "broadcast"


def now_iso_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class TTNMessage:
    """Minimal TTN JSON message.

    Matches the prompt's required fields, with one additional optional field:
    - msg_type: "chat" | "presence" (optional)

    The optional field keeps backwards compatibility for consumers that ignore
    unknown fields.
    """

    msg_id: str
    from_name: str
    from_ip: str
    to: ToField
    ts: str
    text: str

    msg_type: Optional[Literal["chat", "presence"]] = None

    @staticmethod
    def new(
        *,
        from_name: str,
        from_ip: str,
        to: ToField,
        text: str,
        msg_type: Optional[Literal["chat", "presence"]] = None,
    ) -> "TTNMessage":
        return TTNMessage(
            msg_id=str(uuid.uuid4()),
            from_name=from_name,
            from_ip=from_ip,
            to=to,
            ts=now_iso_z(),
            text=text,
            msg_type=msg_type,
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # remove null optional fields to keep messages minimal
        if d.get("msg_type") is None:
            d.pop("msg_type", None)
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def parse_message(payload: str) -> TTNMessage:
    d: Dict[str, Any] = json.loads(payload)
    required = ["msg_id", "from_name", "from_ip", "to", "ts", "text"]
    missing = [k for k in required if k not in d]
    if missing:
        raise ValueError(f"Invalid message; missing keys: {missing}")

    msg_type = d.get("msg_type")
    if msg_type is not None and msg_type not in ("chat", "presence"):
        raise ValueError("msg_type must be 'chat' or 'presence' when provided")

    return TTNMessage(
        msg_id=str(d["msg_id"]),
        from_name=str(d["from_name"]),
        from_ip=str(d["from_ip"]),
        to=str(d["to"]),
        ts=str(d["ts"]),
        text=str(d["text"]),
        msg_type=msg_type,
    )
