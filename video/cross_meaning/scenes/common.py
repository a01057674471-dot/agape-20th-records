"""Shared helpers for the blue picture-book shots of 「その十字架、本当の意味を知っていますか？」.
Each shot is one 1080 x 1920 (9:16) BlueBook page: soft blue blocks, loose ink, scribbled darks, coral and
mustard accents only, chalk whites, printed on the page.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'claude-drawing-skill', 'lib'))
import numpy as np
from bluebook import BlueBook, INK, COLOURS
from core import blur, smoothstep, noise2d

W, H = 1080, 1920
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
HAIR_DARK = '#3b2b28'
SKIN = 'flesh'


def page(seed, stages=None):
    b = BlueBook(W, H, seed=seed, keep_stages=bool(stages), stages_dir=stages)
    b.paper()
    b.stage('paper')
    return b


def finish(b, out, stages=None):
    b.printed(1.0)
    b.save(out, stages_dir=stages, quality=93)


def circle_pts(cx, cy, rx, ry=None, a0=0, a1=360, n=40):
    ry = rx if ry is None else ry
    t = np.deg2rad(np.linspace(a0, a1, n))
    return np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], 1).astype(np.float32)


def cross_mask(b, cx, top, h, w=None, t=None, arm=0.3):
    """a Latin cross: upright from `top` down h px, cross-beam at arm*h"""
    w = w or h * 0.62
    t = t or h * 0.09
    up = b.poly([(cx - t / 2, top), (cx + t / 2, top), (cx + t / 2, top + h), (cx - t / 2, top + h)], smooth=False)
    yb = top + h * arm
    beam = b.poly([(cx - w / 2, yb - t / 2), (cx + w / 2, yb - t / 2), (cx + w / 2, yb + t / 2), (cx - w / 2, yb + t / 2)], smooth=False)
    return np.maximum(up, beam)


def cross_ink(b, cx, top, h, w=None, t=None, arm=0.3, width=4.0, seed=0):
    w = w or h * 0.62
    t = t or h * 0.09
    yb = top + h * arm
    pts = [(cx - t / 2, top), (cx + t / 2, top), (cx + t / 2, yb - t / 2), (cx + w / 2, yb - t / 2), (cx + w / 2, yb + t / 2),
           (cx + t / 2, yb + t / 2), (cx + t / 2, top + h), (cx - t / 2, top + h), (cx - t / 2, yb + t / 2),
           (cx - w / 2, yb + t / 2), (cx - w / 2, yb - t / 2), (cx - t / 2, yb - t / 2)]
    b.outline(pts, width, smooth=False, open_=0.4, seed=seed)


def wood_grain(b, cx, top, h, w=None, t=None, arm=0.3, seed=0):
    w = w or h * 0.62
    t = t or h * 0.09
    r = np.random.default_rng(seed)
    yb = top + h * arm
    for k in range(int(h / 30)):
        y = top + r.uniform(8, h - 8); x = cx + r.uniform(-t * 0.3, t * 0.3)
        b.ink([(x, y), (x + r.uniform(-1, 1), y + r.uniform(12, 28))], 1.6, colour='navy', dry=0.5, seed=seed + k)
    for k in range(int(w / 30)):
        x = cx - w / 2 + r.uniform(8, w - 8); y = yb + r.uniform(-t * 0.3, t * 0.3)
        b.ink([(x, y), (x + r.uniform(12, 26), y + r.uniform(-1, 1))], 1.6, colour='navy', dry=0.5, seed=seed + 50 + k)


# ================================================================== people
class Figure:
    """a picture-book person: big round head, a simple coat / dress, stick legs.
    x, y: head centre; R: head radius. arms: list of paths (shoulder -> hand), absolute px.
    hair: 'short', 'long', 'bun', 'cap' (back view covers the whole head); beard: bool.
    coat: fill colour; dress: long skirt to the floor (hides the legs); back: seen from behind (no face)."""

    def __init__(self, b, x, y, R, coat='cobalt', hair='short', hair_col=HAIR_DARK, beard=False, dress=False,
                 back=False, arms=(), look=(0.0, 0.0), mouth='smile', brows=0, legs=True, length=4.0, seed=0,
                 coat2=None, collar=None, tilt=0.0):
        self.b, self.x, self.y, self.R = b, x, y, R
        self.coat, self.coat2, self.hair, self.hair_col = coat, coat2 or coat, hair, hair_col
        self.beard, self.dress, self.back, self.arms = beard, dress, back, arms
        self.look, self.mouth, self.brows, self.seed, self.collar = look, mouth, brows, seed, collar
        self.tilt = tilt
        R_ = R
        S = self.S = {}
        S['head'] = b.ellipse(x, y, R_, R_ * 0.95, rot=tilt)
        bot = y + R_ * length
        self.bot = bot
        sh = y + R_ * 1.2
        bw = R_ * (1.95 if dress else 1.2)
        self.body_pts = [(x - R_ * 0.35, y + R_ * 0.88), (x + R_ * 0.35, y + R_ * 0.88), (x + R_ * 0.86, sh),
                         (x + bw, bot), (x - bw, bot), (x - R_ * 0.86, sh)]
        S['body'] = b.poly(self.body_pts)
        S['arms'] = [b.band(a, R_ * 0.34, R_ * 0.28) for a in arms]
        S['hands'] = [b.ellipse(a[-1][0], a[-1][1], R_ * 0.17, R_ * 0.16) for a in arms]
        self.legs = []
        if legs and not dress:
            for sgn in (-1, 1):
                self.legs.append([(x + sgn * R_ * 0.45, bot - 4), (x + sgn * R_ * 0.5, bot + R_ * 1.1)])
        cap = S['head'] * (YY < y - R_ * 0.28 + R_ * 0.08 * np.sin((XX - x) / (R_ * 0.25)))
        if back or hair == 'cap':
            hm = S['head'] * (YY < y + R_ * 0.75)
        elif hair == 'short':
            hm = cap
        elif hair == 'long':
            side = b.blob(x, y + R_ * 0.45, R_ * 1.1, R_ * 1.15, 0.05, seed + 1) * (1 - b.ellipse(x, y + R_ * 0.1, R_ * 0.82, R_ * 0.9))
            side = side * np.maximum((np.abs(XX - x) > R_ * 0.62).astype(np.float32), (YY < y).astype(np.float32))
            hm = np.maximum(cap, side)
        elif hair == 'bun':
            hm = np.maximum(cap, b.ellipse(x + R_ * 0.1, y - R_ * 1.02, R_ * 0.36, R_ * 0.3))
        else:
            hm = np.zeros_like(cap)
        if back and hair == 'bun':
            hm = np.maximum(hm, b.ellipse(x, y - R_ * 0.95, R_ * 0.36, R_ * 0.3))
        if back and hair == 'long':
            hm = np.maximum(hm, b.blob(x, y + R_ * 0.5, R_ * 1.02, R_ * 1.1, 0.05, seed + 1))
        S['hair'] = hm
        if beard and not back:
            S['beard'] = S['head'] * (YY > y + R_ * 0.25) * (1 - b.ellipse(x, y + R_ * 0.28, R_ * 0.6, R_ * 0.32)) \
                + b.ellipse(x, y + R_ * 0.72, R_ * 0.55, R_ * 0.32) * (1 - b.ellipse(x, y + R_ * 0.55, R_ * 0.2, R_ * 0.07))
            S['beard'] = np.clip(S['beard'], 0, 1)
        self.mask = np.maximum.reduce([S['head'], S['body'], S['hair']] + S['arms'] + S['hands'])

    # 2 blue blocks: the coat
    def blue(self, shade=True):
        b, S, x = self.b, self.S, self.x
        if self.coat in ('chalk', 'paper'):
            return
        b.fill(S['body'], self.coat, pressure=0.95, angle=78, mottle=0.14, seed=self.seed + 1)
        for a in S['arms']:
            b.fill(a, self.coat2, pressure=0.95, angle=60, seed=self.seed + 2)
        if shade:
            deep = {'cobalt': 'deep', 'blue': 'cobalt', 'cornflower': 'blue', 'powder': 'cornflower', 'teal': 'navy',
                    'navy': INK, 'deep': 'navy', 'coral': 'tomato', 'mustard': '#c8902e'}.get(self.coat, 'deep')
            b.fill(S['body'] * smoothstep(x + self.R * 0.2, x + self.R * 0.9, XX + (YY - self.y) * 0.15), deep, pressure=0.85,
                   angle=74, slip=0, seed=self.seed + 3)

    # 3 ink line
    def ink(self, w=None):
        b, S, x, y, R = self.b, self.S, self.x, self.y, self.R
        w = w or max(3.0, R * 0.07)
        b.head(x, y, R, R * 0.95, width=w * 1.1, rot=self.tilt, seed=self.seed + 10,
               ears=[] if self.back or self.hair in ('long',) else [(x - R * 0.98, y + R * 0.15, R * 0.17)])
        if not self.back:
            ex = R * 0.36; lx, ly = self.look
            ey = y + R * 0.1
            if self.mouth == 'closed_eyes':
                for sgn in (-1, 1):
                    b.ink([(x + sgn * ex - R * 0.1, ey), (x + sgn * ex, ey + R * 0.06), (x + sgn * ex + R * 0.1, ey)], w * 0.75, seed=self.seed + 11 + sgn)
            else:
                b.eyes([(x - ex, ey), (x + ex, ey)], r=max(3.0, R * 0.09), look=(lx, ly), seed=self.seed + 11)
            if self.brows:
                for sgn in (-1, 1):
                    yb = ey - R * 0.24
                    tiltb = self.brows * R * 0.06 * sgn
                    b.ink([(x + sgn * ex - R * 0.1, yb - tiltb), (x + sgn * ex + R * 0.1, yb + tiltb)], w * 0.7, seed=self.seed + 14 + sgn)
            b.ink([(x + R * 0.02, ey + R * 0.12), (x - R * 0.04, ey + R * 0.25), (x + R * 0.05, ey + R * 0.27)], w * 0.6, seed=self.seed + 16)
            my = y + R * 0.5
            if self.mouth in ('smile', 'closed_eyes'):
                b.smile(x, my, R * 0.22, R * 0.08, w * 0.7, seed=self.seed + 17)
            elif self.mouth == 'o':
                b.dot(x, my + R * 0.03, R * 0.06, R * 0.075, seed=self.seed + 17)
            elif self.mouth == 'hmm':
                b.ink([(x - R * 0.12, my + R * 0.02), (x + R * 0.12, my - R * 0.03)], w * 0.7, seed=self.seed + 17)
        b.outline(self.body_pts, w, smooth=False, open_=0.55, seed=self.seed + 18)
        if self.collar:
            b.ink([(x - R * 0.3, y + R * 0.95), (x, y + R * 1.35), (x + R * 0.3, y + R * 0.95)], w * 0.8, seed=self.seed + 19)
        for i, a in enumerate(self.arms):
            b.ink(a, w * 0.9, swell=0.3, seed=self.seed + 20 + i)
            hx, hy = a[-1]
            b.outline(circle_pts(hx, hy, R * 0.17, R * 0.16, n=12), w * 0.7, open_=0.3, seed=self.seed + 30 + i)
        for i, l in enumerate(self.legs):
            b.ink(l, w * 1.4, dry=0.1, seed=self.seed + 40 + i)
            b.dot(l[-1][0] + R * 0.06, l[-1][1] + R * 0.04, R * 0.13, R * 0.08, seed=self.seed + 42 + i)

    # 4 darks
    def dark(self):
        b, S = self.b, self.S
        b.hatch(S['body'] * smoothstep(self.x + self.R * 0.4, self.x + self.R * 1.0, XX), angle=74, spacing=7,
                length=(14, 30), width=2.2, dry=0.4, density=0.8, seed=self.seed + 50)

    # 5 accents: skin, hair, cheeks
    def accents(self):
        b, S, x, y, R = self.b, self.S, self.x, self.y, self.R
        hm = S['hair']
        face = S['head'] * (1 - hm)
        if not self.back:
            b.fill(face, SKIN, pressure=0.55, angle=30, loose=2, edge=6, dry_edge=0.5, lanes=0, seed=self.seed + 60)
            if self.mouth != 'hmm':
                b.blush(x - R * 0.58, y + R * 0.36, R * 0.2, seed=self.seed + 61)
                b.blush(x + R * 0.58, y + R * 0.36, R * 0.2, seed=self.seed + 62)
        for h in S['hands']:
            b.fill(h, SKIN, pressure=0.6, lanes=0, seed=self.seed + 63)
        if hm.max() > 0.3:
            hc = self.hair_col
            med = 'gouache' if hc.startswith('#') and hc < '#8' else 'crayon'
            b.fill(hm, hc, pressure=0.93, angle=20, loose=2.0, medium=med, lanes=0, seed=self.seed + 64)
            rr = np.random.default_rng(self.seed + 65)
            strands = []
            for k in range(int(R * 0.5)):
                a = rr.uniform(200, 340)
                px, py = x + np.cos(np.deg2rad(a)) * R * rr.uniform(0.3, 0.9), y + np.sin(np.deg2rad(a)) * R * rr.uniform(0.3, 0.9)
                if hm[int(np.clip(py, 0, H - 1)), int(np.clip(px, 0, W - 1))] < 0.5: continue
                strands.append([(px, py), (px + rr.uniform(-6, 6), py + rr.uniform(8, 20))])
            if strands:
                b.crayon(strands, 'slate' if med == 'gouache' else 'tomato', width=2.4, pressure=0.6, dry=0.4, seed=self.seed + 66)
        if self.beard and not self.back:
            b.fill(S['beard'] * S['head'], self.hair_col, pressure=0.9, angle=80, loose=1.5, medium='gouache', lanes=0, seed=self.seed + 67)

    def chalk(self):
        b = self.b
        if self.coat not in ('chalk', 'paper'):
            b.chalk([[(self.x - self.R * 0.6, self.y + self.R * 1.6), (self.x - self.R * 0.75, self.y + self.R * 3.2)]],
                    width=max(4, self.R * 0.07), pressure=0.55, seed=self.seed + 70)


def people_phase(figs, phase):
    for f in figs:
        getattr(f, phase)()


def union(*ms):
    return np.maximum.reduce([m for m in ms])
