import json
import hashlib
import time
from pathlib import Path
from typing import Iterable, Dict, List


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def stable_hash(record: Dict) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def append_record(log_path: str, record: Dict) -> str:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = dict(record)
    record.setdefault("time_utc", utc_now())
    record_hash = stable_hash(record)
    record["_hash"] = record_hash
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record_hash


def load_records(log_path: str) -> List[Dict]:
    path = Path(log_path)
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def recent_hashes(log_path: str, limit: int = 200) -> List[str]:
    records = load_records(log_path)
    hashes = [rec.get("_hash") or stable_hash(rec) for rec in records[-limit:]]
    return hashes


def diff_missing(local_log: str, peer_hashes: Iterable[str]) -> List[Dict]:
    peer_set = set(peer_hashes)
    missing = []
    for record in load_records(local_log):
        record_hash = record.get("_hash") or stable_hash(record)
        if record_hash not in peer_set:
            missing.append(record)
    return missing


def compact(log_path: str, snapshot_path: str, max_records: int = 5000) -> int:
    records = load_records(log_path)
    if not records:
        return 0
    keep = records[-max_records:]
    Path(snapshot_path).parent.mkdir(parents=True, exist_ok=True)
    with Path(snapshot_path).open("w", encoding="utf-8") as handle:
        json.dump({"records": keep, "compacted_at": utc_now()}, handle, indent=2, sort_keys=True)
    return len(keep)
