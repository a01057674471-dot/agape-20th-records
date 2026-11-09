"""align script.LINES to the narration by counting syllable nuclei (vowel peaks) between candidate pauses.
python3 align2.py total_seconds -> audio/align.json"""
import json, sys, math
import numpy as np, pykakasi
from script import LINES
kk = pykakasi.kakasi(); SMALL = set('ゃゅょぁぃぅぇぉゎ')
def mor(s): return sum(1 for ch in ''.join(x['hira'] for x in kk.convert(s)) if ('ぁ' <= ch <= 'ゖ' or ch == 'ー') and ch not in SMALL and ch not in 'んっ')
total = float(sys.argv[1])
nuc = np.load('audio/nuclei.npy')
sil = [tuple(map(float, l.split())) for l in open('audio/sil.txt') if len(l.split()) == 2]
start = sil[0][1] if sil[0][0] < 0.05 else 0.0
cuts = [((a + b) / 2, b - a) for a, b in sil if start + 0.2 < a and b < total - 0.1]
pos = [start] + [c[0] for c in cuts] + [total]; plen = [0] + [c[1] for c in cuts] + [0]
m = np.array([mor(l) for l in LINES], float); exp = m * len(nuc) / m.sum()
cnt = lambda a, b: int(((nuc >= a) & (nuc < b)).sum())
n, M = len(LINES), len(pos); INF = 1e18
D = np.full((n + 1, M), INF); B = np.zeros((n + 1, M), int); D[0, 0] = 0
for i in range(1, n + 1):
    for j in range(i, M):
        for k in range(i - 1, j):
            if D[i - 1, k] >= INF: continue
            c = cnt(pos[k], pos[j])
            v = D[i - 1, k] + (c - exp[i - 1]) ** 2 / (exp[i - 1] + 2) - (2.0 * min(plen[j], 0.8) if j < M - 1 else 0)
            if v < D[i, j]: D[i, j], B[i, j] = v, k
j = M - 1; idx = [j]
for i in range(n, 0, -1): j = B[i, j]; idx.append(j)
idx = idx[::-1]; segs = [(pos[idx[i]], pos[idx[i + 1]]) for i in range(n)]
for l, (a, e), x in zip(LINES, segs, exp):
    print(f'{a:6.2f}-{e:6.2f}  nuclei {cnt(a, e):3d} exp {x:5.1f}  {l}')
json.dump(dict(segs=segs, total=total), open('audio/align.json', 'w'))
