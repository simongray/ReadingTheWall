"""Hands drawn by hand, as an illustrator would: each hand is one outline
written as control points in cm, in the figure's own coordinates, against the
hold it grips, with the climbers' smoothing and pen (Fig._smooth_pts,
Fig._path_d). No model and no pose solver.

The proportions, in cm of a hand 19 cm long (research/hand-proportions.md has their
sources, and tools/check_hands.py tests every hand against them), for a straight
side view: knuckles 3.3 deep, palm with the ball of the thumb 4.6-4.9, wrist
4.2-4.4, forearm 4.8-5.1 a hand's width down. First finger segment 1.9, middle
1.65, end 1.4; segments 4.25, 2.45, 2.35. Thumb 2.05 wide and 5-5.5 free. Knuckle
to wrist crease 9.1. From the back: knuckles 8.5, wrist 6.2-6.6, forearm 6.9-7.2, crease
to webs 9.9-10.9, middle finger 7.4 from its web, thumb 5 from its web. There is
no view tilt: a tilt adds palm and no finger.

Side views have the wall on the right, as in the climber side views, and show the
hand from the thumb side (the pocket from the little-finger side). Back views look at
the wall, so the back of the hand faces you. Pinches are seen from above, with the wall
at the top.

A hand is a dict:
  outline   closed loops of control points: the silhouette, then any gaps in it.
            A third value in a point breaks the curve there: 1 for a corner, KEEP in a
            bend too tight for the pen (loop_d).
  grey      what lies behind: [(fill, points)], under the outline. In a straight side
            view the index hides the fingers behind it, so grey shows only where
            one really would show: a fingertip past the index's, the fingers in
            a pocket or a flake. Never a band along the back of the hand, which
            reads as a doubled outline.
  lines     inner lines at outline weight, fading toward the last point
  solid     inner lines at outline weight that end on other lines, no fading
  marks     the slight details at the climbers' hem weight, tapered
  joints    where the joints lie: for the angle arcs, the labels and measuring
"""

import math

from climb import *
from climb import _bezier_d, _chaikin_open, _resample, PEN_OUTLINE, combine, wall_side, filmstrip
import hand as H
from hand import WX

OUT = 0.32              # the climbers' outline: drawn at twice this, with their fill over half
FINE = H.DETAIL         # the climbers' hem
GREY = H.BACK_FILLS[0]
GREY2 = H.BACK_FILLS[1]
TENSION = 1.0
KEEP = 2                # third value of a control point the pen must not thin away
ARM_WOBBLE, ARM_FROM, ARM_RAMP = 0.3, 1.0, 2.0
SHOW_MARKS = [True]     # off while measuring


def curve(f, pts, closed=True):
    """The curve through control points, sharp at points marked as corners."""
    P = [(p[0], p[1]) for p in pts]
    C = [len(p) > 2 for p in pts]
    if not any(C):
        return f._smooth_pts(P, closed, TENSION)
    if closed:
        i = C.index(True)
        P, C = P[i:] + P[:i] + [P[i]], C[i:] + C[:i] + [True]
    out, start = [], 0
    for j in range(1, len(P)):
        if C[j] or j == len(P) - 1:
            out += f._smooth_pts(P[start:j + 1], False, TENSION)[:-1]
            start = j
    if not closed:
        out.append(P[-1])
    return out


def loop_d(f, pts):
    """The pen's path for a closed loop. Fig._page keeps a point only every 0.8 mm, which
    would spoil a bend as tight as a web. So this draws the loop in pieces that start and
    end at the points marked KEEP."""
    S = curve(f, pts)
    cut = sorted(S.index(p[:2]) for p in pts if len(p) > 2 and p[2] == KEEP)
    if not cut:
        return f._path_d(S, True, False)
    S = S[cut[0]:] + S[:cut[0]] + [S[cut[0]]]
    cut = [i - cut[0] for i in cut] + [len(S) - 1]
    P, C = [], []
    for i, j in zip(cut, cut[1:]):
        p, c = f._page(S[i:j + 1], False, False)
        P += p[:-1]
        C += [False] + c[1:-1]
    return _bezier_d(P, C, True, f._dec())


def path(f, loops):
    return " ".join(loop_d(f, q) for q in loops)


def arm_wobble(hand):
    """The share of the pen's wobble this hand's outline keeps at a point. A close-up's
    forearm runs longer on paper than a climber's, long enough for the waves to read as
    a wavy edge. So the outline keeps all of it down to ARM_FROM cm below the wrist crease
    and ARM_WOBBLE of it from ARM_FROM + ARM_RAMP on."""
    j = hand.get("joints")
    if not j:
        return None
    u = norm(j["arm_dir"])

    def at(p):
        s = max(0.0, min(1.0, (-dot(sub(p, j["crease"]), u) - ARM_FROM) / ARM_RAMP))
        return 1 - (1 - ARM_WOBBLE) * s * s * (3 - 2 * s)
    return at


def pen_line(f, pts, z, sw, fade=3.5):
    """An inner line through pts, wobbling with the outline: full weight,
    narrowing to a point over the last `fade` mm (no narrowing with fade=0)."""
    P, _ = f._page(curve(f, pts, False), False, True)
    P = _chaikin_open(P, 2)
    Q = _resample(P, min(f.mm(0.5), 0.3))
    s = [0.0]
    for a, b in zip(Q, Q[1:]):
        s.append(s[-1] + length(sub(b, a)))
    w = f.mm(f.weight(sw)) / 2
    T = min(f.mm(fade), s[-1] * 0.95) if fade else 0.0
    L, R = [], []
    for i, q in enumerate(Q):
        n = perp(norm(sub(Q[min(i + 1, len(Q) - 1)], Q[max(i - 1, 0)])))
        hw = max(w * min(1.0, (s[-1] - s[i]) / T), 0.004) if T else w
        L.append(add(q, mul(n, hw)))
        R.append(add(q, mul(n, -hw)))
    ring = L + R[::-1]
    # square at the start, or the smoothing rounds it out into a bead on the line
    corner = [i in (0, len(ring) - 1) for i in range(len(ring))]
    d = _bezier_d(ring, corner, True, f._dec())
    f.add(f'<path d="{d}" fill="{INK}"/>', z)


def fine_sw():
    """The hem's weight whatever the plate's zoom (Fig.weight thickens lines
    from 0.28 mm up, which a reduced plate reaches)."""
    v = FINE * H.LINE[0]
    return v / PEN_OUTLINE if v / PEN_OUTLINE >= 0.28 else v


def draw_hand(f, hand, z=0.0, fill=WHITE, ghost=False):
    """Draw one authored hand on figure f. ghost: only its dashed outline with no fill, so
    the hold still shows, for where the hand was (a hand that has moved on, or would not
    fit)."""
    k = H.LINE[0]
    sil = list(hand["outline"][0])
    # the arm leaves the frame: no curve round the two points below it
    if not hand.get("whole"):
        sil[0], sil[-1] = (*sil[0][:2], 1), (*sil[-1][:2], 1)
    f.wobble = arm_wobble(hand)
    d = path(f, [sil] + list(hand["outline"][1:]))
    f.wobble = None
    if ghost:
        st = f.style(fill=None, stroke=MID, sw=0.3, dash=(0.9, 0.7))
        f.add(f'<path d="{d}" fill-rule="evenodd" {st}/>', z)
        return
    for i, (g, pts) in enumerate(hand.get("grey", ())):
        zg = z + 0.002 * i
        f.add(f'<path d="{path(f, [pts])}" fill-rule="evenodd" fill="{g}"/>', zg)
        f.add(f'<path d="{path(f, [pts])}" {f.style(fill=None, stroke=INK, sw=fine_sw())}/>',
              zg + 0.001)
    st = f.style(fill=fill, stroke=INK, sw=OUT * k)
    f.add(f'<path d="{d}" fill-rule="evenodd" {st}/>', z + 0.01)
    for pts in hand.get("solid", ()):
        pen_line(f, pts, z + 0.02, OUT * k, fade=0)
    for pts in hand.get("lines", ()):
        pen_line(f, pts, z + 0.02, OUT * k)
    if SHOW_MARKS[0]:
        for pts in hand.get("marks", ()):
            f.poly(curve(f, pts, False), closed=False, z=z + 0.03, taper=True, _smooth=True,
                   fill=None, stroke=INK, sw=fine_sw())


def nail(tip, toward, w=1.12, L=1.12, off=0.0, back=0.3):
    """A nail on a digit whose back faces you: an open U with a round base, open at the
    free edge, `back` short of the digit's end at `tip`. toward: the way the digit
    points; off: sideways, for a digit seen a little from one side."""
    a = norm(toward)
    n = (a[1], -a[0])
    c = add(tip, mul(n, off))

    def at(s, t):
        return add(add(c, mul(a, -back - s)), mul(n, t * w / 2))
    return [at(0.0, -0.94), at(0.5 * L, -1.0), at(0.84 * L, -0.74), at(L, -0.26), at(L, 0.26), at(0.84 * L, 0.74),
            at(0.5 * L, 1.0), at(0.0, 0.94)]


def side_nail(a, b, inward, depth=0.3):
    """A nail seen from the side: a short closed sliver whose ends lie on the digit's
    outline, from a at the root of the nail to b at its free edge. inward: a point
    inside the digit, which says which way the sliver bulges."""
    u = sub(b, a)
    n = norm((-u[1], u[0]))
    if dot(n, sub(inward, a)) < 0:
        n = mul(n, -1.0)

    def at(t, h):
        return add(add(a, mul(u, t)), mul(n, h * depth))
    return [a, at(0.16, 0.8), at(0.42, 1.0), at(0.74, 0.86), b]


def moved(hand, dx=0.0, dy=0.0, deg=0.0, about=(0.0, 0.0), mirror=False):
    """A copy of a hand, reflected in x = 0 if asked, turned by deg about `about`,
    then moved."""
    def pt(p):
        q = (-p[0], p[1]) if mirror else (p[0], p[1])
        q = add(about, rot(sub(q, about), deg))
        q = (q[0] + dx, q[1] + dy)
        return (*q, *p[2:])

    def vec(v):
        return rot((-v[0], v[1]) if mirror else v, deg)
    out = dict(hand)
    out["outline"] = [[pt(p) for p in q] for q in hand["outline"]]
    out["grey"] = [(g, [pt(p) for p in q]) for g, q in hand.get("grey", ())]
    for key in ("lines", "solid", "marks"):
        out[key] = [[pt(p) for p in q] for q in hand.get(key, ())]
    if "joints" in hand:
        j = dict(hand["joints"])
        for key in ("i", "m", "r", "l", "t"):
            if key in j:
                j[key] = [pt(p) for p in j[key]]
        for key in ("crease", "wrist", "dent", "label"):
            if key in j:
                j[key] = pt(j[key])
        for key in ("hand_dir", "arm_dir", "across"):
            if key in j:
                j[key] = vec(j[key])
        out["joints"] = j
    return out


def finger(chain, w0, w1):
    """A straight-on finger as one clean taper with no bulges at its joints: control
    points up its right side, round its end and down its left. chain: root, any joints,
    end. w0, w1: its half-width at the root and just short of the end."""
    seg = [length(sub(b, a)) for a, b in zip(chain, chain[1:])]
    total = sum(seg)
    end = chain[-1]

    def at(d):
        for i, L in enumerate(seg):
            if d <= L or i == len(seg) - 1:
                return lerp(chain[i], chain[i + 1], d / L), norm(sub(chain[i + 1], chain[i]))
            d -= L
    a = total - 1.25 * w1
    stations = []
    for t in (0.0, 0.5, 1.0):
        p, u = at(a * t)
        stations.append((p, u, w0 + (w1 - w0) * t))
    r = [add(p, mul((u[1], -u[0]), w)) for p, u, w in stations]
    l = [sub(p, mul((u[1], -u[0]), w)) for p, u, w in stations]
    d = stations[-1][1]
    n = (d[1], -d[0])
    back = sub(end, mul(d, 0.3 * w1))
    return r + [add(back, mul(n, 0.74 * w1)), end, sub(back, mul(n, 0.74 * w1))] + l[::-1]


# ---------------------------------------------------------------- half crimp
#
# The first segment stands up, the middle and end segments lie on the edge,
# straight. The wrist is bent back a little, which is how you hang on an edge
# and which shows you where the hand ends.

HALF = dict(
    outline=[[
        # the forearm's back, going up to the wrist
        (-6.85, -21.0), (-6.4, -18.4), (-5.85, -16.2), (-5.42, -14.5), (-5.2, -13.3),
        # the back of the hand, a low arch up to the knuckle
        (-5.22, -12.2), (-5.32, -11.0), (-5.5, -9.0), (-5.62, -7.0), (-5.68, -5.0),
        (-5.64, -3.8),
        # the knuckle turns into the first segment
        (-5.42, -2.8), (-5.12, -1.8), (-4.98, -0.6), (-4.88, 0.35), (-4.55, 1.2), (-3.85, 1.68),
        # along the top of the two straight segments to the tip
        (-2.7, 1.66), (-1.4, 1.54), (-0.2, 1.45), (0.6, 1.32), (1.15, 0.98), (1.3, 0.55),
        (1.0, 0.15),
        # the pad and the underside, back to the crook
        (0.3, 0.0), (-0.8, 0.02), (-1.6, -0.03), (-2.4, -0.08), (-2.85, -0.36),
        # the first segment's palm side, to the thumb's tip
        (-3.04, -0.9), (-3.12, -1.72, 1),
        # round the thumb's tip and down its outer edge, which is the palm's
        (-2.86, -1.3), (-2.46, -1.14), (-2.0, -1.4), (-1.7, -1.95), (-1.54, -2.6), (-1.34, -3.4), (-1.15, -4.6),
        (-1.0, -6.0), (-0.8, -7.4),
        # the ball of the thumb, then in to the wrist
        (-0.62, -9.0), (-0.7, -10.6), (-0.85, -11.8), (-1.0, -12.7),
        # the forearm's front
        (-0.98, -14.0), (-1.02, -16.0), (-1.2, -18.4), (-1.6, -21.0),
    ]],
    lines=[
        # the thumb's inner edge, from the fork at its tip down into the palm
        [(-3.12, -1.72), (-3.44, -2.3), (-3.5, -3.1), (-3.36, -4.2), (-3.12, -5.4),
         (-2.9, -6.6)],
    ],
    marks=[
        # index nail, a sliver along the back of the end segment
        [(-0.3, 1.45), (-0.12, 1.17), (0.4, 1.08), (0.85, 1.07), (1.05, 1.1)],
        nail((-2.48, -1.14), (-0.1, 0.99), w=1.06, L=1.04, off=0.02, back=0.46),
        # the wrist, from the palm side
        [(-1.0, -12.7), (-1.65, -12.95), (-2.5, -12.95)],
    ],
    joints=dict(front="i", i=[(-4.1, -3.4), (-3.85, 0.85), (-1.4, 0.8), (1.3, 0.65)],
                t=[(-2.3, -11.0), (-1.9, -7.0), (-2.15, -3.9), (-2.6, -1.22)],
                crease=(-3.1, -12.7), hand_dir=(-0.06, 0.998), wrist=(-3.2, -13.6),
                arm_dir=(0.14, 0.99)),
)


# ---------------------------------------------------------------- full crimp
#
# A tent where the half crimp is a table. The first segment slants up, the middle joint
# peaks well past 90 degrees, the middle segment falls steeply and the end joint bends
# back, so that the end segment lies flat with its pad on the edge. The bend shows in the
# outline itself: a dent, then the end segment's back running on to the wall. The thumb's
# tip comes up over the end segment to the finger's back, and the fingertip shows beyond
# it. On this shallow edge the hand stands nearer the wall than in the half crimp.

FULL_TOP = [
    # forearm's back, wrist, back of the hand
    (-6.35, -18.42), (-5.8, -16.02), (-5.35, -14.42), (-5.03, -13.02), (-4.77, -11.42),
    (-4.69, -10.32), (-4.8, -9.22), (-5.0, -7.42), (-5.17, -5.42), (-5.3, -3.42), (-5.33, -2.5),
    # the knuckle turns into the first segment, slanting up to the middle joint
    (-5.27, -1.55), (-5.06, -0.62), (-4.64, 0.55), (-4.18, 1.76), (-3.74, 2.84),
    # the peak of the middle joint, an arc of 1 cm, and down the middle segment
    (-3.52, 3.37), (-3.21, 3.78), (-2.75, 3.98), (-2.24, 3.92), (-1.83, 3.62), (-1.58, 3.3),
    (-1.06, 2.66), (-0.56, 2.02),
    # the dent of the bent-back end joint, the end segment's back
    (-0.36, 1.68), (-0.2, 1.43), (-0.02, 1.33), (0.22, 1.33), (0.7, 1.44), (1.2, 1.44),
    (1.62, 1.25),
    # the fingertip against the wall
    (1.92, 0.88), (1.98, 0.45),
]
FULL_WRIST = [(-0.5, -10.32), (-1.2, -10.54), (-2.0, -10.54)]
FULL_JOINTS = dict(front="i", i=[(-3.7, -0.95), (-2.48, 2.92), (-0.8, 0.91), (1.9, 0.75)],
                   t=[(-2.15, -7.92), (-1.5, -3.92), (-0.25, -1.29), (0.85, 1.46)],
                   crease=(-2.65, -10.22), hand_dir=(-0.1, 0.995), wrist=(-2.75, -11.12),
                   arm_dir=(0.14, 0.99))

FULL = dict(
    outline=[FULL_TOP + [
        # its pad on the edge
        (1.93, 0.14), (1.65, 0.09), (1.18, 0.14, 1),
        # the thumb's outer edge, which runs on as the palm's
        (1.0, -0.42), (0.74, -1.2), (0.42, -2.1), (0.08, -3.2), (-0.12, -4.4), (-0.24, -5.62),
        (-0.26, -7.0), (-0.22, -8.42), (-0.32, -9.42), (-0.5, -10.32),
        # the forearm's front
        (-0.55, -11.42), (-0.57, -13.42), (-0.71, -15.42), (-1.07, -18.42),
    ]],
    lines=[
        # the thumb: up from the hold's corner, over to the finger's back, down its inner edge
        # and into the palm
        [(1.18, 0.14), (1.3, 0.5), (1.3, 0.95), (1.06, 1.36), (0.62, 1.44), (0.16, 1.3),
         (-0.18, 1.02), (-0.6, 0.45), (-1.14, -0.8), (-1.55, -1.8), (-1.82, -2.7)],
        # the finger's palm side: the end segment, round the crook, down the first segment
        [(-0.78, 0.2), (-1.16, 0.24), (-1.62, 0.42), (-1.96, 0.86), (-2.14, 1.28), (-2.38, 1.54),
         (-2.64, 1.36), (-2.76, 0.96), (-2.86, 0.3), (-3.0, -0.5), (-3.16, -1.3)],
    ],
    marks=[
        nail((0.72, 1.46), (0.3, 0.95), w=0.9, L=0.88, back=0.38),
        FULL_WRIST,
    ],
    joints=dict(FULL_JOINTS, dent=(-0.62, 1.3), label=(1.0, 1.4)),
)

# The same finger with the thumb free below it, which leaves all of the end segment in view:
# its back runs on level from the dent, with its nail, and its pad lies on the edge.
FULL_FREE = dict(
    outline=[[(-6.62, -20.0)] + FULL_TOP + [
        # its pad on the edge, the underside, round the crook, down the first segment
        (1.93, 0.2), (1.65, 0.12), (1.0, 0.09), (0.3, 0.07), (-0.3, 0.08), (-0.78, 0.16), (-1.2, 0.3),
        (-1.62, 0.56), (-1.96, 0.88), (-2.14, 1.28), (-2.38, 1.54), (-2.64, 1.36), (-2.72, 0.96),
        (-2.76, 0.3), (-2.74, -0.3), (-2.66, -0.73, 1),
        # round the thumb's tip and down its outer edge, which is the palm's
        (-2.4, -0.3), (-2.0, -0.15), (-1.42, -0.36), (-1.06, -0.92), (-0.92, -1.6), (-0.82, -2.4), (-0.7, -3.6),
        (-0.58, -5.0), (-0.45, -6.4), (-0.36, -7.8), (-0.34, -9.0), (-0.5, -10.32),
        # the forearm's front
        (-0.55, -11.42), (-0.57, -13.42), (-0.71, -15.42), (-1.07, -18.42), (-1.34, -20.0),
    ]],
    lines=[
        # the thumb's inner edge, from the fork at its tip down into the palm
        [(-2.66, -0.73), (-2.98, -1.33), (-3.04, -2.13), (-2.9, -3.23), (-2.66, -4.43), (-2.44, -5.63)],
    ],
    marks=[
        side_nail((0.46, 1.38), (1.6, 1.27), (1.0, 0.7), 0.28),
        nail((-2.02, -0.15), (-0.1, 0.99), w=1.06, L=1.04, off=0.02, back=0.46),
        FULL_WRIST,
    ],
    joints=dict(FULL_JOINTS, dent=(-0.2, 1.0),
                t=[(-2.0, -8.5), (-1.75, -4.9), (-1.75, -2.7), (-2.02, -0.15)]),
)


# ---------------------------------------------------------------- open hand
#
# A drag: the first segment leans toward the wall, the middle joint bends about
# 40 degrees, the pads lie over the lip. The thumb hangs in an open V.

OPEN_TOP = [
    # the forearm's back, wrist, back of the hand
    (-7.35, -22.0), (-6.92, -20.0), (-6.45, -17.8), (-6.02, -16.2), (-5.68, -15.0), (-5.5, -14.1),
    (-5.45, -13.2), (-5.5, -11.5), (-5.56, -9.5), (-5.6, -7.5), (-5.56, -6.0),
    # the knuckle, the first segment
    (-5.3, -4.85), (-4.8, -3.5), (-4.25, -2.1), (-3.78, -0.6),
    # the middle joint, then along the top to the tip
    (-3.3, 0.1), (-2.4, 0.82), (-1.3, 1.4), (0.0, 1.54), (1.0, 1.42), (1.55, 1.1), (1.72, 0.68),
    (1.5, 0.25), (0.95, 0.03),
    # the pad on the lip, the underside, the crook
    (0.2, 0.0), (-0.45, 0.0), (-1.2, -0.42), (-1.78, -0.98),
    # the first segment's palm side, down to where the thumb crosses it
    (-2.3, -2.1), (-2.42, -3.3), (-2.2, -4.5), (-2.0, -5.5),
]
OPEN_BOTTOM = [
    # the heel, the wrist's notch, the forearm's front
    (-0.86, -10.5), (-0.95, -11.8), (-1.08, -13.0), (-1.18, -13.7),
    (-1.18, -14.6), (-1.26, -16.0), (-1.46, -17.6), (-1.82, -20.0), (-2.15, -22.0),
]
OPEN_NAIL = [(0.0, 1.54), (0.22, 1.26), (0.8, 1.17), (1.22, 1.15), (1.38, 1.22)]
OPEN_WRIST = [(-1.18, -13.7), (-1.9, -13.95), (-2.7, -13.95)]

OPEN = dict(
    outline=[OPEN_TOP + [
        (-2.02, -6.72, 1),
        # up the thumb's inner edge, round its tip, down its outer edge
        (-1.55, -6.0), (-1.25, -5.1), (-1.02, -4.3), (-0.72, -3.65), (-0.18, -3.42),
        (0.32, -3.7), (0.6, -4.4), (0.62, -5.4), (0.36, -6.6), (-0.2, -8.0), (-0.74, -9.4),
    ] + OPEN_BOTTOM],
    lines=[
        # the thumb's edge runs on into the palm and fades
        [(-2.02, -6.72), (-2.32, -7.3), (-2.52, -7.85)],
    ],
    marks=[
        OPEN_NAIL,
        nail((-0.18, -3.42), (0.0, 1.0), w=1.12, L=1.12, off=-0.02),
        OPEN_WRIST,
    ],
    joints=dict(front="i", i=[(-3.85, -4.65), (-2.75, -0.55), (-0.75, 0.85), (1.72, 0.7)],
                t=[(-2.4, -12.0), (-1.6, -9.4), (-0.75, -6.35), (-0.18, -3.42)],
                crease=(-3.3, -13.7), hand_dir=(-0.04, 0.999), wrist=(-3.4, -14.6),
                arm_dir=(0.22, 0.975)),
)

# The same hand with the thumb pressed up into a dimple under the lip.
CATCH = dict(
    outline=[OPEN_TOP + [
        (-2.02, -6.5, 1),
        (-1.4, -5.5), (-1.0, -4.3), (-0.72, -3.3), (-0.42, -2.52), (0.15, -2.24),
        (0.68, -2.52), (0.95, -3.4), (0.95, -4.4), (0.76, -5.5), (0.34, -6.8), (-0.18, -8.0),
        (-0.68, -9.4),
    ] + OPEN_BOTTOM],
    lines=[
        [(-2.02, -6.5), (-2.3, -7.05), (-2.5, -7.55)],
    ],
    marks=[
        OPEN_NAIL,
        nail((0.15, -2.24), (0.04, 1.0), w=0.94, L=0.92, back=0.42),
        OPEN_WRIST,
    ],
    joints=dict(OPEN["joints"], t=[(-2.4, -11.4), (-1.2, -8.35), (-0.2, -5.35), (0.15, -2.24)]),
)


# ---------------------------------------------------------------- jug
#
# The fingers hook over the lip into the bucket, the thumb wraps the front.

JUG = dict(
    outline=[[
        # the forearm's back, wrist, back of the hand up to the knuckle
        (-7.7, -18.0), (-7.58, -15.5), (-7.44, -13.2), (-7.32, -11.4), (-7.28, -10.2),
        (-7.42, -9.1), (-7.75, -7.9), (-8.25, -6.1), (-8.75, -4.3), (-9.15, -2.6), (-9.3, -1.5),
        # the knuckle turns, the first segment, the middle joint
        (-9.08, -0.55), (-8.42, 0.5), (-7.6, 2.0), (-6.85, 3.3), (-6.2, 3.82), (-5.5, 3.78),
        # over the lip and down into the bucket
        (-4.4, 3.45), (-3.4, 3.0), (-2.75, 2.35), (-2.0, 1.55), (-1.45, 0.95), (-1.35, 0.55),
        (-1.6, 0.15), (-2.1, -0.02),
        # the pad, the underside, back over the lip to the crook
        (-2.6, 0.3), (-3.3, 0.95), (-4.0, 1.6), (-4.6, 1.95), (-5.3, 2.05), (-5.65, 1.85),
        (-5.87, 1.3), (-6.13, 0.75, 1),
        # the thumb's tip, its outer edge down the jug's front, the ball of the thumb
        (-5.75, 0.4), (-5.58, -0.3), (-5.46, -1.2), (-5.1, -2.4), (-4.45, -3.3), (-3.82, -4.1),
        (-3.36, -5.1), (-3.08, -6.3), (-2.94, -7.5), (-2.92, -8.7),
        # the forearm's front
        (-2.84, -10.0), (-2.72, -12.0), (-2.62, -14.0), (-2.6, -15.5), (-2.72, -18.0),
    ]],
    lines=[
        # the thumb's inner edge
        [(-6.13, 0.75), (-6.55, 0.95), (-7.1, 0.7), (-7.4, 0.0), (-7.48, -1.0), (-7.38, -2.4),
         (-7.15, -3.6), (-6.9, -4.5)],
    ],
    marks=[
        nail((-6.5, 0.95), (0.0, 1.0), w=1.12, L=1.12, off=0.05),
        # index nail
        side_nail((-2.62, 2.22), (-1.56, 1.08), (-2.6, 1.2), 0.27),
        # the wrist
        [(-2.98, -8.7), (-3.6, -9.25), (-4.4, -9.5)],
    ],
    joints=dict(front="i", i=[(-8.1, -0.8), (-6.0, 2.9), (-3.7, 2.35), (-1.35, 0.55)],
                t=[(-4.7, -7.4), (-5.6, -4.5), (-6.4, -2.0), (-6.55, 0.95)],
                crease=(-5.0, -9.35), hand_dir=(-0.342, 0.94), wrist=(-4.95, -10.25),
                arm_dir=(0.02, 1.0)),
)


# ---------------------------------------------------------------- sloper
#
# Draped over a dome, palm and pads on it, the wrist dropped below the hold:
# the hand comes in on a long diagonal and the arm hangs from it.

SLOPER_TOP = [
    # the back of the hand from the wrist's bump
    (-9.9, -7.2), (-9.25, -5.5), (-8.5, -3.7), (-7.75, -2.0), (-7.1, -0.55),
    # the knuckle turns, first segment, middle joint, top of the finger
    (-6.4, 0.42), (-5.2, 1.85), (-4.12, 3.08), (-3.47, 3.74), (-2.72, 4.42), (-1.53, 5.16),
    (-0.34, 5.52), (0.75, 5.66), (1.35, 5.5), (1.62, 5.08), (1.42, 4.6), (0.9, 4.32),
    # the pad and the underside on the dome
    (0.2, 4.12), (-0.85, 3.75), (-1.8, 3.15), (-2.65, 2.42), (-3.15, 1.55), (-3.52, 0.8),
    (-3.8, 0.35, 1),
]
SLOPER_HANG_BACK = [(-11.45, -19.0), (-11.3, -16.0), (-11.0, -13.0), (-10.85, -11.2), (-10.65, -9.6), (-10.35, -8.5)]
SLOPER_THUMB = [
    # the thumb's tip, its outer edge, the ball of the thumb
    (-3.04, 0.62), (-2.3, 0.24), (-2.02, -0.7), (-2.06, -2.2), (-2.56, -3.6), (-3.46, -4.95),
    (-4.3, -6.1), (-5.2, -7.25), (-5.95, -8.25),
]
SLOPER_HANG_FRONT = [(-6.45, -9.4), (-6.58, -10.4), (-6.5, -11.6), (-6.42, -13.0), (-6.38, -15.0), (-6.45, -19.0)]
SLOPER_MARKS = [
    # index nail
    side_nail((-0.1, 5.56), (1.28, 5.54), (0.6, 4.9), 0.3),
    nail((-3.04, 0.62), (0.0, 1.0), w=1.12, L=1.12, off=0.02),
    # the wrist
    [(-6.45, -9.4), (-7.05, -9.65), (-7.8, -9.6)],
]

SLOPER = dict(
    outline=[SLOPER_HANG_BACK + SLOPER_TOP + SLOPER_THUMB + SLOPER_HANG_FRONT],
    lines=[
        [(-3.8, 0.35), (-3.86, -0.4), (-4.0, -1.3), (-4.18, -2.2), (-4.36, -3.0), (-4.56, -3.8)],
    ],
    marks=SLOPER_MARKS,
    joints=dict(front="i", i=[(-5.45, -0.51), (-3.11, 3.03), (-1.12, 4.43), (1.6, 5.1)],
                t=[(-6.9, -8.0), (-4.6, -5.1), (-3.2, -2.3), (-3.1, 0.55)],
                crease=(-8.6, -9.0), hand_dir=(0.342, 0.94), wrist=(-8.75, -9.9),
                arm_dir=(0.03, 1.0)),
)


# ---------------------------------------------------------------- pocket
#
# Seen from the little-finger side: ring and middle in the hole to about the first
# joint, the little finger in front. The thumb is behind the palm and stands out past it,
# so we see its pad side, a plain round-ended tube with no nail.

POCKET_ARM_BACK = [
    # the forearm's back, wrist, back of the hand
    (-9.9, -19.5), (-9.52, -17.0), (-9.26, -15.0), (-9.08, -13.4), (-9.0, -12.3),
    (-8.9, -11.0), (-8.76, -9.0), (-8.64, -7.0), (-8.52, -5.4),
]
POCKET_ARM_FRONT = [
    (-4.6, -9.2), (-4.6, -10.6), (-4.72, -11.7), (-4.85, -12.4),
    # the forearm's front
    (-4.82, -13.4), (-4.72, -15.2), (-4.62, -17.0), (-4.5, -19.5),
]
POCKET_MIDDLE = (GREY2, [(-4.2, -1.0), (-3.4, -0.75), (-1.0, -0.72), (-0.2, -0.7), (0.3, -0.5), (0.46, -0.12),
                         (0.26, 0.3), (-0.2, 0.5), (-1.0, 0.6), (-3.4, 0.4)])
POCKET_RING = [
    # the ring finger's back, its middle joint, into the hole, round the tip, back under it
    (-7.2, -3.7), (-6.5, -2.8), (-5.98, -1.9), (-5.66, -1.1), (-5.5, -0.25), (-5.0, 0.72), (-4.28, 1.42),
    (-3.3, 1.62), (-1.6, 1.55), (-0.4, 1.47), (0.3, 1.2), (0.56, 0.75), (0.36, 0.3), (-0.2, 0.12),
    (-1.0, 0.05), (-2.4, 0.0),
]
POCKET_THUMB = (GREY, [(-5.4, -7.3), (-4.78, -6.78), (-4.3, -6.25), (-3.84, -5.55), (-3.46, -4.85), (-3.1, -4.42),
                       (-2.6, -4.24), (-1.98, -4.42), (-1.58, -5.05), (-1.62, -5.8), (-2.02, -6.65), (-2.55, -7.55),
                       (-3.2, -8.5), (-3.95, -9.35), (-4.75, -10.0), (-5.6, -10.6), (-6.6, -9.2)])

POCKET = dict(
    outline=[POCKET_ARM_BACK + [
        # the little finger: knuckle, first segment, middle joint
        (-8.3, -4.53), (-7.88, -3.74), (-7.32, -3.03), (-6.88, -2.56), (-6.3, -1.68), (-5.82, -1.08), (-5.2, -0.82),
        # on along its back, level under the pocket fingers, to the tip
        (-4.4, -0.84), (-3.5, -0.96), (-2.75, -1.1), (-2.24, -1.34), (-2.0, -1.74), (-2.2, -2.16),
        (-2.74, -2.3),
        # back along the underside to the crook
        (-3.3, -2.32), (-4.1, -2.28), (-4.72, -2.42),
        # its first segment's palm side, then the palm and the heel
        (-5.14, -3.0), (-5.28, -3.72), (-5.2, -4.5), (-5.06, -5.4), (-4.9, -6.3), (-4.75, -7.6),
    ] + POCKET_ARM_FRONT],
    # the little finger hides the ring finger's root, so that can stop short of the hollow
    grey=[POCKET_MIDDLE,
          (GREY, POCKET_RING + [(-3.2, -0.25), (-3.95, -0.9), (-4.4, -1.45), (-5.1, -2.2), (-6.4, -3.4)]),
          POCKET_THUMB],
    marks=[
        # little finger's nail
        side_nail((-3.22, -1.0), (-2.46, -1.24), (-2.8, -1.75), 0.2),
        # the wrist
        [(-4.85, -12.4), (-5.5, -12.6), (-6.25, -12.6)],
    ],
    joints=dict(front="l", l=[(-6.95, -4.1), (-5.4, -1.45), (-3.4, -1.6), (-2.0, -1.72)],
                t=[(-5.6, -10.0), (-4.7, -8.7), (-3.2, -6.5), (-2.6, -4.24)], label=(-3.95, -1.62),
                crease=(-6.85, -12.2), hand_dir=(0.0, 1.0), wrist=(-6.95, -13.1),
                arm_dir=(0.14, 0.99), thumb_front=False, view="little"),
)

# The little finger curled into the palm: the same finger as one rounded arc from the knuckle
# over the middle joint to where its end comes back to the palm. Its first segment rises less
# steeply, its middle one folds down and its end turns back, so that the tip lies in the palm's
# hollow, with the palm's edge coming out from under the tip. The finger is in front of the
# palm, so its tip and pad are one inner line, which fades as it gets to the crook.
POCKET_CURLED = dict(
    outline=[POCKET_ARM_BACK + [
        (-8.32, -4.6), (-7.9, -3.85), (-7.25, -3.22), (-6.3, -2.6), (-5.4, -2.08),
        # round the middle joint, down the middle segment, round the end joint
        (-4.76, -1.84), (-4.2, -1.92), (-3.78, -2.38), (-3.56, -3.06), (-3.58, -3.74), (-3.86, -4.36),
        # the end segment's back as far as the tip, the palm, the heel
        (-4.28, -4.88), (-4.78, -5.3), (-5.3, -5.58, 1), (-5.06, -6.3), (-4.75, -7.6),
    ] + POCKET_ARM_FRONT],
    # the finger is out of the way here, so the ring finger keeps its width down to the hand
    grey=[POCKET_MIDDLE,
          (GREY, POCKET_RING + [(-3.1, -0.2), (-3.65, -0.8), (-3.95, -1.6), (-4.25, -2.6), (-4.6, -3.6),
                                (-6.4, -4.2)]),
          POCKET_THUMB],
    lines=[
        # round the fingertip on the palm and along its pad, fading before the crook
        [(-5.3, -5.58), (-5.62, -5.4), (-5.74, -5.02), (-5.54, -4.62), (-5.18, -4.28), (-4.96, -3.9), (-4.92, -3.44)],
    ],
    marks=[
        # little finger's nail, on the back of its end segment and clear of the palm's edge
        side_nail((-4.34, -4.94), (-5.2, -5.54), (-4.9, -4.9), 0.24),
        # the wrist
        [(-4.85, -12.4), (-5.5, -12.6), (-6.25, -12.6)],
    ],
    joints=dict(POCKET["joints"], l=[(-7.1, -4.0), (-4.5, -2.25), (-4.13, -4.06), (-5.6, -5.09)],
                label=(-4.15, -2.5)),
)


# ---------------------------------------------------------------- pinch
#
# From above, the wall along the top: an honest C, the thumb on one face of
# the rib and the bent index finger on the other, the arm from the lower left.

PINCH = dict(
    outline=[[
        # the forearm's lower edge, then the back of the hand
        (-12.5, -20.45), (-10.5, -19.1), (-8.6, -17.85), (-6.9, -16.8), (-5.2, -15.72), (-3.9, -14.9), (-2.5, -13.85), (-0.9, -12.65),
        (0.8, -11.4), (2.4, -10.35), (3.6, -9.72),
        # the knuckle, the first segment
        (4.3, -8.85), (5.1, -7.6), (5.85, -6.55), (6.25, -5.75),
        # the middle joint, the top of the finger, the tip
        (6.26, -4.95), (5.82, -4.3), (5.1, -3.76), (4.27, -3.2), (3.42, -2.68), (2.64, -2.24),
        (2.1, -2.0), (1.66, -2.08), (1.48, -2.5), (1.48, -3.0), (1.78, -3.5),
        # the inside of the finger
        (2.57, -4.04), (3.42, -4.58), (4.1, -5.02), (4.3, -5.5), (3.94, -6.12), (3.1, -6.56),
        # the web, a soft floor to the C
        (2.12, -6.98), (1.05, -7.52), (0.0, -7.98), (-0.95, -8.08), (-1.68, -7.58), (-2.0, -6.7),
        # up the thumb's inside to its pad and tip, and down its outside
        (-1.95, -6.0), (-1.75, -5.0), (-1.55, -4.1), (-1.5, -3.5), (-1.55, -2.9), (-1.95, -2.3),
        (-2.5, -2.15), (-3.1, -2.45), (-3.42, -3.1), (-3.58, -3.9), (-3.7, -5.1), (-3.95, -6.8),
        (-4.3, -8.2), (-4.75, -9.4), (-5.3, -10.4), (-6.0, -11.2),
        # the forearm's upper edge
        (-7.0, -11.78), (-8.6, -12.6), (-10.5, -13.75), (-12.5, -15.05),
    ]],
    marks=[
        # thumbnail, on the side away from the hold
        side_nail((-3.5, -3.6), (-2.9, -2.28), (-2.6, -3.2), 0.3),
        # index nail, the same
        side_nail((3.16, -2.53), (1.86, -2.0), (2.6, -3.0), 0.28),
        # the wrist
        [(-6.56, -11.52), (-6.1, -12.05), (-5.65, -12.85)],
    ],
    joints=dict(front="i", i=[(2.75, -8.35), (5.75, -5.35), (3.75, -3.95), (1.5, -2.6)],
                t=[(-3.6, -11.0), (-3.0, -8.0), (-2.7, -5.1), (-2.5, -2.15)],
                crease=(-4.97, -13.17), hand_dir=(0.848, 0.53), wrist=(-5.75, -13.55),
                arm_dir=(0.906, 0.423)),
)

# A 6 cm block: the thumb on one face and the fingers flat and open on the other.
PINCH_WIDE = dict(
    outline=[[
        (-14.0, -20.65), (-11.0, -18.85), (-8.5, -17.15), (-6.2, -15.55), (-3.8, -14.0), (-1.5, -12.7),
        (0.6, -11.7), (2.2, -11.0), (3.5, -10.3),
        # the knuckle, the first segment, straight up the face
        (4.25, -9.3), (4.62, -8.0), (4.72, -6.6), (4.66, -5.2), (4.6, -3.8), (4.55, -2.4),
        (4.42, -1.42), (3.9, -0.86), (3.32, -1.2), (3.06, -2.2),
        (3.05, -3.6), (3.04, -5.0), (2.96, -6.0), (2.58, -7.0),
        # the floor of the C
        (1.8, -7.8), (0.65, -8.28), (-0.6, -8.36), (-1.85, -8.08), (-2.68, -7.36), (-3.02, -6.3),
        # up the thumb's inside to its tip, and down its outside
        (-3.05, -5.0), (-3.05, -3.8), (-3.1, -3.1), (-3.42, -2.42), (-4.0, -2.2), (-4.58, -2.5),
        (-4.92, -3.2), (-5.02, -4.2), (-5.2, -5.6), (-5.5, -7.2), (-6.0, -8.8), (-6.7, -10.2),
        (-7.7, -11.4),
        # the forearm's upper edge
        (-9.2, -12.45), (-11.0, -13.45), (-14.0, -15.05),
    ]],
    marks=[
        # thumbnail, on the side away from the hold
        side_nail((-4.92, -3.5), (-4.32, -2.26), (-4.0, -3.2), 0.3),
        # index nail
        side_nail((4.58, -2.8), (4.44, -1.52), (3.9, -2.2), 0.3),
        # the wrist
        [(-8.2, -11.76), (-7.78, -12.36), (-7.38, -13.25)],
    ],
    joints=dict(front="i", i=[(2.75, -10.0), (3.88, -6.0), (3.88, -3.6), (3.9, -0.86)],
                t=[(-5.4, -11.0), (-4.3, -8.0), (-4.05, -5.1), (-4.0, -2.2)],
                crease=(-6.1, -12.9), hand_dir=(0.95, 0.31), wrist=(-6.9, -13.3),
                arm_dir=(0.86, 0.5)),
)

# The ridge of a volume: the thumb on the near face, the fingers over the ridge on
# the far one, the hand coming up from the lower left.
PINCH_RIDGE = dict(
    outline=[[
        (-16.5, -20.4), (-14.0, -19.0), (-11.0, -17.35), (-8.5, -15.9), (-6.2, -14.55), (-4.0, -13.32),
        (-2.0, -12.3), (-0.3, -11.55),
        # the knuckle, the first segment up the far face
        (0.9, -10.7), (1.68, -9.75), (2.22, -8.45), (2.82, -7.42), (3.55, -6.42),
        # the middle joint, on to the tip
        (4.46, -5.3), (5.34, -4.26), (5.92, -3.3), (6.0, -2.68), (5.66, -2.28), (5.14, -2.62),
        # the pad on the face, the underside
        (4.56, -3.14), (3.5, -4.04), (2.4, -4.9), (1.5, -5.72), (0.82, -6.65),
        # the floor of the C
        (0.05, -7.72), (-0.75, -8.42), (-1.65, -8.9), (-2.58, -9.02),
        # up the thumb's inside, round its tip on the near face, down its outside
        (-3.04, -8.4), (-3.2, -7.5), (-3.24, -6.5), (-3.22, -5.4), (-3.16, -4.72), (-3.5, -4.1), (-4.12, -3.9),
        (-4.72, -4.18), (-5.02, -4.85), (-5.22, -5.9), (-5.52, -7.1), (-6.08, -8.45), (-6.95, -9.62),
        (-8.0, -10.62),
        # the forearm's upper edge
        (-9.6, -11.5), (-11.5, -12.45), (-14.0, -13.8), (-16.5, -15.2),
    ]],
    marks=[
        # thumbnail, on the side away from the hold
        side_nail((-4.96, -4.8), (-4.0, -3.92), (-4.2, -4.8), 0.28),
        # index nail
        side_nail((5.38, -4.2), (5.97, -3.0), (5.0, -3.4), 0.28),
        # the wrist
        [(-8.98, -11.2), (-8.5, -11.8), (-8.08, -12.6)],
    ],
    joints=dict(front="i", i=[(0.2, -8.9), (2.8, -6.2), (4.0, -4.6), (5.6, -2.18)],
                t=[(-7.0, -11.5), (-5.2, -8.3), (-4.4, -6.0), (-4.12, -3.9)],
                crease=(-7.75, -13.47), hand_dir=(0.85, 0.53), wrist=(-8.55, -13.87),
                arm_dir=(0.88, 0.48)),
)


# ---------------------------------------------------------------- undercling
#
# Palm up under a flake, an open hand: the hand comes up on a diagonal. The fingers
# pass the lip and rise into the hollow behind it, where you can see them. The end
# joints curl back, so the fingertips come down on the lip's inner face with their
# nails away from it. A pull up and out draws them onto it. The thumb points out.

UNDER = dict(
    outline=[[
        # the back of the hand, from below the tile up to the knuckle
        (-9.61, -19.55), (-7.61, -17.24), (-5.84, -15.24), (-4.97, -13.99), (-3.72, -12.42), (-2.44, -10.66),
        # the knuckle, the first segment's back, the middle joint
        (-1.77, -9.34), (-1.31, -8.03), (-0.82, -6.8), (-0.34, -5.77),
        # the middle segment, then the end segment curling back toward the lip
        (-0.07, -4.6), (-0.13, -3.5), (-0.5, -2.72), (-1.1, -2.16), (-1.62, -1.76),
        # the fingertip, on the lip's inner face
        (-2.08, -1.56), (-2.52, -1.7), (-2.74, -2.15),
        # the pad and the palm side, one easy curve down to the web
        (-2.62, -2.65), (-2.32, -3.2), (-1.98, -3.85), (-1.8, -4.6), (-1.9, -5.35), (-2.34, -6.14), (-3.05, -6.92),
        (-3.82, -7.6),
        # the web, a soft curve, to the thumb
        (-4.76, -8.18), (-5.36, -8.15), (-5.66, -7.5),
        # up the thumb's inner edge, round its tip, down its outer edge
        (-5.84, -6.4), (-5.98, -5.5), (-6.12, -4.7), (-6.3, -4.05), (-6.6, -3.5), (-7.25, -3.18),
        (-7.78, -3.44), (-7.98, -4.1), (-8.0, -5.2), (-7.94, -6.3), (-7.88, -7.3), (-7.95, -8.5), (-8.19, -9.65),
        # the ball of the thumb, leaving the tile
        (-8.57, -10.77), (-9.22, -11.98), (-10.09, -13.25), (-11.31, -14.63), (-13.39, -17.05),
    ]],
    grey=[
        # the end of the middle finger behind it, longer, its tip up against the hollow's roof
        (GREY, [(-0.6, -3.4), (-0.24, -3.2), (-0.1, -2.66), (-0.36, -1.98), (-0.82, -1.36), (-1.2, -1.12),
                (-1.52, -1.2), (-1.62, -1.5), (-1.4, -2.0), (-0.9, -2.8)]),
    ],
    marks=[
        side_nail((-1.06, -2.2), (-1.76, -1.68), (-1.7, -2.3), 0.2),
        nail((-7.25, -3.18), (-0.13, 0.99), w=0.98, L=1.06, off=-0.08, back=0.4),
        # the wrist, from the palm side
        [(-10.9, -14.17), (-10.55, -14.6), (-10.05, -15.05)],
    ],
    joints=dict(front="i", i=[(-3.44, -9.29), (-0.82, -5.94), (-0.99, -3.5), (-2.5, -1.7)],
                t=[(-8.6, -12.9), (-6.9, -9.1), (-6.87, -6.05), (-7.25, -3.18)],
                crease=(-9.32, -15.69), hand_dir=(0.695, 0.72), wrist=(-9.93, -16.38),
                arm_dir=(0.695, 0.72)),
)


# ---------------------------------------------------------------- back views
#
# Written upright as (across, along) with the wrist crease at the origin, the
# little finger to the right: a right hand, its back toward you.

BACK_RIGHT = [
    # the little-finger side, from the arm up: the forearm, the wrist, the heel, then the palm
    (3.56, -8.0), (3.38, -5.0), (3.22, -2.6), (3.18, -0.9), (3.28, 0.3), (3.56, 1.5), (3.92, 2.9),
    (4.22, 4.6), (4.42, 6.4), (4.52, 7.6),
]
BACK_LEFT = [
    # the ball of the thumb, into the wrist and down the arm
    (-5.0, 4.9), (-4.62, 3.7), (-4.12, 2.4), (-3.66, 1.2), (-3.34, 0.0), (-3.24, -1.2), (-3.28, -2.8),
    (-3.4, -5.0), (-3.6, -8.0),
]


def web(p, q, a):
    """The bottom of the gap between two spread fingers: one soft point at height `a`."""
    return [(0.5 * (p[0] + q[0]), a)]


def closed_web(p, q, a):
    """The bottom of the gap between two fingers side by side: the outline comes down one
    edge at p, round a half circle with its lowest point at height `a` and up the other
    edge at q, so the gap closes in one line. Keep the edges 0.46 apart: that stays open
    under the pen at both plate scales. Edges that converge fill in to a black wedge."""
    r = 0.5 * (p[0] - q[0])
    m = p[0] - r
    return [(m + r * c, a + r * (1 - s), KEEP) for c, s in ((1, 0), (0.71, 0.71), (0, 1), (-0.71, 0.71), (-1, 0))]


def fingers_up(shapes, webs, join=closed_web):
    """The fingers from the little finger across to the index, as lists of control
    points, joined by webs."""
    out = list(shapes[0])
    for d, a in zip(shapes[1:], webs):
        out += join(out[-1], d[0], a) + list(d)
    return out


# The drag: the fingers come up over the edge and their ends go on over its top.
DRAG_CHAINS = [
    ([(3.6, 11.0), (3.8, 12.5), (4.14, 14.05)], 0.77, 0.67),
    ([(1.48, 11.8), (1.72, 14.0), (1.88, 15.75)], 0.89, 0.81),
    ([(-0.8, 11.9), (-0.84, 14.5), (-0.86, 16.5)], 0.93, 0.86),
    ([(-3.15, 11.7), (-3.37, 14.0), (-3.53, 15.9)], 0.96, 0.84),
]
DRAG_WEBS = [10.2, 10.75, 10.65]
BACK_EDGE = [(4.54, 8.8), (4.44, 9.9)]


def back_thumb(tip, w, top=None):
    """The thumb beside the hand, from where the index's edge meets it, round its end and
    down its outer edge. Its inner edge isn't part of the outline: the index's edge runs
    on into the palm as one line."""
    x, y = tip
    return [(x + w * 0.5, y - 1.05, 1), (x + w * 0.46, y - 0.62), (x + w * 0.27, y - 0.16), (x - 0.06, y),
            (x - w * 0.3, y - 0.18), (x - w * 0.48, y - 0.72), (x - w * 0.57, y - 1.85),
            (x - w * 0.56, y - 3.2), (x - w * 0.34, y - 4.6)]


BACK_THUMB_TIP = (-4.95, 11.42)
BACK_THUMB = back_thumb(BACK_THUMB_TIP, 1.72)
BACK_THUMB_LINE = [BACK_THUMB[0][:2], (-4.0, 9.4), (-3.82, 8.3), (-3.6, 7.2), (-3.42, 6.3)]
BACK_THUMB_NAIL = nail(BACK_THUMB_TIP, (0.02, 1.0), w=1.06, L=1.12)

def back_nails(chains):
    """Short nails on the ends of fingers that go on over the hold."""
    return [nail(c[-1], sub(c[-1], c[-2]), w=2 * w1 * 0.6, L=0.5, back=0.2) for c, _, w1 in chains]


_DRAG_SHAPES = [finger(*c) for c in DRAG_CHAINS]
BACK_DRAG = dict(
    outline=[BACK_RIGHT + BACK_EDGE[:2] + fingers_up(_DRAG_SHAPES, DRAG_WEBS)
             + BACK_THUMB + BACK_LEFT],
    lines=[BACK_THUMB_LINE],
    marks=[BACK_THUMB_NAIL] + back_nails(DRAG_CHAINS),
    joints=dict(front=None, view="back",
                i=[(-3.02, 9.9), (-3.37, 13.9), (-3.53, 15.2), (-3.53, 15.9)],
                m=[(-0.83, 10.0), (-0.84, 14.3), (-0.85, 15.8), (-0.86, 16.5)],
                r=[(1.26, 9.7), (1.72, 13.7), (1.83, 15.0), (1.88, 15.75)],
                l=[(3.2, 8.95), (3.9, 12.2), (4.03, 13.05), (4.14, 14.05)],
                t=[(-3.0, 2.0), (-4.55, 5.93), (-5.3, 8.77), (-4.95, 11.42)],
                crease=(0.0, 0.0), hand_dir=(0.0, 1.0), across=(1.0, 0.0), wrist=(0.0, -0.8),
                arm_dir=(0.0, 1.0)),
)

# Three fingers on, the little finger curled off: only its first segment shows, as it bends
# away from you at its end. That's a finger's taper with no nail, higher than the thumb's tip.
DRAG3_CHAINS = [
    ([(1.48, 11.8), (1.8, 14.7), (1.98, 16.95)], 0.89, 0.81),
    ([(-0.8, 11.9), (-0.86, 15.2), (-0.92, 17.7)], 0.93, 0.86),
    ([(-3.13, 11.7), (-3.45, 14.7), (-3.64, 17.0)], 0.94, 0.84),
]
_OFF = [(4.44, 9.9), (4.42, 10.7), (4.26, 11.42), (3.86, 11.92), (3.44, 11.94), (3.1, 11.5), (2.94, 10.8),
        (2.86, 10.05)]
_DRAG3_SHAPES = [_OFF] + [finger(*c) for c in DRAG3_CHAINS]
_DRAG3_WEBS = [9.4, 10.75, 10.65]
BACK_DRAG3 = dict(
    # the arm runs on to the bottom of the figure's taller panel
    outline=[[(3.72, -10.5)] + BACK_RIGHT + BACK_EDGE[:1] + fingers_up(_DRAG3_SHAPES, _DRAG3_WEBS)
             + BACK_THUMB + BACK_LEFT + [(-3.78, -10.5)]],
    lines=[BACK_THUMB_LINE],
    marks=[BACK_THUMB_NAIL] + back_nails(DRAG3_CHAINS),
    joints=dict(BACK_DRAG["joints"],
                i=[(-3.02, 9.9), (-3.45, 14.6), (-3.6, 16.1), (-3.64, 17.0)],
                m=[(-0.83, 10.0), (-0.86, 15.0), (-0.9, 16.6), (-0.92, 17.7)],
                r=[(1.26, 9.7), (1.8, 14.4), (1.93, 15.9), (1.98, 16.95)],
                l=[(3.2, 8.95), (3.66, 10.8), (3.66, 11.4), (3.64, 11.94)]),
)

# A half crimp from behind: the fingers rise side by side to their bent middle joints and
# the rest of each goes away from you, on to the edge. Seen a little from above, each
# finger shows a short nail.
CRIMP_CHAINS = [
    ([(3.6, 11.0), (3.78, 12.4), (3.94, 13.6)], 0.77, 0.69),
    ([(1.48, 11.8), (1.6, 13.2), (1.68, 14.4)], 0.89, 0.83),
    ([(-0.8, 11.9), (-0.82, 13.4), (-0.84, 14.9)], 0.93, 0.89),
    ([(-3.13, 11.7), (-3.27, 13.2), (-3.35, 14.5)], 0.94, 0.86),
]
CRIMP_WEBS = [10.3, 11.0, 10.9]
CRIMP_TIP = (-4.9, 11.25)
CRIMP_THUMB = back_thumb(CRIMP_TIP, 1.78)
CRIMP_NAIL = nail(CRIMP_TIP, (0.0, 1.0), w=1.06, L=1.12)
_CRIMP_SHAPES = [finger(*c) for c in CRIMP_CHAINS]
BACK_CRIMP = dict(
    outline=[BACK_RIGHT + BACK_EDGE[:2] + fingers_up(_CRIMP_SHAPES, CRIMP_WEBS)
             + [(-4.02, 11.0)] + CRIMP_THUMB + BACK_LEFT],
    lines=[[CRIMP_THUMB[0][:2], (-4.0, 9.3), (-3.82, 8.2), (-3.6, 7.2), (-3.42, 6.3)]],
    marks=[CRIMP_NAIL] + back_nails(CRIMP_CHAINS),
    joints=dict(front=None, view="back",
                i=[(-3.02, 9.9), (-3.27, 13.1), (-3.27, 12.8), (-3.27, 12.5)],
                m=[(-0.83, 10.0), (-0.82, 13.5), (-0.82, 13.0), (-0.82, 12.6)],
                r=[(1.26, 9.7), (1.6, 13.0), (1.6, 12.4), (1.6, 12.0)],
                l=[(3.2, 8.95), (3.82, 12.5), (3.82, 12.1), (3.82, 11.8)],
                t=[(-3.0, 2.0), (-4.65, 5.93), (-5.25, 8.6), (-4.9, 11.25)],
                crease=(0.0, 0.0), hand_dir=(0.0, 1.0), across=(1.0, 0.0), wrist=(0.0, -0.8),
                arm_dir=(0.0, 1.0)),
)


# ---------------------------------------------------------------- palm press
#
# The back of the hand toward you, foreshortened a little by the three-quarter
# view: breadth 8.5, 9.9 from the wrist crease to the webs, middle finger 7.4
# from its web, wrist 6.2. The fingers lean a little toward the middle one.

PALM_AT = (0.1, -0.85)    # the wrist crease: thumb and little finger about 0.5 inside the tile
PALM_LEAN = 8.0
PALM_PITCH = 23.0      # three quarters on: cos 23 = 0.92

_P_LITTLE = ([(3.62, 9.4), (4.2, 11.9), (4.9, 15.0)], 0.84, 0.66)
_P_RING = ([(1.38, 11.0), (1.8, 13.2), (2.1, 16.95)], 0.98, 0.8)
_P_MIDDLE = ([(-0.9, 11.15), (-1.0, 13.45), (-1.12, 17.5)], 1.0, 0.82)
_P_INDEX = ([(-3.2, 10.9), (-3.58, 12.95), (-3.94, 16.75)], 0.98, 0.8)
_P_THUMB = ([(-5.1, 6.0), (-6.25, 8.1), (-7.72, 11.3)], 1.14, 0.92)

# the sides of this hand, kept as approved
_PALM_RIGHT = [
    (3.72, -8.0), (3.46, -5.0), (3.22, -2.6), (3.06, -0.9), (3.08, 0.1), (3.42, 1.3), (3.85, 2.9),
    (4.2, 4.6), (4.4, 6.4),
]
_PALM_LEFT = [
    (-4.62, 3.7), (-4.05, 2.3), (-3.48, 1.0), (-3.12, -0.3), (-3.1, -1.2), (-3.24, -2.8),
    (-3.48, -5.0), (-3.75, -8.0),
]
_PALM_LOOP = (
    _PALM_RIGHT + [(4.42, 7.8)]
    + fingers_up([finger(*_P_LITTLE), finger(*_P_RING), finger(*_P_MIDDLE), finger(*_P_INDEX)],
                 [9.05, 10.0, 9.92], join=web)[:-1]
    # the thumb's web, a soft U, and the thumb
    + [(-4.2, 9.5), (-4.16, 8.6), (-4.36, 7.86), (-4.78, 7.72)]
    + finger(*_P_THUMB)[1:]
    + _PALM_LEFT
)

PALM = moved(dict(
    outline=[_PALM_LOOP],
    marks=[nail(c[-1], sub(c[-1], c[-2]), w=2 * w1 * k, L=L, back=0.24)
           for (c, _, w1), k, L in ((_P_LITTLE, 0.62, 0.72), (_P_RING, 0.62, 0.88), (_P_MIDDLE, 0.62, 0.9),
                                    (_P_INDEX, 0.62, 0.88), (_P_THUMB, 0.68, 0.95))],
    joints=dict(front=None, view="back",
                i=[(-3.2, 8.4), (-3.58, 12.95), (-3.8, 14.9), (-3.94, 16.75)],
                m=[(-0.9, 8.4), (-1.0, 13.45), (-1.06, 15.5), (-1.12, 17.5)],
                r=[(1.38, 8.1), (1.78, 13.0), (1.98, 14.95), (2.1, 16.95)],
                l=[(3.14, 7.4), (4.1, 11.9), (4.46, 13.35), (4.86, 15.0)],
                t=[(-3.0, 2.0), (-5.1, 6.0), (-6.25, 8.1), (-7.72, 11.3)],
                crease=(0.0, 0.0), hand_dir=(0.0, 1.0), across=(1.0, 0.0), wrist=(0.0, -0.8),
                arm_dir=(0.0, 1.0)),
), dx=PALM_AT[0], dy=PALM_AT[1], deg=PALM_LEAN)


# ---------------------------------------------------------------- wrap
#
# An arete seen at an angle, its edge upright at x = 0: the arm from the left, the
# palm and thumb on the near face, the fingers across it, turning at the edge on to
# the far face. The back of the hand toward you, its breadth narrowed by the view.

# The fingers lie side by side on the near face with slits between them. They part at
# the edge, rising to it and levelling off beyond, which shows them turning round it.
_W_FINGERS = [
    ([(-0.9, -2.82), (0.25, -2.52), (1.6, -2.6)], 0.79, 0.66),
    ([(-0.9, -1.1), (0.35, -0.72), (2.75, -0.72)], 0.87, 0.75),
    ([(-0.7, 0.77), (0.35, 1.12), (3.0, 1.22)], 0.9, 0.77),
    ([(-0.8, 2.67), (0.25, 3.12), (2.55, 3.36)], 0.9, 0.77),
]
_W_SHAPES = [finger(*c) for c in _W_FINGERS]
_W_FORKS = [(-1.5, -2.2), (-1.55, -0.385), (-1.4, 1.49)]


def _wrap_slit(x, y, end):
    """From a fork back to the knuckles, levelling off as it thins."""
    return [(x, y), (x - 1.2, y - 0.33), (x - 2.2, y - 0.47), (end, y - 0.52)]


WRAP = dict(
    outline=[[
        # the arm's lower edge, the little-finger side of the hand
        (-21.5, -4.95), (-19.0, -4.0), (-16.6, -3.1), (-14.6, -2.5), (-12.6, -2.72), (-10.2, -3.25),
        (-7.8, -3.86), (-5.6, -4.2), (-3.8, -4.17), (-2.2, -3.8),
        # the fingers, turning at the edge
        *_W_SHAPES[0], (*_W_FORKS[0], 1), *_W_SHAPES[1], (*_W_FORKS[1], 1), *_W_SHAPES[2], (*_W_FORKS[2], 1),
        *_W_SHAPES[3],
        # the index finger's upper edge back along to the fork
        (-2.8, 3.14), (-4.2, 3.2), (-5.3, 3.52, 1),
        # the thumb
        (-4.3, 4.28), (-3.2, 4.62), (-2.42, 4.84), (-1.86, 5.3), (-1.84, 5.92), (-2.36, 6.38),
        (-3.2, 6.5), (-4.4, 6.32), (-6.0, 5.84), (-8.0, 5.12), (-10.0, 4.42), (-12.2, 3.84), (-14.3, 3.52),
        # the arm's upper edge
        (-16.6, 3.18), (-19.0, 2.78), (-21.5, 2.35),
    ]],
    lines=[
        _wrap_slit(*_W_FORKS[0], -4.2), _wrap_slit(*_W_FORKS[1], -4.2), _wrap_slit(*_W_FORKS[2], -4.1),
        # the thumb's fork runs on into the back of the hand
        [(-5.3, 3.52), (-6.0, 3.2), (-6.8, 3.0)],
    ],
    marks=[
        *[nail(c[-1], sub(c[-1], c[-2]), w=2 * w1 * 0.62, L=L, back=0.28)
          for (c, _, w1), L in zip(_W_FINGERS, (0.62, 0.74, 0.76, 0.74))],
        nail((-1.84, 5.66), (0.985, 0.17), w=0.98, L=1.0, back=0.36),
    ],
    joints=dict(front=None, view="back",
                i=[(-5.4, 2.0), (-1.2, 2.5), (0.85, 3.18), (2.55, 3.36)],
                m=[(-5.3, 0.2), (-0.9, 0.68), (1.1, 1.15), (3.0, 1.22)],
                r=[(-5.6, -1.6), (-1.2, -1.2), (0.85, -0.72), (2.75, -0.72)],
                l=[(-6.3, -3.2), (-2.1, -3.05), (0.1, -2.55), (1.6, -2.6)],
                t=[(-9.15, 4.21), (-7.4, 4.6), (-4.2, 5.25), (-1.84, 5.62)],
                crease=(-14.3, 1.0), hand_dir=(0.99, -0.07), across=(0.07, 0.99),
                wrist=(-15.0, 1.1), arm_dir=(0.96, 0.28)),
)


# ---------------------------------------------------------------- the same hands on other holds

# Half crimps on three edges, pulled straight down: only the edge changes. On the
# incut the hand sits higher and the end joint comes down behind the lip.
ANGLE_FLAT = HALF
ANGLE_SLOPING = moved(ANGLE_FLAT, dy=-0.75)
_up = moved(HALF, dy=1.2)
ANGLE_INCUT = dict(_up, outline=[[
    *_up["outline"][0][:13],
    # the knuckle, up to a higher middle joint
    (-4.98, 0.55), (-4.86, 1.35), (-4.55, 2.2), (-3.85, 2.88),
    # over the lip and down behind it
    (-2.8, 2.95), (-1.6, 2.82), (-0.5, 2.52), (0.42, 2.0), (1.1, 1.46), (1.4, 0.94), (1.22, 0.5),
    (0.72, 0.36), (0.12, 0.66), (-0.55, 1.06), (-1.25, 1.32), (-2.0, 1.32), (-2.62, 1.08),
    (-2.94, 0.68), (-3.04, 0.2), (-3.12, -0.52, 1),
    *_up["outline"][0][32:],
]], marks=[
    side_nail((-0.1, 2.3), (1.0, 1.54), (0.2, 1.3), 0.28),
    _up["marks"][1],
    _up["marks"][2],
], joints=dict(_up["joints"], i=[(-4.1, -2.2), (-3.65, 2.0), (-1.0, 2.05), (1.4, 0.94)]))


# Fingertips on the dome's shoulder, the palm off it: the hand comes up from the lower
# left, the wrist flexed, the thumb tucked against the index finger.
def _film_hand(outline, line, marks, joints):
    return dict(outline=[outline], lines=[line], marks=marks, joints=joints)


FILM_CATCH = _film_hand([
    # the arm's upper edge, leaving the frame on the left
    (-17.0, -11.8), (-15.2, -8.9), (-14.1, -7.0), (-13.5, -5.55),
    # the back of the hand, the knuckle
    (-12.9, -4.1), (-12.1, -2.0), (-11.2, 0.1), (-10.45, 1.6), (-9.72, 2.72),
    # the first segment, the middle joint
    (-9.0, 3.42), (-7.85, 4.45), (-6.85, 5.5), (-6.15, 6.25),
    # along the top, the end segment curling down on to the dome's shoulder
    (-5.25, 6.5), (-4.1, 6.42), (-3.1, 6.14), (-2.2, 5.52), (-1.46, 4.76), (-1.04, 4.1), (-1.24, 3.56),
    (-1.72, 3.42),
    # the pad, the underside, the crook
    (-2.35, 3.88), (-2.95, 4.28), (-3.6, 4.82), (-4.7, 4.82), (-5.6, 4.5),
    # the first segment's palm side, to the thumb's tip
    (-6.2, 3.7), (-6.72, 3.1, 1),
    # the thumb's tip, its outer edge, the ball of the thumb
    (-6.1, 3.3), (-5.48, 3.05), (-5.22, 2.3), (-5.08, 1.3), (-5.34, 0.2), (-6.06, -1.17),
    (-7.08, -2.86), (-7.9, -4.37), (-8.7, -5.75), (-9.4, -6.9), (-9.75, -7.5),
    # the arm's lower edge
    (-10.5, -8.95), (-11.5, -11.0), (-12.75, -13.4), (-14.1, -15.7),
], [(-6.72, 3.1), (-7.0, 2.5), (-7.2, 1.6), (-7.35, 0.6), (-7.65, -0.35), (-8.0, -1.05)],
    [nail((-5.92, 3.32), (-0.06, 1.0), w=1.0, L=1.12),
     side_nail((-2.25, 5.56), (-1.22, 4.44), (-2.2, 4.6), 0.28),
     [(-9.75, -7.5), (-10.35, -7.42), (-11.1, -7.08)]],
    dict(front="i", i=[(-8.24, 2.14), (-5.8, 5.62), (-3.36, 5.41), (-1.2, 3.8)],
         t=[(-9.5, -3.5), (-7.2, -1.3), (-6.0, 0.6), (-5.92, 3.32)],
         crease=(-11.6, -6.3), hand_dir=(0.375, 0.927), wrist=(-12.0, -7.0),
         arm_dir=(0.545, 0.838)))

# The pads dragged on to the top, the palm nearer.
FILM_DRAG = _film_hand([
    (-17.5, -11.8), (-15.8, -9.0), (-14.7, -7.0), (-14.0, -5.5),
    (-13.12, -4.09), (-12.11, -2.08), (-11.17, -0.17), (-10.35, 1.28), (-9.42, 2.72),
    (-8.4, 3.42), (-7.2, 4.28), (-6.0, 5.08), (-5.02, 5.66),
    (-4.15, 6.08), (-3.0, 6.2), (-1.8, 6.02), (-0.65, 5.6), (0.2, 5.14), (0.52, 4.68), (0.26, 4.26),
    (-0.2, 4.1),
    (-1.0, 4.12), (-2.0, 4.38), (-3.0, 4.52), (-4.0, 4.36), (-4.7, 3.92),
    (-5.3, 3.2), (-5.7, 2.6, 1),
    (-5.05, 2.78), (-4.42, 2.44), (-4.18, 1.5), (-4.32, 0.4), (-4.9, -0.8),
    (-5.65, -1.62), (-6.55, -2.6), (-7.45, -3.6), (-8.45, -4.92), (-9.3, -6.1), (-10.0, -7.2),
    (-10.75, -8.5), (-12.0, -10.4), (-13.4, -12.4), (-14.8, -14.5),
], [(-5.7, 2.6), (-6.12, 2.0), (-6.42, 1.0), (-6.62, 0.1), (-6.92, -0.6), (-7.3, -1.3)],
    [nail((-5.02, 2.78), (-0.04, 1.0), w=1.12, L=1.12),
     side_nail((-0.8, 5.66), (0.32, 5.02), (-0.4, 4.7), 0.28),
     [(-10.0, -7.2), (-10.55, -7.1), (-11.2, -6.75)]],
    dict(front="i", i=[(-7.76, 2.36), (-4.6, 5.2), (-2.17, 5.45), (0.5, 4.7)],
         t=[(-9.5, -3.5), (-7.2, -1.1), (-5.4, 0.3), (-4.95, 2.76)],
         crease=(-12.0, -5.7), hand_dir=(0.47, 0.883), wrist=(-12.5, -6.4),
         arm_dir=(0.56, 0.83)))

_SLOPER_DIAG_BACK = [(-14.7, -18.76), (-13.4, -15.46), (-12.3, -12.76), (-11.36, -10.38), (-10.6, -8.6)]
_SLOPER_DIAG_FRONT = [(-6.6, -9.7), (-7.2, -11.5), (-8.0, -14.0), (-9.0, -17.0), (-9.7, -19.0)]
FILM_PALM = dict(SLOPER, outline=[_SLOPER_DIAG_BACK + SLOPER_TOP + SLOPER_THUMB + _SLOPER_DIAG_FRONT],
                 marks=SLOPER_MARKS[:2] + [[(-6.6, -9.7), (-7.25, -9.95), (-8.0, -9.9)]],
                 joints=dict(SLOPER["joints"], arm_dir=(0.34, 0.94)))

# The thumb has gone under the hold, making a C round its corner, like the pinch. The palm
# stays over the dome where frame 3 put it, and frame 3's inner thumb line is now the palm's
# edge. The thumb runs under the hold's lower face with the pad up, as long as in frame 3.
# Its upper edge lies on that face from the web on, so the two are one line, and the web
# needs no line of its own.
_UNDER_THUMB = SLOPER_TOP[:-1] + [
    # the web, down the palm's edge to the hold's lower face
    (-3.8, 0.35), (-3.86, -0.4), (-4.0, -1.3), (-4.18, -2.2), (-4.36, -3.0), (-4.56, -3.8),
    (-4.7, -4.6), (-4.72, -5.15, 1),
    # the thumb's upper edge, on the hold, and its tip clear of the slope to the wall
    (-4.4, -5.19), (-3.7, -5.27), (-2.9, -5.36), (-2.1, -5.44), (-1.41, -5.53), (-1.0, -5.6), (-0.58, -5.76),
    (-0.14, -6.02), (0.22, -6.46), (0.38, -6.98), (0.18, -7.44), (-0.3, -7.72),
    # its lower edge tilts down with the slope, so the tip keeps a thumb's width, then into the ball
    (-0.95, -7.82), (-1.8, -7.78), (-2.6, -7.8), (-3.4, -7.98), (-4.2, -8.38), (-4.8, -8.9),
    (-5.2, -9.3),
]
_UNDER_MARKS = [
    SLOPER_MARKS[0],
    side_nail((-0.9, -7.82), (0.22, -7.42), (-0.35, -7.0), 0.28),
]
_UNDER_JOINTS = dict(t=[(-7.0, -8.4), (-4.0, -6.95), (-1.7, -6.85), (0.38, -7.0)])
FILM_THUMB = dict(SLOPER, outline=[_SLOPER_DIAG_BACK + _UNDER_THUMB + [
    (-5.8, -9.85), (-6.5, -10.8), (-7.15, -12.05), (-8.0, -14.0), (-9.0, -17.0), (-9.7, -19.0),
]], lines=[],
    marks=_UNDER_MARKS + [[(-6.0, -10.13), (-6.65, -10.35), (-7.4, -10.25)]],
    joints=dict(SLOPER["joints"], arm_dir=(0.34, 0.94), **_UNDER_JOINTS))

# The wrist has dropped. The hand rolls on over the dome about the middle joint, with the
# finger's other two segments still lying on the top, so the crease comes about 0.8 cm lower
# than in frames 3 and 4. The thumb keeps its spot. The arm hangs a little off plumb, with a
# long curve from the thumb, not a corner like a sock's heel.
FILM_HANG = dict(SLOPER, outline=[[
    # the arm's back, the back of the hand, the knuckle
    (-10.65, -19.0), (-10.4, -16.0), (-9.98, -13.0), (-9.64, -11.0), (-9.28, -9.6),
    (-8.9, -8.15), (-8.46, -6.38), (-7.94, -4.51), (-7.4, -2.73), (-6.93, -1.21), (-6.36, -0.16),
    # the first segment, the middle joint, the top of the finger
    (-5.37, 1.44), (-4.42, 2.83), (-3.78, 3.53), (-3.02, 4.26), (-1.84, 5.02), (-0.65, 5.4),
    (0.44, 5.54), (1.05, 5.38), (1.33, 4.95), (1.11, 4.44), (0.56, 4.2),
    # the pad and the underside on the dome
    (-0.12, 4.0), (-1.18, 3.59), (-2.11, 2.97), (-2.86, 2.2), (-3.33, 1.35), (-3.66, 0.62),
    # the web, down the palm's edge to the hold's lower face
    (-3.84, 0.14), (-3.82, -0.67), (-3.82, -1.58), (-3.86, -2.49), (-3.92, -3.31), (-4.02, -4.13),
    (-4.08, -4.8), (-4.08, -5.23, 1),
    # the thumb's upper edge, on the hold, and its tip clear of the slope to the wall
    (-3.7, -5.27), (-2.9, -5.36), (-2.09, -5.44), (-1.41, -5.53), (-0.73, -5.72), (-0.21, -6.05),
    (0.29, -6.41), (0.6, -6.96), (0.42, -7.46), (-0.1, -7.76),
    # its lower edge, into the ball of the thumb, and the arm's front
    (-0.85, -7.84), (-1.7, -7.8), (-2.5, -7.86), (-3.2, -8.1), (-3.8, -8.6), (-4.3, -9.3),
    (-4.72, -10.1), (-5.02, -11.1), (-5.26, -12.3), (-5.42, -13.6), (-5.56, -15.5), (-5.9, -19.0),
]], lines=[], marks=[
    side_nail((-0.4, 5.44), (0.98, 5.42), (0.3, 4.78), 0.3),
    side_nail((-0.8, -7.84), (0.42, -7.46), (-0.12, -7.0), 0.28),
    [(-4.8, -10.3), (-5.5, -10.52), (-6.3, -10.42)],
], joints=dict(SLOPER["joints"], i=[(-5.3, -0.97), (-3.41, 2.83), (-1.42, 4.3), (1.31, 4.97)],
               t=[(-6.6, -8.9), (-3.6, -6.95), (-1.3, -6.9), (0.6, -7.0)],
               crease=(-7.39, -9.78), hand_dir=(0.225, 0.975), wrist=(-7.43, -10.69), arm_dir=(0.09, 0.996)))


# ---------------------------------------------------------------- latching

# Open, a little above the lip: the fingers carry on, only a little bent.
LATCH_OPEN = moved(dict(
    outline=[[
        # the forearm's back, wrist, back of the hand
        (-7.1, -20.0), (-6.5, -17.8), (-6.02, -15.4), (-5.68, -13.4), (-5.5, -12.1),
        (-5.45, -11.2), (-5.5, -9.5), (-5.56, -7.5), (-5.6, -5.5), (-5.56, -4.0),
        # the knuckle, the first segment
        (-5.3, -2.85), (-4.8, -1.5), (-4.25, -0.1), (-3.72, 1.3),
        # the middle joint, and on to the tip
        (-3.2, 2.3), (-2.35, 3.14), (-1.3, 3.84), (-0.3, 4.3), (0.55, 4.62), (1.16, 4.6), (1.44, 4.14),
        (1.2, 3.58),
        # the underside
        (0.5, 3.1), (-0.36, 2.56), (-1.16, 1.96), (-1.84, 1.3),
        # the first segment's palm side
        (-2.2, 0.3), (-2.4, -1.0), (-2.32, -2.4), (-2.12, -3.5),
        (-2.14, -4.9, 1),
        # up the thumb's inner edge, round its tip, down its outer edge
        (-1.9, -4.1), (-1.76, -3.2), (-1.66, -2.4), (-1.42, -1.72), (-0.8, -1.44),
        (-0.2, -1.72), (0.14, -2.45), (0.2, -3.5), (0.0, -4.7), (-0.45, -6.0), (-0.8, -7.4),
        # the heel, the wrist's notch, the forearm's front
        (-0.9, -8.5), (-0.95, -9.8), (-1.08, -11.0), (-1.18, -11.7),
        (-1.18, -12.8), (-1.3, -15.0), (-1.55, -17.8), (-2.0, -20.0),
    ]],
    lines=[[(-2.14, -4.9), (-2.42, -5.45), (-2.6, -6.0)]],
    marks=[
        side_nail((-0.1, 4.38), (1.26, 4.54), (0.6, 3.9), 0.3),
        nail((-0.8, -1.44), (0.0, 1.0), w=1.12, L=1.12, off=-0.02),
        [(-1.18, -11.7), (-1.9, -11.95), (-2.7, -11.95)],
    ],
    joints=dict(front="i", i=[(-3.85, -2.65), (-2.8, 1.5), (-0.6, 3.5), (1.36, 4.14)],
                t=[(-2.4, -10.0), (-1.7, -7.4), (-0.9, -4.35), (-0.8, -1.44)],
                crease=(-3.3, -11.7), hand_dir=(-0.04, 0.999), wrist=(-3.4, -12.6),
                arm_dir=(0.1, 0.995)),
), dx=-0.9)

# Dropped on: the jug hand, on this jug.
_l = moved(JUG, dx=5.4, dy=-1.25)
LATCH_JUG = dict(_l, outline=[[(-2.45, -25.0)] + _l["outline"][0] + [(2.6, -25.0)]])


# ---------------------------------------------------------------- thumb press on a volume

CATCH_RIDGE = dict(
    outline=[[
        # the forearm's back, wrist, back of the hand
        (-9.5, -21.0), (-8.85, -18.6), (-8.25, -16.9), (-7.78, -15.6), (-7.52, -14.6),
        (-7.45, -13.5), (-7.5, -11.5), (-7.56, -9.5), (-7.6, -7.5), (-7.56, -6.0),
        # the knuckle, the first segment
        (-7.3, -4.85), (-6.72, -3.3), (-6.1, -1.75), (-5.58, -0.45),
        # the middle joint, the finger lying along the volume's upper face
        (-5.05, 0.38), (-4.13, 0.92), (-3.09, 1.6), (-2.18, 2.28), (-1.42, 2.77), (-0.93, 2.95),
        (-0.5, 2.87), (-0.33, 2.55),
        # its pad on the face, back to the ridge
        (-0.56, 2.03), (-0.96, 1.47), (-1.39, 0.9), (-1.89, 0.27), (-2.4, -0.2), (-3.12, -0.46), (-3.75, -1.0),
        # the first segment's palm side
        (-4.2, -2.3), (-4.34, -3.6), (-4.3, -5.0), (-4.3, -5.8), (-4.42, -6.9, 1),
        # up the thumb's inner edge to its tip on the lower face, down its outer edge
        (-3.72, -6.1), (-3.2, -5.3), (-2.86, -4.5), (-2.58, -3.75), (-2.14, -3.2), (-1.56, -3.02),
        (-1.0, -3.32), (-0.74, -4.1), (-0.8, -5.1), (-1.24, -6.3), (-1.9, -7.5), (-2.55, -8.8),
        # the ball of the thumb, the heel, the wrist's notch, the forearm's front
        (-2.9, -10.2), (-3.0, -11.6), (-3.1, -13.0), (-3.18, -13.9),
        (-3.18, -14.9), (-3.28, -16.5), (-3.52, -18.2), (-4.0, -21.0),
    ]],
    lines=[[(-4.42, -6.9), (-4.68, -7.55), (-4.86, -8.15)]],
    marks=[
        side_nail((-1.87, 2.47), (-0.72, 2.95), (-1.32, 2.11), 0.28),
        # thumbnail, a sliver on the side away from the volume
        side_nail((-2.66, -3.95), (-1.8, -3.06), (-1.8, -3.9), 0.28),
        [(-3.18, -13.9), (-3.9, -14.15), (-4.7, -14.15)],
    ],
    joints=dict(front="i", i=[(-5.85, -4.65), (-4.75, -0.55), (-2.55, 1.05), (-0.37, 2.71)],
                t=[(-4.4, -12.0), (-3.2, -9.0), (-2.0, -5.9), (-1.56, -3.02)],
                crease=(-5.3, -13.9), hand_dir=(-0.04, 0.999), wrist=(-5.4, -14.8),
                arm_dir=(0.22, 0.975)),
)


# The sloper on the 20 degree wall: the same hand, turned with the wall a little less
# than it, the arm still hanging straight down.
_s = moved(dict(SLOPER, outline=[SLOPER_TOP + SLOPER_THUMB]), deg=-10, about=(1.6, 5.1), dx=-1.7, dy=-0.6)
SLOPER20 = dict(_s, outline=[[
    # the arm hanging from the wrist
    (-14.95, -15.5), (-14.8, -13.0), (-14.62, -10.8), (-14.35, -8.8), (-14.0, -7.2),
] + _s["outline"][0] + [
    (-10.0, -7.95), (-10.18, -8.75), (-10.22, -10.0), (-10.1, -12.5), (-10.0, -15.5),
]], marks=_s["marks"][:2] + [[(-10.18, -8.75), (-10.85, -9.0), (-11.6, -8.95)]],
    joints=dict(_s["joints"], crease=(-12.05, -7.98), hand_dir=(0.5, 0.866), wrist=(-12.15, -8.9), arm_dir=(0.03, 1.0)))


# ---------------------------------------------------------------- figures

CLOSE = H.HAND_SCALE
TILE_W, TILE_H = 14.4, 19.4


def tile_x0():
    return WX + 2.4 / CLOSE + 0.01 - TILE_W


def pull(f, x, y, length_=3.4):
    f.arrow([(x, y), (x, y - length_)], kind="force")


# ---------------------------------------------------------------- the model's hands
#
# The hands seen from the thumb side are drawn by handmodel.py: one skeleton with fixed
# bones, posed by the joint angles read off photographs (handmodel.GRIPS), at HAND_SCALE.
# A grip is the same pose wherever it appears; only where it sits on its hold changes.

def grip(name, anchor, at, arm=None, view="side", mirror=None):
    """The model's hand in grip `name`, placed so its point `anchor` lands on `at`. From
    behind (view "back") it is seen a little from above; mirror: the other hand."""
    import handmodel as M
    pose, a = M.GRIPS[name]
    if view == "back":
        # the grip's lean toward the wall, which turns the drawing from the side, tips the
        # hand's back up toward you from behind: the same hand, seen from behind and a little
        # above. `arm` then turns the drawing only
        return M.Hand(pose, view, arm=arm or 0.0, anchor=anchor, at=at, name=name,
                      mirror=(name in M.MIRRORED) if mirror is None else mirror,
                      pitch=M.BACK_PITCH + a)
    return M.Hand(pose, view, arm=a if arm is None else arm, anchor=anchor, at=at, name=name,
                  mirror=(name in M.MIRRORED) if mirror is None else mirror)


def draw_any(f, hand, z=0.0, fill=WHITE, behind=()):
    """Draw an authored hand (a dict) or one of the model's; behind: the outlines of the
    holds behind it."""
    if isinstance(hand, dict):
        draw_hand(f, hand, z, fill)
    else:
        import handmodel as M
        M.draw(f, hand, z=z, fill=fill, behind=behind)


def grip_outline(kind):
    """The outline of a profile grip's hold (H.grip_hold), for what shows through the hand."""
    draw, kw = H.GRIP_HOLD[kind]
    if draw is H.rounded_lip:
        return H.lip_pts(WX, 0, kw.get("depth", 2.6), kw.get("height", 4.0))
    return H.edge_pts(WX, 0, kw.get("depth", 2.0), kw.get("height", 2.6), kw.get("slope", 0.0))


# where each grip sits on its hold in the atlas's tiles and the entry figures
JUG_M = lambda: grip("jug", "i_tip", (WX - 5.7, 0.45))
OPEN_M = lambda: grip("open", "i_pad", (WX - 0.95, 0.12))
HALF_M = lambda: grip("half", "i_pad", (WX - 1.05, 0.02))
# the full crimp's fingertip on the edge and against the wall; the same crimp on the half
# crimp's edge in half-crimp.svg (b)
FULL_M = lambda: grip("full", "i_pad", (WX - 1.11, 0.26))
FULL_ON_HALF_M = lambda: grip("full", "i_pad", (WX - 1.11, 0.16))
SLOPER_M = lambda: grip("sloper", "i_pad", (0.4, 4.25))


def side(hold, hand, y0, y1, x0=None, arrow=None):
    """A side-view figure: wall at x = WX, a hold, a hand."""
    f = H.profile_frame(tile_x0() if x0 is None else x0, y0, y1)
    if hold in ("half", "full", "open"):
        H.grip_hold(f, hold)
        behind = [grip_outline(hold)]
    else:
        f.smooth(hold[0], z=-5, fill=DARK, stroke=INK, sw=0.35, tension=hold[1])
        H.xray_outline(f, hold[0], hold[1])
        behind = [hold[0]]
    draw_any(f, hand, behind=behind)
    if arrow:
        pull(f, *arrow)
    return f


JUG_HOLD = [(WX, -5.0), (WX - 5.0, -4.6), (WX - 7.2, -2.4), (WX - 7.7, 0.8), (WX - 7.2, 1.85),
            (WX - 6.4, 1.6), (WX - 5.6, 0.3), (WX - 2.8, -0.3), (WX, 0.4)]
DOME = [(2.0, 4.9), (0.66, 4.21), (0.19, 4.08), (-0.39, 3.93), (-0.84, 3.8), (-2.63, 2.55),
        (-3.84, 0.33), (-5.03, -2.53), (-5.97, -4.89), (-1.0, -5.6), (2.0, -6.9)]
FILM_DOME = [(2.0, 4.7), (1.4, 4.55)] + DOME[2:]
DOME20 = [(0.2, 5.29), (-0.69, 4.0), (-1.18, 3.96), (-1.77, 3.91), (-2.24, 3.84), (-3.79, 3.17),
          (-4.75, 2.6), (-5.39, 1.83), (-5.89, 1.15), (-6.3, 0.6), (-7.47, -1.64), (-8.8, -3.8),
          (0.98, -5.6), (4.24, -5.8)]
CATCH_ARROW = [(-1.0, -8.0), (-0.25, -5.2)]    # up the thumb, which does the pressing
CATCH_HOLD = [(WX, 0.05), (WX - 1.17, 0.0), (WX - 2.21, -0.35), (WX - 2.6, -1.2),
              (WX - 2.45, -2.0), (WX - 2.2, -2.5), (WX - 1.75, -2.2), (WX - 1.25, -2.3),
              (WX - 1.2, -3.1), (WX - 0.9, -3.65), (WX, -4.2)]
FLAKE = [(WX - x, y) for x, y in
         [(0, -2.7), (1.45, -1.5), (3.05, -0.8), (4.5, -1.45), (5.65, -3.15), (6.4, -3.7),
          (7.1, -2.5), (6.9, 0.35), (4.5, 2.7), (0, 3.4)]]
POCKET_HOLD = [(WX, 4.0), (WX - 3.0, 3.5), (WX - 3.9, 2.0), (WX - 3.9, -1.6),
               (WX - 3.2, -3.8), (WX, -4.4)]
POCKET_CAVE = [(WX - 3.9, 1.75), (WX - 1.2, 1.85), (WX - 0.55, 0.65), (WX - 1.1, -0.95),
               (WX - 3.9, -1.0)]


def panel_jug():
    # the upright hand's middle joint stands higher over the lip than the authored hand's:
    # the tile shows the same hold 1.8 cm lower in a frame of the same size
    return side((JUG_HOLD, 0.35), JUG_M(), -14.895 + 1.8, 4.505 + 1.8, arrow=(WX - 1.4, -5.6))


def panel_open():
    return side("open", OPEN_M(), -17.386, 2.014, arrow=(WX - 0.7, -4.6))


def panel_halft():
    return side("half", HALF_M(), -16.008, 3.392, arrow=(WX - 1.1, -2.8))


def panel_fullt():
    return side("full", FULL_M(), -13.2, 6.2, arrow=(WX - 0.85, -2.8))


CATCH_M = lambda: grip("catch", "i_pad", (WX - 0.95, 0.12))
PRESS_M = lambda: grip("press", "i_pad", (-0.9, 1.6))


def panel_catch():
    f = side((CATCH_HOLD, 0.6), CATCH_M(), -17.386, 2.014)
    f.arrow(CATCH_ARROW, kind="force", head=2.0)
    return f


def panel_sloper():
    f = Fig(tile_x0(), -12.149, tile_x0() + TILE_W, -12.149 + TILE_H, scale=CLOSE)
    wall_side(f, WX, f.y0, f.y1)
    f.smooth(DOME, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.55)
    H.xray_outline(f, DOME, 0.55)
    draw_any(f, SLOPER_M())
    f.arrow([(0.6, -6.893), (0.6, -10.793)], kind="force")
    return f


def pocket_frame(hand, x0, y0, y1):
    f = H.profile_frame(x0, y0, y1)
    f.smooth(POCKET_HOLD, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    H.xray_outline(f, POCKET_HOLD, 0.5)
    f.smooth(POCKET_CAVE, z=-4.9, fill=HOLD_PALE, stroke=INK, sw=0.3, tension=0.5)
    f.line((WX - 3.92, 1.7), (WX - 3.92, -0.95), z=-4.8, sw=0.6, stroke=HOLD_PALE)
    draw_hand(f, hand)
    return f


def panel_pocket():
    f = pocket_frame(POCKET, tile_x0(), -15.0, 4.4)
    pull(f, WX - 1.4, -4.8)
    return f


def pinch_frame(x0, y0, x1, top, letter=True):
    f = Fig(x0, y0, x1, top, scale=CLOSE)
    w = f.mm(2.4)
    d = max(w, top)
    f.poly([(x0, 0.0), (x1, 0.0), (x1, d), (x0, d)], z=-20, fill=PALE, stroke=None)
    f.line((x0, 0.0), (x1, 0.0), z=-19, sw=0.6)
    x = x0
    while x < x1:
        f.line((x, 0.0), (x + f.mm(1.5), w), z=-19, sw=0.18, stroke=MID)
        x += f.mm(1.9)
    if letter:
        f.poly([(x0, 0.03), (x0, top), (x0 + 1.45, top), (x0 + 1.45, 0.03)], z=-18, fill=WHITE,
               stroke=None)
    return f


def block_panel(hand, half, x0, y0, x1, top, letter=True):
    f = pinch_frame(x0, y0, x1, top, letter)
    hold = [(-half, 0), (-half, -4.6), (half, -4.6), (half, 0)]
    f.poly(hold, z=-5, fill=DARK, stroke=INK, sw=0.35)
    H.xray_outline(f, hold)
    draw_hand(f, hand)
    return f


def panel_pinch():
    f = block_panel(PINCH, 1.5, -7.323, -18.47, 7.077, 0.93, letter=False)
    f.arrow([(1.5 + 2.75 + 2.6, -2.6), (1.5 + 2.75, -2.6)], kind="force")
    f.arrow([(-1.5 - 2.1 - 2.6, -3.5), (-1.5 - 2.1, -3.5)], kind="force")
    return f


# In the plate's tile the wrist falls in the clipped corner, where its crease would read as
# a stray fork.
UNDER_TILE = dict(UNDER, marks=UNDER["marks"][:2])


def panel_under():
    f = H.profile_frame(tile_x0(), 4.3 - TILE_H, 4.3)
    f.smooth(FLAKE, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.45)
    H.xray_outline(f, FLAKE, 0.45)
    # the index's tip on the lip's inner face
    draw_any(f, grip("under", "i_tip", (WX - 4.85, -2.2)))
    f.arrow([(WX - 8.0, -2.4), (WX - 11.0, -0.8)], kind="force")
    return f


def panel_palm():
    x0, y1 = -10.077, 16.902
    f = Fig(x0, y1 - TILE_H, x0 + TILE_W, y1, scale=CLOSE)
    a, b = (x0 - 2, y1 - 6.0), (x0 + 5.6, y1 + 2)
    c, d = (x0 + TILE_W + 2, y1 - TILE_H - 2), (x0 - 2, y1 - TILE_H - 2)
    e = (x0 + TILE_W + 2, y1 + 2)
    f.poly([a, b, e, c, d], z=-12, fill=VOLUME, stroke=INK, sw=0.35)
    f.poly([a, b, (x0 - 2, y1 + 2)], z=-11.9, fill=VOLUME, stroke=INK, sw=0.35)
    # the model's right hand from behind, flat on the face, which is seen three quarters on:
    # the hand's length shows 0.92 of itself (hand-proportions.md), the view tipped 23 degrees.
    # Its wrist crease where the authored hand's was, leaning 8 degrees the same way
    import handmodel as M
    pose, _ = M.GRIPS["press_palm"]
    draw_any(f, M.Hand(pose, "back", arm=PALM_LEAN, anchor="crease", at=PALM_AT, mirror=True,
                       pitch=PALM_PITCH, name="press_palm"))
    f.arrow([(1.357, 4.69), (-0.653, 1.951)], kind="force", z=50)
    return f


def panel_half():
    return side("half", HALF, -18.985, 7.98, x0=-12.0)


def panel_full():
    return side("full", FULL, -15.453, 8.21, x0=-12.0)


# ---------------------------------------------------------------- the figures

def seg_angle(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def pip_arc(f, hand, label, at=None, r=1.5, stop=None):
    """The middle joint's flexion, labelled up and to the left of it: a dashed line where
    the finger would go if the joint were straight and an arc from it to the middle segment.
    stop: the direction the arc stops at, where it would otherwise run on inside the finger.
    No white round them, which would cut the finger's outline."""
    m, p, d, _ = hand["joints"]["i"]
    a0, a1 = seg_angle(m, p), seg_angle(p, d)
    f.line(p, add(p, mul(ang(a0), r + 0.7)), z=40.1, sw=0.28, dash=(0.8, 0.5))
    n = 16
    a1 = a1 if stop is None else stop
    pts = [add(p, mul(ang(a0 + (a1 - a0) * i / n), r)) for i in range(n + 1)]
    f.poly(pts, closed=False, z=40.1, sw=0.2, stroke=INK)
    f.text(label, at or add(p, (-2.6, 2.4)), size=7, z=41)


def pip_arc_m(f, hand, label, at=None, r=1.5):
    """pip_arc for the model's hand: the arc stops where it meets the middle segment's back."""
    import handmodel as M
    m, p, d = (hand.spot(f"i{k}") for k in range(3))
    a0, a1 = seg_angle(m, p), seg_angle(p, d)
    half = M.SECTION[1][1] / 2
    stop = a1 + math.copysign(math.degrees(math.asin(min(0.95, half / r))), a0 - a1)
    f.line(p, add(p, mul(ang(a0), r + 0.7)), z=40.1, sw=0.28, dash=(0.8, 0.5))
    n = 16
    pts = [add(p, mul(ang(a0 + (stop - a0) * i / n), r)) for i in range(n + 1)]
    f.poly(pts, closed=False, z=40.1, sw=0.2, stroke=INK)
    f.text(label, at or add(p, (-2.6, 2.4)), size=7, z=41)


def label_lines(f, lines, at, to=None, size=7):
    """As figs_hands.label_lines: short lines centred under `at`, the leader
    leaving from the first."""
    step = f.pt(size) * 1.15
    if to is not None:
        v = norm(sub(to, at))
        down = v[1] < 0
        hw = max(len(s) for s in (lines if down else lines[:1])) * f.pt(size) * 0.53 / 2
        hh = f.pt(size) * 0.45 + (step * (len(lines) - 1) if down else 0)
        t = min(hw / max(abs(v[0]), 1e-6), hh / max(abs(v[1]), 1e-6)) + f.mm(0.5)
        f.label(lines[0], at, to=to, size=size, anchor="middle", gap=t * f.scale / 1.6)
    else:
        f.text(lines[0], at, size=size, z=60)
    for i, s in enumerate(lines[1:], 1):
        f.text(s, (at[0], at[1] - step * i), size=size, z=60)


GRIP_X0, HALF_Y1, FULL_Y1 = -12.0, 7.98, 8.21
HALF_Y0, FULL_Y0 = -18.985, -15.453       # the old frames, so the figures keep their size


def half_crimp_fig(path):
    h = HALF_M()
    a = side("half", h, HALF_Y0, HALF_Y1, x0=GRIP_X0)
    pip_arc_m(a, h, "≈90°")
    label_lines(a, ["end joint", "straight"], (-9.2, 1.6), to=h.spot("i2"))
    # the full crimp of full-crimp.svg and the atlas, on the same edge as (a)
    g = FULL_ON_HALF_M()
    b = side("half", g, HALF_Y0, HALF_Y1, x0=GRIP_X0)
    pip_arc_m(b, g, "over 90°", at=add(g.spot("i1"), (-3.2, 2.1)))
    label_lines(b, ["end joint", "bent back"], (-0.8, 7.2), to=g.spot("dent"))
    combine([a, b], path, gap=4, labels=["a", "b"], align="top",
            captions=["half crimp", "full crimp, for comparison"])


A2_FULL = (-3.45, 0.55)
HALF_ARC_STOP = 33.0    # on the finger's back, short of the label's leader
FULL_ARC_STOP = -8.0    # just short of the middle segment's back
OPEN_ARC_STOP = 50.0    # on the finger's back


def full_crimp_fig(path):
    h = FULL_M()
    a = side("full", h, FULL_Y0, FULL_Y1, x0=GRIP_X0)
    pip_arc_m(a, h, "over 90°", at=add(h.spot("i1"), (-2.6, 2.4)))
    label_lines(a, ["end joint", "bent back"], (-9.2, 3.5), to=h.spot("dent"))
    label_lines(a, ["A2", "pulley"], (-9.9, -2.6), to=h.spot("a2"))
    a.label("thumb over the nail", (0.9, 7.6), to=h.spot("thumbnail"), anchor="end")
    a.save(path)


def atlas_rows():
    """The plate's ten tiles, as figs_hands.grid wants them."""
    return [[(panel_jug(), "jug"), (panel_open(), "open hand"), (panel_halft(), "half crimp"),
             (panel_fullt(), "full crimp"), (panel_pocket(), "pocket (two fingers)")],
            [(panel_sloper(), "sloper"), (panel_pinch(), "pinch (from above)"),
             (panel_under(), "undercling"), (panel_catch(), "thumb catch"),
             (panel_palm(), "palm press")]]


def face_edge(f, c, w, h, rounded=False, z=-5, stripe_to=None):
    """A horizontal edge seen face-on (a long bar), centred on c. stripe_to: where the
    light stripe along its top stops, if not at the far end."""
    x, y = c
    r = h * (0.5 if rounded else 0.25)
    pts = [(x - w / 2 + r, y + h / 2), (x + w / 2 - r, y + h / 2),
           (x + w / 2, y), (x + w / 2 - r, y - h / 2), (x - w / 2 + r, y - h / 2),
           (x - w / 2, y)]
    f.smooth(pts, z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    H.xray_outline(f, pts, 0.5)
    f.line((x - w / 2 + r, y + h * 0.3), (stripe_to or x + w / 2 - r, y + h * 0.3), z=z + 0.1,
           sw=0.55, stroke=WHITE)


def open_side():
    a = H.profile_frame(GRIP_X0, -20.354, 8.29)
    H.grip_hold(a, "open")
    h = OPEN_M()
    draw_any(a, h)
    pip_arc_m(a, h, "≈40°", r=2.6)
    a.label("pads over the lip", (-4.0, 7.4), to=h.spot("pads"), anchor="middle")
    return a


# low enough that the curled little finger clears the hold
OPEN_BACK_AT = dict(dx=0.95, dy=-14.3, deg=1.5, about=(0.0, 0.0))


def open_back():
    # as tall as (a), so that the arm runs to the same line above the caption
    b = Fig(-7.6, -23.444, 11.6, 5.2, scale=CLOSE)
    face_edge(b, (0.2, 0.0), 14.6, 3.4, rounded=True)
    # the three-finger drag from behind: (a)'s hand, its index's pad on the edge's top
    hand = grip("drag3", "i_pad", (0.2, 1.5), view="back", mirror=True)     # the right hand
    draw_any(b, hand)
    label_lines(b, ["little", "finger off"], (9.6, -3.6), to=hand.flat(hand.skel.joints("l")[1]))
    return b


def open_hand_fig(path):
    combine([open_side(), open_back()], path, gap=4, labels=["a", "b"], align="top",
            captions=["drag, side view", "three-finger drag"])


def pocket_a():
    f = pocket_frame(POCKET, -14.2, -18.737, 5.65)
    label_lines(f, ["little finger", "parallel"], (-11.2, -1.0), to=POCKET["joints"]["label"])
    return f


def pocket_b():
    f = pocket_frame(POCKET_CURLED, -14.2, -18.737, 5.65)
    f.arrow([(-5.3, 1.9), (-2.75, 2.38)], kind="force", z=50)
    # the curled finger's pull, the opposite way, from its tip across the back of the hand
    f.arrow([(-5.95, -5.3), (-8.1, -5.3)], kind="force", z=50, head=2.0)
    label_lines(f, ["opposite", "pulls"], (-10.9, 3.1), to=(-5.65, 1.85))
    label_lines(f, ["little finger", "curled"], (-11.2, -1.0), to=POCKET_CURLED["joints"]["label"])
    return f


def pocket_fig(path):
    # within the 92 mm that sit beside the steps
    combine([pocket_a(), pocket_b()], path, gap=2.5, align="top",
            labels=["a", "b"], captions=["safer", "stronger but riskier"])


def pinch_a():
    f = block_panel(PINCH, 1.5, -9.644, -18.88, 7.42, 1.75)
    f.arrow([(6.85, -2.6), (4.25, -2.6)], kind="force")
    f.arrow([(-6.2, -3.5), (-3.6, -3.5)], kind="force")
    f.text("wall", (6.42, 0.75), size=7)
    f.label("thumb", (-8.6, -6.2), to=(-2.62, -4.73), size=7, gap=2.0)
    f.label("index", (5.2, -12.6), to=(5.03, -4.76), size=7)
    return f


def pinch_b():
    f = block_panel(PINCH_WIDE, 3.0, -11.569, -18.88, 7.94, 1.75)
    f.arrow([(7.7, -2.2), (5.1, -2.2)], kind="force")
    f.arrow([(-7.7, -3.8), (-5.1, -3.8)], kind="force")
    return f


def pinch_c():
    f = pinch_frame(-14.112, -18.88, 7.94, 1.75)
    hold = [(-8.0, 0), (0.0, -7.0), (8.0, 0)]
    f.poly(hold, z=-12, fill=VOLUME, stroke=INK, sw=0.35)
    H.xray_outline(f, hold)
    draw_hand(f, PINCH_RIDGE)
    f.arrow([(7.16, -6.98), (5.45, -5.02)], kind="force")
    f.arrow([(-6.63, -5.32), (-4.92, -3.36)], kind="force")
    return f


def pinch_fig(path):
    combine([pinch_a(), pinch_b(), pinch_c()], path, gap=3, labels=["a", "b", "c"],
            captions=["narrow pinch", "wide pinch", "volume edge"])


def catch_a():
    f = H.profile_frame(-13.5, -20.354, 5.81)
    f.smooth(CATCH_HOLD, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.6)
    H.xray_outline(f, CATCH_HOLD, 0.6)
    draw_any(f, CATCH_M())
    f.arrow(CATCH_ARROW, kind="force", head=2.0)
    f.arrow([(0.6, 3.59), (0.6, 1.59)], kind="force")
    label_lines(f, ["thumb in", "a dimple"], (-10.6, -6.2), to=(0.0, -4.5))
    return f


def catch_b():
    f = H.profile_frame(-13.5, -20.232, 5.81)
    f.poly([(WX, 5.0), (WX - 4.4, -0.6), (WX, -9.0)], z=-12, fill=VOLUME, stroke=INK, sw=0.35)
    h = PRESS_M()
    draw_any(f, h)
    f.arrow([(-2.9, -6.6), (-2.1, -4.05)], kind="force")
    label_lines(f, ["thumb pad", "presses up"], (-10.95, -8.2), to=h.flat(h.skel.digits["t"][2][0].at(1.7, 0.0, -0.5)))
    return f


def thumb_catch_fig(path):
    combine([catch_a(), catch_b()], path, gap=4, labels=["a", "b"], align="top",
            captions=["thumb catch", "thumb press on a volume"])


# tilted a little and high enough for the little finger to reach the hold's top edge
REGRIP_DRAG, REGRIP_CRIMP = dict(dx=-3.75, dy=-10.8, deg=2.5), dict(dx=4.9, dy=-9.2)
# the model's hands from behind: where the middle finger's middle joint sits on the edge
REGRIP_DRAG_AT, REGRIP_CRIMP_AT = (-3.3, 3.75), (5.3, 3.75)


def regrip_panel(k):
    f = Fig(-11, -16.755, 11, 9.74, scale=CLOSE)
    # the stripe stops under the hand in panel 2, or it would show in the gaps where
    # panel 1 has the incut
    face_edge(f, (0, 2.0), 21, 3.2, stripe_to=None if k == 0 else 1.6)
    # the drag from behind, the middle finger's middle joint at the edge's top
    drag = grip("drag", "m1", REGRIP_DRAG_AT, view="back", mirror=True)     # the right hand
    if k == 0:
        # the incut sweet spot on the right half, a screw hole beside it. Panel 2 leaves them
        # out: its hand covers them, and the incut would only show as black blocks in the gaps.
        f.poly([(1.8, 3.3), (8.5, 3.3), (8.0, 2.7), (2.3, 2.7)], z=-4.8, fill=INK, stroke=None)
        f.circle((5.2, 1.5), 0.45, z=-4.8, fill="#b0b0b0", stroke=INK, sw=0.25)
        draw_any(f, drag)
        f.circle((5.2, 1.5), 1.6, z=40, stroke=INK, sw=0.3, fill=None)
        label_lines(f, ["aim at the", "screw hole"], (7.2, -3.4), to=(5.2, -0.1))
        label_lines(f, ["incut"], (7.4, 5.6), to=(7.4, 3.0))
    else:
        # the half crimp of the side views, from behind, in the incut
        crimp = grip("half", "m1", REGRIP_CRIMP_AT, view="back", arm=0.0, mirror=True)
        import handmodel as M
        M.draw(f, drag, z=-3, ghost=True)
        draw_any(f, crimp)
        f.arrow([(-4.6, 8.1), (0.2, 9.0), (3.4, 8.6)], kind="move")
        label_lines(f, ["half crimp", "in the incut"], (7.9, 9.1), to=crimp.flat(crimp.skel.joints("m")[1]))
    return f


def regrip_fig(path):
    combine([regrip_panel(0), regrip_panel(1)], path, gap=4, labels=["1", "2"], align="top",
            captions=["catch where you can", "walk the fingers to the incut"])


def wrap_panel():
    x0, y0, x1, y1 = -20.11, -10.84, 7.13, 7.06
    f = Fig(x0, y0, x1, y1, scale=CLOSE)
    low, high = (0.0, y0 - 2), (0.0, y1 + 2)
    f.poly([low, high, (x0 - 2, y1 + 2), (x0 - 2, y0 - 2)], z=-20, fill=PALE, stroke=None)
    f.poly([low, high, (x1 + 2, y1 + 2), (x1 + 2, y0 - 2)], z=-20, fill="#cccccc", stroke=None)
    f.line(low, high, z=-19, sw=0.7)
    # the model's right hand from its back, the faces seen straight on, the fingers across
    # the edge; the index's middle joint where the authored hand's was
    import handmodel as M
    pose, arm = M.GRIPS["wrap"]
    hand = M.Hand(pose, "back", arm=arm, anchor="i1", at=(-1.2, 2.5), mirror=True, name="wrap")
    draw_any(f, hand)
    # the edge carries on under the fingers, as a hidden line
    f.poly([low, high], closed=False, z=H.XRAY_Z, **H.XRAY_STYLE)
    f.label("arête", (1.75, 5.9), to=(0.0, 5.2), size=7)
    # to the thumb's knuckle, and to the little finger where it crosses the edge
    f.label("palm and thumb", (-14.51, 5.76), to=hand.flat(hand.skel.joints("t")[1]), size=7)
    L = [hand.flat(j) for j in hand.skel.joints("l")]
    a, b = next((a, b) for a, b in zip(L, L[1:]) if a[0] <= 0.0 <= b[0])
    edge = (0.0, a[1] + (b[1] - a[1]) * (0.0 - a[0]) / (b[0] - a[0]))
    label_lines(f, ["fingers", "round", "the edge"], (3.85, -6.9), to=edge)
    f.arrow([(-10.0, -0.75), (-6.8, -0.4)], kind="force", z=50)
    f.arrow([(6.2, 1.4), (3.6, 1.68)], kind="force", z=50)
    return f


def wrap_fig(path):
    wrap_panel().save(path)


def angle_panel(slope, hand, note):
    # the figure is about the edges, so it stops just below the wrist; one length of arm
    # in all three, so the hands look one size
    y0 = -12.43
    f = H.profile_frame(-9.6, y0, 7.03)
    H.edge_profile(f, WX, 0, depth=3.2, height=3.6, slope=slope)
    draw_any(f, hand)
    f.arrow([(WX - 0.85, -3.9), (WX - 0.85, -6.6)], kind="force")
    if slope > 0:
        # above the finger and along the slope: the gap under the finger has no room for it
        f.arrow([(1.25, 2.55), (-0.9, 1.31)], kind="move", z=45)
    f.text(note, (-2.6, 6.13), size=7)
    return f


def angle_a():
    # the end joint curls down behind the lip, toward the corner at the wall
    return angle_panel(-20, grip("half_incut", "i_tip", (WX - 0.25, 0.8)), "incut locks it")


def angle_b():
    return angle_panel(0, grip("half", "i_pad", (WX - 1.05, 0.02)), "friction and curl")


def angle_c():
    # the same hand as on the flat edge, a little lower: it slides off down the slope
    return angle_panel(30, grip("half", "i_pad", (WX - 1.05, -0.6)), "slides off")


def hold_angle_fig(path):
    combine([angle_a(), angle_b(), angle_c()], path, gap=3, align="top",
            captions=["positive (incut)", "flat", "negative (sloping)"])


FILM_ZOOM = 0.73       # the strip is reduced as the atlas is: its frames are drawn at CLOSE
FILM = CLOSE * FILM_ZOOM


def film_frame(hand, arrow=False):
    """One frame of the sloper film strip, drawn at the close-ups' scale. The strip reduces
    it to FILM, as the atlas's plate reduces its tiles."""
    x1 = WX + 2.4 / CLOSE + 0.01
    f = Fig(x1 - 31.3 / FILM, -17.4, x1, 7.6, scale=CLOSE)
    H.wall_profile(f, WX, f.y0, f.y1)
    f.smooth(FILM_DOME, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.55)
    H.xray_outline(f, FILM_DOME, 0.55)
    draw_any(f, hand)
    if arrow:
        f.arrow([(0.6, -8.1), (0.6, -11.9)], kind="force")
    return f


# where the hand sits on the dome: the fingertips on its top, then its pads, as the atlas's sloper
FILM_TIP, FILM_PAD = (0.9, 4.45), (0.4, 4.25)


def film_1():
    return film_frame(grip("film_catch", "i_tip", FILM_TIP))


def film_2():
    return film_frame(grip("film_drag", "i_pad", FILM_PAD))


def film_3():
    return film_frame(grip("film_palm", "i_pad", FILM_PAD))


def film_4():
    return film_frame(grip("film_thumb", "i_pad", FILM_PAD))


def film_5():
    # the fingertips rolled onto the dome's upper shoulder
    return film_frame(grip("film_hang", "i_pad", (-2.0, 3.3)), arrow=True)


def filmstrip_fig(path):
    # the hand's line keeps the climbers' weight though the strip is reduced
    H.LINE[0] = 1 / FILM_ZOOM
    frames = [film_1(), film_2(), film_3(), film_4(), film_5()]
    H.LINE[0] = 1.0
    filmstrip(frames, path, zoom=FILM_ZOOM, captions=[
        "catch with\nthe fingertips", "drag the pads over", "bring the palm on",
        "find a thumb\nspot below", "wrist below,\nhang low"])


def sloper_panel():
    f = Fig(-16.605, -13.269, 5.4, 9.0, scale=CLOSE)
    A = 20
    x_at = lambda y: rot((WX, 0), A)[0] - (y - rot((WX, 0), A)[1]) * math.tan(math.radians(A))
    wall_side(f, x_at(f.y0), f.y0, f.y1, angle=A)
    f.smooth(DOME20, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.55)
    H.xray_outline(f, DOME20, 0.55)
    # the atlas's sloper, turned 10 degrees with the wall
    h = grip("sloper", "i_pad", (-1.0, 4.3), arm=10.0)
    draw_any(f, h)
    f.arrow([(0.6, -6.18), (0.6, -10.08)], kind="force")
    # the palm side of the hand, between the finger's base and the ball of the thumb
    f.label("palm and pads", (-5.2, 7.8), to=h.flat(h.skel.H((1.0, 7.6, -2.1))))
    f.label("wrist below", (-4.6, -11.67), to=h.flat(h.point("crease")))
    return f


def latch_a(jug_profile):
    y0 = -18.438
    f = Fig(-10.5, y0, 7.5 + 2.4 / CLOSE, 9.5, scale=CLOSE)
    H.wall_profile(f, 6.5, y0, 9.5)
    jug_profile(f, (0, 0))
    # the fingertips 2-3 cm above the lip
    h = grip("latch", "i_tip", (0.9, 3.2))
    draw_any(f, h)
    f.arrow([(4.4, 6.6), (4.4, 0.8)], kind="move")
    f.label("2–3 cm above", (-2.9, 8.0), to=h.spot("pads"), size=7)
    return f


def latch_b(jug_profile):
    y0 = -18.548
    f = Fig(-10.5, y0, 7.5 + 2.4 / CLOSE, 9.5, scale=CLOSE)
    H.wall_profile(f, 6.5, y0, 9.5)
    jug_profile(f, (0, 0))
    # the atlas's jug grip, its fingertips on this jug's floor
    h = grip("jug", "i_tip", (1.8, -1.3))
    draw_any(f, h, behind=[[(6.5, -4.5), (1.5, -4.2), (0.1, -2.0), (-0.2, 0.2), (0.25, 0.6), (0.9, -1.3),
                            (2.6, -1.6), (6.5, -0.6)]])
    f.label("fingers over the lip", (-4.0, 8.4), to=h.spot("i2"), size=7)
    return f


def drag_from_behind(side, x, top=0.0):
    """Fingers over an edge whose top is at `top`, seen from behind: the right hand or the
    left one's mirror image, the wrist crease under x."""
    return moved(BACK_DRAG, dx=x, dy=top - 14.9, mirror=side == "l")


def build(out):
    open_hand_fig(out + "/open-hand.svg")
    half_crimp_fig(out + "/half-crimp.svg")
    full_crimp_fig(out + "/full-crimp.svg")
    pinch_fig(out + "/pinch.svg")
    pocket_fig(out + "/pocket.svg")
    thumb_catch_fig(out + "/thumb-catch.svg")
    wrap_fig(out + "/wrap.svg")
    regrip_fig(out + "/regrip.svg")
    hold_angle_fig(out + "/hands-hold-angle.svg")
    filmstrip_fig(out + "/filmstrip-sloper.svg")
