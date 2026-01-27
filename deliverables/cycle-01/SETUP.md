# SETUP (cycle-01)

This document explains how to get the UNIHIKER K10 ready to run the MicroPython TCP BBS.

## 1) Install / verify MicroPython on UNIHIKER K10
Because K10 firmware + tooling can vary by shipping batch, follow the official UNIHIKER documentation for your exact device to:
- flash/enable MicroPython
- confirm you can run a simple `print('hello')`

Minimum requirement: you can copy `.py` files onto the device and run `main.py`.

## 2) Copy the project files to the K10
Copy the `bbs/` directory to the device filesystem so that you have:

```
/bbs/main.py
/bbs/config.py
/bbs/transport_tcp.py
/bbs/session.py
/bbs/protocol.py
/bbs/screens.py
/bbs/storage.py
/bbs/mpdb_lite.py
```

Also copy a starter database file (example):

```
/bbs_data/mpdb_lite.mmpdb
```

(Exact base path may differ; see `bbs/config.py`.)

Tools you can use (depending on your environment):
- the UNIHIKER file manager
- an IDE integration
- `ampy`, `rshell`, or similar MicroPython file upload tools

## 3) Start the server
On the K10, run:

- `import bbs.main` (if it auto-runs)
- or execute `bbs/main.py` as the entrypoint.

Expected behavior:
- The K10 enables Wi‑Fi Access Point mode (SSID/pass configured in `config.py`).
- The TCP server listens on port (default example `2323`).
- The K10 screen displays a minimal “console log” of connects/disconnects.

## 4) Connect from a client
Join the K10 Wi‑Fi network from your computer/phone.

Then connect to the TCP port using one of:
- **Windows**: PuTTY (Connection type: Raw)
- **macOS/Linux**: `nc <k10_ip> 2323`
- `telnet <k10_ip> 2323` (if available)

Type:
- `HELLO`
- `LOGIN yourhandle`
- `MENU`

## 5) Data persistence
Messages are stored in the mpdb-lite file specified in `config.py`.
- If you reboot the K10, the file remains and messages persist.

## Troubleshooting
- If you connect but see no text: ensure your client sends `\r\n` line endings; try typing `HELLO` then ENTER.
- If Wi‑Fi AP does not appear: confirm MicroPython has `network.WLAN(network.AP_IF)` support on this firmware.
- If you get memory errors: reduce page sizes and message limits in `config.py`.

