# Follow-ups

This file lists what's worth doing in a later revision. Most items come
from the editing logs in `research/` (fact-checks, figure reviews,
streamlining), which have the details.

## Content and sources

- **Claims that couldn't be verified,** because their sources are
  paywalled or blocked, are the "could not verify" rows in
  `research/factcheck-1.md` and `research/factcheck-2.md` (marked NV in
  the second). Re-check them if you get access. Most of them cite:
  - UKClimbing articles (B23, C51, C52, E13–E17, E49);
  - sources seen only as search excerpts (C50, C56, C57);
  - forum threads (G7, G8) and secondary citations that weren't
    re-checked (G45–G49, G51).
- **The climbing use of "tic-tac"** is unverified, since the term comes
  from parkour. The entry says so.
- **Deadpoint history:** the book says that John Gill used the word in
  print in 1969 and that Güllich studied the idea in the 1980s. Its claim
  that the idea is "often credited" to Güllich has no source.
- **Grade placements** of most techniques are judgement calls, since no
  public syllabus ties techniques to V-grades. Revisit them as you climb
  more problems in your gyms.
- **Links:** every Watch link (and so every QR code) works
  (`research/linkcheck-2.md`). One source page is gone (F37, kept with a
  note). 38 source sites blocked the automated check, mostly UKClimbing
  and theCrag behind Cloudflare, so check those in a browser.
- **E17's title is cut short** ("Training to ... Part 3"). The page is
  paywalled, so the full title couldn't be found.
- **More videos:** the web-search budget ran out during research, so
  several entries have no "Watch" links. A good video for each of the
  hardest techniques would help. The template makes the QR code from the
  link.

## Figures

- These figure doubts remain (the details are in `research/figpolish.md`,
  `research/figcritic-*.md` and `research/figreview-*.md`):
  - In Twist lock, the forearm points into the wall, so it's drawn short
    in the back view. A side-view panel would show the locked arm better.
  - In Drop knee, the foot is drawn pointing down, which is a drawing
    convention rather than a literal view.
  - The Gaston and the Layback are hard to read from behind.
  - The toe hook in Jumping to a foothold (`foot-catch.svg`) is seen from
    behind and can't be read without its caption.
  - The Counter-kick's barn-door swing is ambiguous in a back view.
  - The thumb lock in Full crimp hides part of the index finger, which is
    true to life.
- The muscle-shading audit found poses that disagree with their text:
  - In Bumping, the holding arm is bent at about 90°, but the text says to
    keep it straight.
  - In Pogo (a), the right arm reads as bent, although it's labelled
    "arms straight".
  - In Double clutch (b), the catching right arm is straight, although the
    text says to catch with the arms slightly bent.
  - In the arête figure (b), both arms are well bent, although the text says
    the heel hook rests them.
- Some muscles can't be shaded as things are:
  - The shoe close-ups (toe hook, heel hook, bicycle, foot atlas) draw no
    leg.
  - In Twist lock (b), the lat that pulls the arm in lies behind the upper
    arm.
- The waist bend (`bend`) is only used in Drop knee, the dyno and the
  straight-arms concept. Most poses would look less stiff with one.
- In the hand close-ups:
  - The half crimp's thumb still points back toward the climber.
  - The little finger falls short of its hold in some grips, hidden
    behind the other fingers.
  - The fingers behind the index are one pale grey shape, which may be
    faint on e-ink.
- The hands chapter has no "In motion" filmstrip; it has the
  hand-position plate instead. Re-gripping a sloper or matching on a crimp
  would make a good one.
- The top of the shoe faces the hip, so a foot at or above hip height is
  drawn sole-up unless its foot dict sets `flip`. Turning the top toward
  the knee in `climb.py` would fix this for every figure.
- In Crossing hands, the target is only about 10 cm
  past the holding hand, because `turn` can't narrow the shoulders below
  half their width. A longer cross from behind needs that limit relaxed.
- The editing passes noted these limits of the drawing library:
  - `arm_len` takes one factor per arm, not one for the upper arm and one
    for the forearm.
  - `turn` narrows the shoulders, so a back view can't show the reach that
    a hip turn gains.
  - The anatomy checks for back views are heuristics, since the
    projection hides the true angles.
  - `warn()` doesn't check figures drawn with custom helpers outside
    `climb.py`.

## X-ray outlines

- The layback flake and the holds in the close-ups aren't dotted where a
  hand covers them.
- The roof holds (`roof_hold` in `figtools/figs_terrain.py`) are still drawn
  in the old flat style, without the new holds' light gripping surface.

## Typography

- `fit-pages` measures a copy of the text without page numbers, so it can
  think text fits when it spills by a line or two. The box in section 6.4
  needed trimming by hand for this reason.

## Book

- The first edition is 266 pages, and the next is 263 so far. A filmstrip
  or a quick-reference card would add more.
- A one-page "on the mat" quick-reference card could be added if it fits
  the page budget. It would hold the reading checklist and the top cue
  for each category.
