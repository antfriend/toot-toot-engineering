# BOOTSTRAP (cycle-01)

## Prompt (from `README.md`)
Create a .wav file of a crisp, deep, robotic synthesized voice saying, "Toot Toot Engineering" in 4/4 time, 65 bpm, emphasis on the 9th beat, heavy dub style echo.

## Interpretation / success criteria
We need an **audio deliverable** (WAV) that contains a robotic synthesized voice phrase “Toot Toot Engineering” with a rhythmic delivery aligned to:
- **4/4 time** at **65 BPM**
- **Emphasis on the 9th beat** (i.e., downbeat of bar 3 if we count continuous quarter-note beats: 1–4 bar1, 5–8 bar2, **9** = bar3 beat1)
- **Heavy dub-style echo** (tempo-synced delay/feedback, filtered repeats)
- “Crisp, deep, robotic” tone (vocoder/bitcrush/formant-ish shaping, controlled sibilance)

**Definition of done (primary):** `deliverables/cycle-01/output/toot-toot-engineering.wav` exists, plays correctly, and has clear beat structure at 65 BPM with a notable accent at beat 9 and an audible dub echo tail.

## Complexity estimate
Moderate. Needs:
- A reproducible speech-synthesis approach.
- Beat/tempo alignment and timing control.
- Audio FX chain (delay/echo, EQ, saturation) with “dub” character.
- Validation (waveform/peak levels, duration, listening check notes).

## Recommended team composition (roles)
- **Bootstrap** (this doc): clarify intent, constraints, deliverables.
- **Storyteller**: convert prompt into a performance script (syllable timing, beat map, accent plan).
- **Orchestrator**: set repo structure + explicit filenames/pipeline.
- **Core worker (Audio engineer)**: generate voice, align to tempo grid, apply FX, export WAV.
- **Reviewer**: check tempo, beat-9 emphasis, intelligibility, echo style, and technical specs.
- **Delivery packager**: package WAV + build notes + sources; update releases.

(Optional if needed)
- **DSP helper**: if we need custom synthesis/delay scripting.

## Plan adjustments recommended
1. Add explicit production artifacts and structure:
   - `deliverables/cycle-01/src/` for scripts/project files
   - `deliverables/cycle-01/output/` for final wav(s)
   - `deliverables/cycle-01/BUILD.md` for exact commands/tools and parameters
2. Ensure the Core Worker step explicitly produces:
   - The WAV
   - The generation script/recipe used
3. Add a small “audio validation” checklist in the Reviewer step:
   - BPM/beat grid check
   - Beat 9 accent confirmation
   - Peak level / headroom (e.g., -1 dBFS ceiling)

## Risks / constraints / assumptions
- If we avoid external services, true TTS may not be available; a “voice-like” synth may be used instead.
- Exact meaning of “emphasis on the 9th beat” interpreted as a stronger delivery/accent at bar 3 beat 1.

## Retrospective (what to improve next time)
1. **Make dependencies explicit:** `requirements.txt` currently doesn’t declare `numpy`/`scipy` even though the renderer uses them. For reproducibility, add them (or vendor a pure-stdlib fallback).
2. **Add an intelligibility gate:** If the prompt demands literal spoken words, add a hard requirement for phoneme-based TTS (offline) and a short listening/confirmation step.
3. **Tighter deliverable spec:** document target duration (e.g., 6–10s) and whether mono/stereo is desired.
4. **Automated checks:** add a small script to print grid landmarks (beat times) and measure the energy spike around beat 9 to verify the “accent” objectively.

## Proposed next-cycle prompts (human must choose one)
1. **Remix pack:** “Create three stylistic variations (clean, gritty, dub-heavy) of the ‘Toot Toot Engineering’ vocal tag, each tempo-synced at 65 BPM, and package them as a mini sample pack.”
2. **Call-and-response:** “Generate a 2-bar robotic call ‘Toot Toot’ and a 2-bar response ‘Engineering’, with beat-9 drop and dub echo throws, delivered as stems + mixdown.”
3. **Audio logo video:** “Create a 5-second audio logo plus a simple waveform/oscilloscope animation video synchronized to the beat-9 emphasis.”
