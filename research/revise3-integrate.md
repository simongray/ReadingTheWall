# Integration log for the third revision

## Findings from the mechanical, grade and claims checks

I checked each finding against the book, `research/REVISE-3.md`, `research/evidence-3.md` and the dossiers. I also re-read F11, D13 and D38 on 2026-11-06, and they say what the claims check reports. `build.sh` now exits 0 with no warnings: 268 PDF pages, the same as edition 2, and all 85 fitted texts take the pages estimated. No `k:` changed, and `template.typ` is untouched.

### Layout and typography

- **Jumping to a foothold:** the stray page is gone. The grade note and summary lost two runt lines by joining a sentence and dropping "so that", and the entry fits one page.
- **Sloper filmstrip:** back between the V3 head and the Sloper entry. A local `show pagebreak: none` stops the strip from stranding the head, so the template needs no change. Sloper now takes three pages (two before), and the book's total still holds at 268.
- **Watch strings, chapters 4 and 5:** typographic quotes and apostrophes, and an en dash in place of the fullwidth hyphen. The fallback font Klee no longer appears in the PDF.
- **Index:** "the setter’s brief" now has a typographic apostrophe.

### Chapter 1

- **Static and dynamic:** the energy saving is attributed to one gym owner's article (D13).

### Chapter 2

- **Heading:** "Why reading pays off" becomes "Why read first", since the study below it found no change in reaching the top.
- **Rests:** knee bars and heel hooks are for harder problems.
- **Hold table, jug row:** "arm straight on steep ground".
- **They avoid ladders:** easier problems get matches and crosses, and sometimes an easy heel hook or dyno, as the dossier says.
- **When to change the beta:** the three-attempts line now says how it fits the four-to-six rule.

### Chapter 3

- **Precise footwork:** the first-session advice is labelled as the book's suggestion, V2–V3 as judgement, and A44 now supports only "at V3".
- **Drills for quiet feet:** only the first three drills go in the warm-up.
- **Front-pointing:** the note says V1, to match the badge.

### Chapter 4

- **Weight shift, Matching:** the coach-training notes no longer read the syllabus as a learning order.
- **Straight arms:** step 4 starts with "Later".
- **Barn door:** the note says to start with fixes 1 and 4 at V1. Fix 3 and fix 5 say when they come. The slab drill is now fix 1 only, which is what B35 covers. The grade check proposed fixes 1 and 2, but fix 2 is the V2 foot swap.
- **Turning the hip in:** the note opens with "Try it from V1".
- **Side flag:** step gives V3 and V4 for the two other flags.
- **Drop knee:** the summary no longer defines the entry by the deep form.
- **Lock-off:** the symptom loses the unsourced "would cost less".
- **Compression:** the tall note attributes the ape-index claim to Lattice's client data and points to the 2007 study that disagrees.

### Chapter 5

- **Jug:** the grade note and step 4 limit straight-arm hanging to steep walls. The pump symptom is attributed to the German school lessons.
- **Half crimp:** the habit warning is labelled as the book's suggestion.
- **Mantle:** the note now supports the V2 badge and carries the heel-hook warning.
- **Using the thumb:** the note opens with "Look for the thumb spot from your first crimps".
- **Full-crimp box:** it says the book's half crimp sits at the top of Schweizer's range, and labels "What to do" as the book's suggestion.

### Chapter 6

- **Opening, Static or dynamic?:** the energy claims are attributed to D38 and D13. "Apart from a few practice goes low on big holds" reconciles big jumps with learning the dyno from V2.
- **Deadpoint:** the note opens with "Try small ones from V2 on big holds". The tall note drops "by V5", which D13 doesn't say, and labels the rest. The small note says "judgement; see" instead of "has the evidence". Step 6 lost its runt line to make room for the note.
- **One-handed dyno:** the tall note restores the dossier's "(judgement)".

### Chapter 7

- **Volumes:** the note dates the squeezes and hooks to V4 and the knee bar to V5, and the reading box does the same.
- **Traverses:** "On steep sections, keep your arms straight".
- **Overhangs:** gentle overhangs "become common" from V2, since V0 and V1 already have slight ones.

### Chapter 8

- **Opening:** the max-hang numbers are averages across men and women.
- **VB–V0:** the Lattice advice is one post on fingerboard training, with a pointer to the coaches who differ. Bent arms say that coaches blame them. The "first few sessions" claim is attributed to one blog (F48).
- **V1:** more moves depend on a weight shift. The square-on fix says that square on suits most vertical walls.
- **V2:** overhangs "become common". Small deadpoints join the practice list. The reading list says "from V3" for the backstep.
- **V3:** the 19 kg average is explained instead of "many V3 climbers can't add that".
- **V4:** "By now, momentum is a normal tool".
- **V4 to V5:** the body-tension cell no longer says "Helps" for a technique badged V3.
- **V5:** the Remember item says "Be ready for the odd" move. The chunks bullet says what F11 says and that it doesn't show that previews help. The paddle dyno is now named here.
- **V6:** the old V6 placement of the paddle dyno is gone. Finger strength as a limiter is labelled judgement.
- **V7, V8+:** "weeks" and "seasons" are labelled judgement. The V8 client is reported as a claim from Lattice, which sells plans.

### Chapter 9

- **Climbing tall:** "Its effect on your grade is less clear" replaces the flat claim. Tall problems start from about V3–V4, now that sit starts are V3. Scrunchy moves use a backstep or a partial drop knee.
- **Climbing small:** the heading and opening no longer overclaim. Heel hooks "caused the most injuries in its study". Big jumps are labelled as the book's suggestion instead of citing the shoulder study.
- **Climbing heavier:** says the shoulder study didn't separate small deadpoints from big jumps.
- **Starting as an adult:** the warm-up figure says it can't show that warming up helps. The run-in head says "some coaches". The keypoint says what the app study measured and whose priority "skill first" is.
- **Learning technique:** a full crimp isn't repeated, and jumps build up slowly.
- **Falling:** the climbers "described" an uncontrolled fall.

### Appendices

- **Card:** "closer to a steep wall", as in chapter 1. It still fits its page.
- **Glossary, open hand:** "far less load … than a crimp", not "the least".
- **Troubleshooting:** the door row adds the back flag and the traverse row adds the side flag, so the first flag named suits the lowest grade. To keep the door row at four lines, "Or turn in" takes the table's usual colon and "Or use your other hand" is shorter. The pump row says that coaches blame bent arms.

### Other files

- **Front matter:** adds a line for readers newer than V2, and says "start to matter" as the guides do.
- **`research/KEYS.md`:** now matches the 73 entries. Seven merged keys are out, three missing keys are in, and thumb-catch is renamed.

### Words

`wc -w` over `book/chapters/*.typ`: 61,311 before this pass, 61,688 after, and 58,879 at HEAD. Most of the growth comes from attributions and from learn-earlier notes the book lacked. Chapter 9 now stands at 6,988, which supersedes the 6,751 in its log.

| File | Before this pass | After |
|---|---|---|
| 00-front | 1329 | 1344 |
| 01-movement | 1868 | 1873 |
| 02-reading | 4218 | 4235 |
| 03-feet | 7501 | 7522 |
| 04-body | 9405 | 9443 |
| 05-hands | 7147 | 7248 |
| 06-dynamic | 7519 | 7543 |
| 07-terrain | 4768 | 4800 |
| 08-grades | 5861 | 5920 |
| 09-considerations | 6922 | 6988 |
| a-card | 340 | 341 |
| a-glossary | 2430 | 2433 |
| a-troubleshooting | 1289 | 1284 |

### Rejected

- **Top-out opening line:** the grade note and summary already cover the heel hook and send flat tops to Mantle.
- **"Big hollow shapes" in the Volumes summary:** an entry's summary defines the entry, and the gloss rule covers passing uses.
- **`lip` glossed twice in chapter 5:** the two glosses explain different senses.
- **Restoring the dropped aliases:** the names beside them in the A–Z cover the same lookups, and the brief requires only the absorbed names.
- **Another pass over the tall notes:** 35 is close to the brief's "roughly half", and the lunge note was restored on purpose.
- **Ten entries that list a source they never cite inline:** all ten were already like that at HEAD, and dropping a source needs a re-read of each.
- **A–Z line with one leader dot:** it looks fine at size.
- **"Start here" in chapter 6:** it tells a V4 reader where to start in the book and doesn't contradict the learn-earlier notes.
- **Body tension on caves and roofs:** "matters earlier" and big holds on low-grade roofs can both be true, so no reader is misled.
- **Lock-off pointer to the V4–V5 section:** Baker's view is attributed, and the entry's symptom already sends readers to the twist lock and the deadpoint.
- **G40 and the culture of thinness:** the brief keeps "Don't diet for grades" as it is.

### Not applied, because the files are outside this pass

- **`figtools/figs_concepts.py:39,45` and `figtools/figs_hands.py:591`:** the figures still print "arm hangs on bones", "straight arms: skeleton holds you" and "bent arms: forearms pump". The labels are confirmed, and they contradict ruling 9 and evidence item 9.
- **`research/H-sources.yml:31,54,123,182`:** straight quotes in titles, which print on the bibliography pages.
