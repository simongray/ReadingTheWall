// The web edition's template. website/build.py puts this file in place of
// book/template.typ in a build copy of the book, with the real template beside
// it as template-print.typ. The chapters don't change: they import the same
// macros and get semantic HTML instead of page layout.
//
// Everything not redefined here falls through to the print template, so a macro
// a later edition adds still works here, as long as it is built from these. The
// print layout it uses (grid, pad, place, ...) is passed through by `book`.
//
// This file marks up the book; build.py does the rest. It splits the result into
// pages, resolves the links and fills in whatever is generated from the whole
// book: the tables, the A–Z list, the backlinks and the index. Those appear here
// as empty elements with a `data-gen` or `data-*` attribute.

#import "template-print.typ": *
#import "template-print.typ" as print-book

#let tag(name, attrs: (:), ..body) = html.elem(name, attrs: attrs, ..body)
#let cls(name, class, ..body) = tag(name, attrs: (class: class), ..body)
#let name-text(c) = if type(c) == str { c } else { plain(c) }

// ------------------------------------------------------------ print-only

// These only set spaces in print.
#let fit-pages(k: auto, body) = body
#let spaced(k, body) = body
#let probe(body) = body
#let kgap(n, k) = 0pt
#let list-after-label(body, k: 1) = body
#let float-figure(body, clearance: 0pt) = body
#let caption-text(body) = body
#let wide-image(file) = image(file)
#let fit-start(what, est) = none
#let fit-end = none

// A page of its own in print: the title page and its back. build.py turns the
// chapters' `#page(...)[...]` into calls to this.
#let web-page(..args, body) = cls("section", "front-page", body)

// ------------------------------------------------------------ type

#let sc(body, tracking: 0.06em) = cls("span", "sc", body)
#let th(body) = body
#let section-label(body) = cls("span", "label", body)

#let fleuron(size: 11pt, name: ornaments.title) = tag("img", attrs: (
  class: "ornament", alt: "", src: "figures/ornament-" + name + ".svg",
))
#let orn-rule(width: 22mm, size: 10pt, name: ornaments.title) = cls("span", "orn-rule", fleuron(name: name))

#let aside-icon(name, inset: 0pt) = if name == none { none } else {
  tag("img", attrs: (class: "aside-icon", alt: "", src: "figures/icon-" + aside-icons.at(name, default: name) + ".svg"))
}

// ------------------------------------------------------------ grades

// The tab's colours, when this edition's print template has them. Editions without
// them keep the plain tab. A tab says its grade in a class (g0, g1, ...), and
// render.py writes the rules for those from the table that `book` passes on.
#let tab-look = dictionary(print-book).at("grade-tab-look", default: none)
#let tab-class(g) = if g == none or tab-look == none { "grade-tab" } else { "grade-tab g" + str(calc.max(g, 0)) }
#let color-text(c) = if type(c) == color { c.to-hex() } else { none }
#let tab-looks() = if tab-look == none { () } else {
  range(0, 9).map(g => {
    let look = tab-look(g)
    (fill: color-text(look.fill), figures: color-text(look.figures), outlined: look.stroke != none)
  })
}

#let grade-tab(body, size: 9pt, g: none) = cls("span", tab-class(g), body)
#let grade-tab-inline(body, size: 9pt, g: none) = grade-tab(body, g: g)
#let badge(g, size: 9pt) = grade-tab(grade-label(g) + "+", g: g)
#let badge-plain(g) = cls("span", "grade-plain", grade-label(g))

// ------------------------------------------------------------ marks and links

// An index mark. build.py gives it an id and files it under its term.
#let ix(term, main: false, display: none) = tag("span", attrs: (
  "data-ix": ix-merge.at(lower(term), default: term),
  "data-main": if main { "1" } else { "0" },
))

// A reference to a technique. build.py follows key-alias, fills in the name when
// there is no `body` and collects these for "Referenced from".
#let tref(key, body: none, show-page: true) = tag("a", attrs: (
  class: "tref", href: "#tech-" + key, "data-key": key,
  "data-named": if body == none { "0" } else { "1" },
), if body == none { key } else { body })

#let jt(term, body: none) = tag("a", attrs: (class: "jt", href: "#" + gloss-key(term)),
  if body == none { term } else { body })

#let gloss(term, body, see: ()) = tag("div", attrs: (class: "gloss", id: gloss-key(term)), {
  tag("dt", { term; ix(term) })
  tag("dd", {
    body
    if see.len() > 0 [ See #see.map(k => tref(k)).join(", ").]
  })
})

// ------------------------------------------------------------ boxes

#let labelled(title, k: 1, icon: none) = cls("h6", "label", { aside-icon(icon); title })

#let panel(title: none, fill: none, breakable: true, tight: false, k: auto, icon: none, class: "box", body) = cls("aside", class, {
  if title != none { cls("h6", "label", { aside-icon(icon); title }) }
  body
})
#let readbox(body, k: 1) = panel(title: [When to use it — reading the wall], icon: "reading", class: "box reading", body)
#let notebox(title, body, icon: none) = panel(title: title, icon: icon, class: "box note", body)
#let remember(title, body) = panel(title: title, class: "box remember", body)
#let keypoint(body) = panel(class: "box keypoint", body)
#let mistakes(body, k: 1) = cls("section", "mistakes", { labelled([Common mistakes], icon: "mistakes"); body })

// ------------------------------------------------------------ figures

#let filmstrip(file, title, caption) = cls("figure", "filmstrip", {
  cls("div", "filmstrip-head", { section-label[In motion]; " "; cls("span", "filmstrip-title", title) })
  image("figures/" + file)
  tag("figcaption", caption)
})

// A figure in an entry. It has no number in print either, and build.py decides
// by its width whether it goes beside the steps.
#let entry-figure(file, caption, wide) = tag("figure", attrs: (
  class: "entry-fig", "data-wide": if wide { "1" } else { "0" },
), {
  image("figures/" + file)
  if caption != none { tag("figcaption", caption) }
})

// A problem of "Eight problems to read". There is no page to turn here, so the
// answer stays closed until the reader opens it.
#let reading-question(n: none, title: none, grade: none, wall: none, start: none, finish: none, figure: none, prompts: none) = cls("section", "reading-question", {
  cls("h5", "step", { section-label[Problem #n]; " "; title })
  tag("p", [About #grade-tab-inline(grade-label(grade), g: grade). #wall Start: #start Finish: #finish])
  cls("section", "how", {
    labelled([Read it yourself])
    prompts
    entry-figure(figure, none, false)
  })
})

#let reading-answer(n: none, figure: none, caption: none, moves: none, crux: none, wrong: none, next: none, tall: none, small: none, entries: ()) = tag("details", attrs: (class: "reading-answer"), {
  tag("summary", [The answer to problem #n])
  cls("section", "how", {
    labelled([The moves])
    moves
    entry-figure(figure, caption, false)
  })
  for (head, body) in (([Crux.], crux), ([Why the obvious try fails.], wrong), ([What to try next.], next)) {
    if body != none { tag("p", [*#head* #body]) }
  }
  if tall != none { cls("div", "climber-note", { aside-icon("tall"); [*_Tall climbers._* ]; tall }) }
  if small != none { cls("div", "climber-note", { aside-icon("small"); [*_Small climbers._* ]; small }) }
  if entries.len() > 0 { cls("dl", "apparatus", { tag("dt", "Entries"); tag("dd", entries.map(k => tref(k)).join(", ")) }) }
})

// ------------------------------------------------------------ technique entry

// A part of an entry (a move it absorbed or gathers): `name` and `how`, and
// optionally `figure`, `caption` and `figure-wide`.
#let entry-part(p) = cls("section", "how entry-part", {
  cls("h6", "label", { ix(name-text(p.name), main: true); p.name })
  p.how
  let file = p.at("figure", default: none)
  if file != none { entry-figure(file, p.at("caption", default: none), p.at("figure-wide", default: false)) }
})

// `..extra` catches any field a later edition adds to its entries. The entry
// still builds, the field's content appears under a plain label, and build.py
// warns that this template should learn about it.
#let technique(
  key: none, name: none, aliases: (), category: none, grade: none, grade-note: none,
  summary: none, figure: none, caption: none, figure-wide: false, how: none, parts: (),
  when: none, errors: none, tall: none, small: none, related: (), watch: (), sources: (),
  k: auto, ..extra,
) = {
  let aliases = if type(aliases) == str { (aliases,) } else { aliases }
  let parts = if type(parts) == dictionary { (parts,) } else { parts }
  let part-names = parts.map(p => lower(name-text(p.name)))
  [#metadata((key: key, name: name, aliases: aliases, category: category, grade: grade))#label("tech-meta-" + key)]
  tag("article", attrs: (
    class: "entry", "data-key": key, "data-name": name-text(name), "data-grade": str(grade),
    "data-category": if category == none { "" } else { category },
    "data-category-name": if category == none { "" } else { categories.at(category, default: category) },
    "data-aliases": aliases.join("|", default: ""),
  ), {
    cls("header", "entry-head", {
      cls("div", "entry-title", {
        [#heading(level: 3, name)#label("tech-" + key)]
        ix(name-text(name), main: true)
        tag("a", attrs: (class: tab-class(grade), href: "#grade-" + str(calc.min(calc.max(grade, 0), 8))), grade-label(grade) + "+")
      })
      if aliases.len() > 0 or category != none {
        cls("p", "entry-meta", {
          if aliases.len() > 0 [_Also called_ #aliases.join(", ")]
          if aliases.len() > 0 and category != none [ · ]
          if category != none { tag("a", attrs: (class: "sc", href: "#cattable-" + category), categories.at(category, default: category)) }
        })
      }
    })
    for a in aliases.filter(a => lower(a) not in part-names) { ix(a + " (see " + name-text(name) + ")") }
    if summary != none { cls("p", "summary", summary) }
    if grade-note != none { cls("p", "grade-note", { sc[Grade]; " "; grade-note }) }
    if how != none or figure != none {
      cls("section", "how", {
        if how != none {
          cls("h6", "label", [How to do it])
          how
        }
        if figure != none { entry-figure(figure, caption, figure-wide) }
      })
    }
    for p in parts { entry-part(p) }
    if when != none { readbox(when) }
    if errors != none { mistakes(errors) }
    if tall != none { cls("div", "climber-note", { aside-icon("tall"); [*_Tall climbers._* ]; tall }) }
    if small != none { cls("div", "climber-note", { aside-icon("small"); [*_Small climbers._* ]; small }) }
    for (field, value) in extra.named() {
      tag("div", attrs: (class: "climber-note", "data-unknown-field": field), {
        [*#field.* ]
        if type(value) in (content, str) { value } else { repr(value) }
      })
    }
    cls("dl", "apparatus", {
      if related.len() > 0 {
        tag("dt", "Related")
        tag("dd", related.map(k => tref(k)).join(", "))
      }
      if watch.len() > 0 {
        tag("dt", "Watch")
        tag("dd", watch.map(w => [#link(w.at(2))[#w.at(1)] (#w.at(0))]).join("; "))
      }
      if sources.len() > 0 {
        tag("dt", "Sources")
        tag("dd", src(..sources))
      }
    })
  })
}

// ------------------------------------------------------------ generated

#let category-table(cat) = tag("div", attrs: ("data-gen": "category-table", "data-category": cat, id: "cattable-" + cat))
#let grade-techniques(g) = tag("div", attrs: ("data-gen": "grade-techniques", "data-grade": str(g)))
#let a-to-z() = tag("div", attrs: ("data-gen": "a-to-z"))
#let make-index() = tag("div", attrs: ("data-gen": "index"))

// ------------------------------------------------------------ the document

// A part page. build.py lists the chapters under it.
#let part(title, subtitle: none, ornament: auto) = tag("section", attrs: (
  class: "part", "data-title": name-text(title),
  "data-subtitle": if subtitle == none { "" } else { name-text(subtitle) },
  "data-ornament": if ornament == auto { ornaments.parts.at(title, default: ornaments.other-part) } else { ornament },
))

#let book(title: none, subtitle: none, author: none, body) = {
  set document(title: title, author: author)
  set text(lang: "en", region: "gb")
  set heading(numbering: (..n) => {
    let n = n.pos()
    if n.len() == 1 { str(n.first()) } else if n.len() == 2 { str(n.at(0)) + "." + str(n.at(1)) } else { none }
  })

  // Print layout that HTML export would drop along with its content.
  show columns: it => tag("div", attrs: (class: "columns", "data-count": str(it.count)), it.body)
  show align: it => if it.alignment == right { cls("div", "flush-end", it.body) } else { it.body }
  show pad: it => it.body
  show place: it => it.body
  show grid: it => it.children.map(c => c.body).join([ ])
  show stack: it => it.children.filter(c => type(c) == content).join([ ])
  show box: it => it.body
  show move: it => it.body
  show scale: it => it.body
  show rotate: it => it.body
  show repeat: none
  // Spacing has no meaning here, but it does part what it stands between.
  show v: parbreak()
  show h: [ ]
  show pagebreak: none
  show colbreak: none
  show line: cls("hr", "rule")
  show rect: none
  show underline: it => cls("span", "dotted", it.body)

  // Paths stay as written; build.py resolves them and adds the sizes.
  show image: it => tag("img", attrs: (src: str(it.source), alt: if it.alt == none { "" } else { it.alt }))

  // A heading keeps its number and, for a chapter, its number in words and its
  // ornament in attributes, for build.py to set as print does.
  show heading: it => context {
    let attrs = (:)
    let lbl = it.at("label", default: none)
    if lbl != none { attrs.insert("id", str(lbl)) }
    let n = counter(heading).get()
    let numbered = it.numbering != none and it.level <= 2
    if numbered { attrs.insert("data-num", n.map(str).join(".")) }
    if it.level == 1 {
      if numbered { attrs.insert("data-word", number-words.at(n.first() - 1, default: str(n.first()))) }
      attrs.insert("data-ornament", if numbered { ornaments.chapters.at(str(n.first()), default: ornaments.other) } else { ornaments.other })
    }
    tag("h" + str(calc.min(it.level + 1, 6)), attrs: attrs, it.body)
  }

  show figure.caption: it => tag("figcaption", {
    sc[#it.supplement #context it.counter.display(it.numbering)]
    " "
    it.body
  })
  show outline: tag("div", attrs: ("data-gen": "contents"))
  // What build.py needs from the print template's tables.
  tag("div", attrs: (
    "data-gen": "book-data",
    "data-key-alias": json.encode(key-alias, pretty: false),
    "data-categories": json.encode(categories, pretty: false),
    "data-tab-looks": json.encode(tab-looks(), pretty: false),
  ))
  body
}
