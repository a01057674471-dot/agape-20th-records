"""⑤ 神の子が、人間として: a close-up portrait of Jesus as a 1st-century Jewish man -- olive-brown skin, dark brown eyes,
dark wavy hair to the jaw, a short beard, a cream tunic and a madder-red mantle, a warm, attentive look."""
from common import *

def main(out, stages=None):
    g, p = canvas(1111, tone='#e8a868', stages=stages)
    j = Person(g, 540, 780, 330, skin=SKIN_OLIVE, hair='curly', hair_col=HAIR_DARK, beard='short', cloth='#efe2c4',
               stripe='#8a5a3a', mantle='#b8643c', look=(0.0, 0.05), mouth='smile', seed=11, torso=(1920, 520))
    g.scumble_background('#e9b86a', bottom='#f6dcae', avoid=j.fig, seed=12, angle=-30)
    g.stage('background')
    paint_people(g, [j])
    finish(g, out, stages)
