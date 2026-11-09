#!/bin/sh
# One command: sound -> frames -> phone-safe mp4 -> poster
set -e
LIB=/root/lemo-opuscar
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
PY=$LIB/.venv/bin/python
[ -f fonts.css ] || sh tools/fonts.sh
$PY audio/sound.py
(cd "$LIB" && node core/render/video.mjs "$HERE" --fps 24 --workers 4 --size 1080x1920 --out "$HERE/out/video.mp4")
ffmpeg -v error -y -i out/video.mp4 -i out/mix.wav -map 0:v -map 1:a -c:v libx264 -profile:v high -level 4.0 -preset slow -crf 20 \
  -maxrate 8M -bufsize 16M -pix_fmt yuv420p -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -af "loudnorm=I=-14:TP=-1.2:LRA=11" -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart -brand mp42 oligopa-cell.mp4
ffmpeg -v error -y -ss 22.2 -i oligopa-cell.mp4 -frames:v 1 -q:v 2 poster.jpg
ffprobe -v error -show_entries format=duration,size -of csv=p=0 oligopa-cell.mp4
