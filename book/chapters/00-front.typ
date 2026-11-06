#import "../template.typ": *
#import "../edition.typ": *

// ------------------------------------------------------------ title page

#page(header: none, footer: none, margin: (x: 26mm, top: 30mm, bottom: 24mm))[
  #set align(center)
  #set par(justify: false, first-line-indent: 0pt)
  #text(size: 11pt, sc(tracking: 0.2em)[A TECHNIQUE HANDBOOK FOR INDOOR BOULDERING])
  #v(10mm)
  // The title a half step above fs.title on the scale (about 59 pt). The
  // leading is set in points: an em inside par() would resolve against the
  // body size. With the top edge at cap height, baselines sit 0.42 + 0.7 =
  // 1.12 times the size apart, so the g of "Reading" clears "the Wall".
  #let title-size = fs.body * calc.pow(1.2, 9.5)
  #block({
    set text(size: title-size, weight: 400)
    set par(leading: 0.42 * title-size)
    [Reading\ the Wall]
  })
  #v(6mm)
  #orn-rule(width: 34mm, size: 12pt)
  #v(7mm)
  #block(width: 82%, text(size: 14pt, style: "italic", hyphenate: false)[
    Learn to read a problem from the ground\ and work out the techniques you need to climb it.
  ])
  #v(1fr)
  #image("../figures/cover.svg")
  #v(1fr)
  #text(size: 11pt, sc(tracking: 0.12em)[Edited by Simon Gray])
  #v(0.5mm)
  #text(size: 11pt, sc(tracking: 0.12em)[Written by Claude, an AI model made by Anthropic])
  #v(2.5mm)
  #text(size: 10.5pt, style: "italic", (if edition-day == none { datetime.today() } else { edition-day }).display("[month repr:long] [year]"))
]

// ------------------------------------------------------------ colophon

// The back of the title page: one quiet page in small type, set at the foot.
#page(header: none, footer: none, margin: (x: 31mm, top: 30mm, bottom: 26mm))[
  #set par(justify: false, first-line-indent: 0pt, leading: 0.82em, spacing: 0.82em)
  #set text(size: fs.note, hyphenate: false)
  #let shown-date = if edition-day == none { none } else {
    edition-day.display("[day padding:none] [month repr:long] [year]")
  }
  #let year = if edition-date == "" { str(datetime.today().year()) } else { edition-date.slice(0, 4) }
  #v(1fr)
  #block(width: 92mm, {
    text(size: fs.body, style: "italic")[Reading the Wall]
    parbreak()
    [A technique handbook for indoor bouldering]
    v(0.9em)
    sc(tracking: 0.08em)[Edited by Simon Gray]
    parbreak()
    sc(tracking: 0.08em)[Written by Claude]
    parbreak()
    [Claude is an AI model made by Anthropic. It also wrote the code that draws the figures and builds the website. No image generator was used. See "How this book was made".]
    v(0.9em)
    [#edition-label#if shown-date != none [, #shown-date]]
    parbreak()
    [Built from commit #text(number-type: "lining", commit)]
    v(0.9em)
    [Errata and the changes between editions are listed in CHANGELOG.md in the source repository at #box(link("https://github.com/simongray/ReadingTheWall")[github.com/simongray/ReadingTheWall]).]
    v(0.9em)
    link("https://creativecommons.org/licenses/by-sa/4.0/", image("../assets/cc-by-sa.svg", width: 22mm, alt: "CC BY-SA 4.0"))
    v(0.4em)
    [The text and illustrations are licensed under the #link("https://creativecommons.org/licenses/by-sa/4.0/")[Creative Commons Attribution-ShareAlike 4.0 International licence] (CC BY-SA 4.0). The code that builds the book is free software under the #link("https://www.gnu.org/licenses/gpl-3.0.html")[GNU General Public License, version 3].]
    v(0.9em)
    [To cite this book: Gray, S. (ed.) (#year). _Reading the Wall: A technique handbook for indoor bouldering._ Written by Claude (Anthropic). #edition-label, commit #text(number-type: "lining", commit). #box(link("https://github.com/simongray/ReadingTheWall")[github.com/simongray/ReadingTheWall]).]
    v(0.9em)
    line(length: 18mm, stroke: 0.5pt + ink)
    v(0.5em)
    [Set in Iowan Old Style, with its small capitals and old-style figures. The ornaments are climbing holds, one for each chapter and part, drawn like those in the illustrations, which were made in Python. Typeset~with~Typst.]
    v(0.5em)
    [The pelican on the cover is a play on Simon Willison's test of language models, which asks them to draw a pelican riding a bicycle.]
  })
]

// ------------------------------------------------------------ how to use

#set heading(numbering: none)

#heading(level: 1, numbering: none, outlined: true)[How to use this book]

This is a technique book, not a training book. It assumes you already climb. You know the V-scale and can get up most V2s and V3s. Strength alone no longer explains why some problems go and others don't. If you're newer than that, the V0–V2 entries and guides are for you too. This book was written for one tall adult climber and now has a few notes for small climbers.

The book names the movements good climbers use and says how to do each one. Above all, it shows you how to recognise when a problem calls for one.

It is written for indoor bouldering. Rock, ropes and lead climbing come up only where they explain something about the gym.

== How the book is organised

*Part I* explains the mechanics behind every technique: centre of gravity, straight arms, hips, and the direction a hold pulls. It also gives a step-by-step method for reading a problem before you touch it.

*Part II* is the catalogue, with one chapter per category: feet and legs, body positioning, hands and holds, dynamic movement, and terrain. Each chapter opens with a table that ranks its techniques by grade, and the entries follow in that order.

*Part III* has a guide for every grade from VB to V8+. Each guide says what indoor problems at that grade look like, which techniques start to matter and what to focus on. The step from V4 to V5 gets extra space.

*Part IV* covers your body (being tall, small or heavier, or starting as an adult), how to learn technique, and how to fall safely.

The *appendices* start with "On the mat", the book on one page to look at between attempts. Then comes a troubleshooting table that goes from a symptom ("I swing off like a door") to the techniques that fix it. They also hold a glossary of climbing jargon, an A–Z list of every technique name, a grade conversion table, the corrections to the previous edition, the sources and the index.

== Anatomy of a technique entry

// sticky: the heading and this line go with the list, not alone at the
// foot of a page
#block(sticky: true)[Every entry has the same parts:]

- *Name and grade badge.* The badge, such as #badge(3), marks the grade where the technique starts to *matter* on indoor problems. Below that grade you can usually get away without it. Above it, more and more problems are set so that you need it. The grade is a judgement based on coaches' advice, technique clinics and climbers' reports, and gyms vary. If you should start learning the technique earlier, the #sc(tracking: 0.08em)[Grade] note says when.
- *Also called.* Other names you will hear. All of them are in the A–Z list and the index.
- *How to do it.* Numbered, concrete steps: which limb goes where, and why.
- *When to use it — reading the wall.* The grey box has two groups. "Look for" lists what you can see on the wall before you climb. "Symptoms" lists what goes wrong when you needed the technique and didn't use it.
- *Common mistakes*, notes for *tall climbers* and *small climbers* where there is something specific to say, *related* techniques, videos to *watch*, and *sources*.
- *Referenced from.* Every place in the book that mentions the technique, so you can jump back to it.

== Finding your way around

Everything is linked. On an e-reader, tap to jump:

- A technique name in italics, such as #context {
    // the real entry and page, linked; not a tref, which would list this
    // page among the entry's backlinks
    let q = query(label("tech-meta-drop-knee"))
    if q.len() == 0 [_Drop knee_] else {
      let m = q.first()
      link(m.location())[#emph[Drop knee] (p.#sym.space.nobreak#counter(page).at(m.location()).first())]
    }
  }, leads to its entry.
- A word with a #underline(stroke: (thickness: 0.5pt, dash: "dotted"), offset: 2pt)[dotted underline] is climbing jargon. It leads to its definition in the glossary.
- A grade badge leads to the guide for that grade. The category name under an entry's title leads to the ranked table at the start of its chapter.
- Numbers in square brackets, such as [12], lead to the sources.
- The header of every page links to the contents, the A–Z list, the troubleshooting table, the glossary and the index. The chapter name in the header leads to the start of the chapter.
- The PDF's bookmarks list every chapter and every technique.

== Reading the illustrations

Most illustrations show the climber from behind, facing the wall, as you would see a friend from the mats. Side views show the wall on the right, with the climber facing it.

#figure(image("../figures/legend.svg"), caption: [Key to the illustrations. In every figure the climber's left limbs are shaded and the right limbs white, so you can follow which hand and foot does what.], kind: image, supplement: [Figure])

== A word on safety

Bouldering falls are short but frequent. Some techniques load joints in unusual ways, e.g. full crimps, heel hooks, drop knees and dynos; their entries say how. Chapter 9 covers injuries, warming up and falling. Back off any move that hurts.

// ------------------------------------------------------------ how it was made

#heading(level: 1, numbering: none, outlined: true)[How this book was made]

Claude, an AI model made by Anthropic, wrote this book. Simon Gray edited it. The book is free and Simon Gray will never sell it. This section says who did what and what has and hasn't been checked, so that you can judge the book. Claude wrote it too, from the book's records.

*The text.* Claude searched the web for sources, read the pages it could open and wrote up what they said in research files. It wrote the chapters from those files. Claude has never climbed, so the technique advice comes from its sources and its own judgement. The records don't show anyone trying the advice on a wall. For this edition Simon Gray decided what should change, reported faults in the figures and said why the prose read as generated. Claude then rewrote much of that prose. The records don't show how much of the text Simon Gray read or changed.

*The figures.* No image generator was used. Claude wrote the Python code that draws every figure, the cover included. It gives each pose as hand and foot positions in centimetres, and the code works out the elbows and knees. The code adds the colour last. Simon Gray supplied the table that gives each grade its colour. For the second edition, Claude compared the poses with photographs or single video frames, which aren't in the book. The logs cover most figures but not those in the hands chapter, and for some techniques the references were thin.

*The website.* Claude wrote the code that builds a website from the book's own files and makes its dark-mode figures. It also wrote the figures' descriptions for screen readers.

*The sources.* The #link(<sources>)[Sources appendix] lists more than 300. About seven in ten are web pages from magazines, coaches, gyms and brands. About one in six is a study or a review, and about one in twenty is a forum thread or a wiki. For some of the studies, Claude read only the abstract. A few are excerpts or chapters from books, which Claude could read only online. Claude didn't watch the linked videos. It chose them from their titles, channels, descriptions and chapter lists. The records don't show anyone else watching them.

*Claims without a source.* Each grade badge is a judgement. Some other unsourced claims carry a label such as "(judgement)". Every technique entry lists its sources at the foot, but about one in five of its numbered steps and common mistakes has no citation of its own and no label. In the "When to use it" boxes, about three lines in five have neither.

*The checks.* Claude also ran the fact checks, which compare a selection of claims with the pages they cite. The first, dated 30~October 2026, took 159 claims from chapters 2, 3, 6 and 7 and the troubleshooting table. Claude left 78 as they were, changed 70 and couldn't verify~11. A second covered every claim in chapter 1 and the flagged claims, numbers, injury claims and attributions in chapters 4, 5, 8 and 9 and the grade appendix. A third, on 31~October, went back to the pages that had been blocked. Most of the unverified claims held and some didn't. The second edition listed 30 corrections to the first. A later check covered the corrections to evidence in this edition.

*What hasn't been done.* No outside expert has reviewed this book and no person has audited its citations. The first three checks read an earlier text. A later check read this edition's rewritten text and new notes for small climbers, but its log doesn't record its scope.

*The records.* The repository at #box(link("https://github.com/simongray/ReadingTheWall")[github.com/simongray/ReadingTheWall]) holds the fact-check logs and other research files (in research/), the code and the list of corrections between editions (CHANGELOG.md). Claude wrote those logs, so they aren't independent evidence. The repository's history starts with the first edition on 31~October 2026, so the work before that isn't in it. The second edition followed on 1~November. The history records every change under Simon Gray's name, so it doesn't show who wrote what.

#outline(title: [Contents], depth: 2, indent: auto) <contents>
