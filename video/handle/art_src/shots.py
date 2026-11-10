"""「私の人生、ほんとうに私のもの?」 paintings -- who holds the wheel of my life. python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *

_k = importlib.util.spec_from_file_location('k_shots', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'kamisama', 'art_src', 'shots.py'))
k = importlib.util.module_from_spec(_k); sys.path.insert(0, os.path.dirname(_k.origin)); _k.loader.exec_module(k)
erase, figure, sky, ground, ridge, RIDGES, path_scene = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, k.path_scene
room = k.ari.room
SKIN4 = ('peach', 'skin', 'skin_shade', 'apricot')


def hand(S, x, y, s, ang, cols=SKIN4, spread=1.0, curl=0.0, paint=True):
    """an open hand: palm at (x, y), fingers pointing along `ang` degrees; returns its mask"""
    p = S.p
    a = np.deg2rad(ang); d = np.array([np.cos(a), np.sin(a)]); n = np.array([-d[1], d[0]])
    palm = p.ellipse(x, y, 62 * s, 54 * s, rot=ang)
    m = palm.copy()
    for j, (off, ln) in enumerate(((-30, 0.85), (-10, 1.0), (10, 0.98), (30, 0.82))):
        b = np.array([x, y]) + d * 40 * s + n * off * s * spread
        tip = b + d * 78 * s * ln + n * off * s * 0.35 * spread - n * curl * 30 * s
        mid = (b + tip) / 2 - n * curl * 14 * s
        m = np.maximum(m, p.tube([tuple(b), tuple(mid), tuple(tip)], 13.5 * s, 11.5 * s))
    tb = np.array([x, y]) + n * 46 * s - d * 6 * s
    tt = tb + n * 40 * s + d * 46 * s
    m = np.maximum(m, p.tube([tuple(tb), tuple((tb + tt) / 2 + n * 4 * s), tuple(tt)], 15 * s, 12 * s))
    if paint:
        erase(S, m)
        p.form(m, cols, p.contour(m, 6, 90), LIGHT, length=(8, 18), density=1.6, warm='butter', seed=S.sd())
        p.edge(m, 'sienna', width=(1.4, 2.0), density=0.9, alpha=0.85)
    return m


def heart_mask(p, cx, cy, r):
    return np.clip(p.ellipse(cx - r * 0.5, cy - r * 0.2, r * 0.56, r * 0.56) + p.ellipse(cx + r * 0.5, cy - r * 0.2, r * 0.56, r * 0.56) +
                   p.poly([(cx - r * 1.02, cy - r * 0.05), (cx + r * 1.02, cy - r * 0.05), (cx, cy + r * 1.05)], smooth=True), 0, 1)


def car(S, cx, cy, w, body=('apricot', 'coral', 'terracotta', 'brick'), hood_up=False):
    """a small round storybook car seen from the side, wheels on the line y = cy"""
    p = S.p
    h = w * 0.42
    bm = p.poly(curve([(cx - w * 0.5, cy - h * 0.12), (cx - w * 0.48, cy - h * 0.5), (cx - w * 0.28, cy - h * 0.55), (cx - w * 0.18, cy - h),
                       (cx + w * 0.18, cy - h), (cx + w * 0.3, cy - h * 0.55), (cx + w * 0.48, cy - h * 0.5), (cx + w * 0.5, cy - h * 0.12)], 60), smooth=True)
    bm = bm * (p.YY < cy - h * 0.05)
    erase(S, bm)
    p.form(bm, body, p.contour(bm, 10, 0), LIGHT, length=(16, 36), density=1.5, warm='butter', seed=S.sd())
    for (x0, x1) in ((cx - w * 0.15, cx - w * 0.01), (cx + w * 0.02, cx + w * 0.16)):
        win = p.poly([(x0, cy - h * 0.58), (x0 + w * 0.02, cy - h * 0.92), (x1 - w * 0.02, cy - h * 0.92), (x1, cy - h * 0.58)])
        p.form(win, ('sky_pale', 'powder', 'cornflower', 'slate'), 0, LIGHT, density=1.4, seed=S.sd())
    p.edge(bm, 'sepia', width=(1.8, 2.6), density=1.0, alpha=0.85)
    for x in (cx - w * 0.3, cx + w * 0.3):
        wm = p.ellipse(x, cy - h * 0.06, h * 0.26, h * 0.26)
        erase(S, wm)
        p.form(wm, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
        p.form(p.ellipse(x, cy - h * 0.06, h * 0.11, h * 0.11), ('stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.5, seed=S.sd())
    p.lift(p.ellipse(cx + w * 0.47, cy - h * 0.35, w * 0.025, h * 0.07), 'lemon', 0.9, tooth=0)
    if hood_up:
        hd = p.poly([(cx + w * 0.28, cy - h * 0.55), (cx + w * 0.5, cy - h * 0.5), (cx + w * 0.56, cy - h * 1.05), (cx + w * 0.36, cy - h * 1.12)])
        erase(S, hd); p.form(hd, body, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(hd, 'sepia', density=1.0, alpha=0.85)
    return bm


# ============================================================ the shots
def mine():
    """私の人生は、私のもの: a young woman in the morning meadow, hand on her chest, sure of herself"""
    S = Shot(1001); p = S.p
    ARMS = [[(470, 1000), (430, 1110), (520, 1060)]]
    w = person(S, 540, 720, 160, coat=('peach', 'coral', 'terracotta', 'brick'), hair_style='long', plan=True, arms=ARMS)
    sky(S, 1250, (820, 420, 380))
    clouds(S, [(200, 420, 320, 70), (880, 300, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1150, 1080, 1120, 1060, 1100, 1130, 1080], RIDGES[0], mist=0.5)
    ground(S, 1240, flowers=120)
    erase(S, w['mask'])
    person(S, 540, 720, 160, coat=('peach', 'coral', 'terracotta', 'brick'), hair_style='long', arms=ARMS, smile=True, look=(0.1, 0.0))
    S.save('mine')


def birth():
    """生まれる日も、親も: a mother holding her newborn wrapped in a blanket, the father close beside"""
    S = Shot(1002); p = S.p
    room(S, np.zeros((H, W), np.float32), win_box=(90, 160, 400, 560), wall_to=1500)
    p.form(p.rect(0, 1500, 1080, 1920), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    f = person(S, 790, 600, 130, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='short', plan=True)
    m = person(S, 480, 640, 150, coat=('pink', 'rose', 'coral', 'brick'), hair_style='long', plan=True)
    erase(S, f['mask'])
    person(S, 790, 600, 130, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='short', smile=True, look=(-0.5, 0.4),
           hair=('hair', 'umber', 'sepia'))
    erase(S, m['mask'])
    person(S, 480, 640, 150, coat=('pink', 'rose', 'coral', 'brick'), hair_style='long', eyes_closed=True, smile=True)
    bundle = p.blob(520, 1060, 190, 105, 0.08, seed=4, rot=-12)
    erase(S, bundle)
    p.form(bundle, ('butter', 'cream', 'apricot', 'peach'), p.contour(bundle, 10, 60), LIGHT, length=(14, 30), density=1.5, seed=S.sd())
    p.edge(bundle, 'tan', density=0.9, alpha=0.8)
    face = p.ellipse(420, 1030, 60, 54)
    erase(S, face)
    p.form(face, SKIN, p.contour(face, 6), LIGHT, length=(6, 12), density=1.5, warm='peach', seed=S.sd())
    p.edge(face, 'skin_shade', density=0.8, alpha=0.8)
    for sgn in (-1, 1):
        ex = 420 + sgn * 20
        p.line(curve([(ex - 9, 1030), (ex, 1036), (ex + 9, 1030)], 8), 'umber', 2.2, 0.8, alpha=0.9)
        p.blush(420 + sgn * 34, 1048, 10, amount=0.7)
    for (x, y, rot) in ((360, 1110, -30), (650, 1080, 20)):            # mother's hands round the bundle
        hm = p.blob(x, y, 46, 34, 0.08, seed=S.sd(), rot=rot)
        erase(S, hm); p.form(hm, SKIN4, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(hm, 'skin_shade', density=0.8, alpha=0.8)
    p.glow(250, 360, 380, strength=0.8, density=0.8)
    S.save('birth')


def fog():
    """明日どうなるかも分からない: a road that runs on into thick morning mist; someone standing, looking ahead"""
    S = Shot(1003); p = S.p
    path_scene(S, 880)
    band = smoothstep(500, 860, p.YY) * smoothstep(1250, 900, p.YY)
    p.lift(blur(band, 20), 'cream', 0.85)
    p.lift(blur(smoothstep(1100, 300, p.YY), 30), 'cream', 0.35)
    figure(S, 540, 1150, 300, coat=('sage', 'lichen', 'moss', 'pine'), back=True)
    S.save('fog')


def heart():
    """好きになる気持ちも、落ちこむ心も: a young woman, hand on her heart; a pink heart one side, a little rain cloud the other"""
    S = Shot(1004); p = S.p
    ARMS = [[(470, 1000), (430, 1110), (520, 1060)]]
    w = person(S, 540, 740, 160, coat=('lavender', 'periwinkle', 'violet', 'indigo'), hair_style='bob', plan=True, arms=ARMS)
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'ivory', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.6, seed=S.sd())
    p.hatch(wall * smoothstep(540, 1080, p.XX), p.flow(2, 4, 500), ['powder', 'sky_pale'], (60, 140), (1.8, 2.4), 1.0, 0.6, alpha=0.45, seed=S.sd())
    p.hatch(wall * smoothstep(540, 0, p.XX), p.flow(2, 4, 500), ['peach', 'pink'], (60, 140), (1.8, 2.4), 1.0, 0.6, alpha=0.45, seed=S.sd())
    hm = heart_mask(p, 210, 560, 110)
    p.form(hm, ('pink', 'rose', 'coral', 'brick'), p.contour(hm, 8, 30), LIGHT, length=(10, 22), density=1.6, warm='butter', seed=S.sd())
    p.edge(hm, 'brick', density=0.9, alpha=0.8)
    p.lift(p.ellipse(170, 520, 22, 14, rot=-30), 'white', 0.7)
    cm = k.cloud_mask(p, 870, 560, 260, 130, np.random.default_rng(3))
    p.form(cm, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, length=(14, 30), density=1.5, seed=S.sd())
    p.edge(cm, 'slate', density=0.8, alpha=0.7)
    for j in range(7):
        x = 780 + j * 30
        p.line([(x, 640), (x - 10, 700 + (j % 2) * 30)], 'cornflower', 3, 0.8, alpha=0.85)
    erase(S, w['mask'])
    person(S, 540, 740, 160, coat=('lavender', 'periwinkle', 'violet', 'indigo'), hair_style='bob', arms=ARMS, smile=False, look=(0.0, -0.4))
    for sgn in (-1, 1):                              # brows a little worried
        ex = 540 + sgn * 54
        p.line([(ex - 20, 700 - sgn * 0), (ex + 20, 700 - sgn * 6)], 'umber', 2.4, 0.8, alpha=0.8)
    p.line(curve([(525, 832), (540, 828), (555, 832)], 8), 'brick', 2.4, 0.8, alpha=0.9)
    S.save('heart')


def crossroads():
    """どうして思い通りにできない: a figure from behind at a fork of three roads, a signpost with blank arrows"""
    S = Shot(1005); p = S.p
    sky(S, 900, (540, 760, 300))
    clouds(S, [(220, 340, 320, 70), (840, 260, 280, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [860, 790, 830, 870, 800, 760, 830], RIDGES[0], mist=0.5)
    ground(S, 880, flowers=100)
    for pts in ([(500, 900), (540, 900), (600, 1200), (480, 1200)], [(470, 920), (500, 920), (420, 1200), (300, 1200)],
                [(560, 920), (600, 930), (830, 1200), (680, 1200)], [(480, 1200), (600, 1200), (820, 1920), (260, 1920)]):
        m = p.poly(pts)
        p.form(m, ('sand', 'butter', 'tan', 'ochre'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.3, seed=S.sd())
    for x, y, h in ((140, 1100, 300), (950, 1060, 340)):
        p.tree(x, y, h, 100, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    post = p.rect(760, 700, 784, 1180)
    p.form(post, ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.5, seed=S.sd())
    for (y, sgn, ln) in ((730, -1, 200), (810, 1, 190), (890, -1, 170)):
        x0 = 772; x1 = x0 + sgn * ln
        ar = p.poly([(x0, y - 26), (x1 - sgn * 30, y - 26), (x1, y), (x1 - sgn * 30, y + 26), (x0, y + 26)])
        erase(S, ar); p.form(ar, ('cream', 'sand', 'tan', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(ar, 'brown', density=0.9, alpha=0.85)
    figure(S, 540, 1250, 330, coat=('peach', 'coral', 'terracotta', 'brick'), hair=('hair', 'umber', 'sepia'), back=True, up=0.3)
    S.save('crossroads')


def car_broken():
    """車がこわれたら: a little car stopped at the roadside, bonnet up, a puff of smoke"""
    S = Shot(1006); p = S.p
    sky(S, 1000, (300, 300, 300))
    clouds(S, [(220, 340, 320, 70), (840, 460, 280, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [960, 900, 940, 880, 920, 950, 900], RIDGES[0], mist=0.5)
    ground(S, 1000, flowers=60)
    road = p.rect(0, 1080, 1080, 1260)
    p.form(road, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, length=(60, 120), density=1.4, seed=S.sd())
    for x in range(40, 1080, 180): p.line([(x, 1170), (x + 90, 1170)], 'cream', 6, 0.8, alpha=0.85)
    car(S, 500, 1120, 560, hood_up=True)
    for (x, y, r) in ((800, 820, 50), (850, 740, 64), (820, 650, 46)):
        sm = p.blob(x, y, r, r * 0.8, 0.2, seed=S.sd())
        p.form(sm, ('stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.2, seed=S.sd())
    tri = p.poly([(980, 1060), (1040, 1160), (920, 1160)])
    p.form(tri, ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    p.lift(p.poly([(980, 1090), (1012, 1145), (948, 1145)]), 'white', 0.8)
    S.save('car_broken')


def garage():
    """つくったメーカーに: the car in the maker's warm workshop, the mechanic with a spanner, smiling, a hand on the car"""
    S = Shot(1007); p = S.p
    wall = (p.YY < 1250).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'sand', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.7, seed=S.sd())
    board = p.rect(120, 300, 960, 620)
    p.form(board, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, length=(40, 90), density=1.3, seed=S.sd())
    for j, x in enumerate(range(180, 940, 110)):              # tools on the pegboard
        if j % 2: p.line([(x, 360), (x, 560)], 'slate', 12, 0.85, alpha=0.95); p.form(p.ellipse(x, 360, 22, 22), ('stone', 'slate', 'indigo'), 0, LIGHT, density=1.4, seed=S.sd())
        else: p.line([(x, 380), (x, 560)], 'red', 14, 0.85, alpha=0.95); p.form(p.rect(x - 26, 350, x + 26, 390), ('stone', 'slate', 'indigo'), 0, LIGHT, density=1.4, seed=S.sd())
    for x in (150, 540, 930):
        p.lift(p.ellipse(x, 120, 120, 30), 'butter', 0.5)
        p.glow(x, 140, 160, strength=0.5, density=0.5)
    floor = (p.YY >= 1250).astype(np.float32)
    p.form(floor, ('stone', 'warmgrey', 'pebble', 'slate'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    ARM = [[(770, 960), (700, 1000), (650, 990)], [(930, 960), (990, 1020), (1000, 940)]]
    w = person(S, 850, 800, 100, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='short', plan=True, arms=ARM)
    erase(S, w['mask'])
    person(S, 850, 800, 100, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='short', smile=True, look=(-0.5, 0.2),
           arms=ARM, hair=('hair', 'umber', 'sepia'))
    p.line([(1000, 940), (1030, 850)], 'slate', 12, 0.85, alpha=0.95)
    p.form(p.ellipse(1033, 840, 20, 20), ('stone', 'slate', 'indigo'), 0, LIGHT, density=1.4, seed=S.sd())
    car(S, 380, 1330, 700, hood_up=True)
    S.save('garage')


def bench():
    """その方はあなたが座るのも立つのも: a woman sitting on a park bench, eyes closed, warm light falling on her"""
    S = Shot(1008); p = S.p
    w = person(S, 540, 820, 140, coat=('butter', 'ochre', 'amber', 'sienna'), hair_style='long', plan=True)
    sky(S, 1150, (300, 260, 360))
    p.tree(900, 1200, 700, 220, colours=('meadow', 'moss', 'pine', 'forest'), clumps=8, seed=S.sd())
    ground(S, 1150, flowers=90)
    beam = p.poly([(160, 0), (420, 0), (760, 1300), (340, 1300)])
    p.hatch(beam, 70, ['butter', 'cream'], (60, 140), (1.8, 2.4), 0.8, 0.6, opacity=0.6, alpha=0.32, seed=S.sd())
    for y in (1000, 1070):
        sl = p.rect(220, y, 860, y + 44) * (1 - w['mask'])
        erase(S, sl); p.form(sl, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, length=(40, 90), density=1.5, seed=S.sd()); p.edge(sl, 'sepia', density=0.8, alpha=0.8)
    erase(S, w['mask'])
    person(S, 540, 820, 140, coat=('butter', 'ochre', 'amber', 'sienna'), hair_style='long', eyes_closed=True, smile=True)
    seat = p.rect(200, 1200, 880, 1250)
    erase(S, seat); p.form(seat, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(seat, 'sepia', density=0.8, alpha=0.8)
    for x in (250, 830):
        lg = p.rect(x - 14, 1250, x + 14, 1420); erase(S, lg); p.form(lg, ('slate', 'indigo', 'umber'), 90, LIGHT, density=1.5, seed=S.sd())
    p.glow(520, 760, 300, strength=0.6, density=0.6)
    S.save('bench')


def letgo():
    """その方の手をはなして: a great warm hand reaching down, a small hand pulling away -- the gap between them"""
    S = Shot(1009); p = S.p
    bg = np.ones((H, W), np.float32)
    v = p.value(0.0, 1.0, 0, 1920)
    p.hatch(bg, p.flow(-30, 6), ['cream', 'butter', 'apricot'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.hatch(bg * v, p.flow(-30, 6), ['powder', 'lavender', 'stone'], (60, 150), (1.8, 2.5), 1.2, 0.64, alpha=0.6, seed=S.sd())
    p.glow(820, 420, 520, strength=1.0, density=1.0)
    sl1 = p.tube([(1250, 120), (1000, 330), (860, 450)], 190, 150)
    erase(S, sl1); p.form(sl1, ('white', 'cream', 'ivory', 'sand'), p.contour(sl1, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
    p.edge(sl1, 'tan', density=0.8, alpha=0.7)
    hand(S, 730, 590, 2.6, 135, cols=('butter', 'peach', 'skin', 'skin_shade'))
    sl2 = p.tube([(-160, 1640), (120, 1360), (260, 1240)], 150, 120)
    erase(S, sl2); p.form(sl2, ('slate', 'indigo', 'umber', 'sepia'), p.contour(sl2, 10, 90), LIGHT, density=1.4, seed=S.sd())
    hand(S, 330, 1130, 1.9, -50, curl=0.6)
    for j in range(5):
        r = 40 + j * 26
        t = np.linspace(-0.6, 0.6, 12) + 0.8
        pass
    S.save('letgo')


def way():
    """わたしが道であり、いのち: a long road through the meadow toward the rising sun"""
    S = Shot(1010); p = S.p
    sky(S, 960, None)
    p.glow(540, 930, 520, strength=1.5, density=1.3)
    p.lift(p.ellipse(540, 940, 90, 90) * (p.YY < 950), 'white', 0.95, tooth=0)
    clouds(S, [(200, 380, 320, 70), (880, 300, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [930, 880, 920, 960, 910, 870, 920], RIDGES[0], mist=0.6)
    ground(S, 960, flowers=180)
    road = p.poly([(525, 960), (555, 960), (840, 1920), (240, 1920)])
    p.form(road, ('butter', 'sand', 'tan', 'ochre'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.3, seed=S.sd())
    p.lift(blur(road * smoothstep(1500, 960, p.YY), 10), 'glow' if False else 'butter', 0.4)
    for x, y, h in ((150, 1160, 360), (960, 1120, 320)):
        p.tree(x, y, h, 100, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    S.save('way')


def wheel():
    """人生のハンドル: through the windscreen, a sunlit road; two hands resting lightly on the steering wheel"""
    S = Shot(1011); p = S.p
    ws = p.poly([(40, 300), (1040, 300), (1080, 1000), (0, 1000)])
    sky(S, 760, (540, 700, 340))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [740, 700, 720, 690, 710, 730, 700], RIDGES[0], mist=0.5)
    g = (p.YY > 760).astype(np.float32)
    p.form(g, ('meadow', 'yellowgreen', 'grass', 'moss'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    road = p.poly([(530, 760), (550, 760), (900, 1000), (180, 1000)])
    p.form(road, ('butter', 'sand', 'tan', 'ochre'), p.flow(90, 8), LIGHT, density=1.3, seed=S.sd())
    frame = 1 - ws
    erase(S, frame)
    p.form(frame * (p.YY < 1000), ('slate', 'umber', 'sepia', 'indigo'), 0, LIGHT, length=(40, 90), density=1.5, seed=S.sd())
    dash = (p.YY >= 1000).astype(np.float32)
    erase(S, dash)
    p.form(dash, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, length=(60, 120), density=1.5, seed=S.sd())
    p.lift(blur(p.rect(0, 1000, 1080, 1030), 4), 'butter', 0.3)
    cx, cy, r = 540, 1300, 330
    ring = p.ellipse(cx, cy, r, r) * (1 - p.ellipse(cx, cy, r - 46, r - 46))
    hub = p.ellipse(cx, cy, 90, 90)
    sp = np.clip(p.tube([(cx - r + 20, cy + 20), (cx, cy)], 26, 26) + p.tube([(cx + r - 20, cy + 20), (cx, cy)], 26, 26) +
                 p.tube([(cx, cy), (cx, cy + r - 20)], 26, 26), 0, 1)
    wm = np.clip(ring + hub + sp, 0, 1)
    erase(S, wm)
    p.form(wm, ('slate', 'indigo', 'umber', 'sepia'), p.contour(wm, 8, 0), LIGHT, length=(14, 30), density=1.6, seed=S.sd())
    p.lift(blur(ring * smoothstep(cy, cy - r, p.YY) * smoothstep(cx + 100, cx - r, p.XX), 6), 'stone', 0.35)
    p.edge(wm, 'sepia', density=0.8, alpha=0.8)
    for sgn in (-1, 1):
        hx, hy = cx + sgn * 250, cy - 210
        sl = p.tube([(cx + sgn * 520, 1980), (cx + sgn * 380, 1500), (hx + sgn * 40, hy + 80)], 90, 70)
        erase(S, sl); p.form(sl, ('peach', 'coral', 'terracotta', 'brick'), p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
        p.edge(sl, 'sepia', density=0.8, alpha=0.75)
        hm = p.blob(hx, hy, 66, 52, 0.06, seed=S.sd(), rot=sgn * 40)
        erase(S, hm); p.form(hm, SKIN4, p.contour(hm, 6), LIGHT, density=1.6, warm='butter', seed=S.sd()); p.edge(hm, 'sienna', density=0.9, alpha=0.85)
        for j in range(3):
            p.line([(hx - sgn * 30 + sgn * j * 18, hy - 30), (hx - sgn * 30 + sgn * j * 18 + sgn * 10, hy + 20)], 'skin_shade', 2.0, 0.6, alpha=0.6)
    p.glow(540, 700, 380, strength=0.6, density=0.6)
    S.save('wheel')


def free():
    """ほんとうの自分に出会う: the woman in the sunrise meadow, arms open wide, smiling"""
    S = Shot(1012); p = S.p
    ARMS = [[(430, 1000), (290, 900), (190, 760)], [(650, 1000), (790, 900), (890, 760)]]
    w = person(S, 540, 700, 150, coat=('butter', 'sun', 'apricot', 'amber'), hair_style='long', plan=True, arms=ARMS)
    sky(S, 1250, (540, 1000, 500))
    p.lift(p.ellipse(540, 1050, 90, 90) * (p.YY < 1100), 'white', 0.8, tooth=0)
    clouds(S, [(200, 380, 320, 70), (880, 300, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1150, 1090, 1120, 1070, 1110, 1140, 1090], RIDGES[0], mist=0.6)
    ground(S, 1230, flowers=180)
    erase(S, w['mask'])
    person(S, 540, 700, 150, coat=('butter', 'sun', 'apricot', 'amber'), hair_style='long', arms=ARMS, eyes_closed=True, smile=True)
    p.glow(540, 760, 380, strength=0.5, density=0.5)
    S.save('free')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
