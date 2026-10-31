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
                reach = c.reach(s)
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


# side profiles of a grip: from x0 to the wall, and from where the frame
# cuts the forearm (H.FOREARM_SHOWN below the wrist) up to y1
GRIP_FRAME = dict(x0=-12.0, y1=8.6)


def top_of(p, y1, height, shown=H.FOREARM_SHOWN):
    """A frame's top: y1, or `height` cm above where the frame cuts the
    forearm of the Posed hand p, `shown` cm below the wrist."""
    return y1 if height is None else p.forearm_point(shown)[1] + height


def drag_face():
    """Three-finger drag on a rounded edge, seen from behind; the little
    finger curled off the hold."""
    h = Hand("open", fingers={"i": (12, 30, 40), "m": (12, 30, 40), "r": (12, 30, 40),
                              "l": (55, 95, 60)}).rest_thumb()
    p = h.view("back", a0=92)
    p.move_point(pad_point(h, "m", 0.55), (-0.2, 2.2))
    b = Fig(-7.6, p.forearm_point()[1], 11.6, 5.2, scale=CLOSE)
    face_edge(b, (0.2, 0.0), 14.6, 4.2, rounded=True)
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
    combine([a, b], path, gap=4, labels=["a", "b"], align="top",
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
    combine([a, b], path, gap=4, labels=["a", "b"], align="top",
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
    combine([a, b], path, gap=4, labels=["a", "b"], align="top",
            captions=["full crimp, side view", "thumb lock"])


def pocket_profile(safe, labels=True, x0=-14.5, y1=5.5, height=None, shown=H.FOREARM_SHOWN):
    """Two-finger pocket seen from the little-finger side: the ring finger
    (grey, behind) in the hole, the little finger (in front) either kept
    parallel or curled into the palm."""
    # the index, out of the hole, hangs loose (hidden behind); the thumb
    # rests along it, in front of the palm, so it shows grey below the
    # fingers and the curled little finger stands out against it
    little = (8, 22, 12, 3) if safe else (70, 95, 45, 3)
    h = Hand("pocket", fingers={"l": little, "r": (30, 60, 25, -3), "i": (35, 60, 25)})
    h.rest_thumb()
    p = h.view("little", tilt=TILT)
    pad = (WX - 1.3, -0.05)
    p.place("r", pad, distal=-8, k=0.8)
    p.reach("m", add(pad, (0.3, 0.0)), k=0.8)
    if safe:
        p.reach("l", (WX - 3.95, -1.3), k=0.75)
    f = profile_frame(x0, y1=top_of(p, y1, height, shown), posed=p, shown=shown)
    # a hold in section, with the pocket cut into its front face
    blk = [(WX, 4.0), (WX - 3.0, 3.5), (WX - 3.9, 2.0), (WX - 3.9, -1.6),
           (WX - 3.2, -3.8), (WX, -4.4)]
    f.smooth(blk, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    H.xray_outline(f, blk, 0.5)
    cav = [(WX - 4.2, 1.75), (WX - 1.2, 1.85), (WX - 0.55, 0.85), (WX - 1.1, -0.15),
           (WX - 4.2, -0.2)]
    f.smooth(cav, z=-4.9, fill=PALE, stroke=INK, sw=0.3, tension=0.5)
    f.line((WX - 3.92, 1.7), (WX - 3.92, -0.15), z=-4.8, sw=0.6, stroke=PALE)
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
    combine([pocket_profile(True), pocket_profile(False)], path, gap=4, align="top",
            labels=["a", "b"], captions=["safer", "stronger but riskier"])


# ---------------------------------------------------------------- face-on hands


def face_edge(f, c, w, h, rounded=False, z=-5):
    """A horizontal edge seen face-on (a long bar), centred on c."""
    x, y = c
    r = h * (0.5 if rounded else 0.25)
    pts = [(x - w / 2 + r, y + h / 2), (x + w / 2 - r, y + h / 2),
           (x + w / 2, y), (x + w / 2 - r, y - h / 2), (x - w / 2 + r, y - h / 2),
           (x - w / 2, y)]
    f.smooth(pts, z=z, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    H.xray_outline(f, pts, 0.5)
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


def pinch_panel(kind, labels=True, x1=8.2, top=1.3, y0=None, scale=CLOSE,
                shown=H.FOREARM_SHOWN, size=None):
    """A pinch seen from above: the wall along the top, the hold sticking out
    toward the climber, the hand's index-finger edge facing you. The thumb
    presses one face and the fingers the opposite face. The arm comes in
    from the lower left: the frame's left edge cuts it `shown` cm below the
    wrist, its bottom edge 2 cm below that (or at y0) and its top is the
    back of the wall (`top`). size=(w, h) instead fixes the frame's size,
    its bottom 3 cm below the cut (an atlas tile)."""
    if kind == "narrow":
        # a 3 cm rib: the thumb pad on one face, the curled index on the
        # other, curled far enough to bring the palm in for the thumb to reach
        h = Hand("pinch", fingers={f_: (55, 35, 10) for f_ in "imrl"})
        cf, ct = (1.5, -2.4), (-1.5, -4.1)
        p = h.view("thumb", tilt=TILT, flip=True).place("i", cf, a0=25, k=0.65)
        # the shorter fingers land further out along the face
        on_edge(p, cf, k=0.65, dx=0.0, slide=[(1.5, -0.3), (1.5, -4.4)])
        p.thumb_to(ct, part="pad", k=0.6, facing=0)
        nf, nt = (1, 0), (-1, 0)
    elif kind == "wide":
        # a 6 cm block: thumb on one face, fingers flat on the other
        h = Hand("pinch", fingers={f_: (55, 15, 0) for f_ in "imrl"})
        cf, ct = (3.0, -2.2), (-3.0, -3.8)
        p = h.view("thumb", tilt=TILT, flip=True).place("i", cf, a0=20, k=0.65)
        on_edge(p, cf, k=0.65, dx=0.0, slide=[(3.0, -0.3), (3.0, -4.4)])
        p.thumb_to(ct, part="pad", k=0.6, facing=0)
        nf, nt = (1, 0), (-1, 0)
    else:
        # the ridge of a volume: the thumb on the near face, the fingers over
        # the ridge on the far face, the hand coming up from the lower left
        # like the other two
        apex = (0.0, -7.0)
        lf = norm(sub((-8.0, 0), apex))
        rf = norm(sub((8.0, 0), apex))
        nt, nf = rot(lf, 90), rot(rf, -90)
        ct = add(apex, mul(lf, 4.4))
        cf = add(apex, mul(rf, 5.4))
        h = Hand("pinch", fingers={f_: (20, 25, 8) for f_ in "imrl"})
        p = h.view("thumb", tilt=TILT, flip=True).place("i", cf, a0=20, k=0.6)
        on_edge(p, cf, k=0.6, dx=0.0, slide=[add(apex, mul(rf, 0.4)), add(apex, mul(rf, 10.0))])
        p.thumb_to(ct, part="pad", k=0.55,
                   facing=math.degrees(math.atan2(-nt[1], -nt[0])))
    cut = p.forearm_point(shown)
    x0 = cut[0]
    if size:
        x1, y0 = x0 + size[0], cut[1] - 3.0
        top = y0 + size[1]
    f = Fig(x0, cut[1] - 2.0 if y0 is None else y0, x1, top, scale=scale)
    wall_top(f, 0.0, x0, x1, depth=top)
    if kind == "narrow":
        hold = [(-1.5, 0), (-1.5, -4.6), (1.5, -4.6), (1.5, 0)]
        f.poly(hold, z=-5, fill=DARK, stroke=INK, sw=0.35)
    elif kind == "wide":
        hold = [(-3, 0), (-3, -4.6), (3, -4.6), (3, 0)]
        f.poly(hold, z=-5, fill=DARK, stroke=INK, sw=0.35)
    else:
        hold = [(-8.0, 0), apex, (8.0, 0)]
        f.poly(hold, z=-12, fill=LIGHT, stroke=INK, sw=0.35)
    H.xray_outline(f, hold)
    p.draw(f, z=0)
    inward(f, cf, nf)
    inward(f, ct, nt)
    if kind == "narrow" and labels:
        f.text("wall", (x1 - 1.0, 0.75), size=7)
        f.label("thumb", (-8.6, -6.0), to=p.joint("t", "ip"), size=7)
        f.label("index", (6.0, -8.6), to=p.joint("i", "pip"), size=7)
    hwarn("pinch " + kind, p)
    return f


def pinch_fig(path):
    # each panel ends just right of its force arrow; a common bottom edge
    # makes the three the same height
    right = {"narrow": 7.0, "wide": 8.2, "volume": 8.2}
    y0 = min(pinch_panel(k, x1=x1).y0 for k, x1 in right.items())
    combine([pinch_panel(k, x1=x1, y0=y0) for k, x1 in right.items()],
            path, gap=3, labels=["a", "b", "c"],
            captions=["narrow pinch", "wide pinch", "volume edge"])


def thumb_catch_panel(labels=True, x0=-13.5, y1=6.0, height=None, shown=H.FOREARM_SHOWN,
                      press=True):
    """Fingers over a rounded edge, the thumb pressing up into a dimple on
    its underside; press=False leaves off the arrow of the fingers pressing
    down."""
    dimple = (WX - 1.9, -2.95)
    p = grip_pose("open")
    p.thumb_to(add(dimple, (-0.2, -0.3)), part="tip")
    f = profile_frame(x0, y1=top_of(p, y1, height, shown), posed=p, shown=shown)
    rounded_lip(f, WX, 0, depth=2.6, height=4.2)
    f.circle(dimple, 0.38, z=-4.9, fill=INK, stroke=None)
    p.draw(f, z=0)
    tip = p.joint("t", "tip")
    f.arrow([add(tip, (-1.0, -3.6)), add(tip, (-0.3, -1.2))], kind="force")
    if press:
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
    ridge = (WX - 4.4, -0.6)
    up = norm(sub((WX, 5.0), ridge))
    lo = norm(sub((WX, -9.0), ridge))
    on_up = add(ridge, mul(up, 2.2))
    h = Hand("open", fingers={f_: (25, 30, 10) for f_ in "imrl"})
    p = h.view("thumb", tilt=TILT).place("i", on_up, a0=110, k=0.6)
    on_edge(p, on_up, k=0.6, along=math.degrees(math.atan2(up[1], up[0])), spread=0.3,
            slide=[add(ridge, mul(up, 0.3)), (WX, 5.0)])
    press = add(ridge, mul(lo, 4.0))
    out = rot(lo, -90)
    p.thumb_to(add(press, mul(out, 0.05)), part="pad", k=0.6,
               facing=math.degrees(math.atan2(-out[1], -out[0])))
    b = profile_frame(-13.5, y1=6.0, posed=p)
    b.poly([(WX, 5.0), ridge, (WX, b.y0)], z=-12, fill=LIGHT, stroke=INK, sw=0.35)
    p.draw(b, z=0)
    b.arrow([add(press, mul(out, 4.4)), add(press, mul(out, 1.9))], kind="force")
    # the leader runs under the force arrow to the thumb, not through it
    label_lines(b, ["thumb pad", "presses up"], (-10.6, -8.2), to=p.joint("t", "ip"))
    hwarn("thumb catch b", p)
    combine([a, b], path, gap=4, labels=["a", "b"], align="top",
            captions=["thumb catch", "thumb press on a volume"])


def regrip_fig(path):
    panels = []
    for k in range(2):
        drag = Hand("open").rest_thumb()
        pd = drag.view("back", a0=90)
        pd.move_point(pad_point(drag, "m", 0.55), (-4.6, 3.6))
        crimp = Hand("half").rest_thumb()
        pc = crimp.view("back", a0=90)
        pc.move_point(pad_point(crimp, "m", 0.85), (4.9, 3.3))
        # each panel cuts the arm of its own hand H.FOREARM_SHOWN below the
        # wrist; the drag, ghosted in panel 2, is cut short there
        f = Fig(-11, (pd if k == 0 else pc).forearm_point()[1], 11, 10.2, scale=CLOSE)
        face_edge(f, (0, 2.0), 19, 3.2)
        # the incut sweet spot on the right half, a screw hole beside it
        f.poly([(1.8, 3.3), (8.5, 3.3), (8.0, 2.7), (2.3, 2.7)], z=-4.8, fill=INK,
               stroke=None)
        f.circle((5.2, 1.5), 0.45, z=-4.8, fill="#b0b0b0", stroke=INK, sw=0.25)
        if k == 0:
            pd.draw(f, z=0)
            f.circle((5.2, 1.5), 1.6, z=40, stroke=INK, sw=0.3, fill=None)
            f.label("aim at the screw hole", (5.0, -8.4), to=(5.2, -0.1), size=7)
        else:
            pd.draw(f, z=-3, ghost=True)
            pc.draw(f, z=0)
            f.arrow([(-4.6, 8.4), (0.2, 9.3), (3.4, 8.9)], kind="move")
            label_lines(f, ["half crimp", "in the incut"], (-1.4, f.y0 + 2.0))
            hwarn("regrip", pc)
        panels.append(f)
    combine(panels, path, gap=4, labels=["1", "2"], align="top",
            captions=["catch where you can", "walk the fingers to the incut"])


def wrap_fig(path):
    """An arete seen from above: palm and thumb on one face, fingers round
    the edge onto the other."""
    apex = (0.0, -3.0)
    lf, rf = ang(135), ang(45)               # along the faces, away from the edge
    out_l, out_r = rot(lf, 90), rot(rf, -90)  # out of each face
    on_l = add(apex, mul(lf, 2.8))
    # the palm lies flush on the right face, the fingers bend round the edge
    # the thumb lies flat in the plane of the palm, on the same face
    h = Hand("wrap", fingers={f_: (9, 75, 5) for f_ in "imrl"},
             thumb=dict(ra=50, pa=0, rot=42, mcp=0, ip=0))
    p = h.view("thumb", tilt=TILT).place("i", on_l, a0=224, k=0.6)
    on_edge(p, on_l, k=0.6, dx=0.0)
    # the arm runs off to the right: the right edge cuts it
    x1, top = p.forearm_point()[0], 7.4
    f = Fig(-11.0, -10.5, x1, top, scale=CLOSE)
    f.poly([apex, add(apex, mul(lf, 16)), (-11, top), (x1, top), add(apex, mul(rf, 16))],
           z=-20, fill=PALE, stroke=None)
    f.line(apex, add(apex, mul(lf, 16)), z=-19, sw=0.7)
    f.line(apex, add(apex, mul(rf, 16)), z=-19, sw=0.7)
    f.text("arête", (0.0, 1.0), size=7)
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
        t = math.tan(math.radians(slope))
        cx = WX - 1.3
        pt = (cx, -(WX - cx) * t)
        h = Hand("half", fingers={f_: (45, 90, 8) for f_ in "imrl"})
        p = h.view("thumb", tilt=TILT).place("i", pt, distal=a3, k=0.85)
        on_edge(p, pt, k=0.85, along=180 + slope, spread=0.3)
        H.tuck_thumb(p, "half")      # against the index finger, as in a half crimp
        # the figure is about the edges, so it stops just below the wrist
        f = profile_frame(-9.6, y1=7.6, posed=p, shown=1.0)
        edge_profile(f, WX, 0, depth=3.2, height=3.6, slope=slope)
        x0 = WX - 2.8
        f.line((x0, -(WX - x0) * t + 0.07), (WX - 0.15, -0.15 * t + 0.07), z=-4.9,
               sw=0.5, stroke=WHITE)
        p.draw(f, z=0)
        f.arrow([(WX - 1.0, -3.9), (WX - 1.0, -6.6)], kind="force")
        if slope > 0:
            f.arrow([add(pt, mul(ang(slope), -0.6)), add(pt, mul(ang(slope), -3.6))],
                    kind="move", z=45)
        f.text(note, (-2.6, 6.7), size=7)
        hwarn("hold angle", p)
        panels.append(f)
    combine(panels, path, gap=3, captions=[c for _, c, _, _ in specs], align="top")


# ---------------------------------------------------------------- filmstrip

# The filmstrip's hands are drawn at the hand atlas's size, so that five
# frames fit the page width.
FILM = CLOSE * 0.73


def _clearance(p, surf, poly):
    """How far the Posed hand p keeps clear of a hold (outline polyline
    surf, closed polygon poly), in cm, negative where it cuts in: its palm,
    its fingers, its forearm and wrist."""
    def gap(q):
        d = H.nearest(surf, q)[0] ** 0.5
        return -d if H.inside(q, poly) else d
    h = p.hand
    palm = min(gap(p.xy(q)) for q in h.palm_solid()[::2] + h.thenar_solid()[::2])
    fingers = min(gap(p.xy(q, f)) for f in "imrl" for s in h.finger_solids(f)[:6]
                  for q in s[::3])
    arm = min(gap(p.xy(q)) for q in h.forearm_solid(14)[::2] + h.wrist_solid()[::2])
    return palm, fingers, arm


def filmstrip_sloper(path):
    """'In motion' strip: re-gripping a dome sloper, seen from the thumb
    side as the other close-ups are. The fingertips catch the front of the
    dome with the palm off it; the pads drag over the top; the palm comes
    on; the thumb finds a spot under the hold; the wrist drops below it and
    the arm hangs. The dome is the one the last frames' hand drapes over
    (dome_under, as in the sloper close-up), so it is the same in every
    frame; in the first two the hand is turned about the index finger's pad
    until its palm stands off the dome by `gap` cm without the fingers or
    the arm cutting into it."""
    def hand(s, fingers=None, a0=None, gap=None, wrist=(0, 0), thumb=None):
        """The hand with the index finger's pad s cm along the dome's
        surface, turned to a0 or fitted to stand `gap` cm off it."""
        pad, u = H.point_along(surf, s)

        def at(a0):
            h = Hand("sloper", fingers=fingers, wrist=wrist)
            return h.view("thumb", tilt=TILT).place("i", pad, a0=a0, k=0.55)
        if a0 is None:
            def miss(a0):
                palm, fing, arm = _clearance(at(a0), surf, poly)
                return (palm - gap) ** 2 + 10 * (min(fing + 0.02, 0) ** 2 +
                                                 min(arm - 0.3, 0) ** 2)
            a0 = min(range(20, 131, 3), key=miss)
            a0 = min((a0 + 0.5 * i for i in range(-4, 5)), key=miss)
        p = at(a0)
        on_edge(p, pad, k=0.55, along=math.degrees(math.atan2(-u[1], -u[0])), spread=0.32,
                slide=surf)
        if thumb == "tuck":
            # against the index finger, clear of the dome
            H.tuck_thumb(p, "half")
        elif thumb is None:
            p.hand.rest_thumb()
        else:
            # the pad pressing up on the dome's underside
            tp, tu = H.point_along(surf, thumb)
            p.thumb_to(tp, part="pad", k=0.6, facing=math.degrees(math.atan2(tu[0], -tu[1])))
        return p
    # the last frames: the hand draped as in the hand atlas's sloper
    last = Hand("sloper").view("thumb", tilt=TILT).place("i", (WX - 1.7, 4.0), distal=15,
                                                         k=0.55)
    # its top rounded off where it meets the wall, which the hand no longer
    # covers in the first frames
    dome = [(WX, 4.7), (WX - 0.6, 4.55)] + dome_under(last)[2:]
    surf = H.outline(dome, 0.55)
    poly = surf + [(WX + 1, dome[-1][1]), (WX + 1, dome[0][1])]
    s_last = H.nearest(surf, (WX - 1.7, 4.0))[1]
    poses = [hand(5.4, {f: (35, 65, 35) for f in "imrl"}, gap=1.2, wrist=(15, 0),
                  thumb="tuck"),
             hand(3.6, {f: (22, 40, 28) for f in "imrl"}, gap=0.6, wrist=(10, 0),
                  thumb="tuck"),
             hand(s_last, a0=last.a0),
             hand(s_last, a0=last.a0, thumb=16.5),
             hand(s_last, a0=last.a0, thumb=16.5, wrist=(-25, 0))]
    frames = []
    for i, p in enumerate(poses):
        x1 = WX + 2.4 / FILM + 0.01
        f = Fig(x1 - 31.3 / FILM, -17.4, x1, 7.6, scale=FILM)
        H.wall_profile(f, WX, f.y0, f.y1)
        f.smooth(dome, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.55)
        H.xray_outline(f, dome, 0.55)
        p.draw(f, z=0)
        if i == 4:
            f.arrow([(0.6, -7.6), (0.6, -11.4)], kind="force")
        hwarn(f"filmstrip-sloper {i + 1}", p)
        frames.append(f)
    filmstrip(frames, path, captions=[
        "catch with the fingertips", "drag the pads over", "bring the palm on",
        "find a thumb spot below", "wrist below, hang low"])


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
            # the left arm hangs straight and the right hand has only just
            # reached the jug: the left leg, pushing left, does the work
            # the body bows away from the sidepull
            c = Climber((38, 120), lean=-14, bend=8, lh=g, rh=grip(T),
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        elbows={"l": "down", "r": "out"},
                        leg_len={"l": 1.0, "r": .95}, active=("lthigh",))
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


def _gaston_plan(f, at, s=0.7):
    """A small top-down inset of a gaston with the right hand, centred on
    the shoulders at `at`, `s` units per cm: the wall at the top, the
    elbow out to the side and the forearm coming back to the hold, which
    the hand pushes away from the body."""
    def P(x, y):
        return add(at, (x * s, y * s))
    wall = 24
    f.line(P(-24, wall), P(62, wall), sw=0.6, z=70)
    k = -24
    while k < 62:
        f.line(P(k, wall), add(P(k, wall), (2, 3)), sw=0.18, stroke=MID, z=70)
        k += 4
    f.poly([P(30, wall), P(38, wall), P(37, wall - 3.5), P(31, wall - 3.5)], z=70,
           fill=DARK, stroke=INK, sw=0.25)
    shoulders = [P(22 * math.cos(math.radians(t)), 9 * math.sin(math.radians(t)))
                 for t in range(0, 360, 20)]
    f.smooth(shoulders, z=70, fill=WHITE, stroke=INK, sw=0.3)
    f.circle(P(0, 1), 7.5 * s, z=71, fill=HAIR, stroke=INK, sw=0.25)
    # the arm, shoulder to elbow to hand, as a white limb with an outline
    arm = [P(19, 0), P(43, 1), P(34, wall - 3.5)]
    f.poly(arm, closed=False, sw=2.8, stroke=INK, z=71)
    f.poly(arm, closed=False, sw=2.1, stroke=WHITE, z=72)
    f.arrow([P(48, 10), P(63, 10)], kind="force", z=73)
    f.text("from above", P(14, -17), size=6.5)


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
            c = Climber((40, 116), lean=-18, bend=8, lh=g, rh=grip(T),
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
            # the gaston arm (drawn by draw_arm, so not in the default)
            # pushes, and the left foot pushes back
            c = Climber(None, shoulders=(-34, 166), lh=grip(T), rh=None,
                        lf={"at": stand(LF)}, rf={"at": stand(RF)},
                        elbows={"l": "out"}, leg_len={"l": .93, "r": .95},
                        order=["lleg", "rleg", "torso", "larm"],
                        active=("+rupper", "+rfore", "+lthigh"))
            c.draw(f)
            el = (13, 159)
            c.draw_arm(f, "r", el, g, z=4)
            f.arrow([add(g, (5, 12)), add(g, (24, 12))], kind="force")
            f.label("elbow out", (50, 142), to=add(el, (2, -2)))
            f.label("thumb down", (-8, 232), to=add(g, (1.8, -6.5)))
            f.arrow([add(stand(LF), (-2, 6)), add(stand(LF), (-20, 6))], kind="force")
            f.label("body left of it", (-30, 40), size=7.5)
            # from behind, the forearm points into the wall and shows only
            # as a stub, so an inset shows the arm from above
            _gaston_plan(f, (36, 42))
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
            # the legs stand up into the hold (the left thigh is hidden)
            c = Climber(None, lh=reach_to, active=("+rthigh",), **kw)
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


def dome_under(p, R=lambda q: q):
    """The points of a dome sloper (drawn with tension 0.55) on a wall at
    x = WX, turned by R with the wall, whose front follows the palm side of
    the Posed hand p a hair inside it: the hand draped over it."""
    h = p.hand
    hand_side = []
    ch = h.finger("i")
    A3, N3, _ = ch["frames"][3]
    for s in (1.7, 1.2, 0.6):
        hand_side.append(p.xy(H.vadd(H.vadd(ch["dip"], H.vmul(A3, s)), H.vmul(N3, -0.68))))
    for j, k in (("dip", 2), ("pip", 1)):
        F = ch["frames"]
        n = H.vnorm(H.vadd(F[k][1], F[k + 1][1]))
        hand_side.append(p.xy(H.vadd(ch[j], H.vmul(n, -0.7))))
    A1, N1, _ = ch["frames"][1]
    hand_side.append(p.xy(H.vadd(H.vadd(ch["mcp"], H.vmul(A1, 1.6)), H.vmul(N1, -0.9))))
    hand_side += [p.at(7.4, 2.8, -1.4), p.at(4.9, 2.6, -1.55)]
    return [R((WX, 4.9))] + hand_side + [R((WX - 3.0, -5.6)), R((WX, -6.9))]


def sloper_closeup(angle=20, scale=CLOSE, labels=True, x1=5.4, y1=9.0, distal=-15,
                   shown=H.FOREARM_SHOWN, size=None):
    """An open hand draped over a dome sloper on a wall overhanging by
    `angle` degrees, seen from the thumb side: palm and finger pads on the
    hold, wrist dropped below it, the pull straight down the arm. `distal`
    is the direction of the fingertips against a vertical wall (the larger,
    the steeper the hand). The frame runs from x1 (right) and y1 (top) to
    where it cuts the arm, `shown` cm below the wrist; size=(w, h) instead
    fixes its size, from x1 and the cut (an atlas tile)."""
    def R(q):
        return rot(q, angle)
    # the hand, posed against a vertical wall at x = WX, then turned with it
    h = Hand("sloper")
    pad = R((WX - 1.7, 4.0))
    p = h.view("thumb", tilt=TILT).place("i", pad, distal=distal + angle, k=0.55)
    on_edge(p, pad, k=0.55, along=200 + angle, spread=0.3)
    cut = p.forearm_point(shown)
    if size:
        y1 = cut[1] + size[1]
    f = Fig(x1 - size[0] if size else cut[0] - 3.0, cut[1], x1, y1, scale=scale)
    x_at = lambda y: R((WX, 0))[0] - (y - R((WX, 0))[1]) * math.tan(math.radians(angle))
    wall_side(f, x_at(f.y0), f.y0, y1, angle=angle)
    dome = dome_under(p, R)
    f.smooth(dome, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.55)
    H.xray_outline(f, dome, 0.55)
    h.rest_thumb()
    p.draw(f, z=0)
    f.arrow([(0.6, -6.3), (0.6, max(-10.2, f.y0 + 0.5))], kind="force")
    if labels:
        f.label("palm and pads", (-5.2, 7.8), to=lerp(p.joint("i", "pip"),
                                                       p.joint("i", "dip"), 0.5))
        f.label("wrist below", (-4.6, f.y0 + 1.6), to=p.at(-0.4, 0.3, -1.8))
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
    # the right side shortens over the pressing palm
    c = Climber((-8, 124), lean=-8, bend=6, lh=grip(T), rh=palm,
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
        Fh, Fl = at(TOP - 92), at(TOP - 150)
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
            # shoulders over the hands, hips close to the lip, so the
            # weight is over the hands and the high foot
            c = Climber((13, 226), view="side", lean=34, bend=10,
                        lh=add(palm2, (-1, 3)), rh=add(palm, (-1, 3)),
                        lf={"at": (WX - 3, 150), "angle": -50, "contact": "ball"},
                        rf={"at": (WX + 13, TOP + 1), "angle": 0, "contact": "ball"},
                        leg_len={"r": 0.85},
                        active=("+rthigh",))   # the right leg steps up
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
            # the palm presses and the legs rock over onto the high foot
            # (the left thigh is hidden behind the right)
            c = Climber((-8, 164), view="side", lean=1, bend=8, lh=palm, rh=reach_to,
                        lf={"at": foot_h}, rf={"at": foot_h},
                        leg_len={"l": 0.85, "r": 0.85}, active=("+rthigh",))
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

TILE_W, TILE_H = 14.4, 19.4      # every tile's size in cm
# The atlas shows this much forearm below the wrist, in every tile: less
# than the other close-ups (H.FOREARM_SHOWN), so that three rows of tiles
# tall enough for an upright open hand stay within about 170 mm.
ATLAS_ARM = 2.5


def tile_x0(w=TILE_W):
    """The left edge of a profile tile `w` cm wide, ending at the wall."""
    return WX + 2.4 / CLOSE + 0.01 - w


def pull(f, x, y, down=True, length_=3.4):
    """A force arrow for the pull on the hold."""
    d = -1 if down else 1
    f.arrow([(x, y), (x, y + d * length_)], kind="force")


# Every tile cuts the arm ATLAS_ARM below the wrist. Where the arm hangs
# down (most grips) that is the tile's bottom edge; where it runs out
# sideways (the palm press, the pinch from above) it is the left edge.

def atlas_grip(kind):
    f, p = grip_profile(kind, x0=tile_x0(), height=TILE_H, shown=ATLAS_ARM)
    pull(f, WX - 1.1, -3.4 if kind == "open" else -2.8)
    hwarn("atlas " + kind, p)
    return f


def atlas_jug():
    h = Hand("jug")
    pad = (WX - 4.2, -0.2)
    p = h.view("thumb", tilt=TILT).place("i", pad, distal=-35, k=0.75)
    on_edge(p, pad, k=0.75, along=-8, spread=0.35)
    # the thumb pad on the jug's front face, below the lip, so that it
    # leaves the whole index finger hooked over the lip in view
    p.thumb_to((WX - 7.85, -1.2), part="pad", k=0.6, facing=0)
    f = profile_frame(tile_x0(), y1=top_of(p, None, TILE_H, ATLAS_ARM), posed=p,
                      shown=ATLAS_ARM)
    # a big incut jug: the fingers hook over its lip into the bucket behind
    jug = [(WX, -5.0), (WX - 5.0, -4.6), (WX - 7.2, -2.4), (WX - 7.7, 0.8),
           (WX - 7.2, 1.85), (WX - 6.4, 1.6), (WX - 5.6, 0.3), (WX - 2.8, -0.3),
           (WX, 0.4)]
    f.smooth(jug, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.35)
    H.xray_outline(f, jug, 0.35)
    p.draw(f, z=0)
    pull(f, WX - 1.4, -5.6)
    hwarn("atlas jug", p)
    return f


def atlas_undercling():
    """Palm up under a flake that faces down, pulling up: the thumb-side view
    mirrored, so the palm faces up and the wall stays on the right. The
    fingers curl up round the flake's edge, the wrist bends back a little
    and the forearm hangs down and a little out from below the hand."""
    flake = [(WX, -2.4), (WX - 5.6, -1.0), (WX - 6.8, 0.0), (WX - 6.0, 0.6),
             (WX - 3.0, 0.5), (WX, 1.6)]
    # the fingers curled enough for the little finger to reach the flake
    # too, the hand far enough from the wall for the knuckles to clear it
    h = Hand("undercling", fingers={f_: (18, 50, 25) for f_ in "imrl"})
    under = H.outline(flake, 0.4)
    pad = H.snap(under, (WX - 3.8, -1.6))
    p = h.view("thumb", tilt=TILT, flip=True).place("i", pad, a0=30, k=0.9)
    on_edge(p, pad, k=0.9, along=166, spread=0.3, slide=under)
    h.rest_thumb()
    f = profile_frame(tile_x0(), y1=top_of(p, None, TILE_H, ATLAS_ARM), posed=p,
                      shown=ATLAS_ARM)
    f.smooth(flake, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.4)
    H.xray_outline(f, flake, 0.4)
    p.draw(f, z=0)
    # the pull, up into the flake beside the thumb
    f.arrow([(WX - 6.2, -4.7), (WX - 6.2, -1.6)], kind="force")
    hwarn("atlas undercling", p)
    return f


def atlas_palm():
    """A palm pressed flat on a steep volume face, the wrist bent back
    (GRIPS "palm") so that the forearm comes in from the lower left and
    pushes into the face. The hand slides along the face until the tile's
    left edge, ATLAS_ARM below the wrist, is where it cuts the arm; at a
    51-degree face that leaves the fingertips just below the face's top."""
    slope = 51
    u = ang(slope)
    top = (WX, 6.4)                    # where the face meets the wall
    n = rot(u, 90)
    h = Hand("palm").rest_thumb()
    x0 = tile_x0()

    def pose(d):
        pad = sub(top, mul(u, d))
        p = h.view("thumb", tilt=TILT).place("i", pad, distal=slope, k=0.6)
        # the longer fingers lie on the face too, their tips short of its top
        on_edge(p, pad, k=0.6, along=slope + 180, spread=0.35, room=(1.0 - d, 8.0))
        return p
    d = 1.8
    p = pose(d)
    d -= (x0 - p.forearm_point(ATLAS_ARM)[0]) / u[0]
    p = pose(d)
    cut = p.forearm_point(ATLAS_ARM)
    # high enough for the fingertips; the arm's palm side leaves through
    # the bottom edge, just inside the corner
    y0 = cut[1] - 1.55
    f = profile_frame(x0, y0, y0 + TILE_H)
    low = sub(top, mul(u, 30))
    face = [add(top, (0, 4)), top, low, (WX, low[1])]
    f.poly(face, z=-12, fill=LIGHT, stroke=INK, sw=0.35)
    H.xray_outline(f, face)
    p.draw(f, z=0)
    c = p.at(5.0, 1.5, -1.8)
    f.arrow([add(c, mul(n, 4.2)), add(c, mul(n, 0.6))], kind="force", z=50)
    hwarn("atlas palm", p)
    return f


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
                       f'font-family="{FONT}" font-size="2.9" font-weight="600" '
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
    size = (TILE_W, TILE_H)
    rows = [[(atlas_jug(), "jug"), (atlas_grip("open"), "open hand"),
             (atlas_grip("half"), "half crimp"), (atlas_grip("lock"), "full crimp"),
             (pocket_atlas(), "pocket (two fingers)")],
            [(sloper_closeup(0, labels=False, x1=tile_x0(0), distal=15, shown=ATLAS_ARM,
                             size=size), "sloper"),
             (pinch_panel("narrow", labels=False, shown=ATLAS_ARM, size=size),
              "pinch (from above)"),
             (atlas_undercling(), "undercling"),
             (thumb_catch_panel(labels=False, x0=tile_x0(), height=TILE_H, shown=ATLAS_ARM,
                                press=False), "thumb catch"),
             (atlas_palm(), "palm press")]]
    # an overview plate: two rows of five, smaller than the close-ups, so
    # that it fits beside the chapter's opening text in the text width
    grid(rows, path, zoom=0.73)


def pocket_atlas():
    f = pocket_profile(True, labels=False, x0=tile_x0(), height=TILE_H, shown=ATLAS_ARM)
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
    filmstrip_sloper(out + "/filmstrip-sloper.svg")


if __name__ == "__main__":
    import sys
    build(sys.argv[1])
