#!/usr/bin/env python3
"""Sound for the reel: the user's narration up front, the user's music (audio/music.mp3) underneath, ducked while
the voice speaks, and only a few clean tonal accents (soft sine chimes when each tip card lands). No noise-based
effects: no hiss bed, no crackle, no whooshes.
  python audio/sound.py  ->  out/mix.wav"""
import os, re, subprocess
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = float(re.search(r'DUR = ([\d.]+)', open(os.path.join(HERE, 'film.js'), encoding='utf-8').read()).group(1))
SR = 48000; N = int(SR * DUR); t = np.arange(N) / SR

def read(path, ch):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32).reshape(-1, ch)[:N]; return np.pad(x, ((0, N - len(x)), (0, 0)))
def chime(f0, d=1.4):
    x = np.arange(int(d * SR)) / SR; y = np.zeros_like(x)
    for m, a in [(1, 1), (2, .35), (3, .12)]: y += a * np.sin(2 * np.pi * f0 * m * x) * np.exp(-x / (.55 / m))
    return y * np.minimum(1, x / .006)
def place(buf, snd, at, g):
    i = int(at * SR); j = min(len(buf), i + len(snd)); buf[i:j] += snd[:j - i, None] * g

voice = read(os.path.join(HERE, 'audio', 'narration.mp3'), 1)[:, 0]
music = read(os.path.join(HERE, 'audio', 'music.mp3'), 2)
rms = lambda x: np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) + 1e-9
voice = voice / rms(voice) * .12
music = music / rms(music) * .12
# music: in over 1 s, ducked ~10 dB under the voice (smoothed), up a little on the summary and product, out over 2.5 s
ve = np.convolve(np.abs(voice), np.ones(SR // 5) / (SR // 5), 'same')
talk = np.clip(ve / (np.percentile(ve[ve > 1e-4], 60) + 1e-9), 0, 1)
k = np.ones(SR // 2) / (SR // 2); talk = np.convolve(talk, k, 'same')
g = lerp = None
g = (1 - talk) * .55 + talk * .17
g *= np.clip(t / 1.0, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1)
g = np.where(t > 43.9, np.maximum(g, .5 * np.clip((DUR - t) / 2.5, 0, 1)), g)
fx = np.zeros((N, 2))
for a in [24.15, 30.65, 37.2]: place(fx, chime(880), a + .1, .05); place(fx, chime(1318.5), a + 2.05, .04)
place(fx, chime(1046.5, 2.0), 47.7, .05)
mix = music * g[:, None] + voice[:, None] + fx
mix /= max(1e-9, np.abs(mix).max()) / .89
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', os.path.join(HERE, 'out', 'mix.wav')],
               input=mix.astype(np.float32).tobytes(), check=True)
print('mix.wav', DUR, 's')
