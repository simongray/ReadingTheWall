# Climber renderer notes

The reader found the climbers rag-doll-like: tubes and ovals, round caps at
the shoulders and hips, seams where limbs meet the body. This log covers the
rewrite of the drawing code in `figtools/climb.py` (October 2026).

## What stayed the same

- The public API and every parameter of `Climber`, `Fig`, `hold`,
  `hold_side`, `volume`, walls, arrows, labels, `combine` and `filmstrip`.
- `solve()` and the joints. A check that records `Climber.J` for every
  climber the figure modules draw (193 climbers) found them identical with
  the old and the new `climb.py`. No pose changed.
- `limb_outline`, `silhouette`, `capsule`, `ellipse_pts`, `catmull`, `SHOE`,
  `DIM` and the `_shoe(fig, s, st, z)` hook that `figs_feet.FootClimber`
  overrides.
- Conventions: left limbs grey, right white, dark shoes, dotted x-ray
  outlines on holds and shoes, ghosts as dashed outlines with white fill,
  outline weight 0.32 mm.

## What changed

**One contour per body part.** Each part (torso with neck, head, each arm,
each leg) is one group: every piece's outline at twice the line weight,
then the fills, so only the group's outer contour shows. Where a limb grows
out of the torso, the limb's outline is left out inside the torso near the
joint (`_root_hide`), and each trouser-seat half leaves out its outline
inside its own thigh. The shoulder and the hip read as one contour, with no
round cap on top. Further from the joint, a limb that passes in front of the
body keeps its full outline, and a foreshortened limb keeps its elbow or
knee.

**Clothing.** A white T-shirt with short sleeves (sleeve hem at about 40 %
of the upper arm), trousers with the left leg and left half of the seat
grey, and a centre seam. The T-shirt hem replaces the old waistband; the
spine line is gone. A bent knee gets one short trouser fold behind it.

**Anatomical outlines** (`tube()` with radius profiles): the torso has
trapezius slopes, rounded shoulders around each joint, chest, waist and
hips; in side view a chest, belly, lower-back curve and buttock (part of
the thigh's back profile, so it moves with the leg). Thighs, calves and
forearms taper and bulge on the right side (the knee's jut side is the
front).

**Head.** Back view: skull, ears and a hair mass with a nape hairline over
a visible neck. Side view: profile with forehead, nose, lips, chin and jaw
line, ear, eye and hair. The head is drawn 2 cm above `J["head"]` and 4 %
smaller (`HEAD_RAISE`, `HEAD_SIZE`): the skeleton's neck is short, and the
old figures looked neckless.

**Hands.** A gripping hand: palm, a thumb lobe on the thumb side, and short
lines between curled fingers. A hanging arm gets a relaxed hand.
`hand_style="open"` draws a palm with spread fingers and thumb.

**Shoes.** Same outline (contact points unchanged), now with a white sole
line, a grey rand line over the toe box and heel, and a strap. Heel-on
(`style="back"`) shoes get sole and heel-rubber lines. The trouser hem sits
over the top of the shoe.

**Turned bodies.** In back view with `turn`, the drawn torso narrows less
than the shoulder and hip joints do (the chest and seat show their depth),
so turned climbers no longer look emaciated.

## Notes for figure authors

- `Climber.draw_arm(fig, s, elbow, hand, z, ghost=False)` draws an arm
  through an explicit elbow in the new style. `figs_body._arm` and
  `figs_hands.draw_arm` still build old-style tube arms from `limb_outline`
  (twist-lock, gaston), which now look out of place; switch them to
  `c.draw_arm(...)`.
- `shoe_details(fig, P, z)` adds the sole, rand and strap lines to a
  profile shoe. `FootClimber`'s own `draw_shoe` draws only its sole line;
  call `shoe_details` there if its shoes should match.
- The sleeves are white on both arms: the grey of the left arm starts below
  the sleeve hem. A leader to "the left arm" should point past about 45 %
  of the upper arm (the legend's 60 % is fine).
- Turned torsos are wider than before; check that labels and arrows near
  the torso in turned figures (cover, drop-knee, hip-turn, twist-lock) still
  clear the body.
- Arms are still drawn over the head and torso in back view, as before, so
  hands on holds in front of the face stay visible.
- Build time and file sizes: about the same speed, SVGs about 30 % larger.

## Round 2: smooth joins and a pen-drawn look

The reader asked for smoother joins and, if possible, a hand-drawn style.
Joints and the API are unchanged again: `Climber.J` matches the previous
build for all 193 climbers.

**Smooth curves.** `Fig.poly` and `Fig.smooth` now write densely sampled
outlines (limbs, heads, hands, the 3D hands of `hand.py`) as cubic Bezier
curves through the points, with handles along the line, so they never
overshoot. Points where the line turns by more than 55 degrees, or that
sit between long straight pieces, stay sharp, so drawn polygons (volumes,
arrow heads, walls) keep their corners. Switch: `SMOOTH_PATHS`.

**Joins.**
- Where a limb's outline runs into the torso (shoulder, armpit, hip,
  crotch) its open stretch now ends square instead of round. The round
  cap had left a small black blob on the torso at every such join.
- Bent elbows and knees get a soft inner curve (`_fillet`: a piece
  filling the notch between the two segments, bounded by a curve that
  follows each segment's real contour) and a short crease line from that
  curve toward the joint. The knee crease replaces the fold of round 1.
- The T-shirt's neck opening is narrower than the neck, so the trapezius
  runs straight into the neck without a step.

**Pen** (switch: `HAND_DRAWN`, applied inside the `Fig` primitives, so
climbers, `hand.py` close-ups, shoes, holds, volumes, walls and arrows all
get it):
- Weight: lines drawn 0.28-0.8 mm wide get 12 % heavier
  (`PEN_OUTLINE`), so the climber's outline is about 0.36 mm and the hand
  close-ups' about 0.38 mm. Nothing is drawn thinner than 0.22 mm
  (`PEN_MIN`). Interior lines are 0.24 (`LINE_SW`: hems, seams, hairline)
  and 0.22 mm (`FINE_SW`: finger lines, creases, ear).
- Taper: open, solid, unfilled lines up to 0.27 mm (folds, creases,
  seams, nails, shoe rands, wall hatching) are drawn as filled pen strokes
  that taper to half their width at both ends. `Fig.poly(..., taper=)`
  forces this on or off.
- Wobble: a smooth displacement field over the page, at most 0.13 mm
  (`WOBBLE`), mostly with wavelengths of 4-10 mm. It depends on position
  alone, so a fill and its outline, two pieces sharing an edge, the x-ray
  outline and its hold, and the same hold in every filmstrip frame all
  move together, and every build is identical.
- Move arrows get an irregular dash rhythm (`MOVE_DASH`). Ghost dashes and
  x-ray dots stay regular.
- Exact, unchanged: text, label leader lines and dots, step numbers, the
  centre-of-gravity symbol and the cross.

**Cost.** The build takes about 7 s instead of 5 s, and the SVGs total
18 MB instead of 11 MB (sampled points are thinned to one every 0.8 mm,
and paths are written with one decimal at book scale).

**Not done.** `research/eink-report.md` didn't exist when this round
finished, so its line-weight and grey advice isn't applied yet. The pen
constants above are the place to apply it.
