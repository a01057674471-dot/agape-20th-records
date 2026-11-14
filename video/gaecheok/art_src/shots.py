"""봉담 개척 이야기 (둘·셋·넷) -- 27 warm coloured-pencil scenes at 16:9. python3 shots.py NAME"""
import sys
from wide import *


def rooftop():
    """첫 예배 후 옥상의 삼겹살: twelve people round a grill on the shop-building roof at dusk, the bell tower with its cross"""
    S = Shot(2001); p = S.p
    sky(S, 760, (1500, 600, 380), dusk=True)
    roof = p.rect(0, 700, W, H)
    erase(S, roof); p.form(roof, ('stone', 'warmgrey', 'sand', 'pebble'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    p.form(p.rect(0, 690, W, 730), ('sand', 'tan', 'warmgrey'), 0, LIGHT, density=1.4, seed=S.sd())
    tower_cross(S, 1650, 300, 1.2)
    for x0, w_ in ((60, 260), (380, 200)):
        building(S, x0, x0 + w_, 520, 700, cols=('lavender', 'stone', 'slate', 'indigo'), floors=2, lit=0.7)
    p.glow(960, 820, 520, strength=0.6, density=0.6)
    seats = [(600, 640, 0), (720, 610, 1), (840, 600, 2), (960, 595, 3), (1080, 600, 4), (1200, 610, 5), (1320, 640, 6)]
    for (x, y, c) in seats:
        bust(S, x, y, 62, COATS[c], hs=['short', 'long', 'bun', 'short', 'long', 'short', 'bob'][c], smile=True, look=(0, 0.3))
    table = p.rect(520, 780, 1400, 840)
    erase(S, table); p.form(table, WOODC, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(table, 'sepia', density=0.8, alpha=0.8)
    grill = p.ellipse(960, 770, 170, 40)
    erase(S, grill); p.form(grill, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    for j in range(6):
        p.form(p.rect(840 + j * 42, 755, 872 + j * 42, 772), ('rose', 'coral', 'apricot'), 0, LIGHT, density=1.4, seed=S.sd())
    for q in range(3):
        p.line(curve([(900 + q * 60, 740), (880 + q * 60, 680), (910 + q * 60, 620)], 20), 'cream', 5, 0.6, alpha=0.6)
    for x in (300, 1600):
        for k_ in range(6): p.lift(p.ellipse(x + k_ * 30 - 75, 560 + 20 * np.sin(k_), 6, 6), 'butter', 0.9, tooth=0)
    S.save('rooftop')


def leaving():
    """주일 해질녘: the members walking home with their bags along the road; one figure stays at the lit 3rd-floor window"""
    S = Shot(2002); p = S.p
    sky(S, 840, (300, 520, 300), dusk=True)
    b = building(S, 1180, 1760, 200, 820, cols=('cream', 'sand', 'tan', 'sienna'), floors=3, lit=0.2)
    tower_cross(S, 1470, 30, 0.9, glow=False)
    p.window(1300, 260, 1480, 380, panes=(2, 1), glow=0.95, seed=S.sd())
    p.form(p.ellipse(1390, 300, 18, 20), ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(p.rect(1372, 318, 1408, 380), ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    ground(S, 820, cols=('sand', 'butter', 'tan', 'ochre'), flowers=0)
    road = p.poly([(0, 900), (1200, 840), (1200, 900), (0, 1000)])
    p.form(road, ('stone', 'warmgrey', 'sand', 'pebble'), 0, LIGHT, density=1.2, seed=S.sd())
    for j, (x, hh) in enumerate(((200, 260), (320, 250), (470, 240), (620, 230), (760, 220))):
        figure(S, x, 900 + (5 - j) * 8, hh, coat=COATS[j], back=True, walk=0.4)
        p.form(p.rect(x - 22, 900 - hh * 0.75, x + 22, 900 - hh * 0.5), ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('leaving')


def empty_sanct():
    """텅 빈 본당: the empty shop-floor sanctuary at night, rows of folding chairs, the pastor and his wife alone at the front"""
    S = Shot(2003); p = S.p
    wall(S, 760, cols=('stone', 'lavender', 'cream'))
    p.form(p.rect(860, 160, 1060, 500), WOODC, 90, LIGHT, density=1.4, seed=S.sd())
    cr = np.clip(p.rect(945, 200, 975, 460) + p.rect(900, 260, 1020, 285), 0, 1)
    p.form(cr, ('butter', 'gold', 'amber'), 0, LIGHT, density=1.6, seed=S.sd())
    floor(S, 760, cols=('stone', 'warmgrey', 'slate', 'umber'))
    pulpit = p.poly([(880, 760), (1040, 760), (1020, 600), (900, 600)])
    erase(S, pulpit); p.form(pulpit, WOODC, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(pulpit, 'sepia', density=0.8, alpha=0.8)
    for r in range(3):
        for c in range(9):
            x = 260 + c * 170 + (r % 2) * 20; y = 800 + r * 90
            ch = np.clip(p.rect(x - 40, y - 60, x + 40, y) + p.rect(x - 45, y, x + 45, y + 14), 0, 1)
            p.form(ch, ('slate', 'indigo', 'stone'), 0, LIGHT, density=1.3, seed=S.sd())
    bust(S, 700, 560, 60, PASTOR, hs='short', eyes_closed=True, smile=False)
    bust(S, 560, 580, 56, WIFE, hs='long', eyes_closed=True, smile=False)
    p.glow(960, 330, 300, strength=0.5, density=0.5)
    S.save('empty_sanct')


def fellowship():
    """지금의 교제: a sunny park -- meat on the grill, a ping-pong table, people laughing together"""
    S = Shot(2004); p = S.p
    sky(S, 560, (300, 200, 300))
    clouds(S, [(500, 180, 300, 70), (1500, 140, 260, 60)])
    xs = np.linspace(0, W, 9)
    ridge(S, xs, [520, 460, 500, 440, 480, 520, 470, 500, 530], RIDGES[2], mist=0.4)
    ground(S, 560, flowers=120)
    tt = p.poly([(1150, 640), (1700, 640), (1760, 720), (1090, 720)])
    erase(S, tt); p.form(tt, ('teal', 'pine', 'forest', 'indigo'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(tt, 'cream', density=0.9, alpha=0.9)
    p.line([(1425, 640), (1425, 720)], 'cream', 4, 0.8, alpha=0.9)
    for x in (1120, 1730): p.form(p.rect(x - 8, 720, x + 8, 820), ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.4, seed=S.sd())
    figure(S, 1060, 860, 300, coat=COATS[1], back=False); figure(S, 1800, 860, 300, coat=COATS[2], back=False)
    p.lift(p.ellipse(1300, 600, 9, 9), 'white', 1.0, tooth=0)
    gr = p.rect(300, 640, 700, 700)
    erase(S, gr); p.form(gr, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    for q in range(3): p.line(curve([(400 + q * 100, 630), (380 + q * 100, 560), (410 + q * 100, 500)], 20), 'cream', 5, 0.6, alpha=0.6)
    for (x, c) in ((250, 3), (500, 4), (760, 5)):
        bust(S, x, 520, 60, COATS[c], hs=['bob', 'short', 'long'][c - 3], smile=True)
    S.save('fellowship')


def field():
    """봉담의 허허벌판: a lone three-storey shop building among rice paddies, a dark lane with no street lights"""
    S = Shot(2005); p = S.p
    sky(S, 560, (1600, 380, 340), dusk=True)
    xs = np.linspace(0, W, 9)
    ridge(S, xs, [520, 470, 500, 450, 480, 510, 470, 490, 520], RIDGES[0], mist=0.5)
    ground(S, 560, cols=('yellowgreen', 'meadow', 'sage', 'moss'), flowers=0)
    for j in range(5):
        y = 620 + j * 90
        p.line([(0, y), (W, y + 10)], 'olive', 3, 0.6, alpha=0.5)
    building(S, 1200, 1520, 260, 600, floors=3, lit=0.3)
    tower_cross(S, 1360, 120, 0.8, glow=False)
    lane = p.poly([(1340, 600), (1400, 600), (1100, H), (760, H)])
    p.form(lane, ('stone', 'warmgrey', 'sand', 'umber'), 0, LIGHT, density=1.2, seed=S.sd())
    S.save('field')


def frogs():
    """봄밤의 개구리와 수양버들: night window of the 3rd-floor sanctuary, the willow swaying outside; the pastor weeping under the pulpit"""
    S = Shot(2006); p = S.p
    wall(S, H, cols=('slate', 'indigo', 'stone'))
    win = p.rect(980, 140, 1700, 700)
    erase(S, win); sky(S, 700, night=True)
    p.form((1 - win) * (p.YY < 9999), ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, length=(60, 120), density=1.2, seed=S.sd())
    paddy = win * (p.YY > 520)
    p.form(paddy, ('indigo', 'slate', 'pine'), 0, LIGHT, density=1.3, seed=S.sd())
    stars(S, win * (p.YY < 480), 40, 3)
    for q in range(16):                                                   # willow
        x0 = 1200 + q * 18
        p.line(curve([(x0, 160), (x0 + 30, 300), (x0 + 60 + 20 * np.sin(q), 460), (x0 + 80, 560)], 30), 'sage', 3, 0.7, alpha=0.8)
    for q in range(4): p.form(p.ellipse(1050 + q * 150, 600 + (q % 2) * 20, 18, 10), ('moss', 'olive', 'pine'), 0, LIGHT, density=1.4, seed=S.sd())
    for x in (980, 1340, 1700): p.line([(x, 140), (x, 700)], 'tan', 10, 0.8, alpha=0.9)
    p.line([(980, 420), (1700, 420)], 'tan', 10, 0.8, alpha=0.9)
    pulpit = p.poly([(300, 900), (620, 900), (590, 520), (330, 520)])
    erase(S, pulpit); p.form(pulpit, WOODC, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(pulpit, 'sepia', density=0.8, alpha=0.8)
    bust(S, 700, 640, 70, PASTOR, hs='short', eyes_closed=True, smile=False)
    tear = p.blob(670, 670, 6, 11, 0.05); p.lift(tear, 'sky_pale', 0.9, tooth=0)
    p.glow(460, 520, 160, strength=0.4, density=0.4)
    S.save('frogs')


def dawn_stairs():
    """매일 새벽: the pastor climbing the dark stairwell to the 3rd floor before dawn, light at the top"""
    S = Shot(2007); p = S.p
    wall(S, H, cols=('slate', 'stone', 'lavender'))
    for j in range(9):
        y = 980 - j * 90; x0 = 300 + j * 110
        st = p.poly([(x0, y), (x0 + 900, y), (x0 + 900, y + 90), (x0, y + 90)])
        p.form(st, ('stone', 'warmgrey', 'pebble', 'slate'), 0, LIGHT, density=1.3, seed=S.sd()); p.line([(x0, y), (x0 + 900, y)], 'umber', 3, 0.7, alpha=0.7)
    door = p.rect(1340, 80, 1560, 240)
    p.lift(door, 'butter', 0.8); p.glow(1450, 160, 260, strength=1.0, density=1.0)
    figure(S, 860, 712, 300, coat=PASTOR, back=True, walk=0.5, up=0.4)
    S.save('dawn_stairs')


def shovel():
    """성전 문 앞에 주저앉아: before the sanctuary door at dawn, a shovel and a bucket; the pastor sitting on the floor in tears"""
    S = Shot(2008); p = S.p
    wall(S, 820, cols=('stone', 'lavender', 'cream'))
    door = p.rect(1100, 160, 1500, 820)
    erase(S, door); p.form(door, ('powder', 'cornflower', 'slate', 'indigo'), 90, LIGHT, density=1.5, seed=S.sd()); p.edge(door, 'sepia', density=0.9, alpha=0.85)
    p.form(p.rect(1180, 230, 1420, 280), ('cream', 'sand', 'tan'), 0, LIGHT, density=1.4, seed=S.sd())
    floor(S, 820, cols=('stone', 'warmgrey', 'pebble', 'slate'))
    sh = p.tube([(1600, 900), (1520, 600)], 10, 10); p.form(sh, WOODC, 0, LIGHT, density=1.5, seed=S.sd())
    blade = p.poly([(1585, 880), (1650, 870), (1660, 980), (1600, 990)]); p.form(blade, ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    bk = p.poly([(1680, 860), (1820, 860), (1800, 990), (1700, 990)]); erase(S, bk); p.form(bk, ('cornflower', 'denim', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    bust(S, 760, 600, 90, PASTOR, hs='short', eyes_closed=True, smile=False)
    for x in (735, 790): p.lift(p.blob(x, 650, 6, 12, 0.05), 'sky_pale', 0.9, tooth=0)
    p.glow(1300, 160, 240, strength=0.4, density=0.4)
    S.save('shovel')


def youngman():
    """고구마 봉지를 품에 안고: the pastor walking to the factory dormitory at evening with a bag of sweet potatoes"""
    S = Shot(2009); p = S.p
    sky(S, 500, (1700, 420, 300), dusk=True)
    for (x0, x1, top) in ((100, 600, 220), (650, 1050, 300), (1100, 1500, 260)):
        building(S, x0, x1, top, 760, cols=('stone', 'warmgrey', 'pebble', 'slate'), floors=3, lit=0.4)
    for x in (300, 900, 1300): p.form(p.rect(x - 14, 60, x + 14, top), ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.4, seed=S.sd()) if False else None
    floor(S, 760, cols=('stone', 'warmgrey', 'sand', 'pebble'))
    figure(S, 1680, 900, 420, coat=PASTOR, back=False, walk=0.3)
    bag = p.blob(1610, 690, 70, 56, 0.1, seed=4)
    erase(S, bag); p.form(bag, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(bag, 'tan', density=0.8, alpha=0.8)
    for (x, y) in ((1590, 650), (1630, 655)): p.form(p.ellipse(x, y, 26, 14, rot=20), ('rose', 'mauve', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('youngman')


def knife():
    """칼이 툭 떨어지고: a dim dormitory room; the young man sitting on the floor in tears, the pastor kneeling beside him;
    the knife lies on the floor, away from them"""
    S = Shot(2010); p = S.p
    wall(S, 700, cols=('stone', 'slate', 'lavender'))
    p.window(1400, 160, 1700, 420, panes=(2, 2), glow=0.2, seed=S.sd())
    floor(S, 700, cols=('sand', 'tan', 'warmgrey', 'umber'))
    p.glow(960, 300, 300, colours=['butter', 'cream'], strength=0.5, density=0.5)
    bust(S, 780, 560, 80, ('stone', 'warmgrey', 'slate', 'umber'), hs='short', eyes_closed=True, smile=False)
    bust(S, 1060, 540, 84, PASTOR, hs='short', eyes_closed=True, smile=False,
         arms=[[(1010, 700), (920, 740), (860, 720)]])
    kn = p.poly([(380, 900), (520, 880), (528, 890), (390, 912)]); p.form(kn, ('stone', 'pebble', 'warmgrey'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.poly([(520, 878), (590, 868), (594, 884), (526, 894)]), ('sepia', 'umber', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    for x in (755, 805): p.lift(p.blob(x, 610, 6, 12, 0.05), 'sky_pale', 0.9, tooth=0)
    bag = p.blob(1320, 760, 70, 50, 0.1, seed=5); erase(S, bag); p.form(bag, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd())
    S.save('knife')


def sky_cry():
    """하늘을 올려다보며: outside the dormitory at night, the pastor looking up at the stars"""
    S = Shot(2011); p = S.p
    m = sky(S, 780, night=True)
    stars(S, m, 120, 4)
    p.glow(1500, 200, 160, strength=0.6, density=0.6); p.lift(p.ellipse(1500, 200, 40, 40) * (1 - p.ellipse(1520, 190, 36, 36)), 'butter', 0.9, tooth=0)
    building(S, 100, 700, 420, 780, cols=('slate', 'indigo', 'stone', 'umber'), floors=2, lit=0.6)
    floor(S, 780, cols=('slate', 'indigo', 'umber', 'sepia'))
    figure(S, 1100, 960, 420, coat=PASTOR, back=True, up=1.0)
    S.save('sky_cry')


def jericho():
    """여리고 땅 밟기: members walking round the apartment construction site at night, cranes and fences, praying"""
    S = Shot(2012); p = S.p
    m = sky(S, 700, night=True); stars(S, m * (p.YY < 400), 60, 5)
    for (x0, x1, top) in ((300, 620, 160), (760, 1080, 120), (1220, 1540, 200)):
        b = p.rect(x0, top, x1, 700)
        erase(S, b); p.form(b, ('stone', 'warmgrey', 'slate', 'indigo'), 90, LIGHT, density=1.3, seed=S.sd()); p.edge(b, 'sepia', density=0.7, alpha=0.7)
        for yy in range(top + 40, 700, 70): p.line([(x0, yy), (x1, yy)], 'slate', 2, 0.6, alpha=0.6)
    for (x, top) in ((680, 60), (1640, 90)):
        p.line([(x, top), (x, 700)], 'butter', 8, 0.8, alpha=0.9); p.line([(x - 300, top + 10), (x + 160, top + 10)], 'butter', 8, 0.8, alpha=0.9)
        p.line([(x + 140, top + 10), (x + 140, top + 160)], 'stone', 2, 0.7, alpha=0.8)
    fence = p.rect(0, 700, W, 790)
    erase(S, fence); p.form(fence, ('powder', 'cornflower', 'slate'), 90, LIGHT, density=1.3, seed=S.sd())
    for x in range(0, W, 120): p.line([(x, 700), (x, 790)], 'slate', 3, 0.7, alpha=0.7)
    floor(S, 790, cols=('slate', 'indigo', 'umber', 'sepia'))
    for j, x in enumerate((300, 520, 760, 1000, 1240, 1480)):
        figure(S, x, 960, 250, coat=COATS[j], back=False, walk=0.4)
    S.save('jericho')


def pancake():
    """부침개 전도: a parasol and table on the pavement, women frying pancakes, a young member handing out a tract"""
    S = Shot(2013); p = S.p
    sky(S, 420, (1600, 160, 260))
    building(S, 0, 900, 120, 640, cols=('cream', 'sand', 'tan', 'sienna'), floors=2, lit=0.3)
    building(S, 1100, W, 160, 640, cols=('powder', 'sky_pale', 'cornflower', 'slate'), floors=2, lit=0.3)
    floor(S, 640, cols=('stone', 'warmgrey', 'sand', 'pebble'))
    para = p.poly(curve([(500, 420), (720, 260), (940, 420)], 40) .tolist() + [(500, 420)])
    erase(S, para); p.form(para, ('rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(para, 'brick', density=0.8, alpha=0.8)
    for j in range(4): p.line([(520 + j * 140, 418), (720, 262)], 'cream', 3, 0.7, alpha=0.7)
    p.line([(720, 420), (720, 700)], 'stone', 6, 0.8, alpha=0.9)
    for (x, c, hs) in ((560, 6, 'bun'), (880, 4, 'bob')):
        bust(S, x, 520, 64, COATS[c], hs=hs, smile=True, look=(0, 0.5))
    tb = p.rect(440, 680, 1000, 740)
    erase(S, tb); p.form(tb, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(tb, 'tan', density=0.8, alpha=0.8)
    pan = p.ellipse(720, 660, 140, 30); p.form(pan, ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    for x in (660, 780): p.form(p.ellipse(x, 652, 50, 16), ('butter', 'ochre', 'amber', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
    for q in range(3): p.line(curve([(680 + q * 40, 630), (670 + q * 40, 570), (690 + q * 40, 520)], 20), 'cream', 4, 0.6, alpha=0.6)
    figure(S, 1300, 900, 380, coat=COATS[0], back=False)
    p.form(p.rect(1360, 650, 1420, 720), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd())
    figure(S, 1600, 920, 360, coat=COATS[7], back=False)
    S.save('pancake')


def moving_day():
    """이삿짐을 맞고: a moving truck before the new apartments; a little tent serving water and hot fish-cake soup"""
    S = Shot(2014); p = S.p
    sky(S, 500, (300, 160, 260))
    building(S, 700, 1300, 40, 620, cols=('cream', 'ivory', 'sand', 'tan'), floors=6, lit=0.2)
    building(S, 1400, 1900, 100, 620, cols=('cream', 'ivory', 'sand', 'tan'), floors=5, lit=0.2)
    floor(S, 620, cols=('stone', 'warmgrey', 'sand', 'pebble'))
    tr = p.rect(100, 420, 560, 720); erase(S, tr); p.form(tr, ('sky_pale', 'powder', 'cornflower', 'slate'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(tr, 'slate', density=0.8, alpha=0.8)
    cab = p.rect(560, 520, 700, 720); erase(S, cab); p.form(cab, ('cornflower', 'denim', 'indigo'), 0, LIGHT, density=1.5, seed=S.sd())
    for x in (200, 460, 630): p.form(p.ellipse(x, 730, 40, 40), ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    for (x, y) in ((260, 640), (380, 620)):
        bx = p.rect(x - 60, y - 60, x + 60, y + 40); erase(S, bx); p.form(bx, ('sand', 'tan', 'sienna'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(bx, 'sienna', density=0.8, alpha=0.8)
    tent = p.poly([(1000, 520), (1180, 400), (1360, 520)])
    erase(S, tent); p.form(tent, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(tent, 'tan', density=0.8, alpha=0.8)
    tb = p.rect(1020, 620, 1340, 680); erase(S, tb); p.form(tb, WOODC, 0, LIGHT, density=1.4, seed=S.sd())
    pot = p.ellipse(1100, 600, 60, 30); p.form(pot, ('stone', 'slate', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    for q in range(2): p.line(curve([(1090 + q * 30, 570), (1080 + q * 30, 520), (1100 + q * 30, 480)], 20), 'cream', 4, 0.6, alpha=0.6)
    for x in (1220, 1260, 1300): p.form(p.rect(x - 12, 570, x + 12, 620), ('sky_pale', 'powder', 'cornflower'), 0, LIGHT, density=1.4, seed=S.sd())
    figure(S, 880, 900, 360, coat=COATS[2], back=False); figure(S, 1500, 900, 360, coat=COATS[4], back=False)
    S.save('moving_day')


def kimbap_car():
    """눈물 젖은 김밥: inside the old church car, the pastor and two members eating kimbap, tired, a little smile"""
    S = Shot(2015); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(0, 6), ['slate', 'stone', 'warmgrey'], (60, 150), (1.8, 2.5), 1.6, 0.66, seed=S.sd())
    ws = p.poly([(300, 80), (1620, 80), (1700, 520), (220, 520)])
    erase(S, ws); sky(S, 520, (1500, 200, 260))
    p.form((p.YY < 520) * (1 - ws), ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    for (x, c, hs) in ((560, PASTOR, 'short'), (960, COATS[6], 'bun'), (1360, COATS[0], 'short')):
        bust(S, x, 600, 80, c, hs=hs, eyes_closed=(x == 960), smile=True)
    dash = p.rect(0, 860, W, H); erase(S, dash); p.form(dash, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    for (x, y) in ((620, 830), (1000, 840)):
        kb = p.ellipse(x, y, 30, 30); p.form(kb, ('sepia', 'pine', 'forest'), 0, LIGHT, density=1.6, seed=S.sd())
        p.form(p.ellipse(x, y, 20, 20), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd())
        p.form(p.ellipse(x, y, 7, 7), ('butter', 'coral', 'leaf'), 0, LIGHT, density=1.4, seed=S.sd())
    S.save('kimbap_car')


def banner_tree():
    """나무 타는 목사님: the pastor up a tall tree tying a banner between branches, the town below"""
    S = Shot(2016); p = S.p
    sky(S, H, (300, 200, 260))
    clouds(S, [(500, 160, 300, 70), (1500, 120, 260, 60)])
    trunk = p.tube([(700, H), (720, 600), (760, 120)], 60, 36)
    erase(S, trunk); p.form(trunk, WOODC, 90, LIGHT, density=1.6, seed=S.sd()); p.edge(trunk, 'sepia', density=0.8, alpha=0.8)
    trunk2 = p.tube([(1500, H), (1490, 600), (1470, 160)], 56, 34)
    erase(S, trunk2); p.form(trunk2, WOODC, 90, LIGHT, density=1.6, seed=S.sd())
    for (x, y, r) in ((760, 160, 220), (1470, 200, 220), (600, 300, 160), (1620, 320, 160)):
        cr = p.blob(x, y, r, r * 0.7, 0.2, seed=S.sd()); p.form(cr, ('meadow', 'moss', 'pine', 'forest'), p.flow(-50, 40), LIGHT, density=1.3, seed=S.sd())
    ban = p.poly([(790, 400), (1440, 420), (1440, 540), (790, 520)])
    erase(S, ban); p.form(ban, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(ban, 'brick', density=0.9, alpha=0.8)
    p.form(p.rect(800, 410, 820, 530), ('brick', 'red', 'rose'), 0, LIGHT, density=1.4, seed=S.sd())
    for j in range(2): p.line([(860, 445 + j * 40), (1380, 460 + j * 40)], 'brick', 7, 0.8, alpha=0.8)
    figure(S, 790, 600, 300, coat=PASTOR, back=True, up=0.3)
    p.line([(820, 380), (790, 410)], 'brick', 3, 0.8, alpha=0.9)
    for (x0, x1) in ((0, 500), (1650, W)):
        building(S, x0, x1, 760, H, cols=('cream', 'sand', 'tan', 'sienna'), floors=2, lit=0.2)
    S.save('banner_tree')


def fall():
    """나무 밑에 주저앉아: under the tree, the pastor sitting on the ground holding his bandaged leg; the banner hanging askew"""
    S = Shot(2017); p = S.p
    sky(S, 600, (1600, 300, 280))
    ground(S, 600, flowers=40)
    trunk = p.tube([(1100, H), (1110, 500), (1130, 0)], 70, 50)
    erase(S, trunk); p.form(trunk, WOODC, 90, LIGHT, density=1.6, seed=S.sd()); p.edge(trunk, 'sepia', density=0.8, alpha=0.8)
    ban = p.poly([(1140, 160), (1700, 300), (1690, 380), (1140, 250)])
    erase(S, ban); p.form(ban, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(ban, 'brick', density=0.9, alpha=0.8)
    bust(S, 820, 560, 90, PASTOR, hs='short', eyes_closed=True, smile=False,
         arms=[[(760, 720), (720, 800), (760, 840)]])
    leg = p.tube([(880, 860), (1060, 880)], 40, 34); erase(S, leg); p.form(leg, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    bd = p.rect(960, 850, 1010, 905); p.form(bd, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(bd, 'warmgrey', density=0.8, alpha=0.7)
    p.form(p.ellipse(985, 878, 8, 6), ('rose', 'coral', 'coral'), 0, LIGHT, density=1.2, seed=S.sd())
    S.save('fall')


def office():
    """읍사무소 창고: a storeroom piled with rolled-up banners; a smiling clerk pointing to the corner, the pastor bowing"""
    S = Shot(2018); p = S.p
    wall(S, 760, cols=('cream', 'ivory', 'powder'))
    floor(S, 760, cols=('stone', 'warmgrey', 'pebble', 'slate'))
    for j in range(14):
        x = 1250 + (j % 5) * 110; y = 720 - (j // 5) * 70
        rl = p.ellipse(x, y, 60, 30); erase(S, rl); p.form(rl, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(rl, 'tan', density=0.8, alpha=0.8)
        p.line([(x - 50, y), (x + 50, y)], 'brick', 3, 0.7, alpha=0.6)
    bust(S, 500, 520, 80, COATS[1], hs='short', smile=True, look=(0.6, 0), arms=[[(570, 680), (680, 640), (780, 600)]])
    bust(S, 960, 560, 80, PASTOR, hs='short', smile=True, eyes_closed=True)
    S.save('office')


def vision():
    """1130 세계비전: the pastor before twelve members in the shop sanctuary; behind him a world map with points of light"""
    S = Shot(2019); p = S.p
    wall(S, H, cols=('cream', 'butter', 'apricot'))
    mp = p.rect(360, 80, 1560, 560)
    erase(S, mp); p.form(mp, ('sky_pale', 'powder', 'cornflower'), 0, LIGHT, density=1.2, seed=S.sd()); p.edge(mp, 'tan', density=0.8, alpha=0.8)
    for (x, y, rx, ry) in ((560, 230, 140, 90), (640, 420, 70, 110), (900, 220, 120, 80), (960, 400, 90, 120), (1200, 230, 220, 110), (1380, 450, 80, 50)):
        p.form(p.blob(x, y, rx, ry, 0.25, seed=S.sd()), ('sage', 'meadow', 'moss'), 0, LIGHT, density=1.3, seed=S.sd())
    for (x, y) in ((1300, 330), (1250, 380), (980, 380), (1000, 330), (1260, 470), (600, 260), (700, 470)):
        p.glow(x, y, 50, strength=0.9, density=0.9)
    bust(S, 960, 640, 70, PASTOR, hs='short', smile=True, arms=[[(1010, 790), (1100, 720), (1150, 640)]])
    for j, x in enumerate(np.linspace(220, 1700, 8)):
        if abs(x - 960) < 160: continue
        bust(S, x, 900, 58, COATS[j % len(COATS)], hs=['short', 'long', 'bun', 'bob'][j % 4], smile=True, look=(0, -0.4))
    S.save('vision')


def mission():
    """구역마다 선교지: a hand-drawn map with threads from the church to Malaysia, Kenya and Uganda; little churches rising"""
    S = Shot(2020); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(4, 6, 500), ['cream', 'ivory', 'butter'], (60, 150), (1.8, 2.5), 1.4, 0.55, seed=S.sd())
    sea = p.rect(80, 60, 1840, 1020)
    p.form(sea, ('sky_pale', 'powder', 'cornflower'), 0, LIGHT, density=1.0, seed=S.sd())
    lands = [(560, 330, 230, 200), (700, 700, 170, 260), (1250, 330, 360, 200), (1350, 650, 120, 80), (1560, 840, 150, 90)]
    for (x, y, rx, ry) in lands:
        p.form(p.blob(x, y, rx, ry, 0.25, seed=S.sd()), ('sage', 'meadow', 'moss', 'yellowgreen'), 0, LIGHT, density=1.3, seed=S.sd())
    home = (1460, 330)
    for (x, y) in ((1330, 650), (720, 640), (760, 560)):
        p.line(curve([home, ((home[0] + x) / 2, min(home[1], y) - 160), (x, y)], 60), 'gold', 4, 0.85, alpha=0.9)
        ch = np.clip(p.rect(x - 22, y - 30, x + 22, y + 10) + p.poly([(x - 30, y - 28), (x, y - 60), (x + 30, y - 28)]), 0, 1)
        erase(S, ch); p.form(ch, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(ch, 'sienna', density=0.9, alpha=0.85)
        p.form(np.clip(p.rect(x - 2, y - 84, x + 2, y - 58) + p.rect(x - 10, y - 76, x + 10, y - 72), 0, 1), ('brick', 'red', 'red'), 0, LIGHT, density=1.6, seed=S.sd())
    p.glow(*home, 70, strength=1.0, density=1.0)
    S.save('mission')


def prayer():
    """목요 중보기도: members kneeling in a circle in the sanctuary, hands together, warm light from above"""
    S = Shot(2021); p = S.p
    wall(S, 700, cols=('cream', 'butter', 'apricot'))
    floor(S, 700, cols=('sand', 'tan', 'sienna', 'brown'))
    beam = p.poly([(800, 0), (1120, 0), (1400, 900), (520, 900)])
    p.hatch(beam, 90, ['glow', 'butter', 'cream'], (60, 160), (1.8, 2.4), 0.9, 0.6, opacity=0.6, alpha=0.4, seed=S.sd())
    for j, (x, y) in enumerate(((560, 560), (760, 520), (960, 510), (1160, 520), (1360, 560), (660, 760), (1260, 760))):
        bust(S, x, y, 62, COATS[j % len(COATS)], hs=['short', 'long', 'bun', 'bob', 'short', 'long', 'short'][j], eyes_closed=True, smile=False)
    for (x, y) in ((560, 690), (760, 650), (960, 640), (1160, 650), (1360, 690)):
        k.ari.gassho(S, x, y, 0.45)
    p.glow(960, 200, 400, strength=0.7, density=0.7)
    S.save('prayer')


def land():
    """240평 부지: an empty plot fenced with a rope and stakes, a sign; the members standing at its edge looking on"""
    S = Shot(2022); p = S.p
    sky(S, 480, (1500, 200, 300))
    clouds(S, [(500, 160, 300, 70), (1300, 120, 260, 60)])
    building(S, 0, 400, 200, 560, floors=3, lit=0.2)
    building(S, 1500, W, 160, 560, cols=('powder', 'sky_pale', 'cornflower', 'slate'), floors=3, lit=0.2)
    ground(S, 480, cols=('sand', 'tan', 'ochre', 'butter'), flowers=0)
    for (x, y) in ((500, 560), (1400, 560), (1500, 820), (420, 820)):
        p.form(p.rect(x - 8, y - 60, x + 8, y), WOODC, 0, LIGHT, density=1.5, seed=S.sd())
    p.line([(500, 520), (1400, 520), (1500, 780), (420, 780), (500, 520)], 'brick', 3, 0.8, alpha=0.85)
    sg = p.rect(860, 380, 1060, 470); erase(S, sg); p.form(sg, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(sg, 'sienna', density=0.9, alpha=0.85)
    p.form(p.rect(955, 470, 965, 560), WOODC, 0, LIGHT, density=1.5, seed=S.sd())
    for j, x in enumerate((420, 640, 1280, 1500)):
        figure(S, x, 1000, 300, coat=COATS[j], back=True, up=0.2)
    S.save('land')


def offerings():
    """두 렙돈: on a wooden offering table, envelopes, a wedding ring, a savings passbook, a small bundle from selling paper"""
    S = Shot(2023); p = S.p
    wall(S, 560, cols=('cream', 'ivory', 'apricot'))
    tb = p.rect(0, 560, W, H); erase(S, tb); p.form(tb, WOODC, 0, LIGHT, length=(60, 140), density=1.5, seed=S.sd())
    cloth = p.rect(300, 600, 1620, 1000); erase(S, cloth); p.form(cloth, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.2, seed=S.sd())
    for (x, y, rot) in ((520, 720, -6), (720, 700, 4), (620, 820, 8)):
        ev = p.poly([(x - 110, y - 60), (x + 110, y - 66), (x + 116, y + 60), (x - 104, y + 66)])
        erase(S, ev); p.form(ev, ('white', 'butter', 'cream'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(ev, 'tan', density=0.9, alpha=0.85)
    ring = p.ellipse(1000, 760, 46, 30) * (1 - p.ellipse(1000, 760, 32, 18))
    p.form(ring, ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd()); p.lift(p.ellipse(1000, 732, 10, 8), 'white', 0.9, tooth=0)
    pb = p.rect(1150, 650, 1420, 820); erase(S, pb); p.form(pb, ('cornflower', 'denim', 'indigo'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(pb, 'slate', density=0.9, alpha=0.85)
    p.line([(1190, 700), (1380, 700)], 'cream', 4, 0.8, alpha=0.8)
    for j in range(4):
        bn = p.rect(1180 + j * 6, 860 - j * 8, 1400 + j * 6, 900 - j * 8); p.form(bn, ('sage', 'lichen', 'cream'), 0, LIGHT, density=1.3, seed=S.sd())
    p.glow(960, 400, 500, strength=0.6, density=0.6)
    S.save('offerings')


def groundbreak():
    """2011년 10월 기공예배: members in a row with white gloves lifting shovels of earth, a ribbon banner behind"""
    S = Shot(2024); p = S.p
    sky(S, 520, (1600, 180, 280))
    ground(S, 520, cols=('sand', 'tan', 'ochre', 'butter'), flowers=0)
    tent = p.rect(260, 160, 1660, 260); erase(S, tent); p.form(tent, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(tent, 'brick', density=0.8, alpha=0.8)
    for x in (280, 1640): p.form(p.rect(x - 8, 260, x + 8, 560), ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.4, seed=S.sd())
    mound = p.blob(960, 800, 700, 90, 0.1, seed=3); p.form(mound * (p.YY > 740), ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    for j, x in enumerate(np.linspace(380, 1540, 6)):
        figure(S, x, 820, 380, coat=COATS[j], back=False)
        sh = p.tube([(x + 50, 760), (x + 70, 600)], 7, 7); p.form(sh, WOODC, 0, LIGHT, density=1.5, seed=S.sd())
        p.form(p.ellipse(x + 50, 770, 26, 16), ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('groundbreak')


def stairs():
    """좁은 계단: a narrow new staircase; a senior deaconess with hands on hips calling out, the pastor scratching his head"""
    S = Shot(2025); p = S.p
    wall(S, H, cols=('cream', 'ivory', 'sand'))
    for j in range(8):
        y = 980 - j * 90; x0 = 1060 + j * 50
        st = p.rect(x0, y, x0 + 220, y + 90); p.form(st, ('stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.3, seed=S.sd()); p.line([(x0, y), (x0 + 220, y)], 'umber', 3, 0.7, alpha=0.7)
    p.line([(1050, 990), (1450, 290)], 'sienna', 6, 0.8, alpha=0.9)
    bust(S, 520, 520, 86, COATS[6], hs='bun', smile=True, look=(0.6, 0),
         arms=[[(450, 680), (390, 760), (440, 800)], [(590, 680), (650, 760), (600, 800)]])
    bust(S, 860, 540, 84, PASTOR, hs='short', smile=True, look=(-0.4, 0), arms=[[(920, 700), (980, 600), (940, 480)]])
    S.save('stairs')


def interest():
    """이자의 날들: at the kitchen table at night, the pastor and his wife over a calculator and bills, holding hands, smiling"""
    S = Shot(2026); p = S.p
    wall(S, 640, cols=('cream', 'apricot', 'butter'))
    p.window(1400, 140, 1700, 420, panes=(2, 2), glow=0.2, seed=S.sd())
    lamp = p.poly([(860, 60), (1060, 60), (1120, 160), (800, 160)]); p.form(lamp, ('butter', 'gold', 'amber'), 0, LIGHT, density=1.4, seed=S.sd())
    p.glow(960, 220, 420, strength=0.9, density=0.9)
    bust(S, 720, 470, 84, PASTOR, hs='short', smile=True, eyes_closed=True)
    bust(S, 1200, 470, 80, WIFE, hs='long', smile=True, eyes_closed=True)
    tb = p.rect(300, 640, 1620, H); erase(S, tb); p.form(tb, WOODC, 0, LIGHT, length=(60, 140), density=1.5, seed=S.sd())
    calc = p.rect(880, 700, 1040, 840); erase(S, calc); p.form(calc, ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.rect(900, 715, 1020, 750), ('sage', 'lichen', 'cream'), 0, LIGHT, density=1.3, seed=S.sd())
    for (x, y) in ((620, 760), (1240, 760)):
        pg = p.rect(x - 90, y - 60, x + 90, y + 60); erase(S, pg); p.form(pg, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(pg, 'tan', density=0.8, alpha=0.8)
        for q in range(4): p.line([(x - 70, y - 35 + q * 22), (x + 60, y - 35 + q * 22)], 'pebble', 2, 0.6, alpha=0.6)
    hm = heart_mask(p, 960, 640, 36); p.form(hm, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('interest')


def church_built():
    """오직 하나님의 이름만: the new church at sunrise, the members gathered on its steps, waving"""
    S = Shot(2027); p = S.p
    sky(S, 760, (1500, 380, 460))
    clouds(S, [(400, 160, 300, 70), (1300, 120, 260, 60)])
    xs = np.linspace(0, W, 9)
    ridge(S, xs, [700, 640, 670, 620, 650, 690, 640, 660, 700], RIDGES[0], mist=0.5)
    ground(S, 760, flowers=120)
    body = p.rect(620, 300, 1300, 800)
    erase(S, body); p.form(body, ('cream', 'ivory', 'sand', 'tan'), 90, LIGHT, length=(30, 70), density=1.4, seed=S.sd()); p.edge(body, 'sepia', density=0.8, alpha=0.8)
    roof = p.poly([(580, 310), (960, 140), (1340, 310)]); erase(S, roof); p.form(roof, ('brick', 'terracotta', 'sienna', 'brown'), 0, LIGHT, density=1.6, seed=S.sd())
    tower_cross(S, 960, -20, 0.9)
    for xx in (700, 1140):
        p.window(xx, 380, xx + 90, 520, panes=(1, 2), glow=0.7, seed=S.sd())
    door = p.rect(880, 600, 1040, 800); p.form(door, ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    steps = p.rect(760, 800, 1160, 860); erase(S, steps); p.form(steps, ('stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.3, seed=S.sd())
    for j, x in enumerate((260, 420, 1500, 1660)):
        figure(S, x, 1000, 320, coat=COATS[j], back=False)
    p.glow(1500, 380, 300, strength=0.6, density=0.6)
    S.save('church_built')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
