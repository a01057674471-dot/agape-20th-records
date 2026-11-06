"""H. the third morning (re-creation): a tomb cut in the rock, the round stone rolled aside, the doorway open and
empty; a pale sunrise in butter and mustard behind the hill; little coral flowers in the grass."""
from common import *

def main(out, stages=None):
    b = page(801, stages)
    rock = b.poly([(40, 1500), (40, 620), (220, 520), (520, 500), (760, 580), (880, 780), (900, 1500)])
    door = b.poly([(260, 1380), (260, 1130), (300, 1050), (380, 1020), (460, 1050), (500, 1130), (500, 1380)])
    stone = b.ellipse(700, 1220, 170, 175)
    sunm = b.ellipse(800, 360, 100, 100)
    b.block((40, 50, 1040, 1870), 'mist', rough=10, corner=30, avoid=union(rock, stone, sunm), halo=3, seed=11)
    b.fill(b.ellipse(800, 360, 260, 260) * (1 - rock) * (1 - stone), 'butter', pressure=0.4, slip=0, edge=40, dry_edge=0.9, seed=12)
    b.fill(rock, 'powder', pressure=0.95, angle=-60, avoid=door, halo=3, seed=13)
    b.fill(rock * (XX > 700), 'cornflower', pressure=0.85, angle=-60, slip=0, avoid=union(door, stone), halo=2, seed=14)
    b.fill(door, 'deep', pressure=0.95, angle=90, seed=15)
    b.fill(stone, 'cornflower', pressure=0.95, angle=40, seed=16)
    b.fill(stone * smoothstep(720, 840, XX + (YY - 1200) * 0.4), 'blue', pressure=0.85, slip=0, seed=17)
    grass = b.poly([(40, 1870), (40, 1420), (400, 1380), (800, 1400), (1040, 1440), (1040, 1870)])
    b.fill(grass * (1 - stone), 'cornflower', pressure=0.95, angle=-80, seed=18)
    b.fill(grass * (1 - stone) * (YY > 1640), 'blue', pressure=0.85, angle=-80, slip=0, seed=19)
    b.stage('blue')
    b.outline([(40, 620), (220, 520), (520, 500), (760, 580), (880, 780), (900, 1400)], 4.8, closed=False, seed=21)
    b.outline([(260, 1380), (260, 1130), (300, 1050), (380, 1020), (460, 1050), (500, 1130), (500, 1380)], 4.6, closed=False, seed=22)
    b.outline(circle_pts(700, 1220, 170, 175, n=40), 4.8, seed=23)
    b.ink(circle_pts(700, 1220, 110, 114, 200, 330, 16), 3, seed=24)
    b.hatch(rock * (XX > 620) * (1 - stone) * (1 - door), angle=70, spacing=10, length=(20, 40), width=2.2, colour='cornflower',
            medium='crayon', density=0.7, seed=60)
    for k in range(12):
        x = 80 + k * 64
        b.ink([(x, 650 + (k % 3) * 40), (x + 30, 720 + (k % 4) * 50)], 2.4, colour='slate', seed=25 + k)
    b.stage('ink')
    b.scribble(door * (YY < 1300), width=4.4, spacing=4.6, angle=80, colour='navy', seed=31)
    b.blades(40, 1040, lambda x: 1440 + 10 * np.sin(x / 60), n=60, height=(30, 90), width=4, clip=1 - stone, seed=32)
    b.stage('dark')
    b.fill(sunm, 'mustard', pressure=0.95, angle=0, seed=41)
    b.crayon([[(800 + np.cos(a) * 130, 360 + np.sin(a) * 130), (800 + np.cos(a) * 190, 360 + np.sin(a) * 190)]
              for a in np.deg2rad(np.arange(0, 360, 30))], 'mustard', width=7, pressure=0.8, seed=42)
    r = np.random.default_rng(43)
    for k in range(26):
        x, y = r.uniform(80, 1000), r.uniform(1480, 1820)
        if stone[int(y), int(x)] > 0.3: continue
        b.ink([(x, y + 4), (x + r.uniform(-5, 5), y + 36)], 2.2, seed=44 + k)
        b.flower(x, y, r.uniform(8, 12), 'coral' if k % 3 else 'cheek', seed=80 + k)
    b.stage('accents')
    linen = b.blob(380, 1350, 80, 20, 0.08, 5)
    b.chalk(linen, pressure=0.95, seed=51)
    b.chalk([[(510, 1120), (640, 900)], [(520, 1250), (700, 1000)]], width=14, pressure=0.35, seed=52)
    b.chalk(b.cloud(260, 250, 300, 110, 5, seed=53), pressure=0.75, seed=53)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=700, size=(0.5, 1.3), seed=54)
    b.stage('chalk')
    finish(b, out, stages)
