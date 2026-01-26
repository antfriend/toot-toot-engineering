# DELIVERY (cycle-01) – Toot-Toot BBS / K10

## Deliverables

### Source code (MicroPython)
- `deliverables/cycle-01/bbs/`
  - `main.py` – server boot + accept loop
  - `transport_tcp.py` – TCP adapter (send/recv_line/recv_exact/close)
  - `session.py` – session state + paging cursor
  - `protocol.py` – line protocol + responses
  - `screens.py` – banner/menu/help text
  - `storage.py` – mpdb-lite load/insert/update + minimal query helpers
  - `config.py` – port, paging, limits

### Database sample
- `deliverables/cycle-01/db/mpdb-lite.mmpdb`

### Documentation
- `deliverables/cycle-01/SETUP.md` – how to upload + run on K10, connect via PuTTY/netcat
- `deliverables/cycle-01/USAGE.md` – command reference + protocol framing
- `deliverables/cycle-01/NOTES.md` – constraints & known gaps

### Tests / tools (CPython)
- `deliverables/cycle-01/tools/test_client.py` – interactive raw TCP client
- `deliverables/cycle-01/tools/test_protocol.py` – minimal smoke tests

### Planning artifacts
- `deliverables/cycle-01/BOOTSTRAP.md`
- `deliverables/cycle-01/STORYTELLER.md`
- `deliverables/cycle-01/REVIEW.md`

## How to run (quick)

1) Copy `deliverables/cycle-01/bbs/` to the device as `bbs/`.
2) Copy `deliverables/cycle-01/db/` to the device as `db/`.
3) Run:

```python
from bbs.main import main
main()
```

4) Connect to TCP port 2323 with a raw TCP client.

## Known limitations (from review)
- Handles one client session at a time (no multiplexing/threading yet).
- Message IDs are heuristic, not a full MMPDB coordinate allocator.
- Canonical `in_area>@AREA_ID` edges exist in sample DB, but listing filters currently rely on `area_name`.

## Next suggested improvements
- Add concurrency via `select` or `_thread` (depending on availability).
- Add a real ID allocator (e.g., persist next lat/lon in a meta node).
- Use area nodes + `in_area` edges as the primary linkage for LIST/READ flows.
