"""⑤ the cross, far off: a lone wooden cross on a hill outside the city walls under a soft apricot sky -- seen from far
away, no figure on it, small and quiet. Not dark."""
from common import *

def main(out, stages=None):
    g, p = canvas(1313, tone='#e8a070', stages=stages)
    sky(g, '#f2b89a', '#fbe6c4', seed=2, angle=-15)
    g.stage('background')
    cloud(g, 250, 380, 1.3, col='#fff0e0', seed=3); cloud(g, 800, 600, 0.9, col='#fff0e0', seed=4)
    hills(g, 1060, '#c8a8a0', seed=5, amp=30, relief=0.15)
    walls = g.poly([(0, 1060), (430, 1060), (430, 990), (470, 990), (470, 1060), (520, 1060), (520, 1110), (0, 1110)], smooth=False)
    g.block_in(walls, '#d8b8a0', angle=0); g.model_form(walls, ramp('#d8b8a0'), steps=3, relief=0.2)
    for k in range(10): g.block_in(g.poly([(k * 44, 1040), (k * 44 + 24, 1040), (k * 44 + 24, 1062), (k * 44, 1062)], smooth=False), '#d8b8a0')
    hill = g.poly([(380, 1920), (480, 1300), (620, 1160), (760, 1150), (900, 1250), (1080, 1400), (1080, 1920)])
    g.block_in(hill, '#c9a87a', angle=-10)
    g.model_form(hill, ramp('#c9a87a', light=0.25, pale=0.45), steps=3, relief=0.35, angle=-10)
    near = hills(g, 1500, '#b89a6e', seed=6, amp=40, relief=0.3)
    cr = np.maximum(g.band([(700, 1160), (700, 820)], 30, 26), g.band([(600, 900), (800, 900)], 26, 24))
    g.cast_shadow(cr, 30, 10, soft=14, alpha=0.25, colour='#7a5040', on=hill)
    g.block_in(cr, '#7a5236', angle=90, length=(14, 30), width=(6, 10))
    g.model_form(cr, ['#3e2a1e', '#5a3c28', '#7a5236', '#9a7050', '#b89070'], steps=3, relief=0.5, angle=90)
    for x, y in ((240, 700), (290, 730)):
        g.line([(x - 18, y), (x - 6, y - 10), (x, y - 2), (x + 6, y - 10), (x + 18, y)], 3.4, '#7a5a5a', 0.7)
    g.strokes(near, '#d8c088', angle=-80, length=(10, 24), width=(2, 4), density=0.4, alpha=0.7, dry=0.4, seed=8)
    finish(g, out, stages)
