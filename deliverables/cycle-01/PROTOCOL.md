# PROTOCOL (cycle-01)

Protocol style: **line-based ASCII**, `\r\n` endings.

## Framing
- Client sends a command line.
- Server replies with a short status line and optionally a screen payload.

Canonical response frame:
```
OK <verb>
SCR <screen_name>
TXT <nbytes>
<exactly nbytes of payload>
END
```

Error frame:
```
ERR <reason>
END
```

## Commands (MVP)
All tokens separated by spaces.

### HELLO
Client announces itself.
- Request: `HELLO`
- Response: `OK HELLO` + welcome screen.

### LOGIN <handle>
- Request: `LOGIN dan`
- Response: `OK LOGIN`

Rules:
- Handle is ASCII, 1..16 chars.

### MENU / ?
- Request: `MENU` or `?`
- Response: `OK MENU` + main menu screen.

### LIST AREAS
- Request: `LIST AREAS`
- Response: `OK AREAS` + area listing screen.

### LIST AREA <area_name>
- Request: `LIST AREA general`
- Response: `OK LIST` + list of latest message headers.

### READ <msg_id> [OFFSET <n>]
- Request: `READ @LAT10LON5`
- Request: `READ @LAT10LON5 OFFSET 400`
- Response: `OK READ` + message screen.

### POST <area_name> <nbytes>
Two-stage post:
1) Client declares intent.
2) Client sends exactly `<nbytes>` bytes of body.

- Request: `POST general 128`
- Response: `OK POST READY`
- Client then sends 128 bytes (ASCII body; may include `\r\n`).
- Server responds: `OK POSTED <msg_id>`

If the connection drops during body transfer, the server should either:
- keep a draft record with a partial body and a `status:draft` field, or
- discard it cleanly.
(Reviewer can decide which is more robust under constraints; draft is preferred.)

### BYE
- Request: `BYE`
- Response: `OK BYE` then server closes.

## Aliases (optional but recommended)
- `1` => `LIST AREAS`
- `R <id>` => `READ <id>`

## Pagination / MORE gate
When a screen exceeds the configured page budget, server sends a partial payload and then:
```
MORE
```
Client may reply with either:
- `MORE` or
- an empty line (just ENTER)

Server continues with the next chunk using another `TXT <nbytes>` frame (screen name may repeat) until complete.

