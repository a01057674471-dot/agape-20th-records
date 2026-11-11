#!/bin/sh
# mix audio/bgm.wav (from bgm.py) under the narration, ducking it while she speaks; video stream copied
# BGM: audio/bgm.wav = 71.1 s from 2:00 of audio/user_bgm.mp3 (the user-supplied track), faded in/out; bgm.py makes the synthesised koto/shō alternative
set -e
ffmpeg -v error -y -i seireki_9x16.mp4 -i audio/bgm.wav -filter_complex "[0:a]aresample=48000,asplit[n][sc];[1:a]volume='0.16+0.12*clip((t-67.5)/1.0,0,1)':eval=frame[m];[m][sc]sidechaincompress=threshold=0.03:ratio=3:attack=40:release=700[md];[n][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart seireki_bgm_9x16.mp4
ffmpeg -v error -y -i seireki_reel.mp4 -i seireki_bgm_9x16.mp4 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -movflags +faststart seireki_bgm_reel.mp4
