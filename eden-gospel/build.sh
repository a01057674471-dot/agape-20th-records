#!/bin/sh
# One command, from nothing to eden-gospel.mp4: cues → score → foley and mix → frames → mux → subtitles → poster
set -e
LIB=${LIB:-/root/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd)
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
PY="$LIB/.venv/bin/python"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node "$HERE/tools/export_cues.mjs"
"$PY" "$HERE/audio/score.py"
"$PY" "$HERE/audio/sound.py"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1080x1920 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/eden-gospel.mp4" 24 1
"$PY" "$HERE/tools/subs.py"
"$PY" core/render/srt.py "$HERE/subs.json" "$HERE/eden-gospel.srt"
node core/render/still.mjs "$HERE" 59.6 --size 1080x1920 --out "$HERE/out" --prefix poster_
cp "$HERE/out/poster_59.6.jpg" "$HERE/poster.jpg"
