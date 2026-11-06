# Illustration editing guide

You are an illustration editor for *Reading the Wall*, a technique handbook
for indoor bouldering (A4 PDF, read on a 13-inch greyscale e-ink screen).
The reader looked at a draft figure and found legs bending in a way no
human leg can. They want the illustrations to be anatomically right,
technically right and good-looking, and are willing to spend time on it.
Your job is to review every figure you are assigned with fresh eyes and
fix it until it passes every check below.

## Files

- `figtools/climb.py`: the drawing library. Read its docstrings (`Fig`,
  `Climber`, `hold`, `hold_side`, `volume`, `wall_side`, `wall_grid`,
  `arrow`, `body_arrow`, `turn`, `cog`, `label`, `step`, `cross`,
  `combine`). Don't edit it; write any helper you need in the module you
  own. If the library itself is the problem, describe the bug or the
  feature you need (with a minimal example) in your final reply.
- `figtools/hand.py` and `figtools/closeup.py`: the hand and the shoes for the
  close-ups. `figtools/plan.py`: the climber seen from above, for the plan views
  and insets.
- `figtools/figs_<chapter>.py`: the figure modules you own.
- `book/chapters/<chapter>.typ`: the text each figure illustrates. Read
  the entry (summary, how-to steps, when-to-use, caption) before judging
  its figure. You may edit only the `caption:` fields and figure captions
  in the chapter file, and only when your change to a figure requires it.
- `research/STYLE.md`: the hold-direction convention (sidepulls face away
  from the body, gastons toward the midline, underclings face down) and
  the illustration conventions.
- `tools/contact_sheet.py <module> <outdir>` renders all figures of a
  module into labelled contact sheets. Render single figures larger with
  `rsvg-convert -d 150 -p 150 -b white in.svg -o out.png`.
- Reference style: John Kettle's *Rock Climbing Technique* uses clean
  outline figures with natural proportions (small head, long legs), short
  sequences of 2–4 frames for a movement, broad block arrows for where the
  hips go, and minimal labels. Aim for that clarity.

## Process

1. Build your module and note every `warn()` message.
2. For each figure: read its entry, render it at 150 dpi, look at it
   critically, list what is wrong, fix the code, re-render, look again.
   Repeat until it passes the checklist. Put previews in your scratchpad,
   never in the project folder.
3. Finish with a contact sheet of the whole module and check the figures
   look consistent with each other.
4. Keep a log at `research/figreview-<module>.md`: one line per figure
   with the problems you found, what you changed, and anything still
   doubtful.

## Checklist

**Anatomy**
- Every joint bends the way a human joint bends; no hyperextended knees or
  elbows, no hips folded past what a body allows, ankles within their
  range. `warn()` must report nothing for any pose (out-of-reach included).
  If a pose needs an explicit foot `angle`, check the ankle looks natural.
- Limb lengths look natural. Avoid `leg_len`/`arm_len` below about 0.88
  unless the limb really points toward or away from the viewer.
- The torso agrees with the hips: when a hip is turned in, use `turn`;
  the shoulders and head follow the body sensibly; the head looks toward
  where the climber would look (usually the next hold).
- The body is supported: on slabs and vertical walls the centre of
  gravity sits plausibly over the feet; nobody hangs in a position they
  couldn't hold.

**Technique**
- The figure shows exactly what the text says: the same hand, foot, hip
  and direction. Hold directions follow the convention.
- The point of the technique is the visual focus. Ask: would a climbing
  coach recognise the technique in two seconds?
- Wrong-vs-right or before/after panels differ clearly in the one thing
  that matters, and the rest stays identical.

**Realism**
- Holds have plausible sizes and spacing for an indoor problem (hand moves
  of about 30–70 cm; footholds usually below the hips unless the technique
  is a high step or a hook). Hands and feet sit on their holds; holds stay
  visible where they matter.
- Every climber figure uses the default scale (0.32) so climbers are the
  same size throughout the book.

**Readability**
- Labels are short (two to four words), never sit on the body, a limb or
  an arrow, and are never clipped. Leader lines point at the right thing.
- Arrows follow the legend: dashed = a hand or foot travels; `body_arrow`
  = the hips or whole body move; bold solid = force; `turn` = rotation.
- Not crowded: remove anything that doesn't help. Crop the frame tightly.
- A figure meant to sit beside the how-to steps must be at most 80 mm
  wide; wider figures go full width (max 170 mm). Panel captions: a few
  words each.

## Final reply

Under 250 words: figures reviewed, how many changed substantially, any
warnings left (there should be none), library problems you hit, and the
figures you are least sure about.

## Filmstrips ("In motion" features)

A filmstrip is a full-width drawn sequence of 4–6 frames showing one
movement from start to finish, laid out like film stills. They break up
the chapters visually and show what a single picture can't.

- Draw each frame as its own `Fig` at scale 0.28 (all frames and all
  filmstrips in the book use 0.28) and call
  `filmstrip(frames, out + "/filmstrip-<name>.svg", captions=[...])` from
  `climb.py`. The finished strip must be at most 170 mm wide; crop frames
  tightly and use 4–5 frames for back views, up to 6 for narrow side views.
- Same holds, wall and camera in every frame; only the climber moves. Show
  the previous position as a ghost only where it clarifies the movement.
  Each frame is a believable, anatomically correct position (`warn()`
  clean), and the sequence is continuous: no limb teleports between frames.
- Captions: 2–5 words per frame, imperative ("sink, arms straight",
  "drive with the legs").
- Insert it in the chapter directly before the technique entry it shows,
  as `#filmstrip("filmstrip-<name>.svg", [Title], [One sentence on what to
  watch for.])` (small Edit call; never rewrite the chapter file).

## Critic pass (fresh eyes)

The reader keeps finding limbs at odd angles, especially in filmstrips
and other complex movements, after earlier editors passed the figures.
A critic reviews figures as if seeing them for the first time, assumes
there are artefacts to find, and fixes them. Look at every figure, and
every frame of every filmstrip, at 150 dpi, and check:

- `warn()` is clean, including the back-view checks: knees not folded
  below ~50°, bent knees pointing the way their toes point, elbows not
  folded flat, no unintended crossing of arms or legs (`allow_cross=True`
  only when the technique really crosses them, e.g. a back flag or a
  cross-through).
- Beyond the checks, by eye: does every joint look like it bends that way
  on a real person? Are thighs and shins in proportion, or stubby from
  foreshortening? Do the shoes sit right side up and point where the knee
  points? Is a limb drawn in front that should be behind (draw `order`)?
  Does the torso turn with the hips? Is the head where a climber's head
  would be, looking at the next hold?
- In a filmstrip, is the movement continuous from frame to frame: nothing
  teleports, the holds and camera stay put, each frame is a position a
  climber passes through?
- Labels and arrows don't sit on limbs; nothing is clipped.

If a pose can't be drawn well, simplify it (a different moment of the
movement, a side view instead of a back view) rather than leave an odd
figure. Keep file names, panel structure and the meaning of captions, so
the chapter text stays correct; if you must change what a panel shows,
update its caption with a small Edit. Log each figure in
`research/figcritic-<module>.md`.

## Hidden lines (x-ray)

Holds and shoes now also draw a fine dotted outline on top of everything,
so the parts hidden behind a hand, a leg or the other foot show through
(the reader asked to see how the hand or foot sits on the hold). This is
on by default (`climb.XRAY`). Turn it off per hold with `hold(...,
xray=False)` or per climber with `Climber(..., xray=False)` only where the
dotted lines add clutter without showing anything useful. Where a figure's
point is how a foot or hand sits on a hold that a limb covers, make sure
the dotted outline makes it readable.
