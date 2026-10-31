# Final read: front matter and chapters 1–2

One line per change, grouped by file. Page numbers are in the draft PDF of
31 October 2026.

## book/chapters/00-front.typ

- Title page: title set at about 59 pt (half a step above fs.title on the 1.2 scale) with 1.12 × size between baselines; the leading had been an em of the body size, so the g of "Reading" touched "the Wall". The page still fits and balances (requested by the reader).
- Colophon: the ornament is now described as a jug like the holds in the illustrations, not the Zapf Dingbats hedera; "Typeset with Typst" kept on one line (requested by the coordinator).
- Removed the `#chapter-end()` call, now a no-op (requested by the coordinator).
- Finding your way around: the example "Drop knee (p. 12)" pointed at a page that isn't the entry; it now shows and links to the real page (86), without leaving a backlink. "A technique name in italics with a page number" → "A technique name in italics", since show-page: false references are also links.
- Anatomy of a technique entry: the heading and "Every entry has the same parts:" sat alone at the foot of p. iii; the line is now sticky to the list, so the section starts p. iv.

## book/chapters/01-movement.typ

- 1.1: dangling modifier "Standing upright, it sits…" → "When you stand upright, it sits…".
- 1.4: "The hands chapter describes each hold type" → "Chapter 5 describes…", matching the chapter references around it.
- 1.7: "Hooper argues" → "The physiotherapist Jason Hooper argues": his first and only mention in the book had no first name or role.
- 1.8: "The troubleshooting appendix lists them by symptom" ("them" had no clear antecedent) → "lists the techniques by symptom".

## book/chapters/02-reading.typ

- Step 1: "Do volumes (p. 180) (big bolt-on shapes) count?" → page number dropped (show-page: false), as for the other glossed references in the chapter.
- Step 1: "A Sit starts (p. 188)" → "A sit start"; "a Top-outs (p. 177)" → "a top-out" (the entry names are plural).
- Step 4: "Or you move the same hand twice" → "Or you can move…", parallel with "You can match… You can cross…".
- Step 5: first mention of Gresham now gives "The coach Neil Gresham".
- Step 7: "The next section lists what setters say they do" pointed at 2.3; now "Section 2.5" via a new label `<reading-setter>` on that heading.
- 2.3 table: unexplained "meat hook" → "a 'meat hook': palm on one face, fingers over the other" (as in Chapter 7, same source E18).
- 2.4 heading: non-breaking spaces so it breaks "What to read first / on each kind of wall" rather than leaving "wall" alone.
- 2.7 Projecting step 3: the gloss of "link" sat after "keep going"; now "Link through the crux (climb past it without stopping) and keep going."
- 2.10: "so a harder colour isn't always harder" → "so a problem in a harder colour isn't always harder".

## figtools/figs_concepts.py (re-rendered into book/figures; warn() silent)

- concept-straight-arms (Fig. 3a): the "biceps working" leader ended on the elbow joint; it now ends on the upper arm.
- filmstrip-hips-first, frame 5: the "stand up" body arrow overlapped the left thigh; raised clear of it, below the bent left arm.
