# BOOTSTRAP (cycle-01)

Project: **MicroPython TCP BBS for UNIHIKER K10**  
Mode: **Option A – Wi‑Fi Raw TCP (Telnet-style)**  
Workflow: Toot‑Toot Engineering v3.8

## Prompt interpretation (what we’re building)
We are building a **modem-era inspired Bulletin Board System (BBS)** that runs on a **UNIHIKER K10** under **MicroPython**, and accepts **raw TCP socket connections over Wi‑Fi** (device acts as an Access Point).

Key properties:
- **Transport-agnostic core**: the BBS “engine” must not depend on TCP details; TCP is the first transport.
- **Low-bandwidth / unreliable link friendly**: small chunks, pagination, deterministic ASCII UI, offsets for reads.
- **Session-centric**: each TCP connection is a session with ID, handle, last activity.
- **Message persistence**: use a MicroPython-friendly “mpdb-lite” derived from **MyMentalPalaceDB (MMPDB)** node/edge records.

Primary outputs required this cycle:
- Working **MicroPython code** (all `.py` files) implementing MVP capabilities.
- **End-user setup + loading documentation** for K10 + MicroPython + running the server.
- **Tests** (host-side where necessary; MicroPython constraints acknowledged) and supporting docs.

## Assumptions / constraints (explicit)
- Hardware: UNIHIKER K10 (ESP32-class constraints likely; exact RAM/FS limits may vary).
- MicroPython standard libs only (e.g., `socket`, `network`, `time`, `ujson` if available). No heavy deps.
- Text protocol: ASCII, `\r\n`, no ANSI assumed.
- Packet/interaction design should anticipate future store-and-forward links (<= ~200 bytes payload mindset).

Open unknowns (non-blocking for MVP):
- Exact UNIHIKER K10 MicroPython firmware build details and filesystem layout.
- Whether `select` is available; we can implement simple blocking I/O per-session or lightweight polling.

## Team composition (roles needed for excellence)
Recommended roles and why:
1. **Storyteller**: define the BBS “feel”, menus, pacing, copy tone, and minimal protocol ergonomics.
2. **Orchestrator**: adjust the PLAN to include concrete code+docs+tests assets, and ensure repo structure.
3. **Core worker**: implement the full MicroPython BBS codebase + mpdb-lite storage + protocol.
4. **Reviewer**: check protocol consistency, MicroPython compatibility pitfalls, and completeness vs prompt.
5. **Delivery packager**: produce a “how to run” guide, loading instructions, and package final tree.

Optional specialist roles (only if needed):
- **SVG engineer** is **not needed** (no SVG deliverable).
- Potential later: **Image producer/PDF assembler** not needed unless we choose to generate a printable manual.

## Recommended plan adjustments
The default plan is close, but for this software+docs deliverable we should:
1. **Remove/skip SVG engineer step** explicitly for this cycle.
2. Ensure the Orchestrator adds explicit artifacts for:
   - Code folder `/bbs/` with specified files.
   - `deliverables/cycle-01/SETUP.md` (K10 MicroPython + Wi‑Fi AP + upload/run instructions).
   - `deliverables/cycle-01/PROTOCOL.md` (command/response contract; paging/chunk rules).
   - `deliverables/cycle-01/TESTS.md` plus `tests/` host-side helpers (parse/format, mpdb-lite roundtrip).
   - `deliverables/cycle-01/ARCHITECTURE.md` (transport boundary & future Meshtastic compatibility notes).
3. Add a “production artifact” requirement for this repo type:
   - at least one runnable entrypoint: `bbs/main.py`, plus a sample `mpdb-lite` DB file.

## Cycle-01 success criteria (definition of done for this prompt)
- A client can connect via raw TCP, receive banner, login, and use a menu.
- Can list areas, list messages in an area, read a message (supports `OFFSET`), and post a message.
- Data persists across server restarts via mpdb-lite file.
- Protocol is documented and deterministic.
- Setup docs allow a human to reproduce on a K10.

## 3 candidate prompts for next cycle (human must choose one)
1. **Make the protocol real**: implement exact-byte `POST` bodies and server-driven pagination with a `MORE` gate (including client acknowledgment handling) while preserving the transport boundary.
2. **Multi-session servicing**: add cooperative multi-client support (select/poll if available, otherwise round-robin time slicing) and document resource tradeoffs on K10.
3. **Meshtastic-ready adapter (simulated)**: implement a second transport adapter that simulates store-and-forward delivery with <=200-byte packets, plus a replay/log file for offline testing.

## Retrospective (cycle-01)
### What went well
- Strong separation between core logic (protocol/screens/storage) and the TCP transport adapter.
- mpdb-lite parsing/writing is small and testable; host-side tests provide quick confidence.
- Deliverables include setup and protocol docs, plus a runnable starter DB.

### What to improve next cycle
- Don’t declare chunking/paging in protocol docs unless implemented; either implement it or clearly label as “planned.”
- Add an explicit “protocol compliance” checklist item for byte-accurate `POST` and `MORE` paging.
- Add one manual smoke-test transcript (copy/paste session) to validate the real user experience.

### Plan/process changes recommended
- Add a dedicated step for **Protocol compliance hardening** right after Core worker, before Reviewer.
- Add a dedicated step for **On-device constraints audit** (RAM/FS/timeouts) to keep changes realistic.

### Offer to implement
If the human selects a next-cycle prompt, the Bootstrap can:
- reset `PLAN.md` to start cycle-02
- create `deliverables/cycle-02/BOOTSTRAP.md` with the chosen prompt and updated success criteria

