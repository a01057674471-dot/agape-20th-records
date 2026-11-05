"""⑥ the third morning (re-creation): a garden tomb cut in the rock at sunrise; the round stone rolled aside, the
doorway open and empty, folded linen inside catching the light; spring flowers."""
from common import *

def main(out, stages=None):
    g, p = canvas(1414, tone='#f0b070', stages=stages)
    sky(g, '#bfe0ee', '#ffe2b0', seed=2, angle=-20)
    g.stage('background')
    sun(g, 900, 820, 110, '#fff0a0')
    cloud(g, 300, 300, 1.0, col='#fff8f0', seed=3)
    hills(g, 980, '#b8c890', seed=4, amp=40, relief=0.2)
    rock = g.poly([(-40, 1500), (-40, 620), (120, 520), (380, 500), (600, 560), (720, 700), (760, 1000), (780, 1500)])
    g.block_in(rock, '#d8c4a4', angle=-60, length=(40, 90), width=(14, 24))
    g.model_form(rock, ['#8a7460', '#a8907a', '#c8b092', '#e0ceb0', '#f2e6cc'], steps=4, relief=0.5, angle='fall')
    for k in range(14):
        x = 40 + k * 50
        g.line([(x, 640 + (k % 3) * 30), (x + 30, 700 + (k % 4) * 40)], 3, '#9a8068', 0.4)
    door = g.poly([(260, 1240), (260, 1010), (300, 930), (380, 900), (460, 930), (500, 1010), (500, 1240)])
    g.block_in(door, '#5a4a40', length=(10, 24), width=(5, 10))
    g.glaze(door * (p.YY > 1080), '#8a7464', 0.6, mode='normal', soft=20)
    linen = g.blob(380, 1200, 80, 22, 0.08, 5)
    g.block_in(linen, '#f8f2e2', length=(8, 16), width=(3, 6))
    g.glaze(linen * (p.YY < 1195), '#ffffff', 0.6, mode='screen')
    g.line([(320, 1205), (440, 1200)], 2, '#c8b898', 0.7)
    g.glaze(g.poly([(500, 900), (1080, 700), (1080, 1100), (500, 1240)]), '#fff4c8', 0.35, mode='screen', soft=40)   # morning light
    ground = floor(g, 1240, '#a8c878')
    stone = g.ellipse(660, 1080, 170, 175)
    g.cast_shadow(stone, 30, 20, soft=20, alpha=0.35, colour='#5a5a40', on=np.maximum(rock, ground))
    g.block_in(stone, '#c8b496', length=(20, 40), width=(8, 14))
    g.sphere_shade(660, 1080, 170, 175, ['#7a6a58', '#9a8670', '#c0aa8e', '#dcc8aa', '#efe0c4'], steps=4, mask=stone)
    th = np.linspace(0, 2 * np.pi, 60)
    g.line(np.stack([660 + 110 * np.cos(th), 1080 + 114 * np.sin(th)], 1), 4, '#9a8670', 0.5, taper=(0, 0))
    rr = np.random.default_rng(6)
    for i in range(80):
        x, y = rr.uniform(0, 1080), rr.uniform(1300, 1900)
        c = ['#f6f2ea', '#ffd34a', '#f49ac0', '#c8a0f0'][i % 4]
        for a in range(5): g.dab(x + 8 * np.cos(a * 1.26), y + 8 * np.sin(a * 1.26), 6, c)
        g.dab(x, y, 3.5, '#f8c030')
    g.strokes((p.YY > 1260).astype(np.float32), '#6a9a48', angle=-80, length=(14, 30), width=(2, 4), density=0.45, alpha=0.8, dry=0.3, seed=9)
    finish(g, out, stages)
