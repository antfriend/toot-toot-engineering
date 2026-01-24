"""Primitive speech synth -> WAV

Generates a lo-fi, robot-earnest rendition of:

    "Humon rite good prompt!"

This is intentionally "primitive": it approximates syllables using
simple oscillators (saw-ish) plus noise bursts for consonant attacks,
with a light resonant filtering to suggest vowel color.

Usage:
    python deliverables/cycle-01/src/synth_speech.py

Output:
    deliverables/cycle-01/output/humon_rite_good_prompt.wav
"""

from __future__ import annotations

import math
import os
import random
import struct
import wave


SR = 22050


def clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def one_pole_lp(x: float, y_prev: float, a: float) -> float:
    # y[n] = (1-a)*x + a*y[n-1]
    return (1.0 - a) * x + a * y_prev


def resonator_process(x: float, st: dict, f_hz: float, q: float) -> float:
    # simple biquad bandpass-ish resonator (RBJ), fed with x
    w0 = 2.0 * math.pi * f_hz / SR
    alpha = math.sin(w0) / (2.0 * q)

    b0 = alpha
    b1 = 0.0
    b2 = -alpha
    a0 = 1.0 + alpha
    a1 = -2.0 * math.cos(w0)
    a2 = 1.0 - alpha

    b0 /= a0
    b1 /= a0
    b2 /= a0
    a1 /= a0
    a2 /= a0

    x1, x2 = st["x1"], st["x2"]
    y1, y2 = st["y1"], st["y2"]

    y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2

    st["x2"], st["x1"] = x1, x
    st["y2"], st["y1"] = y1, y
    return y


def adsr(n: int, a: int, d: int, s: float, r: int) -> list[float]:
    # very simple envelope for a segment of length n
    env = [0.0] * n
    for i in range(n):
        if i < a:
            env[i] = i / max(1, a)
        elif i < a + d:
            t = (i - a) / max(1, d)
            env[i] = 1.0 + t * (s - 1.0)
        elif i < n - r:
            env[i] = s
        else:
            t = (i - (n - r)) / max(1, r)
            env[i] = s * (1.0 - t)
    return env


def sawish(phase: float) -> float:
    # a cheap bandlimited-ish saw approximation using a few harmonics
    # intentionally lo-fi
    v = 0.0
    for k in (1, 2, 3, 4, 5):
        v += (1.0 / k) * math.sin(2 * math.pi * k * phase)
    return (2.0 / math.pi) * v


VOWELS = {
    # rough formant-ish resonances (F1, F2, F3) in Hz
    "AH": (700, 1100, 2450),
    "UH": (500, 1200, 2200),
    "OO": (350, 900, 2200),
    "EE": (300, 2300, 3000),
    "IH": (400, 2000, 2550),
    "AY": (650, 1800, 2550),
    "AO": (600, 900, 2400),
}


def synth_vowel(duration_s: float, f0: float, vowel: str, gain: float, attack_noise: float = 0.0) -> list[float]:
    n = int(duration_s * SR)
    env = adsr(n, a=int(0.02 * SR), d=int(0.03 * SR), s=0.75, r=int(0.05 * SR))

    f1, f2, f3 = VOWELS[vowel]
    st1 = {"x1": 0.0, "x2": 0.0, "y1": 0.0, "y2": 0.0}
    st2 = {"x1": 0.0, "x2": 0.0, "y1": 0.0, "y2": 0.0}
    st3 = {"x1": 0.0, "x2": 0.0, "y1": 0.0, "y2": 0.0}

    out = [0.0] * n
    phase = 0.0
    for i in range(n):
        # mild vibrato for charm
        vib = 0.005 * math.sin(2 * math.pi * 5.0 * (i / SR))
        f = f0 * (1.0 + vib)
        phase = (phase + f / SR) % 1.0

        src = sawish(phase)

        # add a little unvoiced noise at onset (consonant-ish attack)
        if i < int(0.03 * SR) and attack_noise > 0:
            src = 0.85 * src + attack_noise * (random.random() * 2 - 1)

        # resonators in parallel, sum
        y = 0.0
        y += resonator_process(src, st1, f1, q=6.0)
        y += 0.8 * resonator_process(src, st2, f2, q=8.0)
        y += 0.6 * resonator_process(src, st3, f3, q=10.0)

        out[i] = gain * env[i] * y

    # gentle lowpass to reduce harshness
    lp_a = 0.92
    yprev = 0.0
    for i, x in enumerate(out):
        yprev = one_pole_lp(x, yprev, lp_a)
        out[i] = yprev

    return out


def synth_noise_burst(duration_s: float, gain: float) -> list[float]:
    n = int(duration_s * SR)
    env = adsr(n, a=int(0.002 * SR), d=int(0.01 * SR), s=0.0, r=int(0.02 * SR))
    out = [0.0] * n
    for i in range(n):
        out[i] = gain * env[i] * (random.random() * 2 - 1)
    return out


def silence(duration_s: float) -> list[float]:
    return [0.0] * int(duration_s * SR)


def concat(*parts: list[float]) -> list[float]:
    out: list[float] = []
    for p in parts:
        out.extend(p)
    return out


def normalize(samples: list[float], peak: float = 0.9) -> list[float]:
    m = max(1e-9, max(abs(x) for x in samples))
    g = peak / m
    return [x * g for x in samples]


def write_wav_mono_16(path: str, samples: list[float]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = bytearray()
        for x in samples:
            xi = int(clamp(x, -1.0, 1.0) * 32767)
            frames += struct.pack("<h", xi)
        wf.writeframes(frames)


def build_phrase() -> list[float]:
    # Syllable-ish plan: HU-mon | rite | good | prompt!
    base = 140.0

    hu = synth_vowel(0.22, base * 1.05, "UH", gain=0.55, attack_noise=0.05)
    mon = concat(
        synth_vowel(0.18, base, "AO", gain=0.55, attack_noise=0.03),
        synth_vowel(0.10, base * 0.92, "IH", gain=0.40, attack_noise=0.00),
    )

    rite = concat(
        synth_noise_burst(0.015, gain=0.18),
        synth_vowel(0.22, base * 1.10, "AY", gain=0.58, attack_noise=0.03),
    )

    good = concat(
        synth_vowel(0.12, base * 0.98, "OO", gain=0.55, attack_noise=0.02),
        synth_vowel(0.10, base * 0.95, "UH", gain=0.45, attack_noise=0.00),
    )

    prompt = concat(
        synth_noise_burst(0.02, gain=0.22),
        synth_vowel(0.16, base * 1.15, "AO", gain=0.62, attack_noise=0.05),
        synth_noise_burst(0.015, gain=0.12),
    )

    # Word spacing
    s_short = silence(0.05)
    s_long = silence(0.09)

    # Emphasize final word by slight pitch lift and a little extra duration
    prompt_emph = concat(
        synth_noise_burst(0.02, gain=0.22),
        synth_vowel(0.20, base * 1.25, "AO", gain=0.70, attack_noise=0.06),
        synth_noise_burst(0.02, gain=0.14),
    )

    phrase = concat(hu, silence(0.03), mon, s_long, rite, s_short, good, s_short, prompt_emph)

    # Add a tiny "machine room" bed very quietly
    bed = []
    for i in range(len(phrase)):
        bed.append(0.006 * (random.random() * 2 - 1))

    mixed = [phrase[i] + bed[i] for i in range(len(phrase))]
    return normalize(mixed, peak=0.9)


def main() -> None:
    out_path = os.path.join(
        "deliverables", "cycle-01", "output", "humon_rite_good_prompt.wav"
    )
    samples = build_phrase()
    write_wav_mono_16(out_path, samples)
    print(f"Wrote: {out_path} ({len(samples)/SR:.2f}s, {SR} Hz, mono 16-bit)")


if __name__ == "__main__":
    main()
