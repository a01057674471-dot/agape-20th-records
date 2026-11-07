"""all the kintsugi reel's paintings. python3 scenes.py NAME out.jpg ; crack paths go to ../art/cracks.json"""
import sys, json
from kcommon import *

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'art')
CR = {}


def table(b, y0, col='#c8a880'):
    t = (YY > y0).astype(np.float32)
    b.fill(t, 'blue', pressure=0.95, angle=0, seed=7)
    for k in range(10): b.ink([(40, y0 + 40 + k * 70), (1040, y0 + 44 + k * 70)], 2.2, colour='navy', dry=0.5, seed=8 + k)
    b.ink([(40, y0), (1040, y0)], 4.6, seed=6)
    return t


def a_drop():
    """the bowl slipping from a hand and breaking on the table"""
    b = page(2101)
    b.block((40, 50, 1040, 1870), 'powder', rough=10, corner=30, seed=11)
    table(b, 1240)
    # pieces of the broken bowl on the table, scattered
    pieces = [b.poly([(360, 1300), (520, 1290), (500, 1390), (380, 1400)]), b.poly([(540, 1310), (700, 1300), (690, 1420), (560, 1400)]),
              b.poly([(300, 1420), (420, 1410), (410, 1480), (290, 1470)]), b.poly([(720, 1430), (820, 1420), (830, 1480), (720, 1490)])]
    for k, pc in enumerate(pieces):
        b.fill(pc, 'cornflower', pressure=0.95, angle=80, seed=20 + k)
        b.fill(pc * (YY > 1380), 'deep', pressure=0.7, slip=0, seed=25 + k)
    for k, (x, y) in enumerate(((620, 1250), (460, 1270), (780, 1380), (260, 1380), (880, 1460))):
        b.dot(x, y, 6 + k % 3 * 2, colour='cornflower', medium='gouache')
    hand(b, 560, 760, 2.0, 120, SKIN, spread=10, curl=0.1)
    sleeve = b.band([(900, 380), (700, 600), (600, 700)], 230, 190)
    b.fill(sleeve, 'navy', pressure=0.95, angle=-40, seed=30)
    b.stage('blue')
    for pc in ([(360, 1300), (520, 1290), (500, 1390), (380, 1400)], [(540, 1310), (700, 1300), (690, 1420), (560, 1400)],
               [(300, 1420), (420, 1410), (410, 1480), (290, 1470)], [(720, 1430), (820, 1420), (830, 1480), (720, 1490)]):
        b.outline(pc, 4.0, smooth=False, seed=int(pc[0][0]))
    for k in range(7):                                 # little motion lines of the fall
        x = 470 + k * 30
        b.ink([(x, 1000 + k % 2 * 20), (x + 6, 1120)], 2.4, colour='slate', dry=0.4, seed=40 + k)
    for a in range(9):                                 # the crack 'burst'
        t = np.deg2rad(200 + a * 18)
        b.ink([(540 + np.cos(t) * 90, 1330 + np.sin(t) * 50), (540 + np.cos(t) * 160, 1330 + np.sin(t) * 90)], 3, seed=50 + a)
    b.outline([(900, 380), (700, 600), (600, 700)], 4, closed=False, seed=51)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=52)
    finish(b, os.path.join(ART, 'a_drop.jpg'))


def b_craft():
    """the craftsman's hands: lacquer brush on the joined pieces; tools on the bench"""
    b = page(2102)
    b.block((40, 50, 1040, 1870), 'mist', rough=10, corner=30, seed=11)
    table(b, 1160)
    cr = crack_paths(540, 900, 520, 360, seed=3, n=3)
    bowl(b, 540, 900, 520, 360, cracks=cr, seed=60)
    CR['b'] = cr
    # tools: lacquer jar, gold powder dish, brushes
    jar = b.poly([(150, 1220), (290, 1220), (300, 1380), (140, 1380)], smooth=False)
    b.fill(jar, 'teal', pressure=0.95, seed=70); b.outline([(150, 1220), (290, 1220), (300, 1380), (140, 1380)], 4, smooth=False, seed=71)
    b.fill(b.ellipse(220, 1222, 70, 16), 'navy', pressure=0.95, slip=0, seed=72)
    dish = b.ellipse(840, 1320, 130, 40)
    b.fill(dish, 'powder', pressure=0.95, seed=73); b.outline(circle_pts(840, 1320, 130, 40, n=30), 4, seed=74)
    b.fill(b.ellipse(840, 1312, 80, 20), GOLD, pressure=0.95, slip=0, medium='gouache', seed=75)
    b.speckle((760, 1295, 920, 1330), GOLD_HI, n=120, size=(0.6, 1.6), seed=76)
    for k in range(3):
        b.ink([(420 + k * 40, 1560), (560 + k * 50, 1460)], 6, colour='slate', seed=77 + k)
    hand(b, 860, 760, 1.7, 160, SKIN, curl=0.4)
    b.fill(b.band([(1100, 560), (980, 680), (900, 740)], 220, 180), 'navy', pressure=0.95, angle=-30, seed=78)
    b.ink([(760, 760), (650, 840)], 6, colour=INK, seed=79)                       # the brush
    b.dot(642, 846, 9, colour=GOLD, medium='gouache')
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=80)
    finish(b, os.path.join(ART, 'b_craft.jpg'))


def c_bowl():
    """the mended bowl, close and alone, cracks waiting for their gold (drawn on in the edit)"""
    b = page(2103)
    b.block((40, 50, 1040, 1870), 'powder', rough=10, corner=30, seed=11)
    b.fill(b.ellipse(540, 900, 520, 520), 'mist', pressure=0.6, slip=0, edge=40, dry_edge=0.9, seed=12)
    table(b, 1330)
    cr = crack_paths(540, 760, 760, 520, seed=5, n=4)
    bowl(b, 540, 760, 760, 520, cracks=cr, seed=90)
    CR['c'] = cr
    b.speckle((60, 60, 1020, 1860), 'chalk', n=700, size=(0.5, 1.3), seed=91)
    finish(b, os.path.join(ART, 'c_bowl.jpg'))


def person(b, x, y, R, seed, **kw):
    return Figure(b, x, y, R, coat='cobalt', hair='long', hair_col='#3b2b28', seed=seed, length=4.4, **kw)


def d_train():
    """a busy morning train: everyone looking at their phones; she smiles -- under her coat, faint cracks"""
    b = page(2104)
    f = person(b, 540, 900, 120, 1, look=(0.0, 0.1), mouth='smile',
               arms=[[(450, 1060), (430, 1200), (500, 1260)], [(630, 1060), (650, 1200), (580, 1260)]])
    others = [Figure(b, 170, 860, 92, coat='navy', hair='short', mouth='hmm', look=(0.2, 0.9), seed=2, length=4.4,
                     arms=[[(220, 990), (260, 1080), (240, 1100)]]),
              Figure(b, 910, 880, 96, coat='teal', hair='short', mouth='hmm', look=(-0.2, 0.9), seed=3, length=4.4,
                     arms=[[(860, 1010), (820, 1090), (840, 1110)]])]
    figs = others + [f]
    front = union(*[p.mask for p in figs])
    b.block((40, 50, 1040, 1870), 'mist', rough=10, corner=30, avoid=front, halo=3, seed=11)
    for x0 in (60, 400, 740):
        win = b.poly([(x0, 220), (x0 + 280, 220), (x0 + 280, 560), (x0, 560)], smooth=False) * (1 - front)
        b.fill(win, 'powder', pressure=0.95, angle=-10, seed=x0)
    b.ink([(40, 600), (1040, 600)], 5, seed=12); b.ink([(40, 140), (1040, 140)], 8, colour='slate', seed=13)
    for x in range(120, 1000, 120):
        b.ink([(x, 140), (x, 190)], 3, seed=x); b.outline(circle_pts(x, 205, 16, 16, n=14), 3, seed=x + 1)
    people_phase(figs, 'blue')
    for x0 in (60, 400, 740):
        b.outline([(x0, 220), (x0 + 280, 220), (x0 + 280, 560), (x0, 560)], 3.6, smooth=False, seed=x0 + 2)
    people_phase(figs, 'ink')
    for p_ in others:
        hx, hy = p_.arms[0][-1]
        b.fill(b.poly([(hx - 22, hy - 40), (hx + 22, hy - 40), (hx + 22, hy + 30), (hx - 22, hy + 30)], smooth=False), INK, pressure=0.95, slip=0, medium='gouache', seed=int(hx))
    people_phase(figs, 'dark'); people_phase(figs, 'accents')
    hc = heart_cracks(560, 1180, 1.0, seed=7)
    for p in hc: b.ink(p, 3.4, colour='chalk', dry=0.1, seed=int(p[-1][0]))
    CR['d'] = hc
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=14)
    finish(b, os.path.join(ART, 'd_train.jpg'))


def e_night():
    """night, her room: she sits on the floor against the bed, the smile gone; rain on the window; cracks show"""
    b = page(2105)
    f = person(b, 520, 1000, 120, 4, look=(0.0, 0.9), mouth='closed_eyes', brows=1.2,
               arms=[[(430, 1150), (420, 1290), (520, 1340)], [(610, 1150), (630, 1290), (540, 1340)]])
    win = b.poly([(560, 200), (960, 200), (960, 720), (560, 720)], smooth=False)
    b.block((40, 50, 1040, 1870), 'deep', rough=12, corner=30, avoid=union(f.mask, win), halo=3, seed=11)
    b.fill(win, 'navy', pressure=0.95, angle=-80, seed=12)
    bed = b.poly([(40, 1160), (1040, 1160), (1040, 1420), (40, 1420)], smooth=False) * (1 - f.mask)
    b.fill(bed, 'cornflower', pressure=0.95, angle=0, seed=13)
    floor_ = (YY > 1420).astype(np.float32) * (1 - f.mask)
    b.fill(floor_, 'blue', pressure=0.9, angle=2, seed=14)
    f.blue()
    b.outline([(560, 200), (960, 200), (960, 720), (560, 720)], 4.4, smooth=False, seed=15)
    b.ink([(760, 200), (760, 720)], 4, seed=16); b.ink([(560, 460), (960, 460)], 4, seed=17)
    f.ink(); f.dark(); f.accents()
    b.rain(win, n=160, angle=82, length=(10, 26), width=(1.6, 2.4), colour='chalk', seed=18)
    b.fill(b.ellipse(860, 300, 30, 30), 'butter', pressure=0.8, slip=0, seed=19)          # the moon
    hc = heart_cracks(540, 1280, 1.1, seed=8)
    for p in hc: b.ink(p, 3.6, colour='chalk', dry=0.1, seed=int(p[-1][0]))
    CR['e'] = hc
    b.speckle((60, 60, 1020, 1860), 'chalk', n=500, size=(0.5, 1.3), seed=20)
    finish(b, os.path.join(ART, 'e_night.jpg'))


def f_light():
    """rain at night on a park bench; a soft butter light comes down from above and finds her"""
    b = page(2106)
    f = person(b, 540, 1100, 104, 5, look=(0.0, -0.9), mouth='o',
               arms=[[(460, 1230), (440, 1350), (500, 1400)], [(620, 1230), (640, 1350), (580, 1400)]])
    beam = b.poly([(420, 80), (660, 80), (760, 1500), (320, 1500)])
    bench = b.poly([(200, 1440), (880, 1440), (880, 1480), (200, 1480)], smooth=False)
    b.block((40, 50, 1040, 1870), 'cobalt', rough=12, corner=30, avoid=f.mask, halo=3, seed=11)
    b.fill(beam * (1 - f.mask), 'butter', pressure=0.4, angle=90, slip=0, edge=30, dry_edge=0.9, seed=12)
    b.fill(bench * (1 - f.mask), 'navy', pressure=0.95, seed=13)
    ground = (YY > 1600).astype(np.float32)
    b.fill(ground, 'deep', pressure=0.9, angle=2, seed=14)
    f.blue(); f.ink()
    b.ink([(240, 1480), (240, 1600)], 6, seed=15); b.ink([(840, 1480), (840, 1600)], 6, seed=16)
    f.dark(); f.accents()
    b.rain((60, 60, 1020, 1860), n=600, angle=84, length=(12, 32), width=(1.6, 2.6), colour='deep', avoid=beam, seed=17)
    b.rain((60, 60, 1020, 1860), n=260, angle=84, length=(12, 28), width=(1.6, 2.4), colour='chalk', avoid=beam, seed=18)
    b.speckle((380, 60, 700, 1500), 'butter', n=500, size=(0.6, 1.8), seed=19)
    finish(b, os.path.join(ART, 'f_light.jpg'))


def g_cross():
    """far off, the cross on a hill; light from it spreading into the blue"""
    b = page(2107)
    cm = cross_mask(b, 540, 760, 440, w=260, t=34, arm=0.28)
    hill = b.poly([(40, 1870), (40, 1420), (300, 1290), (540, 1220), (780, 1290), (1040, 1420), (1040, 1870)])
    b.block((40, 50, 1040, 1870), 'blue', rough=12, corner=30, avoid=cm, halo=3, seed=11)
    b.fill(b.ellipse(540, 900, 560, 560) * (1 - cm), 'butter', pressure=0.45, slip=0, edge=50, dry_edge=0.9, seed=12)
    b.fill(hill, 'deep', pressure=0.95, angle=-10, seed=13)
    b.fill(cm, '#6a5a52', pressure=0.97, slip=0, medium='gouache', seed=14)
    cross_ink(b, 540, 760, 440, w=260, t=34, arm=0.28, width=4.2, seed=15)
    b.outline([(40, 1420), (300, 1290), (540, 1220), (780, 1290), (1040, 1420)], 5, closed=False, seed=16)
    b.crayon([[(540 + np.cos(a) * 600, 900 + np.sin(a) * 600), (540 + np.cos(a) * 720, 900 + np.sin(a) * 720)]
              for a in np.deg2rad(np.arange(190, 351, 16))], 'butter', width=8, pressure=0.7, seed=17)
    b.blades(40, 1040, lambda x: 1560 + 20 * np.sin(x / 70), n=50, height=(30, 80), width=4, seed=18)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=700, size=(0.5, 1.3), seed=19)
    finish(b, os.path.join(ART, 'g_cross.jpg'))


def h_dawn():
    """morning: she sits by the window with the mended bowl in her hands, looking up; her cracks wait for gold"""
    b = page(2108)
    f = person(b, 380, 960, 120, 6, look=(0.5, -0.6), mouth='smile',
               arms=[[(300, 1110), (300, 1250), (440, 1300)], [(470, 1110), (520, 1220), (560, 1280)]])
    win = b.poly([(620, 200), (1000, 200), (1000, 760), (620, 760)], smooth=False)
    b.block((40, 50, 1040, 1870), 'mist', rough=10, corner=30, avoid=union(f.mask, win), halo=3, seed=11)
    b.fill(win, 'powder', pressure=0.95, angle=-80, seed=12)
    b.fill(b.ellipse(810, 560, 120, 120), 'butter', pressure=0.8, slip=0, seed=13)
    b.fill(b.ellipse(810, 560, 420, 420) * (1 - f.mask) * (1 - win), 'butter', pressure=0.35, slip=0, edge=40, dry_edge=0.9, seed=14)
    table(b, 1420)
    f.blue()
    b.outline([(620, 200), (1000, 200), (1000, 760), (620, 760)], 4.4, smooth=False, seed=15)
    b.ink([(810, 200), (810, 760)], 4, seed=16)
    f.ink(); f.dark(); f.accents()
    cr = crack_paths(720, 1220, 300, 190, seed=9, n=2)
    bowl(b, 720, 1220, 300, 190, cracks=cr, seed=110)
    CR['h_bowl'] = cr
    hc = heart_cracks(400, 1180, 1.0, seed=9)
    for p in hc: b.ink(p, 3.2, colour='chalk', dry=0.1, seed=int(p[-1][0]))
    CR['h'] = hc
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=17)
    finish(b, os.path.join(ART, 'h_dawn.jpg'))


def i_end():
    b = page(2109)
    b.block((40, 50, 1040, 1870), 'powder', rough=10, corner=30, seed=11)
    b.fill(b.ellipse(540, 1300, 460, 420), 'mist', pressure=0.6, slip=0, edge=40, dry_edge=0.9, seed=12)
    cr = crack_paths(540, 1160, 560, 380, seed=5, n=4)
    bowl(b, 540, 1160, 560, 380, cracks=cr, seed=120)
    CR['i'] = cr
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=13)
    finish(b, os.path.join(ART, 'i_end.jpg'))


if __name__ == '__main__':
    name = sys.argv[1]
    globals()[name]()
    p = os.path.join(ART, f'cracks_{name}.json')
    json.dump({k: [[list(map(float, q)) for q in path] for path in v] for k, v in CR.items()}, open(p, 'w'))
