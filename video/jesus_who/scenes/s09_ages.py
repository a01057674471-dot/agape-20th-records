"""④ each one precious: three stacked portraits on one board -- a mother holding her baby, a grandfather, a laughing kid."""
from common import *

def main(out, stages=None):
    g = GouachePortrait(W, H, seed=909, keep_stages=bool(stages), stages_dir=stages)
    ps = [g.panel(24, 24 + i * 632, 1032, 608) for i in range(3)]
    g.ground('#e8a868', alpha=0.4)
    # 1 mother and baby
    g.use(ps[0])
    mom = Person(g, 430, 250, 150, skin=SKIN_JP, hair='bun', hair_col=HAIR_BLACK, body='shirt', cloth='#e88a6a',
                 look=(0.5, 0.6), mouth='smile', turn=0.4, seed=1, arms=[[(330, 430), (360, 540), (560, 560)]], torso=(700, 240))
    baby = Person(g, 640, 440, 78, skin=SKIN_LIGHT, hair='bald', hair_col=HAIR_DARK, body='shirt', cloth='#fff2d0',
                  look=(-0.4, -0.6), mouth='open', seed=2, torso=(640, 110), blush=0.7)
    g.scumble_background('#f4c8b0', bottom='#f8e0c8', avoid=np.maximum(mom.fig, baby.fig), seed=11)
    paint_people(g, [mom, baby])
    # 2 grandfather
    g.use(ps[1])
    gpa = Person(g, 520, 270, 165, skin=SKIN_JP, hair='bald', hair_col=HAIR_GREY, beard=None, body='shirt', cloth='#5a7a9a',
                 look=(-0.2, 0.1), mouth='smile', age=80, eyes_closed=True, seed=3, torso=(720, 260))
    g.scumble_background('#a8d0c0', bottom='#d8ecd8', avoid=gpa.fig, seed=12)
    paint_people(g, [gpa])
    for sgn in (-1, 1):                                 # round glasses
        th = np.linspace(0, 2 * np.pi, 40)
        g.line(np.stack([520 + sgn * 60 + 44 * np.cos(th), 285 + 40 * np.sin(th)], 1), 4, '#5a4030', 0.9, taper=(0, 0))
    g.line([(500, 285), (540, 285)], 4, '#5a4030', 0.9)
    # 3 laughing kid
    g.use(ps[2])
    kid = Person(g, 520, 280, 160, skin=SKIN_DEEP, hair='curly', hair_col=HAIR_BLACK, body='shirt', cloth='#f2c040',
                 look=(0.2, -0.1), mouth='open', brows=1.0, seed=4, torso=(720, 250), blush=0.6)
    g.scumble_background('#b8c8f0', bottom='#e8e0f4', avoid=kid.fig, seed=13)
    paint_people(g, [kid])
    finish(g, out, stages)
