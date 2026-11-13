#!/usr/bin/env python3
"""Sound: narration up front, the user's music (audio/music.mp3) under it, ducked while the voice speaks, and a few
clean sine accents (numbers, arrows, cards). No noise effects.   python audio/sound.py -> out/mix.wav"""
import os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = 44.5; SR = 48000; N = int(SR * DUR); t = np.arange(N) / SR
def read(path, ch):
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', str(ch), '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32).reshape(-1, ch)[:N]; return np.pad(x, ((0, N - len(x)), (0, 0)))
def tone(f, d=.6, dec=.22):
    x = np.arange(int(d * SR)) / SR; return (np.sin(2 * np.pi * f * x) + .25 * np.sin(4 * np.pi * f * x)) * np.exp(-x / dec) * np.minimum(1, x / .004)
def place(buf, snd, at, g):
    i = int(at * SR); j = min(len(buf), i + len(snd)); buf[i:j] += snd[:j - i, None] * g
voice = read(os.path.join(HERE, 'audio', 'narration.mp3'), 1)[:, 0]
music = read(os.path.join(HERE, 'audio', 'music.mp3'), 2)
rms = lambda x: np.sqrt(np.mean(x[np.abs(x) > 1e-4] ** 2)) + 1e-9
voice = voice / rms(voice) * .12; music = music / rms(music) * .12
ve = np.convolve(np.abs(voice), np.ones(SR // 5) / (SR // 5), 'same')
talk = np.clip(ve / (np.percentile(ve[ve > 1e-4], 60) + 1e-9), 0, 1); talk = np.convolve(talk, np.ones(SR // 2) / (SR // 2), 'same')
g = ((1 - talk) * .55 + talk * .18) * np.clip(t / .8, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1)
fx = np.zeros((N, 2))
place(fx, tone(659.3), 5.0, .035); place(fx, tone(880), 5.1, .03)                                      # 52 people
for k in range(4): place(fx, tone(523.3 + 60 * k, .35), 9.4 + k * .65, .025)                           # the weeks filling
place(fx, tone(784), 17.7, .045); place(fx, tone(1046.5), 17.8, .04)                                   # +60%
place(fx, tone(880), 19.95, .045); place(fx, tone(1174.7), 20.05, .04)                                 # 2x
place(fx, tone(659.3), 22.3, .04); place(fx, tone(987.8), 22.4, .035)                                  # antibodies up
place(fx, tone(587.3), 24.05, .04); place(fx, tone(392), 24.15, .035)                                  # inflammation down
for a in [27.45, 30.85, 33.5]: place(fx, tone(1046.5, .5), a, .035)                                    # cards
place(fx, tone(784, 1.2, .5), 37.1, .04); place(fx, tone(1174.7, 1.2, .5), 37.2, .035)                  # product
mix = music * g[:, None] + voice[:, None] + fx
mix /= max(1e-9, np.abs(mix).max()) / .89
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', os.path.join(HERE, 'out', 'mix.wav')], input=mix.astype(np.float32).tobytes(), check=True)
print('mix.wav', DUR, 's')
