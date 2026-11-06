"""C. two thousand years ago: a bare hill outside a walled city under a heavy navy sky, three wooden crosses
standing empty and far away -- an execution place, shown quietly, nothing graphic."""
from common import *

def main(out, stages=None):
    b = page(301, stages)
    hill = b.poly([(40, 1870), (40, 1420), (250, 1270), (460, 1170), (640, 1160), (820, 1240), (1040, 1380), (1040, 1870)])
    crs = [(390, 870, 300), (560, 800, 360), (730, 880, 290)]
    cm = union(*[cross_mask(b, x, y, h, t=h * 0.08) for x, y, h in crs])
    wall = b.poly([(60, 1330), (60, 1250), (180, 1250), (180, 1200), (220, 1200), (220, 1250), (330, 1250), (330, 1290), (60, 1330)], smooth=False)
    b.block((40, 50, 1040, 1870), 'deep', rough=12, corner=30, avoid=cm, halo=2, seed=11)
    b.fill(b.poly([(40, 50), (1040, 50), (1040, 700), (40, 760)], smooth=False), 'navy', pressure=0.8, angle=-10, slip=0,
           avoid=cm, halo=2, seed=12)
    b.fill(wall, 'slate', pressure=0.95, angle=0, seed=13)
    b.fill(hill, 'blue', pressure=0.95, angle=-14, seed=14)
    b.fill(hill * (YY > 1500), 'cobalt', pressure=0.9, angle=-8, slip=0, seed=15)
    b.fill(cm, '#6a5a52', pressure=0.97, slip=0, loose=1.5, medium='gouache', seed=16)
    b.stage('blue')
    for (x, y, h) in crs:
        cross_ink(b, x, y, h, t=h * 0.08, width=4.4, seed=x)
        wood_grain(b, x, y, h, t=h * 0.08, seed=x + 1)
        b.ink([(x - 40, y + h), (x - 8, y + h - 10), (x + 30, y + h + 4)], 3.4, seed=x + 2)      # stones at the foot
    b.outline([(40, 1420), (250, 1270), (460, 1170), (640, 1160), (820, 1240), (1040, 1380)], 5.0, closed=False, seed=21)
    b.outline([(60, 1250), (180, 1250), (180, 1200), (220, 1200), (220, 1250), (330, 1250)], 3.6, closed=False, seed=22)
    for k in range(6):
        b.ink([(k * 22 + 70, 1250), (k * 22 + 70, 1236)], 2.6, seed=23 + k)
    b.stage('ink')
    b.scribble(hill * (YY > 1600), width=5.0, spacing=5.4, angle=80, colour='navy', dry=0.5, seed=31)
    b.blades(40, 1040, lambda x: 1640 + 20 * np.sin(x / 90), n=50, height=(30, 90), width=4.0, seed=32)
    b.stage('dark')
    b.stage('accents')
    for i, (x, y, w, h) in enumerate([(260, 300, 360, 120), (800, 420, 300, 100), (520, 560, 260, 80)]):
        b.chalk(b.cloud(x, y, w, h, 5, seed=40 + i), pressure=0.45, alpha=0.7, seed=40 + i)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=900, size=(0.5, 1.4), seed=45)
    b.spatter((60, 60, 1020, 1300), 'ink', n=40, size=(0.8, 3.0), seed=46)
    b.stage('chalk')
    finish(b, out, stages)
