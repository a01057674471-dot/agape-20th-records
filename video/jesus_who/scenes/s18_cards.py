"""plain painted grounds for the typographic cards"""
from common import *

def main(out, stages=None):
    for i, (top, bot) in enumerate((('#ffd88a', '#fff0d0'), ('#bfe2d8', '#eef6ea'), ('#f6c8b0', '#fbe8d8'))):
        g, p = canvas(1800 + i, tone='#f0b070')
        g.scumble_background(top, bottom=bot, seed=20 + i, angle=-30, dark=0.04, light=0.14)
        for k in range(5):
            x, y = 120 + k * 210, 1780 - (k % 2) * 40
            for a in range(5): g.dab(x + 10 * np.cos(a * 1.26), y + 10 * np.sin(a * 1.26), 8, ['#f26a5a', '#ffffff', '#f2c04a'][k % 3])
            g.dab(x, y, 5, '#f8c030')
        finish(g, out.replace('.jpg', f'_{i}.jpg'))
