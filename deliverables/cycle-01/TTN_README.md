# TTN_README (cycle-01)

## Overview
This package builds a **simple 3-node Toot Toot Network (TTN)** on a single IP subnet.

It supports:
- **Direct messages**: Node A → Node B (unicast UDP)
- **Group messages**: Node C → everyone (UDP multicast by default; broadcast fallback)
- **User configuration** per node:
  - `NODE_NAME`
  - `NODE_IP`
  - `NODE_PORT`
  - `GROUP_IP` / `GROUP_PORT`
  - `NODE_PEERS`

Transport: **UDP** (single transport for all nodes).

## Folder layout
- `ttn/` : minimal Python implementation
- `config/` : example JSON configs for three nodes
- `demo/` : a local simulation script

## TTN message schema
Required fields (per prompt):
```json
{
  "msg_id": "uuid",
  "from_name": "node-alpha",
  "from_ip": "192.168.1.10",
  "to": "node-beta|broadcast",
  "ts": "2026-01-27T18:14:02Z",
  "text": "Hello team"
}
```

Optional field used by the reference implementation:
```json
{
  "msg_type": "chat|presence"
}
```
Consumers that ignore unknown fields remain compatible.

## Transport choice and rationale (UDP)
- No broker/service required.
- Easy to run on a LAN.
- Unicast handles direct messages.
- Multicast/broadcast handles group messages.

## Configuration instructions (node name + IP address)
### 1) Pick a unique `NODE_NAME`
Choose a friendly label you can recognize in logs. Examples:
- `k10-alpha`
- `tdeck-beta`
- `pc-charlie`

### 2) Assign or reserve a static IP address
Recommended approach: **DHCP reservation** (router assigns the same IP every time).
Alternative: **static IP** on the device.

You must ensure:
- All nodes are on the **same subnet** (e.g., `192.168.1.x`).
- IPs do not conflict.

### 3) Edit the node config JSON
Copy one of the example configs from `config/` and edit:
- `NODE_NAME`: your chosen name
- `NODE_IP`: the IP of that device
- `NODE_PORT`: default `5005`
- `GROUP_MODE`: `multicast` (default) or `broadcast`
- `GROUP_IP`:
  - multicast example: `224.1.1.1`
  - broadcast fallback: `255.255.255.255` (may be blocked on some routers)
- `GROUP_PORT`: **must equal `NODE_PORT`** in this reference implementation (single-port design)
- `NODE_PEERS`: map of **peer node name -> peer IP** for direct messages

## How to run (Windows 11 reference implementation)
Prereq: **Python 3.10+**

Open three terminals.

### Terminal A (Node A)
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_a.json run --presence
```

### Terminal B (Node B)
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_b.json run --presence
```

### Terminal C (Node C)
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_c.json run --presence
```

### Send direct messages
From Node A terminal (or a 4th terminal):
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_a.json send --to tdeck-beta --text "Can you hear me?"
```

Reply from Node B:
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_b.json send --to k10-alpha --text "Loud and clear."
```

### Broadcast to the group
From Node C:
```powershell
cd deliverables\cycle-01
python -m ttn.cli --config config\node_c.json send --to broadcast --text "Workshop check-in: everyone report status."
```

All three terminals should log the broadcast.

## Demo script (single-machine simulation)
This simulates three nodes on loopback IPs.
```powershell
cd deliverables\cycle-01
python demo\demo_three_nodes.py
```

If your OS does not support `127.0.0.2/127.0.0.3/127.0.0.4`, edit the script to use different ports instead.

## Device-specific notes
### Node A: Unihiker K10
- Goal: run the same UDP concepts.
- Reality check: depending on its Python environment, you may not have full CPython 3.10.

Recommended approach for cycle-01:
- Use the Windows 11 reference node as the runnable baseline.
- On K10, aim to replicate:
  - UDP receive loop
  - JSON encode/decode
  - config file fields

If K10 supports CPython and networking, you can try running `ttn/` directly; otherwise, port the logic to the supported runtime.

### Node B: Lilygo T-Deck Plus
- Commonly ESP32-class; often runs MicroPython.
- The reference code is written to be easy to port:
  - Replace `socket` usage with `usocket`.
  - Replace `json` with `ujson`.
  - Replace threads with a simple polling loop.

### Node C: Windows 11 PC
- Recommended as the reference node and for monitoring/log visibility.

## Known pitfalls
- Windows Firewall may block UDP inbound; allow Python for private networks.
- Multicast may be blocked on some Wi‑Fi APs; switch to `GROUP_MODE=broadcast` if needed.
- Ensure `GROUP_PORT == NODE_PORT` for this reference implementation.

## Compliance notes (TTN RFC)
- Transport agnostic (TTN-RFC-0001): we choose UDP for simplicity.
- This implementation is a messaging substrate; it does not implement semantic mesh or TTDB.
