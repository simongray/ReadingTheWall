"""One hand for every close-up in the book.

The hand is a 3D model in centimetres, drawn in orthographic projection, so
a pose looks the same from every side and every close-up shows the same
hand at the same paper size (HAND_SCALE). Its proportions are those of an
adult hand 19 cm long from the wrist crease to the tip of the middle finger:
8.4 cm across the knuckles, the palm 10.8 cm from the wrist crease to the
webs and the middle finger 8.2 cm from its web, the fingers tapering from
1.9 cm across at the index knuckle, the palm about 3.4 cm deep with the pads
at its base standing out in front of it, and a wrist (5.7 by 3.3 cm) narrower
than both the hand and the forearm.

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
  front, white, and the other fingers are drawn behind it, each with its
  own outline in a grey one step darker than the finger in front of it
  (BACK_FILLS). tilt turns the back of the hand toward you, by TILT unless
  a figure says otherwise, so that the palm has its width and the fingers
  step apart; STAGGER moves them a little further aside.
- "little": from the little-finger side, palm facing right; the fingers
  behind are grey as from the thumb side, and the thumb is grey too.
- "back": the back of the hand, thumb on the left when the fingers point up.
  With tilt (the thumb side toward you) and pitch (the fingertips toward
  you) it is a three-quarter view; p.xy draws the rock in the same projection.
- "palm": the palm, thumb on the right.
`a0` is the screen direction of the hand (wrist to knuckles) and `flip`
mirrors the drawing (the palm then faces left in a profile).

Every part is built as convex hulls of cross-section rings (a tube per
finger segment, a rounded wedge per joint, the palm with the pad on its
little-finger side, the ball of the thumb, the wrist and the forearm, the
last two meeting in a waist), projected and merged with the silhouette technique of
climb.py. The silhouette carries the grip. The lines drawn inside it are few:
the nails (seen from the side, a line inside the back of the fingertip), the
creases over the knuckles and the joints (finger_creases, thumb_creases), the
line that sets the thumb's base off from the back of the hand (thumb_base)
and, in back and palm views, the fine lines between fingers that touch.

Typical use (a half crimp on an edge whose top meets the wall at WX, 0):

    h = Hand("half")                                   # a grip from GRIPS
    p = h.view("thumb").place("i", (WX - 0.85, 0), a0=95, k=0.85)
    h.rest_thumb()                       # or p.thumb_to(...) where it grips
    fig = profile_frame(-12.0, y1=8.6, posed=p)    # cuts the arm below the wrist
    p.draw(fig)
    joint_arc(fig, p, "i", "pip", 1.5, "≈90°")

place() puts a finger pad on a page point with the hand at a0 (or with the
last segment pointing along `distal`); reach() and thumb_to() solve finger
and thumb joints for a contact point, as close as they can to the pose the
digit started in; on_edge() sets the other fingers on the same hold, a
short finger sliding along the hold's surface (a polyline, e.g. from
outline()) to where it reaches it; forearm_point() is where a close-up's
frame cuts the arm (FOREARM_SHOWN below the wrist, the same in every
close-up; profile_frame takes the Posed hand for that); joint(), angle(),
surface() and at() read page points back for labels and arrows.
grip_profile() draws the standard side views of the open hand, half crimp,
full crimp and thumb lock.
"""

import math

from climb import (INK, WHITE, LIGHT, MID, PALE, DARK, Fig, ang, add, sub, mul, norm,
                   length, rot, lerp, perp, dot, XRAY, XRAY_Z, XRAY_STYLE)

HAND_SCALE = 2.6        # paper mm per cm, for every hand close-up in the book

OUTLINE = 0.34          # outline weights in mm, as elsewhere in the book
BACK_SW = 0.26          # the fingers behind the front one in a side view
# their greys, nearest first: one step apart on the e-ink panel's 16 greys
# (#000000, #111111, ... #ffffff), so that each finger reads on its own
BACK_FILLS = ("#dddddd", "#cccccc", "#bbbbbb")
FINE = 0.20             # lines between fingers that touch
DETAIL = 0.24           # nails

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
# Lengths in cm for an adult hand 19 cm long, in the proportions of published
# means: across the knuckles 0.44 of the length (8.4 cm), the palm from the
# wrist crease to the webs between the fingers 0.57 (10.8 cm) and the middle
# finger from its web to its tip 0.43 (8.2 cm). The surveys give breadth 0.43-
# 0.47 of length, palm to the base crease of the middle finger 0.58-0.60 and
# that finger from its web 0.43: Zarzycka, Zaluska & Osemlak 1990, Annales UMCS
# D 45(11), 65-; Spahr, Bradtmiller & Guan (NIOSH), stacks.cdc.gov/view/cdc/187718;
# Madadin & Menezes 2022, Acta Biomed 93(2), e2022063.
# The knuckle joints sit about 2 cm inside the palm, since the skin of the
# palm runs on to the webs halfway along the first bones, so the joint centres
# of the middle finger are 9.1 + 4.55 + 2.85 + 2.05 + pad 0.45 = 19 cm. From
# the back, the hand to the knuckles is still a little shorter than the middle
# finger, as in a real hand; a palm as long as the finger, with thick fingers,
# reads as a mitten.

MCP = {"i": (9.0, 3.2, 0.0), "m": (9.1, 1.1, 0.05), "r": (8.8, -0.95, 0.0),
       "l": (8.05, -2.85, -0.15)}
SEG = {"i": (4.25, 2.45, 1.9), "m": (4.55, 2.85, 2.05), "r": (4.3, 2.75, 2.0),
       "l": (3.6, 2.05, 1.8)}
PAD = {"i": 0.45, "m": 0.45, "r": 0.45, "l": 0.4}
SPLAY = {"i": 5.0, "m": 0.0, "r": -5.0, "l": -11.0}   # relaxed, toward the thumb
GIRTH = {"i": 1.0, "m": 1.02, "r": 0.96, "l": 0.84}
WEB = {"i": 2.0, "m": 2.0, "r": 2.0, "l": 1.85}       # knuckle to web, along the finger
FINGERS = "imrl"
NAMES = {"i": "index", "m": "middle", "r": "ring", "l": "little", "t": "thumb"}

# cross-sections along each finger segment, for an index finger:
# (fraction of the segment, half-width, back, palm side), from the bone axis.
# The finger tapers and waists between its joints: 1.9 cm across at the
# knuckle, 1.8 at the middle joint, 1.6 at the end joint. Thickness in profile
# (back + palm side) is about 1.7 cm along the first segment, 1.5 along the
# middle one and 1.4 along the last, the pad fullest under the nail. The palm
# side swells at the base of the finger, where it runs into the palm.
SECTIONS = (
    ((0.00, 0.96, 0.82, 1.22), (0.30, 0.93, 0.78, 0.96), (0.65, 0.88, 0.75, 0.92),
     (1.00, 0.91, 0.78, 0.88)),
    ((0.00, 0.91, 0.78, 0.88), (0.50, 0.82, 0.69, 0.82), (1.00, 0.80, 0.66, 0.78)),
    ((0.00, 0.80, 0.66, 0.78), (0.50, 0.76, 0.58, 0.82), (0.95, 0.70, 0.50, 0.74)),
)
KNUCKLE = (0.96, 1.1, 1.5)       # the metacarpal head, round which the knuckle bends

# thumb: metacarpal, proximal and distal (end joint to the tip of the pad).
# Laid alongside the index finger, its tip reaches the middle of the index
# finger's first segment.
THUMB_SEG = (4.4, 3.15, 2.7)
CMC = (1.7, 2.45, -0.95)        # base of the thumb metacarpal
THUMB_SECTIONS = (    # 2.05 cm across at its knuckle, 1.95 at the end joint
    ((0.10, 0.62, 0.55, 0.7), (0.45, 1.02, 0.82, 1.02), (1.00, 1.03, 0.84, 1.0)),
    ((0.00, 1.03, 0.84, 1.0), (0.50, 0.96, 0.78, 0.97), (1.00, 0.98, 0.78, 0.92)),
    ((0.00, 0.98, 0.78, 0.92), (0.40, 0.96, 0.72, 1.0), (0.80, 0.88, 0.6, 0.9)),
)

# palm: rings across the hand (x, y centre, z centre, half-width, back, palm side)
# Seen from the back the palm widens from 5.7 cm at the wrist to 8.4 cm at
# the knuckles. In profile the back of the hand arches a little over the
# metacarpals, and the hand is about 3.4 cm deep across the palm and 2.8
# cm at the knuckles. The pads at the base of the palm stand out in front
# of it: the ball of the thumb (thenar_solid) to about 4.5 cm deep, the
# pad on the little-finger side (HYPOTHENAR, part of the palm) to about 3.7.
# Without them a profile is a flat board running straight into the arm.
PALM_RINGS = ((-0.9, 0.25, -0.1, 2.85, 1.28, 2.02), (0.0, 0.15, -0.05, 3.05, 1.38, 2.0),
              (1.8, 0.1, 0.0, 3.55, 1.55, 1.9), (4.5, 0.15, 0.0, 3.95, 1.55, 1.85),
              (6.6, 0.2, 0.0, 4.15, 1.36, 1.7), (7.4, 0.2, 0.0, 4.2, 1.2, 1.6))
HYPOTHENAR = ((-0.5, -1.5, -0.4, 1.0, 0.5, 1.7), (1.0, -1.85, -0.6, 1.2, 0.5, 1.55),
              (2.8, -2.15, -0.6, 1.3, 0.5, 1.5), (4.8, -2.5, -0.5, 1.1, 0.5, 1.2))
WRIST = (-0.9, 0.25, -0.1)        # centre of the wrist joint
WRIST_REACH = 1.2                 # how far the wrist's own solid runs into hand and forearm
# forearm rings: (distance from the wrist centre toward the elbow, half-width,
# back, front). The wrist is a waist, 5.7 cm across and 3.3 cm deep,
# narrower than the palm with its pads and than the forearm, which fills
# out to about 7.1 cm across and 4.6 cm deep 8 cm up and 7.5 by 5.5 cm 18
# cm up.
FOREARM = ((-0.12, 2.85, 1.28, 2.02), (1.5, 3.05, 1.42, 2.15), (4.0, 3.35, 1.62, 2.38),
           (8.0, 3.55, 1.9, 2.7), (13.0, 3.7, 2.2, 3.05), (18.0, 3.75, 2.3, 3.25),
           (24.0, 3.6, 2.3, 3.3), (32.0, 3.45, 2.2, 3.2))

# joint ranges (degrees)
RANGE = {"mcp": (0, 90), "pip": (0, 110), "dip": (-20, 80),
         "t_ra": (0, 60), "t_pa": (0, 80), "t_rot": (30, 175), "t_mcp": (-10, 60),
         "t_ip": (-25, 80), "ext": (-70, 85), "dev": (-30, 20)}

# ---------------------------------------------------------------- grips
#
# Finger angles (MCP, PIP, DIP) per finger, the thumb, and the wrist. Figure
# code starts from one of these and overrides what it needs. Every grip the
# arm hangs from keeps the wrist at HANG (extended a little, not deviated),
# so that the hand looks the same from tile to tile; only the sloper (wrist
# dropped below the hold), the undercling (the straight arm comes down to the
# wrist, which bends forward), the palm press (bent back, the forearm off the
# face) and the wrap (palm flat on the face, the arm coming up to it) set
# their own.

HANG = (10, 0)

RELAXED_THUMB = dict(ra=18, pa=22, rot=125, mcp=18, ip=18)

GRIPS = {
    "relaxed": dict(f=dict(i=(18, 24, 10), m=(22, 30, 12), r=(26, 36, 14), l=(30, 40, 16)),
                    thumb=RELAXED_THUMB, wrist=HANG),
    "flat": dict(f=dict(i=(0, 0, 0, 2), m=(0, 0, 0, 0), r=(0, 0, 0, -1), l=(0, 0, 0, -3)),
                 thumb=dict(ra=28, pa=8, rot=60, mcp=8, ip=6), wrist=(0, 0)),
    "open": dict(f=dict(i=(18, 40, 36), m=(18, 40, 36), r=(20, 42, 36), l=(22, 44, 34)),
                 thumb=RELAXED_THUMB, wrist=HANG),
    # the crimps hang the hand below the edge: the first segments rise from
    # knuckles below it, the middle joints bend over it and the end segments
    # lie on it, pointing into the wall (with the knuckles bent far, the
    # fingers hook down over the edge like a claw). The angles match
    # photographs of each grip seen from the thumb side
    "half": dict(f=dict(i=(13, 85, 0), m=(13, 87, 0), r=(16, 87, 1), l=(18, 85, 3)),
                 thumb=RELAXED_THUMB, wrist=HANG),
    "full": dict(f=dict(i=(40, 98, -20), m=(40, 98, -20), r=(40, 95, -18),
                        l=(43, 90, -12)),
                 thumb=RELAXED_THUMB, wrist=HANG),
    "pinch": dict(f=dict(i=(40, 62, 24), m=(42, 64, 24), r=(44, 66, 26), l=(46, 66, 26)),
                  thumb=dict(ra=22, pa=58, rot=145, mcp=10, ip=8), wrist=HANG),
    "sloper": dict(f=dict(i=(10, 22, 20), m=(10, 24, 20), r=(12, 26, 20), l=(14, 28, 20)),
                   thumb=dict(ra=30, pa=30, rot=115, mcp=8, ip=6), wrist=(-25, 0)),
    "pocket": dict(f=dict(i=(55, 85, 45), m=(30, 60, 25), r=(30, 60, 25), l=(25, 30, 15)),
                   thumb=RELAXED_THUMB, wrist=HANG),
    # an open hand, the thumb pointing out, as the undercling entry asks
    "undercling": dict(f=dict(i=(12, 32, 20), m=(12, 32, 20), r=(12, 32, 20), l=(12, 32, 20)),
                       thumb=dict(ra=58, pa=22, rot=95, mcp=5, ip=5), wrist=(-45, 0)),
    # flat with the fingers spread, their tips coming down to the face
    "palm": dict(f=dict(i=(8, 5, 2, 3), m=(8, 5, 2, 1), r=(8, 5, 2, -1), l=(8, 5, 2, -5)),
                 thumb=dict(ra=26, pa=8, rot=70, mcp=4, ip=4), wrist=(25, 0)),
    "wrap": dict(f=dict(i=(9, 75, 20), m=(9, 75, 20), r=(9, 75, 20), l=(9, 75, 20)),
                 thumb=dict(ra=28, pa=2, rot=45, mcp=4, ip=4), wrist=(30, -12)),
    "jug": dict(f=dict(i=(35, 70, 35), m=(35, 70, 35), r=(37, 72, 35), l=(40, 72, 35)),
                thumb=RELAXED_THUMB, wrist=HANG),
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


OVERLAP = 0.3     # cm: how far the pieces of a finger reach into each other


def _tube(origin, fr, length_, stations, g, cap=None, back=OVERLAP, fwd=OVERLAP):
    """Hulls along one bone: one per pair of cross-sections, each reaching a
    little past its ends so that neighbours overlap (abutting fills leave a
    hairline seam, and chaikin's rounded corners a notch in the outline)."""
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
        pa = ring(vadd(a[0], vmul(A, -back)), fr, *a[1:]) if i == 0 else ext(a, b, OVERLAP)
        if last:
            pb = ring(vadd(b[0], vmul(A, 0 if cap else fwd)), fr, *b[1:])
        else:
            pb = ext(b, a, OVERLAP)
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

    def view(self, view="thumb", a0=90.0, tilt=None, flip=False, at=(0.0, 0.0), front=None,
             stagger=None, pitch=0.0):
        """Place the hand in a figure (see Posed). In a side view the front
        finger (the index from the thumb side, the little finger from the
        other side) bends in the plane of the page when tilt is 0, so its
        segments show their true lengths. stagger: how far the fingers behind
        it step aside (cm, one number or three, nearest first; default STAGGER,
        which every close-up in the book uses). A three-quarter view is a back view with
        tilt (the thumb side toward you) and pitch (the fingertips toward
        you). tilt defaults to TILT in a side view and to 0 in the others."""
        if tilt is None:
            tilt = TILT if view in ("thumb", "little") else 0.0
        return Posed(self, view, a0, tilt, flip, at, front, stagger, pitch)

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
                         back=0.4 if k == 0 and buried else OVERLAP)
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

    def knuckle_solid(self, f, ch=None, k=1.0):
        """The round head of the bone at finger f's knuckle, k times its size."""
        ch = ch or self.finger(f)
        g = GIRTH[f]
        w, d, p = (x * g * k for x in KNUCKLE)
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
        return ring(vadd(ch["mcp"], vmul(F1[0], reach)), F1, 0.86 * g, 0.72 * g, 1.05 * g) + \
            ring((x - 1.6, y, z), F0, 0.88 * g, 1.15 * g, 1.55 * g) + \
            ring((x, y, z), F0, 0.88 * g, 1.05 * g, 1.5 * g)

    def root_mask(self, f, ch=None):
        """The part of finger f that lies inside the hand, from its knuckle to
        its webs: in a back or palm view, no line runs across it. An outer
        finger has a web on one side only, so its far end leans that way, off
        the side of the hand."""
        ch = ch or self.finger(f)
        g = GIRTH[f]
        A, N, L = ch["frames"][1]
        lean = {"i": -0.32, "l": 0.32}.get(f, 0.0)
        far = vadd(vadd(ch["mcp"], vmul(A, WEB[f] - 0.12)), vmul(L, lean))
        return ring(ch["mcp"], (A, N, L), 1.06 * g, 0.9 * g, 1.1 * g) + \
            ring(vadd(ch["mcp"], vmul(A, 0.5)), (A, N, L), 1.0 * g, 0.9 * g, 1.1 * g) + \
            ring(far, (A, N, L), (1.0 - abs(lean)) * g, 0.9 * g, 1.1 * g)

    def palm_solid(self):
        F0 = frame_of(X, Z)
        pts = []
        for x, y, z, w, d, p in PALM_RINGS + HYPOTHENAR:
            pts += ring((x, y, z), F0, w, d, p)
        for f in FINGERS:
            x, y, z = MCP[f]
            g = GIRTH[f]
            pts += ring((x - 0.1, y, z), F0, KNUCKLE[0] * g, KNUCKLE[1] * g, KNUCKLE[2] * g)
        # the sides of the hand run on smoothly past the outer knuckles,
        # where the splayed outer fingers leave it
        x, y, z = MCP["l"]
        pts += ring((x + 0.5, y - 0.28, z), F0, 0.8, 0.6, 0.8)
        x, y, z = MCP["i"]
        pts += ring((x + 0.5, y + 0.14, z), F0, 0.96, 0.6, 0.8)
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

    def wrist_solid(self, reach=WRIST_REACH):
        """The wrist joint: its cross-section swept from the forearm to the
        hand, which rounds the bend, and carried `reach` cm into each, so
        that the waist where the two meet is one clean corner."""
        fa = self.forearm_frame()
        fh = frame_of(X, Z)
        pts = []
        for i in range(7):
            t = i / 6
            fr = frame_of(vlerp(fa[0], fh[0], t), vlerp(fa[1], fh[1], t))
            c = vadd(WRIST, vmul(fr[0], reach * (2 * t - 1)))
            pts += ring(c, fr, *FOREARM[0][1:])
        return pts

    def thenar_solid(self, th=None):
        """The ball of the thumb: the muscles round the thumb's metacarpal,
        pulled toward the middle of the palm, so that it fills the base of
        the thumb without swelling it much past the thumb's own width."""
        th = th or self.thumb()
        F1 = th["frames"][0]
        F0 = frame_of(X, Z)
        # (the first ring tapers it into the wrist, so that no corner shows there)
        pts = ring((-1.9, 0.9, -0.3), F0, 0.9, 0.4, 1.7) + \
            ring((-0.6, 1.1, -0.6), F0, 1.05, 0.5, 1.55) + \
            ring((0.8, 1.4, -1.0), F0, 1.3, 0.5, 1.75) + \
            ring((2.0, 1.6, -1.0), F0, 1.5, 0.5, 2.0) + \
            ring((3.6, 1.75, -1.0), F0, 1.5, 0.5, 2.0) + \
            ring((5.2, 1.85, -0.9), F0, 1.2, 0.5, 1.3)
        mid = (3.6, 0.7, -1.1)
        for s, k, w, d, p in ((0.6, 0.5, 1.1, 0.8, 1.25), (2.0, 0.55, 1.1, 0.8, 1.25),
                              (3.4, 0.3, 0.98, 0.74, 1.0)):
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
        T1 = vadd(a, vmul(tw, 0.75))
        F1 = ix["frames"][1]
        I1 = vadd(vadd(ix["mcp"], vmul(F1[0], 0.6)), vmul(F1[2], 0.78))
        m = vlerp(T1, I1, 0.5)
        ctrl = vlerp(m, CMC, 0.3)
        edge = [vadd(vmul(T1, (1 - s) ** 2), vadd(vmul(ctrl, 2 * s * (1 - s)), vmul(I1, s * s)))
                for s in (i / 8 for i in range(9))]
        return [vlerp(CMC, th["mcp"], 0.4), th["mcp"]] + edge + [ix["mcp"], (5.3, 2.35, -0.3)]

    def finger_web(self, a, b):
        """The skin between two fingers, from their knuckles to the web, whose
        free edge dips a little between them."""
        ca, cb = self.finger(a), self.finger(b)
        sa = 1 if MCP[b][1] > MCP[a][1] else -1
        ga, gb = GIRTH[a], GIRTH[b]
        Fa, Fb = ca["frames"][1], cb["frames"][1]
        ea = vadd(vadd(ca["mcp"], vmul(Fa[0], WEB[a])), vmul(Fa[2], sa * 0.86 * ga))
        eb = vadd(vadd(cb["mcp"], vmul(Fb[0], WEB[b])), vmul(Fb[2], -sa * 0.86 * gb))
        dip = vadd(vlerp(ea, eb, 0.5), vmul(vlerp(Fa[0], Fb[0], 0.5), -0.22))
        return [vadd(ca["mcp"], vmul(Fa[2], sa * 0.9 * ga)), ea, dip, eb,
                vadd(cb["mcp"], vmul(Fb[2], -sa * 0.9 * gb))]

    # ------------------------------------------------------------ surface marks
    def _crease(self, c, fr, w, d, a0, a1, bow=0.0, n=9):
        """A crease across the back of a joint: from angle a0 to a1 round the
        cross-section (0 the middle of the back, positive toward +L), bowed
        `bow` cm along the bone at its middle. Points with surface normals."""
        A, N, L = fr
        out = []
        mid = (a0 + a1) / 2
        half = max(abs(a1 - a0) / 2, 1e-6)
        for i in range(n):
            t = math.radians(a0 + (a1 - a0) * i / (n - 1))
            k = 1 - ((math.degrees(t) - mid) / half) ** 2
            q = vadd(vadd(c, vmul(N, d * math.cos(t))), vmul(L, w * math.sin(t)))
            nrm = vnorm(vadd(vmul(N, math.cos(t) / d), vmul(L, math.sin(t) / w)))
            out.append((vadd(q, vmul(A, bow * k)), nrm))
        return out

    def finger_creases(self, f, ch=None, side=None, skip=(), arc=0.26):
        """The creases on the back of finger f: a curve over its knuckle, two
        across its middle joint and one across its end joint. side: None
        draws each right across the back, as a back view sees it; +1 or -1
        only that side of the finger's back (+L or -L), as a side view sees
        it, where it starts at the outline (the knuckle's starts inside it,
        where the finger's own outline ends). skip: joints to leave plain
        ("mcp", "pip", "dip"); arc: how far the knuckle's curve bows along
        the finger in a back view."""
        ch = ch or self.finger(f)
        g = GIRTH[f]
        F = ch["frames"]
        flex = ch["flex"]

        def span(half, far=72, near=6):
            return (-half, half) if side is None else (side * near, side * far)
        out = []
        if "mcp" not in skip:
            fr = flexed(F[0], flex[0] / 2)
            w, d = KNUCKLE[0] * g, KNUCKLE[1] * g
            a0, a1 = span(46, 72, 34)
            out.append(self._crease(ch["mcp"], fr, w, d, a0, a1,
                                    bow=arc if side is None else 0.12))
        if "pip" not in skip:
            fr = flexed(F[1], flex[1] / 2)
            w, d = SECTIONS[1][0][1] * g, SECTIONS[1][0][2] * g
            a0, a1 = span(40)
            for s_ in (-1, 1):
                out.append(self._crease(vadd(ch["pip"], vmul(fr[0], s_ * 0.16)), fr, w, d, a0, a1,
                                        bow=s_ * 0.05))
        if "dip" not in skip:
            fr = flexed(F[2], flex[2] / 2)
            w, d = SECTIONS[2][0][1] * g, SECTIONS[2][0][2] * g
            a0, a1 = span(36, 62)
            out.append(self._crease(ch["dip"], fr, w, d, a0, a1))
        return out

    def thumb_creases(self, th=None, side=None):
        """A crease over the thumb's knuckle and one over its end joint."""
        th = th or self.thumb()
        F = th["frames"]
        flex = th["flex"]
        out = []
        for c, fr, st in ((th["mcp"], flexed(F[0], flex[0] / 2), THUMB_SECTIONS[1][0]),
                          (th["ip"], flexed(F[1], flex[1] / 2), THUMB_SECTIONS[2][0])):
            a0, a1 = (-42, 42) if side is None else (side * 6, side * 62)
            out.append(self._crease(c, fr, st[1], st[2], a0, a1))
        return out

    def thumb_base(self, th=None):
        """The line that sets the thumb's base off from the rest of the hand:
        along the side of its metacarpal that faces the index knuckle, from
        where the thumb's own outline ends toward the wrist. The fleshy mound
        lies between it and the outline. 3D points, thumb end first."""
        th = th or self.thumb()
        A, N, L = th["frames"][0]
        Q = vadd(MCP["i"], (0.0, 0.0, 1.2))
        end = vadd(CMC, vmul(A, THUMB_SEG[0]))
        sgn = 1 if vlen(vsub(vadd(end, L), Q)) < vlen(vsub(vsub(end, L), Q)) else -1
        w = THUMB_SECTIONS[0][-1][1]
        out = []
        for t in (0.98, 0.84, 0.68, 0.52, 0.38, 0.26):
            bow = 0.14 * math.sin(math.pi * (t - 0.26) / 0.72)
            out.append(vadd(vadd(CMC, vmul(A, THUMB_SEG[0] * t)), vmul(L, sgn * (w * 0.96 + bow))))
        return out

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
# In a true side view the palm is only its thickness wide and the fingers
# behind the front one hide almost exactly behind it, which makes the hand a
# thin board with one long finger. So every side view turns the back of the
# hand TILT degrees toward you: the fingers step apart by about 0.4 cm each
# and the palm shows its width, while the front finger's segments lose at most
# 2% of their length. Each finger behind is also shifted on the page by
# STAGGER cm (nearest first) along SHEAR_DIR, a direction in the hand frame
# (its parts toward the fingertips and toward the palm), so that its tip steps
# out from behind the front finger. A larger shift stacks the fingers into a
# thick grey band along the back of the hand, which makes them look short and
# fat. Everything that reads or solves a finger (joint, angle, surface, reach,
# on_edge, place) uses the same projection, so the pads still land on the hold
# as drawn.
STAGGER = (0.1, 0.2, 0.3)
TILT = 12.0
# A close-up shows this much forearm (cm) below the wrist joint: its frame
# cuts the arm there (Posed.forearm_point), so that the wrist sits the same
# way in every close-up. A long stretch of arm reads as part of the hand
# and makes the palm look huge; a frame that cuts above the wrist hides the
# waist that tells the hand from the arm. (The hand atlas, short of room,
# shows a little less, the same in every tile.)
FOREARM_SHOWN = 5.5
SHEAR_DIR = (1.0, -0.3)
# A finger set on a hold (on_edge) that can reach its spot only by bending
# more than SLIDE_BEND degrees (summed over its three joints) away from the
# grip slides along the hold's surface instead, each cm of sliding costing
# as much as SLIDE_COST of bending (see Posed.reach).
SLIDE_BEND = 45.0
SLIDE_COST = 0.004
BASE_INSIDE = 0.7   # cm: how far inside the palm's outline the thumb's base line must run
PITCH_ARC = 0.016   # cm per degree of pitch that the knuckles' arcs bow further in a back view


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

    def __init__(self, hand, view, a0, tilt, flip, at=(0.0, 0.0), front=None, stagger=None,
                 pitch=0.0):
        self.hand = hand
        self.kind = view
        self.a0, self.tilt, self.flip, self.pitch = a0, tilt, flip, pitch
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
        b = math.radians(self.pitch)
        S = ((math.cos(b), 0.0, math.sin(b)), Y, (-math.sin(b), 0.0, math.cos(b)))
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

    def forearm_point(self, s=FOREARM_SHOWN):
        """Page point on the forearm's axis s cm below the wrist joint:
        where a close-up's frame cuts the arm (see FOREARM_SHOWN)."""
        u = self.hand.forearm_frame()[0]
        return self.xy(vsub(WRIST, vmul(u, s)))

    # -- solving
    def reach(self, f, target, dip=None, k=0.8, lock=None, slide=None, room=None):
        """Bend finger f so that its pad lands on page point `target`,
        keeping as close as it can to the pose it started in: the middle
        joint gives most and the knuckle least. dip, if given, fixes the end
        joint; lock=(lo, hi) limits the middle joint. Returns the miss in
        cm.

        slide: the hold's surface near the target, as a page direction
        (degrees; a straight face) or a page polyline (a curved one). The
        pad then lands on that surface wherever the finger meets it nearest
        its starting pose and the target, and within `room` (cm along the
        surface from the target) if given: a short finger lands nearer the
        palm instead of straightening to reach. The miss is then its
        distance from that stretch of surface.

        Three joints for one point leave a degree of freedom over, which
        goes on staying near the starting pose: a finger beside the front
        one then bends the way the front one does, and a side view shows it
        behind the front one instead of along the back of the hand."""
        mcp0, pip0, dip0, spl = self.hand.f[f]
        free = dip is None
        lo, hi = lock or RANGE["pip"]
        line = _surface(slide, target) if slide is not None else None
        s0 = nearest(line, target)[1] if line else 0.0

        def off(pt):
            """Squared miss of page point pt, and how far along the surface
            from the target it lies."""
            if line is None:
                d = sub(pt, target)
                return d[0] ** 2 + d[1] ** 2, 0.0
            d2, s = nearest(line, pt)
            a = s - s0
            return d2 + (penalty(a, *room) if room else 0.0), a

        def joints(q):
            return (q[0], q[1], q[2] if free else dip)

        def cost(q):
            m, p, d = joints(q)
            pt = self.xy(pad_point(None, f, k, finger_chain(f, m, p, d, spl)), f)
            e, a = off(pt)
            e = 4 * e + SLIDE_COST * a * a if line else e
            e += 4 * (penalty(m, *RANGE["mcp"]) + penalty(p, lo, hi) +
                      penalty(d, *RANGE["dip"]))
            return e + 1e-5 * (8 * (m - mcp0) ** 2 + (p - pip0) ** 2 + 2 * (d - dip0) ** 2)
        best, v = None, 1e9
        for m0, p0 in ((mcp0, pip0), (mcp0 + 20, pip0 - 20), (mcp0 - 15, pip0 + 15)):
            q0 = [m0, p0, dip0] if free else [m0, p0]
            q, val = nelder_mead(cost, q0, [8.0] * len(q0), iters=300)
            if val < v:
                best, v = q, val
        m, p, d = joints(best)
        m = min(max(m, RANGE["mcp"][0]), RANGE["mcp"][1])
        p = min(max(p, lo), hi)
        d = min(max(d, RANGE["dip"][0]), RANGE["dip"][1])
        self.hand.f[f] = (m, p, d, spl)
        pt = self.xy(pad_point(self.hand, f, k), f)
        return math.sqrt(off(pt)[0])

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
    def draw(self, fig, z=0.0, front=None, fill=WHITE, back_fill=None, ghost=False,
             thumb_front=None, details=True, forearm=32.0, hide=(), others="copy", plain=()):
        """Draw the hand, always with its thumb. front: the finger drawn in
        front in a side view (default the view's front finger). others, in
        a side view: which fingers to draw behind it, each in its own grey
        (back_fill: one grey, or three, nearest first; default BACK_FILLS)
        with its own outline: "copy" or "all" (the default) all of them,
        "none" none, or a string of finger names (a pocket, where the
        finger in the hole is the subject). From the little-finger
        side the thumb, behind the hand, is a darker grey. thumb_front: in a
        back or palm view, whether the thumb is drawn over the hand; drawn
        under it, only what sticks out past its side shows (default: over it
        in a back view, where a thumb without its own outline reads as a lump
        on the side of a wide hand; from its depth in a palm view). hide:
        fingers not to draw (back and palm views). details: the nails, the
        creases and the line along the thumb's base, the only lines drawn
        inside the outline besides the
        lines between fingers that touch. plain: joints of the front finger
        without creases ("pip" where joint_arc measures it, whose lines they
        would tangle)."""
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

        def layer(polys, fill_, sw, masks=(), nails=()):
            layers.append((polys, fill_, sw, masks, nails))
            return len(layers) - 1

        def creases(f, side=None, skip=(), arc=0.26):
            """A layer of its own for the creases, above every finger's mask."""
            layer([], fill, sw_fine, nails=[("crease", c, f) for c in
                                            h.finger_creases(f, chains[f], side, skip, arc)])

        def side_of(fr):
            """Which side of the frame's back faces you, in a side view."""
            return 1 if vdot(fr[2], self.eye) >= 0 else -1

        if kind in ("thumb", "little"):
            front = front or self.front
            main.append(P(h.knuckle_solid(front, chains[front])))
            if kind == "little":
                thumb_layer = layer(tsol, LIGHT, sw_back)
            # the fingers behind the front one, farthest first, each with
            # its own outline and a grey one step darker than the finger in
            # front of it (BACK_FILLS), so that they read as fingers
            near = [f for f in (FINGERS if kind == "thumb" else FINGERS[::-1]) if f != front]
            if others in ("copy", "all"):
                behind = near
            elif others == "none":
                behind = []
            else:
                behind = [f for f in near if f in others]
            self._behind = {f: [P(h.root_solid(f, chains[f]), f)] +
                            [P(s, f) for s in h.finger_solids(f, chains[f], buried=False)]
                            for f in behind}
            fills = back_fill or BACK_FILLS
            if isinstance(fills, str):
                fills = (fills,) * 3
            self._behind_layer = {}
            for f in reversed(behind):
                self._behind_layer[f] = layer(self._behind[f], fill if ghost else
                                              fills[near.index(f)], sw_back)
            layer(main, fill, sw_out)
            front_layer = layer([P(s) for s in h.finger_solids(front, chains[front])], fill,
                                # the finger's own line stops at the knuckle's outline
                                sw_out, masks=[P(h.root_solid(front, chains[front])),
                                               P(h.knuckle_solid(front, chains[front], 0.96))],
                                nails=[front] if details else ())
            if details:
                creases(front, side_of(chains[front]["frames"][1]), plain)
            if kind == "thumb":
                thumb_layer = layer(tsol, fill, sw_out, masks=tmask,
                                    nails=["t"] if details else ())
                if details:
                    layer([], fill, sw_fine, nails=["base"] +
                          [("crease", c, None) for c in
                           h.thumb_creases(th, side_of(th["frames"][1]))])
        else:
            for f in FINGERS:
                if f not in hide:
                    main.append(P(h.knuckle_solid(f, chains[f])))
            if thumb_front is None:
                tip_d = vdot(vsub(th["tip"], (5.0, 1.0, 0.0)), self.eye)
                thumb_front = kind == "back" or tip_d > -0.3
            fingers = [f for f in FINGERS if f not in hide]
            allf = []
            for f in fingers:
                allf += [P(s) for s in h.finger_solids(f, chains[f])]
            webs = [self._poly(h.finger_web(a, b)) for a, b in (("i", "m"), ("m", "r"), ("r", "l"))
                    if a not in hide and b not in hide]
            # a thumb behind the hand is drawn before it, with its own outline:
            # what shows of it sticks out past the side of the hand
            if not thumb_front:
                thumb_layer = layer(tsol, fill, sw_out, nails=["t"] if details else ())
            layer(main + allf + webs, fill, sw_out)
            mask = webs + [P(h.knuckle_solid(f, chains[f])) for f in fingers] + \
                [P(h.root_mask(f, chains[f])) for f in fingers]
            if kind == "back":
                mask = [P(h.palm_solid())] + mask
            else:
                band = []
                F0 = frame_of(X, Z)
                for f in fingers:
                    x, y, zc = MCP[f]
                    band += ring((x - 1.6, y, zc), F0, 1.0, 0.95, 1.36) + \
                        ring((x + 0.2, y, zc), F0, 0.96, 0.9, 1.3)
                mask += [P(band)] + [P(h.root_solid(f, chains[f])) for f in fingers]
            if not ghost:
                dep = {f: vdot(chains[f]["pip"], self.eye) for f in fingers}
                for f in sorted(fingers, key=lambda f: dep[f]):
                    layer([P(s) for s in h.finger_solids(f, chains[f])], fill, sw_fine,
                          masks=mask, nails=[f] if details else ())
            if details and not ghost:
                # seen from along the hand, the arcs over the knuckles flatten
                # into a line of dashes across its back, so they bow further
                for f in fingers:
                    creases(f, arc=0.26 + PITCH_ARC * min(abs(self.pitch), 15.0))
            if thumb_front:
                thumb_layer = layer(tsol, fill, sw_out, masks=tmask,
                                    nails=["t"] if details else ())
            if details and not ghost:
                layer([], fill, sw_fine, nails=["base"] +
                      [("crease", c, None) for c in h.thumb_creases(th)])
        self._record(layers, thumb_layer, th, chains, front if kind in ("thumb", "little")
                     else None, front_layer if kind in ("thumb", "little") else None, ghost)
        for i, (polys, fill_, sw, masks, nails) in enumerate(layers):
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
                if f == "base":
                    self._thumb_base(fig, th, zl + 0.008)
                    continue
                if isinstance(f, tuple):
                    self._mark_run(fig, f[1], zl + 0.008, f[2])
                    continue
                loop = h.nail(f, th if f == "t" else chains[f])
                # the part of the nail turned toward you: seen from the side,
                # a line just inside the back of the fingertip
                vis = [self.xy(p, f) for p, n in loop if vdot(n, self.eye) > 0.2]
                if len(vis) > 4 and _area(hull2(vis)) > 0.1:
                    self._mark_run(fig, loop + loop[:1], zl + 0.008, f)

    def xray_end(self, fig, f="i"):
        """The end segment of finger f as a dotted outline, the convention for
        what a hand or shoe covers (XRAY_STYLE): for a thumb locked over it."""
        h = self.hand
        ch = h.finger(f)
        g = GIRTH[f]
        F, st = ch["frames"], SECTIONS[2]
        pts = [q for s in _tube(ch["dip"], F[3], SEG[f][2], st, g,
                                h._cap(ch["dip"], F[3], SEG[f][2] * st[-1][0], ch["lens"][2],
                                       [x * g for x in st[-1][1:]])) for q in s]
        fig.poly(self._proj(pts, f), z=XRAY_Z, **XRAY_STYLE)

    def _record(self, layers, thumb_layer, th, chains, front, front_layer, ghost):
        """Measure what is drawn, for tools/check_hands.py: the front
        finger's segment lengths and thickness in a side view, and how much
        of the thumb shows."""
        rec = dict(context=CONTEXT[0], view=self.kind, ghost=ghost, tilt=self.tilt)
        # the thumb: points along its two visible segments, hidden if inside
        # anything drawn after (nearer than) it
        pts = [vlerp(th["mcp"], th["ip"], t) for t in (0.3, 0.6, 0.9)] + \
            [vlerp(th["ip"], th["tip"], t) for t in (0.2, 0.5, 0.8)]
        nearer = [q for L in layers[thumb_layer + 1:] for q in L[0]] if thumb_layer is not None else []
        vis = [not any(inside(self.xy(p), q) for q in nearer) for p in pts]
        rec["thumb"] = sum(vis) / len(vis) if thumb_layer is not None else 0.0
        # how long it is drawn, as a share of its length (a thumb pointing at
        # the viewer is a stump), and which joints sit at a limit that strains
        # them: right out from the hand, or bent back (flat against the hand
        # is where a thumb rests)
        drawn = length(sub(self.xy(th["ip"]), self.xy(th["mcp"]))) + \
            length(sub(self.xy(th["tip"]), self.xy(th["ip"])))
        rec["thumb_len"] = drawn / (THUMB_SEG[1] + THUMB_SEG[2])
        t = self.hand.t
        rec["thumb_limits"] = [j for j in ("ra", "pa") if t[j] > RANGE["t_" + j][1] - 0.5] + \
            [j for j in ("mcp", "ip") if t[j] < RANGE["t_" + j][0] + 0.5]
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
            for f, polys in getattr(self, "_behind", {}).items():
                nearer = [q for L in layers[self._behind_layer[f] + 1:] for q in L[0]]
                pts = []
                for q in polys:
                    c = (sum(x for x, _ in q) / len(q), sum(y for _, y in q) / len(q))
                    pts += [add(v, mul(norm(sub(c, v)), 0.12)) for v in q[::3]]
                vis = [not any(inside(v, q) for q in nearer) for v in pts]
                rec["behind"][f] = sum(vis) / max(len(vis), 1)
        RECORD.append(rec)

    def _thumb_base(self, fig, th, z):
        """Draw Hand.thumb_base, unless the thumb lies behind the palm, where
        the line would only double the hand's outline."""
        pts = self._poly(self.hand.thumb_base(th))
        if self.kind in ("back", "palm"):
            palm = self._proj(self.hand.palm_solid())
            mid = pts[len(pts) // 2]
            if not inside(mid, palm) or nearest(palm + palm[:1], mid)[0] < BASE_INSIDE ** 2:
                return
        fig.poly(pts, closed=False, z=z, sw=DETAIL, fill=None)

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


def _surface(slide, at):
    """A hold's surface as a page polyline: `slide` itself, or a straight
    line through `at` in page direction `slide` (degrees)."""
    if isinstance(slide, (int, float)):
        u = ang(slide)
        return [add(at, mul(u, -40.0)), add(at, mul(u, 40.0))]
    return list(slide)


def nearest(line, p):
    """Squared distance from page point p to polyline `line`, and the arc
    length along the line to the point nearest p."""
    best, s_best, s = 1e18, 0.0, 0.0
    for a, b in zip(line, line[1:]):
        ab = sub(b, a)
        L2 = dot(ab, ab)
        L = math.sqrt(L2)
        t = min(max(dot(sub(p, a), ab) / L2, 0.0), 1.0) if L2 else 0.0
        q = add(a, mul(ab, t))
        d2 = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
        if d2 < best:
            best, s_best = d2, s + t * L
        s += L
    return best, s_best


def snap(line, p):
    """The point of polyline `line` nearest page point p."""
    return point_along(line, nearest(line, p)[1])[0]


def point_along(line, s):
    """The point arc length s along polyline `line` (clamped to its ends)
    and the line's direction there."""
    for a, b in zip(line, line[1:]):
        L = length(sub(b, a))
        if s <= L or b is line[-1]:
            u = norm(sub(b, a))
            return add(a, mul(u, min(max(s, 0.0), L))), u
        s -= L


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


def profile_frame(x0=-10.0, y0=-9.0, y1=7.5, scale=HAND_SCALE, posed=None,
                  shown=FOREARM_SHOWN):
    """A close-up frame with the wall face at x = WX, cropped at the back of
    the wall's hatched strip. With a Posed hand whose forearm runs down out
    of the frame, the bottom edge instead cuts the arm `shown` cm below the
    wrist (y0 is then ignored)."""
    if posed is not None:
        y0 = posed.forearm_point(shown)[1]
    f = Fig(x0, y0, WX + 2.4 / scale + 0.01, y1, scale=scale)
    wall_profile(f, WX, y0, y1)
    return f


def outline(pts, tension):
    """The closed curve Fig.smooth draws through pts, as a page polyline
    from the first point round to the last (leaving out the stretch back to
    the first): a hold's surface for on_edge."""
    k = 8
    return Fig(0, 0, 1, 1)._smooth_pts(pts, True, tension, k)[:(len(pts) - 1) * k + 1]


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


# ---------------------------------------------------------------- standard grips in profile


def nail_point(hand, f="i", k=0.45, out=0.9):
    """A point on the nail of finger f, `out` cm from the bone axis."""
    ch = hand.finger(f)
    return vadd(vlerp(ch["dip"], ch["tip"], k), vmul(ch["frames"][3][1], out))


def on_edge(posed, at, fingers="mrl", k=0.8, dx=0.25, along=None, spread=None, slide=None,
            room=None):
    """Bend the fingers so that their pads also sit on the hold at page
    point `at` (an edge running into the page), each `dx` cm further along
    page x. With `spread`, they fan out along the hold's surface instead,
    each `spread` cm further than the one before it in page direction
    `along` (degrees), so that every fingertip shows beside the first.

    A finger that can't reach its spot, or reaches it only by bending far
    from the grip (the little finger, mostly: it is the shortest), slides
    along the hold's surface instead (Posed.reach): `slide` is that
    surface, a page direction (default `along`) or a page polyline, and
    `room` the range in cm along it from `at` that the hold covers. On a
    polyline the fingers' spots also fan out along it, `spread` cm apart
    the way `along` points."""
    s = slide if slide is not None else along if spread is not None else None
    line = _surface(s, at) if s is not None else None
    if line and spread is not None and not isinstance(s, (int, float)):
        s_at = nearest(line, at)[1]
        sgn = 1 if dot(point_along(line, s_at)[1], ang(along or 0.0)) >= 0 else -1
    for i, f in enumerate(fingers):
        if spread is None:
            t = add(at, (dx, 0))
        elif line and not isinstance(s, (int, float)):
            t = point_along(line, s_at + sgn * spread * (i + 1))[0]
        else:
            t = add(at, mul(ang(along or 0.0), spread * (i + 1)))
        f0 = posed.hand.f[f]
        miss = posed.reach(f, t, k=k)
        bent = sum(abs(a - b) for a, b in zip(f0[:3], posed.hand.f[f][:3]))
        if line and (miss > 0.05 or bent > SLIDE_BEND):
            posed.hand.f[f] = f0
            a = nearest(line, t)[1] - nearest(line, at)[1]
            posed.reach(f, t, k=k, slide=line, room=room and (room[0] - a, room[1] - a))


# the holds of the profile grips, on a wall at x = WX with their tops at y = 0
GRIP_HOLD = {"open": (lip_pts, rounded_lip, 0.8, dict(depth=2.6, height=4.2)),
             "half": (edge_pts, edge_profile, 0.35, dict(depth=2.0, height=2.6)),
             "full": (edge_pts, edge_profile, 0.35, dict(depth=0.8, height=2.0, slope=-12))}


def grip_hold(fig, kind):
    """The hold for a profile grip on a wall at x = WX, its top at y = 0: a
    rounded edge ('open'), a flat edge ('half') or a small incut edge."""
    GRIP_HOLD[kind][1](fig, WX, 0, **GRIP_HOLD[kind][3])


def grip_surface(kind):
    """The surface of grip_hold's hold, as a page polyline (see on_edge)."""
    pts, _, tension, kw = GRIP_HOLD[kind]
    return outline(pts(WX, 0, **kw), tension)


def grip_pose(kind, tilt=TILT):
    """The hand for a profile grip on the hold from grip_hold, seen from the
    thumb side with the arm hanging below the hold: 'open' (drag), 'half'
    (half crimp), 'full' (full crimp) or 'lock' (full crimp, the thumb over
    the index nail). The thumb rests unless the grip uses it. Returns the
    Posed."""
    hold = kind if kind in ("open", "half") else "full"
    surf = grip_surface(hold)
    if kind == "open":
        h = Hand("open")
        pad, k, a0 = snap(surf, (WX - 1.25, 0.0)), 0.6, 94
        along, spread, room = 172, 0.4, (-0.8, 2.6)
    elif kind == "half":
        h = Hand("half")
        # the middle and end segments flat on the edge, as in photographs,
        # far enough out on it that the forearm hangs clear of the wall
        pad, k, a0 = (WX - 1.3, 0.0), 0.85, 97
        along, spread, room = 180, 0.36, (-0.6, 1.1)
    else:
        h = Hand("full", fingers={"i": (45, 95, -20)} if kind == "lock" else None)
        pad, k, a0 = snap(surf, (WX - 0.55, 0.1)), 0.9, 95
        along, spread, room = 168, 0.08, (-0.3, 0.24)
    p = h.view("thumb", tilt=tilt).place("i", pad, a0=a0, k=k)
    # the other fingers on the same hold, fanned out toward its front so
    # that their tips show beside the index finger's
    on_edge(p, pad, k=k, along=along, spread=spread, slide=surf, room=room)
    if kind == "open":
        # the little finger, too short to reach over the lip, rests on its
        # front with its tip against the surface, not inside the hold
        p.reach("l", (WX - 2.3, -0.75), k=0.85, slide=surf, room=(-0.5, 0.5))
    if kind == "lock":
        n = nail_point(h, k=0.3)
        # the pad near the thumb tip, so the tip ends at the wall, not in it
        p.thumb_to(p.xy(n), part="pad", k=0.85, depth=p.depth(n))
    else:
        # the thumb rests clear of the middle and end joints, the angle
        # arcs and the edge, which these views exist to show
        tuck_thumb(p, kind)
    return p


def tuck_thumb(posed, kind, drop=0.0):
    """Rest the thumb of a drag ('open'), half crimp ('half') or full crimp
    ('full') profile clear of the index finger's middle and end joints and
    of the edge. In the crimps it rests against the index finger, its pad
    on the palm side of the first segment near the knuckle, pointing along
    it, `drop` cm further toward the palm; in the drag it hangs low along the
    palm side."""
    if kind in ("half", "full"):
        ch = posed.hand.finger("i")
        A1, N1, L1 = ch["frames"][1]
        pt = vadd(vadd(vlerp(ch["mcp"], ch["pip"], 0.15), vmul(L1, 0.6)),
                  vadd(vmul(N1, -0.8), vmul(A1, -drop)))
        posed.thumb_to(posed.xy(pt), part="pad", k=0.7, depth=posed.depth(pt))
    else:
        posed.thumb_to((WX - 3.0, -3.8), part="tip")


def grip_profile(kind, z=0, x0=-12.0, y1=8.6, height=None, scale=HAND_SCALE,
                 shown=FOREARM_SHOWN, plain=()):
    """A side-profile panel of a grip (see grip_pose), from x0 to the wall and
    from where it cuts the forearm (`shown` cm below the wrist) up to y1, or
    `height` cm up; plain as in Posed.draw. Returns the figure and the Posed
    hand."""
    p = grip_pose(kind)
    if height is not None:
        y1 = p.forearm_point(shown)[1] + height
    f = profile_frame(x0, y1=y1, scale=scale, posed=p, shown=shown)
    grip_hold(f, "open" if kind == "open" else "half" if kind == "half" else "full")
    p.draw(f, z=z, plain=plain)
    return f, p


def a2_point(posed, f="i"):
    """Where the A2 pulley lies, for a label: on the palm side of the
    finger's first segment, a little short of its middle."""
    ch = posed.hand.finger(f)
    A, N, L = ch["frames"][1]
    c = vadd(ch["mcp"], vmul(A, SEG[f][0] * 0.45))
    return posed.xy(vadd(c, vmul(N, -0.82 * GIRTH[f])))
