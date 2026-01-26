🧭 TOOT-TOOT ENGINEERING PROMPT

Project: MicroPython TCP BBS for UNIHIKER K10
Mode: Option A – Wi-Fi Raw TCP (Telnet-style)
Philosophy: Low-bandwidth, resilient, modem-era inspired systems   
Deliverables: end user how-to documentation, including how to set up the K10 for MicroPython and all .py files and how to load them. Include source files, tests, and supporting documentation.

## 🎯 Objective

Design and implement a MicroPython-based Bulletin Board System (BBS) running on a UNIHIKER K10 that accepts raw TCP socket connections over Wi-Fi, optimized for slow, unreliable, and low-bandwidth links, with architecture intentionally shaped to later support Meshtastic-class transports.

The system should feel like a classic landline modem BBS: deliberate pacing, concise text, server-driven flow, and minimal assumptions about client capabilities.

## 🧠 Core Principles (Non-Negotiable)

- Transport-agnostic core
  - Separate the BBS engine from the transport layer.
  - TCP is the first "modem," not the last.
  - All I/O passes through a narrow interface:
    - send(bytes)
    - recv()
    - close()
- Bandwidth respect
  - No large screens dumped blindly.
  - All output is chunked, paged, or explicitly requested.
  - Server decides pagination boundaries.
- Deterministic text UI
  - Plain ASCII.
  - \r\n line endings.
  - No ANSI assumptions (optional later).
  - Backspace handling is minimal and forgiving.
- Session-centric design
  - Each connection is a session with:
    - session ID
    - username/handle
    - last activity timestamp
  - Multiple sessions may exist concurrently.
- Graceful degradation
  - If a client disconnects mid-read or mid-post, state is recoverable.
  - Reads can resume via offsets.
  - Writes are atomic or explicitly chunked.

## 🏗️ System Architecture (Desired)

```
/bbs
  ├── main.py              # boot + Wi-Fi AP + socket server
  ├── transport_tcp.py     # raw TCP accept/read/write
  ├── session.py           # session lifecycle + state
  ├── protocol.py          # command parsing + responses
  ├── screens.py           # menu text generators
  ├── storage.py           # message persistence
  └── config.py            # ports, limits, banner text
```

## 🔌 Transport: Wi-Fi TCP

- UNIHIKER runs as Wi-Fi Access Point.
- output Wi-Fi server activity to the K10 screen, console style
- TCP server listens on a configurable port (ex: 2323).
- Clients connect using:
  - Windows: PuTTY (Raw), telnet, netcat
  - Anything capable of raw TCP text
- No encryption assumed at this stage.

## 📜 Protocol Expectations

Commands are line-based, human-readable, and short.

Examples:

```
HELLO
LOGIN dan
MENU
LIST AREAS
READ 12
READ 12 OFFSET 400
POST general 128
<128 bytes follow>
BYE
```

Responses are concise and structured:

```
OK LOGIN
SCR MENU MAIN
TXT 312
<bytes>
END
```

## 🗂️ Message Model

Use TTE MyMentalPalaceDB (MMPDB) records as the canonical message model and storage.

Store each BBS message as a node record and use typed edges for relationships:

- reply_to>@NODE_ID
- thread_root>@NODE_ID
- in_area>@AREA_NODE_ID
- next_in_area>@NODE_ID (optional link for paging)

Nodes must include message metadata as plain fields:

- id (MMPDB coordinate-style id)
- author
- timestamp (unix_utc, can mirror created)
- area_name (human-readable string)
- body (length-limited, ASCII)

Areas are nodes too. Use `in_area>@AREA_NODE_ID` for canonical linkage and keep `area_name` for quick display.

Reading supports offsets for partial retrieval, but data is stored as nodes/edges.

Export a MicroPython-reduced DB file (mpdb-lite) that follows the MMPDB spirit:

- single-file, markdown-like records or a compact structured format
- typed edges preserved using `relates:` with `type>@TARGET_ID` tokens
- minimal fields and parsing for MicroPython constraints

If `created`/`updated` headers are present, keep them in sync with `timestamp` (for messages, `timestamp` may mirror `created`).

Provide MicroPython data-access methods for:

- load_db()
- find_node(id)
- insert_node(node)
- update_node(node)
- add_edge(src, edge_type, dst)
- list_edges(src, edge_type=None)
- list_messages_in_area(area_id, area_name=None)
- list_thread(root_id)

Minimal example (mpdb-lite):

```mmpdb
@LAT0LON1 | created:1700001900 | updated:1700001900

id: @LAT0LON1
area_name: general
```

```mmpdb
@LAT10LON5 | created:1700002000 | updated:1700002000 | relates:in_area>@LAT0LON1,thread_root>@LAT10LON5

id: @LAT10LON5
author: dan
timestamp: 1700002000
area_name: general
body: Hello from the modem era.
```

```mmpdb
@LAT10LON6 | created:1700002100 | updated:1700002100 | relates:in_area>@LAT0LON1,reply_to>@LAT10LON5,thread_root>@LAT10LON5

id: @LAT10LON6
author: bee
timestamp: 1700002100
area_name: general
body: Copy that, loud and clear.
```

## 🧪 Initial MVP Capabilities

- Accept TCP connections.
- Show banner + login prompt.
- Main menu with numbered choices.
- Read existing messages.
- Post a short message.
- Clean disconnect.

## 🚦 Explicit Non-Goals (for now)

- No ANSI art.
- No file transfers.
- No authentication security.
- No rich formatting.
- No web UI.
- No Meshtastic yet (but design as if it’s coming).

## 🔮 Future Compatibility Signal

All protocol decisions should assume:

- Packet sizes under 200 bytes.
- Latency measured in seconds.
- Opportunistic delivery.
- Store-and-forward transport.

If a design choice would fail under those conditions, reconsider it now.

## 🧩 Output Expectations from the Agent

- Clear MicroPython code.
- Minimal dependencies.
- Explicit comments explaining why, not just what.
- Preference for clarity over cleverness.
- Systems thinking over features.
- Include a micro Python reduced MMPDB export file and its reader/writer helpers, demonstrating node/edge storage for BBS messages.
