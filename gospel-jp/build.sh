#!/bin/sh
# One command: 「あなたが隠れている場所まで」 -> gospel-jp.mp4 (+ .srt, poster.jpg)
#   sh build.sh                      picture on the script's planned timing, silent
#   sh build.sh audio/narration.mp3  timing fitted to the recorded narration (tools/fit.py), pauses widened
#                                    at scene changes (tools/pace.py); the paced narration is the soundtrack
set -e
LIB=/root/lemo-opuscar
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
PY=$LIB/.venv/bin/python
if [ -n "$1" ]; then $PY tools/fit.py "$1" && $PY tools/pace.py "$1"; else $PY tools/cues.py plan; fi
sh tools/fonts.sh
[ -f paper.jpg ] || $PY tools/paper.py
[ -f grain.png ] || $PY tools/grain.py
mkdir -p out
(cd "$LIB" && node core/render/video.mjs "$HERE" --fps 24 --workers 4 --out "$HERE/out/video.mp4")
python3 -c "
import json
d=json.load(open('cues.json'))
L=d['lines']
json.dump([{'t0':l['t0'],'t1':min(max(l['t1']+.4,l['t0']+1.8),L[k+1]['t0']-.12 if k+1<len(L) else 1e9),'text':l['text'].replace(chr(10),' ')} for k,l in enumerate(L)],open('out/subs.json','w'),ensure_ascii=False)"
$PY $LIB/core/render/srt.py out/subs.json gospel-jp.srt
DUR=$(python3 -c "import json;print(json.load(open('cues.json'))['dur'])")
if [ -n "$1" ]; then
  ffmpeg -v error -y -i audio/narration_paced.wav -af "apad,atrim=0:$DUR" -ar 48000 -ac 2 out/mix.wav
  sh $LIB/core/render/mux.sh out/video.mp4 out/mix.wav gospel-jp.mp4 24 0
else
  ffmpeg -v error -y -i out/video.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart gospel-jp.mp4
fi
ffmpeg -v error -y -ss $(python3 -c "import json;L=json.load(open('cues.json'))['lines'];print(L[23]['t1']+2.5)") -i gospel-jp.mp4 -frames:v 1 -q:v 2 poster.jpg
echo "done gospel-jp.mp4"
