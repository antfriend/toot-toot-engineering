"""bbs/storage.py

Persistence and message model built on mpdb-lite.

We treat:
- Areas as nodes (fields include: id, area_name)
- Messages as nodes (fields include: id, author, timestamp, area_name, body)

Edges:
- in_area>@AREA_ID
- reply_to>@MSG_ID (optional)
- thread_root>@MSG_ID

This module keeps logic simple and file-based for MicroPython.
"""

import time

from . import mpdb_lite
from . import config


def _now():
    return int(time.time())


def _safe_read(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except OSError:
        return ""


def _safe_write(path, text):
    # Ensure directory exists if possible (MicroPython may not support makedirs)
    # Caller should create /bbs_data manually if needed.
    with open(path, "w") as f:
        f.write(text)


class DB:
    def __init__(self, path=None):
        self.path = path or config.DB_PATH
        self.nodes = []
        self._index = {}

    def load_db(self):
        txt = _safe_read(self.path)
        self.nodes = mpdb_lite.parse(txt) if txt else []
        self._reindex()
        return self

    def save_db(self):
        _safe_write(self.path, mpdb_lite.dumps(self.nodes))

    def _reindex(self):
        self._index = {}
        for n in self.nodes:
            self._index[n["_id"]] = n

    def find_node(self, node_id):
        return self._index.get(node_id)

    def insert_node(self, node):
        if node["_id"] in self._index:
            raise ValueError("node exists")
        self.nodes.append(node)
        self._index[node["_id"]] = node

    def update_node(self, node):
        self._index[node["_id"]] = node
        # also update in list
        for i in range(len(self.nodes)):
            if self.nodes[i]["_id"] == node["_id"]:
                self.nodes[i] = node
                return
        self.nodes.append(node)

    def add_edge(self, src, edge_type, dst):
        n = self.find_node(src)
        if not n:
            raise ValueError("missing src")
        edges = n.get("edges") or []
        edges.append((edge_type, dst))
        n["edges"] = edges
        self.update_node(n)

    def list_edges(self, src, edge_type=None):
        n = self.find_node(src)
        if not n:
            return []
        edges = n.get("edges") or []
        if edge_type is None:
            return list(edges)
        return [e for e in edges if e[0] == edge_type]

    # --- ID generation ---
    def new_id(self, prefix="@N"):
        # MicroPython-safe unique-ish id: timestamp + counter scan.
        base = "%s%d" % (prefix, _now())
        cand = base
        i = 0
        while cand in self._index:
            i += 1
            cand = "%s_%d" % (base, i)
        return cand

    # --- Domain operations ---
    def ensure_area(self, area_name):
        area_name = area_name.strip().lower()
        # find by field
        for n in self.nodes:
            f = n.get("fields") or {}
            if f.get("area_name") == area_name and f.get("kind") == "area":
                return n["_id"]
        nid = self.new_id(prefix="@AREA")
        ts = _now()
        node = {
            "_id": nid,
            "created": ts,
            "updated": ts,
            "fields": {
                "id": nid,
                "kind": "area",
                "area_name": area_name,
            },
            "edges": [],
        }
        self.insert_node(node)
        return nid

    def list_areas(self):
        areas = []
        for n in self.nodes:
            f = n.get("fields") or {}
            if f.get("kind") == "area":
                areas.append((n["_id"], f.get("area_name") or ""))
        areas.sort(key=lambda x: x[1])
        return areas

    def post_message(self, author, area_name, body, reply_to=None, draft=False):
        area_id = self.ensure_area(area_name)
        ts = _now()
        msg_id = self.new_id(prefix="@MSG")
        edges = [("in_area", area_id), ("thread_root", msg_id)]
        if reply_to:
            edges.append(("reply_to", reply_to))
            # Try to inherit thread_root from parent
            parent = self.find_node(reply_to)
            if parent:
                trs = self.list_edges(reply_to, "thread_root")
                if trs:
                    edges = [("in_area", area_id), ("thread_root", trs[0][1]), ("reply_to", reply_to)]
        fields = {
            "id": msg_id,
            "kind": "message",
            "author": author,
            "timestamp": str(ts),
            "area_name": area_name.strip().lower(),
            "body": body,
        }
        if draft:
            fields["status"] = "draft"
        node = {
            "_id": msg_id,
            "created": ts,
            "updated": ts,
            "fields": fields,
            "edges": edges,
        }
        self.insert_node(node)
        return msg_id

    def update_message_body(self, msg_id, body, finalize=True):
        n = self.find_node(msg_id)
        if not n:
            return False
        ts = _now()
        n["updated"] = ts
        f = n.get("fields") or {}
        f["body"] = body
        if finalize and f.get("status") == "draft":
            del f["status"]
        n["fields"] = f
        self.update_node(n)
        return True

    def list_messages_in_area(self, area_id=None, area_name=None, limit=20):
        if area_id is None and area_name is not None:
            # resolve
            area_name = area_name.strip().lower()
            for nid, nm in self.list_areas():
                if nm == area_name:
                    area_id = nid
                    break
        out = []
        for n in self.nodes:
            f = n.get("fields") or {}
            if f.get("kind") != "message":
                continue
            edges = n.get("edges") or []
            in_area = [e for e in edges if e[0] == "in_area"]
            if area_id is not None:
                if not in_area or in_area[0][1] != area_id:
                    continue
            out.append(n)
        # newest first by timestamp field (string int)
        out.sort(key=lambda n: int((n.get("fields") or {}).get("timestamp") or 0), reverse=True)
        return out[:limit]

    def list_thread(self, root_id):
        msgs = []
        for n in self.nodes:
            f = n.get("fields") or {}
            if f.get("kind") != "message":
                continue
            trs = self.list_edges(n["_id"], "thread_root")
            if trs and trs[0][1] == root_id:
                msgs.append(n)
        msgs.sort(key=lambda n: int((n.get("fields") or {}).get("timestamp") or 0))
        return msgs
