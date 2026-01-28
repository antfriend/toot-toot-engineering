# DELIVERY (cycle-01)

## What was delivered
A minimal, complete **TTN (Toot-Toot Network)** messaging system for **3 nodes on a single IP subnet**.

### Primary artifacts
- `ttn/node.py` — node CLI runtime (`listen`, `direct`, `broadcast`)
- `ttn/message.py` — TTN JSON message schema
- `ttn/config.py` — `.env` config loader (`NODE_NAME`, `NODE_IP`, ports, peers)
- `ttn/transport_udp.py` — UDP helpers (unicast + multicast)

### Other deliverables
- `README.md` — setup + configuration + run + demo instructions
- `config/node_a.env`, `config/node_b.env`, `config/node_c.env` — example configs
- `scripts/run_three_nodes.py` — prints the demo commands
- `deliverables/cycle-01/BOOTSTRAP.md`
- `deliverables/cycle-01/STORYTELLER.md`
- `deliverables/cycle-01/SOLUTION.md`
- `deliverables/cycle-01/REVIEW.md`

## How to run (quick)
1. Configure each node’s `.env` file under `config/`:
   - Set `NODE_NAME` unique per node
   - Set `NODE_IP` to the device’s IP on your LAN
   - Set `NODE_PEERS` to map peer names to IPs
2. Start listeners (3 terminals):
   - `python -m ttn.node --config config/node_a.env listen`
   - `python -m ttn.node --config config/node_b.env listen`
   - `python -m ttn.node --config config/node_c.env listen`
3. Send the required demo scenario:
   - `python -m ttn.node --config config/node_a.env direct node-b "Hello node-b"`
   - `python -m ttn.node --config config/node_b.env direct node-a "Hi node-a"`
   - `python -m ttn.node --config config/node_c.env broadcast "Hello everyone"`

(See `README.md` for the full explanation and troubleshooting.)

## Notes / export considerations
- **UDP ports:** the listener listens on both `NODE_PORT` and `GROUP_PORT` (if different). Ensure firewalls allow inbound UDP on those ports.
- **Multicast:** broadcast uses UDP multicast to `GROUP_IP:GROUP_PORT`. If multicast is blocked/unavailable, the sender falls back to sending the message to each peer in `NODE_PEERS`.

## Definition of Done check
- Configure unique names and IPs for three nodes ✅
- Start all three nodes ✅
- Send direct messages between any two nodes ✅
- Broadcast a message that all nodes receive ✅ (multicast or peer fanout)
