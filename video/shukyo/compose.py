"""Edit ゼロベース 「宗教って、こわい?」 (9:16): three ways to tell a harmful group -- a calm, plain explainer in warm
coloured pencil. The word 「宗教」 trembles; the bill, the empty room, the news; the speaker; three numbered cards, each
with its Bible verse at the top; the church, the door He knocks on, the window. Subtitles above the Reels UI.
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


SPLIT = {0: ['"宗教"って聞いて、', 'ちょっと、身構えましたか？'],
         4: ['…そんなニュース、', '何度も見てきましたよね。'],
         6: ['それは、あなたを守る、', '大切な感覚なんです。'],
         8: ['クリスチャンの私から、', '3つだけ伝えさせてください。'],
         10: ['"お金を払えば救われる"と', '言われたら、気をつけて。'],
         11: ['聖書は、救いは', '"プレゼント"だと言っています。'],
         14: ['家族や友だちから、', '引き離そうとするところ。'],
         15: ['聖書は、"父と母を敬いなさい"と', '教えています。'],
         18: ['聖書は、"愛には、恐れがない"と', '語ります。'],
         19: ['ほんとうの信仰は、', 'こわさで縛るものじゃありません。'],
         20: ['これは、キリスト教の名前を', '使っているところにも、当てはまります。'],
         21: ['神様は、あなたを', '無理やり連れていく方じゃない。'],
         22: ['ドアの外に立って、ノックして…', '待っている方なんです。'],
         25: ['あなたのペースで、', '知ってみてください。']}


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
        (0.0, L(1), 'tl_bg', 1.0, 1.0, 0.5, 0.5),                # 「宗教」 trembles
        (L(1), L(2), 'bill', 1.0, 1.04, 0.5, 0.45),              # 高いお金を払わされる
        (L(2), L(4), 'alone', 1.0, 1.04, 0.5, 0.5),              # 家族と引き離される / やめられない
        (L(4), L(5), 'tv', 1.0, 1.04, 0.5, 0.45),                # そんなニュース
        (L(5), L(7), 'speaker', 1.0, 1.04, 0.5, 0.45),           # こわいと思うのは当然 / 大切な感覚
        (L(7), L(9), 'tl_bg', 1.0, 1.0, 0.5, 0.5),               # 見分け方3つ
        (L(9), L(13), 'gift', 1.0, 1.05, 0.5, 0.55),             # 1つめ: お金 (エペソ2:8-9)
        (L(13), L(16), 'family', 1.0, 1.05, 0.5, 0.5),           # 2つめ: 家族 (出エジプト20:12)
        (L(16), L(20), 'free', 1.0, 1.05, 0.5, 0.45),            # 3つめ: 脅し (Iヨハネ4:18)
        (L(20), L(21), 'church', 1.0, 1.05, 0.5, 0.45),          # キリスト教の名前を使っているところにも
        (L(21), L(23), 'door', 1.0, 1.05, 0.5, 0.5),             # ドアの外に立ってノックして (黙示録3:20)
        (L(23), TOTAL, 'window', 1.0, 1.05, 0.5, 0.45),          # 急がなくていい。疑ってもいい。
    ]
    imgs = {n: Image.open(os.path.join(ART, n + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    BIG = big_word()
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    caps = [(L(7) + 0.1, L(9), caption(['宗教の', '見分け方 3つ'], 640, 112, accent=(1,), box=True)),
            (L(9), L(11), point_card(1, ['"お金を払えば救われる"', 'と言われたら'])),
            (L(11), L(13), verse(['あなたがたは恵みによって救われた。', 'それは、神の賜物（プレゼント）です。'], 'エペソ人への手紙 2章8〜9節より', 200)),
            (L(13), L(15), point_card(2, ['家族や友だちから', '引き離そうとする'])),
            (L(15), L(16), verse(['あなたの父と母を敬え。'], '出エジプト記 20章12節より', 200)),
            (L(16), L(18), point_card(3, ['"やめたら不幸になる"', 'と脅す'])),
            (L(18), L(20), verse(['愛には恐れがありません。', '全き愛は恐れを締め出します。'], 'ヨハネの手紙 第一 4章18節より', 200)),
            (L(22), L(23), verse(['見よ、わたしは戸の外に立って', 'たたいている。'], 'ヨハネの黙示録 3章20節より', 200)),
            (seg0[-1] - 0.1, TOTAL, caption(['質問はコメントでどうぞ。', '勧誘はしません。'], 300, 66, accent=(1,))),
            (seg0[-1] + 0.4, TOTAL, chip(['困ったときは', '消費者ホットライン「188」'], 560))]

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        src = imgs[n]
        if n == 'tl_bg' and t0 == 0.0:
            src = src.convert('RGBA')
            g = smooth(t / 0.5)
            amp = 7 * smooth((t - 1.0) / 0.3) * max(0.0, 1 - (t - 2.4) / 1.2) if t > 1.0 else 0.0
            dx = amp * np.sin(2 * np.pi * 6.5 * t); ang = 0.8 * amp / 7 * np.sin(2 * np.pi * 4.3 * t + 1)
            bw = BIG.rotate(ang, resample=Image.BICUBIC) if abs(ang) > 0.01 else BIG
            if g < 1: bw = Image.fromarray((np.asarray(bw) * np.array([1, 1, 1, g])).astype(np.uint8), 'RGBA')
            src.alpha_composite(bw, (int(40 + dx), 600))
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
