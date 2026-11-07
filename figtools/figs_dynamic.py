"""Figures for the dynamic movement chapter (06-dynamic)."""

import copy
import math
import os

from climb import *
import plan


def _inner(a, b, c):
    """Interior angle at b (degrees)."""
    v1, v2 = norm(sub(a, b)), norm(sub(c, b))
    return math.degrees(math.acos(max(-1, min(1, dot(v1, v2)))))


def _ankle(c, s):
    ft = getattr(c, "_" + s + "f")
    shin_up = norm(sub(c.J[s + "kn"], c.J[s + "an"]))
    return math.degrees(math.acos(max(-1, min(1, dot(shin_up, ft["d"]))))), ft


def _warn(name, *climbers):
    """Climber.warn(), plus the ankle range for profile feet in back views
    (warn() checks ankles in side views only). DYN_ANGLES=1 prints every
    joint angle."""
    for c in climbers:
        for w in c.warn():
            print(f"{name}: {w}")
        for s in "lr":
            a, ft = _ankle(c, s)
            if (c.view == "back" and ft["style"] != "back"
                    and ft["contact"] != "heel" and not 45 <= a <= 160):
                print(f"{name}: {s} ankle {a:.0f} deg in back view")
        if os.environ.get("DYN_ANGLES"):
            J = c.J
            parts = []
            for s in "lr":
                parts.append(f"{s} elbow {_inner(J[s + 'sh'], J[s + 'el'], J[s + 'ha']):.0f}"
                             f" knee {_inner(J[s + 'hip'], J[s + 'kn'], J[s + 'an']):.0f}"
                             f" ankle {_ankle(c, s)[0]:.0f}")
            print(f"  {name}: " + " | ".join(parts))


def _side_grip(pos, angle, out=4.5, up=3.0):
    """Where the hand sits on a side-view jug on a wall overhanging by
    `angle` degrees: in the cup, a little out from the wall."""
    d = norm((-math.tan(math.radians(angle)), 1))
    n = (-d[1], d[0])
    return add(pos, add(mul(n, out), mul(d, up)))


def _side_foot(pos, angle, out=2.5, up=1.6):
    """Toe contact on top of a side-view foothold."""
    return _side_grip(pos, angle, out, up)


def _toward(pelvis, targets, **kw):
    """A climber whose hands stretch as far as they can toward `targets`
    ({"l": point, "r": point}): a throw still in flight, or arms swinging.
    The hands land within reach, so warn() stays quiet."""
    c = Climber(pelvis, **kw, **{s + "h": p for s, p in targets.items()})
    return Climber(pelvis, **kw, **{s + "h": c.J[s + "ha"] for s in targets})


def _ghost_limbs(f, c, parts, z=0, on=None):
    """Draw only `parts` of climber `c` (e.g. ("lleg", "rleg")) as a ghost:
    the limbs that moved. A whole ghost body drawn close to the climber
    merges with it into one double body. With `on` (a climber), the ghost
    limbs hang from that climber's hips and shoulders instead of c's, so
    they join the body that is drawn solid; hands, feet and the way the
    joints bend come from c. Returns the ghost, for warn()."""
    g = copy.copy(on if on is not None else c)
    if on is not None:
        for k in ("lh", "rh", "lf", "rf", "elbows", "knees", "arm_len", "leg_len"):
            setattr(g, k, getattr(c, k))
        g.solve()
    g.order = list(parts)
    g.draw(f, ghost=True, z=z)
    return g


def _axis_turn(f, c, rx=30, ry=9, a0=-80, a1=55, z=60):
    """Rotation about a vertical axis through `c` (back view), drawn as an
    arc of a flattened ellipse; the lower half is the side nearer the
    viewer. Returns the arc's points."""
    n = 14
    pts = [add(c, (rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                   ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))))
           for i in range(n + 1)]
    f.arrow(pts, kind="turn", z=z)
    return pts


# ---------------------------------------------------------------- deadpoint


def deadpoint(path):
    """Side view, 20 degree overhang. (a) Load: arms straight, hips out and
    low. (b) Drive: the push leg straightens, the hips go in and up, and
    the right hand grabs the high hold at the top of the rise."""
    A = 20
    x0 = 70
    t = math.tan(math.radians(A))
    LO = (x0 - t * (190 - 40), 190)
    HI = (x0 - t * (250 - 40), 250)
    FT = (x0 - t * (66 - 40), 66)
    lo = _side_grip(LO, A)
    hi = _side_grip(HI, A)
    foot = _side_foot(FT, A)
    # the back rounds a little as the hips sag out
    load = Climber(None, shoulders=add(lo, (-34, -54)), view="side", lean=6,
                   lh=lo, rh=add(lo, (0.4, -0.6)),
                   lf={"at": add(foot, (-1, -0.5)), "contact": "toe"},
                   rf={"at": foot, "contact": "edge"}, bend=8)
    # the push leg drives; the holding arm bends only to let the body pass,
    # and at the top of the rise the body weighs almost nothing; the back
    # arches to bring the hips to the wall
    top = Climber(None, shoulders=add(hi, (-6, -60)), view="side", lean=-20,
                  lh=lo, rh=hi,
                  lf={"at": add(foot, (-1, -0.5)), "contact": "toe"},
                  rf={"at": foot, "contact": "edge"}, bend=-10, active=("rthigh",))
    panels = []
    for k in range(2):
        # room on the left, so the labels sit left of the hand and the hips; narrow
        # enough to sit beside the steps
        f = Fig(-61, 40, 74, 270)
        wall_side(f, x0, 40, 262, angle=A)
        hold_side(f, "jug", LO, angle=A)
        hold_side(f, "jug", HI, angle=A)
        hold_side(f, "foot", FT, angle=A)
        if k == 0:
            load.draw(f)
            f.label("arms straight", (-58, 238), to=lerp(load.J["rsh"], lo, 0.72), anchor="start")
            f.label("hips sag out", (-58, 70), to=add(load.pelvis, (-10, -6)), anchor="start")
            _warn("deadpoint a", load)
        else:
            load.draw(f, ghost=True)
            top.draw(f, z=5)
            f.body_arrow([add(load.pelvis, (-4, -16)), add(load.pelvis, (14, -18)),
                          add(top.pelvis, (6, -18))])
            f.label("grab at", (-22, 240), to=add(hi, (-4, 1)), anchor="end")
            f.text("the top", (-22, 240 - f.pt(9.5)), anchor="end")
            f.label("hips in and up", (-58, 56), anchor="start")
            _warn("deadpoint b", top)
        panels.append(f)
    combine(panels, path, gap=4.5, labels=["a", "b"],
            captions=["load: hips out", "drive in, grab at the top"])


# ---------------------------------------------------------------- hip pump


def hip_pump(path):
    """Back view, two frames. (a) The hips start over the left foot (ghost),
    swing across and dip over the right push foot, under the target.
    (b) They rise out of the dip in one arc and the right hand reaches for
    the next hold at the top of it. Arms stay straight in the dip."""
    LH, RH = (-4, 246), (32, 246)
    LF, RF = (-46, 66), (40, 74)
    T = (52, 292)
    # the hips swing out to each side while the chest stays under the
    # hands, so the waist bends against the swing
    start = Climber((-18, 152), lean=-4, lh=grip(LH), rh=grip(RH),
                    lf={"at": stand(LF)}, rf={"at": stand(RF), "style": "back"},
                    knees={"l": "out", "r": "down"}, bend=8)
    dip = Climber((18, 139), lean=4, lh=grip(LH), rh=grip(RH),
                  lf={"at": stand(LF)}, rf={"at": stand(RF), "style": "back"},
                  knees={"l": "out", "r": "out"}, bend=-6)
    # the push leg lifts the hips, so the arms don't have to; the reaching
    # side stretches
    rise = _toward((12, 164), {"r": grip(T)}, lean=12, lh=grip(LH),
                     lf={"at": stand(LF), "contact": "toe", "angle": 215}, rf={"at": stand(RF), "style": "back"},
                     elbows={"l": "down"}, knees={"l": "down", "r": "out"},
                     bend=-8, active=("rthigh",))
    panels = []
    for k, (g, c) in enumerate([(start, dip), (dip, rise)]):
        f = Fig(-88, 44, 82, 300)
        wall_grid(f)
        for p in (LH, RH, T):
            hold(f, "jug", p)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        # (b) has no ghost: the dip is (a)'s climber, next to it, and
        # ghost legs there only doubled the solid legs
        if k == 0:
            g.draw(f, ghost=True)
        c.draw(f, z=5)
        if k == 0:
            # under the crotch, between the legs: the hips dip as they cross
            f.body_arrow([(-14, 112), (6, 98), (26, 108)])
            f.label("push foot", (62, 52), to=add(stand(RF), (4, -2)))
            f.label("arms straight", (-56, 280), to=lerp(c.J["lsh"], c.J["lha"], 0.6))
        else:
            # the hips rise out of the dip: up through the open space
            # between the legs, from the dip's height to under the seat
            f.body_arrow([(28, 92), (25, 114), (17, 138)])
            f.arrow([add(c.J["rha"], (6, -2)), add(grip(T), (4, -5))], kind="move")
        _warn(f"hip-pump {'ab'[k]}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["dip onto the push foot", "rise in one arc"])


# ---------------------------------------------------------------- dyno


def dyno(path):
    """Side view of a gently overhanging wall (10 degrees), three frames.
    (a) Sink: arms straight, hips low and out. (b) Drive: the legs
    straighten and the hips swing in and up around the hands, which let
    go late. (c) Catch: feet off, the right hand latches the jug at the top
    of the flight. Blank wall between the start holds and the target."""
    A = 10
    x0 = 52
    t = math.tan(math.radians(A))

    def W(h):
        return (x0 - t * (h - 60), h)
    S, T, F = W(170), W(306), W(70)
    s, tg, ft = _side_grip(S, A), _side_grip(T, A), _side_foot(F, A)
    sink = Climber(None, shoulders=add(s, (-48, -43)), view="side", lean=24,
                   lh=s, rh=add(s, (0.4, -0.6)),
                   lf={"at": add(ft, (-1, -0.5)), "contact": "toe"},
                   rf={"at": ft, "contact": "toe"}, head=(1, 1),
                   # the back rounds a little in the crouch; the head tips
                   # back to look up at the target, as in video of the sink
                   bend=8, head_tilt=-25)
    # arched: hips in, shoulders back, arms nearly straight; the legs are
    # nearly straight too, so the knees stay off the wall
    drive = Climber(None, shoulders=add(s, (-58, 24.5)), view="side", lean=-35,
                    lh=s, rh=add(s, (0.4, -0.6)),
                    lf={"at": add(ft, (-1, -0.5)), "contact": "toe"},
                    rf={"at": ft, "contact": "toe"}, head=(3, 0), bend=-14,
                    active=("lthigh", "rthigh", "lcalf", "rcalf"))
    catch = Climber(None, shoulders=add(tg, (-13, -56)), view="side", lean=-6,
                    lh=add(tg, (0.4, -0.6)), rh=tg,
                    lf={"at": (4, 108), "contact": "toe", "angle": 292},
                    rf={"at": (8, 106), "contact": "toe", "angle": 294})
    panels = []
    for k, (g, c) in enumerate([(None, sink), (sink, drive), (drive, catch)]):
        f = Fig(-80, 50, 60, 322)
        wall_side(f, x0, 50, 322, angle=A)
        for p in (S, T):
            hold_side(f, "jug", p, angle=A)
        hold_side(f, "foot", F, angle=A)
        if g:
            g.draw(f, ghost=True)
        c.draw(f, z=5)
        if k == 0:
            f.label("arms straight", (-44, 214), to=lerp(c.J["rsh"], s, 0.6))
            f.label("hips low", (-52, 60), to=add(c.pelvis, (-9, -6)))
            f.label("big jug", (-34, 300), to=add(T, (-6, 0)))
            f.label("blank wall", (-34, 250), to=W(250))
        elif k == 1:
            f.body_arrow([add(g.pelvis, (-14, -8)), add(g.pelvis, (-22, 28)),
                          add(c.pelvis, (-26, -8))])
            f.label("let go late", (-14, 252), to=add(s, (-3, 2)))
            f.label("legs drive", (14, 58))
        else:
            f.body_arrow([add(g.pelvis, (-30, -16)), add(c.pelvis, (-28, -2))])
            f.arrow([add(s, (-6, 10)), add(lerp(s, tg, 0.5), (4, 0)), add(tg, (-2, -8))],
                    kind="move")
            f.label("feet off", (-46, 84), to=add(c.J["ran"], (-2, -8)))
        _warn(f"dyno {k}", c)
        panels.append(f)
    combine(panels, path, gap=5, labels=["a", "b", "c"],
            captions=["sink", "drive with the legs", "catch at the top"])


# ---------------------------------------------------------------- double dyno


def double_dyno(path):
    """Back view, two narrow frames on the same wall. (a) Sink on two start
    holds: arms straight, knees bent, toes pointed at the wall; the pair of
    targets sits above a blank stretch of wall. (b) Both hands leave
    together and catch the pair with slightly bent arms, feet off; two
    parallel hand paths."""
    LH, RH = (-20, 192), (20, 192)
    A, B = (-22, 294), (22, 294)
    LF, RF = (-30, 20), (30, 28)
    sink = Climber((0, 85), lh=grip(LH), rh=grip(RH),
                   lf={"at": stand(LF), "style": "back"},
                   rf={"at": stand(RF), "style": "back"},
                   knees={"l": "out", "r": "out"})
    # slightly bent arms catch and check the swing
    catch = Climber((0, 190), lh=grip(A), rh=grip(B),
                    lf={"at": (-14, 102), "style": "back"},
                    rf={"at": (14, 100), "style": "back"},
                    elbows={"l": "out", "r": "out"}, knees={"l": "out", "r": "out"},
                    active=("lupper", "lfore", "rupper", "rfore"))
    panels = []
    for k, c in enumerate((sink, catch)):
        f = Fig(-59, 10, 59, 304)
        wall_grid(f)
        for p in (LH, RH, A, B):
            hold(f, "jug", p)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        c.draw(f)
        if k == 0:
            f.label("pair of holds", (0, 278))
        else:
            for sg, p, q in ((-1, LH, A), (1, RH, B)):
                f.arrow([add(grip(p), (sg * 10, 6)), add(lerp(p, q, 0.45), (sg * 28, 0)),
                         add(grip(q), (sg * 9, -6))], kind="move")
            f.body_arrow([(-40, 70), (-40, 160)])
        _warn(f"double-dyno {'ab'[k]}", c)
        panels.append(f)
    combine(panels, path, gap=4, labels=["a", "b"],
            captions=["sink, arms straight", "both hands catch"])


# ---------------------------------------------------------------- cutting loose


def cutting_loose(path):
    """Side view on a 35 degree overhang. (a) The feet cut and the legs
    swing out. (b) At the outward peak the knees snap toward the wall.
    (c) On the swing back in, the toes catch the foothold. Each frame
    shows the previous position of the legs as a ghost, hung from the
    solid hips (the hands stay put, so a whole ghost body would sit on the
    climber)."""
    A = 35
    x0 = 150
    t = math.tan(math.radians(A))
    H = (x0 - t * (245 - 30), 245)
    F = (x0 - t * (140 - 30), 140)
    hand = _side_grip(H, A)
    foot = _side_foot(F, A)

    def hang(shoulders, lean, lf, rf, active=None, bend=0):
        return Climber(None, shoulders=add(hand, shoulders), view="side",
                       lean=lean, lh=hand, rh=add(hand, (0.4, -0.6)), lf=lf, rf=rf,
                       active=active, bend=bend)

    on = hang((-6, -50), -12, {"at": add(foot, (-1, -1)), "contact": "toe"},
              {"at": foot, "contact": "toe"})
    # the legs travel out freely and the back arches; the stomach snaps them
    # back at the peak, curling the back, and tenses again as the toes touch
    out = hang((-10, -54), 14, {"at": (-70, 50), "contact": "toe", "angle": 288},
               {"at": (-64, 47), "contact": "toe", "angle": 292}, bend=-10)
    tuck = hang((-10, -54), 12, {"at": (-2, 84), "contact": "toe", "angle": 302},
                {"at": (0, 83), "contact": "toe", "angle": 302}, active=("+core",),
                bend=10)
    back = hang((-6, -50), -10, {"at": add(foot, (-1, -1)), "contact": "toe"},
                {"at": foot, "contact": "toe"}, active=("+core",), bend=6)
    panels = []
    for k, (g, c) in enumerate([(on, out), (out, tuck), (tuck, back)]):
        f = Fig(-82, 40, 84, 268)
        wall_side(f, x0, 30, 268, angle=A)
        hold_side(f, "jug", H, angle=A)
        hold_side(f, "foot", F, angle=A)
        # the hands stay put and the legs swing: ghost the legs only
        legs = _ghost_limbs(f, g, ("lleg", "rleg"), on=c)
        c.draw(f, z=5)
        if k == 0:
            f.arrow([add(foot, (-4, -10)), (10, 62), (-56, 44)], kind="move")
            f.label("feet cut", (70, 100))       # right of the arrow
        elif k == 1:
            f.arrow([add(g.J["rkn"], (8, 0)), lerp(g.J["rkn"], c.J["rkn"], 0.5),
                     add(c.J["rkn"], (-4, -2))], kind="move")
            f.label("knees snap in", (40, 80))
        else:
            f.arrow([add(g.J["ran"], (6, -16)), (30, 96), add(foot, (-8, -8))],
                    kind="move")
            # below the arrow, clear of the ghost legs
            f.label("toes catch", (62, 88), to=add(foot, (2, -2)))
        _warn(f"cutting-loose {k}", c, legs)
        panels.append(f)
    combine(panels, path, gap=4, labels=["a", "b", "c"],
            captions=["feet cut, legs swing out", "at the peak, tuck", "swing in, toes on"])


# ---------------------------------------------------------------- one-handed dyno


def lunge(path):
    """Back view, two frames. (a) Sink: left hand on the jug with a straight
    arm, right arm swung low and back, eyes on the target. (b) Throw: the
    left leg drives, the right hip turns in, the right arm goes long to the
    single jug up and right; the left hand stays on."""
    LH = (-34, 200)
    LF, RF = (-48, 32), (40, 40)
    T = (54, 226)
    # hanging off the straight left arm: the left side stretches and the
    # hips sag away from the hold
    sink = Climber((-8, 93), lean=-2, lh=grip(LH), rh=(33, 83),
                   arm_len={"r": 0.92},
                   lf={"at": stand(LF)}, rf={"at": stand(RF)},
                   elbows={"r": "out"}, knees={"l": "out", "r": "out"},
                   head=(3, 1), bend=8)
    # the throwing side stretches and lifts the right shoulder
    throw = Climber((18, 124), turn=0.7, lean=19, lh=grip(LH), rh=grip(T),
                    lf={"at": stand(LF), "contact": "toe", "angle": 210},
                    rf={"at": (42, 52), "contact": "toe", "angle": 266},
                    head=(3, 0), bend=-8,
                    elbows={"l": "down"}, knees={"l": "out", "r": "down"},
                    active=("+lthigh",))      # the left leg drives
    panels = []
    for k in range(2):
        # no more wall than the climber needs, so the figure stays under the steps
        f = Fig(-80, 22, 104, 238)
        wall_grid(f)
        hold(f, "jug", LH)
        hold(f, "jug", T)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        if k == 0:
            sink.draw(f)
            f.label("eyes on target", (2, 226), to=add(T, (-9, 0)))
            f.label("arm low", (70, 132), to=sink.J["rha"])
            _warn("lunge a", sink)
        else:
            sink.draw(f, ghost=True)
            throw.draw(f, z=5)
            f.arrow([add(sink.J["rha"], (8, 4)), (80, 170), add(grip(T), (7, -5))],
                    kind="move")
            arc = _axis_turn(f, add(throw.pelvis, (2, -4)), rx=32, ry=10, a0=-120, a1=50)
            f.label("hip", (74, 124), to=arc[6], anchor="start")
            f.text("turns in", (74, 124 - f.pt(9.5)), anchor="start")
            f.label("left hand stays", (-62, 221), to=grip(LH), anchor="start")
            _warn("lunge b", throw)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["sink, eyes on target", "hip in, throw long"])


# ---------------------------------------------------------------- counter-kick


def counter_kick(path):
    """Back view, two frames. (a) The right hand has just caught a sidepull
    up and right; the left hand and left foot are off, and the body swings
    open to the left about the line through the right hand and right foot.
    (b) The left leg kicks across behind the right leg, straight and close
    to the wall, and squares the body back to the wall. A back view can't
    show which way the body turns, so each frame has a "from above" inset
    of the body as a door on that hinge: swinging open in (a), back to the
    wall in (b)."""
    R = (40, 238)
    RF = (30, 64)
    rh = grip(R, use=0)
    # hanging off the right arm: the right side stretches
    opened = Climber((4, 146), turn=0.5, lean=-5, lh=(-70, 176), rh=rh,
                     lf={"at": (-56, 72), "contact": "toe", "angle": 240},
                     rf={"at": stand(RF), "style": "back"}, elbows={"l": "down"},
                     knees={"l": "out", "r": "down"}, bend=-6,
                     active=("-lupper", "-lfore"))      # the left hand is off
    # the stomach tenses as the kick stops the swing; the chest leans left
    # against the leg kicked right. The left foot ends in a back flag: below the
    # right foot, its edge pressed on the wall, on no hold (as in Barn door b)
    kicked = Climber((14, 146), lean=8, lh=None, rh=rh,
                     lf={"at": (62, 57), "contact": "edge", "angle": -20},
                     rf={"at": stand(RF), "style": "back"}, elbows={"l": "down"},
                     knees={"l": "down", "r": "down"}, allow_cross=True, bend=-8,
                     # behind the standing leg = nearer the viewer
                     order=["rleg", "torso", "lleg", "larm", "rarm"],
                     active=("+core",))
    panels = []
    for k in range(2):
        # room at the top for the view from above
        f = Fig(-84, 40, 96, 280)
        wall_grid(f)
        hold(f, "jug", R, use=0)
        hold(f, "foot", RF)
        if k == 0:
            opened.draw(f)
            f.line(add(rh, (4, 14)), add(stand(RF), (6, -18)), sw=0.45,
                   dash=(2.2, 1.2), z=60)
            f.label("hinge", (76, 250), to=add(rh, (4, 10)))
            # the left arm flung out, level with the shoulders (the left leg would
            # lie under it)
            plan.from_back(f, opened, (-6, 272), "r", s=0.56, span=(12, 116),
                           label_at=(-44, -36))
            _warn("counter-kick a", opened)
        else:
            # only the kicking leg as a ghost: the hips barely move
            _ghost_limbs(f, opened, ("lleg",))
            kicked.draw(f, z=5)
            f.arrow([add(opened.J["lan"], (-2, -14)), (12, 58), add(kicked.J["lan"], (12, -10))],
                    kind="move")
            # under the kick's path, in the clear
            f.label("kick across behind", (-8, 45), to=(-4, 60), anchor="middle")
            # square to the wall again: the left arm hangs, and the left leg
            # crosses under the body to press the wall right of the right foot
            # back square to the wall: the left arm hangs out of sight, and the left
            # leg crosses under the body to press the wall right of the right foot
            plan.from_back(f, kicked, (-6, 272), "r", s=0.56, feet={"l": 0}, swing="back",
                           span=(46, 56), label_at=(-44, -36))
            _warn("counter-kick b", kicked)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["swings open", "kick across stops it"])


# ---------------------------------------------------------------- hip pop


def hip_pop(path):
    """Back view, two frames. (a) Left hand on a sidepull, right foot on its
    outside edge in a partial drop knee, left leg flagged, hips sagging back
    from the wall, right arm hanging ready. (b) The right hip snaps into the wall and up, and the
    right hand throws to the hold up and right. The foot is drawn as in the
    drop knee: on its outside edge, heel up, toes into the wall (pointing
    down). The knee turns in but stays level with the foot, since step 1 warns
    against snapping off a deep drop."""
    L = (-49, 223)
    T = (38, 250)
    RF = (62, 62)
    back = {"at": stand(RF), "angle": 268}
    # hanging off the straight left arm, the left side stretches and the
    # hips sag away from the hold
    sag = Climber((-12, 116), turn=0.55, lean=-6, lh=grip(L, use=180), rh=None,
                  lf={"at": (-54, 46), "contact": "toe", "angle": 250},
                  rf=back, elbows={"l": "down"}, knees={"r": "left"},
                  leg_len={"l": 0.95}, bend=8, tuck=("r",))
    # the drop-knee leg pushes and the right hip snaps into the wall; as in
    # a deadpoint, the holding arm bends only to let the body pass. The
    # throwing side stretches.
    pop = _toward((1, 142), {"r": grip(T)}, turn=0.85, lean=14, lh=grip(L, use=180),
                    lf={"at": (-34, 50), "contact": "toe", "angle": 236},
                    rf=back, knees={"r": "left"}, elbows={"l": "down"},
                    leg_len={"l": 0.95, "r": (0.95, 1.0)}, bend=-18,
                    active=("rthigh", "rglute"))
    panels = []
    for k in range(2):
        f = Fig(-84, 24, 84, 268)
        wall_grid(f)
        hold(f, "jug", L, use=180)
        hold(f, "jug", T)
        hold(f, "foot", RF)
        if k == 0:
            sag.draw(f)
            f.label("partial drop knee", (7, 50), to=add(sag.J["rkn"], (2, -3)), anchor="start")
            f.label("arm straight", (-16, 209), to=lerp(sag.J["lel"], sag.J["lwr"], 0.3))
            f.label("hips sag", (-43, 152), to=add(sag.pelvis, (-8, 2)))
            _warn("hip-pop a", sag)
        else:
            sag.draw(f, ghost=True)
            pop.draw(f, z=5)
            arc = _axis_turn(f, add(pop.pelvis, (0, -2)), rx=30, ry=9, a0=-120, a1=50)
            # between the legs, clear of the limbs: the hips rise
            f.body_arrow([(-14, 72), (-11, 114)])
            f.arrow([add(sag.J["rha"], (8, 0)), (70, 200), add(pop.J["rha"], (8, -4))],
                    kind="move")
            f.label("hip snaps in", (36, 50), to=arc[-4])
            _warn("hip-pop b", pop)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["sit back on the drop knee", "pop the hip, throw"])


# ---------------------------------------------------------------- latching


def _jug_profile(fig, top):
    """A positive jug in profile on a wall to the right of `top`."""
    x, y = top
    pts = [(x + 6.5, y - 4.5), (x + 1.5, y - 4.2), (x + 0.1, y - 2.0),
           (x - 0.2, y + 0.2), (x + 0.25, y + 0.6), (x + 0.9, y - 1.3),
           (x + 2.6, y - 1.6), (x + 6.5, y - 0.6)]
    fig.smooth(pts, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    if XRAY:     # dotted where the hand covers it
        fig.smooth(pts, z=XRAY_Z, tension=0.5, **XRAY_STYLE)


def latching(path):
    """(a) Close-up, side view: the open hand arrives with the fingertips
    2-3 cm above the jug. (b) The fingers drop over the lip. (c) Back view:
    the right hand has caught with a slightly bent arm, the shoulder pulled
    down and both feet pressing on their holds."""
    import authored as A
    # the close-ups use the book's hands (authored.py) at their fixed scale
    a = A.latch_a(_jug_profile)
    b = A.latch_b(_jug_profile)

    # (c) body, back view: arm slightly bent, shoulder set, feet press down
    T = (26, 236)
    LO = (-40, 132)
    LF, RF = (-30, 56), (32, 68)
    c_ = Fig(-70, 30, 94, 262)        # room right of the body for a label
    wall_grid(c_)
    hold(c_, "jug", T)
    hold(c_, "jug", LO)
    hold(c_, "foot", LF)
    hold(c_, "foot", RF)
    # the catching arm, and the lat pulling its shoulder down, which bends
    # the right side a little; the low hand only steadies
    c = Climber((0, 137), lean=0, lh=grip(LO), rh=grip(T),
                lf={"at": stand(LF)}, rf={"at": stand(RF)},
                elbows={"l": "down", "r": "out"}, knees={"l": "out", "r": "out"},
                bend=6, active=("rupper", "rfore", "rlat"))
    c.draw(c_)
    c_.arrow([add(stand(LF), (0, 14)), add(stand(LF), (0, 3))], kind="force")
    c_.arrow([add(stand(RF), (0, 14)), add(stand(RF), (0, 3))], kind="force")
    c_.arrow([add(c.J["rsh"], (12, 16)), add(c.J["rsh"], (12, 4))], kind="force")
    c_.label("arm slightly bent", (52, 252), to=c.J["rel"])
    c_.label("shoulder down", (30, 162), to=add(c.J["rsh"], (12, 8)), anchor="start")
    c_.label("feet press down", (0, 40))
    _warn("latching", c)
    combine([a, b, c_], path, gap=5, labels=["a", "b", "c"],
            captions=["aim above", "drop on", "bent arm, feet press"])


# ---------------------------------------------------------------- jump start


def jump_start(path):
    """Side view with the floor: a quarter squat with the arms back, then a
    jump straight up; catch with bent arms, then the feet go on."""
    S = (40, 242)            # start jug, out of reach from the floor
    FH = (40, 100)           # the marked foothold
    hand = add(S, (-3.5, 2))
    # in the crouch the back rounds a little over the knees
    crouch = Climber((-16, 86), view="side", lean=29,
                     lh=(-48, 100), rh=(-45, 97),
                     lf={"at": (2, 0.3), "contact": "ball", "angle": 0},
                     rf={"at": (5, 0.3), "contact": "ball", "angle": 0},
                     head=(2, 1), bend=6)
    catch = Climber(None, shoulders=add(hand, (-25, -50)), view="side", lean=-2,
                    lh=hand, rh=add(hand, (0.5, -0.5)),
                    lf={"at": (15, 40), "contact": "toe", "angle": -66},
                    rf={"at": (19, 44), "contact": "toe", "angle": -62})
    panels = []
    for k in range(2):
        f = Fig(-62, -10, 50, 262)
        ground(f, 0)
        wall_side(f, 40, 0, 262, angle=0)
        hold_side(f, "jug", S)
        hold_side(f, "foot", FH)
        if k == 0:
            crouch.draw(f)
            f.label("arms back", (-38, 150), to=add(crouch.J["lel"], (-1, 2)))
            f.label("quarter squat", (-29, 46), to=crouch.J["lkn"], anchor="middle")
            f.label("out of reach", (-18, 242), to=add(S, (-5, 0)))
            _warn("jump-start a", crouch)
        else:
            catch.draw(f)
            f.body_arrow([(-30, 80), (-30, 170)])
            f.label("straight up", (-30, 186))
            f.arrow([add(catch.J["ran"], (6, -6)), add(FH, (-8, -10)), add(FH, (-6, 2))],
                    kind="move")
            f.label("arms bent", (-20, 240), to=lerp(catch.J["rel"], catch.J["rha"], 0.35))
            f.label("then feet on", (-28, 60))
            _warn("jump-start b", catch)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["crouch, arms back", "catch, then feet on"])


# ---------------------------------------------------------------- run and jump


def run_and_jump(path):
    """Side view of the mat and a vertical wall, one continuous scene. Ghost
    1: the last running step (steps 1-3 on the mat). Ghost 2: the right
    foot on the volume, pushing up and along the wall. Solid: the catch at
    the top of the flight, feet straight back on the volume."""
    f = Fig(-120, -14, 113, 274)
    ground(f, 0)
    wall_side(f, 102, 0, 274, angle=0)
    J = (102, 258)
    hold_side(f, "jug", J)
    volume_side(f, (102, 54), 36, 36, top=1.0)
    top = (72, 90)                       # the push spot on the volume
    hand = _side_grip(J, 0)
    run = _toward((-58, 96), {"l": (-20, 136), "r": (-96, 112)}, view="side",
                  lean=12, lf={"at": (-50, 0.3), "contact": "ball", "angle": 0},
                  rf={"at": (-20, 42), "contact": "toe", "angle": -60})
    # the body stretches out of the push and curls a little as the feet
    # land back on the volume
    push = _toward((30, 124), {"l": (90, 250), "r": (96, 254)}, view="side",
                   lean=28, lf={"at": (-4, 44), "contact": "toe", "angle": -70},
                   rf={"at": top, "contact": "ball", "angle": 0}, bend=-6)
    catch = Climber(None, shoulders=add(hand, (-26, -50)), view="side", lean=10,
                    lh=add(hand, (0.4, -0.6)), rh=hand,
                    lf={"at": (94, 90.5), "contact": "ball"},
                    rf={"at": (92, 90.5), "contact": "ball"}, bend=6)
    run.draw(f, ghost=True)
    push.draw(f, ghost=True, z=2)
    catch.draw(f, z=5)
    for i, x in enumerate((-110, -80, -50)):
        f.step(i + 1, (x, 9))
    f.step(4, (50, 92))
    f.body_arrow([add(run.pelvis, (0, -10)), add(push.pelvis, (-10, -16)),
                  add(catch.pelvis, (-26, -2))])
    f.arrow([(56, 104), (64, 128)], kind="force")
    f.label("push up and along", (50, 26), to=add(top, (-8, 1)))
    _warn("run-and-jump", run, push, catch)
    f.save(path)


# ---------------------------------------------------------------- pogo


def pogo(path):
    """Back view, two frames. (a) Arms straight, hips sunk, the free right
    leg swung back across behind the left. (b) The right leg swings forward
    and up nearly straight, the left foot pushes off the single low
    foothold, and the right hand goes for the jug up and right."""
    LH, RH = (-40, 216), (37, 215)
    LF = (-22, 50)
    T = (58, 266)
    # the free right leg swings between the standing leg and the wall, so
    # it is drawn first, behind the left leg
    # the chest leans right against the leg swung left
    back = Climber((-4, 112), lean=-5, lh=grip(LH), rh=grip(RH),
                   lf={"at": stand(LF), "contact": "toe", "angle": 235},
                   rf={"at": (-58, 46), "contact": "toe", "angle": 228},
                   knees={"l": "out", "r": "left"}, allow_cross=True, bend=6,
                   order=["rleg", "lleg", "torso", "larm", "rarm"],
                   active=())          # hanging on straight arms
    # the left foot pushes off while the left arm pulls; the chest leans
    # left against the leg swung right, and the reaching side stretches
    swing = _toward((16, 154), {"r": grip(T)}, lean=8, bend=-8, lh=grip(LH),
                      lf={"at": stand(LF), "contact": "toe", "angle": 235},
                      # the swinging foot leads with the heel, toes up
                      rf={"at": (117, 152), "contact": "heel", "angle": 55},
                      elbows={"l": "down"}, knees={"l": "out", "r": "up"},
                      active=("+lthigh",))
    panels = []
    for k in range(2):
        # no more wall than the climber needs, so the figure stays under the steps
        f = Fig(-90, 38, 134, 274)
        wall_grid(f)
        for p in (LH, RH, T):
            hold(f, "jug", p)
        hold(f, "foot", LF)
        if k == 0:
            back.draw(f)
            f.label("arms straight", (-56, 256), to=lerp(back.J["lsh"], back.J["lha"], 0.5))
            f.label("right leg back", (40, 48), to=add(back.J["ran"], (6, -6)))
            _warn("pogo a", back)
        else:
            back.draw(f, ghost=True)
            swing.draw(f, z=5)
            f.arrow([add(back.J["ran"], (-8, -4)), (-10, 44), (90, 70),
                     add(swing.J["ran"], (10, -10))], kind="move")
            f.arrow([add(stand(LF), (-12, 20)), add(stand(LF), (-12, 4))], kind="force")
            f.arrow([add(swing.J["rha"], (6, -2)), add(grip(T), (5, -5))], kind="move")
            # (between the standing leg and the swing's arc, clear of both)
            f.label("leg nearly straight", (90, 120), to=lerp(swing.J["rkn"], swing.J["ran"], 0.4), anchor="end")
            # right of the standing leg, clear of it and the ghost
            f.label("left foot pushes", (2, 92), to=add(stand(LF), (6, 6)))
            _warn("pogo b", swing)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["sink, leg swings back", "swing up, foot pushes"])


# ---------------------------------------------------------------- campus move


def campus_move(path):
    """Side view under a 50 degree overhang with no footholds. (a) Hang on
    the jug, arms slightly bent, knees tucked. (b) A small pop of the hips
    up toward the wall; the right hand moves on to the next jug, 50 cm
    farther along, and catches with a bent arm."""
    A = 50
    x0 = 176
    t = math.tan(math.radians(A))

    def W(h):
        return (x0 - t * (h - 120), h)
    d = norm((-t, 1))
    H1 = W(232)
    H2 = add(H1, mul(d, 50))
    h1, h2 = _side_grip(H1, A), _side_grip(H2, A)

    def tucked(shoulders, lean, lh, rh, bend=0):
        c0 = Climber(None, shoulders=shoulders, view="side", lean=lean, lh=lh, rh=rh,
                     bend=bend)
        P = c0.pelvis
        # footless: the arms and body tension hold the tucked legs still
        return Climber(None, shoulders=shoulders, view="side", lean=lean, lh=lh, rh=rh,
                       lf={"at": add(P, (32, -52)), "contact": "toe", "angle": -44},
                       rf={"at": add(P, (36, -54)), "contact": "toe", "angle": -44},
                       bend=bend, active=("+core",))

    # as in photographs of boulder campusing: the arms only slightly bent,
    # the chest open rather than curled over the tucked knees; the pop
    # drives the hips toward the wall and arches the back a little
    hang = tucked(add(h1, (-11, -60)), -6, h1, add(h1, (0.4, -0.6)), bend=0)
    pop = tucked(add(h1, (-32, -24)), -16, h1, h2, bend=-4)
    panels = []
    for k, c in enumerate((hang, pop)):
        f = Fig(-50, 66, 138, 292)
        wall_side(f, x0, 120, 300, angle=A)
        hold_side(f, "jug", H1, angle=A)
        hold_side(f, "jug", H2, angle=A)
        if k == 0:
            c.draw(f)
            f.label("knees tucked", (107, 104), to=c.J["rkn"])
            f.label("no footholds", (100, 150), to=W(186))
        else:
            hang.draw(f, ghost=True)
            c.draw(f, z=5)
            f.body_arrow([add(hang.pelvis, (6, -18)), add(c.pelvis, (8, -18))])
            f.arrow([add(h1, (-8, 6)), add(lerp(h1, h2, 0.5), (-10, 12)), add(h2, (-4, 6))],
                    kind="move")
            f.label("hips pop up", (107, 104), to=add(c.pelvis, (14, -18)))
        _warn(f"campus-move {'ab'[k]}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["hang, knees tucked", "small pop, hand moves on"])


# ---------------------------------------------------------------- double clutch


def double_clutch(path):
    """Back view, two frames. (a) From both hands matched on one big hold
    (ghost), the climber flies up and right; the left hand makes catch 1
    with a firm, slightly bent arm while the right hand is still on its way.
    (b) The right hand makes catch 2 before the swing reverses."""
    S = (-34, 196)
    A, B = (-8, 292), (70, 296)
    LF, RF = (-66, 34), (-2, 36)       # low and wide: the sink keeps its knees open
    sg = grip(S, size=1.3)
    start = Climber((-34, 92), lh=add(sg, (-6, 0)), rh=add(sg, (6, 0)),
                    lf={"at": stand(LF)}, rf={"at": stand(RF), "style": "back"},
                    knees={"l": "out", "r": "out"})
    # the right hand stops visibly short of B, so (a) reads as catch 1 only;
    # the left arm catches firm and slightly bent, the right is in flight.
    # The body hangs off the left arm: its left side stretches and the hips
    # carry on to the right
    one = _toward((24, 194), {"r": (48, 278)}, lean=-18, bend=6, lh=grip(A),
                    lf={"at": (-6, 112), "style": "back"},
                    rf={"at": (30, 106), "style": "back"},
                    elbows={"l": "down"}, knees={"l": "out", "r": "out"},
                    active=("lupper", "lfore"))
    # still rising a little: both arms catch slightly bent
    two = Climber((28, 198), lean=2, lh=grip(A), rh=grip(B),
                  lf={"at": (16, 110), "style": "back"},
                  rf={"at": (48, 106), "style": "back"},
                  elbows={"l": "down", "r": "out"}, knees={"l": "out", "r": "out"},
                  active=("lupper", "lfore", "rupper", "rfore"))
    panels = []
    for k, (g, c) in enumerate([(start, one), (one, two)]):
        f = Fig(-92, 24, 96, 310)
        wall_grid(f)
        hold(f, "jug", S, size=1.3)
        hold(f, "jug", A)
        hold(f, "jug", B)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        if k == 0:
            g.draw(f, ghost=True)
        else:
            # the hips hardly move from catch 1 to catch 2, so a whole ghost
            # would sit on the climber: show only the legs swinging right
            _ghost_limbs(f, g, ("lleg", "rleg"))
        c.draw(f, z=5)
        if k == 0:
            # up between the legs of the flying climber
            f.body_arrow([add(g.pelvis, (14, -2)), (4, 118), add(c.pelvis, (-10, -38))])
            f.step(1, add(A, (-16, 6)))
            f.arrow([add(c.J["rha"], (4, 4)), add(grip(B), (-5, -5))], kind="move")
            f.label("matched start", (-58, 230), to=add(S, (-12, 4)))
        else:
            f.step(1, add(A, (-16, 6)))
            f.step(2, add(B, (16, 6)))
            f.arrow([add(g.J["rha"], (6, 4)), add(grip(B), (-6, -6))], kind="move")
        _warn(f"double-clutch {'ab'[k]}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["catch 1, left hand", "catch 2, right hand"])


# ---------------------------------------------------------------- foot catch


def foot_catch(path):
    """(a) Back view: the right hand has caught a hold up and right, both
    feet off, and the body swings right. The left leg reaches across the
    front of the volume at hip height; the foot is flexed and the top of
    the toes hooks the volume's far side, pulling back toward the body to
    stop the swing. (b) Close-up from behind, as in the toe hook figure:
    the top of the toes behind the volume's far edge."""
    from figs_feet import shoe_side
    R = (44, 246)
    vol = [(-90, 108), (-48, 114), (-52, 156), (-88, 164)]
    # narrow enough, with the close-up, to sit beside the steps
    f = Fig(-118, 54, 58, 270)
    wall_grid(f)
    hold(f, "jug", R)
    volume(f, vol, apex=(-70, 136))
    # the catching arm, the toe hook pulling back and the stomach tensing
    # as the toe touches; the free left hand holds nothing. The right side
    # hangs long off the arm and the left hip hitches up to lift the leg
    c = Climber((0, 152), lean=-2, bend=-8, lh=(-52, 186), rh=grip(R),
                lf={"at": (-104, 150), "contact": "toe", "angle": 98},
                rf={"at": (22, 70), "contact": "toe", "angle": 290},
                elbows={"l": "down"}, knees={"l": "up", "r": "out"},
                hand_style={"l": "open"},
                order=["rleg", "rarm", "torso", "larm", "lleg"],
                active=("rupper", "rfore", "lshin", "core"))
    c.draw(f)
    f.arrow([(-114, 168), (-94, 168)], kind="force")     # above the toe, off the shin
    f.arrow([(-30, 76), (-86, 84), add(c.J["lan"], (-6, -10))], kind="move")
    f.body_arrow([add(c.pelvis, (-4, -36)), add(c.pelvis, (34, -36))])
    # above the volume, clear of the torso; the leader passes right of
    # the force arrow's head
    f.label("toe hooks far side", (-74, 206), to=add(c.J["lan"], (-8, 14)),
            anchor="middle")
    f.label("swing", (6, 102))
    _warn("foot-catch", c)

    # (b) close-up, same view: the volume's far edge, the ankle flexed and
    # the top of the toes pressing on the far side, the leg pulling back
    shin = sub(c.J["lkn"], c.J["lan"])
    sdeg = math.degrees(math.atan2(shin[1], shin[0]))
    k = Fig(-12.5, -30, 35.5, 30, scale=0.62)
    # the volume's lower left corner, up and right of the toes as the hold
    # is in the toe hook figure, with the shin passing below it
    volume(k, [(-5.5, -4), (44, -11), (44, 19), (-3.9, 19)], apex=(16, 6))
    shoe_side(k, (-6.2, -1), 98, spot="toptoe", up=-1, shin=sdeg, shin_len=50,
              shin_fill=LEFT, name="foot-catch close-up")
    k.arrow([(2, -22), (17, -22)], kind="force")
    k.text("leg pulls", (9, -26.5), size=7)
    k.label("top of the toes", (-12.2, 25), to=(-7, 0.5), size=7, anchor="start")
    # a figure this wide hangs 11 mm into the page margin beside the steps
    # (template.typ's overhang), like the others beside their steps
    combine([f, k], path, gap=4, labels=["a", "b"],
            captions=["toe hooks, swing stops", "behind the edge"])


# ---------------------------------------------------------------- lache


def lache(path):
    """Back view, one wide scene. Feet off, the climber swings the legs on
    the two left jugs (pendulum arrow). At the right end of the swing
    (ghost) both hands let go; the right hand catches the far jug at the
    same height while the left hand follows. Blank wall, no footholds."""
    L1, L2 = (-176, 238), (-148, 238)
    R1 = (64, 238)
    # at the end of the swing the hips lead and the chest stays under the
    # hands, so the waist bends
    rel = Climber((-130, 140), lean=-20, lh=grip(L1), rh=grip(L2),
                  lf={"at": (-100, 60), "contact": "toe", "angle": 262},
                  rf={"at": (-86, 64), "contact": "toe", "angle": 290},
                  elbows={"l": "out", "r": "out"}, knees={"l": "out", "r": "out"},
                  bend=8)
    # the right arm catches, slightly bent; the left hand is still on its
    # way. Hanging off the right arm, the right side stretches.
    catch = _toward((28, 142), {"l": (-20, 252)}, lean=17, bend=-6, rh=grip(R1),
                      lf={"at": (-8, 66), "contact": "toe", "angle": 250},
                      rf={"at": (6, 60), "contact": "toe", "angle": 280},
                      elbows={"l": "out"}, knees={"l": "out", "r": "out"},
                      active=("rupper", "rfore"))
    f = Fig(-222, 44, 100, 282)
    wall_grid(f)
    for p in (L1, L2, R1):
        hold(f, "jug", p)
    rel.draw(f, ghost=True)
    catch.draw(f, z=5)
    f.body_arrow([(-210, 112), (-186, 92), (-156, 94), (-128, 116)])
    f.arrow([add(grip(L2), (8, 10)), (-40, 274), add(grip(R1), (-6, 8))], kind="move")
    f.label("swing", (-200, 70))
    f.label("let go here", (-96, 214), to=add(grip(L2), (6, 2)))
    f.label("no footholds", (-44, 50))
    _warn("lache", rel, catch)
    f.save(path)


# ---------------------------------------------------------------- paddle dyno


def paddle_dyno(path):
    """Back view, time-lapse in one wide scene. Ghost: the launch from two
    start holds. Solid: the left hand leaves sloper 3 on a bent arm and
    the right hand catches the jug. Hand paths arc from hold to hold over
    the top; the taps on 1 and 2 are shown by the arcs and numbers alone
    (a second ghost there crowded the middle). The hips travel along a
    curve through the empty middle, starting beside the ghost and
    stopping short of the climber, so it crosses no limb."""
    S1, S2 = (-150, 200), (-118, 200)
    I = [(-66, 264), (-6, 268), (54, 264)]
    F = (112, 266)
    LF, RF = (-154, 40), (-114, 46)
    launch = Climber((-134, 96), lh=grip(S1), rh=grip(S2),
                     lf={"at": stand(LF), "style": "back"},
                     rf={"at": stand(RF), "style": "back"},
                     knees={"l": "out", "r": "out"})
    catch = Climber((84, 174), lean=4, lh=add(grip(I[2], kind="sloper", size=0.8), (2, -6)),
                    rh=grip(F),
                    lf={"at": (64, 90), "contact": "toe", "angle": 255},
                    rf={"at": (96, 86), "contact": "toe", "angle": 285},
                    elbows={"l": "out", "r": "out"}, knees={"l": "out", "r": "out"},
                    active=("-lupper", "-lfore"))       # the left hand only taps 3
    f = Fig(-196, 34, 150, 300)
    wall_grid(f)
    hold(f, "jug", S1)
    hold(f, "jug", S2)
    for p in I:
        hold(f, "sloper", p, size=0.8)
    hold(f, "jug", F)
    hold(f, "foot", LF)
    hold(f, "foot", RF)
    launch.draw(f, ghost=True)
    catch.draw(f, z=5)
    stops = [grip(S2)] + [grip(p, kind="sloper", size=0.8) for p in I] + [grip(F)]
    for a, b in zip(stops, stops[1:]):
        f.arrow([add(a, (6, 10)), add(lerp(a, b, 0.5), (0, 24)), add(b, (-4, 10))],
                kind="move")
    # 3 sits left of its hold, off the climber's forearm
    for i, p in enumerate(I):
        f.step(i + 1, add(p, (-16, -6) if i == 2 else (0, -15)))
    f.body_arrow([(-100, 112), (-62, 156), (-18, 168), (16, 162)])
    f.label("tap, don’t hold", (-36, 234))
    _warn("paddle-dyno", launch, catch)
    f.save(path)


# ---------------------------------------------------------------- tic-tac


def tic_tac(path):
    """Back view with the floor. The left foot plants on the volume's right
    face and pushes (ghost, standing over the volume with the arms swinging
    up); the push sends the body up and right, and the right hand catches
    the jug with the left arm thrown up beside it (solid). The ghost and the
    climber stand apart, so neither covers the other; the displacement
    from one to the other shows the redirect, so there is no arrow to cross
    a limb. The label sits beside the volume, clear of both bodies. The
    volume gives a step but no foothold to stand on."""
    T = (62, 246)
    vol = [(-118, 16), (-34, 16), (-44, 104), (-108, 112)]
    apex = (-64, 58)
    plant = add(lerp(apex, vol[2], 0.2), (4, 0))        # on the right face
    f = Fig(-150, -12, 98, 270)
    ground(f, 0)
    wall_grid(f, y0=10)
    hold(f, "jug", T)
    volume(f, vol, apex=apex)
    push = _toward((-42, 128), {"l": (-76, 234), "r": (-24, 238)}, lean=-10,
                   lf={"at": plant, "contact": "ball", "angle": 210},
                   rf={"at": (-18, 44), "contact": "toe", "angle": 280},
                   elbows={"l": "out", "r": "out"}, knees={"l": "up", "r": "out"})
    fly = _toward((36, 164), {"l": (26, 262)}, lean=-16, rh=grip(T),
                  head=(5, 1),
                  lf={"at": (6, 86), "contact": "toe", "angle": 250},
                  rf={"at": (30, 78), "contact": "toe", "angle": 275},
                  elbows={"l": "out"}, knees={"l": "out", "r": "out"})
    push.draw(f, ghost=True)
    fly.draw(f, z=5)
    f.label("push, don’t kick", (-28, 28), to=add(plant, (-1, 0)))
    _warn("tic-tac", push, fly)
    f.save(path)


# ---------------------------------------------------------------- filmstrip: the dyno


def filmstrip_dyno(path):
    """'In motion' strip: one dyno in side view on a gently overhanging
    (10 degree) wall, five frames with the same wall, holds and framing:
    feet set and eyes on the target in a straight-armed sink; legs drive
    the hips in and up; let go and reach; catch with both hands; feet off,
    hold the swing. Same geometry as the dyno figure. The feet are on the
    wall, so a bent knee bends toward it: the knees stay clear of the wall
    only while the hips are far out (1) or the legs are nearly straight
    (2, 3)."""
    A = 10
    x0 = 52
    t = math.tan(math.radians(A))

    def W(h):
        return (x0 - t * (h - 60), h)
    S, T, F = W(170), W(306), W(70)
    s, tg, ft = _side_grip(S, A), _side_grip(T, A), _side_foot(F, A)
    s2, tg2 = add(s, (0.4, -0.6)), add(tg, (0.4, -0.6))
    on = dict(lf={"at": add(ft, (-1, -0.5)), "contact": "toe"},
              rf={"at": ft, "contact": "toe"})
    poses = [
        Climber(None, shoulders=add(s, (-48, -43)), view="side", lean=24,
                lh=s, rh=s2, head=(1, 2), bend=8, head_tilt=-25, **on),
        # arched: hips in, shoulders back, arms nearly straight; the legs
        # drive, as in the dyno figure
        Climber(None, shoulders=add(s, (-58, 24.5)), view="side", lean=-35,
                lh=s, rh=s2, head=(3, 0), bend=-14, **on,
                active=("lthigh", "rthigh", "lcalf", "rcalf")),
        # legs straight, toes just off the foothold; the head tips back to
        # look up past the arms
        _toward(None, {"l": add(tg, (-2, -14)), "r": add(tg, (0, -12))},
                shoulders=add(s, (-24, 56)), view="side", lean=-8, head=(-6, -1),
                lf={"at": add(ft, (-5, 7)), "contact": "toe", "angle": 318},
                rf={"at": add(ft, (-3, 9)), "contact": "toe", "angle": 320}),
        Climber(None, shoulders=add(tg, (-13, -56)), view="side", lean=-6,
                lh=tg2, rh=tg,
                lf={"at": (4, 108), "contact": "toe", "angle": 292},
                rf={"at": (8, 106), "contact": "toe", "angle": 294}),
        # the arms, slightly bent, and the stomach hold the swing, which
        # curls the back a little
        Climber(None, shoulders=add(tg, (-17, -58)), view="side", lean=8,
                lh=tg2, rh=tg,
                lf={"at": (-34, 112), "contact": "toe", "angle": 282},
                rf={"at": (-30, 110), "contact": "toe", "angle": 284},
                bend=6, active=("+rupper", "+rfore", "+core")),
    ]
    caps = ["sink, eyes\non target", "drive with\nthe legs", "let go, reach",
            "catch with\nboth hands", "feet off,\nhold the swing"]
    frames = []
    for k, c in enumerate(poses):
        f = Fig(-57.5, 56, 54, 316, scale=0.28)
        wall_side(f, x0, 40, 316, angle=A)
        for p in (S, T):
            hold_side(f, "jug", p, angle=A)
        hold_side(f, "foot", F, angle=A)
        ghosts = []
        if k == 4:
            # the hands stay put and the legs swing out: ghost the legs of
            # frame 4 only, hung from these hips
            ghosts.append(_ghost_limbs(f, poses[3], ("lleg", "rleg"), on=c))
        c.draw(f, z=5)
        _warn(f"filmstrip-dyno {k + 1}", c, *ghosts)
        frames.append(f)
    filmstrip(frames, path, captions=caps)


def build(out):
    deadpoint(out + "/deadpoint.svg")
    hip_pump(out + "/hip-pump.svg")
    dyno(out + "/dyno.svg")
    double_dyno(out + "/double-dyno.svg")
    cutting_loose(out + "/cutting-loose.svg")
    lunge(out + "/lunge.svg")
    counter_kick(out + "/counter-kick.svg")
    hip_pop(out + "/hip-pop.svg")
    latching(out + "/latching.svg")
    jump_start(out + "/jump-start.svg")
    run_and_jump(out + "/run-and-jump.svg")
    pogo(out + "/pogo.svg")
    campus_move(out + "/campus-move.svg")
    double_clutch(out + "/double-clutch.svg")
    foot_catch(out + "/foot-catch.svg")
    lache(out + "/lache.svg")
    paddle_dyno(out + "/paddle-dyno.svg")
    tic_tac(out + "/tic-tac.svg")
    filmstrip_dyno(out + "/filmstrip-dyno.svg")
