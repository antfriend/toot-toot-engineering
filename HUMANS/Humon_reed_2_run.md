# Toot Toot Engineering (Runner)

This repo includes a local agent runner for the Toot Toot Engineering workflow.

## Quick start
1. Install dependencies.
   - `pip install -r requirements.txt`
   - or `pip install openai`
2. Set your API key:
   - `export OPENAI_API_KEY="..."` (macOS/Linux)
   - `setx OPENAI_API_KEY "..."` (Windows PowerShell)
3. Run the agent:
   - `python tte_agent.py` (or `python3 tte_agent.py`)
4. Run monitor + agent together (monitor logs to `%TEMP%\tte_monitor.log` on Windows or `/tmp/tte_monitor.log` on macOS/Linux):
   - `./run_tte.sh` (macOS/Linux)
   - `run_tte.bat` (Windows cmd)
   - `.\run_tte.ps1` (Windows PowerShell)

## Notes
- The workflow instructions live in `README.md` and `AGENTS.md`.
- The agent reads and operates inside the repo workspace.
- `tte_monitor.py` uses only the Python standard library, but it requires `tkinter` (installed via system packages, not pip).
  - macOS: `brew install python-tk`
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
  - Arch: `sudo pacman -S tk`
  - Windows: use the official python.org installer and ensure "tcl/tk and IDLE" is selected.

## Troubleshooting
- If you see "Missing OPENAI_API_KEY", confirm the env var is set in the shell you are using.
- If Python cannot import `openai`, rerun the install step or ensure you are in the right virtualenv.
