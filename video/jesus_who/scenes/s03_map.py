"""② a simple painted map of the land where Jesus lived, ~2000 years ago: the coast of the Mediterranean, the Sea of
Galilee, the Jordan river and the Dead Sea; Nazareth, Jerusalem; an arrow far to the east toward Japan."""
from common import *

def main(out, stages=None):
    g, p = canvas(303, tone='#e0b070', stages=stages)
    X, Y = p.XX, p.YY
    # land fills the board; the sea is everything west of a wobbly coastline
    coast_x = 330 - (Y - 200) * 0.085 + 22 * np.sin(Y / 140) + 10 * np.sin(Y / 47)
    sea = smoothstep(-2, 2, coast_x - X)
    land = 1 - sea
    g.block_in(land, '#ecd29a', angle=-20, length=(60, 120), width=(16, 30))
    g.model_form(land, ramp('#ecd29a', light=0.2, pale=0.4), steps=3, relief=0.1, height=noise2d(H, W, 260, 3, 5),
                 angle=-20, length=(50, 100), width=(14, 24))
    # hill country: soft green-ochre patches
    for cx, cy, rx, ry, c in ((600, 520, 260, 200, '#c9c48a'), (560, 1260, 220, 300, '#d8bf86'), (840, 900, 200, 380, '#e2c890')):
        g.glaze(g.blob(cx, cy, rx, ry, 0.2, cx) * land, c, 0.6, mode='normal', soft=20)
    g.block_in(sea, '#7fc0d8', angle=-60, length=(60, 120), width=(16, 28))
    g.model_form(sea, ['#4a8ab0', '#62a4c4', '#7fc0d8', '#a6d6e6', '#d0eef4'], steps=3, relief=0.1,
                 height=noise2d(H, W, 220, 3, 6), angle=-60)
    for k in range(9):                                  # little wave marks
        wx, wy = 70 + (k % 3) * 80, 380 + k * 150
        g.line([(wx, wy), (wx + 16, wy - 8), (wx + 32, wy), (wx + 48, wy - 8)], 3, '#e8f6fa', 0.8)
    coast = np.stack([coast_x[:, 0] * 0 + np.array([330 - (y - 200) * 0.085 + 22 * np.sin(y / 140) + 10 * np.sin(y / 47) for y in range(H)]), np.arange(H)], 1)[::6]
    g.line(coast, 4, '#5a8aa0', 0.8, taper=(0, 0))
    g.stage('land')
    # Sea of Galilee, the Jordan, the Dead Sea
    gal = g.blob(705, 640, 46, 70, 0.08, 7, 8)
    dead = g.blob(705, 1420, 58, 190, 0.08, 8, 2)
    jordan = [(700, 725), (690, 820), (712, 920), (692, 1020), (714, 1120), (700, 1230)]
    for m in (gal, dead):
        g.block_in(m, '#6ab4d0', length=(10, 24), width=(5, 9))
        g.glaze(m * (X < 690), '#a6d6e6', 0.5, mode='screen')
    g.line(jordan, 7, '#6ab4d0', 0.95, taper=(0.1, 0.1))
    g.line([(700, 545), (712, 470), (730, 380)], 5, '#6ab4d0', 0.9, taper=(0.1, 0.6))
    # towns
    for x, y in ((560, 700), (590, 1350)):
        g.dab(x, y, 20, '#c0392b', 0.95); g.dab(x, y, 9, '#fff6e4', 0.95)
    paint_text(g, 'ナザレ', 560, 760, 44)
    paint_text(g, 'エルサレム', 560, 1410, 44)
    paint_text(g, 'ガリラヤ湖', 840, 600, 32, '#2a5a74')
    paint_text(g, 'ヨルダン川', 800, 1000, 30, '#2a5a74', anchor='lm')
    paint_text(g, '死海', 830, 1420, 32, '#2a5a74', anchor='lm')
    paint_text(g, '地中海', 150, 960, 46, '#f4fbfd', weight=900)
    # compass rose and the long arrow east to Japan
    g.line([(960, 300), (960, 200)], 6, '#3a2418', 0.9, taper=(0, 0.0))
    g.line([(942, 240), (960, 196), (978, 240)], 6, '#3a2418', 0.9)
    paint_text(g, 'N', 960, 175, 34)
    arr = [(820, 1760), (920, 1740), (1040, 1700)]
    g.line(arr, 10, '#c0392b', 0.95, taper=(0, 0))
    g.line([(1000, 1670), (1050, 1698), (1010, 1736)], 10, '#c0392b', 0.95)
    paint_text(g, '日本は ずっと東', 990, 1810, 38, '#c0392b', anchor='rm')
    g.stage('labels')
    finish(g, out, stages)
