# Streamlining pass: kill your darlings

The book is nearly finished. Your job is to make it leaner and sharper
without losing anything a reader would miss. The reader asked for this
pass explicitly: eliminate fluff, repetition, and things too obvious to
include. The whole book should end up under 200 A4 pages (it is a little
over now), and it should read faster everywhere.

The reader: an adult starter, tall and heavier than average, climbing
indoor boulders for about a year, solid at V3, most V4s, no V5 yet. They are not an expert at those
grades: they are still learning technique there, so lower-grade material
is not "obvious" to them. They own training books and want concrete
technique and route-reading help, in natural, succinct English.

The aim is to cut words that carry nothing (padding, repeats, platitudes),
not to cut content. A cut is right only if the reader loses nothing they
would want.

## What to cut

- **Repetition across the book.** The same idea explained in several
  entries or chapters (straight arms, hips over feet, "turn the hip in",
  how to fall, why indoor grades vary, the hold-direction rule). Keep the
  best explanation in the place a reader would look for it, and replace
  the others with a short `#tref("key")` or a pointer ("see Chapter 1").
  Use `grep` across `book/chapters/` to find repeats outside your chapters.
- **Repetition inside an entry.** Mistakes that only negate a how-to step
  ("Not turning the hip in" right after the step "Turn the hip in"), a
  summary that the first step repeats, a "when to use" bullet that restates
  the summary, a caption that repeats the steps.
- **Generic filler, not technique.** Platitudes that teach nothing
  specific: "chalk your hands", "have fun", "try hard", "practise makes
  perfect", "everyone is different", "listen to your body" with nothing
  concrete attached. This is NOT a licence to cut beginner or intermediate
  technique. The reader is still learning the V0–V4 techniques and wants
  them explained properly: keep every technique entry, how-to step, "Look
  for" and "Symptom" cue at every grade, including the basic ones. If in
  doubt whether something is "too basic", keep it.
- **Fluff.** Meta-commentary ("This section explains…", "It is worth
  noting that…", "As we saw earlier…"), throat-clearing openings,
  motivational lines, hedges stacked on hedges, cute or clever phrases,
  tics repeated across entries, "simply", "just", "really", "very".
- **Over-detailed evidence.** Long attributions in the prose ("According
  to a 2021 article by X on the Y blog, which surveyed…") when a citation
  number carries the source. Keep the claim, its number and its citation;
  keep the name only when the reader benefits (a well-known coach, a
  study). Keep one example where three make the same point.
- **Generic notes.** "Tall climbers" notes that would apply to anyone;
  grade notes longer than two lines; "Watch" lists longer than two items.

## What to keep

- Every concrete instruction, every "Look for" and "Symptom" cue that is
  specific, every safety warning, every number with its citation, and
  every claim the reader couldn't easily guess.
- All cross-references and markup: `#tref`, `#jt`, `#ix`, `#src`,
  `sources:`, `related:`, labels such as `<grade-3>` and `<troubleshooting>`,
  `#remember` boxes (but tighten their wording if needed), `#category-table`,
  `#grade-techniques`. Never remove a technique entry or a key.
- The plain-language rules in `research/STYLE.md`: explain jargon at
  first use per entry or section (a few words), short sentences, active
  voice. Don't strip a jargon explanation to save words.
- Figures and figure code are out of scope. Captions may be shortened.

## Sentence rules (from the reader's own style guide)

- Read each sentence aloud; if a coach wouldn't say it that way, rewrite
  it. No fragments for punch, no odd word order.
- Split a long sentence only where two thoughts meet; don't chop for a
  word count. Past about 30 words a sentence almost always needs it.
- A paragraph that is only a list should be a real list, or shorter.
- Mark an example with "e.g." in the sentence it illustrates.
- No counts that drift ("fourteen problems" → "a dozen-odd problems" only
  if the number doesn't matter).
- One word, one meaning: don't use a technique's name loosely for
  something else.
- Don't make the rewrite longer. Each edited passage should be as short
  or shorter than before.

## How to work

1. Read every chapter you own in full before cutting anything, and skim
   the others' headings so you know what lives where.
2. Edit in place with small `Edit` calls. Don't rewrite whole files with
   `Write`; other editors may touch the same files.
3. After each chapter, compile a standalone preview (see `STYLE.md`,
   "Compiling your chapter") to make sure nothing broke, and check that no
   `#tref` key or label you touched went missing.
4. Log what you cut at `research/streamline-<your chapters>.md`: per
   section, a line on what went and why (not every word).
5. Report: words before and after per chapter (`wc -w` on the .typ files
   is fine as a proxy), the biggest cuts, and any repeats you left in
   place on purpose.

## Where each topic lives (so two editors never both cut the same thing)

Four editors work in parallel on different chapters. When the same
explanation appears in your chapter and in another one, cut it from your
chapter only if its home below is NOT your chapter, and leave a short
pointer (`#tref("key")` or "see Chapter N"). If your chapter is the home,
keep the full explanation.

| Topic | Home |
|---|---|
| Mechanics: centre of gravity, straight arms, hips and the wall, direction of pull, rotation/barn door, static vs dynamic, tension | Chapter 1 (01-movement) |
| How to read a problem, setter intent, flash vs project, rest between attempts, indoor grade variation | Chapter 2 (02-reading) |
| How to do a technique and when to use it | That technique's own entry |
| What problems look like at a grade, what to focus on there, plateaus | Chapter 8 (08-grades) |
| Tall/heavier/adult-onset climbers, injuries, warm-up, learning, falling | Chapter 9 (09-considerations) |
| Definitions of jargon | The glossary (keep the few-word explanation at first use in each entry; cut longer re-definitions) |
| Symptom → fix lists | The troubleshooting appendix (other chapters keep their "Symptom:" bullets) |

Other editors may be editing figure captions in the same files while you
work: always use small `Edit` calls and re-read the region first.
