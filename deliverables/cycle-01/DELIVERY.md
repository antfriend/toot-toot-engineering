# DELIVERY (cycle-01)

## Primary deliverable
- `deliverables/cycle-01/output/toot-toot-engineering.wav`

## Additional artifacts
- Dry reference: `deliverables/cycle-01/output/toot-toot-engineering-dry.wav`
- Renderer source: `deliverables/cycle-01/src/render_tte.py`
- Build notes: `deliverables/cycle-01/BUILD.md`
- Beat map / performance script: `deliverables/cycle-01/STORYTELLER.md`
- Review notes: `deliverables/cycle-01/REVIEW.md`

## How to reproduce
From repo root:
1. Ensure Python is available.
2. Ensure dependencies are available (`numpy`, `scipy`).
3. Run:
   - `python deliverables/cycle-01/src/render_tte.py`

The script writes/overwrites:
- `deliverables/cycle-01/output/toot-toot-engineering.wav`
- `deliverables/cycle-01/output/toot-toot-engineering-dry.wav`

## Output characteristics (as rendered)
- Sample rate: 44,100 Hz
- Format: 16-bit PCM WAV
- Timing: 65 BPM; “Engineering” onset aligned to **beat 9** (Bar 3 Beat 1)
- FX: quarter-note dub delay with filtered feedback; stronger delay throw at beat 9

## Notes / caveats
- The voice is a fully offline robotic *voice-like synth* rather than a phoneme-based TTS engine. If strict intelligibility of the literal phrase is required, swap in an offline TTS voice and keep the timing + FX approach.
- Echo tail is intentionally long; can be shortened by reducing delay echoes/feedback.
