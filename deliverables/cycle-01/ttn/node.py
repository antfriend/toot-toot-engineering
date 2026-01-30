from __future__ import annotations

import socket
import threading
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from .config import NodeConfig
from .message import TTNMessage, parse_message


def _make_udp_socket() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s


@dataclass
class Received:
    msg: TTNMessage
    addr: Tuple[str, int]


class TTNNode:
    """Single-socket UDP node.

    Design choice for simplicity/reliability:
    - Use ONE UDP port for both direct and group messages.
    - Therefore GROUP_PORT == NODE_PORT (enforced by config loader).
    """

    def __init__(self, cfg: NodeConfig, *, on_receive: Optional[Callable[[Received], None]] = None):
        self.cfg = cfg
        self.on_receive = on_receive

        self._sock = _make_udp_socket()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        # Bind to node listen address
        self._sock.bind((self.cfg.node_ip, self.cfg.node_port))

        # Join multicast group if configured
        if self.cfg.group_mode == "multicast":
            # IP_ADD_MEMBERSHIP expects packed group addr + interface addr
            mreq = socket.inet_aton(self.cfg.group_ip) + socket.inet_aton(self.cfg.node_ip)
            self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # Allow broadcast sends when group_mode=broadcast
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self._thread = threading.Thread(target=self._recv_loop, name=f"ttn-recv-{self.cfg.node_name}", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        try:
            self._sock.close()
        except OSError:
            pass

    def send_direct(self, *, to_name: str, text: str) -> None:
        if to_name not in self.cfg.node_peers:
            raise KeyError(f"Unknown peer name: {to_name}. Known: {list(self.cfg.node_peers)}")
        to_ip = self.cfg.node_peers[to_name]
        msg = TTNMessage.new(from_name=self.cfg.node_name, from_ip=self.cfg.node_ip, to=to_name, text=text)
        self._sock.sendto(msg.to_json().encode("utf-8"), (to_ip, self.cfg.node_port))

    def send_group(self, *, text: str) -> None:
        msg = TTNMessage.new(
            from_name=self.cfg.node_name,
            from_ip=self.cfg.node_ip,
            to="broadcast",
            text=text,
        )
        self._sock.sendto(msg.to_json().encode("utf-8"), (self.cfg.group_ip, self.cfg.group_port))

    def announce_presence(self) -> None:
        msg = TTNMessage.new(
            from_name=self.cfg.node_name,
            from_ip=self.cfg.node_ip,
            to="broadcast",
            text=f"{self.cfg.node_name} is online",
            msg_type="presence",
        )
        self._sock.sendto(msg.to_json().encode("utf-8"), (self.cfg.group_ip, self.cfg.group_port))

    def _recv_loop(self) -> None:
        while not self._stop.is_set():
            try:
                data, addr = self._sock.recvfrom(65535)
            except OSError:
                break

            try:
                payload = data.decode("utf-8", errors="replace")
                msg = parse_message(payload)
            except Exception:
                # ignore malformed payloads
                continue

            # Delivery rule:
            # - Always accept group messages (to="broadcast")
            # - Accept direct messages addressed to this node by name
            if msg.to != "broadcast" and msg.to != self.cfg.node_name:
                continue

            if self.on_receive:
                self.on_receive(Received(msg=msg, addr=addr))
