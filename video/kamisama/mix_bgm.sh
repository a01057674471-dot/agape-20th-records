#!/bin/sh
# mix audio/bgm.wav (from bgm.py) under the narration, ducking it while she speaks; video stream copied
set -e
ffmpeg -v error -y -i kamisama_9x16.mp4 -i audio/bgm.wav -filter_complex "[0:a]aresample=48000,asplit[n][sc];[1:a]volume='0.13+0.09*clip((t-51.8)/1.2,0,1)':eval=frame[m];[m][sc]sidechaincompress=threshold=0.03:ratio=3:attack=40:release=700[md];[n][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart kamisama_bgm_9x16.mp4
ffmpeg -v error -y -i kamisama_reel.mp4 -i kamisama_bgm_9x16.mp4 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -movflags +faststart kamisama_bgm_reel.mp4
