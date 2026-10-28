#!/bin/sh
# One command, from nothing to barehand.mp4: narration timeline → reading check → cues → score, foley and voice → frames → mux → poster
set -e
LIB=${LIB:-/root/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd)
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
PY="$LIB/.venv/bin/python"
cd "$LIB"
python3 "$HERE/tools/voice.py"
# every line on screen is also spoken, so the reading check runs at 8 chars/s and only warns
node core/render/readcheck.mjs "$HERE" --size 1080x1920 --step 0.08 --cjk-cps 8 || echo "⚠ reading-time warnings above (these lines are read aloud by the narration)"
node "$HERE/tools/export_cues.mjs"
"$PY" "$HERE/audio/score.py"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1080x1920 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/barehand.mp4" 24 0
# mix.wav carries trailing silence for mux.sh's length check: cut the film back to the picture
VD=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$HERE/barehand.mp4")
ffmpeg -v error -y -i "$HERE/barehand.mp4" -t "$VD" -c copy -movflags +faststart "$HERE/out/trim.mp4" && mv "$HERE/out/trim.mp4" "$HERE/barehand.mp4"
node core/render/still.mjs "$HERE" 2.5 --size 1080x1920 --out "$HERE/out" --prefix poster_
cp "$HERE/out/poster_2.5.jpg" "$HERE/poster.jpg"
