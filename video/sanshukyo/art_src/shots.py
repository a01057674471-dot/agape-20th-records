"""「ユダヤ教・キリスト教・イスラム教、なにがちがう?」 paintings -- symbols only (no depiction of Muhammad, no people at the mosque).
python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *

def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), rel))
    m = importlib.util.module_from_spec(sp); sys.path.insert(0, os.path.dirname(sp.origin)); sp.loader.exec_module(m); return m
h = _load('h_shots', '../../handle/art_src/shots.py')
hj = _load('hj_shots', '../../hajimemashite/art_src/shots.py')
z = _load('z_shots', '../../zenaku1/art_src/shots.py')
k = h.k
import pcommon
pcommon.ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art')
erase, figure, sky, ground, ridge, RIDGES, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.SKIN4
COAT, HAIR = hj.SANGHEE, hj.HAIR
HAIRD = ('hair', 'umber', 'sepia')
dusk, night = z.dusk, z.night


def abraham():
    """アブラハム: an old man with a staff in simple robes in the desert at night, seen from behind, looking up at countless stars"""
    S = Shot(3501); p = S.p
    night(S, 1150)
    rr = np.random.default_rng(21)
    for _ in range(260):
        x, y = rr.uniform(10, 1070), rr.uniform(10, 1080); s_ = rr.uniform(2, 5)
        p.lift(p.ellipse(x, y, s_, s_), 'cream', rr.uniform(0.8, 1.0), tooth=0)
    for _ in range(18):
        x, y = rr.uniform(40, 1040), rr.uniform(40, 900); p.glow(x, y, 26, strength=0.7, density=0.7); p.lift(p.ellipse(x, y, 6, 6), 'white', 1.0, tooth=0)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1120, 1080, 1100, 1060, 1090, 1110, 1080], [('umber', 'sepia', 'indigo', 'slate')] [0], mist=0.0)
    p.form((p.YY >= 1150).astype(np.float32), ('ochre', 'tan', 'sienna', 'umber'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    for x0 in (120, 860):
        tn = p.poly([(x0 - 110, 1200), (x0, 1060), (x0 + 110, 1200)]); erase(S, tn); p.form(tn, ('sand', 'tan', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
    fm = figure(S, 520, 1660, 560, coat=('sand', 'tan', 'sienna', 'brown'), hair=('stone', 'warmgrey', 'white'), back=True, up=1.0, legs=('tan', 'sienna', 'umber'))
    p.line([(600, 1660), (640, 1100)], 'sepia', 9, 0.85, alpha=0.95)
    p.line(curve([(640, 1100), (660, 1075), (650, 1050)], 10), 'sepia', 9, 0.85, alpha=0.95)
    S.save('abraham')


def three_branches():
    """3つとも、神様はひとり: one great ancient tree whose strong trunk splits into three big branches; warm golden light"""
    S = Shot(3502); p = S.p
    sky(S, 1250, (540, 300, 420))
    ground(S, 1250, flowers=80)
    tr = p.poly([(470, 1300), (610, 1300), (580, 900), (500, 900)]); erase(S, tr)
    p.form(tr, ('brown', 'sienna', 'umber', 'sepia'), 90, LIGHT, length=(30, 60), density=1.6, seed=S.sd())
    for path in ([(530, 920), (380, 740), (230, 560)], [(540, 920), (540, 700), (540, 470)], [(550, 920), (700, 740), (850, 560)]):
        b = p.tube(path, 44, 24); erase(S, b); p.form(b, ('brown', 'sienna', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    for (cx, cy) in ((230, 500), (540, 400), (850, 500)):
        p.leaves(p.blob(cx, cy, 190, 150, 0.2), ('meadow', 'moss', 'pine', 'forest'), size=(16, 30), density=1.3, seed=S.sd())
    rt = p.poly([(400, 1320), (470, 1280), (610, 1280), (680, 1320)]); p.form(rt, ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('three_branches')


def scroll():
    """ユダヤ教: an old scroll partly unrolled on a wooden table beside a seven-branched lampstand in soft candlelight"""
    S = Shot(3503); p = S.p
    wall = (p.YY < 950).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sienna', 'umber', 'brick'], (60, 140), (1.8, 2.5), 1.7, 0.72, seed=S.sd())
    p.form((p.YY >= 950).astype(np.float32), ('sienna', 'brown', 'tan', 'umber'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', seed=S.sd())
    sh = p.rect(180, 1080, 900, 1300); erase(S, sh)
    p.hatch(sh, 0, ('cream', 'ivory', 'sand'), (30, 70), (1.6, 2.3), 1.5, 0.7, opacity=0.85, alpha=0.85, seed=S.sd())
    for x in np.arange(240, 860, 70):
        for q in range(6): p.line([(x, 1110 + q * 30), (x + 40, 1110 + q * 30)], 'pebble', 2.2, 0.6, alpha=0.6)
    for x in (180, 900):
        rl = p.ellipse(x, 1190, 50, 140); erase(S, rl); p.form(rl, ('cream', 'sand', 'tan'), 90, LIGHT, density=1.5, seed=S.sd())
        p.form(p.rect(x - 14, 1030, x + 14, 1350), ('brown', 'sienna', 'umber'), 90, LIGHT, density=1.6, seed=S.sd())
    cx, base = 540, 950
    stem = p.rect(cx - 12, 560, cx + 12, base); erase(S, stem); p.form(stem, ('gold', 'amber', 'ochre'), 90, LIGHT, density=1.6, seed=S.sd())
    p.form(p.poly([(cx - 90, base), (cx + 90, base), (cx + 40, base - 50), (cx - 40, base - 50)]), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    for j, r in enumerate((90, 180, 270)):
        arc = curve([(cx - r, 470), (cx - r, 560 + r * 0.6), (cx, 560 + r * 0.9), (cx + r, 560 + r * 0.6), (cx + r, 470)], 60)
        p.line([tuple(q) for q in arc], 'gold', 14, 0.85, alpha=0.95)
    for x in (cx - 270, cx - 180, cx - 90, cx, cx + 90, cx + 180, cx + 270):
        top = 470 if x != cx else 560 - 90
        p.form(p.rect(x - 16, top - 40, x + 16, top), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
        p.glow(x, top - 70, 60, strength=1.0, density=0.9)
        p.lift(p.blob(x, top - 62, 10, 22, 0.1), 'lemon', 1.0, tooth=0)
    S.save('scroll')


def mosque():
    """イスラム教: the silhouette of a mosque with a dome and a minaret against a soft sunset sky; peaceful, no people"""
    S = Shot(3504); p = S.p
    dusk(S, 1250, cols=('lavender', 'mauve', 'periwinkle'), low=('tangerine', 'apricot', 'butter'))
    p.glow(540, 1150, 420, strength=1.2, density=1.0)
    SIL = ('umber', 'sepia', 'indigo')
    body = p.rect(220, 900, 860, 1250)
    dome = p.ellipse(540, 900, 220, 230) * (p.YY < 900)
    dtop = p.poly([(530, 650), (550, 650), (545, 600), (535, 600)])
    smalld = np.clip(p.ellipse(320, 900, 90, 90) * (p.YY < 900) + p.ellipse(760, 900, 90, 90) * (p.YY < 900), 0, 1)
    mn = p.rect(925, 520, 975, 1250); mtop = p.poly([(915, 520), (950, 420), (985, 520)])
    gal = p.rect(905, 760, 995, 790)
    m = np.clip(body + dome + dtop + smalld + mn + mtop + gal, 0, 1); erase(S, m)
    p.form(m, SIL, 0, LIGHT, density=1.8, seed=S.sd())
    for x in np.linspace(280, 800, 6):
        ar = np.clip(p.rect(x - 26, 1010, x + 26, 1120) + p.ellipse(x, 1010, 26, 26), 0, 1)
        p.lift(ar, 'butter', 0.55, tooth=0)
    p.form((p.YY >= 1250).astype(np.float32), ('ochre', 'tan', 'sienna', 'umber'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    S.save('mosque')


def three_roads():
    """まったくちがう: a person standing where one path splits into three roads under a wide sky"""
    S = Shot(3505); p = S.p
    sky(S, 1000, (540, 760, 360))
    clouds(S, [(200, 260, 300, 66), (860, 360, 260, 60)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [960, 920, 940, 910, 930, 960, 930], RIDGES[0], mist=0.6)
    ground(S, 1000, flowers=120)
    trunk = p.poly([(470, 1920), (650, 1920), (590, 1380), (530, 1380)])
    roads = [p.poly([(530, 1390), (590, 1390), (210, 1000), (170, 1000)]), p.poly([(540, 1390), (580, 1390), (562, 1000), (548, 1000)]),
             p.poly([(530, 1390), (590, 1390), (920, 1000), (880, 1000)])]
    pm = np.clip(trunk + sum(roads), 0, 1)
    p.form(pm, ('sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.2, seed=S.sd())
    figure(S, 560, 1600, 340, coat=COAT, hair=HAIR, back=True, up=0.3, legs=('cornflower', 'denim', 'indigo'))
    S.save('three_roads')


def look_ahead():
    """私たちひとりひとりに: the young woman looking straight ahead, thoughtful and open, soft warm light on her face"""
    S = Shot(3506); p = S.p
    w = person(S, 540, 820, 190, coat=COAT, hair_style='long', plan=True)
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['cream', 'apricot', 'peach'], (60, 140), (1.8, 2.5), 1.5, 0.6, avoid=w['mask'], seed=S.sd())
    p.glow(760, 520, 520, strength=1.2, density=1.0)
    erase(S, w['mask'])
    person(S, 540, 820, 190, coat=COAT, hair_style='long', hair=HAIR, smile=True)
    p.lift(blur(w['head'] * smoothstep(500, 700, p.XX), 30), 'butter', 0.3)
    S.save('look_ahead')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
