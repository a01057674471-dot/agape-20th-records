#!/usr/bin/env python3
"""Line timings from the narration by speech recognition: transcribe with character timestamps (faster-whisper),
align the script's characters to the transcript, take each line's first and last matched character.
  python tools/align.py audio/narration.mp3   -> cues.json (same format as cues.py)"""
import json, os, re, sys, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cues import script, HERE, TAIL
from faster_whisper import WhisperModel

KEEP = lambda s: re.sub(r'[\s、。「」・，．,.!?！？（）()〜ー…]', '', s)
audio = sys.argv[1]
m = WhisperModel(os.environ.get('WHISPER_MODEL', 'small'), device='cpu', compute_type='int8')
segs, _ = m.transcribe(audio, language='ja', word_timestamps=True, beam_size=5,
                       initial_prompt=''.join(t for _, t in script())[:200])
chars = []                                          # (char, start, end)
for s in segs:
    for w in s.words:
        t = KEEP(w.word)
        for k, ch in enumerate(t):
            a = w.start + (w.end - w.start) * k / len(t); chars.append((ch, a, a + (w.end - w.start) / len(t)))
heard = ''.join(c for c, _, _ in chars)
L = script(); want, owner = '', []
for i, (_, t) in enumerate(L):
    k = KEEP(t.split('\n（')[0] if '（' in t else t); want += k; owner += [i] * len(k)
sm = difflib.SequenceMatcher(None, want, heard, autojunk=False)
hit = {}
for a, b, n in sm.get_matching_blocks():
    for j in range(n): hit[a + j] = b + j
print('matched', len(hit), 'of', len(want), 'chars; heard', len(heard))
lines = []
for i, (c, t) in enumerate(L):
    idx = [hit[p] for p in range(len(want)) if owner[p] == i and p in hit]
    if not idx: sys.exit(f'line {i} not found in the narration: {t}')
    lines.append({'cue': c, 't0': round(chars[min(idx)][1], 2), 't1': round(chars[max(idx)][2], 2), 'text': t, 'i': i})
for a, b in zip(lines, lines[1:]):
    if b['t0'] < a['t1']: b['t0'] = a['t1']
dur = round(lines[-1]['t1'] + TAIL, 2)
json.dump({'dur': dur, 'lines': lines}, open(os.path.join(HERE, 'cues.json'), 'w'), ensure_ascii=False, indent=1)
print('heard:', heard)
for l in lines: print(l['i'], l['t0'], l['t1'], l['text'][:18].replace('\n', '/'))
