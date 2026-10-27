# 올리고파 (value cut) — the user's narration + print foley, no music: metal type, paper, utility knife, steel rule, wooden blocks → out/mix.wav
# Every sound is an event the picture already placed on the beat (audio/cues.json). Dry and close, no reverb.
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
vp = os.path.join(ROOT, 'voices', 'narration.wav')
if C.get('voice') and os.path.exists(vp):
    v, sr = sf.read(vp, dtype='float32'); v = v.mean(1) if v.ndim > 1 else v
    if sr != SR: v = soxr.resample(v, sr, SR)
    voice = np.zeros((N, 2))
    for a0, a1, at in C['voice']:                                  # each piece cut inside a pause, 10 ms edges
        pc = v[int(a0 * SR):int(a1 * SR)].copy(); k = int(.01 * SR)
        pc[:k] *= np.linspace(0, 1, k); pc[-k:] *= np.linspace(1, 0, k); add(voice, pc, at, 1, 0)
    act = np.convolve((np.abs(voice[:, 0]) > 1e-3).astype(float), np.ones(int(.15 * SR)) / int(.15 * SR), 'same')
    duck = 1 - .45 * np.clip(act * 4, 0, 1)
    vr = rms(voice[np.abs(voice[:, 0]) > 1e-3])
    mix = voice + fol / rms(fol[np.abs(fol[:, 0]) > 1e-3]) * vr * 10 ** (-12 / 20) * duck[:, None]
else:
    mix = fol.copy()
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
# 24 s of trailing silence: mux.sh's decode check runs ~2.9 s behind and allows 5 % of the length; build.sh trims back to the picture
mix = np.concatenate([mix, np.zeros((24 * SR, 2))])
sf.write(os.path.join(OUT, 'mix.wav'), mix.astype(np.float32), SR)
print('mix.wav', DUR, 's; events', len(C['ev']), '; peak', round(float(np.abs(mix).max()), 3))
