# TTDB Sync v2

## Overview
Sync v2 adds a versioned handshake and optional HMAC integrity. It remains backward compatible with v1 hash-list sync.

## Security model
- Optional HMAC-SHA256 using a shared secret (`sync_key.txt`).
- If the key is missing, nodes operate in unauthenticated mode and log `mode=unauth` in `sync_diff` records.
- Signatures cover canonical JSON payloads (sorted keys, stable separators).

## Backward compatibility
- v2 nodes must accept v1 endpoints and payloads.
- v2 nodes attempt `/sync/handshake` and fall back to v1 if unavailable.

## Migration notes
- Deploy hub v2 first to support both versions.
- Roll out v2 nodes gradually; mixed networks should converge.
