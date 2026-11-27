#!/usr/bin/env python3
"""
Solve for a three-colour palette that hits the style's value structure.

    python palette.py --ground-hue 150 --accent-hue 168 --void-hue 18

Targets (measured from the reference): ground luma 197 @ 46% sat,
accent 77 @ 73%, void 38 @ 41%.

Sanity-check the result against references/palette.md before using it. The two
things that matter most: the accent is nearly locked to red (only red sits at
full chroma AND at luma 77), and the void must OPPOSE the accent in hue or the
accent floods the frame.
"""
import argparse, colorsys

T = {'ground': (197, 0.46), 'accent': (77, 0.73), 'void': (38, 0.41)}


def solve(hue_deg, sat, target_luma):
    best = None
    for i in range(1001):
        l = i / 1000
        r, g, b = colorsys.hls_to_rgb(hue_deg / 360, l, sat)
        R, G, B = (int(round(v * 255)) for v in (r, g, b))
        lum = 0.299 * R + 0.587 * G + 0.114 * B
        d = abs(lum - target_luma)
        if best is None or d < best[0]:
            best = (d, f"#{R:02X}{G:02X}{B:02X}", lum)
    return best[1], best[2]




def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ground-hue', type=float, required=True)
    p.add_argument('--accent-hue', type=float, required=True)
    p.add_argument('--void-hue', type=float, required=True)
    a = p.parse_args()
    hues = {'ground': a.ground_hue, 'accent': a.accent_hue, 'void': a.void_hue}

    for role in ('ground', 'accent', 'void'):
        lum, sat = T[role]
        hx, got = solve(hues[role], sat, lum)
        print(f"{role:7} {hx}   luma {got:5.1f} (target {lum})   hue {hues[role]:g}deg")

    def sep(x, y):
        d = abs(x - y) % 360
        return min(d, 360 - d)

    ga = sep(hues['ground'], hues['accent'])
    va = sep(hues['void'], hues['accent'])
    print(f"\nground/accent {ga:.0f}deg apart   (reference 23 — same family, reads as one material)")
    print(f"void/accent   {va:.0f}deg apart   (reference 148 — opposition; this is what restrains the accent)")
    if va < 90:
        print("\nWARNING: void sits close to the accent in hue. In testing, weakening this")
        print("opposition let the accent flood to 50% and collapsed the ground to 33%.")
    if 60 < hues['accent'] < 300:
        print("\nWARNING: accent hue is outside the red/violet region. Only red (luma 76) and")
        print("violet (67) sit at the accent value at full chroma. Others turn to mud there.")


if __name__ == '__main__':
    main()
