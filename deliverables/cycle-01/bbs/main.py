# main.py - boot + Wi-Fi + socket server for Toot-Toot BBS
#
# Notes:
# - UNIHIKER K10 MicroPython APIs may vary; Wi-Fi AP bring-up is best-effort.
# - The BBS engine is kept mostly in protocol.py; TCP is just one transport.

import time

try:
    import usocket as socket
except ImportError:
    import socket

from . import config
from .transport_tcp import TcpTransport
from .session import Session
from . import storage
from . import protocol


def log_local(msg):
    # Minimal logging: print to serial console. On K10 you can redirect to screen.
    try:
        print(msg)
    except Exception:
        pass


def wifi_setup_best_effort():
    # Best-effort Wi-Fi setup. Actual UNIHIKER K10 may use different modules.
    try:
        import network
    except ImportError:
        log_local("WIFI: network module not available")
        return

    if config.WIFI_MODE == "ap":
        try:
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            if config.AP_PASSWORD:
                ap.config(essid=config.AP_SSID, password=config.AP_PASSWORD, channel=config.AP_CHANNEL)
            else:
                ap.config(essid=config.AP_SSID, channel=config.AP_CHANNEL)
            log_local("WIFI: AP %s active=%s" % (config.AP_SSID, ap.active()))
        except Exception as e:
            log_local("WIFI: AP setup failed: %r" % e)


def serve_forever():
    wifi_setup_best_effort()

    nodes = storage.load_db(config.DB_PATH)

    # Ensure there is at least a default 'general' area node.
    if not any((n.get("area_name") == "general" and ("body" not in n)) for n in nodes.values()):
        storage.insert_node(config.DB_PATH, {"id": "@LAT0LON1", "area_name": "general", "relates": []})
        nodes = storage.load_db(config.DB_PATH)

    addr = ("0.0.0.0", config.PORT)
    s = socket.socket()
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception:
        pass
    s.bind(addr)
    s.listen(2)

    log_local("BBS: listening on %s:%d" % addr)

    sid_counter = 1

    while True:
        try:
            client, caddr = s.accept()
        except Exception:
            time.sleep(0.05)
            continue

        log_local("BBS: connect %r" % (caddr,))
        transport = TcpTransport(client, caddr)
        session = Session("S%03d" % sid_counter, transport)
        sid_counter += 1

        try:
            protocol.handle_connect(session, config.DB_PATH)
            while True:
                line = transport.recv_line(max_bytes=config.MAX_LINE_BYTES, timeout_s=config.IDLE_TIMEOUT_S)
                if line is None:
                    break
                protocol.handle_line(session, line, nodes, config.DB_PATH)
        except Exception as e:
            log_local("BBS: session error %r" % e)
        finally:
            transport.close()
            log_local("BBS: disconnect %r" % (caddr,))


def main():
    serve_forever()


if __name__ == "__main__":
    main()
