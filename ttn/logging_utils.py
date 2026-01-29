from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict

_LEVELS: Dict[str, int] = {
    "debug": 10,
    "info": 20,
    "warning": 30,
    "error": 40,
}


def _level_value(level: str) -> int:
    return _LEVELS.get(level.lower(), 20)


def _ts_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class Logger:
    level: str = "info"
    fmt: str = "text"

    def log(self, level: str, event: str, **fields: object) -> None:
        if _level_value(level) < _level_value(self.level):
            return
        record = {"ts": _ts_utc(), "level": level.lower(), "event": event}
        record.update(fields)
        if self.fmt == "json":
            print(json.dumps(record, ensure_ascii=False), flush=True)
            return

        # Text format: [LEVEL] event key=value ...
        extras = " ".join(f"{k}={v}" for k, v in record.items() if k not in {"ts", "level", "event"})
        if extras:
            print(f"[{record['level'].upper()}] {record['event']} {extras}", flush=True)
        else:
            print(f"[{record['level'].upper()}] {record['event']}", flush=True)

    def debug(self, event: str, **fields: object) -> None:
        self.log("debug", event, **fields)

    def info(self, event: str, **fields: object) -> None:
        self.log("info", event, **fields)

    def warning(self, event: str, **fields: object) -> None:
        self.log("warning", event, **fields)

    def error(self, event: str, **fields: object) -> None:
        self.log("error", event, **fields)
