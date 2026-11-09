"""reel 2 「迷惑をかけちゃいけない」 paintings. python3 shots.py NAME"""
import sys
from mcommon import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'arigatou', 'art_src'))
from shots import room, gassho        # noqa  (reel 1's room and hands)

SUIT = ('lavender', 'slate', 'indigo', 'umber')
NIGHT = ('periwinkle', 'slate', 'indigo', 'umber')


def office_bg(S, fg, night=False):
    p = S.p
    wall = np.ones((H, W), np.float32)
    if night:
        p.hatch(wall, p.flow(2, 4, 500), ('slate', 'periwinkle', 'indigo'), (60, 140), (1.8, 2.5), 1.8, 0.7, avoid=fg, seed=S.sd())
    else:
        p.hatch(wall, p.flow(2, 4, 500), ('cream', 'ivory', 'powder'), (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.55, avoid=fg, seed=S.sd())
    return wall


def hook():
    """① a young office worker smiling and bowing a little, a hand at the back of his head -- 'daijoubu desu'"""
    S = Shot(401); p = S.p
    ARMS = [[(700, 1080), (800, 900), (720, 640)]]
    m = person(S, 540, 760, 190, coat=SUIT, hair_style='short', plan=True, arms=ARMS)
    office_bg(S, m['mask'])
    for x0 in (60, 720):                                  # office windows, daylight, desks behind (soft)
        win = p.rect(x0, 160, x0 + 300, 700) * (1 - m['mask'])
        p.hatch(win, p.flow(-4, 4), ('day_sky', p.value(0.3, 0.9, 160, 700)), (40, 100), (1.7, 2.4), 1.4, 0.68, seed=S.sd())
        for y in (160, 430, 700): p.line([(x0, y), (x0 + 300, y)], 'warmgrey', 6, 0.7, alpha=0.8)
    desk = p.rect(0, 1500, 1080, 1920) * (1 - m['mask'])
    p.form(desk, ('ivory', 'stone', 'warmgrey', 'pebble'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    person(S, 540, 760, 190, coat=SUIT, hair_style='short', eyes_closed=True, smile=True, arms=ARMS,
           hair=('hair', 'umber', 'sepia'))
    tie = p.poly([(530, 980), (550, 980), (562, 1200), (540, 1240), (518, 1200)])
    p.form(tie, ('powder', 'cornflower', 'slate'), 90, LIGHT, density=1.4, seed=S.sd())
    p.form(p.poly([(470, 950), (540, 1000), (610, 950), (600, 1060), (540, 1040), (480, 1060)]), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.2, seed=S.sd())
    # a little sweat drop of the brave smile
    drop = p.poly(curve([(370, 640), (385, 680), (370, 700), (355, 680)], 20), smooth=True)
    p.form(drop, ('white', 'powder', 'cornflower'), 90, LIGHT, density=1.4, seed=S.sd())
    S.save('hook')


def train():
    """② a packed morning train: rows of tired commuters holding the straps, one face in the middle"""
    S = Shot(402); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(80, 6), ('ivory', 'stone', 'warmgrey'), (60, 140), (1.8, 2.5), 1.6, 0.66, seed=S.sd())
    for x0 in (40, 560):
        win = p.rect(x0, 260, x0 + 480, 700)
        p.hatch(win, p.flow(-4, 4), ('slate', 'periwinkle', 'powder'), (40, 120), (1.7, 2.4), 1.5, 0.68, seed=S.sd())
        p.strokes([[(x0 + 30 + k * 90, 640), (x0 + 130 + k * 90, 320)] for k in range(4)], 'powder', width=4, pressure=0.6, opacity=0.6, alpha=0.6)
    p.line([(0, 200), (1080, 200)], 'warmgrey', 12, 0.8, alpha=0.9)
    for x in range(90, 1080, 150):                       # hanging straps
        p.line([(x, 200), (x, 330)], 'warmgrey', 4, 0.8, alpha=0.9)
        p.ripples(x, 350, 22, 22, rings=1, colour='warmgrey', width=4)
    specs = [(170, 820, 110, ('stone', 'warmgrey', 'pebble', 'umber')), (900, 800, 115, SUIT), (540, 900, 150, SUIT),
             (330, 1000, 140, ('powder', 'slate', 'indigo', 'umber')), (760, 1010, 140, ('sand', 'tan', 'sienna', 'umber'))]
    arms = lambda x, y, R: [[(x + R * 0.6, y + R * 1.2), (x + R * 0.7, y + R * 0.2), (x + R * 0.5, y - R * 1.6)]] if x in (170, 900) else None
    masks = [person(S, x, y, R, coat=c, plan=True, arms=arms(x, y, R), hair_style='short' if x != 330 else 'bob')['mask'] for (x, y, R, c) in specs]
    for i, (x, y, R, c) in enumerate(specs):            # back to front: each one hidden where someone in front stands
        front = np.clip(sum(masks[i + 1:]), 0, 1) if i + 1 < len(masks) else None
        person(S, x, y, R, coat=c, hair_style='short' if x != 330 else 'bob', eyes_closed=x != 540, smile=False,
               arms=arms(x, y, R), hair=('hair', 'umber', 'sepia'), cut=front, cut_head=True)
    S.save('train')


def overtime():
    """② late in the office: one desk lamp and a monitor still on, the windows dark blue, everyone else gone"""
    S = Shot(403); p = S.p
    m = person(S, 540, 980, 130, coat=SUIT, hair_style='short', plan=True)
    office_bg(S, m['mask'], night=True)
    for x0 in (60, 400, 740):
        win = p.rect(x0, 150, x0 + 280, 700) * (1 - m['mask'])
        p.hatch(win, p.flow(-4, 4), ('indigo', 'slate', 'ultramarine'), (40, 100), (1.7, 2.4), 1.6, 0.72, seed=S.sd())
        p.dots(win * (p.YY > 500), ('butter', 'lantern'), n=14, size=(3, 6))
    person(S, 540, 980, 130, coat=SUIT, hair_style='short', eyes_closed=False, smile=False, look=(0, 0.4), hair=('hair', 'umber', 'sepia'))
    desk = p.rect(0, 1300, 1080, 1920)
    p.form(desk, ('slate', 'warmgrey', 'indigo', 'umber'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    mon = p.rect(340, 1050, 740, 1320)
    p.form(mon, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    p.glow(540, 1000, 340, colours='glow', strength=0.9, density=0.9)
    p.form(p.rect(330, 1320, 750, 1350), ('stone', 'warmgrey', 'umber'), 0, LIGHT, density=1.3, seed=S.sd())
    for (x, y) in ((180, 1450), (900, 1420)):
        p.form(p.rect(x - 90, y - 40, x + 90, y + 40), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.0, seed=S.sd())
    p.glow(880, 1150, 200, strength=0.8, density=0.9)
    S.save('overtime')


def room_dark():
    """② home at night, the light off: sitting on the floor against the bed, only the phone's glow on her face"""
    S = Shot(404); p = S.p
    ARMS = [[(450, 1180), (440, 1300), (520, 1330)], [(630, 1180), (650, 1300), (560, 1330)]]
    m = person(S, 540, 1000, 140, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='bob', plan=True, arms=ARMS)
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ('indigo', 'slate', 'periwinkle'), (60, 140), (1.8, 2.5), 2.0, 0.72, avoid=m['mask'], seed=S.sd())
    win = p.rect(640, 200, 980, 640)
    p.hatch(win, p.flow(-4, 4), ('ultramarine', 'indigo', 'periwinkle'), (40, 100), (1.7, 2.4), 1.6, 0.72, seed=S.sd())
    p.lift(p.ellipse(880, 300, 36, 36), 'cream', 0.8)
    bed = p.rect(0, 1150, 1080, 1430) * (1 - m['mask'])
    p.form(bed, ('periwinkle', 'slate', 'indigo'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.rect(0, 1430, 1080, 1920), ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    person(S, 540, 1000, 140, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='bob', eyes_closed=False, smile=False,
           look=(0, 0.6), arms=ARMS, hands=False, hair=('hair', 'umber', 'sepia'))
    phone = p.rect(500, 1280, 580, 1400)
    p.form(phone, ('powder', 'cream', 'white'), 0, LIGHT, density=1.4, seed=S.sd())
    p.glow(540, 1260, 230, colours='glow', strength=0.7, density=0.8)
    S.save('room_dark')


def station():
    """③ やさしさ: a rainy station platform, people waiting in a neat line under umbrellas, making room for each other"""
    S = Shot(405); p = S.p
    sky = (p.YY < 800).astype(np.float32)
    p.hatch(sky, p.flow(-4, 4), ('powder', 'lavender', 'warmgrey', 'sky_pale'), (60, 140), (1.8, 2.5), 1.8, 0.7, seed=S.sd())
    roof = p.poly([(0, 0), (1080, 0), (1080, 260), (0, 360)])
    p.form(roof, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    for x in (200, 860):
        p.form(p.rect(x - 22, 300, x + 22, 1500), ('stone', 'warmgrey', 'umber'), 90, LIGHT, density=1.4, seed=S.sd())
    plat = (p.YY >= 1300).astype(np.float32)
    p.form(plat, ('ivory', 'stone', 'warmgrey', 'pebble'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    p.form(p.rect(0, 1300, 1080, 1340), ('lemon', 'butter', 'sun'), 0, LIGHT, density=1.6, seed=S.sd())   # the yellow line
    cols = [('coral', 'red', 'brick'), ('powder', 'cornflower', 'slate'), ('butter', 'sun', 'amber'), ('sage', 'moss', 'forest'), ('lavender', 'mauve', 'violet')]
    for k in range(5):
        x, y, R = 160 + k * 190, 1060 + k * 22, 70 + k * 4
        person(S, x, y, R, coat=cols[(k + 2) % 5], hair_style='short' if k % 2 else 'bob', eyes_closed=k == 2, smile=True, look=(0.3, 0),
               hair=('hair', 'umber', 'sepia'))
        um = p.poly(curve([(x - R * 1.7, y - R * 0.7), (x, y - R * 2.0), (x + R * 1.7, y - R * 0.7)], 30).tolist() + [(x, y - R * 0.55)])
        p.form(um, cols[k], 0, LIGHT, density=1.5, seed=S.sd())
        p.line([(x, y - R * 2.0), (x, y - R * 2.3)], 'umber', 4, 0.8, alpha=0.9)
    rain = [[(x, y), (x + 6, y + S.r.uniform(30, 60))] for x, y in zip(S.r.uniform(0, 1080, 700), S.r.uniform(330, 1900, 700))]
    p.strokes(rain[:350], ['slate', 'periwinkle'], width=2.2, pressure=0.7, opacity=0.4, alpha=0.6)
    p.strokes(rain[350:], ['white', 'cream'], width=2.4, pressure=0.7, opacity=0.8, alpha=0.7)
    S.save('station')


def phone():
    """④ the phone in her hand: a chat with an empty message box (the words are typed and deleted in the edit)"""
    S = Shot(406); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-30, 10, 300), ('slate', 'periwinkle', 'indigo', 'lavender'), (60, 140), (1.8, 2.6), 1.8, 0.7, seed=S.sd())
    from pcommon import curve as _c
    def rr(x0, y0, x1, y1, r):
        pts = []
        for (cx, cy, a0) in ((x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)):
            for a in np.linspace(a0, a0 + 90, 8):
                pts.append((cx + r * np.cos(np.deg2rad(a)), cy + r * np.sin(np.deg2rad(a))))
        return p.poly(pts)
    body = rr(300, 260, 780, 1300, 70)
    hand = p.poly(_c([(160, 1920), (200, 1500), (300, 1180), (360, 1120), (420, 1180), (380, 1500), (420, 1920)], 50), smooth=True)
    fingers = np.clip(sum(p.ellipse(800, 700 + k * 110, 60, 46) for k in range(4)), 0, 1)
    p.form(np.clip(fingers, 0, 1) * (1 - body), SKIN, 0, LIGHT, density=1.5, seed=S.sd())
    p.form(body, ('slate', 'indigo', 'umber'), 90, LIGHT, density=1.6, seed=S.sd())
    scr = rr(326, 290, 754, 1270, 50)
    p.lift(scr, 'white', 0.9)
    p.hatch(scr, 90, ('white', 'cream', 'ivory'), (40, 100), (1.6, 2.2), 1.4, 0.7, opacity=0.85, alpha=0.7, seed=S.sd())
    p.form(p.rect(326, 300, 754, 400) * scr, ('powder', 'sky_pale', 'cornflower'), 0, LIGHT, density=1.3, seed=S.sd())
    p.form(p.ellipse(385, 350, 30, 30), ('peach', 'apricot', 'tan'), 0, LIGHT, density=1.3, seed=S.sd())      # a friend's icon
    for (x0, y0, x1, y1, c) in ((350, 440, 620, 510, ('stone', 'warmgrey', 'pebble')), (350, 530, 560, 600, ('stone', 'warmgrey', 'pebble')),
                                (480, 640, 730, 710, ('yellowgreen', 'meadow', 'grass'))):
        p.form(rr(x0, y0, x1, y1, 30), c, 0, LIGHT, density=1.2, seed=S.sd())
    box = rr(345, 800, 690, 870, 30)
    p.form(box, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.0, seed=S.sd()); p.edge(box, 'warmgrey', density=0.9)
    p.form(p.ellipse(720, 835, 26, 26), ('powder', 'cornflower', 'slate'), 0, LIGHT, density=1.3, seed=S.sd())   # send
    kb = p.rect(326, 900, 754, 1240) * scr
    p.form(kb, ('stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.3, seed=S.sd())
    for r_, n in ((0, 10), (1, 9), (2, 7)):
        w = (754 - 326 - 20) / 10
        x0 = 336 + (10 - n) * w / 2
        for c in range(n):
            p.form(rr(x0 + c * w + 3, 920 + r_ * 80, x0 + (c + 1) * w - 3, 985 + r_ * 80, 8), ('white', 'cream', 'ivory'), 0, LIGHT, density=0.9, seed=S.sd())
    p.form(rr(420, 1160, 660, 1225, 10), ('white', 'cream', 'ivory'), 0, LIGHT, density=0.9, seed=S.sd())
    p.form(hand, SKIN, p.contour(hand, 8, 90), LIGHT, density=1.5, warm='peach', seed=S.sd())
    p.edge(hand, 'skin_shade', density=0.8)
    th = p.tube([(380, 1250), (450, 1120), (520, 1040)], 62, 50)
    p.form(th, SKIN, p.contour(th, 8, 90), LIGHT, density=1.5, warm='peach', seed=S.sd()); p.edge(th, 'skin_shade', density=0.8)
    S.save('phone')


def clearing():
    """⑤ the rain stopping over the city: the clouds parting, light coming down"""
    S = Shot(407); p = S.p
    sky = (p.YY < 1350).astype(np.float32)
    v = p.value(0.15, 0.9, 0, 1350)
    p.hatch(sky, p.flow(-3, 4), ('day_sky', v), (60, 150), (1.8, 2.6), 1.6, 0.72, seed=S.sd())
    cm = clouds(S, [(200, 300, 520, 160), (860, 240, 520, 150), (540, 520, 600, 140), (150, 700, 420, 110), (930, 760, 420, 110)])
    p.hatch(cm * 0.7, p.flow(-2, 6, 300), ('lavender', 'stone', 'warmgrey'), (40, 100), (1.6, 2.3), 1.0, 0.66, alpha=0.5, seed=S.sd())
    beam = p.poly([(470, 330), (620, 330), (860, 1400), (220, 1400)])
    p.hatch(beam, 92, ('butter', 'cream', 'white'), (60, 140), (1.8, 2.4), 1.2, 0.62, opacity=0.7, alpha=0.5, seed=S.sd())
    p.glow(545, 360, 220, strength=1.3, density=1.1)
    city = np.zeros((H, W), np.float32)
    x = 0
    rr_ = np.random.default_rng(5)
    while x < 1080:
        w = rr_.uniform(70, 150); top = rr_.uniform(1000, 1220)
        city = np.maximum(city, p.rect(x, top, x + w, 1400)); x += w + rr_.uniform(0, 10)
    city = np.maximum(city, p.rect(600, 900, 660, 1400))
    p.form(city * (p.YY < 1400), ('lavender', 'periwinkle', 'slate', 'indigo'), 90, LIGHT, density=1.4, warm='peach', seed=S.sd())
    p.dots(city * (p.YY < 1380) * (p.YY > 1100), ('butter', 'lantern', 'cream'), n=120, size=(3, 6))
    wet = (p.YY >= 1400).astype(np.float32)
    p.form(wet, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    p.hatch(wet * np.exp(-((p.XX - 540) / 220) ** 2), 90, ('butter', 'cream', 'glow'), (40, 120), (1.6, 2.2), 1.2, 0.66, opacity=0.6, alpha=0.6, seed=S.sd())
    S.save('clearing')


def sprout():
    """⑥ 弱いときにこそ: a small green sprout coming up through a crack in the wet pavement, the sun on it"""
    S = Shot(408); p = S.p
    bg = np.ones((H, W), np.float32)
    p.form(bg, ('ivory', 'stone', 'warmgrey', 'pebble'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    for k in range(5):                                    # paving joints
        p.line([(0, 300 + k * 380), (1080, 340 + k * 380)], 'pebble', 3.0, 0.7, alpha=0.7)
        p.line([(200 + k * 260, 0), (160 + k * 260, 1920)], 'pebble', 3.0, 0.7, alpha=0.6)
    pts = [(250, 1700), (330, 1640), (300, 1560), (420, 1500), (470, 1400), (560, 1330), (640, 1350), (700, 1250), (820, 1200)]
    crack = curve(pts, 80)
    p.strokes([crack], 'umber', width=9.0, pressure=0.85, opacity=0.5, alpha=0.95)
    p.strokes([crack + [0, 4]], 'sepia', width=4.0, pressure=0.8, opacity=0.5, alpha=0.8)
    p.glow(560, 1050, 420, strength=1.0, density=1.0)
    stem = curve([(560, 1330), (552, 1220), (566, 1080), (590, 960)], 30)
    p.strokes([stem], ['leaf', 'grass'], width=10.0, pressure=0.8, opacity=0.4, alpha=0.95)
    for (cx, cy, rx, ry, rot) in ((500, 950, 100, 42, -30), (680, 905, 110, 44, 25)):
        lf = p.ellipse(cx, cy, rx, ry, rot)
        p.form(lf, ('yellowgreen', 'leaf', 'grass', 'forest'), rot, LIGHT, density=1.6, warm='butter', seed=S.sd())
        p.edge(lf, 'forest', density=0.7)
    p.dots(p.ellipse(560, 1250, 180, 60), ('powder', 'white'), n=20, size=(3, 6))   # rain drops still on the stone
    S.save('sprout')


def bag():
    """⑦ morning: the heavy bag set down on the floor by the window, the light coming in"""
    S = Shot(409); p = S.p
    room(S, np.zeros((H, W), np.float32), win_box=(160, 180, 920, 980), wall_to=1250)
    p.glow(540, 560, 420, strength=1.2, density=1.1)
    floor_ = (p.YY >= 1250).astype(np.float32)
    p.form(floor_, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', seed=S.sd())
    beam = p.poly([(160, 980), (920, 980), (1080, 1700), (0, 1700)])
    p.hatch(beam * floor_, 80, ('butter', 'cream'), (60, 140), (1.8, 2.4), 1.0, 0.62, opacity=0.7, alpha=0.45, seed=S.sd())
    bagm = p.poly(curve([(330, 1650), (310, 1420), (360, 1330), (720, 1330), (770, 1420), (750, 1650)], 60), smooth=True)
    p.form(bagm, ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, warm='butter', seed=S.sd())
    p.line(curve([(440, 1335), (480, 1230), (600, 1230), (640, 1335)], 30), 'umber', 10, 0.85, alpha=0.95)
    p.form(p.rect(330, 1440, 750, 1470) * bagm, ('brown', 'umber', 'sepia'), 0, LIGHT, density=1.2, seed=S.sd())
    p.edge(bagm, 'umber', density=0.8)
    for (x, c) in ((90, ('terracotta', 'brick', 'sienna')), (990, ('powder', 'cornflower', 'slate'))):
        pot = p.poly([(x - 60, 1150), (x + 60, 1150), (x + 48, 1240), (x - 48, 1240)])
        p.form(pot, c, 90, LIGHT, density=1.4, seed=S.sd())
        p.leaves(p.blob(x, 1080, 90, 80, 0.2), ('leaf', 'grass', 'meadow', 'forest'), size=(12, 22), density=1.2, seed=S.sd())
    S.save('bag')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
