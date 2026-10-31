"""One hand for every close-up in the book.

The hand is a 3D model in centimetres, drawn in orthographic projection, so
a pose looks the same from every side and every close-up shows the same
hand at the same paper size (HAND_SCALE). Its proportions are those of an
adult hand 19 cm long from the wrist crease to the tip of the middle finger.

Hand frame (a right hand): x runs from the middle of the wrist crease toward
the middle finger, y toward the thumb, z out of the back of the hand.

Pose. Each finger is a chain of three joints, the knuckle (MCP), the middle
joint (PIP) and the end joint (DIP); its angles are flexion in degrees,
positive toward the palm. The thumb has its base joint (CMC: `ra` radial
abduction away from the index, `pa` palmar abduction out of the palm,
`rot` how far the thumbnail is turned from facing the same way as the
fingernails: about 90 faces the nail away from the index, more turns the
pad toward the fingers), its knuckle
(`mcp`) and its end joint (`ip`). The wrist extends (`ext`, bends back) and
deviates toward the thumb (`dev`).

Views (`Hand.view`):
- "thumb": from the thumb side, the standard profile. The palm faces right
  (toward the wall in the side-view convention), the index finger is in
  front, white, and the other fingers are drawn behind it, each its own
  finger in a lighter grey, stepped a little aside (STAGGER) so that their
  knuckles and tips show. tilt turns the back of the hand toward you.
- "little": from the little-finger side, palm facing right; the thumb and
  the fingers behind are grey.
- "back": the back of the hand, thumb on the left when the fingers point up.
- "palm": the palm, thumb on the right.
`a0` is the screen direction of the hand (wrist to knuckles) and `flip`
mirrors the drawing (the palm then faces left in a profile).

Every part is built as convex hulls of cross-section rings (a tube per
finger segment, a rounded wedge per joint, the palm, the ball of the thumb
and the forearm), projected and merged with the silhouette technique of
climb.py. Nails (seen from the side, a line inside the back of the
fingertip), joint creases, knuckle arcs on the back of a bent hand and the
fine lines between fingers are drawn on top.

Typical use (a half crimp on an edge whose top meets the wall at WX, 0):

    h = Hand("half")                                   # a grip from GRIPS
    p = h.view("thumb").place("i", (WX - 0.85, 0), a0=95, k=0.85)
    h.rest_thumb()                       # or p.thumb_to(...) where it grips
    p.draw(fig)
    joint_arc(fig, p, "i", "pip", 1.5, "≈90°")

place() puts a finger pad on a page point with the hand at a0 (or with the
last segment pointing along `distal`); reach() and thumb_to() solve finger
and thumb joints for a contact point; joint(), angle(), surface() and at()
read page points back for labels and arrows. grip_profile() draws the
standard side views of the open hand, half crimp, full crimp and thumb lock.
"""

import math

from climb import (INK, WHITE, LIGHT, MID, PALE, DARK, Fig, ang, add, sub, mul, norm,
                   length, rot, lerp, perp, dot, XRAY, XRAY_Z, XRAY_STYLE)

HAND_SCALE = 2.6        # paper mm per cm, for every hand close-up in the book

OUTLINE = 0.34          # outline weights in mm, as elsewhere in the book
BACK_SW = 0.26          # the fingers behind the front one in a side view
FINE = 0.20             # lines between fingers that touch
DETAIL = 0.24           # nails and creases

# ---------------------------------------------------------------- 3D vectors


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vmul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def vlen(a):
    return math.sqrt(vdot(a, a))


def vnorm(a):
    n = vlen(a)
    return vmul(a, 1 / n) if n else (0.0, 0.0, 0.0)


def vlerp(a, b, t):
    return vadd(a, vmul(vsub(b, a), t))


def vsum(*vs):
    out = (0.0, 0.0, 0.0)
    for x in vs:
        out = vadd(out, x)
    return out


X, Y, Z = (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)


def flexed(frame, deg):
    """A segment frame (A along the bone, N toward the back, L across)
    bent toward its palm side by `deg`."""
    A, N, L = frame
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return (vsub(vmul(A, c), vmul(N, s)), vadd(vmul(N, c), vmul(A, s)), L)


def frame_of(A, N):
    A = vnorm(A)
    N = vnorm(vsub(N, vmul(A, vdot(N, A))))
    return (A, N, vcross(N, A))


def spin(v, axis, deg):
    """Rotate v about the unit vector `axis` (Rodrigues)."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return vsum(vmul(v, c), vmul(vcross(axis, v), s),
                vmul(axis, vdot(axis, v) * (1 - c)))

# ---------------------------------------------------------------- anatomy
#
# Lengths in cm for a hand 19 cm long. The knuckle joints sit about 1.3 cm
# inside the palm: the skin of the palm runs on to the webs between the
# fingers (about 10.7 cm from the wrist crease), while the joint centres of
# the middle finger are 9.35 + 4.4 + 2.8 + 2.0 + pad 0.45 = 19 cm long.

MCP = {"i": (9.0, 3.0, 0.0), "m": (9.35, 1.0, 0.05), "r": (9.05, -1.0, 0.0),
       "l": (8.35, -2.95, -0.15)}
SEG = {"i": (4.0, 2.4, 1.9), "m": (4.4, 2.8, 2.0), "r": (4.1, 2.7, 1.9),
       "l": (3.2, 1.9, 1.7)}
PAD = {"i": 0.45, "m": 0.45, "r": 0.45, "l": 0.4}
SPLAY = {"i": 5.0, "m": 0.0, "r": -5.0, "l": -11.0}   # relaxed, toward the thumb
GIRTH = {"i": 1.0, "m": 1.02, "r": 0.97, "l": 0.88}
FINGERS = "imrl"
NAMES = {"i": "index", "m": "middle", "r": "ring", "l": "little", "t": "thumb"}

# cross-sections along each finger segment, for an index finger:
# (fraction of the segment, half-width, back, palm side), from the bone axis.
# Thickness in profile (back + palm side) is 1.9 cm along the first
# segment, 1.7 along the middle one and 1.5 along the last, the pad
# fullest under the nail.
SECTIONS = (
    ((0.00, 1.00, 0.90, 1.40), (0.28, 0.98, 0.86, 1.06), (0.65, 0.95, 0.84, 1.06),
     (1.00, 0.96, 0.86, 1.00)),
    ((0.00, 0.96, 0.86, 1.00), (0.50, 0.88, 0.78, 0.96), (1.00, 0.83, 0.73, 0.90)),
    ((0.00, 0.83, 0.73, 0.90), (0.50, 0.79, 0.64, 0.92), (0.95, 0.74, 0.56, 0.84)),
)
KNUCKLE = (0.98, 1.02, 1.33)     # the metacarpal head, round which the knuckle bends

# thumb: metacarpal, proximal and distal (end joint to the tip of the pad)
THUMB_SEG = (4.5, 3.2, 2.7)
CMC = (1.5, 2.3, -0.9)         # base of the thumb metacarpal
THUMB_SECTIONS = (    # 2.2 cm across, about 2.1 cm thick
    ((0.45, 1.12, 0.95, 1.15), (1.00, 1.14, 0.98, 1.15)),
    ((0.00, 1.14, 0.98, 1.15), (0.50, 1.08, 0.92, 1.16), (1.00, 1.10, 0.92, 1.12)),
    ((0.00, 1.10, 0.92, 1.12), (0.40, 1.10, 0.85, 1.22), (0.80, 1.00, 0.70, 1.08)),
)

# palm: rings across the hand (x, y centre, z centre, half-width, back, palm side)
# In profile the back of the hand runs straight from the wrist to the
# knuckles; the hand is about 3 cm thick at the base of the thumb and 2.4 cm
# at the knuckles, and the ball of the thumb (thenar_solid) bulges on the
# palm side.
PALM_RINGS = ((-0.9, 0.3, -0.1, 2.95, 1.45, 1.85), (0.0, 0.3, 0.0, 3.0, 1.40, 1.72),
              (1.5, 0.25, 0.0, 3.2, 1.32, 1.62), (4.0, 0.15, 0.0, 3.65, 1.22, 1.56),
              (6.5, 0.1, 0.0, 4.0, 1.12, 1.44), (7.6, 0.05, 0.0, 4.15, 1.07, 1.38))
WRIST = (-0.9, 0.3, -0.1)        # centre of the wrist joint
# forearm rings: (distance from the wrist centre toward the elbow, half-width,
# back, front)
FOREARM = ((-0.12, 2.95, 1.45, 1.85), (1.5, 3.0, 1.5, 1.9), (5.0, 3.25, 1.7, 2.05),
           (10.0, 3.6, 2.0, 2.35), (16.0, 3.85, 2.25, 2.55), (24.0, 4.05, 2.4, 2.7),
           (32.0, 4.2, 2.5, 2.8))

# joint ranges (degrees)
RANGE = {"mcp": (0, 90), "pip": (0, 110), "dip": (-20, 80),
         "t_ra": (0, 60), "t_pa": (0, 80), "t_rot": (30, 175), "t_mcp": (-10, 60),
         "t_ip": (-25, 80), "ext": (-70, 85), "dev": (-30, 20)}

# ---------------------------------------------------------------- grips
#
# Finger angles (MCP, PIP, DIP) per finger, the thumb, and the wrist. Figure
# code starts from one of these and overrides what it needs.

RELAXED_THUMB = dict(ra=18, pa=22, rot=125, mcp=18, ip=18)

GRIPS = {
    "relaxed": dict(f=dict(i=(18, 24, 10), m=(22, 30, 12), r=(26, 36, 14), l=(30, 40, 16)),
                    thumb=RELAXED_THUMB, wrist=(12, 0)),
    "flat": dict(f=dict(i=(0, 0, 0, 2), m=(0, 0, 0, 0), r=(0, 0, 0, -1), l=(0, 0, 0, -3)),
                 thumb=dict(ra=40, pa=8, rot=55, mcp=4, ip=4), wrist=(0, 0)),
    "open": dict(f=dict(i=(22, 40, 38), m=(22, 40, 38), r=(24, 42, 38), l=(26, 44, 36)),
                 thumb=RELAXED_THUMB, wrist=(10, 0)),
    "half": dict(f=dict(i=(70, 95, 8), m=(70, 95, 8), r=(70, 95, 10), l=(70, 92, 12)),
                 thumb=RELAXED_THUMB, wrist=(15, 0)),
    "full": dict(f=dict(i=(35, 110, -18), m=(35, 110, -18), r=(35, 106, -16),
                        l=(38, 100, -10)),
                 thumb=RELAXED_THUMB, wrist=(20, 0)),
    "pinch": dict(f=dict(i=(40, 62, 24), m=(42, 64, 24), r=(44, 66, 26), l=(46, 66, 26)),
                  thumb=dict(ra=22, pa=58, rot=145, mcp=10, ip=8), wrist=(10, 0)),
    "sloper": dict(f=dict(i=(10, 22, 20), m=(10, 24, 20), r=(12, 26, 20), l=(14, 28, 20)),
                   thumb=dict(ra=30, pa=30, rot=115, mcp=8, ip=6), wrist=(-5, 0)),
    "pocket": dict(f=dict(i=(55, 85, 45), m=(30, 60, 25), r=(30, 60, 25), l=(25, 30, 15)),
                   thumb=RELAXED_THUMB, wrist=(12, 0)),
    "undercling": dict(f=dict(i=(12, 70, 30), m=(12, 72, 30), r=(14, 72, 30), l=(16, 70, 30)),
                       thumb=dict(ra=30, pa=30, rot=115, mcp=10, ip=10), wrist=(25, 0)),
    "palm": dict(f=dict(i=(0, 6, 2, 4), m=(0, 6, 2, 1), r=(0, 6, 2, -2), l=(0, 6, 2, -6)),
                 thumb=dict(ra=38, pa=12, rot=100, mcp=4, ip=4), wrist=(80, 0)),
    "wrap": dict(f=dict(i=(8, 85, 20), m=(8, 85, 20), r=(10, 85, 20), l=(12, 85, 20)),
                 thumb=dict(ra=45, pa=10, rot=98, mcp=4, ip=4), wrist=(0, 0)),
    "jug": dict(f=dict(i=(35, 70, 35), m=(35, 70, 35), r=(37, 72, 35), l=(40, 72, 35)),
                thumb=RELAXED_THUMB, wrist=(10, 0)),
}


# ---------------------------------------------------------------- geometry helpers


def ring(c, frame, w, d, p, n=24):
    """Cross-section ring centred on c: half-width w across, d toward the
    back and p toward the palm side."""
    A, N, L = frame
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        cs, sn = math.cos(t), math.sin(t)
        h = d if sn >= 0 else p
        pts.append(vadd(c, vadd(vmul(L, w * cs), vmul(N, h * sn))))
    return pts


def hull2(pts):
    """Convex hull of 2D points (counter-clockwise)."""
    P = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))
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


def chaikin(poly, n=2, k=0.22, cut=0.12):
    """Round the corners of a closed polygon by cutting each one at most
    `cut` cm back along its edges, so that where one part's corner pokes out
    of another it doesn't show as a tick in the outline."""
    for _ in range(n):
        if len(poly) < 3:
            return poly
        out = []
        for a, b in zip(poly, poly[1:] + poly[:1]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            t = min(k, cut / L) if L > 0 else k
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            out.append((a[0] + (b[0] - a[0]) * (1 - t), a[1] + (b[1] - a[1]) * (1 - t)))
        poly = out
    return poly


def _area(poly):
    n = len(poly)
    if n < 3:
        return 0.0
    return abs(sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1]
                   for i in range(n))) / 2


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


def nelder_mead(f, x0, step, iters=160):
    n = len(x0)
    pts = [list(x0)] + [[x0[j] + (step[j] if j == i else 0.0) for j in range(n)]
                        for i in range(n)]
    vals = [f(p) for p in pts]
    for _ in range(iters):
        order = sorted(range(n + 1), key=lambda i: vals[i])
        pts = [pts[i] for i in order]
        vals = [vals[i] for i in order]
        c = [sum(p[j] for p in pts[:-1]) / n for j in range(n)]
        xr = [2 * c[j] - pts[-1][j] for j in range(n)]
        fr = f(xr)
        if fr < vals[0]:
            xe = [3 * c[j] - 2 * pts[-1][j] for j in range(n)]
            fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = [0.5 * (c[j] + pts[-1][j]) for j in range(n)]
            fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                for i in range(1, n + 1):
                    pts[i] = [0.5 * (pts[0][j] + pts[i][j]) for j in range(n)]
                    vals[i] = f(pts[i])
    b = min(range(n + 1), key=lambda i: vals[i])
    return pts[b], vals[b]


def _interp(stations, t):
    """Interpolate (w, d, p) at fraction t of a segment."""
    if t <= stations[0][0]:
        return stations[0][1:]
    for a, b in zip(stations, stations[1:]):
        if t <= b[0]:
            k = (t - a[0]) / (b[0] - a[0])
            return tuple(a[i] + (b[i] - a[i]) * k for i in (1, 2, 3))
    return stations[-1][1:]


def _tube(origin, fr, length_, stations, g, cap=None, back=0.12, fwd=0.12):
    """Hulls along one bone: one per pair of cross-sections, each reaching a
    little past its ends so that neighbours overlap (abutting fills leave a
    hairline seam)."""
    A = fr[0]
    rs = [(vadd(origin, vmul(A, length_ * t)), w * g, d * g, p * g)
          for t, w, d, p in stations]
    out = []

    def ext(a, b, s):
        """Ring a moved s cm further from b, its size carried on along the
        piece, so that the overlap doesn't step out of the outline."""
        L = max(vlen(vsub(b[0], a[0])), 1e-6)
        return ring(vadd(a[0], vmul(vsub(a[0], b[0]), s / L)), fr,
                    *[max(x + (x - y) * s / L, 0.03) for x, y in zip(a[1:], b[1:])])
    for i, (a, b) in enumerate(zip(rs, rs[1:])):
        last = i == len(rs) - 2
        pa = ring(vadd(a[0], vmul(A, -back)), fr, *a[1:]) if i == 0 else ext(a, b, 0.12)
        if last:
            pb = ring(vadd(b[0], vmul(A, 0 if cap else fwd)), fr, *b[1:])
        else:
            pb = ext(b, a, 0.12)
        pts = pa + pb
        if last and cap:
            pts += cap
        out.append(pts)
    return out


def penalty(v, lo, hi):
    return (max(0.0, lo - v) + max(0.0, v - hi)) ** 2


# ---------------------------------------------------------------- chains


def finger_chain(f, mcp, pip, dip, splay=0.0):
    """Joint centres and segment frames of finger f in the hand frame."""
    A0 = (math.cos(math.radians(SPLAY[f] + splay)), math.sin(math.radians(SPLAY[f] + splay)), 0.0)
    F0 = frame_of(A0, Z)
    F1 = flexed(F0, mcp)
    F2 = flexed(F1, pip)
    F3 = flexed(F2, dip)
    L1, L2, L3 = SEG[f]
    k = MCP[f]
    p = vadd(k, vmul(F1[0], L1))
    d = vadd(p, vmul(F2[0], L2))
    t = vadd(d, vmul(F3[0], L3 + PAD[f]))
    return dict(name=f, mcp=k, pip=p, dip=d, tip=t, frames=(F0, F1, F2, F3),
                flex=(mcp, pip, dip), lens=(L1, L2, L3 + PAD[f]), bone=L3)


def thumb_chain(ra, pa, rot_, mcp, ip):
    """Joints and frames of the thumb in the hand frame."""
    A = (math.cos(math.radians(pa)) * math.cos(math.radians(ra)),
         math.cos(math.radians(pa)) * math.sin(math.radians(ra)),
         -math.sin(math.radians(pa)))
    N0 = vnorm(vsub(Z, vmul(A, vdot(Z, A))))
    N = spin(N0, A, -rot_)
    F1 = frame_of(A, N)
    F2 = flexed(F1, mcp)
    F3 = flexed(F2, ip)
    L1, L2, L3 = THUMB_SEG
    m = vadd(CMC, vmul(F1[0], L1))
    i = vadd(m, vmul(F2[0], L2))
    t = vadd(i, vmul(F3[0], L3))
    return dict(name="t", cmc=CMC, mcp=m, ip=i, tip=t, frames=(F1, F2, F3),
                flex=(mcp, ip), lens=THUMB_SEG)


# ---------------------------------------------------------------- the hand


class Hand:
    """A posed hand. `grip` names a preset in GRIPS; `fingers` overrides
    finger angles {f: (mcp, pip, dip[, splay])}, `thumb` thumb angles
    (ra, pa, rot, mcp, ip) and `wrist` is (ext, dev)."""

    def __init__(self, grip="relaxed", fingers=None, thumb=None, wrist=None):
        g = GRIPS[grip]
        self.f = {k: tuple(v) + (0.0,) * (4 - len(v)) for k, v in g["f"].items()}
        for k, v in (fingers or {}).items():
            self.f[k] = tuple(v) + (0.0,) * (4 - len(v))
        self.t = dict(g["thumb"])
        self.t.update(thumb or {})
        self.wrist = tuple(wrist if wrist is not None else g["wrist"])

    # chains
    def finger(self, f):
        return finger_chain(f, *self.f[f])

    def thumb(self):
        t = self.t
        return thumb_chain(t["ra"], t["pa"], t["rot"], t["mcp"], t["ip"])

    def warn(self):
        out = []
        for f in FINGERS:
            for v, j in zip(self.f[f][:3], ("mcp", "pip", "dip")):
                lo, hi = RANGE[j]
                if not lo - 0.5 <= v <= hi + 0.5:
                    out.append(f"{NAMES[f]} {j} {v:.0f} outside {lo}..{hi}")
        for j in ("ra", "pa", "rot", "mcp", "ip"):
            lo, hi = RANGE["t_" + j]
            if not lo - 0.5 <= self.t[j] <= hi + 0.5:
                out.append(f"thumb {j} {self.t[j]:.0f} outside {lo}..{hi}")
        for v, j in zip(self.wrist, ("ext", "dev")):
            lo, hi = RANGE[j]
            if not lo - 0.5 <= v <= hi + 0.5:
                out.append(f"wrist {j} {v:.0f} outside {lo}..{hi}")
        return out

    def forearm_frame(self):
        e, d = (math.radians(a) for a in self.wrist)
        u = vnorm((math.cos(e) * math.cos(d), -math.sin(d), -math.sin(e) * math.cos(d)))
        return frame_of(u, Z)

    def view(self, view="thumb", a0=90.0, tilt=0.0, flip=False, at=(0.0, 0.0), front=None,
             stagger=None):
        """Place the hand in a figure (see Posed). In a side view the front
        finger (the index from the thumb side, the little finger from the
        other side) lies exactly in the page, so its segments show their
        true lengths. stagger: how far the fingers behind it step aside (cm,
        one number or three, nearest first; default STAGGER), e.g. 0 for a
        hand seen from above, where they lie hidden under the front one."""
        return Posed(self, view, a0, tilt, flip, at, front, stagger)

    def rest_thumb(self, along=0.4, out=1.2, palm=1.5):
        """Put the thumb in its resting place: alongside the index finger's
        first segment, slightly bent, the tip level with the middle of that
        segment (`along`), `out` cm to its thumb side and `palm` cm toward
        its palm side. For grips that don't use the thumb (tuck_thumb keeps
        it clear of a crimping index finger instead)."""
        ix = self.finger("i")
        A1, N1, L1 = ix["frames"][1]
        T = vadd(vadd(vlerp(ix["mcp"], ix["pip"], along), vmul(L1, out)), vmul(N1, -palm))
        pref = dict(ra=12, pa=25, rot=125, mcp=15, ip=15)
        names = ("ra", "pa", "rot", "mcp", "ip")

        def cost(q):
            t = dict(zip(names, q))
            ch = thumb_chain(t["ra"], t["pa"], t["rot"], t["mcp"], t["ip"])
            e = vlen(vsub(ch["tip"], T)) ** 2
            for n in names:
                e += 30 * penalty(t[n], *RANGE["t_" + n]) + 4e-4 * (t[n] - pref[n]) ** 2
            e += 1e-3 * ((t["mcp"] - 15) ** 2 + (t["ip"] - 15) ** 2)
            return e
        best, bv = None, 1e9
        for ra in (0, 10, 20, 30):
            for pa in (10, 25, 40, 55):
                q0 = [ra, pa, 100 + 0.9 * pa, 15, 15]
                q, v = nelder_mead(cost, q0, [5.0] * 5, iters=300)
                if v < bv:
                    best, bv = q, v
        self.t = dict(zip(names, best))
        return self

    # ------------------------------------------------------------ solids
    def finger_solids(self, f, ch=None, buried=True):
        """Hulls (3D point lists) of finger f: tubes and the middle and end
        joints. The knuckle is separate (knuckle_solid). buried=False leaves
        off the base of the first segment that swells into the palm (for a
        finger drawn behind the hand, where it would show past the palm)."""
        ch = ch or self.finger(f)
        g = GIRTH[f]
        F = ch["frames"]
        J = (ch["mcp"], ch["pip"], ch["dip"])
        out = []
        for k in range(3):
            st = SECTIONS[k]
            if k == 0 and not buried:
                st = ((0.0,) + st[1][1:],) + st[1:]
            Lk = SEG[f][k]
            cap = None
            if k == 2:
                cap = self._cap(J[2], F[3], Lk * st[-1][0], ch["lens"][2],
                                [x * g for x in st[-1][1:]])
            out += _tube(J[k], F[k + 1], Lk, st, g, cap,
                         back=0.4 if k == 0 and buried else 0.12)
        for k in (1, 2):
            w, d, p = (x * g for x in SECTIONS[k][0][1:])
            out.append(self._joint(J[k], F[k], ch["flex"][k], w, d, p))
        return out

    def _cap(self, base, fr, s0, s1, wdp):
        """Rounded fingertip from s0 to s1 along frame fr."""
        w, d, p = wdp
        A, N, L = fr
        pts = []
        for phi in (15, 30, 45, 60, 72, 82, 89):
            ph = math.radians(phi)
            k = math.cos(ph)
            c = vadd(base, vmul(A, s0 + (s1 - s0) * math.sin(ph)))
            c = vadd(c, vmul(N, -(p - d) * 0.45 * math.sin(ph)))
            pts += ring(c, fr, max(w * k, 0.05), max(d * k, 0.03), max(p * k, 0.03), n=16)
        return pts

    def _joint(self, c, fr_in, flex, w, d, p, step=12):
        """A rounded wedge at a joint: the cross-section swept from the
        incoming frame through the flexion angle."""
        n = max(1, int(abs(flex) / step))
        pts = []
        for i in range(n + 1):
            pts += ring(c, flexed(fr_in, flex * i / n), w, d, p, n=20)
        return pts

    def knuckle_solid(self, f, ch=None):
        ch = ch or self.finger(f)
        g = GIRTH[f]
        w, d, p = (x * g for x in KNUCKLE)
        return self._joint(ch["mcp"], ch["frames"][0], ch["flex"][0], w, d, p)

    def root_solid(self, f, ch=None, reach=0.6):
        """The base of finger f where it leaves the palm: one convex shape,
        drawn over the finger's own outline so that it grows out of the
        hand."""
        ch = ch or self.finger(f)
        g = GIRTH[f]
        F1 = ch["frames"][1]
        x, y, z = ch["mcp"]
        F0 = frame_of(X, Z)
        return ring(vadd(ch["mcp"], vmul(F1[0], reach)), F1, 0.96 * g, 0.74 * g, 1.1 * g) + \
            ring((x - 1.6, y, z), F0, 0.96 * g, 1.0 * g, 1.45 * g) + \
            ring((x, y, z), F0, 0.96 * g, 0.98 * g, 1.42 * g)

    def palm_solid(self):
        F0 = frame_of(X, Z)
        pts = []
        for x, y, z, w, d, p in PALM_RINGS:
            pts += ring((x, y, z), F0, w, d, p)
        for f in FINGERS:
            x, y, z = MCP[f]
            g = GIRTH[f]
            pts += ring((x - 0.1, y, z), F0, KNUCKLE[0] * g, KNUCKLE[1] * g, KNUCKLE[2] * g)
        return pts

    def forearm_solid(self, length_=24.0):
        fr = self.forearm_frame()
        u = fr[0]
        pts = []
        for s, w, d, p in FOREARM:
            if s > length_:
                break
            c = vadd(WRIST, vmul(u, -s))
            pts += ring(c, fr, w, d, p)
        return pts

    def wrist_solid(self):
        """The wrist joint: its cross-section swept from the forearm to the
        hand, which rounds the bend."""
        fa = self.forearm_frame()
        fh = frame_of(X, Z)
        pts = []
        for i in range(7):
            t = i / 6
            fr = frame_of(vlerp(fa[0], fh[0], t), vlerp(fa[1], fh[1], t))
            pts += ring(WRIST, fr, 2.95, 1.45, 1.85)
        return pts

    def thenar_solid(self, th=None):
        th = th or self.thumb()
        F1 = th["frames"][0]
        F0 = frame_of(X, Z)
        pts = ring((1.3, 1.5, -0.9), F0, 1.55, 0.6, 1.05) + \
            ring((4.3, 1.75, -0.9), F0, 1.4, 0.5, 0.8)
        mid = (3.5, 0.6, -1.2)
        for s, k, w, d, p in ((0.6, 0.55, 1.25, 0.9, 1.3), (2.0, 0.6, 1.3, 0.92, 1.32),
                              (3.4, 0.3, 1.15, 0.86, 1.1)):
            c = vadd(CMC, vmul(F1[0], s))
            c = vadd(c, vmul(vnorm(vsub(mid, c)), k))
            pts += ring(c, F1, w, d, p)
        return pts

    def thumb_solids(self, th=None):
        th = th or self.thumb()
        F = th["frames"]
        J = (th["cmc"], th["mcp"], th["ip"])
        out = []
        for k in range(3):
            st = THUMB_SECTIONS[k]
            Lk = THUMB_SEG[k]
            cap = self._cap(J[2], F[2], Lk * st[-1][0], Lk, st[-1][1:]) if k == 2 else None
            out += _tube(J[k], F[k], Lk, st, 1.0, cap)
        for k in (1, 2):
            w, d, p = THUMB_SECTIONS[k][0][1:]
            out.append(self._joint(J[k], F[k - 1], th["flex"][k - 1], w, d, p))
        return out

    def thumb_web(self, th=None):
        """The skin between the thumb and the index finger: a polygon whose
        free edge sags toward the wrist."""
        th = th or self.thumb()
        ix = self.finger("i")
        F2 = th["frames"][1]
        a = vadd(th["mcp"], vmul(F2[0], 1.0))
        tw = vnorm(vsub(ix["mcp"], a))
        tw = vnorm(vsub(tw, vmul(F2[0], vdot(tw, F2[0]))))
        T1 = vadd(a, vmul(tw, 0.85))
        F1 = ix["frames"][1]
        I1 = vadd(vadd(ix["mcp"], vmul(F1[0], 0.6)), vmul(F1[2], 0.85))
        m = vlerp(T1, I1, 0.5)
        ctrl = vlerp(m, CMC, 0.3)
        edge = [vadd(vmul(T1, (1 - s) ** 2), vadd(vmul(ctrl, 2 * s * (1 - s)), vmul(I1, s * s)))
                for s in (i / 8 for i in range(9))]
        return [vlerp(CMC, th["mcp"], 0.4), th["mcp"]] + edge + [ix["mcp"], (5.0, 2.2, -0.3)]

    def finger_web(self, a, b):
        ca, cb = self.finger(a), self.finger(b)
        sa = 1 if MCP[b][1] > MCP[a][1] else -1
        ga, gb = GIRTH[a], GIRTH[b]
        Fa, Fb = ca["frames"][1], cb["frames"][1]
        return [vadd(ca["mcp"], vmul(Fa[2], sa * 0.9 * ga)),
                vadd(vadd(ca["mcp"], vmul(Fa[0], 1.25)), vmul(Fa[2], sa * 0.92 * ga)),
                vadd(vadd(cb["mcp"], vmul(Fb[0], 1.25)), vmul(Fb[2], -sa * 0.92 * gb)),
                vadd(cb["mcp"], vmul(Fb[2], -sa * 0.9 * gb))]

    # ------------------------------------------------------------ surface marks
    def nail(self, f, ch=None):
        """Outline of a fingernail (or the thumbnail, f="t") as 3D points with
        surface normals."""
        if f == "t":
            ch = ch or self.thumb()
            fr, base, L3 = ch["frames"][2], ch["ip"], THUMB_SEG[2]
            st = THUMB_SECTIONS[2]
            s0, s1, half = 0.42 * L3, L3 - 0.16, 55
            g = 1.0
        else:
            ch = ch or self.finger(f)
            fr, base, L3 = ch["frames"][3], ch["dip"], ch["bone"]
            st = SECTIONS[2]
            s0, s1, half = 0.42 * ch["bone"], ch["lens"][2] - 0.15, 52
            g = GIRTH[f]
            L3 = ch["lens"][2]
        A, N, L = fr
        bone = SEG[f][2] if f != "t" else THUMB_SEG[2] * 0.8

        def surf(s, th):
            t = min(s / bone, st[-1][0])
            w, d, p = _interp(st, t)
            w, d = w * g, d * g
            if s > bone * st[-1][0]:
                ph = (s - bone * st[-1][0]) / max(L3 - bone * st[-1][0], 0.01)
                k = math.cos(math.asin(min(ph, 0.98)))
                w, d = w * k, d * k
            c = vadd(base, vmul(A, s))
            a = math.radians(th)
            pt = vadd(c, vadd(vmul(L, w * math.sin(a)), vmul(N, d * math.cos(a) * 1.02)))
            nrm = vnorm(vadd(vmul(L, math.sin(a) / max(w, 0.05)),
                             vmul(N, math.cos(a) / max(d, 0.05))))
            return pt, nrm
        loop = []
        for i in range(9):                      # cuticle, curving toward the wrist
            th = -half + 2 * half * i / 8
            loop.append(surf(s0 - 0.13 * math.cos(math.radians(th / half * 90)), th))
        for i in range(1, 7):                    # side
            loop.append(surf(s0 + (s1 - s0) * i / 6, half))
        for i in range(1, 8):                    # free edge
            th = half - 2 * half * i / 8
            loop.append(surf(s1 + 0.05 * math.cos(math.radians(th / half * 90)), th))
        for i in range(0, 7):                    # other side
            loop.append(surf(s1 - (s1 - s0) * i / 6, -half))
        return loop

    def creases(self, f, ch=None):
        """Short creases on the bent side of the middle and end joints (or
        the thumb's end joint): pairs of 3D points."""
        out = []
        if f == "t":
            ch = ch or self.thumb()
            items = [(ch["ip"], ch["frames"][1], ch["frames"][2], ch["flex"][1],
                      THUMB_SECTIONS[2][0][1:])]
        else:
            ch = ch or self.finger(f)
            F = ch["frames"]
            g = GIRTH[f]
            items = [(ch["pip"], F[1], F[2], ch["flex"][1],
                      [x * g for x in SECTIONS[1][0][1:]]),
                     (ch["dip"], F[2], F[3], ch["flex"][2],
                      [x * g for x in SECTIONS[2][0][1:]])]
        for c, fa, fb, fl, (w, d, p) in items:
            if fl > 18:
                b = vnorm(vadd(fa[1], fb[1]))
                out.append((vadd(c, vmul(b, -p * 0.45)), vadd(c, vmul(b, -p * 0.98))))
            elif fl < -8:
                b = vnorm(vadd(fa[1], fb[1]))
                out.append((vadd(c, vmul(b, d * 0.4)), vadd(c, vmul(b, d * 0.98))))
        return out

    def wrinkles(self, f, ch=None):
        """A short arc across the back of the middle and end joints of a
        fairly straight finger (seen from the back), as 3D points with
        normals."""
        ch = ch or self.finger(f)
        F = ch["frames"]
        g = GIRTH[f]
        out = []
        for j, k, half in (("pip", 1, 38), ("dip", 2, 30)):
            if ch["flex"][k] > 35:
                continue
            w, d, p = (x * g for x in SECTIONS[k][0][1:])
            A, N, L = F[k + 1]
            arc = []
            for i in range(7):
                a = math.radians(-half + 2 * half * i / 6)
                pt = vadd(ch[j], vadd(vmul(L, w * 0.98 * math.sin(a)),
                                      vmul(N, d * 1.03 * math.cos(a))))
                pt = vadd(pt, vmul(A, 0.1 * math.cos(a) - 0.05))
                arc.append((pt, vnorm(vadd(vmul(L, math.sin(a) / w),
                                           vmul(N, math.cos(a) / d)))))
            out.append(arc)
        return out

    def knuckle_arc(self, f, ch=None):
        """A short arc over the knuckle (the head of the metacarpal) of a
        bent finger, where it stands out on the back of the hand, as 3D
        points with normals; [] for a fairly straight finger."""
        ch = ch or self.finger(f)
        flex = ch["flex"][0]
        if flex < 25:
            return []
        g = GIRTH[f]
        w, d = KNUCKLE[0] * g, KNUCKLE[1] * g
        A, N, L = flexed(ch["frames"][0], flex * 0.55)
        arc = []
        for i in range(7):
            a = math.radians(-40 + 80 * i / 6)
            pt = vadd(ch["mcp"], vadd(vmul(L, w * 0.85 * math.sin(a)),
                                      vmul(N, d * 1.01 * math.cos(a))))
            arc.append((pt, vnorm(vadd(vmul(L, math.sin(a) / w), vmul(N, math.cos(a) / d)))))
        return [arc]


# ---------------------------------------------------------------- views

BASE = {  # images of the hand's x, y, z axes for a hand pointing up the page
    "thumb": ((0, 1, 0), (0, 0, 1), (-1, 0, 0)),
    "little": ((0, 1, 0), (0, 0, -1), (-1, 0, 0)),
    "back": ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    "palm": ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
}
TILT_SIGN = {"thumb": -1, "little": 1, "back": 1, "palm": -1}


def _apply(M, p):
    return vsum(vmul(M[0], p[0]), vmul(M[1], p[1]), vmul(M[2], p[2]))


def _compose(A, B):
    return tuple(_apply(A, c) for c in B)


class Shape(list):
    """A projected outline that remembers its mean depth."""


# what Posed.draw measured, for tools/check_hands.py; CONTEXT[0] names the
# figure being drawn
RECORD = []
CONTEXT = [""]
# In a true side view the fingers behind the front one hide almost exactly
# behind it. Each is drawn shifted on the page by STAGGER cm (nearest
# first) along SHEAR_DIR, a direction in the hand frame (toward the
# fingertips, toward the back of the hand), so that its own knuckles and
# tip step out from behind the front finger, which keeps its true lengths.
# Everything that reads or solves a finger (joint, angle, surface, reach,
# on_edge, place) uses the same shift, so the pads still land on the hold
# as drawn.
STAGGER = (0.35, 0.65, 0.9)
SHEAR_DIR = (1.0, -0.3)
# their fills, nearest first: the middle finger almost white, the others grey
BACK_TONES = (PALE, LIGHT, LIGHT)


def _extent(polys, m, n):
    """Length of the line through m along n covered by the polygons that the
    line crosses at m (a drawn thickness)."""
    lo = hi = None
    for P in polys:
        ss = []
        k = len(P)
        for i in range(k):
            a, b = P[i], P[(i + 1) % k]
            d = (b[0] - a[0], b[1] - a[1])
            den = -n[0] * d[1] + n[1] * d[0]
            if abs(den) < 1e-12:
                continue
            r = (a[0] - m[0], a[1] - m[1])
            s = (-r[0] * d[1] + r[1] * d[0]) / den
            t = (n[0] * r[1] - n[1] * r[0]) / den
            if 0 <= t <= 1:
                ss.append(s)
        if len(ss) >= 2 and min(ss) <= 1e-9 <= max(ss) + 2e-9:
            lo = min(ss) if lo is None else min(lo, min(ss))
            hi = max(ss) if hi is None else max(hi, max(ss))
    return (hi - lo) if lo is not None else 0.0


class Posed:
    """A hand placed in a figure: hand-frame points map to the page."""

    def __init__(self, hand, view, a0, tilt, flip, at=(0.0, 0.0), front=None, stagger=None):
        self.hand = hand
        self.kind = view
        self.a0, self.tilt, self.flip = a0, tilt, flip
        self.front = front or ("l" if view == "little" else "i")
        # how far the fingers behind the front one step aside, nearest first
        self.stagger = STAGGER if stagger is None else (
            (stagger,) * 3 if isinstance(stagger, (int, float)) else tuple(stagger))
        self.T = (at[0], at[1], 0.0)
        self._mat()

    def _mat(self):
        a = math.radians(TILT_SIGN[self.kind] * self.tilt)
        Rx = ((1, 0, 0), (0, math.cos(a), math.sin(a)), (0, -math.sin(a), math.cos(a)))
        B = BASE[self.kind]
        if self.flip:
            B = tuple((-c[0], c[1], c[2]) for c in B)
        r = math.radians(self.a0 - 90)
        Rz = ((math.cos(r), math.sin(r), 0), (-math.sin(r), math.cos(r), 0), (0, 0, 1))
        S = (X, Y, Z)
        if self.kind in ("thumb", "little"):
            # turn the hand about its back-to-palm axis so that the front
            # finger's plane of bending is the page: no foreshortening
            s = -math.radians(SPLAY[self.front] + self.hand.f[self.front][3])
            S = ((math.cos(s), math.sin(s), 0.0), (-math.sin(s), math.cos(s), 0.0), Z)
        self.R = _compose(Rz, _compose(B, _compose(Rx, S)))
        # direction toward the viewer, in the hand frame
        self.eye = (self.R[0][2], self.R[1][2], self.R[2][2])
        self.sdir = None        # the page direction of STAGGER in a side view
        if self.kind in ("thumb", "little"):
            v = _apply(self.R, vadd(vmul(X, SHEAR_DIR[0]), vmul(Z, SHEAR_DIR[1])))
            self.sdir = norm((v[0], v[1]))

    def _off(self, f):
        """The page offset of finger f behind the front one (STAGGER)."""
        if not self.sdir or f is None or f == "t" or f == self.front:
            return 0.0
        near = [g for g in (FINGERS if self.kind == "thumb" else FINGERS[::-1])
                if g != self.front]
        return self.stagger[near.index(f)]

    def p3(self, p, f=None):
        """Page point (x, y, depth) of hand point p; f names the finger it
        belongs to, since the fingers behind the front one are drawn a
        little apart (STAGGER)."""
        q = _apply(self.R, p)
        s = self._off(f)
        if s:
            q = (q[0] + self.sdir[0] * s, q[1] + self.sdir[1] * s, q[2])
        return vadd(q, self.T)

    def xy(self, p, f=None):
        q = self.p3(p, f)
        return (q[0], q[1])

    def depth(self, p):
        return self.p3(p)[2]

    # -- placing
    def move_point(self, p, to, f=None):
        """Translate so that hand point p (of finger f) lands on page point
        `to`."""
        q = self.xy(p, f)
        self.T = (self.T[0] + to[0] - q[0], self.T[1] + to[1] - q[1], self.T[2])
        return self

    def place(self, f="i", at=(0.0, 0.0), distal=None, a0=None, k=0.8):
        """Put the pad of finger f (fraction k along its last segment) on page
        point `at`, either turning the hand so that the last segment points
        along page direction `distal` (degrees) or with the hand at `a0`."""
        if a0 is not None:
            self.a0 = a0
            self._mat()
        elif distal is not None:
            ch = self.hand.finger(f) if f != "t" else None
            sgn = -1 if self.flip else 1
            self.a0 = distal + sgn * sum(ch["flex"]) if ch else distal
            for _ in range(6):
                self._mat()
                d = self.angle(f, 3)
                err = (distal - d + 180) % 360 - 180
                self.a0 += err
                if abs(err) < 0.05:
                    break
            self._mat()
        return self.move_point(pad_point(self.hand, f, k), at, f)

    # -- reading points back
    def joint(self, f, j):
        ch = self.hand.thumb() if f == "t" else self.hand.finger(f)
        return self.xy(ch[j], f)

    def angle(self, f, k):
        """Page direction (degrees) of segment k of finger f (0 the palm,
        1-3 the bones); for the thumb, 0-2."""
        if f == "t":
            ch = self.hand.thumb()
            pts = (ch["cmc"], ch["mcp"], ch["ip"], ch["tip"])
            a, b = pts[k], pts[k + 1]
        else:
            ch = self.hand.finger(f)
            if k == 0:
                a, b = vsub(ch["mcp"], ch["frames"][0][0]), ch["mcp"]
            else:
                pts = (ch["mcp"], ch["pip"], ch["dip"], ch["tip"])
                a, b = pts[k - 1], pts[k]
        v = sub(self.xy(b, f), self.xy(a, f))
        return math.degrees(math.atan2(v[1], v[0]))

    def surface(self, f, j, side="palm", k=0.95):
        """A page point on the palm side (or the back) of joint j of finger f."""
        ch = self.hand.thumb() if f == "t" else self.hand.finger(f)
        F = ch["frames"]
        if f == "t":
            i = ("cmc", "mcp", "ip", "tip").index(j)
            fa, fb = F[max(i - 1, 0)], F[min(i, 2)]
        else:
            i = ("mcp", "pip", "dip", "tip").index(j)
            fa, fb = F[i], F[min(i + 1, 3)]
        n = vnorm(vadd(fa[1], fb[1]))
        g = 1.0 if f == "t" else GIRTH[f]
        h = (0.8 if side == "palm" else 0.62) * g
        sgn = -1 if side == "palm" else 1
        return self.xy(vadd(ch[j], vmul(n, sgn * h * k)), f)

    def at(self, x, y, z=0.0):
        """Page point of a hand-frame point."""
        return self.xy((x, y, z))

    # -- solving
    def reach(self, f, target, dip=None, k=0.8, lock=None):
        """Bend finger f (its knuckle and middle joint) so that its pad lands
        on page point `target`; dip fixes the end joint, else the current
        one. lock=(lo, hi) limits the middle joint. Returns the miss in cm."""
        mcp0, pip0, dip0, spl = self.hand.f[f]
        dip = dip0 if dip is None else dip
        lo, hi = lock or RANGE["pip"]

        def cost(q):
            m, p = q
            pt = self.xy(pad_point(None, f, k, finger_chain(f, m, p, dip, spl)), f)
            e = (pt[0] - target[0]) ** 2 + (pt[1] - target[1]) ** 2
            return e + 4 * (penalty(m, *RANGE["mcp"]) + penalty(p, lo, hi)) + \
                1e-5 * ((m - mcp0) ** 2 + (p - pip0) ** 2)
        best, v = None, 1e9
        for m0, p0 in ((mcp0, pip0), (mcp0 + 20, pip0 - 20), (mcp0 - 15, pip0 + 15)):
            q, val = nelder_mead(cost, [m0, p0], [8.0, 8.0], iters=200)
            if val < v:
                best, v = q, val
        m, p = best
        m = min(max(m, RANGE["mcp"][0]), RANGE["mcp"][1])
        p = min(max(p, lo), hi)
        self.hand.f[f] = (m, p, dip, spl)
        pt = self.xy(pad_point(self.hand, f, k), f)
        return length(sub(pt, target))

    def thumb_to(self, target, part="pad", depth=None, keep=(), k=0.65, prefer=None,
                 weight=1.0, facing=None):
        """Move the thumb so that its pad (fraction k along the last
        segment), tip or nail lands on page point `target`, in a natural
        pose close to its current one. depth: the wanted depth of that point
        (toward the viewer), or None. facing: a page direction (degrees) the
        pad should face, e.g. into the face it presses. Returns the miss in
        cm."""
        fv = ang(facing) if facing is not None else None
        t0 = dict(self.hand.t)
        pref = dict(t0, **(prefer or {}))
        names = [n for n in ("ra", "pa", "rot", "mcp", "ip") if n not in keep]

        def setq(q):
            t = dict(t0)
            for n, v in zip(names, q):
                t[n] = v
            return t

        def cost(q):
            t = setq(q)
            ch = thumb_chain(t["ra"], t["pa"], t["rot"], t["mcp"], t["ip"])
            p3 = thumb_point(ch, part, k)
            pt = self.xy(p3)
            e = (pt[0] - target[0]) ** 2 + (pt[1] - target[1]) ** 2
            if depth is not None:
                e += 0.5 * (self.depth(p3) - depth) ** 2
            if fv is not None:
                pn = _apply(self.R, vmul(ch["frames"][2][1], -1))
                q = norm((pn[0], pn[1]))
                e += 3.0 * (1 - (q[0] * fv[0] + q[1] * fv[1])) + 2.0 * pn[2] ** 2
            for n in names:
                e += 30 * penalty(t[n], *RANGE["t_" + n])
                e += weight * 1.5e-4 * (t[n] - pref[n]) ** 2
            # the thumb pad turns toward the fingers as the thumb comes forward
            e += weight * 1e-4 * (t["rot"] - (100 + 0.9 * t["pa"])) ** 2
            # its joints rarely bend backward under load
            e += weight * 3e-4 * (min(t["mcp"], 0) ** 2 + min(t["ip"], 0) ** 2)
            return e
        # a coarse search over natural poses, then refine the best few
        cands = []
        for ra in range(0, 61, 10):
            for pa in range(0, 81, 10):
                for mcp in range(-10, 61, 10):
                    for ip in range(-20, 81, 20):
                        s = dict(t0, ra=ra, pa=pa, mcp=mcp, ip=ip, rot=100 + 0.9 * pa)
                        q = [s[n] for n in names]
                        cands.append((cost(q), q))
        cands.sort(key=lambda c: c[0])
        best, bv = None, 1e9
        for _, q0 in cands[:4] + [(0, [t0[n] for n in names])]:
            q, _ = nelder_mead(cost, q0, [6.0] * len(names), iters=400)
            q, v = nelder_mead(cost, q, [2.0] * len(names), iters=300)
            if v < bv:
                best, bv = q, v
        self.hand.t = setq(best)
        ch = self.hand.thumb()
        return length(sub(self.xy(thumb_point(ch, part, k)), target))

    # -- drawing
    def draw(self, fig, z=0.0, front=None, fill=WHITE, back_fill=LIGHT, ghost=False,
             thumb_front=None, details=True, forearm=32.0, hide=(), others="copy"):
        """Draw the hand, always with its thumb. front: the finger drawn in
        front in a side view (default the view's front finger). others, in
        a side view: which fingers to draw behind it, each as its own
        finger with its own outline, nails and creases, the nearest almost
        white and the others grey (BACK_TONES, or back_fill if given):
        "copy" or "all" (the default) all of them, "none" none, or a string
        of finger names (a pocket, where the finger in the hole is the
        subject). thumb_front: in a back or palm
        view, whether the thumb lies in front of the palm (default: decided
        from its depth). hide: fingers not to draw (back and palm views)."""
        h = self.hand
        chains = {f: h.finger(f) for f in FINGERS}
        th = h.thumb()
        P = self._proj
        st = dict(stroke=INK, dash=None)
        sw_out, sw_back, sw_fine = OUTLINE, BACK_SW, FINE
        if ghost:
            st = dict(stroke=MID, dash=(0.9, 0.7))
            sw_out = sw_back = sw_fine = 0.3
            details = False
        main = [P(h.palm_solid())]
        if forearm:
            main += [P(h.forearm_solid(forearm)), P(h.wrist_solid())]
        tsol_all = h.thumb_solids(th)
        meta = [P(s) for s in tsol_all[:1]]          # the metacarpal, inside the hand
        main += [P(h.thenar_solid(th)), self._poly(h.thumb_web(th))] + meta
        tmask = [P(h.thenar_solid(th))] + meta
        tsol = [P(s) for s in tsol_all[1:]]
        layers = []
        thumb_layer = None
        kind = self.kind

        def layer(polys, fill_, sw, masks=(), marks=None, nails=()):
            layers.append((polys, fill_, sw, masks, marks, nails))
            return len(layers) - 1

        if kind in ("thumb", "little"):
            front = front or self.front
            main.append(P(h.knuckle_solid(front, chains[front])))
            if kind == "little":
                thumb_layer = layer(tsol, back_fill, sw_back)
            # the fingers behind the front one, nearest first, each its own
            # finger, drawn from the farthest
            near = [f for f in (FINGERS if kind == "thumb" else FINGERS[::-1]) if f != front]
            if others in ("copy", "all"):
                behind = near
            elif others == "none":
                behind = []
            else:
                behind = [f for f in near if f in others]
            tones = {f: (back_fill if back_fill != LIGHT else BACK_TONES[min(i, 2)])
                     for i, f in enumerate(behind)}
            self._behind = {}
            for f in behind[::-1]:
                self._behind[f] = layer([P(h.root_solid(f, chains[f]), f)] +
                                        [P(s, f) for s in
                                         h.finger_solids(f, chains[f], buried=False)],
                                        tones[f], sw_back, marks=f,
                                        nails=[f] if details else ())
            layer(main, fill, sw_out)
            front_layer = layer([P(s) for s in h.finger_solids(front, chains[front])], fill,
                                sw_out, masks=[P(h.root_solid(front, chains[front]))],
                                marks=front, nails=[front] if details else ())
            if kind == "thumb":
                thumb_layer = layer(tsol, fill, sw_out, masks=tmask, marks="t",
                                    nails=["t"] if details else ())
        else:
            for f in FINGERS:
                if f not in hide:
                    main.append(P(h.knuckle_solid(f, chains[f])))
            if thumb_front is None:
                tip_d = vdot(vsub(th["tip"], (5.0, 1.0, 0.0)), self.eye)
                thumb_front = tip_d > -0.3
            if not thumb_front:
                thumb_layer = layer(tsol, fill, sw_out, nails=["t"] if details else ())
            fingers = [f for f in FINGERS if f not in hide]
            allf = []
            for f in fingers:
                allf += [P(s) for s in h.finger_solids(f, chains[f])]
            webs = [self._poly(h.finger_web(a, b)) for a, b in (("i", "m"), ("m", "r"), ("r", "l"))
                    if a not in hide and b not in hide]
            layer(main + allf + webs, fill, sw_out)
            mask = webs + [P(h.knuckle_solid(f, chains[f])) for f in fingers]
            if kind == "back":
                mask = [P(h.palm_solid())] + mask
            else:
                band = []
                F0 = frame_of(X, Z)
                for f in fingers:
                    x, y, zc = MCP[f]
                    band += ring((x - 1.6, y, zc), F0, 1.05, 1.05, 1.5) + \
                        ring((x + 0.2, y, zc), F0, 1.0, 1.0, 1.45)
                mask += [P(band)] + [P(h.root_solid(f, chains[f])) for f in fingers]
            if not ghost:
                dep = {f: vdot(chains[f]["pip"], self.eye) for f in fingers}
                for f in sorted(fingers, key=lambda f: dep[f]):
                    layer([P(s) for s in h.finger_solids(f, chains[f])], fill, sw_fine,
                          masks=mask, marks=f if kind == "back" else None,
                          nails=[f] if details else ())
            if thumb_front:
                thumb_layer = layer(tsol, fill, sw_out, masks=tmask,
                                    nails=["t"] if details else ())
        self._record(layers, thumb_layer, th, chains, front if kind in ("thumb", "little")
                     else None, front_layer if kind in ("thumb", "little") else None, ghost)
        for i, (polys, fill_, sw, masks, marks, nails) in enumerate(layers):
            polys = [q for q in polys if _area(q) > 0.01]
            masks = [q for q in masks if _area(q) > 0.01]
            zl = z + i * 0.01
            for q in polys:
                fig.poly(q, z=zl, fill=fill_, stroke=st["stroke"], sw=sw * 2, dash=st["dash"])
            for q in masks:
                fig.poly(q, z=zl + 0.003, fill=fill_, stroke=None)
            for q in polys:
                fig.poly(q, z=zl + 0.006, fill=fill_, stroke=None)
            if not details:
                continue
            self._occ = [(q, q.dep) for q in polys if hasattr(q, "dep")]
            for f in nails:
                loop = h.nail(f, th if f == "t" else chains[f])
                # the part of the nail turned toward you: seen from the side,
                # a line just inside the back of the fingertip
                vis = [self.xy(p, f) for p, n in loop if vdot(n, self.eye) > 0.2]
                if len(vis) > 4 and _area(hull2(vis)) > 0.1:
                    self._mark_run(fig, loop + loop[:1], zl + 0.008, f)
            if marks and kind in ("thumb", "little"):
                for a, b in h.creases(marks, th if marks == "t" else chains[marks]):
                    fr = (th["frames"][1] if marks == "t" else chains[marks]["frames"][1])
                    if abs(vdot(fr[2], self.eye)) > 0.55:
                        fig.line(self.xy(a, marks), self.xy(b, marks), z=zl + 0.008,
                                 sw=DETAIL)
            if marks and kind == "back":
                for arc in h.wrinkles(marks, chains[marks]):
                    self._mark_run(fig, arc, zl + 0.008, marks)
        if details and kind == "back" and not ghost:
            # knuckle arcs go on after every finger (whose layers mask the
            # back of the hand) but under a thumb that lies in front
            n = len(layers) - (1 if thumb_front else 0)
            self._occ = [(q, q.dep) for L in layers[:n] for q in L[0] if hasattr(q, "dep")]
            for f in fingers:
                for arc in h.knuckle_arc(f, chains[f]):
                    self._mark_run(fig, arc, z + n * 0.01 - 0.001)

    def _record(self, layers, thumb_layer, th, chains, front, front_layer, ghost):
        """Measure what is drawn, for tools/check_hands.py: the front
        finger's segment lengths and thickness in a side view, and how much
        of the thumb shows."""
        rec = dict(context=CONTEXT[0], view=self.kind, ghost=ghost)
        # the thumb: points along its two visible segments, hidden if inside
        # anything drawn after (nearer than) it
        pts = [vlerp(th["mcp"], th["ip"], t) for t in (0.3, 0.6, 0.9)] + \
            [vlerp(th["ip"], th["tip"], t) for t in (0.2, 0.5, 0.8)]
        nearer = [q for L in layers[thumb_layer + 1:] for q in L[0]] if thumb_layer is not None else []
        vis = [not any(inside(self.xy(p), q) for q in nearer) for p in pts]
        rec["thumb"] = sum(vis) / len(vis) if thumb_layer is not None else 0.0
        if front:
            ch = chains[front]
            A3 = ch["frames"][3][0]
            J = [ch["mcp"], ch["pip"], ch["dip"], vadd(ch["dip"], vmul(A3, SEG[front][2]))]
            rec["front"] = front
            rec["lengths"] = [length(sub(self.xy(J[i + 1]), self.xy(J[i]))) for i in range(3)]
            polys = layers[front_layer][0]
            th_ = []
            for i in range(3):
                m = self.xy(vlerp(J[i], J[i + 1], 0.5))
                n = perp(norm(sub(self.xy(J[i + 1]), self.xy(J[i]))))
                th_.append(_extent(polys, m, n))
            rec["thickness"] = th_
            if thumb_layer is not None and thumb_layer > front_layer:
                tp = layers[thumb_layer][0]
                axis = [vlerp(J[0], J[1], t) for t in (0.4, 0.7, 1.0)] + \
                    [vlerp(J[1], J[2], t) for t in (0.33, 0.67, 1.0)] + \
                    [vlerp(J[2], ch["tip"], t) for t in (0.33, 0.67, 0.9)]
                hid = [any(inside(self.xy(p), q) for q in tp) for p in axis]
                rec["hidden"] = sum(hid) / len(hid)
            ax = norm(sub(self.at(8.0, 0.5, 0.0), self.at(0.0, 0.5, 0.0)))
            pp = [self._proj(self.hand.palm_solid())]
            rec["palm"] = [_extent(pp, self.at(x, 0.5, 0.0), perp(ax)) for x in (3.0, 8.6)]
            # how much of each finger behind the front one shows: the share
            # of points just inside its outline that no nearer layer covers
            rec["behind"] = {}
            for f, i in getattr(self, "_behind", {}).items():
                nearer = [q for L in layers[i + 1:] for q in L[0]]
                pts = []
                for q in layers[i][0]:
                    c = (sum(x for x, _ in q) / len(q), sum(y for _, y in q) / len(q))
                    pts += [add(v, mul(norm(sub(c, v)), 0.12)) for v in q[::3]]
                vis = [not any(inside(v, q) for q in nearer) for v in pts]
                rec["behind"][f] = sum(vis) / max(len(vis), 1)
        RECORD.append(rec)

    def _proj(self, pts, f=None):
        s = Shape(chaikin(hull2([self.xy(p, f) for p in pts])))
        s.dep = sum(self.depth(p) for p in pts) / len(pts)
        return s

    def _poly(self, pts):
        return [self.xy(p) for p in pts]

    def _visible(self, p, nrm, occluders, f=None):
        if vdot(nrm, self.eye) < 0.2:
            return False
        q = self.xy(p, f)
        d = self.depth(p)
        for poly, dep in occluders:
            if dep > d + 0.25 and inside(q, poly):
                return False
        return True

    def _mark_run(self, fig, pts, z, f=None):
        occ = getattr(self, "_occ", [])
        run = []
        for p, n in pts:
            if self._visible(p, n, occ, f):
                run.append(self.xy(p, f))
            else:
                if len(run) > 1:
                    fig.poly(run, closed=False, z=z, sw=DETAIL, fill=None)
                run = []
        if len(run) > 1:
            fig.poly(run, closed=False, z=z, sw=DETAIL, fill=None)


def pad_point(hand, f, k=0.8, ch=None):
    """The palm-side surface of finger f's last segment, fraction k of the
    way from the end joint to the fingertip: where it touches a hold."""
    if f == "t":
        return thumb_point(ch or hand.thumb(), "pad", k)
    ch = ch or hand.finger(f)
    A, N, L = ch["frames"][3]
    s = ch["lens"][2] * k
    t = min(s / SEG[f][2], SECTIONS[2][-1][0])
    w, d, p = _interp(SECTIONS[2], t)
    p *= GIRTH[f]
    if s > SEG[f][2] * SECTIONS[2][-1][0]:
        ph = (s - SEG[f][2] * SECTIONS[2][-1][0]) / (ch["lens"][2] - SEG[f][2] * SECTIONS[2][-1][0])
        p *= math.cos(math.asin(min(ph, 0.98)))
    return vadd(vadd(ch["dip"], vmul(A, s)), vmul(N, -p))


def thumb_point(ch, part="pad", k=0.65):
    """A point of the thumb: its pad (fraction k along the last segment),
    its tip, or its nail."""
    A, N, L = ch["frames"][2]
    L3 = THUMB_SEG[2]
    if part == "tip":
        return ch["tip"]
    w, d, p = _interp(THUMB_SECTIONS[2], min(k, 0.8))
    if part == "nail":
        return vadd(vadd(ch["ip"], vmul(A, L3 * k)), vmul(N, d))
    return vadd(vadd(ch["ip"], vmul(A, L3 * k)), vmul(N, -p))


# ---------------------------------------------------------------- annotation


def flex_arc(f, joint, a_in, a_out, r, label=None, at=None, size=7, z=40, ext=None):
    """Mark a joint's flexion Kettle-style: a dashed continuation of the
    incoming segment (where the finger would point if the joint were
    straight) and an arc from it to the outgoing segment."""
    while a_out - a_in > 180:
        a_out -= 360
    while a_in - a_out > 180:
        a_out += 360
    e = ext if ext is not None else r + f.mm(1.6)
    end = add(joint, mul(ang(a_in), e))
    n = 16
    pts = [add(joint, mul(ang(a_in + (a_out - a_in) * i / n), r)) for i in range(n + 1)]
    f.line(joint, end, z=z, sw=0.6, stroke=WHITE)
    f.poly(pts, closed=False, z=z, sw=0.75, stroke=WHITE)
    f.line(joint, end, z=z + 0.1, sw=0.28, dash=(0.8, 0.5))
    f.poly(pts, closed=False, z=z + 0.1, sw=0.32, stroke=INK)
    if label:
        p = at or add(joint, mul(ang(a_in), e + f.mm(2.2)))
        f.text(label, p, size=size, z=z + 1)


def joint_arc(fig, posed, f, j, r=2.1, label=None, at=None, **kw):
    """flex_arc on joint j ("pip", "dip" or "mcp") of finger f."""
    k = {"mcp": 1, "pip": 2, "dip": 3}[j]
    flex_arc(fig, posed.joint(f, j), posed.angle(f, k - 1), posed.angle(f, k), r,
             label, at=at, **kw)


# ---------------------------------------------------------------- close-up scenery
#
# Side profiles have the wall on the right with its face at x = WX, as in the
# climber side views.

WX = 2.0


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


def edge_profile(f, wx, top, depth=2.0, height=2.6, slope=0.0, round_r=0.35, z=-5):
    """An edge sticking out of a wall face at x=wx, seen from the side.
    `slope` tilts the top (degrees): positive slopes down and away from the
    wall, negative is incut. Returns the front corner of the top."""
    t = math.tan(math.radians(slope))
    front_top = (wx - depth, top - depth * t)
    pts = [(wx, top + 0.05), front_top,
           (wx - depth - round_r * 0.4, front_top[1] - round_r),
           (wx - depth * 0.85, top - height * 0.75), (wx, top - height)]
    f.smooth(pts, z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.35)
    if XRAY:     # where the hand covers the edge, its outline shows dotted
        f.smooth(pts, z=XRAY_Z, tension=0.35, **XRAY_STYLE)
    return front_top


def rounded_lip(f, wx, top, depth=2.6, height=4.0, z=-5):
    """A rounded edge (the front corner is a large radius)."""
    pts = [(wx, top + 0.05), (wx - depth * 0.45, top), (wx - depth * 0.85, top - 0.35),
           (wx - depth, top - 1.2), (wx - depth * 0.92, top - 2.2),
           (wx - depth * 0.55, top - height * 0.8), (wx, top - height)]
    f.smooth(pts, z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.8)
    if XRAY:
        f.smooth(pts, z=XRAY_Z, tension=0.8, **XRAY_STYLE)


# ---------------------------------------------------------------- standard grips in profile

TILT = 0.0      # profiles are true side views: the front finger lies in the page


def nail_point(hand, f="i", k=0.45, out=0.9):
    """A point on the nail of finger f, `out` cm from the bone axis."""
    ch = hand.finger(f)
    return vadd(vlerp(ch["dip"], ch["tip"], k), vmul(ch["frames"][3][1], out))


def on_edge(posed, at, fingers="mrl", k=0.8, dx=0.25, along=None, spread=None):
    """Bend the fingers so that their pads also sit on the hold at page
    point `at` (an edge running into the page), each `dx` cm further along
    page x. With `spread`, they fan out along the hold's surface instead,
    each `spread` cm further than the one before it in page direction
    `along` (degrees), so that every fingertip shows beside the first."""
    for i, f in enumerate(fingers):
        if spread is None:
            posed.reach(f, add(at, (dx, 0)), k=k)
        else:
            posed.reach(f, add(at, mul(ang(along or 0.0), spread * (i + 1))), k=k)


def grip_hold(fig, kind):
    """The hold for a profile grip on a wall at x = WX, its top at y = 0: a
    rounded edge ('open'), a flat edge ('half') or a small incut edge."""
    if kind == "open":
        rounded_lip(fig, WX, 0, depth=2.6, height=4.2)
    elif kind == "half":
        edge_profile(fig, WX, 0, depth=1.5, height=2.4)
    else:
        edge_profile(fig, WX, 0, depth=0.8, height=2.0, slope=-12)


def grip_pose(kind, tilt=TILT):
    """The hand for a profile grip on the hold from grip_hold, seen from the
    thumb side with the arm hanging below the hold: 'open' (drag), 'half'
    (half crimp), 'full' (full crimp) or 'lock' (full crimp, the thumb over
    the index nail). The thumb rests unless the grip uses it. Returns the
    Posed."""
    if kind == "open":
        h = Hand("open", wrist=(5, 0))
        pad, k, a0 = (WX - 1.25, 0.72), 0.6, 100
        along, spread = 172, 0.3
    elif kind == "half":
        h = Hand("half")
        pad, k, a0 = (WX - 0.85, 0.0), 0.85, 95
        along, spread = 180, 0.3
    else:
        h = Hand("full", fingers={"i": (45, 105, -18)} if kind == "lock" else None)
        pad, k, a0 = (WX - 0.55, 0.1), 0.9, 95
        along, spread = 168, 0.22
    p = h.view("thumb", tilt=tilt).place("i", pad, a0=a0, k=k)
    # the other fingers on the same hold, fanned out toward its front
    on_edge(p, pad, k=k, along=along, spread=spread)
    if kind == "lock":
        n = nail_point(h)
        # the pad near the thumb tip, so the tip ends at the wall, not in it
        p.thumb_to(p.xy(n), part="pad", k=0.8, depth=p.depth(n))
    else:
        # the thumb rests low and back along the palm side, clear of the
        # index finger, the angle arcs and the edge these views exist to show
        tuck_thumb(p, kind)
    return p


def tuck_thumb(posed, kind):
    """Rest the thumb of a drag ('open'), half crimp ('half') or full crimp
    ('full') profile low and back along the palm side, so that the whole
    index finger and the edge stay in view."""
    if kind == "half":
        posed.thumb_to((WX - 5.0, 1.0), part="tip", weight=8,
                       prefer=dict(pa=15, ra=55, mcp=50, ip=60))
    else:
        posed.thumb_to((WX - 2.5, -3.6) if kind == "open" else (WX - 3.0, -3.5), part="tip")


def grip_profile(kind, pulley=False, z=0, **frame):
    """A side-profile panel of a grip (see grip_pose). Returns the figure and
    the Posed hand."""
    f = profile_frame(**frame)
    grip_hold(f, "open" if kind == "open" else "half" if kind == "half" else "full")
    p = grip_pose(kind)
    p.draw(f, z=z)
    if pulley:
        a2_pulley(f, p)
    return f, p


def a2_pulley(fig, posed, f="i", z=5):
    """Mark the A2 pulley: a dark band on the palm side of the finger's
    first segment."""
    h = posed.hand
    ch = h.finger(f)
    A, N, L = ch["frames"][1]
    g = GIRTH[f]
    c0 = vadd(ch["mcp"], vmul(A, SEG[f][0] * 0.3))
    c1 = vadd(ch["mcp"], vmul(A, SEG[f][0] * 0.62))
    q = [posed.xy(vadd(c0, vmul(N, -0.35))), posed.xy(vadd(c1, vmul(N, -0.35))),
         posed.xy(vadd(c1, vmul(N, -0.88 * g))), posed.xy(vadd(c0, vmul(N, -1.0 * g)))]
    fig.poly(q, z=z, fill=DARK, stroke=INK, sw=0.2)
    return lerp(q[2], q[3], 0.5)
