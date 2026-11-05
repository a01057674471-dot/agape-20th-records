#!/usr/bin/env python3
"""Line timings from the narration by speech recognition (sherpa-onnx, ReazonSpeech Japanese zipformer, offline).
The audio is cut at pauses into chunks of up to ~12 s, each chunk transcribed with token timestamps, the script's
characters aligned to the transcript; each line takes its first and last matched character.
  ASR_MODEL=<model dir> python tools/align.py audio/narration.mp3 -> cues.json
Model: github.com/k2-fsa/sherpa-onnx/releases (asr-models/sherpa-onnx-zipformer-ja-reazonspeech-2024-08-01)."""
import json, os, re, subprocess, sys, difflib
import numpy as np, sherpa_onnx
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cues import script, HERE, TAIL

KEEP = lambda s: re.sub(r'[\s、。「」・，．,.!?！？（）()〜ー…]', '', s)
M = os.environ['ASR_MODEL']
rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=f'{M}/encoder-epoch-99-avg-1.int8.onnx', decoder=f'{M}/decoder-epoch-99-avg-1.int8.onnx',
    joiner=f'{M}/joiner-epoch-99-avg-1.int8.onnx', tokens=f'{M}/tokens.txt', num_threads=4, decoding_method='greedy_search')
sr = 16000
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
hop = sr // 100; n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
quiet = db < max(np.percentile(db, 97) - 32, -55)
cuts, last = [0], 0                                   # cut in the middle of pauses, chunks ≤ 12 s
k = 0
while k < n:
    if quiet[k]:
        j = k
        while j < n and quiet[j]: j += 1
        mid = (k + j) // 2
        if j - k >= 20 and mid - cuts[-1] > 60: cuts.append(mid)
        k = j
    else: k += 1
    if k - cuts[-1] > 1200:                           # force a cut at the longest pause in the window
        w = quiet[cuts[-1] + 300:k].astype(int); cuts.append(cuts[-1] + 300 + int(np.argmax(np.convolve(w, np.ones(15), 'same'))))
cuts.append(n)
chars, heard_txt = [], ''
for a, b in zip(cuts, cuts[1:]):
    pad = np.zeros(int(.3 * sr), np.float32)
    s = rec.create_stream(); s.accept_waveform(sr, np.concatenate([pad, x[a * hop:b * hop], pad])); rec.decode_stream(s)
    r = s.result; heard_txt += r.text + '|'
    for tok, ts in zip(r.tokens, r.timestamps):
        for ch in KEEP(tok): chars.append((ch, a / 100 + ts - .3))
heard = ''.join(c for c, _ in chars)
L = script(); want, owner = '', []
for i, (_, t) in enumerate(L):
    kk = KEEP(t); want += kk; owner += [i] * len(kk)
sm = difflib.SequenceMatcher(None, want, heard, autojunk=False)
hit = {}
for a, b, m in sm.get_matching_blocks():
    for j in range(m): hit[a + j] = b + j
print('heard:', heard_txt)
print('matched', len(hit), 'of', len(want), 'script chars')
# pauses in the recording (quiet stretches of at least 0.12 s)
q2 = db < -45; P, k = [], 0
while k < n:
    if q2[k]:
        j = k
        while j < n and q2[j]: j += 1
        if j - k >= 12: P.append((k / 100, j / 100))
        k = j
    else: k += 1
def snap(b, lo, hi):              # the pause that best explains a boundary near b, inside (lo, hi)
    c = [p for p in P if lo < (p[0] + p[1]) / 2 < hi]
    return min(c, key=lambda p: abs((p[0] + p[1]) / 2 - b) - .6 * (p[1] - p[0])) if c else (b, b)
first, last = [], []
for i, (c, t) in enumerate(L):
    idx = [hit[p] for p in range(len(want)) if owner[p] == i and p in hit]
    first.append(chars[min(idx)][1] if idx else None); last.append(chars[max(idx)][1] if idx else None)
    if not idx: print(f'line {i} not recognised, placed between its neighbours: {t}')
bounds = []                       # pause between line i and i+1
for i in range(len(L) - 1):
    a = last[i] + .15 if last[i] is not None else None
    b = first[i + 1] if first[i + 1] is not None else None
    est = (a + b) / 2 if a is not None and b is not None else (a if a is not None else b)
    lo = (bounds[-1][1] if bounds else 0) + .2
    bounds.append(snap(est, lo, est + .8))
t_start = (P[0][1] if P and P[0][0] < .05 else 0)
lines = []
for i, (c, t) in enumerate(L):
    t0 = bounds[i - 1][1] if i else t_start
    t1 = bounds[i][0] if i < len(L) - 1 else max(P[-1][0] if P else n / 100, t0 + .5)
    lines.append({'cue': c, 't0': round(t0, 2), 't1': round(t1, 2), 'text': t, 'i': i})
dur = round(lines[-1]['t1'] + TAIL, 2)
json.dump({'dur': dur, 'lines': lines}, open(os.path.join(HERE, 'cues.json'), 'w'), ensure_ascii=False, indent=1)
for l in lines: print(f"{l['i']:2d} {l['t0']:6.2f}-{l['t1']:6.2f}  {l['text'][:18]}")
