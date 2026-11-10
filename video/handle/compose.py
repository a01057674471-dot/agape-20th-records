"""Edit 「私の人生、ほんとうに私のもの?」 (9:16): who holds the wheel of my life -- warm coloured-pencil shots timed to the
recorded narration (audio/align.json: Whisper word times snapped to speech onsets). Verses and captions sit at the TOP and
the subtitles in the middle-low band, clear of the Reels buttons and caption at the bottom. BGM mixed by mix_bgm.sh.
python3 compose.py out.mp4 [--preview | --frames t1,t2]
"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from script import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, 'art')
W, H, FPS = 1080, 1920, 30
F = lambda w, s: ImageFont.truetype(os.path.join(HERE, 'fonts', f'ZenMaruGothic-{w}.ttf'), s)
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
BROWN = (92, 58, 40); CREAM = (255, 250, 238); WARM = (196, 110, 60); INKC = (60, 60, 70)
SUB_Y1 = 1420                                            # subtitle box bottom (Reels UI covers below ~1500)
LEAD, END_HOLD = 0.0, 3.0


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


SPLIT = {0: ['私の人生は、私のもの。', '…ずっと、そう思っていました。'],
         1: ['でも、生まれる日も、親も、', '自分で選んだわけじゃない。'],
         3: ['好きになる気持ちも、落ちこむ心も、', '自分ではどうにもできない。'],
         5: ['どうして、私は私を', '思い通りにできないんだろう。'],
         6: ['車がこわれたら、', 'つくったメーカーに持っていきますよね。'],
         7: ['どう走るためにつくられたのか、', 'いちばん知っているのは、', 'つくった人だから。'],
         8: ['聖書は、あなたにも', '"つくった方"がいると語ります。'],
         9: ['その方は、あなたが', '座るのも、立つのも、言葉にする前の', '思いまで、ぜんぶ知っている、と。'],
         10: ['でも人は、その方の手をはなして、', '"自分が、自分の主人になろう"とした。'],
         11: ['聖書は、そこからすべてが', 'ずれ始めたと言います。'],
         12: ['だから神様は、', '遠くから説明するだけじゃなく、', 'ご自分から来てくださった。'],
         14: None,
         15: ['人生のハンドルを、', '私をつくった方に、あずけてみる。'],
         16: ['それは、自分を失うことじゃなく、', 'ほんとうの自分に出会うことなんです。'],
         17: None}


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
        (0.0, L(1), 'mine', 1.0, 1.04, 0.5, 0.45),               # 私の人生は、私のもの
        (L(1), L(2), 'birth', 1.0, 1.04, 0.45, 0.4),            # 生まれる日も、親も
        (L(2), L(3), 'fog', 1.0, 1.04, 0.5, 0.5),               # 明日どうなるかも
        (L(3), L(4), 'heart', 1.0, 1.04, 0.5, 0.4),             # 好きになる気持ちも、落ちこむ心も
        (L(4), L(6), 'crossroads', 1.0, 1.05, 0.5, 0.5),        # 持ち主なら… どうして思い通りにできない
        (L(6), L(7), 'car_broken', 1.0, 1.04, 0.5, 0.55),       # 車がこわれたら
        (L(7), L(8), 'garage', 1.0, 1.04, 0.5, 0.5),            # いちばん知っているのは、つくった人
        (L(8), L(9), 'bible', 1.0, 1.04, 0.5, 0.65),            # 聖書は、あなたにもつくった方が
        (L(9), L(10), 'bench', 1.0, 1.04, 0.5, 0.45),           # 座るのも、立つのも (詩篇139)
        (L(10), L(11), 'letgo', 1.0, 1.04, 0.5, 0.5),           # その方の手をはなして (創世記3)
        (L(11), L(12), 'walk', 1.0, 1.04, 0.5, 0.6),            # すべてがずれ始めた
        (L(12), L(13), 'starlight', 1.0, 1.05, 0.5, 0.55),      # ご自分から来てくださった
        (L(13), L(15), 'way', 1.0, 1.05, 0.5, 0.5),             # わたしが道であり、いのち (ヨハネ14:6)
        (L(15), L(16), 'wheel', 1.0, 1.04, 0.5, 0.5),           # ハンドルを、あずけてみる
        (L(16), L(17), 'free', 1.0, 1.04, 0.5, 0.45),           # ほんとうの自分に出会う
        (L(17), TOTAL, 'wheel', 1.04, 1.08, 0.5, 0.5),          # 誰がにぎっていますか
    ]
    imgs = {n: Image.open(os.path.join(ART, n + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    caps = [(0.05, L(1), caption(['私の人生、', 'ほんとうに私のもの？'], 300, 76, accent=(1,))),
            (L(9) + 0.2, L(10), verse(['あなたは、私が座るのも立つのも知り、', '私の舌にことばがのぼる前に、', 'そのすべてを知っておられる。'], '詩篇 139篇1〜4節より', 230)),
            (L(10) + 0.2, L(11), chip(['"自分が主人になる"と、', '人は神の手をはなした。', '創世記 3章より'], 290)),
            (L(14), L(15), verse(['わたしが道であり、', '真理であり、いのちなのです。'], 'ヨハネの福音書 14章6節より', 230)),
            (L(17), TOTAL, caption(['あなたの人生のハンドル、', 'いま、誰が', 'にぎっていますか？'], 300, 72, accent=(2,)))]

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
