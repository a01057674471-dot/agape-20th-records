# 동산의 동편 — original score from the cue map (TREATMENT.md §6): 72 bpm in 3/4, D major → B minor → D major
# nylon guitar (modelled), harp, flute, clarinet, cellos, violas, violins, contrabass, hand chimes, timpani — all CC0 samples or synthesis
# run: LIB=<library> $LIB/.venv/bin/python audio/score.py
import os, sys
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf
from core.audio import sampler as S, pluck as P
from core.audio.sfx import SR, add

D = os.path.dirname(os.path.abspath(__file__))
DUR = 66.0; N = int(DUR * SR)
BEAT = 60 / 72; BAR = 3 * BEAT; E8 = BEAT / 2
S.seed(11)
mix = np.zeros((N, 2), np.float32)
ev = []                                   # sampled events: (t, inst, pitch, dur, vel, pan[, gain])

CH = {  # guitar voicings: bass, then the upper tones the arpeggio walks through
  'D': ['D3', 'A3', 'D4', 'F#4'], 'Bm': ['B2', 'F#3', 'B3', 'D4'], 'G': ['G2', 'D3', 'G3', 'B3'], 'A': ['A2', 'E3', 'A3', 'C#4'],
  'Em': ['E3', 'B3', 'E4', 'G4'], 'F#m': ['F#2', 'C#3', 'F#3', 'A3'], 'F#': ['F#2', 'C#3', 'F#3', 'A#3'], 'D/F#': ['F#2', 'A3', 'D4', 'F#4'],
}
PAT = [0, 1, 2, 3, 2, 1]                 # six eighths in a bar of three
def guitar_bar(t0, chord, vel=.55, n=6, pan=-.25):
    tones = CH[chord]
    for i in range(n):
        p = tones[PAT[i]]; v = vel * (1.0 if i == 0 else .72) * (.92 + .16 * ((i * 37) % 7) / 7)
        add(mix, P.pluck('nylon_guitar', p, None, vel=v), t0 + i * E8 + (.004 * (i % 2)), .55, pan)
def bar(n): return (n - 1) * BAR       # bar 1 starts at 0

# ---------- Eden (bars 1–4, 0–10): guitar, then the flute when the colour arrives ----------
for n, c in [(2, 'D'), (3, 'Bm'), (4, 'G')]:
    guitar_bar(bar(n), c, .5 if n == 2 else .55)
ev += [(1.0, 'hand_chimes', 'A5', 2.5, .38, .2)]                          # the fruit turns red: the one coloured thing
for i, p in enumerate(['D4', 'F#4', 'A4', 'D5', 'F#5']):                # colour arrives: a soft harp run
    ev.append((3.6 + i * .09, 'harp', p, 2.0, .38, .35))
ev += [(5.0, 'flute', 'D5', 1.55, .42, .15), (6.67, 'flute', 'B4', .8, .38, .15), (7.5, 'flute', 'C#5', 1.15, .4, .15), (8.75, 'flute', 'E5', .4, .38, .15), (9.17, 'flute', 'D5', .8, .36, .15)]
ev += [(bar(2), 'cellos', 'D3', 2.4, .22, .25), (bar(3), 'cellos', 'B2', 2.4, .22, .25), (bar(4), 'cellos', 'G2', 2.4, .22, .25)]

# ---------- Temptation (bars 5–6, 10–14.6): guitar thins, low clarinet, a bass pedal; then silence ----------
guitar_bar(bar(5), 'Em', .38, 6)
add(mix, P.pluck('nylon_guitar', 'A2', None, vel=.4), bar(6), .5, -.2)
add(mix, P.pluck('nylon_guitar', 'E3', None, vel=.3), bar(6) + BEAT, .5, -.2)
ev += [(10.0, 'clarinet', 'E4', 2.3, .34, -.1), (12.5, 'clarinet', 'D4', 1.5, .32, -.1), (14.0, 'clarinet', 'C#4', .55, .28, -.1)]
ev += [(10.0, 'contrabass', 'A1', 4.5, .2, 0, .8)]

# ---------- The bite and the drain (bars 7–9, 15–21.6): B minor, pizzicato, low clarinet ----------
ev += [(15.0, 'timpani', 'B2', 2.5, .55, 0), (15.0, 'cellos', 'B2', 6.4, .3, .1), (15.0, 'contrabass', 'B1', 6.4, .22, 0, .8)]
for i, (dt, p) in enumerate([(0, 'F#3'), (1, 'D3'), (3, 'B2'), (4, 'F#3'), (6, 'G3'), (7, 'E3'), (9, 'F#3'), (10, 'C#3')]):
    ev.append((15.83 + dt * BEAT, 'cellos_pizz', p, .8, .42 - .015 * i, -.15))
ev += [(17.5, 'clarinet', 'B3', 1.2, .3, .1), (18.75, 'clarinet', 'A3', .8, .28, .1), (19.58, 'clarinet', 'G3', 1.0, .27, .1), (20.6, 'clarinet', 'F#3', .95, .25, .1)]

# ---------- The call and the promise (bars 10–12, 22.5–30) ----------
ev += [(22.7, 'cellos', 'D2', 3.7, .3, 0), (22.7, 'contrabass', 'D2', 3.7, .18, 0, .7)]
ev += [(26.6, 'cellos', 'D3', 3.6, .2, .1), (26.6, 'violas', 'A3', 3.6, .14, -.1)]
MOTIF = ['F#5', 'A5', 'B5', 'D6']                                        # the promise: four rising notes
for i, p in enumerate(MOTIF):
    ev.append((27.5 + i * BEAT, 'flute', p, BEAT * (1.9 if i == 3 else .95), .3 + .03 * i, .1))

# ---------- Garments of skin (bars 13–15, 30–37.5): the guitar returns, warmer ----------
for n, c in [(13, 'G'), (14, 'D'), (15, 'Em')]: guitar_bar(bar(n), c, .45)
ev += [(30.0, 'cellos', 'G2', 2.4, .2, .2), (32.5, 'cellos', 'D3', 2.4, .2, .2), (35.0, 'cellos', 'E3', 2.4, .2, .2)]
ev += [(34.2, 'hand_chimes', 'F#5', 2.0, .3, .3)]
for i, p in enumerate(['E4', 'G4', 'B4', 'D5', 'E5', 'G5']):            # the garments bloom: harp gliss
    ev.append((35.3 + i * .07, 'harp', p, 2.0, .35, .35))

# ---------- Exile (bars 16–19, 37.5–46.5): pulse in pizzicato, clarinet, footfalls on the beat ----------
EX = [('Bm', 'B2'), ('G', 'G2'), ('Em', 'E2'), ('F#', 'F#2')]
for k, (c, root) in enumerate(EX):
    t0 = 37.5 + k * BAR
    for b in range(3):
        tb = t0 + b * BEAT
        if tb >= 46.4: break
        ev.append((tb, 'cellos_pizz', root if b == 0 else CH[c][1], .7, .4 if b == 0 else .3, -.2))
        if b == 0: ev.append((tb, 'contrabass_pizz', root.replace('2', '1') if root != 'B2' else 'B1', .9, .45, 0))
    ev.append((t0, 'cellos', root.replace('2', '3'), BAR * .95, .16, .2))
ev += [(38.33, 'clarinet', 'F#4', 1.55, .34, .1), (40.0, 'clarinet', 'E4', .8, .32, .1), (40.83, 'clarinet', 'D4', 1.55, .32, .1), (42.5, 'clarinet', 'B3', 2.3, .3, .1), (45.0, 'clarinet', 'C#4', 1.25, .3, .1)]

# ---------- The cross (bar 20, 47.5–50): the promise in full ----------
for i, p in enumerate(MOTIF):
    ev.append((47.5 + i * BEAT, 'flute', p, BEAT * (2.4 if i == 3 else .98), .42 + .04 * i, .1))
guitar_bar(47.5, 'D', .5)
ev += [(48.8, 'hand_chimes', 'D6', 3.0, .4, .2), (48.8, 'hand_chimes', 'A5', 3.0, .3, -.2)]
for i, p in enumerate(['D4', 'F#4', 'A4', 'D5', 'F#5', 'A5', 'D6']):
    ev.append((48.8 + i * .06, 'harp', p, 2.5, .42, .3))
ev += [dict(t=49.0, inst='violins', pitch='F#4', dur=1.4, vel=.25, pan=.3, attack=1.0), dict(t=49.0, inst='violas', pitch='D4', dur=1.4, vel=.22, pan=-.2, attack=1.0), dict(t=49.0, inst='cellos', pitch='D3', dur=1.4, vel=.28, pan=0, attack=.8)]

# ---------- Return (bars 21–25, 50–66): D major, everything, a last chord ----------
PROG = [(21, 'G', ['G2', 'D3'], ['B3', 'D4'], ['G4', 'B4']), (22, 'D/F#', ['F#2', 'D3'], ['A3', 'D4'], ['F#4', 'A4']), (23, 'Bm', ['B2', 'F#3'], ['B3', 'D4'], ['F#4', 'B4']), (24, 'A', ['A2', 'E3'], ['A3', 'C#4'], ['E4', 'A4'])]
for n, c, lo, mid, hi in PROG:
    t0 = bar(n); guitar_bar(t0, c, .55)
    for p in lo: ev.append(dict(t=t0, inst='cellos', pitch=p, dur=BAR, vel=.3, pan=.1, attack=.15))
    for p in mid: ev.append(dict(t=t0, inst='violas', pitch=p, dur=BAR, vel=.24, pan=-.15, attack=.15))
    for p in hi: ev.append(dict(t=t0, inst='violins', pitch=p, dur=BAR, vel=.26 + .02 * (n - 21), pan=.3, attack=.2))
    ev.append((t0, 'contrabass_pizz', lo[0].replace('2', '1') if lo[0][-1] == '2' else lo[0], 1.2, .4, 0))
MEL = [(50.0, 'B5', 1.6), (51.67, 'A5', .8), (52.5, 'F#5', 1.6), (54.17, 'D5', .8), (55.0, 'D5', .8), (55.83, 'E5', .8), (56.67, 'F#5', .8), (57.5, 'E5', 2.4)]
ev += [(t, 'flute', p, d * .97, .44, .1) for t, p, d in MEL]
# the last chord at 60 (bar 25): rings to the end
ev += [dict(t=60.0, inst='cellos', pitch='D3', dur=5.2, vel=.3, pan=.1), dict(t=60.0, inst='contrabass', pitch='D2', dur=5.2, vel=.2, pan=0),
       dict(t=60.0, inst='violas', pitch='A3', dur=5.2, vel=.24, pan=-.15), dict(t=60.0, inst='violins', pitch='F#4', dur=5.2, vel=.24, pan=.3), dict(t=60.0, inst='violins', pitch='D5', dur=5.2, vel=.2, pan=.3),
       dict(t=60.0, inst='flute', pitch='D5', dur=4.6, vel=.36, pan=.1), (60.0, 'hand_chimes', 'D6', 4.0, .34, .2), (60.0, 'contrabass_pizz', 'D1', 1.5, .4, 0)]
for i, p in enumerate(['D3', 'A3', 'D4', 'F#4', 'A4', 'D5']):
    ev.append((60.0 + i * .08, 'harp', p, 5.0, .4, .3))
add(mix, P.strum('nylon_guitar', ['D3', 'A3', 'D4', 'F#4', 'A4'], 5.5, vel=.5, spread=.05), 60.02, .5, -.25)
# one more guitar arpeggio, fading, over the final verse
for i, p in enumerate(['D4', 'F#4', 'A4', 'D5']):
    add(mix, P.pluck('nylon_guitar', p, None, vel=.32 - .04 * i), 62.5 + i * E8 * 1.5, .5, -.25)

mix += S.render(ev, dur=DUR, master=False)
mix = S.room(mix, size=.55, mix=.2)
# fade out the last second
fade = np.ones(N, np.float32); k = int(1.2 * SR); fade[-k:] = np.linspace(1, 0, k) ** 1.5; mix *= fade[:, None]
pk = np.abs(mix).max(); mix = mix / pk * .8 if pk > 0 else mix
sf.write(os.path.join(D, 'score.wav'), mix, SR)
names = sorted({(e['inst'] if isinstance(e, dict) else e[1]) for e in ev})
open(os.path.join(D, 'instruments.json'), 'w').write(__import__('json').dumps(names))
print('score.wav', round(N / SR, 2), 's; instruments:', ', '.join(names))
