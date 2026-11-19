"""「祈りって、なに?」 paintings -- prayer as a conversation: speaking, and listening. python3 shots.py NAME"""
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
gassho, torii = k.gassho, k.ari.torii
COAT, HAIR = hj.SANGHEE, hj.HAIR


def shrine_pray():
    """神社で手を合わせる: the young woman before a small quiet shrine, eyes closed, hands together; a torii behind, morning light"""
    S = Shot(2601); p = S.p
    ARMS = [[(447, 1046), (433, 1157), (517, 1180)], [(633, 1046), (647, 1157), (563, 1180)]]
    w = person(S, 540, 860, 130, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    sky(S, 1100, (820, 300, 360))
    clouds(S, [(200, 260, 300, 70), (900, 470, 240, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1020, 960, 1000, 940, 980, 1010, 970], RIDGES[2], mist=0.5)
    ground(S, 1100, cols=('sand', 'cream', 'stone', 'tan'), flowers=0)
    for x, y, hh in ((110, 1120, 560), (970, 1120, 600)):
        p.tree(x, y, hh, 140, colours=('meadow', 'moss', 'pine', 'forest'), clumps=7, seed=S.sd())
    torii(S, 540, 1110, 800, 620, avoid=w['mask'])
    p.lift(blur(w['mask'], 30) * (1 - w['mask']), 'cream', 0.35)
    erase(S, w['mask'])
    person(S, 540, 860, 130, coat=COAT, hair_style='long', hair=HAIR, eyes_closed=True, arms=ARMS, hands=False)
    gassho(S, 540, 1157, 0.93)
    S.save('shrine_pray')


def tea_light():
    """祈りは、会話: the young woman at a little table, talking with a warm gentle light sitting across from her, two cups of tea"""
    S = Shot(2602); p = S.p
    table = p.rect(0, 1300, 1080, 1920)
    SA = [[(330, 1080), (360, 1230), (450, 1300)]]
    s = person(S, 300, 830, 140, coat=COAT, hair_style='long', plan=True, arms=SA, cut=table)
    hj.room(S, np.clip(s['mask'] + table, 0, 1), win_box=(400, 150, 720, 600), wall_to=1300)
    for kk in range(4):
        p.glow(790, 960, 330 - kk * 50, strength=0.9, density=0.9)
    p.lift(blur(p.ellipse(790, 960, 150, 220), 40), 'white', 0.55, tooth=0)
    p.lift(blur(p.ellipse(790, 960, 70, 110), 20), 'white', 0.8, tooth=0)
    person(S, 300, 830, 140, coat=COAT, hair_style='long', hair=HAIR, arms=SA, cut=table, smile=True, look=(0.7, 0.1))
    p.form(table, ('cream', 'sand', 'tan', 'sienna'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', avoid=s['mask'], seed=S.sd())
    p.line([(0, 1302), (1080, 1302)], 'tan', 5, 0.8, alpha=0.8)
    for (x, c) in ((420, ('cream', 'powder', 'cornflower')), (720, ('cream', 'peach', 'apricot'))):
        cupm = np.clip(p.poly(curve([(x - 70, 1420), (x - 62, 1520), (x, 1545), (x + 62, 1520), (x + 70, 1420)], 30)) + p.ellipse(x, 1420, 70, 20), 0, 1)
        p.form(cupm, c, 90, LIGHT, density=1.4, seed=S.sd())
        p.form(p.ellipse(x, 1420, 58, 14), ('yellowgreen', 'sage', 'moss'), 0, LIGHT, density=1.3, seed=S.sd())
        p.strokes([curve([(x - 10, 1395), (x - 25, 1330), (x, 1270)], 20)], 'white', width=6.0, pressure=0.55, opacity=0.8, alpha=0.5)
    p.glow(790, 1500, 300, strength=0.5, density=0.6)
    S.save('tea_light')


def samuel():
    """しもべは、聞いております: a young boy in simple old clothes sitting up on his mat at night beside an oil lamp, listening"""
    S = Shot(2603); p = S.p
    wall = (p.YY < 1250).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['indigo', 'slate', 'violet'], (60, 140), (1.8, 2.5), 1.7, 0.75, seed=S.sd())
    p.hatch(wall * p.value(0.0, 1.0, 0, 1250), p.flow(-2, 4), ['periwinkle', 'lavender'], (60, 140), (1.8, 2.4), 0.8, 0.65, alpha=0.5, seed=S.sd())
    win = p.rect(640, 180, 920, 560)                 # a small high opening, the moon and stars outside
    erase(S, win); p.hatch(win, p.flow(-3, 4), ['ultramarine', 'indigo', 'cobalt'], (40, 100), (1.7, 2.3), 1.6, 0.75, seed=S.sd())
    p.lift(p.ellipse(820, 290, 46, 46), 'cream', 1.0, tooth=0); p.glow(820, 290, 90, strength=0.6, density=0.6)
    rr = np.random.default_rng(4)
    for _ in range(16):
        x, y = rr.uniform(660, 900), rr.uniform(200, 540); p.lift(p.ellipse(x, y, 3, 3), 'cream', 0.9, tooth=0)
    for x in (640, 920): p.line([(x, 180), (x, 560)], 'umber', 10, 0.8, alpha=0.9)
    for y in (180, 560): p.line([(640, y), (920, y)], 'umber', 10, 0.8, alpha=0.9)
    beam = p.poly([(640, 560), (920, 560), (760, 1500), (300, 1500)])
    p.hatch(beam, 70, ['periwinkle', 'cream'], (60, 140), (1.8, 2.4), 0.7, 0.6, opacity=0.5, alpha=0.3, seed=S.sd())
    floor = (p.YY >= 1250).astype(np.float32)
    p.form(floor, ('sand', 'tan', 'sienna', 'umber'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    mat = p.poly(curve([(150, 1420), (900, 1400), (980, 1600), (100, 1640)], 30))
    p.form(mat, ('cream', 'sand', 'ochre', 'tan'), 0, LIGHT, length=(30, 60), density=1.4, seed=S.sd())
    ARMS = [[(470, 1250), (450, 1380), (520, 1430)], [(650, 1250), (670, 1380), (600, 1430)]]
    b = person(S, 560, 1060, 110, coat=('cream', 'ivory', 'sand', 'tan'), hair_style='short', plan=True, arms=ARMS)
    blanket = p.poly(curve([(300, 1400), (560, 1360), (860, 1400), (900, 1560), (560, 1600), (260, 1560)], 40), smooth=True)
    erase(S, b['mask'])
    person(S, 560, 1060, 110, coat=('cream', 'ivory', 'sand', 'tan'), hair_style='short', hair=('hair', 'umber', 'sepia'), arms=ARMS,
           smile=True, look=(0.3, -0.5))
    erase(S, blanket); p.form(blanket, ('apricot', 'terracotta', 'sienna', 'brick'), 0, LIGHT, length=(30, 60), density=1.4, seed=S.sd())
    p.edge(blanket, 'sepia', density=0.8, alpha=0.8)
    lamp = p.poly(curve([(150, 1330), (190, 1300), (260, 1300), (300, 1330), (260, 1360), (180, 1360)], 30), smooth=True)
    erase(S, lamp); p.form(lamp, ('ochre', 'sienna', 'terracotta', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    p.glow(300, 1250, 340, strength=1.2, density=1.1)
    p.lift(p.blob(305, 1270, 16, 36, 0.1), 'lemon', 1.0, tooth=0); p.lift(p.ellipse(305, 1285, 7, 16), 'white', 1.0, tooth=0)
    S.save('samuel')


def _wall(S, gap):
    p = S.p
    sky(S, 950, (540, 220, 380))
    p.glow(540, 220, 560, strength=1.2, density=1.1)
    ground(S, 950, flowers=60)
    top = 330
    wall = p.rect(0, top, 1080, 1000)
    hole = p.poly([(540 - gap, 1000), (540 - gap * 0.9, top - 10), (540 + gap * 0.9, top - 10), (540 + gap, 1000)]) if gap else np.zeros((H, W), np.float32)
    wm = wall * (1 - hole)
    erase(S, wm)
    p.form(wm, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, length=(30, 70), density=1.5, cool='lavender', seed=S.sd())
    rr = np.random.default_rng(9)
    for row, y in enumerate(range(top + 70, 1000, 90)):
        p.line([(0, y), (1080, y)], 'umber', 3, 0.7, alpha=0.55)
        for x in np.arange((row % 2) * 70, 1080, 140):
            p.line([(x, y - 90), (x, y)], 'umber', 2.6, 0.7, alpha=0.5)
    p.edge(wm, 'sepia', density=0.9, alpha=0.8)
    return wm, hole


def wall():
    """自分の力では立てない: a small person standing before a tall wall; a warm light glows beyond it, out of reach"""
    S = Shot(2605); p = S.p
    wm, _ = _wall(S, 0)
    p.lift(blur(p.rect(0, 290, 1080, 350), 30), 'butter', 0.6)
    figure(S, 540, 1150, 300, coat=COAT, hair=HAIR, back=True, up=0.6, legs=('cornflower', 'denim', 'indigo'))
    S.save('wall')


def wall_open():
    """十字架で、その道を開いてくれた: the wall opened in the middle; a glowing path through it to a far cross on a hill"""
    S = Shot(2606); p = S.p
    wm, hole = _wall(S, 190)
    hill = p.ellipse(540, 960, 300, 100) * hole
    p.form(hill, ('yellowgreen', 'meadow', 'moss', 'sage'), 0, LIGHT, density=1.4, seed=S.sd())
    p.glow(540, 600, 300, strength=1.6, density=1.3, clip=hole)
    for seg in (p.rect(532, 640, 548, 880), p.rect(492, 700, 588, 715)):
        erase(S, seg); p.form(seg, ('sepia', 'umber', 'brown'), 90, LIGHT, density=1.6, seed=S.sd())
    path = p.poly([(525, 880), (555, 880), (860, 1920), (220, 1920)])
    p.form(path, ('butter', 'lemon', 'sand', 'ochre'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.3, seed=S.sd())
    p.lift(blur(path * smoothstep(1700, 880, p.YY), 12), 'butter', 0.5)
    p.dots(hole * (p.YY < 880), ('white', 'cream', 'butter'), n=60, size=(2, 4))
    figure(S, 560, 1180, 280, coat=COAT, hair=HAIR, back=True, up=0.4, walk=0.6, legs=('cornflower', 'denim', 'indigo'))
    S.save('wall_open')


def night_listen():
    """耳をすませてみませんか: the young woman by the window at night, eyes closed, calm, a soft lamp glow around her"""
    S = Shot(2607); p = S.p
    ARMS = [[(420, 1180), (400, 1330), (510, 1360)], [(660, 1180), (680, 1330), (570, 1360)]]
    w = person(S, 540, 930, 170, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    m = (p.YY < 1500).astype(np.float32) * (1 - w['mask'])
    p.hatch(m, p.flow(-3, 4), ['indigo', 'ultramarine', 'slate'], (60, 150), (1.8, 2.6), 1.8, 0.8, seed=S.sd())
    p.hatch(m * p.value(0.0, 1.0, 0, 1500), p.flow(-2, 4), ['violet', 'cobalt', 'periwinkle'], (60, 140), (1.8, 2.4), 1.0, 0.7, alpha=0.6, seed=S.sd())
    rr = np.random.default_rng(7)
    for _ in range(200):
        x, y = rr.uniform(20, 1060), rr.uniform(20, 1100)
        if w['mask'][int(y), int(x)] > 0.1: continue
        p.lift(p.ellipse(x, y, rr.uniform(2.5, 5.5), rr.uniform(2.5, 5.5)), 'cream', rr.uniform(0.8, 1.0), tooth=0.0)
    p.lift(p.ellipse(860, 260, 60, 60), 'cream', 1.0, tooth=0); p.glow(860, 260, 140, strength=0.7, density=0.7)
    sill = p.rect(0, 1500, 1080, 1600)
    p.form(sill, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.4, seed=S.sd())
    p.form(p.rect(0, 1600, 1080, 1920), ('terracotta', 'sienna', 'brown', 'umber'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    for x in (40, 1040):
        p.form(p.rect(x - 40, 0, x + 40, 1500), ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.3, seed=S.sd())
    p.glow(540, 1000, 520, strength=0.9, density=0.9)
    erase(S, w['mask'])
    person(S, 540, 930, 170, coat=COAT, hair_style='long', hair=HAIR, eyes_closed=True, arms=ARMS, hands=False, smile=True)
    gassho(S, 540, 1290, 1.2)
    S.save('night_listen')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
