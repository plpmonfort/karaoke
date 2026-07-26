# -*- coding: utf-8 -*-
"""
Generates the app icons used when you add Karaoke Night to a phone home screen.

    python3 make_icons.py

Writes into icons/. You only need to run this again if you want to restyle the
icon -- the generated PNGs are committed to the repo.
"""

import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "icons")
SS = 4  # supersample factor, for smooth edges

BG_CORE = (255, 46, 154)    # --pink
BG_MID = (98, 40, 160)
BG_EDGE = (18, 8, 38)       # near --ink
MIC = (255, 255, 255)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def background(size):
    """Radial glow: hot pink core falling off to deep purple at the corners."""
    img = Image.new("RGB", (size, size), BG_EDGE)
    px = img.load()
    cx, cy = size * 0.5, size * 0.36
    maxd = math.hypot(size, size) * 0.62
    for y in range(size):
        for x in range(size):
            d = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            px[x, y] = lerp(BG_CORE, BG_MID, d ** 0.85) if d < 0.55 \
                else lerp(BG_MID, BG_EDGE, (d - 0.55) / 0.45)
    return img


def draw_mic(d, size, scale=1.0, cy_shift=0.0):
    """A microphone, drawn in unit coordinates scaled to `size`."""
    def X(u):
        return (0.5 + (u - 0.5) * scale) * size

    def Y(u):
        return (0.5 + (u - 0.5 + cy_shift) * scale) * size

    # capsule head
    d.rounded_rectangle([X(0.385), Y(0.175), X(0.615), Y(0.575)],
                        radius=(0.115 * scale * size), fill=MIC)

    # grille lines, knocked out of the capsule
    for u in (0.28, 0.36, 0.44):
        d.rounded_rectangle([X(0.435), Y(u), X(0.565), Y(u + 0.022)],
                            radius=(0.012 * scale * size), fill=BG_CORE)

    # U-shaped bracket under the head
    w = 0.052 * scale * size
    d.arc([X(0.285), Y(0.34), X(0.715), Y(0.735)],
          start=0, end=180, fill=MIC, width=int(round(w)))

    # stem + base
    d.rectangle([X(0.4785), Y(0.70), X(0.5215), Y(0.80)], fill=MIC)
    d.rounded_rectangle([X(0.375), Y(0.792), X(0.625), Y(0.835)],
                        radius=(0.022 * scale * size), fill=MIC)


def build(size, scale=1.0, cy_shift=0.0):
    s = size * SS
    img = background(s)
    d = ImageDraw.Draw(img)
    draw_mic(d, s, scale, cy_shift)
    return img.resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [
        ("icon-192.png", 192, 1.0, 0.0),
        ("icon-512.png", 512, 1.0, 0.0),
        ("apple-touch-icon.png", 180, 1.0, 0.0),
        # Maskable: content pulled into the 80% safe zone so Android can crop it
        # to a circle without clipping the microphone.
        ("icon-maskable-512.png", 512, 0.66, 0.01),
        ("favicon-32.png", 32, 1.0, 0.0),
    ]
    for name, size, scale, shift in jobs:
        build(size, scale, shift).save(os.path.join(OUT, name), optimize=True)
        print(f"  icons/{name}  ({size}x{size})")
    print(f"\nWrote {len(jobs)} icons.")


if __name__ == "__main__":
    main()
