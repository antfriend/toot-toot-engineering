from __future__ import annotations

import argparse
import time

from .config import load_config
from .node import TTNNode


def main() -> int:
    ap = argparse.ArgumentParser(description="TTN UDP node (direct + group messaging)")
    ap.add_argument("--config", required=True, help="Path to node JSON config")

    sub = ap.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run a node and print received messages")
    run.add_argument("--presence", action="store_true", help="Announce presence on startup")

    send = sub.add_parser("send", help="Send a single message")
    send.add_argument("--to", required=True, help="Peer node name, or 'broadcast'")
    send.add_argument("--text", required=True, help="Message text")

    args = ap.parse_args()
    cfg = load_config(args.config)

    def on_rx(rec):
        m = rec.msg
        print(f"[{cfg.node_name}] RX from={m.from_name} to={m.to} ts={m.ts} text={m.text}")

    node = TTNNode(cfg, on_receive=on_rx)
    node.start()

    if args.cmd == "run":
        if args.presence:
            node.announce_presence()
        print(f"[{cfg.node_name}] listening on {cfg.node_ip}:{cfg.node_port} (group {cfg.group_mode} {cfg.group_ip}:{cfg.group_port})")
        try:
            while True:
                time.sleep(0.25)
        except KeyboardInterrupt:
            return 0
        finally:
            node.stop()

    if args.cmd == "send":
        if args.to == "broadcast":
            node.send_group(text=args.text)
        else:
            node.send_direct(to_name=args.to, text=args.text)
        # give the socket a moment to flush
        time.sleep(0.1)
        node.stop()
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
