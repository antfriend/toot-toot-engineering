# DELIVERY (cycle-01)

## Primary deliverable
- `deliverables/cycle-01/output/humon_rite_good_prompt.wav`
  - primitively synthesized, robot-like speech of: **"Humon rite good prompt!"**

## Source / regeneration
- `deliverables/cycle-01/src/synth_speech.py`
- `deliverables/cycle-01/NOTES.md`

Regenerate from repo root:

```bash
python deliverables/cycle-01/src/synth_speech.py
```

## Companion asset (Toot Toot Engineering logo)
- `deliverables/cycle-01/toot-toot-logo.svg`

## Validation performed
- WAV metadata check: mono, 16-bit, 22050 Hz, ~1.41s duration.

## What to do if intelligibility needs improvement
Edit `deliverables/cycle-01/src/synth_speech.py`:
- adjust word pauses (`s_short`, `s_long`)
- tweak base pitch (`base`)
- modify vowel formants (`VOWELS` table)
- increase consonant noise bursts slightly

Then regenerate the WAV.
