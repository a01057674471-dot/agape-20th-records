"""K. 愛のかたち: back in the chapel, now from the front -- the couple face each other under the cross, holding
hands, a gold ring glinting between them; the cross glows warm behind; petals falling."""
from common import *

def main(out, stages=None):
    b = page(1101, stages)
    cm = cross_mask(b, 540, 170, 560, w=340, t=46, arm=0.3)
    groom = Figure(b, 360, 1000, 100, coat='navy', hair='short', look=(0.9, 0.2), mouth='smile', seed=1, length=4.3, collar=True,
                   arms=[[(430, 1140), (490, 1230), (528, 1262)]])
    bride = Figure(b, 720, 1010, 94, coat='chalk', hair='bun', hair_col='#3b2b28', look=(-0.9, 0.2), mouth='smile', seed=2,
                   dress=True, length=5.0, arms=[[(650, 1150), (590, 1230), (556, 1262)]])
    veil = b.poly([(650, 930), (720, 900), (800, 960), (860, 1200), (900, 1500), (820, 1500), (780, 1200)])
    figs = [groom, bride]
    front = union(groom.mask, bride.mask, veil)
    b.block((40, 50, 1040, 1870), 'mist', rough=10, corner=30, avoid=union(front, cm), halo=3, seed=11)
    b.fill(b.ellipse(540, 450, 420, 400) * (1 - front) * (1 - cm), 'butter', pressure=0.5, slip=0, edge=40, dry_edge=0.9, seed=12)
    b.fill(cm * (1 - front), '#8a7a70', pressure=0.97, slip=0, medium='gouache', seed=13)
    b.fill(cm * (1 - front) * (XX > 550), '#6a5a52', pressure=0.9, slip=0, medium='gouache', seed=14)
    floor = (YY > 1560).astype(np.float32)
    b.fill(floor * (1 - front), 'powder', pressure=0.9, angle=2, seed=15)
    people_phase(figs, 'blue')
    b.stage('blue')
    cross_ink(b, 540, 170, 560, w=340, t=46, arm=0.3, width=4.4, seed=21)
    wood_grain(b, 540, 170, 560, w=340, t=46, arm=0.3, seed=22)
    b.outline([(650, 930), (720, 900), (800, 960), (860, 1200), (900, 1500), (820, 1500), (780, 1200)], 3.2, open_=0.6, seed=23)
    b.ink([(40, 1560), (1040, 1560)], 4, seed=24)
    people_phase(figs, 'ink')
    b.ink([(332, 1110), (360, 1150), (388, 1110)], 3.4, seed=25)          # bow tie
    b.dot(360, 1128, 6)
    b.stage('ink')
    people_phase(figs, 'dark')
    b.stage('dark')
    people_phase(figs, 'accents')
    ring = b.ellipse(542, 1262, 16, 13) * (1 - b.ellipse(542, 1262, 9, 7))
    b.fill(ring, 'mustard', pressure=0.97, slip=0, loose=0.6, medium='gouache', lanes=0, seed=31)
    for k in range(8):
        a = np.deg2rad(k * 45)
        b.crayon([[(542 + np.cos(a) * 26, 1262 + np.sin(a) * 22), (542 + np.cos(a) * 40, 1262 + np.sin(a) * 34)]], 'mustard',
                 width=4, pressure=0.85, seed=32 + k)
    bq = b.ellipse(760, 1330, 46, 40)
    b.fill(bq, 'coral', pressure=0.95, medium='gouache', seed=41)
    for k in range(7):
        b.flower(735 + (k % 3) * 24, 1312 + (k // 3) * 20, 10, 'cheek', seed=42 + k)
    r = np.random.default_rng(50)
    for k in range(30):
        x, y = r.uniform(80, 1000), r.uniform(120, 1500)
        if front[int(y), int(x)] > 0.2 or cm[int(y), int(x)] > 0.2: continue
        b.dot(x, y, r.uniform(4, 7), r.uniform(3, 5), colour='coral' if k % 2 else 'cheek', medium='gouache', seed=60 + k)
    b.stage('accents')
    b.chalk(bride.S['body'], pressure=0.85, angle=80, seed=71)
    b.chalk(veil * (1 - bride.S['head']), pressure=0.5, angle=70, alpha=0.75, seed=72)
    groom.chalk()
    b.speckle((60, 60, 1020, 1860), 'chalk', n=700, size=(0.5, 1.3), seed=73)
    b.speckle((200, 100, 880, 800), 'butter', n=300, size=(0.8, 2.0), seed=74)
    b.stage('chalk')
    finish(b, out, stages)
