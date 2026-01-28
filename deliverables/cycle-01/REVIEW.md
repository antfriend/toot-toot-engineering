# REVIEW (cycle-01)

## Scope check vs prompt
Required:
- Direct messages ✅ (CLI: `direct to_name text`)
- Broadcast to whole group ✅ (CLI: `broadcast text`; UDP multicast + fallback)
- End-user configured node name and IP ✅ (`config/node_*.env` with `NODE_NAME`, `NODE_IP`)
- Clear instructions ✅ (top-level `README.md`)
- Minimal runnable implementation ✅ (`ttn/` package)
- Message format spec ✅ (README schema + `ttn/message.py`)
- Demo scenario ✅ (documented in README + `scripts/run_three_nodes.py`)
- Optional monitor/logging ✅ (console logs on each node)

## Key fixes applied during review
1. **Multicast receive ports**
   - Broadcast is sent to `GROUP_PORT`.
   - Listener now listens on **both** `NODE_PORT` and `GROUP_PORT` (if different) using `select`, so group packets can be received reliably.

## Remaining risks / notes
- **Windows Firewall:** allow inbound UDP on the chosen ports (node + group port). If ports differ, allow both.
- **Multicast availability:** some networks block multicast; the sender falls back to peer fanout if multicast send fails and `NODE_PEERS` is configured.

## Overall assessment
Meets the prompt requirements for a minimal, complete 3-node TTN. Ready for delivery packaging.
