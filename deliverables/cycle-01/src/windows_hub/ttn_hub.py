import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from common.ttdb import append_record, diff_missing, recent_hashes, load_records

DATA_DIR = Path("./data")
LOG_PATH = str(DATA_DIR / "ttdb.log")
MONITOR_PATH = Path(__file__).with_name("monitor.html")


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class TTNHubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/health":
            return json_response(self, 200, {"status": "ok"})
        if route == "/sync/recent":
            return json_response(self, 200, {"hashes": recent_hashes(LOG_PATH)})
        if route == "/ttdb/records":
            return json_response(self, 200, {"records": load_records(LOG_PATH)[-500:]})
        if route == "/monitor.html":
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
        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return json_response(self, 400, {"error": "invalid_json"})

        if route == "/sync/hash_list":
            hashes = data.get("hashes", [])
            missing = diff_missing(LOG_PATH, hashes)
            return json_response(self, 200, {"missing": missing})

        if route == "/sync/push":
            records = data.get("records", [])
            stored = 0
            for record in records:
                append_record(LOG_PATH, record)
                stored += 1
            return json_response(self, 200, {"stored": stored})

        json_response(self, 404, {"error": "not_found"})


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    server = HTTPServer(("0.0.0.0", 8080), TTNHubHandler)
    print("TTN hub listening on :8080")
    server.serve_forever()


if __name__ == "__main__":
    main()
