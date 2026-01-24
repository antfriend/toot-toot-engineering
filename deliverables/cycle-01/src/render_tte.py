"""Render 'Toot Toot Engineering' audio tag.

Cycle-01 target:
- 4/4 time, 65 BPM
- emphasis on beat 9 (Bar 3 Beat 1)
- heavy dub-style echo

Offline, reproducible synth approach (not true TTS): harmonic carrier + formant-ish filters,
bitcrush, and tempo-synced dub delay with a stronger send at beat 9.

Outputs:
- deliverables/cycle-01/output/toot-toot-engineering.wav
- deliverables/cycle-01/output/toot-toot-engineering-dry.wav
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter


@dataclass
class Config:
    sr: int = 44100
    bpm: float = 65.0

    def q(self) -> float:
        return 60.0 / self.bpm

    bars: int = 3
    tail_s: float = 3.0

    out_path: str = os.path.join(
        "deliverables", "cycle-01", "output", "toot-toot-engineering.wav"
    )


def butter_bandpass(low_hz: float, high_hz: float, sr: int, order: int = 3):
    nyq = 0.5 * sr
    low = max(1e-6, low_hz / nyq)
    high = min(0.999999, high_hz / nyq)
    b, a = butter(order, [low, high], btype="band")
    return b, a


def bandpass(x: np.ndarray, low_hz: float, high_hz: float, sr: int, order: int = 3):
    b, a = butter_bandpass(low_hz, high_hz, sr, order=order)
    return lfilter(b, a, x)


def adsr_envelope(n: int, sr: int, a: float, d: float, s: float, r: float):
    a_n = int(a * sr)
    d_n = int(d * sr)
    r_n = int(r * sr)
    s_n = max(0, n - a_n - d_n - r_n)

    env = np.zeros(n, dtype=np.float32)
    idx = 0
    if a_n > 0:
        env[idx : idx + a_n] = np.linspace(0.0, 1.0, a_n, endpoint=False)
        idx += a_n
    if d_n > 0:
        env[idx : idx + d_n] = np.linspace(1.0, s, d_n, endpoint=False)
        idx += d_n
    if s_n > 0:
        env[idx : idx + s_n] = s
        idx += s_n
    if r_n > 0:
        env[idx : idx + r_n] = np.linspace(s, 0.0, r_n, endpoint=True)
    return env


def harmonic_carrier(t: np.ndarray, f0: float, harmonics: int = 30):
    x = np.zeros_like(t, dtype=np.float32)
    for k in range(1, harmonics + 1):
        x += (1.0 / k) * np.sin(2 * np.pi * (f0 * k) * t)
    x /= np.max(np.abs(x)) + 1e-9
    return x


def voice_like_synth(duration_s: float, sr: int, f0: float, formants: list[tuple[float, float]]):
    n = int(duration_s * sr)
    t = np.arange(n, dtype=np.float32) / sr
    carrier = harmonic_carrier(t, f0=f0, harmonics=30)

    y = np.zeros_like(carrier)
    for (fc, bw) in formants:
        low = max(50.0, fc - bw / 2)
        high = min(sr * 0.45, fc + bw / 2)
        y += bandpass(carrier, low, high, sr, order=3)

    y /= np.max(np.abs(y)) + 1e-9

    noise = np.random.default_rng(0).normal(0, 1, size=n).astype(np.float32)
    noise = bandpass(noise, 2500, 8000, sr, order=2)
    y = 0.88 * y + 0.12 * noise

    env = adsr_envelope(n, sr, a=0.01, d=0.06, s=0.6, r=0.08)
    return (y * env).astype(np.float32)


def bitcrush(x: np.ndarray, bits: int = 11, downsample: int = 2):
    if downsample > 1:
        x = x.copy()
        for i in range(1, downsample):
            x[i::downsample] = x[::downsample][: len(x[i::downsample])]
    levels = 2**bits
    xq = np.round((x + 1.0) * (levels / 2)) / (levels / 2) - 1.0
    return np.clip(xq, -1.0, 1.0).astype(np.float32)


def dub_delay(
    x: np.ndarray,
    sr: int,
    bpm: float,
    delay_beats: float = 1.0,
    feedback: float = 0.68,
    wet: float = 0.55,
    send: np.ndarray | None = None,
    echoes: int = 10,
):
    """Classic delay line with feedback, plus low-pass in feedback path."""
    n = len(x)
    d = int((60.0 / bpm) * delay_beats * sr)
    if d < 1:
        return x

    if send is None:
        send = np.ones(n, dtype=np.float32)
    else:
        send = np.asarray(send, dtype=np.float32)
        if len(send) < n:
            send = np.pad(send, (0, n - len(send)), constant_values=float(send[-1]))
        elif len(send) > n:
            send = send[:n]

    out_len = n + echoes * d
    y = np.zeros(out_len, dtype=np.float32)

    # lowpass coefficient for feedback darkening
    cutoff = 2600.0
    a = math.exp(-2.0 * math.pi * cutoff / sr)

    def lp_step(z: float, x0: float) -> tuple[float, float]:
        z = a * z + (1 - a) * x0
        return z, z

    z = 0.0

    for i in range(out_len):
        dry = x[i] if i < n else 0.0
        s = dry * float(send[i]) if i < n else 0.0

        # delay output from previous writes
        delayed = y[i]

        # feedback is filtered version of delayed signal
        z, fb_filt = lp_step(z, delayed)

        # output mix: dry + wet*delayed (delayed already includes previous feedback)
        y[i] = dry + wet * delayed

        # write into future tap
        j = i + d
        if j < out_len:
            y[j] += s + fb_filt * feedback

    return y.astype(np.float32)


def limiter(x: np.ndarray, ceiling_db: float = -1.0):
    ceiling = 10 ** (ceiling_db / 20.0)
    peak = float(np.max(np.abs(x)) + 1e-12)
    if peak <= ceiling:
        return x
    return (x * (ceiling / peak)).astype(np.float32)


def place_segment(buf: np.ndarray, seg: np.ndarray, start_s: float, sr: int, gain: float = 1.0):
    start = int(start_s * sr)
    end = start + len(seg)
    if end > len(buf):
        buf = np.pad(buf, (0, end - len(buf)))
    buf[start:end] += seg * gain
    return buf


def main():
    cfg = Config()

    total_s = cfg.bars * 4 * cfg.q() + cfg.tail_s
    n_total = int(total_s * cfg.sr)
    buf = np.zeros(n_total, dtype=np.float32)

    q = cfg.q()

    toot_formants = [(350, 120), (900, 180), (2400, 400)]
    eng_formants = [(500, 140), (1500, 250), (2500, 500)]

    toot = bitcrush(voice_like_synth(0.28, cfg.sr, f0=95.0, formants=toot_formants))
    en = voice_like_synth(0.38, cfg.sr, f0=88.0, formants=eng_formants)
    gi = voice_like_synth(0.34, cfg.sr, f0=92.0, formants=eng_formants)
    neer = voice_like_synth(0.40, cfg.sr, f0=84.0, formants=[(400, 140), (1200, 260), (2200, 520)])
    ing = voice_like_synth(0.26, cfg.sr, f0=90.0, formants=[(600, 200), (1700, 300), (2700, 600)])

    # placement per STORYTELLER Option A
    buf = place_segment(buf, toot, start_s=0 * q, sr=cfg.sr, gain=0.95)  # beat 1
    buf = place_segment(buf, toot, start_s=1 * q, sr=cfg.sr, gain=0.88)  # beat 2

    beat9_s = 8 * q
    buf = place_segment(buf, en, start_s=beat9_s + 0 * q, sr=cfg.sr, gain=1.20)  # emphasis
    buf = place_segment(buf, gi, start_s=beat9_s + 1 * q, sr=cfg.sr, gain=1.00)
    buf = place_segment(buf, neer, start_s=beat9_s + 2 * q, sr=cfg.sr, gain=0.98)
    buf = place_segment(buf, ing, start_s=beat9_s + 3 * q, sr=cfg.sr, gain=0.95)

    # highpass (1-pole) to remove rumble
    cutoff = 90.0
    a = math.exp(-2.0 * math.pi * cutoff / cfg.sr)
    lp = np.zeros_like(buf)
    z = 0.0
    for i in range(len(buf)):
        z = a * z + (1 - a) * buf[i]
        lp[i] = z
    buf = (buf - lp).astype(np.float32)

    # Delay send automation: base + strong around beat 9
    send = np.ones(len(buf), dtype=np.float32) * 0.55
    b9 = int(beat9_s * cfg.sr)
    win = int(0.35 * cfg.sr)
    start = max(0, b9 - int(0.05 * cfg.sr))
    end = min(len(send), b9 + win)
    if end > start:
        send[start:end] = np.linspace(0.85, 1.0, end - start).astype(np.float32)

    buf_dry = buf.copy()
    buf = dub_delay(buf, sr=cfg.sr, bpm=cfg.bpm, delay_beats=1.0, feedback=0.70, wet=0.60, send=send, echoes=12)

    buf = limiter(buf, ceiling_db=-1.0)

    os.makedirs(os.path.dirname(cfg.out_path), exist_ok=True)
    wavfile.write(cfg.out_path, cfg.sr, (np.clip(buf, -1, 1) * 32767.0).astype(np.int16))

    dry_path = cfg.out_path.replace(".wav", "-dry.wav")
    dry = limiter(buf_dry, ceiling_db=-1.0)
    wavfile.write(dry_path, cfg.sr, (np.clip(dry, -1, 1) * 32767.0).astype(np.int16))

    print("Wrote:", cfg.out_path)
    print("Wrote:", dry_path)


if __name__ == "__main__":
    main()
