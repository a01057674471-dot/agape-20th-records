"""Shared helpers for the retro-gouache shots of 「イエス・キリストって、だれ？」.
Every shot is a 1080 x 1920 (9:16) GouachePortrait panel. Bright, warm, picture-book palette.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'claude-drawing-skill', 'lib')
sys.path.insert(0, SKILL)
import numpy as np
from gouache import GouachePortrait, ramp, hexc, mix
from core import blur, shift, smoothstep, spline, noise2d

W, H = 1080, 1920

# warm skin ramps (dark -> light). Jesus and the people of 1st-century Judea: olive / light-brown.
SKIN_OLIVE = ['#9a5a3e', '#b9744f', '#d39468', '#e2ad82', '#efc9a2']
SKIN_DEEP = ['#7c4630', '#98593c', '#b8754f', '#cf9168', '#e3b088']
SKIN_LIGHT = ['#c0705d', '#d98d76', '#efbb98', '#f6d0b2', '#fbe3cc']
SKIN_JP = ['#c27a5f', '#d9967a', '#eebd9c', '#f5d2b6', '#fbe5d0']
HAIR_DARK = ['#1c1410', '#2e2018', '#4a3224', '#6a4a34', '#8a6648']
HAIR_BLACK = ['#121214', '#1f1d22', '#33303a', '#4c4856', '#6a6676']
HAIR_GREY = ['#77736f', '#a8a39d', '#d4cec4', '#ece6db', '#fffbf2']


def canvas(seed, tone='#e0a868', alpha=0.32, stages=None):
    g = GouachePortrait(W, H, seed=seed, keep_stages=bool(stages), stages_dir=stages)
    p = g.panel(0, 0, W, H)
    g.ground(tone, alpha=alpha)
    g.stage('ground')
    return g, p


def finish(g, out, stages=None):
    g.grain(0.9)
    g.save(out, stages_dir=stages, quality=93)


def rrect(cx, cy, w, h, r=10.0, n=5):
    pts = []
    for qx, qy, a0 in ((1, 1, 0), (-1, 1, 90), (-1, -1, 180), (1, -1, 270)):
        ox, oy = cx + qx * (w / 2 - r), cy + qy * (h / 2 - r)
        for a in np.linspace(a0, a0 + 90, n):
            pts.append((ox + r * np.cos(np.deg2rad(a)), oy + r * np.sin(np.deg2rad(a))))
    return np.array(pts, np.float32)


def flat_form(g, mask, colour, steps=3, relief=0.35, angle=None, length=(20, 48), width=(8, 16), bias=0.0, **kw):
    """block in + a gentle modelling: the workhorse for scenery"""
    g.block_in(mask, colour, angle=angle, length=length, width=width)
    return g.model_form(mask, ramp(colour, deep=0.62, shadow=0.8, light=0.22, pale=0.42, cool='#6a3a40'),
                        steps=steps, relief=relief, length=length, width=width, bias=bias,
                        **({'angle': angle} if angle is not None else {}), **kw)


# ================================================================== people
class Person:
    """a picture-book figure with a big head.
    hx, hy, r: head centre and radius. body: 'tunic' (1st century), 'jacket', 'shirt', 'dress', 'school'.
    arms: list of paths (shoulder -> hand) in absolute coords; hands are drawn at the last point.
    hair: 'curly', 'short', 'long', 'bun', 'scarf', 'bald', 'side' ; beard: None / 'short' / 'full' / 'grey'
    look: eye direction; mouth: 'smile', 'open', 'flat', 'sad', 'talk'; eyes_closed: for sorrow/prayer
    torso: (bottom_y, bottom_half_width) ; legs: list of paths (hip -> foot) or None
    """

    def __init__(self, g, hx, hy, r, skin=SKIN_OLIVE, hair='short', hair_col=HAIR_DARK, beard=None,
                 body='tunic', cloth='#e9dcc0', cloth2=None, stripe=None, arms=(), legs=None, torso=None,
                 look=(0.0, 0.0), mouth='smile', eyes_closed=False, brows=0.0, turn=0.0, scarf_col='#c4553a',
                 mantle=None, blush=0.45, seed=0, iris='#2a1a12', age=0, shoes='#5a3a2a', trousers='#3d4a66'):
        self.g, self.hx, self.hy, self.r = g, hx, hy, r
        self.skin, self.hair, self.hair_col, self.beard = skin, hair, hair_col, beard
        self.body, self.cloth, self.cloth2, self.stripe = body, cloth, cloth2, stripe
        self.arms, self.legs, self.look, self.mouth = arms, legs, look, mouth
        self.eyes_closed, self.brows, self.turn, self.scarf_col = eyes_closed, brows, turn, scarf_col
        self.mantle, self.blushs, self.seed, self.iris, self.age = mantle, blush, seed, iris, age
        self.shoes, self.trousers = shoes, trousers
        S = self.S = {}
        t = turn * r * 0.18                              # features shift with a 3/4 turn
        self.fx = hx + t
        S['face'] = g.ellipse(hx, hy, r * 0.86, r * 0.98)
        S['neck'] = g.poly([(hx - r * 0.28, hy + r * 0.6), (hx + r * 0.28, hy + r * 0.6),
                            (hx + r * 0.32, hy + r * 1.15), (hx - r * 0.32, hy + r * 1.15)])
        by, bw = torso or (hy + r * 3.3, r * 1.25)
        sy = hy + r * 1.02
        if body == 'dress':
            bw = bw * 1.3
        S['torso'] = g.poly([(hx - r * 0.95, sy + r * 0.25), (hx - r * 0.55, sy - r * 0.02), (hx, sy - r * 0.08),
                             (hx + r * 0.55, sy - r * 0.02), (hx + r * 0.95, sy + r * 0.25),
                             (hx + bw * 1.02, by - r * 0.4), (hx + bw, by), (hx - bw, by), (hx - bw * 1.02, by - r * 0.4)])
        self.shoulders = [(hx - r * 0.82, sy + r * 0.25), (hx + r * 0.82, sy + r * 0.25)]
        S['arms'] = [g.band(a, r * 0.42, r * 0.34) for a in arms]
        S['hands'] = [g.ellipse(a[-1][0], a[-1][1], r * 0.22, r * 0.2) for a in arms]
        S['legs'] = [g.band(l, r * 0.4, r * 0.32) for l in (legs or [])]
        S['feet'] = [g.ellipse(l[-1][0] + r * 0.12, l[-1][1] + r * 0.05, r * 0.3, r * 0.15) for l in (legs or [])]
        # hair masks
        top = g.ellipse(hx, hy - r * 0.32, r * 0.95, r * 0.78)
        if hair == 'curly':
            hm = np.maximum(top, g.blob(hx, hy - r * 0.18, r * 0.98, r * 0.86, 0.07, seed + 3))
            hm = hm * (1 - g.ellipse(self.fx, hy + r * 0.3, r * 0.76, r * 0.8) * smoothstep(hy - r * 0.4, hy - r * 0.12, g.P.YY))
            for sgn, sd in ((-1, 4), (1, 5)):          # wavy locks down to the jaw, behind the ears
                if self.turn * sgn > 0.5: continue
                lk = g.blob(hx + sgn * r * 0.82, hy + r * 0.42, r * 0.22, r * 0.55, 0.1, seed + sd, sgn * 8)
                hm = np.maximum(hm, lk * (1 - g.ellipse(self.fx, hy + r * 0.1, r * 0.78, r * 0.9)))
        elif hair in ('short', 'side'):
            hm = top * (1 - g.ellipse(self.fx, hy + r * 0.28, r * 0.8, r * 0.82) * smoothstep(hy - r * 0.32, hy - r * 0.05, g.P.YY))
            if hair == 'side':
                hm = np.maximum(hm, g.blob(self.fx - r * 0.3, hy - r * 0.55, r * 0.6, r * 0.28, 0.1, seed + 6, -12))
        elif hair == 'long':
            back = g.blob(hx, hy + r * 0.45, r * 1.08, r * 1.35, 0.06, seed + 7)
            hm = np.maximum(top, back) * (1 - g.ellipse(self.fx, hy + r * 0.32, r * 0.74, r * 0.78) * smoothstep(hy - r * 0.3, hy - r * 0.05, g.P.YY))
        elif hair == 'bun':
            hm = np.maximum(top, g.ellipse(hx + r * 0.1, hy - r * 1.0, r * 0.38, r * 0.32))
            hm = hm * (1 - g.ellipse(self.fx, hy + r * 0.28, r * 0.8, r * 0.82) * smoothstep(hy - r * 0.36, hy - r * 0.1, g.P.YY))
        elif hair == 'scarf':
            hm = g.poly([(hx - r * 1.08, hy + r * 1.3), (hx - r * 1.05, hy - r * 0.2), (hx - r * 0.7, hy - r * 0.92),
                         (hx, hy - r * 1.15), (hx + r * 0.7, hy - r * 0.92), (hx + r * 1.05, hy - r * 0.2),
                         (hx + r * 1.08, hy + r * 1.3)])
            hm = hm * (1 - g.ellipse(self.fx, hy + r * 0.12, r * 0.74, r * 0.86))
        elif hair == 'bald':
            hm = g.ellipse(hx, hy - r * 0.1, r * 0.92, r * 0.62) * (1 - g.ellipse(self.fx, hy - r * 0.3, r * 0.72, r * 0.9))
        else:
            hm = np.zeros_like(top)
        S['hair'] = hm
        if beard:
            ext = 1.16 if beard == 'full' else 1.06
            bm = g.poly([(hx - r * 0.84, hy + r * 0.12), (hx - r * 0.78, hy + r * 0.55), (hx - r * 0.45, hy + r * 0.95),
                         (hx, hy + r * ext), (hx + r * 0.45, hy + r * 0.95),
                         (hx + r * 0.78, hy + r * 0.55), (hx + r * 0.84, hy + r * 0.12),
                         (hx + r * 0.7, hy + r * 0.4), (self.fx + r * 0.36, hy + r * 0.6), (self.fx + r * 0.2, hy + r * 0.5),
                         (self.fx, hy + r * 0.5), (self.fx - r * 0.2, hy + r * 0.5), (self.fx - r * 0.36, hy + r * 0.6),
                         (hx - r * 0.7, hy + r * 0.4)])
            bm = bm * (1 - g.ellipse(self.fx, hy + r * 0.68, r * 0.2, r * 0.09))   # the mouth shows
            S['beard'] = bm
        if mantle:
            S['mantle'] = g.poly([(hx - r * 0.95, sy + r * 0.2), (hx - r * 0.3, sy + r * 0.05), (hx + r * 0.25, sy + r * 1.4),
                                  (hx + bw * 0.4, by), (hx - bw * 1.04, by), (hx - bw * 1.06, by - r * 0.6)]) * S['torso']
        self.fig = np.maximum.reduce([S['face'], S['neck'], S['torso'], S['hair']] + S['arms'] + S['hands'] + S['legs']
                                     + S['feet'] + ([S['beard']] if beard else []))

    # ---------------------------------------------------------------- phases
    def block(self):
        g, S, r = self.g, self.S, self.r
        for l, f in zip(S['legs'], S['feet']):
            g.block_in(l, self.trousers, angle=90, length=(14, 34), width=(6, 12))
            g.model_form(l, ramp(self.trousers, light=0.25, pale=0.42), steps=3, relief=0.4, length=(12, 26), width=(5, 10))
            g.block_in(f, self.shoes, angle=0, length=(8, 18), width=(4, 8))
            g.model_form(f, ramp(self.shoes, light=0.3, pale=0.5), steps=3, relief=0.5, length=(6, 12), width=(3, 6))
        g.block_in(S['torso'], self.cloth, angle=90, length=(30, 70), width=(12, 24))
        g.model_form(S['torso'], ramp(self.cloth, deep=0.6, shadow=0.8, light=0.25, pale=0.5, cool='#6a4048'),
                     steps=4, relief=0.45, angle=90, length=(24, 54), width=(9, 18))
        if self.stripe:                                 # the clavus stripes of a tunic, or a jacket's lapels
            for sgn in (-1, 1):
                x0 = self.hx + sgn * r * 0.36
                st = g.band([(x0, self.hy + r * 1.05), (x0 + sgn * r * 0.08, self.hy + r * 2.4),
                             (x0 + sgn * r * 0.14, self.hy + r * 4.6)], r * 0.13) * S['torso']
                g.glaze(st, self.stripe, 0.75, mode='normal', soft=1)
        if self.mantle:
            g.cast_shadow(S['mantle'], -4, 6, soft=8, alpha=0.3, colour='#5a3a30', on=S['torso'])
            g.block_in(S['mantle'], self.mantle, angle=75, length=(26, 60), width=(10, 20))
            g.model_form(S['mantle'], ramp(self.mantle, light=0.25, pale=0.5, cool='#4a2a38'), steps=4, relief=0.5,
                         angle=70, length=(22, 50), width=(8, 16))
        if self.body in ('jacket', 'school'):
            col = '#f4efe6' if self.body == 'jacket' else '#f8f4ea'
            v = self.g.poly([(self.hx - r * 0.3, self.hy + r * 1.0), (self.hx + r * 0.3, self.hy + r * 1.0),
                             (self.hx, self.hy + r * 2.0)]) * S['torso']
            g.block_in(v, col, length=(8, 20), width=(4, 8))
            if self.body == 'jacket':
                g.line([(self.hx, self.hy + r * 1.3), (self.hx - r * 0.06, self.hy + r * 1.95)], r * 0.12, '#b8423a', 0.9)
            else:
                g.line([(self.hx - r * 0.2, self.hy + r * 1.15), (self.hx, self.hy + r * 1.35), (self.hx + r * 0.2, self.hy + r * 1.15)],
                       r * 0.1, '#c23b3b', 0.9)
        for a, m in zip(self.arms, S['arms']):
            col = self.cloth2 or self.cloth
            g.block_in(m, col, length=(16, 36), width=(7, 13))
            g.model_form(m, ramp(col, light=0.25, pale=0.48, cool='#6a4048'), steps=3, relief=0.5, length=(14, 30), width=(6, 11))
        g.block_in(S['neck'], self.skin[2], length=(10, 22), width=(5, 9))
        g.model_form(S['neck'], self.skin, steps=3, relief=0.3, bias=-0.15, length=(10, 20), width=(4, 8))
        g.cast_shadow(S['face'], 0, r * 0.18, soft=r * 0.12, alpha=0.45, colour='#7a3f30', on=S['neck'])
        g.block_in(S['face'], self.skin[2], length=(r * 0.3, r * 0.7), width=(r * 0.12, r * 0.24))
        g.model_form(S['face'], self.skin, steps=4, relief=0.45, length=(r * 0.24, r * 0.5), width=(r * 0.1, r * 0.2))
        for h in S['hands']:
            g.block_in(h, self.skin[2], length=(6, 14), width=(3, 6))
            g.model_form(h, self.skin, steps=3, relief=0.5, length=(6, 12), width=(3, 6))
        # ears just outside the face at eye level
        if self.hair not in ('scarf', 'long'):
            for sgn in (-1, 1):
                if self.turn * sgn > 0.5: continue
                ex = self.hx + sgn * r * 0.86
                e = g.ellipse(ex, self.hy + r * 0.12, r * 0.14, r * 0.22) * (1 - S['face'] * 0.0)
                g.block_in(e * (1 - S['hair']), self.skin[2], length=(4, 10), width=(2, 5))
                g.model_form(e * (1 - S['hair']), self.skin, steps=3, relief=0.5, length=(4, 9), width=(2, 4))

    def texture(self):
        g, S, r = self.g, self.S, self.r
        hm = S['hair']
        if hm.max() > 0.2:
            if self.hair == 'scarf':
                g.cast_shadow(hm, 0, r * 0.1, soft=r * 0.1, alpha=0.4, colour='#6a3a2a', on=S['face'])
                g.block_in(hm, self.scarf_col, angle=80, length=(20, 50), width=(8, 16))
                g.model_form(hm, ramp(self.scarf_col, light=0.25, pale=0.5, cool='#4a2030'), steps=4, relief=0.55,
                             angle='fall', length=(18, 40), width=(7, 14))
                g.felt(hm, 0.35, fibres=0.5, fuzz=0.4, seed=self.seed + 9)
            else:
                hc = self.hair_col
                g.cast_shadow(hm, 0, r * 0.08, soft=r * 0.1, alpha=0.4, colour='#6a3a2a', on=S['face'])
                g.block_in(hm, hc[1], length=(12, 30), width=(6, 12))
                lam = g.form_light(hm, relief=0.6)[0]
                hx, hy = self.hx, self.hy
                if self.hair == 'curly':
                    flow = lambda x, y: np.degrees(np.arctan2(y - (hy - r * 0.2), x - hx)) + 60
                    g.hair_strands(hm, flow, hc, n=int(r * 9), length=(r * 0.2, r * 0.45), width=(1.0, 2.2), shade=lam,
                                   curl=1.6, spread=0.22, pad=2, seed=self.seed + 11)
                elif self.hair == 'long':
                    flow = lambda x, y: np.where(y < hy - r * 0.3, np.degrees(np.arctan2(y - (hy + r * 0.6), x - hx)) + 180,
                                                 90 - (x - hx) / r * 12)
                else:
                    flow = lambda x, y: np.degrees(np.arctan2(y - (hy + r * 0.6), x - hx)) + 180
                    g.hair_strands(hm, flow, hc, n=int(r * 11), length=(r * 0.18, r * 0.5), width=(1.0, 2.2), shade=lam,
                                   curl=0.8, spread=0.25, seed=self.seed + 11)
        if self.beard:
            bm = S['beard']
            bc = HAIR_GREY if self.beard == 'grey' else self.hair_col
            g.block_in(bm, bc[1], length=(8, 20), width=(4, 9))
            lam = g.form_light(bm, relief=0.5)[0]
            fx, hy = self.fx, self.hy
            g.hair_strands(bm, lambda x, y: 90 + (np.degrees(np.arctan2(y - hy, x - fx)) - 90) * 0.5, bc,
                           n=int(r * 6), length=(r * 0.07, r * 0.18), width=(0.9, 1.8), shade=lam, curl=1.2,
                           spread=0.2, pad=1, seed=self.seed + 12)

    def face(self):
        g, S, r = self.g, self.S, self.r
        fx, hy = self.fx, self.hy
        if self.blushs:
            for sgn in (-1, 1):
                g.blush(fx + sgn * r * 0.5, hy + r * 0.38, r * 0.2, r * 0.15, 'blush', self.blushs, mask=S['face'])
        ey = hy + r * 0.08
        sep = r * 0.36
        for sgn in (-1, 1):
            ex = fx + sgn * sep
            if self.eyes_closed:
                g.line([(ex - r * 0.13, ey + r * 0.02), (ex, ey + r * 0.08), (ex + r * 0.13, ey + r * 0.02)],
                       max(2.0, r * 0.05), '#3a2018', 0.9, taper=(0.3, 0.3))
            else:
                g.eye(ex, ey, r * 0.13, r * 0.12, iris=self.iris, iris_r=0.7, look=self.look, lid=0.25,
                      lid_colour=self.skin[1], lower=0.25)
            # brows (+ raised, - knitted)
            b0 = ey - r * 0.25 - self.brows * r * 0.06
            g.line([(ex - r * 0.15, b0 + sgn * self.brows * r * 0.0 + (r * 0.05 if self.brows < 0 and sgn < 0 else 0)),
                    (ex + r * 0.15, b0 - (r * 0.04 if self.brows < 0 else 0) * sgn)],
                   max(2.5, r * 0.065), (self.hair_col if self.beard != 'grey' else HAIR_GREY)[0] if self.hair != 'scarf' else '#3a2418',
                   0.85, taper=(0.3, 0.4))
        g.nose(fx + self.turn * r * 0.06, hy + r * 0.34, r * 0.14, r * 0.12, self.skin[2], on=S['face'], nostrils=0.5,
               highlight=0.6)
        my = hy + r * 0.64
        mc = '#7a2e28'
        if self.mouth == 'smile':
            g.line([(fx - r * 0.17, my - r * 0.03), (fx, my + r * 0.06), (fx + r * 0.17, my - r * 0.03)], max(2.5, r * 0.06), mc, 0.9)
        elif self.mouth == 'open':
            m = g.ellipse(fx, my + r * 0.02, r * 0.11, r * 0.08)
            g.block_in(m, '#6a2024', length=(4, 8), width=(2, 4), edge=0.3)
            g.glaze(g.ellipse(fx, my + r * 0.07, r * 0.07, r * 0.035) * m, '#d56a6a', 0.8, mode='normal')
        elif self.mouth == 'talk':
            g.line([(fx - r * 0.12, my), (fx, my + r * 0.05), (fx + r * 0.12, my)], max(3.0, r * 0.08), mc, 0.9)
        elif self.mouth == 'sad':
            g.line([(fx - r * 0.13, my + r * 0.05), (fx, my - r * 0.01), (fx + r * 0.13, my + r * 0.05)], max(2.5, r * 0.055), mc, 0.85)
        else:
            g.line([(fx - r * 0.12, my), (fx + r * 0.12, my)], max(2.5, r * 0.055), mc, 0.85)
        if self.age > 60:
            for sgn in (-1, 1):
                g.line([(fx + sgn * r * 0.55, ey + r * 0.02), (fx + sgn * r * 0.66, ey + r * 0.08)], 1.6, self.skin[0], 0.5)
                g.line([(fx + sgn * r * 0.26, my - r * 0.18), (fx + sgn * r * 0.32, my + r * 0.02)], 1.8, self.skin[0], 0.4)

    def highlight(self):
        g, S = self.g, self.S
        g.dry_highlight(S['face'] * (g.P.YY < self.hy), self.skin[4], above=0.72, length=(10, 26), width=(3, 7),
                        density=0.35, alpha=0.4, seed=self.seed + 21)
        g.dry_highlight(S['torso'], mix(hexc(self.cloth), hexc('#fff6e6'), 0.5) if False else '#fff3df', above=0.75,
                        length=(20, 50), width=(5, 10), density=0.3, alpha=0.35, seed=self.seed + 22)


def paint_people(g, people):
    for ph in ('block', 'texture', 'face', 'highlight'):
        for pp in people:
            getattr(pp, ph)()
        g.stage(ph)


# ================================================================== scenery
def stone_house(g, x, y, w, h, side=0.35, col='#e8cf9e', door=True, win=1, roof_items=True, seed=0):
    """a flat-roofed 1st-century stone house: lit front, shaded side, a dark door, small windows, a parapet"""
    sw = w * side
    front = g.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], smooth=False)
    sidem = g.poly([(x + w, y), (x + w + sw, y - sw * 0.45), (x + w + sw, y + h - sw * 0.45), (x + w, y + h)], smooth=False)
    roof = g.poly([(x, y), (x + sw, y - sw * 0.45), (x + w + sw, y - sw * 0.45), (x + w, y)], smooth=False)
    g.block_in(front, col, angle=0, length=(20, 50), width=(8, 16))
    g.model_form(front, ramp(col, light=0.2, pale=0.4, cool='#7a4a3a'), steps=3, relief=0.2, height=np.zeros_like(front),
                 angle=0, length=(18, 40), width=(6, 12), bias=0.1)
    g.block_in(sidem, mix(hexc(col), hexc('#a8705a'), 0.45), angle=90, length=(16, 36), width=(6, 12))
    g.block_in(roof, mix(hexc(col), hexc('#fff4dc'), 0.35), angle=0, length=(16, 36), width=(6, 12))
    rr = np.random.default_rng(seed)
    for _ in range(int(w * h / 1800)):                 # stone courses
        sx, sy = x + rr.uniform(4, w - 4), y + rr.uniform(6, h - 6)
        g.line([(sx, sy), (sx + rr.uniform(10, 26), sy + rr.uniform(-1, 1))], 1.6, '#b08a62', 0.35)
    if door:
        dw, dh = w * 0.24, h * 0.5
        dx = x + w * rr.uniform(0.2, 0.55)
        d = g.poly(rrect(dx + dw / 2, y + h - dh / 2, dw, dh, dw * 0.45), smooth=False) * (g.P.YY < y + h)
        g.block_in(d, '#6a4a3a', angle=90, length=(10, 24), width=(4, 8))
        g.glaze(d * (g.P.XX < dx + dw * 0.35), '#3a2620', 0.4)
    for i in range(win):
        wx = x + w * (0.72 if i == 0 else 0.15) - w * 0.06
        wm = g.poly([(wx, y + h * 0.22), (wx + w * 0.12, y + h * 0.22), (wx + w * 0.12, y + h * 0.36), (wx, y + h * 0.36)], smooth=False)
        g.block_in(wm, '#5a3a30', length=(4, 10), width=(2, 5))
    return np.maximum.reduce([front, sidem, roof])


def olive_tree(g, x, y, s=1.0, seed=0, col='#8a9a5a'):
    """a gnarled trunk and a broken, silvery canopy"""
    trunk = g.band([(x, y), (x - 8 * s, y - 60 * s), (x + 6 * s, y - 120 * s), (x - 4 * s, y - 160 * s)], 26 * s, 12 * s)
    g.block_in(trunk, '#7a5a40', angle=90, length=(10, 24), width=(4, 8))
    g.model_form(trunk, ['#3e2a1e', '#5a3e2c', '#7a5a40', '#9a7a5a', '#b89a78'], steps=3, relief=0.6, angle=90,
                 length=(8, 20), width=(3, 7))
    rr = np.random.default_rng(seed)
    can = np.zeros_like(trunk)
    for i in range(18):
        a = rr.uniform(0, 2 * np.pi); d = rr.uniform(0, 1) ** 0.6
        can = np.maximum(can, g.blob(x + np.cos(a) * d * 120 * s, y - 200 * s + np.sin(a) * d * 70 * s,
                                     rr.uniform(30, 52) * s, rr.uniform(22, 38) * s, 0.3, seed + i))
    g.block_in(can, col, length=(10, 24), width=(5, 10))
    g.model_form(can, ['#4a5a32', '#66763f', col, '#aab87a', '#d0d9a6'], steps=4, relief=0.7, length=(8, 18),
                 width=(4, 8), round_=0.8)
    for _ in range(int(160 * s)):                    # silvery leaves catching the light
        lx, ly = x + rr.normal(0, 90 * s), y - 210 * s + rr.normal(0, 50 * s)
        if can[int(np.clip(ly, 0, H - 1)), int(np.clip(lx, 0, W - 1))] > 0.5:
            a = rr.uniform(-60, 0)
            g.line([(lx, ly), (lx + 9 * s * np.cos(np.deg2rad(a)), ly + 9 * s * np.sin(np.deg2rad(a)))], 3.2 * s,
                   '#d6dfb0' if ly < y - 220 * s else '#9aaa6a', 0.8, taper=(0.3, 0.3))
    return np.maximum(trunk, can)


def palm(g, x, y, s=1.0, seed=0):
    tr = g.band([(x, y), (x + 8 * s, y - 120 * s), (x + 20 * s, y - 250 * s)], 18 * s, 12 * s)
    g.block_in(tr, '#9a7650', angle=90, length=(8, 20), width=(4, 8))
    for k in range(int(14 * s)):
        yy = y - k * 18
        g.line([(x - 8 * s + k * 1.4 * s, yy), (x + 10 * s + k * 1.4 * s, yy - 4)], 2, '#6a4a30', 0.5)
    cx, cy = x + 20 * s, y - 250 * s
    for a in np.linspace(-170, -10, 7).tolist() + [20, 160]:
        rad = np.deg2rad(a)
        L = 130 * s
        p = [(cx, cy), (cx + np.cos(rad) * L * 0.5, cy + np.sin(rad) * L * 0.5 - 18 * s),
             (cx + np.cos(rad) * L, cy + np.sin(rad) * L + 30 * s)]
        g.line(p, 22 * s, '#6f8a44', 0.95, taper=(0.1, 0.9))
        g.line(p, 6 * s, '#a8c070', 0.7, taper=(0.1, 0.9))


def hills(g, ys, col, seed=0, amp=60, avoid=None, relief=0.35):
    """a band of hills: everything below a wavy ridge line"""
    X = g.P.XX
    rr = np.random.default_rng(seed)
    ph = rr.uniform(0, 6, 3)
    ridge = ys + amp * (0.5 * np.sin(X / 210 + ph[0]) + 0.3 * np.sin(X / 97 + ph[1]) + 0.2 * np.sin(X / 51 + ph[2]))
    m = smoothstep(-1.5, 1.5, g.P.YY - ridge)
    if avoid is not None: m = m * (1 - avoid)
    g.block_in(m, col, angle=-8, length=(40, 90), width=(14, 26))
    g.model_form(m, ramp(col, deep=0.7, shadow=0.85, light=0.2, pale=0.4, cool='#7a5a50'), steps=3, relief=relief,
                 angle=-8, length=(36, 80), width=(12, 22))
    return m


def sky(g, top, bottom, avoid=None, seed=1, angle=-25):
    g.scumble_background(top, bottom=bottom, avoid=avoid, angle=angle, seed=seed, scratches=60, flecks=300,
                         dark=0.05, light=0.12)


def cloud(g, cx, cy, s=1.0, col='#fff6ea', seed=0):
    m = np.zeros((H, W), np.float32)
    rr = np.random.default_rng(seed)
    for i in range(6):
        m = np.maximum(m, g.ellipse(cx + rr.uniform(-110, 110) * s, cy + rr.uniform(-25, 15) * s,
                                    rr.uniform(50, 90) * s, rr.uniform(34, 52) * s))
    m = m * (g.P.YY < cy + 30 * s)
    g.block_in(m, col, angle=0, length=(20, 50), width=(8, 16))
    g.glaze(m * smoothstep(cy - 10 * s, cy + 30 * s, g.P.YY), '#e8c8c0', 0.35)
    return m


def sun(g, cx, cy, r, col='#ffe28a'):
    m = g.ellipse(cx, cy, r, r)
    g.glaze(g.ellipse(cx, cy, r * 2.4, r * 2.4), '#fff1c0', 0.45, mode='screen', soft=r * 0.8)
    g.block_in(m, col, length=(10, 24), width=(5, 10))
    g.glaze(g.ellipse(cx - r * 0.2, cy - r * 0.2, r * 0.6, r * 0.6), '#fffbe8', 0.6, mode='screen', soft=r * 0.3)
    return m


def floor(g, y0, col, avoid=None, angle=0):
    m = (g.P.YY > y0).astype(np.float32)
    if avoid is not None: m = m * (1 - avoid)
    g.block_in(m, col, angle=angle, length=(50, 110), width=(14, 26))
    g.model_form(m, ramp(col, light=0.2, pale=0.38), steps=3, relief=0.2, height=np.zeros_like(m), angle=angle,
                 length=(40, 90), width=(12, 22))
    return m


def bread(g, cx, cy, rx, ry, seed=0):
    m = g.blob(cx, cy, rx, ry, 0.06, seed)
    g.block_in(m, '#d9a35a', length=(6, 14), width=(3, 7))
    g.sphere_shade(cx, cy, rx, ry, ['#8a4e22', '#b06e32', '#d9a35a', '#ecc480', '#f8e2b0'], steps=4, mask=m,
                   length=(5, 12), width=(3, 6))
    for k in range(3):
        g.line([(cx - rx * 0.5 + k * rx * 0.45, cy - ry * 0.4), (cx - rx * 0.3 + k * rx * 0.45, cy + ry * 0.1)], 2.2, '#8a4e22', 0.6)
    return m


def cup(g, cx, cy, s, col='#c8784a'):
    body = g.poly([(cx - 26 * s, cy - 30 * s), (cx + 26 * s, cy - 30 * s), (cx + 20 * s, cy + 24 * s), (cx - 20 * s, cy + 24 * s)])
    g.block_in(body, col, angle=90, length=(6, 14), width=(3, 6))
    g.model_form(body, ramp(col, light=0.3, pale=0.5), steps=3, relief=0.6, length=(5, 12), width=(3, 6))
    g.glaze(g.ellipse(cx, cy - 30 * s, 26 * s, 7 * s), '#5a2a1a', 0.7, mode='normal')
    return body


FONT = os.path.join(HERE, '..', 'fonts', 'ZenMaruGothic-700.ttf')


def paint_text(g, text, x, y, size, colour='#3a2418', anchor='mm', alpha=0.95, weight=700, spacing=0.0):
    """lettering painted into the picture (map labels, a book title)"""
    from PIL import ImageFont
    from core import text_mask
    f = ImageFont.truetype(os.path.join(HERE, '..', 'fonts', f'ZenMaruGothic-{weight}.ttf'), int(size))
    m = text_mask(g.P.h, g.P.w, text, f, (x, y), anchor=anchor, spacing=spacing)
    m = blur(m, 0.6)
    g.glaze(m, colour, alpha, mode='normal')
    return m


def hand(g, x, y, s, angle, skin=SKIN_JP, fingers=4, spread=0.0, curl=0.0, thumb=True):
    """a simple painted hand: a palm and rounded fingers pointing along `angle` (degrees)"""
    a = np.deg2rad(angle)
    ux, uy = np.cos(a), np.sin(a)                     # along the fingers
    vx, vy = -uy, ux                                  # across the palm
    palm = g.blob(x, y, 46 * s, 40 * s, 0.03, 3, angle)
    m = palm
    for i in range(fingers):
        o = (i - (fingers - 1) / 2) * 22 * s
        da = np.deg2rad((i - (fingers - 1) / 2) * spread)
        fx, fy = np.cos(a + da), np.sin(a + da)
        L = (62 if i in (1, 2) else 52) * s
        bx, by = x + ux * 30 * s + vx * o, y + uy * 30 * s + vy * o
        tip = (bx + fx * L - vx * curl * 10 * s, by + fy * L - vy * curl * 10 * s)
        m = np.maximum(m, g.band([(bx, by), ((bx + tip[0]) / 2, (by + tip[1]) / 2), tip], 21 * s, 17 * s))
    if thumb:
        bx, by = x - ux * 5 * s + vx * 40 * s, y - uy * 5 * s + vy * 40 * s
        m = np.maximum(m, g.band([(bx, by), (bx + (ux * 0.6 + vx * 0.6) * 45 * s, by + (uy * 0.6 + vy * 0.6) * 45 * s)], 24 * s, 18 * s))
    g.cast_shadow(m, 6 * s, 10 * s, soft=8 * s, alpha=0.3, colour='#6a4030')
    g.block_in(m, skin[2], length=(8, 20), width=(4, 8))
    g.model_form(m, skin, steps=4, relief=0.55, length=(8, 18), width=(3, 7))
    for i in range(fingers - 1):                       # creases between fingers
        o = (i - (fingers - 2) / 2) * 22 * s
        bx, by = x + ux * 32 * s + vx * o, y + uy * 32 * s + vy * o
        g.line([(bx, by), (bx + ux * 28 * s, by + uy * 28 * s)], 1.6 * s, skin[0], 0.45, taper=(0.2, 0.6))
    return m


def page_lines(g, mask, x0, x1, y0, y1, gap=22, col='#8a7a6a', seed=0, alpha=0.45):
    """scribbled lines of text on a page (unreadable on purpose)"""
    rr = np.random.default_rng(seed)
    y = y0
    while y < y1:
        x = x0
        while x < x1 - 20:
            L = rr.uniform(20, 70)
            L = min(L, x1 - x)
            g.line([(x, y), (x + L, y + rr.uniform(-0.6, 0.6))], 2.6, col, alpha, taper=(0.1, 0.1), clip=mask)
            x += L + rr.uniform(8, 14)
        y += gap


def open_book(g, cx, cy, w, h, cover='#4a6a52', seed=0, tilt=0.0):
    """an open book seen from above, pages curving into the gutter"""
    t = tilt
    cov = g.poly([(cx - w / 2 - 14, cy - h / 2 - 10 + t), (cx + w / 2 + 14, cy - h / 2 - 10 - t),
                  (cx + w / 2 + 14, cy + h / 2 + 14 - t), (cx - w / 2 - 14, cy + h / 2 + 14 + t)], smooth=False)
    g.cast_shadow(cov, 14, 22, soft=18, alpha=0.4, colour='#5a3a2a')
    g.block_in(cov, cover, length=(20, 40), width=(8, 14))
    L = g.poly([(cx - w / 2, cy - h / 2 + t), (cx - w * 0.25, cy - h / 2 - 14), (cx - 4, cy - h / 2 + 4),
                (cx - 4, cy + h / 2), (cx - w * 0.25, cy + h / 2 - 8), (cx - w / 2, cy + h / 2 + t)])
    R = g.poly([(cx + 4, cy - h / 2 + 4), (cx + w * 0.25, cy - h / 2 - 14), (cx + w / 2, cy - h / 2 - t),
                (cx + w / 2, cy + h / 2 - t), (cx + w * 0.25, cy + h / 2 - 8), (cx + 4, cy + h / 2)])
    for m, sgn in ((L, -1), (R, 1)):
        g.block_in(m, '#f8f0dc', angle=90, length=(20, 50), width=(8, 16))
        X = g.P.XX
        g.glaze(m * np.exp(-np.abs(X - cx) / (w * 0.08)), '#c8a878', 0.55)          # the gutter shadow
        g.glaze(m * smoothstep(w * 0.38, w * 0.5, np.abs(X - cx)), '#e8d8b8', 0.4)
        x0 = cx - w / 2 + 40 if sgn < 0 else cx + 34
        page_lines(g, m, x0, x0 + w / 2 - 74, cy - h / 2 + 50, cy + h / 2 - 40, gap=h / 18, seed=seed + sgn)
    g.line([(cx + 30, cy - h / 2 + 2), (cx + 40, cy + h / 2 + 60)], 9, '#c0392b', 0.95, taper=(0.0, 0.0))   # ribbon
    return np.maximum(cov, np.maximum(L, R))
