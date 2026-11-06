"""Edit the blue picture-book shots into a 9:16 short for 「その十字架、本当の意味を知っていますか？」, timed to the
recorded narration (audio/align.json from align.py). Calm: one shot per line or two, a slow 2-3% drift, soft
dissolves. No music or sound effects -- the narration only.
python3 compose.py out.mp4 [--preview]
"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from script import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
W, H, FPS = 1080, 1920, 30
F = lambda w, s: ImageFont.truetype(os.path.join(HERE, 'fonts', f'ZenMaruGothic-{w}.ttf'), s)
INK = (29, 52, 80)            # navy ink
CREAM = (251, 250, 245)
CORAL = (232, 87, 74)
END_HOLD = 4.5

# shots: (first line, last line, image, zoom0, zoom1, (cx0, cy0), (cx1, cy1))
SHOTS = [
    (0, 1, 'a', 1.00, 1.03, (0.5, 0.42), (0.5, 0.38)),
    (2, 2, 'b1', 1.00, 1.02, (0.5, 0.5), (0.5, 0.5)),
    (2, 2, 'b2', 1.00, 1.02, (0.5, 0.45), (0.5, 0.45)),
    (3, 4, 'c', 1.00, 1.03, (0.5, 0.5), (0.5, 0.46)),
    (5, 6, 'd', 1.00, 1.02, (0.5, 0.5), (0.52, 0.5)),
    (7, 7, 'e', 1.00, 1.02, (0.5, 0.6), (0.5, 0.6)),
    (8, 8, 'f', 1.00, 1.03, (0.5, 0.5), (0.5, 0.45)),
    (9, 10, 'g', 1.00, 1.02, (0.5, 0.55), (0.5, 0.55)),
    (11, 11, 'h', 1.00, 1.03, (0.5, 0.55), (0.48, 0.55)),
    (12, 13, 'i', 1.00, 1.03, (0.5, 0.5), (0.5, 0.45)),
    (14, 15, 'j', 1.00, 1.02, (0.5, 0.5), (0.5, 0.5)),
    (16, 17, 'k', 1.00, 1.03, (0.5, 0.5), (0.5, 0.45)),
]
RECREATION = {'c', 'f', 'h'}           # 聖書に基づく再現
# big captions: (first line, last line, text, y)
CAPTIONS = [
    (0, 1, 'この印、\n本当の意味 知ってる？', 110),
    (3, 4, 'もともとは\n「処刑の道具」', 300),
    (5, 6, 'なぜ、それを飾るの？', 300),
    (9, 10, '私たちの代わりに', 300),
    (11, 11, '三日後、よみがえった', 300),
    (12, 13, '死の印 → 愛の印', 300),
    (16, 17, 'それが、愛のかたち', 770),
]
CHIPS = [(4, 4, '約2,000年前')]
TERMS = [(9, 10, '罪', '神に背を向けること')]
SUBS = {6: ['では、なぜそれを、教会や結婚式に', '飾るのでしょう。'], 4: ['2,000年前、重い罪人を', '死なせるためのものです。'],
        8: ['罪のないイエスが、', 'この十字架で死にました。'], 11: ['そして三日後、', 'イエスはよみがえりました。'],
        13: ['「死の印」から「愛の印」に', '変わったのです。']}


def rounded(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def sub_layer(i):
    lines = SUBS.get(i, [LINES[i]])
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 54); lh = 76
    bw = max(d.textlength(l, font=f) for l in lines) + 80
    y1 = 1600; y0 = y1 - lh * len(lines) - 40
    rounded(d, (W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 32, (251, 250, 245, 236))
    for k, l in enumerate(lines):
        d.text((W / 2, y0 + 20 + lh * k + lh / 2), l, font=f, fill=INK, anchor='mm')
    return im


def caption_layer(text, y):
    im = layer(); d = ImageDraw.Draw(im)
    lines = text.split('\n')
    f = F(900, 88 if max(len(l) for l in lines) <= 9 else 76)
    lh = f.size * 1.35
    bw = max(d.textlength(l, font=f) for l in lines) + 100
    y0 = y - 30; y1 = y0 + lh * len(lines) + 50
    rounded(d, (W / 2 - bw / 2 + 8, y0 + 10, W / 2 + bw / 2 + 8, y1 + 10), 40, (29, 52, 80, 60))
    rounded(d, (W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 40, (251, 250, 245, 246))
    for k, l in enumerate(lines):
        if '「' in l or '→' in l:
            # the key words in coral: inside 「」, and everything after →
            x = W / 2 - d.textlength(l, font=f) / 2
            coral = False
            for ch in l:
                if ch == '「': coral = True
                d.text((x, y0 + 25 + lh * k + lh / 2), ch, font=f, fill=CORAL if coral or ch == '→' else INK, anchor='lm')
                if ch == '」': coral = False
                if ch == '→': coral = True
                x += d.textlength(ch, font=f)
        else:
            d.text((W / 2, y0 + 25 + lh * k + lh / 2), l, font=f, fill=INK, anchor='mm')
    return im


def tag_layer():
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 32)
    t = '聖書に基づく再現'; w = d.textlength(t, font=f) + 44
    rounded(d, (64, 96, 64 + w, 154), 29, (29, 52, 80, 200))
    d.text((64 + w / 2, 125), t, font=f, fill=CREAM, anchor='mm')
    return im


def chip_layer(text):
    im = layer(); d = ImageDraw.Draw(im); f = F(900, 60)
    w = d.textlength(text, font=f) + 80
    rounded(d, (W / 2 - w / 2, 1300, W / 2 + w / 2, 1410), 55, CORAL + (240,))
    d.text((W / 2, 1355), text, font=f, fill=CREAM, anchor='mm')
    return im


def term_layer(word, meaning):
    im = layer(); d = ImageDraw.Draw(im)
    f1, f2 = F(900, 54), F(700, 40)
    w = d.textlength(word, font=f1) + d.textlength(meaning, font=f2) + 140
    x0, y0 = W / 2 - w / 2, 1270
    rounded(d, (x0, y0, x0 + w, y0 + 110), 55, (251, 250, 245, 246), outline=CORAL + (255,), width=5)
    d.text((x0 + 50, y0 + 55), word, font=f1, fill=CORAL, anchor='lm')
    d.text((x0 + 60 + d.textlength(word, font=f1) + 10, y0 + 55), '＝ ' + meaning, font=f2, fill=INK, anchor='lm')
    return im


def end_layer():
    im = layer(); d = ImageDraw.Draw(im)
    rounded(d, (90, 330, 990, 1010), 50, (251, 250, 245, 246))
    d.text((540, 450), 'もっと知りたい人は', font=F(700, 54), fill=INK, anchor='mm')
    d.text((540, 580), '聖書の', font=F(700, 50), fill=INK, anchor='mm')
    d.text((540, 710), '「マルコによる福音書」', font=F(900, 74), fill=CORAL, anchor='mm')
    d.text((540, 860), '15〜16章へ', font=F(900, 66), fill=INK, anchor='mm')
    return im


def smooth(t): t = min(max(t, 0.0), 1.0); return t * t * (3 - 2 * t)


def view(im, z, cx, cy):
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch / 2, 0), H - ch)
    if abs(z - 1) < 1e-4 and x0 == 0 and y0 == 0: return im.copy()
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


def main():
    out = sys.argv[1]; preview = '--preview' in sys.argv
    al = json.load(open(os.path.join(HERE, 'audio', 'align.json')))
    segs = al['segs']
    seg0 = [0.0] + [s[1] for s in segs]                 # line i runs seg0[i] .. seg0[i+1]
    seg0[-1] = al['total']
    total = al['total'] + END_HOLD
    # shot timeline: shots sharing a line split it evenly
    tl = []
    for k, (a, e, img, z0, z1, c0, c1) in enumerate(SHOTS):
        t0, t1 = seg0[a], seg0[e + 1]
        same = [s for s in SHOTS if s[0] == a and s[1] == e]
        if len(same) > 1:
            j = same.index(SHOTS[k]); n = len(same)
            t0, t1 = t0 + (t1 - t0) * j / n, t0 + (t1 - t0) * (j + 1) / n
        tl.append(dict(t0=t0, t1=t1, img=img, z0=z0, z1=z1, c0=c0, c1=c1))
    tl.append(dict(t0=seg0[-1], t1=total, img='l', z0=1.0, z1=1.02, c0=(0.5, 0.5), c1=(0.5, 0.5), end=True))
    imgs = {s['img']: Image.open(f'{OUT}/{s["img"]}.jpg').convert('RGB') for s in tl}
    subs = {i: sub_layer(i) for i in range(len(LINES))}
    caps = [(seg0[a], seg0[e + 1], caption_layer(t, y)) for a, e, t, y in CAPTIONS]
    chips = [(seg0[a], seg0[e + 1], chip_layer(t)) for a, e, t in CHIPS]
    terms = [(seg0[a], seg0[e + 1], term_layer(w_, m)) for a, e, w_, m in TERMS]
    tag, endl = tag_layer(), end_layer()

    def fade(im, a):
        if a >= 1: return im
        c = im.copy(); c.putalpha(Image.eval(im.getchannel('A'), lambda v: int(v * a))); return c

    def picture(s, t):
        u = smooth((t - s['t0']) / max(s['t1'] - s['t0'], 1e-3))
        z = s['z0'] + (s['z1'] - s['z0']) * u
        cx = s['c0'][0] + (s['c1'][0] - s['c0'][0]) * u; cy = s['c0'][1] + (s['c1'][1] - s['c0'][1]) * u
        return view(imgs[s['img']], z, cx, cy)

    XF = 0.35                                            # cross-dissolve length (s)
    nfr = int(total * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', os.path.join(HERE, 'audio', 'narration.mp3'), '-filter_complex', '[1:a]apad[a]', '-map', '0:v', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
           '-shortest', '-movflags', '+faststart', out]
    proc = None if preview else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    if preview: os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
    for fi in range(nfr):
        t = fi / FPS
        if preview and fi % 15: continue
        k = max(i for i, s in enumerate(tl) if s['t0'] <= t + 1e-6)
        s = tl[k]
        im = picture(s, t)
        if k > 0 and t - s['t0'] < XF:                   # dissolve from the previous shot
            im = Image.blend(picture(tl[k - 1], t), im, smooth((t - s['t0']) / XF))
        base = im.convert('RGBA')
        if s['img'] in RECREATION: base.alpha_composite(tag)
        for (a, e, L) in caps + chips + terms:
            if a <= t < e:
                base.alpha_composite(fade(L, min((t - a) / 0.25, (e - t) / 0.2, 1)))
        if s.get('end'):
            base.alpha_composite(fade(endl, smooth((t - s['t0'] - 0.2) / 0.6)))
        else:
            i = max(i for i in range(len(LINES)) if seg0[i] <= t + 1e-6) if t < seg0[-1] else None
            if i is not None: base.alpha_composite(subs[i])
        rgb = base.convert('RGB')
        if preview: rgb.resize((360, 640)).save(os.path.join(HERE, 'preview', f'{fi:05d}.jpg'), quality=80)
        else: proc.stdin.write(rgb.tobytes())
    if proc: proc.stdin.close(); proc.wait()
    print('done', out, f'{total:.1f}s')


if __name__ == '__main__':
    main()
