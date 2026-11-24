"""「なぜ、あの木を取りのぞかなかったのか」 paintings. python3 shots.py NAME"""
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
fruit_tree, dusk, night = z.fruit_tree, z.dusk, z.night


def shadows():
    """争いも、病も、別れも: faint grey scenes in the sky above the garden tree -- people arguing, someone sick in bed, a farewell at a grave"""
    S = Shot(3301); p = S.p
    m = (p.YY < 1150).astype(np.float32)
    p.hatch(m, p.flow(-3, 4), ['stone', 'warmgrey', 'lavender'], (60, 150), (1.8, 2.5), 1.6, 0.66, seed=S.sd())
    ground(S, 1150, flowers=60)
    fruit_tree(S, 540, 1260, 420, 160, fruit=('gold', 'amber', 'tangerine'), n=14, glow=True, seed=5, cols=('sage', 'moss', 'pine', 'forest'))
    G = ('stone', 'warmgrey', 'slate')
    def ghost(mask):
        p.lift(blur(mask, 3), 'paper', 0.5, tooth=0); p.form(mask, G, 0, LIGHT, density=1.0, seed=S.sd())
    # two people arguing (left)
    for (x, sg) in ((150, 1), (330, -1)):
        ghost(np.clip(p.ellipse(x, 300, 36, 40) + p.ellipse(x, 400, 56, 70) * (p.YY < 450) + p.tube([(x + sg * 40, 370), (x + sg * 90, 330)], 12, 10), 0, 1))
    # someone sick in bed (right)
    ghost(np.clip(p.rect(700, 330, 980, 380) + p.rect(700, 380, 716, 430) + p.rect(964, 380, 980, 430) + p.ellipse(740, 314, 30, 26) + p.ellipse(860, 322, 110, 22), 0, 1))
    # a farewell at a grave (centre, higher)
    ghost(np.clip(p.rect(500, 150, 560, 260) + p.ellipse(530, 150, 30, 30) * (p.YY < 160) + p.ellipse(620, 160, 26, 28) + p.ellipse(620, 250, 42, 60) * (p.YY < 300), 0, 1))
    p.lift(blur((p.YY < 520).astype(np.float32), 40), 'stone', 0.25)
    S.save('shadows')


def angel():
    """天使と、ほのおのつるぎ: a majestic angel standing guard before the glowing tree of life, a softly flaming sword turning in the air"""
    S = Shot(3302); p = S.p
    dusk(S, 1150, cols=('lavender', 'periwinkle', 'mauve'), low=('apricot', 'peach', 'butter'))
    ground(S, 1150, cols=('meadow', 'moss', 'olive', 'sage'), flowers=40)
    p.glow(760, 600, 360, strength=1.2, density=1.1)
    fruit_tree(S, 760, 1180, 520, 200, fruit=('white', 'cream', 'butter'), n=18, glow=True, seed=11, cols=('yellowgreen', 'meadow', 'moss', 'pine'))
    wings = np.clip(p.ellipse(220, 640, 170, 300, rot=-20) + p.ellipse(520, 640, 170, 300, rot=20), 0, 1)
    erase(S, wings); p.form(wings, ('white', 'cream', 'ivory', 'stone'), p.contour(wings, 6), LIGHT, length=(20, 40), density=1.5, seed=S.sd())
    for q in range(6):
        for cx_, sg in ((220, -1), (520, 1)):
            p.line(curve([(cx_ + sg * 20, 420 + q * 70), (cx_ - sg * 90, 470 + q * 70)], 10), 'stone', 2.4, 0.6, alpha=0.5)
    p.edge(wings, 'warmgrey', density=0.8, alpha=0.6)
    ARMS = [[(300, 830), (250, 760), (230, 690)]]
    w = person(S, 370, 640, 120, coat=('white', 'cream', 'ivory', 'sand'), hair_style='short', plan=True, arms=ARMS)
    erase(S, w['mask'])
    person(S, 370, 640, 120, coat=('white', 'cream', 'ivory', 'sand'), hair_style='short', hair=('butter', 'ochre', 'tan'), arms=ARMS, smile=False, eyes_closed=True)
    blade = p.poly([(222, 680), (238, 680), (250, 300), (230, 270), (210, 300)]); erase(S, blade)
    p.form(blade, ('white', 'cream', 'stone'), 90, LIGHT, density=1.5, seed=S.sd())
    p.form(p.rect(190, 680, 270, 696), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.6, seed=S.sd())
    p.glow(230, 460, 220, colours=('lantern', 'flame', 'glow'), strength=1.4, density=1.2)
    rr = np.random.default_rng(3)
    for _ in range(16):
        y = rr.uniform(300, 680); x = 230 + rr.uniform(-40, 40)
        p.line(curve([(x, y), (x + rr.uniform(-20, 20), y - 30), (x, y - 60)], 10), 'tangerine', 4, 0.7, alpha=0.6)
    S.save('angel')


def heart_shadow():
    """問題は、人の心にある: a person standing with a hand on the chest; a small dark shadow softly inside the heart"""
    S = Shot(3303); p = S.p
    ARMS = [[(400, 1000), (420, 1100), (520, 1080)]]
    w = person(S, 540, 760, 170, coat=COAT, hair_style='long', plan=True, arms=ARMS)
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['cream', 'apricot', 'peach'], (60, 140), (1.8, 2.5), 1.5, 0.6, avoid=w['mask'], seed=S.sd())
    p.glow(540, 760, 500, strength=0.7, density=0.7)
    erase(S, w['mask'])
    person(S, 540, 760, 170, coat=COAT, hair_style='long', hair=HAIR, arms=ARMS, hands=False, smile=False, eyes_closed=True)
    sh = h.heart_mask(p, 600, 1080, 70)
    p.lift(blur(sh, 18), 'sepia', 0.55); p.lift(blur(sh, 6), 'umber', 0.45)
    p.form(p.ellipse(520, 1080, 40, 34), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    S.save('heart_shadow')


def bird(S, x, y, s, cols=('butter', 'sun', 'amber', 'ochre'), fly=False):
    p = S.p
    body = p.ellipse(x, y, 46 * s, 34 * s); head = p.ellipse(x + 40 * s, y - 26 * s, 24 * s, 22 * s)
    tail = p.poly([(x - 40 * s, y), (x - 90 * s, y - 20 * s), (x - 84 * s, y + 18 * s)])
    m = np.clip(body + head + tail, 0, 1); erase(S, m); p.form(m, cols, 0, LIGHT, density=1.6, seed=S.sd())
    wing = p.ellipse(x - 6 * s, y - (40 if fly else 4) * s, 40 * s, (30 if fly else 18) * s, rot=-30 if fly else 10)
    erase(S, wing); p.form(wing, ('ochre', 'amber', 'tan'), 0, LIGHT, density=1.6, seed=S.sd())
    p.form(p.poly([(x + 62 * s, y - 30 * s), (x + 82 * s, y - 24 * s), (x + 62 * s, y - 18 * s)]), ('tangerine', 'orange', 'brick'), 0, LIGHT, density=1.6, seed=S.sd())
    p.lift(p.ellipse(x + 46 * s, y - 30 * s, 4 * s, 4 * s), 'sepia', 1.0, tooth=0)
    p.edge(m, 'umber', density=0.8, alpha=0.6)


def cage(S, cx, cy, open_=False):
    p = S.p
    top = p.ellipse(cx, cy - 300, 260, 120) * (p.YY < cy - 300)
    p.form(top, ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.4, seed=S.sd())
    base = p.rect(cx - 280, cy + 260, cx + 280, cy + 310); erase(S, base); p.form(base, ('gold', 'amber', 'ochre', 'tan'), 0, LIGHT, density=1.6, seed=S.sd())
    door = (cx + 60, cx + 200)
    for x in np.linspace(cx - 260, cx + 260, 12):
        if open_ and door[0] < x < door[1]: continue
        top_y = cy - 300 - 120 * np.sqrt(max(0, 1 - ((x - cx) / 260) ** 2))
        p.line([(x, top_y), (x, cy + 260)], 'gold', 5, 0.85, alpha=0.95)
    for y in (cy - 120, cy + 80): p.line([(cx - 260, y), (cx + 260, y)], 'amber', 4, 0.8, alpha=0.85)
    p.line([(cx, cy - 420), (cx, cy - 520)], 'gold', 5, 0.85, alpha=0.95)
    p.form(p.ellipse(cx, cy - 530, 22, 22) - p.ellipse(cx, cy - 530, 12, 12), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.5, seed=S.sd())
    if open_:
        d = p.poly([(door[1], cy - 140), (door[1] + 150, cy - 100), (door[1] + 150, cy + 150), (door[1], cy + 230)])
        for x in np.linspace(door[1] + 20, door[1] + 140, 4): p.line([(x, cy - 130 + (x - door[1]) * 0.25), (x, cy + 220 - (x - door[1]) * 0.5)], 'gold', 4, 0.8, alpha=0.9)


def birdcage():
    """鳥かご: a small bird inside a beautiful closed golden cage, safe but sad, looking out at the open sky"""
    S = Shot(3304); p = S.p
    wall = np.ones((H, W), np.float32)
    p.hatch(wall, p.flow(2, 4, 500), ['sand', 'tan', 'stone'], (60, 140), (1.8, 2.5), 1.6, 0.64, seed=S.sd())
    win = p.rect(640, 120, 1020, 560); erase(S, win)
    p.hatch(win, p.flow(-3, 4), ['sky', 'sky_pale', 'powder'], (40, 100), (1.7, 2.4), 1.6, 0.7, seed=S.sd())
    for x in (640, 830, 1020): p.line([(x, 120), (x, 560)], 'tan', 9, 0.8, alpha=0.9)
    for y in (120, 340, 560): p.line([(640, y), (1020, y)], 'tan', 9, 0.8, alpha=0.9)
    bird(S, 500, 940, 1.2)
    p.line([(380, 990), (620, 990)], 'brown', 7, 0.85, alpha=0.95)
    cage(S, 480, 880)
    p.form((p.YY >= 1250).astype(np.float32), ('brown', 'sienna', 'umber'), 0, LIGHT, density=1.4, seed=S.sd())
    S.save('birdcage')


def bird_free():
    """自分で選んで: the cage door open, the bird flying freely and landing gently on the open hand of a smiling child; bright sun"""
    S = Shot(3305); p = S.p
    sky(S, 1250, (860, 260, 360))
    clouds(S, [(200, 300, 300, 66), (760, 520, 220, 56)])
    ground(S, 1250, flowers=160)
    ARMS = [[(620, 1060), (720, 980), (790, 930)]]
    c = person(S, 520, 860, 110, coat=('butter', 'sun', 'amber', 'ochre'), hair_style='bob', plan=True, arms=ARMS)
    erase(S, c['mask'])
    person(S, 520, 860, 110, coat=('butter', 'sun', 'amber', 'ochre'), hair_style='bob', hair=HAIRD, arms=ARMS, hands=False, smile=True, look=(0.6, -0.5))
    p.form(p.ellipse(800, 920, 40, 26), SKIN4, 0, LIGHT, density=1.6, seed=S.sd())
    bird(S, 800, 870, 0.8, fly=True)
    cg = p.rect(100, 980, 300, 1250); p.lift(blur(cg, 2), 'paper', 0.0)
    for x in np.linspace(110, 290, 7): p.line([(x, 1000), (x, 1250)], 'gold', 4, 0.8, alpha=0.9)
    p.form(p.ellipse(200, 1000, 100, 40) * (p.YY < 1000), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.4, seed=S.sd())
    p.form(p.rect(90, 1240, 310, 1270), ('gold', 'amber', 'ochre'), 0, LIGHT, density=1.5, seed=S.sd())
    for q in range(3): p.line(curve([(330 + q * 140, 820 - q * 20), (380 + q * 140, 790 - q * 25), (430 + q * 140, 800 - q * 20)], 10), 'butter', 3, 0.6, alpha=0.6)
    S.save('bird_free')


def _phone_room(S, warm=False):
    p = S.p
    m = np.ones((H, W), np.float32)
    p.hatch(m, p.flow(2, 4, 500), ['indigo', 'slate', 'umber'] if not warm else ['slate', 'mauve', 'apricot'], (60, 140), (1.8, 2.5), 1.8, 0.78, seed=S.sd())
    p.form((p.YY >= 1250).astype(np.float32), ('slate', 'umber', 'sepia'), 0, LIGHT, length=(60, 140), density=1.4, seed=S.sd())
    ARMS = [[(420, 1030), (430, 1130), (500, 1150)], [(660, 1030), (650, 1130), (580, 1150)]]
    w = person(S, 540, 800, 150, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='long', plan=True, arms=ARMS)
    erase(S, w['mask'])
    person(S, 540, 800, 150, coat=('stone', 'warmgrey', 'slate', 'umber'), hair_style='long', hair=HAIRD, arms=ARMS, smile=warm, look=(0, 0.8), eyes_closed=warm)
    ph = p.rect(480, 1110, 600, 1250); erase(S, ph); p.form(ph, ('slate', 'indigo', 'umber'), 0, LIGHT, density=1.7, seed=S.sd())
    p.lift(p.rect(492, 1124, 588, 1238), 'powder', 0.9, tooth=0)
    p.glow(540, 1000, 280, colours=('powder', 'sky_pale', 'white'), strength=0.9, density=0.8)
    for (x, y) in ((500, 1150), (580, 1150)): p.form(p.ellipse(x, y, 30, 26), SKIN4, 0, LIGHT, density=1.5, seed=S.sd())
    return w


def phone_night():
    """やめられない習慣。だれにも言えない秘密: a person alone on the floor of a dark room at night, lit only by a phone"""
    S = Shot(3306)
    _phone_room(S)
    S.save('phone_night')


def phone_light():
    """ひとりで戦わせない: the same person; a warm gentle light resting on the shoulder, the room slowly brighter"""
    S = Shot(3307); p = S.p
    w = _phone_room(S, warm=True)
    p.glow(250, 600, 360, strength=0.9, density=0.8)
    p.glow(400, 960, 220, strength=1.1, density=1.0)
    p.lift(blur(p.ellipse(410, 955, 70, 50), 20), 'butter', 0.6, tooth=0)
    S.save('phone_light')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
