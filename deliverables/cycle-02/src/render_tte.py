"""Render 'Toot Toot Engineering' audio tag.

Cycle-02 target:
- 4/4 time, 130 BPM (double-time)
- emphasis on beat 9 (Bar 3 Beat 1)
- heavy dub-style echo
- enhanced consonant articulation (crisp plosives/sibilants)

Offline, reproducible synth approach (no external deps): harmonic carrier + formant-ish filters,
bitcrush, consonant noise layers, and tempo-synced dub delay with a stronger send at beat 9.

Outputs:
- deliverables/cycle-02/output/toot-toot-engineering.wav
- deliverables/cycle-02/output/toot-toot-engineering-dry.wav
"""

from __future__ import annotations

import math
import os
import random
import wave
from dataclasses import dataclass


def clip(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


@dataclass
class Config:
    sr: int = 44100
    bpm: float = 130.0

    def q(self) -> float:
        return 60.0 / self.bpm

    bars: int = 3
    tail_s: float = 2.5

    out_path: str = os.path.join(
        "deliverables", "cycle-02", "output", "toot-toot-engineering.wav"
    )


def adsr_envelope(n: int, sr: int, a: float, d: float, s: float, r: float) -> list[float]:
    a_n = max(0, int(a * sr))
    d_n = max(0, int(d * sr))
    r_n = max(0, int(r * sr))
    s_n = max(0, n - a_n - d_n - r_n)

    env: list[float] = [0.0] * n
    idx = 0

    def fill_linear(start: float, end: float, count: int) -> None:
        nonlocal idx
        if count <= 0:
            return
        for i in range(count):
            if idx >= n:
                return
            t = i / float(count)
            env[idx] = start + (end - start) * t
            idx += 1

    def fill_const(value: float, count: int) -> None:
        nonlocal idx
        if count <= 0:
            return
        for _ in range(count):
            if idx >= n:
                return
            env[idx] = value
            idx += 1

    fill_linear(0.0, 1.0, a_n)
    fill_linear(1.0, s, d_n)
    fill_const(s, s_n)
    fill_linear(s, 0.0, r_n)
    return env


def harmonic_carrier(n: int, sr: int, f0: float, harmonics: int = 28) -> list[float]:
    carrier: list[float] = [0.0] * n
    for i in range(n):
        t = i / float(sr)
        val = 0.0
        for k in range(1, harmonics + 1):
            val += (1.0 / k) * math.sin(2.0 * math.pi * (f0 * k) * t)
        carrier[i] = val
    return normalize(carrier)


def biquad_bandpass(low_hz: float, high_hz: float, sr: int) -> tuple[float, float, float, float, float]:
    fc = max(1.0, (low_hz + high_hz) / 2.0)
    bw = max(1.0, high_hz - low_hz)
    q = max(0.2, fc / bw)
    w0 = 2.0 * math.pi * fc / sr
    cos_w0 = math.cos(w0)
    sin_w0 = math.sin(w0)
    alpha = sin_w0 / (2.0 * q)

    b0 = sin_w0 / 2.0
    b1 = 0.0
    b2 = -sin_w0 / 2.0
    a0 = 1.0 + alpha
    a1 = -2.0 * cos_w0
    a2 = 1.0 - alpha

    b0 /= a0
    b1 /= a0
    b2 /= a0
    a1 /= a0
    a2 /= a0

    return b0, b1, b2, a1, a2


def biquad_filter(x: list[float], coeffs: tuple[float, float, float, float, float]) -> list[float]:
    b0, b1, b2, a1, a2 = coeffs
    y: list[float] = [0.0] * len(x)
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0
    for i, x0 in enumerate(x):
        y0 = b0 * x0 + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        y[i] = y0
        x2 = x1
        x1 = x0
        y2 = y1
        y1 = y0
    return y


def bandpass(x: list[float], low_hz: float, high_hz: float, sr: int) -> list[float]:
    coeffs = biquad_bandpass(low_hz, high_hz, sr)
    return biquad_filter(x, coeffs)


def normalize(x: list[float]) -> list[float]:
    peak = max((abs(v) for v in x), default=0.0)
    if peak <= 1e-9:
        return x
    return [v / peak for v in x]


def voice_like_synth(duration_s: float, sr: int, f0: float, formants: list[tuple[float, float]], seed: int) -> list[float]:
    n = int(duration_s * sr)
    carrier = harmonic_carrier(n, sr, f0=f0, harmonics=28)

    y = [0.0] * n
    for (fc, bw) in formants:
        low = max(50.0, fc - bw / 2.0)
        high = min(sr * 0.45, fc + bw / 2.0)
        filtered = bandpass(carrier, low, high, sr)
        for i in range(n):
            y[i] += filtered[i]

    y = normalize(y)

    rng = random.Random(seed)
    noise = [rng.gauss(0.0, 1.0) for _ in range(n)]
    noise = bandpass(noise, 2500, 9000, sr)

    for i in range(n):
        y[i] = 0.86 * y[i] + 0.14 * noise[i]

    env = adsr_envelope(n, sr, a=0.008, d=0.05, s=0.58, r=0.07)
    return [y[i] * env[i] for i in range(n)]


def consonant_burst(duration_s: float, sr: int, low_hz: float, high_hz: float, seed: int) -> list[float]:
    n = int(duration_s * sr)
    rng = random.Random(seed)
    noise = [rng.gauss(0.0, 1.0) for _ in range(n)]
    burst = bandpass(noise, low_hz, high_hz, sr)
    env = adsr_envelope(n, sr, a=0.001, d=0.03, s=0.0, r=0.06)
    return [burst[i] * env[i] for i in range(n)]


def add_burst(seg: list[float], sr: int, start_s: float, burst: list[float], gain: float) -> list[float]:
    start = int(start_s * sr)
    end = min(len(seg), start + len(burst))
    for i in range(start, end):
        seg[i] += burst[i - start] * gain
    return seg


def bitcrush(x: list[float], bits: int = 11, downsample: int = 2) -> list[float]:
    if downsample > 1:
        for i in range(1, downsample):
            for j in range(i, len(x), downsample):
                x[j] = x[j - i]
    levels = 2**bits
    out = []
    for v in x:
        q = round((v + 1.0) * (levels / 2.0)) / (levels / 2.0) - 1.0
        out.append(clip(q))
    return out


def dub_delay(
    x: list[float],
    sr: int,
    bpm: float,
    delay_beats: float = 1.0,
    feedback: float = 0.70,
    wet: float = 0.60,
    send: list[float] | None = None,
    echoes: int = 10,
) -> list[float]:
    n = len(x)
    d = int((60.0 / bpm) * delay_beats * sr)
    if d < 1:
        return x

    if send is None:
        send = [1.0] * n
    elif len(send) < n:
        send = send + [send[-1]] * (n - len(send))
    elif len(send) > n:
        send = send[:n]

    out_len = n + echoes * d
    y = [0.0] * out_len

    cutoff = 2400.0
    a = math.exp(-2.0 * math.pi * cutoff / sr)
    z = 0.0

    for i in range(out_len):
        dry = x[i] if i < n else 0.0
        s = dry * send[i] if i < n else 0.0
        delayed = y[i]

        z = a * z + (1.0 - a) * delayed
        fb_filt = z

        y[i] = dry + wet * delayed

        j = i + d
        if j < out_len:
            y[j] += s + fb_filt * feedback

    return y


def limiter(x: list[float], ceiling_db: float = -1.0) -> list[float]:
    ceiling = 10 ** (ceiling_db / 20.0)
    peak = max((abs(v) for v in x), default=0.0)
    if peak <= ceiling or peak <= 1e-12:
        return x
    scale = ceiling / peak
    return [v * scale for v in x]


def place_segment(buf: list[float], seg: list[float], start_s: float, sr: int, gain: float = 1.0) -> list[float]:
    start = int(start_s * sr)
    end = start + len(seg)
    if end > len(buf):
        buf.extend([0.0] * (end - len(buf)))
    for i in range(len(seg)):
        buf[start + i] += seg[i] * gain
    return buf


def write_wav(path: str, sr: int, x: list[float]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    frames = bytearray()
    for v in x:
        v = int(clip(v) * 32767.0)
        frames += v.to_bytes(2, byteorder="little", signed=True)

    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(frames)


def main() -> None:
    cfg = Config()

    total_s = cfg.bars * 4 * cfg.q() + cfg.tail_s
    n_total = int(total_s * cfg.sr)
    buf = [0.0] * n_total

    q = cfg.q()

    toot_formants = [(360, 120), (980, 180), (2600, 420)]
    eng_formants = [(520, 140), (1560, 260), (2600, 520)]

    toot = bitcrush(voice_like_synth(0.22, cfg.sr, f0=100.0, formants=toot_formants, seed=11))
    en = voice_like_synth(0.30, cfg.sr, f0=92.0, formants=eng_formants, seed=12)
    gi = voice_like_synth(0.26, cfg.sr, f0=96.0, formants=eng_formants, seed=13)
    neer = voice_like_synth(0.32, cfg.sr, f0=86.0, formants=[(420, 140), (1280, 260), (2320, 520)], seed=14)
    ing = voice_like_synth(0.22, cfg.sr, f0=94.0, formants=[(620, 200), (1760, 320), (2800, 600)], seed=15)

    t_plosive = consonant_burst(0.04, cfg.sr, 300, 1400, seed=21)
    t_sizzle = consonant_burst(0.05, cfg.sr, 3500, 9000, seed=22)
    g_attack = consonant_burst(0.04, cfg.sr, 400, 1800, seed=23)
    s_sizzle = consonant_burst(0.06, cfg.sr, 4200, 9800, seed=24)

    toot = add_burst(toot, cfg.sr, 0.0, t_plosive, 0.65)
    toot = add_burst(toot, cfg.sr, 0.0, t_sizzle, 0.55)
    toot = add_burst(toot, cfg.sr, 0.15, t_plosive, 0.50)

    en = add_burst(en, cfg.sr, 0.0, t_sizzle, 0.25)
    gi = add_burst(gi, cfg.sr, 0.0, g_attack, 0.55)
    neer = add_burst(neer, cfg.sr, 0.0, s_sizzle, 0.22)
    ing = add_burst(ing, cfg.sr, 0.02, s_sizzle, 0.35)

    buf = place_segment(buf, toot, start_s=0 * q, sr=cfg.sr, gain=0.98)
    buf = place_segment(buf, toot, start_s=1 * q, sr=cfg.sr, gain=0.92)

    beat9_s = 8 * q
    buf = place_segment(buf, en, start_s=beat9_s + 0 * q, sr=cfg.sr, gain=1.30)
    buf = place_segment(buf, gi, start_s=beat9_s + 1 * q, sr=cfg.sr, gain=1.05)
    buf = place_segment(buf, neer, start_s=beat9_s + 2 * q, sr=cfg.sr, gain=1.02)
    buf = place_segment(buf, ing, start_s=beat9_s + 3 * q, sr=cfg.sr, gain=0.98)

    cutoff = 95.0
    a = math.exp(-2.0 * math.pi * cutoff / cfg.sr)
    lp = [0.0] * len(buf)
    z = 0.0
    for i, v in enumerate(buf):
        z = a * z + (1.0 - a) * v
        lp[i] = z
    for i in range(len(buf)):
        buf[i] = buf[i] - lp[i]

    send = [0.58] * len(buf)
    b9 = int(beat9_s * cfg.sr)
    win = int(0.30 * cfg.sr)
    start = max(0, b9 - int(0.04 * cfg.sr))
    end = min(len(send), b9 + win)
    if end > start:
        span = end - start
        for i in range(span):
            send[start + i] = 0.90 + (1.0 - 0.90) * (i / float(span))

    buf_dry = list(buf)
    buf = dub_delay(buf, sr=cfg.sr, bpm=cfg.bpm, delay_beats=1.0, feedback=0.72, wet=0.62, send=send, echoes=11)

    buf = limiter(buf, ceiling_db=-1.0)
    write_wav(cfg.out_path, cfg.sr, buf)

    dry_path = cfg.out_path.replace(".wav", "-dry.wav")
    dry = limiter(buf_dry, ceiling_db=-1.0)
    write_wav(dry_path, cfg.sr, dry)

    print("Wrote:", cfg.out_path)
    print("Wrote:", dry_path)


if __name__ == "__main__":
    main()
