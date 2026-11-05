"""③ Jesus listens: sitting on a low stone wall in a sunny courtyard, leaning in to an older woman who is talking."""
import sys
from common import *

def main(out, stages=None):
    g, p = canvas(505, tone='#e8b070', stages=stages)
    jesus = Person(g, 360, 820, 150, skin=SKIN_OLIVE, hair='curly', hair_col=HAIR_DARK, beard='short',
                   cloth='#efe2c4', stripe='#8a5a3a', mantle='#b8643c', look=(0.55, 0.15), mouth='smile', turn=0.6,
                   arms=[[(250, 1010), (300, 1250), (420, 1330)], [(470, 1010), (560, 1180), (640, 1240)]],
                   torso=(1420, 230), seed=1)
    woman = Person(g, 770, 900, 128, skin=SKIN_DEEP, hair='scarf', scarf_col='#3f7a8a', cloth='#c9864a',
                   look=(-0.6, -0.1), mouth='talk', turn=-0.6, age=68, brows=0.5,
                   arms=[[(860, 1060), (900, 1240), (820, 1300)], [(680, 1060), (650, 1200), (720, 1290)]],
                   torso=(1460, 210), seed=2)
    figs = np.maximum(jesus.fig, woman.fig)
    wall = g.poly([(0, 1380), (1080, 1400), (1080, 1600), (0, 1590)], smooth=False)
    sky(g, '#9fd0e0', '#f6e6c4', avoid=np.maximum(figs, wall), seed=3)
    g.stage('background')
    cloud(g, 760, 260, 1.2, seed=7); cloud(g, 200, 420, 0.8, seed=8)
    far = hills(g, 760, '#c9b58a', seed=6, amp=40, avoid=figs, relief=0.2)
    for i, (hx_, hy_, hw, hh) in enumerate(((30, 700, 200, 150), (250, 740, 150, 120), (620, 690, 220, 170), (880, 730, 170, 130))):
        stone_house(g, hx_, hy_, hw, hh, col=['#efd6a6', '#ead0a0', '#f2dcb2', '#e6c896'][i], win=1, seed=10 + i)
    near = hills(g, 900, '#d8b47c', seed=9, amp=25, avoid=figs, relief=0.25)
    olive_tree(g, 960, 1120, 1.25, seed=5)
    olive_tree(g, 110, 1060, 0.9, seed=15)
    wm = wall * (1 - figs)
    g.block_in(wm, '#e2c08c', angle=0, length=(30, 70), width=(12, 22))
    for k in range(9):
        g.line([(k * 130 + 20, 1390 + k % 2 * 6), (k * 130 + 20, 1590)], 3, '#b08a5a', 0.5)
    g.line([(0, 1488), (1080, 1496)], 3, '#b08a5a', 0.45)
    g.cast_shadow(figs, 18, 30, soft=24, alpha=0.3, colour='#8a5a3a', on=wm)
    g.stage('scenery')
    paint_people(g, [woman, jesus])
    # a few flowers on the ground and a small clay jar
    for x, y, c in ((120, 1700, '#e86a50'), (200, 1760, '#f2c04a'), (930, 1720, '#e86a50'), (1000, 1800, '#ffffff')):
        for a in range(5):
            g.dab(x + 12 * np.cos(a * 1.26), y + 12 * np.sin(a * 1.26), 8, c)
        g.dab(x, y, 5, '#f8d860')
    cup(g, 560, 1660, 2.2, '#c8784a')
    finish(g, out, stages)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[sys.argv.index('--stages') + 1] if '--stages' in sys.argv else None)
