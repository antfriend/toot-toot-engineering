from __future__ import annotations

import argparse
from typing import Optional

from .config import NodeConfig
from .message import TTNMessage
from .transport_udp import UDPTransport


def run_listener(config_path: str) -> None:
    cfg = NodeConfig.load(config_path)

    # For simplest behavior, listen on BOTH the node port and the group port
    # (these may be the same).
    sock_node = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port).open_socket()
    sock_group = sock_node
    if cfg.group_port != cfg.node_port:
        sock_group = UDPTransport(cfg.group_port, cfg.group_ip, cfg.group_port).open_socket()

    print(
        f"[{cfg.node_name}] listening on UDP ports: {sorted({cfg.node_port, cfg.group_port})} "
        f"(group {cfg.group_ip}:{cfg.group_port})"
    )
    if cfg.peers:
        print(f"[{cfg.node_name}] peers: {', '.join([f'{k}@{v}' for k, v in cfg.peers.items()])}")

    # Simple two-socket polling without extra deps.
    socks = [sock_node] if sock_group is sock_node else [sock_node, sock_group]

    import select

    while True:
        readable, _, _ = select.select(socks, [], [])
        for s in readable:
            data, (src_ip, src_port) = s.recvfrom(65535)
            try:
                msg = TTNMessage.from_json_bytes(data)
                print(
                    f"[{cfg.node_name}] RX from {msg.from_name}@{msg.from_ip} "
                    f"src={src_ip}:{src_port} to={msg.to} id={msg.msg_id}: {msg.text}"
                )
            except Exception as e:
                print(f"[{cfg.node_name}] RX malformed from {src_ip}:{src_port}: {e}")


def send_direct(config_path: str, to_name: str, text: str) -> None:
    cfg = NodeConfig.load(config_path)
    t = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port)

    to_ip, to_port = cfg.resolve_peer(to_name)
    msg = TTNMessage.new(cfg.node_name, cfg.node_ip, to_name, text)
    t.send_unicast(msg.to_json_bytes(), to_ip, to_port)
    print(f"[{cfg.node_name}] TX direct to {to_name}@{to_ip}:{to_port} id={msg.msg_id}: {text}")


def send_broadcast(config_path: str, text: str) -> None:
    cfg = NodeConfig.load(config_path)
    t = UDPTransport(cfg.node_port, cfg.group_ip, cfg.group_port)

    msg = TTNMessage.new(cfg.node_name, cfg.node_ip, "broadcast", text)

    # Try multicast group send first.
    try:
        t.send_group(msg.to_json_bytes())
        print(
            f"[{cfg.node_name}] TX broadcast (multicast) to {cfg.group_ip}:{cfg.group_port} "
            f"id={msg.msg_id}: {text}"
        )
        return
    except OSError:
        pass

    # Fallback: fan-out to peers (still UDP).
    if not cfg.peers:
        raise RuntimeError("Broadcast failed (multicast unavailable) and NODE_PEERS is empty for fallback.")
    for _name, ip in cfg.peers.items():
        t.send_unicast(msg.to_json_bytes(), ip, cfg.node_port)
    print(f"[{cfg.node_name}] TX broadcast (peer fanout) to {len(cfg.peers)} peers id={msg.msg_id}: {text}")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(prog="ttn-node", description="Minimal TTN node over UDP")
    p.add_argument("--config", required=True, help="Path to node .env config file")

    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("listen", help="Start node listener")

    sp_direct = sub.add_parser("direct", help="Send direct message")
    sp_direct.add_argument("to_name")
    sp_direct.add_argument("text")

    sp_bcast = sub.add_parser("broadcast", help="Send group/broadcast message")
    sp_bcast.add_argument("text")

    args = p.parse_args(argv)

    if args.cmd == "listen":
        run_listener(args.config)
        return 0
    if args.cmd == "direct":
        send_direct(args.config, args.to_name, args.text)
        return 0
    if args.cmd == "broadcast":
        send_broadcast(args.config, args.text)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
