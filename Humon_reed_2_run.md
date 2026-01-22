# Toot Toot Engineering (Runner)

This repo includes a local agent runner that executes the Toot Toot Engineering workflow.

## Quick start
1. Install dependencies (at least `openai` for Python).
   - `pip install -r requirements.txt`
   - or `pip install openai`
2. Set your API key:
   - `export OPENAI_API_KEY="..."` (macOS/Linux)
   - `setx OPENAI_API_KEY "..."` (Windows PowerShell)
3. Run the agent:
   - `python tte_agent.py`

## Notes
- The workflow instructions live in `tte/README.md`.
- The agent reads and operates inside the repo workspace.

## Troubleshooting
- If you see "Missing OPENAI_API_KEY", confirm the env var is set in the shell you are using.
- If Python cannot import `openai`, rerun the install step or ensure you are in the right virtualenv.
