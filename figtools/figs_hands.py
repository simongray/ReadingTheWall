"""Figures for chapter 5, Hands and holds.

Every figure is written as <technique-key>.svg, plus a concept figure and
the hand-atlas plate. Close-ups of hands all use the one hand model in
hand.py at its fixed close-up scale (HAND_SCALE, 2.6 mm per cm), so every
hand in the book has the same size and proportions; whole-climber figures
use the mannequin from climb.py at the book's standard scale (0.32 mm per
cm).

Close-up conventions: side profiles have the wall on the right, as in the
climber side views, and show the hand from the thumb side (the pocket from
the little-finger side). Face-on views look at the wall, so the back of the
hand faces you. Pinches and the wrap are seen from above, wall at the top.
"""

from climb import *
import hand as H
from hand import (WX, HAND_SCALE, TILT, Hand, profile_frame, edge_profile, rounded_lip,
                  grip_profile, grip_pose, joint_arc, on_edge, nail_point, pad_point)

CLOSE = HAND_SCALE   # paper mm per cm for every hand close-up
SKIN = dict(fill=WHITE, stroke=INK, sw=0.35)


def warn(name, *climbers):
    for c in climbers:
        for w in c.warn():
            print(name + ":", w)
            if DEBUG and "hand" in w:
                s = w[0]
                t = getattr(c, s + "h")
                reach = (c.D["upper_arm"] + c.D["forearm"] + c.D["hand"]) * c.arm_len[s]
                print("   shoulder", tuple(round(v, 1) for v in c.J[s + "sh"]), "target", t,
                      "dist", round(length(sub(t, c.J[s + "sh"])), 1), "reach", reach)


def hwarn(name, *posed):
    """Joint angles outside their range, for close-up hands."""
    for p in posed:
        for w in p.hand.warn():
            print(name + ":", w)


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


def pip_arc(f, p, label, r=1.5, at=None, finger="i"):
    """The middle joint's flexion, labelled up and to the left of it."""
    j = p.joint(finger, "pip")
    joint_arc(f, p, finger, "pip", r, label, at=at or add(j, (-2.6, 2.4)), ext=r + 0.7)


GRIP_FRAME = dict(x0=-12.0, y0=-8.5, y1=8.6)


def drag_face():
    """Three-finger drag on a rounded edge, seen from behind; the little
    finger curled off the hold."""
    b = Fig(-7.6, -12.0, 11.6, 5.2, scale=CLOSE)
    face_edge(b, (0.2, 0.0), 14.6, 4.2, rounded=True)
    h = Hand("open", fingers={"i": (12, 30, 40), "m": (12, 30, 40), "r": (12, 30, 40),
                              "l": (55, 95, 60)}, wrist=(0, 0)).rest_thumb()
    p = h.view("back", a0=92)
    p.move_point(pad_point(h, "m", 0.55), (-0.2, 2.2))
    p.draw(b, z=0)
    label_lines(b, ["little", "finger off"], (9.2, -3.2), to=p.joint("l", "pip"))
    hwarn("drag face", p)
    return b


def open_hand_fig(path):
    a, p = grip_profile("open", **GRIP_FRAME)
    pip_arc(a, p, "≈40°")
    a.label("pads over the lip", (-4.0, 7.4), to=a_pad(p), anchor="middle")
    hwarn("open hand", p)
    b = drag_face()
    combine([a, b], path, gap=4, labels=["a", "b"],
            captions=["drag, side view", "three-finger drag"])


def a_pad(p, f="i", k=0.62):
    return p.xy(pad_point(p.hand, f, k))


def half_crimp_fig(path):
    a, p = grip_profile("half", **GRIP_FRAME)
    pip_arc(a, p, "≈90°")
    label_lines(a, ["end joint", "straight"], (-9.2, 1.6), to=p.joint("i", "dip"))
    b, pb = grip_profile("full", **GRIP_FRAME)
    pip_arc(b, pb, "over 90°")
    label_lines(b, ["end joint", "bent back"], (-9.2, 1.6), to=pb.joint("i", "dip"))
    hwarn("half crimp", p, pb)
    combine([a, b], path, gap=4, labels=["a", "b"],
            captions=["half crimp", "full crimp, for comparison"])


def full_crimp_fig(path):
    a, p = grip_profile("full", **GRIP_FRAME)
    pip_arc(a, p, "over 90°")
    label_lines(a, ["end joint", "bent back"], (-9.2, 1.6), to=p.joint("i", "dip"))
    a2 = H.a2_pulley(a, p)
    a.label("A2 pulley", (-9.2, -4.4), to=a2)
    b, pb = grip_profile("lock", **GRIP_FRAME)
    th = pb.hand.thumb()
    b.label("thumb over the nail", (-4.0, 7.6), to=pb.xy(H.thumb_point(th, "nail", 0.55)),
            anchor="middle")
    hwarn("full crimp", p, pb)
    combine([a, b], path, gap=4, labels=["a", "b"],
            captions=["full crimp, side view", "thumb lock"])


def pocket_profile(safe, labels=True, **frame):
    """Two-finger pocket seen from the little-finger side: the ring finger
    (grey, behind) in the hole, the little finger (in front) either kept
    parallel or curled into the palm."""
    f = profile_frame(**(frame or dict(y0=-12.0, y1=5.5, x0=-14.5)))
    # a hold in section, with the pocket cut into its front face
    blk = [(WX, 4.0), (WX - 3.0, 3.5), (WX - 3.9, 2.0), (WX - 3.9, -1.6),
           (WX - 3.2, -3.8), (WX, -4.4)]
    f.smooth(blk, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    cav = [(WX - 4.2, 1.75), (WX - 1.2, 1.85), (WX - 0.55, 0.85), (WX - 1.1, -0.15),
           (WX - 4.2, -0.2)]
    f.smooth(cav, z=-4.9, fill=PALE, stroke=INK, sw=0.3, tension=0.5)
    f.line((WX - 3.92, 1.7), (WX - 3.92, -0.15), z=-4.8, sw=0.6, stroke=PALE)
    # the index, out of the hole, hangs loose (hidden behind); the thumb
    # rests along it, in front of the palm, so it shows grey below the
    # fingers and the curled little finger stands out against it
    little = (8, 22, 12, 3) if safe else (70, 95, 45, 3)
    h = Hand("pocket", fingers={"l": little, "r": (30, 60, 25, -3), "i": (35, 60, 25)})
    h.rest_thumb()
    p = h.view("little", tilt=TILT, stagger=0)
    pad = (WX - 1.3, -0.05)
    p.place("r", pad, distal=-8, k=0.8)
    p.reach("m", add(pad, (0.3, 0.0)), k=0.8)
    if safe:
        p.reach("l", (WX - 3.95, -1.3), k=0.75)
    p.draw(f, z=0, others="r")
    if safe:
        if labels:
            label_lines(f, ["little finger", "parallel"], (-11.2, -6.6),
                        to=p.surface("l", "pip", "palm", 0.6))
    else:
        # the ring finger's tendon is pulled out toward the hole, the
        # little finger's into the palm: one arrow along each finger
        ur = ang(p.angle("r", 2))
        cr = add(lerp(p.joint("r", "pip"), p.joint("r", "dip"), 0.2), mul(rot(ur, 90), 1.25))
        f.arrow([add(cr, mul(ur, -1.2)), add(cr, mul(ur, 1.2))], kind="force", z=50)
        ul = ang(p.angle("l", 1))
        cl = add(lerp(p.joint("l", "mcp"), p.joint("l", "pip"), 0.3), mul(rot(ul, -90), 1.2))
        f.arrow([add(cl, mul(ul, 1.0)), add(cl, mul(ul, -1.2))], kind="force", z=50)
        if labels:
            label_lines(f, ["opposite", "pulls"], (-11.2, -6.6), to=add(cl, mul(ul, -0.4)))
            label_lines(f, ["little finger", "curled"], (-11.2, 3.4),
                        to=p.surface("l", "pip", "back", 0.9))
    hwarn("pocket", p)
    return f


def pocket_fig(path):
    combine([pocket_profile(True), pocket_profile(False)], path, gap=4,
            labels=["a", "b"], captions=["safer", "stronger but riskier"])


# ---------------------------------------------------------------- face-on hands


def face_edge(f, c, w, h, rounded=False, z=-5):
    """A horizontal edge seen face-on (a long bar), centred on c."""
    x, y = c
    r = h * (0.5 if rounded else 0.25)
    f.smooth([(x - w / 2 + r, y + h / 2), (x + w / 2 - r, y + h / 2),
              (x + w / 2, y), (x + w / 2 - r, y - h / 2), (x - w / 2 + r, y - h / 2),
              (x - w / 2, y)], z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    f.line((x - w / 2 + r, y + h * 0.3), (x + w / 2 - r, y + h * 0.3), z=z + 0.1,
           sw=0.55, stroke=WHITE)


def wall_top(f, y, x0, x1, z=-20, depth=None):
    """The wall seen from above: a horizontal line, hatched above; `depth`
    fills the wall's section further up."""
    w = f.mm(2.4)
    d = max(w, depth or 0)
    f.poly([(x0, y), (x1, y), (x1, y + d), (x0, y + d)], z=z, fill=PALE, stroke=None)
    f.line((x0, y), (x1, y), z=z + 1, sw=0.6)
    x = x0
    while x < x1:
        f.line((x, y), (x + f.mm(1.5), y + w), z=z + 1, sw=0.18, stroke=MID)
        x += f.mm(1.9)


def inward(f, contact, normal, length_=2.6, gap=2.1):
    """A force arrow pressing toward `contact` along -normal (normal points
    out of the hold's face), stopping `gap` cm short, outside the digit."""
    n = norm(normal)
    f.arrow([add(contact, mul(n, length_ + gap)), add(contact, mul(n, gap))],
            kind="force")


def pinch_panel(kind, labels=True, frame=(-9.5, -12.0, 9.5, 1.3), scale=CLOSE):
    """A pinch seen from above: the wall along the top, the hold sticking out
    toward the climber, the hand's index-finger edge facing you. The thumb
    presses one face and the fingers the opposite face."""
    f = Fig(*frame, scale=scale)
    wall_top(f, 0.0, frame[0], frame[2], depth=frame[3])
    if kind == "narrow":
        # a 3 cm rib: the thumb pad on one face, the curled index on the other
        f.poly([(-1.5, 0), (-1.5, -4.6), (1.5, -4.6), (1.5, 0)], z=-5, fill=DARK,
               stroke=INK, sw=0.35)
        h = Hand("pinch", fingers={f_: (40, 20, 10) for f_ in "imrl"}, wrist=(10, 0))
        cf, ct = (1.5, -2.4), (-1.5, -4.1)
        p = h.view("thumb", tilt=0, flip=True, stagger=0).place("i", cf, a0=20, k=0.65)
        on_edge(p, cf, k=0.65, dx=0.0)
        p.thumb_to(ct, part="pad", k=0.6, facing=0)
        nf, nt = (1, 0), (-1, 0)
    elif kind == "wide":
        # a 6 cm block: thumb on one face, fingers flat on the other
        f.poly([(-3, 0), (-3, -4.6), (3, -4.6), (3, 0)], z=-5, fill=DARK,
               stroke=INK, sw=0.35)
        h = Hand("pinch", fingers={f_: (55, 15, 0) for f_ in "imrl"}, wrist=(10, 0))
        cf, ct = (3.0, -2.2), (-3.0, -3.8)
        p = h.view("thumb", tilt=0, flip=True, stagger=0).place("i", cf, a0=20, k=0.65)
        on_edge(p, cf, k=0.65, dx=0.0)
        p.thumb_to(ct, part="pad", k=0.6, facing=0)
        nf, nt = (1, 0), (-1, 0)
    else:
        # the ridge of a volume: the thumb on the near face, the fingers over
        # the ridge on the far face
        apex = (0.0, -7.0)
        f.poly([(-8.0, 0), apex, (8.0, 0)], z=-12, fill=LIGHT, stroke=INK, sw=0.35)
        lf = norm(sub((-8.0, 0), apex))
        rf = norm(sub((8.0, 0), apex))
        nt, nf = rot(lf, 90), rot(rf, -90)
        ct = add(apex, mul(lf, 4.4))
        cf = add(apex, mul(rf, 5.4))
        h = Hand("pinch", fingers={f_: (20, 25, 8) for f_ in "imrl"}, wrist=(20, 0))
        p = h.view("thumb", tilt=0, flip=True, stagger=0).place("i", cf, a0=-12, k=0.6)
        on_edge(p, cf, k=0.6, dx=0.0)
        p.thumb_to(ct, part="pad", k=0.55,
                   facing=math.degrees(math.atan2(-nt[1], -nt[0])))
    p.draw(f, z=0)
    inward(f, cf, nf)
    inward(f, ct, nt)
    if kind == "narrow" and labels:
        f.text("wall", (7.6, 0.75), size=7)
        f.label("thumb", (-6.6, -6.0), to=p.joint("t", "ip"), size=7)
        f.label("index", (6.8, -7.6), to=p.joint("i", "pip"), size=7)
    hwarn("pinch " + kind, p)
    return f


def pinch_fig(path):
    combine([pinch_panel("narrow"), pinch_panel("wide"), pinch_panel("volume")],
            path, gap=3, labels=["a", "b", "c"],
            captions=["narrow pinch", "wide pinch", "volume edge"])


def thumb_catch_panel(labels=True, **frame):
    """Fingers over a rounded edge, the thumb pressing up into a dimple on
    its underside."""
    f = profile_frame(**(frame or dict(y0=-11.0, y1=6.0, x0=-13.5)))
    rounded_lip(f, WX, 0, depth=2.6, height=4.2)
    dimple = (WX - 1.9, -2.95)
    f.circle(dimple, 0.38, z=-4.9, fill=INK, stroke=None)
    p = grip_pose("open")
    p.thumb_to(add(dimple, (-0.2, -0.3)), part="tip")
    p.draw(f, z=0)
    tip = p.joint("t", "tip")
    f.arrow([add(tip, (-1.0, -3.6)), add(tip, (-0.3, -1.2))], kind="force")
    f.arrow([add(a_pad(p), (-0.2, 3.6)), add(a_pad(p), (-0.2, 1.2))], kind="force")
    if labels:
        label_lines(f, ["thumb in", "a dimple"], (-10.6, -6.2), to=add(tip, (-0.1, -0.5)))
    hwarn("thumb catch", p)
    return f


def thumb_catch_fig(path):
    # (a) fingers over a rounded edge, thumb pressing up into a dimple under it
    a = thumb_catch_panel()
    # (b) the ridge of a volume in profile: fingers over it, thumb pad
    # pressing up on the lower face
    b = profile_frame(y0=-11.0, y1=6.0, x0=-13.5)
    ridge = (WX - 4.4, -0.6)
    b.poly([(WX, 5.0), ridge, (WX, -9.0)], z=-12, fill=LIGHT, stroke=INK, sw=0.35)
    up = norm(sub((WX, 5.0), ridge))
    lo = norm(sub((WX, -9.0), ridge))
    on_up = add(ridge, mul(up, 2.2))
    h = Hand("open", fingers={f_: (25, 30, 10) for f_ in "imrl"})
    p = h.view("thumb", tilt=TILT).place("i", on_up, a0=110, k=0.6)
    on_edge(p, on_up, k=0.6, along=math.degrees(math.atan2(up[1], up[0])), spread=0.3)
    press = add(ridge, mul(lo, 4.0))
    out = rot(lo, -90)
    p.thumb_to(add(press, mul(out, 0.05)), part="pad", k=0.6,
               facing=math.degrees(math.atan2(-out[1], -out[0])))
    p.draw(b, z=0)
    b.arrow([add(press, mul(out, 4.4)), add(press, mul(out, 1.9))], kind="force")
    # the leader runs under the force arrow to the thumb, not through it
    label_lines(b, ["thumb pad", "presses up"], (-10.6, -8.2), to=p.joint("t", "ip"))
    hwarn("thumb catch b", p)
    combine([a, b], path, gap=4, labels=["a", "b"],
            captions=["thumb catch", "thumb press on a volume"])


def regrip_fig(path):
    panels = []
    for k in range(2):
        f = Fig(-11, -12, 11, 10.2, scale=CLOSE)
        face_edge(f, (0, 2.0), 19, 3.2)
        # the incut sweet spot on the right half, a screw hole beside it
        f.poly([(1.8, 3.3), (8.5, 3.3), (8.0, 2.7), (2.3, 2.7)], z=-4.8, fill=INK,
               stroke=None)
        f.circle((5.2, 1.5), 0.45, z=-4.8, fill="#b0b0b0", stroke=INK, sw=0.25)
        drag = Hand("open", wrist=(0, 0)).rest_thumb()
        pd = drag.view("back", a0=90)
        pd.move_point(pad_point(drag, "m", 0.55), (-4.6, 3.6))
        if k == 0:
            pd.draw(f, z=0)
            f.circle((5.2, 1.5), 1.6, z=40, stroke=INK, sw=0.3, fill=None)
            f.label("aim at the screw hole", (5.0, -8.4), to=(5.2, -0.1), size=7)
        else:
            pd.draw(f, z=-3, ghost=True)
            crimp = Hand("half", wrist=(10, 0)).rest_thumb()
            pc = crimp.view("back", a0=90)
            pc.move_point(pad_point(crimp, "m", 0.85), (4.9, 3.3))
            pc.draw(f, z=0)
            f.arrow([(-4.6, 8.4), (0.2, 9.3), (3.4, 8.9)], kind="move")
            label_lines(f, ["half crimp", "in the incut"], (-1.4, -9.4))
            hwarn("regrip", pc)
        panels.append(f)
    combine(panels, path, gap=4, labels=["1", "2"],
            captions=["catch where you can", "walk the fingers to the incut"])


def wrap_fig(path):
    """An arete seen from above: palm and thumb on one face, fingers round
    the edge onto the other."""
    f = Fig(-11.0, -10.5, 11.0, 5.4, scale=CLOSE)
    apex = (0.0, -3.0)
    lf, rf = ang(135), ang(45)               # along the faces, away from the edge
    out_l, out_r = rot(lf, 90), rot(rf, -90)  # out of each face
    f.poly([apex, add(apex, mul(lf, 16)), (-11, 5.4), (11, 5.4), add(apex, mul(rf, 16))],
           z=-20, fill=PALE, stroke=None)
    f.line(apex, add(apex, mul(lf, 16)), z=-19, sw=0.7)
    f.line(apex, add(apex, mul(rf, 16)), z=-19, sw=0.7)
    f.text("arête", (0.0, 1.0), size=7)
    on_l = add(apex, mul(lf, 2.8))
    # the palm lies flush on the right face, the fingers bend round the edge
    # the thumb lies flat in the plane of the palm, on the same face
    h = Hand("wrap", fingers={f_: (9, 75, 5) for f_ in "imrl"}, wrist=(55, 0),
             thumb=dict(ra=50, pa=0, rot=42, mcp=0, ip=0))
    p = h.view("thumb", tilt=0, stagger=0).place("i", on_l, a0=224, k=0.6)
    on_edge(p, on_l, k=0.6, dx=0.0)
    p.draw(f, z=0)
    f.label("palm and thumb", (7.6, -8.8), to=p.joint("t", "ip"), size=7)
    f.label("fingers round the edge", (-6.0, -8.8), to=p.joint("i", "pip"), size=7)
    inward(f, add(apex, mul(lf, 2.6)), out_l, 2.2, gap=1.9)
    inward(f, add(apex, mul(rf, 7.2)), out_r, 2.2, gap=3.0)
    hwarn("wrap", p)
    f.save(path)


def hold_angle_fig(path):
    """Concept: incut, flat and sloping edges in profile, each pulled
    straight down by a half-crimping finger."""
    panels = []
    specs = ((-20, "positive (incut)", -52, "lip locks it"),
             (0, "flat", -60, "friction and curl"),
             (30, "negative (sloping)", -40, "slides off"))
    for slope, cap, a3, note in specs:
        f = profile_frame(y0=-7.0, y1=7.6, x0=-8.0)
        t = math.tan(math.radians(slope))
        edge_profile(f, WX, 0, depth=3.2, height=3.6, slope=slope)
        x0 = WX - 2.8
        f.line((x0, -(WX - x0) * t + 0.07), (WX - 0.15, -0.15 * t + 0.07), z=-4.9,
               sw=0.5, stroke=WHITE)
        cx = WX - 1.3
        pt = (cx, -(WX - cx) * t)
        h = Hand("half", fingers={f_: (45, 90, 8) for f_ in "imrl"})
        p = h.view("thumb", tilt=TILT).place("i", pt, distal=a3, k=0.85)
        on_edge(p, pt, k=0.85, along=180 + slope, spread=0.3)
        H.tuck_thumb(p, "half")      # clear of the finger and the edge
        p.draw(f, z=0)
        f.arrow([(WX - 1.0, -3.9), (WX - 1.0, -6.6)], kind="force")
        if slope > 0:
            f.arrow([add(pt, mul(ang(slope), -0.6)), add(pt, mul(ang(slope), -3.6))],
                    kind="move", z=45)
        f.text(note, (-2.6, 6.7), size=7)
        hwarn("hold angle", p)
        panels.append(f)
    combine(panels, path, gap=3, captions=[c for _, c, _, _ in specs])


# ---------------------------------------------------------------- climber figures


def jug_fig(path):
    J = (-8, 210)
    LF = (-32, 62)
    RF = (24, 60)
    panels = []
    for good in (False, True):
        f = Fig(-80, 25, 80, 240)
        wall_grid(f)
        hold(f, "jug", J, size=1.3)
        hold(f, "foot", LF)
        hold(f, "foot", RF)
        g = grip(J, size=1.3)
        if not good:
            c = Climber(None, shoulders=(-6, 166), lh=add(g, (-7, 0)), rh=add(g, (7, 0)),
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        elbows={"l": "out", "r": "out"},
                        leg_len={"l": .9, "r": .9})
            c.draw(f)
            f.label("arms bent", (58, 196), to=c.J["rel"])
        else:
            kw = dict(shoulders=(6, 154), lean=-6, lh=g, lf={"at": stand(LF)},
                      rf={"at": stand(RF)}, leg_len={"l": .95, "r": .95})
            rsh = Climber(None, **kw).J["rsh"]
            hang = add(rsh, mul(ang(-68), 64.5))     # arm hangs straight, a little out
            c = Climber(None, rh=hang, elbows={"r": "out"}, **kw)
            c.draw(f)
            ha = c.J["rha"]
            for k in (-1, 1):
                f.smooth([add(ha, (k * 7, -5)), add(ha, (k * 9.5, -1)), add(ha, (k * 7, 3))],
                         closed=False, z=50, sw=0.35)
            f.label("shake out", (64, 140), to=add(ha, (3, 3)))
            f.label("straight arm", (-66, 178), to=lerp(c.J["lsh"], c.J["lha"], 0.55))
        f.cog(c.cog(), plumb_to=45)
        warn("jug", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["bent arms: forearms pump", "straight arm, other hand rests"])


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
            kw = dict(shoulders=(-26, 150), lh=g, lf={"at": stand(LF)},
                      rf={"at": stand(RF)}, elbows={"l": "out", "r": "out"},
                      knees={"l": "out", "r": "out"}, leg_len={"l": .9, "r": .95})
            rsh = Climber(None, **kw).J["rsh"]
            c = Climber(None, rh=add(rsh, mul(norm(sub(grip(T), rsh)), 62)), **kw)
            c.draw(f)
            f.turn(add(c.pelvis, (4, 26)), 36, -8, -172)
            f.label("swings open", (52, 128), size=7.5)
        else:
            c = Climber((38, 120), lean=-10, lh=g, rh=grip(T),
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        elbows={"l": "down", "r": "out"},
                        leg_len={"l": 1.0, "r": .95})
            c.draw(f)
            f.arrow([add(g, (8, -11)), add(g, (26, -11))], kind="force")
            f.arrow([add(stand(LF), (-3, 6)), add(stand(LF), (-21, 6))], kind="force")
            f.label("lean away", (-46, 142), to=lerp(c.J["lsh"], c.J["lel"], 0.5))
            f.label("foot pushes left", (-46, 40), size=7.5)
        f.cog(c.cog(), plumb_to=48)
        warn("sidepull", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["under the hold: barn door", "body right of it, leaning away"])


def gaston_fig(path):
    H = (0, 172)         # one hold, its gripping surface facing left
    panels = []
    for kind in ("sidepull", "gaston"):
        f = Fig(-85, 25, 85, 245)
        wall_grid(f)
        hold(f, "jug", H, use=180)
        g = grip(H, use=180)
        if kind == "sidepull":
            T = (60, 222)
            LF, RF = (-6, 72), (46, 64)
            hold(f, "jug", T)
            hold(f, "foot", LF)
            hold(f, "foot", RF)
            c = Climber((40, 116), lean=-14, lh=g, rh=grip(T),
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        elbows={"l": "down"}, leg_len={"l": .95, "r": .9})
            c.draw(f)
            f.arrow([add(g, (8, -12)), add(g, (26, -12))], kind="force")
            f.label("body right of it", (40, 40), size=7.5)
        else:
            # right hand in front of the right shoulder, thumb down, elbow
            # out to the side at about hand height; the forearm points into
            # the wall, so it looks short from behind
            T = (-66, 222)
            LF, RF = (-56, 72), (2, 62)
            hold(f, "jug", T)
            hold(f, "foot", LF)
            hold(f, "foot", RF)
            c = Climber(None, shoulders=(-34, 166), lh=grip(T), rh=None,
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        elbows={"l": "out"}, leg_len={"l": .93, "r": .95},
                        order=["lleg", "rleg", "torso", "larm"])
            c.draw(f)
            el = (13, 159)
            c.draw_arm(f, "r", el, g, z=4)
            f.arrow([add(g, (5, 12)), add(g, (24, 12))], kind="force")
            f.label("elbow out", (50, 142), to=add(el, (2, -2)))
            f.label("thumb down", (-8, 232), to=add(g, (1.8, -6.5)))
            f.arrow([add(stand(LF), (-2, 6)), add(stand(LF), (-20, 6))], kind="force")
            f.label("body left of it", (-30, 40), size=7.5)
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
        U = at(190 if not good else 132)
        hand = on_hold(U, 0, 5.0, -4.6)
        if not good:
            hold_side(f, "undercling", U)
            F1 = at(60)
            hold_side(f, "foot", F1)
            foot = add(F1, (-2.5, 2.5))
            c = Climber(None, shoulders=(-2, 160), view="side", lean=0,
                        lh=hand, rh=hand, lf={"at": foot}, rf={"at": foot},
                        elbows={"l": "down", "r": "down"},
                        knees={"l": "up", "r": "up"})
            c.draw(f)
            f.turn((-34, 140), 24, 30, 150)
            f.label("tips backwards", (-64, 182), size=7.5)
            f.label("bent arms", (-10, 224), to=lerp(c.J["rel"], c.J["rha"], 0.55))
        else:
            # the hold sits beside the right knee, nearer to you than it
            hold_side(f, "undercling", U, z=3.5)
            F1 = at(88)
            hold_side(f, "foot", F1)
            foot = add(F1, (-2.5, 2.5))
            T = at(238)
            hold_side(f, "jug", T)
            kw = dict(shoulders=(-28, 161), view="side", lean=-20, rh=hand,
                      lf={"at": foot}, rf={"at": foot})
            sh = Climber(None, **kw).J["lsh"]
            reach_to = add(sh, mul(norm(sub(add(T, (-4, -2)), sh)), 60))
            c = Climber(None, lh=reach_to, **kw)
            c.draw(f)
            f.arrow([add(c.J["lha"], (2, 4)), add(T, (-4, -2))], kind="move")
            f.arrow([add(hand, (-1, -3)), add(hand, (-9, 9))], kind="force", z=50)
            f.arrow([add(foot, (-13, 1)), add(foot, (-1, 1))], kind="force")
            f.label("arm straight", (-72, 120), to=lerp(c.J["rsh"], hand, 0.5))
            f.label("feet up", (-64, 70), to=add(foot, (-8, -1)))
        f.cog(c.cog(), plumb_to=35)
        warn("undercling", c)
        panels.append(f)
    combine(panels, path, gap=6, labels=["a", "b"],
            captions=["hold above the head", "feet up, hold at the waist"])


def sloper_closeup(angle=20, scale=CLOSE, labels=True,
                   frame=(-10.6, -11.0, 6.2, 9.0)):
    """An open hand draped over a dome sloper on a wall overhanging by
    `angle` degrees, seen from the thumb side: palm and finger pads on the
    hold, wrist below it, the pull straight down the arm."""
    def R(q):
        return rot(q, angle)
    f = Fig(*frame, scale=scale)
    x_at = lambda y: R((WX, 0))[0] - (y - R((WX, 0))[1]) * math.tan(math.radians(angle))
    wall_side(f, x_at(frame[1]), frame[1], frame[3], angle=angle)
    # the hand, posed against a vertical wall at x = WX, then turned with it
    h = Hand("sloper", wrist=(-8, 0))
    pad = R((WX - 1.7, 4.0))
    p = h.view("thumb", tilt=TILT).place("i", pad, distal=-15 + angle, k=0.55)
    on_edge(p, pad, k=0.55, along=200 + angle, spread=0.3)
    # the dome follows the palm side of the hand, a hair inside it
    hand_side = []
    ch = h.finger("i")
    A3, N3, _ = ch["frames"][3]
    for s in (1.7, 1.2, 0.6):
        hand_side.append(p.xy(H.vadd(H.vadd(ch["dip"], H.vmul(A3, s)), H.vmul(N3, -0.78))))
    for j, k in (("dip", 2), ("pip", 1)):
        F = ch["frames"]
        n = H.vnorm(H.vadd(F[k][1], F[k + 1][1]))
        hand_side.append(p.xy(H.vadd(ch[j], H.vmul(n, -0.8))))
    A1, N1, _ = ch["frames"][1]
    hand_side.append(p.xy(H.vadd(H.vadd(ch["mcp"], H.vmul(A1, 1.6)), H.vmul(N1, -1.05))))
    hand_side += [p.at(7.6, 3.0, -1.6), p.at(5.0, 2.8, -1.8)]
    dome = [R((WX, 4.9))] + hand_side + [R((WX - 3.0, -5.6)), R((WX, -6.9))]
    f.smooth(dome, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.55)
    h.rest_thumb()
    p.draw(f, z=0)
    f.arrow([(0.6, -6.3), (0.6, max(-10.2, frame[1] + 0.5))], kind="force")
    if labels:
        f.label("palm and pads", (-5.2, 7.8), to=lerp(p.joint("i", "pip"),
                                                       p.joint("i", "dip"), 0.5))
        f.label("wrist below", (-7.0, -10.2), to=p.at(-0.4, 0.3, -1.8))
    hwarn("sloper close-up", p)
    return f


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
            f.arrow([add(hand, (-2, 1)), add(hand, (-13, -6))], kind="move")
            f.text("hand", (-70, 255), size=7.5, z=60)
            f.label("rolls off", (-70, 255 - f.pt(7.5) * 1.15), to=add(hand, (-3, 3)),
                    anchor="middle")
            # low on the right, clear of the wall; the plumb line stops above
            # the label under the arrow
            f.label("both feet high", (-24, 70), to=add(fh, (-3, -2)))
            f.body_arrow([(-44, 132), (-74, 128)], width=2.4)
            f.label("hips pushed out", (-70, 104), size=7.5)
        else:
            Fh, Fl = at(102), at(62)
            hold_side(f, "foot", Fh, angle=A)
            hold_side(f, "foot", Fl, angle=A)
            fh = on_hold(Fh, A, 2.6, 2.4)
            fl = on_hold(Fl, A, 2.6, 2.4)
            c = Climber((-42, 102), view="side", lean=0, lh=hand, rh=hand,
                        lf={"at": fl, "angle": A}, rf={"at": fh, "angle": A},
                        leg_len={"r": 0.85})
            c.draw(f)
            f.label("arm straight", (-90, 200), to=lerp(c.J["rsh"], hand, 0.5))
            label_lines(f, ["hips low,", "under it"], (-76, 74), to=add(c.pelvis, (-6, -4)),
                        size=7.5)
            f.label("one foot low", (-30, 30), to=add(fl, (-3, -2)), anchor="start")
        f.cog(c.cog(), plumb_to=28 if good else 116)
        warn("sloper", c)
        panels.append(f)
    panels.append(sloper_closeup(A))
    combine(panels, path, gap=4, labels=["a", "b", "c"],
            captions=["hips up and out: it rolls off", "hips low: it holds",
                      "hand draped over it"])


def palming_fig(path):
    f = Fig(-90, 25, 90, 245)
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
    c = Climber((-8, 124), lean=-8, lh=grip(T), rh=palm,
                lf={"at": stand(LF)}, rf={"at": stand(RF0)},
                elbows={"r": "down", "l": "out"}, hand_style={"r": "open"},
                leg_len={"l": .95, "r": .9})
    c.draw(f)
    f.arrow([add(palm, (7, 2)), add(palm, (22, -10))], kind="force")
    f.arrow([add(stand(RF0), (-6, 8)), (-4, 88)], kind="move")
    label_lines(f, ["palm presses", "down-right"], (62, 76), to=add(palm, (1, -3)), size=7.5)
    f.label("right foot goes up", (-48, 36), to=(4, 64))
    f.cog(c.cog(), plumb_to=45)
    warn("palming", c)
    f.save(path)


def mantle_fig(path):
    TOP = 200
    WX = 30
    frames = []
    for k in range(3):
        f = Fig(-75, 32, 70, 290)
        at = wall_side(f, WX, 32, TOP, angle=0)
        f.poly([(WX, TOP), (70, TOP), (70, TOP - f.mm(2.4)), (WX, TOP - f.mm(2.4))],
               z=-21, fill=PALE, stroke=None)
        f.line((WX, TOP), (70, TOP), z=-19, sw=0.6)
        Fh, Fl = at(TOP - 82), at(TOP - 150)
        hold_side(f, "foot", Fh)
        hold_side(f, "foot", Fl)
        foot_h = add(Fh, (-2.5, 2.5))
        foot_l = add(Fl, (-2.5, 2.5))
        lip = (WX + 1, TOP + 1.5)
        if k == 0:
            c = Climber((-26, 114), view="side", lean=20, lh=lip, rh=lip,
                        lf={"at": foot_l}, rf={"at": foot_h, "flip": True},
                        leg_len={"r": 0.85})
            c.draw(f)
        elif k == 1:
            palm = (WX + 7, TOP)
            flat_palm(f, palm)
            # shoulders over the lip and above the palm, so the bent elbow
            # points up and back, as the caption says
            c = Climber(None, shoulders=(33, 227), view="side", lean=34, lh=lip,
                        rh=add(palm, (-1, 3)),
                        lf={"at": (6, 88), "angle": -40}, rf={"at": foot_h},
                        leg_len={"r": 0.65})
            c.draw(f)
            f.arrow([add(palm, (1, 16)), add(palm, (1, 5))], kind="force")
            f.label("palm flat, elbow up", (-34, 268), to=c.J["rel"])
            f.body_arrow([(-22, 146), (-14, 182)], width=2.2)
        else:
            palm = (WX + 8, TOP)
            palm2 = (WX + 16, TOP)
            flat_palm(f, palm)
            flat_palm(f, palm2, z=-1)
            # shoulders over the hands, hips close to the lip, so the
            # weight is over the hands and the high foot
            c = Climber((13, 226), view="side", lean=40,
                        lh=add(palm2, (-1, 3)), rh=add(palm, (-1, 3)),
                        lf={"at": (WX - 3, 150), "angle": -50, "contact": "ball"},
                        rf={"at": (WX + 13, TOP + 1), "angle": 0, "contact": "ball"},
                        leg_len={"r": 0.85})
            c.draw(f)
            f.label("arms straight", (-36, 268), to=lerp(c.J["rsh"], c.J["rha"], 0.45))
            f.label("foot on top, no knee", (-30, 176), to=c.J["rkn"])
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
            f.label("foot high", (-50, 70), to=c.J["rkn"])
        else:
            flat_palm(f, add(palm, (0, -3.2)), length_=8)
            sh = (-8 + math.sin(math.radians(5)) * 47, 164 + math.cos(math.radians(5)) * 47)
            reach_to = add(sh, mul(norm(sub(add(T, (-4, -2)), sh)), 60))
            c = Climber((-8, 164), view="side", lean=5, lh=palm, rh=reach_to,
                        lf={"at": foot_h}, rf={"at": foot_h},
                        leg_len={"l": 0.85, "r": 0.85})
            c.draw(f)
            f.arrow([add(c.J["rha"], (1, 4)), add(T, (-5, -3))], kind="move")
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


def flat_palm(f, at, length_=9.0, z=60):
    """A palm pressed flat on a horizontal surface, seen from the side."""
    f.poly(capsule(add(at, (-length_ / 2, 1.6)), 1.7, add(at, (length_ / 2, 1.6)), 1.4),
           z=z, **SKIN)


# ---------------------------------------------------------------- hand atlas
#
# A reference plate: one small close-up per grip, all at the book's hand
# scale, each with a force arrow for the pull. Profiles (wall on the right)
# where a profile shows the grip; the pinch is seen from above.

TILE_W, TILE_H = 14.4, 16.4      # tile size in cm


def tile_profile(y0=-10.0):
    x1 = WX + 2.4 / CLOSE + 0.01
    return dict(x0=x1 - TILE_W, y0=y0, y1=y0 + TILE_H)


def pull(f, x, y, down=True, length_=3.4):
    """A force arrow for the pull on the hold."""
    d = -1 if down else 1
    f.arrow([(x, y), (x, y + d * length_)], kind="force")


def atlas_grip(kind):
    f, p = grip_profile(kind, **tile_profile())
    pull(f, WX - 1.1, -3.4 if kind == "open" else -2.8)
    hwarn("atlas " + kind, p)
    return f


def atlas_jug():
    f = profile_frame(**tile_profile())
    # a big incut jug: the fingers hook over its lip into the bucket behind
    jug = [(WX, -5.0), (WX - 5.0, -4.6), (WX - 7.2, -2.4), (WX - 7.7, 0.8),
           (WX - 7.2, 1.85), (WX - 6.4, 1.6), (WX - 5.6, 0.3), (WX - 2.8, -0.3),
           (WX, 0.4)]
    f.smooth(jug, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.35)
    h = Hand("jug")
    pad = (WX - 4.2, -0.2)
    p = h.view("thumb", tilt=TILT).place("i", pad, distal=-35, k=0.75)
    on_edge(p, pad, k=0.75, along=-8, spread=0.35)
    h.rest_thumb()
    p.draw(f, z=0)
    pull(f, WX - 1.4, -5.6)
    hwarn("atlas jug", p)
    return f


def atlas_undercling():
    """Palm up under a flake that faces down, pulling up: the thumb-side view
    mirrored, so the palm faces up and the wall stays on the right."""
    f = profile_frame(**tile_profile())
    flake = [(WX, -2.4), (WX - 5.6, -1.0), (WX - 6.8, 0.0), (WX - 6.0, 0.6),
             (WX - 3.0, 0.5), (WX, 1.6)]
    f.smooth(flake, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.4)
    h = Hand("undercling", fingers={f_: (5, 28, 10) for f_ in "imrl"}, wrist=(10, 0))
    pad = (WX - 2.6, -1.95)
    p = h.view("thumb", tilt=TILT, flip=True).place("i", pad, a0=-32, k=0.75)
    on_edge(p, pad, k=0.75, along=166, spread=0.3)
    h.rest_thumb()
    p.draw(f, z=0)
    f.arrow([(WX - 1.4, -7.2), (WX - 1.4, -3.8)], kind="force")
    hwarn("atlas undercling", p)
    return f


def atlas_palm():
    """A palm pressed flat on a steep volume face, wrist bent right back so
    the forearm pushes straight into the face. The tile is cropped 1.8 cm
    higher than the others: at this extension the back of the wrist
    folds into a sharp crease (the union of the hand and forearm solids),
    so the bottom edge cuts across the heel of the hand just above it."""
    f = profile_frame(**tile_profile(-8.2))
    slope = 55
    u = ang(slope)
    top = (WX, 6.4)
    low = sub(top, mul(u, 22))
    f.poly([top, low, (WX, low[1])], z=-12, fill=LIGHT, stroke=INK, sw=0.35)
    n = rot(u, 90)
    h = Hand("palm", wrist=(70, 0)).rest_thumb()
    pad = sub(top, mul(u, 1.8))
    p = h.view("thumb", tilt=TILT).place("i", pad, distal=slope, k=0.6)
    on_edge(p, pad, k=0.6, along=slope + 180, spread=0.35)
    p.draw(f, z=0)
    c = p.at(5.0, 1.5, -1.8)
    f.arrow([add(c, mul(n, 4.2)), add(c, mul(n, 0.6))], kind="force", z=50)
    hwarn("atlas palm", p)
    return f


def grid(rows, path, gap=3.0, row_gap=1.5):
    """Lay out figures in centred rows, each with a caption under it.
    rows: lists of (figure, caption)."""
    cap_h = 5.0
    widths = [sum((f.x1 - f.x0) * f.scale for f, _ in r) + gap * (len(r) - 1)
              for r in rows]
    W = max(widths)
    out, y, n = [], 0.0, 0
    for r, w in zip(rows, widths):
        x = (W - w) / 2
        h = max((f.y1 - f.y0) * f.scale for f, _ in r)
        for f, cap in r:
            fw, fh = f.x1 - f.x0, f.y1 - f.y0
            inner = f.svg().split("\n", 1)[1].rsplit("</svg>", 1)[0]
            out.append(f'<clipPath id="g{n}"><rect x="0" y="0" width="{fw:.2f}" '
                       f'height="{fh:.2f}"/></clipPath>')
            out.append(f'<g transform="translate({x:.2f},{y + h - fh * f.scale:.2f}) '
                       f'scale({f.scale:.5f})"><g clip-path="url(#g{n})">{inner}</g></g>')
            out.append(f'<text x="{x + fw * f.scale / 2:.2f}" y="{y + h + 3.8:.2f}" '
                       f'font-family="{FONT}" font-size="2.9" font-weight="600" '
                       f'text-anchor="middle">{esc(cap)}</text>')
            x += fw * f.scale + gap
            n += 1
        y += h + cap_h + row_gap
    H_ = y - row_gap
    with open(path, "w") as fh_:
        fh_.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" '
                  f'height="{H_:.2f}mm" viewBox="0 0 {W:.2f} {H_:.2f}">\n'
                  + "\n".join(out) + "\n</svg>\n")


def hand_atlas_fig(path):
    k = tile_profile()
    pinch = pinch_panel("narrow", labels=False,
                        frame=(-TILE_W / 2, 4.6 - TILE_H, TILE_W / 2, 4.6))
    rows = [[(atlas_jug(), "jug"), (atlas_grip("open"), "open hand"),
             (atlas_grip("half"), "half crimp"), (atlas_grip("lock"), "full crimp")],
            [(sloper_closeup(0, labels=False, frame=(k["x0"], -9.0, k["x0"] + TILE_W, 7.4)),
              "sloper"),
             (pinch, "pinch (from above)"),
             (pocket_atlas(), "pocket (two fingers)")],
            [(atlas_undercling(), "undercling"),
             (thumb_catch_panel(labels=False, **tile_profile()), "thumb catch"),
             (atlas_palm(), "palm press")]]
    grid(rows, path)


def pocket_atlas():
    f = pocket_profile(True, labels=False, **tile_profile(-11.0))
    pull(f, WX - 1.4, -4.8)
    return f


# ---------------------------------------------------------------- build


def build(out):
    hold_angle_fig(out + "/hands-hold-angle.svg")
    jug_fig(out + "/jug.svg")
    open_hand_fig(out + "/open-hand.svg")
    half_crimp_fig(out + "/half-crimp.svg")
    full_crimp_fig(out + "/full-crimp.svg")
    pinch_fig(out + "/pinch.svg")
    sloper_fig(out + "/sloper.svg")
    pocket_fig(out + "/pocket.svg")
    sidepull_fig(out + "/sidepull.svg")
    gaston_fig(out + "/gaston.svg")
    undercling_fig(out + "/undercling.svg")
    palming_fig(out + "/palming.svg")
    mantle_fig(out + "/mantle.svg")
    volume_mantle_fig(out + "/volume-mantle.svg")
    thumb_catch_fig(out + "/thumb-catch.svg")
    wrap_fig(out + "/wrap.svg")
    regrip_fig(out + "/regrip.svg")
    hand_atlas_fig(out + "/hand-atlas.svg")


if __name__ == "__main__":
    import sys
    build(sys.argv[1])
