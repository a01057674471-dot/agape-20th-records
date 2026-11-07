"""the map of Japan in blue picture-book style. variant 'night': a navy sea, the islands dim, only a few tiny
lights. variant 'dawn': the same map at sunrise, lights spreading over the islands, a coral glow from the west."""
import sys
from common_amj import *

def main(out, variant='night'):
    b = page(1301 if variant == 'night' else 1302)
    I = islands(b)
    land = np.maximum(I['japan'], I['kor'])
    night = variant == 'night'
    b.block((40, 50, 1040, 1870), 'navy' if night else 'powder', rough=12, corner=30, avoid=land, halo=3, seed=11)
    if not night:
        b.fill(b.ellipse(120, 1100, 700, 700) * (1 - land) * smoothstep(48, 70, XX), 'butter', pressure=0.45, slip=0, edge=40, dry_edge=0.9, seed=12)
    b.fill(I['japan'], 'deep' if night else 'cornflower', pressure=0.95, angle=-50, seed=13)
    b.fill(I['kor'], 'teal' if night else 'blue', pressure=0.95, angle=-50, seed=14)
    b.stage('blue')
    for k, nm in enumerate(('hon', 'kyu', 'shi', 'hok', 'kor')):
        b.outline(OUTLINES[nm], 4.2, closed=nm != 'kor', open_=0.5, seed=20 + k, colour=INK if not night else '#0e1622')
    b.stage('ink')
    if night:
        b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.6), avoid=land, seed=31)
        for (x, y) in (CITIES['도쿄'], CITIES['후쿠오카'], CITIES['아키타']):              # only a few lights
            b.fill(b.ellipse(x, y, 40, 40), 'butter', pressure=0.55, slip=0, lanes=0, seed=int(x))
            b.dot(x, y, 10, colour='mustard', medium='gouache')
            b.dot(x - 2, y - 2, 4, colour='chalk', medium='chalk')
        for i, (x, y, w, h) in enumerate([(300, 300, 280, 90), (760, 1650, 240, 80)]):
            b.chalk(b.cloud(x, y, w, h, 5, seed=40 + i), pressure=0.3, alpha=0.6, seed=40 + i)
    else:
        r = np.random.default_rng(50)
        lights = list(CITIES.values())
        ys, xs = np.nonzero(I['japan'] > 0.6)
        pick = r.choice(len(xs), 90, replace=False)
        lights += [(xs[i], ys[i]) for i in pick]
        for (x, y) in lights:
            b.fill(b.ellipse(x, y, 20, 20), 'butter', pressure=0.4, slip=0, lanes=0, seed=int(x * 3 + y))
            b.dot(x, y, r.uniform(4, 7), colour='mustard', medium='gouache')
        b.flower(*P(127.8, 35.6), 18, 'coral', seed=60)                             # a little coral flower on Korea
        b.chalk(b.cloud(320, 300, 300, 100, 5, seed=61), pressure=0.75, seed=61)
        b.chalk(b.cloud(780, 1700, 260, 90, 5, seed=62), pressure=0.75, seed=62)
        for x, y in ((420, 600), (470, 640), (520, 590)):
            b.ink([(x - 20, y), (x - 7, y - 11), (x, y - 2), (x + 7, y - 11), (x + 20, y)], 3.2, seed=int(x))
    b.stage('accents')
    finish(b, out)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
