"""⑥ a gift, not a prize: two open hands receiving a small wrapped present with a red ribbon, on a warm ground."""
from common import *

def main(out, stages=None):
    g, p = canvas(1515, tone='#f0b070', stages=stages)
    g.scumble_background('#f8cf88', bottom='#f6e2bc', seed=2, angle=-30)
    g.stage('background')
    sleeves = [g.band([(-40, 1900), (160, 1500), (300, 1300)], 200, 160), g.band([(1120, 1900), (920, 1500), (780, 1300)], 200, 160)]
    for m in sleeves:
        g.block_in(m, '#5a8ab8', angle=-60); g.model_form(m, ramp('#5a8ab8', light=0.25, pale=0.45), steps=3, relief=0.5)
    hand(g, 380, 1180, 2.3, -60, SKIN_JP, spread=8, curl=0.2)
    hand(g, 700, 1180, 2.3, -120, SKIN_JP, spread=8, curl=0.2)
    box = g.poly([(380, 760), (700, 760), (720, 1060), (360, 1060)], smooth=False)
    lid = g.poly([(350, 700), (730, 700), (740, 790), (340, 790)], smooth=False)
    g.cast_shadow(np.maximum(box, lid), 10, 30, soft=24, alpha=0.4, colour='#7a4a30')
    for m, c in ((box, '#f4f0e8'), (lid, '#f8f6f0')):
        g.block_in(m, c, angle=90); g.model_form(m, ramp(c, light=0.2, pale=0.4), steps=3, relief=0.3)
    for k in range(6):
        for j in range(4):
            g.dab(410 + k * 56, 830 + j * 60, 9, '#f2b0a0')
    g.block_in(g.band([(540, 700), (540, 1060)], 44), '#d83a3a', angle=90)
    g.block_in(g.band([(345, 745), (735, 745)], 40), '#d83a3a', angle=0)
    for sgn in (-1, 1):
        loop = g.blob(540 + sgn * 70, 650, 70, 44, 0.05, 3 + sgn * 2 + 4, sgn * 20)
        g.block_in(loop, '#e04a4a'); g.model_form(loop, ramp('#e04a4a', cool='#5a1020'), steps=3, relief=0.6)
    g.sphere_shade(540, 670, 30, 28, ramp('#d83a3a', cool='#5a1020'), steps=3, mask=g.ellipse(540, 670, 30, 28))
    finish(g, out, stages)
