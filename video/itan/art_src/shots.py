"""「"異端"ってなに?」 paintings. python3 shots.py NAME"""
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


def phone_news():
    """ニュースで聞いたこと: the young woman in the evening looking at blurred news on her phone, worried and confused"""
    S = Shot(3101); p = S.p
    ARMS = [[(420, 1010), (400, 1150), (470, 1200)], [(660, 1010), (680, 1150), (610, 1200)]]
    w = person(S, 540, 760, 160, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    hj.room(S, w['mask'], win_box=(660, 140, 1000, 600))
    win = p.rect(660, 140, 1000, 600)
    p.hatch(win, p.flow(-3, 4), ['indigo', 'violet', 'mauve'], (40, 100), (1.7, 2.4), 1.6, 0.75, seed=S.sd())
    for x in (660, 830, 1000): p.line([(x, 140), (x, 600)], 'tan', 9, 0.8, alpha=0.9)
    for y in (140, 370, 600): p.line([(660, y), (1000, y)], 'tan', 9, 0.8, alpha=0.9)
    erase(S, w['mask'])
    person(S, 540, 760, 160, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, smile=False, look=(0, 0.7))
    for sg in (-1, 1): p.line(curve([(540 + sg * 70, 690), (540 + sg * 45, 676), (540 + sg * 20, 684)], 8), 'umber', 3, 0.8, alpha=0.85)
    ph = p.rect(470, 1120, 610, 1300); erase(S, ph); p.form(ph, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.7, seed=S.sd())
    sc = p.rect(484, 1136, 596, 1284); p.lift(sc, 'powder', 0.9, tooth=0)
    for q in range(5): p.line([(494, 1160 + q * 24), (586 - (q % 2) * 30, 1160 + q * 24)], 'slate', 4, 0.7, alpha=0.5)
    p.glow(540, 1150, 260, strength=0.8, density=0.8)
    for (x, y) in ((470, 1200), (610, 1200)): p.form(p.ellipse(x, y, 34, 30), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('phone_news')


def two_boxes():
    """中身が同じとは限らない: two similar gift boxes, lids slightly open -- one glowing warmly inside, the other dark and empty"""
    S = Shot(3102); p = S.p
    wall = (p.YY < 1000).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['cream', 'apricot', 'sand'], (60, 140), (1.8, 2.5), 1.5, 0.6, seed=S.sd())
    p.form((p.YY >= 1000).astype(np.float32), ('tan', 'sienna', 'brown', 'umber'), 0, LIGHT, length=(80, 160), density=1.5, seed=S.sd())
    for cx, inner in ((290, 'light'), (790, 'dark')):
        bx = p.rect(cx - 170, 820, cx + 170, 1120); erase(S, bx)
        p.form(bx, ('rose', 'pink', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
        p.form(p.rect(cx - 26, 820, cx + 26, 1120), ('gold', 'amber', 'ochre'), 90, LIGHT, density=1.6, seed=S.sd())
        lid = p.poly([(cx - 190, 760), (cx + 190, 720), (cx + 196, 780), (cx - 184, 820)]); erase(S, lid)
        p.form(lid, ('rose', 'pink', 'coral', 'brick'), 0, LIGHT, density=1.5, seed=S.sd())
        p.form(p.poly([(cx - 26, 742), (cx + 26, 738), (cx + 28, 798), (cx - 24, 802)]), ('gold', 'amber', 'ochre'), 90, LIGHT, density=1.6, seed=S.sd())
        gap = p.poly([(cx - 170, 820), (cx + 170, 780), (cx + 170, 820)])
        if inner == 'light':
            p.lift(gap, 'lemon', 1.0, tooth=0); p.glow(cx, 760, 300, strength=1.4, density=1.2)
        else:
            p.form(gap, ('sepia', 'sepia', 'umber'), 0, LIGHT, density=1.8, seed=S.sd())
        p.edge(np.clip(bx + lid, 0, 1), 'sepia', density=0.8, alpha=0.75)
    S.save('two_boxes')


def stage():
    """教祖が、新しい救い主だ: far away, a shadowy figure on a stage raising his hands to a crowd under harsh light; no faces"""
    S = Shot(3103); p = S.p
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['slate', 'indigo', 'umber'], (60, 140), (1.8, 2.5), 1.8, 0.8, seed=S.sd())
    st = p.rect(220, 720, 860, 820); erase(S, st); p.form(st, ('stone', 'warmgrey', 'slate'), 0, LIGHT, density=1.5, seed=S.sd())
    beam = p.poly([(500, 0), (580, 0), (720, 720), (360, 720)])
    p.lift(blur(beam, 30), 'stone', 0.5, tooth=0)
    fig = np.clip(p.ellipse(540, 520, 34, 38) + p.poly(curve([(480, 720), (470, 620), (500, 570), (580, 570), (610, 620), (600, 720)], 30), smooth=True)
                  + p.tube([(500, 590), (430, 500), (420, 440)], 18, 14) + p.tube([(580, 590), (650, 500), (660, 440)], 18, 14), 0, 1)
    erase(S, fig); p.lift(fig, 'sepia', 0.9, tooth=0); p.form(fig, ('sepia', 'umber', 'slate'), 0, LIGHT, density=1.8, seed=S.sd())
    for r in range(3):
        for c in range(8):
            x = 110 + c * 125 + (r % 2) * 60; y = 1000 + r * 150
            hd = p.ellipse(x, y, 40, 44); bd = p.ellipse(x, y + 90, 60, 70) * (p.YY < y + 140)
            mm = np.clip(hd + bd, 0, 1); erase(S, mm); p.form(mm, ('slate', 'indigo', 'umber', 'sepia'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form((p.YY >= 1450).astype(np.float32), ('indigo', 'slate', 'sepia'), 0, LIGHT, density=1.4, seed=S.sd())
    S.save('stage')


def books_light():
    """何が基準か: a single large open book shining with light; beside it a stack of thick unfamiliar books in shadow"""
    S = Shot(3104); p = S.p
    wall = (p.YY < 900).astype(np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sand', 'tan', 'stone'], (60, 140), (1.8, 2.5), 1.6, 0.62, seed=S.sd())
    p.form((p.YY >= 900).astype(np.float32), ('sienna', 'brown', 'umber', 'sepia'), 0, LIGHT, length=(80, 160), density=1.5, seed=S.sd())
    p.lift(blur(p.rect(560, 300, 1080, 1300), 60), 'sepia', 0.35)
    for j in range(6):
        y1 = 1150 - j * 70; w_ = 300 - (j % 3) * 30
        bk = p.rect(820 - w_ / 2, y1 - 64, 820 + w_ / 2, y1); erase(S, bk)
        p.form(bk, [('slate', 'indigo', 'umber'), ('sepia', 'umber', 'brown'), ('warmgrey', 'slate', 'umber')][j % 3], 0, LIGHT, density=1.6, seed=S.sd())
        p.edge(bk, 'sepia', density=0.8, alpha=0.7)
    L_ = p.poly(curve([(80, 1060), (230, 1010), (395, 1050), (395, 1380), (230, 1350), (60, 1400)], 50), smooth=True)
    R_ = p.poly(curve([(405, 1050), (570, 1010), (720, 1060), (740, 1400), (570, 1350), (405, 1380)], 50), smooth=True)
    for mm, x0 in ((L_, 100), (R_, 430)):
        erase(S, mm); p.hatch(mm, 90, ('white', 'cream', 'ivory'), (20, 50), (1.6, 2.3), 1.5, 0.7, opacity=0.85, alpha=0.85, seed=S.sd())
        for kk in range(10): p.line([(x0, 1090 + kk * 26), (x0 + 270, 1092 + kk * 26)], 'pebble', 2.2, 0.7, alpha=0.65)
    p.line(curve([(410, 1050), (420, 1450)], 20), 'red', 7, 0.85, alpha=0.95)
    p.glow(400, 1150, 420, strength=1.4, density=1.2)
    p.dots(p.ellipse(400, 850, 260, 260), ('white', 'cream', 'butter'), n=60, size=(2, 4))
    S.save('books_light')


def coins_box():
    """お金や、団体への忠誠で: hands dropping coins into a large dark box under a dim light"""
    S = Shot(3105); p = S.p
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['warmgrey', 'slate', 'umber'], (60, 140), (1.8, 2.5), 1.7, 0.72, seed=S.sd())
    p.glow(540, 200, 300, strength=0.6, density=0.6)
    bx = p.rect(260, 900, 820, 1500); erase(S, bx); p.form(bx, ('umber', 'sepia', 'slate'), 0, LIGHT, density=1.7, seed=S.sd())
    top = p.poly([(260, 900), (820, 900), (880, 840), (320, 840)]); erase(S, top); p.form(top, ('sepia', 'umber', 'slate'), 0, LIGHT, density=1.7, seed=S.sd())
    p.form(p.rect(460, 862, 680, 880), ('sepia', 'sepia', 'umber'), 0, LIGHT, density=1.8, seed=S.sd())
    p.edge(np.clip(bx + top, 0, 1), 'sepia', density=0.8, alpha=0.8)
    rr = np.random.default_rng(4)
    for j, (x, y) in enumerate(((330, 560), (750, 520), (560, 420))):
        arm = p.tube([(x + (-200 if x < 540 else 200), y - 300), (x, y)], 42, 36); erase(S, arm)
        p.form(arm, ('stone', 'warmgrey', 'slate'), 90, LIGHT, density=1.5, seed=S.sd())
        p.form(p.ellipse(x, y + 10, 40, 34), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
        for q in range(3):
            cx, cy = x + rr.uniform(-20, 20), y + 90 + q * 110 + rr.uniform(-10, 10)
            p.form(p.ellipse(cx, cy, 20, 12), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    S.save('coins_box')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
