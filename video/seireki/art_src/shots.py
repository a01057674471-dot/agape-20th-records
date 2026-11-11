"""「2026年って、何から数えてる?」 paintings. python3 shots.py NAME"""
import sys, importlib.util
from tcommon import *
from PIL import Image, ImageDraw, ImageFont

def _load(name, rel):
    sp = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), rel))
    m = importlib.util.module_from_spec(sp); sys.path.insert(0, os.path.dirname(sp.origin)); sp.loader.exec_module(m); return m
h = _load('h_shots', '../../handle/art_src/shots.py')
k = h.k
erase, figure, sky, ground, ridge, RIDGES, hand, SKIN4 = k.erase, k.figure, k.sky, k.ground, k.ridge, k.RIDGES, h.hand, h.SKIN4
HERE = os.path.dirname(os.path.abspath(__file__))
ARTD = os.path.join(HERE, '..', 'art')
FONT = os.path.join(HERE, '..', 'fonts', 'ZenMaruGothic-{}.ttf')
ROBE = ('white', 'cream', 'ivory', 'sand')


def calendar26():
    """2026: a wall calendar above the desk and a phone on it, both showing the year"""
    S = Shot(1201); p = S.p
    k.ari.room(S, np.zeros((H, W), np.float32), win_box=(700, 160, 1010, 560), wall_to=1250)
    p.form(p.rect(0, 1250, 1080, 1920), ('sand', 'tan', 'sienna', 'brown'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    cal = p.rect(130, 300, 610, 1000)
    erase(S, cal); p.form(cal, ('white', 'cream', 'ivory', 'sand'), 0, LIGHT, density=1.1, seed=S.sd())
    p.form(p.rect(130, 300, 610, 480), ('sky_pale', 'powder', 'cornflower', 'cobalt'), 0, LIGHT, density=1.4, seed=S.sd())
    p.edge(cal, 'warmgrey', density=0.9, alpha=0.8)
    for x in np.linspace(180, 560, 5): p.line([(x, 280), (x, 320)], 'warmgrey', 7, 0.8, alpha=0.9)
    ph = p.rect(560, 1330, 860, 1820)
    erase(S, ph); p.form(ph, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    scr = p.rect(580, 1360, 840, 1790); p.lift(scr, 'sky_pale', 0.85, tooth=0)
    mug = p.rect(180, 1400, 360, 1620) + p.ellipse(270, 1620, 90, 30)
    erase(S, np.clip(mug, 0, 1)); p.form(np.clip(mug, 0, 1), ('peach', 'coral', 'terracotta', 'brick'), 90, LIGHT, density=1.5, seed=S.sd())
    p.edge(np.clip(mug, 0, 1), 'brick', density=0.8, alpha=0.8)
    S.save('calendar26')
    im = Image.open(os.path.join(ARTD, 'calendar26.jpg')).convert('RGBA'); lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((370, 390), '2026', font=ImageFont.truetype(FONT.format(900), 110), fill=(255, 250, 238, 240), anchor='mm')
    fn = ImageFont.truetype(FONT.format(700), 34)
    for c, wd in enumerate('日月火水木金土'): d.text((165 + c * 68, 530), wd, font=fn, fill=(110, 80, 60, 210), anchor='mm')
    n = 1
    for r in range(5):
        for c in range(7):
            if (r == 0 and c < 4) or n > 31: continue
            d.text((165 + c * 68, 600 + r * 80), str(n), font=fn, fill=(196, 68, 58, 220) if c == 0 else (92, 64, 48, 215), anchor='mm'); n += 1
    d.text((710, 1480), '2026', font=ImageFont.truetype(FONT.format(900), 70), fill=(60, 70, 110, 235), anchor='mm')
    d.text((710, 1550), '1月1日 木曜日', font=ImageFont.truetype(FONT.format(700), 28), fill=(80, 90, 120, 220), anchor='mm')
    im.alpha_composite(lay); im.convert('RGB').save(os.path.join(ARTD, 'calendar26.jpg'), quality=90)


def tl_bg():
    """a warm sheet of paper for the timeline"""
    S = Shot(1202); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(4, 6, 500), ['cream', 'ivory', 'butter'], (60, 150), (1.8, 2.5), 1.3, 0.55, alpha=0.6, seed=S.sd())
    p.hatch(bg * smoothstep(300, 1500, np.abs(p.YY - 880) * 2 + 300), p.flow(4, 6, 500), ['apricot', 'peach'], (60, 140), (1.8, 2.4), 0.7, 0.55, alpha=0.35, seed=S.sd())
    p.glow(540, 880, 420, strength=0.45, density=0.5)
    S.save('tl_bg')


def village():
    """2000年前のイスラエル: flat-roofed stone houses on a dry hillside, olive trees and a palm, a dusty road"""
    S = Shot(1203); p = S.p
    sky(S, 950, (820, 320, 340))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [900, 860, 880, 840, 870, 900, 860], ('sand', 'ochre', 'tan', 'sienna'), mist=0.4)
    hill = p.below([0, 400, 800, 1080], [1100, 1050, 1080, 1040])
    p.form(hill, ('butter', 'sand', 'ochre', 'tan'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.3, seed=S.sd())
    houses = [(120, 1060, 200, 150), (330, 1020, 170, 170), (520, 1050, 220, 140), (760, 1010, 180, 180), (950, 1060, 190, 140),
              (220, 1230, 240, 170), (640, 1220, 260, 180), (900, 1250, 200, 160)]
    for (x, y, w, hh) in houses:
        m = p.rect(x - w / 2, y - hh, x + w / 2, y)
        erase(S, m); p.form(m, ('cream', 'sand', 'tan', 'ochre'), 90, LIGHT, length=(20, 50), density=1.4, seed=S.sd())
        p.form(p.rect(x - w / 2 - 8, y - hh - 14, x + w / 2 + 8, y - hh + 6), ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.4, seed=S.sd())
        p.form(p.rect(x - w * 0.12, y - hh * 0.55, x + w * 0.12, y), ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.5, seed=S.sd())
        p.edge(m, 'sienna', density=0.7, alpha=0.7)
        p.form(p.rect(x + w * 0.22, y - hh * 0.78, x + w * 0.38, y - hh * 0.6), ('umber', 'sepia', 'sepia'), 0, LIGHT, density=1.5, seed=S.sd())
    for (x, y) in ((450, 1180), (1010, 1170), (60, 1200)):
        p.tree(x, y, 120, 70, colours=('sage', 'lichen', 'olive', 'moss'), clumps=5, seed=S.sd())
    trunk = p.tube([(820, 1340), (835, 1100), (850, 880)], 14, 10)
    p.form(trunk, ('tan', 'sienna', 'brown'), 90, LIGHT, density=1.5, seed=S.sd())
    for a in np.linspace(-160, -20, 7):
        r = np.deg2rad(a); end = (850 + 150 * np.cos(r), 880 + 150 * np.sin(r) + 70)
        lf = p.tube([(850, 880), (850 + 90 * np.cos(r), 880 + 90 * np.sin(r) - 10), end], 14, 3)
        p.form(lf, ('sage', 'moss', 'pine'), a, LIGHT, density=1.5, seed=S.sd())
    road = p.poly([(500, 1300), (580, 1300), (820, 1920), (260, 1920)])
    ground(S, 1300, cols=('sand', 'butter', 'tan', 'ochre'), flowers=0)
    p.form(road, ('butter', 'cream', 'sand', 'tan'), p.flow(90, 8), LIGHT, density=1.3, seed=S.sd())
    figure(S, 470, 1520, 260, coat=ROBE, back=True, walk=0.4, legs=('tan', 'sienna', 'umber'))
    figure(S, 680, 1600, 230, coat=('sand', 'tan', 'sienna', 'brown'), back=True, walk=0.4, legs=('tan', 'sienna', 'umber'))
    S.save('village')


def carpenter():
    """大工として: a carpenter's hands planing a board on the bench, curls of wood shaving, tools and light"""
    S = Shot(1204); p = S.p
    wall = (p.YY < 1000).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sand', 'cream', 'apricot'], (60, 140), (1.8, 2.5), 1.6, 0.62, alpha=0.7, seed=S.sd())
    p.glow(900, 260, 420, strength=0.9, density=0.9)
    beam = p.poly([(820, 160), (1000, 160), (640, 1200), (300, 1200)])
    p.hatch(beam, 70, ['butter', 'cream'], (60, 140), (1.8, 2.4), 0.8, 0.6, opacity=0.6, alpha=0.35, seed=S.sd())
    bench = p.poly([(0, 900), (1080, 860), (1080, 1920), (0, 1920)])
    erase(S, bench); p.form(bench, ('tan', 'sienna', 'brown', 'umber'), p.flow(-4, 6), LIGHT, length=(60, 140), density=1.5, seed=S.sd())
    board = p.poly([(60, 980), (1020, 930), (1040, 1130), (80, 1190)])
    erase(S, board); p.form(board, ('butter', 'sand', 'ochre', 'tan'), p.flow(-4, 4), LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    p.edge(board, 'sienna', density=0.9, alpha=0.8)
    for j in range(6):
        y0 = 995 + j * 28
        p.line(curve([(100, y0 + 8), (500, y0 - 14), (1000, y0 - 40)], 30), 'ochre', 1.8, 0.6, alpha=0.6)
    plane = p.poly([(400, 990), (700, 970), (715, 1080), (410, 1100)])
    erase(S, plane); p.form(plane, ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(plane, 'sepia', density=0.9, alpha=0.85)
    p.form(p.ellipse(600, 950, 60, 30), ('brown', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    saw = p.poly([(120, 1300), (560, 1250), (560, 1330), (140, 1380)])
    erase(S, saw); p.form(saw, ('stone', 'pebble', 'warmgrey', 'slate'), 0, LIGHT, density=1.5, seed=S.sd()); p.edge(saw, 'slate', density=0.9, alpha=0.85)
    for x in range(150, 555, 18): p.line([(x, 1380 - (x - 140) * 0.12), (x + 9, 1392 - (x - 140) * 0.12)], 'slate', 2, 0.7, alpha=0.8)
    hd = p.poly([(560, 1240), (690, 1225), (700, 1345), (570, 1360)])
    erase(S, hd); p.form(hd, ('sienna', 'brown', 'umber'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(hd, 'sepia', density=0.9, alpha=0.85)
    hm_h = p.tube([(760, 1560), (900, 1380)], 18, 16)
    erase(S, hm_h); p.form(hm_h, ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    hh = p.poly([(850, 1330), (960, 1400), (935, 1440), (825, 1370)])
    erase(S, hh); p.form(hh, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.6, seed=S.sd()); p.edge(hh, 'sepia', density=0.9, alpha=0.85)
    ch = p.tube([(240, 1560), (520, 1520)], 12, 10)
    erase(S, ch); p.form(ch, ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    chh = p.tube([(520, 1520), (650, 1502)], 22, 20)
    erase(S, chh); p.form(chh, ('tan', 'sienna', 'brown'), 0, LIGHT, density=1.5, seed=S.sd())
    for (x, y, r) in ((800, 930, 50), (870, 980, 38), (260, 1000, 42), (740, 1160, 46), (330, 1460, 40), (600, 1620, 52)):
        t = np.linspace(0, 2 * np.pi * 1.6, 50)
        p.line(np.stack([x + r * np.cos(t) * (1 - t / 14), y + r * 0.5 * np.sin(t) * (1 - t / 14)], 1), 'cream', 9, 0.85, alpha=0.95)
    S.save('carpenter')


def beside():
    """いつもそばにいた人: from behind, a figure in a white robe sitting close beside someone alone, a hand on their shoulder"""
    S = Shot(1205); p = S.p
    sky(S, 1150, (540, 950, 520))
    xs = np.linspace(0, 1080, 7)
    ridge(S, xs, [1080, 1020, 1050, 1000, 1040, 1070, 1020], RIDGES[0], mist=0.6)
    ground(S, 1150, cols=('butter', 'sand', 'yellowgreen', 'meadow'), flowers=60)
    wall = p.rect(0, 1330, 1080, 1520)
    erase(S, wall); p.form(wall, ('stone', 'warmgrey', 'pebble', 'sand'), 0, LIGHT, length=(40, 90), density=1.4, seed=S.sd())
    for x in range(0, 1080, 160): p.line([(x, 1330), (x + 20, 1520)], 'warmgrey', 2.4, 0.6, alpha=0.6)
    p.form(p.rect(0, 1520, 1080, 1920), ('sand', 'tan', 'ochre', 'sienna'), 0, LIGHT, length=(60, 120), density=1.3, seed=S.sd())
    def seated(x, R, coat, hair, slump=0.0):
        hy = 1330 - R * 3.4 + slump * R * 0.5
        head = p.ellipse(x - slump * R * 0.3, hy, R * 0.92, R)
        body = p.poly(curve([(x - R * 0.5, hy + R * 0.85), (x - R * 1.3, hy + R * 1.5), (x - R * 1.6, 1345), (x + R * 1.6, 1345),
                             (x + R * 1.3, hy + R * 1.5), (x + R * 0.5, hy + R * 0.85)], 50), smooth=True)
        erase(S, np.clip(head + body, 0, 1))
        p.form(body, coat, 85, LIGHT, length=(14, 30), density=1.4, warm='butter', cool='lavender', seed=S.sd())
        p.form(head, hair, p.radial(x, hy - R, 90), LIGHT, length=(8, 18), density=1.6, seed=S.sd())
        p.edge(body, 'sepia', density=0.8, alpha=0.7); p.edge(head, 'sepia', density=0.6, alpha=0.6)
        return hy
    seated(380, 95, ('stone', 'warmgrey', 'slate', 'umber'), ('hair', 'umber', 'sepia'), slump=0.6)
    hy = seated(680, 105, ROBE, ('umber', 'sepia', 'sepia'))
    arm = p.tube([(610, 1150), (530, 1150), (455, 1172)], 34, 28)
    erase(S, arm); p.form(arm, ROBE, p.contour(arm, 6, 0), LIGHT, density=1.5, warm='butter', seed=S.sd()); p.edge(arm, 'sepia', density=0.8, alpha=0.7)
    p.form(p.ellipse(452, 1172, 32, 24), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    p.glow(540, 950, 360, strength=0.7, density=0.7)
    S.save('beside')


def cross():
    """十字架: a lone cross on the hill against the evening sky"""
    S = Shot(1206); p = S.p
    m = (p.YY < 1250).astype(np.float32)
    v = p.value(0.0, 1.0, 0, 1250)
    p.hatch(m, p.flow(-3, 4), ('dusk_sky', np.clip(v * 1.05, 0, 1)), (60, 150), (1.8, 2.6), 1.8, 0.76, seed=S.sd())
    p.hatch(m * smoothstep(0.4, 1.0, v), p.flow(-3, 4), ['peach', 'apricot', 'rose'], (60, 140), (1.8, 2.4), 1.0, 0.66, alpha=0.55, seed=S.sd())
    p.glow(540, 1180, 520, strength=0.9, density=0.9, colours='glow')
    clouds(S, [(220, 420, 320, 60), (860, 560, 280, 50)])
    hill = p.below([0, 300, 540, 780, 1080], [1400, 1250, 1180, 1250, 1400])
    p.form(hill, ('slate', 'indigo', 'violet', 'sepia'), p.flow(-4, 10), LIGHT, length=(30, 70), density=1.6, seed=S.sd())
    p.form((p.YY > 1400).astype(np.float32), ('indigo', 'slate', 'sepia', 'umber'), 0, LIGHT, length=(40, 90), density=1.5, seed=S.sd())
    cr = np.clip(p.rect(522, 640, 558, 1190) + p.rect(420, 760, 660, 794), 0, 1)
    erase(S, cr); p.form(cr, ('umber', 'sepia', 'indigo', 'sepia'), 90, LIGHT, density=1.8, seed=S.sd()); p.edge(cr, 'sepia', density=0.9, alpha=0.9)
    S.save('cross')


def tomb():
    """三日目に: the garden tomb at dawn, the round stone rolled aside, morning light pouring into the empty opening"""
    S = Shot(1207); p = S.p
    sky(S, 900, (900, 380, 420))
    rock = p.poly(curve([(0, 600), (300, 520), (700, 560), (1080, 640), (1080, 1350), (0, 1350)], 60), smooth=True)
    erase(S, rock); p.form(rock, ('stone', 'warmgrey', 'sand', 'umber'), p.flow(80, 30), LIGHT, length=(30, 70), density=1.5, seed=S.sd())
    p.leaves(rock * (p.YY < 700) * (noise2d(H, W, 60, 2, 3) > 0.5), ('meadow', 'moss', 'pine'), (10, 18), 1.2, seed=S.sd())
    door = p.poly(curve([(360, 1250), (360, 960), (450, 860), (560, 860), (640, 960), (640, 1250)], 50), smooth=True)
    erase(S, door)
    p.form(door, ('umber', 'sepia', 'sienna', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.lift(blur(door * smoothstep(360, 640, p.XX), 6), 'butter', 0.55)
    p.glow(500, 1080, 240, strength=0.8, density=0.8)
    stone = p.ellipse(830, 1110, 170, 170)
    erase(S, stone); p.form(stone, ('stone', 'warmgrey', 'pebble', 'umber'), p.contour(stone, 10), LIGHT, density=1.6, seed=S.sd())
    p.edge(stone, 'sepia', density=0.9, alpha=0.85)
    ground(S, 1250, cols=('meadow', 'yellowgreen', 'grass', 'moss'), flowers=120)
    beam = p.poly([(980, 300), (1080, 360), (640, 1260), (420, 1240)])
    p.hatch(beam, 60, ['glow', 'butter', 'cream'], (60, 160), (1.8, 2.4), 1.0, 0.6, opacity=0.6, alpha=0.45, seed=S.sd())
    p.glow(900, 380, 360, strength=0.9, density=0.9)
    cloth = p.rect(420, 1200, 580, 1240)
    p.form(cloth, ROBE, 0, LIGHT, density=1.4, seed=S.sd())
    S.save('tomb')


def palm():
    """新しいはじまり: an open hand, palm up, held out in warm light (the light itself is drawn on it in the edit)"""
    S = Shot(1208); p = S.p
    bg = np.ones((H, W), np.float32)
    p.hatch(bg, p.flow(-10, 6), ['apricot', 'butter', 'peach'], (60, 150), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.glow(540, 700, 640, strength=1.0, density=1.0)
    hms = []
    for (x, ang, curl, sx) in ((450, -112, -0.5, 200), (630, -68, 0.5, 880)):
        sl = p.tube([(sx, 1980), ((sx + x) / 2, 1560), (x, 1290)], 140, 115)
        erase(S, sl); p.form(sl, ('powder', 'cornflower', 'denim', 'indigo'), p.contour(sl, 10, 90), LIGHT, density=1.4, warm='butter', seed=S.sd())
        p.edge(sl, 'sepia', density=0.8, alpha=0.7)
    for (x, ang, curl) in ((450, -112, -0.5), (630, -68, 0.5)):
        hms.append(hand(S, x, 1200, 1.9, ang, curl=curl))
    p.lift(blur(p.ellipse(540, 1120, 190, 120), 20) * np.clip(hms[0] + hms[1], 0, 1), 'butter', 0.3)
    S.save('palm')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
