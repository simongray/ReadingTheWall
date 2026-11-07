"""A climber seen from above, for the plan views in the figures.

A plan view looks straight down on a climber who faces the wall, with the wall
along the top. The climber's left is on the left of the page, as in a back view.
The clothes match the other figures: a white T-shirt, a grey left trouser leg and
half of the seat, a grey left forearm and grey hair.

From above, the higher part covers the lower: the legs go under the pelvis, the
arms come out from under the shoulders and the head is on top.

Points are in centimetres from the middle of the pelvis: x runs to the climber's
right and y toward the wall. Turns are in degrees: a negative turn brings the left
side to the wall and a positive one the right, as `turn` does in climb.py. The
widths come from climb.DIM.

top() draws a back-view Climber from above, to go beside it. It takes all it can
from the back view, and assumes the depth, which a back view can't show, from one
model:

- The middle of the pelvis is `hips` cm from the wall and the middle of the
  shoulders `chest` cm. The shoulders hang further back than the hips, as when the
  arms reach up to holds, so the pelvis shows between the wall and the shoulders.
- The hips and the shoulders turn as far as the back view narrows them: climb.py
  draws a part turned by a at cos a of its width.
- A hand with a target is on the wall, and so is a foot: the hand at the wall, the
  shoe with its toe or edge touching it. A figure names those that are off the wall,
  with how far they are from it.
- An elbow or knee lies between its neighbours. A forearm or shin that the back view
  draws at most 0.8 of its length points away from the wall, as far as that takes.
- A shoe that points into the wall in the back view points into it from above. One
  on its edge lies along the wall, its toe a little in, and one that points down
  shows short.
- The head faces the way the shoulders do, as the back view draws it.

A leg that the back view draws over the other is nearer the viewer, so further from
the wall where the two cross. top() warns when its depths say otherwise.
"""

from climb import *
from closeup import SHOE_TOP, SHOE_TOP_UPPER

# The right half of each outline, from the front round to the back of a climber
# who is square to the wall, in cm from the middle of the part. The skull is a
# little larger than life, as drawings of people from above show it.
SHOULDERS = [(0, 9.0), (7, 9.2), (13, 8.2), (17.5, 6.6), (21.8, 4.6), (23.4, 0),
             (22, -4.6), (17, -7.4), (9, -9.4), (0, -10.2)]
PELVIS = [(0, 9.0), (8, 8.6), (13.6, 6.4), (16.3, 1), (15.5, -5), (10, -9.6), (0, -11)]
SKULL = [(0, 11.2), (5.1, 9.8), (8.1, 5.5), (8.9, 0), (8.0, -5.9), (4.4, -9.9), (0, -11)]
NOSE = [(-2.2, 10.2), (-1.2, 13.0), (0, 14.6), (1.2, 13.0), (2.2, 10.2)]
EAR = [(8.0, 2.8), (10.1, 2.0), (10.4, -0.6), (8.4, -2.0)]
SHOE_ANKLE = 7.0        # the shin enters the shoe this far from its heel
SHOE_RAND = "#bbbbbb"   # the light line where the rubber meets the upper
HAND = [(0, 2.8), (1, 3.9)]
PALM = [(0, 2.2), (0.5, 1.8), (1, 1.1)]     # a hand flat on a wall, side-on
LEG_SLIM = 0.8          # legs a little slimmer than life, which leaves the pelvis clear

OUTLINE = 0.3
INSET_LABEL = 6.5       # pt

HAND_OFF_WALL = 4.0     # the middle of a hand on a hold, from the wall
TOE_IN = 8.0            # a shoe on its edge along the wall points in this much
SHORT = 0.8             # a forearm or shin drawn shorter than this points into the wall


class View:
    """The frame of a plan view. P() turns plan cm into world units, with the middle
    of the pelvis on `at`."""

    def __init__(self, at, s=0.6):
        self.at, self.s = at, s

    def P(self, p):
        return add(self.at, mul(p, self.s))


def wall(f, a, b, depth=3.0, z=70):
    """A wall from above. Its face runs from `a` to `b` in world units, with the
    hatching on the left of that direction."""
    d = norm(sub(b, a))
    n = perp(d)
    f.line(a, b, sw=0.6, z=z)
    k = 0.0
    while k < length(sub(b, a)):
        p = add(a, mul(d, k))
        f.line(p, add(p, add(mul(n, depth), mul(d, 2))), sw=0.18, stroke=MID, z=z)
        k += 2.2


def hold_on(f, view, at, w=17.0, d=5.0, z=69.5):
    """A hold on a wall along the top of the view. `at` is the middle of its base in
    plan cm, and it sticks out `d` cm. The default size is a jug's."""
    pts = [(-w / 2, 0), (w / 2, 0), (w / 2 - 1, -d), (-w / 2 + 1, -d)]
    f.poly([view.P(add(at, p)) for p in pts], z=z, fill=DARK, stroke=INK, sw=0.25)


def turn_arrow(f, view, c, r, a0, a1, z=72.0):
    """A turn arrow round `c` in plan cm, from angle a0 to a1 at a radius of r cm."""
    pts = [view.P(add(c, mul(ang(a0 + (a1 - a0) * i / 8), r))) for i in range(9)]
    f.arrow(pts, kind="turn", z=z, head=1.5)


def _dense(half):
    """A part's closed outline in cm, sampled densely, from its right half."""
    return catmull(half + [(-x, y) for x, y in half[-2:0:-1]], k=5)


def _hull(pts):
    pts = sorted(set(pts))

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and cross(sub(out[-1], out[-2]), sub(p, out[-1])) <= 0:
                out.pop()
            out.append(p)
        return out[:-1]
    return half(pts) + half(pts[::-1])


def _limb(f, view, parts, fill, z, scale=1.0):
    """Overlapping tubes in plan cm, drawn as one silhouette."""
    shapes = [[view.P(p) for p in tube(a, b, ra, rb, scale)] for a, b, ra, rb in parts]
    silhouette(f, shapes, z, fill, sw=OUTLINE)


def _shoe(ankle, deg, side, fore=1.0):
    """map(x, y) from shoe-outline cm to plan cm for a shoe whose ankle is at
    `ankle`, pointing `deg`, its length shortened to `fore`."""
    d = ang(deg)
    heel = sub(ankle, mul(d, SHOE_ANKLE * fore))
    medial = 1 if side == "r" else -1
    return lambda p: add(heel, add(mul(d, p[0] * fore), mul(perp(d), p[1] * medial)))


def _leg(f, view, hip, side, leg, z):
    on = _shoe(leg["ankle"], leg["deg"], side, leg.get("fore", 1.0))
    shoe = [view.P(on(p)) for p in SHOE_TOP]
    f.smooth(shoe, z=z, tension=0.7, fill=SHOE_FILL, stroke=INK, sw=OUTLINE)
    f.smooth([view.P(on(p)) for p in SHOE_TOP_UPPER], z=z + 0.005, tension=0.7, fill=None,
             stroke=SHOE_RAND, sw=0.14)
    # the dotted outline of a shoe that a leg or the body hides, as in the other views
    if leg.get("xray", True):
        f.smooth(shoe, z=z + 0.9, tension=0.7, **XRAY_STYLE)
    fill = LEFT if side == "l" else WHITE
    knee = leg.get("knee", lerp(hip, leg["ankle"], 0.5))
    # from above the thigh lies over the shin, so a bend shows
    _limb(f, view, [(knee, leg["ankle"], SHIN_FRONT, SHIN_BACK)], fill, z + 0.01, LEG_SLIM)
    _limb(f, view, [(hip, knee, THIGH_FRONT, THIGH_BACK)], fill, z + 0.03, LEG_SLIM)


def _arm(f, view, sh, side, arm, z):
    hand = arm["hand"]
    el = arm.get("elbow", lerp(sh, hand, 0.54))
    tips = arm.get("flat")
    wr = hand if tips else lerp(el, hand, 0.86)
    palm = (wr, tips, PALM, PALM) if tips else (wr, hand, HAND, HAND)
    _limb(f, view, [(sh, el, UPPER_ARM_OUT, UPPER_ARM_IN), (el, wr, FORE_RADIAL, FORE_ULNAR), palm],
          LEFT if side == "l" else WHITE, z)
    sleeve = tube(sh, lerp(sh, el, SLEEVE_LEN), SLEEVE, SLEEVE, cap2=0)
    f.poly([view.P(p) for p in sleeve], z=z + 0.02, fill=WHITE, stroke=INK, sw=OUTLINE)


def climber(f, view, hips=0.0, chest=None, lean=(0.0, -20.0), arms=None, legs=None, z=70.0):
    """Draw a climber from above in a View. top() works this out from a back view;
    call it directly only for a view that has none, such as a corner.

    hips, chest: how far the pelvis and the shoulders turn. The chest follows the
      hips unless you set it, and the head faces the way the chest does.
    lean: the middle of the shoulders in plan cm.
    arms: {"l": arm, "r": arm}, each a dict with the `hand` in plan cm and its `elbow`
      (by default halfway). With `flat`, the fingertips of a hand pressed flat on a
      wall, `hand` is the wrist.
    legs: {"l": leg, "r": leg}, each a dict with the shoe's `ankle` in plan cm, its
      heel-to-toe direction `deg`, its length `fore` as a share of the whole (1 by
      default; less for a shoe that points down), its `knee` (by default halfway) and
      `z`, which puts one leg over the other. xray=False leaves out the dotted
      outline of a hidden shoe."""
    chest = hips if chest is None else chest
    head_c = add(lean, rot((0, 2.5), chest))
    for side, sgn in (("l", -1), ("r", 1)):
        if legs and side in legs:
            _leg(f, view, rot((sgn * DIM["hip_half"], 0), hips), side, legs[side],
                 legs[side].get("z", z))
    # the left half of the seat is grey, as in the other views
    seat = _dense(PELVIS)
    outline = [view.P(rot(p, hips)) for p in seat]
    f.poly(outline, z=z + 0.2, fill=WHITE, stroke=None)
    f.poly([view.P(rot(p, hips)) for p in seat if p[0] <= 0.001], z=z + 0.21,
           fill=LEFT, stroke=None)
    f.poly(outline, z=z + 0.22, fill=None, stroke=INK, sw=OUTLINE)
    # the T-shirt runs from the waist to the shoulders and covers the back of the pelvis
    torso = _hull(ellipse_pts(lerp((0, 0), lean, 0.5), 11.5, 5.5, (hips + chest) / 2,
                              n=18) + ellipse_pts(lean, 15, 7.5, chest, n=18))
    f.poly([view.P(p) for p in torso], z=z + 0.3, fill=WHITE, stroke=INK, sw=OUTLINE)
    for side, sgn in (("l", -1), ("r", 1)):
        if arms and side in arms:
            _arm(f, view, add(lean, rot((sgn * DIM["sh_half"], 0), chest)), side, arms[side],
                 z + 0.35)
    # the arms are higher and cover the pelvis, so its outline shows dotted through
    # them, as the other views show a hidden shoe
    if arms:
        f.poly(outline, z=z + 0.37, **XRAY_STYLE)
    f.poly([view.P(add(lean, rot(p, chest))) for p in _dense(SHOULDERS)], z=z + 0.4,
           fill=WHITE, stroke=INK, sw=OUTLINE)
    # the nose and ears show which way the head faces
    for pts in (NOSE, EAR, [(-x, y) for x, y in EAR]):
        q = [add(head_c, rot(p, chest)) for p in pts]
        f.poly([view.P(p) for p in catmull(q, closed=False, k=4) + [q[-1]]], z=z + 0.5,
               fill=WHITE, stroke=INK, sw=0.22, taper=False)
    f.poly([view.P(add(head_c, rot(p, chest))) for p in _dense(SKULL)], z=z + 0.6,
           fill=HAIR, stroke=INK, sw=OUTLINE)


def _turned(w, turn):
    """The turn in degrees of a part that a back view draws at `w` of its width."""
    return math.copysign(math.degrees(math.acos(max(-1.0, min(1.0, w)))), turn) if turn else 0.0


def _behind(name, c, legs, P):
    """Warn when the leg that the back view draws over the other is not further from
    the wall where the two cross."""
    order = c.order or (["rleg", "torso", "lleg"] if c.turn > 0.15 else ["lleg", "rleg"])
    if "lleg" not in order or "rleg" not in order:
        return
    front = "l" if order.index("lleg") > order.index("rleg") else "r"
    back = "r" if front == "l" else "l"

    def chain(s, J):
        return [J[s + "hip"], J[s + "kn"], J[s + "an"]]

    def at(pts, t):
        i = min(int(t * 2), 1)
        return lerp(pts[i], pts[i + 1], t * 2 - i)
    ts = [i / 40 for i in range(41)]
    gap, t1, t2 = min((length(sub(at(chain(front, c.J), a), at(chain(back, c.J), b))), a, b)
                      for a in ts for b in ts)
    if gap > 6:
        return          # the legs don't cross in the back view
    yf = at([P[front + "hip"], legs[front]["knee"], legs[front]["ankle"]], t1)[1]
    yb = at([P[back + "hip"], legs[back]["knee"], legs[back]["ankle"]], t2)[1]
    if yf > yb - 2:
        print(f"{name}: from above the {front} leg should be behind the {back} leg")


def top(f, c, at, s=0.6, hips=20.0, chest=40.0, off=None, shoes=None, joints=None,
        span=(-40, 40), spin=None, label="from above", label_at=None, name="top"):
    """Draw the back-view climber `c` from above, as an inset beside it, by the model in
    this module's notes. Returns the View and the plan points of the joints.

    at: where the middle of the pelvis goes, in world units.
    hips, chest: how far the middle of the pelvis and of the shoulders are from the
      wall, in cm.
    off: the hands and feet that are off the wall, and any elbow or knee placed by
      hand, as {joint: cm from the wall} with c.J's names, e.g. {"rha": 8, "lan": 30}.
    shoes: {side: deg}, the direction of a shoe from above, where the model's guess
      won't do.
    joints: back-view points that c doesn't hold, such as an elbow drawn with
      draw_arm(), as {name: (x, y)} in world units.
    span: where the wall starts and ends, as x in plan cm.
    spin: a turn arrow (about, r, a0, a1) round the joint `about` ("pelvis", or a hand
      such as "lha", which then gets a black dot as the hinge), at r cm from angle a0
      to a1.
    label_at: where the label goes, in world units (by default under the inset)."""
    J = dict(c.J, **(joints or {}))
    off = off or {}
    shoes = shoes or {}
    W = hips                                  # the wall, in plan y
    px = c.pelvis[0]

    def x(j):
        return J[j][0] - px
    h_turn, c_turn = _turned(c.hip_w, c.turn), _turned(c.sh_w, c.turn)
    lean = (x("sh_c"), W - chest)
    P = {"pelvis": (0.0, 0.0), "sh_c": lean}
    for side, sgn in (("l", -1), ("r", 1)):
        P[side + "sh"] = add(lean, rot((sgn * DIM["sh_half"], 0), c_turn))
        P[side + "hip"] = rot((sgn * DIM["hip_half"], 0), h_turn)

    def middle(j, a, b, outer, f_len):
        """The plan point of elbow or knee `j` between joints a and b."""
        if j in off:
            return (x(j), W - off[j])
        if f_len <= SHORT:
            return (x(j), P[b][1] - outer * math.sqrt(1 - f_len ** 2))
        la, lb = length(sub(J[j], J[a])), length(sub(J[b], J[j]))
        return (x(j), lerp(P[a], P[b], la / (la + lb))[1])

    arms, legs, holds = {}, {}, []
    for side in "lr":
        ha = side + "ha"
        if getattr(c, side + "h") is not None or ha in (joints or {}):
            P[ha] = (x(ha), W - off.get(ha, HAND_OFF_WALL))
            if ha not in off:
                holds.append(P[ha][0])
            P[side + "el"] = middle(side + "el", side + "sh", ha,
                                    c.D["forearm"] + c.D["hand"], c.arm_factors(side)[1])
            arms[side] = dict(hand=P[ha], elbow=P[side + "el"])
        # a hanging arm is hidden under its shoulder
        ft, an = getattr(c, "_" + side + "f"), side + "an"
        a = ft["angle"]
        back = ft["style"] == "back"
        deg = shoes.get(side, 90.0 if back else TOE_IN if math.cos(math.radians(a)) >= 0
                        else 180.0 - TOE_IN)
        fore = 1.0 if back else max(0.4, abs(math.cos(math.radians(a))))
        if an in off:
            P[an] = (x(an), W - off[an])
        else:
            # the shoe touches the wall
            on = _shoe((x(an), 0.0), deg, side, fore)
            P[an] = (x(an), W - 0.4 - max(on(p)[1] for p in SHOE_TOP))
        lf = c.leg_len[side]
        P[side + "kn"] = middle(side + "kn", side + "hip", an, c.D["shin"],
                                lf[1] if isinstance(lf, tuple) else 1.0)
        legs[side] = dict(ankle=P[an], deg=deg, fore=fore, knee=P[side + "kn"])
    # the leg with the higher knee is on top
    hi = max("lr", key=lambda s: J[s + "kn"][1])
    for side in "lr":
        legs[side]["z"] = 70.0 + (0.05 if side == hi else 0.0)
    _behind(name, c, legs, P)

    view = View(at, s)
    wall(f, view.P((span[0], W)), view.P((span[1], W)))
    for hx in holds:
        hold_on(f, view, (hx, W))
    climber(f, view, h_turn, c_turn, lean=lean, arms=arms, legs=legs)
    if spin:
        about, r, a0, a1 = spin
        turn_arrow(f, view, P[about], r, a0, a1)
        if about != "pelvis":
            f.circle(view.P(P[about]), 1.5, z=72, fill=INK, stroke=None)
    if label:
        lowest = min(view.P(p)[1] for p in P.values())
        f.text(label, label_at or (at[0], lowest - 9), size=INSET_LABEL)
    return view, P
