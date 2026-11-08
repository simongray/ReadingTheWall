# Follow-ups

This file lists what's worth doing in a later revision. Most items come
from the editing logs in `research/` (fact-checks, figure reviews,
streamlining), which have the details.

## Content and sources

- **Sources re-checked in a browser** (`research/factcheck-3.md`):
  UKClimbing's articles open in full in a browser, although automated
  checks hit a paywall, so the claims that cite them are now checked. D46
  and E63 still show a bot check; D46's entry gives a Wayback copy, and
  E63's DOI checks out. F37's page is gone, with no Wayback copy.
- **The climbing use of "tic-tac"** is still unverified: no climbing
  source uses the name, only parkour ones. The entry says so.
- **Grade placements** of most techniques are judgement calls, since no
  public syllabus ties techniques to V-grades. Revisit them as you climb
  more problems in your gyms.
- **Links:** every Watch link (and so every QR code) was checked through
  YouTube's oEmbed when it was added (`research/linkcheck-2.md`,
  `research/videos-2.md`).
- **More videos:** 21 more entries got one in this revision
  (`research/videos-2.md`). No good video turned up for Volume mantle,
  Campus move, Double clutch, Tic-tac, Thumb catch, Counter-kick, Hip pop,
  Latching, Run-and-jump, Sit starts, Hand–foot match, Bumping and Jump
  start, and Lock-off's only candidate was too weak to use. Two videos
  serve more than one entry: Lunge and Double dyno share one, and Open
  hand, Pinch and Wrapping link to different points of another. None of
  the new picks was watched, only checked by title, channel and
  description, so watch them before a release.

## Figures

- Every figure was checked against photographs and video in this revision
  (`research/photo-check-*.md`, and `research/photo-check-3-poses.md` for
  the second pass, which fixed High step, Rockover, Hand–foot match, Knee bar
  and Traverse). These doubts remain:
  - References are still thin for Tic-tac (parkour only), Heel–toe cam (one
    video) and Pogo (low-resolution stills). In Heel–toe cam the shin may
    come in level along the slot rather than from above.
  - The Stemming text says the fingers point down or away from the corner,
    as its source says. Photos show them down for a palm at the hip and out
    or up for one at shoulder height, as both figures draw them.
  - Twist lock (c) is a side view, which can't show the twist of the torso,
    since the drawing library has no front view. The inset from above in (b)
    shows the turn instead.
  - The thumb lock in Full crimp hides part of the index finger, which is
    true to life.
- The shoe close-ups (toe hook, heel hook, bicycle, foot atlas) draw no
  leg, so they can't show the muscles at work. In Twist lock (b), the lat
  that pulls the arm in lies behind the upper arm.
- Some of the waist bends are only 5–8°, so they barely show at print size.
- The hand close-ups seen from the thumb side come from the hand model in
  `figtools/handmodel.py`. These are still written by hand in
  `figtools/authored.py`, with the old proportions: Pinch and Pocket, and the
  atlas's pinch and pocket tiles. Both were tried with the model:
  - A pinch lifts the thumb out in front of the palm, which brings the ball of
    the thumb with it, so the side-view mid-palm reads 6–6.6 cm against the
    4.5–4.9 that `check_hands` allows for a relaxed thumb. The drawings also
    showed a flat line under the hold where the palm's edge runs.
  - From the little-finger side the model's palm is 4.3 cm deep against the
    3.4–3.9 that `check_hands` allows there, and the thumb behind the palm
    showed as a grey band.

  The old hands that no figure draws any more are still defined in
  `authored.py`.
  - No photo of matching on a rail from behind, or of a palm press close up,
    was found; those views rest on the anatomy and the side-view photos.
  - The atlas's undercling bends its middle joint 60°, not the photos' 90°,
    because the tile's flake is shallow.
  `research/hands-drawing-reference.md` has the photos and joint angles.
- A prototype drawing the hands from a CC0 3D mesh (MakeHuman) is on the
  branch `claude/hands-3d-model-b315ef`, unmerged. It is the better route to
  views from above, such as the pinches.
- The editing passes noted these limits of the drawing library:
  - `turn` narrows the shoulders, so a back view can't show the reach that
    a hip turn gains.
  - The anatomy checks for back views are heuristics, since the
    projection hides the true angles. The check that a knee points the
    same way as its toes can't tell a deep drop knee from a broken pose;
    a per-leg exemption, like `allow_cross`, would allow one.

## Book

- The third edition is 306 pages. The eight worked problems
  moved out of it into the exercises booklet.
- **Typography, for Simon to judge** (`research/revise3-typography.md`):
  - A few entries' first pages still end short, with the figure or box on the
    next page. It no longer happens because of a near miss.
  - Three figures changed in ways worth a look: the worked problem's film strip
    is at a smaller scale than the others, Mantle's low foothold moved up, and
    Deadpoint, Pocket and Overhangs are narrower so they sit beside their steps.
  - Sources' last page is even through two numbers set by hand in
    `10-appendices.typ`. `check_fit` says when they need changing.
  - The video titles keep "Greshams", as published, without their episode numbers.
  - The "Fix" numbering in Barn door is as it was.
  - Three entries still run loose. Straight arms' box misses its first page
    by about a line, and the only fixes are to cut a line from the box or let
    it break across the page turn, both worse than the gap. Bicycle and Mantle
    keep their current splits. Twist lock now sets its figure before the
    steps (`figure-first` in `technique()`), so the two share a page.
  - None of this has been read on the Boox.
