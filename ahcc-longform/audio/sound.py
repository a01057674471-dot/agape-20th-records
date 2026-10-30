# 면역과 AHCC — foley and data sonification, no music bed (the brand adds its own) → out/mix.wav
# Graphite and paper: a scratch for every handwritten line (as long as the writing), a light stroke for drawn lines,
# a ruler hiss for axes, a paper sweep when the camera moves to a new part of the sheet, a hard strike at the end.
# Each data mark that lands plays a soft low-pass "plonk" whose pitch is its category (pentatonic, wood → metal).
# When voices/narration.wav exists (the recording, laid by tools/timeline.py's clock) the voice leads and all of this sits under it.
# run: LIB=<library> $LIB/.venv/bin/python audio/sound.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio.sfx import SR, add, bp, hp, lp, limit, noise, t_, env_exp, norm, brown

D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..'); OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR)
rng = np.random.default_rng(12)
fol = np.zeros((N, 2))

def scratch(d):                  # graphite on paper: band-passed noise in little strokes (the letters)
    n = noise(d); x = bp(n, 1800, 7000) * .5 + bp(n, 500, 1600) * .15
    u = np.arange(len(x)) / SR; strokes = .55 + .45 * np.sin(2 * np.pi * (5.5 + rng.random() * 2) * u) ** 2
    e = np.minimum(1, u / .03) * np.minimum(1, (d - u) / .06)
    return x * strokes * e
def stroke(d):                   # a single drawn line: smoother, softer
    n = noise(d); u = np.arange(len(n)) / SR
    return bp(n, 1200, 5000) * np.sin(np.pi * np.clip(u / d, 0, 1)) ** .8 * .45
def ruler(d):                    # ruler-guided axis: a steady hiss with a tick at each end
    x = stroke(d) * .8 + hp(noise(d), 6000) * .08; k = int(.01 * SR); x[:k] += hp(noise(.01), 3000) * .5; return x
def plonk(k):                    # sonification: pitch by category, sine + light FM through a low-pass gate
    PENT = [220.0, 261.6, 293.7, 329.6, 392.0, 440.0, 523.3, 587.3]
    f = PENT[k % len(PENT)]; d = .6; tt = t_(d); idx = 1.2 + k * .25
    y = np.sin(2 * np.pi * f * tt + idx * np.exp(-tt / .08) * np.sin(2 * np.pi * f * 2 * tt))
    return lp(y * np.exp(-tt / .18), 2400) * .5
def sweep():                     # the sheet slides under the camera
    d = 1.1; u = np.linspace(0, 1, int(d * SR)); return bp(noise(d), 500, 4000) * np.sin(np.pi * u) ** 2 * .35
def strike():                    # the pencil strikes the question out
    d = .3; tt = t_(d); return norm(bp(noise(d), 1500, 6000) * env_exp(d, .06)) * .8

for e in C['ev']:
    t, k = e['t'], e['type']
    if t >= DUR: continue
    if k == 'write': add(fol, scratch(min(4, e['d'])), t, .55, float(rng.uniform(-.25, .25)))
    elif k == 'stroke': add(fol, stroke(max(.2, min(3, e['d']))), t, .5, float(rng.uniform(-.2, .2)))
    elif k == 'rule': add(fol, ruler(max(.3, e['d'])), t, .55, 0)
    elif k == 'land': add(fol, plonk(e.get('k', 0)), t, .45, float(rng.uniform(-.3, .3)))
    elif k == 'sweep': add(fol, sweep(), t - .4, 1, 0)
    elif k == 'strike': add(fol, strike(), t, 1, 0)
room = lp(brown(DUR), 220)[:N] * .004; fol[:, 0] += room; fol[:, 1] += room     # a quiet room: the paper is never digital black

rms = lambda x: float(np.sqrt((x ** 2).mean()) + 1e-9)
vp = os.path.join(ROOT, 'voices', 'narration.wav')
if os.path.exists(vp):
    v, sr = sf.read(vp, dtype='float32'); v = v.mean(1) if v.ndim > 1 else v
    if sr != SR: v = soxr.resample(v, sr, SR)
    voice = np.zeros((N, 2)); add(voice, v[:N], 0, 1, 0)
    act = np.convolve((np.abs(voice[:, 0]) > 2e-3).astype(float), np.ones(int(.2 * SR)) / int(.2 * SR), 'same')
    vr = rms(voice[np.abs(voice[:, 0]) > 2e-3])
    mix = voice + fol / rms(fol[np.abs(fol[:, 0]) > 1e-3]) * vr * 10 ** (-13 / 20) * (1 - .3 * np.clip(act * 3, 0, 1))[:, None]
else:
    mix = fol

import subprocess, tempfile, re
def lufs(x):
    with tempfile.NamedTemporaryFile(suffix='.wav') as fh:
        sf.write(fh.name, x.astype(np.float32), SR)
        out = subprocess.run(['ffmpeg', '-nostats', '-i', fh.name, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])
from scipy.signal import butter, sosfiltfilt
mix = sosfiltfilt(butter(8, 15000, 'low', fs=SR, output='sos'), mix, axis=0)
# without a voice the foley alone is mastered quieter (-20 LUFS) so it does not pretend to be a programme level
target = -14 if os.path.exists(vp) else -20
for _ in range(3):
    mix = mix * 10 ** ((target - lufs(mix)) / 20)
    up = soxr.resample(mix, SR, SR * 4)
    up = np.stack([limit(up[:, c], .7) for c in range(2)], 1)
    mix = soxr.resample(up, SR * 4, SR)[:len(mix)]
print('mastered to', lufs(mix), 'LUFS')
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
print('mix.wav', DUR, 's; events', len(C['ev']))
