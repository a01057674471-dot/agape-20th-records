"""kintsugi gold: raised, polished gold beads grown along crack lines (order <= u), and the thin dark cracks
before the gold reaches them. Seams are always clipped to their own object (the bowl, or her coat)."""
import os
import numpy as np
from scipy import ndimage as ndi
from PIL import Image
from core_noise import noise2d

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, '..', 'art')


class Seams:
    def __init__(self, crack, order, clip, width=2, seed=5):
        self.crack, self.clip = crack, clip > 0.5
        self.thick = ndi.binary_dilation(crack, iterations=width) & self.clip
        idx = ndi.distance_transform_edt(~crack, return_distances=False, return_indices=True)
        self.order = order[idx[0], idx[1]]
        self.spark = (np.random.default_rng(seed).random(crack.shape) < 0.004) & self.thick
        self.cache = {}

    def dark(self, colour=(16, 24, 40), alpha=0.9):
        a = ndi.gaussian_filter(self.crack.astype(np.float32), 0.6)
        rgba = np.zeros(self.crack.shape + (4,), np.float32)
        rgba[..., :3] = np.array(colour, np.float32) / 255
        rgba[..., 3] = np.clip(a * 1.6, 0, 1) * alpha * self.clip
        return Image.fromarray((rgba * 255).astype(np.uint8), 'RGBA')

    def gold(self, u, tip=True):
        u = round(float(u), 3)
        if u <= 0: return None
        if u in self.cache: return self.cache[u]
        grow = (self.order <= u) & self.thick
        a = ndi.gaussian_filter(grow.astype(np.float32), 0.8)
        hgt = ndi.gaussian_filter(grow.astype(np.float32), 1.6)
        gy, gx = np.gradient(hgt)
        lit = np.clip(0.5 + (gx * 0.6 + gy * 0.8) * 6.0, 0, 1)
        base = np.array([205, 150, 52], np.float32) / 255
        hi = np.array([255, 236, 170], np.float32) / 255
        lo = np.array([150, 100, 30], np.float32) / 255
        k = np.abs(lit - 0.5)[..., None] * 2
        col = base * (1 - k) + np.where(lit[..., None] > 0.5, hi, lo) * k
        col[self.spark & grow] = 1.0
        glow = ndi.gaussian_filter(grow.astype(np.float32), 6) * 0.35
        if tip and u < 1:
            front = (self.order <= u) & (self.order > u - 0.03) & self.thick
            glow = glow + ndi.gaussian_filter(front.astype(np.float32), 8) * 2.5
        glow = np.clip(glow, 0, 0.8) * self.clip
        ga = glow[..., None]; ca = np.clip(a * 1.3, 0, 1)[..., None]
        gcol = np.array([255, 226, 140], np.float32) / 255
        out_a = ca + ga * (1 - ca)
        out_c = (col * ca + gcol * ga * (1 - ca)) / np.maximum(out_a, 1e-4)
        im = Image.fromarray((np.clip(np.dstack([out_c, out_a]), 0, 1) * 255).astype(np.uint8), 'RGBA')
        self.cache[u] = im
        return im


def flow_order(crack, start):
    """geodesic distance along the crack from the start pixels, normalised to 0..1"""
    order = np.full(crack.shape, np.inf, np.float32)
    reached = start & crack
    if not reached.any():
        ys, xs = np.nonzero(crack); reached = np.zeros_like(crack); reached[ys[0], xs[0]] = True
    order[reached] = 0; k = 0
    while True:
        k += 1
        nxt = ndi.binary_dilation(reached, structure=np.ones((3, 3), bool)) & crack & ~reached
        if not nxt.any(): break
        order[nxt] = k; reached |= nxt
    order[crack & ~reached] = k
    order[np.isinf(order)] = 0
    return order / max(order.max(), 1)


def heart_seams(coat, cx, cy, r=95, seed=11):
    """a small break over her heart: a noisy Voronoi of a few shards inside a circle, clipped to her coat;
    the gold flows out from the middle"""
    H, W = coat.shape
    YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
    rng = np.random.default_rng(seed)
    region = (((XX - cx) ** 2 + (YY - cy) ** 2) < r * r) & (coat > 0.5)
    seeds = [(cx + np.cos(a) * r * 0.62, cy + np.sin(a) * r * 0.62) for a in np.linspace(0, 2 * np.pi, 5, endpoint=False) + rng.uniform(0, 1)]
    seeds.append((cx + rng.uniform(-8, 8), cy + rng.uniform(-8, 8)))
    n1 = noise2d(H, W, 30, 3, seed) - 0.5; n2 = noise2d(H, W, 30, 3, seed + 1) - 0.5
    WX, WY = XX + 30 * n1, YY + 30 * n2
    d = np.stack([(WX - sx) ** 2 + (WY - sy) ** 2 for sx, sy in seeds])
    label = (np.argmin(d, 0) + 1) * region
    edge = np.zeros_like(region)
    for dy, dx in ((0, 1), (1, 0)):
        sh = np.roll(np.roll(label, dy, 0), dx, 1)
        edge |= (label != sh) & (label > 0) & (sh > 0)
    # the outer rim of the circle is not a crack; the lines fade out before it
    edge &= ((XX - cx) ** 2 + (YY - cy) ** 2) < (r * 0.92) ** 2
    crack = ndi.binary_dilation(edge, iterations=1) & region
    start = ((XX - cx) ** 2 + (YY - cy) ** 2) < 30 ** 2
    return Seams(crack, flow_order(crack, start), coat, width=1, seed=seed)


_bowl = None
def bowl():
    global _bowl
    if _bowl is None:
        m = dict(np.load(os.path.join(ART, 'bowl_meta.npz')))
        im = Image.open(os.path.join(ART, 'bowl.png')).convert('RGBA')
        _bowl = dict(meta=m, im=im, seams=Seams(m['crack'], m['order'], m['all'], width=2))
    return _bowl


def bowl_image(u=0.0, cracks=True):
    B = bowl()
    im = B['im'].copy()
    if cracks: im.alpha_composite(B['seams'].dark())
    g = B['seams'].gold(u)
    if g is not None: im.alpha_composite(g)
    return im
