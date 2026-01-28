# TTN (Toot-Toot Network) — Minimal 3-Node Messaging over UDP

This repo contains a minimal, runnable **3-node IP messaging network** (TTN) where nodes can:
- Send **direct** messages to a specific node
- **Broadcast to the group** (implemented as UDP multicast, with a peer fanout fallback)
- Use end-user configured **node name** and **IP address**

Target nodes (conceptually):
- Node A: Unihiker K10
- Node B: Lilygo T-Deck Plus
- Node C: Windows 11 PC

The implementation is **Python 3.10** and is designed to run locally on one subnet.

## Transport choice
**UDP**
- **Direct:** UDP unicast to a peer’s IP/port.
- **Group/broadcast:** UDP multicast to `GROUP_IP:GROUP_PORT`.

No broker, no extra services.

## Folder layout
```
/ttn/
  config.py          # loads .env-style config
  message.py         # TTN message schema (JSON)
  transport_udp.py   # UDP unicast + multicast helpers
  node.py            # CLI entrypoint: listen/direct/broadcast
/config/
  node_a.env
  node_b.env
  node_c.env
/scripts/
  run_three_nodes.py # prints commands for the demo scenario
```

## TTN message schema
JSON object:
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

## Configuration (node name + IP address)
Each node uses a simple config file like `config/node_a.env`:

Required keys:
- `NODE_NAME` — friendly unique name (e.g., `node-a`)
- `NODE_IP` — the node’s own IP address (e.g., `192.168.1.10`)

Also used:
- `NODE_PORT` — UDP port to listen on (default `5005`)
- `GROUP_IP`, `GROUP_PORT` — multicast group for “broadcast” (defaults `239.255.0.1:5006`)
- `NODE_PEERS` — comma-separated `name@ip` entries for direct messaging

### 1) Pick a unique NODE_NAME
Choose any short unique label. Recommendation:
- lowercase
- dashes
- no spaces

Examples: `node-a`, `k10`, `tdeck`, `workshop-pc`

### 2) Assign or reserve a static IP (NODE_IP)
You need stable IPs so peers can reach each other.

Options:
1. **DHCP reservation (recommended):** in your router’s admin UI, reserve an IP per device MAC address.
2. **Static IP:** configure the device network settings manually.

Pick three IPs on the same subnet, for example:
- Node A: `192.168.1.10`
- Node B: `192.168.1.11`
- Node C: `192.168.1.12`

### 3) Edit each node’s config
Update `NODE_NAME`, `NODE_IP`, and `NODE_PEERS` to match your network.

Example `NODE_PEERS`:
```
NODE_PEERS=node-b@192.168.1.11,node-c@192.168.1.12
```

## How to run
### Requirements
- Python 3.10+
- No external pip dependencies (see `requirements.txt`)

### Start three listeners
Open **three terminals** (or three SSH sessions) and run:

Terminal A:
```bash
python -m ttn.node --config config/node_a.env listen
```
Terminal B:
```bash
python -m ttn.node --config config/node_b.env listen
```
Terminal C:
```bash
python -m ttn.node --config config/node_c.env listen
```

### Send direct messages
From any terminal:
```bash
python -m ttn.node --config config/node_a.env direct node-b "Hello node-b"
python -m ttn.node --config config/node_b.env direct node-a "Hi node-a"
```

### Send a broadcast to the group
```bash
python -m ttn.node --config config/node_c.env broadcast "Hello everyone"
```

### Demo helper
This prints the exact commands:
```bash
python scripts/run_three_nodes.py
```

## Troubleshooting
- **Windows Firewall:** allow Python to receive UDP on your chosen port.
- **Multicast not working:** some networks block multicast. Broadcast will fall back to “send to all peers” if `NODE_PEERS` is set.

## Notes for real devices
- If a device can’t use CPython, keep the schema and CLI concepts and port the same UDP behavior.
