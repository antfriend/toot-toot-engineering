import json
import tempfile
import unittest
from pathlib import Path

import ttge_runner as runner


def seed_payload() -> dict:
    return {
        "identity": {"name": "TTGE-0", "role": "Self-Improving System Engineer"},
        "goedel_goal": {"description": "x", "invariant": True},
        "system_state": {"timestamp": "2026-02-08T00:00:00Z", "components": []},
        "hypotheses": [{"id": "GE-H-001", "claim": "x", "status": "active", "evidence": [], "tests": []}],
        "tests": [],
        "iterations": [],
        "self_modifications": [],
        "metrics": {"progress_score": 0, "goal_threshold": 10},
    }


class TestTTGERunner(unittest.TestCase):
    def test_first_step_sets_delta_and_progress(self) -> None:
        payload = seed_payload()
        updated = runner.simulate_one_step(payload)
        self.assertEqual(updated["metrics"]["progress_score"], 1)
        self.assertEqual(len(updated["tests"]), 1)
        self.assertEqual(len(updated["iterations"]), 1)

    def test_bell_history_appends(self) -> None:
        payload = seed_payload()
        payload["metrics"]["progress_score"] = 1
        payload["metrics"]["goal_threshold"] = 1
        payload["iterations"].append({"iteration_id": "0001"})

        with tempfile.TemporaryDirectory() as td:
            readme = Path(td) / "README_TTGE.md"
            readme.write_text("# TTGE\n\n## Bell Event History\n\n", encoding="utf-8")
            codex = Path(td) / "TTGE.Codex.ttdb.md"
            codex.write_text("# TTGE Codex\n", encoding="utf-8")

            runner.append_bell_history(str(readme), payload, str(codex))
            text = readme.read_text(encoding="utf-8")
            self.assertIn("Bell Event History", text)
            self.assertIn("codex TTGE.Codex.ttdb.md", text)


if __name__ == "__main__":
    unittest.main()
