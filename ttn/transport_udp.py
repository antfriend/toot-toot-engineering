from __future__ import annotations

import socket
import struct
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class UDPTransport:
    listen_port: int
    group_ip: str
    group_port: int

    def open_socket(self) -> socket.socket:
        """Open a UDP socket bound to listen_port and (best-effort) joined to group_ip."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to all interfaces for receiving.
        sock.bind(("", self.listen_port))

        # Join multicast group for group receive.
        try:
            mreq = struct.pack("4sl", socket.inet_aton(self.group_ip), socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except OSError:
            # Some environments may not support multicast; node can still do direct.
            pass

        return sock

    def send_unicast(self, data: bytes, to_ip: str, to_port: Optional[int] = None) -> None:
        port = self.listen_port if to_port is None else to_port
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
            s.sendto(data, (to_ip, port))

    def send_group(self, data: bytes) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as s:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            s.sendto(data, (self.group_ip, self.group_port))

    def recv(self, sock: socket.socket, bufsize: int = 65535) -> Tuple[bytes, Tuple[str, int]]:
        return sock.recvfrom(bufsize)
