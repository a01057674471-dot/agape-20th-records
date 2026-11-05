"""Cut the gouache shots into a 9:16 video for 「イエス・キリストって、だれ？」.
No music, no narration: Japanese subtitles timed to a calm narration pace (so a voice can be laid on later),
glossary chips for first-time words, a 「聖書に基づく再現」 tag on historical re-creations, fast cuts every ~2.5 s.
python3 compose.py out.mp4 [--preview]
"""
import os, sys, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
W, H, FPS = 1080, 1920, 30
F = lambda w, s: ImageFont.truetype(os.path.join(HERE, 'fonts', f'ZenMaruGothic-{w}.ttf'), s)
INK = (58, 36, 24)
CREAM = (255, 248, 234)
RED = (192, 57, 43)

# ---------------------------------------------------------------- shots
# a shot: (image, start (zoom, cx, cy), end (zoom, cx, cy)); cx, cy are 0..1 of the source
def S(img, z0=1.0, c0=(0.5, 0.5), z1=None, c1=None):
    return (img, (z0, *c0), (z1 if z1 else z0 * 1.07, *(c1 or c0)))

RE = '聖書に基づく再現'     # tag for historical re-creations
HIST = {'s04', 's05', 's06', 's07', 's11', 's13', 's14'}

# blocks: (subtitle lines, shots, extras)   extras: term=(word, meaning), card=text, pause=seconds
BLOCKS = [
    (['イエス・キリスト。'], [S('build:s01', 1.0)], dict(title=True, min=3.2)),
    (['初めて聞く名前かもしれません。'], [S('s01', 1.0, (0.5, 0.5), 1.06), ], dict(title=True)),
    (['この人は、いったい誰なのでしょう。'], [S('s02', 1.0), S('s02', 1.45, (0.32, 0.6), 1.55, (0.36, 0.58)), S('s02', 1.6, (0.85, 0.66), 1.7)], {}),
    (['イエスは、およそ2,000年前、'], [S('s03', 1.0, (0.5, 0.5), 1.08)], dict(chip='約2,000年前')),
    (['今のイスラエルとパレスチナに', 'あたる地域で生きた、'], [S('s03', 1.5, (0.55, 0.42), 1.6, (0.55, 0.62)), S('s04', 1.0)], dict(chip='約2,000年前')),
    (['実在の人物です。'], [S('s04', 1.6, (0.6, 0.73), 1.7), S('s05', 1.35, (0.33, 0.47), 1.45)], {}),
    (['「キリスト」は、名字ではありません。'], [S('card:0', 1.0)], dict(card='キリスト ≠ 名字')),
    (['神が約束された「救い主」を', '意味する呼び名です。'], [S('card:0', 1.0)], dict(card='キリスト\n＝ 救い主', term=('キリスト', '神が約束された救い主'))),
    (['でも、誰を、何から', '救うのでしょうか。'], [S('s02', 1.2, (0.5, 0.62), 1.3), S('s02', 1.0, (0.5, 0.5), 1.08)], {}),
    (['その話をする前に、'], [S('s08', 1.3, (0.5, 0.3), 1.0, (0.5, 0.5))], {}),
    (['イエスが伝えた「神」について、', '少し説明させてください。'], [S('s08', 1.0), S('s08', 1.6, (0.7, 0.2), 1.7)], {}),
    (['聖書は、キリスト教が', '大切にしている書物です。'], [S('s10', 1.0), S('s10', 1.5, (0.54, 0.69), 1.6)], dict(term=('聖書', 'キリスト教が大切にしている書物'))),
    (['そこでは、神は、'], [S('s08', 1.5, (0.5, 0.75), 1.6)], {}),
    (['この世界と私たちの命を', '造った方として語られています。'], [S('s08', 1.0, (0.5, 0.5), 1.08), S('s08', 1.55, (0.3, 0.86), 1.65, (0.4, 0.86))], {}),
    (['遠くから人間を', '眺めているだけではなく、'], [S('s09', 1.0), S('s09', 1.75, (0.5, 0.17), 1.85)], {}),
    (['一人ひとりを知り、', '大切にされる方です。'], [S('s09', 1.75, (0.5, 0.5), 1.85), S('s09', 1.75, (0.5, 0.83), 1.85)], {}),
    (['イエスは、その神の愛を、', '言葉と行動で伝えました。'], [S('s05', 1.0), S('s05', 1.5, (0.5, 0.52), 1.6)], {}),
    (['病気で苦しむ人に近づき、'], [S('s07', 1.0), S('s07', 1.5, (0.45, 0.65), 1.6)], {}),
    (['周りから避けられていた人と', '食事をし、'], [S('s06', 1.3, (0.5, 0.6), 1.4), S('s06', 1.75, (0.27, 0.58), 1.85)], {}),
    (['人を赦すこと、', '愛することを教えました。'], [S('s05', 1.7, (0.5, 0.65), 1.8), S('s06', 1.8, (0.5, 0.5), 1.9)], {}),
    (['けれど、キリスト教は、'], [S('s11', 1.25, (0.5, 0.45), 1.15)], {}),
    (['イエスを単なる', '「優しい先生」として'], [S('card:1', 1.0)], dict(card='ただの\n「優しい先生」？')),
    (['伝えているのでは', 'ありません。'], [S('card:1', 1.0)], dict(card='ただの\n「優しい先生」？', strike=True)),
    (['神の子が、人間として、'], [S('build:s11', 1.0)], dict(min=3.0)),
    (['私たちのもとに', '来てくださった。'], [S('s11', 1.0, (0.5, 0.5), 1.2, (0.5, 0.42))], {}),
    (['それがイエスだと伝えています。'], [S('s05', 1.4, (0.33, 0.45), 1.5)], dict(pause=0.6)),
    (['では、なぜイエスは、', '十字架で死んだのでしょうか。'], [S('s13', 1.0), S('s13', 1.8, (0.65, 0.5), 1.9)], {}),
    (['十字架は、当時、', '人を処刑するために', '使われていたものでした。'], [S('s13', 1.3, (0.6, 0.55), 1.4), S('s13', 1.0)], dict(term=('十字架', '当時の処刑に使われたもの'))),
    (['聖書は、イエスの死が、'], [S('s10', 1.3, (0.55, 0.6), 1.4)], {}),
    (['私たちの「罪」と', '関わっていると語ります。'], [S('card:2', 1.0)], dict(card='罪')),
    (['ここでいう罪は、', '法律に違反することだけでは', 'ありません。'], [S('card:2', 1.0)], dict(card='罪 ＝ 法律違反\nだけではない')),
    (['自分を造った神に背を向け、'], [S('s12', 1.0), S('s12', 1.6, (0.48, 0.5), 1.7)], {}),
    (['自分の都合を優先し、'], [S('s12', 1.8, (0.49, 0.67), 1.9)], {}),
    (['人を傷つけてしまう。'], [S('s12', 1.4, (0.3, 0.8), 1.5)], {}),
    (['それは、誰か特別に', '悪い人だけではなく、'], [S('s02', 1.0), S('s09', 1.0)], {}),
    (['私たちみんなに', '関わる問題です。'], [S('s02', 1.4, (0.55, 0.6), 1.5), S('s06', 1.0)], {}),
    (['ただ、疲れていることや、', '悲しい気持ちになることが、'], [S('s12', 1.3, (0.5, 0.5), 1.4)], {}),
    (['罪なのではありません。'], [S('card:1', 1.0)], dict(card='疲れ・悲しみ\n＝ 罪 ではない')),
    (['聖書は、罪のないイエスが、'], [S('s11', 1.15, (0.5, 0.45), 1.25)], {}),
    (['私たちの罪を引き受け、'], [S('s13', 1.0, (0.5, 0.5), 1.1)], {}),
    (['私たちに代わって、', 'その裁きを受けたと語ります。'], [S('s13', 1.9, (0.65, 0.5), 2.0), S('s13', 1.35, (0.55, 0.35), 1.45, (0.55, 0.3))], {}),
    (['私たちが赦され、', '神との関係を取り戻すためです。'], [S('s05', 1.7, (0.5, 0.65), 1.8), S('s08', 1.0)], dict(pause=0.6)),
    (['そして、話は', '死で終わりません。'], [S('s14', 1.3, (0.5, 0.6), 1.0, (0.5, 0.5))], {}),
    (['イエスは、死んでから三日目に、'], [S('s14', 1.0), S('s14', 1.7, (0.36, 0.58), 1.8)], {}),
    (['再び生きる者となった。'], [S('s14', 1.8, (0.82, 0.43), 1.9)], {}),
    (['これを「復活」といいます。'], [S('card:0', 1.0)], dict(card='復活', term=('復活', '死からよみがえること'))),
    (['人々の思い出の中に残った、', 'という意味ではありません。'], [S('s14', 1.6, (0.36, 0.62), 1.7)], {}),
    (['本当に死からよみがえったと、', '聖書は伝えているのです。'], [S('s14', 1.0, (0.5, 0.5), 1.1), S('s10', 1.5, (0.54, 0.69), 1.6)], {}),
    (['だから、キリスト教では、'], [S('s11', 1.0)], {}),
    (['イエスを、今も生きている', '救い主として信じています。'], [S('s11', 1.25, (0.5, 0.42), 1.35), S('s08', 1.7, (0.7, 0.2), 1.8)], dict(pause=0.6)),
    (['神の赦しは、'], [S('s15', 1.0)], {}),
    (['立派な人になることで', '獲得する賞品ではありません。'], [S('card:2', 1.0)], dict(card='賞品', strike=True)),
    (['自分の罪を認め、'], [S('s15', 1.5, (0.5, 0.5), 1.6)], {}),
    (['イエスを信頼し、'], [S('s11', 1.6, (0.5, 0.42), 1.7)], {}),
    (['神に向き直る人に', '与えられる贈り物です。'], [S('s15', 1.0, (0.5, 0.45), 1.2, (0.5, 0.4))], dict(card2='贈り物')),
    (['初めて聞くと、', '不思議に思うことも、'], [S('s17', 1.0), S('s17', 1.6, (0.62, 0.35), 1.7)], {}),
    (['すぐには納得できないことも', 'あるかもしれません。'], [S('s17', 1.6, (0.5, 0.5), 1.7)], {}),
    (['疑問を持ったまま、', '読み始めてもかまいません。'], [S('s16', 1.0), S('s16', 1.5, (0.5, 0.47), 1.6)], {}),
    (['イエスは、どんな人に、'], [S('s07', 1.6, (0.5, 0.65), 1.7), S('s06', 1.0)], {}),
    (['どんな言葉をかけたのか。'], [S('s05', 1.5, (0.5, 0.5), 1.6)], {}),
    (['まずは、その物語を、', '少し読んでみませんか。'], [S('s16', 1.3, (0.5, 0.5), 1.45)], dict(pause=0.8)),
    ([], [S('s10', 1.0, (0.5, 0.5), 1.05)], dict(end=True, min=7.0)),
]


def dur_of(lines, ex):
    n = sum(len(l.replace('、', '').replace('。', '').replace('「', '').replace('」', '')) for l in lines)
    d = max(1.8, n / 6.8 + 0.45) + ex.get('pause', 0.0)
    return max(d, ex.get('min', 0))


# ---------------------------------------------------------------- overlays
def rounded(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def subtitle_layer(lines):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if not lines: return im
    d = ImageDraw.Draw(im)
    f = F(700, 56)
    lh = 80
    widths = [d.textlength(l, font=f) for l in lines]
    bw = max(widths) + 80
    y1 = 1560
    y0 = y1 - lh * len(lines) - 44
    rounded(d, (W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 34, (255, 248, 234, 232))
    for i, l in enumerate(lines):
        d.text((W / 2, y0 + 22 + lh * i + lh / 2), l, font=f, fill=INK, anchor='mm')
    return im


def tag_layer(text):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = F(700, 34)
    w = d.textlength(text, font=f) + 44
    rounded(d, (40, 150, 40 + w, 212), 31, (58, 36, 24, 190))
    d.text((40 + w / 2, 181), text, font=f, fill=CREAM, anchor='mm')
    return im


def term_layer(word, meaning):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f1, f2 = F(900, 58), F(700, 40)
    w = max(d.textlength(word, font=f1), d.textlength(meaning, font=f2)) + 90
    x0, y0 = W / 2 - w / 2, 250
    rounded(d, (x0 + 6, y0 + 8, x0 + w + 6, y0 + 172), 30, (120, 60, 30, 70))
    rounded(d, (x0, y0, x0 + w, y0 + 164), 30, (255, 248, 234, 245), outline=RED + (255,), width=5)
    d.text((W / 2, y0 + 52), word, font=f1, fill=RED, anchor='mm')
    d.text((W / 2, y0 + 120), meaning, font=f2, fill=INK, anchor='mm')
    return im


def chip_layer(text):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = F(900, 72)
    w = d.textlength(text, font=f) + 90
    rounded(d, (W / 2 - w / 2, 250, W / 2 + w / 2, 380), 64, RED + (240,))
    d.text((W / 2, 315), text, font=f, fill=CREAM, anchor='mm')
    return im


def card_layer(text, strike=False, y=760):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lines = text.split('\n')
    size = 150 if max(len(l) for l in lines) <= 4 else 104
    f = F(900, size)
    lh = size * 1.3
    y0 = y - lh * (len(lines) - 1) / 2
    for i, l in enumerate(lines):
        d.text((W / 2 + 5, y0 + i * lh + 7), l, font=f, fill=(150, 90, 50, 90), anchor='mm')
        d.text((W / 2, y0 + i * lh), l, font=f, fill=INK + (255,), anchor='mm')
    if strike:
        ww = max(d.textlength(l, font=f) for l in lines)
        yy = y0 + (len(lines) - 1) * lh
        d.line([(W / 2 - ww / 2 - 30, yy + 10), (W / 2 + ww / 2 + 30, yy - 20)], fill=RED + (255,), width=18)
    return im


def title_layer():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((540, 730), 'イエス・キリストって、', font=F(900, 74), fill=INK, anchor='mm')
    d.text((540, 880), 'だれ？', font=F(900, 170), fill=RED, anchor='mm')
    return im


def end_layer():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rounded(d, (70, 200, 1010, 900), 50, (255, 248, 234, 240))
    d.text((540, 320), 'もう少し、知りたいと思ったら。', font=F(700, 52), fill=INK, anchor='mm')
    d.text((540, 440), '聖書の中の', font=F(700, 50), fill=INK, anchor='mm')
    d.text((540, 570), '「マルコによる福音書」へ', font=F(900, 74), fill=RED, anchor='mm')
    d.text((540, 720), 'イエスの行動と言葉が', font=F(700, 48), fill=INK, anchor='mm')
    d.text((540, 800), '書かれています。', font=F(700, 48), fill=INK, anchor='mm')
    return im


# ---------------------------------------------------------------- sources
_cache = {}
def src(name):
    if name in _cache: return _cache[name]
    if name.startswith('card:'):
        im = Image.open(f'{OUT}/card_{name[5:]}.jpg').convert('RGB')
    elif name.startswith('build:'):
        k = name[6:]
        d = f'{OUT}/stages/{k}'
        im = [Image.open(f'{d}/{f}').convert('RGB') for f in sorted(os.listdir(d))]
    else:
        im = Image.open(f'{OUT}/{name}.jpg').convert('RGB')
    _cache[name] = im
    return im


def ease(t): return 1 - (1 - t) ** 3 if t < 1 else 1.0
def smooth(t): return t * t * (3 - 2 * t)


def view(im, z, cx, cy):
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw)
    y0 = min(max(cy * H - ch / 2, 0), H - ch)
    if abs(z - 1) < 1e-3: return im.copy()
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


def frame_of(shot, t, T):
    name, (z0, x0, y0), (z1, x1, y1) = shot
    u = smooth(min(t / T, 1.0))
    z, cx, cy = z0 + (z1 - z0) * u, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    im = src(name)
    if isinstance(im, list):                          # paint build-up: stages over the first 70% of the shot
        k = min(t / (T * 0.7), 1.0) * (len(im) - 1)
        i = int(k); a = k - i
        base = im[i] if i + 1 >= len(im) else Image.blend(im[i], im[i + 1], smooth(a))
        return view(base, z, cx, cy)
    return view(im, z, cx, cy)


def build_timeline():
    tl, t = [], 0.0
    for lines, shots, ex in BLOCKS:
        d = dur_of(lines, ex)
        n = len(shots)
        for i, sh in enumerate(shots):
            tl.append(dict(t0=t + d * i / n, t1=t + d * (i + 1) / n, shot=sh, lines=lines, ex=ex, bt0=t, bt1=t + d))
        t += d
    return tl, t


def main():
    out = sys.argv[1]
    preview = '--preview' in sys.argv
    tl, total = build_timeline()
    print(f'total {total:.1f}s, {len(tl)} shots, mean {total / len(tl):.2f}s')
    layers = {}
    def L(key, fn):
        if key not in layers: layers[key] = fn()
        return layers[key]
    tag = tag_layer(RE)
    title = title_layer()
    endl = end_layer()
    nfr = int(total * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    if preview:
        os.makedirs(f'{HERE}/preview', exist_ok=True)
    proc = None if preview else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    XF = 5                                            # frames of the quick cross-dissolve + punch-in at each cut
    si = 0
    prev_last = None
    for fi in range(nfr):
        t = fi / FPS
        if preview and fi % int(FPS * 1.5) != 0: continue
        while si + 1 < len(tl) and t >= tl[si]['t1']: si += 1
        s = tl[si]
        T = s['t1'] - s['t0']; lt = t - s['t0']
        name = s['shot'][0]
        sh = s['shot']
        # punch-in: a fast extra 6% zoom easing out over the first 8 frames
        pz = 1 + 0.06 * (1 - ease(min(lt * FPS / 8, 1)))
        sh2 = (sh[0], (sh[1][0] * pz, sh[1][1], sh[1][2]), sh[2])
        im = frame_of(sh2, lt, T)
        fcut = int(round(lt * FPS))
        if si > 0 and fcut < XF and prev_last is not None:
            im = Image.blend(prev_last, im, smooth((fcut + 1) / (XF + 1)))
        if t + 1 / FPS >= s['t1']: prev_last = im
        base = im.convert('RGBA')
        ex = s['ex']
        key = name.split(':')[-1][:3]
        if key in HIST: base.alpha_composite(tag)
        if ex.get('title'):
            a = min(max((t - 1.2) / 0.5, 0), 1) if s['bt0'] == 0 else 1
            if a > 0:
                tt = title.copy(); tt.putalpha(Image.eval(title.getchannel('A'), lambda v: int(v * a)))
                base.alpha_composite(tt)
        if ex.get('card'):
            c = L(('card', ex['card'], ex.get('strike', False)), lambda: card_layer(ex['card'], ex.get('strike', False)))
            base.alpha_composite(c)
        if ex.get('card2'):
            base.alpha_composite(L(('c2', ex['card2']), lambda: card_layer(ex['card2'], y=330)))
        if ex.get('chip'):
            base.alpha_composite(L(('chip', ex['chip']), lambda: chip_layer(ex['chip'])))
        if ex.get('term'):
            base.alpha_composite(L(('term',) + ex['term'], lambda: term_layer(*ex['term'])))
        if ex.get('end'):
            a = min(max((t - s['bt0'] - 0.4) / 0.6, 0), 1)
            e = endl.copy(); e.putalpha(Image.eval(endl.getchannel('A'), lambda v: int(v * a)))
            base.alpha_composite(e)
        if s['lines']:
            base.alpha_composite(L(('sub',) + tuple(s['lines']), lambda: subtitle_layer(s['lines'])))
        rgb = base.convert('RGB')
        if preview:
            rgb.resize((360, 640)).save(f'{HERE}/preview/{fi:05d}.jpg', quality=80)
        else:
            proc.stdin.write(rgb.tobytes())
        if fi % 300 == 0: print(f'{fi}/{nfr}', flush=True)
    if proc:
        proc.stdin.close(); proc.wait()
    print('done', out)


if __name__ == '__main__':
    main()
