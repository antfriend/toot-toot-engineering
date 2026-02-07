from ttdb_sync.sync_v2 import hmac_signature, verify_signature


def test_hmac_signature_roundtrip():
    payload = {"sync_version": 2, "node_id": "test", "nonce": "abc"}
    key = b"secret"
    sig = hmac_signature(payload, key)
    assert verify_signature(payload, key, sig)
