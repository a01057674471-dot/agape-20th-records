"""「はじめまして」 paintings: サンヒ (Sanghee) in the warm coloured-pencil storybook style. python3 shots.py NAME"""
import sys
from hcommon import *
import importlib.util
_spec = importlib.util.spec_from_file_location('r1', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'arigatou', 'art_src', 'shots.py'))
r1 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(r1)
room, gassho = r1.room, r1.gassho

SANGHEE = ('peach', 'coral', 'terracotta', 'brick')         # her coral cardigan
HAIR = ('hair', 'umber', 'sepia')


def hello():
    """サンヒ at her desk, waving, a notebook and a cup of tea, the window behind her"""
    S = Shot(501); p = S.p
    desk = p.rect(0, 1400, 1080, 1920)
    ARMS = [[(400, 1150), (330, 1000), (300, 780)], [(680, 1150), (700, 1300), (600, 1380)]]
    m = person(S, 540, 900, 175, coat=SANGHEE, hair_style='long', plan=True, arms=ARMS, cut=desk)
    room(S, np.clip(m['mask'] + desk, 0, 1), win_box=(620, 160, 1000, 700))
    person(S, 540, 900, 175, coat=SANGHEE, hair_style='long', hair=HAIR, arms=ARMS, cut=desk, smile=True, look=(0, 0.1))
    p.form(desk, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', avoid=m['mask'], seed=S.sd())
    p.line([(0, 1402), (1080, 1402)], 'sienna', 5, 0.8, alpha=0.8)
    nb = p.poly([(160, 1500), (520, 1470), (540, 1700), (180, 1730)])
    p.form(nb, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.3, seed=S.sd())
    for k in range(6):
        p.line([(200, 1530 + k * 30), (500, 1505 + k * 30)], 'pebble', 2.2, 0.6, alpha=0.6)
    cup = p.poly(curve([(760, 1480), (770, 1600), (850, 1630), (930, 1600), (940, 1480)], 30))
    p.form(np.clip(cup + p.ellipse(850, 1480, 90, 26), 0, 1), ('cream', 'powder', 'cornflower'), 90, LIGHT, density=1.4, seed=S.sd())
    p.form(p.ellipse(850, 1480, 76, 18), ('apricot', 'ochre', 'amber'), 0, LIGHT, density=1.3, seed=S.sd())
    p.strokes([curve([(830, 1450), (815, 1380), (840, 1320)], 20), curve([(870, 1450), (885, 1380), (860, 1310)], 20)],
              'white', width=6.0, pressure=0.55, opacity=0.8, alpha=0.5)
    p.flowers(p.blob(160, 1440, 60, 30), kinds=('daisy', 'pink'), n=8, size=(8, 12))
    S.save('hello')


def young():
    """twenty years ago: a young student with a suitcase and a backpack under the cherry blossoms of a Japanese street"""
    S = Shot(502); p = S.p
    sky = (p.YY < 1000).astype(np.float32)
    morning_sky(S, sky)
    clouds(S, [(260, 260, 380, 90), (850, 380, 300, 70)])
    for (x, y, w, h, wall, roof) in ((40, 1180, 260, 300, ('cream', 'ivory', 'sand', 'tan'), ('slate', 'indigo', 'umber', 'sepia')),
                                     (760, 1160, 300, 320, ('cream', 'apricot', 'peach', 'tan'), ('slate', 'indigo', 'umber', 'sepia'))):
        p.cottage(x, y, w, h, wall, roof, light=LIGHT, glow=0.0, seed=S.sd())
    road = (p.YY >= 1180).astype(np.float32)
    p.form(road, ('ivory', 'stone', 'warmgrey', 'pebble'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    for (x, y, h, r) in ((170, 1180, 520, 230), (920, 1150, 560, 250)):
        p.tree(x, y, h, r, ('white', 'pink', 'rose', 'mauve'), trunk=('tan', 'brown', 'umber'), clumps=10, leaf=(7, 13), light=LIGHT, seed=S.sd())
    ARMS = [[(470, 1290), (430, 1420), (400, 1520)], [(610, 1290), (630, 1420), (620, 1500)]]
    person(S, 540, 1130, 120, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='long', hair=HAIR, arms=ARMS, smile=True, look=(-0.2, -0.3))
    bp = p.ellipse(640, 1250, 60, 90)
    suit = p.rect(300, 1500, 420, 1700)
    p.form(suit, ('lemon', 'butter', 'sun', 'amber'), 90, LIGHT, density=1.5, seed=S.sd())
    p.line(curve([(320, 1500), (360, 1450), (400, 1500)], 10), 'umber', 6, 0.8, alpha=0.9)
    for (x, y) in ((330, 1710), (390, 1710)): p.form(p.ellipse(x, y, 14, 14), ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.3, seed=S.sd())
    for i in range(140):                                  # petals in the air and on the road
        x, y = S.r.uniform(0, 1080), S.r.uniform(200, 1900)
        p.strokes([[(x, y), (x + 8, y + 4)]], ['pink', 'white', 'rose'], width=6, pressure=0.7, opacity=0.6, alpha=0.8)
    S.save('young')


def help_():
    """the kind landlady at her door handing the young student an onigiri wrapped in a cloth"""
    S = Shot(503); p = S.p
    LA = [[(300, 1150), (380, 1250), (520, 1250)]]
    SA = [[(780, 1180), (700, 1260), (580, 1270)]]
    a = person(S, 270, 900, 150, coat=('sage', 'moss', 'olive', 'forest'), hair_style='bun', grey=True, plan=True, arms=LA)
    s = person(S, 820, 960, 130, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='long', plan=True, arms=SA)
    fg = np.clip(a['mask'] + s['mask'], 0, 1)
    wall = (p.YY < 1500).astype(np.float32)
    p.hatch(wall, p.flow(80, 4), ('cream', 'sand', 'apricot'), (60, 140), (1.8, 2.5), 1.6, 0.66, avoid=fg, seed=S.sd())
    door = p.rect(60, 300, 520, 1500) * (1 - fg)
    p.form(door, ('sand', 'tan', 'sienna', 'brown'), 90, LIGHT, density=1.5, seed=S.sd())
    for x in range(90, 520, 70): p.line([(x, 300), (x, 1500)], 'sienna', 3, 0.6, alpha=0.6)
    p.window(660, 360, 980, 700, panes=(2, 2), glow=0.4)
    p.form((p.YY >= 1500).astype(np.float32), ('ivory', 'stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.4, seed=S.sd())
    person(S, 270, 900, 150, coat=('sage', 'moss', 'olive', 'forest'), hair_style='bun', grey=True, arms=LA, smile=True, look=(0.6, 0.1), hair=HAIR)
    apron = p.poly([(190, 1080), (350, 1080), (380, 1400), (160, 1400)])
    p.form(apron, ('cream', 'ivory', 'sand'), 90, LIGHT, density=1.3, seed=S.sd())
    person(S, 820, 960, 130, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='long', arms=SA, smile=True, look=(-0.6, 0.2), hair=HAIR)
    cloth = p.blob(550, 1250, 100, 70, 0.1)
    p.form(cloth, ('pink', 'coral', 'red'), 0, LIGHT, density=1.5, seed=S.sd())
    oni = p.poly([(490, 1240), (550, 1130), (610, 1240)], smooth=True)
    p.form(oni, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.rect(515, 1195, 585, 1240), ('indigo', 'slate', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())      # nori
    p.glow(560, 1200, 200, strength=0.6, density=0.7)
    S.save('help')


def now():
    """now: サンヒ at home holding her little one, her desk behind with a map of Japan and a laptop"""
    S = Shot(504); p = S.p
    ARMS = [[(420, 1100), (430, 1250), (560, 1270)], [(660, 1100), (680, 1220), (600, 1150)]]
    m = person(S, 520, 820, 165, coat=SANGHEE, hair_style='long', plan=True, arms=ARMS)
    kid = person(S, 640, 1100, 85, coat=('lemon', 'butter', 'sun', 'amber'), hair_style='short', plan=True)
    fg = np.clip(m['mask'] + kid['mask'], 0, 1)
    room(S, fg, win_box=(80, 160, 400, 620), wall_to=1450)
    mapm = p.rect(700, 220, 1000, 560) * (1 - fg)
    p.form(mapm, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.2, seed=S.sd())
    # a little map of Japan pinned on the wall (rough real coastlines, north up)
    Pm = lambda lon, lat: (705 + (lon - 128.5) * 17.0, 555 - (lat - 30.8) * 21.0)
    HON = [(130.9, 34.0), (132.8, 35.3), (135.2, 35.7), (136.7, 36.8), (138.3, 37.2), (139.8, 39.0), (139.9, 40.6), (141.4, 41.4),
           (141.9, 39.5), (141.0, 37.8), (140.6, 35.7), (139.2, 35.2), (137.3, 34.6), (135.8, 33.5), (135.3, 34.5), (132.4, 34.2)]
    KYU = [(129.7, 33.3), (131.0, 33.95), (131.9, 32.6), (130.7, 31.0), (130.1, 32.1)]
    SHI = [(132.4, 33.6), (134.1, 34.35), (134.7, 34.0), (133.0, 32.8)]
    HOK = [(140.0, 41.5), (139.8, 42.8), (141.7, 44.3), (141.9, 45.4), (145.3, 44.3), (143.3, 42.0), (141.0, 41.7)]
    jp = np.clip(sum(p.poly([Pm(*q) for q in isl], smooth=True) for isl in (HON, KYU, SHI, HOK)), 0, 1) * (1 - fg)
    p.form(jp, ('yellowgreen', 'meadow', 'grass'), 0, LIGHT, density=1.5, seed=S.sd())
    p.edge(jp, 'olive', density=0.8)
    p.dots(p.ellipse(*Pm(135.5, 34.7), 8, 8) * (1 - fg), ('red',), n=4, size=(5, 7))           # Osaka
    p.form(p.ellipse(850, 225, 12, 12), ('coral', 'red', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())    # the pin
    p.form((p.YY >= 1450).astype(np.float32), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, density=1.4, seed=S.sd())
    lap = p.poly([(740, 1300), (1000, 1300), (1040, 1450), (700, 1450)]) * (1 - fg)
    p.form(lap, ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.3, seed=S.sd())
    person(S, 520, 820, 165, coat=SANGHEE, hair_style='long', hair=HAIR, arms=ARMS, hands=False, smile=True, look=(0.4, 0.4))
    person(S, 640, 1100, 85, coat=('lemon', 'butter', 'sun', 'amber'), hair_style='short', hair=HAIR, smile=True, look=(-0.3, -0.4))
    p.form(p.ellipse(560, 1270, 30, 26), SKIN, 0, LIGHT, density=1.4, seed=S.sd())
    p.glow(560, 1000, 300, strength=0.5, density=0.6)
    S.save('now')


def osaka():
    """studying theology in Osaka: books and a notebook on a desk by the window, the old tower on the skyline"""
    S = Shot(505); p = S.p
    win = p.rect(100, 140, 980, 1000)
    sky = win * (p.YY < 1000)
    morning_sky(S, sky)
    city = np.zeros((H, W), np.float32)
    rr_ = np.random.default_rng(3); x = 100
    while x < 980:
        w = rr_.uniform(60, 120); top = rr_.uniform(760, 900)
        city = np.maximum(city, p.rect(x, top, x + w, 1000)); x += w
    tower = np.clip(p.poly([(520, 900), (580, 900), (566, 520), (534, 520)]) + p.rect(500, 470, 600, 520) + p.poly([(530, 470), (570, 470), (550, 380)]), 0, 1)
    city = np.maximum(city, tower) * win
    p.form(city, ('lavender', 'periwinkle', 'slate', 'indigo'), 90, LIGHT, density=1.4, warm='peach', seed=S.sd())
    p.dots(city * (p.YY > 800), ('butter', 'cream'), n=60, size=(3, 5))
    frame = (1 - win).astype(np.float32) * (p.YY < 1100)
    p.form(frame, ('cream', 'sand', 'tan'), 90, LIGHT, density=1.4, seed=S.sd())
    p.line([(540, 140), (540, 1000)], 'tan', 10, 0.8, alpha=0.9)
    desk = (p.YY >= 1100).astype(np.float32)
    p.form(desk, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', seed=S.sd())
    stack = [(('cornflower', 'slate', 'indigo'), 1160), (('coral', 'red', 'brick'), 1220), (('sage', 'moss', 'forest'), 1280), (('butter', 'gold', 'amber'), 1340)]
    for (c, y) in stack:
        bk = p.rect(140, y, 520, y + 60)
        p.form(bk, c, 0, LIGHT, density=1.5, seed=S.sd())
        p.form(p.rect(500, y + 6, 520, y + 54), ('cream', 'ivory', 'sand'), 90, LIGHT, density=1.2, seed=S.sd())
    L_ = p.poly([(580, 1300), (800, 1270), (820, 1560), (600, 1590)])
    R_ = p.poly([(820, 1270), (1020, 1300), (1000, 1590), (820, 1560)])
    for m in (L_, R_):
        p.lift(m, 'white', 0.8)
        p.hatch(m, 90, ('white', 'cream', 'ivory'), (20, 50), (1.6, 2.2), 1.3, 0.7, opacity=0.8, alpha=0.7, seed=S.sd())
    for k in range(8):
        p.line([(610, 1330 + k * 28), (790, 1305 + k * 28)], 'pebble', 2.2, 0.6, alpha=0.7)
        p.line([(840, 1305 + k * 28), (990, 1330 + k * 28)], 'pebble', 2.2, 0.6, alpha=0.7)
    p.line(curve([(860, 1600), (980, 1450)], 10), 'umber', 7, 0.85, alpha=0.95)      # a pencil
    p.glow(540, 600, 360, strength=0.7, density=0.8, clip=win)
    S.save('osaka')


def tea():
    """sharing: サンヒ and a Japanese friend at a small table with tea, an open Bible between them, both smiling"""
    S = Shot(506); p = S.p
    table = p.rect(0, 1300, 1080, 1920)
    SA = [[(300, 1080), (330, 1230), (420, 1300)]]
    FA = [[(780, 1080), (750, 1230), (660, 1300)]]
    s = person(S, 280, 830, 140, coat=SANGHEE, hair_style='long', plan=True, arms=SA, cut=table)
    f = person(S, 800, 830, 140, coat=('lavender', 'mauve', 'violet', 'indigo'), hair_style='bob', plan=True, arms=FA, cut=table)
    fg = np.clip(s['mask'] + f['mask'], 0, 1)
    room(S, np.clip(fg + table, 0, 1), win_box=(380, 150, 700, 600), wall_to=1300)
    person(S, 280, 830, 140, coat=SANGHEE, hair_style='long', hair=HAIR, arms=SA, cut=table, smile=True, look=(0.6, 0.3))
    person(S, 800, 830, 140, coat=('lavender', 'mauve', 'violet', 'indigo'), hair_style='bob', hair=HAIR, arms=FA, cut=table, smile=True, look=(-0.6, 0.3))
    p.form(table, ('cream', 'sand', 'tan', 'sienna'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', avoid=fg, seed=S.sd())
    p.line([(0, 1302), (1080, 1302)], 'tan', 5, 0.8, alpha=0.8)
    L_ = p.poly(curve([(330, 1420), (450, 1390), (535, 1410), (535, 1640), (450, 1620), (320, 1650)], 40), smooth=True)
    R_ = p.poly(curve([(545, 1410), (630, 1390), (750, 1420), (760, 1650), (630, 1620), (545, 1640)], 40), smooth=True)
    for m in (L_, R_):
        p.lift(m, 'white', 0.85)
        p.hatch(m, 90, ('white', 'cream', 'ivory'), (20, 50), (1.6, 2.2), 1.3, 0.7, opacity=0.85, alpha=0.75, seed=S.sd())
    for k in range(7):
        p.line([(350, 1440 + k * 26), (520, 1430 + k * 26)], 'pebble', 2.0, 0.6, alpha=0.7)
        p.line([(560, 1430 + k * 26), (735, 1440 + k * 26)], 'pebble', 2.0, 0.6, alpha=0.7)
    p.line(curve([(548, 1410), (556, 1680)], 10), 'red', 6, 0.85, alpha=0.95)
    for (x, c) in ((170, ('cream', 'powder', 'cornflower')), (910, ('cream', 'peach', 'apricot'))):
        cupm = np.clip(p.poly(curve([(x - 70, 1420), (x - 62, 1520), (x, 1545), (x + 62, 1520), (x + 70, 1420)], 30)) + p.ellipse(x, 1420, 70, 20), 0, 1)
        p.form(cupm, c, 90, LIGHT, density=1.4, seed=S.sd())
        p.form(p.ellipse(x, 1420, 58, 14), ('yellowgreen', 'sage', 'moss'), 0, LIGHT, density=1.3, seed=S.sd())   # green tea
        p.strokes([curve([(x - 10, 1395), (x - 25, 1330), (x, 1270)], 20)], 'white', width=6.0, pressure=0.55, opacity=0.8, alpha=0.5)
    p.glow(540, 1450, 280, strength=0.6, density=0.7)
    S.save('tea')


if __name__ == '__main__':
    n = sys.argv[1]
    globals()['help_' if n == 'help' else n]()
