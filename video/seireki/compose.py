"""Edit 「知ってた?」 2 「2026年って、何から数えてる?」 (9:16): the calendar split by one life -- a timeline drawn in the edit
(the line, the shining point, BC and AD parting to either side), then warm coloured-pencil shots of Jesus' life, the cross
and the empty tomb, and the point of light settling into open hands. Text at the top, subtitles above the Reels UI.
python3 compose.py out.mp4 [--preview | --frames t1,t2]
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
LEAD, END_HOLD = 0.0, 3.5


def smooth(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def sub_layer(lines):
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 50); lh = 72
    bw = max(d.textlength(l, font=f) for l in lines) + 76
    y1 = SUB_Y1; y0 = y1 - lh * len(lines) - 36
    d.rounded_rectangle((W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 30, fill=CREAM + (232,))
    for k, l in enumerate(lines):
        d.text((W / 2, y0 + 18 + lh * k + lh / 2), l, font=f, fill=BROWN, anchor='mm')
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


SPLIT = {1: ['…でもこれ、"何から"数えて', '2026年か、知ってますか？'],
         4: ['"Before Christ"、', 'キリストより前、という意味なんです。'],
         5: ['そして、紀元後の"AD"は、', 'ラテン語で"主の年"。'],
         6: ['世界の暦は、この人を真ん中にして、', '前と後ろに分けられているんです。'],
         7: None,
         8: ['ちなみに"キリスト"は、', '名字じゃありません。'],
         10: ['イエスは、約2000年前、', 'いまのイスラエルで生まれた、', 'ひとりの男性。'],
         11: ['大工として働き、30歳ごろから、', '人々に神様のことを語り始めました。'],
         13: ['誰からも相手にされない人のそばに、', 'いつもいた人です。'],
         14: ['でも最後は、十字架という刑で', '殺されてしまいます。'],
         16: ['弟子たちは、命をかけて、', 'そう伝え続けました。'],
         17: ['聖書は、このイエスこそ、', '神様が人となって', '来てくださった方だと語ります。'],
         19: ['あなたの人生にも、', '"新しいはじまり"をくれる方なんです。']}


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


TY = 860                                               # the timeline's height on screen


def timeline(t, T, dim=1.0):
    """the timeline overlay at time t; T holds the cue times"""
    im = layer(); d = ImageDraw.Draw(im)
    a = lambda x: int(255 * x * dim)
    u = smooth((t - T['line']) / 1.4)
    if u > 0:
        x1 = 90 + 900 * u
        split = smooth((t - T['halves']) / 1.2)
        d.line((90, TY, x1, TY), fill=(110, 78, 52, a(1)), width=9)
        if split > 0:
            d.line((90, TY, min(x1, 540), TY), fill=(80, 112, 176, a(split)), width=9)
            if x1 > 540: d.line((540, TY, x1, TY), fill=(206, 120, 60, a(split)), width=9)
        for x in range(90, int(x1) + 1, 75):
            d.line((x, TY - 14, x, TY + 14), fill=(110, 78, 52, a(0.8)), width=4)
    for key, x0, sgn, big, col, small, sub, sub_key in (('bc', 540, -1, 'BC', (80, 112, 176), '紀元前', '"Before Christ"', 'bc2'),
                                                       ('ad', 540, 1, 'AD', (206, 120, 60), '紀元後', '"Anno Domini"（主の年）', 'ad2')):
        v = smooth((t - T[key]) / 0.9)
        if v <= 0: continue
        x = x0 + sgn * 270 * v
        d.text((x, TY - 150), big, font=F(900, 120), fill=col + (a(v),), anchor='mm')
        d.text((x, TY - 60), small, font=F(700, 44), fill=(92, 58, 40, a(v)), anchor='mm')
        w = smooth((t - T[sub_key]) / 0.6)
        if w > 0: d.text((x, TY + 75), sub, font=F(700, 34), fill=(120, 90, 60, a(w)), anchor='mm')
        ax = 90 if sgn < 0 else 990
        d.text((ax + (-sgn) * 10, TY - 4), '◀' if sgn < 0 else '▶', font=F(700, 40), fill=col + (a(v),), anchor='mm')
    n = smooth((t - T['now']) / 0.8)
    if n > 0:
        d.line((960, TY - 40, 960, TY + 40), fill=(206, 120, 60, a(n)), width=6)
        d.text((960, TY + 150), '2026年（いま）', font=F(700, 32), fill=(160, 90, 50, a(n)), anchor='mm')
    nt = smooth((t - T['bc']) / 0.8) * (1 - smooth((t - T['note_off']) / 0.5))
    if nt > 0: d.text((540, TY + 230), '※実際の誕生は紀元前4年ごろとされています', font=F(500, 30), fill=(120, 90, 60, a(nt * 0.9)), anchor='mm')
    dv = smooth((t - T['dot']) / 0.8)
    if dv > 0:
        pulse = 1 + 0.12 * np.sin(2 * np.pi * (t - T['dot']) / 2.2)
        glow_dot(im, 540, TY, 24 * pulse * (1 + 0.5 * smooth((t - T['halves']) / 2)), dv * dim)
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
    T = dict(line=L(2) + 0.1, dot=a(8.4), bc=L(3), bc2=L(4) + 0.1, ad=L(5), ad2=a(17.4), halves=L(6) + 0.3, now=L(6) + 1.2, note_off=L(7))
    shots = [
        (0.0, L(2), 'calendar26', 1.0, 1.04, 0.5, 0.45),         # 今年は2026年 / 何から数えて
        (L(2), L(10), 'tl_bg', 1.0, 1.0, 0.5, 0.5),              # timeline (drawn) / イエス・キリストって誰？ / 救い主
        (L(10), L(11), 'village', 1.0, 1.05, 0.5, 0.55),         # 約2000年前、いまのイスラエル
        (L(11), a(38.3), 'carpenter', 1.0, 1.04, 0.5, 0.45),     # 大工として働き
        (a(38.3), L(12), 'teach', 1.0, 1.04, 0.5, 0.45),         # 人々に神様のことを語り始めました
        (L(12), L(14), 'beside', 1.0, 1.05, 0.5, 0.5),           # 病気の人… のそばに、いつもいた
        (L(14), L(15), 'cross', 1.0, 1.05, 0.5, 0.5),            # 十字架という刑で
        (L(15), L(17), 'tomb', 1.0, 1.05, 0.5, 0.5),             # 三日目に、よみがえった / 弟子たちは
        (L(17), L(18), 'walker', 1.0, 1.06, 0.5, 0.5),           # 神様が人となって来てくださった方
        (L(18), L(19), 'tl_bg', 1.0, 1.0, 0.5, 0.5),             # 歴史を前と後ろに分けたこの方は
        (L(19), TOTAL, 'palm', 1.0, 1.05, 0.5, 0.5),             # あなたの人生にも新しいはじまり
    ]
    imgs = {n: Image.open(os.path.join(ART, n + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    TL_FULL = None
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    caps = [(0.05, L(2), caption(['2026年って、', '何から数えてる？'], 1090, 76, accent=(1,))),
            (L(7), L(8), caption(['イエス・キリストって', '誰？'], 520, 96, accent=(1,), box=True)),
            (L(8), L(10), caption(['"キリスト"', '＝ "救い主"'], 520, 96, accent=(1,), box=True)),
            (seg0[-1] - 0.1, TOTAL, caption(['イエスについて、', 'もっと知りたい？', '次回へ。'], 300, 72, accent=(2,)))]

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        src = imgs[n]
        if n == 'tl_bg':
            src = src.convert('RGBA')
            if t < L(17):
                dim = 1.0 - 0.65 * smooth((t - L(7)) / 0.6)
                src.alpha_composite(timeline(t, T, dim))
            else:                                              # the finished timeline again, the point shining
                src.alpha_composite(timeline(T['now'] + 3 + (t - L(18)), T))
                glow_dot(src, 540, TY, 26 + 6 * smooth((t - L(18)) / 2), 1.0)
            src = src.convert('RGB')
        if n == 'palm':
            src = src.convert('RGBA')
            m = smooth((t - L(19)) / 1.6)
            glow_dot(src, 540, TY + (1170 - TY) * m, 28 + 14 * m, 1.0)
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
