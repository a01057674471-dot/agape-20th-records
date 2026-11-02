# song.mp3 → src/env.json: per-frame (24 fps) energy envelopes the picture follows
#   v: vocal band (250–3500 Hz, mid of stereo), normalised 0..1 — drives her jaw when she sings
#   b: low band (< 150 Hz) — the bed of the arrangement, used to check sections
import json, subprocess, numpy as np, os
from scipy.signal import butter, sosfiltfilt
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, '..')
SR = 16000
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(R, 'audio/song.mp3'), '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2)
mid = x.mean(1); side = (x[:, 0] - x[:, 1]) / 2
v = sosfiltfilt(butter(4, [250, 3500], 'band', fs=SR, output='sos'), mid)
b = sosfiltfilt(butter(4, 150, 'low', fs=SR, output='sos'), mid)
hop = SR // 24; n = len(mid) // hop
rms = lambda s: np.sqrt(np.array([np.mean(s[i * hop:(i + 1) * hop] ** 2) for i in range(n)]) + 1e-12)
V, B = rms(v), rms(b)
def norm(a): a = 20 * np.log10(a); lo, hi = np.percentile(a, 20), np.percentile(a, 98); return np.clip((a - lo) / (hi - lo), 0, 1)
V, B = norm(V), norm(B)
json.dump({'fps': 24, 'v': [round(float(a), 3) for a in V], 'b': [round(float(a), 3) for a in B]}, open(os.path.join(R, 'src/env.json'), 'w'))
for t in range(0, n // 24, 2): print(f'{t//60}:{t%60:02d} v{V[t*24:(t+2)*24].mean():.2f} b{B[t*24:(t+2)*24].mean():.2f}', end='  |  ' if t % 8 != 6 else '\n')
