# CORE_WORKER_NOTES (cycle-01)

## What was produced
- `deliverables/cycle-01/output/toot-toot-engineering.wav` (final, with dub delay)
- `deliverables/cycle-01/output/toot-toot-engineering-dry.wav` (dry reference)
- `deliverables/cycle-01/src/render_tte.py` (offline renderer)

## How the prompt requirements were addressed
- **Robotic synthesized voice**: implemented as a fully offline, voice-like synth (harmonic carrier through multiple bandpass filters + noise edge + bitcrush). This is not a natural-language TTS engine, but it produces a robotic, vowel-ish “spoken tag” impression.
- **4/4 at 65 BPM**: events are placed on a quarter-note grid using `q = 60/bpm`.
- **Emphasis on the 9th beat**: the “Engineering” onset starts at beat 9 (Bar 3 Beat 1), and the first syllable segment is given higher gain and a stronger delay send.
- **Heavy dub-style echo**: tempo-synced quarter-note delay with feedback and filtered repeats; send automation boosts the delay throw at beat 9.

## Technical specs
- Sample rate: **44,100 Hz**
- Format: **16-bit PCM WAV**
- Measured duration: ~25.15s (includes long echo tail)
- Peak: ~0.89 FS (~-1 dBFS ceiling was applied; actual peak slightly below ceiling)

## Known limitations / future improvement ideas
- Because this is not real phoneme-based TTS, intelligibility of the exact words may be more “tag-like” than literal. If strict intelligibility is required, we should integrate an offline TTS voice (if available) and then apply the same timing + FX chain.
- The echo tail is long; reviewer can request a tighter tail (~8–12s total).
