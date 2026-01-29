# DELIVERY (cycle-03)

## What shipped
- Device guides for Unihiker K10 and Lilygo T-Deck Plus (`docs/DEVICE_GUIDES.md`).
- MicroPython-friendly reference implementation (`ttn_mpy/`).

## How to run (MicroPython)
Example:
```bash
python ttn_mpy/node.py --config config/node_b.env listen
```

## Export notes
- The MicroPython reference intentionally keeps the TTN JSON schema identical to CPython.
- For ESP32-class devices, peer-fanout broadcast is the most reliable fallback.
