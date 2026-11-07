# Typography changes for the third revision

The brief is the section "Typography" in `REVISE-3.md`. Most faults had one root: the template saved pages by tightening entries, floating figures and letting boxes fill the page around them. Taking that away cleared most of the fault list, and the book went from 290 to 317 pages with no blanks. A second pass then fixed what a page-by-page reading of the result found, which brought it to 311, and a third brought it to 313. The sections below record each pass, the merge with the third edition's figure work and the repairs after it.

## The first pass, measured against the book before this work

| Measure | Before | After the first pass |
|---|---|---|
| Pages | 290 | 317 |
| Texts set with tightened space | 18 | 0 |
| Word gaps at 1.6× or more, narrow columns | 61 | 2 |
| Word gaps at 2× or more, narrow columns | 13 | 0 |
| Word gaps at 1.6× or more, full measure | 17 | 7 |
| Word gaps at 2× or more, full measure | 1 | 0 |
| Tight lines (under 0.68×) | 12 | 8 |
| Line-end hyphens | 112 | 23 |
| Page feet 8 or more lines short inside a text | 3 | 52 |
| The same, 14 or more lines | 2 | 16 |
| Index marks, cross-references, citations, heads | 744, 1,066, 2,284, 270 | the same |
| List numbers in the body | 736 | identical |

The short page feet are the cost. Nearly all are an entry's first page ending after its steps, with the figure or box at the top of the next page.

## The template (`book/template.typ`)

- **No tightening.** Removed `fit-space`, `fit-pages`, `spaced`, `page-estimate`, `part-waste`, `kgap`, `space-k` and every `k`, because they traded white space for fit. Every text now sets at full space.
- **No page sharing.** Removed the `flow` experiment (`page-flow`, `flow-share`, `entry-gap`, `need-space`), which the book doesn't use and the code above depended on.
- **Wide figures in flow.** A wide figure follows the steps instead of floating, so an entry's order never changes: steps, figure, parts, box, mistakes, notes, apparatus. This ends the reading box split around a figure.
- **Running figures in flow.** `float-figure` became `figure-block`, a whole block with a line of space around it. This ends figures inside lists and tables, and figures that parted a sentence.
- **Reading box whole.** The box never breaks now, so the stretched grey fill and its split lists are gone. It takes `title:` and `icon:`, and "Is this move meant to be dynamic?" uses them, so that box gets the reading box's shade.
- **Other long boxes.** A box that may break repeats its title on the next page through `grid.header`, tested with a forced split. Aside icons are fixed at 7 mm.
- **Apparatus whole.** The apparatus never breaks, and the last mistake, note or box stays with it, which ends stray apparatus lines on a page of their own.
- **Parts.** A part may break between its steps and its figure, which ends figure-only pages two-thirds empty.
- **Lists.** Up to three short items stay whole; longer lists keep two items together at each end (`keep-list`).
- **Step columns.** The column beside a figure is ragged, since narrow justified columns opened rivers. It ends after the step that makes the whole lowest, and the rest go on at full measure with their numbers.
- **Text blocks fill the measure.** Summaries, grade notes, tall and small notes, answer notes and list blocks get `width: 100%`, because an auto-width block justifies only to its widest line and its right edge wandered.
- **Captions.** Captions are ragged and stay inside the measure beside a hanging figure. A panel mark stays with the next word (`tie-marks`). The caption beside a narrow figure is flush left, not centred.
- **Section heads.** A head needs room for itself and five lines. The hanging indent sits on an explicit `par`, and the h2 rule reads the head's own counter.
- **Subheads.** Level 4 heads have half a line below, so a head sits the same distance from a list and a paragraph.
- **Tables.** Rows never split. Up to six rows stay whole, and longer tables keep two rows together at each end and repeat the header. The first row of a long table is tagged as a header in the PDF, which I accepted.
- **Grades in tables.** `badge-plain` is a capital V with lining figures, since "V0" read as "vo" in small caps.
- **Empty grade tables.** `grade-techniques` emits nothing when no technique is listed.
- **Lead-ins.** A paragraph ending in ":" keeps six lines of room under it through a strut, and `check_fit` fails the build if one still ends a page. The bold-only paragraph rule never fired, so it went, and three labels use a new `lead-label` macro instead.
- **Paragraphs in entries.** Paragraphs have half a line between them, so "Hop.", "Slide" and "Drill:" no longer run together.
- **Line breaks.** A citation binds to the word before it with a word joiner. Ranges and the listed compounds are boxed, and `Chapter N`, `Font N` and measurements take non-breaking spaces.
- **Justification.** `justification-limits` allows tracking from −0.01 to 0.015 em. Ragged text no longer hyphenates.
- **Figures in type.** `A1`–`A5` and bare Font grades take lining figures. A spaced hyphen becomes a spaced en dash.
- **Page references.** A page reference stays in regular weight inside a bold run-in.
- **Alias line.** The category under an entry's title is a box, so "hands and / holds" no longer breaks.
- **Watch line.** The number beside a Watch link uses `grade-tab-inline`, so the line keeps its height.
- **Answer pages.** The answer's head sits inside the left column, so the figure rises beside it. All reading figures hang to the head rule, which ends the jumping right edge across the run. This holds each answer on its page with no squeezing and no wording change.
- **Marks.** `reading-question`, `reading-answer` and film strips leave metadata marks for `check_fit`.

## Reference matter

- **Columns.** `balanced-columns` evens the columns of the last page of the Index, the A–Z and the Glossary. It also starts the last page a page earlier when both pages' items fit, because an early pass could leave two entries on a page of their own.
- **Index.** Turnovers are at 2 em, the first page number binds to the word before it, a parent head stays with its first sub-entry and two lines stay together at each end of a letter.
- **A–Z.** The page box is 2 em wide, for three-digit folios.
- **Glossary.** `gloss` sets its hanging indent on an explicit `par`. `glossary-columns` splits the entries for balancing, and the website has its own version.
- **Sources.** An entry never breaks across columns.
- **Contents.** Part III starts p. xi, so Chapter 8 no longer breaks across two pages. Chapter numbers take lining figures, and the section number column is wider, since "2.10" crowded its title.

## Numbering

- **Arabic 1 on Chapter 1.** The Part I divider is now the last unnumbered page of the front matter, so arabic 1 falls on physical p. 13 with no page added. Odd folios fall on recto, and each question has its answer on the back of the leaf.
- **The rule to keep.** Arabic 1 must be physically odd. If the front matter ever has an even number of pages, number from the Part I divider instead. `check_fit` fails the build otherwise.
- **Parity before Problem 1.** No forced breaks: moving three figures in the source put Problem 1 on physical p. 33 with no blank.

## Chapters

- **Barn door figure** (`01-movement`) moved after its list, **the worked-problem strip** (`02-reading`) after Step 5's list, and **Figure 7** after the next paragraph. Each closed a large hole in running text.
- **Part II subtitle** (`main.typ`) is tied so that it breaks after the comma.
- **Foreword.** The signature has a line of space above it (layout only).
- **Colophon** aligns with the body's left edge.
- **Two-line heads** 2.6, 4.2, 4.4, 5.4 and 5.5 are tied so they don't end on "and" or "for".
- **3.2's lead-in** stays with its table through `lead-in`, because the head and one line were left at the foot of a page.
- **V3 and V8** keep "Physical side" and "Why people stall here" together through `keep-together`, so the second page matches V6 and V7 instead of holding one short section.
- **Chapter 9's end** keeps "Practise falling" and the key point together, since the key point stood alone on the last page.
- **Warming up table.** `1. Pulse` and the like became `1.~Pulse`, because they parsed as lists and collapsed a column.
- **Terrain table** gives its second column more room, so "Your weight and hips" stays on one line.
- **Limiter table** in From V4 to V5 is rebalanced to 1.1, 1, 1.1.
- **Grade guides' tables** have a fixed Category column, so the column stays put from guide to guide.

## Figures (`figtools/`)

- **Grid-dot crumbs.** `Fig.svg` drops a bolt hole when an edge, a stroke, a label or the frame cuts it (one library change). It removes about 1,900 dots across 66 figures, nearly all of them already half hidden. I compared figures before and after and saw no gap in the grid. Text and page layout don't change.
- **Figure 12** has gaps of 3.3 mm instead of 5, so it fits the measure and lines up with the box under it. The drawings keep their size.
- **Problem 7's answer** has A as a boxed tag, like the other tags.
- **`book/figure-alt.toml`.** I refreshed `drawn` only for figures whose description was current and which changed in these ways, and no description needed a change. The 23 already listed by `check_alt` before this work stay listed.

## Tools and website

- **`tools/check_fit.py` checks something else now.** It used to compare each text's pages with the template's estimate, and that estimate is gone. It now reads the finished PDF and fails the build on the faults in its docstring, and it reports thin pages, holes and wide word gaps. The file keeps its name, so `build.sh` doesn't change. It needs Poppler.
- **`website/template.typ`.** Added `src` without the word joiner, `title:` and `icon:` on `readbox`, and versions of `glossary-columns`, `lead-label`, `lead-in` and `keep-together`. The old pass-throughs stay, since older editions still call them.

## Wording changes

- `04-body`: "pinch (p. N)-shaped feature" → "pinch-shaped feature", because a page reference can't sit inside a compound. The link stays.
- `05-hands`: "On a Sloper (p. N):" → "On a sloper (p. N):", to match the other run-ins.
- `00-front`, "The checks": "chapters 2, 3, 6 and 7", "chapter 1" and "chapters 4, 5, 8 and 9" → "Chapters" and "Chapter", as elsewhere in the book. This isn't in the Foreword.
- `grade-techniques`: "None listed." is gone from V6, V7 and V8.

No wording changed to make something fit a page.

## Decided against

- **`gap(0.6)` between the notes on answer pages.** I kept the half line, `gap(0.5)`. I couldn't tell them apart at reading size, it is the book's list spacing and `gap(0.6)` overflows Problem 4.
- **Whole-box exceptions by position.** Never splitting a reading box costs no more pages than splitting it above some hole size, and it needs no position logic.
- **0.6 tightening for deadpoint and mantle.** Breaking a part before its figure cures what the tightening was for.
- **Scaling Pocket, High step, Pogo and Smearing to fit under their steps.** It would leave those climbers smaller than the rest. The second pass cropped or narrowed them instead.
- **Ragged tail on a cut step list.** I compared Edging and Problem 2 both ways. The difference is small, and full-measure steps are justified everywhere else.
- **"Referenced from" at full measure under the QR codes.** It added a page and didn't read better than the column beside them.
- **Forced breaks before 2.10 and 2.11.** They left two pages about 30 lines short, and moving figures did the same job.
- **A global runt cost.** It adds loose lines. The second pass measured this again: at 300% the lines over 1.45× went from 6 to 21 and over 1.7× from 0 to 8, for five fewer runts. Ragged text takes the cost instead.

## Second pass: faults found reading the rendered pages

A reading of all 317 pages listed about 125 faults. All of them are fixed here unless "Left alone" says otherwise. No space around a head, figure or box got smaller, and no type size, leading or margin changed. The only space taken out is the excess between a drawing and its caption, which the rules ask for.

| Measure, pp. 1–264 | Before this pass | Now |
|---|---|---|
| Pages in the book | 317 | 311 |
| Body lines with word gaps under 0.72× the median | 12 | 0 |
| Body lines over 1.45× | 10 | 6 |
| Body lines over 1.7× | 1 | 0 |
| Narrowest and widest mean word gap, body lines | 1.90 and 5.49 pt | 2.29 and 5.04 pt |
| Hyphens at line ends, narrow ragged columns | 32 | 0 |
| Hyphens at line ends, justified lines | 0 | 33 |
| One- or two-word last lines under a full line | 102 | 51 |
| Citations broken across lines | 19 | 0 |

`check_fit` reports 0 faults and 10 notes. The notes are short section ends and short last pages of entries. Index marks, cross-references, citations and heads stay at 744, 1,066, 2,284 and 270.

### The template

- **Citations.** `src` boxes a group of up to four numbers, so it never breaks. A longer group, as in a Sources line, may still break after a comma.
- **Section heads.** The hanging indent measured the number at body size, because a `set` inside a `context` doesn't reach `measure` there. It now measures at the head's size, which corrects every two-line head.
- **List numbers.** `step-number` sets the number bold and flush right in a box 0.9 em wide. A long list is set in parts (`keep-list`), and each part used to size its column by its own figures, so the text edge jogged by up to 1.3 pt. Plain lists now take the same bold number, so the book has one style. No list reaches ten items; the function widens the box if one does.
- **Justification.** Word spaces now run from 82% to 130%, and hyphenation costs 40%. Typst was hyphenating no justified line at all, because a hyphen cost it more than a stretched line. The result is 33 hyphens in 264 pages, never two in a row.
- **Ragged text.** `ragged` sets optimized line breaks with a high runt cost. Captions, reading boxes, key points, step columns, apparatus, tables, Five-things boxes, grade notes and Common mistakes all use it. The last two were justified and short, so justifying them only opened gaps; they now match the reading box above them.
- **Step columns.** They no longer hyphenate.
- **Captions.** One gap, `caption-gap`, a line under the drawing. A caption's block used to add the paragraph spacing on top, so the gap changed with the context and came out at 21, 15 or 13 pt. The space below a caption is unchanged, so it now reads as part of its figure.
- **Lead-in lines.** `lead-label` and the new `lead-line` bring the list up close under them. The list's own space above used to win, which left the line floating between the two.
- **Run-in heads.** `run-in` sets a head flush left with half a line above, and stays a paragraph so the next paragraph keeps its indent.
- **Common mistakes.** With a list of up to four and nothing after it but the apparatus, every item now stays with the next, so the last can't go over alone.
- **Apparatus.** A reading box straight above it closes the entry, so the apparatus drops its own rule. A page reference is tied to the name before it in ragged text, and "V5 (Font 6C/6C+)" stays whole. Heads tied for their own line breaks are untied here, which was why these lines broke short.
- **Page references in justified text.** They stay free to break, against the fault list's advice. In a test, tying them there left two lines over 1.7× (the widest at 6.43 pt) where there are now none, since a name and page have to move as one.
- **Doubled parentheses.** `tref(..., inner: true)` sets "(Compression, p. 125)". All 17 use it.
- **Entry head.** When the other names and the category don't fit on one line, the category takes a line of its own and the dot goes.
- **`foot-free` and `after-figure`.** These are two new `technique` options, and the website's template takes both. `foot-free` lets the last note stay on its page when a box follows the entry. `after-figure` sets paragraphs straight after a wide figure.
- **Part titles.** The block is 90% wide. Part I is tied to break after "works".
- **Running head.** It sets its own paragraph spacing. The A–Z's last page began inside the A–Z's rule, which moved the head down 1.45 pt on that one page.
- **Measurements.** "seconds" and "minutes" take non-breaking spaces, and the words "Section" and "Figure" no longer hyphenate.

### Reference matter

- **A–Z.** Two rows stay together at each end of a letter, as in the index. A page number stays with its leader, and a target name never breaks.
- **Index.** A head stays whole with up to four sub-entries. A longer group keeps two together at each end and repeats its head at the top of a column, through `grid.header`. A reader who sees one page at a time can't see the head on the page before. An earlier attempt with "(continued)" read positions from the layout and didn't settle within Typst's five passes.
- **Sources.** The columns now sit in a block of a set height, which Typst shares out over the pages, so the last page's columns are even. `pages` and `last` in `10-appendices.typ` have to be given by hand, since working them out from the layout doesn't settle either. `check_fit` fails the build if the block drops a source and notes uneven columns.
- **URLs.** A DOI's link text doesn't start with "http", so the old rule skipped it and Typst broke it anywhere. All links in Sources now break only after `/ . - _ ? = &` or a `%20`, and a tail under seven characters stays with the piece before it. This also ends the one line that ran off the page.
- **Glossary.** "3, 4, 5" in the Font grade entry takes lining figures.

### Chapters

- **1.5 and 2.3** start new pages. 2.3 now has its sentence, table and Figure 7 on one page. Its key point moved after the figure, since the table announced by "This table" came second otherwise. This moved no words.
- **2.3's table** has a narrower Faces column, so both long head cells fit on one line. I kept the labels.
- **Flashing and Projecting** use `run-in`.
- **Heel hook and Smearing** set their variants as separate paragraphs. Smearing's go after the figure.
- **5.1**'s "German school" paragraph splits before "The same lessons", with no change of words, so the lead-in and its list stay on one page.
- **Chapter 9**'s mats list may break (`loose-list`), which closes three short pages in a row.
- **The step table in Reading the wall for body position** sits closer to its step than to the next one.
- **Tables.** The foot table and the V4/V5 comparison have fixed columns, so the long cells set fewer lines. The comparison stayed whole then. Since the third pass it may break (8.6), and it runs over pp. 235–236.
- **On the mat.** The opening line is centred under the title.
- **Local fixes.** A few last words are tied (`new~problem`, `meet~them`). Five list items with an unbreakable tail are set ragged, since no break could close the gaps: Compression step 7, Opposition's "Foot against foot", "Keep the hips close" in Chapter 6, the hands-behind-you step in Chapter 9 and two bullets in the grade guides.

### Figures (`figtools/`)

- **Film strips.** A caption can say where it breaks with `\n`, and all the captions that broke badly now break by sense. The worked problem's strip has the standard gutter and a wider frame, at scale 0.245 against 0.28, so the climber clears the frame edges. It is the only strip at a smaller scale. The top-out strip's gutter is standard too, for 0.6 mm off each frame.
- **Figures kept with their steps.** Pocket, Deadpoint and Overhangs are now under 92 mm wide, so they sit beside their steps. High step, Mantle, One-handed dyno and Pogo lost blank wall from the top or foot. Mantle's low foothold moved up 28 cm for this, so its first panel's feet are closer together. Run-and-jump lost 5 mm of blank mat. None of them changed scale.
- **Blank feet.** Crossing hands, Opposition, Bumping, Back flag, Compression, Palming, Lâche, Paddle dyno and Dynamic slab lost the empty band at the foot, so their captions sit as close as the others'.
- **Key to the illustrations.** The rows are further apart, the left label is one right-aligned block, and the figure sits inside the measure.
- **Labels.** I moved the ones that touched a line or crowded a panel caption: Figure 6, Sitting into it, Twist lock, Inside flag, Sidepull, Counter-kick, One-handed dyno, Latching, Pogo, Campus move and Traverse.
- **Body tension.** Panel b's head is whole, and the wall stops short of the panel edge.
- **Figure 9** cuts all three panels at one height. **Figure 10**'s labels are regular weight.
- **Edging** has its panel letters.
- **`book/figure-alt.toml`.** I refreshed `drawn` for the 38 figures I changed, after reading each description against the drawing. 15 others stay listed by `check_alt`.

### Wording changes

- `03-feet`, Pulling with the toes caption: "(grey band)" → "(shaded band)". The band is pink in colour, and captions never name a colour.
- Watch titles: the episode number and double space are gone from the six Gresham videos, since the number clashed with the black tab beside it. "Greshams" stays, as the video's published title.

### Left alone

- **Table head labels** weren't shortened. The columns changed instead.
- **Lists in the grade guides** stay justified apart from the bullets above. Word spacing no longer calls for more.
- **Single-word last lines in justified text** remain where tying them opened a worse line, such as "coaches:".
- **Side captions** still start a little left of the bolt holes in some figures, since the caption aligns with the image's edge.
- **None of this has been read on the Boox.**

## Third pass: faults from reading the rendered pages

This pass worked through the fault list by class. The book goes from 311 to 313 pages, and `check_fit` reports 0 faults and 11 notes.

| Measure, body pages | Before this pass | Now |
|---|---|---|
| Line-end hyphens | 42 | 12 |
| Full-measure lines with word gaps over 4.2 pt (normal is about 3 pt) | 20 | 2 |
| Names, page marks, grades and hold marks parted at a line end, or a dash starting a line | 76 | 2 |

The last two are the words "straight arms" as ordinary text, in Layback's caption and in a troubleshooting cell, not references.

### The template

- **Ragged lists.** Every list is ragged now, not only the steps beside a figure. This one rule removed the six `par(justify: false)` patches and the loose lines they were covering. It also ends hyphenated last words such as "sec-/onds" and "sur-/face". A list can gain a line, since ragged text can't shrink its spaces.
- **Ragged summaries.** An entry's summary is ragged like the grade note under it, since a stretched line shows most at that size. A citation tied to its word caused most of the loose lines there.
- **Compounds.** Ragged text no longer breaks a compound at its hyphen (`keep-compounds`).
- **Short names.** In ragged text a name of up to 22 characters stays whole with its page, so tables and apparatus break at their commas. This uses no-break spaces, because Typst weighs a ragged line by its spaces and a line of boxes comes out uneven.
- **Grades in Referenced from.** "V3 (Font 6A/6A+)" stays whole in a box. The old rule split the text and lost the lining figure in "Font 5+".
- **Small caps.** Digits leave the small-cap features and take lining figures at 0.8 em, since "V0" read as "VO" and "V1" as "VI". This covers labels, table heads and figure numbers.
- **Captions.** A film strip's caption shrinks to its text and centres under the strip. So does the caption of a figure wider than the 130 mm limit. `fig` takes `caption-width`, which Figure 9 uses to set its caption in two lines.
- **Apparatus.** The last block before the apparatus stays with it only when the apparatus is under 120 pt, about nine lines. A taller one can stand alone at the top of a page, where it drops its rule. Four entries now do this.
- **Mistakes.** Up to four mistakes stay whole with their label, whatever follows them.
- **Climber notes.** A note never breaks across pages. The tall note stays with the small note when both are there.
- **Lead paragraphs.** A paragraph that opens a list of steps stays with its first steps (`keep-leads`). Hip pop now starts its own page.
- **`closing-box`.** This replaces `foot-free`, and the website's template takes it too. Precise footwork's drills now come before its apparatus, so the apparatus closes the entry as elsewhere.
- **`after-figure`** no longer breaks.
- **Glossary.** Entries use `ragged` and sit further apart, at 1.15 em.
- **Tables.** `data-table` rows have 7 pt above and below instead of 5 pt, so the rows of multi-line tables read apart. The short generated tables keep theirs.
- **Spaced dashes** take a no-break space before them, so a dash never starts a line.
- **Glossed terms** don't hyphenate, which keeps their dotted underline in one piece.
- **Reading pages.** `tie-holds` keeps a hold's mark with the word before it, so "2." can't start a line.
- **Sources.** The columns start a gap below the opening text, like the other reference openers. URLs and DOIs take lining figures. A show rule drops the comma the citation style leaves before a year or after a title ending in "?" or "!".
- **Columns.** `balanced-columns` takes a `margin`: none for the A–Z, 1.3 lines for the Index and one line for the Glossary. The columns of the last page now end within 3 pt in the A–Z (58 pt before), 61 pt in the Index (86 pt before) and 33 pt in the Glossary.
- **Section 8.11** takes the grade-guide head through its label `<progression-map>`. I didn't use a `grade` label, because the website makes a guide page from those.

### Chapters

- **2.3.** "A hold that faces the wrong way..." now follows the figure and stays with the key point, so 2.3 closes on the next page with both.
- **2.5.** "Climbers often find..." moved up to follow the section's first paragraph, with no change of words. The move in 2.3 pushed Chapter 2 two lines over, onto a page of its own and a blank. This takes the two lines back without tightening anything, and the chapter now falls into whole sections on most pages.
- **2.10.** The key point breaks at its sentence.
- **Pulling with the toes.** The drill moved after the figure, so the figure stays with its steps.
- **8.6.** The note on the table's sources now stands with the lead-in above the table. The table may break, with its header repeated and two rows over.
- **9.6.** The mats list no longer needs `loose-list`, so that macro is gone. "found~that:" is tied.
- **Case.** 149 references that follow "a", "the" or a similar word now print in lower case, such as "a sidepull (p. 131)".
- **Short ties.** Seven troubleshooting cells have their last two words tied. The one-sentence paragraph after the injuries table is ragged, since either fix for its "in-/juries" left a loose line.

### Figures (`figtools/`)

- **Label size.** "right foot free" and "crux: cross" are at the standard 7.5 pt.
- **Moved labels.** Precise footwork's note is beside its mark, in two lines, and the panel lost its blank foot. "push" in Toe hook, "pull" in Bicycle, "elbow to ribs" in Twist lock, "fingers round the edge" in Wrapping, "leg nearly straight" in Pogo and "feet swing off" in Roofs have clear air now. "between leg and wall" in Inside flag is in two lines, clear of the foothold. "kick across behind" in Counter-kick is one line under the kick's path.
- **Half crimp.** Panel b's forearm and wall run down as far as panel a's.
- **Jumping to a foothold.** The close-up uses the blank 11 mm beside it, so the panel hangs into the margin like the figures around it.
- **`book/figure-alt.toml`.** I refreshed `drawn` for these 13 figures after reading each description against the drawing. None needed new words.

### Wording changes

- `02-reading`, Step 7: "Ask yourself: what movement is this problem testing?" → "Ask yourself what movement this problem is testing." The old line could only break inside "problem" or leave "testing?" alone. This is the one sentence reworded, so Simon may want to look at it.

### Left for Simon

- **Straight arms.** The box misses the first page by about 23 pt, which is two lines of copy. The content is settled, so I left it. The page ends at 65%.
- **Twist lock.** The figure can't come back to the steps, since panel b fills its height and trimming wouldn't gain 19 mm. Setting the figure before "How to do it" would give two full pages, but it changes the entry's order. It stays as a loose run of three pages.
- **Bicycle.** I compared both by eye. With the box on the first page, eight lines of references stand alone on the next and read as a stray, and the same test on Matching hands looked no better. So the split stays, with steps on one page and box and references on the next, as in High step and Rockover.
- **Mantle.** Its figure misses the first page by one line (16 pt). The mistakes, the note and the apparatus now sit together, so the box doesn't need to break, and it stays whole.
- **Heights set by hand.** The `margin` values and Sources' `pages` and `last` may need changing if the reference matter changes.
- **Still not read on the Boox.**

## The merge with the third edition

- **Hands.** The old hand figures are gone, so the crops and label moves made on them were redone on the outlines in `figtools/authored.py`. Pocket fits in the 92 mm beside its steps, Hold angle stops just below the wrist, "fingers round the edge" in Wrapping clears the arête's line and "2–3 cm above" in Latching clears its panel letter.
- **Citations [56] and [57]** swap throughout, with Sources in step. Sources are numbered in order of first citation, and the move in 2.5 (third pass) now cites "Climbers often find..." first.
- **"Is this move meant to be dynamic?"** has the reading box's marks instead of round bullets, since it became a `readbox` with `title:` and `icon:` in the first pass.

## After the merge: repairs

A reading of the merged book and site listed these faults. The book stays at 313 pages, and every change stays on its own page: the pages that differ are PDF 2, 5, 22, 30, 34, 38, 42, 46, 55, 59, 64, 75, 82, 84, 114, 127, 132, 138, 144, 151, 156, 160, 162, 166, 170, 183, 189, 190, 194, 201, 216, 223, 227, 247, 259 and 271. `check_fit` reports 0 faults and the same 11 notes.

### The template and the chapters

- **Ranges with a unit.** "10–25 / minutes" broke in the rest table, because the box that keeps a range whole hid its last digit from the measurement rule. The range rule now ties a following unit itself.
- **"Chapter" doesn't hyphenate,** as "Section" and "Figure" don't, since "Chap-/ter 2" opened 5.1.
- **Bold run-ins.** A page reference inside `*...*` printed bold, because `text(weight: "regular")` can't undo strong's weight delta. The two run-ins with one ("Not on a slab", "On a sloper") end the bold before the reference, with the same words.
- **Case.** Ten references the third pass missed are in lower case: lock-off twice, undercling, stemming, smearing, half crimp, open hand, sidepull, body tension, run-and-jump and latching.
- **"The grey box" → "The shaded box"** in "How to use this book", since the text never names a tone.
- **Ties.** "a~bicycle" ends the colophon, and "A~2024" in 9.6 no longer leaves "A" at a line end.
- **Watch line.** Mantle's video title has a spaced hyphen, which prints as an en dash like the other titles, instead of an em dash.
- **Heel hook rock-up** (content correction). The strip draws the hips moving towards the heel but not over it, so frame 3 says "hips towards the heel" and the caption "up and across towards the foot". Re-posing would need new left footholds.

### Figures (`figtools/`)

These drawings changed, so their alt text should be rechecked: reading-worked-problem, reading-v4-sit-answer, reading-v5-volumes-answer, reading-v3-overhang-answer, reading-v2-slab-answer, precise-footwork, front-pointing, filmstrip-heel-hook, heel-toe-cam, bicycle, twist-lock, pinch, wrap, hip-pump, dyno, filmstrip-dyno, overhang, volume and sit-start. I read each description against its drawing, and none needed new words.

- **Figure 6.** L4 and R5 sat on the crux box's lines, and the "rest" leader grazed R3's tag. The tags moved off the lines and the leader runs below the tag to the jug's lower edge.
- **Problem 5.** "C R1" covered the right wrist, so it moved onto the wall beside hold C. B's leader stopped on the torso; it now reaches B's hidden outline.
- **Problem 7.** The A tag lay across the left thigh, and the legs and tape leave no room for it by the hold. It is on open wall above the thigh, with a leader to the hold, as in Problem 5.
- **Problems 1 and 3.** "D R3" and "C L1" touched the arm and hand, so they moved about 1 mm clear.
- **Precise footwork.** "lands short, slips" sat on the shin, because the frame pushed the centred first line left. Both lines now end at the panel's right side.
- **Front-pointing.** The leader ended on the "b" of "back", for the same reason. The label's end now sits at its anchor and the leader leaves from the "k".
- **Heel–toe cam.** The volume's corner was cut off at the measure. The frame is 6 cm wider, so the figure hangs into the margin beside the steps, as Knee bar does.
- **Bicycle.** "push" moved 2 cm off the wall line.
- **Twist lock.** "elbow to ribs" ran past the panel edge, so the frame pushed it under its own leader and onto a bolt hole. It is in two lines, and "feet squeeze" moved off its arrow.
- **Pinch.** The panel letters stood on the wall line, so the band above the wall is a little deeper. The drawings keep their size.
- **Wrapping.** "fingers round the edge" touched the arête's line, so it is in three lines.
- **Hip pump.** The label and steps say straight arms, but the dip's elbows were at 147° and 140°. The dip's hips are 3 cm lower, so the arms hang straight.
- **Dyno and its strip.** The sink is labelled "arms straight" but was drawn at about 142°, and the drive bent to 122°. The sink's shoulders sit lower and further out (about 172°) and the drive's further back (155–160°, "nearly straight" as step 5 says).
- **Overhangs.** Panel a's climber lay on the wall line and hid it. The body now hangs off the wall between the hand and the low foot. The X is off the wall line, "feet cut loose" sits in two lines beside its arrow instead of on the plumb line, and panel b's "arms straight" leader ends on the arm's near edge.
- **Volumes.** Panel a's elbows went through the wall. The hands are a little lower and the climber stands further out, with the arms still bent.
- **Sit starts.** Panel a's caption "square on (frog)" marked the frog as the mistake, which step 3 recommends. It is "square on, bottom out".
- **Ghosts in the dark copies.** `Climber.draw` marks a ghost's white pieces (`data-ghost`), and `website/dark.py` turns marked pieces into the page. The count of outlines it relied on broke when the real body's lines came between a ghost's outlines and its fills, which left white ghosts in Dynamic slab, the falling strip, Roofs, Run-and-jump and Figure 1. Print ignores the mark.
- **`book/figure-alt.toml`.** `drawn` is current for all figures. Besides those above, this covers the figures changed by the hands work and the ghost mark, after reading each description against its drawing.

### The website

- **Tied heads.** A part subtitle or a section head tied for print reached the site as no-break spaces, and a tied run too wide for a phone broke inside a word. The site turns them into spaces in heads and subtitles, which also clears the part pages' descriptions and `llms.txt`. The mid-word sweep at 320–430 px now matches the site before the merge, in Iowan and Georgia.
- **2.10's key point** runs on as one paragraph instead of a `<br>`. Print keeps its break.
- **Zero-width spaces** in the repository's address are dropped, so copied text and search match it.
- **Sources line.** A long citation group may wrap, as in print. On Deadpoint it widened the page to 359 px at 320 px.
- **Grades in tables and the A–Z** are a capital V with lining figures, as in print, since "V0" read as "vo".
- **The Foreword's signature** has a line of space above it, as in print.
- **Spacing.** A level-4 head has half a line below it and paragraphs in an entry are half a line apart, the values print uses.

### Left for Simon

- **Top-out palms.** The words promise flat palms, but the hands stand on end and dip into the block. Mantle's flat palm needs the hands lifted about 3.5 cm with the body, so that the fists end at the palm. The left foot then misses its hold and the right shoe overlaps the right palm. I drew a first sample but didn't apply it, since a change to a hand waits for Simon.
- **Tones in the key.** Figure 1's caption and key still say "white" ("the right limbs white", "The white lip"). Whether white counts as a tone is Simon's call.
- **Hold angle.** Panels b and c end at the heel of the hand with no wrist. Showing a wrist in all three adds about 5 mm and moves a line of p. 127 over.
