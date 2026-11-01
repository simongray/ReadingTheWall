#import "../template.typ": *

// The corrections are written once, as the Errata of the newest section of
// CHANGELOG.md; tools/errata.py (run by build.sh) turns them into
// book/errata.json.
#let errata = json("../errata.json")
#let previous = lower(errata.previous)

#if errata.items.len() > 0 [
#heading(level: 1, numbering: none)[Corrections to the #previous] <corrections>

#ix("Errata")
This edition corrects these mistakes in the #previous. The page numbers are the #previous's. CHANGELOG.md in the source repository (see the back of the title page) lists every change, the redrawn figures among them.

#{
  set par(justify: false)
  set table.cell(breakable: false)
  data-table(
    columns: (auto, 1fr),
    table.header(align(right, th[Page]), th[Correction]),
    ..errata.items.map(e => (
      align(right, e.pages),
      [#if e.place != "" [#strong(e.place). ]#e.text#if e.subs.len() > 0 { list(..e.subs) }],
    )).flatten(),
  )
}
]
