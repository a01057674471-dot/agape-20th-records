"""「聖書が語る天国って、どんなところ?」 paintings. python3 shots.py NAME"""
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
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4, heart_mask = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4, h.heart_mask
COAT, HAIR = hj.SANGHEE, hj.HAIR
COATS = [('powder', 'cornflower', 'denim', 'indigo'), ('butter', 'ochre', 'amber', 'sienna'), ('sage', 'lichen', 'moss', 'pine'),
         ('lavender', 'periwinkle', 'violet', 'indigo'), ('pink', 'rose', 'coral', 'brick'), ('sand', 'tan', 'sienna', 'brown'),
         ('cream', 'ivory', 'sand', 'tan'), ('stone', 'warmgrey', 'slate', 'umber')]
HAIRS = [('hair', 'umber', 'sepia'), ('hair_light', 'hair', 'umber'), ('umber', 'sepia', 'sepia'), ('stone', 'warmgrey', 'pebble')]


def bust(S, x, y, R, coat, hs='short', hair=HAIRS[0], **kw):
    m = person(S, x, y, R, coat=coat, hair_style=hs, plan=True, arms=kw.get('arms'))
    erase(S, m['mask'])
    person(S, x, y, R, coat=coat, hair_style=hs, hair=hair, **kw)
    return m['mask']


def farewell():
    """天国で見守っていてね: a simple farewell -- white flowers, a small framed photo; she stands quietly, hands together"""
    S = Shot(2301); p = S.p
    wall = (p.YY < 1350).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'ivory', 'stone'], (60, 140), (1.8, 2.5), 1.6, 0.6, alpha=0.65, seed=S.sd())
    p.form(p.rect(0, 1350, 1080, 1920), ('stone', 'warmgrey', 'sand', 'pebble'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    alt = p.rect(240, 620, 840, 760); erase(S, alt); p.form(alt, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(alt, 'warmgrey', density=0.8, alpha=0.7)
    fr = p.rect(450, 300, 630, 520); ph = p.rect(468, 318, 612, 502)
    erase(S, fr); p.form(fr * (1 - ph), ('sepia', 'umber', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(ph, ('cream', 'sand', 'butter'), 0, LIGHT, density=1.2, seed=S.sd())
    p.form(p.ellipse(540, 390, 36, 40) * ph, ('sand', 'tan', 'tan'), 0, LIGHT, density=1.0, seed=S.sd())
    p.form(p.ellipse(540, 480, 60, 40) * ph, ('stone', 'warmgrey', 'warmgrey'), 0, LIGHT, density=1.0, seed=S.sd())
    for (x, y) in ((300, 560), (380, 520), (700, 520), (780, 560), (340, 470), (740, 470)):
        p.flowers(p.blob(x, y, 60, 50, 0.2, seed=S.sd()), kinds=('daisy',), n=10, size=(10, 15))
        p.leaves(p.blob(x, y + 40, 50, 30, 0.2, seed=S.sd()), ('sage', 'moss', 'pine'), (8, 14), 1.0, seed=S.sd())
    ARMS = [[(450, 1160), (430, 1270), (520, 1300)], [(630, 1160), (650, 1270), (560, 1300)]]
    m = person(S, 540, 900, 150, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='long', plan=True, arms=ARMS)
    erase(S, m['mask'])
    person(S, 540, 900, 150, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='long', hair=HAIR, arms=ARMS, hands=False, eyes_closed=True, smile=False)
    k.ari.gassho(S, 540, 1270, 0.9)
    p.glow(540, 400, 300, strength=0.5, density=0.5)
    S.save('farewell')


def cliche(erased=False):
    """雲の上、お花畑、天使とハープ -- the usual dreamy heaven, pastel and faded like an old picture book;
    erased=True: the same picture being rubbed out like a pencil sketch, warm golden light left behind"""
    S = Shot(2302); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-3, 4), ['sky_pale', 'powder', 'lavender', 'pink'], (60, 150), (1.8, 2.5), 1.4, 0.55, seed=S.sd())
    clouds(S, [(220, 300, 360, 90), (820, 240, 320, 80), (540, 520, 420, 90), (180, 760, 300, 80), (900, 820, 320, 80)])
    for (cx, cy, w_, h_) in ((540, 1250, 900, 260), (200, 1450, 500, 200), (880, 1460, 500, 200)):
        cm = k.cloud_mask(p, cx, cy, w_, h_, np.random.default_rng(int(cx)))
        p.form(cm, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.2, seed=S.sd()); p.edge(cm, 'periwinkle', density=0.8, alpha=0.6)
    fl = p.blob(540, 1300, 380, 90, 0.2, seed=4)
    p.form(fl, ('meadow', 'yellowgreen', 'sage'), 0, LIGHT, density=1.2, seed=S.sd())
    p.flowers(fl, kinds=('daisy', 'buttercup', 'poppy', 'forgetmenot'), n=60, size=(6, 10))
    hp = np.clip(p.tube(curve([(430, 1220), (420, 1000), (480, 920), (560, 960)], 30), 14, 14) + p.tube([(430, 1220), (580, 1200)], 14, 14), 0, 1)
    p.form(hp, ('butter', 'gold', 'amber'), 0, LIGHT, density=1.5, seed=S.sd())
    for q in range(5): p.line([(450 + q * 24, 1000 + q * 6), (450 + q * 24, 1200)], 'stone', 1.6, 0.7, alpha=0.8)
    for (x, y) in ((780, 900), (280, 820)):
        b = p.ellipse(x, y, 60, 80); erase(S, b); p.form(b, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(b, 'stone', density=0.8, alpha=0.7)
        hd = p.ellipse(x, y - 110, 44, 44); erase(S, hd); p.form(hd, SKIN, 0, LIGHT, density=1.3, seed=S.sd())
        p.form(p.ellipse(x, y - 130, 46, 28) * (p.YY < y - 120), ('hair_light', 'butter', 'ochre'), 0, LIGHT, density=1.4, seed=S.sd())
        for sgn in (-1, 1):
            wg = p.ellipse(x + sgn * 84, y - 20, 54, 32, rot=sgn * 30); p.form(wg, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(wg, 'stone', density=0.8, alpha=0.7)
        t = np.linspace(0, 2 * np.pi, 30); p.line(np.stack([x + 40 * np.cos(t), y - 176 + 10 * np.sin(t)], 1), 'gold', 4, 0.8, alpha=0.9)
    p.lift(np.ones((H, W), np.float32), 'cream', 0.07)                       # faded like an old book
    if erased:
        band = smoothstep(0.0, 1.0, (p.XX * 0.6 + (H - p.YY) * 0.4 - 380) / 500)
        p.lift(blur(band, 30), 'paper', 0.92, tooth=0.6)
        rr = np.random.default_rng(9)
        for _ in range(26):
            x, y = rr.uniform(150, 950), rr.uniform(300, 1500)
            p.line(curve([(x, y), (x + 60, y - 20), (x + 120, y + 10)], 12), 'stone', 2.0, 0.5, alpha=0.25)
        p.glow(700, 700, 520, strength=1.2, density=1.1)
    S.save('cliche_erased' if erased else 'cliche')


def cliche_heaven(): cliche(False)
def cliche_erased(): cliche(True)


def presence():
    """ともに住んでくださる: people of all ages gathered in peace, everyone turned toward a warm light in the middle"""
    S = Shot(2303); p = S.p
    sky(S, 1000, (540, 600, 460))
    ground(S, 1000, flowers=120)
    p.glow(540, 760, 420, strength=1.6, density=1.3)
    p.lift(blur(p.ellipse(540, 760, 120, 120), 30), 'white', 0.9)
    spots = [(150, 1200, 260, 0), (330, 1150, 240, 1), (750, 1150, 240, 2), (930, 1200, 260, 3),
             (230, 1480, 320, 4), (480, 1520, 300, 5), (700, 1500, 330, 6), (900, 1500, 310, 7)]
    for (x, y, hh, c) in spots:
        figure(S, x, y, hh, coat=COATS[c], hair=HAIRS[c % 4], back=True, up=0.4)
    S.save('presence')


def tear_wipe():
    """涙をぬぐい取って: close on a crying face; a gentle hand of light softly wipes the tear from her cheek"""
    S = Shot(2304); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-10, 6), ['lavender', 'peach', 'cream'], (60, 150), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.glow(820, 700, 600, strength=1.0, density=1.0)
    ARMS = None
    m = person(S, 470, 820, 230, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='long', plan=True)
    erase(S, m['mask'])
    person(S, 470, 820, 230, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='long', hair=HAIR, eyes_closed=True, smile=False)
    for x in (400, 545):
        tr = p.blob(x, 900, 9, 18, 0.05); p.lift(tr, 'sky_pale', 0.9, tooth=0); p.edge(tr, 'cornflower', density=0.8, alpha=0.7)
    sl = p.tube([(1200, 360), (980, 600), (820, 820)], 120, 90)
    p.lift(blur(sl, 10), 'butter', 0.7)
    hm = hand(S, 720, 890, 1.5, 200, cols=('butter', 'glow', 'cream', 'apricot'), curl=0.3, paint=False)
    erase(S, hm); p.form(hm, ('butter', 'cream', 'lemon', 'apricot'), p.contour(hm, 6, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
    p.edge(hm, 'gold', density=0.8, alpha=0.7)
    p.glow(700, 880, 200, strength=1.0, density=1.0)
    S.save('tear_wipe')


def new_earth():
    """すべてが新しくされる: a renewed earth -- a clear river, fruit trees, green hills, people walking and laughing under a bright sky"""
    S = Shot(2305); p = S.p
    sky(S, 760, (800, 260, 360))
    clouds(S, [(220, 300, 300, 70), (900, 200, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [740, 680, 710, 660, 700, 730, 690], RIDGES[2], mist=0.3)
    ground(S, 760, flowers=200)
    river = p.poly(curve([(500, 760), (560, 760), (680, 1000), (560, 1300), (760, 1920), (360, 1920), (330, 1300), (500, 1000), (500, 760)], 100), smooth=True)
    p.hatch(river, 0, ('water', p.value(0.6, 0.2, 760, 1920)), (40, 100), (1.8, 2.4), 1.6, 0.72, seed=S.sd())
    for y in range(820, 1900, 70): p.lift(p.ellipse(540 + 60 * np.sin(y / 120), y, 40, 3), 'white', 0.7)
    for (x, y, hh) in ((150, 1000, 300), (900, 960, 320), (220, 1420, 380), (920, 1400, 360)):
        p.tree(x, y, hh, 120, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
        for q in range(6):
            a = q * 1.05; p.form(p.ellipse(x + 70 * np.cos(a), y - hh * 0.8 + 50 * np.sin(a), 14, 14), ('coral', 'red', 'tangerine'), 0, LIGHT, density=1.6, seed=S.sd())
    for (x, y, hh, c) in ((300, 1700, 300, 4), (420, 1720, 260, 1), (760, 1680, 300, 0), (880, 1720, 270, 2)):
        figure(S, x, y, hh, coat=COATS[c], hair=HAIRS[c % 4], back=False, walk=0.3)
    S.save('new_earth')


def house_door():
    """場所を用意しに行く: a large warm house with many rooms, its front door a little open, golden light inside"""
    S = Shot(2306); p = S.p
    sky(S, 1300, (850, 300, 360))
    ground(S, 1300, flowers=100)
    body = p.rect(140, 600, 940, 1320)
    erase(S, body); p.form(body, ('cream', 'ivory', 'sand', 'tan'), 90, LIGHT, length=(30, 70), density=1.4, seed=S.sd()); p.edge(body, 'sepia', density=0.8, alpha=0.8)
    rf = p.poly([(100, 620), (540, 330), (980, 620)]); erase(S, rf); p.form(rf, ('brick', 'terracotta', 'sienna', 'brown'), 0, LIGHT, density=1.6, seed=S.sd())
    for r in range(2):
        for c in range(4):
            x = 200 + c * 190; y = 700 + r * 220
            if r == 1 and c in (1, 2): continue
            p.window(x, y, x + 110, y + 140, panes=(2, 2), glow=0.85, seed=S.sd())
    door = p.rect(440, 1000, 640, 1320)
    p.form(door, ('butter', 'glow', 'lemon', 'amber'), 0, LIGHT, density=1.3, seed=S.sd())
    p.glow(540, 1160, 300, strength=1.2, density=1.1)
    leaf = p.poly([(440, 1000), (520, 1020), (520, 1340), (440, 1320)]); erase(S, leaf); p.form(leaf, ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    path = p.poly([(470, 1320), (610, 1320), (760, 1920), (320, 1920)]); p.form(path, ('butter', 'sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, density=1.2, seed=S.sd())
    p.lift(blur(path * smoothstep(1700, 1320, p.YY), 10), 'butter', 0.5)
    S.save('house_door')


def morning_walk():
    """もう始まっています: the young woman walking a morning path; a warm gentle light walks beside her"""
    S = Shot(2307); p = S.p
    sky(S, 1000, (540, 900, 420))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [960, 910, 940, 890, 920, 950, 910], RIDGES[0], mist=0.5)
    ground(S, 1000, flowers=160)
    road = p.poly([(500, 1000), (580, 1000), (840, 1920), (240, 1920)]); p.form(road, ('butter', 'sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, density=1.2, seed=S.sd())
    figure(S, 440, 1600, 420, coat=COAT, hair=HAIR, back=False, walk=0.4)
    p.glow(680, 1380, 230, strength=1.4, density=1.2)
    p.lift(blur(p.ellipse(680, 1380, 90, 200), 20), 'white', 0.8)
    for x in (400, 480): pass
    S.save('morning_walk')


def open_door():
    """扉は、開いています: the young woman before a wide open door full of warm light, about to step forward"""
    S = Shot(2308); p = S.p
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['stone', 'lavender', 'cream'], (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.7, seed=S.sd())
    op = p.rect(270, 300, 810, 1500)
    erase(S, op); p.form(op, ('butter', 'glow', 'lemon', 'cream'), 0, LIGHT, density=1.2, seed=S.sd())
    p.glow(540, 900, 700, strength=1.6, density=1.3)
    p.lift(blur(op, 20), 'white', 0.6)
    for x0, x1 in ((230, 270), (810, 850)):
        p.form(p.rect(x0, 280, x1, 1520), ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.5, seed=S.sd())
    p.form(p.rect(230, 260, 850, 300), ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    dl = p.poly([(810, 300), (1000, 220), (1000, 1600), (810, 1500)]); erase(S, dl); p.form(dl, ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(dl, 'sepia', density=0.8, alpha=0.8)
    p.form(p.rect(0, 1500, 1080, 1920), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    p.lift(blur(p.poly([(270, 1500), (810, 1500), (1000, 1920), (80, 1920)]), 20), 'butter', 0.6)
    figure(S, 540, 1680, 520, coat=COAT, hair=HAIR, back=True, walk=0.25, legs=('cornflower', 'denim', 'indigo'))
    S.save('open_door')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
