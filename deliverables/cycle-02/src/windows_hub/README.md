# TTN Hub v2

## Run
```bash
cd deliverables/cycle-02/src
PYTHONPATH=. python windows_hub/ttn_hub_v2.py
```

## Endpoints
- `GET /health`
- `GET /sync/recent` (v1)
- `POST /sync/hash_list` (v1)
- `POST /sync/push` (v1)
- `POST /sync/handshake` (v2)
- `POST /sync/pull` (v2)
- `POST /sync/push_v2` (v2)
- `GET /sync/health`
- `GET /ttdb/records`
- `GET /monitor_v2.html`

## Sync key
Create `sync_key.txt` in the working directory to enable HMAC signing.
