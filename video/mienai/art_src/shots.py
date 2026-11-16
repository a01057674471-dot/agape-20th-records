"""「ほんとうに大切なものは、目に見えない」 paintings. python3 shots.py NAME"""
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
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4, heart_mask = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4, h.heart_mask
COAT, HAIR = hj.SANGHEE, hj.HAIR


def her(S, x, y, R, plan=False, **kw):
    m = person(S, x, y, R, coat=COAT, hair_style='long', plan=True, arms=kw.get('arms'))
    if plan: return m['mask']
    erase(S, m['mask'])
    person(S, x, y, R, coat=COAT, hair_style='long', hair=HAIR, **kw)
    return m['mask']


def breeze(S, region_y=(300, 1300), n=9, seed=1, col='cream'):
    p = S.p; rr = np.random.default_rng(seed)
    for _ in range(n):
        y = rr.uniform(*region_y); x0 = rr.uniform(-100, 300)
        t = np.linspace(0, 1, 60)
        xs = x0 + t * rr.uniform(500, 900); ys = y + 40 * np.sin(t * 6 + rr.uniform(0, 6)) * t
        p.line(np.stack([xs, ys], 1), col, rr.uniform(3, 5), 0.6, alpha=0.75)
        tx, ty = xs[-1], ys[-1]
        p.line(np.stack([tx + 30 * np.cos(np.linspace(0, 4.5, 20)), ty - 30 + 30 * np.sin(np.linspace(0, 4.5, 20))], 1), col, 3, 0.6, alpha=0.7)


def field_wind():
    """the young woman standing in a field, eyes closed, the wind moving her hair and the grass -- the breeze drawn in soft lines"""
    S = Shot(2201); p = S.p
    m = her(S, 540, 780, 160, plan=True)
    sky(S, 1150, (820, 380, 360))
    clouds(S, [(220, 380, 320, 70), (880, 280, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1090, 1030, 1060, 1010, 1050, 1080, 1030], RIDGES[0], mist=0.5)
    ground(S, 1150, flowers=120)
    p.grass((p.YY > 1150).astype(np.float32) * (p.YY < 1350), lean=-60, sway=30)
    her(S, 540, 780, 160, eyes_closed=True, smile=True)
    for j in range(5):
        p.line(curve([(650, 700 + j * 30), (760, 690 + j * 40), (860, 720 + j * 45)], 20), 'hair', 4, 0.7, alpha=0.75)
    breeze(S, (350, 1250), 10, 2)
    S.save('field_wind')


def breath():
    """空気: on a hilltop in the morning, taking a deep breath; soft swirls of fresh air round her"""
    S = Shot(2202); p = S.p
    m = her(S, 540, 760, 150, plan=True, arms=[[(430, 1000), (300, 900), (220, 780)], [(650, 1000), (780, 900), (860, 780)]])
    sky(S, 1420, (540, 1150, 520))
    p.lift(p.ellipse(540, 1180, 80, 80) * (p.YY < 1250), 'white', 0.85, tooth=0)
    hill = p.below([0, 300, 540, 780, 1080], [1400, 1290, 1250, 1290, 1400])
    p.form(hill, ('meadow', 'yellowgreen', 'grass', 'moss'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    p.flowers(hill * (p.YY > 1450), n=80, size=(5, 9))
    her(S, 540, 760, 150, eyes_closed=True, smile=True, arms=[[(430, 1000), (300, 900), (220, 780)], [(650, 1000), (780, 900), (860, 780)]])
    for (cx, cy, r) in ((280, 520, 90), (800, 480, 110), (540, 380, 80), (200, 900, 70), (900, 880, 80)):
        t = np.linspace(0, 2 * np.pi * 1.5, 60)
        p.line(np.stack([cx + r * np.cos(t) * (1 - t / 14), cy + r * 0.6 * np.sin(t) * (1 - t / 14)], 1), 'sky_pale', 3.5, 0.6, alpha=0.8)
    S.save('breath')


def bench_hearts():
    """心: two people sitting side by side on a bench, a soft warm glow between their hearts"""
    S = Shot(2203); p = S.p
    sky(S, 1150, (300, 300, 340))
    p.tree(900, 1200, 700, 220, colours=('meadow', 'moss', 'pine', 'forest'), clumps=8, seed=S.sd())
    ground(S, 1150, flowers=80)
    for y in (1000, 1070):
        sl = p.rect(160, y, 920, y + 44); erase(S, sl); p.form(sl, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    her(S, 380, 780, 130, smile=True, look=(0.4, 0.1))
    m2 = person(S, 700, 770, 135, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='short', plan=True)
    erase(S, m2['mask']); person(S, 700, 770, 135, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='short', hair=('hair', 'umber', 'sepia'), smile=True, look=(-0.4, 0.1))
    seat = p.rect(140, 1220, 940, 1270); erase(S, seat); p.form(seat, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    for x in (200, 880):
        lg = p.rect(x - 14, 1270, x + 14, 1420); erase(S, lg); p.form(lg, ('slate', 'indigo', 'umber'), 90, LIGHT, density=1.5, seed=S.sd())
    p.glow(540, 1060, 220, strength=1.0, density=1.0)
    hm = heart_mask(p, 540, 1050, 40); p.form(hm, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.4, seed=S.sd())
    p.lift(blur(hm, 8) * 0.5, 'butter', 0.3)
    S.save('bench_hearts')


def tree_shade():
    """おかげさま: a small figure walking under the soft shade of a great tree, sheltered from the sun"""
    S = Shot(2204); p = S.p
    sky(S, 1250, (980, 160, 300))
    ground(S, 1250, cols=('yellowgreen', 'meadow', 'butter', 'grass'), flowers=60)
    tr = p.tube([(560, 1400), (540, 1000), (520, 700)], 80, 50)
    erase(S, tr); p.form(tr, ('tan', 'sienna', 'brown', 'umber'), 90, LIGHT, density=1.6, seed=S.sd()); p.edge(tr, 'sepia', density=0.8, alpha=0.8)
    for (x, y, r) in ((540, 480, 360), (260, 620, 230), (820, 600, 240), (400, 360, 220), (700, 340, 220)):
        cr = p.blob(x, y, r, r * 0.7, 0.2, seed=S.sd())
        p.form(cr, ('meadow', 'moss', 'pine', 'forest'), p.flow(-50, 40), LIGHT, density=1.3, seed=S.sd())
    shade = p.ellipse(540, 1450, 520, 110) * (p.YY > 1350)
    p.form(shade, ('sage', 'moss', 'pine'), 0, LIGHT, density=0.9, seed=S.sd())
    rr = np.random.default_rng(4)
    for _ in range(14):
        x, y = rr.uniform(120, 960), rr.uniform(1380, 1530)
        p.lift(p.ellipse(x, y, 18, 8), 'butter', 0.5)
    figure(S, 420, 1500, 300, coat=COAT, hair=HAIR, back=False, walk=0.4)
    S.save('tree_shade')


def mirror():
    """自分の顔は見えない: the young woman holding a little hand mirror up, surprised and thoughtful"""
    S = Shot(2205); p = S.p
    ARMS = [[(650, 1000), (720, 900), (760, 800)]]
    m = her(S, 470, 760, 160, plan=True, arms=ARMS)
    hj.room(S, m, win_box=(680, 160, 1010, 520))
    her(S, 470, 760, 160, arms=ARMS, smile=False, look=(0.5, -0.1))
    p.line(curve([(455, 865), (470, 872), (485, 865)], 8), 'brick', 2.4, 0.8, alpha=0.9)
    for sgn in (-1, 1): p.line([(470 + sgn * 54 - 16, 712), (470 + sgn * 54 + 16, 706)], 'umber', 2.4, 0.8, alpha=0.8)
    hd = p.rect(752, 820, 772, 960); erase(S, hd); p.form(hd, ('butter', 'gold', 'amber', 'ochre'), 90, LIGHT, density=1.5, seed=S.sd())
    fr = p.ellipse(762, 700, 110, 130); gl = p.ellipse(762, 700, 92, 112)
    erase(S, fr); p.form(fr * (1 - gl), ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(gl, ('sky_pale', 'powder', 'cream'), 0, LIGHT, density=1.0, seed=S.sd())
    p.form(p.ellipse(770, 710, 46, 52) * gl, SKIN, 0, LIGHT, density=1.2, seed=S.sd())
    p.form(p.ellipse(770, 670, 52, 34) * gl, HAIR, 0, LIGHT, density=1.3, seed=S.sd())
    p.lift(p.poly([(700, 620), (730, 600), (680, 760), (660, 740)]) * gl, 'white', 0.7)
    p.form(p.ellipse(762, 960, 34, 30), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('mirror')


def starry():
    """神様も、目に見えない方: a vast starry night over a quiet Japanese town; a small person looking up in wonder"""
    S = Shot(2206); p = S.p
    m = (p.YY < 1460).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['indigo', 'ultramarine', 'slate'], (60, 150), (1.8, 2.6), 1.8, 0.8, seed=S.sd())
    p.hatch(m * p.value(0.0, 1.0, 0, 1460), p.flow(-2, 4), ['violet', 'cobalt', 'periwinkle'], (60, 140), (1.8, 2.4), 1.0, 0.7, alpha=0.6, seed=S.sd())
    rr = np.random.default_rng(6)
    for _ in range(320):
        x, y = rr.uniform(20, 1060), rr.uniform(20, 1150); s = rr.uniform(2.5, 6.5)
        p.lift(p.ellipse(x, y, s, s), 'cream', rr.uniform(0.8, 1.0), tooth=0.0)
    for _ in range(14):
        x, y = rr.uniform(60, 1020), rr.uniform(60, 900)
        p.glow(x, y, 30, strength=0.7, density=0.7); p.lift(p.ellipse(x, y, 7, 7), 'white', 1.0, tooth=0)
    band = np.exp(-((p.YY - (200 + p.XX * 0.6)) / 140) ** 2) * m
    p.lift(blur(band, 30), 'lavender', 0.35)
    for (x0, x1, top, c) in ((0, 220, 1150, ('slate', 'indigo', 'umber', 'sepia')), (240, 480, 1100, ('stone', 'slate', 'indigo', 'umber')),
                             (640, 880, 1130, ('slate', 'indigo', 'umber', 'sepia')), (900, 1080, 1180, ('stone', 'slate', 'indigo', 'umber'))):
        b = p.rect(x0, top, x1, 1450); erase(S, b); p.form(b, c, 90, LIGHT, density=1.5, seed=S.sd())
        rf = p.poly([(x0 - 20, top + 10), ((x0 + x1) / 2, top - 70), (x1 + 20, top + 10)]); erase(S, rf); p.form(rf, ('indigo', 'slate', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
        p.window(x0 + 50, top + 80, x0 + 130, top + 170, panes=(2, 2), glow=0.9, seed=S.sd())
    p.form((p.YY >= 1450).astype(np.float32), ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, length=(60, 120), density=1.4, seed=S.sd())
    figure(S, 560, 1700, 360, coat=COAT, hair=HAIR, back=True, up=1.0, legs=('cornflower', 'denim', 'indigo'))
    S.save('starry')


def mirror_cross():
    """ほんとうの姿: her reflection in a mirror, a little shadowed; behind, through the window, a far cross on a hill glowing gold"""
    S = Shot(2207); p = S.p
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['stone', 'lavender', 'cream'], (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.7, seed=S.sd())
    fr = p.rect(180, 220, 900, 1380); gl = p.rect(220, 260, 860, 1340)
    erase(S, fr); p.form(fr * (1 - gl), ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(fr, 'sepia', density=0.9, alpha=0.85)
    erase(S, gl)
    # in the glass: the evening window behind her, a hill with the glowing cross
    p.hatch(gl * (p.YY < 900), p.flow(-3, 4), ('dusk_sky', np.clip(p.value(0.2, 1.0, 260, 900), 0, 1)), (40, 100), (1.8, 2.4), 1.6, 0.72, seed=S.sd())
    hill = p.below([220, 540, 860], [900, 820, 900]) * gl
    p.form(hill, ('slate', 'violet', 'indigo', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(gl * (p.YY >= 900), ('stone', 'slate', 'lavender', 'umber'), 0, LIGHT, density=1.3, seed=S.sd())
    cr = np.clip(p.rect(530, 640, 550, 820) + p.rect(495, 680, 585, 696), 0, 1)
    p.glow(540, 720, 200, strength=1.1, density=1.0)
    p.form(cr, ('butter', 'gold', 'amber'), 0, LIGHT, density=1.7, seed=S.sd())
    rm = person(S, 540, 1020, 150, coat=COAT, hair_style='long', plan=True)['mask'] * gl
    erase(S, rm)
    person(S, 540, 1020, 150, coat=COAT, hair_style='long', hair=HAIR, cut=1 - gl, smile=False, eyes_closed=True)
    p.lift(rm * 0, 'cream', 0)
    p.hatch(rm, 60, ['slate', 'indigo'], (20, 50), (1.6, 2.2), 0.9, 0.6, opacity=0.5, alpha=0.4, seed=S.sd())   # a shadow over the reflection
    p.lift(blur(p.ellipse(540, 900, 300, 260), 30) * gl, 'butter', 0.25)
    S.save('mirror_cross')


def heart_hands():
    """買い取られた: two hands gently holding a small glowing heart like a treasure, warm light"""
    S = Shot(2208); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-10, 6), ['apricot', 'butter', 'peach'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.glow(540, 960, 620, strength=1.2, density=1.1)
    hms = []
    for (x, ang, curl, sx) in ((450, -112, -0.5, 180), (630, -68, 0.5, 900)):
        sl = p.tube([(sx, 1980), ((sx + x) / 2, 1620), (x, 1330)], 140, 115)
        erase(S, sl); p.form(sl, ('cream', 'ivory', 'sand', 'tan'), p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
        p.edge(sl, 'tan', density=0.8, alpha=0.7)
    for (x, ang, curl) in ((450, -112, -0.5), (630, -68, 0.5)):
        hms.append(hand(S, x, 1240, 1.9, ang, curl=curl))
    hm = heart_mask(p, 540, 1080, 95)
    p.glow(540, 1080, 260, strength=1.2, density=1.1)
    erase(S, hm); p.form(hm, ('pink', 'rose', 'coral', 'brick'), p.contour(hm, 8, 30), LIGHT, density=1.6, warm='butter', seed=S.sd())
    p.edge(hm, 'brick', density=0.9, alpha=0.85)
    p.lift(p.ellipse(500, 1030, 26, 16, rot=-30), 'white', 0.8)
    S.save('heart_hands')


def sunset_walk():
    """見守られています: the young woman walking home at sunset, a long soft shadow beside her, warm light round her"""
    S = Shot(2209); p = S.p
    m = (p.YY < 1150).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ('dusk_sky', np.clip(p.value(0.0, 1.0, 0, 1150) * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.8, 0.76, seed=S.sd())
    p.hatch(m * smoothstep(400, 1150, p.YY), p.flow(-3, 4), ['peach', 'apricot', 'butter'], (60, 140), (1.8, 2.4), 1.0, 0.64, alpha=0.55, seed=S.sd())
    p.glow(820, 1080, 440, strength=1.0, density=1.0)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1100, 1060, 1080, 1040, 1070, 1090, 1060], RIDGES[0], mist=0.5)
    for (x, w_, hh) in ((120, 200, 200), (360, 160, 170)):
        hs = p.rect(x - w_ / 2, 1150 - hh, x + w_ / 2, 1150); erase(S, hs); p.form(hs, ('cream', 'sand', 'tan', 'sienna'), 90, LIGHT, density=1.4, seed=S.sd())
        rf = p.poly([(x - w_ / 2 - 20, 1160 - hh), (x, 1080 - hh), (x + w_ / 2 + 20, 1160 - hh)]); erase(S, rf); p.form(rf, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
        p.window(x - 30, 1080 - hh * 0.5, x + 30, 1140 - hh * 0.5, panes=(1, 1), glow=0.9, seed=S.sd())
    ground(S, 1150, cols=('butter', 'sand', 'ochre', 'tan'), flowers=0)
    road = p.poly([(500, 1150), (640, 1150), (900, 1920), (200, 1920)])
    p.form(road, ('cream', 'butter', 'sand', 'tan'), p.flow(90, 8), LIGHT, density=1.2, seed=S.sd())
    fm = figure(S, 520, 1600, 360, coat=COAT, hair=HAIR, back=True, walk=0.4)
    sh = p.poly([(520, 1600), (560, 1610), (220, 1760), (160, 1740)])
    p.form(sh, ('tan', 'sienna', 'umber'), 0, LIGHT, density=0.9, seed=S.sd())
    p.lift(blur(p.ellipse(520, 1420, 220, 260), 40) * (1 - fm), 'butter', 0.35)
    S.save('sunset_walk')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
