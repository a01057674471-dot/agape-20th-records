#!/usr/bin/env python3
"""「내가 숨은 곳까지」 live-action cut: twelve 10 s clips laid to the song (277.6 s).

Each shot is a slice of one clip, retimed to its slot with motion interpolation, lightly graded
(cool at night, neutral, then soft daylight), joined with short dissolves, a white bloom where the
vocal returns (3:42, the door opens), titles, and the song.

  python3 build.py          -> hidden-place-live.mp4
Needs clips/01..12.mp4 (the user's clips, in the order they were given; not committed) and
../hidden-place-mv/audio/song.mp3.
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SONG = os.path.join(HERE, '..', 'hidden-place-mv', 'audio', 'song.mp3')
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
FPS, X, DUR = 24, 0.5, 277.632   # X = dissolve length

# clips (the order given):
#  1 bus window, night      2 sitting on the bed, door ajar   3 curtain blowing, at the window
#  4 stairwell, going down  5 her hand meets a hand          6 walking the street
#  7 sitting on the steps   8 walking the bridge at dusk      9 notebook pages
# 10 standing in the church 11 riverside with the coat      12 close-up by the river
# (slot start, clip, src in, src out, zoom, look)   look: 0 night-cool .. 1 neutral .. 2 day
SHOTS = [
    (0,     1, 0, 10, 1.00, 0),     # intro: the bus at night
    (13,    2, 0, 10, 1.00, 0),     # verse 1: hiding in the room
    (27.5,  9, 0, 10, 1.00, 0),     # the notebook
    (42,    3, 0, 10, 1.00, .3),    # wind in the curtain
    (57,    1, 4, 10, 1.25, 0),     # the night again, closer
    (64,    5, 0, 5.5, 1.00, .5),   # chorus 1: a hand waits
    (76,   12, 0, 8, 1.00, .7),     # her face
    (88,    5, 4.5, 10, 1.15, .8),  # the hands meet
    (98,    3, 4, 10, 1.20, 1),     # light comes in
    (106,   4, 0, 6, 1.00, 1),      # verse 2: down the stairs
    (116,   6, 0, 10, 1.00, 1),     # into the street
    (127,   4, 5, 10, 1.20, 1),
    (134,   8, 0, 10, 1.00, 1),     # over the bridge
    (145,  10, 0, 8, 1.00, 1),      # the church
    (156,   7, 0, 10, 1.00, 1.1),   # sitting by a door
    (176,  10, 4, 10, 1.25, 1.1),
    (186,   8, 4, 10, 1.20, 1.1),
    (196,  12, 3, 10, 1.20, 1.2),   # bridge
    (204,   9, 3, 10, 1.25, 1.2),
    (214,   2, 3, 9, 1.20, 1.2),    # back in the room... door ajar
    (222,  11, 0, 10, 1.00, 2),     # vocal returns: out into the day
    (236,   6, 2, 10, 1.15, 2),     # final chorus
    (248,   5, 1, 10, 1.00, 2),
    (258,   7, 3, 10, 1.20, 2),
    (265,  11, 3, 10, 1.20, 2),     # walking on with the coat
]
BLOOM = 222   # white bloom instead of a dissolve at this cut

def grade(look):
    # cool, slightly lifted night -> neutral -> gentle daylight; never heavy yellow
    if look <= 1:
        k = look
        rs, bs = -0.06 * (1 - k), 0.07 * (1 - k)
        sat, gam = 0.85 + 0.1 * k, 1.0
    else:
        k = look - 1
        rs, bs = 0.02 * k, -0.01 * k
        sat, gam = 0.95, 1.0 + 0.04 * k
    return (f"colorbalance=rs={rs:.3f}:bs={bs:.3f}:rm={rs/2:.3f}:bm={bs/2:.3f},"
            f"eq=saturation={sat:.3f}:gamma={gam:.3f}")

def tr(i):   # transition INTO shot i: (kind, duration, lead before the cut)
    return ('fadewhite', 1.2, 0.6) if SHOTS[i][0] == BLOOM else ('fade', X, 0.0)

def slot(i):   # output length of shot i, including its overlaps
    a = SHOTS[i][0]; b = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else DUR
    lead = tr(i)[2] if i else 0.0
    tail = (tr(i + 1)[1] - tr(i + 1)[2]) if i + 1 < len(SHOTS) else 0.0
    return b - a + lead + tail

def render(i):
    t0, clip, a, b, z, look = SHOTS[i]
    d = slot(i); n = round(d * FPS); k = d / (b - a)
    src = os.path.join(HERE, 'clips', f'{clip:02d}.mp4')
    w, h = 1284, 724
    cw, ch = int(w / z) // 2 * 2, int(w / z * 9 / 16) // 2 * 2
    vf = (f"trim={a}:{b},setpts=PTS-STARTPTS,mpdecimate,setpts={k:.5f}*PTS,"
          f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
          f"crop={cw}:{ch}:(iw-{cw})/2:(ih-{ch})/2,scale=1920:1080:flags=lanczos,setsar=1,"
          f"{grade(look)},vignette=PI/5,noise=alls=3:allf=t,"
          f"tpad=stop_mode=clone:stop_duration=2,trim=end_frame={n},format=yuv420p")
    out = os.path.join(OUT, f'seg{i:02d}.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', vf, '-an', '-r', str(FPS),
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', out], check=True)
    print('seg', i, f'{d:.2f}s x{1/k:.2f}', flush=True)
    return out

def main():
    with ThreadPoolExecutor(4) as ex: segs = list(ex.map(render, range(len(SHOTS))))
    F = os.path.join(HERE, 'fonts', 'myeongjo-1.ttf')
    inputs, fc, last = [], [], '0:v'
    for p in segs: inputs += ['-i', p]
    for i in range(1, len(segs)):
        kind, dx, lead = tr(i)
        fc.append(f"[{last}][{i}:v]xfade=transition={kind}:duration={dx}:offset={SHOTS[i][0] - lead:.4f}[v{i}]")
        last = f'v{i}'
    def title(text, t0, t1, y):
        al = f"if(lt(t,{t0}),0,if(lt(t,{t0+1.5}),(t-{t0})/1.5,if(lt(t,{t1-1.5}),1,if(lt(t,{t1}),({t1}-t)/1.5,0))))"
        return (f"drawtext=fontfile={F}:text='{text}':fontsize=64:fontcolor=white:alpha='{al}*0.92':"
                f"x=(w-text_w)/2:y={y}:shadowcolor=black@0.35:shadowx=0:shadowy=2")
    fc.append(f"[{last}]{title('내가 숨은 곳까지', 2.5, 11, 'h*0.78')},"
              f"{title('주님은 버리지 않으셨죠', DUR-11, DUR-2.6, 'h*0.78')},"
              f"fade=t=in:st=0:d=1.5,fade=t=out:st={DUR-2.5}:d=2.5,format=yuv420p[v]")
    vid = os.path.join(OUT, 'video.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[v]',
                    '-r', str(FPS), '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', vid], check=True)
    final = os.path.join(HERE, 'hidden-place-live.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', SONG, '-map', '0:v', '-map', '1:a',
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-af', 'loudnorm=I=-14:TP=-1:LRA=11', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
                    '-shortest', '-movflags', '+faststart', final], check=True)
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,size', '-of', 'csv=p=0', final],
                       capture_output=True, text=True)
    print('final', final, r.stdout.strip())

if __name__ == '__main__':
    main()
