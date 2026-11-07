# Typography pass

The book's content and figures are final. Your job is to make it look like
a real typographer spent time setting it: a pretty, serious technique book,
not a quickly generated one-off. The reader asked for "excellent serif
typography in deliberately varying sizes, well thought out spacing and a
tiny bit of ornamentation".

## Constraints

- Output: A4 PDF read on a 13.3-inch greyscale e-ink screen (Onyx Boox Max,
  about 207 ppi, page shown at ~95% size). Strokes thinner than ~0.25 pt
  and text lighter than about 45% grey wash out; avoid them. Body text no
  smaller than 10.5 pt.
- Page count is not a target (see "Typography" in `REVISE-3.md`).
- Typst 0.15 (`typst compile --root /Users/simongray/Books/Bouldering
  book/main.typ out.pdf`). Fonts: macOS system fonts (`typst fonts` lists
  them: Charter, Iowan Old Style, Palatino, New York, Optima, Avenir Next
  ...) plus Typst's bundled Libertinus Serif and New Computer Modern.
  Check that any font feature you rely on (small caps `smcp`, old-style
  figures `onum`, ligatures) really exists in that font by rendering it.
- Keep every function in `book/template.typ` working with the same
  signature (chapters call `technique`, `tref`, `jt`, `ix`, `src`,
  `readbox`, `notebox`, `keypoint`, `remember`, `filmstrip`, `badge`,
  `category-table`, `grade-techniques`, `a-to-z`, `make-index`, `gloss`,
  `part`, `book`). Keep all links, labels, backlinks, the header
  navigation (Contents · A–Z · Troubleshooting · Glossary · Index), QR
  codes and the index. You may restyle all of them.
- You own `book/template.typ`, the title page and "How to use this book"
  layout in `book/chapters/00-front.typ` (not its wording), the
  appendix assembly in `10-appendices.typ`, and the `FONT` constant and
  label text styles in `figtools/climb.py` (figure labels should match the
  book's typography; re-run `python3 figtools/build_all.py` after changing
  them and check that no label now overflows or collides). Don't change
  chapter wording.

## What to aim for

- **Typefaces.** An all-serif design: a sturdy text face that survives
  e-ink (Charter is a good candidate) and, if it helps, a second serif or
  the same family's small caps and italics for display, headings, labels
  and captions. Use true small caps with light letterspacing for running
  heads, section labels ("HOW TO DO IT", "WHEN TO USE IT"), the grade
  badges' grade names if suitable, and table heads. Old-style figures in
  running text if the face has them; lining figures in tables.
- **A deliberate type scale.** Distinct, related sizes for: part titles,
  chapter numbers and titles, section heads, technique names, body, the
  reading-the-wall box, notes and footers, captions, tables, index. A
  modular scale is fine; what matters is that each level is clearly
  different and they look designed together.
- **Spacing as a system.** Consistent vertical rhythm; generous but not
  wasteful chapter openings; a clear gap between technique entries; space
  above a heading larger than below it; no heading stranded at the foot
  of a page; tolerable widows and orphans; figures and their captions kept
  together; lists and boxes with the same internal spacing everywhere.
- **Measure and margins.** Keep line length comfortable (roughly 70–90
  characters). Margins balanced for a screen (no binding gutter), with the
  running head and folio placed deliberately.
- **A little ornament, used consistently.** For example: a small fleuron
  or rule ornament on part pages and chapter openers, a centred ornament
  between major sections or at chapter ends, a refined treatment of the
  technique title band (e.g. a thin rule pair), a classic look for boxes
  (the grey reading box, the remember box, note boxes), booktabs-style
  tables, an elegant title page. Restraint: one ornament family, not
  clip art.
- **Captions** in an italic or small serif style that sets them apart from
  body text; figure labels in the same family.
- **Title page and part pages** that look designed (consider the cover
  figure's placement, a subtitle in italic, small caps for the byline).

## Process

1. Render a sample of pages before you start (`pdftoppm -r 70`) to see
   the current state: title page, contents, a part page, a chapter opener,
   a page of prose, two technique-entry pages, a grade-guide page with a
   remember box, a filmstrip page, the troubleshooting table, the glossary,
   the A–Z, the sources and the index.
2. Try two or three typographic directions on a few sample pages, compare
   them side by side, pick one.
3. Apply it to the whole template, then go through the entire book page by
   page at low resolution (contact sheets of ~12 pages each) and fix
   layout problems: bad breaks, stranded headings, crowded or empty pages,
   overflowing tables, figure placement.
4. Keep a short design note in `research/typography-notes.md` (fonts, scale,
   spacing rules, ornaments) so the design can be maintained.

Reply in under 250 words: the design choices, the page count, and any
remaining layout issues.
