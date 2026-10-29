# 깻잎인 줄 알았던 그 잎 — the user's narration + chamber score + printmaking foley, one file → out/mix.wav
# 100 bpm, G major (G–D/F♯–Em–C). Harpsichord arpeggios carry it; pizzicato strings join on the second plate; a held cello
# under the lab plate; a glockenspiel ting when the balance levels; one cadence on the last plate that rings out.
# Foley follows the materials: burin hiss while a photograph is engraved, a sheet laid on the bed at every plate,
# a water plip and brush swish when the colour blooms, a tick for every cut letter, a scribed ring for each roundel.
# run: LIB=<library> $LIB/.venv/bin/python audio/score.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio import sampler as S
from core.audio.sfx import SR, add, bp, hp, lp, limit, noise, t_, env_exp, norm, whoosh, brown

D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..'); OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR); BEAT = .6; E8 = BEAT / 2
S.seed(4); rng = np.random.default_rng(4)
sheets = sorted(e['t'] for e in C['ev'] if e['type'] in ('start', 'sheet'))      # plate starts: 0, 4.6, 9.0, 13.8, 19.0, 24.4
def plate(t): return max(i for i, s in enumerate(sheets) if t >= s - 1e-6)
PROG = [['G3', 'B3', 'D4', 'G4'], ['F#3', 'A3', 'D4', 'F#4'], ['E3', 'G3', 'B3', 'E4'], ['C3', 'E3', 'G3', 'C4']]
BASS = ['G2', 'F#2', 'E2', 'C2']
ev = []
END = sheets[-1] + 3.6          # the cadence on the last plate

# ---------- the arpeggio bed ----------
k = 0; t = .3
while t < END - .01:
    pl = plate(t); bar = int(t // (4 * BEAT)) % 4; ch = PROG[bar]; step = k % 8
    if pl == 0 and step % 2: t += E8; k += 1; continue                          # the hook: half density, the burin leads
    ev.append((t, 'harpsichord', ch[[0, 2, 1, 3, 2, 1, 3, 2][step]] if pl != 3 else ch[step % 4], E8 * 1.8, .5 if step % 4 == 0 else .38, -.2 + .1 * (step % 3)))
    if step == 0: ev.append((t, 'harpsichord', BASS[bar], 2.0, .5, 0))
    if pl in (1, 2, 4) and step in (2, 6): ev.append((t, 'violins_pizz', ch[3], .4, .4, .35))
    if pl in (1, 4, 5) and step in (0, 4): ev.append((t, 'cellos_pizz', BASS[bar].replace('2', '3'), .5, .45, -.3))
    if pl == 3 and step == 0: ev.append(dict(t=t, inst='cellos', pitch=BASS[bar], dur=4 * BEAT, vel=.32, pan=-.1))
    t += E8; k += 1
# the cadence: D → G, held to the end
ev += [dict(t=END - 1.2, inst='harpsichord', pitch=p, dur=1.2, vel=.45, pan=.1) for p in ('D3', 'A3', 'D4', 'F#4')]
ev += [dict(t=END, inst=i, pitch=p, dur=DUR - END, vel=v, pan=pn) for i, p, v, pn in
       [('harpsichord', 'G2', .55, 0), ('harpsichord', 'D3', .45, 0), ('harpsichord', 'B3', .45, .1), ('harpsichord', 'G4', .45, .1),
        ('cellos', 'G2', .32, -.1), ('violins_pizz', 'G5', .4, .35), ('glockenspiel', 'G6', .3, .3)]]
# accents from the picture
for e in C['ev']:
    if e['type'] == 'reveal': ev.append((e['t'], 'glockenspiel', 'D6', 1.2, .35, .3)); ev.append((e['t'] + .05, 'glockenspiel', 'G6', 1.2, .3, .3))
    if e['type'] == 'roundel': ev.append((e['t'] + .3, 'glockenspiel', 'B5', 1.0, .26, .35))
    if e['type'] == 'level': ev += [(e['t'], 'glockenspiel', p, 1.6, .32, .3) for p in ('G5', 'D6')]
    if e['type'] == 'loupe': ev.append((e['t'] + .3, 'violins_pizz', 'D5', .3, .4, .3))
music = S.render(ev, dur=DUR, master=False)
music = S.room(music, size=.3, mix=.14)

# ---------- foley ----------
fol = np.zeros((N, 2))
def burin(d):                      # the graver through copper: high band-passed hiss, chatter, a faint ring
    n = noise(d); x = bp(n, 4500, 11000) * .6 + bp(n, 1800, 3500) * .2
    ch = 1 + .6 * (np.sin(2 * np.pi * 23 * t_(d)) > .6); x = x * ch
    u = np.linspace(0, 1, len(x)); x *= np.minimum(1, u * 8) * np.minimum(1, (1 - u) * 6)
    return x + np.sin(2 * np.pi * 5200 * t_(d)) * .02
def sheet():                       # a damp sheet laid on the bed: air whoosh and a soft slap
    d = .35; tt = t_(d)
    return norm(lp(noise(d), 900) * env_exp(d, .05) + np.sin(2 * np.pi * 105 * tt) * env_exp(d, .05) * .5 + hp(noise(d), 2500) * env_exp(d, .01) * .3)
def plip():                        # a brush into water
    d = .25; tt = t_(d); f = 900 + 1600 * np.exp(-tt / .02)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, .04) + bp(noise(d), 1500, 6000) * env_exp(d, .015) * .3)
def swish(d=.7):                   # the wet brush across paper
    u = np.linspace(0, 1, int(d * SR)); return bp(noise(d), 1200, 6000) * np.sin(np.pi * u) ** 1.5 * .5
def tick():                        # a letter cut
    d = .025; tt = t_(d); return norm(np.sin(2 * np.pi * 3800 * tt) * env_exp(d, .003) + hp(noise(d), 6000) * env_exp(d, .001) * .5)
def scribe(d=.4):                  # the compass point scribing a ring
    u = np.linspace(0, 1, int(d * SR)); return bp(noise(d), 5000, 12000) * np.sin(np.pi * u) * .6
for e in C['ev']:
    t, k = e['t'], e['type']
    if k == 'burin': add(fol, burin(e['d']), t, .55, .15)
    if k == 'sheet': add(fol, whoosh(.3), t - .2, .3, 0); add(fol, sheet(), t + .25, .55, 0)
    if k == 'wash': add(fol, plip(), t, .45, .2); add(fol, swish(), t + .1, .4, -.1)
    if k == 'letter':
        for j in range(4): add(fol, tick(), t + j * .07, .18 * (1 - j * .15), float(rng.uniform(-.3, .3)))
    if k in ('roundel', 'leader'): add(fol, scribe(.4 if k == 'roundel' else .25), t, .4, .25)
    if k == 'loupe': add(fol, whoosh(.35), t, .25, 0)
room = lp(brown(DUR), 250)[:N] * .006; fol[:, 0] += room; fol[:, 1] += room

rms = lambda x: float(np.sqrt((x ** 2).mean()) + 1e-9)
# the narration (voices/narration.wav, laid by tools/voice.py) leads; music ~14 dB under it, ducked a further 4 dB while it speaks
v, sr = sf.read(os.path.join(ROOT, 'voices', 'narration.wav'), dtype='float32'); v = v.mean(1) if v.ndim > 1 else v
if sr != SR: v = soxr.resample(v, sr, SR)
voice = np.zeros((N, 2)); add(voice, v[:N], 0, 1, 0)
act = np.convolve((np.abs(voice[:, 0]) > 2e-3).astype(float), np.ones(int(.2 * SR)) / int(.2 * SR), 'same')
duck = 1 - .37 * np.clip(act * 3, 0, 1)
vr = rms(voice[np.abs(voice[:, 0]) > 2e-3])
mix = voice + music / rms(music) * vr * 10 ** (-14 / 20) * duck[:, None] + fol / rms(fol) * vr * 10 ** (-13 / 20)
k = int(1.0 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None] ** 1.5

import subprocess, tempfile, re
def lufs(x):
    with tempfile.NamedTemporaryFile(suffix='.wav') as fh:
        sf.write(fh.name, x.astype(np.float32), SR)
        out = subprocess.run(['ffmpeg', '-nostats', '-i', fh.name, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', out)[-1])
from scipy.signal import butter, sosfiltfilt
mix = sosfiltfilt(butter(8, 15000, 'low', fs=SR, output='sos'), mix, axis=0)
for _ in range(3):
    mix = mix * 10 ** ((-14 - lufs(mix)) / 20)
    up = soxr.resample(mix, SR, SR * 4)
    up = np.stack([limit(up[:, c], .7) for c in range(2)], 1)
    mix = soxr.resample(up, SR * 4, SR)[:len(mix)]
print('mastered to', lufs(mix), 'LUFS')
# 32 s of trailing silence: mux.sh's decode check runs ~2.9 s behind and allows 5 % of the length; build.sh trims back to the picture
mix = np.concatenate([mix, np.zeros((32 * SR, 2))])
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
names = sorted({(e['inst'] if isinstance(e, dict) else e[1]) for e in ev})
json.dump(names, open(os.path.join(D, 'instruments.json'), 'w'))
print('mix.wav', DUR, 's;', ', '.join(names))
