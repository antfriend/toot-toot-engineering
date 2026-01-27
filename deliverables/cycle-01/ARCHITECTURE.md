# ARCHITECTURE (cycle-01)

## High-level design
The system is split into two layers:

1. **BBS core (transport-agnostic)**
   - Owns: sessions, protocol parsing, screen composition, storage.
   - Talks to the outside world only via a minimal connection interface:
     - `send(data: bytes) -> None`
     - `recv(max_bytes: int) -> bytes`
     - `close() -> None`

2. **Transport adapters (TCP first)**
   - Owns: accepting connections, turning sockets into the above interface.
   - Handles timeouts, socket close, and any transport-specific buffering.

This separation is required so later transports (Meshtastic-class store-and-forward, serial, etc.) can reuse the same BBS engine.

## Module responsibilities
Planned code tree:

```
/bbs
  main.py            # boot + Wi-Fi AP + start TCP server + log to screen
  config.py          # ports, limits, banner text, file paths
  transport_tcp.py   # accept loop + per-client connection wrapper
  session.py         # session objects + activity tracking
  protocol.py        # command parsing + state machine
  screens.py         # generate deterministic text screens
  storage.py         # mpdb-lite load/save + message operations
  mpdb_lite.py        # parser/writer for node/edge records
```

## Low-bandwidth / deterministic UI strategy
- The server is responsible for pagination.
- Any screen that may exceed a page budget must be chunked with a `MORE` gate.
- No ANSI cursor movement; only `\r\n` newlines.

## Future-compatibility notes (Meshtastic-class)
Design choices made now to avoid repaint later:
- **Short commands**, line-based.
- **Small response frames**: `SCR`, `TXT`, `END` encourages bounded payloads.
- **Offset reads**: `READ <id> OFFSET <n>` supports partial delivery.
- **Node/edge storage**: messages can be synced as records; edges preserve threading and area membership.

## Concurrency model (MVP)
- MVP can be **single-threaded** with a simple accept loop and per-connection servicing.
- MicroPython threading support varies; prefer cooperative loops and timeouts.

