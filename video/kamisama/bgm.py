"""Instrumental BGM for the reel: the hymn "Joyful, Joyful, We Adore Thee" (HYMN TO JOY, Beethoven; public domain) --
"field and forest, vale and mountain ... flashing sea" praising their Maker -- arranged for soft piano + warm pad and
synthesised here from scratch (no samples, no recordings). 4/4, D major, 1-bar intro, the tune once, a held last chord,
fitted to the video length.  python3 bgm.py seconds -> audio/bgm.wav (48 kHz stereo)"""
import sys, wave
import numpy as np

SR = 48000
TOTAL = float(sys.argv[1]) if len(sys.argv) > 1 else 55.2
BARS = 18
BEAT = TOTAL / (BARS * 4 + 0.0)             # seconds per beat (~78 bpm)
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

# the tune in D (note, beats)
TUNE = [('F#4', 1), ('F#4', 1), ('G4', 1), ('A4', 1), ('A4', 1), ('G4', 1), ('F#4', 1), ('E4', 1),
        ('D4', 1), ('D4', 1), ('E4', 1), ('F#4', 1), ('F#4', 1.5), ('E4', .5), ('E4', 2),
        ('F#4', 1), ('F#4', 1), ('G4', 1), ('A4', 1), ('A4', 1), ('G4', 1), ('F#4', 1), ('E4', 1),
        ('D4', 1), ('D4', 1), ('E4', 1), ('F#4', 1), ('E4', 1.5), ('D4', .5), ('D4', 2),
        ('E4', 1), ('E4', 1), ('F#4', 1), ('D4', 1), ('E4', 1), ('F#4', .5), ('G4', .5), ('F#4', 1), ('D4', 1),
        ('E4', 1), ('F#4', .5), ('G4', .5), ('F#4', 1), ('E4', 1), ('D4', 1), ('E4', 1), ('A3', 2),
        ('F#4', 1), ('F#4', 1), ('G4', 1), ('A4', 1), ('A4', 1), ('G4', 1), ('F#4', 1), ('E4', 1),
        ('D4', 1), ('D4', 1), ('E4', 1), ('F#4', 1), ('E4', 1.5), ('D4', .5), ('D4', 4)]
CH = {'D': ['D2', 'A2', 'F#3'], 'A': ['A1', 'E2', 'C#3'], 'A7': ['A1', 'E2', 'G3'], 'G': ['G1', 'D2', 'B2'],
      'Bm': ['B1', 'F#2', 'D3'], 'E': ['E2', 'B2', 'G#3']}
PADV = {'D': ['A3', 'D4', 'F#4'], 'A': ['A3', 'C#4', 'E4'], 'A7': ['G3', 'C#4', 'E4'], 'G': ['G3', 'B3', 'D4'],
        'Bm': ['F#3', 'B3', 'D4'], 'E': ['G#3', 'B3', 'E4']}
# chords per half bar: intro 1 bar, tune 16 bars, ending 1 bar
HALF = (['D', 'G'] +
        ['D', 'D', 'A', 'A', 'D', 'G', 'A', 'A'] + ['D', 'D', 'A', 'A', 'D', 'G', 'A7', 'D'] +
        ['A', 'D', 'A', 'D', 'A', 'Bm', 'E', 'A7'] + ['D', 'D', 'A', 'A', 'D', 'G', 'A7', 'D'] + ['D', 'D'])
H2 = 2 * BEAT
for h, c in enumerate(HALF):
    r, f5, t10 = [mid(x) + 12 for x in CH[c]]
    t0 = h * H2
    last = h >= len(HALF) - 2
    vv = 0.4 if h < 2 or last else 0.32
    if last:
        if h == len(HALF) - 2:
            for k, m in enumerate((r, f5, t10, r + 12)):
                piano(m, t0 + k * 0.16, 5 * BEAT, 0.34, -0.1)
            pad([mid(x) for x in PADV[c]], t0, 5 * BEAT, 0.05)
        continue
    piano(r, t0, H2, vv * 1.1, -0.3)                         # bass, then a soft broken chord on the eighths
    for k, m in enumerate((f5, t10, f5 + 12)):
        piano(m, t0 + (0.5 + k * 0.5) * BEAT, 1.2 * BEAT, vv * 0.62, -0.15)
    pad([mid(x) for x in PADV[c]], t0, H2, 0.045)
for (n, bt) in (('A5', 0), ('F#5', 1), ('D5', 2), ('B4', 3)):    # intro: a few falling notes
    piano(mid(n), bt * BEAT, 1.5 * BEAT, 0.26, 0.25)
t = 4 * BEAT                                                     # melody an octave up: music-box warmth
for n, d in TUNE:
    piano(mid(n) + 12, t, d * BEAT, 0.48, 0.2)
    t += d * BEAT
piano(mid('A5'), 17 * 4 * BEAT + 0.3, 4 * BEAT, 0.22, 0.3)

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
