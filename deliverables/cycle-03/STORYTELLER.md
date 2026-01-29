# STORYTELLER (cycle-03)

## Narrative focus
This cycle moves TTN from “local demo” to “real device companion.” Each device guide tells a consistent story: get online, confirm IP, configure peers, then run a listener. The MicroPython reference keeps the TTN message envelope identical so that CPython and MicroPython nodes can talk without translation.

## UX narrative beats
- **Same schema everywhere:** device differences do not alter message fields.
- **Config-first setup:** node identity and peers are always set in `.env` files.
- **Fallback clarity:** if multicast is unavailable, peer fanout keeps the mesh alive.
