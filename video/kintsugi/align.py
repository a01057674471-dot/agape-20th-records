"""align script.LINES to the narration's pauses (mora-length DP); prints fit and writes audio/align.json"""
import json, sys, math
import numpy as np, pykakasi
from script import LINES
kk = pykakasi.kakasi(); SMALL = set('ゃゅょぁぃぅぇぉゎ')
def morae(t):
    t = t.replace('2,000', 'にせん')
    return sum(1 for ch in ''.join(x['hira'] for x in kk.convert(t)) if ('ぁ' <= ch <= 'ゖ' or ch == 'ー') and ch not in SMALL)
sil = [tuple(map(float, l.split())) for l in open('audio/sil.txt') if len(l.split()) == 2]
total = float(sys.argv[1])
start = sil[0][1] if sil[0][0] < 0.05 else 0.0
end = sil[-1][0] if sil[-1][1] > total - 0.05 else total
speech_end = end
cuts = [((a + b) / 2, b - a) for a, b in sil if start + 0.2 < a and b < end - 0.1]
pos = [start] + [c[0] for c in cuts] + [end]; plen = [0] + [c[1] for c in cuts] + [0]
mo = np.array([morae(l) for l in LINES], float); pu = np.array([sum(l.count(c) for c in '、。') for l in LINES], float)
p = 0.22; rate = (end - start - p * pu.sum()) / mo.sum(); exp = rate * mo + p * pu
n, m = len(LINES), len(pos); INF = 1e18
D = np.full((n + 1, m), INF); B = np.zeros((n + 1, m), int); D[0, 0] = 0
for i in range(1, n + 1):
    for j in range(i, m):
        for k in range(i - 1, j):
            if D[i - 1, k] >= INF: continue
            c = D[i - 1, k] + 6 * math.log((pos[j] - pos[k]) / exp[i - 1]) ** 2 - (1.5 * min(plen[j], 1.0) if j < m - 1 else 0)
            if c < D[i, j]: D[i, j], B[i, j] = c, k
j = m - 1; idx = [j]
for i in range(n, 0, -1): j = B[i, j]; idx.append(j)
idx = idx[::-1]; segs = [(pos[idx[i]], pos[idx[i + 1]]) for i in range(n)]
print(f'rate {rate:.3f}s/mora, speech {start:.2f}-{end:.2f}, cuts used {len(set(idx))-2}/{len(cuts)}')
for l, (a, e), x in zip(LINES, segs, exp):
    print(f'{a:6.2f}-{e:6.2f} ({e-a:4.2f} exp {x:4.2f}){" <<" if abs(math.log((e-a)/x))>0.3 else ""}  {l}')
json.dump(dict(segs=segs, total=total, speech_end=speech_end), open('audio/align.json', 'w'))
