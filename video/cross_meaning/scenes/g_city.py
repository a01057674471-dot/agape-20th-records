"""G. 私たちの罪を赦すために: today, a rainy crossing in a Japanese city at dusk -- people under umbrellas, each
on their own way; one small person without an umbrella looks up. The 'us' the cross was for."""
from common import *

def main(out, stages=None):
    b = page(701, stages)
    blds = [(40, 300, 300, 1150, 'blue'), (300, 520, 560, 1150, 'cobalt'), (560, 380, 800, 1150, 'teal'), (800, 600, 1040, 1150, 'blue')]
    peeps, umbs = [], []
    spec = [(200, 1290, 44, 'cobalt', 'coral'), (420, 1340, 48, 'navy', 'mustard'), (650, 1300, 42, 'teal', 'powder'),
            (860, 1350, 46, 'cobalt', 'coral'), (300, 1560, 56, 'deep', 'mustard'), (760, 1580, 58, 'navy', 'coral')]
    for i, (x, y, R, c, uc) in enumerate(spec):
        peeps.append(Figure(b, x, y, R, coat=c, hair='short' if i % 2 else 'long', seed=10 + i, mouth='hmm',
                            arms=[[(x + R * 0.5, y + R * 1.4), (x + R * 0.55, y + R * 0.6), (x + R * 0.1, y - R * 0.7)]]))
        umbs.append((b.poly([(x - R * 2.0, y - R * 1.05), (x, y - R * 2.4), (x + R * 2.0, y - R * 1.05)]), uc, x, y, R))
    kid = Figure(b, 540, 1640, 50, coat='coral', hair='short', look=(0, -1), mouth='o', seed=30,
                 arms=[[(515, 1710), (500, 1780), (512, 1830)], [(565, 1710), (580, 1780), (568, 1830)]])
    figs = peeps + [kid]
    front = union(*[p.mask for p in figs], *[u[0] for u in umbs])
    b.block((40, 50, 1040, 1870), 'powder', rough=10, corner=30, avoid=front, halo=3, seed=11)
    for x0, y0, x1, y1, c in blds:
        b.fill(b.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], smooth=False) * (1 - front), c, pressure=0.95, angle=80, seed=x0)
    road = (YY > 1150) * (YY < 1870)
    b.fill(road.astype(np.float32) * (1 - front), 'cornflower', pressure=0.9, angle=2, seed=12)
    for k in range(7):
        x0 = 80 + k * 140
        b.fill(b.poly([(x0, 1440), (x0 + 80, 1440), (x0 + 90, 1500), (x0 - 10, 1500)], smooth=False) * (1 - front), 'mist',
               pressure=0.85, angle=0, slip=0, seed=13 + k)
    people_phase(figs, 'blue')
    b.stage('blue')
    for x0, y0, x1, y1, c in blds:
        b.outline([(x0, y1), (x0, y0), (x1, y0), (x1, y1)], 4, closed=False, smooth=False, seed=x0 + 1)
        for r_ in range(int((y1 - y0 - 60) / 110)):
            for c_ in range(2):
                wx, wy = x0 + 40 + c_ * (x1 - x0 - 120) / 1.5, y0 + 40 + r_ * 110
                b.outline([(wx, wy), (wx + 60, wy), (wx + 60, wy + 60), (wx, wy + 60)], 2.6, smooth=False, seed=int(wx + wy))
    for (m, uc, x, y, R) in umbs:
        b.outline([(x - R * 2.0, y - R * 1.05), (x, y - R * 2.4), (x + R * 2.0, y - R * 1.05)], 3.6, seed=int(x) + 3)
    people_phase(figs, 'ink')
    b.stage('ink')
    for x0, y0, x1, y1, c in blds:
        if c == 'teal':
            b.scribble(b.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], smooth=False) * (XX > x1 - 70) * (1 - front),
                       width=4, spacing=5, angle=80, colour='navy', seed=x0 + 5)
    people_phase(figs, 'dark')
    b.stage('dark')
    for (m, uc, x, y, R) in umbs:
        b.fill(m, uc, pressure=0.95, angle=-20, seed=int(x) + 7)
    for x0, y0, x1, y1, c in blds:
        for r_ in range(int((y1 - y0 - 60) / 110)):
            if (r_ + x0) % 3: continue
            wx, wy = x0 + 40, y0 + 40 + r_ * 110
            b.fill(b.poly([(wx, wy), (wx + 60, wy), (wx + 60, wy + 60), (wx, wy + 60)], smooth=False), 'butter', pressure=0.9, slip=0, seed=int(wy))
    people_phase(figs, 'accents')
    b.stage('accents')
    b.rain((60, 60, 1020, 1860), n=700, angle=82, length=(12, 34), width=(1.6, 2.8), colour='deep',
           avoid=union(*[u[0] for u in umbs]), seed=41)
    b.rain((60, 60, 1020, 1860), n=320, angle=82, length=(12, 28), width=(1.6, 2.6), colour='chalk',
           avoid=union(*[u[0] for u in umbs]), seed=42)
    for (m, uc, x, y, R) in umbs:
        b.splash(x, y - R * 2.3, 10, 'chalk', n=4, seed=int(x))
    for k in range(5):
        b.splash(520 + k * 10, 1590, 8, 'chalk', n=3, seed=60 + k)
    b.stage('rain')
    finish(b, out, stages)
