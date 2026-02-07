# SOLUTION (cycle-02)

## Executive summary
This cycle hardens the TTDB sync protocol with versioning, integrity checks, and backward compatibility, and delivers a Windows hub dashboard that visualizes node status, sync health, and message flows. It remains compatible with cycle-01 JSONL TTDB and the existing HTTP sync endpoints.

## TTDB Sync Protocol v2

### Goals
- Backward compatibility with cycle-01 hash-list sync.
- Versioned handshake to support future extensions.
- Integrity and authenticity with optional HMAC signatures.

### Protocol versioning
- `sync_version`: integer, current v2.
- v1 nodes (cycle-01) omit `sync_version` and use the v1 endpoints.
- v2 nodes MUST accept v1 requests and respond with v1-compatible payloads when `sync_version` is absent.

### Handshake
1. Client sends `POST /sync/handshake` with:
   - `sync_version`
   - `node_id`
   - `capabilities` (e.g., `hmac`, `delta_push`, `gzip`)
   - `nonce`
2. Server responds with:
   - `sync_version`
   - `server_id`
   - `accepts` (capabilities)
   - `nonce`
   - `signature` (optional if HMAC enabled)

### Message integrity and auth
- Shared secret `sync_key` provisioned out-of-band (per LAN or per node).
- HMAC-SHA256 over canonical JSON for handshake and data payloads.
- If `sync_key` missing, nodes downgrade to integrity-only mode (hash lists) and log `sync_diff` with `mode=unauth`.

### Backward compatibility
- v2 nodes keep the v1 endpoints:
  - `GET /sync/recent`
  - `POST /sync/hash_list`
  - `POST /sync/push`
- v2 nodes add:
  - `POST /sync/handshake`
  - `POST /sync/pull`
  - `POST /sync/push_v2`

### Data payload schema
```json
{
  "sync_version": 2,
  "node_id": "hw:k10",
  "records": [ ... ],
  "hashes": [ ... ],
  "nonce": "<random>",
  "signature": "<hmac hex>"
}
```

### Migration notes
- Cycle-01 nodes continue to sync with v1 endpoints without change.
- v2 nodes should attempt `/sync/handshake` first; on 404, fall back to v1.
- During migration, hubs should accept both v1 and v2; mark `sync_diff` records with `mode=v1|v2`.

## Tests
- `tests/test_sync_signature.py`: validates HMAC signature generation/verification.
- `tests/test_sync_compat.py`: verifies v1 fallback behavior when handshake is unavailable.
- `tests/test_payload_hashes.py`: ensures hash canonicalization matches v1.

## Windows hub dashboard

### Features
- Live node registry with last-seen timestamps.
- Sync health panel (last handshake, mode, missing records count).
- Message flow list and simple rate indicator.

### Deployment
- Served from `/monitor_v2.html`.
- Uses `/ttdb/records` and `/sync/health` endpoints for data.
 - Sync key file `sync_key.txt` enables HMAC signatures for v2 endpoints.

## Artifacts
- `deliverables/cycle-02/src/ttdb_sync/sync_v2.py` (protocol + HMAC helpers)
- `deliverables/cycle-02/src/ttdb_sync/README.md`
- `deliverables/cycle-02/src/windows_hub/ttn_hub_v2.py` (v2 endpoints + health)
- `deliverables/cycle-02/src/windows_hub/static/monitor_v2.html`
- `deliverables/cycle-02/src/windows_hub/README.md`
- `deliverables/cycle-02/tests/`
