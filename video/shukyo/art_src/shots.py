"""「宗教って、こわい?」 paintings. python3 shots.py NAME"""
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
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4
HERE = os.path.dirname(os.path.abspath(__file__))
ARTD = os.path.join(HERE, '..', 'art')
FONT = os.path.join(HERE, '..', 'fonts', 'ZenMaruGothic-{}.ttf')


def speaker():
    """サンヒ facing us, a hand on her heart, a gentle smile, the window light behind"""
    S = Shot(1301); p = S.p
    desk = p.rect(0, 1450, 1080, 1920)
    ARMS = [[(470, 1180), (430, 1300), (520, 1260)]]
    m = person(S, 540, 900, 175, coat=hj.SANGHEE, hair_style='long', plan=True, arms=ARMS, cut=desk)
    hj.room(S, np.clip(m['mask'] + desk, 0, 1), win_box=(640, 160, 1000, 680))
    erase(S, m['mask'])
    person(S, 540, 900, 175, coat=hj.SANGHEE, hair_style='long', hair=hj.HAIR, arms=ARMS, cut=desk, smile=True, look=(0, 0.05))
    p.form(desk, ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(80, 160), density=1.5, warm='butter', avoid=m['mask'], seed=S.sd())
    p.line([(0, 1452), (1080, 1452)], 'sienna', 5, 0.8, alpha=0.8)
    p.flowers(p.blob(170, 1490, 60, 30), kinds=('daisy', 'pink'), n=8, size=(8, 12))
    S.save('speaker')


def tv():
    """そんなニュース: a dim room at night, the television glowing with a blurred, nameless news picture"""
    S = Shot(1302); p = S.p
    wall = (p.YY < 1300).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['slate', 'indigo', 'lavender'], (60, 140), (1.8, 2.5), 1.8, 0.7, alpha=0.75, seed=S.sd())
    p.form(p.rect(0, 1300, 1080, 1920), ('umber', 'sepia', 'slate', 'indigo'), 0, LIGHT, length=(60, 120), density=1.4, seed=S.sd())
    cab = p.rect(150, 1180, 930, 1360)
    erase(S, cab); p.form(cab, ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(cab, 'sepia', density=0.8, alpha=0.8)
    frame = p.rect(140, 560, 940, 1100)
    erase(S, frame); p.form(frame, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.7, seed=S.sd())
    scr = p.rect(170, 590, 910, 1070)
    erase(S, scr)
    p.hatch(scr, p.flow(0, 30, 80), ['powder', 'periwinkle', 'stone', 'lavender'], (30, 80), (2.0, 3.0), 1.8, 0.66, seed=S.sd())
    p.lift(blur(p.blob(540, 800, 160, 140, 0.3, seed=2), 30), 'cream', 0.4)
    p.form(p.rect(170, 960, 910, 1030), ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.3, seed=S.sd())
    p.form(p.rect(190, 975, 360, 1015), ('red', 'brick', 'vermilion'), 0, LIGHT, density=1.3, seed=S.sd())
    p.lift(blur(scr, 8), 'powder', 0.25)
    p.glow(540, 830, 560, colours=['powder', 'sky_pale', 'cream'], strength=0.6, density=0.6)
    p.form(p.rect(510, 1100, 570, 1180), ('slate', 'umber', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    S.save('tv')


def bill():
    """高いお金を払わされる: a long invoice on the table, a big sum circled, a pen and a cup gone cold"""
    S = Shot(1303); p = S.p
    tb = np.ones((H, W), np.float32)
    p.hatch(tb, p.flow(-4, 6), ['tan', 'sienna', 'sand'], (60, 150), (1.8, 2.5), 1.7, 0.66, seed=S.sd())
    pg = p.poly([(220, 330), (860, 300), (900, 1500), (240, 1540)])
    erase(S, pg); p.form(pg, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, length=(60, 120), density=1.0, seed=S.sd())
    p.edge(pg, 'warmgrey', density=0.8, alpha=0.7)
    rr = np.random.default_rng(3)
    for j in range(7):
        y = 620 + j * 52
        p.line([(300, y + 2 - j * 0.5), (640 + rr.uniform(-60, 40), y - 2)], 'warmgrey', 3, 0.7, alpha=0.7)
        p.line([(700, y - 3), (810, y - 5)], 'warmgrey', 3, 0.7, alpha=0.7)
    t = np.linspace(0, 2 * np.pi * 1.05, 70)
    p.line(np.stack([600 + 250 * np.cos(t), 1060 + 70 * np.sin(t)], 1), 'red', 6, 0.9, alpha=0.9)
    pen = p.tube([(880, 1660), (620, 1500)], 14, 12)
    erase(S, pen); p.form(pen, ('slate', 'indigo', 'ultramarine'), 0, LIGHT, density=1.6, seed=S.sd())
    cup = p.ellipse(220, 1700, 130, 110)
    erase(S, cup); p.form(cup, ('stone', 'warmgrey', 'pebble'), 0, LIGHT, density=1.5, seed=S.sd()); p.form(p.ellipse(220, 1700, 100, 82), ('umber', 'sepia', 'sienna'), 0, LIGHT, density=1.6, seed=S.sd())
    S.save('bill')
    im = Image.open(os.path.join(ARTD, 'bill.jpg')).convert('RGBA'); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((560, 440), '請 求 書', font=ImageFont.truetype(FONT.format(900), 76), fill=(70, 55, 45, 235), anchor='mm')
    d.text((330, 1060), '合計', font=ImageFont.truetype(FONT.format(700), 46), fill=(90, 70, 55, 230), anchor='lm')
    d.text((820, 1060), '¥3,000,000', font=ImageFont.truetype(FONT.format(900), 70), fill=(60, 45, 40, 240), anchor='rm')
    im.alpha_composite(lay); im.convert('RGB').save(os.path.join(ARTD, 'bill.jpg'), quality=90)


def alone():
    """家族と引き離される: someone alone in an empty room at dusk, hugging their knees by the window; a phone face-down"""
    S = Shot(1304); p = S.p
    wall = (p.YY < 1350).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['lavender', 'stone', 'powder'], (60, 140), (1.8, 2.5), 1.7, 0.66, alpha=0.75, seed=S.sd())
    win = p.rect(600, 250, 960, 800)
    erase(S, win)
    p.hatch(win, p.flow(-3, 4), ('dusk_sky', p.value(0.2, 1.0, 250, 800)), (40, 100), (1.8, 2.4), 1.6, 0.72, seed=S.sd())
    for x in (600, 780, 960): p.line([(x, 250), (x, 800)], 'tan', 9, 0.8, alpha=0.9)
    for y in (250, 525, 800): p.line([(600, y), (960, y)], 'tan', 9, 0.8, alpha=0.9)
    beam = p.poly([(600, 800), (960, 800), (700, 1700), (200, 1700)])
    p.hatch(beam, 70, ['peach', 'apricot'], (60, 140), (1.8, 2.4), 0.7, 0.6, opacity=0.6, alpha=0.3, seed=S.sd())
    p.form((p.YY >= 1350).astype(np.float32), ('sand', 'tan', 'warmgrey', 'umber'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    w = person(S, 470, 1000, 130, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='long', plan=True)
    erase(S, w['mask'])
    person(S, 470, 1000, 130, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='long', smile=False, look=(0.2, 0.6))
    p.line(curve([(455, 1072), (470, 1066), (485, 1072)], 8), 'brick', 2.2, 0.8, alpha=0.85)
    knees = p.blob(470, 1360, 240, 150, 0.06, seed=4)
    erase(S, knees); p.form(knees, ('cornflower', 'denim', 'indigo', 'slate'), p.contour(knees, 10, 0), LIGHT, density=1.5, seed=S.sd())
    p.edge(knees, 'sepia', density=0.8, alpha=0.75)
    arms = p.tube([(280, 1270), (470, 1300), (660, 1270)], 46, 46)
    erase(S, arms); p.form(arms, ('stone', 'warmgrey', 'slate', 'umber'), p.contour(arms, 8, 0), LIGHT, density=1.5, seed=S.sd())
    p.edge(arms, 'sepia', density=0.8, alpha=0.7)
    for x in (430, 510): p.form(p.ellipse(x, 1300, 36, 28), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    ph = p.rect(720, 1500, 840, 1560)
    erase(S, ph); p.form(ph, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd())
    S.save('alone')


def gift():
    """救いはプレゼント: a wrapped present in a pool of light, a ribbon bow, no price tag"""
    S = Shot(1305); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(4, 6, 500), ['cream', 'butter', 'apricot'], (60, 150), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.glow(540, 1000, 600, strength=1.1, density=1.0)
    p.form((p.YY > 1300).astype(np.float32), ('sand', 'tan', 'apricot', 'sienna'), 0, LIGHT, length=(60, 120), density=1.2, seed=S.sd())
    bx0, by0, bx1, by1 = 300, 900, 780, 1360
    box = p.rect(bx0, by0, bx1, by1); lid = p.rect(bx0 - 24, by0 - 90, bx1 + 24, by0)
    erase(S, np.clip(box + lid, 0, 1))
    p.form(box, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form(lid, ('pink', 'rose', 'coral', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    mx = (bx0 + bx1) / 2
    rib = np.clip(p.rect(mx - 32, by0 - 90, mx + 32, by1), 0, 1)
    p.form(rib, ('butter', 'gold', 'amber', 'ochre'), 90, LIGHT, density=1.6, seed=S.sd())
    for sgn in (-1, 1):
        loop = p.blob(mx + sgn * 95, by0 - 150, 95, 60, 0.08, seed=S.sd(), rot=sgn * 20)
        erase(S, loop); p.form(loop, ('butter', 'gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(loop, 'ochre', density=0.9, alpha=0.8)
    p.form(p.ellipse(mx, by0 - 120, 34, 30), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    for m in (box, lid): p.edge(m, 'brick', width=(1.6, 2.2), density=0.9, alpha=0.8)
    p.lift(blur(p.rect(bx0, by0, bx0 + 120, by1), 12), 'white', 0.2)
    S.save('gift')


def church():
    """正直に: a small church on the rise at dusk, a cross on its steeple, warm light in the windows"""
    S = Shot(1306); p = S.p
    m = (p.YY < 1200).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ('dusk_sky', np.clip(p.value(0.0, 1.0, 0, 1200) * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.8, 0.76, seed=S.sd())
    clouds(S, [(220, 420, 300, 60), (860, 300, 260, 50)])
    hill = p.below([0, 400, 800, 1080], [1260, 1180, 1200, 1250])
    p.form(hill, ('sage', 'moss', 'pine', 'forest'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.4, seed=S.sd())
    body = p.rect(380, 900, 760, 1230)
    roof = p.poly([(350, 910), (570, 720), (790, 910)])
    tower = p.rect(470, 560, 590, 920); spire = p.poly([(450, 570), (530, 390), (610, 570)])
    sil = np.clip(body + roof + tower + spire, 0, 1)
    erase(S, sil)
    p.form(np.clip(body + tower, 0, 1), ('cream', 'sand', 'tan', 'sienna'), 90, LIGHT, density=1.4, seed=S.sd())
    p.form(np.clip(roof + spire, 0, 1), ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.edge(sil, 'sepia', density=0.9, alpha=0.85)
    cr = np.clip(p.rect(523, 300, 537, 400) + p.rect(500, 330, 560, 344), 0, 1)
    p.form(cr, ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.7, seed=S.sd())
    for (x0, y0, x1, y1) in ((420, 980, 480, 1100), (660, 980, 720, 1100), (505, 640, 555, 740)):
        p.window(x0, y0, x1, y1, panes=(1, 2), glow=0.9, seed=S.sd())
    door = p.poly(curve([(540, 1230), (540, 1080), (575, 1040), (610, 1080), (610, 1230)], 30))
    p.form(door, ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
    p.form((p.YY > 1250).astype(np.float32), ('moss', 'pine', 'forest', 'sepia'), 0, LIGHT, length=(40, 90), density=1.4, seed=S.sd())
    for x, hh in ((150, 420), (930, 380)):
        p.tree(x, 1300, hh, 120, colours=('sage', 'moss', 'pine', 'forest'), clumps=6, seed=S.sd())
    S.save('church')


def door():
    """ドアの外に立ってノックして: a closed wooden door at evening; a hand knocks; warm light glows round its edges"""
    S = Shot(1307); p = S.p
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['stone', 'lavender', 'warmgrey'], (60, 140), (1.8, 2.5), 1.7, 0.66, alpha=0.75, seed=S.sd())
    X0, Y0, X1, Y1 = 260, 380, 820, 1560
    p.lift(blur(p.rect(X0 - 14, Y0 - 14, X1 + 14, Y1), 10), 'butter', 0.7)
    p.glow(540, 970, 520, strength=0.6, density=0.6)
    dm = p.rect(X0, Y0, X1, Y1)
    erase(S, dm); p.form(dm, ('tan', 'sienna', 'brown', 'umber'), 90, LIGHT, length=(60, 140), density=1.6, seed=S.sd())
    for x in np.linspace(X0 + 90, X1 - 90, 4): p.line([(x, Y0 + 10), (x, Y1 - 10)], 'umber', 3, 0.7, alpha=0.7)
    p.edge(dm, 'sepia', density=0.9, alpha=0.85)
    p.lift(p.rect(X0, Y1 - 8, X1, Y1 + 6), 'lemon', 0.9, tooth=0)                     # light under the door
    p.lift(blur(p.rect(X0 - 40, Y1, X1 + 40, Y1 + 120) * smoothstep(Y1 + 120, Y1, p.YY), 12), 'butter', 0.6)
    p.form(p.ellipse(760, 1000, 22, 22), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form((p.YY > Y1 + 6).astype(np.float32) * (1 - blur(p.rect(X0 - 40, Y1, X1 + 40, Y1 + 120), 12)), ('stone', 'warmgrey', 'umber'), 0, LIGHT, density=1.2, seed=S.sd())
    sl = p.tube([(1160, 1300), (980, 980), (800, 850)], 120, 95)
    erase(S, sl); p.form(sl, ('white', 'cream', 'ivory', 'sand'), p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
    p.edge(sl, 'tan', density=0.8, alpha=0.7)
    fist = p.blob(720, 800, 95, 80, 0.06, seed=7, rot=-20)
    knuck = np.clip(sum(p.ellipse(650 + j * 8, 735 + j * 34, 34, 26) for j in range(4)), 0, 1)
    fm = np.clip(fist + knuck, 0, 1)
    erase(S, fm); p.form(fm, SKIN4, p.contour(fm, 6), LIGHT, density=1.6, warm='butter', seed=S.sd()); p.edge(fm, 'sienna', density=0.9, alpha=0.85)
    for j in range(3): p.line([(668 + j * 8, 752 + j * 34), (720 + j * 6, 760 + j * 30)], 'skin_shade', 2.0, 0.6, alpha=0.7)
    for (r0, r1) in ((40, 70), (80, 110)):
        t = np.linspace(2.4, 3.9, 12)
        p.line(np.stack([630 + r0 * np.cos(t), 800 + r0 * np.sin(t)], 1), 'sepia', 3, 0.7, alpha=0.6)
    S.save('door')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
