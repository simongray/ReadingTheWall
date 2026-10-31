# Streamline log: 08-grades, 09-considerations, appendices

Words (wc -w on the .typ files), before → after:

| File | Before | After |
|---|---|---|
| 08-grades.typ | 6425 | 5848 |
| 09-considerations.typ | 5576 | 5215 |
| a-troubleshooting.typ | 1271 | 1260 |
| a-glossary.typ | 2419 | 2260 |
| a-grades.typ | 484 | 400 |

Full book: 222 → 213 pages at the time of the last compile (all four editors' cuts combined). No `[?` references.

## 08-grades

- **Intro.** Merged the two opening paragraphs. Cut the indoor-grade explanation to one sentence plus a pointer to Chapter 2 (its home). Cut the badge definition that the front matter already gives.
- **Within-chapter repeats of Lattice's progress data.** The years-to-grade figures (5.8/8.6/9.7 years, and 3.8 vs 13 years for under-25s vs over-40s) appeared in the notebox, the V4→V5 age notes, "How long it takes" and the V8 guide. Kept them in the notebox only. Cut the "How long it takes" subsection (everything in it repeated the notebox). The V8 "stall" now points back to the box.
- **VB–V0.** Cut the Focus bullet on straight arms (repeated the Techniques paragraph and the remember box). The fear-of-falling fix and the tall-climber low-start note now point to Chapter 9 (home for falling and tall climbers).
- **V1–V3.** Removed the hold-direction explanation (Chapter 1 is its home), keeping the concrete cue. Cut the V2 undercling reading bullet (it repeated the Techniques sentence). Cut the clinic quote at V3 and the Bouldering Project quotes at V4 and V8 (they named grade labels, not technique).
- **Prose now agrees with the badges.** The "Techniques that start to matter" paragraphs named techniques badged at other grades. Moved them: foot-swap V1→V2, pinch out of V1 into V3, gaston V3→V4, compression V4→V5, pogo/double-clutch/knee-bar V6→V5, roof and run-and-jump out of V5 (both V4). Added frog to V1 to match the map.
- **Progression map.** Every `#tref` in it was checked against the `grade:` fields in 03–07. All rows matched except V7, which listed latching (badge V4) as if new. That row now reads "No new techniques; precise latching, hooks and compression". Shortened the map's intro.
- **V4→V5.** Cut the repeated F9 plateau sentence. Cut the "small errors" item (a platitude with a long attribution). Folded the "short steep problems" item (F43) into plan step 5. Cut the forum line on V6 gaps (F46) here, since it appears at V5 and V6. Cut the keypoint box, which restated remember item 1. "Finger training is outside this book" was wrong: it now points to @cons-adult. Remember item 4 now reads "rather than locking off" instead of "never lock off", which contradicted the lock-off entry. Item 3 now says "off foot", the term used in the text.
- **Notes for you.** The height notes on cramped problems and hip mobility repeated Chapter 9, so they became a pointer to @cons-tall. The duplicate F2 age figure went, and so did two of the three body-mass studies (F10, F17), which made the same point as Chapter 9. Kept F18, the relative-strength calculation, the age data on training hours and strength loss, and the 51-year-old example.
- **V5.** Cut the problem description that restated the V4/V5 table. The reading list now points to "Reading V5 problems" instead of repeating the swing and body-position bullets. "That is an estimate" became "(an estimate)" throughout.
- **V6–V8.** Cut "V6 is 7A, the first grade with a 7" (the heading gives Font 7A). Merged the duplicated "weak styles" and "other gyms" Focus bullets. The V8 physical side no longer repeats the years-climbing figure. Fixed the ambiguous "that test" so it names the weighted pull-up test.
- All ten `#remember` boxes still have five points, and all `<grade-N>` labels and `#grade-techniques(N)` calls remain.

## 09-considerations

- **Intro.** Cut the unused "Coaches' view" label explanation and merged the reader description into one sentence.
- **Climbing tall.** Cut the Lattice arm-span line (a third source for the same point). Cut the spotting bullet from "Where height hurts" (the Spotting section covers it). Cut "Don't hug the wall" (Hooper, G64 = B48): it isn't tall-specific, and Chapter 1 ("Hips and the wall") and the V4→V5 section already cover it. Folded the high-step how-to into "Skip high footholds" with links to the high-step and rockover entries (their home). Shortened the sit-start caption, which repeated the step.
- **Mobility.** Turned three stacked "You need…" sentences into one list sentence. Fixed `#jt("hamstrings")`, which linked to no entry.
- **Heavier.** Merged the three generic footwork steps into one with a pointer to precise-footwork. The climb-down step now points to @cons-falling instead of repeating the G14 statistic. Trimmed the second meniscus definition to two words.
- **Adult / injuries.** Merged the "two pictures" explanation into the table's intro. Replaced the DAV 89%/46% figures in the injury table with a summary (the full figures are in the falling section). Cut the second "campus board doubled injury odds" mention. Shortened the attributions in the finger-training and recovery paragraphs (Torr, Randall). Kept Hörst and MacLeod by name, since the reader owns training books.
- **Learning.** Removed the duplicate G43 citation. Cut "experts read better from the ground" and the step-by-step reading routine in the flash block (Chapter 2 is home), leaving a pointer. Cut the line about watching tall and short climbers, which repeats "Copy positions". Moved the beta gloss into the drills table.
- **Falling.** Merged the ACL and ligament definitions. Cut the BMC poster line (a second source for the DAV rule). Resolved "use the marked holds" vs "any holds you like". Cut "most injuries happen on good mats", which repeated the 94% bullet. Tightened the spotting paragraphs and the fall-roll caption. Every safety instruction and number stayed.

## Appendices

- **Troubleshooting.** Tightened the intro. Fixed `#jt("pumped")` to link to "pump". Added a pointer to @cons-tall on the scrunched row. The rows were already terse.
- **Grade conversion.** Cut the provenance chain (UIAA, Rockfax, theCrag) to its citation. Merged the "first V5 in a Font gym" caveat into the first caveat and corrected it to "From V3 to V5". Cut the IRCRA caveat (nothing a gym climber meets). Cut the circuit bullets that repeated Chapter 2 ("ask the staff", "grade yourself per gym") and kept the "treat a circuit as a range" advice plus a pointer.
- **Glossary.**
  - Merged true duplicates into one-line "Another name for…" entries: spot/spotter → spotting, fingerboard → hangboard, dual texture → dual-tex.
  - Deleted "link", which duplicated link-up and had no links to it.
  - Deleted five entries too obvious for a reader a year in, none of them linked by `#jt`: chalk, foothold, grade, hold and mat.
  - Shortened about a dozen definitions to one or two sentences.
  - Added four short entries for terms that chapters link with `#jt` but had no entry: campus board (06, 09), Font scale (02), pumped (07), RED-S (09).
  - Every `#jt` term in the book now has an entry.

## Repeats left in place on purpose

- The `#remember` boxes restate each band's Focus bullets. That is their job, and the brief says to keep them.
- Each band's "Physical side" keeps its own max-hang figure and a short definition, so every grade guide still reads on its own.
- The "Find your limiter" table in 08 overlaps the troubleshooting appendix. It is a V5 plateau diagnosis (finger strength vs technique), and plateaus live in Chapter 8.
- Chapter 9 keeps the full tall-climber advice (sit starts, scrunchy problems), the knee-injury study (G9) and the landing technique, because it is their home. Other chapters repeat them and should point here: the tall notes in 03/05/07, Chapter 2's "Reading for a tall body" box, and the bailing and landing advice in 06's mistakes lists.
