"""The key to the illustrations, shown in the introduction."""

from climb import *


def legend(path):
    # (inside the measure, and tall enough for the key's rows to stay apart)
    f = Fig(-96, -8, 361, 272)
    wall_grid(f, x0=-88, x1=80, y0=44)
    # a climber with a ghost of the earlier position: the right hand has
    # moved from the lower hold to the higher one. Only the arm that moved
    # is a ghost; a whole ghost body this close would merge with the climber.
    # The lower hold sits out to the side, about an arm's length from the
    # shoulder, so the ghost is a whole, nearly straight arm clear of the
    # torso (with the hold by the waist, only a forearm showed).
    LH, R0, R1 = (-30, 222), (70, 146), (36, 240)
    LF, RF = (-30, 64), (30, 70)
    hold(f, "jug", LH)
    hold(f, "jug", R0)
    hold(f, "jug", R1)
    hold(f, "foot", LF)
    hold(f, "foot", RF)
    body = dict(lean=-4, lh=grip(LH), lf={"at": stand(LF)}, rf={"at": stand(RF)},
                head=(2, 2))
    g = Climber((4, 142), rh=grip(R0), elbows={"r": "down", "l": "down"},
                order=["rarm"], **body)
    g.draw(f, ghost=True)
    c = Climber((4, 142), rh=grip(R1), elbows={"l": "down"}, **body)
    c.draw(f, z=5)
    f.arrow([add(R0, (4, 10)), (62, 214), add(R1, (12, -4))], kind="move")
    # Both sleeves are white, so the labels name the arm and leg and the
    # left leader points at the shaded forearm, below the sleeve. Short
    # lines keep them clear of the frame edge and of the key.
    f.label("left arm", (-48, 176), to=add(lerp(c.J["lel"], c.J["lwr"], 0.4), (-2, 0)), anchor="end")
    for i, s in enumerate(("and leg", "shaded")):
        f.text(s, (-48, 166 - 10 * i), size=7.5, anchor="end")
    # the leader rises to the thigh, clear of the lines below
    f.label("right arm", (68, 96), to=add(lerp(c.J["rhip"], c.J["rkn"], 0.65), (3, 0)))
    for i, s in enumerate(("and leg", "white")):
        f.text(s, (68, 86 - 10 * i), size=7.5, anchor="start")
    for w in c.warn() + g.warn():
        print("legend:", w)

    # the key
    rows = [
        ("hold", "Hold. The white lip marks the surface you grab"),
        ("foot", "Foothold"),
        ("xray", "Dotted outline: hidden behind a limb"),
        ("volume", "Volume (a large bolt-on shape)"),
        ("wall", "Wall seen from the side; the climber faces it"),
        ("move", "A hand or foot travels this way"),
        ("body", "The hips or the whole body move this way"),
        ("force", "Force: where you push or pull"),
        ("turn", "Rotation (e.g. the body swinging open)"),
        ("hinge", "Hinge: the line the body can swing around"),
        ("cog", "Centre of gravity, with a plumb line"),
        ("ghost", "Earlier position"),
        ("step", "Order of moves"),
        ("cross", "Mistake or position to avoid"),
    ]
    x0, y = 116, 262
    for kind, text in rows:
        sx = x0 + 18
        if kind == "hold":
            hold(f, "jug", (sx, y))
        elif kind == "foot":
            hold(f, "foot", (sx, y))
        elif kind == "xray":
            # a hand over a jug: the covered part of the hold shows dotted
            hold(f, "jug", (sx, y + 1), size=1.15)
            wr, ha = (sx + 3, y - 3), (sx + 1, y + 4)
            silhouette(f, [limb_outline((sx + 6, y - 9), 2.8, wr, 2.6),
                           limb_outline(wr, 2.6, ha, 3.6)], z=1, fill=WHITE)
        elif kind == "volume":
            volume(f, [(sx - 15, y - 7), (sx + 15, y - 7), (sx, y + 8)],
                   apex=(sx + 2, y - 2))
        elif kind == "wall":
            wall_side(f, sx + 4, y - 8, y + 8, angle=0)
        elif kind == "move":
            f.arrow([(sx - 16, y), (sx + 16, y)], kind="move")
        elif kind == "body":
            f.body_arrow([(sx - 16, y), (sx + 17, y)], width=1.8)
        elif kind == "force":
            f.arrow([(sx - 16, y), (sx + 16, y)], kind="force")
        elif kind == "turn":
            f.turn((sx, y - 4), 9, 160, 20)
        elif kind == "hinge":
            f.line((sx - 16, y), (sx + 16, y), sw=0.45, dash=(2.2, 1.2))
        elif kind == "cog":
            f.cog((sx, y + 3), plumb_to=y - 8)
        elif kind == "ghost":
            f.poly(capsule((sx - 14, y), 4.5, (sx + 14, y), 3.5), fill=WHITE,
                   stroke=MID, sw=0.3, dash=(0.9, 0.7))
        elif kind == "step":
            f.step(1, (sx - 8, y))
            f.step(2, (sx + 8, y))
        elif kind == "cross":
            f.cross((sx, y))
        # (the frame is cut to these lines, wider in this estimate than in fact)
        f.text(text, (x0 + 46, y), size=8, anchor="start", halo=False, keep_in=False)
        y -= 20
    f.save(path)


def build(out):
    legend(out + "/legend.svg")
