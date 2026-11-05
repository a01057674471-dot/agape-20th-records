#!/usr/bin/env python3
"""Give the narration room to breathe: insert silence in the pause after chosen lines (and a lead-in),
shift cues.json to match, write audio/narration_paced.wav.   python tools/pace.py audio/narration.mp3"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cues import HERE

LEAD = 2.5
AFTER = {1: 2.5, 5: 1.5, 6: 1.5, 7: 2.5, 10: 1.5, 13: 2.5, 15: 1.0, 17: 1.5, 18: 3.0, 20: 1.0,
         22: 3.0, 23: 2.5, 24: 2.0, 25: 3.0, 27: 2.0, 30: 2.5, 32: 1.0}
TAIL = 9.5
sr = 48000
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.float32)
d = json.load(open(os.path.join(HERE, 'cues.json'))); L = d['lines']
cuts = []                                    # (time in the original, seconds of silence to insert there)
for i, s in AFTER.items(): cuts.append(((L[i]['t1'] + L[i + 1]['t0']) / 2, s))
cuts.sort(); parts, prev, shift = [np.zeros(int(LEAD * sr), np.float32)], 0, []
for t, s in cuts:
    k = int(t * sr); parts += [x[prev:k], np.zeros(int(s * sr), np.float32)]; prev = k
parts.append(x[prev:])
y = np.concatenate(parts)
def moved(t): return t + LEAD + sum(s for c, s in cuts if c < t)
for l in L: l['t0'] = round(moved(l['t0']), 2); l['t1'] = round(moved(l['t1']), 2)
d['dur'] = round(L[-1]['t1'] + TAIL, 2)
y = np.concatenate([y, np.zeros(max(0, int(d['dur'] * sr) - len(y)), np.float32)])[:int(d['dur'] * sr)]
out = os.path.join(HERE, 'audio', 'narration_paced.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', '-', '-ac', '2', out], input=y.tobytes(), check=True)
json.dump(d, open(os.path.join(HERE, 'cues.json'), 'w'), ensure_ascii=False, indent=1)
print('paced', d['dur'], 's ->', out)
