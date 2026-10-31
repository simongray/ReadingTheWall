# Changelog

Errata and changes between editions of *Reading the Wall*. Each edition is
a git tag (`edition-N`); the colophon on the back of the title page prints
the edition, its date and the commit it was built from, so you can always
tell which text you are reading.

Add entries under **Unreleased** as you make changes, using the page
numbers of the edition being corrected. Before a release, rename it to the
new edition, e.g. "Second edition (edition-2)"; `release.sh` uses that
section as the notes of the GitHub release.

## Unreleased

### Errata
<!-- - p. 37, Heel hook, step 3: "pull with the quads" → "pull with the hamstrings". -->
- p. 11, "Climbing the worked problem", frames 1 and 4: the arms were drawn
  over the head, although the hands are on the wall beyond it. The head now
  hides them, with their hidden outline dotted. In frame 4 the right arm,
  which reaches forward to R3, is hidden by the shoulder too, and the
  crossing left arm passes in front of the right hand.
- p. 236, glossary, MCL: "Drop knees and frog positions with the knee
  twisted can strain it" → "A deep drop knee can strain it, especially when
  you're tired". The book names only the drop knee as a risk to the MCL.
- p. 235, glossary, incut: dropped "Incuts are easier than they look",
  which nothing in the book supports.
- pp. 245 and 250, sources: Movement's "Intermediate Technique Series" (71
  and 242) and the Mountain Project thread "Progressing from V2 to V3
  Boulders" (68 and 247) were each listed twice. Each is now listed once,
  and the thread is cited by its own address rather than by single posts.
  Some source numbers change as a result.

### Added

### Changed
- The climber in every figure has fewer lines and a more natural shape:
  - The seams, creases, finger lines and hairline are gone, leaving the
    outline and the hems.
  - The shoulders slope and the back narrows to the waist.
  - The sleeves are snug, and the upper arms have a deltoid and a biceps
    instead of being tubes.
  - In some figures the torso bends at the waist, e.g. Drop knee (b) and
    the dyno.
- Muscles at work are stippled, in every figure where the text or labels
  say they do the work: e.g. a bent arm that pulls or presses, a leg that
  stands up or drives, the hamstring in a heel hook, the shin in a toe hook
  and the core in body tension. Straight arms, resting poses and falls have
  none.
- The hand close-ups are redrawn with an adult hand's proportions:
  - The fingers are longer and slimmer than before, and the palm deeper.
  - The wrist is narrower than the hand and the forearm.
  - Every close-up shows the same hand at the same scale, with the same
    short stretch of forearm.
  - p. 98: the hand positions plate (figure 10) is now two rows of five.
- Grade sections (Part II) and grade guides (Part III) no longer have a
  grade tab beside their heading, since the heading already names the
  grade. Grade guides start a line lower instead.
- pp. 77–78, Bumping, and pp. 90–91, Lock-off: each entry fits on one
  page, so its "Tall climbers" note no longer sits on a page of its own.
  Bumping's note drops "using the intermediates", and Lock-off's caption
  is shorter, since the figure's labels already mark the reaching hand.
  Pages from p. 78 on move up by one, and from p. 90 on by two.
- p. 131, box "Is this move meant to be dynamic?": four bullets are
  shorter, so the box fits on one page and its last bullet no longer sits
  alone on p. 132. Every page from there on moves up by one more, and the
  book is 263 pages.

### Removed
- pp. 235–236, glossary: "dab", "highball" and "macro", which the book
  never uses.

## First edition (edition-1)

The first complete edition of *Reading the Wall*, a technique handbook for
indoor bouldering, edited by Simon Gray and written and illustrated with
Claude (Anthropic).

- About 90 named techniques in five categories (feet, body, hands,
  dynamic movement and terrain). Each entry gives the grade where it starts
  to matter, how to do it, when a problem asks for it, common mistakes and
  notes for tall climbers, with figures and links to videos.
- How movement works and how to read a problem, with a worked example.
- A guide for every grade from VB to V8+, each with five things to keep in
  mind.
- Chapters on climbing tall or heavier, starting as an adult, learning
  technique and falling safely.
- A glossary, a troubleshooting table, an A–Z of technique names, a grade
  conversion table, the sources and an index.

The text and illustrations are licensed under CC BY-SA 4.0 and the code
that builds the book under the GNU GPL, version 3.
