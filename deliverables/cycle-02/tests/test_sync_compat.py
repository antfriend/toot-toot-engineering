from ttdb_sync.sync_v2 import build_handshake


def test_handshake_has_version_and_nonce():
    payload = build_handshake("node", {"hmac": False}, None)
    assert payload["sync_version"] == 2
    assert "nonce" in payload
