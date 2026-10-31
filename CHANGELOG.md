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
- p. 17, Rest between attempts: the long rests (10–15 minutes after a
  30-second try, 10–25 for a long problem) are for attempts at your limit,
  as their sources say, but the section gave them as the rest for any
  attempt. It now says so, adds the sources' shorter rests for easier
  problems (30–60 seconds) and for repeats of a hard one (1–3 times the
  climbing time), and says that a session mixes the two. The
  troubleshooting row on p. 233 says "at your limit" too.
- p. 69, Straight arms, common mistakes: "Hanging slack with shrugged
  shoulders" → "Sagging onto fully straight arms with slack shoulders",
  as the source says.
- p. 98, dual texture: "The smooth part can turn a big hold into a hard
  one" → "…a big, easy hold into one that needs precise movement".
- p. 114, Re-gripping, how to do it: the step "Change grip as your body
  moves past the hold" had no support in its source. It now says to switch
  between half crimp and open hand on a long run of edges to rest the
  fingers, and the matching step adds "or pinch it", with a new source.
- p. 130, where "deadpoint" comes from: "Güllich studied the idea in the
  1980s" → "By 1987, Güllich was studying how to use the deadpoint", the
  date its source gives.
- p. 165, Tic-tac: the grade note now cites coverage of parkour-style moves
  in competition boulders. The symptom "You stood too upright against it"
  → "Lean further away from it and step quickly", as its source says.
- p. 171, Corners: "Sometimes you can let go with both hands" → "Often…",
  as the source says.
- pp. 216–224, Part IV, corrected to what the sources say:
  - Tall climbers: forum climbers say the advantage of height fades by
    about V6, not around V3–V5. "Big jumps … hips sag away from the wall on
    a dyno" → "Big moves with cut feet": tall climbers find the swing
    harder to hold.
  - RED-S: 17 of the 114 climbers "said they currently had an eating
    disorder".
  - Reading a problem first means fewer and shorter stops; the study found
    it didn't change how often climbers reached the top.
  - Novices learned from watching a video of a skilled climber.
  - The hover-hands drill holds the hand still for about 3 seconds, not 2,
    and now has a source.
- Sources: titles, authors and dates corrected for several UKClimbing
  articles, which could only be read as search excerpts before. Two
  citations now point at the Gresham articles that make their claims
  ("Toe-Hooking and Clamping" and "Technique – Use of the Toe"). E17's
  full title is "Training to Become a Better Climber – Part 3". A paper
  listed twice is listed once.
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
- p. 116, Hands and holds: an "In motion" filmstrip before the Sloper
  entry, re-gripping a sloper in five frames. The chapter had none. It
  adds a page, so pages from p. 116 on move down by one.
- Appendices: "On the mat", the book on one page to look at between
  attempts. It comes before the troubleshooting table (p. 230) and holds
  the reading steps, the three questions, one thing from each technique
  chapter and what to do when a problem doesn't go.
- Videos (Watch links and QR codes) for 21 more entries, among them most
  of the hardest techniques: Bicycle, Heel–toe cam, Pulling with the toes,
  Drop knee, Twist lock, Compression, Backstep, Opposition, Pocket, Pinch,
  Re-gripping and adjusting, Wrapping, Hip pump, Cutting loose and swing
  control, One-handed dyno, Double dyno, Jumping to a foothold, Lache,
  Arêtes, Overhangs and Roofs.

### Changed
- Title page: the subtitle is one sentence, "Learn to read a problem from
  the ground and work out the techniques you need to climb it", instead of
  a list of what the book covers. The colophon on its back says what the
  pelican on the cover is about.
- The climber in every figure has fewer lines and a more natural shape:
  - The seams, creases, finger lines and hairline are gone, leaving the
    outline and the hems.
  - The shoulders slope and the back narrows to the waist.
  - The sleeves are snug, and the upper arms have a deltoid and a biceps
    instead of being tubes.
  - The torso bends at the waist wherever a body would, e.g. sideways when
    it hangs off one arm, and forward over the knee in a rockover or over
    the hands in a mantle.
  - The top of a shoe faces the shin. A foot at or above the hip used to be
    drawn sole up, e.g. in Pogo (b) (p. 164), Mantle (frame 1, p. 104) and
    the sit start (a) on p. 217.
- Muscles at work are stippled, in every figure where the text or labels
  say they do the work: e.g. a bent arm that pulls or presses, a leg that
  stands up or drives, the hamstring in a heel hook, the shin in a toe hook
  and the core in body tension. Straight arms, resting poses and falls have
  none. The dots are large and sparse enough to stay dots on an e-ink
  screen, and the climber's grey limbs are one of its 16 greys.
- Four figures now show what their text says:
  - p. 77, Bumping: the holding arm hangs straight.
  - p. 164, Pogo (a): the arms are straight, as the label says. In (b) the
    swinging foot leads with the heel.
  - p. 156, Double clutch (b): both arms catch slightly bent.
  - p. 182, Arêtes (b): the arms hang nearly straight, since the heel hook
    rests them.
- p. 63, Crossing hands: the right hand crosses about 25 cm past the left,
  not 10.
- p. 65, Layback: the flake grows out of the wall with the crack behind
  it, instead of standing free like a pole, and is dotted where the hands
  cover it. The body hangs off straight arms with the chest lifted.
- p. 92, Twist lock: a third panel shows the lock from the side, with the
  right forearm pointing into the wall. The caption says so.
- p. 119, Gaston (b): an inset shows the arm from above, with the elbow
  out and the hand pushing the hold away, since from behind the forearm
  shows only as a stub.
- p. 139, Counter-kick: an inset in each panel shows the swing from above,
  in place of the arc over the head. The caption says so.
- p. 160, Jumping to a foothold: a close-up (b) shows the top of the toes
  behind the volume's far side, as the Toe hook figure does, and the
  caption says so.
- p. 186, Roofs: the holds are drawn like every other hold, with a light
  gripping surface.
- The hand close-ups are redrawn with an adult hand's proportions:
  - The fingers are longer and slimmer than before, and the palm deeper.
  - The wrist is narrower than the hand and the forearm.
  - Every close-up shows the same hand at the same scale, with the same
    short stretch of forearm.
  - p. 98: the hand positions plate (figure 10) is now two rows of five.
  - The half crimp's thumb rests beside the index finger, as the text
    says, instead of pointing back toward the climber.
  - The little finger reaches its hold in every grip.
  - The fingers behind the index are each drawn on their own, in three
    greys, so they stay apart on an e-ink screen.
  - A hold is dotted where the hand covers it, as in the other figures.
  - p. 148, Latching (b): the fingers behind the index hook into the jug
    too, instead of hanging in front of it.
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
  alone on p. 132. Every page from there on moves up by one more.
- With the filmstrip and the card added, the book is 265 pages, one fewer
  than the first edition.

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
