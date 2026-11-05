"""Align the subtitle blocks in compose.BLOCKS to a recorded narration.
Expected length of each block = its morae (pykakasi reading) x the speaker's rate, plus a pause per comma/period.
A DP picks block boundaries among the detected pauses, matching expected lengths and preferring longer pauses.
python3 align.py <silences.txt> <audio_seconds>  ->  audio/align.json"""
import json, sys, math
import numpy as np
import pykakasi
import compose

kk = pykakasi.kakasi()
SMALL = set('ゃゅょぁぃぅぇぉゎ')

def morae(text):
    text = text.replace('2,000', 'にせん')
    h = ''.join(x['hira'] for x in kk.convert(text))
    return sum(1 for ch in h if ('ぁ' <= ch <= 'ゖ' or ch == 'ー') and ch not in SMALL)

def puncts(text):
    return sum(text.count(c) for c in '、。')

sil = [tuple(map(float, l.split())) for l in open(sys.argv[1]) if len(l.split()) == 2]
total = float(sys.argv[2])
blocks = [b[0] for b in compose.BLOCKS if b[0]]
mo = np.array([morae(''.join(b)) for b in blocks], float)
pu = np.array([puncts(''.join(b)) for b in blocks], float)
start = sil[0][1] if sil[0][0] < 0.05 else 0.0
end = total
cuts = [((a + b) / 2, b - a) for a, b in sil if start + 0.3 < a and b < end - 0.3]
pos = [start] + [c[0] for c in cuts] + [end]
plen = [0.0] + [c[1] for c in cuts] + [0.0]
m, n = len(pos), len(blocks)
# speaker model: dur = rate * morae + p * puncts ; fit rate with p = 0.25
p = 0.25
rate = (end - start - p * pu.sum()) / mo.sum()
exp = rate * mo + p * pu
INF = 1e18
D = np.full((n + 1, m), INF); B = np.zeros((n + 1, m), int); D[0, 0] = 0
for i in range(1, n + 1):
    for j in range(i, m):
        best, arg = INF, -1
        for k in range(max(i - 1, 0), j):
            if D[i - 1, k] >= INF: continue
            dur = pos[j] - pos[k]
            c = 6 * math.log(dur / exp[i - 1]) ** 2 - (1.5 * min(plen[j], 1.0) if j < m - 1 else 0)
            v = D[i - 1, k] + c
            if v < best: best, arg = v, k
        D[i, j], B[i, j] = best, arg
j = m - 1; idx = [j]
for i in range(n, 0, -1):
    j = B[i, j]; idx.append(j)
idx = idx[::-1]
segs = [(pos[idx[i]], pos[idx[i + 1]]) for i in range(n)]
print(f'rate {rate:.3f}s/mora')
for b, (a, e), x in zip(blocks, segs, exp):
    flag = ' <<' if abs(math.log((e - a) / x)) > 0.35 else ''
    print(f'{a:6.2f}-{e:6.2f} ({e - a:4.2f} exp {x:4.2f}){flag}  {"".join(b)}')
json.dump(dict(segs=segs, total=total), open('audio/align.json', 'w'))
