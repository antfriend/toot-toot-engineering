# DELIVERY (cycle-01)

## What shipped
- Reference spec and operator guide for six-device TTN + TTDB build.
- Python reference code for TTDB storage, Windows hub sync server, and K10 gateway.
- Meshtastic TTDB logging module skeleton for Heltec nodes and T-Deck.
- Monitor page for Windows hub visualization.

## How to run (quick)
```bash
cd deliverables/cycle-01/src
PYTHONPATH=. python windows_hub/ttn_hub.py
PYTHONPATH=. python k10_gateway/k10_gateway.py --port /dev/ttyACM0 --k10-id hw:k10
```

Open `http://<hub>:8080/monitor.html` to view nodes and recent messages.

## Notes
- Meshtastic firmware integration requires wiring TTDB module callbacks to the firmware version in use.
- TTDB storage is JSONL per prompt; RFC container export is optional and not implemented as code.
