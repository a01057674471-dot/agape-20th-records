"""A. a wedding in a small white chapel, seen from the back of the aisle: the couple at the altar (from behind),
a tall arched window of soft blue sky, and on the wall between them and the window a plain wooden cross.
Coral flowers on the aisle stands, mustard candle flames, petals on the floor."""
from common import *

def main(out, stages=None):
    b = page(101, stages)
    groom = Figure(b, 445, 1185, 66, coat='navy', hair='cap', back=True, seed=1,
                   arms=[[(388, 1270), (372, 1390), (392, 1470)], [(500, 1270), (540, 1360), (570, 1420)]])
    bride = Figure(b, 640, 1200, 60, coat='chalk', hair='bun', hair_col='#3b2b28', back=True, dress=True, length=4.6, seed=2,
                   arms=[[(590, 1280), (560, 1360), (585, 1420)]])
    veil = b.poly([(600, 1150), (680, 1150), (760, 1300), (800, 1480), (760, 1520), (520, 1520), (500, 1460), (560, 1260)])
    figs = [groom, bride]
    front = union(groom.mask, bride.mask, veil)
    # architecture shapes
    arch = b.poly([(330, 900), (330, 470), (360, 380), (430, 320), (540, 296), (650, 320), (720, 380), (750, 470), (750, 900)])
    cross = cross_mask(b, 540, 360, 420, w=250, t=34, arm=0.32)
    altar = b.poly([(250, 1000), (830, 1000), (850, 1110), (230, 1110)], smooth=False)
    floor = (YY > 1110).astype(np.float32)
    aisle = b.poly([(380, 1110), (700, 1110), (980, 1920), (100, 1920)], smooth=False)
    # --- 2 blue blocks
    b.block((40, 60, 1040, 1860), 'mist', rough=10, corner=30, avoid=union(front, arch), halo=3, seed=11)
    b.fill(arch, 'powder', pressure=0.95, angle=-80, loose=3, avoid=cross, halo=3, seed=12)
    b.fill(b.poly([(330, 900), (750, 900), (750, 760), (330, 760)], smooth=False) * arch, 'cornflower', pressure=0.85,
           angle=0, slip=0, avoid=cross, halo=3, seed=13)
    b.fill(cross, '#9a8a7e', pressure=0.95, angle=90, slip=0, loose=1.5, medium='gouache', seed=14)
    b.fill(cross * (XX > 548), '#7a6a60', pressure=0.9, angle=90, slip=0, loose=1, medium='gouache', seed=15)
    b.fill(altar * (1 - front), 'powder', pressure=0.95, angle=0, seed=16)
    b.fill(floor * (1 - front), 'powder', pressure=0.9, angle=4, avoid=aisle, halo=2, seed=17)
    b.fill(aisle * (1 - front), 'cornflower', pressure=0.95, angle=90, seed=18)
    # pews down both sides
    pews = []
    for k in range(4):
        y0 = 1250 + k * 160
        for side in (-1, 1):
            xa = 540 + side * (230 + k * 90); xb = 540 + side * (560 + k * 70)
            p = b.poly([(min(xa, xb), y0), (max(xa, xb), y0), (max(xa, xb), y0 + 90), (min(xa, xb), y0 + 90)], smooth=False)
            pews.append(p)
    pm = union(*pews) * (1 - front)
    b.fill(pm, 'blue', pressure=0.95, angle=0, seed=19)
    people_phase(figs, 'blue')
    b.stage('blue')
    # --- 3 ink
    b.outline([(330, 900), (330, 470), (360, 380), (430, 320), (540, 296), (650, 320), (720, 380), (750, 470), (750, 900)], 4.6,
              closed=False, seed=21)
    b.ink([(330, 900), (750, 900)], 4.0, seed=22)
    for x in (470, 610):
        b.ink([(x, 330 if x < 540 else 325), (x, 900)], 2.6, seed=x)
    for y in (560, 740):
        b.ink([(338, y), (742, y)], 2.6, seed=y)
    cross_ink(b, 540, 360, 420, w=250, t=34, arm=0.32, width=4.4, seed=23)
    wood_grain(b, 540, 360, 420, w=250, t=34, arm=0.32, seed=24)
    b.outline([(250, 1000), (830, 1000), (850, 1110), (230, 1110)], 4.4, smooth=False, seed=25)
    b.ink([(210, 1110), (870, 1110)], 4.0, seed=26)
    for p_ in pews:
        ys, xs = np.nonzero(p_ > 0.5)
        if len(xs):
            b.outline([(xs.min(), ys.min()), (xs.max(), ys.min()), (xs.max(), ys.max()), (xs.min(), ys.max())], 3.6,
                      smooth=False, seed=int(xs.min()))
    # candles on the altar
    for cx in (300, 780):
        b.outline([(cx - 14, 930), (cx + 14, 930), (cx + 14, 1000), (cx - 14, 1000)], 3.0, smooth=False, seed=cx)
        b.ink([(cx, 930), (cx, 916)], 2.0, seed=cx + 1)
    # flower stands at the front of the aisle
    for cx in (200, 880):
        b.ink([(cx, 1500), (cx - 4, 1200)], 5.0, seed=cx + 2)
        b.outline(circle_pts(cx, 1180, 70, 50, n=24), 3.4, seed=cx + 3)
        b.ink([(cx - 60, 1500), (cx + 60, 1500)], 4.0, seed=cx + 4)
    people_phase(figs, 'ink')
    b.outline([(600, 1150), (680, 1150), (760, 1300), (800, 1480), (760, 1520), (520, 1520), (500, 1460), (560, 1260)],
              3.2, open_=0.6, seed=27)
    b.stage('ink')
    # --- 4 darks
    b.hatch(pm, angle=-80, spacing=8, length=(10, 20), width=2.0, density=0.7, seed=31)
    b.hatch(altar * (YY > 1060), angle=80, spacing=7, length=(8, 16), width=2.0, density=0.6, seed=32)
    people_phase(figs, 'dark')
    b.scribble(groom.S['body'] * smoothstep(1250, 1500, YY), width=4.2, spacing=4.4, angle=78, colour='navy', dry=0.5, seed=33)
    b.stage('dark')
    # --- 5 accents
    for cx in (200, 880):
        for k in range(14):
            a = k * 0.45; rr = 20 + (k % 4) * 12
            b.flower(cx + np.cos(a) * rr * 1.4, 1180 + np.sin(a) * rr * 0.9, 12, 'coral' if k % 3 else 'cheek', seed=cx + k)
    for cx in (300, 780):
        b.fill(b.ellipse(cx, 906, 9, 15), 'mustard', pressure=0.95, slip=0, lanes=0, medium='gouache', seed=cx + 5)
        b.crayon([[(cx + np.cos(a) * 24, 906 + np.sin(a) * 24), (cx + np.cos(a) * 38, 906 + np.sin(a) * 38)]
                  for a in np.deg2rad([200, 240, 270, 300, 340])], 'butter', width=4, pressure=0.7, seed=cx + 6)
    bq = b.ellipse(578, 1420, 34, 30)                              # the bride's bouquet
    b.fill(bq, 'coral', pressure=0.95, medium='gouache', seed=41)
    for k in range(6):
        b.flower(560 + (k % 3) * 18, 1408 + (k // 3) * 22, 9, 'cheek', seed=42 + k)
    r = np.random.default_rng(43)
    for k in range(40):
        x, y = r.uniform(140, 940), r.uniform(1560, 1840)
        b.dot(x, y, r.uniform(4, 7), r.uniform(3, 5), colour='coral' if k % 2 else 'cheek', medium='gouache', seed=44 + k)
    people_phase(figs, 'accents')
    b.stage('accents')
    # --- 6 chalk: the bride's dress and veil, light from the window
    b.chalk(bride.S['body'], pressure=0.85, angle=80, seed=51)
    b.chalk(veil * (1 - bride.S['hair']), pressure=0.5, angle=70, alpha=0.75, seed=52)
    b.chalk([[(360, 880), (470, 560)], [(420, 890), (600, 420)], [(620, 880), (700, 600)]], width=10, pressure=0.45, seed=53)
    b.chalk([[(540, 1000), (520, 1110)]], width=30, pressure=0.35, seed=54)
    b.speckle((60, 80, 1020, 1840), 'chalk', n=900, size=(0.5, 1.4), seed=55)
    b.stage('chalk')
    finish(b, out, stages)
