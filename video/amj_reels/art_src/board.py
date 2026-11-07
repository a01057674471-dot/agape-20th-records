"""collage boards: a soft-blue painted block on white paper, little doodles (flowers, stars, a tiny cross, a
paper plane) only round the edges, the middle left clear for the photos."""
import sys
from common_amj import *

def main(out, seed, colour):
    seed = int(seed)
    b = page(1500 + seed)
    b.block((40, 50, 1040, 1870), colour, rough=12, corner=30, seed=11 + seed)
    r = np.random.default_rng(seed)
    edge = [(r.uniform(70, 1010), r.choice([r.uniform(80, 230), r.uniform(1640, 1840)])) for _ in range(10)] + \
           [(r.choice([r.uniform(70, 130), r.uniform(950, 1010)]), r.uniform(250, 1600)) for _ in range(8)]
    for k, (x, y) in enumerate(edge):
        kind = k % 4
        if kind == 0:
            b.ink([(x, y + 6), (x + r.uniform(-4, 4), y + 34)], 2.2, seed=seed * 100 + k)
            b.flower(x, y, r.uniform(9, 13), ['coral', 'cheek', 'mustard'][k % 3], seed=seed * 100 + k)
        elif kind == 1:
            for a in range(4):
                t = np.deg2rad(a * 45)
                b.ink([(x - 12 * np.cos(t), y - 12 * np.sin(t)), (x + 12 * np.cos(t), y + 12 * np.sin(t))], 2.4, colour='mustard', seed=seed * 100 + k * 5 + a)
        elif kind == 2:
            b.dot(x, y, r.uniform(4, 7), colour='chalk', medium='chalk')
        else:
            b.ink([(x, y - 14), (x, y + 14)], 3, seed=seed * 100 + k); b.ink([(x - 9, y - 5), (x + 9, y - 5)], 3, seed=seed * 100 + k + 1)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=700, size=(0.5, 1.4), seed=seed + 7)
    finish(b, out)

if __name__ == '__main__':
    main(*sys.argv[1:4])
