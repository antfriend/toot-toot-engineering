# transport_tcp.py - raw TCP transport adapter

import time


class TcpTransport:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.sock.settimeout(0.2)

    def send(self, data):
        if isinstance(data, str):
            data = data.encode("ascii", "ignore")
        try:
            self.sock.send(data)
        except Exception:
            # ignore send failures; upper layers will close
            pass

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def recv_line(self, max_bytes=120, timeout_s=30):
        # Read until '\n' or max_bytes. Returns decoded ASCII without CRLF.
        start = time.time()
        buf = b""
        while True:
            if time.time() - start > timeout_s:
                return None
            try:
                b = self.sock.recv(1)
                if not b:
                    return None
                if b == b"\n":
                    # strip optional '\r'
                    if buf.endswith(b"\r"):
                        buf = buf[:-1]
                    return buf.decode("ascii", "ignore")
                buf += b
                if len(buf) >= max_bytes:
                    # truncate line
                    return buf.decode("ascii", "ignore")
            except Exception:
                # timeout or EAGAIN
                time.sleep(0.01)

    def recv_exact(self, nbytes, timeout_s=20):
        start = time.time()
        buf = b""
        while len(buf) < nbytes:
            if time.time() - start > timeout_s:
                return None
            try:
                chunk = self.sock.recv(nbytes - len(buf))
                if not chunk:
                    return None
                buf += chunk
            except Exception:
                time.sleep(0.01)
        return buf
