"""D. a young woman in front of a wedding-chapel window display (a white dress, a small cross on the glass),
her head tilted: why would anyone put THAT up?  A chalk question mark."""
from common import *

def main(out, stages=None):
    b = page(401, stages)
    wom = Figure(b, 330, 1060, 92, coat='coral', hair='long', hair_col='#3b2b28', look=(0.9, -0.5), mouth='hmm', brows=1,
                 tilt=-10, seed=1, arms=[[(260, 1180), (250, 1320), (300, 1400)], [(410, 1180), (440, 1120), (410, 1080)]], length=4.2)
    shop = b.poly([(520, 520), (1000, 520), (1000, 1600), (520, 1600)], smooth=False)
    glass = b.poly([(560, 600), (960, 600), (960, 1480), (560, 1480)], smooth=False)
    cr = cross_mask(b, 760, 680, 300, w=190, t=30)
    dress = b.ellipse(760, 1280, 110, 80)          # a bouquet on a stand
    front = union(wom.mask)
    b.block((40, 50, 1040, 1860), 'powder', rough=10, corner=30, avoid=union(front, shop), halo=3, seed=11)
    b.fill(shop * (1 - glass), 'cobalt', pressure=0.95, angle=80, avoid=front, halo=3, seed=12)
    b.fill(glass * (1 - front), 'mist', pressure=0.9, angle=60, avoid=union(cr, dress), halo=3, seed=13)
    b.fill(cr * (1 - front), '#9a8a7e', pressure=0.95, slip=0, medium='gouache', seed=14)
    pave = (YY > 1600).astype(np.float32)
    b.fill(pave * (1 - front), 'cornflower', pressure=0.9, angle=2, seed=15)
    wom.blue()
    b.stage('blue')
    b.outline([(520, 520), (1000, 520), (1000, 1600), (520, 1600)], 4.8, smooth=False, seed=21)
    b.outline([(560, 600), (960, 600), (960, 1480), (560, 1480)], 3.6, smooth=False, seed=22)
    cross_ink(b, 760, 680, 300, w=190, t=30, width=4.0, seed=23)
    b.ink([(760, 1340), (760, 1470)], 5, seed=24)
    b.ink([(700, 1470), (820, 1470)], 4, seed=25)
    b.ink([(500, 480), (1020, 480)], 6, seed=26)
    wom.ink()
    b.stage('ink')
    b.hatch(glass * (XX > 880) * (1 - dress) * (1 - cr), angle=60, spacing=12, length=(18, 36), width=2.0, colour='cornflower',
            medium='crayon', density=0.6, seed=31)
    wom.dark()
    b.stage('dark')
    wom.accents()
    for k in range(9):
        b.flower(600 + k * 42, 1460, 10, 'coral', seed=40 + k)
    b.stage('accents')
    for k in range(16):
        a = k * 0.4; rr_ = 20 + (k % 4) * 22
        b.flower(760 + np.cos(a) * rr_ * 1.3, 1280 + np.sin(a) * rr_ * 0.8, 13, 'coral' if k % 3 else 'cheek', seed=60 + k)
    b.chalk([[(600, 1300), (700, 700)], [(640, 1400), (760, 760)]], width=12, pressure=0.4, seed=52)
    q = [(150, 560), (160, 500), (210, 470), (270, 490), (280, 550), (230, 600), (220, 650)]
    b.ink(q, 14, colour='coral', dry=0.15, seed=53)
    b.dot(222, 705, 11, colour='coral', medium='gouache')
    b.speckle((60, 60, 1020, 1860), 'chalk', n=700, size=(0.5, 1.3), seed=56)
    b.stage('chalk')
    finish(b, out, stages)
