try:
    import ujson as json
except ImportError:  # pragma: no cover - CPython fallback
    import json

try:
    import utime as time
except ImportError:  # pragma: no cover - CPython fallback
    import time

try:
    import ubinascii as binascii
except ImportError:  # pragma: no cover - CPython fallback
    import binascii

try:
    import urandom as random
except ImportError:  # pragma: no cover - CPython fallback
    import os

    class _Random:
        @staticmethod
        def urandom(n):
            return os.urandom(n)

    random = _Random()


def _iso_ts():
    tm = time.gmtime()
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])


def _new_id():
    return binascii.hexlify(random.urandom(16)).decode("ascii")


class TTNMessage:
    def __init__(self, msg_id, from_name, from_ip, to, ts, text):
        self.msg_id = msg_id
        self.from_name = from_name
        self.from_ip = from_ip
        self.to = to
        self.ts = ts
        self.text = text

    @staticmethod
    def new(from_name, from_ip, to, text):
        return TTNMessage(_new_id(), from_name, from_ip, to, _iso_ts(), text)

    def to_json_bytes(self):
        return json.dumps(
            {
                "msg_id": self.msg_id,
                "from_name": self.from_name,
                "from_ip": self.from_ip,
                "to": self.to,
                "ts": self.ts,
                "text": self.text,
            }
        ).encode("utf-8")

    @staticmethod
    def from_json_bytes(data):
        obj = json.loads(data.decode("utf-8"))
        for key in ("msg_id", "from_name", "from_ip", "to", "ts", "text"):
            if key not in obj:
                raise ValueError("Missing field: %s" % key)
        return TTNMessage(
            str(obj["msg_id"]),
            str(obj["from_name"]),
            str(obj["from_ip"]),
            str(obj["to"]),
            str(obj["ts"]),
            str(obj["text"]),
        )
