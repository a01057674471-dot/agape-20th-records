"""「神様がいるなら、なぜ悪いことが起きるの?」 paintings. python3 shots.py NAME"""
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
ROBE_J = ('white', 'cream', 'ivory', 'sand')
dusk, night = z.dusk, z.night


def _window_girl(S, dawn=False):
    p = S.p
    ARMS = [[(430, 1060), (470, 1160), (560, 1180)], [(650, 1060), (610, 1160), (560, 1180)]]
    w = person(S, 540, 820, 160, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    win = p.rect(120, 120, 960, 1040) * (1 - w['mask'])
    if dawn:
        sky(S, 1040, (760, 600, 420)); p.glow(760, 600, 420, strength=1.3, density=1.1)
    else:
        night(S, 1040)
    p.lift(blur(win, 1) * 0, 'paper', 0)
    for x in (120, 540, 960): p.line([(x, 120), (x, 1040)], 'tan', 12, 0.8, alpha=0.9)
    for y in (120, 580, 1040): p.line([(120, y), (960, y)], 'tan', 12, 0.8, alpha=0.9)
    wall = np.clip(np.ones((H, W), np.float32) - p.rect(120, 120, 960, 1040), 0, 1) * (p.YY < 1300)
    p.hatch(wall, p.flow(2, 4, 500), ['tan', 'sienna', 'brown'] if not dawn else ['cream', 'apricot', 'sand'], (60, 140), (1.8, 2.5), 1.6, 0.66, avoid=w['mask'], seed=S.sd())
    p.form((p.YY >= 1300).astype(np.float32), ('brown', 'sienna', 'umber'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    if not dawn:
        rr = np.random.default_rng(4)
        for _ in range(140):
            x, y = rr.uniform(130, 950), rr.uniform(130, 1030)
            if w['mask'][int(y), int(x)] > 0.1: continue
            p.line([(x, y), (x - 4, y + rr.uniform(20, 40))], 'powder', 2.2, 0.6, alpha=0.55)
        p.glow(980, 1180, 260, strength=0.8, density=0.8)
    erase(S, w['mask'])
    person(S, 540, 820, 160, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, eyes_closed=True, smile=dawn, hands=False)
    knees = p.ellipse(560, 1230, 220, 90) * (p.YY < 1300)
    erase(S, knees); p.form(knees, ('cornflower', 'denim', 'indigo'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(560, 1175, 46, 34), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    return w


def rain_window():
    """どうして、こんなことが: the young woman by a rainy window at night, hugging her knees, a dim lamp"""
    S = Shot(3401)
    _window_girl(S)
    S.save('rain_window')


def dawn_window():
    """あなたは、ひとりではありません: the same window at dawn after the rain, a warm light on her shoulder, the sky brightening"""
    S = Shot(3402); p = S.p
    _window_girl(S, dawn=True)
    p.glow(390, 1000, 220, strength=1.0, density=0.9)
    S.save('dawn_window')


def empty_chair():
    """地震、病気、突然の別れ: an empty wooden chair with a single white flower on it in a quiet grey room"""
    S = Shot(3403); p = S.p
    wall = (p.YY < 1250).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['stone', 'warmgrey', 'lavender'], (60, 140), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.form((p.YY >= 1250).astype(np.float32), ('tan', 'warmgrey', 'umber'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    beam = p.poly([(700, 0), (900, 0), (760, 1400), (360, 1400)])
    p.lift(blur(beam, 40), 'cream', 0.35, tooth=0)
    back = p.rect(360, 560, 720, 620); seat = p.poly([(330, 960), (750, 960), (790, 1030), (290, 1030)])
    posts = np.clip(p.rect(370, 560, 400, 1000) + p.rect(680, 560, 710, 1000), 0, 1)
    legs = np.clip(p.rect(300, 1030, 330, 1360) + p.rect(750, 1030, 780, 1360) + p.rect(360, 1030, 385, 1280) + p.rect(690, 1030, 715, 1280), 0, 1)
    slats = sum(p.rect(x, 620, x + 20, 960) for x in (450, 530, 610))
    ch = np.clip(back + seat + posts + legs + slats, 0, 1); erase(S, ch)
    p.form(ch, ('tan', 'sienna', 'brown', 'umber'), 90, LIGHT, density=1.6, seed=S.sd()); p.edge(ch, 'sepia', density=0.8, alpha=0.75)
    p.line(curve([(470, 990), (560, 980), (660, 970)], 20), 'moss', 6, 0.85, alpha=0.95)
    for (fx, fy, r) in ((470, 985, 40),):
        for a in np.linspace(0, 2 * np.pi, 7)[:-1]:
            pt = p.ellipse(fx + r * 0.6 * np.cos(a), fy + r * 0.6 * np.sin(a), r * 0.5, r * 0.3, rot=np.degrees(a))
            erase(S, pt); p.form(pt, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(pt, 'stone', density=0.6, alpha=0.6)
        p.form(p.ellipse(fx, fy, 12, 12), ('butter', 'gold', 'amber'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('empty_chair')


def compassion():
    """罰とは限りません: Jesus in simple robes kneeling beside a suffering person, holding their hand; warm light"""
    S = Shot(3404); p = S.p
    dusk(S, 1150, cols=('cream', 'apricot', 'lavender'), low=('butter', 'peach', 'apricot'))
    ground(S, 1150, cols=('sand', 'ochre', 'tan', 'olive'), flowers=0)
    p.glow(380, 640, 380, strength=1.1, density=1.0)
    JA = [[(450, 1040), (530, 1110), (600, 1120)]]
    j = person(S, 360, 780, 130, coat=ROBE_J, hair_style='long', plan=True, arms=JA)
    SA = [[(690, 1150), (650, 1140), (610, 1125)]]
    s_ = person(S, 760, 960, 110, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='short', plan=True, arms=SA)
    for mm in (j['mask'], s_['mask']): erase(S, mm)
    person(S, 760, 960, 110, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='short', hair=HAIRD, arms=SA, hands=False, eyes_closed=True, smile=False)
    person(S, 360, 780, 130, coat=ROBE_J, hair_style='long', hair=HAIRD, arms=JA, hands=False, eyes_closed=True, smile=True)
    p.line([(330, 670), (360, 690), (390, 670)], 'umber', 0.1, 0.1, alpha=0.0)
    p.form(p.ellipse(605, 1120, 36, 30), SKIN4, 0, LIGHT, density=1.6, seed=S.sd()); p.edge(p.ellipse(605, 1120, 36, 30), 'skin_shade', density=0.8)
    p.glow(605, 1120, 160, strength=0.7, density=0.7)
    S.save('compassion')


def father_wait():
    """忍耐して待っている: a father standing at the door of his house at sunset, looking far down a long road, waiting with hope"""
    S = Shot(3405); p = S.p
    dusk(S, 1000)
    p.glow(560, 960, 380, strength=1.3, density=1.1)
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [960, 930, 950, 920, 940, 960, 940], RIDGES[0], mist=0.5)
    ground(S, 1000, cols=('ochre', 'olive', 'sand', 'moss'), flowers=40)
    road = p.poly([(540, 1000), (580, 1000), (820, 1920), (380, 1920)])
    p.form(road, ('sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, length=(30, 60), density=1.2, seed=S.sd())
    house = p.rect(40, 700, 330, 1250); erase(S, house); p.form(house, ('cream', 'sand', 'tan'), 90, LIGHT, density=1.4, seed=S.sd())
    rf = p.poly([(10, 710), (185, 560), (360, 710)]); erase(S, rf); p.form(rf, ('terracotta', 'brick', 'sienna'), 0, LIGHT, density=1.6, seed=S.sd())
    dr = p.rect(220, 950, 310, 1250); p.lift(dr, 'lemon', 0.8, tooth=0); p.glow(265, 1100, 160, strength=0.8, density=0.8)
    p.window(70, 800, 170, 900, panes=(2, 2), glow=0.8, seed=S.sd())
    figure(S, 400, 1300, 460, coat=('peach', 'coral', 'terracotta', 'brick'), hair=('stone', 'warmgrey', 'umber'), back=True, up=0.2, legs=('umber', 'sepia', 'sepia'))
    S.save('father_wait')


def lazarus():
    """友の死に、なみだを流しました: Jesus with grieving friends near a stone tomb, quietly shedding tears; soft sorrowful light"""
    S = Shot(3406); p = S.p
    dusk(S, 1100, cols=('lavender', 'stone', 'mauve'), low=('peach', 'sand', 'apricot'))
    ground(S, 1100, cols=('sand', 'tan', 'olive', 'ochre'), flowers=0)
    rock = p.ellipse(860, 920, 320, 300) * (p.YY < 1120); erase(S, rock)
    p.form(rock, ('stone', 'warmgrey', 'slate', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(860, 1000, 110, 120) * (p.YY < 1110), ('sepia', 'umber', 'slate'), 0, LIGHT, density=1.7, seed=S.sd())
    for (x, y, R, c, hs) in ((170, 860, 95, ('olive', 'moss', 'sage', 'pine'), 'bun'), (360, 820, 115, ROBE_J, 'long'), (560, 870, 95, ('rose', 'pink', 'coral', 'brick'), 'long')):
        m = person(S, x, y, R, coat=c, hair_style=hs, plan=True); erase(S, m['mask'])
        person(S, x, y, R, coat=c, hair_style=hs, hair=HAIRD, eyes_closed=True, smile=False)
    for dx in (-36, 36): p.form(p.ellipse(360 + dx, 880, 7, 12), ('powder', 'sky_pale', 'cornflower'), 0, LIGHT, density=1.6, seed=S.sd())
    p.glow(360, 760, 260, strength=0.6, density=0.6)
    S.save('lazarus')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
