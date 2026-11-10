"""Christmas special 1 「クリスマスは、イエスの誕生日…じゃない?」 paintings. python3 shots.py NAME"""
import sys, json, importlib.util
from tcommon import *
from PIL import Image, ImageDraw, ImageFont

_k = importlib.util.spec_from_file_location('k_shots', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'kamisama', 'art_src', 'shots.py'))
k = importlib.util.module_from_spec(_k); sys.path.insert(0, os.path.dirname(_k.origin)); _k.loader.exec_module(k)
erase, figure, sky_day = k.erase, k.figure, k.sky
HERE = os.path.dirname(os.path.abspath(__file__))
ARTD = os.path.join(HERE, '..', 'art')
FONT = os.path.join(HERE, '..', 'fonts', 'ZenMaruGothic-{}.ttf')
NIGHT = ('ultramarine', 'indigo', 'slate', 'violet')


def night_sky(S, region, low_glow=True):
    p = S.p
    v = p.value(0.0, 1.0, 0, int(H * 0.75))
    p.hatch(region, p.flow(-3, 4), ['indigo', 'ultramarine', 'slate'], (60, 150), (1.8, 2.6), 1.8, 0.8, seed=S.sd())
    p.hatch(region * v, p.flow(-2, 4), ['violet', 'cobalt', 'periwinkle'], (60, 140), (1.8, 2.4), 1.0, 0.7, alpha=0.6, seed=S.sd())
    if low_glow:
        p.hatch(region * smoothstep(0.55, 1.0, v), p.flow(-2, 4), ['lavender', 'mauve', 'peach'], (60, 140), (1.8, 2.4), 0.8, 0.66,
                opacity=0.5, alpha=0.45, seed=S.sd())


def stars(S, region, n=120, seed=1, big=()):
    p = S.p; r = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        x, y = r.uniform(20, 1060), r.uniform(20, 1300)
        if region[int(y), int(x)] > 0.5: pts.append((x, y))
    for x, y in pts:
        s = r.uniform(2, 5)
        p.lift(p.ellipse(x, y, s, s), 'cream', r.uniform(0.6, 0.95), tooth=0.2)
    for (x, y, s) in big:
        star(S, x, y, s)


def star(S, x, y, s):
    p = S.p
    p.glow(x, y, s * 5, strength=0.9, density=0.9)
    for a in (0, 90, 45, 135):
        r = np.deg2rad(a); L = s * (2.4 if a in (0, 90) else 1.2)
        p.line([(x - L * np.cos(r), y - L * np.sin(r)), (x + L * np.cos(r), y + L * np.sin(r))], 'white', s * (0.22 if a in (0, 90) else 0.14), 0.9, alpha=0.95)
    p.lift(p.ellipse(x, y, s * 0.5, s * 0.5), 'white', 1.0, tooth=0)


def building(S, x0, x1, top, base, wall, roof, wins, lit=True):
    p = S.p
    m = p.rect(x0, top, x1, base)
    p.form(m, wall, 90, LIGHT, length=(30, 70), density=1.4, seed=S.sd())
    p.form(p.rect(x0 - 12, top - 40, x1 + 12, top + 6), roof, 0, LIGHT, density=1.4, seed=S.sd())
    p.edge(m, 'sepia', width=(1.6, 2.4), density=0.9, alpha=0.8)
    for (a, b, c, d) in wins:
        p.window(a, b, c, d, panes=(2, 2), glow=0.9 if lit else 0.5, seed=S.sd())
    return m


def street(lit):
    """illuminated shopping street at night: shops either side, a tall tree hung with lights, light strings across the street"""
    S = Shot(901); p = S.p
    skym = (p.YY < 1100).astype(np.float32)
    night_sky(S, skym)
    stars(S, skym * (p.YY < 900), 50, 3)
    shopL = [(0, 380, 640, 1500, ('peach', 'apricot', 'terracotta', 'brick'), ('slate', 'indigo', 'umber', 'sepia'), [(50, 760, 170, 900), (210, 760, 330, 900), (60, 1180, 320, 1400)]),
             (700, 1080, 700, 1500, ('cream', 'sand', 'tan', 'sienna'), ('brick', 'terracotta', 'sienna', 'brown'), [(760, 820, 880, 960), (920, 820, 1040, 960), (760, 1180, 1030, 1400)])]
    for (x0, x1, top, base, w, r, wins) in shopL:
        building(S, x0, x1, top, base, w, r, wins)
    road = p.rect(0, 1500, 1080, 1920)
    p.form(road, ('stone', 'warmgrey', 'slate', 'umber'), p.flow(0, 6), LIGHT, length=(40, 90), density=1.4, seed=S.sd())
    for (x, y) in ((470, 1700), (610, 1760), (250, 1820), (860, 1800)):
        p.lift(blur(p.ellipse(x, y, 120, 26), 8), 'butter', 0.25)      # light pooling on the pavement
    tree = p.poly([(540, 430), (400, 900), (450, 900), (360, 1250), (420, 1250), (320, 1520), (760, 1520), (660, 1250), (720, 1250), (630, 900), (680, 900)])
    p.form(tree, ('pine', 'forest', 'moss', 'sepia'), p.flow(-30, 30), LIGHT, length=(14, 30), density=1.6, seed=S.sd())
    p.edge(tree, 'sepia', width=(1.4, 2.0), density=0.7, alpha=0.6)
    p.form(p.rect(515, 1520, 565, 1600), ('sienna', 'brown', 'umber'), 90, LIGHT, density=1.4, seed=S.sd())
    for (x, y, coat) in ((200, 1760, ('rose', 'coral', 'brick', 'sienna')), (300, 1790, ('powder', 'cornflower', 'denim', 'indigo')),
                         (850, 1780, ('butter', 'ochre', 'amber', 'sienna'))):
        figure(S, x, y, 250, coat=coat, back=True)
    # the star on top -- drawn in both versions (lit or not)
    star(S, 540, 410, 18)
    # bulbs: strings across the street + spiral on the tree + along the eaves
    bulbs = []
    for (y0, sag) in ((260, 120), (520, 90)):
        for t in np.linspace(0.02, 0.98, 22):
            bulbs.append((1080 * t, y0 + sag * 4 * t * (1 - t) * 1.0))
    for t in np.linspace(0.05, 0.95, 40):
        y = 470 + t * 1040; half = 30 + t * 190
        bulbs.append((540 + half * np.sin(t * 22), y))
    for x in np.linspace(20, 360, 9): bulbs.append((x, 655))
    for x in np.linspace(720, 1060, 9): bulbs.append((x, 715))
    for (x0, x1, y0, sag) in ((0, 1080, 260, 120), (0, 1080, 520, 90)):
        t = np.linspace(0, 1, 80)
        p.line(np.stack([x0 + (x1 - x0) * t, y0 + sag * 4 * t * (1 - t)], 1), 'sepia', 1.6, 0.6, alpha=0.6)
    cols = ['glow', 'lantern', 'flame', 'sun']
    for i, (x, y) in enumerate(bulbs):
        if lit:
            p.glow(x, y, 26, strength=0.8, density=0.7, length=(4, 10))
            p.lift(p.ellipse(x, y, 6, 6), 'white', 0.95, tooth=0)
        else:
            p.form(p.ellipse(x, y, 5, 5), ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.4, seed=1)
    if lit:
        p.glow(540, 1000, 520, strength=0.45, density=0.5)
    S.save('street_on' if lit else 'street_off')
    if lit:
        json.dump([(float(x), float(y)) for x, y in bulbs], open(os.path.join(ARTD, 'bulbs.json'), 'w'))


def street_on(): street(True)
def street_off(): street(False)


def table():
    """the Christmas table: a strawberry cake, roast chicken, a wrapped present, candlelight, the window at night"""
    S = Shot(902); p = S.p
    ari_room = k.ari.room
    ari_room(S, np.zeros((H, W), np.float32), win_box=(620, 140, 1000, 620), wall_to=1150)
    win = p.rect(620, 140, 1000, 620)
    p.hatch(win, p.flow(-3, 4), ['indigo', 'ultramarine', 'slate'], (40, 100), (1.7, 2.4), 1.8, 0.8, seed=S.sd())
    stars(S, win, 14, 5)
    for x in (620, 810, 1000): p.line([(x, 140), (x, 620)], 'tan', 9.0, 0.8, alpha=0.9)
    for y in (140, 380, 620): p.line([(620, y), (1000, y)], 'tan', 9.0, 0.8, alpha=0.9)
    # garland on the wall
    t = np.linspace(0, 1, 60)
    gl = p.tube(np.stack([60 + 460 * t, 220 + 90 * np.sin(t * np.pi)], 1), 22, 22)
    p.leaves(gl, ('pine', 'forest', 'moss'), (8, 14), 1.4, seed=S.sd())
    for tt in np.linspace(0.1, 0.9, 6):
        p.form(p.ellipse(60 + 460 * tt, 230 + 90 * np.sin(tt * np.pi), 11, 11), ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    cloth = p.rect(0, 1150, 1080, 1920)
    p.form(cloth, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    for x in range(0, 1080, 120):                # a red check runner down the middle
        pass
    runner = p.rect(0, 1300, 1080, 1520)
    p.form(runner, ('rose', 'red', 'brick', 'sienna'), 0, LIGHT, length=(40, 100), density=1.3, seed=S.sd())
    for x in range(40, 1080, 90): p.line([(x, 1300), (x, 1520)], 'cream', 3, 0.6, alpha=0.5)
    # cake (centre)
    cx, cy = 560, 1240
    plate = p.ellipse(cx, cy + 150, 270, 60)
    erase(S, plate); p.form(plate, ('white', 'powder', 'sky_pale', 'stone'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(plate, 'warmgrey', density=0.8, alpha=0.7)
    side = p.rect(cx - 220, cy - 40, cx + 220, cy + 140) + p.ellipse(cx, cy + 140, 220, 50)
    top = p.ellipse(cx, cy - 40, 220, 50)
    body = np.clip(side, 0, 1) * (1 - top * (p.YY < cy - 40))
    erase(S, np.clip(side + top, 0, 1))
    p.form(body, ('white', 'cream', 'ivory', 'sand'), 90, LIGHT, length=(14, 30), density=1.5, seed=S.sd())
    p.form(p.rect(cx - 220, cy + 30, cx + 220, cy + 60) * body, ('rose', 'red', 'pink'), 0, LIGHT, density=1.4, seed=S.sd())   # strawberry layer
    p.form(top, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.5, seed=S.sd())
    p.edge(np.clip(side + top, 0, 1), 'warmgrey', width=(1.4, 2.0), density=0.9, alpha=0.75)
    for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
        sx, sy = cx + 160 * np.cos(a), cy - 40 + 34 * np.sin(a)
        b = p.blob(sx, sy - 8, 22, 22, 0.1, seed=S.sd())
        p.form(b, ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
        p.form(p.ellipse(sx, sy - 28, 12, 6), ('leaf', 'grass', 'moss'), 0, LIGHT, density=1.4, seed=S.sd())
    for (x, h) in ((cx - 60, 110), (cx + 10, 130), (cx + 80, 110)):
        cm = p.rect(x - 9, cy - 40 - h, x + 9, cy - 40)
        p.form(cm, ('powder', 'cornflower', 'white'), 90, LIGHT, density=1.4, seed=S.sd())
        p.glow(x, cy - 40 - h - 22, 70, strength=0.9, density=0.9)
        p.form(p.blob(x, cy - 40 - h - 22, 9, 18, 0.05, seed=S.sd()), ('lemon', 'sun', 'flame'), 0, LIGHT, density=1.6, seed=S.sd())
    # roast chicken (left)
    pl2 = p.ellipse(190, 1620, 200, 64)
    erase(S, pl2); p.form(pl2, ('white', 'powder', 'stone'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(pl2, 'warmgrey', density=0.8, alpha=0.7)
    for (x, y, rot) in ((140, 1560, -20), (250, 1580, 25)):
        leg = p.blob(x, y, 80, 54, 0.08, seed=S.sd(), rot=rot)
        p.form(leg, ('amber', 'ochre', 'sienna', 'brown'), p.contour(leg, 6), LIGHT, length=(8, 18), density=1.6, warm='butter', seed=S.sd())
        p.edge(leg, 'brown', density=0.9, alpha=0.8)
        bx, by = x + 80 * np.cos(np.deg2rad(rot - 60)), y + 80 * np.sin(np.deg2rad(rot - 60))
        bone = p.tube([(x, y), (bx, by)], 11, 10)
        erase(S, bone); p.form(bone, ('white', 'cream', 'ivory'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(bone, 'tan', density=0.9, alpha=0.9)
        for sg in (-1, 1): p.form(p.ellipse(bx + sg * 9, by - 6, 11, 11), ('white', 'cream', 'ivory'), 0, LIGHT, density=1.5, seed=S.sd())
    p.leaves(p.blob(200, 1660, 140, 20, 0.2, seed=3), ('leaf', 'grass', 'moss'), (8, 14), 1.0, seed=S.sd())
    # present (right)
    bx0, by0, bx1, by1 = 760, 1500, 1010, 1720
    box = p.rect(bx0, by0, bx1, by1)
    lid = p.rect(bx0 - 14, by0 - 50, bx1 + 14, by0)
    erase(S, np.clip(box + lid, 0, 1))
    p.form(box, ('powder', 'cornflower', 'cobalt', 'ultramarine'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(lid, ('sky_pale', 'powder', 'cornflower', 'cobalt'), 0, LIGHT, density=1.5, seed=S.sd())
    rib = np.clip(p.rect((bx0 + bx1) / 2 - 18, by0 - 50, (bx0 + bx1) / 2 + 18, by1), 0, 1)
    p.form(rib, ('butter', 'gold', 'amber', 'ochre'), 90, LIGHT, density=1.6, seed=S.sd())
    mx = (bx0 + bx1) / 2
    for sgn in (-1, 1):
        loop = p.blob(mx + sgn * 50, by0 - 80, 50, 32, 0.08, seed=S.sd(), rot=sgn * 20)
        p.form(loop, ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(loop, 'ochre', density=0.9, alpha=0.8)
    for m in (box, lid): p.edge(m, 'indigo', width=(1.4, 2.0), density=0.9, alpha=0.75)
    p.glow(560, 1060, 420, strength=0.5, density=0.6)
    # lift the whole table 300 px so it fills the frame above the subtitles; fresh tablecloth below
    p.C[:-300] = p.C[300:].copy()
    low = p.rect(0, 1600, 1080, 1920)
    erase(S, low)
    p.form(low, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    S.save('table')


def calendar():
    """a wall calendar on December, 25 circled in red, a sprig of holly; morning light"""
    S = Shot(903); p = S.p
    k.ari.room(S, np.zeros((H, W), np.float32), win_box=(-400, -400, -300, -300), wall_to=1920)
    X0, Y0, X1, Y1 = 150, 300, 930, 1500
    page = p.rect(X0, Y0, X1, Y1)
    erase(S, p.rect(X0 + 12, Y0 + 12, X1 + 16, Y1 + 18))
    p.form(p.rect(X0 + 12, Y0 + 12, X1 + 16, Y1 + 18), ('tan', 'sienna', 'sienna'), 0, LIGHT, density=0.6, seed=S.sd())   # shadow
    erase(S, page)
    p.form(page, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, length=(40, 90), density=1.2, seed=S.sd())
    p.form(p.rect(X0, Y0, X1, Y0 + 230), ('rose', 'red', 'brick', 'sienna'), 0, LIGHT, length=(40, 90), density=1.4, seed=S.sd())
    p.edge(page, 'warmgrey', width=(1.4, 2.0), density=0.9, alpha=0.7)
    for x in np.linspace(X0 + 80, X1 - 80, 6):
        p.line([(x, Y0 - 30), (x, Y0 + 20)], 'warmgrey', 7, 0.8, alpha=0.9)
    p.line([(540, Y0 - 30), (540, 160)], 'sepia', 3, 0.7, alpha=0.8)
    p.form(p.ellipse(540, 150, 14, 14), ('stone', 'warmgrey', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    # grid geometry (Dec 2026 starts on a Tuesday; Sunday first)
    gx0, gy0, cw, ch = X0 + 30, Y0 + 340, (X1 - X0 - 60) / 7, 165
    pos = {}
    for d in range(1, 32):
        i = d + 1; c, r = i % 7, i // 7
        pos[d] = (gx0 + cw * (c + 0.5), gy0 + ch * r + ch * 0.45)
    cx, cy = pos[25]
    t = np.linspace(0, 2 * np.pi * 1.08, 70)
    p.line(np.stack([cx + 58 * np.cos(t) * (1 + 0.05 * t), cy + 50 * np.sin(t)], 1), 'red', 6, 0.9, alpha=0.95)
    # holly sprig on the top corner
    for (x, y, rot) in ((830, 250, 30), (890, 300, -20), (790, 320, 70)):
        lf = p.blob(x, y, 56, 26, 0.12, seed=S.sd(), rot=rot)
        p.form(lf, ('leaf', 'grass', 'forest', 'pine'), rot, LIGHT, density=1.6, seed=S.sd()); p.edge(lf, 'forest', density=0.9, alpha=0.8)
    for (x, y) in ((840, 300), (865, 318), (835, 330)):
        p.form(p.ellipse(x, y, 15, 15), ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    S.save('calendar')
    # the printed numbers, set in type (pencil-grey, a little soft)
    im = Image.open(os.path.join(ARTD, 'calendar.jpg')).convert('RGBA')
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((540, Y0 + 115), '12', font=ImageFont.truetype(FONT.format(900), 130), fill=(255, 250, 238, 240), anchor='mm')
    d.text((540, Y0 + 195), 'DECEMBER', font=ImageFont.truetype(FONT.format(700), 40), fill=(255, 250, 238, 220), anchor='mm')
    fw = ImageFont.truetype(FONT.format(700), 34)
    for c, wd in enumerate('日月火水木金土'):
        d.text((gx0 + cw * (c + 0.5), gy0 - 45), wd, font=fw, fill=(196, 68, 58, 230) if c == 0 else (106, 74, 51, 220), anchor='mm')
    fn = ImageFont.truetype(FONT.format(700), 54)
    for dd, (x, y) in pos.items():
        col = (196, 68, 58, 235) if (dd + 1) % 7 == 0 or dd == 25 else (92, 64, 48, 225)
        d.text((x, y), str(dd), font=fn, fill=col, anchor='mm')
    im.alpha_composite(lay); im.convert('RGB').save(os.path.join(ARTD, 'calendar.jpg'), quality=90)


def stable(beam=False):
    """a starry night over the hills, a small stable with warm light inside, the great star above;
    beam=True: the star's light pouring down onto the earth"""
    S = Shot(904); p = S.p
    skym = (p.YY < 1350).astype(np.float32)
    night_sky(S, skym)
    stars(S, skym * (p.YY < 1150), 160, 7)
    hills = p.below([0, 300, 640, 1080], [1300, 1240, 1290, 1220])
    p.form(hills, ('slate', 'indigo', 'violet', 'sepia'), p.flow(-6, 10), LIGHT, length=(30, 70), density=1.5, seed=S.sd())
    near = p.below([0, 400, 800, 1080], [1560, 1520, 1550, 1500])
    p.form(near, ('indigo', 'slate', 'sepia', 'umber'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.6, seed=S.sd())
    # the stable: posts, a thatched roof, light from the open front
    sx, sy = 540, 1520
    roof = p.poly([(sx - 260, sy - 250), (sx, sy - 420), (sx + 260, sy - 250), (sx + 230, sy - 230), (sx - 230, sy - 230)])
    inside = p.rect(sx - 200, sy - 240, sx + 200, sy)
    p.form(inside, ('lantern', 'glow', 'apricot', 'amber'), 0, LIGHT, density=1.4, seed=S.sd())
    p.glow(sx, sy - 100, 260, strength=1.0, density=1.0)
    # Mary, Joseph and the manger, as small dark shapes against the light
    for (x, h) in ((sx - 110, 170), (sx + 120, 190)):
        b = p.poly(curve([(x - 40, sy - 5), (x - 34, sy - h * 0.6), (x, sy - h * 0.8), (x + 34, sy - h * 0.6), (x + 40, sy - 5)], 30), smooth=True)
        p.form(np.clip(b + p.ellipse(x, sy - h * 0.86, 24, 26), 0, 1), ('slate', 'indigo', 'umber', 'sepia'), 90, LIGHT, density=1.5, seed=S.sd())
    mg = p.poly([(sx - 60, sy - 70), (sx + 60, sy - 70), (sx + 40, sy - 10), (sx - 40, sy - 10)])
    p.form(mg, ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(p.ellipse(sx, sy - 76, 46, 14), ('butter', 'cream', 'white'), 0, LIGHT, density=1.4, seed=S.sd())
    p.glow(sx, sy - 80, 90, strength=0.8, density=0.8)
    for x in (sx - 220, sx + 220):
        p.form(p.rect(x - 14, sy - 250, x + 14, sy), ('brown', 'umber', 'sepia'), 90, LIGHT, density=1.5, seed=S.sd())
    p.form(roof, ('ochre', 'sienna', 'brown', 'umber'), p.flow(60, 10), LIGHT, length=(20, 50), density=1.6, seed=S.sd())
    p.edge(roof, 'sepia', density=0.9, alpha=0.85)
    # a few sheep and a palm for place
    for (x, y) in ((190, 1590), (270, 1610), (860, 1600)):
        sh = p.blob(x, y, 46, 30, 0.15, seed=S.sd())
        p.form(sh, ('cream', 'ivory', 'stone'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(sh, 'warmgrey', density=0.8, alpha=0.7)
        p.form(p.ellipse(x - 40, y - 8, 14, 12), ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.4, seed=S.sd())
    ground = (p.YY > 1640).astype(np.float32)
    p.form(ground * (1 - near * 0), ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, length=(40, 90), density=1.3, seed=S.sd())
    star(S, 540, 330, 30)
    if beam:
        bm = p.poly([(510, 340), (570, 340), (sx + 280, sy - 300), (sx - 280, sy - 300)]) * smoothstep(sy - 260, 360, p.YY)
        p.hatch(bm, 90, ['glow', 'butter', 'cream'], (60, 160), (1.8, 2.4), 1.2, 0.66, opacity=0.6, alpha=0.5, seed=S.sd())
        p.lift(blur(bm, 24), 'butter', 0.35)
        r = np.random.default_rng(11)
        for _ in range(26):                          # sparkles drifting down in the light
            y = r.uniform(420, sy - 320); half = 30 + (y - 340) / (sy - 640) * 250
            x = 540 + r.uniform(-half, half) * 0.8
            star(S, x, y, r.uniform(4, 9))
        p.glow(sx, sy - 280, 360, strength=0.7, density=0.7)
    S.save('starlight' if beam else 'stable')


def starlight(): stable(True)
def stable_(): stable(False)


def candle():
    """two hands cupped round a single lit candle in the dark"""
    S = Shot(905); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-20, 10), ['indigo', 'slate', 'umber', 'sepia'], (60, 150), (1.8, 2.6), 2.0, 0.84, seed=S.sd())
    p.glow(540, 760, 620, strength=1.1, density=1.0)
    p.lift(blur(p.ellipse(540, 900, 520, 640), 60), 'amber', 0.3)
    cm = p.rect(485, 760, 595, 1330)
    sleeves = [p.tube([(-40, 1960), (180, 1640), (360, 1430)], 170, 130), p.tube([(1120, 1960), (900, 1640), (720, 1430)], 170, 130)]
    hands = [p.blob(455, 1340, 150, 105, 0.06, seed=4, rot=-25), p.blob(625, 1355, 150, 105, 0.06, seed=5, rot=25)]
    thumbs = [p.tube([(470, 1290), (478, 1210), (488, 1160)], 30, 24), p.tube([(610, 1300), (602, 1215), (592, 1165)], 30, 24)]
    erase(S, np.clip(cm + sleeves[0] + sleeves[1] + hands[0] + hands[1] + thumbs[0] + thumbs[1], 0, 1))
    p.form(cm, ('white', 'cream', 'ivory', 'sand'), 90, LIGHT, length=(14, 30), density=1.5, warm='butter', seed=S.sd())
    p.form(p.ellipse(540, 760, 55, 14), ('cream', 'butter', 'sand'), 0, LIGHT, density=1.4, seed=S.sd())
    p.edge(cm, 'tan', density=0.9, alpha=0.8)
    p.line(curve([(560, 762), (566, 800), (562, 840)], 10), 'butter', 6, 0.8, alpha=0.8)        # a wax drip
    for sl in sleeves:
        p.form(sl, ('rose', 'coral', 'brick', 'sienna'), p.contour(sl, 10, 90), LIGHT, length=(16, 36), density=1.5, warm='butter', seed=S.sd())
        p.edge(sl, 'sepia', density=0.8, alpha=0.75)
    for k2, (h, th) in enumerate(zip(hands, thumbs)):
        sgn = -1 if k2 == 0 else 1
        hm = np.clip(h + th, 0, 1)
        erase(S, hm)
        p.form(hm, ('peach', 'skin', 'skin_shade', 'apricot'), p.contour(hm, 8, 90), LIGHT, length=(10, 20), density=1.6, warm='butter', seed=S.sd())
        p.edge(hm, 'sienna', width=(1.4, 2.0), density=0.9, alpha=0.85)
        cx0 = 455 if k2 == 0 else 625
        for j in range(3):                            # the fingers curled round the front
            y = 1320 + j * 34
            p.line(curve([(cx0 - sgn * 120, y - 20 + j * 4), (cx0 - sgn * 40, y + 6), (cx0 + sgn * 40, y + 2)], 12), 'skin_shade', 2.2, 0.7, alpha=0.7)
    p.lift(blur(np.clip(hands[0] + hands[1] + thumbs[0] + thumbs[1], 0, 1) * (p.YY < 1330), 10), 'butter', 0.22)
    p.line([(540, 760), (540, 728)], 'sepia', 4, 0.9, alpha=0.95)
    p.glow(540, 670, 220, strength=1.4, density=1.2)
    fl = p.poly(curve([(540, 570), (562, 640), (558, 700), (540, 725), (522, 700), (518, 640), (540, 570)], 40), smooth=True)
    p.lift(fl, 'lemon', 0.95, tooth=0)
    p.lift(p.blob(540, 692, 10, 22, 0.05), 'white', 1.0, tooth=0)
    S.save('candle')


if __name__ == '__main__':
    n = sys.argv[1]
    globals()['stable_' if n == 'stable' else n]()
