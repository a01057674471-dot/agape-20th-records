"""「神様は、なぜその木を置いたの?」 amusement-park paintings (mother and child). python3 shots.py NAME"""
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
HAIRD = ('hair', 'umber', 'sepia')
MOM = ('rose', 'pink', 'coral', 'brick')
KID = ('butter', 'sun', 'amber', 'ochre')
LEGS = ('cornflower', 'denim', 'indigo')


def dusk(S, y1):
    p = S.p; m = (p.YY < y1).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['violet', 'lavender', 'mauve'], (60, 150), (1.8, 2.5), 1.6, 0.68, seed=S.sd())
    p.hatch(m * p.value(0.0, 1.0, 0, y1), p.flow(-2, 4), ['tangerine', 'apricot', 'peach'], (60, 140), (1.8, 2.4), 1.4, 0.66, alpha=0.75, seed=S.sd())


def ferris(S, cx, cy, r, lit=False):
    p = S.p
    ring = np.clip(p.ellipse(cx, cy, r, r) - p.ellipse(cx, cy, r - 14, r - 14), 0, 1)
    p.form(ring, ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.4, seed=S.sd())
    for a in np.linspace(0, np.pi, 7)[:-1]:
        p.line([(cx - r * np.cos(a), cy - r * np.sin(a)), (cx + r * np.cos(a), cy + r * np.sin(a))], 'warmgrey', 3, 0.7, alpha=0.7)
    for leg in (-1, 1): p.line([(cx, cy), (cx + leg * r * 0.55, cy + r * 1.25)], 'slate', 8, 0.8, alpha=0.85)
    cols = [('coral', 'red', 'brick'), ('butter', 'gold', 'amber'), ('powder', 'cornflower', 'cobalt'), ('yellowgreen', 'meadow', 'moss')]
    for j, a in enumerate(np.linspace(0, 2 * np.pi, 13)[:-1]):
        gx, gy = cx + r * np.cos(a), cy + r * np.sin(a) + 30
        g = p.ellipse(gx, gy, 26, 24); erase(S, g); p.form(g, cols[j % 4], 0, LIGHT, density=1.5, seed=S.sd())
        if lit: p.glow(gx, gy, 40, strength=0.6, density=0.6)
    p.form(p.ellipse(cx, cy, 24, 24), ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())


def tent(S, cx, base, w, hgt, lit=False):
    p = S.p
    body = p.rect(cx - w / 2, base - hgt * 0.55, cx + w / 2, base); erase(S, body)
    p.form(body, ('cream', 'ivory', 'sand'), 90, LIGHT, density=1.4, seed=S.sd())
    roof = p.poly([(cx - w / 2 - 30, base - hgt * 0.55), (cx, base - hgt), (cx + w / 2 + 30, base - hgt * 0.55)]); erase(S, roof)
    p.form(roof, ('red', 'vermilion', 'coral'), 0, LIGHT, density=1.5, seed=S.sd())
    for q in np.linspace(-0.8, 0.8, 5):
        p.line([(cx, base - hgt), (cx + q * (w / 2 + 30), base - hgt * 0.55)], 'cream', 10, 0.8, alpha=0.85)
    p.line([(cx, base - hgt), (cx, base - hgt - 40)], 'umber', 4, 0.8, alpha=0.9)
    p.form(p.poly([(cx, base - hgt - 40), (cx + 40, base - hgt - 30), (cx, base - hgt - 20)]), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.5, seed=S.sd())
    if lit:
        for x in np.linspace(cx - w / 2, cx + w / 2, 7): p.glow(x, base - hgt * 0.55 + 10, 26, strength=0.7, density=0.7)


def bulbs(S, pts, n=14):
    p = S.p
    path = np.array(curve(pts, n * 4))
    for x, y in path[::4]:
        p.glow(x, y, 34, strength=0.8, density=0.8); p.lift(p.ellipse(x, y, 6, 6), 'lemon', 1.0, tooth=0)
    p.line([tuple(q) for q in path], 'umber', 2, 0.6, alpha=0.5)


def park_bg(S, y_ground=1100, evening=False):
    p = S.p
    if evening: dusk(S, y_ground)
    else:
        sky(S, y_ground, (200, 260, 300)); clouds(S, [(300, 220, 280, 60), (880, 340, 240, 56)])
    ferris(S, 790, 560, 280, lit=evening)
    tent(S, 230, y_ground - 10, 300, 420, lit=evening)
    p.form((p.YY >= y_ground).astype(np.float32), ('sand', 'cream', 'tan', 'ochre') if not evening else ('tan', 'sienna', 'stone', 'umber'),
           0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())


def park_gate():
    """ぜんぶ乗っていいよ: a mother kneeling and smiling at her small child at the entrance of a generic amusement park"""
    S = Shot(3201); p = S.p
    MA = [[(350, 1010), (390, 1100), (470, 1120)], [(510, 1010), (560, 1080), (600, 1080)]]
    m = person(S, 430, 840, 120, coat=MOM, hair_style='bun', plan=True, arms=MA)
    c = person(S, 680, 1000, 80, coat=KID, hair_style='bob', plan=True)
    park_bg(S)
    gate = np.clip(p.rect(60, 560, 120, 1100) + p.rect(960, 560, 1020, 1100) + p.poly(curve([(60, 600), (540, 470), (1020, 600), (1020, 650), (540, 520), (60, 650)], 40)), 0, 1)
    gate = gate * (1 - np.clip(m['mask'] + c['mask'], 0, 1))
    erase(S, gate); p.form(gate, ('apricot', 'coral', 'terracotta'), 0, LIGHT, density=1.5, seed=S.sd())
    for x in np.linspace(140, 940, 9): p.form(p.ellipse(x, 600 - 110 * np.sin(np.pi * (x - 60) / 960) + 30, 18, 18), ('butter', 'gold', 'amber'), 0, LIGHT, density=1.5, seed=S.sd())
    for mm in (m['mask'], c['mask']): erase(S, mm)
    person(S, 430, 840, 120, coat=MOM, hair_style='bun', hair=HAIRD, arms=MA, smile=True, look=(0.6, 0.4))
    person(S, 680, 1000, 80, coat=KID, hair_style='bob', hair=HAIRD, smile=True, look=(-0.6, -0.4))
    for x, y in ((150, 1300), (950, 1350)):
        st = p.ellipse(x, y, 30, 30); bl = p.ellipse(x, y - 230, 60, 70)
        p.line([(x, y), (x, y - 160)], 'warmgrey', 2, 0.6, alpha=0.6)
    for (bx, by, col) in ((870, 820, ('red', 'vermilion', 'coral')), (930, 760, ('powder', 'cornflower', 'cobalt'))):
        p.line([(bx, by + 60), (680 + 40, 1060)], 'warmgrey', 2, 0.6, alpha=0.6)
        b = p.ellipse(bx, by, 44, 54); erase(S, b); p.form(b, col, 0, LIGHT, density=1.5, seed=S.sd()); p.lift(p.ellipse(bx - 14, by - 18, 8, 12), 'white', 0.8, tooth=0)
    S.save('park_gate')


def pinky():
    """ひとつだけ、約束ね: mother and child hooking little fingers to make a promise; the park soft behind them"""
    S = Shot(3202); p = S.p
    MA = [[(360, 1020), (430, 1120), (515, 1130)]]
    CA = [[(720, 1110), (650, 1140), (565, 1135)]]
    m = person(S, 320, 780, 140, coat=MOM, hair_style='bun', plan=True, arms=MA)
    c = person(S, 770, 900, 100, coat=KID, hair_style='bob', plan=True, arms=CA)
    park_bg(S)
    p.lift(blur(np.ones((H, W), np.float32) * (p.YY < 1100), 2), 'cream', 0.35)
    for mm in (m['mask'], c['mask']): erase(S, mm)
    person(S, 320, 780, 140, coat=MOM, hair_style='bun', hair=HAIRD, arms=MA, smile=True, look=(0.6, 0.3), hands=False)
    person(S, 770, 900, 100, coat=KID, hair_style='bob', hair=HAIRD, arms=CA, smile=True, look=(-0.6, -0.2), hands=False)
    for (x, y, r) in ((520, 1132, 34), (566, 1136, 28)):
        p.form(p.ellipse(x, y, r, r * 0.9), SKIN4, 0, LIGHT, density=1.6, seed=S.sd()); p.edge(p.ellipse(x, y, r, r * 0.9), 'skin_shade', density=0.8)
    p.line(curve([(538, 1104), (546, 1092), (556, 1100), (548, 1112)], 16), 'skin_shade', 5, 0.85, alpha=0.95)
    p.glow(545, 1110, 120, strength=0.7, density=0.7)
    S.save('pinky')


def horse(S, x, y, s, cols=('white', 'cream', 'ivory', 'stone')):
    p = S.p
    body = p.ellipse(x, y, 90 * s, 46 * s); neck = p.poly([(x + 50 * s, y - 20 * s), (x + 90 * s, y - 100 * s), (x + 120 * s, y - 90 * s), (x + 90 * s, y)])
    head = p.ellipse(x + 125 * s, y - 100 * s, 40 * s, 24 * s, rot=20)
    legs = sum(p.tube([(x + dx * s, y + 30 * s), (x + dx * s + 10 * s, y + 110 * s)], 10 * s, 8 * s) for dx in (-60, -30, 40, 70))
    m = np.clip(body + neck + head + legs, 0, 1); erase(S, m); p.form(m, cols, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(m, 'warmgrey', density=0.8, alpha=0.7)
    p.form(p.poly([(x + 60 * s, y - 40 * s), (x + 95 * s, y - 110 * s), (x + 80 * s, y - 115 * s), (x + 45 * s, y - 45 * s)]), ('ochre', 'amber', 'tan'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.rect(x - 40 * s, y - 50 * s, x + 20 * s, y - 36 * s), ('red', 'brick', 'vermilion'), 0, LIGHT, density=1.6, seed=S.sd())
    return m


def carousel():
    """子どもを、愛しているから: a happy child riding a carousel horse, laughing; the mother waving from nearby"""
    S = Shot(3203); p = S.p
    sky(S, 1250, (540, 200, 300))
    p.form((p.YY >= 1250).astype(np.float32), ('sand', 'cream', 'tan'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    canopy = p.poly([(80, 520), (540, 260), (1000, 520), (1000, 580), (80, 580)]); erase(S, canopy)
    p.form(canopy, ('red', 'vermilion', 'coral'), 0, LIGHT, density=1.5, seed=S.sd())
    for q in np.linspace(-0.85, 0.85, 7): p.line([(540, 260), (540 + q * 460, 520)], 'cream', 14, 0.8, alpha=0.85)
    p.form(p.rect(80, 520, 1000, 580), ('butter', 'gold', 'amber'), 0, LIGHT, density=1.5, seed=S.sd())
    for x in np.linspace(110, 970, 10): p.glow(x, 590, 24, strength=0.7, density=0.7)
    plat = p.rect(60, 1150, 1020, 1220); erase(S, plat); p.form(plat, ('cream', 'sand', 'tan'), 0, LIGHT, density=1.4, seed=S.sd())
    for x in (230, 540, 850): p.line([(x, 580), (x, 1150)], 'gold', 8, 0.85, alpha=0.95)
    horse(S, 150, 980, 0.9, cols=('powder', 'sky_pale', 'cream', 'stone'))
    horse(S, 760, 1000, 0.9, cols=('pink', 'rose', 'cream', 'stone'))
    horse(S, 460, 900, 1.1)
    CA = [[(470, 790), (520, 700), (535, 640)]]
    c = person(S, 470, 640, 78, coat=KID, hair_style='bob', plan=True, arms=CA)
    erase(S, c['mask'] * (p.YY < 900))
    person(S, 470, 640, 78, coat=KID, hair_style='bob', hair=HAIRD, arms=CA, smile=True, cut=(p.YY > 880).astype(np.float32))
    MA = [[(930, 1330), (1000, 1230), (1020, 1150)]]
    m = person(S, 900, 1130, 110, coat=MOM, hair_style='bun', plan=True, arms=MA); erase(S, m['mask'])
    person(S, 900, 1130, 110, coat=MOM, hair_style='bun', hair=HAIRD, arms=MA, smile=True, look=(-0.6, -0.4))
    S.save('carousel')


def hand_in_hand():
    """お母さんが言うなら、大丈夫: a small child holding the mother's hand tightly, walking with a trusting smile through the park"""
    S = Shot(3204); p = S.p
    park_bg(S, 1150)
    bulbs(S, [(0, 300), (300, 380), (540, 340), (800, 400), (1080, 320)])
    figure(S, 440, 1720, 760, coat=MOM, hair=HAIRD, back=False, walk=0.3, legs=LEGS)
    figure(S, 690, 1740, 440, coat=KID, hair=HAIRD, back=False, walk=0.3, legs=('cornflower', 'denim', 'indigo'))
    hold = p.tube([(560, 1270), (600, 1340), (630, 1390)], 22, 18); erase(S, hold); p.form(hold, SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(605, 1360, 28, 24), SKIN4, 0, LIGHT, density=1.6, seed=S.sd()); p.edge(p.ellipse(605, 1360, 28, 24), 'skin_shade', density=0.8)
    S.save('hand_in_hand')


def lost_child():
    """ついて行ってしまいました: a small child walking away alone into a crowd at dusk, the lights growing dim; lonely"""
    S = Shot(3205); p = S.p
    park_bg(S, 1100, evening=True)
    p.lift(blur(np.ones((H, W), np.float32), 1), 'slate', 0.25)
    rr = np.random.default_rng(5)
    for j in range(9):
        x = rr.uniform(80, 1000); y = rr.uniform(1150, 1350); hh = rr.uniform(300, 420)
        figure(S, x, y, hh, coat=('stone', 'warmgrey', 'slate', 'umber'), hair=HAIRD, back=True, legs=('stone', 'warmgrey', 'umber'))
    figure(S, 560, 1560, 300, coat=KID, hair=HAIRD, back=True, walk=0.5, legs=LEGS)
    S.save('lost_child')


def searching_mom():
    """あなたは、どこにいるのか: the mother searching anxiously through the dusk crowd, a hand to her mouth, lanterns lighting up"""
    S = Shot(3206); p = S.p
    park_bg(S, 1150, evening=True)
    bulbs(S, [(0, 380), (280, 460), (540, 420), (800, 480), (1080, 400)])
    rr = np.random.default_rng(9)
    for j in range(6):
        x = [90, 250, 840, 990, 150, 930][j]; y = 1250 + (j // 4) * 150; hh = 380
        figure(S, x, y, hh, coat=('stone', 'warmgrey', 'slate', 'umber'), hair=HAIRD, back=True, legs=('stone', 'warmgrey', 'umber'))
    MA = [[(460, 1050), (430, 960), (500, 880)], [(640, 1050), (670, 1180), (640, 1260)]]
    m = person(S, 540, 780, 130, coat=MOM, hair_style='bun', plan=True, arms=MA); erase(S, m['mask'])
    person(S, 540, 780, 130, coat=MOM, hair_style='bun', hair=HAIRD, arms=MA, smile=False, look=(0.4, -0.2))
    p.form(p.ellipse(505, 870, 30, 26), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    for sg in (-1, 1): p.line(curve([(540 + sg * 64, 720), (540 + sg * 40, 706), (540 + sg * 18, 714)], 8), 'umber', 3, 0.8, alpha=0.85)
    for q in range(3): p.line(curve([(470 - q * 26, 850 - q * 10), (450 - q * 26, 870), (470 - q * 26, 890 + q * 10)], 10), 'cream', 3.4, 0.7, alpha=0.7)
    S.save('searching_mom')


def reunion():
    """家に連れて帰るために: the mother hugging the found child tightly with tears of relief; far behind, a cross on a hill glowing gold"""
    S = Shot(3207); p = S.p
    dusk(S, 1100)
    hill = p.ellipse(860, 700, 260, 110) * (p.YY < 720)
    p.glow(860, 450, 300, strength=1.3, density=1.1)
    p.form(hill, ('moss', 'olive', 'sage'), 0, LIGHT, density=1.4, seed=S.sd())
    for seg in (p.rect(852, 420, 868, 610), p.rect(815, 465, 905, 480)): p.form(seg, ('sepia', 'umber', 'brown'), 90, LIGHT, density=1.7, seed=S.sd())
    p.form((p.YY >= 1100).astype(np.float32), ('tan', 'sienna', 'stone', 'umber'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    bulbs(S, [(0, 260), (260, 330), (540, 300), (760, 360)])
    m = person(S, 470, 760, 140, coat=MOM, hair_style='bun', plan=True); erase(S, m['mask'])
    person(S, 470, 760, 140, coat=MOM, hair_style='bun', hair=HAIRD, eyes_closed=True, smile=True)
    p.form(p.ellipse(420, 800, 7, 11), ('powder', 'sky_pale', 'cornflower'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(p.ellipse(522, 806, 7, 11), ('powder', 'sky_pale', 'cornflower'), 0, LIGHT, density=1.6, seed=S.sd())
    fig = figure(S, 560, 1360, 430, coat=KID, hair=HAIRD, back=True, legs=LEGS)
    for arm in ([(340, 1000), (420, 1080), (540, 1090)], [(620, 990), (690, 1060), (640, 1110)]):
        t_ = p.tube(arm, 34, 28); erase(S, t_); p.form(t_, MOM, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(t_, 'sepia', density=0.7, alpha=0.6)
    p.lift(blur(np.clip(m['mask'] + fig, 0, 1), 30) * (1 - np.clip(m['mask'] + fig, 0, 1)), 'butter', 0.35)
    S.save('reunion')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
