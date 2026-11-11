"""snap script.STARTS to speech onsets (ends of pauses >= 0.18 s near each start) -> audio/align.json"""
import json, subprocess
from script import STARTS
total = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'audio/narration.mp3']))
sil = [tuple(map(float, l.split())) for l in open('audio/sil.txt') if len(l.split()) == 2]
ends = [b for a, b in sil if b - a >= 0.18]
st = []
for t in STARTS:
    c = [b for b in ends if t - 0.3 <= b <= t + 0.8]
    st.append(max(0.0, (min(c, key=lambda b: abs(b - t)) if c else t) - 0.08) if t > 0 else 0.0)
segs = [(a, b) for a, b in zip(st, st[1:] + [total])]
for (a, b), t in zip(segs, STARTS): print(f'{t:6.2f} -> {a:6.2f}-{b:6.2f}')
json.dump(dict(segs=segs, total=total), open('audio/align.json', 'w'))
