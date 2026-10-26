# AHCC whiteboard — marker foley (one sound per real stroke), props, room tone, voice and the final mix → out/mix.wav
# The voice (voices/<id>.wav) is placed at each line's start; if no voice files exist yet, the mix is music + foley only.
# run: LIB=<library> $LIB/.venv/bin/python audio/sound.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio.sfx import SR, add, bp, hp, lp, brown, compress, limit

D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..'); OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR); tt = np.arange(N) / SR
rng = np.random.default_rng(3)
fol = np.zeros((N, 2), np.float32); voice = np.zeros((N, 2), np.float32)

# ---------- felt marker on gloss: hiss band + body, enveloped by the stroke's speed curve, nib tick, occasional squeak ----------
TONE = {'k': 1.0, 'b': 1.08, 'o': .94}
def marker(d, pen, L, kind):
    d = max(.035, d); n = int(d * SR); u = np.arange(n) / n
    speed = np.clip(1 - np.cos(2 * np.pi * u) * .8, .2, 2)          # slow-fast-slow, like the drawing
    x = rng.standard_normal(n); f = TONE.get(pen, 1)
    y = bp(x, 2000 * f, 7500, 2) * .8 + bp(x, 500 * f, 1500 * f, 2) * .35
    stick = (rng.random(n) > .996) * rng.standard_normal(n) * 3      # stick-slip grains
    y = (y + hp(stick, 1800) * .4) * speed
    e = np.minimum(1, np.arange(n) / (.006 * SR)) * np.minimum(1, (n - np.arange(n)) / (.02 * SR))
    y = y * e * (.16 if kind == 'write' else .2)
    tick = np.zeros(n); m = min(n, int(.006 * SR)); tick[:m] = rng.standard_normal(m) * np.linspace(1, 0, m) * .5
    y += hp(tick, 2500)
    if kind == 'stroke' and L > 250 and rng.random() < .3:            # the dry-erase squeak
        s = np.arange(n) / SR; fq = rng.uniform(1500, 2600) + 60 * np.sin(2 * np.pi * rng.uniform(7, 13) * s)
        sq = np.sin(2 * np.pi * np.cumsum(fq) / SR) * np.sin(np.pi * u) ** 2 * .035; y += sq
    return y.astype(np.float32)
for e in C['ev']:
    if e['type'] in ('stroke', 'write', 'dash', 'tap'):
        pan = np.clip((e.get('x', 750) - 750) / 600, -.7, .7)
        add(fol, marker(e['dur'], e.get('pen', 'k'), e.get('len', 100), e['type']), e['t'], 1, pan)
    elif e['type'] == 'magnet':                                    # magnet on steel: click + metal ring + a low thump
        n = int(.5 * SR); s = np.arange(n) / SR
        y = np.sin(2 * np.pi * 2350 * s) * np.exp(-s / .05) * .08 + np.sin(2 * np.pi * 3720 * s) * np.exp(-s / .03) * .05 + lp(rng.standard_normal(n), 220) * np.exp(-s / .04) * .5
        add(fol, y.astype(np.float32), e['t'], 1, .4)
    elif e['type'] == 'cap':                                       # the marker cap clicks on
        n = int(.08 * SR); s = np.arange(n) / SR; add(fol, (hp(rng.standard_normal(n), 2000) * np.exp(-s / .006) * .4).astype(np.float32), e['t'], 1, .3)
room = (lp(brown(DUR), 300) * .02).astype(np.float32); fol[:, 0] += room; fol[:, 1] += room

# ---------- voice ----------
have = 0
for l in C['lines']:
    p = os.path.join(ROOT, 'voices', l['id'] + '.wav')
    if not os.path.exists(p): continue
    x, sr = sf.read(p, dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
    if sr != SR: x = soxr.resample(x, sr, SR)
    add(voice, x, l['t0'], 1, 0); have += 1
if have:
    v = compress(voice[:, 0], thr=.2, ratio=3.0); voice = np.stack([v, v], 1)

# ---------- mix ----------
score, sr = sf.read(os.path.join(D, 'score.wav'), dtype='float32'); assert sr == SR
score = score[:N] if len(score) >= N else np.pad(score, ((0, N - len(score)), (0, 0)))
rms = lambda x: float(np.sqrt((x ** 2).mean()) + 1e-9)
if have:
    vr = rms(voice[np.abs(voice[:, 0]) > 1e-4])
    duck = np.ones(N)
    for l in C['lines']: duck[int(l['t0'] * SR):int(min(DUR, l['t1'] + .15) * SR)] = .45
    duck = np.convolve(duck, np.ones(int(.12 * SR)) / int(.12 * SR), 'same')
    music = score / rms(score) * vr * 10 ** (-13 / 20) * duck[:, None]          # music ~13 dB under the voice, ducked further under speech
    foley = fol / rms(fol) * vr * 10 ** (-11 / 20)                               # foley ~11 dB under the voice
    mix = voice + music + foley
else:
    mix = score * .55 + fol * (rms(score) * .55 / rms(fol)) * .6
mix = np.stack([limit(mix[:, c], .95) for c in range(2)], 1)
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
print('mix.wav', DUR, 's; voice lines:', have, '; peak', round(float(np.abs(mix).max()), 3))
