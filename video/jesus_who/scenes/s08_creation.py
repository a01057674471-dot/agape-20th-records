"""④ the world and life: a bright morning over sea and green hills, a big sun, birds, a river, trees and flowers.
God is not shown as a person or as a glowing figure: only the made world."""
from common import *

def main(out, stages=None):
    g, p = canvas(808, tone='#f0b860', stages=stages)
    sky(g, '#7fc6ea', '#fff0c8', seed=1)
    g.stage('background')
    sun(g, 760, 360, 120, '#ffe680')
    cloud(g, 250, 260, 1.1, seed=2); cloud(g, 640, 560, 0.7, seed=3)
    hills(g, 780, '#8fb0c8', seed=4, amp=70, relief=0.2)                        # far blue mountains
    sea = (p.YY > 900).astype(np.float32)
    g.block_in(sea, '#5fb0d0', angle=0, length=(60, 120), width=(12, 20))
    g.glaze(sea * g.ellipse(760, 920, 160, 60), '#fff4c0', 0.6, mode='screen', soft=10)
    for k in range(18):
        x, y = (k * 137) % 1080, 930 + (k * 53) % 140
        g.line([(x, y), (x + 40, y)], 3, '#e8f8fc', 0.7)
    hill = hills(g, 1040, '#7ab85a', seed=5, amp=60, relief=0.4)
    hill2 = hills(g, 1300, '#94c868', seed=6, amp=45, relief=0.4)
    river = g.poly([(520, 1080), (600, 1080), (700, 1400), (620, 1920), (360, 1920), (520, 1400)])
    g.block_in(river * (p.YY > 1060), '#7ec4dc', angle=90, length=(30, 60), width=(10, 18))
    g.glaze(river * (p.YY > 1060) * (p.XX < 560), '#c8ecf4', 0.5, mode='screen')
    for x, y, s in ((140, 1270, 1.0), (930, 1300, 1.2), (260, 1340, 0.7)):
        trunk = g.band([(x, y), (x, y - 120 * s)], 22 * s, 14 * s)
        g.block_in(trunk, '#7a5a3a', angle=90, length=(8, 20), width=(4, 8))
        for i in range(4):
            cm = g.blob(x + (i - 1.5) * 34 * s, y - 170 * s - (i % 2) * 40 * s, 70 * s, 60 * s, 0.15, i + int(x))
            g.block_in(cm, '#4f9a48', length=(10, 24), width=(5, 10))
            g.model_form(cm, ['#2f6a34', '#3f8a40', '#4f9a48', '#7cc060', '#b0e080'], steps=4, relief=0.6, round_=0.8)
    for x, y in ((300, 560), (350, 600), (420, 540), (180, 650)):
        g.line([(x - 22, y), (x - 8, y - 12), (x, y - 2), (x + 8, y - 12), (x + 22, y)], 4, '#4a3a3a', 0.85)
    rr = np.random.default_rng(9)
    for i in range(70):
        x, y = rr.uniform(0, 1080), rr.uniform(1500, 1900)
        if 360 < x < 700: continue
        c = ['#f26a5a', '#ffd34a', '#ffffff', '#f49ac0'][i % 4]
        for a in range(5): g.dab(x + 9 * np.cos(a * 1.26), y + 9 * np.sin(a * 1.26), 6, c)
        g.dab(x, y, 4, '#f8c030')
    g.strokes((p.YY > 1350).astype(np.float32), '#5a9a40', angle=-80, length=(14, 30), width=(2, 4), density=0.5, alpha=0.8, dry=0.3, seed=10)
    finish(g, out, stages)
