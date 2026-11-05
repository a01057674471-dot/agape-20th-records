"""② a 1st-century hill town (re-creation): flat-roofed stone houses climbing a hill, olive trees and a palm,
a well where a woman fills a jar, a man leading a donkey along the path. Bright midday."""
from common import *

def donkey(g, x, y, s=1.0):
    body = g.blob(x, y, 90 * s, 48 * s, 0.03, 1)
    head = g.blob(x - 105 * s, y - 50 * s, 34 * s, 26 * s, 0.03, 2, -30)
    neck = g.band([(x - 60 * s, y - 10 * s), (x - 95 * s, y - 45 * s)], 40 * s, 30 * s)
    legs = [g.band([(x + dx * s, y + 20 * s), (x + dx * s + 2, y + 95 * s)], 16 * s, 12 * s) for dx in (-60, -35, 45, 70)]
    ears = [g.band([(x - 100 * s, y - 70 * s), (x - 92 * s + k * 14, y - 112 * s)], 12 * s, 6 * s) for k in (0, 1)]
    m = np.maximum.reduce([body, head, neck] + legs + ears)
    g.cast_shadow(m, 10, 20, soft=12, alpha=0.3, colour='#7a5a40')
    g.block_in(m, '#9a8f86', length=(10, 24), width=(5, 10))
    g.model_form(m, ['#5a524e', '#7a706a', '#9a8f86', '#bdb4aa', '#ddd6cc'], steps=4, relief=0.55, length=(10, 22), width=(4, 9))
    g.glaze(g.ellipse(x - 128 * s, y - 40 * s, 14 * s, 12 * s), '#e8e0d6', 0.8, mode='normal')
    g.dab(x - 108 * s, y - 58 * s, 4.5 * s, '#1a1410', 0.95)
    g.line([(x + 88 * s, y - 10 * s), (x + 110 * s, y + 40 * s)], 5 * s, '#5a524e', 0.9)
    g.block_in(g.blob(x + 5 * s, y - 34 * s, 50 * s, 22 * s, 0.05, 3), '#c0553a', length=(8, 16), width=(4, 8))
    return m

def main(out, stages=None):
    g, p = canvas(404, tone='#e8b070', stages=stages)
    sky(g, '#8ccbe6', '#f2ecd6', seed=3)
    g.stage('background')
    cloud(g, 780, 200, 1.0, seed=4); cloud(g, 180, 330, 0.7, seed=6)
    hills(g, 560, '#c9b88e', seed=1, amp=50, relief=0.2)
    hill = hills(g, 700, '#dcc28c', seed=2, amp=70, relief=0.3)
    rr = np.random.default_rng(5)
    rows = [(640, 7, 0.55), (760, 6, 0.7), (900, 5, 0.85)]
    for y0, n, sc in rows:
        for i in range(n):
            w = rr.uniform(150, 210) * sc
            x = i * 1080 / n + rr.uniform(-20, 20)
            stone_house(g, x, y0 + rr.uniform(-25, 25), w, w * rr.uniform(0.6, 0.8), col=['#efd6a6', '#ead0a0', '#f4dfb6', '#e6c896'][i % 4],
                        win=1, seed=int(y0 + i))
    olive_tree(g, 120, 1180, 1.0, seed=7); palm(g, 930, 1180, 1.2, seed=8); olive_tree(g, 700, 1150, 0.8, seed=9)
    path = g.poly([(380, 1920), (700, 1920), (620, 1250), (520, 1250)])
    near = floor(g, 1160, '#e4c88e')
    g.block_in(path, '#f2dcae', angle=90, length=(40, 90), width=(14, 24))
    well = g.poly([(150, 1360), (350, 1360), (340, 1500), (160, 1500)], smooth=False)
    g.cast_shadow(well, 20, 20, soft=16, alpha=0.3, colour='#8a6a4a', on=near)
    g.block_in(well, '#cfb48a', angle=0, length=(16, 36), width=(6, 12))
    g.model_form(well, ramp('#cfb48a', light=0.2, pale=0.4), steps=3, relief=0.4, length=(14, 30), width=(5, 10))
    g.glaze(g.ellipse(250, 1360, 100, 22), '#4a3a30', 0.85, mode='normal')
    for k in range(6):
        g.line([(160 + k * 34, 1370), (162 + k * 34, 1500)], 2, '#9a7a5a', 0.5)
    g.stage('scenery')
    wom = Person(g, 440, 1300, 64, skin=SKIN_OLIVE, hair='scarf', scarf_col='#d9a03a', cloth='#3f7a8a',
                 look=(-0.6, 0.2), mouth='smile', turn=-0.5, arms=[[(400, 1380), (370, 1420), (350, 1400)], [(490, 1380), (510, 1300), (500, 1240)]],
                 torso=(1540, 90), seed=21)
    man = Person(g, 820, 1360, 70, skin=SKIN_DEEP, hair='curly', hair_col=HAIR_DARK, beard='short', cloth='#e9dcc0',
                 stripe='#6a4a3a', look=(-0.6, 0), mouth='smile', turn=-0.5, arms=[[(770, 1450), (720, 1520), (680, 1540)], [(870, 1450), (890, 1540), (880, 1600)]],
                 torso=(1640, 96), seed=22)
    paint_people(g, [wom, man])
    jar = g.poly([(486, 1200), (514, 1200), (530, 1225), (522, 1260), (478, 1260), (470, 1225)])
    g.block_in(jar, '#c8784a', length=(6, 12), width=(3, 6)); g.model_form(jar, ramp('#c8784a'), steps=3, relief=0.6)
    donkey(g, 560, 1610, 1.1)
    g.line([(680, 1540), (640, 1560), (470, 1560)], 3, '#5a3a2a', 0.85)
    finish(g, out, stages)
