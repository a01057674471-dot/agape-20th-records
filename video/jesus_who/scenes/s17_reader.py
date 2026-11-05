"""⑦ asking questions while reading: a young woman at a café window table reads, her chin on her hand, a little
painted question mark floating above; a latte and a croissant."""
from common import *

def main(out, stages=None):
    g, p = canvas(1717, tone='#e8a868', stages=stages)
    wom = Person(g, 560, 860, 150, skin=SKIN_JP, hair='bun', hair_col=HAIR_DARK, body='shirt', cloth='#e8c060',
                 look=(-0.1, 0.8), mouth='flat', brows=0.6, turn=-0.2, seed=1,
                 arms=[[(450, 1050), (420, 1180), (470, 1300)], [(680, 1050), (720, 1000), (690, 930)]], torso=(1340, 220))
    wall = (p.YY < 1300).astype(np.float32) * (1 - wom.fig)
    g.block_in(wall, '#f2e2c4', angle=0)
    win = g.poly([(80, 160), (1000, 160), (1000, 760), (80, 760)], smooth=False) * (1 - wom.fig)
    g.block_in(win, '#a8dcec', length=(30, 70), width=(10, 18))
    stone_house(g, 120, 560, 200, 200, col='#f2b8a0', door=False, seed=4)
    olive_tree(g, 860, 760, 0.9, seed=5)
    cloud(g, 700, 280, 0.8, seed=6)
    for x in (80, 540, 1000): g.line([(x, 160), (x, 760)], 20, '#8a5a3a', 1.0, taper=(0, 0))
    for y in (160, 760): g.line([(80, y), (1000, y)], 20, '#8a5a3a', 1.0, taper=(0, 0))
    g.stage('room')
    paint_people(g, [wom])
    hand(g, 680, 930, 0.9, -100, SKIN_JP, curl=0.6)
    table = (p.YY > 1300).astype(np.float32)
    g.block_in(table, '#f6f0e6', angle=0); g.model_form(table, ramp('#f6f0e6', light=0.2, pale=0.4), steps=3, relief=0.1, height=np.zeros_like(table), angle=0)
    open_book(g, 500, 1480, 600, 300, cover='#2f5a4a', seed=7)
    hand(g, 460, 1330, 0.9, 60, SKIN_JP, curl=0.3)
    cup(g, 900, 1420, 2.0, '#f8f4ee')
    g.glaze(g.ellipse(900, 1360, 46, 12), '#c08a5a', 0.9, mode='normal')
    bread(g, 160, 1460, 90, 40, seed=8)
    q = paint_text(g, '?', 860, 500, 220, '#e06a4a', weight=900)
    q2 = paint_text(g, '?', 960, 620, 120, '#4a8ac0', weight=900)
    finish(g, out, stages)
