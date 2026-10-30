#!/bin/sh
# One command, from nothing to ahcc-longform.mp4: clock (estimated, or from the recording) → reading check → cues → foley (+ voice) → frames → mux → poster
# When the narration is recorded: put voices/narration.wav and voices/times.json (line id → [start, end] in that file) in place, then run this again.
set -e
LIB=${LIB:-/root/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd)
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
PY="$LIB/.venv/bin/python"
python3 "$HERE/tools/timeline.py"
cd "$LIB"
node core/render/readcheck.mjs "$HERE" --size 1920x1080 --step 0.25 --cjk-cps 6 || echo "⚠ reading-time warnings above"
node "$HERE/tools/export_cues.mjs"
"$PY" "$HERE/audio/sound.py"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1920x1080 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/ahcc-longform.mp4" 24 0
# the paper grain makes a large file: re-encode at crf 23 so it stays under GitHub's 100 MB limit
ffmpeg -v error -y -i "$HERE/ahcc-longform.mp4" -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -c:a copy -movflags +faststart "$HERE/out/small.mp4" && mv "$HERE/out/small.mp4" "$HERE/ahcc-longform.mp4"
node core/render/still.mjs "$HERE" 5 --size 1920x1080 --out "$HERE/out" --prefix poster_
cp "$HERE/out/poster_5.jpg" "$HERE/poster.jpg"
