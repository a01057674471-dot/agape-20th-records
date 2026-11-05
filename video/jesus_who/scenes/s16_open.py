"""⑦ hands opening the Bible: seen from above, a book on a wooden table, two hands turning a page."""
from common import *

def main(out, stages=None):
    g, p = canvas(1616, tone='#e8a868', stages=stages)
    table = np.ones((H, W), np.float32)
    g.block_in(table, '#c8946a', angle=0, length=(90, 160), width=(16, 26))
    g.model_form(table, ['#7a4a2a', '#9a6a40', '#c8946a', '#dcae80', '#efcaa0'], steps=3, relief=0.12, height=noise2d(H, W, 300, 2, 3), angle=0)
    for k in range(24): g.line([(0, 30 + k * 82), (1080, 36 + k * 82)], 2.4, '#8a5a34', 0.35)
    g.glaze(g.poly([(0, 0), (700, 0), (1080, 600), (1080, 1400), (0, 600)]), '#fff2c8', 0.25, mode='screen', soft=60)
    g.stage('table')
    book = open_book(g, 540, 900, 900, 620, cover='#2f5a4a', seed=3)
    hand(g, 130, 1180, 1.5, -40, SKIN_JP, spread=6)
    hand(g, 960, 1150, 1.5, -150, SKIN_JP, spread=6)
    for m in (g.band([(-60, 1560), (120, 1260)], 190, 160), g.band([(1140, 1520), (980, 1240)], 190, 160)):
        g.block_in(m, '#e8c060', angle=-60); g.model_form(m, ramp('#e8c060', light=0.25, pale=0.45), steps=3, relief=0.5)
    cup(g, 860, 1600, 2.6, '#f2e6d0')
    g.line([(820, 1500), (800, 1440), (826, 1380)], 6, '#ffffff', 0.5, dry=0.4)
    leaf = g.blob(200, 1650, 120, 60, 0.1, 9, -30)
    g.block_in(leaf, '#6aa050'); g.model_form(leaf, ['#2f6a34', '#3f8a40', '#6aa050', '#8cc070', '#b8e090'], steps=3, relief=0.5)
    g.line([(110, 1700), (300, 1600)], 3, '#3f7a38', 0.8)
    finish(g, out, stages)
