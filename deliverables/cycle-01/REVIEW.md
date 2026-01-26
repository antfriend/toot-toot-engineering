# REVIEW (cycle-01)

## Scope reviewed
- Code: `deliverables/cycle-01/bbs/`
- Docs: `deliverables/cycle-01/SETUP.md`, `USAGE.md`, `NOTES.md`
- Storage sample: `deliverables/cycle-01/db/mpdb-lite.mmpdb`
- Tools: `deliverables/cycle-01/tools/test_client.py`, `test_protocol.py`

## What looks good
- Clear separation of concerns:
  - TCP specifics in `transport_tcp.py`
  - session state in `session.py`
  - command parsing/responses in `protocol.py`
  - mpdb-lite persistence in `storage.py`
- Deterministic, low-bandwidth UI:
  - ASCII output, CRLF normalization, compact menu/help
  - server-driven paging with `MORE`
- Storage matches the prompt’s intent:
  - single-file, markdown-like records
  - typed edges preserved via `relates:` tokens
  - append-only update strategy is MicroPython-friendly

## Gaps / issues to fix (recommended)

### 1) Area filtering by `area_id` is buggy / unused
`storage.list_messages_in_area()` contains a complicated partial check for `area_id` and does not correctly verify `in_area>@ID` tokens.
- Impact: low right now (code mainly filters by `area_name`), but it undermines the “canonical linkage” requirement.
- Fix: implement a simple, correct matcher for `in_area>@...` and use it in `protocol.py` (LIST by area could map area_name -> area node id).

### 2) Message ID allocator is not truly MMPDB coordinate-style
IDs are generated from time modulus:
- Impact: may collide and isn’t aligned with MMPDB coordinate increment/collision policy.
- Fix: add a tiny allocator:
  - scan existing IDs, track last used lat/lon, increment lon, then lat on overflow; or
  - maintain a `@META` node in DB storing `next_lat/next_lon`.

### 3) Concurrency claim vs implementation
Prompt says “multiple sessions may exist concurrently.” Current `main.py` handles one connection at a time.
- Impact: functional MVP still works; but it violates a stated requirement.
- Fix options:
  - implement cooperative multiplexing using `select` (if available) or
  - a very small `_thread`-based handler per client (if `_thread` exists).

### 4) Login prompt mismatch
On connect we show `HANDLE?` but also support `LOGIN <handle>`.
- Impact: not harmful, but mixed UX.
- Fix: accept raw handle input at `HANDLE?` (treat any non-command line as handle if not logged in) OR change prompt to `LOGIN?`.

### 5) Protocol response framing consistency
Some flows send direct text (banner + HANDLE prompt) while others use SCR/TXT/END framing.
- Impact: acceptable for modem-era human clients, but can confuse automated clients.
- Fix: optional: wrap initial banner in `SCR BANNER` block always.

## Documentation checks
- Setup + connection instructions exist and are actionable.
- Clarifies best-effort Wi‑Fi AP setup and known platform variability.

## Overall assessment
Meets the cycle-01 MVP intent as a functional, readable baseline with clear next fixes. The top priority improvements are: (1) concurrency strategy, and (2) a more MMPDB-faithful ID allocator, and (3) canonical `in_area` edge usage.
