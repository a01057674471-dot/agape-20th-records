#!/usr/bin/env python3
"""Sound: the paced narration up front, the user's music (audio/music.mp3) under it (ducked while the voice speaks),
and two clean tonal accents only: a soft falling two-note on each NG cross, a bright rising two-note on each OK circle.
No noise-based effects.   python audio/sound.py -> out/mix.wav"""
import json, os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(HERE, 'audio', 'lines_paced.json')))
DUR = round(L[-1]['t1'] + 3.0, 2); SR = 48000; N = int(SR * DUR); t = np.arange(N) / SR
ITEMS = [(1, 3), (4, 6), (7, 8), (9, 10), (11, 13)]
def read(path, ch):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32).reshape(-1, ch)[:N]; return np.pad(x, ((0, N - len(x)), (0, 0)))
def tone(f, d=.5, dec=.18):
    x = np.arange(int(d * SR)) / SR; y = (np.sin(2 * np.pi * f * x) + .3 * np.sin(4 * np.pi * f * x)) * np.exp(-x / dec)
    return y * np.minimum(1, x / .004)
def place(buf, snd, at, g):
    i = int(at * SR); j = min(len(buf), i + len(snd)); buf[i:j] += snd[:j - i, None] * g
voice = read(os.path.join(HERE, 'audio', 'narration_paced.wav'), 1)[:, 0]
music = read(os.path.join(HERE, 'audio', 'music.mp3'), 2)
rms = lambda x: np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) + 1e-9
voice = voice / rms(voice) * .12; music = music / rms(music) * .12
ve = np.convolve(np.abs(voice), np.ones(SR // 5) / (SR // 5), 'same')
talk = np.clip(ve / (np.percentile(ve[ve > 1e-4], 60) + 1e-9), 0, 1); talk = np.convolve(talk, np.ones(SR // 2) / (SR // 2), 'same')
g = ((1 - talk) * .6 + talk * .2) * np.clip(t / .5, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
fx = np.zeros((N, 2))
for x, o in ITEMS:
    tx = L[x]['t0'] - .15 + .3; to = L[o]['t0'] - .15 + .3
    place(fx, tone(392), tx, .05); place(fx, tone(311), tx + .1, .05)
    place(fx, tone(784), to, .04); place(fx, tone(1046.5), to + .09, .04)
mix = music * g[:, None] + voice[:, None] + fx
mix /= max(1e-9, np.abs(mix).max()) / .89
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', os.path.join(HERE, 'out', 'mix.wav')], input=mix.astype(np.float32).tobytes(), check=True)
print('mix.wav', DUR, 's')
