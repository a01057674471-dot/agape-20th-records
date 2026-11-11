#!/usr/bin/env python3
"""Widen the narration a little: silence after the hook and after each ⭕ line, so every ❌ → ⭕ card can be read.
audio/lines.json (recording times) -> audio/lines_paced.json + audio/narration_paced.wav"""
import json, os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AFTER = {0: .45, 3: .9, 6: .9, 8: .9, 10: .9, 13: 1.0}
L = json.load(open(os.path.join(HERE, 'audio', 'lines.json')))
sr = 48000
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(HERE, 'audio', 'narration.mp3'), '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)
cuts = sorted(((L[i]['t1'] + L[i + 1]['t0']) / 2, s) for i, s in AFTER.items())
parts, prev = [], 0
for t, s in cuts: k = int(t * sr); parts += [x[prev:k], np.zeros(int(s * sr), np.float32)]; prev = k
parts.append(x[prev:]); y = np.concatenate(parts)
mv = lambda t: t + sum(s for c, s in cuts if c < t)
P = [{'text': l['text'], 't0': round(mv(l['t0']), 2), 't1': round(mv(l['t1']), 2)} for l in L]
json.dump(P, open(os.path.join(HERE, 'audio', 'lines_paced.json'), 'w'), ensure_ascii=False, indent=1)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', os.path.join(HERE, 'audio', 'narration_paced.wav')], input=y.tobytes(), check=True)
print('paced', round(len(y) / sr, 2), 's')
for p in P: print(p['t0'], p['t1'], p['text'])
