"""Figures for the body positioning chapter (04-body).

Hold facing follows the book's convention: `use=` is the way the gripping
surface faces. A sidepull faces away from the body (a right-hand sidepull on
your right faces right, use=0); a gaston faces the body's midline.
"""

from climb import *
import plan
from figs_hands import label_lines


def _warn(name, *climbers):
    """Print every limb that misses its hold (with the gap in cm) and every
    joint the library flags as impossible."""
    for c in climbers:
        for s in "lr":
            t = getattr(c, s + "h")
            if t is not None:
                gap = length(sub(t, c.J[s + "ha"]))
                if gap > 1:
                    print(f"{name}: {s} hand short by {gap:.0f}")
            ft = getattr(c, "_" + s + "f")
            gap = length(sub(ft["ankle_target"], c.J[s + "an"]))
            if gap > 1:
                print(f"{name}: {s} foot short by {gap:.0f}")
        for w in c.warn():
            if "out of reach" not in w:
                print(f"{name}: {w}")


def _short(make, side, target):
    """Build a climber whose `side` hand ("l" or "r") stretches fully toward
    `target` but stops short of it. `make(point)` builds the climber with
    that hand at `point`. The hand ends exactly at full reach, so the pose
    is valid and the gap to the hold shows the missing reach."""
    c = make(target)
    sh = c.J[side + "sh"]
    reach = c.reach(side)
    d = sub(target, sh)
    if length(d) <= reach - 0.5:
        return c
    return make(add(sh, mul(norm(d), reach - 0.5)))


def _back(x0, y0, x1, y1):
    f = Fig(x0, y0, x1, y1)
    wall_grid(f)
    return f


def _hinge(f, a, b, ext=14, label=None, label_at=None):
    """Dashed line through two contacts: the axis the body rotates about."""
    d = norm(sub(b, a))
    p0, p1 = sub(a, mul(d, ext)), add(b, mul(d, ext))
    f.line(p0, p1, sw=0.45, dash=(2.2, 1.2), z=55)
    if label:
        f.label(label, label_at, to=lerp(p0, a, 0.5))


# ---------------------------------------------------------------- frog


def frog(path):
    """(a) Back view: knees out, inside edges, hips between the feet.
    (b) Side view on a vertical wall, the mistake: knees pointing at the
    wall push the hips out. (c) The same wall and holds: knees turned out to
    the sides let the hips come in (the thighs point toward the viewer, so
    they are drawn foreshortened). (b) and (c) are separate panels, not a
    ghost over the climber, so the two bodies don't merge into one."""
    a = _back(-80, 44, 80, 240)
    LH, RH = (-28, 222), (30, 214)
    LF, RF = (-36, 70), (38, 74)
    hold(a, "jug", LH)
    hold(a, "crimp", RH)
    hold(a, "foot", LF)
    hold(a, "foot", RF)
    c = Climber((0, 128), lh=grip(LH), rh=grip(RH, kind="crimp"),
                lf={"at": stand(LF)}, rf={"at": stand(RF)},
                knees={"l": "out", "r": "out"})
    c.draw(a)
    a.cog(c.cog(), plumb_to=62)
    a.arrow([add(c.J["lkn"], (-6, 6)), add(c.J["lkn"], (-18, 10))], kind="move")
    a.arrow([add(c.J["rkn"], (6, 6)), add(c.J["rkn"], (18, 10))], kind="move")
    a.label("knees out", (-30, 52), to=add(c.J["lkn"], (2, -5)))
    _warn("frog a", c)

    sides = []
    for k in range(2):
        f = Fig(-75, 44, 55, 240)
        at = wall_side(f, 35, 44, 240, angle=0)
        H, F = at(212), at(72)
        hold_side(f, "jug", H)
        hold_side(f, "foot", F)
        hand = add(H, (-3.5, 2))
        foot = add(F, (-2.5, 2.5))
        if k == 0:
            # knees to the wall: the hips stay out and the chest curls in
            # over the knees toward the hands
            c = Climber((-18, 132), view="side", lean=4, bend=8, lh=hand, rh=hand,
                        lf={"at": foot}, rf={"at": foot})
            f.cross(add(c.pelvis, (-30, -2)))
        else:
            # the hips in, the chest back off them
            c = Climber((8, 128), view="side", lean=0, bend=-6, lh=hand, rh=hand,
                        lf={"at": foot}, rf={"at": foot},
                        leg_len={"l": (0.62, 0.9), "r": (0.62, 0.9)})
        c.draw(f)
        f.cog(c.cog(), plumb_to=62)
        _warn(f"frog {'bc'[k]}", c)
        sides.append(f)
    combine([a] + sides, path, gap=6, labels=["a", "b", "c"],
            captions=["frog: knees out, inside edges", "knees to wall: hips out",
                      "hips come close to the wall"])


# ---------------------------------------------------------------- hip turn


# The backstep family (hip turn, backstep) shares one problem: the right
# hand on a sidepull that faces right (use=0, so you hang to its left), the
# left foot on a hold below it, the right foot wide, a target up and left.
SIDE_RH = (78, 244)
SIDE_A = (74, 86)
SIDE_B = (115, 82)
SIDE_T = (12, 246)
SIDE_P = (58, 154)      # pelvis of the turned climber


def _turned(pelvis=SIDE_P, lh=None, a=SIDE_A, turn=-0.85, lean=-28, bend=-10, foot=-8, **kw):
    """The hip-turned climber of the backstep family: left foot on its
    outside edge on `a`, left hip to the wall, right arm long, hips over
    the left heel. The hips stand over the heel and the chest leans on
    toward the reach, so the side under the long right arm stretches.
    `foot` is the angle of the left shoe: more negative points its toe down."""
    return Climber(pelvis, turn=turn, lean=lean, bend=bend, lh=lh, rh=grip(SIDE_RH, use=0),
                   lf={"at": stand(a), "angle": foot}, rf={"at": stand(SIDE_B)},
                   knees={"l": "right", "r": "out"}, elbows={"r": "down"},
                   leg_len={"l": 0.9}, head=(3, 1), **kw)   # head clear of the reaching arm


# from above: the left foot on its outside edge along the wall, the hips over
# its heel, the right foot on its inside edge
_TURNED_LEGS = {"l": dict(heel=(-3, 10), deg=10, knee=(22, -2)),
                "r": dict(heel=(28, 10), deg=2, knee=(38, 1))}


def _side_holds(f, a=SIDE_A):
    hold(f, "jug", SIDE_RH, use=0)
    hold(f, "jug", SIDE_T, variant="bucket")
    hold(f, "foot", a)
    hold(f, "foot", SIDE_B)


def hip_turn(path):
    """Back view, overhang. The right hand holds a sidepull facing right;
    the left hand reaches up and left. (a) Square on, the left toe front-on
    (an inside edge would push its ankle right and fold the knee flat at
    foot height): the hand falls short. (b) Left foot on its outside edge,
    left hip to the wall, right arm long: the hand reaches."""
    panels = []
    for k in range(2):
        f = _back(-34, 50, 140, 276)
        _side_holds(f)
        if k == 0:
            # the chest leans on toward the reach, as in (b)
            c = _short(lambda h: Climber(
                (80, 138), lean=-20, bend=-8, lh=h, rh=grip(SIDE_RH, use=0),
                lf={"at": stand(SIDE_A), "style": "back"}, rf={"at": stand(SIDE_B)},
                knees={"l": "out", "r": "out"}, elbows={"r": "down"},
                head=(3, 1)), "l", grip(SIDE_T))
            c.draw(f)
            f.cross(add(SIDE_T, (-3, -12)))
            f.label("hips square", (14, 126), to=add(c.pelvis, (-8, -2)))
            plan.hips(f, (5, 78), 0, head=20, to_wall=28, lean=(-8, -22), span=(-46, 60),
                      label_y=54.5,
                      legs={"l": dict(heel=(-1, 2), deg=90, knee=(-34, 11), xray=False),
                            "r": dict(heel=(26, 22), deg=2, knee=(38, 13))})
        else:
            c = _turned(lh=grip(SIDE_T))
            c.draw(f)
            # placed so the leader starts past the end of the text (the
            # frame edge holds the text where it was)
            f.label("left hip in", (20, 146), to=add(c.pelvis, (-7, -3)))
            f.label("outside edge", (104, 56), to=add(stand(SIDE_A), (2, -1)))
            # the head looks back at the right hand, as the steps say
            plan.hips(f, (3, 85.2), -55, chest=-30, head=-60, to_wall=16, lean=(-12, -22),
                      span=(-46, 60), spin=(36, 190, 160), label_y=54.5, legs=_TURNED_LEGS)
        _warn(f"hip-turn {k}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["square on: hand falls short", "left hip in: hand reaches"])


# ---------------------------------------------------------------- backstep


def backstep(path):
    """Back view. Right hand on a sidepull facing right. (a) Left foot on
    its outside edge on the line under that hold: the left hip stays in and
    the hips settle over the heel. (b) The same foot behind the line: the
    hips rotate back out and the left hand falls short."""
    line_x = SIDE_RH[0]
    panels = []
    for k in range(2):
        A = SIDE_A if k == 0 else (36, 84)
        # a little wider than the hip-turn frame, so the inset's label
        # clears the line
        f = _back(-34, 50, 146, 276)
        f.line((line_x, 234), (line_x, 70), sw=0.35, dash=(1.0, 1.0), z=-1)
        f.text("the line", (line_x, 62), size=7)
        _side_holds(f, A)
        if k == 0:
            c = _turned(lh=grip(SIDE_T))
            c.draw(f)
            f.cog(c.cog(), plumb_to=78)
            f.label("hips over heel", (36, 70), to=(c.cog()[0], 80))
            plan.hips(f, (112, 218), -55, chest=-30, head=-60, to_wall=16, lean=(-12, -22),
                      s=0.55, span=(-34, 56), legs=_TURNED_LEGS, label_y=188)
        else:
            # the hips spin out: the arm stretches toward the hold, short.
            # The chest sags away from the right hand that holds the spin.
            # With the knee off to the right, the toe points down or the
            # ankle would fold past what an ankle can do
            kw = dict(a=A, turn=-0.3, lean=-12, bend=-8, foot=-24)
            sh = _turned((46, 152), **kw).J["lsh"]
            tg = grip(SIDE_T)
            # the right arm holds the spin; the reaching arm is relaxed
            c = _turned((46, 152), sub(tg, mul(norm(sub(tg, sh)), 24)),
                        active=("-lupper", "-lfore"), **kw)
            c.draw(f)
            f.cross(add(SIDE_T, (-1, -11)))
            f.label("foot behind", (4, 66), to=add(stand(A), (-14, -3)))
            plan.hips(f, (112, 211.4), -15, chest=-8, head=15, to_wall=28, lean=(-10, -22),
                      s=0.55, span=(-34, 56), spin=(28, 150, 195), label="hips turn out",
                      label_y=188,
                      legs={"l": dict(heel=(-28, 22), deg=-2, knee=(0, 8)),
                            "r": dict(heel=(28, 22), deg=2, knee=(38, 12))})
        _warn(f"backstep {k}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["foot on the line: hips stay in",
                      "foot behind it: hips spin out"])


# ---------------------------------------------------------------- drop knee


def _dropped_foot(at, angle=-10):
    """The foot of a dropped knee, as photographs from behind show it: rolled
    onto its outside edge with the sole facing up and back, the toes along
    the wall away from the body and the heel up by the shin. The shoe's top
    faces down and the outside of its toe box rests on the hold `at`, so
    the contact point on the sole sits the toe box's depth above it."""
    d = ang(angle)
    down = perp(d) if perp(d)[1] < 0 else mul(perp(d), -1)
    return {"at": sub(stand(at), mul(down, 6.7)), "angle": angle}


def drop_knee(path):
    """Back view, steep wall. Left hand on a sidepull facing left (pulled to
    the right), right foot on a high foothold out right at hip height (the
    text puts it between waist and shoulder), left foot low and wide. (a)
    Square on, the right toe on the hold with the knee up: the right hand
    falls short. (b) Right knee dropped, the foot rolled onto its
    outside edge, the right hip turned in; both feet push apart and the
    right hand reaches. The thigh and shin lie along the wall, so they are
    drawn full length."""
    L = (-70, 172)    # left sidepull, gripping edge faces left
    T = (28, 236)
    LF = (-66, 52)    # low and wide, so the push leg in (b) is nearly straight
    RF = (76, 130)
    panels = []
    for k in range(2):
        f = _back(-92, 40, 100, 252)
        hold(f, "jug", L, use=180)
        hold(f, "jug", T)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        if k == 0:
            # the chest tips toward the sidepull as in (b): the reaching side
            # stretches, and still falls short. The high toe points into
            # the wall (seen heel-on), as the how-to places it
            c = _short(lambda h: Climber(
                (-8, 108), bend=-8, lh=grip(L, use=180), rh=h,
                lf={"at": stand(LF)}, rf={"at": stand(RF), "style": "back"},
                knees={"l": "out", "r": "up"}, elbows={"l": "down"},
                head=(2, 1)), "r", grip(T))
            c.draw(f)
            f.cross(add(T, (-11, -7)))
            f.label("knee up", (72, 160), to=add(c.J["rkn"], (3, 2)))
            plan.hips(f, (-52, 219.6), 0, head=-20, to_wall=28, lean=(-3, -22), s=0.55,
                      span=(-56, 56), label_y=196.5, label_dx=-4,
                      legs={"l": dict(heel=(-28, 22), deg=178, knee=(-36, 12)),
                            "r": dict(heel=(40, 2), deg=90, knee=(36, 10))})
        else:
            # as in photographs of drop knees from behind: the thigh runs
            # down and out along the wall to a knee below both the hip and
            # the foot, and the shin rises to the foot
            c = Climber((0, 134), turn=0.85, lean=-4, lh=grip(L, use=180),
                        rh=grip(T), lf={"at": stand(LF)}, rf=_dropped_foot(RF),
                        knees={"l": "out", "r": "down"}, elbows={"l": "down"},
                        head=(2, 1),
                        bend=-12,   # hips upright, chest bent: the reaching side stretches
                        active=("lthigh",))   # the push leg works; the arms unload
            c.draw(f)
            f.arrow([add(stand(LF), (-8, 14)), add(stand(LF), (-26, 14))],
                    kind="force")
            f.arrow([add(stand(RF), (-2, -12)), add(stand(RF), (16, -12))], kind="force")
            f.label("knee points down", (56, 62), to=add(c.J["rkn"], (2, -3)))
            f.label("right hip in", (41, 168), to=add(c.J["rhip"], (3, 2)))
            plan.hips(f, (-52, 226.2), 55, chest=30, head=-10, to_wall=16, lean=(-8, -22), s=0.55,
                      span=(-56, 56), spin=(28, -60, -22), label_y=196.5, label_dx=-4,
                      legs={"l": dict(heel=(-28, 10), deg=178),
                            "r": dict(heel=(26, 10), deg=2, knee=(32, 10))})
        _warn(f"drop-knee {k}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["square on: too short", "knee dropped: hip in, reach gained"])


# ---------------------------------------------------------------- flags


# Flags: the hand that stays on and the foot you stand on make a hinge (the
# long-dashed line). The free leg must press the wall on the far side of the
# hinge from the body, or the body swings open around it.


def flag(path):
    """Back view. Left hand above the right foot: the hinge is vertical.
    (a) Reaching right with the left leg dangling: the CoG hangs right of
    the hinge and the body swings open (its right side comes off the wall).
    (b) Side flag: the left leg stretched out to the left, inside edge on
    the wall, hips over the standing foot."""
    LH = (-12, 256)
    RF = (-6, 72)
    T = (52, 250)
    panels = []
    for k in range(2):
        f = _back(-100, 50, 92, 276)
        hold(f, "jug", LH)
        hold(f, "jug", T)
        hold(f, "foot", RF)
        _hinge(f, add(grip(LH), (0, -6)), stand(RF), ext=12)
        if k == 0:
            # the chest leans on into the reach, out past the hinge. The hand stops
            # short, because the body swings open before it arrives
            c = Climber((8, 150), turn=-0.35, lean=4, bend=8, lh=grip(LH),
                        rh=add(grip(T), (-6, -26)), rf={"at": stand(RF), "style": "back"},
                        lf={"at": (-44, 74), "angle": -110, "contact": "toe"},
                        knees={"r": "out", "l": "left"}, head=(2, 1), active=("-rupper", "-rfore"))
            c.draw(f)
            f.cog(c.cog(), plumb_to=66)
            plan.from_back(f, c, (48, 165), "l", s=0.56, reach=8, span=(8, 48),
                           label_at=(4, -49))
            f.label("hinge", (-56, 262), to=(-11, 238))
            f.cross(add(T, (0, -13)))
        else:
            # the chest bends right, against the flagged leg out left
            c = Climber((-4, 154), lean=4, bend=8, lh=grip(LH), rh=grip(T),
                        rf={"at": stand(RF), "style": "back"},
                        lf={"at": (-88, 90), "angle": 200, "contact": "edge"},
                        knees={"l": "up", "r": "out"}, head=(2, 1),
                        active=("-lupper", "-lfore"))     # the flagged leg balances, not the arm
            c.draw(f)
            f.cog(c.cog(), plumb_to=66)
            f.label("foot presses wall", (-78, 68), to=(-84, 88))
        _warn(f"flag {k}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["no flag: door opens", "side flag: leg balances"])


def back_flag(path):
    """Back view. Left hand above the left foot: the hinge is vertical. The
    right leg crosses behind the left calf (on the viewer's side), straight,
    and presses the wall left of and below the left foot. The hips sit over
    the left foot, so the CoG is on the hinge."""
    LH = (-36, 262)    # sidepull facing left: the body hangs to its right
    LF = (-30, 70)
    T = (36, 238)
    f = _back(-100, 54, 76, 276)
    hold(f, "jug", LH, use=180)
    hold(f, "jug", T)
    hold(f, "foot", LF)
    _hinge(f, add(grip(LH, use=180), (0, -6)), stand(LF), ext=12)
    # the chest bends right, against the leg crossed out to the left
    c = _back_flagger(LH, LF, T, lean=3, bend=10)
    c.draw(f)
    f.cog(c.cog(), plumb_to=58)
    f.label("hinge", (-74, 250), to=(-39, 236))
    f.label("right leg behind", (8, 70), to=add(lerp(c.J["rkn"], c.J["ran"], 0.3), (2, 0)))
    _warn("back-flag", c)
    f.save(path)


def _back_flagger(LH, LF, T, lean=8, bend=0.0):
    """The back-flag climber: standing on the left foot (pointing into the
    wall) under the left hand; the right leg drawn over the left one."""
    return Climber((-30, 156), lean=lean, bend=bend, turn=0.2, lh=grip(LH, use=180),
                   rh=grip(T), lf={"at": stand(LF), "style": "back"},
                   rf={"at": (-70, 62), "angle": 200, "contact": "edge"},
                   knees={"l": "out", "r": "down"}, leg_len={"l": .95},
                   elbows={"l": "out"}, head=(2, 1), allow_cross=True,
                   order=["lleg", "torso", "rleg", "larm", "rarm"])


def inside_flag(path):
    """Back view. The left hand holds a low edge and the left foot stands on
    the only foothold, below it. (a) Crouched: left foot on the hold, right
    foot smeared on the wall. (b) Standing up: the right leg passes between
    the left leg and the wall (so from behind it is hidden by the left leg)
    and presses the wall on the far left; the right hip turns in and every
    limb ends nearly straight."""
    LH = (-44, 140)
    S = (60, 196)
    T = (38, 251)
    LF = (-14, 52)
    panels = []
    for k in range(2):
        f = _back(-92, 34, 84, 264)
        hold(f, "jug", LH)
        hold(f, "jug", S)
        hold(f, "jug", T, variant="horn")
        hold(f, "foot", LF, size=1.4)
        if k == 0:
            # the chest settles left, over the foot that will stand you up
            c = Climber((4, 122), bend=-6, lh=grip(LH), rh=grip(S),
                        lf={"at": stand(LF, size=1.4)},
                        rf={"at": (54, 64), "angle": 10, "contact": "ball"},
                        knees={"l": "out", "r": "out"}, elbows={"l": "down"},
                        head=(2, 1), active=("+lthigh",))   # the left leg stands you up
            c.draw(f)
            f.body_arrow([(-72, 72), (-72, 120)])
            f.text("stand up", (-72, 62), size=7.5)
        else:
            # the chest bends right, against the leg pressed out to the left
            c = Climber((2, 150), lean=-1, bend=10, turn=0.7, lh=grip(LH), rh=grip(T),
                        lf={"at": stand(LF, size=1.4)},
                        rf={"at": (-66, 76), "angle": 200, "contact": "edge"},
                        knees={"l": "out", "r": "left"}, elbows={"l": "down"},
                        head=(2, 1), order=["rleg", "rarm", "torso", "lleg", "larm"],
                        allow_cross=True)
            c.draw(f)
            f.text("and wall", (-64, 52 - f.pt(9.5)), size=7.5)
            f.label("between leg", (-64, 52), to=lerp(c.J["rkn"], c.J["ran"], 0.45), anchor="middle")
            f.label("limbs straight", (46, 168), to=lerp(c.J["rel"], c.J["rha"], .4), anchor="middle")
            plan.hips(f, (-46, 232), 45, chest=25, to_wall=16, lean=(4, -22), span=(-74, 24),
                      spin=(27, -8, 30), label_y=205,
                      legs={"l": dict(heel=(4, 11), deg=175, knee=(-10, 0)),
                            "r": dict(heel=(-45, 10), deg=182, knee=(-30, 8))})
        _warn(f"inside-flag {k}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["start: one low foothold", "stand up, leg through"])


# ---------------------------------------------------------------- twist lock


def twist_lock(path):
    """Back view, steep wall. Right hand on a sidepull facing right, left foot
    backstepped under it, right foot wide. (a) Set: right arm straight, hips
    half turned, shoulders still square. (b) Locked: the legs have pushed the
    body up, the left hip and left shoulder are turned in, the right elbow
    is down at the ribs and the left hand reaches high. The right forearm
    points into the wall, so the arm is drawn a little foreshortened. (c)
    The lock of (b) from the side, where that forearm shows its length."""
    RH = (61, 194)      # sidepull, faces right
    S = (-40, 200)
    T = (26, 262)
    A = (60, 74)
    B = (100, 86)       # a little higher, so the right thigh clears the left knee
    panels = []
    for k in range(2):
        # wide enough on the left for the left elbow in (a)
        f = _back(-63, 50, 124, 276)
        hold(f, "jug", RH, use=0)
        hold(f, "jug", S)
        hold(f, "jug", T)
        hold(f, "foot", A)
        hold(f, "foot", B)
        kw = dict(rh=grip(RH, use=0), lf={"at": stand(A), "angle": -8},
                  rf={"at": stand(B)}, knees={"l": "right", "r": "out"},
                  elbows={"r": "down", "l": "down"}, arm_len={"r": 0.88},
                  leg_len={"l": 0.9}, head=(-2, 1))
        if k == 0:
            # hanging off the straight arm, the chest sags away from it
            c = Climber((6, 138), turn=-0.45, sh_w=1.0, lean=-14, bend=-8,
                        lh=grip(S), **kw)
            c.draw(f)
            f.label("arm straight", (100, 150), to=lerp(c.J["rsh"], c.J["rha"], .6))
            plan.hips(f, (-34, 89), -28, chest=-5, head=30, to_wall=24, lean=(-14, -22),
                      span=(-42, 52), spin=(29, 200, 160), label="from above", label_y=62,
                      legs={"l": dict(heel=(-6, 18), deg=2, knee=(14, 8)),
                            "r": dict(heel=(24, 18), deg=2, knee=(36, 8))})
        else:
            # the locked arm works (its lat, which pulls it down, is hidden
            # behind the upper arm); the reaching arm is relaxed. The elbow
            # is down by the ribs and the forearm points into the wall, so
            # the forearm shows a little more than half its length. The
            # right side shortens as the elbow pulls down; the left
            # stretches into the reach
            kw["arm_len"] = {"r": (0.95, 0.6)}
            c = Climber((48, 162), turn=-0.95, lean=-13, bend=10, lh=grip(T),
                        order=["lleg", "larm", "torso", "rleg", "rarm"],
                        active=("rupper", "rfore"), **kw)
            c.draw(f)
            f.arrow([add(stand(A), (-20, -8)), add(stand(A), (-6, -8))], kind="force")
            f.arrow([add(stand(B), (20, -8)), add(stand(B), (6, -8))], kind="force")
            # in two lines: in one, the text ran past the panel's edge and was
            # pushed back under its own leader
            label_lines(f, ["elbow", "to ribs"], (100, 172), to=add(c.J["rel"], (-1, 1)), size=7.5)
            f.label("shoulder in", (-8, 222), to=add(c.J["lsh"], (2, 0)))
            f.label("feet squeeze", (83, 62))
            # the chin comes round to the right shoulder, as the steps say
            plan.hips(f, (-34, 93.8), -65, chest=-55, head=-115, to_wall=16, lean=(-6, -22),
                      span=(-42, 52), spin=(29, 195, 160), label="from above", label_y=62,
                      legs={"l": dict(heel=(-6, 10), deg=2, knee=(14, 4)),
                            "r": dict(heel=(24, 10), deg=2, knee=(34, 2))})
        _warn(f"twist-lock {k}", c)
        panels.append(f)
    panels.append(_twist_lock_side(RH, T, A, B))
    combine(panels, path, gap=6, labels=["a", "b", "c"],
            captions=["set: arm straight", "lock: hip, then shoulder",
                      "forearm into wall"])


def _twist_lock_side(RH, T, A, B, W=30):
    """(c) of the twist lock: (b) seen from its right side, the holds at
    the same heights. The forearm that (b) shows short points into the
    wall at its full length; the elbow is down at the ribs and the hips
    are in at the wall."""
    f = Fig(W - 80, 50, W + 10, 276)
    at = wall_side(f, W, 50, 276)
    for kind, h in (("jug", RH), ("jug", T), ("foot", A), ("foot", B)):
        hold_side(f, kind, at(h[1]))
    # both knees point along the wall, toward the viewer (the left one
    # backstepped, the right one out), so the thighs are foreshortened.
    # The hips press in and the chest arches back off them
    c = Climber((W - 18, 162), view="side", lean=-6, bend=-10,
                lh=add(at(T[1]), (-3.5, 2)), rh=add(at(RH[1]), (-3.5, 2)),
                lf={"at": add(at(A[1]), (-2.5, 2.5))},
                rf={"at": add(at(B[1]), (-2.5, 2.5))},
                leg_len={"l": (0.8, 1.0), "r": (0.62, 1.0)},
                # the chest arches back, but the head stays nearly level and
                # back from the raised arm, so the jaw slopes and the chin
                # doesn't run into the arm's line
                head=(-2, 0), head_tilt=12,
                active=("rupper", "rfore"))
    c.draw(f)
    _warn("twist-lock c", c)
    return f


# ---------------------------------------------------------------- lock-off


def lock_off(path):
    """Side view, vertical wall: the right hand (near side, white) locked
    on an edge beside the shoulder, elbow down by the ribs; feet set fairly
    high on one foothold; the left hand reaches slowly for a small hold."""
    # room on the left for the labels, so the frame doesn't push them onto
    # their leaders (the figure stays narrower than its caption)
    f = Fig(-80, 44, 46, 248)
    at = wall_side(f, 32, 44, 248, angle=0)
    E, T, F = at(170), at(226), at(66)
    hold_side(f, "edge", E)
    hold_side(f, "crimp", T)
    hold_side(f, "foot", F)
    # knees turned out to the sides (frog), so the thighs are foreshortened
    c = Climber((2, 128), view="side", lean=-3, lh=add(T, (-2.5, 1.0)),
                rh=add(E, (-2.5, 1.5)), lf={"at": add(F, (-2.5, 2.5))},
                rf={"at": add(F, (-2.5, 2.5))}, head=(1, 2),
                leg_len={"l": (0.72, 1.0), "r": (0.72, 1.0)},
                active=("rupper", "rfore", "rthigh"))     # the reaching arm is relaxed
    c.draw(f)
    f.label("locked arm", (-34, 140), to=c.J["rel"])
    f.label("slow reach", (-30, 232), to=add(T, (-6, 3)))
    _warn("lock-off", c)
    f.save(path)


# ---------------------------------------------------------------- layback


def layback(path):
    """Seen from the side of a flake (the climber faces the flake, as in
    every side view): the arms are straight and pull the flake's edge out
    toward the body; the feet press flat on the flake's face, fairly high;
    the hips hang low and out. Arms and body make a "7". The force arrows
    point in opposite directions: that opposition is the technique."""
    f = Fig(-116, 34, 50, 182)
    W = 36
    wall_side(f, W, 34, 182, angle=0)
    fx = W - 9
    # the flake grows out of the wall at its foot, with the crack behind it
    # (where the fingers hook) opening upward
    flake = [(W, 40), (fx, 54), (fx, 172), (fx + 2.5, 176), (fx + 4, 172),
             (fx + 4, 62), (W, 50)]
    f.poly(flake, z=-6, fill=DARK, stroke=INK, sw=0.3)
    if XRAY:
        # dotted where the hands and feet cover it, as on a hold
        f.poly(flake, z=XRAY_Z, **XRAY_STYLE)
    H1, H2 = (fx + 3, 158), (fx + 3, 144)
    F1, F2 = (fx - 1, 86), (fx - 1, 68)
    # the hips hang out off straight arms, the hands above the shoulders;
    # the chest lifts and the head looks up at the hands, so the body
    # leans off the arms instead of hunching over them. The near arm takes
    # the upper hold, so the arm in front is the straight one
    c = Climber(None, shoulders=(-31, 136), view="side", lean=46, bend=-16,
                head=(-1, 1), head_tilt=-10, lh=H2, rh=H1,
                lf={"at": F1, "contact": "ball", "angle": 72},
                rf={"at": F2, "contact": "ball", "angle": 66},
                active=("lthigh", "rthigh"))   # the feet push in; the arms hang straight
    c.draw(f)
    # each arrow beside its contacts: the pull just above the hands, the
    # push just below the feet
    pull, push = H1[1] + 10, F2[1] - 16
    f.arrow([(fx - 2, pull), (fx - 26, pull)], kind="force")
    f.arrow([(fx - 26, push), (fx - 2, push)], kind="force")
    f.label("hands pull out", (-50, pull + 6), to=(fx - 26, pull + 1))
    f.label("feet push in", (-50, push - 8), to=(fx - 26, push))
    _warn("layback", c)
    f.save(path)


# ---------------------------------------------------------------- stemming


def stemming(path):
    """Back view between two volumes, so as not to repeat the corner figure a
    page later: each foot pushes outward into the face of its own volume (heels
    low, toes up), the left palm presses the left volume with the fingers pointing
    down, the right hand reaches. The force arrows point away from each other:
    the feet push apart."""
    X0, Y0, X1, Y1 = -96, 44, 96, 262
    # a strip at the bottom for the label
    f = Fig(X0, Y0 - 10, X1, Y1)
    wall_grid(f)
    # the faces toward the climber end at the apexes; the outlines run on behind
    # the frame's edge, as these are big volumes
    volume(f, [(-128, 60), (-50, 70), (-42, 130), (-56, 198), (-128, 206)], apex=(-88, 126))
    volume(f, [(128, 68), (50, 80), (44, 130), (60, 182), (128, 190)], apex=(90, 128))
    T = (30, 249)
    hold(f, "jug", T)
    # wide, the legs only a little bent, as in photographs of stems from
    # behind (and "higher and wider than feels natural")
    LF, RF = (-78, 98), (76, 104)
    LH = (-70, 166)
    # the chest tips over the pressing palm; the reaching side stretches
    c = Climber((-2, 154), bend=-6, lh=LH, rh=grip(T),
                lf={"at": LF, "angle": 165, "contact": "ball"},
                rf={"at": RF, "angle": 15, "contact": "ball"},
                knees={"l": "out", "r": "out"}, elbows={"l": "out"},
                hand_style={"l": "open"}, head=(2, 1),
                active=("+lthigh", "+rthigh"))   # the legs push apart
    c.draw(f)
    # under the shoes and beside the palm
    f.arrow([add(LF, (2, -12)), add(LF, (-14, -12))], kind="force")
    f.arrow([add(RF, (-2, -12)), add(RF, (14, -12))], kind="force")
    f.arrow([add(LH, (-10, -2)), add(LH, (-25, -2))], kind="force")
    f.label("palm presses", (-62, 222), to=add(LH, (-2, 4)))
    f.label("feet push apart", (0, 40))
    _warn("stemming", c)
    f.save(path)


def cross_through(path):
    """Back view, traversing left. The left hand holds a sidepull facing
    left, locked off beside the head with the body hanging to its right.
    The right hip rolls in (right foot on its outside edge), the left leg
    presses the wall as the off foot, and the right hand crosses over the
    left to a hold beyond it.

    With the hip rolled in, the right arm passes between the face and the
    wall, so from behind it goes behind the head. The right elbow is carried
    over the head, so the arm shows rising from the right shoulder; a
    straight arm reaching further left would be hidden behind the head from
    the shoulder on and look as if it grew out of the neck."""
    LH = (-17.2, 193)
    S = (34, 212)
    T = (-44, 216)
    RF = (12, 62)
    f = _back(-88, 57, 84, 262)
    hold(f, "jug", LH, use=180, size=0.85)
    hold(f, "jug", S)
    hold(f, "jug", T, size=0.85)
    hold(f, "foot", RF)
    # the left elbow points back from the wall in the lock-off, so the arm
    # is drawn a little foreshortened
    # fully turned, so the shoulders narrow and the right hand crosses
    # well past the left; the chest leans on after the crossing arm
    c = Climber((12, 138), turn=1.0, lean=-12, bend=-8,
                lh=grip(LH, use=180, size=0.85),
                rh=grip(T, size=0.85),
                lf={"at": (-62, 96), "angle": 190, "contact": "edge"},
                rf={"at": stand(RF), "angle": 180},
                knees={"l": "up", "r": "left"}, elbows={"l": "down", "r": "up"},
                arm_len={"l": 0.85}, head=(-2, -2), allow_cross=True,
                active=("+llat",))   # the locked-off arm pulls in with the back
    c.draw(f)
    f.arrow([add(S, (-4, 10)), (4, 250), (-34, 232)], kind="move")
    f.label("off foot on wall", (-84, 66), to=(-64, 92), anchor="start")
    f.label("hip rolls in", (26, 112), to=add(c.J["rhip"], (2, 0)), anchor="start")
    f.label("start", (56, 186), to=add(S, (4, -4)))
    _warn("cross-through", c)
    f.save(path)

# ---------------------------------------------------------------- matching


# The hands come from authored.py, like every hand close-up in the book, but at
# 1.6 mm per cm rather than the close-ups' HAND_SCALE (2.6): at that scale the
# two panels would be about 140 mm wide, too wide to sit beside the steps.
MATCH_SCALE = 1.6
MATCH_TOP = 0.0          # top of the edge


def _face_edge(f, c, w, h, z=-5):
    """A short edge seen face-on, with its hidden outline dotted where the
    hands cover it."""
    x, y = c
    r = h * 0.25
    pts = [(x - w / 2 + r, y + h / 2), (x + w / 2 - r, y + h / 2), (x + w / 2, y),
           (x + w / 2 - r, y - h / 2), (x - w / 2 + r, y - h / 2), (x - w / 2, y)]
    f.smooth(pts, z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    f.line((x - w / 2 + r, y + h * 0.3), (x + w / 2 - r, y + h * 0.3), z=z + 0.1,
           sw=0.55, stroke=WHITE)
    if XRAY:
        f.smooth(pts, z=XRAY_Z, tension=0.5, **XRAY_STYLE)


def matching(path):
    """Close-up from behind of a short edge, fingers over it. (a) Left hand in
    the middle: the right hand would hang off the end. (b) Left hand on the
    left half: the right hand fits beside it."""
    import authored as A
    panels = []
    for k in range(2):
        f = Fig(-11.5, -17.732, 14.5, 7.0, scale=MATCH_SCALE)
        wall_grid(f, step=10)
        _face_edge(f, (0, MATCH_TOP - 1.5), 21.6, 3.0)
        if k == 0:
            A.draw_hand(f, A.drag_from_behind("l", 0.08, MATCH_TOP), z=0, fill=LEFT)
            # a little low, so its thumb stays behind the solid one
            A.draw_hand(f, A.drag_from_behind("r", 9.72, MATCH_TOP - 0.3), z=-3, ghost=True)
            f.cross((9.38, -11.27))
        else:
            A.draw_hand(f, A.drag_from_behind("l", -5.82, MATCH_TOP), z=0, fill=LEFT)
            A.draw_hand(f, A.drag_from_behind("r", 5.82, MATCH_TOP), z=2)
        panels.append(f)
    combine(panels, path, gap=5, labels=["a", "b"],
            captions=["centred: no room", "left half: room to match"])

# ---------------------------------------------------------------- compression


def compression(path):
    """Back view. A big volume at head height, the Y of reading 7. It stands
    about 45 cm off the wall on a base 60 cm wide, so its left face faces left
    and its right face faces right: a wider, shallower one would face out at
    you, with nothing to squeeze. The palms press those faces inward, elbows
    down, as in a hug; the feet squeeze a lower volume the same way. All four
    force arrows point inward."""
    f = Fig(-92, 46, 92, 246)
    wall_grid(f)
    volume(f, [(-30, 176), (-24, 238), (24, 238), (30, 176), (20, 148), (-20, 148)],
           apex=(0, 200))
    V, TOP = (-34, 66), (0, 104)       # the lower volume's left corner and top
    volume(f, [V, TOP, (34, 66), (0, 50)], apex=(0, 70))
    # frog: knees out, each shoe side-on along an upper face of the lower
    # volume, toes out and down the slope like the knees, the sole pressing
    # the face down and in. (Toes pointing in toward the volume would need
    # the knees to point in too: a bent knee points where the toes point.)
    e = norm(sub(V, TOP))
    down_face = math.degrees(math.atan2(e[1], e[0]))
    P = lerp(V, TOP, 0.35)
    # the shoulders stand well off the wall and the palms close to it, so the
    # arms point partly at the viewer and are drawn shortened
    c = Climber((0, 130), lh=(-25, 198), rh=(25, 198),
                lf={"at": P, "angle": down_face, "contact": "ball"},
                rf={"at": (-P[0], P[1]), "angle": 180 - down_face, "contact": "ball"},
                knees={"l": "out", "r": "out"}, elbows={"l": "down", "r": "down"},
                arm_len={"l": (.6, .9), "r": (.6, .9)},
                hand_style={"l": "open", "r": "open"},
                active=("+llat", "+rlat"))   # a hug: the back squeezes too
    c.draw(f)
    for sg in (-1, 1):
        f.arrow([(sg * 58, 196), (sg * 38, 196)], kind="force")
        # square to the face, stopping short of the toe
        f.arrow([(sg * 52, 93.5), (sg * 36, 81.5)], kind="force")
    _warn("compression", c)
    f.save(path)


# ---------------------------------------------------------------- body tension


def body_tension(path):
    """Side view, 40 degree overhang. (a) Slack: the feet have cut and the
    body swings down under the hands. (b) Tense: straight arms, toes pulled
    into the foothold, hips held up close to the wall."""
    A = 40
    panels = []
    for k in range(2):
        # the wall stops short of the panel's edge, so it isn't cut off by it
        f = Fig(-150, 18, 22, 240)
        at = wall_side(f, 95 - (112 - 18) * math.tan(math.radians(A)), 112, 240, angle=A)
        H = at(222)
        F = at(130)
        hold_side(f, "jug", H, angle=A)
        hold_side(f, "foot", F, angle=A)
        hand = add(H, (-3.5, 1.5))
        foot = add(F, (-2.5, 2.5))
        if k == 0:
            c = Climber(None, shoulders=add(hand, (-1, -60)), view="side", lean=-2,
                        lh=hand, rh=hand,
                        lf={"at": add(hand, (-6, -190)), "angle": -50},
                        rf={"at": add(hand, (0, -192)), "angle": -50})
            c.draw(f)
            f.turn(hand, 202, 290, 256)
            f.text("you swing", (-4, 50))
            f.cross(add(foot, (-6, -8)))
        else:
            # the hamstrings pull the toes in; the trunk holds the hips up
            c = Climber(None, shoulders=add(hand, (-30, -52)), view="side", lean=-50,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        active=("rham", "core"))
            c.draw(f)
            f.arrow([add(foot, (-16, -12)), add(foot, (-3, 0))], kind="force")
            f.label("toes pull in", (-4, 84), to=add(foot, (-12, -8)))
            f.label("hips stay up", (-100, 96), to=add(c.pelvis, (-6, -6)))
        _warn(f"body-tension {k}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["slack: feet cut", "tense: feet stay on"])

# ---------------------------------------------------------------- pre-loading


def pre_loading(path):
    """Side view, 25 degree overhang. (a) Pulled in tight: knees to the wall,
    feet barely weighted. (b) Sat back: arms straight, hips down and out,
    heels low; then drive the hips up and in."""
    A = 25
    panels = []
    for k in range(2):
        f = Fig(-116, 40, 66, 256)
        at = wall_side(f, 50, 40, 256, angle=A)
        H, T, F = at(196), at(244), at(88)
        hold_side(f, "jug", H, angle=A)
        hold_side(f, "jug", T, angle=A)
        hold_side(f, "foot", F, angle=A)
        hand = add(H, (-3.5, 2))
        foot = add(F, (-2.5, 2.5))
        if k == 0:
            # pulled in tight, the chest curled to the wall over the knees
            c = Climber(None, shoulders=add(hand, (-18, -32)), view="side",
                        lean=-16, bend=8,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        elbows={"l": "down", "r": "down"},
                        knees={"l": "up", "r": "up"})
            c.draw(f)
            f.arrow([add(foot, (-2, -4)), add(foot, (-12, -16))], kind="move")
            f.label("feet unweighted", (-42, 56), to=add(foot, (-6, -6)))
        else:
            # sunk before the drive: the hips sit back and the chest curls
            # in over them
            c = Climber(None, shoulders=add(hand, (-33, -55)), view="side",
                        lean=0, bend=10,
                        lh=hand, rh=hand, lf={"at": foot, "angle": 20},
                        rf={"at": foot, "angle": 20}, head=(-6, 0),
                        active=("rthigh",))   # the loaded legs will drive
            c.draw(f)
            f.arrow([add(foot, (-20, -16)), add(foot, (-6, -9))], kind="force")
            p = c.pelvis
            # next: drive the hips up and in toward the wall
            f.body_arrow([add(p, (-26, -2)), add(p, (-28, 36)), add(p, (-10, 62))])
            f.text("then up and in", (p[0] - 18, p[1] - 26), size=7)
            f.label("arms straight", (-72, 234), to=lerp(c.J["lsh"], hand, .5))
            f.label("heels low", (12, 54), to=add(foot, (-12, -2)))
        _warn(f"pre-loading {k}", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["tight: feet slide", "sat back: feet press"])


# ---------------------------------------------------------------- opposition


def opposition(path):
    """Back view: two sidepulls that face away from each other (the left one
    faces left, the right one faces right), pulled toward each other. The
    force arrows at the hands point at each other."""
    a = _back(-90, 57, 90, 232)
    L, R = (-54, 188), (54, 188)
    hold(a, "jug", L, use=180)
    hold(a, "jug", R, use=0)
    LF, RF = (-30, 62), (32, 66)
    hold(a, "foot", LF)
    hold(a, "foot", RF)
    c = Climber((0, 136), lh=grip(L, use=180), rh=grip(R, use=0),
                lf={"at": stand(LF)}, rf={"at": stand(RF)},
                elbows={"l": "down", "r": "down"}, knees={"l": "out", "r": "out"},
                active=("+llat", "+rlat"))   # pulling inward works the back
    c.draw(a)
    for sg in (-1, 1):
        a.arrow([(sg * 88, 188), (sg * 68, 188)], kind="force")
    a.label("pull inward", (0, 224))
    _warn("opposition", c)
    a.save(path)

# ---------------------------------------------------------------- bumping


def bumping(path):
    """Back view: the right hand went from its start hold to a small
    intermediate (1), then straight on to the jug (2). The left hand and
    the feet stayed put."""
    LH = (-57, 241)    # high enough that the holding arm hangs straight
    S = (40, 170)
    I = (70, 212)
    T = (34, 250)
    LF, RF = (-28, 66), (30, 72)
    # the frame sits right of centre so "intermediate" fits beside its
    # hold, clear of the arrow
    f = _back(-74, 60, 122, 266)
    hold(f, "jug", LH)
    hold(f, "jug", S)
    hold(f, "crimp", I)
    hold(f, "jug", T)
    hold(f, "foot", LF)
    hold(f, "foot", RF)
    # the body hangs off the straight left arm, its chest swung on after
    # the moving right hand
    c = Climber((-2, 147), lean=3, bend=5, lh=grip(LH), rh=grip(T),
                lf={"at": stand(LF)}, rf={"at": stand(RF)},
                knees={"l": "out", "r": "out"}, elbows={"l": "down"},
                head=(2, 2))
    c.draw(f)
    f.arrow([add(S, (6, 8)), add(I, (-4, -7))], kind="move")
    f.arrow([add(I, (-4, 8)), add(T, (14, -2))], kind="move")
    f.step(1, (46, 198))
    f.step(2, (66, 244))
    f.label("intermediate", (90, 190), to=add(I, (6, -2)))
    f.label("start", (78, 158), to=add(S, (5, -3)))
    _warn("bumping", c)
    f.save(path)


# ---------------------------------------------------------------- filmstrip


def filmstrip_drop_knee(path):
    """In motion: a drop knee into a long reach, back view, five frames.
    Left hand on a sidepull facing left; the right hand starts on a hold
    at chest height; the target is up and right. (1) Square on, both feet
    low: the target is out of reach. (2) The right toe steps up to a hold
    at hip height, the knee up. (3) The right knee drops, the foot rolls
    onto its outside edge and the right hip turns to the wall. (4) The hips
    rise and the right hand reaches the target. (5) The knee turns back up
    before standing.

    The high foothold sits a little above the hips (the text puts it
    between waist and shoulder), as in the drop-knee figure, so the frames
    are wider than in the other filmstrips and drawn a little smaller."""
    L = (-34, 226)      # sidepull, faces left
    S = (34, 196)
    T = (14, 236)
    LF, RF0, RF = (-36, 46), (14, 46), (56, 148)
    # the toe on the hold, pointing at the wall (seen heel-on)
    toe = {"at": stand(RF), "style": "back"}
    # dropped, as in the drop-knee figure: the thigh and shin lie along the
    # wall, the knee below the hip and the foot, the foot rolled onto its
    # outside edge with the sole up. The straight left leg pushes out
    drop = dict(turn=0.85, rf=_dropped_foot(RF), knees={"l": "out", "r": "down"},
                active=("+lthigh",))
    poses = [
        dict(P=(-8, 125), rh=grip(S), rf={"at": stand(RF0)},
             knees={"l": "out", "r": "out"}),
        dict(P=(-4, 128), rh=grip(S), rf=toe, knees={"l": "out", "r": "up"}),
        # with the knee dropped the chest tips toward the sidepull, as in
        # the drop-knee figure, and the reaching side stretches
        dict(P=(-8, 132), lean=-6, bend=-10, rh=grip(S), **drop),
        dict(P=(-8, 134), lean=-4, bend=-10, rh=grip(T), **drop),
        # the knee turns up toward the wall: the thigh is foreshortened
        dict(P=(4, 142), turn=0.3, lean=-4, bend=-6, rh=grip(T), rf=toe,
             knees={"l": "out", "r": "up"}, leg_len={"r": (0.8, 1.0)}),
    ]
    frames = []
    for k, p in enumerate(poses):
        f = Fig(-56, 38, 64, 258, scale=0.26)
        wall_grid(f)
        hold(f, "jug", L, use=180)
        hold(f, "jug", S, xray=False if k == 4 else None)   # empty, behind the arm
        hold(f, "jug", T)
        for h in (LF, RF0, RF):
            hold(f, "foot", h)
        kw = {k_: v for k_, v in p.items() if k_ != "P"}
        c = Climber(p["P"], lh=grip(L, use=180), lf={"at": stand(LF)},
                    elbows={"l": "down"}, head=(2, 1), **kw)
        c.draw(f)
        if k == 0:
            f.arrow([add(grip(S), (2, 10)), add(T, (0, -18))], kind="move")
            f.cross(add(T, (0, -12)))
        elif k == 1:
            f.arrow([add(stand(RF0), (8, 8)), (44, 84), add(RF, (0, -10))],
                    kind="move")
        elif k == 2:
            # below the thigh: the knee drops
            hp, kn = c.J["rhip"], c.J["rkn"]
            off = mul(perp(norm(sub(kn, hp))), -11)
            f.arrow([add(lerp(hp, kn, 0.25), off), add(lerp(hp, kn, 0.85), off)],
                    kind="move")
        elif k == 3:
            f.arrow([add(S, (8, 8)), add(T, (8, -10))], kind="move")
        else:
            kn = c.J["rkn"]
            # below the shin, clear of the hips: the knee turns back up
            f.arrow([add(kn, (14, -46)), add(kn, (14, -26))], kind="move")
        _warn(f"filmstrip-drop-knee {k + 1}", c)
        frames.append(f)
    filmstrip(frames, path, captions=["square on: short",
                                      "right toe on\nthe high hold",
                                      "drop the knee,\nhip in",
                                      "reach high",
                                      "catch, knee up"])


def build(out):
    frog(out + "/frog.svg")
    hip_turn(out + "/hip-turn.svg")
    backstep(out + "/backstep.svg")
    drop_knee(out + "/drop-knee.svg")
    flag(out + "/flag.svg")
    back_flag(out + "/back-flag.svg")
    inside_flag(out + "/inside-flag.svg")
    twist_lock(out + "/twist-lock.svg")
    lock_off(out + "/lock-off.svg")
    layback(out + "/layback.svg")
    stemming(out + "/stemming.svg")
    cross_through(out + "/cross-through.svg")
    matching(out + "/matching.svg")
    compression(out + "/compression.svg")
    body_tension(out + "/body-tension.svg")
    pre_loading(out + "/pre-loading.svg")
    opposition(out + "/opposition.svg")
    bumping(out + "/bumping.svg")
    filmstrip_drop_knee(out + "/filmstrip-drop-knee.svg")
