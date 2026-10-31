# Typography notes

How the book is set, so the design can be kept up. The rules behind it,
with their reasons, are in `typography-principles.md`. Everything lives in
`book/template.typ`; the title page and colophon are in
`book/chapters/00-front.typ`, the appendix assembly in
`book/chapters/10-appendices.typ`.

## Typeface

- **Iowan Old Style** for everything, with its true small caps
  (`c2sc` + `smcp`), old-style and lining figures and real italic. The
  figure labels use it too (`FONT` in `figtools/climb.py`). Libertinus
  Serif fills in symbols Iowan lacks (→).
- Iowan reports its ascender as its cap height, so the text's top edge is
  set to the true cap height (0.7 em). Spaces between blocks then measure
  the white from a baseline to the next capitals, and boxes and tabs look
  centred.
- Old-style figures in running text; lining figures in tables, the
  contents, the A–Z, the index, the grade tabs and for grades (`V3`,
  `6A+`, via a regex show rule).
- Small caps, letterspaced: labels (How to do it, When to use it — reading
  the wall, Common mistakes, In motion, box titles, Grade, Step), the
  entry apparatus labels, table heads, the category, the running-head
  navigation, chapter and part labels, figure numbers.
- Italic: captions, the chapter in the running head, "Also called", key
  points, part titles.

## Type scale

One ratio, 1.2, from the 10.5 pt text size (`fs`). Reading and reference
matter take the half steps next to the text size, headings whole steps.

| Size | Used for |
|---|---|
| 8.75 pt | index, sources, "Scan to watch" |
| 9.6 pt | captions, tables, glossary, A–Z, entry apparatus, grade notes, running head |
| 10.5 pt | text, boxes, labels |
| 11.5 pt | entry summaries, key points |
| 12.6 pt | subheads (level 4) and method steps, bold; chapter and part labels; film-strip titles; index letters |
| 15.1 pt | the grade tab in an entry's title band |
| 18.1 pt | technique names, bold |
| 21.8 pt | sections, regular |
| 26.1 pt | grade guides; part titles |
| 31.4 pt | chapter titles |
| 45 pt | the title page |

## Page

- A4, margins 30 mm left and right, 25 mm head, 23 mm foot. The text block
  is 150 mm, about 90 characters, wide enough for a figure beside the
  steps. Wide figures, the running head and the multi-column reference
  matter use the outer frame, `overhang` (11 mm) into each margin.
- Running head: folio (bold), chapter (italic, shortened at a colon) and
  the navigation in small caps, with a light rule below. Chapter openings
  drop the chapter name; part pages have no head.

## Vertical space

- Text is 10.5/16.5. The unit of space is the line: `gap(n)` adds n empty
  lines to the normal line spacing.
- Paragraphs: an indent of 1.5 em, no extra space; flush after a head, list
  or box.
- List items +0.4 line; lists +0.5 above and below.
- Labels (How to do it, …) +1 above, +0.2 below; the list after a label
  follows it closely (`list-after-label`).
- Boxes, tables and figures +1 above and below; the entry title band +1
  below; the entry apparatus +1.5 above.
- Subheads +1.5 above, +0.35 below. Sections +2.5 above, +0.9 below; a
  grade section +2.5 below, a grade guide +2 below.
- Chapter openings are sunk 2 lines, with 3 lines between the ornament and
  the text. Heads, title bands, summaries and labels are sticky.

## Page breaks and fitting

- Chapters, grade guides, grade sections and technique entries start a
  page. An entry right after its grade section's head stays on that page
  (`entry-top`). Floats left over from an entry are set before the next
  one starts (`place.flush`).
- A film strip between two entries opens the page of the entry after it
  (`entries-running`); elsewhere it floats like a figure.
- A technique entry measures itself and is set with its spaces scaled
  down (to 0.6, 0.35 or 0.1 of normal, the most that works) when that saves
  a page it would otherwise spill a few lines onto. `fit-pages[...]` does
  the same for running text that starts at a fixed place: the grade guides
  in chapter 8 and the openings of chapters 4 and 6 are wrapped in it.
- Measured copies are marked by a style (`probe`, which sets the text
  region to "AQ"). In them `tref`, `navlink`, backlinks and the generated
  tables leave out links and real page numbers, and citations are
  stand-ins. A measured copy that refers to the document keeps the layout
  from converging.
- Page breaks that depend on where something ended on the page don't
  converge in Typst (tried both in a heading's show rule and before it), so
  short spills before a grade head are handled by fitting, not by
  skipping the break.
- A note box after an entry is kept whole, on a page of its own if need be.
  In running text a short one (under a third of a page) is kept whole and
  a long one may break.

## The grade

- One tab: white bold lining figures on black, proportions in em
  (`grade-tab`). Sizes: about 9 pt in running text (`badge`) and 15.1 pt
  in an entry's title band. The QR-code numbers use the same tab at 7.2 pt.
- The tab is a marker at the right end of the title band it marks, aligned
  on the heading's last baseline. Section heads and grade guides name
  their grade in the heading text and have no tab, which would only
  repeat it.
- In tables and lists the grade is set in small caps without a tab
  (`badge-plain`).

## Rules and ornament

- Two weights, horizontal only: heavy 1.2 pt, light 0.5 pt (`rule-heavy`,
  `rule-light`).
- Heavy: under an entry's title band; the top of every box and table.
- Light: under the running head; under a table's head; the foot of every
  box and table; above an entry's apparatus; the rules either side of an
  ornament.
- Boxes (`panel`): the reading box, note boxes, the remember box and key
  points share the rules, a 12 pt side inset and the space around them.
  Only the reading box is tinted (#eeeeee). Each has a small-caps label
  except the key point, which is italic at 11.5 pt.
- Tables: no row rules; rows are parted by a 5 pt inset. Chapter tables
  use the book's table style (no local strokes or sans heads).
- The ornaments are holds, drawn like the holds in the figures
  (`book/figures/ornament-<name>.svg`, from `ORNAMENTS` in
  `figtools/figs_cover.py`, set with `fleuron()` and `orn-rule()`). The
  title page has a chalked jug between two light rules; each part page has
  its part's hold, large; each chapter opening has its chapter's hold,
  small, between two 9 mm light rules under the title. The front matter and
  the appendix chapters share a quiet foothold, and chapters end without an
  ornament. The `ornaments` table in `book/template.typ` says which hold
  goes where and why.
- Each ornament is drawn at the height it is set at (12 pt on the title
  page, 24 pt on a part page, 5 mm at a chapter opening), so its lines have
  the figures' weights. All the ornaments of one place have that height,
  with the hold centred in it, and are as wide as the hold, so the rules
  beside them stay the same distance away.

## Aside icons

- Three asides of a technique entry have an icon beside their label
  (`book/figures/icon-<name>.svg`, from `ICONS` in
  `figtools/figs_icons.py`, set with `aside-icon()`; the `aside-icons`
  table in `book/template.typ` says which goes where). Each is drawn with
  the figures' own code and signs, for what its aside is about:
  - *Tall climbers*: the mannequin standing, seen from behind like the
    climbers in the figures, beside a dimension line from the floor to the
    top of its head, drawn the way the figures measure a distance.
  - *When to use it — reading the wall*: the mannequin's head looking up
    at a jug along the figures' dotted line of sight. Reading the wall
    means looking for the holds that call for the technique.
  - *Common mistakes*: a climbing shoe skating off a foothold, with the
    cross that marks the wrong way in the figures. The same cross marks
    each mistake in the list.
- The icon hangs in the left margin. Its right edge is 0.8 em from the
  text block (or from the edge of the reading box), and its middle is
  level with the label's lowercase. It takes no room, so the label stays
  flush left and the spaces and page breaks are the same as without it.
  The icons line up in one column down the margin, inside the outer frame
  (`overhang`).
- Like the ornaments, every icon is drawn at the height it is set at
  (7 mm, about one and a quarter lines), its drawing centred in it, with
  the pen's line weights, the figures' greys and holds drawn by `hold()`.
  The mannequin is drawn ten times larger and set down at the icon's size
  with its line weights scaled to match: at a few centimetres to the
  millimetre, the pen would thin a head to a few points. At that size only
  its outline reads, so the figure is drawn as one shape, without its
  inner lines or ears.
- The grade note has no icon: the grade tab sits just above it, and a
  second sign for the grade would compete with the tab. The apparatus
  (Related, Watch, Sources, Referenced from) has none either, since its
  rule already sets it off.
- `panel` and `notebox` take `icon:` too, for a note on the subject of an
  aside, e.g. `icon: "tall"`. No note uses it yet.

## Figures

- Figures keep the size they were drawn at. Narrow technique figures
  (≤ 92 mm) sit beside the steps; wider ones go below them as a top float
  inside a block that starts after the steps.
- Figures in running text and film strips float to the top of a page, but
  never above the head of their own section: when that head is on the same
  page, they go to the bottom if they fit. Narrow ones (< 80 mm) take
  their caption beside them.

## Reference matter

- Category tables: two columns at the start of each chapter.
- A–Z: two columns with dot leaders, grade in small caps, page.
- Sources: two columns at 8.75 pt. The access date, the same for every web
  page and stated in the introduction, is left out of the entries.
- Index: three columns, letter heads in bold 12.6 pt.

## Colophon

The back of the title page reads `book/edition.typ` (edition label, date,
commit), so a plain `typst compile` shows "Draft".

## The October 2026 redesign

The first design (195 pages) broke the principles in these ways; the
redesign (267 pages) fixes them.

- Sections (12.6 pt bold) were smaller than the technique names under them
  (15.1 pt), and a grade guide's head was barely bigger than its subheads.
- The space between blocks (6–11 pt) was hardly more than the 17 pt line
  pitch, so paragraphs, lists, boxes and footers ran together; list items
  were spaced like lines.
- Technique entries ran on, the next title a few lines below the previous
  entry's footer.
- The grade badge was a 9.6 pt tab in the title band and appeared nowhere
  else as a marker.
- Eight rule weights (0.3–1.3 pt), full frames, a double frame, a double
  rule under titles, a short rule above footers, grey row rules, and
  chapter tables with their own 0.3 pt grey strokes and sans heads.
- A 12 mm foot margin, so the text ran almost to the foot of the page.
- Iowan's misreported cap height made every space look a third of an em
  larger than set.

## Fixes after the read-through

A page-by-page read of the 266-page draft found these; the book still has
266 pages.

- Tightened grade guides set their subheads with almost no space above.
  The space above a subhead now shrinks to half at most, so it stays about
  twice the space below. Boxes inside `fit-pages` tighten with the text
  around them, which wins back the room for it.
- Technique names in an italic key point were upright and looked too big.
  In italic text a cross-reference is still upright, but a twentieth
  smaller, to match the italic's capitals.
- The grade tab in running text widened its line. Its black is now drawn
  behind the figures, which sit on the baseline, so the line keeps its
  height.
- A figure could float above the head of its own section (Figures 3 and 5
  in Chapter 1, Figures 9 and 10 in Chapter 5). It now goes to the bottom
  of that page instead.
- Section heads left one word on their second line. A head that wraps is
  now broken as a whole with a high runt cost, and never inside a compound
  such as "comp-style". Heads tied with no-break spaces keep their breaks.
- The A–Z sorted with `lower()`, so "Hand–foot match" came after
  "Handle". It now sorts like the index.
- Index heads taken from the glossary were lower case (fingerboard,
  pulley) above capitalised sub-entries. A head is now capitalised when
  any entry under it is.
- The reading box could break after its first item. Its items are now
  set so that the label and the first two items stay together, and the
  last two, which keeps a short box whole.
- Removed the unused `chapter-end`.
