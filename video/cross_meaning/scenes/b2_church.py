"""B2. a little church on a corner of a Japanese town in the evening rain: a steeple with a cross, a lit window,
utility poles and wires, small houses, umbrellas passing."""
from common import *

def main(out, stages=None):
    b = page(202, stages)
    church = b.poly([(300, 1500), (300, 900), (540, 700), (780, 900), (780, 1500)], smooth=False)
    tower = b.poly([(470, 760), (470, 420), (540, 330), (610, 420), (610, 760)], smooth=False)
    cr = cross_mask(b, 540, 160, 180, w=110, t=22)
    houses = [b.poly([(20, 1500), (20, 1150), (140, 1060), (260, 1150), (260, 1500)], smooth=False),
              b.poly([(820, 1500), (820, 1120), (950, 1020), (1070, 1120), (1070, 1500)], smooth=False)]
    peeps = [Figure(b, 200, 1600, 40, coat='cobalt', hair='short', seed=5, arms=[[(180, 1650), (215, 1610), (230, 1540)]]),
             Figure(b, 880, 1620, 36, coat='teal', hair='long', seed=6, arms=[[(865, 1665), (895, 1630), (905, 1565)]])]
    umbs = [b.poly([(130, 1540), (230, 1470), (330, 1540)]), b.poly([(820, 1560), (905, 1495), (990, 1560)])]
    front = union(church, tower, cr, *houses, *[p.mask for p in peeps], *umbs)
    b.block((40, 50, 1040, 1500), 'cornflower', rough=10, corner=30, avoid=front, halo=3, seed=11)
    b.fill(church, 'mist', pressure=0.95, angle=80, seed=12)
    b.fill(tower, 'mist', pressure=0.95, angle=80, seed=13)
    b.fill(cr, 'mist', pressure=0.95, angle=90, slip=0, seed=14)
    b.fill(church * (XX > 640), 'powder', pressure=0.85, angle=80, slip=0, seed=15)
    for hm, c in zip(houses, ('blue', 'teal')):
        b.fill(hm, c, pressure=0.95, angle=80, seed=16)
    road = (YY > 1500).astype(np.float32)
    b.fill(road * (1 - front), 'powder', pressure=0.9, angle=2, seed=17)
    people_phase(peeps, 'blue')
    b.stage('blue')
    b.outline([(300, 1500), (300, 900), (540, 700), (780, 900), (780, 1500)], 4.8, smooth=False, seed=21)
    b.outline([(470, 760), (470, 420), (540, 330), (610, 420), (610, 760)], 4.4, smooth=False, seed=22)
    cross_ink(b, 540, 160, 180, w=110, t=22, width=4.0, seed=23)
    win = b.poly([(470, 1000), (470, 1150), (610, 1150), (610, 1000), (540, 940)], smooth=False)
    b.outline([(470, 1150), (470, 1000), (540, 940), (610, 1000), (610, 1150)], 4.0, seed=24)
    b.outline([(480, 1340), (480, 1500), (600, 1500), (600, 1340), (540, 1300)], 4.2, seed=25)       # door
    b.outline([(505, 560), (505, 640), (575, 640), (575, 560)], 3.0, seed=26)                         # bell window
    for hm, pts in zip(houses, ([(20, 1500), (20, 1150), (140, 1060), (260, 1150), (260, 1500)],
                                [(820, 1500), (820, 1120), (950, 1020), (1070, 1120), (1070, 1500)])):
        b.outline(pts, 4.2, smooth=False, seed=int(pts[0][0]) + 3)
    for x in (100, 980):
        b.ink([(x, 1500), (x + 4, 600)], 8, dry=0.3, seed=x)
        b.ink([(x - 40, 650), (x + 44, 650)], 5, seed=x + 1)
    b.ink([(0, 700), (100, 660), (540, 760), (980, 660), (1080, 700)], 2.4, seed=27, taper=(0, 0))
    b.ink([(0, 740), (100, 700), (540, 800), (980, 700), (1080, 740)], 2.2, seed=28, taper=(0, 0))
    for pts in ([(130, 1540), (230, 1470), (330, 1540)], [(820, 1560), (905, 1495), (990, 1560)]):
        b.outline(pts, 3.6, seed=int(pts[0][0]) + 9)
    people_phase(peeps, 'ink')
    b.stage('ink')
    b.scribble(houses[0] * (XX > 160), width=4.4, spacing=5.0, angle=80, colour='navy', seed=31)
    b.hatch(church * (XX > 650), angle=80, spacing=9, length=(18, 36), width=2.2, colour='cornflower', medium='crayon', seed=32)
    b.stage('dark')
    b.fill(win, 'butter', pressure=0.95, angle=0, slip=0, medium='gouache', seed=41)
    b.fill(b.poly([(490, 1360), (590, 1360), (590, 1500), (490, 1500)], smooth=False), 'mustard', pressure=0.9, slip=0, seed=42)
    b.fill(umbs[0], 'coral', pressure=0.95, seed=43); b.fill(umbs[1], 'mustard', pressure=0.95, seed=44)
    for x, y in ((60, 1250), (180, 1300), (880, 1220), (1000, 1260)):
        b.fill(b.poly([(x, y), (x + 50, y), (x + 50, y + 60), (x, y + 60)], smooth=False), 'butter', pressure=0.9, slip=0, seed=x)
    people_phase(peeps, 'accents')
    b.crayon([[(470 + k * 12, 1520), (440 + k * 15, 1760)] for k in range(12)], 'butter', width=6, pressure=0.5, dry=0.6, seed=45)
    b.stage('accents')
    b.chalk(b.cloud(260, 240, 280, 100, 5, seed=51), pressure=0.6, seed=51)
    b.rain((60, 60, 1020, 1860), n=520, angle=82, length=(12, 34), width=(1.6, 2.8), colour='deep', avoid=front, seed=52)
    b.rain((60, 60, 1020, 1860), n=260, angle=82, length=(12, 28), width=(1.6, 2.6), colour='chalk', avoid=front, seed=53)
    for k in range(10):
        b.ripples(150 + k * 85, 1700 + (k % 3) * 60, 20, 5, rings=2, width=2.2, seed=54 + k)
    b.stage('rain')
    finish(b, out, stages)
