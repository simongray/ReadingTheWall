# Revision brief for the next edition

This is the single source of truth for the revision that follows the second
edition. Simon, the editor, decided its scope on 2026-11-06. No new edition
has been named: never tag, run `release.sh` or publish, and don't commit.
Edit the working tree only.

## What Simon decided

**In scope**
- Correct the evidence problems listed below.
- Change the grades and the order of entries as listed below.
- Rewrite the prose where it reads as generated (see "Prose").
- Clear, natural language throughout. This is the goal for the prose. Word
  count matters too, so don't ignore it, but it isn't the end goal (see "Prose").
- Merge entries that belong together and remove repetition, because that serves
  the reader.
- Excellent typography, pretty on every page (see "Typography").
- Add worked readings to Chapter 2 (a separate brief covers them).
- Add a section "How this book was made" and make the credits agree.
- Add a few notes for small climbers, and delete tall-climber notes whose
  advice is obvious.
- Improve the hand close-ups and the top-down views.
- Add a kit for surveying real gym problems.
- Evidence line on each entry: only a prototype that is off by default.

**Out of scope, don't do these**
- Paying an illustrator. Named or paid reviewers. A human citation audit.
  Dated notes from the wall or per-entry "tested by" stamps.
- Item 5 of the analysis: no text-overlap check, no page about creators, no
  letters to coaches. When Simon said "ignore 5" he meant this item and nothing
  else. It says nothing about any other list that has a fifth item.
- Anything about selling the book. It will never be sold anywhere.
- Cutting the V7 and V8+ guides. They stay, with the same structure.

## Build on what works

Simon: the book does many things right, so the changes should build on that
foundation. This is a revision, neither a rewrite nor a redesign.

- **Keep** the structure of parts and chapters, the anatomy of an entry with its
  reading box and cross-links, the sourcing and the fact checks behind it, the
  honest labels such as "(judgement)", the plain second-person voice, the figure
  system and the typographic design.
- **Leave alone** a sentence, figure or layout that is already good. Change
  something only when this brief asks for it or when it has a real fault, and be
  able to name the fault. Rewording a good sentence for the sake of it is a
  mistake, even if the new one is also good.

## Rules for every editor

- Read `research/STYLE.md` first. British spelling, second person.
- Keep all markup working: `#tref`, `#jt`, `#ix`, `#src`, `sources:`,
  `related:`, labels such as `<grade-3>`, `#remember`, `#keypoint`,
  `#category-table`, `#grade-techniques`.
- Edit only the files you own. Use small `Edit` calls.
- Put previews and scratch files in the scratchpad given in your task, never
  in the project folder.
- Never invent a source, a number, a quotation or a video. If you have no
  source for a new claim, mark it "(judgement)" or "(this book's suggestion)".
- Never write in Simon's first person. Never add his exact height, age or
  weight anywhere in this repository.
- Quote at most a few words from any source.
- Word count matters, but it isn't the end goal. Clarity comes first, so a
  sentence may grow when it has to, which is the one exception to the
  `natural-phrasing` skill's advice on length. When two wordings are equally
  clear, take the shorter. Report each file's word count before and after
  (`wc -w`), and say why if a file grew.

## Grades, order and merges

Within a grade, entries go in the order given here, which follows what
depends on what. It is no longer alphabetical. `→` marks a changed grade.
Rewrite the `grade:` and `grade-note:` of every moved entry so the note
supports the new badge, and rename or re-sort the section heads as needed.

| Chapter | Grade | Entries in order |
|---|---|---|
| 03 feet | V0 | precise-footwork, edging |
| | V1 | front-pointing, smearing, high-step, rockover (→V1) |
| | V2 | pivoting, foot-swap, hand-foot-match (→V2) |
| | V3 | toe-pull, heel-hook (the heel-hook filmstrip stays just before it) |
| | V4 | toe-hook |
| | V5 | bicycle, heel-toe-cam, knee-bar |
| 04 body | V0 | weight-shift, straight-arms (→V0) |
| | V1 | frog, barn-door, matching, stemming (absorbs corner) |
| | V2 | hip-turn, flag, cross-through, layback |
| | V3 | backstep, back-flag, drop-knee (→V3, with its filmstrip), pre-loading, body-tension (→V3), lock-off (→V3), opposition, bumping |
| | V4 | twist-lock, inside-flag, compression (→V4) |
| 05 hands | V0 | jug |
| | V1 | sidepull |
| | V2 | half-crimp (→V2), open-hand, undercling, palming, mantle (absorbs volume-mantle) |
| | V3 | sloper (with its filmstrip), pinch, wrap, gaston (→V3), regrip |
| | V4 | pocket, thumb-catch (renamed "Using the thumb") |
| | V5 | full-crimp and its notebox |
| 06 dynamic | V3 | deadpoint (absorbs hip-pop), hip-pump, jump-start |
| | V4 | lunge, dyno (with its filmstrip), latching, cutting-loose (absorbs counter-kick), run-and-jump |
| | V5 | double-dyno, campus-move, foot-catch, pogo, comp-moves (new entry: absorbs lache, paddle-dyno, tic-tac, double-clutch) |
| 07 terrain | V2 | slab, volume, traverse (→V2), top-out (with its filmstrip) |
| | V3 | overhang, arete, sit-start (→V3) |
| | V4 | roof |
| | V5 | dynamic-slab |

Corner moves out of chapter 7 into Stemming in chapter 4. The wall-angle
table and the Vertical walls section in chapter 7 stay.

**Merged keys.** `book/key-alias.typ` maps these so that every `#tref` keeps
working: `corner`→`stemming`, `volume-mantle`→`mantle`, `hip-pop`→`deadpoint`,
`counter-kick`→`cutting-loose`, and `lache`, `paddle-dyno`, `tic-tac` and
`double-clutch`→`comp-moves`. The name of each absorbed entry becomes an alias
of the entry that holds it, so that it stays in the A–Z and the index. Keep
each absorbed entry's useful steps, cues, warnings, sources and videos, and
drop what repeats. Each merged entry should take no more pages than it can
justify. An absorbed entry's figure may stay as a second figure inside the
merged entry only if it teaches something the main figure doesn't.

**Competition moves.** `comp-moves` ("Competition set pieces", category
dynamic, grade 5) says in its grade note that these moves depend more on a
gym's setting style than on its grades. Give each move a short named part.
Say plainly that the names "tic-tac" and "double clutch" are loose: no
climbing source uses the first, and sources disagree on the second.

**Learning earlier than the badge.** The badge says where you start to need a
technique. Where you should start learning it earlier, say so at the start of
the grade note in plain words, e.g. "Learn it from V2 on big holds." Do this
for at least dyno (V2), double-dyno (V3), lunge (V3), run-and-jump (V3),
precise-footwork and straight-arms (first session), and deep versus partial
drop knees. Keep the warning against habitual full crimping where V1–V2
readers will see it (in half-crimp).

## Evidence corrections

`research/evidence-3.md` gives the checked facts and wording for each item.
Use it. These are the changes, by file:

**01-movement**
- Line 26: "coaches teach straight arms from the start" overstates B1, which
  is the second coaching workshop. Say "early".
- Line 28: straightening the arms to reduce pump is coaching advice. Say that
  coaches recommend it and that we found no study measuring it.

**02-reading**
- Line 17: retitle "Reading improves how you climb" to "Reading changes how
  you climb", and say the study used roped indoor routes.
- Line 184 and the keypoint at line 202: "your first try is your best chance"
  leaves the keypoint. Report it as a finding from World Cup finals, with
  the selection effect: climbers still trying after a failed attempt are
  those the problem suits least, and they rest very little. The four-to-six
  attempts rule stays as a rule of thumb (judgement).
- Line 186: delete the inference that most failed attempts end early. Failed
  attempts are shorter by definition.

**03-feet**
- Line 21: "about three foot moves for every hand move" is one how-to
  article's figure. Present it as a way to notice lazy feet, not a target.

**04-body**
- Straight arms errors: say that coaches warn about slack shoulders. It isn't
  measured.

**05-hands**
- The full-crimp box: add that we found no load figure for the half crimp.
  The model compares a crimp with an open grip.

**06-dynamic**
- Lines 29 and 81: replace "you weigh almost nothing" with what is true, that
  you are neither rising nor falling, so you feel almost weightless and
  the hold takes your weight only as you start to sink.
- Line 25: reconcile with chapter 9 line 73 (see below).

**08-grades** (also "when you weigh nothing" at line 185)
- Keep the forum reconstruction (F15) once, in "Technique or strength?" with
  its caveat. Delete it from the V4, V5, V6, V7 and V8+ guides.
- "The finger-strength gap between V4 and V5 is small" rests on Lattice's
  bands V1–V4 and V5–V7, which are too wide to show that step. Say so.
- Line 24: replace "you are in the middle of the pack" with what the data
  can support: self-reported figures from keen climbers, which give no reason
  to think a year without a V5 is slow.
- Line 14: add that the descriptions under "What problems look like" are
  judgement, not measurement.

**09-considerations**
- Lines 17 and 57: cite Mermier et al. directly (G3 is being changed to the
  paper).
- Lines 77–81: "Does weight cost you grades? At your level, hardly" overclaims.
  These studies compare different climbers at one moment, so they can't say
  what happens when one climber loses weight. Reviews differ, and a lower
  weight raises your strength relative to bodyweight by simple arithmetic.
  Say that nobody has tested this for climbers like you. Keep "Don't diet for
  grades" in full and keep the book's view, labelled as its view.
- Line 50 (knee box): add that these are injuries seen in clinics, so they
  show what hurts people, not how risky each move is.
- Line 73: reconcile with chapter 6 line 25. Small deadpoints are fine and
  often cost less. Save big jumps and fast catches on small holds for moves
  that need them.
- Line 142: say that the gentle protocol tested in G28 ("Abrahangs") is
  associated with a co-author of the paper, and that the study is
  retrospective, from app logs.
- Line 171: external focus. A 2024 analysis that corrected for publication
  bias found the average advantage close to zero. Present the cue as
  something to try.

**Rulings on points flagged in `research/evidence-3.md` and `research/H-small.md`.**
These settle them for the editors. Simon can overrule any of them later.
- Item 3: keep "small to nil", the authors' own summary, over "close to zero".
- Item 8: drop the superlatives about weight loss, as the wording there does.
- Item 9: "one physiotherapist warns" replaces "coaches warn", since it is one
  source. "Hang on your skeleton" stays as the coaches' figure of speech, in the
  chapter 1 heading and as an alias. Chapter 1 gives the physiotherapist's
  correction once. Elsewhere, reword a line only if it states as mechanism that
  the bones take the load in place of the muscles.
- Item 12: use the wording there. It removes the "so" in the wording above,
  because being neither rising nor falling isn't what makes you feel light.
- Item 15: "early" is labelled this book's suggestion.
- Keypoint at `09-considerations.typ:147`: the dose of two or three sessions is
  this book's cautious suggestion. Say so, and say the study's gentle group logged
  at least three a week.
- Small climbers: use the nine notes in `H-small.md` section 1, the "Climbing
  small" section in chapter 9, kept to about the length of a page, and the doubled
  box in chapter 2. Simon can take the section or the box out.

## Prose

Simon's notes on why the text reads as generated:
- 36% of sentences have eight words or fewer, and runs of them read staccato.
- "Big hollow shape" and other glosses repeat in every entry.
- "Look for" and "Symptom" repeat on nearly 400 lines.
- Tall notes appear on most entries, some of them filler.

Simon's goal is clear and natural language. Word count matters, but it isn't the
end goal: judge a sentence first by how it reads, then by whether it could say
the same in fewer words.

Rules:
- **Rhythm.** In running text, join sentences that belong together, using
  because, so, when, while or which, and vary the length. Say it the way a
  coach would say it out loud. Numbered steps stay short and imperative.
- **Natural phrasing.** Fix passive voice that hides who acts, inverted or
  stacked clauses, comma chains, habitual ", and" joins and fragments. Don't
  trade one tic for another, and don't add "just", "simply" or "note that".
- **Contrast tic.** Cut ", not X" and "rather than X" where the contrast adds
  nothing the sentence hasn't already said.
- **No flourishes.** No motivational lines, and no sentence that exists only
  for rhythm.
- **Glosses.** Explain a jargon word in parentheses once per chapter, at its
  first use. After that, keep the `#jt(...)` link, which gives a dotted
  underline to the glossary, and drop the parenthesis.
- **Look for and symptoms.** In `when:`, group the bullets under two bold
  labels, and put any other bullet (Choose, Check first, Rule of thumb) in the
  list where it reads best, keeping its bold label:

  ```typst
  when: [
    *Look for*
    - a foothold out to one side of your body.
    - a slab or a vertical wall. Nearly every move there starts with a shift.

    *Symptoms*
    - Your foot skates or bangs onto the hold as you stand on it #src("B22").
    - You stand up on both feet at once while your hands pull hard.
  ],
  ```

  Bullets under "Look for" continue the phrase, in lower case. Bullets under
  "Symptoms" are full sentences. Do the same for any `*Look for*` or
  `*Symptom:*` list outside an entry.

In chapters 1 and 2, go through every sentence and rewrite those that read
staccato or awkwardly, keeping those that already read well. Every other chapter
gets a lighter pass over its running text, summaries and grade notes. Don't change
a fact, a citation or a step's meaning while doing this.

## Tall and small climbers

**Delete a `tall:` note** when its advice is obvious or applies to anyone:
restating that long limbs reach further, "a tall body weighs more" with no
action to take, or a note that only repeats the entry. **Keep it** when it
has a safety point, a source, or an action a tall climber wouldn't guess.
Report what you deleted. Aim for roughly half of the current 59.

**Add a `small:` note** (rendered as "Small climbers.") on a few entries only,
where something specific and useful can be said. `research/H-small.md` lists
the candidates and their sources. Don't add one to every entry, and don't write
a note that only mirrors a tall note.

## Typography

Simon's instruction: the book must have excellent typography and look pretty
throughout. White space is applied intelligently, following the usual norms
of book typography. It is not something to eliminate to lower the page count.

- **Page count is not a target.** Never reduce type size, leading, margins or
  the space around headings, figures and boxes to save pages. A longer, better
  looking book beats a shorter, cramped one.
- **White space has a job.** It groups what belongs together and separates
  what doesn't: more space above a heading than below it, a caption close to
  its figure, and a generous chapter opening. An entry may start on a new page
  when that reads best. A page that ends short at the end of an entry or
  chapter is normal; what looks wrong is a stray line or two alone on a page.
- **The usual faults are bugs.** No widows or orphans, no heading stranded at
  the foot of a page, no figure parted from the text it explains when it could
  stay with it, no table split without a repeated header, no rivers in
  justified text, and no line that overflows the measure.
- **Consistency.** The same element gets the same size, weight and spacing
  everywhere, on a consistent vertical rhythm.
- **Details.** Proper dashes and quotation marks, non-breaking spaces in
  "V5", "p. 12" and measurements, old-style figures in running text and lining
  figures where the template already sets them in tables.

The design stays: the typeface, the type scale, the page and the ornaments are
the foundation, and the work is to fix faults and refine. Editors keep this in
mind when they add or move content: don't place two figures so they fight for a
page, don't cut good space to make something fit, and don't add or lower a `k:`
in an entry. Report any entry that spills instead. A dedicated pass over the
rendered pages comes after the content settles.

## What each editor returns

Log what you changed at `research/revise3-<your file>.md`, one line per section.
Then return the structured result your task asks for, including changelog lines:
- **Errata** are mistakes the previous edition made. Write them as
  `p. N, Place: what was wrong → what it says now`, using edition 2's printed
  page numbers. To find a page, search the scratchpad's `ed2.txt`, the text of
  edition 2 with one form feed per PDF page; printed numbers appear in each
  page's footer.
- **Changed** lines are anything else a reader of edition 2 should know.

## Figure faults to fix in the figure pass

- **Undercling in `hand-atlas`:** Simon reports that the hold looks inverted, and the code agrees. `atlas_undercling()` in `figtools/figs_hands.py` draws a wedge whose underside drops toward the wall, so the fingers would slide off instead of hooking behind a lip. `HOLD_PROFILES["undercling"]` in `climb.py` has it the right way round, with the underside rising from the tip to a hollow. Reshape the flake to match that profile and re-pose the hand, since `H.snap` and `on_edge` follow the outline. Keep `fill=DARK` with an outline. Do this after any change to the hand's proportions. Tell Simon when it's done.
- **Other atlas tiles:** check each hold in `hand-atlas` and `foot-atlas` against its entry and its `HOLD_PROFILES` shape. Only the undercling has been examined so far.
