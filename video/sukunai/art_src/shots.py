"""「なぜ日本には、クリスチャンが少ないの?」 paintings -- history, the household, the crowd; the hidden believers;
the shepherd who goes after the one. python3 shots.py NAME"""
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
erase, figure, sky, ground, ridge, RIDGES, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.SKIN4
gassho = k.gassho
COAT, HAIR = hj.SANGHEE, hj.HAIR
EDO = [('indigo', 'slate', 'cobalt', 'umber'), ('sienna', 'brown', 'terracotta', 'umber'), ('olive', 'moss', 'sage', 'pine'),
       ('stone', 'warmgrey', 'slate', 'umber')]


def paper_bg():
    """a plain warm cream sheet for the numbers"""
    S = Shot(2701); p = S.p
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['cream', 'ivory', 'apricot'], (60, 140), (1.8, 2.5), 1.4, 0.55, alpha=0.5, seed=S.sd())
    p.glow(540, 760, 700, strength=0.5, density=0.6)
    S.save('paper_bg')


def dusk_sky(S, y1):
    p = S.p; m = (p.YY < y1).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['lavender', 'periwinkle', 'mauve'], (60, 150), (1.8, 2.5), 1.6, 0.66, seed=S.sd())
    p.hatch(m * p.value(0.0, 1.0, 0, y1), p.flow(-2, 4), ['apricot', 'peach', 'butter'], (60, 140), (1.8, 2.4), 1.4, 0.66, alpha=0.75, seed=S.sd())
    return m


def kosatsu():
    """250年以上も禁止: an Edo village entrance at dusk, an old wooden notice board on posts under a small roof; tense and quiet"""
    S = Shot(2702); p = S.p
    dusk_sky(S, 1000)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [900, 840, 880, 820, 860, 900, 860], RIDGES[1], mist=0.4)
    ground(S, 1000, cols=('sand', 'tan', 'ochre', 'olive'), flowers=0)
    for (x, y, w_) in ((120, 1000, 230), (900, 990, 260)):
        hs = p.rect(x - w_ / 2, y - 140, x + w_ / 2, y); erase(S, hs); p.form(hs, ('tan', 'sienna', 'brown', 'umber'), 90, LIGHT, density=1.4, seed=S.sd())
        rf = p.poly([(x - w_ / 2 - 40, y - 130), (x, y - 260), (x + w_ / 2 + 40, y - 130)]); erase(S, rf)
        p.form(rf, ('ochre', 'tan', 'sienna', 'umber'), p.flow(70, 6), LIGHT, density=1.6, seed=S.sd())
        p.window(x - 40, y - 110, x + 10, y - 60, panes=(1, 2), glow=0.5, seed=S.sd())
    road = p.poly([(500, 1000), (580, 1000), (900, 1920), (180, 1920)])
    p.form(road, ('sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.2, seed=S.sd())
    posts = np.clip(p.rect(300, 700, 330, 1330) + p.rect(750, 700, 780, 1330), 0, 1)
    board = p.rect(270, 760, 810, 1120)
    roof = p.poly([(220, 770), (540, 640), (860, 770), (830, 790), (540, 680), (250, 790)])
    erase(S, np.clip(posts + board + roof, 0, 1))
    p.form(posts, ('brown', 'umber', 'sepia'), 90, LIGHT, density=1.6, seed=S.sd())
    p.form(roof, ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(board, ('sand', 'tan', 'ochre', 'sienna'), 90, LIGHT, length=(30, 60), density=1.5, seed=S.sd())
    for j in range(4): p.line([(270, 760 + j * 90), (810, 760 + j * 90)], 'umber', 3, 0.7, alpha=0.6)
    rr = np.random.default_rng(5)
    for c in range(9):                                 # unreadable brushed columns
        x = 760 - c * 56
        y = 790 + rr.uniform(0, 20)
        while y < 1080:
            L_ = rr.uniform(12, 30); p.line([(x + rr.uniform(-6, 6), y), (x + rr.uniform(-6, 6), y + L_)], 'sepia', 4.5, 0.85, alpha=0.85); y += L_ + rr.uniform(8, 18)
    p.edge(board, 'sepia', density=0.9, alpha=0.85)
    S.save('kosatsu')


def terauke():
    """お寺に登録: villagers lining up before a temple while a monk writes their names in a big record book"""
    S = Shot(2703); p = S.p
    sky(S, 900, (860, 260, 300))
    tem = p.rect(140, 520, 940, 900); erase(S, tem)
    p.form(tem, ('cream', 'sand', 'tan', 'sienna'), 90, LIGHT, density=1.4, seed=S.sd())
    for x in np.linspace(180, 900, 7): p.form(p.rect(x - 14, 520, x + 14, 900), ('brick', 'sienna', 'brown'), 90, LIGHT, density=1.5, seed=S.sd())
    rf = p.poly(curve([(40, 560), (200, 470), (380, 360), (540, 330), (700, 360), (880, 470), (1040, 560)], 40) .tolist() + [(940, 520), (140, 520)])
    erase(S, rf); p.form(rf, ('slate', 'indigo', 'umber', 'sepia'), p.flow(80, 6), LIGHT, density=1.6, seed=S.sd())
    p.edge(rf, 'sepia', density=0.9, alpha=0.8)
    ground(S, 900, cols=('sand', 'cream', 'stone', 'tan'), flowers=0)
    for j in range(3): p.form(p.rect(300 - j * 30, 900 + j * 30, 780 + j * 30, 930 + j * 30), ('stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.4, seed=S.sd())
    desk = p.rect(560, 1140, 960, 1230)
    MA = [[(830, 1060), (790, 1130), (740, 1150)], [(950, 1060), (980, 1130), (900, 1150)]]
    mk = person(S, 880, 900, 95, coat=('slate', 'umber', 'sepia', 'sepia'), hair_style='none', plan=True, arms=MA, cut=desk)
    erase(S, mk['mask'])
    person(S, 880, 900, 95, coat=('slate', 'umber', 'sepia', 'sepia'), hair_style='none', arms=MA, cut=desk, eyes_closed=False, smile=False, look=(-0.4, 0.6))
    erase(S, desk); p.form(desk, ('brown', 'sienna', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    bk = p.rect(600, 1100, 840, 1150); erase(S, bk); p.form(bk, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd())
    p.line([(720, 1100), (720, 1150)], 'tan', 3, 0.8, alpha=0.8)
    for q in range(3):
        p.line([(620, 1112 + q * 12), (700, 1112 + q * 12)], 'sepia', 2, 0.7, alpha=0.6); p.line([(740, 1112 + q * 12), (820, 1112 + q * 12)], 'sepia', 2, 0.7, alpha=0.6)
    for j, (x, y, hh) in enumerate(((470, 1330, 300), (330, 1420, 330), (190, 1520, 360), (60, 1620, 390))):
        figure(S, x, y, hh, coat=EDO[j % 4], hair=('hair', 'umber', 'sepia'), back=True, legs=('stone', 'warmgrey', 'umber'))
    S.save('terauke')


def umbrella(S, x, y, r, cols):
    p = S.p
    m = p.ellipse(x, y, r, r * 0.55) * (p.YY < y + 4)
    erase(S, m); p.form(m, cols, p.radial(x, y, 90), LIGHT, length=(14, 30), density=1.5, seed=S.sd())
    for a in np.linspace(-0.8, 0.8, 5):
        p.line([(x, y - r * 0.55), (x + r * np.sin(a), y - r * 0.55 * np.cos(a) * 0.1)], 'umber', 1.8, 0.6, alpha=0.4)
    p.edge(m, 'umber', density=0.8, alpha=0.7)
    p.line([(x, y - r * 0.6), (x, y - r * 0.68)], 'umber', 3, 0.8, alpha=0.9)


def umbrellas():
    """みんなと同じ: a crowd under identical grey umbrellas in the rain; one person holds a warm-coloured one, a little hesitant"""
    S = Shot(2704); p = S.p
    m = (p.YY < 700).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['stone', 'powder', 'warmgrey'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    for x0 in (0, 280, 600, 860):
        b = p.rect(x0, 260 + (x0 % 3) * 40, x0 + 240, 760); erase(S, b); p.form(b, ('stone', 'warmgrey', 'slate'), 90, LIGHT, density=1.3, seed=S.sd())
        for yy in range(320 + (x0 % 3) * 40, 700, 110):
            for xx in (x0 + 40, x0 + 140): p.window(xx, yy, xx + 60, yy + 70, panes=(1, 1), glow=0.2, seed=S.sd())
    p.form((p.YY >= 700).astype(np.float32), ('stone', 'pebble', 'warmgrey', 'slate'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    rr = np.random.default_rng(2)
    rows = [(860, 170, 6), (1120, 210, 5), (1420, 250, 4)]
    for ri, (yb, hh, n) in enumerate(rows):
        xs = np.linspace(120, 960, n) + rr.uniform(-30, 30, n)
        for j, x in enumerate(xs):
            warm = (ri == 1 and j == 2)
            figure(S, x, yb, hh, coat=(('peach', 'coral', 'terracotta', 'brick') if warm else ('stone', 'warmgrey', 'slate', 'umber')),
                   hair=('hair', 'umber', 'sepia'), back=not warm, legs=('stone', 'warmgrey', 'umber'))
            umbrella(S, x, yb - hh * (0.86 if warm else 0.98), hh * 0.62,
                     ('apricot', 'coral', 'tangerine', 'terracotta') if warm else ('stone', 'warmgrey', 'slate', 'pebble'))
    for _ in range(300):
        x, y = rr.uniform(0, W), rr.uniform(0, H); L_ = rr.uniform(24, 44)
        p.line([(x, y), (x - 6, y + L_)], 'cornflower', 2.4, 0.7, alpha=0.6)
    S.save('umbrellas')


def hidden_prayer():
    """ひそかに信仰を守り続けた人たち: an Edo family praying quietly by a small oil lamp in a hidden room, shadows around them"""
    S = Shot(2705); p = S.p
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['umber', 'sepia', 'indigo'], (60, 140), (1.8, 2.5), 1.8, 0.8, seed=S.sd())
    p.form((p.YY >= 1250).astype(np.float32), ('brown', 'umber', 'sepia'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    for y in (1250, 1450, 1650): p.line([(0, y), (1080, y)], 'sepia', 3, 0.7, alpha=0.5)
    p.glow(540, 1150, 620, strength=1.3, density=1.2)
    fam = [(270, 820, 120, EDO[0], 'short', ('hair', 'umber', 'sepia')), (810, 840, 112, EDO[1], 'bun', ('hair', 'umber', 'sepia')),
           (540, 1000, 82, ('sand', 'ochre', 'tan', 'sienna'), 'bob', ('hair', 'umber', 'sepia'))]
    for (x, y, R, c, hs, hr) in fam:
        A = [[(x - R * 0.7, y + R * 1.45), (x - R * 0.8, y + R * 2.3), (x - R * 0.18, y + R * 2.45)],
             [(x + R * 0.7, y + R * 1.45), (x + R * 0.8, y + R * 2.3), (x + R * 0.18, y + R * 2.45)]]
        w = person(S, x, y, R, coat=c, hair_style=hs, plan=True, arms=A)
        erase(S, w['mask'])
        person(S, x, y, R, coat=c, hair_style=hs, hair=hr, eyes_closed=True, arms=A, hands=False)
        gassho(S, x, y + R * 2.3, R / 140)
    lamp = p.poly(curve([(470, 1430), (510, 1400), (570, 1400), (610, 1430), (570, 1460), (500, 1460)], 30), smooth=True)
    erase(S, lamp); p.form(lamp, ('ochre', 'sienna', 'terracotta', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    p.glow(545, 1350, 300, strength=1.3, density=1.2)
    p.lift(p.blob(548, 1370, 16, 38, 0.1), 'lemon', 1.0, tooth=0); p.lift(p.ellipse(548, 1385, 7, 16), 'white', 1.0, tooth=0)
    S.save('hidden_prayer')


def shepherd():
    """1匹の羊を、探しに行く: a shepherd in simple old clothes carrying a lost lamb on his shoulders down a rocky path, sunset"""
    S = Shot(2706); p = S.p
    x, y, R = 540, 760, 120
    ARMS = [[(x - R * 1.05, y + R * 1.7), (x - R * 1.45, y + R * 1.5), (x - R * 1.35, y + R * 1.25)],
            [(x + R * 1.05, y + R * 1.7), (x + R * 1.45, y + R * 1.5), (x + R * 1.35, y + R * 1.25)]]
    w = person(S, x, y, R, coat=('cream', 'sand', 'tan', 'sienna'), hair_style='short', plan=True, arms=ARMS)
    lamb = np.clip(p.blob(x, y + R * 0.95, R * 1.85, R * 0.62, 0.12)
                   + sum(p.ellipse(x + dx * R, y + R * (0.95 + dy), R * 0.32, R * 0.3) for dx, dy in
                         ((-1.6, -0.25), (-1.0, -0.5), (1.0, -0.5), (1.6, -0.25), (-1.3, 0.4), (-0.5, 0.55), (0.5, 0.55), (1.3, 0.4))), 0, 1)
    fg = np.clip(w['mask'] + lamb, 0, 1)
    dusk_sky(S, 1150)
    p.glow(860, 700, 420, strength=1.3, density=1.1)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [960, 880, 920, 860, 900, 940, 900], RIDGES[0], mist=0.5)
    ground(S, 1150, cols=('sand', 'ochre', 'olive', 'tan'), flowers=0)
    for (sx, sy, rx, ry) in ((130, 1500, 140, 80), (950, 1420, 120, 70), (220, 1250, 90, 50), (880, 1700, 160, 90)):
        p.stone(sx, sy, rx, ry, avoid=fg, seed=S.sd())
    path = p.poly([(480, 1150), (600, 1150), (840, 1920), (240, 1920)]) * (1 - fg)
    p.form(path, ('sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.2, seed=S.sd())
    p.lift(blur(fg, 30) * (1 - fg), 'butter', 0.4)
    erase(S, w['mask'])
    person(S, x, y, R, coat=('cream', 'sand', 'tan', 'sienna'), hair_style='short', hair=('hair', 'umber', 'sepia'), arms=ARMS, hands=False,
           smile=True, eyes_closed=True)
    erase(S, lamb * (1 - w['head']))
    lb = lamb * (1 - w['head'])
    for lx in (-1.5, -1.1, 1.1, 1.5):                 # little legs hanging down
        lg = p.tube([(x + lx * R, y + R * 1.3), (x + lx * R + 4, y + R * 1.85)], R * 0.12, R * 0.1)
        erase(S, lg); p.form(lg, ('cream', 'stone', 'warmgrey'), 90, LIGHT, density=1.5, seed=S.sd())
        p.form(p.ellipse(x + lx * R + 4, y + R * 1.88, R * 0.1, R * 0.07), ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    erase(S, lb)
    p.form(lb, ('white', 'cream', 'ivory', 'stone'), p.radial(x, y + R * 0.95, 90), LIGHT, length=(6, 14), density=1.8, seed=S.sd())
    rr = np.random.default_rng(11)
    for _ in range(70):                                # woolly curls
        cx_, cy_ = x + rr.uniform(-1.8, 1.8) * R, y + R * (0.95 + rr.uniform(-0.55, 0.55))
        if lb[int(cy_), int(cx_)] < 0.5: continue
        p.line(curve([(cx_ - 8, cy_), (cx_, cy_ - 8), (cx_ + 8, cy_)], 8), 'warmgrey', 2.0, 0.6, alpha=0.5)
    p.edge(lb, 'warmgrey', density=0.8, alpha=0.7)
    hx0, hy0 = x + R * 2.05, y + R * 0.75
    ears = np.clip(p.ellipse(hx0 - R * 0.3, hy0 - R * 0.28, R * 0.18, R * 0.08, rot=-30) + p.ellipse(hx0 + R * 0.3, hy0 - R * 0.28, R * 0.18, R * 0.08, rot=30), 0, 1)
    lh = p.ellipse(hx0, hy0, R * 0.36, R * 0.42)
    erase(S, np.clip(lh + ears, 0, 1)); p.form(ears, ('stone', 'warmgrey', 'pink'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(lh, ('cream', 'ivory', 'stone'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(lh, 'warmgrey', density=0.8, alpha=0.7)
    p.form(p.ellipse(hx0, hy0 - R * 0.3, R * 0.3, R * 0.16), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.8, seed=S.sd())
    for ex in (-0.13, 0.13): p.lift(p.ellipse(hx0 + ex * R, hy0 - R * 0.02, 5, 6), 'sepia', 1.0, tooth=0)
    p.form(p.ellipse(hx0, hy0 + R * 0.22, R * 0.09, R * 0.06), ('pink', 'rose', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    for (hx, hy) in ((x - R * 1.35, y + R * 1.25), (x + R * 1.35, y + R * 1.25)):
        p.form(p.ellipse(hx, hy, R * 0.22, R * 0.2), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('shepherd')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
