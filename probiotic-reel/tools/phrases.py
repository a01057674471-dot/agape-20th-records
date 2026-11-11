#!/usr/bin/env python3
"""Print the narration's speech phrases (split at pauses) with a Korean transcript of each, to time the subtitles.
  ASR_MODEL=<sherpa-onnx-zipformer-korean dir> python tools/phrases.py audio/narration.mp3"""
import os, subprocess, sys
import numpy as np, sherpa_onnx
M = os.environ['ASR_MODEL']
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f'{M}/encoder-epoch-99-avg-1.int8.onnx', decoder=f'{M}/decoder-epoch-99-avg-1.int8.onnx',
                                                   joiner=f'{M}/joiner-epoch-99-avg-1.int8.onnx', tokens=f'{M}/tokens.txt', num_threads=4)
sr = 16000
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
hop = 160; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
q = db < -45; runs = []; k = 0
gap = int(float(os.environ.get('GAP', '0.2')) * 100)
while k < n:
    if not q[k]:
        j = k
        while j < n and not q[j]: j += 1
        if runs and k - runs[-1][1] < gap: runs[-1][1] = j
        else: runs.append([k, j])
        k = j
    else: k += 1
for a, b in runs:
    if b - a < 8: continue
    pad = np.zeros(4800, np.float32); s = rec.create_stream()
    s.accept_waveform(sr, np.concatenate([pad, x[max(0, a - 5) * hop:(b + 5) * hop], pad])); rec.decode_stream(s)
    print(f'{a/100:6.2f}-{b/100:6.2f}', s.result.text)
