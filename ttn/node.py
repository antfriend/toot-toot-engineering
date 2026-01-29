from __future__ import annotations

import argparse
from typing import Optional

from .config import NodeConfig
from .logging_utils import Logger
from .message import TTNMessage
from .monitor import run_monitor
from .transport_udp import UDPTransport


def run_listener(config_path: str, logger: Logger) -> None:
    cfg = NodeConfig.load(config_path)

    # For simplest behavior, listen on BOTH the node port and the group port
    # (these may be the same).
    sock_node, node_multicast = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port).open_socket()
    sock_group = sock_node
    group_multicast = node_multicast
    if cfg.group_port != cfg.node_port:
        sock_group, group_multicast = UDPTransport(cfg.group_port, cfg.group_ip, cfg.group_port).open_socket()

    logger.info(
        "listener_start",
        node=cfg.node_name,
        ports=sorted({cfg.node_port, cfg.group_port}),
        group_ip=cfg.group_ip,
        group_port=cfg.group_port,
        multicast_joined=bool(group_multicast),
    )
    if cfg.peers:
        logger.info(
            "peers_loaded",
            node=cfg.node_name,
            peers=",".join([f"{k}@{v}" for k, v in cfg.peers.items()]),
        )

    # Simple two-socket polling without extra deps.
    socks = [sock_node] if sock_group is sock_node else [sock_node, sock_group]

    import select

    while True:
        readable, _, _ = select.select(socks, [], [])
        for s in readable:
            data, (src_ip, src_port) = s.recvfrom(65535)
            try:
                msg = TTNMessage.from_json_bytes(data)
                logger.info(
                    "rx_message",
                    node=cfg.node_name,
                    from_name=msg.from_name,
                    from_ip=msg.from_ip,
                    src=f"{src_ip}:{src_port}",
                    to=msg.to,
                    msg_id=msg.msg_id,
                    text=msg.text,
                )
            except Exception as e:
                logger.warning(
                    "rx_malformed",
                    node=cfg.node_name,
                    src=f"{src_ip}:{src_port}",
                    error=str(e),
                )


def send_direct(config_path: str, to_name: str, text: str, logger: Logger) -> None:
    cfg = NodeConfig.load(config_path)
    t = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port)

    to_ip, to_port = cfg.resolve_peer(to_name)
    msg = TTNMessage.new(cfg.node_name, cfg.node_ip, to_name, text)
    t.send_unicast(msg.to_json_bytes(), to_ip, to_port)
    logger.info(
        "tx_direct",
        node=cfg.node_name,
        to_name=to_name,
        to=f"{to_ip}:{to_port}",
        msg_id=msg.msg_id,
        text=text,
    )


def send_broadcast(config_path: str, text: str, logger: Logger) -> None:
    cfg = NodeConfig.load(config_path)
    t = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port)

    msg = TTNMessage.new(cfg.node_name, cfg.node_ip, "broadcast", text)

    # Try multicast group send first.
    try:
        t.send_group(msg.to_json_bytes())
        logger.info(
            "tx_broadcast",
            node=cfg.node_name,
            mode="multicast",
            group=f"{cfg.group_ip}:{cfg.group_port}",
            msg_id=msg.msg_id,
            text=text,
        )
        return
    except OSError as e:
        logger.warning(
            "multicast_failed",
            node=cfg.node_name,
            group=f"{cfg.group_ip}:{cfg.group_port}",
            error=str(e),
        )

    # Fallback: fan-out to peers (still UDP).
    if not cfg.peers:
        logger.error(
            "broadcast_failed_no_peers",
            node=cfg.node_name,
            msg_id=msg.msg_id,
        )
        raise RuntimeError("Broadcast failed (multicast unavailable) and NODE_PEERS is empty for fallback.")
    for _name, ip in cfg.peers.items():
        t.send_unicast(msg.to_json_bytes(), ip, cfg.node_port)
    logger.info(
        "tx_broadcast",
        node=cfg.node_name,
        mode="peer_fanout",
        peers=len(cfg.peers),
        msg_id=msg.msg_id,
        text=text,
    )


def show_info(config_path: str, logger: Logger) -> None:
    cfg = NodeConfig.load(config_path)
    logger.info(
        "config_info",
        node=cfg.node_name,
        node_ip=cfg.node_ip,
        node_port=cfg.node_port,
        group_ip=cfg.group_ip,
        group_port=cfg.group_port,
        peers=",".join([f"{k}@{v}" for k, v in cfg.peers.items()]) if cfg.peers else "",
    )


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="ttn-node", description="Minimal TTN node over UDP")
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

    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("listen", help="Start node listener")
    sub.add_parser("info", help="Print parsed config info")

    sp_direct = sub.add_parser("direct", help="Send direct message")
    sp_direct.add_argument("to_name")
    sp_direct.add_argument("text")

    sp_bcast = sub.add_parser("broadcast", help="Send group/broadcast message")
    sp_bcast.add_argument("text")

    sp_monitor = sub.add_parser("monitor", help="Monitor group traffic")
    sp_monitor.add_argument(
        "--summary-seconds",
        type=int,
        default=5,
        help="Emit a periodic summary every N seconds (0 disables)",
    )
    sp_monitor.add_argument("--export", default="", help="Append JSON lines to this file")

    args = p.parse_args(argv)
    logger = Logger(level=args.log_level, fmt=args.log_format)

    if args.cmd == "listen":
        run_listener(args.config, logger)
        return 0
    if args.cmd == "info":
        show_info(args.config, logger)
        return 0
    if args.cmd == "direct":
        send_direct(args.config, args.to_name, args.text, logger)
        return 0
    if args.cmd == "broadcast":
        send_broadcast(args.config, args.text, logger)
        return 0
    if args.cmd == "monitor":
        run_monitor(
            args.config,
            logger,
            summary_seconds=args.summary_seconds,
            export_path=args.export or None,
        )
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
