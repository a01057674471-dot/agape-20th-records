# AHCC whiteboard — clockwork-minimal score that follows the narration lines (audio/cues.json)
# marimba ostinato + pizzicato bass + glockenspiel pings on the key facts; a full stop into silence before "not a medicine";
# A minor for the cautions; back to C major for the checklist and the end. CC0 samples (VSCO 2 CE, VCSL).
# run: LIB=<library> $LIB/.venv/bin/python audio/score.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf
from core.audio import sampler as S
from core.audio.sfx import SR

D = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR)
V = {l['id']: l for l in C['lines']}
at = lambda i, u: V[i]['t0'] + V[i]['d'] * u
BEAT = 60 / 100; E8 = BEAT / 2
S.seed(5)
ev = []

PROG_MAJ = [['C4', 'G4', 'E5', 'G4'], ['A3', 'E4', 'C5', 'E4'], ['F3', 'C4', 'A4', 'C4'], ['G3', 'D4', 'B4', 'D4']]
BASS_MAJ = ['C2', 'A1', 'F2', 'G2']
PROG_MIN = [['A3', 'E4', 'C5', 'E4'], ['F3', 'C4', 'A4', 'C4'], ['D4', 'A4', 'F5', 'A4'], ['E3', 'B3', 'G#4', 'B3']]
BASS_MIN = ['A1', 'F1', 'D2', 'E2']
def ostinato(t0, t1, prog, bass, vel=.34, layer=0):
    k = 0; t = t0
    while t < t1 - .05:
        bar = (k // 8) % 4; tones = prog[bar]
        ev.append((t, 'marimba', tones[k % 4], E8 * 1.6, vel * (1.0 if k % 4 == 0 else .78), -.25 + .15 * (k % 2)))
        if k % 8 == 0: ev.append((t, 'contrabass_pizz', bass[bar], 1.2, .42, 0))
        if layer and k % 8 == 4: ev.append((t, 'violins_pizz', tones[2], .5, .3, .35))
        if layer > 1 and k % 8 == 0: ev.append(dict(t=t, inst='vibraphone', pitch=tones[1], dur=BEAT * 4, vel=.22, pan=.3))
        t += E8; k += 1

# intro and explanation (v01–v05): C major, grows by one layer as the mechanism unfolds
ostinato(.3, V['v03']['t0'], PROG_MAJ, BASS_MAJ, .3, 0)
ostinato(V['v03']['t0'], V['v04']['t0'], PROG_MAJ, BASS_MAJ, .32, 1)
ostinato(V['v04']['t0'], V['v05']['t1'] + .1, PROG_MAJ, BASS_MAJ, .34, 2)
# pings on the numbers
ev += [(at('v01', .3), 'glockenspiel', 'E6', 1.2, .35, .3), (at('v02', .76), 'glockenspiel', 'G6', 1.2, .35, .3), (at('v04', .78), 'glockenspiel', 'C7', 1.4, .42, .3), (at('v05', .84), 'glockenspiel', 'G6', 1.4, .34, -.2)]
ev += [(at('v03', .12), 'xylophone', 'C6', .4, .35, .4)]                  # the magnet drops
# a full stop into silence, then sparse A minor for "not a medicine" and "not the same ingredient"
t6 = V['v06']['t0']
ev += [(t6, 'contrabass_pizz', 'A1', 1.4, .5, 0), (t6, 'cellos', 'A2', V['v07']['t1'] - t6, .16, 0)]
k = 0; t = t6 + BEAT
while t < V['v07']['t1']:
    bar = (k // 4) % 4; ev.append((t, 'marimba', PROG_MIN[bar][k % 4], BEAT * 1.2, .26, -.2)); t += BEAT; k += 1
ev += [(at('v06', .84), 'glockenspiel', 'E6', 1.2, .32, .3)]
# the checklist: C major returns, one ping per tick; then the double circle and a last chord
ostinato(V['v08']['t0'], V['v09']['t1'] + 1.0, PROG_MAJ, BASS_MAJ, .3, 1)
for i in range(3): ev.append((at('v08', .45 + i * .23), 'glockenspiel', ['C6', 'E6', 'G6'][i], 1.0, .34, .3))
tc = at('v09', .84)
ev += [dict(t=tc, inst='vibraphone', pitch=p, dur=2.4, vel=.3, pan=.2) for p in ['C4', 'E4', 'G4', 'C5']]
te = V['v09']['t1'] + 1.0
ev += [dict(t=te, inst=i, pitch=p, dur=DUR - te, vel=v, pan=pn) for i, p, v, pn in [('vibraphone', 'C4', .3, .2), ('vibraphone', 'G4', .28, .2), ('vibraphone', 'E5', .26, .2), ('marimba', 'C3', .4, -.2), ('contrabass_pizz', 'C2', .45, 0), ('glockenspiel', 'C7', .35, .3)]]

mix = S.render(ev, dur=DUR, master=False)
mix = S.room(mix, size=.35, mix=.14)
k = int(1.0 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None] ** 1.5
pk = np.abs(mix).max(); mix = mix / pk * .8
sf.write(os.path.join(D, 'score.wav'), mix.astype(np.float32), SR)
names = sorted({(e['inst'] if isinstance(e, dict) else e[1]) for e in ev})
json.dump(names, open(os.path.join(D, 'instruments.json'), 'w'))
print('score.wav', DUR, 's;', ', '.join(names))
