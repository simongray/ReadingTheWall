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
hand faces you. Pinches are seen from above, wall at the top. The wrap and the
palm press are three-quarter views of the back of the hand, with the rock
drawn in the same projection (Hand.view's tilt and pitch).
"""

from climb import *
import hand as H
import plan
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
                              "l": (55, 95, 60)}).rest_thumb(out=2.0)
    p = h.view("back", a0=92)
    p.move_point(pad_point(h, "m", 0.55), (-0.2, 2.2))
    b = Fig(-7.6, p.forearm_point()[1], 11.6, 5.2, scale=CLOSE)
    face_edge(b, (0.2, 0.0), 14.6, 4.2, rounded=True)
    p.draw(b, z=0)
    label_lines(b, ["little", "finger off"], (9.2, -3.2), to=p.joint("l", "pip"))
    hwarn("drag face", p)
    return b


def open_hand_fig(path):
    a, p = grip_profile("open", plain=("pip",), **dict(GRIP_FRAME, y1=8.29))
    pip_arc(a, p, "≈40°")
    a.label("pads over the lip", (-4.0, 7.4), to=a_pad(p), anchor="middle")
    hwarn("open hand", p)
    b = drag_face()
    combine([a, b], path, gap=4, labels=["a", "b"], align="top",
            captions=["drag, side view", "three-finger drag"])


def a_pad(p, f="i", k=0.62):
    return p.xy(pad_point(p.hand, f, k))


def half_crimp_fig(path):
    frame = dict(GRIP_FRAME, y1=7.98, plain=("pip",))
    a, p = grip_profile("half", **frame)
    pip_arc(a, p, "≈90°")
    label_lines(a, ["end joint", "straight"], (-9.2, 1.6), to=p.joint("i", "dip"))
    # the full crimp as it is usually climbed, the thumb locked over the nail
    # (cut at the same depth as panel a, so their feet and the captions under them line up)
    shown = H.FOREARM_SHOWN
    while grip_pose("lock").forearm_point(shown)[1] > a.y0:
        shown += 0.01
    b, pb = grip_profile("lock", shown=shown, **frame)
    pb.xray_end(b)         # the bend the panel names lies under the thumb
    pip_arc(b, pb, "over 90°")
    label_lines(b, ["end joint", "bent back"], (-9.2, 1.6), to=pb.joint("i", "dip"))
    hwarn("half crimp", p, pb)
    combine([a, b], path, gap=4, labels=["a", "b"], align="top",
            captions=["half crimp", "full crimp, for comparison"])


def full_crimp_fig(path):
    """The full crimp from the side as it is usually climbed, the thumb
    locked over the index fingernail: the middle joint past 90 degrees, the
    end joint bent back and the A2 pulley, which the grip loads most."""
    a, p = grip_profile("lock", plain=("pip",), **dict(GRIP_FRAME, y1=8.21))
    p.xray_end(a)          # the bend the label names lies under the thumb
    # the angle to the left of the joint, leaving the top for the thumb
    pip_arc(a, p, "over 90°", at=add(p.joint("i", "pip"), (-5.2, 1.0)))
    label_lines(a, ["end joint", "bent back"], (-9.2, 1.6), to=p.joint("i", "dip"))
    label_lines(a, ["A2", "pulley"], (-9.9, -2.6), to=H.a2_point(p))
    th = p.hand.thumb()
    # the leader drops from the label's right end through clear space, off the finger
    a.label("thumb over the nail", (0.9, 7.6), to=p.xy(H.thumb_point(th, "nail", 0.55)),
            anchor="end")
    hwarn("full crimp", p)
    a.save(path)


def pocket_profile(safe, labels=True, x0=-14.5, y1=5.65, height=None, shown=H.FOREARM_SHOWN):
    """Two-finger pocket seen from the little-finger side: the ring and middle
    fingers (grey, behind) in the hole, the little finger (in front) either
    kept parallel or curled into the palm."""
    # the index, out of the hole, hangs loose behind the others, so it isn't
    # drawn; the thumb rests along it, in front of the palm, so it shows grey
    # below the fingers and the curled little finger stands out against it
    little = (28, 72, 35, 3) if safe else (70, 95, 45, 3)
    h = Hand("pocket", fingers={"l": little, "r": (24, 52, 20, -3)})
    h.rest_thumb(palm=2.1)
    p = h.view("little", tilt=TILT)
    pad = (WX - 1.3, -0.05)
    p.place("r", pad, distal=-8, k=0.8)
    # the middle finger lies a step lower in the hole, so that it shows as the
    # second finger in it
    p.reach("m", add(pad, (0.1, -0.75)), k=0.8)
    if safe:
        # its first segment in line with the ring finger's, the rest bending
        # loosely down to the hold's face below the hole
        p.reach("l", (WX - 3.95, -3.0), k=0.75)
    f = profile_frame(x0, y1=top_of(p, y1, height, shown), posed=p, shown=shown)
    # a hold in section, with the pocket cut into its front face
    blk = [(WX, 4.0), (WX - 3.0, 3.5), (WX - 3.9, 2.0), (WX - 3.9, -1.6),
           (WX - 3.2, -3.8), (WX, -4.4)]
    f.smooth(blk, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.5)
    H.xray_outline(f, blk, 0.5)
    cav = [(WX - 4.2, 1.75), (WX - 1.2, 1.85), (WX - 0.55, 0.65), (WX - 1.1, -0.95),
           (WX - 4.2, -1.0)]
    f.smooth(cav, z=-4.9, fill=HOLD_PALE, stroke=INK, sw=0.3, tension=0.5)
    f.line((WX - 3.92, 1.7), (WX - 3.92, -0.95), z=-4.8, sw=0.6, stroke=HOLD_PALE)
    p.draw(f, z=0, others="rm")
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
        cl = lerp(p.joint("l", "mcp"), p.joint("l", "pip"), 0.5)
        f.arrow([add(cl, mul(ul, 1.1)), add(cl, mul(ul, -1.1))], kind="force", z=50)
        if labels:
            label_lines(f, ["opposite", "pulls"], (-11.2, -6.6), to=add(cl, mul(ul, -0.9)))
            label_lines(f, ["little finger", "curled"], (-11.2, 3.4),
                        to=p.surface("l", "pip", "back", 0.9))
    hwarn("pocket", p)
    return f


def pocket_fig(path):
    # within the 92 mm that sit beside the steps
    combine([pocket_profile(True, x0=-14.2), pocket_profile(False, x0=-14.2)], path, gap=2.5, align="top",
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
        # a 3 cm rib: the thumb pad on one face, the index on the other, its
        # fingers bent as in a half crimp, as the entry says, which brings the
        # palm in for the thumb to reach
        h = Hand("pinch", fingers={f_: (35, 75, 5) for f_ in "imrl"})
        cf, ct = (1.5, -3.0), (-1.5, -3.5)
        p = h.view("thumb", tilt=TILT, flip=True).place("i", cf, a0=30, k=0.65)
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
        # set by hand: solved for this contact it ends bent back at both joints
        h.t = dict(ra=50, pa=28, rot=55, mcp=10, ip=10)
    cut = p.forearm_point(shown)
    x0 = cut[0]
    if size:
        x1, y0 = x0 + size[0], cut[1] - 3.0
        top = y0 + size[1]
    f = Fig(x0, cut[1] - 2.15 if y0 is None else y0, x1, top, scale=scale)
    wall_top(f, 0.0, x0, x1, depth=top)
    # a clear corner for the panel letter, which would otherwise sit on the hatching
    f.poly([(x0, 0.03), (x0, top), (x0 + 1.45, top), (x0 + 1.45, 0.03)], z=-18, fill=WHITE,
           stroke=None)
    if kind == "narrow":
        hold = [(-1.5, 0), (-1.5, -4.6), (1.5, -4.6), (1.5, 0)]
        f.poly(hold, z=-5, fill=DARK, stroke=INK, sw=0.35)
    elif kind == "wide":
        hold = [(-3, 0), (-3, -4.6), (3, -4.6), (3, 0)]
        f.poly(hold, z=-5, fill=DARK, stroke=INK, sw=0.35)
    else:
        hold = [(-8.0, 0), apex, (8.0, 0)]
        f.poly(hold, z=-12, fill=VOLUME, stroke=INK, sw=0.35)
    H.xray_outline(f, hold)
    p.draw(f, z=0)
    # on the narrow pinch the bent index stands out from the rib, so the
    # arrow presses on it near its tip, above the middle joint
    inward(f, (1.5, -2.6) if kind == "narrow" else cf, nf, gap=2.75 if kind == "narrow" else 2.1)
    if kind == "volume":
        # beside the thumb, which lies along the push
        inward(f, add(ct, mul(lf, 1.7)), nt, gap=0.5)
    else:
        inward(f, ct, nt)
    if kind == "narrow" and labels:
        f.text("wall", (x1 - 1.0, 0.75), size=7)
        f.label("thumb", (-8.6, -6.0), to=p.joint("t", "ip"), size=7)
        f.label("index", (5.2, -12.6), to=p.joint("i", "pip"), size=7)
    hwarn("pinch " + kind, p)
    return f


def pinch_fig(path):
    # each panel ends just right of its force arrow; a common bottom edge
    # makes the three the same height
    right = {"narrow": 7.42, "wide": 7.94, "volume": 7.94}
    y0 = -18.88
    combine([pinch_panel(k, x1=x1, y0=y0) for k, x1 in right.items()],
            path, gap=3, labels=["a", "b", "c"],
            captions=["narrow pinch", "wide pinch", "volume edge"])


def thumb_catch_panel(labels=True, x0=-13.5, y1=5.81, height=None, shown=H.FOREARM_SHOWN,
                      press=True):
    """Fingers over a rounded edge, the thumb pressing up into a dimple on
    its underside; press=False leaves off the arrow of the fingers pressing
    down."""
    dimple = (WX - 1.5, -2.55)
    p = grip_pose("open")
    p.thumb_to(add(dimple, (-0.15, -0.2)), part="tip")
    f = profile_frame(x0, y1=top_of(p, y1, height, shown), posed=p, shown=shown)
    # the rounded lip, with the dimple cut into its underside
    hold = [(WX, 0.05), (WX - 1.17, 0.0), (WX - 2.21, -0.35), (WX - 2.6, -1.2),
            (WX - 2.45, -2.0), (WX - 2.2, -2.5), (WX - 1.75, -2.2), (WX - 1.25, -2.3),
            (WX - 1.2, -3.1), (WX - 0.9, -3.65), (WX, -4.2)]
    f.smooth(hold, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.6)
    H.xray_outline(f, hold, 0.6)
    p.draw(f, z=0)
    tip = p.joint("t", "tip")
    # the thumb's push, in the gap beside it, up to the hold's underside
    f.arrow([(WX - 0.47, -7.4), (WX - 0.47, -4.35)], kind="force", head=2.0)
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
    p = h.view("thumb", tilt=TILT).place("i", on_up, a0=98, k=0.6)
    on_edge(p, on_up, k=0.6, along=math.degrees(math.atan2(up[1], up[0])), spread=0.3,
            slide=[add(ridge, mul(up, 0.3)), (WX, 5.0)])
    press = add(ridge, mul(lo, 4.0))
    out = rot(lo, -90)
    # set by hand: solved for this contact it foreshortens to a stump, bent back
    h.t = dict(ra=50, pa=12, rot=55, mcp=30, ip=0)
    b = profile_frame(-13.5, y1=5.81, posed=p)
    b.poly([(WX, 5.0), ridge, (WX, -9.0)], z=-12, fill=VOLUME, stroke=INK, sw=0.35)
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
        drag = Hand("open").rest_thumb(out=2.0)
        pd = drag.view("back", a0=90)
        pd.move_point(pad_point(drag, "m", 0.55), (-4.6, 3.6))
        crimp = Hand("half").rest_thumb(out=2.0)
        pc = crimp.view("back", a0=90)
        pc.move_point(pad_point(crimp, "m", 0.85), (4.9, 3.3))
        # each panel cuts the arm of its own hand H.FOREARM_SHOWN below the
        # wrist; the drag, ghosted in panel 2, is cut short there
        f = Fig(-11, (pd if k == 0 else pc).forearm_point()[1], 11, 9.74, scale=CLOSE)
        face_edge(f, (0, 2.0), 19, 3.2)
        # the incut sweet spot on the right half, a screw hole beside it
        f.poly([(1.8, 3.3), (8.5, 3.3), (8.0, 2.7), (2.3, 2.7)], z=-4.8, fill=INK,
               stroke=None)
        f.circle((5.2, 1.5), 0.45, z=-4.8, fill="#b0b0b0", stroke=INK, sw=0.25)
        if k == 0:
            pd.draw(f, z=0)
            f.circle((5.2, 1.5), 1.6, z=40, stroke=INK, sw=0.3, fill=None)
            label_lines(f, ["aim at the", "screw hole"], (7.2, -3.4), to=(5.2, -0.1))
        else:
            pd.draw(f, z=-3, ghost=True)
            pc.draw(f, z=0)
            f.arrow([(-4.6, 8.1), (0.2, 9.0), (3.4, 8.6)], kind="move")
            label_lines(f, ["half crimp", "in the incut"], (7.9, 9.1), to=pc.joint("m", "dip"))
            hwarn("regrip", pc)
        panels.append(f)
    combine(panels, path, gap=4, labels=["1", "2"], align="top",
            captions=["catch where you can", "walk the fingers to the incut"])


WRAP_TILT, WRAP_PITCH = 32, 15     # the wrap's view


def plane_arrow(f, p, at, along, length_=3.4, gap=0.6):
    """A force arrow toward page point `at`, along the page image of the
    hand-frame direction `along`, stopping `gap` cm short of it."""
    a, b = p.xy((0.0, 0.0, 0.0)), p.xy(along)
    u = norm(sub(b, a))
    f.arrow([sub(at, mul(u, gap + length_)), sub(at, mul(u, gap))], kind="force", z=50)


def wrap_fig(path):
    """An arête seen at an angle, its edge upright on the page: the palm and
    thumb on the near face, the fingers bending round the edge on to the far
    one. The rock is drawn in the hand's own projection: the near face is
    the plane z = -FACE of the hand frame and the far one the plane x = EDGE,
    so the fingers land on it from a side view of the same hand. The angle is
    the one at which the fingers visibly turn at the edge: seen from further
    round, their two directions project on to the same line and the bend
    disappears."""
    EDGE, FACE = 14.0, 2.1
    h = Hand("wrap")
    side = h.view("thumb", tilt=0, stagger=0, a0=90)
    for f_ in "imrl":
        y = H.MCP[f_][1]
        side.reach(f_, side.at(EDGE, y, -FACE - 1.6), k=0.8,
                   slide=[side.at(EDGE, y, -FACE + 0.5), side.at(EDGE, y, -FACE - 6)])
    # turned until the edge stands upright on the page

    def posed(a0):
        return h.view("back", a0=a0, tilt=WRAP_TILT, pitch=WRAP_PITCH)
    a0 = 0.0
    for _ in range(3):
        v = sub(posed(a0).at(EDGE, 10, -FACE), posed(a0).at(EDGE, -10, -FACE))
        a0 += 90 - math.degrees(math.atan2(v[1], v[0]))
    p = posed(a0).move_point((EDGE, 0, -FACE), (0, 0))
    # the arm runs off to the left: the left edge cuts it
    x0 = p.forearm_point()[0]
    top = p.xy(h.thumb()["tip"])[1] + 1.0
    x1, y0 = x0 + 27.24, top - 17.9
    f = Fig(x0, y0, x1, top, scale=CLOSE)
    Q = lambda x, y, z: p.xy((x, y, z))
    low, high = Q(EDGE, -40, -FACE), Q(EDGE, 40, -FACE)
    f.poly([low, high, Q(EDGE - 60, 40, -FACE), Q(EDGE - 60, -40, -FACE)], z=-20, fill=PALE,
           stroke=None)
    f.poly([low, high, Q(EDGE, 40, -FACE - 60), Q(EDGE, -40, -FACE - 60)], z=-20,
           fill="#cccccc", stroke=None)
    f.line(low, high, z=-19, sw=0.7)
    p.draw(f, z=0)
    # the edge carries on under the fingers, as a hidden line
    f.poly([low, high], closed=False, z=H.XRAY_Z, **H.XRAY_STYLE)
    f.text("arête", (1.6, top - 1.3), size=7, anchor="start")
    f.label("palm and thumb", (x0 + 5.6, top - 1.3), to=p.xy(H.vlerp(h.thumb()["cmc"],
                                                                     h.thumb()["mcp"], 0.8)), size=7)
    label_lines(f, ["fingers round", "the edge"], (x1 - 2.6, y0 + 2.2), to=p.joint("l", "tip"))
    plane_arrow(f, p, Q(6.8, 1.2, 1.2), (0, 0, -1), gap=0.0)
    plane_arrow(f, p, add(p.joint("m", "tip"), (0.5, 0)), (-1, 0, 0), length_=2.6)
    hwarn("wrap", p)
    f.save(path)


def hold_angle_fig(path):
    """Concept: incut, flat and sloping edges in profile, each pulled
    straight down by a half-crimping finger."""
    panels = []
    # the same half crimp on each edge, the forearm hanging straight down:
    # only the edge changes
    specs = ((-20, "positive (incut)", "incut locks it"),
             (0, "flat", "friction and curl"),
             (30, "negative (sloping)", "slides off"))

    def posed(slope):
        t = math.tan(math.radians(slope))
        cx = WX - 1.3
        pt = (cx, -(WX - cx) * t)
        # on the incut the fingertip comes down behind the lip, so it hooks
        flex, distal = ((10, 80, 22), -32) if slope < 0 else ((10, 86, 8), -10)
        h = Hand("half", fingers={f_: flex for f_ in "imrl"},
                 wrist=(-8, 0) if slope < 0 else None)
        p = h.view("thumb", tilt=TILT).place("i", pt, distal=distal, k=0.85)
        on_edge(p, pt, k=0.85, along=180 + slope, spread=0.3)
        # against the index finger, as in a half crimp, and low enough to leave
        # the edge in view
        H.tuck_thumb(p, "half", drop=0.5)
        return p, pt, t

    # the figure is about the edges, so it stops just below the wrist; the three
    # panels are cut at one height, the highest of the three
    y0 = max(posed(s)[0].forearm_point(1.0)[1] for s, _, _ in specs)
    for slope, cap, note in specs:
        p, pt, t = posed(slope)
        f = profile_frame(-9.6, y0=y0, y1=7.03)
        edge_profile(f, WX, 0, depth=3.2, height=3.6, slope=slope)
        x0 = WX - 2.8
        f.line((x0, -(WX - x0) * t + 0.07), (WX - 0.15, -0.15 * t + 0.07), z=-4.9,
               sw=0.5, stroke=WHITE)
        p.draw(f, z=0)
        f.arrow([(WX - 0.85, -3.9), (WX - 0.85, -6.6)], kind="force")
        if slope > 0:
            f.arrow([add(pt, mul(ang(slope), -0.3)), add(pt, mul(ang(slope), -2.3))],
                    kind="move", z=45)
        f.text(note, (-2.6, 6.13), size=7)
        hwarn("hold angle", p)
        panels.append(f)
    combine(panels, path, gap=3, captions=[c for _, c, _ in specs], align="top")


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


# the thumb in the filmstrip's last frames: up under the dome, at nearly its
# full length (solving for a contact there runs it into three joint limits,
# pointing at the viewer and bent back, which draws it as a stump)
UNDER_DOME = dict(ra=8, pa=80, rot=142, mcp=50, ip=50)


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
            p.hand.t = dict(thumb)
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
             hand(s_last, a0=last.a0, thumb=UNDER_DOME),
             hand(s_last, a0=last.a0, thumb=UNDER_DOME, wrist=(-25, 0))]
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
        "catch with\nthe fingertips", "drag the\npads over", "bring the\npalm on",
        "find a thumb\nspot below", "wrist below,\nhang low"])


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
    hand_side += [p.at(7.4, 2.2, -1.4), p.at(4.9, 1.7, -1.55)]
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
    f = Fig(x1 - size[0] if size else cut[0] - 2.41, cut[1], x1, y1, scale=scale)
    x_at = lambda y: R((WX, 0))[0] - (y - R((WX, 0))[1]) * math.tan(math.radians(angle))
    wall_side(f, x_at(f.y0), f.y0, y1, angle=angle)
    dome = dome_under(p, R)
    f.smooth(dome, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.55)
    H.xray_outline(f, dome, 0.55)
    h.rest_thumb()
    p.draw(f, z=0)
    # the pull, from just under the hold's lower face
    a, b = dome[-2], dome[-1]
    low = a[1] + (b[1] - a[1]) * (0.6 - a[0]) / (b[0] - a[0]) - 0.6
    f.arrow([(0.6, low), (0.6, max(low - 3.9, f.y0 + 0.5))], kind="force")
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
    panels.append(sloper_closeup(A))
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
# A reference plate: one small close-up per grip, all at the book's hand
# scale, each with a force arrow for the pull. Profiles (wall on the right)
# where a profile shows the grip; the pinch is seen from above and the palm
# press at three-quarters.

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
# sideways (the undercling, the pinch from above) it is the left edge.

def atlas_grip(kind):
    f, p = grip_profile(kind, x0=tile_x0(), height=TILE_H, shown=ATLAS_ARM)
    if kind == "lock":
        p.xray_end(f)
    # the open hand's thumb hangs low, so its arrow starts below the hold, between
    # the thumb and the wall
    pull(f, *((WX - 0.7, -4.6) if kind == "open" else (WX - 1.1, -2.8)))
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


# The undercling's flake (cm out of the wall, up it) has the shape of
# HOLD_PROFILES["undercling"] from the wall round to its top: the underside
# rises from the wall to a hollow, then drops to a lip that hangs down at its
# far end. The hollow is a little deeper, to take a fingertip at this scale.
FLAKE = [(0, -2.7), (1.45, -1.5), (3.05, -0.8), (4.5, -1.45), (5.65, -3.15), (6.4, -3.7),
         (7.1, -2.5), (6.9, 0.35), (4.5, 2.7), (0, 3.4)]


def atlas_undercling():
    """Palm up under a flake that faces down: the thumb-side view mirrored, so
    the palm faces up and the wall stays on the right. The fingers reach in
    under the lip and hook up behind it, into the hollow, with an open hand
    and the thumb pointing out. The arm is straight, as the entry asks, so the
    wrist bends forward and the forearm comes down to it from the upper left,
    outside the tile; the arrow shows the way the pull goes, up and out along
    the arm. (undercling.svg shows the whole arm.)"""
    flake = [(WX - x, y) for x, y in FLAKE]
    under = H.outline(flake, 0.45)
    h = Hand("undercling")
    pad = H.snap(under, (WX - 3.8, -1.3))
    p = h.view("thumb", flip=True).place("i", pad, a0=42, k=0.8)
    on_edge(p, pad, k=0.8, along=200, spread=0.34, slide=under)
    y1 = FLAKE[-1][1] + 0.9
    f = profile_frame(tile_x0(), y1 - TILE_H, y1)
    f.smooth(flake, z=-5, fill=DARK, stroke=INK, sw=0.35, tension=0.45)
    H.xray_outline(f, flake, 0.45)
    p.draw(f, z=0)
    f.arrow([(WX - 8.0, -3.2), (WX - 11.0, -1.6)], kind="force")
    hwarn("atlas undercling", p)
    return f


def atlas_palm():
    """A palm pressed flat on a volume's face, in three-quarter view: the back
    of the hand toward you, seen from the wrist's end, the wrist bent back so
    that the forearm comes up off the face. A push into the face then shows
    on the page as a push down the hand, through its heel, where the arrow
    ends (seen from the fingers' end it would point up the hand, along the
    rock, which is the mistake the entry warns of)."""
    h = Hand("palm")
    p = h.view("back", a0=90, tilt=20, pitch=-25).move_point((0, 0, 0), (0, 0))
    pts = [p.xy(q) for s_ in h.thumb_solids() + [h.palm_solid()] for q in s_]
    pts += [p.xy(q) for f_ in "imrl" for s_ in h.finger_solids(f_) for q in s_]
    left, right = min(q[0] for q in pts), max(q[0] for q in pts)
    x0 = left - (TILE_W - (right - left)) / 2
    y1 = max(q[1] for q in pts) + 0.6
    f = Fig(x0, y1 - TILE_H, x0 + TILE_W, y1, scale=CLOSE)
    # the face, and past its ridge the next facet of the volume
    a, b = (x0 - 2, y1 - 6.0), (x0 + 5.6, y1 + 2)
    c, d = (x0 + TILE_W + 2, y1 - TILE_H - 2), (x0 - 2, y1 - TILE_H - 2)
    e = (x0 + TILE_W + 2, y1 + 2)
    f.poly([a, b, e, c, d], z=-12, fill=VOLUME, stroke=INK, sw=0.35)
    f.poly([a, b, (x0 - 2, y1 + 2)], z=-11.9, fill=VOLUME, stroke=INK, sw=0.35)
    p.draw(f, z=0)
    plane_arrow(f, p, p.at(1.5, 0.5, 1.4), (0, 0, -1), length_=3.4, gap=0.0)
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
