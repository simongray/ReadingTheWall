"""Figures for "Eight problems to read" in the reading chapter (02).

Each problem has a question figure, with only the wall and its marks, and an
answer figure of the same wall with a climber and the hand order. A file's name
gives the grade, which paint.py turns into the holds' colour, and never gives
away the answer. research/worked-readings.md says why each hold and pose is what
it is.
"""

import math

from climb import *
from figs_terrain import tag
from figs_feet import FootClimber, check
from figs_dynamic import _side_grip, _side_foot
from figs_body import _hinge


# ---------------------------------------------------------------- helpers


def hand(kind, pos, **opts):
    """A hold a hand takes, so it shows chalk."""
    return dict(kind=kind, pos=pos, chalk=True, **opts)


def shoe(kind, pos, **opts):
    """A hold only a foot takes, so it shows rubber."""
    return dict(kind=kind, pos=pos, rubber=True, **opts)


def foot(pos, size=1):
    return shoe("foot", pos, size=size)


def draw_holds(f, holds, used=()):
    """Draw `holds`. Only those named in `used` show through the climber."""
    for name, h in holds.items():
        opts = {k: v for k, v in h.items() if k not in ("kind", "pos")}
        hold(f, h["kind"], h["pos"], xray=name in used, **opts)


def back_view(frame):
    """A figure of a wall from behind, with its bolt holes and the mat."""
    x0, _, x1, y1 = frame
    f = Fig(*frame)
    wall_grid(f, x0=x0 + 4, x1=x1 - 4, y0=10, y1=y1 - 4)
    ground(f, 0)
    return f


def start_tape(f, *points):
    for x, y in points:
        f.poly([(x - 1.6, y), (x + 1.6, y), (x + 1.6, y - 9), (x - 1.6, y - 9)],
               fill=INK, stroke=None, z=-4)


def number(f, n, p):
    f.text(str(n), p, size=6.2, weight=600)


def number_with_leader(f, n, at, to):
    f.label("", at, to=to)
    number(f, n, at)


def mark(f, tags, numbers):
    """The letters or hand orders, boxed, and the foothold numbers, bare."""
    for s, p in tags.items():
        tag(f, s, p)
    for n, p in numbers.items():
        number(f, n, p)


# ---------------------------------------------------------------- 1, slab


SLAB_FRAME = (-90, -8, 90, 366)
SLAB_VOLUME = [(4, 42), (44, 40), (50, 56), (30, 68), (8, 62)]
SLAB_SMEAR = (24, 60)
SLAB = {
    "A": hand("crimp", (-6, 150), variant="rail", size=1.3),
    "B": hand("sloper", (48, 228), variant="dome"),
    "C": hand("crimp", (-38, 250), use=180, w=17, h=8),
    "D": hand("crimp", (30, 296), variant="rail"),
    "E": hand("jug", (2, 348), variant="bucket"),
    1: foot((-24, 16), 1.15), 2: foot((20, 22), 1.15),
    3: foot((-20, 92)), 4: foot((30, 112), 1.6),
    5: foot((-12, 128)), 6: foot((26, 165)), 7: foot((-22, 200)),
}


def slab_wall(used=()):
    f = back_view(SLAB_FRAME)
    volume(f, SLAB_VOLUME, apex=(26, 54))
    draw_holds(f, SLAB, used)
    start_tape(f, (-20, 146), (8, 146))
    return f


def slab(out):
    f = slab_wall()
    mark(f, dict(A=(13, 154), B=(63, 230), C=(-27, 253), D=(44, 297), E=(16, 350)),
         {1: (-14, 17), 2: (30, 23), 3: (-11, 93), 4: (42, 113), 5: (-3, 129),
          6: (36, 166), 7: (-13, 201)})
    f.save(out + "/reading-v2-slab.svg")

    f = slab_wall(used=("A", "B", "C", "D", 4, 5))
    c = Climber((36, 203), lean=8,
                lh=grip(SLAB["C"]["pos"], use=180, kind="crimp"),
                rh=grip(SLAB["D"]["pos"], kind="crimp"),
                lf=stand(SLAB[5]["pos"]), rf=stand(SLAB[4]["pos"], size=1.6),
                active=("lfore", "rthigh"))
    c.draw(f)
    f.label("", (-66, 160), to=(-14, 150))
    mark(f, {"A": (-66, 160), "C L1": (-61, 253), "B R2": (74, 230), "D R3": (58, 297), "E R4 L5": (31, 350)},
         {1: (-14, 17), 2: (30, 23), 3: (-11, 93), 6: (15, 166), 7: (-13, 201)})
    number_with_leader(f, 4, (72, 112), (38, 112))
    number_with_leader(f, 5, (-62, 126), (-18, 128))
    f.arrow([(20, 26), (24, 61)])
    f.arrow([(-23, 22), (-21, 84)])
    f.arrow([(26, 70), (29, 108)])
    f.step(1, (8, 31))
    f.step(2, (-33, 54))
    f.step(3, (16, 92))
    check("reading-v2-slab-answer", c)
    f.save(out + "/reading-v2-slab-answer.svg")


# ---------------------------------------------------------------- 2, traverse


TRAVERSE_FRAME = (-185, -8, 102, 262)
TRAVERSE = {
    "A": hand("jug", (-150, 208), variant="bucket"),
    "B": hand("jug", (-92, 216), variant="flat"),
    "C": hand("crimp", (-38, 222), w=11, h=6),
    "D": hand("crimp", (14, 208), use=180, w=15, h=5, variant="rail"),
    "E": hand("jug", (86, 212), variant="bucket"),
    1: foot((-168, 44), 1.15), 2: foot((-128, 36)), 3: foot((-90, 42)), 4: foot((-26, 50)),
    5: foot((8, 62)), 6: foot((50, 40)), 7: foot((88, 44)),
}
TRAVERSE_NUMBERS = {1: (-158, 45), 2: (-118, 37), 3: (-81, 43), 4: (-17, 51),
                    5: (18, 63), 6: (60, 41), 7: (97, 45)}


def traverse_wall(used=()):
    f = back_view(TRAVERSE_FRAME)
    draw_holds(f, TRAVERSE, used)
    start_tape(f, (-164, 204), (-136, 204))
    return f


def traverse(out):
    f = traverse_wall()
    mark(f, dict(A=(-136, 211), B=(-77, 218), C=(-24, 224), D=(26, 210), E=(71, 214)),
         TRAVERSE_NUMBERS)
    f.save(out + "/reading-v3-traverse.svg")

    f = traverse_wall(used=("C", "D", 4, 5))
    # mirrors the pose in cross_through
    c = Climber((-36, 120), turn=-1.0, lean=12, bend=8, head=(2, -2),
                lh=grip(TRAVERSE["D"]["pos"], use=180, kind="crimp"),
                rh=grip(TRAVERSE["C"]["pos"], kind="crimp"),
                lf={"at": stand(TRAVERSE[4]["pos"]), "angle": 0},
                rf={"at": stand(TRAVERSE[5]["pos"]), "angle": -10},
                knees={"r": "up", "l": "right"}, elbows={"r": "down", "l": "up"},
                allow_cross=True, active=("rfore", "lthigh"))
    c.draw(f)
    mark(f, {"A": (-136, 211), "B R1 L2": (-99, 227), "C R3": (-58, 228),
             "D L4": (31, 210), "E R5 L6": (78, 224)},
         TRAVERSE_NUMBERS)
    f.arrow([(-82, 208), (-64, 199), (-46, 198)])
    f.step(4, (-68, 186))
    check("reading-v3-traverse-answer", c)
    f.save(out + "/reading-v3-traverse-answer.svg")


# ---------------------------------------------------------------- 3, overhang


OVERHANG_FRAME = (-72, -8, 112, 338)
OVERHANG = {
    "A": shoe("jug", (84, 168), size=1.4, variant="bucket"),
    "B": hand("crimp", (-14, 172), size=1.4, variant="rail"),
    "C": hand("crimp", (4, 262), use=165, w=14, h=7, variant="rail"),
    "D": hand("sloper", (60, 270), variant="rail"),
    "E": hand("jug", (44, 322), variant="bucket"),
    1: foot((-28, 30), 1.15), 2: foot((28, 44), 1.15), 3: foot((-14, 76)), 4: foot((-26, 120)),
}
OVERHANG_NUMBERS = {1: (-17, 31), 2: (38, 45), 3: (-4, 77), 4: (-16, 121)}


def overhang_wall(used=()):
    f = back_view(OVERHANG_FRAME)
    draw_holds(f, OVERHANG, used)
    start_tape(f, (-30, 168), (2, 168))
    return f


def overhang(out):
    f = overhang_wall()
    mark(f, dict(A=(102, 170), B=(12, 174), C=(14, 263), D=(78, 271), E=(58, 324)),
         OVERHANG_NUMBERS)
    f.save(out + "/reading-v3-overhang.svg")

    f = overhang_wall(used=("A", "B", "C", "D", 4))
    c = FootClimber((34, 176), lean=16, bend=8,
                    lh=grip(OVERHANG["C"]["pos"], use=165, kind="crimp"),
                    rh=grip(OVERHANG["D"]["pos"], kind="sloper"),
                    lf={"at": stand(OVERHANG[4]["pos"]), "angle": 196},
                    rf={"at": add(OVERHANG["A"]["pos"], (-5, 4)), "angle": 14, "spot": "heel", "up": 1},
                    knees={"r": "up"}, leg_len={"r": (.85, .7)}, head=(2, 3), active=("+rham", "+lthigh"))
    c.draw(f)
    f.label("", (-50, 172), to=(-28, 172))
    mark(f, {"A heel": (84, 150), "B": (-50, 172), "C L1": (-14, 270),
             "D R2": (85, 271), "E R3 L4": (73, 324)},
         {**OVERHANG_NUMBERS, 4: (-36, 121)})
    f.body_arrow([(14, 120), (42, 146)])
    check("reading-v3-overhang-answer", c)
    f.save(out + "/reading-v3-overhang-answer.svg")


# ---------------------------------------------------------------- 4, steep wall


# hold_side turns a hold with the wall, so the library's sloper would fall 53 degrees
# from level at its top on this wall, too steep to rise on. This one has no lip
# either, but its top falls only 28 degrees.
HOLD_PROFILES["sloper_steep"] = (
    [(0, -8), (4, -7.5), (8, -4.5), (9.5, -1), (7.5, 2.8), (3.5, 4.6), (0, 4.2)], (0, 6), (3, 4, 5, 6), -1,
    [(HOLD_MID, 3.2), (HOLD_LIGHT, 2.0), (WHITE, 0.9)])

# From the side: each hold's kind, height along the wall and size. This wall has
# no chalk or rubber, since hold_side draws neither.
STEEP_ANGLE = 35
STEEP_FRAME = (-100, -8, 180, 342)
STEEP = {
    "A": ("edge", 156, 1), "B": ("jug", 200, 1), "C": ("edge", 242, 1),
    "D": ("sloper_steep", 286, 1), "E": ("jug", 326, 1),
    1: ("foot", 54, 1), 2: ("foot", 84, 1), 3: ("foot", 116, 1.7), 4: ("foot", 216, 1),
}
# How far the drawn pose's joints must stay from the wall, in centimetres, since
# warn() doesn't test the wall in a side view: the hips, shoulders, head, elbows
# and knees.
STEEP_CLEARANCE = {"hips": 12, "lsh": 10, "rsh": 10, "head": 11,
                   "lel": 3, "rel": 3, "lkn": 3, "rkn": 3}


def steep_wall(used=()):
    f = Fig(*STEEP_FRAME)
    ground(f, 0)
    at = wall_side(f, 170, 0, 338, angle=STEEP_ANGLE)
    for name, (kind, height, size) in STEEP.items():
        hold_side(f, kind, at(height), angle=STEEP_ANGLE, size=size, xray=name in used)
    return f, at


def steep_marks(f, at, labels={}):
    """Letters and numbers on the wall's hatched side, clear of the climber."""
    for name, (_, height, _) in STEEP.items():
        if isinstance(name, str):
            s = labels.get(name, name)
            tag(f, s, add(at(height), (11 + f.mm(1.25 + 1.55 * len(s)) / 2, 6)))
        else:
            number(f, name, add(at(height), (17, -3)))


def check_clear_of_wall(name, c, at):
    along = norm(sub(at(338), at(0)))
    out = (-along[1], along[0])         # from the wall towards the climber
    points = {**c.J, "hips": c.pelvis, "head": c._head_centre()}
    for joint, least in STEEP_CLEARANCE.items():
        clear = dot(sub(points[joint], at(0)), out)
        if clear < least:
            print(f"{name}: {joint} {clear:.0f} cm from the wall (want {least})")


def steep(out):
    f, at = steep_wall()
    steep_marks(f, at)
    f.save(out + "/reading-v4-steep.svg")

    f, at = steep_wall(used=("A", "C", "D", 3))
    c = Climber((2.1, 184), view="side", lean=-35, bend=0,
                lh=_side_grip(at(242), STEEP_ANGLE), rh=_side_grip(at(286), STEEP_ANGLE, out=4.5, up=2.0),
                lf={"at": _side_foot(at(116), STEEP_ANGLE), "contact": "toe"},
                rf={"at": _side_foot(at(156), STEEP_ANGLE), "contact": "toe"},
                arm_len={"l": .7}, leg_len={"r": (.35, .95)}, active=("+rham",))
    c.draw(f)
    steep_marks(f, at, {"B": "B R1", "C": "C L2", "D": "D R3", "E": "E R4 L5"})
    f.body_arrow([(-44, 180), (-12, 186)])
    check("reading-v4-steep-answer", c)
    check_clear_of_wall("reading-v4-steep-answer", c, at)
    f.save(out + "/reading-v4-steep-answer.svg")


# ---------------------------------------------------------------- 5, sit start


SIT_FRAME = (-110, -8, 90, 326)
SIT = {
    "A": hand("crimp", (-25, 114), variant="rail"),
    "B": hand("crimp", (23, 118), variant="rail"),
    "C": hand("crimp", (38, 194), size=1.2),
    "D": hand("crimp", (-26, 236)),
    "E": hand("sloper", (28, 262)),
    "F": hand("jug", (0, 306), variant="bucket"),
    1: foot((-64, 8)), 2: foot((24, 12)), 3: foot((58, 44)), 4: foot((-22, 62)),
    5: foot((44, 98)), 6: foot((58, 146)),
}


def sit_wall(used=()):
    f = back_view(SIT_FRAME)
    draw_holds(f, SIT, used)
    start_tape(f, (-38, 110), (10, 116))
    return f


def sit_start(out):
    f = sit_wall()
    mark(f, dict(A=(-12, 115), B=(37, 119), C=(52, 196), D=(-14, 237), E=(43, 264), F=(14, 308)),
         {1: (-55, 9), 2: (33, 13), 3: (68, 45), 4: (-13, 63), 5: (53, 99), 6: (68, 147)})
    f.save(out + "/reading-v4-sit.svg")

    f = sit_wall(used=("A", "B", "C", 3, 4, 5, 6))
    c = Climber((24, 106), turn=.2, lean=6,
                lh=grip(SIT["A"]["pos"], kind="crimp"), rh=grip(SIT["C"]["pos"], kind="crimp"),
                lf=stand(SIT[4]["pos"]), rf=stand(SIT[3]["pos"]),
                knees={"l": "left", "r": "out"}, head=(2, 3), leg_len={"l": (1.0, .65)},
                active=("rfore", "rupper", "lthigh", "rthigh"),
                order=["rleg", "rarm", "torso", "larm", "lleg"])
    c.draw(f)
    f.label("", (-58, 130), to=(-34, 119))
    f.label("", (58, 130), to=(44, 123))
    number_with_leader(f, 5, (32, 78), (41, 94))
    mark(f, {"A": (-58, 130), "B": (58, 130), "C R1": (59, 196), "D L2": (-6, 237),
             "E R3": (50, 264), "F R4 L5": (29, 308)},
         {1: (-73, 9), 2: (14, 13), 3: (68, 45), 4: (-36, 54), 6: (68, 147)})
    # the feet went first: the left from 1 to 4, then the right from 2 to 3
    f.arrow([(-60, 16), (-78, 36), (-68, 58), (-44, 66)])
    f.step(2, (-92, 38))
    f.arrow([(32, 18), (40, 30), (50, 40)])
    f.step(3, (52, 22))
    check("reading-v4-sit-answer", c)
    f.save(out + "/reading-v4-sit-answer.svg")


# ---------------------------------------------------------------- 6, long gap


GAP_FRAME = (-78, -8, 72, 344)
GAP = {
    "A": hand("jug", (-24, 150)),
    "B": hand("jug", (18, 156)),
    "C": hand("crimp", (-26, 206), variant="rail", size=1.4),
    "D": hand("crimp", (-30, 262)),
    "E": hand("crimp", (24, 300), variant="curved"),
    "F": hand("jug", (-2, 332), variant="bucket"),
    1: foot((24, 26), 1.15), 2: foot((-30, 30), 1.15), 3: foot((-32, 66), 1.5),
    4: foot((26, 74), 1.5), 5: foot((-46, 100)), 6: foot((32, 108)),
}
GAP_NUMBERS = {1: (34, 27), 2: (-20, 31), 3: (-21, 67), 4: (39, 75), 5: (-37, 101), 6: (42, 109)}


def gap_wall(used=()):
    f = back_view(GAP_FRAME)
    draw_holds(f, GAP, used)
    start_tape(f, (-34, 146), (8, 152))
    return f


def long_gap(out):
    f = gap_wall()
    mark(f, dict(A=(-10, 152), B=(32, 158), C=(-11, 207), D=(-16, 263), E=(36, 301), F=(12, 332)),
         GAP_NUMBERS)
    f.save(out + "/reading-v5-gap.svg")

    f = gap_wall(used=("A", "D", "E", 5, 6))
    c = Climber((14, 186), lean=-16,
                lh=grip(GAP["D"]["pos"], kind="crimp"), rh=grip(GAP["E"]["pos"], kind="crimp"),
                lf=stand(GAP[5]["pos"]), rf=stand(GAP[6]["pos"]), active=("rthigh",))
    c.draw(f)
    f.label("", (-6, 128), to=(-17, 149))
    mark(f, {"A": (-6, 128), "B": (17, 137), "C L1 R2": (-57, 207), "D L3": (-53, 263),
             "E R4": (3, 301), "F L5 R6": (27, 332)},
         {**GAP_NUMBERS, 5: (-55, 101)})
    f.body_arrow([(60, 176), (60, 216)])
    check("reading-v5-gap-answer", c)
    f.save(out + "/reading-v5-gap-answer.svg")


# ---------------------------------------------------------------- 7, volumes


VOLUMES_FRAME = (-92, -8, 92, 324)
VOLUME_Y = [(-30, 176), (-24, 238), (24, 238), (30, 176), (20, 148), (-20, 148)]
VOLUME_X = [(-34, 66), (0, 104), (34, 66), (0, 50)]
VOLUMES = {
    "A": hand("jug", (0, 120), variant="flat"),
    "B": hand("jug", (10, 312), variant="bucket"),
    1: foot((34, 24), 1.15), 2: foot((-36, 28), 1.15), 3: foot((-46, 146)), 4: foot((46, 150)),
}
VOLUMES_NUMBERS = {1: (44, 25), 2: (-26, 29), 3: (-58, 147), 4: (58, 151)}


def volumes_wall(used=()):
    f = back_view(VOLUMES_FRAME)
    volume(f, VOLUME_Y, apex=(0, 200))
    volume(f, VOLUME_X, apex=(0, 70))
    draw_holds(f, VOLUMES, used)
    start_tape(f, (-14, 116), (14, 116))
    return f


def volumes(out):
    f = volumes_wall()
    mark(f, dict(A=(15, 123), B=(24, 314), X=(46, 70), Y=(44, 214)), VOLUMES_NUMBERS)
    f.save(out + "/reading-v5-volumes.svg")

    f = volumes_wall(used=("A",))
    # the pose in compression() in figs_body.py, on the same volumes. The shoulders
    # stand well off the wall and the palms close to it, so the arms point partly
    # at the viewer.
    edge = norm(sub(VOLUME_X[0], VOLUME_X[1]))
    down = math.degrees(math.atan2(edge[1], edge[0]))
    toe = (-17.6, 75.3)                 # on the volume's upper face, inside its outline
    c = Climber((0, 130), lh=(-25, 198), rh=(25, 198),
                lf={"at": toe, "angle": down, "contact": "ball"},
                rf={"at": (-toe[0], toe[1]), "angle": 180 - down, "contact": "ball"},
                knees={"l": "out", "r": "out"}, elbows={"l": "down", "r": "down"},
                arm_len={"l": (.6, .9), "r": (.6, .9)},
                hand_style={"l": "open", "r": "open"}, active=("+llat", "+rlat"))
    c.draw(f)
    for side in (-1, 1):
        f.arrow([(side * 58, 196), (side * 38, 196)], kind="force")
        f.arrow([(side * 50, 93.5), (side * 34, 81.5)], kind="force")
    mark(f, {"B R3 L4": (39, 314), "Y L1": (-58, 176), "Y R2": (58, 176), "X": (46, 62)}, VOLUMES_NUMBERS)
    f.text("A", (-23, 113), size=6.8, weight=500)
    check("reading-v5-volumes-answer", c)
    f.save(out + "/reading-v5-volumes-answer.svg")


# ---------------------------------------------------------------- 8, cave


CAVE_FRAME = (-112, -8, 70, 336)
CAVE = {
    "A": shoe("jug", (-84, 138), use=180, size=1.2),
    "B": hand("crimp", (-40, 150), size=1.3, variant="rail"),
    "C": hand("crimp", (32, 196), use=45, w=11, h=6),
    "D": hand("jug", (-44, 246), use=135, size=.8, variant="flat"),
    "E": hand("crimp", (14, 300)),
    "F": hand("jug", (-16, 322), variant="bucket"),
    1: foot((2, 30), 1.15), 2: foot((26, 54), 1.15), 3: foot((46, 104)), 4: foot((48, 148)),
}
CAVE_NUMBERS = {1: (12, 31), 2: (36, 55), 3: (56, 105), 4: (58, 149)}


def cave_wall(used=()):
    f = back_view(CAVE_FRAME)
    draw_holds(f, CAVE, used)
    start_tape(f, (-50, 148), (44, 188))
    return f


def cave(out):
    f = cave_wall()
    mark(f, dict(A=(-73, 142), B=(-26, 151), C=(46, 197), D=(-31, 250), E=(26, 301), F=(-2, 324)),
         CAVE_NUMBERS)
    f.save(out + "/reading-v6-cave.svg")

    f = cave_wall(used=("A", "B", "C", "D", 3, 4))
    right_hand = grip(CAVE["C"]["pos"], use=45, kind="crimp", size=1.3)
    right_foot = stand(CAVE[3]["pos"])
    c = FootClimber((0, 150), lean=-12, bend=-6,
                    lh=grip(CAVE["D"]["pos"], use=135, size=.8), rh=right_hand,
                    lf={"at": add(CAVE["A"]["pos"], (-7.2, -1)), "angle": 88, "spot": "toptoe", "up": -1},
                    rf=right_foot, knees={"l": "up", "r": "out"}, elbows={"r": "down"}, head=(-3, 3),
                    leg_len={"l": .96}, active=("+lshin", "+rthigh"))
    c.draw(f)
    _hinge(f, right_hand, right_foot)
    number_with_leader(f, 4, (64, 170), (50, 151))
    mark(f, {"A toe": (-84, 156), "B": (-42, 166), "C": (46, 197), "D L1": (-24, 250),
             "E R2": (34, 301), "F R3 L4": (13, 324)}, {k: v for k, v in CAVE_NUMBERS.items() if k != 4})
    check("reading-v6-cave-answer", c)
    f.save(out + "/reading-v6-cave-answer.svg")


def build(out):
    slab(out)
    traverse(out)
    overhang(out)
    steep(out)
    sit_start(out)
    long_gap(out)
    volumes(out)
    cave(out)
