

## Toot Toot Engineering
 can make an AI agent system (like yours, human!) work better by externalizing structure, intent, and sequencing that would otherwise live implicitly inside prompts, code, or runtime state.

![feature-side-by-side](feature-side-by-side.png)


## What is different
 about toot-toot engineering is that it is
 - free
 - open-source
 - plain text files in English
   
 No runtime dependencies, no libraries. Just this, you are looking at it.   
 The magic is that there is no magic to this, just read the whole thing as a human or an agent, and you'll understand everything.

## What’s novel is not the components.
It’s the placement.

Most AI tooling tries to improve things:

inside the model

inside prompts

inside agents

inside orchestration layers

Toot Toot Engineering moves improvement outside all of that.   

![how toot toot engineering helps AI agents](how-toot-toot-engineering-helps.png)


## Who This Is For

Toot-Toot Engineering is designed for people working in multi-step, intention-heavy processes who want clarity, reliability, and repeatability when collaborating with AI systems.

It is especially useful for:

- [Engineers](./AUDIENCE.md#engineers) building reviewable, Git-native workflows  
- [Researchers](./AUDIENCE.md#researchers) designing reproducible AI-assisted methods  
- [Makers](./AUDIENCE.md#makers) iterating across experiments and build sessions  
- [Storytellers](./AUDIENCE.md#storytellers) maintaining continuity across creative phases  

Across all of these groups, TTE helps externalize structure and intent so both humans and AI systems can work more effectively together.



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
