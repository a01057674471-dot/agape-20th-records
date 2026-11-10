"""Music-box BGM: 「きよしこの夜」 (Stille Nacht, Gruber 1818; public domain), synthesised from scratch -- a comb of
plucked steel tines (sine partials with the tine's inharmonic overtones, quick bright decay) plus a soft low pad,
with a little room reverb. 3/4 in C (sounding an octave up), 1-bar intro, the tune once, fitted to the video.
python3 bgm.py seconds -> audio/bgm.wav (48 kHz stereo)"""
import sys, wave
import numpy as np

SR = 48000
TOTAL = float(sys.argv[1]) if len(sys.argv) > 1 else 54.0
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def mid(n): return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + (1 if '#' in n else 0)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
TUNE = [('G4', 1.5), ('A4', .5), ('G4', 1), ('E4', 3), ('G4', 1.5), ('A4', .5), ('G4', 1), ('E4', 3),
        ('D5', 2), ('D5', 1), ('B4', 3), ('C5', 2), ('C5', 1), ('G4', 3),
        ('A4', 2), ('A4', 1), ('C5', 1.5), ('B4', .5), ('A4', 1), ('G4', 1.5), ('A4', .5), ('G4', 1), ('E4', 3),
        ('A4', 2), ('A4', 1), ('C5', 1.5), ('B4', .5), ('A4', 1), ('G4', 1.5), ('A4', .5), ('G4', 1), ('E4', 3),
        ('D5', 2), ('D5', 1), ('F5', 1.5), ('D5', .5), ('B4', 1), ('C5', 3), ('E5', 3),
        ('C5', 1), ('G4', 1), ('E4', 1), ('G4', 1.5), ('F4', .5), ('D4', 1), ('C4', 6)]
BARCH = ['C', 'C', 'C', 'C', 'G', 'G', 'C', 'C', 'F', 'F', 'C', 'C', 'F', 'F', 'C', 'C', 'G', 'G7', 'C', 'C', 'C', 'G7', 'C', 'C']
BASS = {'C': ['C3', 'G3', 'E4'], 'G': ['G2', 'D3', 'B3'], 'G7': ['G2', 'F3', 'B3'], 'F': ['F2', 'C3', 'A3']}
BEATS = 3 + sum(d for _, d in TUNE)          # intro bar + tune (72) -> last note rings out
BEAT = (TOTAL - 1.0) / BEATS
N = int(TOTAL * SR) + SR * 3
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(3)

def tine(m, t0, vel, pan=0.0, ring=2.6):
    f = hz(m); n = int(ring * SR); t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * f * t) * np.exp(-t * (1.6 + f / 900))
         + 0.35 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 5)
         + 0.22 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 14)        # the tine's bright inharmonic ping
         + 0.10 * np.sin(2 * np.pi * f * 8.9 * t) * np.exp(-t * 26))
    y *= np.minimum(1, t / 0.002) * (1 + 0.04 * np.sin(2 * np.pi * 5.2 * t))
    i = int(t0 * SR); j = min(N, i + n)
    L[i:j] += y[:j - i] * vel * (1 - pan) * 0.5; R[i:j] += y[:j - i] * vel * (1 + pan) * 0.5

def pad(ms, t0, dur, vel):
    n = int((dur + 1.5) * SR); t = np.arange(n) / SR
    env = np.minimum(1, t / 1.0) * np.where(t < dur, 1, np.clip(1 - (t - dur) / 1.4, 0, 1))
    for m in ms:
        for det, side in ((-0.05, 0), (0.05, 1)):
            y = np.sin(2 * np.pi * hz(m) * 2 ** (det / 12) * t) * env
            i = int(t0 * SR); j = min(N, i + n)
            (L if side == 0 else R)[i:j] += y[:j - i] * vel * 0.5

for (n, bt) in (('E5', 0), ('G5', 1), ('C6', 2)):      # intro: three bell notes
    tine(mid(n) + 12, bt * BEAT, 0.32, 0.3)
t = 3 * BEAT
for n, d in TUNE:
    tine(mid(n) + 12, t, 0.55, 0.15, ring=max(2.0, d * BEAT + 1.2))
    t += d * BEAT
for b, c in enumerate(BARCH):
    t0 = (3 + b * 3) * BEAT
    r, f5, t3 = [mid(x) + 12 for x in BASS[c]]
    tine(r, t0, 0.3, -0.25)
    tine(f5, t0 + BEAT, 0.18, -0.2); tine(t3, t0 + 2 * BEAT, 0.16, -0.1)
    pad([mid(x) for x in BASS[c]], t0, 3 * BEAT, 0.03)
tl = t - 6 * BEAT                                       # the last note: a held chord and two bells under the end card
pad([mid('C3'), mid('G3'), mid('E4')], tl, 6 * BEAT, 0.035)
tine(mid('E5') + 12, tl + 3 * BEAT, 0.2, 0.3, 3.0); tine(mid('G5') + 12, tl + 3 * BEAT + 0.3, 0.18, -0.2, 3.0)
tine(mid('C6') + 12, tl + 4.5 * BEAT, 0.16, 0.2, 3.0)

ir_n = int(2.0 * SR); ti = np.arange(ir_n) / SR
def ir(seed):
    g = np.random.default_rng(seed).standard_normal(ir_n) * np.exp(-ti * 3.0); g[:int(0.01 * SR)] = 0
    return g / np.sqrt((g ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
L2 = L * 0.8 + conv(L, ir(1)) * 0.45; R2 = R * 0.8 + conv(R, ir(2)) * 0.45
out = np.stack([L2, R2], 1)[:int(TOTAL * SR)]
fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
out = np.tanh(out / np.abs(out).max() * 1.1) * 0.85
w = wave.open('audio/bgm.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
print('bgm', TOTAL, 'beat', round(BEAT, 3), 'beats', BEATS)
