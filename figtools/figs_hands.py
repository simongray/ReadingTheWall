"""Figures for chapter 5, Hands and holds.

Every figure is written as <technique-key>.svg, plus a concept figure and
the hand-atlas plate. The hand close-ups and the plate's tiles come from
authored.py. Whole-climber figures use the mannequin from climb.py at the
book's standard scale (0.32 mm per cm).
"""

from climb import *
import hand as H
import plan

SKIN = dict(fill=WHITE, stroke=INK, sw=0.35)


def warn(name, *climbers):
    for c in climbers:
        for w in c.warn():
            print(name + ":", w)
            if DEBUG and "hand" in w:
                s = w[0]
                t = getattr(c, s + "h")
                reach = c.reach(s)
                print("   shoulder", tuple(round(v, 1) for v in c.J[s + "sh"]), "target", t,
                      "dist", round(length(sub(t, c.J[s + "sh"])), 1), "reach", reach)


DEBUG = False


def label_lines(f, lines, at, to=None, size=7, lead=None):
    """A label of several short lines centred under `at`; the leader (if
    any) leaves from the first line."""
    step = f.pt(size) * 1.15
    if to is not None:
        # start the leader at the edge of the first line (the width estimate
        # Fig.text uses), so it doesn't show through the gaps between words
        # (a leader heading down clears the lines below the first one too)
        v = norm(sub(to, at))
        down = v[1] < 0
        hw = max(len(s) for s in (lines if down else lines[:1])) * f.pt(size) * 0.53 / 2
        hh = f.pt(size) * 0.45 + (step * (len(lines) - 1) if down else 0)
        t = min(hw / max(abs(v[0]), 1e-6), hh / max(abs(v[1]), 1e-6)) + f.mm(0.5)
        f.label(lines[0], at, to=to, size=size, anchor="middle", gap=t * f.scale / 1.6)
    else:
        f.text(lines[0], at, size=size, z=60)
    for i, s in enumerate(lines[1:], 1):
        f.text(s, (at[0], at[1] - step * i), size=size, z=60)


# ---------------------------------------------------------------- climber figures


def jug_fig(path):
    J = (-8, 213.5)
    LF = (-32, 62)
    RF = (36, 48)       # low and wide: higher, the bent knee folds the ankle shut
    panels = []
    for good in (False, True):
        f = Fig(-80, 25, 80, 240)
        wall_grid(f)
        hold(f, "jug", J, size=1.3)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        g = grip(J, size=1.3)
        if not good:
            # dots on the upper arms only: the evidence behind this figure
            # shows the biceps and shoulders working harder, not the forearms
            c = Climber(None, shoulders=(-6, 166), lh=add(g, (-7, 0)), rh=add(g, (7, 0)),
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        elbows={"l": "out", "r": "out"},
                        leg_len={"l": .9, "r": .9}, active=("lupper", "rupper"))
            c.draw(f)
            f.label("arms bent", (58, 196), to=c.J["rel"])
        else:
            # the body sags off the one holding arm
            kw = dict(shoulders=(6, 154), lean=-6, bend=8, lh=g, lf={"at": stand(LF)},
                      rf={"at": stand(RF)}, leg_len={"l": .95, "r": .95})
            rsh = Climber(None, **kw).J["rsh"]
            hang = add(rsh, mul(ang(-68), 64.5))     # arm hangs straight, a little out
            c = Climber(None, rh=hang, elbows={"r": "out"}, **kw)
            c.draw(f)
            ha = c.J["rha"]
            for k in (-1, 1):
                f.smooth([add(ha, (k * 7, -5)), add(ha, (k * 9.5, -1)), add(ha, (k * 7, 3))],
                         closed=False, z=50, sw=0.35)
            f.label("shake out", (64, 152), to=add(ha, (3, 3)))
            f.label("straight arm", (-26, 188), to=lerp(c.J["lsh"], c.J["lel"], 0.5))
        f.cog(c.cog(), plumb_to=45)
        warn("jug", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["bent arms: biceps work", "straight arm, other hand rests"])


def sidepull_fig(path):
    S = (-40, 188)       # left-hand sidepull facing left (away from the body)
    T = (46, 218)
    LF = (-36, 60)
    RF = (40, 58)
    panels = []
    for good in (False, True):
        f = Fig(-85, 25, 85, 245)
        wall_grid(f)
        hold(f, "jug", S, use=180)
        hold(f, "jug", T)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        g = grip(S, use=180)
        if not good:
            # hips under the hold, arm bent: the body swings open
            kw = dict(shoulders=(-16, 163), lh=g, lf={"at": stand(LF), "angle": 198},
                      rf={"at": stand(RF)}, elbows={"l": "out", "r": "out"},
                      knees={"l": "out", "r": "out"}, leg_len={"l": .9, "r": .95})
            rsh = Climber(None, **kw).J["rsh"]
            # the free hand still short of the jug, and not working
            c = Climber(None, rh=add(rsh, mul(norm(sub(grip(T), rsh)), 58)),
                        active=("-rupper", "-rfore"), **kw)
            c.draw(f)
            f.turn(add(c.pelvis, (4, 26)), 36, -8, -172)
            f.label("swings open", (52, 128), size=7.5)
        else:
            # the left arm hangs straight and the right hand has only just
            # reached the jug: the left leg, pushing left, does the work
            # the body bows away from the sidepull
            c = Climber((41, 119), lean=-14, bend=8, lh=g, rh=grip(T),
                        lf={"at": stand(LF)}, rf={"at": stand(RF), "angle": -30},
                        elbows={"l": "down", "r": "out"},
                        leg_len={"l": 1.0, "r": .95}, active=("lthigh",))
            c.draw(f)
            f.arrow([add(g, (12, 6)), add(g, (30, 6))], kind="force")
            f.arrow([add(stand(LF), (-8, 6)), add(stand(LF), (-26, 6))], kind="force")
            f.label("lean away", (-40, 148), to=lerp(c.J["lsh"], c.J["lel"], 0.5))
            f.label("foot pushes left", (-46, 50), size=7.5)
        f.cog(c.cog(), plumb_to=48)
        warn("sidepull", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["under the hold: barn door", "body right of it, leaning away"])


def _gaston_plan(f):
    """A small top-down inset of a gaston with the right hand: the wall at the
    top, the elbow out to the side and the forearm coming back to the hold,
    which the hand pushes away from the body."""
    view = plan.View((28, 54), 0.5)
    plan.wall(f, view.P((-22, 34)), view.P((62, 34)))
    plan.hold_on(f, view, (34, 34), w=13, d=4)
    plan.climber(f, view, -10, lean=(4, -18), arms={"r": dict(hand=(32, 27), elbow=(40, -6))})
    f.arrow([view.P((44, 16)), view.P((64, 16))], kind="force", z=73)
    f.text("from above", (38, 33), size=plan.INSET_LABEL)


def gaston_fig(path):
    H = (0, 172)         # one hold, its gripping surface facing left
    panels = []
    for kind in ("sidepull", "gaston"):
        # the panels show the same width, each round its own climber
        f = Fig(-85, 25, 85, 245) if kind == "sidepull" else Fig(-92, 25, 78, 245)
        wall_grid(f)
        hold(f, "jug", H, use=180)
        g = grip(H, use=180)
        if kind == "sidepull":
            T = (60, 222)
            LF, RF = (-6, 72), (46, 64)
            hold(f, "jug", T)
            hold(f, "foot", LF)
            hold(f, "foot", RF)
            c = Climber((40, 116), lean=-18, bend=8, lh=g, rh=grip(T),
                        lf={"at": stand(LF)}, rf={"at": stand(RF), "angle": -30},
                        elbows={"l": "down"}, leg_len={"l": .95, "r": .9})
            c.draw(f)
            f.arrow([add(g, (-4, 14)), add(g, (14, 14))], kind="force")
            f.label("body right of it", (40, 34), size=7.5)
        else:
            # right hand in front of the right shoulder, thumb down, the
            # elbow out to the side and about level with the hand, as the
            # entry asks
            T = (-66, 222)
            LF, RF = (-60, 70), (2, 62)
            hold(f, "jug", T)
            hold(f, "foot", LF)
            hold(f, "foot", RF)
            # the gaston arm (drawn by draw_arm, so not in the default)
            # pushes, and the left foot pushes back
            c = Climber(None, shoulders=(-34, 166), lh=grip(T), rh=None,
                        lf={"at": stand(LF), "angle": 190}, rf={"at": stand(RF)},
                        elbows={"l": "out"}, leg_len={"l": .93, "r": .95},
                        order=["lleg", "rleg", "torso", "larm"],
                        active=("+rupper", "+rfore", "+lthigh"))
            c.draw(f)
            el = (12, 164)
            c.draw_arm(f, "r", el, g, z=4)
            f.arrow([add(g, (5, 12)), add(g, (24, 12))], kind="force")
            f.label("elbow out", (33, 142), to=add(el, (2, -2)))
            f.arrow([add(stand(LF), (-8, 6)), add(stand(LF), (-26, 6))], kind="force")
            f.label("body left of it", (-30, 34), size=7.5)
            # from behind, the forearm points into the wall and shows only
            # as a stub, so an inset shows the arm from above
            _gaston_plan(f)
        f.cog(c.cog(), plumb_to=52)
        warn("gaston", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["used as a sidepull", "used as a gaston"])


def undercling_fig(path):
    WX = 30
    panels = []
    for good in (False, True):
        f = Fig(-95, 20, 50, 255)
        at = wall_side(f, WX, 20, 255, angle=0)
        U = at(214 if not good else 132)
        hand = on_hold(U, 0, 5.0, -4.6)
        if not good:
            hold_side(f, "undercling", U)
            F1 = at(42)
            hold_side(f, "foot", F1)
            foot = add(F1, (-2.5, 2.5))
            c = Climber(None, shoulders=(-14, 170), view="side", lean=0,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        elbows={"l": "down", "r": "down"},
                        knees={"l": "up", "r": "up"})
            c.draw(f)
            f.turn((-34, 140), 24, 30, 150)
            f.label("tips backwards", (-64, 182), size=7.5)
            f.label("bent arms", (-30, 240), to=lerp(c.J["rel"], c.J["rha"], 0.55))
        else:
            # the hold sits beside the right knee, nearer to you than it
            hold_side(f, "undercling", U, z=3.5)
            F1 = at(88)
            hold_side(f, "foot", F1)
            foot = add(F1, (-2.5, 2.5))
            T = at(238)
            hold_side(f, "jug", T)
            kw = dict(shoulders=(-29, 161), view="side", lean=-20, rh=hand,
                      lf={"at": foot}, rf={"at": foot})
            sh = Climber(None, **kw).J["lsh"]
            reach_to = add(sh, mul(norm(sub(add(T, (-4, -2)), sh)), 60))
            # the legs stand up into the hold (the left thigh is hidden)
            c = Climber(None, lh=reach_to, active=("+rthigh",), **kw)
            c.draw(f)
            f.arrow([add(c.J["lha"], (2, 4)), add(T, (-4, -2))], kind="move")
            # the pull, up and out along the straight arm, beside it so that the
            # hand stays in view; the feet push into the wall, from behind the heel
            u = norm(sub(c.J["rsh"], hand))
            n = rot(u, -90)
            f.arrow([add(add(hand, mul(u, 12)), mul(n, 8)), add(add(hand, mul(u, 28)), mul(n, 8))],
                    kind="force", z=50)
            f.arrow([add(foot, (-39, -2)), add(foot, (-25, -2))], kind="force")
            f.label("arm straight", (-36, 120), to=lerp(c.J["rsh"], hand, 0.5))
            f.label("feet up", (-64, 70), to=c.J["ran"])
        f.cog(c.cog(), plumb_to=35)
        warn("undercling", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["hold above the head", "feet up, hold at the waist"])


def sloper_fig(path):
    A = 20
    panels = []
    for good in (False, True):
        f = Fig(-104, 20, 54, 260)
        at = wall_side(f, 38, 20, 260, angle=A)
        S = at(208)
        hold_side(f, "sloper", S, angle=A, size=1.4)
        hand = on_hold(S, A, 4.6, 7.6)
        if not good:
            Fh = at(140)
            hold_side(f, "foot", Fh, angle=A)
            fh = on_hold(Fh, A, 2.6, 2.4)
            c = Climber((-68, 148), view="side", lean=10, lh=hand, rh=hand,
                        lf={"at": fh, "angle": A}, rf={"at": fh, "angle": A})
            c.draw(f)
            f.text("hand", (-70, 255), size=7.5, z=60)
            f.label("rolls off", (-70, 255 - f.pt(7.5) * 1.15), to=add(hand, (-3, 3)),
                    anchor="middle")
            # low on the right, clear of the wall; the plumb line stops above
            # the label under the arrow
            f.label("both feet high", (-24, 70), to=add(fh, (-3, -2)))
            f.body_arrow([(-44, 132), (-74, 128)], width=2.4)
            f.label("hips pushed out", (-70, 104), size=7.5)
        else:
            Fh, Fl = at(102), at(44)
            hold_side(f, "foot", Fh, angle=A)
            hold_side(f, "foot", Fl, angle=A)
            fh = on_hold(Fh, A, 2.6, 2.4)
            fl = on_hold(Fl, A, 2.6, 2.4)
            c = Climber((-42, 102), view="side", lean=0, lh=hand, rh=hand,
                        lf={"at": fl, "angle": A}, rf={"at": fh, "angle": A},
                        leg_len={"r": 0.85})
            c.draw(f)
            label_lines(f, ["arm", "straight"], (-62, 208), to=lerp(c.J["rsh"], hand, 0.5),
                        size=7.5)
            label_lines(f, ["hips low,", "under it"], (-76, 74), to=add(c.pelvis, (-6, -4)),
                        size=7.5)
            f.label("one foot low", (19, 30), to=add(fl, (-3, -2)), anchor="end")
        f.cog(c.cog(), plumb_to=28 if good else 116)
        warn("sloper", c)
        panels.append(f)
    import authored
    panels.append(authored.sloper_panel())
    combine(panels, path, gap=4, labels=["a", "b", "c"],
            captions=["hips up and out: it rolls off", "hips low: it holds",
                      "hand draped over it"])


def palming_fig(path):
    f = Fig(-90, 28, 90, 245)
    wall_grid(f)
    outline = [(16, 90), (78, 90), (78, 152), (16, 152)]
    volume(f, outline, apex=(47, 121))
    T = (-46, 226)
    hold(f, "jug", T)
    LF = (-30, 62)
    RF0 = (14, 46)
    RF1 = (2, 96)
    hold(f, "foot", LF)
    hold(f, "foot", RF0)
    hold(f, "foot", RF1)
    palm = (34, 140)
    # the right side shortens over the pressing palm
    c = Climber((-8, 124), lean=-8, bend=6, lh=grip(T), rh=palm,
                lf={"at": stand(LF)}, rf={"at": stand(RF0)},
                elbows={"r": "down", "l": "out"}, hand_style={"r": "open"},
                leg_len={"l": .95, "r": .9})
    c.draw(f)
    f.arrow([add(palm, (7, 2)), add(palm, (22, -10))], kind="force")
    f.arrow([add(stand(RF0), (-6, 8)), (1, 91)], kind="move")
    label_lines(f, ["palm presses", "down-right"], (50, 76), to=add(palm, (1, -3)), size=7.5)
    f.label("right foot goes up", (-48, 36), to=(4, 64))
    f.cog(c.cog(), plumb_to=45)
    warn("palming", c)
    f.save(path)


def mantle_fig(path):
    TOP = 200
    WX = 30
    frames = []
    for k in range(3):
        # (the low foothold sits high enough that the figure fits under the steps)
        f = Fig(-75, 66, 70, 297)
        at = wall_side(f, WX, 66, TOP, angle=0)
        f.poly([(WX, TOP), (70, TOP), (70, TOP - f.mm(2.4)), (WX, TOP - f.mm(2.4))],
               z=-21, fill=PALE, stroke=None)
        f.line((WX, TOP), (70, TOP), z=-19, sw=0.6)
        Fh, Fl = at(TOP - 92), at(TOP - 122)
        hold_side(f, "foot", Fh)
        hold_side(f, "foot", Fl)
        foot_h = add(Fh, (-2.5, 2.5))
        foot_l = add(Fl, (-2.5, 2.5))
        lip = (WX + 1, TOP + 1.5)
        if k == 0:
            # the arms pull, though not yet bent far enough for the default
            # (the left arm is hidden behind the right). The hips stay back
            # and the chest upright, so the high knee has room
            c = Climber((-20, 118), view="side", lean=6, lh=lip, rh=lip,
                        lf={"at": foot_l}, rf={"at": foot_h},
                        leg_len={"r": 0.85}, active=("+rupper", "+rfore"))
            c.draw(f)
        elif k == 1:
            palm = (WX + 7, TOP)
            flat_palm(f, palm)
            # shoulders over the lip and above the palm, so the bent elbow
            # points up and back, as the caption says
            c = Climber(None, shoulders=(33, 227), view="side", lean=30, bend=8, lh=lip,
                        rh=add(palm, (-1, 3)),
                        lf={"at": (6, 88), "angle": -40}, rf={"at": foot_h},
                        leg_len={"r": 0.8})
            c.draw(f)
            f.arrow([add(palm, (1, 16)), add(palm, (1, 5))], kind="force")
            f.label("palm flat, elbow up", (-34, 268), to=c.J["rel"])
            f.body_arrow([(-22, 146), (-14, 182)], width=2.2)
        else:
            palm = (WX + 8, TOP)
            palm2 = (WX + 16, TOP)
            flat_palm(f, palm)
            flat_palm(f, palm2, z=-1)
            # both arms straight, the shoulders over the hands and the hips at
            # the lip, so the weight is over the hands and the high foot; the
            # other leg hangs down the wall, its knee below the top
            c = Climber((26, 226), view="side", lean=26, bend=4,
                        lh=add(palm2, (-1, 3)), rh=add(palm, (-1, 3)),
                        lf={"at": (WX - 4, 125), "angle": -20, "contact": "ball"},
                        rf={"at": (WX + 13, TOP + 1), "angle": -20, "contact": "ball"},
                        leg_len={"r": 0.85},
                        active=("+rthigh",))   # the right leg steps up
            c.draw(f)
            f.label("arms straight", (-36, 268), to=lerp(c.J["rsh"], c.J["rha"], 0.45))
            label_lines(f, ["foot on top,", "no knee"], (-22, 182), to=c.J["ran"], size=7.5)
        f.cog(c.cog())
        warn("mantle %d" % k, c)
        frames.append(f)
    combine(frames, path, gap=4, labels=["1", "2", "3"],
            captions=["pull, foot high", "flip one hand, press", "press out, step up"])


def volume_mantle_fig(path):
    WX = 45
    panels = []
    for k in (0, 1):
        f = Fig(-95, 30, 65, 280)
        at = wall_side(f, WX, 30, 280, angle=0)
        p0, p2, p1 = volume_side(f, at(120), 26, 60, angle=0, top=0.95)
        T = at(262)
        hold_side(f, "jug", T)
        Fh, Fl = at(95.5), at(55.5)
        hold_side(f, "foot", Fh)
        hold_side(f, "foot", Fl)
        foot_h = add(Fh, (-2.5, 2.5))
        foot_l = add(Fl, (-2.5, 2.5))
        edge = add(p2, (1, 2.5))
        palm = (WX - 16, p2[1] + 4.5)
        if k == 0:
            # head back from the hands, so the pull and the face don't overlap
            c = Climber((-16, 120), view="side", lean=4, lh=edge, rh=edge,
                        lf={"at": foot_l}, rf={"at": foot_h})
            c.draw(f)
            f.label("pull on the edge", (-4, 224), to=add(edge, (-1, 2)))
            f.label("foot high", (-50, 70), to=c.J["ran"])
        else:
            flat_palm(f, add(palm, (0, -3.2)), length_=8, fill=LEFT)
            sh = (6 + math.sin(math.radians(5)) * 47, 172 + math.cos(math.radians(5)) * 47)
            aim = add(T, (-4, -2))
            reach_to = add(sh, mul(norm(sub(aim, sh)), 36))
            # the palm presses and the legs rock over onto the high foot
            # (the left thigh is hidden behind the right)
            c = Climber((6, 172), view="side", lean=1, bend=8, lh=add(palm, (0, 1.5)), rh=reach_to,
                        lf={"at": foot_h}, rf={"at": foot_h},
                        leg_len={"l": 0.85, "r": 0.85}, active=("+rthigh",))
            c.draw(f)
            u = norm(sub(aim, c.J["rha"]))
            f.arrow([add(c.J["rha"], mul(u, 6)), sub(aim, mul(u, 2))], kind="move")
            f.arrow([add(palm, (0, 16)), add(palm, (0, 5))], kind="force")
            label_lines(f, ["palm presses", "the top"], (-66, 238), to=add(palm, (-2, 2)),
                        size=7.5)
            f.body_arrow([(-26, 140), (-16, 172)], width=2.2)
        f.cog(c.cog())
        warn("volume mantle %d" % k, c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["pull on the edge, foot up", "press the top, reach"])


def wall_frame(angle):
    """Up-the-wall and out-of-the-wall unit vectors for a side-view wall."""
    d = norm((-math.tan(math.radians(angle)), 1))
    n = (-d[1], d[0])
    return d, n


def on_hold(pos, angle, x, y):
    """A point in a side-view hold's own frame: x out of the wall, y up it."""
    d, n = wall_frame(angle)
    return add(pos, add(mul(n, x), mul(d, y)))


def flat_palm(f, at, length_=9.0, z=60, fill=WHITE):
    """A palm pressed flat on a horizontal surface, seen from the side, in the
    grey of the limb it belongs to."""
    f.poly(capsule(add(at, (-length_ / 2, 1.6)), 1.7, add(at, (length_ / 2, 1.6)), 1.4),
           z=z, **dict(SKIN, fill=fill))


# ---------------------------------------------------------------- hand atlas
#
# A reference plate of one small close-up per grip, in two rows of five. It's smaller than
# the close-ups, so that it fits beside the chapter's opening text in the text width.

ATLAS_ZOOM = 0.73


def grid(rows, path, gap=3.0, row_gap=1.5, zoom=1.0):
    """Lay out figures in centred rows, each with a caption under it, the
    drawings scaled by `zoom` (the captions keep their size).
    rows: lists of (figure, caption)."""
    cap_h = 5.0
    widths = [sum((f.x1 - f.x0) * f.scale * zoom for f, _ in r) + gap * (len(r) - 1)
              for r in rows]
    W = max(widths)
    out, y, n = [], 0.0, 0
    for r, w in zip(rows, widths):
        x = (W - w) / 2
        h = max((f.y1 - f.y0) * f.scale * zoom for f, _ in r)
        for f, cap in r:
            fw, fh, s = f.x1 - f.x0, f.y1 - f.y0, f.scale * zoom
            inner = f.svg().split("\n", 1)[1].rsplit("</svg>", 1)[0]
            out.append(f'<clipPath id="g{n}"><rect x="0" y="0" width="{fw:.2f}" '
                       f'height="{fh:.2f}"/></clipPath>')
            out.append(f'<g transform="translate({x:.2f},{y + h - fh * s:.2f}) '
                       f'scale({s:.5f})"><g clip-path="url(#g{n})">{inner}</g></g>')
            out.append(f'<text x="{x + fw * s / 2:.2f}" y="{y + h + 3.8:.2f}" '
                       f'font-family="{FONT}" font-size="2.9" font-weight="500" '
                       f'text-anchor="middle">{esc(cap)}</text>')
            x += fw * s + gap
            n += 1
        y += h + cap_h + row_gap
    H_ = y - row_gap
    with open(path, "w") as fh_:
        fh_.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
                  f'height="{H_:.2f}mm" viewBox="0 0 {W:.2f} {H_:.2f}">\n'
                  + "\n".join(out) + "\n</svg>\n")


def hand_atlas_fig(path):
    import authored as A
    # the hand's line stays the climbers' weight though the plate is reduced
    H.LINE[0] = 1 / ATLAS_ZOOM
    rows = A.atlas_rows()
    H.LINE[0] = 1.0
    grid(rows, path, zoom=ATLAS_ZOOM)


# ---------------------------------------------------------------- build


def build(out):
    import authored as A
    A.hold_angle_fig(out + "/hands-hold-angle.svg")
    jug_fig(out + "/jug.svg")
    A.open_hand_fig(out + "/open-hand.svg")
    A.half_crimp_fig(out + "/half-crimp.svg")
    A.full_crimp_fig(out + "/full-crimp.svg")
    A.pinch_fig(out + "/pinch.svg")
    sloper_fig(out + "/sloper.svg")
    A.pocket_fig(out + "/pocket.svg")
    sidepull_fig(out + "/sidepull.svg")
    gaston_fig(out + "/gaston.svg")
    undercling_fig(out + "/undercling.svg")
    palming_fig(out + "/palming.svg")
    mantle_fig(out + "/mantle.svg")
    volume_mantle_fig(out + "/volume-mantle.svg")
    A.thumb_catch_fig(out + "/thumb-catch.svg")
    A.wrap_fig(out + "/wrap.svg")
    A.regrip_fig(out + "/regrip.svg")
    hand_atlas_fig(out + "/hand-atlas.svg")
    A.filmstrip_fig(out + "/filmstrip-sloper.svg")


if __name__ == "__main__":
    import sys
    build(sys.argv[1])
