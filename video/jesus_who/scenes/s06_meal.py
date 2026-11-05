"""③ sharing a meal: Jesus at a low table in a courtyard under a vine, laughing with a tax collector, a young
fisherman and a woman; bread, fish, grapes, cups."""
from common import *

def main(out, stages=None):
    g, p = canvas(606, tone='#e8a868', stages=stages)
    jesus = Person(g, 540, 860, 128, skin=SKIN_OLIVE, hair='curly', hair_col=HAIR_DARK, beard='short', cloth='#efe2c4',
                   stripe='#8a5a3a', mantle='#b8643c', look=(-0.4, 0.1), mouth='open', seed=1,
                   arms=[[(450, 1020), (430, 1130), (480, 1230)], [(630, 1020), (690, 1120), (720, 1220)]], torso=(1300, 200))
    tax = Person(g, 200, 960, 112, skin=SKIN_LIGHT, hair='bald', hair_col=HAIR_DARK, beard='full', cloth='#6a4a9a',
                 stripe='#e0b040', look=(0.6, 0), mouth='open', turn=0.6, seed=2, brows=0.8,
                 arms=[[(120, 1100), (140, 1200), (230, 1250)], [(280, 1100), (330, 1180), (360, 1240)]], torso=(1300, 170))
    fish = Person(g, 870, 960, 112, skin=SKIN_DEEP, hair='curly', hair_col=HAIR_BLACK, beard=None, cloth='#3f7a8a',
                  look=(-0.6, 0), mouth='smile', turn=-0.6, seed=3,
                  arms=[[(800, 1100), (760, 1200), (720, 1250)], [(950, 1100), (980, 1200), (930, 1260)]], torso=(1300, 170))
    wom = Person(g, 360, 1020, 96, skin=SKIN_OLIVE, hair='scarf', scarf_col='#e08a3a', cloth='#c9564a', look=(0.5, -0.2),
                 mouth='smile', turn=0.4, seed=4, arms=[[(300, 1140), (320, 1220), (380, 1250)]], torso=(1300, 140))
    people = [tax, fish, wom, jesus]
    figs = np.maximum.reduce([pp.fig for pp in people])
    wall = (p.YY < 1180).astype(np.float32)
    g.block_in(wall * (1 - figs), '#f0d8ac', angle=0, length=(50, 110), width=(14, 26))
    g.model_form(wall * (1 - figs), ramp('#f0d8ac', light=0.2, pale=0.4), steps=3, relief=0.15, height=np.zeros_like(wall), angle=0)
    for k in range(14):
        y = 160 + k * 72
        g.line([(0, y), (1080, y + 4)], 2.4, '#c8a878', 0.35)
    # an arched doorway with blue sky beyond, and a vine with leaves and grapes across the top
    arch = g.poly([(380, 760), (380, 420), (420, 330), (540, 290), (660, 330), (700, 420), (700, 760)]) * (1 - figs)
    g.block_in(arch, '#a8d8ea', length=(16, 36), width=(6, 12))
    g.glaze(arch * (p.YY > 600), '#cfe8c0', 0.6, mode='normal')
    g.line([(0, 140), (300, 190), (600, 150), (1080, 200)], 16, '#7a5a3a', 0.95)
    rr = np.random.default_rng(7)
    for i in range(46):
        x = rr.uniform(0, 1080); y = 160 + 40 * np.sin(x / 200) + rr.uniform(-20, 70)
        lf = g.blob(x, y, rr.uniform(26, 40), rr.uniform(20, 30), 0.25, i, rr.uniform(0, 180))
        g.block_in(lf, ['#6a9a4a', '#88b05a', '#5a8a42'][i % 3], length=(6, 14), width=(3, 6))
    for x, y in ((240, 260), (820, 290), (620, 230)):
        for k in range(9):
            g.dab(x + (k % 3) * 14 - 14 + (k // 3) * 4, y + (k // 3) * 14, 9, '#6a3a7a')
            g.dab(x + (k % 3) * 14 - 17 + (k // 3) * 4, y + (k // 3) * 14 - 3, 3, '#c8a0d8')
    g.stage('room')
    paint_people(g, people)
    table = g.poly([(0, 1240), (1080, 1240), (1080, 1460), (0, 1460)], smooth=False)
    g.cast_shadow(table, 0, 30, soft=20, alpha=0.35, colour='#6a4030')
    g.block_in(table, '#b07a4a', angle=0, length=(60, 120), width=(12, 22))
    g.model_form(table, ['#6a4028', '#8a5a36', '#b07a4a', '#cc9a66', '#e6bc88'], steps=3, relief=0.2, height=np.zeros_like(table), angle=0)
    for k in range(5): g.line([(0, 1280 + k * 36), (1080, 1282 + k * 36)], 2, '#7a4a2a', 0.4)
    floor(g, 1460, '#d8b888')
    g.block_in(g.ellipse(540, 1260, 230, 50), '#f2e6cc', length=(20, 40), width=(8, 14))     # a plate with two fish
    for dx in (-80, 70):
        f = g.blob(540 + dx, 1255, 80, 24, 0.03, dx + 200, 4)
        g.block_in(f, '#b8c8d0', length=(8, 16), width=(4, 7))
        g.model_form(f, ['#5a7080', '#7a92a0', '#a8bcc6', '#d0dce2', '#eef4f6'], steps=3, relief=0.6)
        g.dab(540 + dx - 60, 1250, 4, '#1a1a1a')
        g.line([(540 + dx + 78, 1255), (540 + dx + 100, 1238), (540 + dx + 100, 1272), (540 + dx + 78, 1255)], 5, '#8aa0ac', 0.9)
    bread(g, 250, 1280, 90, 40, seed=1); bread(g, 840, 1290, 80, 36, seed=2)
    for x, y in ((380, 1300), (690, 1300)): cup(g, x, y, 1.3, '#c8784a')
    for k in range(14):                                 # grapes in a bowl
        g.dab(980 + (k % 5) * 16 - 32, 1280 + (k // 5) * 14, 10, '#7a4a8a'); g.dab(976 + (k % 5) * 16 - 32, 1276 + (k // 5) * 14, 3, '#d8b8e8')
    finish(g, out, stages)
