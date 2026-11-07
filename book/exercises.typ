// Reading the Wall: Exercises, the booklet of problems to read that goes with
// the book. Compile it with `--input booklet=1`: its references into the book
// then take their pages from book/book-pages.json, which tools/book_pages.py
// writes. build.sh and release.sh do both.
#import "template.typ": *
#import "edition.typ": *

#show: book.with(
  title: "Reading the Wall: Exercises",
  author: "Edited by Simon Gray; written by Claude (Anthropic)",
  links: false,
)

// ------------------------------------------------------------ title page

#page(header: none, footer: none, margin: (x: 26mm, top: 30mm, bottom: 24mm))[
  #set align(center)
  #set par(justify: false, first-line-indent: 0pt)
  #text(size: 11pt, sc(tracking: 0.2em)[A COMPANION TO READING THE WALL])
  #v(10mm)
  #let title-size = fs.body * calc.pow(1.2, 8)
  #block({
    set text(size: title-size, weight: 400)
    set par(leading: 0.42 * title-size)
    [Exercises]
  })
  #v(6mm)
  #orn-rule(width: 34mm, size: 12pt)
  #v(7mm)
  #block(width: 82%, text(size: 14pt, style: "italic", hyphenate: false)[
    Eight problems to read from the ground,\ with their answers overleaf.
  ])
  #v(1fr)
  #text(size: 11pt, sc(tracking: 0.12em)[Edited by Simon Gray])
  #v(0.5mm)
  #text(size: 11pt, sc(tracking: 0.12em)[Written by Claude, an AI model made by Anthropic])
  #v(2.5mm)
  #text(size: 10.5pt, style: "italic", (if edition-day == none { datetime.today() } else { edition-day }).display("[month repr:long] [year]"))
]

// ------------------------------------------------------------ colophon

#page(header: none, footer: none, margin: (x: margin-x, top: 30mm, bottom: 26mm))[
  #set par(justify: false, first-line-indent: 0pt, leading: 0.82em, spacing: 0.82em)
  #set text(size: fs.note, hyphenate: false)
  #let shown-date = if edition-day == none { none } else {
    edition-day.display("[day padding:none] [month repr:long] [year]")
  }
  #v(1fr)
  #block(width: 92mm, {
    text(size: fs.body, style: "italic")[Reading the Wall: Exercises]
    parbreak()
    [A companion to _Reading the Wall: A technique handbook for indoor bouldering_. Its page numbers in brackets are the book's.]
    v(0.9em)
    sc(tracking: 0.08em)[Edited by Simon Gray]
    parbreak()
    sc(tracking: 0.08em)[Written by Claude]
    parbreak()
    [Claude is an AI model made by Anthropic. It also wrote the code that draws the figures. No image generator was used.]
    v(0.9em)
    [For the #lower(edition-label)#if shown-date != none [, #shown-date]]
    parbreak()
    [Built from commit #text(number-type: "lining", commit)]
    v(0.9em)
    [The book, this booklet and their sources are at #box(link("https://github.com/simongray/ReadingTheWall")[github.com/simongray/ReadingTheWall]).]
    v(0.9em)
    link("https://creativecommons.org/licenses/by-sa/4.0/", image("assets/cc-by-sa.svg", width: 22mm, alt: "CC BY-SA 4.0"))
    v(0.4em)
    [The text and illustrations are licensed under the #link("https://creativecommons.org/licenses/by-sa/4.0/")[Creative Commons Attribution-ShareAlike 4.0 International licence] (CC BY-SA 4.0).]
  })
]

// ------------------------------------------------------------ the problems

#set page(numbering: "1")
#counter(page).update(1)
#include "chapters/x-problems.typ"

#heading(level: 1, numbering: none)[Sources]

Sources are numbered in the order they are first cited here, so their numbers differ from the book's. Web pages were accessed in October 2026.

#sources-columns(bibliography(
  source-files,
  title: none,
  style: "springer-lecture-notes-in-computer-science",
))
