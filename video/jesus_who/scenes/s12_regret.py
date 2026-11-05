"""⑤ today: a young man sits on the edge of his bed in a soft morning room, phone in his hands, head down -- he said
something that hurt a friend. A cracked mug on the floor. Muted, but not dark."""
from common import *

def main(out, stages=None):
    g, p = canvas(1212, tone='#c8a888', stages=stages)
    man = Person(g, 520, 900, 140, skin=SKIN_JP, hair='side', hair_col=HAIR_BLACK, body='shirt', cloth='#6a8ab0',
                 look=(0.0, 0.9), eyes_closed=True, mouth='sad', brows=-1.0, blush=0.1, seed=1,
                 arms=[[(410, 1080), (400, 1240), (500, 1300)], [(630, 1080), (650, 1240), (560, 1300)]], torso=(1360, 210),
                 legs=[[(460, 1360), (420, 1560), (420, 1700)], [(590, 1360), (630, 1560), (640, 1700)]], trousers='#4a4a5a', shoes='#e8e4dc')
    wall = (p.YY < 1250).astype(np.float32)
    g.block_in(wall * (1 - man.fig), '#cdd8e0', angle=0, length=(60, 120), width=(16, 26))
    g.model_form(wall * (1 - man.fig), ramp('#cdd8e0', light=0.15, pale=0.3), steps=3, relief=0.1, height=np.zeros_like(wall), angle=0)
    win = g.poly([(700, 200), (1000, 200), (1000, 700), (700, 700)], smooth=False)
    g.block_in(win, '#e8f2f4', length=(20, 50), width=(8, 14))
    g.line([(850, 200), (850, 700)], 14, '#f8f6f2', 1.0, taper=(0, 0)); g.line([(700, 450), (1000, 450)], 14, '#f8f6f2', 1.0, taper=(0, 0))
    g.glaze(g.poly([(700, 700), (1000, 700), (900, 1400), (500, 1400)]), '#fff8e8', 0.3, mode='screen', soft=30)
    frame = g.poly([(140, 300), (380, 300), (380, 520), (140, 520)], smooth=False)
    g.block_in(frame, '#f2e6d0'); g.block_in(g.poly([(170, 330), (350, 330), (350, 490), (170, 490)], smooth=False), '#a8c8a0')
    bed = g.poly([(0, 1250), (1080, 1250), (1080, 1460), (0, 1460)], smooth=False) * (1 - man.fig)
    g.block_in(bed, '#f2f0ea', angle=0, length=(50, 100), width=(14, 24))
    g.model_form(bed, ['#a8b0c0', '#c4cad6', '#e2e4ea', '#f2f0ea', '#fcfaf6'], steps=3, relief=0.4, angle=0)
    g.glaze(g.band([(0, 1300), (300, 1330), (600, 1300)], 30) * bed, '#9ab0d0', 0.4)
    floor(g, 1460, '#d8c0a0', avoid=man.fig)
    g.stage('room')
    paint_people(g, [man])
    ph = g.poly(rrect(530, 1290, 90, 150, 14), smooth=False)
    g.block_in(ph, '#2a2a32', length=(8, 16), width=(4, 8))
    g.glaze(g.poly(rrect(530, 1290, 72, 128, 10), smooth=False), '#8ab8e0', 0.7, mode='normal')
    hand(g, 480, 1310, 0.7, 10, SKIN_JP, fingers=4, thumb=False); hand(g, 580, 1310, 0.7, 170, SKIN_JP, fingers=4, thumb=False)
    # the cracked mug on the floor
    for (x, y, rx, ry, a) in ((240, 1700, 46, 32, 10), (300, 1730, 30, 20, -30), (200, 1745, 22, 16, 40)):
        sh = g.blob(x, y, rx, ry, 0.15, int(x), a)
        g.block_in(sh, '#f2d860', length=(6, 12), width=(3, 6)); g.model_form(sh, ramp('#f2d860'), steps=3, relief=0.5)
    finish(g, out, stages)
