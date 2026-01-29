# Device Guides (cycle-03)

This document provides practical, device-specific guidance for running TTN on:
- Unihiker K10 (Linux-class device)
- Lilygo T-Deck Plus (ESP32-class device)

If your device firmware differs, keep the message schema and UDP transport unchanged and adapt the
startup steps to your environment.

## Unihiker K10 (Linux-class)
Assumptions: the device runs a Linux-style OS with Python 3.10+ available.

1) **Connect to Wi-Fi and confirm IP**
   - Join the target Wi-Fi network and note the assigned IP address.
   - If possible, reserve a static/DHCP IP so it stays stable.

2) **Copy the TTN repo (or minimal files)**
   - Copy the `ttn/` package, `config/` folder, and `TTN_README.md` to the device.
   - Keep the same `NODE_NAME` and `NODE_IP` conventions as your other nodes.

3) **Edit config**
   - Update `config/node_a.env` (or a device-specific env) with:
     - `NODE_NAME` (unique)
     - `NODE_IP` (device IP)
     - `NODE_PEERS` (other nodes)

4) **Run a listener**
```bash
python -m ttn.node --config config/node_a.env listen
```

5) **Verify multicast status**
   - Look for `multicast_joined=true|false` in the startup log.
   - If `false`, ensure `NODE_PEERS` is set so broadcasts can fall back to peer fanout.

## Lilygo T-Deck Plus (ESP32-class)
Assumptions: the device runs MicroPython and can access Wi-Fi and UDP sockets.

1) **Flash MicroPython and connect Wi-Fi**
   - Install MicroPython firmware for your board.
   - Use a boot script (e.g., `boot.py`) to connect to Wi-Fi and confirm the IP address.

2) **Copy MicroPython-friendly files**
   - Use the `ttn_mpy/` folder as a minimal, MicroPython-friendly reference implementation.
   - Copy `ttn_mpy/` and a config file (e.g., `config/node_b.env`) to the device filesystem.

3) **Edit config**
   - Ensure `NODE_NAME`, `NODE_IP`, and `NODE_PEERS` match your network.

4) **Run the MicroPython node**
```bash
python ttn_mpy/node.py --config config/node_b.env listen
```

5) **If multicast fails**
   - MicroPython stacks vary; multicast may not be supported.
   - Set `NODE_PEERS` so broadcast falls back to peer fanout (direct UDP unicast).

## MicroPython adaptation notes
- The `ttn_mpy/` implementation avoids `argparse`, `dataclasses`, and `uuid`.
- Message IDs are generated via random bytes and hex encoding.
- Timestamps are ISO-8601 UTC (Z) using `utime.gmtime()` formatting.
