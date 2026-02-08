#!/usr/bin/env python3
"""
Minimal TTGE repo indexer.

Scans for .md (Documents) and .py (Tools) and emits TTDB graph nodes/edges.
This is a stub meant to be expanded with richer parsing later.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Tuple


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: str) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip common ignore dirs.
        dirnames[:] = [d for d in dirnames if d not in {".git", ".venv", "__pycache__"}]
        for name in filenames:
            yield os.path.join(dirpath, name)


def classify_node(path: str) -> Tuple[str, str] | None:
    if path.endswith(".md"):
        return "Document", f"DOC:{os.path.relpath(path)}"
    if path.endswith(".py"):
        return "Tool", f"TOOL:{os.path.relpath(path)}"
    return None


def build_nodes(root: str) -> List[Dict]:
    nodes: List[Dict] = []
    for path in iter_files(root):
        info = classify_node(path)
        if not info:
            continue
        node_type, node_id = info
        rel = os.path.relpath(path, root)
        nodes.append(
            {
                "id": node_id.replace("\\", "/"),
                "type": node_type,
                "props": {
                    "source_path": rel.replace("\\", "/"),
                    "checksum": sha256_file(path),
                    "last_seen": now_iso(),
                    "status": "active",
                },
            }
        )
    return nodes


def build_edges(nodes: List[Dict]) -> List[Dict]:
    # Stub: no semantic edges yet.
    return []


def main() -> int:
    p = argparse.ArgumentParser(description="TTGE repo indexer (nodes/edges stub).")
    p.add_argument("--root", default=".", help="Repo root to scan.")
    p.add_argument("--out", default="", help="Optional output JSON file.")
    args = p.parse_args()

    nodes = build_nodes(args.root)
    edges = build_edges(nodes)
    graph = {"nodes": nodes, "edges": edges, "indexed_at": now_iso(), "root": os.path.abspath(args.root)}
    text = json.dumps(graph, indent=2, sort_keys=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
