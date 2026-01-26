# SETUP (cycle-01) – UNIHIKER K10 + MicroPython + Toot-Toot BBS

This guide describes a practical, tool-agnostic setup path. UNIHIKER firmware and MicroPython builds vary; if a menu item or module name differs, follow the closest equivalent and keep the file layout the same.

## 1) Files to upload

Upload the entire `deliverables/cycle-01/bbs/` folder to the device, plus the sample database:

- `bbs/` (package)
  - `main.py`
  - `config.py`
  - `transport_tcp.py`
  - `session.py`
  - `protocol.py`
  - `screens.py`
  - `storage.py`
  - `__init__.py`
- `db/mpdb-lite.mmpdb`

On-device, the expected paths are:
- `bbs/main.py`
- `db/mpdb-lite.mmpdb`

## 2) Configure Wi‑Fi mode

Open `bbs/config.py`:
- Default mode is AP:
  - `WIFI_MODE = "ap"`
  - `AP_SSID = "TOOT-TOOT-BBS"`
  - `AP_PASSWORD = ""` (open)
  - Port: `2323`

If your MicroPython build does not support AP mode, switch to station mode later (not implemented here beyond best-effort).

## 3) Run

From the MicroPython REPL (or your device’s run mechanism):

```python
from bbs.main import main
main()
```

You should see a console log similar to:
- `BBS: listening on 0.0.0.0:2323`

## 4) Connect from a client

Join the Wi‑Fi network `TOOT-TOOT-BBS` (if AP mode succeeded), then connect:

### Windows (PowerShell)
```powershell
# Raw TCP using netcat (if installed)
nc <k10-ip> 2323
```

### PuTTY
- Connection type: **Raw**
- Host: `<k10-ip>`
- Port: `2323`

### Linux/macOS
```sh
nc <k10-ip> 2323
# or
python3 -m telnetlib <k10-ip> 2323
```

Once connected, you should see:
- banner
- `HANDLE?`

Type a handle, then use commands like `HELP`, `MENU`, `LIST AREAS`, `LIST general`, `READ @LAT10LON5`, `POST general 12`, `BYE`.

## Notes
- If you can connect but don’t see output, your client may be line-buffering; press Enter once.
- If AP setup fails due to platform differences, the rest of the server can still run on an existing network if the device already has Wi‑Fi.
