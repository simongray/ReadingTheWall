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
- **Grade placements** are the book's estimates. Only the French federation's
  syllabus ties techniques to boulder grades, for three of its levels
  (`research/grade-syllabi.md`). Courses and setters put four groups of
  techniques earlier than the third edition's badges: standing on volumes at
  about V0–V1, bicycles at V2–V4, toe hooks at V2–V4 and competition-style
  moves from V2–V4 (`research/judgement-pass.md`). On 2026-11-17 four badges
  moved for that reason: Volumes to V1, Toe hook and Run-and-jump to V3, and
  Bicycle to V4. The other competition-style moves kept V5, since setters
  disagree about them. Revisit them as you climb more problems in your gyms.
- **Steps that point up a grade.** `check_order` lists 33. All were read on
  2026-11-17 and are meant: a pointer that says "later" or names the grade, a
  link for a term used in passing, a warning, or one of Barn door's fixes.
- **Sources added after the third edition.** The 22 studies were read again on
  2026-11-17, 19 of them in full, and 13 sentences changed
  (`research/factcheck-4.md`). G80, G84 and G86 are still abstracts only. The
  page quotes were checked for eight of the web pages. A London gym whose
  course page is cited (F71) says it is closed for now, so the page may go.
- **Repeated and misplaced passages.** `research/placement-audit.md` lists 55,
  and its head says which few are still open and why. New links add lines to
  the "Referenced from" lists, which can push the end of an entry onto a new
  page: check the page count after adding any.
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

- **The technique map** (`book/map.toml`, `technique-map` in the template):
  - Its type is 7.2 pt, the smallest in the book, so that the map fits one
    page. It has not been read on the Boox.
  - The print map has no drawings in its nodes. A small pose for each technique
    would need every figure's code to draw one climber on its own. The web map
    shows an entry's drawing when you hover over its name.
  - The paths have no links between them, such as from the heel hook to the
    top-out. The entries' "Related" lists hold those.
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
