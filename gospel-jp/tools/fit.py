#!/usr/bin/env python3
"""Line timings from the narration without speech recognition.
The recording is split into speech runs at every pause; a dynamic programme groups consecutive runs into the
script's lines so that each line's length matches its character count (at the reader's own pace) and lines
break at the longest pauses.   python tools/fit.py audio/narration.mp3 -> cues.json"""
import json, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cues import script, HERE, TAIL

KEEP = lambda s: re.sub(r'[\s、。「」・，．,.!?！？（）()〜ー…]', '', s)
sr = 16000
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
hop = sr // 100; n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
db = np.convolve(db, np.ones(3) / 3, 'same')
thr = max(np.percentile(db, 97) - 32, -55); on = db > thr
runs, i = [], 0
while i < n:
    if on[i]:
        j = i
        while j < n and on[j]: j += 1
        if runs and i - runs[-1][1] < 12: runs[-1][1] = j      # join across gaps < 0.12 s
        else: runs.append([i, j])
        i = j
    else: i += 1
runs = [r for r in runs if r[1] - r[0] > 6]
R = len(runs); st = np.array([r[0] for r in runs]) / 100; en = np.array([r[1] for r in runs]) / 100
L = script()
w = np.array([len(KEEP(t.split('\n（')[0])) + (3 if '\n' in t else 0) for _, t in L], float)
M = len(L); rate = (en - st).sum() / w.sum()          # seconds per character, at the reader's pace
gap = np.r_[st[1:] - en[:-1], 9.0]                     # pause after run k
INF = 1e18; D = np.full((M + 1, R + 1), INF); P = np.zeros((M + 1, R + 1), int); D[0, 0] = 0
for m in range(1, M + 1):
    exp = w[m - 1] * rate
    for k in range(m, R - (M - m) + 1):                 # line m ends with run k-1
        best, arg = INF, 0
        for j in range(m - 1, k):                       # line m starts with run j
            if D[m - 1, j] >= INF: continue
            d = en[k - 1] - st[j]
            c = D[m - 1, j] + ((d - exp) / (0.35 * exp + 0.6)) ** 2 - 3.0 * min(gap[k - 1], 1.2)
            if c < best: best, arg = c, j
        D[m, k], P[m, k] = best, arg
k = R; spans = []
for m in range(M, 0, -1):
    j = P[m, k]; spans.append((j, k)); k = j
spans.reverse()
lines = [{'cue': c, 't0': round(st[a], 2), 't1': round(en[b - 1], 2), 'text': t, 'i': i} for i, ((c, t), (a, b)) in enumerate(zip(L, spans))]
dur = round(lines[-1]['t1'] + TAIL, 2)
json.dump({'dur': dur, 'lines': lines}, open(os.path.join(HERE, 'cues.json'), 'w'), ensure_ascii=False, indent=1)
print(f'{R} runs, rate {rate:.3f} s/char')
for l, (a, b), wi in zip(lines, spans, w):
    print(f"{l['i']:2d} {l['t0']:6.2f}-{l['t1']:6.2f} {l['t1']-l['t0']:5.2f}s exp {wi*rate:5.2f} pause-after {gap[b-1]:.2f}  {l['text'][:16]}")
