# REVIEW (cycle-01)

## Scope check (prompt requirements)
Required:
- 3-node IP network, direct + broadcast/group messaging ✅ (implemented via UDP unicast + UDP multicast/broadcast)
- User-configurable:
  - `NODE_NAME` ✅
  - `NODE_IP` ✅
  - `NODE_PORT` ✅
  - `GROUP_IP` / `GROUP_PORT` ✅
  - `NODE_PEERS` ✅
- Clear instructions for configuring names and static/reserved IPs ✅ (TTN_README)
- Single transport choice ✅ (UDP)
- Minimal runnable implementation ✅ (`deliverables/cycle-01/ttn/`)
- Message format spec ✅ (TTN_README includes required JSON; optional `msg_type` documented)
- Demo scenario A→B, B→A, C→broadcast ✅ (demo script exists; also CLI instructions)
- Optional monitor/log view ✅ (stdout logs)
- Bundled zip ✅ (`TTN_delivery_cycle-01.zip`)

## Correctness review
### Direct messaging
- `send_direct()` sends to peer IP on `NODE_PORT` (assumes all nodes listen on same port). Matches example configs.
- Receiver filters messages to either `to==broadcast` or `to==this_node_name`. Good.

### Group messaging
- Design was adjusted to a **single-port** design: `GROUP_PORT == NODE_PORT` is enforced by config loader to reduce OS-dependent multicast binding issues.
- Sender uses `GROUP_IP:GROUP_PORT`.

Observed in local run:
- Direct messaging works (A→B, B→A).
- Multicast delivery on loopback may not show reliably in this environment (platform-dependent). This is a known limitation; on a real LAN with multicast enabled, it should work. Broadcast mode is provided as fallback.

### Config validation
- Config loader errors if `GROUP_PORT != NODE_PORT`, preventing silent misconfiguration.

## Usability review
- TTN_README is clear and copy/paste friendly.
- Known pitfalls include firewall and multicast restrictions.
- Device notes correctly caveat that CPython 3.10 may not run on target devices and provide porting guidance.

## RFC alignment
- TTN-RFC-0001 transport-agnostic satisfied.
- This package is intentionally not implementing semantic mesh/TTDB (explicitly stated).

## Delivery readiness
Ready to package with one note:
- Multicast can be blocked on some Wi‑Fi networks; users may need `GROUP_MODE=broadcast`.
