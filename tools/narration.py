"""Japanese voice narration for reels (pyopenjtalk; `pip install pyopenjtalk`).

Usage:
    from narration import build
    build(lines=[(0.3, 2.8, "クローゼット、もう限界ですか？"), ...],  # (start_sec, max_sec, text)
          total=19.4, bgm="bgm.wav", out="audio.wav")
Then mux: ffmpeg -i joined.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart out.mp4

Tips: write numbers and Latin letters in kana so they are read correctly
(2,980円 -> 二千九百八十円, DS -> ディーエス, 24時間 -> 二十四時間, SECOM -> セコム, WEB -> ウェブ).
Each line is sped up automatically (max 1.35x) if it would not fit in max_sec.
"""
import numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
import pyopenjtalk

SR = 44100


def synth(text, max_sec):
    speed = 1.05
    for _ in range(6):
        x, sr = pyopenjtalk.tts(text, speed=speed)
        if len(x) / sr <= max_sec or speed >= 1.35:
            break
        speed = min(1.35, speed * (len(x) / sr) / max_sec + 0.02)
    x = resample_poly(x.astype(np.float64), SR, sr)
    nz = np.where(np.abs(x) > 200)[0]
    if len(nz):
        x = x[max(0, nz[0] - 400): nz[-1] + 2000]
    return x / (np.max(np.abs(x)) + 1e-9), len(x) / SR


def build(lines, total, bgm=None, out="audio.wav", bgm_level=0.22, voice_level=0.9):
    n = int(total * SR)
    voice = np.zeros(n)
    for start, max_sec, text in lines:
        x, d = synth(text, max_sec)
        i = int(start * SR)
        j = min(n, i + len(x))
        voice[i:j] += x[: j - i]
        print(f"{start:5.1f}s  {d:4.1f}s/{max_sec:.1f}s  {text}")
    mix = voice * voice_level
    if bgm:
        sr, b = wavfile.read(bgm)
        b = b.astype(np.float64)
        if b.ndim > 1:
            b = b.mean(axis=1)
        b = b / (np.max(np.abs(b)) + 1e-9)
        if sr != SR:
            b = resample_poly(b, SR, sr)
        b = np.pad(b, (0, max(0, n - len(b))))[:n]
        mix = mix + b * bgm_level
    mix = mix / max(1.0, np.max(np.abs(mix))) * 0.95
    wavfile.write(out, SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
