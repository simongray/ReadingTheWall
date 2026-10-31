# Figure critic: ghosts on top of the climber

The reader saw panel (b) of the frog figure and asked "Conjoined twins?": a
whole ghost body drawn almost on top of the solid climber merges with the
white-filled clothed body into one double body. `build_all.py` flagged nine
cases ("ghost overlaps the climber"). All nine are fixed, and the build now
prints no warnings at all.

`figs_dynamic.py` has a new helper, `_ghost_limbs(f, c, parts, on=None)`. It
draws only the named limbs of `c` as a ghost. With `on=<solid climber>` the
ghost limbs hang from the solid climber's hips, so they join the body instead
of floating beside it, and the helper returns the ghost so `_warn` can check
it.

- **frog** (figs_body): the comparison of wrong and right ghosts is now two
  side-by-side panels with the same wall, holds and centre of gravity.
  (b) "knees to wall: hips out" is solid and marked with a `cross` beside
  the seat. (c) "hips come close to the wall" is unchanged. The in-panel
  label is gone, because the panel caption says it. The figure is 146 mm
  wide (full width as before). I edited the caption in 04-body.typ to
  "(b) Side view. Knees pointed at the wall keep the hips out. (c) Knees out
  let the hips come in."
- **counter_kick** (b): the ghost is now only the left leg, at its panel (a)
  place, from its own hip. The hips moved only 10 cm, so the ghost leg
  starts behind the solid hips and reads as "this leg kicked across".
- **cutting_loose** (a, b, c): the hands stay put and the legs swing, so each
  ghost is now the previous frame's legs, hung from the solid hips. The
  legs drawn from their own hips floated beside the body in (a) and (c).
  In (c) the "toes catch" label moved to (62, 88) under the foothold,
  because the ghost shin now passes its old place.
- **double_clutch** (b): the hips move only 4 cm from catch 1 to catch 2, so
  the ghost is now only catch 1's legs. They show the body swinging right.
  Panel (a) keeps its whole ghost of the matched start, which sits well
  away from the climber.
- **hip_pump** (b): the ghost is now only the dip's legs, bent and wide,
  behind the straightening solid legs. The body arrow still shows the hips
  rising. Panel (a) is unchanged.
- **filmstrip_dyno** frame 5: the ghost is now only frame 4's legs, hung from
  frame 5's hips, so it shows the legs swinging out under the same hands.
- **legend**: the ghost is now only the right arm in its earlier place,
  drawn from the solid climber's own shoulder with the elbow down, and its
  hand on the lower jug. The dashed move arrow goes from there to the upper
  jug. The solid climber, the holds, the labels and the key are unchanged.

Still doubtful: in the legend, the ghost's upper arm is hidden behind the
torso (the elbow hangs down by the waist), so the visible ghost is mostly
the forearm and hand. Raising the elbow showed more arm but made a
chicken-wing pull on a jug. In hip_pump (b), the ghost legs partly overlap
the solid legs. They read as "were bent", but the panel is busier than the
others.
