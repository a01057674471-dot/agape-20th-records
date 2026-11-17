"""「めぐみ」 paintings -- grace, the gift given 価なしに. python3 shots.py NAME"""
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
COAT, HAIR = hj.SANGHEE, hj.HAIR


def rain(S, region, n=260, seed=1, col='cornflower', glow=False):
    p = S.p; rr = np.random.default_rng(seed)
    for _ in range(n):
        x, y = rr.uniform(0, W), rr.uniform(0, H)
        if region[int(y), int(x)] < 0.5: continue
        L_ = rr.uniform(24, 46)
        p.line([(x, y), (x - 6, y + L_)], col, 3.0, 0.8, alpha=0.85)
        if glow and rr.random() < 0.3: p.lift(p.ellipse(x - 6, y + L_, 4, 4), 'white', 0.9, tooth=0)


def sea_bounty():
    """海のめぐみ: a little fishing harbour in the morning, boats coming in with baskets of silver fish"""
    S = Shot(2401); p = S.p
    sky(S, 860, (800, 600, 360))
    clouds(S, [(220, 340, 320, 70), (860, 260, 260, 60)])
    sea = (p.YY >= 860).astype(np.float32)
    p.hatch(sea, p.flow(0, 3), ('water', p.value(0.4, 0.1, 860, 1920)), (60, 150), (1.8, 2.6), 1.8, 0.74, seed=S.sd())
    p.line([(0, 862), (1080, 862)], 'cornflower', 3, 0.7, alpha=0.6)
    for (x, y, s) in ((300, 1150, 1.0), (760, 1050, 0.75)):
        hull = p.poly([(x - 220 * s, y), (x + 220 * s, y), (x + 170 * s, y + 90 * s), (x - 170 * s, y + 90 * s)])
        erase(S, hull); p.form(hull, ('white', 'cream', 'sky_pale', 'cornflower'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(hull, 'slate', density=0.9, alpha=0.85)
        p.form(p.rect(x - 220 * s, y + 20 * s, x + 220 * s, y + 34 * s) * hull, ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
        cab = p.rect(x + 40 * s, y - 120 * s, x + 150 * s, y); erase(S, cab); p.form(cab, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd())
        p.line([(x - 60 * s, y), (x - 60 * s, y - 260 * s)], 'sepia', 5 * s, 0.85, alpha=0.9)
        bk = p.rect(x - 160 * s, y - 60 * s, x - 20 * s, y); erase(S, bk); p.form(bk, ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
        for j in range(5): p.form(p.ellipse(x - 140 * s + j * 28 * s, y - 64 * s, 18 * s, 8 * s, rot=20), ('stone', 'sky_pale', 'white'), 0, LIGHT, density=1.4, seed=S.sd())
        p.ripples(x, y + 90 * s, 240 * s, 20 * s, 3, 'white')
    for (x, y) in ((560, 520), (600, 545), (640, 515)):
        p.line(curve([(x - 18, y), (x - 7, y - 9), (x, y - 2), (x + 7, y - 9), (x + 18, y)], 12), 'sepia', 2.4, 0.8, alpha=0.8)
    S.save('sea_bounty')


def mountain_bounty():
    """山のめぐみ: an autumn mountain slope, a persimmon tree heavy with fruit, a basket of chestnuts and mushrooms"""
    S = Shot(2402); p = S.p
    sky(S, 800, (300, 300, 300))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [760, 640, 560, 600, 680, 620, 700], ('butter', 'ochre', 'tangerine', 'sienna'), mist=0.4)
    ridge(S, xs, [960, 900, 940, 880, 920, 950, 900], ('apricot', 'terracotta', 'ochre', 'olive'), mist=0.3)
    ground(S, 1000, cols=('butter', 'ochre', 'sand', 'olive'), flowers=0)
    p.tree(700, 1500, 650, 240, colours=('butter', 'ochre', 'tangerine', 'olive'), clumps=8, seed=S.sd())
    rr = np.random.default_rng(3)
    for _ in range(20):
        x, y = 700 + rr.uniform(-230, 230), 900 + rr.uniform(-200, 160)
        p.form(p.ellipse(x, y, 18, 16), ('tangerine', 'orange', 'terracotta'), 0, LIGHT, density=1.6, seed=S.sd())
    bk = p.poly(curve([(140, 1480), (160, 1640), (300, 1680), (440, 1640), (460, 1480)], 30))
    erase(S, bk); p.form(bk, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(bk, 'sepia', density=0.9, alpha=0.85)
    for j in range(7):
        x = 190 + j * 40; p.form(p.ellipse(x, 1478 - (j % 2) * 16, 22, 18), ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    for (x, y) in ((380, 1450), (230, 1440)):
        p.form(p.ellipse(x, y, 34, 18) * (p.YY < y + 4), ('sand', 'tan', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
        p.form(p.rect(x - 7, y, x + 7, y + 34), ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd())
    S.save('mountain_bounty')


def rain_paddy():
    """めぐみの雨: soft rain falling on green rice paddies, a farmhouse, someone under an umbrella looking up glad"""
    S = Shot(2403); p = S.p
    m = (p.YY < 800).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['stone', 'powder', 'lavender'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.lift(blur(p.rect(0, 500, 1080, 800), 30), 'cream', 0.3)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [780, 740, 760, 720, 750, 770, 740], RIDGES[2], mist=0.6)
    fields = (p.YY >= 800).astype(np.float32)
    for kk in range(7):
        band = fields * (p.YY > 800 + kk * 160) * (p.YY < 950 + kk * 160)
        p.form(band, [('yellowgreen', 'meadow', 'grass', 'leaf'), ('meadow', 'sage', 'grass', 'moss')][kk % 2], 0, LIGHT, length=(40, 100), density=1.3, seed=S.sd())
        p.line([(0, 800 + kk * 160), (1080, 800 + kk * 160)], 'olive', 3, 0.6, alpha=0.6)
    p.cottage(820, 880, 180, 120, ('cream', 'ivory', 'sand', 'tan'), ('slate', 'indigo', 'umber', 'sepia'), light=LIGHT, glow=0.5, seed=S.sd())
    um = p.poly(curve([(220, 1260), (360, 1150), (500, 1260)], 30).tolist() + [(220, 1260)])
    figure(S, 360, 1560, 300, coat=('sage', 'lichen', 'moss', 'pine'), hair=('hair', 'umber', 'sepia'), back=False, up=0.5)
    erase(S, um); p.form(um, ('rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(um, 'brick', density=0.9, alpha=0.8)
    p.line([(360, 1150), (360, 1340)], 'sepia', 4, 0.8, alpha=0.9)
    rain(S, np.ones((H, W), np.float32), 300, 2)
    S.save('rain_paddy')


def gift_rain():
    """ただ、与えられたもの: two cupped hands catching drops of light falling from above"""
    S = Shot(2404); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-10, 6), ['apricot', 'butter', 'peach'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.glow(540, 300, 500, strength=1.0, density=1.0)
    for (x, ang, curl, sx) in ((450, -112, -0.5, 180), (630, -68, 0.5, 900)):
        sl = p.tube([(sx, 1980), ((sx + x) / 2, 1620), (x, 1330)], 140, 115)
        erase(S, sl); p.form(sl, COAT, p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd()); p.edge(sl, 'brick', density=0.8, alpha=0.7)
    for (x, ang, curl) in ((450, -112, -0.5), (630, -68, 0.5)):
        hand(S, x, 1240, 1.9, ang, curl=curl)
    rr = np.random.default_rng(5)
    for _ in range(26):
        x, y = rr.uniform(300, 780), rr.uniform(200, 1050)
        d = p.blob(x, y, 9, 15, 0.05); p.lift(d, 'white', 0.9, tooth=0); p.glow(x, y, 26, strength=0.6, density=0.6)
    p.lift(blur(p.ellipse(540, 1110, 150, 50), 10), 'butter', 0.5)
    S.save('gift_rain')


def rain_both():
    """良い人の上にも、悪い人の上にも: one rain over two neighbouring gardens -- a smiling woman watering flowers and a grumpy man
    with his arms folded; the same soft rain falls on both"""
    S = Shot(2405); p = S.p
    m = (p.YY < 900).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['powder', 'stone', 'butter'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.glow(540, 300, 400, strength=0.7, density=0.7)
    for x0, c in ((60, ('cream', 'sand', 'tan', 'sienna')), (600, ('powder', 'sky_pale', 'cornflower', 'slate'))):
        b = p.rect(x0, 560, x0 + 420, 900); erase(S, b); p.form(b, c, 90, LIGHT, density=1.4, seed=S.sd()); p.edge(b, 'sepia', density=0.8, alpha=0.8)
        rf = p.poly([(x0 - 20, 570), (x0 + 210, 420), (x0 + 440, 570)]); erase(S, rf); p.form(rf, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
        p.window(x0 + 60, 640, x0 + 160, 760, panes=(2, 2), glow=0.6, seed=S.sd())
    ground(S, 900, flowers=0)
    p.line([(540, 900), (540, 1500)], 'tan', 8, 0.8, alpha=0.9)
    p.flowers(p.rect(80, 1350, 500, 1480), kinds=('daisy', 'poppy', 'buttercup'), n=40, size=(8, 12))
    p.flowers(p.rect(600, 1350, 1020, 1480), kinds=('daisy', 'poppy', 'buttercup'), n=40, size=(8, 12))
    ARMS = [[(330, 1180), (420, 1180), (470, 1140)]]
    bm = person(S, 260, 1000, 100, coat=('pink', 'rose', 'coral', 'brick'), hair_style='bun', plan=True, arms=ARMS)
    erase(S, bm['mask']); person(S, 260, 1000, 100, coat=('pink', 'rose', 'coral', 'brick'), hair_style='bun', hair=('hair', 'umber', 'sepia'), arms=ARMS, smile=True, eyes_closed=True)
    cn = p.poly([(470, 1120), (540, 1110), (530, 1170), (480, 1175)]); p.form(cn, ('sage', 'moss', 'pine'), 0, LIGHT, density=1.5, seed=S.sd())
    gm = person(S, 820, 1000, 100, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='short', plan=True, arms=[[(740, 1180), (820, 1200), (900, 1180)]])
    erase(S, gm['mask']); person(S, 820, 1000, 100, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='short', hair=('hair', 'umber', 'sepia'),
                                 arms=[[(740, 1180), (820, 1200), (900, 1180)]], hands=False, smile=False)
    for sgn in (-1, 1): p.line([(820 + sgn * 34 - 14, 1036 - 4 * sgn), (820 + sgn * 34 + 14, 1036 + 4 * sgn)], 'umber', 2.4, 0.8, alpha=0.85)
    p.line(curve([(805, 1062), (820, 1056), (835, 1062)], 8), 'brick', 2.4, 0.8, alpha=0.9)
    rain(S, (p.YY < 1700).astype(np.float32), 340, 3, glow=True)
    S.save('rain_both')


def blessing_rain():
    """降りそそいでいます: the young woman in a meadow, face lifted, smiling, a gentle rain of light falling on her"""
    S = Shot(2406); p = S.p
    ARMS = [[(430, 1000), (330, 900), (280, 800)], [(650, 1000), (750, 900), (800, 800)]]
    w = person(S, 540, 760, 150, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    sky(S, 1200, (540, 300, 520))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1150, 1090, 1120, 1070, 1110, 1140, 1090], RIDGES[0], mist=0.5)
    ground(S, 1200, flowers=160)
    erase(S, w['mask'])
    person(S, 540, 760, 150, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, eyes_closed=True, smile=True)
    rr = np.random.default_rng(8)
    for _ in range(70):
        x, y = rr.uniform(60, 1020), rr.uniform(80, 1400)
        if w['mask'][int(y), int(x)] > 0.3: continue
        d = p.blob(x, y, 7, 13, 0.05); p.lift(d, 'white', 0.85, tooth=0); p.glow(x, y, 22, strength=0.5, density=0.5)
    p.glow(540, 300, 360, strength=0.8, density=0.8)
    S.save('blessing_rain')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
