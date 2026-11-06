"""I. 「死の印」から「愛の印」に: the same cross on the hill at sunrise, now standing in a field of coral and pink
flowers, a warm butter sky, birds; the cross plain and empty."""
from common import *

def main(out, stages=None):
    b = page(901, stages)
    cm = cross_mask(b, 540, 640, 620, w=380, t=46, arm=0.27)
    hill = b.poly([(40, 1870), (40, 1380), (300, 1270), (540, 1240), (780, 1270), (1040, 1380), (1040, 1870)])
    b.block((40, 50, 1040, 1870), 'mist', rough=10, corner=30, avoid=cm, halo=3, seed=11)
    b.fill(b.ellipse(540, 1240, 640, 520) * (1 - cm) * (YY < 1300), 'butter', pressure=0.55, slip=0, edge=40, dry_edge=0.9, seed=12)
    b.fill(hill * (1 - cm), 'cornflower', pressure=0.95, angle=-10, seed=13)
    b.fill(hill * (YY > 1560), 'blue', pressure=0.9, angle=-8, slip=0, seed=14)
    b.fill(cm, '#8a7a70', pressure=0.97, slip=0, medium='gouache', seed=15)
    b.fill(cm * (XX > 552), '#6a5a52', pressure=0.9, slip=0, medium='gouache', seed=16)
    b.stage('blue')
    cross_ink(b, 540, 640, 620, w=380, t=46, arm=0.27, width=4.6, seed=21)
    wood_grain(b, 540, 640, 620, w=380, t=46, arm=0.27, seed=22)
    b.outline([(40, 1380), (300, 1270), (540, 1240), (780, 1270), (1040, 1380)], 5, closed=False, seed=23)
    for x, y in ((230, 420), (290, 470), (800, 360), (860, 400)):
        b.ink([(x - 22, y), (x - 8, y - 12), (x, y - 2), (x + 8, y - 12), (x + 22, y)], 3.4, seed=int(x + y))
    b.stage('ink')
    b.blades(40, 1040, lambda x: 1330 + 50 * ((x - 540) / 500) ** 2, n=70, height=(30, 90), width=4, seed=31)
    b.stage('dark')
    r = np.random.default_rng(41)
    for k in range(150):
        x = r.uniform(70, 1010); y = r.uniform(1300, 1840)
        if y < 1270 + 120 * ((x - 540) / 500) ** 2: continue
        if cm[int(y), int(x)] > 0.3: continue
        s = 7 + (y - 1300) / 540 * 9
        b.ink([(x, y + s * 0.4), (x + r.uniform(-4, 4), y + s * 3.4)], 2.0, seed=100 + k)
        b.flower(x, y, s, ['coral', 'cheek', 'coral', 'mustard'][k % 4], seed=300 + k)
    b.crayon([[(540 + np.cos(a) * 700, 1240 + np.sin(a) * 700), (540 + np.cos(a) * 820, 1240 + np.sin(a) * 820)]
              for a in np.deg2rad(np.arange(200, 341, 14))], 'butter', width=8, pressure=0.7, seed=42)
    b.stage('accents')
    b.chalk([[(510, 660), (508, 1200)], [(380, 812), (520, 810)]], width=6, pressure=0.6, seed=51)
    b.chalk(b.cloud(240, 260, 300, 110, 5, seed=52), pressure=0.75, seed=52)
    b.chalk(b.cloud(820, 200, 240, 90, 5, seed=53), pressure=0.75, seed=53)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=54)
    b.stage('chalk')
    finish(b, out, stages)
