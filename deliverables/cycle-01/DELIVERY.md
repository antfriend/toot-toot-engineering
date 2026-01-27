# DELIVERY (cycle-01)

## What you got
A MicroPython-friendly raw TCP (telnet-style) BBS for UNIHIKER K10.

Included:
- `/bbs/` codebase implementing:
  - TCP transport adapter
  - sessions
  - line-command protocol with `SCR/TXT/END` framing
  - deterministic ASCII screens
  - mpdb-lite persistence (MMPDB-inspired nodes/edges)
- Starter database: `/bbs_data/mpdb_lite.mmpdb`
- Host-side tests: `/tests/`
- Supporting docs in `deliverables/cycle-01/`:
  - `ARCHITECTURE.md`, `PROTOCOL.md`, `SETUP.md`, `TESTS.md`, `REVIEW.md`

## File tree
```
bbs/
  __init__.py
  main.py
  config.py
  transport_tcp.py
  session.py
  protocol.py
  screens.py
  storage.py
  mpdb_lite.py
bbs_data/
  mpdb_lite.mmpdb
deliverables/cycle-01/
  BOOTSTRAP.md
  STORYTELLER.md
  ARCHITECTURE.md
  PROTOCOL.md
  SETUP.md
  TESTS.md
  REVIEW.md
  DELIVERY.md
tests/
  test_mpdb_lite.py
  test_protocol_parse.py
```

## How to run (quick)
1. Copy `bbs/` to your K10.
2. Ensure the DB path exists (default expects `/bbs_data/mpdb_lite.mmpdb`).
   - Create `/bbs_data/` if needed.
3. Run `bbs/main.py`.
4. Join the K10 Wi‑Fi AP (SSID in `bbs/config.py`).
5. From a computer: `nc <k10_ip> 2323`

Try:
- `HELLO`
- `LOGIN dan`
- `MENU`
- `LIST AREAS`
- `LIST AREA general`
- `READ @MSG_WELCOME`
- `POST general 12` then send `Hello world!`
- `BYE`

(Full notes in `deliverables/cycle-01/SETUP.md`.)

## Important limitations (known gaps)
These are the main deltas vs the ideal prompt behavior:
1. **POST body framing**: protocol specifies "exactly N bytes follow"; current MVP collects line-based input until it has at least N characters. For true byte-accurate posts, extend transport/protocol with a `read_exact(n)` path.
2. **Pagination / MORE gate**: response framing exists, but automatic chunking and interactive `MORE` paging is not implemented yet.
3. **Concurrency**: accept loop is sequential; one client at a time in practice.

Despite these, the architecture is intentionally shaped so these improvements are localized.

## Running tests (host-side)
From your development machine (CPython):

```
python -m unittest discover -s tests
```

## Next recommended enhancements
- Implement `read_exact(n)` for POST and make it transport-driven (keeping protocol transport-agnostic).
- Implement screen chunking with `MORE`.
- Add cooperative multi-session servicing if `select` is available.

