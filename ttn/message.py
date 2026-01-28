from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import uuid


@dataclass(frozen=True)
class TTNMessage:
    msg_id: str
    from_name: str
    from_ip: str
    to: str  # node-name or "broadcast"
    ts: str  # ISO-8601 UTC (Z)
    text: str

    @staticmethod
    def new(from_name: str, from_ip: str, to: str, text: str) -> "TTNMessage":
        ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        return TTNMessage(
            msg_id=str(uuid.uuid4()),
            from_name=from_name,
            from_ip=from_ip,
            to=to,
            ts=ts,
            text=text,
        )

    def to_json_bytes(self) -> bytes:
        return json.dumps(asdict(self), ensure_ascii=False).encode("utf-8")

    @staticmethod
    def from_json_bytes(data: bytes) -> "TTNMessage":
        obj = json.loads(data.decode("utf-8"))
        # minimal validation
        required = {"msg_id", "from_name", "from_ip", "to", "ts", "text"}
        missing = required - set(obj.keys())
        if missing:
            raise ValueError(f"Missing fields: {sorted(missing)}")
        return TTNMessage(
            msg_id=str(obj["msg_id"]),
            from_name=str(obj["from_name"]),
            from_ip=str(obj["from_ip"]),
            to=str(obj["to"]),
            ts=str(obj["ts"]),
            text=str(obj["text"]),
        )
