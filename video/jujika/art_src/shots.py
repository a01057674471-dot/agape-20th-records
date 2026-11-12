"""「十字架の、ほんとうの意味」 paintings -- only empty crosses, the crucifixion seen far off. python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *
from PIL import Image, ImageDraw, ImageFont

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
ROBE = ('white', 'cream', 'ivory', 'sand')
WOOD = ('tan', 'sienna', 'brown', 'umber')
SILVER = ('white', 'sky_pale', 'stone', 'warmgrey')


def cross_shape(p, cx, top, h, w, t):
    return np.clip(p.rect(cx - t / 2, top, cx + t / 2, top + h) + p.rect(cx - w / 2, top + h * 0.26, cx + w / 2, top + h * 0.26 + t), 0, 1)


def pendant(S, cx, cy, s=1.0, cols=SILVER):
    p = S.p
    m = cross_shape(p, cx, cy - 46 * s, 92 * s, 60 * s, 16 * s)
    erase(S, m); p.form(m, cols, 0, LIGHT, density=1.6, seed=S.sd()); p.edge(m, 'slate', width=(1.2, 1.8), density=0.9, alpha=0.8)
    p.lift(p.rect(cx - 7 * s, cy - 40 * s, cx - 2 * s, cy + 30 * s), 'white', 0.8, tooth=0)
    p.form(p.ellipse(cx, cy - 52 * s, 8 * s, 8 * s), cols, 0, LIGHT, density=1.4, seed=S.sd())
    return m


def necklace():
    """その十字架のネックレス: close on the collarbone -- a small silver cross on a fine chain, the coral cardigan, soft light"""
    S = Shot(1401); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(4, 6, 500), ['cream', 'apricot', 'butter'], (60, 150), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.glow(820, 300, 520, strength=0.8, density=0.8)
    hairL = p.poly(curve([(150, 0), (330, 0), (360, 500), (300, 1000), (120, 1100), (60, 600)], 50), smooth=True)
    hairR = p.poly(curve([(930, 0), (750, 0), (720, 500), (780, 1000), (960, 1100), (1020, 600)], 50), smooth=True)
    face = p.ellipse(540, 120, 260, 300) * (p.YY > 0)
    neck = p.rect(430, 300, 650, 900)
    chest = p.poly(curve([(200, 1920), (230, 1000), (420, 780), (540, 760), (660, 780), (850, 1000), (880, 1920)], 60), smooth=True)
    skin = np.clip(face + neck + chest, 0, 1)
    erase(S, skin)
    p.form(skin, SKIN, p.contour(skin, 10), LIGHT, length=(12, 26), density=1.4, warm='peach', seed=S.sd())
    p.line(curve([(470, 330), (540, 350), (610, 330)], 16), 'brick', 3.2, 0.8, alpha=0.9)          # the smile
    p.blush(400, 220, 40, amount=0.6); p.blush(680, 220, 40, amount=0.6)
    for sgn in (-1, 1):                                                                        # collarbones
        p.line(curve([(540 + sgn * 40, 900), (540 + sgn * 160, 870), (540 + sgn * 280, 900)], 20), 'skin_shade', 3, 0.6, alpha=0.6)
    shirt = p.poly([(420, 1920), (450, 1250), (540, 1350), (630, 1250), (660, 1920)])
    for sgn in (-1, 1):
        cg = p.poly([(540 + sgn * 120, 1920), (540 + sgn * 90, 1260), (540 + sgn * 330, 960), (540 + sgn * 560, 1050), (540 + sgn * 560, 1920)])
        erase(S, cg); p.form(cg, COAT, 85, LIGHT, length=(16, 36), density=1.5, warm='butter', seed=S.sd()); p.edge(cg, 'brick', density=0.8, alpha=0.7)
    erase(S, shirt * (1 - (np.abs(p.XX - 540) > 110)))
    p.form(shirt, ('cream', 'ivory', 'sand', 'tan'), 90, LIGHT, density=1.3, seed=S.sd())
    erase(S, np.clip(hairL + hairR, 0, 1))
    p.form(np.clip(hairL + hairR, 0, 1), HAIR, p.flow(85, 10), LIGHT, length=(30, 70), density=1.6, seed=S.sd())
    t = np.linspace(0, 1, 60)
    for sgn in (-1, 1):
        xs = 540 + sgn * (110 * (1 - t) ** 1.3); ys = 600 + 400 * t ** 0.9
        p.line(np.stack([xs, ys], 1), 'warmgrey', 2.2, 0.8, alpha=0.9)
    pendant(S, 540, 1080, 1.3)
    k.ari.pcommon if False else None
    p.glow(560, 1060, 80, strength=0.9, density=0.9)
    p.lift(p.ellipse(530, 1050, 6, 6), 'white', 1.0, tooth=0)
    S.save('necklace')


def shop():
    """おしゃれなアクセサリー: an accessory shop counter -- little stands hung with cross pendants, trays, soft lights"""
    S = Shot(1402); p = S.p
    wall = (p.YY < 1100).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'pink', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.6, alpha=0.65, seed=S.sd())
    for x in (200, 540, 880):
        p.lift(p.ellipse(x, 120, 110, 26), 'butter', 0.5); p.glow(x, 150, 200, strength=0.6, density=0.6)
    mirror = p.ellipse(540, 520, 220, 300)
    p.form(mirror * (1 - p.ellipse(540, 520, 196, 276)), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(540, 520, 196, 276), ('sky_pale', 'powder', 'cream'), 0, LIGHT, density=1.0, seed=S.sd())
    counter = p.rect(0, 1100, 1080, 1920)
    erase(S, counter); p.form(counter, ('cream', 'ivory', 'sand', 'tan'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    p.form(p.rect(0, 1100, 1080, 1140), ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.4, seed=S.sd())
    for (x, hh, col) in ((220, 520, SILVER), (540, 600, ('butter', 'gold', 'amber', 'ochre')), (860, 520, SILVER)):
        stand = np.clip(p.rect(x - 12, 1100 - hh, x + 12, 1110) + p.rect(x - 150, 1100 - hh, x + 150, 1100 - hh + 18), 0, 1)
        erase(S, stand); p.form(stand, ('pink', 'rose', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
        for j, dx in enumerate((-110, 0, 110)):
            top = 1100 - hh + 18; L_ = 160 + 40 * (j % 2)
            p.line([(x + dx - 30, top), (x + dx, top + L_), (x + dx + 30, top)], 'warmgrey', 2.0, 0.7, alpha=0.85)
            pendant(S, x + dx, top + L_ + 34, 0.6, col)
    for (x0, x1) in ((80, 460), (620, 1000)):
        tray = p.rect(x0, 1250, x1, 1420)
        erase(S, tray); p.form(tray, ('slate', 'indigo', 'violet', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
        for j in range(3):
            pendant(S, x0 + 70 + j * 120, 1335, 0.55, SILVER if j % 2 else ('butter', 'gold', 'amber', 'ochre'))
    S.save('shop')


def lone_cross():
    """もともとは死刑の道具: a rough wooden cross alone on a barren hill under a dark, heavy sky -- no one there"""
    S = Shot(1403); p = S.p
    m = (p.YY < 1520).astype(np.float32)
    p.hatch(m, p.flow(-8, 20, 300), ['slate', 'indigo', 'umber', 'stone'], (60, 160), (1.8, 2.8), 2.0, 0.82, seed=S.sd())
    for (x, y, r) in ((250, 300, 260), (800, 500, 300), (500, 900, 240)):
        p.form(p.blob(x, y, r * 1.4, r * 0.5, 0.3, seed=S.sd()), ('slate', 'warmgrey', 'umber', 'sepia'), p.flow(-8, 20), LIGHT, density=1.2, seed=S.sd())
    p.lift(blur(p.rect(0, 1150, 1080, 1260), 30), 'stone', 0.3)
    hill = p.below([0, 300, 540, 780, 1080], [1500, 1330, 1260, 1330, 1500])
    p.form(hill, ('ochre', 'tan', 'sienna', 'umber'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.5, seed=S.sd())
    p.form((p.YY > 1500).astype(np.float32), ('tan', 'sienna', 'umber', 'sepia'), 0, LIGHT, length=(40, 90), density=1.4, seed=S.sd())
    cr = cross_shape(p, 540, 520, 760, 440, 54)
    erase(S, cr); p.form(cr, ('sienna', 'brown', 'umber', 'sepia'), 90, LIGHT, length=(30, 70), density=1.8, seed=S.sd())
    for j in range(6): p.line([(526 + j * 5, 540), (524 + j * 5, 1270)], 'sepia', 1.6, 0.6, alpha=0.5)
    p.edge(cr, 'sepia', width=(2.0, 3.0), density=1.0, alpha=0.9)
    for (x, y) in ((330, 1420), (760, 1440)):
        p.stone(x, y, 50, 26)
    S.save('lone_cross')


def palm_necklace():
    """じゃあ、なぜ: the young woman with the necklace lying in her open palm, looking down at it"""
    S = Shot(1404); p = S.p
    w = person(S, 540, 720, 170, coat=COAT, hair_style='long', plan=True)
    hj.room(S, w['mask'], win_box=(680, 160, 1010, 600))
    erase(S, w['mask'])
    person(S, 540, 720, 170, coat=COAT, hair_style='long', hair=HAIR, smile=False, look=(0.0, 0.7))
    sl = p.tube([(720, 1330), (660, 1240), (610, 1170)], 66, 56)
    erase(S, sl); p.form(sl, COAT, p.contour(sl, 8, 90), LIGHT, density=1.5, warm='butter', seed=S.sd()); p.edge(sl, 'brick', density=0.8, alpha=0.7)
    hm = hand(S, 560, 1080, 1.45, -100, curl=-0.25)
    t = np.linspace(0, 1, 40)
    p.line(np.stack([500 + 120 * t, 1040 + 40 * np.sin(t * np.pi)], 1), 'warmgrey', 2.0, 0.8, alpha=0.9)
    pendant(S, 560, 1090, 0.75)
    p.glow(560, 1080, 70, strength=0.7, density=0.7)
    S.save('palm_necklace')


def bread():
    """病気の人を癒し、仲間はずれの人と一緒にごはんを: a man in a simple robe sharing bread with poor and lonely people
    sitting round a cloth, warm evening light; he is seen from behind"""
    S = Shot(1405); p = S.p
    sky(S, 900, (800, 600, 400))
    p.hatch((p.YY < 900).astype(np.float32), p.flow(-3, 4), ['peach', 'apricot', 'rose'], (60, 140), (1.8, 2.4), 0.9, 0.62, alpha=0.45, seed=S.sd())
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [860, 820, 840, 800, 830, 850, 820], ('sand', 'ochre', 'tan', 'sienna'), mist=0.4)
    ground(S, 900, cols=('butter', 'sand', 'ochre', 'tan'), flowers=0)
    guests = [(200, 900, 80, ('stone', 'warmgrey', 'slate', 'umber'), 'short', True), (380, 860, 80, ('sand', 'tan', 'sienna', 'brown'), 'long', False),
              (700, 860, 80, ('sage', 'lichen', 'moss', 'pine'), 'bun', False), (880, 900, 80, ('stone', 'pebble', 'warmgrey', 'umber'), 'short', False)]
    for (x, y, R, c, hs, grey) in guests:
        g = person(S, x, y, R, coat=c, hair_style=hs, plan=True)
        erase(S, g['mask'])
        person(S, x, y, R, coat=c, hair_style=hs, grey=grey, smile=True, eyes_closed=(x == 380), look=(0.0, 0.3))
    cloth = p.ellipse(540, 1260, 430, 120)
    erase(S, cloth); p.form(cloth, ('cream', 'ivory', 'sand', 'tan'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(cloth, 'tan', density=0.7, alpha=0.7)
    for (x, y) in ((380, 1230), (560, 1210), (720, 1250), (470, 1290)):
        b = p.blob(x, y, 62, 34, 0.1, seed=S.sd())
        p.form(b, ('butter', 'ochre', 'amber', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(b, 'sienna', density=0.8, alpha=0.7)
    jar = p.poly(curve([(800, 1260), (790, 1160), (820, 1120), (860, 1160), (850, 1260)], 30))
    p.form(jar, ('terracotta', 'brick', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
    # the man in the robe, from behind, holding a loaf out to them
    x = 540; R = 120; hy = 1500
    head = p.ellipse(x, hy, R * 0.92, R)
    body = p.poly(curve([(x - R * 0.5, hy + R * 0.85), (x - R * 1.4, hy + R * 1.6), (x - R * 1.7, 1960), (x + R * 1.7, 1960),
                         (x + R * 1.4, hy + R * 1.6), (x + R * 0.5, hy + R * 0.85)], 50), smooth=True)
    arm = p.tube([(x + R * 1.0, hy + R * 1.6), (x + R * 1.5, hy + R * 0.9), (x + R * 1.3, hy - R * 0.1)], R * 0.36, R * 0.3)
    allm = np.clip(head + body + arm, 0, 1)
    erase(S, allm)
    p.form(np.clip(body + arm, 0, 1), ROBE, 85, LIGHT, length=(16, 36), density=1.4, warm='butter', seed=S.sd())
    p.form(p.rect(x - R * 0.4, hy + R * 0.9, x + R * 0.4, 1960) * body, ('sienna', 'brick', 'rose'), 90, LIGHT, density=0.6, seed=S.sd())
    p.form(head, ('hair', 'umber', 'sepia'), p.radial(x, hy - R, 90), LIGHT, density=1.6, seed=S.sd())
    p.edge(allm, 'sepia', density=0.8, alpha=0.7)
    lb = p.blob(x + R * 1.3, hy - R * 0.25, 60, 34, 0.1, seed=3)
    p.form(lb, ('butter', 'ochre', 'amber', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
    p.glow(560, 1100, 520, strength=0.6, density=0.6)
    S.save('bread')


def three_crosses():
    """十字架にかけられました: far off, three crosses on a hill at dusk -- silhouettes only, quiet"""
    S = Shot(1406); p = S.p
    m = (p.YY < 1200).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ('dusk_sky', np.clip(p.value(0.0, 1.0, 0, 1200) * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.8, 0.76, seed=S.sd())
    p.hatch(m * smoothstep(500, 1200, p.YY), p.flow(-3, 4), ['lavender', 'mauve', 'rose'], (60, 140), (1.8, 2.4), 1.0, 0.66, alpha=0.5, seed=S.sd())
    p.glow(540, 1150, 420, strength=0.5, density=0.5)
    hill = p.below([0, 300, 540, 780, 1080], [1200, 1110, 1070, 1110, 1200])
    p.form(hill, ('slate', 'violet', 'indigo', 'sepia'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.6, seed=S.sd())
    for (x, hh) in ((440, 150), (540, 190), (640, 150)):
        cr = cross_shape(p, x, 1080 - hh, hh, hh * 0.55, 12)
        p.form(cr, ('sepia', 'umber', 'indigo'), 90, LIGHT, density=1.8, seed=S.sd())
    p.form((p.YY > 1200).astype(np.float32), ('indigo', 'slate', 'sepia', 'umber'), 0, LIGHT, length=(40, 90), density=1.5, seed=S.sd())
    for (x, y) in ((420, 520), (450, 545), (480, 515)):
        p.line(curve([(x - 16, y), (x - 6, y - 8), (x, y - 2), (x + 6, y - 8), (x + 16, y)], 12), 'sepia', 2.2, 0.8, alpha=0.7)
    S.save('three_crosses')


def burden_scene(lifted):
    """身代わり: someone kneeling under a heavy sack; a gentle man in a robe lifts it from them (lifted=True: it is on
    his shoulder now and they look up, lighter)"""
    S = Shot(1407 if not lifted else 1408); p = S.p
    sky(S, 1150, (800, 500, 420))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1080, 1030, 1060, 1010, 1040, 1070, 1030], RIDGES[0], mist=0.5)
    ground(S, 1150, cols=('butter', 'sand', 'yellowgreen', 'meadow'), flowers=60)
    jx, jy, JR = 720, 720, 125
    jm = person(S, jx, jy, JR, coat=ROBE, hair_style='long', plan=True,
                arms=[[(jx - 100, jy + 230), (jx - 190, jy + 280), (jx - 260, jy + 290)]] if not lifted else None)
    erase(S, jm['mask'])
    person(S, jx, jy, JR, coat=ROBE, hair_style='long', hair=('hair', 'umber', 'sepia'), eyes_closed=True, smile=True,
           arms=[[(jx - 100, jy + 230), (jx - 190, jy + 280), (jx - 260, jy + 290)]] if not lifted else None)
    px, py, PR = 360, (1100 if not lifted else 980), 105
    pm = person(S, px, py, PR, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='short', plan=True)
    if not lifted:
        sack = p.blob(400, 1110, 250, 170, 0.1, seed=6, rot=-8)
        erase(S, sack)
        p.form(sack, ('sand', 'tan', 'sienna', 'brown'), p.contour(sack, 10, 30), LIGHT, length=(16, 36), density=1.6, seed=S.sd())
        p.edge(sack, 'sepia', width=(1.8, 2.6), density=0.9, alpha=0.85)
        for j in range(4): p.line([(300 + j * 70, 990), (320 + j * 70, 1200)], 'sienna', 2.4, 0.7, alpha=0.6)
    erase(S, pm['mask'])
    person(S, px, py, PR, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='short', hair=('hair', 'umber', 'sepia'),
           smile=lifted, eyes_closed=not lifted, look=(0.3, -0.5) if lifted else (0, 0))
    if lifted:
        sack = p.blob(jx + 190, jy + 150, 160, 110, 0.1, seed=6, rot=20)
        erase(S, sack)
        p.form(sack, ('sand', 'tan', 'sienna', 'brown'), p.contour(sack, 10, 30), LIGHT, length=(16, 36), density=1.6, seed=S.sd())
        p.edge(sack, 'sepia', width=(1.8, 2.6), density=0.9, alpha=0.85)
        for j in range(3): p.line([(jx + 110 + j * 70, jy + 70), (jx + 130 + j * 70, jy + 230)], 'sienna', 2.4, 0.7, alpha=0.6)
    if lifted:
        p.glow(px, py, 260, strength=0.7, density=0.7)
    p.glow(800, 500, 300, strength=0.5, density=0.5)
    S.save('lifted' if lifted else 'burden')


def burden(): burden_scene(False)
def lifted(): burden_scene(True)


def empty_cross():
    """イエスの姿がありません: a plain empty wooden cross on a church wall in golden morning light, pews below"""
    S = Shot(1409); p = S.p
    wall = (p.YY < 1500).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'ivory', 'sand'], (60, 140), (1.8, 2.5), 1.6, 0.6, alpha=0.65, seed=S.sd())
    beam = p.poly([(0, 150), (240, 80), (900, 1300), (520, 1400)])
    p.hatch(beam, 55, ['glow', 'butter', 'cream'], (60, 160), (1.8, 2.4), 1.0, 0.62, opacity=0.6, alpha=0.4, seed=S.sd())
    p.glow(540, 760, 520, strength=0.9, density=0.9)
    cr = cross_shape(p, 540, 330, 860, 460, 70)
    p.form(blur(cr, 14) * 0.0 + np.clip(blur(cr, 24) - cr, 0, 1) * 0.7, ('tan', 'sienna', 'sienna'), 0, LIGHT, density=0.6, seed=S.sd())
    erase(S, cr); p.form(cr, ('butter', 'ochre', 'tan', 'sienna'), 90, LIGHT, length=(30, 70), density=1.7, seed=S.sd())
    p.edge(cr, 'sienna', width=(1.8, 2.6), density=0.9, alpha=0.85)
    p.lift(p.rect(512, 340, 528, 1180), 'butter', 0.5)
    floor = (p.YY >= 1500).astype(np.float32)
    p.form(floor, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    for y in (1520, 1680):
        pew = p.rect(60, y, 1020, y + 70)
        erase(S, pew); p.form(pew, ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(pew, 'sepia', density=0.8, alpha=0.8)
    p.flowers(p.blob(180, 1450, 90, 50), kinds=('daisy', 'poppy'), n=12, size=(9, 13))
    S.save('empty_cross')


def street():
    """今度、十字架を見かけたら: the young woman on a city street at sunset, looking up at a small church cross"""
    S = Shot(1410); p = S.p
    m = (p.YY < 1300).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ('dusk_sky', np.clip(p.value(0.0, 1.0, 0, 1300) * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.7, 0.74, seed=S.sd())
    p.hatch(m * smoothstep(400, 1300, p.YY), p.flow(-3, 4), ['peach', 'apricot', 'butter'], (60, 140), (1.8, 2.4), 1.0, 0.64, alpha=0.55, seed=S.sd())
    p.glow(700, 1000, 520, strength=0.9, density=0.9)
    for (x0, x1, top, c) in ((0, 300, 520, ('peach', 'apricot', 'terracotta', 'brick')), (780, 1080, 560, ('cream', 'sand', 'tan', 'sienna'))):
        b = p.rect(x0, top, x1, 1500)
        erase(S, b); p.form(b, c, 90, LIGHT, length=(30, 70), density=1.4, seed=S.sd()); p.edge(b, 'sepia', density=0.7, alpha=0.7)
        for yy in range(top + 80, 1400, 180):
            for xx in range(x0 + 50, x1 - 60, 110):
                p.window(xx, yy, xx + 60, yy + 90, panes=(1, 2), glow=0.7, seed=S.sd())
    ch = np.clip(p.rect(400, 860, 680, 1500) + p.poly([(380, 870), (540, 740), (700, 870)]) + p.rect(500, 560, 580, 880) + p.poly([(486, 570), (540, 450), (594, 570)]), 0, 1)
    erase(S, ch); p.form(ch, ('cream', 'ivory', 'sand', 'tan'), 90, LIGHT, density=1.3, seed=S.sd()); p.edge(ch, 'sepia', density=0.8, alpha=0.8)
    cr = cross_shape(p, 540, 330, 120, 70, 14)
    p.form(cr, ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.7, seed=S.sd())
    p.glow(540, 380, 100, strength=0.8, density=0.8)
    p.window(500, 960, 580, 1100, panes=(1, 2), glow=0.9, seed=S.sd())
    road = (p.YY >= 1500).astype(np.float32)
    p.form(road, ('stone', 'warmgrey', 'sand', 'umber'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    figure(S, 640, 1820, 560, coat=COAT, hair=HAIR, back=True, up=1.0, legs=('cornflower', 'denim', 'indigo'))
    S.save('street')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
