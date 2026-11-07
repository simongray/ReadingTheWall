"""Figures for the foundations chapter: the mechanics behind every technique."""

from climb import *
import figs_body as fb


def straight_arms(path):
    """Side view on a 20 degree overhang, same holds in both panels: (a) on
    bent arms the arm muscles hold the body up; (b) on straight arms the elbow
    muscles rest while the bent legs push."""
    panels = []
    for bent in (True, False):
        f = Fig(-104, 50, 66, 236)
        at = wall_side(f, 55, 50, 236, angle=20)
        H = at(205)
        F = at(95)
        hold_side(f, "jug", H, angle=20)
        hold_side(f, "foot", F, angle=20)
        hand = add(H, (-3.5, 2))
        foot = add(F, (-2.5, 2.5))
        if bent:
            # dots on the upper arm only: the evidence behind this figure
            # shows the biceps and shoulder working harder, not the forearm
            c = Climber(None, shoulders=add(hand, (-34, -32)), view="side", lean=-4,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        head=(1, 1), active=("rupper",))
        else:
            # the head tips back, out from behind the straight arm, and stays
            # up off the shoulder: this is no shrugged hang. The left thigh,
            # behind the right, would show no dots
            c = Climber(None, shoulders=add(hand, (-38, -52)), view="side", lean=6,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        head=(-8, 5), active=("rthigh",),
                        bend=10)        # hanging back, the back rounds
        c.draw(f)
        sh = c.J["rsh"]
        if bent:
            # the leader ends on the upper arm, where the biceps is, not on
            # the elbow joint, and comes down between face and forearm
            f.label("biceps working", (-16, 225), to=lerp(sh, c.J["rel"], 0.7), anchor="end")
        else:
            f.label("elbow muscles rest", (-22, 206), to=lerp(sh, c.J["rha"], 0.5), anchor="end")
            f.label("legs push", (-70, 66), to=c.J["rkn"])
        for w in c.warn():
            print("straight-arms:", w)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["bent arms: arm muscles work", "straight arms: muscles work less"])


def hips_in(path):
    """Side view, 30 degree overhang, same holds in both panels: (a) hips
    sagging out, the plumb line far from the feet; (b) hips in, the plumb
    line moves toward the feet."""
    panels = []
    for good in (False, True):
        f = Fig(-132, 40, 64, 240)
        at = wall_side(f, 60, 40, 240, angle=30)
        H = at(210)
        F = at(100)
        hold_side(f, "jug", H, angle=30)
        hold_side(f, "foot", F, angle=30)
        hand = add(H, (-3.5, 2))
        foot = add(F, (-2.5, 2.5))
        if good:
            # the hips press in and the lower back arches a little
            c = Climber(None, shoulders=add(hand, (-38, -50)), view="side", lean=-36,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        head=(1, 1), bend=-8)
        else:
            # the hips sag out and the back rounds
            c = Climber(None, shoulders=add(hand, (-30, -58)), view="side", lean=8,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        head=(-7, 0), bend=8)
        c.draw(f)
        g = c.cog()
        f.cog(g, plumb_to=50)
        if good:
            f.body_arrow([add(g, (-44, -2)), add(g, (-16, -2))])
        for w in c.warn():
            print("hips-in:", w)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["hips out: arms carry you", "hips in: feet carry you"])


def barn_door(path):
    """Back view, the same holds as the back-flag figure. The left hand and
    left foot make a vertical hinge. (a) The right hand lets go to reach:
    the CoG hangs right of the hinge and the body swings open (inset from
    above). (b) Fixed with a back flag: the right leg crosses behind the
    left and presses the wall on the far side of the hinge; the hips move
    over the left foot, so the CoG sits on the hinge."""
    LH = (-36, 262)    # sidepull facing left: the body hangs to its right
    LF = (-30, 70)
    T = (36, 238)
    panels = []
    for fixed in (False, True):
        f = Fig(-100, 50, 80, 276)
        wall_grid(f)
        hold(f, "jug", LH, use=180)
        hold(f, "jug", T)
        hold(f, "foot", LF)
        fb._hinge(f, add(grip(LH, use=180), (0, -6)), stand(LF), ext=12)
        if not fixed:
            # the right hand has just let go: it never gets to the hold.
            # The body sags right, away from the one hand that holds, the
            # left side stretched
            c = Climber((-16, 154), turn=-0.35, lean=4, bend=8, lh=grip(LH, use=180),
                        rh=add(grip(T), (-8, -28)),
                        lf={"at": stand(LF), "style": "back"},
                        rf={"at": (-4, 72), "angle": -85, "contact": "toe"},
                        knees={"l": "out", "r": "right"}, elbows={"l": "down"},
                        head=(2, 1), active=("-rupper", "-rfore"))
            c.draw(f)
            f.cog(c.cog(), plumb_to=58)
            f.cross(add(T, (0, -13)))
            fb._door(f, (58, 178), w=40)
            f.label("hinge", (-74, 250), to=(-39, 236))
        else:
            c = fb._back_flagger(LH, LF, T)
            c.draw(f)
            f.cog(c.cog(), plumb_to=58)
            f.label("right leg behind", (14, 70),
                    to=add(lerp(c.J["rkn"], c.J["ran"], 0.3), (2, 0)))
        for w in c.warn():
            print("barn-door:", w)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["barn door", "fixed with a back flag"])


def balance(path):
    """Back view, vertical wall. (a) Hips centred: the plumb line falls
    between the feet, which share the weight. (b) The hips have moved over
    the left foot (block arrow): the plumb line falls on it, and the right
    foot is free to step up to the higher foothold (dashed arrow)."""
    LH, RH = (-30, 242), (30, 242)
    LF, RF = (-30, 62), (32, 66)
    F2 = (36, 110)
    panels = []
    for shifted in (False, True):
        f = Fig(-84, 48, 84, 260)
        wall_grid(f)
        hold(f, "jug", LH)
        hold(f, "jug", RH)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        hold(f, "foot", F2)
        if not shifted:
            c = Climber((0, 140), lh=grip(LH), rh=grip(RH),
                        lf={"at": stand(LF)}, rf={"at": stand(RF)})
            c.draw(f)
            f.cog(c.cog(), plumb_to=58)
        else:
            # the left arm bends only because the hips moved: the feet
            # carry the weight and the hands just steady it. The free right
            # hip drops and the chest bends back over the left hip, so the
            # shoulders stay level
            c = Climber((-22, 146), lean=10, bend=-8, lh=grip(LH), rh=grip(RH),
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        knees={"r": "out"}, active=())
            c.draw(f)
            f.cog(c.cog(), plumb_to=58)
            f.body_arrow([(36, 160), (8, 160)], width=1.8)
            f.arrow([add(stand(RF), (12, 4)), add(stand(F2), (12, 2))], kind="move")
            f.label("right foot free", (54, 138), to=add(stand(F2), (14, 4)), size=6.5)
        for w in c.warn():
            print("balance:", w)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["hips centred: weight split", "hips over the left foot"])


def filmstrip_hips_first(path):
    """In motion: hips first, then the foot. Back view, vertical wall, the
    hands stay on two jugs until the last frame. (1) Centred, weight split.
    (2) The hips slide over the left foot (plumb line on it). (3) The light
    right foot steps up to a higher hold. (4) The hips slide across over the
    new foot. (5) Stand up on it; only now the right hand goes up."""
    LH, RH, T = (-24, 244), (24, 244), (38, 280)
    LF, RF, F2 = (-24, 60), (24, 64), (26, 92)
    # every knee bends out, the way its toes point. With the hips over one
    # foot the free hip drops and the chest bends back over the standing
    # hip, as in the balance figure; reaching up, the right side stretches
    out = {"l": "out", "r": "out"}
    poses = [
        dict(P=(0, 142), rh=grip(RH), lf={"at": stand(LF)}, rf={"at": stand(RF)}),
        dict(P=(-14, 146), lean=8, bend=-6, rh=grip(RH), lf={"at": stand(LF)},
             rf={"at": stand(RF)}),
        dict(P=(-14, 146), lean=8, bend=-6, rh=grip(RH), lf={"at": stand(LF)},
             rf={"at": stand(F2)}),
        dict(P=(12, 150), lean=-8, bend=6, rh=grip(RH), lf={"at": stand(LF)},
             rf={"at": stand(F2), "angle": -10}, leg_len={"r": 0.92}),
        dict(P=(16, 172), lean=1, bend=-6, rh=grip(T),
             lf={"at": (-14, 104), "angle": 190, "contact": "ball"},
             rf={"at": stand(F2)}, active=("rthigh",)),
    ]
    frames = []
    for k, p in enumerate(poses):
        f = Fig(-54, 46, 58, 290, scale=0.28)
        wall_grid(f)
        for h in (LH, RH, T):
            # in the last frame the empty right-hand jug sits behind the
            # head: its hidden outline would only add clutter
            hold(f, "jug", h, xray=False if (k == 4 and h == RH) else None)
        for h in (LF, RF, F2):
            hold(f, "foot", h)
        kw = {k_: v for k_, v in p.items() if k_ != "P"}
        # the feet carry the weight and the hands only steady it, until the
        # right leg stands up in the last frame
        kw.setdefault("active", ())
        c = Climber(p["P"], lh=grip(LH), elbows=out, knees=out, head=(0, 1), **kw)
        c.draw(f)
        f.cog(c.cog(), plumb_to=54)
        pv = c.pelvis
        if k == 1:
            f.body_arrow([(pv[0] + 40, pv[1] + 14), (pv[0] + 18, pv[1] + 14)], width=1.6)
        elif k == 2:
            f.arrow([add(stand(RF), (14, 4)), add(stand(F2), (14, 2))], kind="move")
        elif k == 3:
            f.body_arrow([(pv[0] - 38, pv[1] + 14), (pv[0] - 18, pv[1] + 14)], width=1.6)
        elif k == 4:
            # raised clear of the left thigh, below the bent left arm
            f.body_arrow([(pv[0] - 36, pv[1] - 4), (pv[0] - 36, pv[1] + 30)], width=1.6)
            f.arrow([add(RH, (16, 4)), add(T, (16, -6))], kind="move")
        for w in c.warn():
            print("filmstrip-hips-first:", w)
        frames.append(f)
    filmstrip(frames, path, captions=["centred: weight split",
                                      "hips over the left foot",
                                      "step the light foot up",
                                      "hips over the new foot",
                                      "stand up, then reach"])


def build(out):
    straight_arms(out + "/concept-straight-arms.svg")
    hips_in(out + "/concept-hips-in.svg")
    barn_door(out + "/concept-barn-door.svg")
    balance(out + "/concept-balance.svg")
    filmstrip_hips_first(out + "/filmstrip-hips-first.svg")
