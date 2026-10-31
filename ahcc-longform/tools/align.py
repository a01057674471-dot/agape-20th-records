# Find each script line in the recording (voices/source.mp3): split the recording at its pauses (silencedetect,
# -35 dB, ≥ 0.3 s), then give every line a run of consecutive segments so that the run's length best matches the
# line's syllable count at the recording's own pace (dynamic programming). → voices/times.json {line id: [start, end]}
# run: python3 tools/align.py
# For the 2026-10-31 recording the result was checked against syllable peaks per segment; where two lines were joined
# by a pause shorter than 0.3 s (l03|l04, l27|l27b|l28, l30|l31) the boundary was set by hand at the short pause
# found with silencedetect d=0.1 inside that block. voices/times.json holds the corrected result.
import os, json, re, subprocess
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, 'voices', 'source.mp3')
L = json.load(open(os.path.join(HERE, 'lines.json'), encoding='utf-8'))
out = subprocess.run(['ffmpeg', '-nostats', '-i', SRC, '-af', 'silencedetect=noise=-35dB:d=0.3', '-f', 'null', '-'], capture_output=True, text=True).stderr
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SRC], capture_output=True, text=True).stdout)
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
cuts = sorted(zip(st, en))
segs, a = [], 0.0
for s, e in cuts:
    if s > a + .05: segs.append((a, s))
    a = e
if dur > a + .05: segs.append((a, dur))
# trim leading silence of the first segment
syl = lambda t: len(re.findall(r'[가-힣]', t)) + len(re.findall(r'[0-9]', t)) + .5 * len(re.findall(r'[A-Za-z]', t))
S = [syl(l['text']) for l in L]
speech = sum(e - s for s, e in segs); rate = sum(S) / speech
n, m = len(L), len(segs)
INF = 1e18
best = [[INF] * (m + 1) for _ in range(n + 1)]; back = [[0] * (m + 1) for _ in range(n + 1)]
best[0][0] = 0
for i in range(1, n + 1):
    for j in range(i, m - (n - i) + 1):
        for k in range(i - 1, j):
            if best[i - 1][k] >= INF: continue
            d = sum(e - s for s, e in segs[k:j]); exp = S[i - 1] / rate
            c = best[i - 1][k] + ((d - exp) / max(1, exp)) ** 2
            if c < best[i][j]: best[i][j] = c; back[i][j] = k
res, j = {}, m
for i in range(n, 0, -1):
    k = back[i][j]; res[L[i - 1]['id']] = [round(segs[k][0], 3), round(segs[j - 1][1], 3)]; j = k
json.dump(res, open(os.path.join(HERE, 'voices', 'times.json'), 'w'), indent=1)
for l, s in zip(L, S):
    a, b = res[l['id']]; print(f"{l['id']:5} {a:7.2f}–{b:7.2f} {b - a:5.2f}s exp {s / rate:5.2f}s  {l['text'][:28]}")
print('segments', m, 'lines', n, 'rate', round(rate, 2), 'syl/s')
