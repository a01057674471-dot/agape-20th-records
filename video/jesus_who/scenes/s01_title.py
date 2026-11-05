"""① title: a bright sunny board, a big cream speech bubble (the title goes in it), two small people looking up."""
from common import *

def main(out, stages=None):
    g, p = canvas(101, tone='#f0b060', stages=stages)
    bub = np.maximum(g.poly(rrect(540, 820, 900, 560, 120), smooth=False),
                     g.poly([(380, 1060), (470, 1060), (330, 1220)]))
    kid = Person(g, 330, 1500, 92, skin=SKIN_JP, hair='short', hair_col=HAIR_BLACK, body='shirt', cloth='#4a8ac0',
                 look=(0.2, -0.8), mouth='open', brows=1.0, arms=[[(255, 1610), (240, 1700), (260, 1770)],
                 [(400, 1610), (440, 1520), (470, 1440)]], torso=(1830, 120), seed=3)
    wom = Person(g, 720, 1470, 104, skin=SKIN_JP, hair='bun', hair_col=HAIR_BLACK, body='jacket', cloth='#d0604a',
                 look=(-0.2, -0.8), mouth='smile', brows=0.6, arms=[[(640, 1590), (620, 1700), (650, 1790)],
                 [(800, 1590), (830, 1700), (810, 1790)]], torso=(1920, 150), seed=4)
    figs = np.maximum(kid.fig, wom.fig)
    sky(g, '#ffd66e', '#ffc07c', avoid=np.maximum(bub, figs), seed=5, angle=-35)
    g.stage('background')
    sun(g, 900, 230, 90, '#fff0a0')
    cloud(g, 200, 300, 0.9, seed=6); cloud(g, 760, 440, 0.6, seed=7)
    for x, y in ((140, 520), (190, 500), (860, 1280), (920, 1310)):
        g.line([(x - 18, y), (x - 6, y - 10), (x, y - 2), (x + 6, y - 10), (x + 18, y)], 3.4, '#8a5a3a', 0.8)
    floor(g, 1700, '#9ac27a', avoid=figs)
    g.cast_shadow(bub, 16, 24, soft=26, alpha=0.3, colour='#c0703a')
    g.block_in(bub, '#fff6e4', angle=0, length=(60, 120), width=(18, 30))
    g.glaze(bub * smoothstep(900, 1100, g.P.YY), '#f2dcc0', 0.4)
    g.line(np.vstack([rrect(540, 820, 870, 530, 104)]), 4, '#f0c890', 0.6)
    g.stage('bubble')
    paint_people(g, [kid, wom])
    finish(g, out, stages)
