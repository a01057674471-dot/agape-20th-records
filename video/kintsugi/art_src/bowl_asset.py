"""The hero chawan, painted once in the blue picture-book style and reused in every shot.

Outputs (in ../art):
  bowl.png       RGBA cut-out of the intact bowl (1080 x 1080 canvas)
  bowl_meta.npz  masks on the same canvas: body (glazed outside), inner (the visible inside), foot, all (union),
                 label (which shard each pixel belongs to, 0 = none), crack (the fracture lines between shards),
                 order (when the gold reaches each crack pixel, 0..1, flowing from the rim along the lines)

The shards are a noisy Voronoi partition of the bowl, so every crack runs from edge to edge and meets the others
like real breaks; the gold is then drawn only on those lines, so it can never leave the bowl.
"""
import os, sys
import numpy as np
from scipy import ndimage as ndi
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'claude-drawing-skill', 'lib'))
from bluebook import BlueBook, INK
from core import blur, smoothstep, noise2d

S = 1080
YY, XX = np.mgrid[0:S, 0:S].astype(np.float32)
CX, RIM_Y, R, HB = 540.0, 330.0, 400.0, 470.0       # centre, rim height, rim half-width, body height
RIM_RY = 74.0
FOOT_R, FOOT_H = 150.0, 58.0


def profile(s):
    """half-width of the body at depth s (0 = rim, 1 = bottom): straight-ish walls that turn into a round base"""
    return R * (1 - 0.22 * s ** 1.6) * np.sqrt(np.clip(1 - np.clip((s - 0.72) / 0.28, 0, 1) ** 2 * 0.62, 0, 1))


def body_pts():
    rng = np.random.default_rng(4)
    ss = np.linspace(0, 1, 40)
    wob = 1 + 0.008 * np.sin(ss * 9 + 1)
    left = [(CX - profile(s) * w, RIM_Y + s * HB) for s, w in zip(ss, wob)]
    right = [(CX + profile(s) * w, RIM_Y + s * HB) for s, w in zip(ss[::-1], wob[::-1])]
    t = np.linspace(0, np.pi, 50)                   # the front lip: lower half of the rim ellipse, slightly uneven
    lip = [(CX + R * np.cos(a), RIM_Y + RIM_RY * np.sin(a) * (1 + 0.04 * np.sin(a * 7))) for a in t]
    return np.array(left + right + lip[1:-1], np.float32)


def main(out_dir):
    b = BlueBook(S, S, seed=777, keep_stages=False)
    b.paper()
    bp = body_pts()
    body = b.poly(bp, smooth=False)
    inner = b.ellipse(CX, RIM_Y, R - 6, RIM_RY - 4)
    foot = b.poly([(CX - FOOT_R, RIM_Y + HB - 14), (CX + FOOT_R, RIM_Y + HB - 14), (CX + FOOT_R * 0.92, RIM_Y + HB + FOOT_H),
                   (CX - FOOT_R * 0.92, RIM_Y + HB + FOOT_H)], smooth=False) * (1 - body)
    allm = np.clip(body + inner + foot, 0, 1)
    # ---- glaze: indigo body, a pale blue glaze that ran down from the rim in drips, deep inside
    b.fill(body, 'cobalt', pressure=0.97, angle=82, mottle=0.16, seed=1)
    b.fill(body * smoothstep(RIM_Y + HB * 0.45, RIM_Y + HB, YY), 'deep', pressure=0.85, angle=82, slip=0, seed=2)
    b.fill(body * smoothstep(CX + 120, CX + R, XX), 'navy', pressure=0.8, angle=82, slip=0, seed=3)
    drip_y = RIM_Y + 70 + 40 * noise2d(S, S, 40, 2, 9)[0:1, :] + 60 * np.maximum(0, np.sin(XX / 37.0)) ** 6
    drip = body * (YY < drip_y)
    b.fill(drip, 'cornflower', pressure=0.95, angle=88, slip=0, loose=1.5, seed=4)
    b.fill(drip * (YY < RIM_Y + 40 + 15 * np.sin(XX / 23.0)), 'powder', pressure=0.9, angle=88, slip=0, seed=5)
    b.fill(inner, 'navy', pressure=0.97, angle=0, slip=0, seed=6)
    b.fill(inner * (YY < RIM_Y - 18), 'deep', pressure=0.85, angle=0, slip=0, seed=7)
    b.fill(foot, '#d6bd96', pressure=0.95, angle=0, slip=0, seed=8)                 # unglazed clay foot
    b.fill(foot * smoothstep(CX + 40, CX + FOOT_R, XX), '#b89a74', pressure=0.85, angle=0, slip=0, seed=9)
    # ---- ink: loose outline, lip, foot ring
    b.outline(bp[:80], 5.0, closed=False, smooth=True, open_=0.3, seed=11)
    b.outline(np.stack([CX + R * np.cos(np.linspace(0, 2 * np.pi, 80)), RIM_Y + RIM_RY * np.sin(np.linspace(0, 2 * np.pi, 80))], 1),
              4.4, open_=0.3, seed=12)
    b.outline([(CX - FOOT_R, RIM_Y + HB - 6), (CX - FOOT_R * 0.92, RIM_Y + HB + FOOT_H), (CX + FOOT_R * 0.92, RIM_Y + HB + FOOT_H),
               (CX + FOOT_R, RIM_Y + HB - 6)], 3.8, closed=False, smooth=False, seed=13)
    # ---- whites: glints on the glaze, lip highlight, speckles in the glaze
    b.chalk([[(CX - R * 0.78, RIM_Y + 90), (CX - R * 0.7, RIM_Y + 300)], [(CX - R * 0.6, RIM_Y + 120), (CX - R * 0.55, RIM_Y + 220)]],
            width=12, pressure=0.6, seed=21)
    t = np.linspace(np.pi * 0.62, np.pi * 0.95, 20)
    b.chalk([np.stack([CX + R * np.cos(t), RIM_Y + RIM_RY * np.sin(t) + 2], 1)], width=6, pressure=0.8, seed=22)
    b.speckle((CX - R, RIM_Y, CX + R, RIM_Y + HB), 'chalk', n=500, size=(0.6, 1.8), seed=23)
    b.speckle((CX - R, RIM_Y, CX + R, RIM_Y + HB), 'powder', n=300, size=(0.8, 2.2), seed=24)
    b.printed(0.8)
    rgb = np.asarray(b.composite(), np.float32) / 255
    # alpha: the bowl, plus the ink just outside its edge (but never the paper)
    ext = ndi.binary_dilation(allm > 0.5, iterations=6)
    dark = rgb.mean(-1) < 0.82
    alpha = np.clip(blur(allm, 0.8) + (ext & dark & (allm < 0.5)) * 1.0, 0, 1)
    rgba = np.dstack([rgb, alpha])
    from PIL import Image
    Image.fromarray((rgba * 255).astype(np.uint8), 'RGBA').save(os.path.join(out_dir, 'bowl.png'))

    # ---- the shards: noisy Voronoi over the glazed body + the visible inside
    region = (np.clip(body + inner, 0, 1) > 0.5)
    seeds = np.array([(CX - 230, RIM_Y + 160), (CX + 40, RIM_Y + 90), (CX + 260, RIM_Y + 220), (CX - 90, RIM_Y + 340),
                      (CX + 170, RIM_Y + 400), (CX - 300, RIM_Y + 380), (CX + 330, RIM_Y - 20)], np.float32)
    n1 = noise2d(S, S, 90, 3, 31) - 0.5; n2 = noise2d(S, S, 90, 3, 32) - 0.5
    n3 = noise2d(S, S, 18, 2, 33) - 0.5; n4 = noise2d(S, S, 18, 2, 34) - 0.5
    WX, WY = XX + 90 * n1 + 14 * n3, YY + 90 * n2 + 14 * n4              # warp -> jagged, natural breaks
    d = np.stack([(WX - sx) ** 2 + (WY - sy) ** 2 for sx, sy in seeds])
    label = (np.argmin(d, 0) + 1) * region
    edge = np.zeros_like(region)
    for dy, dx in ((0, 1), (1, 0)):
        sh = np.roll(np.roll(label, dy, 0), dx, 1)
        edge |= (label != sh) & (label > 0) & (sh > 0)
    crack = ndi.binary_dilation(edge, iterations=1) & region
    lab, n = ndi.label(crack, structure=np.ones((3, 3), bool))            # drop stray little islands
    sizes = ndi.sum(crack, lab, range(1, n + 1))
    crack = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz >= 400])
    # ---- when the gold arrives at each crack pixel: geodesic distance along the cracks from where they meet the rim
    ys, xs = np.nonzero(crack)
    start = np.zeros_like(crack)
    near_rim = crack & (np.abs((XX - CX) ** 2 / R ** 2 + (YY - RIM_Y) ** 2 / RIM_RY ** 2 - 1) < 0.08) & (YY >= RIM_Y)
    start |= near_rim
    if not start.any():
        start[ys[np.argmin(ys)], xs[np.argmin(ys)]] = True
    order = np.full(crack.shape, np.inf, np.float32)
    reached = start.copy(); order[reached] = 0
    k = 0
    while True:
        k += 1
        nxt = ndi.binary_dilation(reached, structure=np.ones((3, 3), bool)) & crack & ~reached
        if not nxt.any(): break
        order[nxt] = k; reached |= nxt
    left = crack & ~reached                                  # pieces not connected to the rim start late
    order[left] = k * 0.55                                   # (the inside wall: gilded halfway through)
    order[np.isinf(order)] = 0
    order = order / max(order.max(), 1)
    idx = ndi.distance_transform_edt(label == 0, return_distances=False, return_indices=True)
    shard = label[idx[0], idx[1]] * (alpha > 0.01)
    np.savez_compressed(os.path.join(out_dir, 'bowl_meta.npz'), shard=shard.astype(np.uint8), body=body.astype(np.float32), inner=inner.astype(np.float32),
                        foot=foot.astype(np.float32), all=allm.astype(np.float32), label=label.astype(np.uint8),
                        crack=crack, order=order.astype(np.float32))
    print('shards', len(np.unique(label)) - 1, 'crack px', crack.sum(), 'flow steps', k)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'art'))
