# USAGE (cycle-01) – Toot-Toot BBS protocol quick reference

All commands are ASCII, line-based, and should end with CRLF (`\r\n`).

## Typical session (human-typed)

```
# connect via raw TCP

HELLO
LOGIN dan
MENU
LIST AREAS
LIST general
READ @LAT10LON5
POST general 18
Hello from TCP BBS
BYE
```

## Commands

- `HELLO`
- `LOGIN <handle>`
- `MENU`
- `HELP`
- `LIST AREAS`
- `LIST <area>`
- `READ <id> [OFFSET n]`
- `POST <area> <nbytes>` then send exactly `<nbytes>` bytes (ASCII suggested)
- `MORE` (continues a prior paged listing, if any)
- `BYE`

## Response framing

Multi-line blocks use:
- `SCR <name>` or `OK <something>`
- `TXT <nbytes>`
- `<bytes>`
- `END`

Errors begin with:
- `ERR <code>`
