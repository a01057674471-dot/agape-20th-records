#!/usr/bin/env python3
"""Start/end of each script line in the narration, from Korean speech recognition with token timestamps.
  ASR_MODEL=<sherpa-onnx-zipformer-korean dir> python tools/align.py audio/narration.mp3 -> audio/lines.json"""
import json, os, re, subprocess, sys, difflib
import numpy as np, sherpa_onnx
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINES = ['러닝 끝나고 이거 하면, 뛴 거 손해 봐요.', '하나, 바로 주저앉기.', '어지러울 수 있어요.', '3~5분은 천천히 걸어요.',
         '둘, 땀에 젖은 옷 그대로.', '몸이 식고 피부 트러블이 생길 수 있어요.', '바로 갈아입어요.',
         '셋, 바로 뜨거운 샤워나 사우나.', '숨부터 고르고, 미지근한 물로 시작해요.',
         '넷, 물 안 마시기, 또는 한 번에 벌컥벌컥.', '조금씩 나눠 마셔요.',
         '다섯, 뛰었으니까 맥주 한 잔?', '수분이 더 빠지고 회복이 느려져요.', '물과 식사 먼저.',
         '잘 뛰는 것만큼, 잘 끝내는 게 실력.', '몇 개 해당돼요?', '댓글로 알려 주세요.']
SAY = {'3~5분은': '삼에서오분은'}
KEEP = lambda s: re.sub(r'[\s,.?!~·]', '', s)
M = os.environ['ASR_MODEL']
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{M}/encoder-epoch-99-avg-1.int8.onnx', decoder=f'{M}/decoder-epoch-99-avg-1.int8.onnx',
                                                   joiner=f'{M}/joiner-epoch-99-avg-1.int8.onnx', tokens=f'{M}/tokens.txt', num_threads=4)
sr = 16000
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
hop = 160; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
q = db < -45; runs, k = [], 0
while k < n:
    if not q[k]:
        j = k
        while j < n and not q[j]: j += 1
        if runs and k - runs[-1][1] < 5: runs[-1][1] = j
        else: runs.append([k, j])
        k = j
    else: k += 1
chars = []
for a, b in runs:
    if b - a < 8: continue
    a0 = max(0, a - 5); pad = np.zeros(4800, np.float32); s = rec.create_stream()
    s.accept_waveform(sr, np.concatenate([pad, x[a0 * hop:(b + 5) * hop], pad])); rec.decode_stream(s)
    for tok, ts in zip(s.result.tokens, s.result.timestamps):
        for ch in KEEP(tok.replace('▁', '')): chars.append((ch, a0 / 100 + ts - .3))
heard = ''.join(c for c, _ in chars)
want, owner = '', []
for i, l in enumerate(LINES):
    for w, r in SAY.items(): l = l.replace(w, r)
    kk = KEEP(l); want += kk; owner += [i] * len(kk)
hit = {}
for a, b, m in difflib.SequenceMatcher(None, want, heard, autojunk=False).get_matching_blocks():
    for j in range(m): hit[a + j] = b + j
out = []
for i, l in enumerate(LINES):
    idx = [hit[p] for p in range(len(want)) if owner[p] == i and p in hit]
    out.append({'text': l, 't0': round(chars[min(idx)][1] - .05, 2) if idx else None, 't1': round(chars[max(idx)][1] + .25, 2) if idx else None})
for k2, o in enumerate(out):   # fill a line not heard from its neighbours
    if o['t0'] is None: o['t0'] = out[k2 - 1]['t1']; o['t1'] = out[k2 + 1]['t0'] if k2 + 1 < len(out) else o['t0'] + 1
for a, b in zip(out, out[1:]): a['t1'] = min(a['t1'], b['t0'] - .02)
json.dump(out, open(os.path.join(HERE, 'audio', 'lines.json'), 'w'), ensure_ascii=False, indent=1)
print('heard:', heard); print('matched', len(hit), 'of', len(want))
for o in out: print(f"{o['t0']:6.2f}-{o['t1']:6.2f} {o['text']}")
