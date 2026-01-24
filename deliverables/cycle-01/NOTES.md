# NOTES (cycle-01)

## Goal
Generate a `.wav` file of primitively synthesized speech saying:

> "Humon rite good prompt!"

## How to regenerate
From repo root:

```bash
python deliverables/cycle-01/src/synth_speech.py
```

This writes:
- `deliverables/cycle-01/output/humon_rite_good_prompt.wav`

## Implementation notes
- Pure-Python (standard library only): `wave`, `struct`, `math`, `random`.
- Synthesis approach:
  - a cheap saw-like source (few harmonics)
  - crude vowel coloring via 3 parallel resonators (approx. formant-ish)
  - small noise bursts for consonant onsets
  - conservative normalization to prevent clipping

## Expected properties
- Sample rate: 22050 Hz
- Channels: mono
- Bit depth: 16-bit PCM
- Duration: ~1–2 seconds (varies slightly with parameters)

