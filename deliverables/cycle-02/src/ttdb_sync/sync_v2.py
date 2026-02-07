import hashlib
import hmac
import json
import os
from typing import Dict, Any, Tuple


def canonical_json(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def hmac_signature(payload: Dict[str, Any], key: bytes) -> str:
    return hmac.new(key, canonical_json(payload), hashlib.sha256).hexdigest()


def verify_signature(payload: Dict[str, Any], key: bytes, signature: str) -> bool:
    expected = hmac_signature(payload, key)
    return hmac.compare_digest(expected, signature)


def build_handshake(node_id: str, capabilities: Dict[str, Any], key: bytes | None = None) -> Dict[str, Any]:
    payload = {
        "sync_version": 2,
        "node_id": node_id,
        "capabilities": capabilities,
        "nonce": os.urandom(8).hex(),
    }
    if key:
        payload["signature"] = hmac_signature(payload, key)
    return payload


def build_payload(node_id: str, records: list, hashes: list, key: bytes | None = None) -> Dict[str, Any]:
    payload = {
        "sync_version": 2,
        "node_id": node_id,
        "records": records,
        "hashes": hashes,
        "nonce": os.urandom(8).hex(),
    }
    if key:
        payload["signature"] = hmac_signature(payload, key)
    return payload


def verify_payload(payload: Dict[str, Any], key: bytes | None) -> Tuple[bool, str]:
    if not key:
        return True, "unauth"
    signature = payload.get("signature")
    if not signature:
        return False, "missing_signature"
    payload_copy = dict(payload)
    payload_copy.pop("signature", None)
    return verify_signature(payload_copy, key, signature), "hmac"
