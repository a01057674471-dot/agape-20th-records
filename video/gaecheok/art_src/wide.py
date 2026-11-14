"""16:9 helpers: the warm coloured-pencil shots at 1920 x 1080 for the YouTube film."""
import os, sys, importlib.util
from tcommon import *
import pcommon
W, H = 1920, 1080
pcommon.W, pcommon.H = W, H
pcommon.ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art')

def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), rel))
    m = importlib.util.module_from_spec(sp); sys.path.insert(0, os.path.dirname(sp.origin)); sp.loader.exec_module(m); return m
h = _load('h_shots', '../../handle/art_src/shots.py')
k = h.k
pcommon.W, pcommon.H = W, H
pcommon.ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art')
erase, figure, ground, ridge, RIDGES, hand, SKIN4, heart_mask = k.erase, k.figure, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4, h.heart_mask
PASTOR = ('slate', 'indigo', 'umber', 'sepia')
WIFE = ('peach', 'coral', 'terracotta', 'brick')
COATS = [('powder', 'cornflower', 'denim', 'indigo'), ('butter', 'ochre', 'amber', 'sienna'), ('sage', 'lichen', 'moss', 'pine'),
         ('lavender', 'periwinkle', 'violet', 'indigo'), ('pink', 'rose', 'coral', 'brick'), ('sand', 'tan', 'sienna', 'brown'),
         ('cream', 'ivory', 'sand', 'tan'), ('stone', 'warmgrey', 'slate', 'umber')]
HAIR = ('hair', 'umber', 'sepia')
WOODC = ('tan', 'sienna', 'brown', 'umber')


def sky(S, y1, sun=None, dusk=False, night=False):
    p = S.p
    m = (p.YY < y1).astype(np.float32)
    if night:
        p.hatch(m, p.flow(-3, 4), ['indigo', 'ultramarine', 'slate'], (60, 150), (1.8, 2.6), 1.8, 0.8, seed=S.sd())
        p.hatch(m * p.value(0.0, 1.0, 0, y1), p.flow(-2, 4), ['violet', 'cobalt', 'periwinkle'], (60, 140), (1.8, 2.4), 1.0, 0.7, alpha=0.6, seed=S.sd())
    elif dusk:
        p.hatch(m, p.flow(-3, 4), ('dusk_sky', np.clip(p.value(0.0, 1.0, 0, y1) * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.8, 0.76, seed=S.sd())
        p.hatch(m * smoothstep(y1 * 0.4, y1, p.YY), p.flow(-3, 4), ['peach', 'apricot', 'rose'], (60, 140), (1.8, 2.4), 1.0, 0.66, alpha=0.55, seed=S.sd())
    else:
        morning_sky(S, m)
    if sun: p.glow(sun[0], sun[1], sun[2], strength=1.0, density=1.0)
    return m


def stars(S, region, n=80, seed=1):
    p = S.p; r = np.random.default_rng(seed); k_ = 0
    while k_ < n:
        x, y = r.uniform(20, W - 20), r.uniform(20, H - 20)
        if region[int(y), int(x)] < 0.5: continue
        s = r.uniform(2, 4.5); p.lift(p.ellipse(x, y, s, s), 'cream', r.uniform(0.6, 0.95), tooth=0.2); k_ += 1


def wall(S, y1=H, cols=('cream', 'ivory', 'apricot')):
    p = S.p
    w = (p.YY < y1).astype(np.float32)
    p.hatch(w, p.flow(2, 4, 500), list(cols), (60, 140), (1.8, 2.5), 1.6, 0.6, alpha=0.65, seed=S.sd())
    return w


def floor(S, y0, cols=('sand', 'tan', 'sienna', 'brown')):
    p = S.p
    f = (p.YY >= y0).astype(np.float32)
    p.form(f, cols, 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    return f


def bust(S, x, y, R, coat, hs='short', hair=HAIR, **kw):
    """a person (head + shoulders) painted opaque over whatever is behind"""
    m = person(S, x, y, R, coat=coat, hair_style=hs, plan=True, arms=kw.get('arms'))
    erase(S, m['mask'])
    person(S, x, y, R, coat=coat, hair_style=hs, hair=hair, **kw)
    return m['mask']


def building(S, x0, x1, top, base, cols=('cream', 'sand', 'tan', 'sienna'), floors=3, lit=0.5, sign=True):
    p = S.p
    b = p.rect(x0, top, x1, base)
    erase(S, b); p.form(b, cols, 90, LIGHT, length=(30, 70), density=1.4, seed=S.sd()); p.edge(b, 'sepia', density=0.8, alpha=0.8)
    fh = (base - top) / floors
    for f in range(floors):
        for xx in np.arange(x0 + 30, x1 - 90, 120):
            p.window(xx, top + f * fh + fh * 0.25, xx + 80, top + f * fh + fh * 0.75, panes=(2, 1), glow=lit, seed=S.sd())
    return b


def tower_cross(S, x, top, s=1.0, glow=True):
    """the rooftop bell tower with its cross"""
    p = S.p
    tw = np.clip(p.rect(x - 22 * s, top + 60 * s, x + 22 * s, top + 260 * s) + p.poly([(x - 40 * s, top + 70 * s), (x, top + 20 * s), (x + 40 * s, top + 70 * s)]), 0, 1)
    erase(S, tw); p.form(tw, ('cream', 'stone', 'warmgrey', 'slate'), 90, LIGHT, density=1.5, seed=S.sd()); p.edge(tw, 'sepia', density=0.8, alpha=0.8)
    cr = np.clip(p.rect(x - 5 * s, top - 50 * s, x + 5 * s, top + 22 * s) + p.rect(x - 22 * s, top - 32 * s, x + 22 * s, top - 22 * s), 0, 1)
    p.form(cr, ('red', 'vermilion', 'brick') if glow else ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.7, seed=S.sd())
    if glow: p.glow(x, top - 15 * s, 60 * s, colours=['rose', 'coral', 'cream'], strength=0.7, density=0.7)
