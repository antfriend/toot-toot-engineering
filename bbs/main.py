"""bbs/main.py

Entry point for UNIHIKER K10 MicroPython TCP BBS.

- Starts Wi-Fi in AP mode.
- Starts raw TCP server.
- Logs basic activity to the device screen/console.

Note: UNIHIKER screen APIs may vary; we keep logging conservative.
"""

import time

from . import config
from .transport_tcp import make_server, serve_forever
from .session import Session
from .protocol import Protocol
from .storage import DB


def log(msg):
    # Minimal logging; on UNIHIKER you may print to console and/or draw to screen.
    try:
        print("[BBS]", msg)
    except Exception:
        pass


def wifi_ap_setup():
    """Best-effort AP setup.

    If network module is not present in your firmware, this will no-op.
    """
    try:
        import network
    except ImportError:
        log("network module not available; skipping AP setup")
        return None

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    # Some firmwares require authmode; keep simple.
    try:
        ap.config(essid=config.AP_SSID, password=config.AP_PASSWORD)
    except Exception:
        try:
            ap.config(essid=config.AP_SSID)
        except Exception:
            pass
    time.sleep(0.5)
    try:
        ip = ap.ifconfig()[0]
        log("AP %s up at %s" % (config.AP_SSID, ip))
    except Exception:
        log("AP up")
    return ap


def run():
    wifi_ap_setup()

    db = DB().load_db()
    proto = Protocol(db)

    server = make_server(config.TCP_HOST, config.TCP_PORT)
    log("LISTEN %s:%d" % (config.TCP_HOST, config.TCP_PORT))

    sid_counter = 0

    def on_connect(conn):
        nonlocal sid_counter
        sid_counter += 1
        session = Session("S%d" % sid_counter, conn)
        # send welcome immediately
        resp = proto.handle_line(session, "HELLO")
        if resp:
            conn.send(resp)

        while True:
            try:
                line = conn.readline()
            except OSError:
                break
            if line is None:
                continue
            session.touch()
            resp = proto.handle_line(session, line)
            if resp:
                try:
                    conn.send(resp)
                except OSError:
                    break
            # Close on BYE
            if line.strip().upper() == "BYE":
                break

    serve_forever(server, on_connect, log=log)


# Auto-run if launched as main script
if __name__ == "__main__":
    run()
