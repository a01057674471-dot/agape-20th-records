"""「言霊」 paintings -- the word that made the world. python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *
from PIL import Image, ImageDraw, ImageFont

def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), rel))
    m = importlib.util.module_from_spec(sp); sys.path.insert(0, os.path.dirname(sp.origin)); sp.loader.exec_module(m); return m
h = _load('h_shots', '../../handle/art_src/shots.py')
k = h.k
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4
HERE = os.path.dirname(os.path.abspath(__file__))
ARTD = os.path.join(HERE, '..', 'art')
FONT = os.path.join(HERE, '..', 'fonts', 'ZenMaruGothic-{}.ttf')
SUMI = ('sepia', 'umber', 'indigo', 'slate')


def ema():
    """合格祈願: wooden ema plaques hung on the shrine rack, red cords, a little shrine roof behind, morning"""
    S = Shot(1101); p = S.p
    sky(S, 900, (850, 300, 300))
    p.tree(120, 950, 500, 170, colours=('meadow', 'moss', 'pine', 'forest'), clumps=7, seed=S.sd())
    p.tree(980, 930, 520, 170, colours=('meadow', 'moss', 'pine', 'forest'), clumps=7, seed=S.sd())
    ground(S, 900, cols=('sand', 'butter', 'tan', 'ochre'), flowers=0)
    for x in range(0, 1080, 70):
        p.form(p.blob(x, 905, 60, 40, 0.2, seed=S.sd()), ('moss', 'pine', 'forest', 'sepia'), 0, LIGHT, density=1.3, seed=S.sd())
    rail = [p.rect(60, 560, 1020, 600), p.rect(60, 960, 1020, 1000)]
    for x in (80, 1000):
        r = p.rect(x - 22, 520, x + 22, 1500); erase(S, r); p.form(r, ('tan', 'sienna', 'brown', 'umber'), 90, LIGHT, density=1.5, seed=S.sd())
    for r in rail:
        erase(S, r); p.form(r, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(r, 'sepia', density=0.8, alpha=0.8)
    plaques = []
    rr = np.random.default_rng(4)
    for row, y in ((0, 620), (1, 1020)):
        for j in range(5):
            x = 180 + j * 180 + rr.uniform(-12, 12)
            big = (row == 0 and j == 2)
            w, hh = (230, 200) if big else (150, 130)
            if big: x = 540
            yy = y + (10 if big else rr.uniform(0, 20))
            pts = [(x - w / 2, yy + hh * 0.3), (x - w * 0.32, yy), (x + w * 0.32, yy), (x + w / 2, yy + hh * 0.3), (x + w / 2, yy + hh), (x - w / 2, yy + hh)]
            m = p.poly(pts)
            erase(S, m)
            p.form(m, ('cream', 'sand', 'butter', 'tan'), 0, LIGHT, length=(20, 50), density=1.4, seed=S.sd())
            p.edge(m, 'sienna', width=(1.6, 2.4), density=0.9, alpha=0.85)
            p.line([(x, yy + 8), (x, y - 40)], 'red', 3.0, 0.8, alpha=0.9)
            plaques.append((x, yy, w, hh, big))
    p.glow(850, 300, 300, strength=0.6, density=0.6)
    S.save('ema')
    im = Image.open(os.path.join(ARTD, 'ema.jpg')).convert('RGBA')
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    words = ['合格', '健康', '合格祈願', '良縁', '必勝', '学業', '合格', '家内安全', '感謝', '安全']
    for (x, yy, w, hh, big), wd in zip(plaques, words):
        if big:
            d.text((x, yy + hh * 0.42), '合格', font=ImageFont.truetype(FONT.format(900), 70), fill=(70, 45, 35, 235), anchor='mm')
            d.text((x, yy + hh * 0.78), '祈願', font=ImageFont.truetype(FONT.format(700), 40), fill=(180, 60, 50, 230), anchor='mm')
        else:
            d.text((x, yy + hh * 0.58), wd[:2], font=ImageFont.truetype(FONT.format(700), 40), fill=(80, 55, 40, 215), anchor='mm')
    im.alpha_composite(lay); im.convert('RGB').save(os.path.join(ARTD, 'ema.jpg'), quality=90)


def wedding():
    """結婚式: bride in white with a veil and the groom, petals falling, a chapel door behind"""
    S = Shot(1102); p = S.p
    b = person(S, 400, 700, 150, coat=('white', 'cream', 'ivory', 'sand'), hair_style='bun', plan=True)
    g = person(S, 700, 660, 150, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='short', plan=True)
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'ivory', 'peach'], (60, 140), (1.8, 2.5), 1.6, 0.6, alpha=0.6, seed=S.sd())
    door = p.poly(curve([(250, 1500), (250, 500), (540, 300), (830, 500), (830, 1500)], 60))
    p.form(door, ('powder', 'sky_pale', 'cream', 'lavender'), 0, LIGHT, density=1.0, seed=S.sd())
    p.edge(door, 'tan', density=0.7, alpha=0.6)
    ground(S, 1500, cols=('rose', 'pink', 'coral', 'brick'), flowers=0)
    erase(S, g['mask'])
    person(S, 700, 660, 150, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='short', smile=True, look=(-0.4, 0.1), hair=('hair', 'umber', 'sepia'))
    p.form(p.poly([(700, 820), (680, 900), (720, 900)]), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd())
    erase(S, b['mask'])
    veil = p.blob(400, 760, 210, 330, 0.06, seed=3) * (p.YY > 560) * (1 - b['mask'] * 0.0)
    p.hatch(veil * (1 - b['mask']) * (1 - g['mask']), 90, ['white', 'cream'], (40, 100), (1.6, 2.2), 1.0, 0.6, opacity=0.5, alpha=0.45, seed=S.sd())
    person(S, 400, 700, 150, coat=('white', 'cream', 'ivory', 'sand'), hair_style='bun', smile=True, eyes_closed=True)
    bq = p.blob(450, 1120, 80, 60, 0.2, seed=8)
    p.flowers(bq, kinds=('daisy', 'poppy'), n=14, size=(9, 14))
    rr = np.random.default_rng(2)
    for _ in range(40):
        x, y = rr.uniform(0, 1080), rr.uniform(100, 1400)
        m = p.ellipse(x, y, 9, 6, rot=rr.uniform(0, 180))
        p.form(m, ('pink', 'rose', 'coral'), 0, LIGHT, density=1.4, seed=S.sd())
    S.save('wedding')


def washi():
    """the calligraphy desk from above: dark felt, a sheet of white washi held by a wooden paperweight, the inkstone"""
    S = Shot(1103); p = S.p
    felt = np.ones((H, W), np.float32)
    p.hatch(felt, p.flow(10, 8), ['slate', 'indigo', 'ultramarine'], (60, 150), (1.8, 2.6), 1.9, 0.78, seed=S.sd())
    sheet = p.rect(150, 300, 930, 1200)
    erase(S, p.rect(160, 312, 942, 1214))
    p.form(p.rect(160, 312, 942, 1214), ('sepia', 'indigo', 'slate'), 0, LIGHT, density=0.6, seed=S.sd())
    erase(S, sheet)
    p.form(sheet, ('white', 'cream', 'ivory', 'paper'), 0, LIGHT, length=(60, 140), density=0.9, seed=S.sd())
    p.hatch(sheet, p.flow(80, 30, 60), ['ivory', 'sand'], (20, 60), (1.0, 1.4), 0.5, 0.4, opacity=0.3, alpha=0.25, seed=S.sd())   # fibres
    bun = p.rect(170, 300, 910, 350)
    erase(S, bun); p.form(bun, ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, length=(40, 90), density=1.6, seed=S.sd()); p.edge(bun, 'sepia', density=0.9, alpha=0.85)
    st = p.blob(820, 1500, 170, 120, 0.05, seed=2)
    erase(S, st); p.form(st, ('slate', 'indigo', 'umber', 'sepia'), p.contour(st, 8), LIGHT, density=1.7, seed=S.sd()); p.edge(st, 'sepia', density=0.9, alpha=0.8)
    well = p.ellipse(820, 1450, 110, 50)
    p.form(well, ('sepia', 'umber', 'indigo'), 0, LIGHT, density=1.9, seed=S.sd())
    p.lift(p.ellipse(790, 1440, 40, 10), 'stone', 0.4)
    for (x, y) in ((260, 1420), (300, 1460)):
        p.line([(x, y), (x + 360, y - 120)], 'sand', 10, 0.85, alpha=0.95)
    p.glow(300, 300, 520, strength=0.5, density=0.5)
    S.save('washi')


def phone(S, x, y, s=1.0):
    p = S.p
    m = p.rect(x - 60 * s, y - 100 * s, x + 60 * s, y + 100 * s)
    erase(S, m); p.form(m, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    sc = p.rect(x - 50 * s, y - 88 * s, x + 50 * s, y + 88 * s)
    return sc


def phone_face(happy):
    """a young woman reading a message on her phone: smiling, or hurt"""
    S = Shot(1104 if happy else 1105); p = S.p
    ARMS = [[(430, 1010), (420, 1130), (500, 1120)], [(650, 1010), (660, 1130), (580, 1120)]]
    coat = ('butter', 'sun', 'apricot', 'amber') if happy else ('powder', 'cornflower', 'denim', 'indigo')
    w = person(S, 540, 720, 160, coat=coat, hair_style='long', plan=True, arms=ARMS)
    wall = np.ones((H, W), np.float32)
    if happy:
        p.hatch(wall, p.flow(2, 4, 500), ['cream', 'butter', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.65, seed=S.sd())
        p.glow(540, 760, 520, strength=0.6, density=0.6)
    else:
        p.hatch(wall, p.flow(2, 4, 500), ['powder', 'lavender', 'stone'], (60, 140), (1.8, 2.5), 1.7, 0.66, alpha=0.7, seed=S.sd())
        p.hatch(wall, p.flow(2, 4, 500), ['slate', 'periwinkle'], (60, 140), (1.8, 2.4), 0.8, 0.6, alpha=0.4, seed=S.sd())
    erase(S, w['mask'])
    person(S, 540, 720, 160, coat=coat, hair_style='long', arms=ARMS, hands=True, smile=happy, eyes_closed=False,
           look=(0.0, 0.5))
    sc = phone(S, 540, 1080, 0.9)
    p.lift(sc, 'butter' if happy else 'powder', 0.8, tooth=0)
    if happy:
        for (x, y) in ((470, 1040), (500, 1090), (470, 1130)):
            p.lift(p.rect(x - 20, y - 14, x + 50, y + 14), 'white', 0.9, tooth=0)
        hm = h.heart_mask(p, 790, 520, 60)
        p.form(hm, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
        hm2 = h.heart_mask(p, 290, 600, 38)
        p.form(hm2, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    else:
        for sgn in (-1, 1):
            ex = 540 + sgn * 54
            p.line([(ex - 20, 690 + (6 if sgn < 0 else 0)), (ex + 20, 690 + (0 if sgn < 0 else 6))], 'umber', 2.6, 0.8, alpha=0.85)
        p.line(curve([(520, 812), (540, 804), (560, 812)], 8), 'brick', 2.4, 0.8, alpha=0.9)
        tear = p.blob(478, 790, 8, 14, 0.05)
        p.lift(tear, 'sky_pale', 0.9, tooth=0); p.edge(tear, 'cornflower', density=0.8, alpha=0.7)
        cm = k.cloud_mask(p, 820, 480, 220, 110, np.random.default_rng(3))
        p.form(cm, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
        for j in range(6):
            x = 740 + j * 30; p.line([(x, 550), (x - 8, 610 + (j % 2) * 26)], 'cornflower', 3, 0.8, alpha=0.85)
    S.save('smile' if happy else 'hurt')


def smile(): phone_face(True)
def hurt(): phone_face(False)


def ink(light):
    """the deep of ink before the world: swirling sumi; light=True -- the light bursting out of it"""
    S = Shot(1106); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.radial(540, 900, 0, 30, 200), list(SUMI), (60, 160), (1.8, 2.8), 2.2, 0.86, seed=S.sd())
    p.hatch(bg, p.flow(30, 40, 300), ['sepia', 'indigo'], (60, 160), (1.8, 2.6), 1.4, 0.84, alpha=0.7, seed=S.sd())
    for (x, y, r) in ((300, 500, 300), (800, 1300, 340), (650, 700, 220)):
        p.lift(blur(p.blob(x, y, r, r * 0.6, 0.3, seed=S.sd()), 40), 'slate', 0.18)
    if light:
        for a in np.linspace(0, 2 * np.pi, 17)[:-1]:
            ray = p.poly([(540, 900), (540 + 1800 * np.cos(a - 0.05), 900 + 1800 * np.sin(a - 0.05)), (540 + 1800 * np.cos(a + 0.05), 900 + 1800 * np.sin(a + 0.05))])
            p.hatch(ray, np.rad2deg(a), ['glow', 'butter', 'cream'], (60, 160), (1.8, 2.4), 1.0, 0.66, opacity=0.6, alpha=0.5, seed=S.sd())
        p.glow(540, 900, 700, strength=1.8, density=1.5)
        p.lift(blur(p.ellipse(540, 900, 260, 260), 60), 'white', 0.9)
        p.lift(blur(p.ellipse(540, 900, 520, 520), 80), 'butter', 0.5)
    S.save('ink_light' if light else 'ink_dark')


def ink_dark(): ink(False)
def ink_light(): ink(True)


def walker():
    """ことばは人となって: a figure walking toward us out of the light"""
    S = Shot(1107); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-3, 4), ['butter', 'cream', 'apricot'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.glow(540, 760, 760, strength=1.6, density=1.3)
    p.lift(blur(p.ellipse(540, 760, 360, 420), 60), 'white', 0.85)
    g = (p.YY > 1250).astype(np.float32)
    p.form(g, ('meadow', 'yellowgreen', 'butter', 'sage'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.1, seed=S.sd())
    p.lift(blur(g * smoothstep(1600, 1250, p.YY), 20), 'cream', 0.55)
    road = p.poly([(500, 1250), (580, 1250), (820, 1920), (260, 1920)])
    p.form(road, ('sand', 'butter', 'cream', 'tan'), p.flow(90, 8), LIGHT, density=1.0, seed=S.sd())
    figure(S, 540, 1330, 520, coat=('cream', 'sand', 'tan', 'sienna'), hair=('umber', 'sepia', 'sepia'), back=True, walk=0.35,
           legs=('tan', 'sienna', 'umber'))
    p.lift(blur(p.ellipse(540, 1000, 170, 330), 30) * 0.5, 'butter', 0.25)
    S.save('walker')


def teach():
    """イエスはたくさんのことばを語りました: on a green hillside a figure in white speaks; people sit listening"""
    S = Shot(1108); p = S.p
    sky(S, 900, (540, 360, 360))
    clouds(S, [(200, 380, 320, 70), (880, 300, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [860, 800, 840, 780, 820, 850, 800], RIDGES[0], mist=0.5)
    hill = p.below([0, 300, 540, 800, 1080], [1010, 960, 930, 960, 1010])
    p.form(hill, ('meadow', 'yellowgreen', 'grass', 'moss'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    p.flowers(hill * (p.YY > 1100), n=120, size=(5, 9))
    figure(S, 540, 1020, 320, coat=('white', 'cream', 'ivory', 'sand'), hair=('hair', 'umber', 'sepia'), back=False, legs=('sand', 'tan', 'sienna'))
    p.form(p.rect(498, 830, 582, 852), ('rose', 'brick', 'sienna'), 0, LIGHT, density=1.4, seed=S.sd())    # sash
    p.glow(540, 880, 260, strength=0.5, density=0.5)
    rr = np.random.default_rng(6)
    coats = [('peach', 'coral', 'terracotta', 'brick'), ('powder', 'cornflower', 'denim', 'indigo'), ('butter', 'ochre', 'amber', 'sienna'),
             ('sage', 'lichen', 'moss', 'pine'), ('lavender', 'periwinkle', 'violet', 'indigo'), ('pink', 'rose', 'coral', 'brick')]
    for j, (x, y, hh) in enumerate(((180, 1330, 230), (390, 1300, 220), (690, 1310, 220), (900, 1340, 230), (290, 1560, 280), (560, 1580, 290), (820, 1560, 280))):
        figure(S, x, y, hh, coat=coats[j % len(coats)], back=True, up=0.3)
    S.save('teach')


def rise():
    """起きなさい: a man up on his feet, arms wide with joy, his sleeping mat rolled at his side; friends watching"""
    S = Shot(1109); p = S.p
    ARMS = [[(430, 1000), (290, 900), (200, 770)], [(650, 1000), (790, 900), (880, 770)]]
    w = person(S, 540, 700, 150, coat=('sand', 'tan', 'sienna', 'brown'), hair_style='short', plan=True, arms=ARMS)
    sky(S, 1200, (540, 420, 460))
    ground(S, 1200, cols=('sand', 'butter', 'tan', 'ochre'), flowers=0)
    for x, c in ((130, ('cream', 'sand', 'tan', 'sienna')), (950, ('cream', 'ivory', 'sand', 'tan'))):
        hs = p.rect(x - 140, 780, x + 140, 1210); erase(S, hs); p.form(hs, c, 90, LIGHT, density=1.4, seed=S.sd()); p.edge(hs, 'sienna', density=0.7, alpha=0.7)
        p.window(x - 50, 900, x + 50, 1000, panes=(1, 1), glow=0.3, seed=S.sd())
    erase(S, w['mask'])
    person(S, 540, 700, 150, coat=('sand', 'tan', 'sienna', 'brown'), hair_style='short', arms=ARMS, smile=True, hair=('hair', 'umber', 'sepia'))
    mat = p.tube([(560, 1330), (900, 1290)], 60, 60)
    erase(S, mat); p.form(mat, ('butter', 'ochre', 'sand', 'sienna'), p.contour(mat, 6, 0), LIGHT, density=1.6, seed=S.sd()); p.edge(mat, 'sienna', density=0.9, alpha=0.85)
    p.glow(540, 600, 420, strength=0.6, density=0.6)
    S.save('rise')


def forgiven():
    """あなたの罪は赦された: a woman who had bowed her head lifts it into warm light, eyes closed, at peace"""
    S = Shot(1110); p = S.p
    ARMS = [[(440, 1010), (420, 1120), (515, 1095)], [(640, 1010), (660, 1120), (565, 1095)]]
    w = person(S, 540, 760, 160, coat=('lavender', 'periwinkle', 'violet', 'indigo'), hair_style='long', plan=True, arms=ARMS)
    bg = np.ones((H, W), np.float32)
    v = p.value(0.0, 1.0, 0, 1920)
    p.hatch(bg, p.flow(-3, 4), ['butter', 'cream', 'apricot'], (60, 150), (1.8, 2.5), 1.5, 0.62, seed=S.sd())
    p.hatch(bg * v, p.flow(-3, 4), ['lavender', 'periwinkle', 'slate'], (60, 150), (1.8, 2.5), 1.4, 0.66, alpha=0.6, seed=S.sd())
    beam = p.poly([(340, 0), (740, 0), (900, 1500), (180, 1500)])
    p.hatch(beam, 90, ['glow', 'butter', 'cream'], (60, 160), (1.8, 2.4), 1.0, 0.6, opacity=0.6, alpha=0.45, seed=S.sd())
    p.glow(540, 200, 500, strength=1.0, density=1.0)
    erase(S, w['mask'])
    person(S, 540, 760, 160, coat=('lavender', 'periwinkle', 'violet', 'indigo'), hair_style='long', arms=ARMS, hands=False, eyes_closed=True, smile=True)
    k.ari.gassho(S, 540, 1090, 0.9)
    p.lift(blur(p.ellipse(540, 700, 180, 160), 20), 'butter', 0.25)
    S.save('forgiven')


def letter():
    """世界をつくったその方が、いま、あなたにも語りかけている: two hands opening a handwritten letter in warm light"""
    S = Shot(1111); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-10, 6), ['apricot', 'butter', 'peach'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.glow(700, 300, 600, strength=1.0, density=1.0)
    pg = p.poly([(200, 420), (880, 400), (900, 1180), (180, 1200)])
    for sgn, (x, y) in ((-1, (175, 860)), (1, (905, 840))):
        sl = p.tube([(x + sgn * 330, y + 900), (x + sgn * 150, y + 420), (x + sgn * 20, y + 110)], 120, 95)
        erase(S, sl); p.form(sl, ('cream', 'ivory', 'sand', 'tan'), p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
        p.edge(sl, 'sienna', density=0.8, alpha=0.7)
        hand(S, x - sgn * 10, y, 1.5, -15 if sgn < 0 else 195, curl=0.2)
    erase(S, pg)
    p.form(pg, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, length=(60, 120), density=1.0, seed=S.sd())
    p.edge(pg, 'tan', density=0.8, alpha=0.7)
    p.line([(190, 800), (890, 790)], 'sand', 2.4, 0.6, alpha=0.6)          # the fold
    rr = np.random.default_rng(7)
    for j in range(11):                                                # handwriting
        y = 500 + j * 58 + (30 if j > 5 else 0)
        x0, x1 = 260, 820 - (rr.uniform(0, 260) if j in (5, 10) else rr.uniform(0, 60))
        xs = np.linspace(x0, x1, 60)
        ys = y + 6 * np.sin(xs / 9 + j) * rr.uniform(0.6, 1.0) + 3 * np.sin(xs / 3.1)
        p.line(np.stack([xs, ys], 1), 'umber', 2.2, 0.7, alpha=0.75)
    hm = h.heart_mask(p, 760, 1110, 26)
    p.form(hm, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    for sgn, (x, y) in ((-1, (175, 860)), (1, (905, 840))):
        th = p.tube([(x + sgn * 20, y + 40), (x - sgn * 40, y - 10), (x - sgn * 80, y - 40)], 24, 19)
        erase(S, th); p.form(th, SKIN4, p.contour(th, 5, 0), LIGHT, density=1.6, warm='butter', seed=S.sd()); p.edge(th, 'sienna', density=0.9, alpha=0.85)
    p.lift(blur(pg, 20) * 0.6, 'butter', 0.15)
    S.save('letter')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
