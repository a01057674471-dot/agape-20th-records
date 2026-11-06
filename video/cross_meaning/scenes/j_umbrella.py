"""J. 自分を差し出してでも、相手を大切にする: in the rain, one person holds their only umbrella over a friend --
the friend is dry under coral, the one holding it is getting soaked and smiling anyway."""
from common import *

def main(out, stages=None):
    b = page(1001, stages)
    giver = Figure(b, 700, 1000, 100, coat='cobalt', hair='short', look=(-0.8, 0.2), mouth='smile', seed=1, length=4.2,
                   arms=[[(640, 1130), (560, 1060), (490, 900)]])
    friend = Figure(b, 400, 1080, 92, coat='mustard', hair='bun', hair_col='#3b2b28', look=(0.7, -0.6), mouth='smile', seed=2,
                    length=4.2, arms=[[(340, 1200), (330, 1330), (370, 1400)], [(460, 1200), (480, 1330), (450, 1400)]])
    canopy = b.poly([(160, 860), (240, 720), (420, 640), (560, 700), (640, 820), (500, 830), (380, 860), (260, 880)])
    dry = np.maximum(canopy, b.poly([(160, 860), (640, 820), (560, 1600), (200, 1600)]))
    figs = [friend, giver]
    front = union(giver.mask, friend.mask, canopy)
    b.block((40, 50, 1040, 1870), 'powder', rough=10, corner=30, avoid=front, halo=3, seed=11)
    pave = (YY > 1500).astype(np.float32)
    b.fill(pave * (1 - front), 'cornflower', pressure=0.9, angle=2, seed=12)
    for x, y, rx, ry in ((560, 1640, 260, 40), (880, 1760, 140, 26)):
        b.fill(b.blob(x, y, rx, ry, 0.06, int(x)), 'blue', pressure=0.95, angle=4, slip=0, seed=int(x))
    people_phase(figs, 'blue')
    b.fill(giver.S['body'] * (YY > 1100), 'deep', pressure=0.6, angle=80, slip=0, seed=13)          # soaked coat
    b.stage('blue')
    b.outline([(160, 860), (240, 720), (420, 640), (560, 700), (640, 820), (500, 830), (380, 860), (260, 880)], 4.6, seed=21)
    b.ink([(420, 640), (420, 600)], 4, seed=22)
    b.ink([(400, 845), (420, 650)], 2.6, seed=23); b.ink([(260, 870), (420, 650)], 2.6, seed=24); b.ink([(560, 820), (420, 650)], 2.6, seed=25)
    b.ink([(490, 900), (430, 650)], 5, seed=26)
    people_phase(figs, 'ink')
    b.stage('ink')
    people_phase(figs, 'dark')
    b.stage('dark')
    b.fill(canopy, 'coral', pressure=0.96, angle=-30, seed=41)
    b.hatch(canopy * (XX > 480), angle=60, spacing=6, length=(14, 30), width=3, colour='tomato', medium='crayon', seed=42)
    people_phase(figs, 'accents')
    b.stage('accents')
    b.rain((60, 60, 1020, 1860), n=800, angle=82, length=(12, 36), width=(1.6, 2.8), colour='deep', avoid=dry, seed=51)
    b.rain((60, 60, 1020, 1860), n=360, angle=82, length=(12, 28), width=(1.6, 2.6), colour='chalk', avoid=dry, seed=52)
    for x, y in ((650, 900), (700, 895), (750, 905), (680, 1180), (760, 1250)):
        b.splash(x, y, 13, 'chalk', n=4, seed=int(x + y))
    for x, y in ((620, 960), (780, 960)):
        b.ink([(x, y), (x + 1, y + 14)], 3, colour='deep', seed=int(x))
        b.dot(x + 2, y + 26, 2.6, 3.5, colour='deep', medium='crayon')
    for u in (180, 300, 420, 560):
        b.ink([(u, 880), (u + 2, 896)], 3, colour='deep', seed=u)
    b.ripples(560, 1640, 60, 9, rings=2, seed=53); b.ripples(880, 1760, 30, 6, rings=2, seed=54)
    b.stage('rain')
    finish(b, out, stages)
