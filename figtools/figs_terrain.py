"""Figures for the terrain chapter (07) and the reading chapter (02)."""

from climb import *
from figs_hands import flat_palm
import plan


# ---------------------------------------------------------------- helpers


def warn(name, *climbers):
    for c in climbers:
        for w in c.warn():
            print(name + ":", w)


def tag(fig, s, p, z=85, size=6.8):
    """A small boxed label such as L1 or R2."""
    w = fig.mm(1.25 + 1.55 * len(s))
    h = fig.mm(3.4)
    x, y = p
    fig.poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2),
              (x + w / 2, y + h / 2), (x - w / 2, y + h / 2)],
             z=z, fill=WHITE, stroke=INK, sw=0.3)
    fig.text(s, (x, y), size=size, weight=700, z=z + 1, halo=False)


def ceiling(fig, x0, x1, y, z=-20):
    """A horizontal roof surface at height y, seen from the side, hatched
    above (the rock is above the line)."""
    t = fig.mm(2.2)
    fig.poly([(x0, y), (x1, y), (x1, y + t), (x0, y + t)], z=z, fill=PALE,
             stroke=None)
    fig.line((x0, y), (x1, y), z=z + 1, sw=0.6)
    x = x0
    while x < x1:
        fig.line((x, y), (x + fig.mm(1.4), y + t), z=z + 1, sw=0.18,
                 stroke=MID)
        x += fig.mm(2.0)


def hatch_block(fig, pts, z=-20):
    """A solid piece of wall (filled, outlined), marked so the site's dark copy
    can tell it from a volume of the same grey."""
    fig.poly(pts, z=z, fill=PALE, stroke=INK, sw=0.5, wall=True)


def wall_dirs(angle):
    """Unit vectors up the wall and out of it (toward the climber) for a
    side-view wall of the given overhang angle, as in climb.hold_side."""
    d = norm((-math.tan(math.radians(angle)), 1))
    return d, (-d[1], d[0])


def off(p, angle, out=0.0, up=0.0):
    """The point `out` cm out from the wall surface at `p` and `up` cm
    further up the wall."""
    d, n = wall_dirs(angle)
    return add(p, add(mul(n, out), mul(d, up)))


def slab_scene(f, good, x=20, y0=30, y1=250, angle=-15, F_h=70):
    """A side-view slab with one foothold and two small hand holds. good:
    hips stacked over the foot, heel low; bad: chest to the wall, heel up.
    Returns (climber, foot contact point)."""
    at = wall_side(f, x, y0, y1, angle=angle)
    F = at(F_h)
    hold_side(f, "foot", F, angle=angle, size=0.8)
    foot = off(F, angle, 1.6, 2.4)
    if good:
        # the hands press low, about level with the chin, so the bent
        # elbows hang below them, clear of the slab
        H1, H2 = at(F_h + 156), at(F_h + 144)
        # the weight is on the foot: the hands only steer
        c = Climber((foot[0] - 4, F_h + 96), view="side", lean=10,
                    lh=off(H1, angle, 2.5, 1.5), rh=off(H2, angle, 2.5, 1.5),
                    lf={"at": foot, "contact": "edge", "angle": 5},
                    rf={"at": foot, "contact": "edge", "angle": 5}, active=())
    else:
        # chest on the slab, reaching high: the arms run up along the wall
        # nearly straight, the elbows turned out to the sides (so the arms
        # are a little shortened); a bend toward the wall would put the
        # elbows into it
        H1, H2 = at(F_h + 194), at(F_h + 186)
        c = Climber((foot[0] + 12, F_h + 94), view="side", lean=18,
                    lh=off(H1, angle, 2.5, 1.5), rh=off(H2, angle, 2.5, 1.5),
                    arm_len={"l": 0.965, "r": 0.84},
                    lf={"at": foot, "contact": "toe", "angle": -15},
                    rf={"at": foot, "contact": "toe", "angle": -15})
    for H in (H1, H2):
        hold_side(f, "edge", H, angle=angle, size=0.9)
    c.draw(f)
    return c, foot


def vertical_scene(f, x=28, y0=30, y1=250):
    """A side-view vertical wall: straight arms on a jug, hips close to the
    wall, feet on one foothold. Returns (climber, foot contact point)."""
    at = wall_side(f, x, y0, y1, angle=0)
    H, F = at(246), at(44)
    hold_side(f, "jug", H)
    hold_side(f, "foot", F)
    foot = off(F, 0, 1.6, 2.4)
    hand = off(H, 0, 3.5, 2)
    c = Climber((x - 20, 139), view="side", lean=4, lh=hand, rh=hand,
                lf={"at": foot}, rf={"at": foot}, head=(0, 1))
    c.draw(f)
    return c, foot


def overhang_scene(f, good=True, x=106, y0=20, y1=250, angle=30):
    """A side-view 30-degree overhang. good: feet up, toes pulling, hips in,
    arms straight; bad: low feet, stretched out. Returns (climber, foot)."""
    at = wall_side(f, x, y0, y1, angle=angle)
    H = at(222)
    F = at(108) if good else at(34)
    hold_side(f, "jug", H, angle=angle)
    hold_side(f, "foot", F, angle=angle)
    hand = off(H, angle, 3.5, 2)
    foot = off(F, angle, 1.6, 2.4)
    if good:
        # as in photographs of overhangs from the side: the feet high with
        # the knees well bent, the arms straight, the trunk hanging nearly
        # upright below the hands and the hips in close; body tension and
        # the toes pulling in keep the feet on
        c = Climber(None, shoulders=add(hand, (-24, -58)), view="side",
                    lean=-20, bend=-8, lh=hand, rh=hand, head=(1, 1),
                    lf={"at": foot, "contact": "toe", "angle": -10},
                    rf={"at": foot, "contact": "toe", "angle": -10},
                    active=("+core",))
    else:
        # stretched out between the hand and the low foot, but hanging off
        # the wall: drawn on the line between them, the body hid the wall
        _, n = wall_dirs(angle)
        v = norm(sub(foot, hand))
        sh = add(hand, add(mul(v, 62), mul(n, 14)))
        hips = add(hand, add(mul(v, 118), mul(n, 17)))
        u = norm(sub(hips, sh))
        ln = 90 - math.degrees(math.atan2(-u[1], -u[0]))
        c = Climber(None, shoulders=sh, view="side", lean=ln,
                    lh=hand, rh=hand, head=(1, 1),
                    lf={"at": foot, "contact": "toe", "angle": -20},
                    rf={"at": foot, "contact": "toe", "angle": -20})
    c.draw(f)
    return c, foot


ROOF_Y = 232


def roof_hold(f, x, facing=-1, y=ROOF_Y, z=-5):
    """A jug hanging from a ceiling at height y, seen from the side, its
    incut lip facing left (facing=-1) or right (+1)."""
    hold_side(f, "jug", (x, y), z=z, frame=((0, -1), (facing, 0)))


def roof_room(f, x0, x1, back=None):
    """The ceiling from x0 to x1 and, if given, the back wall at x=back."""
    ceiling(f, x0, x1 if back is None else back, ROOF_Y)
    if back is not None:
        hatch_block(f, [(back, f.y0 - 5), (x1 + 5, f.y0 - 5),
                        (x1 + 5, ROOF_Y + f.mm(2.2)),
                        (back, ROOF_Y + f.mm(2.2))])


ROOF_H = -70     # the hand jug
ROOF_F = 50      # the foothold the toes hook


def roof_climber(f, ghost=False):
    """Under a roof: arms straight, body nearly flat with the hips up, both
    toes hooked behind a foothold (foot flexed, top of the foot pulling)."""
    toe = (ROOF_F + 7.5, ROOF_Y - 2.5)
    # the shins pull the toes in (the near leg hides the far one), and the
    # trunk holds the body flat
    c = Climber(None, shoulders=(ROOF_H + 1, 163), view="side", lean=-110,
                lh=(ROOF_H - 2, ROOF_Y - 6), rh=(ROOF_H - 2, ROOF_Y - 6),
                lf={"at": toe, "contact": "toe", "angle": 100},
                rf={"at": toe, "contact": "toe", "angle": 100},
                head=(-1, 2), active=("+rshin", "+core"))
    c.draw(f, ghost=ghost)
    return c


def combine_rows(rows, path, gap=6.0, row_gap=3.0, labels=None,
                 captions=None):
    """Like climb.combine, but several rows of panels stacked vertically.
    `labels` and `captions` are lists of lists matching `rows`."""
    out_rows = []
    W = 0.0
    y = 0.0
    parts = []
    k = 0
    for r, figs in enumerate(rows):
        sizes = [((f.x1 - f.x0) * f.scale, (f.y1 - f.y0) * f.scale) for f in figs]
        cap_h = 5.0 if captions else 0.0
        hmax = max(h for _, h in sizes)
        x = 0.0
        for i, (f, (w, h)) in enumerate(zip(figs, sizes)):
            yy = y + (hmax - h)
            inner = f.svg().split("\n", 1)[1].rsplit("</svg>", 1)[0]
            fw, fh = f.x1 - f.x0, f.y1 - f.y0
            parts.append(f'<clipPath id="cr{k}"><rect x="0" y="0" width="{fw:.2f}" '
                         f'height="{fh:.2f}"/></clipPath>')
            parts.append(f'<g transform="translate({x:.2f},{yy:.2f}) '
                         f'scale({f.scale:.5f})"><g clip-path="url(#cr{k})">{inner}</g></g>')
            if labels:
                parts.append(f'<text x="{x + 1:.2f}" y="{y + 3.2:.2f}" font-family="{FONT}" '
                             f'font-size="3.3" font-weight="700">{esc(labels[r][i])}</text>')
            if captions:
                parts.append(f'<text x="{x + w / 2:.2f}" y="{y + hmax + 3.8:.2f}" '
                             f'font-family="{FONT}" font-size="2.9" font-weight="500" '
                             f'text-anchor="middle">{esc(captions[r][i])}</text>')
            x += w + gap
            k += 1
        W = max(W, x - gap)
        y += hmax + cap_h + row_gap
    H = y - row_gap
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
           f'height="{H:.2f}mm" viewBox="0 0 {W:.2f} {H:.2f}">'] + parts + ["</svg>"]
    with open(path, "w") as fh:
        fh.write("\n".join(out) + "\n")


# ---------------------------------------------------------------- chapter 02


def hold_orientation(path):
    """Back views: the side a hold opens to sets where the body goes."""
    panels = []
    Y0, Y1 = 22, 240

    # (a) jugs face up: hang straight below them
    f = Fig(-50, Y0, 50, Y1)
    wall_grid(f)
    H1, H2 = (-17, 220), (17, 220)
    LF, RF = (-24, 34), (24, 34)
    for p in (H1, H2):
        hold(f, "jug", p)
    for p in (LF, RF):
        hold(f, "foot", p)
    c = Climber((0, 113), lh=grip(H1), rh=grip(H2),
                lf={"at": stand(LF)}, rf={"at": stand(RF)})
    c.draw(f)
    f.arrow([(36, 232), (36, 210)], kind="force")
    f.cog(c.cog(), plumb_to=Y0 + 6)
    warn("orient-a", c)
    panels.append(f)

    # (b) a sidepull facing right: the right hand pulls it to the left and
    # the body hangs to its left, leaning away on a straight arm
    f = Fig(-58, Y0, 76, Y1)
    wall_grid(f)
    S = (58, 178)
    J = (-40, 214)
    LF, RF = (-30, 42), (26, 50)
    hold(f, "jug", S, use=0)
    hold(f, "jug", J)
    for p in (LF, RF):
        hold(f, "foot", p)
    # both arms hang nearly straight: leaning away, the elbow muscles rest.
    # The body bows away from the sidepull: the hips lean out to the left
    # and the chest bends back toward the hold
    c = Climber((-6, 118), lean=-16, bend=8, lh=grip(J), rh=grip(S, use=0),
                lf={"at": stand(LF)}, rf={"at": stand(RF)},
                elbows={"l": "out", "r": "down"}, head=(-1, 0), active=())
    c.draw(f)
    f.arrow([(70, 194), (48, 194)], kind="force")
    f.cog(c.cog(), plumb_to=Y0 + 6)
    warn("orient-b", c)
    panels.append(f)

    # (c) an undercling faces down: hold low, pull up, feet high
    f = Fig(-52, Y0, 64, Y1)
    wall_grid(f)
    U = (48, 156)
    J = (-30, 214)
    LF, RF = (-26, 62), (24, 70)
    hold(f, "jug", U, use=270)
    hold(f, "jug", J)
    for p in (LF, RF):
        hold(f, "foot", p)
    # the right side bends over the undercling, the left stretches up
    c = Climber((2, 126), lean=-1, bend=6, lh=grip(J), rh=grip(U, use=270),
                lf={"at": stand(LF), "angle": 190}, rf={"at": stand(RF), "angle": -20},
                elbows={"l": "out", "r": "down"}, head=(1, 0))
    c.draw(f)
    f.arrow([(62, 128), (62, 152)], kind="force")
    f.cog(c.cog(), plumb_to=Y0 + 6)
    warn("orient-c", c)
    panels.append(f)

    # (d) a gaston: a hold on your right facing left (toward your midline),
    # taken with the right hand and pushed to the right, elbow out
    f = Fig(-54, Y0, 70, Y1)
    wall_grid(f)
    G = (48, 202)
    J = (-38, 214)
    LF, RF = (-26, 42), (24, 48)
    hold(f, "jug", G, use=180)
    hold(f, "jug", J)
    for p in (LF, RF):
        hold(f, "foot", p)
    # the chest bends a little toward the gaston, staying close to it
    c = Climber((-2, 118), lean=-2, bend=6, lh=grip(J),
                rh=add(grip(G, use=180), (0, -4)),
                lf={"at": stand(LF)}, rf={"at": stand(RF)},
                elbows={"l": "out", "r": "out"}, head=(1, 0))
    c.draw(f)
    f.arrow([(46, 224), (66, 224)], kind="force")
    f.label("elbow out", (52, 150), to=c.J["rel"])
    f.cog(c.cog(), plumb_to=Y0 + 6)
    warn("orient-d", c)
    panels.append(f)

    combine(panels, path, gap=4, labels=["a", "b", "c", "d"],
            captions=["jug: hang below", "sidepull: lean away",
                      "undercling: pull up, feet high", "gaston: push it away"])


# the worked problem of chapter 02: hand holds (kind, position, use) and
# footholds, shared by the diagram and its filmstrip
WP_HANDS = {
    "S": ("jug", (0, 150), 90),
    "R1": ("jug", (48, 180), 0),      # sidepull facing right
    "L2": ("crimp", (2, 212), 90),
    "R3": ("jug", (38, 240), 90),     # a jug: the rest
    "L4": ("crimp", (76, 262), 90),   # right of R3: the cross
    "R5": ("sloper", (46, 302), 90),
    "F": ("jug", (72, 330), 90),
}
WP_HRF = (70, 128)                    # the high right foot
WP_FEET = [(-30, 34), (24, 28), (-14, 82), (40, 74), (-36, 122), WP_HRF,
           (12, 166), (98, 196)]


def wp_grip(name):
    """Where the hand goes on a hold of the worked problem."""
    kind, p, use = WP_HANDS[name]
    return grip(p, use=use, kind=kind)


def worked_problem_wall(f, used=None):
    """Holds and start tape of the worked problem. `used`: the names of
    the hand holds and the positions of the footholds in use; only those
    show their dotted outline through the climber (default: all)."""
    for name, (kind, p, use) in WP_HANDS.items():
        hold(f, kind, p, use=use, xray=used is None or name in used)
    for p in WP_FEET:
        hold(f, "foot", p, size=1.15, xray=used is None or p in used)
    # the start tape sits on the wall, under the climber
    for x in (-14, 14):
        f.poly([(x - 1.6, 146), (x + 1.6, 146), (x + 1.6, 137), (x - 1.6, 137)],
               fill=INK, stroke=None, z=-4)


def reading_problem(path):
    """A worked reading of an indoor problem: hand order, feet and crux."""
    # hand moves of 50-70 cm; the cross L2 -> L4 is the long one
    f = Fig(-78, -8, 128, 352, scale=0.24)
    wall_back(f, -72, 0, 122, 348)
    wall_grid(f, x0=-72, x1=122, y0=8, y1=344)
    ground(f, 0, x0=-78, x1=128)
    worked_problem_wall(f)
    HRF = WP_HRF
    f.label("start: both hands", (-34, 112), to=(-14, 136))
    f.label("finish: match", (16, 336), to=(66, 334))
    # hand order tags beside their holds
    tags = {"R1": (72, 180), "L2": (-22, 212), "R3": (60, 243),
            "L4": (98, 266), "R5": (19, 304), "F": (96, 330)}
    for name, p in tags.items():
        tag(f, "L6" if name == "F" else name, p)
    # moves as dashed arrows
    f.arrow([(6, 158), (30, 166), (40, 176)], kind="move")          # S -> R1
    f.arrow([(-4, 158), (-6, 184), (0, 204)], kind="move")          # S -> L2
    f.arrow([(48, 192), (46, 212), (40, 231)], kind="move")         # R1 -> R3
    f.arrow([(4, 219), (14, 258), (68, 266)], kind="move")          # L2 -> L4
    f.arrow([(42, 248), (50, 272), (48, 292)], kind="move")         # R3 -> R5
    f.arrow([(80, 268), (82, 300), (74, 322)], kind="move")         # L4 -> F
    # crux box around the cross and the slap
    f.poly([(32, 254), (112, 254), (112, 316), (32, 316)], fill=None,
           stroke=INK, sw=0.45, dash=(1.4, 0.9), z=30)
    f.label("crux: cross", (-14, 278))
    f.label("high right foot", (88, 152), to=add(HRF, (2, 2)))
    f.label("rest", (80, 220), to=(44, 235))
    f.save(path)


# ---------------------------------------------------------------- chapter 07


def wall_angles(path):
    """Side views of slab, vertical, overhang and roof."""
    panels = []

    # slab, 15 degrees less than vertical: hips over the feet
    f = Fig(-20, 30, 82, 258)
    c, foot = slab_scene(f, True)
    f.cog(c.cog(), plumb_to=foot[1] + 3)
    warn("angles-slab", c)
    panels.append(f)

    # vertical: hips close, arms straight
    f = Fig(-30, 30, 44, 258)
    c, foot = vertical_scene(f)
    f.cog(c.cog(), plumb_to=foot[1] + 3)
    warn("angles-vertical", c)
    panels.append(f)

    # overhang, 30 degrees: feet up, the weight hangs behind them
    # the scene sits right of centre: the hanging body needs the room
    f = Fig(-62, 30, 84, 258)
    c, foot = overhang_scene(f, True)
    f.cog(c.cog(), plumb_to=foot[1] - 10)
    warn("angles-overhang", c)
    panels.append(f)

    # roof: arms hang straight, feet pull on the ceiling
    f = Fig(-100, 110, 76, 258)
    roof_room(f, -100, 76, back=70)
    roof_hold(f, ROOF_H, -1)
    roof_hold(f, ROOF_F, +1)
    c = roof_climber(f)
    f.cog(c.cog(), plumb_to=116)
    warn("angles-roof", c)
    panels.append(f)

    combine(panels, path, gap=3, labels=["a", "b", "c", "d"],
            captions=["slab", "vertical", "overhang", "roof"], align="top")


def slab(path):
    """Side view on a slab: leaning in vs hips over the feet."""
    panels = []
    for good in (False, True):
        f = Fig(-28, 46, 86, 274)
        c, foot = slab_scene(f, good, y1=280)
        if good:
            f.cog(c.cog(), plumb_to=foot[1] + 3)
            f.label("heel low", (-14, 100), to=add(foot, (-19, 4)))
        else:
            g = c.cog()
            # the plumb line meets the slab above the foot: the weight
            # goes into the hands, not the shoe
            hit = 30 + (g[0] - 20) / math.tan(math.radians(15))
            f.cog(g, plumb_to=hit)
            f.arrow([add(foot, (-4, -3)), add(foot, (-18, -16))], kind="move")
            f.cross(add(foot, (-22, -21)))
            f.label("heel up", (-14, 100), to=add(foot, (-17, 9)))
        warn("slab", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["leaning in: foot skates", "hips back over the foot"])


def dynamic_slab(path):
    """Back view: a volume-to-volume move planned from its end position.
    The feet stand on each volume's top facet out near the apex (the side
    away from the wall), so the hips can sit over them."""
    f = Fig(-146, 26, 140, 290)
    wall_grid(f)
    A = [(-130, 30), (-40, 30), (-58, 92), (-112, 92)]
    B = [(28, 56), (122, 56), (104, 118), (46, 118)]
    volume(f, A, apex=(-85, 62))
    volume(f, B, apex=(75, 88))
    S1 = (-104, 222)
    S2 = (104, 270)
    hold(f, "sloper", S1, size=0.8)
    hold(f, "sloper", S2, size=0.8)
    # start (ghost): crouched on volume A, left hand on its sloper, the
    # chest bending right, toward the jump
    g = Climber((-82, 140), lean=2, bend=8, lh=grip(S1, kind="sloper"),
                rh=(-40, 158), lf={"at": (-108, 72)}, rf={"at": (-62, 72)},
                elbows={"r": "down"})
    g.draw(f, ghost=True)
    # end: right foot landed near B's apex, hips over it, right hand on the
    # sloper, left foot set on B's left facet
    RFt = (86, 94)
    LFt = (46, 90)
    # the open left hand only balances; the right side stretches up to the
    # sloper, so the chest bends back left over the hips, which sink a
    # little so the right arm stays nearly straight
    c = Climber((76, 170), lean=10, bend=-8, lh=(32, 196), rh=grip(S2, kind="sloper"),
                lf={"at": LFt}, rf={"at": RFt, "angle": 0},
                elbows={"l": "down"}, knees={"l": "out", "r": "out"},
                hand_style={"l": "open"}, head=(2, 1),
                active=("-lupper", "-lfore"))
    c.draw(f)
    f.body_arrow([(-80, 168), (-14, 240), (46, 224)], width=2.4)
    f.step(1, add(RFt, (16, -8)))
    f.step(2, add(S2, (16, 6)))
    f.step(3, add(LFt, (-14, -10)))
    f.label("hips over the foot", (90, 36), to=add(RFt, (2, -2)))
    f.label("start", (-132, 148), size=7.5)
    warn("dynamic-slab", g, c)
    f.save(path)


def overhang(path):
    """Side view, 30 degree overhang: stretched with low feet vs feet up."""
    panels = []
    for good in (False, True):
        # (b) sits further left on the wall: its body hangs out from
        # the hands while (a) lies along the wall down to the low foot
        # (narrow enough to sit beside the steps)
        f = Fig(-58, 20, 72, 250) if good else Fig(-38, 20, 104, 250)
        c, foot = overhang_scene(f, good)
        if good:
            f.arrow([add(foot, (-18, -16)), add(foot, (-4, -7))], kind="force")
            f.label("toes pull in", (16, 70), to=add(foot, (-4, -3)))
            f.label("arms straight", (24, 238),
                    to=add(lerp(c.J["rsh"], c.J["rha"], 0.45), (10, -2)))
            f.cog(c.cog(), plumb_to=foot[1] - 12)
        else:
            f.arrow([add(foot, (-6, -2)), add(foot, (-26, 4)), add(foot, (-40, 20))],
                    kind="move")
            f.cross(add(foot, (-10, -11)))
            # beside the arrow, between it and the plumb line
            f.text("feet", (42, 75), size=7.5)
            f.text("cut loose", (42, 75 - f.pt(9.5)), size=7.5)
            f.cog(c.cog(), plumb_to=26)
        warn("overhang", c)
        panels.append(f)
    combine(panels, path, gap=4.5, labels=["a", "b"],
            captions=["stretched out", "feet up, hips in"])


def roof(path):
    """Side view under a roof: pushing feet swing off; hooked toes hold."""
    panels = []
    for good in (False, True):
        f = Fig(-100, 6, 76, 250)
        roof_room(f, -100, 76, back=72)
        roof_hold(f, ROOF_H, -1)
        roof_hold(f, ROOF_F, +1)
        if good:
            c = roof_climber(f)
            toe = (ROOF_F + 7.5, ROOF_Y - 2.5)
            f.arrow([add(toe, (10, -38)), add(toe, (-8, -38))], kind="force")
            f.label("toes hook and pull", (24, 150), to=add(toe, (-2, -6)))
            f.label("arms straight", (-61, 213), to=(ROOF_H + 2, 204), size=7)
        else:
            # before: the soles push on the near face of the foothold.
            # Both moments hang from the same jug on straight arms, so
            # their shoulders coincide: a whole ghost body would share the
            # climber's arms and put its head on the climber's shoulder.
            # Only the legs, which swing, are drawn as the ghost
            sole = (ROOF_F - 4.8, ROOF_Y - 4.5)
            g = Climber(None, shoulders=(ROOF_H + 1, 163), view="side",
                        lean=-110, lh=(ROOF_H - 2, ROOF_Y - 6),
                        rh=(ROOF_H - 2, ROOF_Y - 6), head=(-1, 2),
                        lf={"at": sole, "contact": "ball", "angle": 100},
                        rf={"at": sole, "contact": "ball", "angle": 100},
                        order=["lleg", "rleg"])
            g.draw(f, ghost=True)
            # after: a hand moves, the feet slip and the body swings down
            dangle = {"at": (ROOF_H + 14, 16), "contact": "toe", "angle": -40}
            c = Climber(None, shoulders=(ROOF_H + 2, 163), view="side",
                        lean=-4, lh=(ROOF_H - 2, ROOF_Y - 6),
                        rh=(ROOF_H - 2, ROOF_Y - 6), head=(1, 0),
                        lf=dangle, rf=dangle)
            c.draw(f)
            f.arrow([add(sole, (-4, -16)), (34, 120), (-30, 40)], kind="move")
            f.cross(add(sole, (12, -12)))
            f.label("feet swing off", (32, 70), size=7.5)
            warn("roof-ghost", g)
        warn("roof", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["pushing: feet swing off", "toes pull: feet stay on"])


ARETE_R = 9.0          # the rounded edge, as wide as it looks from behind
ARETE_SIDE = "#d4d4d4"  # the side face, turned away from the light


def shade_strip(f, x0, x1, lo, hi, c0, c1, z):
    """A vertical strip from x0 to x1 shaded from colour c0 to c1."""
    import hashlib
    a, b = f.P((x0, lo)), f.P((x1, hi))
    gid = "sh" + hashlib.md5(f"{a}{b}{c0}{c1}".encode()).hexdigest()[:10]
    f.add(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
          f'x1="{a[0]:.2f}" y1="0" x2="{b[0]:.2f}" y2="0">'
          f'<stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/>'
          f'</linearGradient><rect x="{a[0]:.2f}" y="{b[1]:.2f}" '
          f'width="{b[0] - a[0]:.2f}" height="{a[1] - b[1]:.2f}" fill="url(#{gid})"/>', z)


def arete_wall(f, E):
    """An arête seen from behind: the main face (bolt holes) left of the
    edge at x=E; right of it the side face, turned away from us and seen
    obliquely, so it is shaded and its bolt holes sit closer together; and
    between them the rounded edge, light where it catches the light and
    darkening as it turns into the side face."""
    R = ARETE_R
    lo, hi = f.y0 - 5, f.y1 + 5
    wall_grid(f, x1=E - 6)
    f.poly([(E + R, lo), (f.x1 + 5, lo), (f.x1 + 5, hi), (E + R, hi)], z=-35,
           fill=ARETE_SIDE, stroke=None)
    # the side face's bolt holes: rows at the main face's heights, columns
    # foreshortened to about half the spacing
    x = E + R + 5
    while x < f.x1 + 2:
        y = math.ceil(f.y0 / 20) * 20
        while y <= f.y1:
            f.circle((x, y), f.mm(0.3), z=-34, fill="#a0a0a0", stroke=None)
            y += 20
        x += 9
    # the rounded edge: the outline where the main face starts to round
    # off, a highlight, then shading into the side face
    shade_strip(f, E, E + R * 0.25, lo, hi, WHITE, WHITE, -34)
    shade_strip(f, E + R * 0.25, E + R + 0.05, lo, hi, WHITE, ARETE_SIDE, -34)
    f.line((E, lo), (E, hi), z=-5, sw=0.5)


def arete(path):
    """Back view: laybacking an arete, and a heel hook round it."""
    panels = []
    E = 40
    for k in range(2):
        f = Fig(-66, 24, 88, 246)
        arete_wall(f, E)
        f.label("arête", (66, 236), size=7.5)
        if k == 0:
            # a gym wall: a few holds on the face, none near the edge
            hold(f, "jug", (-50, 200), variant="flat")
            hold(f, "crimp", (-54, 96))
            hold(f, "foot", (-34, 58))
            # body turned to face the edge, leaning away on nearly straight
            # arms, the fingers wrapped round the edge; the toes press on
            # two small footholds on the side face (seen obliquely, so
            # narrower). The legs push and do the work; the arms hang on
            # the edge nearly straight. Between them the back rounds, the
            # chest curling toward the edge
            LF, RF = (E + 15, 50), (E + 17, 76)
            for p in (LF, RF):
                hold(f, "foot", sub(p, (0, 2.2)), w=5.5)
            c = Climber((-6, 112), turn=-0.85, lean=-18, bend=8,
                        lh=(E - 1, 164), rh=(E - 1, 194),
                        lf={"at": LF, "angle": 30, "contact": "ball"},
                        rf={"at": RF, "angle": 30, "contact": "ball"},
                        elbows={"l": "down", "r": "down"},
                        knees={"l": "right", "r": "right"}, head=(3, 1),
                        active=("lthigh", "rthigh"))
            c.draw(f)
            f.arrow([(E - 8, 214), (E - 30, 214)], kind="force")
            f.arrow([(66, 66), (84, 66)], kind="force")
            f.label("hands pull left", (-10, 228), size=7.5)
            # left of the edge: the side face is too narrow for it
            f.label("feet push right", (4, 36), size=7.5)
        else:
            J = (-36, 217)
            LF = (-18, 56)
            hold(f, "jug", J)
            hold(f, "foot", LF)
            hold(f, "crimp", (-56, 150))
            hold(f, "foot", (-54, 42))
            # the heel round the edge just below hip height: the knee
            # raised and pointing up and out like the toes, the shin coming
            # down to the ankle on top of the shoe. The top of the shoe faces
            # the knee, heel on the side face, toes pulled up and out. The
            # thigh and shin point partly toward the wall, so they are a
            # little shortened. The hook rests the arms, so they hang nearly
            # straight; it hikes the right hip, and the right side bends
            # over it
            heel = (E + 6, 100)
            c = Climber((0, 114), turn=0.3, lean=-9, bend=6, lh=grip(J),
                        rh=(E - 1, 220), lf={"at": stand(LF), "angle": 205},
                        rf={"at": heel, "angle": 35, "contact": "heel"},
                        leg_len={"r": (0.85, 0.85)},
                        elbows={"r": "down"}, knees={"r": "up"}, head=(2, 1),
                        active=("+rham",))
            c.draw(f)
            # below the heel on the side face, clear of the edge line
            f.label("heel round", (64, 68), to=add(heel, (3, -1)), size=7,
                    anchor="middle")
            f.arrow([(E + 26, 122), (E + 11, 122)], kind="force")
        warn("arete", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["layback the edge", "heel hook round it"])


def corner(path):
    """Back view into an inside corner, and the same from above."""
    f = Fig(-95, 30, 95, 250)
    # right-hand wall shaded, fold line at x=0
    f.poly([(0, 30), (95, 30), (95, 250), (0, 250)], z=-45, fill=PALE,
           stroke=None)
    wall_grid(f, x1=-5)
    f.line((0, 30), (0, 250), z=-5, sw=0.6)
    for p in ((-66, 82), (64, 90)):
        hold(f, "foot", p)
    # palms and feet press out, but the legs carry the weight and the arms
    # can rest, so only the legs pressing apart are shaded. As in
    # photographs of stemming from behind, the legs spread wide with the
    # knees only partly bent, and the arms reach out to the sides nearly
    # straight, the palms a little below the shoulders
    c = Climber((0, 162), lh=(-78, 190), rh=(78, 194),
                lf={"at": stand((-66, 82)), "angle": 180},
                rf={"at": stand((64, 90)), "angle": 0},
                elbows={"l": "down", "r": "down"},
                hand_style={"l": "open", "r": "open"},
                active=("lthigh", "rthigh"))
    c.draw(f)
    f.arrow([(-76, 210), (-92, 210)], kind="force")
    f.arrow([(76, 214), (92, 214)], kind="force")
    f.arrow([(-74, 98), (-90, 98)], kind="force")
    f.arrow([(72, 106), (88, 106)], kind="force")
    f.cog(c.cog(), plumb_to=45)
    # two lines on the left wall, under the arm and clear of the head: one
    # line is wider than a wall and would cross the fold line
    f.label("palms and feet", (-56, 173), size=7.5)
    f.label("press out", (-56, 163), size=7.5)
    warn("corner", c)

    # from above: the climber faces into the corner, and the palms and feet push at
    # right angles to each wall. The hands and feet are as far out to the sides as
    # in (a), and the fold is as far away as puts the palms level with the
    # shoulders, as the arms reach out nearly straight
    g = Fig(-72, 0, 72, 130)
    fold = 66                       # cm from the pelvis to where the walls meet
    view = plan.View((0, 55), 0.74)
    apex = view.P((0, fold))
    plan.wall(g, view.P((-92, fold - 92)), apex, depth=3.5)
    plan.wall(g, apex, view.P((92, fold - 92)), depth=3.5)
    arms, legs = {}, {}
    for side, sgn in (("l", -1), ("r", 1)):
        into, along = norm((sgn, 1)), norm((sgn, -1))   # into the wall, and away from the fold
        px = c.J[side + "ha"][0] - c.pelvis[0]
        palm = (px, fold - abs(px))
        # the shoe points into the wall, its ankle where (a) has it
        ax = c.J[side + "an"][0] - c.pelvis[0]
        toe_x = ax + sgn * 18 * math.cos(math.radians(45))
        toe = (toe_x, fold - abs(toe_x))
        arms[side] = dict(hand=sub(palm, mul(into, 3)),
                          flat=add(sub(palm, mul(into, 1.6)), mul(along, 17)))
        legs[side] = dict(ankle=sub(toe, mul(into, 18.2)), deg=90 - sgn * 45,
                          knee=(c.J[side + "kn"][0] - c.pelvis[0], 4))
        for p in (add(palm, mul(along, 8)), toe):
            q = view.P(p)
            g.arrow([add(q, mul(into, 7.5)), add(q, mul(into, 19))], kind="force")
    plan.climber(g, view, lean=(0, -20), arms=arms, legs=legs)
    g.label("faces into the corner", (0, 16), size=7)
    combine([f, g], path, gap=6, labels=["a", "b"],
            captions=["bridged across the corner", "from above"])


def volume_fig(path):
    """Side view: standing on a volume near the wall vs on its far edge."""
    panels = []
    W = 40
    for good in (False, True):
        f = Fig(-56, 44, 56, 292)
        at = wall_side(f, W, 30, 292, angle=0)
        # a wedge volume whose top face rises 20 degrees to the wall
        p0, p2, p1 = volume_side(f, at(50), 44, 66, angle=0, top=0.76)
        face = norm(sub(p1, p2))
        up = (-face[1], face[0])            # out of the top face
        if good:
            foot = add(lerp(p2, p1, 0.16), mul(up, 0.8))
            H1, H2 = at(280), at(266)
            # the weight is on the foot: the hands only steer
            c = Climber((foot[0] - 6, foot[1] + 92), view="side", lean=10,
                        lh=off(H1, 0, 2.5, 1.5), rh=off(H2, 0, 2.5, 1.5),
                        lf={"at": foot, "contact": "ball", "angle": 10},
                        rf={"at": foot, "contact": "ball", "angle": 10},
                        active=())
        else:
            foot = add(lerp(p2, p1, 0.84), mul(up, 0.8))
            H1, H2 = at(276), at(262)
            # pushed back off the slope, the bent arms hold on; the elbows
            # stay on the climber's side of the wall
            c = Climber((foot[0] - 28, foot[1] + 84), view="side", lean=2,
                        lh=off(H1, 0, 2.5, 1.5), rh=off(H2, 0, 2.5, 1.5),
                        lf={"at": foot, "contact": "ball", "angle": 14},
                        rf={"at": foot, "contact": "ball", "angle": 14})
        for H in (H1, H2):
            hold_side(f, "edge", H, size=0.9)
        c.draw(f)
        if good:
            f.cog(c.cog(), plumb_to=foot[1] + 3)
        else:
            f.cog(c.cog(), plumb_to=foot[1] - 4)
            f.arrow([add(foot, (-4, -3)), add(foot, (-30, -13))], kind="move")
            # beside the heel: the mistake is this foot, not the far edge
            f.cross(add(foot, (-27, 8)))
        warn("volume", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["near the wall: pushed off", "far edge: hips over foot"])


# pressing out at the lip of a vertical wall (lip at x=40, y=200), right
# foot on top beside the hands. Its knee points out to the side, toward
# us, so that leg is foreshortened and drawn in front of the arm. The
# straight arms press, so they work. The chest curls over the hands, which
# sit ahead of the shoe so their flat palms show (press_palms).
# Shared by the top-out figure and its filmstrip.
TOP_OUT_PRESS = dict(pelvis=(16, 232), lean=45, bend=12, lh=(73, 203), rh=(67, 203),
                     leg_len={"r": 0.85},
                     rf={"at": (46, 201), "contact": "ball", "angle": -10},
                     order=["lleg", "larm", "torso", "rarm", "rleg"],
                     active=("+lupper", "+lfore", "+rupper", "+rfore"))


def press_palms(f, p, top=200):
    """Flat palms on the top under a pose's hands, set as in Mantle: the
    hand point 1 cm behind its palm and just above it."""
    flat_palm(f, (p["lh"][0] + 1, top), fill=LEFT, z=1.5)
    flat_palm(f, (p["rh"][0] + 1, top), z=3.5)


def top_out(path):
    """A heel-hook top-out on a flat-topped boulder. (a) From behind: feet
    high, right heel hooked on the lip beside the hands. (b) From the side:
    rolled onto the toe, knee in, chest over the top, a palm pressing."""
    LIP = 200
    # (a) back view: the boulder face with its lip, the top seen edge-on
    a = Fig(-70, 90, 92, 246)
    wall_grid(a, y1=LIP - 4)
    a.poly([(a.x0, LIP), (a.x1, LIP), (a.x1, LIP + 9), (a.x0, LIP + 9)],
           z=-30, fill=PALE, stroke=None)
    a.line((a.x0, LIP), (a.x1, LIP), z=-5, sw=0.7)
    # the right leg swung up and out to the side, as a climber throws a
    # heel onto a lip: the thigh rises from the hip, the knee bends a
    # little and points down and out, and the shin reaches up and out to
    # the heel, which sits on the edge of the top with the toes pointing
    # out and up. The shin comes toward us, so the sole is down although
    # the knee is below the heel: "flip" turns the top of the shoe away
    # from the knee. The shin points a little into the wall, so it is a
    # little shortened. The heel is well outside the right hand, so the
    # arm and leg stay apart. The hands grip the lip at shoulder height,
    # elbows down; the forearms point into the wall, so the arms are
    # shortened. The left foot is high: a frog leg whose knee points out
    # and a little toward the wall, so its thigh is shortened. The arms
    # and the heel pull together; the heel hikes the right hip, and the
    # right side bends over it to keep the shoulders level.
    LF = (-38, 112)
    HEEL = (66, LIP + 1)
    hold(a, "foot", LF)
    c = Climber((2, 156), lean=-10, bend=8, lh=(-44, LIP + 4), rh=(34, LIP + 4),
                lf={"at": stand(LF)},
                rf={"at": HEEL, "contact": "heel", "angle": 32, "flip": True},
                knees={"l": "out", "r": "down"},
                arm_len={"l": 0.82, "r": 0.8},
                leg_len={"l": (0.8, 0.9), "r": (0.97, 0.88)},
                elbows={"l": "down", "r": "down"}, head=(5, -1),
                active=("+rham",))
    c.draw(a)
    a.label("heel on the lip", (50, 237), to=add(HEEL, (0, 10)))
    a.label("foot high", (-6, 98), to=add(stand(LF), (5, -1)))
    warn("top-out-a", c)

    # (b) side view: rolled onto the toe, knee in, chest over the top
    b = Fig(-30, 54, 122, 302)
    hatch_block(b, [(40, b.y0 - 5), (b.x1 + 5, b.y0 - 5), (b.x1 + 5, LIP),
                    (40, LIP)])
    # the press pose of the filmstrip; the left toe stays on a foothold,
    # and the right leg rocks over
    hold_side(b, "foot", (40, 124))
    p = dict(TOP_OUT_PRESS, active=TOP_OUT_PRESS["active"] + ("+rthigh",))
    press_palms(b, p, LIP)
    d = Climber(p.pop("pelvis"), view="side", head=(1, 0),
                lf={"at": (38.6, 126.2), "contact": "toe", "angle": -35}, **p)
    d.draw(b)
    b.arrow([(71, 228), (71, 207)], kind="force")
    b.label("palm presses", (98, 250), size=7.5)
    b.label("on the toe", (86, 166), to=(45, LIP + 1.5))
    warn("top-out-b", d)
    combine([a, b], path, gap=6, labels=["a", "b"],
            captions=["from behind: heel on the lip",
                      "from the side: rock over"])


def traverse(path):
    """Back view: crossing the left hand through, with a back flag."""
    f = Fig(-62, 18, 92, 266)
    wall_grid(f, y0=26)
    A = (-24, 206)      # where the left hand was
    B = (32, 222)       # right hand
    C = (60, 200)       # the left hand crosses over to here
    RF = (32, 38)       # the right foot stays
    for p in (A, B, C):
        hold(f, "jug", p)
    hold(f, "foot", RF)
    hold(f, "foot", (-30, 70))
    # the hips sit under the right hand, so the right arm hangs nearly
    # straight up from its own shoulder to B. As in photographs of back
    # flags, the standing leg's hip (the right) turns in to the wall and
    # the flagging hip comes out toward the viewer. The flagging left leg
    # then passes behind the standing right leg, on the side away from the
    # wall, and the left arm reaches across over the right arm to C, so the
    # library's own drawing order draws both over their right-hand partners.
    # (With the left hip in, the leg would pass between the right leg and
    # the wall, an inside flag.) The chest bends right, toward the crossing
    # reach, the left side stretched
    c = Climber((18, 116), lean=1, bend=6, turn=0.65, lh=grip(C), rh=grip(B),
                lf={"at": (78, 56), "angle": -20, "contact": "ball"},
                rf={"at": stand(RF)},
                elbows={"l": "down", "r": "out"}, knees={"l": "up", "r": "out"},
                head=(-5, -1), allow_cross=True)
    c.draw(f)
    f.arrow([(-20, 216), (22, 252), (55, 218)], kind="move")
    f.label("left hand crosses over", (14, 258), size=7.5)
    f.label("left leg flags behind", (40, 23), to=(70, 52))
    warn("traverse", c)
    f.save(path)


def sit_start(path):
    """Back view on the mat: frog vs hips turned with the outside edge."""
    panels = []
    # start holds high enough that the seated climber reaches them on
    # nearly straight arms, as in photographs of sit starts from behind
    L, R = (-25, 114), (23, 118)
    # both feet on footholds just above the mat, a little lower than the
    # hips that sit on it, so the shoes stand the right way up. Side-on to
    # the wall, both feet lie ahead of the hips, to the left
    LF, RF = (-64, 8), (-28, 12)
    for good in (False, True):
        f = Fig(-75, -6, 75, 150)
        wall_grid(f, y0=10)
        ground(f, 0)
        for p in (L, R):
            hold(f, "jug", p)
        LFa, RFa = (-62, 7), (62, 9)
        for p in ((LF, RF) if good else (LFa, RFa)):
            hold(f, "foot", p)
        if good:
            # right hip turned to the wall, so the climber sits side-on,
            # facing left. The right foot lies ahead of the hips with its toes
            # the same way, on its outside edge against the wall, its knee up
            # and hidden behind the body. It is the leg nearest the wall, so
            # the left leg passes in front of it. The left foot goes on its
            # inside edge further along, ready to push. Both shins point
            # toward the wall, so they are shortened. The hips sit to the
            # right of the hands, so the chest leans over to them, and the
            # arms hang nearly straight
            c = Climber((12, 15), turn=0.8, lean=-10, bend=-8, lh=grip(L), rh=grip(R),
                        lf={"at": stand(LF)},
                        rf={"at": stand(RF), "angle": 180},
                        knees={"l": "up", "r": "up"},
                        leg_len={"l": (0.95, 0.85), "r": (0.8, 0.7)},
                        elbows={"l": "down", "r": "down"}, head=(2, 0), head_tilt=8,
                        allow_cross=True)
            c.draw(f)
            f.label("outside edge", (-72, 58), to=(-30, 15), size=7, anchor="start")
            f.label("right hip turned in", (14, 140), size=7.5)
        else:
            # bottom on the mat, knees up and splayed wide, each foot out
            # below its knee; the shins point at the wall, so they are
            # foreshortened
            c = Climber((0, 14), lh=grip(L), rh=grip(R),
                        lf={"at": stand(LFa)}, rf={"at": stand(RFa)},
                        knees={"l": "up", "r": "up"},
                        leg_len={"l": (1.0, 0.72), "r": (1.0, 0.72)},
                        elbows={"l": "down", "r": "down"})
            c.draw(f)
            f.cross((0, 6))
            f.label("knees splayed, hips square", (0, 140), size=7.5)
        warn("sit-start", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["square on, bottom out", "hips turned, outside edge"])


# ---------------------------------------------------------------- filmstrips

FS = 0.28    # every filmstrip frame uses this scale


def filmstrip_top_out(path):
    """Side view at the lip of a vertical wall: hang, pull and walk the feet
    up, flip a hand to a palm press, press out with a foot on top beside
    the hands, rock over it and stand."""
    W, TOP = 40, 200
    FA, FB, FC = 56, 80, 124            # footholds on the face
    lip = (W + 3, TOP + 1.5)

    def toe(y, angle=-25):
        return {"at": (W - 1.4, y + 2.2), "contact": "toe", "angle": angle}

    def smear(y, angle):
        return {"at": (W - 1.4, y), "contact": "toe", "angle": angle}

    def frame():
        f = Fig(-28, 46, 84, 358, scale=FS)
        hatch_block(f, [(W, f.y0 - 5), (f.x1 + 5, f.y0 - 5), (f.x1 + 5, TOP),
                        (W, TOP)])
        for y in (FA, FB, FC):
            hold_side(f, "foot", (W, y))
        return f

    # the pelvis sits far enough from the face that the knees, which bend
    # toward the wall, stay clear of it
    poses = [
        # 1 hang on straight arms, feet high: the back rounds
        dict(pelvis=(-12, 130), lean=-8, bend=8, lh=lip, rh=lip,
             lf=toe(FA, -30), rf=toe(FB, -35)),
        # 2 pull and walk the feet up until the chest is at the lip, the
        # chest curling toward it
        dict(pelvis=(-9, 164), lean=25, bend=10, lh=lip, rh=lip,
             lf=toe(FB), rf=toe(FC)),
        # 3 right hand flipped to a palm on top, elbow up (the arm turns
        # out of the side-view plane, so the joints are set by hand); the
        # chest curls over the lip
        dict(pelvis=(-11, 202), lean=35, bend=10, lh=lip, rh=(48, TOP + 3),
             lf=toe(FC), rf=smear(146, -40), anatomy=False,
             elbows={"l": "down", "r": "up"},
             knees={"l": "right", "r": "right"}),
        # 4 press out on straight arms, right foot on top beside the hands
        # (TOP_OUT_PRESS); the left leg hangs nearly straight to its
        # foothold, so its knee stays off the lip
        dict(TOP_OUT_PRESS, lf=toe(FC, -35)),
        # 5 rock over the right foot and stand up, the chest still over it
        dict(pelvis=(36, 284), lean=22, bend=8, lf=smear(190, -50),
             rf={"at": (56, TOP + 1), "contact": "ball", "angle": 0},
             active=("+rthigh",)),
    ]
    frames = []
    for i, p in enumerate(poses):
        f = frame()
        if i == 2:
            flat_palm(f, (49, TOP))         # the flipped hand's palm
        elif i == 3:
            press_palms(f, p, TOP)
        c = Climber(p.pop("pelvis"), view="side", head=(1, 0), **p)
        c.draw(f)
        warn(f"filmstrip-top-out {i + 1}", c)
        frames.append(f)
    filmstrip(frames, path, captions=[
        "hang, feet high", "pull, walk\nthe feet up", "flip a palm,\nelbow up",
        "press out,\nfoot on top", "rock over\nand stand"])


def filmstrip_worked_problem(path):
    """Back view: the worked problem of chapter 02 climbed move by move.
    At most three limbs move between frames: the right foot steps up
    while the right hand takes R1, so that from frame 2 to 3 only the
    hands and the left foot move. The last frame shows the slap to R5
    with the left hand still crossed on L4 and its last move to the
    finish as an arrow: with both hands on R5 and F the hands sit either
    side of the head at face height, so the arms would cross on it."""
    def frame(used):
        # cropped to the holds the climber uses, with air around the climber: five
        # frames this wide fit the page only at a smaller scale
        f = Fig(-42, 22, 86, 344, scale=0.245)
        wall_grid(f)
        worked_problem_wall(f, used)
        return f

    S = WP_HANDS["S"][1]
    stand_ = lambda p, a=None: {"at": stand(p), **({} if a is None else {"angle": a})}
    LF0, RF0, LF1, RF1, LF2 = (-30, 34), (24, 28), (-14, 82), (40, 74), (12, 166)
    poses = [
        # 1 low start, both hands on the start jug on straight arms. The
        # arms reach forward and up to the wall past the face, so the head
        # hides them; in the crouch the thighs and shins point toward the
        # wall too, so they are shortened
        dict(pelvis=(7, 65), lh=add(wp_grip("S"), (-6, 0)),
             rh=add(wp_grip("S"), (6, 0)), arm_len={"l": 0.72, "r": 0.72},
             elbows={"l": "out", "r": "out"},
             lf={"at": (-26, 36), "style": "back"},
             rf={"at": stand(RF0), "style": "back"},
             leg_len={"l": (0.6, 0.52), "r": (0.66, 0.56)},
             order=["lleg", "rleg", "torso", "larm", "rarm", "head"],
             used={"S", LF0, RF0}),
        # 2 right hand to the sidepull R1, right foot up: standing up off
        # the start, the hips move right over the high right foot so the
        # start jug sits beside the body, the left hand pressing on it with
        # the elbow out; the body stays left of R1 and leans a little away
        # from it, the left hip turned in. Both holds are near shoulder
        # height, so both arms reach forward to the wall and are shortened;
        # the right elbow hangs below the sidepull. The left foot rolls
        # from its toe on to its inside edge as the climber stands. As in
        # the sidepull of the hold-orientation figure, the body bows away
        # from R1, the chest bending back toward it. The high foot stands
        # on its toe, heel up, which keeps the ankle in its range
        dict(pelvis=(24, 128), lean=-9, bend=6, turn=-0.7, lh=wp_grip("S"),
             rh=wp_grip("R1"), lf=stand_(LF0), rf=stand_(RF1, -24),
             arm_len={"l": 0.7, "r": 0.8}, elbows={"l": "out", "r": "down"},
             used={"S", "R1", LF0, RF1}),
        # 3 left hand to L2, right hand to R3 on a straight arm; left foot
        # up. Resting on R3, the body sags left away from it, the right
        # side stretched
        dict(pelvis=(28, 130), lean=-4, bend=-8, lh=wp_grip("L2"), rh=wp_grip("R3"),
             lf=stand_(LF1), rf=stand_(RF1, -30), used={"L2", "R3", LF1, RF1}),
        # 4 stand up on the high right foot, left hand crosses to L4. R3 is
        # level with the face here, so the left hip starts to turn in
        # (on to frame 5's turn) and the head tips left, clear of R3. The
        # right hand holds R3 beside the face, the arm pointing into the
        # wall and so drawn short, its hand behind the head; the crossing
        # left arm passes between the face and the wall. The high knee goes
        # toward the wall, so that shin is shortened too. The chest bends
        # right, toward the cross, the left side stretched
        dict(pelvis=(36, 178), lean=0, bend=6, turn=-0.5, lh=wp_grip("L4"),
             rh=wp_grip("R3"), lf=stand_(LF1), rf=stand_(WP_HRF),
             allow_cross=True, head=(-10, -4), head_tilt=-30,
             elbows={"l": "up", "r": "down"}, arm_len={"r": 0.45},
             leg_len={"r": (0.7, 0.95)},
             order=["lleg", "rarm", "larm", "torso", "rleg"],
             active=("+rthigh",), used={"L4", "R3", LF1, WP_HRF}),
        # 5 left foot up to LF2, right hand slaps R5: the head sits under
        # R5 between the arms, the right arm reaches up from its own
        # shoulder with the elbow out, and the left arm still crosses in
        # front of the chest to L4 (hidden by the turned torso). The
        # arrow shows the left hand's last move, from L4 to the finish.
        # The slapping side stretches: the chest bends back left
        dict(pelvis=(34, 218), lean=12, bend=-8, turn=-0.6, lh=wp_grip("L4"),
             rh=wp_grip("R5"), lf=stand_(LF2, 200), rf=stand_(WP_HRF),
             allow_cross=True, elbows={"l": "down", "r": "out"},
             used={"R5", "L4", LF2, WP_HRF},
             arrow=[(79, 271), (80, 296), (75, 321)]),
    ]
    frames = []
    for i, p in enumerate(poses):
        f = frame(p.pop("used"))
        if "arrow" in p:
            f.arrow(p.pop("arrow"), kind="move")
        p.setdefault("knees", {"l": "out", "r": "out"})
        p.setdefault("elbows", {"l": "down", "r": "down"})
        c = Climber(p.pop("pelvis"), **p)
        c.draw(f)
        warn(f"filmstrip-worked-problem {i + 1}", c)
        frames.append(f)
    filmstrip(frames, path, captions=[
        "both hands\non the start", "right hand\nto sidepull R1",
        "L2, then\nrest on R3", "high right foot,\ncross to L4",
        "slap R5,\nleft to finish"])


def build(out):
    filmstrip_top_out(out + "/filmstrip-top-out.svg")
    filmstrip_worked_problem(out + "/filmstrip-worked-problem.svg")
    hold_orientation(out + "/reading-hold-orientation.svg")
    reading_problem(out + "/reading-worked-problem.svg")
    wall_angles(out + "/terrain-wall-angles.svg")
    slab(out + "/slab.svg")
    dynamic_slab(out + "/dynamic-slab.svg")
    overhang(out + "/overhang.svg")
    roof(out + "/roof.svg")
    arete(out + "/arete.svg")
    corner(out + "/corner.svg")
    volume_fig(out + "/volume.svg")
    top_out(out + "/top-out.svg")
    traverse(out + "/traverse.svg")
    sit_start(out + "/sit-start.svg")
