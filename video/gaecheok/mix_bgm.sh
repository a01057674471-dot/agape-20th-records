#!/bin/sh
# lay audio/bgm.wav (Tranquil Peace looped x4 with crossfades, trimmed, faded; the film has no narration) under the video
set -e
ffmpeg -v error -y -i gaecheok_16x9.mp4 -i audio/bgm.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart gaecheok_youtube.mp4
