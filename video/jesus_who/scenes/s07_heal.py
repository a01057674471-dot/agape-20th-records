"""③ drawing near: a sick man sitting on a mat by a wall, people hurrying past at a distance; Jesus kneels beside him
and puts a hand on his shoulder."""
from common import *

def main(out, stages=None):
    g, p = canvas(707, tone='#e8b070', stages=stages)
    sick = Person(g, 330, 1150, 108, skin=SKIN_DEEP, hair='bald', hair_col=HAIR_GREY, beard='grey', cloth='#9aa0a8', age=70,
                  look=(0.5, -0.4), mouth='flat', turn=0.4, brows=-0.8, blush=0.15, seed=1,
                  arms=[[(260, 1290), (240, 1400), (330, 1450)], [(400, 1290), (430, 1400), (360, 1450)]], torso=(1500, 170))
    jesus = Person(g, 700, 1060, 120, skin=SKIN_OLIVE, hair='curly', hair_col=HAIR_DARK, beard='short', cloth='#efe2c4',
                   stripe='#8a5a3a', mantle='#b8643c', look=(-0.6, 0.3), mouth='smile', turn=-0.6, seed=2,
                   arms=[[(610, 1210), (530, 1270), (452, 1292)], [(790, 1210), (820, 1340), (760, 1430)]], torso=(1560, 190))
    p1 = Person(g, 880, 690, 56, skin=SKIN_DEEP, hair='scarf', scarf_col='#6a5aa8', cloth='#9a6aa8', look=(-0.8, 0),
                mouth='flat', turn=0.7, seed=3, torso=(880, 70), arms=[], legs=[[(870, 880), (860, 920)], [(900, 880), (915, 920)]])
    p2 = Person(g, 990, 700, 58, skin=SKIN_LIGHT, hair='short', hair_col=HAIR_DARK, beard='short', cloth='#7a8a5a',
                look=(-0.8, 0), mouth='flat', turn=0.7, seed=4, torso=(890, 72), arms=[], legs=[[(975, 890), (965, 930)], [(1005, 890), (1015, 930)]])
    people = [p1, p2, sick, jesus]
    figs = np.maximum.reduce([pp.fig for pp in people])
    sky(g, '#9ccfe4', '#f4e8cc', avoid=figs, seed=5)
    cloud(g, 300, 220, 0.9, seed=6)
    hills(g, 620, '#cdb88a', seed=7, amp=30, avoid=figs, relief=0.2)
    stone_house(g, 700, 480, 240, 200, col='#f0d8aa', seed=8)
    wall = g.poly([(0, 700), (560, 720), (560, 1420), (0, 1420)], smooth=False) * (1 - figs)
    g.block_in(wall, '#e6caa0', angle=0, length=(30, 70), width=(12, 22))
    g.model_form(wall, ramp('#e6caa0', light=0.2, pale=0.4), steps=3, relief=0.15, height=np.zeros_like(wall), angle=0)
    rr = np.random.default_rng(9)
    for row in range(10):
        y = 720 + row * 70
        off = 60 if row % 2 else 0
        for k in range(6):
            x = off + k * 120
            g.line([(x, y), (x, y + 70)], 2.4, '#b8946a', 0.45)
        g.line([(0, y), (560, y + 2)], 2.4, '#b8946a', 0.45)
    street = floor(g, 900, '#e8d2a4', avoid=np.maximum(figs, wall))
    mat = g.poly([(140, 1430), (620, 1430), (660, 1540), (100, 1540)], smooth=False)
    g.block_in(mat, '#c8a060', angle=0, length=(20, 40), width=(6, 10))
    for k in range(10): g.line([(150 + k * 50, 1432), (120 + k * 54, 1538)], 3, '#9a7440', 0.6)
    stick = g.band([(540, 1530), (600, 1180)], 14, 12)
    g.block_in(stick, '#8a6040', angle=-80, length=(10, 20), width=(4, 6))
    g.stage('scenery')
    paint_people(g, people)
    hand(g, 432, 1294, 0.8, 175, SKIN_OLIVE, curl=0.3)
    for dy in (0, 16, 32): g.line([(222, 1350 + dy), (268, 1358 + dy)], 12, '#f4efe2', 0.95)   # a bandaged arm
    finish(g, out, stages)
