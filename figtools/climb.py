"""SVG illustrations of climbers, holds and movement, drawn in greys.

World units are centimetres on the wall, y pointing up. A figure maps world
units to paper at a fixed scale, so line weights and text sizes, which are
given in paper millimetres and points, look the same in every figure.

Conventions used throughout the book:
- back view: the climber is seen from behind, facing the wall
- side view: the wall is on the right, the climber faces right
- the climber's LEFT limbs are shaded grey, the RIGHT limbs are white
  (trouser legs and bare arms; the T-shirt, sleeves included, is white)
- holds are dark resin; the light (white) surface is the one you grab

Every figure is a grey drawing first. paint.py adds the colour at the end of
a build, so draw and judge a figure in grey.
"""

import math
import os
import random
import re

# ---------------------------------------------------------------- vectors


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def length(a):
    return math.hypot(a[0], a[1])


def norm(a):
    n = length(a)
    return (a[0] / n, a[1] / n) if n else (0.0, 0.0)


def perp(a):
    return (-a[1], a[0])


def ang(deg):
    r = math.radians(deg)
    return (math.cos(r), math.sin(r))


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def rot(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)


# ---------------------------------------------------------------- palette

INK = "#000000"
DARK = "#555555"     # holds (on the e-ink panel's 16 greys)
MID = "#8c8c8c"
LEFT = "#aaaaaa"     # climber's left limbs (on the panel's 16 greys)
LIGHT = "#cccccc"    # (on the e-ink panel's 16 greys)
PALE = "#ececec"
WHITE = "#ffffff"
GHOST_LINE = "#777777"   # ghost outlines: one panel level darker than MID

# Greys that only one role uses, so that paint.py can find that role in a
# finished SVG and colour it. DARK works the same way for holds, and the
# HOLD_ greys are the shades drawn on a hold. Each sits on the same panel level
# as the grey the role used to share with other shapes.
BLOCK_ARROW = "#cbcbcb"
HOLD_DEEP = "#343434"
VOLUME = "#cdcdcd"       # marks a volume that a figure draws itself, for its surface
HOLD_MID = "#8d8d8d"
HOLD_LIGHT = "#cecece"
HOLD_PALE = "#ebebeb"

# Label text: the book's serif (book/template.typ), so figure labels match
# the captions.
FONT = "Iowan Old Style"

# Hidden lines: holds, shoes and hands (and forearms behind the body) also
# get a fine dotted outline drawn over the climber, so the parts covered
# by a hand, a leg or the body show through.
XRAY = True
# above every body, hand and hold (z <= 20), below the annotations: arrows,
# labels, tension bands and centre-of-gravity markers stay clean on top
XRAY_Z = 30
XRAY_STYLE = dict(fill=None, stroke="#2a2a2a", sw=0.2, dash=(0.45, 0.55))
# ---------------------------------------------------------------- pen
# SMOOTH_PATHS draws densely sampled outlines (limbs, heads, hands) as
# smooth Bezier curves instead of short straight pieces. HAND_DRAWN gives
# every line a pen-drawn look: outlines a little heavier, nothing thinner
# than PEN_MIN, thin open lines (folds, creases, seams, nails, hatching)
# tapering at both ends, a slight wobble on long lines and contours, and an
# irregular dash rhythm on "move" arrows. Labels, leader lines, step numbers,
# the centre-of-gravity symbol and text stay exact.
#
# The wobble is a smooth displacement field over the page, a function of
# position alone, so a fill and its outline, two shapes sharing an edge, or
# the same hold in every frame of a filmstrip all wobble the same way, and
# every build is identical.
SMOOTH_PATHS = True
HAND_DRAWN = True
WOBBLE = 0.13           # mm on paper: the largest sideways shift of a line
WOBBLE_STEP = 1.4       # mm: longer straight pieces are split before they wobble
PEN_OUTLINE = 1.12      # lines drawn 0.28-0.8 mm wide get this much heavier
PEN_MIN = 0.22          # mm: no line is drawn thinner
PEN_TAPER = 0.27        # mm: open, solid, unfilled lines up to this weight taper
TAPER_END = 0.5         # their width at the very end, as a fraction
MOVE_DASH = (1.6, 1.0, 1.3, 1.15, 1.75, 0.9)   # the dash rhythm of move arrows


def _field(x, y):
    """The wobble at page point (x, y) in mm: a smooth displacement no larger
    than WOBBLE, mostly with wavelengths of 4-10 mm and a little at 3 mm."""
    dx = (0.45 * math.sin(0.61 * x + 0.37 * y + 1.3) +
          0.28 * math.sin(-0.23 * x + 0.97 * y + 4.1) +
          0.17 * math.sin(1.37 * x - 0.53 * y + 2.2) +
          0.10 * math.sin(1.9 * x + 1.1 * y + 0.7))
    dy = (0.45 * math.sin(0.43 * x - 0.71 * y + 0.4) +
          0.28 * math.sin(0.89 * x + 0.29 * y + 5.3) +
          0.17 * math.sin(-0.61 * x - 1.29 * y + 0.9) +
          0.10 * math.sin(-1.2 * x + 1.8 * y + 3.6))
    return dx * WOBBLE, dy * WOBBLE


def _bezier_d(P, corner, closed, dec=2):
    """An SVG path through the points P (page units), smooth except at the
    points flagged in `corner`: each piece is a cubic whose handles follow
    the local direction of the line and are a third of the piece long, so
    the curve never overshoots. `dec`: decimals written."""
    n = len(P)

    def f(p):
        return f"{p[0]:.{dec}f},{p[1]:.{dec}f}"
    if n < 3:
        return "M" + " L".join(f(p) for p in P) + (" Z" if closed else "")
    tin, tout = [], []
    for i in range(n):
        if not closed and i == 0:
            t = norm(sub(P[1], P[0]))
            tin.append(t), tout.append(t)
            continue
        if not closed and i == n - 1:
            t = norm(sub(P[-1], P[-2]))
            tin.append(t), tout.append(t)
            continue
        a, b, c = P[i - 1], P[i], P[(i + 1) % n]
        if corner[i]:
            tin.append(norm(sub(b, a)))
            tout.append(norm(sub(c, b)))
        else:
            t = norm(sub(c, a))
            tin.append(t), tout.append(t)
    d = ["M" + f(P[0])]
    for i in range(n if closed else n - 1):
        j = (i + 1) % n
        L = length(sub(P[j], P[i])) / 3
        c1 = add(P[i], mul(tout[i], L))
        c2 = sub(P[j], mul(tin[j], L))
        d.append(f"C{f(c1)} {f(c2)} {f(P[j])}")
    return " ".join(d) + (" Z" if closed else "")


def _chaikin_open(P, n=2):
    for _ in range(n):
        if len(P) < 3:
            return P
        Q = [P[0]]
        for a, b in zip(P, P[1:]):
            Q += [lerp(a, b, 0.25), lerp(a, b, 0.75)]
        P = Q + [P[-1]]
    return P


def _resample(P, step):
    """Points every `step` along the open polyline P (ends included)."""
    out = [P[0]]
    need = step
    for a, b in zip(P, P[1:]):
        L = length(sub(b, a))
        pos = 0.0
        while L - pos >= need:
            pos += need
            out.append(lerp(a, b, pos / L))
            need = step
        need -= L - pos
    if len(out) > 1 and length(sub(P[-1], out[-1])) < step * 0.3:
        out[-1] = P[-1]
    else:
        out.append(P[-1])
    return out

# ---------------------------------------------------------------- figure


class Fig:
    """A drawing area in world units with a fixed paper scale.

    `scale` is the paper size of one world unit in millimetres."""

    def __init__(self, x0, y0, x1, y1, scale=0.32):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.scale = scale
        self.items = []
        self.defs = set()
        self._plain = 0         # > 0 while drawing exact symbols (no pen effects)
        self.wobble = None      # world point -> the share of WOBBLE kept there (None: all)

    # unit helpers
    def mm(self, v):
        return v / self.scale

    def pt(self, v):
        # figure text is set 8% larger than its nominal size, to match the
        # 11.5 pt body text of the book
        return v * 1.08 * 0.3528 / self.scale

    def P(self, p):
        return (p[0] - self.x0, self.y1 - p[1])

    def fmt(self, p):
        q = self.P(p)
        return f"{q[0]:.2f},{q[1]:.2f}"

    def add(self, svg, z=0):
        self.items.append((z, len(self.items), svg))

    # pen (see HAND_DRAWN)
    def _pen(self):
        return HAND_DRAWN and not self._plain

    def weight(self, sw):
        """The line weight (mm) actually drawn for a requested weight."""
        if not self._pen():
            return sw
        if sw < PEN_MIN:
            return PEN_MIN
        if 0.28 <= sw <= 0.8:
            return sw * PEN_OUTLINE
        return sw

    def _page(self, pts, closed, all_smooth=False):
        """World points of a path -> page points and a corner flag for each.
        Dense stretches are thinned; with the pen on, long straight pieces
        are split and every point is moved by the wobble field. A point is a
        corner (kept sharp) where the line turns by more than 55 degrees or
        a neighbouring piece is longer than 1.6 mm (a drawn polygon rather
        than a sampled curve)."""
        k = self.scale
        n = len(pts)
        corner = []
        for i in range(n):
            if not closed and (i == 0 or i == n - 1):
                corner.append(True)
                continue
            if all_smooth:
                corner.append(False)
                continue
            a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
            u, v = sub(b, a), sub(c, b)
            la, lb = length(u), length(v)
            if la * k < 1e-4 or lb * k < 1e-4:
                corner.append(True)
                continue
            corner.append(dot(u, v) / (la * lb) < 0.57 or la * k > 1.6 or lb * k > 1.6)
        kp, kc, last = [], [], None
        for i, p in enumerate(pts):
            if (last is not None and not corner[i] and i != n - 1 and
                    length(sub(p, last)) * k < 0.8):
                continue
            kp.append(p)
            kc.append(corner[i])
            last = p
        pen = self._pen()
        m = len(kp)
        P, C = [], []
        for i in range(m):
            p = kp[i]
            seg = [(p, kc[i])]
            if pen and (closed or i < m - 1):
                q = kp[(i + 1) % m]
                L = length(sub(q, p)) * k
                if L > WOBBLE_STEP:
                    s = int(L / WOBBLE_STEP)
                    seg += [(lerp(p, q, j / (s + 1)), False) for j in range(1, s + 1)]
            for p_, c_ in seg:
                if pen:
                    dx, dy = _field(p_[0] * k, p_[1] * k)
                    a = self.wobble(p_) if self.wobble else 1.0
                    p_ = (p_[0] + a * dx / k, p_[1] + a * dy / k)
                P.append(self.P(p_))
                C.append(c_)
        return P, C

    def _dec(self):
        # enough decimals to place a point within about 0.02 mm on paper
        return 1 if self.scale <= 0.5 else 2

    def _path_d(self, pts, closed, all_smooth=False):
        if not (SMOOTH_PATHS or self._pen()):
            return "M" + " L".join(self.fmt(p) for p in pts) + (" Z" if closed else "")
        P, C = self._page(pts, closed, all_smooth)
        return _bezier_d(P, C, closed, self._dec())

    def _ribbon(self, pts, z, st, all_smooth=False):
        """A thin open line drawn as a filled band that tapers to
        TAPER_END of its width at both ends, like a pen stroke."""
        P, _ = self._page(pts, False, all_smooth)
        P = _chaikin_open(P, 2)
        s = [0.0]
        for a, b in zip(P, P[1:]):
            s.append(s[-1] + length(sub(b, a)))
        if s[-1] < 1e-6:
            return
        Q = _resample(P, min(self.mm(0.6), s[-1] / 4))
        s = [0.0]
        for a, b in zip(Q, Q[1:]):
            s.append(s[-1] + length(sub(b, a)))
        w = self.mm(self.weight(st.get("sw", 0.3))) / 2
        T = min(self.mm(1.0), s[-1] / 3)
        Lf, Rt = [], []
        for i, q in enumerate(Q):
            nv = perp(norm(sub(Q[min(i + 1, len(Q) - 1)], Q[max(i - 1, 0)])))
            e = min(1.0, min(s[i], s[-1] - s[i]) / T)
            e = e * e * (3 - 2 * e)
            hw = w * (TAPER_END + (1 - TAPER_END) * e)
            # page y points down: perp() turns the other way, which only
            # swaps the sides
            Lf.append(add(q, mul(nv, hw)))
            Rt.append(add(q, mul(nv, -hw)))
        he = w * TAPER_END
        d1 = norm(sub(Q[-1], Q[-2]))
        d0 = norm(sub(Q[0], Q[1]))
        n1, n0 = perp(norm(sub(Q[-1], Q[-2]))), perp(norm(sub(Q[1], Q[0])))
        cap1 = [add(Q[-1], add(mul(n1, he * math.cos(a)), mul(d1, he * math.sin(a))))
                for a in (math.pi / 4, math.pi / 2, 3 * math.pi / 4)]
        cap0 = [add(Q[0], add(mul(n0, he * math.cos(a)), mul(d0, he * math.sin(a))))
                for a in (3 * math.pi / 4, math.pi / 2, math.pi / 4)]
        ring = Lf + cap1 + Rt[::-1] + cap0
        d = _bezier_d(ring, [False] * len(ring), True, self._dec())
        op = st.get("opacity")
        op = f' opacity="{op}"' if op is not None else ""
        self.add(f'<path d="{d}" fill="{st.get("stroke", INK)}"{op}/>', z)

    # primitives
    def style(self, fill=None, stroke=INK, sw=0.3, dash=None, opacity=None,
              join="round", cap="round", ghost=False, wall=False):
        """ghost: mark a piece of an earlier position, whose white is paper, for
        the site's dark copy (website/dark.py). wall: mark a solid piece of wall,
        which the dark copy turns wall grey, unlike a volume of the same grey.
        Print ignores both marks."""
        s = f'fill="{fill or "none"}"'
        if stroke:
            s += (f' stroke="{stroke}" stroke-width="{self.mm(self.weight(sw)):.2f}"'
                  f' stroke-linejoin="{join}" stroke-linecap="{cap}"')
        if dash:
            s += ' stroke-dasharray="' + " ".join(
                f"{self.mm(d):.2f}" for d in dash) + '"'
        if opacity is not None:
            s += f' opacity="{opacity}"'
        if ghost:
            s += ' data-ghost="1"'
        if wall:
            s += ' data-wall="1"'
        return s

    def stipple(self, outline, c, u, ra, rb, colour, focus=None, z=0):
        """Dots inside `outline`, largest at `focus` (default `c`) and
        shrinking to none at the ellipse round the world point `c` with
        semi-axes `ra` along the unit vector `u` and `rb` across it. The
        dots sit on a hexagonal grid aligned with `u`, as in a halftone, so
        the tone fades evenly; a slight jitter, the same on every build,
        keeps it from looking printed."""
        poly = _Poly(outline)
        f = c if focus is None else focus
        v = perp(u)
        o = dot(sub(f, c), u)            # how far the focus sits toward +u
        step, rmax = self.mm(STIPPLE_STEP), self.mm(STIPPLE_DOT)
        row = step * math.sqrt(3) / 2
        rng = random.Random(f"{c[0]:.1f},{c[1]:.1f}")
        nu, nv = int(ra / step) + 2, int(rb / row) + 2
        d = []
        for j in range(-nv, nv + 1):
            for i in range(-nu, nu + 1):
                p = add(c, add(mul(u, (i + 0.5 * (j % 2) + rng.uniform(-0.12, 0.12)) * step),
                               mul(v, (j + rng.uniform(-0.12, 0.12)) * row)))
                q = sub(p, f)
                a = dot(q, u)
                # measured from the focus to the ellipse's end on that side
                e = math.hypot(a / max(ra - o if a > 0 else ra + o, 1e-6), dot(q, v) / rb)
                r = rmax * math.sqrt(max(0.0, 1 - e) ** STIPPLE_FALL)
                if r < 0.35 * rmax or not poly.has(p):
                    continue
                x, y = self.P(p)
                d.append(f"M{x - r:.2f},{y:.2f}a{r:.2f},{r:.2f} 0 1,0 {2 * r:.2f},0"
                         f"a{r:.2f},{r:.2f} 0 1,0 {-2 * r:.2f},0")
        if d:
            self.add(f'<path d="{"".join(d)}" fill="{colour}"/>', z)

    def poly(self, pts, closed=True, z=0, taper=None, _smooth=False, **st):
        """A path through `pts`. taper: draw an open line as a tapered pen
        stroke (default: thin, solid, unfilled open lines when HAND_DRAWN)."""
        if taper is None:
            taper = (not closed and not st.get("fill") and not st.get("dash") and
                     st.get("stroke", INK) is not None and
                     self.weight(st.get("sw", 0.3)) <= PEN_TAPER)
        if taper and self._pen() and len(pts) >= 2:
            self._ribbon(pts, z, st, _smooth)
            return
        self.add(f'<path d="{self._path_d(pts, closed, _smooth)}" {self.style(**st)}/>', z)
        if st.get("stroke") and st.get("fill") == DARK:
            _surface(self, pts, z, _smooth, st)
        elif st.get("stroke") and st.get("fill") == VOLUME:
            _surface(self, pts, z, _smooth, st, light=VOLUME_LIT, dark=VOLUME_SHADE)

    def smooth(self, pts, closed=True, z=0, tension=1.0, **st):
        if not self._pen() or len(pts) < 3:
            self.add(f'<path d="{self.smooth_d(pts, closed, tension)}" '
                     f'{self.style(**st)}/>', z)
            return
        self.poly(self._smooth_pts(pts, closed, tension), closed=closed, z=z,
                  _smooth=True, **st)

    def _smooth_pts(self, pts, closed, tension, k=8):
        """The curve smooth() draws through `pts`, sampled into points."""
        n = len(pts)
        t = tension / 6
        out = []
        for i in (range(n) if closed else range(n - 1)):
            p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
            p1, p2 = pts[i], pts[(i + 1) % n]
            p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
            c1 = add(p1, mul(sub(p2, p0), t))
            c2 = sub(p2, mul(sub(p3, p1), t))
            for j in range(k):
                u = j / k
                a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
                out.append((a * p1[0] + b * c1[0] + c * c2[0] + d * p2[0],
                            a * p1[1] + b * c1[1] + c * c2[1] + d * p2[1]))
        if not closed:
            out.append(pts[-1])
        return out

    def smooth_d(self, pts, closed=True, tension=1.0):
        n = len(pts)
        if n < 3:
            return "M" + " L".join(self.fmt(p) for p in pts)
        P = [self.P(p) for p in pts]
        d = f"M{P[0][0]:.2f},{P[0][1]:.2f}"
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p0 = P[(i - 1) % n] if (closed or i > 0) else P[i]
            p1 = P[i]
            p2 = P[(i + 1) % n]
            p3 = P[(i + 2) % n] if (closed or i + 2 < n) else P[(i + 1) % n]
            t = tension / 6
            c1 = (p1[0] + (p2[0] - p0[0]) * t, p1[1] + (p2[1] - p0[1]) * t)
            c2 = (p2[0] - (p3[0] - p1[0]) * t, p2[1] - (p3[1] - p1[1]) * t)
            d += (f" C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f}"
                  f" {p2[0]:.2f},{p2[1]:.2f}")
        return d + (" Z" if closed else "")

    def circle(self, c, r, z=0, **st):
        q = self.P(c)
        self.add(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="{r:.2f}" '
                 f'{self.style(**st)}/>', z)

    def line(self, a, b, z=0, sw=0.3, stroke=INK, dash=None, cap="round"):
        self.poly([a, b], closed=False, z=z, sw=sw, stroke=stroke, dash=dash,
                  cap=cap)

    def text(self, s, p, size=7.5, anchor="middle", weight=500, z=50,
             fill=INK, italic=False, halo=True, keep_in=True):
        q = self.P(p)
        fs = self.pt(size)
        # keep the text inside the frame (approximate width)
        w = len(s) * fs * 0.53
        x0 = {"start": q[0], "middle": q[0] - w / 2, "end": q[0] - w}[anchor]
        W = self.x1 - self.x0
        pad = self.mm(0.8)
        if keep_in and x0 < pad:
            q = (q[0] + pad - x0, q[1])
        elif keep_in and x0 + w > W - pad:
            q = (q[0] - (x0 + w - W + pad), q[1])
        style = ' font-style="italic"' if italic else ""
        base = (f'x="{q[0]:.2f}" y="{q[1] + fs * 0.35:.2f}" '
                f'font-family="{FONT}" font-size="{fs:.2f}" '
                f'font-weight="{weight}" text-anchor="{anchor}"{style}')
        if halo:
            self.add(f'<text {base} fill="{WHITE}" stroke="{WHITE}" '
                     f'stroke-width="{self.mm(0.9):.2f}" '
                     f'stroke-linejoin="round">{esc(s)}</text>', z)
        self.add(f'<text {base} fill="{fill}">{esc(s)}</text>', z + 0.01)

    # annotations
    def label(self, s, at, to=None, size=7.5, anchor=None, z=60, gap=1.2):
        """Text at `at`, optionally with a leader line to the point `to`."""
        if to is not None:
            v = norm(sub(to, at))
            self._plain += 1
            self.line(add(at, mul(v, self.mm(gap) * 1.6)), to, z=z - 1,
                      sw=0.22)
            self.circle(to, self.mm(0.55), z=z - 1, fill=INK, stroke=None)
            self._plain -= 1
            if anchor is None:
                anchor = ("end" if v[0] > 0.35 else
                          "start" if v[0] < -0.35 else "middle")
        self.text(s, at, size=size, anchor=anchor or "middle", z=z)

    def arrow(self, pts, kind="move", z=40, label=None, label_at=0.5,
              label_off=(0, 0), size=7.5, head=None):
        """Arrow along 2 points (straight) or 3+ points (smooth curve).

        kind: move (dashed: a limb or the body travels this way), force
        (bold solid: push or pull), path (thin solid), turn (rotation)."""
        sw = {"move": 0.45, "force": 0.9, "path": 0.35, "turn": 0.5}[kind]
        dash = (MOVE_DASH if self._pen() else (1.6, 1.0)) if kind == "move" else None
        hl = self.mm(head or {"force": 2.6, "move": 2.0}.get(kind, 2.0))
        end = pts[-1]
        prev = pts[-2] if len(pts) == 2 else self._curve_prev(pts)
        v = norm(sub(end, prev))
        stem_end = sub(end, mul(v, hl * 0.75))
        body = pts[:-1] + [stem_end]
        if len(pts) == 2:
            self.poly(body, closed=False, z=z, sw=sw, dash=dash,
                      stroke=INK, cap="butt")
        else:
            self.smooth(body, closed=False, z=z, sw=sw, dash=dash, cap="butt")
        w = hl * 0.42
        tip = end
        base = sub(end, mul(v, hl))
        self.poly([tip, add(base, mul(perp(v), w)), add(base, mul(perp(v), -w))],
                  z=z, fill=INK, stroke=INK, sw=0.1)
        if label:
            if len(pts) == 2:
                p = lerp(pts[0], pts[1], label_at)
            else:
                p = pts[len(pts) // 2]
            self.text(label, add(p, label_off), size=size, z=z + 5)

    def body_arrow(self, pts, width=2.0, z=45, fill=BLOCK_ARROW, label=None,
                   size=7.5, label_off=(0, 0)):
        """A broad block arrow along `pts` (2+ points, curved through them),
        for movement of the whole body or the hips. `width` is in mm."""
        w = self.mm(width) / 2
        path = catmull(pts, closed=False, k=8) + [pts[-1]] if len(pts) > 2 else \
            [lerp(pts[0], pts[1], i / 12) for i in range(13)]
        head_len = w * 3.2
        # trim the shaft to leave room for the head
        total = sum(length(sub(b, a)) for a, b in zip(path, path[1:]))
        keep, acc = [path[0]], 0.0
        for a, b in zip(path, path[1:]):
            seg = length(sub(b, a))
            if acc + seg >= total - head_len:
                keep.append(lerp(a, b, (total - head_len - acc) / seg))
                break
            keep.append(b)
            acc += seg
        L, R = [], []
        for i, p in enumerate(keep):
            q0 = keep[max(i - 1, 0)]
            q1 = keep[min(i + 1, len(keep) - 1)]
            nv = perp(norm(sub(q1, q0)))
            L.append(add(p, mul(nv, w)))
            R.append(add(p, mul(nv, -w)))
        end = keep[-1]
        dv = norm(sub(pts[-1], end))
        nv = perp(dv)
        head = [add(end, mul(nv, w * 2.2)), pts[-1], add(end, mul(nv, -w * 2.2))]
        self.poly(L + head + R[::-1], z=z, fill=fill, stroke=INK, sw=0.35)
        if label:
            self.text(label, add(keep[len(keep) // 2], label_off), size=size, z=z + 5)

    def _curve_prev(self, pts):
        # direction at the end of a Catmull-Rom curve ~ from pts[-2] to end
        return lerp(pts[-2], pts[-1], 0.6)

    def turn(self, c, r, a0, a1, z=40, label=None, size=7.5):
        """Curved arrow around centre `c` from angle a0 to a1 (degrees)."""
        n = 12
        pts = [add(c, mul(ang(a0 + (a1 - a0) * i / n), r)) for i in range(n + 1)]
        self.arrow(pts, kind="turn", z=z)
        if label:
            mid = add(c, mul(ang((a0 + a1) / 2), r + self.mm(3)))
            self.text(label, mid, size=size, z=z + 5)

    def cog(self, p, z=70, r=None, plumb_to=None):
        """Centre-of-gravity symbol, with an optional plumb line."""
        r = r or self.mm(1.5)
        self._plain += 1
        if plumb_to is not None:
            self.line(p, (p[0], plumb_to), z=z - 1, sw=0.3, dash=(0.6, 0.8))
        self.circle(p, r, z=z, fill=WHITE, stroke=INK, sw=0.3)
        for a in (0, 180):
            pts = [p] + [add(p, mul(ang(a + t * 9), r)) for t in range(11)]
            self.poly(pts, z=z + 0.1, fill=INK, stroke=None)
        self.circle(p, r, z=z + 0.2, stroke=INK, sw=0.3)
        self._plain -= 1

    def step(self, n, p, z=80, r=None):
        """A circled step number."""
        r = r or self.mm(1.9)
        self._plain += 1
        self.circle(p, r, z=z, fill=INK, stroke=WHITE, sw=0.3)
        self._plain -= 1
        self.text(str(n), p, size=6.5, weight=700, fill=WHITE, z=z + 1,
                  halo=False)

    def cross(self, p, z=60, size=None):
        """An X marking something to avoid."""
        s = size or self.mm(1.4)
        self._plain += 1
        for a, b in (((-s, -s), (s, s)), ((-s, s), (s, -s))):
            self.line(add(p, a), add(p, b), z=z, sw=0.6)
        self._plain -= 1

    # output
    def svg(self):
        W, H = self.x1 - self.x0, self.y1 - self.y0
        body = "\n".join(s for _, _, s in sorted(_without_cut_dots(self.items, W, H)))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{W * self.scale:.2f}mm" height="{H * self.scale:.2f}mm" '
                f'viewBox="0 0 {W:.2f} {H:.2f}">\n{body}\n</svg>\n')

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.svg())


# A bolt hole on the wall (wall_grid) that a shape or a label cuts leaves a tiny
# fragment of a dot beside the shape, which reads as a speck on e-ink. So a dot goes
# when an edge or a stroke runs through it, or the frame does. One wholly under a shape
# doesn't show anyway, and one clear of everything stays. The test uses the drawn
# paths, so it sees exactly what the pen effects made of a shape.
GRID_DOT = re.compile(r'<circle cx="([-\d.]+)" cy="([-\d.]+)" r="([\d.]+)" fill="#b0b0b0"/>$')
_CLIPPED = re.compile(r'<clipPath.*?</clipPath>|<g clip-path.*?</g>', re.S)
_ELEMENT = re.compile(r'<(path|circle|text|rect)\b([^>]*)>([^<]*)')
_CELL = 10.0            # world units; the side of a square of the index below


def _attr(attrs, name, default=None):
    m = re.search(rf'\b{name}="([^"]*)"', attrs)
    return m.group(1) if m else default


def _path_segments(d):
    """A path's outline as straight pieces. Dots of a stipple (arcs) are skipped:
    they lie inside the limb they shade."""
    if "a" in d:
        return []
    pieces, cur, start = [], None, None
    for op, nums in re.findall(r'([MLCZ])([^MLCZ]*)', d):
        n = [float(v) for v in re.findall(r'-?\d+\.?\d*', nums)]
        if op == "M":
            cur = start = (n[0], n[1])
        elif op == "L":
            for i in range(0, len(n), 2):
                pieces.append((cur, (n[i], n[i + 1])))
                cur = (n[i], n[i + 1])
        elif op == "C":
            for i in range(0, len(n), 6):
                p0, p1, p2, p3 = cur, (n[i], n[i + 1]), (n[i + 2], n[i + 3]), (n[i + 4], n[i + 5])
                last = p0
                for t in (0.25, 0.5, 0.75, 1.0):
                    u = 1 - t
                    q = (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                         u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])
                    pieces.append((last, q))
                    last = q
                cur = p3
        elif op == "Z" and cur != start:
            pieces.append((cur, start))
            cur = start
    return pieces


def _edges(svg):
    """The straight pieces of an item's visible edges, with the half width of the
    stroke along each."""
    out = []
    for kind, attrs, inner in _ELEMENT.findall(_CLIPPED.sub("", svg)):
        stroked = _attr(attrs, "stroke") not in (None, "none")
        hw = float(_attr(attrs, "stroke-width", "0")) / 2 if stroked else 0.0
        if kind == "path":
            out += [(a, b, hw) for a, b in _path_segments(_attr(attrs, "d", ""))]
        elif kind == "rect":
            x, y, w, h = (float(_attr(attrs, k, "0")) for k in ("x", "y", "width", "height"))
            ring = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
            out += [(a, b, hw) for a, b in zip(ring, ring[1:])]
        elif kind == "circle":
            cx, cy, r = (float(_attr(attrs, k, "0")) for k in ("cx", "cy", "r"))
            ring = [(cx + r * math.cos(i * math.pi / 8), cy + r * math.sin(i * math.pi / 8)) for i in range(17)]
            out += [(a, b, hw) for a, b in zip(ring, ring[1:])]
        elif kind == "text":
            # a label's box, drawn as a hatch of edges so that a dot inside it goes too
            size = float(_attr(attrs, "font-size", "0"))
            w = len(inner) * size * 0.53
            x = float(_attr(attrs, "x", "0"))
            x -= {"start": 0, "middle": w / 2, "end": w}[_attr(attrs, "text-anchor", "start")]
            y = float(_attr(attrs, "y", "0"))
            for j in range(4):
                level = y - j * size / 3
                out.append(((x, level), (x + w, level), hw + size / 6))
    return out


def _without_cut_dots(items, W, H):
    dots = [it for it in items if GRID_DOT.match(it[2])]
    if not dots:
        return items
    index = {}
    for z, _, svg in items:
        if GRID_DOT.match(svg) or z <= dots[0][0]:
            continue
        for a, b, hw in _edges(svg):
            pad = hw + 2.0
            for i in range(int((min(a[0], b[0]) - pad) // _CELL), int((max(a[0], b[0]) + pad) // _CELL) + 1):
                for j in range(int((min(a[1], b[1]) - pad) // _CELL), int((max(a[1], b[1]) + pad) // _CELL) + 1):
                    index.setdefault((i, j), []).append((a, b, hw))

    def cut(item):
        x, y, r = (float(v) for v in GRID_DOT.match(item[2]).groups())
        if x < r or y < r or x > W - r or y > H - r:
            return True
        for a, b, hw in index.get((int(x // _CELL), int(y // _CELL)), ()):
            d = sub(b, a)
            t = max(0.0, min(1.0, dot(sub((x, y), a), d) / max(dot(d, d), 1e-9)))
            if length(sub((x, y), add(a, mul(d, t)))) < r + hw:
                return True
        return False

    return [it for it in items if it not in dots or not cut(it)]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- walls


def wall_side(fig, x, y0, y1, angle=0, z=-20, label=None):
    """Side-view wall line from height y0 to y1. `angle` is the overhang in
    degrees past vertical (positive leans over the climber, negative is a
    slab). The wall is on the right of the line, hatched."""
    a = (math.tan(math.radians(angle)) * -1, 1)
    top = (x + a[0] * (y1 - y0), y1)
    bot = (x, y0)
    d = norm(sub(top, bot))
    n = (d[1], -d[0])  # into the wall (right)
    fig.poly([bot, top, add(top, mul(n, fig.mm(2.2))), add(bot, mul(n, fig.mm(2.2)))],
             z=z, fill=PALE, stroke=None)
    fig.line(bot, top, z=z + 1, sw=0.6)
    L = length(sub(top, bot))
    step = fig.mm(2.0)
    k = 0.0
    while k < L:
        p = add(bot, mul(d, k))
        fig.line(p, add(add(p, mul(n, fig.mm(2.2))), mul(d, fig.mm(-1.4))),
                 z=z + 1, sw=0.18, stroke=MID)
        k += step
    return lambda h: lerp(bot, top, (h - y0) / (y1 - y0))


def ground(fig, y=0, x0=None, x1=None, z=-20, mat=True):
    """Floor line with a mat."""
    x0 = fig.x0 if x0 is None else x0
    x1 = fig.x1 if x1 is None else x1
    if mat:
        fig.poly([(x0, y), (x1, y), (x1, y - fig.mm(2.5)), (x0, y - fig.mm(2.5))],
                 z=z, fill=LIGHT, stroke=INK, sw=0.3)
    else:
        fig.line((x0, y), (x1, y), z=z, sw=0.5)


def wall_back(fig, x0, y0, x1, y1, z=-30):
    """A faint panel outline for back views."""
    fig.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z=z, fill=None,
             stroke=MID, sw=0.2, dash=(0.8, 0.8))


# ---------------------------------------------------------------- holds
#
# Holds are drawn like resin gym holds, with the figures' pen: a dark body
# (DARK, outlined in INK), the surface you grab light (WHITE where fingers
# or toes go, HOLD_LIGHT and HOLD_MID where a rounded top turns away from the light),
# the shadow inside an incut or a pocket in INK, a bolt (a light washer
# round a dark socket) or screws where a real hold has them, and on a large
# hold a stroke of shading or texture. A detail too small to read on paper
# is left out, so a foothold in a full-body figure is a body and a light top.
#
# Each kind comes in several shapes, as on a gym wall (HOLD_VARIANTS).
# hold() picks one, and whether to mirror it, from the hold's position, so
# the same hold looks the same in every frame of a filmstrip and in every
# build while a wall of holds shows variety; `variant=` picks one by name.
# Every shape keeps its kind's grabbing surface on the side that faces
# `use` (y = +1 in its unit frame) and stays close to its kind's size, so
# grip(), stand() and the dotted outline stay right.

HOLD_SIZE = {"jug": (17, 10), "crimp": (13, 4), "pinch": (7, 15),
             "sloper": (19, 13), "foot": (8, 4), "pocket": (9, 7),
             "dual": (18, 11), "macro": (32, 18)}


def _arc(cx, cy, rx, ry, a0=0, a1=360, n=24):
    """Points on an ellipse from angle a0 to a1 (degrees); a full turn
    leaves out the repeated end point."""
    full = abs(a1 - a0) >= 360
    m = n if full else n + 1
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(m)]


def _curve(f, x0=-1.6, x1=1.6, n=16):
    return [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n))
            for i in range(n + 1)]


def _above(f, top=1.9):
    """The region above the curve y = f(x) in a hold's unit frame (the
    outline clips it)."""
    c = _curve(f)
    return c + [(c[-1][0], top), (c[0][0], top)]


def _between(f_top, f_bot):
    return _curve(f_top) + _curve(f_bot)[::-1]


def _crescent(cx, cy, rx, ry, k=0.45, n=14):
    """The lit floor of a pocket: the lower half of the hole's ellipse less
    a flatter one."""
    return _arc(cx, cy, rx, ry, 180, 360, n) + _arc(cx, cy, rx, ry * k, 360, 180, n)[1:-1]


def _wavy(x0, x1, y0, y1, amp, n=10, ph=0.0, side=1):
    """A slightly wavy edge from (x0, y0) to (x1, y1), for tufa ribs."""
    return [(lerp((x0, y0), (x1, y1), i / n)[0] +
             side * amp * math.sin(ph + i * 2.1) * (1 - abs(2 * i / n - 1) ** 3),
             lerp((x0, y0), (x1, y1), i / n)[1]) for i in range(n + 1)]


def _stipple(region_top, x0=-0.9, x1=0.9, y1=1.0, step=0.16):
    """Texture dots for a dual-texture lip: a staggered grid above the curve
    y = region_top(x)."""
    pts, row = [], 0
    y = y1
    while True:
        y -= step * 0.8
        if y < -1:
            break
        x = x0 + (step / 2 if row % 2 else 0)
        while x <= x1:
            if y > region_top(x) + 0.05:
                pts.append((x, y))
            x += step
        row += 1
    return pts


def _facets(outline, apex, shades):
    """Triangles from each edge of an angular outline to `apex`, as volume()
    draws them, with their shades, and the ridge lines between them."""
    n = len(outline)
    fills = [(shades[i], [outline[i], outline[(i + 1) % n], apex]) for i in range(n)]
    ridges = [[apex, p] for p in outline]
    return fills, ridges


# The shapes. A variant gives its name, its size relative to HOLD_SIZE, its
# outline in the unit frame (x along the lip, y = +1 the grabbing side),
# whether its outline is angular (cut facets) or smooth (cast), whether it
# may be mirrored, and its details, drawn inside the outline in order:
#   fills   (shade, region[, smallest paper height in mm to draw it at])
#   lines   ridges and seams in INK, on holds at least 2.8 mm tall on paper
#   strokes (shade, line): shading or texture, on holds at least 7 mm wide
#   stipple texture dots, on holds at least 3.5 mm wide
#   bolts   washer and socket; screws: small light heads
_MACRO = [(-1.0, 0.25), (-0.15, 1.0), (0.85, 0.62), (0.8, -0.72), (-0.55, -0.9)]
_MACRO_APEX = (0.0, 0.15)
_MACRO_FILLS, _MACRO_RIDGES = _facets(_MACRO, _MACRO_APEX,
                                      [HOLD_LIGHT, WHITE, HOLD_MID, DARK, HOLD_MID])
_CHIP = [(-1.0, 0.25), (-0.3, 1.0), (0.75, 0.8), (0.95, -0.35), (-0.4, -0.95)]
_CHIP_FILLS, _CHIP_RIDGES = _facets(_CHIP, (0.0, 0.32),
                                    [HOLD_LIGHT, WHITE, HOLD_MID, DARK, DARK])
_FCHIP = [(-1.0, 0.15), (-0.35, 1.0), (0.8, 0.75), (0.95, -0.45), (-0.45, -0.9)]
_FCHIP_FILLS, _FCHIP_RIDGES = _facets(_FCHIP, (0.1, 0.3),
                                      [WHITE, WHITE, HOLD_MID, DARK, HOLD_MID])


def _bar(top, bot, x_end=1.0, n=7):
    """A rail: its top and bottom edges y = top(x), bot(x), with round ends."""
    xs = [-x_end * 0.92 + 1.84 * x_end * i / (n - 1) for i in range(n)]
    mid_r = (top(x_end) + bot(x_end)) / 2
    mid_l = (top(-x_end) + bot(-x_end)) / 2
    return ([(x, top(x)) for x in xs] + [(x_end, mid_r)] +
            [(x, bot(x)) for x in xs[::-1]] + [(-x_end, mid_l)])


def _crv_top(x):
    return 1.0 - 0.55 * x * x


def _crv_bot(x):
    return -0.5 - 0.5 * x * x


HOLD_VARIANTS = {
    "jug": [
        # a bucket: the dark mouth of the bowl behind a chalked rim
        dict(name="bucket",
             outline=[(-1.0, 0.6), (-0.88, 0.95), (-0.45, 1.03), (0.0, 1.0),
                      (0.45, 1.03), (0.88, 0.95), (1.0, 0.6), (0.85, -0.2),
                      (0.5, -0.75), (0.0, -0.92), (-0.5, -0.75), (-0.85, -0.2)],
             fills=[(WHITE, _above(lambda x: 0.24 - 0.12 * (1 - x * x))),
                    (INK, _arc(0, 0.75, 0.62, 0.17), 1.3)],
             strokes=[(HOLD_MID, [(-0.74, -0.02), (-0.6, -0.42), (-0.3, -0.66)])],
             bolts=[(0.0, -0.4)]),
        # a horn: one end of the lip rises into a horn to wrap
        dict(name="horn", mirror=True,
             outline=[(-0.95, -0.4), (-1.0, 0.12), (-0.82, 0.48), (-0.45, 0.58),
                      (-0.05, 0.56), (0.25, 0.6), (0.45, 0.78), (0.58, 1.02),
                      (0.7, 1.2), (0.84, 1.22), (0.9, 1.05), (0.92, 0.7),
                      (0.9, 0.3), (0.75, -0.3), (0.4, -0.78), (-0.1, -0.92),
                      (-0.6, -0.82)],
             fills=[(WHITE, _curve(lambda x: 0.22 + 0.06 * x, -1.6, 0.4, 8) +
                     [(0.5, 0.42), (0.62, 0.72), (0.7, 1.0), (0.74, 1.9),
                      (-1.6, 1.9)])],
             strokes=[(HOLD_MID, [(-0.8, -0.3), (-0.5, -0.62), (-0.12, -0.74)]),
                      (HOLD_MID, [(0.82, 1.0), (0.8, 0.6), (0.7, 0.1)])],
             bolts=[(-0.22, -0.34)]),
        # a long flat incut: a flat chalked top over the shadow of its lip
        dict(name="flat", size=(1.12, 0.82),
             outline=[(-1.0, 0.72), (-0.93, 0.98), (-0.5, 1.02), (0.5, 1.02),
                      (0.93, 0.98), (1.0, 0.72), (0.95, -0.15), (0.72, -0.75),
                      (0.25, -0.95), (-0.25, -0.95), (-0.72, -0.75),
                      (-0.95, -0.15)],
             fills=[(WHITE, _above(lambda x: 0.4)),
                    (INK, _between(lambda x: 0.4, lambda x: 0.22), 1.6)],
             strokes=[(HOLD_MID, [(-0.82, -0.05), (-0.6, -0.55), (-0.25, -0.75)])],
             bolts=[(0.0, -0.4)], screws=[(-0.74, -0.2), (0.74, -0.2)]),
    ],
    "crimp": [
        # a straight rail with a flat chalked top
        dict(name="rail",
             outline=_bar(lambda x: 1.0 - 0.05 * x ** 4, lambda x: -0.92 + 0.1 * x ** 4),
             fills=[(WHITE, _above(lambda x: 0.22))],
             screws=[(-0.62, -0.35), (0.62, -0.35)]),
        # a curved edge
        dict(name="curved", outline=_bar(_crv_top, _crv_bot),
             fills=[(WHITE, _above(lambda x: _crv_top(x) - 0.75))],
             screws=[(0.0, -0.05)]),
        # a small cut chip
        dict(name="chip", size=(0.7, 1.3), angular=True, mirror=True,
             outline=_CHIP, fills=_CHIP_FILLS, lines=_CHIP_RIDGES),
    ],
    "pinch": [
        # a fin: two flanks meeting at a ridge
        dict(name="fin", size=(0.85, 1.05),
             outline=[(0.0, 1.0), (0.48, 0.66), (0.66, 0.0), (0.5, -0.66),
                      (0.0, -1.0), (-0.5, -0.66), (-0.66, 0.0), (-0.48, 0.66)],
             fills=[(HOLD_LIGHT, [(-1.9, -1.9), (0.0, -1.9), (0.06, 0.0), (0.0, 1.9),
                             (-1.9, 1.9)]),
                    (WHITE, [(-1.9, -1.9), (-0.42, -1.9), (-0.36, 0.0),
                             (-0.42, 1.9), (-1.9, 1.9)])],
             lines=[[(0.0, 0.92), (0.06, 0.0), (0.0, -0.92)]],
             mirror=True),
        # a block, pinched on both sides
        dict(name="block", size=(1.0, 0.9),
             outline=[(-1.0, 0.82), (-0.85, 1.0), (0.85, 1.0), (1.0, 0.82),
                      (1.0, -0.82), (0.85, -1.0), (-0.85, -1.0), (-1.0, -0.82)],
             fills=[(WHITE, [(-1.9, -1.9), (-0.5, -1.9), (-0.5, 1.9), (-1.9, 1.9)]),
                    (HOLD_LIGHT, [(1.9, -1.9), (0.55, -1.9), (0.55, 1.9), (1.9, 1.9)])],
             bolts=[(0.0, 0.0)]),
        # a tufa: a knobbly rib
        dict(name="tufa", size=(0.9, 1.08), mirror=True,
             outline=(_wavy(-0.62, -0.7, -0.9, 0.9, 0.12, ph=0.4) +
                      [(-0.3, 1.0), (0.3, 0.98)] +
                      _wavy(0.66, 0.6, 0.9, -0.9, 0.1, ph=1.7) +
                      [(0.25, -1.0), (-0.3, -1.0)]),
             fills=[(HOLD_LIGHT, [(-1.9, -1.9), (-0.22, -1.9), (-0.3, 0.0),
                             (-0.2, 1.9), (-1.9, 1.9)])],
             strokes=[(HOLD_MID, [(-0.1, 0.55), (0.35, 0.5)]),
                      (HOLD_MID, [(-0.05, 0.0), (0.4, 0.05)]),
                      (HOLD_MID, [(-0.12, -0.5), (0.3, -0.55)])]),
    ],
    "sloper": [
        # a round dome, lit on its rounded top
        dict(name="dome",
             outline=[(1.0, 0.05), (0.82, 0.62), (0.4, 0.95), (0.0, 1.0),
                      (-0.4, 0.95), (-0.82, 0.62), (-1.0, 0.05), (-0.85, -0.55),
                      (-0.45, -0.88), (0.0, -0.95), (0.45, -0.88), (0.85, -0.55)],
             fills=[(HOLD_MID, _arc(-0.04, 0.42, 0.96, 0.74)),
                    (HOLD_LIGHT, _arc(-0.08, 0.6, 0.7, 0.46)),
                    (WHITE, _arc(-0.12, 0.74, 0.4, 0.22))],
             bolts=[(0.06, -0.52)]),
        # a long rounded rail
        dict(name="rail", size=(1.3, 0.62),
             outline=[(-1.0, 0.0), (-0.95, 0.6), (-0.75, 0.95), (0.0, 1.0),
                      (0.75, 0.95), (0.95, 0.6), (1.0, 0.0), (0.95, -0.6),
                      (0.75, -0.95), (0.0, -1.0), (-0.75, -0.95), (-0.95, -0.6)],
             fills=[(HOLD_MID, _above(lambda x: -0.18 + 0.25 * x ** 4)),
                    (HOLD_LIGHT, _above(lambda x: 0.22 + 0.25 * x ** 4)),
                    (WHITE, _above(lambda x: 0.6 + 0.2 * x ** 4))],
             bolts=[(-0.3, -0.52)], screws=[(0.62, -0.5)]),
        # a lumpy blob with two rounded lobes
        dict(name="blob", mirror=True,
             outline=[(-1.0, -0.05), (-0.95, 0.5), (-0.68, 0.88), (-0.3, 0.88),
                      (0.0, 0.66), (0.3, 0.94), (0.72, 0.96), (0.98, 0.55),
                      (0.95, -0.25), (0.6, -0.82), (0.0, -0.95), (-0.6, -0.8)],
             fills=[(HOLD_MID, _arc(-0.52, 0.36, 0.55, 0.6)),
                    (HOLD_MID, _arc(0.52, 0.42, 0.55, 0.6)),
                    (HOLD_LIGHT, _arc(-0.54, 0.58, 0.36, 0.32)),
                    (HOLD_LIGHT, _arc(0.52, 0.64, 0.38, 0.32)),
                    (WHITE, _arc(-0.56, 0.72, 0.2, 0.13)),
                    (WHITE, _arc(0.5, 0.78, 0.22, 0.13))],
             bolts=[(0.02, -0.45)]),
    ],
    "pocket": [
        # one finger: a mono, high in a lumpy body
        dict(name="mono", mirror=True,
             outline=[(-1.0, 0.1), (-0.8, 0.72), (-0.2, 1.0), (0.55, 0.9),
                      (0.98, 0.4), (0.9, -0.4), (0.45, -0.92), (-0.35, -0.95),
                      (-0.85, -0.55)],
             fills=[(INK, _arc(0.02, 0.3, 0.34, 0.4)),
                    (WHITE, _crescent(0.02, 0.3, 0.34, 0.4, k=0.6))]),
        # two fingers
        dict(name="two", size=(1.12, 1.0), mirror=True,
             outline=[(-1.0, 0.05), (-0.82, 0.72), (-0.1, 1.0), (0.7, 0.86),
                      (1.0, 0.2), (0.82, -0.6), (0.2, -0.98), (-0.6, -0.88)],
             fills=[(INK, _arc(0.0, 0.3, 0.54, 0.38)),
                    (WHITE, _crescent(0.0, 0.3, 0.54, 0.38, k=0.6))]),
        # three fingers
        dict(name="three", size=(1.28, 0.95), mirror=True,
             outline=[(-1.0, 0.1), (-0.8, 0.8), (-0.1, 1.0), (0.7, 0.85),
                      (1.0, 0.1), (0.78, -0.72), (0.0, -1.0), (-0.75, -0.72)],
             fills=[(INK, _arc(0.0, 0.28, 0.68, 0.36)),
                    (WHITE, _crescent(0.0, 0.28, 0.68, 0.36, k=0.6))]),
    ],
    "foot": [
        # a cut chip
        dict(name="chip", angular=True, mirror=True, outline=_FCHIP,
             fills=_FCHIP_FILLS, lines=_FCHIP_RIDGES),
        # a screw-on: a rounded nub with one screw
        dict(name="screw-on", size=(0.92, 1.05),
             outline=[(-1.0, 0.15), (-0.8, 0.75), (-0.3, 1.0), (0.3, 1.0),
                      (0.8, 0.75), (1.0, 0.15), (0.85, -0.6), (0.3, -0.9),
                      (-0.3, -0.9), (-0.85, -0.6)],
             fills=[(WHITE, _above(lambda x: 0.3 - 0.1 * (1 - x * x)))],
             screws=[(0.0, -0.32)]),
        # a small flat edge
        dict(name="edge", size=(1.18, 0.75),
             outline=_bar(lambda x: 1.0 - 0.08 * x ** 4, lambda x: -0.92 + 0.15 * x ** 4),
             fills=[(WHITE, _above(lambda x: 0.12))]),
    ],
    "dual": [
        # a dual-texture hold: a textured lip, a smooth glossy body
        dict(name="dual", mirror=True,
             outline=[(-1.0, 0.3), (-0.92, 0.82), (-0.5, 1.0), (0.2, 1.02),
                      (0.78, 0.92), (1.0, 0.5), (0.9, -0.35), (0.5, -0.85),
                      (-0.2, -0.95), (-0.75, -0.65)],
             fills=[(WHITE, _above(lambda x: 0.2 + 0.14 * x))],
             lines=[_curve(lambda x: 0.2 + 0.14 * x, -1.1, 1.1, 8)],
             stipple=lambda x: 0.2 + 0.14 * x,
             strokes=[(WHITE, [(-0.66, -0.12), (-0.48, -0.48), (-0.16, -0.68)])],
             bolts=[(0.32, -0.38)]),
    ],
    "macro": [
        # a faceted macro, cut like a small volume
        dict(name="facet", angular=True, mirror=True, outline=_MACRO,
             fills=_MACRO_FILLS, lines=_MACRO_RIDGES, bolts=[_MACRO_APEX]),
        # a rounded macro
        dict(name="pebble",
             outline=[(-1.0, 0.0), (-0.9, 0.62), (-0.5, 0.95), (0.1, 1.0),
                      (0.68, 0.9), (0.98, 0.45), (0.96, -0.3), (0.6, -0.86),
                      (0.0, -1.0), (-0.62, -0.86), (-0.94, -0.48)],
             fills=[(HOLD_MID, _arc(-0.04, 0.34, 0.98, 0.78)),
                    (HOLD_LIGHT, _arc(-0.08, 0.56, 0.74, 0.5)),
                    (WHITE, _arc(-0.14, 0.72, 0.44, 0.24))],
             bolts=[(0.0, -0.5)], screws=[(-0.7, -0.28), (0.7, -0.3)]),
    ],
}

# The first shape of each kind, for code that wants one outline.
HOLD_SHAPES = {k: v[0]["outline"] for k, v in HOLD_VARIANTS.items()}


def _pick(kind, pos, variant=None, mirror=None):
    """The variant of a hold and whether it is mirrored: from `variant` (a
    name or an index) if given, else from the hold's position."""
    vs = HOLD_VARIANTS[kind]
    h = 2166136261
    for v in (round(pos[0] * 2), round(pos[1] * 2), sum(map(ord, kind))):
        h = ((h ^ (v & 0xffffffff)) * 16777619) & 0xffffffff
    h ^= h >> 15
    h = (h * 0x2C1B3C6D) & 0xffffffff
    h ^= h >> 12
    if variant is None:
        i = h % len(vs)
    elif isinstance(variant, str):
        i = [v["name"] for v in vs].index(variant)
    else:
        i = variant % len(vs)
    flip = bool((h >> 9) & 1) if mirror is None else mirror
    return vs[i], flip and vs[i].get("mirror", False)


def _shape_d(fig, pts, angular, tension=0.9):
    """The path fig.smooth() (or fig.poly() for an angular shape) would draw
    through `pts`."""
    if angular:
        return fig._path_d(pts, True)
    if not fig._pen():
        return fig.smooth_d(pts, True, tension)
    return fig._path_d(fig._smooth_pts(pts, True, tension), True, True)


def _bolt(g, c, r):
    g.circle(c, r, fill=LIGHT, stroke=None)
    g.circle(c, r * 0.42, fill=INK, stroke=None)


def _clipped(fig, d, body, z):
    """Add the SVG `body` clipped to the closed path `d` (a hold's outline).
    The clip's id comes from the path, so builds are identical and figures
    combined into one SVG keep distinct ids."""
    if not body:
        return
    import hashlib
    cid = "hc" + hashlib.md5(d.encode()).hexdigest()[:10]
    fig.add(f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{body}</g>', z)


def _layer(fig):
    g = Fig(fig.x0, fig.y0, fig.x1, fig.y1, fig.scale)
    g._plain = fig._plain
    return g


def _body(g):
    return "".join(s for _, _, s in sorted(g.items))


# The surface of holds and volumes. They are rough as sandpaper and stand out
# from the wall in light from above. So a shape has a lit rim along its upper
# edge, a dark crescent along its lower edge, a shadow on the wall and a grain of
# light and dark specks, more of each where that tone falls. Dots show the grain
# because they print cleanly on the e-ink panel, where a gradient would band.
# Shapes too small to carry any of this stay flat. A faceted volume shows its
# form through its facets, so it only takes the grain and the shadow.
VOLUME_LIT = "#eeeeee"      # the lit rim and light grain of a volume
VOLUME_SHADE = "#999999"    # the dark crescent and dark grain of a volume
ROCK_MIN = 2.4          # mm: a shape's smaller side, below which it stays flat
ROCK_RIM = 0.07         # the lit rim's depth, as a share of that side
ROCK_SHADE = 0.15       # the dark crescent's depth, as a share of that side
ROCK_LIMITS = (0.3, 1.6)    # mm: the smallest and largest depth of either
ROCK_SHADOW = "#dddddd"     # the shadow on the wall
GRAIN_MIN = 3.0         # mm: a hold's smaller side, below which it has no grain
GRAIN_STEP = 0.62       # mm on paper between neighbouring grains
GRAIN_DOT = 0.14        # mm: the radius of the largest grain


def _rock_depth(fig, side, share):
    lo, hi = ROCK_LIMITS
    return max(fig.mm(lo), min(share * side, fig.mm(hi)))


def _side(outline):
    return min(max(p[0] for p in outline) - min(p[0] for p in outline),
               max(p[1] for p in outline) - min(p[1] for p in outline))


def _rock(fig, g, outline, shape, light=HOLD_MID, dark=HOLD_DEEP):
    """Draw the surface of a hold or volume into the layer `g`, which is clipped
    to `outline`, in the greys `light` and `dark`. `shape` returns the path
    through a list of points."""
    side = _side(outline)
    if side * fig.scale < ROCK_MIN:
        return
    d = shape(outline)
    for grey, share, sign in ((light, ROCK_RIM, -1), (dark, ROCK_SHADE, 1)):
        a = sign * _rock_depth(fig, side, share)
        # The two paths overlap except along one edge, and the even-odd rule
        # fills only what they don't share. Past the other edge the clip cuts it.
        moved = shape([(x, y + a) for x, y in outline])
        g.add(f'<path d="{d}{moved}" fill="{grey}" fill-rule="evenodd"/>', 0)
    if side * fig.scale >= GRAIN_MIN:
        _grain(fig, g, outline, light, dark)


def _grain(fig, g, outline, light, dark):
    """Add sandpaper grain to the layer `g`: specks of `light` mostly high on the
    shape and of `dark` mostly low, the same on every build and in every frame
    of a filmstrip."""
    poly = _Poly(outline)
    x0, y0, x1, y1 = poly.box
    step, rmax = fig.mm(GRAIN_STEP), fig.mm(GRAIN_DOT)
    rng = random.Random(f"{x0:.1f},{y0:.1f}")
    dots = {light: [], dark: []}
    y = y0
    while y < y1:
        x = x0
        while x < x1:
            p = (x + rng.uniform(-0.4, 0.4) * step, y + rng.uniform(-0.4, 0.4) * step)
            high = (p[1] - y0) / (y1 - y0)
            roll = rng.random()
            r = rmax * rng.uniform(0.7, 1.0)
            grey = (light if roll < 0.12 + 0.28 * high else
                    dark if roll > 0.88 - 0.28 * (1 - high) else None)
            if grey and poly.has(p):
                px, py = fig.P(p)
                dots[grey].append(f"M{px - r:.2f},{py:.2f}a{r:.2f},{r:.2f} 0 1,0 {2 * r:.2f},0"
                                  f"a{r:.2f},{r:.2f} 0 1,0 {-2 * r:.2f},0")
            x += step
        y += step
    for grey, d in dots.items():
        if d:
            g.add(f'<path d="{"".join(d)}" fill="{grey}"/>', 0)


def _surface(fig, pts, z, smooth, st, light=HOLD_MID, dark=HOLD_DEEP):
    """Add the surface to a hold or volume that a figure draws itself, as an
    outlined shape filled with DARK or VOLUME, and draw its outline again over
    the grain."""
    def shape(q):
        return fig._path_d(q, True, smooth)
    g = _layer(fig)
    _rock(fig, g, pts, shape, light, dark)
    if g.items:
        _clipped(fig, shape(pts), _body(g), z + 0.001)
        fig.add(f'<path d="{shape(pts)}" {fig.style(**dict(st, fill=None))}/>', z + 0.002)


def _panel_grey(value):
    """The grey nearest to `value` (0 to 255) among the panel's 16."""
    v = min(255, max(0, round(value / 17) * 17))
    return f"#{v:02x}{v:02x}{v:02x}"


def _facet_grain(fig, pts, shade, z):
    """Add grain to the facet `pts` of a volume, in specks a little lighter and
    darker than its grey `shade`, and draw its outline again over them."""
    if _side(pts) * fig.scale >= GRAIN_MIN:
        grey = int(shade[1:3], 16)
        g = _layer(fig)
        _grain(fig, g, pts, _panel_grey(grey + 34), _panel_grey(grey - 51))
        _clipped(fig, fig._path_d(pts, True), _body(g), z)
        fig.poly(pts, z=z + 0.001, stroke=INK, sw=0.25)


def _facet_shade(a, b, apex):
    """The grey of a volume's facet between the edge a-b and its apex, lighter
    the more it faces the light from the upper left."""
    faces = dot(norm(sub(lerp(a, b, 0.5), apex)), norm((-0.5, 1)))
    return ("#bbbbbb", "#cccccc", "#dddddd", "#eeeeee")[min(3, int((faces + 1) * 2))]


def _cast_shadow(fig, outline, angular, z):
    """The shadow a hold or volume seen face-on throws down the wall below it."""
    side = _side(outline)
    if side * fig.scale >= ROCK_MIN:
        a = _rock_depth(fig, side, ROCK_SHADE)
        moved = [(x + 0.5 * a, y - a) for x, y in outline]
        fig.add(f'<path d="{_shape_d(fig, moved, angular)}" '
                f'{fig.style(fill=ROCK_SHADOW, stroke=None)}/>', z - 0.01)


def _frame(kind, pos, use, size, w, h, variant, mirror):
    """A hold's variant and the map T from its unit frame to the wall."""
    v, flip = _pick(kind, pos, variant, mirror)
    sw_, sh_ = HOLD_SIZE[kind]
    vx, vy = v.get("size", (1.0, 1.0))
    W = (w or sw_) * size * vx
    H = (h or sh_) * size * vy
    a = use - 90
    fx = -1 if flip else 1

    def T(pts):
        return [add(pos, rot((x * fx * W / 2, y * H / 2), a)) for x, y in pts]
    return v, T, W, H


def hold_outline(kind, pos, use=90, size=1.0, w=None, h=None, variant=None,
                 mirror=None):
    """The outline points of the hold hold() draws with the same arguments."""
    v, T, _, _ = _frame(kind, pos, use, size, w, h, variant, mirror)
    return T(v["outline"])


def _chalked(region):
    """Chalk rubbed off the grabbing surface onto the body: the region moved
    a little away from the lip, by an uneven amount."""
    return [(x, y - 0.13 - 0.05 * math.sin(7.3 * x + 0.8)) for x, y in region]


def _rubber():
    """Black shoe rubber smeared on a foothold's top: two short streaks."""
    return [[(-0.55, 0.6), (-0.2, 0.68), (0.2, 0.64)],
            [(-0.1, 0.42), (0.18, 0.47), (0.42, 0.42)]]


def hold(fig, kind, pos, use=90, size=1.0, z=-5, lip=True, w=None, h=None,
         xray=None, variant=None, mirror=None, chalk=False, rubber=False,
         shadow=True):
    """Draw a hold seen face-on. `use` is the direction (degrees) the grabbed
    surface faces: 90 is a normal downward-pull hold (jug, edge), 270 an
    undercling, 0 or 180 a sidepull or gaston. `variant` picks a shape of
    HOLD_VARIANTS[kind] by name or index (default: chosen by position);
    `mirror` mirrors an asymmetric shape. chalk: chalk rubbed from the
    grabbing surface onto the body; rubber: shoe rubber smeared on a
    foothold. lip=False leaves out the light grabbing surface and the other
    details. shadow=False leaves out the shadow on the wall."""
    v, T, W, H = _frame(kind, pos, use, size, w, h, variant, mirror)
    pw, ph = W * fig.scale, H * fig.scale
    angular = v.get("angular", False)
    outline = T(v["outline"])
    d = _shape_d(fig, outline, angular)
    if shadow:
        _cast_shadow(fig, outline, angular, z)
    fig.add(f'<path d="{d}" {fig.style(fill=DARK, stroke=None)}/>', z)
    g = _layer(fig)
    if lip:
        _rock(fig, g, outline, lambda q: _shape_d(fig, q, angular))
        for item in v.get("fills", ()):
            if len(item) > 2 and ph < item[2]:
                continue
            if chalk and item[0] == WHITE:
                g.poly(T(_chalked(item[1])), fill=HOLD_LIGHT, stroke=None)
            g.poly(T(item[1]), fill=item[0], stroke=None)
        if rubber and ph >= 1.5:
            for r in _rubber():
                g.poly(T(r), closed=False, stroke=DARK, sw=0.26)
        if ph >= 2.8:
            for ln in v.get("lines", ()):
                g.poly(T(ln), closed=False, stroke=INK, sw=0.22)
        top = v.get("stipple")
        if top and pw >= 3.5:
            r = fig.mm(0.09)
            for p in _stipple(top, step=max(0.12, fig.mm(0.55) * 2 / W)):
                g.circle(T([p])[0], r, fill=HOLD_MID, stroke=None)
        if pw >= 7.0:
            for col, ln in v.get("strokes", ()):
                g.poly(T(ln), closed=False, stroke=col, sw=0.22)
    rb = min(W, H) * 0.11
    if rb * fig.scale >= 0.26 and min(pw, ph) >= 2.1:
        for c in v.get("bolts", ()):
            _bolt(g, T([c])[0], rb)
    if ph >= 1.8:
        for c in v.get("screws", ()):
            g.circle(T([c])[0], max(min(W, H) * 0.05, fig.mm(0.16)),
                     fill=LIGHT, stroke=None)
    _clipped(fig, d, _body(g), z + 0.01)
    fig.add(f'<path d="{d}" {fig.style(fill=None, stroke=INK, sw=0.3)}/>', z + 0.02)
    if XRAY if xray is None else xray:
        if angular:
            fig.poly(outline, z=XRAY_Z, **XRAY_STYLE)
        else:
            fig.smooth(outline, z=XRAY_Z, tension=0.9, **XRAY_STYLE)
    return pos


def grip(pos, use=90, kind="jug", size=1.0):
    """Where to put a hand so that the hold stays visible: the hand sits on
    the grabbed lip, slightly past the hold centre."""
    h = HOLD_SIZE[kind][1] * size
    return add(pos, mul(ang(use), h * 0.45))


def stand(pos, kind="foot", size=1.0):
    """Toe or heel contact point on top of a foothold."""
    return add(pos, (0, HOLD_SIZE[kind][1] * size * 0.55))


def wall_grid(fig, step=20, z=-40, x0=None, x1=None, y0=None, y1=None):
    """Bolt holes on an indoor wall panel."""
    x0 = fig.x0 if x0 is None else x0
    x1 = fig.x1 if x1 is None else x1
    y0 = max(fig.y0, 3) if y0 is None else y0
    y1 = fig.y1 if y1 is None else y1
    x = math.ceil(x0 / step) * step
    while x <= x1:
        y = math.ceil(y0 / step) * step
        while y <= y1:
            fig.circle((x, y), fig.mm(0.32), z=z, fill="#b0b0b0", stroke=None)
            y += step
        x += step


def volume(fig, outline, apex=None, z=-12, shades=None, hatch=False, bolt=False,
           shadow=True):
    """A volume seen face-on: an outline polygon, optionally split into facets
    meeting at `apex` (a point inside the outline) to suggest 3D. Each facet takes
    its grey from `shades`, or else from how far it faces the light. bolt: the
    bolt that holds it to the wall, at the apex, as on a hold. shadow=False leaves
    out the shadow on the wall."""
    if shadow:
        _cast_shadow(fig, outline, True, z)
    fig.poly(outline, z=z, fill=PALE, stroke=INK, sw=0.35)
    if apex is None:
        _facet_grain(fig, outline, PALE, z + 0.01)
    else:
        n = len(outline)
        for i in range(n):
            a, b = outline[i], outline[(i + 1) % n]
            shade = shades[i % len(shades)] if shades else _facet_shade(a, b, apex)
            fig.poly([a, b, apex], z=z + 0.1, fill=shade, stroke=INK, sw=0.25)
            _facet_grain(fig, [a, b, apex], shade, z + 0.11)
        if bolt:
            g = _layer(fig)
            r = max(fig.mm(0.42), 1.4)
            # a metal bolt, a touch off DARK so that it doesn't take a hold's colour
            g.circle(apex, r, fill="#565656", stroke=None)
            g.circle(apex, r * 0.62, fill=LIGHT, stroke=None)
            g.circle(apex, r * 0.26, fill=INK, stroke=None)
            fig.add(_body(g), z + 0.2)
    if hatch:
        pass


# Profiles for hold_side(): the outline in cm (x out of the wall, y up it),
# the indices of its points on the wall (kept sharp, the rest rounded), the
# run of points along the grabbed surface, which side of that run the body
# lies (-1 below, +1 above) and the light bands along it as (shade, depth
# in cm), lightest last.
HOLD_PROFILES = {
    "jug": ([(0, -4), (5, -3.5), (8, 0), (7.5, 3.5), (5.5, 2.0), (3, 1.5),
             (0, 3)], (0, 6), (3, 4, 5, 6), -1, [(WHITE, 1.1)]),
    "crimp": ([(0, -2), (2.2, -1.5), (2.4, 0.6), (0, 1.0)], (0, 3), (2, 3),
              -1, [(WHITE, 0.6)]),
    "sloper": ([(0, -7), (4, -6), (6.5, -2), (6, 2), (3, 5), (0, 6)], (0, 5),
               (2, 3, 4, 5), -1, [(HOLD_MID, 3.2), (HOLD_LIGHT, 2.0), (WHITE, 0.9)]),
    "foot": ([(0, -2.5), (3, -2), (3.4, 0.5), (0, 1.2)], (0, 3), (2, 3), -1,
             [(WHITE, 0.6)]),
    "edge": ([(0, -3), (3.5, -2.5), (3.8, 0.3), (0, 0.8)], (0, 3), (2, 3), -1,
             [(WHITE, 0.7)]),
    "undercling": ([(0, 4), (5, 3.5), (8, 0), (7.5, -3.5), (5.5, -2.0),
                    (3, -1.5), (0, -3)], (0, 6), (3, 4, 5, 6), 1,
                   [(WHITE, 1.1)]),
}


def _round(pts, sharp, k=0.38, n=5):
    """A closed polygon with its corners rounded, except those in `sharp`."""
    out, m = [], len(pts)
    for i, v in enumerate(pts):
        if i in sharp:
            out.append(v)
            continue
        p0, p2 = lerp(v, pts[i - 1], k), lerp(v, pts[(i + 1) % m], k)
        for j in range(n + 1):
            t = j / n
            out.append(add(add(mul(p0, (1 - t) ** 2), mul(v, 2 * t * (1 - t))),
                           mul(p2, t * t)))
    return out


def hold_side(fig, kind, pos, angle=0, size=1.0, z=-5, xray=None, frame=None):
    """A hold in side profile on a wall whose surface passes through `pos`.
    The wall is to the right; `angle` is the wall overhang angle. Drawn as
    hold() draws a hold face-on: a dark body, its grabbed surface light.
    `frame` replaces `angle` with the unit vectors (out of the wall, up the
    wall), e.g. ((0, -1), (-1, 0)) for a jug on a ceiling, its lip facing
    left."""
    if frame:
        n, d = frame
    else:
        d = norm((-math.tan(math.radians(angle)), 1))   # up the wall
        n = (-d[1], d[0])                                # out of the wall (left)
    s = size
    shape, sharp, run, side, bands = HOLD_PROFILES[kind]

    def T(q):
        return add(pos, add(mul(n, q[0] * s), mul(d, q[1] * s)))

    pts = [T(q) for q in _round(shape, sharp)]
    dd = fig._path_d(pts, True)
    fig.add(f'<path d="{dd}" {fig.style(fill=DARK, stroke=None)}/>', z)
    edge = [T(shape[i]) for i in run]
    g = _layer(fig)
    _rock(fig, g, pts, lambda q: fig._path_d(q, True))
    for shade, depth in bands:
        t = max(depth * s, fig.mm(0.3) * depth / bands[-1][1])
        g.poly(edge + [add(p, mul(d, side * t)) for p in edge[::-1]],
               fill=shade, stroke=None)
    _clipped(fig, dd, _body(g), z + 0.01)
    fig.add(f'<path d="{dd}" {fig.style(fill=None, stroke=INK, sw=0.3)}/>', z + 0.02)
    if XRAY if xray is None else xray:
        fig.poly(pts, z=XRAY_Z, **XRAY_STYLE)
    return pos


def volume_side(fig, pos, w, h, angle=0, top=0.5, z=-12):
    """A triangular volume in profile, bolted to the wall at `pos` (bottom
    corner). `w` sticks out of the wall, `h` runs up the wall."""
    d = norm((-math.tan(math.radians(angle)), 1))
    n = (-d[1], d[0])
    p0 = pos
    p1 = add(pos, mul(d, h))
    p2 = add(add(pos, mul(d, h * top)), mul(n, w))
    fig.poly([p0, p2, p1], z=z, fill=VOLUME, stroke=INK, sw=0.35)
    return p0, p2, p1


# ---------------------------------------------------------------- climber

DIM = dict(
    torso=48, neck=7, head_rx=7.8, head_ry=10.4, head_side_rx=9.6,
    sh_half=18, hip_half=8.5,
    upper_arm=31, forearm=27, hand=7,     # hand: wrist to the middle of the grip
    thigh=45, shin=44,
    r_shoulder=5.0, r_elbow=3.7, r_wrist=2.8, r_hand=3.9,
    r_hip=7.8, r_knee=5.0, r_ankle=3.4,
)


def ik(root, target, l1, l2, choose):
    """Two-bone IK. Returns (joint, end). `choose(c1, c2)` picks between the
    two joint solutions. If the target is out of reach the limb points at it
    fully straight."""
    v = sub(target, root)
    d = length(v)
    u = norm(v)
    if d >= l1 + l2 - 1e-6:
        return add(root, mul(u, l1)), add(root, mul(u, l1 + l2))
    d = max(d, abs(l1 - l2) + 1e-3)
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(l1 * l1 - a * a, 0))
    m = add(root, mul(u, a))
    c1 = add(m, mul(perp(u), h))
    c2 = add(m, mul(perp(u), -h))
    return choose(c1, c2), target


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def chooser(mode, side_sign, axis_point, right_vec):
    """Returns a function choosing an elbow/knee position.

    mode: out | in | up | down | left | right"""
    def f(c1, c2):
        def score(c):
            if mode == "up":
                return c[1]
            if mode == "down":
                return -c[1]
            if mode == "left":
                return -c[0]
            if mode == "right":
                return c[0]
            s = dot(sub(c, axis_point), right_vec) * side_sign
            return s if mode == "out" else -s
        return c1 if score(c1) >= score(c2) else c2
    return f


def anatomical(root, target, sign):
    """Chooser for side views: the joint bends the way a real elbow (sign +1)
    or knee (sign -1) bends for a climber facing right."""
    def f(c1, c2):
        def ok(c):
            return cross(sub(c, root), sub(target, c)) * sign >= 0
        return c1 if ok(c1) else c2
    return f


SHOE_FILL = "#262626"
SHOE = [(0, 1.5), (4, 0), (16, 0), (21, 0.5), (24.5, 2.6), (23, 5.6),
        (14, 8.2), (8, 11.5), (7.5, 14.5), (0, 13.5), (-1.6, 7), (-1.2, 3)]
SHOE_ANKLE = (3.5, 9.0)
SHOE_TOE = (23.0, 1.0)
SHOE_HEEL = (0.0, 1.5)
# where on the shoe the foot touches the hold
SHOE_CONTACTS = {"toe": SHOE_TOE,       # the very tip (front-pointing, toe hooks)
                 "edge": (18.5, 0.2),   # inside or outside edge near the ball
                 "ball": (15.0, 0.0)}   # smearing / standing on the ball
SHOE_BACK = [(-4.5, 0), (4.5, 0), (5.2, 4), (4.6, 12), (-4.6, 12), (-5.2, 4)]


def limb_outline(p1, r1, p2, r2, bulge=0.0, at=0.35, side=0, n=9):
    """Outline of one limb segment: a tapered tube with round ends and an
    optional muscle bulge peaking at fraction `at` of its length. `side` 0
    bulges both sides, +1 only the left of p1->p2, -1 only the right."""
    v = sub(p2, p1)
    L = length(v)
    if L < 1e-6:
        return [add(p1, mul(ang(i * 20), max(r1, r2))) for i in range(18)]
    d = mul(v, 1 / L)
    nv = perp(d)

    def rad(t, which):
        r = r1 + (r2 - r1) * t
        if bulge and (side == 0 or side == which):
            k = math.sin(math.pi / 2 * t / at) if t < at else \
                math.cos(math.pi / 2 * (t - at) / (1 - at))
            r += bulge * k * k
        return r
    ts = [i / n for i in range(n + 1)]
    left = [add(add(p1, mul(d, L * t)), mul(nv, rad(t, 1))) for t in ts]
    right = [add(add(p1, mul(d, L * t)), mul(nv, -rad(t, -1))) for t in ts]
    cap2 = [add(p2, mul(rot(nv, -a), r2)) for a in range(15, 180, 15)]
    cap1 = [add(p1, mul(rot(mul(nv, -1), -a), r1)) for a in range(15, 180, 15)]
    return left + cap2 + right[::-1] + cap1


def ellipse_pts(c, rx, ry, deg=0.0, n=40):
    return [add(c, rot((rx * math.cos(2 * math.pi * i / n),
                        ry * math.sin(2 * math.pi * i / n)), deg))
            for i in range(n)]


def catmull(pts, closed=True, k=6):
    """Sample a smooth closed curve through `pts` into a dense polygon."""
    n = len(pts)
    out = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        for j in range(k):
            t = j / k
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[q]) + (-p0[q] + p2[q]) * t +
                                    (2 * p0[q] - 5 * p1[q] + 4 * p2[q] - p3[q]) * t2 +
                                    (-p0[q] + 3 * p1[q] - 3 * p2[q] + p3[q]) * t3)
                             for q in (0, 1)))
    return out


def silhouette(fig, shapes, z, fill, stroke=INK, sw=0.32, dash=None):
    """Draw overlapping shapes as one outlined silhouette: outlines first
    (twice as wide, so half shows), then the fills over the inner lines."""
    for pts in shapes:
        fig.poly(pts, z=z, fill=fill, stroke=stroke, sw=sw * 2, dash=dash)
    for pts in shapes:
        fig.poly(pts, z=z + 0.001, fill=fill, stroke=None)


def _seg_cross(a, b, c, d):
    """True if segments ab and cd properly intersect."""
    def o(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (o(a, b, c) * o(a, b, d) < 0) and (o(c, d, a) * o(c, d, b) < 0)


def J_tmp(c, s, joint):
    return c._J[s + joint]


# ---------------------------------------------------------------- body shapes
# How the climber is drawn: a clothed figure (T-shirt with short sleeves,
# long trousers, climbing shoes) built from smooth anatomical outlines.
# Sizes are in cm at scale 1. They only change the drawing: the joints
# (Climber.J) come from DIM alone.
#
# Each body part (torso with head, an arm, a leg) is drawn as one group:
# the outlines of its pieces first, at twice the line width, then their
# fills, so only the outer contour of the group shows; then the shades of
# the muscles at work, and the few inner lines: the hems of the T-shirt and
# its sleeves, and in profile the ear. The silhouette and the fills carry
# the rest, so there are no seams, creases, finger lines or hairline. Where
# a limb grows out of the torso, the limb's outline is left out inside the
# torso near the joint (and the trouser seat's outline inside its own
# thigh), so the shoulder and the hip read as one contour; further from the
# joint a limb passing in front of the body keeps its full outline.

HAIR = "#6e6e6e"
LINE_SW = 0.24          # inner lines: hems (mm)
FINE_SW = 0.22          # the ear (mm)

# radius profiles [(t, r)] along a limb segment, t = 0 at the upper joint
SLEEVE_LEN = 0.34       # the short sleeve covers this much of the upper arm
SLEEVE = [(0, 5.8), (0.5, 5.5), (1, 4.9)]
# the upper arm is not a tube: on its outer side the deltoid rounds the
# shoulder and ends a third of the way down; on its inner side the biceps
# (or triceps) swells below that. In a side view the inner side is the one
# the elbow bends toward.
UPPER_ARM_OUT = [(0, 5.4), (0.2, 5.0), (0.42, 4.0), (0.7, 3.9), (1, 3.5)]
UPPER_ARM_IN = [(0, 4.7), (0.3, 4.0), (0.58, 4.3), (0.85, 3.8), (1, 3.5)]
FORE_RADIAL = [(0, 3.6), (0.18, 4.2), (0.5, 3.5), (0.85, 2.7), (1, 2.5)]
FORE_ULNAR = [(0, 3.6), (0.3, 3.8), (0.62, 3.1), (0.88, 2.6), (1, 2.5)]
THIGH_FRONT = [(0, 8.0), (0.3, 8.1), (0.65, 7.0), (1, 5.6)]
THIGH_BACK = [(0, 8.3), (0.2, 8.1), (0.55, 6.8), (0.85, 5.9), (1, 5.6)]
# in profile the back of the thigh starts with the buttock
THIGH_BACK_SIDE = [(0, 10.0), (0.1, 10.2), (0.24, 8.4), (0.55, 6.8), (0.85, 5.9),
                   (1, 5.6)]
SHIN_FRONT = [(0, 5.5), (0.35, 5.0), (0.75, 4.6), (1, 4.4)]
SHIN_BACK = [(0, 5.5), (0.25, 5.9), (0.6, 5.0), (1, 4.4)]
HEM_ABOVE_ANKLE = 3.5   # trouser hem, measured up the shin from the ankle
BACK_ANKLE_MIN = 33     # the lowest shin-to-foot angle that passes in a back view

# A muscle at work is stippled: dots, largest at its belly and shrinking
# toward its ends and edges, with no outline (see Climber, `active`). Dots
# can't be mistaken for the flat grey of the left limbs, show as well on
# grey as on white, and print cleanly on the e-ink panel, where a gradient
# would band. MUSCLE_DOTS is the dots' colour, keyed by the fill under them, and
# paint.py turns this grey red. It's dark enough to show on the left limbs' grey.
# The dots are large and sparse enough to stay dots on the panel at 197 dpi
# (research/eink-report.md); smaller ones blur into a faint grey.
MUSCLE_DOTS = {WHITE: "#545454", LEFT: "#545454"}
MUSCLE_BAND = "#cacaca"     # the band over a chain of muscles held tight
STIPPLE_STEP = 0.6      # mm on paper between neighbouring dots
STIPPLE_DOT = 0.19      # mm: the radius of the largest dot
STIPPLE_FALL = 0.9      # how fast the dots shrink toward the edge
# patches on the torso, seen from behind, (s, t) as for the shirt; the right
# side, mirrored for the left. The lat runs from the armpit down and in.
LAT_BACK = [(15.6, 41.2), (17.4, 38.2), (16.6, 32.0), (15.2, 26.0), (13.4, 20.4),
            (10.8, 21.2), (8.8, 26.4), (9.4, 32.6), (11.8, 38.4)]
GLUTE_BACK = ((7.6, -2.6), 4.8, 4.6)           # centre, half-width, half-height
CORE_BACK = [(1.4, 31.0), (3.8, 29.0), (4.4, 19.0), (3.8, 9.5), (1.4, 8.0)]
# and in profile (s forward): the abdominals
CORE_SIDE = [(9.2, 34.0), (10.2, 27.0), (9.6, 18.0), (9.2, 10.6), (7.0, 10.6),
             (6.8, 20.0), (7.4, 30.0)]
SHOULDER_R = (5.6, 4.3)  # the torso rounds each shoulder joint (across, up)
# the head is drawn this much higher than Climber.J["head"] (the skeleton's
# neck is a little short) and at this size, for a longer neck and a smaller
# head, as in a well-proportioned figure
HEAD_RAISE = 2.0
HEAD_SIZE = 0.96
# the spine bends (Climber, `bend`) round this point, in cm above the hip
# joints, spread over this much of it either way
WAIST_T = 22.0
WAIST_SPAN = 10.0

# hands, in a frame with x from the wrist toward the grip (the grip point is
# at x = 7) and y across the hand, positive on the thumb side
HAND_GRIP = [(0, -2.5), (2.6, -3.0), (5.4, -3.4), (7.6, -3.5), (9.8, -3.2),
             (11.4, -2.6), (12.2, -1.3), (12.4, 0.4), (12.0, 2.0), (11.0, 3.1),
             (9.0, 3.6), (8.7, 4.5), (7.4, 5.1), (5.4, 4.9), (3.4, 4.0),
             (1.4, 2.9), (0, 2.5)]
HAND_HANG = [(0, -2.4), (3.0, -2.9), (6.4, -3.1), (9.6, -2.6), (11.6, -1.4),
             (12.0, 0.2), (11.2, 1.8), (9.0, 2.9), (6.0, 3.4), (3.0, 3.1), (0, 2.5)]

# head seen from behind (x to the right, y up the spine, centred on
# Climber.J["head"]); the right half, mirrored for the left
HEAD_BACK = [(0, 10.4), (3.7, 10.0), (6.3, 8.2), (7.7, 5.0), (8.0, 1.6),
             (7.7, -2.0), (7.1, -4.8), (6.0, -7.6), (4.4, -9.6), (2.0, -10.6)]
EAR_BACK = [(7.3, 1.7), (8.5, 1.6), (9.1, 0.1), (8.9, -2.4), (8.2, -4.3), (7.1, -4.9)]
HAIRLINE_BACK = [(7.5, -3.6), (6.4, -5.6), (3.4, -6.0), (0, -5.9)]

# head in profile, facing right (x forward)
HEAD_SIDE = [(0.6, 10.4), (4.6, 9.6), (7.4, 7.4), (8.9, 4.4), (9.3, 2.0),
             (8.9, 0.7), (9.9, -0.8), (10.9, -2.4), (9.4, -3.2), (9.6, -4.4),
             (9.2, -5.4), (9.4, -6.3), (9.1, -7.6), (7.6, -9.1), (4.6, -8.8),
             (1.4, -7.6), (-0.8, -6.4), (-3.6, -6.6), (-5.8, -7.0), (-7.6, -5.2),
             (-9.2, -2.2), (-9.6, 1.2), (-8.6, 5.2), (-5.6, 8.7), (-2.2, 10.2)]
HAIR_SIDE_EDGE = [(-7.7, -5.0), (-5.8, -4.6), (-4.2, -2.6), (-3.0, 0.2),
                  (-2.4, 2.6), (0.0, 3.2), (1.6, 2.2), (1.8, -0.8), (3.0, 1.6),
                  (4.6, 4.6), (6.2, 6.6), (7.0, 7.7)]
EAR_SIDE = [(-1.6, 1.4), (0.0, 1.0), (0.4, -0.6), (-0.1, -2.8), (-1.0, -3.4),
            (-2.0, -2.0), (-2.2, 0.2)]
EYE_SIDE = (6.6, 0.7)

# torso seen from behind: (s, t) with s to the right, t up the spine from the
# hip joints; right half, from the neck down to the hem (the shoulder is an
# arc around the shoulder joint, inserted between)
# the shoulders slope down from the neck over the trapezius, and the back
# narrows from the lats to the waist
SHIRT_BACK_TOP = [(5.0, 54.6), (8.6, 53.6), (12.4, 51.9)]
SHIRT_BACK_SIDE = [(18.8, 39.0), (17.9, 33.5), (16.6, 26.5), (15.4, 19.5),
                   (15.3, 12.5), (16.2, 4.4)]
SHIRT_BACK_HEM = [(8.0, 3.0), (0, 2.6)]
SEAT_BACK = [(14.8, 8.0), (16.0, 3.0), (16.4, -2.0), (15.4, -5.6), (12.0, -8.2),
             (7.0, -10.2), (0.6, -11.0)]

# torso in profile (s forward, toward the wall)
SHIRT_SIDE = [(4.4, 52.4), (8.6, 49.0), (11.4, 44.0), (12.6, 37.5), (12.0, 31.5),
              (10.8, 25.0), (10.4, 17.0), (10.6, 10.0), (10.7, 4.8), (5.0, 3.8),
              (-4.0, 3.2), (-12.2, 3.8), (-11.6, 9.0), (-8.6, 18.5), (-9.6, 27.0),
              (-11.4, 36.0), (-11.6, 43.5), (-9.6, 49.5), (-6.6, 53.2),
              (-3.8, 54.6), (-1.0, 54.4), (2.0, 53.6)]
SEAT_SIDE = [(10.4, 9.5), (9.8, 3.0), (8.6, -2.0), (5.5, -6.5), (0.0, -8.5),
             (-5.5, -8.5), (-10.0, -6.0), (-12.2, -1.5), (-12.4, 3.5),
             (-11.4, 9.0), (0, 10.5)]


class _Poly:
    """A polygon with a bounding box, for point-in-polygon tests."""

    def __init__(self, pts):
        self.pts = pts
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.box = (min(xs), min(ys), max(xs), max(ys))

    def has(self, p):
        x, y = p
        b = self.box
        if x < b[0] or x > b[2] or y < b[1] or y > b[3]:
            return False
        pts, inside = self.pts, False
        xj, yj = pts[-1]
        for xi, yi in pts:
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                inside = not inside
            xj, yj = xi, yi
        return inside


def _near_inside(c, R, polys, also=None):
    """Predicate: a point within R of c that lies inside one of `polys`
    (and satisfies `also`, if given)."""
    R2 = R * R

    def f(p):
        dx, dy = p[0] - c[0], p[1] - c[1]
        if dx * dx + dy * dy > R2:
            return False
        if also is not None and not also(p):
            return False
        return any(q.has(p) for q in polys)
    return f


def _root_hide(root, joint, R, polys):
    """Predicate for the outline points of a limb segment root->joint that
    merge into the torso: inside it, within R of the root and in the first
    part of the segment (so a foreshortened limb keeps its elbow or knee)."""
    v = sub(joint, root)
    L = length(v)
    d = mul(v, 1 / L) if L > 1e-6 else (0.0, 0.0)
    lim = min(R, 0.45 * L)
    return _near_inside(root, R, polys, lambda p: dot(sub(p, root), d) < lim)


def _runs(pts, hidden):
    """The visible stretches of the closed outline `pts`: a list of
    (points, closed). `hidden(p)` says which points to leave out."""
    if hidden is None:
        return [(pts, True)]
    n = len(pts)
    vis = [not hidden(p) for p in pts]
    if all(vis):
        return [(pts, True)]
    if not any(vis):
        return []

    def edge(a, b):
        # a hidden, b visible: the point where the outline comes into view
        lo, hi = 0.0, 1.0
        for _ in range(7):
            m = (lo + hi) / 2
            if hidden(lerp(a, b, m)):
                lo = m
            else:
                hi = m
        return lerp(a, b, hi)
    start = next(i for i in range(n) if not vis[i] and vis[(i + 1) % n])
    runs, cur = [], None
    for k in range(1, n + 1):
        i = (start + k) % n
        prev = (i - 1) % n
        if vis[i]:
            if cur is None:
                cur = [edge(pts[prev], pts[i])]
            cur.append(pts[i])
        elif cur is not None:
            cur.append(edge(pts[i], pts[prev]))
            runs.append((cur, False))
            cur = None
    return runs


def _outward(pts, d):
    """The closed outline `pts` moved outward by d."""
    n = len(pts)
    area = sum(cross(pts[i], pts[(i + 1) % n]) for i in range(n))
    out = []
    for i in range(n):
        t = norm(sub(pts[(i + 1) % n], pts[i - 1]))
        nv = (t[1], -t[0]) if area > 0 else (-t[1], t[0])
        out.append(add(pts[i], mul(nv, d)))
    return out


def _profile(ctrl, t):
    """Smooth (cubic Hermite) interpolation of a radius profile [(t, r)]."""
    n = len(ctrl)
    if t <= ctrl[0][0]:
        return ctrl[0][1]
    if t >= ctrl[-1][0]:
        return ctrl[-1][1]
    i = 0
    while ctrl[i + 1][0] < t:
        i += 1
    (t0, r0), (t1, r1) = ctrl[i], ctrl[i + 1]

    def slope(j):
        a, b = ctrl[max(j - 1, 0)], ctrl[min(j + 1, n - 1)]
        return (b[1] - a[1]) / (b[0] - a[0])
    h = t1 - t0
    x = (t - t0) / h
    m0, m1 = slope(i) * h, slope(i + 1) * h
    return ((2 * x ** 3 - 3 * x ** 2 + 1) * r0 + (x ** 3 - 2 * x ** 2 + x) * m0 +
            (-2 * x ** 3 + 3 * x ** 2) * r1 + (x ** 3 - x ** 2) * m1)


def _cap(c, d, nv, rl, rr, depth):
    """End cap around c from c + nv*rl to c - nv*rr, bulging along d."""
    if depth <= 0:
        return []
    a, off = (rl + rr) / 2, (rl - rr) / 2
    cc = add(c, mul(nv, off))
    return [add(cc, add(mul(nv, a * math.cos(math.pi * k / 8)),
                        mul(d, a * math.sin(math.pi * k / 8) * depth)))
            for k in range(1, 8)]


def tube(p1, p2, left, right, scale=1.0, cap1=1.0, cap2=1.0, n=14):
    """Closed outline of a body segment from p1 to p2 whose half-widths
    follow the radius profiles `left` and `right` ([(t, r)], t from 0 at p1
    to 1 at p2; left is the side of perp(p2 - p1)). cap1/cap2: depth of the
    end caps (1 round, 0 flat)."""
    v = sub(p2, p1)
    L = length(v)
    d = mul(v, 1 / L) if L > 1e-6 else (0.0, 1.0)
    nv = perp(d)
    ts = [i / n for i in range(n + 1)]
    lt = [add(add(p1, mul(d, L * t)), mul(nv, _profile(left, t) * scale)) for t in ts]
    rt = [add(add(p1, mul(d, L * t)), mul(nv, -_profile(right, t) * scale)) for t in ts]
    rl1, rr1 = _profile(left, 1) * scale, _profile(right, 1) * scale
    rl0, rr0 = _profile(left, 0) * scale, _profile(right, 0) * scale
    return (lt + _cap(p2, d, nv, rl1, rr1, cap2) + rt[::-1] +
            _cap(p1, mul(d, -1), mul(nv, -1), rr0, rl0, cap1))


def belly(p1, p2, left, right, scale, t0, t1, w=1.0, bias=0.0, inset=0.0, peak=0.5):
    """The outline of a muscle's shade in the segment p1 -> p2 whose radius
    profiles are `left` and `right` (as for tube): from t0 to t1 along it,
    `w` of the radius wide at its fullest (at `peak` of its length), its
    middle moved `bias` of the radius toward the left side (negative: the
    right), and kept `inset` inside the outline. It fills the limb along
    most of its length and rounds off toward the ends, so the shade covers
    the muscle rather than a spot on it."""
    v = sub(p2, p1)
    L = length(v)
    d = mul(v, 1 / L) if L > 1e-6 else (0.0, 1.0)
    nv = perp(d)
    n = 18
    lt, rt = [], []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        rl, rr = _profile(left, t) * scale, _profile(right, t) * scale
        x = i / n
        x = 0.5 * x / peak if x < peak else 0.5 + 0.5 * (x - peak) / (1 - peak)
        e = math.sin(math.pi * x) ** 0.4
        c = bias * (rl if bias > 0 else rr)
        a = min(c + w * rl * e, rl - inset)
        b = max(c - w * rr * e, inset - rr)
        base = add(p1, mul(d, L * t))
        lt.append(add(base, mul(nv, a)))
        rt.append(add(base, mul(nv, min(a, b))))
    return lt + rt[::-1]


def _frame_pts(o, x, y, pts, sx=1.0, sy=1.0):
    """Points (a, b) of a local frame at o with axes x and y, scaled."""
    return [add(o, add(mul(x, a * sx), mul(y, b * sy))) for a, b in pts]


def _walk(poly, start, away, dist, other):
    """The point `dist` along the outline `poly` from its point nearest to
    `start` that lies outside `other`, walking in the direction `away`."""
    out = [i for i, p in enumerate(poly) if not other.has(p)]
    if not out:
        return None
    i0 = min(out, key=lambda i: length(sub(poly[i], start)))
    n = len(poly)
    step = 1 if dot(sub(poly[(i0 + 1) % n], poly[(i0 - 1) % n]), away) > 0 else -1
    p, acc, i = poly[i0], 0.0, i0
    for _ in range(n):
        q = poly[(i + step) % n]
        L = length(sub(q, p))
        if acc + L >= dist:
            return lerp(p, q, (dist - acc) / L) if L > 1e-9 else q
        acc += L
        p, i = q, (i + step) % n
    return p


def _fillet(root, joint, end, upper, lower, reach, crease, S):
    """Soften the inner corner of a bent elbow or knee. `upper` and `lower`
    are the outlines of the two segments meeting at `joint`. Returns a piece
    that fills the notch where their inner contours cross with a smooth
    curve running from `reach` up one contour to `reach` down the other, and
    a short crease line `crease` long from that curve toward the joint; or
    (None, None) for a straight or tightly folded joint."""
    a, b = norm(sub(root, joint)), norm(sub(end, joint))
    cosk = dot(a, b)
    if not -0.92 < cosk < 0.8:
        return None, None
    bis = norm(add(a, b))
    A, B = _Poly(upper), _Poly(lower)
    k = 1.0
    while k < 20 and (A.has(add(joint, mul(bis, k * S))) or
                      B.has(add(joint, mul(bis, k * S)))):
        k += 0.2
    if k >= 20:
        return None, None
    C = add(joint, mul(bis, (k - 0.1) * S))          # the notch
    reach = min(reach, 0.3 * length(sub(root, joint)), 0.3 * length(sub(end, joint)))
    pa = _walk(upper, C, a, reach, B)
    pb = _walk(lower, C, b, reach, A)
    if pa is None or pb is None:
        return None, None
    curve = [add(add(mul(pa, (1 - t) ** 2), mul(C, 2 * t * (1 - t))), mul(pb, t * t))
             for t in (i / 10 for i in range(11))]
    # tuck the ends into the segments, so only the curve shows
    piece = [add(pa, mul(norm(sub(joint, pa)), 1.2 * S))] + curve + \
        [add(pb, mul(norm(sub(joint, pb)), 1.2 * S)), joint]
    m = curve[5]
    line = [m, add(m, mul(norm(sub(joint, m)), crease))] if crease else None
    return piece, line


def shoe_details(fig, P, z):
    """Sole, rand and strap lines on a dark profile shoe. P maps shoe
    coordinates (heel at x=0, sole at y=0, toe at +x; see SHOE) to world
    points."""
    fig.poly([P(*q) for q in ((1.0, 2.3), (12.0, 2.15), (21.5, 2.0))], closed=False,
             z=z, sw=0.22, stroke=WHITE)
    rand = [(-1.3, 5.4), (2.0, 4.1), (8.5, 3.7), (13.5, 4.2), (16.6, 5.5), (18.4, 6.9)]
    fig.smooth([P(*q) for q in rand], closed=False, z=z, sw=0.17, stroke="#9a9a9a")
    for a, b in (((9.6, 10.6), (7.0, 3.9)), ((11.5, 9.5), (9.0, 3.8))):
        fig.line(P(*a), P(*b), z=z, sw=0.17, stroke="#9a9a9a")


def _draw_group(fig, z, pieces, lines, st):
    """Draw pieces as one outlined group: every outline at twice the line
    width, then the fills on top, so only the outer contour shows; then the
    inner lines. A piece is a dict: pts, fill, hide (predicate for outline
    points to leave out), stroke (False: fill only)."""
    for pc in pieces:
        if pc.get("stroke", True):
            for run, closed in _runs(pc["pts"], pc.get("hide")):
                # an open stretch ends where the outline runs into another
                # part: a round cap there would leave a blob on that part
                fig.poly(run, closed=closed, z=z, fill=None, stroke=st["stroke"],
                         sw=st["sw"] * 2, dash=st.get("dash"), taper=False,
                         cap="round" if closed else "butt")
    for pc in pieces:
        if pc.get("fill"):
            fig.poly(pc["pts"], z=z + 0.001, fill=pc["fill"], stroke=None,
                     ghost=st.get("ghost", False))
    for ln in lines:
        ln = dict(ln)
        pts = ln.pop("pts")
        closed = ln.pop("closed", False)
        dots = ln.pop("dots", None)
        if dots:
            c, u, ra, rb, focus, colour = dots
            fig.stipple(pts, c, u, ra, rb, colour, focus, z=z + 0.002)
            continue
        st_ = dict(fill=None, stroke=st["stroke"], sw=LINE_SW, dash=st.get("dash"))
        st_.update(ln)
        fig.poly(pts, closed=closed, z=z + 0.002, **st_)


class Climber:
    """A mannequin climber.

    view: "back" (seen from behind, facing the wall) or "side" (profile,
    facing right, wall on the right).

    pelvis: (x, y) world point between the hip joints. Alternatively pass
      shoulders=(x, y), the point between the shoulders, and pelvis=None.
    lean: spine angle from vertical in degrees; positive tips the shoulders
      to the right of the hips (in side view: toward the wall).
    bend: degrees the spine bends at the waist, the chest, shoulders and
      head turning further than the hips the same way as `lean` (a back view
      bends sideways; a side view curls forward, negative arches back). The
      hands and feet stay where they are put.
    turn: back view only, -1..1. Positive turns the right hip into the wall
      (the back then faces right and the left side comes toward you).
    lh, rh: hand positions: where the middle of the hand grips (None = the
      arm hangs).
    lf, rf: feet. A tuple is a toe placement with the foot pointing outward
      (inside edge on the hold). A dict allows: at, angle (heel-to-toe
      direction in degrees), contact ("edge" default | "toe" | "ball" |
      "heel"), style ("profile" | "back" for a foot pointing into the wall),
      flip (True turns the top of the shoe away from the knee, which it
      otherwise faces).
    elbows, knees: dicts {"l": mode, "r": mode}, mode one of
      out | in | up | down | left | right. In side view the joints bend
      anatomically and these are ignored, unless anatomy=False.
    arm_len, leg_len: per-limb length factors for foreshortening,
      e.g. {"l": 0.9}. A factor may be a pair for the two segments, e.g.
      {"r": (1.0, 0.8)} to shorten only the shin, or only the forearm.
    head: offset of the head centre from its neutral position (look toward
      a hold by nudging it). Keep it within a few cm: the neck stretches.
    head_tilt: degrees to tip the head, and the neck with it. Positive tips
      the top of the head to the climber's right in a back view (a look
      down to the right foot), and forward, chin down, in a side view.
    xray: draw the parts of the shoes hidden behind a leg, and of the hands
      and forearms hidden behind the body, as dotted outlines (default: the
      module setting XRAY; see _xray_arm). hold() takes the same option for
      the parts of a hold hidden behind a hand or foot.
    active: the muscles at work, stippled (MUSCLE_DOTS). Names
      are a side and a muscle, e.g. "rupper", "lthigh": fore, upper (biceps
      or triceps), lat, thigh, ham (hamstring), calf, shin (its front, for a
      toe hook), glute; and "core".
      By default (None) a bent arm that holds on works its upper arm and
      forearm. A list of names replaces that; names written "+name" or
      "-name" add to it or take from it, e.g. ("+rthigh",) for a leg that
      drives the move or ("+lham",) for a heel hook.
    tuck: the arms ("l", "r") whose root stays under the T-shirt's shoulder.
      An upper arm that hangs close to the side can have the root of its
      sleeve run along the shoulder just outside the T-shirt's line, which
      doubles that line into a heavy stroke; this takes it back inside.

    The climber is drawn clothed: a white T-shirt with short sleeves, and
    trousers whose left leg (and left half of the seat) is grey; the bare
    left forearm and hand are grey too. To draw an arm through an explicit
    elbow (an arm pointing into the wall), leave it out of `order` and call
    draw_arm() after draw(). The head is drawn with the torso; put "head" in
    `order` to draw it on its own, e.g. last, over hands that reach past the
    face to the wall.
    """

    def __init__(self, pelvis, view="back", lean=0.0, turn=0.0, lh=None,
                 rh=None, lf=None, rf=None, elbows=None, knees=None,
                 arm_len=None, leg_len=None, head=(0, 0), sh_w=None,
                 hip_w=None, order=None, hand_style=None, scale=1.0,
                 shoulders=None, anatomy=True, allow_cross=False, xray=None,
                 head_tilt=0.0, active=None, bend=0.0, tuck=()):
        self.view = view
        self.tuck = tuck
        self.head_tilt = head_tilt
        self.active = active
        self.lean = lean
        self.bend = bend
        self.s = scale
        if shoulders is not None:
            # place the climber by the point between the shoulders
            u, (uc, _) = ang(90 - lean), self.chest_frame()
            pelvis = sub(shoulders, add(mul(u, WAIST_T * scale),
                                        mul(uc, (DIM["torso"] - 1 - WAIST_T) * scale)))
        self.pelvis = pelvis
        self.turn = turn
        self.lh, self.rh, self.lf, self.rf = lh, rh, lf, rf
        self.elbows = {"l": "out", "r": "out", **(elbows or {})}
        self.knees = {"l": "out", "r": "out", **(knees or {})}
        self.arm_len = {"l": 1.0, "r": 1.0, **(arm_len or {})}
        self.leg_len = {"l": 1.0, "r": 1.0, **(leg_len or {})}
        self.head_off = head
        self.anatomy = anatomy
        self.allow_cross = allow_cross
        self._xray_feet = XRAY if xray is None else xray
        self._ghost = False
        k = math.cos(math.radians(abs(turn) * 70))
        self.sh_w = sh_w if sh_w is not None else (1 if view == "back" else 0)
        self.hip_w = hip_w if hip_w is not None else (1 if view == "back" else 0)
        if view == "back" and turn and sh_w is None:
            self.sh_w = k
        if view == "back" and turn and hip_w is None:
            self.hip_w = max(0.4, k)
        self.order = order
        self.hand_style = hand_style or {}
        self.solve()

    def arm_factors(self, s):
        """The (upper arm, forearm) length factors of arm `s`."""
        f = self.arm_len[s]
        return f if isinstance(f, tuple) else (f, f)

    def reach(self, s):
        """How far hand `s` reaches from its shoulder to the grip, in cm."""
        fu, ff = self.arm_factors(s)
        return self.D["upper_arm"] * fu + (self.D["forearm"] + self.D["hand"]) * ff

    # frame
    def frame(self):
        """The frame of the hips: (up the spine, to the climber's right, or
        forward in a side view)."""
        u = ang(90 - self.lean)
        r = (u[1], -u[0])
        return u, r

    def chest_frame(self):
        """The frame of the chest and shoulders: the hips' frame turned by
        `bend` at the waist."""
        u = ang(90 - self.lean - self.bend)
        return u, (u[1], -u[0])

    def head_frame(self):
        """The chest's frame tipped by head_tilt: (up the head, its right)."""
        u, r = self.chest_frame()
        a = math.radians(self.head_tilt)
        c, sn = math.cos(a), math.sin(a)
        return add(mul(u, c), mul(r, sn)), sub(mul(r, c), mul(u, sn))

    def local(self, s, t):
        """The world point at (s, t) cm in the body: s to the right (or
        forward), t up the spine from the hip joints. With `bend` the frame
        turns round the waist, gradually over WAIST_SPAN either side of it,
        so the flanks curve instead of breaking."""
        u, r = self.frame()
        p = add(self.pelvis, add(mul(r, s * self.s), mul(u, t * self.s)))
        if not self.bend:
            return p
        x = max(0.0, min(1.0, (t - WAIST_T + WAIST_SPAN) / (2 * WAIST_SPAN)))
        waist = add(self.pelvis, mul(u, WAIST_T * self.s))
        return add(waist, rot(sub(p, waist), -self.bend * x * x * (3 - 2 * x)))

    def solve(self):
        D = {k: v * self.s for k, v in DIM.items()}
        u, r = self.frame()
        uc, rc = self.chest_frame()
        J = {}
        side = 1 if self.view == "back" else 0
        sh_off = D["sh_half"] * self.sh_w * side
        hip_off = D["hip_half"] * self.hip_w * side
        J["sh_c"] = self.local(0, DIM["torso"] - 1)
        if self.view == "back":
            J["lsh"] = add(J["sh_c"], mul(rc, -sh_off))
            J["rsh"] = add(J["sh_c"], mul(rc, sh_off))
            J["lhip"] = add(self.pelvis, mul(r, -hip_off))
            J["rhip"] = add(self.pelvis, mul(r, hip_off))
        else:
            J["lsh"] = J["rsh"] = add(J["sh_c"], mul(rc, -1.5 * self.s))
            J["lhip"] = J["rhip"] = add(self.pelvis, mul(r, 1.0 * self.s))
        J["head"] = add(add(J["sh_c"], mul(uc, D["neck"] + D["head_ry"] + 0.5)),
                        mul(self.head_off, self.s))
        self.D = D
        self._J = J
        side_anat = self.view == "side" and self.anatomy
        for s in ("l", "r"):
            sign = -1 if s == "l" else 1
            # arms: solve to the grip point, then step back to the wrist
            target = getattr(self, s + "h")
            sh = J[s + "sh"]
            fu, ff = self.arm_factors(s)
            la = D["upper_arm"] * fu
            lf = (D["forearm"] + D["hand"]) * ff
            if target is None:
                target = add(sh, (sign * 6 * self.s, -(la + lf) * 0.97))
            if side_anat:
                ch = anatomical(sh, target, +1)
            else:
                ch = chooser(self.elbows[s], sign if self.view == "back" else 1,
                             self.pelvis, r)
            J[s + "el"], J[s + "ha"] = ik(sh, target, la, lf, ch)
            fv = norm(sub(J[s + "ha"], J[s + "el"]))
            J[s + "wr"] = sub(J[s + "ha"], mul(fv, D["hand"] * ff))
            # legs
            ft = getattr(self, s + "f")
            hip = J[s + "hip"]
            if ft is None:
                ft = {"at": add(hip, (sign * 4 * self.s, -(D["thigh"] + D["shin"]) - 12 * self.s))}
            if not isinstance(ft, dict):
                ft = {"at": ft}
            ft = dict(ft)
            ft.setdefault("contact", "edge")
            ft.setdefault("style", "profile")
            auto_angle = "angle" not in ft and self.view == "side"
            if "angle" not in ft:
                if self.view == "side":
                    ft["angle"] = 0
                else:
                    ft["angle"] = 180 if s == "l" else 0
            for _ in range(4 if auto_angle else 1):
                self._solve_leg(s, ft, hip, r, side_anat, D)
                if not auto_angle:
                    break
                # keep the ankle between 65 and 135 deg (90 is neutral)
                shin_up = norm(sub(J_tmp(self, s, "kn"), J_tmp(self, s, "an")))
                a_shin = math.degrees(math.atan2(shin_up[1], shin_up[0]))
                a_ft = ft["angle"]
                rel = (a_shin - a_ft) % 360          # ankle angle measured from foot to shin
                if rel > 180:
                    rel -= 360
                want = max(65, min(135, rel))
                if abs(want - rel) < 0.5:
                    break
                ft["angle"] = a_shin - want
            continue
        self.J = J


    def _solve_leg(self, s, ft, hip, r, side_anat, D):
        J = self._J
        d = ang(ft["angle"])
        n = perp(d)
        if dot(n, sub(hip, ft["at"])) < 0:
            n = mul(n, -1)
        self._place_leg(s, ft, d, n, hip, r, side_anat, D)
        # the top of the shoe faces the shin. Facing the hip is only a first
        # guess, wrong for a foot at or above the hip, so check the knee
        if dot(n, norm(sub(J[s + "kn"], J[s + "an"]))) < -0.2:
            n = mul(n, -1)
            self._place_leg(s, ft, d, n, hip, r, side_anat, D)
        if ft.get("flip"):
            self._place_leg(s, ft, d, mul(n, -1), hip, r, side_anat, D)

    def _place_leg(self, s, ft, d, n, hip, r, side_anat, D):
        """Put the shoe on its contact point with its top toward `n`, and
        solve the knee and ankle of leg `s` from `hip` to it."""
        J = self._J
        sign = -1 if s == "l" else 1
        sc = self.s
        # `fore` shortens a profile shoe along its length: a foot turned partway
        # toward the viewer, e.g. 0.7 for a high foot turned out 45 degrees
        # in a back view
        k = ft.get("fore", 1.0)
        if ft["style"] == "back":
            ankle = add(ft["at"], (0, 8 * sc))
        elif ft["contact"] in SHOE_CONTACTS:
            o = sub(SHOE_ANKLE, SHOE_CONTACTS[ft["contact"]])
            ankle = add(ft["at"], add(mul(d, o[0] * sc * k), mul(n, o[1] * sc)))
        else:
            o = sub(SHOE_ANKLE, SHOE_HEEL)
            ankle = add(ft["at"], add(mul(d, o[0] * sc * k), mul(n, o[1] * sc)))
        ft["d"], ft["n"] = d, n
        ft["ankle_target"] = ankle
        setattr(self, "_" + s + "f", ft)
        f = self.leg_len[s]
        ft_, fs_ = f if isinstance(f, tuple) else (f, f)
        lt, ls = D["thigh"] * ft_, D["shin"] * fs_
        if side_anat:
            kh = anatomical(hip, ankle, -1)
        else:
            kh = chooser(self.knees[s], sign if self.view == "back" else 1,
                         self.pelvis, r)
        J[s + "kn"], J[s + "an"] = ik(hip, ankle, lt, ls, kh)
        reach = length(sub(ankle, J[s + "an"]))
        ft["short"] = reach > 1.0

    # drawing
    def _check_ghost_overlap(self, fig, ghost):
        """Warn when a ghost and a climber in the same panel nearly coincide:
        the two bodies then merge into one double body ("conjoined twins").
        A ghost should show an earlier position the body has clearly moved
        away from; a wrong-vs-right comparison belongs in its own panel."""
        drawn = fig.__dict__.setdefault("_climbers_drawn", [])

        def whole(c):
            # a partial ghost (order without the torso) shows only moving limbs
            return c.order is None or "torso" in c.order
        for other, other_ghost in drawn:
            if other_ghost == ghost or other.view != self.view:
                continue
            if not (whole(self) and whole(other)):
                continue
            d_pel = length(sub(self.pelvis, other.pelvis))
            d_sh = length(sub(self.J["sh_c"], other.J["sh_c"]))
            if d_pel < 28 * self.s and d_sh < 28 * self.s:
                import inspect
                caller = next((f"{os.path.basename(fr.filename)}:{fr.function}"
                               for fr in inspect.stack()[1:]
                               if not fr.filename.endswith("climb.py")), "figure")
                print(f"{caller}: ghost overlaps the climber "
                      f"(hips {d_pel:.0f} cm, shoulders {d_sh:.0f} cm apart): the bodies "
                      f"merge; use a separate panel or move the ghost clearly away")
        drawn.append((self, ghost))

    def draw(self, fig, ghost=False, z=0, fills=None):
        self._check_ghost_overlap(fig, ghost)
        self._fig = fig
        if ghost:
            dash = (0.9, 0.7)
            line = dict(stroke=GHOST_LINE, sw=0.3, dash=dash, ghost=True)
            shoe_st = dict(fill=WHITE, stroke=GHOST_LINE, sw=0.3, dash=dash)
            g = WHITE
            if fills == "solid":
                line = dict(stroke=GHOST_LINE, sw=0.3, dash=None)
                g = PALE
            col = dict(l=g, r=g, shirt=g, hair=g)
        else:
            line = dict(stroke=INK, sw=0.32, dash=None)
            shoe_st = dict(fill=SHOE_FILL, stroke=INK, sw=0.3)
            col = dict(l=LEFT, r=WHITE, shirt=WHITE, hair=HAIR)
        self._ghost = ghost
        geo = self._geometry(col, ghost)

        order = self.order
        if order is None:
            if self.view == "back":
                if self.turn > 0.15:
                    order = ["rleg", "rarm", "torso", "lleg", "larm"]
                elif self.turn < -0.15:
                    order = ["lleg", "larm", "torso", "rleg", "rarm"]
                else:
                    order = ["lleg", "rleg", "torso", "larm", "rarm"]
            else:
                order = ["lleg", "larm", "torso", "rleg", "rarm"]
        self._torso_z = z + order.index("torso") if "torso" in order else None
        # the head goes with the torso unless `order` places it on its own,
        # e.g. above arms that reach past the face to the wall
        self._head_z = z + order.index("head") if "head" in order else self._torso_z
        self._arms = {"fig": fig}
        zz = z
        for name in order:
            if name == "torso":
                _draw_group(fig, zz, *geo["torso"], line)
                if "head" not in order:
                    _draw_group(fig, zz + 0.01, *geo["head"], line)
            elif name == "head":
                _draw_group(fig, zz, *geo["head"], line)
            elif name in geo:
                if name.endswith("leg"):
                    # the shoe goes behind its leg, so the trouser leg
                    # covers the top of the shoe
                    self._shoe(fig, name[0], shoe_st, zz - 0.02)
                    if self.view == "back" and "torso" in order and \
                            order.index(name) > order.index("torso"):
                        geo[name] = (self._front_thigh(name[0], geo[name][0]), geo[name][1])
                _draw_group(fig, zz, *geo[name], line)
                if name.endswith("arm"):
                    self._arms[name[0]] = (zz, geo[name][0])
            zz += 1
        if not ghost:
            for s in "lr":
                if s in self._arms:
                    self._xray_arm(fig, s, *self._arms[s], line["sw"])

    def draw_arm(self, fig, s, elbow, hand, z, ghost=False):
        """Draw arm `s` ("l"/"r") from its shoulder through an explicit
        `elbow` to the grip point `hand`, in the climber's style. For an arm
        that points into the wall, whose upper arm and forearm shorten by
        different amounts: leave the arm out of `order`, draw the climber,
        then call this. The segments are checked as warn() checks a solved
        arm: the upper arm may shorten to 0.6 (pointing well out of the
        wall), the forearm further, and neither may stretch."""
        J = self.J
        up = length(sub(elbow, J[s + "sh"])) / self.D["upper_arm"]
        fo = length(sub(hand, elbow)) / (self.D["forearm"] + self.D["hand"])
        if not ghost and not (0.6 <= up <= 1.01 and fo <= 1.01):
            import inspect
            caller = next((f"{os.path.basename(fr.filename)}:{fr.function}"
                           for fr in inspect.stack()[1:]
                           if not fr.filename.endswith("climb.py")), "figure")
            print(f"{caller}: arm {s} drawn with its upper arm {up:.2f} and its "
                  f"forearm {fo:.2f} of their full length")
        v = norm(sub(hand, elbow))
        wr = sub(hand, mul(v, min(self.D["hand"], length(sub(hand, elbow)) * 0.4)))
        col = (dict(l=WHITE, r=WHITE, shirt=WHITE) if ghost else
               dict(l=LEFT, r=WHITE, shirt=WHITE))
        line = (dict(stroke=GHOST_LINE, sw=0.3, dash=(0.9, 0.7), ghost=True) if ghost else
                dict(stroke=INK, sw=0.32, dash=None))
        torso_polys = self._torso_shapes()[0]
        pieces, lines = self._arm_geometry(s, J[s + "sh"], elbow, wr, hand,
                                           col, ghost, torso_polys)
        _draw_group(fig, z, pieces, lines, line)
        if not ghost:
            self._xray_arm(fig, s, z, pieces, line["sw"])

    def _xray_arm(self, fig, s, z, pieces, sw):
        """The x-ray outline (see XRAY) of arm `s`, drawn at z from `pieces`
        with outline weight `sw`: the outline of the hand (of an open hand,
        the palm), leaving out where it runs into the forearm or lies under
        the other hand. The forearm is outlined too when the hand or forearm
        lies over the torso or head and that is drawn above the arm: an arm
        that only crosses the other arm or a leg keeps its plain outline."""
        if not self._xray_feet:
            return
        polys = [_Poly(pc["pts"]) for pc in pieces]
        # the dots run in the outer half of the drawn outline (the inner
        # half lies under the fill), so on a visible hand they fall on it
        d = fig.mm(fig.weight(sw * 2)) / 4
        # a hand hidden by the other hand, which is drawn over it, is where
        # that hand is: its outline would only clutter the visible hand
        hands, fores = [], []
        arms = getattr(self, "_arms", {})
        same = arms.get("fig") is fig       # drawn by draw() in this figure
        o = "r" if s == "l" else "l"
        if same and o in arms and arms[o][0] > z:
            for pc in arms[o][1]:
                if pc.get("part") in ("hand", "finger"):
                    hands.append(_Poly(_outward(pc["pts"], 1.5 * d)))
                elif pc.get("part") == "fore":
                    fores.append(_Poly(_outward(pc["pts"], 1.5 * d)))
        parts = {"hand"}
        tz = self._torso_z if same else None
        hz = self._head_z if same else None
        body = self._body_polys(torso=tz is not None and tz > z,
                                head=hz is not None and hz > z)
        lower = [p for pc in pieces if pc.get("part") for p in pc["pts"]]
        if any(b.has(p) for b in body for p in lower):
            parts.add("fore")
        for i, pc in enumerate(pieces):
            if pc.get("part") not in parts:
                continue
            out = _outward(pc["pts"], d)
            if pc["part"] == "fore" and fores:
                # a forearm right behind the other one (both hands on one
                # hold, in a side view) shows nothing new
                if sum(any(q.has(p) for q in hands + fores) for p in out) >= 0.9 * len(out):
                    continue
            others = polys[:i] + polys[i + 1:] + hands

            def inside(p):
                return any(q.has(p) for q in others)
            for run, closed in _runs(out, inside):
                # no specks where the outline just touches another part
                if closed or sum(length(sub(b, a)) for a, b in zip(run, run[1:])) >= fig.mm(0.6):
                    fig.poly(run, closed=closed, z=XRAY_Z, **XRAY_STYLE)

    def _body_polys(self, torso=True, head=True):
        """Polygons of the torso (with neck and seat) and of the head."""
        if not (torso or head):
            return []
        polys, _, _, neck, _ = self._torso_shapes()
        col = dict(l=LEFT, r=WHITE, shirt=WHITE, hair=HAIR)
        heads = self._head_geometry(col, True, _Poly(neck))[0] if head else []
        return (polys if torso else []) + [_Poly(pc["pts"]) for pc in heads]

    # ---- geometry of the drawn body

    def _muscles(self):
        """The names of the muscles at work (see `active`)."""
        J = self.J
        auto = set()
        for s in "lr":
            sh, el, wr = J[s + "sh"], J[s + "el"], J[s + "wr"]
            # a bent arm (under 130 degrees at the elbow) that holds on
            # (a bent leg may push or just rest, and a heel may hook or just
            # stand, so legs are shaded only where a figure says so)
            if getattr(self, s + "h") is not None and \
                    dot(norm(sub(sh, el)), norm(sub(wr, el))) > -0.64:
                auto |= {s + "upper", s + "fore"}
        if self.active is None:
            return auto
        names = list(self.active)
        if names and all(n[:1] in "+-" for n in names):
            for n in names:
                (auto.add if n[0] == "+" else auto.discard)(n[1:])
            return auto
        return set(names)

    def _shade(self, pts, fill, axis=None, focus=None):
        """A line entry that stipples a muscle under `fill` within the
        outline `pts`, or None. The dots thin out over an ellipse round the
        shape's centre, long along `axis` (default: the shape's longest
        direction), from `focus`, where they are densest."""
        colour = MUSCLE_DOTS.get(fill)
        if not colour:
            return None
        n = len(pts)
        c = (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)
        if axis is None:
            sxx = sum((p[0] - c[0]) ** 2 for p in pts)
            syy = sum((p[1] - c[1]) ** 2 for p in pts)
            sxy = sum((p[0] - c[0]) * (p[1] - c[1]) for p in pts)
            axis = ang(math.degrees(0.5 * math.atan2(2 * sxy, sxx - syy)))
        v = perp(axis)
        ra = max(abs(dot(sub(p, c), axis)) for p in pts)
        rb = max(abs(dot(sub(p, c), v)) for p in pts)
        if focus is not None:
            # only along the axis: a muscle on one side of a limb is densest
            # across its own middle
            focus = add(c, mul(axis, dot(sub(focus, c), axis)))
        return dict(pts=pts, dots=(c, axis, ra, rb, focus, colour))

    def _belly_shade(self, p1, p2, left, right, t0, t1, fill, peak=0.5, **kw):
        """The shade of a muscle in a limb segment (see belly), densest at
        its fullest."""
        pts = belly(p1, p2, left, right, self.s, t0, t1, peak=peak,
                    inset=self._inset(), **kw)
        d = norm(sub(p2, p1))
        focus = lerp(p1, p2, t0 + (t1 - t0) * peak)
        return self._shade(pts, fill, axis=d, focus=focus)

    def _inset(self):
        """How far a shade keeps inside an outline, in world units. The
        visible half of an outline lies outside its path, so this only has
        to cover the pen's wobble (WOBBLE) and leave a hair of white."""
        fig = getattr(self, "_fig", None)
        return fig.mm(0.26) if fig is not None else 0.8 * self.s

    def _geometry(self, col, ghost):
        J, S = self.J, self.s
        polys, shirt, seats, neck, lines = self._torso_shapes(ghost)
        self._on = set() if ghost else self._muscles()
        lines = self._torso_shades(col, seats) + lines
        G = {}
        thighs = {}
        for s in "lr":
            pieces, lns, thigh = self._leg_geometry(s, col[s], polys)
            G[s + "leg"] = (pieces, [] if ghost else lns)
            thighs[s] = _Poly(thigh)
        # the torso: neck, trouser seat (one half per leg, coloured like the
        # leg), T-shirt; each seat half leaves out its outline inside its
        # own thigh near the hip, so the trouser leg runs up into the seat
        pieces = [dict(pts=neck, fill=col["shirt"])]
        for s, pts in seats:
            pieces.append(dict(pts=pts, fill=col[s], hide=_near_inside(
                J[s + "hip"], 16 * S, [thighs[s]])))
        pieces.append(dict(pts=shirt, fill=col["shirt"]))
        G["torso"] = (pieces, [] if ghost else lines)
        G["head"] = self._head_geometry(col, ghost, _Poly(neck))
        for s in "lr":
            G[s + "arm"] = self._arm_geometry(
                s, J[s + "sh"], J[s + "el"], J[s + "wr"], J[s + "ha"], col, ghost,
                polys)
        return G

    def _under_hem(self, p):
        """Point `p`, moved straight down the body if it's above the T-shirt's
        hem, whose height across the back is SHIRT_BACK_HEM's."""
        u, r = self.frame()
        q = sub(p, self.pelvis)
        t = dot(q, u) / self.s
        x = abs(dot(q, r)) / self.s / (self.hip_w + 0.5 * (1 - self.hip_w))
        (x0, t0), (x1, t1) = (SHIRT_BACK_HEM[1], SHIRT_BACK_HEM[0]) if x < SHIRT_BACK_HEM[0][0] \
            else (SHIRT_BACK_HEM[0], SHIRT_BACK_SIDE[-1])
        hem = t0 + (t1 - t0) * min(1.0, (x - x0) / (x1 - x0)) - 0.4
        return sub(p, mul(u, (t - hem) * self.s)) if t > hem else p

    def _front_thigh(self, s, pieces):
        """The pieces of a leg drawn over the torso in a back view. Whole, the
        hidden root of its thigh would show across the seam as a torn edge. So
        the root stops at the seam, and below the hem the outline stops at its
        own half of the seat, with which it is one shape. A thigh whose outline
        comes out across the seam meets the other half along one straight line,
        from just under the hem to where that outline comes out."""
        thigh = pieces[0]
        hip, kn = self.J[s + "hip"], self.J[s + "kn"]
        u, _ = self.frame()
        own = _Poly(dict(self._torso_shapes()[2])[s])
        # (not all the way along the thigh: a foreshortened one keeps its knee)
        d, reach = norm(sub(kn, hip)), 0.6 * length(sub(kn, hip))
        hide = lambda p: thigh["hide"](p) or (
            dot(sub(p, hip), d) < reach and own.has(p) and
            dot(sub(p, self.pelvis), u) / self.s < 3)
        runs = _runs(thigh["pts"], hide)
        if not runs or runs[0][1]:
            return pieces
        visible = [p for run, _ in runs for p in run]
        top, crotch = self._seam
        seam = sub(crotch, top)
        sg = 1 if s == "l" else -1      # the sign of cross() across the seam
        across = lambda p: sg * cross(seam, sub(p, top))
        ends = [visible[0], visible[-1]]
        over = [e for e in ends if across(e) > 0]
        root = []       # the thigh on its own side of the seam
        pts = thigh["pts"]
        for a, b in zip(pts, pts[1:] + pts[:1]):
            if across(a) <= 0:
                root.append(a)
            if (across(a) <= 0) != (across(b) <= 0):
                root.append(lerp(a, b, across(a) / (across(a) - across(b))))
        root = [self._under_hem(p) if thigh["hide"](p) else p for p in root]
        out = [dict(pts=pts, hide=hide), dict(pts=visible, fill=thigh["fill"], stroke=False)]
        if root:
            out.append(dict(pts=root, fill=thigh["fill"], stroke=False))
        # where the outline stops well short of the hem, the same edge runs on to it
        for a, b in zip(pts, pts[1:] + pts[:1]):
            for e, h in ((a, b), (b, a)):
                on_hem = self._under_hem(h)
                if not hide(e) and thigh["hide"](h) and across(e) <= 0 and \
                        5 * self.s < length(sub(on_hem, e)) < 14 * self.s:
                    out.append(dict(pts=[e, on_hem]))
        if over:
            # the seat's top is at t = 9.5, the crotch at t = -10, the hem at 2.6
            under_hem = lerp(top, crotch, 8.0 / 19.5)
            ends.sort(key=lambda e: length(sub(e, under_hem)))
            gusset = [under_hem] + ends + ([crotch] if len(over) == 2 else [])
            out.append(dict(pts=gusset, fill=thigh["fill"], stroke=False))
        return out + pieces[1:]

    def _torso_shades(self, col, seats):
        """Line entries shading the lats, glutes and core that are at work."""
        on, L, out = self._on, self.local, []
        if not on:
            return out
        if self.view == "back":
            sw_o = self.sh_w + 0.35 * (1 - self.sh_w)
            hw_o = self.hip_w + 0.5 * (1 - self.hip_w)
            for s, sg in (("l", -1), ("r", 1)):
                if s + "lat" in on:
                    out.append(self._shade(catmull([L(sg * x * sw_o, t) for x, t in LAT_BACK],
                                                   k=4), col["shirt"]))
                if s + "glute" in on:
                    (x, t), rx, ry = GLUTE_BACK
                    out.append(self._shade(ellipse_pts(L(sg * x * hw_o, t), rx * hw_o * self.s,
                                                       ry * self.s, n=28), col[s]))
            if "core" in on:
                for sg in (-1, 1):
                    out.append(self._shade(catmull([L(sg * x, t) for x, t in CORE_BACK],
                                                   k=4), col["shirt"]))
        elif "core" in on:
            out.append(self._shade(catmull([L(x, t) for x, t in CORE_SIDE], k=4),
                                   col["shirt"]))
        return [o for o in out if o]

    def _torso_shapes(self, ghost=True):
        """(polygons for hit tests, shirt, [(side, seat half)], neck, inner
        lines) in world coordinates."""
        J, S = self.J, self.s
        u, r = self.frame()
        L = self.local

        def chain(pts, k=5):
            return catmull(pts, closed=False, k=k) + [pts[-1]]
        lines = []
        if self.view == "back":
            sw, hw = self.sh_w, self.hip_w
            # a turned body narrows less than its joint spacing: the depth
            # of the chest and the seat shows as the width goes
            sw_o, hw_o = sw + 0.35 * (1 - sw), hw + 0.5 * (1 - hw)

            def wsc(t):
                if t >= 34:
                    return sw_o
                if t <= 12:
                    return hw_o
                return hw_o + (sw_o - hw_o) * (t - 12) / 22

            def P(x, t, sg):
                return L(sg * x * wsc(t), t)

            def arc(sg):
                sh = J["rsh" if sg > 0 else "lsh"]
                rx, ry = SHOULDER_R
                uc, rc = self.chest_frame()
                return [add(sh, add(mul(rc, sg * rx * S * math.cos(math.radians(a))),
                                    mul(uc, ry * S * math.sin(math.radians(a)))))
                        for a in (100, 70, 40, 10, -20)]

            def flank(sg):   # from the neck down to the hem corner
                return chain([P(x, t, sg) for x, t in SHIRT_BACK_TOP] + arc(sg) +
                             [P(x, t, sg) for x, t in SHIRT_BACK_SIDE])
            right, left = flank(1), flank(-1)
            hem = chain([left[-1]] + [P(x, t, -1) for x, t in SHIRT_BACK_HEM] +
                        [P(x, t, 1) for x, t in SHIRT_BACK_HEM[::-1]] + [right[-1]])
            shirt = left + hem[1:-1] + right[::-1]
            # spine offset when the hips turn: the trouser seam moves with it
            off = math.sin(math.radians(self.turn * 70)) * 9
            seam = max(-0.3, min(0.3, off / 9)) * DIM["hip_half"] * hw
            top, crotch = L(seam, 9.5), L(seam * 0.6, -10.0)
            # the seat's lower edge runs from the inside of each thigh to the
            # crotch, so the trouser legs meet there in a V
            inner = {}
            for s, sg in (("l", -1), ("r", 1)):
                hip, kn = J[s + "hip"], J[s + "kn"]
                d = norm(sub(kn, hip))
                nm = perp(d)
                if dot(nm, sub(crotch, hip)) < 0:
                    nm = mul(nm, -1)
                m = add(hip, add(mul(d, 9 * S), mul(nm, 7.6 * S)))
                # only a thigh that hangs mostly downward cuts the seat; a
                # raised or sideways thigh leaves the buttock's round curve
                down = -dot(d, u) > 0.64
                # a thigh that has crossed the seam (crossed legs, or narrow
                # hips turned side on) would fold this half over the other
                if down and dot(sub(m, self.pelvis), u) / S < -4 and \
                        dot(sub(m, hip), mul(r, sg)) <= 0 and \
                        dot(sub(m, crotch), mul(r, sg)) > 0:
                    inner[s] = m
            if len(inner) == 2:
                # the crotch sits between the two inner thighs
                q = sub(lerp(inner["l"], inner["r"], 0.5), self.pelvis)
                cs = max(-6 * hw, min(6 * hw, dot(q, r) / S))
                ct = max(-11.0, min(-7.0, dot(q, u) / S))
                crotch = L(cs, ct)
            seats = []
            for s, sg in (("l", -1), ("r", 1)):
                low = [inner[s]] if s in inner else [P(x, t, sg) for x, t in SEAT_BACK[4:]]
                outer = chain([P(x, t, sg) for x, t in SEAT_BACK[:4]] + low)
                # the left half reaches a little past the seam, under the
                # right half, so no hairline gap shows between the fills
                k = 0.4 * S if s == "l" else 0.0
                seats.append((s, outer + [add(crotch, mul(r, k)), add(top, mul(r, k))]))
            self._seam = (top, crotch)
            neck_base = L(0, 50)
            hu, _ = self.head_frame()
            neck_top = sub(self._head_centre(), mul(hu, 6 * S))
            neck = tube(neck_base, neck_top, [(0, 5.2), (1, 4.7)], [(0, 5.2), (1, 4.7)], S)
            # the T-shirt's hem, the one line inside the torso
            lines.append(dict(pts=hem, sw=LINE_SW))
        else:
            front = [L(x, t) for x, t in SHIRT_SIDE[0:9]]
            hem = [L(x, t) for x, t in SHIRT_SIDE[8:12]]
            back = [L(x, t) for x, t in SHIRT_SIDE[11:20]]
            collar = [L(x, t) for x, t in SHIRT_SIDE[19:]] + [front[0]]
            hem_c = chain(hem)
            shirt = chain(front)[:-1] + hem_c[:-1] + chain(back)[:-1] + chain(collar)[:-1]
            seats = [("r", catmull([L(x, t) for x, t in SEAT_SIDE], k=5))]
            neck_base = L(-1.5, 50)
            hu, hr = self.head_frame()
            neck_top = add(self._head_centre(),
                           add(mul(hr, -1.8 * S), mul(hu, -7.0 * S)))
            neck = tube(neck_base, neck_top, [(0, 5.0), (1, 4.5)], [(0, 5.0), (1, 4.5)], S)
            lines.append(dict(pts=hem_c, sw=LINE_SW))
        polys = [_Poly(shirt), _Poly(neck)] + [_Poly(p) for _, p in seats]
        return polys, shirt, seats, neck, lines

    def _head_geometry(self, col, ghost, neck):
        S = self.s
        u, r = self.head_frame()
        hc = self._head_centre()

        def H(pts):
            return _frame_pts(hc, r, u, pts, S * HEAD_SIZE, S * HEAD_SIZE)

        def chain(pts, k=4):
            return catmull(pts, closed=False, k=k) + [pts[-1]]

        def big(pts):
            # hair stands a little proud of the skull
            return [(x * 1.03, y * 1.03) for x, y in pts]
        lines = []
        if self.view == "back":
            half = HEAD_BACK
            skull = catmull(H(half + [(-x, y) for x, y in half[::-1]][1:-1]), k=4)
            ears = [catmull(H(EAR_BACK), k=4),
                    catmull(H([(-x, y) for x, y in EAR_BACK]), k=4)]
            # hairline from the right ear round the nape to the left ear
            hl = H(HAIRLINE_BACK + [(-x, y) for x, y in HAIRLINE_BACK[::-1]][1:])
            top = [p for p in half if p[1] > -3.0]
            over = [(-x, y) for x, y in top][::-1][:-1] + top     # left to right
            x0, y0 = HAIRLINE_BACK[0]
            hair = chain(H([(-x0, y0)] + big(over) + [(x0, y0)])) + chain(hl)[1:]
            pieces = [dict(pts=skull, fill=col["shirt"], hide=neck.has)]
            pieces += [dict(pts=e, fill=col["shirt"]) for e in ears]
            # the hair's tone marks the hairline, without a line
            pieces.append(dict(pts=hair, fill=col["hair"]))
        else:
            head = catmull(H(HEAD_SIDE), k=4)

            def nape(p):
                # the back of the head runs into the neck without a line;
                # the jaw stays drawn in front of the neck
                return neck.has(p) and dot(sub(p, hc), r) < -1.2 * S
            # the hair: from the forehead over the crown to the nape, then
            # back along its edge past the ear to the temple
            outer = [(7.0, 7.7)] + [HEAD_SIDE[i] for i in (1, 0, 24, 23, 22, 21, 20)] + \
                [(-7.7, -5.0)]
            edge = H(HAIR_SIDE_EDGE)
            hair = chain(H(big(outer))) + chain(edge)[1:]
            pieces = [dict(pts=head, fill=col["shirt"], hide=nape),
                      dict(pts=hair, fill=col["hair"])]
            if not ghost:
                lines.append(dict(pts=catmull(H(EAR_SIDE), k=4), closed=True,
                                  fill=WHITE, sw=FINE_SW))
                eye = H([EYE_SIDE])[0]
                lines.append(dict(pts=[add(eye, mul(ang(a * 45), 0.75 * S))
                                       for a in range(8)], closed=True, fill=INK,
                                  stroke=None))
        return pieces, lines

    def _head_centre(self):
        u, _ = self.head_frame()
        return add(self.J["head"], mul(u, HEAD_RAISE * self.s))

    def _thumb_side(self, s, v):
        """+1 if the thumb is on the left of the hand direction v."""
        _, r = self.chest_frame()
        if self.view == "back":
            return -1 if s == "l" else 1
        return 1 if dot(perp(v), r) >= 0 else -1

    def _arm_geometry(self, s, sh, el, wr, ha, col, ghost, torso_polys):
        S = self.s
        skin = col[s]
        v = norm(sub(ha, wr)) if length(sub(ha, wr)) > 1e-6 else norm(sub(wr, el))
        th = self._thumb_side(s, v)
        hide = _root_hide(sh, el, 1.2 * SLEEVE[0][1] * S, torso_polys)
        se = lerp(sh, el, SLEEVE_LEN)
        # (see tuck) a shallower root stays under the T-shirt's shoulder
        tucked = s in self.tuck
        sleeve = tube(sh, se, SLEEVE, SLEEVE, S, cap1=0.6 if tucked else 0.85, cap2=0.2)
        # the inner side of the upper arm: toward the body in a back view
        # (the hips are below a hanging arm and beside a raised one), toward
        # the bend of the elbow in a side view
        n_up = perp(norm(sub(el, sh)))
        if self.view == "back":
            in_left = dot(n_up, sub(self.pelvis, sh)) > 0
        else:
            elbow = dot(n_up, sub(wr, el))
            _, r = self.chest_frame()
            in_left = elbow > 0 if abs(elbow) > 1.5 * S else dot(n_up, r) > 0
        up_l, up_r = (UPPER_ARM_IN, UPPER_ARM_OUT) if in_left else (UPPER_ARM_OUT, UPPER_ARM_IN)
        upper = tube(sh, el, up_l, up_r, S, cap1=0.5 if tucked else 1.0)
        rad, uln = FORE_RADIAL, FORE_ULNAR
        fo_l, fo_r = (rad, uln) if th > 0 else (uln, rad)
        fore = tube(el, wr, fo_l, fo_r, S)
        # part: which pieces the x-ray pass outlines (see _xray_arm)
        pieces = [dict(pts=upper, fill=skin, hide=hide),
                  dict(pts=fore, fill=skin, part="fore")]
        lines = []
        fil, _ = _fillet(sh, el, wr, upper, fore, 3.2 * S, 2.4 * S, S)
        if fil:
            pieces.append(dict(pts=fil, fill=skin))
        on = getattr(self, "_on", set())
        if s + "upper" in on:
            # the belly of the biceps or triceps, below the sleeve
            lines.append(self._belly_shade(sh, el, up_l, up_r, SLEEVE_LEN + 0.03, 0.93,
                                           skin, peak=0.45))
        if s + "fore" in on:
            # the forearm's muscles lie in its upper part, its tendons below
            lines.append(self._belly_shade(el, wr, fo_l, fo_r, 0.04, 0.8, skin, peak=0.3))
        lines = [ln for ln in lines if ln]
        hlen = length(sub(ha, wr))
        k = hlen / 7.0 if hlen > 1e-6 else S
        y = mul(perp(v), th)
        hanging = getattr(self, s + "h") is None and ha is self.J[s + "ha"]
        style = self.hand_style.get(s)
        if style == "open":
            palm = [(0, -2.5), (2.6, -3.0), (5.4, -3.4), (7.8, -3.4), (8.6, -2.0),
                    (8.8, 0), (8.6, 2.2), (7.8, 3.4), (5.0, 3.8), (2.6, 3.4), (0, 2.5)]
            pieces.append(dict(pts=catmull(_frame_pts(wr, v, y, palm, k, S), k=3),
                               fill=skin, part="hand"))
            for (fy, a, fl) in ((-2.5, -20, 5.6), (-0.85, -7, 6.6), (0.8, 6, 6.4),
                                (2.5, 18, 5.4), (3.0, 52, 5.0)):
                base = add(add(wr, mul(v, (7.6 if a < 40 else 3.6) * k)), mul(y, fy * S))
                dirn = add(mul(v, math.cos(math.radians(a))),
                           mul(y, math.sin(math.radians(a))))
                tip = add(base, mul(dirn, fl * S))
                rr = 1.25 if a > 40 else 1.0
                pieces.append(dict(pts=capsule(base, rr * S, tip, rr * 0.85 * S, n=6),
                                   fill=skin, part="finger"))
        else:
            # at this size the fingers are only noise: the hand is its outline
            shape = HAND_HANG if hanging else HAND_GRIP
            pieces.append(dict(pts=catmull(_frame_pts(wr, v, y, shape, k, S), k=3),
                               fill=skin, part="hand"))
        pieces.append(dict(pts=sleeve, fill=col["shirt"], hide=hide))
        if not ghost:
            # the sleeve hem: the curved end of the sleeve
            d = norm(sub(se, sh))
            nv = perp(d)
            a = _profile(SLEEVE, 1) * S
            lines.insert(0, dict(pts=[add(se, mul(nv, a))] + _cap(se, d, nv, a, a, 0.2) +
                                 [add(se, mul(nv, -a))], sw=LINE_SW))
        return pieces, lines

    def _leg_geometry(self, s, fill, torso_polys):
        J, S = self.J, self.s
        u, r = self.frame()
        hip, kn, an = J[s + "hip"], J[s + "kn"], J[s + "an"]
        lateral = r if (self.view == "side" or s == "r") else mul(r, -1)

        def front_left(a, b, w):
            # True if the front of segment a->b is on its left: the side the
            # knee juts out to, away from w (the other segment, from the knee)
            dd = norm(sub(b, a))
            c = cross(dd, norm(w))
            if abs(c) > 0.08:
                return c < 0
            return dot(perp(dd), lateral) > 0
        fl = front_left(hip, kn, sub(an, kn))
        back = THIGH_BACK_SIDE if self.view == "side" else THIGH_BACK
        thigh = tube(hip, kn, THIGH_FRONT if fl else back,
                     back if fl else THIGH_FRONT, S, cap1=0, cap2=1)
        # keep the root of the thigh under the T-shirt's hem, so a leg drawn
        # in front of the torso doesn't cover the hem near the hip
        R = 1.25 * back[0][1] * S
        t_hem = 3.0 if self.view == "side" else 3.5
        out = []
        for p in thigh:
            q = sub(p, self.pelvis)
            t = dot(q, u) / S
            if t > t_hem and length(sub(p, hip)) < R and any(pl.has(p) for pl in torso_polys):
                p = sub(p, mul(u, (t - t_hem) * S))
            out.append(p)
        thigh = out
        sl = length(sub(an, kn))
        hem = add(an, mul(norm(sub(kn, an)), min(HEM_ABOVE_ANKLE * S, 0.4 * sl)))
        fs = front_left(kn, an, sub(hip, kn))
        shin = tube(kn, hem, SHIN_FRONT if fs else SHIN_BACK,
                    SHIN_BACK if fs else SHIN_FRONT, S, cap1=1, cap2=0.15)
        hide = _root_hide(hip, kn, R, torso_polys)
        pieces = [dict(pts=thigh, fill=fill, hide=hide), dict(pts=shin, fill=fill)]
        # a bent knee: a soft inner curve
        fil, _ = _fillet(hip, kn, an, thigh, shin, 4.5 * S, 3.2 * S, S)
        if fil:
            pieces.append(dict(pts=fil, fill=fill))
        lines = []
        on = getattr(self, "_on", set())
        th_l, th_r = (THIGH_FRONT, back) if fl else (back, THIGH_FRONT)
        sh_l, sh_r = (SHIN_FRONT, SHIN_BACK) if fs else (SHIN_BACK, SHIN_FRONT)
        if s + "thigh" in on:
            lines.append(self._belly_shade(hip, kn, th_l, th_r, 0.1, 0.9, fill, peak=0.4))
        if s + "ham" in on:
            # the back of the thigh: the side away from the front
            lines.append(self._belly_shade(hip, kn, th_l, th_r, 0.14, 0.9, fill, peak=0.45,
                                           w=0.6, bias=-0.4 if fl else 0.4))
        if s + "calf" in on:
            lines.append(self._belly_shade(kn, hem, sh_l, sh_r, 0.06, 0.62, fill, peak=0.35,
                                           w=0.6, bias=-0.4 if fs else 0.4))
        if s + "shin" in on:
            # the front of the shin, which pulls the toes up in a toe hook
            lines.append(self._belly_shade(kn, hem, sh_l, sh_r, 0.08, 0.7, fill, peak=0.4,
                                           w=0.55, bias=0.4 if fs else -0.4))
        lines = [ln for ln in lines if ln]
        return pieces, lines, thigh

    def _shoe(self, fig, s, st, z):
        ft = getattr(self, "_" + s + "f")
        an = self.J[s + "an"]
        d, n = ft["d"], ft["n"]
        sc = self.s
        detail = st.get("fill") == SHOE_FILL
        if ft["style"] == "back":
            origin = sub(an, (0, 8 * sc))
            pts = [add(origin, (x * sc, y * sc)) for x, y in SHOE_BACK]
            fig.smooth(pts, z=z, tension=0.6, **st)
            if self._xray_feet and not self._ghost:
                fig.smooth(pts, z=XRAY_Z + 1, tension=0.6, **XRAY_STYLE)
            if detail:
                # sole and the top of the heel rubber
                for y, w in ((1.7, 4.3), (4.6, 5.0)):
                    fig.line(add(origin, (-w * sc, y * sc)), add(origin, (w * sc, y * sc)),
                             z=z + 0.01, sw=0.18, stroke="#9a9a9a" if y > 2 else WHITE)
            return
        # place the shoe so that its ankle point sits at the solved ankle
        o = SHOE_ANKLE
        k = ft.get("fore", 1.0)
        base = sub(an, add(mul(d, o[0] * sc * k), mul(n, o[1] * sc)))

        def P(x, y):
            return add(base, add(mul(d, x * sc * k), mul(n, y * sc)))
        pts = [P(x, y) for x, y in SHOE]
        fig.smooth(pts, z=z, tension=0.7, **st)
        if self._xray_feet and not self._ghost:
            fig.smooth(pts, z=XRAY_Z + 1, tension=0.7, **XRAY_STYLE)
        if detail:
            shoe_details(fig, P, z + 0.01)

    # handy reference points
    def cog(self):
        """Rough centre of gravity: just above the pelvis on the spine."""
        u, _ = self.frame()
        return add(self.pelvis, mul(u, 12 * self.s))

    def warn(self):
        """Hands or feet that don't reach their holds, and (side view) joint
        angles a human body can't make."""
        out = []
        J = self.J
        u, r = self.frame()
        for s in "lr":
            ft = getattr(self, "_" + s + "f")
            if ft["short"]:
                out.append(s + " foot out of reach")
            t = getattr(self, s + "h")
            if t is not None and length(sub(t, J[s + "ha"])) > 1:
                out.append(s + " hand out of reach")
            if self.view == "side":
                thigh = sub(J[s + "kn"], J[s + "hip"])
                down = mul(u, -1)
                # hip flexion: 0 = thigh along the spine downward, positive
                # = thigh forward (toward the wall), measured without wrapping
                hip = math.degrees(math.atan2(cross(down, thigh), dot(down, thigh)))
                if hip < -100:
                    hip += 360
                if hip < -30:
                    out.append(f"{s} hip over-extended: thigh {-hip:.0f} deg behind the body")
                if hip > 165:
                    out.append(f"{s} hip over-flexed: thigh {hip:.0f} deg in front of the body (max about 150)")
                # ankle: angle between the shin (pointing up) and the foot;
                # 90 is neutral, below ~50 or above ~160 a real ankle can't go
                shin_up = sub(J[s + "kn"], J[s + "an"])
                ankle = math.degrees(math.acos(max(-1, min(1, dot(norm(shin_up), ft["d"])))))
                if ft["style"] != "back" and ft["contact"] != "heel" and not (45 <= ankle <= 160):
                    kind = "toes pulled up too far" if ankle < 45 else "toes pointed too far"
                    out.append(f"{s} ankle {ankle:.0f} deg ({kind}; 90 is neutral)")
        if self.view == "back":
            out += self._warn_back()
        return out + self._warn_frame()

    def _warn_frame(self):
        """Joints whose outline runs past the edge of the figure they were
        last drawn in, where the panel or film frame cuts them off."""
        f = getattr(self, "_fig", None)
        if f is None:
            return []
        out = []
        joints = [("head", "head", DIM["head_rx"])]
        for s in "lr":
            joints += [(s + "sh", s + " shoulder", DIM["r_shoulder"]),
                       (s + "el", s + " elbow", DIM["r_elbow"]),
                       (s + "ha", s + " hand", DIM["r_hand"]),
                       (s + "kn", s + " knee", DIM["r_knee"]),
                       (s + "an", s + " ankle", DIM["r_ankle"])]
        for key, name, rad in joints:
            x, y = self._head_centre() if key == "head" else self.J[key]
            rr = rad * self.s
            if x - rr < f.x0 or x + rr > f.x1 or y - rr < f.y0 or y + rr > f.y1:
                out.append(f"{name} runs off the frame")
        return out

    def _warn_back(self):
        """Back-view plausibility: projected joints that look wrong."""
        J, out = self.J, []

        def inner(a, b, c):
            v1, v2 = norm(sub(a, b)), norm(sub(c, b))
            return math.degrees(math.acos(max(-1, min(1, dot(v1, v2)))))
        for s in "lr":
            ft = getattr(self, "_" + s + "f")
            hip, kn, an = J[s + "hip"], J[s + "kn"], J[s + "an"]
            knee = inner(hip, kn, an)
            if knee < 50:
                out.append(f"{s} knee folded to {knee:.0f} deg in back view "
                           f"(looks broken below ~50; shorten leg_len or move the foot)")
            # the shin and the foot as drawn: a foot turned toward the viewer
            # foreshortens this angle, so it may pass 45 where a side view can't
            ankle = inner(kn, an, add(an, ft["d"]))
            if ft["style"] == "profile" and ft["contact"] != "heel" and ankle < BACK_ANKLE_MIN:
                out.append(f"{s} ankle {ankle:.0f} deg in back view (looks broken below "
                           f"~{BACK_ANKLE_MIN}; tilt the foot's `angle` or move the hips)")
            # a bent knee should point roughly the way the toes point
            if ft["style"] == "profile" and knee < 150:
                mid = lerp(hip, an, 0.5)
                side = (kn[0] - mid[0]) * ft["d"][0]
                if side < -2 * self.s:
                    out.append(f"{s} knee points against the toes (the foot points "
                               f"{'right' if ft['d'][0] > 0 else 'left'}, the knee the other way)")
            el = inner(J[s + "sh"], J[s + "el"], J[s + "wr"])
            if el < 35:
                out.append(f"{s} elbow folded to {el:.0f} deg in back view")
        # limbs crossing each other (fine for a back flag or cross-through:
        # pass allow_cross=True to the climber then)
        if not getattr(self, "allow_cross", False):
            def segs(s, kind):
                if kind == "leg":
                    return [(J[s + "hip"], J[s + "kn"]), (J[s + "kn"], J[s + "an"])]
                return [(J[s + "sh"], J[s + "el"]), (J[s + "el"], J[s + "wr"])]
            for kind in ("leg", "arm"):
                hit = any(_seg_cross(a, b, c, d) for a, b in segs("l", kind)
                          for c, d in segs("r", kind))
                if hit:
                    out.append(f"{kind}s cross each other (pass allow_cross=True if intended)")
        return out


def capsule(p1, r1, p2, r2, n=14):
    v = sub(p2, p1)
    L = length(v)
    if L < 1e-6 or abs(r1 - r2) >= L:
        c, r = (p1, r1) if r1 >= r2 else (p2, r2)
        return [add(c, mul(ang(i * 360 / (2 * n)), r)) for i in range(2 * n)]
    th = math.atan2(v[1], v[0])
    phi = math.acos((r1 - r2) / L)
    pts = []
    for i in range(n + 1):
        a = th + phi - (2 * phi) * i / n
        pts.append((p2[0] + r2 * math.cos(a), p2[1] + r2 * math.sin(a)))
    for i in range(n + 1):
        a = th - phi - (2 * math.pi - 2 * phi) * i / n
        pts.append((p1[0] + r1 * math.cos(a), p1[1] + r1 * math.sin(a)))
    return pts


# ---------------------------------------------------------------- panels


def combine(figs, path, gap=4.0, labels=None, captions=None, align="bottom", margin=0.0):
    """Lay out several figures side by side in one SVG, with optional
    panel letters and captions under each panel, and `margin` of white to the
    right of the last (sizes in mm)."""
    sizes = [((f.x1 - f.x0) * f.scale, (f.y1 - f.y0) * f.scale) for f in figs]
    cap_h = 5.0 if captions else 0.0
    lab_h = 0.0
    W = sum(w for w, _ in sizes) + gap * (len(figs) - 1) + margin
    H = max(h for _, h in sizes) + cap_h + lab_h
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
           f'height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">']
    x = 0.0
    hmax = max(h for _, h in sizes)
    for i, (f, (w, h)) in enumerate(zip(figs, sizes)):
        y = (hmax - h) if align == "bottom" else 0.0
        inner = f.svg().split("\n", 1)[1].rsplit("</svg>", 1)[0]
        fw, fh = f.x1 - f.x0, f.y1 - f.y0
        out.append(f'<clipPath id="cp{i}"><rect x="0" y="0" width="{fw:.2f}" '
                   f'height="{fh:.2f}"/></clipPath>')
        out.append(f'<g transform="translate({x:.2f},{y:.2f}) '
                   f'scale({f.scale:.5f})"><g clip-path="url(#cp{i})">{inner}</g></g>')
        if labels:
            out.append(f'<text x="{x + 1:.2f}" y="{3.2:.2f}" font-family="{FONT}" '
                       f'font-size="3.3" font-weight="700">{esc(labels[i])}</text>')
        if captions:
            out.append(f'<text x="{x + w / 2:.2f}" y="{hmax + 3.8:.2f}" '
                       f'font-family="{FONT}" font-size="2.9" font-weight="500" '
                       f'text-anchor="middle">{esc(captions[i])}</text>')
        x += w + gap
    out.append("</svg>")
    with open(path, "w") as fh:
        fh.write("\n".join(out) + "\n")


def _wrap(text, width_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def filmstrip(frames, path, captions=None, gap=2.2, band=4.2, zoom=1.0):
    """Lay out frames (Fig objects) as a strip of film: a dark band with
    sprocket holes above and below, numbered frames, and a short caption
    under each frame, wrapped to fit unless "\n" says where it should break.
    Sizes in mm. Use the same Fig scale for every frame (0.28 keeps a five-frame
    strip of back views within the page width). zoom scales the frames' drawings,
    as a plate of close-ups drawn at their own scale is reduced."""
    sizes = [((f.x1 - f.x0) * f.scale * zoom, (f.y1 - f.y0) * f.scale * zoom) for f in frames]
    fh = max(h for _, h in sizes)
    W = sum(w for w, _ in sizes) + gap * (len(frames) + 1)
    # a caption is wrapped to its frame, unless "\n" says where it should break
    cap_lines = [c.split("\n") if "\n" in c else _wrap(c, max(8, int(w / 1.75)))
                 for c, (w, _) in zip(captions or [""] * len(frames), sizes)]
    cap_h = (max(len(c) for c in cap_lines) * 3.6 + 2.5) if captions else 0
    H = band * 2 + fh + cap_h
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
           f'height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">']
    film = "#3a3a3a"
    out.append(f'<rect x="0" y="0" width="{W:.2f}" height="{band * 2 + fh:.2f}" '
               f'fill="{film}"/>')
    # sprocket holes
    x = 1.2
    while x + 1.6 < W:
        for y in (band / 2 - 0.65, band + fh + band / 2 - 0.65):
            out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="1.6" height="1.3" '
                       f'rx="0.3" fill="#ffffff"/>')
        x += 3.4
    x = gap
    for i, (f, (w, h)) in enumerate(zip(frames, sizes)):
        y = band + (fh - h)
        out.append(f'<rect x="{x:.2f}" y="{band:.2f}" width="{w:.2f}" '
                   f'height="{fh:.2f}" fill="#ffffff"/>')
        inner = f.svg().split("\n", 1)[1].rsplit("</svg>", 1)[0]
        fw, fhh = f.x1 - f.x0, f.y1 - f.y0
        out.append(f'<clipPath id="fs{i}"><rect x="0" y="0" width="{fw:.2f}" '
                   f'height="{fhh:.2f}"/></clipPath>')
        out.append(f'<g transform="translate({x:.2f},{y:.2f}) scale({f.scale * zoom:.5f})">'
                   f'<g clip-path="url(#fs{i})">{inner}</g></g>')
        # frame number
        out.append(f'<rect x="{x + 0.8:.2f}" y="{band + 0.8:.2f}" width="4.2" '
                   f'height="4.2" rx="0.6" fill="{film}"/>')
        out.append(f'<text x="{x + 2.9:.2f}" y="{band + 4.0:.2f}" font-family="{FONT}" '
                   f'font-size="3.1" font-weight="700" text-anchor="middle" '
                   f'fill="#ffffff">{i + 1}</text>')
        if captions:
            for k, line in enumerate(cap_lines[i]):
                out.append(f'<text x="{x + w / 2:.2f}" y="{band * 2 + fh + 4.2 + k * 3.6:.2f}" '
                           f'font-family="{FONT}" font-size="2.95" font-weight="500" '
                           f'text-anchor="middle">{esc(line)}</text>')
        x += w + gap
    out.append("</svg>")
    with open(path, "w") as fh_:
        fh_.write("\n".join(out) + "\n")
