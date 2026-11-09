"""the paintings. python3 shots.py NAME [--stages DIR]"""
import sys
from pcommon import *


def room(S, fg, win_box=(90, 160, 470, 700), wall_to=1300):
    p = S.p
    wall = (p.YY < wall_to).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ('cream', 'ivory', 'apricot'), (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.55,
            avoid=fg, seed=S.sd())
    p.hatch(wall * smoothstep(300, 1080, p.XX), p.flow(4, 4, 500), ('peach', 'apricot'), (60, 140), (1.8, 2.4), 0.8, 0.6,
            alpha=0.4, avoid=fg, seed=S.sd())
    x0, y0, x1, y1 = win_box
    win = p.rect(x0, y0, x1, y1)
    p.hatch(win, p.flow(-4, 4), ('day_sky', p.value(0.25, 0.95, y0, y1)), (40, 100), (1.7, 2.4), 1.6, 0.7, avoid=fg, seed=S.sd())
    p.glow((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * 0.7, strength=0.7, density=0.8, clip=win)
    for x in (x0, (x0 + x1) / 2, x1):
        p.line([(x, y0), (x, y1)], 'tan', 9.0, 0.8, alpha=0.9)
    for y in (y0, (y0 + y1) / 2, y1):
        p.line([(x0, y), (x1, y)], 'tan', 9.0, 0.8, alpha=0.9)
    beam = p.poly([(x1, y0 + 40), (x1 + 520, y0 + 600), (x1 + 520, y1 + 700), (x1, y1)]) * smoothstep(x1 + 560, x1, p.XX)
    p.hatch(beam, 40, ('butter', 'cream'), (40, 100), (1.8, 2.4), 0.9, 0.62, opacity=0.6, alpha=0.4, avoid=fg, seed=S.sd())


def gassho(S, x, y, s=1.0):
    """two small hands pressed together, fingertips up (the いただきます gesture)"""
    p = S.p
    out = curve([(x - 34 * s, y + 70 * s), (x - 40 * s, y + 10 * s), (x - 30 * s, y - 60 * s), (x - 14 * s, y - 104 * s),
                 (x, y - 112 * s), (x + 14 * s, y - 104 * s), (x + 30 * s, y - 60 * s), (x + 40 * s, y + 10 * s),
                 (x + 34 * s, y + 70 * s)], 60)
    m = p.poly(out, smooth=True)
    p.form(m, SKIN, p.contour(m, 6, 90), LIGHT, length=(8, 16), width=(1.3, 1.9), density=1.6, warm='peach', seed=S.sd())
    p.line(curve([(x, y - 108 * s), (x, y + 60 * s)], 20), 'skin_shade', 2.4, 0.75, alpha=0.85)
    for sgn in (-1, 1):                                  # finger lines and the thumbs
        for k, yy in enumerate((-70, -40, -12)):
            p.line(curve([(x + sgn * 34 * s, y + (yy + 8) * s), (x + sgn * 10 * s, y + yy * s)], 6), 'skin_shade', 1.8, 0.6, alpha=0.6)
        p.line(curve([(x + sgn * 6 * s, y + 10 * s), (x + sgn * 18 * s, y + 46 * s), (x + sgn * 14 * s, y + 66 * s)], 10),
               'skin_shade', 2.0, 0.65, alpha=0.75)
    p.edge(m, 'skin_shade', density=0.9)
    return m


def hands():
    """① いただきます: a child at the low table, eyes closed, hands pressed together; rice, miso soup, a little fish"""
    S = Shot(301); p = S.p
    table = p.poly([(0, 1290), (1080, 1290), (1080, 1920), (0, 1920)])
    ARMS = [[(420, 1000), (390, 1150), (500, 1205)], [(660, 1000), (690, 1150), (580, 1205)]]
    kid = person(S, 540, 760, 160, coat=('cream', 'butter', 'apricot', 'amber'), hair_style='bob', plan=True, arms=ARMS, cut=table)
    fg = kid['mask']
    room(S, np.clip(fg + table, 0, 1))
    S.p.stage('room')
    person(S, 540, 760, 160, coat=('cream', 'butter', 'apricot', 'amber'), hair_style='bob', eyes_closed=True, smile=True,
           arms=ARMS, cut=table, hands=False)
    gassho(S, 540, 1150, 1.15)
    p.form(table, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', avoid=fg, seed=S.sd())
    p.line([(0, 1292), (1080, 1292)], 'sienna', 5, 0.8, alpha=0.8)
    for k in range(6):
        p.line(curve([(0, 1360 + k * 95), (540, 1366 + k * 95), (1080, 1358 + k * 95)], 30), 'brown', 2.0, 0.5, alpha=0.4)
    S.p.stage('kid')
    rice_bowl(S, 330, 1460, 150)
    soup = np.clip(p.poly(curve([(620, 1470), (650, 1580), (770, 1630), (890, 1580), (920, 1470)], 30)) + p.ellipse(770, 1470, 150, 60), 0, 1)
    p.form(soup, ('brick', 'red', 'sienna', 'umber'), 0, LIGHT, length=(12, 26), density=1.3, seed=S.sd())
    p.form(p.ellipse(770, 1465, 128, 46), ('apricot', 'ochre', 'amber'), 0, LIGHT, length=(10, 22), density=1.2, seed=S.sd())
    p.dots(p.ellipse(770, 1462, 100, 32), ('sage', 'leaf'), n=40, size=(3, 5))
    p.strokes([curve([(740, 1420), (725, 1350), (750, 1290)], 30), curve([(800, 1420), (815, 1350), (790, 1280)], 30)],
              'white', width=7.0, pressure=0.55, opacity=0.8, alpha=0.5)
    plate = p.ellipse(540, 1760, 210, 62)
    p.form(plate, ('white', 'cream', 'powder', 'cornflower'), 0, LIGHT, length=(20, 40), density=1.1, seed=S.sd())
    fish = p.blob(540, 1745, 140, 34, 0.04)
    p.form(fish, ('peach', 'apricot', 'tan', 'sienna'), 0, LIGHT, length=(10, 22), density=1.4, warm='butter', seed=S.sd())
    for k in range(5):
        p.line(curve([(470 + k * 30, 1725), (480 + k * 30, 1765)], 6), 'sienna', 2.0, 0.6, alpha=0.6)
    p.line(curve([(930, 1700), (1060, 1880)], 20), 'umber', 10, 0.85, alpha=0.95)
    p.line(curve([(960, 1690), (1075, 1860)], 20), 'umber', 10, 0.85, alpha=0.95)
    p.glow(540, 1100, 260, colours='glow', strength=0.45, density=0.6)
    S.save('hands')


def torii(S, cx, base, w, h, avoid=None):
    p = S.p
    col = ('apricot', 'vermilion', 'red', 'brick')
    posts = [p.poly([(cx + sgn * w * 0.36 - 22, base), (cx + sgn * w * 0.34 - 18, base - h), (cx + sgn * w * 0.34 + 18, base - h),
                     (cx + sgn * w * 0.36 + 22, base)]) for sgn in (-1, 1)]
    kasagi = p.poly(curve([(cx - w * 0.62, base - h - 40), (cx, base - h - 10), (cx + w * 0.62, base - h - 40)], 40).tolist()
                    + curve([(cx + w * 0.58, base - h + 10), (cx, base - h + 36), (cx - w * 0.58, base - h + 10)], 40).tolist())
    nuki = p.rect(cx - w * 0.48, base - h + 120, cx + w * 0.48, base - h + 160)
    m = np.clip(sum(posts) + kasagi + nuki, 0, 1)
    p.form(np.clip(sum(posts), 0, 1), col, 90, LIGHT, length=(20, 50), density=1.6, warm='butter', seed=S.sd())
    p.form(nuki, col, 0, LIGHT, length=(20, 50), density=1.6, seed=S.sd())
    p.form(kasagi, ('slate', 'indigo', 'umber'), 0, LIGHT, length=(20, 50), density=1.5, seed=S.sd())
    for sgn in (-1, 1):
        p.form(p.rect(cx + sgn * w * 0.36 - 26, base - 40, cx + sgn * w * 0.36 + 26, base), ('stone', 'warmgrey', 'umber'), 90,
               LIGHT, length=(10, 20), density=1.4, seed=S.sd())
    return m


def shrine():
    """② 初詣: a clear winter morning, a vermilion torii at the top of stone steps, pines, a few visitors walking up"""
    S = Shot(302); p = S.p
    tor = torii(S, 540, 1150, 620, 560) if False else None
    sky = (p.YY < 1200).astype(np.float32)
    morning_sky(S, sky)
    clouds(S, [(260, 260, 380, 90), (840, 420, 300, 70)])
    for (x, y, h, r) in ((110, 1150, 520, 190), (980, 1160, 480, 170)):
        p.tree(x, y, h, r, ('sage', 'moss', 'pine', 'forest'), trunk=('tan', 'brown', 'umber'), clumps=9, leaf=(6, 12),
               light=LIGHT, seed=S.sd())
    torii(S, 540, 1170, 620, 560)
    steps = p.poly([(260, 1170), (820, 1170), (1080, 1920), (0, 1920)])
    gravel = (p.YY >= 1150).astype(np.float32) * (1 - steps)
    p.form(gravel, ('sand', 'stone', 'warmgrey', 'pebble'), 0, LIGHT, length=(20, 50), density=1.4, seed=S.sd())
    p.dots(gravel, ('pebble', 'warmgrey', 'ivory'), n=500, size=(2, 5))
    p.form(steps, ('ivory', 'stone', 'warmgrey', 'pebble'), 0, LIGHT, length=(40, 100), density=1.4, warm='butter', seed=S.sd())
    for k in range(9):
        y = 1180 + (k ** 1.35) * 32
        x0 = 260 - (y - 1170) * 0.35; x1 = 820 + (y - 1170) * 0.35
        p.line([(x0, y), (x1, y)], 'pebble', 3.0, 0.7, alpha=0.8)
    for (x, y, R, coat, hs) in ((430, 1380, 42, ('powder', 'cornflower', 'slate', 'indigo'), 'short'),
                                (520, 1450, 40, ('peach', 'coral', 'terracotta', 'brick'), 'bob'),
                                (660, 1560, 52, ('cream', 'sand', 'tan', 'brown'), 'bun'),
                                (360, 1640, 58, ('lavender', 'mauve', 'violet', 'indigo'), 'short')):
        person(S, x, y, R, coat=coat, hair_style=hs, eyes_closed=False, smile=False, look=(0, -1), back=True) if False else None
        head = p.ellipse(x, y, R * 0.9, R)
        body = p.poly(curve([(x - R * 0.5, y + R * 0.9), (x - R * 1.2, y + R * 1.5), (x - R * 1.4, y + R * 3.4), (x + R * 1.4, y + R * 3.4),
                             (x + R * 1.2, y + R * 1.5), (x + R * 0.5, y + R * 0.9)], 40), smooth=True)
        p.form(body, coat, 80, LIGHT, length=(12, 26), density=1.4, warm='butter', seed=S.sd())
        p.form(head, ('hair_light', 'hair', 'umber'), p.radial(x, y - R), LIGHT, length=(10, 20), density=1.4, seed=S.sd())
        p.form(p.rect(x - R * 0.55, y + R * 2.2, x + R * 0.55, y + R * 2.3) * body, ('cream', 'ivory', 'sand'), 0, LIGHT, density=0.6, seed=S.sd())
    p.glow(540, 700, 380, strength=0.4, density=0.6)
    S.save('shrine')


def omamori():
    """② お守り: a brocade amulet pouch with 御守 embroidered in gold, hanging by its red cord from a school bag strap,
    in soft morning light"""
    S = Shot(303); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-20, 10, 300), ('butter', 'apricot', 'peach', 'cream'), (60, 140), (1.8, 2.6), 1.6, 0.66, seed=S.sd())
    for (x, y, r) in ((200, 300, 160), (900, 600, 200), (240, 1600, 180), (880, 1700, 140)):
        p.glow(x, y, r, strength=0.7, density=0.7)
    strap = p.tube([(1080, 120), (700, 260), (380, 360), (0, 420)], 90, 90)
    p.form(strap, ('pink', 'coral', 'red', 'brick'), p.contour(strap, 10), LIGHT, length=(30, 70), density=1.5, seed=S.sd())
    for k in range(2):
        p.line(curve([(1080, 90 + k * 60), (700, 230 + k * 60), (380, 330 + k * 60), (0, 390 + k * 60)], 40), 'apricot', 2.2, 0.7, alpha=0.7)
    om = p.poly(curve([(330, 1600), (330, 860), (380, 760), (540, 720), (700, 760), (750, 860), (750, 1600), (540, 1640)], 80), smooth=True)
    p.line(curve([(520, 330), (510, 560), (530, 730)], 30), 'red', 8, 0.85, alpha=0.95)
    p.line(curve([(560, 330), (575, 560), (552, 730)], 30), 'red', 8, 0.85, alpha=0.95)
    p.form(om, ('lavender', 'mauve', 'violet', 'indigo'), 90, LIGHT, length=(16, 34), density=1.7, warm='peach', seed=S.sd())
    ys, xs = np.nonzero(om > 0.6)                          # little gold brocade flowers
    for i in S.r.choice(len(xs), 40, replace=False):
        x, y = xs[i], ys[i]
        if 420 < x < 660 and 900 < y < 1480: continue
        for k in range(5):
            a_ = k * 1.256
            p.line([(x, y), (x + 13 * np.cos(a_), y + 13 * np.sin(a_))], 'gold', 3.0, 0.8, alpha=0.9)
    from PIL import ImageFont
    from core import text_mask
    f = ImageFont.truetype(os.path.join(HERE, '..', 'fonts', 'ZenMaruGothic-900.ttf'), 210)
    for ch, y in (('御', 1020), ('守', 1300)):
        tm = blur(text_mask(H, W, ch, f, (540, y), anchor='mm'), 1.0)
        p.hatch(tm, 90, ('butter', 'gold', 'amber'), (8, 18), (1.6, 2.2), 2.4, 0.9, opacity=0.85, alpha=0.95, seed=S.sd())
    knot = p.ellipse(540, 730, 46, 30)
    p.form(knot, ('pink', 'coral', 'red', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    for sgn in (-1, 1):
        p.line(curve([(540, 720), (540 + sgn * 80, 640), (540 + sgn * 56, 580)], 20), 'red', 9, 0.85, alpha=0.95)
    p.edge(om, 'indigo', density=0.9)
    p.glow(380, 900, 200, strength=0.5, density=0.6)
    S.save('omamori')


def family():
    """③ 自分の力だけで…: grandma and a child at the breakfast table, grandma passing a bowl of rice, both smiling"""
    S = Shot(304); p = S.p
    table = p.poly([(0, 1330), (1080, 1330), (1080, 1920), (0, 1920)])
    GA = [[(240, 1050), (300, 1200), (430, 1250)], [(420, 1050), (460, 1180), (480, 1250)]]
    KA = [[(700, 1110), (650, 1220), (600, 1270)], [(850, 1110), (880, 1230), (830, 1290)]]
    g = person(S, 330, 800, 150, coat=('lavender', 'mauve', 'violet', 'indigo'), hair_style='bun', grey=True, plan=True, arms=GA, cut=table)
    k = person(S, 780, 900, 125, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='short', plan=True, arms=KA, cut=table)
    fg = np.clip(g['mask'] + k['mask'], 0, 1)
    room(S, np.clip(fg + table, 0, 1), win_box=(620, 140, 1000, 640))
    person(S, 330, 800, 150, coat=('lavender', 'mauve', 'violet', 'indigo'), hair_style='bun', grey=True, arms=GA, cut=table, look=(0.6, 0.2))
    person(S, 780, 900, 125, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='short', arms=KA, cut=table, look=(-0.6, -0.3))
    for sgn in (-1, 1):                                    # grandma's smile lines
        p.line(curve([(330 + sgn * 70, 820), (330 + sgn * 80, 850)], 6), 'skin_shade', 2.0, 0.6, alpha=0.6)
    p.form(table, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', avoid=fg, seed=S.sd())
    p.line([(0, 1332), (1080, 1332)], 'sienna', 5, 0.8, alpha=0.8)
    rice_bowl(S, 520, 1230, 95)
    rice_bowl(S, 300, 1560, 120, steam=False)
    rice_bowl(S, 800, 1580, 110, steam=False)
    p.form(p.ellipse(560, 1760, 150, 46), ('white', 'cream', 'powder'), 0, LIGHT, density=1.1, seed=S.sd())
    p.dots(p.ellipse(560, 1750, 110, 28), ('lemon', 'butter', 'sun'), n=30, size=(6, 10))     # tamagoyaki pieces
    S.save('family')


def paddy():
    """④ rain over green rice paddies below the hills; a farmhouse; the rain soft and silver"""
    S = Shot(305); p = S.p
    sky = (p.YY < 700).astype(np.float32)
    p.hatch(sky, p.flow(-6, 4), ('powder', 'lavender', 'warmgrey', 'sky_pale'), (60, 140), (1.8, 2.5), 1.8, 0.72, seed=S.sd())
    p.hatch(sky * (p.YY < 350), p.flow(-4, 4), ('slate', 'periwinkle'), (60, 140), (1.8, 2.5), 0.9, 0.66, alpha=0.5, seed=S.sd())
    hills = p.below([0, 300, 600, 900, 1080], [620, 560, 600, 540, 580])
    p.form(hills * (p.YY < 760), ('sage', 'moss', 'pine', 'forest'), p.flow(-8, 10), LIGHT, length=(30, 70), density=1.3, cool='lavender', seed=S.sd())
    p.cottage(800, 760, 160, 110, wall=('cream', 'ivory', 'sand', 'tan'), roof=('slate', 'indigo', 'umber', 'sepia'), light=LIGHT, glow=0.3, seed=S.sd())
    # terraced paddies: bands of green and water reflecting the sky
    for k, y0 in enumerate([760, 900, 1080, 1300, 1560]):
        y1 = [900, 1080, 1300, 1560, 1920][k]
        band = (p.YY >= y0) * (p.YY < y1)
        p.form(band.astype(np.float32), ('yellowgreen', 'meadow', 'grass', 'leaf'), 0, LIGHT, length=(40, 100), density=1.2, seed=S.sd())
        water = band * (p.YY < y0 + (y1 - y0) * 0.35)
        p.hatch(water.astype(np.float32), 0, ('powder', 'sky_pale', 'cornflower'), (40, 100), (1.6, 2.3), 1.2, 0.7, opacity=0.5, seed=S.sd())
        p.line([(0, y0), (1080, y0)], 'olive', 4, 0.7, alpha=0.8)
        rows = np.arange(30, 1080, 60 + k * 14)
        for x in rows:
            p.grass(p.ellipse(x, y1 - (y1 - y0) * 0.3, 14 + k * 4, 6 + k * 2), ('grass', 'leaf', 'yellowgreen'),
                    height=(20 + k * 14, 40 + k * 22), density=1.2, seed=S.sd())
    rain = []
    for i in range(900):
        x, y = S.r.uniform(0, 1080), S.r.uniform(0, 1920)
        L = S.r.uniform(30, 70)
        rain.append([(x, y), (x + L * 0.12, y + L)])
    p.strokes(rain[:500], ['slate', 'periwinkle', 'cornflower'], width=2.2, pressure=0.7, opacity=0.4, alpha=0.6)
    p.strokes(rain[500:], ['white', 'cream'], width=2.4, pressure=0.7, opacity=0.8, alpha=0.7)
    for i in range(60):
        x, y = S.r.uniform(40, 1040), S.r.uniform(780, 1900)
        p.ripples(x, y, 18, 5, rings=2, colour='cream')
    S.save('paddy')


def rice():
    """④ golden ears of rice bowing heavy in the sun, close; the sun warm behind them"""
    S = Shot(306); p = S.p
    sky = np.ones((H, W), np.float32)
    v = p.value(0.15, 0.95, 0, 1300)
    p.hatch(sky, p.flow(-4, 4), ('day_sky', v), (60, 150), (1.8, 2.6), 1.5, 0.72, seed=S.sd())
    p.hatch(sky * smoothstep(400, 1300, p.YY), p.flow(-3, 4), ('glow', 1 - v), (60, 140), (1.8, 2.5), 1.3, 0.72, opacity=0.6, seed=S.sd())
    p.glow(760, 640, 300, strength=1.2, density=1.1)
    field = (p.YY > 1250).astype(np.float32)
    p.form(field, ('butter', 'gold', 'amber', 'ochre'), p.flow(-80, 10), LIGHT, length=(30, 80), density=1.5, seed=S.sd())
    p.grass(field, ('gold', 'amber', 'ochre', 'butter'), height=(40, 90), density=1.0, seed=S.sd())
    for k in range(14):                                    # near stalks bowing with heavy ears
        x0 = 40 + k * 76 + S.r.uniform(-20, 20)
        top = S.r.uniform(700, 1000)
        stem = curve([(x0, 1920), (x0 + 10, 1500), (x0 + 30, top + 120), (x0 + 90, top)], 60)
        p.strokes([stem], ['olive', 'gold'], width=5.0, pressure=0.75, opacity=0.4, alpha=0.9)
        ear = curve([(x0 + 90, top), (x0 + 150, top + 60), (x0 + 175, top + 170)], 30)
        for j, (ex, ey) in enumerate(ear[::3]):
            for sgn in (-1, 1):
                p.ellipse  # noqa
                p.strokes([[(ex, ey), (ex + sgn * 14, ey + 18)]], ['gold', 'amber', 'butter'], width=7.0, pressure=0.8, opacity=0.5, alpha=0.95)
        p.strokes([ear], 'amber', width=3.0, pressure=0.7, opacity=0.4, alpha=0.8)
        for (lx, ly) in stem[20:50:10]:
            p.strokes([curve([(lx, ly), (lx - 60, ly - 40), (lx - 120, ly - 30)], 20)], ['olive', 'gold'], width=6, pressure=0.7, opacity=0.4, alpha=0.8)
    S.save('rice')


def bible():
    """⑤ 聖書: an open Bible on a wooden desk by the window, the morning light falling across the pages"""
    S = Shot(307); p = S.p
    wall = (p.YY < 900).astype(np.float32)
    room(S, np.zeros((H, W), np.float32), win_box=(120, 120, 600, 760), wall_to=900)
    desk = (p.YY >= 900).astype(np.float32)
    p.form(desk, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', seed=S.sd())
    for k in range(8):
        p.line(curve([(0, 960 + k * 120), (540, 966 + k * 120), (1080, 958 + k * 120)], 30), 'brown', 2.0, 0.5, alpha=0.4)
    cover = p.poly([(110, 1140), (970, 1140), (1010, 1660), (70, 1660)]) * (1 - np.clip(
        p.poly(curve([(130, 1160), (300, 1110), (530, 1150), (530, 1630), (300, 1600), (110, 1640)], 60), smooth=True)
        + p.poly(curve([(550, 1150), (780, 1110), (950, 1160), (970, 1640), (780, 1600), (550, 1630)], 60), smooth=True), 0, 1))
    p.form(cover, ('brick', 'sienna', 'brown', 'umber'), 0, LIGHT, length=(20, 50), density=1.4, seed=S.sd())
    L = p.poly(curve([(130, 1160), (300, 1110), (530, 1150), (530, 1630), (300, 1600), (110, 1640)], 60), smooth=True)
    R = p.poly(curve([(550, 1150), (780, 1110), (950, 1160), (970, 1640), (780, 1600), (550, 1630)], 60), smooth=True)
    for m, x0 in ((L, 170), (R, 590)):
        p.lift(m, 'white', 0.9)
        p.hatch(m, 90, ('white', 'cream', 'ivory'), (20, 50), (1.6, 2.3), 1.5, 0.7, opacity=0.85, alpha=0.8, seed=S.sd())
        for kk in range(14):
            y = 1200 + kk * 28
            xs = S.r.uniform(0, 30)
            p.line([(x0 + xs, y), (x0 + 300 - S.r.uniform(0, 40), y + 2)], 'pebble', 2.4, 0.7, alpha=0.75)
    p.hatch(p.ellipse(540, 1390, 60, 260) * np.clip(L + R, 0, 1), 90, ('tan', 'sand'), (20, 40), (1.6, 2.2), 1.0, 0.6, alpha=0.5, seed=S.sd())
    p.line(curve([(560, 1150), (575, 1700)], 20), 'red', 8, 0.85, alpha=0.95)
    beam = p.poly([(600, 120), (760, 120), (1080, 1300), (1080, 1800), (300, 1800), (380, 760)])
    p.hatch(beam * 0.8, 62, ('butter', 'cream', 'white'), (60, 140), (1.8, 2.4), 1.0, 0.62, opacity=0.7, alpha=0.45, seed=S.sd())
    p.glow(560, 1380, 380, strength=0.8, density=0.8)
    p.dots(beam * (p.YY < 1100), ('white', 'cream', 'butter'), n=90, size=(2, 4))
    S.save('bible')


def sunrise():
    """⑤ 上から来る: the sun coming up over the hills, morning light over a small town and its fields"""
    S = Shot(308); p = S.p
    sky = (p.YY < 1100).astype(np.float32)
    v = p.value(0.0, 1.0, 0, 1100)
    p.hatch(sky, p.flow(-3, 4), ('dusk_sky', np.clip(v * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.7, 0.74, seed=S.sd())
    clouds(S, [(220, 300, 360, 80), (820, 220, 300, 70), (600, 560, 260, 50)])
    p.glow(540, 1060, 420, strength=1.4, density=1.2)
    p.lift(p.ellipse(540, 1080, 120, 120), 'sun', 0.8)
    far = p.below([0, 270, 540, 810, 1080], [1040, 1000, 1080, 990, 1050])
    p.form(far * (p.YY < 1300), ('lavender', 'periwinkle', 'violet', 'indigo'), p.flow(-6, 10), LIGHT, length=(30, 70), density=1.3,
           warm='peach', seed=S.sd())
    near = p.below([0, 300, 700, 1080], [1260, 1220, 1270, 1230])
    p.form(near, ('meadow', 'yellowgreen', 'grass', 'moss'), p.flow(-8, 12), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    for (x, y, w, h, wall, roof) in ((120, 1330, 110, 80, ('cream', 'ivory', 'sand', 'tan'), ('peach', 'terracotta', 'brick', 'sienna')),
                                     (300, 1310, 90, 70, ('powder', 'sky_pale', 'cornflower', 'slate'), ('slate', 'indigo', 'umber', 'sepia')),
                                     (720, 1340, 130, 90, ('cream', 'sun', 'apricot', 'amber'), ('lavender', 'slate', 'indigo', 'violet')),
                                     (900, 1300, 90, 70, ('cream', 'pink', 'rose', 'brick'), ('peach', 'terracotta', 'brick', 'sienna'))):
        p.cottage(x, y, w, h, wall, roof, light=LIGHT, glow=0.6, seed=S.sd())
    fields = (p.YY > 1400).astype(np.float32)
    for k in range(6):
        band = fields * (p.YY > 1400 + k * 90) * (p.YY < 1490 + k * 90)
        p.form(band, [('butter', 'gold', 'amber', 'ochre'), ('yellowgreen', 'meadow', 'grass', 'leaf')][k % 2], 0, LIGHT, length=(40, 100), density=1.3, seed=S.sd())
    p.flowers(fields * (p.YY > 1800), n=60, size=(5, 9))
    for (x, y) in ((400, 600), (440, 630), (480, 590)):
        p.line(curve([(x - 20, y), (x - 8, y - 10), (x, y - 2), (x + 8, y - 10), (x + 20, y)], 12), 'sepia', 2.6, 0.8, alpha=0.85)
    S.save('sunrise')


def window():
    """⑥ 先に愛してくださった: a young woman at the open window in the morning, eyes closed, hands together at her chest,
    the light on her face; plants on the sill"""
    S = Shot(309); p = S.p
    ARMS = [[(420, 1180), (400, 1330), (510, 1360)], [(660, 1180), (680, 1330), (570, 1360)]]
    w = person(S, 540, 930, 170, coat=('cream', 'ivory', 'sand', 'tan'), hair_style='bob', plan=True, arms=ARMS)
    win = p.rect(0, 0, 1080, 1920) * (1 - w['mask'])
    morning_sky(S, (p.YY < 1500).astype(np.float32) * (1 - w['mask']))
    clouds(S, [(200, 300, 340, 80), (860, 460, 300, 70)])
    p.glow(860, 300, 360, strength=1.0, density=1.0)
    sill = p.rect(0, 1500, 1080, 1600)
    p.form(sill, ('cream', 'sand', 'tan', 'brown'), 0, LIGHT, length=(60, 120), density=1.4, seed=S.sd())
    p.form(p.rect(0, 1600, 1080, 1920), ('apricot', 'terracotta', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    for x in (40, 1040):
        p.form(p.rect(x - 40, 0, x + 40, 1500), ('cream', 'sand', 'tan'), 90, LIGHT, density=1.3, seed=S.sd())
    person(S, 540, 930, 170, coat=('cream', 'ivory', 'sand', 'tan'), hair_style='bob', eyes_closed=True, arms=ARMS, hands=False,
           hair=('hair_light', 'hair', 'umber'))
    gassho(S, 540, 1290, 1.2)
    for (x, c) in ((150, ('terracotta', 'brick')), (930, ('powder', 'cornflower'))):
        pot = p.poly([(x - 70, 1420), (x + 70, 1420), (x + 55, 1510), (x - 55, 1510)])
        p.form(pot, c + ('sienna',), 90, LIGHT, density=1.4, seed=S.sd())
        p.leaves(p.blob(x, 1340, 110, 90, 0.2), ('leaf', 'grass', 'meadow', 'forest'), size=(12, 22), density=1.2, seed=S.sd())
    p.flowers(p.blob(150, 1300, 80, 50), kinds=('daisy', 'buttercup'), n=12, size=(7, 11))
    p.glow(560, 900, 300, strength=0.5, density=0.6)
    S.save('window')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
