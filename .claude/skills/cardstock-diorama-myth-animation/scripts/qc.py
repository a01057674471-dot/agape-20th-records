#!/usr/bin/env python3
"""
QC for paper-diorama hero frames and clips (multi-shot producer edition).

    python qc.py frame a.png b.png c.png      # pick a hero frame on numbers
    python qc.py video shot_04.mp4            # full pass on one finished clip

Optional palette override (defaults to the reference cream/vermilion/navy). Pass
the film's locked palette so the share/flat-field checks use the right colours:
    --ground '#DCC0A0' --accent '#6B3389' --void '#16301C'

Targets come from measuring the reference films. See references/palette.md.

The `video` pass also reports the LEADING and TRAILING flat-field runs, so you can
confirm a clip is properly wipe-bookended for its join: a clip that opens an
incoming join should show a ~0.2-0.3s flat head, and one that closes an outgoing
join a ~0.4s flat tail, in the join colour. The concat cut is hidden inside those
flat fields (see references/pipeline.md §9).
"""
import argparse, subprocess, sys
import numpy as np

REF = {'ground': '#DCC0A0', 'accent': '#A02D19', 'void': '#1B2740'}
TARGET_SHARE = {'ground': 45, 'accent': 35, 'void': 20}   # hero frame; time-avg for video
TARGET_LUMA = {'ground': 197, 'accent': 77, 'void': 38}
REF_SWING = 145          # reference luma swing; flat clips come in under ~80


def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def fam(c, pal):
    return min(pal, key=lambda n: sum((int(c[i]) - pal[n][i]) ** 2 for i in range(3)))


def shares(arr, pal, k=6):
    from sklearn.cluster import KMeans
    px = arr.reshape(-1, 3).astype(float)
    km = KMeans(n_clusters=k, n_init=5, random_state=0).fit(px)
    c = km.cluster_centers_.astype(int)
    w = np.bincount(km.labels_, minlength=k) / len(px)
    s = {'ground': 0.0, 'accent': 0.0, 'void': 0.0}
    for i in range(k):
        s[fam(c[i], pal)] += w[i] * 100
    return s


def load_img(path, w=240):
    from PIL import Image
    im = Image.open(path).convert('RGB')
    full = np.array(im.convert('L'))
    small = np.array(im.resize((w, int(w * im.height / im.width))))
    return full, small


def probe(path):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                        '-show_entries', 'stream=width,height,r_frame_rate,nb_frames',
                        '-show_entries', 'format=duration', '-of', 'default=nw=1', path],
                       capture_output=True, text=True).stdout
    d = dict(l.split('=', 1) for l in o.strip().splitlines() if '=' in l)
    return d


def frames(path, w=120, fps=None):
    vf = f'scale={w}:-1' + (f',fps={fps}' if fps else '')
    o = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', vf,
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True).stdout
    d = probe(path)
    h = int(round(w * int(d['height']) / int(d['width'])))
    h -= h % 2
    n = len(o) // (w * h * 3)
    return np.frombuffer(o[:n * w * h * 3], dtype=np.uint8).reshape(n, h, w, 3).astype(float)


def cmd_frame(args, pal):
    print(f"{'file':22} {'mean':>6} {'<10%':>6} {'>245%':>6}   {'grnd':>5} {'accn':>5} {'void':>5}   verdict")
    best = None
    for p in args.files:
        full, small = load_img(p)
        s = shares(small, pal)
        mean = full.mean()
        crush = float((full < 10).mean() * 100)
        blow = float((full > 245).mean() * 100)
        err = sum(abs(s[k] - TARGET_SHARE[k]) for k in s)
        bad = []
        if mean < 95: bad.append('DARK')
        if mean > 175: bad.append('WASHED')
        if crush > 2: bad.append('crushed')
        if blow > 2: bad.append('blown')
        if err > 45: bad.append('palette off')
        v = 'OK' if not bad else ', '.join(bad)
        print(f"{p.split('/')[-1][:22]:22} {mean:6.1f} {crush:6.2f} {blow:6.2f}   "
              f"{s['ground']:5.1f} {s['accent']:5.1f} {s['void']:5.1f}   {v}")
        score = err + crush * 3 + blow * 3
        if not bad and (best is None or score < best[0]):
            best = (score, p)
    print(f"\ntarget: mean 95-175, crushed <2%, blown <2%, share ~"
          f"{TARGET_SHARE['ground']}/{TARGET_SHARE['accent']}/{TARGET_SHARE['void']}")
    if best:
        print(f"PICK -> {best[1]}")
    else:
        print("PICK -> none clean. Re-roll; it costs ~1 min and beats animating a bad plate.")


def wipe_colour(seg):
    return ('cream' if seg[0] > 150 and seg[2] > 110
            else 'vermilion' if seg[0] > seg[2] + 40 else 'void')


def cmd_video(args, pal):
    d = probe(args.files[0])
    fps = eval(d['r_frame_rate'])
    print(f"specs      {d['width']}x{d['height']}  {fps:g}fps  {float(d['duration']):.2f}s")
    if abs(fps - 24) > 0.5:
        print(f"           ^ WARNING: style is native 24fps, this is {fps:g}")

    f = frames(args.files[0])
    g = f.mean(axis=3)
    per = g.mean(axis=(1, 2))
    std = g.std(axis=(1, 2))

    swing = per.max() - per.min()
    print(f"\nexposure   mean {per.mean():.1f}   range {per.min():.1f} -> {per.max():.1f}   "
          f"SWING {swing:.1f}   (reference ~{REF_SWING})")
    if swing < 80:
        print("           ^ TOO FLAT. The reference swings ~150. A global exposure lock in the")
        print("             prompt causes this. Remove it and add paper wipes.")

    # paper wipes = flat colour fields
    runs, cur = [], None
    for i in range(len(f)):
        flat = std[i] < 25
        if flat and cur is None: cur = i
        if not flat and cur is not None:
            if i - cur >= 3: runs.append((cur, i))
            cur = None
    if cur is not None and len(f) - cur >= 3: runs.append((cur, len(f)))
    print(f"\npaper wipes ({len(runs)} found; ~1 per 3-4s of screen time is dense)")
    if not runs:
        print("           none. Name the wipes explicitly, with colour and duration.")
        print("           See references/beats.md.")
    for a, b in runs:
        seg = f[a:b].mean(axis=(0, 1, 2))
        col = wipe_colour(seg)
        dur = (b - a) / fps
        note = '' if 0.15 <= dur <= 0.8 else '  <- TOO LONG, reads as dead air' if dur > 0.8 else '  <- very fast'
        print(f"   {a/fps:5.2f}s -> {b/fps:5.2f}s  ({dur:.2f}s)  {col}{note}")

    # head/tail bookend check — is this clip wipe-bookended for a join?
    def edge_run(indices):
        n = 0
        for i in indices:
            if std[i] < 25: n += 1
            else: break
        return n
    head = edge_run(range(len(f)))
    tail = edge_run(range(len(f) - 1, -1, -1))
    print(f"\nbookends   leading flat field {head/fps:.2f}s"
          + (f" ({wipe_colour(f[:head].mean(axis=(0,1,2)))})" if head else "")
          + f"   trailing flat field {tail/fps:.2f}s"
          + (f" ({wipe_colour(f[-tail:].mean(axis=(0,1,2)))})" if tail else ""))
    print("           (a clip opening an incoming join wants a ~0.2-0.3s flat head;")
    print("            one closing an outgoing join wants a ~0.4s flat tail, in the join colour.")
    print("            The concat cut hides inside these. Cold-open shot 1 and the final shot hold.)")

    # motion, and whether stalls are wipes or bugs
    dif = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))
    sec = [float(dif[int(i*fps):int((i+1)*fps)].mean()) for i in range(int(len(dif)/fps))]
    print(f"\nmotion/sec {[round(x,1) for x in sec]}")
    for i, m in enumerate(sec):
        if m < 0.6:
            j = int((i + 0.5) * fps)
            if j < len(std):
                kind = ('flat field -> a paper wipe, fine' if std[j] < 25
                        else 'FULL DETAIL, FROZEN -> a bug. Never write "hold" in the prompt.')
                print(f"           second {i}: dead ({m:.1f}) — {kind}")

    # palette: time-average, not per-frame
    small = f[::max(1, len(f)//40)]
    s = shares(small.reshape(-1, small.shape[2], 3).astype(np.uint8), pal)
    print(f"\npalette    TIME-AVERAGED  ground {s['ground']:.1f}%  accent {s['accent']:.1f}%  void {s['void']:.1f}%")
    print(f"           (target ~{TARGET_SHARE['ground']}/{TARGET_SHARE['accent']}/{TARGET_SHARE['void']} "
          f"averaged over the film — per-frame is SUPPOSED to swing)")
    if s['ground'] < 30:
        print("           ^ ground collapsed — too many accent cues in the prompt.")

    crush = float((g < 10).mean() * 100)
    if crush > 2:
        print(f"\ncrushed    {crush:.1f}% of pixels below 10 — pin the close-up's exposure explicitly")

    # audio: paper impacts carry legit low body; a DRONE is what sustains.
    a = subprocess.run(['ffmpeg', '-v', 'error', '-i', args.files[0], '-map', '0:a',
                        '-ac', '1', '-ar', '22050', '-f', 'f32le', '-'],
                       capture_output=True).stdout
    if not a:
        print("\naudio      none (generateAudio was off? this style needs the native SFX bed)")
        return
    x = np.frombuffer(a, dtype=np.float32)
    N = 1024
    fr = np.array([x[i:i+N] * np.hanning(N) for i in range(0, len(x) - N, 512)])
    S = np.abs(np.fft.rfft(fr, axis=1)) + 1e-9
    freqs = np.fft.rfftfreq(N, 1 / 22050)
    band = S[:, (freqs > 40) & (freqs < 90)].sum(axis=1)
    band = band / (band.max() + 1e-9)
    present = float((band > 0.15).mean() * 100)
    runs, cur = [], None
    for i, v in enumerate(band > 0.15):
        if v and cur is None: cur = i
        if not v and cur is not None:
            dd = (i - cur) * 512 / 22050
            if dd > 0.5: runs.append(round(dd, 2))
            cur = None
    print(f"\naudio      low band (40-90Hz) present in {present:.0f}% of frames  "
          f"(reference ~20%; a continuous bed would be >80%)")
    print(f"           sustained low runs >0.5s: {runs if runs else 'none'}  "
          f"(reference: one 1.49s / none)")
    if any(r > 2.0 for r in runs) or present > 60:
        print("           ^ DRONE. Seedance adds this unasked, under the biggest move. Ban the")
        print("             SUSTAIN, not the frequency: 'no sustained tone, no cinematic drone,")
        print("             no continuous hum'.  (NOTE: if this clip is meant to carry a music")
        print("             bed, run QC on the RAW clip BEFORE the mix — the bed reads as a drone.)")
    elif present < 8:
        print("           ^ THIN. Well under the reference's ~20%. Paper impacts are supposed to")
        print("             carry low body — card hitting card has weight. Ask for 'heavy card")
        print("             dropped flat' rather than banning low bass.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['frame', 'video'])
    p.add_argument('files', nargs='+')
    for k, v in REF.items():
        p.add_argument(f'--{k}', default=v)
    a = p.parse_args()
    pal = {'ground': hexrgb(a.ground), 'accent': hexrgb(a.accent), 'void': hexrgb(a.void)}
    (cmd_frame if a.mode == 'frame' else cmd_video)(a, pal)


if __name__ == '__main__':
    main()
