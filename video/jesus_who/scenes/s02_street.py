"""① everyday Japan: a sunny shopping street, pastel buildings, a utility pole, a crosswalk, people walking by."""
from common import *

def building(g, x, y, w, h, col, win='#a8d0e0', rows=4, cols=3, awning=None, seed=0):
    m = g.poly([(x, y), (x + w, y), (x + w, 1300), (x, 1300)], smooth=False)
    g.block_in(m, col, angle=90, length=(30, 70), width=(12, 22))
    g.model_form(m, ramp(col, light=0.18, pale=0.35), steps=3, relief=0.15, height=np.zeros_like(m), angle=90,
                 length=(30, 60), width=(10, 18), bias=0.05)
    g.glaze(g.poly([(x + w - 26, y), (x + w, y), (x + w, 1300), (x + w - 26, 1300)], smooth=False), '#7a6070', 0.25)
    for r_ in range(rows):
        for c in range(cols):
            wx = x + 24 + c * (w - 48) / cols
            wy = y + 30 + r_ * 120
            if wy + 70 > 1080: continue
            wm = g.poly([(wx, wy), (wx + (w - 48) / cols - 22, wy), (wx + (w - 48) / cols - 22, wy + 72), (wx, wy + 72)], smooth=False)
            g.block_in(wm, win, length=(8, 18), width=(4, 8))
            g.glaze(wm * (g.P.XX < wx + 18), '#ffffff', 0.5, mode='screen')
            g.line([(wx, wy + 72), (wx + (w - 48) / cols - 22, wy + 72)], 3, '#ffffff', 0.7)
    if awning:
        aw = g.poly([(x + 10, 1110), (x + w - 10, 1110), (x + w + 6, 1170), (x - 6, 1170)], smooth=False)
        g.block_in(aw, awning, length=(10, 24), width=(5, 9))
        for k in range(int(w / 40)):
            xx = x + 10 + k * 40
            g.glaze(g.poly([(xx, 1110), (xx + 20, 1110), (xx + 24, 1170), (xx + 2, 1170)], smooth=False) * aw, '#fff6e8', 0.85, mode='normal')
        door = g.poly([(x + w * 0.2, 1185), (x + w * 0.8, 1185), (x + w * 0.8, 1300), (x + w * 0.2, 1300)], smooth=False)
        g.block_in(door, '#bfe0e8', length=(8, 20), width=(4, 8))
        g.glaze(door * (g.P.XX < x + w * 0.45), '#ffffff', 0.45, mode='screen')
    return m

def main(out, stages=None):
    g, p = canvas(202, tone='#e8b878', stages=stages)
    sky(g, '#8fcde8', '#e6f2ea', seed=3)
    g.stage('background')
    cloud(g, 300, 220, 1.1, seed=4); cloud(g, 860, 360, 0.7, seed=5)
    building(g, -20, 420, 330, 0, '#f2b8a0', rows=6, awning='#d9533a', seed=1)
    building(g, 300, 560, 300, 0, '#bfe0c8', rows=5, awning='#3f8a7a', seed=2)
    building(g, 590, 380, 280, 0, '#f6e0a8', rows=6, awning='#e0903a', seed=3)
    building(g, 860, 520, 260, 0, '#c8c0e8', rows=5, awning='#6a5aa8', seed=4)
    # utility pole and wires
    pole = g.band([(150, 1330), (160, 300)], 26, 22)
    g.block_in(pole, '#b8b0a8', angle=90, length=(20, 40), width=(6, 10))
    g.model_form(pole, ['#6a6460', '#8a847e', '#b8b0a8', '#d6d0c8', '#efe9e0'], steps=3, relief=0.6, angle=90)
    g.line([(110, 360), (210, 352)], 10, '#8a847e', 1.0)
    for dy in (0, 26):
        g.line([(0, 380 + dy), (160, 362 + dy), (600, 420 + dy), (1080, 330 + dy)], 2.6, '#4a4448', 0.85, taper=(0, 0))
    # pavement and road with a crosswalk
    pave = floor(g, 1300, '#e6dcc8')
    road = (g.P.YY > 1520).astype(np.float32)
    g.block_in(road, '#8a8a92', angle=0, length=(60, 120), width=(16, 28))
    for k in range(7):
        x0 = 40 + k * 150
        g.block_in(g.poly([(x0, 1560), (x0 + 90, 1560), (x0 + 70, 1920), (x0 - 20, 1920)], smooth=False), '#f6f4ee', angle=90,
                   length=(30, 60), width=(10, 18))
    g.line([(0, 1520), (1080, 1520)], 8, '#c8c0b0', 0.9)
    g.stage('scenery')
    sal = Person(g, 300, 1040, 88, skin=SKIN_JP, hair='side', hair_col=HAIR_BLACK, body='jacket', cloth='#3d4a6a',
                 look=(0.5, 0), mouth='flat', turn=0.5, arms=[[(230, 1150), (220, 1250), (240, 1330)], [(370, 1150), (400, 1250), (420, 1320)]],
                 torso=(1370, 110), legs=[[(270, 1360), (250, 1450), (230, 1500)], [(330, 1360), (350, 1440), (380, 1490)]],
                 trousers='#3d4a6a', shoes='#2a2420', seed=11)
    stu = Person(g, 560, 1080, 80, skin=SKIN_JP, hair='long', hair_col=HAIR_BLACK, body='school', cloth='#2f3e6a',
                 look=(-0.3, 0.2), mouth='smile', turn=-0.3, arms=[[(500, 1180), (480, 1270), (490, 1340)], [(620, 1180), (650, 1260), (640, 1330)]],
                 torso=(1380, 100), legs=[[(530, 1380), (520, 1450), (510, 1500)], [(590, 1380), (600, 1450), (615, 1500)]],
                 trousers='#efc9a2', shoes='#3a2a22', seed=12)
    gma = Person(g, 820, 1100, 82, skin=SKIN_JP, hair='bun', hair_col=HAIR_GREY, body='shirt', cloth='#9a6aa8',
                 look=(-0.6, 0.1), mouth='smile', turn=-0.5, age=75, arms=[[(760, 1200), (730, 1290), (720, 1360)], [(880, 1200), (900, 1280), (890, 1350)]],
                 torso=(1410, 104), legs=[[(790, 1410), (780, 1460), (770, 1500)], [(850, 1410), (860, 1460), (870, 1500)]],
                 trousers='#5a4a60', shoes='#3a2a22', seed=13)
    kid = Person(g, 980, 1250, 56, skin=SKIN_JP, hair='short', hair_col=HAIR_BLACK, body='shirt', cloth='#f2c040',
                 look=(-0.7, -0.2), mouth='open', turn=-0.6, arms=[[(940, 1320), (900, 1330), (880, 1300)], [(1020, 1320), (1040, 1380), (1036, 1420)]],
                 torso=(1440, 74), legs=[[(960, 1440), (955, 1475), (950, 1505)], [(1000, 1440), (1005, 1475), (1010, 1505)]],
                 trousers='#4a7ab0', shoes='#d04a3a', seed=14)
    people = [sal, stu, gma, kid]
    for pp in people:
        g.cast_shadow(pp.fig * (g.P.YY > pp.hy + pp.r * 3), 30, 14, soft=12, alpha=0.25, colour='#6a5a50', on=pave)
    paint_people(g, people)
    finish(g, out, stages)
