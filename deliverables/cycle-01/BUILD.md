# BUILD (cycle-01)

## Goal
Produce the primary artifact:
- `deliverables/cycle-01/output/toot-toot-engineering.wav`

## Proposed offline build pipeline (Python)
Because external TTS engines and DAWs may not be available in-repo, the most reproducible path is:
1. Generate a simple robotic “voice-like” source in Python (harmonic carrier + formant-ish filtering), *or* use an offline TTS if available.
2. Place/align phrase to a 65 BPM grid (bars 1–3, with the primary accent starting at beat 9).
3. Apply dub delay (tempo-synced) with filtered feedback and a stronger send at beat 9.
4. Export 44.1 kHz, 16-bit PCM WAV (or 48 kHz if preferred; choose one and document).

## Dependencies
- Preferred: `numpy`, `scipy` (for WAV IO and filters).
- If `scipy` is unavailable, fall back to Python’s built-in `wave` module and implement simple delay with numpy.

## Commands (to be used once scripts exist)
- Create/activate venv, install deps:
  - `python -m venv .venv`
  - `./.venv/Scripts/pip install -r requirements.txt`
- Run render:
  - `python deliverables/cycle-01/src/render_tte.py`

## Notes
- Sample rate target: **44,100 Hz** unless reviewer requests 48,000 Hz.
- Loudness/headroom target: limiter ceiling **-1 dBFS**.
- Timing reference: see `deliverables/cycle-01/STORYTELLER.md`.
