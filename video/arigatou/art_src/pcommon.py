"""helpers for the warm coloured-pencil shots of 「無宗教です」って言うけど (9:16)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'claude-drawing-skill', 'lib'))
import numpy as np
from pencilbook import PencilStorybook, hexc
from core import blur, spline, smoothstep, noise2d

W, H = 1080, 1920
ART = os.path.join(HERE, '..', 'art')
LIGHT = (-0.75, -0.5, 0.45)                 # warm morning light from the upper left
SKIN = ('pink', 'skin', 'skin_shade')


class Shot:
    def __init__(self, seed, stages=None):
        self.p = PencilStorybook(W, H, seed=seed, keep_stages=bool(stages), stages_dir=stages)
        self.p.finish(vignette=0.5, warmth=0.6)
        self.p.paper()
        self.r = np.random.default_rng(seed)
        self.stages = stages

    def sd(self):
        return int(self.r.integers(1 << 30))

    def save(self, name):
        import pcommon as _pc
        self.p.save(os.path.join(_pc.ART, name + '.jpg'), stages_dir=self.stages)


def curve(pts, n):
    P = spline(np.asarray(pts, np.float32), 16)
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    s = np.linspace(0, d[-1], n)
    return np.stack([np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], 1).astype(np.float32)


def morning_sky(S, region, warm_low=True, avoid=None):
    p = S.p
    v = np.clip(p.value(0.0, 1.0, 0, int(region.shape[0] * 0.7), 0.03), 0, 1)
    f = p.flow(-3, 4, 400)
    p.hatch(region, f, ('day_sky', v * 0.9 + 0.1), length=(60, 150), width=(1.8, 2.6), density=1.6, pressure=0.74,
            avoid=avoid, seed=S.sd())
    p.hatch(region, p.rotate(f, 6), ('day_sky', np.clip(v + 0.1, 0, 1)), length=(50, 120), width=(1.7, 2.4),
            density=1.0, pressure=0.7, alpha=0.5, avoid=avoid, seed=S.sd())
    if warm_low:
        low = region * smoothstep(0.45, 1.0, v)
        p.hatch(low, p.rotate(f, 3), ('glow', 1 - v), length=(50, 120), width=(1.7, 2.4), density=1.1,
                pressure=0.7, opacity=0.5, alpha=0.6, avoid=avoid, seed=S.sd())


def cloud_mask(p, cx, cy, w, h, rng, bumps=4):
    m = p.ellipse(cx, cy, w * 0.5, h * 0.42)
    for k in range(bumps):
        t = (k + 0.5) / bumps - 0.5
        bw = w * rng.uniform(0.16, 0.26)
        m = np.maximum(m, p.ellipse(cx + t * w * 0.8, cy - h * rng.uniform(0.15, 0.45), bw, bw * rng.uniform(0.55, 0.8)))
    return blur(m * (p.YY < cy + h * 0.3), 3)


def clouds(S, specs):
    """soft storybook clouds: the paper lifted almost white, long horizontal strokes, a warm underside"""
    p = S.p
    cm = np.zeros((H, W), np.float32)
    for (cx, cy, w, h) in specs:
        cm = np.maximum(cm, cloud_mask(p, cx, cy, w, h, S.r))
    cm = blur(cm, 6)
    p.lift(cm, 'white', 0.75)
    p.hatch(cm, p.flow(-2, 6, 300), ('white', 'cream', 'ivory'), (40, 110), (1.7, 2.4), 1.4, 0.66, opacity=0.75, alpha=0.6, seed=S.sd())
    under = blur(cm * (1 - np.roll(cm, -24, 0)), 10) * cm
    p.hatch(np.clip(under * 1.4, 0, 1), p.flow(-2, 6, 300), ('peach', 'apricot', 'lavender'), (40, 100), (1.6, 2.3), 0.9, 0.66,
            opacity=0.45, alpha=0.45, seed=S.sd())
    return cm


def rice_bowl(S, cx, cy, rw, steam=True, bowl=('cream', 'powder', 'cornflower', 'slate'), avoid=None):
    """a chawan of rice seen a little from above: the bowl body, the white rice dome with grains, rising steam"""
    p = S.p
    rh = rw * 0.42
    body = p.poly(np.vstack([curve([(cx - rw, cy), (cx - rw * 0.92, cy + rh * 1.1), (cx - rw * 0.55, cy + rh * 1.9),
                                    (cx, cy + rh * 2.05), (cx + rw * 0.55, cy + rh * 1.9), (cx + rw * 0.92, cy + rh * 1.1),
                                    (cx + rw, cy)], 60)]), smooth=True)
    foot = p.rect(cx - rw * 0.38, cy + rh * 1.95, cx + rw * 0.38, cy + rh * 2.25)
    rim = p.ellipse(cx, cy, rw, rh * 0.55)
    rice = p.ellipse(cx, cy - rh * 0.15, rw * 0.9, rh * 0.75) * (p.YY < cy + rh * 0.3)
    p.form(np.clip(body + foot, 0, 1) * (1 - rim), bowl, p.contour(body, 10, 90), LIGHT, length=(14, 30),
           width=(1.5, 2.2), density=1.3, warm='butter', avoid=avoid, seed=S.sd())
    for k in range(3):                                  # a painted band on the bowl
        y = cy + rh * (0.75 + k * 0.18)
        p.line(curve([(cx - rw * 0.92, y), (cx, y + rh * 0.35), (cx + rw * 0.92, y)], 30), 'cornflower', 2.0, 0.6, alpha=0.6)
    p.form(rim * (1 - rice), ('cream', 'ivory', 'sand'), 0, LIGHT, length=(10, 22), density=1.0, seed=S.sd())
    p.form(rice, ('white', 'cream', 'ivory', 'sand'), p.radial(cx, cy - rh * 0.2), LIGHT, length=(6, 14), width=(1.4, 2.0),
           density=1.2, warm='butter', seed=S.sd())
    ys, xs = np.nonzero(rice > 0.6)
    pick = S.r.choice(len(xs), min(len(xs), 260), replace=False)
    paths = [[(xs[i] - 3, ys[i]), (xs[i] + 3, ys[i] - 1)] for i in pick]
    p.strokes(paths, ['sand', 'ivory'], width=2.0, pressure=0.6, opacity=0.4, alpha=0.6)
    p.edge(np.clip(body + foot, 0, 1), 'slate', density=0.7)
    p.edge(rim, 'sand', density=0.5)
    if steam:
        paths = []
        for k in range(3):
            x0 = cx - rw * 0.35 + k * rw * 0.35
            paths.append(curve([(x0, cy - rh * 0.6), (x0 - 18, cy - rh * 1.4), (x0 + 16, cy - rh * 2.2), (x0 - 8, cy - rh * 3.0)], 40))
        p.strokes(paths, 'white', width=7.0, pressure=0.55, opacity=0.8, alpha=0.55)
        p.strokes(paths, 'cream', width=3.0, pressure=0.6, opacity=0.8, alpha=0.6)
    return np.clip(body + foot + rim, 0, 1)


def person(S, x, y, R, coat=('peach', 'coral', 'terracotta', 'brick'), hair=('hair_light', 'hair', 'umber'),
           hair_style='bob', eyes_closed=False, look=(0.0, 0.0), smile=True, arms=None, plan=False, grey=False, field=80, cut=None, hands=True, cut_head=False):
    """a storybook adult/child: round head (radius R) at (x, y), soft coat body below. Returns masks."""
    p = S.p
    head = p.ellipse(x, y, R * 0.9, R)
    neck = p.rect(x - R * 0.25, y + R * 0.7, x + R * 0.25, y + R * 1.15)
    body = p.poly(curve([(x - R * 0.5, y + R * 0.95), (x - R * 1.15, y + R * 1.45), (x - R * 1.45, y + R * 3.6),
                         (x + R * 1.45, y + R * 3.6), (x + R * 1.15, y + R * 1.45), (x + R * 0.5, y + R * 0.95)], 60), smooth=True)
    if hair_style == 'bob':
        hm = p.ellipse(x, y - R * 0.18, R * 1.02, R * 0.98) * (1 - p.ellipse(x, y + R * 0.38, R * 0.8, R * 0.78) * (p.YY > y - R * 0.3))
    elif hair_style == 'long':                          # a bob that carries on down to the shoulders at the sides
        top = p.ellipse(x, y - R * 0.18, R * 1.02, R * 0.98) * (1 - p.ellipse(x, y + R * 0.38, R * 0.8, R * 0.78) * (p.YY > y - R * 0.3))
        side = p.blob(x, y + R * 0.55, R * 1.08, R * 1.15, 0.05) * (p.YY < y + R * 1.55)
        side = side * np.maximum((np.abs(p.XX - x) > R * 0.66).astype(np.float32), (p.YY < y - R * 0.2).astype(np.float32))
        hm = np.maximum(top, side)
    elif hair_style == 'short':
        hm = p.ellipse(x, y - R * 0.3, R * 0.96, R * 0.82) * (p.YY < y - R * 0.15)
    elif hair_style == 'bun':
        hm = np.maximum(p.ellipse(x, y - R * 0.3, R * 0.95, R * 0.8) * (p.YY < y - R * 0.2), p.ellipse(x, y - R * 1.05, R * 0.42, R * 0.36))
    else:
        hm = np.zeros((H, W), np.float32)
    armm = np.zeros((H, W), np.float32)
    for a in (arms or []):
        armm = np.maximum(armm, p.tube(a, R * 0.36, R * 0.3))
    if cut is not None:
        body = body * (1 - cut); armm = armm * (1 - cut)
        if cut_head:
            head = head * (1 - cut); neck = neck * (1 - cut); hm = hm * (1 - cut)
    mask = np.clip(head + neck + body + hm + armm, 0, 1)
    if plan: return dict(mask=mask, head=head, body=body)
    p.form(body, coat, field, LIGHT, length=(18, 40), density=1.3, warm='butter', cool='lavender', seed=S.sd())
    if arms:
        p.form(armm, coat, p.contour(armm, 8, 90), LIGHT, length=(12, 26), density=1.2, warm='butter', seed=S.sd())
        for a in (arms if hands else []):
            hx, hy = a[-1]
            hand = p.ellipse(hx, hy, R * 0.2, R * 0.18)
            p.form(hand, SKIN, 0, LIGHT, length=(6, 12), density=1.2, seed=S.sd())
    p.form(np.clip(head + neck, 0, 1) * (1 - hm), SKIN, p.contour(head, 8), LIGHT, length=(8, 18), width=(1.4, 2.0),
           density=1.3, warm='peach', seed=S.sd())
    if hm.max() > 0.3:
        hc = ('stone', 'warmgrey', 'pebble') if grey else hair
        p.form(hm, hc, p.radial(x, y - R * 1.2, 90), LIGHT, length=(14, 30), width=(1.4, 2.0), density=1.5, seed=S.sd())
    p.edge(head * (1 - hm), 'skin_shade', density=0.6)
    ey = y + R * 0.12
    for sgn in (-1, 1):
        ex = x + sgn * R * 0.34
        if eyes_closed:
            p.line(curve([(ex - R * 0.12, ey), (ex, ey + R * 0.07), (ex + R * 0.12, ey)], 12), 'umber', 2.4, 0.8, alpha=0.9)
        else:
            p.eye(ex, ey, max(3.0, R * 0.075), look=look)
        p.blush(x + sgn * R * 0.55, y + R * 0.4, R * 0.2, amount=0.7)
    if smile:
        p.line(curve([(x - R * 0.14, y + R * 0.52), (x, y + R * 0.6), (x + R * 0.14, y + R * 0.52)], 12), 'brick', 2.4, 0.8, alpha=0.9)
    return dict(mask=mask, head=head, body=body)
