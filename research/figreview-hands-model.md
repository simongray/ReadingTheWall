# Figure review: one hand model (figtools/hand.py)

The reader found the hands strange and inconsistent: palm too long against
the fingers, short thick finger segments, a sausage thumb at odd angles,
stick fingers, and a different hand in every figure. All hand close-ups now
come from one 3D model in `figtools/hand.py`, drawn at one scale.

## The model

- Proportions for a hand 19 cm long. Knuckle joints 9.0–9.35 cm from the
  wrist crease, on an arc (little finger 8.35); the skin of the palm runs on
  to the webs at about 10.7 cm, so the palm reads as 10.5–11 cm. The palm is
  8.4 cm across the knuckles and 2.7 cm thick there, 3.5 cm at the wrist.
- Finger segments (proximal / middle / distal + pad): index 4.0/2.4/1.9,
  middle 4.4/2.8/2.0, ring 4.1/2.7/1.9, little 3.2/1.9/1.7, pads 0.4–0.45.
  Widths 2.0 cm at the base to 1.45 at the tip (little × 0.84), a swelling
  at the middle joint, a fleshy pad, the nail on the back.
- Thumb: metacarpal 4.5 from a base joint near the wrist, proximal 3.2,
  distal 2.7 to the tip, 2.1–2.2 cm wide; a ball of the thumb (thenar) and
  a web join it to the palm. Relaxed, its tip sits at the middle of the
  index finger's first segment.
- Joint ranges checked by `Hand.warn()`: knuckle 0–90°, middle joint
  0–110°, end joint −20–80°, thumb joints in proportion, wrist −70–85°.
- Every part is a convex hull of cross-section rings (tube per segment,
  rounded wedge per joint, palm, thenar, forearm), projected
  orthographically and merged with the silhouette technique. Views: thumb
  side (index in front, the other fingers grey behind, offset by turning
  the back of the hand 6° toward you), little-finger side, back, palm;
  `flip` mirrors a profile.
- Posing: `Hand(grip, fingers=, thumb=, wrist=)` with presets in `GRIPS`
  (relaxed, flat, open, half, full, pinch, sloper, pocket, undercling,
  palm, wrap, jug); `place()` puts a pad on a page point; `on_edge()` and
  `reach()` bend the other fingers onto the same edge; `thumb_to()` solves
  the thumb for a contact (natural-pose priors, optional pad direction);
  `grip_profile()` gives the standard open / half / full / thumb-lock views.
- One scale for every hand: `HAND_SCALE` = 2.6 mm per cm. Outlines 0.34 mm,
  grey fingers 0.30, lines between fingers 0.20, nails and creases 0.24.

Test sheet (scratchpad): the hand flat from the back and palm, relaxed from
both sides and the back, and every grip on its hold, compared with Climbing
Bible photos of a flat hand, crimps, a pinch and slopers, and with Kettle's
crimp drawings (proportions and poses only, nothing traced).

## Figures

- **hands-hold-angle**: new hand in a half crimp on each edge, no thumb; notes moved up off the hand.
- **open-hand**: (a) drag with the arm hanging below, thumb under the rounded hold, ≈40° arc; (b) three-finger drag from behind with the thumb visible and the little finger curled off; labels off the hand.
- **half-crimp**: palm upright, first segments level, ≈90° at the middle joint, thumb tip on the hold's front below the fingertips; labels moved left of the hand.
- **full-crimp**: (a) A2 pulley as a band on the palm side of the first segment; (b) thumb solved onto the index nail.
- **pinch**: the old hand was geometrically impossible (thumb base floating). Redrawn as a real C-grip from above with the forearm coming from below: index on the right face, thumb on the left. The wide block is now 6 cm (a 12 cm block can't be pinched with the palm at its front); caption still matches.
- **sloper (c)**: dome follows the palm side of the hand; thumb under it.
- **pocket**: from the little-finger side; ring and middle in the hole, index hidden behind; (a) little finger reaching the hold face below the pocket, (b) curled; labels moved left.
- **thumb-catch**: (a) thumb tip in the dimple; (b) thumb lying flat on the lower face, pad pressing up; labels moved left.
- **wrap**: palm flush on one face (solved), fingers round the edge, thumb flat beside the palm.
- **regrip**: back views; (2) ghost drag plus a half crimp whose knuckles stand above the incut; two-line label between the forearms.
- **hand-atlas**: all ten tiles redrawn at 2.6 mm/cm (tiles 14.4 × 16.4 cm; plate 159 × 146 mm); undercling is a mirrored thumb-side view with the arm reaching down.
- **latching (a, b)** in figs_dynamic: same hand at 2.6 mm/cm; panel c untouched.
- **grip-crimps** (closeup.py, not in the book): redrawn with `grip_profile`.

`closeup.py` lost its old hand code (profile hand, face-on hand, finger
chains); nothing else used it. No caption needed changing; the book compiles.

## Doubts

- The thumb lock still covers much of the curled index; that is how it
  looks, but the middle-joint angle is clearer in panel (a).
- The volume-edge pinch thumb reads a little heavy.
- The palm press tile shows a sharp crease at the bent-back wrist.
- Unrelated: the sidepull climber now triggers a new knee warning from
  climb.py ("l knee folded to 47 deg"); I left the climber figures alone.

## Second pass: side views (31 Oct)

The reader found the side views weird: thin fingers, and joints at
seemingly random lengths from panel to panel. Measured on the drawings
(`tools/check_hands.py`, which also fails the build check if a side view
draws a segment off the model by more than 0.02 cm or a hand shows less
than a quarter of its thumb):

| | before | after |
|---|---|---|
| index segments drawn (cm) | 3.95–4.00 / 2.38–2.40 / 1.88–1.90 | 4.00 / 2.40 / 1.90 in all 24 side-view hands |
| index thickness in profile | 1.62 / 1.35 / 1.22 | 1.91 / 1.71–1.74 / 1.52–1.56 |
| palm, thumb base / knuckles | 3.33 / 2.84 (tilted block) | 3.01 / 2.48, straight back |
| thumb | missing in 2 panels, posed ad hoc | in every hand; rests beside the index's first segment unless the grip uses it |

- Profiles are true side views: no tilt, and the front finger's plane of
  bending is turned into the page, so its segments show true lengths.
- The fingers behind the index are one grey copy of the index, 0.3 cm
  toward the fingertips and 0.4 cm toward the back of the hand: depth
  without extra joints. Exception: the pocket, where the ring finger in the
  hole is the subject; it is drawn grey with its own joints, parallel to the
  little finger (both are checked).
- Thumb used in the thumb lock, thumb catch, pinch and wrap; elsewhere
  `Hand.rest_thumb()`.
- Little finger stays thinner (1.68 / 1.54 / 1.36), as in a real hand.
- Consistency sheet of all side-view panels with their lengths, next to
  Kettle's grip drawings, in the scratchpad. Same contour logic as Kettle's:
  straight back of the hand, rounded knuckle, thumb in front of the palm.

Climber figures in figs_hands (new renderer): the gaston arm now uses
`Climber.draw_arm`; sidepull (a) shoulders 3 cm higher to clear the knee
warning; labels moved clear of the wider torsos and sleeves on jug (b),
palming, volume-mantle (b) and sloper (a, b; sloper panels 10 cm taller).
`build_all.py` shows no warnings for figs_hands.

Still doubtful: in the half and full crimp the resting thumb sits in front
of the curled finger and hides part of the small edge.

Third pass: in the drag, half-crimp, full-crimp (both) and hold-angle
panels the thumb now rests low and back along the palm side
(`tuck_thumb`), so the whole index finger, the arcs and the edge show;
`check_hands.py` reports the share of the index axis under the thumb (0 %
in these, 22 % in the thumb lock, kept as it is). Close-up holds now draw
their dotted hidden outline where the hand covers them, as climb.py's holds
do.

Fourth pass, from the critics' findings on the third edition's model. In
`hand.py` back-view thumbs got their own outline, joints with an arc lost their
creases, the wrist softened, and `xray_end()` draws the end segment under a
locked thumb as a dotted outline. `check_hands.py` now fails a thumb drawn under
70% of its length or with two joints at straining limits, and it checks matching.
The close-ups changed are wrap (tilt 32, pitch 15, the arête runs on under the
fingers as a hidden line), the atlas tiles, pocket, hold angle, thumb catch,
pinch, the filmstrip and the drag.

Still doubtful: the gaston's elbow follows step 3 ("about level with your hand"),
which an earlier comment's photographs may contradict; a small kink remains in the
pocket thumb; the fingers on crimps stay grey.
