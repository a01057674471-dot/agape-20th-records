"""「1分でわかる、聖書ってどんな本?」 paintings -- an infographic in coloured pencil (numbers are set in the edit).
python3 shots.py NAME"""
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
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4
COAT, HAIR = hj.SANGHEE, hj.HAIR
WOODC = ('tan', 'sienna', 'brown', 'umber')
SPINES = [('rose', 'coral', 'brick'), ('sky_pale', 'cornflower', 'cobalt'), ('butter', 'gold', 'amber'), ('sage', 'moss', 'pine'),
          ('lavender', 'periwinkle', 'violet'), ('peach', 'apricot', 'terracotta'), ('cream', 'sand', 'tan'), ('powder', 'cornflower', 'slate')]
OLD = [('tan', 'sienna', 'brown'), ('sand', 'ochre', 'sienna'), ('apricot', 'terracotta', 'brick'), ('butter', 'ochre', 'tan')]
NEW = [('sky_pale', 'cornflower', 'cobalt'), ('powder', 'periwinkle', 'slate'), ('cornflower', 'cobalt', 'indigo'), ('lavender', 'periwinkle', 'cornflower')]


def warm_wall(S, y1=1920, cols=('cream', 'ivory', 'apricot')):
    p = S.p
    w = (p.YY < y1).astype(np.float32)
    p.hatch(w, p.flow(2, 4, 500), list(cols), (60, 140), (1.8, 2.5), 1.6, 0.6, alpha=0.65, seed=S.sd())
    return w


def book(S, x0, y0, x1, y1, cols, gold=True):
    p = S.p
    m = p.rect(x0, y0, x1, y1)
    erase(S, m); p.form(m, cols + (cols[-1],), 90, LIGHT, length=(10, 24), density=1.5, seed=S.sd())
    p.edge(m, 'sepia', width=(1.2, 1.8), density=0.8, alpha=0.75)
    if gold and y1 - y0 > 60:
        for yy in (y0 + 18, y1 - 18):
            p.line([(x0 + 4, yy), (x1 - 4, yy)], 'gold', 2.4, 0.8, alpha=0.85)


def shelf(S, x0, x1, rows, top, rowh, palette_fn, seed=1):
    p = S.p
    rr = np.random.default_rng(seed)
    frame = p.rect(x0 - 30, top - 30, x1 + 30, top + rowh * len(rows) + 20)
    erase(S, frame); p.form(frame, WOODC, 0, LIGHT, length=(40, 90), density=1.5, seed=S.sd()); p.edge(frame, 'sepia', density=0.9, alpha=0.85)
    inner = p.rect(x0, top, x1, top + rowh * len(rows) - 10)
    p.form(inner, ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    n = 0
    for r, cnt in enumerate(rows):
        y1 = top + rowh * (r + 1) - 24
        w = (x1 - x0 - 10) / cnt
        for j in range(cnt):
            hgt = rowh * rr.uniform(0.62, 0.86)
            book(S, x0 + 5 + j * w + 2, y1 - hgt, x0 + 5 + (j + 1) * w - 2, y1, palette_fn(n, rr))
            n += 1
        board = p.rect(x0 - 30, y1, x1 + 30, y1 + 24)
        erase(S, board); p.form(board, WOODC, 0, LIGHT, density=1.6, seed=S.sd()); p.edge(board, 'sepia', density=0.8, alpha=0.8)
    return n


def curious():
    """the young woman holding a thick book, head tilted, curious"""
    S = Shot(1601); p = S.p
    ARMS = [[(420, 1000), (400, 1130), (470, 1180)], [(660, 1000), (690, 1130), (620, 1180)]]
    w = person(S, 540, 760, 165, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    hj.room(S, w['mask'], win_box=(700, 160, 1010, 560))
    erase(S, w['mask'])
    person(S, 540, 760, 165, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, smile=False, look=(0.3, -0.2))
    p.line(curve([(525, 865), (540, 860), (555, 868)], 8), 'brick', 2.4, 0.8, alpha=0.9)
    bk = p.poly([(380, 1110), (700, 1110), (720, 1290), (360, 1290)])
    erase(S, bk); p.form(bk, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(bk, 'sepia', density=0.9, alpha=0.85)
    pages = p.rect(370, 1290, 710, 1340)
    erase(S, pages); p.form(pages, ('cream', 'ivory', 'sand', 'tan'), 0, LIGHT, density=1.4, seed=S.sd())
    for j in range(5): p.line([(375, 1298 + j * 9), (705, 1298 + j * 9)], 'sand', 1.6, 0.6, alpha=0.6)
    p.line([(500, 1150), (580, 1150)], 'gold', 4, 0.85, alpha=0.9); p.line([(540, 1130), (540, 1210)], 'gold', 4, 0.85, alpha=0.9)
    for (x, y) in ((470, 1170), (640, 1170)):
        p.form(p.ellipse(x, y, 40, 34), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('curious')


def shelf66():
    """a cozy wooden bookshelf holding 66 small books of different colours"""
    S = Shot(1602); p = S.p
    warm_wall(S)
    p.glow(540, 900, 600, strength=0.5, density=0.5)
    n = shelf(S, 150, 930, [11, 11, 11, 11, 11, 11], 640, 135, lambda n, rr: SPINES[(n * 5 + int(rr.integers(3))) % len(SPINES)], seed=3)
    p.form((p.YY > 1500).astype(np.float32), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.2, seed=S.sd())
    print('books', n)
    S.save('shelf66')


def shelf2():
    """the same shelf in two halves: 39 warm brown spines on the left, 27 soft blue on the right"""
    S = Shot(1603); p = S.p
    warm_wall(S)
    p.glow(540, 900, 600, strength=0.5, density=0.5)
    # 6 rows; left part 39 books (7,7,7,6,6,6), right part 27 (4,4,4,5,5,5) -> divided by a board
    p_ = p
    top, rowh = 640, 135
    frame = p.rect(120, top - 30, 960, top + rowh * 6 + 20)
    erase(S, frame); p.form(frame, WOODC, 0, LIGHT, length=(40, 90), density=1.5, seed=S.sd()); p.edge(frame, 'sepia', density=0.9, alpha=0.85)
    p.form(p.rect(150, top, 930, top + rowh * 6 - 10), ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    rr = np.random.default_rng(5)
    L_, R_ = [7, 7, 7, 6, 6, 6], [4, 4, 4, 5, 5, 5]
    xm = 600
    for r in range(6):
        y1 = top + rowh * (r + 1) - 24
        for (xa, xb, cnt, pal) in ((155, xm - 18, L_[r], OLD), (xm + 18, 925, R_[r], NEW)):
            wd = (xb - xa) / cnt
            for j in range(cnt):
                hgt = rowh * rr.uniform(0.62, 0.86)
                book(S, xa + j * wd + 2, y1 - hgt, xa + (j + 1) * wd - 2, y1, pal[int(rr.integers(len(pal)))])
        board = p.rect(120, y1, 960, y1 + 24)
        erase(S, board); p.form(board, WOODC, 0, LIGHT, density=1.6, seed=S.sd()); p.edge(board, 'sepia', density=0.8, alpha=0.8)
    div = p.rect(xm - 14, top - 30, xm + 14, top + rowh * 6 + 20)
    erase(S, div); p.form(div, ('gold', 'amber', 'ochre'), 90, LIGHT, density=1.6, seed=S.sd()); p.edge(div, 'sepia', density=0.8, alpha=0.8)
    p.form((p.YY > 1500).astype(np.float32), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.2, seed=S.sd())
    S.save('shelf2')


def authors():
    """the writers: a king with a crown, a fisherman, a shepherd with his staff, a physician -- each writing on a scroll"""
    S = Shot(1604); p = S.p
    warm_wall(S, cols=('cream', 'butter', 'apricot'))
    people = [(200, 820, ('butter', 'gold', 'amber', 'ochre'), 'short'), (420, 860, ('powder', 'cornflower', 'denim', 'indigo'), 'short'),
              (650, 840, ('sand', 'tan', 'sienna', 'brown'), 'long'), (880, 860, ('sage', 'lichen', 'moss', 'pine'), 'short')]
    for j, (x, y, coat, hs) in enumerate(people):
        R = 95
        ARMS = [[(x - 60, y + 160), (x - 40, y + 270), (x + 10, y + 290)]]
        m = person(S, x, y, R, coat=coat, hair_style=hs, plan=True, arms=ARMS)
        erase(S, m['mask'])
        person(S, x, y, R, coat=coat, hair_style=hs, hair=('hair', 'umber', 'sepia'), arms=ARMS, smile=True, look=(0, 0.4))
        sc = p.rect(x - 70, y + 290, x + 70, y + 360)
        erase(S, sc); p.form(sc, ('cream', 'ivory', 'sand', 'tan'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(sc, 'tan', density=0.8, alpha=0.8)
        for e in (x - 74, x + 74):
            ro = p.ellipse(e, y + 325, 12, 40); erase(S, ro); p.form(ro, ('sand', 'tan', 'sienna'), 90, LIGHT, density=1.4, seed=S.sd())
        for q in range(3): p.line([(x - 50, y + 305 + q * 18), (x + 40 - q * 10, y + 305 + q * 18)], 'umber', 1.6, 0.6, alpha=0.6)
        p.line([(x + 20, y + 280), (x + 60, y + 220)], 'sepia', 3, 0.8, alpha=0.9)            # the pen
        if j == 0:                                                                           # crown
            cr = p.poly([(x - 70, y - 70), (x - 70, y - 140), (x - 35, y - 105), (x, y - 155), (x + 35, y - 105), (x + 70, y - 140), (x + 70, y - 70)], smooth=False)
            erase(S, cr); p.form(cr, ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(cr, 'ochre', density=0.9, alpha=0.85)
        if j == 1:                                                                           # fisherman: a net and a fish
            for q in range(5): p.line([(x - 120 + q * 20, y + 420), (x - 40 + q * 20, y + 520)], 'tan', 2, 0.7, alpha=0.8)
            for q in range(4): p.line([(x - 125, y + 430 + q * 25), (x + 50, y + 430 + q * 25)], 'tan', 2, 0.7, alpha=0.8)
            fish = p.ellipse(x + 90, y + 470, 46, 20)
            p.form(fish, ('sky_pale', 'cornflower', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
        if j == 2:                                                                           # shepherd's staff
            stf = p.tube([(x + 150, y + 520), (x + 140, y - 60), (x + 110, y - 120), (x + 80, y - 90)], 9, 9)
            p.form(stf, WOODC, 0, LIGHT, density=1.6, seed=S.sd())
        if j == 3:                                                                           # the physician's jar of oil and a leaf
            jar = p.poly(curve([(x + 60, y + 520), (x + 50, y + 440), (x + 80, y + 410), (x + 110, y + 440), (x + 100, y + 520)], 30))
            p.form(jar, ('terracotta', 'brick', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
            p.leaves(p.blob(x - 80, y + 470, 50, 30, 0.2, seed=3), ('leaf', 'grass', 'moss'), (10, 16), 1.2, seed=S.sd())
    p.form((p.YY > 1500).astype(np.float32), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.2, seed=S.sd())
    S.save('authors')


def road():
    """a long road winding through time -- from tents in the desert to the stone city -- with old scrolls along the way"""
    S = Shot(1605); p = S.p
    sky(S, 760, (880, 260, 280))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [740, 700, 720, 690, 710, 730, 700], ('sand', 'ochre', 'tan', 'sienna'), mist=0.4)
    ground(S, 760, cols=('butter', 'sand', 'ochre', 'tan'), flowers=0)
    path = curve([(540, 1920), (300, 1650), (720, 1380), (360, 1130), (640, 930), (520, 780)], 120)
    for i in range(len(path) - 1):
        wdt = 14 + 160 * (path[i][1] - 760) / 1160
        seg = p.tube([tuple(path[i]), tuple(path[i + 1])], wdt, wdt)
        p.form(seg, ('cream', 'sand', 'butter', 'tan'), 0, LIGHT, density=1.0, seed=S.sd()) if i % 6 == 0 else None
    rd = np.zeros((H, W), np.float32)
    for i in range(0, len(path) - 1, 2):
        wdt = 14 + 160 * (path[i][1] - 760) / 1160
        rd = np.maximum(rd, p.tube([tuple(path[i]), tuple(path[min(i + 2, len(path) - 1)])], wdt, wdt))
    p.form(rd, ('cream', 'sand', 'butter', 'tan'), p.flow(90, 8), LIGHT, density=1.3, seed=S.sd())
    for (x, y, s) in ((180, 1700, 1.4), (300, 1560, 1.1)):                                # tents, near
        tn = p.poly([(x - 110 * s, y), (x, y - 120 * s), (x + 110 * s, y)])
        erase(S, tn); p.form(tn, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(tn, 'sepia', density=0.8, alpha=0.8)
    for (x, w_, h_) in ((620, 70, 120), (700, 90, 90), (520, 60, 80)):                    # a stone city, far
        m = p.rect(x - w_ / 2, 830 - h_, x + w_ / 2, 830)
        erase(S, m); p.form(m, ('cream', 'stone', 'sand', 'warmgrey'), 90, LIGHT, density=1.4, seed=S.sd()); p.edge(m, 'warmgrey', density=0.7, alpha=0.7)
    p.form(p.rect(650, 680, 750, 700), ('stone', 'warmgrey', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    for q in range(4):
        cx = 660 + q * 26; p.form(p.rect(cx - 8, 700, cx + 8, 760), ('cream', 'stone', 'sand'), 0, LIGHT, density=1.4, seed=S.sd())
    for i, (x, y, s) in enumerate(((560, 1760, 1.3), (640, 1430, 1.0), (420, 1180, 0.8), (600, 980, 0.6))):
        sc = p.rect(x - 60 * s, y - 22 * s, x + 60 * s, y + 22 * s)
        erase(S, sc); p.form(sc, ('cream', 'ivory', 'sand', 'tan'), 0, LIGHT, density=1.4, seed=S.sd())
        for e in (x - 62 * s, x + 62 * s):
            ro = p.ellipse(e, y, 10 * s, 28 * s); erase(S, ro); p.form(ro, ('sand', 'tan', 'sienna'), 90, LIGHT, density=1.4, seed=S.sd())
        p.edge(sc, 'tan', density=0.8, alpha=0.8)
    S.save('road')


def genres():
    """the kinds of writing, as playful icons: a history scroll, a harp for poems, a sealed letter, a little portrait book"""
    S = Shot(1606); p = S.p
    warm_wall(S, cols=('cream', 'butter', 'peach'))
    # history scroll (upper left)
    x, y = 300, 560
    sc = p.rect(x - 150, y - 90, x + 150, y + 90)
    erase(S, sc); p.form(sc, ('cream', 'ivory', 'sand', 'tan'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(sc, 'tan', density=0.8, alpha=0.8)
    for e in (x - 160, x + 160):
        ro = p.ellipse(e, y, 22, 105); erase(S, ro); p.form(ro, ('sand', 'tan', 'sienna'), 90, LIGHT, density=1.5, seed=S.sd()); p.edge(ro, 'sienna', density=0.8, alpha=0.8)
    for q in range(5): p.line([(x - 120, y - 60 + q * 30), (x + 110 - (q % 2) * 40, y - 60 + q * 30)], 'umber', 2, 0.6, alpha=0.6)
    # harp (upper right)
    x, y = 780, 560
    fr = np.clip(p.tube(curve([(x - 90, y + 120), (x - 100, y - 40), (x - 40, y - 130), (x + 60, y - 110), (x + 100, y - 40)], 40), 16, 16) +
                 p.tube([(x - 90, y + 120), (x + 100, y - 40)], 16, 16), 0, 1)
    erase(S, fr); p.form(fr, ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(fr, 'ochre', density=0.9, alpha=0.85)
    for q in range(7):
        xa = x - 75 + q * 22
        p.line([(xa, y - 80 + q * 4), (xa, y + 100 - q * 20)], 'stone', 1.8, 0.7, alpha=0.8)
    # sealed letter (lower left)
    x, y = 300, 960
    env = p.rect(x - 160, y - 100, x + 160, y + 100)
    erase(S, env); p.form(env, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(env, 'tan', density=0.9, alpha=0.85)
    p.line([(x - 160, y - 100), (x, y + 10), (x + 160, y - 100)], 'tan', 3, 0.8, alpha=0.85)
    p.form(p.ellipse(x, y + 10, 34, 34), ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    # little portrait book (lower right)
    x, y = 780, 960
    bk = p.rect(x - 120, y - 140, x + 120, y + 140)
    erase(S, bk); p.form(bk, ('sage', 'moss', 'pine', 'forest'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(bk, 'sepia', density=0.9, alpha=0.85)
    fr2 = p.ellipse(x, y - 10, 70, 86)
    erase(S, fr2); p.form(fr2, ('cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.ellipse(x, y - 30, 30, 32), SKIN, 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.ellipse(x, y + 40, 46, 26) * (p.YY < y + 66), ('cornflower', 'denim', 'indigo'), 0, LIGHT, density=1.4, seed=S.sd())
    p.edge(fr2, 'gold', density=0.9, alpha=0.85)
    S.save('genres')


def thread():
    """many small books joined by one golden thread, all leading to a soft warm light in the middle"""
    S = Shot(1607); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(4, 6, 500), ['powder', 'lavender', 'cream'], (60, 150), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.glow(540, 880, 520, strength=1.4, density=1.2)
    p.lift(blur(p.ellipse(540, 880, 110, 110), 20), 'white', 0.85)
    rr = np.random.default_rng(4)
    pts = []
    for j in range(14):
        a = j / 14 * 2 * np.pi + 0.3; r = rr.uniform(330, 420)
        pts.append((540 + r * np.cos(a), 880 + r * 1.15 * np.sin(a)))
    for j, (x, y) in enumerate(pts):
        pal = OLD if np.arctan2(y - 880, x - 540) > -np.pi / 2 and x < 540 or (x < 540) else NEW
        bx = (x - 34, y - 46, x + 34, y + 46)
        p.line(curve([(x, y), ((x + 540) / 2 + rr.uniform(-40, 40), (y + 880) / 2 + rr.uniform(-40, 40)), (540, 880)], 30), 'gold', 3.2, 0.85, alpha=0.9)
        book(S, *bx, pal[j % len(pal)], gold=False)
    p.line(curve([pts[i] for i in range(len(pts))] + [pts[0]], 200), 'gold', 2.4, 0.8, alpha=0.7)
    p.glow(540, 880, 200, strength=0.9, density=0.9)
    S.save('thread')


def letter_sky():
    """神様からの手紙: a warm glowing letter in its envelope floating down from the sky into open hands"""
    S = Shot(1608); p = S.p
    sky(S, 1920, (540, 300, 420))
    clouds(S, [(220, 380, 320, 70), (860, 300, 260, 60)])
    env = p.rect(400, 720, 680, 900)
    p.glow(540, 810, 300, strength=1.0, density=1.0)
    erase(S, env); p.form(env, ('white', 'cream', 'butter', 'sand'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(env, 'gold', density=0.9, alpha=0.85)
    p.line([(400, 720), (540, 820), (680, 720)], 'gold', 3, 0.8, alpha=0.9)
    hm = h.heart_mask(p, 540, 830, 26)
    p.form(hm, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    for q in range(5):
        y = 920 + q * 40; p.lift(p.ellipse(540 + (q % 2) * 30 - 15, y, 4, 4), 'butter', 0.9, tooth=0)
    for sgn, (x, ang, curl, sx) in ((-1, (450, -112, -0.5, 180)), (1, (630, -68, 0.5, 900))):
        sl = p.tube([(sx, 1980), ((sx + x) / 2, 1620), (x, 1330)], 140, 115)
        erase(S, sl); p.form(sl, COAT, p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
        p.edge(sl, 'brick', density=0.8, alpha=0.7)
    for (x, ang, curl) in ((450, -112, -0.5), (630, -68, 0.5)):
        hand(S, x, 1240, 1.9, ang, curl=curl)
    S.save('letter_sky')


def reading():
    """まずは1冊: the young woman by a sunny window, opening the first page of a book, a gentle smile"""
    S = Shot(1609); p = S.p
    ARMS = [[(430, 1000), (410, 1120), (470, 1150)], [(650, 1000), (670, 1120), (610, 1150)]]
    w = person(S, 540, 760, 160, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    hj.room(S, w['mask'], win_box=(640, 140, 1010, 640))
    beam = p.poly([(640, 640), (1010, 640), (700, 1500), (260, 1500)])
    p.hatch(beam, 70, ['butter', 'cream'], (60, 140), (1.8, 2.4), 0.8, 0.6, opacity=0.6, alpha=0.35, seed=S.sd())
    erase(S, w['mask'])
    person(S, 540, 760, 160, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, smile=True, look=(0, 0.6))
    bk = p.poly([(300, 1140), (540, 1170), (780, 1140), (790, 1260), (540, 1290), (290, 1260)])
    erase(S, bk); p.form(bk, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(bk, 'tan', density=0.9, alpha=0.85)
    p.line([(540, 1170), (540, 1290)], 'tan', 3, 0.8, alpha=0.85)
    for q in range(4):
        p.line([(330, 1175 + q * 22), (510, 1192 + q * 22)], 'pebble', 1.8, 0.6, alpha=0.6)
        p.line([(570, 1192 + q * 22), (750, 1175 + q * 22)], 'pebble', 1.8, 0.6, alpha=0.6)
    for (x, y) in ((470, 1150), (610, 1150)):
        p.form(p.ellipse(x, y, 36, 30), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    p.glow(540, 1150, 260, strength=0.5, density=0.5)
    S.save('reading')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
