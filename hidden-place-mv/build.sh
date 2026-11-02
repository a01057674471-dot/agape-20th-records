#!/bin/bash
# out/video.mp4 (the picture) + audio/song.mp3 → hidden-place-mv.mp4 (the song untouched apart from a 0.4 s fade-in guard; −14 LUFS for YouTube)
set -e; cd "$(dirname "$0")"
ffmpeg -y -v error -i out/video.mp4 -i audio/song.mp3 -map 0:v -map 1:a -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -tune film \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart hidden-place-mv.mp4
ffprobe -v error -show_entries format=duration,size -of csv=p=0 hidden-place-mv.mp4
