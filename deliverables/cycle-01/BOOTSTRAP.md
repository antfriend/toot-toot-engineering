# BOOTSTRAP (cycle-01)

## Prompt (from README.md)
Create a `.wav` file of primitively synthesized speech saying:

> "Humon rite good prompt!"

## Interpretation
We need to **produce an actual WAV audio file** containing synthesized speech of the given phrase. “Primitively synthesized” suggests something intentionally simple/retro, e.g.:
- formant-ish synthesis (simple vowel formants + noise for fricatives), or
- a minimal concatenative/phoneme approach using generated tones/noise,
- or a very small TTS engine in “robot voice” mode.

Given repo constraints (lightweight, reproducible), the best path is:
- **Python-only generation** of audio samples (standard library) to produce intelligible robotic speech.
- Store the resulting artifact under `deliverables/cycle-01/output/`.
- Include build notes and a small Toot Toot Engineering logo companion asset (SVG) in the cycle folder.

## Objectives (definition of done for this cycle)
1. Produce `deliverables/cycle-01/output/humon_rite_good_prompt.wav`.
2. Provide reproducible source code and notes to regenerate the WAV.
3. Validate the WAV:
   - correct sample rate/bit depth,
   - audible, not clipped,
   - phrase intelligible enough to recognize.
4. Package deliverables with a small Toot Toot Engineering logo asset.

## Proposed team composition
- **Storyteller**: establish intended “voice character” and cadence for the phrase; decide on stylization (robotic, playful).
- **Orchestrator**: adjust `PLAN.md` to include concrete production artifacts.
- **Core worker (Audio engineer)**: implement primitive speech synthesis and generate the WAV.
- **Reviewer**: verify artifact correctness and reproducibility; inspect WAV properties.
- **Delivery packager**: organize final outputs, write delivery notes, update `RELEASES.md`.
- **Retrospective/Bootstrap**: process improvements and next-cycle prompt suggestions.

## Recommended plan adjustments
1. In step 5 (“Core worker produces primary solution assets”), explicitly require:
   - `deliverables/cycle-01/src/synth_speech.py`
   - `deliverables/cycle-01/output/humon_rite_good_prompt.wav`
   - `deliverables/cycle-01/NOTES.md` with regeneration instructions
2. Add a lightweight validation subtask in Review:
   - check WAV metadata (duration, sample rate, channels)
3. Ensure Delivery includes a small logo asset in the cycle folder (do **not** pull from `HUMANS/` unless requested).

## Risks / constraints
- Pure “primitive” synthesis may be less intelligible than real TTS. We should optimize for **recognizability** over perfect phonetics.
- Prefer no external dependencies for maximum portability.

## Three suggested next-cycle prompts (human chooses one)
1. **“Add two more phrases and generate a mini ‘robot announcer’ demo reel WAV with a short intro/outro jingle.”**
2. **“Create an SVG ‘spectrogram poster’ of the generated phrase, and package it with the WAV.”**
3. **“Implement an alternate synthesis mode (whisper/alien) and output both WAVs plus a comparison report.”**
