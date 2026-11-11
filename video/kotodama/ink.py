"""brush calligraphy written stroke by stroke: 「言」 and 「光」 as hand-set brush paths (unit box, y down) with a press
at the entry, tome (stop) or harai (sweep) endings, dry-brush streaks and a soft bleed of ink into the washi."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

#      path points                                  width  ending
STROKES = {
    '言': [([(0.44, 0.03), (0.50, 0.08), (0.56, 0.14)], 0.075, 'dot'),
           ([(0.10, 0.27), (0.50, 0.255), (0.90, 0.245)], 0.055, 'tome'),
           ([(0.26, 0.41), (0.50, 0.405), (0.74, 0.40)], 0.048, 'tome'),
           ([(0.26, 0.55), (0.50, 0.545), (0.74, 0.54)], 0.048, 'tome'),
           ([(0.28, 0.68), (0.29, 0.82), (0.30, 0.96)], 0.05, 'tome'),
           ([(0.29, 0.68), (0.55, 0.675), (0.73, 0.67), (0.715, 0.82), (0.70, 0.95)], 0.05, 'tome'),
           ([(0.31, 0.935), (0.50, 0.93), (0.69, 0.93)], 0.045, 'tome')],
    '光': [([(0.50, 0.03), (0.50, 0.20), (0.50, 0.37)], 0.06, 'tome'),
           ([(0.21, 0.13), (0.27, 0.22), (0.33, 0.32)], 0.06, 'dot'),
           ([(0.80, 0.11), (0.74, 0.22), (0.67, 0.32)], 0.06, 'harai'),
           ([(0.07, 0.46), (0.50, 0.445), (0.93, 0.43)], 0.058, 'tome'),
           ([(0.40, 0.47), (0.39, 0.62), (0.33, 0.78), (0.22, 0.90), (0.08, 0.97)], 0.062, 'harai'),
           ([(0.60, 0.47), (0.60, 0.70), (0.605, 0.86), (0.66, 0.935), (0.86, 0.94), (0.93, 0.90), (0.94, 0.84)], 0.058, 'tome')],
}
INK = (30, 28, 36)


def _dense(pts, n=260):
    P = np.asarray(pts, np.float64)
    # Catmull-Rom through the points
    Q = [P[0]] + list(P) + [P[-1]]
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for t in np.linspace(0, 1, 40, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-1])
    A = np.array(out)
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(A, axis=0), axis=1))]
    s = np.linspace(0, d[-1], n)
    return np.stack([np.interp(s, d, A[:, 0]), np.interp(s, d, A[:, 1])], 1), d[-1]


def _width(s, W, kind, P):
    v = np.gradient(P, axis=0); ang = np.arctan2(v[:, 1], v[:, 0])
    dirf = 0.86 + 0.3 * np.abs(np.sin(ang))                 # verticals carry more ink than horizontals
    press = 0.8 + 0.4 * np.exp(-((s - 0.06) / 0.06) ** 2)
    if kind == 'dot':
        return W * dirf * (0.3 + 0.95 * np.sin(np.clip(s, 0, 1) * np.pi * 0.62) ** 1.2)
    if kind == 'harai':
        return W * dirf * press * np.clip(1.08 - 0.98 * smooth(np.clip((s - 0.35) / 0.65, 0, 1)), 0.05, 2)
    return W * dirf * press * (0.92 + 0.16 * np.exp(-((s - 0.96) / 0.05) ** 2)) * np.clip(1.2 - 0.25 * smooth(np.clip((s - 0.995) / 0.005, 0, 1)), 0, 2)


def smooth(u): return u * u * (3 - 2 * u)


class Calligraphy:
    def __init__(self, char, box, seed=1):
        x0, y0, x1, y1 = box
        self.box = box; self.S = x1 - x0
        self.strokes = []
        for pts, w, kind in STROKES[char]:
            P, L = _dense([(x0 + px * self.S, y0 + py * self.S) for px, py in pts])
            s = np.linspace(0, 1, len(P))
            self.strokes.append((P, _width(s, w * self.S, kind, P), L))
        self.total = sum(L for _, _, L in self.strokes) + 0.12 * self.S * len(self.strokes)    # pen-up gaps count as travel
        rng = np.random.default_rng(seed)
        pad = 60
        self.bx = (int(x0 - pad), int(y0 - pad), int(x1 + pad), int(y1 + pad))
        bw, bh = self.bx[2] - self.bx[0], self.bx[3] - self.bx[1]
        n = rng.random((bh // 3 + 1, bw // 3 + 1)).astype(np.float32)
        tex = Image.fromarray((n * 255).astype(np.uint8)).resize((bw, bh), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3.0))
        self.tex = np.asarray(tex, np.float32) / 255                     # dry-brush tooth

    def state(self, f):
        """f in 0..1 of the whole writing -> per-stroke fraction drawn, and the brush tip (x, y, down)"""
        d = f * self.total; out = []; tip = None
        gap = 0.12 * self.S
        for i, (P, Wd, L) in enumerate(self.strokes):
            if d <= 0:
                out.append(0.0)
                continue
            if d < L:
                u = d / L; out.append(u)
                j = min(len(P) - 1, int(u * (len(P) - 1))); tip = (P[j][0], P[j][1], True)
                d = -1; continue
            out.append(1.0); d -= L
            if d < gap and i + 1 < len(self.strokes):                        # travelling to the next stroke, brush lifted
                a, b = P[-1], self.strokes[i + 1][0][0]; u = d / gap
                tip = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - 30 * np.sin(np.pi * u), False); d = -1
            else:
                d -= gap
        if tip is None:
            P = self.strokes[-1][0]; tip = (P[-1][0], P[-1][1], False)
        return out, tip

    def layer(self, f, bleed=0.0, size=(1080, 1920)):
        fr, tip = self.state(f)
        X0, Y0, X1, Y1 = self.bx
        bw, bh = X1 - X0, Y1 - Y0
        k = 2
        m = Image.new('L', (bw * k, bh * k), 0); d = ImageDraw.Draw(m)
        for (P, Wd, L), u in zip(self.strokes, fr):
            if u <= 0: continue
            n = max(2, int(u * len(P)))
            for (x, y), w in zip(P[:n], Wd[:n]):
                r = w / 2 * k; cx, cy = (x - X0) * k, (y - Y0) * k
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
        m = m.resize((bw, bh), Image.LANCZOS)
        a = np.asarray(m, np.float32) / 255
        dry = np.clip(1.0 - 0.35 * np.clip((self.tex - 0.58) / 0.2, 0, 1), 0, 1)
        core = a * dry
        bl = np.asarray(m.filter(ImageFilter.GaussianBlur(2.5 + 4 * bleed)), np.float32) / 255
        al = np.clip(np.maximum(core * 0.96, bl * (0.28 + 0.12 * bleed)), 0, 1)
        out = Image.new('RGBA', size, (0, 0, 0, 0))
        lay = np.zeros((bh, bw, 4), np.uint8); lay[..., :3] = INK; lay[..., 3] = (al * 255).astype(np.uint8)
        out.paste(Image.fromarray(lay, 'RGBA'), (X0, Y0))
        return out, tip, a

    def glow(self, amount, size=(1080, 1920)):
        """the finished character shining gold"""
        _, _, a = self.layer(1.0, 1.0, size)
        X0, Y0, X1, Y1 = self.bx
        m = Image.fromarray((a * 255).astype(np.uint8))
        out = Image.new('RGBA', size, (0, 0, 0, 0))
        for rad, op, col in ((40, 0.55, (255, 214, 120)), (14, 0.6, (255, 236, 170)), (0, 0.85, (236, 178, 70))):
            g = np.asarray(m.filter(ImageFilter.GaussianBlur(rad)) if rad else m, np.float32) / 255
            g = np.clip(g * (2.2 if rad else 1.0), 0, 1) * op * amount
            lay = np.zeros(g.shape + (4,), np.uint8); lay[..., :3] = col; lay[..., 3] = (g * 255).astype(np.uint8)
            big = Image.new('RGBA', size, (0, 0, 0, 0)); big.paste(Image.fromarray(lay, 'RGBA'), (X0, Y0))
            out.alpha_composite(big)
        return out


def brush_image():
    """a calligraphy brush, tip at the bottom centre of the image"""
    W, Hh = 90, 700
    im = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((W / 2 - 15, 0, W / 2 + 15, Hh - 190), 12, fill=(196, 160, 104, 255), outline=(120, 88, 50, 255), width=3)
    for y in (90, 260, 420): d.line((W / 2 - 15, y, W / 2 + 15, y), fill=(140, 104, 60, 255), width=4)
    d.rectangle((W / 2 - 18, Hh - 200, W / 2 + 18, Hh - 160), fill=(70, 50, 40, 255))
    d.polygon([(W / 2 - 22, Hh - 165), (W / 2 + 22, Hh - 165), (W / 2 + 10, Hh - 40), (W / 2, Hh - 2), (W / 2 - 10, Hh - 40)], fill=(236, 226, 206, 255))
    d.polygon([(W / 2 - 17, Hh - 110), (W / 2 + 17, Hh - 110), (W / 2 + 9, Hh - 40), (W / 2, Hh - 2), (W / 2 - 9, Hh - 40)], fill=INK + (255,))
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    return im.rotate(-22, resample=Image.BICUBIC, expand=True, center=(W / 2, Hh - 2))
