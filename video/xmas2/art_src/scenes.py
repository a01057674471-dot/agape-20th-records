"""Christmas special 「いちばん低いところに生まれた神様」: blue picture-book pages (BlueBook, the style of
「その十字架、本当の意味」) -- soft blue blocks, loose ink, mustard and coral lights.  python3 scenes.py NAME"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cross_meaning', 'scenes'))
from common import *
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art')


def lights(b, pts, r=7, seed=0):
    rr = np.random.default_rng(seed)
    for k, (x, y) in enumerate(pts):
        b.fill(b.ellipse(x, y, r * 3.2, r * 3.2), 'butter', pressure=0.35, slip=0, edge=10, dry_edge=0.9, lanes=0, seed=seed + k)
        b.dot(x, y, r, colour='mustard' if k % 3 else 'butter', medium='gouache', seed=seed + 500 + k)


def halo(b, x, y, r, colour='butter', seed=0, pressure=0.45):
    b.fill(b.ellipse(x, y, r, r), colour, pressure=pressure, slip=0, edge=r * 0.4, dry_edge=0.95, lanes=0, seed=seed)


def stars(b, region, n=60, seed=0):
    rr = np.random.default_rng(seed); k = 0
    while k < n:
        x, y = rr.uniform(60, 1020), rr.uniform(80, 1200)
        if region[int(y), int(x)] < 0.5: continue
        b.dot(x, y, rr.uniform(1.8, 3.6), colour='chalk', medium='gouache', seed=seed + k); k += 1


def save(b, name):
    finish(b, os.path.join(ART, name + '.jpg'))


def illum():
    """Christmas lights on a Japanese street at night; among them one small warm light"""
    b = page(1501)
    bl = [b.poly([(40, 1500), (40, 520), (330, 520), (330, 1500)], smooth=False), b.poly([(750, 1500), (750, 600), (1040, 600), (1040, 1500)], smooth=False),
          b.poly([(330, 1500), (330, 760), (420, 700), (510, 760), (510, 1500)], smooth=False)]
    tree = b.poly([(620, 640), (520, 960), (560, 960), (480, 1260), (530, 1260), (450, 1500), (790, 1500), (710, 1260), (760, 1260), (680, 960), (720, 960)], smooth=False)
    road = (YY > 1500).astype(np.float32)
    b.block((40, 60, 1040, 1860), 'deep', rough=10, corner=30, avoid=union(*bl, tree), halo=3, seed=11)
    for k, m in enumerate(bl):
        b.fill(m, ['blue', 'cobalt', 'cornflower'][k], pressure=0.95, angle=90, seed=12 + k)
    b.fill(tree, 'teal', pressure=0.95, angle=70, seed=15)
    b.fill(road, 'cobalt', pressure=0.9, angle=0, seed=16)
    b.stage('blue')
    for m in bl:
        ys, xs = np.nonzero(m > 0.5)
        b.outline([(xs.min(), ys.max()), (xs.min(), ys.min()), (xs.max(), ys.min()), (xs.max(), ys.max())], 4.2, closed=False, smooth=False, seed=int(xs.min()))
    b.outline([(620, 640), (520, 960), (560, 960), (480, 1260), (530, 1260), (450, 1500), (790, 1500), (710, 1260), (760, 1260), (680, 960), (720, 960)], 4.2, smooth=False, seed=17)
    b.ink([(40, 1500), (1040, 1500)], 4, seed=18)
    b.stage('ink')
    b.scribble(road * (YY > 1700), width=4, spacing=5, angle=10, colour='navy', dry=0.5, seed=31)
    b.stage('dark')
    for (x0, x1, y0, y1) in ((80, 300, 580, 1450), (790, 1000, 660, 1450)):
        for yy in range(y0, y1, 170):
            for xx in range(x0, x1 - 60, 110):
                b.fill(b.poly([(xx, yy), (xx + 60, yy), (xx + 60, yy + 90), (xx, yy + 90)], smooth=False), 'mustard', pressure=0.9, angle=0, slip=0, lanes=0, seed=xx + yy)
    t = np.linspace(0, 1, 26)
    lights(b, [(1080 * u, 380 + 90 * np.sin(u * np.pi)) for u in t], 6, seed=40)
    lights(b, [(620 + (40 + u * 120) * np.sin(u * 20), 680 + u * 800) for u in np.linspace(0, 1, 30)], 6, seed=80)
    b.ink([(0, 380), (1080, 380)], 0.1, seed=1)
    halo(b, 300, 1640, 120, 'butter', seed=99, pressure=0.6)
    b.dot(300, 1640, 16, colour='mustard', medium='gouache', seed=98)
    b.stage('accents')
    stars(b, (YY < 500).astype(np.float32), 30, seed=5)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'illum')


def starbeam():
    """a soft beam of starlight coming down from the night sky toward a quiet little village"""
    b = page(1502)
    hill = b.poly([(40, 1860), (40, 1250), (300, 1180), (600, 1220), (1040, 1150), (1040, 1860)])
    houses = [b.poly([(x, 1330), (x, 1240), (x + 50, 1200), (x + 100, 1240), (x + 100, 1330)], smooth=False) for x in (260, 420, 600, 760)]
    beam = b.poly([(520, 260), (560, 260), (760, 1230), (360, 1230)], smooth=False)
    b.block((40, 60, 1040, 1860), 'navy', rough=10, corner=30, avoid=hill, halo=3, seed=11)
    b.fill(beam * (1 - hill), 'cornflower', pressure=0.55, angle=90, slip=0, seed=12)
    b.fill(hill, 'blue', pressure=0.95, angle=-70, avoid=union(*houses), halo=2, seed=13)
    b.fill(hill * (YY > 1500), 'cobalt', pressure=0.85, angle=-70, slip=0, avoid=union(*houses), seed=14)
    for k, hm in enumerate(houses): b.fill(hm, 'powder', pressure=0.95, angle=90, seed=15 + k)
    b.stage('blue')
    b.outline([(40, 1250), (300, 1180), (600, 1220), (1040, 1150)], 4.6, closed=False, seed=21)
    for k, x in enumerate((260, 420, 600, 760)):
        b.outline([(x, 1330), (x, 1240), (x + 50, 1200), (x + 100, 1240), (x + 100, 1330)], 3.6, smooth=False, seed=22 + k)
    b.stage('ink')
    b.chalk([[(540, 270), (540, 1180)]], width=60, pressure=0.25, seed=31)
    for k, x in enumerate((260, 420, 600, 760)):
        b.fill(b.poly([(x + 35, 1270), (x + 65, 1270), (x + 65, 1300), (x + 35, 1300)], smooth=False), 'mustard', pressure=0.95, slip=0, lanes=0, seed=40 + k)
    halo(b, 540, 250, 140, 'butter', seed=41, pressure=0.7)
    b.dot(540, 250, 20, colour='chalk', medium='gouache', seed=42)
    b.crayon([[(540 + np.cos(a) * 30, 250 + np.sin(a) * 30), (540 + np.cos(a) * 80, 250 + np.sin(a) * 80)] for a in np.deg2rad(np.arange(0, 360, 45))], 'butter', width=6, pressure=0.8, seed=43)
    r = np.random.default_rng(44)
    for k in range(18):
        y = r.uniform(350, 1150); half = 20 + (y - 260) / 970 * 200
        b.dot(540 + r.uniform(-half, half), y, r.uniform(2, 4.5), colour='butter', medium='gouache', seed=45 + k)
    b.stage('accents')
    stars(b, (YY < 1100).astype(np.float32) * (np.abs(XX - 540) > 160), 70, seed=6)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'starbeam')


def manger():
    """a newborn wrapped in cloth lying in a wooden feeding trough; the young mother and father beside him, gentle animals,
    a humble shelter, warm lantern light"""
    b = page(1503)
    mary = Figure(b, 360, 900, 82, coat='cornflower', hair='long', hair_col='#3b2b28', dress=True, length=4.2, seed=1, mouth='closed_eyes',
                  arms=[[(330, 1010), (380, 1120), (460, 1150)]])
    jos = Figure(b, 760, 820, 86, coat='teal', hair='short', beard=True, length=4.6, seed=2, look=(-0.3, 0.3),
                 arms=[[(800, 940), (840, 1070), (820, 1170)]])
    figs = [mary, jos]
    front = union(mary.mask, jos.mask)
    trough = b.poly([(400, 1280), (700, 1280), (660, 1420), (440, 1420)], smooth=False)
    legs = union(b.poly([(450, 1410), (470, 1410), (440, 1520), (420, 1520)], smooth=False), b.poly([(630, 1410), (650, 1410), (680, 1520), (660, 1520)], smooth=False))
    baby = b.blob(550, 1255, 120, 46, 0.06, seed=3)
    face = b.ellipse(470, 1245, 34, 32)
    roof = b.poly([(40, 520), (540, 340), (1040, 520), (1040, 600), (40, 600)], smooth=False)
    posts = union(b.poly([(120, 600), (150, 600), (150, 1560), (120, 1560)], smooth=False), b.poly([(930, 600), (960, 600), (960, 1560), (930, 1560)], smooth=False))
    floor = (YY > 1520).astype(np.float32)
    sheep = [b.cloud(220, 1600, 170, 110, 5, seed=4), b.cloud(880, 1640, 160, 100, 5, seed=5)]
    donkey = union(b.ellipse(870, 1240, 120, 70), b.ellipse(990, 1160, 46, 40))
    allfront = union(front, trough, baby, face, *sheep, donkey, legs)
    b.block((40, 60, 1040, 1860), 'navy', rough=10, corner=30, avoid=union(roof, posts, allfront), halo=3, seed=11)
    b.fill(b.poly([(150, 600), (930, 600), (930, 1520), (150, 1520)], smooth=False) * (1 - allfront), 'blue', pressure=0.95, angle=90, seed=12)
    b.fill(roof, 'cobalt', pressure=0.95, angle=20, seed=13)
    b.fill(posts, 'deep', pressure=0.95, angle=90, seed=14)
    b.fill(floor * (1 - allfront), 'cornflower', pressure=0.95, angle=0, seed=15)
    b.fill(trough, '#9a8a7e', pressure=0.95, angle=0, medium='gouache', seed=16)
    b.fill(legs, '#7a6a60', pressure=0.95, angle=90, medium='gouache', seed=17)
    b.fill(donkey, 'slate', pressure=0.95, angle=20, seed=18)
    people_phase(figs, 'blue')
    b.stage('blue')
    b.outline([(400, 1280), (700, 1280), (660, 1420), (440, 1420)], 4.2, smooth=False, seed=21)
    for m in (legs,): pass
    b.outline(circle_pts(870, 1240, 120, 70, n=30), 3.8, seed=22)
    b.outline(circle_pts(990, 1160, 46, 40, n=20), 3.6, seed=23)
    for x in (960, 1010): b.ink([(x, 1130), (x + 10, 1070)], 4, seed=x)
    for x in (800, 840, 900, 940): b.ink([(x, 1300), (x, 1390)], 4, seed=x + 1)
    for k, s in enumerate(sheep):
        ys, xs = np.nonzero(s > 0.5)
        b.outline(circle_pts((xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2, (xs.max() - xs.min()) / 2, (ys.max() - ys.min()) / 2, n=28), 3.4, open_=0.7, seed=24 + k)
    b.outline([(40, 520), (540, 340), (1040, 520)], 4.6, closed=False, seed=26)
    b.outline(circle_pts(550, 1255, 120, 46, n=28), 3.4, seed=27)
    b.head(470, 1245, 34, 32, width=3.2, seed=28)
    for sgn in (-1, 1): b.ink([(470 + sgn * 12 - 5, 1245), (470 + sgn * 12, 1249), (470 + sgn * 12 + 5, 1245)], 2.2, seed=29 + sgn)
    people_phase(figs, 'ink')
    b.stage('ink')
    b.hatch(trough, angle=10, spacing=9, length=(20, 40), width=2, colour='navy', density=0.7, seed=31)
    people_phase(figs, 'dark')
    b.stage('dark')
    halo(b, 550, 1200, 330, 'butter', seed=40, pressure=0.55)
    b.fill(face, 'flesh', pressure=0.6, lanes=0, seed=41)
    b.blush(470, 1258, 8, seed=42)
    b.fill(b.poly([(420, 1270), (680, 1270), (690, 1290), (410, 1290)], smooth=False), 'mustard', pressure=0.85, slip=0, lanes=0, seed=43)   # straw
    b.crayon([[(420 + k * 26, 1280), (430 + k * 26, 1262)] for k in range(11)], 'mustard', width=4, pressure=0.8, seed=44)
    lx, ly = 760, 700
    b.ink([(lx, 600), (lx, ly - 40)], 2.4, seed=45)
    b.fill(b.poly([(lx - 26, ly - 40), (lx + 26, ly - 40), (lx + 30, ly + 30), (lx - 30, ly + 30)], smooth=False), 'mustard', pressure=0.95, slip=0, lanes=0, seed=46)
    halo(b, lx, ly, 150, 'butter', seed=47, pressure=0.6)
    people_phase(figs, 'accents')
    b.stage('accents')
    for s in sheep: b.chalk(s, pressure=0.9, seed=50)
    b.chalk(baby * (1 - face), pressure=0.95, seed=51)
    people_phase(figs, 'chalk')
    stars(b, (YY < 330).astype(np.float32), 25, seed=7)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'manger')


def flight():
    """the young family travelling through the desert at night, the mother and baby on a donkey, the father leading it"""
    b = page(1504)
    mary = Figure(b, 520, 960, 70, coat='cornflower', hair='long', hair_col='#3b2b28', dress=True, length=3.0, seed=1, mouth='closed_eyes',
                  arms=[[(500, 1050), (540, 1110), (590, 1100)]])
    jos = Figure(b, 820, 1000, 74, coat='teal', hair='short', beard=True, length=4.2, seed=2, look=(-0.4, 0.0),
                 arms=[[(770, 1110), (700, 1150), (650, 1170)]])
    figs = [mary, jos]
    babe = b.blob(585, 1090, 40, 30, 0.06, seed=3)
    donkey = union(b.ellipse(520, 1250, 170, 90), b.ellipse(690, 1150, 56, 46))
    dunes = b.poly([(40, 1860), (40, 1380), (300, 1320), (620, 1400), (1040, 1330), (1040, 1860)])
    front = union(mary.mask, jos.mask, babe, donkey)
    b.block((40, 60, 1040, 1860), 'navy', rough=10, corner=30, avoid=union(front, dunes), halo=3, seed=11)
    b.fill(dunes * (1 - front), 'cobalt', pressure=0.95, angle=-10, seed=12)
    b.fill(dunes * (YY > 1600) * (1 - front), 'blue', pressure=0.85, angle=-10, slip=0, seed=13)
    b.fill(donkey, 'slate', pressure=0.95, angle=20, seed=14)
    people_phase(figs, 'blue')
    b.stage('blue')
    b.outline(circle_pts(520, 1250, 170, 90, n=30), 3.8, seed=21)
    b.outline(circle_pts(690, 1150, 56, 46, n=20), 3.6, seed=22)
    for x in (680, 720): b.ink([(x, 1110), (x + 14, 1040)], 4, seed=x)
    for x in (400, 450, 580, 630): b.ink([(x, 1320), (x + (6 if x % 2 else -6), 1420)], 4.4, seed=x + 1)
    b.ink([(380, 1220), (340, 1300)], 3, seed=23)
    b.outline([(40, 1380), (300, 1320), (620, 1400), (1040, 1330)], 4.2, closed=False, seed=24)
    b.ink([(650, 1170), (690, 1170)], 2.4, seed=25)
    b.outline(circle_pts(585, 1090, 40, 30, n=20), 3, seed=26)
    people_phase(figs, 'ink')
    b.stage('ink')
    people_phase(figs, 'dark')
    b.stage('dark')
    b.fill(b.ellipse(1030 - 130, 260, 70, 70) * 0 + b.ellipse(880, 300, 60, 60) * (1 - b.ellipse(905, 285, 52, 52)), 'butter', pressure=0.95, slip=0, lanes=0, seed=40)
    people_phase(figs, 'accents')
    b.stage('accents')
    b.chalk(babe, pressure=0.95, seed=50)
    people_phase(figs, 'chalk')
    stars(b, (YY < 1250).astype(np.float32) * (1 - front), 120, seed=8)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'flight')


def carpenter():
    """a young man in simple clothes working wood at his bench in a small workshop, warm sunlight, a bead of sweat"""
    b = page(1505)
    jes = Figure(b, 560, 760, 90, coat='powder', hair='short', beard=True, length=4.4, seed=1, look=(0.0, 0.6), legs=False,
                 arms=[[(490, 890), (450, 1030), (460, 1130)], [(630, 890), (690, 1030), (680, 1130)]])
    bench = b.poly([(120, 1150), (980, 1150), (980, 1230), (120, 1230)], smooth=False)
    blegs = union(b.poly([(170, 1230), (210, 1230), (210, 1560), (170, 1560)], smooth=False), b.poly([(890, 1230), (930, 1230), (930, 1560), (890, 1560)], smooth=False))
    board = b.poly([(220, 1110), (900, 1100), (900, 1150), (220, 1150)], smooth=False)
    plane = b.poly([(420, 1080), (560, 1076), (560, 1120), (420, 1124)], smooth=False)
    win = b.poly([(700, 240), (980, 240), (980, 560), (700, 560)], smooth=False)
    floor = (YY > 1560).astype(np.float32)
    front = union(jes.mask, bench, blegs, board, plane)
    b.block((40, 60, 1040, 1860), 'powder', rough=10, corner=30, avoid=union(front, win), halo=3, seed=11)
    b.fill(win, 'mist', pressure=0.9, angle=0, seed=12)
    b.fill(b.poly([(700, 560), (980, 560), (700, 1500), (300, 1500)], smooth=False) * (1 - front), 'butter', pressure=0.45, slip=0, edge=30, dry_edge=0.9, seed=13)
    b.fill(floor * (1 - front), 'cornflower', pressure=0.95, angle=0, seed=14)
    b.fill(union(bench, blegs), '#9a8a7e', pressure=0.95, angle=0, medium='gouache', seed=15)
    b.fill(board, '#c8a46e', pressure=0.95, angle=0, medium='gouache', seed=16)
    b.fill(plane, '#7a6a60', pressure=0.95, angle=0, medium='gouache', seed=17)
    people_phase([jes], 'blue')
    b.stage('blue')
    b.outline([(700, 240), (980, 240), (980, 560), (700, 560)], 4.2, smooth=False, seed=21)
    b.ink([(840, 240), (840, 560)], 3, seed=22); b.ink([(700, 400), (980, 400)], 3, seed=23)
    b.outline([(120, 1150), (980, 1150), (980, 1230), (120, 1230)], 4.2, smooth=False, seed=24)
    b.outline([(220, 1110), (900, 1100), (900, 1150), (220, 1150)], 3.4, smooth=False, seed=25)
    for x in (190, 910): b.ink([(x, 1230), (x, 1560)], 6, seed=x)
    for k in range(5):                       # tools on the wall
        x = 120 + k * 100
        b.ink([(x, 300), (x, 520)], 4, seed=30 + k)
    people_phase([jes], 'ink')
    b.stage('ink')
    people_phase([jes], 'dark')
    b.stage('dark')
    r = np.random.default_rng(3)
    for k in range(7):
        x, y = r.uniform(250, 900), r.uniform(1050, 1100)
        b.crayon([circle_pts(x, y, 22, 12, 0, 330, 12)], 'mustard', width=5, pressure=0.8, seed=40 + k)
    halo(b, 840, 400, 220, 'butter', seed=47, pressure=0.6)
    people_phase([jes], 'accents')
    b.dot(625, 715, 6, ry=9, colour='chalk', medium='gouache', seed=48)        # a bead of sweat
    b.stage('accents')
    people_phase([jes], 'chalk')
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'carpenter')


def withpoor():
    """a gentle man in simple robes sitting with the poor, the sick and the lonely, sharing bread in the evening light"""
    b = page(1506)
    jes = Figure(b, 540, 880, 84, coat='chalk', hair='short', beard=True, length=3.6, seed=1, mouth='smile',
                 arms=[[(600, 990), (680, 1060), (740, 1050)]])
    guests = [Figure(b, 230, 980, 70, coat='slate', hair='short', length=3.2, seed=2, look=(0.3, 0)),
              Figure(b, 850, 990, 70, coat='cobalt', hair='bun', hair_col='#8a8a8a', length=3.2, seed=3, look=(-0.3, 0)),
              Figure(b, 330, 1250, 64, coat='blue', hair='long', hair_col='#3b2b28', back=True, length=3.0, seed=4),
              Figure(b, 760, 1260, 64, coat='teal', hair='short', back=True, length=3.0, seed=5)]
    figs = [jes] + guests
    cloth = b.ellipse(540, 1240, 300, 80)
    front = union(*[f.mask for f in figs])
    ground = (YY > 1150).astype(np.float32)
    b.block((40, 60, 1040, 1860), 'mist', rough=10, corner=30, avoid=front, halo=3, seed=11)
    b.fill(b.ellipse(540, 760, 330, 260) * (1 - front), 'butter', pressure=0.3, slip=0, edge=80, dry_edge=0.95, seed=12)
    b.fill(ground * (1 - front), 'cornflower', pressure=0.95, angle=0, avoid=cloth, halo=2, seed=13)
    b.fill(cloth * (1 - front), 'powder', pressure=0.95, angle=0, seed=14)
    people_phase(figs, 'blue')
    b.stage('blue')
    b.outline(circle_pts(540, 1240, 300, 80, n=40), 3.6, seed=21)
    people_phase(figs, 'ink')
    b.stage('ink')
    people_phase(figs, 'dark')
    b.stage('dark')
    for (x, y) in ((440, 1230), (560, 1250), (650, 1220), (750, 1050)):
        bl = b.blob(x, y, 46, 26, 0.1, seed=x)
        b.fill(bl, '#c8a46e', pressure=0.95, angle=0, medium='gouache', lanes=0, seed=x + 1)
        b.outline(circle_pts(x, y, 46, 26, n=18), 2.8, seed=x + 2)
    halo(b, 540, 860, 150, 'butter', seed=40, pressure=0.35)
    people_phase(figs, 'accents')
    b.stage('accents')
    people_phase(figs, 'chalk')
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'withpoor')


def tears():
    """the gentle man standing with his grieving friends, quietly shedding tears, soft sorrowful light"""
    b = page(1507)
    jes = Figure(b, 540, 760, 92, coat='chalk', hair='short', beard=True, length=4.8, seed=1, mouth='closed_eyes',
                 arms=[[(480, 890), (440, 1040), (410, 1120)]])
    m1 = Figure(b, 300, 880, 80, coat='slate', hair='long', hair_col='#3b2b28', dress=True, length=4.4, seed=2, mouth='closed_eyes')
    m2 = Figure(b, 800, 900, 78, coat='cobalt', hair='bun', hair_col='#3b2b28', dress=True, length=4.4, seed=3, mouth='closed_eyes')
    figs = [m1, m2, jes]
    tomb = b.poly([(40, 1250), (40, 700), (200, 640), (300, 700), (300, 1250)], smooth=False)
    ground = (YY > 1250).astype(np.float32)
    front = union(*[f.mask for f in figs])
    b.block((40, 60, 1040, 1860), 'powder', rough=10, corner=30, avoid=union(front, tomb), halo=3, seed=11)
    b.fill(tomb * (1 - front), 'cornflower', pressure=0.95, angle=-60, seed=12)
    b.fill(ground * (1 - front), 'blue', pressure=0.95, angle=0, seed=13)
    people_phase(figs, 'blue')
    b.stage('blue')
    b.outline([(40, 700), (200, 640), (300, 700), (300, 1250)], 4.2, closed=False, smooth=False, seed=21)
    people_phase(figs, 'ink')
    b.stage('ink')
    people_phase(figs, 'dark')
    b.scribble(ground * (YY > 1600), width=4, spacing=5, angle=10, colour='cobalt', dry=0.5, seed=31)
    b.stage('dark')
    people_phase(figs, 'accents')
    for (x, y) in ((505, 800), (575, 800)):
        b.dot(x, y + 22, 5, ry=8, colour='cornflower', medium='gouache', seed=x)
        b.ink([(x, y + 6), (x, y + 16)], 1.6, colour='cornflower', seed=x + 1)
    b.stage('accents')
    people_phase(figs, 'chalk')
    b.chalk(b.cloud(780, 260, 280, 100, 5, seed=53), pressure=0.7, seed=53)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'tears')


def window():
    """someone sitting alone by the window at night; a soft warm light resting on their shoulder; Christmas lights outside"""
    b = page(1508)
    who = Figure(b, 420, 1000, 88, coat='cobalt', hair='long', hair_col='#3b2b28', back=False, length=4.6, seed=1, mouth='closed_eyes', legs=False,
                 arms=[[(360, 1110), (380, 1240), (440, 1270)]])
    win = b.poly([(560, 300), (980, 300), (980, 980), (560, 980)], smooth=False)
    sill = b.poly([(520, 980), (1020, 980), (1020, 1030), (520, 1030)], smooth=False)
    floor = (YY > 1400).astype(np.float32)
    front = union(who.mask, sill)
    b.block((40, 60, 1040, 1860), 'blue', rough=10, corner=30, avoid=union(front, win), halo=3, seed=11)
    b.fill(win, 'navy', pressure=0.95, angle=0, seed=12)
    b.fill(sill, 'powder', pressure=0.95, angle=0, seed=13)
    b.fill(floor * (1 - front), 'cobalt', pressure=0.95, angle=0, seed=14)
    people_phase([who], 'blue')
    b.stage('blue')
    b.outline([(560, 300), (980, 300), (980, 980), (560, 980)], 4.6, smooth=False, seed=21)
    b.ink([(770, 300), (770, 980)], 4, seed=22); b.ink([(560, 640), (980, 640)], 4, seed=23)
    b.outline([(520, 980), (1020, 980), (1020, 1030), (520, 1030)], 3.8, smooth=False, seed=24)
    people_phase([who], 'ink')
    b.stage('ink')
    people_phase([who], 'dark')
    b.stage('dark')
    t = np.linspace(0.05, 0.95, 12)
    lights(b, [(560 + 420 * u, 420 + 60 * np.sin(u * np.pi)) for u in t], 5, seed=40)
    lights(b, [(560 + 420 * u, 760 + 50 * np.sin(u * np.pi)) for u in t], 5, seed=60)
    halo(b, 470, 1110, 210, 'butter', seed=80, pressure=0.7)
    halo(b, 470, 1110, 110, 'mustard', seed=81, pressure=0.35)
    people_phase([who], 'accents')
    b.stage('accents')
    people_phase([who], 'chalk')
    stars(b, win * (YY < 960), 25, seed=9)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=54)
    save(b, 'window')


if __name__ == '__main__':
    globals()[sys.argv[1]]()
