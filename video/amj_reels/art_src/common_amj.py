"""helpers for the AMJ reel's blue picture-book art; reuses the cross_meaning helpers"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cross_meaning', 'scenes'))
from common import *          # noqa: F401,F403  (BlueBook, page, finish, Figure, XX, YY, ...)

# Japan and the tip of Korea from rough real coastlines (lon, lat), north up, filling the middle of the page
def P(lon, lat):
    return (40 + (lon - 125.8) * 49.0, 1350 - (lat - 30.8) * 56.0)

KYUSHU = [(129.7, 33.3), (130.4, 33.95), (131.0, 33.95), (131.6, 33.4), (131.9, 32.6), (131.4, 31.4), (130.7, 31.0),
          (130.2, 31.4), (130.1, 32.1), (130.4, 32.7), (129.8, 32.8), (129.6, 33.1)]
SHIKOKU = [(132.5, 33.0), (132.4, 33.6), (133.0, 34.15), (134.1, 34.35), (134.7, 34.0), (134.3, 33.6), (133.6, 33.4), (133.0, 32.8)]
HONSHU = [(130.9, 34.0), (131.5, 34.6), (132.8, 35.3), (133.8, 35.5), (135.2, 35.7), (136.0, 35.9), (136.7, 36.8),
          (137.3, 37.5), (137.0, 36.9), (138.3, 37.2), (139.2, 38.0), (139.8, 39.0), (140.0, 40.0), (139.9, 40.6),
          (140.6, 41.2), (141.4, 41.4), (141.5, 40.5), (141.9, 39.5), (141.5, 38.3), (141.0, 37.8), (140.9, 36.9),
          (140.6, 35.7), (140.1, 35.0), (139.8, 35.2), (139.2, 35.2), (138.8, 34.7), (138.2, 34.6), (137.3, 34.6),
          (136.9, 34.3), (136.3, 34.0), (135.8, 33.5), (135.2, 33.9), (135.3, 34.5), (134.5, 34.7), (133.3, 34.4),
          (132.4, 34.2), (131.2, 33.95)]
HOKKAIDO = [(140.0, 41.5), (140.3, 42.5), (139.8, 42.8), (140.5, 43.2), (141.4, 43.3), (141.7, 44.3), (141.9, 45.4),
            (142.9, 44.6), (144.3, 44.1), (145.3, 44.3), (145.5, 43.3), (144.3, 42.9), (143.3, 42.0), (141.7, 42.6), (141.0, 41.7)]
KOREA = [(125.2, 34.2), (126.3, 34.4), (127.5, 34.7), (128.6, 34.9), (129.3, 35.3), (129.5, 36.0), (129.4, 37.0),
         (128.6, 38.0), (127.5, 39.0), (125.2, 39.4)]
CITIES = {k: P(*v) for k, v in {'도쿄': (139.7, 35.7), '후쿠오카': (130.4, 33.6), '교토': (135.8, 35.0), '고베': (135.2, 34.7),
                                 '아키타': (140.1, 39.7), '미토': (140.5, 36.4), '오사카': (135.5, 34.7), '센다이': (140.9, 38.3),
                                 '삿포로': (141.35, 43.06), '나고야': (136.9, 35.2), '히로시마': (132.5, 34.4)}.items()}
OUTLINES = {k: [P(*q) for q in v] for k, v in dict(hon=HONSHU, kyu=KYUSHU, shi=SHIKOKU, hok=HOKKAIDO, kor=KOREA).items()}


def islands(b):
    M = {k: b.poly(v, smooth=True) for k, v in OUTLINES.items()}
    M['kor'] = M['kor'] * smoothstep(52, 60, XX)
    M['japan'] = np.maximum.reduce([M['hon'], M['kyu'], M['shi'], M['hok']])
    return M


def mask_outline(b, m, width=4.0, seed=0, colour=INK):
    """ink the contour of a mask with a loose line (via its largest contour)"""
    from PIL import Image
    import numpy as _np
    ys, xs = _np.nonzero(m > 0.5)
    if not len(xs): return
    # march round the boundary by angle from the centroid (fine for these blob-like islands)
    cx, cy = xs.mean(), ys.mean()
    edge = (m > 0.5) & ~((_np.roll(m, 1, 0) > 0.5) & (_np.roll(m, -1, 0) > 0.5) & (_np.roll(m, 1, 1) > 0.5) & (_np.roll(m, -1, 1) > 0.5))
    ey, ex = _np.nonzero(edge)
    ang = _np.arctan2(ey - cy, ex - cx)
    o = _np.argsort(ang)
    pts = _np.stack([ex[o], ey[o]], 1)[::6].astype(_np.float32)
    b.outline(pts, width, seed=seed, colour=colour)
