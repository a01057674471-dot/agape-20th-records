"""reel 4 「"罪"って犯罪のこと?」 paintings -- kyudo, the arrow that misses. python3 shots.py NAME"""
import sys
from tcommon import *

GI = ('white', 'cream', 'ivory', 'sand')
HAKAMA = ('slate', 'indigo', 'umber', 'sepia')
HAIR = ('hair', 'umber', 'sepia')
WOOD = ('sand', 'tan', 'sienna', 'brown')


def mato(S, cx, cy, r):
    """the kyudo target: white ground, black rings (kasumi-mato), a dark wooden rim"""
    p = S.p
    p.form(p.ellipse(cx, cy, r * 1.08, r * 1.08), ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    for k, (rr, col) in enumerate(((1.0, ('white', 'cream', 'ivory')), (0.86, ('slate', 'indigo', 'umber')), (0.74, ('white', 'cream', 'ivory')),
                                   (0.62, ('slate', 'indigo', 'umber')), (0.5, ('white', 'cream', 'ivory')), (0.32, ('slate', 'indigo', 'umber')),
                                   (0.2, ('white', 'cream', 'ivory')))):
        p.form(p.ellipse(cx, cy, r * rr, r * rr), col, 0, LIGHT, length=(6, 14), density=1.6, seed=S.sd())


def azuchi(S, y_top, y_bot, roof=True):
    """the earthen target mound under its little roof, raked sand in front"""
    p = S.p
    mound = p.poly([(0, y_top + 60), (1080, y_top + 60), (1080, y_bot), (0, y_bot)])
    p.form(mound, ('sand', 'ochre', 'tan', 'sienna'), 80, LIGHT, length=(30, 70), density=1.4, seed=S.sd())
    if roof:
        rf = p.poly([(0, y_top - 40), (1080, y_top - 40), (1080, y_top + 70), (0, y_top + 70)])
        p.form(rf, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
        p.line([(0, y_top + 70), (1080, y_top + 70)], 'sepia', 6, 0.8, alpha=0.9)
    return mound


def archer_back(S, x, y, R, draw=1.0):
    """an archer seen from behind: hair in a low knot, white gi, black hakama, the long bow held up at the left,
    the right elbow drawn back (draw 0..1 opens the stance)"""
    p = S.p
    head = p.ellipse(x, y, R * 0.9, R)
    knot = p.ellipse(x, y + R * 0.75, R * 0.3, R * 0.24)
    torso = p.poly(curve([(x - R * 0.5, y + R * 0.9), (x - R * 1.25, y + R * 1.5), (x - R * 1.2, y + R * 3.2), (x + R * 1.2, y + R * 3.2),
                          (x + R * 1.25, y + R * 1.5), (x + R * 0.5, y + R * 0.9)], 50), smooth=True)
    hakama = p.poly(curve([(x - R * 1.2, y + R * 3.0), (x - R * 1.7, y + R * 6.2), (x + R * 1.7, y + R * 6.2), (x + R * 1.2, y + R * 3.0)], 40), smooth=True)
    larm = p.tube([(x - R * 1.0, y + R * 1.5), (x - R * 2.2, y + R * 1.0), (x - R * 3.0, y + R * 0.6)], R * 0.36, R * 0.3)
    rarm = p.tube([(x + R * 1.0, y + R * 1.5), (x + R * 1.9 * draw + R * 0.3, y + R * 1.4), (x + R * 0.9, y + R * 0.75)], R * 0.38, R * 0.32)
    p.form(hakama, HAKAMA, 90, LIGHT, length=(20, 50), density=1.6, seed=S.sd())
    for k in range(5):
        xx = x - R * 1.2 + k * R * 0.6
        p.line([(xx, y + R * 3.2), (xx - R * 0.15 + k * R * 0.07, y + R * 6.1)], 'umber', 2.4, 0.6, alpha=0.6)    # pleats
    p.form(np.clip(torso + larm + rarm, 0, 1), GI, 80, LIGHT, length=(16, 36), density=1.5, warm='butter', cool='lavender', seed=S.sd())
    p.hatch(np.clip(torso + larm + rarm, 0, 1) * smoothstep(x - R * 0.2, x + R * 1.4, p.XX), 80, ('stone', 'lavender'), (14, 30), (1.5, 2.2), 1.0, 0.66, alpha=0.6, seed=S.sd())
    for m in (torso, larm, rarm, hakama):
        p.edge(m, 'sepia', width=(2.0, 3.0), density=1.0, pressure=0.75, alpha=0.9)
    p.form(p.rect(x - R * 1.22, y + R * 2.95, x + R * 1.22, y + R * 3.15) * torso, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(np.clip(head + knot, 0, 1), HAIR, p.radial(x, y + R), LIGHT, length=(10, 24), density=1.6, seed=S.sd())
    p.form(p.ellipse(x - R * 3.05, y + R * 0.6, R * 0.2, R * 0.2), SKIN, 0, LIGHT, density=1.4, seed=S.sd())      # bow hand
    p.form(p.ellipse(x + R * 0.9, y + R * 0.75, R * 0.22, R * 0.2), ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.4, seed=S.sd())  # glove
    bow = curve([(x - R * 3.2, y - R * 4.2), (x - R * 3.5, y - R * 1.5), (x - R * 3.0, y + R * 0.6), (x - R * 3.25, y + R * 2.6), (x - R * 3.0, y + R * 3.6)], 60)
    p.strokes([bow], ['tan', 'sienna'], width=R * 0.12, pressure=0.85, opacity=0.5, alpha=0.95)
    p.line([(x - R * 3.2, y - R * 4.2), (x + R * 0.9 * draw - R * 0.6 * (1 - draw), y + R * 0.75), (x - R * 3.0, y + R * 3.6)], 'cream', 2.0, 0.7, alpha=0.8)
    p.line([(x + R * 0.95, y + R * 0.72), (x - R * 3.6, y + R * 0.55)], 'sepia', 3.0, 0.8, alpha=0.9)       # the arrow
    return np.clip(head + knot + torso + hakama + larm + rarm, 0, 1)


def dojo(S, dark=0.0, light_door=0.0):
    """inside the shooting hall looking out across the sand yard to the target mound; dark = dusk, light_door = a
    bright opening in the shoji at the right"""
    p = S.p
    sky = (p.YY < 640).astype(np.float32)
    if dark < 0.5:
        morning_sky(S, sky)
    else:
        p.hatch(sky, p.flow(-4, 4), ('indigo', 'slate', 'periwinkle'), (60, 140), (1.8, 2.5), 1.8, 0.72, seed=S.sd())
    p.tree(140, 640, 300, 150, ('sage', 'moss', 'pine', 'forest'), clumps=8, light=LIGHT, seed=S.sd())
    p.tree(960, 640, 340, 170, ('sage', 'moss', 'pine', 'forest'), clumps=8, light=LIGHT, seed=S.sd())
    azuchi(S, 560, 780)
    for cx in (330, 540, 750):
        mato(S, cx, 700, 44)
    yard = p.rect(0, 780, 1080, 1180)
    p.form(yard, ('ivory', 'sand', 'stone', 'warmgrey'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    for k in range(8): p.line([(0, 800 + k * 48), (1080, 806 + k * 48)], 'stone', 2.0, 0.5, alpha=0.4)      # raked lines
    eaves = p.rect(0, 0, 1080, 150)
    p.form(eaves, WOOD, 0, LIGHT, density=1.6, seed=S.sd())
    for x in (30, 1050):
        p.form(p.rect(x - 30, 0, x + 30, 1300), WOOD, 90, LIGHT, density=1.6, seed=S.sd())
    floor_ = (p.YY >= 1180).astype(np.float32)
    p.form(floor_, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.6, warm='butter', seed=S.sd())
    for k in range(10):
        p.line([(0, 1200 + k * 75), (1080, 1210 + k * 75)], 'brown', 2.4, 0.6, alpha=0.5)
    if dark > 0:
        p.hatch(np.ones((H, W), np.float32), p.flow(-30, 10, 400), ('indigo', 'slate', 'umber'), (60, 140), (1.8, 2.5), 1.4 * dark,
                0.7, opacity=0.35, alpha=0.55 * dark, seed=S.sd())
    if light_door > 0:
        door = p.rect(640, 160, 1040, 1300)
        p.lift(door, 'cream', 0.85 * light_door)
        p.hatch(door, 90, ('butter', 'cream', 'white'), (40, 120), (1.7, 2.4), 1.4, 0.66, opacity=0.8, alpha=0.7, seed=S.sd())
        p.glow(840, 700, 520, strength=1.4 * light_door, density=1.2)
        beam = p.poly([(640, 1300), (1040, 1300), (900, 1920), (100, 1920)])
        p.hatch(beam, 100, ('butter', 'cream'), (60, 140), (1.8, 2.4), 1.2, 0.62, opacity=0.7, alpha=0.5 * light_door, seed=S.sd())
        for x in (640, 840, 1040): p.line([(x, 160), (x, 1300)], 'tan', 8, 0.8, alpha=0.9)


def hook():
    """① a face looking straight at us, a little offended (ムッ)"""
    S = Shot(601); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-20, 10, 300), ('cream', 'peach', 'apricot'), (60, 140), (1.8, 2.6), 1.6, 0.64, seed=S.sd())
    person(S, 540, 800, 260, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='short', hair=HAIR, smile=False, look=(0, 0))
    for sgn in (-1, 1):                                    # knitted brows and a pout
        p.line([(540 + sgn * 160, 760 - 70), (540 + sgn * 50, 760 - 40)], 'umber', 7, 0.85, alpha=0.95)
    p.line(curve([(500, 960), (540, 945), (580, 960)], 10), 'brick', 5, 0.85, alpha=0.95)
    p.strokes([[(820, 560), (870, 520)], [(840, 600), (900, 580)], [(820, 520), (840, 470)]], 'red', width=6, pressure=0.8, opacity=0.5, alpha=0.9)   # the little anger marks
    S.save('hook')


def crosswalk():
    """② an ordinary morning: people waiting at a red light, nobody crossing"""
    S = Shot(602); p = S.p
    sky = (p.YY < 700).astype(np.float32)
    morning_sky(S, sky)
    for (x, w, top, wall) in ((0, 300, 260, ('cream', 'apricot', 'peach')), (300, 260, 360, ('powder', 'sky_pale', 'cornflower')),
                              (560, 280, 220, ('cream', 'ivory', 'sand')), (840, 240, 320, ('peach', 'apricot', 'tan'))):
        b = p.rect(x, top, x + w, 1000)
        p.form(b, wall + ('slate',), 90, LIGHT, density=1.4, seed=S.sd())
        for r_ in range(int((1000 - top - 80) / 110)):
            for c in range(2):
                p.form(p.rect(x + 30 + c * (w / 2), top + 50 + r_ * 110, x + w / 2 - 10 + c * (w / 2), top + 120 + r_ * 110),
                       ('powder', 'sky_pale', 'cornflower'), 0, LIGHT, density=1.2, seed=S.sd())
    road = (p.YY >= 1000).astype(np.float32)
    p.form(road, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    for k in range(6):
        x0 = 60 + k * 170
        p.form(p.poly([(x0, 1500), (x0 + 110, 1500), (x0 + 130, 1700), (x0 - 20, 1700)]), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd())
    pole = p.rect(920, 700, 940, 1300)
    p.form(pole, ('stone', 'warmgrey', 'slate'), 90, LIGHT, density=1.5, seed=S.sd())
    sig = p.rect(880, 700, 980, 900)
    p.form(sig, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(930, 750, 30, 30), ('coral', 'red', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    p.glow(930, 750, 70, colours='glow', strength=0.7, density=0.8)
    for k, (x, c) in enumerate(((150, ('cream', 'sand', 'tan', 'brown')), (330, ('slate', 'indigo', 'umber', 'sepia')),
                                (520, ('peach', 'coral', 'terracotta', 'brick')), (700, ('lavender', 'mauve', 'violet', 'indigo')))):
        person(S, x, 1130, 64, coat=c, hair_style=('short', 'bob', 'long', 'short')[k], hair=HAIR, smile=False, look=(0.6, -0.3))
    S.save('crosswalk')


def koban():
    """③ a little police box on the corner, its red lamp, a bicycle, a friendly officer standing in front"""
    S = Shot(603); p = S.p
    sky = (p.YY < 800).astype(np.float32)
    morning_sky(S, sky)
    clouds(S, [(260, 300, 360, 90)])
    box = p.rect(200, 620, 880, 1300)
    p.form(box, ('cream', 'ivory', 'sand', 'tan'), 90, LIGHT, density=1.5, seed=S.sd())
    rf = p.poly([(160, 560), (920, 560), (900, 640), (180, 640)])
    p.form(rf, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    p.window(260, 760, 480, 1000, panes=(2, 2), glow=0.3)
    door = p.rect(560, 780, 820, 1300)
    p.form(door, ('powder', 'sky_pale', 'cornflower', 'slate'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.ellipse(540, 600, 34, 34), ('coral', 'red', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    p.glow(540, 600, 90, strength=0.8, density=0.8)
    p.form((p.YY >= 1300).astype(np.float32), ('stone', 'warmgrey', 'pebble', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    person(S, 690, 1180, 78, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='short', hair=HAIR, smile=True, look=(-0.3, 0.1))
    cap = p.poly([(620, 1090), (760, 1090), (750, 1130), (630, 1130)])
    p.form(np.clip(cap + p.ellipse(690, 1090, 66, 30), 0, 1), ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    for (cx, cy) in ((300, 1500), (470, 1500)):            # a bicycle
        p.ripples(cx, cy, 70, 70, rings=1, colour='slate', width=5)
    p.line([(300, 1500), (380, 1400), (470, 1500)], 'slate', 5, 0.8, alpha=0.9)
    p.line([(380, 1400), (360, 1360), (430, 1360)], 'slate', 5, 0.8, alpha=0.9)
    S.save('koban')


def dojo_wide():
    """④ the quiet dojo: an archer from behind at the line, the bow raised, the targets far across the sand"""
    S = Shot(604); p = S.p
    dojo(S)
    archer_back(S, 620, 1150, 110, draw=0.4)
    S.save('dojo_wide')


def draw_():
    """④ full draw (kai): closer behind the archer, the arrow at the cheek, aimed at the far target"""
    S = Shot(605); p = S.p
    dojo(S)
    archer_back(S, 600, 1000, 160, draw=1.0)
    S.save('draw')


def miss():
    """④ the arrow has missed: the target close, its centre empty; the arrow stuck in the sand beside it"""
    S = Shot(606); p = S.p
    azuchi(S, 120, 1920, roof=True)
    p.hatch(p.rect(0, 0, 1080, 90), p.flow(-4, 4), ('day_sky', p.value(0.2, 0.6, 0, 90)), (40, 100), (1.7, 2.4), 1.4, 0.7, seed=S.sd())
    mato(S, 460, 900, 300)
    p.glow(460, 900, 90, colours='glow', strength=0.5, density=0.6)
    sh = p.poly([(860, 1180), (1000, 1050), (1010, 1060), (870, 1195)])
    p.form(sh, ('sepia', 'umber', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    p.strokes([curve([(870, 1190), (1060, 1010)], 20)], ['sepia', 'umber'], width=10, pressure=0.85, opacity=0.5, alpha=0.95)
    for k in range(3):                                     # fletching
        p.strokes([[(1040 + k * 8, 1030 - k * 8), (1080, 980 - k * 6)]], ['white', 'cream'], width=10, pressure=0.8, opacity=0.8, alpha=0.95)
    p.form(p.ellipse(860, 1195, 50, 16), ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.4, seed=S.sd())   # the sand it struck
    S.save('miss')


def many_miss():
    """⑤ すべての人が: the target, and around it many arrows in the sand -- every one of them off"""
    S = Shot(607); p = S.p
    azuchi(S, 120, 1920, roof=True)
    mato(S, 540, 860, 260)
    rr_ = np.random.default_rng(3)
    for k in range(14):
        a = rr_.uniform(0, 2 * np.pi); d = rr_.uniform(340, 520)
        x, y = 540 + np.cos(a) * d, 860 + np.sin(a) * d * 0.9
        if not (40 < x < 1040 and 240 < y < 1800): continue
        ang = rr_.uniform(-0.5, 0.5)
        tail = (x + 140 * np.cos(-0.7 + ang), y + 140 * np.sin(-0.7 + ang))
        p.strokes([[(x, y), tail]], ['sepia', 'umber'], width=7, pressure=0.85, opacity=0.5, alpha=0.95)
        p.strokes([[(tail[0] - 20, tail[1] + 14), tail]], ['white', 'cream'], width=8, pressure=0.8, opacity=0.8, alpha=0.95)
        p.form(p.ellipse(x, y, 26, 9), ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.3, seed=S.sd())
    S.save('many_miss')


def turnaway():
    """⑤ 背を向けて: someone walking toward us, away from the warm light behind them, into the cool blue"""
    S = Shot(608); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(80, 6), ('cream', 'butter', 'apricot'), (60, 140), (1.8, 2.5), 1.4, 0.62, seed=S.sd())
    p.hatch(bg * smoothstep(500, 1920, p.YY), p.flow(80, 6), ('slate', 'periwinkle', 'indigo'), (60, 140), (1.8, 2.5), 1.7, 0.7, seed=S.sd())
    p.glow(540, 240, 380, strength=1.5, density=1.2)
    path = p.poly([(470, 420), (610, 420), (980, 1920), (100, 1920)])
    p.form(path, ('ivory', 'stone', 'warmgrey', 'pebble'), 90, LIGHT, density=1.3, seed=S.sd())
    p.hatch(path * smoothstep(900, 1920, p.YY), 90, ('slate', 'periwinkle'), (40, 100), (1.7, 2.4), 1.2, 0.66, alpha=0.6, seed=S.sd())
    person(S, 540, 1180, 110, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='short', hair=HAIR, smile=False, look=(0.5, 0.5),
           arms=[[(450, 1320), (420, 1480), (430, 1560)], [(630, 1320), (660, 1480), (650, 1560)]])
    p.form(p.ellipse(540, 1620, 160, 26), ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.2, seed=S.sd())
    S.save('turnaway')


def clutch():
    """⑤ 贈り物だけを握りしめる: someone holding a gift box tight to the chest, eyes away from the light"""
    S = Shot(609); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-30, 10, 300), ('slate', 'periwinkle', 'lavender', 'indigo'), (60, 140), (1.8, 2.6), 1.6, 0.7, seed=S.sd())
    p.glow(130, 200, 320, strength=1.0, density=0.9)
    ARMS = [[(340, 1080), (300, 1260), (420, 1330)], [(740, 1080), (780, 1260), (660, 1330)]]
    person(S, 540, 760, 200, coat=('lavender', 'slate', 'indigo', 'umber'), hair_style='short', hair=HAIR, smile=False, look=(0.8, 0.4),
           arms=ARMS, hands=False)
    box = p.rect(380, 1180, 700, 1460)
    p.form(box, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.rect(515, 1180, 565, 1460), ('coral', 'red', 'brick'), 90, LIGHT, density=1.6, seed=S.sd())
    p.form(p.rect(380, 1295, 700, 1345), ('coral', 'red', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    for sgn in (-1, 1):
        p.form(p.ellipse(540 + sgn * 70, 1165, 60, 34, sgn * 25), ('coral', 'red', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    for (x, sgn) in ((395, -1), (685, 1)):                  # fingers gripping the box
        for k in range(4):
            f = p.ellipse(x - sgn * 6, 1250 + k * 50, 34, 22)
            p.form(f, SKIN, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(f, 'skin_shade', density=0.7)
    S.save('clutch')


def dark_dojo():
    """⑥ the dojo at dusk, the doors shut: the distance we cannot close ourselves"""
    S = Shot(610); dojo(S, dark=1.0); S.save('dark_dojo')


def light_dojo():
    """⑥ the same dojo, a door opened from outside: light pouring in across the floor"""
    S = Shot(611); dojo(S, dark=0.6, light_door=1.0); S.save('light_dojo')


if __name__ == '__main__':
    n = sys.argv[1]
    globals()['draw_' if n == 'draw' else n]()
