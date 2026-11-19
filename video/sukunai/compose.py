"""Edit 「なぜ日本には、クリスチャンが少ないの?」 (9:16): warm coloured-pencil shots and simple number graphics timed to the
narration (audio/align.json): 200 people with one lit; Japan and Korea side by side; the long ban (1614-1873); the temple
register; the grey umbrellas; the hidden believers; the shepherd who goes after the one. Verses and sources at the top;
subtitles above the Reels UI.  python3 compose.py out.mp4 [--preview | --frames t1,t2]
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


SPLIT = {0: ['日本で、クリスチャンに', '会ったこと、ありますか？'],
         1: ['実は、日本のプロテスタントの', 'クリスチャンは、人口の0.5%にも', '満たないと言われています。'],
         3: ['おとなりの韓国では、クリスチャンは、', '大人のおよそ4人に1人。'],
         7: ['江戸時代、キリスト教は、', '250年以上も禁止されていました。'],
         8: ['信じていると知られれば、', '命さえうばわれた時代です。'],
         10: ['江戸時代、すべての人が', 'お寺に登録するしくみがつくられ、'],
         11: ['宗教は、"自分で選ぶもの"ではなく、', '"家で決まっているもの"に', 'なっていきました。'],
         12: ['みっつめは、', '"みんなと同じ"でいたい気持ち。'],
         14: ['ニュースで見る事件が、', '"宗教はこわい"という思いを、', '強くしてきました。'],
         15: ['でも、その長い禁教の時代にも、', 'ひそかに信仰を守り続けた', '人たちがいました。'],
         16: ['見つかれば、命がけ。', 'それでも、二百年以上。'],
         17: ['命よりも大切なものに、', '出会っていたからです。'],
         18: ['数が少ないのは、', '神様の愛が小さいからじゃありません。'],
         19: ['まだ、知らせが', '届いていないだけなんです。'],
         20: ['イエスは、100匹のうち、', 'いなくなった1匹の羊を、', '探しに行くかた。'],
         21: ['そのために、十字架で、', '命までささげたかたです。']}


def note(text, y):
    """a small source line"""
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 30)
    w = d.textlength(text, font=f) + 50
    d.rounded_rectangle((W / 2 - w / 2, y - 28, W / 2 + w / 2, y + 28), 28, fill=CREAM + (225,))
    d.text((W / 2, y), text, font=f, fill=(150, 110, 80), anchor='mm')
    return im


GX, GY, GN = 20, 10, (4, 11)                                # 200 people; the one lit up at row 4, col 11


def icon(d, x, y, s, col):
    d.ellipse((x - 7 * s, y - 22 * s, x + 7 * s, y - 8 * s), fill=col)
    d.rounded_rectangle((x - 11 * s, y - 6 * s, x + 11 * s, y + 18 * s), int(8 * s), fill=col)


def grid_layer(t, t0, t_lit):
    im = layer(); d = ImageDraw.Draw(im)
    lit = smooth((t - t_lit) / 0.6)
    for r in range(GY):
        for c in range(GX):
            x, y = 112 + c * 45, 600 + r * 58
            u = smooth((t - t0 - (r * 0.06 + c * 0.015)) / 0.35)
            if u <= 0: continue
            if (r, c) == GN: continue
            a = int(255 * u * (1 - 0.55 * lit))
            icon(d, x, y, 1.0, (140, 120, 105, a))
    x, y = 112 + GN[1] * 45, 600 + GN[0] * 58
    u = smooth((t - t0 - (GN[0] * 0.06 + GN[1] * 0.015)) / 0.35)
    if lit > 0:
        g = Image.new('RGBA', (240, 240), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((40, 40, 200, 200), fill=(255, 210, 110, int(200 * lit)))
        g = g.filter(ImageFilter.GaussianBlur(26)); im.alpha_composite(g, (int(x - 120), int(y - 124)))
    col = tuple(int(a_ + (b_ - a_) * lit) for a_, b_ in zip((140, 120, 105), (226, 140, 40))) + (int(255 * u),)
    icon(d, x, y, 1.0 + 0.5 * lit, col)
    return im


def bars_layer(t, t0):
    im = layer(); d = ImageDraw.Draw(im)
    base, top = 1050, 1050 - 640                            # 30% = 640 px
    for k, (x, pct, val, name, sub, col) in enumerate(((330, 0.47, '0.5%未満', '日本', 'プロテスタント', (226, 140, 40)),
                                                       (750, 24.0, '約24%', '韓国', '大人・キリスト教', (110, 140, 190)))):
        u = smooth((t - t0 - 0.2 - k * 0.5) / 1.2)
        hgt = max(6, 640 * pct / 30 * u)
        d.rounded_rectangle((x - 110, base - hgt, x + 110, base), 18, fill=col + (235,))
        if u > 0:
            fa = int(255 * min(1, u * 2))
            d.text((x, base - hgt - 50), val, font=F(900, 64), fill=col[:3] + (fa,), anchor='mm', stroke_width=6, stroke_fill=CREAM)
        d.text((x, base + 50), name, font=F(900, 56), fill=BROWN, anchor='mm')
        d.text((x, base + 104), sub, font=F(700, 32), fill=(150, 110, 80), anchor='mm')
    d.line((150, base, 930, base), fill=(150, 110, 80, 200), width=4)
    return im


def timeline_layer(t, t0):
    im = layer(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 190, 990, 520), 44, fill=CREAM + (238,))
    x0, x1, y = 190, 890, 380
    u = smooth((t - t0 - 0.3) / 1.8)
    d.line((x0, y, x1, y), fill=(200, 180, 160, 255), width=8)
    if u > 0: d.line((x0, y, x0 + (x1 - x0) * u, y), fill=WARM + (255,), width=14)
    for x, lab, sub in ((x0, '1614', '禁教令'), (x1, '1873', '禁教の高札撤去')):
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=BROWN)
        d.text((x, y + 60), lab, font=F(900, 46), fill=BROWN, anchor='mm')
        d.text((x, y + 105), sub, font=F(700, 28), fill=(150, 110, 80), anchor='mm')
    a = int(255 * smooth((t - t0 - 1.6) / 0.5))
    d.text((540, 290), '250年以上', font=F(900, 72), fill=WARM + (a,), anchor='mm')
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
        (0.0, L(1), 'crosswalk', 1.0, 1.05, 0.5, 0.55),         # クリスチャンに会ったこと、ありますか
        (L(1), L(3), 'grid', 1.0, 1.0, 0.5, 0.5),               # 0.5%にも満たない / 200人に1人もいない
        (L(3), L(5), 'bars', 1.0, 1.0, 0.5, 0.5),               # 韓国は大人の4人に1人
        (L(5), L(9), 'kosatsu', 1.0, 1.05, 0.5, 0.5),           # 理由① 歴史: 250年以上の禁教
        (L(9), L(12), 'terauke', 1.0, 1.05, 0.5, 0.5),          # 理由② 家: お寺に登録
        (L(12), L(15), 'umbrellas', 1.0, 1.05, 0.5, 0.5),       # 理由③ みんなと同じ / 宗教はこわい
        (L(15), L(18), 'hidden_prayer', 1.0, 1.06, 0.5, 0.5),   # ひそかに信仰を守り続けた人たち
        (L(18), L(20), 'sunrise', 1.0, 1.05, 0.5, 0.5),         # まだ、知らせが届いていないだけ
        (L(20), L(21), 'shepherd', 1.0, 1.06, 0.5, 0.45),       # 1匹の羊を探しに行くかた (ルカ15:4)
        (L(21), L(22), 'cross', 1.0, 1.05, 0.5, 0.5),           # 十字架で命までささげた
        (L(22), TOTAL, 'sunset_walk', 1.0, 1.06, 0.5, 0.5),     # あなたひとりのためにも
    ]
    FILE = {'grid': 'paper_bg', 'bars': 'paper_bg'}
    imgs = {n: Image.open(os.path.join(ART, FILE.get(n, n) + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    POPS = [(pop_img('0.5', '%', label='にも満たない'), 540, 330, a(6.6), L(3)),
            (word_img('理由①　歴史', col=WARM, size=72), 540, 380, L(6) - 0.1, L(7)),
            (word_img('理由②　"家"', col=WARM, size=72), 540, 380, L(9) - 0.1, L(10)),
            (word_img('理由③　"みんなと同じ"', col=WARM, size=64), 540, 300, L(12) - 0.1, L(14))]
    caps = [(0.05, L(1), caption(['なぜ日本には、', 'クリスチャンが少ないの？'], 300, 76, accent=(1,))),
            (a(6.6), L(3), note('※日本宣教リサーチ(JMR)調査より', 530)),
            (L(3), L(5), caption(['200人に1人未満　と　4人に1人'], 250, 50)),
            (L(3) + 0.8, L(5), note('※韓国ギャラップ『韓国人の宗教 1983〜2025』より', 1210)),
            (L(20), L(21), verse(['いなくなった一匹を', '見つけるまで捜し歩かないでしょうか。'], 'ルカ15:4より', 170)),
            (seg0[-1] - 0.1, TOTAL, caption(['あなたが出会う', '"はじめてのクリスチャン"に、', 'なれたらうれしいです。'], 280, 64, accent=(1,)))]

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        src = imgs[n]
        if n == 'grid':
            src = src.convert('RGBA'); src.alpha_composite(grid_layer(t, t0 + 0.2, a(10.0))); src = src.convert('RGB')
        elif n == 'bars':
            src = src.convert('RGBA'); src.alpha_composite(bars_layer(t, t0)); src = src.convert('RGB')
        elif n == 'kosatsu' and t >= L(7):
            src = src.convert('RGBA'); tl = timeline_layer(t, L(7)); al_ = min(1.0, (t - L(7)) / 0.4, (L(9) - t) / 0.3)
            if t < L(9): src.alpha_composite(Image.fromarray((np.asarray(tl) * np.array([1, 1, 1, max(al_, 0)])).astype(np.uint8), 'RGBA'))
            src = src.convert('RGB')
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
