#import "../template.typ": *

#include "a-card.typ"

#include "a-troubleshooting.typ"

#include "a-glossary.typ"

#heading(level: 1, numbering: none)[A–Z of techniques] <a-to-z>

Every technique in this book, with the names you may hear for it. Aliases point to the entry they belong to. The grade is where the technique typically starts to matter indoors.

#a-to-z()

#include "a-grades.typ"

#include "a-errata.typ"

#heading(level: 1, numbering: none)[Sources] <sources>

Sources are numbered in the order they are first cited. Web pages were accessed in October and November 2026. Where a claim rests on a coach's or a gym's advice rather than on a study, the text says so.

#sources-columns(pages: 12, last: 470pt, bibliography(
  source-files,
  title: none,
  style: "springer-lecture-notes-in-computer-science",
))

#heading(level: 1, numbering: none)[Index] <index>

#make-index()
