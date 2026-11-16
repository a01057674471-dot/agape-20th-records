"""「教会って、なに?」 paintings -- the church is people, one family under one head. python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *

def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), rel))
    m = importlib.util.module_from_spec(sp); sys.path.insert(0, os.path.dirname(sp.origin)); sp.loader.exec_module(m); return m
h = _load('h_shots', '../../handle/art_src/shots.py')
hj = _load('hj_shots', '../../hajimemashite/art_src/shots.py')
k = h.k
import pcommon
pcommon.ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art')
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4
COATS = [('powder', 'cornflower', 'denim', 'indigo'), ('butter', 'ochre', 'amber', 'sienna'), ('sage', 'lichen', 'moss', 'pine'),
         ('lavender', 'periwinkle', 'violet', 'indigo'), ('pink', 'rose', 'coral', 'brick'), ('sand', 'tan', 'sienna', 'brown'),
         ('cream', 'ivory', 'sand', 'tan'), ('stone', 'warmgrey', 'slate', 'umber'), ('peach', 'coral', 'terracotta', 'brick')]
HAIRS = [('hair', 'umber', 'sepia'), ('hair_light', 'hair', 'umber'), ('umber', 'sepia', 'sepia'), ('stone', 'warmgrey', 'pebble')]
WOODC = ('tan', 'sienna', 'brown', 'umber')


def bust(S, x, y, R, coat, hs='short', hair=HAIRS[0], **kw):
    m = person(S, x, y, R, coat=coat, hair_style=hs, plan=True, arms=kw.get('arms'))
    erase(S, m['mask'])
    person(S, x, y, R, coat=coat, hair_style=hs, hair=hair, **kw)
    return m['mask']


def ekklesia():
    """呼び集められた人たち: people of all kinds coming along many paths across the fields toward one warm light"""
    S = Shot(2101); p = S.p
    sky(S, 760, (540, 640, 380))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [720, 680, 700, 660, 690, 710, 680], RIDGES[0], mist=0.5)
    ground(S, 760, flowers=120)
    p.glow(540, 820, 300, strength=1.2, density=1.1)
    for (x0, y0) in ((0, 1500), (1080, 1450), (200, 1920), (880, 1920), (540, 1920)):
        path = p.tube([(x0, y0), ((x0 + 540) / 2, (y0 + 840) / 2 + 40), (540, 840)], 70, 16)
        p.form(path, ('butter', 'sand', 'cream', 'tan'), 0, LIGHT, density=1.1, seed=S.sd())
    spots = [(170, 1400, 230, 0), (330, 1180, 180, 1), (860, 1300, 210, 2), (720, 1080, 160, 3), (420, 1700, 280, 4),
             (690, 1640, 270, 5), (560, 1000, 130, 6), (940, 1650, 260, 8)]
    for (x, y, hh, c) in spots:
        figure(S, x, y, hh, coat=COATS[c], hair=HAIRS[c % 4], back=True, walk=0.4)
    S.save('ekklesia')


def gathered():
    """完璧だから集まるんじゃなく: a warm room, people who are far from perfect -- a bandaged arm, a cane, tired eyes -- smiling together"""
    S = Shot(2102); p = S.p
    hj.room(S, np.zeros((H, W), np.float32), win_box=(680, 160, 1010, 560), wall_to=1450)
    p.form(p.rect(0, 1450, 1080, 1920), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    p.glow(540, 900, 500, strength=0.6, density=0.6)
    row1 = [(250, 820, 0, 'short', 3), (540, 780, 4, 'long', 0), (830, 820, 2, 'bun', 3)]
    row2 = [(160, 1150, 5, 'short', 2), (430, 1120, 7, 'bob', 1), (700, 1120, 1, 'short', 0), (950, 1160, 3, 'long', 0)]
    for (x, y, c, hs, hr) in row1 + row2:
        bust(S, x, y, 95, COATS[c], hs=hs, hair=HAIRS[hr], smile=True, eyes_closed=(x == 540))
    p.form(p.rect(380, 1290, 480, 1330), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd())       # a sling
    p.line([(1040, 1300), (1060, 1700)], 'sienna', 8, 0.85, alpha=0.9); p.line([(1040, 1300), (1000, 1290)], 'sienna', 8, 0.85, alpha=0.9)  # cane
    p.form(p.rect(210, 870, 290, 890), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd())         # a plaster
    hm = h.heart_mask(p, 540, 560, 40); p.form(hm, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('gathered')


def table():
    """神様の家族: a long table, people of every age eating together in warm light -- and one empty chair, lit, waiting"""
    S = Shot(2103); p = S.p
    hj.room(S, np.zeros((H, W), np.float32), win_box=(80, 140, 400, 520), wall_to=1300)
    p.form(p.rect(0, 1300, 1080, 1920), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    lamp = p.poly([(440, 80), (640, 80), (700, 180), (380, 180)]); p.form(lamp, ('butter', 'gold', 'amber'), 0, LIGHT, density=1.4, seed=S.sd())
    p.glow(540, 260, 520, strength=0.9, density=0.9)
    back = [(170, 760, 5, 'bun', 3), (400, 740, 0, 'short', 0), (650, 740, 4, 'long', 1), (890, 760, 2, 'short', 2)]
    for (x, y, c, hs, hr) in back:
        bust(S, x, y, 88, COATS[c], hs=hs, hair=HAIRS[hr], smile=True)
    tb = p.poly([(40, 1020), (1040, 1020), (1080, 1180), (0, 1180)])
    erase(S, tb); p.form(tb, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, density=1.2, seed=S.sd()); p.edge(tb, 'tan', density=0.8, alpha=0.8)
    for x in (160, 380, 600, 820):
        p.form(p.ellipse(x, 1080, 70, 22), ('white', 'powder', 'stone'), 0, LIGHT, density=1.4, seed=S.sd())
        p.form(p.ellipse(x, 1074, 40, 12), ('butter', 'ochre', 'coral'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.ellipse(500, 1130, 90, 30), ('sienna', 'tan', 'butter'), 0, LIGHT, density=1.4, seed=S.sd())
    for (x, c, hs, hr) in ((260, 1, 'short', 0), (820, 6, 'long', 0)):
        bust(S, x, 1300, 92, COATS[c], hs=hs, hair=HAIRS[hr], smile=True, look=(0, -0.5))
    # the empty chair (front centre), back to us, a soft light on it
    ch = np.clip(p.rect(470, 1240, 610, 1460) + p.rect(450, 1440, 630, 1480), 0, 1)
    p.glow(540, 1360, 220, strength=1.0, density=1.0)
    erase(S, ch); p.form(ch, WOODC, 90, LIGHT, density=1.5, seed=S.sd()); p.edge(ch, 'sepia', density=0.9, alpha=0.85)
    for x in (465, 615): p.form(p.rect(x - 10, 1480, x + 10, 1640), WOODC, 0, LIGHT, density=1.5, seed=S.sd())
    p.lift(blur(p.rect(480, 1250, 600, 1300), 6), 'butter', 0.4)
    S.save('table')


def world_churches():
    """世界中に: a coloured-pencil world map with many tiny, different churches, all joined by fine golden threads"""
    S = Shot(2104); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(4, 6, 500), ['cream', 'ivory', 'butter'], (60, 150), (1.8, 2.5), 1.4, 0.55, seed=S.sd())
    sea = p.rect(60, 300, 1020, 1300)
    p.form(sea, ('sky_pale', 'powder', 'cornflower'), 0, LIGHT, density=1.0, seed=S.sd()); p.edge(sea, 'tan', density=0.7, alpha=0.7)
    lands = [(260, 520, 150, 120), (330, 860, 90, 160), (560, 500, 100, 80), (590, 820, 110, 170), (800, 520, 200, 120), (880, 720, 50, 60), (930, 1060, 90, 60)]
    for (x, y, rx, ry) in lands:
        p.form(p.blob(x, y, rx, ry, 0.25, seed=S.sd()), ('sage', 'meadow', 'moss', 'yellowgreen'), 0, LIGHT, density=1.3, seed=S.sd())
    pts = [(240, 480), (300, 560), (340, 860), (560, 480), (600, 760), (620, 900), (760, 500), (860, 560), (880, 720), (930, 1060), (300, 920), (700, 480)]
    rr = np.random.default_rng(3)
    for i, (x, y) in enumerate(pts):
        for (x2, y2) in pts[i + 1:i + 3]:
            p.line(curve([(x, y), ((x + x2) / 2, min(y, y2) - 60), (x2, y2)], 30), 'gold', 2.4, 0.8, alpha=0.8)
    for i, (x, y) in enumerate(pts):
        s = rr.uniform(0.7, 1.2); cols = [('white', 'cream', 'ivory'), ('peach', 'apricot', 'terracotta'), ('powder', 'sky_pale', 'cornflower'), ('butter', 'sand', 'tan')][i % 4]
        ch = np.clip(p.rect(x - 20 * s, y - 24 * s, x + 20 * s, y + 10 * s) + p.poly([(x - 26 * s, y - 22 * s), (x, y - 50 * s), (x + 26 * s, y - 22 * s)]), 0, 1)
        if i % 3 == 1: ch = np.clip(ch + p.rect(x + 10 * s, y - 60 * s, x + 22 * s, y - 20 * s), 0, 1)
        erase(S, ch); p.form(ch, cols + (cols[-1],), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(ch, 'sienna', density=0.9, alpha=0.85)
        p.form(np.clip(p.rect(x - 2, y - 72 * s, x + 2, y - 48 * s) + p.rect(x - 8 * s, y - 66 * s, x + 8 * s, y - 62 * s), 0, 1), ('brick', 'red', 'red'), 0, LIGHT, density=1.6, seed=S.sd())
        p.glow(x, y - 20, 40, strength=0.5, density=0.5)
    S.save('world_churches')


def circle():
    """からだは、ひとつ: people of many nations and ages standing hand in hand in a great circle round a warm light"""
    S = Shot(2105); p = S.p
    sky(S, 900, (540, 700, 420))
    ground(S, 900, flowers=100)
    cx, cy, rx, ry = 540, 1150, 400, 230
    p.glow(cx, cy - 80, 360, strength=1.4, density=1.2)
    p.lift(blur(p.ellipse(cx, cy - 60, 90, 90), 30), 'white', 0.8)
    n = 12; people = []
    for j in range(n):
        a = np.pi * (0.5 + 2 * j / n)
        x, y = cx + rx * np.cos(a), cy + ry * np.sin(a)
        people.append((y, x, j))
    for (y, x, j) in sorted(people):
        hh = 260 + (y - (cy - ry)) / (2 * ry) * 160
        skin = SKIN if j % 3 else ('skin_shade', 'sienna', 'brown')
        figure(S, x, y + hh * 0.5, hh, coat=COATS[j % len(COATS)], hair=HAIRS[j % 4], back=(y < cy), legs=('slate', 'umber', 'sepia'))
    for j in range(n):                                                   # the joined hands
        a1, a2 = np.pi * (0.5 + 2 * j / n), np.pi * (0.5 + 2 * (j + 1) / n)
        x1, y1 = cx + rx * np.cos(a1), cy + ry * np.sin(a1); x2, y2 = cx + rx * np.cos(a2), cy + ry * np.sin(a2)
        hy1 = y1 + (260 + (y1 - (cy - ry)) / (2 * ry) * 160) * 0.05; hy2 = y2 + (260 + (y2 - (cy - ry)) / (2 * ry) * 160) * 0.05
        p.line([(x1, hy1), (x2, hy2)], 'skin_shade', 4, 0.7, alpha=0.6)
    S.save('circle')


def road_ages():
    """2000年前の弟子たちも: one long road to the sunrise; people of every age walk it together -- robed disciples far back,
    then later travellers, then people of today in front -- the past fading softly"""
    S = Shot(2106); p = S.p
    sky(S, 720, None)
    p.glow(540, 700, 480, strength=1.5, density=1.3)
    p.lift(p.ellipse(540, 710, 80, 80) * (p.YY < 720), 'white', 0.95, tooth=0)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [700, 660, 690, 720, 680, 650, 690], RIDGES[0], mist=0.6)
    ground(S, 720, flowers=120)
    road = p.poly(curve([(500, 720), (580, 720), (760, 1100), (980, 1920), (120, 1920), (320, 1100), (500, 720)], 80), smooth=True)
    p.form(road, ('butter', 'sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, density=1.2, seed=S.sd())
    groups = [(520, 840, 110, ('white', 'cream', 'ivory', 'sand'), 0.55), (590, 880, 120, ('sand', 'tan', 'sienna', 'brown'), 0.55),
              (470, 980, 150, ('cream', 'ivory', 'sand', 'tan'), 0.4), (620, 1040, 160, ('slate', 'umber', 'sepia', 'sepia'), 0.4),
              (400, 1220, 220, COATS[3], 0.2), (680, 1260, 230, COATS[1], 0.2),
              (330, 1560, 330, COATS[0], 0.0), (560, 1620, 340, COATS[4], 0.0), (780, 1580, 320, COATS[2], 0.0)]
    for (x, y, hh, c, fade) in groups:
        m = figure(S, x, y, hh, coat=c, hair=HAIRS[0], back=True, walk=0.4)
        if fade: p.lift(blur(m, 3), 'cream', fade)
    S.save('road_ages')


def worship():
    """日曜日に集まって: a small Japanese church on Sunday -- a few people with Bibles open, singing and praying, a wooden cross"""
    S = Shot(2107); p = S.p
    wall = (p.YY < 1300).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'ivory', 'sand'], (60, 140), (1.8, 2.5), 1.6, 0.6, alpha=0.65, seed=S.sd())
    cr = np.clip(p.rect(520, 160, 560, 620) + p.rect(410, 280, 670, 318), 0, 1)
    erase(S, cr); p.form(cr, ('butter', 'ochre', 'tan', 'sienna'), 90, LIGHT, density=1.6, seed=S.sd()); p.edge(cr, 'sienna', density=0.8, alpha=0.8)
    p.glow(540, 380, 360, strength=0.7, density=0.7)
    for x in (100, 980):
        p.window(x - 70, 300, x + 70, 620, panes=(1, 3), glow=0.6, seed=S.sd())
    p.form(p.rect(0, 1300, 1080, 1920), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    people = [(220, 900, 4, 'long', 0, True), (440, 880, 0, 'short', 2, False), (660, 880, 5, 'bun', 3, True), (880, 900, 2, 'bob', 1, False)]
    for (x, y, c, hs, hr, closed) in people:
        bust(S, x, y, 92, COATS[c], hs=hs, hair=HAIRS[hr], eyes_closed=closed, smile=True)
        bk = p.poly([(x - 70, y + 230), (x, y + 245), (x + 70, y + 230), (x + 70, y + 300), (x, y + 315), (x - 70, y + 300)])
        erase(S, bk); p.form(bk, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(bk, 'tan', density=0.8, alpha=0.8)
        p.line([(x, y + 245), (x, y + 315)], 'tan', 2, 0.7, alpha=0.8)
    for (x, y) in ((340, 640), (760, 620), (560, 720)):
        p.form(p.ellipse(x, y, 16, 12, rot=-20), ('butter', 'gold', 'amber'), 0, LIGHT, density=1.5, seed=S.sd())
        p.line([(x + 14, y), (x + 14, y - 60), (x + 40, y - 46)], 'ochre', 4, 0.85, alpha=0.9)
    pew = p.rect(0, 1240, 1080, 1320); erase(S, pew); p.form(pew, WOODC, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('worship')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
