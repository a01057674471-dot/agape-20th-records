"""helpers for the kintsugi reel: the chawan (tea bowl), its cracks, the person's 'heart cracks'"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cross_meaning', 'scenes'))
from common import *      # noqa

GOLD, GOLD_HI = '#d9a43a', '#fff0b0'


def bowl_pts(cx, cy, w, h):
    """side view of a chawan: rim at cy, body down to the foot ring"""
    pts = [(cx - w / 2, cy)]
    for t in np.linspace(0, 1, 14):
        a = np.pi * t
        pts.append((cx - w / 2 * np.cos(a) * (1 - 0.12 * np.sin(a) ** 2), cy + h * 0.86 * np.sin(a) ** 0.45))
    foot = [(cx + w * 0.2, cy + h * 0.78), (cx + w * 0.2, cy + h), (cx - w * 0.2, cy + h), (cx - w * 0.2, cy + h * 0.78)]
    return np.array(pts[1:], np.float32), np.array(foot, np.float32)


def crack_paths(cx, cy, w, h, seed=0, n=3):
    """jagged cracks running from the rim down the body; returned as lists of (x, y)"""
    r = np.random.default_rng(seed)
    out = []
    for k in range(n):
        x0 = cx + (k - (n - 1) / 2) * w * 0.28 + r.uniform(-20, 20)
        pts = [(x0, cy + 4)]
        y = cy + 4
        x = x0
        steps = int(r.integers(5, 8))
        for s in range(steps):
            y += h * 0.8 / steps * r.uniform(0.7, 1.2)
            x += r.uniform(-30, 30)
            u = np.clip((x - cx) / (w / 2), -0.92, 0.92)            # stay inside the body's curve
            ymax = cy + h * 0.86 * np.sqrt(max(1 - u * u, 0)) ** 0.45 - 14
            x = cx + u * w / 2
            pts.append((x, min(y, ymax)))
            if y >= ymax: break
        out.append(pts)
        if k == 1:                                     # one crack branches
            j = len(pts) // 2
            bx, by = pts[j]
            out.append([(bx, by), (bx + r.uniform(30, 60), by + r.uniform(20, 50)), (bx + r.uniform(60, 110), by + r.uniform(50, 90))])
    return out


def bowl(b, cx, cy, w, h, glaze='cornflower', cracks=None, seed=0, shadow=True):
    body, foot = bowl_pts(cx, cy, w, h)
    m = b.poly(body, smooth=False)
    mf = b.poly(foot, smooth=False)
    inside = b.ellipse(cx, cy, w / 2, h * 0.12)
    full = union(m, mf, inside)
    if shadow:
        b.fill(b.ellipse(cx + 20, cy + h + 10, w * 0.5, h * 0.09), 'slate', pressure=0.5, slip=0, lanes=0, seed=seed + 1)
    b.fill(union(m, mf) * (1 - inside), glaze, pressure=0.96, angle=80, seed=seed + 2)
    b.fill(union(m, mf) * smoothstep(cx + w * 0.05, cx + w * 0.45, XX), 'deep', pressure=0.8, angle=80, slip=0, seed=seed + 3)
    b.fill(inside, 'navy', pressure=0.95, angle=0, slip=0, seed=seed + 4)
    b.fill(mf, 'slate', pressure=0.9, angle=0, slip=0, seed=seed + 5)
    b.outline(body, 4.4, closed=False, smooth=False, open_=0.4, seed=seed + 6)
    b.outline(circle_pts(cx, cy, w / 2, h * 0.12, n=36), 4.0, seed=seed + 7)
    b.outline(foot, 3.4, closed=False, smooth=False, seed=seed + 8)
    b.chalk([[(cx - w * 0.36, cy + h * 0.2), (cx - w * 0.3, cy + h * 0.6)]], width=8, pressure=0.6, seed=seed + 9)
    b.chalk([[(cx - w * 0.4, cy - h * 0.04), (cx - w * 0.1, cy - h * 0.1)]], width=5, pressure=0.6, seed=seed + 10)
    for p in (cracks or []):
        b.ink(p, 2.6, colour=INK, dry=0.1, taper=(0.05, 0.4), seed=seed + 11 + int(p[0][0]))
    return full


def heart_cracks(x, y, s=1.0, seed=0):
    """small jagged cracks over the chest of a figure (x, y = centre of the chest)"""
    r = np.random.default_rng(seed)
    out = []
    for k, (a0, L) in enumerate(((-100, 90), (-30, 80), (200, 70), (60, 60))):
        pts = [(x, y)]
        ang = np.deg2rad(a0)
        px, py = x, y
        for st in range(4):
            ang += np.deg2rad(r.uniform(-35, 35))
            px += np.cos(ang) * L * s / 4 * r.uniform(0.8, 1.3); py += np.sin(ang) * L * s / 4 * r.uniform(0.8, 1.3)
            pts.append((px, py))
        out.append(pts)
    return out


def hand(b, x, y, s, angle, skin=SKIN, fingers=4, spread=6.0, curl=0.0, thumb=True, seed=0):
    """a picture-book hand: an oval palm and rounded fingers along `angle` (degrees); filled, then inked"""
    a = np.deg2rad(angle); ux, uy = np.cos(a), np.sin(a); vx, vy = -uy, ux
    parts = [('e', (x, y, 46 * s, 40 * s, angle))]
    for i in range(fingers):
        o = (i - (fingers - 1) / 2) * 22 * s
        da = np.deg2rad((i - (fingers - 1) / 2) * spread)
        fx, fy = np.cos(a + da), np.sin(a + da)
        L = (60 if i in (1, 2) else 50) * s
        bx, by = x + ux * 30 * s + vx * o, y + uy * 30 * s + vy * o
        mx, my = bx + fx * L * 0.55, by + fy * L * 0.55
        tx, ty = bx + fx * L - vx * curl * 12 * s, by + fy * L - vy * curl * 12 * s
        parts.append(('t', [(bx, by), (mx, my), (tx, ty)], 20 * s, 16 * s))
    if thumb:
        bx, by = x + vx * 38 * s, y + vy * 38 * s
        parts.append(('t', [(bx, by), (bx + (ux * 0.7 + vx * 0.5) * 42 * s, by + (uy * 0.7 + vy * 0.5) * 42 * s)], 22 * s, 17 * s))
    m = np.zeros((H, W), np.float32)
    for p in parts:
        m = np.maximum(m, b.ellipse(*p[1][:4], rot=p[1][4]) if p[0] == 'e' else b.band(p[1], p[2], p[3]))
    b.fill(m, skin, pressure=0.7, lanes=0, seed=seed + 1)
    for k, p in enumerate(parts):
        if p[0] == 'e':
            cx, cy, rx, ry, rot = p[1]
            t = np.deg2rad(np.linspace(0, 360, 30)); r_ = np.deg2rad(rot)
            pts = np.stack([cx + rx * np.cos(t) * np.cos(r_) - ry * np.sin(t) * np.sin(r_),
                            cy + rx * np.cos(t) * np.sin(r_) + ry * np.sin(t) * np.cos(r_)], 1)
            b.outline(pts, 3.4 * max(s, 0.8), open_=0.5, seed=seed + 10 + k)
        else:
            b.outline(BlueBook.tube(p[1], p[2], p[3]), 3.0 * max(s, 0.8), open_=0.5, seed=seed + 10 + k)
    return m
