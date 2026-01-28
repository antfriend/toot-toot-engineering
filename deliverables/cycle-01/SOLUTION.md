# SOLUTION (cycle-01)

This cycle delivers a minimal runnable **3-node TTN messaging network** over **UDP** with:
- Direct node-to-node messages (unicast)
- Group “broadcast” messages (multicast, with peer-fanout fallback)
- Configurable `NODE_NAME` and `NODE_IP` via simple `.env` files

## Primary runnable assets
- `ttn/node.py` — CLI to `listen`, `direct`, and `broadcast`
- `ttn/message.py` — TTN JSON message schema helpers
- `ttn/config.py` — `.env` loader + peer mapping parser
- `ttn/transport_udp.py` — UDP unicast/multicast helpers
- `config/node_a.env`, `config/node_b.env`, `config/node_c.env` — example configs
- `scripts/run_three_nodes.py` — prints the demo commands

## How to run (summary)
See the top-level `README.md` for step-by-step instructions.

Quick demo:
1. Start listeners in 3 terminals:
   - `python -m ttn.node --config config/node_a.env listen`
   - `python -m ttn.node --config config/node_b.env listen`
   - `python -m ttn.node --config config/node_c.env listen`
2. Send the required scenario:
   - `python -m ttn.node --config config/node_a.env direct node-b "Hello node-b"`
   - `python -m ttn.node --config config/node_b.env direct node-a "Hi node-a"`
   - `python -m ttn.node --config config/node_c.env broadcast "Hello everyone"`

## Notes
- If multicast is unavailable, broadcast attempts fall back to sending the same message to each peer listed in `NODE_PEERS`.
