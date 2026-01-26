# BOOTSTRAP (cycle-01)

Project: **MicroPython TCP BBS for UNIHIKER K10**  
Mode: **Option A – Wi‑Fi Raw TCP (Telnet-style)**  
Workflow: Toot-Toot Engineering v3.8

## 1) Prompt interpretation (what we’re building)

We are building a **modem-era inspired Bulletin Board System (BBS)** that runs on a **UNIHIKER K10** under **MicroPython**, and accepts **raw TCP socket connections over Wi‑Fi**.

Key intent:
- **Transport-agnostic BBS core**: the BBS “engine” must not depend on TCP. TCP is just the first transport adapter.
- **Low bandwidth / high latency friendly**: output is deliberately paced and **paged/chunked**; server controls pagination.
- **Deterministic text UI**: ASCII + CRLF. No ANSI assumptions.
- **Session-centric**: each connection maps to a session record with identity + timestamps.
- **Graceful degradation**: partial reads via offsets; atomic-ish posting (or explicitly chunked posting).
- **Storage model**: Use **MyMentalPalaceDB (MMPDB)**-style node/edge records; implement a MicroPython-light “mpdb-lite” file format with helpers.

Primary deliverables for cycle-01:
- A working MicroPython codebase under `deliverables/cycle-01/` (and/or a `bbs/` folder) that can:
  - start Wi‑Fi AP (or connect to Wi‑Fi if configured),
  - listen on TCP port (default 2323),
  - accept multiple concurrent sessions (as feasible in MicroPython),
  - implement a small line-based protocol + menu screens,
  - persist messages using mpdb-lite.
- End-user documentation: setup K10, load `.py` files, run, connect via PuTTY/netcat/telnet.
- Tests/supporting docs (PC-side tests are acceptable; on-device smoke checks documented).

## 2) Team composition (roles) for this cycle

Recommended roles (mapped to the workflow plan steps):
1. **Bootstrap (this step)** – define success criteria, roles, plan adjustments.
2. **Storyteller** – craft the “modem-era” UX voice: banner, menus, pacing rules, concise copy.
3. **Orchestrator** – refine PLAN + repo layout for MicroPython constraints; define module boundaries.
4. **Core worker** – implement the code and documentation.
5. **Reviewer** – protocol correctness, paging/chunking, storage integrity, MicroPython feasibility.
6. **Delivery packager** – package files + quickstart + connection recipes; update `RELEASES.md`.
7. **Retrospective** – lessons learned + next-cycle prompt options.

Optional specialists (may be merged into Core worker if time):
- **Test engineer**: PC-based socket client tests + fuzz for partial reads/timeouts.
- **Embedded constraints advisor**: memory/timeouts, file IO, wear considerations.

## 3) Objectives & acceptance criteria

### MVP acceptance criteria
- TCP server accepts a connection and shows:
  - banner
  - login prompt
  - main menu
- Protocol supports (minimum):
  - `HELLO`
  - `LOGIN <handle>`
  - `MENU`
  - `LIST AREAS`
  - `READ <id> [OFFSET n]`
  - `POST <area> <nbytes>` then reads exactly `nbytes`
  - `BYE`
- Messages persist to a **single-file mpdb-lite** store.
- Output uses ASCII and `\r\n`.
- Output is chunked/paged (server decides page size; client can request “MORE” or menu flow).

### Non-goals (must not creep into MVP)
- No encryption/auth hardening.
- No ANSI art.
- No file transfer.

## 4) Recommended plan adjustments

The existing PLAN is close; recommended refinements for higher success probability:

1) **Split implementation step (Core worker) into sub-steps** (still one role per step, but clearer deliverables):
- Core worker A: storage + mpdb-lite + protocol scaffolding.
- Core worker B: transport adapter + session mgmt + screens + docs.

2) Add an explicit artifact list for the code layout under cycle deliverables, e.g.:
- `deliverables/cycle-01/bbs/` containing:
  - `main.py`, `transport_tcp.py`, `session.py`, `protocol.py`, `screens.py`, `storage.py`, `config.py`
- `deliverables/cycle-01/db/mpdb-lite.mmpdb`
- `deliverables/cycle-01/SETUP.md` (K10 + MicroPython + upload)
- `deliverables/cycle-01/USAGE.md` (how to connect + example session)

3) Add a **PC-side test harness** (runs on desktop CPython) to validate protocol framing, chunking, and offset reads:
- `deliverables/cycle-01/tools/test_client.py`
- `deliverables/cycle-01/tools/test_protocol.py`

4) Add a short **“constraints & decisions”** doc to capture MicroPython realities:
- `deliverables/cycle-01/NOTES.md` (timeouts, max line length, max body length, file format decisions).

These adjustments should be applied by the Orchestrator when updating `PLAN.md`.

## 5) Risks / open questions (to be resolved downstream)

- UNIHIKER K10 MicroPython specifics: exact WLAN/AP APIs and screen logging APIs can vary; we may need an abstraction and a “known-good” default.
- Concurrency model: true concurrent sessions may be limited; we may implement cooperative multitasking with `select` (if available) or a simple accept-loop with short time slices.
- File system performance/wear: mpdb-lite append strategy and compaction policy.

## 6) Next-cycle prompt candidates (human must choose later)

These are **for cycle-02** and should build on cycle-01 deliverables.

1) **Meshtastic-ready transport adapter**: Implement a store-and-forward transport interface + a simulated high-latency/200-byte MTU link adapter; update protocol to be robust under packetization.
2) **Offline-first message sync**: Add export/import bundles for areas/threads, plus conflict-handling rules and deterministic message IDs.
3) **UI/UX polish + accessibility**: Add help screens, better pagination, optional minimal ANSI detection, and on-device status dashboard.
