# STORYTELLER (cycle-01)

## Narrative goal

Make the BBS feel like a **patient, resilient, modem-era machine**: spare words, deliberate pacing, and a friendly-but-deterministic server voice.

The server is “in charge”:
- It offers *small, readable* chunks.
- It remembers where you are.
- It never assumes your terminal can do anything fancy.

## Voice & tone guide (to keep the experience coherent)

**Tone**: calm, technical, slightly charming, never verbose.  
**Style**: short lines, clear prompts, consistent response framing.  
**Reliability cues**: always acknowledge, always provide next instruction.

Preferred phrasing:
- “OK …” for confirmations
- “ERR …” for errors
- “SCR …” for screen blocks
- “TXT <nbytes>” when raw text follows
- “END” always terminates multi-line blocks

Avoid:
- jokes that pad bandwidth
- long banners
- paragraph dumps

## Banner concept

The banner should be short, iconic, and repeatable:

```
TOOT-TOOT BBS / K10
RAW TCP 2323
TYPE HELP

```

Optionally include a single status hint (kept under ~60 chars):
- “LINK: SLOW OK”
- “STORE: MPDB-LITE”

## Login flow (session handshake)

### Human-facing flow

1) On connect, show banner.
2) Ask for handle.
3) After handle, show menu.

Example:

```
TOOT-TOOT BBS / K10
RAW TCP 2323
TYPE HELP

HANDLE? 
```

If the user types nothing / disconnects: session ends silently.

### Protocol-aligned flow

- If the client speaks first (`HELLO`), respond with `OK HELLO` + banner screen.
- If the client sends `LOGIN <handle>`, respond `OK LOGIN` then `SCR MENU MAIN`.

## Menu design (server-driven, minimal)

Main menu should be short and numeric:

```
SCR MENU MAIN
TXT 120
1) LIST AREAS
2) READ (latest)
3) POST
4) HELP
5) BYE
END

CHOICE? 
```

If we keep strict protocol commands, then the “menu” can simply *teach* commands:

```
MENU:
LIST AREAS
LIST <area>
READ <id> [OFFSET n]
POST <area> <nbytes>
BYE
```

## Pagination / “slow link respect” rules

Hard constraints we should bake into implementation:
- Default **page size**: 10–14 lines or <= 600 bytes, whichever first.
- Every screen ends with a clear continuation prompt:
  - `MORE? (Y/N)` or
  - `MORE <token>` (token can be a session-local cursor)

Recommended minimal command:
- `MORE` continues the last paged listing.

If the design avoids a `MORE` command, menu flow can handle it (but `MORE` is very modem-true and keeps bandwidth low).

## Error handling copy (concise and consistent)

Examples:
- Unknown command:
  - `ERR UNKNOWN` then `TYPE HELP`
- Bad args:
  - `ERR ARGS` then show usage line:
    - `USE: READ <id> [OFFSET n]`
- Not logged in:
  - `ERR LOGIN REQUIRED`

## Areas & message listing presentation

Areas should feel like “boards”:

```
OK AREAS
TXT 80
general
hardware
ops
END
```

Message lists should show *just enough*:
- id (short)
- author
- timestamp (maybe human short)
- first 32 chars of body

Example:

```
OK LIST general
TXT 160
@LAT10LON5 dan 1700002000 Hello from the modem era.
@LAT10LON6 bee 1700002100 Copy that, loud and clear.
END
```

## Posting UX

Server should *confirm intent* and keep it strict:

1) Client: `POST general 128`
2) Server: `OK POST SEND 128` (and maybe rules)
3) Client sends exactly 128 bytes.
4) Server: `OK STORED <id>`

If fewer bytes arrive before timeout/disconnect:
- store nothing (or store as a draft node) and respond next connect with recovery option.

## “Future compatibility signal” woven into UX

Without mentioning Meshtastic, we can hint at it through deterministic wording:
- “PACKETS SMALL”
- “RESUME OK”
- “OFFSET READ READY”

Keep hints brief.

## Deliverable: what engineering should implement from this

- A fixed banner and prompt copy.
- A stable menu text generator in `screens.py`.
- A pagination rule (line/byte threshold) used by any “listing” output.
- Standard error strings.
- Optional `MORE` command for continuing a prior listing.
