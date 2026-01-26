# NOTES (cycle-01) – Constraints & decisions

## MicroPython constraints (assumed)
- Limited RAM; avoid building huge strings.
- Socket APIs differ (`usocket` vs `socket`).
- `select` may not exist; concurrency is best-effort.

## Design decisions
- **Transport abstraction**: the BBS core only relies on `send(bytes)`, `recv_line(...)`, `recv_exact(...)`, and `close()` provided by the transport adapter.
- **ASCII + CRLF**: all output is ASCII with CRLF line endings; no ANSI.
- **Server-driven pagination**: list outputs are paged; a simple `MORE` continues.
- **mpdb-lite storage**: append-only records; “update” is implemented as append-new and latest-wins on load.

## Known gaps
- True multi-session concurrency is not implemented; the server handles one client at a time in a simple accept-loop.
- Wi‑Fi AP setup is best-effort; UNIHIKER K10 may require different APIs.
- MMPDB coordinate IDs are generated heuristically; a more rigorous allocator can be added later.
