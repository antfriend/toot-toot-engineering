# REVIEW (cycle-01)

## Scope check vs prompt
### Required MVP capabilities
- Accept TCP connections: **Yes** (`bbs/transport_tcp.py`, `bbs/main.py`)
- Banner + login prompt: **Partial**
  - Banner/welcome is shown immediately on connect (HELLO screen sent automatically).
  - Login exists (`LOGIN <handle>`), but there is not a separate interactive prompt; it’s command-based.
- Main menu with numbered choices: **Yes** (`MENU`, `screens.menu_main`)
- Read existing messages: **Yes** (`READ <id> [OFFSET]`)
- Post a short message: **Yes**, with caveat (see below)
- Clean disconnect: **Yes** (`BYE`)

### Architectural non-negotiables
- Transport-agnostic core with narrow I/O interface: **Mostly**
  - Protocol and storage are transport-agnostic.
  - Transport wrapper provides `send/recv/close` and a `readline()` helper.
  - Protocol currently assumes line-based inputs even for POST body; strict byte-count framing not fully honored.

- Bandwidth respect / pagination: **Gap**
  - Protocol uses `SCR/TXT/END` frames but does **not** implement chunking and `MORE` gates yet.
  - Screens are modest now; still, listing could exceed budgets later.

- Deterministic text UI: **Yes**
  - ASCII encode ignore, CRLF in screens.

- Session-centric design: **Yes** (`Session` has id, handle, last_activity)

- Graceful degradation / resume via offsets: **Partial**
  - READ supports offset.
  - POST creates draft node before body; however, the body reader is line-based and does not track partial byte offsets reliably.

### Storage model (MMPDB/mpdb-lite)
- Nodes + typed edges: **Yes**
- Areas are nodes too: **Yes**
- Exportable single-file format: **Yes** (`bbs_data/mpdb_lite.mmpdb`)
- MicroPython data-access methods listed in prompt: **Mostly**
  - Implemented as methods on `storage.DB` (load/find/insert/update/add_edge/list_edges/list_messages_in_area/list_thread).

## Key issues to address before calling it “excellent”
1. **POST exact byte mode**
   - Protocol says: `POST area nbytes` then `<nbytes bytes follow>`.
   - Current implementation collects *lines* until len(buf) >= need, and appends `\n` while waiting.
   - Recommendation: adjust transport/protocol to read **raw bytes** for POST body (exactly nbytes) from socket.

2. **Pagination (`MORE` gate)**
   - Not implemented.
   - Recommendation: implement a helper that chunks payload to `PAGE_MAX_BYTES`/`PAGE_MAX_LINES` and sends `MORE` frames.
   - Note: This requires protocol to be able to send multiple frames per command, and transport to read a `MORE` response.

3. **Multi-session concurrency**
   - Prompt says multiple sessions may exist concurrently.
   - Current server is sequential accept+serve; a second client will wait.
   - Recommendation: for MicroPython MVP, consider cooperative multiplexing with `select` if available; otherwise document limitation clearly in DELIVERY.

4. **LOGIN requirement enforcement**
   - POST requires login; READ/LIST do not. That’s acceptable unless you want private boards.

## What’s solid
- Clean module boundaries.
- mpdb-lite parsing fixed to handle blank lines without record splitting.
- Host-side unit tests pass.

## Suggested fixes (if time permits in this cycle)
- Implement `conn.read_exact(n)` and drive POST body reading from transport.
- Add a minimal pagination helper that can split screens and require `MORE`.
- Update docs to clearly describe limitations if not implemented.

