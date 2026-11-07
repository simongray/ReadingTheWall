"""Close-up drawings: shoes on footholds and small edges."""

import math

from climb import *
import hand as H


def edge_side(fig, top=(0, 0), depth=1.6, height=2.2, z=-5, wall_x=None):
    """A small edge in profile sticking out of a wall to the right."""
    x, y = top
    wx = x + depth if wall_x is None else wall_x
    pts = [(wx, y - height), (x + 0.3, y - height * 0.75), (x, y - 0.25),
           (x + 0.2, y), (wx, y + 0.05)]
    fig.poly(pts, z=z, fill=DARK, stroke=INK, sw=0.35)
    H.xray_outline(fig, pts)


def wall_strip(fig, x, y0, y1, z=-10):
    fig.poly([(x, y0), (x, y1), (x + 1.4, y1), (x + 1.4, y0)], z=z, fill=PALE,
             stroke=None)
    fig.line((x, y0), (x, y1), z=z + 1, sw=0.6)
    y = y0
    while y < y1:
        fig.line((x, y), (x + 1.4, y + 1.0), z=z + 1, sw=0.18, stroke=MID)
        y += 0.9


# ---------------------------------------------------------------- shoes from above

# Shoe coordinates in cm: heel at (0, 0), toe along +x, big-toe side at +y. A
# shoe about 25 x 8.8 cm on an asymmetric last. Its longest point sits over the
# big toe, the big-toe side runs almost straight up to that point and the
# little-toe side sweeps back from it along the line of the toes. The waist is
# hollow on the big-toe side but about as wide as the heel, since the foot fills
# it, and the heel has a rim of rubber round the leg.
SHOE_TOP = [(0, 0.1), (0.55, 2.0), (2.2, 3.1), (5, 3.3), (8, 2.8), (10.5, 2.7),
            (13, 3.0), (15.8, 3.6), (18.5, 3.95), (21, 3.85), (23.3, 3.5),
            (24.65, 2.85), (25, 2.0), (24.8, 1.1), (23.9, -0.2), (22.6, -1.9),
            (20.9, -3.4), (18.6, -4.5), (15.9, -4.85), (13, -4.5), (10.5, -3.95),
            (8, -3.55), (5, -3.3), (2.2, -3.0), (0.55, -1.9)]
SHOE_TOP_TIP = (25, 2.0)
SHOE_TOP_BIG_TOE = (22.2, 1.9)      # the pad of the big toe: a pivot's fulcrum

# The upper, which leaves the rubber showing: a narrow rand along both sides,
# a heel cup and a toe cap whose back edge follows the toe joints, so it reaches
# further back on the little-toe side.
SHOE_TOP_UPPER = [(19.6, 3.15), (16, 2.85), (13, 2.3), (10.5, 2.0), (8, 2.1),
                  (5, 2.65), (2.7, 2.35), (1.7, 1.1), (1.5, 0), (1.7, -1.1),
                  (2.7, -2.2), (5, -2.65), (8, -2.85), (10.5, -3.25), (13, -3.8),
                  (15.4, -4.1), (17.2, -3.1), (18.5, -1.5), (19.7, 0.2), (20.2, 1.7)]
# dark enough for a ghost's dashes to show on it, and not DARK, which paint.py colours
SHOE_TOP_UPPER_FILL = "#666666"
# two straps across the instep, slanting back to the little-toe side, whose
# ends fold back on that side
SHOE_TOP_STRAPS = [((9.2, 2.45), (11.3, 2.45), (10.3, -3.7), (8.2, -3.55)),
                   ((12.3, 2.6), (14.4, 3.05), (13.4, -4.45), (11.3, -4.15))]
# a heel loop, in the upper's grey so that the heel keeps its outline
SHOE_TOP_LOOP = [(-0.3, -0.8), (-0.3, 0.8), (2.2, 0.8), (2.2, -0.8)]
# the leg end-on, in the collar over the heel, 6.2 x 5.3 cm: about as thick as the
# leg in the side views
SHOE_TOP_LEG = [(4.9 + 3.1 * math.cos(i * math.pi / 8), 2.65 * math.sin(i * math.pi / 8))
                for i in range(16)]


def shoe_top(fig, heel, deg, medial=+1, z=0, ghost=None):
    """A shoe seen from above, heel at `heel` and pointing at `deg`. `medial` +1
    puts the big-toe side to the left of the heel-to-toe direction, which makes
    it a right shoe, and -1 makes it a left shoe. `ghost` is a style for showing
    an earlier position: only the outline and the leg, drawn in that style.
    Returns a function mapping shoe coordinates to world points."""
    d = ang(deg)
    n = perp(d)

    def P(x, y):
        return add(heel, add(mul(d, x), mul(n, y * medial)))

    def ps(q):
        return [P(*p) for p in q]

    if ghost:
        fig.smooth(ps(SHOE_TOP), z=z, tension=0.7, **ghost)
        fig.smooth(ps(SHOE_TOP_LEG), z=z + 0.01, tension=0.8, **ghost)
        return P
    fig.smooth(ps(SHOE_TOP), z=z, fill=SHOE_FILL, stroke=INK, sw=0.35, tension=0.7)
    fig.smooth(ps(SHOE_TOP_UPPER), z=z + 0.01, fill=SHOE_TOP_UPPER_FILL, stroke=None,
               tension=0.8)
    for a, b, c, e in SHOE_TOP_STRAPS:
        fig.poly(ps((a, b, c, e)), z=z + 0.02, fill=LIGHT, stroke=INK, sw=0.22)
        fig.line(P(*lerp(a, e, 0.62)), P(*lerp(b, c, 0.62)), z=z + 0.03, sw=0.2)
    fig.poly(ps(SHOE_TOP_LOOP), z=z + 0.02, fill=SHOE_TOP_UPPER_FILL, stroke=INK, sw=0.2)
    # left limbs are grey and right limbs white, as on the climbers
    fig.smooth(ps(SHOE_TOP_LEG), z=z + 0.04, fill=WHITE if medial > 0 else LEFT,
               stroke=INK, sw=0.4, tension=0.8)
    return P


def foot_edges_figure(path):
    panels = []
    for kind in ("inside", "outside", "toe"):
        f = Fig(-15, -27 if kind == "toe" else -17, 15, 6, scale=1.6)
        # the wall along the top, a foothold sticking out of it
        f.poly([(-15, 3.5), (15, 3.5), (15, 6), (-15, 6)], z=-10, fill=PALE,
               stroke=None)
        f.line((-15, 3.5), (15, 3.5), z=-9, sw=0.6)
        x = -15
        while x < 15:
            f.line((x, 3.5), (x + 1.4, 6), z=-9, sw=0.18, stroke=MID)
            x += 1.2
        hold = [(-8, 3.5), (8, 3.5), (7.4, 0.8), (-7.4, 0.8)]
        f.poly(hold, z=-5, fill=DARK, stroke=INK, sw=0.35)
        H.xray_outline(f, hold)
        if kind == "inside":
            # right foot turned out: big-toe side on the hold
            shoe_top(f, (-13.5, -3.6), 4, medial=+1)
            f.label("big-toe side", (-2, -12.5), to=(3, 0.9), size=7)
        elif kind == "outside":
            # right foot turned in: little-toe side on the hold
            shoe_top(f, (13.5, -3.4), 176, medial=+1)
            f.label("little-toe side", (2, -12.5), to=(-3, 1.8), size=7)
        else:
            shoe_top(f, (-1.6, -24), 90, medial=+1)
            f.label("big-toe tip", (-14.3, -5), to=(-3.2, 0.2), size=7, anchor="start")
        panels.append(f)
    combine(panels, path, gap=4, captions=["inside edge", "outside edge",
                                           "toe (front-pointing)"])


# Helpers only: figs_feet uses shoe_top and edge_side. The figure function
# above is kept as an example but is not part of the book.
