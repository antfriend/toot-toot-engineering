# STORYTELLER (cycle-01)

## Creative intent: the “primitive voice”
The phrase **“Humon rite good prompt!”** reads like a proud, slightly goofy factory-floor chant: misspelled on purpose, enthusiastic, and a bit mechanical.

We want the audio to feel:
- **Robot-earnest** (sincere praise)
- **Lo-fi / early-synth** (simple tones/noise, not naturalistic)
- **Legible** (the words should be recognizable)

## Performance direction
**Tempo / cadence**
- Medium tempo, with clear word breaks:
  - “HU-mon” (tiny pause)
  - “rite” (tiny pause)
  - “good” (tiny pause)
  - “prompt!” (slightly longer, emphasized)

**Prosody**
- Slight upward inflection across the sentence.
- Strong emphasis on **“prompt!”** (higher pitch and/or louder).

## Audio character specification (for the Core worker)
A good “primitive” but intelligible approach:
- Use **voiced segments** as a simple saw/square-ish tone (fundamental ~120–180 Hz).
- Shape syllables with **very simple formant-ish filtering** (even 2–3 broad resonances approximated crudely).
- Use **noise bursts** for consonants like:
  - /p/ (brief silence then burst)
  - /t/ (burst)
  - /k/ (burst)
  - /m/ and /n/ can be voiced but lower/softer.
- Keep dynamics conservative to avoid clipping; leave headroom.

If full phoneme modeling is too heavy, a fallback that still meets “primitive”:
- **Concatenate per-syllable tones** with amplitude envelopes and occasional noise onsets.
- Aim for a classic “Speak & Spell-ish” vibe.

## Suggested syllable breakdown
This is a pragmatic breakdown for synthesis timing:
- HU (voiced)
- mon (voiced, a little nasal)
- rite (voiced + light noise onset)
- good (voiced)
- prompt (voiced, with stronger onset and a crisp ending)

## Acceptance criteria for narrative/character
- Listener can identify at least: “... good prompt!”
- Overall feeling: cheerful machine praising the human.

## Notes for packaging
If we later generate a companion visual (optional), it should resemble a simple factory label: bold text, minimal lines, lo-fi aesthetic.
