"""a Christmas street in a Japanese city at night: a big lit tree, snow, shop windows, two young people with
shopping bags and a Santa hat -- a happy night, no idea whose birthday it is."""
import sys
from common_amj import *

def main(out):
    b = page(1401)
    tree = b.poly([(540, 380), (700, 760), (630, 760), (780, 1080), (690, 1080), (840, 1400), (240, 1400), (390, 1080),
                   (300, 1080), (450, 760), (380, 760)])
    trunk = b.poly([(505, 1400), (575, 1400), (575, 1470), (505, 1470)], smooth=False)
    a = Figure(b, 300, 1440, 70, coat='coral', hair='long', look=(0.6, -0.3), mouth='smile', seed=1, length=4.0,
               arms=[[(250, 1540), (230, 1640), (240, 1700)], [(350, 1540), (390, 1600), (420, 1640)]])
    c = Figure(b, 790, 1450, 72, coat='mustard', hair='short', look=(-0.6, -0.3), mouth='o', seed=2, length=4.0,
               arms=[[(740, 1550), (700, 1610), (670, 1640)], [(840, 1550), (860, 1650), (850, 1710)]])
    hat = b.poly([(735, 1400), (850, 1400), (800, 1300), (760, 1290)])
    bags = [b.poly([(200, 1690), (270, 1690), (275, 1790), (195, 1790)], smooth=False), b.poly([(820, 1700), (890, 1700), (895, 1800), (815, 1800)], smooth=False)]
    figs = [a, c]
    front = union(tree, trunk, a.mask, c.mask, hat, *bags)
    b.block((40, 50, 1040, 1870), 'deep', rough=12, corner=30, avoid=front, halo=3, seed=11)
    shops = [(40, 700, 230, 1400, 'cobalt'), (850, 650, 1040, 1400, 'blue')]
    for x0, y0, x1, y1, col in shops:
        b.fill(b.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], smooth=False) * (1 - front), col, pressure=0.95, angle=80, seed=x0)
    b.fill(tree, 'teal', pressure=0.95, angle=-70, seed=12)
    b.fill(tree * (XX > 560), 'navy', pressure=0.85, angle=-70, slip=0, seed=13)
    ground = (YY > 1500).astype(np.float32)
    b.fill(ground * (1 - front), 'powder', pressure=0.9, angle=2, seed=14)
    people_phase(figs, 'blue')
    b.stage('blue')
    b.outline([(540, 380), (700, 760), (630, 760), (780, 1080), (690, 1080), (840, 1400), (240, 1400), (390, 1080),
               (300, 1080), (450, 760), (380, 760)], 4.6, smooth=False, seed=21)
    b.outline([(505, 1400), (575, 1400), (575, 1470), (505, 1470)], 3.6, smooth=False, seed=22)
    for x0, y0, x1, y1, col in shops:
        b.outline([(x0, y1), (x0, y0), (x1, y0), (x1, y1)], 4, closed=False, smooth=False, seed=x0 + 1)
        for k in range(3):
            wy = y0 + 80 + k * 200
            b.outline([(x0 + 30, wy), (x1 - 30, wy), (x1 - 30, wy + 120), (x0 + 30, wy + 120)], 3, smooth=False, seed=int(wy + x0))
    b.outline([(735, 1400), (850, 1400), (800, 1300), (760, 1290)], 3.4, seed=23)
    for pts in ([(200, 1690), (270, 1690), (275, 1790), (195, 1790)], [(820, 1700), (890, 1700), (895, 1800), (815, 1800)]):
        b.outline(pts, 3.4, smooth=False, seed=int(pts[0][0]))
        b.ink([(pts[0][0] + 15, pts[0][1]), (pts[0][0] + 35, pts[0][1] - 30), (pts[1][0] - 15, pts[0][1])], 3, seed=int(pts[0][0]) + 1)
    people_phase(figs, 'ink')
    b.stage('ink')
    people_phase(figs, 'dark')
    b.stage('dark')
    # star, ornaments, garland lights, shop windows, Santa hat, bags
    star = b.poly([(540 + 46 * np.cos(np.deg2rad(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45),
                    350 + 46 * np.sin(np.deg2rad(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45)) for k in range(10)], smooth=False)
    b.fill(star, 'mustard', pressure=0.97, slip=0, medium='gouache', seed=41)
    r = np.random.default_rng(42)
    ys, xs = np.nonzero(tree > 0.7)
    for i in r.choice(len(xs), 60, replace=False):
        b.dot(xs[i], ys[i], r.uniform(7, 11), colour=['coral', 'butter', 'mustard', 'cheek'][i % 4], medium='gouache')
    for y0 in (700, 1000, 1300):
        g = [(320 + (y0 - 700) * -0.25 + k * (440 + (y0 - 700) * 0.5) / 10, y0 + 30 * np.sin(k / 10 * np.pi)) for k in range(11)]
        b.ink(g, 2.4, colour='butter', seed=y0)
    for x0, y0, x1, y1, col in shops:
        for k in range(3):
            wy = y0 + 80 + k * 200
            b.fill(b.poly([(x0 + 30, wy), (x1 - 30, wy), (x1 - 30, wy + 120), (x0 + 30, wy + 120)], smooth=False), 'butter', pressure=0.85, slip=0, seed=int(wy + x0) + 5)
    b.fill(hat, 'tomato', pressure=0.97, seed=43)
    b.chalk(b.ellipse(760, 1290, 18, 18), pressure=0.95, seed=44)
    b.chalk(b.band([(735, 1402), (850, 1402)], 20), pressure=0.95, seed=45)
    b.fill(bags[0], 'cheek', pressure=0.95, seed=46); b.fill(bags[1], 'coral', pressure=0.95, seed=47)
    people_phase(figs, 'accents')
    b.stage('accents')
    for k in range(80):
        x, y = r.uniform(60, 1020), r.uniform(60, 1500)
        if front[int(y), int(x)] > 0.3: continue
        b.dot(x, y, r.uniform(3, 6), colour='chalk', medium='chalk')
    b.speckle((60, 60, 1020, 1860), 'chalk', n=1200, size=(0.5, 1.6), seed=49)
    b.stage('chalk')
    finish(b, out)

if __name__ == '__main__':
    main(sys.argv[1])
