#!/usr/bin/env python3
"""Sound for the reel: the user's narration up front, a low lab-ambience bed, and effects made here from noise and
sines (no samples): snaps when the threads break, whooshes on cuts, a glassy shimmer on the healthy network,
a shatter on "조각조각", a dip into stillness for the ER, a rising swell when the fragments heal, a chime on the logo.
  python audio/sound.py  ->  out/mix.wav   (times match window.EV in film.js)"""
import os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR, DUR = 48000, 31.0
N = int(SR * DUR); rng = np.random.default_rng(7)
t = np.arange(N) / SR

def env(n, a, d):  # attack / exponential decay
    x = np.arange(n) / SR; e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-np.maximum(0, x - a) / d); return e
def lp(x, k):       # one-pole low-pass, k in (0,1): higher = brighter
    y = np.empty_like(x); s = 0.
    for i in range(len(x)): s += k * (x[i] - s); y[i] = s
    return y
def place(buf, snd, at, g=1., pan=0.):
    i = int(at * SR); j = min(len(buf), i + len(snd)); s = snd[:j - i] * g
    buf[i:j, 0] += s * (1 - max(0, pan)); buf[i:j, 1] += s * (1 + min(0, pan))

def snap():
    n = int(.25 * SR); x = rng.standard_normal(n) * env(n, .001, .03)
    tone = np.sin(2 * np.pi * 1800 * np.arange(n) / SR) * env(n, .001, .015)
    return (x - lp(x, .15)) * .7 + tone * .4
def whoosh(d=.55):
    n = int(d * SR); x = rng.standard_normal(n); k = np.linspace(.02, .25, n) ** 1.2
    y = np.empty(n); s = 0.
    for i in range(n): s += k[i] * (x[i] - s); y[i] = s
    sh = np.sin(np.pi * np.arange(n) / n) ** 2; return y * sh * 1.6
def shimmer():
    n = int(1.8 * SR); x = np.arange(n) / SR; y = np.zeros(n)
    for f in [1568, 2093, 2637, 3136]: y += np.sin(2 * np.pi * f * x + rng.uniform(0, 6)) * np.exp(-x / 1.1) * (0.5 + .5 * np.sin(2 * np.pi * rng.uniform(4, 7) * x))
    return y * np.minimum(1, x / .05) * .18
def shatter():
    n = int(1.2 * SR); y = np.zeros(n)
    for k in range(40):
        at = int(abs(rng.normal(0, .12)) * SR); m = int(.06 * SR)
        if at + m >= n: continue
        f = rng.uniform(2000, 6000); xx = np.arange(m) / SR
        y[at:at + m] += np.sin(2 * np.pi * f * xx) * np.exp(-xx / .012) * rng.uniform(.2, .7)
    b = rng.standard_normal(n) * env(n, .002, .09); y += (b - lp(b, .1)) * .5
    thump = np.sin(2 * np.pi * 70 * np.arange(n) / SR) * env(n, .003, .12) * .8
    return y * .6 + thump
def swell():
    n = int(2.2 * SR); x = np.arange(n) / SR; y = np.zeros(n)
    for f in [220, 277.2, 329.6, 440]: y += np.sin(2 * np.pi * f * x * (1 + .002 * np.sin(2 * np.pi * .7 * x)))
    sh = np.sin(np.pi * np.minimum(1, x / 2.2)) ** 1.5; return y * sh * .07
def chime():
    n = int(2.6 * SR); x = np.arange(n) / SR; y = np.zeros(n)
    for f, a in [(880, 1), (1318.5, .6), (1760, .35), (2637, .2)]: y += a * np.sin(2 * np.pi * f * x) * np.exp(-x / .9)
    return y * np.minimum(1, x / .004) * .16

fx = np.zeros((N, 2))
for a in [.35, .8, 1.25]: place(fx, snap(), a, .55, rng.uniform(-.5, .5))
for a in [2.45, 6.8, 9.85, 12.95, 15.45, 22.75]: place(fx, whoosh(), a - .3, .22)
place(fx, shimmer(), 7.1, 1.)
place(fx, shatter(), 11.75, .5)
place(fx, swell(), 20.9, 1.)
place(fx, chime(), 26.4, 1.)
# bed: a low hum and filtered air, ducking out for the ER moment (13.2–15.3) and under the end card
bed = (np.sin(2 * np.pi * 55 * t) * .5 + np.sin(2 * np.pi * 82.4 * t) * .3) * (0.8 + .2 * np.sin(2 * np.pi * .13 * t))
air = rng.standard_normal(N); air = lp(air, .02) * 3
g = np.ones(N) * .05
g *= 1 - .7 * np.clip(1 - np.abs(t - 14.2) / 1.2, 0, 1)
g *= np.clip((DUR - .3 - t) / 2.5, 0, 1)
g *= np.clip(t / .6, 0, 1)
bedm = (bed * .5 + air) * g
fx[:, 0] += bedm; fx[:, 1] += bedm

# narration
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(HERE, 'audio', 'narration.mp3'), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
v = np.frombuffer(pcm, np.float32)[:N]; v = np.pad(v, (0, N - len(v)))
v = v / (np.sqrt(np.mean(v[v != 0] ** 2)) + 1e-9) * .12
# duck the effects under the voice
ve = np.convolve(np.abs(v), np.ones(2400) / 2400, 'same'); duck = 1 - .45 * np.clip(ve / (ve.max() * .3), 0, 1)
mix = fx * duck[:, None] + v[:, None]
mix /= max(1e-9, np.abs(mix).max()) / .89
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', os.path.join(HERE, 'out', 'mix.wav')],
               input=mix.astype(np.float32).tobytes(), check=True)
print('mix.wav', DUR, 's')
