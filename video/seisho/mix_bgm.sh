#!/bin/sh
# mix audio/bgm.wav (from bgm.py) under the narration, ducking it while she speaks; video stream copied
# BGM: audio/bgm.wav = all of audio/user_bgm.mp3 (the user-supplied track) slowed 5% (atempo 0.952) to fill 66.3 s, faded in/out; bgm.py makes the synthesised koto/shō alternative
set -e
ffmpeg -v error -y -i seisho_9x16.mp4 -i audio/bgm.wav -filter_complex "[0:a]aresample=48000,asplit[n][sc];[1:a]volume='0.13+0.11*clip((t-62.7)/1.0,0,1)':eval=frame[m];[m][sc]sidechaincompress=threshold=0.03:ratio=3:attack=40:release=700[md];[n][md]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart seisho_bgm_9x16.mp4
ffmpeg -v error -y -i seisho_reel.mp4 -i seisho_bgm_9x16.mp4 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -movflags +faststart seisho_bgm_reel.mp4
