"""「クリスチャンは、お墓参りしちゃダメなの?」 paintings -- gravestones carry no readable text. python3 shots.py NAME"""
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
GREY_HAIR = ('stone', 'warmgrey', 'white')
GRAN = ('lavender', 'mauve', 'violet', 'indigo')
STONE = ('stone', 'warmgrey', 'pebble', 'slate')
dusk = z.dusk


def grave(S, x, base, s=1.0, flowers=True, cols=STONE):
    """a simple Japanese gravestone on two plinths, a vase each side -- no lettering"""
    p = S.p
    b1 = p.rect(x - 150 * s, base - 50 * s, x + 150 * s, base)
    b2 = p.rect(x - 110 * s, base - 100 * s, x + 110 * s, base - 50 * s)
    st = p.rect(x - 60 * s, base - 380 * s, x + 60 * s, base - 100 * s)
    top = p.poly([(x - 60 * s, base - 380 * s), (x, base - 400 * s), (x + 60 * s, base - 380 * s)])
    m = np.clip(b1 + b2 + st + top, 0, 1); erase(S, m)
    p.form(m, cols, 90, LIGHT, length=(20, 50), density=1.5, seed=S.sd()); p.edge(m, 'slate', density=0.8, alpha=0.7)
    for yy in (base - 50 * s, base - 100 * s): p.line([(x - 150 * s, yy), (x + 150 * s, yy)], 'slate', 2.4, 0.6, alpha=0.6)
    if flowers:
        for sg in (-1, 1):
            vx = x + sg * 90 * s
            v = p.rect(vx - 16 * s, base - 170 * s, vx + 16 * s, base - 100 * s); erase(S, v); p.form(v, ('slate', 'stone', 'umber'), 90, LIGHT, density=1.5, seed=S.sd())
            for j, c in enumerate((('rose', 'pink', 'red'), ('butter', 'gold', 'amber'), ('white', 'cream', 'ivory'), ('lavender', 'violet', 'mauve'))):
                fx, fy = vx + (j - 1.5) * 14 * s, base - (200 + (j % 2) * 26) * s
                p.line([(vx, base - 170 * s), (fx, fy)], 'moss', 3 * s, 0.8, alpha=0.9)
                p.form(p.ellipse(fx, fy, 16 * s, 14 * s), c, 0, LIGHT, density=1.6, seed=S.sd())
    return m


def family_photo():
    """できなくなるの?: the young woman at home looking at an old family photo in her hands, thoughtful, afternoon light"""
    S = Shot(3601); p = S.p
    ARMS = [[(420, 1020), (430, 1130), (480, 1170)], [(660, 1020), (650, 1130), (600, 1170)]]
    w = person(S, 540, 780, 160, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    hj.room(S, w['mask'], win_box=(660, 140, 1000, 600))
    erase(S, w['mask'])
    person(S, 540, 780, 160, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, hands=False, smile=False, look=(0, 0.7))
    fr = p.rect(440, 1080, 640, 1250); erase(S, fr); p.form(fr, ('brown', 'sienna', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    ph = p.rect(458, 1098, 622, 1232); p.lift(ph, 'cream', 1.0, tooth=0); p.form(ph, ('sand', 'cream', 'stone'), 0, LIGHT, density=1.0, seed=S.sd())
    for (fx, fy, r) in ((500, 1150, 16), (540, 1145, 18), (585, 1155, 14)):
        p.form(p.ellipse(fx, fy, r, r), ('tan', 'sienna', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
        p.form(p.ellipse(fx, fy + r * 2.3, r * 1.3, r * 1.4) * (p.YY < 1232), ('stone', 'warmgrey', 'tan'), 0, LIGHT, density=1.3, seed=S.sd())
    for (x, y) in ((480, 1170), (600, 1170)): p.form(p.ellipse(x, y, 30, 26), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('family_photo')


def cemetery_bg(S, y_g=1000, sun=(860, 260, 300)):
    p = S.p
    sky(S, y_g, sun)
    clouds(S, [(200, 260, 280, 60), (760, 420, 220, 54)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [y_g - 60, y_g - 100, y_g - 70, y_g - 110, y_g - 80, y_g - 60, y_g - 90], RIDGES[2], mist=0.5)
    ground(S, y_g, cols=('sand', 'cream', 'stone', 'tan'), flowers=0)
    for x in (80, 1000): p.tree(x, y_g + 20, 420, 140, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())


def cemetery_walk():
    """クリスチャンも、お墓参りをします: three generations walking through a quiet Japanese cemetery on a sunny day, flowers and a bucket"""
    S = Shot(3602); p = S.p
    cemetery_bg(S)
    for j, (x, b, s_) in enumerate(((170, 1060, 0.55), (360, 1050, 0.5), (720, 1050, 0.5), (900, 1060, 0.55), (250, 1180, 0.7), (840, 1180, 0.7))):
        grave(S, x, b, s_, flowers=(j % 2 == 0))
    path = p.poly([(470, 1000), (610, 1000), (820, 1920), (260, 1920)]) * (p.YY > 1000)
    p.form(path, ('cream', 'sand', 'stone'), p.flow(90, 6), LIGHT, length=(30, 60), density=1.2, seed=S.sd())
    figure(S, 400, 1700, 560, coat=GRAN, hair=GREY_HAIR, back=True, legs=('stone', 'warmgrey', 'umber'))
    figure(S, 600, 1740, 640, coat=COAT, hair=HAIR, back=True, legs=('cornflower', 'denim', 'indigo'))
    figure(S, 770, 1760, 400, coat=('butter', 'sun', 'amber', 'ochre'), hair=HAIRD, back=True, legs=('cornflower', 'denim', 'indigo'))
    bq = p.ellipse(500, 1390, 46, 60); erase(S, bq); p.form(bq, ('rose', 'pink', 'butter', 'red'), 0, LIGHT, density=1.6, seed=S.sd())
    p.line([(500, 1440), (505, 1500)], 'moss', 5, 0.8, alpha=0.9)
    bk = p.poly([(820, 1500), (880, 1500), (872, 1580), (828, 1580)]); erase(S, bk); p.form(bk, ('powder', 'cornflower', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    p.line(curve([(822, 1500), (850, 1460), (878, 1500)], 10), 'slate', 3, 0.8, alpha=0.9)
    S.save('cemetery_walk')


def grave_wash():
    """お墓をきれいにして、お花を供えて: a gravestone freshly washed (wet streaks), fresh flowers in both vases, a wooden bucket and ladle"""
    S = Shot(3603); p = S.p
    cemetery_bg(S, 900)
    gm = grave(S, 540, 1400, 1.9, flowers=False)
    rr = np.random.default_rng(2)
    for q in range(14):
        x0 = 540 + rr.uniform(-100, 100); y0 = rr.uniform(660, 800)
        p.line(curve([(x0, y0), (x0 + rr.uniform(-4, 4), y0 + 120), (x0 + rr.uniform(-6, 6), y0 + rr.uniform(260, 420))], 12), 'slate', 4, 0.6, alpha=0.45)
    for q in range(10):
        x0 = 540 + rr.uniform(-100, 100); y0 = rr.uniform(700, 1100); p.lift(p.ellipse(x0, y0, 6, 9), 'white', 0.8, tooth=0)
    cols = (('rose', 'pink', 'red'), ('butter', 'gold', 'amber'), ('white', 'cream', 'ivory'), ('lavender', 'violet', 'mauve'), ('coral', 'tangerine', 'red'))
    for sg in (-1, 1):
        vx = 540 + sg * 175
        v = p.rect(vx - 30, 1090, vx + 30, 1210); erase(S, v); p.form(v, ('slate', 'stone', 'umber'), 90, LIGHT, density=1.5, seed=S.sd())
        for j, c in enumerate(cols):
            fx, fy = vx + (j - 2) * 26, 960 - (j % 2) * 50
            p.line([(vx, 1090), (fx, fy)], 'moss', 5, 0.8, alpha=0.9)
            for a_ in np.linspace(0, 2 * np.pi, 6)[:-1]:
                p.form(p.ellipse(fx + 14 * np.cos(a_), fy + 14 * np.sin(a_), 13, 11), c, 0, LIGHT, density=1.6, seed=S.sd())
            p.form(p.ellipse(fx, fy, 8, 8), ('butter', 'gold', 'amber'), 0, LIGHT, density=1.6, seed=S.sd())
    bk = p.poly([(120, 1500), (320, 1500), (300, 1700), (140, 1700)]); erase(S, bk)
    p.form(bk, ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.6, seed=S.sd())
    for y in (1540, 1660): p.line([(124, y), (316, y)], 'umber', 6, 0.85, alpha=0.9)
    p.form(p.ellipse(220, 1500, 100, 22), ('powder', 'sky_pale', 'cornflower'), 0, LIGHT, density=1.4, seed=S.sd())
    p.line([(240, 1500), (380, 1300)], 'tan', 9, 0.85, alpha=0.95)
    lad = p.ellipse(240, 1505, 34, 16); p.form(lad, ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.6, seed=S.sd())
    p.glow(540, 900, 320, strength=0.6, density=0.6)
    S.save('grave_wash')


def grandma():
    """父と母を敬いなさい: the young woman holding her grandmother's hand and smiling together on a bench"""
    S = Shot(3604); p = S.p
    sky(S, 1050, (800, 260, 320)); clouds(S, [(220, 300, 280, 60)])
    ground(S, 1050, flowers=140)
    for x in (110, 980): p.tree(x, 1080, 520, 170, colours=('meadow', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    bench = np.clip(p.rect(140, 1160, 940, 1200) + p.rect(140, 1000, 940, 1030) + p.rect(170, 1200, 200, 1320) + p.rect(880, 1200, 910, 1320), 0, 1)
    GA = [[(430, 1060), (480, 1130), (530, 1150)]]
    WA = [[(650, 1060), (600, 1130), (555, 1150)]]
    g = person(S, 330, 840, 120, coat=GRAN, hair_style='bun', plan=True, arms=GA)
    w = person(S, 750, 820, 130, coat=COAT, hair_style='long', plan=True, arms=WA)
    erase(S, bench * (1 - np.clip(g['mask'] + w['mask'], 0, 1))); p.form(bench * (1 - np.clip(g['mask'] + w['mask'], 0, 1)), ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    for mm in (g['mask'], w['mask']): erase(S, mm)
    person(S, 330, 840, 120, coat=GRAN, hair_style='bun', hair=GREY_HAIR, arms=GA, hands=False, smile=True, eyes_closed=True)
    person(S, 750, 820, 130, coat=COAT, hair_style='long', hair=HAIR, arms=WA, hands=False, smile=True, look=(-0.6, 0.2))
    for (x, y, r) in ((530, 1150, 32), (556, 1152, 30)): p.form(p.ellipse(x, y, r, r * 0.85), SKIN4, 0, LIGHT, density=1.6, seed=S.sd())
    p.edge(p.ellipse(543, 1151, 50, 30), 'skin_shade', density=0.7)
    S.save('grandma')


def _grave_girl(S, up=False):
    p = S.p
    cemetery_bg(S, 1050, sun=(260, 240, 340) if up else (860, 260, 300))
    grave(S, 820, 1350, 1.4)
    ARMS = [[(230, 1010), (230, 1130), (300, 1170)], [(450, 1010), (450, 1130), (380, 1170)]] if not up else None
    w = person(S, 340, 790, 150, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    if up:
        p.glow(300, 300, 520, strength=1.4, density=1.2)
        for a in np.linspace(-0.4, 0.3, 5):
            ray = p.poly([(300, 200), (300 + 1600 * np.sin(a) - 40, 200 + 1600 * np.cos(a)), (300 + 1600 * np.sin(a) + 40, 200 + 1600 * np.cos(a))])
            p.lift(blur(ray * (1 - w['mask']), 24), 'butter', 0.35, tooth=0)
    erase(S, w['mask'])
    person(S, 340, 790, 150, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, hands=False, smile=True,
           eyes_closed=not up, look=(-0.1, -0.8) if up else (0, 0))
    if not up: k.gassho(S, 340, 1150, 0.8)
    return w


def grave_pray():
    """思い出して、感謝します: the young woman before a gravestone with fresh flowers, eyes closed, a peaceful grateful smile"""
    S = Shot(3605); _grave_girl(S); S.save('grave_pray')


def grave_lookup():
    """祈りは、神様にささげます: the young woman in the cemetery lifting her face toward the sky, warm light shining down on her"""
    S = Shot(3606); _grave_girl(S, up=True); S.save('grave_lookup')


def cemetery_sunrise():
    """希望: a quiet hillside cemetery at sunrise, golden light spreading over the gravestones and the town below"""
    S = Shot(3607); p = S.p
    dusk(S, 900, cols=('lavender', 'periwinkle', 'powder'), low=('butter', 'apricot', 'peach'))
    p.glow(540, 860, 440, strength=1.6, density=1.3)
    p.lift(p.ellipse(540, 880, 80, 80) * (p.YY < 890), 'white', 0.95, tooth=0)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [880, 860, 880, 850, 870, 890, 870], RIDGES[0], mist=0.6)
    town = (p.YY > 890) & (p.YY < 1000)
    p.form(town.astype(np.float32), ('sage', 'lichen', 'moss'), 0, LIGHT, density=1.3, seed=S.sd())
    for x in np.arange(40, 1080, 90):
        hb = p.rect(x, 940, x + 60, 990); p.form(hb, ('cream', 'sand', 'stone'), 0, LIGHT, density=1.4, seed=S.sd())
        p.form(p.poly([(x - 6, 942), (x + 30, 920), (x + 66, 942)]), ('terracotta', 'slate', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    hill = (p.YY >= 1000).astype(np.float32)
    p.form(hill, ('meadow', 'yellowgreen', 'moss', 'sage'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    for j, (x, b, s_) in enumerate(((140, 1180, 0.6), (380, 1150, 0.55), (700, 1150, 0.55), (940, 1180, 0.6), (260, 1420, 0.8), (820, 1420, 0.8))):
        grave(S, x, b, s_, flowers=(j % 2 == 1))
    p.lift(blur((p.YY > 1000).astype(np.float32) * smoothstep(1500, 1000, p.YY), 30), 'butter', 0.35)
    S.save('cemetery_sunrise')


def walk_home():
    """神様に、つなげていく: the young woman walking down the cemetery path hand in hand with her family at sunset, a ray of light to the sky"""
    S = Shot(3608); p = S.p
    dusk(S, 1000)
    p.glow(540, 880, 420, strength=1.4, density=1.2)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [960, 930, 950, 920, 940, 960, 940], RIDGES[0], mist=0.5)
    ground(S, 1000, cols=('ochre', 'olive', 'sand', 'moss'), flowers=40)
    for j, (x, b, s_) in enumerate(((120, 1100, 0.5), (960, 1100, 0.5), (230, 1250, 0.65), (860, 1250, 0.65))): grave(S, x, b, s_, flowers=False)
    path = p.poly([(500, 1000), (580, 1000), (820, 1920), (260, 1920)])
    p.form(path, ('sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.2, seed=S.sd())
    ray = p.poly([(500, 0), (600, 0), (640, 1500), (440, 1500)])
    p.lift(blur(ray, 40), 'butter', 0.4, tooth=0)
    figure(S, 400, 1720, 560, coat=GRAN, hair=GREY_HAIR, back=True, walk=0.4, legs=('stone', 'warmgrey', 'umber'))
    figure(S, 560, 1740, 620, coat=COAT, hair=HAIR, back=True, walk=0.4, legs=('cornflower', 'denim', 'indigo'))
    figure(S, 710, 1760, 400, coat=('butter', 'sun', 'amber', 'ochre'), hair=HAIRD, back=True, walk=0.4, legs=('cornflower', 'denim', 'indigo'))
    for (x0, y0, x1, y1) in ((460, 1360, 500, 1380), (620, 1390, 660, 1500)):
        t_ = p.tube([(x0, y0), (x1, y1)], 18, 16); erase(S, t_); p.form(t_, SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('walk_home')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
