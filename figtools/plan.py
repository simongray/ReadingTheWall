"""A climber seen from above, for the plan views in the figures.

A plan view looks straight down on a climber who faces the wall, with the wall
along the top. The climber's left is on the left of the page, as in a back view.
The clothes match the other figures: a white T-shirt, a grey left trouser leg and
half of the seat, a grey left forearm and grey hair.

From straight above, the shoulders would hide the pelvis. So the climber leans out
from the hips, which keeps the pelvis in view between the wall and the shirt. A
figure draws arms and legs only where it needs them.

Points are in centimetres from the middle of the pelvis: x runs to the climber's
right and y toward the wall. Turns are in degrees: a negative turn brings the left
side to the wall and a positive one the right. The widths come from climb.DIM.
"""

from climb import *
from closeup import SHOE_TOP, SHOE_TOP_UPPER

# The right half of each outline, from the front round to the back of a climber
# who is square to the wall, in cm from the middle of the part.
SHOULDERS = [(0, 9.0), (7, 9.2), (13, 8.2), (17.5, 6.6), (21.8, 4.6), (23.4, 0),
             (22, -4.6), (17, -7.4), (9, -9.4), (0, -10.2)]
PELVIS = [(0, 9.0), (8, 8.6), (13.6, 6.4), (16.3, 1), (15.5, -5), (10, -9.6), (0, -11)]
SKULL = [(0, 10.2), (4.6, 8.9), (7.3, 5), (8, 0), (7.2, -5.4), (4, -9), (0, -10)]
NOSE = [(-2.0, 9.2), (-1.1, 11.9), (0, 13.4), (1.1, 11.9), (2.0, 9.2)]
EAR = [(7.2, 2.6), (9.2, 1.8), (9.5, -0.6), (7.6, -1.8)]
SHOE_ANKLE = 7.0        # the shin enters the shoe this far from its heel
SHOE_RAND = "#bbbbbb"   # the light line where the rubber meets the upper
HAND = [(0, 2.8), (1, 3.9)]
PALM = [(0, 2.2), (0.5, 1.8), (1, 1.1)]     # a hand flat on a wall, side-on
LEG_SLIM = 0.8          # legs a little slimmer than life, which leaves the pelvis clear

OUTLINE = 0.3
GHOST_STYLE = dict(stroke=GHOST_LINE, sw=OUTLINE, dash=(0.9, 0.7))
INSET_LABEL = 6.5       # pt


class View:
    """The frame of a plan view. P() turns plan cm into world units. The middle of
    the pelvis lands on `at`, and the whole drawing can swing by `swing` degrees
    about `pivot`, a point in plan cm."""

    def __init__(self, at, s=0.6, pivot=(0.0, 0.0), swing=0.0):
        self.at, self.s, self.pivot, self.swing = at, s, pivot, swing

    def P(self, p):
        q = add(self.pivot, rot(sub(p, self.pivot), self.swing))
        return add(self.at, mul(q, self.s))


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


def _limb(f, view, parts, fill, z, scale=1.0, ghost=False):
    """Overlapping tubes in plan cm, drawn as one silhouette."""
    shapes = [[view.P(p) for p in tube(a, b, ra, rb, scale)] for a, b, ra, rb in parts]
    if ghost:
        silhouette(f, shapes, z, WHITE, stroke=GHOST_LINE, sw=OUTLINE, dash=GHOST_STYLE["dash"])
    else:
        silhouette(f, shapes, z, fill, sw=OUTLINE)


def _leg(f, view, hip, side, leg, z):
    d = ang(leg["deg"])
    ankle = add(leg["heel"], mul(d, SHOE_ANKLE))
    medial = 1 if side == "r" else -1

    def on_shoe(pts):
        return [view.P(add(leg["heel"], add(mul(d, x), mul(perp(d), y * medial)))) for x, y in pts]
    shoe = on_shoe(SHOE_TOP)
    f.smooth(shoe, z=z, tension=0.7, fill=SHOE_FILL, stroke=INK, sw=OUTLINE)
    f.smooth(on_shoe(SHOE_TOP_UPPER), z=z + 0.005, tension=0.7, fill=None, stroke=SHOE_RAND, sw=0.14)
    # the dotted outline of a shoe that a leg or the body hides, as in the other views
    if leg.get("xray", True):
        f.smooth(shoe, z=z + 0.9, tension=0.7, **XRAY_STYLE)
    fill = LEFT if side == "l" else WHITE
    if "knee" in leg:
        # a bent leg: from above the thigh lies over the shin, so the bend shows
        _limb(f, view, [(leg["knee"], ankle, SHIN_FRONT, SHIN_BACK)], fill, z + 0.01, LEG_SLIM)
        _limb(f, view, [(hip, leg["knee"], THIGH_FRONT, THIGH_BACK)], fill, z + 0.03, LEG_SLIM)
    else:
        knee = lerp(hip, ankle, 0.5)
        _limb(f, view, [(hip, knee, THIGH_FRONT, THIGH_BACK), (knee, ankle, SHIN_FRONT, SHIN_BACK)],
              fill, z + 0.01, LEG_SLIM)


def _arm(f, view, sh, side, arm, z, ghost=False):
    if not isinstance(arm, dict):
        arm = dict(hand=arm)
    hand = arm["hand"]
    el = arm.get("elbow", lerp(sh, hand, 0.54))
    tips = arm.get("flat")
    wr = hand if tips else lerp(el, hand, 0.86)
    palm = (wr, tips, PALM, PALM) if tips else (wr, hand, HAND, HAND)
    _limb(f, view, [(sh, el, UPPER_ARM_OUT, UPPER_ARM_IN), (el, wr, FORE_RADIAL, FORE_ULNAR), palm],
          LEFT if side == "l" else WHITE, z, ghost=ghost)
    if not ghost:
        sleeve = tube(sh, lerp(sh, el, SLEEVE_LEN), SLEEVE, SLEEVE, cap2=0)
        f.poly([view.P(p) for p in sleeve], z=z + 0.02, fill=WHITE, stroke=INK, sw=OUTLINE)


def climber(f, view, hips=0.0, chest=None, head=None, lean=(0.0, -23.0), arms=None,
            legs=None, ghost=False, pelvis=True, z=70.0):
    """Draw a climber from above in a View.

    hips, chest, head: how far the pelvis, shoulders and head turn. The chest follows
      the hips and the head follows the chest unless you set them.
    lean: the middle of the shoulders in plan cm.
    arms: {"l": hand, "r": hand}. Each is a point in plan cm or a dict with `hand` and
      `elbow`. With `flat`, the fingertips of a hand pressed flat on a wall, `hand` is
      the wrist.
    legs: {"l": leg, "r": leg}. Each is a dict with the shoe's `heel` in plan cm, its
      heel-to-toe direction `deg`, and `knee` (by default halfway, so the leg is straight).
      xray=False leaves out the dotted outline of a hidden shoe.
    ghost: draw the body and arms as one dashed outline and dashed lines, for an earlier
      position.
    pelvis=False: the view from straight above, with the shoulders over the pelvis and
      hiding it. Set lean to (0, 0) for it. A ghost then keeps its head and the shape of
      its arms."""
    chest = hips if chest is None else chest
    head = chest if head is None else head
    head_c = add(lean, rot((0, 2.5), head))
    if ghost and not pelvis:
        for side, sgn in (("l", -1), ("r", 1)):
            if arms and side in arms:
                _arm(f, view, add(lean, rot((sgn * DIM["sh_half"], 0), chest)), side,
                     arms[side], z, ghost=True)
        for part, c, turn in ((SHOULDERS, lean, chest), (SKULL, head_c, head)):
            f.poly([view.P(add(c, rot(p, turn))) for p in _dense(part)], z=z + 0.1,
                   fill=WHITE, **GHOST_STYLE)
        return
    if ghost:
        body = [rot(p, hips) for p in _dense(PELVIS)]
        body += [add(lean, rot(p, chest)) for p in _dense(SHOULDERS)]
        f.poly([view.P(p) for p in _hull(body)], z=z, fill=WHITE, **GHOST_STYLE)
        for side, sgn in (("l", -1), ("r", 1)):
            if arms and side in arms:
                sh = add(lean, rot((sgn * DIM["sh_half"], 0), chest))
                f.line(view.P(sh), view.P(arms[side]), z=z + 0.1, **GHOST_STYLE)
        return
    for side, sgn in (("l", -1), ("r", 1)):
        if legs and side in legs:
            _leg(f, view, rot((sgn * DIM["hip_half"], 0), hips), side, legs[side], z)
    if pelvis:
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
    f.poly([view.P(add(lean, rot(p, chest))) for p in _dense(SHOULDERS)], z=z + 0.4,
           fill=WHITE, stroke=INK, sw=OUTLINE)
    # the nose and ears show which way the head faces
    for pts in (NOSE, EAR, [(-x, y) for x, y in EAR]):
        q = [add(head_c, rot(p, head)) for p in pts]
        f.poly([view.P(p) for p in catmull(q, closed=False, k=4) + [q[-1]]], z=z + 0.5,
               fill=WHITE, stroke=INK, sw=0.22, taper=False)
    f.poly([view.P(add(head_c, rot(p, head))) for p in _dense(SKULL)], z=z + 0.6,
           fill=HAIR, stroke=INK, sw=OUTLINE)


def hips(f, at, deg, chest=None, head=None, to_wall=26.0, s=0.6, lean=(0.0, -23.0), legs=None,
         spin=None, span=(-36.0, 36.0), label="hips from above", label_dx=0.0, *, label_y):
    """An inset of the hips from above, with the pelvis `to_wall` cm from the wall.

    at: the middle of the pelvis in world units.
    deg, chest, head, lean, legs: as for climber(), where `deg` is its `hips`.
    spin: a turn arrow round the pelvis, as (radius, from angle, to angle).
    span: where the wall starts and ends, as x in plan cm.
    label_y, label_dx: the height of the label, and how far it sits from the middle of
      the pelvis, in world units."""
    view = View(at, s)
    wall(f, view.P((span[0], to_wall)), view.P((span[1], to_wall)))
    climber(f, view, deg, chest, head, lean=lean, legs=legs)
    if spin:
        turn_arrow(f, view, (0, 0), *spin)
    f.text(label, (at[0] + label_dx, label_y), size=INSET_LABEL)


# climb.py turns a back view by up to this many degrees, at turn = ±1
TURN_DEG = 70.0


def from_back(f, c, hinge, hold="l", s=0.6, depth=28.0, reach=None, feet=None, swing="open",
              span=(12, 56), label="from above", label_at=None):
    """An inset of the back-view climber `c` seen from straight above, to go beside it.

    The sideways positions of the shoulders, hands and feet come from c, and the turn
    of the body from c.turn. A back view has no depth, so a hand on a hold is at the
    wall, the middle of the shoulders is `depth` cm from it and the turn sets how far
    each shoulder is. The shoulders hide the hips, as from straight above.

    hinge: where the holding hand `hold` goes, in world units. It is a black dot.
    reach: how far the other hand is from the wall, in cm (by default level with the
      shoulders). A hand that hangs is left out.
    feet: {"l": deg} draws that leg with its foot on the wall, the shoe pointing `deg`.
    swing: "open" or "back", a turn arrow about the hinge for the free side.
    span: how far the wall runs past the hinge on its outer side and on the body's
      side, in cm.
    label_at: where the label goes, from the hinge in world units."""
    sgn = -1 if hold == "l" else 1
    sx = c.J["sh_c"][0]
    turn = c.turn * TURN_DEG

    def on_plan(p, from_wall):
        return (p[0] - sx, depth - from_wall)
    h = on_plan(c.J[hold + "ha"], 4.0)
    arms = {hold: h}
    other = "r" if hold == "l" else "l"
    if getattr(c, other + "h") is not None:
        arms[other] = on_plan(c.J[other + "ha"], depth if reach is None else reach)
    legs = {}
    for side, deg in (feet or {}).items():
        ankle = on_plan(c.J[side + "an"], 4.5)
        legs[side] = dict(heel=sub(ankle, mul(ang(deg), SHOE_ANKLE)), deg=deg, xray=False)
    view = View(sub(hinge, mul(h, s)), s)
    x0, x1 = sorted((h[0] + span[0] * sgn, h[0] - span[1] * sgn))
    wall(f, view.P((x0, depth)), view.P((x1, depth)))
    hold_on(f, view, (h[0], depth))
    climber(f, view, turn, lean=(0.0, 0.0), arms=arms, legs=legs, pelvis=False, z=70.7)
    f.circle(hinge, 1.5, z=72, fill=INK, stroke=None)
    # the arc runs round the hinge just outside the free shoulder, the way it swings
    v = sub(rot((-sgn * DIM["sh_half"], 0.0), turn), h)
    a_sh = math.degrees(math.atan2(v[1], v[0]))
    a0, a1 = a_sh + 6 * sgn, a_sh + 38 * sgn
    turn_arrow(f, view, h, length(v) + 14, *((a0, a1) if swing == "open" else (a1, a0)))
    f.text(label, add(hinge, label_at or (-sgn * 14, -(60 * s + 4))), size=INSET_LABEL)
