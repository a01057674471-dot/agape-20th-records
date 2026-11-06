"""F. the cross, from far away: one cross on the hill, a small figure on it (Jesus) seen as a quiet silhouette,
a break in the clouds letting a soft butter light down; two small figures kneeling at the foot."""
from common import *

def main(out, stages=None):
    b = page(601, stages)
    hill = b.poly([(40, 1870), (40, 1500), (300, 1330), (520, 1240), (700, 1260), (880, 1360), (1040, 1460), (1040, 1870)])
    cm = cross_mask(b, 560, 760, 500, w=300, t=36, arm=0.26)
    head = b.ellipse(560, 868, 30, 32)
    body = b.poly([(530, 900), (590, 900), (582, 1080), (538, 1080)])
    arms = b.band([(420, 900), (560, 905), (700, 900)], 22)
    jesus = union(head, body, arms)
    beam = b.poly([(380, 90), (760, 90), (700, 1240), (440, 1240)])
    kneel = [b.blob(470, 1240, 30, 40, 0.05, 1), b.blob(640, 1235, 28, 38, 0.05, 2)]
    b.block((40, 50, 1040, 1870), 'cobalt', rough=12, corner=30, avoid=union(cm, jesus), halo=2, seed=11)
    b.fill(b.poly([(40, 50), (1040, 50), (1040, 600), (40, 650)], smooth=False), 'deep', pressure=0.8, angle=-8, slip=0,
           avoid=union(cm, beam), halo=4, seed=12)
    b.fill(hill, 'blue', pressure=0.95, angle=-12, seed=13)
    b.fill(cm, '#6a5a52', pressure=0.97, slip=0, medium='gouache', seed=14)
    b.fill(jesus, '#2a2630', pressure=0.97, slip=0, medium='gouache', loose=1.2, seed=15)
    b.stage('blue')
    cross_ink(b, 560, 760, 500, w=300, t=36, arm=0.26, width=4.4, seed=21)
    wood_grain(b, 560, 760, 500, w=300, t=36, arm=0.26, seed=22)
    b.outline([(40, 1500), (300, 1330), (520, 1240), (700, 1260), (880, 1360), (1040, 1460)], 5, closed=False, seed=23)
    for k, m in enumerate(kneel):
        b.fill(m, 'navy', pressure=0.95, slip=0, medium='gouache', seed=24 + k)
    b.dot(470, 1192, 18, colour='navy', medium='gouache'); b.dot(640, 1188, 17, colour='navy', medium='gouache')
    b.stage('ink')
    b.scribble(hill * (YY > 1640), width=5, spacing=5.4, angle=80, colour='navy', seed=31)
    b.blades(40, 1040, lambda x: 1660 + 20 * np.sin(x / 80), n=40, height=(30, 80), width=4, seed=32)
    b.stage('dark')
    b.fill(beam * (1 - cm) * (1 - jesus) * (YY < 1240), 'butter', pressure=0.45, angle=90, slip=0, edge=30, dry_edge=0.9, seed=41)
    b.stage('accents')
    for i, (x, y, w, h) in enumerate([(200, 330, 340, 120), (880, 300, 300, 110)]):
        b.chalk(b.cloud(x, y, w, h, 5, seed=50 + i), pressure=0.5, alpha=0.8, seed=50 + i)
    b.chalk([[(470, 150), (500, 700)], [(600, 120), (590, 680)], [(680, 160), (650, 700)]], width=10, pressure=0.35, seed=53)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=900, size=(0.5, 1.4), seed=54)
    b.stage('chalk')
    finish(b, out, stages)
