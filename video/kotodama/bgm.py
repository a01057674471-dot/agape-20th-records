"""Quiet Japanese-style BGM, an original piece synthesised from scratch: a plucked koto (bright attack, the little
downward bend of the string, quick-fading overtones) playing a slow tune in the Yo pentatonic scale (D E G A B),
over a soft shō-like chord that breathes in and out. At the light (≈24 s) the koto moves up and the chord opens.
python3 bgm.py seconds -> audio/bgm.wav (48 kHz stereo)"""
import sys, wave
import numpy as np

SR = 48000
TOTAL = float(sys.argv[1]) if len(sys.argv) > 1 else 63.3
N = int(TOTAL * SR) + SR * 4
L = np.zeros(N); R = np.zeros(N)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def mid(n): return 12 * (int(n[-1]) + 1) + NOTE[n[0]] + (1 if '#' in n else 0)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
rng = np.random.default_rng(11)

def koto(m, t0, vel, pan=0.0, ring=3.2, bend=0.0):
    f = hz(m); n = int(ring * SR); t = np.arange(n) / SR
    fb = f * (1 + 0.012 * np.exp(-t * 30) + bend * smooth_step(t, 0.05, 0.25))   # pluck pitch drop; optional press-bend up
    ph = 2 * np.pi * np.cumsum(fb) / SR
    y = np.zeros(n)
    for k, (a, dk) in enumerate(((1.0, 2.2), (0.55, 4.0), (0.32, 6.5), (0.2, 9.0), (0.12, 13.0), (0.07, 18.0)), 1):
        y += a * np.sin(k * ph + rng.uniform(0, 6.28)) * np.exp(-t * dk * (0.5 + f / 900))
    y += 0.25 * rng.standard_normal(n) * np.exp(-t * 180)                          # the plectrum click
    y *= np.minimum(1, t / 0.002)
    i = int(t0 * SR); j = min(N, i + n)
    L[i:j] += y[:j - i] * vel * (1 - pan) * 0.5; R[i:j] += y[:j - i] * vel * (1 + pan) * 0.5

def smooth_step(t, a, b): u = np.clip((t - a) / (b - a), 0, 1); return u * u * (3 - 2 * u)

def sho(ms, t0, t1, vel):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR
    env = smooth_step(t, 0, 3.0) * (1 - smooth_step(t, t1 - t0 - 3.0, t1 - t0)) * (0.8 + 0.2 * np.sin(2 * np.pi * t / 7.0))
    for m in ms:
        f = hz(m)
        y = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) + 0.25 * np.sin(6 * np.pi * f * t) + 0.12 * np.sin(8 * np.pi * f * t))
        y *= env * (1 + 0.003 * np.sin(2 * np.pi * 4.5 * t))
        i = int(t0 * SR); j = min(N, i + n)
        L[i:j] += y[:j - i] * vel * 0.5; R[i:j] += y[:j - i] * vel * 0.5 * 0.95

BEAT = 0.9
# (start beat, note, vel)  -- an original melody in D Yo scale
A = [(0, 'A4', .5), (1, 'B4', .42), (1.5, 'A4', .38), (2, 'G4', .45), (4, 'E4', .42), (5, 'G4', .4), (6, 'A4', .48),
     (8, 'D5', .5), (9.5, 'B4', .38), (10, 'A4', .45), (12, 'G4', .42), (13, 'E4', .38), (14, 'D4', .5)]
B = [(0, 'G4', .45), (1, 'A4', .42), (2, 'B4', .5), (4, 'D5', .5), (5, 'E5', .45), (6, 'D5', .5),
     (8, 'B4', .45), (9, 'A4', .38), (9.5, 'B4', .38), (10, 'G4', .45), (12, 'A4', .5)]
END = [(0, 'D5', .45), (1, 'B4', .4), (2, 'A4', .45), (4, 'G4', .4), (5, 'E4', .38), (6, 'D4', .5)]
plan = [(2.0, A, 0), (18.0, B, 0), (26.6, A, 12), (40.8, B, 0), (55.2, END, 0)]   # seconds of each phrase start
for t0, ph, up in plan:
    for bt, n, v in ph:
        koto(mid(n) + up, t0 + bt * BEAT * (0.85 if up else 1.0), v * (0.8 if up else 1.0), 0.2, bend=0.02 if n in ('E4', 'B4') and bt % 4 == 2 else 0)
# low koto: open strings on each phrase and a slow sparse pulse
for t0 in np.arange(0.0, TOTAL - 4, BEAT * 4):
    koto(mid('D3'), t0, 0.32, -0.35, ring=4.0)
    koto(mid('A3'), t0 + BEAT * 2, 0.22, -0.3, ring=3.5)
# a glissando ornament into the light (24.2 s) and at the end
for k, n in enumerate(('D4', 'E4', 'G4', 'A4', 'B4', 'D5', 'E5', 'G5', 'A5')):
    koto(mid(n), 23.6 + k * 0.06, 0.28, 0.3, ring=2.5)
for k, n in enumerate(('A5', 'G5', 'E5', 'D5', 'B4', 'A4', 'G4', 'E4', 'D4')):
    koto(mid(n), TOTAL - 3.2 + k * 0.07, 0.22, 0.1, ring=3.0)
koto(mid('D3'), TOTAL - 2.5, 0.3, -0.3, ring=3.5)
# the shō: a quiet aitake-like cluster, then opening at the light
sho([mid('D4'), mid('A4'), mid('E5')], 0.0, 24.6, 0.028)
sho([mid('D4'), mid('A4'), mid('E5'), mid('B5'), mid('F#5')], 23.4, TOTAL + 1, 0.026)

ir_n = int(2.6 * SR); ti = np.arange(ir_n) / SR
def ir(seed):
    g = np.random.default_rng(seed).standard_normal(ir_n) * np.exp(-ti * 2.2); g[:int(0.015 * SR)] = 0
    return g / np.sqrt((g ** 2).sum())
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h))))
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
L2 = L * 0.75 + conv(L, ir(1)) * 0.5; R2 = R * 0.75 + conv(R, ir(2)) * 0.5
out = np.stack([L2, R2], 1)[:int(TOTAL * SR)]
fi = int(0.4 * SR); out[:fi] *= np.linspace(0, 1, fi)[:, None]
fo = int(1.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
out = np.tanh(out / np.abs(out).max() * 1.1) * 0.85
w = wave.open('audio/bgm.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
print('bgm', TOTAL)
