"""bbs/transport_tcp.py

Raw TCP transport adapter.

Responsibilities:
- create listening socket
- accept connections
- provide a small conn wrapper implementing send/recv/close
- read lines with minimal buffering

MVP implementation is single-connection-at-a-time friendly, but can be extended.
"""

import socket
import time

from . import config


class TCPConn:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.sock.settimeout(0.5)
        self._rx = b""

    def send(self, data):
        if not data:
            return
        # best-effort sendall
        try:
            self.sock.sendall(data)
        except OSError:
            # client likely gone
            raise

    def recv(self, max_bytes=256):
        return self.sock.recv(max_bytes)

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass

    def readline(self, max_bytes=config.MAX_LINE_BYTES):
        """Read until '\n' (accepts either \n or \r\n), return decoded ASCII line (no newline).

        Returns None on timeout/no data yet.
        Raises on disconnect.
        """
        # Fill buffer
        while b"\n" not in self._rx:
            try:
                chunk = self.recv(64)
            except OSError:
                return None
            if not chunk:
                raise OSError("disconnect")
            self._rx += chunk
            if len(self._rx) > max_bytes:
                # too long; cut
                line = self._rx[:max_bytes]
                self._rx = b""
                return line.decode("ascii", "ignore").replace("\r", "")
        line, rest = self._rx.split(b"\n", 1)
        self._rx = rest
        return line.decode("ascii", "ignore").replace("\r", "")


def make_server(host=config.TCP_HOST, port=config.TCP_PORT, backlog=2):
    s = socket.socket()
    ai = socket.getaddrinfo(host, port)[0][-1]
    s.bind(ai)
    s.listen(backlog)
    return s


def serve_forever(server_sock, on_connect, log=None):
    """Accept loop. Calls on_connect(TCPConn) for each new connection."""
    while True:
        try:
            client_sock, addr = server_sock.accept()
        except OSError:
            time.sleep(0.1)
            continue
        conn = TCPConn(client_sock, addr)
        if log:
            log("CONNECT %s" % (addr,))
        try:
            on_connect(conn)
        except Exception as e:
            if log:
                log("SESSION ERROR %s" % (e,))
        try:
            conn.close()
        except Exception:
            pass
        if log:
            log("DISCONNECT %s" % (addr,))
