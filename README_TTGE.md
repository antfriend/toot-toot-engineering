# TTGE Drop-In (Minimal Toot Toot Gödel Engine)

This is a tiny, runnable seed for a **Self-Improving System Engineer** that stores *everything* in one TTDB-style Markdown file.

## Files

- `TTGE.seed.ttdb.md`  
  The whole engine state in a single JSON payload embedded in Markdown.

- `ttge_runner.py`  
  A zero-dependency Python 3.10 runner that reads the seed, appends iterations, creates tests, and (eventually) mints a Codex.

## Quick start

From the folder containing these files:

```bash
python ttge_runner.py status --file TTGE.seed.ttdb.md
python ttge_runner.py run --file TTGE.seed.ttdb.md --steps 1
python ttge_runner.py run --file TTGE.seed.ttdb.md --steps 5
python ttge_runner.py status --file TTGE.seed.ttdb.md
```

When `progress_score >= goal_threshold`, the runner triggers the **Bell Event** 🔔 and writes:

- `TTGE.Codex.ttdb.md`

## Bell Event History

This section is append-only. Each Bell Event adds a timestamped line here.

## How to make it less toy

Open `TTGE.seed.ttdb.md` and start editing:

- Add hypotheses
- Add concrete tests for those hypotheses
- Replace the toy metric in `ttge_runner.py` with checks that:
  - review bootstrap retrospectives
  - test hypotheses (not required to be Python tests; agentic checks are allowed)

If you want, tell me what your current TTE repo structure looks like (folders + key files) and I’ll wire the runner to real signals.

The unifying goal for TTGE is to ring a Bell Event recording a Toot Toot Engineering System Self Improvement. Each one in the history is a trophy of self-improvement.

