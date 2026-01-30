# ORCHESTRATOR (cycle-01)

## Plan adjustments applied
- Confirmed **UDP** as the single transport for direct + group messaging.
- Marked SVG engineer step as **skipped** (prompt is not SVG-centered).

## Repo structure for cycle-01 deliverables
All cycle artifacts live under `deliverables/cycle-01/`.

Planned contents:
- `deliverables/cycle-01/TTN_README.md` (end-user instructions; device notes)
- `deliverables/cycle-01/ttn/`
  - `__init__.py`
  - `config.py` (load config from JSON)
  - `message.py` (schema helpers / validation)
  - `node.py` (UDP send/receive, presence)
  - `cli.py` (run a node from config; send message)
- `deliverables/cycle-01/config/`
  - `node_a.json`
  - `node_b.json`
  - `node_c.json`
- `deliverables/cycle-01/demo/`
  - `demo_three_nodes.py` (spawns 3 local nodes for simulation)
- `deliverables/cycle-01/MAKE_ZIP.md` (how to create the requested zip)

Notes:
- We keep dependencies to stdlib only.
- Config format is JSON (simple for non-experts).
- We will include multicast group defaults and a broadcast fallback setting.

## Open decisions for Core Worker
- Choose default group mode: `multicast` with `GROUP_IP=224.1.1.1` (or similar) and document broadcast fallback.
- Presence event shape: use the same message schema with `to="broadcast"` and a reserved `text` prefix like `[presence]` OR add `msg_type` field. (Core Worker should keep schema simple.)

## Release tracking
Delivery Packager will update `RELEASES.md` during packaging. (No update yet.)
