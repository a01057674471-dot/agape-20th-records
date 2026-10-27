# 올리고파 — 120 bpm tuned-percussion build (Dark Tech Keynote score family), driven by audio/cues.json
# E major, C#m–A–E–B one chord per bar. Each section adds one layer: sine pulse → marimba → vibraphone + shaker →
# glockenspiel + hi-hat; digital silence before the chart; one chord lands on the title and rings to the end. CC0 samples (VSCO 2 CE, VCSL).
# run: LIB=<library> $LIB/.venv/bin/python audio/score.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf
from core.audio import sampler as S
from core.audio.sfx import SR, lp

D = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR)
E = {}
for e in C['ev']: E.setdefault(e['type'], []).append(e['t'])
SIL0 = E['silence'][0]; SIL1 = SIL0 + [e for e in C['ev'] if e['type'] == 'silence'][0]['d']
TITLE = E['chord'][0]
BEAT = .5; E8 = BEAT / 2; BAR = 4 * BEAT
S.seed(7)

PROG = [['C#4', 'E4', 'G#4', 'C#5'], ['A3', 'C#4', 'E4', 'A4'], ['E4', 'G#4', 'B4', 'E5'], ['B3', 'D#4', 'F#4', 'B4']]
ROOT = ['C#2', 'A1', 'E2', 'B1']
ROOT_HZ = [69.30, 55.0, 82.41, 61.74]
# section starts (seconds) from the picture's own beats
SEC = dict(num=0.0, cards=E['whoosh'][0], dive=E['expand'][0], mol=E['pop'][0], chart=SIL1, taste=E['sparkle'][0], prod=TITLE)
def layer(t):            # how many layers are playing at time t
    if t < SEC['cards']: return 0
    if t < SEC['dive']: return 1
    if t < SEC['mol']: return 2
    if t < SIL0: return 3
    if t < SEC['taste']: return 1
    return 3

ev = []
pulse = np.zeros((N, 2), np.float32)
def sine_pulse(t, f, v):             # low sine pulse on each eighth, the heartbeat of the build
    n = int(.22 * SR); s = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * s) * np.exp(-s / .09) * v
    y[:int(.004 * SR)] *= np.linspace(0, 1, int(.004 * SR))
    i = int(t * SR); m = min(n, N - i)
    if m > 0: pulse[i:i + m] += y[:m, None]

k = 0; t = .25
while t < TITLE - .01:
    if SIL0 - .01 <= t < SIL1: t += E8; k += 1; continue
    bar = int(t // BAR) % 4; tones = PROG[bar]; L = layer(t); step = k % 8
    sine_pulse(t, ROOT_HZ[bar], .55 if step % 2 == 0 else .3)
    if L >= 1:
        ev.append((t, 'marimba', tones[[0, 2, 1, 3, 2, 1, 3, 2][step]], E8 * 1.5, .34 if step % 4 == 0 else .26, -.25 + .15 * (step % 2)))
        if step == 0: ev.append((t, 'contrabass_pizz', ROOT[bar], 1.2, .4, 0))
    if L >= 2:
        if step == 0: ev += [dict(t=t, inst='vibraphone', pitch=p, dur=BAR, vel=.2, pan=.3) for p in tones[1:3]]
        ev.append((t, 'shaker', 'down' if step % 2 == 0 else 'up', .2, .22 if step % 2 else .3, .35))
    if L >= 3:
        if step in (3, 7): ev.append((t, 'glockenspiel', tones[3] if step == 3 else PROG[bar][2].replace('4', '5'), .8, .22, .4))
        ev.append((t, 'hihat', 'closed', .1, .16 if step % 2 else .22, -.35))
    t += E8; k += 1

# accents from the picture
for tl in E['lock'][:4]: ev.append((tl, 'glockenspiel', 'E6', .5, .26, .3))
ev.append((E['lock'][3], 'glockenspiel', 'B6', 1.0, .34, .3))
for i, tl in enumerate(E['snap'][:3]): ev.append((tl, 'xylophone', ['G#5', 'B5', 'E6'][i], .4, .3, -.3))
ev.append((E['pop'][0], 'timpani', 'E2', 1.5, .35, 0))
ev += [(E['split'][0], 'hand_chimes', p, 1.6, .35, pn) for p, pn in (('E5', -.3), ('B5', .3))]
for i, tb in enumerate(E['bar']): ev += [(tb, 'marimba', ['E3', 'G#3', 'B3'][i], .6, .45, 0), (tb, 'contrabass_pizz', ['E2', 'G#2', 'B2'][i], .8, .4, 0)]
hb = E['barHero'][0]
ev += [(hb, 'timpani', 'E2', 1.8, .5, 0), (hb, 'tubular_bells', 'E5', 2.0, .3, .2)]
ev += [dict(t=E['lock'][-1], inst='vibraphone', pitch=p, dur=2.5, vel=.32, pan=.2) for p in ('E4', 'G#4', 'B4', 'E5')]
ev.append((E['sparkle'][0], 'glockenspiel', 'B6', 1.0, .32, .4))
# the title chord: everything lands on E major and rings out
ring = DUR - TITLE
ev += [dict(t=TITLE, inst=i, pitch=p, dur=ring, vel=v, pan=pn) for i, p, v, pn in [
    ('vibraphone', 'E4', .34, .2), ('vibraphone', 'G#4', .3, .2), ('vibraphone', 'B4', .3, .2), ('vibraphone', 'E5', .28, .2),
    ('marimba', 'E3', .45, -.2), ('contrabass_pizz', 'E2', .5, 0), ('glockenspiel', 'E7', .3, .35), ('tubular_bells', 'E5', .3, -.3), ('timpani', 'E2', .45, 0)]]

mix = S.render(ev, dur=DUR, master=False)
mix = S.room(mix, size=.32, mix=.13)
p = lp(pulse[:, 0], 400); mix += np.stack([p, p], 1) * (np.abs(mix).max() / (np.abs(p).max() + 1e-9)) * .5
# digital silence: nothing from before carries into it
a, b = int(SIL0 * SR), int(SIL1 * SR); f = int(.012 * SR)
mix[a - f:a] *= np.linspace(1, 0, f)[:, None]; mix[a:b] = 0
k = int(1.2 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None] ** 1.5
mix = mix / np.abs(mix).max() * .8
sf.write(os.path.join(D, 'score.wav'), mix.astype(np.float32), SR)
names = sorted({(e['inst'] if isinstance(e, dict) else e[1]) for e in ev})
json.dump(names, open(os.path.join(D, 'instruments.json'), 'w'))
print('score.wav', DUR, 's;', ', '.join(names))
