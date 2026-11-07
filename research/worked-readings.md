# Worked readings for Chapter 2: the brief

Simon accepted "Add more worked readings". This file is the brief for the people who draw the
figures, write the chapter text and mirror it on the website. The section is now built, and this file
says what is in it and why. Don't commit, tag or release anything from it.

The colours and the web edition are both on `third-edition` now (`0580e58` merged the colours,
`8ca0997` the website), so every problem must come through both. Sections 5 and 6 say how.

**What has been checked.** Three critics attacked the first version of this brief. Their findings are
fixed here or listed under "Rejected findings" at the end. All of this was then run on a scratch copy of
the repository, with a prototype `figtools/figs_reading.py`, the macros and the text below.
- Every move of all eight problems has a pose that passes `warn()` (or `problems()` for a hook) at all three
  climber sizes, except the moves a size note says are out of reach. Problem 4's poses also keep the
  body off the wall (section 7).
- All sixteen figures come through `figtools/build_all.py`, and the eight answer poses print no warning.
  They were looked at in grey and painted, including tags, arrows and leaders.
- The whole book compiled with the section in place. All sixteen pages fit, questions on odd pages and
  answers on the back of the leaf. `tools/check_fit.py` passes, and `tools/check_alt.py` reports nothing for the new figures.
- `website/build.py` built the site with the twin macros, CSS and wording rule. The section was opened in light, dark and at phone width.
- Every source key below exists, and the claims come from the entries that cite those keys.

**Round 1 of review.** Eleven reviewers then attacked the built section. Their findings are fixed here or listed under "Rejected findings", and sections 3, 4, 9 and 10 describe the section as it now stands. Every move's pose was searched again at all three sizes, and all sixteen pages were built and looked at.

**Round 2 of review.** Eight reviewers attacked the repaired section, one problem each. Each finding was checked against the drawn wall and the arithmetic. What held is fixed here, and "Rejected findings, round 2" says what wasn't taken. Sections 3, 9 and 10 describe the section as it now stands, and all sixteen pages were built and looked at again.

**Round 3 of review.** Eight reviewers attacked the section again, one problem each. Each finding was checked with new scans of clean poses at all three sizes, and with the reviewers' statics where the finding rests on them. What held is fixed here, and "Rejected findings, round 3" says what wasn't taken. All sixteen pages were built and looked at again.

**Round 4 of review.** Eight reviewers attacked the section a fourth time, and the section then had to converge. A finding was a must only if a printed statement is false against the wall and the climber as drawn, a move can't be done by geometry, the page contradicts itself or the book's entries, a route is rejected for a cost the beta also pays or called wrong when it is easier, a citation doesn't support its sentence, or the advice could injure. A rival route the page doesn't deny isn't a must, and neither is a number from a private statics model that the printed claim doesn't depend on. Two skeptics checked each must. What held is fixed here, and "Rejected findings, round 4" says what wasn't taken. All sixteen pages were built and looked at again.

**What hasn't been checked**
- Nobody has climbed these problems. The grades and the beta are judgement, and the text says so.
- Chalk and rubber on the Boox. They show on paper-sized renders only when you look for them (section 7).
- The scratch copy is a snapshot. Other sessions are still editing the book, so page numbers will move and the
  fit has to be tested again at the end.
- Reach figures come from the drawing library, whose back views ignore the wall's lean. Section 10 says how much that costs.

## 1. The set

| # | File stem | Grade | Title on the page | Wall and view | The single decision |
|---|---|---|---|---|---|
| 1 | `reading-v2-slab` | V2 | Slab | leans back 15°, from behind | One high step to the big foothold, or two small steps by way of a low volume? |
| 2 | `reading-v3-traverse` | V3 | Traverse | overhangs 10°, from behind | Which hand takes the hold that faces back the way you came? |
| 3 | `reading-v3-overhang` | V3 | Overhang | overhangs 20°, from behind | Is the big hold out to the side for a hand, a toe or a heel? |
| 4 | `reading-v4-steep` | V4 | Steep wall | overhangs 35°, **from the side** | Stay on the big low foothold, or step up to the thin high edge? |
| 5 | `reading-v4-sit` | V4 | Sit start | overhangs 15°, from behind | Hand or foot first off the mat? Your size decides. |
| 6 | `reading-v5-gap` | V5 | Long gap | overhangs 25°, from behind | Static, deadpoint or dyno? |
| 7 | `reading-v5-volumes` | V5 | Volumes | overhangs 25°, from behind | Pull down, or squeeze? |
| 8 | `reading-v6-cave` | V6 | Cave | overhangs 40°, from behind | When you swing open, back flag or toe hook? |

Each problem has `<stem>.svg` and `<stem>-answer.svg`. The titles and file names name the terrain and
never the answer, because the site's zoom links show file names.

**The required styles are all here.** Slab: 1. Steep from the side: 4. Traverse with a cross: 2. Heel
hook: 3. Dyno or deadpoint: 6. Compression on volumes: 7. Toe hook, with a swing to control: 8. Sit
start that differs for tall and small: 5.

**The grades climb** V2, V3, V3, V4, V4, V5, V5, V6, so all five hold colours from yellow to red appear.

**No two teach the same decision.** Three pairs looked close, and this is how they stay apart.
- Problems 3 and 8 both have a big hold out to one side. Problem 3 asks whether it is a hand's or a
  foot's, and the heel draws your hips under a sloper. Problem 8 asks how to stop a door, and the toe holds you in.
- Problems 4 and 6 both have a big low foothold and a higher one. Problem 4 is about what a higher right foot
  gives you while the left foot stays low and it adds no reach: a bent leg to pull and drive with. Problem 6 is about what the target can take.
- Problems 1 and 4 are both about feet. Problem 1 is the route to a foothold on a wall where you stand.
  Problem 4 is which foothold you need on a wall where you hang.

**Where the choices came from.** The base is the first designer's eight, because each has one clear decision.
The second design gave the letters that run up the wall, the stated reach, `xray=False` on question pages, tags
that keep the letter beside the hand order, the volume names X and Y, and the prompt that counts bolt holes. The
third gave the side-view prompts, the macro that prints "turn the page", the prompt about what could stay under you, and chalk and
rubber marks on the big holds.

**Which problems the critics changed**
- Problem 1: its lesson was false, because a jug at chest height made the high step easy. A is now a thin rail, feet 3 and 4 are higher, and C, D and E are higher. A smear on a 75° wall can't hold by friction alone, so the beta keeps your arms straight and hips back, and the crux moves to where your hips pass A.
- Problem 2: C and D faced each other, so no body position used both. C now faces up, D is a thin flake that costs something as a gaston, and the wrong attempt honestly goes at a higher price.
- Problem 3: the prompts no longer hand over the heel, the toe option is answered, and the finish keeps your hips under E and G.
- Problem 4: the most changed. The tiny foothold beside jug A is gone, and A itself is now the thin high edge. A higher foot adds no reach, so the reason is now the bent leg. The pose no longer goes through the wall, the finish order no longer lets go of the only edge, and footholds 5 and 6 become one foothold plus A and B.
- Problem 5: smaller start edges, a crimp as first target and six footholds instead of eight, so it no longer climbs like a ladder. A also takes the left foot later.
- Problem 6: the beta changes. The left hand goes on to D first, so the holding arm can hang straight as the deadpoint entry says. The finish hold comes down 12 cm and the ghost goes.
- Problem 7: the squeeze could be skipped. A moves down, and feet 3 and 4 move up and out, above your hands. Old move 5 and the size notes that depended on it are gone.
- Problem 8: the right foot now moves while the hook is still on, because the old order left no foot on a hold. The back flag is no longer said to fail outright, feet 3 and 4 move clear of the hinge, and the text states the locked arm.

**What round 1 changed**
- Problem 1: left foot straight from 1 to 3 made the smear unnecessary, and hips above a bare smear on this wall needed more friction than a shoe has. The shoe marks are gone. A low volume takes the smear, feet 1 and 2 are lower, the left hand goes to C before the right goes to B, and the crux is move 5.
- Problem 2: C is narrower, so a swap means two or three fingers, and the text answers it. Feet 4, 5 and 6 move so that foot 4 sits on the line under C, as a backstep asks. D holds nothing until your right hand lets go of C, so the moves and crux say that.
- Problem 3: F is within reach from foot 4 if the right foot comes off, so reach is no longer the reason. The reason is the hinge and the sloper. E faces left, A is a bucket with a rim, and foot 4 comes before the heel.
- Problem 4: the head says C takes one hand. Left foot goes up to A before the right foot goes to B, and both size notes are rewritten, since the old ones couldn't be done.
- Problem 5: the seated right leg couldn't be drawn or done. The head states the start feet, the hip turns as the bottom lifts, the figure shows move 3, and layback is gone. Foot 6 moves right, clear of the drawn arm.
- Problem 6: the right hand goes up to C before the throw, D comes down to one hand's size, and foot 6 is lower. The text says that A and B let you skip E.
- Problem 7: the most changed. A foot on A made the old moves 3 and 4 unnecessary, Y was too shallow to squeeze and its corners broke the problem. Y is narrower and its depth is stated, and the beta now stands on A. You must leave A with both hands before a foot can use it, and only the squeeze holds you meanwhile.
- Problem 8: nothing forced the left hand to go first. B comes down, E goes up and A comes up to hip height. C faces up and right, the right foot goes to 3 before the left hand moves, and the wrong try says what a flag costs.

**What round 2 changed**
- Problem 1: the figure shows move 6, because no honest lean off C can be drawn at move 5 with the right hand on B. The crux runs over moves 5 and 6 and answers move 7. The prompt no longer says something comes first. Move 3 says how far you can really rise.
- Problem 2: E, feet 4, 6 and 7 move and D becomes a straight rail, because a left hand on C with a right hand on E skipped the whole problem. The wrong try now answers that route. Move 5 stands onto the right foot as the left foot pivots, the cross goes under the arm, and the muscle dots match the words.
- Problem 3: redesigned. A route of jugs alone (match on D, feet on B and C, right hand to G) skipped the heel, the sloper and the edge, so D goes and the holds above it are re-lettered: old E, F and G are now D, E and F. The heel goes on first, with both hands still on the start jugs. Left foot to B replaces left foot to C, and the roll comes after the heel has done its work. "A toe can only push" is gone, because the toe-pull entry says otherwise. A is bigger so its marks read.
- Problem 4: the walls stay and the words change. E is called a deadpoint and the crux runs to move 7. Both routes that skip D are named. The Next no longer tells you to hang lower when the arm is already straight. "That is why your left foot stays low" becomes the trade-off it is.
- Problem 5: the feet go first, to 4 and 3, because staying on foot 2 had no benefit. The catch of C is a deadpoint for everyone. The figure shows that stance. The wrong try is now the route that goes straight for C. The tall note cites Figure 12 c, the one high foot, and frog is gone.
- Problem 6: the crux no longer states a rule that picks a rival stance over the beta. The route that skips E gets a true cost, and the rival right foot on B gets an answer. Move 5 says it is a lock-off, move 4 gives its reason, and the size notes are rewritten. The figure's holding arm opens up.
- Problem 7: Y is narrower, because the squeeze couldn't hold on the old one. The crux runs from your right hand leaving A to its catch of B. Move 2 says why the left hand goes while your hips are below A, and move 3 why the foot goes to A. The wrong try answers a knee bar. The head no longer gives the squeeze away.
- Problem 8: the page now concedes the backstep, which the book's own entries point to here. The wrong try's reach claim ran the wrong way, so it now says what a flag costs in lock. D faces up and left, C has room for one hand, the left foot goes straight from the hook to B, and both size notes are rewritten.

**What round 3 changed**
- Problem 1: move 5 sends the right hand to B before the hips move over 4, since the right hand can't stay on A that far. Move 7 shifts the hips before each step. The figure stands up on the right foot with the left arm straight, as the words say. The crux no longer says the hips pass A, or that move 7 is all feet.
- Problem 2: the page no longer rejects the route with the left hand on C for a cost the beta pays too. It moves to Next as a fair fallback. The Crux says that only your feet hold you for a moment, and the wrong try says it goes at a price. "Trap" is gone, since the wrong hand forces no fall here.
- Problem 3: redesigned again. A right hand on A freed the start jug C for the right foot, which gave a route with no heel. B and C become one thin rail, B, and old D, E and F become C, D and E. A jug would still have let a right foot share it with the right hand, so the start is thin. The left foot goes up to B and stands before the roll, so the page no longer does what it condemns. The heel sits in A's bowl.
- Problem 4: the right hand stays on D through the rise to E, so D gives the rise something above you. D is a new profile whose top falls 28° from level, not 53°. The route that skips D is both toes on A, and foot 4 adds nothing to it. The caption says hips in and low, and why the hip turn doesn't show.
- Problem 5: the wrong try's reasons were false, so it now says the try is at its limit. The figure has the hips lower and the leg in front of the arm. Everyone steps to foot 5 before the left hand goes to D. The hips come square at move 3. The small note drops its crossed left foot and matches with that foot on the wall.
- Problem 6: the finish moves the lower hand first, so the left hand goes to F. That also gives the route over A and B a true cost. The size note for small climbers steps both feet up, because A and 6 only touches E. The Next no longer tells you to sag further out. The prompt no longer says the jump tempts you.
- Problem 7: the fallback could not hold, so it now takes Y with the right hand first, and the page says that order is easier on the palms. The small note lets the left foot leave A. "Your feet can only push you out" now applies only on X. Moves stop using "upper face" for Y.
- Problem 8: the page concedes the heel and the plain throw, and it gives the backstep's real costs. The kick is gone, since it answered a case that hardly exists. Move 3 says the deadpoint isn't optional, the hook leg is drawn straighter, and the facings are stated. Both size notes are rewritten.

**What round 4 changed**
- Problem 1: words only. A is at shoulder height. The step to 3 is measured from the foot you stand on, since move 2 makes the same step from the volume. Move 2 puts your hips over the volume first. The crux says only the reach to E is on your feet alone.
- Problem 2: the page no longer calls a swap no better. The beta has its own moment with no hand, and the Matching entry teaches the swap, so the page says where it leads and what it costs. D is drawn thinner than C and the head says it can't be pinched. The caption says which foot you stand on, move 3 gives the backstep's reason and move 5 loses its stray "it". The crux says no hand holds you in, which is true on any model.
- Problem 3: the heel lesson stays. "You must stand on 4 and 3" is gone, because its hip range was scanned with the wrong right hand and other stances exist. "It looks like a jug" is gone, because A is one. The wrong try is now the right foot off, and Next concedes the hand on A with the heel beside it. The caption no longer says the heel draws your hips up at move 4, and move 6 says higher than A.
- Problem 4: the crux states the turn on flat C, as Problems 2 and 5 do. The tall note lost a sentence to pay for it. Move 7 lets go as the rise slows, in the Deadpoint entry's words. Wrong says your feet tend to come off. Next says you catch D with your hips out, since move 6 also has both toes on A once you hold D. The right shin no longer covers B.
- Problem 5: move 4 says to rise before the step to 5. Skipping E has a true cost, because the old one was paid by the left hand's move too. Wrong answers setting both feet before the lift. Step 5 asks what you do if it is only just in reach. The left shin is foreshortened so A and the hand show, and the dots are on the right arm and both thighs.
- Problem 6: move 5 says why you leave C for D. The crux no longer calls D far smaller than C, and the throw off D is reworded. The small note says you are still short from A and 6, because the plane figure's 0 cm ignores the wall. Step 5 asks the reader to count holes to E. Move 1 is shorter to pay for this.
- Problem 7: printed order and figure stay. Next gives the page's one answer to "Does the order matter?": left or right doesn't, a foot on A before your second hand does. The mirror sentence moves there from the caption. Move 2 sends the right hand before your hips pass A and without "fast", which the Volumes entry warns against. The caption says start of move 3, because the drawn hips are above A. The fallback says hips low and well left of A.
- Problem 8: the toe stays and the heel is still conceded. Wrong now says what the flag costs: C at your chest can only press. Move 3 presses until the hook leg goes tight. B's tag sits on free wall with no leader across the thigh. Next's backstep sentence now cites B44, because B42 says nothing about the outside edge or foothold size.

**Rejected designs**
- The third design's roof. It would be a second side view with eleven ceiling holds and untested poses,
  and its answer wouldn't fit a page. It is the first alternative if Problem 8 fails by eye.
- A person standing on the mat for scale on each question. It adds 25 mm of width and looks like a hint.
  The bolt holes do the job, and the chapter already teaches counting them.
- A small profile inset for the wall angle. The line under the head gives the angle in words.
- Drawing tall and small climbers beside each other in Problem 5. Three panels took the page set for one
  and spilled about 270 pt onto a second, and they would have broken the rule that every climber is the
  same size. The notes say what differs, and the tall note points to the existing `@fig-cons-sit`.
- A second traverse or a second V2. A cross at V2 is fair, but this one's small-climber fallback is a
  deadpoint, which belongs at V3.

## 2. The section in Chapter 2

**Place.** The last section of Chapter 2, after "Indoor grades". The answers use "When to change the
beta" and the size box, the grades need "Indoor grades", and sixteen pages in the middle would split
the chapter. Chapter numbers don't change. The `reading-worked-problem` figure, its filmstrip and their
text stay exactly as they are.

**Heading and label**
```typst
== Eight problems to read <reading-problems>
```

**Opening text, ready to use.** This is the one label for the whole section, so don't repeat "(judgement)"
on the beta itself. Facts about technique that go beyond the entries still carry a source or "(judgement)".

```typst
#ix("Route reading!practice problems", main: true)
These eight problems are invented for this book. No gym has set them and nobody has climbed them, so the grades are rough and the #jt("beta") is this book's judgement. They run from about V2 to about V6 in different styles, and the harder ones are worth reading even if you can't climb that grade yet.

Read each drawing using the method in @reading-method, answer the prompts and make your plan, then turn the page and compare. Your beta may be as good as this one, especially if you are much taller or smaller than the climber it was worked out for, who stands about 1.75 m and reaches about 2.1 m from toes to fingers, or about ten and a half bolt holes.

Letters mark holds big enough for a hand and numbers mark holds only a foot can use, though a lettered hold can still take a foot. Letters and numbers run up the wall, or along it on the traverse, so their order says nothing about the sequence. Tape marks the start, and volumes count. The dots are bolt holes 20 cm apart, so you can count distances as "Reading for your size" suggests. Short streaks on a hold are shoe rubber, and a smudge just below its lip is chalk.

On the answer drawings, D R3 means hold D, taken by the right hand as the third hand move. The numbered moves also count the feet, so the two numbers don't match.
```

**Two small additions elsewhere in the chapter**
- Opening paragraph (line 12): "This chapter gives you that method, then covers planning attempts,
  resting between them and reading gym grades, and ends with eight problems to read for yourself."
- At the end of the first paragraph of "The method, step by step": "@reading-problems gives you eight drawn problems to practise on." As a line of its own after the keypoint, it broke the hold table and the size box.
- The heading "What to read first" gets the label `<reading-first>`, for Problem 1's Step 2. A section reference names no technique, so it is safe on a question page.

**Size.** Sixteen pages for the problems, plus the opening text on the end of "Indoor grades" and at most
one blank page before Problem 1.

## 3. How each page pair looks

The form is the same eight times, so nothing here needs a decision per problem.

**Question page**
1. The head, in the style of the chapter's `#step`: `PROBLEM 1` in small caps, then the title in bold.
2. A short paragraph: "About [V2 tab]. The wall leans back 15°, seen from behind. Start: both hands on A.
   Finish: both hands on E."
3. The figure on the right, with "Read it yourself" and the prompts on the left. Every question figure
   is 92 mm wide or less, so all eight sit beside their prompts in the same layout as an entry's steps.
4. At the foot of the page, set right in the caption size: *Make your plan, then turn the page.*

The space under the figure stays empty. It keeps the page calm and leaves room for notes on a
tablet, so don't enlarge anything to fill it. The figure carries only holds, tape, grid, mat, letters and numbers. It has
no climber, arrows, step numbers, L or R, crux box or labels.

**Answer page**
1. The head: `PROBLEM 1`, then **The answer**.
2. "The moves" as a numbered list on the left, with the figure and a short caption on the right.
3. Across the full measure, as run-in bold labels: **Crux.** **Why the obvious try fails.** **What to try next.**
4. *Tall climbers.* and *Small climbers.*, with their icons as in an entry, only where the beta differs.
5. A foot line in the entry's apparatus type: `ENTRIES` and the linked entries with their pages. It has no rule above it, which would cost two lines on every page.

**Pages.** A question starts on an odd page, so in a two-page view its answer is on the back of the leaf
and doesn't face it. On a single-page e-reader nothing changes. The first question may need a blank
page before it, depending on where "Indoor grades" ends. In the last test build it didn't. If an answer spills to a second page,
report it and don't squeeze it: the next question would then bring a blank page.

**Fit.** All sixteen pages were set with the macros in section 4 and the text in section 9, in the whole book with the
real figures, so the links and page numbers are real. Text may run down to about 780 pt, and the answers end here:

| Problem | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Lowest text, pt | 766 | 777 | 779 | 777 | 770 | 771 | 775 | 777 |

A foot line needs its half line and one note line, so a problem with one has to end its notes by about 753 pt. Page numbers changing elsewhere could tip Problems 2, 3, 4 and 8, which have less than a line to spare. If one tips, cut words from its Next. Don't cut Problem 4's "Square your hips once you hold it": the Sloper entry lists twisting into the hold as an error. On Problems 2, 4 and 5 the moves are taller than the figure, so words in the moves cost page height there. A two-line foot line, as on Problem 1, needs another line of room. As a limit when you edit, keep
to about 140 words of moves beside the figure and about 240 words below it. Words beside the figure cost no page height if the figure is the taller. If a page spills, cut a sentence:
don't shrink a figure or close up a space. A full line parts the figure block from Crux, as under a figure in an entry, and a half line parts the notes from each other. That half line is this element's design. It is smaller than any step the template otherwise uses, and `gap(0.6)` would cost every page two or three points per note, so Simon may want to decide it.

## 4. The macros

Two new macros, both in `book/template.typ` and both mirrored in `website/template.typ`. They are built
from what is already there: `labelled-steps`, `beside-steps`, `section-label`, `grade-tab-inline`, `tref`
and `aside-icon`. Set the head locally, as `reading-head` below does; it is print-only and needs no twin.

**`book/template.typ`**, after `beside-steps` and `wide-figure-block`:

```typst
// ------------------------------------------------------------ worked readings

// The problems at the end of Chapter 2: a question page, then an answer page. A
// question starts on an odd page, so in a two-page view its answer is on the back
// of the leaf. website/template.typ has its own versions of these two macros.
#let reading-head(n, title) = block(above: 0pt, below: gap(0.5), breakable: false, sticky: true,
  text(size: fs.sub)[#section-label[Problem #n]#h(0.6em)#text(weight: 700, title)])

// Every figure here is under 92 mm wide, so it always sits beside its text.
#let reading-layout(label, steps, file, caption) = context beside-steps(
  labelled-steps(label, steps, 1), "figures/" + file, caption, 1)

#let reading-question(n: none, title: none, grade: none, wall: none, start: none, finish: none, figure: none, prompts: none) = {
  pagebreak(weak: true, to: "odd")
  reading-head(n, title)
  [About #grade-tab-inline(grade-label(grade), g: grade). #wall Start: #start Finish: #finish]
  reading-layout([Read it yourself], prompts, figure, none)
  v(1fr)
  align(right, text(size: fs.caption, emph[Make your plan, then turn the page.]))
}

// A full line parts the notes from the figure above them, as under a figure in an
// entry. The notes belong together, so half a line parts them from each other.
#let reading-answer(n: none, figure: none, caption: none, moves: none, crux: none, wrong: none, next: none, tall: none, small: none, entries: ()) = {
  pagebreak(weak: true)
  reading-head(n, [The answer])
  reading-layout([The moves], moves, figure, caption)
  block(above: gap(1), below: 0pt, [#text(weight: 700)[Crux.] #crux])
  for (head, body) in (([Why the obvious try fails.], wrong), ([What to try next.], next)) {
    if body != none { block(above: gap(0.5), below: 0pt, [#text(weight: 700, head) #body]) }
  }
  if tall != none { block(above: gap(0.5), below: 0pt, [#aside-icon("tall")#text(weight: 700, style: "italic")[Tall climbers.] #tall]) }
  if small != none { block(above: gap(0.5), below: 0pt, [#aside-icon("small")#text(weight: 700, style: "italic")[Small climbers.] #small]) }
  if entries.len() > 0 {
    block(above: gap(0.5), below: 0pt, {
      set text(size: fs.note)
      set par(justify: false, leading: 0.68em, hanging-indent: 1em)
      [#sc[Entries]#h(0.45em)#entries.map(k => tref(k)).join(", ")]
    })
  }
}
```

**`website/template.typ`**, in the figures section after `entry-figure`:

```typst
// A problem of "Eight problems to read". There is no page to turn here, so the
// answer stays closed until the reader opens it.
#let reading-question(n: none, title: none, grade: none, wall: none, start: none, finish: none, figure: none, prompts: none) = cls("section", "reading-question", {
  cls("h5", "step", { section-label[Problem #n]; " "; title })
  tag("p", [About #grade-tab-inline(grade-label(grade), g: grade). #wall Start: #start Finish: #finish])
  cls("section", "how", {
    labelled([Read it yourself])
    prompts
    entry-figure(figure, none, false)
  })
})

#let reading-answer(n: none, figure: none, caption: none, moves: none, crux: none, wrong: none, next: none, tall: none, small: none, entries: ()) = tag("details", attrs: (class: "reading-answer"), {
  tag("summary", [The answer to problem #n])
  cls("section", "how", {
    labelled([The moves])
    moves
    entry-figure(figure, caption, false)
  })
  for (head, body) in (([Crux.], crux), ([Why the obvious try fails.], wrong), ([What to try next.], next)) {
    if body != none { tag("p", [*#head* #body]) }
  }
  if tall != none { cls("div", "climber-note", { aside-icon("tall"); [*_Tall climbers._* ]; tall }) }
  if small != none { cls("div", "climber-note", { aside-icon("small"); [*_Small climbers._* ]; small }) }
  if entries.len() > 0 { cls("dl", "apparatus", { tag("dt", "Entries"); tag("dd", entries.map(k => tref(k)).join(", ")) }) }
})
```

The `section.how` and `entry-fig` classes reuse the layout that `lay_out_steps` already gives an entry,
so a figure under 66 mm wide goes beside the prompts on a wide screen and the others go below them. At phone width a figure that would go beside comes above the prompts, as it does in an entry.
`dom.py` already knows `details` and `summary`.

**Use in the chapter**
```typst
#reading-question(
  n: 1, title: [Slab], grade: 2,
  wall: [The wall leans back 15°, seen from behind.],
  start: [both hands on A.], finish: [both hands on E.],
  figure: "reading-v2-slab.svg",
  prompts: [
    - *Step 2.* ...
  ],
)
#reading-answer(
  n: 1,
  figure: "reading-v2-slab-answer.svg",
  caption: [...],
  moves: [
    + ...
  ],
  crux: [...], wrong: [...], next: [...],
  entries: ("slab", "smearing", "volume", "sidepull", "rockover", "high-step"),
)
```

## 5. Colours

`paint.py` runs at the end of `figtools/build_all.py`. It reads the grade from `reading-v(\d+)-`, so question
and answer take the same hold colour with no `CHOSEN` entry: V2 yellow, V3 orange, V4 blue, V5 purple, V6 red.
The grade tab on the question page takes the same colour through `g: grade`, so the tab and the holds agree as
they do in an entry. All sixteen were painted this way in the scratch build, and the tabs matched. The new figures need nothing more than these rules.

- **Draw and judge in grey** with `python3 figtools/build_all.py --grey`, then check again in colour.
- **Holds:** only `hold()` and `hold_side()`. They bring the surface and the shadow with them.
- **Volumes:** only `volume()`, with no `shades=`, so they stay neutral with their facets.
- **Block arrows:** only `body_arrow()`, with no `fill=`, so they turn amber.
- **Muscle dots:** `active=` on the climber.
- **Don't use a hold's greys for anything else.** `DARK`, `HOLD_DEEP`, `HOLD_MID`, `HOLD_LIGHT` and `HOLD_PALE` are
  replaced by value. Tape stays `INK` and tags stay `WHITE` and `INK`.
- **Yellow is lighter.** V2 holds sit on `#aaaaaa` on a monochrome screen, where the others sit on `#555555`. So
  Problem 1 is the one figure pair where the white lip has less to stand out against. C is enlarged for that reason (`w=17, h=8`), and on the painted file turned to grey its direction now reads. Check it again on the Boox.
- **If a grade changes,** rename both files and their `figure-alt.toml` keys, and change `grade:` in the chapter.
- **Text never names a colour,** in a caption, a prompt or a description. Descriptions don't name tones either:
  no dark, white, grey, shaded or faint.

## 6. Website

The web edition needs these additions, and all of them belong in the same stage as the chapter text.
They were all built on the scratch copy and worked as written.

1. **The twin macros** in section 4. `show pagebreak: none` already removes print's breaks, so without the
   twins an answer would sit straight under its question.
2. **`website/style.css`**, near `.how`:
   ```css
   .reading-question { margin-block-start: 2rlh; }

   .reading-answer {
     margin-block-start: 1rlh;
     padding-block: .35rem;
     border-block: var(--rule-light);

     > summary {
       letter-spacing: .08em;
       list-style: none;
       cursor: pointer;

       &::-webkit-details-marker { display: none; }
       &::before { content: "›"; display: inline-block; margin-inline-end: .5em; font-weight: 700; }
     }
     &[open] > summary::before { rotate: 90deg; }

     /* print parts these notes by half a line and indents none of them */
     > :is(p, .climber-note) { margin-block: .5rlh 0; text-indent: 0; }

     /* a caption wraps under its image instead of widening the figure's column */
     .how.beside figcaption { contain: inline-size; }
   }
   ```
3. **`website/wording.json`**: add this rule. `PRINT_WORDS` wouldn't catch the phrase, so the check won't warn you.
   ```json
   {"find": "then turn the page and compare", "replace": "then open the answer and compare"}
   ```
   The rule works on one text node, so keep the phrase free of markup in the chapter.
4. **`book/figure-alt.toml`**: sixteen new tables, sorted in with the others, using the descriptions in
   section 9. Keep each to one short sentence of about 125 characters that gives the gist. A question's
   description must not give the sequence. Take `drawn` from the final painted files, since `check_alt.py`
   hashes what is in `book/figures`.
5. **Dark mode** needs nothing. `dark.py` handles holds, volumes, tags and tape from the helpers.
6. **Width.** Only Problems 2 and 4 are wider than `BESIDE_MM`, 66 mm, so on the site those two figures go below their prompts and the other six sit beside them. At phone width those six come above their prompts, and the page doesn't scroll sideways.
7. **Links.** Don't put `#tref` on a question page. It would name the technique in the page's links and in
   "Referenced from". `#jt` is fine there, because a glossary link names nothing the prompt hasn't named. The whole section counts as one "Referenced from" link on each entry it mentions. On the current text, a link to `overhang` pushes that entry from two pages to three, so `overhang` stays out of the `#tref`s and foot lines here. Run `tools/check_fit.py` and report any other entry that spills.

Search will find answer text inside a closed `details`, and that's fine.

## 7. Drawing rules

**Module.** A new `figtools/figs_reading.py` with `build(out)`, which `build_all.py` finds by itself. Don't edit
`climb.py` or another module. Import what exists:

```python
from climb import *
from figs_terrain import tag
from figs_feet import FootClimber, problems
from figs_dynamic import _side_grip, _side_foot
from figs_body import _hinge
```

**One wall function per problem,** shared by its two figures, as `worked_problem_wall` does. Both figures
use `Fig(..., scale=0.32)`, so a problem looks the same on both pages.

- **Back views:** `ground(f, 0)` and `wall_grid(f, x0=x0+4, x1=x1-4, y0=10, y1=y1-4)`.
- **Tape:** as in `worked_problem_wall`, a rectangle from `(x-1.6, y)` to `(x+1.6, y-9)`, `fill=INK, stroke=None, z=-4`.
- **Chalk and rubber.** `chalk=True` on any hold a hand takes, and `rubber=True` on footholds and on a hold only a foot takes. The library shows these marks only on big holds: chalk mainly on bucket and horn jugs, rubber only on holds at least 1.5 mm tall on paper. `hold_side` has neither, so Problem 4 has none. Only Problem 3's prompt relies on them, which is why its shapes are fixed in its table. If the streaks on its A don't read on the Boox, enlarge A.
- **Question figures:** `xray=False` on every hold. Tags from `figs_terrain.tag` for letters. Numbers from
  `f.text(str(n), p, size=6.2, weight=600)`.
- **Answer figures:** `xray` on the holds the climber touches and on any hold that gets a leader, as `worked_problem_wall(f, used)` does.
  Keep the letter and add the hand order in the same tag, such as `B R1` or `E R4 L5`, in the same order as the moves.
- **Nothing sits on the climber,** as `research/ILLUSTRATION.md` says. A number or letter the climber would cover gets a leader to a free spot. For a number, keep its weight with `f.label("", at, to=p)` followed by `f.text(str(n), at, size=6.2, weight=600)`.
- **Arrows:** `f.arrow(pts, kind="move")` for hands and feet, only where they stay off the climber. The tags
  carry the rest of the order. Don't cross a limb with an arrow or a label. `f.step(n, ...)` uses the number of the move in the list.
- **Poses:** use the `lh`, `rh`, `lf`, `rf` given. Hand positions are `grip(pos, use=, kind=, size=)` and foot
  positions `stand(pos, size=)`. `stand()` returns a point, so a foot with an angle is written `{"at": stand(p), "angle": a}`. After drawing, `warn()` or `problems()` must report nothing.
- **Side views need one check more,** because `warn()` doesn't test the wall. In Problem 4, measure each joint's distance from the wall line and require at least 12 cm for the hips, 10 for the shoulders, 11 for the head and 3 for the elbows and knees. A limb shortened by `leg_len` or `arm_len` points at the viewer, as in the side view of the twist lock, which uses 0.62.
- **Look at every figure at 150 dpi**, as `research/ILLUSTRATION.md` says. The tag points below were drawn and looked at, but not at print size on the Boox, so move any that look wrong.
- **Hold direction must read.** It is what the reader is asked to find. If a lip doesn't read at print size,
  enlarge that hold and tell the writers.

**A hold faces the way `use` points.** You pull the opposite way, with your body on that side. So a hold facing right (`use` below 90) is a right-hand sidepull with your body on its left, and a left-hand gaston with your body on its right. Check the sign against the table in "Hold direction and body position" whenever you turn a hold.

**Coordinates** are world centimetres. Back view: x runs to the climber's right. Side view: the wall is on
the right.

## 8. Rules for the text

These are additions to `research/REVISE-3.md`, `research/STYLE.md` and the `natural-phrasing` skill.

- The moves below are ready to paste. Edit them only for fit or a real fault, and rerun the page test.
- Say "right hand" and "left foot" in full. Moves stay short and imperative. Running text joins its sentences.
- Add a size note only where this brief has one. A problem with no note has no real difference.
- Gloss a jargon word once in the chapter, then keep the `#jt`. The text already glosses `off foot` and `hinge`, `deadpoint` at Problem 4 and `dyno` at Problem 6.
- A `#tref` that isn't an entry's own name needs `body:` in lower case, or it prints the entry's capitalised name. Give a technique's first mention on the page a `#tref(..., show-page: false)` where it helps. The foot
  line carries the page numbers.
- The foot lines list the entries a problem turns on. Where a page had no room, hip turn, half crimp and flag are linked in the text instead.
- Every technique is at or below its problem's badge, so no problem needs a "stretch" label. A technique named
  only as what fails is marked in its list.
- No colour names and no personal details. The 1.75 m and 2.1 m in the opening describe the drawn climber.

## 9. The eight problems

In the hold tables, `use` is the direction a hold faces in degrees (90 up, 0 right, 180 left), and a type with
no `use` faces up. In the poses, a letter stands for that hold's point, and `stand(3)` means `stand` at foothold 3's
point. The moves, notes and captions are the chapter's text. **Crux**, **Wrong** and **Next** fill the macro's `crux:`,
`wrong:` and `next:`. Every problem's moves begin with its start feet.

---

### Problem 1: `reading-v2-slab`

About V2. Slab, leaning back 15°, seen from behind. Decision: one high step to the big foothold, or two small steps by way of a low volume?

| Hold | x, y | Type | What it offers |
|---|---|---|---|
| A | -6, 150 | crimp, `variant="rail"`, size 1.3 | Start, both hands. A thin edge: it won't pull you up over a high foot. You press down on it once your hips pass it. |
| B | 48, 228 | sloper, `variant="dome"` | Right hand. It has no edge and only steers. |
| C | -38, 250 | crimp, `use=180, w=17, h=8` | Left hand. A sidepull: lean right off it. |
| D | 30, 296 | crimp, `variant="rail"` | Right hand, half crimp. |
| E | 2, 348 | jug, `variant="bucket"` | Finish, both hands. |
| 1, 2 | -24, 16 and 20, 22 | foot, size 1.15 | Start feet. |
| 3 | -20, 92 | foot | 70 cm above foot 2, so just below mid-thigh: a real high step, and the fallback the text names. |
| 4 | 30, 112 | foot, size 1.6 | The obvious big foothold, 90 cm above foot 2 and level with your hips. 20 cm above foot 3. |
| 5, 6, 7 | -12, 128 and 26, 165 and -22, 200 | foot | Small. Each is 16 to 37 cm above the foot you stand on when you step to it. |
| volume | `[(4,42), (44,40), (50,56), (30,68), (8,62)]`, apex (26, 54) | `volume()` | The smear: right foot at (24, 60). Its upper face lies far flatter than the wall, so friction can hold you (about 28° from level at 15 cm deep) and your hands only balance. |

**Head:** `wall: [The wall leans back 15°, seen from behind.]`, `start: [both hands on A, feet on 1 and 2.]`, `finish: [both hands on E.]`

**Prompts**
- *Step 2.* The wall leans back. What does @reading-first say to read first?
- *Step 3.* Which way does C face? What can you do with B?
- *Step 4.* Give B, C and D an L or an R.
- *Step 5.* Foothold 4 is the big one. Count the bolt holes to it from foothold 2. How high is that compared with your hips? Which foot goes there? How does it get there?
- *Step 6.* Where will you have least to pull on?

**Moves**
+ Left foot on 1, right foot on 2. #tref("smearing", body: [Smear], show-page: false) your right foot on the #tref("volume", body: [volume], show-page: false), heel low.
+ Move your hips over it and stand up. Left foot to 3.
+ Move your hips over 3 and rise until your arms are straight. Right foot to 4, only 20 cm above 3.
+ Press down on A with your right hand. Left hand to C, a #tref("sidepull", body: [sidepull], show-page: false). It faces left, so you lean right off it.
+ Right hand to B, only to steer. Move your hips over 4 and rise.
+ Left foot to 5. Stand up on your right foot and lean right until your left arm is straight. Right hand to D.
+ Move your hips over 5. Right foot to 6 and stand on it. Left foot to 7 and stand on it. Right hand to E.
+ Left hand to E.

**Crux:** Moves 5 and 6. Your right hand leaves A and your hips move right of it. C only stops you tipping right. B has no edge. So your feet hold you until your right hand reaches D. Move~7 is easier. You hold D while your feet move. Only the reach to E is on your feet alone.

**Wrong:** You stay on A and step from 2 to 4, the biggest foothold. That is about 90 cm, level with your hips. Your knee folds tight and your hips have a long way to cross. A is a thin edge at shoulder height, so it helps little. Reaching for B falls short and brings your chest to the wall. Leaning in pushes your feet off #src("E3", "E24"). A high step on a slab upsets your balance #src("A34"). When the big foothold is a long step, look for a smear on the way.

**Next:** If the smear slips as you stand, drop your heel and keep your hips over the foot. Commit all your weight at once #src("E1", "E3", "E16"). If the shoe still skates, stand further out on the volume #src("E5", "E18"). You could also skip the volume: stay on 2 and take your left foot to 3. That small foothold is about 70 cm above the foot you stand on.

**Entries:** `("slab", "smearing", "volume", "sidepull", "rockover", "high-step")`

**Techniques and badges:** `slab` V2, `smearing` V1, `volume` V2, `weight-shift` V0, `precise-footwork` V0, `rockover` V1, `sidepull` V1, `half-crimp` V2, `matching` V1. `high-step` V1 is what fails.

**Tall or small:** none. Every size passes every move. With the left hand on C and feet on 3 and 4, the right hand holds A only until the hips are near 3: x=5 at the ordinary size, 8 small and 29 tall, unless you lean left. So the right hand goes to B before the hips move over 4. Reaching for B from feet 1 and 4 with the left hand on A leaves the ordinary climber 11 cm short and the small climber 30 cm short. The tall climber has 9 cm to spare.

**Question figure:** `Fig(-90, -8, 90, 366)`, 58 × 120 mm. Tape at (-20, 146) and (8, 146). `volume(f, SLAB_VOLUME, apex=(26, 54))` before the holds.
Tags: A (13, 154), B (63, 230), C (-27, 253), D (44, 297), E (16, 350).
Numbers: 1 (-14, 17), 2 (30, 23), 3 (-11, 93), 4 (42, 113), 5 (-3, 129), 6 (36, 166), 7 (-13, 201).

**Answer figure:** same frame, showing move 6. `Climber((36, 203), lean=8, lh=grip(C, use=180, kind="crimp"), rh=grip(D, kind="crimp"), lf=stand(5), rf=stand(4, size=1.6), active=("lfore", "rthigh"))`. The left arm is 64.5 of 65 cm long as drawn and the right knee is about 137°. `xray` on A, B, C, D and feet 4 and 5. The small climber's clean pose is at (30, 202), lean 8.
Tags: `C L1` (-61, 253), `B R2` (74, 230), `D R3` (58, 297), `E R4 L5` (31, 350), and A at (-66, 160) with a leader to (-14, 150).
Bare numbers 1 (-14, 17), 2 (30, 23), 3 (-11, 93), 6 (15, 166), 7 (-13, 201), and with leaders: 4 from (72, 112) to (38, 112), 5 from (-62, 126) to (-18, 128).
Foot arrows `[(20, 26), (24, 61)]`, so the first ends on the volume's upper face with room further out, `[(-23, 22), (-21, 84)]` and `[(26, 70), (29, 108)]`, with `f.step(1, (8, 31))`, `f.step(2, (-33, 54))` and `f.step(3, (16, 92))`.

**Caption:** Move 6. Read a slab's feet first: the volume turns the long step to 4 into two. The discs are moves 1 to 3.

**Alt, question:** A slab from behind with five lettered holds, seven numbered footholds and a low volume.

**Alt, answer:** The same slab with a climber on the big foothold; arrows take the feet up by way of the volume.

---

### Problem 2: `reading-v3-traverse`

About V3. A traverse moving right, overhanging 10°, seen from behind. Decision: which hand takes the hold that faces back the way you came?

| Hold | x, y | Type | What it offers |
|---|---|---|---|
| A | -150, 208 | jug, `variant="bucket"` | Start, both hands. |
| B | -92, 216 | jug, `variant="flat"` | Room for both hands. |
| C | -38, 222 | crimp, `w=11, h=6` | Faces up, with room for one hand, so a swap means two or three fingers. You hang straight under it. |
| D | 14, 208 | crimp, `use=180, w=15, h=5, variant="rail"` | A thin upright flake facing left, as straight as C so its direction reads, and thinner than C so "thin" is true as drawn. Its back is smooth, as the head says. With your hips on its left it is a right-hand gaston and holds a left hand nothing. With your hips past it, a left-hand sidepull. |
| E | 86, 212 | jug, `variant="bucket"` | Finish, both hands. Far enough along that a left hand on C has to pull it about 30° sideways at the catch. |
| 1 | -168, 44 | foot, size 1.15 | Start, left foot. |
| 2 to 7 | -128, 36 and -90, 42 and -26, 50 and 8, 62 and 50, 40 and 88, 44 | foot | A line along the wall. Foot 4 sits a little right of the line under C, as a backstep asks. |

**Head:** `wall: [The wall overhangs 10° and runs to the right, seen from behind. D's back is smooth, so you can't pinch it.]`, `start: [both hands on A.]`, `finish: [both hands on E.]`

**Prompts**
- *Step 3.* Which way does each hold face? Where does your body go for each hand on D?
- *Step 4.* Give each hold an L or an R. Which holds have room for both hands?
- *Step 5.* Which foot do you stand on as your hand lands on D? What does the other foot do?
- *Step 6.* Where does the wrong hand cost you most?

**Moves**
+ Left foot on 1, right foot on 2. Right hand, then left hand to B. Walk your feet to right foot on 4, left foot on 3.
+ Right hand to C, which faces up. Hang under it on a straight arm.
+ Right foot to 5 as your #jt("off foot") (it presses to stop a swing). Left foot to 4 on its outside edge, toes right (a #tref("backstep", body: [backstep], show-page: false), to clear your chest).
+ Turn your #tref("hip-turn", body: [left hip to the wall], show-page: false) as your left hand leaves B. Left hand under your right arm to D, which faces left. Keep your right foot pressing.
+ Move your hips towards foot 5. Stand up on that foot as you let go of C. Lean right off D as your left foot #tref("pivoting", body: [pivots], show-page: false), toes left. Right hand to E. D is now a #tref("sidepull", body: [sidepull], show-page: false).
+ Walk your feet along to right foot on~7, left foot on~6.
+ Left hand to E.

**Crux:** The #tref("cross-through", body: [cross], show-page: false) in move 4. Then letting go of C. C is a flat edge, which loses grip as you turn #src("B38"). D holds nothing yet, so C holds you. D becomes a sidepull only once your shoulder passes it. Your right arm stops that. For a moment no hand holds you in: keep moving right.

**Wrong:** The mistake is arriving at D with the wrong hand. C is too small to match and D is too thin to share (judgement). So your right hand goes on to D with your left still on B. With your body on D's left, D is a thin #tref("gaston", body: [gaston], show-page: false). You then let go of B with only that to pull on. Your shoulder does most of the work #src("C34"). It can go, but you pay twice: this gaston, then E with your left hand on C pulled sideways (judgement). Swapping hands on C leads to the same catch, after a moment on two or three fingers of a flat edge. A hold that faces back the way you came only works as a sidepull once your shoulder is past it.

**Next:** If your chest blocks the cross, roll further onto your left hip #src("B49"). If you can't let go of C, cross your left hand from B to C instead. Then take your right hand past D to E. You pull C about 30° sideways at the catch. If you are small, E is out of reach from C.

**Entries:** `("traverse", "cross-through", "sidepull", "backstep", "gaston")`

**Techniques and badges:** `traverse` V2, `cross-through` V2, `backstep` V3, `pivoting` V2, `matching` V1, `sidepull` V1, `hip-turn` V2, `half-crimp` V2, `edging` V0, `straight-arms` V0, `barn-door` V1. `gaston` V3 is what fails.

**Tall or small:** only the last sentence of Next. Every size reaches D. Every size can go from feet 4 and 5 to E once the left foot pivots, but with its toes still right the small climber is 8 cm short, which is why move 5 turns the foot. The small climber can't hold C from feet 5 and 6, so the moves let go of C before the feet walk on.

**Question figure:** `Fig(-185, -8, 102, 262)`, 92 × 86 mm (91.8 mm, so it still sits beside). Tape at (-164, 204) and (-136, 204).
Tags: A (-136, 211), B (-77, 218), C (-24, 224), D (26, 210), E (71, 214).
Numbers: 1 (-158, 45), 2 (-118, 37), 3 (-81, 43), 4 (-17, 51), 5 (18, 63), 6 (60, 41), 7 (97, 45).

**Answer figure:** same frame. `Climber((-36, 120), turn=-1.0, lean=12, bend=8, head=(2, -2), lh=grip(D, use=180, kind="crimp"), rh=grip(C, kind="crimp"), lf={"at": stand(4), "angle": 0}, rf={"at": stand(5), "angle": -10}, knees={"r": "up", "l": "right"}, elbows={"r": "down", "l": "up"}, allow_cross=True, active=("rfore", "lthigh"))`. This mirrors the pose in `cross_through`, with the hips about 10 cm from the foothold and the right elbow at 164°. The arm runs between the face and the wall, so it is a cross-under. `xray` on C, D and feet 4 and 5.
Tags: A (-136, 211), `B R1 L2` (-99, 227), `C R3` (-58, 228), `D L4` (31, 210), `E R5 L6` (78, 224). Numbers as on the question.
One arrow for the cross, from B towards the right arm: `[(-82, 208), (-64, 199), (-46, 198)]`, with `f.step(4, (-68, 186))` beside it so it can't read as the right hand going to C. It stops short of the arm, so it crosses no limb.

**Caption:** Move 4. You stand on your left foot with that hip at the wall. The right foot presses. The left hand crosses to D.

**Alt, question:** A traverse from behind, running right: five lettered holds above seven footholds. D faces left and the others face up.

**Alt, answer:** The same traverse with a climber crossing the left hand under the right arm, left hip to the wall.

---

### Problem 3: `reading-v3-overhang`

About V3. Overhanging 20°, seen from behind. Decision: is the big hold out to the side for a hand, a toe or a heel?

| Hold | x, y | Type | What it offers |
|---|---|---|---|
| A | 84, 168 | jug, `variant="bucket"`, size 1.4, `rubber=True`, no chalk | Right heel, then right sole. It is a jug and a hand can use it, as Next says, but its bowl gives a heel something to pull against. Big enough for its rubber marks to read. |
| B | -14, 172 | crimp, `variant="rail"`, size 1.4 | Start, both hands, with room for two as the head says. A thin rail, so a foot can't easily share it with a hand. Later the left foothold. |
| C | 4, 262 | crimp, `use=165, w=14, h=7, variant="rail"` | Faces left. With your hips to its right, a left-hand sidepull. |
| D | 60, 270 | sloper, `variant="rail"` | Right hand. You must hang under it. |
| E | 44, 322 | jug, `variant="bucket"` | Finish, both hands. Its chalk is the mark the prompt compares with A's rubber. |
| 1, 2 | -28, 30 and 28, 44 | foot, size 1.15 | Start feet. |
| 3, 4 | -14, 76 and -26, 120 | foot | Left foot. |

There is one start hold, because each earlier wall gave a route round the heel. A jug between the start and the edge let you match it and throw to the finish. Two start jugs let a right hand on A free one of them for the right foot. One wide jug still let the right foot share it with the right hand, so B is a thin rail. Section 10 has the routes that remain.

**Head:** `wall: [The wall overhangs 20°, seen from behind. B has room for two hands.]`, `start: [both hands on B.]`, `finish: [both hands on E.]`

**Prompts**
- *Step 3.* Which way does each hold face?
- *Step 4.* Give A, C and D an L or an R.
- *Step 5.* Compare the marks on A with those on E. What do they tell you? What kind of hold is D? Where must your body be to hold it? What could put it there?
- *Step 6.* Where is the crux?

**Moves**
+ Left foot on 1, right foot on 2. Left foot to 3, then 4.
+ Right heel into the bowl of A. Toes out, knee out. Both hands stay on.
+ Tighten your buttocks. Press the heel and pull it towards your bum. Stand up on your left foot at the same time. Your hips go in and up to the right. B is below your shoulder now and can only press, so don't stop. As your hips rise, left hand to C, a #tref("sidepull", body: [sidepull], show-page: false).
+ Right hand to D, a sloper. Hang under it. Keep pulling with the heel.
+ Left foot up to B, the old start hold. Keep the heel on.
+ Stand up on your left foot until your hips are higher than A. Then roll onto your whole foot on A. Right hand to E, leaving D as your hips rise.
+ Left hand to E.

**Crux:** Moves 3 to 5. You leave the start for a small edge and a sloper. Only the #tref("heel-hook", body: [heel], show-page: false) keeps your hips in. At move 5 both feet come high, so the sloper can roll off (judgement).

**Wrong:** You take A with your right hand: it is the biggest hold in reach. Then you stand on 4 and take your right foot off. D is now in reach. But your left hand and foot make a #jt("hinge") (the line you swing around) far left of D. You swing open as your right hand lets go. A #tref("back-flag", body: [back flag], show-page: false) stops the swing, but your hips stay far left. A sloper only holds with your body below it #src("C3", "C34"). A toe or #tref("toe-pull", body: [flat sole], show-page: false) on A can only drag on friction. Press hard and it shoves your hips left and out. A heel sits in A's bowl, so it has something to pull against and draws you in (judgement). Rubber marks and no chalk suggest a foothold #src("E30", "E31").

**Next:** If the heel won't go on with both hands on B, take A with your right hand first. Set the heel beside your hand and carry on from move 3. If the heel slips, change the foot's angle by a few degrees #src("A8") and keep your hips close #src("A9"). Warm up first #src("A11"). Turning the foot out hard on a heel close to your hip can tear a knee ligament #src("A10").

**Tall:** C and D are in reach from feet 4 and 3. The heel still keeps your hips in.

**Small:** Don't skip foot 4. From foot 3, D is out of reach even with the heel.

**Entries:** `("heel-hook", "sloper", "rockover")`

**Techniques and badges:** `heel-hook` V3, `sloper` V3, `rockover` V1, `sidepull` V1, `half-crimp` V2, `matching` V1, `straight-arms` V0, `toe-pull` V3. `back-flag` V3 is what costs more. `overhang` stays unlinked, as ruled.

**Question figure:** `Fig(-72, -8, 112, 338)`, 59 × 111 mm. Tape at (-30, 168) and (2, 168).
Tags: A (102, 170), B (12, 174), C (14, 263), D (78, 271), E (58, 324).
Numbers: 1 (-17, 31), 2 (38, 45), 3 (-4, 77), 4 (-16, 121).

**Answer figure:** same frame, showing move 4. `FootClimber((34, 176), lean=16, bend=8, lh=grip(C, use=165, kind="crimp"), rh=grip(D, kind="sloper"), lf={"at": stand(4), "angle": 196}, rf={"at": add(A, (-5, 4)), "angle": 14, "spot": "heel", "up": 1}, knees={"r": "up"}, leg_len={"r": (.85, .7)}, head=(2, 3), active=("+rham", "+lthigh"))`. `xray` on A, B, C, D and foot 4. The right elbow is at 156° with the right shoulder just past D. The left elbow is at 93°, and the line from hand to shoulder runs 33° off C's face, which reads as a sidepull.
Tags: `A heel` (84, 150), B (-50, 172) with a leader to (-28, 172), `C L1` (-14, 270), `D R2` (85, 271), `E R3 L4` (73, 324). Number 4 moves to (-36, 121).
`f.body_arrow([(14, 120), (42, 146)])`, under the right thigh, pointing up and right.

**Caption:** Move 4. The heel holds your hips in. The arrow shows where they went in move 3.

**Alt, question:** A 20-degree overhang from behind with lettered holds and four footholds; one big hold sits out to the right.

**Alt, answer:** The same overhang with a climber whose right heel hooks the big hold out to the side, the right hand high on a rounded hold.

---

### Problem 4: `reading-v4-steep`

About V4. Overhanging 35°, **seen from the side**. Decision: stay on the big low foothold, or step up to the thin high edge?

World points lie on the wall line: `at = wall_side(f, 170, 0, 338, angle=35)` gives `at(h) = (170 - 0.7 h, h)`.

| Hold | Height on the wall | x, y | Type | What it offers |
|---|---|---|---|---|
| A | 156 | 60.8, 156 | `hold_side("edge")` | Start, both hands: a thin edge with room for two. Later the high foothold for one foot, then both. |
| B | 200 | 30.0, 200 | `hold_side("jug")` | Right hand. Later a foothold. |
| C | 242 | 0.5, 242 | `hold_side("edge")` | Left hand, with room for one, as the head says. It holds you at the crux. A side view can't show that, and a match here would let you skip D. |
| D | 286 | -30.3, 286 | `hold_side("sloper_steep")`, a profile in `figs_reading.py` | Right hand. Hang low under it. The library's sloper turns with the wall, so its top would fall 53° from level and need friction of about 1.3 to rise on. This one falls 28° and needs about 0.6, and still has no lip. |
| E | 326 | -58.3, 326 | `hold_side("jug")` | Finish, both hands. |
| 1, 2 | 54 and 84 | 132.2, 54 and 111.2, 84 | foot | Start feet. |
| 3 | 116 | 88.8, 116 | foot, size 1.7 | The big foothold, wide enough for two feet. |
| 4 | 216 | 18.8, 216 | foot | Only small climbers need it, for the finish. |

**Head:** `wall: [The wall overhangs 35°, seen from the side. The lettered holds run in one line, about 50 cm apart along it. A has room for two hands and C for one. Foothold 3 is wide enough for two feet.]`, `start: [both hands on A.]`, `finish: [both hands on E.]`

**Prompts**
- *Step 2.* You can't tell left from right from here. What can you see that you couldn't see from behind?
- *Step 3.* Compare the profiles of B, D and E. Which one has no lip to hook? Where does that want your hips?
- *Step 5.* Which holds could take a foot?
- *Step 6.* Which hand moves need your full stretch? What do you stand on for them? What is each leg doing?

**Moves**
+ Left foot on 1, right foot on 2. Right hand to B. Hang on your straight right arm.
+ Right foot to 3, then left foot to 2.
+ Left hand to C.
+ Left foot to 3, beside your right. Right foot up to A, on its outside edge. Drive the toe in and pull. Keep your whole body tight and your hips in.
+ #jt("lock-off", body: [Lock off]) on C. Turn your right hip in and take D with your right hand. Use a small #tref("deadpoint", body: [deadpoint], show-page: false) (a catch at the top of your rise) if you need one. Square your hips once you hold it.
+ Left foot up to A beside your right. Right foot to B.
+ Deadpoint to E: rise with your right hand on D and let go as the rise slows. Then left hand to E.

**Crux:** Moves 5 to 7. C is a flat edge, which loses grip as you turn #src("B38"). Your toe is on a thin edge while your hand goes to the worst hold. Then both feet come up: D rolls and C drops to your waist. So go for E in one movement.

**Wrong:** You stay on the big foothold and reach for D. From feet 2 and 3, D is about 30 cm out of reach. From both feet on 3 you reach it only with both legs straight. Your feet tend to come off #src("E8") and you land on a sloper with no tension (judgement). With your left foot on 3, a higher right foot adds no reach. It keeps one leg bent to pull and drive with.

**Next:** If the toe pops, place it again and press it down and in #src("A6", "A38"). If your hand rolls off D, your hips swung out: pull them in. Both toes on A give about 45 cm more reach, but you catch D with your hips out and it rolls sooner #src("C2", "C3", "C11"). From both toes on A you could skip D, but nothing is above you as you rise to E (judgement).

**Tall:** You can reach D from both feet on 3, so A can wait until you hold D.

**Small:** Left foot to 3 before your left hand goes to C. From 3 and A you are 15 cm short of D, so put both toes on A or deadpoint off A. Finish: right foot to 4, left foot to B.

**Entries:** `("toe-pull", "body-tension", "sloper", "deadpoint")`

**Techniques and badges:** `toe-pull` V3, `body-tension` V3, `straight-arms` V0, `hip-turn` V2, `backstep` V3, `deadpoint` V3, `sloper` V3, `half-crimp` V2, `matching` V1. `overhang` stays unlinked, as ruled.

**Question figure:** `Fig(-100, -8, 180, 342)`, 90 × 112 mm. `ground(f, 0)`, then `wall_side` as above. No grid and no tape: the line under the head gives the start.
Holds with `hold_side(f, kind, at(h), angle=35, size=...)`. On both figures, tags and numbers sit on the hatched side of the wall, clear of the climber: tags at `add(at(h), (11 + w/2, 6))` with `w = f.mm(1.25 + 1.55 * len(s))`, and numbers at `add(at(h), (17, -3))`.

**Answer figure:** same frame. `Climber((2.1, 184), view="side", lean=-35, bend=0, lh=_side_grip(at(242), 35), rh=_side_grip(at(286), 35, out=4.5, up=2.0), lf={"at": _side_foot(at(116), 35), "contact": "toe"}, rf={"at": _side_foot(at(156), 35), "contact": "toe"}, arm_len={"l": .7}, leg_len={"r": (.35, .95)}, active=("+rham",))`. `xray` on A, C, D and foot 3, and not on B: the leg passes close to it, no limb is on it, and dashes under the shin would look like contact. The shorter thigh points at the viewer, which moves the knee off B and shows the bent leg working. Shin to B's lip is 8 cm, so B shows whole with its cup.
Distances from the wall line: hips and head 32 cm, shoulders 34, left knee 15, right knee 16, elbows 15 to 18. Tags: A, `B R1`, `C L2`, `D R3`, `E R4 L5`. `f.body_arrow([(-44, 180), (-12, 186)])`, to the left of the hips, pointing in towards the wall.

**Caption:** Move 5. Hips in and low under D, on a straight right arm. Left and right could swap. A side view hides the hip turn.

**Alt, question:** A 35-degree overhang from the side with five lettered holds and four footholds (one of them large).

**Alt, answer:** The same wall with a climber holding the hips in: toes on the large foothold and a thin edge, right hand on a rounded hold.

---

### Problem 5: `reading-v4-sit`

About V4. A sit start, overhanging 15°, seen from behind. Decision: hand or foot first off the mat? Your size decides.

| Hold | x, y | Type | What it offers |
|---|---|---|---|
| A, B | -25, 114 and 23, 118 | crimp, `variant="rail"` | Start edges: left hand and right hand. A later takes the left foot. |
| C | 38, 194 | crimp, size 1.2 | Right hand, the first target. |
| D | -26, 236 | crimp | Left hand. |
| E | 28, 262 | sloper | Right hand. |
| F | 0, 306 | jug, `variant="bucket"` | Finish, both hands. |
| 1, 2 | -64, 8 and 24, 12 | foot | Start feet, stated in the head, almost on the mat. |
| 3, 4 | 58, 44 and -22, 62 | foot | The feet go here first. 4 sits about 45 cm above the hips while you are folded up. |
| 5, 6 | 44, 98 and 58, 146 | foot | Right foot. 6 sits clear of the drawn climber's arm. |

**Head:** `wall: [The wall overhangs 15°, seen from behind.]`, `start: [sitting on the mat with your left hand on A, your right hand on B and your feet on 1 and 2.]`, `finish: [both hands on F.]`

**Prompts**
- *Step 1.* What do you need to check with your gym before you move off a sit start?
- *Step 4.* Give C, D and E an L or an R.
- *Step 5.* What can your hips do as your bottom lifts? What does each foot do?
- *Step 5, your size.* Work out how many bolt holes your reach covers (toes to fingers, at 20 cm a hole). Take off one: feet 1 and 2 are too far apart to stand up straight. Then count the holes from foothold 2 to C. Can you reach it before your feet move? If not, or only just, which footholds would help? How high are they compared with your hips?
- *Step 6.* Where will you need the most power?

**Moves**
+ Left foot on 1, right foot on 2. Sit close to the wall and hang from A and B.
+ Left foot to 4, about 45 cm above your hips. Rock back a little, then pull your bottom off the mat in one movement #src("E11"). As it lifts, turn your right hip to the wall and roll onto the right foot's outside edge.
+ Right foot to 3, on its big-toe edge. Your hips come square so this foot can push. Rise between 3 and 4. Right hand to C as a small #tref("deadpoint", body: [deadpoint], show-page: false) (a catch at the top of your rise). By then A is at your waist and can only press.
+ Press on A and rise until your hips clear 5. Right foot to 5: D comes well within reach.
+ Left hand to D. Left foot up to A. Right hand to E. You could skip E from foot 6, but C drops below your shoulder as you stand. E stays above it.
+ Right foot to 6. Stand up and catch F with your right hand. Then left hand to F.

**Crux:** Moves 2 and 3. You pull off the mat on two flat edges. A flat edge loses grip as you turn #src("B38"). At the catch A is at your waist, so your hand must arrive at the top of your rise.

**Wrong:** You pull straight for C from feet 1 and 2. You can touch it, but only at full stretch with your left leg long. Your left hand is locked at your chest on a thin edge, with no rise left to help it (judgement). Feet 4 and 3 give you about 30 cm to spare. But set both of them before you lift and you fold up square with your bottom away from the wall. The first pull is then all arms #src("E11").

**Next:** Roll your right knee onto the mat and push off it #src("E11"). Don't bounce off the mat if your gym wants a still start (judgement).

**Tall:** Hand first works: C is in reach from feet 1 and 2, so long legs can skip the high step. Bring your left foot to 4 once your hand is on C. Foot first still works: see the one high foot in @fig-cons-sit c, under @cons-tall.

**Small:** A and B are a full stretch from the mat, so you can't rock back. C is out of reach from feet 1 and 2, so you must step up first. Finish with a small deadpoint to F. Your left foot comes off A, so press it on the wall and match (judgement).

**Entries:** `("sit-start", "hip-turn", "edging", "deadpoint")`

**Techniques and badges:** `sit-start` V3, `hip-turn` V2, `edging` V0, `half-crimp` V2, `sloper` V3, `weight-shift` V0, `matching` V1, `deadpoint` V3.

**Bolt-hole count, for the editors.** Foot 2 to C is 182 cm, or 9.1 holes. Take one hole off the reach, as the prompt says, and the count agrees with section 10: ordinary 9.5, tall 10.4, small 8.5 holes. That needs the ten and a half holes in the opening.

**Question figure:** `Fig(-110, -8, 90, 326)`, 64 × 107 mm. Tape at (-38, 110) and (10, 116).
Tags: A (-12, 115), B (37, 119), C (52, 196), D (-14, 237), E (43, 264), F (14, 308).
Numbers: 1 (-55, 9), 2 (33, 13), 3 (68, 45), 4 (-13, 63), 5 (53, 99), 6 (68, 147).

**Answer figure:** same frame, showing the catch of move 3. `Climber((24, 106), turn=.2, lean=6, lh=grip(A, kind="crimp"), rh=grip(C, kind="crimp"), lf=stand(4), rf=stand(3), knees={"l": "left", "r": "out"}, head=(2, 3), leg_len={"l": (1.0, .65)}, active=("rfore", "rupper", "lthigh", "rthigh"), order=["rleg", "rarm", "torso", "larm", "lleg"])`. The leg goes over the arm because the hand is on the wall and the thigh is off it. The left shin is foreshortened because the knee comes off an overhanging wall, so the knee drops to (-27, 93) and the whole hand on A shows. The dots are on the right arm and both thighs, since A can only press. Knees 63° and 70°, right elbow 89°, and A is 41 cm below the left shoulder and 8 cm above the pelvis. `xray` on A, B, C and feet 3, 4, 5 and 6. Tape at (-38, 110) and (10, 116), so the thigh covers the second and the first stands clear.
Tags: A (-58, 130) with a leader to (-34, 119), B (58, 130) with a leader to (44, 123), `C R1` (59, 196), `D L2` (-6, 237), `E R3` (50, 264), `F R4 L5` (29, 308). Numbers 1 (-73, 9), 2 (14, 13), 3 (68, 45), 4 (-36, 54), 6 (68, 147), and 5 from (32, 78) with a leader to (41, 94).
Dashed arrows for the feet, numbered as the moves: `f.arrow([(-60, 16), (-78, 36), (-68, 58), (-44, 66)])` with `f.step(2, (-92, 38))`, and `f.arrow([(32, 18), (40, 30), (50, 40)])` with `f.step(3, (52, 22))`.

**Caption:** Move 3. The feet went first: the discs are moves 2 and 3. The right hand reaches C.

**Alt, question:** A sit start from behind: lettered holds above and six footholds (two almost on the mat).

**Alt, answer:** The same problem with a climber off the mat: left foot high on one side, right foot lower on the other, right hand high.

---

### Problem 6: `reading-v5-gap`

About V5. Overhanging 25°, seen from behind. Decision: static, deadpoint or dyno?

| Hold | x, y | Type | What it offers |
|---|---|---|---|
| A, B | -24, 150 and 18, 156 | jug | Start, left and right hand. Later footholds. |
| C | -26, 206 | crimp, `variant="rail"`, size 1.4 | Both hands, one after the other, so the left hand takes its left end. A long edge you can push down on and lock off. |
| D | -30, 262 | crimp | Left hand, with room for one. High enough for that arm to hang straight before the throw. |
| E | 24, 300 | crimp, `variant="curved"` | Right hand. Small, room for one hand. |
| F | -2, 332 | jug, `variant="bucket"` | Finish, both hands. |
| 1, 2 | 24, 26 and -30, 30 | foot, size 1.15 | Start feet. |
| 3, 4 | -32, 66 and 26, 74 | foot, size 1.5 | Big, low and centred: they look like a launch pad. |
| 5, 6 | -46, 100 and 32, 108 | foot | Ordinary. 6 sits under E. |

**Head:** `wall: [The wall overhangs 25°, seen from behind.]`, `start: [left hand on A, right hand on B.]`, `finish: [both hands on F.]`

**Prompts**
- *Step 3.* Which holds could stop a moving body? How many hands fit on E?
- *Step 4.* Give C, D, E and F an L, an R or both.
- *Step 5.* Which footholds are biggest? Count the holes to E from each one. Which let you reach it?
- *Step 6.* Static, #jt("deadpoint") (a catch at the top of your rise, feet on) or #jt("dyno") (a jump, feet off)? What would change your answer?
- *Step 7.* What is the setter testing?

**Moves**
+ Right foot on 1, left on 2. Left foot to 3, right foot to 4.
+ Left hand to the left end of C.
+ Right foot to 6 under E, on the #tref("edging", body: [inside edge], show-page: false) of your shoe. Left foot to 5.
+ Right hand up to C, beside your left. From B it can't hold you in while your left hand moves (judgement).
+ Lock off on C with your right arm and take your left hand up to D. Your left arm can hang straight there. At the catch of E, D is above your shoulder. C would be below.
+ Let your hips sag out on that straight arm #src("D10"). Drive through your right leg in one movement, hips in and up #src("D13"). Send your right hand from C to 2–3 cm above E #src("D16"). Close it in a #tref("half-crimp", body: [half crimp], show-page: false) at the top: a full crimp at speed risks your fingers #src("C25"). Then push down through your right foot #src("D21").
+ Left foot up to A. Right foot up to B and stand.
+ Left hand to F, then right hand to F.

**Crux:** Move 6. The setter is testing whether you choose a #tref("deadpoint", body: [deadpoint], show-page: false). E takes one hand and has a foothold under it, so you want a foot on as you catch it. A slow #jt("lock-off") may just reach E. But it keeps you on one bent arm on D for the whole reach #src("D13"). Stepping a foot up to A or B shortens the rise, but it folds you up with your hips out (judgement). With both feet on A and B you can skip E for F. But D is then no higher than your shoulder as you throw, so nothing holds you in (judgement). A dyno would suit a jug at E with no foot 6.

**Wrong:** It looks like a #tref("dyno", body: [dyno], show-page: false): no hold above B on that side until E, and two big footholds low down. So with your left hand on C you stand on 3 and 4, sink and jump. That is about twice the rise. Even if you stick E, your feet are off. Small edges must then stop the swing, which may pull you off (judgement).

**Next:** If you fall short, drive your hips in and up #src("D10", "D17"). Or use your outside edge on 6 for a #jt("hip pop", body: [hip~pop]) #src("D7", "D10"). If your fingers touch and slide, send your hand sooner.

**Tall:** E is well within reach from feet 5 and 6, so your deadpoint can be small.

**Small:** E is out of reach from 5 and 6. From A and 6 you are still short. Step both feet up to A and B #src("H2", "H3"): your hips fold out, but E is in reach (judgement).

**Entries:** `("deadpoint", "dyno", "latching")`

**Techniques and badges:** `deadpoint` V3 with its hip pop, `latching` V4, `half-crimp` V2, `straight-arms` V0, `edging` V0, `matching` V1, `lock-off` V3 (move 5, and the slow option). `dyno` V4 is what fails.

**Question figure:** `Fig(-78, -8, 72, 344)`, 48 × 113 mm. Tape at (-34, 146) and (8, 152).
Tags: A (-10, 152), B (32, 158), C (-11, 207), D (-16, 263), E (36, 301), F (12, 332).
Numbers: 1 (34, 27), 2 (-20, 31), 3 (-21, 67), 4 (39, 75), 5 (-37, 101), 6 (42, 109).

**Answer figure:** same frame, with no ghost. `Climber((14, 186), lean=-16, lh=grip(D, kind="crimp"), rh=grip(E, kind="crimp"), lf=stand(5), rf=stand(6), active=("rthigh",))`. The left elbow opens to 76° and the right arm is straight. `xray` on A, D, E and feet 5 and 6, because the knee covers A and move 7 stands on it. `f.body_arrow([(60, 176), (60, 216)])`, in the free space above the right thigh.
Tags: A (-6, 128) with a leader to (-17, 149), B (17, 137), `C L1 R2` (-57, 207), `D L3` (-53, 263), `E R4` (3, 301), `F L5 R6` (27, 332). Number 5 moves to (-55, 101).

**Caption:** Move 6. The top of the deadpoint.

**Alt, question:** A 25-degree overhang from behind with a long gap below a small high edge and footholds at three heights.

**Alt, answer:** The same wall with a climber at the top of a deadpoint, both feet on, the right hand catching the small edge.

---

### Problem 7: `reading-v5-volumes`

About V5. Overhanging 25°, seen from behind. Decision: pull down, or squeeze?

| Hold | Position | Type | What it offers |
|---|---|---|---|
| X | `[(-34,66), (0,104), (34,66), (0,50)]`, apex (0, 70) | `volume()` | The lower volume. Toes press its upper faces at about (∓22, 79). |
| Y | `[(-30,176), (-24,238), (24,238), (30,176), (20,148), (-20,148)]`, apex (0, 200) | `volume()` | The upper volume, about 45 cm deep as the head says. Palm spots (∓25, 198). The faces lie 59° off the wall plane. The test is load, not slope: with friction cones on the drawn pose, each palm must press sideways with about 1 body weight at skin friction of 1, 0.7 at 1.2, 0.5 at 1.5 and 0.4 at 2. The earlier Y, 92 cm wide at the waist, needed 5.2, 1.6, 0.9 and 0.6. A wider or shallower Y needs more, so don't widen it. These are a model's figures and judgement. |
| A | 0, 120 | jug, `variant="flat"` | Start, both hands, between the volumes. Later the left foothold that makes B reachable, and the nearest one to X. |
| B | 10, 312 | jug, `variant="bucket"` | Finish, both hands. Nearly 12 holes from your toes on X and just under ten from A, against a reach of about ten and a half. |
| 1, 2 | 34, 24 and -36, 28 | foot, size 1.15 | Start feet. |
| 3, 4 | -46, 146 and 46, 150 | foot | 4 takes the right foot. 3 is the mirror order's left foot and the small climber's. With both hands on A, your hips can't rise over them. |

**Head:** `wall: [The wall overhangs 25°, seen from behind. Y stands about 45 cm off the wall. Neither volume has an edge to grip.]`, `start: [both hands on A.]`, `finish: [both hands on B.]`

**Prompts**
- *Step 3.* Which way do the faces of Y point?
- *Step 4.* Where can each hand go after A? Does the order matter?
- *Step 5.* Count the holes from your toes on X to B. What must you stand on to reach it?
- *Step 6.* Where is the crux? How long does it last?

**Moves**
+ Right foot on 1, left foot on 2. Left foot onto the left upper face of X, right foot onto the right. Squeeze X between your feet.
+ Rise on X only until your left hand reaches the left face of Y: palm flat, elbow down. Your hips are still below A, so your right hand can still pull. Before they pass A, right hand to the right face, palm flat. Until it lands, nothing holds you in.
+ Stand a little taller on your right foot, so your left knee has room. Left foot up to A, the old start hold. It is the nearest foothold, so your foot is off for the least time. Move it fast.
+ Right foot to 4. Move your hips right round Y. Drive off both feet in one movement. Take B with your right hand as a #tref("deadpoint", body: [deadpoint], show-page: false). It is nearly 12 holes from your toes on X and under ten from A. Your left palm only steers.
+ Left hand to B.

**Crux:** Moves 2 to 4, from the moment your right hand leaves A until it catches B. This is #tref("compression", body: [compression], show-page: false). On X your feet can only push you out, so only the squeeze holds you in. Once your right hand leaves Y, nothing does. So don't pause.

**Wrong:** You stand up on X and reach for the top of Y with one hand, the other still on A. To reach it your hips must pass A, so you can only press down on A. On an overhang a press can't hold you in, so you fall away from the wall (judgement). Feet 3 and 4 don't save it: with your hands on A, your hips can't rise over them. Y's side faces point sideways and out, so pulling down on them only slides your hands off. A #tref("knee-bar", body: [knee bar], show-page: false) under Y won't hold either: the underside slopes out, so your knee slides off (judgement). When a volume has no edge, squeeze it instead of pulling down.

**Next:** Squeeze from your chest and back as in a hug. Keep your hips close and trunk tight #src("B31"). If a foot pops, press your free foot on a foothold or the wall #src("B45"). Left or right first doesn't matter: the mirror image also works. A foot on A before your second hand does: it is easier on the palms. So if the squeeze won't last, take Y with your right hand first, hips low and well left of A. Left foot to A, then left hand to Y. Chalk your whole hand #src("E18").

**Small:** B is out of reach with both feet on. Let your left foot leave A as you drive.

**Entries:** `("compression", "volume", "palming", "body-tension")`

**Techniques and badges:** `compression` V4, `volume` V2, `palming` V2, `body-tension` V3, `smearing` V1, `matching` V1, `deadpoint` V3.

**Question figure:** `Fig(-92, -8, 92, 324)`, 59 × 106 mm. Tape at (-14, 116) and (14, 116). `volume(f, Y, apex=(0, 200))` and `volume(f, X, apex=(0, 70))`.
Tags: A (15, 123), B (24, 314), X (46, 70), Y (44, 214).
Numbers: 1 (44, 25), 2 (-26, 29), 3 (-58, 147), 4 (58, 151).

**Answer figure:** same frame, showing the start of move 3. The pose is the one in `compression()` in `figs_body.py`, on the narrower Y: `e = norm(sub((-34, 66), (0, 104)))`, `down = math.degrees(math.atan2(e[1], e[0]))`, `p = (-17.6, 75.3)`, on the upper face and inside X's outline, then `Climber((0, 130), lh=(-25, 198), rh=(25, 198), lf={"at": p, "angle": down, "contact": "ball"}, rf={"at": (-p[0], p[1]), "angle": 180 - down, "contact": "ball"}, knees={"l": "out", "r": "out"}, elbows={"l": "down", "r": "down"}, arm_len={"l": (.6, .9), "r": (.6, .9)}, hand_style={"l": "open", "r": "open"}, active=("+llat", "+rlat"))`. The shoulders stand well off the wall and the palms close to it, so the arms point partly at the viewer. `xray` on A. Four inward `kind="force"` arrows: `[(s*58, 196), (s*38, 196)]` and `[(s*50, 93.5), (s*34, 81.5)]` for `s` of -1 and 1.
Tags: `B R3 L4` (39, 314), `Y L1` (-58, 176), `Y R2` (58, 176), X (46, 62). `f.text("A", (-23, 113), size=6.8, weight=500)`, in the gap under the left thigh. Numbers as on the question.

**Caption:** Start of move 3. The palms press in with the elbows down. The feet squeeze X.

**Alt, question:** A 25-degree overhang from behind with two big volumes one above the other, a start hold between them and a finish hold above.

**Alt, answer:** The same wall with a climber squeezing the upper volume's sides with the palms and the lower volume with the feet.

---

### Problem 8: `reading-v6-cave`

About V6. Overhanging 40°, seen from behind. Decision: when you swing open, back flag or toe hook?

| Hold | x, y | Type | What it offers |
|---|---|---|---|
| A | -84, 138 | jug, `use=180`, size 1.2, `rubber=True`, no chalk | Far left at hip height, its lip facing away from you. Left toes hook behind it. |
| B | -40, 150 | crimp, `variant="rail"`, size 1.3 | Start, left hand. Low enough that the right hand can't reach E while the left stays on it (except at full stretch for the tall climber). Later a foothold. |
| C | 32, 196 | crimp, `use=45, w=11, h=6` | Start, right hand, with room for one, as the head says. Faces up and right, so it can take the pull down and left that the hook and D put on you. A match here would skip A and D. |
| D | -44, 246 | jug, `use=135`, size 0.8, `variant="flat"` | Left hand. Faces up and left, so it holds at the catch, with your shoulder well below it, and as a sidepull later on. |
| E | 14, 300 | crimp | Right hand. |
| F | -16, 322 | jug, `variant="bucket"` | Finish, both hands. |
| 1, 2 | 2, 30 and 26, 54 | foot, size 1.15 | Start feet. All the footholds sit right of the middle. |
| 3, 4 | 46, 104 and 48, 148 | foot | Right foot. They sit clear of the hinge line. Foot 3 is also where a left foot would backstep. |

**Head:** `wall: [The wall overhangs 40°, seen from behind. C has room for one hand.]`, `start: [left hand on B, right hand on C.]`, `finish: [both hands on F.]`

**Prompts**
- *Step 3.* Which way does each hold face?
- *Step 4.* Give each hold above the start an L or an R.
- *Step 5.* Look where the footholds sit. Which start hand can't let go without your body swinging? What could stop the swing?
- *Step 6.* Where is the crux?

**Moves**
+ Left foot on 1, right foot on 2. Rise on your right foot. A faces left: hook the top of your left toes behind it. Bend the ankle up towards your shin and keep the leg nearly straight. Hold it with leg tension and don't curl your toes #src("A13").
+ Keep both hands on. Right foot up to 3.
+ Press up on your right foot until the hook leg goes tight. Keep your right arm straight at first and lock it as your shoulders reach C. Left hand to D with a small deadpoint.
+ Your left hand and right foot now oppose each other, so take the hook off in small steps #src("A12"). Left foot to B, then right foot to 4.
+ Right hand to E. You may skip it with a deadpoint to F.
+ Right hand to F, then left hand to F.

**Crux:** Move 3. When your left hand lets go of B, your right hand and right foot hold you on one side. You swing open like a door unless something stops it. C faces up and right, so it takes the hook's pull. D faces up and left, so it holds as you catch it.

**Wrong:** Your right hand and foot call for a #tref("back-flag", body: [back flag], show-page: false), so you try one. A flag wants your hips over your right foot #src("B26"). To reach D from there, C must come down to your chest. There it can only press, so it can't hold you in (judgement). Stay low with your hips towards D and the door opens. A #tref("toe-hook", body: [toe hook], show-page: false) on the left holds you in with C at your shoulder #src("A15"). With all the footholds on one side, try a backstep or a hook on the other.

**Next:** If the toe creeps out, pull it and your right hand towards each other #src("A13"). A heel behind A also holds you in and brings D closer, but your hips sit further from the hinge (judgement). A #tref("backstep", body: [backstep], show-page: false) with your left foot on 3 and your right leg out also works. It costs a little more lock and puts your outside edge on a small foothold #src("B44"). A fast throw from feet 2 and 3 can beat the door #src("B62"), but you land on D at full stretch and swinging.

**Tall:** Your longer lever makes the hook harder to hold (judgement). Try the backstep.

**Small:** From the hook, D is out of reach. Use a bigger deadpoint or the backstep.

**Entries:** `("toe-hook", "barn-door", "back-flag", "backstep")`

**Techniques and badges:** `toe-hook` V4, `barn-door` V1, `body-tension` V3, `lock-off` V3, `sidepull` V1, `deadpoint` V3, `half-crimp` V2, `matching` V1. `back-flag` V3 is the fallback, and `backstep` V3 and `heel-hook` V3 are fair rivals.

**Question figure:** `Fig(-112, -8, 70, 336)`, 58 × 110 mm. Tape at (-50, 148) and (44, 188), so the thigh covers the first in the answer.
Tags: A (-73, 142), B (-26, 151), C (46, 197), D (-31, 250), E (26, 301), F (-2, 324).
Numbers: 1 (12, 31), 2 (36, 55), 3 (56, 105), 4 (58, 149).

**Answer figure:** same frame, showing move 3. `FootClimber((0, 150), lean=-12, bend=-6, lh=grip(D, use=135, size=.8), rh=grip(C, use=45, kind="crimp", size=1.3), lf={"at": add(A, (-7.2, -1)), "angle": 88, "spot": "toptoe", "up": -1}, rf=stand(3), knees={"l": "up", "r": "out"}, elbows={"r": "down"}, head=(-3, 3), leg_len={"l": .96}, active=("+lshin", "+rthigh"))`. `xray` on A, B, C, D and feet 3 and 4. The hook leg's length of 96% is the depth of hips about 26 cm off the wall, so the knee reads as nearly straight (about 170°).
`_hinge(f, grip(C, use=45, kind="crimp", size=1.3), stand(3))` for the dashed line from the right hand to the right foot.
Tags: `A toe` (-84, 156), B (-42, 166) on the free wall above it with no leader, so nothing crosses the thigh, C (46, 197), `D L1` (-24, 250), `E R2` (34, 301), `F R3 L4` (13, 324). Number 4 at (64, 170) with a leader to (50, 151).

**Caption:** Move 3. The toe hook holds you in. The dashed line is the #jt("hinge").

**Open judgement.** The hook carries a lot, and it may not be the best answer. At the drawn pose the centre of gravity is about 45 cm off the hinge, the hook about 130 cm, and the leg runs only about 17° off the wall. A rough estimate of the leg's tension is three-quarters of body weight, with C taking about 1.1 body weights nearly sideways on one crimp in a locked arm. That can't hold, so the hook only has to last for the catch, the toes also take some of the load by friction, and the deadpoint in move 3 isn't optional. With leg tension of about 0.3 of body weight, C takes about 0.7. A heel on A is at least as good on most measures: D has 19, 13 and 26 cm to spare from it (ordinary, small, tall), against 3.5 to spare, 5 short and 1 short from the toe, for 5 to 8 cm more off the hinge. The heel entry says heels suit holds out to the side. Moving A out to x=-112 or turning it to `use=225` doesn't close the heel: the first takes the centre of gravity 64 cm off the hinge, and the second folds the ankle to 30 to 48°. A thinner A is untested. So the page concedes the heel and the backstep, and the toe stays as the shown beta because this is the set's toe-hook problem. That choice is Simon's.

**Alt, question:** A 40-degree overhang from behind: the footholds all sit right of the middle and one big hold sits far out to the left.

**Alt, answer:** The same wall with a climber: left toes hooked behind the far left hold, right foot pushing, left hand on a high hold facing up and left.

## 10. Reach figures, for the editors and not for print

The gap to the target in cm at the best clean pose. **+** means short by that much, and **−** means that much to
spare. Ordinary is the drawn climber, about 1.75 m. Tall and small are `scale=1.09` and `0.91`, about 1.90 m and 1.60 m. "Room" means the arm can bend, so the gap says nothing more.

| Problem | Target and stance | Ordinary | Tall | Small |
|---|---|---|---|---|
| 2 | D, crossing, from feet 4 and 5 | −44 | −63 | −22 |
| 2 | E, from feet 4 and 5, left hand on D, left foot pivoted | −28 | −46 | −7 |
| 2 | E, from feet 4 and 5, left hand on D, toes still right | −10 | −28 | +8 |
| 2 | E, from feet 5 and 6, left hand on C | −19 | −43 | +15 |
| 3 | D, from feet 3 and 2, left hand on C | +21 | +2 | +40 |
| 3 | D, from feet 4 and 3, left hand on C | +5 | −14 | +23 |
| 3 | D, from foot 4 with the right foot free, left hand on C | −48 | −68 | −29 |
| 3 | D, from foot 4 with the right foot free, left hand on B | −32 | −46 | −17 |
| 3 | D, from foot 3 and the heel, left hand on C | −13 | −31 | +18 |
| 3 | D, from foot 4 and the heel, left hand on C | −48 | −68 | −29 |
| 3 | C, from foot 4 and the heel, right hand on B | −50 | −63 | −33 |
| 3 | C, from feet 4 and 3, right hand on B | −28 | −49 | −11 |
| 3 | C, from feet 4 and 3, right hand on A | −28 | −49 | −8 |
| 3 | D, from foot 4 and a right foot on B, left hand on C | −48 | −68 | −29 |
| 3 | E, from B and the sole on A, left hand on C | −59 | −70 | −38 |
| 3 | E, from foot 4 and the sole on A, left hand on C | −6 | −25 | +13 |
| 4 | D, from feet 2 and 3 | +33 | +14 | +52 |
| 4 | D, from both feet on 3 | −7 | −25 | +14 |
| 4 | D, from 3 and A | −7 | −25 | +14 |
| 4 | D, from both toes on A | −53 | −65 | −34 |
| 4 | E, from A and B, or both toes on A, or A and 4 | −7 | −25 | +14 |
| 4 | E, from B and 4 | −27 | −39 | −15 |
| 5 | C, from feet 1 and 2 | −11 | −31 | +9 |
| 5 | C, from feet 1 and 3 | −11 | −32 | +9 |
| 5 | C, from feet 4 and 2 | −26 | −45 | −8 |
| 5 | C, from feet 2 and 3 | −32 | −47 | −10 |
| 5 | C, from feet 4 and 3 | −44 | −55 | −34 |
| 5 | D, from feet 4 and 3 | −12 | −30 | +7 |
| 5 | D, from feet 4 and 5 | −36 | −54 | −18 |
| 5 | F, from A and 6 | −20 | −39 | +3 |
| 6 | E, from feet 3 and 4 | +19 | 0 | no pose |
| 6 | E, from feet 5 and 6 | −9 | −28 | +10 |
| 6 | E, from A and 6 | −18 | −35 | 0 |
| 6 | E, from 5 and B | −5 | −28 | +13 |
| 6 | E, from A and B | −64 | −70 | −47 |
| 6 | F, from A and B | −35 | −53 | −16 |
| 7 | B, from toes on X, back view | +23 | +3 | +46 |
| 7 | B, from A and a toe on X, back view | +23 | +4 | +43 |
| 7 | B, from A and 4, back view | −26 | −46 | −7 |
| 7 | B, from A and 4, in 3D | −17 | −36 | +3 |
| 7 | B, from feet 3 and 4, in 3D | −25 | −40 | −8 |
| 7 | B, from high on X, in 3D | +22 | +5 | +40 |
| 8 | D, from the hook and foot 3, leg 85 of 89 cm, in the plane | −7 | −3 | +2 |
| 8 | D, the same, with the shoulders 20 cm off the wall | −3.5 | +0.6 | +4.8 |
| 8 | D, from a heel on A and foot 3, with the shoulders off the wall | −19 | −26 | −13 |
| 8 | D, from a left foot on 3 and the right leg out, the shoulder within 5 cm of C's height | −12.5 | −22 | −2.4 |
| 8 | D, from feet 2 and 3 with no hook | +6 | −14 | +25 |
| 8 | D, from a flag and foot 3, with the hips free to drift | −54 | −70 | −34 |
| 8 | D, from a left foot on 3 and a right foot on 4 | −48 | −67 | −29 |
| 8 | E, from B and 3, left hand on D | −16 | −34 | +3 |
| 8 | F, from B and 4, left hand on D | −26 | −37 | −9 |
| 8 | E, left hand on B, from a flag and foot 3 | +9 | −2 | +23 |

**Problem 8 turns on lock, not reach.** To catch D, how far must your right shoulder rise above C, and how far is your centre of gravity off the hinge? From the hook, the shoulder stays level with C, with the centre of gravity about 42 cm off. From a flag with the centre of gravity within 25 cm, the shoulder rises about 10 cm, and within 15 cm about 18 cm, with the elbow no deeper than the hook's. A left foot on 3 with the right leg out reaches D with the shoulder within 5 cm of C's height and the centre of gravity about 36 cm off. So the flag costs height at C and not a deeper elbow, which is what the wrong try now says. The backstep is at least as good on lock and reach. Its costs are a turned edge on foothold 3, which is small, and more lock if you keep your hips close.

The size notes in section 9 rest on these. These were also checked:
- Problem 4's figures already hold the body off the wall (section 7), so they include the cost of its depth. At the small size, C is 2 cm short from feet 2 and 3 and within reach from both feet on 3, which is why the note brings the left foot up first. Both toes on A hold C and D at the small size, and feet 4 and B reach E. The route that skips D is both toes on A, at the ordinary and tall sizes. Foot 4 adds no reach to it: E from A and 4 is the same as from both toes on A, and with the left foot on 3 the hips stop about 45 cm short. Nothing is above you as you rise to E on that route. In the beta D stays above the shoulder through the rise, by 58 cm down to 10 cm, and that is why move 7 keeps the right hand on D until the top. On a model with a 110 N·m shoulder, C alone stops balancing you at hips 265 to 285 cm along the wall, 10 to 30 cm before the catch.
- Problem 5's small climber can't match on F from A and 6. With the left foot free and pressed on the wall and the right foot on 6, the match has clean poses at every size. The old note stepped the left foot from A to C, 102 cm, which passes `warn()` only because the legs don't cross in projection. With feet on the mat, the same climber's hands are a full stretch from A and B: both reach only with the hips about 2 cm off the mat, before the wall's lean. Foot 4 isn't strictly needed: left foot on 1 and right foot on 3 reaches C at the ordinary and tall sizes, with less rise to spare. It is still feet first, so the opening's "Your beta may be as good" covers it. The head fixes the left foot on 1 for the start, though it takes no weight there.
- Problem 5's wrong try isn't straight-legged at the low end: at the lowest clean pelvis, y=82, the right knee is about 91°. It is at its limit because the arm is at full stretch and the left hand is locked at the chest, with A 9 to 35 cm below the left shoulder and the elbow at 35° to 78°. The drawn catch from feet 4 and 3 is clean from pelvis y=84 and has A at the waist.
- Problem 6's finish: with the left hand on D and the right hand going to F, D is 37 cm below to 4 cm above the left shoulder at the ordinary size, -25 to -3 small and -51 to +13 tall. With the right hand on E and the left hand going to F, E is up to 44, 37 and 49 cm above the right shoulder. So the lower hand moves first.
- Problem 2's small climber can't hold C from feet 5 and 6, so the moves let go of C from feet 4 and 5.
- Problem 7: the left palm lands with the pelvis as low as y=90 (ordinary), 104 (small) or 88 (tall), and A is at y=120. The top of Y needs a pelvis of at least y=120, 130 or 116. Back-view margins flatter this problem, because the legs and spine must clear Y, so the 3D rows are the ones to trust.
- Problem 7's statics, with friction cones and point contacts. These are a model's figures and judgement. In the printed order, the right hand travels with nothing holding you in (left palm and two toes: no solution in any pose). The left foot then travels on two palms and a smear, at about 1.07 body weights sideways per palm at skin friction of 1 (0.8 at 1.2, 0.6 at 1.5). With the right palm first and hips below A, the left foot travels with the left hand on A at about 0.35 to 0.45 per palm at friction 1.2, with the hips at x -31 to -40 and y 111 to 117. The earlier 0.15 holds only with hips above A and a hand that still pulls, so the page says hips low and well left of A. The left hand travels on the right palm, A and the right toe at about 0.15, if the toe on A can pull (foot friction of at least 1). Moving the right foot then still needs both palms, at about 1.0 (0.7 at 1.2). So the lesson survives either way, and the heavy squeeze lasts one foot move instead of three. The first palm should be opposite the foot going to A. The old fallback, with the left palm first and hips left of A, has no solution while low: the left palm pushes left and can't pull you back. It solves only at pelvis y 142 to 148, x -4 to 2.
- Problem 7's second palm. Move 2 now sends the right hand before the hips pass A at y=120. Both palms with toes on X have clean poses at pelvis y 112 to 116 at all three sizes if the legs are foreshortened, and in the model the palms cost less low down: 0.33 per palm at y=108, 0.40 at 118 and 0.49 at 130 at friction 1.2. The drawn pelvis is at y=130, above A, so the caption calls it the start of move 3. The mirror order is about equal to the printed one, and only B at x=10 and the feet differ: hand on A and other palm on Y 340 poses each way at the ordinary size, and the reach to B in 3D within 4 cm. The palm spots at (∓25, 198) sit 2.9 cm inside Y's outline, so a hand overhangs the rim by about 1.6 cm. (∓20, 198) with arrows `[(s*53, 196), (s*33, 196)]` is clean at the ordinary and small sizes, but the figure stays for now.
- Problem 7's small climber is 3 cm short of B from A and 4 in 3D, and has about 18 cm to spare from foot 4 with the left foot free, hips round Y as in move 4. Both hands on B have no clean pose on A and 4 at this size but have on 3 and 4, so the left foot can go to 3 once the right hand holds the jug. The page has no line to say so.
- Problem 7's tall climber is about 5 cm short of B from high on X in 3D. That is a throw off a smear with one palm on, so it gets no note.
- Problem 8: the left hand can stay on B with the hips over foot 3 (up to about x=38 at y=170) if you lean left, so a flag can reach D. The answer calls the flag worse and doesn't call it impossible. Turning C to face up and right loads it more with the hook: about 0.7 body weight at a leg tension of 0.3, and 1.1 at 0.76, against 0.3 to 0.4 for a backstep with the hips over the heel. So the old case against the backstep, that C loses grip as you turn, was false as drawn.
- Problem 8's backstep and flag. With the right shoulder 2 to 5 cm above C and the centre of gravity 25 to 35 cm off the hinge, the right elbow is 56 to 69° from a flag and 58 to 71° from the backstep at the ordinary size, and much the same small and tall. Either foot on 3 gives the same hinge, so at the same rise the door is the same, and the page's preference rests on the book's entries and not on geometry. In a reviewer's model the toe hook needs about 86 N·m at the ankle against perhaps 45 and holds 22 of 45 cm. The backstep needs about 288 N·m at the hip against perhaps 150 and holds 15 of 29 cm. Both are about 1.9 times over, so neither holds statically, and each only has to last for a quick catch. That is why move 3 has a deadpoint. Those limits are the reviewer's estimates.
- Problem 8's open route: a left foot on B beside the left hand has no door and uses a V2 technique. It is clean with the right foot on 2 (22 ordinary, 8 tall, 175 small), and C ends at the chest as with the flag. The page doesn't deny it. A smaller B would close it, with the head saying B and C each take one hand, but that is a figure change for a route the page doesn't deny.
- Problem 8's moves 1 and 3: the leg is straight on foot 2 at all sizes, and on foot 3 it bends again and goes tight as the arm locks. Hook angle against right elbow on foot 3 at the ordinary size runs from 180/180 at y=90 to 180/65 at the drawn pose. The earlier scan's cap came from the back-view knee rule.
- Problem 2: the route with the left hand on C is open, not closed. It pulls C at least 34° sideways at the catch at the ordinary size and 25° at the tall size, and the small climber is 15 cm short of E. The beta costs at least as much on the same measure. With the right hand on C, the left shoulder gets no closer than 10 cm short of D (23 small, and 2 past it tall), with C pulled 54° sideways. Hips over foot 5 pull C at least 36°, 28° small and 46° tall. Keeping C within 30°, the shoulder stays 41, 33 and 52 cm short. So for a moment no hand holds you in. D is drawn 15 cm long and 5 cm thick, and both hands on D have clean poses at every size, so "too thin to share" is a ruling (judgement). Right on D with left on B has clean poses at all three sizes, so the wrong hand costs you and doesn't force a fall. The wrong try and the swap both end on the fallback's catch. The gaston isn't a pure extra, because the right hand then has about 72 cm to E on C alone instead of 178 from B, so the page says you pay twice and doesn't say the gaston buys nothing. Both hands on C has more clean poses than the left hand on C with the right on B (1150, 92 and 2994 against 346, 5 and 1412 on feet 3 and 4), so the swap isn't worse than the fallback by geometry, and the book's Matching entry teaches it. The page now describes its cost without ranking it. The small climber's margin on E from C is thin on feet 4 and 5 (1.8 cm short with C at 45°) and 15 cm on feet 5 and 6. The fallback is a route the page doesn't reject.
- Problem 3's routes on the single rail. Every move of the beta is clean at all three sizes. With the heel on, the left hand reaches C with hips right of C (x up to 30, 25 and 25). Without it, from feet 4 and 3 and the right hand on B, the hips must be under C or left of it (x up to 5 at the ordinary size and -5 small; 35 tall, so the tall note says so). With the right hand on A the same stance is much freer, which is why the page no longer says "must": flat right foot x up to 25, -5 and 40 (18, 1 and 75 poses), and with the toe pointed down x up to 45, 25 and 60 (271 to 304, 46 to 53 and 584 to 650 poses).
- Problem 3's doors, the centre of gravity's distance off the hinge with the arm within 15° of the sloper: 35, 42 and 31 cm (ordinary, small, tall) for the left hand on B, left foot on 4 and right foot off; 29, 32 and 26 for the left hand on C; 19, 22 and 17 with a right foot on B. The last is an open route. With both hands on B, a right foot shares B with the right hand (clean at all sizes, x about 0 to 40), then stands up as the hand goes to D. The same line works with the right hand on A: the foot shares B with the left hand, or the left hand goes to C first with the right foot off (1121, 549 and 1657 poses), and then the foot goes to B. Nothing on your right holds you in as you catch the sloper, so it must hold the door alone. The page doesn't deny it, and "Your beta may be as good" covers it. With two start jugs that door was 7 to 9 cm, which is what made the lesson false.
- Problem 3's other way to the heel. The page concedes it in Next: right hand on A first, then the heel beside it. A is 24 cm wide. With the hand inboard at x=77 and the heel at x=84 to 88, the heel goes on in 175 to 181, 123 to 127 and 169 to 192 poses (ordinary, small, tall). The left hand then reaches C in 301 to 346, 250 to 298 and 348 to 377, and the right hand reaches D as in move 4. The right hand on A from feet 4 and 2 has 658, 512 and 834. The drawn heel sits where that hand would go, so the figure can't be read as this route. The wrong try is the right foot off: D from there has 1937, 907 and 3172 poses with the left hand on C, and from a right foot on 3 none, none and 102. A reviewer's statics rank hand first as easier. They compare against move 2 poses that the back-view knee rule thins out, so treat them as a model's figures.
- Problem 3's scans of move 2 are limited by the rule that flags a folded knee in back view, which is a rule about how a figure looks. The review's door of 47 to 53 cm comes from poses with the heel above the head. By reach alone, with hips at y=135, the door is 7 to 18, 16 to 30 and 0 to 10. So don't reuse 47 to 53 as a door.
- Problem 3's span: left foot on B and right foot on A are 98 cm apart at one height. Hips about 50 cm above them need friction of about 1.1 if the legs alone carry you, which is why the left foot stands up first. Old wall: 111 cm and 3 to 4. The right shoulder is at least 26 cm above B at the catch of C (median 52), 18 small and 14 tall, so B can only press there.
- Problem 1: the ordinary and tall climbers can skip B and foot 5, since D from feet 3 and 4 has clean poses, but the small climber has none. Nothing in the text denies it, and foot 5 keeps the small steps. Foot 7 earns its place only while the left foot stays off A: E from feet 5 and 6 with the left hand on C is out of reach at the ordinary size.
- Problem 1 has two more open routes. The opening says a lettered hold can take a foot, and A is free once the right hand leaves it. A left foot on A reaches D at all three sizes (28, 47 and 9 cm to spare) and, with foot 6, reaches E at the ordinary and tall sizes (11 and 32 to spare; small 4 short). That cuts three hip crossings to one. Separately, the left hand can stay pressing on A while the right hand goes straight to D, skipping C and B: easily when tall, only with a strong lean to the left at the ordinary size, and not at all when small. Neither touches the lesson, which is decided low on the wall, and "Your beta may be as good" covers them.
- Problem 4: the turn on C is a cost the page now states, as Problems 2 and 5 do, and no route is rejected for it. Move 5 is clean at the ordinary and tall sizes (71 and 482 poses) and 14 cm short when small, as the note says. A reviewer's model puts about 0.86 body weight on C at friction 1.0, 0.70 to 0.76 at 1.2 and 0.59 to 0.67 at 1.5, with no solution at 0.9 or below. These are a model's figures and nothing printed depends on them, which is why the page doesn't say "nearly all your weight". C drops to waist height only at the top of the rise (pelvis 295, 301 and 289 along the wall against C at 298). Two open routes: both feet up while the right hand is on jug B, which is the small note's route, and right foot to B before the left foot goes to A in move 6, clean at the ordinary and tall sizes.
- Problem 5's step to foot 5 isn't blocked. From the drawn pose a chain of clean poses rises 16 to 20 cm with the foot still on 3, to (38, 122) ordinary, (38, 120) small and (40, 126) tall, with A still below the pelvis. Moving foot 5 would nearly close the next step: pelvis positions clean on both 5 and 6 fall from 207 to 61, 91 to 5 and 307 to 128. So the wall stays and move 4 says to rise first.
- Problem 5's open routes. Staying on foot 2: C has 26, 45 and 8 cm to spare, but the hips top out at y=114, 104 and 122 on foot 2, below the 122, 120 and 124 that the step to 5 needs, so foot 3 is still needed after the catch. Setting both feet on 4 and 3 before the lift is what the wrong try's last sentence now answers. Skipping E: as you stand, C ends 40 to 60 cm below the right shoulder and E stays 16 to 30 above it. D is at or below the left shoulder by the catch of F either way, so the page gives that as no difference. The finish stays right hand first because left hand first has no clean pose at the small size.
- Problem 6's left hand can stay on C and reach E just as well from feet 5 and 6: 372 clean poses against 378 at the ordinary size, the lowest pelvis at y=188 in both, and clean at the tall size too. D earns its place because of where it sits at the catch: 16 to 45 cm above the left shoulder, while C is 10 to 40 below it. C is drawn 18.2 by 5.4 cm and D 13.0 by 3.8, 1.4 times each way, so the page no longer says "far smaller".

**The back views flatter steep walls.** They measure in the wall's plane, so they ignore how far your hips and shoulders stay off the wall. On walls of 25° and steeper that costs about 5 to 12 cm, or about 10 cm for hips 30 cm and shoulders 20 cm off. Treat any margin under about 12 cm there as needing a deadpoint. That is why Problem 6's E from feet 5 and 6, Problem 7's B from A and 4, and Problem 8's D from the hook are deadpoints in the text. Problem 6's small climber, from A and 6, has 0 cm in the plane with the leg and arm both straight, so hips 15 to 25 cm off the wall leave E 15 to 22 cm short. With the hips 26 cm off the wall and the shoulders 20 cm off, the hook has 3.5 cm to spare for the drawn climber, and the small and tall are 5 and 1 cm short.

One pose doesn't come out clean and isn't drawn: Problem 3's right hand on D from foot 3 fails at the small size, which is the shortfall the note describes.

## 11. Order of work

1. Write `figtools/figs_reading.py` with `--grey`, and look at all sixteen at 150 dpi. Report any hold whose direction doesn't read, and any pose that looks wrong.
2. Add the macros to both templates, and the CSS and wording rule to the website.
3. Add the section to `book/chapters/02-reading.typ` with small `Edit` calls, and the two small additions.
4. Add sixteen tables to `book/figure-alt.toml`, then run `python3 figtools/build_all.py` and copy the `drawn` hashes in.
5. Check it all:
   - `./build.sh`, which runs `tools/check_fit.py` and `tools/check_order.py`. Look for entries that now spill because of a new "Referenced from" link.
   - `python3 tools/check_alt.py`, which must print nothing about these figures.
   - `./build-site.sh`. Open the chapter page, open and close an answer, and check a figure beside the prompts on a wide screen and below them on a phone, in both light and dark.
   - Look at the sixteen PDF pages. Each question is on an odd page and each answer on the page after it.
   - Look at Problem 1's C, Problem 2's D and Problem 3's A and E on the Boox.
6. Add a line to `CHANGELOG.md` under "Unreleased", and log the work in `research/revise3-02-reading.md`.

**What Simon has ruled**
- A blank page before Problem 1 is acceptable.
- The opening states the drawn climber's height and reach.
- Problems 3 and 4 don't link to `overhang`.
- Problem 6 keeps its treatment of the static option: a slow lock-off or a step up to A may work, and the deadpoint is the better choice.

**For Simon to decide, none of it blocking**
- Problem 7's beta. A foot on A before the second palm is easier on the palms (section 10), and Next says so. Making it the beta would shorten the heavy squeeze to one foot move and needs a new figure. A first draft was cramped, with the left knee low and the foot hidden, so the printed order and figure stay for now. The tags would become Y R1 and Y L2. The palm spots could also move in to (∓20, 198) if the figure changes. One reviewer's shoulder figures, from memory and unmeasured, suggest V5 is low for the printed order.
- Problem 3's order. Right hand on A with the heel beside it is clean at all sizes and a reviewer's statics rank it easier, so the printed order may not be the easiest. Next concedes it and the heel lesson stands either way. Making it the beta retags to A R1, C L2, D R3, E R4 L5 and needs a new figure. A wall fix would make A a big rounded hold with a dip so that a hand fails, which is a redraw and changes the bowl wording.
- Problem 8's toe. A heel on A is at least as good on most measures, and the wall can't close it. The page concedes it, and the toe stays because this is the set's toe-hook problem. The book's decision table sends an edge out to the side to the heel, so the toe stands by ruling and not by reading. Turning A to `use=225` would close the heel but isn't a ready fix: the ordinary climber ends 2 cm short and small and tall have no pose. If that isn't enough, the first alternative is the rejected roof in section 1.
- Problem 8's flag and backstep have the same hinge and the same offset at the same rise (section 10). The page prefers the backstep because the book's entries do, not because of geometry.
- Problem 4's move 5 leads with a lock-off and offers the deadpoint "if you need one". A reviewer wants the deadpoint first, on a model's 0.86 body weight on flat C. Nothing printed is false, so it stays.
- Whether "What to try next." should become "On a real wall." A reader's point: the problems can't be climbed, and the advice under the label is for similar moves. It is shorter and reads correctly on all eight. The label is in both templates.
- Whether the half line between notes should become `gap(0.6)`, the template's own first step. Problem 4 would then have no slack.
- `book/figures/sit-start.svg` panel b has the same reversed right foot that Problem 5 lost. Its fix belongs in the main checkout.
- `compression.svg` still has the old, too shallow volume that Problem 7 lost.

## Rejected findings

The critics' findings were checked one by one against the drawing library and the entries. These are the ones rejected, in whole or in part.

**Problem 1**
- *Bring the later rises down to 45 cm or less.* This compared the wrong numbers. The 52, 54 and 62 cm are one foot's rise to its next hold. The 64 cm step it set them against rose 70 cm above the foot you stand on, while the later steps rise less than 40 cm above theirs.
- *Keep the crux at moves 1 to 3 and ask where you first trust a foot with no foothold under it.* The hands help most during those moves, so the first critic's physics holds. That prompt would also point straight at the smear. The crux moves to where your hips pass A, which fits the existing prompt about having least to pull on.

**Problem 2**
- *Turn C to `use=60` to `70`.* C has to keep working as your hips move right, and an edge facing up and right pulls off in that direction. `use=90` holds under the hand and as the hips move, so that one was taken.
- *Move your hips right past D until your left arm is straight, with your right hand still on C.* It is out of reach. With the hips turned fully, the right hand holds C only until the hips come about under D. So the moves take the hips under D, then send the right hand to E as the left leans off D.
- *Replace the end of Wrong with a gaston "at full reach".* D is only about 25 cm from the right shoulder in that position, so the gaston is close, as the first critic found.
- *Use `variant="flat"` on a jug for D.* A jug is an easy gaston, so the wrong attempt would cost nothing. D is a thin flake instead, whose lip also reads.

**Problem 4**
- *Move foot 4 to height 136, or part it from A by 15 to 20 cm, and add the rule "one foot to each".* Jug A would still be a higher and bigger foothold than foot 4, and gyms have no such rule. It would rescue the numbers with something invented. A becomes the thin edge and foot 4 goes.
- *Say that foot 3 takes only one shoe.* It would make the wrong attempt fail by decree. The honest version keeps foot 3 wide, lets you touch D from it, and says what stretching out costs.
- *The pose at `(6.6, 188)`, and the pose at `(9, 193)`.* With the right foot on A at height 156, the first pushes the right knee 4 cm into the wall line and the second 22 cm. A new pose keeps every joint clear.

**Problem 5**
- *Take off two bolt holes.* That breaks the count for the ordinary climber, who would get 8.5 holes against the 9.1 needed although the pose has 11 cm to spare. One hole matches all three sizes.
- *Move foot 2 out to about x=40.* The same critic's other option works without changing the wall: the prompts are reworded, and move 1 says why foot 2.
- *Rename it `reading-v3-sit`.* Not needed, since smaller edges, a crimp as first target and fewer footholds answer the fault.

**Problem 6**
- *A slow reach fails because your hips sag out.* The climber has about 10 cm to spare in the drawing and perhaps nothing on the real wall, so "fails" overclaims. The text says it may just go but leaves you on one bent arm.
- *Add to Next that the left hand may go to D first, or make D poorer.* Neither goes far enough. With the left hand on C the arm can't hang straight, and on D it can, as the deadpoint entry asks. D first becomes the beta.

**Problem 7**
- *Round the top of Y's outline.* Not needed. The top is out of reach from A once A moves down, and the moves use its corners from feet 3 and 4.
- *Say which of Y's low corners move 5 means.* Move 5 no longer exists.

**Problem 8**
- *Say "with your arms taking your weight for a moment" at the foot move.* The fault is real, but cutting a foot on a 40° wall isn't the answer. The hook stays on while the right foot steps to 3, and that pose is clean at all three sizes.

**Colours and website**
- *No fault found in sections 5 and 6.* This finding reported nothing to fix, and its checks still hold for the changed figures: all sixteen paint by file name, and only Problems 2 and 4 are wider than `BESIDE_MM`. Its advice to take the `drawn` hashes from the final files stays in section 6.

## Rejected findings, round 1

These findings from the review of the built section were checked against the poses and the arithmetic, and rejected in whole or in part.

**Problem 2**
- *With the left hand on B the right shoulder can't get closer than 51 cm to D.* It gets within 20 to 27 cm, on the old feet and the new, which agrees with what the first critics found. So the gaston isn't far from the shoulder, and the wrong try now fails on letting go of B with only a thin gaston holding you.
- *Move 5: right foot to 6, left foot to 5, with the right hand still on C.* The small climber has no pose there. Moves 5 and 6 now let go of C first and walk the feet after, which suits every size.

**Problem 3**
- *E with `use=15`.* That is the wrong way round. A hold facing right is a right-hand sidepull with your body on its left, so it would have helped the ladder it was meant to stop. E has `use=165`, which gives what the finding wanted: a left-hand sidepull with your hips to its right, and a right-hand gaston.
- *A with `use=130`, facing up and left.* That face suits a toe and lets a heel pulled towards you slide off, the opposite of the lesson. A stays up-facing and becomes a bucket, whose rim gives a heel something to pull against and whose top still takes a toe.
- *Keep "a few centimetres short" and blame the low right foot.* True with the foot on 3 (+6), but the foot can come off, and then F is well within reach. The hinge and the sloper are the reason.

**Problem 4**
- *Share B between the right hand and the left foot in the small note.* The right hand is still on B at that point, and both toes on A work.

**Problem 5**
- *Lower A and B by about 8 cm.* Not needed. The note says they are a full stretch from the mat at this size.
- *A leader to foot 6 across the arm.* Foot 6 moved right to (58, 146) instead, with every move's pose still clean.

**Problem 6**
- *Make a wall change that closes the route over A and B.* The finding itself found none. The text answers the route.
- *Keep the one-handed dyno in the small note.* There was no room, and it argued with the wrong try.

**Problem 7**
- *"Don't rush your palms."* The other finding's cut is simpler, and `E18` is about holds with no obvious grip, which these are. "Move it fast" comes from the compression entry and is about the foot.
- *Small: B is a long deadpoint from A and 4.* In the plane it has 1 cm to spare, so with the wall's lean it is out of reach. The left foot goes up to 3 first (7 cm to spare), then a long deadpoint. Round 3 changed this: with the left foot free and leaving A, B has about 18 cm to spare, and that is what the note now says.

**Problem 8**
- *The hips can't pass x=12 while the left hand is on B.* With a lean to the left they can reach the hinge. So the flag isn't impossible, and the wrong try says what it costs instead of saying that the door must open.
- *Small: E is out of reach from 3.* True, but the moves now send everyone to foot 4 first, so the note says what does differ: the flag leaves D out of reach.

**Pages**
- *A rule and 1.5 lines of space above the foot line.* It would cost two lines on every answer page. The difference from an entry's apparatus stays.

**Website**
- *Leave the caption width to the typography pass.* It was cheap, so it went in, scoped to the answers. It leaves entries alone.

## Rejected findings, round 2

These findings from the second review were checked against the poses and the arithmetic, and rejected in whole or in part.

**Problem 2**
- *Your shoulder "does all the work" on the gaston.* The entry and C34 say most, so the text says most.
- *Arrow `[(-80, 208), (-46, 196), (4, 204)]`.* It crosses the right forearm and lies along the left, which section 7 forbids. The cross-under is right, but the arrow stops short of the arm.
- *Three short sentences for the question's alt.* It ran over the length rule, so it became two shorter ones.

**Problem 3**
- *Right foot to 3 before the left hand goes up.* The hand on the higher edge has no clean pose from feet 4 and 3 at the ordinary or small size, so that order can't be drawn. The heel goes on first, with both hands on the start jugs, and every later stance is clean at all three sizes.
- *The fallback that keeps D.* The route it answers would still be easy, and it costs a line that the page hasn't got.
- *Pose `(32, 168), lean=-12, bend=-10`.* It works, but the right shoulder stays 30 cm left of the sloper. `(30, 172), lean=12, bend=6` puts it under the sloper with a straighter arm, which is what the words say.

**Problem 4**
- *"The hip turn doesn't show from the side" in the caption.* A third caption line spills the page.

**Problem 5**
- *"About 25 cm of slack".* My scan gives 44, 34 and 55 cm to spare, and the reviewer's own gave 36, 26 and 46, so the text says about 30 cm. "Slack" also isn't the book's word.
- *"Both legs end straight" from feet 1 and 2.* The left leg does and the right nearly does, so the text says "your legs".

**Problem 6**
- *"Brings E within reach" for a foot on A or B.* E is already in reach at the ordinary size, and a right foot on B adds no reach at all. What both steps do is shorten the rise, so the text says that.

**Problem 7**
- *A tall climbers' note.* From high on X the tall climber is about 5 cm short in 3D with one palm on, so it is a throw off a smear. It isn't a real difference in the beta, so no note. Section 10 records it.

**Problem 8**
- *"A backstep on 3" as written.* It doesn't say which foot, and the backstep needs the left, so the text names it.
- *"Pull your hips close to the wall" in the small note.* True, but the note has to fit one line. Move 3 and the figure already show the hips close.
- *The foot line with five entries.* It wraps and spills the page. `cutting-loose` is linked in the text at the kick instead.
- *Moving D to save the reach claim.* The reviewer tried three spots and the hook ran out first each time, so the text concedes the backstep instead.

**Pages**
- *Fixes that "should fit".* Problems 1, 2 and 8 spilled on the first build with the reviewers' wording. Words were cut, and no space, size or `k:` changed.

## Rejected findings, round 3

These findings from the third review were checked against the poses and the arithmetic, and rejected in whole or in part.

**Problem 2**
- *C pulls "at least 30°" in the fallback.* True at the ordinary size (34°) but not the tall (25°), so the text says about 30°.
- *Shorten D to `w=11`.* The ruling "too thin to share (judgement)" answers the prompt without touching a hold whose lip reads.
- *"Pivots to point left" and "hips right towards foot 5".* The meaning survives with fewer words, and move 5 sets the page's height.

**Problem 3**
- *One wide start jug.* The wrong size of fix. A right foot beside the right hand on a jug is clean at all three sizes, with a door of 19 to 22 cm, and a big foothold there is a plain rockover. A thin rail keeps the single hold and takes that away, and it makes A look better to a hand.
- *"D is no closer from there."* False on the new wall: D is 105 cm from A and 120 cm from the hand on B. The sentence goes.
- *"Compare the marks on A with those on C."* The library shows chalk only on big jugs, so the prompt compares A with E.
- *"Keep your left hand on B" in the wrong try.* With one start hold the door is far open with the left hand on B or on C (35 and 29 cm), so the sentence no longer needs to say which.
- *Pose (36, 180), lean 20, bend 10.* It takes C to 24° off its face, but the arm hides the head. (34, 176), lean 16, bend 8, gives 33° with the right shoulder 7 cm past D and the head clear.

**Problem 6**
- *Pose (14, 192), lean -20.* It straightens the right leg but closes the left elbow to 66° and bends the right arm. Round 2 opened that left arm on purpose, so the pose stays.
- *Keep "A deadpoint is more controlled than a dyno" and the longer small note.* Two lines over, as the reviewer expected. The wrong try covers the first.

**Problem 7**
- *Make the right palm first the beta now.* The finding is sound and is logged for Simon. The reviewer's draft figure was cramped and the printed figure teaches the squeeze well, so Next carries the order and says it is easier on the palms.
- *"Your right foot must leave X first."* True, but there is no line to spare, and the move order implies it.

**Problem 8**
- *Move A out to (-96, 138).* Optional and it doesn't close the heel. D would gain about 5 cm, and the tags and feet would all need another look.

**Problem 4 and the rest.** No finding was rejected on Problems 1, 4 or 5.

## Rejected findings, round 4

These findings from the fourth review were checked against the drawing, the book's entries and the strict test at the top of this file, and rejected in whole or in part. The "could" findings were left, apart from those already logged in section 10.

**Problem 1.** Every "should" went in. No finding was rejected.

**Problem 2**
- *"Only your feet hold you" is false, must.* It says which contacts carry you for a moment, not that you balance there, and the book uses "hold" that way. The next positions exist at all sizes, and the tip rate fits "for a moment". The reviewer's friction limit is a model's. "No hand holds you in" went in as a tidy.
- *"Like a small deadpoint."* That entry grabs the next hold at the top of a rise. Here the hand is already on D and the other has 124 cm to go.
- *The rival in Next costs less, must.* It is a rival the page doesn't reject, and "If you can't let go of C" is a condition. The beta's pull on C is a choice and its catch of E has more clean poses (1083, 59 and 2504 against 226, 0 and 1227). "This may be easier" is an unlabelled judgement and "a hand always holds you" asserts that C holds at 50°. The two wording points went in.
- *Delete the swap sentence.* The fault is the ranking, and the two skeptics split. An earlier round asked for the swap to be answered, and the Matching entry teaches a way round "too small to match". The sentence now describes and doesn't rank.
- *"The gaston buys you nothing."* False: the right hand then has about 72 cm to E on C alone instead of 178 from B. "You pay twice" stays, since it counts the wrong try's own costs and says "It can go".

**Problem 3**
- *"Moves 2 to 5", "You swing until the heel lands", must.* The door of 47 to 53 cm comes from a drawing rule and poses with the heel above the head. By reach alone the beta's door at move 2 is smaller than the one Wrong rejects, it has two hands on and it ends in a bowl. The new text would put a swing in the beta beside "You swing open".
- *"A right foot on B makes the swing smaller, but you still catch a sloper on the move."* Move 4 catches the sloper too, so this rejects a route for a cost the beta pays. The route is in section 10 as one the page doesn't deny.
- *"That hand must leave for D", "With no foot on A, your left hand and foot make a hinge", "Your right hand goes from A to D (judgement)".* The first adds a "must" that the tall note contradicts. The second is untrue with a right foot on B or 3. The third repeats move 4 with a label the opening covers.
- *Move 3 as a small deadpoint.* It rests on a model's statics, and "so don't stop" already says it.
- *Cut ", the old start hold" to pay for Next.* The moves column ends above the caption, so it pays no height. "A heel you don't pull on won't hold" paid instead, since moves 3 and 4 say to pull.
- *Marks on E.* The page needs a look on the Boox first, so section 11's check now covers E as well as A. If E's band doesn't read, the prompt can drop the comparison.

**Problem 4**
- *The page hides C's load, must.* No printed sentence says anything false about C, the move can be done, and no route is rejected for it. The cost now goes in as a should, without "nearly all your weight", which is a private figure at one friction and reads against "Drive the toe in and pull". "Your toe is on a thin edge" stays, because Next's "If the toe pops" follows from it. "Place it again" stays.
- *Deadpoint first at move 5.* Rests on the model, so it is logged for Simon.
- *"It may just go, but straight legs can't pull you in."* Over budget. "Tend to" with the label does the work.

**Problem 5**
- *Move foot 5 to (64, 84), must.* From the drawn pose a chain of clean poses rises to the step at all sizes. The reviewer's tall claim came from a lean grid that skipped -8. The 50° knee limit is a drawing rule. The move would nearly close the next step at the small size.
- *Move 3 undoes move 2, stay on foot 2, must.* A rival the page doesn't deny, and "so this foot can push" is true (knee 50 to 105 from foot 3, 112 to 180 from foot 2). "From 2 your leg is nearly straight at the catch" would be false at the ordinary and tall sizes, and staying on 2 has no clean pose into the step to 5.
- *"Only D above it".* D is at or below the left shoulder by the catch of F, so the page contrasts C and E instead.
- *"E won't hold you alone."* Unsupported, and D is alone in the printed order. Section 10 has the real reason for the finish.

**Problem 6**
- *"Feet on 1 and 2".* It loses which foot, and "Right foot on 1, left on 2" fits the line.
- *"You reach about ten and a half bolt holes" in Step 5.* True only of the drawn climber, so the prompt asks the reader to count.

**Problem 7**
- *"Does the order matter?" gets three answers, must.* The skeptics found the three statements compatible and the caption true, and the order is logged for Simon. The page still needed one answer, so Next now gives it. "The order matters." alone would overclaim, because which hand goes first changes almost nothing on this wall.
- *"Right foot fast to 4."* Rests on the model, and move 4's next sentences already keep you moving.
- *Palm spots.* The figure stays by decision, so this is in section 10.

**Problem 8**
- *The backstep opens the same door, must.* The doors match at the same rise, but the same model also fails the printed hook by the same factor, so it can't single out the backstep. "Opens the same door" would contradict Chapter 1, the troubleshooting list and Chapter 4's sidepull rule. The size notes follow the Backstep entry.
- *Moves 1 and 3 can't both be true, must.* The cap on the knee came from a drawing rule. On foot 2 leg and arm are both long at all sizes, and the leg bends again on foot 3. "Until the hook leg is straight" fails for a small climber whose leg starts straight, so "goes tight" went in.
- *"A toe hook mostly steadies you, so don't wait to catch D."* It rests on the model, the entry's summary also says the leg keeps your body in place, and it would clash with the caption. Move 3's deadpoint covers it.
- *A smaller B.* A figure change for a route the page doesn't deny, so it is in section 10.
- *Finish order.* Left as a could. D is a jug and E a crimp, and the right hand travels only 37 cm.
