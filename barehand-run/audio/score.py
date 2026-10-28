# 맨손 겨울 러닝 — the user's narration + picture-locked score + foley, one file → out/mix.wav
# 150 bpm, D minor (Dm–B♭–F–C, one chord per bar). A running groove (kick, snare, 16th hats, a shaker for the stride, finger bass),
# glockenspiel for the ice. Each card sets the density; the picture's events (audio/cues.json) place every accent.
# Foley keeps attention on the screen: a whoosh and a low hit on every cut, a tick on every line that slides up, a riser into
# the half beat of silence before the twist. The voice leads; music sits ~14 dB under it. CC0 / CC BY samples (see CREDITS).
# run: LIB=<library> $LIB/.venv/bin/python audio/score.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio import sampler as S
from core.audio.sfx import SR, add, bp, hp, lp, limit, noise, t_, env_exp, norm, whoosh

D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..'); OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR); BEAT = .4; S16 = BEAT / 4
S.seed(11); rng = np.random.default_rng(11)
cut = {e['card']: e['t'] for e in C['ev'] if e['type'] == 'cut'}
sil = [e for e in C['ev'] if e['type'] == 'silence'][0]; SIL0, SIL1 = sil['t'], sil['t'] + sil['d']
order = sorted(cut, key=cut.get)
def card(t):
    k = order[0]
    for c in order:
        if t >= cut[c] - 1e-6: k = c
    return k
PROG = [('D2', ['D4', 'F4', 'A4']), ('A#1', ['A#3', 'D4', 'F4']), ('F2', ['F3', 'A3', 'C4']), ('C2', ['C4', 'E4', 'G4'])]
ev = []
kit = lambda t, v, vel, pan=0: ev.append(dict(t=t, inst='drum_kit', pitch=v, vel=vel, pan=pan))

# ---------- the groove, step by step on sixteenths ----------
DENS = {'hook': 2, 'wind': 3, 'finger': 1, 'study': 1, 'result': 2, 'twist': 0, 'check': 3, 'cta': 3}
END = DUR - .8
n16 = int(END / S16)
for i in range(n16):
    t = i * S16
    if SIL0 - 1e-6 <= t < SIL1: continue
    c = card(t); d = DENS[c]; step = i % 16; beat = i // 4; bar = (i // 16) % 4
    root, chord = PROG[bar]
    if c == 'twist':                         # half time: kick on 1, snare on 3, long bass
        if step == 0: kit(t, 'kick_drum_left', .9); ev.append((t, 'electric_bass', root, 2.0, .8, 0))
        if step == 8: kit(t, 'snare_1', .75)
        if step % 4 == 0: kit(t, 'hi_hat_closed', .25, .3)
        continue
    if d >= 1:
        if step % 4 == 0 and (d >= 2 or step in (0, 8)): kit(t, 'kick_drum_left', .85)
        if step in (4, 12) and d >= 2: kit(t, 'snare_1', .7)
        if d >= 2 and step == 14: kit(t, 'kick_drum_right', .55)
        hat = (d >= 3) or (step % 2 == 0)
        if hat: kit(t, 'hi_hat_open' if (d >= 3 and step == 6) else 'hi_hat_closed', .32 if step % 4 == 0 else .2, .35)
        if d >= 3: ev.append((t, 'shaker', 'down' if step % 2 == 0 else 'up', .15, .22, -.3))
        if step % 2 == 0: ev.append((t, 'electric_bass', root if step % 8 != 6 else PROG[bar][0].replace('2', '3').replace('1', '2'), .22, .62 if step % 4 == 0 else .5, 0))
    if d >= 2 and step == 0: ev += [dict(t=t, inst='vibraphone', pitch=p, dur=2.0, vel=.16, pan=.25) for p in chord]

# ---------- accents from the picture ----------
GL = lambda t, p, v=.32, d=1.0, pan=.35: ev.append((t, 'glockenspiel', p, d, v, pan))
for e in C['ev']:
    t, k = e['t'], e['type']
    if k == 'cut' and e['card'] != 'twist':
        kit(t, 'crash_left' if e['i'] % 2 == 0 else 'crash_right', .55)
    if k == 'cut' and e['card'] == 'hook':
        for j, p in enumerate(['D6', 'F6', 'A6', 'D7']): GL(t + .25 + j * BEAT * .5, p, .3)
    if k == 'slam':
        for j, tm in enumerate(['tom_1', 'tom_2', 'tom_3']): kit(t - S16 * (3 - j), tm, .5 + j * .1)
        kit(t, 'kick_drum_left', 1.0); GL(t, ['A5', 'F5', 'D5', 'D6'][e['k']], .38)
    if k == 'warn': kit(t, 'china', .7)
    if k == 'drop':
        for j, p in enumerate(['A5', 'F5', 'D5']): GL(t + j * S16, p, .3, .6)
        kit(t, 'tom_4', .7)
    if k == 'numb': kit(t, 'china', .6); GL(t, 'D7', .3)
    if k == 'vs': kit(t, 'tom_2' if e['k'] == 0 else 'tom_3', .7); ev.append(dict(t=t, inst='claps', pitch='group', vel=.5, pan=0))
    if k == 'gauge':
        for j, p in enumerate(['D6', 'A5', 'F5', 'D5']): GL(t + j * e['d'] / 3, p, .3, .8)
    if k == 'count': ev.append((t, 'glockenspiel', 'D6' if e['d'] < 14 else 'D7', .25, .14 if e['d'] < 14 else .4, .4))
    if k == 'row': kit(t, 'snare_2', .55); GL(t, ['F6', 'C5'][e['k']], .34)
    if k == 'check': ev.append(dict(t=t, inst='claps', pitch='group', vel=.6, pan=0)); GL(t, 'A6', .34)
ev.append(dict(t=SIL1, inst='timpani', pitch='D2', dur=2.5, vel=.8, pan=0)); kit(SIL1, 'crash_left', .9); kit(SIL1, 'kick_drum_left', 1.0)
ev += [dict(t=SIL1, inst='vibraphone', pitch=p, dur=3.5, vel=.25, pan=.2) for p in ('D3', 'A3', 'F4')]
ev += [dict(t=END, inst=i, pitch=p, dur=DUR - END, vel=v, pan=pn) for i, p, v, pn in
       [('vibraphone', 'D4', .3, .2), ('vibraphone', 'F4', .28, .2), ('vibraphone', 'A4', .28, .2), ('glockenspiel', 'D7', .35, .35), ('electric_bass', 'D2', .7, 0)]]
kit(END, 'crash_right', .8); kit(END, 'kick_drum_left', .95)

music = S.render(ev, dur=DUR, master=False)
music = S.room(music, size=.22, mix=.08)

# ---------- foley ----------
fol = np.zeros((N, 2))
def wind(d):                                    # the headwind: band-passed noise swelling with each wind step
    x = bp(noise(d), 300, 4000) * .5 + bp(noise(d), 2500, 7000) * .25
    u = np.linspace(0, 1, len(x)); return x * np.minimum(1, u * 6) * np.minimum(1, (1 - u) * 6)
def crack():                                    # ice crack for the −27 warning
    d = .35; tt = t_(d); x = hp(noise(d), 1500) * env_exp(d, .012) * (1 + (rng.random(len(tt)) > .97) * 3)
    return norm(x + np.sin(2 * np.pi * 70 * tt) * env_exp(d, .08) * .8)
def splash():                                   # a hand into cold water
    d = .3; tt = t_(d); return norm(bp(noise(d), 600, 5000) * env_exp(d, .06) + np.sin(2 * np.pi * 180 * tt * (1 + tt)) * env_exp(d, .03) * .3)
def thud():                                     # a short low hit under each cut and number
    d = .25; tt = t_(d); return norm(np.sin(2 * np.pi * 62 * tt * (1 - .3 * tt)) * env_exp(d, .07) + lp(noise(d), 300) * env_exp(d, .01) * .4)
def tick():                                     # a dry click as a line of type lands
    d = .03; tt = t_(d); return norm(np.sin(2 * np.pi * 3400 * tt) * env_exp(d, .004) + hp(noise(d), 5000) * env_exp(d, .0012) * .6)
def riser(d):                                   # band-passed noise rising into the silence
    n = noise(d); u = np.linspace(0, 1, len(n)); out = np.zeros_like(n); hop = 480
    for i in range(0, len(n), hop):
        fc = 400 + 6000 * (i / len(n)) ** 2; s = bp(n[max(0, i - 2400):i + hop], fc * .7, min(fc * 1.4, 20000))[-hop:]; out[i:i + len(s)] = s
    return norm(out) * u ** 2
def boom():                                     # sub drop under the twist
    d = 1.4; tt = t_(d); f = 70 * np.exp(-tt / .5) + 32; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(d, .5)
ws = [e['t'] for e in C['ev'] if e['type'] == 'slam' and e['k'] < 2]
for j, t in enumerate(ws):
    t1 = ws[j + 1] if j + 1 < len(ws) else cut['finger']
    add(fol, wind(t1 - t + .2) * (.5 + .25 * j), t - .1, 1, 0)
for e in C['ev']:
    if e['type'] == 'warn': add(fol, crack(), e['t'], .7, .2)
    if e['type'] == 'dip': add(fol, splash(), e['t'] + .12, .35, -.2)
    if e['type'] == 'cut' and e['t'] > 0:                       # every cut: a whoosh into a short low hit
        add(fol, whoosh(.25), e['t'] - .18, .35, 0); add(fol, thud(), e['t'], .5, 0)
    if e['type'] == 'text': add(fol, tick(), e['t'] + .06, .22, float(rng.uniform(-.3, .3)))
    if e['type'] == 'slam': add(fol, thud(), e['t'], .7, 0)
add(fol, boom(), SIL1, .9, 0)
add(fol, riser(1.2), SIL0 - 1.2, .45, 0)

rms = lambda x: float(np.sqrt((x ** 2).mean()) + 1e-9)
# the narration (voices/narration.wav, built by tools/voice.py) leads; music ~14 dB under it and ducked a further 4 dB while it speaks
v, sr = sf.read(os.path.join(ROOT, 'voices', 'narration.wav'), dtype='float32'); v = v.mean(1) if v.ndim > 1 else v
if sr != SR: v = soxr.resample(v, sr, SR)
voice = np.zeros((N, 2)); add(voice, v[:N], 0, 1, 0)
act = np.convolve((np.abs(voice[:, 0]) > 2e-3).astype(float), np.ones(int(.2 * SR)) / int(.2 * SR), 'same')
duck = 1 - .37 * np.clip(act * 3, 0, 1)
vr = rms(voice[np.abs(voice[:, 0]) > 2e-3])
mix = voice + music / rms(music) * vr * 10 ** (-14 / 20) * duck[:, None] + fol / rms(fol) * vr * 10 ** (-12 / 20)
a, b = int(SIL0 * SR), int(SIL1 * SR); f = int(.01 * SR)
mix[a - f:a] *= np.linspace(1, 0, f)[:, None]; mix[a:b] = 0
k = int(.8 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None] ** 1.5

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
mix[a:b] = 0
print('mastered to', lufs(mix), 'LUFS')
# 32 s of trailing silence: mux.sh's decode check runs ~2.9 s behind and allows 5 % of the length; build.sh trims back to the picture
mix = np.concatenate([mix, np.zeros((32 * SR, 2))])
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
names = sorted({(e['inst'] if isinstance(e, dict) else e[1]) for e in ev})
json.dump(names, open(os.path.join(D, 'instruments.json'), 'w'))
print('mix.wav', DUR, 's;', ', '.join(names))
