"""Edit 3rd season 「言霊」 (9:16): the word that made the world -- warm coloured-pencil shots timed to the recorded narration
(audio/align.json). The brush writes 「言」 and then 「光」 stroke by stroke on washi (ink.py); the 光 turns to gold.
Verses and captions at the top, subtitles above the Reels UI; koto + shō BGM (bgm.py) mixed by mix_bgm.sh.
python3 compose.py out.mp4 [--preview | --frames t1,t2]
"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from script import LINES
import ink

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


SPLIT = {0: ['受験生の前で、', '"落ちる"って言っちゃダメ。'],
         2: ['日本では昔から、言葉には', '"魂"が宿ると言われてきました。'],
         4: ['たったひと言で、', '元気が出たり、深く傷ついたり。'],
         5: ['言葉に力があるって、', 'きっとみんな知っているんです。'],
         6: ['実は聖書も、', '言葉の力について語っています。'],
         8: ['神様が"光あれ"と言うと…', '光があった。'],
         10: None,
         11: ['この世界は、神様の"ことば"に', 'よってつくられた、と。'],
         12: ['でも、聖書の"ことば"は、', 'ただの音じゃありません。'],
         13: ['そのことばは、人となって、', '私たちのところに来た。'],
         15: ['イエスは、たくさんの', 'ことばを語りました。'],
         16: ['動けなかった人に、', '"起きなさい"。'],
         17: ['自分を責め続けていた人に、', '"あなたの罪は、赦された"。'],
         18: ['誰かのひと言で、傷ついたあなたに、', '届いてほしい。'],
         19: ['世界をつくったその方が、いま、', 'あなたにも語りかけていることを。']}


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
    BOX = (240, 480, 840, 1080)
    KOTO = ink.Calligraphy('言', BOX, 1); HIKARI = ink.Calligraphy('光', BOX, 2)
    W1 = (L(2) + 0.35, L(3) - 0.15)                           # 言 written while 「言葉には魂が宿る」
    W2 = (L(10) - 0.1, L(11) + 0.9)                           # 光 written on 「はじめに、ことばがあった」
    G2 = W2[1] + 0.3                                          # then it turns to gold
    BRUSH = ink.brush_image()
    shots = [
        (0.0, L(1), 'ema', 1.0, 1.04, 0.5, 0.4),                 # 受験生の前で"落ちる"はダメ
        (L(1), L(2), 'wedding', 1.0, 1.04, 0.5, 0.45),           # 結婚式で"切れる"もダメ
        (L(2), L(4), 'w_koto', 1.0, 1.03, 0.5, 0.42),            # 言葉には魂が宿る / 言霊
        (L(4), a(12.85), 'smile', 1.0, 1.04, 0.5, 0.45),         # 元気が出たり
        (a(12.85), L(5), 'hurt', 1.0, 1.04, 0.5, 0.45),          # 深く傷ついたり
        (L(5), L(6), 'w_koto', 1.05, 1.1, 0.5, 0.4),             # 言葉に力がある
        (L(6), L(7), 'bible', 1.0, 1.04, 0.5, 0.65),             # 実は聖書も
        (L(7), a(24.25), 'ink_dark', 1.0, 1.03, 0.5, 0.47),      # 世界のはじまり。神様が"光あれ"と言うと…
        (a(24.25), L(9), 'ink_light', 1.0, 1.06, 0.5, 0.47),     # 光があった
        (L(9), L(12), 'w_hikari', 1.0, 1.04, 0.5, 0.42),         # はじめに、ことばがあった (光 written, turns gold)
        (L(12), L(15), 'walker', 1.0, 1.07, 0.5, 0.5),           # ただの音じゃない / ことばは人となって
        (L(15), L(16), 'teach', 1.0, 1.04, 0.5, 0.45),           # たくさんのことばを語りました
        (L(16), L(17), 'rise', 1.0, 1.04, 0.5, 0.42),            # 起きなさい
        (L(17), L(18), 'forgiven', 1.0, 1.05, 0.5, 0.42),        # あなたの罪は、赦された
        (L(18), TOTAL, 'letter', 1.0, 1.06, 0.5, 0.42),          # 届いてほしい / 語りかけている
    ]
    imgs = {n: Image.open(os.path.join(ART, n + '.jpg')).convert('RGB') for n in set(s[2] for s in shots) - {'w_koto', 'w_hikari'} | {'washi'}}

    def written(cal, w0, w1, t, glow_at=None):
        base = imgs['washi'].convert('RGBA')
        f = min(max((t - w0) / (w1 - w0), 0.0), 1.0)
        lay, tip, _ = cal.layer(f, bleed=min(1.0, max(0.0, (t - w0) / 6)))
        base.alpha_composite(lay)
        if glow_at is not None and t > glow_at:
            base.alpha_composite(cal.glow(smooth((t - glow_at) / 1.2)))
        # the brush: in at the start, follows the tip, then away up and to the right
        if w0 - 0.6 < t < w1 + 0.8:
            x, y, down = tip
            if t < w0: u = (w0 - t) / 0.6; x, y = x + 300 * u, y - 260 * u
            if t > w1: u = (t - w1) / 0.8; x, y = x + 380 * smooth(u), y - 340 * smooth(u)
            if not down and w0 <= t <= w1: y -= 6
            alpha = 1.0 if w0 <= t <= w1 else max(0.0, 1 - abs(t - (w0 if t < w0 else w1)) / (0.6 if t < w0 else 0.8))
            br = BRUSH if alpha >= 0.99 else Image.fromarray((np.asarray(BRUSH) * np.array([1, 1, 1, alpha])).astype(np.uint8), 'RGBA')
            bw, bh = br.size
            base.alpha_composite(br, (int(x - bw * 0.07), int(y - bh + 4)))
        return base.convert('RGB')

    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    caps = [(0.05, L(2), caption(['言霊（ことだま）って、', 'ほんとうにある？'], 300, 74, accent=(1,))),
            (L(8), L(9), verse(['神は仰せられた。「光、あれ。」', 'すると光があった。'], '創世記 1章3節より', 150)),
            (L(10), L(12), verse(['はじめに、ことばがあった。'], 'ヨハネの福音書 1章1節より', 150)),
            (L(13), L(15), verse(['ことばは人となって、', '私たちの間に住まわれた。'], 'ヨハネの福音書 1章14節より', 150)),
            (L(16), L(18), chip(['「起きなさい」', '「あなたの罪は赦された」', 'マルコの福音書 2章より'], 240)),
            (seg0[-1] - 0.2, TOTAL, caption(['あなたが、いちばん', '言われたいひと言は？'], 300, 72, accent=(1,)))]

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        if n == 'w_koto': src = written(KOTO, *W1, t)
        elif n == 'w_hikari': src = written(HIKARI, *W2, t, glow_at=G2)
        else: src = imgs[n]
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
        xf = 0.9 if s[2] == 'ink_light' else XF
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
