"""bbs/mpdb_lite.py

A MicroPython-friendly, MMPDB-inspired record format.

Format (very small):
- Records are separated by blank lines.
- First line is a header:
    @ID | created:1700000000 | updated:1700000000 | relates:type>@OTHER,type2>@OTHER2
- Following lines are key: value pairs.

This module provides parsing and serialization helpers.

Note: Host-side tests can import this module under CPython.
"""


def _strip(s):
    return s.strip() if s is not None else s


def parse_relates_token(token):
    # token: "type>@ID"
    token = token.strip()
    if not token:
        return None
    if ">@" not in token:
        return None
    edge_type, dst = token.split(">@", 1)
    return _strip(edge_type), "@" + _strip(dst)


def parse_header_line(line):
    # "@ID | created:.. | updated:.. | relates:..."
    parts = [p.strip() for p in line.split("|")]
    rec_id = parts[0]
    meta = {"_id": rec_id, "created": None, "updated": None, "relates": []}
    for p in parts[1:]:
        if p.startswith("created:"):
            meta["created"] = int(p.split(":", 1)[1].strip())
        elif p.startswith("updated:"):
            meta["updated"] = int(p.split(":", 1)[1].strip())
        elif p.startswith("relates:"):
            rel = p.split(":", 1)[1].strip()
            if rel:
                for tok in rel.split(","):
                    parsed = parse_relates_token(tok)
                    if parsed:
                        meta["relates"].append(parsed)
    return meta


def parse(text):
    """Parse mpdb-lite text into a list of node dicts.

    Notes:
    - We treat each record as starting with a header line that begins with '@'.
    - Body fields may contain blank lines; therefore we DO NOT split records by '\n\n'.
      Instead, we scan linearly and start a new record on each '@' header.

    Node dict shape:
    {
      '_id': '@MSG1',
      'created': 170..., 'updated': 170...,
      'fields': {...},
      'edges': [('in_area','@AREA1'), ...]
    }
    """
    nodes = []
    text = (text or "").replace("\r\n", "\n")
    lines = text.split("\n")

    cur = None

    def flush():
        nonlocal cur
        if cur is not None:
            nodes.append(cur)
            cur = None

    for ln in lines:
        if ln.startswith("@"):
            flush()
            meta = parse_header_line(ln.strip())
            cur = {
                "_id": meta["_id"],
                "created": meta["created"],
                "updated": meta["updated"],
                "fields": {},
                "edges": meta["relates"],
            }
            continue

        if cur is None:
            continue

        # skip pure blank separators
        if not ln.strip():
            continue

        if ":" not in ln:
            continue
        k, v = ln.split(":", 1)
        cur["fields"][_strip(k)] = v.lstrip()

    flush()
    return nodes


def _fmt_relates(edges):
    if not edges:
        return ""
    toks = []
    for edge_type, dst in edges:
        toks.append("%s>%s" % (edge_type, dst))
    return "relates:" + ",".join(toks)


def dumps_node(node):
    """Serialize one node dict to text block."""
    parts = [node.get("_id")]
    created = node.get("created")
    updated = node.get("updated")
    if created is not None:
        parts.append("created:%d" % int(created))
    if updated is not None:
        parts.append("updated:%d" % int(updated))
    rel = _fmt_relates(node.get("edges") or [])
    if rel:
        parts.append(rel)
    header = " | ".join(parts)

    lines = [header, ""]
    fields = node.get("fields") or {}
    # stable ordering for readability
    for k in sorted(fields.keys()):
        lines.append("%s: %s" % (k, fields[k]))
    return "\n".join(lines)


def dumps(nodes):
    return "\n\n".join([dumps_node(n) for n in nodes]) + "\n"
