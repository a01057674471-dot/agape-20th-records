#!/usr/bin/env python3
"""Narration timing -> cues.json (one entry per spoken line).

  python3 tools/cues.py plan                 # timings from the script's planned cue windows (no audio yet)
  python3 tools/cues.py audio narration.wav  # timings from the recorded narration: lines are found as
                                             # the speech runs between pauses, in script order

cues.json = {"dur": seconds, "lines": [{"i", "cue", "t0", "t1", "text"}]}
"""
import json, os, re, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAIL = 6.0   # title hold after the last line

def script():
    """[(cue, text)] from SCRIPT.md: Japanese lines under each ### #n heading (translation lines start with '>')."""
    out, cue = [], None
    for ln in open(os.path.join(HERE, 'SCRIPT.md'), encoding='utf-8'):
        ln = ln.rstrip('\n')
        m = re.match(r'### #(\d+)', ln)
        if m: cue = int(m.group(1)); continue
        if cue is None or not ln.strip() or ln.startswith('>') or ln.startswith('#'): continue
        out.append((cue, ln.strip()))
    # the verse (#6) is one spoken piece: written on screen, not subtitled
    merged = []
    for c, t in out:
        if c == 6 and merged and merged[-1][0] == 6: merged[-1] = (6, merged[-1][1] + '\n' + t)
        else: merged.append((c, t))
    return merged

PLAN = {1: (0, 18), 2: (18, 45), 3: (45, 70), 4: (70, 95), 5: (95, 130), 6: (130, 145), 7: (145, 165), 8: (165, 178)}

def plan():
    L = script(); lines = []
    for c, (a, b) in PLAN.items():
        sub = [t for cc, t in L if cc == c]
        a0 = a + (2.0 if c == 1 else 1.2); b0 = b - 0.8
        w = [len(t.replace('\n', '')) + 6 for t in sub]; tot = sum(w); x = a0
        for t, wi in zip(sub, w):
            d = (b0 - a0) * wi / tot
            lines.append({'cue': c, 't0': round(x, 2), 't1': round(x + d - 0.55, 2), 'text': t}); x += d
    return lines

def audio(path):
    L = script()
    sr = 16000
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    hop = sr // 100; n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    thr = max(np.percentile(db, 95) - 30, -50); on = db > thr
    runs, i = [], 0                                    # speech runs, joined across gaps < 0.25 s
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]: j += 1
            if runs and i - runs[-1][1] < 25: runs[-1][1] = j
            else: runs.append([i, j])
            i = j
        else: i += 1
    runs = [r for r in runs if r[1] - r[0] > 12]
    need = len(L)
    while len(runs) > need:                           # merge across the shortest gap until one run per line
        g = min(range(len(runs) - 1), key=lambda k: runs[k + 1][0] - runs[k][1])
        runs[g][1] = runs[g + 1][1]; del runs[g + 1]
    if len(runs) < need:
        sys.exit(f'found {len(runs)} speech runs for {need} lines: leave a clear pause (≥0.5 s) between lines')
    return [{'cue': c, 't0': round(a / 100, 2), 't1': round(b / 100, 2), 'text': t} for (c, t), (a, b) in zip(L, runs)]

if __name__ == '__main__':
    lines = plan() if sys.argv[1] == 'plan' else audio(sys.argv[2])
    for k, l in enumerate(lines): l['i'] = k
    dur = round(lines[-1]['t1'] + TAIL, 2)
    json.dump({'dur': dur, 'lines': lines}, open(os.path.join(HERE, 'cues.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(lines), 'lines, dur', dur)
