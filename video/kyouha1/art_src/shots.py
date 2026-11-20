"""「カトリックとプロテスタント、なにがちがう?」 paintings for both parts (歴史編 / ちがい編). python3 shots.py NAME"""
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
ROBE = ('sienna', 'brown', 'umber', 'sepia')
STONE = ('cream', 'sand', 'stone', 'warmgrey')


def cathedral(S, cx, base, s=1.0):
    """an ornate church: two pointed towers, a tall spire, a rose window and an arched door"""
    p = S.p
    body = p.rect(cx - 170 * s, base - 380 * s, cx + 170 * s, base)
    gable = p.poly([(cx - 170 * s, base - 380 * s), (cx, base - 560 * s), (cx + 170 * s, base - 380 * s)])
    towers = [p.rect(cx + sg * 210 * s - 60 * s, base - 620 * s, cx + sg * 210 * s + 60 * s, base) for sg in (-1, 1)]
    tops = [p.poly([(cx + sg * 210 * s - 72 * s, base - 620 * s), (cx + sg * 210 * s, base - 820 * s), (cx + sg * 210 * s + 72 * s, base - 620 * s)]) for sg in (-1, 1)]
    spire = p.poly([(cx - 26 * s, base - 540 * s), (cx, base - 760 * s), (cx + 26 * s, base - 540 * s)])
    m = np.clip(body + gable + sum(towers) + sum(tops) + spire, 0, 1)
    erase(S, m)
    p.form(np.clip(body + gable + sum(towers), 0, 1), STONE, 90, LIGHT, length=(20, 50), density=1.5, seed=S.sd())
    p.form(np.clip(sum(tops) + spire, 0, 1), ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    rose = p.ellipse(cx, base - 400 * s, 62 * s, 62 * s)
    p.form(rose, ('cobalt', 'ruby' if False else 'red', 'butter', 'violet'), p.radial(cx, base - 400 * s, 0), LIGHT, density=1.6, seed=S.sd())
    for a in np.linspace(0, np.pi, 5)[:-1]:
        p.line([(cx - 62 * s * np.cos(a), base - 400 * s - 62 * s * np.sin(a)), (cx + 62 * s * np.cos(a), base - 400 * s + 62 * s * np.sin(a))], 'umber', 2.4, 0.8, alpha=0.8)
    door = np.clip(p.rect(cx - 55 * s, base - 160 * s, cx + 55 * s, base) + p.ellipse(cx, base - 160 * s, 55 * s, 55 * s), 0, 1)
    p.form(door, ('brown', 'umber', 'sepia'), 90, LIGHT, density=1.6, seed=S.sd())
    for sg in (-1, 1):
        for yy in (base - 520 * s, base - 330 * s):
            w_ = np.clip(p.rect(cx + sg * 210 * s - 20 * s, yy, cx + sg * 210 * s + 20 * s, yy + 80 * s) + p.ellipse(cx + sg * 210 * s, yy, 20 * s, 20 * s), 0, 1)
            p.form(w_, ('butter', 'amber', 'tangerine'), 90, LIGHT, density=1.5, seed=S.sd())
    for mm in (np.clip(body + gable + sum(towers), 0, 1),): p.edge(mm, 'sepia', density=0.8, alpha=0.75)
    p.line([(cx, base - 760 * s), (cx, base - 830 * s)], 'umber', 5 * s, 0.85, alpha=0.95)
    p.line([(cx - 22 * s, base - 805 * s), (cx + 22 * s, base - 805 * s)], 'umber', 5 * s, 0.85, alpha=0.95)
    return m


def chapel(S, cx, base, s=1.0):
    """a simple white church with a plain cross"""
    p = S.p
    body = p.rect(cx - 150 * s, base - 260 * s, cx + 150 * s, base)
    roof = p.poly([(cx - 180 * s, base - 250 * s), (cx, base - 420 * s), (cx + 180 * s, base - 250 * s)])
    m = np.clip(body + roof, 0, 1); erase(S, m)
    p.form(body, ('white', 'cream', 'ivory', 'sand'), 90, LIGHT, density=1.4, seed=S.sd())
    p.form(roof, ('terracotta', 'brick', 'sienna', 'brown'), 0, LIGHT, density=1.6, seed=S.sd())
    p.window(cx - 100 * s, base - 200 * s, cx - 40 * s, base - 110 * s, panes=(1, 2), glow=0.7, seed=S.sd())
    p.window(cx + 40 * s, base - 200 * s, cx + 100 * s, base - 110 * s, panes=(1, 2), glow=0.7, seed=S.sd())
    door = p.rect(cx - 36 * s, base - 120 * s, cx + 36 * s, base); p.form(door, ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.5, seed=S.sd())
    p.edge(m, 'sepia', density=0.8, alpha=0.75)
    p.line([(cx, base - 420 * s), (cx, base - 540 * s)], 'umber', 7 * s, 0.85, alpha=0.95)
    p.line([(cx - 34 * s, base - 500 * s), (cx + 34 * s, base - 500 * s)], 'umber', 7 * s, 0.85, alpha=0.95)
    return m


def two_churches():
    """なにがちがうの?: the young woman, from behind, looking at two churches side by side -- one ornate, one simple"""
    S = Shot(2801); p = S.p
    sky(S, 1150, (540, 300, 380))
    clouds(S, [(180, 260, 280, 60), (900, 330, 240, 56)])
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1060, 1000, 1040, 980, 1020, 1050, 1010], RIDGES[0], mist=0.5)
    ground(S, 1150, flowers=90)
    cathedral(S, 290, 1150, 0.95)
    chapel(S, 810, 1150, 0.95)
    p.form(p.poly([(520, 1150), (560, 1150), (700, 1920), (380, 1920)]), ('sand', 'cream', 'tan'), p.flow(90, 8), LIGHT, density=1.2, seed=S.sd())
    figure(S, 540, 1700, 420, coat=COAT, hair=HAIR, back=True, up=0.5, legs=('cornflower', 'denim', 'indigo'))
    S.save('two_churches')


def one_hill():
    """同じところ: the two churches on the same green hill, one great cross of light in the sky above both"""
    S = Shot(2802); p = S.p
    sky(S, 1200, None)
    p.glow(540, 420, 520, strength=1.4, density=1.2)
    cr = np.clip(p.rect(520, 180, 560, 640) + p.rect(400, 300, 680, 340), 0, 1)
    p.lift(blur(cr, 18), 'white', 0.9, tooth=0); p.lift(blur(cr, 50), 'butter', 0.6, tooth=0)
    hill = p.ellipse(540, 1500, 900, 380)
    p.form(hill, ('yellowgreen', 'meadow', 'moss', 'sage'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form((p.YY > 1500).astype(np.float32) * (1 - hill), ('meadow', 'grass', 'moss'), 0, LIGHT, density=1.3, seed=S.sd())
    cathedral(S, 330, 1180, 0.7)
    chapel(S, 760, 1180, 0.75)
    p.flowers(hill * (p.YY > 1230), kinds=('daisy', 'buttercup', 'poppy'), n=60, size=(7, 11))
    S.save('one_hill')


def luther_door():
    """1517年: a monk, seen from behind, nailing a paper to a great wooden church door in an old town; warm light"""
    S = Shot(2803); p = S.p
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sand', 'stone', 'cream'], (60, 140), (1.8, 2.5), 1.7, 0.66, seed=S.sd())
    for y in range(80, 1500, 110):
        p.line([(0, y), (1080, y)], 'tan', 2.4, 0.6, alpha=0.4)
        for x in np.arange((y // 110 % 2) * 90, 1080, 180): p.line([(x, y), (x, y + 110)], 'tan', 2.2, 0.6, alpha=0.35)
    arch = np.clip(p.rect(220, 520, 860, 1500) + p.ellipse(540, 520, 320, 300), 0, 1)
    erase(S, arch); p.form(arch, ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    door = np.clip(p.rect(270, 560, 810, 1500) + p.ellipse(540, 560, 270, 250), 0, 1)
    p.form(door, ('sienna', 'brown', 'umber', 'sepia'), 90, LIGHT, length=(40, 90), density=1.6, seed=S.sd())
    for x in range(330, 810, 80): p.line([(x, 470 if abs(x - 540) < 200 else 560), (x, 1500)], 'sepia', 2.6, 0.7, alpha=0.6)
    for y in (760, 1150): p.line([(270, y), (810, y)], 'umber', 9, 0.85, alpha=0.9)
    p.form((p.YY >= 1500).astype(np.float32), ('stone', 'pebble', 'warmgrey', 'umber'), 0, LIGHT, length=(60, 120), density=1.4, seed=S.sd())
    paper = p.poly([(500, 820), (660, 810), (670, 1030), (505, 1040)])
    erase(S, paper); p.form(paper, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.4, seed=S.sd())
    for q in range(8): p.line([(520, 850 + q * 22), (650, 846 + q * 22)], 'pebble', 2, 0.6, alpha=0.6)
    fm = figure(S, 470, 1780, 760, coat=ROBE, hair=('hair', 'umber', 'sepia'), back=True, legs=('umber', 'sepia', 'sepia'))
    arm = p.tube([(560, 1150), (620, 980), (600, 860)], 34, 28)
    erase(S, arm); p.form(arm, ROBE, 90, LIGHT, density=1.5, seed=S.sd()); p.edge(arm, 'sepia', density=0.8, alpha=0.7)
    p.form(p.ellipse(600, 840, 26, 24), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    p.line([(590, 830), (640, 790)], 'umber', 7, 0.85, alpha=0.95); p.form(p.rect(628, 770, 668, 800), ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.glow(900, 300, 420, strength=0.8, density=0.8)
    S.save('luther_door')


def indulgence():
    """贖宥状: people handing coins to an official at a table covered with papers; a monk at the side, worried"""
    S = Shot(2804); p = S.p
    wall = (p.YY < 1050).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sand', 'stone', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    for x in (140, 940):
        col = p.rect(x - 50, 0, x + 50, 1050); p.form(col, STONE, 90, LIGHT, density=1.4, seed=S.sd())
    p.form((p.YY >= 1050).astype(np.float32), ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    table = p.rect(260, 980, 820, 1100)
    OA = [[(470, 880), (430, 960), (480, 990)], [(610, 880), (650, 960), (600, 990)]]
    of = person(S, 540, 700, 110, coat=('red', 'brick', 'terracotta', 'brown'), hair_style='short', plan=True, arms=OA, cut=table)
    erase(S, of['mask'])
    person(S, 540, 700, 110, coat=('red', 'brick', 'terracotta', 'brown'), hair_style='short', hair=('hair', 'umber', 'sepia'), arms=OA, cut=table, smile=True, look=(0, 0.5))
    cap = p.ellipse(540, 600, 100, 40) * (p.YY < 610); erase(S, cap); p.form(cap, ('brick', 'red', 'brown'), 0, LIGHT, density=1.6, seed=S.sd())
    erase(S, table); p.form(table, ('brown', 'sienna', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    rr = np.random.default_rng(3)
    for j in range(7):
        x, y = 320 + j * 70 + rr.uniform(-10, 10), 975 - rr.uniform(0, 20)
        pg = p.poly([(x - 34, y - 30), (x + 34, y - 34), (x + 36, y + 6), (x - 32, y + 10)]); erase(S, pg)
        p.form(pg, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.3, seed=S.sd()); p.lift(p.ellipse(x + 20, y - 4, 8, 8), 'red', 0.9, tooth=0)
    for j in range(9):
        cx_, cy_ = 680 + rr.uniform(-60, 60), 1030 + rr.uniform(-20, 20)
        p.form(p.ellipse(cx_, cy_, 16, 10), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    for (x, y, hh, c) in ((300, 1700, 520, ('olive', 'moss', 'sage', 'pine')), (620, 1780, 560, ('cornflower', 'denim', 'slate', 'indigo'))):
        figure(S, x, y, hh, coat=c, hair=('hair', 'umber', 'sepia'), back=True, legs=('stone', 'warmgrey', 'umber'))
    hand_ = p.tube([(680, 1350), (700, 1180)], 30, 26); erase(S, hand_); p.form(hand_, ('cornflower', 'denim', 'slate'), 90, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(704, 1160, 24, 20), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(708, 1136, 16, 10), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    MA = [[(900, 990), (880, 1080), (930, 1110)], [(1010, 990), (1030, 1080), (980, 1110)]]
    mk = person(S, 955, 820, 90, coat=ROBE, hair_style='short', plan=True, arms=MA)
    erase(S, mk['mask'])
    person(S, 955, 820, 90, coat=ROBE, hair_style='short', hair=('hair', 'umber', 'sepia'), arms=MA, smile=False, look=(-0.6, 0.1))
    p.line(curve([(920, 752), (935, 760), (948, 756)], 6), 'umber', 2.4, 0.8, alpha=0.85)
    p.line(curve([(962, 756), (975, 760), (990, 752)], 6), 'umber', 2.4, 0.8, alpha=0.85)
    S.save('indulgence')


def luther_read():
    """ルターは聖書を読み: a monk reading a large open book by candlelight late at night, light rising from the pages"""
    S = Shot(2805); p = S.p
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['umber', 'sepia', 'indigo'], (60, 140), (1.8, 2.5), 1.8, 0.8, seed=S.sd())
    desk = (p.YY >= 1120).astype(np.float32)
    ARMS = [[(400, 960), (360, 1080), (420, 1140)], [(680, 960), (720, 1080), (660, 1140)]]
    w = person(S, 540, 720, 150, coat=ROBE, hair_style='short', plan=True, arms=ARMS, cut=desk)
    p.glow(540, 1000, 600, strength=1.2, density=1.1)
    erase(S, w['mask'])
    person(S, 540, 720, 150, coat=ROBE, hair_style='short', hair=('hair', 'umber', 'sepia'), arms=ARMS, cut=desk, smile=True, look=(0, 0.8))
    p.form(desk, ('brown', 'sienna', 'umber', 'sepia'), 0, LIGHT, length=(80, 160), density=1.5, seed=S.sd())
    L_ = p.poly(curve([(200, 1180), (370, 1130), (535, 1170), (535, 1500), (370, 1470), (180, 1520)], 50), smooth=True)
    R_ = p.poly(curve([(545, 1170), (710, 1130), (880, 1180), (900, 1520), (710, 1470), (545, 1500)], 50), smooth=True)
    for mm, x0 in ((L_, 230), (R_, 580)):
        erase(S, mm); p.hatch(mm, 90, ('white', 'cream', 'ivory'), (20, 50), (1.6, 2.3), 1.5, 0.7, opacity=0.85, alpha=0.85, seed=S.sd())
        for kk in range(10): p.line([(x0, 1200 + kk * 28), (x0 + 270, 1202 + kk * 28)], 'pebble', 2.2, 0.7, alpha=0.65)
    p.glow(540, 1300, 360, strength=1.0, density=1.0)
    cd = p.rect(880, 820, 940, 1130); erase(S, cd); p.form(cd, ('white', 'cream', 'ivory'), 90, LIGHT, density=1.4, seed=S.sd())
    p.glow(910, 770, 300, strength=1.2, density=1.1)
    p.lift(p.blob(910, 780, 18, 42, 0.1), 'lemon', 1.0, tooth=0); p.lift(p.ellipse(910, 795, 8, 18), 'white', 1.0, tooth=0)
    S.save('luther_read')


def priest_pastor():
    """神父と牧師: left, a priest in a black robe, alone and smiling; right, a pastor in a simple suit with his wife and child"""
    S = Shot(2806); p = S.p
    left = (p.XX < 540).astype(np.float32); right = 1 - left
    p.hatch(left, p.flow(2, 4, 500), ['cream', 'lavender', 'stone'], (60, 140), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.hatch(right, p.flow(2, 4, 500), ['cream', 'apricot', 'peach'], (60, 140), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.form((p.YY >= 1300).astype(np.float32), ('sand', 'tan', 'sienna'), 0, LIGHT, length=(60, 140), density=1.3, seed=S.sd())
    pr = person(S, 270, 760, 120, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='short', plan=True)
    erase(S, pr['mask'])
    person(S, 270, 760, 120, coat=('slate', 'indigo', 'umber', 'sepia'), hair_style='short', hair=('hair', 'umber', 'sepia'), smile=True)
    col = p.rect(245, 870, 295, 895); p.lift(col, 'white', 1.0, tooth=0)
    for (x, y, R, c, hs) in ((760, 760, 110, ('cobalt', 'denim', 'indigo', 'slate'), 'short'),
                             (945, 800, 98, ('rose', 'pink', 'coral', 'brick'), 'long'),
                             (860, 1050, 70, ('butter', 'sun', 'amber', 'ochre'), 'bob')):
        mm = person(S, x, y, R, coat=c, hair_style=hs, plan=True); erase(S, mm['mask'])
        person(S, x, y, R, coat=c, hair_style=hs, hair=('hair', 'umber', 'sepia'), smile=True)
    p.form(p.poly([(740, 880), (780, 880), (770, 990), (750, 990)]), ('red', 'brick', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    p.line([(540, 0), (540, 1920)], 'tan', 6, 0.8, alpha=0.85)
    S.save('priest_pastor')


def paper_bg():
    S = Shot(2807); p = S.p
    p.hatch(np.ones((H, W), np.float32), p.flow(2, 4, 500), ['cream', 'ivory', 'apricot'], (60, 140), (1.8, 2.5), 1.4, 0.55, alpha=0.5, seed=S.sd())
    p.glow(540, 760, 700, strength=0.5, density=0.6)
    S.save('paper_bg')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
