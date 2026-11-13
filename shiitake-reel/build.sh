#!/bin/sh
# 「표고버섯, 4주 매일 먹었더니 면역세포가?」 -> shiitake-reel.mp4
#   CMS = 자막 모션 스킬(caption-motion-seqc) 폴더 (이 환경에선 폰트를 Google Fonts로 등록한 사본)
set -e
LIB=/root/lemo-opuscar; HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"; CMS=${CMS:?set CMS to the caption-motion-seqc folder}
[ -f fonts.css ] || sh tools/fonts.sh
$LIB/.venv/bin/python audio/sound.py
(cd "$LIB" && node core/render/video.mjs "$HERE" --fps 24 --workers 4 --size 1080x1920 --out "$HERE/out/video.mp4")
ffmpeg -v error -y -i out/video.mp4 -i out/mix.wav -map 0:v -map 1:a -c:v libx264 -crf 16 -pix_fmt yuv420p -af "loudnorm=I=-14:TP=-1.2:LRA=11" -c:a aac -b:a 192k -shortest out/base.mp4
(cd "$CMS" && node scripts/subs.cjs "$HERE/captions/captions.json")
ffmpeg -v error -y -i "$CMS/out/captions.mp4" -c:v libx264 -profile:v high -level 4.0 -preset slow -crf 20 -maxrate 8M -bufsize 16M -pix_fmt yuv420p \
  -color_range tv -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 192k -ar 48000 -movflags +faststart -brand mp42 shiitake-reel.mp4
