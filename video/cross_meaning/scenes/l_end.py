"""L. end card ground: a quiet soft-blue page with a small cross and a few flowers along the bottom."""
from common import *

def main(out, stages=None):
    b = page(1201, stages)
    b.block((40, 50, 1040, 1870), 'mist', rough=10, corner=30, seed=11)
    cm = cross_mask(b, 540, 1330, 260, w=160, t=24)
    b.fill(cm, '#8a7a70', pressure=0.97, slip=0, medium='gouache', seed=12)
    cross_ink(b, 540, 1330, 260, w=160, t=24, width=3.6, seed=13)
    r = np.random.default_rng(14)
    b.blades(60, 1020, lambda x: 1700, n=60, height=(30, 80), width=3.6, seed=15)
    for k in range(40):
        x = r.uniform(80, 1000); y = r.uniform(1600, 1800)
        b.ink([(x, y + 4), (x, y + 30)], 2, seed=20 + k)
        b.flower(x, y, r.uniform(8, 12), ['coral', 'cheek', 'mustard'][k % 3], seed=100 + k)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=16)
    finish(b, out, stages)
