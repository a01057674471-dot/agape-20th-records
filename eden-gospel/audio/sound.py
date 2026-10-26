# 동산의 동편 — foley, ambience and the final mix (TREATMENT.md §7). All sounds are synthesised here.
# run: LIB=<library> $LIB/.venv/bin/python audio/sound.py   (after tools/export_cues.mjs and audio/score.py) → out/mix.wav
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
from core.audio.sfx import SR, add, bp, hp, lp, brown, thump, whoosh, compress, limit

D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, '..', 'out'); os.makedirs(OUT, exist_ok=True)
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR); tt = np.arange(N) / SR
rng = np.random.default_rng(7)
B = {k: np.zeros((N, 2), np.float32) for k in ['pen', 'wash', 'amb', 'fx']}
ev = lambda typ: [e for e in C['ev'] if e['type'] == typ]
def envk(keys): ks = np.array(keys, float); return np.interp(tt, ks[:, 0], ks[:, 1])
SILENCES = [(e['t'], e['t'] + e['d']) for e in ev('silence')]

# ---------- pen on cold-press paper ----------
def pen(d, v=1., bright=1.):
    d = max(.03, d); n = int(d * SR); x = rng.standard_normal(n)
    fiber = lp(rng.standard_normal(n), 90); fiber = .55 + .45 * np.abs(fiber) / (np.abs(fiber).max() + 1e-9)
    grain = (rng.random(n) > .9975) * rng.standard_normal(n) * 4
    y = bp(x, 1600 * bright, min(SR / 2 - 200, 7500 * min(1.25, bright)), 2) * fiber + hp(grain, 2500)
    e = np.minimum(1, np.arange(n) / (.008 * SR)) * np.minimum(1, (n - np.arange(n)) / (.025 * SR))
    return (y * e * v * .22).astype(np.float32)
def strokes(t0, d, v=.8, bright=1.):
    t = t0
    while t < t0 + d:
        dd = .05 + rng.random() * .14; add(B['pen'], pen(min(dd, t0 + d - t + .02), v * (.8 + rng.random() * .4), bright), t, 1, rng.uniform(-.3, .3)); t += dd + .02 + rng.random() * .04
def write(t0, d, v=.75):              # handwriting: choppier rhythm, brighter
    t = t0
    while t < t0 + d:
        dd = .03 + rng.random() * .07; add(B['pen'], pen(dd, v * (.7 + rng.random() * .5), 1.15), t, 1, rng.uniform(-.1, .1)); t += dd + .012 + rng.random() * .03
        if rng.random() < .14: t += .07
for t0, du, L, g in C['strokes']:     # every world stroke at its real draw time
    if g == 0: v = .07 + min(.1, L / 5000)          # the Eden spread: hundreds of strokes pile into one hiss
    else: v = .25 + min(.15, L / 3000)              # the lower page: fewer, crisper strokes (the cross strokes stand out)
    if g == 1 and t0 > 47.2: v = .7
    add(B['pen'], pen(du, v, 1.25 if g else 1.0), t0, 1, rng.uniform(-.5, .5))
for e in ev('pen'): strokes(e['t'], e['d'], .75)
for e in ev('write'): write(e['t'], e['d'])

# ---------- watercolour ----------
def wet(d, v=1., lo=180, hi=2600):
    n = int(d * SR); x = rng.standard_normal(n)
    bub = lp(np.abs(rng.standard_normal(n)), 30); bub = bub / (bub.max() + 1e-9)
    y = bp(x, lo, hi, 2) * (.5 + .8 * bub); s = np.arange(n) / SR
    return (y * (1 - np.exp(-s / .06)) * np.exp(-s / (d * .45)) * v * .5).astype(np.float32)
for e in ev('bloom'): add(B['wash'], wet(1.4, .55 + .4 * e.get('g', 1)), e['t'], 1, rng.uniform(-.2, .2))
for e in ev('bloomBig'):            # colour spreading over the page: a long string of soft blooms
    t = e['t']
    while t < e['t'] + e['d']: add(B['wash'], wet(1.0 + rng.random(), .25 + rng.random() * .15), t, 1, rng.uniform(-.6, .6)); t += .35 + rng.random() * .4
for e in ev('drain'):               # colour lifting off: a dry brush dragging, falling in pitch
    n = int(e['d'] * SR); x = rng.standard_normal(n); s = np.arange(n) / SR
    y = np.zeros(n); step = 2400
    for i in range(0, n, step):
        fc = 2400 * np.exp(-s[i] / 2.2) + 300
        y[i:i + step] = sosfilt(butter(2, [fc * .5, fc * 1.4], 'band', fs=SR, output='sos'), x[max(0, i - 3000):i + step])[-len(x[i:i + step]):]
    scr = .5 + .5 * np.abs(lp(rng.standard_normal(n), 12)) / .05
    y = y * np.clip(scr, 0, 2) * np.minimum(1, s / .3) * np.exp(-s / (e['d'] * .6)) * .16
    add(B['wash'], y.astype(np.float32), e['t'], 1, 0)

# ---------- ambience ----------
room = lp(brown(DUR), 900) * .05 + hp(rng.standard_normal(N), 3000) * .002          # paper room tone, always there
add(B['amb'], room.astype(np.float32), 0, 1, 0)
def chirp(f0, f1, d, v):
    s = np.arange(int(d * SR)) / SR; f = np.linspace(f0, f1, len(s)); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.sin(np.pi * s / d) ** 2 * v).astype(np.float32)
def birds(t0, t1, dens=1.):
    t = t0
    while t < t1:
        f = 2600 + rng.random() * 2200; k = 2 + int(rng.random() * 4)
        for j in range(k): add(B['amb'], chirp(f * (1 + .15 * rng.random()), f * (.8 + .5 * rng.random()), .05 + rng.random() * .07, .045), t + j * (.09 + rng.random() * .05), 1, rng.uniform(-.8, .8))
        t += (.6 + rng.random() * 1.4) / dens
birds(3.0, 14.5); birds(57.5, 65.5, 1.2)
brook = bp(rng.standard_normal(N), 500, 3000) * (.5 + .5 * np.abs(lp(rng.standard_normal(N), 7)) / .05)
brook = np.clip(brook, -3, 3) * .012 * envk([(0, 0), (3.6, 0), (5, 1), (14.5, 1), (14.6, 0), (57, 0), (59, .8), (66, .8)])
add(B['amb'], brook.astype(np.float32), 0, 1, -.3)
wind = bp(brown(DUR) * .7 + rng.standard_normal(N) * .05, 200, 1100) * envk([(0, 0), (15.3, 0), (17, .35), (21.5, .4), (21.6, 0), (26.4, 0), (27, .25), (37, .3), (39, .55), (46.4, .6), (46.5, 0), (47.3, 0), (48, .4), (54, .25), (58, .1), (66, .08)])
add(B['amb'], (wind * .35).astype(np.float32), 0, 1, .15)

# ---------- foley ----------
def crunch(v):                     # a bite into a crisp fruit
    n = int(.16 * SR); s = np.arange(n) / SR; x = rng.standard_normal(n)
    clicks = np.zeros(n); idx = rng.choice(n // 2, 14, replace=False); clicks[idx] = rng.standard_normal(14) * 6
    y = bp(x, 1200, 6000) * np.exp(-s / .045) + hp(clicks, 1500) * .5 + lp(x, 400) * np.exp(-s / .03) * .8
    return (y * v * .5).astype(np.float32)
for e in ev('bite'): add(B['fx'], crunch(.6 + .6 * e.get('g', 1)), e['t'], 1, -.1)
for e in ev('pluck'):              # twig snap
    n = int(.05 * SR); s = np.arange(n) / SR; add(B['fx'], (hp(rng.standard_normal(n), 1800) * np.exp(-s / .008) * .35).astype(np.float32), e['t'], 1, -.2)
for e in ev('drop') + ev('thud'): add(B['fx'], (thump(.8, 85) * (.6 if e['type'] == 'drop' else .9)).astype(np.float32), e['t'], 1, 0)
def rustle(d, v):
    n = int(d * SR); s = np.arange(n) / SR; x = bp(rng.standard_normal(n), 900, 5000) * (np.abs(lp(rng.standard_normal(n), 25)) / .1)
    return (np.clip(x, -2, 2) * np.sin(np.pi * s / d) * v * .08).astype(np.float32)
for e in ev('rustle'): add(B['fx'], rustle(1.2, 1), e['t'], 1, .1)
for e in ev('cloth'): add(B['fx'], rustle(.8, .8), e['t'], 1, -.1)
for e in ev('whoosh'): add(B['fx'], (whoosh(.45, .5)).astype(np.float32), e['t'], 1, 0)
for e in ev('hiss'):               # the serpent: a dry breath of a hiss
    n = int(.9 * SR); s = np.arange(n) / SR; add(B['fx'], (bp(rng.standard_normal(n), 3500, 9000) * np.sin(np.pi * s / .9) ** 2 * .05).astype(np.float32), e['t'], 1, -.4)
for e in ev('slither'):
    n = int(e['d'] * SR); s = np.arange(n) / SR; x = bp(rng.standard_normal(n), 400, 2500) * (.6 + .4 * np.sin(2 * np.pi * 3.2 * s))
    add(B['fx'], (x * np.sin(np.pi * s / e['d']) * .05).astype(np.float32), e['t'], 1, .2)
def drip(v):
    s = np.arange(int(.25 * SR)) / SR; f = 900 + 1400 * np.exp(-s / .03); y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s / .05)
    return (y * v * .18).astype(np.float32)
for e in ev('drip'): add(B['fx'], drip(e.get('g', 1)), e['t'], 1, .25)
def step(v):
    n = int(.12 * SR); s = np.arange(n) / SR; x = rng.standard_normal(n)
    y = lp(x, 900) * np.exp(-s / .03) * .6 + bp(x, 1500, 5000) * np.exp(-s / .015) * .25
    return (y * v * .45).astype(np.float32)
for i, e in enumerate(ev('step')): add(B['fx'], step(.8 + .2 * (i % 2)), e['t'], 1, -.15 if i % 2 else .15)
for e in ev('flameIn'): add(B['fx'], (whoosh(.6, .7)).astype(np.float32), e['t'], 1, 0)
for e in ev('flame'):              # the flaming sword: a crackling roar while it turns
    n = int(e['d'] * SR); s = np.arange(n) / SR; x = rng.standard_normal(n)
    roar = lp(x, 500) * (.7 + .3 * np.sin(2 * np.pi * 1.5 / 6.28 * s * 6.28)) * .25
    crack = np.zeros(n); idx = rng.choice(n, int(e['d'] * 18), replace=False); crack[idx] = rng.standard_normal(len(idx)) * 3; crack = bp(crack, 1500, 7000) * .5
    env = np.minimum(1, s / .5) * np.minimum(1, (e['d'] - s) / 1.0)
    add(B['fx'], ((roar + crack) * env * .35).astype(np.float32), e['t'], 1, 0)
for e in ev('flameOut'): add(B['fx'], (whoosh(.9, .5)).astype(np.float32), e['t'], 1, 0)

# ---------- mix ----------
score, sr = sf.read(os.path.join(D, 'score.wav'), dtype='float32'); assert sr == SR
score = score[:N] if len(score) >= N else np.pad(score, ((0, N - len(score)), (0, 0)))
fol = B['pen'] * .9 + B['wash'] * 1.0 + B['fx'] * 1.0
fol = np.stack([hp(fol[:, 0], 90), hp(fol[:, 1], 90)], 1)
amb = B['amb']
# duck the music under the bites and the heel
duck = np.ones(N)
for e in ev('bite') + ev('thud'):
    duck *= 1 - .45 * np.exp(-np.maximum(0, tt - e['t']) / .35) * (tt >= e['t'] - .02)
music = score * duck[:, None] * .9
# true silences: everything off, then the next gesture
gate = np.ones(N)
for a, b in SILENCES: gate *= 1 - (np.clip((tt - a) / .03, 0, 1) * np.clip((b - tt) / .015, 0, 1))
mix = (music + fol * .75 + amb * .9) * gate[:, None]
mix = np.stack([limit(compress(mix[:, c], thr=.3, ratio=2.5), .95) for c in range(2)], 1)   # sfx dynamics work per channel
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
for k in B: sf.write(os.path.join(OUT, f'stem_{k}.wav'), B[k], SR)
print('mix.wav', round(N / SR, 2), 's, peak', round(float(np.abs(mix).max()), 3))
