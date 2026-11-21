"""「善悪の知識の木」 paintings for both parts (前編 / 後編). python3 shots.py NAME"""
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
erase, figure, sky, ground, ridge, RIDGES, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.SKIN4
gassho = k.gassho
COAT, HAIR = hj.SANGHEE, hj.HAIR
GARB = ('cream', 'ivory', 'sand', 'tan')
GARB2 = ('ivory', 'butter', 'sand', 'ochre')
HAIRD = ('hair', 'umber', 'sepia')


def dusk(S, y1, cols=('lavender', 'periwinkle', 'mauve'), low=('apricot', 'peach', 'butter')):
    p = S.p; m = (p.YY < y1).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), list(cols), (60, 150), (1.8, 2.5), 1.6, 0.66, seed=S.sd())
    p.hatch(m * p.value(0.0, 1.0, 0, y1), p.flow(-2, 4), list(low), (60, 140), (1.8, 2.4), 1.4, 0.66, alpha=0.75, seed=S.sd())


def night(S, y1):
    p = S.p; m = (p.YY < y1).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['indigo', 'ultramarine', 'slate'], (60, 150), (1.8, 2.6), 1.8, 0.8, seed=S.sd())
    p.hatch(m * p.value(0.0, 1.0, 0, y1), p.flow(-2, 4), ['violet', 'cobalt', 'periwinkle'], (60, 140), (1.8, 2.4), 1.0, 0.7, alpha=0.6, seed=S.sd())
    rr = np.random.default_rng(8)
    for _ in range(120):
        x, y = rr.uniform(20, 1060), rr.uniform(20, y1 - 60); p.lift(p.ellipse(x, y, rr.uniform(2, 5), rr.uniform(2, 5)), 'cream', rr.uniform(0.7, 1.0), tooth=0)


def fruit_tree(S, x, base, hgt, crown, fruit=('red', 'vermilion', 'brick'), n=16, glow=False, seed=1, cols=('meadow', 'moss', 'pine', 'forest')):
    p = S.p
    p.tree(x, base, hgt, crown, colours=cols, clumps=7, seed=S.sd())
    rr = np.random.default_rng(seed)
    cy = base - hgt - crown * 0.55
    for _ in range(n):
        a, r = rr.uniform(0, 2 * np.pi), rr.uniform(0.1, 0.85) * crown
        fx, fy = x + r * np.cos(a), cy + r * np.sin(a) * 0.75
        if glow: p.glow(fx, fy, 30, strength=0.8, density=0.8)
        p.form(p.ellipse(fx, fy, 14, 14), fruit, 0, LIGHT, density=1.6, seed=S.sd())
        if glow: p.lift(p.ellipse(fx - 4, fy - 4, 4, 4), 'white', 0.9, tooth=0)


def tamatebako():
    """開けてはいけない玉手箱: a young fisherman on the beach at dusk holding a closed lacquered box tied with a cord"""
    S = Shot(2901); p = S.p
    BOX = p.rect(400, 1100, 680, 1230)
    ARMS = [[(430, 1000), (400, 1110), (430, 1160)], [(650, 1000), (680, 1110), (650, 1160)]]
    w = person(S, 540, 780, 140, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='short', plan=True, arms=ARMS)
    dusk(S, 1000)
    sea = ((p.YY >= 900) & (p.YY < 1250)).astype(np.float32)
    p.hatch(sea, p.flow(0, 3), ['cornflower', 'periwinkle', 'powder'], (60, 150), (1.8, 2.6), 1.8, 0.74, avoid=w['mask'], seed=S.sd())
    p.glow(820, 900, 260, strength=1.1, density=1.0); p.lift(p.ellipse(820, 905, 60, 60) * (p.YY < 905), 'butter', 0.9, tooth=0)
    p.form((p.YY >= 1250).astype(np.float32), ('sand', 'cream', 'ochre', 'tan'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    for x0 in (120, 950): p.ripples(x0, 1240, 140, 14, 3, 'white')
    erase(S, w['mask'])
    person(S, 540, 780, 140, coat=('powder', 'cornflower', 'slate', 'indigo'), hair_style='short', hair=HAIRD, arms=ARMS, hands=False, smile=False, look=(0, 0.6))
    erase(S, BOX); p.form(BOX, ('sepia', 'umber', 'brick'), 0, LIGHT, density=1.7, seed=S.sd())
    lid = p.rect(392, 1090, 688, 1130); erase(S, lid); p.form(lid, ('brick', 'red', 'sepia'), 0, LIGHT, density=1.7, seed=S.sd())
    p.line([(540, 1090), (540, 1230)], 'vermilion', 8, 0.85, alpha=0.95); p.line([(400, 1165), (680, 1165)], 'vermilion', 8, 0.85, alpha=0.95)
    p.form(p.ellipse(540, 1165, 22, 16), ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    for x in (420, 660): p.form(p.ellipse(x, 1150, 30, 26), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('tamatebako')


def hataori():
    """のぞいてはいけない機織りの部屋: a closed sliding paper door, a thin line of light from the gap; a wooden floor"""
    S = Shot(2902); p = S.p
    wall = (p.YY < 1350).astype(np.float32)
    p.hatch(wall, p.flow(90, 4, 500), ['tan', 'sienna', 'brown'], (60, 140), (1.8, 2.5), 1.6, 0.66, seed=S.sd())
    fr = p.rect(180, 280, 900, 1350); erase(S, fr); p.form(fr, ('brown', 'umber', 'sepia'), 90, LIGHT, density=1.6, seed=S.sd())
    for (x0, x1) in ((210, 528), (552, 870)):
        pane = p.rect(x0, 310, x1, 1330); erase(S, pane)
        p.hatch(pane, 90, ['cream', 'ivory', 'butter'], (40, 90), (1.6, 2.2), 1.4, 0.6, seed=S.sd())
        p.glow((x0 + x1) / 2, 820, 260, strength=0.6, density=0.7, clip=pane)
        for x in np.linspace(x0, x1, 4): p.line([(x, 310), (x, 1330)], 'sepia', 5, 0.8, alpha=0.9)
        for y in np.linspace(310, 1330, 7): p.line([(x0, y), (x1, y)], 'sepia', 5, 0.8, alpha=0.9)
    gap = p.rect(528, 310, 552, 1330)
    p.lift(gap, 'white', 1.0, tooth=0); p.glow(540, 820, 360, strength=1.0, density=0.9)
    p.form((p.YY >= 1350).astype(np.float32), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.4, seed=S.sd())
    beam = p.poly([(528, 1350), (552, 1350), (700, 1920), (380, 1920)])
    p.lift(blur(beam, 20), 'butter', 0.6, tooth=0)
    for (x, y) in ((300, 1500), (330, 1530)):
        p.line(curve([(x, y), (x + 30, y - 14), (x + 70, y - 8)], 10), 'white', 5, 0.7, alpha=0.8)
    S.save('hataori')


def eden():
    """美しい園: a lush garden of fruit trees, a river, flowers and rabbits; a man and a woman in simple garments walking happily"""
    S = Shot(2903); p = S.p
    sky(S, 860, (540, 260, 380))
    clouds(S, [(200, 280, 300, 66), (880, 380, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [800, 740, 780, 720, 760, 790, 750], RIDGES[2], mist=0.5)
    ground(S, 860, flowers=220)
    river = p.poly(curve([(700, 860), (760, 1000), (600, 1200), (760, 1450), (980, 1920), (1080, 1920), (1080, 1700), (860, 1400), (760, 1200), (880, 980), (760, 860)], 80), smooth=True)
    p.hatch(river, p.flow(70, 4), ['powder', 'sky_pale', 'cornflower'], (40, 100), (1.7, 2.4), 1.7, 0.7, seed=S.sd())
    for (x, b, hh, cr, fr, sd) in ((130, 1000, 430, 140, ('red', 'vermilion', 'brick'), 1), (380, 900, 330, 110, ('tangerine', 'orange', 'amber'), 2),
                                   (960, 960, 400, 130, ('rose', 'pink', 'red'), 3), (560, 880, 280, 90, ('gold', 'amber', 'ochre'), 4)):
        fruit_tree(S, x, b, hh, cr, fruit=fr, n=12, seed=sd)
    for (x, y) in ((220, 1500), (880, 1620)):
        rb = np.clip(p.ellipse(x, y, 44, 30) + p.ellipse(x + 38, y - 24, 22, 20) + p.ellipse(x + 34, y - 58, 8, 24) + p.ellipse(x + 48, y - 56, 8, 24), 0, 1)
        erase(S, rb); p.form(rb, ('white', 'cream', 'stone'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(rb, 'warmgrey', density=0.8, alpha=0.7)
    figure(S, 430, 1520, 380, coat=GARB, hair=HAIRD, back=False, walk=0.4, legs=SKIN4[:3])
    figure(S, 600, 1530, 360, coat=GARB2, hair=HAIRD, back=False, walk=0.4, legs=SKIN4[:3])
    S.save('eden')


def tree_center():
    """ただ、ひとつだけ: one mysterious tree in the middle of the garden, its fruit softly glowing; the two look at it from afar"""
    S = Shot(2904); p = S.p
    sky(S, 980, (540, 380, 420))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [920, 870, 900, 850, 880, 910, 880], RIDGES[2], mist=0.6)
    ground(S, 980, flowers=120)
    p.glow(540, 620, 420, strength=0.9, density=0.9)
    fruit_tree(S, 540, 1080, 640, 230, fruit=('gold', 'amber', 'tangerine'), n=22, glow=True, seed=7, cols=('sage', 'moss', 'pine', 'forest'))
    for x in (90, 990): p.tree(x, 1000, 420, 130, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    figure(S, 470, 1660, 320, coat=GARB, hair=HAIRD, back=True, up=0.6, legs=SKIN4[:3])
    figure(S, 620, 1670, 300, coat=GARB2, hair=HAIRD, back=True, up=0.6, legs=SKIN4[:3])
    S.save('tree_center')


def apple():
    """りんごとは書いていない: one red apple with a leaf on cream paper"""
    S = Shot(2905); p = S.p
    p.hatch(np.ones((H, W), np.float32), p.flow(2, 4, 500), ['cream', 'ivory', 'apricot'], (60, 140), (1.8, 2.5), 1.4, 0.55, alpha=0.5, seed=S.sd())
    ap = np.clip(p.ellipse(480, 900, 200, 210) + p.ellipse(600, 900, 200, 210), 0, 1) * (1 - p.ellipse(540, 690, 60, 40))
    p.lift(blur(p.ellipse(560, 1130, 260, 40), 20), 'tan', 0.4)
    erase(S, ap); p.form(ap, ('red', 'vermilion', 'brick', 'brick'), p.contour(ap, 6), LIGHT, length=(14, 30), density=1.7, warm='tangerine', seed=S.sd())
    p.lift(p.ellipse(440, 820, 40, 70, rot=20), 'white', 0.45, tooth=0)
    p.line(curve([(540, 720), (550, 660), (570, 620)], 10), 'sepia', 10, 0.85, alpha=0.95)
    lf = p.ellipse(630, 640, 70, 30, rot=-25); p.form(lf, ('leaf', 'grass', 'moss', 'forest'), -25, LIGHT, density=1.6, seed=S.sd())
    p.edge(ap, 'brick', density=0.8, alpha=0.7)
    S.save('apple')


def fork():
    """自分で選べる存在: a person at a fork in the garden path -- one way toward a warm light, the other toward the single tree"""
    S = Shot(2906); p = S.p
    sky(S, 980, None)
    p.glow(260, 900, 360, strength=1.4, density=1.2)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [930, 900, 920, 890, 910, 930, 900], RIDGES[2], mist=0.6)
    ground(S, 980, flowers=140)
    fruit_tree(S, 840, 1000, 300, 100, fruit=('gold', 'amber', 'tangerine'), n=10, glow=True, seed=9, cols=('sage', 'moss', 'pine', 'forest'))
    trunk = p.poly([(470, 1920), (650, 1920), (590, 1330), (530, 1330)])
    left = p.poly([(530, 1340), (590, 1340), (300, 990), (250, 990)])
    right = p.poly([(530, 1340), (590, 1340), (860, 1000), (820, 1000)])
    pm = np.clip(trunk + left + right, 0, 1)
    p.form(pm, ('sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.2, seed=S.sd())
    p.lift(blur(left, 14), 'butter', 0.4)
    figure(S, 560, 1560, 340, coat=COAT, hair=HAIR, back=True, legs=('cornflower', 'denim', 'indigo'))
    S.save('fork')


def serpent():
    """神のようになれる: a shadowy serpent coiled on a branch of the single tree, whispering toward the woman; muted, not scary"""
    S = Shot(2907); p = S.p
    dusk(S, 1150, cols=('stone', 'lavender', 'warmgrey'), low=('peach', 'apricot', 'sand'))
    ground(S, 1150, cols=('sage', 'moss', 'olive', 'pine'), flowers=0)
    tr = p.poly([(130, 1400), (230, 1400), (210, 400), (160, 400)]); erase(S, tr)
    p.form(tr, ('brown', 'umber', 'sepia'), 90, LIGHT, density=1.6, seed=S.sd())
    br = p.tube([(190, 640), (420, 600), (640, 560)], 26, 16); erase(S, br); p.form(br, ('brown', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.leaves(p.blob(200, 380, 260, 200, 0.2), ('sage', 'moss', 'pine', 'forest'), size=(16, 30), density=1.3, seed=S.sd())
    for (fx, fy) in ((300, 430), (420, 520), (120, 470)):
        p.form(p.ellipse(fx, fy, 16, 16), ('gold', 'amber', 'tangerine'), 0, LIGHT, density=1.6, seed=S.sd())
    sn = p.tube(curve([(250, 610), (330, 570), (410, 610), (490, 560), (570, 590), (640, 540)], 40), 22, 14)
    erase(S, sn); p.form(sn, ('olive', 'moss', 'slate', 'umber'), 0, LIGHT, length=(10, 20), density=1.6, seed=S.sd()); p.edge(sn, 'sepia', density=0.8, alpha=0.8)
    hd = p.ellipse(660, 530, 34, 22, rot=-15); erase(S, hd); p.form(hd, ('olive', 'moss', 'slate'), 0, LIGHT, density=1.6, seed=S.sd())
    p.lift(p.ellipse(668, 524, 4, 4), 'sepia', 1.0, tooth=0)
    for q in range(3):
        p.line(curve([(710 + q * 30, 510 - q * 6), (725 + q * 30, 500 - q * 6), (740 + q * 30, 512 - q * 6)], 8), 'stone', 2.4, 0.6, alpha=0.6)
    w = person(S, 800, 900, 130, coat=GARB2, hair_style='long', plan=True)
    erase(S, w['mask'])
    person(S, 800, 900, 130, coat=GARB2, hair_style='long', hair=HAIRD, smile=False, look=(-0.6, -0.6))
    S.save('serpent')


def hiding():
    """神様から隠れる: the man and the woman hiding behind big leaves in the evening garden, ashamed and afraid"""
    S = Shot(2908); p = S.p
    dusk(S, 1000, cols=('slate', 'lavender', 'indigo'), low=('mauve', 'peach', 'apricot'))
    ground(S, 1000, cols=('moss', 'pine', 'olive', 'sage'), flowers=0)
    for x in (120, 960): p.tree(x, 1000, 520, 160, colours=('moss', 'pine', 'forest', 'sepia'), clumps=6, seed=S.sd())
    for (x, R, hs, c) in ((420, 120, 'short', GARB), (680, 115, 'long', GARB2)):
        w = person(S, x, 860, R, coat=c, hair_style=hs, plan=True); erase(S, w['mask'])
        person(S, x, 860, R, coat=c, hair_style=hs, hair=HAIRD, smile=False, look=(0.5 if x < 540 else -0.5, -0.3))
    rr = np.random.default_rng(12)
    for (x, y, rx, ry, rot) in ((250, 1140, 260, 130, -30), (560, 1180, 300, 150, 10), (850, 1130, 260, 130, 35), (430, 1060, 200, 90, -60), (700, 1050, 200, 90, 60)):
        lf = p.ellipse(x, y, rx, ry, rot=rot); erase(S, lf)
        p.form(lf, ('leaf', 'grass', 'moss', 'forest'), rot, LIGHT, length=(20, 50), density=1.6, seed=S.sd())
        p.line([(x - rx * 0.9 * np.cos(np.radians(rot)), y - rx * 0.9 * np.sin(np.radians(rot))), (x + rx * 0.9 * np.cos(np.radians(rot)), y + rx * 0.9 * np.sin(np.radians(rot)))], 'pine', 3, 0.8, alpha=0.8)
        p.edge(lf, 'pine', density=0.8, alpha=0.7)
    p.form((p.YY >= 1250).astype(np.float32), ('moss', 'pine', 'olive', 'sepia'), 0, LIGHT, density=1.4, seed=S.sd())
    S.save('hiding')


def generations():
    """すべての人に広がっていった: a long line of people through the generations walking away from a distant light, fading to grey"""
    S = Shot(2909); p = S.p
    m = (p.YY < 1000).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['stone', 'warmgrey', 'slate'], (60, 150), (1.8, 2.5), 1.6, 0.66, seed=S.sd())
    p.glow(930, 900, 260, strength=1.0, density=0.9)
    p.form((p.YY >= 1000).astype(np.float32), ('stone', 'warmgrey', 'pebble', 'slate'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    cols = [GARB2, ('apricot', 'peach', 'coral', 'terracotta'), ('sage', 'lichen', 'moss', 'pine'), ('powder', 'cornflower', 'slate', 'indigo'),
            ('stone', 'warmgrey', 'slate', 'umber'), ('stone', 'pebble', 'warmgrey', 'slate'), ('pebble', 'stone', 'warmgrey', 'slate')]
    for j, c in enumerate(cols):
        x = 820 - j * 120; y = 1080 + j * 70; hh = 170 + j * 30
        figure(S, x, y, hh, coat=c, hair=HAIRD, back=True, walk=0.5, legs=('stone', 'warmgrey', 'umber'))
    S.save('generations')


def searching():
    """隠れた人を、探しに来る: a warm gentle light moving through the evening garden among the trees, tender and quiet"""
    S = Shot(2910); p = S.p
    dusk(S, 1050, cols=('indigo', 'slate', 'violet'), low=('mauve', 'lavender', 'peach'))
    ground(S, 1050, cols=('moss', 'pine', 'olive', 'sepia'), flowers=0)
    for (x, b, hh, cr) in ((140, 1150, 700, 200), (430, 1080, 520, 150), (880, 1120, 680, 190), (650, 1060, 430, 120)):
        p.tree(x, b, hh, cr, colours=('pine', 'forest', 'moss', 'sepia'), clumps=6, seed=S.sd())
    p.glow(560, 1250, 420, strength=1.5, density=1.3)
    p.lift(blur(p.ellipse(560, 1250, 80, 110), 30), 'white', 0.8, tooth=0)
    p.lift(blur(p.ellipse(560, 1460, 360, 50), 20), 'butter', 0.6, tooth=0)
    S.save('searching')


def promise_light():
    """いつか、ひとりのかたが来て: a tiny warm light shining far away on the horizon of a dark land, like a promise"""
    S = Shot(2911); p = S.p
    night(S, 1000)
    p.form((p.YY >= 1000).astype(np.float32), ('indigo', 'slate', 'umber', 'sepia'), 0, LIGHT, length=(60, 140), density=1.5, seed=S.sd())
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [980, 940, 960, 930, 950, 970, 960], RIDGES[4], mist=0.0)
    p.glow(540, 960, 300, strength=1.6, density=1.3)
    p.lift(p.ellipse(540, 960, 12, 12), 'white', 1.0, tooth=0)
    S.save('promise_light')


def gethsemane():
    """わたしの願いではなく: a man kneeling in prayer among olive trees at night under the moon -- a silhouette"""
    S = Shot(2912); p = S.p
    night(S, 860)
    p.lift(p.ellipse(720, 600, 60, 60), 'cream', 1.0, tooth=0); p.glow(720, 600, 200, strength=0.9, density=0.8)
    p.form((p.YY >= 860).astype(np.float32), ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, length=(60, 140), density=1.5, seed=S.sd())
    for (x, b, hh, cr) in ((110, 1000, 230, 140), (990, 990, 250, 150)):
        p.tree(x, b, hh, cr, colours=('sage', 'lichen', 'slate', 'pine'), clumps=6, seed=S.sd())
    dy = -330
    rock = p.ellipse(700, 1440 + dy, 170, 90) * (p.YY < 1480 + dy); erase(S, rock); p.form(rock, ('stone', 'slate', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    body = p.poly(curve([(420, 1500 + dy), (400, 1360 + dy), (450, 1230 + dy), (520, 1200 + dy), (580, 1240 + dy), (600, 1360 + dy), (620, 1500 + dy)], 40), smooth=True)
    head = p.ellipse(560, 1150 + dy, 52, 58)
    arms = p.tube([(560, 1260 + dy), (630, 1330 + dy), (640, 1370 + dy)], 26, 22)
    sil = np.clip(body + head + arms, 0, 1); erase(S, sil)
    p.lift(sil, 'indigo', 0.85, tooth=0)
    p.form(sil, ('indigo', 'slate', 'umber', 'sepia'), 0, LIGHT, density=1.8, seed=S.sd())
    p.lift(blur(p.ellipse(590, 1120 + dy, 70, 60), 10) * head, 'periwinkle', 0.35)
    p.edge(sil, 'periwinkle', density=0.8, alpha=0.6)
    p.glow(560, 1000 + dy + 330 - 200, 260, strength=0.5, density=0.6)
    S.save('gethsemane')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
