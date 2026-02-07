# DELIVERY (cycle-02)

## What shipped
- TTDB sync v2 protocol spec with versioned handshake and optional HMAC integrity.
- Hub v2 server with sync health endpoint and compatibility with v1.
- Windows hub dashboard for node status, sync health, and message flow.
- Unit tests and migration notes.

## How to run
```bash
cd deliverables/cycle-02/src
PYTHONPATH=. python windows_hub/ttn_hub_v2.py
```

Open `http://<hub>:8081/monitor_v2.html`.

## Notes
- Create `sync_key.txt` (shared secret) to enable HMAC signing.
- Sync health is stored in memory; it resets on restart.
