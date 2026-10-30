# 라파힐 AHCC — a calm 120 bpm bed + print foley → out/mix.wav. Every accent is an event the picture placed on the beat (audio/cues.json).
# The bed is light on purpose (vibraphone and marimba pulse, soft kick, finger bass, C major) so narration can sit on it later;
# drop voices/narration.wav in and the voice leads, the bed and foley duck under it.
# run: LIB=<library> $LIB/.venv/bin/python audio/sound.py
import os, sys, json
LIB = os.environ['LIB']; sys.path.insert(0, LIB)
import numpy as np, soundfile as sf, soxr
from core.audio.sfx import SR, t_, env_exp, bp, lp, hp, noise, norm, add, brown, limit, whoosh

D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(D, '..'); OUT = os.path.join(ROOT, 'out'); os.makedirs(OUT, exist_ok=True)
C = json.load(open(os.path.join(D, 'cues.json')))
DUR = C['dur']; N = int(DUR * SR)
rng = np.random.default_rng(26)

def type_clack(big=False):      # metal type into the tray: transient + 3.3 / 5.1 kHz resonances + the wooden tray
    d = .12 if big else .07; tt = t_(d); p = .92 + rng.random() * .16
    x = hp(noise(d), 2500) * env_exp(d, .0012) * .9
    x += sum(a * np.sin(2 * np.pi * f * p * tt + rng.random() * 6) * env_exp(d, tau) for f, a, tau in [(3300, .45, .010), (5100, .25, .006), (1250, .35, .016)])
    x += np.sin(2 * np.pi * (140 if big else 420) * p * tt) * env_exp(d, .03 if big else .012) * (.9 if big else .35)
    return norm(x)
def rule_line():                # steel rule "tss"
    d = .05; return norm(bp(noise(d), 3000, 9000) * np.sin(np.pi * t_(d) / d) ** 2)
def knife(d=.16):               # blade across (rising band-pass) + a metal snick at the end
    n = noise(d); tt = t_(d); out = np.zeros_like(n); hop = 240
    for i in range(0, len(n), hop):
        f = 1500 + 4500 * (i / len(n)) ** 1.5
        s = bp(n[max(0, i - 1200):i + hop], f * .8, min(f * 1.25, 20000))[-hop:]; out[i:i + len(s)] = s
    out *= np.minimum(1, tt / (d * .7)) ** 1.5 * np.exp(-np.maximum(0, tt - d * .8) / .02)
    sn = t_(.08); snick = np.sin(2 * np.pi * 4200 * sn) * env_exp(.08, .012) + hp(noise(.08), 4000) * env_exp(.08, .003)
    x = out * .7; x[-len(sn):] += snick[:len(x)] * .8 if len(sn) <= len(x) else 0
    return norm(x)
def paper():                    # a sheet laid down: pushed air + surface slap
    d = .25; tt = t_(d)
    return norm(lp(noise(d), 900) * env_exp(d, .03) + np.sin(2 * np.pi * 110 * tt) * env_exp(d, .04) * .6 + hp(noise(d), 3000) * env_exp(d, .006) * .4)
def thunk():                    # the giant numeral, one module per step
    d = .12; tt = t_(d)
    return norm(np.sin(2 * np.pi * 95 * tt) * env_exp(d, .025) + bp(noise(d), 300, 1500) * env_exp(d, .006) * .6)
def slide(d=.2):
    tt = t_(d); return norm(bp(noise(d), 700, 5000) * np.sin(np.pi * tt / d) ** 1.5)
def block(hero=False):          # a block snapping into its slot; the lime one lands heavier
    d = .09 if hero else .05; tt = t_(d)
    x = hp(noise(d), 1500) * env_exp(d, .002) + np.sin(2 * np.pi * 1900 * tt) * env_exp(d, .007) * .6 + np.sin(2 * np.pi * 620 * tt) * env_exp(d, .01) * .4
    if hero: x += np.sin(2 * np.pi * 180 * tt) * env_exp(d, .03) * .9
    return norm(x)
def thump():                    # felt landing
    d = .45; tt = t_(d)
    return norm(np.sin(2 * np.pi * 58 * tt * (1 - .25 * tt)) * env_exp(d, .09) + lp(noise(d), 250) * env_exp(d, .02) * .4)
def tick():
    d = .03; tt = t_(d); return norm(np.sin(2 * np.pi * 3600 * tt) * env_exp(d, .004) + hp(noise(d), 5000) * env_exp(d, .001) * .5)
def stamp():                    # rubber stamp: a soft press + a paper pop
    d = .2; tt = t_(d)
    return norm(lp(noise(d), 600) * env_exp(d, .015) + np.sin(2 * np.pi * 75 * tt) * env_exp(d, .05) * .8 + hp(noise(d), 2500) * env_exp(d, .003) * .3)

FOLEY = {
    'clack': (lambda e: type_clack(), .16), 'clackBig': (lambda e: type_clack(True), .26), 'rule': (lambda e: rule_line(), .09),
    'knife': (lambda e: knife(), .24), 'paper': (lambda e: paper(), .32), 'thunk': (lambda e: thunk(), .30), 'slide': (lambda e: slide(), .12),
    'snap': (lambda e: block(), .16), 'snapHero': (lambda e: block(True), .34), 'thump': (lambda e: thump(), .55), 'tick': (lambda e: tick(), .08),
    'swish': (lambda e: whoosh(e.get('d', .5)), .14), 'stamp': (lambda e: stamp(), .4),
}
fol = np.zeros((N, 2))
for e in C['ev']:
    if e['type'] not in FOLEY: continue
    fn, gain = FOLEY[e['type']]; x = np.asarray(fn(e), np.float64)
    at = e['t'] - (len(x) / SR - .02 if e['type'] == 'knife' else 0)        # the snick lands on the beat
    add(fol, x, max(0, at), gain * e.get('g', 1), pan=float(rng.uniform(-.25, .25)))
room = lp(brown(DUR), 200)[:N] * .006; fol[:, 0] += room; fol[:, 1] += room   # a quiet studio, so the cuts aren't digital black
s0 = [e for e in C['ev'] if e['type'] == 'silence']                              # an optional beat of real silence
a, b = (int(s0[0]['t'] * SR), int((s0[0]['t'] + s0[0]['d']) * SR)) if s0 else (0, 0)
# the narration (voices/narration.wav, the user's recording) in the pieces film.js lists; foley sits ~12 dB under it and dips a little more while it speaks
rms = lambda x: float(np.sqrt((x ** 2).mean()) + 1e-9)
# ---------- the bed ----------
from core.audio import sampler as S
S.seed(9); BEAT = .5; E8 = BEAT / 2
PROG = [['C4', 'E4', 'G4', 'B4'], ['A3', 'C4', 'E4', 'G4'], ['F3', 'A3', 'C4', 'E4'], ['G3', 'B3', 'D4', 'G4']]
BASS = ['C2', 'A1', 'F2', 'G2']
cuts = sorted(e['t'] for e in C['ev'] if e['type'] in ('start', 'cut'))
ev = []; k = 0; t = .25; END = DUR - 1.6
while t < END:
    bar = int(t // 2) % 4; step = k % 8; sec = max(i for i, c in enumerate(cuts) if t >= c - 1e-6)
    ev.append((t, 'marimba', PROG[bar][[0, 2, 1, 3, 2, 1, 3, 2][step]], E8 * 1.6, .3 if step % 4 == 0 else .22, -.2 + .1 * (step % 3)))
    if step == 0: ev += [dict(t=t, inst='vibraphone', pitch=p, dur=2.0, vel=.16, pan=.25) for p in PROG[bar][1:3]]
    if step % 2 == 0 and sec >= 1: ev.append((t, 'electric_bass', BASS[bar], .4, .5 if step % 4 == 0 else .4, 0))
    if step % 4 == 0 and sec >= 2: ev.append(dict(t=t, inst='drum_kit', pitch='kick_drum_left', vel=.55, pan=0))
    if step % 2 == 1 and sec >= 3: ev.append(dict(t=t, inst='drum_kit', pitch='hi_hat_closed', vel=.18, pan=.3))
    t += E8; k += 1
for c in cuts[1:]: ev.append((c, 'glockenspiel', 'G6', .8, .22, .3))
ev += [dict(t=END, inst=i, pitch=p, dur=DUR - END, vel=v, pan=pn) for i, p, v, pn in [('vibraphone', 'C4', .3, .2), ('vibraphone', 'E4', .28, .2), ('vibraphone', 'G4', .28, .2), ('marimba', 'C3', .4, -.2), ('electric_bass', 'C2', .55, 0), ('glockenspiel', 'C7', .3, .3)]]
music = S.room(S.render(ev, dur=DUR, master=False), size=.25, mix=.1)
music = music[:N] if len(music) >= N else np.pad(music, ((0, N - len(music)), (0, 0)))
bed = music + fol / rms(fol[np.abs(fol[:, 0]) > 1e-3]) * rms(music) * 10 ** (-4 / 20)
# ---------- narration (later): voices/narration.wav leads, the bed sits ~14 dB under it ----------
vp = os.path.join(ROOT, 'voices', 'narration.wav')
if os.path.exists(vp):
    v, sr = sf.read(vp, dtype='float32'); v = v.mean(1) if v.ndim > 1 else v
    if sr != SR: v = soxr.resample(v, sr, SR)
    voice = np.zeros((N, 2)); add(voice, v[:N], 0, 1, 0)
    act = np.convolve((np.abs(voice[:, 0]) > 2e-3).astype(float), np.ones(int(.2 * SR)) / int(.2 * SR), 'same')
    vr = rms(voice[np.abs(voice[:, 0]) > 2e-3])
    mix = voice + bed / rms(bed) * vr * 10 ** (-14 / 20) * (1 - .37 * np.clip(act * 3, 0, 1))[:, None]
else:
    mix = bed
mix[a:b] = 0

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
# 32 s of trailing silence: mux.sh's decode check runs ~2.9 s behind and allows 5 % of the length; build.sh trims back to the picture
mix = np.concatenate([mix, np.zeros((32 * SR, 2))])
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
print('mix.wav', DUR, 's; events', len(C['ev']), '; peak', round(float(np.abs(mix).max()), 3))
