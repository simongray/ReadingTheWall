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

Sources are numbered in the order they are first cited. Web pages were accessed in October 2026. Where a claim rests on a coach's or a gym's advice rather than on a study, the text says so.

// The access date is the same for every web page and is given above, so
// it is left out of the entries: each URL keeps its value, not its date.
#let source-list(letter) = {
  let data = yaml("../../research/" + letter + "-sources.yml")
  // a file with no sources yet parses as none, or as an empty mapping
  if data == none { data = (:) }
  for (k, e) in data {
    if type(e) == dictionary and type(e.at("url", default: none)) == dictionary {
      e.url = e.url.value
      data.insert(k, e)
    }
  }
  bytes(yaml.encode(data))
}

#sources-columns(pages: 12, last: 470pt, bibliography(
  ("A", "B", "C", "D", "E", "F", "G", "H").map(source-list),
  title: none,
  style: "springer-lecture-notes-in-computer-science",
))

#heading(level: 1, numbering: none)[Index] <index>

#make-index()
