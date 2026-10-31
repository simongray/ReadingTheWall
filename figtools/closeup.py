"""Close-up drawings: shoes on footholds, small edges, and the crimp
comparison. Hands come from hand.py, the one hand model every close-up in
the book uses."""

from climb import *
import hand as H


def edge_side(fig, top=(0, 0), depth=1.6, height=2.2, z=-5, wall_x=None):
    """A small edge in profile sticking out of a wall to the right."""
    x, y = top
    wx = x + depth if wall_x is None else wall_x
    pts = [(wx, y - height), (x + 0.3, y - height * 0.75), (x, y - 0.25),
           (x + 0.2, y), (wx, y + 0.05)]
    fig.poly(pts, z=z, fill=DARK, stroke=INK, sw=0.35)


def wall_strip(fig, x, y0, y1, z=-10):
    fig.poly([(x, y0), (x, y1), (x + 1.4, y1), (x + 1.4, y0)], z=z, fill=PALE,
             stroke=None)
    fig.line((x, y0), (x, y1), z=z + 1, sw=0.6)
    y = y0
    while y < y1:
        fig.line((x, y), (x + 1.4, y + 1.0), z=z + 1, sw=0.18, stroke=MID)
        y += 0.9


def crimp_figure(path):
    """Open hand, half crimp and full crimp side by side, middle joint
    angles marked."""
    panels = []
    for kind, lab in (("open", "≈40°"), ("half", "≈90°"), ("full", "over 90°")):
        f, p = H.grip_profile(kind, x0=-12.0, y0=-8.5, y1=8.6)
        j = p.joint("i", "pip")
        H.joint_arc(f, p, "i", "pip", 1.5, lab, at=add(j, (-2.6, 2.4)), ext=2.2)
        panels.append(f)
    combine(panels, path, gap=3, captions=["open hand", "half crimp", "full crimp"])


# ---------------------------------------------------------------- shoes from above

# heel at (0, 0), toe along +x, big-toe side at +y: about 25 x 8.6 cm, a
# narrow heel, the widest point at the ball and an asymmetric toe that
# points toward the big toe
SHOE_TOP = [(0, 0), (0.6, 2.2), (2.5, 3.0), (6, 3.2), (10, 3.5), (14.5, 4.1),
            (18.5, 4.2), (22, 3.6), (24.3, 2.4), (25, 1.3), (24.6, -0.4),
            (23.3, -2.2), (21, -3.6), (18, -4.4), (14, -4.3), (10, -3.5),
            (6, -3.1), (2.5, -2.8), (0.6, -2.0)]
SHOE_TOP_TIP = (25, 1.3)


def shoe_top(fig, heel, deg, medial=+1, z=0, contact=None):
    """A right-or-left shoe seen from above. `medial` +1 puts the big-toe
    side to the left of the heel-to-toe direction."""
    d = ang(deg)
    n = perp(d)
    pts = [add(heel, add(mul(d, x), mul(n, y * medial))) for x, y in SHOE_TOP]
    fig.smooth(pts, z=z, fill="#5a5a5a", stroke=INK, sw=0.35, tension=0.7)
    # black rubber toe rand
    rand = [p for p in SHOE_TOP if p[0] >= 17.5]
    cut = [(17.5, -3.2), (17.5, 4.05)]
    rp = [add(heel, add(mul(d, x), mul(n, y * medial))) for x, y in
          [cut[1]] + rand + [cut[0]]]
    fig.smooth(rp, z=z + 0.05, fill=INK, stroke=INK, sw=0.3, tension=0.7)
    # heel rand
    hp = [add(heel, add(mul(d, x), mul(n, y * medial))) for x, y in
          [(4.2, 3.0), (0.8, 2.3), (0, 0), (0.8, -1.9), (4.2, -2.6)]]
    fig.smooth(hp, closed=False, z=z + 0.05, stroke=INK, sw=0.9, tension=0.7)
    # velcro straps
    for xs in (8.0, 11.5):
        s0 = add(heel, add(mul(d, xs), mul(n, 3.5 * medial)))
        s1 = add(heel, add(mul(d, xs + 0.6), mul(n, -2.9 * medial)))
        fig.line(s0, s1, z=z + 0.1, sw=0.8, stroke=WHITE)
    return pts


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
        f.poly([(-8, 3.5), (8, 3.5), (7.4, 0.8), (-7.4, 0.8)], z=-5, fill=DARK,
               stroke=INK, sw=0.35)
        if kind == "inside":
            # right foot turned out: big-toe side on the hold
            shoe_top(f, (-13.5, -3.6), 4, medial=+1)
            f.label("big-toe side", (-2, -12.5), to=(3, -0.4), size=7)
        elif kind == "outside":
            # right foot turned in: little-toe side on the hold
            shoe_top(f, (13.5, -3.4), 176, medial=+1)
            f.label("little-toe side", (2, -12.5), to=(-3, -0.5), size=7)
        else:
            shoe_top(f, (-1.6, -24), 90, medial=+1)
            f.label("big-toe tip", (-7, -5), to=(-0.4, 0.4), size=7)
        panels.append(f)
    combine(panels, path, gap=4, captions=["inside edge", "outside edge",
                                           "toe (front-pointing)"])


# Helpers only: figs_feet uses shoe_top and edge_side. The two figure
# functions above are kept as examples but are not part of the book.
