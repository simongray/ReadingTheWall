"""Figures for chapter 09, "Your body and how you learn"."""

import math

from climb import *


# ---------------------------------------------------------------- helpers


def hip_flexion(c, s):
    """Side view: angle of the thigh in front of the spine (0 = thigh
    hanging along the spine, about 140 = folded as far as a hip goes)."""
    u, _ = c.frame()
    thigh = sub(c.J[s + "kn"], c.J[s + "hip"])
    down = mul(u, -1)
    h = math.degrees(math.atan2(cross(down, thigh), dot(down, thigh)))
    return h + 360 if h < -100 else h


def warn(name, *climbers, max_hip=147):
    for c in climbers:
        for w in c.warn():
            print(name + ":", w)
        if c.view == "side":
            for s in "lr":
                h = hip_flexion(c, s)
                if h > max_hip:
                    print(f"{name}: {s} hip flexed {h:.0f} deg (max {max_hip})")


# ---------------------------------------------------------------- sit start


def tall_sit_start(path):
    """A tall climber on a sit start: knees jammed vs frog vs staggered feet.
    All three panels use the same start holds: hands at 72 cm, the start
    foothold at 22 cm."""
    panels = []
    WX = 62          # wall line (side view)
    HAND_Y = 72
    FOOT_Y = 22

    # (a) side view: both feet on the start foothold, knees in the chest,
    # bum far out
    f = Fig(-34, -10, 72, 106)
    ground(f, 0, x1=WX)
    at = wall_side(f, WX, 0, 106)
    hold_side(f, "jug", at(HAND_Y))
    hold_side(f, "foot", at(FOOT_Y))
    hand = add(at(HAND_Y), (-4, 3))
    foot = add(at(FOOT_Y), (-2.5, 2.2))
    c = Climber((2, 14), view="side", lean=-7, lh=hand, rh=hand,
                lf={"at": foot}, rf={"at": foot}, head=(-3, -2))
    c.draw(f)
    bum = c.local(-12, -4)
    f.arrow([(bum[0] + 18, 5), (WX - 1, 5)], kind="path")
    f.arrow([(WX - 18, 5), (bum[0] - 1, 5)], kind="path")
    warn("sit-a", c)
    panels.append(f)

    LH, RH = (-24, HAND_Y), (24, HAND_Y)
    # seen from behind, the arms reach forward to the wall and look short;
    # in a frog the thighs go out to the sides and the shins point forward
    # to the wall, away from us, so only the shins are shortened
    REACH = {"l": 0.42, "r": 0.42}
    FROG = (1.0, 0.5)

    # (b) back view: frog, knees wide, chest drops between them
    f = Fig(-74, -10, 74, 106)
    wall_grid(f, y0=12)
    ground(f, 0)
    for h in (LH, RH):
        hold(f, "jug", h)
    LF, RF = (-44, FOOT_Y), (44, FOOT_Y)
    hold(f, "foot", LF)
    hold(f, "foot", RF)
    c = Climber((0, 16), lh=grip(LH), rh=grip(RH),
                lf={"at": stand(LF), "style": "back"},
                rf={"at": stand(RF), "style": "back"},
                knees={"l": "up", "r": "up"}, elbows={"l": "out", "r": "out"},
                arm_len=REACH, leg_len={"l": FROG, "r": FROG})
    c.draw(f)
    warn("sit-b", c)
    panels.append(f)

    # (c) back view: left foot on the start foothold, right foot low and far
    # out, so the right leg stays long
    f = Fig(-74, -10, 112, 106)
    wall_grid(f, y0=12)
    ground(f, 0)
    for h in (LH, RH):
        hold(f, "jug", h)
    RL = (100, 4)
    hold(f, "foot", LF)
    hold(f, "foot", RL)
    c = Climber((2, 15), lean=-3, lh=grip(LH), rh=grip(RH),
                lf={"at": stand(LF), "style": "back"},
                rf={"at": stand(RL), "angle": 70},
                knees={"l": "up", "r": "up"}, elbows={"l": "out", "r": "out"},
                arm_len=REACH, leg_len={"l": FROG})
    c.draw(f)
    f.label("leg long", (84, 44), to=add(c.J["rkn"], (4, 4)))
    warn("sit-c", c)
    panels.append(f)

    combine(panels, path, gap=5, labels=["a", "b", "c"],
            captions=["side: knees jammed", "behind: knees out (frog)",
                      "behind: one foot high, one low"])


# ---------------------------------------------------------------- falling


def fall_roll(path):
    """A safe feet-first fall as a filmstrip: side view, one camera for all
    four frames (wall on the right edge, mat below). Only the first frame
    ghosts the start, the climber hanging on the wall."""
    WX = 70
    hang = add((WX, 248), (-4, 3))
    FOOT = 44                     # the foothold the start position stands on

    def p_hang():
        # on the wall: straight arms, legs nearly straight to a low
        # foothold, hips far enough out that the knees clear the wall
        toe = {"at": (WX - 1.5, FOOT + 2.2), "contact": "toe", "angle": -25}
        return Climber(None, shoulders=add(hang, (-21, -58)), view="side",
                       lean=8, lh=hang, rh=hang, lf=toe, rf=toe)

    def p_air():
        # dropping clear of the wall: the knees stay off it
        # pushed off a little, so the fall clears the climber on the wall
        return Climber((-4, 106), view="side", lean=6,
                       lh=(12, 150), rh=(14, 146),
                       lf={"at": (8, 32), "angle": -25},
                       rf={"at": (4, 29), "angle": -25}, head=(2, -1),
                       head_tilt=30)

    def p_land():
        return Climber((12, 52), view="side", lean=24,
                       lh=(44, 92), rh=(46, 88),
                       lf={"at": (28, 0), "contact": "ball"},
                       rf={"at": (26, 0), "contact": "ball"}, head=(2, -1),
                       head_tilt=20)

    def p_sit():
        return Climber((6, 11), view="side", lean=-18,
                       lh=(34, 50), rh=(36, 46),
                       lf={"at": (40, 0), "contact": "heel", "angle": 30},
                       rf={"at": (38, 0), "contact": "heel", "angle": 30},
                       head=(3, -1), head_tilt=30)

    def p_roll():
        # rounded upper back on the mat, hips lifted, knees to the chest,
        # chin tucked so the head stays off the mat, arms crossed
        chest = Climber((12, 28), view="side", lean=-110).local(15, 32)
        return Climber((12, 28), view="side", lean=-110,
                       lh=add(chest, (2, 2)), rh=chest,
                       lf={"at": (18, 78), "angle": 115},
                       rf={"at": (15, 75), "angle": 115}, head=(1, 7),
                       head_tilt=60)

    def frame():
        f = Fig(-69, -12, 72, 274, scale=0.28)
        ground(f, 0, x1=WX)
        at = wall_side(f, WX, 0, 274)
        hold_side(f, "jug", at(248))
        hold_side(f, "foot", at(FOOT))
        return f

    frames = []
    for i, pose in enumerate((p_air, p_land, p_sit, p_roll)):
        f = frame()
        if i == 0:
            g = p_hang()
            g.draw(f, ghost=True)
            warn("fall-start", g)
            f.arrow([(-38, 160), (-38, 110)], kind="move")
        c = pose()
        c.draw(f)
        if i == 3:
            f.turn((0, 34), 60, 30, 150)
        warn(f"fall-{i + 1}", c)
        frames.append(f)
    filmstrip(frames, path, captions=["look down, arms in", "land on both feet",
                                      "sit back", "roll, chin tucked"])


def fall_mistakes(path):
    """Side view: two landings to avoid."""
    panels = []

    # (a) straight, locked arms planted behind the hips
    f = Fig(-90, -12, 62, 100)
    ground(f, 0)
    c = Climber((0, 14), view="side", lean=-40,
                lh=(-76.5, 3.5), rh=(-76.5, 3.5),
                lf={"at": (36, 0), "contact": "heel", "angle": 20},
                rf={"at": (34, 0), "contact": "heel", "angle": 20},
                head=(-2, 2))
    c.draw(f)
    el = c.J["rel"]
    f.cross(add(el, (-9, 10)), size=f.mm(1.6))
    f.label("straight arms", (-60, 92), to=add(el, (-1, 3)))
    warn("mistake-a", c)
    panels.append(f)

    # (b) stiff, straight legs and arms flung back
    f = Fig(-82, -12, 52, 196)
    ground(f, 0)
    c = Climber((0, 94), view="side", lean=-10,
                lh=(-70, 124), rh=(-64, 138),
                lf={"at": (14, 0), "contact": "ball"},
                rf={"at": (10, 0), "contact": "ball"})
    c.draw(f)
    f.cross(add(c.J["rkn"], (15, 4)), size=f.mm(1.6))
    f.label("knees locked", (-40, 58), to=add(c.J["rkn"], (-5, -1)))
    f.label("arms flung back", (-36, 186), to=add(c.J["rha"], (1, 4)))
    warn("mistake-b", c)
    panels.append(f)

    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["posting the arms", "landing stiff"])


def build(out):
    tall_sit_start(out + "/considerations-sit-start.svg")
    fall_roll(out + "/considerations-fall-roll.svg")
    fall_mistakes(out + "/considerations-fall-mistakes.svg")
