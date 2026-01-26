# storage.py - mpdb-lite persistence helpers
#
# Design goals:
# - Single append-friendly text file.
# - Records are markdown-ish blocks.
# - Typed edges stored in header "relates:" as comma-separated tokens: type>@TARGET_ID
# - Fields stored as "key: value" lines.
# - Minimal parsing for MicroPython.

import time


def _now():
    return int(time.time())


def ensure_db_dirs(db_path):
    # Create parent directories if missing (MicroPython friendly).
    parts = db_path.split("/")
    if len(parts) <= 1:
        return
    path = ""
    for p in parts[:-1]:
        path = p if path == "" else (path + "/" + p)
        try:
            import os
            os.mkdir(path)
        except OSError:
            pass


def load_db_text(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except OSError:
        return ""


def _split_records(text):
    # Records are separated by a blank line + '---' line + blank line in the reference MMPDB.
    # For mpdb-lite we accept either '---' separators or just double-newline before an '@ID' line.
    recs = []
    cur = []
    for line in text.splitlines():
        if line.strip() == "---":
            if cur:
                recs.append("\n".join(cur).strip("\n"))
                cur = []
            continue
        cur.append(line)
    if cur:
        recs.append("\n".join(cur).strip("\n"))
    # filter empties
    return [r for r in recs if r.strip()]


def _parse_header_line(line):
    # Example:
    # @LAT10LON5 | created:1700002000 | updated:1700002000 | relates:in_area>@LAT0LON1,thread_root>@LAT10LON5
    parts = [p.strip() for p in line.split("|")]
    if not parts:
        return None
    rid = parts[0].strip()
    meta = {"id": rid, "created": None, "updated": None, "relates": []}
    for p in parts[1:]:
        if p.startswith("created:"):
            meta["created"] = int(p.split(":", 1)[1])
        elif p.startswith("updated:"):
            meta["updated"] = int(p.split(":", 1)[1])
        elif p.startswith("relates:"):
            rels = p.split(":", 1)[1].strip()
            if rels:
                meta["relates"] = [t.strip() for t in rels.split(",") if t.strip()]
    return meta


def _parse_fields(lines):
    fields = {}
    for ln in lines:
        if ":" in ln:
            k, v = ln.split(":", 1)
            fields[k.strip()] = v.lstrip()
    return fields


def load_db(path):
    text = load_db_text(path)
    nodes = {}
    records = _split_records(text)
    for rec in records:
        lines = [l.rstrip("\r") for l in rec.splitlines() if l.strip()]
        if not lines:
            continue
        header = lines[0].strip()
        if not header.startswith("@"):
            continue
        meta = _parse_header_line(header)
        fields = _parse_fields(lines[1:])
        rid = meta["id"]
        node = {
            "id": rid,
            "created": meta.get("created"),
            "updated": meta.get("updated"),
            "relates": meta.get("relates") or [],
        }
        for k in fields:
            node[k] = fields[k]
        nodes[rid] = node
    return nodes


def find_node(nodes, rid):
    return nodes.get(rid)


def _format_node(node):
    created = node.get("created") or _now()
    updated = node.get("updated") or created
    relates = node.get("relates") or []
    header = "%s | created:%d | updated:%d" % (node["id"], created, updated)
    if relates:
        header += " | relates:" + ",".join(relates)

    # stable field order for readability
    field_keys = [
        "id",
        "author",
        "timestamp",
        "area_name",
        "body",
    ]
    extras = [k for k in node.keys() if k not in ("created", "updated", "relates") and k not in field_keys]
    lines = [header, ""]
    for k in field_keys + sorted(extras):
        if k in node and node[k] is not None:
            lines.append("%s: %s" % (k, node[k]))
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def insert_node(path, node):
    ensure_db_dirs(path)
    node = dict(node)
    now = _now()
    node.setdefault("created", now)
    node.setdefault("updated", now)
    with open(path, "a") as f:
        f.write(_format_node(node))


def update_node(path, node):
    # Simple approach: append an updated version. Latest wins on load.
    node = dict(node)
    node["updated"] = _now()
    insert_node(path, node)


def add_edge(nodes, src, edge_type, dst):
    node = nodes.get(src)
    if not node:
        return False
    token = "%s>@%s" % (edge_type, dst.lstrip("@"))
    rels = node.get("relates") or []
    if token not in rels:
        rels.append(token)
        node["relates"] = rels
    return True


def list_edges(nodes, src, edge_type=None):
    node = nodes.get(src)
    if not node:
        return []
    out = []
    for tok in (node.get("relates") or []):
        if ">@" not in tok:
            continue
        et, dst = tok.split(">@", 1)
        dst = "@" + dst
        if edge_type is None or et == edge_type:
            out.append((et, dst))
    return out


def list_messages_in_area(nodes, area_id=None, area_name=None):
    # Filter nodes that look like messages: have body and author.
    out = []
    for rid, n in nodes.items():
        if "body" not in n:
            continue
        if area_id is not None:
            # match via relates token
            want = "in_area>%s" % area_id
            if not any(t.startswith("in_area>") and (">" + area_id) in ("">" + t.split(">", 1)[1]) for t in (n.get("relates") or [])):
                # simpler: accept both in_area>@ID and in_area>ID forms
                if not any(t.startswith("in_area>") and ("@" + t.split(">@", 1)[1]) == area_id for t in (n.get("relates") or [])):
                    pass
        if area_name is not None and n.get("area_name") != area_name:
            continue
        out.append(n)

    # sort by timestamp/created
    def keyf(m):
        try:
            return int(m.get("timestamp") or m.get("created") or 0)
        except Exception:
            return 0

    out.sort(key=keyf)
    return out


def list_thread(nodes, root_id):
    out = []
    for rid, n in nodes.items():
        if "body" not in n:
            continue
        if any(t == ("thread_root>%s" % root_id) or t == ("thread_root>@%s" % root_id.lstrip("@")) for t in (n.get("relates") or [])):
            out.append(n)
    out.sort(key=lambda m: int(m.get("timestamp") or m.get("created") or 0))
    return out
