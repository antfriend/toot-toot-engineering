from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from typing import Dict, Optional

from .config import NodeConfig
from .logging_utils import Logger
from .message import TTNMessage
from .transport_udp import UDPTransport


def _write_export(path: str, msg: TTNMessage, src: str) -> None:
    record = asdict(msg)
    record["src"] = src
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_monitor(
    config_path: str,
    logger: Logger,
    summary_seconds: int = 5,
    export_path: Optional[str] = None,
) -> None:
    cfg = NodeConfig.load(config_path)
    sock, multicast_ok = UDPTransport(cfg.group_port, cfg.group_ip, cfg.group_port).open_socket()

    logger.info(
        "monitor_start",
        node=cfg.node_name,
        group=f"{cfg.group_ip}:{cfg.group_port}",
        multicast_joined=bool(multicast_ok),
        summary_seconds=summary_seconds,
        export_path=export_path or "",
    )

    stats: Dict[str, Dict[str, object]] = {}
    last_summary = time.time()

    while True:
        data, (src_ip, src_port) = sock.recvfrom(65535)
        src = f"{src_ip}:{src_port}"
        try:
            msg = TTNMessage.from_json_bytes(data)
            info = stats.setdefault(msg.from_name, {"count": 0, "last_seen": ""})
            info["count"] = int(info["count"]) + 1
            info["last_seen"] = msg.ts

            logger.info(
                "monitor_rx",
                from_name=msg.from_name,
                to=msg.to,
                msg_id=msg.msg_id,
                text=msg.text,
                src=src,
            )
            if export_path:
                _write_export(export_path, msg, src)
        except Exception as e:
            logger.warning("monitor_malformed", src=src, error=str(e))

        now = time.time()
        if summary_seconds > 0 and (now - last_summary) >= summary_seconds:
            last_summary = now
            summary = ",".join(
                [f"{name}:{data['count']} last={data['last_seen']}" for name, data in stats.items()]
            )
            logger.info("monitor_summary", nodes=summary)


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="ttn-monitor", description="TTN multicast monitor")
    p.add_argument("--config", required=True, help="Path to node .env config file")
    p.add_argument(
        "--log-format",
        default="text",
        choices=["text", "json"],
        help="Log output format",
    )
    p.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error"],
        help="Minimum log level",
    )
    p.add_argument(
        "--summary-seconds",
        type=int,
        default=5,
        help="Emit a periodic summary every N seconds (0 disables)",
    )
    p.add_argument("--export", default="", help="Append JSON lines to this file")
    args = p.parse_args(argv)

    logger = Logger(level=args.log_level, fmt=args.log_format)
    run_monitor(args.config, logger, summary_seconds=args.summary_seconds, export_path=args.export or None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
