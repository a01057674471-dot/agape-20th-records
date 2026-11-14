"""YouTube film (16:9, 1920x1080): the planting of 아가페교회, chapters 둘·셋·넷 -- warm coloured-pencil scenes with
slow drift and soft dissolves, the story told in captions at a calm reading pace (no narration), chapter cards,
section labels, the 1130 vision and the 18억 figures popping in. BGM mixed by mix_bgm.sh.
python3 compose.py out.mp4 [--preview | --frames t1,t2]"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from story import STORY

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, 'art')
W, H, FPS = 1920, 1080, 24
BODY = lambda s: ImageFont.truetype(os.path.join(HERE, 'fonts', 'GowunDodum.ttf'), s)
HEAD = lambda s: ImageFont.truetype(os.path.join(HERE, 'fonts', 'Jua.ttf'), s)
BROWN = (78, 52, 38); CREAM = (255, 250, 238); WARM = (196, 110, 60); BLUE = (70, 110, 180)


def smooth(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def wrap(text, font, maxw, d):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    if len(lines) == 2:                                   # balance two lines: split at the space nearest the middle
        best = None
        for i in range(1, len(words)):
            a_, b_ = ' '.join(words[:i]), ' '.join(words[i:])
            wmax = max(d.textlength(a_, font=font), d.textlength(b_, font=font))
            if wmax <= maxw and (best is None or wmax < best[0]): best = (wmax, [a_, b_])
        if best: lines = best[1]
    return lines


def cap_layer(text):
    im = layer(); d = ImageDraw.Draw(im); f = BODY(46); lh = 66
    lines = wrap(text, f, 1500, d)
    quote = text[:1] in '"\'“‘'
    bw = max(d.textlength(l, font=f) for l in lines) + 100
    y1 = 1020; y0 = y1 - lh * len(lines) - 44
    d.rounded_rectangle((W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 28, fill=(255, 250, 238, 236))
    for k, l in enumerate(lines):
        d.text((W / 2, y0 + 22 + lh * k + lh / 2), l, font=f, fill=WARM if quote else BROWN, anchor='mm')
    return im


def sec_layer(text):
    im = layer(); d = ImageDraw.Draw(im); f = HEAD(40)
    w = d.textlength(text, font=f) + 80
    d.rounded_rectangle((60, 50, 60 + w, 126), 38, fill=(255, 250, 238, 236), outline=WARM + (255,), width=4)
    d.text((100, 88), text, font=f, fill=BROWN, anchor='lm')
    return im


def card_layer(main, sub, big=96):
    im = layer(); d = ImageDraw.Draw(im)
    fm = HEAD(big)
    while d.textlength(main, font=fm) > 1640: big -= 4; fm = HEAD(big)
    d.text((W / 2 + 4, 470 + 5), main, font=fm, fill=(120, 80, 40, 70), anchor='mm')
    d.text((W / 2, 470), main, font=fm, fill=BROWN, anchor='mm', stroke_width=8, stroke_fill=CREAM)
    if sub:
        fs = HEAD(54)
        d.text((W / 2, 610), sub, font=fs, fill=WARM, anchor='mm', stroke_width=7, stroke_fill=CREAM)
    return im


def pop_layer(kind):
    """(image, list of (sub-image, cx, cy, delay))"""
    def num(n, unit, label, col, size=150):
        im = Image.new('RGBA', (560, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        fn, fu = HEAD(size), HEAD(int(size * 0.42))
        tw = d.textlength(n, font=fn) + 8 + d.textlength(unit, font=fu); x0 = 280 - tw / 2
        d.ellipse((280 - tw / 2 - 60, 60, 280 + tw / 2 + 60, 300), fill=CREAM + (225,))
        kw = dict(stroke_width=8, stroke_fill=CREAM)
        d.text((x0, 200), n, font=fn, fill=col, anchor='ls', **kw)
        d.text((x0 + d.textlength(n, font=fn) + 8, 200), unit, font=fu, fill=col, anchor='ls', **kw)
        d.text((280, 250), label, font=BODY(38), fill=BROWN, anchor='mm', **kw)
        return im
    if kind == '1130':
        return [(num('1,000', '명', '참된 예배자(셀리더)', WARM, 120), 420, 260, 0.0), (num('100', '개', '열방에 세울 교회', BLUE, 130), 960, 260, 0.9),
                (num('30', '명', '파송할 선교사', (90, 140, 80), 140), 1500, 260, 1.8)]
    if kind == '18':
        return [(num('18', '억 원', '성전 건축 예산', WARM, 170), 960, 280, 0.0)]
    if kind == '7000':
        return [(num('7,000', '만 원', '당시 연간 재정', BLUE, 130), 960, 280, 0.0)]


def view(im, z, cx, cy):
    if abs(z - 1) < 1e-4: return im.copy()
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


def capdur(t): return min(max(2.0 + len(t) / 7.0, 3.6, ), 8.0)


def timeline():
    """turn STORY into timed events"""
    t = 0.0; scenes = []; caps = []; secs = []; cards = []; pops = []; pend = None
    for it in STORY:
        kind = it[0]
        if kind == 'scene':
            scenes.append([t, None, it[1]])
        elif kind == 'title' or kind == 'ch':
            d_ = 5.5 if kind == 'title' else 5.0
            cards.append((t, t + d_, card_layer(it[1], it[2], 104 if kind == 'title' else 78), kind))
            t += d_
        elif kind == 'sec':
            secs.append([t, t + 6.0, sec_layer(it[1])])
        elif kind == 'pop':
            pend = it[1]
        elif kind == 'cap':
            d_ = capdur(it[1])
            if pend:
                pops.append((t, t + d_ + (2.5 if pend == '1130' else 0.6), pop_layer(pend))); pend = None
            caps.append((t + 0.15, t + d_ - 0.15, cap_layer(it[1])))
            t += d_
    t += 1.5
    for i, s in enumerate(scenes): s[1] = scenes[i + 1][0] if i + 1 < len(scenes) else t
    return scenes, caps, secs, cards, pops, t


def main():
    out = sys.argv[1]; preview = '--preview' in sys.argv; only = None
    if '--frames' in sys.argv:
        only = {int(float(x) * FPS) for x in sys.argv[sys.argv.index('--frames') + 1].split(',')}; preview = True
    scenes, caps, secs, cards, pops, TOTAL = timeline()
    print('total', round(TOTAL, 1), 's  scenes', len(scenes), ' captions', len(caps))
    imgs = {n: Image.open(os.path.join(ART, n + '.jpg')).convert('RGB') for n in set(s[2] for s in scenes)}
    XF = 0.9

    def pic(i, t):
        t0, t1, n = scenes[i]
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        drift = [(0.5, 0.45), (0.45, 0.5), (0.55, 0.5), (0.5, 0.55)][i % 4]
        return view(imgs[n], 1.0 + 0.05 * u, *drift)

    nfr = int(TOTAL * FPS)
    if preview: os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    proc = None if preview else subprocess.Popen(cmd, stdin=subprocess.PIPE)

    def fade(lay, a, e, t, fin=0.4, fout=0.4):
        al = min((t - a) / fin, (e - t) / fout, 1.0)
        if al >= 1: return lay
        c = lay.copy(); c.putalpha(Image.eval(lay.getchannel('A'), lambda v: int(v * max(al, 0)))); return c

    for fi in range(nfr):
        t = fi / FPS
        if only is not None:
            if fi not in only: continue
        elif preview and fi % (FPS * 2): continue
        i = max(k for k, s in enumerate(scenes) if s[0] <= t + 1e-6)
        im = pic(i, t)
        if i > 0 and t - scenes[i][0] < XF:
            im = Image.blend(pic(i - 1, t), im, smooth((t - scenes[i][0]) / XF))
        im = im.convert('RGBA')
        for (a, e, lay, kind) in cards:
            if a <= t < e:
                u = min((t - a) / 0.8, (e - t) / 0.8, 1.0)
                veil = Image.new('RGBA', (W, H), (255, 248, 232, int(200 * smooth(u)) if kind == 'ch' else int(150 * smooth(u))))
                im.alpha_composite(veil); im.alpha_composite(fade(lay, a, e, t, 0.8, 0.8))
        for (a, e, lay) in secs:
            if a <= t < e: im.alpha_composite(fade(lay, a, e, t))
        for (a, e, items) in pops:
            if not (a <= t < e): continue
            for (pim, cx, cy, dl) in items:
                tt = t - a - dl
                if tt < 0: continue
                s = 0.55 + 0.6 * smooth(tt / 0.3) - 0.15 * smooth((tt - 0.3) / 0.25)
                al = min(1.0, tt / 0.15, (e - t) / 0.4)
                pi = pim.resize((max(1, int(pim.size[0] * s)), max(1, int(pim.size[1] * s))), Image.BICUBIC)
                if al < 1: pi = Image.fromarray((np.asarray(pi) * np.array([1, 1, 1, al])).astype(np.uint8), 'RGBA')
                im.alpha_composite(pi, (int(cx - pi.size[0] / 2), int(cy - pi.size[1] / 2)))
        for (a, e, lay) in caps:
            if a <= t < e: im.alpha_composite(fade(lay, a, e, t, 0.35, 0.3))
        rgb = im.convert('RGB')
        if only is not None: rgb.save(os.path.join(HERE, 'preview', f'full_{fi:05d}.jpg'), quality=88)
        elif preview: rgb.resize((480, 270)).save(os.path.join(HERE, 'preview', f'{fi:05d}.jpg'), quality=80)
        else: proc.stdin.write(rgb.tobytes())
    if proc: proc.stdin.close(); proc.wait()
    print('done', out, round(TOTAL, 1))


if __name__ == '__main__':
    main()
