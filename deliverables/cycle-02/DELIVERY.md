# DELIVERY (cycle-02)

## Primary deliverable
- `deliverables/cycle-02/output/toot-toot-engineering.wav`

## Additional artifacts
- Dry reference: `deliverables/cycle-02/output/toot-toot-engineering-dry.wav`
- Renderer source: `deliverables/cycle-02/src/render_tte.py`
- Build notes: `deliverables/cycle-02/BUILD.md`
- Beat map / performance script: `deliverables/cycle-02/STORYTELLER.md`
- Review notes: `deliverables/cycle-02/REVIEW.md`

## How to reproduce
From repo root:
1. Ensure Python 3 is available.
2. Run:
   - `python3 deliverables/cycle-02/src/render_tte.py`

The script writes/overwrites:
- `deliverables/cycle-02/output/toot-toot-engineering.wav`
- `deliverables/cycle-02/output/toot-toot-engineering-dry.wav`

## Output characteristics (as rendered)
- Sample rate: 44,100 Hz
- Format: 16-bit PCM WAV
- Timing: 130 BPM; “Engineering” onset aligned to **beat 9** (Bar 3 Beat 1)
- FX: quarter-note dub delay with filtered feedback; stronger delay throw at beat 9

## Notes / caveats
- The voice is an offline robotic *voice-like synth* rather than a phoneme-based TTS engine.
- Echo tail is intentionally long; can be shortened by reducing `tail_s` or delay echoes.
