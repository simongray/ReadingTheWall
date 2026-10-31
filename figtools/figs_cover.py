"""The cover: a pelican bouldering in the gym.

A pun on the well-known test of asking a language model for an SVG of "a
pelican riding a bicycle". The bird is a great white pelican (white body,
black flight feathers, long flat bill with a hooked nail, a throat pouch,
short legs and big webbed feet), drawn in the book's pen and greys on a
perspective gym wall. It hooks the nail of its bill over a jug like a heel
hook.
"""

import math

from climb import *          # noqa: F401,F403
from climb import _draw_group

OUT_SW = 0.32        # outlines, as the climbers
IN_SW = 0.24         # inner lines
FEATHER = "#2b2b2b"  # flight feathers
QUILL = "#7a7a7a"    # feather edges on the dark feathers
BILL = "#d4d4d4"
NAIL = "#9a9a9a"
POUCH = "#b4b4b4"
WRINKLE = "#6e6e6e"
FOOT = "#a4a4a4"
TOE_LINE = "#5c5c5c"

LINE = dict(stroke=INK, sw=OUT_SW, dash=None)


# ---------------------------------------------------------------- geometry

def place(c, deg, s=1.0, mirror=False):
    """Local (x, y) -> world: scaled by s, mirrored in y if asked, rotated
    by deg and moved to c."""
    m = -1 if mirror else 1

    def P(x, y=None):
        if y is None:
            x, y = x
        return add(c, rot((x * s, y * s * m), deg))
    return P


def curve(ctrl, closed=True, k=8):
    """A dense polyline through the control points."""
    pts = catmull(ctrl, closed=closed, k=k)
    return pts if closed else pts + [ctrl[-1]]


def interp(vals, t):
    """Piecewise-linear lookup in vals (evenly spaced over 0..1)."""
    n = len(vals) - 1
    i = min(int(t * n), n - 1)
    u = t * n - i
    return vals[i] + (vals[i + 1] - vals[i]) * u


def band(ctrl, widths, k=10):
    """A tube of varying width along a smooth centreline (open ends)."""
    C = curve(ctrl, closed=False, k=k)
    n = len(C)
    L, R = [], []
    for i, p in enumerate(C):
        w = interp(widths, i / (n - 1)) / 2
        d = norm(sub(C[min(i + 1, n - 1)], C[max(i - 1, 0)]))
        nv = perp(d)
        L.append(add(p, mul(nv, w)))
        R.append(add(p, mul(nv, -w)))
    return L + R[::-1], C, L, R


def stroke(f, pts, z, sw=IN_SW, color=INK, smooth=True, k=6):
    """A thin open pen line through pts (smoothed)."""
    P = curve(pts, closed=False, k=k) if (smooth and len(pts) > 2) else pts
    f.poly(P, closed=False, z=z, stroke=color, sw=sw)


def shape(f, pts, fill, z, sw=OUT_SW, stroke_=INK):
    f.poly(pts, closed=True, z=z, fill=fill, stroke=stroke_, sw=sw)


def edge(f, pts, z, sw=OUT_SW):
    """An outline run that is not tapered (part of a silhouette)."""
    f.poly(pts, closed=False, z=z, fill=None, stroke=INK, sw=sw, taper=False)


def centroid(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


# ---------------------------------------------------------------- the wall

Y0 = 6
SPREAD = 0.0008
STRETCH = 0.0004


def _wp(x, y):
    h = max(y - Y0, 0)
    return (x * (1 + SPREAD * h), y + STRETCH * h * h * 0.5)


def wall(f, x0=-260, x1=260, y1=300, step=20, seam=120):
    """The cover's wall: bolt holes and panel seams in a mild perspective,
    the kicker and the mat (as in figs_cover.py)."""
    y = 20
    while _wp(0, y)[1] <= y1:
        x = math.ceil(x0 / step) * step
        while x <= x1:
            p = _wp(x, y)
            if f.x0 + 2 < p[0] < f.x1 - 2 and p[1] < f.y1 - 2:
                f.circle(p, f.mm(0.32), z=-40, fill="#b0b0b0", stroke=None)
            x += step
        y += step
    for x in range(math.ceil(x0 / seam) * seam, x1 + 1, seam):
        pts = [_wp(x - seam / 2, y) for y in range(int(Y0), int(y1) + 40, 10)]
        f.poly(pts, closed=False, z=-41, stroke=LIGHT, sw=0.35)
    for y in range(int(Y0) + seam, int(y1) + 1, seam):
        pts = [_wp(x, y) for x in range(x0, x1 + 1, 10)]
        f.poly(pts, closed=False, z=-41, stroke=LIGHT, sw=0.35)
    f.poly([(f.x0, 0), (f.x1, 0), (f.x1, Y0), (f.x0, Y0)], z=-42, fill=PALE,
           stroke=None)
    f.line((f.x0, Y0), (f.x1, Y0), z=-41, sw=0.35, stroke=MID)
    ground(f, 0)


# ---------------------------------------------------------------- head

class Head:
    """The head in profile, eye at `eye`, the bill pointing at `deg`.

    Local frame: the eye at the origin, the bill along +x, the crown +y.
    `s` scales the whole head; `L` is the bill length in local units.
    flip: draw the other side of the head (the crown is then on the other
    side of the bill: use it when the bill points left, so the crown stays
    up). pouch: depth of the throat pouch; sag: how far the pouch hangs
    toward the ground rather than straight below the bill."""

    def __init__(self, eye, deg, s=1.25, L=36, flip=False, pouch=1.0, sag=0.6,
                 crest=True):
        self.P = place(eye, deg, s, flip)
        self.s, self.L, self.pouch, self.sag = s, L, pouch, sag
        self.crest = crest
        down = sub(self.P(0, -1), self.P(0, 0))
        self.g = norm(lerp(norm(down), (0, -1), sag))

    def low(self, x):
        """The lower edge of the lower mandible at bill station x."""
        return self.P(x, -2.5)

    def Q(self, x, depth):
        """A point `depth` (local units) below the lower mandible at x."""
        return add(self.low(x), mul(self.g, depth * self.s))

    def neck_join(self):
        """Centre and direction (down the neck) of the neck stub."""
        P = self.P
        c = lerp(P(-9.5, -9.0), P(-2.0, -9.0), 0.5)
        return c, norm(sub(P(-6.5, -14), P(-5.5, -6)))

    def silhouette(self):
        """The feathered head (and crest) as white pieces for a group."""
        P = self.P
        skull = [(4.4, 4.4), (2.0, 6.6), (-2.4, 8.0), (-7.0, 7.4), (-10.6, 4.8),
                 (-12.0, 0.6), (-11.6, -4.0), (-10.4, -10.0), (-2.0, -10.0),
                 (-1.0, -4.6), (1.6, -2.6), (3.6, 0.4)]
        pieces = [dict(pts=[P(p) for p in curve(skull, k=8)], fill=WHITE)]
        if self.crest:
            # a short, soft crest at the back of the crown
            tuft = [(-8.0, 6.6), (-12.4, 6.0), (-15.0, 3.6), (-12.6, 3.4),
                    (-14.2, 0.8), (-11.4, 0.6), (-11.0, -1.0)]
            pieces.insert(0, dict(pts=[P(p) for p in curve(tuft, k=6)],
                                  fill=WHITE))
        return pieces

    def draw(self, f, z, neck=None):
        """Bill, pouch and eye. With `neck` (white pieces), also the feathered
        head merged with them into one silhouette; without it the head's
        silhouette is left to the body group."""
        P, Q, L, pd = self.P, self.Q, self.L, self.pouch
        if neck is not None:
            _draw_group(f, z, list(neck) + self.silhouette(), [], LINE)
        # the pouch, hanging from the lower mandible and the throat
        ctrl = ([self.low(L - 2.0), Q(L * 0.82, 2.4 * pd), Q(L * 0.62, 7.2 * pd),
                 Q(L * 0.40, 9.8 * pd), Q(L * 0.18, 10.0 * pd),
                 Q(L * 0.0, 8.4 * pd), P(-3.4, -12.5)] +
                [P(-1.4, -5.0), self.low(2.0), self.low(L * 0.35),
                 self.low(L * 0.7)])
        C = curve(ctrl, k=8)
        f.poly(C, z=z + 0.1, fill=POUCH, stroke=None)
        # outline from the bill tip round the bottom to the throat
        n_out = 5 * 8 + 1
        edge(f, C[:n_out + 1], z + 0.11)
        # wrinkles in the pouch skin, following its lower edge
        for x0, x1, dep in ((0.74, 0.30, 3.6), (0.58, 0.10, 6.4),
                            (0.86, 0.56, 1.6)):
            dd = dep * pd
            stroke(f, [Q(L * x0, dd * 0.75), Q(L * (x0 + x1) / 2, dd),
                       Q(L * x1, dd * 0.92)], z + 0.12, sw=0.2, color=WRINKLE)
        stroke(f, [P(-1.6, -7.2), Q(L * 0.05, 6.6 * pd)], z + 0.12, sw=0.2,
               color=WRINKLE)
        # lower mandible: a thin strip along the top of the pouch
        def top(x):
            return P(x, -1.3 + 0.5 * x / L)
        lower = [P(2.6, -1.6), top(L * 0.3), top(L * 0.7), top(L - 1.6),
                 self.low(L - 1.8), self.low(L * 0.7), self.low(L * 0.3),
                 self.low(2.8)]
        shape(f, curve(lower, k=6), BILL, z + 0.19, sw=0.26)
        # upper mandible: long and flat, deep at the base, hooked nail
        upper = [(3.0, 4.4), (L * 0.3, 3.4), (L * 0.7, 2.8), (L - 1.0, 2.6),
                 (L + 1.0, 2.2), (L + 2.2, 0.6), (L + 2.0, -1.8),
                 (L + 1.0, -3.5), (L + 0.3, -3.0), (L + 0.4, -1.3),
                 (L - 1.6, -0.6),
                 (L * 0.6, -0.8), (L * 0.25, -1.2), (2.4, -1.9), (0.6, 0.2),
                 (1.2, 2.8)]
        shape(f, [P(p) for p in curve(upper, k=6)], BILL, z + 0.2)
        nail = [(L - 1.4, 2.65), (L + 1.0, 2.2), (L + 2.2, 0.6), (L + 2.0, -1.8),
                (L + 1.0, -3.5), (L + 0.3, -3.0), (L + 0.4, -1.3),
                (L - 1.0, -0.4), (L - 1.8, 1.2)]
        shape(f, [P(p) for p in curve(nail, k=5)], NAIL, z + 0.21, sw=0.26)
        # the ridge along the upper mandible
        stroke(f, [P(5.0, 2.3), P(L * 0.5, 1.5), P(L - 2.2, 1.2)], z + 0.22,
               sw=0.22, color="#7a7a7a")
        # bare skin round the eye, the eye
        skin = [(3.4, 3.4), (0.4, 3.4), (-2.6, 1.6), (-2.8, -0.8),
                (-0.6, -2.0), (2.4, -1.8)]
        f.poly([P(p) for p in curve(skin, k=6)], z=z + 0.15, fill=BILL,
               stroke=None)
        e = P(-0.2, 0.6)
        f.circle(e, 1.8 * self.s, z=z + 0.3, fill=WHITE, stroke=INK, sw=0.24)
        f.circle(add(e, mul(sub(P(1, 0), P(0, 0)), 0.15)), 1.0 * self.s,
                 z=z + 0.31, fill=INK, stroke=None)
        f.circle(add(e, (0.45 * self.s, 0.45 * self.s)), 0.32 * self.s,
                 z=z + 0.32, fill=WHITE, stroke=None)


# ---------------------------------------------------------------- wings

def _smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def quill(r, th0, l, curl=0.0, bend=0.5, n=18):
    """Centreline of a feather from r: straight at angle th0 (degrees) for
    `bend` of its length, then curving by `curl` degrees to the tip."""
    pts, angs, p = [r], [th0], r
    ds = l / n
    for i in range(n):
        s = (i + 0.5) * ds
        a = th0 + curl * max(0.0, (s - bend * l) / (l * (1 - bend)))
        p = add(p, mul(ang(a), ds))
        pts.append(p)
        angs.append(a)
    return pts, angs


def vane(pts, angs, w, notch=0.5, blunt=False):
    """Outline of a feather along a centreline: full width w for the inner
    half, narrowing to notch * w toward the tip; rounded or blunt tip."""
    n = len(pts) - 1
    L, R = [], []
    for i in range(n + 1):
        t = i / n
        hw = w / 2 * (1 - (1 - notch) * _smoothstep((t - 0.42) / 0.3))
        hw *= 0.15 + 0.85 * _smoothstep(t / 0.3)     # quill end, under coverts
        if not blunt:
            hw *= 1 - 0.55 * _smoothstep((t - 0.86) / 0.14)
        nv = perp(ang(angs[i]))
        L.append(add(pts[i], mul(nv, hw)))
        R.append(add(pts[i], mul(nv, -hw)))
    tip = add(pts[-1], mul(ang(angs[-1]), w * notch * (0.1 if blunt else 0.45)))
    return L + [tip] + R[::-1]


def at(pts, t):
    """The point at fraction t along a polyline (by index)."""
    t = max(0.0, min(1.0, t)) * (len(pts) - 1)
    i = min(int(t), len(pts) - 2)
    return lerp(pts[i], pts[i + 1], t - i)


# Both wings are the same wing: the arm (shoulder to wrist), the hand bones
# (wrist to where the outer primaries grow), the outer primaries (the
# 'fingers') and the breadth of the arm. A pose only bends them.
WING = dict(arm=66.0, hand=22.0, finger=48.0, chord=37.0, nf=4, nprim=9,
            nsec=14, finger_w=6.2)


def _fingers(W, u2, sgn, curl, spread, P=WING):
    """The outer primaries of a hand at W pointing along u2: they grow along
    the end of the hand and fan toward the trailing edge, `spread` degrees
    apart, their tips curling by `curl` degrees toward it."""
    H = add(W, mul(u2, P["hand"]))
    nprim, nf = P["nprim"], P["nf"]
    roots = [lerp(H, W, i / (nprim - 1) * 0.92) for i in range(nprim)]
    th0 = math.degrees(math.atan2(u2[1], u2[0]))
    out = []
    for i in range(nf):
        th = th0 + sgn * 2 - sgn * spread * i
        pts, angs = quill(roots[i], th, P["finger"] * (1 - 0.05 * i),
                          -sgn * curl)
        out.append((pts, angs, P["finger_w"], 0.55, P["finger"] * (1 - 0.05 * i)))
    return H, roots, out


def pose_wing(S, target, toward, curl, spread, P=WING):
    """Two-bone IK for a wing: the wrist W that puts the centre of the
    finger tips on `target`, the wrist bent toward the leading edge (the hand
    swept back) as in a bird. Returns (W, u2, sgn)."""
    v = sub(target, S)
    d = length(v)
    sgn = 1 if dot(perp(norm(v)), sub(toward, S)) > 0 else -1
    # the finger tips' centre in the hand's own frame
    H, roots, fing = _fingers((0.0, 0.0), (1.0, 0.0), sgn, curl, spread, P)
    T0 = centroid([fp[0][-1] for fp in fing])
    a, b = T0[0], T0[1] * sgn             # along the hand, toward the lead
    E = math.hypot(a, b)
    phi = math.degrees(math.atan2(b, a))
    L1 = P["arm"]
    d = min(d, L1 + E - 0.5)
    alpha = math.degrees(math.acos(max(-1.0, min(1.0, (L1 * L1 + d * d - E * E) /
                                                  (2 * L1 * d)))))
    th = math.degrees(math.atan2(v[1], v[0]))
    W = add(S, mul(ang(th + sgn * alpha), L1))
    u2 = rot(norm(sub(target, W)), -sgn * phi)
    return W, u2, sgn


def wing(f, S, target, toward, z, curl=0.0, spread=7.0, fan=14.0, covert=1.0,
         P=WING):
    """A wing seen from above, from the shoulder S, posed so its finger tips
    reach `target`; the leading edge faces the point `toward`. curl and
    spread are the fingers' grip on the hold. Returns the finger tips."""
    W, u2, sgn = pose_wing(S, target, toward, curl, spread, P)
    u1, L1 = norm(sub(W, S)), length(sub(W, S))
    n1 = mul(perp(u1), sgn)        # toward the leading edge
    n2 = mul(perp(u2), sgn)
    chord, nprim, nf, nsec = P["chord"], P["nprim"], P["nf"], P["nsec"]
    H, roots, prim = _fingers(W, u2, sgn, curl, spread, P)
    tips = [fp[0][-1] for fp in prim]

    # secondaries: overlapping feathers along the arm; the inner ones are
    # shorter, so the trailing edge curves into the body at the armpit
    sec = []
    for j in range(nsec):
        t = j / (nsec - 1)
        e = norm(add(mul(n1, -1), mul(u1, -0.05 + 0.32 * t)))
        l = chord * (1.0 - 0.10 * t) * (0.55 + 0.45 * _smoothstep(t / 0.3))
        base = add(lerp(S, W, t), mul(n1, -2.0))
        th = math.degrees(math.atan2(e[1], e[0]))
        pts, angs = quill(base, th, l, n=10)
        sec.append((pts, angs, L1 / (nsec - 1) * 2.2, 0.92, l))
    # the inner primaries end on a curve that bows out from the last finger
    # back to the secondaries at the wrist: the hand's feathers fan out
    ni = nprim - nf
    A = at(prim[nf - 1][0], 0.62) if curl else prim[nf - 1][0][-1]
    B = sec[-1][0][-1]
    ctl = add(lerp(A, B, 0.5), mul(n2, -fan / 100 * length(sub(B, A))))
    for k in range(ni):
        t = (k + 1) / (ni + 1)
        q = add(add(mul(A, (1 - t) ** 2), mul(ctl, 2 * t * (1 - t))),
                mul(B, t * t))
        r = roots[nf + k]
        v = sub(q, r)
        th = math.degrees(math.atan2(v[1], v[0]))
        pts, angs = quill(r, th, length(v))
        prim.append((pts, angs, 10.0, 0.85, length(v)))

    # the flight feathers as one dark silhouette; inside it the edge of
    # each feather where it lies over the next
    pieces, lines = [], []
    for pts, angs, w, notch, l in sec:
        pieces.append(dict(pts=curve(vane(pts, angs, w, notch, blunt=True), k=3),
                           fill=FEATHER))
    for i, (pts, angs, w, notch, l) in enumerate(prim):
        pieces.append(dict(pts=curve(vane(pts, angs, w, notch, blunt=i >= nf),
                                     k=3), fill=FEATHER))

    def side(pts, angs, w, notch, t0, t1, sd):
        n = len(pts) - 1
        out = []
        for i in range(int(t0 * n), int(t1 * n) + 1):
            t = i / n
            hw = w / 2 * (1 - (1 - notch) * _smoothstep((t - 0.42) / 0.3))
            out.append(add(pts[i], mul(perp(ang(angs[i])), sd * hw * 0.85)))
        return out
    for j in range(2, nsec, 2):
        pts, angs, w, notch, l = sec[j]
        sd = 1 if dot(perp(ang(angs[0])), u1) < 0 else -1   # toward the body
        lines.append(dict(pts=side(pts, angs, w, notch, 0.55, 0.97, sd),
                          stroke=QUILL, sw=0.22))
    for pts, angs, w, notch, l in prim[1:]:
        lines.append(dict(pts=side(pts, angs, w, notch, 0.45, 0.88, sgn),
                          stroke=QUILL, sw=0.22))
    _draw_group(f, z, pieces, lines, LINE)

    # coverts: white, over the bases of the flight feathers
    p0 = prim[0]
    lead = [add(S, mul(n1, 2.0)), add(lerp(S, W, 0.45), mul(n1, 5.4)),
            add(W, mul(n1, 3.6)), add(lerp(W, H, 0.55), mul(n2, 3.4)),
            add(p0[0][0], mul(n2, 3.2)),
            add(p0[0][3], mul(perp(ang(p0[1][3])), sgn * p0[2] * 0.42))]
    hand_b = [at(prim[i][0], (0.2 + 6.0 / prim[i][4]) * covert)
              for i in (0, nf - 1, nprim - 1)]
    arm_b = [at(pts, 0.5 * covert) for pts, *_ in sec[::-2]]
    arm_b.append(add(S, mul(n1, -chord * 0.5)))
    sc = list(hand_b)
    for a_, b_ in zip([hand_b[-1]] + arm_b, arm_b):
        sc += [add(lerp(a_, b_, 0.5), mul(n1, 1.8)), b_]
    C = curve(lead + sc, closed=True, k=5)
    f.poly(C, z=z + 0.1, fill=WHITE, stroke=None)
    m = (len(lead) - 1) * 5
    edge(f, C[:m + 1], z + 0.101)
    edge(f, C[m:len(C) - 5], z + 0.101, sw=0.26)
    # a row of small coverts along the leading edge
    row = [add(lerp(S, W, 0.2), mul(n1, -3)), add(lerp(S, W, 0.55), mul(n1, -1)),
           add(W, mul(n1, -3.5)), add(lerp(W, H, 0.6), mul(n2, -3.5))]
    stroke(f, row, z + 0.102, sw=0.22, color=MID)
    return tips


# ---------------------------------------------------------------- feet

# toe: angle from the foot's axis (deg), length, width at base and tip (cm)
TOES = [(-60, 10.5, 2.8, 1.7), (-25, 18.5, 3.0, 1.9), (3, 23.5, 3.2, 2.0),
        (29, 21.5, 3.0, 1.9)]
WEB = "#bdbdbd"


def foot(f, A, deg, z, mirror=False, squash=1.0, size=1.0, claws=True):
    """A webbed foot (all four toes joined by web) seen from above, the
    middle toe pointing at `deg`, its heel at A. squash < 1 foreshortens it
    across (a foot seen at a slant). mirror: the short hind toe on the
    other side. Returns the world points of the toe tips."""
    m = -1 if mirror else 1
    u = ang(deg)
    nv = mul(perp(u), m * squash)

    def F(p):
        return add(A, add(mul(u, p[0] * size), mul(nv, p[1] * size)))

    def toe_pt(k, t, side):
        a, l, w0, w1 = TOES[k]
        v = ang(a)
        sd = perp(v)
        hw = (w0 + (w1 - w0) * t) / 2
        return (v[0] * l * t + sd[0] * hw * side, v[1] * l * t + sd[1] * hw * side)

    def tip(k):
        a, l, w0, w1 = TOES[k]
        v = ang(a)
        return (v[0] * (l + w1 * 0.45), v[1] * (l + w1 * 0.45))
    ring = [(-2.6, 0.0), toe_pt(0, 0.3, -1), toe_pt(0, 0.85, -1), tip(0)]
    for k in range(len(TOES)):
        if k:
            ring += [toe_pt(k, 0.94, -1), tip(k)]
        if k < len(TOES) - 1:
            a = toe_pt(k, 0.9, 1)
            b = toe_pt(k + 1, 0.9, -1)
            mid = lerp(a, b, 0.5)
            ring += [toe_pt(k, 0.94, 1), a, mul(mid, 0.9), b]
    ring += [toe_pt(3, 0.88, 1), toe_pt(3, 0.4, 1), (0.6, -2.4)]
    shape(f, [F(p) for p in curve(ring, k=4)], WEB, z)
    # the toes, darker than the web, with joints and claws
    out = []
    for k, (a, l, w0, w1) in enumerate(TOES):
        side_a = [toe_pt(k, t / 10, -1) for t in range(1, 10)]
        side_b = [toe_pt(k, t / 10, 1) for t in range(9, 0, -1)]
        pts = [F(p) for p in curve(side_a + [tip(k)] + side_b, k=3)]
        f.poly(pts, z=z + 0.01, fill=FOOT, stroke=None)
        for t in (0.42, 0.66, 0.86):
            stroke(f, [F(toe_pt(k, t, -0.8)), F(toe_pt(k, t, 0.8))], z + 0.02,
                   sw=0.2, color=TOE_LINE, smooth=False)
        v = norm(sub(F(tip(k)), F(toe_pt(k, 0.5, 0))))
        tp = F(tip(k))
        out.append(tp)
        if claws:
            c1 = sub(tp, mul(v, 0.5))
            c2 = add(add(tp, mul(v, 1.6 * size)), mul(perp(v), -0.5 * m))
            f.poly([add(c1, mul(perp(v), 0.65 * size)), c2,
                    add(c1, mul(perp(v), -0.65 * size))],
                   z=z + 0.02, fill="#3a3a3a", stroke="#3a3a3a", sw=0.12)
    return out


# ---------------------------------------------------------------- bird

def _scallop(p0, p1, n, out, depth=1.6):
    """Control points for a row of n feather tips bulging `out` between p0
    and p1 (p0 itself left out)."""
    pts = []
    for k in range(n):
        pts.append(add(lerp(p0, p1, (k + 0.5) / n), mul(out, depth)))
        pts.append(lerp(p0, p1, (k + 1) / n))
    return pts


class Pelican:
    """A great white pelican seen from behind, flat against the wall like
    the book's climbers, the body turned a little to its right (toward the
    hook) so the right breast shows. The body is a teardrop: a full breast
    that tapers to the tail, the shoulders sloping up into the neck. It is
    placed by its centre and tilt; wings, legs, neck and head are added.

    Local frame: x to the bird's right, y up, in units of the half width w
    and half height h."""

    K = 8                       # curve samples per control point
    LEG = 22.0                  # tarsus, from the hock to the ankle (cm)

    def __init__(self, c, tilt=0.0, w=35, h=46):
        self.c, self.tilt, self.w, self.h = c, tilt, w, h
        self.B = place(c, tilt, 1.0)
        self._outline()

    def L(self, x, y):
        return self.B(x * self.w, y * self.h)

    def shoulder(self, s):
        """The wing root, tucked in under the scapulars."""
        return self.L(s * 0.70, 0.56)

    def hock(self, s):
        """Where the leg leaves the belly feathers: low on the body, beside
        the tail, as in a pelican."""
        return self.L(s * 0.36, -0.86)

    def neck_base(self):
        return self.L(-0.02, 0.84)

    def _outline(self):
        """The body's outline as control points (local units), with the
        indices that bound the right flank. Small scallops mark the
        scapulars lying over each wing root; the tail's feather tips end the
        teardrop."""
        right = [(0.0, 0.98), (0.40, 0.92), (0.68, 0.78)]
        right += _scallop((0.68, 0.78), (0.95, 0.46), 3, norm((0.8, 0.6)), 0.03)
        i_flank0 = len(right) - 1
        right += [(1.07, 0.16), (1.06, -0.18), (0.95, -0.48), (0.76, -0.74),
                  (0.52, -0.94), (0.30, -1.08)]
        i_flank1 = len(right) - 1
        tail = [(0.20, -1.18), (0.16, -1.30)]
        tail += _scallop((0.16, -1.30), (-0.16, -1.30), 3, (0, -1), 0.04)
        tail += [(-0.20, -1.18)]
        left = [(-0.30, -1.07), (-0.50, -0.94), (-0.72, -0.72), (-0.90, -0.42),
                (-0.99, -0.08), (-0.96, 0.26)]
        left += _scallop((-0.96, 0.26), (-0.72, 0.66), 3, norm((-0.8, 0.6)),
                         0.03)
        left += [(-0.56, 0.84), (-0.30, 0.96)]      # the hunch below the neck
        ring = right + tail + left
        self.i_flank = (i_flank0, i_flank1)
        self.i_tail = (len(right) - 1, len(right) + len(tail))
        self.i_left = len(right) + len(tail)
        self.dense = [self.L(*p) for p in curve(ring, closed=True, k=self.K)]

    def dense_run(self, i0, i1):
        K = self.K
        return self.dense[i0 * K:i1 * K + 1]

    def leg(self, f, s, deg, z):
        """The bare tarsus, LEG long, from the hock at the angle deg. It is
        drawn under the body, so it comes out of the belly feathers. Returns
        the ankle."""
        hock = self.hock(s)
        ankle = add(hock, mul(ang(deg), self.LEG))
        shape(f, capsule(hock, 4.4, ankle, 3.5), FOOT, z)
        v = ang(deg)
        for t in (0.6, 0.8):
            p = add(hock, mul(v, self.LEG * t))
            q = perp(v)
            stroke(f, [add(p, mul(q, 2.4)), add(p, mul(v, 0.9)),
                       add(p, mul(q, -2.4))], z + 0.01, sw=0.2, color=TOE_LINE)
        return ankle

    def neck(self, head, bend=(8, 0.5), w0=31, w1=19):
        """A short neck in an S from the shoulders to the head: it rises
        back over the body (bend[0] sideways at fraction bend[1]) and then
        reaches forward into the head. Its base spreads into the shoulders,
        so the back runs on into the neck without a corner."""
        a = self.neck_base()
        c, dn = head.neck_join()
        b = sub(c, mul(dn, 9))
        v = norm(sub(b, a))
        mid = add(lerp(a, b, bend[1]), mul(perp(v), bend[0]))
        ctrl = [add(a, mul(v, -20)), a, mid, b, add(c, mul(dn, -3))]
        pts, *_ = band(ctrl, [w0 + 2, w0 + 4, (w0 + w1) / 2 + 1, w1, w1 - 0.5])
        return [dict(pts=pts, fill=WHITE)]

    def draw_body(self, f, z, extra=()):
        """The white silhouette of body, neck and head, then the body's
        form: the turned flank a shade darker, the base of the tail, and a
        little feather texture."""
        L = self.L
        _draw_group(f, z, [dict(pts=self.dense, fill=WHITE)] + list(extra), [],
                    LINE)
        # the right flank and breast, turned away from us
        i0, i1 = self.i_flank
        inner = [L(*p) for p in curve([(0.30, -1.02), (0.52, -0.82),
                                       (0.74, -0.48), (0.84, -0.12),
                                       (0.84, 0.22), (0.74, 0.52),
                                       (0.64, 0.66)], closed=False, k=8)]
        flank = self.dense_run(i0 - 2, i1) + inner
        f.poly(flank, z=z + 0.0015, fill=PALE, stroke=None)
        stroke(f, inner[::-1][:-10], z + 0.003, sw=0.24, color=MID,
               smooth=False)
        # the tail: its root under the rump feathers, a few feather lines
        stroke(f, [L(-0.26, -1.0), L(-0.10, -1.08), L(0.10, -1.08),
                   L(0.26, -1.0)], z + 0.003, sw=0.22, color=MID)
        for x in (-0.11, 0.0, 0.11):
            stroke(f, [L(x * 0.9, -1.12), L(x * 1.05, -1.24)], z + 0.003,
                   sw=0.22, color=MID)
        # feather texture: scapulars along the wing roots, a few rows of
        # small feathers on the mantle, long feathers on the flank
        for sx in (-1, 1):
            stroke(f, [L(sx * 0.36, 0.80), L(sx * 0.58, 0.64),
                       L(sx * 0.72, 0.40), L(sx * 0.76, 0.14)], z + 0.003,
                   sw=0.22, color=MID)
            stroke(f, [L(sx * 0.46, 0.40), L(sx * 0.56, 0.18),
                       L(sx * 0.58, -0.06)], z + 0.003, sw=0.22, color=MID)
        for y0, xs in ((0.58, (-0.22, 0.0, 0.22)),
                       (0.36, (-0.32, -0.11, 0.11, 0.32)),
                       (0.14, (-0.22, 0.0, 0.22)),
                       (-0.10, (-0.11, 0.11))):
            for x in xs:
                arc = [L(x - 0.10 + 0.2 * k / 6,
                         y0 - 0.035 * math.sin(math.pi * k / 6))
                       for k in range(7)]
                stroke(f, arc, z + 0.003, sw=0.22, color=LIGHT, smooth=False)
        for y in (0.06, -0.22, -0.48):
            stroke(f, [L(0.90, y + 0.10), L(0.94, y - 0.04),
                       L(0.86, y - 0.20)], z + 0.003, sw=0.22, color=MID)


# ---------------------------------------------------------------- the cover

def lip(pos, kind="crimp", use=90, n=4, size=1.0, spread=0.8):
    """n points spread along the grabbed lip of a hold, from its left end to
    its right, as seen with `use` up."""
    W = HOLD_SIZE[kind][0] * size
    H = HOLD_SIZE[kind][1] * size
    a = use - 90
    return [add(pos, rot(((-0.5 + (i + 0.5) / n) * W * spread, H * 0.42), a))
            for i in range(n)]


def beak_hook(path):
    """Beak hook: the pelican hooks the nail of its bill over a jug out to
    the right, like a heel hook, and pulls in with its neck; that frees the
    left wing to crimp far out left. The right wing palms a sloper, the left
    foot smears on a volume and the right foot edges on a foothold."""
    f = Fig(-196, -10, 196, 300)
    wall(f)
    HOOK = (76, 188)
    CRIMP = (-128, 222)
    SLOPER = (100, 104)
    FH = (35, 66.5)
    volume(f, [(-175, 34), (-10, 50), (-78, 130)], apex=(-90, 72),
           shades=["#d0d0d0", "#ececec", "#b9b9b9"])
    volume(f, [(104, 236), (176, 250), (160, 296), (110, 290)], apex=(140, 268))
    volume(f, [(96, 22), (150, 26), (122, 64)], apex=(123, 38),
           shades=["#d6d6d6", "#e8e8e8", "#c2c2c2"])
    hold(f, "jug", HOOK, size=1.1, chalk=True)
    hold(f, "crimp", CRIMP, size=1.5)
    hold(f, "sloper", SLOPER)
    hold(f, "foot", FH)
    for p, kind, use, size in [((-40, 290), "crimp", 90, 0.9),
                               ((40, 282), "jug", 90, 0.8),
                               ((170, 150), "sloper", 90, 0.9),
                               ((-160, 170), "pocket", 90, 1.0),
                               ((-60, 238), "foot", 90, 1.0),
                               ((150, 96), "crimp", 90, 0.8)]:
        hold(f, kind, p, use=use, size=size, xray=False)

    bird = Pelican((-16, 132), tilt=-6)
    # the head: the bill reaches down to the jug, its nail over the lip
    deg, hs, L = -22, 1.85, 36
    nail = (HOOK[0] + 3, HOOK[1] + 3.5)
    eye = sub(nail, rot(((L + 0.9) * hs, -3.4 * hs), deg))
    head = Head(eye, deg, s=hs, pouch=1.15, sag=0.7)
    wing(f, bird.shoulder(-1), centroid(lip(CRIMP, "crimp", n=4, size=1.5)),
         toward=(0, 260), z=2, curl=100, spread=3.5)
    wing(f, bird.shoulder(1), centroid(lip(SLOPER, "sloper", n=4)),
         toward=(0, 260), z=2, curl=80)
    # legs (the same length), feet (the same size), and what they stand on
    al = bird.leg(f, -1, 236, z=0.9)
    ar = bird.leg(f, 1, -62, z=0.9)
    foot(f, al, 145, z=1, mirror=True, size=1.25)
    foot(f, ar, -8, z=1, squash=0.86, size=1.25)
    neck = bird.neck(head)
    bird.draw_body(f, z=6, extra=neck + head.silhouette())
    head.draw(f, z=8)
    f.save(path)


# ---------------------------------------------------------------- ornaments
#
# The book's ornaments are holds, drawn by hold() like the holds in the
# figures: one for the title page, one for each part page and one for each
# chapter opening, each chosen for what its part or chapter is about. The
# front matter and the appendices share one quiet foothold. The table that
# maps the parts and chapters to them is `ornaments` in book/template.typ.
#
# Each ornament is drawn at the size it is set at, so its lines keep the
# figures' weights: the title page's at 12 pt (4.2 mm) tall, a chapter's at
# 5 mm between two rules, a part page's at 24 pt (8.5 mm). Every ornament of
# a set has the same height, its drawing centred in it, and is as wide as
# its drawing, so the rules either side of it stay the same distance away.

ORN_SETS = {
    # set: (paper height in mm, scale in mm per cm)
    "title": (12 * 0.3528, 0.36),
    "chapter": (5.0, 0.36),
    "part": (24 * 0.3528, 0.72),
}
ORN_PAD = 0.45       # mm of paper left and right of the drawing
ORN_VPAD = 0.3       # mm of paper the drawing needs above and below


def one(kind, size, use=90, **kw):
    """An ornament of a single hold at (0, 0)."""
    def draw(f):
        hold(f, kind, (0, 0), use=use, size=size, xray=False, **kw)
        return hold_outline(kind, (0, 0), use=use, size=size,
                           variant=kw.get("variant"), mirror=kw.get("mirror"))
    return draw


def grades(f):
    """A jug, a crimp and a chip in a row, each smaller: the holds shrink as
    the grade rises."""
    pts, x = [], 0.0
    for kind, size, v in (("jug", 0.9, "bucket"), ("crimp", 0.9, "rail"),
                          ("crimp", 0.9, "chip")):
        W = HOLD_SIZE[kind][0] * size * (0.7 if v == "chip" else 1.0)
        p = (x + W / 2, 0)
        hold(f, kind, p, size=size, variant=v, mirror=False, xray=False,
             chalk=True)
        pts += hold_outline(kind, p, size=size, variant=v, mirror=False)
        x += W + 4.2
    return pts


def volume_orn(f):
    """A small volume with its bolt."""
    out = [(-9.5, -5.6), (9.5, -5.6), (1.2, 6.4)]
    volume(f, out, apex=(0.9, -1.4), bolt=True)
    return out


# name: (set, drawing, what it means)
ORNAMENTS = {
    "jug": ("title", one("jug", 0.95, variant="bucket", chalk=True),
            "the book's emblem: the hold every climber knows"),
    "sidepull": ("part", one("jug", 0.62, use=0, variant="bucket", chalk=True),
                 "Part I: a hold has a direction, the idea Part I builds on"),
    "sloper": ("chapter", one("sloper", 0.78, variant="dome", chalk=True),
               "How movement works: only the body's position holds a sloper"),
    "chalked": ("chapter", one("jug", 0.8, variant="flat", chalk=True),
                "Reading a problem: chalk on a hold shows where others have "
                "taken it"),
    "macro": ("part", one("macro", 0.6, variant="facet", mirror=False),
              "Part II: a macro, a hold you can take a dozen ways"),
    "foothold": ("chapter", one("foot", 1.75, variant="screw-on", rubber=True),
                 "Feet and legs: a foothold, rubber on its top"),
    "undercling": ("chapter", one("jug", 0.72, use=270, variant="bucket",
                                  chalk=True),
                   "Body positioning: an undercling holds only with the hips "
                   "and feet in place"),
    "crimp": ("chapter", one("crimp", 1.3, variant="rail", chalk=True),
              "Hands and holds: the crimp, the grip the chapter keeps returning to"),
    "dual": ("chapter", one("dual", 0.7, variant="dual", mirror=False),
             "Dynamic movement: a dual-texture hold of comp-style setting"),
    "volume": ("chapter", volume_orn,
               "Terrain: a volume changes the wall's angle"),
    "grades": ("part", grades,
               "Part III: the holds shrink as the grade rises"),
    "chip": ("chapter", one("crimp", 1.5, variant="chip", mirror=False,
                            chalk=True),
             "Grade by grade: the small chip the grades lead to"),
    "pinch": ("part", one("pinch", 0.8, variant="block"),
              "Part IV: a pinch fits each hand differently, as holds fit "
              "each body differently"),
    "pocket": ("chapter", one("pocket", 1.35, variant="two", mirror=False),
               "Your body: a pocket loads the finger pulleys most"),
    "foot-chip": ("chapter", one("foot", 1.45, variant="chip", mirror=False),
                  "front matter and appendices: the quiet foothold"),
    "foot-chip-large": ("part", one("foot", 1.8, variant="chip", mirror=False),
                        "Appendices: the quiet foothold"),
}


def ornament_fig(name):
    """The Fig of an ornament, framed to its set's height."""
    kind, draw, _ = ORNAMENTS[name]
    height, scale = ORN_SETS[kind]
    pts = draw(Fig(-100, -100, 100, 100, scale))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    pad = ORN_PAD / scale
    H = height / scale
    cy = (min(ys) + max(ys)) / 2
    assert max(ys) - min(ys) + 2 * ORN_VPAD / scale <= H + 1e-6, name + " is too tall"
    f = Fig(min(xs) - pad, cy - H / 2, max(xs) + pad, cy + H / 2, scale)
    draw(f)
    return f


def ornament(path):
    """The title page's ornament (also written as ornament-jug.svg)."""
    ornament_fig("jug").save(path)


def build(out):
    beak_hook(out + "/cover.svg")
    ornament(out + "/ornament.svg")
    for name in ORNAMENTS:
        ornament_fig(name).save(out + f"/ornament-{name}.svg")
