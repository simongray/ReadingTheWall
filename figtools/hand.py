"""The frames, walls and holds of the hand close-ups.

The hands themselves are in authored.py. Side profiles have the wall on the right with
its face at x = WX, as in the climber side views.
"""

import math

from climb import INK, MID, PALE, DARK, Fig, XRAY, XRAY_Z, XRAY_STYLE

HAND_SCALE = 2.6        # paper mm per cm, for every hand close-up in the book

LINE = [1.0]            # multiplies the hands' line weights, for a plate that gets reduced
# the greys of the fingers behind the front one, nearest first: one step apart on the
# e-ink panel's 16 greys (#000000, #111111, ... #ffffff), so that each finger reads on its own
BACK_FILLS = ("#dddddd", "#cccccc")
DETAIL = 0.24           # nails

WX = 2.0


def inside(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                c = not c
    return c


def wall_profile(f, x, y0, y1, z=-20):
    """A vertical wall face at x seen from the side, hatched to the right."""
    w = f.mm(2.4)
    f.poly([(x, y0), (x, y1), (x + w, y1), (x + w, y0)], z=z, fill=PALE, stroke=None)
    f.line((x, y0), (x, y1), z=z + 1, sw=0.6)
    y = y0
    while y < y1:
        f.line((x, y), (x + w, y + f.mm(1.5)), z=z + 1, sw=0.18, stroke=MID)
        y += f.mm(1.9)


def profile_frame(x0=-10.0, y0=-9.0, y1=7.5, scale=HAND_SCALE):
    """A close-up frame with the wall face at x = WX, cropped at the back of
    the wall's hatched strip."""
    f = Fig(x0, y0, WX + 2.4 / scale + 0.01, y1, scale=scale)
    wall_profile(f, WX, y0, y1)
    return f


def xray_outline(f, pts, tension=None):
    """The outline of a hold through `pts`, which shows dotted where a hand
    or shoe covers it (see XRAY): smooth with `tension`, else straight."""
    if not XRAY:
        return
    if tension is None:
        f.poly(pts, z=XRAY_Z, **XRAY_STYLE)
    else:
        f.smooth(pts, z=XRAY_Z, tension=tension, **XRAY_STYLE)


def edge_pts(wx, top, depth=2.0, height=2.6, slope=0.0, round_r=0.35):
    """The points edge_profile draws its edge through."""
    t = math.tan(math.radians(slope))
    front_top = (wx - depth, top - depth * t)
    return [(wx, top + 0.05), front_top,
            (wx - depth - round_r * 0.4, front_top[1] - round_r),
            (wx - depth * 0.85, top - height * 0.75), (wx, top - height)]


def edge_profile(f, wx, top, depth=2.0, height=2.6, slope=0.0, round_r=0.35, z=-5):
    """An edge sticking out of a wall face at x=wx, seen from the side.
    `slope` tilts the top (degrees): positive slopes down and away from the
    wall, negative is incut. Returns the front corner of the top."""
    pts = edge_pts(wx, top, depth, height, slope, round_r)
    f.smooth(pts, z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.35)
    xray_outline(f, pts, 0.35)
    return pts[1]


def lip_pts(wx, top, depth=2.6, height=4.0):
    """The points rounded_lip draws its edge through."""
    return [(wx, top + 0.05), (wx - depth * 0.45, top), (wx - depth * 0.85, top - 0.35),
            (wx - depth, top - 1.2), (wx - depth * 0.92, top - 2.2),
            (wx - depth * 0.55, top - height * 0.8), (wx, top - height)]


def rounded_lip(f, wx, top, depth=2.6, height=4.0, z=-5):
    """A rounded edge (the front corner is a large radius)."""
    pts = lip_pts(wx, top, depth, height)
    f.smooth(pts, z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.8)
    xray_outline(f, pts, 0.8)


# the holds of the profile grips, on a wall at x = WX with their tops at y = 0
GRIP_HOLD = {"open": (rounded_lip, dict(depth=2.6, height=4.2)),
             "half": (edge_profile, dict(depth=2.0, height=2.6)),
             "full": (edge_profile, dict(depth=0.8, height=2.0, slope=-12))}


def grip_hold(fig, kind):
    """The hold for a profile grip on a wall at x = WX, its top at y = 0: a
    rounded edge ('open'), a flat edge ('half') or a small incut edge."""
    draw, kw = GRIP_HOLD[kind]
    draw(fig, WX, 0, **kw)
