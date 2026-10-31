# Final read: appendices

Read pages 230–258 of the draft PDF and the source of the four appendix files. Checked with `typst compile … read-app.pdf`: no `[?`.

## Changes

### 10-appendices.typ

- Removed the six `#chapter-end()` calls (now a no-op). Pages rendered pixel-identical before and after.

### a-troubleshooting.typ

- `ttable`: rows no longer split across pages. The volume row in "Holds" was split between two pages.
- `ttable`: no hyphenation in the narrow ragged cells ("con-trol", "se-quence", "in-termediate" broken across a dotted underline).
- Sway row: "your hips zig-zag" → "your hips zig-zag on steep ground". Ch. 4 (Weight shift) teaches zig-zag hips as correct. Added a link to Overhangs, the entry that lists the error.
- Cutting-loose row: "Tense your back to stop the swing" → "Don't fight the swing on the way out. At its peak, tense your stomach…", as the entry says.
- Toe-hook row: added "If it still pops, clamp the hold with both feet: Bicycle". The Bicycle entry lists a popping toe hook as its symptom.
- Sloper row: "Flag a foot" → "Keep one foot low", as the Sloper entry says.
- Glossary links added: downturned shoes, core, centre of gravity, bailed, pumpy, shake out, intermediate holds.

### a-glossary.typ

- centre of gravity: now matches Ch. 1 ("Standing upright, it sits in your pelvis, near your navel").
- circuit: "covers a range of grades" → "covering one grade or a range of two or three" (Ch. 2, grade appendix).
- feature: unexplained slang '"on" for every problem' → "usually count for every problem" (Ch. 2's wording).
- Font grade: the scale list now starts at 3 (grade table, Ch. 2), and the entry names the Grade conversion appendix.
- off foot: "not standing on a hold" → "not carrying you" (Ch. 4, Ch. 8).
- positive hold: "faces you" → "faces up or tilts back into the wall" (Ch. 5). "Faces you" broke the hold-direction convention.
- training board: "Kilter or Tension board" → "Kilter Board or Tension Board".
- volume: reference form "A big hollow shape bolted to the wall, usually a pyramid or wedge."

### a-grades.typ

- Heading labelled `<grade-conversion>`. The heading is unnumbered, so `@grade-conversion` fails to compile ("cannot reference heading without numbering"). Link to it with `#link(<grade-conversion>)[…]`.
- V-scale linked to the glossary at first use.
- "The BMC's example" → "The British Mountaineering Council's example".

## Handed back: index and A–Z

- 03-feet, heel-hook alias "Heelhook": make it lower case ("heelhook").
- 03-feet, hand–foot match alias "hand-foot match": drop it. It is the entry name with a hyphen instead of an en dash.
- "outside edging" is an alias of both Edging (03-feet) and Backstep (04-body:466), so the index and the A–Z each list it twice. Drop it from Backstep.
- "keeping feet on" (03-feet, toe-pull) and "keeping your feet on" (04-body, body-tension) are near-duplicates that point to different entries. Keep one.
- 07-terrain, volume alias "features" sits next to the glossary's "feature" in the index and points somewhere else. Drop the alias, or file "feature" under Volumes in `ix-merge`.
- Some heads print in lower case although the chapters capitalise their sub-entries: fingerboard (05, 08, 09), pulley (05), tendon (09), core (01, 03), max hang (08), crux (02), edge (05), beta (02), campus board (09), friction (03). The head takes the glossary's spelling. Either make `make-index` prefer a capitalised sub-entry head, or add a capitalised `#ix` on the main page.
- Missing chapter pages: `#ix("Babyboxer")`, `#ix("ACL")` and `#ix("BMI")` in 09-considerations (the landing steps, the falls/knee text and the RED-S box), and `#ix("Momentum")` in 01-movement ("Static and dynamic"). The index points only to the glossary or to Ch. 6.
- Template, `a-to-z`: the sort uses `lower()` rather than `ix-fold`, so "Hand–foot match" files after "handle" and "Heel–toe cam" after "Heelhook". The en dash sorts after the letters.

## Handed back: sources (research/*-sources.yml, src-map)

- Listed twice: A19/B56, A21/C34, A22/B58, B30/C4, E34/G48, E58/F24, B4 (=F28)/C44. Probably also A43/F35 (one course, two URLs) and A44/F44 (one forum thread).
- C42 prints as "(zfs.bildung.hessen.de): Praxis Griffarten." and G56 as "Boulderzentrum Schwaben (rockerei): …". The organisation names are parsed as personal names and part of each is dropped. Both are `type: report`, so their URLs don't print either.
- E17: truncated title "Training to ... Part 3".
- D41: "Lattice Training: Lattice Training | How to: Train for Bouldering". The author is repeated in the title.
- Site suffixes after "|" in titles: E1, E2, E30, E41, B52, D42.
- E48: title "Gym route setting??".
- Climbing magazine appears as "Climbing", as "Climbing.com" or with no author (A4–A16 and G30/G59 vs B30, C3–C9, D5–D8, F14, F43).
- Titles keep straight quotes and apostrophes ('Tight to the Wall', "Off Foot", Climber's).

## Noted, not changed

- Glossary MCL: "frog positions with the knee twisted" has no support in the chapters (Ch. 4 names only the drop knee).
- Glossary incut: "Incuts are easier than they look" appears nowhere else.
- Glossary dab, highball and macro define words the book never uses, although the intro says "used in this book".
