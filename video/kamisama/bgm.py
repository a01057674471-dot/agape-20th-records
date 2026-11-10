"""Instrumental BGM for the reel: "Amazing Grace" (New Britain, public domain) arranged for soft piano + warm pad,
synthesised here from scratch (no samples, no recordings). 3/4, G major, 2-bar intro, the tune once, 2-bar ending,
fitted to the video length.  python3 bgm.py seconds -> audio/bgm.wav (48 kHz stereo)"""
import sys, wave
import numpy as np

SR = 48000
TOTAL = float(sys.argv[1]) if len(sys.argv) > 1 else 55.2
BARS = 20
BEAT = TOTAL / (BARS * 3 + 0.0)             # seconds per beat (~65 bpm)
N = int(TOTAL * SR) + SR * 2
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(8)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 6 - 1, 'G': 7, 'A': 9, 'B': 11}
def mid(n):                                  # 'G4', 'F#4'
    s = n[:-1]; o = int(n[-1])
    return 12 * (o + 1) + NOTE[s[0]] + (1 if '#' in s else 0)

def piano(m, t0, dur, vel, pan=0.0):
    f = hz(m); n = int((dur + 2.5) * SR); t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(1, 9):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)
        if fk > 9000: break
        dec = 0.9 + 2.2 * k / (1 + f / 300)
        y += np.sin(2 * np.pi * fk * t + rng.uniform(0, 6.28)) * (1 / k ** 1.6) * np.exp(-t * dec * (0.6 + f / 1200))
    y *= np.minimum(1, t / 0.006)
    rel = np.clip(1 - (t - dur) / 0.6, 0, 1) ** 2               # damper after the note's length
    y *= np.where(t < dur, 1, rel)
    i = int(t0 * SR); j = min(N, i + n)
    L[i:j] += y[:j - i] * vel * (1 - pan) * 0.5; R[i:j] += y[:j - i] * vel * (1 + pan) * 0.5

def pad(ms, t0, dur, vel):
    n = int((dur + 1.5) * SR); t = np.arange(n) / SR
    env = np.minimum(1, t / 0.9) * np.where(t < dur, 1, np.clip(1 - (t - dur) / 1.4, 0, 1))
    for m in ms:
        for det, side in ((-0.06, -1), (0.06, 1)):
            f = hz(m) * 2 ** (det / 12)
            y = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t)) * env
            i = int(t0 * SR); j = min(N, i + n)
            (L if side < 0 else R)[i:j] += y[:j - i] * vel * 0.5

# the tune, (note, beats); bar lines implied (pickup D4 on beat 3 of intro bar 2)
TUNE = [('D4', 1),
        ('G4', 2), ('B4', .5), ('G4', .5), ('B4', 2), ('A4', 1), ('G4', 2), ('E4', 1), ('D4', 2), ('D4', 1),
        ('G4', 2), ('B4', .5), ('G4', .5), ('B4', 2), ('A4', 1), ('D5', 5), ('B4', 1),
        ('D5', 2), ('B4', .5), ('D5', .5), ('B4', 2), ('A4', 1), ('G4', 2), ('E4', 1), ('D4', 2), ('D4', 1),
        ('G4', 2), ('B4', .5), ('G4', .5), ('B4', 2), ('A4', 1), ('G4', 6)]
CH = {'G': ['G2', 'D3', 'B3'], 'C': ['C3', 'G3', 'E4'], 'D': ['D3', 'A3', 'F#4'], 'Em': ['E2', 'B2', 'G3'], 'D7': ['D3', 'A3', 'C4']}
PADV = {'G': ['G3', 'B3', 'D4'], 'C': ['G3', 'C4', 'E4'], 'D': ['F#3', 'A3', 'D4'], 'Em': ['G3', 'B3', 'E4'], 'D7': ['F#3', 'A3', 'C4']}
# chords per bar: intro 2, tune 16, ending 2
BARCH = ['G', 'C'] + ['G', 'G', 'C', 'G', 'G', 'G', 'D', 'D7', 'G', 'G', 'C', 'G', 'Em', 'D', 'G', 'G'] + ['C', 'G']

beat = 0.0
t_bar = lambda b: b * 3 * BEAT
# left hand: gentle broken chord (root on 1, fifth & tenth on the "and"s)
for b, c in enumerate(BARCH):
    r, f5, t10 = [mid(x) for x in CH[c]]
    last = b == len(BARCH) - 1
    vv = 0.42 if b < 2 or b >= 18 else 0.34
    piano(r, t_bar(b), 3 * BEAT, vv * 1.1, -0.3)
    if not last:
        for k, m in enumerate((f5, t10, f5 + 12 if c != 'Em' else t10 + 5, t10)):
            piano(m, t_bar(b) + (1 + k * 0.5) * BEAT, 1.4 * BEAT, vv * 0.7, -0.15)
    else:
        for k, m in enumerate((f5, t10, r + 24)):
            piano(m, t_bar(b) + k * 0.18, 4 * BEAT, vv * 0.8, -0.1)
    pad([mid(x) for x in PADV[c]], t_bar(b), 3 * BEAT + (2 * BEAT if last else 0), 0.05)
# intro: a few high notes over the first two bars
for (n, bt) in (('D5', 0), ('B4', 1), ('G4', 2), ('E5', 3), ('C5', 4)):
    piano(mid(n), bt * BEAT, 1.5 * BEAT, 0.28, 0.25)
# melody, softly, an octave up from the hymn book for a music-box warmth
t = t_bar(2) - BEAT
for n, d in TUNE:
    piano(mid(n) + 12, t, d * BEAT, 0.5, 0.2)
    t += d * BEAT
# ending: high G
piano(mid('G5'), t_bar(19), 4 * BEAT, 0.3, 0.25); piano(mid('D6'), t_bar(19) + 0.25, 4 * BEAT, 0.18, 0.3)

# a simple reverb: decaying noise impulse, convolved per channel (FFT)
ir_n = int(2.4 * SR); ti = np.arange(ir_n) / SR
def ir(seed):
    g = np.random.default_rng(seed).standard_normal(ir_n) * np.exp(-ti * 2.6)
    g[:int(0.012 * SR)] = 0; return g / np.sqrt((g ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
wetL, wetR = conv(L, ir(1)), conv(R, ir(2))
L2 = L * 0.75 + wetL * 0.5; R2 = R * 0.75 + wetR * 0.5
out = np.stack([L2, R2], 1)[:int(TOTAL * SR)]
fo = int(2.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
out = np.tanh(out / np.abs(out).max() * 1.1) * 0.85
w = wave.open('audio/bgm.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
print('bgm', TOTAL, 's, beat', round(BEAT, 3), 'peak', np.abs(out).max())
