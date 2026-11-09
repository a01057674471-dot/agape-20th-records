"""Edit 「無宗教です」って言うけど (reel 1, 9:16, ~60 s): warm coloured-pencil storybook shots timed to the recorded
narration (audio/align.json, from align2.py). Japanese subtitles, the hook and closing captions, the verse card.
Calm: one picture per thought, a slow 2-4% drift, soft dissolves; one quick 4-cut run for 「空も、雨も、ごはんも、いのちも」.
No music or effects -- the narration only.  python3 compose.py out.mp4 [--preview | --frames t1,t2]
"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from script import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, 'art')
W, H, FPS = 1080, 1920, 30
F = lambda w, s: ImageFont.truetype(os.path.join(HERE, 'fonts', f'ZenMaruGothic-{w}.ttf'), s)
BROWN = (92, 58, 40); CREAM = (255, 250, 238); WARM = (196, 110, 60)
TOTAL = 60.0


def smooth(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def sub_layer(lines):
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 50); lh = 72
    bw = max(d.textlength(l, font=f) for l in lines) + 76
    y1 = 1600; y0 = y1 - lh * len(lines) - 36
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


def verse():
    im = layer(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((110, 260, 970, 760), 44, fill=CREAM + (236,))
    d.text((540, 350), '聖書のことば', font=F(700, 38), fill=(170, 130, 90), anchor='mm')
    d.text((540, 480), 'すべての良い贈り物は、', font=F(900, 64), fill=BROWN, anchor='mm')
    d.text((540, 580), '上から来る。', font=F(900, 64), fill=BROWN, anchor='mm')
    d.text((540, 690), 'ヤコブの手紙 1章17節', font=F(700, 38), fill=WARM, anchor='mm')
    return im


def view(im, z, cx, cy):
    if abs(z - 1) < 1e-4: return im.copy()
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


SPLIT = {1: ['私たちは毎日、たくさんの', '「ありがとう」を口にします。'], 3: ['自分の力だけで', '生きているんじゃないと、'],
         6: ['お米を実らせてくれた、', 'お日さまや雨。'], 8: ['その「ありがとう」は、', '誰に届いているんだろう。'],
         10: None, 11: ['空も、雨も、今日のごはんも、', 'あなたのいのちも。'], 14: ['だから人は、', '「ありがとう」と応えるのです。'],
         15: ['感謝は、神さまとの関係の、', 'はじまりなんです。'], 0: ['いただきます。', 'ごちそうさま。おかげさまで。']}


def main():
    out = sys.argv[1]; preview = '--preview' in sys.argv
    only = None
    if '--frames' in sys.argv:
        only = {int(float(x) * FPS) for x in sys.argv[sys.argv.index('--frames') + 1].split(',')}; preview = True
    al = json.load(open(os.path.join(HERE, 'audio', 'align.json')))
    seg0 = [0.0] + [s[1] for s in al['segs'][:-1]] + [al['total']]
    L = lambda i: seg0[i]
    # the 4-cut run on line 11, split by the words' lengths
    a11, e11 = L(11), L(12)
    w = np.cumsum([0, 3, 3, 8, 8]) / 22.0
    run = [a11 + (e11 - a11) * x for x in w]
    # (t0, t1, image, zoom0, zoom1, cx, cy)
    shots = [
        (0.0, L(1), 'hands', 1.0, 1.04, 0.5, 0.55),
        (L(1), L(1) + (L(2) - L(1)) * 0.5, 'shrine', 1.0, 1.03, 0.5, 0.5),
        (L(1) + (L(2) - L(1)) * 0.5, L(2), 'omamori', 1.0, 1.04, 0.5, 0.45),
        (L(2), L(5), 'family', 1.0, 1.05, 0.48, 0.55),
        (L(5), L(7), 'paddy', 1.0, 1.03, 0.5, 0.5),
        (L(7), L(9), 'rice', 1.0, 1.04, 0.5, 0.5),
        (L(9), L(11), 'bible', 1.0, 1.04, 0.5, 0.65),
        (run[0], run[1], 'sunrise', 1.25, 1.28, 0.5, 0.2),          # 空も
        (run[1], run[2], 'paddy', 1.3, 1.33, 0.5, 0.55),            # 雨も
        (run[2], run[3], 'hands', 1.45, 1.48, 0.32, 0.77),          # 今日のごはんも
        (run[3], run[4], 'family', 1.45, 1.48, 0.72, 0.5),          # あなたのいのちも
        (L(12), L(13), 'sunrise', 1.0, 1.03, 0.5, 0.5),
        (L(13), seg0[-1], 'window', 1.0, 1.05, 0.5, 0.5),
        (seg0[-1], TOTAL, 'hands', 1.04, 1.07, 0.5, 0.52),
    ]
    imgs = {n: Image.open(os.path.join(ART, n + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    caps = [(0.0, L(1) - 0.2, caption(['日本人は、毎日', '"誰か"に感謝している。'], 300, 70, accent=(1,))),
            (L(10), L(11), verse()),
            (seg0[-1] + 0.2, TOTAL, caption(['あなたの"いただきます"には、', '宛先がある。'], 300, 64, accent=(1,))),
            (seg0[-1] + 2.0, TOTAL, caption(['今日、何に"ありがとう"と', '言いましたか？'], 1440, 54, box=True))]
    XF_SOFT, XF_QUICK = 0.5, 0.12

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        return view(imgs[n], z0 + (z1 - z0) * u, cx, cy)

    nfr = int(TOTAL * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', os.path.join(HERE, 'audio', 'narration.mp3'), '-filter_complex', '[1:a]apad[a]', '-map', '0:v', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
           '-shortest', '-movflags', '+faststart', out]
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
        xf = XF_QUICK if (a11 - 0.01 <= s[0] < e11 - 0.01 and k > 0) else XF_SOFT
        if k > 0 and t - s[0] < xf:
            im = Image.blend(pic(shots[k - 1], t), im, smooth((t - s[0]) / xf))
        im = im.convert('RGBA')
        for (a, e, Lr) in caps:
            if a <= t < e:
                al_ = min((t - a) / 0.4, (e - t) / 0.3 if e < TOTAL else 1.0, 1.0)
                c = Lr
                if al_ < 1:
                    c = Lr.copy(); c.putalpha(Image.eval(Lr.getchannel('A'), lambda v: int(v * al_)))
                im.alpha_composite(c)
        if t < seg0[-1]:
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
