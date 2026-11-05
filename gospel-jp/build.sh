#!/bin/sh
# One command: 「あなたが隠れている場所まで」 -> gospel-jp.mp4 (+ .srt, poster.jpg)
#   sh build.sh                      picture on the script's planned timing, silent
#   sh build.sh audio/narration.mp3  timing fitted to the recorded narration (tools/fit.py), pauses widened
#                                    at scene changes (tools/pace.py); the paced narration is the soundtrack
set -e
LIB=/root/lemo-opuscar
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
PY=$LIB/.venv/bin/python
# line timings: speech recognition when a model is given (ASR_MODEL, see tools/align.py), else pauses + line lengths
if [ -n "$1" ]; then
  if [ -n "$ASR_MODEL" ]; then $PY tools/align.py "$1"; else $PY tools/fit.py "$1"; fi
  $PY tools/pace.py "$1"
else $PY tools/cues.py plan; fi
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
  # H.264 High@4.0, BT.709, AAC, faststart: plays and saves on phones
  ffmpeg -v error -y -i out/video.mp4 -i audio/narration_paced.wav -map 0:v -map 1:a -c:v libx264 -profile:v high -level 4.0 \
    -preset slow -crf 23 -maxrate 3500k -bufsize 7M -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
    -af "apad,atrim=0:$DUR,loudnorm=I=-14:TP=-1.2:LRA=11" -c:a aac -b:a 160k -ar 48000 -movflags +faststart -brand mp42 gospel-jp.mp4
else
  ffmpeg -v error -y -i out/video.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart gospel-jp.mp4
fi
ffmpeg -v error -y -ss $(python3 -c "import json;L=json.load(open('cues.json'))['lines'];print(L[23]['t1']+2.5)") -i gospel-jp.mp4 -frames:v 1 -q:v 2 poster.jpg
echo "done gospel-jp.mp4"
