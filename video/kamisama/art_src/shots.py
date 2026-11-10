"""reel 8 「"神様"は一人じゃないの?」 paintings -- nature, its Maker, and the one who calls your name. python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *

_sp = importlib.util.spec_from_file_location('ari_shots', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'arigatou', 'art_src', 'shots.py'))
ari = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ari)
gassho = ari.gassho

HAIR = ('hair_light', 'hair', 'umber')
RIDGES = [('powder', 'periwinkle', 'lavender', 'violet'), ('lavender', 'periwinkle', 'slate', 'indigo'),
          ('sage', 'lichen', 'moss', 'pine'), ('yellowgreen', 'sage', 'moss', 'pine'), ('moss', 'pine', 'forest', 'sepia')]


def erase(S, m):
    """clear an area back to paper so a figure painted there is opaque"""
    S.p.lift(blur(np.clip(m, 0, 1), 1.5), 'paper', 1.0, tooth=0.0)


def sky(S, y1, sun=None, warm=True):
    p = S.p
    m = (p.YY < y1).astype(np.float32)
    morning_sky(S, m, warm_low=warm)
    if sun:
        p.glow(sun[0], sun[1], sun[2], strength=1.2, density=1.1)
    return m


def ridge(S, xs, ys, cols, mist=0.0, cut=None, field=-8):
    """one mountain ridge (everything below the line), with a band of mist lifted at its foot"""
    p = S.p
    m = p.below(xs, ys)
    if cut is not None: m = m * (1 - cut)
    p.form(m, cols, p.flow(field, 14), LIGHT, length=(30, 70), density=1.3, warm='peach', seed=S.sd())
    if mist:
        top = np.interp(p.XX, xs, ys)
        band = smoothstep(top + 40, top + 200, p.YY) * m
        p.lift(blur(band, 12), 'cream', mist)
    return m


def mist(S, y, h, amount=0.7, wob=40):
    p = S.p
    yy = y + wob * (noise2d(H, W, 260, 2, S.sd()) - 0.5)
    band = np.exp(-((p.YY - yy) / h) ** 2)
    p.lift(blur(band, 6), 'cream', amount)


def figure(S, x, y, h, coat=('peach', 'coral', 'terracotta', 'brick'), hair=HAIR, back=True, up=0.0, walk=0.0, legs=('stone', 'warmgrey', 'umber')):
    """a small full-length person, feet at (x, y), h px tall; from behind (back=True) the head is all hair.
    up > 0 tips the head back (looking up at the sky); walk opens the stride."""
    p = S.p
    R = h * 0.11
    hx, hy = x, y - h + R - up * R * 0.25
    head = p.ellipse(hx, hy, R * 0.92, R)
    body = p.poly(curve([(x - R * 0.45, y - h + R * 1.85), (x - R * 1.25, y - h + R * 2.5), (x - R * 1.55, y - h * 0.38),
                         (x + R * 1.55, y - h * 0.38), (x + R * 1.25, y - h + R * 2.5), (x + R * 0.45, y - h + R * 1.85)], 50), smooth=True)
    lg = [p.tube([(x - R * 0.55, y - h * 0.4), (x - R * 0.6 - walk * R * 0.8, y - R * 0.3)], R * 0.36, R * 0.3),
          p.tube([(x + R * 0.55, y - h * 0.4), (x + R * 0.6 + walk * R * 0.5, y - R * 0.3)], R * 0.36, R * 0.3)]
    legm = np.clip(lg[0] + lg[1], 0, 1) * (1 - body)
    arms = np.clip(p.tube([(x - R * 1.2, y - h + R * 2.6), (x - R * 1.6, y - h * 0.55)], R * 0.34, R * 0.3) +
                   p.tube([(x + R * 1.2, y - h + R * 2.6), (x + R * 1.6, y - h * 0.55)], R * 0.34, R * 0.3), 0, 1)
    erase(S, np.clip(head + body + arms + legm, 0, 1))
    p.form(legm, legs, 90, LIGHT, length=(8, 18), density=1.4, seed=S.sd())
    for sx in (x - R * 0.6 - walk * R * 0.8, x + R * 0.6 + walk * R * 0.5):
        p.form(p.ellipse(sx, y - R * 0.2, R * 0.42, R * 0.24), ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    cm = np.clip(body + arms, 0, 1)
    p.form(cm, coat, 85, LIGHT, length=(12, 28), density=1.4, warm='butter', cool='lavender', seed=S.sd())
    if back:
        p.form(head, hair, p.radial(hx, hy - R, 90), LIGHT, length=(8, 18), density=1.6, seed=S.sd())
    else:
        hm = p.ellipse(hx, hy - R * 0.25, R * 0.98, R * 0.85) * (p.YY < hy - R * 0.1)
        p.form(head * (1 - hm), SKIN, p.contour(head, 6), LIGHT, length=(6, 12), density=1.4, warm='peach', seed=S.sd())
        p.form(hm, hair, p.radial(hx, hy - R, 90), LIGHT, length=(8, 18), density=1.6, seed=S.sd())
    for m in (cm, head, legm):
        p.edge(m, 'sepia', width=(1.4, 2.2), density=0.8, pressure=0.6, alpha=0.7)
    return np.clip(head + cm + legm, 0, 1)


def shimenawa(S, cx, y, rx, ry, thick=40, shide=4):
    """the straw rope round a sacred tree trunk (the front half of an ellipse), with white zigzag paper shide hanging"""
    p = S.p
    t = np.linspace(np.pi * 0.02, np.pi * 0.98, 60)
    path = np.stack([cx + rx * np.cos(np.pi - t), y + ry * np.sin(t)], 1)
    rope = p.tube(path, thick, thick)
    p.form(rope, ('butter', 'sand', 'ochre', 'sienna'), p.contour(rope, 6, 60), LIGHT, length=(8, 18), density=1.6, seed=S.sd())
    for k in range(1, 22):                          # the twist
        a = path[int(k * 59 / 22)]
        p.line([(a[0] - thick * 0.5, a[1] - thick * 0.8), (a[0] + thick * 0.5, a[1] + thick * 0.8)], 'sienna', 2.4, 0.7, alpha=0.75)
    p.edge(rope, 'sepia', width=(1.6, 2.4), density=0.9, pressure=0.6, alpha=0.8)
    for k in range(shide):
        a = path[int((k + 0.7) * 59 / (shide + 0.4))]
        x0, y0 = a[0], a[1] + thick * 0.8
        s = thick * 0.9
        z = [(x0 - s * 0.35, y0), (x0 + s * 0.35, y0), (x0 + s * 0.35, y0 + s), (x0 + s * 0.85, y0 + s), (x0 + s * 0.85, y0 + s * 2),
             (x0 + s * 0.35, y0 + s * 2), (x0 + s * 0.35, y0 + s * 3), (x0 - s * 0.35, y0 + s * 3), (x0 - s * 0.35, y0 + s * 2),
             (x0 + s * 0.15, y0 + s * 2), (x0 + s * 0.15, y0 + s), (x0 - s * 0.35, y0 + s)]
        m = p.poly(z)
        p.form(m, ('white', 'cream', 'ivory'), 90, LIGHT, density=1.4, seed=S.sd())
        p.edge(m, 'warmgrey', width=(1.2, 1.8), density=0.9, alpha=0.7)
    return rope


def sacred_tree(S, cx, base, tw, top, crown_r):
    """a huge old tree: a wide trunk with flared roots, a broad crown; returns the trunk mask"""
    p = S.p
    trunk = p.poly(curve([(cx - tw * 1.25, base), (cx - tw * 0.62, base - 120), (cx - tw * 0.5, top + crown_r * 0.6),
                          (cx - tw * 0.8, top + crown_r * 0.2), (cx + tw * 0.8, top + crown_r * 0.2), (cx + tw * 0.5, top + crown_r * 0.6),
                          (cx + tw * 0.62, base - 120), (cx + tw * 1.3, base)], 80), smooth=True)
    trunk = trunk * (p.YY > top + crown_r * 0.2)
    p.form(trunk, ('tan', 'sienna', 'brown', 'umber'), 90, LIGHT, length=(30, 70), density=1.6, seed=S.sd())
    for k in range(9):                              # bark furrows
        xx = cx - tw * 0.45 + k * tw * 0.11
        p.line(curve([(xx, top + crown_r * 0.7), (xx + 6 * np.sin(k), (top + base) / 2), (xx + (xx - cx) * 0.6, base - 30)], 30),
               'umber', 2.6, 0.7, alpha=0.6)
    p.edge(trunk, 'sepia', width=(2.0, 3.0), density=1.0, pressure=0.7, alpha=0.85)
    blobs = ((cx - crown_r * 0.95, top + crown_r * 0.3, crown_r * 0.7), (cx + crown_r * 0.95, top + crown_r * 0.25, crown_r * 0.7),
             (cx, top - crown_r * 0.15, crown_r * 0.9), (cx - crown_r * 0.45, top + crown_r * 0.55, crown_r * 0.6),
             (cx + crown_r * 0.45, top + crown_r * 0.55, crown_r * 0.6))
    ms = [p.blob(bx, by, br, br * 0.8, 0.16, seed=S.sd()) for bx, by, br in blobs]
    crown = np.clip(sum(ms), 0, 1)
    erase(S, crown)
    lit = np.zeros_like(crown)
    for m, (bx, by, br) in sorted(zip(ms, blobs), key=lambda z: z[1][1]):
        lit = lit * (1 - m) + p.shading(m, LIGHT, br * 0.5) * m
    p.form(crown, ('yellowgreen', 'meadow', 'moss', 'pine'), p.flow(-55, 60, 80), LIGHT, length=(12, 26), density=1.3,
           warm='butter', lit=lit, seed=S.sd())
    p.leaves(crown * smoothstep(0.45, 0.9, 1 - lit), 'pine', (10, 18), 0.9, pressure=0.8, seed=S.sd())
    p.leaves(crown * (0.3 + 0.7 * smoothstep(0.25, 0.7, lit)), 'meadow', (10, 18), 0.8, seed=S.sd())
    p.leaves(crown * smoothstep(0.5, 0.95, lit), 'yellowgreen', (10, 18), 0.8, opacity=0.6, seed=S.sd())
    for (bx, by, br) in blobs[:2]:
        p.edge(p.blob(bx, by, br, br * 0.8, 0.16), 'pine', width=(1.4, 2.0), density=0.4, alpha=0.4)
    return trunk


def ground(S, y0, cols=('meadow', 'yellowgreen', 'grass', 'moss'), flowers=40):
    p = S.p
    g = (p.YY > y0).astype(np.float32)
    p.form(g, cols, p.flow(-4, 10), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    if flowers: p.flowers(g * (p.YY > y0 + 120), n=flowers, size=(5, 9))
    return g


# ============================================================ the shots
def mountains():
    """八百万の神様: a sea of cloud from above, ridge after ridge of misty mountains, the morning sun"""
    S = Shot(801); p = S.p
    sky(S, 900, (800, 640, 360))
    p.lift(p.ellipse(800, 640, 70, 70), 'sun', 0.8)
    clouds(S, [(220, 320, 340, 70), (760, 220, 260, 60)])
    xs = np.linspace(0, 1080, 9)
    ys = [[820, 760, 700, 760, 800, 740, 690, 740, 780], [980, 900, 940, 1010, 930, 880, 940, 990, 960],
          [1160, 1110, 1060, 1130, 1180, 1120, 1080, 1140, 1170], [1380, 1320, 1350, 1300, 1260, 1330, 1380, 1340, 1300],
          [1640, 1560, 1600, 1660, 1620, 1560, 1520, 1580, 1620]]
    for k, (yy, c) in enumerate(zip(ys, RIDGES)):
        ridge(S, xs, yy, c, mist=0.75 - k * 0.08)
        if k < 4: mist(S, ys[k + 1][4] + 10, 70, 0.55)
    for x in range(30, 1080, 55):                    # treetops on the nearest ridge
        top = np.interp(x, xs, ys[4])
        p.form(p.blob(x, top + 30, 34, 50, 0.2, seed=S.sd()), ('moss', 'pine', 'forest', 'sepia'), 90, LIGHT, density=1.3, seed=S.sd())
    for (x, y) in ((380, 520), (420, 545), (455, 510)):
        p.line(curve([(x - 18, y), (x - 7, y - 9), (x, y - 2), (x + 7, y - 9), (x + 18, y)], 12), 'sepia', 2.4, 0.8, alpha=0.8)
    S.save('mountains')


def sea():
    """海にも: the calm sea in morning light, two rocks joined by a shimenawa rope, waves at the shore"""
    S = Shot(802); p = S.p
    sky(S, 860, (540, 820, 380))
    clouds(S, [(200, 300, 320, 70), (860, 420, 300, 60)])
    water = (p.YY >= 860).astype(np.float32)
    p.hatch(water, p.flow(0, 3), ('water', p.value(0.3, 0.0, 860, 1920)), (60, 150), (1.8, 2.6), 1.9, 0.76, seed=S.sd())
    p.line([(0, 862), (1080, 862)], 'cornflower', 3, 0.7, alpha=0.7)
    path = p.poly([(470, 860), (610, 860), (760, 1920), (320, 1920)]) * smoothstep(1700, 860, p.YY)
    p.hatch(path, 0, ('glow', 'butter', 'cream'), (30, 80), (1.6, 2.2), 1.0, 0.7, opacity=0.6, alpha=0.6, seed=S.sd())
    rocks = []
    for (cx, cy, rx, ry) in ((360, 1280, 150, 210), (780, 1340, 100, 140)):
        m = p.blob(cx, cy, rx, ry, 0.12, seed=S.sd()) * (p.YY < cy + ry * 0.55)
        p.form(m, ('stone', 'warmgrey', 'umber', 'sepia'), p.contour(m, 10, 60), LIGHT, length=(14, 30), density=1.5, seed=S.sd())
        p.edge(m, 'sepia', width=(1.8, 2.6), density=1.0, alpha=0.85)
        p.line(curve([(cx - rx * 1.1, cy + ry * 0.55), (cx, cy + ry * 0.62), (cx + rx * 1.1, cy + ry * 0.55)], 20), 'white', 6, 0.85, alpha=0.9)
        p.ripples(cx, cy + ry * 0.6, rx * 1.1, 18, 3, 'white')
        rocks.append((cx, cy, rx, ry))
    a = (rocks[0][0] + rocks[0][2] * 0.6, rocks[0][1] - rocks[0][3] * 0.55); b = (rocks[1][0] - rocks[1][2] * 0.6, rocks[1][1] - rocks[1][3] * 0.5)
    rp = curve([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 60), b], 40)
    rope = p.tube(rp, 13, 13)
    p.form(rope, ('butter', 'sand', 'ochre', 'sienna'), p.contour(rope, 4, 60), LIGHT, density=1.6, seed=S.sd())
    p.edge(rope, 'sepia', width=(1.2, 1.8), density=0.9, alpha=0.8)
    shore = p.below([0, 400, 800, 1080], [1700, 1740, 1680, 1720])
    p.form(shore, ('sand', 'butter', 'tan', 'ochre'), p.flow(-3, 8), LIGHT, length=(30, 70), density=1.3, seed=S.sd())
    for y in (1690, 1725):
        p.line(curve([(0, y), (300, y + 30), (600, y - 10), (1080, y + 20)], 40), 'white', 5, 0.8, alpha=0.85)
    for (x, y) in ((680, 560), (715, 585)):
        p.line(curve([(x - 18, y), (x - 7, y - 9), (x, y - 2), (x + 7, y - 9), (x + 18, y)], 12), 'sepia', 2.4, 0.8, alpha=0.8)
    S.save('sea')


def bigtree():
    """大きな木にも: the old sacred tree in a quiet grove, the shimenawa round its trunk, light through the leaves"""
    S = Shot(803); p = S.p
    sky(S, 1500, (860, 260, 320))
    for x, h in ((70, 380), (1010, 420)):
        p.tree(x, 1520, h, 150, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    ground(S, 1500, flowers=50)
    p.form(p.ellipse(540, 1560, 420, 60), ('moss', 'olive', 'umber'), 0, LIGHT, density=1.0, seed=S.sd())
    sacred_tree(S, 540, 1580, 200, 420, 330)
    shimenawa(S, 540, 1040, 175, 50, 30, shide=4)
    beam = p.poly([(860, 260), (980, 260), (640, 1600), (380, 1600)])
    p.hatch(beam, 70, ('butter', 'cream'), (60, 140), (1.8, 2.4), 0.7, 0.6, opacity=0.6, alpha=0.3, seed=S.sd())
    for (x, y) in ((260, 1650), (820, 1680)):
        p.stone(x, y, 60, 36)
    S.save('bigtree')


def waterfall():
    """自然の中に何か尊いもの: a waterfall falling into a green pool between mossy cliffs, mist and light"""
    S = Shot(804); p = S.p
    sky(S, 500, (540, 200, 300))
    fall = p.poly([(450, 330), (630, 330), (660, 1350), (420, 1350)])
    for side, pts in (('l', [(0, 300), (300, 260), (455, 330), (440, 900), (425, 1360), (0, 1360)]),
                      ('r', [(1080, 280), (760, 250), (625, 330), (640, 900), (655, 1360), (1080, 1360)])):
        m = p.poly(pts) * (1 - fall)
        p.form(m, ('stone', 'warmgrey', 'slate', 'umber'), p.flow(90, 20), LIGHT, length=(30, 70), density=1.5, seed=S.sd())
        p.leaves(m * (noise2d(H, W, 90, 2, S.sd()) > 0.55), ('yellowgreen', 'meadow', 'moss'), (10, 18), 1.0, seed=S.sd())
        p.edge(m, 'sepia', width=(1.6, 2.4), density=0.7, alpha=0.7)
    for x, h in ((120, 520), (960, 560), (300, 420)):
        p.tree(x, 300, h * 0.22, 90, colours=('meadow', 'moss', 'pine', 'forest'), clumps=5, seed=S.sd())
    p.hatch(fall, 90, ('white', 'powder', 'sky_pale', 'cream'), (60, 160), (1.6, 2.4), 2.0, 0.7, seed=S.sd())
    for k in range(10):
        x = 455 + k * 20
        p.line(curve([(x, 340), (x + 4 * np.sin(k), 800), (x + (x - 540) * 0.1, 1340)], 30), 'cornflower', 1.8, 0.6, alpha=0.5)
    pool = (p.YY > 1340).astype(np.float32)
    p.hatch(pool, p.flow(0, 4), ('water', p.value(0.25, 0.7, 1340, 1920)), (50, 130), (1.8, 2.5), 1.6, 0.7, seed=S.sd())
    bank = p.below([0, 300, 700, 1080], [1720, 1690, 1730, 1700])
    p.form(bank, ('meadow', 'yellowgreen', 'grass', 'moss'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    p.flowers(bank * (p.YY > 1780), n=40, size=(5, 9))
    p.lift(blur(p.ellipse(540, 1360, 380, 120), 30), 'white', 0.75)
    p.ripples(540, 1400, 160, 30, 4, 'white')
    for (x, y, r) in ((150, 1560, 110), (930, 1600, 130), (760, 1700, 80)):
        p.stone(x, y, r, r * 0.55, moss=('moss', 'lichen'))
    p.glow(540, 260, 260, strength=0.6, density=0.7)
    S.save('waterfall')


def pray():
    """その感覚、大切: a young woman in the grove, eyes closed, hands together; the sacred tree behind her"""
    S = Shot(805); p = S.p
    ARMS = [[(440, 1470), (425, 1590), (515, 1615)], [(640, 1470), (655, 1590), (565, 1615)]]
    w = person(S, 540, 1270, 140, coat=('sage', 'lichen', 'moss', 'pine'), hair_style='long', plan=True, arms=ARMS)
    sky(S, 1300, (860, 300, 360))
    ground(S, 1300, flowers=30)
    sacred_tree(S, 540, 1340, 130, 230, 290)
    shimenawa(S, 540, 820, 112, 32, 22, shide=3)
    p.lift(blur(w['mask'], 30) * (1 - w['mask']), 'cream', 0.35)
    erase(S, w['mask'])
    person(S, 540, 1270, 140, coat=('apricot', 'peach', 'coral', 'terracotta'), hair_style='long', eyes_closed=True, arms=ARMS, hands=False)
    gassho(S, 540, 1590, 1.0)
    S.save('pray')


def dawn():
    """造った方がいる (創世記1:1): the very first light -- the sun rising out of the sea, rays over the whole sky"""
    S = Shot(806); p = S.p
    m = (p.YY < 1100).astype(np.float32)
    v = p.value(0.0, 1.0, 0, 1100)
    p.hatch(m, p.flow(-3, 4), ('dusk_sky', np.clip(v * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.7, 0.74, seed=S.sd())
    for a in np.linspace(-150, -30, 9):
        r = np.deg2rad(a)
        ray = p.poly([(540, 1100), (540 + 1600 * np.cos(r - 0.05), 1100 + 1600 * np.sin(r - 0.05)), (540 + 1600 * np.cos(r + 0.05), 1100 + 1600 * np.sin(r + 0.05))])
        p.hatch(ray * m, a, ('glow', 'butter', 'cream'), (60, 160), (1.8, 2.4), 0.8, 0.6, opacity=0.6, alpha=0.35, seed=S.sd())
    clouds(S, [(200, 420, 300, 60), (880, 560, 280, 55), (640, 260, 220, 45)])
    p.glow(540, 1100, 460, strength=1.1, density=1.1)
    p.lift(p.ellipse(540, 1100, 120, 120) * (p.YY < 1100), 'white', 0.9)
    p.edge(p.ellipse(540, 1100, 120, 120) * (p.YY < 1100), 'apricot', width=(1.4, 2.0), density=0.6, alpha=0.5)
    water = (p.YY >= 1100).astype(np.float32)
    p.hatch(water, p.flow(0, 3), ('water', p.value(0.3, 0.0, 1100, 1920)), (60, 150), (1.8, 2.6), 1.9, 0.76, seed=S.sd())
    path = p.poly([(440, 1100), (640, 1100), (900, 1920), (180, 1920)])
    p.hatch(path, 0, ('glow', 'butter', 'cream', 'apricot'), (30, 90), (1.6, 2.2), 1.3, 0.72, opacity=0.6, alpha=0.7, seed=S.sd())
    for y in range(1130, 1920, 70):
        w = 60 + (y - 1100) * 0.4
        p.line([(540 - w, y), (540 + w, y)], 'white', 3, 0.7, alpha=0.5)
    S.save('dawn')


def easel():
    """きれいな絵の向こうに描いた人: a landscape painting on an easel, a painter's hand holding a brush to it"""
    S = Shot(807); p = S.p
    ari.room(S, np.zeros((H, W), np.float32), win_box=(760, 60, 1020, 380), wall_to=1330)
    p.form(p.rect(0, 1330, 1080, 1920), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    for (x0, y0, x1, y1) in ((300, 1130, 330, 1650), (760, 1130, 790, 1650), (525, 370, 555, 1590)):
        p.form(p.rect(x0, y0, x1, y1), ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.4, seed=S.sd())
    X0, Y0, X1, Y1 = 170, 430, 910, 1160
    frame = p.rect(X0 - 24, Y0 - 24, X1 + 24, Y1 + 24)
    erase(S, frame)
    p.form(frame, ('ochre', 'gold', 'sienna', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    cv = p.rect(X0, Y0, X1, Y1)
    p.hatch(cv * (p.YY < Y0 + 420), p.flow(-3, 4), ('day_sky', p.value(0.0, 1.0, Y0, Y0 + 400)), (30, 80), (1.8, 2.5), 1.6, 0.72, seed=S.sd())
    p.glow(760, Y0 + 300, 160, strength=0.9, density=0.9, clip=cv)
    xs = np.linspace(X0, X1, 7)
    for yy, c in (([790, 710, 660, 730, 700, 650, 710], RIDGES[0]), ([870, 830, 880, 810, 790, 850, 830], RIDGES[2]),
                  ([970, 950, 990, 960, 940, 970, 980], ('meadow', 'yellowgreen', 'grass', 'moss'))):
        p.form(p.below(xs, yy) * cv, c, p.flow(-6, 10), LIGHT, length=(20, 50), density=1.3, warm='peach', seed=S.sd())
    lake = p.rect(X0, 1010, X1, Y1) * cv
    p.hatch(lake, 0, ('water', p.value(0.35, 0.6, 1010, 1160)), (30, 80), (1.6, 2.2), 1.5, 0.72, seed=S.sd())
    p.flowers(p.rect(X0, 970, X1, 1010), n=30, size=(4, 7))
    p.edge(cv, 'sepia', width=(2, 3), density=1.0, alpha=0.8)
    arm = p.tube([(1120, 1560), (980, 1360), (870, 1230)], 95, 70)
    p.form(arm, ('powder', 'cornflower', 'denim', 'indigo'), p.contour(arm, 8, 90), LIGHT, length=(14, 30), density=1.4, seed=S.sd())
    p.edge(arm, 'sepia', width=(1.6, 2.4), density=0.9, alpha=0.8)
    hand = p.blob(810, 1170, 80, 64, 0.08, seed=S.sd(), rot=-35)
    erase(S, hand)
    p.form(hand, SKIN, p.contour(hand, 6), LIGHT, length=(8, 16), density=1.5, warm='peach', seed=S.sd())
    p.edge(hand, 'skin_shade', width=(1.4, 2.0), density=0.9, alpha=0.85)
    p.line([(870, 1240), (660, 970)], 'brown', 9, 0.85, alpha=0.95)
    p.line([(670, 983), (638, 942)], 'sienna', 7, 0.85, alpha=0.95)
    p.form(p.ellipse(630, 932, 11, 15, rot=-40), ('apricot', 'peach', 'coral'), 0, LIGHT, density=1.5, seed=S.sd())
    for k in range(3):
        p.line(curve([(770 + k * 28, 1150 + k * 6), (730 + k * 28, 1190 + k * 10)], 6), 'skin_shade', 1.8, 0.6, alpha=0.6)
    pal = p.ellipse(200, 1740, 140, 64)
    p.form(pal, ('sand', 'tan', 'sienna'), 0, LIGHT, density=1.4, seed=S.sd())
    for (x, y, c) in ((140, 1720, 'cobalt'), (190, 1705, 'sun'), (240, 1715, 'coral'), (280, 1745, 'meadow'), (170, 1765, 'white')):
        p.form(p.ellipse(x, y, 18, 12), (c, c, c), 0, LIGHT, density=1.6, seed=S.sd())
    S.save('easel')


def world():
    """この世界の美しさの向こうに (ローマ1:20): a wide valley -- mountains, a lake, meadows of flowers -- light from above"""
    S = Shot(808); p = S.p
    sky(S, 980, (540, 200, 420))
    for a in np.linspace(-115, -65, 5):
        r = np.deg2rad(a + 180)
        ray = p.poly([(540, 120), (540 - 1900 * np.cos(r - 0.04), 120 - 1900 * np.sin(r - 0.04)), (540 - 1900 * np.cos(r + 0.04), 120 - 1900 * np.sin(r + 0.04))])
        p.hatch(ray, a, ('butter', 'cream'), (60, 160), (1.8, 2.4), 0.7, 0.6, opacity=0.6, alpha=0.28, seed=S.sd())
    clouds(S, [(200, 420, 300, 60), (860, 360, 280, 55)])
    xs = np.linspace(0, 1080, 9)
    ridge(S, xs, [900, 760, 640, 720, 860, 700, 600, 700, 820], RIDGES[0], mist=0.5)
    snow = p.below(xs, [900, 760, 640, 720, 860, 700, 600, 700, 820]) * (p.YY < np.interp(p.XX, xs, [900, 760, 640, 720, 860, 700, 600, 700, 820]) + 50)
    p.lift(snow, 'white', 0.6)
    ridge(S, xs, [1060, 1000, 1040, 980, 1020, 1060, 990, 1030, 1070], RIDGES[2], mist=0.4)
    lake = p.poly([(0, 1150), (1080, 1130), (1080, 1330), (0, 1360)])
    ridge(S, xs, [1150, 1130, 1140, 1120, 1130, 1140, 1130, 1120, 1130], ('yellowgreen', 'meadow', 'grass', 'moss'), mist=0)
    p.hatch(lake, 0, ('water', p.value(0.3, 0.6, 1130, 1360)), (50, 120), (1.8, 2.4), 1.6, 0.72, seed=S.sd())
    p.lift(blur(p.rect(300, 1160, 800, 1200), 10), 'cream', 0.4)
    near = p.below([0, 300, 700, 1080], [1360, 1330, 1370, 1340])
    p.form(near, ('meadow', 'yellowgreen', 'grass', 'moss'), p.flow(-6, 12), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    p.flowers(near * (p.YY > 1450), n=160, size=(5, 10))
    for x, y, h in ((140, 1500, 360), (930, 1470, 400)):
        p.tree(x, y, h, 110, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    for (x, y) in ((420, 520), (455, 545), (490, 515)):
        p.line(curve([(x - 18, y), (x - 7, y - 9), (x, y - 2), (x + 7, y - 9), (x + 18, y)], 12), 'sepia', 2.4, 0.8, alpha=0.8)
    S.save('world')


def path_scene(S, y_h=1000):
    p = S.p
    sky(S, y_h + 40, (540, y_h - 80, 300))
    clouds(S, [(220, 340, 320, 70), (840, 260, 280, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [y_h - 60, y_h - 140, y_h - 90, y_h - 30, y_h - 110, y_h - 150, y_h - 70], RIDGES[0], mist=0.5)
    ground(S, y_h, flowers=120)
    road = p.poly([(510, y_h), (570, y_h), (820, 1920), (260, 1920)])
    p.form(road, ('sand', 'butter', 'tan', 'ochre'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.3, seed=S.sd())
    p.edge(road, 'tan', width=(1.4, 2.0), density=0.6, alpha=0.6)
    for x, y, h in ((120, y_h + 200, 380), (980, y_h + 160, 340)):
        p.tree(x, y, h, 100, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    return road


def walk():
    """遠くから見ているだけじゃない: someone walking alone, away from us, down a long country road"""
    S = Shot(809); p = S.p
    path_scene(S)
    figure(S, 545, 1380, 260, coat=('powder', 'cornflower', 'denim', 'indigo'), back=True, walk=0.6)
    p.form(p.ellipse(545, 1385, 70, 14), ('tan', 'sienna', 'sienna'), 0, LIGHT, density=0.8, seed=S.sd())
    S.save('walk')


def turn():
    """わたしはあなたの名を呼んだ: called by name, she turns round on the road -- facing us, eyes wide, in warm light"""
    S = Shot(810); p = S.p
    w = person(S, 540, 1080, 200, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='bob', plan=True)
    p0 = path_scene(S, 900)
    p.lift(blur(w['mask'], 40) * (1 - w['mask']), 'cream', 0.4)
    p.glow(540, 1180, 520, strength=0.5, density=0.6)
    erase(S, w['mask'])
    person(S, 540, 1080, 200, coat=('powder', 'cornflower', 'denim', 'indigo'), hair_style='bob', look=(0.0, 0.1), smile=True)
    for sgn in (-1, 1):                              # a little lift of surprise: brows
        ex = 540 + sgn * 68
        p.line(curve([(ex - 24, 1030), (ex, 1020), (ex + 24, 1030)], 10), 'umber', 2.4, 0.8, alpha=0.8)
    S.save('turn')


def father():
    """お父さんのような方: a father kneeling in the meadow, arms open, his child running into them"""
    S = Shot(811); p = S.p
    ARMS = [[(410, 1230), (260, 1270), (150, 1190)], [(670, 1230), (820, 1270), (930, 1190)]]
    f = person(S, 540, 960, 170, coat=('peach', 'coral', 'terracotta', 'brick'), hair_style='short', plan=True, arms=ARMS)
    sky(S, 1250, (540, 700, 520))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1150, 1060, 1100, 1040, 1090, 1120, 1060], RIDGES[0], mist=0.5)
    ground(S, 1250, flowers=140)
    p.lift(blur(f['mask'], 40) * (1 - f['mask']), 'cream', 0.4)
    erase(S, f['mask'])
    person(S, 540, 960, 170, coat=('peach', 'coral', 'terracotta', 'brick'), hair_style='short', arms=ARMS, smile=True,
           hair=('hair', 'umber', 'sepia'))
    figure(S, 540, 1880, 560, coat=('butter', 'sun', 'raincoat', 'amber'), back=True, walk=0.5, legs=('cornflower', 'denim', 'indigo'))
    S.save('father')


def lookup():
    """その向こうで名前を呼んでいる方: someone standing on a hill before the misty mountains, looking up into the light"""
    S = Shot(812); p = S.p
    sky(S, 1200, (640, 420, 460))
    p.lift(p.ellipse(640, 420, 80, 80), 'sun', 0.7)
    for a in np.linspace(-160, -20, 8):
        r = np.deg2rad(a)
        ray = p.poly([(640, 420), (640 + 1800 * np.cos(r - 0.04), 420 - 1800 * np.sin(r - 0.04) * -1), (640 + 1800 * np.cos(r + 0.04), 420 - 1800 * np.sin(r + 0.04) * -1)])
    clouds(S, [(200, 640, 300, 60), (900, 760, 260, 55)])
    xs = np.linspace(0, 1080, 9)
    ridge(S, xs, [1060, 980, 1020, 960, 900, 970, 1030, 980, 1010], RIDGES[0], mist=0.6)
    mist(S, 1150, 60, 0.6)
    ridge(S, xs, [1240, 1200, 1230, 1180, 1210, 1250, 1200, 1220, 1250], RIDGES[1], mist=0.6)
    mist(S, 1320, 60, 0.6)
    hill = p.below([0, 300, 600, 800, 1080], [1560, 1500, 1480, 1520, 1600])
    p.form(hill, ('meadow', 'yellowgreen', 'grass', 'moss'), p.flow(-6, 12), LIGHT, length=(30, 70), density=1.3, warm='butter', seed=S.sd())
    p.flowers(hill * (p.YY > 1620), n=80, size=(5, 9))
    p.grass(hill * (p.YY < 1600) * (p.YY > 1470))
    figure(S, 470, 1560, 330, coat=('cream', 'ivory', 'sand', 'tan'), hair=('hair', 'umber', 'sepia'), back=True, up=1.0)
    p.glow(640, 420, 200, strength=0.5, density=0.6)
    S.save('lookup')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
