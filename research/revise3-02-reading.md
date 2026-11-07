# Chapter 2 changes for the third revision

- Opening: joined the staccato sentences in the second paragraph. Facts unchanged.
- 2.1 Why reading pays off: applied evidence items 4 and 5 (retitled "Reading changes how you climb", roped routes, 29 male climbers, part of the stops effect held up, "one 2018 World Cup"), cut the inference about time on the arms, joined sentences in the other bullets and the closing line.
- 2.2 The method: joined sentences in steps 2, 3, 4, 5 and 8 and the closing keypoint. Steps stay imperative, and 1, 6, 7 and 9 read well and stayed as they were. The figure captions are unchanged.
- 2.3 Hold direction: rewrote the keypoint ("Put your body where you are pulling towards" was awkward) and the paragraph after the figure. The table is unchanged.
- 2.4 What to read first: joined the opening sentences. `#tref("corner", body: [Corners])` keeps the row's name after the merge into Stemming.
- 2.5 What the setter had in mind: turned the fragment questions in the opening into one sentence, joined sentences in the "force body positions" bullet and the box, and removed a repeated "problems" from the comp-style gloss.
- 2.6 Other people's beta: renamed "Other people's beta, and reading for your size", joined sentences in the bullets, replaced the box with the doubled box from `H-small.md` section 3, and renamed the "Short climbers" index term "Small climbers".
- 2.7 Flash or project?: applied evidence item 5 (Flashing paragraph, routine lead-in, keypoint, six-attempt paragraph). Dropped the repeated gloss on crux and joined two project steps.
- 2.8 Rest between attempts: applied evidence item 5 (table row, "about four to six full attempts", "The 2018 figure ... Neither figure is advice"). The rest stays as it was.
- 2.9 When to change the beta: dropped the repeated gloss on beta and joined one bullet. The rest stays as it was.
- 2.10 Indoor grades: joined sentences in "How a gym grade is made", the consistency paragraph and three bullets, replaced "turned up in our search" with "We found no", and joined one calibration step.

**After review.** Restored edition 2's wording where the sentence pass had over-joined (opening, "Experts read in chunks", steps 4 and 5, the Kaya sentence, "Style and sequence") and cut needless word swaps at lines 12, 39, 159, 248 and 256. Deleted "Chapter 7 covers each terrain", which the corner merge made false; every row prints its page. Fixed the garden path at "Rest between attempts", said "competition figure" at line 233, moved the gloss on "link" to its first use, linked "smears", and made `@cons-small` a plain reference now that chapter 9 has the label. Three box bullets differ from `H-small.md` section 3 for clarity: "where the holds allow", "climb" for the unglossed "send", and the bolt-hole check now starts by counting what your reach covers, as H9 does. Rejected: shortening the selection effect at line 212 to "the same cautions", because `evidence-3.md` keeps it there as the 6% figure is the one most exposed to it, and a pointer sends the reader back; adding "warm up again" after 15 minutes at line 233, because G38 speaks of breaks in general and chapter 9 already has the rule, so this would be new advice for no fault here; adding "once you have warmed up" at line 192, because line 26 and chapter 9's warm-up table already assume it and the clause would interrupt the sentence `evidence-3.md` gives. No action on the `a-troubleshooting.typ` double reference: its owner has already fixed it.

**Layout.** The doubled box now breaks across two pages, between the bullets of its second list. Left for the pass over rendered pages. The chapter still takes 12 pages.

**Words.** 3,961 before, 4,218 after. The doubled box adds 150, the evidence wording 111, and the sentence pass saves 4.

## Eight problems to read

Built from `research/worked-readings.md`: section 2.11 with its sixteen pages, `figtools/figs_reading.py`, `reading-question` and `reading-answer` in both templates, the CSS, the wording rule and sixteen tables in `book/figure-alt.toml`. The opening states the drawn climber's height and reach, Problems 3 and 4 don't link to `overhang`, and Problem 6 keeps its static option, as ruled.

**Text that differs from the brief.** All of it follows the rule on short sentences and few commas, so most long sentences became two or took a colon or parentheses.
- The opening paragraph keeps its sentence and adds "It ends with eight problems to read for yourself", instead of a longer sentence with a third comma.
- "(judgement)" comes off claims that are only about one problem's beta, since the opening covers those and the brief's own rule says not to repeat it. It stays on claims about technique or physics, and on Problem 6's step up to A. Removed from Problem 1's Next (twice), Problem 3's Next, Problem 5's Crux, Problem 6's Crux, Problem 7's Wrong (feet 3 and 4) and Problem 8's Wrong.
- Three phrases could suggest that someone had climbed the problems or were unclear. "Feels more exposed" became "looks more exposed", "the problem still goes" became "you could carry on", and "have the hips for it" became "your hips are mobile enough".

**Figures that differ from the brief.** Problem 6's answer had tag B on the right thigh, so it moved to the left of its hold, at (-1, 159). Problem 5's dashed arrow ran along the leader to foot 4 and into the arm, so the arrow now stops short of the climber at (-44, 63) and the number moved up to (-88, 76). Problem 7's A moved from (-25, 112) to (-23, 113), clear of the shin. All answer poses print no warning, and Problem 4's joints stay clear of the wall as the brief gives them.

**Alt text.** Problem 6's question says footholds at three heights, because the drawing has three. Six others lost a comma or two.

**Layout.** All sixteen pages fit with nothing squeezed, and no space or `k:` changed. The lowest text on the answer pages is unchanged from the brief's table. Questions are on odd PDF pages 33 to 47 with no blank page before the first, which makes them even printed pages (22 to 36), because `to: "odd"` counts physical pages and the front matter takes 11. For the pass over rendered pages:
- The new line after the method's keypoint leaves only one row of the hold table on printed page 13, with the rest and a repeated header on page 14.
- "Reading for your size" still breaks across two pages, now with a single bullet before the break.
- References in Chapter 1 grew to three digits, so it takes one more page, and 1.8 sits alone on printed page 8.
- The book goes from 271 to 289 pages: sixteen for the problems, one in Chapter 1, and one in Chapter 2 before the problems. `deadpoint` is now estimated at four pages but still takes three.

**Not checked.** Problem 1's C and Problem 3's A on the Boox, and how chalk and rubber look there.

**Words.** 4,235 before, 8,642 after, nearly all in the new section.

## Review of "Eight problems to read", round 1

Eleven reviewers read the built section. I checked each finding against the drawn wall with a search of clean poses at all three sizes, and did the arithmetic. The brief, `research/worked-readings.md`, now describes the section as it stands, and its "Rejected findings, round 1" says what I turned down and why. Its sections 9 and 10 have the new walls, text and reach figures.

**Problems whose lesson was false or whose moves couldn't be done.**
- Problem 1: redesigned. A low volume replaces the shoe marks, feet 1 and 2 are lower, and the left hand goes to C before the right goes to B.
- Problem 2: C is narrower, feet 4, 5 and 6 moved, and the moves and crux say that D holds nothing until your right hand lets go of C.
- Problem 3: reach is no longer the reason, because F is in reach from foot 4 once the right foot comes off. E faces left and A is a bucket. The review's two hold directions were the wrong way round, so neither went in as written.
- Problem 4: the head says C takes one hand, and the crux, Next and size notes are rewritten around "left foot stays low until you hold D".
- Problem 5: the seated pose was impossible. The figure now shows move 3, the head states the start feet and `layback` is gone.
- Problem 6: the right hand goes up to C first. The text answers the route that skips E, and the static option stays as ruled.
- Problem 7: redesigned. Y is narrower and its depth is stated, the beta stands on A, and the corners are gone.
- Problem 8: redesigned. B, E, A and C moved, the right foot goes to 3 before the left hand moves, and the wrong try says what a flag costs instead of saying that it fails.

**Layout.**
- A full line now parts the figure block from Crux, as under a figure in an entry, and pages were cut to fit it. No `k:` changed and no space closed up.
- The pointer to the problems moved into the first paragraph of 2.2. That cures the one-row table remnant on printed page 13 and the one-bullet break in the size box.
- The foot line takes the apparatus's paragraph settings, so a wrapped line stays correct.
- Lowest text on the answer pages: 706, 760, 763, 766, 766, 771, 739 and 761 pt. The book stays at 289 pages. `tools/check_fit.py` passes.

**Web edition.** The notes take print's half-line rhythm, the problem head uses the Step head form with an anchor, the summary reads "The answer to problem 1", and a caption no longer widens the figure's column on answers. Checked in Chromium, WebKit and Firefox at 1280, 768 and 375 px, with every answer open: no sideways scroll and no broken image.

**Left for Simon.** "What to try next." against "On a real wall."; `gap(0.6)` between the notes; `sit-start.svg` panel b, which has the reversed foot that Problem 5 lost; and `compression.svg`, which has the shallow volume that Problem 7 lost.

**Not checked.** The Boox, including Problem 1's C and Problem 3's marks. Nobody has climbed any of this, and the friction and swing arguments are judgement.

**Words.** 4,235 before the section, 8,642 after the first build and 8,717 after this round. The file grew because the new notes answer routes the first text left open.

## Review of "Eight problems to read", round 2

Eight reviewers attacked the repaired section, one problem each. I checked each finding against the drawn wall with my own scans of clean poses at all three sizes, ran the reviewer's statics for the volume and did the arithmetic. The brief, `research/worked-readings.md`, describes the section as it now stands. Its "What round 2 changed" gives each problem's changes, sections 9 and 10 have the walls, text and reach figures, and "Rejected findings, round 2" says what I turned down and why.

**Lessons that were false, and problems redesigned.**
- Problem 3: redesigned. A route of jugs alone skipped the heel, the sloper and the edge, so the old D goes and the holds above it are re-lettered. The heel goes on first, because the left hand has no clean pose on the higher edge from feet 4 and 3 at the ordinary or small size.
- Problem 7: the squeeze needed about 5 body weights per palm at skin friction of 1 on the old Y, and about 1 on the narrower one. The crux now runs until your right hand catches B.
- Problem 2: a left hand on C with a right hand on E skipped the problem, so E and three footholds moved and the wrong try answers that route.
- Problem 5: staying on foot 2 had no benefit, so the feet go first and the catch is a deadpoint. The figure was redrawn.
- Problem 8: the book's own entries point to a backstep here, so the page concedes it. The wrong try's reach claim ran the wrong way and now says what a flag costs in lock.

**Words and drawing that disagreed.** Problem 1's figure moves to move 6, because an honest lean off C can't be drawn at move 5. Problem 2's muscle dots, Problem 3's bent arms, Problem 4's knee on B, and Problem 6's holding arm are all redrawn.

**Text.** All of it follows the rule on short sentences and few commas. The reviewers' wording spilled Problems 1, 2 and 8 on the first build, so I cut words. No `k:` changed and no space closed up. Some reviewers' wording changed for accuracy, as the rejected list says: "most of the work" for the gaston, "shortens the rise" for a foot on A or B, and about 30 cm to spare in Problem 5.

**Layout.** Lowest text on the answer pages: 765, 760, 763, 777, 752, 755, 772 and 761 pt. The book stays at 289 pages, `tools/check_fit.py` passes and `tools/check_alt.py` says nothing about these figures. Problem 4 has less than a line to spare. If page numbers move it, cut "Square your hips once you hold it." The opening now says ten and a half bolt holes.

**Web edition.** Built with no warnings. Opened at desktop and phone width with every answer open: no broken image and no sideways scroll. It needs no new macro or CSS.

**Not checked.** The Boox, including Problem 2's D, Problem 3's bigger A, Problem 8's turned C and D, and how chalk and rubber look there. Nobody has climbed any of this. The friction, swing and hook-load arguments are a model's figures and judgement, and Problem 7's squeeze and Problem 8's hook are the least certain.

**Words.** 8,717 before this round, 8,990 after. The file grew because the notes now answer routes that the earlier text left open.

## Review of "Eight problems to read", round 3

Eight reviewers attacked the section again, one problem each. I checked each finding with my own scans of clean poses at all three sizes, reran the reviewers' statics where a finding rested on them, and did the arithmetic. The brief, `research/worked-readings.md`, describes the section as it now stands. Its "What round 3 changed" gives each problem's changes, sections 9 and 10 have the walls, text and reach figures, and "Rejected findings, round 3" says what I turned down and why.

**A lesson that was false, and the problem redesigned.** Problem 3: taking A with the right hand freed the start jug C for the right foot, which gave a route with no heel at all three sizes. The review proposed one wide start jug. My scan found that a jug still lets the right foot share it with the right hand, so B is one thin rail. Old D, E and F are now C, D and E. The left foot now stands up on B before the roll, because the old move 6 did what the page's own wrong try condemned.

**Reasons that were false, now replaced.**
- Problem 2 rejected a rival for a cost the beta pays too. The rival moves to Next as a fair fallback, and the page says that only your feet hold you for a moment. "Trap" is gone.
- Problem 5's wrong try blamed straight legs and a press, and neither separates it from the beta. It now says the try is at its limit. Everyone steps to foot 5 before the left hand goes to D, and the small note no longer has a leg crossed under the thigh.
- Problem 6's finish let go of the higher hand, which also made the stated cost of skipping E false. The left hand now goes to F first, and the small note steps both feet up.
- Problem 7's fallback couldn't hold, so it now takes Y with the right hand first.
- Problem 8's case against the backstep ran the wrong way. The kick is gone, the heel and the plain throw are conceded, and the size notes are rewritten.
- Problem 4's rise to E had nothing above you as written, so the right hand stays on D until the top. D is a new local profile, because the library's sloper turns with the wall and fell 53° from level.
- Problem 1's move 5 couldn't be done in the order written, and two crux sentences were false.

**Figures changed.** Problem 1 (move 6 stands up on the right foot with the left arm straight), Problem 2 (a disc by the cross), Problem 3 (new wall, heel in the bowl, a clearer sidepull), Problem 4 (D, and no dashes under the shin), Problem 5 (hips lower, leg over the arm, closer tags), Problem 6 (A shows through the knee, new finish tag) and Problem 8 (hook leg nearly straight). All answer poses print no warning, and Problem 4's joints stay clear of the wall. Each changed figure was looked at in grey and painted, and the `drawn` hashes are copied in.

**Text.** Short sentences and few commas, as the foreword promises. The reviewers' wording spilled Problems 2, 3, 6 and 7 on the first build, so I cut words. No `k:` changed and no space closed up. Problem 6 lost "A deadpoint is more controlled than a dyno", as the reviewer allowed, since the wrong try covers it.

**Layout.** Lowest text on the answer pages: 766, 777, 779, 777, 770, 771, 772 and 777 pt. The book stays at 289 pages, `tools/check_fit.py` passes and `tools/check_alt.py` says nothing about these figures. Problems 2, 3, 4 and 8 have less than a line to spare.

**Web edition.** Built with no warnings. Opened at desktop in light and at phone width in dark with every answer open: no broken image and no sideways scroll.

**For Simon.** Problem 7's easier order is in Next, and making it the beta needs a new figure. A heel beats Problem 8's toe on most measures, and no wall change closed it, so the page concedes it and the toe stays because this is the set's toe-hook problem.

**Not checked.** The Boox, including Problem 3's marks and thin rail, Problem 4's new D and Problem 1's C. Nobody has climbed any of this. The friction, swing and hook-load arguments are a model's figures and judgement.

**Words.** 8,990 before this round, 9,161 after. The file grew because Problems 2, 3, 7 and 8 now concede routes in print, and Problem 3's moves say what the left leg does.

## Review of "Eight problems to read", round 4

Eight reviewers attacked the section again, and it then had to converge, so a must had to meet a strict test (top of `research/worked-readings.md`). Two skeptics checked each must. Where they split, I read the evidence and checked it. The brief describes the section as it now stands. Its "What round 4 changed" gives each problem's changes, section 10 has the new figures and "Rejected findings, round 4" says what I turned down and why.

**Musts.**
- Fixed: Problem 3's "you must stand on 4 and 3" (both skeptics: false, scanned with the wrong right hand). Problem 3's hand on A called wrong for "it looks like a jug" (the skeptics split; A is a jug, so the page concedes the hand in words, as decided). Problem 2's "no better" on the swap (the skeptics split; I took it as real because the beta has its own moment with no hand and the Matching entry teaches the swap).
- Answered as decided: Problem 7's "Does the order matter?" now has one answer in Next, although the skeptics found no contradiction.
- Dropped, both skeptics against: Problem 2's Crux and rival, Problem 3's route with a right foot on B and its move 2, Problem 4's load on C, Problem 5's foot 5 and foot 2, Problem 8's backstep and moves 1 and 3. Most came from a drawing rule on folded knees or from a private model, and several proposed wordings would themselves have been false.

**Shoulds.** Taken where they met the test or were cheap and plainly right with no added line. All of Problem 1's went in. The largest is Problem 4's crux, which now states the turn on flat C. I changed two reviewers' wordings because my own scan contradicted them: Problem 2's "buys you nothing" (the gaston does shorten the flight, so "you pay twice" stays) and Problem 5's "only D above it" (D is at or below the shoulder by the catch).

**Figures changed.** Problem 2 (D is `h=5`, on both figures), Problem 4 (right thigh, so B shows whole), Problem 5 (left shin foreshortened, dots on the legs, tag A) and Problem 8 (tag B with no leader). All went through `warn()` at the three sizes. Problem 5 is clean at all three. Problem 4's small climber is short of D, as the note says. Problem 2's and 8's poses didn't change. I looked at each, and the `drawn` hashes are copied in. The alt text still holds for all of them.

**Text.** Short sentences and few commas. The first build spilled six Entries lines, so I cut words: Problem 3's caption, Problem 5's "the old start edge", Problem 6's move 1, Problem 7's caption sentence (moved into Next) and part of Problem 8's Wrong. No `k:` changed and no space closed up. "What to try next." and the gap between notes stay.

**Layout.** Lowest text on the answer pages: 766, 777, 779, 777, 770, 771, 775 and 777 pt. No answer page has a full line to spare. The book stays at 289 pages and `tools/check_fit.py` passes. `tools/check_alt.py` says nothing about the changed figures. It still lists `reading-hold-orientation.svg` and `reading-worked-problem.svg`, as it did before this round.

**Web edition.** Built with 0 warnings. I checked that the new wording reaches the page but didn't open it in a browser this round.

**Not checked.** The Boox, including Problem 2's thinner D and its lip, Problem 3's marks on A and E, Problem 4's new D and Problem 1's C. Nobody has climbed any of this. The friction, swing and load arguments are a model's figures and judgement.

**Words.** 9,161 before this round, 9,230 after.

**Last recheck: Problem 8's citation.** The recheck of Problem 8 left one must, under test (e). Next's sentence on the backstep cited B42, Rowland's article on the reverse flag. That article says nothing about a backstep's outside edge or foothold size, and its only comparison on lock is that the flag costs more upper-body effort than a backstep. I read both live pages. B44 says footholds can be too high or sometimes too small for a backstep, and it contrasts the reverse flag's inside edge with the outside edge, so the sentence now cites B44. `research/factcheck-2.md` had already moved the same claim to B44 in Chapter 4. The cost in lock is about this problem's beta alone. B44 doesn't speak to it because it never mentions toe hooks, and under the rule above it needs no "(judgement)". Only the key changed, in the chapter and the brief. B42 is still cited in Chapter 4. The book stays at 289 pages, the page's lowest text stays at 777 pt and `tools/check_fit.py` passes. The page still prints [100], which now points at the Complete Guidelines. The web edition wasn't rebuilt for this.

## For Simon to decide

None of it blocks. The decisions below were made so the work could finish, and each can be overruled.
- Problem 3 keeps the heel lesson and the page concedes the right hand on A in Next. Right hand first may be the easier order. Making it the beta needs a new figure and tags A R1, C L2, D R3, E R4 L5.
- Problem 7 keeps the printed order and figure, and Next answers the prompt. Making the foot-first order the beta needs a new figure, which could also move the palms in to (∓20, 198). V5 may be low for the printed order, on unmeasured shoulder figures.
- Problem 8 keeps the toe and concedes the heel. A as drawn matches the heel row of the book's own table, so the toe stands by ruling. The flag and backstep have the same door at the same rise, so the page's preference rests on the book's entries.
- Problem 4's move 5 leads with a lock-off and offers the deadpoint. A reviewer wants them the other way round, on a model's figure.
- "What to try next." or "On a real wall."
- The half line between notes, or `gap(0.6)`.
- `sit-start.svg` panel b has the reversed right foot that Problem 5 lost. `compression.svg` has the old shallow volume that Problem 7 lost. Their fixes belong in the main checkout.

