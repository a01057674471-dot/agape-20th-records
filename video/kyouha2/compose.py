"""Edit 「カトリックとプロテスタント、なにがちがう?」【ちがい編】 (9:16): warm coloured-pencil shots and comparison cards --
what both share, then priest / pastor, 73 / 66 books, and what each relies on most -- timed to the narration
(audio/align.json); a summary table to end. Subtitles above the Reels UI.  python3 compose.py out.mp4 [--preview | --frames t1,t2]
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
LEAD, END_HOLD = 0.0, 4.5


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


SPLIT = {2: ['どちらも、父・子・聖霊の、', 'ひとりの神様を信じています。'],
         3: ['イエス・キリストが、十字架で死に、', 'よみがえったことも、同じです。'],
         5: ['ひとつめ。', '教会の先生の呼び方。'],
         6: ['カトリックは"神父"。', '結婚しません。'],
         7: ['プロテスタントは"牧師"。', '結婚することができます。'],
         10: ['カトリックは、それに7冊を加えた、', '73冊です。'],
         12: ['いちばん大きなちがいは、', '"何を、いちばんの', 'よりどころにするか"。'],
         13: ['カトリックは、聖書とともに、', '教会の伝統と、'],
         14: ['ローマ教皇を中心とした教えを、', '大切にします。'],
         15: ['プロテスタントは、"聖書だけ"を、', 'いちばんのよりどころにします。'],
         16: ['そして、イエス・キリストこそ、', '神様と人とのあいだの、', 'ただひとりの仲介者。'],
         17: ['だから、だれでも、イエスを通して、', '直接、神様に祈れると考えます。'],
         18: ['ちなみに、日本では、カトリックと', 'プロテスタントが、いっしょに訳した', '聖書も、使われています。'],
         19: ['どの教会に行くかより、', 'まず大切なのは…'],
         20: ['"イエス・キリストが、だれなのか"を、', '知ることなんです。']}

CATH = (112, 92, 150)
PROT_ = WARM
LX, RX = 280, 800


def fade(t, t0, d=0.4): return smooth((t - t0) / d)


def pill(d, x, y, text, size=40, col=BROWN, edge=None, a=255):
    f = F(900, size); w = d.textlength(text, font=f) + 44
    x = min(max(x, w / 2 + 20), W - w / 2 - 20)
    d.rounded_rectangle((x - w / 2, y - size * 0.8, x + w / 2, y + size * 0.8), int(size * 0.8), fill=CREAM + (int(240 * a / 255),),
                        outline=(edge + (a,)) if edge else None, width=4)
    d.text((x, y), text, font=f, fill=col + (a,), anchor='mm')




def card(d, x, y0, y1, w, head, col, a=255):
    d.rounded_rectangle((x - w / 2, y0, x + w / 2, y1), 36, fill=CREAM + (int(242 * a / 255),), outline=col + (a,), width=5)
    d.rounded_rectangle((x - w / 2, y0, x + w / 2, y0 + 90), 36, fill=col + (a,))
    d.rectangle((x - w / 2, y0 + 50, x + w / 2, y0 + 90), fill=col + (a,))
    d.text((x, y0 + 46), head, font=F(900, 46), fill=(255, 250, 240, a), anchor='mm')


def common_layer(t, T):
    im = layer(); d = ImageDraw.Draw(im)
    m = smooth((t - T['merge']) / 0.9) * (1 - smooth((t - T['apart']) / 0.8))
    a0 = int(255 * fade(t, T['start']))
    for x0, head, col in ((LX, 'カトリック', CATH), (RX, 'プロテスタント', PROT_)):
        x = x0 + (540 - x0) * m
        card(d, x, 420 if x0 == LX else 440, 1080, 460, head, col, int(a0 * (1 - 0.35 * m)))
    if m > 0.6:
        a = int(255 * min(1, (m - 0.6) / 0.4))
        x0_, y0_ = 540 - 230, 440
        d.rounded_rectangle((x0_, y0_, x0_ + 460, y0_ + 90), 36, fill=CATH + (a,)); d.rectangle((x0_, y0_ + 50, x0_ + 460, y0_ + 90), fill=CATH + (a,))
        d.rounded_rectangle((540, y0_, x0_ + 460, y0_ + 90), 36, fill=PROT_ + (a,)); d.rectangle((540, y0_, x0_ + 400, y0_ + 90), fill=PROT_ + (a,))
        d.rectangle((540, y0_ + 50, x0_ + 460, y0_ + 90), fill=PROT_ + (a,))
        d.text((425, y0_ + 46), 'カトリック', font=F(900, 34), fill=(255, 250, 240, a), anchor='mm')
        d.text((655, y0_ + 46), 'プロテスタント', font=F(900, 30), fill=(255, 250, 240, a), anchor='mm')
        d.text((540, 600), '同じところ', font=F(900, 54), fill=BROWN + (a,), anchor='mm')
        for key, y, txt in (('c1', 760, '父・子・聖霊の、'), ('c1', 830, 'ひとりの神様'), ('c2', 960, '十字架と'), ('c2', 1025, 'よみがえり')):
            b_ = fade(t, T[key])
            if b_ > 0: d.text((540, y), txt, font=F(900, 48), fill=WARM + (int(a * b_),), anchor='mm')
    q = fade(t, T['apart'] + 0.3, 0.5)
    if q > 0: d.text((540, 760), '？', font=F(900, 200), fill=WARM + (int(255 * q),), anchor='mm', stroke_width=10, stroke_fill=CREAM)
    return im


def priest_layer(t, T):
    im = layer(); d = ImageDraw.Draw(im)
    a = fade(t, T['p0'])
    if a > 0: pill(d, 540, 180, '①　教会の先生', 48, col=WARM, edge=WARM, a=int(255 * a))
    for key, x, head, col, sub in (('p1', LX, '神父', CATH, '結婚しない'), ('p2', RX, '牧師', PROT_, '結婚できる')):
        b_ = fade(t, T[key])
        if b_ <= 0: continue
        A = int(255 * b_)
        d.rounded_rectangle((x - 200, 260, x + 200, 500), 36, fill=CREAM + (int(240 * b_),), outline=col + (A,), width=5)
        d.text((x, 290), 'カトリック' if x == LX else 'プロテスタント', font=F(700, 30), fill=col + (A,), anchor='mm')
        d.text((x, 370), head, font=F(900, 84), fill=BROWN + (A,), anchor='mm')
        d.text((x, 455), sub, font=F(900, 38), fill=col + (A,), anchor='mm')
    return im


def books_layer(t, T):
    im = layer(); d = ImageDraw.Draw(im)
    a = fade(t, T['b0'])
    if a > 0: pill(d, 540, 250, '②　聖書', 52, col=WARM, edge=WARM, a=int(255 * a))
    rng = np.random.default_rng(4)
    tones = [(150, 90, 70), (120, 100, 80), (170, 120, 80), (110, 80, 70), (140, 110, 90)]
    for key, x0, n, head, col in (('b2', LX, 73, 'カトリック', CATH), ('b1', RX, 66, 'プロテスタント', PROT_)):
        st = T[key]
        if t < st - 0.3: continue
        ha = fade(t, st - 0.3)
        pill(d, x0, 360, head, 40, col=col, a=int(255 * ha))
        for i in range(n):
            u = fade(t, st + i * 0.018, 0.2)
            if u <= 0: break
            r, c = divmod(i, 11)
            x = x0 - 209 + c * 38; y = 460 + r * 95
            extra = i >= 66
            fill = (226, 170, 60) if extra else tones[i % 5]
            h_ = 80 - (i * 7 % 11)
            d.rounded_rectangle((x, y + 80 - h_ * u, x + 32, y + 80), 5, fill=fill + (255,))
            d.line((x + 4, y + 80 - h_ * u + 12, x + 28, y + 80 - h_ * u + 12), fill=(250, 235, 200, 200), width=3)
        for r in range(7 if n == 73 else 6):
            if t >= st + r * 11 * 0.018: d.line((x0 - 220, 460 + r * 95 + 82, x0 + 220, 460 + r * 95 + 82), fill=(140, 100, 70, 230), width=5)
        na = fade(t, st + n * 0.018, 0.4)
        if na > 0:
            d.text((x0, 1150), f'{n}冊', font=F(900, 80), fill=col + (int(255 * na),), anchor='mm', stroke_width=7, stroke_fill=CREAM)
    ea = fade(t, T['b2'] + 73 * 0.018 + 0.2)
    if ea > 0: d.text((LX, 1085 - 95 * 0 - 30), '＋7冊', font=F(900, 36), fill=(200, 140, 30, int(255 * ea)), anchor='mm')
    return im


def basis_layer(t, T):
    im = layer(); d = ImageDraw.Draw(im)
    a = fade(t, T['r0'])
    if a > 0: pill(d, 540, 250, '③　いちばんのよりどころ', 46, col=WARM, edge=WARM, a=int(255 * a))
    ca = fade(t, T['r0'] + 0.3)
    if ca > 0:
        card(d, LX, 360, 1110, 470, 'カトリック', CATH, int(255 * ca))
        card(d, RX, 360, 1110, 470, 'プロテスタント', PROT_, int(255 * ca))
    for key, y, txt, sz in (('r1', 560, '聖書', 64), ('r2', 690, '＋　教会の伝統', 46), ('r3', 820, '＋　教導権', 46), ('r3', 880, '（ローマ教皇を中心とした教え）', 26)):
        b_ = fade(t, T[key])
        if b_ > 0: d.text((LX, y), txt, font=F(900, sz), fill=BROWN + (int(255 * b_),), anchor='mm')
    b_ = fade(t, T['r4'], 0.6)
    if b_ > 0:
        g = layer(); ImageDraw.Draw(g).ellipse((RX - 190, 560, RX + 190, 860), fill=(255, 214, 120, int(170 * b_)))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
        d = ImageDraw.Draw(im)
        d.text((RX, 700), '聖書だけ', font=F(900, 76), fill=WARM + (int(255 * b_),), anchor='mm', stroke_width=7, stroke_fill=CREAM)
    return im


ROWS = [('教会の先生', '神父', '（結婚しない）', '牧師', '（結婚できる）'),
        ('聖書', '73冊', '', '66冊', ''),
        ('よりどころ', '聖書＋伝統', '＋教導権', '聖書だけ', ''),
        ('秘跡・礼典', '7つ', '', '2つ', '（洗礼・聖餐）')]


def summary_layer(t, t0):
    im = layer(); d = ImageDraw.Draw(im)
    A = fade(t, t0, 0.6)
    if A <= 0: return im
    a = int(255 * A)
    x0, x1, x2, x3 = 50, 270, 650, 1030
    y = 520
    d.rounded_rectangle((x0, y, x3, y + 100 + 150 * len(ROWS)), 30, fill=CREAM + (int(245 * A),), outline=(150, 110, 80, a), width=4)
    d.rectangle((x1, y + 6, x2, y + 100), fill=CATH + (a,)); d.rounded_rectangle((x2, y + 6, x3 - 6, y + 100), 24, fill=PROT_ + (a,))
    d.rectangle((x2, y + 6, x3 - 30, y + 100), fill=PROT_ + (a,))
    d.text(((x1 + x2) / 2, y + 52), 'カトリック', font=F(900, 42), fill=(255, 250, 240, a), anchor='mm')
    d.text(((x2 + x3) / 2, y + 52), 'プロテスタント', font=F(900, 42), fill=(255, 250, 240, a), anchor='mm')
    for k, (lab, c1, c1s, c2, c2s) in enumerate(ROWS):
        yy = y + 100 + 150 * k
        d.line((x0 + 10, yy, x3 - 10, yy), fill=(190, 160, 130, a), width=3)
        d.text(((x0 + x1) / 2, yy + 75), lab, font=F(900, 32), fill=BROWN + (a,), anchor='mm')
        for (cx, main, sub, col) in (((x1 + x2) / 2, c1, c1s, CATH), ((x2 + x3) / 2, c2, c2s, PROT_)):
            d.text((cx, yy + (58 if sub else 75)), main, font=F(900, 46), fill=col + (a,), anchor='mm')
            if sub: d.text((cx, yy + 112), sub, font=F(700, 28), fill=BROWN + (a,), anchor='mm')
    d.line((x1, y + 100, x1, y + 100 + 150 * len(ROWS)), fill=(190, 160, 130, a), width=3)
    d.line((x2, y + 100, x2, y + 100 + 150 * len(ROWS)), fill=(190, 160, 130, a), width=3)
    return im

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
        (0.0, L(2), 'one_hill', 1.0, 1.05, 0.5, 0.5),           # まずは、同じところから
        (L(2), L(5), 'common', 1.0, 1.0, 0.5, 0.5),             # 父・子・聖霊 / 十字架と復活 / では、ちがいは?
        (L(5), L(8), 'priest_pastor', 1.0, 1.03, 0.5, 0.5),     # ① 神父 / 牧師
        (L(8), L(11), 'books', 1.0, 1.0, 0.5, 0.5),             # ② 66冊 / 73冊
        (L(11), L(16), 'basis', 1.0, 1.0, 0.5, 0.5),            # ③ よりどころ
        (L(16), L(18), 'window', 1.0, 1.05, 0.5, 0.5),          # ただひとりの仲介者 / 直接、神様に祈れる (1テモテ2:5)
        (L(18), L(19), 'tea', 1.0, 1.05, 0.5, 0.55),            # いっしょに訳した聖書
        (L(19), seg0[-1], 'teach', 1.0, 1.05, 0.5, 0.5),        # イエス・キリストが、だれなのか
        (seg0[-1], TOTAL, 'summary', 1.0, 1.0, 0.5, 0.5),       # まとめの表
    ]
    FILE = {'common': 'paper_bg', 'books': 'paper_bg', 'basis': 'paper_bg', 'summary': 'paper_bg'}
    TT = dict(start=L(2) - 0.3, merge=L(2) + 0.1, c1=a(4.64), c2=a(9.34), apart=L(4),
              p0=L(5), p1=a(18.06), p2=a(20.94), b0=L(8), b1=a(25.96), b2=a(29.72),
              r0=L(11), r1=a(37.44), r2=a(38.62), r3=a(40.0), r4=a(44.48))
    imgs = {n: Image.open(os.path.join(ART, FILE.get(n, n) + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    POPS = []
    caps = [(0.05, L(2), caption(['カトリックとプロテスタント、', 'なにがちがう？'], 290, 70, accent=(1,))),
            (0.05, L(2), chip(['【ちがい編】'], 520)),
            (L(16), L(18), verse(['神と人との間の仲介者も唯一であり、', 'それは人としてのキリスト・イエスです。'], '1テモテ2:5より', 170)),
            (L(18), L(19), chip(['『聖書協会共同訳』（2018年）', 'カトリックとプロテスタントが共同で翻訳'], 260)),
            (seg0[-1], TOTAL, caption(['もっと知りたいことがあれば、', 'コメントでどうぞ。'], 290, 64, accent=(1,)))]

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        src = imgs[n]
        LAY = {'common': common_layer, 'priest_pastor': priest_layer, 'books': books_layer, 'basis': basis_layer}
        if n in LAY:
            src = src.convert('RGBA'); src.alpha_composite(LAY[n](t, TT)); src = src.convert('RGB')
        elif n == 'summary':
            src = src.convert('RGBA'); src.alpha_composite(summary_layer(t, t0)); src = src.convert('RGB')
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
