"""One hand for every close-up, built the way an illustrator constructs one: a skeleton
of fixed bones, soft solids over it, posed by joint angles, seen from one of three views
and outlined with the climbers' pen.

Nothing in the book uses this module yet. It is a sample for Simon to judge against the
authored hands in authored.py.

The hand frame, in cm: x toward the thumb side, y along the hand from the wrist joint, z
out of the back of the hand. The forearm runs down -y from the wrist joint. The model is
one hand; a figure mirrors it for the other.

The skeleton (research/hand-proportions.md has the sources):
  radius and ulna end at the wrist joint; the carpus is one block from there to the bases
  of the metacarpals; four finger metacarpals end in heads on the knuckle arc, and the
  thumb's metacarpal starts at its own joint near the wrist (the CMC, on the trapezium);
  phalanges have the lengths below, and with the fingers straight each row of joints lies
  on its own arc, concentric with the knuckles'.

The soft tissue is a set of convex solids: a tapered section round each phalanx with a round
end at each joint, the palm as a rounded slab, the metacarpal heads as the knuckles'
bumps, a pad across the base of the fingers, the ball of the thumb along its metacarpal,
the mass on the little-finger side, the web between thumb and index, and the forearm.

Drawing: each solid is projected and becomes a convex outline. The solids of one piece
(a finger, the thumb, the palm with the forearm) are joined with a smooth minimum, so a
joint's crook gets a fillet, and each finger joins the palm the same way. The outline is
the zero line of that field, traced on a grid and drawn with the climbers' pen. Pieces are
stacked back to front for the view; where a piece lies over one behind it, its own outline
shows as an inner line, except near its root, where it grows out of the palm. Fingers
that lie behind the front one in a side view are grey, as in the authored hands.
"""

import math

from climb import INK, MID, WHITE, add, sub, mul, dot, norm, perp, length, rot
import authored as A
import hand as H

GRID = 0.08             # cm between the samples of a field
FAR = 1.5               # cm: a field is only computed this close to a solid

# ---------------------------------------------------------------- 3D vectors


def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_mul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def v_dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def v_cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def v_len(a):
    return math.sqrt(v_dot(a, a))


def v_norm(a):
    n = v_len(a)
    return v_mul(a, 1.0 / n)


def turn(v, axis, deg):
    """v turned by deg about the unit vector axis (right-hand rule)."""
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    k = axis
    return v_add(v_add(v_mul(v, c), v_mul(v_cross(k, v), s)), v_mul(k, v_dot(k, v) * (1 - c)))


class Frame:
    """An origin and three unit axes: u along the bone, w out of its back, v = u x w,
    which points to the thumb side for the fingers."""

    def __init__(self, o, u, w):
        self.o, self.u, self.w = o, v_norm(u), v_norm(w)
        self.v = v_cross(self.u, self.w)

    def at(self, a, b, c):
        """The point a along u, b along v and c along w."""
        return v_add(self.o, v_add(v_mul(self.u, a), v_add(v_mul(self.v, b), v_mul(self.w, c))))

    def vec(self, a, b, c):
        return v_add(v_mul(self.u, a), v_add(v_mul(self.v, b), v_mul(self.w, c)))

    def turned(self, axis, deg, o=None):
        return Frame(self.o if o is None else o, turn(self.u, axis, deg), turn(self.w, axis, deg))


# ---------------------------------------------------------------- the skeleton
#
# A hand 19 cm from the wrist crease to the tip of the middle finger, 8.5 cm across the
# knuckles (hand-proportions.md). The wrist joint is at the origin and its crease lies over it.
# The bones are Buryanov & Kotiuk 2010's X-ray means (hands-drawing-reference.md), which come
# out at this hand's size: the middle knuckle 9.77 cm from the crease, its phalanges
# 4.46, 2.63 and 1.74 cm and 0.40 cm of pulp past the bone, which ends the finger at 19.0.

DIGITS = "imrl"
# metacarpal heads: the knuckle arc, the index's 0.2 cm behind the middle knuckle, the
# ring's 0.75 and the little finger's 1.35; across the back a low dome, highest at the middle
MC_HEAD = dict(i=(3.2, 9.57, -0.15), m=(1.05, 9.77, 0.0), r=(-1.1, 9.02, -0.12), l=(-3.1, 8.42, -0.45))
# metacarpal bases, from the metacarpals' lengths: 6.81, 6.46, 5.80, 5.37
MC_BASE = dict(i=(2.1, 2.76, 0.1), m=(0.6, 3.31, 0.25), r=(-0.9, 3.22, 0.15), l=(-2.2, 3.05, -0.05))
# phalanges from joint to joint, the last with its pulp: the index and ring tips then end
# level, 1.2 cm short of the middle tip, and the little tip near the ring's end joint, as
# the artists have them
PHALANX = dict(i=(3.98, 2.24, 1.96), m=(4.46, 2.63, 2.14), r=(4.14, 2.57, 2.13), l=(3.27, 1.81, 1.97))
# (breadth, depth) at the base of the first segment, the middle joint, the end joint and
# the fingertip, for the index; the others are scaled by GIRTH. The breadth at the middle
# joint is Kouchi's 0.216 of the knuckles' 8.6 (hand-proportions.md); a breadth up at the US
# hands' 0.23 made the hand from behind read too wide, its fingers touching
SECTION = [(1.95, 2.0), (1.86, 1.8), (1.62, 1.42), (1.43, 1.2)]
GIRTH = dict(i=(1.0, 1.0), m=(1.01, 1.03), r=(0.94, 0.96), l=(0.83, 0.85))
# the fingers fan out a little from the knuckles when straight (degrees, + to the thumb side),
# so from behind they part with slight gaps, as in the photos
SPREAD = dict(i=7.0, m=1.0, r=-6.0, l=-13.0)

# the thumb: its CMC near the wrist on the thumb side, about 1 cm nearer the wrist than the
# index's metacarpal base; metacarpal 4.62, phalanges 3.16 and 2.17 with 0.57 of pulp
# (Buryanov). Laid along the hand its tip ends about 1 cm short of the index's middle joint
# (ANSUR 1988), which this CMC gives.
CMC = (2.4, 2.8, -1.45)
THUMB = (4.62, 3.16, 2.74)
# (breadth, depth): at the CMC, the knuckle, the end joint and the tip; 1.12 times the
# index's breadth and 1.03 its depth (Kouchi 2012)
THUMB_SECTION = [(1.8, 1.5), (2.25, 1.95), (2.15, 1.8), (1.85, 1.3)]
# the thumb at rest, beside the palm: its metacarpal leaves the CMC toward the index's
# knuckle and a little out in front of the palm; turned about 80 degrees to the fingers, so
# its nail faces out to the thumb side
THUMB_U = v_norm((0.3, 0.9, -0.4))
THUMB_W = v_norm((0.85, -0.3, 0.42))

# the forearm: its bones end at the wrist joint. Sections (y, breadth, depth, z of centre)
RADIUS = ((1.9, -25.0, -0.2), (1.95, -0.6, -0.3))
ULNA = ((-2.4, -25.0, 0.4), (-2.55, -1.1, 0.35))
# From behind the forearm stays near the wrist's breadth for a hand's length before it
# widens toward the elbow, as in the photos from behind; it does not flare from the wrist
FOREARM = [(-0.9, 5.8, 4.25, -0.35), (-5.0, 6.75, 4.95, -0.3), (-12.0, 7.2, 5.4, -0.25),
           (-26.0, 7.9, 6.0, -0.2)]
# the palm as a wedge, thicker at the wrist: sections (y, x of centre, breadth, z of centre,
# depth)
PALM = [(-0.2, -0.15, 5.8, -0.425, 4.15), (2.8, -0.15, 7.8, -0.475, 3.85),
        (6.0, 0.0, 8.3, -0.6, 3.45), (8.7, 0.05, 8.35, -0.8, 3.05)]

WRIST_CREASE = (0.0, 0.0, -2.6)
# the ball of the thumb's half-widths across the metacarpal: out to the palm side, and
# along the thumb's back. The side view's mid-palm with it is 4.5-4.9 (hand-proportions.md)
BALL = (1.2, 0.95)
BALL_AT = (1.9, 4.0, -2.6)    # where the ball of the thumb sits on the palm
BALL_LOW = (1.4, 1.0, -2.3)   # and where it tapers off toward the wrist
# how far up the thumb's first segment and the index's the web's free edge runs
WEB = (0.5, 0.4)


def default_pose():
    return dict(wrist=(0.0, 0.0),
                i=(0, 0, None), m=(0, 0, None), r=(0, 0, None), l=(0, 0, None),
                spread=None,
                thumb=dict(cmc=(0.0, 0.0), mcp=10.0, ip=10.0))


def dip_of(pip, dip):
    """The end joint: given, or two thirds of the middle joint in a relaxed curl."""
    return pip * 2.0 / 3.0 if dip is None else dip


class Skeleton:
    """The bones' joints in the forearm's frame for a pose. Each digit is a list of
    frames, one per segment, at the segment's base."""

    def __init__(self, pose):
        P = default_pose()
        P.update(pose)
        self.pose = P
        flex, dev = P["wrist"]
        X, Y, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)
        # wrist: palmar flexion turns the hand toward the palm, deviation toward the thumb
        hx = turn(X, Z, -dev)
        hy = turn(Y, Z, -dev)
        hz = Z
        hy, hz = turn(hy, hx, -flex), turn(hz, hx, -flex)
        self.hand = (hx, hy, hz)

        def H_(p):
            return v_add(v_add(v_mul(hx, p[0]), v_mul(hy, p[1])), v_mul(hz, p[2]))
        self.H = H_
        self.digits, self.lengths = {}, {}
        spread = P.get("spread") or SPREAD
        for k in DIGITS:
            mcp, pip, dip = P[k]
            dip = dip_of(pip, dip)
            base = Frame(H_(MC_HEAD[k]), hy, hz)
            # a turn about the back of the hand's axis: positive spreads toward the thumb
            base = base.turned(hz, -spread[k])
            segs, f = [], base
            for ang, L in zip((mcp, pip, dip), PHALANX[k]):
                f = f.turned(f.v, -ang)
                segs.append((f, L))
                f = Frame(v_add(f.o, v_mul(f.u, L)), f.u, f.w)
            self.digits[k] = segs
            self.lengths[k] = PHALANX[k]
        T = P["thumb"]
        self.thumb_pose = T
        u, w = H_(THUMB_U), H_(THUMB_W)
        c = Frame(H_(CMC), u, w)
        a_flex, a_abd = T["cmc"]
        # CMC flexion swings the thumb across the palm; abduction lifts it out in front
        c = c.turned(v_cross(c.w, c.u), a_flex)
        c = turn_abd(c, a_abd, H_)
        segs, f = [], c
        for ang, L in zip((0.0, T["mcp"], T["ip"]), THUMB):
            f = f.turned(v_cross(f.w, f.u), ang)
            segs.append((f, L))
            f = Frame(v_add(f.o, v_mul(f.u, L)), f.u, f.w)
        self.digits["t"] = segs
        self.lengths["t"] = THUMB

    def joints(self, k):
        """The joints of digit k, base to tip."""
        segs = self.digits[k]
        return [s[0].o for s in segs] + [v_add(segs[-1][0].o, v_mul(segs[-1][0].u, segs[-1][1]))]


def turn_abd(c, deg, H_):
    """Palmar abduction: the thumb's metacarpal lifts away from the palm's plane, about an
    axis across the palm."""
    palm_n = H_((0.0, 0.0, -1.0))
    axis = v_cross(c.u, palm_n)
    if v_len(axis) < 1e-6:
        return c
    axis = v_norm(axis)
    return c.turned(axis, deg)


# ---------------------------------------------------------------- solids


def ellipsoid(c, ax, n_lat=6, n_lon=12):
    """Points on an ellipsoid at c with three axis vectors (each with its length)."""
    a, b, d = ax
    pts = []
    for i in range(n_lat + 1):
        t = math.pi * i / n_lat - math.pi / 2
        for j in range(n_lon):
            s = 2 * math.pi * j / n_lon
            p = v_add(c, v_add(v_mul(a, math.sin(t)),
                               v_add(v_mul(b, math.cos(t) * math.cos(s)), v_mul(d, math.cos(t) * math.sin(s)))))
            pts.append(p)
    return pts


def section(f, a, half_b, half_d, dz=0.0, p=3.0, n=16):
    """A superellipse section across frame f's axis at a, with its centre dz out of the back."""
    out = []
    for j in range(n):
        s = 2 * math.pi * j / n
        cs, sn = math.cos(s), math.sin(s)
        x = math.copysign(abs(cs) ** (2 / p), cs) * half_b
        y = math.copysign(abs(sn) ** (2 / p), sn) * half_d
        out.append(f.at(a, x, dz + y))
    return out


def digit_solids(skel, k):
    """The solids of a finger or the thumb's free part, one per phalanx: the hull of a round
    knob at each of its joints and the pad under it. So its back runs straight from knob to
    knob, its palm side curves out over the pad, and a crease parts it from the next."""
    segs = skel.digits[k]
    out = []
    if k == "t":
        # the thumb grows out of the ball of the thumb: its metacarpal and the ball are one
        # convex mass, so the palm side runs in one curve from the wrist over the ball and on
        # up the thumb. Its outline runs from the tip down past the knuckle and over the
        # ball; only its back, where it crosses the palm near the base, melts away
        mc, L = segs[0]
        H_ = skel.H
        hx, hy, hz = skel.hand
        (b0, d0), (b1, d1) = THUMB_SECTION[0], THUMB_SECTION[1]
        out.append(ellipsoid(mc.o, (v_mul(mc.u, d0 * 0.45), v_mul(mc.v, b0 / 2), v_mul(mc.w, d0 / 2)))
                   + ellipsoid(mc.at(L, 0, 0), (v_mul(mc.u, d1 * 0.45), v_mul(mc.v, b1 / 2), v_mul(mc.w, d1 / 2)))
                   + ellipsoid(H_(BALL_AT), (v_mul(hy, 2.0), v_mul(hx, BALL[0]), v_mul(hz, BALL[1])))
                   + ellipsoid(H_(BALL_LOW), (v_mul(hy, 1.0), v_mul(hx, BALL[0] * 0.9), v_mul(hz, BALL[1] * 0.7))))
        f1, _ = segs[1]
        out.append(ellipsoid(f1.o, (v_mul(f1.u, 1.05), v_mul(f1.v, 1.15), v_mul(f1.w, 1.0))))
        segs, sec = segs[1:], THUMB_SECTION[1:]
    else:
        gb, gd = GIRTH[k]
        sec = [(b * gb, d * gd) for b, d in SECTION]
    for i, (f, L) in enumerate(segs):
        (b0, d0), (b1, d1) = sec[i], sec[i + 1]
        last = i == len(segs) - 1
        pts = ellipsoid(f.o, (v_mul(f.u, d0 * 0.45), v_mul(f.v, b0 / 2), v_mul(f.w, d0 / 2)))
        dm, bm = (d0 + d1) / 2, (b0 + b1) / 2
        # the pad: the palm side bulges a little between the creases
        pts += ellipsoid(f.at(L * 0.5, 0.0, -dm * 0.1),
                         (v_mul(f.u, L * 0.3), v_mul(f.v, bm * 0.46), v_mul(f.w, dm * 0.47)), 4, 10)
        if last:
            # the fingertip: rounder under the pad, flattened on the back by the nail
            r1 = d1 / 2
            pts += ellipsoid(f.at(L - r1 * 1.05, 0.0, -0.05),
                             (v_mul(f.u, r1 * 1.05), v_mul(f.v, b1 / 2), v_mul(f.w, d1 / 2)))
        else:
            pts += ellipsoid(f.at(L, 0, 0), (v_mul(f.u, d1 * 0.45), v_mul(f.v, b1 / 2), v_mul(f.w, d1 / 2)))
        out.append(pts)
    return out


def palm_solids(skel):
    H_ = skel.H
    hx, hy, hz = skel.hand
    hand = Frame((0.0, 0.0, 0.0), hy, hz)
    out = []
    # the slab of the palm, sections across it from the wrist to below the knuckles
    slab = []
    for y, xc, b, zc, d in PALM:
        f = Frame(H_((xc, 0.0, 0.0)), hy, hz)
        slab += [v_add(p, (0.0, 0.0, 0.0)) for p in section(f, y, b / 2, d / 2, dz=zc, p=3.0)]
    # v of the hand frame points to the thumb side, which section() uses as its breadth
    out.append(slab)
    # the knuckles: the metacarpal heads, which stand out as bumps on the back of the hand
    for k in DIGITS:
        c = H_(v_add(MC_HEAD[k], (0.0, -0.1, -0.15)))
        gb, _ = GIRTH[k]
        out.append(ellipsoid(c, (v_mul(hy, 0.9), v_mul(hx, 1.0 * gb), v_mul(hz, 1.2))))
    # the pad across the base of the fingers, on the palm side
    out.append(ellipsoid(H_((0.1, 8.5, -1.5)), (v_mul(hx, 4.1), v_mul(hy, 1.0), v_mul(hz, 0.8))))
    # the mass on the little-finger side of the palm
    out.append(ellipsoid(H_((-2.85, 4.3, -1.15)), (v_mul(hx, 1.25), v_mul(hy, 3.4), v_mul(hz, 1.25))))
    # the ball of the thumb is the thumb's (digit_solids)
    mc, L = skel.digits["t"][0]
    f1, _ = skel.digits["t"][1]
    # the web between thumb and index: a sheet of skin from the ball of the thumb up both
    # digits to the middle of their first segments. Its free edge, from one to the other, is
    # a shallow curve once the joins round it off. Without it the space between them would
    # be a deep slot, and the outline would run from the index down into it and up the thumb
    # as if the two were one forked digit
    fi, Li = skel.digits["i"][0]
    _, L1 = skel.digits["t"][1]
    pts = [f1.o, f1.at(L1 * WEB[0], 0.0, 0.0), fi.at(Li * WEB[1], 0.0, -0.3), fi.o,
           H_(BALL_AT), mc.at(L * 0.6, 0.0, 0.0)]
    n = v_norm(v_cross(v_sub(pts[2], pts[0]), v_sub(pts[4], pts[0])))
    web = []
    for p in pts:
        web += [v_add(p, v_mul(n, 0.35)), v_add(p, v_mul(n, -0.35))]
    out.append(web)
    return out


def forearm_solids():
    out = []
    X, Y, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)
    f = Frame((0.0, 0.0, 0.0), Y, Z)
    pts = []
    for y, b, d, zc in FOREARM:
        pts += section(f, y, b / 2, d / 2, dz=zc, p=2.4)
    out.append(pts)
    # the wrist: round where the hand turns on the forearm
    out.append(ellipsoid((0.0, -0.3, -0.38), ((0.0, 1.6, 0.0), (3.15, 0.0, 0.0), (0.0, 0.0, 2.1))))
    return out


# ---------------------------------------------------------------- views

VIEWS = {
    # wall on the right: the thumb side toward you, the palm toward the wall
    "side": ((0.0, 0.0, -1.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0)),
    # the pocket: the little-finger side toward you, the palm still toward the wall
    "little": ((0.0, 0.0, -1.0), (0.0, 1.0, 0.0), (-1.0, 0.0, 0.0)),
    # the back of the hand toward you, the fingers up
    "back": ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
    # from above, the wall at the top: the back of the hand toward you, as from behind, the
    # fingers pointing at the wall
    "above": ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
}
# back to front; grey pieces lie behind the front finger. From behind the thumb lies beside
# the index and is drawn over the hand as a digit of its own, as from the side
ORDER = {
    "side": ["l", "r", "m", "palm", "i", "t"],
    "little": ["t", "i", "m", "r", "palm", "l"],
    "back": ["palm", "l", "r", "m", "i", "t"],
    "above": ["palm", "l", "r", "m", "i", "t"],
}
GREYS = {"side": {"m": A.GREY, "r": A.GREY2, "l": A.GREY2},
         "little": {"r": A.GREY, "m": A.GREY2, "i": A.GREY2},
         "back": {}, "above": {}}
# a finger behind the front one shows only where it steps out further than this (cm): a
# thinner band along the front finger's back would read as a doubled outline
BEHIND_INSET = -0.25
# cm: a finger this close beside the next one draws the line between them
NEAR = 0.3
# how softly the solids of a piece join, and each digit joins the palm (cm)
BLEND_IN = dict(palm=0.35, t=0.2, i=0.2, m=0.2, r=0.2, l=0.2)
BLEND_ROOT = dict(t=0.4, i=0.28, m=0.28, r=0.28, l=0.28)


def hull(points):
    """The convex hull of 2D points, counter-clockwise."""
    P = sorted(set((round(p[0], 4), round(p[1], 4)) for p in points))
    if len(P) < 3:
        return P

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


class Convex:
    """A projected solid: a convex outline, and its field (negative inside)."""

    def __init__(self, pts):
        self.pts = hull(pts)
        n = len(self.pts)
        self.planes = []
        for i in range(n):
            a, b = self.pts[i], self.pts[(i + 1) % n]
            d = sub(b, a)
            L = length(d)
            if L < 1e-9:
                continue
            nx, ny = d[1] / L, -d[0] / L
            self.planes.append((nx, ny, nx * a[0] + ny * a[1]))
        xs, ys = [p[0] for p in self.pts], [p[1] for p in self.pts]
        self.box = (min(xs), min(ys), max(xs), max(ys))

    def field(self, x, y):
        return max(nx * x + ny * y - c for nx, ny, c in self.planes)


def smin(a, b, k):
    if k <= 0:
        return min(a, b)
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - h * h * k * 0.25


class Grid:
    def __init__(self, box, step=GRID):
        x0, y0, x1, y1 = box
        self.x0, self.y0, self.s = x0, y0, step
        self.nx = int((x1 - x0) / step) + 2
        self.ny = int((y1 - y0) / step) + 2

    def blank(self, v=FAR):
        return [[v] * self.nx for _ in range(self.ny)]

    def paint(self, F, solid, k):
        """Join a solid into field F with a smooth minimum of radius k."""
        bx0, by0, bx1, by1 = solid.box
        m = FAR
        i0 = max(0, int((bx0 - m - self.x0) / self.s))
        i1 = min(self.nx - 1, int((bx1 + m - self.x0) / self.s) + 1)
        j0 = max(0, int((by0 - m - self.y0) / self.s))
        j1 = min(self.ny - 1, int((by1 + m - self.y0) / self.s) + 1)
        planes = solid.planes
        for j in range(j0, j1 + 1):
            y = self.y0 + j * self.s
            row = F[j]
            for i in range(i0, i1 + 1):
                x = self.x0 + i * self.s
                d = max(nx * x + ny * y - c for nx, ny, c in planes)
                if d > FAR:
                    d = FAR
                a = row[i]
                if k > 0 and abs(a - d) < k:
                    h = (k - abs(a - d)) / k
                    row[i] = min(a, d) - h * h * k * 0.25
                elif d < a:
                    row[i] = d

    def join(self, F, G, k):
        """F joined with G, smoothly."""
        return [[smin(a, b, k) for a, b in zip(rf, rg)] for rf, rg in zip(F, G)]

    def at(self, F, p):
        """F at p, interpolated."""
        x = (p[0] - self.x0) / self.s
        y = (p[1] - self.y0) / self.s
        i, j = int(math.floor(x)), int(math.floor(y))
        if i < 0 or j < 0 or i >= self.nx - 1 or j >= self.ny - 1:
            return FAR
        fx, fy = x - i, y - j
        a = F[j][i] * (1 - fx) + F[j][i + 1] * fx
        b = F[j + 1][i] * (1 - fx) + F[j + 1][i + 1] * fx
        return a * (1 - fy) + b * fy

    def contours(self, F, level=0.0):
        """The lines where F crosses level, as closed loops (marching squares)."""
        s, x0, y0 = self.s, self.x0, self.y0
        segs = {}

        def pt(i, j, a, b, di, dj):
            t = (level - a) / (b - a)
            return (round(x0 + (i + di * t) * s, 5), round(y0 + (j + dj * t) * s, 5))
        edges = []
        for j in range(self.ny - 1):
            r0, r1 = F[j], F[j + 1]
            for i in range(self.nx - 1):
                a, b, c, d = r0[i], r0[i + 1], r1[i + 1], r1[i]
                idx = (a < level) | ((b < level) << 1) | ((c < level) << 2) | ((d < level) << 3)
                if idx == 0 or idx == 15:
                    continue
                e = {}
                if (a < level) != (b < level):
                    e["s"] = pt(i, j, a, b, 1, 0)
                if (b < level) != (c < level):
                    e["e"] = (round(x0 + (i + 1) * s, 5), pt(i, j, b, c, 0, 1)[1])
                if (d < level) != (c < level):
                    e["n"] = pt(i, j + 1, d, c, 1, 0)
                if (a < level) != (d < level):
                    e["w"] = (round(x0 + i * s, 5), pt(i, j, a, d, 0, 1)[1])
                # orient each piece with the inside on its left
                table = {1: [("w", "s")], 2: [("s", "e")], 3: [("w", "e")], 4: [("e", "n")],
                         6: [("s", "n")], 7: [("w", "n")], 8: [("n", "w")], 9: [("n", "s")],
                         11: [("n", "e")], 12: [("e", "w")], 13: [("e", "s")], 14: [("s", "w")],
                         5: [("w", "n"), ("e", "s")] if (a + b + c + d) / 4 < level else
                            [("w", "s"), ("e", "n")],
                         10: [("s", "e"), ("n", "w")] if (a + b + c + d) / 4 < level else
                             [("s", "w"), ("n", "e")]}
                for p, q in table[idx]:
                    edges.append((e[p], e[q]))
        nxt = {}
        for p, q in edges:
            nxt[p] = q
        loops, seen = [], set()
        for start in list(nxt):
            if start in seen:
                continue
            loop, p = [], start
            while p in nxt and p not in seen:
                seen.add(p)
                loop.append(p)
                p = nxt[p]
            if len(loop) > 8:
                loops.append(loop)
        return loops


def resample(P, step, closed=True):
    """Points every `step` along a polyline."""
    Q = P + [P[0]] if closed else P
    out, acc = [Q[0]], 0.0
    for a, b in zip(Q, Q[1:]):
        L = length(sub(b, a))
        while acc + L >= step:
            t = (step - acc) / L
            a = add(a, mul(sub(b, a), t))
            L = length(sub(b, a))
            out.append(a)
            acc = 0.0
        acc += L
    if closed and length(sub(out[-1], out[0])) < step * 0.5:
        out.pop()
    if not closed and out[-1] != Q[-1]:
        out.append(Q[-1])
    return out


def relax(P, n=2, closed=True):
    for _ in range(n):
        m = len(P)
        if closed:
            P = [mul(add(add(P[i - 1], P[(i + 1) % m]), mul(P[i], 2.0)), 0.25) for i in range(m)]
        else:
            P = [P[0]] + [mul(add(add(P[i - 1], P[i + 1]), mul(P[i], 2.0)), 0.25)
                          for i in range(1, m - 1)] + [P[-1]]
    return P


# ---------------------------------------------------------------- a posed hand in a view


class Hand:
    """A pose seen from a view and placed in a figure: `arm` turns the drawing so the
    forearm runs that many degrees clockwise from straight down (0: hanging); the point
    named `anchor` lands on `at`. mirror: the other hand."""

    def __init__(self, pose, view="side", arm=0.0, anchor=None, at=(0.0, 0.0), mirror=False,
                 pitch=0.0, name=""):
        self.pose, self.view, self.name = pose, view, name
        self.skel = Skeleton(pose)
        R, U, D = VIEWS[view]
        if pitch:
            # look down on the hand by `pitch` degrees
            U2 = turn(U, R, -pitch)
            D2 = turn(D, R, -pitch)
            U, D = U2, D2
        self.R, self.U, self.D = R, U, D
        self.mirror = mirror
        self.roll = -arm
        self.shift = (0.0, 0.0)
        if anchor:
            p = self.flat(self.point(anchor))
            self.shift = sub(at, p)

    def flat(self, p):
        x, y = v_dot(p, self.R), v_dot(p, self.U)
        q = rot((x, y), self.roll)
        q = (-q[0], q[1]) if self.mirror else q
        return add(q, self.shift)

    def unflat(self, q, x):
        """The point of the hand's frame that a view from the side draws at q, x cm toward
        the thumb side."""
        q = sub(q, self.shift)
        q = (-q[0], q[1]) if self.mirror else q
        a, b = rot(q, -self.roll)
        return v_add(v_add(v_mul(self.R, a), v_mul(self.U, b)), v_mul(self.D, x))

    def depth(self, p):
        return v_dot(p, self.D)

    def point(self, name):
        """Named points: 'i_pad' the pad of a digit's end segment, 'i_tip' its end, 'i2'
        its joints (0 the knuckle), 'crease' the wrist crease on the palm side, 'wrist'."""
        s = self.skel
        if name == "crease":
            return s.H(WRIST_CREASE)
        if name == "wrist":
            return (0.0, 0.0, 0.0)
        k, what = name[0], name[1:]
        segs = s.digits[k]
        f, L = segs[-1]
        sec = THUMB_SECTION if k == "t" else [(b * GIRTH[k][0], d * GIRTH[k][1]) for b, d in SECTION]
        if what == "_pad":
            return f.at(L * 0.55, 0.0, -sec[-1][1] / 2 - 0.05)
        if what == "_tip":
            return f.at(L, 0.0, -0.1)
        if what == "_nail":
            return f.at(L * 0.6, 0.0, sec[-1][1] / 2)
        return s.joints(k)[int(what)]

    def spot(self, name):
        """Figure points for labels: 'i0'-'i3' the index's joints and tip, 'dent' the back of
        its end joint, 'a2' the palm side of its first segment, where the A2 pulley is, 'pads'
        its fingertip's pad, 'thumbnail' the back of the thumb's end segment."""
        s = self.skel
        if name[0] == "i" and name[1:].isdigit():
            return self.flat(s.joints("i")[int(name[1:])])
        sec = [(b * GIRTH["i"][0], d * GIRTH["i"][1]) for b, d in SECTION]
        if name == "dent":
            # the back of the end joint, or, where the thumb covers it, the nearest part of
            # the end segment that still shows
            f, L = s.digits["i"][2]
            dent = self.flat(f.at(0.0, 0.0, sec[2][1] / 2))
            if not hasattr(self, "grid"):
                self.build()
            g, own = self.grid, self.own
            if g.at(own["t"], dent) > 0.05:
                return dent
            for k in range(1, 41):
                for up in (0.4, 0.2, 0.0, -0.2):
                    q = self.flat(f.at(L * k / 40, 0.0, up))
                    if g.at(own["t"], q) > 0.12 and g.at(own["i"], q) < -0.12:
                        return q
            return dent
        if name == "a2":
            f, L = s.digits["i"][0]
            return self.flat(f.at(L * 0.4, 0.0, -sec[1][1] / 2 * 0.4))
        if name == "pads":
            return self.flat(self.point("i_pad"))
        if name == "thumbnail":
            f, L = s.digits["t"][2]
            return self.flat(f.at(L * 0.55, 0.0, THUMB_SECTION[2][1] / 2 * 0.7))
        raise KeyError(name)

    # -------------------------------------------------------- the drawing's geometry

    def pieces(self):
        """Each piece's projected solids, and its root: where it grows out of the palm."""
        s = self.skel
        out = {}
        palm = [Convex([self.flat(p) for p in pts]) for pts in palm_solids(s) + forearm_solids()]
        out["palm"] = palm
        for k in "imrlt":
            out[k] = [Convex([self.flat(p) for p in pts]) for pts in digit_solids(s, k)]
        return out

    def build(self):
        P = self.pieces()
        boxes = [c.box for cs in P.values() for c in cs]
        box = (min(b[0] for b in boxes) - 1.0, min(b[1] for b in boxes) - 1.0,
               max(b[2] for b in boxes) + 1.0, max(b[3] for b in boxes) + 1.0)
        g = Grid(box)
        own = {}
        for name, cs in P.items():
            F = g.blank()
            for c in cs:
                g.paint(F, c, BLEND_IN[name])
            own[name] = F
        joined = {"palm": own["palm"]}
        for k in "imrlt":
            joined[k] = g.join(own[k], own["palm"], BLEND_ROOT[k])
        self.grid, self.own, self.joined, self.P = g, own, joined, P
        return self

    def root_t(self, k, p2):
        """How far a point of digit k's outline lies out along it from its root, in cm: the
        distance past the knuckle (thumb: past its first joint), along the first segment."""
        f, L = self.skel.digits[k][0]
        a, b = self.flat(f.o), self.flat(f.at(L, 0, 0))
        u = norm(sub(b, a))
        return dot(sub(p2, a), u) / max(length(sub(b, a)), 1e-6)


# ---------------------------------------------------------------- drawing

def _pen_loop(f, pts):
    return f._path_d(pts, True, True)


def draw(f, hand, z=0.0, fill=WHITE, ghost=False, show_lines=True, skeleton=False, behind=()):
    """Draw a posed hand on figure f, with the climbers' pen. behind: the outlines of the
    holds behind the hand, which show through a hole in it."""
    if not hasattr(hand, "grid"):
        hand.build()
    g, own, joined = hand.grid, hand.own, hand.joined
    order = ORDER[hand.view]
    greys = GREYS[hand.view]
    k_ = H.LINE[0]
    front = [n for n in order if n not in greys]
    # From the side the thumb stands in front of the palm and the index; from behind it lies
    # beside the index. Either way it is a digit with its own outline, drawn over the rest of
    # the hand, which is outlined without it. Joined into one silhouette, the outline would
    # run from the index down between them and up the thumb, as if the two were one forked
    # digit.
    apart = thumb_apart(hand)
    hidden = thumb_hidden(hand)
    body = [n for n in front if not ((apart or hidden) and n == "t")]
    U = union(hand, body)
    loops = [relax(resample(L, 0.18), 2) for L in g.contours(U)]
    loops = [L for L in loops if len(L) > 5]
    if hand.view in ("side", "little") and loops:
        outer = max(loops, key=lambda L: abs(area(L)))
        loops[loops.index(outer)] = palm_side(hand, outer, U)
    crease = hand.flat(hand.point("crease"))
    arm_dir = hand.flat((0.0, -10.0, 0.0))
    arm_u = norm(sub(arm_dir, hand.flat((0.0, 0.0, 0.0))))

    def wob(p):
        s = max(0.0, min(1.0, (dot(sub(p, crease), arm_u) - A.ARM_FROM) / A.ARM_RAMP))
        return 1 - (1 - A.ARM_WOBBLE) * s * s * (3 - 2 * s)
    f.wobble = wob
    d = " ".join(_pen_loop(f, L) for L in loops)
    if ghost:
        # an earlier position: one outer outline of the whole hand, thumb and all unless it is
        # out of sight, dashed, with no line of one part drawn across another
        whole = union(hand, [n for n in front if not (hidden and n == "t")])
        outer = max((relax(resample(L, 0.18), 2) for L in g.contours(whole)), key=lambda L: abs(area(L)))
        st = f.style(fill=None, stroke=MID, sw=0.3, dash=(0.9, 0.7))
        f.add(f'<path d="{_pen_loop(f, outer)}" fill-rule="evenodd" {st}/>', z)
        f.wobble = None
        return
    # grey fingers behind: only where they stand out above the front finger's back or past
    # its tip, never as a band or a tongue below it
    for i, n in enumerate([n for n in order if n in greys]):
        G = behind_field(hand, n)
        for L in g.contours(G):
            L = relax(resample(L, 0.18), 2)
            if len(L) < 6 or abs(area(L)) < 0.08:
                continue
            dd = _pen_loop(f, L)
            f.add(f'<path d="{dd}" fill="{greys[n]}"/>', z - 0.05 + 0.002 * i)
            f.add(f'<path d="{dd}" {f.style(fill=None, stroke=INK, sw=A.fine_sw())}/>', z - 0.05 + 0.002 * i + 0.001)
    f.add(f'<path d="{d}" fill-rule="evenodd" {f.style(fill=fill, stroke=INK, sw=A.OUT * k_)}/>', z + 0.01)
    # a hole in the outline, as between the thumb, the index and the palm in a full crimp,
    # is a dark gap, not paper
    every = [relax(resample(L, 0.18), 2) for L in g.contours(union(hand, front))]
    every = [L for L in every if len(L) > 5]
    if every:
        outer = max(every, key=lambda L: abs(area(L)))
        for L in every:
            if L is not outer and area(L) * area(outer) < 0:
                # a hole shows what lies behind it: where a hold does, it is left open and the
                # hold shows through; where a finger behind does, as the next finger behind a
                # full crimp's index, that finger's grey; where nothing does, a dark gap
                if not any(_inside(q, poly) for poly in behind for q in L):
                    c = (sum(q[0] for q in L) / len(L), sum(q[1] for q in L) / len(L))
                    shade = next((greys[n] for n in reversed(order)
                                  if n in greys and g.at(own[n], c) < 0.0), GAP)
                    f.add(f'<path d="{_pen_loop(f, L)}" fill="{shade}"/>', z + 0.012)
    # the thumb: white over the hand, and its outline all round, but for its base, where it
    # melts into the ball of the thumb inside the hand's outline
    zt = z + 0.015
    apart = apart and not hidden
    if apart:
        for L in g.contours(own["t"]):
            L = relax(resample(L, 0.18), 2)
            if len(L) > 5:
                f.add(f'<path d="{_pen_loop(f, L)}" fill="{fill}"/>', zt)
    f.wobble = None
    if apart:
        for pts, fade in thumb_outline(hand, U):
            A.pen_line(f, pts, zt + 0.005, A.OUT * k_, fade=fade)
    if show_lines:
        for pts, fade in inner_lines(hand, front, skip=("t",) if apart or hidden else ()):
            A.pen_line(f, pts, z + 0.02, A.OUT * k_, fade=fade)
    for pts in nails(hand, [n for n in front if not (hidden and n == "t")]):
        f.poly(A.curve(f, pts, False), closed=False, z=z + 0.03, taper=True, _smooth=True,
               fill=None, stroke=INK, sw=A.fine_sw())
    for pts in creases(hand):
        f.poly(A.curve(f, pts, False), closed=False, z=z + 0.03, taper=True, _smooth=True,
               fill=None, stroke=INK, sw=A.fine_sw())
    if skeleton:
        draw_skeleton(f, hand, z + 0.05)


ROOT = dict(t=0.8, i=0.42, m=0.42, r=0.42, l=0.42)   # of the first segment: a digit's root
# Over the palm the thumb's back melts into the hand from its knuckle down, so the thumb widens
# into the ball of the thumb; a line on down to the ball would part it from the hand, as if
# it were stuck on. Its palm side carries on down over the ball as the hand's own outline
THUMB_MELT = 1.0


def thumb_apart(hand):
    """Whether the thumb is drawn as a digit of its own, over the hand: in every view where
    it is not a grey digit behind. From behind too it lies beside the index, not under it,
    so no line of the hand's edge runs across it."""
    return "t" not in GREYS[hand.view]


def thumb_hidden(hand):
    """From behind, a thumb tucked under the palm: every point of its outline inside the
    hand's own outline, and behind the back of the hand, so none of it shows."""
    if hand.view not in ("back", "above"):
        return False
    if not hasattr(hand, "grid"):
        hand.build()
    g, s = hand.grid, hand.skel
    U = union(hand, [n for n in ORDER[hand.view] if n not in GREYS[hand.view] and n != "t"])
    inside = all(g.at(U, p) < -0.05 for L in g.contours(hand.own["t"]) for p in L)
    behind = hand.depth(s.joints("t")[-1]) < hand.depth(s.joints("i")[0]) - 1.0
    return inside and behind


def union(hand, names):
    """The field of these pieces together, each joined to the palm."""
    U = None
    for n in names:
        F = hand.joined[n]
        U = F if U is None else [[min(a, b) for a, b in zip(ra, rb)] for ra, rb in zip(U, F)]
    return U


def thumb_outline(hand, U):
    """The thumb's outline as drawn: all of it, except its base where that lies inside the
    hand's outline U. [(points, fade mm)]"""
    g, own = hand.grid, hand.own
    back = hand.view in ("back", "above")
    # down the thumb, from its knuckle toward its base
    J = [hand.flat(j) for j in hand.skel.joints("t")]
    down = norm(sub(J[0], J[1]))
    out = []
    for L in g.contours(own["t"]):
        L = relax(resample(L, 0.12), 2)
        if back:
            # from behind the thumb grows out of the back of the hand: inside the hand's
            # outline its edge shows only where it lies over a finger, never over the palm
            # or the web, which join it to the hand
            keep = [g.at(U, p) > -0.05 or (hand.root_t("t", p) >= 1.0 and
                                           any(g.at(own[k], p) < 0.04 for k in "imrl"))
                    for p in L]
        else:
            keep = [hand.root_t("t", p) >= THUMB_MELT or g.at(U, p) > -0.05 for p in L]
        if all(keep):
            out.append((L + [L[0]], 0.0))
            continue
        for r in _runs(L, keep):
            if len(r) < 3:
                continue
            # fade toward an end inside the hand, where the thumb melts into the ball
            if g.at(U, r[0]) < g.at(U, r[-1]):
                r = r[::-1]
            inside = g.at(U, r[-1]) < -0.25
            if inside:
                # and stop before its end turns off down the thumb, round the ball: a hook
                # there closes the thumb off from the hand, as if it were stuck on
                j, run = len(r) - 1, 0.0
                while j > 1 and run < 1.5 and dot(norm(sub(r[j], r[j - 1])), down) < 0.5:
                    run += length(sub(r[j], r[j - 1]))
                    j -= 1
                r = r[:j + 1]
            if len(r) >= 3:
                out.append((r, 3.5 if inside else 0.0))
    return out
ROOT_BACK = 0.22        # from the back the fingers part down to the webs, near the knuckles
GAP = "#3c3c3c"         # a hole in the outline, where no hold lies behind it


def _inside(p, poly):
    x, y = p
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c
FRONT = dict(side="i", little="l")      # the finger in front, in the views with grey fingers


def palm_side(hand, L, U):
    """The outline with its palm side, from the thumb's knuckle down to the wrist, as one
    convex curve: the ball of the thumb, the thumb's base and the heel of the hand are
    separate solids, and their joins would show as bumps."""
    s = hand.skel
    mc, Lm = s.digits["t"][0]
    a = hand.flat(mc.at(Lm * 0.9, 0, 0))
    b = hand.flat(s.H((0.0, -0.6, -2.6)))
    ia = min(range(len(L)), key=lambda i: length(sub(L[i], a)))
    ib = min(range(len(L)), key=lambda i: length(sub(L[i], b)))
    n = len(L)
    fwd = (ib - ia) % n
    i0, i1 = (ia, ib) if fwd <= n - fwd else (ib, ia)
    m = (i1 - i0) % n
    if m < 4:
        return L
    idx = [(i0 + k) % n for k in range(m + 1)]
    P = [L[i] for i in idx]
    u = norm(sub(P[-1], P[0]))
    v = perp(u)
    mid = mul(add(P[0], P[-1]), 0.5)
    g = hand.grid
    if g.at(U, add(mid, mul(v, 3.0))) < g.at(U, add(mid, mul(v, -3.0))):
        v = mul(v, -1.0)        # v points out of the hand
    T = [(dot(sub(q, P[0]), u), dot(sub(q, P[0]), v)) for q in P]
    if any(t1 <= t0 for (t0, _), (t1, _) in zip(T, T[1:])):
        return L                # not a simple curve along the chord: leave it
    # the upper hull of (t, out): the convex envelope on the outside
    hull = []
    for q in T:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (x2 - x1) * (q[1] - y1) - (y2 - y1) * (q[0] - x1) >= 0:
                hull.pop()
            else:
                break
        hull.append(q)
    def at(t):
        for (x1, y1), (x2, y2) in zip(hull, hull[1:]):
            if x1 <= t <= x2:
                return y1 + (y2 - y1) * (t - x1) / max(x2 - x1, 1e-9)
        return hull[-1][1]
    new = [add(P[0], add(mul(u, t), mul(v, at(t)))) for t, _ in T]
    out = list(L)
    for k, i in enumerate(idx):
        out[i] = new[k]
    return relax(out, 2)


def area(L):
    return 0.5 * sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(L, L[1:] + L[:1]))


def behind_field(hand, n):
    """The field of the part of grey finger n that shows: inside it by more than
    BEHIND_INSET, and on the back side of the front finger's axis or past its tip."""
    g, own = hand.grid, hand.own
    k = FRONT[hand.view]
    segs = hand.skel.digits[k]
    axis = []
    for f, L in segs:
        a, b = hand.flat(f.o), hand.flat(f.at(L, 0, 0))
        up = sub(hand.flat(f.at(L / 2, 0, 1.0)), hand.flat(f.at(L / 2, 0, 0)))
        axis.append((a, b, norm(up)))
    F = own[n]
    out = [[FAR] * g.nx for _ in range(g.ny)]
    for j in range(g.ny):
        y = g.y0 + j * g.s
        row, src = out[j], F[j]
        for i in range(g.nx):
            v = src[i] - BEHIND_INSET
            if v > 0.5:
                continue
            p = (g.x0 + i * g.s, y)
            best, side = None, 0.0
            for m, (a, b, up) in enumerate(axis):
                d = sub(b, a)
                L2 = dot(d, d)
                t = dot(sub(p, a), d) / L2
                # the first segment's line runs on behind the knuckle, the last one's past the tip
                lo = -1e9 if m == 0 else 0.0
                hi = 1e9 if m == len(axis) - 1 else 1.0
                q = add(a, mul(d, min(hi, max(lo, t))))
                e = length(sub(p, q))
                if best is None or e < best:
                    best, side = e, dot(sub(p, q), up)
            row[i] = max(v, -side)
    return out


def inner_lines(hand, front, skip=()):
    """Where a front piece lies over one behind it: its own outline, but not where it grows
    out of the palm. [(points, fade mm)]"""
    g, own = hand.grid, hand.own
    order = ORDER[hand.view]
    from_back = hand.view in ("back", "above")
    out = []
    for n in front:
        if n == "palm" or n in skip:
            continue
        idx = order.index(n)
        behind = order[:idx]            # grey fingers too: the thumb's edge shows over them
        ahead = [a for a in order[idx + 1:] if a in front]
        for L in g.contours(own[n]):
            L = relax(resample(L, 0.12), 2)
            keep = []
            for p in L:
                # over a piece behind, or close beside a finger next to it: two fingers that
                # touch need the line between them, or the hand reads as a mitten
                over = any(g.at(own[b], p) < (NEAR if b in DIGITS and n in DIGITS else 0.04)
                           for b in behind)
                hidden = any(g.at(own[a], p) < -0.03 for a in ahead)
                root = hand.root_t(n, p) < (ROOT_BACK if from_back and n != "t" else ROOT[n])
                # where a finger blends into the palm its line would cut the fillet. The
                # thumb is a digit of its own in front of the palm: all of its edge shows,
                # and only its root melts into the ball of the thumb
                q = g.at(own["palm"], p)
                blend = n != "t" and not from_back and -0.12 < q < 0.25
                keep.append(over and not hidden and not root and not blend)
            runs = _runs(L, keep)
            for r in runs:
                if len(r) < 4:
                    continue
                Lr = sum(length(sub(b, a)) for a, b in zip(r, r[1:]))
                if Lr < 1.0:       # a shorter run would read as a stray tick
                    continue
                # fade toward an end that lies inside the hand, not one that meets the outline
                U0 = min(g.at(hand.joined[m], r[0]) for m in front)
                U1 = min(g.at(hand.joined[m], r[-1]) for m in front)
                if U0 < U1:
                    r = r[::-1]
                    U0, U1 = U1, U0
                # from the back the line between two fingers runs down to the web
                fade = (1.0 if from_back else 3.5) if U1 < -0.25 else 0.0
                out.append((r, fade))
    return out


def _runs(L, keep):
    """The kept stretches of a closed loop, as open polylines."""
    n = len(L)
    if all(keep):
        return [L + [L[0]]]
    if not any(keep):
        return []
    start = keep.index(False)
    runs, cur = [], []
    for i in range(1, n + 1):
        j = (start + i) % n
        if keep[j]:
            cur.append(L[j])
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def nails(hand, front):
    """The nails, where they face you: an outline round the nail plate on the back of each
    end segment, 0.78 of its breadth and 0.6 of its length."""
    g, own = hand.grid, hand.own
    out = []
    for k in "imrlt":
        segs = hand.skel.digits[k]
        f, L = segs[-1]
        if k == "t":
            b, d = THUMB_SECTION[-1]
            nb = 0.85
        else:
            b, d = SECTION[-1][0] * GIRTH[k][0], SECTION[-1][1] * GIRTH[k][1]
            nb = 0.78
        facing = v_dot(f.w, hand.D)
        if facing < 0.3 or k not in front:
            continue
        # the plate's edge on the surface: round its base, up both sides to the free edge
        a0, a1 = L * 0.32, L * 0.93
        half = nb * b / 2
        rows = []
        for s in (-1.0, -0.95, -0.7, -0.35, 0.0, 0.35, 0.7, 0.95, 1.0):
            # across the nail, s from one side to the other; the base is round
            a = a0 + (1 - math.sqrt(max(0.0, 1 - s * s))) * (a1 - a0) * 0.5 * 0.6
            x = s * half
            # on the surface: the section's top at that breadth
            zz = d / 2 * math.sqrt(max(0.0, 1 - (x / (b / 2)) ** 2)) ** 0.66
            rows.append(f.at(a, x, zz))
        start = f.at(a1, -half, d / 2 * 0.55)
        end = f.at(a1, half, d / 2 * 0.55)
        pts3 = [start] + rows + [end]
        P = [hand.flat(p) for p in pts3]
        # only what no piece in front covers, and on the digit's own outline
        idx = ORDER[hand.view].index(k)
        ahead = [m for m in ORDER[hand.view][idx + 1:] if m in front]
        vis = [all(g.at(own[m], p) > 0.0 for m in ahead) and g.at(own[k], p) < -0.06 for p in P]
        if sum(vis) < 4:
            continue
        out.append([p for p, v in zip(P, vis) if v])
    return out


def creases(hand):
    """The wrist crease on the palm side, where it shows in a side view."""
    if hand.view not in ("side", "little"):
        return []
    s = hand.skel
    a = s.H((0.0, 0.05, -2.45))
    b = s.H((0.0, -0.05, -1.4))
    c = s.H((0.0, -0.15, -0.6))
    return [[hand.flat(a), hand.flat(b), hand.flat(c)]]


def draw_skeleton(f, hand, z):
    """The bones under the drawing, for the model sheet."""
    s = hand.skel
    st = dict(sw=0.18, stroke="#4a7fbf")
    for a, b in (RADIUS, ULNA):
        f.line(hand.flat(a), hand.flat(b), z=z, **st)
    for k in DIGITS:
        f.line(hand.flat(s.H(MC_BASE[k])), hand.flat(s.H(MC_HEAD[k])), z=z, **st)
        J = s.joints(k)
        for a, b in zip(J, J[1:]):
            f.line(hand.flat(a), hand.flat(b), z=z, **st)
        for p in J[:-1]:
            f.circle(hand.flat(p), 0.35, z=z, fill="#4a7fbf", stroke=None)
    J = s.joints("t")
    for a, b in zip(J, J[1:]):
        f.line(hand.flat(a), hand.flat(b), z=z, **st)
    for p in J[:-1]:
        f.circle(hand.flat(p), 0.35, z=z, fill="#4a7fbf", stroke=None)
    # the carpus as one block
    q = [s.H(p) for p in ((-2.6, 0.4, 0.0), (2.4, 0.4, 0.0), (2.6, 2.5, 0.0), (-2.4, 2.4, 0.0))]
    f.poly([hand.flat(p) for p in q], z=z, fill=None, stroke="#4a7fbf", sw=0.18)


# ---------------------------------------------------------------- the grips
#
# Each grip is one pose, used wherever the book shows it: (pose, arm). The angles are the
# index's knuckle, middle joint and end joint, in degrees of flexion (negative bends back);
# a negative wrist is bent back. arm turns the drawing so the back of the hand stands as the
# photos show it. The rows (H2, F1 ...) are research/hands-drawing-reference.md's. The other
# fingers were solved to put their tips on the edge, and the thumb to where the photo puts
# it, with finger_to and a thumb solver; the results are written out here so every figure
# gets exactly the same hand.

GRIPS = dict(
    # J2, J1: knuckle 45-60, middle joint 90, end joint 30-45, the back of the hand upright;
    # the thumb up beside the index, in front of the palm, its tip on the lip below the
    # fingers and clear of the index's middle joint (J2, and jug photos 2, 7 and 8). The
    # middle finger's knuckle stands a little higher and its tip further on, so the fingers
    # over the lip step instead of merging into one rounded top
    jug=(dict(wrist=(0, 0), i=(45, 90, 40), m=(39, 86, 40), r=(28, 94, 40), l=(26, 94, 40),
              thumb=dict(cmc=(-44, 2), mcp=30, ip=30)), 0.0),
    # O1 (a true side view), Fischer 2024: knuckle 10, middle joint 38 (Fischer's mean 39;
    # O1 reads 20-30, O3 about 60), end joint 45 over the lip, wrist bent back 8; the thumb
    # nearly straight along the palm side, free below the lip
    open=(dict(wrist=(-8, 0), i=(10, 38, 45), m=(2, 58, 45), r=(-1, 51, 45), l=(13, 6, 45),
               thumb=dict(cmc=(-24, -4), mcp=5, ip=5)), 8.0),
    # The thumb catch: the open hand, its thumb pressed up into a dimple under the lip. The
    # thumb runs on from the ball of the thumb in one line on the wall side, as in the full
    # crimp, so its palm side is the hand's own outline from the wrist to its pad (Rock and
    # Ice's thumb press, thumbpress-1, and ClimbingCrux's thumbcatch-11: the thumb in line
    # with the hand's edge under the hold). The pose came from a search for a thumb in line
    # with its metacarpal with its pad in the dimple; the hand leans in more to bring it there
    catch=(dict(wrist=(8, 0), i=(10, 38, 45), m=(2, 58, 45), r=(-1, 51, 45), l=(13, 6, 45),
                thumb=dict(cmc=(-20, 2), mcp=15, ip=0)), 24.0),
    # the thumb pressing up on a volume's lower face, the fingers nearly straight along its
    # upper face (Rock and Ice's thumb press; no true side view); the thumb straight on from
    # the ball of the thumb in the same way
    press=(dict(wrist=(8, 0), i=(15, 15, 8), m=(15, 15, 8), r=(15, 17, 8), l=(18, 17, 8),
                thumb=dict(cmc=(-15, -6), mcp=0, ip=0)), 0.0),
    # latching: the open hand arriving above the lip, the fingers only a little bent, the
    # thumb along the palm (no close-up photo: the reference's whole-body dyno only)
    latch=(dict(wrist=(-8, 0), i=(25, 25, 15), m=(25, 27, 15), r=(25, 27, 15), l=(27, 27, 15),
                thumb=dict(cmc=(14, -12), mcp=5, ip=5)), 22.0),
    # the undercling: palm up under a flake, seen from the thumb side, which is the other
    # hand's view (MIRRORED). The fingers rise past the lip and curl up behind it, the thumb
    # points out (Momentum and Mesa Rim photos: palm up, middle joints curled up behind the
    # lip, the thumb out along the hold's side). The atlas's flake is shallow, so the middle
    # joint bends 60, where the photos show about 90 on deeper holds
    under=(dict(wrist=(0, 0), i=(10, 60, 30), m=(10, 65, 30), r=(13, 65, 30), l=(16, 60, 30),
                thumb=dict(cmc=(-20, 0), mcp=10, ip=10)), -60.0),
    # The sloper film strip: one hand in five moments of a regrip. No photo shows the
    # sequence; the end is S1's and the atlas's sloper, the steps between rest on the
    # anatomy. 1 catch with the fingertips: the fingers curled, only their tips on the top
    film_catch=(dict(wrist=(0, 0), i=(20, 60, 35), m=(14, 76, 35), r=(8, 70, 35), l=(11, 47, 35),
                     thumb=dict(cmc=(-30, -4), mcp=5, ip=5)), 0.0),
    # 2 drag the pads over: the fingers open out, the pads come onto the top
    film_drag=(dict(wrist=(5, 0), i=(15, 30, 25), m=(3, 56, 25), r=(3, 47, 25), l=(23, 0, 25),
                    thumb=dict(cmc=(-30, -4), mcp=5, ip=5)), 0.0),
    # 3 bring the palm on: the sloper's drape, the thumb still free, off the hold, the wrist
    # not yet dropped: turned 15 less toward the palm, so the forearm comes in from the side
    film_palm=(dict(wrist=(8, 0), i=(25, 15, 15), m=(25, 15, 15), r=(25, 17, 15), l=(28, 17, 15),
                    thumb=dict(cmc=(-20, -30), mcp=5, ip=5)), 15.0),
    # 4 find a thumb spot below: the same, the thumb's pad now on the hold below the fingers
    film_thumb=(dict(wrist=(8, 0), i=(25, 15, 15), m=(25, 15, 15), r=(25, 17, 15), l=(28, 17, 15),
                     thumb=dict(cmc=(-10, -21), mcp=15, ip=10)), 15.0),
    # From behind, the open hand's drag over a rail: the index as the open hand's (O1, O2), the
    # other fingers alike, over the top beside it (ClimbingCrux's two hands sharing a hold, from
    # behind). Its thumb is tucked under the palm, out of sight from behind (BACK_THUMB)
    drag=(dict(wrist=(-8, 0), i=(10, 38, 45), m=(10, 40, 45), r=(12, 40, 45), l=(15, 38, 45),
               thumb=dict(cmc=(-10, 80), mcp=20, ip=40)), 0.0),
    # open-hand.svg (b), the three-finger drag: (a)'s open hand from behind, the same pose and
    # lean (which tips its back up toward you), the little finger curled off the edge
    drag3=(dict(wrist=(-8, 0), i=(10, 38, 45), m=(2, 58, 45), r=(-1, 51, 45), l=(20, 70, 20),
                thumb=dict(cmc=(-24, -4), mcp=5, ip=5)), 8.0),
    # the palm press: the hand flat on a volume's face, the fingers straight and spread, the
    # thumb out to the side (the reference's palm press and TripSavvy's palm on a slab: the heel
    # presses, the fingers lie flat). Seen from behind, flat on the face
    press_palm=(dict(wrist=(0, 0), i=(0, 5, 5), m=(0, 5, 5), r=(0, 5, 5), l=(0, 5, 5),
                     spread=dict(i=6.0, m=0.0, r=-6.0, l=-12.0),
                     thumb=dict(cmc=(-20, 0), mcp=5, ip=5)), 0.0),
    # the half crimp on an incut edge: the same hand with the end joint curled 40 behind the lip
    half_incut=(dict(wrist=(-15, 0), i=(15, 85, 40), m=(10, 98, 40), r=(3, 93, 40), l=(4, 73, 40),
                     thumb=dict(cmc=(-20, -8), mcp=5, ip=5)), 15.0),
    # H2 (a true side view), the book's "about 85-90" (C25): knuckle 15, middle joint 85, end
    # joint bent back 5, wrist bent back 15, the back of the hand upright; the thumb nearly
    # straight, raised along the palm, its tip free about 1 cm under the middle segment. From
    # behind its tip comes level with the index's middle joint
    half=(dict(wrist=(-15, 0), i=(15, 85, -5), m=(10, 98, -5), r=(3, 93, -5), l=(4, 73, -5),
               thumb=dict(cmc=(-20, -8), mcp=5, ip=5)), 15.0),
    # F1-F5, Fischer 2024: knuckle 35, middle joint 108, end joint bent back 25, wrist bent
    # back 25; the thumb crosses the index's end segment, its pad on the nail, its tip just
    # past and above the index's tip
    # The other fingers curl in line with the index, so their knuckles stay behind its crest
    full=(dict(wrist=(-25, 0), i=(35, 108, -25), m=(38, 108, -20), r=(35, 110, -20), l=(30, 110, -20),
               thumb=dict(cmc=(-18, -6), mcp=30, ip=15)), 20.0),
    # S1 (a true side view): the fingers nearly straight and draped as the index, the wrist
    # below the hold and turned toward the palm, which lies on it; the thumb's pad on the hold
    # below the fingers. The knuckle and wrist were fitted to the atlas's dome.
    sloper=(dict(wrist=(23, 0), i=(25, 15, 15), m=(25, 15, 15), r=(25, 17, 15), l=(28, 17, 15),
                 thumb=dict(cmc=(-10, -21), mcp=15, ip=10)), 0.0),
    # Wrapping an arête, its two faces opened out flat (wrap.svg): seen from the back of the
    # hand, the palm and thumb on one face, the fingers round the edge onto the other. Opened
    # flat, the fingers' bend round the edge comes out straight (b3 wrap-1, wrap-2: 10-20 /
    # 30-40 / 10-20 on the rock). The thumb lies out beside the index, as wrap-1's does,
    # parted from it down to the web
    wrap=(dict(wrist=(0, 0), i=(0, 5, 5), m=(0, 5, 5), r=(0, 5, 5), l=(0, 5, 5),
               thumb=dict(cmc=(-20, -5), mcp=5, ip=5)), -86.0),
)


# A hand on a rail or edge seen from behind tucks its thumb under the palm, out of sight,
# as the photos from behind show it (back-1, a hangboard edge; back-4, two hands matched):
# the thumb's pose from behind comes from those photos, not from the side view, whose thumb
# is free below the edge. Folded in front of the palm, every point of its outline lies inside
# the hand's, behind the back of the hand (thumb_hidden)
BACK_THUMB = dict(cmc=(-10, 80), mcp=20, ip=40)
BACK_TUCKED = {"drag", "half"}

# grips seen from the thumb side of the other hand: drawn mirrored
MIRRORED = {"under"}
# from behind, a little from above, so the fingers curled over an edge's top show; no more,
# or the back of the hand shortens and the hand reads wide (photos back-1 and back-6 are
# nearly level)
BACK_PITCH = 10.0


# ---------------------------------------------------------------- solving a pose


def finger_to(pose, k, target, dip=None, lo=(-20, 0), hi=(90, 125), rest=None):
    """The knuckle and middle joint that bring digit k's tip nearest to target (3D, in the
    forearm's frame), with its end joint at dip (or two thirds of the middle joint)."""
    best = None
    for mcp in range(lo[0], hi[0] + 1, 3):
        for pip in range(lo[1], hi[1] + 1, 3):
            P = dict(pose)
            P[k] = (mcp, pip, dip)
            s = Skeleton(P)
            tip = s.joints(k)[-1]
            e = v_len(v_sub(tip, target))
            if best is None or e < best[0]:
                best = (e, mcp, pip)
    e, mcp, pip = best
    for m2 in (mcp - 2, mcp - 1, mcp, mcp + 1, mcp + 2):
        for p2 in (pip - 2, pip - 1, pip, pip + 1, pip + 2):
            P = dict(pose)
            P[k] = (m2, p2, dip)
            tip = Skeleton(P).joints(k)[-1]
            e2 = v_len(v_sub(tip, target))
            if e2 < best[0]:
                best = (e2, m2, p2)
    return best


def thumb_to(pose, target, mcp, ip, rng=((-40, 90), (-30, 90))):
    """The CMC angles that bring the thumb's tip, or its pad, nearest to target."""
    best = None
    for a in range(rng[0][0], rng[0][1] + 1, 4):
        for b in range(rng[1][0], rng[1][1] + 1, 4):
            P = dict(pose)
            P["thumb"] = dict(cmc=(a, b), mcp=mcp, ip=ip)
            s = Skeleton(P)
            tip = s.joints("t")[-1]
            e = v_len(v_sub(tip, target))
            if best is None or e < best[0]:
                best = (e, a, b)
    e, a, b = best
    for a2 in range(a - 3, a + 4):
        for b2 in range(b - 3, b + 4):
            P = dict(pose)
            P["thumb"] = dict(cmc=(a2, b2), mcp=mcp, ip=ip)
            tip = Skeleton(P).joints("t")[-1]
            e2 = v_len(v_sub(tip, target))
            if e2 < best[0]:
                best = (e2, a2, b2)
    return best


def thumb_reach(pose, tip, ip_at=None, w_ip=0.7, mcps=(0, 10, 20, 30, 40), ips=(0, 10, 20, 30)):
    """The whole thumb, angles and all, that puts its tip nearest `tip` and, if given, its
    end joint nearest `ip_at`, which sets the angle it crosses at. Returns (error, thumb)."""
    best = None
    for mcp in mcps:
        for ip in ips:
            for a in range(-40, 91, 6):
                for b in range(-40, 91, 6):
                    P = dict(pose)
                    P["thumb"] = dict(cmc=(a, b), mcp=mcp, ip=ip)
                    J = Skeleton(P).joints("t")
                    e = v_len(v_sub(J[-1], tip)) + (w_ip * v_len(v_sub(J[-2], ip_at)) if ip_at else 0.0)
                    if best is None or e < best[0]:
                        best = (e, a, b, mcp, ip)
    e, a, b, mcp, ip = best
    for a2 in range(a - 4, a + 5, 2):
        for b2 in range(b - 4, b + 5, 2):
            P = dict(pose)
            P["thumb"] = dict(cmc=(a2, b2), mcp=mcp, ip=ip)
            J = Skeleton(P).joints("t")
            e2 = v_len(v_sub(J[-1], tip)) + (w_ip * v_len(v_sub(J[-2], ip_at)) if ip_at else 0.0)
            if e2 < best[0]:
                best = (e2, a2, b2, mcp, ip)
    e, a, b, mcp, ip = best
    return e, dict(cmc=(a, b), mcp=mcp, ip=ip)


# ---------------------------------------------------------------- consistency


def bones(hand):
    """The length of every bone as posed, to check that no pose changes the hand."""
    s = hand.skel
    out = {}
    for k in "imrlt":
        J = s.joints(k)
        out[k] = tuple(round(v_len(v_sub(b, a)), 6) for a, b in zip(J, J[1:]))
    return out


def check_same_hand(hands):
    """Every hand has the same bones and is drawn at the same scale: returns a list of faults."""
    faults = []
    ref = bones(hands[0][1])
    for fig_scale, h in hands:
        if bones(h) != ref:
            faults.append(f"{h.name}: bones differ")
        if abs(fig_scale - H.HAND_SCALE) > 1e-9:
            faults.append(f"{h.name}: drawn at {fig_scale} mm/cm, not {H.HAND_SCALE}")
    return faults
