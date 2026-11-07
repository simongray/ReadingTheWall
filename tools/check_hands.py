"""Check every hand close-up as the book draws it, against research/hand-proportions.md.

Usage: python3 tools/check_hands.py [--table]

This builds all the figures in a temporary folder and records each call of draw_hand, and
of handmodel.draw, so no hand or figure can be left out. For an authored hand it reads the
outline from the pen's path and measures it in cm of a hand 19 cm long; a hand's joints only
say where to measure. A hand from handmodel.py is checked through the model: its bones, its
joints' ranges, its scale, and the same chords measured on the solids its outline is traced
from. It exits with status 1 if a measure is out of range, and --table prints every number.
Look at the figures as well: a hand must look right before it measures right, and contact
with the rock isn't tested.
"""
import contextlib
import glob
import importlib
import io
import math
import os
import re
import statistics
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "figtools"))

import climb  # noqa: E402
import authored as A  # noqa: E402
import handmodel as HM  # noqa: E402
from climb import sub, dot, perp, norm as unit  # noqa: E402

STEP = 0.1          # cm between the stations along a digit
TIP = 0.2           # cm: no chord this close to a digit's end
CAP = 3.0           # cm: a wider chord across a digit has lost one of its sides
MID_PALM = 4.5      # cm above the wrist crease
ARM_BELOW = 5.0     # cm below the wrist joint
FINGER = 1.9        # cm: a ratio may miss by what the pen's wobble does to a finger this wide
STROKE = 0.015      # mm: a stroke's width is written to two decimals of a cm
RING = 0.03         # mm: each side of a filled line is written to two decimals of a cm

# ---------------------------------------------------------------- the ranges
#
# (low, high) from research/hand-proportions.md, which has the sources. A chord may also
# miss by the most the pen's wobble can move it, so no range here is widened by hand.
# f1-f3 are the finger's three segments, and t1 and t2 are the thumb's two free ones.

SIDE = {
    "f1": (1.75, 2.25),     # index depth at its middle joint, up to a finger's width at its base
    "f2": (1.55, 1.73),     # halfway from that joint to the end joint
    "f3": (1.2, 1.5),       # the depth at the end joint, down to the tip's
    "flen": (8.54, 9.68),   # the index along its back, up to the middle finger that stands behind it
    "t1": (1.9, 2.4),       # thumb at its end joint: AIST 2.08, US surveys 2.4
    "t2": (1.8, 2.25),      # its tip at mid-nail, up to the US thumb halfway to the tip
    "tlen": (4.7, 6.3),     # free of the palm 5-5.5, less 0.3 for posture, up to all of it from its crease
    "mid-palm": (4.5, 4.9),     # with the ball of the thumb
    "knuckles": (2.86, 3.33),   # index knuckle to middle knuckle
    "wrist": (4.2, 4.6),    # deeper than the knuckles: in profile a wrist is no waist
    "forearm": (4.6, 5.2),  # estimated from girths, since no survey here measures it
    "f/palm": (0.36, 0.43),     # finger at its middle joint against the palm with the ball
    "f/body": (0.94, 1.06),     # the index's and middle finger's back length against knuckle to crease, 9.1
    "t/f": (1.05, 1.2),     # thumb's breadth against finger's depth
    "tlen/flen": (0.52, 0.67),  # free thumb 5 against middle finger 9.68, whole thumb 5.71 against index 8.54
}
LITTLE = dict(SIDE, **{     # from the little-finger side, with no ball of the thumb in front
    "f1": (1.49, 1.91), "f2": (1.32, 1.47), "f3": (1.02, 1.28),     # the side's x 0.85, little against index depth
    "flen": (6.11, 7.15),   # the little finger's palm-side length, up to its back length
    "mid-palm": (3.4, 3.9),     # mid-palm up to the outer heel
    "f/palm": (0.43, 0.49),     # the index's 0.51-0.57 x 0.85
    "f/body": (0.67, 0.79),     # those two lengths against 9.1
    "t/f": (1.24, 1.41),    # the side's, over 0.85
    "tlen/flen": (0.7, 0.93),   # free thumb against its back length, whole thumb against its palm-side length
})
BACK = {
    "f1": (1.9, 2.25),      # index breadth at its middle joint, up to a finger's share of the knuckles
    "f2": (1.75, 2.03),     # halfway from that joint to the end joint
    "f3": (1.44, 1.85),     # the breadth at the end joint, down to the tip's
    "flen": (8.24, 9.68),   # middle finger from the palm side, up to its back length
    "t1": (1.8, 2.1),       # the thumb seen edge-on
    "t2": (1.7, 2.0),       # the same, less its taper
    "tlen": (4.7, 6.3),     # as from the side
    "mid-palm": (8.2, 9.35),    # 8.2-8.5 alone, up to half of what the thumb adds at its knuckle, 2.16
    "knuckles": (8.5, 9.0),     # AIST 8.63, US surveys 8.5-8.97
    "wrist": (6.0, 6.6),    # seven tenths of the knuckles: from the back a wrist is a waist
    "forearm": (6.7, 7.2),  # estimated from girths
    "webs": (9.9, 10.9),    # the mean of the webs: 10.4 from the palm lengths, +-0.5 as no survey measures them
    "f/palm": (0.21, 0.26),     # between a fifth and a quarter of the knuckles
    "f/body": (0.7, 0.77),  # middle finger's palm-side length against the palm
    "t/f": (0.85, 1.05),    # about 0.95, edge-on
    "tlen/flen": (0.52, 0.69),  # free thumb 5 against middle finger 9.68, and against 7.4 foreshortened
}
PRESS = dict(BACK, **{      # the palm press, three quarters on: its column in the reference, along the hand x 0.92
    "f1": (1.85, 2.1), "f2": (1.72, 1.95), "f3": (1.4, 1.8), "flen": (7.58, 8.9),
    "t1": (1.9, 2.2), "t2": (1.8, 2.1), "tlen": (4.3, 5.8),
    "mid-palm": (7.9, 9.15), "knuckles": (8.3, 8.7), "wrist": (5.8, 6.7), "forearm": (6.2, 6.7),
    "webs": (9.1, 10.05), "f/palm": (0.21, 0.25), "t/f": (0.9, 1.1),
})
TURNED = dict(BACK, **{     # the wrap: breadth x 0.84 and depth x 0.54, by the reference's formula for a section
    "f1": (1.86, 2.2), "f2": (1.72, 1.99), "f3": (1.37, 1.76), "t1": (1.9, 2.4), "t2": (1.8, 2.25),
    "mid-palm": (7.5, 7.75), "knuckles": (7.75, 8.2), "wrist": (5.5, 6.6), "forearm": (6.15, 7.25),
    "f/palm": (0.22, 0.27), "t/f": (1.05, 1.2),     # the thumb's back shows, as from the side
})
VIEWS = dict(PALM=PRESS, WRAP=TURNED)
GIRTH = dict(i=1.0, m=1.01, r=0.94, l=0.83)     # a finger's breadth against the index's (AIST)
REACH = dict(i=0.897, m=1.0, r=0.937, l=0.741)  # its length against the middle finger's (AIST)

# Where a part is hidden, foreshortened or spread across a chord, that measure can't be read.
# Nothing else goes here.
SKIP = {
    "JUG": ("i1", "f/palm", "t/f"),         # the thumb hides the finger's first segment
    "LATCH_JUG": ("i1", "f/palm", "t/f"),   # the thumb hides the finger's first segment
    "FULL": ("i3",),                        # the thumb covers the end segment
    "PALM": ("mid-palm",),                  # the spread thumb's base is in the chord
    "BACK_DRAG3": ("l2", "l3"),             # the little finger curls away and only its first segment shows
    "POCKET_CURLED": ("l1",),               # foreshortened, so the chord takes in the knuckle
    "WRAP": ("webs",),                      # the slits run back into the hand, so the forks aren't its webs
    "FILM_THUMB": ("t/f",),                 # its base widens into the palm, so the chord there isn't the thumb's
    "FILM_HANG": ("t/f",),                  # its base widens into the palm, so the chord there isn't the thumb's
}
# The thumb stands off the palm: the mid-palm chord runs up it and its length runs to its web.
THUMB_OFF = ("PINCH", "PINCH_WIDE", "PINCH_RIDGE", "FILM_THUMB", "FILM_HANG")
# These fingers may look short, but never long.
SHORT_FINGER = (
    "BACK_DRAG", "BACK_DRAG3",  # they go on away from you over the edge
    "BACK_CRIMP",               # they bend away at their middle joints
    "WRAP",                     # they turn round the arête
    "FULL",                     # curled, with the end under the thumb
    "JUG", "LATCH_JUG",         # the thumb hides part of the finger
    "PINCH_WIDE",               # its base runs into the palm, with no far side to measure
)


# ---------------------------------------------------------------- plane geometry

def along(p, u, t):
    return (p[0] + u[0] * t, p[1] + u[1] * t)


def segments(paths, closed=True):
    out = []
    for P in paths:
        out += list(zip(P, P[1:] + P[:1] if closed else P[1:]))
    return out


def crossings(o, u, segs):
    """Where the line through o along u crosses the segments: signed distances, sorted."""
    out = []
    for a, b in segs:
        d = sub(b, a)
        den = u[0] * d[1] - u[1] * d[0]
        if abs(den) > 1e-12:
            r = sub(a, o)
            w = (r[0] * u[1] - r[1] * u[0]) / den
            if 0.0 <= w < 1.0:
                out.append((r[0] * d[1] - r[1] * d[0]) / den)
    return sorted(out)


def inside(q, segs):
    # along no axis, or the ray can run down a piece of a path rounded to two decimals
    return sum(t > 0 for t in crossings(q, (0.8191, 0.5736), segs)) % 2 == 1


def span(o, u, segs):
    """The filled stretch of the line through o that holds o, or the nearest: its two ends."""
    ts = crossings(o, u, segs)
    runs = list(zip(ts[::2], ts[1::2]))
    if not runs:
        return None
    return min(runs, key=lambda r: 0.0 if r[0] <= 0.0 <= r[1] else min(abs(r[0]), abs(r[1])))


def between(o, u, segs):
    """The distance between the nearest drawn lines either side of o."""
    ts = crossings(o, u, segs)
    lo, hi = [t for t in ts if t <= 0.0], [t for t in ts if t > 0.0]
    return hi[0] - lo[-1] if lo and hi else None


def stretch(P, p, q):
    """The part of a closed outline between the points nearest p and q, the short way."""
    a, b = (min(range(len(P)), key=lambda i: math.dist(P[i], x)) for x in (p, q))
    a, b = (a, b) if (b - a) % len(P) < (a - b) % len(P) else (b, a)
    return [P[(a + i) % len(P)] for i in range((b - a) % len(P) + 1)]


def gap(q, segs):
    """How far q lies from the nearest segment."""
    best = math.inf
    for a, b in segs:
        v = sub(b, a)
        L = dot(v, v)
        t = max(0.0, min(1.0, dot(sub(q, a), v) / L)) if L else 0.0
        best = min(best, math.dist(q, along(a, v, t)))
    return best


def bends(chain):
    """The bend at each joint of a chain, in degrees."""
    out = [0.0]
    for a, b, c in zip(chain, chain[1:], chain[2:]):
        u, v = unit(sub(b, a)), unit(sub(c, b))
        out.append(math.degrees(math.acos(max(-1.0, min(1.0, dot(u, v))))))
    return out


# ---------------------------------------------------------------- what the pen drew

PATH = re.compile(r'<path d="([^"]*)"([^>]*)/>')
WIDTH = re.compile(r'stroke-width="([\d.]+)"')


def flatten(d, k=2):
    """A path's d attribute as lists of points. Fig writes absolute M, L, C and Z. k: the
    points kept along each curve, whose pieces are short enough to be nearly straight."""
    out = []
    for part in re.findall(r"M[^M]*", d):
        n = [float(v) for v in re.findall(r"-?\d*\.?\d+(?:[eE][-+]?\d+)?", part)]
        P, i = [(n[0], n[1])], 2
        while "C" in part and i < len(n):
            a, b, c, e = P[-1], (n[i], n[i + 1]), (n[i + 2], n[i + 3]), (n[i + 4], n[i + 5])
            for j in range(1, k + 1):
                t = j / k
                w = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
                P.append(tuple(w[0] * a[x] + w[1] * b[x] + w[2] * c[x] + w[3] * e[x] for x in (0, 1)))
            i += 6
        out.append(P if "C" in part else P + list(zip(n[2::2], n[3::2])))
    return out


def read(f, hand, items):
    """What one draw_hand added to figure f, in the hand's cm. A pen line comes as a ring
    round both its sides, its first half running out and its second half back."""
    def world(P):
        return [(x + f.x0, f.y1 - y) for x, y in P]
    d = dict(hand=hand, fig=f, loops=[], grey=[], rings=[], grey_sw=[])
    for _, _, svg in items:
        path, attrs = PATH.match(svg).groups()
        sw = WIDTH.search(attrs)
        if 'fill-rule="evenodd"' in attrs and sw:
            d.update(loops=[world(P) for P in flatten(path)], stroke=float(sw.group(1)), path=path,
                     ghost="stroke-dasharray" in attrs)
        elif sw:
            d["grey_sw"].append(float(sw.group(1)))
        elif 'fill-rule="evenodd"' in attrs:
            d["grey"] += [world(P) for P in flatten(path)]
        else:
            d["rings"].append(world(flatten(path, 1)[0][:-1]))
    n = len(hand.get("solid", ())) + len(hand.get("lines", ()))
    d["lines"] = [[((a[0] + b[0]) / 2, (a[1] + b[1]) / 2) for a, b in zip(V, V[::-1])][:len(V) // 2]
                  for V in d["rings"][:n]]
    d["inner_rings"], d["marks"] = d["rings"][:n], d["rings"][n:]
    return d


def record():
    """Build every figure. Returns each drawn hand with the figure and paper scale it landed
    on, and the weights the climbers are drawn at."""
    names, drawn, solid, ghost = {}, [], [], []
    for name, v in vars(A).items():
        if isinstance(v, dict) and "outline" in v and not name.startswith("_"):
            names.setdefault(id(v), name)
    draw, moved, climber = A.draw_hand, A.moved, climb.Climber.draw

    def spy(f, hand, *a, **k):
        n = len(f.items)
        draw(f, hand, *a, **k)
        drawn.append(dict(read(f, hand, f.items[n:]), name=hand.get("name") or names.get(id(hand), "?")))

    def spy_moved(hand, *a, **k):
        return dict(moved(hand, *a, **k), name=hand.get("name") or names.get(id(hand)))

    def spy_climber(self, f, *a, **k):
        n = len(f.items)
        out = climber(self, f, *a, **k)
        for _, _, svg in f.items[n:]:
            m = WIDTH.search(svg)
            if m:
                (ghost if climb.GHOST_LINE in svg else solid).append(round(float(m.group(1)) * f.scale, 2))
        return out
    model_draw = HM.draw

    def spy_model(f, hand, *a, **k):
        n = len(f.items)
        model_draw(f, hand, *a, **k)
        d = dict(hand=hand, fig=f, model=True, name=hand.name or "?", ghost=k.get("ghost", False))
        for _, _, svg in f.items[n:]:
            m = PATH.match(svg)
            sw = WIDTH.search(svg)
            if m and sw and 'fill-rule="evenodd"' in svg:
                d.update(path=m.group(1), stroke=float(sw.group(1)))
                break
        drawn.append(d)
    A.draw_hand, A.moved, climb.Climber.draw, HM.draw = spy, spy_moved, spy_climber, spy_model
    with tempfile.TemporaryDirectory() as out, contextlib.redirect_stdout(io.StringIO()):
        for p in sorted(glob.glob(os.path.join(ROOT, "figtools", "figs_*.py"))):
            importlib.import_module(os.path.basename(p)[:-3]).build(out)
        svgs = {os.path.basename(p)[:-4]: open(p).read() for p in glob.glob(out + "/*.svg")}
    for d in drawn:
        d["figure"], d["paper"] = "not placed", d["fig"].scale
        for fig, text in svgs.items():
            at = text.find(d["path"])
            if at >= 0:
                g = re.findall(r' scale\(([\d.]+)\)', text[:at])
                d["figure"], d["paper"] = fig, float(g[-1]) if g else d["fig"].scale
                break
    # a climber's outline is drawn at twice its weight, and its fill hides half
    weights = dict(outline=statistics.mode(solid) / 2, ghost=statistics.mode(ghost) / 2, hem=climb.LINE_SW)
    return drawn, weights


# ---------------------------------------------------------------- measuring

def walk(chain, lines, is_in, hidden=lambda q: False, begins=False):
    """Stations down a digit from its tip: [(arc length, chord or None, seen)], with the
    joints' arc lengths and the drawn tip. A bent joint has no chord that means anything
    but still shows. begins: where the chords go over CAP the thumb runs into the hand, and
    nothing below that counts. One such chord may only have slipped through the fork."""
    u = unit(sub(chain[3], chain[2]))
    L = math.dist(chain[2], chain[3])
    ts = [t for t in crossings(chain[2], u, lines) if t > 0.2]
    t = min(ts, key=lambda v: abs(v - L)) if ts else L
    pts = chain[:3] + [along(chain[2], u, t) if abs(t - L) < 1.5 else chain[3]]
    arc = [0.0]
    for a, b in zip(pts, pts[1:]):
        arc.append(arc[-1] + math.dist(a, b))
    bent = bends(pts)
    near = [(arc[1], 0.75 if bent[1] > 50 else 0.0), (arc[2], 0.6 if bent[2] > 30 else 0.0)]
    out, s, over = [], arc[-1] - TIP, 0
    while s >= 0.0:
        i = next(k for k in range(3) if s <= arc[k + 1] or k == 2)
        v = unit(sub(pts[i + 1], pts[i]))
        q = along(pts[i], v, s - arc[i])
        c, seen = None, False
        if (begins and over >= 3) or hidden(q) or not is_in(q):
            pass
        elif any(abs(s - a) < r for a, r in near):
            seen = True
        else:
            c = between(q, perp(v), lines)
            if c is None or c > CAP:
                over, c = over + 1, None
            else:
                over, seen = 0, True
        out.append((s, c, seen))
        s -= STEP
    return out, arc, pts[-1]


def middle(stations, a, b):
    """The chord at the middle of a segment's visible part."""
    c = [x[1] for x in stations if a <= x[0] <= b and x[1] is not None]
    return c[len(c) // 2] if c else None


def measure(d):
    """Every number the ranges test, for one drawn hand."""
    j = d["hand"]["joints"]
    loops = segments(d["loops"])
    lines = loops + segments(d["lines"], closed=False)
    grey = segments(d["grey"])
    c, hd, ad = j["crease"], unit(j["hand_dir"]), unit(j["arm_dir"])
    n = perp(hd)
    is_hand = lambda q: inside(q, loops)
    behind = j.get("thumb_front", True) is False
    m, tips = {}, {}

    def on_thumb(q):
        """Under the thumb where it lies over a finger: within a capsule round its joints."""
        for a, b in zip(j["t"][1:], j["t"][2:]):
            v = sub(b, a)
            if math.dist(q, along(a, v, max(0.0, min(1.0, dot(sub(q, a), v) / dot(v, v))))) < 0.9:
                return True
        return False
    for k in "imrl":
        if k in j:
            st, s, tips[k] = walk(j[k], lines, is_hand, (lambda q: False) if behind else on_thumb)
            for i in (1, 2, 3):
                m[f"{k}{i}"] = middle(st, s[i - 1], s[i])
            m[k + "len"] = TIP + sum(x[2] for x in st) * STEP
    if behind:     # the thumb in grey behind the hand
        st, s, tip = walk(j["t"], grey + loops, lambda q: inside(q, grey), is_hand, begins=True)
    else:
        st, s, tip = walk(j["t"], lines, is_hand, begins=True)
    m["t1"], m["t2"] = middle(st, s[1], s[2]), middle(st, s[2], s[3])
    seen = [x[0] for x in st if x[1] is not None]
    m["tlen"] = s[3] - min(seen) if seen else None

    front = j.get("front") or "m"
    P = max(d["loops"], key=len)
    if d["name"] in THUMB_OFF:
        u = unit(sub(tip, j["t"][1]))
        m["tlen"] = max(dot(sub(tip, q), u) for q in stretch(P, tip, tips[front]))
    m["body"] = dot(sub(j[front][0], c), hd)
    if j.get("view") == "back":
        # across the knuckles: out to the little finger's edge and in to the thumb's line
        row = tuple(sum(j[k][0][i] for k in "imrl") / 4 for i in (0, 1))
        u = unit(j["across"])
        out = 1 if dot(sub(j["t"][3], row), u) > 0 else -1
        ts = [t * out for t in crossings(row, u, lines)]
        m["knuckles"] = min(t for t in ts if t > 0) - min(ts)
        # how far above the crease the outline comes down between each pair of fingertips
        m["webs"] = statistics.fmean(min(dot(sub(q, c), hd) for q in stretch(P, tips[a], tips[b]))
                                     for a, b in ("im", "mr", "rl"))
    else:
        # a bent knuckle or a thumb across it leaves no depth to read
        o = j[front][0]
        lo, hi = span(o, n, loops)
        over = any(lo < t < hi for t in crossings(o, n, segments([j["t"]], closed=False)))
        straight = bends([along(o, hd, -1.0), o, j[front][1]])[1] < 30
        m["knuckles"] = hi - lo if straight and not over else None
    lo, hi = span(along(c, hd, MID_PALM), n, loops)
    m["mid-palm"] = hi - lo

    def width(t):
        """Across the arm t cm from the wrist joint, on an axis that turns from hand to arm.
        The arm leaves the frame, and only what shows can be measured."""
        k = max(0.0, min(1.0, (t + 1.2) / 2.4))
        k = k * k * (3 - 2 * k)
        u = perp(unit((hd[0] * k + ad[0] * (1 - k), hd[1] * k + ad[1] * (1 - k))))
        q = along(j["wrist"], hd if t >= 0 else ad, t)
        run = span(q, u, loops)
        f = d["fig"]
        if run is None or not all(f.x0 - 1 <= e[0] <= f.x1 + 1 and f.y0 - 1 <= e[1] <= f.y1 + 1
                                  for e in (along(q, u, run[0]), along(q, u, run[1]))):
            return None
        return run[1] - run[0]
    m["wrist"], m["forearm"] = width(0.0), width(-ARM_BELOW)
    return m


def check(d, climbers):
    """[(measure, value, low, high, in range)] for one drawn hand."""
    name, j = d["name"], d["hand"]["joints"]
    p = d["paper"]
    rows = []

    def weight(key, v, want, tol):
        rows.append((key, v, want, want, abs(v - want) <= tol))
    weight("outline mm", d["stroke"] * p, climbers["ghost" if d["ghost"] else "outline"], STROKE)
    for sw in d["grey_sw"]:
        weight("back line mm", sw * p, climbers["hem"], STROKE)
    for V in d["inner_rings"]:
        weight("inner line mm", math.dist(V[0], V[-1]) * p, climbers["outline"], RING)
    for V in d["marks"]:
        h = (len(V) - 6) // 2     # the fine ribbon: one side, three round its end, the other, three more
        w = [math.dist(V[i], V[2 * h + 2 - i]) for i in range(h // 3, 2 * h // 3 + 1)]
        weight("mark mm", statistics.median(w) * p, climbers["hem"], RING)
    if d["ghost"]:      # a dashed copy of a hand drawn solid elsewhere, with no inner lines to read
        return rows

    back = j.get("view") == "back"
    view = VIEWS.get(name) or (BACK if back else LITTLE if j.get("view") == "little" else SIDE)
    skip = SKIP.get(name, ()) + (("mid-palm", "f/palm") if name in THUMB_OFF else ())
    short = name in SHORT_FINGER
    m = measure(d)
    pen = 2 * climb.WOBBLE / d["fig"].scale

    def test(key, v, r, tol, low=True, high=True):
        if v is not None and key not in skip:
            rows.append((key, v, r[0], r[1], (not low or v >= r[0] - tol) and (not high or v <= r[1] + tol)))
    for k in "imrl" if back else j["front"]:
        for i in "123":
            test(k + i, m[f"{k}{i}"], [v * (GIRTH[k] if back else 1) for v in view["f" + i]], pen)
        test(k + "len", m[k + "len"], [v * (REACH[k] if back else 1) for v in view["flen"]], pen + STEP, low=not short)
    for key in ("t1", "t2", "mid-palm", "knuckles", "wrist", "forearm", "webs"):
        if key in view:
            test(key, m.get(key), view[key], pen)
    test("tlen", m["tlen"], view["tlen"], pen + STEP)

    def ratio(key, a, b, **k):
        if a and b:
            test(key, a / b, view[key], pen / FINGER * sum(view[key]) / 2, **k)

    def mean(*vs):
        vs = [v for v in vs if v is not None]
        return sum(vs) / len(vs) if vs else None
    near, far = ("i", "m") if back else (j["front"], j["front"])
    finger = mean(m[near + "1"], m[near + "2"])     # at its middle joint, between the two segments it joins
    ratio("f/palm", finger, m["knuckles"] if back else m["mid-palm"])
    ratio("f/body", m[far + "len"], m["webs"] if back else m["body"], low=not short)
    ratio("t/f", mean(m["t1"], m["t2"]), finger)
    ratio("tlen/flen", m["tlen"], m[far + "len"], high=not short)

    # the nails and the other slight details stay on the hand
    hand, grey = segments(d["loops"]), segments(d["grey"])
    for V in d["marks"]:
        out = max((gap(q, hand + grey) for q in V if not inside(q, hand) and not inside(q, grey)), default=0.0)
        rows.append(("mark past outline", out, 0.0, d["stroke"] / 2, out <= d["stroke"] / 2))

    # a line across the thumb below its end joint would read as an extra joint
    thumb = j["t"][:3]
    axis = unit(sub(thumb[2], thumb[0]))
    across = sum(abs(dot(unit(sub(b, a)), axis)) < 0.7
                 and any(0.0 <= t <= math.dist(a, b) for t in crossings(a, unit(sub(b, a)), segments([thumb], False)))
                 for a, b in segments(d["lines"] + d["marks"], closed=False) if a != b)
    rows.append(("lines across thumb", float(across), 0.0, 0.0, across == 0))
    return rows


# ---------------------------------------------------------------- the model's hands
#
# A model hand's outline is traced from its solids, so the chords are measured on those
# solids' fields, in the hand's own cm, square to each part, as the side view shows them.

# The thumb seen from the side, from its tip to the ball of the thumb: at least the free thumb
# (SIDE's tlen, 4.7), up to the whole thumb from its crease (6.3, Kouchi 2012) and the knuckle
# below it, which the outline runs past (about 0.7 more)
THUMB_SEEN = (4.7, 7.0)
# its drawn edge runs at least as far; where the thumb stands off the palm the outline may
# carry it down to its base joint, the whole thumb, 10.5
THUMB_DRAWN = (4.7, 10.5)
# each joint's range, in degrees of flexion (negative bends back): hands-drawing-reference.md
JOINTS = dict(mcp=(-45, 90), pip=(0, 120), dip=(-30, 80), wrist=(-70, 80),
              t_mcp=(-8, 60), t_ip=(-12, 88))


def chord(hand, piece, at, along):
    """The width of a piece's solids through `at`, square to the direction `along`."""
    g = hand.grid
    F = hand.own[piece] if isinstance(piece, str) else piece
    n = perp(unit(along))
    inside = lambda t: g.at(F, (at[0] + n[0] * t / 50, at[1] + n[1] * t / 50)) < 0
    if not inside(0):
        return None
    lo = hi = 0     # the run through `at` only: a folded finger's other segment isn't this one's
    while lo > -300 and inside(lo - 1):
        lo -= 1
    while hi < 300 and inside(hi + 1):
        hi += 1
    return (hi - lo) / 50


def measure_model(hand):
    """The side view's measures of a model hand, in cm."""
    if not hasattr(hand, "grid"):
        hand.build()
    s, m = hand.skel, {}
    J = [hand.flat(j) for j in s.joints("i")]
    g = hand.grid
    for i, solid in enumerate(hand.P["i"]):
        # each segment's own solid: in a curled finger the next segment lies across the chord
        F = [[solid.field(g.x0 + a * g.s, g.y0 + b * g.s) for a in range(g.nx)] for b in range(g.ny)]
        mid = ((J[i][0] + J[i + 1][0]) / 2, (J[i][1] + J[i + 1][1]) / 2)
        m[f"f{i + 1}"] = chord(hand, F, mid, sub(J[i + 1], J[i]))
    T = [hand.flat(j) for j in s.joints("t")]
    m["t1"] = chord(hand, "t", T[2], sub(T[3], T[1]))
    f, L = s.digits["t"][2]
    m["t2"] = chord(hand, "t", hand.flat(f.at(L * 0.55, 0, 0)), sub(T[3], T[2]))
    c = hand.flat(s.H((0, 0, 0)))
    up = unit(sub(hand.flat(s.H((0, 1, 0))), c))
    palm = hand.own["palm"]
    m["mid-palm"] = chord(hand, palm, (c[0] + up[0] * MID_PALM, c[1] + up[1] * MID_PALM), up)
    m["wrist"] = chord(hand, palm, c, up)
    down = unit(sub(hand.flat((0.0, -1.0, 0.0)), hand.flat((0.0, 0.0, 0.0))))
    m["forearm"] = chord(hand, palm, (c[0] + down[0] * ARM_BELOW, c[1] + down[1] * ARM_BELOW), down)
    # how much thumb shows: from its tip down to where its outline melts into the ball of the
    # thumb. A thumb that turns toward you, or melts away too soon, comes out a stub
    mc, Lm = s.digits["t"][0]
    m["thumb seen"] = math.dist(hand.flat(mc.at(Lm * HM.ROOT["t"], 0, 0)), T[3])
    # and how far down from the tip the drawing really carries the thumb's edge: its lines
    # and the stretch of the outline that is the thumb's
    order = HM.ORDER[hand.view]
    body = [n for n in order if n not in HM.GREYS[hand.view] and n != "t"]
    edge = [q for pts, _ in HM.thumb_outline(hand, HM.union(hand, body)) for q in pts]
    axis = unit(sub(T[3], hand.flat(mc.o)))
    m["thumb drawn"] = max(dot(sub(T[3], q), axis) for q in edge) if edge else 0.0
    return m


def check_model(d, climbers):
    """[(measure, value, low, high, in range)] for one hand from the model."""
    hand, p = d["hand"], d["paper"]
    rows = []
    want = climbers["ghost" if d["ghost"] else "outline"]
    rows.append(("outline mm", d["stroke"] * p, want, want, abs(d["stroke"] * p - want) <= STROKE))
    if d["ghost"]:
        return rows
    # one hand: the bones of every pose are the model's
    same = HM.bones(hand) == HM.bones(HM.Hand(HM.default_pose()))
    rows.append(("same bones", float(same), 1.0, 1.0, same))
    # the close-ups' scale, before a plate is reduced
    rows.append(("mm per cm", d["fig"].scale, HM.H.HAND_SCALE, HM.H.HAND_SCALE,
                 abs(d["fig"].scale - HM.H.HAND_SCALE) < 1e-9))
    P = hand.skel.pose
    for k in "imrl":
        mcp, pip, dip = P[k]
        dip = HM.dip_of(pip, dip)
        for key, v in (("mcp", mcp), ("pip", pip), ("dip", dip)):
            lo, hi = JOINTS[key]
            rows.append((f"{k} {key}", float(v), lo, hi, lo <= v <= hi))
    lo, hi = JOINTS["wrist"]
    rows.append(("wrist", float(P["wrist"][0]), lo, hi, lo <= P["wrist"][0] <= hi))
    for key, v in (("t_mcp", P["thumb"]["mcp"]), ("t_ip", P["thumb"]["ip"])):
        lo, hi = JOINTS[key]
        rows.append((key, float(v), lo, hi, lo <= v <= hi))
    pen = 2 * climb.WOBBLE / d["fig"].scale
    for key, v in measure_model(hand).items():
        r = dict(SIDE, **{"thumb seen": THUMB_SEEN, "thumb drawn": THUMB_DRAWN})[key]
        rows.append((key, v if v is not None else -1.0, r[0], r[1],
                     v is not None and r[0] - pen <= v <= r[1] + pen))
    return rows


def main():
    drawn, climbers = record()
    bad = 0
    for d in drawn:
        rows = check_model(d, climbers) if d.get("model") else check(d, climbers)
        if "--table" in sys.argv:
            print(f"{d['name']:14s}{d['figure'][:16]:17s}" + " ".join(
                f"{k}={v:.2f}{'' if ok else '!'}" for k, v, _, _, ok in rows))
        for k, v, lo, hi, ok in rows:
            if not ok:
                bad += 1
                print(f"check_hands: {d['name']} in {d['figure']}: {k} {v:.2f}, range {lo:.2f}-{hi:.2f}")
    what = (f"{len(drawn)} drawings of {len({d['name'] for d in drawn})} hands "
            f"in {len({d['figure'] for d in drawn})} figures")
    print(f"check_hands: {what}: {bad} out of range" if bad else f"check_hands: {what} all in range")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
