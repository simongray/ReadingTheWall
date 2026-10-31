// Layout and building blocks for the bouldering technique handbook.
// The design is described in research/typography-notes.md, and the rules
// behind it in research/typography-principles.md.

// ------------------------------------------------------------ type

// One serif family for everything: Iowan Old Style has true small caps,
// old-style and lining figures, a real italic and a sturdy stroke that
// survives e-ink. Libertinus Serif fills in arrows and other symbols.
#let serif = ("Iowan Old Style", "Charter", "Libertinus Serif")
// Kept for chapter code that asks for it; the book has no sans-serif.
#let sans = serif

// The type scale: one ratio, 1.2, from the 10.5 pt text size. Reading and
// reference matter takes the half steps next to the text size; headings
// take whole steps, two or more apart, so that each level is clearly
// different from the next.
#let fs = (
  index: 8.75pt,    // −1: index, sources
  note: 9.6pt,      // −½: entry apparatus, grade notes, running head
  caption: 9.6pt,   // −½: captions, tables, glossary, A–Z
  body: 10.5pt,     //  0: text and boxes
  lead: 11.5pt,     // +½: entry summaries, key points
  sub: 12.6pt,      // +1: subheads, chapter labels
  badge: 15.1pt,    // +2: the grade in an entry's title band
  tech: 18.1pt,     // +3: technique names
  section: 21.8pt,  // +4: numbered sections, and the grade beside a grade section
  guide: 26.1pt,    // +5: grade guides
  part-sub: 26.1pt, // +5: part titles
  chapter: 31.4pt,  // +6: chapter titles
  guide-tab: 31.4pt,// +6: the grade beside a grade guide
  title: 45pt,      // +8: the title page
)

#let ink = black
#let shade = luma(238)      // the reading box
#let shade-dark = luma(200)
#let rule-grey = luma(102)  // kept for chapter code; the rules are black

// The rules: two weights, horizontal only. A heavy rule opens a unit (an
// entry's title band, the top of every box and table); a light rule
// divides or closes one (the running head, a table's head, the foot of
// boxes and tables, an entry's references).
#let rule-heavy = 1.2pt + ink
#let rule-light = 0.5pt + ink

// The page. The measure (150 mm, about 90 characters) leaves room for the
// figures beside the steps; wide figures may extend into the margins by
// `overhang` on both sides. The foot margin is deeper than the head.
#let margin-x = 30mm
#let margin-top = 25mm
#let margin-bottom = 23mm
#let overhang = 11mm

// Vertical space is measured in lines of text. Text edges are set at the
// cap height and the baseline, so the space between two blocks of text is
// the white between a baseline and the next capitals: `gap(n)` is the
// space that adds n empty lines to the normal line spacing.
#let cap = 0.7em
#let pitch = 16.5pt                          // baseline to baseline at 10.5 pt
#let lead = (pitch / fs.body - 0.7) * 1em    // the leading that gives it
#let gap(n) = pitch - 0.7 * fs.body + n * pitch

#let smcp = ("c2sc", "smcp")
// True small caps with light letterspacing.
#let sc(body, tracking: 0.06em) = text(features: smcp, tracking: tracking, body)
// Table heads.
#let th(body) = sc(body, tracking: 0.05em)

// The ornaments are holds, drawn like the holds in the figures by
// figtools/figs_cover.py (book/figures/ornament-<name>.svg): a chalked jug
// on the title page, and a hold of its own for each part page and each
// chapter opening, chosen for what the part or chapter is about. The front
// matter and the appendix chapters share one quiet foothold. Each is drawn
// at the height it is set at (12 pt on the title page, 24 pt on a part
// page, 5 mm at a chapter opening), so its lines match the figures'.
// This is the one table that says which ornament goes where.
#let ornaments = (
  title: "jug",                       // the hold every climber knows
  parts: (                            // by the part's title, as part() is called
    "Part I": "sidepull",             // foundations: every hold has a direction
    "Part II": "macro",               // the techniques: a hold you can take a dozen ways
    "Part III": "grades",             // a jug, a crimp, a chip: holds shrink as grades rise
    "Part IV": "pinch",               // your body: a pinch fits each hand differently
    "Appendices": "foot-chip-large",  // the quiet foothold, large
  ),
  chapters: (                         // by chapter number
    "1": "sloper",                    // How movement works: only body position holds a sloper
    "2": "chalked",                   // Reading a problem: chalk shows where others took the hold
    "3": "foothold",                  // Feet and legs: a foothold with rubber on it
    "4": "undercling",                // Body positioning: holds only with hips and feet placed
    "5": "crimp",                     // Hands and holds
    "6": "dual",                      // Dynamic movement: a dual-texture hold, as set for comp-style moves
    "7": "volume",                    // Terrain
    "8": "chip",                      // Grade by grade: the small chip the grades lead to
    "9": "pocket",                    // Your body and how you learn: pockets load the pulleys most
  ),
  other: "foot-chip",                 // unnumbered chapters: front matter, appendices
  other-part: "foot-chip-large",      // a part not listed above
)

// An ornament by name, `size` tall, and the rule built from it: the
// ornament between two light rules, each `width` long.
#let fleuron(size: 11pt, name: ornaments.title) = box(image("figures/ornament-" + name + ".svg", height: size))
#let orn-rule(width: 22mm, size: 10pt, name: ornaments.title) = box(grid(
  columns: (width, auto, width), column-gutter: 0.6em, align: horizon,
  line(length: 100%, stroke: rule-light), fleuron(size: size, name: name), line(length: 100%, stroke: rule-light),
))
#let arrow = text(font: "Libertinus Serif", sym.arrow.r)

// The icons of an entry's asides, drawn like the figures by
// figtools/figs_icons.py (book/figures/icon-<name>.svg), each with a
// meaning for its aside. This is the one table that says which goes where.
#let aside-icons = (
  tall: "tall",           // Tall climbers: the mannequin standing beside a height mark
  reading: "reading",     // When to use it — reading the wall: a look up at a hold
  mistakes: "mistakes",   // Common mistakes: a shoe skating off a foothold, crossed
)
// The icon hangs in the margin beside its label, its right edge
// `icon-gap` from the text block (or from the edge of the box the label is
// in: `inset`) and its middle level with the label's lowercase. It takes
// no room, so the label stays flush left and the spaces stay as they are.
// Every icon is drawn 7 mm tall and at most 8 mm wide, so it stays inside
// the outer frame (`overhang`). (The image is set in a box of that width:
// in the label's box of no width it would shrink to nothing.)
#let icon-gap = 0.8em
#let aside-icon(name, inset: 0pt) = if name == none { none } else {
  box(width: 0pt, place(right + horizon, dx: -inset - icon-gap, dy: -0.25em,
    box(width: overhang, align(right, image("figures/icon-" + aside-icons.at(name, default: name) + ".svg")))))
}

// Plain text of a heading body (for short running heads).
#let plain(c) = {
  if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(plain).join() }
  else if c.has("body") { plain(c.body) }
  else if c == [ ] { " " }
  else { "" }
}

// A figure image that may extend into the margins when it is wider than
// the text block. Figures keep the size they were drawn at, so line
// weights are equal across figures.
#let wide-image(file) = pad(x: -overhang, align(center, image(file)))

// Content measured before it is set (see `technique`) is marked by this
// region, so that cross-references in it leave out their links and marks:
// a measured copy may not hold anything that refers to the document.
#let probe-region = "AQ"
#let probing() = text.region == probe-region
#let probe(body) = {
  set text(region: probe-region)
  show cite: box(width: 1.6em, height: 0.7em)
  show link: it => it.body
  body
}

// ------------------------------------------------------------ categories

#let categories = (
  feet: "Feet and legs",
  body: "Body positioning",
  hands: "Hands and holds",
  dynamic: "Dynamic movement",
  terrain: "Terrain",
)

// ------------------------------------------------------------ sources

// Citation keys from the research dossiers that point at the same source
// are mapped onto one bibliography entry here.
#import "src-map.typ": src-map
#import "key-alias.typ": key-alias
#import "@preview/tiaoma:0.3.0": qrcode

#let src(..keys) = {
  let ks = keys.pos()
  for k in ks { cite(label(src-map.at(k, default: k))) }
}

// ------------------------------------------------------------ index

// #ix("term") marks an index entry at this spot; "Main!sub" makes a
// sub-entry. #ix("term", main: true) marks the defining page (bold).
#let ix(term, main: false, display: none) = [#metadata((term: term, main: main))<ix>]

// Sort key for index terms: case- and accent-insensitive, with sub-entries
// directly under their main entry.
#let ix-fold(s) = lower(s).replace("â", "a").replace("ä", "a").replace("é", "e").replace("ê", "e").replace("è", "e").replace("ö", "o").replace("ü", "u").replace("ß", "ss").replace("–", "-")

// Glossary terms filed under the index's own spelling, so that "flash"
// and "Flashing" don't appear as two entries. Keys are lower case.
#let ix-merge = (
  "arête": "Arêtes",
  "bail": "Bailing",
  "campus": "Campus move",
  "circuit": "Circuits",
  "cut loose": "Cutting loose and swing control",
  "flag": "Side flag",
  "match": "Matching hands",
  "overhang": "Overhangs",
  "roof": "Roofs",
  "sit start": "Sit starts",
  "slab": "Slab technique",
  "smear": "Smearing",
  "top out": "Top-outs",
  "volume": "Volumes",
  "comp style": "Comp-style setting",
  "downclimb": "Downclimbing",
  "downturned shoe": "Climbing shoes!downturned",
  "dual-tex": "Dual texture",
  "dynamic": "Dynamic movement",
  "static": "Static movement",
  "flash": "Flashing",
  "project": "Projecting",
  "font grade": "Font grades",
  "font scale": "Font grades",
  "pumped": "Pump",
  "spot": "Spotting",
  "spotter": "Spotting",
  "the line": "Line, the",
)

#let make-index() = context {
  let entries = query(<ix>)
  // Terms that differ only in case ("Sloper", "sloper") share one entry,
  // shown with the capitalised spelling.
  let groups = (:)
  let shown = (:)
  for e in entries {
    let t = ix-merge.at(lower(e.value.term), default: e.value.term)
    let g = lower(t)
    let pg = counter(page).at(e.location()).first()
    let rec = (page: pg, main: e.value.main, loc: e.location())
    if g in groups { groups.at(g).push(rec) } else { groups.insert(g, (rec,)); shown.insert(g, t) }
    if t.first() != lower(t.first()) { shown.insert(g, t) }
  }
  let keys = groups.keys().sorted(key: g => ix-fold(g).replace("!", "\u{1}"))
  // A head is shown capitalised when any entry under it is: the glossary's
  // "fingerboard" files under the chapters' "Fingerboard!when to start".
  let heads = (:)
  for g in keys {
    let h = shown.at(g).split("!").first()
    let capital = h.first() != lower(h.first())
    if lower(h) not in heads or capital { heads.insert(lower(h), h) }
  }
  let last-head = none
  let last-letter = none
  set par(justify: false, hanging-indent: 1em, spacing: 0.75em, leading: 0.72em, first-line-indent: 0pt)
  set text(size: fs.index, number-type: "lining")
  columns(3, gutter: 1.4em, {
    for g in keys {
      let k = shown.at(g)
      let parts = k.split("!")
      let head = heads.at(lower(parts.first()))
      let letter = upper(ix-fold(head).first())
      if letter != last-letter {
        block(above: 1.6em, below: 0.75em, sticky: true, text(size: fs.sub, weight: 700, letter))
        last-letter = letter
      }
      let recs = groups.at(g)
      // de-duplicate pages, keep the first location per page, prefer main
      let seen = (:)
      for r in recs {
        let key = str(r.page)
        if key not in seen { seen.insert(key, r) } else if r.main { seen.insert(key, r) }
      }
      let pages = seen.values().sorted(key: r => r.page)
      let refs = pages.map(r => link(r.loc, if r.main { strong(str(r.page)) } else { str(r.page) })).join(", ")
      if parts.len() == 1 {
        par[#head#h(0.45em)#refs]
        last-head = lower(head)
      } else {
        if lower(head) != last-head {
          par[#head]
          last-head = lower(head)
        }
        par[#h(0.9em)#parts.at(1)#h(0.45em)#refs]
      }
    }
  })
}

// ------------------------------------------------------------ the grade mark

#let grade-label(g) = if g == none { "—" } else if g < 0 { "VB" } else if g >= 8 { "V8+" } else { "V" + str(g) }

// The grade mark: white lining figures on a black tab. One design at four
// sizes: in running text, in an entry's title band, beside the head of a
// grade section and beside the head of a grade guide. It marks a heading
// and never replaces one: the heading keeps its text in the heading
// type. The proportions are in em, so every size is the same shape.
#let grade-tab(body, size: 9pt) = text(
  size: size, weight: 700, fill: white, number-type: "lining", tracking: 0.02em, top-edge: cap,
  box(fill: ink, inset: (x: 0.34em, y: 0.2em), radius: 0.09em, baseline: 0.2em, body),
)

// The grade of a section head as a marker: "V5 and up" becomes "V5+", the
// form the entry badges use.
#let grade-marker(s) = s.replace(" and up", "+").replace(" and above", "+")

// The same tab in running text, its black drawn behind the figures
// instead of around them: the figures sit on the baseline and the line
// keeps its height, as the tab takes no more room than the figures do.
#let grade-tab-inline(body, size: 9pt) = text(
  size: size, weight: 700, fill: white, number-type: "lining", tracking: 0.02em, top-edge: cap,
  context {
    let figs = [#h(0.34em)#body#h(0.34em)]
    let w = measure(figs).width
    box(width: w, {
      place(top + left, dy: -0.2em, rect(width: w, height: 1.1em, fill: ink, radius: 0.09em, stroke: none))
      figs
    })
  },
)

// The grade badge of a technique in running text: the grade where it
// starts to matter.
#let badge(g, size: 9pt) = grade-tab-inline(grade-label(g) + "+", size: size)

// The grade in tables and lists: small caps, no tab.
#let badge-plain(g) = text(number-type: "lining", sc(grade-label(g), tracking: 0.03em))

// ------------------------------------------------------------ technique cross-references

#let tech-page(key) = {
  let q = query(label("tech-" + key))
  if q.len() == 0 { none } else { q.first() }
}

// A link to a label that may not exist yet (plain text until it does).
#let navlink(lbl, body) = context {
  if not probing() and query(lbl).len() == 1 { link(lbl, body) } else { body }
}

// Reference a technique by key: "Heel hook (p. 34)" with a link. Each
// reference also leaves a mark, so the entry can list where it is
// referenced from (backlinks).
//
// The name is set in italic, and upright in italic text (a key point, a
// caption). Iowan's roman is wider and its capitals taller than its
// italic, so an upright name there is set a twentieth smaller to look the
// same size as the words around it.
#let tref-name(name) = if text.style == "italic" { text(style: "normal", size: 0.95em, name) } else { emph(name) }

#let tref(key, body: none, show-page: true) = context {
  let key = key-alias.at(key, default: key)
  let q = query(label("tech-meta-" + key))
  if probing() {
    let name = if body == none and q.len() > 0 { q.first().value.name } else if body == none { key } else { body }
    [#tref-name(name)#if show-page [ (p.#sym.space.nobreak#"000")]]
  } else if q.len() == 0 {
    text(fill: red, weight: 700)[[?#key]]
  } else {
    let m = q.first()
    let name = if body == none { m.value.name } else { body }
    let pg = counter(page).at(m.location()).first()
    [#metadata((key: key))<tref-mark>#link(m.location())[#tref-name(name)#if show-page [ (p.#sym.space.nobreak#pg)]]]
  }
}

// ------------------------------------------------------------ glossary

#let gloss-key(term) = "gl-" + lower(term).replace(" ", "-").replace("’", "").replace("'", "")

// Jargon in running text, linked to its glossary entry: #jt("beta"),
// or #jt("crimp", body: [crimping]) to show different words.
#let jt(term, body: none) = {
  let shown = underline(stroke: (thickness: 0.5pt, dash: "dotted"), offset: 2pt, if body == none { term } else { body })
  navlink(label(gloss-key(term)), shown)
}

// One glossary entry. `see` lists technique keys.
#let gloss(term, body, see: ()) = block(above: 0.85em, below: 0.85em, breakable: false, {
  set text(size: fs.caption)
  set par(hanging-indent: 1em, first-line-indent: 0pt, leading: 0.78em)
  [#text(weight: 700, term)#label(gloss-key(term))#ix(term)]
  h(0.5em)
  body
  if see.len() > 0 [ See #see.map(k => tref(k)).join(", ").]
})

// Where a technique is referenced from: one link per section or entry.
#let backlink-items(key) = {
  let own = query(label("tech-" + key))
  let own-pos = if own.len() > 0 { own.first().location().position() } else { none }
  let marks = query(<tref-mark>).filter(m => m.value.key == key)
  let seen = ()
  let items = ()
  for m in marks {
    let hs = query(selector(heading).before(m.location())).filter(h => h.level <= 3 and h.at("label", default: none) != <part>)
    if hs.len() == 0 { continue }
    let h = hs.last()
    let pos = h.location().position()
    if own-pos != none and pos == own-pos { continue }
    let id = str(pos.page) + "/" + repr(pos.y)
    if id in seen { continue }
    seen.push(id)
    let pg = counter(page).at(m.location()).first()
    items.push(link(m.location())[#h.body (p.#sym.space.nobreak#pg)])
  }
  items
}

// ------------------------------------------------------------ page state

// True right after the head of a grade section (or a film strip that
// leads into an entry): the next entry starts on that same page.
#let entry-top = state("entry-top", false)
// True from the first technique entry of a chapter on: a film strip
// between entries leads into the entry that follows it.
#let entries-running = state("entries-running", false)

// ------------------------------------------------------------ boxes

// "HOW TO DO IT", "COMMON MISTAKES": letterspaced small caps, the label of
// every part of an entry and of every box.
#let section-label(body) = text(size: fs.body, sc(body, tracking: 0.08em))

// The spaces of an entry and its boxes take a factor `k`: 1 normally,
// less for an entry that would otherwise spill a few lines onto a page of
// its own (see `technique`).
#let kgap(n, k) = gap(0) + n * k * pitch

// A label and the block it belongs to: never apart. `icon` names the
// aside's icon (`aside-icons`), hung in the margin beside the label.
#let labelled(title, k: 1, icon: none) = block(above: kgap(1, k), below: kgap(0.2, k), sticky: true,
  [#aside-icon(icon)#section-label(title)])

// Lists inside entries and boxes follow their label closely.
#let list-after-label(body, k: 1) = {
  show list: set block(above: kgap(0.2, k))
  show enum: set block(above: kgap(0.2, k))
  body
}

// Every box is set off the same way: a line of space around it, a heavy
// rule above, a light rule below, and its text inset from both sides.
#let box-inset = (x: 12pt, top: 12pt, bottom: 13pt)
#let box-gap = gap(1)

// The factor `k` of the text a box sits in. `spaced` and `technique` set
// the list spacing to kgap(0.4, k), so it is read back from there; it is 1
// in ordinary running text.
#let space-k() = if type(list.spacing) == length {
  // to-absolute: a spacing given in em (as the brochure does) can't be
  // divided by a length in pt until it is resolved
  calc.min(1, calc.max(0, (list.spacing.to-absolute() - gap(0)) / (0.4 * pitch)))
} else { 1 }

// A box takes the factor of the text around it unless it is given one, so
// a box in a grade guide set with tighter space (`fit-pages`) tightens too.
// `icon` hangs an aside's icon in the margin beside the title, in line
// with the icons of labels outside boxes.
#let panel(title: none, fill: none, breakable: true, tight: false, k: auto, icon: none, body) = context {
  let k = if k == auto { space-k() } else { k }
  block(
    width: 100%, fill: fill, breakable: breakable,
    inset: (x: box-inset.x, top: box-inset.top * (0.5 + k / 2), bottom: box-inset.bottom * (0.5 + k / 2)),
    stroke: (top: rule-heavy, bottom: rule-light), above: kgap(1, k), below: kgap(1, k),
    {
      if title != none {
        block(below: kgap(0.2, k), sticky: true, [#aside-icon(icon, inset: box-inset.x)#section-label(title)])
      }
      // a box that is one list keeps it close under the label
      if tight { list-after-label(body, k: k) } else { body }
    },
  )
}

// The reading box: the one tinted panel. It is a list, set item by item
// so that a page break never parts the label from the first two items or
// the last two items from each other: a short box stays whole.
#let readbox(body, k: 1) = panel(title: [When to use it — reading the wall], icon: "reading", fill: shade, tight: true, k: k, {
  set par(justify: false)
  set list(marker: text(weight: 700)[›], indent: 0.1em, body-indent: 0.55em)
  let kids = if body.func() == [].func() { body.children } else { (body,) }
  let items = kids.filter(c => c.func() == list.item)
  let other = kids.filter(c => c.func() not in (list.item, [ ].func(), parbreak, linebreak))
  if items.len() == 0 or other.len() > 0 { body } else {
    let n = items.len()
    for (i, item) in items.enumerate() {
      block(
        above: if i == 0 { kgap(0.2, k) } else { kgap(0.4, k) }, below: kgap(0.4, k),
        breakable: false, sticky: i == 0 or i == n - 2,
        list(item),
      )
    }
  }
})

// A note box. One that follows a technique entry is kept whole (on a
// page of its own if need be), like the entry; in running text a short
// one (under a third of a page) is kept whole and a long one may break.
// A note on the subject of an aside takes its icon: `icon: "tall"`.
#let notebox(title, body, icon: none) = context {
  let h = measure(block(width: 210mm - 2 * margin-x, probe(panel(title: title, body)))).height
  let whole = entries-running.get() or h < (297mm - margin-top - margin-bottom) / 3
  panel(title: title, icon: icon, breakable: not whole, body)
}

// A quick-reminder box: "Five things to keep in mind at V3".
#let remember(title, body) = panel(title: title, breakable: false, tight: true, {
  set enum(numbering: n => text(weight: 700, str(n) + "."), body-indent: 0.6em)
  set par(justify: false)
  body
})

// A key point: the same panel, the text in italic one half step up.
#let keypoint(body) = panel(breakable: false, {
  set par(first-line-indent: 0pt)
  set par(justify: false)
  text(size: fs.lead, style: "italic", body)
})

#let mistakes(body, k: 1) = {
  labelled([Common mistakes], k: k, icon: "mistakes")
  set par(first-line-indent: 0pt)
  set list(marker: text(weight: 700)[×], body-indent: 0.55em)
  list-after-label(body, k: k)
}

// ------------------------------------------------------------ figures

#let caption-text(body) = text(size: fs.caption, style: "italic", par(leading: 0.72em, body))

// Figures in the running text float to the top of the page (or of the
// next one, when they don't fit), so they never leave a gap. A figure
// never rises above the head of its own section, though: when that head
// is on the same page (a chapter's title included), the figure goes to
// the bottom of the page when it fits there, and otherwise to the top of
// the next page.
#let float-figure(body, clearance: gap(1)) = context {
  let here-pos = here().position()
  let height = measure(block(width: 210mm - 2 * margin-x, body)).height
  let heads = query(selector(heading).before(here())).filter(h => h.at("label", default: none) != <part>)
  let under-head = heads.len() > 0 and heads.last().location().page() == here-pos.page
  // Where the figure is measured from: where its text would be without
  // it. A figure set above its text on the same page (the mark it leaves)
  // has pushed that text down by its own height.
  let mark = query(selector(<float-mark>).after(here()))
  let above = mark.len() > 0 and mark.first().location().page() == here-pos.page and mark.first().location().position().y < here-pos.y
  let y = if above { here-pos.y - height - clearance } else { here-pos.y }
  let fits = y + height + 8mm < 297mm - margin-bottom
  let mark = if probing() { none } else [#metadata("float")<float-mark>]
  place(if under-head and fits { bottom } else { top }, float: true, clearance: clearance, mark + body)
}

// A full-width drawn sequence of one movement, set apart as a feature:
// #filmstrip("filmstrip-dyno.svg", [The dyno], [One sentence on what to watch for.])
// Between technique entries it opens the page of the entry that follows.
#let filmstrip(file, title, caption) = {
  let strip = block(width: 100%, breakable: false, {
    block(below: gap(0.5), [#section-label[In motion]#h(0.7em)#text(size: fs.sub, style: "italic", title)])
    wide-image("figures/" + file)
    v(0.6em)
    align(center, block(width: 88%, align(left, caption-text(caption))))
  })
  context if entries-running.get() {
    place.flush()
    pagebreak(weak: true)
    block(below: gap(2), strip)
    entry-top.update(true)
  } else {
    float-figure(clearance: gap(1.5), strip)
  }
}

// A figure from book/figures. `width` scales it; by default it keeps the
// size it was drawn at, which keeps line weights equal across figures.
#let fig(file, caption: none, width: auto, lbl: none) = {
  let img = if width == auto { image("figures/" + file) } else { image("figures/" + file, width: width) }
  [#figure(img, caption: caption, kind: image, supplement: [Figure]) #if lbl != none { label(lbl) }]
}

// ------------------------------------------------------------ technique entry

#let technique(
  key: none,
  name: none,
  aliases: (),
  category: none,
  grade: none,
  grade-note: none,
  summary: none,
  figure: none,
  caption: none,
  figure-wide: false,
  how: none,
  when: none,
  errors: none,
  tall: none,
  related: (),
  watch: (),
  sources: (),
) = {
  // `aliases: ("one name")` is a string, not an array: accept both
  let aliases = if type(aliases) == str { (aliases,) } else { aliases }
  let meta = (key: key, name: name, aliases: aliases, category: category, grade: grade)
  // The entry, its spaces scaled by `k`. With `live` false it carries no
  // heading, labels or index marks, for measuring.
  let entry(k, live) = {
    set par(first-line-indent: 0pt)
    set list(spacing: kgap(0.4, k))
    set enum(spacing: kgap(0.4, k))
    show list: set block(above: kgap(0.5, k), below: kgap(0.5, k))
    show enum: set block(above: kgap(0.5, k), below: kgap(0.5, k))
    // title band: the name and the grade, the other names and the
    // category, then a heavy rule (sticky: never left alone at the foot
    // of a page)
    block(width: 100%, below: kgap(1, k), breakable: false, sticky: true, {
      grid(columns: (1fr, auto), column-gutter: 1em, align: (left + bottom, right + bottom),
        if live [#heading(level: 3, name)#label("tech-" + key)#metadata(meta)#label("tech-meta-" + key)#ix(name, main: true)]
        else { text(size: fs.tech, weight: 700, name) },
        navlink(label("grade-" + str(calc.min(calc.max(grade, 0), 8))), grade-tab(grade-label(grade) + "+", size: fs.badge)),
      )
      if aliases.len() > 0 or category != none {
        set par(justify: false)
        block(above: 0.85em, text(size: fs.caption)[
          #if aliases.len() > 0 [_Also called_ #aliases.join(", ")]
          #if aliases.len() > 0 and category != none [#h(0.4em)·#h(0.4em)]
          #if category != none [#navlink(label("cattable-" + category), sc(categories.at(category), tracking: 0.05em))]
        ])
      }
      block(above: 0.8em, line(length: 100%, stroke: rule-heavy))
    })
    if live { for a in aliases { ix(a + " (see " + name + ")") } }
    if summary != none { block(above: 0pt, below: kgap(0.6, k), sticky: true, text(size: fs.lead, par(summary))) }
    if grade-note != none {
      block(above: kgap(0.6, k), below: 0pt, text(size: fs.note)[#sc(tracking: 0.08em)[Grade]#h(0.6em)#grade-note])
    }
    // how-to with figure
    let howblock = {
      labelled([How to do it], k: k)
      set enum(numbering: n => text(weight: 700, str(n) + "."), body-indent: 0.5em)
      list-after-label(how, k: k)
    }
    // after the steps: the reading box, mistakes, tall climbers and the
    // entry's apparatus
    let rest = {
      if when != none { readbox(when, k: k) }
      if errors != none { mistakes(errors, k: k) }
      if tall != none {
        block(above: kgap(1, k), below: 0pt, [#aside-icon("tall")#text(weight: 700, style: "italic")[Tall climbers.] #tall])
      }
      // the entry's apparatus: related entries, videos, sources, backlinks
      let foot = ()
      if related.len() > 0 {
        foot.push([#sc[Related]#h(0.45em)#related.map(k => tref(k)).join(", ")])
      }
      // a small black tab with the link's number, matching the number under
      // its QR code (and unlike a digit in the video's title)
      let qr-num(n) = grade-tab(str(n), size: 7.2pt)
      if watch.len() > 0 {
        let items = watch.enumerate().map(((i, w)) => {
          let num = if i < 2 { [#qr-num(i + 1)#h(0.3em)] } else { [] }
          [#num#link(w.at(2))[#w.at(1)] (#w.at(0))]
        })
        foot.push([#sc[Watch]#h(0.45em)#items.join("; ")])
      }
      if sources.len() > 0 {
        foot.push([#sc[Sources]#h(0.45em)#src(..sources)])
      }
      let back = backlink-items(key)
      let back = if live { back } else { back.map(b => [#b.body.children.first() (p.#sym.space.nobreak#"000")]) }
      if back.len() > 0 {
        foot.push([#sc[Referenced from]#h(0.45em)#back.join(", ")])
      }
      if foot.len() > 0 {
        // up to two QR codes for the videos, numbered like the Watch links
        let qrs = watch.slice(0, calc.min(watch.len(), 2)).enumerate().map(((i, w)) => stack(
          spacing: 3pt,
          link(w.at(2), qrcode(w.at(2), width: 13mm)),
          align(center, qr-num(i + 1)),
        ))
        let lines = {
          set text(size: fs.note)
          set par(justify: false, leading: 0.68em, spacing: 0.75em, hanging-indent: 1em)
          for f in foot { par(f) }
        }
        block(above: kgap(1.5, k), width: 100%, breakable: true, {
          block(below: kgap(0.5, k), sticky: true, line(length: 100%, stroke: rule-light))
          if qrs.len() == 0 { lines } else {
            grid(columns: (1fr, auto), column-gutter: 14pt, lines,
              stack(spacing: 4pt,
                text(size: fs.index, style: "italic")[Scan to watch],
                stack(dir: ltr, spacing: 7pt, ..qrs)))
          }
        })
      }
    }
    let file = if figure != none { "figures/" + figure } else { none }
    let img-w = if file != none { measure(image(file)).width } else { 0pt }
    let wide = figure-wide or (file != none and img-w > 92mm)
    if file != none and not wide {
      // narrow figure: beside the steps, hanging into the right margin
      // (the grid sits in a block, since a cell ignores the space above
      // its first block)
      block(above: kgap(1, k), below: 0pt, pad(right: if img-w > 60mm { -overhang } else { 0pt }, grid(columns: (1fr, auto), column-gutter: 16pt,
        howblock,
        block(breakable: false, {
          image(file)
          if caption != none {
            v(0.6em)
            block(width: calc.max(img-w, 48mm), caption-text(caption))
          }
        }),
      )))
      rest
    } else if file != none {
      // wide figure: below the steps when it fits on the page, otherwise at
      // the top of the next page while the reading box fills this one. The
      // float sits in a block that starts after the steps, so it can't rise
      // above them.
      howblock
      block(width: 100%, breakable: true, above: kgap(1, k), {
        place(top, float: true, clearance: kgap(1, k), block(width: 100%, breakable: false, {
          wide-image(file)
          if caption != none {
            v(0.6em)
            align(center, block(width: calc.min(calc.max(img-w, 60mm), 125mm), align(left, caption-text(caption))))
          }
        }))
        rest
      })
    } else {
      howblock
      rest
    }
  }
  // Every entry starts a page, unless it follows the head of its grade
  // section on that page. Floats still waiting from the entry before are
  // set first, so they can't land on this entry's page.
  place.flush()
  context if not entry-top.get() { pagebreak(weak: true) }
  entry-top.update(false)
  entries-running.update(true)
  context {
    // An entry is set with tighter spaces when that saves it a page, i.e.
    // when it would otherwise spill a little onto a page of its own: the
    // most space (six tenths, a third or a tenth of it) that does. Its
    // height is measured each way; a line a page is added for what page
    // breaks cost (widowed lines, blocks moved whole).
    let page-h = 297mm - margin-top - margin-bottom
    let avail = 297mm - margin-bottom - here().position().y
    let pages(k) = {
      let h = measure(block(width: 210mm - 2 * margin-x, probe(entry(k, false)))).height
      let h = h + pitch * calc.ceil(h / page-h)
      if h <= avail { 1 } else { 1 + calc.ceil((h - avail) / page-h) }
    }
    let n = pages(1)
    let k = if n == 1 { 1 } else if pages(0.6) < n { 0.6 } else if pages(0.35) < n { 0.35 } else if pages(0.1) < n { 0.1 } else { 1 }
    block(breakable: true, above: 0pt, below: 0pt, width: 100%, entry(k, true) + [#metadata("end")<entry-end>])
  }
}

// ------------------------------------------------------------ fitting running text

// Running text set with its spaces scaled by `k` (see `kgap`). The space
// above a subhead shrinks to half at most, so that it stays about twice
// the space below.
#let spaced(k, body) = {
  set list(spacing: kgap(0.4, k))
  set enum(spacing: kgap(0.4, k))
  show list: set block(above: kgap(0.5, k), below: kgap(0.5, k))
  show enum: set block(above: kgap(0.5, k), below: kgap(0.5, k))
  show heading.where(level: 4): it => block(above: kgap(1.5, calc.max(k, 1 / 3)), below: kgap(0.35, k), sticky: true, text(size: fs.sub, weight: 700, it.body))
  body
}

// A stretch of running text that starts at a fixed place (a grade guide
// under its head, a chapter's opening sections) and ends where a new page
// begins. Like an entry, it is set with tighter space when that saves it
// a page of a few lines: #fit-pages[...].
#let fit-pages(body) = context {
  let page-h = 297mm - margin-top - margin-bottom
  let avail = 297mm - margin-bottom - here().position().y
  let pages(k) = {
    let h = measure(block(width: 210mm - 2 * margin-x, probe(spaced(k, body)))).height
    let h = h + pitch * calc.ceil(h / page-h)
    if h <= avail { 1 } else { 1 + calc.ceil((h - avail) / page-h) }
  }
  let n = pages(1)
  let k = if n == 1 { 1 } else if pages(0.6) < n { 0.6 } else if pages(0.35) < n { 0.35 } else if pages(0.1) < n { 0.1 } else { 1 }
  spaced(k, body)
}

// ------------------------------------------------------------ generated tables

#let all-techniques() = query(<technique-meta-dummy>)

#let tech-metas() = query(metadata).filter(m => type(m.value) == dictionary and "category" in m.value and "grade" in m.value)

// The page of a technique for the generated tables ("000" in a measured
// copy, which may not depend on page numbers).
#let tech-pg(m) = if probing() { "000" } else { str(counter(page).at(m.location()).first()) }

// Tables: a light rule under the head; the heavy rule above and the light
// rule below come from the table show rule in `book`. Rows are parted by
// space, not by rules.
#let head-rule = (x, y) => if y == 0 { (bottom: rule-light) }
#let row-rules = head-rule
#let cell-inset = (x: 5pt, y: 5pt)

// A table with the book's style (chapters use it through `gtable` etc.).
#let data-table(columns: auto, ..args) = table(
  columns: columns, stroke: head-rule, inset: cell-inset, align: left + top, ..args,
)

// Table of the techniques in one category, ranked by grade, in two columns.
#let category-table(cat) = [#metadata(cat)#label("cattable-" + cat)] + context {
  let ms = tech-metas().filter(m => m.value.category == cat)
  let rows = ms.sorted(key: m => (m.value.grade, lower(m.value.name)))
  let half = calc.ceil(rows.len() / 2)
  let tab(rs) = table(
    columns: (auto, 1fr, auto),
    stroke: head-rule,
    inset: (x: 5pt, y: 4.2pt),
    align: (left + horizon, left + horizon, right + horizon),
    table.header(th[Grade], th[Technique], th[Page]),
    ..rs.map(m => (
      badge-plain(m.value.grade),
      link(m.location(), m.value.name),
      link(m.location(), tech-pg(m)),
    )).flatten(),
  )
  block(above: gap(1), below: gap(1.5), breakable: false,
    grid(columns: (1fr, 1fr), column-gutter: 1.8em, tab(rows.slice(0, half)), tab(rows.slice(half))))
}

// Techniques that become important at one grade (for the grade guides).
#let grade-techniques(g) = context {
  let ms = tech-metas().filter(m => if g >= 8 { m.value.grade >= 8 } else { m.value.grade == g })
  if ms.len() == 0 { block(above: gap(0.5), par(first-line-indent: 0pt, emph[None listed.])) } else {
    let rows = ms.sorted(key: m => (m.value.category, lower(m.value.name)))
    table(
      columns: (1fr, auto, auto),
      stroke: head-rule,
      inset: (x: 5pt, y: 4.2pt),
      align: (left, left, right),
      table.header(th[Technique], th[Category], th[Page]),
      ..rows.map(m => (
        link(m.location(), m.value.name),
        text(style: "italic", categories.at(m.value.category)),
        link(m.location(), tech-pg(m)),
      )).flatten(),
    )
  }
}

// The A–Z list of every technique and alias, in two columns with leaders.
#let a-to-z() = context {
  let ms = tech-metas()
  let rows = ()
  for m in ms {
    // sorted as the index sorts: "Hand–foot match" before "Handle"
    rows.push((sort: ix-fold(m.value.name), name: m.value.name, see: none, m: m))
    for a in m.value.aliases {
      rows.push((sort: ix-fold(a), name: a, see: m.value.name, m: m))
    }
  }
  rows = rows.sorted(key: r => r.sort)
  let dots = box(width: 1fr, repeat(gap: 0.25em, text(size: 0.8em, ".")))
  set text(size: fs.caption, number-type: "lining")
  set par(justify: false, leading: 0.72em, spacing: 0.72em, hanging-indent: 1em, first-line-indent: 0pt)
  block(above: gap(1.5), columns(2, gutter: 2em, {
    let last-letter = none
    for r in rows {
      let letter = upper(ix-fold(r.sort).first())
      if last-letter != none and letter != last-letter { v(gap(0.5), weak: true) }
      last-letter = letter
      let loc = r.m.location()
      let pg = str(counter(page).at(loc).first())
      if r.see == none {
        par[#link(loc, strong(r.name))#h(0.3em)#dots#h(0.3em)#box(width: 2.1em, badge-plain(r.m.value.grade))#box(width: 1.6em, align(right, link(loc, pg)))]
      } else {
        par[#link(loc)[#r.name #arrow _#r.see _]#h(0.3em)#dots#h(0.3em)#box(width: 1.6em, align(right, link(loc, pg)))]
      }
    }
  }))
}

// ------------------------------------------------------------ document

#let number-words = ("One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve")

// A part page: the part's hold (from `ornaments`, or `ornament` by name),
// its label and its subtitle.
#let part(title, subtitle: none, ornament: auto) = {
  pagebreak(weak: true)
  entries-running.update(false)
  [#metadata("part-page")<part-page>]
  v(1fr)
  align(center, {
    let name = if ornament == auto { ornaments.parts.at(title, default: ornaments.other-part) } else { ornament }
    fleuron(size: 24pt, name: name)
    v(12mm)
    if subtitle != none {
      text(size: fs.sub, sc(title, tracking: 0.24em))
      v(8mm)
      block(width: 80%, text(size: fs.part-sub, style: "italic", hyphenate: false, par(justify: false, leading: 0.5em, subtitle)))
    } else {
      text(size: fs.chapter, style: "italic", title)
    }
  })
  v(1.6fr)
  // an invisible heading puts the part in the contents and the bookmarks
  [#heading(level: 1, numbering: none, bookmarked: true, outlined: true)[#title#if subtitle != none [ — #subtitle]] <part>]
}

// The head of a section named after a grade: "V0: standing on holds",
// "VB–V0 (Font 3–4+)". Returns the grade phrase and the rest, or none.
#let grade-head-re = regex("^(V[B0-9]+(?:–V[0-9]+)?(?: and (?:up|above))?)(?:: (.+)| \((.+)\))?$")
#let grade-head(it) = {
  let m = plain(it.body).match(grade-head-re)
  if m == none { none } else { (grade: m.captures.at(0), title: m.captures.at(1), font: m.captures.at(2)) }
}

#let book(title: none, subtitle: none, author: none, body) = {
  set document(title: title, author: author)
  set page(
    paper: "a4",
    margin: (top: margin-top, bottom: margin-bottom, x: margin-x),
    header-ascent: 10mm,
    // The running head: folio and chapter on the left, the navigation on
    // the right, a light rule below. Part pages have none; chapter
    // openings keep the folio and the navigation but not the chapter name.
    header: context {
      let pg = here().page()
      let on-part = query(<part-page>).filter(m => m.location().page() == pg).len() > 0
      if not on-part {
        let h1 = query(heading.where(level: 1))
        let chs = h1.filter(h => h.location().page() <= pg and h.at("label", default: none) != <part>)
        let opening = h1.filter(h => h.location().page() == pg).len() > 0
        set text(size: fs.note, number-type: "old-style")
        set par(justify: false, first-line-indent: 0pt)
        let dot = h(0.45em) + sym.dot.c + h(0.45em)
        let nav = sc(tracking: 0.05em)[#navlink(<contents>)[Contents]#dot#navlink(<a-to-z>)[A–Z]#dot#navlink(<troubleshooting>)[Troubleshooting]#dot#navlink(<glossary>)[Glossary]#dot#navlink(<index>)[Index]]
        let running = if chs.len() > 0 and not opening {
          let t = plain(chs.last().body)
          link(chs.last().location(), emph(if t.contains(":") { t.split(":").first() } else { chs.last().body }))
        }
        pad(x: -overhang, {
          grid(columns: (auto, 1fr, auto), column-gutter: 1.1em, align: bottom,
            text(weight: 700, counter(page).display()), running, nav)
          v(5pt)
          line(length: 100%, stroke: rule-light)
        })
      }
    },
    footer: none,
  )
  set text(font: serif, size: fs.body, lang: "en", region: "gb", hyphenate: true, number-type: "old-style", top-edge: cap)
  // Grades and Font grades take lining figures: V3, 6A+.
  show regex("\bV\d+|\b\d[ABC]\b"): set text(number-type: "lining")
  // Running text: paragraphs are marked by an indent, not by space; space
  // is kept for the boundaries between blocks.
  set par(justify: true, leading: lead, spacing: lead, first-line-indent: 1.5em)
  // Lists: items half a line apart, the list half a line from the text.
  set list(indent: 0.25em, body-indent: 0.5em, spacing: gap(0.4), marker: text(size: 0.9em, [•]))
  set enum(indent: 0.1em, body-indent: 0.5em, spacing: gap(0.4))
  show list: set block(above: gap(0.5), below: gap(0.5))
  show enum: set block(above: gap(0.5), below: gap(0.5))
  show list: set par(first-line-indent: 0pt)
  show enum: set par(first-line-indent: 0pt)
  show link: it => it
  // Reference matter set in columns (glossary, A–Z, sources, index) uses
  // the outer frame.
  show columns: it => block(above: gap(1.5), pad(x: -overhang, it))
  show cite: set text(size: 0.9em)
  set heading(numbering: (..n) => {
    let n = n.pos()
    if n.len() == 1 { str(n.first()) } else if n.len() == 2 { str(n.at(0)) + "." + str(n.at(1)) } else { none }
  })
  show heading: set text(font: serif, hyphenate: false)
  show heading: set par(justify: false, first-line-indent: 0pt)
  // Chapter openings: a new page, sunk a little; the chapter number in
  // small caps, the title on the scale's chapter step, the chapter's hold
  // between two short light rules (`ornaments`), and three empty lines
  // before the text.
  show heading.where(level: 1): it => {
    if it.at("label", default: none) == <part> {
      pagebreak()
      return
    }
    pagebreak(weak: true)
    entry-top.update(false)
    entries-running.update(false)
    v(gap(2))
    block(width: 100%, below: gap(3), align(center, {
      if it.numbering != none {
        let n = counter(heading).get().first()
        text(size: fs.sub, sc(tracking: 0.22em)[Chapter #number-words.at(n - 1, default: str(n))])
        v(gap(0.5))
      }
      block(width: 88%, text(size: fs.chapter, weight: 400, par(leading: 0.45em, it.body)))
      v(gap(1))
      let name = if it.numbering != none {
        ornaments.chapters.at(str(counter(heading).get().first()), default: ornaments.other)
      } else { ornaments.other }
      orn-rule(width: 9mm, size: 5mm, name: name)
    }))
  }
  // Sections. Every section head is a heading in the heading type, with
  // its own text; a grade only adds a marker. A section named after a
  // grade (Part II) starts a page and carries its grade on a tab at the
  // right end of the head, as an entry's title band does. A grade guide
  // (Part III) is a major division: it starts a page, its head is one
  // step larger and its tab larger still.
  show heading.where(level: 2): it => {
    let lbl = it.at("label", default: none)
    let lbl = if lbl == none { "" } else { str(lbl) }
    let g = grade-head(it)
    let guide = lbl.starts-with("grade")
    let marker = if guide and g == none { "V4–V5" } else if g != none { grade-marker(g.grade) }
    let size = if guide { fs.guide } else { fs.section }
    let head = context {
      set text(size: size)
      let num = if it.numbering != none [#text(number-type: "old-style", counter(heading).display())#h(0.45em)]
      set par(leading: 0.42em, hanging-indent: if num != none { measure(num).width } else { 0pt })
      [#num#it.body]
    }
    if guide or (g != none and g.title != none) {
      pagebreak(weak: true)
      if guide { entries-running.update(false) } else { entry-top.update(true) }
      block(width: 100%, above: 0pt, below: if guide { gap(2) } else { gap(2.5) }, sticky: true,
        grid(columns: (1fr, auto), column-gutter: 1em, align: (left + bottom, right + bottom),
          head, grade-tab(marker, size: if guide { fs.guide-tab } else { fs.section })))
    } else {
      block(width: 100%, above: gap(2.5), below: gap(0.9), sticky: true, head)
    }
  }
  show heading.where(level: 3): it => text(size: fs.tech, weight: 700, it.body)
  show heading.where(level: 4): it => block(above: gap(1.5), below: gap(0.35), sticky: true, text(size: fs.sub, weight: 700, it.body))
  // A head that runs to two lines is broken as a whole, so that no word is
  // left alone on the last line, and never inside a compound such as
  // "comp-style" or "V0–V1". A head tied with no-break spaces keeps the
  // breaks it was given. (This rule comes after the ones above, so that it
  // applies first and their output inherits it.)
  show heading: it => {
    show regex("[\p{L}\p{N}]+([-–][\p{L}\p{N}]+)+"): box
    if plain(it.body).contains("\u{a0}") { it } else {
      set text(costs: (runt: 1000000%))
      set par(linebreaks: "optimized")
      it
    }
  }
  // Figures: the drawing (allowed into the margins when wide) and an
  // italic caption led by the figure number in small caps.
  show figure.caption: it => {
    set par(justify: false, first-line-indent: 0pt, leading: 0.72em)
    text(size: fs.caption)[#sc(tracking: 0.05em)[#it.supplement #context it.counter.display(it.numbering)]#h(0.5em)#emph(it.body)]
  }
  // Narrow figures take their caption beside them.
  show figure: it => float-figure(block(width: 100%, breakable: false, context {
    let w = measure(it.body).width
    if w < 80mm {
      align(center, grid(columns: (w, 62mm), column-gutter: 7mm, align: bottom, it.body, it.caption))
    } else {
      pad(x: -overhang, align(center, it.body))
      v(0.7em)
      align(center, block(width: calc.min(calc.max(w, 70mm), 130mm), align(left, it.caption)))
    }
  }))
  // Tables: a heavy rule above, a light rule under the head and another
  // below; small caps heads; lining figures.
  set table(stroke: head-rule, inset: cell-inset)
  show table.cell.where(y: 0): it => {
    show strong: s => sc(s.body, tracking: 0.05em)
    it
  }
  show table: it => {
    set text(size: fs.caption, number-type: "lining")
    set par(justify: false, first-line-indent: 0pt, leading: 0.6em)
    block(above: gap(1), below: gap(1), inset: (top: 2pt, bottom: 3pt), stroke: (top: rule-heavy, bottom: rule-light), it)
  }
  // The contents: parts in small caps, chapters in bold, sections indented,
  // dotted leaders to lining page numbers.
  show outline.entry: it => {
    let el = it.element
    let pg = text(number-type: "lining", it.page())
    let dots = box(width: 1fr, repeat(gap: 0.3em, text(size: 0.8em, ".")))
    if it.level == 1 and el.at("label", default: none) == <part> {
      let t = plain(el.body).split(" — ")
      block(above: gap(1.25), below: gap(0.4), sticky: true, link(el.location(), {
        sc(tracking: 0.08em, t.first())
        if t.len() > 1 { h(0.6em); emph(t.slice(1).join(" — ")) }
      }))
    } else if it.level == 1 {
      block(above: gap(0.4), below: 0.6em, sticky: true, link(el.location(), {
        let pre = it.prefix()
        strong[#box(width: 1.6em, if pre != none { pre })#it.body()]
        h(0.4em); dots; h(0.4em); pg
      }))
    } else {
      block(above: 0.6em, below: 0.6em, pad(left: 1.6em, link(el.location(), {
        let pre = it.prefix()
        box(width: 2.3em, if pre != none { text(number-type: "lining", pre) })
        it.body(); h(0.4em); dots; h(0.4em); pg
      })))
    }
  }
  body
}
