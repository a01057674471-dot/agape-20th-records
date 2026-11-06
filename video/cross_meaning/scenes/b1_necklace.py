"""B1. a young woman wearing a small gold cross on a fine chain, just as an accessory -- a close-up bust."""
from common import *

def main(out, stages=None):
    b = page(201, stages)
    f = Figure(b, 540, 640, 230, coat='cobalt', hair='long', hair_col='#3b2b28', look=(0.2, 0.2), mouth='smile', seed=1,
               legs=False, length=6.0, collar=False)
    f.body_pts = [(460, 840), (620, 840), (660, 930), (900, 1040), (1000, 1200), (1040, 1870), (40, 1870), (80, 1200), (180, 1040), (420, 930)]
    neckv = b.poly([(430, 900), (650, 900), (540, 1280)])
    f.S['body'] = b.poly(f.body_pts) * (1 - neckv)
    f.mask = np.maximum.reduce([f.S['head'], f.S['body'], f.S['hair'], neckv])
    b.block((40, 50, 1040, 1870), 'powder', rough=10, corner=30, avoid=f.mask, halo=3, seed=11)
    f.blue()
    b.stage('blue')
    f.ink(w=6)
    b.ink([(430, 900), (540, 1280), (650, 900)], 5, seed=21)
    chain = [(450, 920), (476, 1030), (512, 1092), (540, 1110), (568, 1092), (604, 1030), (630, 920)]
    b.ink(chain, 2.2, colour='#b08030', dry=0.0, seed=27)
    b.stage('ink')
    f.dark()
    b.stage('dark')
    f.accents()
    b.fill(neckv, SKIN, pressure=0.6, lanes=0, seed=40)
    cr = cross_mask(b, 540, 1110, 120, w=78, t=20, arm=0.3)
    b.fill(cr, 'mustard', pressure=0.97, slip=0, loose=1, medium='gouache', lanes=0, seed=42)
    b.fill(cr * (XX > 545), '#c8902e', pressure=0.9, slip=0, loose=1, medium='gouache', lanes=0, seed=43)
    cross_ink(b, 540, 1110, 120, w=78, t=20, arm=0.3, width=3.0, seed=44)
    b.stage('accents')
    b.chalk([[(530, 1124), (529, 1200)]], width=5, pressure=0.9, seed=51)
    f.chalk()
    b.speckle((60, 60, 1020, 1860), 'chalk', n=700, size=(0.5, 1.3), seed=52)
    b.stage('chalk')
    finish(b, out, stages)
