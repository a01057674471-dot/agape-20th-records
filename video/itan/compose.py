"""Edit 「"異端"ってなに?」 (9:16): warm coloured-pencil shots and a three-point checklist, timed to the narration
(audio/align.json) -- the news; two boxes; who Jesus is, what the standard is, what saves; the creed; check it with the Bible.
Verses at the top; subtitles above the Reels UI.  python3 compose.py out.mp4 [--preview | --frames t1,t2]
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


SPLIT = {0: ['"キリスト教っぽいけど、', '何かちがう"。'],
         1: ['そんな団体の話を、ニュースで', '聞いたことは、ありませんか。'],
         2: ['キリスト教では、聖書の教えから', '大きく外れた団体を、', '"異端"と呼びます。'],
         3: ['名前に"キリスト"や"教会"が', '入っていても、中身が同じとは、', '限らないんです。'],
         6: ['ひとつめ。', '"イエスは、だれか"。'],
         7: ['聖書は、イエス・キリストだけが、', '神であり、ただひとりの', '救い主だと語ります。'],
         8: ['もし、"教祖が、新しい救い主だ"と', '言うなら、それは聖書とちがいます。'],
         9: ['ふたつめ。', '"何が、いちばんの基準か"。'],
         10: ['聖書より大切な本や、', '"この団体の解釈だけが正しい"という', '教えがあるなら、注意が必要です。'],
         11: ['みっつめ。', '"救いの条件"。'],
         12: ['聖書は、救いは', '神様からの贈り物だと語ります。'],
         13: ['お金や、団体への忠誠で', '救いが決まるなら、それは', '聖書の福音では、ありません。'],
         14: ['教会は、2000年前から、', '"使徒信条"という短い言葉で、', 'この信仰を守ってきました。'],
         15: ['名前ではなく、中身を、', '聖書で確かめてください。'],
         16: ['ほんとうの福音は、あなたを', 'しばるものではなく、', '自由にするものです。']}

ITEMS = ['イエスは、だれか', '何が、基準か', '救いの条件は']


def check_layer(t, T):
    """the three points: rows appear, the current one is lit, each gets a tick; at the end they gather into 聖書で確かめる"""
    im = layer(); d = ImageDraw.Draw(im)
    mg = smooth((t - T['merge']) / 0.8)
    ha = smooth((t - T['rows']) / 0.4) * (1 - mg)
    if ha > 0: d.text((540, 430), '見分ける3つのポイント', font=F(900, 58), fill=BROWN + (int(255 * ha),), anchor='mm')
    for k, txt in enumerate(ITEMS):
        u = smooth((t - T['rows'] - 0.3 - k * 0.3) / 0.4)
        if u <= 0: continue
        y = 620 + k * 190
        y = y + (820 - y) * mg
        a = int(255 * u * (1 - mg))
        if a <= 0: continue
        lit = 1.0 if T['hl'][k] <= t < T['ck'][k] + 0.6 else 0.0
        d.rounded_rectangle((110, y - 72, 970, y + 72), 40, fill=((255, 236, 200) if lit else CREAM) + (int(240 * u * (1 - mg)),),
                            outline=(WARM + (a,)) if lit else None, width=5)
        d.rounded_rectangle((150, y - 42, 234, y + 42), 14, fill=(255, 255, 255, a), outline=BROWN + (a,), width=5)
        c = smooth((t - T['ck'][k]) / 0.35)
        if c > 0:
            p1, p2, p3 = (166, y), (190, y + 26), (232, y - 36)
            if c < 0.5: d.line([p1, (p1[0] + (p2[0] - p1[0]) * c * 2, p1[1] + (p2[1] - p1[1]) * c * 2)], fill=WARM + (a,), width=12)
            else:
                q = (c - 0.5) * 2
                d.line([p1, p2, (p2[0] + (p3[0] - p2[0]) * q, p2[1] + (p3[1] - p2[1]) * q)], fill=WARM + (a,), width=12, joint='curve')
        d.text((600, y), txt, font=F(900, 60), fill=BROWN + (a,), anchor='mm')
    if mg > 0:
        g = layer(); ImageDraw.Draw(g).ellipse((200, 640, 880, 1000), fill=(255, 214, 120, int(170 * mg)))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(50))); d = ImageDraw.Draw(im)
        d.text((540, 820), '聖書で確かめる', font=F(900, 96), fill=WARM + (int(255 * mg),), anchor='mm', stroke_width=9, stroke_fill=CREAM + (int(255 * mg),))
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
        (0.0, L(2), 'phone_news', 1.0, 1.05, 0.5, 0.45),        # キリスト教っぽいけど / ニュースで
        (L(2), L(4), 'two_boxes', 1.0, 1.05, 0.5, 0.5),         # 異端 / 中身が同じとは限らない
        (L(4), L(7), 'check', 1.0, 1.0, 0.5, 0.5),              # どう見分ける / みっつ / ひとつめ
        (L(7), L(8), 'teach', 1.0, 1.05, 0.5, 0.5),             # イエス・キリストだけが神、ただひとりの救い主
        (L(8), L(9), 'stage', 1.0, 1.05, 0.5, 0.45),            # 教祖が新しい救い主 (マタイ24:24)
        (L(9), L(10), 'check', 1.0, 1.0, 0.5, 0.5),             # ふたつめ
        (L(10), L(11), 'books_light', 1.0, 1.05, 0.5, 0.5),     # 聖書より大切な本 (ガラテヤ1:8)
        (L(11), L(12), 'check', 1.0, 1.0, 0.5, 0.5),            # みっつめ
        (L(12), L(13), 'receive', 1.0, 1.05, 0.5, 0.45),        # 救いは贈り物 (エペソ2:8〜9)
        (L(13), L(14), 'coins_box', 1.0, 1.05, 0.5, 0.45),      # お金や忠誠で
        (L(14), L(15), 'worship', 1.0, 1.05, 0.5, 0.5),         # 使徒信条
        (L(15), L(16), 'check', 1.0, 1.0, 0.5, 0.5),            # 聖書で確かめてください
        (L(16), TOTAL, 'free', 1.0, 1.06, 0.5, 0.5),            # 自由にするもの (ヨハネ8:32)
    ]
    FILE = {'check': 'paper_bg'}
    TT = dict(rows=L(4) + 0.5, hl=[L(6), L(9), L(11)], ck=[L(9) + 0.2, L(11) + 0.2, L(15) + 0.2], merge=a(64.86))
    imgs = {n: Image.open(os.path.join(ART, FILE.get(n, n) + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    g0 = imgs['books_light']; gs = Image.new('RGB', (W, H)); gs.paste(g0.crop((0, 350, W, H)), (0, 0)); gs.paste(g0.crop((0, 1500, W, H)).resize((W, 350)), (0, H - 350))
    imgs['books_light'] = gs
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    POPS = [(word_img('異端', col=WARM, size=110), 540, 380, a(10.9), L(3)),
            (word_img('使徒信条', col=WARM, size=80), 540, 330, a(58.92), L(15))]
    caps = [(0.05, L(2), caption(['"異端"って、', 'なに？'], 300, 84, accent=(1,))),
            (L(8), L(9), verse(['偽キリストたち、偽預言者たちが現れて、', '大きなしるしや不思議を行います。'], 'マタイ24:24より', 170)),
            (L(10), L(11), verse(['私たちが宣べ伝えた福音に反することを', '宣べ伝えるなら、だれであっても…'], 'ガラテヤ1:8より', 170)),
            (L(12), L(13), verse(['あなたがたは恵みのゆえに、', '信仰によって救われたのです。', 'それは神の賜物です。'], 'エペソ2:8〜9より', 170)),
            (L(16), seg0[-1], verse(['真理はあなたがたを', '自由にします。'], 'ヨハネ8:32より', 170)),
            (seg0[-1] - 0.1, TOTAL, caption(['気になる団体があれば、', '近くの教会の牧師に', '相談してみてください。'], 280, 64, accent=(1,)))]

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        src = imgs[n]
        if n == 'check':
            src = src.convert('RGBA'); src.alpha_composite(check_layer(t, TT)); src = src.convert('RGB')
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
