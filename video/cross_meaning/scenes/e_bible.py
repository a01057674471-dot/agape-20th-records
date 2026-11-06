"""E. 聖書によると: an open Bible on a small table by a rainy window, a lamp with a warm mustard glow."""
from common import *

def main(out, stages=None):
    b = page(501, stages)
    win = b.poly([(160, 200), (920, 200), (920, 900), (160, 900)], smooth=False)
    table = b.poly([(40, 1180), (1040, 1180), (1040, 1870), (40, 1870)], smooth=False)
    L = b.poly([(170, 1300), (330, 1250), (530, 1290), (530, 1640), (330, 1600), (170, 1650)])
    R = b.poly([(550, 1290), (750, 1250), (910, 1300), (910, 1650), (750, 1600), (550, 1640)])
    book = union(L, R)
    lamp = b.poly([(800, 760), (960, 760), (1010, 900), (750, 900)], smooth=False)
    b.block((40, 50, 1040, 1180), 'mist', rough=10, corner=30, avoid=union(win, lamp), halo=3, seed=11)
    b.fill(win, 'cornflower', pressure=0.95, angle=-80, seed=12)
    b.fill(table, 'blue', pressure=0.95, angle=0, avoid=book, halo=3, seed=13)
    b.fill(b.poly([(160, 1560), (920, 1560), (940, 1700), (140, 1700)]) * (1 - book), 'deep', pressure=0.6, angle=0, slip=0, seed=14)
    b.stage('blue')
    b.outline([(160, 200), (920, 200), (920, 900), (160, 900)], 5, smooth=False, seed=21)
    b.ink([(540, 200), (540, 900)], 4, seed=22); b.ink([(160, 550), (920, 550)], 4, seed=23)
    b.ink([(40, 1180), (1040, 1180)], 5, seed=24)
    for pts in ([(170, 1300), (330, 1250), (530, 1290), (530, 1640), (330, 1600), (170, 1650)],
                [(550, 1290), (750, 1250), (910, 1300), (910, 1650), (750, 1600), (550, 1640)]):
        b.outline(pts, 4.4, seed=int(pts[0][0]))
    for side in (0, 1):
        x0 = 205 if side == 0 else 585
        for k in range(9):
            y = 1330 + k * 30
            b.ink([(x0, y), (x0 + 290, y - 6 + (6 if side else 0))], 2.0, colour='slate', dry=0.4, seed=30 + k + side * 20)
    b.outline([(800, 760), (960, 760), (1010, 900), (750, 900)], 4, smooth=False, seed=25)
    b.ink([(880, 900), (880, 1180)], 6, seed=26); b.ink([(820, 1180), (940, 1180)], 6, seed=27)
    b.stage('ink')
    b.hatch(table * (YY > 1700), angle=-10, spacing=9, length=(30, 60), width=2.2, density=0.6, seed=31)
    b.stage('dark')
    b.fill(lamp, 'mustard', pressure=0.95, angle=0, seed=41)
    b.fill(b.ellipse(880, 1040, 260, 200) * (1 - lamp) * (1 - win), 'butter', pressure=0.35, angle=0, slip=0, seed=42)
    b.ink([(560, 1290), (566, 1700)], 7, colour='coral', seed=43)                  # ribbon
    b.stage('accents')
    b.chalk(book, pressure=0.7, angle=90, seed=51)
    b.rain(win, n=180, angle=82, length=(10, 28), width=(1.6, 2.6), colour='chalk', seed=52)
    b.rain(win, n=160, angle=82, length=(10, 28), width=(1.6, 2.6), colour='deep', seed=53)
    b.speckle((60, 60, 1020, 1860), 'chalk', n=600, size=(0.5, 1.3), seed=54)
    b.stage('chalk')
    finish(b, out, stages)
