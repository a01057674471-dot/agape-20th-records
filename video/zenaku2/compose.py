"""Edit 「善悪の知識の木」【後編】 (9:16): warm coloured-pencil shots timed to the narration (audio/align.json) -- the
whisper; hiding; sin spreading through the generations; the light that comes searching; the promise; the tree and the cross;
Gethsemane; the call. Verses at the top; subtitles above the Reels UI.  python3 compose.py out.mp4 [--preview | --frames t1,t2]
"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from script import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, 'art')
W, H, FPS = 1080, 1920, 30
F = lambda w, s: ImageFont.truetype(os.path.join(HERE, 'fonts', f'ZenMaruGothic-{w}.ttf'), s)
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
BROWN = (92, 58, 40); CREAM = (255, 250, 238); WARM = (196, 110, 60); INKC = (60, 60, 70)
SUB_Y1 = 1420                                            # subtitle box bottom (Reels UI covers below ~1500)
LEAD, END_HOLD = 0.0, 4.0


def smooth(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def sub_layer(lines):
    """the subtitle box; text inside ［ ］ is set small (a reading aside)"""
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 50); fs = F(700, 30); lh = 72
    def parts(l):
        out = []; rest = l
        while '［' in rest:
            a_, b_ = rest.index('［'), rest.index('］')
            out += [(rest[:a_], f), ('（' + rest[a_ + 1:b_] + '）', fs)]; rest = rest[b_ + 1:]
        return out + [(rest, f)]
    widths = [sum(d.textlength(t, font=ff) for t, ff in parts(l)) for l in lines]
    bw = max(widths) + 76
    y1 = SUB_Y1; y0 = y1 - lh * len(lines) - 36
    d.rounded_rectangle((W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 30, fill=CREAM + (232,))
    for k, (l, wd) in enumerate(zip(lines, widths)):
        x = W / 2 - wd / 2; yc = y0 + 18 + lh * k + lh / 2
        for t, ff in parts(l):
            d.text((x, yc + (6 if ff is fs else 0)), t, font=ff, fill=BROWN if ff is f else (150, 110, 80), anchor='lm')
            x += d.textlength(t, font=ff)
    return im


def caption(lines, y, size=66, accent=(), box=False):
    im = layer(); d = ImageDraw.Draw(im); f = F(900, size); lh = size * 1.4
    if box:
        bw = max(d.textlength(l, font=f) for l in lines) + 90
        d.rounded_rectangle((W / 2 - bw / 2, y - lh / 2 - 26, W / 2 + bw / 2, y + lh * (len(lines) - 0.5) + 26), 36, fill=CREAM + (236,))
    for k, l in enumerate(lines):
        col = WARM if k in accent else BROWN
        d.text((W / 2 + 3, y + k * lh + 4), l, font=f, fill=(120, 80, 40, 60), anchor='mm')
        d.text((W / 2, y + k * lh), l, font=f, fill=col, anchor='mm', stroke_width=7, stroke_fill=CREAM)
    return im


def verse(lines, ref, y0=240):
    im = layer(); d = ImageDraw.Draw(im)
    size = 58
    while max(d.textlength(l, font=F(900, size)) for l in lines) > 820: size -= 2
    f = F(900, size); lh = int(size * 1.48)
    h = 190 + lh * len(lines)
    d.rounded_rectangle((90, y0, 990, y0 + h), 44, fill=CREAM + (240,))
    d.text((540, y0 + 60), '聖書のことば', font=F(700, 36), fill=(170, 130, 90), anchor='mm')
    for k, l in enumerate(lines):
        d.text((540, y0 + 130 + k * lh), l, font=f, fill=BROWN, anchor='mm')
    d.text((540, y0 + h - 50), ref, font=F(700, 36), fill=WARM, anchor='mm')
    return im


def ref_chip(text, y=250):
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 40)
    w = d.textlength(text, font=f) + 70
    d.rounded_rectangle((W / 2 - w / 2, y - 36, W / 2 + w / 2, y + 36), 36, fill=CREAM + (235,), outline=WARM + (255,), width=4)
    d.text((W / 2, y), text, font=f, fill=BROWN, anchor='mm')
    return im


def end_layer():
    im = caption(['言葉にできなくても', '大丈夫。'], 330, 70, accent=(1,))
    d = ImageDraw.Draw(im); f = F(700, 48)
    t1, t2 = 'コメントに', 'だけ置いていってね。'
    em = ImageFont.truetype(EMOJI, 109)
    heart = Image.new('RGBA', (140, 140), (0, 0, 0, 0))
    ImageDraw.Draw(heart).text((10, 10), '🤍', font=em, embedded_color=True)
    heart = heart.crop(heart.getbbox()).resize((60, 60), Image.LANCZOS)
    w = d.textlength(t1, font=f) + 70 + d.textlength(t2, font=f)
    x0, y = W / 2 - w / 2, 1460
    d.rounded_rectangle((x0 - 40, y - 56, x0 + w + 40, y + 56), 40, fill=CREAM + (238,))
    d.text((x0, y), t1, font=f, fill=BROWN, anchor='lm')
    im.alpha_composite(heart, (int(x0 + d.textlength(t1, font=f) + 5), int(y - 30)))
    d.text((x0 + d.textlength(t1, font=f) + 70, y), t2, font=f, fill=BROWN, anchor='lm')
    return im


def view(im, z, cx, cy):
    if abs(z - 1) < 1e-4: return im.copy()
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


SPLIT = {1: ['そのささやきに、人は耳を貸し、', 'あの実を、食べてしまいました。'],
         2: ['その日から、人は、', '神様から隠れるようになりました。'],
         5: ['神様から離れて、', '自分が中心になること。'],
         6: ['その罪は、すべての人に、', '広がっていきました。'],
         7: ['でも、神様は、', '隠れた人を、探しに来ます。'],
         10: ['いつか、ひとりのかたが来て、', '罪と死の力を、打ち砕く、と。'],
         11: ['人は、木の実を食べて、', '神様から離れた。'],
         12: ['イエスは、十字架という木にかかって、', '私たちを取り戻してくれた。'],
         13: ['最初の人が、"自分の思い"を', '選んだその場所で…'],
         14: ['イエスは、"わたしの願いではなく、', 'あなたの思いを"と祈り、', '自分から、十字架へ向かいました。'],
         16: ['神様は、いまも、', 'あなたの名前を呼んでいます。']}

BLUE = (70, 110, 180)


def pop_img(num, unit='', label=None, col=WARM, pre='', size=190):
    """a big number with its unit (and a small label under it), on a soft cream disc"""
    im = Image.new('RGBA', (900, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fn, fu, fp = F(900, size), F(900, int(size * 0.42)), F(900, int(size * 0.36))
    wn, wu, wp = d.textlength(num, font=fn), d.textlength(unit, font=fu), d.textlength(pre, font=fp)
    tw = wp + wn + wu; x0 = 450 - tw / 2; base = 250
    d.ellipse((450 - tw / 2 - 70, base - size * 0.78, 450 + tw / 2 + 70, base + size * 0.3 + (60 if label else 0)), fill=CREAM + (225,))
    kw = dict(stroke_width=8, stroke_fill=CREAM)
    if pre: d.text((x0, base), pre, font=fp, fill=BROWN, anchor='ls', **kw)
    d.text((x0 + wp, base), num, font=fn, fill=col, anchor='ls', **kw)
    if unit: d.text((x0 + wp + wn + 6, base), unit, font=fu, fill=col, anchor='ls', **kw)
    if label: d.text((450, base + 62), label, font=F(700, 44), fill=BROWN, anchor='mm', **kw)
    return im


def char_img(ch, size=330):
    im = Image.new('RGBA', (460, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((236, 236), ch, font=F(900, size), fill=(120, 80, 40, 60), anchor='mm')
    d.text((230, 230), ch, font=F(900, size), fill=(40, 34, 40), anchor='mm')
    return im


def word_img(text, col=BROWN, size=70):
    im = Image.new('RGBA', (900, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = d.textlength(text, font=F(900, size))
    d.rounded_rectangle((450 - w / 2 - 36, 150 - size * 0.75, 450 + w / 2 + 36, 150 + size * 0.75), 40, fill=CREAM + (238,), outline=col + (255,), width=5)
    d.text((450, 150), text, font=F(900, size), fill=col, anchor='mm')
    return im


def pop_at(frame, img, cx, cy, t, t0, t1):
    if not (t0 <= t < t1): return
    u = smooth((t - t0) / 0.3)
    s = 0.55 + 0.6 * u - 0.15 * smooth((t - t0 - 0.3) / 0.25)
    a = min(1.0, (t - t0) / 0.15, (t1 - t) / 0.3)
    w_, h_ = img.size
    im = img.resize((max(1, int(w_ * s)), max(1, int(h_ * s))), Image.BICUBIC)
    if a < 1: im = Image.fromarray((np.asarray(im) * np.array([1, 1, 1, a])).astype(np.uint8), 'RGBA')
    frame.alpha_composite(im, (int(cx - im.size[0] / 2), int(cy - im.size[1] / 2)))


def glow_dot(im, x, y, r, amount=1.0):
    """a shining point of gold light"""
    r = float(r); amount = float(amount); s = int(r * 6); g = Image.new('L', (2 * s, 2 * s), 0); d = ImageDraw.Draw(g)
    for k in range(24, 0, -1):
        rr = s * k / 24; v = int(255 * (1 - k / 24) ** 1.6 * amount)
        d.ellipse((s - rr, s - rr, s + rr, s + rr), fill=v)
    col = Image.new('RGBA', (2 * s, 2 * s), (255, 214, 120, 0)); col.putalpha(g)
    im.alpha_composite(col, (int(x - s), int(y - s)))
    core = Image.new('RGBA', (2 * s, 2 * s), (0, 0, 0, 0)); dc = ImageDraw.Draw(core)
    dc.ellipse((s - r, s - r, s + r, s + r), fill=(255, 250, 225, int(255 * amount)))
    im.alpha_composite(core.filter(ImageFilter.GaussianBlur(r * 0.25)), (int(x - s), int(y - s)))


def point_card(num, lines, y0=220):
    """a numbered point: the number in a warm circle, the words beside it"""
    im = layer(); d = ImageDraw.Draw(im)
    size = 54
    while max(d.textlength(l, font=F(900, size)) for l in lines) > 640: size -= 2
    lh = int(size * 1.5); hh = max(200, 60 + lh * len(lines))
    d.rounded_rectangle((70, y0, 1010, y0 + hh), 44, fill=CREAM + (242,))
    cx, cy = 190, y0 + hh / 2
    d.ellipse((cx - 78, cy - 78, cx + 78, cy + 78), fill=WARM + (255,))
    d.text((cx, cy + 4), str(num), font=F(900, 110), fill=CREAM, anchor='mm')
    for k, l in enumerate(lines):
        d.text((630, y0 + hh / 2 + (k - (len(lines) - 1) / 2) * lh), l, font=F(900, size), fill=BROWN, anchor='mm')
    return im


def big_word():
    im = Image.new('RGBA', (1000, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((506, 288), '宗教', font=F(900, 340), fill=(120, 80, 40, 70), anchor='mm')
    d.text((500, 280), '宗教', font=F(900, 340), fill=BROWN, anchor='mm', stroke_width=12, stroke_fill=CREAM)
    return im


def name_card():
    im = caption(['はじめまして。', 'サンヒです。'], 300, 84, accent=(1,))
    return im


def chip(lines, y=1200):
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 44); lh = 62
    bw = max(d.textlength(l, font=f) for l in lines) + 80
    d.rounded_rectangle((W / 2 - bw / 2, y - 40, W / 2 + bw / 2, y - 40 + lh * len(lines) + 30), 34, fill=CREAM + (236,), outline=WARM + (255,), width=4)
    for k, l in enumerate(lines):
        ref = len(lines) > 1 and k == len(lines) - 1
        d.text((W / 2, y - 25 + lh * k + lh / 2), l, font=F(700, 36) if ref else f, fill=WARM if ref else BROWN, anchor='mm')
    return im


def end_card():
    im = caption(['これから、', 'よろしくお願いします。'], 300, 76, accent=(1,))
    d = ImageDraw.Draw(im); f = F(700, 42)
    t = 'AMJ日本アガペ宣教会　サンヒ'
    w = d.textlength(t, font=f) + 80
    d.rounded_rectangle((W / 2 - w / 2, 1420, W / 2 + w / 2, 1510), 40, fill=CREAM + (238,))
    d.text((W / 2, 1465), t, font=f, fill=BROWN, anchor='mm')
    return im


def main():
    out = sys.argv[1]; preview = '--preview' in sys.argv
    only = None
    if '--frames' in sys.argv:
        only = {int(float(x) * FPS) for x in sys.argv[sys.argv.index('--frames') + 1].split(',')}; preview = True
    al = json.load(open(os.path.join(HERE, 'audio', 'align.json')))
    seg0 = [LEAD + s[0] for s in al['segs']] + [LEAD + al['total']]
    seg0[0] = LEAD
    L = lambda i: seg0[i]
    TOTAL = seg0[-1] + END_HOLD
    a = lambda t: LEAD + t                                  # audio time -> video time
    shots = [
        (0.0, L(2), 'serpent', 1.0, 1.05, 0.5, 0.45),           # 神のようになれる / あの実を食べてしまった
        (L(2), L(4), 'hiding', 1.0, 1.05, 0.5, 0.5),            # 神様から隠れる / はずかしさと、こわさ
        (L(4), L(7), 'generations', 1.0, 1.05, 0.5, 0.5),       # 罪 / 自分が中心 / すべての人に
        (L(7), L(9), 'searching', 1.0, 1.06, 0.5, 0.55),        # 探しに来ます / あなたは、どこにいるのか
        (L(9), L(11), 'promise_light', 1.0, 1.06, 0.5, 0.5),    # 約束 / 打ち砕く (創世記3:15)
        (L(11), L(13), 'tree_cross', 1.0, 1.04, 0.5, 0.5),      # 木の実 / 十字架という木
        (L(13), L(15), 'gethsemane', 1.0, 1.06, 0.5, 0.55),     # わたしの願いではなく (ルカ22:42)
        (L(15), L(16), 'cross', 1.0, 1.05, 0.5, 0.5),           # 強制じゃない。愛だから。
        (L(16), TOTAL, 'morning_walk', 1.0, 1.06, 0.5, 0.5),    # あなたの名前を呼んでいます
    ]
    FILE = {}
    imgs = {n: Image.open(os.path.join(ART, FILE.get(n, n) + '.jpg')).convert('RGB') for n in set(s[2] for s in shots) if n != 'tree_cross'}
    tl = Image.open(os.path.join(ART, 'tree_center.jpg')).convert('RGB').crop((270, 0, 810, 1920))
    tr = Image.open(os.path.join(ART, 'cross.jpg')).convert('RGB').crop((270, 0, 810, 1920))
    tc = Image.new('RGB', (W, H)); tc.paste(tl, (0, 0)); tc.paste(tr, (540, 0))
    ImageDraw.Draw(tc).line((540, 0, 540, H), fill=(250, 240, 220), width=8)
    imgs['tree_cross'] = tc
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    POPS = [(word_img('罪', col=WARM, size=110), 540, 400, a(14.16), L(5)),
            (word_img('木の実', col=BROWN, size=60), 270, 900, a(35.16), L(13)),
            (word_img('十字架という木', col=WARM, size=52), 810, 900, a(39.32), L(13))]
    caps = [(0.05, L(2), caption(['隠れた人を、', '探しに来た神様'], 290, 72, accent=(1,))),
            (0.05, L(2), chip(['【後編】善悪の知識の木'], 520)),
            (L(8), L(9), verse(['あなたは、どこにいるのか。'], '創世記3:9より', 200)),
            (L(10), L(11), verse(['彼はおまえの頭を打ち、', 'おまえは彼のかかとを打つ。'], '創世記3:15より', 170)),
            (L(14), L(15), verse(['わたしの願いではなく、', 'みこころがなりますように。'], 'ルカ22:42より', 170)),
            (seg0[-1] - 0.1, TOTAL, caption(['あなたは、いま、', 'どこにいますか？'], 300, 80, accent=(1,)))]

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        src = imgs[n]
        return view(src, z0 + (z1 - z0) * u, cx, cy)
    XF = 0.5
    nfr = int(TOTAL * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', os.path.join(HERE, 'audio', 'narration.mp3'), '-filter_complex', f'[1:a]adelay={int(LEAD * 1000)}:all=1,apad[a]',
           '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]
    proc = None if preview else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    if preview: os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
    for fi in range(nfr):
        t = fi / FPS
        if only is not None:
            if fi not in only: continue
        elif preview and fi % 15: continue
        k = max(i for i, s in enumerate(shots) if s[0] <= t + 1e-6)
        s = shots[k]
        im = pic(s, t)
        xf = XF
        if k > 0 and t - s[0] < xf:
            im = Image.blend(pic(shots[k - 1], t), im, smooth((t - s[0]) / xf))
        im = im.convert('RGBA')
        for (a0, e0, Lr) in caps:
            if a0 <= t < e0:
                al_ = min((t - a0) / 0.4, (e0 - t) / 0.3 if e0 < TOTAL else 1.0, 1.0)
                c = Lr
                if al_ < 1:
                    c = Lr.copy(); c.putalpha(Image.eval(Lr.getchannel('A'), lambda v: int(v * al_)))
                im.alpha_composite(c)
        for (img_, x_, y_, t0_, t1_) in POPS: pop_at(im, img_, x_, y_, t, t0_, t1_)
        if L(0) <= t < seg0[-1]:
            i = max(i for i in range(len(LINES)) if seg0[i] <= t + 1e-6)
            if i in subs: im.alpha_composite(subs[i])
        rgb = im.convert('RGB')
        if only is not None: rgb.save(os.path.join(HERE, 'preview', f'full_{fi:05d}.jpg'), quality=90)
        elif preview: rgb.resize((360, 640)).save(os.path.join(HERE, 'preview', f'{fi:05d}.jpg'), quality=80)
        else: proc.stdin.write(rgb.tobytes())
    if proc: proc.stdin.close(); proc.wait()
    print('done', out, f'{TOTAL:.1f}s')


if __name__ == '__main__':
    main()
