#!/usr/bin/env python3
"""
ttge_runner.py - Minimal TTGE runner for a single-file TTDB seed.

Usage:
  python ttge_runner.py run --file TTGE.seed.ttdb.md --steps 1
  python ttge_runner.py status --file TTGE.seed.ttdb.md

Design goals:
- Zero third-party dependencies (Python 3.10 stdlib only)
- Append-only iteration log
- Deterministic, toy "progress" so you can see it move
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Tuple, List

from ttge import index_repo

JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_seed(path: str) -> Tuple[str, Dict[str, Any]]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    text = open(path, "r", encoding="utf-8").read()
    m = JSON_BLOCK_RE.search(text)
    if not m:
        raise ValueError("Could not find a ```json ... ``` block in the seed file.")
    payload = json.loads(m.group(1))
    return text, payload


def write_seed(path: str, original_text: str, payload: Dict[str, Any]) -> None:
    new_json = json.dumps(payload, indent=2, sort_keys=False)
    new_text = JSON_BLOCK_RE.sub(f"```json\n{new_json}\n```", original_text, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)


def next_iteration_id(payload: Dict[str, Any]) -> str:
    n = len(payload.get("iterations", [])) + 1
    return f"{n:04d}"


def ensure_append_only(payload: Dict[str, Any]) -> None:
    # Lightweight guardrails: forbid destructive edits to history if runner sees missing keys
    for k in ("iterations", "self_modifications"):
        if k not in payload or not isinstance(payload[k], list):
            payload[k] = []


def choose_active_hypothesis(payload: Dict[str, Any]) -> Dict[str, Any] | None:
    for h in payload.get("hypotheses", []):
        if h.get("status") == "active":
            return h
    return None


def propose_test_for_hypothesis(h: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    test_id = f"GE-T-{len(payload.get('tests', [])) + 1:03d}"
    test = {
        "id": test_id,
        "hypothesis": h["id"],
        "scenario": {
            "description": "Apply a small, local change implied by the hypothesis and measure iteration friction.",
            "duration_iterations": 3,
            "notes": "Toy runner: simulate expected utility via progress_score increments."
        },
        "success_criteria": [
            "progress_score increases",
            "no loss of traceability (iteration log remains append-only)",
            "hypothesis evidence updated"
        ],
        "status": "planned",
        "created_at": now_iso()
    }
    return test


def simulate_one_step(payload: Dict[str, Any]) -> Dict[str, Any]:
    ensure_append_only(payload)

    h = choose_active_hypothesis(payload)
    actions: List[str] = ["assessed_system", "reviewed_hypotheses_and_tests"]

    # If there is an active hypothesis without a planned/active test, create one.
    if h is not None:
        existing = set(h.get("tests", []))
        has_any = any(t for t in payload.get("tests", []) if t.get("hypothesis") == h["id"])
        if not has_any:
            test = propose_test_for_hypothesis(h, payload)
            payload.setdefault("tests", []).append(test)
            h.setdefault("tests", []).append(test["id"])
            actions.append(f"formalized_test:{test['id']}")
            delta = 1
        else:
            # Run a toy "scenario" step: mark first planned test as running or completed.
            related = [t for t in payload.get("tests", []) if t.get("hypothesis") == h["id"]]
            planned = next((t for t in related if t.get("status") == "planned"), None)
            running = next((t for t in related if t.get("status") == "running"), None)

            if planned:
                planned["status"] = "running"
                planned["started_at"] = now_iso()
                actions.append(f"ran_scenario:start:{planned['id']}")
                delta = 2
            elif running:
                running["status"] = "completed"
                running["completed_at"] = now_iso()
                actions.append(f"ran_scenario:complete:{running['id']}")
                delta = 3
                # Add evidence
                h.setdefault("evidence", []).append({
                    "type": "toy_metric",
                    "test_id": running["id"],
                    "observed": {"progress_delta": delta},
                    "timestamp": now_iso()
                })
            else:
                # If all tests completed, optionally propose a self-modification
                delta = 1
                sm_id = f"SM-{len(payload.get('self_modifications', [])) + 1:03d}"
                payload.setdefault("self_modifications", []).append({
                    "mod_id": sm_id,
                    "description": "Refined internal evaluation template for hypotheses (toy change).",
                    "justification": {"improves_goal_progress": True, "reason": "reduces ambiguity in test writing"},
                    "applied": True,
                    "timestamp": now_iso()
                })
                actions.append(f"self_modify_model:{sm_id}")
    else:
        delta = 1
        actions.append("no_active_hypothesis")

    payload.setdefault("metrics", {}).setdefault("progress_score", 0)
    payload["metrics"]["progress_score"] += int(delta)

    it = {
        "iteration_id": next_iteration_id(payload),
        "timestamp": now_iso(),
        "actions_taken": actions,
        "outcome": "progress" if delta > 0 else "stalled",
        "notes": "Toy TTGE runner step completed.",
        "progress_delta": int(delta),
        "progress_score": int(payload["metrics"]["progress_score"])
    }
    payload.setdefault("iterations", []).append(it)
    return payload


def goal_reached(payload: Dict[str, Any]) -> bool:
    m = payload.get("metrics", {})
    return int(m.get("progress_score", 0)) >= int(m.get("goal_threshold", 10))


def write_codex(seed_path: str, payload: Dict[str, Any]) -> str:
    # Exciting thing: mint a Codex that summarizes what was learned.
    codex_path = os.path.join(os.path.dirname(seed_path), "TTGE.Codex.ttdb.md")
    last_it = payload.get("iterations", [])[-1] if payload.get("iterations") else {}
    summary = {
        "codex": {
            "minted_at": now_iso(),
            "from_seed": os.path.basename(seed_path),
            "final_progress_score": payload.get("metrics", {}).get("progress_score", 0),
            "iterations": len(payload.get("iterations", [])),
            "active_hypotheses": [h["id"] for h in payload.get("hypotheses", []) if h.get("status") == "active"],
        },
        "principles_distilled": [
            "Append-only iteration logs preserve epistemic traceability.",
            "Hypotheses must be falsifiable and paired with at least one scenario test.",
            "Self-modifications require explicit, recorded justification."
        ],
        "last_iteration": last_it
    }

    md = "# TTGE Codex\n\n"
    md += "🔔 **The Bell Event:** goal threshold reached. The engine seals the moment into a portable Codex.\n\n"
    md += "```json\n" + json.dumps(summary, indent=2) + "\n```\n"
    md += "\n## What now?\n\n- Keep iterating in the seed file, or\n- Fork this Codex into a new seed for a new engine lineage.\n"

    with open(codex_path, "w", encoding="utf-8") as f:
        f.write(md)
    return codex_path


def append_bell_history(readme_path: str, payload: Dict[str, Any], codex_path: str) -> None:
    if not os.path.exists(readme_path):
        return
    text = open(readme_path, "r", encoding="utf-8").read()
    header = "## Bell Event History"
    if header not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n" + header + "\n\n"
    entry = (
        f"- {now_iso()} | progress "
        f"{payload.get('metrics', {}).get('progress_score', 0)} / "
        f"{payload.get('metrics', {}).get('goal_threshold', 10)} | "
        f"iterations {len(payload.get('iterations', []))} | "
        f"codex {os.path.basename(codex_path)}"
    )
    lines = text.splitlines()
    out: List[str] = []
    inserted = False
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if lines[i].strip() == header:
            out.append("")
            out.append(entry)
            inserted = True
            i += 1
            # Skip any existing blank line immediately after header to keep spacing neat.
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        i += 1
    if not inserted:
        out.append("")
        out.append(header)
        out.append("")
        out.append(entry)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out).rstrip() + "\n")


def update_graph(payload: Dict[str, Any], root: str) -> None:
    nodes = index_repo.build_nodes(root)
    edges = index_repo.build_edges(nodes)
    payload["graph"] = {
        "nodes": nodes,
        "edges": edges,
        "indexed_at": now_iso(),
        "root": os.path.abspath(root),
    }
    payload.setdefault("system_state", {}).setdefault("repo_snapshot", {})
    payload["system_state"]["repo_snapshot"]["paths_indexed"] = len(nodes)


def cmd_status(args: argparse.Namespace) -> int:
    _, payload = read_seed(args.file)
    m = payload.get("metrics", {})
    print(f"Seed: {args.file}")
    print(f"Role: {payload.get('identity', {}).get('role')}")
    print(f"Progress: {m.get('progress_score', 0)} / {m.get('goal_threshold', 10)}")
    print(f"Hypotheses: {len(payload.get('hypotheses', []))} (active: {sum(1 for h in payload.get('hypotheses', []) if h.get('status')=='active')})")
    print(f"Tests: {len(payload.get('tests', []))}")
    print(f"Iterations: {len(payload.get('iterations', []))}")
    graph = payload.get("graph", {})
    print(f"Graph nodes: {len(graph.get('nodes', []))}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    text, payload = read_seed(args.file)
    update_graph(payload, os.path.dirname(args.file) or ".")

    steps = max(1, int(args.steps))
    for _ in range(steps):
        payload = simulate_one_step(payload)

    write_seed(args.file, text, payload)

    if goal_reached(payload):
        codex = write_codex(args.file, payload)
        append_bell_history(os.path.join(os.path.dirname(args.file), "README_TTGE.md"), payload, codex)
        print(f"🔔 Bell Event: goal reached. Codex minted at: {codex}")
    else:
        print(f"Ran {steps} step(s). Progress is now {payload.get('metrics', {}).get('progress_score')} / {payload.get('metrics', {}).get('goal_threshold')}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Minimal TTGE runner (single-file TTDB seed).")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="Show current TTGE status.")
    p_status.add_argument("--file", required=True, help="Path to TTGE.seed.ttdb.md")
    p_status.set_defaults(func=cmd_status)

    p_run = sub.add_parser("run", help="Run one or more TTGE steps.")
    p_run.add_argument("--file", required=True, help="Path to TTGE.seed.ttdb.md")
    p_run.add_argument("--steps", default="1", help="Number of steps to run (default 1).")
    p_run.set_defaults(func=cmd_run)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
