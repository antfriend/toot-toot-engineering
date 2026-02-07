import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from common.ttdb import append_record, diff_missing, recent_hashes, load_records
from ttdb_sync.sync_v2 import build_handshake, verify_payload

DATA_DIR = Path("./data")
LOG_PATH = str(DATA_DIR / "ttdb.log")
MONITOR_PATH = Path(__file__).with_name("static") / "monitor_v2.html"

SYNC_STATE = {
    "last_handshake": None,
    "last_mode": None,
    "last_missing": 0,
}


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_json(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", "0"))
    payload = handler.rfile.read(length) if length else b"{}"
    return json.loads(payload)


def sync_key() -> bytes | None:
    key = (Path("./sync_key.txt").read_text(encoding="utf-8").strip()
           if Path("./sync_key.txt").exists() else "")
    return key.encode("utf-8") if key else None


class TTNHubV2Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/health":
            return json_response(self, 200, {"status": "ok"})
        if route == "/sync/recent":
            return json_response(self, 200, {"hashes": recent_hashes(LOG_PATH)})
        if route == "/ttdb/records":
            return json_response(self, 200, {"records": load_records(LOG_PATH)[-500:]})
        if route == "/sync/health":
            return json_response(self, 200, SYNC_STATE)
        if route == "/monitor_v2.html":
            if MONITOR_PATH.exists():
                body = MONITOR_PATH.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            return json_response(self, 404, {"error": "monitor_missing"})
        json_response(self, 404, {"error": "not_found"})

    def do_POST(self):
        route = urlparse(self.path).path
        try:
            data = read_json(self)
        except json.JSONDecodeError:
            return json_response(self, 400, {"error": "invalid_json"})

        if route == "/sync/handshake":
            key = sync_key()
            payload = build_handshake("hub", {"hmac": bool(key)}, key)
            SYNC_STATE["last_handshake"] = "ok"
            return json_response(self, 200, payload)

        if route == "/sync/hash_list":
            hashes = data.get("hashes", [])
            missing = diff_missing(LOG_PATH, hashes)
            SYNC_STATE["last_mode"] = "v1"
            SYNC_STATE["last_missing"] = len(missing)
            return json_response(self, 200, {"missing": missing})

        if route == "/sync/push":
            records = data.get("records", [])
            stored = 0
            for record in records:
                append_record(LOG_PATH, record)
                stored += 1
            SYNC_STATE["last_mode"] = "v1"
            return json_response(self, 200, {"stored": stored})

        if route == "/sync/push_v2":
            key = sync_key()
            valid, mode = verify_payload(data, key)
            if not valid:
                return json_response(self, 403, {"error": "invalid_signature"})
            records = data.get("records", [])
            stored = 0
            for record in records:
                append_record(LOG_PATH, record)
                stored += 1
            SYNC_STATE["last_mode"] = mode
            SYNC_STATE["last_missing"] = 0
            return json_response(self, 200, {"stored": stored})

        if route == "/sync/pull":
            key = sync_key()
            valid, mode = verify_payload(data, key)
            if not valid:
                return json_response(self, 403, {"error": "invalid_signature"})
            hashes = data.get("hashes", [])
            missing = diff_missing(LOG_PATH, hashes)
            SYNC_STATE["last_mode"] = mode
            SYNC_STATE["last_missing"] = len(missing)
            return json_response(self, 200, {"records": missing})

        json_response(self, 404, {"error": "not_found"})


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    server = HTTPServer(("0.0.0.0", 8081), TTNHubV2Handler)
    print("TTN hub v2 listening on :8081")
    server.serve_forever()


if __name__ == "__main__":
    main()
