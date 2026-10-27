#!/bin/sh
# One command, from nothing to oligopa.mp4: reading check → cues → foley mix → frames → mux → poster. No music by design.
set -e
LIB=${LIB:-/root/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd)
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
PY="$LIB/.venv/bin/python"
cd "$LIB"
node core/render/readcheck.mjs "$HERE" --size 1080x1920 --step 0.08 --cjk-cps 6
node "$HERE/tools/export_cues.mjs"
"$PY" "$HERE/audio/sound.py"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1080x1920 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/oligopa.mp4" 24 0
# mix.wav carries trailing silence for mux.sh's length check: cut the film back to the picture
VD=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$HERE/oligopa.mp4")
ffmpeg -v error -y -i "$HERE/oligopa.mp4" -t "$VD" -c copy -movflags +faststart "$HERE/out/trim.mp4" && mv "$HERE/out/trim.mp4" "$HERE/oligopa.mp4"
node core/render/still.mjs "$HERE" 38.5 --size 1080x1920 --out "$HERE/out" --prefix poster_
cp "$HERE/out/poster_38.5.jpg" "$HERE/poster.jpg"
