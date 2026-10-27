# 올리고파 — foley from the picture's events (audio/cues.json), room tone, score, master → out/mix.wav
# run: LIB=<library> $LIB/.venv/bin/python audio/sound.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio.sfx import SR, add, bp, hp, lp, brown, limit, click, clack, whoosh, pop, ding, thump

D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..'); OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR)
rng = np.random.default_rng(3)
fol = np.zeros((N, 2), np.float32)
f32 = lambda y: np.asarray(y, np.float32)

def bolt():               # electric crack + a sub drop under it
    n = int(.9 * SR); s = np.arange(n) / SR
    crack = hp(rng.standard_normal(n), 1800) * np.exp(-s / .035) * (1 + (rng.random(n) > .93) * 2) * .5
    f = 90 * np.exp(-s / .25) + 32; sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s / .35) * .9
    return f32(crack + sub)
def shimmer(d):           # the light sweep: an airy band that rises and falls
    n = int(d * SR); u = np.arange(n) / n
    return f32(bp(rng.standard_normal(n), 6000, 12000, 2) * np.sin(np.pi * u) ** 2 * .06)
def grain():              # a digit settling: tiny high tick
    n = int(.03 * SR); return f32(hp(rng.standard_normal(n), 4000) * np.exp(-np.arange(n) / SR / .004) * .25)
def tap(i):               # one hex lands: a glassy pitched tick
    n = int(.12 * SR); s = np.arange(n) / SR; f = 2600 + (i % 6) * 180
    return f32(np.sin(2 * np.pi * f * s) * np.exp(-s / .025) * .08)

for e in C['ev']:
    t, k = e['t'], e['type']
    if k == 'bolt': add(fol, bolt(), t, 1, .15)
    elif k == 'lock': add(fol, f32(click(1.3, .5)), t, 1, .1)
    elif k == 'snap': add(fol, f32(clack(1.2, .45)), t, 1, -.2)
    elif k == 'whoosh': add(fol, f32(whoosh(.4, .45)), t - .2, 1, 0)
    elif k == 'expand': add(fol, f32(whoosh(.55, .55)), t - .25, 1, 0)
    elif k == 'grain': add(fol, grain(), t, 1, .25)
    elif k == 'shimmer': add(fol, shimmer(e.get('d', 1.6)), t, 1, .3)
    elif k == 'pop': add(fol, f32(thump(.45, 60)), t, 1, 0)
    elif k == 'split': add(fol, f32(pop(.5)), t, 1, 0)
    elif k == 'tap': add(fol, tap(e.get('i', 0)), t, 1, -.6 + (e.get('i', 0) % 6) * .24)
    elif k in ('bar', 'barHero'): add(fol, f32(thump(.5 if k == 'bar' else .75, 70)), t, 1, 0)
    elif k == 'sparkle': add(fol, f32(ding(.3)), t, 1, .4)
    elif k == 'tick': add(fol, f32(click(1.6, .28)), t, 1, -.6 + (e.get('i', 0) % 7) * .2)
room = (lp(brown(DUR), 200) * .012).astype(np.float32); fol[:, 0] += room[:N]; fol[:, 1] += room[:N]

score, sr = sf.read(os.path.join(D, 'score.wav'), dtype='float32'); assert sr == SR
score = score[:N] if len(score) >= N else np.pad(score, ((0, N - len(score)), (0, 0)))
rms = lambda x: float(np.sqrt((x ** 2).mean()) + 1e-9)
mix = score + fol * (rms(score) / rms(fol)) * 10 ** (-6 / 20)
s0 = [e for e in C['ev'] if e['type'] == 'silence'][0]; a, b = int(s0['t'] * SR), int((s0['t'] + s0['d']) * SR)
mix[a:b] = 0                                                     # the silence is total: no room tone either

import subprocess, tempfile, re
def lufs(x):
    with tempfile.NamedTemporaryFile(suffix='.wav') as f:
        sf.write(f.name, x.astype(np.float32), SR)
        out = subprocess.run(['ffmpeg', '-nostats', '-i', f.name, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])
from scipy.signal import butter, sosfiltfilt
mix = sosfiltfilt(butter(8, 15000, 'low', fs=SR, output='sos'), mix, axis=0)
for _ in range(3):
    mix = mix * 10 ** ((-14 - lufs(mix)) / 20)
    up = soxr.resample(mix, SR, SR * 4)
    up = np.stack([limit(up[:, c], .7) for c in range(2)], 1)
    mix = soxr.resample(up, SR * 4, SR)[:len(mix)]
mix[a:b] = 0
print('mastered to', lufs(mix), 'LUFS')
# 24 s of trailing silence: mux.sh's decode check runs ~2.9 s behind and allows 5 % of the length, so the file must exceed ~58 s; build.sh trims the film back to the picture
mix = np.concatenate([mix, np.zeros((24 * SR, 2))])
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
print('mix.wav', DUR, 's; peak', round(float(np.abs(mix).max()), 3))
