"""Figures for chapter 3, Feet and legs.

Every figure is written as <technique-key>.svg, plus the plate
foot-atlas.svg. Close-ups of shoes on holds use the helpers at the top of
this module; whole-climber figures use the mannequin from climb.py at the
book's standard scale.
"""

import math

import climb
from climb import *
from closeup import SHOE_TOP, SHOE_TOP_TIP, edge_side

SHOE_COL = "#262626"
SHOE_SHAPE = climb.SHOE          # side-profile outline (heel at x=0, sole at y=0)

# points on the side-profile shoe, in shoe coordinates (cm)
SPOT = {
    "tip": (24.4, 2.4),     # very front of the toe
    "toe": (23.0, 1.0),     # front of the sole under the big toe
    "edge": (18.5, 0.2),    # sole under the ball
    "ball": (15.0, 0.0),
    "heel": (0.2, 0.9),     # bottom-back of the heel
    "heelback": (-1.4, 4.0),
    "top": (18.5, 6.9),     # top of the foot behind the toes (toe hooks)
    "toptoe": (21.5, 5.4),  # top of the toes
    "laces": (12.0, 9.3),   # top of the foot over the laces
}
ANKLE = (3.5, 9.0)
BALL = (15.5, 2.0)              # big-toe joint: the forefoot bends here

GHOST = dict(fill=WHITE, stroke=MID, sw=0.3, dash=(0.9, 0.7))


# ---------------------------------------------------------------- helpers


def bend_pt(p, bend):
    """Shoe point `p` with the toes bent up by `bend` degrees at the ball."""
    if not bend:
        return p
    w = min(1.0, max(0.0, (p[0] - 12.0) / 6.0))
    # the sole bends fully; the top of the toe box creases and bends less
    w *= 1.0 - 0.45 * min(1.0, max(0.0, p[1] / 8.0))
    return add(BALL, rot(sub(p, BALL), bend * w)) if w else p


def spot_pt(spot, bend=0.0):
    cp = SPOT[spot] if isinstance(spot, str) else spot
    return bend_pt(cp, bend)


def auto_spot(d, n, bend, wn):
    """The point of the shoe that reaches deepest into a wall whose outward
    normal is `wn` (shoe coordinates)."""
    pts = catmull([bend_pt(p, bend) for p in SHOE_SHAPE], closed=True, k=8)
    return min(pts, key=lambda q: dot(add(mul(d, q[0]), mul(n, q[1])), wn))


def flatten(pts, w0, wn):
    """Squash every point that lies inside the wall onto its surface, the
    way shoe rubber flattens against a smear."""
    out = []
    for p in pts:
        k = dot(sub(p, w0), wn)
        out.append(sub(p, mul(wn, k)) if k < 0 else p)
    return out


def draw_shoe(f, base, d, n, k=1.0, bend=0.0, flat=None, st=None, z=0,
              sole_line=True, xray=False):
    """Draw the profile shoe whose heel-sole origin is `base`. `flat` is a
    (wall point, outward normal) pair: rubber pressed into it is flattened.
    sole_line adds the sole, rand and strap lines of the climbers' shoes;
    xray the dotted outline that shows through a trouser leg."""
    st = st or dict(fill=SHOE_COL, stroke=INK, sw=0.35)

    def P(x, y):
        return add(base, add(mul(d, x * k), mul(n, y * k)))
    shape = [bend_pt(p, bend) for p in SHOE_SHAPE]
    if flat is not None:
        pts = flatten([P(*q) for q in catmull(shape, closed=True, k=8)], *flat)
        f.poly(pts, z=z, **st)
        if xray:
            f.poly(pts, z=climb.XRAY_Z + 1, **climb.XRAY_STYLE)
    else:
        f.smooth([P(*q) for q in shape], z=z, tension=0.7, **st)
        if xray:
            f.smooth([P(*q) for q in shape], z=climb.XRAY_Z + 1, tension=0.7,
                     **climb.XRAY_STYLE)
    if sole_line and st.get("fill") == SHOE_COL:
        shoe_details(f, lambda x, y: P(*bend_pt((x, y), bend)), z + 0.01)
    return P


def ankle_angle(deg, shin, up=1):
    """Angle between the shin (pointing up from the ankle) and the
    heel-to-toe line, as on a real ankle: 90 is neutral, below about 50 the
    toes are pulled up further than an ankle bends, above about 145 they
    are pointed further. Negative if the shin sits on the sole side."""
    d = ang(deg)
    s = ang(shin)
    a = math.degrees(math.acos(max(-1, min(1, dot(d, s)))))
    return a if dot(s, mul(perp(d), up)) >= 0 else -a


class FootClimber(Climber):
    """Climber whose feet may touch with any point of the shoe.

    Extra keys in a foot dict:
      spot: a key of SPOT, an (x, y) point in shoe coordinates, or "auto"
            (the point that reaches deepest into the `flat` wall)
      up:   +1 or -1 to fix which side of the heel-to-toe line the top of
            the shoe faces (perp(direction) * up), instead of letting the
            library turn the top of the foot toward the hip.
      bend: toes bent up at the ball by this many degrees (smears)
      flat: (wall point, outward wall normal): rubber pressed past the wall
            surface is drawn flattened onto it
      press: how far (cm) the contact point is pushed into `flat`
    In side view the knees always bend anatomically.
    """

    KEYS = ("spot", "up", "bend", "flat")

    def solve(self):
        super().solve()
        u, r = self.frame()
        side_anat = self.view == "side" and self.anatomy
        for s in "lr":
            ft = getattr(self, "_" + s + "f")
            if ft["style"] == "back" or not any(k in ft for k in self.KEYS):
                continue
            d = ft["d"]
            n = mul(perp(d), ft["up"]) if "up" in ft else ft["n"]
            bend = ft.get("bend", 0.0)
            spot = ft.get("spot", ft.get("contact", "edge"))
            at = ft["at"]
            if spot == "auto":
                cp = auto_spot(d, n, bend, ft["flat"][1])
                at = sub(at, mul(ft["flat"][1], ft.get("press", 0.8)))
            else:
                cp = spot_pt(spot, bend)
            o = sub(ANKLE, cp)
            ankle = add(at, add(mul(d, o[0] * self.s), mul(n, o[1] * self.s)))
            ft["n"] = n
            ft["ankle_target"] = ankle
            hip = self.J[s + "hip"]
            k = self.leg_len[s]
            kt, ks = k if isinstance(k, tuple) else (k, k)
            lt, ls = self.D["thigh"] * kt, self.D["shin"] * ks
            if side_anat:
                kh = anatomical(hip, ankle, -1)
            else:
                sign = -1 if s == "l" else 1
                kh = chooser(self.knees[s], sign if self.view == "back" else 1,
                             self.pelvis, r)
            self.J[s + "kn"], self.J[s + "an"] = ik(hip, ankle, lt, ls, kh)
            ft["short"] = length(sub(ankle, self.J[s + "an"])) > 1.0

    def _shoe(self, fig, s, st, z):
        ft = getattr(self, "_" + s + "f")
        if ft["style"] == "back":
            return super()._shoe(fig, s, st, z)
        d, n = ft["d"], ft["n"]
        k = self.s
        base = sub(self.J[s + "an"], add(mul(d, ANKLE[0] * k), mul(n, ANKLE[1] * k)))
        ghost = getattr(self, "_ghost", False)
        draw_shoe(fig, base, d, n, k, ft.get("bend", 0.0), ft.get("flat"),
                  st=st, z=z, sole_line=not ghost,
                  xray=self._xray_feet and not ghost)

    def ankles(self):
        """(side, ankle angle) for each profile foot, any view."""
        out = []
        for s in "lr":
            ft = getattr(self, "_" + s + "f")
            if ft["style"] == "back":
                continue
            shin = norm(sub(self.J[s + "kn"], self.J[s + "an"]))
            a = math.degrees(math.acos(max(-1, min(1, dot(shin, ft["d"])))))
            out.append((s, a if dot(shin, ft["n"]) >= 0 else -a))
        return out


def problems(c, lo=48, hi=148):
    """warn() plus ankle angles outside [lo, hi] in any view."""
    out = list(c.warn())
    if isinstance(c, FootClimber):
        for s, a in c.ankles():
            if not lo <= a <= hi:
                out.append(f"{s} ankle {a:.0f} deg (want {lo}-{hi})")
    return out


def check(name, *climbers):
    for c in climbers:
        for w in problems(c):
            print(f"{name}: {w}")


def check_shoe(name, deg, shin, up=1, lo=48, hi=148):
    a = ankle_angle(deg, shin, up)
    if not lo <= a <= hi:
        print(f"{name}: close-up ankle {a:.0f} deg (want {lo}-{hi})")


def shoe_side(f, at, deg, spot="toe", up=1, z=0, ghost=False, shin=None,
              shin_fill=WHITE, shin_len=60, sole_line=True, bend=0.0, k=1.0,
              flat=None, press=0.8, name=None):
    """A shoe in side profile with its `spot` on the point `at`.

    deg: heel-to-toe direction. up: +1 puts the top of the shoe on the left
    of that direction (perp), -1 on the right. shin: direction (degrees) of
    the shin from the ankle, drawn long so the panel edge cuts it off.
    k scales the shoe; bend/flat/press as for FootClimber feet. Returns a
    function mapping shoe coordinates to world points."""
    d = ang(deg)
    n = mul(perp(d), up)
    if spot == "auto":
        cp = auto_spot(d, n, bend, flat[1])
        at = sub(at, mul(flat[1], press))
    else:
        cp = spot_pt(spot, bend)
    base = sub(at, add(mul(d, cp[0] * k), mul(n, cp[1] * k)))

    def P(x, y):
        return add(base, add(mul(d, x * k), mul(n, y * k)))

    st = GHOST if ghost else dict(fill=SHOE_COL, stroke=INK, sw=0.35)
    ankle = P(*ANKLE)
    if shin is not None:
        # the leg goes in front of the shoe, so the shin enters it from
        # above, with a cuff line where they meet
        sv = ang(shin)
        top = add(ankle, mul(sv, shin_len * k))
        sst = GHOST if ghost else dict(fill=shin_fill, stroke=INK, sw=0.35)
        f.poly(capsule(ankle, 3.6 * k, top, 5.6 * k), z=z + 0.2, **sst)
        if not ghost:
            cuf = add(ankle, mul(sv, 2.4 * k))
            w = 3.9 * k
            f.line(add(cuf, mul(perp(sv), w)), add(cuf, mul(perp(sv), -w)),
                   z=z + 0.21, sw=0.3)
        if name:
            check_shoe(name, deg, shin, up)
    draw_shoe(f, base, d, n, k, bend, flat, st=st, z=z,
              sole_line=sole_line and not ghost)
    return P


def shoe_top(f, heel, deg, medial=+1, z=0, ghost=False):
    """A shoe seen from above (from closeup.py), optionally as a ghost."""
    d = ang(deg)
    n = perp(d)

    def P(x, y):
        return add(heel, add(mul(d, x), mul(n, y * medial)))

    pts = [P(x, y) for x, y in SHOE_TOP]
    if ghost:
        f.smooth(pts, z=z, tension=0.7, **GHOST)
        return P
    f.smooth(pts, z=z, fill="#5a5a5a", stroke=INK, sw=0.35, tension=0.7)
    # black toe rand over the toe box, its back edge curving behind the toes
    rand = [P(x, y) for x, y in SHOE_TOP if x >= 21.5]
    rp = [P(21.2, 3.75)] + rand + [P(20.8, -3.85), P(19.6, -1.2), P(19.8, 1.6)]
    f.smooth(rp, z=z + 0.05, fill=INK, stroke=INK, sw=0.3, tension=0.7)
    # one velcro strap across the instep, slanting back to the outside
    f.poly([P(10.4, 3.6), P(13.4, 3.95), P(12.2, -4.1), P(9.2, -3.6)],
           z=z + 0.1, fill=MID, stroke=INK, sw=0.25)
    # the ankle in the heel cup
    f.smooth([P(x, y) for x, y in [(2.2, 0), (3.0, 1.6), (4.8, 1.9), (6.6, 1.3),
                                   (7.0, -0.2), (6.0, -1.6), (4.0, -1.8),
                                   (2.7, -1.3)]],
             z=z + 0.1, fill=LIGHT, stroke=INK, sw=0.3, tension=0.7)
    return P


def shoe_top_against(f, x, wall_y, deg, medial=+1, gap=0.2, **kw):
    """Draw a top-view shoe pointing at `deg` whose toe end is at `x` and
    whose nearest point to the wall (the face at height `wall_y`) sits just
    short of it, so the shoe touches the wall without poking into it.
    Returns the shoe's point function and that nearest point."""
    heel = place_top((x, wall_y), deg, medial)
    d, n = ang(deg), perp(ang(deg))
    pts = [add(heel, add(mul(d, px), mul(n, py * medial))) for px, py in SHOE_TOP]
    top = max(pts, key=lambda p: p[1])
    heel = add(heel, (0, wall_y - gap - top[1]))
    return shoe_top(f, heel, deg, medial, **kw), (top[0], wall_y - gap)


def wall_top(f, x0, x1, y):
    """The wall seen from above, along the top of a plan-view panel."""
    f.poly([(x0, y), (x1, y), (x1, y + 2.5), (x0, y + 2.5)], z=-10, fill=PALE,
           stroke=None)
    f.line((x0, y), (x1, y), z=-9, sw=0.6)
    x = x0
    while x < x1:
        f.line((x, y), (x + 1.4, y + 2.5), z=-9, sw=0.18, stroke=MID)
        x += 1.2


def wall_right(f, x, y0, y1):
    """A vertical wall in side view with its face at x, hatched to the right."""
    w = f.mm(2.2)
    f.poly([(x, y0), (x, y1), (x + w, y1), (x + w, y0)], z=-20, fill=PALE,
           stroke=None)
    f.line((x, y0), (x, y1), z=-19, sw=0.6)
    y = y0
    while y < y1:
        f.line((x, y), (x + w, y + f.mm(1.4)), z=-19, sw=0.18, stroke=MID)
        y += f.mm(2.0)


def tension_line(f, pts, z=35):
    """A broad grey band: the chain of muscles held tight."""
    f.add(f'<path d="{f.smooth_d(pts, closed=False)}" fill="none" '
          f'stroke="{LIGHT}" stroke-width="{f.mm(2.2):.2f}" '
          f'stroke-linecap="round" opacity="0.85"/>', z)


def sight(f, a, b, z=55):
    """A dotted line of sight."""
    f.line(a, b, z=z, sw=0.3, dash=(0.25, 0.9))


# ---------------------------------------------------------------- edging


def plan_panel(x0=-17, x1=17, y0=-26, y1=6, hold_w=16, depth=2.7, scale=1.0):
    f = Fig(x0, y0, x1, y1, scale=scale)
    wall_top(f, x0, x1, 3.5)
    f.poly([(-hold_w / 2, 3.5), (hold_w / 2, 3.5), (hold_w / 2 - 0.6, 3.5 - depth),
            (-hold_w / 2 + 0.6, 3.5 - depth)], z=-5, fill=DARK, stroke=INK, sw=0.35)
    return f


def place_top(tip, deg, medial):
    """Heel point that puts the shoe's toe tip at `tip`."""
    d = ang(deg)
    n = mul(perp(d), medial)
    return sub(tip, add(mul(d, SHOE_TOP_TIP[0]), mul(n, SHOE_TOP_TIP[1])))


def edging(path):
    kw = dict(x0=-17.5, x1=17.5, y0=-22, y1=6, scale=0.7)
    # (a) inside edge: right foot turned out about 40 degrees to the wall
    a = plan_panel(**kw)
    shoe_top_against(a, 5.0, 3.5, 40)
    a.label("big-toe side", (-1, -18.5), to=(2.8, 1.6), size=7)
    # (b) outside edge: right foot turned in, little-toe side on the hold
    b = plan_panel(**kw)
    shoe_top_against(b, -5.0, 3.5, 140)
    b.label("little-toe side", (1, -18.5), to=(-2.8, 1.6), size=7)
    # (c) wrong: arch on the hold, ankle against the wall
    c = plan_panel(**kw)
    shoe_top_against(c, 12.5, 3.5, 0)
    c.cross((0, -9))
    c.label("arch on the hold", (0, -16), size=7)
    combine([a, b, c], path, gap=3, captions=["inside edge", "outside edge",
                                              "not the arch"])


def pivoting(path):
    f = plan_panel(x0=-24, x1=24, y0=-23, y1=6, hold_w=14, depth=3.4, scale=1.2)
    c = (0.0, -0.35)                       # the toe end stays here
    for deg, ghost in ((40, True), (140, False)):
        d = ang(deg)
        n = perp(d)
        # put shoe point (21.5, 0) (front, centre line) on c
        heel = sub(c, mul(d, 21.5))
        shoe_top(f, heel, deg, medial=+1, ghost=ghost, z=2 if not ghost else 0)
    f.turn(c, 17.5, 222, 318)
    f.label("toe stays put", (9.1, 0.4), to=(2.6, -0.9), size=7)
    f.label("heel swings", (0, -20.5), size=7)
    f.save(path)


# ---------------------------------------------------------------- toeing


POCKET = dict(x=-10.0, back=-6.4, lo=-3.2, hi=3.8)   # cavity, section view


def pocket_hold(f):
    """A pocket hold cut through its middle: the dark body sticks out of the
    wall (x = 0) and the pale cavity opens to the left."""
    P = POCKET
    out = [(0, -9.0), (-5.0, -8.6), (-9.2, -6.0), (-11.0, -2.2), (-11.0, 3.0),
           (-9.4, 7.0), (-5.0, 9.6), (0, 10.0)]
    f.smooth(out + [(0.6, 0.5)], z=-6, fill=DARK, stroke=INK, sw=0.35,
             tension=0.6)
    lo, hi = P["lo"], P["hi"]
    mid = (-11.6 + P["back"]) / 2
    hole = [(-11.6, lo), (mid, lo - 0.3), (P["back"] - 0.5, lo + 0.9),
            (P["back"], (lo + hi) / 2), (P["back"] - 0.5, hi - 0.9),
            (mid, hi + 0.2), (-11.6, hi)]
    f.smooth(hole, closed=True, z=-5, fill=PALE, stroke=INK, sw=0.3, tension=0.5)
    # hide the cavity outline across the open mouth
    f.line((-11.55, lo + 0.2), (-11.55, hi - 0.2), z=-4.9, sw=1.1, stroke=WHITE)


def front_pointing(path):
    panels = []
    for good in (False, True):
        f = Fig(-40, -15, 3.5, 30, scale=0.86)
        wall_right(f, 0, -15, 30)
        pocket_hold(f)
        if good:
            tip = (POCKET["back"] - 0.25, 0.4)
            shoe_side(f, tip, -9, spot="tip", shin=104, name="front-pointing b")
            f.label("into the back", (-25, -11), to=(POCKET["back"] - 1.2, -0.6),
                    size=7)
        else:
            lip = (-11.2, POCKET["lo"] + 0.2)
            shoe_side(f, lip, 18, spot="tip", shin=118, name="front-pointing a")
            f.arrow([(-13, -7.5), (-20, -13)], kind="move")
            f.cross((-6, -12.5))
            f.label("tip on the lip", (-22, 24), to=add(lip, (-0.6, 0.6)), size=7)
        panels.append(f)
    combine(panels, path, gap=4, labels=["a", "b"],
            captions=["easiest angle: pops", "point into the back"])


# ---------------------------------------------------------------- foot swap


def swap_frame(n):
    f = Fig(-38, -14, 3.5, 34, scale=0.72)
    # the frame number goes top right, beside the wall: the left shin
    # fills the top-left corner
    f.text(str(n), (-1.6, 30.6), size=9.35, weight=700, anchor="end", z=90)
    wall_right(f, 0, -14, 34)
    edge_side(f, top=(-3.6, 0), depth=3.6, height=2.6)
    lower = (-1.7, 0.1)
    if n == 1:
        shoe_side(f, lower, 0, spot="toe", shin=112, shin_fill=LEFT, z=0)
        shoe_side(f, (-2.4, 5.6), -24, spot="toe", shin=92, z=2)
        f.label("toe over toe", (-17, -10), size=7)
    elif n == 2:
        shoe_side(f, lower, 0, spot="toe", shin=112, ghost=True, z=-1)
        shoe_side(f, (-10.5, -2.5), -6, spot="toe", shin=120, shin_fill=LEFT, z=0)
        shoe_side(f, (-2.4, 3.6), -18, spot="toe", shin=94, z=2)
        f.arrow([(-12, -8.5), (-22, -8.5)], kind="move")
        f.arrow([(-3.5, 13.5), (-3.5, 7)], kind="move")
        f.label("kick back", (-17, -11.6), size=7)
    else:
        shoe_side(f, (-12, -7.5), -12, spot="toe", shin=124, shin_fill=LEFT, z=0)
        shoe_side(f, lower, 0, spot="toe", shin=96, z=2)
        f.label("same spot", (-8, -11.6), to=(-1.4, 0.2), size=7)
    return f


def foot_swap(path):
    combine([swap_frame(i) for i in (1, 2, 3)], path, gap=3,
            captions=["rest lightly", "pop the lower foot", "drop in"])


# ---------------------------------------------------------------- smearing


def wall_frame(angle):
    """Unit vectors for a side-view wall: up the wall, and out of it."""
    d = norm((-math.tan(math.radians(angle)), 1))
    n = (-d[1], d[0])
    return d, n


SL = -20                         # the slab: 20 degrees past vertical


def tw(f, s, size=7.5):
    """Approximate width of a label in world units."""
    return len(s) * f.pt(size) * 0.53


def slab_at(h):
    return (20 + math.tan(math.radians(-SL)) * (h - 30), h)


def smear_pose(good):
    """Climber on the slab (side view) and the wall geometry."""
    wd, wn = wall_frame(SL)
    H = slab_at(150)
    F = slab_at(64)
    hand = add(H, add(mul(wn, 5.5), mul(wd, 2.5)))
    if good:
        foot = {"at": F, "angle": 8, "spot": "auto", "bend": 26,
                "flat": (F, wn), "press": 1.9, "up": 1}
        c = FootClimber((16, 146), view="side", lean=10, lh=hand, rh=hand,
                        lf=foot, rf=foot, head=(1, -2))
    else:
        foot = {"at": F, "angle": -16, "spot": "auto", "flat": (F, wn),
                "press": 0.25, "up": 1}
        c = FootClimber((40, 150), view="side", lean=28, lh=hand, rh=hand,
                        lf=foot, rf=foot, head=(2, -1))
    return c, H, F, wd, wn


def smear_body(good):
    c, H, F, wd, wn = smear_pose(good)
    f = Fig(-26, 40, 84, 226)
    wall_side(f, 20, 30, 226, angle=SL)
    hold_side(f, "jug", H, angle=SL)
    c.draw(f)
    g = c.cog()
    if good:
        f.cog(g, plumb_to=F[1] - 6)
    else:
        # the plumb line meets the slab above the foot: the weight shoves
        # the foot down the slab
        y_hit = 30 + (g[0] - 20) / math.tan(math.radians(-SL))
        f.cog(g, plumb_to=y_hit)
        f.arrow([add(F, add(mul(wd, -5), mul(wn, 2))),
                 add(F, add(mul(wd, -22), mul(wn, 2)))], kind="move")
        f.cross(add(add(F, mul(wd, -15)), mul(wn, 12)))
    check("smearing " + ("b" if good else "a"), c)
    return f, c


def smear_close(good, c):
    """Close-up of the right foot from the body panel `c`."""
    wd, wn = wall_frame(SL)
    f = Fig(-36, -22, 7, 27, scale=0.62)
    w0 = (0, 0)
    t = math.tan(math.radians(-SL))
    wall_side(f, w0[0] + t * (-22 - w0[1]), -22, 27, angle=SL)
    ft = c._rf
    deg = math.degrees(math.atan2(ft["d"][1], ft["d"][0]))
    shin = sub(c.J["rkn"], c.J["ran"])
    sdeg = math.degrees(math.atan2(shin[1], shin[0]))
    shoe_side(f, w0, deg, spot="auto", bend=ft.get("bend", 0),
              flat=(w0, wn), press=ft.get("press", 0.8), shin=sdeg,
              shin_len=40, name="smearing close-up")
    if good:
        p = add(w0, mul(wd, -16))       # below the shoe, clear of the sole
        f.arrow([add(p, mul(wn, 10)), add(p, mul(wn, 0.8))], kind="force")
        f.label("more rubber", (-23, -19.6), size=6.5)
    else:
        f.arrow([add(w0, add(mul(wd, -4), mul(wn, 2))),
                 add(w0, add(mul(wd, -15), mul(wn, 2)))], kind="move")
        f.label("tip only", (-17, -15), to=add(w0, mul(wn, 0.4)), size=7)
    return f


def smearing(path):
    fa, ca = smear_body(False)
    fb, cb = smear_body(True)
    combine([fa, smear_close(False, ca), fb, smear_close(True, cb)], path,
            gap=4, labels=["a", "", "b", ""],
            captions=["leaning in", "heel high", "hips over feet", "heel low"])


# ---------------------------------------------------------------- toe pull


def toe_pull(path):
    """Side view of a 35 degree overhang. The hands, holds and foot spot are
    the same in both panels; only the hips and the tension change."""
    panels = []
    aw = 35
    wd, wn = wall_frame(aw)
    for good in (False, True):
        f = Fig(-124, 52, 52, 226)
        at = wall_side(f, 44, 40, 226, angle=aw)
        H = at(205)
        F = at(92)
        hold_side(f, "jug", H, angle=aw)
        hold_side(f, "foot", F, angle=aw)
        hand = add(H, (-3.5, 2))
        tip = add(F, (-2.8, 2.6))
        foot = {"at": tip, "angle": 10, "spot": "tip"}
        if good:
            c = FootClimber(None, shoulders=add(H, (-12, -55)), view="side",
                            lean=-30, lh=hand, rh=hand, lf=foot, rf=foot,
                            head=(1, -2))
            c.draw(f)
            J = c.J
            u, r = c.frame()
            band = [add(J["ran"], (-4, -3)),
                    add(lerp(J["ran"], J["rkn"], 0.5), mul(perp(norm(sub(J["rkn"], J["ran"]))), -6)),
                    add(J["rkn"], (-3, -7)), add(c.pelvis, add(mul(r, -10), (0, -3))),
                    c.local(-13, 26), add(J["rsh"], mul(r, -9)),
                    add(lerp(J["rsh"], J["rha"], 0.55), mul(r, -7)),
                    add(J["rha"], (-6, 4))]
            tension_line(f, band, z=-2)
            f.label("hips in", (-96, 66), to=add(c.pelvis, (-8, -8)))
        else:
            c = FootClimber(None, shoulders=add(H, (-4, -62)), view="side",
                            lean=8, lh=hand, rh=hand, lf=foot, rf=foot,
                            head=(1, -2))
            c.draw(f)
            f.arrow([add(tip, add(mul(wn, 4), mul(wd, -3))),
                     add(tip, add(mul(wn, 18), mul(wd, -14)))], kind="move")
            f.cross(add(tip, add(mul(wn, 4), mul(wd, -20))))
            f.label("hips sag out", (-90, 62), to=add(c.pelvis, (-8, -8)))
        check("toe-pull", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["passive foot pops off", "pull the foot onto the hold"])


# ---------------------------------------------------------------- heel hook


def reach_toward(c, side, target, k=0.99):
    """The point at (almost) full arm's reach from a climber's shoulder
    toward `target`: where the hand goes when it falls short."""
    sh = c.J[side + "sh"]
    L = (c.D["upper_arm"] + c.D["forearm"] + c.D["hand"]) * c.arm_len[side]
    return add(sh, mul(norm(sub(target, sh)), L * k))


HK = dict(LH=(-42, 196), T=(60, 278), HH=(84, 168), LF=(-14, 76), RF=(28, 44))
HK_FOOT = 30                     # heel-to-toe direction of the hooked foot
HEEL_ON = (-3, 5.4)              # the heel on a jug's lip, relative to the jug


def heel_hook_pose():
    heel = add(HK["HH"], HEEL_ON)
    return FootClimber((30, 172), lh=grip(HK["LH"]), rh=grip(HK["T"]),
                       lf={"at": stand(HK["LF"]), "angle": 196},
                       rf={"at": heel, "angle": HK_FOOT, "spot": "heel", "up": 1},
                       knees={"r": "up"}, leg_len={"r": (.85, .7)}, head=(2, 3))


def hk_panel():
    f = Fig(-62, 34, 110, 296)
    wall_grid(f)
    hold(f, "jug", HK["LH"])
    hold(f, "jug", HK["T"])
    hold(f, "jug", HK["HH"], size=1.1)
    hold(f, "foot", HK["LF"])
    hold(f, "foot", HK["RF"])
    return f


def heel_hook(path):
    a = hk_panel()
    kw = dict(lh=grip(HK["LH"]), lf={"at": stand(HK["LF"]), "angle": 196},
              rf={"at": stand(HK["RF"]), "angle": -16}, head=(2, 3),
              elbows={"l": "down"})
    c = FootClimber((2, 145), rh=(0, 0), **kw)
    c = FootClimber((2, 145), rh=reach_toward(c, "r", grip(HK["T"])), **kw)
    c.draw(a)
    a.cross((56, 263), size=a.mm(1.2))
    b = hk_panel()
    d = heel_hook_pose()
    d.draw(b)
    heel = add(HK["HH"], HEEL_ON)
    b.arrow([add(heel, (-6, -13)), add(heel, (-34, -24))], kind="force")
    b.label("pull heel to bum", (66, 136), size=7.5)
    check("heel-hook", c, d)
    # (c) close-up of the hooked heel, same view
    shin = sub(d.J["rkn"], d.J["ran"])
    sdeg = math.degrees(math.atan2(shin[1], shin[0]))
    k = Fig(-27, -14, 27, 32, scale=0.75)
    hold(k, "jug", (0, 0), size=1.1)
    hc = HEEL_ON
    P = shoe_side(k, hc, HK_FOOT, spot="heel", up=1, shin=sdeg, shin_len=40,
                  name="heel-hook close-up")
    k.arrow([(-7, 5), (-25, -3)], kind="force")
    k.text("pull", (-17, -7), size=7)
    k.label("toes out", (6, 28), to=P(22.5, 4.5), size=7)
    combine([a, b, k], path, gap=5, labels=["a", "b", "c"],
            captions=["feet low: too short", "heel hook: hips rise",
                      "heel on, toes out"])


# ---------------------------------------------------------------- toe hook


TK = dict(RH=(32, 196), LT=(-36, 236), LH0=(-40, 188), TH=(-84, 118), RF=(22, 54))
TK_FOOT = 88                     # the hooked foot points up, toes flexed


def toe_hook(path):
    # (a) back view: a left toe hook keeps the left side in while the left
    # hand moves; the right foot pushes below the centre of gravity
    a = Fig(-114, 34, 66, 254)
    wall_grid(a)
    hold(a, "jug", TK["RH"])
    hold(a, "jug", TK["LT"])
    hold(a, "jug", TK["LH0"])
    hold(a, "jug", TK["TH"], use=180, size=1.2)
    hold(a, "foot", TK["RF"])
    contact = add(TK["TH"], (-7.2, -1))
    c = FootClimber((6, 116), lean=-4, lh=(-34, 222), rh=grip(TK["RH"]),
                    lf={"at": contact, "angle": TK_FOOT, "spot": "toptoe", "up": -1},
                    rf={"at": stand(TK["RF"]), "angle": -24},
                    knees={"l": "up", "r": "out"}, leg_len={"r": .9},
                    head=(-3, 3))
    c.draw(a)
    a.arrow([add(grip(TK["LH0"]), (0, 7)), (-35, 214)], kind="move")
    a.arrow([add(stand(TK["RF"]), (10, 18)), add(stand(TK["RF"]), (10, 4))],
            kind="force")
    a.label("push", (44, 66), size=7.5)
    a.label("toe hook", (-92, 146), to=add(contact, (0, 4)))
    a.cog(c.cog(), plumb_to=46)
    check("toe-hook a", c)

    # (b) close-up, same view: the top of the toes behind the far side of
    # the hold, ankle flexed, the leg pulling the foot toward the body
    shin = sub(c.J["lkn"], c.J["lan"])
    sdeg = math.degrees(math.atan2(shin[1], shin[0]))
    k = Fig(-34, -30, 24, 22, scale=0.75)
    hold(k, "jug", (0, 0), use=180, size=1.2)
    kc = (-7.2, -1)
    P = shoe_side(k, kc, TK_FOOT, spot="toptoe", up=-1, shin=sdeg, shin_len=50,
                  shin_fill=LEFT, name="toe-hook close-up")
    k.arrow([(4, -22), (20, -22)], kind="force")
    k.text("leg pulls", (11, -26.5), size=7)
    k.label("top of the toes", (-16, 18), to=add(kc, (-0.8, 1.5)), size=7)
    combine([a, k], path, gap=6, labels=["a", "b"],
            captions=["left side held in", "toes behind the hold"])


# ---------------------------------------------------------------- bicycle


SHELF = [(0, -5.2), (8.5, -3.0), (11.2, -0.6), (11.4, 2.0), (9.5, 3.4),
         (3.0, 3.1), (0, 4.2)]


def shelf(f, H, z=-6, k=1.0):
    """A big flat-topped hold in side view (hold coordinates via H)."""
    f.smooth([H(x * k, y * k) for x, y in SHELF], z=z, fill=DARK, stroke=INK,
             sw=0.35, tension=0.45)


def bicycle(path):
    ang_w = 20
    f = Fig(-46, -40, 14, 34, scale=0.85)
    at = wall_side(f, 13.1, -40, 34, angle=ang_w)
    P = at(0)
    d, n = wall_frame(ang_w)

    def H(x, y):                      # hold coordinates -> world
        return add(P, add(mul(n, x), mul(d, y)))

    k = 1.5                          # a big hold or volume edge
    shelf(f, H, k=k)
    # top foot (right): toe on the top of the hold, pressing down
    top = H(5.5, 3.15 * k)
    shoe_side(f, top, 6, spot="toe", up=1, shin=114, z=2, name="bicycle top")
    # bottom foot (left): top of the toes under the hold, pulling up; the
    # shin rises in front of the hold
    under = H(7.5, -3.75 * k)
    shoe_side(f, under, 22, spot="top", up=1, shin=134, shin_fill=LEFT,
              z=0, name="bicycle under")
    f.arrow([add(top, (-2, 16)), add(top, (-2, 7.5))], kind="force")
    f.arrow([add(under, (2, -22)), add(under, (2, -12))], kind="force")
    f.label("push", (-16, 26), size=7)
    f.label("pull", (-4, -31), size=7)
    f.save(path)


# ---------------------------------------------------------------- heel-toe cam


def heel_toe_cam(path):
    """Back view close-up: heel down on a jug, top of the toes up under a
    volume, the foot wedged between them."""
    f = Fig(-34, -14, 44, 44, scale=0.75)
    hold(f, "jug", (0, 0), size=1.1)
    heel = (-5.5, 5.5)
    deg = 14
    P = shoe_side(f, heel, deg, spot="heel", up=1, shin=104, shin_len=50,
                  name="heel-toe cam")
    t0 = P(*SPOT["top"])
    # the underside of the volume rests on the top of the toes
    u = norm(sub(P(23, 5.6), P(14, 8.2)))
    a0 = add(P(13.0, 8.5), mul(perp(u), 0.2))
    a1 = add(a0, mul(u, 42))
    apex = add(lerp(a0, a1, 0.6), mul(perp(u), 24))
    volume(f, [a0, a1, apex], apex=add(lerp(a0, a1, 0.6), mul(perp(u), 9)))
    f.arrow([add(heel, (-11, 16)), add(heel, (-11, 4))], kind="force")
    f.arrow([add(t0, (2, -20)), add(t0, (2, -7.5))], kind="force")
    f.label("heel down", (-23, 25), size=7)
    f.label("toes up", (24, -10), size=7)
    f.save(path)


# ---------------------------------------------------------------- knee bar


def knee_bar(path):
    """Side view of a 40 degree overhang: right toe on a foothold, the
    thigh just above the knee wedged up under a volume, both arms hanging
    (the left arm behind the right), so the right hand is free."""
    ang_w = 40
    WX = 60
    t = math.tan(math.radians(ang_w))
    wd, wn = wall_frame(ang_w)

    def at(h):
        return (WX - t * (h - 30), h)

    f = Fig(-142, 40, 62, 214)
    wall_side(f, WX, 30, 214, angle=ang_w)
    F = at(96)
    hold_side(f, "foot", F, angle=ang_w, size=1.3)
    tip = add(F, add(mul(wn, 3.0), mul(wd, 2.2)))
    # the shin runs close along the wall and the thigh falls gently away
    # from the knee, so the lower thigh sits under a face that sticks
    # straight out of the wall: the underside of a big volume
    fa, shin_deg, thigh_deg, lean = 20, 140, 205, -15
    # build the leg backwards from the toe: ankle, knee, hip
    d = ang(fa)
    o = sub(ANKLE, SPOT["tip"])
    ankle = add(tip, add(mul(d, o[0]), mul(perp(d), o[1])))
    K = add(ankle, mul(ang(shin_deg), DIM["shin"]))
    hip = add(K, mul(ang(thigh_deg), DIM["thigh"]))
    u = ang(90 - lean)
    pelvis = sub(hip, mul((u[1], -u[0]), 1.0))
    # the volume's underside lies along the top of the thigh above the knee
    th = ang(thigh_deg)
    nrm = ang(thigh_deg - 90)                 # top side of the thigh
    touch = add(add(K, mul(th, 9)), mul(nrm, DIM["r_knee"] + 1.4))
    s_dir = ang(thigh_deg + 180 - 6)          # from the touch toward the wall
    k_hit = cross(sub((WX, 30), touch), wd) / cross(s_dir, wd)
    W0 = add(touch, mul(s_dir, k_hit))
    # a triangular volume about 45 cm deep on a 72 cm base: its outer
    # corner V sits just past the contact, and its outer face rises
    # almost vertically back to the wall, clear of the face and chest
    V = add(touch, mul(s_dir, -3))
    W1 = add(W0, mul(wd, 72))
    f.poly([W0, V, W1], z=-12, fill=LIGHT, stroke=INK, sw=0.35)
    c = FootClimber(pelvis, view="side", lean=lean, lh=None, rh=None,
                    rf={"at": tip, "angle": fa, "spot": "tip", "up": 1},
                    lf={"at": (-60, 50), "angle": -62, "up": 1},
                    head=(-4, -3))
    c.draw(f)
    f.label("toe digs in", (-2, 52), to=add(tip, mul(wn, 1.5)))
    # on two lines, so the label stays left of the wall line; the leader
    # comes down between the head and the volume and ends on the thigh
    # where it goes under the volume's corner
    f.text("thigh above", (-115, 203), size=7.5)
    f.label("the knee", (-115, 194), anchor="middle",
            to=add(add(K, mul(th, 15)), mul(nrm, 6.2)))
    f.label("hand free", (-100, 52), to=add(c.J["rha"], (0, -3)))
    check("knee-bar", c)
    f.save(path)


# ---------------------------------------------------------------- high step


HS = dict(LH=(-44, 216), RH=(72, 178), T=(44, 282), LF=(-18, 60), RF=(26, 60),
          HF=(46, 114))


def hs_panel(x0=-62, x1=100, y1=296):
    f = Fig(x0, 40, x1, y1)
    wall_grid(f)
    for k in ("LH", "RH", "T"):
        hold(f, "jug", HS[k])
    for k in ("LF", "RF", "HF"):
        hold(f, "foot", HS[k])
    return f


def high_step_pose():
    """Right foot up on the high hold beside the hip, knee up and out."""
    return FootClimber((-6, 136), lh=grip(HS["LH"]), rh=grip(HS["RH"]),
                       lf={"at": stand(HS["LF"]), "angle": 196},
                       rf={"at": stand(HS["HF"]), "style": "back"},
                       knees={"r": "up", "l": "out"}, leg_len={"r": .85},
                       elbows={"r": "down"}, head=(3, -2))


def high_step(path):
    a = hs_panel()
    # standing tall on the low feet, right arm at full stretch: still short
    c = FootClimber((0, 150), lh=grip(HS["LH"]), rh=(36, 259),
                    lf={"at": stand(HS["LF"]), "angle": 196},
                    rf={"at": stand(HS["RF"]), "angle": -16}, head=(2, 3))
    c.draw(a)
    a.cross((41, 272), size=a.mm(1.2))
    b = hs_panel()
    d = high_step_pose()
    d.draw(b)
    b.arrow([add(stand(HS["RF"]), (10, 8)), add(stand(HS["HF"]), (10, -10))],
            kind="move")
    b.label("knee out", (80, 146), to=add(d.J["rkn"], (6, -2)))
    check("high-step", c, d)
    combine([a, b], path, gap=6, labels=["a", "b"],
            captions=["feet low: too short", "high step, knee out"])


RO_LF = (14, 104)                # where the left foot steps up in a rockover
RO_ARM = ("r", (75, 212), grip(HS["RH"]))   # right hand presses, elbow up


def rockover_poses():
    """Hips across over the high foot, then stand up. While the hips move
    across, the right hand presses down on its hold with the elbow up and
    back: that upper arm points out of the wall, so the arm is drawn
    through an explicit elbow (RO_ARM)."""
    across = FootClimber((38, 150), lean=-4, lh=grip(HS["LH"]),
                         rh=grip(HS["RH"]),
                         lf={"at": stand(HS["LF"]), "angle": 200},
                         rf={"at": stand(HS["HF"]), "style": "back"},
                         knees={"r": "right", "l": "out"}, leg_len={"r": .7},
                         elbows={"l": "down", "r": "down"}, head=(3, -1),
                         order=["lleg", "rleg", "torso", "larm"])
    up = FootClimber((36, 186), lean=-8, lh=grip(HS["LH"]), rh=grip(HS["T"]),
                     lf={"at": stand(RO_LF), "style": "back"},
                     rf={"at": stand(HS["HF"]), "style": "back"},
                     knees={"r": "right", "l": "out"}, leg_len={"r": .9},
                     elbows={"l": "down"}, head=(1, 3))
    return across, up


def ro_panel():
    f = hs_panel()
    hold(f, "foot", RO_LF)
    return f


def rockover(path):
    across, up = rockover_poses()
    start = high_step_pose()
    p1 = ro_panel()
    start.draw(p1, ghost=True)
    across.draw(p1, z=5)
    across.draw_arm(p1, *RO_ARM, z=8.5)
    p1.body_arrow([add(start.pelvis, (-2, -2)), add(across.pelvis, (-8, -2))],
                  width=3.0)
    p1.cog(across.cog(), plumb_to=HS["HF"][1] + 4)
    p2 = ro_panel()
    across.draw(p2, ghost=True)
    across.draw_arm(p2, *RO_ARM, z=3.5, ghost=True)
    up.draw(p2, z=5)
    p2.body_arrow([add(across.pelvis, (0, 4)), add(up.pelvis, (0, 2))],
                  width=3.0)
    check("rockover", across, up)
    combine([p1, p2], path, gap=6, labels=["1", "2"],
            captions=["hips across first", "then stand up"])


# ---------------------------------------------------------------- hand-foot match


def hand_foot_match(path):
    L = (-36, 118)                  # the ledge
    RH = (30, 214)
    RF = (26, 62)
    LF = (-4, 56)
    top = add(L, (0, 10))           # top surface of the ledge
    hand = add(top, (11, 2))        # left hand pressing on the right part
    spot = add(top, (-10, 0.5))     # where the left foot goes
    panels = []
    for stage in (1, 2):
        f = Fig(-76, 40, 72, 250)
        wall_grid(f)
        hold(f, "jug", L, size=2.0)
        hold(f, "jug", RH)
        hold(f, "foot", RF)
        hold(f, "foot", LF)
        if stage == 1:
            c = FootClimber((8, 142), lh=hand, rh=grip(RH),
                            lf={"at": stand(LF), "angle": 196},
                            rf={"at": stand(RF), "angle": -16},
                            elbows={"l": "out"}, head=(-3, -2))
            c.draw(f)
            f.arrow([add(hand, (-11, 24)), add(hand, (-11, 9))], kind="force")
            f.arrow([add(stand(LF), (-14, 6)), add(spot, (-2, -12))],
                    kind="move")
            f.label("press", (-53, 148), size=7.5)
        else:
            # the left knee comes up beside the chest: the thigh points
            # into the wall, so it is drawn behind the seat, the T-shirt
            # and the pressing arm, and only the knee shows past the body
            c = FootClimber((10, 146), lh=hand, rh=grip(RH),
                            lf={"at": spot, "style": "back"},
                            rf={"at": stand(RF), "angle": -16},
                            knees={"l": "up"}, leg_len={"l": .85},
                            elbows={"l": "in"}, head=(-3, -2),
                            order=["rleg", "lleg", "torso", "rarm", "larm"])
            c.draw(f)
            f.body_arrow([add(c.pelvis, (14, -14)), add(c.pelvis, (-16, -14)),
                          add(spot, (14, 16))], width=2.2)
            f.label("foot beside hand", (-38, 92), to=add(spot, (2, -2)))
        check("hand-foot-match", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["press, then foot up", "hips over the foot"])


# ---------------------------------------------------------------- precise footwork


def precise_footwork(path):
    LH = (-28, 182)
    RH = (28, 186)
    T = (40, 250)
    LF = (-24, 52)
    F = (30, 66)                    # the small foothold being stepped on
    panels = []
    for good in (False, True):
        f = Fig(-70, 26, 88, 262)
        wall_grid(f)
        for h in (LH, RH, T):
            hold(f, "jug", h)
        hold(f, "foot", LF)
        hold(f, "foot", F, size=0.8)
        kw = dict(lh=grip(LH), rh=grip(RH),
                  lf={"at": stand(LF), "angle": 196}, leg_len={"l": .95})
        if good:
            # head bowed and tipped toward the right foot
            c = FootClimber((-4, 118), head=(3, 0), head_tilt=18,
                            rf={"at": stand(F, size=0.8), "angle": -12}, **kw)
            c.draw(f)
            sight(f, add(c.J["head"], (7, -7)), add(F, (-1, 5)))
        else:
            # head tipped back to look up at the target
            c = FootClimber((-4, 118), head=(2.5, -1.5),
                            rf={"at": add(F, (1, -8)), "angle": -15,
                                "spot": "tip"}, **kw)
            c.draw(f)
            sight(f, add(c.J["head"], (4, 9)), add(T, (-2, -5)))
            for k in range(3):
                x = F[0] - 3 + 3 * k
                f.line((x, F[1] - 3.0), (x + 1.0, F[1] - 6.0), sw=0.3)
            f.arrow([add(F, (14, -6)), add(F, (14, -20))], kind="move")
            f.cross(add(F, (24, -13)))
            f.label("lands short, slips", (40, 33), size=7.5)
        check("precise-footwork", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["eyes already up", "eyes on the foot"])


# ---------------------------------------------------------------- filmstrip


HR = dict(LH=(-24, 226), RH=(60, 180), T=(36, 290), HH=(44, 110), LF=(-4, 56),
          LF2=(0, 100))


def rock_up_poses():
    """Heel hook rock-up, back view: heel on a hip-high hold, pull, hips over
    the heel, roll onto the toe, stand and reach. The hooked foot turns
    from toes-out to level as the hips rise; once the hips are over it the
    knee points into the wall, so that leg is foreshortened (as is the left
    leg while its knee points out from the wall). While the body rises on
    the bent left arm, its elbow points back and down, out of the wall, so
    that arm is shortened a little; it keeps the elbow inside the frame.
    In frame 4 the right hand presses on its hold with the elbow up and
    back: the upper arm points out of the wall, so that arm is drawn
    through an explicit elbow (the climber's `press_arm`)."""
    heel = add(HR["HH"], HEEL_ON)
    on_lf = {"at": stand(HR["LF"]), "style": "back"}
    on_lf2 = {"at": stand(HR["LF2"]), "style": "back"}
    toe = {"at": stand(HR["HH"]), "style": "back"}
    kw = dict(lh=grip(HR["LH"]), order=["lleg", "larm", "torso", "rarm", "rleg"])
    low = {"l": "down", "r": "down"}            # elbows while hanging
    press = {"l": "down", "r": "right"}         # right elbow out to reach

    def hook(a):
        return {"at": heel, "angle": a, "spot": "heel", "up": 1}
    # the hooking shin points out from the wall toward us, the thigh less so.
    # The right hand's hold is out to the side at shoulder height, so that
    # arm points into the wall and is shortened a little; its elbow then
    # stays above the raised right knee instead of meeting it
    hk = (0.85, 0.7)
    ra = .82
    poses = [
        FootClimber((-6, 120), rh=grip(HR["RH"]), lf=on_lf, rf=hook(40),
                    knees={"r": "up", "l": "out"}, leg_len={"r": hk, "l": .8},
                    arm_len={"r": ra}, head=(3, -1), elbows=low, **kw),
        FootClimber((2, 134), rh=grip(HR["RH"]), lf=on_lf, rf=hook(24),
                    knees={"r": "up", "l": "out"}, leg_len={"r": hk, "l": .86},
                    arm_len={"l": .9, "r": ra}, head=(3, 0), elbows=low, **kw),
        FootClimber((12, 148), rh=grip(HR["RH"]), lf=on_lf, rf=hook(4),
                    knees={"r": "up", "l": "out"}, leg_len={"r": hk, "l": .94},
                    arm_len={"l": .94, "r": ra}, head=(2, 0), elbows=low, **kw),
        FootClimber((22, 166), rh=add(HR["RH"], (-2, 6)), lf=on_lf2, rf=toe,
                    knees={"r": "right", "l": "out"}, leg_len={"r": .66},
                    head=(1, 2), elbows=low, lh=kw["lh"],
                    order=["lleg", "larm", "torso", "rleg"]),
        FootClimber((28, 192), rh=grip(HR["T"]), lf=on_lf2, rf=toe,
                    knees={"r": "right", "l": "out"}, leg_len={"r": .86},
                    head=(1, 4), elbows=press, **kw),
    ]
    poses[3].press_arm = ("r", (60, 210), add(HR["RH"], (-2, 6)))
    return poses


def rock_up_frame():
    f = Fig(-42, 46, 70, 302, scale=0.28)
    wall_grid(f)
    for k in ("LH", "RH", "T"):
        hold(f, "jug", HR[k])
    hold(f, "jug", HR["HH"], size=1.1)
    hold(f, "foot", HR["LF"])
    hold(f, "foot", HR["LF2"])
    return f


def filmstrip_heel_hook(path):
    poses = rock_up_poses()
    frames = []
    for i, c in enumerate(poses):
        f = rock_up_frame()
        c.draw(f)
        if hasattr(c, "press_arm"):
            c.draw_arm(f, *c.press_arm, z=2.5)
        if i == 1:
            heel = add(HR["HH"], HEEL_ON)
            f.arrow([add(heel, (-6, -12)), add(heel, (-30, -20))], kind="force")
        check(f"filmstrip heel hook {i + 1}", c)
        frames.append(f)
    filmstrip(frames, path, captions=[
        "hook the heel, toes out", "pull heel to bum", "hips over the heel",
        "roll onto the toe", "stand up and reach"])


# ---------------------------------------------------------------- foot atlas


def grid(rows, path, gap=5.0, row_gap=3.0, captions=None):
    """Lay out rows of figures (a list of lists) in one SVG, each row
    centred, with a caption under every tile (sizes in mm)."""
    cap_h = 4.6 if captions else 0.0
    sizes = [[((f.x1 - f.x0) * f.scale, (f.y1 - f.y0) * f.scale) for f in row]
             for row in rows]
    widths = [sum(w for w, _ in r) + gap * (len(r) - 1) for r in sizes]
    W = max(widths)
    heights = [max(h for _, h in r) + cap_h for r in sizes]
    H = sum(heights) + row_gap * (len(rows) - 1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
           f'height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">']
    y = 0.0
    k = 0
    for ri, (row, sz) in enumerate(zip(rows, sizes)):
        x = (W - widths[ri]) / 2
        hmax = max(h for _, h in sz)
        for f, (w, h) in zip(row, sz):
            inner = f.svg().split("\n", 1)[1].rsplit("</svg>", 1)[0]
            fw, fh = f.x1 - f.x0, f.y1 - f.y0
            out.append(f'<clipPath id="gp{k}"><rect x="0" y="0" width="{fw:.2f}" '
                       f'height="{fh:.2f}"/></clipPath>')
            out.append(f'<g transform="translate({x:.2f},{y + hmax - h:.2f}) '
                       f'scale({f.scale:.5f})"><g clip-path="url(#gp{k})">'
                       f'{inner}</g></g>')
            if captions:
                out.append(f'<text x="{x + w / 2:.2f}" y="{y + hmax + 3.5:.2f}" '
                           f'font-family="{FONT}" font-size="2.9" font-weight="500" '
                           f'text-anchor="middle">{esc(captions[k])}</text>')
            x += w + gap
            k += 1
        y += heights[ri] + row_gap
    out.append("</svg>")
    with open(path, "w") as fh:
        fh.write("\n".join(out) + "\n")


AT = 0.48                       # paper mm per cm in every atlas tile
TILE = (-62, -34, 34, 40)       # world frame of a tile (x0, y0, x1, y1)


def tile():
    return Fig(*TILE, scale=AT)


def touch(f, p, z=70):
    """Mark the contact point: a black dot with a white ring."""
    f.circle(p, f.mm(0.75), z=z, fill=WHITE, stroke=None)
    f.circle(p, f.mm(0.5), z=z + 0.1, fill=INK, stroke=None)


def wall_line(f, angle, through=(0, 0)):
    """A side-view wall at `angle` passing through `through`, over the whole
    tile; returns (up-the-wall, out-of-the-wall) unit vectors."""
    d, n = wall_frame(angle)
    t = math.tan(math.radians(angle))
    y0, y1 = f.y0, f.y1
    wall_side(f, through[0] - t * (y0 - through[1]), y0, y1, angle=angle)
    return d, n


def atlas_toe_edge():
    f = tile()
    wall_line(f, 0, (0, 0))
    y = -8
    edge_side(f, top=(-3.4, y), depth=3.4, height=3.0, wall_x=0)
    tip = (-3.0, y + 0.25)
    shoe_side(f, tip, -8, spot="tip", shin=102, shin_len=45,
              name="atlas toe edge")
    f.arrow([(-8, y + 21), (-8, y + 8.5)], kind="force")
    touch(f, tip)
    return f


def atlas_edge_top(inside):
    """Seen from above, wall along the top as in the edging figure: the
    right foot on an edge. Drawn at twice the side views' scale, since a
    shoe from above has no leg to fill the tile."""
    k = 2.0
    f = Fig(*[v / k for v in TILE], scale=AT * k)
    cx, wy = (f.x0 + f.x1) / 2, 12.0
    wall_top(f, f.x0, f.x1, wy)
    f.poly([(cx - 8, wy), (cx + 8, wy), (cx + 7.4, wy - 2.7), (cx - 7.4, wy - 2.7)],
           z=-5, fill=DARK, stroke=INK, sw=0.35)
    if inside:
        deg, tip = 40, (cx + 5.0, wy)      # toes turned out
    else:
        deg, tip = 140, (cx - 5.0, wy)     # toes across the body
    P, contact = shoe_top_against(f, tip[0], wy, deg)
    touch(f, contact)
    return f


def atlas_smear_wall():
    f = tile()
    c, H, F, wd, wn = smear_pose(True)
    o = (4, -4)
    d, n = wall_line(f, SL, o)
    ft = c._rf
    deg = math.degrees(math.atan2(ft["d"][1], ft["d"][0]))
    shin = sub(c.J["rkn"], c.J["ran"])
    sdeg = math.degrees(math.atan2(shin[1], shin[0]))
    shoe_side(f, o, deg, spot="auto", bend=ft["bend"], flat=(o, n),
              press=ft["press"], shin=sdeg, shin_len=50, name="atlas smear")
    p = add(o, mul(d, -20))         # below the shoe, clear of the sole
    f.arrow([add(p, mul(n, 14)), add(p, mul(n, 1.0))], kind="force")
    touch(f, add(o, mul(d, -1.6)))
    return f


def atlas_smear_volume():
    """A volume on a vertical wall; the foot smears on its sloping face with
    the heel well down."""
    f = tile()
    wall_line(f, 0, (14, 0))
    face = 38                                   # slope of the volume face
    u = ang(face)
    nf = perp(u)                                # out of the face (up-left)
    base = (-40, -34)
    top = add(base, mul(u, 69))
    f.poly([base, top, (14, top[1]), (14, base[1])], z=-12, fill=LIGHT,
           stroke=INK, sw=0.35)
    cpt = add(base, mul(u, 44))
    shoe_side(f, cpt, 14, spot="auto", bend=14, flat=(cpt, nf), press=1.6,
              shin=82, shin_len=45, name="atlas smear volume")
    p = add(cpt, mul(u, 8))
    f.arrow([add(p, mul(nf, 13)), add(p, mul(nf, 0.8))], kind="force")
    touch(f, add(cpt, mul(u, -1.5)))
    return f


def atlas_heel_hook():
    """Heel over a jug above you on a vertical wall, sole against the wall,
    toes up; the leg pulls the heel down and out toward the body."""
    f = tile()
    wall_line(f, 0, (0, 0))
    hold_side(f, "jug", (0, 2))
    heel = (-4.4, 6.0)
    shoe_side(f, heel, 98, spot="heel", up=1, shin=226, shin_len=80,
              name="atlas heel hook")
    # the pull along the shin, drawn beside it (below), not on it
    f.arrow([(-9, -4), (-21, -15)], kind="force")
    touch(f, heel)
    return f


def atlas_toe_hook():
    """Top of the toes pulling up under a big hold on a 20 degree wall."""
    f = tile()
    ang_w = 20
    o = (6, 8)
    d, n = wall_line(f, ang_w, o)

    def H(x, y):
        return add(o, add(mul(n, x), mul(d, y)))
    shelf(f, H, k=1.4)
    under = H(7.0, -3.75 * 1.4)
    shoe_side(f, under, 16, spot="top", up=1, shin=118, shin_len=50,
              name="atlas toe hook")
    f.arrow([add(under, (2, -22)), add(under, (2, -9))], kind="force")
    touch(f, under)
    return f


def atlas_cam():
    """From behind (as in the entry figure): heel down on a jug, top of the
    toes up under a volume."""
    f = tile()
    o = (-24, -12)
    hold(f, "jug", o, size=1.1)
    heel = add(o, (-5.5, 5.5))
    deg = 14
    P = shoe_side(f, heel, deg, spot="heel", up=1, shin=104, shin_len=50,
                  name="atlas cam")
    t0 = P(*SPOT["top"])
    u = norm(sub(P(23, 5.6), P(14, 8.2)))
    a0 = add(P(13.0, 8.5), mul(perp(u), 0.2))
    a1 = add(a0, mul(u, 40))
    apex = add(lerp(a0, a1, 0.6), mul(perp(u), 24))
    volume(f, [a0, a1, apex], apex=add(lerp(a0, a1, 0.6), mul(perp(u), 9)))
    f.arrow([add(heel, (-11, 16)), add(heel, (-11, 4))], kind="force")
    f.arrow([add(t0, (2, -20)), add(t0, (2, -7.5))], kind="force")
    touch(f, heel)
    touch(f, t0)
    return f


def atlas_knee_bar():
    """Shin wedged between a foothold and a volume on a 40 degree wall."""
    f = tile()
    ang_w = 40
    F = (24, -16)                # far enough right that the thigh shows
    d, n = wall_line(f, ang_w, F)
    hold_side(f, "foot", F, angle=ang_w, size=1.3)
    tip = add(F, add(mul(n, 3.0), mul(d, 2.2)))
    fa, shin_deg, thigh_deg = 20, 150, 230
    dd = ang(fa)
    o = sub(ANKLE, SPOT["tip"])
    ankle = add(tip, add(mul(dd, o[0]), mul(perp(dd), o[1])))
    K = add(ankle, mul(ang(shin_deg), DIM["shin"]))
    hipdir = ang(thigh_deg)
    far = add(K, mul(hipdir, 40))
    leg = dict(fill=WHITE, stroke=INK, sw=0.35)
    f.poly(capsule(far, 6.6, K, 5.0), z=0.2, **leg)
    f.poly(capsule(K, 5.0, ankle, 3.6), z=0.25, **leg)
    sv = ang(shin_deg)                         # cuff where the shin enters
    cuf = add(ankle, mul(sv, 2.4))
    f.line(add(cuf, mul(perp(sv), 3.9)), add(cuf, mul(perp(sv), -3.9)), z=0.26,
           sw=0.3)
    shoe_side(f, tip, fa, spot="tip", up=1)
    check_shoe("atlas knee bar", fa, shin_deg)
    nrm = ang(thigh_deg - 90)
    cpt = add(add(K, mul(hipdir, 9)), mul(nrm, 6.4))
    s_dir = ang(thigh_deg + 180 - 6)
    k_hit = cross(sub(F, cpt), d) / cross(s_dir, d)
    W0 = add(cpt, mul(s_dir, k_hit))
    V = add(cpt, mul(s_dir, -8))
    Vt = add(V, mul(d, 30))
    k_top = cross(sub(F, Vt), d) / cross(s_dir, d)
    W1 = add(Vt, mul(s_dir, k_top + 6))
    f.poly([W0, V, Vt, W1], z=-12, fill=LIGHT, stroke=INK, sw=0.35)
    # the thigh pushes up into the volume: the arrow sits on the volume side
    # of the contact, not across the thigh
    f.arrow([add(cpt, mul(nrm, 2.5)), add(cpt, mul(nrm, 12))], kind="force")
    side = mul(ang(shin_deg - 90), 10)
    f.arrow([add(add(tip, mul(ang(shin_deg), 44)), side),
             add(add(tip, mul(ang(shin_deg), 30)), side)], kind="force")
    touch(f, cpt)
    touch(f, tip)
    return f


def foot_atlas(path):
    rows = [[atlas_toe_edge(), atlas_edge_top(True), atlas_edge_top(False)],
            [atlas_smear_wall(), atlas_smear_volume(), atlas_heel_hook()],
            [atlas_toe_hook(), atlas_cam(), atlas_knee_bar()]]
    grid(rows, path, captions=[
        "toe on an edge", "inside edge (from above)", "outside edge (from above)",
        "smear on the wall", "smear on a volume", "heel hook",
        "toe hook", "heel\u2013toe cam (from behind)", "knee bar"])


def build(out):
    edging(out + "/edging.svg")
    pivoting(out + "/pivoting.svg")
    front_pointing(out + "/front-pointing.svg")
    foot_swap(out + "/foot-swap.svg")
    smearing(out + "/smearing.svg")
    toe_pull(out + "/toe-pull.svg")
    heel_hook(out + "/heel-hook.svg")
    toe_hook(out + "/toe-hook.svg")
    bicycle(out + "/bicycle.svg")
    heel_toe_cam(out + "/heel-toe-cam.svg")
    knee_bar(out + "/knee-bar.svg")
    high_step(out + "/high-step.svg")
    rockover(out + "/rockover.svg")
    hand_foot_match(out + "/hand-foot-match.svg")
    precise_footwork(out + "/precise-footwork.svg")
    foot_atlas(out + "/foot-atlas.svg")
    filmstrip_heel_hook(out + "/filmstrip-heel-hook.svg")
