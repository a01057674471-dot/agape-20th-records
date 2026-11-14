"""「福音って、なに?」 paintings -- good news that has already arrived. python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *
from PIL import Image, ImageDraw, ImageFont

def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), rel))
    m = importlib.util.module_from_spec(sp); sys.path.insert(0, os.path.dirname(sp.origin)); sp.loader.exec_module(m); return m
h = _load('h_shots', '../../handle/art_src/shots.py')
hj = _load('hj_shots', '../../hajimemashite/art_src/shots.py')
k = h.k
import pcommon
pcommon.ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art')
ARTD = pcommon.ART
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts', 'ZenMaruGothic-{}.ttf')
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4
COAT, HAIR = hj.SANGHEE, hj.HAIR


def envelope(S, cx, cy, w, glow=True):
    p = S.p
    hh = w * 0.64
    if glow: p.glow(cx, cy, w * 1.1, strength=1.0, density=1.0)
    m = p.rect(cx - w / 2, cy - hh / 2, cx + w / 2, cy + hh / 2)
    erase(S, m); p.form(m, ('white', 'cream', 'butter', 'sand'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(m, 'gold', density=0.9, alpha=0.85)
    p.line([(cx - w / 2, cy - hh / 2), (cx, cy + hh * 0.08), (cx + w / 2, cy - hh / 2)], 'gold', 3, 0.8, alpha=0.9)
    hm = h.heart_mask(p, cx, cy + hh * 0.06, w * 0.09)
    p.form(hm, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    return m


def envelope_girl():
    """the young woman tilting her head, curious; a soft glowing envelope floats beside her"""
    S = Shot(1701); p = S.p
    w = person(S, 470, 860, 165, coat=COAT, hair_style='long', plan=True)
    hj.room(S, w['mask'], win_box=(700, 160, 1010, 560))
    erase(S, w['mask'])
    person(S, 470, 860, 165, coat=COAT, hair_style='long', hair=HAIR, smile=False, look=(0.5, -0.3))
    p.line(curve([(455, 965), (470, 960), (485, 968)], 8), 'brick', 2.4, 0.8, alpha=0.9)
    envelope(S, 820, 760, 220)
    for (x, y, r) in ((740, 620, 5), (900, 640, 4), (930, 860, 5), (700, 900, 4)):
        p.lift(p.ellipse(x, y, r, r), 'white', 1.0, tooth=0); p.glow(x, y, r * 6, strength=0.5, density=0.5)
    S.save('envelope_girl')


def brush_paper():
    """a calligraphy brush on cream paper; little musical notes and warm light rising from the page (the characters go on in the edit)"""
    S = Shot(1702); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(4, 6, 500), ['apricot', 'butter', 'peach'], (60, 150), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    sheet = p.rect(130, 420, 950, 1280)
    erase(S, sheet); p.form(sheet, ('white', 'cream', 'ivory', 'paper'), 0, LIGHT, length=(60, 140), density=0.9, seed=S.sd())
    p.edge(sheet, 'tan', density=0.7, alpha=0.6)
    p.glow(540, 820, 420, strength=0.7, density=0.7)
    br = p.tube([(990, 1500), (830, 1310), (760, 1230)], 16, 14)
    erase(S, br); p.form(br, ('sand', 'tan', 'sienna'), 0, LIGHT, density=1.5, seed=S.sd())
    tip = p.poly(curve([(770, 1240), (745, 1205), (722, 1170), (745, 1195), (780, 1225)], 20), smooth=True)
    p.form(tip, ('sepia', 'umber', 'indigo'), 0, LIGHT, density=1.8, seed=S.sd())
    for (x, y, s) in ((230, 360, 1.0), (850, 300, 1.2), (180, 1350, 0.9), (930, 1380, 1.0), (500, 250, 0.8)):
        p.form(p.ellipse(x, y, 20 * s, 15 * s, rot=-20), ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
        p.line([(x + 18 * s, y), (x + 18 * s, y - 80 * s), (x + 50 * s, y - 60 * s)], 'ochre', 4 * s, 0.85, alpha=0.9)
    S.save('brush_paper')


def gogai():
    """号外: a Japanese shopping street by day; someone hands out special-edition papers, passers-by take them, surprised"""
    S = Shot(1703); p = S.p
    sky(S, 500, (850, 220, 260))
    for (x0, x1, top, c) in ((0, 360, 300, ('cream', 'sand', 'tan', 'sienna')), (720, 1080, 260, ('peach', 'apricot', 'terracotta', 'brick')),
                             (360, 720, 420, ('powder', 'sky_pale', 'cornflower', 'slate'))):
        b = p.rect(x0, top, x1, 1250)
        erase(S, b); p.form(b, c, 90, LIGHT, length=(30, 70), density=1.4, seed=S.sd()); p.edge(b, 'sepia', density=0.7, alpha=0.7)
        aw = p.rect(x0 + 10, top + 330, x1 - 10, top + 400)
        p.form(aw, ('rose', 'coral', 'brick', 'sienna') if x0 != 360 else ('sage', 'moss', 'pine', 'forest'), 0, LIGHT, density=1.5, seed=S.sd())
        for xx in range(int(x0) + 50, int(x1) - 80, 120):
            p.window(xx, top + 80, xx + 70, top + 200, panes=(2, 2), glow=0.3, seed=S.sd())
    p.form((p.YY > 1250).astype(np.float32), ('stone', 'warmgrey', 'sand', 'pebble'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    # the person handing out papers (centre), one arm raised with a paper
    figure(S, 540, 1500, 420, coat=('white', 'cream', 'ivory', 'sand'), hair=('hair', 'umber', 'sepia'), back=False, legs=('slate', 'indigo', 'umber'))
    p.form(p.rect(480, 1200, 600, 1222), ('red', 'vermilion', 'brick'), 0, LIGHT, density=1.4, seed=S.sd())     # a happi-coat band
    arm = p.tube([(600, 1180), (680, 1080), (700, 980)], 26, 22)
    erase(S, arm); p.form(arm, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(arm, 'sepia', density=0.8, alpha=0.7)
    pap = p.rect(650, 880, 790, 990)
    erase(S, pap); p.form(pap, ('white', 'ivory', 'cream'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(pap, 'warmgrey', density=0.9, alpha=0.8)
    stack = p.rect(420, 1260, 560, 1330)
    erase(S, stack); p.form(stack, ('white', 'ivory', 'cream'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(stack, 'warmgrey', density=0.9, alpha=0.8)
    for (x, y, c) in ((200, 1560, ('powder', 'cornflower', 'denim', 'indigo')), (880, 1580, ('butter', 'ochre', 'amber', 'sienna'))):
        figure(S, x, y, 380, coat=c, hair=('hair', 'umber', 'sepia'), back=False, legs=('stone', 'warmgrey', 'umber'))
        pp = p.rect(x - 60, y - 230, x + 60, y - 150)
        erase(S, pp); p.form(pp, ('white', 'ivory', 'cream'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(pp, 'warmgrey', density=0.9, alpha=0.8)
    rr = np.random.default_rng(3)
    for _ in range(6):
        x, y = rr.uniform(150, 950), rr.uniform(650, 1000)
        m = p.poly([(x, y), (x + 60, y - 14), (x + 70, y + 30), (x + 8, y + 44)])
        erase(S, m); p.form(m, ('white', 'ivory', 'cream'), 0, LIGHT, density=1.3, seed=S.sd()); p.edge(m, 'warmgrey', density=0.8, alpha=0.7)
    S.save('gogai')
    im = Image.open(os.path.join(ARTD, 'gogai.jpg')).convert('RGBA'); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((720, 935), '号外', font=ImageFont.truetype(FONT.format(900), 52), fill=(190, 50, 45, 240), anchor='mm')
    for (x, y) in ((200, 1370), (880, 1390)):
        d.text((x, y), '号外', font=ImageFont.truetype(FONT.format(900), 40), fill=(190, 50, 45, 235), anchor='mm')
    im.alpha_composite(lay); im.convert('RGB').save(os.path.join(ARTD, 'gogai.jpg'), quality=90)


def gogai_close():
    """受け取る人は、何もしていない: two hands simply receiving the special-edition paper"""
    S = Shot(1704); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-10, 6), ['cream', 'butter', 'apricot'], (60, 150), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.glow(700, 300, 500, strength=0.8, density=0.8)
    pg = p.poly([(170, 380), (900, 350), (930, 1180), (150, 1210)])
    for sgn, (x, y) in ((-1, (150, 860)), (1, (930, 840))):
        sl = p.tube([(x + sgn * 330, y + 900), (x + sgn * 150, y + 420), (x + sgn * 20, y + 110)], 120, 95)
        erase(S, sl); p.form(sl, COAT, p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd()); p.edge(sl, 'brick', density=0.8, alpha=0.7)
        hand(S, x - sgn * 10, y, 1.5, -15 if sgn < 0 else 195, curl=0.2)
    erase(S, pg); p.form(pg, ('white', 'ivory', 'cream', 'sand'), 0, LIGHT, length=(60, 120), density=1.0, seed=S.sd())
    p.edge(pg, 'warmgrey', density=0.9, alpha=0.8)
    for j in range(9):
        y = 700 + j * 50
        p.line([(230, y), (520, y - 6)], 'warmgrey', 3, 0.7, alpha=0.7); p.line([(580, y - 7), (850, y - 12)], 'warmgrey', 3, 0.7, alpha=0.7)
    for sgn, (x, y) in ((-1, (150, 860)), (1, (930, 840))):
        th = p.tube([(x + sgn * 20, y + 40), (x - sgn * 40, y - 10), (x - sgn * 80, y - 40)], 24, 19)
        erase(S, th); p.form(th, SKIN4, p.contour(th, 5, 0), LIGHT, density=1.6, warm='butter', seed=S.sd()); p.edge(th, 'sienna', density=0.9, alpha=0.85)
    S.save('gogai_close')
    im = Image.open(os.path.join(ARTD, 'gogai_close.jpg')).convert('RGBA'); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((540, 520), '号 外', font=ImageFont.truetype(FONT.format(900), 170), fill=(190, 50, 45, 240), anchor='mm')
    im.alpha_composite(lay); im.convert('RGB').save(os.path.join(ARTD, 'gogai_close.jpg'), quality=90)


def gift_door():
    """もう、何をしてくれたか: a big gift already set before a closed door, its lid open, golden light pouring out"""
    S = Shot(1705); p = S.p
    wall = (p.YY < 1350).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['stone', 'lavender', 'cream'], (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.7, seed=S.sd())
    dm = p.rect(300, 280, 780, 1350)
    erase(S, dm); p.form(dm, ('tan', 'sienna', 'brown', 'umber'), 90, LIGHT, length=(60, 140), density=1.6, seed=S.sd()); p.edge(dm, 'sepia', density=0.9, alpha=0.85)
    for x in (420, 540, 660): p.line([(x, 290), (x, 1340)], 'umber', 3, 0.7, alpha=0.7)
    p.form(p.ellipse(730, 820, 20, 20), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form((p.YY >= 1350).astype(np.float32), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    p.glow(540, 1100, 520, strength=1.3, density=1.2)
    box = p.rect(310, 1180, 770, 1560)
    erase(S, box); p.form(box, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(box, 'brick', density=0.9, alpha=0.85)
    rib = p.rect(510, 1180, 570, 1560)
    p.form(rib, ('butter', 'gold', 'amber', 'ochre'), 90, LIGHT, density=1.6, seed=S.sd())
    lid = p.poly([(280, 1180), (300, 1090), (760, 1010), (790, 1100)])
    erase(S, lid); p.form(lid, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(lid, 'brick', density=0.9, alpha=0.85)
    p.lift(blur(p.ellipse(540, 1180, 220, 50), 10), 'lemon', 0.95)
    for a in np.linspace(-150, -30, 7):
        r = np.deg2rad(a)
        ray = p.poly([(540, 1170), (540 + 900 * np.cos(r - 0.06), 1170 + 900 * np.sin(r - 0.06)), (540 + 900 * np.cos(r + 0.06), 1170 + 900 * np.sin(r + 0.06))])
        p.hatch(ray, a, ['glow', 'butter', 'cream'], (40, 120), (1.8, 2.4), 1.0, 0.62, opacity=0.6, alpha=0.4, seed=S.sd())
    S.save('gift_door')


def receive():
    """神様からのプレゼント: the young woman receiving a glowing gift in both hands, a tear and a smile"""
    S = Shot(1706); p = S.p
    ARMS = [[(430, 1000), (400, 1120), (450, 1180)], [(650, 1000), (690, 1120), (630, 1180)]]
    w = person(S, 540, 740, 165, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-3, 4), ['butter', 'cream', 'apricot'], (60, 150), (1.8, 2.5), 1.5, 0.62, seed=S.sd())
    p.glow(540, 1120, 600, strength=1.2, density=1.1)
    erase(S, w['mask'])
    person(S, 540, 740, 165, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, eyes_closed=True, smile=True)
    tear = p.blob(470, 790, 8, 14, 0.05); p.lift(tear, 'sky_pale', 0.9, tooth=0); p.edge(tear, 'cornflower', density=0.8, alpha=0.7)
    p.glow(540, 1150, 320, strength=1.0, density=1.0)
    gb = p.rect(380, 1060, 700, 1310)
    erase(S, gb); p.form(gb, ('white', 'cream', 'ivory', 'butter'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(gb, 'gold', density=0.9, alpha=0.9)
    p.form(p.rect(515, 1060, 565, 1310), ('butter', 'gold', 'amber'), 90, LIGHT, density=1.6, seed=S.sd())
    p.form(p.rect(380, 1160, 700, 1200), ('butter', 'gold', 'amber'), 0, LIGHT, density=1.6, seed=S.sd())
    for sgn in (-1, 1):
        lp = p.blob(540 + sgn * 60, 1020, 62, 38, 0.08, seed=S.sd(), rot=sgn * 20)
        erase(S, lp); p.form(lp, ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(lp, 'ochre', density=0.9, alpha=0.85)
    for (x, y) in ((385, 1250), (695, 1250)):
        hm = p.ellipse(x, y, 40, 34); erase(S, hm); p.form(hm, SKIN4, 0, LIGHT, density=1.5, seed=S.sd()); p.edge(hm, 'sienna', density=0.8, alpha=0.8)
    p.glow(540, 1190, 220, strength=0.8, density=0.8)
    S.save('receive')


def mailbox():
    """しあわせの知らせは、もう届いています: a small Japanese house at sunrise; a warm glowing letter in its mailbox"""
    S = Shot(1707); p = S.p
    sky(S, 1100, (800, 900, 480))
    p.hatch((p.YY < 1100).astype(np.float32) * smoothstep(400, 1100, p.YY), p.flow(-3, 4), ['peach', 'apricot', 'butter'], (60, 140), (1.8, 2.4), 1.0, 0.64, alpha=0.5, seed=S.sd())
    clouds(S, [(200, 380, 320, 70), (860, 300, 260, 60)])
    ground(S, 1250, flowers=60)
    hs = p.rect(120, 760, 700, 1300)
    erase(S, hs); p.form(hs, ('cream', 'sand', 'tan', 'sienna'), 90, LIGHT, length=(30, 70), density=1.4, seed=S.sd()); p.edge(hs, 'sepia', density=0.8, alpha=0.8)
    rf = p.poly([(80, 780), (410, 560), (740, 780)])
    erase(S, rf); p.form(rf, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(rf, 'sepia', density=0.9, alpha=0.85)
    p.window(200, 880, 330, 1010, panes=(2, 2), glow=0.8, seed=S.sd())
    door = p.rect(460, 1000, 600, 1300)
    p.form(door, ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    post = p.rect(840, 1120, 866, 1420)
    p.form(post, ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.5, seed=S.sd())
    mb = p.rect(760, 980, 950, 1130)
    erase(S, mb); p.form(mb, ('red', 'vermilion', 'brick', 'sienna'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(mb, 'brick', density=0.9, alpha=0.85)
    p.form(p.rect(780, 1010, 930, 1030), ('sepia', 'umber', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    env = p.poly([(800, 1020), (920, 990), (930, 1060), (810, 1080)])
    erase(S, env); p.form(env, ('white', 'cream', 'butter', 'sand'), 0, LIGHT, density=1.4, seed=S.sd()); p.edge(env, 'gold', density=0.9, alpha=0.85)
    p.glow(860, 1030, 220, strength=1.0, density=1.0)
    S.save('mailbox')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
