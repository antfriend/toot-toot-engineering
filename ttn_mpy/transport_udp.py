try:
    import usocket as socket
except ImportError:  # pragma: no cover - CPython fallback
    import socket

try:
    import ustruct as struct
except ImportError:  # pragma: no cover - CPython fallback
    import struct


class UDPTransport:
    def __init__(self, listen_port, group_ip, group_port):
        self.listen_port = listen_port
        self.group_ip = group_ip
        self.group_port = group_port

    def open_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception:
            pass
        sock.bind(("", self.listen_port))
        try:
            mreq = struct.pack("4sl", socket.inet_aton(self.group_ip), socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            return sock, True
        except Exception:
            return sock, False

    def send_unicast(self, data, to_ip, to_port=None):
        port = self.listen_port if to_port is None else to_port
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.sendto(data, (to_ip, port))
        finally:
            try:
                s.close()
            except Exception:
                pass

    def send_group(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        except Exception:
            pass
        try:
            s.sendto(data, (self.group_ip, self.group_port))
        finally:
            try:
                s.close()
            except Exception:
                pass
