# TESTS (cycle-01)

MicroPython on-device unit testing can be limited. This project uses:
- **host-side tests** for pure parsing/serialization logic (mpdb-lite parser/writer, protocol line parsing)
- optional **manual smoke tests** via netcat/telnet to validate end-to-end behavior.

## Host-side tests (recommended)
Create a `tests/` folder with CPython tests that can run via `python -m unittest`.

Test targets:
- mpdb-lite roundtrip:
  - parse -> object -> write -> parse
  - edges preserved
- message insertion:
  - add area node
  - add message node linked via `in_area`
- protocol parsing:
  - `READ <id> OFFSET <n>` tokenization
  - aliases (`R <id>`, `?`)

## Manual smoke test script (end-to-end)
1. Connect: `nc <k10_ip> 2323`
2. Send:
   - `HELLO`
   - `LOGIN dan`
   - `MENU`
   - `LIST AREAS`
   - `POST general 12` then send `Hello world!`
   - `LIST AREA general`
   - `READ <returned_id>`
   - `BYE`

Expected:
- server never dumps huge text without paging
- responses always end with `END`

