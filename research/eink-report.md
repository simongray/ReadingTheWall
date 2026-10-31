# E-ink check of the figures

How the figures look on an Onyx Boox Max (13.3" E Ink Carta, 207 ppi, 16
greys) showing the A4 PDF at about 95%, and what to change in
`figtools/climb.py` for it (October 2026).

The figures hold up well. Nothing becomes unreadable: label text, step
numbers, arrows, outlines, the dotted hidden lines, the grid dots and the
filmstrip band and captions all survive. What suffers is the grey scale
itself:

- DARK and LIGHT sit halfway between two of the panel's greys, so they turn
  into a fine stipple, or shift by a whole level, depending on how the Boox
  maps 256 greys to 16.
- PALE is one level below white and nearly disappears.
- Ghost outlines fade where they cross a volume.
- Volume facets flatten to two or three panel levels.

## How it was checked

- Each SVG is rendered with `rsvg-convert` at 197 dpi (207 ppi × 0.95) on
  white, the size the PDF places it at.
- The render is mapped to 16 even greys (#000000, #111111, … #ffffff) with
  Floyd–Steinberg dithering, using `magick -dither FloydSteinberg -remap` onto
  a fixed palette. `-colors 16` isn't used, since it picks its own levels.
- A "panel" view also compresses the tone range to a Carta-like 15:1
  contrast, with the levels evenly spaced in L\*. This is an approximation,
  used for the grey-on-grey judgements below.

`figtools/climb.py` changed while I worked (the pen pass: `PEN_MIN`,
`PEN_OUTLINE`, tapering, wobble). I checked a build from before the pen
pass and one with it, and the findings are the same for both. The "before"
samples are the pen build. Line numbers in `climb.py` keep moving, so the
recommendations name functions and constants.

Contrast of some pairs, as ΔL\* (about 2 is a just-visible difference):

| Pair                                  | Screen | Panel now | Panel after 1–3 |
|---------------------------------------|-------:|----------:|----------------:|
| PALE fill on white                    |    6.6 |       4.1 |  4.1 (8.2 with 4) |
| LIGHT fill on white                   |   15.1 |      12.4 |            12.4 |
| ghost line on white                   |   41.7 |      29.9 |            34.5 |
| ghost line on a #bcbcbc volume facet  |   18.0 |      13.2 |            17.8 |
| sloper rings on the hold              |   25.5 |      14.2 |            23.1 |
| left limb (LEFT) on a hold            |   35.4 |      23.1 |            23.1 |
| left limb on a #bcbcbc volume facet   |    8.1 |       4.3 |             4.3 |
| shoe on a foothold                    |   17.6 |      15.8 |            15.8 |
| black arrow or outline on a hold      |   32.7 |      24.9 |            24.9 |

## Recommendations

In order of value. Changes 1–3 are variant A in the samples, and change 4 is
variant B.

**1. Snap the fill greys to the panel's 16 levels.** A grey on the grid
(#000000, #111111, … #ffffff) looks the same whether the Boox dithers,
rounds or truncates, and it renders as a flat tone. None of these changes
moves a grey by more than 9/255 on screen.

| Constant                              | Now                               | Change to                         |
|---------------------------------------|-----------------------------------|-----------------------------------|
| `DARK`                                | #4d4d4d                           | #555555                           |
| `LIGHT`                               | #d4d4d4                           | #cccccc                           |
| `volume()` default shades             | "#bcbcbc", "#e0e0e0", "#c8c8c8"   | "#bbbbbb", "#dddddd", "#cccccc"   |
| `LEFT` (optional)                     | #a6a6a6                           | #aaaaaa                           |
| `MID` (optional)                      | #8c8c8c                           | #888888                           |
| `PALE` (optional)                     | #ececec                           | #eeeeee                           |
| `HAIR` (optional)                     | #6e6e6e                           | #666666                           |
| `SHOE_FILL`, `figs_feet.SHOE_COL` (optional) | #262626                    | #222222                           |

DARK and LIGHT matter most. The panel now shows DARK as #444444 or
#555555 and LIGHT as #cccccc or #dddddd, depending on the Boox's rounding,
and dithering turns both into a 50/50 stipple. #555555 is better than
#444444 because it keeps the dark shoes apart from the footholds. #cccccc
keeps body arrows, mats, the grey back fingers and side-on volumes clear of
white. The optional rows only remove dither speckle, since the panel
already shows those greys at the new value.

**2. Draw ghost outlines one level darker.** Add `GHOST_LINE = "#777777"`
and use it instead of `MID` for ghost strokes, keeping their weight and
dash. The ghost strokes are in the ghost branch of `Climber.draw`, in
`Climber.draw_arm`, `figs_feet.GHOST`, the dashed closed body of the
barn-door inset and the ghost in `_hand_back` in `figs_body.py`, the ghost
hand in `hand.py` and the "Earlier position" key in `legend.py`. This mainly helps ghosts that cross a volume.

**3. Draw the sloper rings in `LEFT` instead of `MID`.** In `hold()`, the
rings on a face-on sloper are `MID` on `DARK`, only three panel levels
apart. `LEFT` makes it five. This is a small gain, since the slopers in the
book are small.

**4. Optional: PALE → #dddddd.** Use this only if, on the device, the second
wall face, the top of the boulder and the pale volume facets look too faint,
e.g. with the Boox contrast boost on. It doubles PALE's contrast with white
on the panel. On screen, though, the pale areas turn visibly greyer and PALE
ends up one level from LIGHT, which flattens the volume shading.

**Leave as they are:**

- `XRAY_STYLE`: the 0.2 mm (0.22 under `PEN_MIN`) #2a2a2a dashes still read
  as dotted, on white and on grey limbs. The gap left after the round caps
  is 0.33 mm, enough to resolve.
- Wall hatching (0.18 mm `MID` on `PALE`): faint but visible, and
  `PEN_MIN` raises it to 0.22 mm.
- Label text (7–8 pt nominal, set 8% larger), leader lines, step numbers,
  move and force arrows, the grid dots and the `wall_back` panel outline.
- The filmstrip band (#3a3a3a), sprocket holes, white frame numbers and
  captions.

## Figures with problems

- **dynamic-slab**: the "start" ghost's feet on the volume nearly dissolve
  on the panel. Changes 1 and 2 outline them clearly.
- **tic-tac**: the ghost leg that crosses the volume fades into the dark
  facet. Change 2 helps.
- **top-out**, panel a: the pale strip above the lip (the top of the
  boulder) has no outline on its top edge and nearly vanishes. Use change 4,
  or give that `PALE` polygon in `top_out()` a thin `MID` top edge.
- **corner**, panel a: the pale right-hand wall is almost white on the
  panel. It still reads from the corner line and the missing grid dots, so
  no change is needed.
- **compression** and the other figures with `volume()` facets: the facet
  shading flattens and dithers. The outlines keep the volumes readable, and
  change 1 removes the stipple.

## Files

Scripts:

- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/tools/eink_sim.sh: render, dither and contact sheets (`eink_sim.sh SVG_DIR OUT_DIR`)
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/tools/beforeafter.sh: 2x before/after crops
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/tools/contrast.py: the ΔL\* table
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/tools/build_figs.py: builds a copy of figtools into another folder

Contact sheets for the current (pen) build, with screen and e-ink side by
side, and the panel view:

- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/sim_pen/sheets/pairs-01-half.png (to pairs-13-half.png)
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/sim_pen/sheets/tone-01.png (to tone-13.png)

Before/after samples (top row on screen, bottom row on the panel, at 2x):

- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/dynamic-slab-ghost-feet.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/tic-tac-ghost-on-volume.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/top-out-lip.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/compression-volume.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/legend-holds-left-limb.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/paddle-dyno-sloper.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/campus-move-hatch-prepen-vs-pen.png

Whole figures on the panel (before, A, B):

- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/full-dynamic-slab-tone.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/full-tic-tac-tone.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/full-top-out-tone.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/full-compression-tone.png
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/samples/full-corner-tone.png

The variants as code, to diff against the pen build in
/private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/figtools_pen:

- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/figtools_A
- /private/tmp/claude-501/-Users-simongray-Books-Bouldering/e74111f2-de8c-4e1f-b6db-afa64a76b805/scratchpad/figtools_B
