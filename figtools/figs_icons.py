"""The icons of a technique entry's asides.

The asides that recur in technique entries each have a small icon beside
their label, drawn with the figures' own code so that it belongs to the
book's drawings as the hold ornaments do (figs_cover.py):

- tall: the "Tall climbers" note. The mannequin standing, with a height
  mark beside it: a dimension line, as the figures measure a distance.
- small: the "Small climbers" note. A shorter mannequin with a shorter
  height mark, stretching up to a jug out of its reach.
- reading: the "When to use it — reading the wall" box. The mannequin's
  head looking up at a hold along a dotted line of sight, as the figures
  draw a look: reading the wall is looking for the holds that call for
  the technique.
- mistakes: the "Common mistakes" list. A climbing shoe skating off a
  foothold, with the cross that marks the wrong way in the figures and
  that marks each item of the list.

Every icon is drawn at the height it is set at (ICON_H), with its drawing
centred in it, and is as wide as its drawing, like the ornaments. The
helper that sets them is `aside-icon` in book/template.typ.

The mannequin is drawn at K times the icon's scale and set down at the
icon's size, with its line weights multiplied by K, so that its lines keep
the pen's weights. Drawn directly at a few centimetres to the millimetre,
the pen would thin a head to a few points and its wobble would bend it out
of shape. At that size only its silhouette reads: the figure is drawn as
one outlined shape, without its inner lines or its ears.
"""

from climb import *          # noqa: F401,F403
from climb import _draw_group

ICON_H = 7.0       # mm: the height every icon is drawn and set at
ICON_W = 8.0       # mm: the widest an icon may be, to hang in the margin
ICON_PAD = 0.45    # mm of paper left and right of the drawing
ICON_VPAD = 0.3    # mm of paper the drawing needs above and below
FIG_SW = 0.22      # the mannequin's line weight (mm), as _draw_group takes it
K = 10             # the mannequin is drawn this many times larger


# ---------------------------------------------------------------- helpers


def _enlarged(f):
    """A Fig on the same world frame as f, K times larger on paper. SVG
    units are world units in both, so its drawing can be added to f."""
    return Fig(f.x0, f.y0, f.x1, f.y1, f.scale * K)


def _merge(f, g):
    for z, _, svg in g.items:
        f.add(svg, z)


def _mannequin(f, pieces, lines=(), shoes=()):
    """Draw the mannequin's pieces as one outlined shape (_draw_group), and
    its inner lines, enlarged (see the module's docstring). shoes: outlines
    of shoes, drawn black under the shape."""
    g = _enlarged(f)
    for pts in shoes:
        g.smooth(pts, z=-1, tension=0.7, fill=INK, stroke=INK, sw=FIG_SW * K)
    lines = [dict(ln, sw=ln.get("sw", LINE_SW) * K) for ln in lines]
    _draw_group(g, 0, pieces, lines, dict(stroke=INK, sw=FIG_SW * K))
    _merge(f, g)


def _shoe_outline(c, s):
    """The outline Climber._shoe() draws for the shoe of leg s."""
    ft = getattr(c, "_" + s + "f")
    if ft["style"] == "back":
        origin = sub(c.J[s + "an"], (0, 8 * c.s))
        return [add(origin, (x * c.s, y * c.s)) for x, y in SHOE_BACK]
    d, n = ft["d"], ft["n"]
    base = sub(c.J[s + "an"], add(mul(d, SHOE_ANKLE[0] * c.s),
                                  mul(n, SHOE_ANKLE[1] * c.s)))
    return [add(base, add(mul(d, x * c.s), mul(n, y * c.s))) for x, y in SHOE]


COL = dict(l=LEFT, r=WHITE, shirt=WHITE, hair=HAIR)


def _points(pieces):
    return [p for pc in pieces for p in pc["pts"]]


# ---------------------------------------------------------------- the icons


def _standing(f, c):
    """Draw climber c as one shape and return its points and its head's."""
    geo = c._geometry(COL, False)
    pieces = []
    for name in ("lleg", "rleg", "torso", "head", "larm", "rarm"):
        ps = geo[name][0]
        if name == "head":
            ps = [ps[0], ps[-1]]          # skull and hair, without the ears
        pieces += ps
    shoes = [_shoe_outline(c, s) for s in "lr"]
    _mannequin(f, pieces, shoes=shoes)
    return _points(pieces) + [p for s in shoes for p in s], _points(geo["head"][0])


def _height_mark(f, pts, top):
    """The dimension line from the floor to `top`, beside the points pts,
    and the floor under them. Returns the points of its left end."""
    bot = min(p[1] for p in pts)
    x = min(p[0] for p in pts) - f.mm(1.1)
    t = f.mm(0.6)
    f.line((x - t, top), (x + t, top), sw=0.3)
    f.line((x - t, bot), (max(p[0] for p in pts) + t, bot), sw=0.3)
    mid = (top + bot) / 2
    for end in (top, bot):
        f.arrow([(x, mid), (x, end)], kind="path", head=0.9)
    return [(x - t, top), (x - t, bot)]


def tall(f):
    """The mannequin standing, seen from behind like the climbers in the
    figures, with a dimension line from the floor to the top of its head."""
    c = Climber((0, 96), view="back", xray=False,
                lh=(-34, 64), rh=(34, 64), elbows={"l": "down", "r": "down"},
                lf={"at": (-10, 0), "style": "back"},
                rf={"at": (10, 0), "style": "back"})
    pts, _ = _standing(f, c)
    return pts + _height_mark(f, pts, max(p[1] for p in pts))


def small(f):
    """The same mannequin about two thirds the height, with its height mark
    just as tall as it is. One arm stretches up to a jug out of its reach."""
    s = 0.68
    hand = (22 * s, 198 * s)
    c = Climber((0, 96 * s), view="back", xray=False, scale=s,
                lh=(-34 * s, 64 * s), rh=hand,
                elbows={"l": "down", "r": "out"},
                lf={"at": (-10 * s, 0), "style": "back"},
                rf={"at": (10 * s, 0), "style": "back"})
    pts, head = _standing(f, c)
    mark = _height_mark(f, pts, max(p[1] for p in head))
    A = add(hand, (6, 27))
    hold(f, "jug", A, size=2.5, variant="bucket", chalk=True, xray=False)
    return pts + mark + hold_outline("jug", A, size=2.5, variant="bucket")


def reading(f):
    """The mannequin's head and shoulders in profile, looking up at a jug
    along a dotted line of sight (the figures' `sight`). The icon's frame
    cuts the shoulders."""
    c = Climber((0, 0), view="side", xray=False, head_tilt=-34)
    geo = c._geometry(COL, False)
    head, lines = geo["head"]
    neck, shirt = geo["torso"][0][0], geo["torso"][0][-1]
    _mannequin(f, [neck, shirt] + head, lines)
    u, r = c.head_frame()
    hc = c._head_centre()
    eye = add(hc, add(mul(r, EYE_SIDE[0] * HEAD_SIZE),
                      mul(u, EYE_SIDE[1] * HEAD_SIZE)))
    A = add(hc, (29, 22))
    hold(f, "jug", A, size=1.0, variant="bucket", chalk=True, xray=False)
    pts = _points(head) + hold_outline("jug", A, size=1.0, variant="bucket")
    look = norm(sub(A, eye))
    f.line(add(eye, mul(look, 3)), sub(A, mul(look, 9)), sw=0.3, dash=(0.25, 0.9))
    # the frame ends 5 cm below the chin, cutting the shoulders
    lo = min(p[1] for p in pts)
    return pts + [(min(p[0] for p in pts), lo - 5)]


def mistakes(f):
    """A climbing shoe skating off a foothold, and the figures' cross."""
    pts = []
    F = (0, 0)
    hold(f, "foot", F, size=1.5, variant="screw-on", xray=False)
    pts += hold_outline("foot", F, size=1.5, variant="screw-on")
    # the shoe tipped down, its toe on the edge of the foothold, skating
    # off it
    d = ang(-24)
    n = perp(d)
    tip = (-3.4, 1.4)
    base = sub(tip, add(mul(d, 24.0), mul(n, 1.8)))

    def P(x, y):
        return add(base, add(mul(d, x), mul(n, y)))
    shoe = [P(*q) for q in SHOE]
    f.smooth(shoe, z=2, tension=0.7, fill=SHOE_FILL, stroke=INK, sw=0.3)
    shoe_details(f, P, 2.01)
    pts += shoe
    # the cross under the toe, where the foot fails
    c = (-9.5, -7.0)
    s = f.mm(0.85)
    f.cross(c, size=s)
    m = s + f.mm(0.3)          # the cross's half-width with its line
    return pts + [add(c, (-m, -m)), add(c, (m, m))]


# name: (scale in mm per cm, drawing, what it means)
ICONS = {
    "tall": (0.0365, tall,
             "Tall climbers: a standing climber and a height mark"),
    "small": (0.0365, small,
              "Small climbers: a short height mark and a jug out of reach"),
    "reading": (0.145, reading,
                "When to use it — reading the wall: a look at a hold"),
    "mistakes": (0.18, mistakes,
                 "Common mistakes: a shoe skating off a foothold, crossed"),
}


def icon_fig(name):
    """The Fig of an icon, framed to ICON_H."""
    scale, draw, _ = ICONS[name]
    pts = draw(Fig(-400, -400, 400, 400, scale))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    pad = ICON_PAD / scale
    H = ICON_H / scale
    cy = (min(ys) + max(ys)) / 2
    assert max(ys) - min(ys) + 2 * ICON_VPAD / scale <= H + 1e-6, name + " is too tall"
    assert (max(xs) - min(xs)) * scale + 2 * ICON_PAD <= ICON_W, name + " is too wide"
    f = Fig(min(xs) - pad, cy - H / 2, max(xs) + pad, cy + H / 2, scale)
    draw(f)
    return f


def build(out):
    for name in ICONS:
        icon_fig(name).save(out + f"/icon-{name}.svg")
