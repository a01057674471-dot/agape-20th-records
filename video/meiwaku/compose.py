"""Edit reel 2 「迷惑をかけちゃいけない」 (9:16): warm coloured-pencil shots timed to the recorded narration
(audio/align.json: Whisper word times snapped to speech onsets). A 2.5 s hook before the voice, 「助けて」 typed and
deleted on the phone, the two verse references, and the closing comment prompt with a white heart.
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
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
BROWN = (92, 58, 40); CREAM = (255, 250, 238); WARM = (196, 110, 60); INKC = (60, 60, 70)
LEAD, END_HOLD = 2.5, 5.0


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


def verse(lines, ref, y0=240):
    im = layer(); d = ImageDraw.Draw(im); f = F(900, 58); lh = 86
    h = 150 + lh * len(lines)
    d.rounded_rectangle((90, y0, 990, y0 + h), 44, fill=CREAM + (238,))
    d.text((540, y0 + 60), '聖書のことば', font=F(700, 36), fill=(170, 130, 90), anchor='mm')
    for k, l in enumerate(lines):
        d.text((540, y0 + 130 + k * lh), l, font=f, fill=BROWN, anchor='mm')
    d.text((540, y0 + h - 42), ref, font=F(700, 36), fill=WARM, anchor='mm')
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


def typed(text_shown, cursor):
    """the phone's message box (box at 345..690 x 800..870 in the painting) with what she has typed"""
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 40)
    d.text((372, 836), text_shown, font=f, fill=INKC, anchor='lm')
    if cursor:
        x = 372 + d.textlength(text_shown, font=f) + 4
        d.line([(x, 812), (x, 860)], fill=(70, 120, 200), width=4)
    return im


def view(im, z, cx, cy):
    if abs(z - 1) < 1e-4: return im.copy()
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


SPLIT = {1: ['だから、しんどくても', '「大丈夫です」って笑っちゃうんですよね。'], 3: ['相手を思いやる、', '日本のやさしさだと思うんです。'],
         5: ['いつの間にか、', '自分をひとりにしていませんか。'], 6: ['「助けて」の言い方、', '忘れちゃっていませんか。'],
         7: ['聖書の中で、イエス・キリストは', 'こう言いました。'], 8: None,
         9: ['「迷惑かけないで」じゃなくて、', '「重いまま、おいで」って。'], 10: ['聖書には、「弱いときにこそ、', '強くされる」という言葉もあります。'],
         11: ['神様の前では、「大丈夫じゃない」から', '始めていいんです。'], 12: ['あなたが今かかえている', 'その荷物、']}


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
        (0.0, L(0), 'hook', 1.0, 1.04, 0.5, 0.5),                       # hook: 「大丈夫です」って、今日何回言った？
        (L(0), a(1.74), 'train', 1.0, 1.03, 0.5, 0.5),                  # 迷惑かけたくない。
        (a(1.74), a(3.9), 'overtime', 1.0, 1.03, 0.5, 0.55),            # だから、しんどくても
        (a(3.9), L(2), 'hook', 1.08, 1.12, 0.5, 0.45),                  # 「大丈夫です」って笑っちゃう
        (L(2), L(4), 'station', 1.0, 1.04, 0.5, 0.55),                  # 迷惑をかけない、日本のやさしさ
        (L(4), L(5), 'room_dark', 1.0, 1.04, 0.5, 0.55),                # でも、そのやさしさが…
        (L(5), L(7), 'phone', 1.0, 1.03, 0.5, 0.45),                    # ひとりに / 「助けて」の言い方
        (L(7), L(10), 'clearing', 1.0, 1.05, 0.5, 0.45),                # イエス・キリストは… 重いまま、おいで
        (L(10), L(12), 'sprout', 1.0, 1.05, 0.5, 0.55),                 # 弱いときにこそ / 大丈夫じゃない
        (L(12), TOTAL, 'bag', 1.0, 1.05, 0.5, 0.55),                    # その荷物、ひとりで持たなくていい
    ]
    imgs = {n: Image.open(os.path.join(ART, n + '.jpg')).convert('RGB') for n in set(s[2] for s in shots)}
    subs = {i: sub_layer(SPLIT.get(i) or [LINES[i]]) for i in range(len(LINES)) if SPLIT.get(i, 1) is not None}
    caps = [(0.15, L(1), caption(['"大丈夫です"って、', '今日何回言った？'], 300, 72, accent=(0,))),
            (L(8), L(9), verse(['疲れた人、重い荷物を', '背負っている人は、', 'わたしのところに来なさい。'], 'マタイの福音書 11章28節より')),
            (L(9), L(10), caption(['"重いまま、おいで"'], 330, 84, accent=(0,))),
            (L(10), L(12), ref_chip('コリント人への手紙 第二 12章10節より', 260)),
            (seg0[-1] + 0.2, TOTAL, end_layer())]
    # 「助けて」: typed during line 5, held, deleted during line 6 (as she says 「言い方、忘れちゃって」)
    word = '助けて'
    t_type0, t_type1 = L(5) + 0.6, L(5) + 1.8
    t_del0, t_del1 = L(6) + 1.0, L(6) + 1.9

    def phone_text(t):
        if t < t_type0: n = 0
        elif t < t_type1: n = int(len(word) * (t - t_type0) / (t_type1 - t_type0)) + 1
        elif t < t_del0: n = len(word)
        elif t < t_del1: n = len(word) - int(len(word) * (t - t_del0) / (t_del1 - t_del0)) - 1
        else: n = 0
        return word[:max(0, min(len(word), n))]
    XF = 0.5

    def pic(s, t):
        t0, t1, n, z0, z1, cx, cy = s
        u = smooth((t - t0) / max(t1 - t0, 1e-3))
        base = imgs[n]
        if n == 'phone':
            base = base.convert('RGBA'); base.alpha_composite(typed(phone_text(t), int(t * 2) % 2 == 0)); base = base.convert('RGB')
        return view(base, z0 + (z1 - z0) * u, cx, cy)

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
        if k > 0 and t - s[0] < XF:
            im = Image.blend(pic(shots[k - 1], t), im, smooth((t - s[0]) / XF))
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
