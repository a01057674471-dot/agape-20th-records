"""「救いって、だれのためのもの?」 paintings. python3 shots.py NAME"""
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
COAT, HAIR = hj.SANGHEE, hj.HAIR
HAIRD = ('hair', 'umber', 'sepia')
ROBE_J = ('white', 'cream', 'ivory', 'sand')


def old_book():
    """善人なおもて…: an old Japanese book open on a wooden desk, blurred vertical brush lines, soft lamp light"""
    S = Shot(3001); p = S.p
    wall = (p.YY < 860).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sand', 'tan', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    desk = (p.YY >= 860).astype(np.float32)
    p.form(desk, ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', seed=S.sd())
    for kk in range(8): p.line(curve([(0, 920 + kk * 130), (540, 926 + kk * 130), (1080, 918 + kk * 130)], 30), 'umber', 2.0, 0.5, alpha=0.4)
    L_ = p.poly([(120, 1050), (535, 1020), (535, 1560), (100, 1600)])
    R_ = p.poly([(545, 1020), (960, 1050), (980, 1600), (545, 1560)])
    for mm in (L_, R_):
        erase(S, mm); p.hatch(mm, 90, ('cream', 'ivory', 'sand'), (20, 50), (1.6, 2.3), 1.5, 0.7, opacity=0.85, alpha=0.85, seed=S.sd())
    p.line([(540, 1020), (540, 1560)], 'tan', 4, 0.8, alpha=0.85)
    rr = np.random.default_rng(2)
    for x0, x1 in ((150, 500), (580, 940)):
        for x in np.arange(x1 - 30, x0, -48):
            y = 1080 + rr.uniform(0, 20)
            while y < 1520:
                L2 = rr.uniform(14, 34); p.line([(x + rr.uniform(-4, 4), y), (x + rr.uniform(-4, 4), y + L2)], 'sepia', 4.0, 0.75, alpha=0.55); y += L2 + rr.uniform(6, 16)
    p.form(p.rect(80, 1590, 1000, 1640), ('indigo', 'slate', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    lamp = p.poly(curve([(800, 560), (880, 520), (960, 560), (940, 860), (820, 860)], 30), smooth=True)
    erase(S, lamp); p.form(lamp, ('cream', 'ivory', 'butter'), 90, LIGHT, density=1.3, seed=S.sd())
    p.glow(880, 700, 420, strength=1.3, density=1.1)
    p.glow(540, 1300, 360, strength=0.5, density=0.6)
    S.save('old_book')


def feast():
    """罪人を招くため: Jesus in simple robes at a table with outcasts and poor people, laughing together, lamp light"""
    S = Shot(3002); p = S.p
    table = p.rect(0, 1180, 1080, 1920)
    ppl = [(170, 800, 105, ('stone', 'warmgrey', 'slate', 'umber'), 'short'), (390, 740, 115, ('olive', 'moss', 'sage', 'pine'), 'bob'),
           (690, 740, 115, ROBE_J, 'long'), (910, 800, 105, ('brick', 'terracotta', 'sienna', 'brown'), 'bun')]
    masks = [person(S, x, y, R, coat=c, hair_style=hs, plan=True, cut=table)['mask'] for (x, y, R, c, hs) in ppl]
    fg = np.clip(sum(masks) + table, 0, 1)
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sand', 'tan', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.62, avoid=fg, seed=S.sd())
    p.glow(540, 380, 360, strength=1.2, density=1.1)
    p.lift(p.ellipse(540, 380, 30, 40), 'lemon', 1.0, tooth=0)
    p.line([(540, 0), (540, 340)], 'umber', 4, 0.8, alpha=0.8)
    p.glow(690, 700, 300, strength=0.7, density=0.7)
    for (x, y, R, c, hs), m in zip(ppl, masks):
        erase(S, m)
        person(S, x, y, R, coat=c, hair_style=hs, hair=HAIRD, cut=table, smile=True, eyes_closed=True)
    p.form(table, ('sienna', 'brown', 'tan', 'umber'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', seed=S.sd())
    p.line([(0, 1182), (1080, 1182)], 'umber', 5, 0.8, alpha=0.8)
    for (x, y) in ((300, 1300), (540, 1340), (780, 1300)):
        br = p.ellipse(x, y, 90, 40); erase(S, br); p.form(br, ('ochre', 'tan', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
    for x in (150, 930):
        cup = p.poly([(x - 40, 1250), (x + 40, 1250), (x + 30, 1340), (x - 30, 1340)]); erase(S, cup); p.form(cup, ('stone', 'warmgrey', 'umber'), 90, LIGHT, density=1.5, seed=S.sd())
    S.save('feast')


def thief():
    """わたしを、思い出してください: a man in a dark sky turning his face toward a soft light, full of hope; no injuries"""
    S = Shot(3003); p = S.p
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(-3, 4), ['slate', 'indigo', 'warmgrey'], (60, 150), (1.8, 2.5), 1.8, 0.74, seed=S.sd())
    p.glow(1000, 600, 520, strength=1.4, density=1.2)
    w = person(S, 440, 760, 180, coat=('stone', 'warmgrey', 'umber', 'sepia'), hair_style='short', plan=True)
    erase(S, w['mask'])
    person(S, 440, 760, 180, coat=('stone', 'warmgrey', 'umber', 'sepia'), hair_style='short', hair=HAIRD, smile=False, look=(0.9, -0.3))
    p.lift(blur(w['mask'] * smoothstep(400, 640, p.XX), 20), 'butter', 0.35)
    S.save('thief')


def breakthrough():
    """パラダイスにいます: soft golden light breaking through dark clouds over the hill"""
    S = Shot(3004); p = S.p
    m = (p.YY < 1250).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['slate', 'stone', 'lavender'], (60, 150), (1.8, 2.5), 1.6, 0.7, seed=S.sd())
    rr = np.random.default_rng(3)
    for (cx, cy, rw, rh) in ((180, 300, 330, 120), (900, 260, 360, 130), (540, 160, 420, 110), (300, 560, 260, 90), (820, 600, 300, 100)):
        cm = cloud_mask(p, cx, cy, rw, rh, rr); p.form(cm, ('slate', 'stone', 'warmgrey', 'indigo'), 0, LIGHT, density=1.4, seed=S.sd())
    rays = np.zeros((H, W), np.float32)
    for a in np.linspace(-0.5, 0.5, 7):
        rays = np.maximum(rays, p.poly([(540, 420), (540 + 2000 * np.sin(a) - 60, 420 + 2000 * np.cos(a)), (540 + 2000 * np.sin(a) + 60, 420 + 2000 * np.cos(a))]))
    p.lift(blur(rays * (p.YY < 1300), 30), 'butter', 0.55, tooth=0)
    p.glow(540, 420, 420, strength=1.6, density=1.3)
    hill = p.ellipse(540, 1500, 900, 300)
    p.form(np.clip(hill + (p.YY >= 1500), 0, 1), ('moss', 'sage', 'olive', 'pine'), 0, LIGHT, density=1.4, seed=S.sd())
    p.lift(blur(hill * (p.YY < 1350), 20), 'butter', 0.4)
    S.save('breakthrough')


def gavel():
    """神様は、正しいかた: a judge's wooden gavel resting on a desk beside an open book; warm, serious light"""
    S = Shot(3005); p = S.p
    wall = (p.YY < 900).astype(np.float32)
    p.hatch(wall, p.flow(90, 4, 500), ['brown', 'sienna', 'umber'], (60, 140), (1.8, 2.5), 1.6, 0.7, seed=S.sd())
    for x in range(60, 1080, 160): p.line([(x, 0), (x, 900)], 'sepia', 3, 0.6, alpha=0.5)
    desk = (p.YY >= 900).astype(np.float32)
    p.form(desk, ('sienna', 'brown', 'tan', 'umber'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', seed=S.sd())
    L_ = p.poly(curve([(90, 1000), (260, 960), (450, 990), (450, 1340), (260, 1310), (70, 1350)], 50), smooth=True)
    R_ = p.poly(curve([(460, 990), (650, 960), (820, 1000), (840, 1350), (650, 1310), (460, 1340)], 50), smooth=True)
    for mm, x0 in ((L_, 110), (R_, 490)):
        erase(S, mm); p.hatch(mm, 90, ('white', 'cream', 'ivory'), (20, 50), (1.6, 2.3), 1.5, 0.7, opacity=0.85, alpha=0.85, seed=S.sd())
        for kk in range(10): p.line([(x0, 1030 + kk * 28), (x0 + 300, 1032 + kk * 28)], 'pebble', 2.2, 0.7, alpha=0.65)
    base = p.ellipse(800, 1520, 190, 50); erase(S, base); p.form(base, ('brown', 'sienna', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(p.rect(610, 1470, 990, 1520), ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    handle_ = p.poly([(400, 1430), (720, 1350), (730, 1380), (410, 1460)]); erase(S, handle_)
    p.form(handle_, ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.6, seed=S.sd())
    head = p.poly([(690, 1250), (790, 1225), (840, 1450), (740, 1475)]); erase(S, head)
    p.form(head, ('sienna', 'brown', 'umber', 'sepia'), 75, LIGHT, density=1.7, seed=S.sd())
    for t_ in (0.18, 0.82): p.line([(690 + 100 * t_, 1250 - 25 * t_ + 0), (740 + 100 * t_, 1475 - 25 * t_)], 'gold', 6, 0.85, alpha=0.9)
    p.glow(540, 700, 520, strength=0.8, density=0.8)
    S.save('gavel')


def wrapped():
    """正しいまま、ゆるす: a cross on a hill in golden light; beneath it a person kneeling, wrapped in a soft white cloth"""
    S = Shot(3006); p = S.p
    sky(S, 1150, None)
    p.glow(540, 420, 560, strength=1.5, density=1.3)
    for seg in (p.rect(520, 220, 560, 760), p.rect(420, 330, 660, 370)):
        erase(S, seg); p.form(seg, ('sepia', 'umber', 'brown'), 90, LIGHT, density=1.7, seed=S.sd())
    hill = p.ellipse(540, 1250, 800, 480)
    p.form(np.clip(hill + (p.YY >= 1250), 0, 1), ('yellowgreen', 'meadow', 'moss', 'sage'), 0, LIGHT, density=1.4, seed=S.sd())
    p.lift(blur(p.ellipse(540, 800, 300, 80), 30), 'butter', 0.5)
    ox, oy = 190, 140
    body = p.poly(curve([(400 + ox, 1120 + oy), (385 + ox, 990 + oy), (440 + ox, 880 + oy), (540 + ox, 850 + oy), (640 + ox, 880 + oy),
                         (695 + ox, 990 + oy), (680 + ox, 1120 + oy)], 40), smooth=True)
    head = p.ellipse(540 + ox, 815 + oy, 52, 58)
    p.lift(blur(p.ellipse(540 + ox, 1120 + oy, 200, 30), 12), 'moss', 0.5)
    erase(S, np.clip(body + head, 0, 1))
    p.form(head, ('hair', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(body, ('white', 'cream', 'ivory', 'stone'), p.contour(body, 6), LIGHT, length=(20, 40), density=1.6, seed=S.sd())
    for q in range(5):
        p.line(curve([(410 + ox + q * 10, 900 + oy + q * 45), (540 + ox, 880 + oy + q * 50), (680 + ox - q * 10, 900 + oy + q * 45)], 20), 'stone', 2.6, 0.6, alpha=0.5)
    p.edge(body, 'warmgrey', density=0.8, alpha=0.6)
    p.lift(blur(body, 24) * (1 - body), 'butter', 0.5)
    p.flowers(hill * (p.YY > 1150), kinds=('daisy', 'buttercup'), n=40, size=(7, 11))
    S.save('wrapped')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
