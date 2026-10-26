#!/bin/sh
# One command, from nothing to ahcc.mp4: voice (if the speech service is reachable) → cues → score → foley and mix → frames → mux → subtitles → poster
set -e
LIB=${LIB:-/root/lemo-opuscar}
HERE=$(cd "$(dirname "$0")" && pwd)
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
PY="$LIB/.venv/bin/python"
cd "$LIB"
# Korean narration (edge-tts, needs speech.platform.bing.com) and a Whisper check (needs huggingface.co once)
if "$PY" core/tts/tts_zh.py "$HERE/lines.json" "$HERE/voices" --voice ko-KR-SunHiNeural --rate -4%; then
  "$PY" core/tts/asr_check.py "$HERE/lines.json" "$HERE/voices" --lang ko --threshold 0.85 || echo "⚠ voice check reported mismatches: listen before delivery"
else
  echo "⚠ speech service unreachable: building without a voice (subtitles carry the narration)"
fi
node core/render/events.mjs "$HERE" --size 1080x1920
node "$HERE/tools/export_cues.mjs"
"$PY" "$HERE/audio/score.py"
"$PY" "$HERE/audio/sound.py"
node core/render/video.mjs "$HERE" --fps 24 --workers 3 --size 1080x1920 --out "$HERE/out/video.mp4"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/ahcc.mp4" 24 0
"$PY" -c "import json;c=json.load(open('$HERE/audio/cues.json'));json.dump(c['subs'],open('$HERE/subs.json','w'),ensure_ascii=False)"
"$PY" core/render/srt.py "$HERE/subs.json" "$HERE/ahcc.srt"
node core/render/still.mjs "$HERE" 51 --size 1080x1920 --out "$HERE/out" --prefix poster_
cp "$HERE/out/poster_51.jpg" "$HERE/poster.jpg"
