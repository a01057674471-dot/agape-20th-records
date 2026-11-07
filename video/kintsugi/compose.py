"""Edit the kintsugi reel 「割れたままで、美しい」 (9:16), timed to the recorded narration (audio/align.json).
Blue picture-book paintings; the only warm colour is gold, and the gold seams are drawn on in the edit along the
painted cracks (art/cracks_*.json): first on the bowl, at the end over her heart. No music or effects.
python3 compose.py out.mp4 [--preview]
"""
import os, sys, json, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from script import LINES

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, 'art')
W, H, FPS = 1080, 1920, 30
F = lambda w, s: ImageFont.truetype(os.path.join(HERE, 'fonts', f'ZenMaruGothic-{w}.ttf'), s)
NAVY = (29, 52, 80); PAPER = (251, 250, 245); GOLD = (217, 164, 58); GOLD_HI = (255, 240, 176); GOLD_GLOW = (242, 212, 136)
END_HOLD = 5.0
CRACKS = {}
for f in glob.glob(os.path.join(ART, 'cracks_*.json')):
    CRACKS.update(json.load(open(f)))


def smooth(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def layer(): return Image.new('RGBA', (W, H), (0, 0, 0, 0))


# ---------------------------------------------------------------- the gold seams
def resample(path, step=3.0):
    P = np.asarray(path, np.float32)
    seg = np.hypot(*np.diff(P, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
    n = max(2, int(s[-1] / step) + 1); ss = np.linspace(0, s[-1], n)
    return np.stack([np.interp(ss, s, P[:, 0]), np.interp(ss, s, P[:, 1])], 1)


def gold_layer(paths, u, width=7.0, stagger=0.25):
    """gold seams drawn up to fraction u (0..1); paths start one after another (stagger) and grow along their length"""
    if u <= 0: return None
    SS = 2
    big = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    glow = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    n = len(paths)
    for k, p in enumerate(paths):
        a = k * stagger / max(n - 1, 1)
        v = smooth((u - a) / (1 - stagger)) if n > 1 else smooth(u)
        if v <= 0: continue
        Q = resample(p)
        m = max(2, int(len(Q) * v))
        Q = Q[:m] * SS
        rr = np.random.default_rng(k)
        wob = rr.normal(0, 0.6, Q.shape) * SS
        pts = [tuple(q) for q in (Q + wob)]
        g.line(pts, fill=GOLD_GLOW + (150,), width=int(width * 3.2 * SS), joint='curve')
        d.line(pts, fill=GOLD + (255,), width=int(width * SS), joint='curve')
        d.line([(x - 1.2 * SS, y - 1.2 * SS) for x, y in pts], fill=GOLD_HI + (235,), width=int(width * 0.32 * SS), joint='curve')
        tip = Q[-1]
        if v < 1:                                         # a bright spark at the growing tip
            r = 7 * SS; g.ellipse((tip[0] - r * 2, tip[1] - r * 2, tip[0] + r * 2, tip[1] + r * 2), fill=GOLD_HI + (180,))
    glow = glow.filter(ImageFilter.GaussianBlur(9 * SS))
    out = Image.alpha_composite(glow, big).resize((W, H), Image.LANCZOS)
    return out


# ---------------------------------------------------------------- text
def sub_layer(lines, y1=1590):
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 52); lh = 74
    bw = max(d.textlength(l, font=f) for l in lines) + 76
    y0 = y1 - lh * len(lines) - 38
    d.rounded_rectangle((W / 2 - bw / 2, y0, W / 2 + bw / 2, y1), 30, fill=PAPER + (236,))
    for k, l in enumerate(lines):
        d.text((W / 2, y0 + 19 + lh * k + lh / 2), l, font=f, fill=NAVY, anchor='mm')
    return im


def caption_layer(text, y, size=84, sub=None, gold_words=()):
    im = layer(); d = ImageDraw.Draw(im); f = F(900, size)
    lines = text.split('\n'); lh = size * 1.32
    for k, l in enumerate(lines):
        yy = y + k * lh
        col = GOLD if l in gold_words else NAVY
        d.text((W / 2 + 4, yy + 5), l, font=f, fill=(20, 30, 50, 70), anchor='mm')
        d.text((W / 2, yy), l, font=f, fill=col, anchor='mm', stroke_width=6, stroke_fill=PAPER)
    if sub:
        d.text((W / 2, y + len(lines) * lh + 10), sub, font=F(700, 46), fill=NAVY, anchor='mm', stroke_width=5, stroke_fill=PAPER)
    return im


def verse_layer():
    im = layer(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((90, 260, 990, 820), 46, fill=PAPER + (240,))
    d.text((540, 360), '聖書', font=F(700, 40), fill=(111, 143, 174), anchor='mm')
    for k, l in enumerate(['主は心の打ち砕かれた者を', '癒やし、', 'その傷を包まれる。']):
        d.text((540, 480 + k * 100), l, font=F(900, 62), fill=NAVY, anchor='mm')
    d.text((540, 760), '詩篇 147篇3節', font=F(700, 40), fill=GOLD, anchor='mm')
    return im


def chip_layer(text, y=300):
    im = layer(); d = ImageDraw.Draw(im); f = F(700, 40)
    w = d.textlength(text, font=f) + 70
    d.rounded_rectangle((W / 2 - w / 2, y - 36, W / 2 + w / 2, y + 36), 36, fill=PAPER + (235,), outline=GOLD + (255,), width=4)
    d.text((W / 2, y), text, font=f, fill=NAVY, anchor='mm')
    return im


def end_layer():
    im = layer(); d = ImageDraw.Draw(im)
    d.text((540, 430), '割れたままで、', font=F(900, 92), fill=NAVY, anchor='mm', stroke_width=6, stroke_fill=PAPER)
    d.text((540, 570), '美しい。', font=F(900, 120), fill=GOLD, anchor='mm', stroke_width=7, stroke_fill=PAPER)
    d.rounded_rectangle((150, 1560, 930, 1720), 34, fill=PAPER + (238,))
    d.text((540, 1610), '聖書', font=F(700, 36), fill=(111, 143, 174), anchor='mm')
    d.text((540, 1668), '詩篇147篇 ・ ペテロの手紙 第一 2章', font=F(700, 42), fill=NAVY, anchor='mm')
    return im


def view(im, z, cx, cy):
    if abs(z - 1) < 1e-4: return im.copy()
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw); y0 = min(max(cy * H - ch / 2, 0), H - ch)
    return im.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)


# shots: (first line, last line, image, zoom0, zoom1, centre)
SHOTS = [(0, 1, 'a_drop', 1.0, 1.02, (0.5, 0.55)), (2, 3, 'b_craft', 1.0, 1.02, (0.5, 0.5)),
         (4, 5, 'c_bowl', 1.0, 1.02, (0.5, 0.45)), (6, 6, 'd_train', 1.0, 1.02, (0.5, 0.55)),
         (7, 8, 'e_night', 1.0, 1.03, (0.5, 0.6)), (9, 10, 'f_light', 1.0, 1.02, (0.5, 0.55)),
         (11, 13, 'g_cross', 1.0, 1.03, (0.5, 0.5)), (14, 16, 'h_dawn', 1.0, 1.02, (0.45, 0.6))]
SPLIT = {0: ['大切なお茶碗が、', '割れてしまったら。'], 2: ['日本には「金継ぎ」という', '技があります。'],
         3: ['割れた器を、', '漆と金でつなぐのです。'], 5: ['金の線になって、', '前よりも美しくなる。'],
         6: ['私たちの心にも、', 'ひびがあります。'], 8: ['笑顔の下に、', 'そっと隠している傷。'],
         12: ['私たちの傷を、ご自分の身に', '負ってくださいました。'], 13: ['その傷によって、', '私たちは癒やされたのです。'],
         16: ['ひびの一つひとつを、', '愛でつないでくださいます。']}


def main():
    out = sys.argv[1]; preview = '--preview' in sys.argv
    al = json.load(open(os.path.join(HERE, 'audio', 'align.json')))
    seg0 = [0.0] + [s[1] for s in al['segs'][:-1]] + [al['total']]
    total = al['total'] + END_HOLD
    L = lambda i: seg0[i]
    tl = [dict(t0=L(a), t1=L(e + 1), img=img, z0=z0, z1=z1, c=c) for a, e, img, z0, z1, c in SHOTS]
    tl.append(dict(t0=seg0[-1], t1=total, img='i_end', z0=1.0, z1=1.02, c=(0.5, 0.55), end=True))
    imgs = {s['img']: Image.open(os.path.join(ART, s['img'] + '.jpg')).convert('RGB') for s in tl}
    subs = {i: sub_layer(SPLIT.get(i, [LINES[i]])) for i in range(len(LINES)) if i != 10}
    caps = [(L(0) + 0.3, L(2), caption_layer('割れたら、\n捨てますか？', 260)),
            (L(2) + 0.2, L(4), caption_layer('金継ぎ', 260, 150, 'ひびを、金でつなぐ', gold_words=('金継ぎ',))),
            (L(7), L(9), caption_layer('笑顔の下の、ひび', 300, 76)),
            (L(10), L(11), verse_layer()),
            (L(12), L(14), chip_layer('ペテロの手紙 第一 2章24節', 250)),
            (L(14) + 0.1, L(16) + 0.2, caption_layer('割れたままで、\n来ていい。', 240, 86))]
    endl = end_layer()
    # gold: the bowl in C (grows over lines 4-5), the bowl in H (already mended), her heart in H (grows over line 16),
    # the end bowl (complete)
    gold_c = [(L(4) + 0.3, L(6) - 0.6, CRACKS['c'], 8.0)]
    gold_h = [(L(14) - 0.01, L(14), CRACKS['h_bowl'], 5.0), (L(16) - 0.2, seg0[-1] - 0.3, CRACKS['h'], 6.0)]
    gold_i = [(seg0[-1] - 0.01, seg0[-1], CRACKS['i'], 7.0)]
    GOLD_BY = {'c_bowl': gold_c, 'h_dawn': gold_h, 'i_end': gold_i}
    gcache = {}

    def gold_for(img, t):
        outl = []
        for (a, e, paths, w) in GOLD_BY.get(img, []):
            u = smooth((t - a) / max(e - a, 1e-3)) if e - a > 0.05 else (1.0 if t >= a else 0.0)
            u = round(u, 3)
            key = (img, a, u)
            if key not in gcache:
                gcache[key] = gold_layer(paths, u, w, stagger=0.35)
            if gcache[key] is not None: outl.append(gcache[key])
        return outl

    def picture(s, t):
        u = smooth((t - s['t0']) / max(s['t1'] - s['t0'], 1e-3))
        z = s['z0'] + (s['z1'] - s['z0']) * u
        base = imgs[s['img']].convert('RGBA')
        for gl in gold_for(s['img'], t): base.alpha_composite(gl)
        return view(base, z, *s['c'])

    XF = 0.4
    nfr = int(total * FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', os.path.join(HERE, 'audio', 'narration.mp3'), '-filter_complex', '[1:a]apad[a]', '-map', '0:v', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
           '-shortest', '-movflags', '+faststart', out]
    proc = None if preview else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    if preview: os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
    for fi in range(nfr):
        t = fi / FPS
        if preview and fi % 15: continue
        k = max(i for i, s in enumerate(tl) if s['t0'] <= t + 1e-6)
        s = tl[k]
        im = picture(s, t)
        if k > 0 and t - s['t0'] < XF:
            im = Image.blend(picture(tl[k - 1], t), im, smooth((t - s['t0']) / XF))
        for (a, e, Lr) in caps:
            if a <= t < e:
                al_ = min((t - a) / 0.3, (e - t) / 0.25, 1.0)
                c = Lr if al_ >= 1 else Lr.copy()
                if al_ < 1: c.putalpha(Image.eval(Lr.getchannel('A'), lambda v: int(v * al_)))
                im.alpha_composite(c)
        if s.get('end'):
            a = smooth((t - s['t0'] - 0.3) / 0.7)
            e = endl.copy(); e.putalpha(Image.eval(endl.getchannel('A'), lambda v: int(v * a))); im.alpha_composite(e)
        elif t < seg0[-1]:
            i = max(i for i in range(len(LINES)) if seg0[i] <= t + 1e-6)
            if i in subs: im.alpha_composite(subs[i])
        rgb = im.convert('RGB')
        if preview: rgb.resize((360, 640)).save(os.path.join(HERE, 'preview', f'{fi:05d}.jpg'), quality=80)
        else: proc.stdin.write(rgb.tobytes())
    if proc: proc.stdin.close(); proc.wait()
    print('done', out, f'{total:.1f}s')


if __name__ == '__main__':
    main()
