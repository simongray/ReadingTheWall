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
  section: 21.8pt,  // +4: numbered sections
  guide: 26.1pt,    // +5: grade guides
  part-sub: 26.1pt, // +5: part titles
  chapter: 31.4pt,  // +6: chapter titles
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
#let page-height = 297mm - margin-top - margin-bottom

// Vertical space is measured in lines of text. Text edges are set at the
// cap height and the baseline, so the space between two blocks of text is
// the white between a baseline and the next capitals: `gap(n)` is the
// space that adds n empty lines to the normal line spacing.
#let cap = 0.7em
#let pitch = 16.5pt                          // baseline to baseline at 10.5 pt
#let lead = (pitch / fs.body - 0.7) * 1em    // the leading that gives it
#let gap(n) = pitch - 0.7 * fs.body + n * pitch

// Ragged text. Its lines are weighed over the whole paragraph, as in justified text,
// so that no word is left alone on a last line when the others can make room for it.
// A compound stays whole, since a rag can spare the room: "toe-/hook" reads as two words.
#let keep-compounds(body) = {
  show regex("[\p{L}\p{N}]+(-[\p{L}\p{N}]+)+"): box
  body
}
#let ragged(body) = {
  set par(justify: false, linebreaks: "optimized")
  set text(costs: (runt: 2000%))
  keep-compounds(body)
}

// The number of a numbered list, bold and flush right in a column of one width. A long
// list is set in parts (`keep-list`), and without this each part would size its column
// by its own figures, which differ in width, so the text edge would jog.
#let step-number(n) = box(width: if n < 10 { 0.9em } else { 1.4em }, align(right, text(weight: 700, str(n) + ".")))

// A caption sits one line under its drawing, closer to it than to what follows.
#let caption-gap = gap(0)

#let smcp = ("c2sc", "smcp")
// True small caps with light letterspacing.
// A figure stays out of them: under these features a 0 reads as the letter O and a 1 as
// the letter I, so it is a lining figure scaled to the small caps.
#let sc(body, tracking: 0.06em) = {
  show regex("\d+"): it => text(features: (c2sc: 0, smcp: 0), number-type: "lining", size: 0.8em, it)
  text(features: smcp, tracking: tracking, body)
}
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
  small: "small",         // Small climbers: a shorter mannequin stretching up to a jug out of reach
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
    box(width: overhang, align(right, image("figures/icon-" + aside-icons.at(name, default: name) + ".svg", height: 7mm)))))
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

// Content measured before it is set (a note box, a part, the steps beside a
// figure, the last page of columns) is marked by this region, so that cross-references in it leave out their links and marks:
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

// A citation stays with the word before it. A group of up to four numbers is never
// broken, since half a citation alone on a line reads as a stray; a longer one, as in
// an entry's Sources line, may break after a comma.
#let src(..keys) = {
  let ks = keys.pos()
  let group = for k in ks { cite(label(src-map.at(k, default: k))) }
  sym.wj
  if ks.len() <= 4 { box(group) } else { group }
}

// The evidence line of an entry, a prototype that is off by default. With
// `--input evidence=1` each entry's apparatus counts its sources by kind,
// using book/source-kinds.yaml. A source missing from that file counts as
// "other".
#let evidence-on = sys.inputs.at("evidence", default: none) == "1"
#let source-kinds = if evidence-on {
  let kinds = yaml("source-kinds.yaml")
  if kinds == none { (:) } else { kinds }
} else { (:) }
#let evidence-groups = (
  (kinds: ("study", "review"), one: "study", many: "studies"),
  (kinds: ("book",), one: "book", many: "books"),
  (kinds: ("governing-body",), one: "coaching body", many: "coaching bodies"),
  (kinds: ("coach", "gym", "magazine", "brand", "video"), one: "coach, gym or magazine", many: "coaches, gyms and magazines"),
  (kinds: ("forum", "wiki"), one: "forum or wiki", many: "forums and wikis"),
)
#let evidence-line(sources) = {
  // two keys that map onto one source count once
  let kinds = sources.map(k => src-map.at(k, default: k)).dedup().map(k => source-kinds.at(k, default: none))
  let known = evidence-groups.map(g => g.kinds).flatten()
  let parts = ()
  for g in evidence-groups {
    let n = kinds.filter(x => x in g.kinds).len()
    if n > 0 { parts.push(str(n) + " " + if n == 1 { g.one } else { g.many }) }
  }
  let other = kinds.filter(x => x not in known).len()
  if other > 0 { parts.push(str(other) + " other") }
  parts.join(" · ")
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
  "corner": "Corners",
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

// Items set in n columns, the columns of the last page even. Each item leaves a
// mark, so the pass after tells where the last page starts; what lies on it is
// set in a block of its own, a little over an nth of its height. The last page
// starts a page earlier when the items of both fit on it, or an early pass could
// leave a few items on a page of their own. (`sizes` is a copy of the items to
// measure, with no links, since a measurement of a link doesn't settle.) `margin` is what
// a column may run over an nth: the smallest that leaves nothing over depends on how the
// last items fall, so each caller sets its own.
#let balanced-columns(id, n, items, gutter: 1.4em, sizes: none, margin: pitch) = context {
  let sizes = if sizes == none { items } else { sizes }
  let w = (page.width - 2 * margin-x + 2 * overhang - (n - 1) * gutter) / n
  let height-from(i) = measure(block(width: w, probe(sizes.slice(i).join()))).height
  let marks = query(selector(<col-item>)).filter(m => m.value.id == id)
  let last = marks.map(m => m.location().page()).fold(0, calc.max)
  let first-on(pg) = marks.filter(m => m.location().page() == pg).map(m => m.value.i).first(default: 0)
  let cut = if marks.len() == items.len() {
    let earlier = first-on(last - 1)
    if earlier > 0 and height-from(earlier) / n + margin <= page-height { earlier } else { first-on(last) }
  } else { 0 }
  let tagged = items.enumerate().map(((i, c)) => [#metadata((id: id, i: i))<col-item>#c])
  if cut > 0 {
    columns(n, gutter: gutter, tagged.slice(0, cut).join())
    pagebreak()
    block(height: height-from(cut) / n + margin, columns(n, gutter: gutter, tagged.slice(cut).join()))
  } else {
    columns(n, gutter: gutter, tagged.join())
  }
}

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
  set par(justify: false, hanging-indent: 2em, leading: 0.72em, first-line-indent: 0pt)
  set text(size: fs.index, number-type: "lining")
  // Each line's text, with links to set and without them to measure, under its letter.
  let rows = ()
  {
    for g in keys {
      let k = shown.at(g)
      let parts = k.split("!")
      let head = heads.at(lower(parts.first()))
      let letter = upper(ix-fold(head).first())
      if letter != last-letter {
        rows.push((letter: letter, kind: "letter", body: none, plain: none))
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
      let plainrefs = pages.map(r => if r.main { strong(str(r.page)) } else { str(r.page) }).join(", ")
      // the word and its first page number stay on one line
      let tie = [#sym.wj#h(0.45em)#sym.wj]
      if parts.len() == 1 {
        rows.push((letter: letter, kind: "entry", parent: head, body: [#head#tie#refs], plain: [#head#tie#plainrefs]))
        last-head = lower(head)
      } else {
        if lower(head) != last-head {
          rows.push((letter: letter, kind: "parent", parent: head, body: [#head], plain: [#head]))
          last-head = lower(head)
        }
        rows.push((letter: letter, kind: "sub", parent: head, body: [#h(0.9em)#parts.at(1)#tie#refs], plain: [#h(0.9em)#parts.at(1)#tie#plainrefs]))
      }
    }
  }
  // A line never breaks, a head stays with its sub-entries, and two lines stay together
  // at each end of a letter's group. A head with up to four sub-entries stays whole with
  // them. Under a longer one two sub-entries stay together at each end, and the head
  // repeats at the top of a column, since a reader who sees one page at a time can't see
  // it on the page before.
  let line(body) = block(above: 0.75em, below: 0.75em, breakable: false, par(body))
  let groups = ()
  let i = 0
  while i < rows.len() {
    let r = rows.at(i)
    let j = i + 1
    if r.kind != "letter" {
      while j < rows.len() and rows.at(j).kind == "sub" and rows.at(j).parent == r.parent { j += 1 }
    }
    groups.push(rows.slice(i, j))
    i = j
  }
  let set-group(k, field) = {
    let g = groups.at(k)
    let r = g.first()
    if r.kind == "letter" { return block(above: 1.6em, below: 0.75em, sticky: true, text(size: fs.sub, weight: 700, r.letter)) }
    let same-letter(n) = n < groups.len() and groups.at(n).first().letter == r.letter
    let keep = same-letter(k + 1) and not same-letter(k + 2)
    if g.len() <= 5 {
      block(above: 0.75em, below: 0.75em, breakable: false, sticky: keep, g.map(x => line(x.at(field))).join())
    } else {
      let subs = g.slice(1).map(x => line(x.at(field)))
      let n = subs.len()
      block(above: 0.75em, below: 0.75em, grid(columns: 1fr, row-gutter: 0.75em,
        grid.header(par(r.at(field))),
        block(breakable: false, subs.slice(0, 2).join()),
        ..subs.slice(2, n - 2),
        block(breakable: false, subs.slice(n - 2).join())))
    }
  }
  let items = range(groups.len()).map(k => set-group(k, "body"))
  let sizes = range(groups.len()).map(k => set-group(k, "plain"))
  balanced-columns("index", 3, items, sizes: sizes, margin: 1.3 * pitch)
}

// The sources of one research file (research/A-sources.yml and so on) for
// bibliography(). The access date is the same for every web page and is given
// above the list, so it is left out of the entries: each URL keeps its value,
// not its date.
#let source-list(letter) = {
  let data = yaml("../research/" + letter + "-sources.yml")
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
#let source-files = ("A", "B", "C", "D", "E", "F", "G", "H").map(source-list)

// The sources, set in two columns with the last page even. The bibliography is one
// element, so its entries can't be handed to `balanced-columns`. Instead the columns
// sit in a block of a set height, which is shared out over the pages, so that only the
// last page gets shorter columns: `pages` pages, the last with columns `last` tall. The
// two numbers have to be given, since working them out from the layout doesn't settle
// within Typst's five passes. tools/check_fit.py fails the build if they drop a source,
// and says when the columns of the last page come out uneven. website/template.typ has
// its own version of this macro.
#let sources-columns(body, pages: 1, last: auto) = {
  show columns: it => context {
    let first = page.height - margin-bottom - here().position().y - gap(1.5)
    block(above: gap(1.5), breakable: true, height: if last == auto { auto } else { first + (pages - 2) * page-height + last }, it)
  }
  columns(2, gutter: 1.5em, {
    set text(size: fs.index)
    set par(justify: false, leading: 0.72em, spacing: 0.95em, first-line-indent: 0pt)
    body
  })
}

// ------------------------------------------------------------ the grade mark

#let grade-label(g) = if g == none { "—" } else if g < 0 { "VB" } else if g >= 8 { "V8+" } else { "V" + str(g) }

// Each grade's tab colour, from V0 up, as on the walls at Boulders, the Danish
// gym chain. It publishes no V grades, so the table comes from Simon, who climbs
// there. The tabs darken as the grade rises, so on a monochrome screen a tab's
// tone still says how hard the grade is. Light tabs take black figures and an
// outline; dark ones take white figures. Each colour holds its panel level like
// the figures' colours (figtools/paint.py).
#let tab-green = (fill: rgb("#a2dea2"), figures: ink, stroke: 0.4pt + ink)
#let grade-tabs = (
  tab-green,                                                  // V0
  tab-green,                                                  // V1
  (fill: rgb("#d7be2e"), figures: ink, stroke: 0.4pt + ink),  // V2, yellow
  (fill: rgb("#e98421"), figures: ink, stroke: 0.4pt + ink),  // V3, orange
  (fill: rgb("#3b69ae"), figures: white, stroke: none),       // V4, blue
  (fill: rgb("#58328a"), figures: white, stroke: none),       // V5, purple
  (fill: rgb("#6b211b"), figures: white, stroke: none),       // V6, red
  (fill: ink, figures: white, stroke: none),                  // V7 and up, black
)
#let grade-tab-look(g) = if g == none { (fill: ink, figures: white, stroke: none) } else {
  grade-tabs.at(calc.clamp(g, 0, grade-tabs.len() - 1))
}

// The grade mark: lining figures on a coloured tab. One design at two
// sizes: in running text and in an entry's title band. It marks an entry
// and never replaces a heading. A section head that names a grade has no
// tab, since it would only repeat the head. The proportions are in em, so
// every size is the same shape. Without a grade `g` the tab is black, as on
// the numbers beside the QR codes.
#let grade-tab(body, size: 9pt, g: none) = {
  let look = grade-tab-look(g)
  text(
    size: size, weight: 700, fill: look.figures, number-type: "lining", tracking: 0.02em, top-edge: cap,
    box(fill: look.fill, stroke: look.stroke, inset: (x: 0.34em, y: 0.2em), radius: 0.09em, baseline: 0.2em, body),
  )
}

// The same tab in running text, its colour drawn behind the figures
// instead of around them: the figures sit on the baseline and the line
// keeps its height, as the tab takes no more room than the figures do.
#let grade-tab-inline(body, size: 9pt, g: none) = {
  let look = grade-tab-look(g)
  text(
    size: size, weight: 700, fill: look.figures, number-type: "lining", tracking: 0.02em, top-edge: cap,
    context {
      let figs = [#h(0.34em)#body#h(0.34em)]
      let w = measure(figs).width
      box(width: w, {
        place(top + left, dy: -0.2em, rect(width: w, height: 1.1em, fill: look.fill, radius: 0.09em, stroke: look.stroke))
        figs
      })
    },
  )
}

// The grade badge of a technique in running text: the grade where it
// starts to matter.
#let badge(g, size: 9pt) = grade-tab-inline(grade-label(g) + "+", size: size, g: g)

// The grade in tables and lists: small caps, no tab.
#let badge-plain(g) = text(number-type: "lining", grade-label(g))

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

// The key of the entry that a reference lands on. An entry with this very
// key wins, so an entry stays reachable until it is merged. After the merge
// the key follows key-alias.typ to the entry that absorbed it. A key with no
// entry either way shows as [?key].
#let resolve-key(key) = if query(label("tech-meta-" + key)).len() > 0 { key } else { key-alias.at(key, default: key) }

// The page after a technique's name: "Heel hook (p. 34)", or inside parentheses
// "(Heel hook, p. 34)". In ragged text, a list of references say, it is tied to the
// name so that it never stands alone on a line, and a short name and its page stay
// whole, so that such a list breaks at its commas. In justified text they stay free,
// as an unbreakable name and page would stretch the line before it.
#let tref-page(pg, inner, tied) = {
  let sep = if tied { sym.space.nobreak } else { [ ] }
  text(weight: "regular", if inner [,#sep;p.#sym.space.nobreak#pg] else [#sep;(p.#sym.space.nobreak#pg)])
}

#let short-name(name) = plain(name).len() <= 22
// (no-break spaces, not a box: a ragged line is weighed by its spaces, so a line of boxes
// counts as badly filled. A name with figures would lose its lining figures, so it is boxed.)
#let unbroken(name) = if plain(name).match(regex("\d")) != none { box(name) } else {
  show " ": sym.space.nobreak
  name
}
#let tref-set(name, pg, show-page, inner) = {
  let tied = not par.justify
  let set-name = if tied and short-name(name) { unbroken(tref-name(name)) } else { tref-name(name) }
  [#set-name#if show-page { tref-page(pg, inner, tied) }]
}

// The exercises booklet refers to the book's entries and sections. It is
// compiled with `--input booklet=1`, and reads their pages from
// book/book-pages.json, which tools/book_pages.py writes from the book.
#let in-booklet = sys.inputs.at("booklet", default: none) == "1"
#let book-pages = if in-booklet { json("book-pages.json") }

#let tref(key, body: none, show-page: true, inner: false) = context {
  let key = resolve-key(key)
  let q = query(label("tech-meta-" + key))
  let outside = book-pages
  if probing() {
    let name = if body == none and q.len() > 0 { q.first().value.name } else if body == none { key } else { body }
    tref-set(name, "000", show-page, inner)
  } else if q.len() == 0 and outside != none and key in outside.tech {
    // an entry of the book, from the booklet: no link
    let m = outside.tech.at(key)
    tref-set(if body == none { m.name } else { body }, m.page, show-page, inner)
  } else if q.len() == 0 {
    text(fill: red, weight: 700)[[?#key]]
  } else {
    let m = q.first()
    let name = if body == none { m.value.name } else { body }
    let pg = counter(page).at(m.location()).first()
    [#metadata((key: key))<tref-mark>#link(m.location(), tref-set(name, pg, show-page, inner))]
  }
}

// ------------------------------------------------------------ glossary

#let gloss-key(term) = "gl-" + lower(term).replace(" ", "-").replace("’", "").replace("'", "")

// Jargon in running text, linked to its glossary entry: #jt("beta"),
// or #jt("crimp", body: [crimping]) to show different words.
#let jt(term, body: none) = {
  let word = text(hyphenate: false, if body == none { term } else { body })
  // the booklet has no glossary, so its terms are not marked
  if in-booklet { word } else {
    navlink(label(gloss-key(term)), underline(stroke: (thickness: 0.5pt, dash: "dotted"), offset: 2pt, word))
  }
}

// A section or figure of the book, from the booklet: "Section 2.4 (p. 14)", or
// "Figure 72c (p. 251)" with sub: "c". `body` replaces the name and number.
#let bref(lbl, body: none, sub: "") = {
  let r = book-pages.refs.at(lbl, default: none)
  if r == none { text(fill: red, weight: 700)[[?#lbl]] } else {
    [#if body == none [#r.supplement~#r.number#sub] else { body } (p.~#r.page)]
  }
}

// The glossary's entries in two columns, the last page even. website/template.typ
// has its own version of this macro.
#let glossary-columns(body) = {
  let items = body.children.filter(c => c.func() not in ([ ].func(), parbreak))
  balanced-columns("glossary", 2, items, gutter: 1.6em)
}

// One glossary entry. `see` lists technique keys, as links with no page: the A–Z
// right after the glossary gives the pages. (With pages, the layout took more
// passes to settle than Typst makes.)
#let gloss(term, body, see: ()) = block(above: 1.15em, below: 1.15em, breakable: false, ragged({
  set text(size: fs.caption)
  par(hanging-indent: 1em, first-line-indent: 0pt, leading: 0.78em)[#text(weight: 700, term)#label(gloss-key(term))#ix(term)#h(0.5em)#body#if see.len() > 0 [ See #see.map(k => tref(k, show-page: false)).join(", ").]]
}))

// Where a technique is referenced from: one link per section or entry.
// (`measuring`: with no links and a set page number, since a measurement of those doesn't settle)
#let backlink-items(key, measuring: false) = {
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
    // A head tied for its own line breaks is free here. A grade keeps its Font grade,
    // and a short head stays whole with its page, as a reference does.
    let t = plain(h.body)
    let grade = t.match(regex("^V\S+.* \(Font")) != none
    let title = if grade { box(h.body) } else if short-name(t) { unbroken(h.body) } else {
      show "\u{a0}": " "
      h.body
    }
    let item = [#title#tref-page(if measuring { "000" } else { pg }, false, true)]
    items.push(if measuring { item } else { link(m.location(), item) })
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

// A label and the block it belongs to: never apart. `icon` names the
// aside's icon (`aside-icons`), hung in the margin beside the label.
#let labelled(title, icon: none) = block(above: gap(1), below: gap(0.2), sticky: true,
  [#aside-icon(icon)#section-label(title)])

// Lists inside entries and boxes follow their label closely.
#let list-after-label(body) = {
  show list: set block(above: gap(0.2))
  show enum: set block(above: gap(0.2))
  body
}

// Every box is set off the same way: a line of space around it, a heavy
// rule above, a light rule below, and its text inset from both sides.
#let box-inset = (x: 12pt, top: 12pt, bottom: 13pt)
#let box-gap = gap(1)

// A list of up to three items stays whole unless it is long; a longer one keeps
// its first two and its last two items together. (<kept> marks a part already made.)
#let keep-list(make, it) = {
  if it.at("label", default: none) == <kept> or probing() { return it }
  let n = it.children.len()
  let chars = it.children.map(c => plain(c.body).len()).sum(default: 0)
  if n <= 3 and chars < 900 { return block(width: 100%, breakable: false, it) }
  if n < 4 { return it }
  let st = if make == enum { let x = it.at("start", default: auto); if x == auto { 1 } else { x } } else { 1 }
  let part(from, to) = [#make(..if make == enum { (start: st + from) } else { (:) }, ..it.children.slice(from, to)) <kept>]
  let sp = it.at("spacing", default: auto)
  let sp = if type(sp) == length { sp } else { gap(0.4) }
  block(width: 100%, breakable: false, below: sp, part(0, 2))
  if n > 4 { block(width: 100%, above: sp, below: sp, breakable: true, part(2, n - 2)) }
  block(width: 100%, breakable: false, above: sp, part(n - 2, n))
}

// A box. `icon` hangs an aside's icon in the margin beside the title, in line
// with the icons of labels outside boxes. A box that may break repeats its title
// above the rest on the next page.
#let panel(title: none, fill: none, breakable: true, tight: false, icon: none, body) = block(
  width: 100%, fill: fill, breakable: breakable, inset: box-inset,
  stroke: (top: rule-heavy, bottom: rule-light), above: gap(1), below: gap(1),
  {
    // a box that is one list keeps it close under the label
    let content = if tight { list-after-label(body) } else { body }
    let label = [#aside-icon(icon, inset: box-inset.x)#section-label(title)]
    if title == none { content } else if breakable {
      grid(columns: 1fr, row-gutter: gap(0.2), grid.header(label), content)
    } else {
      block(below: gap(0.2), sticky: true, label)
      content
    }
  },
)

// The reading box: the one tinted panel. It holds one list, or several lists that
// each follow a bold label (*Look for*, *Symptoms*), and never breaks: the reader
// takes it in as one thing. Each list is set item by item, for its spacing.
#let readbox(body, title: [When to use it — reading the wall], icon: "reading") = panel(title: title, icon: icon, fill: shade, tight: true, breakable: false, ragged({
  set list(marker: text(weight: 700)[›], indent: 0.1em, body-indent: 0.55em)
  let kids = if body.func() == [].func() { body.children } else { (body,) }
  // Split the body into runs: list items, and the text between them. A blank
  // line ends a run of text but not a list. An index mark between runs takes
  // no room, so it is set first.
  let runs = ()
  let marks = ()
  let in-text = false
  for c in kids {
    if c.func() == list.item {
      if runs.len() > 0 and runs.last().items { runs.last().kids.push(c) } else { runs.push((items: true, kids: (c,))) }
      in-text = false
    } else if c.func() == parbreak {
      in-text = false
    } else if in-text {
      runs.last().kids.push(c)
    } else if c.func() == metadata {
      marks.push(c)
    } else if c.func() not in ([ ].func(), linebreak) {
      runs.push((items: false, kids: (c,)))
      in-text = true
    }
  }
  if runs.filter(r => r.items).len() == 0 { body } else {
    marks.join()
    for (i, run) in runs.enumerate() {
      if run.items {
        for (j, item) in run.kids.enumerate() {
          block(above: if j == 0 { gap(0.2) } else { gap(0.4) }, below: gap(0.4), breakable: false, list(item))
        }
      } else {
        block(above: if i == 0 { gap(0.2) } else { gap(0.8) }, below: gap(0.2), run.kids.join())
      }
    }
  }
}))

// A note box. One that follows a technique entry is kept whole (on a
// page of its own if need be), like the entry; in running text a short
// one (under a third of a page) is kept whole and a long one may break.
// A note on the subject of an aside takes its icon: `icon: "tall"` or
// `icon: "small"`.
#let notebox(title, body, icon: none) = context {
  let h = measure(block(width: 210mm - 2 * margin-x, probe(panel(title: title, body)))).height
  let whole = entries-running.get() or h < (297mm - margin-top - margin-bottom) / 3
  panel(title: title, icon: icon, breakable: not whole, body)
}

// A quick-reminder box: "Five things to keep in mind at V3".
#let remember(title, body) = panel(title: title, breakable: false, tight: true, ragged({
  set enum(body-indent: 0.6em)
  body
}))

// A key point: the same panel, the text in italic one half step up.
#let keypoint(body) = panel(breakable: false, ragged({
  set par(first-line-indent: 0pt)
  text(size: fs.lead, style: "italic", body)
}))

// A line that opens the list after it: flush left, never apart from the list and
// close above it, as a label is. (The space above a list is the larger of its own and
// the line's, so the difference is taken back here.) `lead-label` is the bold form.
#let lead-line(body) = {
  block(width: 100%, above: gap(0.5), below: 0pt, sticky: true, par(first-line-indent: 0pt, body))
  v(gap(0.2) - gap(0.5))
}
#let lead-label(body) = lead-line(strong(body))

// A run-in head that opens a stretch of a section: flush left, with half a line above.
// (It stays a paragraph, so the paragraph after it keeps its indent.)
#let run-in(body) = {
  v(gap(0.5))
  par(first-line-indent: 0pt, body)
}

// A short lead-in that stays with the table or figure after it.
#let lead-in(body) = block(width: 100%, sticky: true, body)

// The last stretch of a text, kept on one page so that its end isn't left alone on
// the next. It replaces a page break: if it fits where it falls, nothing moves.
#let keep-together(body) = block(breakable: false, above: gap(1.5), body)

// Ragged, like the reading box above them: these are one or two lines each, and
// justifying them buys nothing.
#let mistakes(body, glue: false) = {
  labelled([Common mistakes], icon: "mistakes")
  show: ragged
  set par(first-line-indent: 0pt)
  set list(marker: text(weight: 700)[×], body-indent: 0.55em)
  // Item by item. Up to four items move as one with their label; a longer list keeps two
  // together at each end, so no item is ever carried over alone. With `glue` the last ones
  // also go with what follows.
  let kids = if body.func() == [].func() { body.children } else { (body,) }
  let items = kids.filter(c => c.func() == list.item)
  kids.filter(c => c.func() == metadata).join()
  let n = items.len()
  for (j, item) in items.enumerate() {
    let keep = n <= 4 or j == 0 or j >= n - 2
    block(above: if j == 0 { gap(0.2) } else { gap(0.4) }, below: gap(0.4),
      breakable: false, sticky: keep and (glue or j < n - 1), list(item))
  }
}

// ------------------------------------------------------------ figures

// A panel's mark stays with the word after it.
#let tie-marks(body) = {
  show regex("\([a-z0-9]\) "): it => it.text.replace(" ", "\u{a0}")
  body
}
// Every drawing is numbered, on the one sequence that Typst's figures count, so any of
// them can be cited: "Figure 37". The drawings of entries and film strips aren't Typst
// figures, so they step the counter themselves. Their number leads the caption in small
// caps, as a figure's does, or stands alone under a drawing with no caption.
#let drawings = counter(figure.where(kind: image))
#let numbered-caption(body) = {
  drawings.step()
  let number = sc(tracking: 0.05em)[Figure #context drawings.display()]
  text(size: fs.caption, tie-marks(ragged(par(leading: 0.72em,
    if body == none { number } else [#number#h(0.5em)#emph(body)]))))
}

// A figure in the running text stays where the text puts it, whole, with a line
// of space around it.
#let figure-block(body, clearance: gap(1)) = block(above: clearance, below: clearance, breakable: false, body)

// A full-width drawn sequence of one movement, set apart as a feature:
// #filmstrip("filmstrip-dyno.svg", [The dyno], [One sentence on what to watch for.])
// Between technique entries it opens the page of the entry that follows.
#let filmstrip(file, title, caption) = {
  let strip = block(width: 100%, breakable: false, {
    block(below: gap(0.5), [#section-label[In motion]#h(0.7em)#text(size: fs.sub, style: "italic", title)])
    wide-image("figures/" + file)
    v(caption-gap)
    // (the inner block shrinks to its text, which centres as a whole under the strip)
    align(center, block(above: 0pt, width: 88%, align(center, block(align(left, numbered-caption(caption))))))
  })
  context if entries-running.get() {
    pagebreak(weak: true)
    [#metadata("strip")<strip-page>]
    block(below: gap(2), strip)
    entry-top.update(true)
  } else {
    figure-block(clearance: gap(1.5), strip)
  }
}

// A figure from book/figures. `width` scales it; by default it keeps the
// size it was drawn at, which keeps line weights equal across figures.
// `caption-width` lets a short last line of a caption come up: the caption then centres
// under the figure instead of starting at its edge.
#let fig-caption-width = state("fig-caption-width", none)
#let fig(file, caption: none, width: auto, lbl: none, caption-width: none) = {
  let img = if width == auto { image("figures/" + file) } else { image("figures/" + file, width: width) }
  fig-caption-width.update(caption-width)
  [#figure(img, caption: caption, kind: image, supplement: [Figure]) #if lbl != none { label(lbl) }]
  fig-caption-width.update(none)
}

// ------------------------------------------------------------ technique entry

// The spaces inside an entry.
#let entry-spaces(body) = {
  set par(first-line-indent: 0pt, spacing: gap(0.5))
  body
}

// A paragraph that opens a list of steps stays with its first steps, or the steps would
// open the next page with no label, restarted from 1.
#let keep-leads(how) = {
  if how == none or how.func() != [].func() { return how }
  let blank(c) = c.func() in ([ ].func(), parbreak)
  let out = ()
  let run = ()
  for c in how.children {
    if c.func() == enum.item {
      if run.any(x => not blank(x)) {
        out.push(block(width: 100%, below: gap(0.5), sticky: true, run.join()))
      } else { out += run }
      run = ()
      out.push(c)
    } else if c.func() == parbreak {
      out += run
      out.push(c)
      run = ()
    } else { run.push(c) }
  }
  (out + run).join()
}

// A label and the numbered steps or short paragraph under it.
#let labelled-steps(title, how) = {
  labelled(title)
  list-after-label(keep-leads(how))
}

// An entry's figures, its main figure and those of its parts, follow one rule:
// a figure up to 92 mm wide sits beside its steps, and a wider one or one marked
// wide goes below them. (These take a context, to measure the image.)
#let fig-width(file) = measure(image(file)).width
#let sits-beside(file, wide) = not (wide or fig-width(file) > 92mm)
#let side-figure-block(file, caption) = block(breakable: false, {
  image(file)
  v(caption-gap)
  block(above: 0pt, width: calc.max(fig-width(file) - overhang, 48mm), numbered-caption(caption))
})
// A narrow figure beside the steps, hanging into the right margin when it is wide.
// The steps are ragged here, since a narrow justified column opens rivers. The column
// ends after the step that makes the whole lowest, and the other steps go on at full
// measure under the figure, with their numbers. (The grid sits in a block, since a
// cell ignores the space above its first block.)
#let beside-steps(title, how, file, caption, hang: auto, lead: none) = context {
  let w = fig-width(file)
  let hang = if hang != auto { hang } else if w > 60mm { overhang } else { 0pt }
  let col = 210mm - 2 * margin-x + hang - w - 16pt
  let how = if how == none { [] } else { how }
  let fig-h = measure(probe(side-figure-block(file, caption))).height
  let kids = if how.func() == [].func() { how.children } else { (how,) }
  // the places where the column could end: after each item
  let ends = kids.enumerate().filter(((i, c)) => c.func() == enum.item).map(((i, c)) => i + 1)
  let steps(slice) = list-after-label(slice)
  let label-h = measure(block(width: col, probe({ lead; labelled(title) }))).height + gap(0.2)
  let height-to(e) = label-h + measure(block(width: col, probe(ragged(steps(kids.slice(0, e).join()))))).height
  let rest-h(e) = if e >= kids.len() or kids.slice(e).filter(c => c.func() not in ([ ].func(), parbreak)).len() == 0 { 0pt } else { gap(0.4) + measure(block(width: 210mm - 2 * margin-x, probe({ steps(kids.slice(e).join()) }))).height }
  // the end of the column that makes the whole lowest, the later one on a tie
  let cut = kids.len()
  let best = calc.max(fig-h, height-to(cut))
  for e in ends.rev() {
    let t = calc.max(fig-h, height-to(e)) + rest-h(e)
    if t < best - 1pt { best = t; cut = e }
  }
  let rest = kids.slice(cut)
  block(above: gap(1), below: 0pt,
    pad(right: -hang, grid(columns: (1fr, auto), column-gutter: 16pt,
      ragged({ lead; labelled(title); steps(kids.slice(0, cut).join()) }),
      side-figure-block(file, caption),
    )))
  if rest.filter(c => c.func() not in ([ ].func(), parbreak)).len() > 0 {
    // the list that was cut goes on with its numbers; a later list starts again
    let is-filler(c) = c.func() in ([ ].func(), parbreak)
    let run-start = kids.slice(0, cut).enumerate().filter(((i, c)) => c.func() != enum.item and not is-filler(c)).map(((i, c)) => i + 1).last(default: 0)
    let done = kids.slice(run-start, cut).filter(c => c.func() == enum.item).len()
    let run-end = rest.enumerate().filter(((i, c)) => c.func() != enum.item and not is-filler(c)).map(((i, c)) => i).first(default: rest.len())
    block(above: gap(0.4), below: 0pt, width: 100%, {
      {
        set enum(start: done + 1)
        show enum: set block(above: 0pt)
        steps(rest.slice(0, run-end).join())
      }
      if run-end < rest.len() { steps(rest.slice(run-end).join()) }
    })
  }
}
#let wide-figure-block(file, caption) = block(width: 100%, breakable: false, {
  wide-image(file)
  v(caption-gap)
  align(center, block(above: 0pt, width: calc.min(calc.max(fig-width(file), 60mm), 125mm), align(left, numbered-caption(caption))))
})

// ------------------------------------------------------------ worked readings

// The problems at the end of Chapter 2: a question page, then an answer page. A
// question starts on an odd page, so in a two-page view its answer is on the back
// of the leaf. website/template.typ has its own versions of these two macros.
#let reading-head(n, title) = block(above: 0pt, below: gap(0.5), breakable: false, sticky: true,
  text(size: fs.sub)[#section-label[Problem #n]#h(0.6em)#text(weight: 700, title)])

// A hold's mark stays with the word before it, since "2." at the start of a line reads
// as a list number and "B." as a stray letter.
#let tie-holds(body) = {
  show regex("[\p{L}\p{N}]+,? [A-Z0-9]\b"): it => it.text.replace(" ", "\u{a0}")
  body
}

// Every figure here is under 92 mm wide, so it always sits beside its text.
#let reading-layout(label, steps, file, caption, lead: none) = beside-steps(label, steps, "figures/" + file, caption, hang: overhang, lead: lead)

#let reading-question(n: none, title: none, grade: none, wall: none, start: none, finish: none, figure: none, prompts: none) = {
  pagebreak(weak: true, to: "odd")
  [#metadata((n: n, side: "question"))<reading-page>]
  show: tie-holds
  reading-head(n, title)
  [About #grade-tab-inline(grade-label(grade), g: grade). #wall Start: #start Finish: #finish]
  reading-layout([Read it yourself], prompts, figure, none)
  v(1fr)
  align(right, text(size: fs.caption, emph[Make your plan, then turn the page.]))
}

// A full line parts the notes from the figure above them, as under a figure in an
// entry. The notes belong together, so half a line parts them from each other.
#let reading-answer(n: none, figure: none, caption: none, moves: none, crux: none, wrong: none, next: none, tall: none, small: none, entries: ()) = {
  pagebreak(weak: true)
  [#metadata((n: n, side: "answer"))<reading-page>]
  show: tie-holds
  reading-layout([The moves], moves, figure, caption, lead: reading-head(n, [The answer]))
  block(width: 100%, above: gap(1), below: 0pt, [#text(weight: 700)[Crux.] #crux])
  for (head, body) in (([Why the obvious try fails.], wrong), ([What to try next.], next)) {
    if body != none { block(width: 100%, above: gap(0.5), below: 0pt, [#text(weight: 700, head) #body]) }
  }
  if tall != none { block(width: 100%, above: gap(0.5), below: 0pt, [#aside-icon("tall")#text(weight: 700, style: "italic")[Tall climbers.] #tall]) }
  if small != none { block(width: 100%, above: gap(0.5), below: 0pt, [#aside-icon("small")#text(weight: 700, style: "italic")[Small climbers.] #small]) }
  if entries.len() > 0 {
    block(above: gap(0.5), below: 0pt, ragged({
      set text(size: fs.note)
      set par(leading: 0.68em, hanging-indent: 1em)
      par[#sc[Entries]#h(0.45em)#entries.map(k => tref(k)).join(", ")]
    }))
  }
}

// A part of an entry, for a move the entry absorbed or gathers: a dictionary
// with `name` and `how` (numbered steps or a short paragraph), and optionally
// `figure`, `caption` and `figure-wide`, which work as they do for the entry.
// With `live` false it carries no index mark, for measuring.
#let part-content(p, live) = {
  let title = [#if live { ix(plain(p.name), main: true) }#p.name]
  let figure = p.at("figure", default: none)
  let caption = p.at("caption", default: none)
  if figure == none {
    labelled-steps(title, p.how)
  } else if sits-beside("figures/" + figure, p.at("figure-wide", default: false)) {
    beside-steps(title, p.how, "figures/" + figure, caption)
  } else {
    labelled-steps(title, p.how)
    block(above: gap(1), wide-figure-block("figures/" + figure, caption))
  }
}
// A part with no figure stays whole when it is short (under a third of a page, as
// for a note box), and otherwise breaks like the main steps. A part with a figure
// may break between its steps and its figure, rather than leave a page half empty.
#let part-whole(p) = p.at("figure", default: none) == none and measure(block(width: 210mm - 2 * margin-x, probe(entry-spaces(part-content(p, false))))).height <= page-height / 3
#let entry-part(p) = block(width: 100%, breakable: not part-whole(p), above: gap(1), below: gap(1), part-content(p, true))

// An apparatus at least this tall (about nine lines) can stand alone on a page.
#let apparatus-alone = 120pt

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
  // what the entry absorbed or gathers, set after its steps and figure: an
  // array of dictionaries (see `part-content`)
  parts: (),
  when: none,
  errors: none,
  tall: none,
  small: none,
  related: (),
  watch: (),
  sources: (),
  // a box that belongs to the entry (of drills, say), set last, so the apparatus still
  // closes the entry
  closing-box: none,
  // paragraphs on variants of the move, set straight after a wide figure rather than
  // between the steps and the figure, for when they would part the two
  after-figure: none,
) = {
  // `aliases: ("one name")` is a string, not an array: accept both
  let aliases = if type(aliases) == str { (aliases,) } else { aliases }
  // and `parts: (name: ..., how: ...)` is one part, not an array
  let parts = if type(parts) == dictionary { (parts,) } else { parts }
  let meta = (key: key, name: name, aliases: aliases, category: category, grade: grade)
  // The head of the entry.
  let head = {
    // title band: the name and the grade, the other names and the
    // category, then a heavy rule (sticky: never left alone at the foot
    // of a page)
    block(width: 100%, below: gap(1), breakable: false, sticky: true, {
      grid(columns: (1fr, auto), column-gutter: 1em, align: (left + bottom, right + bottom),
        [#heading(level: 3, name)#label("tech-" + key)#metadata(meta)#label("tech-meta-" + key)#ix(name, main: true)],
        navlink(label("grade-" + str(calc.min(calc.max(grade, 0), 8))), grade-tab(grade-label(grade) + "+", size: fs.badge, g: grade)),
      )
      if aliases.len() > 0 or category != none {
        set par(justify: false)
        // other names and category on one line, or the category on a line of its own
        // with no separator left hanging
        let others = if aliases.len() > 0 [_Also called_ #aliases.join(", ")]
        let cat = if category != none { box(navlink(label("cattable-" + category), sc(categories.at(category), tracking: 0.05em))) }
        let sep = [#h(0.4em)·#h(0.4em)]
        block(above: 0.85em, text(size: fs.caption, context {
          if others == none or cat == none { others; cat }
          else if measure([#others#sep#cat]).width <= 210mm - 2 * margin-x { others; sep; cat }
          else { others; linebreak(); cat }
        }))
      }
      block(above: 0.8em, line(length: 100%, stroke: rule-heavy))
    })
    // (an alias that names a part is indexed at the part, under that name alone)
    let part-names = parts.map(p => lower(plain(p.name)))
    for a in aliases.filter(a => lower(a) not in part-names) { ix(a + " (see " + name + ")") }
    // (ragged, like the grade note under it: at this size a line stretched to justify shows)
    if summary != none { block(width: 100%, above: 0pt, below: gap(0.6), sticky: true, ragged(text(size: fs.lead, par(summary)))) }
    if grade-note != none {
      block(width: 100%, above: gap(0.6), below: 0pt, ragged(text(size: fs.note)[#sc(tracking: 0.08em)[Grade]#h(0.6em)#grade-note]))
    }
  }
  // The figure of the entry. `side-figure` is true when it sits beside the
  // steps (it takes a context, to measure the image).
  let file = if figure != none { "figures/" + figure } else { none }
  let side-figure() = file != none and sits-beside(file, figure-wide)
  // The entry: the head and the steps, with the figure if it sits beside them.
  // (An entry made up of parts may have no steps of its own.)
  // (It takes a context, for the figure's width and the backlinks.)
  let entry() = {
    show: entry-spaces
    head
    if side-figure() { beside-steps([How to do it], how, file, caption) }
    else if how != none { labelled-steps([How to do it], how) }
    // after the steps: the parts, the reading box, mistakes, the notes for tall
    // and small climbers and the entry's apparatus
    let rest = {
      // the entry's apparatus: related entries, videos, sources, backlinks
      let foot = ()
      if related.len() > 0 {
        foot.push([#sc[Related]#h(0.45em)#related.map(k => tref(k)).join(", ")])
      }
      // a small black tab with the link's number, matching the number under
      // its QR code (and unlike a digit in the video's title)
      let qr-num(n) = grade-tab-inline(str(n), size: 7.2pt)
      if watch.len() > 0 {
        let items = watch.enumerate().map(((i, w)) => {
          let num = if i < 2 { [#qr-num(i + 1)#h(0.3em)] } else { [] }
          [#num#link(w.at(2))[#w.at(1)] (#w.at(0))]
        })
        foot.push([#sc[Watch]#h(0.45em)#items.join("; ")])
      }
      if evidence-on and sources.len() > 0 {
        foot.push([#sc[Evidence]#h(0.45em)#evidence-line(sources)])
      }
      if sources.len() > 0 {
        foot.push([#sc[Sources]#h(0.45em)#src(..sources)])
      }
      let foot-with(back) = foot + if back.len() > 0 { ([#sc[Referenced from]#h(0.45em)#back.join(", ")],) } else { () }
      // up to two QR codes for the videos, numbered like the Watch links
      let qrs = watch.slice(0, calc.min(watch.len(), 2)).enumerate().map(((i, w)) => stack(
        spacing: 3pt,
        link(w.at(2), qrcode(w.at(2), width: 13mm)),
        align(center, qr-num(i + 1)),
      ))
      let references(back) = {
        let lines = ragged({
          set text(size: fs.note)
          set par(leading: 0.68em, spacing: 0.75em, hanging-indent: 1em)
          for f in foot-with(back) { par(f) }
        })
        if qrs.len() == 0 { lines } else {
          grid(columns: (1fr, auto), column-gutter: 14pt, lines,
            stack(spacing: 4pt,
              text(size: fs.index, style: "italic")[Scan to watch],
              stack(dir: ltr, spacing: 7pt, ..qrs)))
        }
      }
      let back = backlink-items(key)
      // A short apparatus alone on a page reads as a stray, so whatever comes last before
      // it stays with it. A long one can stand on its own, and the block before it can
      // then stay on its page instead of leaving a hole there.
      let has-apparatus = foot.len() > 0 or back.len() > 0
      let glue = closing-box != none or (has-apparatus and measure(block(width: 210mm - 2 * margin-x, probe(references(backlink-items(key, measuring: true))))).height < apparatus-alone)
      let last-note = tall == none and small == none
      for p in parts { entry-part(p) }
      if when != none {
        if errors == none and last-note and closing-box == none and glue { block(sticky: true, below: 0pt, readbox(when)) } else { readbox(when) }
      }
      if errors != none { mistakes(errors, glue: last-note and closing-box == none and glue) }
      if tall != none {
        // (the two notes are a pair, and stay together)
        block(width: 100%, above: gap(1), below: 0pt, breakable: false, sticky: small != none or (closing-box == none and glue), [#aside-icon("tall")#text(weight: 700, style: "italic")[Tall climbers.] #tall])
      }
      if small != none {
        block(width: 100%, above: gap(1), below: 0pt, breakable: false, sticky: closing-box == none and glue, [#aside-icon("small")#text(weight: 700, style: "italic")[Small climbers.] #small])
      }
      if closing-box != none { block(sticky: true, below: 0pt, closing-box) }
      if has-apparatus {
        // A box straight above closes the entry with its own rule, since two rules with
        // nothing between them read like an empty table row. At the top of a page the
        // running head's rule is enough.
        let after-box = closing-box != none or (when != none and errors == none and last-note)
        block(above: if after-box { gap(1) } else { gap(1.5) }, width: 100%, breakable: false, {
          context if not after-box and here().position().y > margin-top + 1pt {
            block(below: gap(0.5), sticky: true, line(length: 100%, stroke: rule-light))
          }
          references(back)
        })
      }
    }
    // a wide figure stays in flow after the steps, so the order never changes:
    // steps, figure, parts, box, mistakes, notes, apparatus
    if file != none and not side-figure() { block(above: gap(1), below: 0pt, wide-figure-block(file, caption)) }
    if after-figure != none { block(width: 100%, above: gap(1), below: 0pt, breakable: false, after-figure) }
    rest
  }
  // Every entry starts a page, unless it follows the head of its grade section on
  // that page. The updates come after the page break: Typst moves the start of this
  // context past the break, so a state update before it would count as coming before
  // the context, and `entry-top.get()` would read its value.
  context if not entry-top.get() { pagebreak(weak: true) }
  context {
    entry-top.update(false)
    entries-running.update(true)
    block(breakable: true, above: 0pt, below: 0pt, width: 100%, entry())
  }
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
// Its rows run to several lines, so they are parted by more space than the short rows
// of the generated tables.
#let data-table(columns: auto, ..args) = table(
  columns: columns, stroke: head-rule, inset: (x: cell-inset.x, y: 7pt), align: left + top, ..args,
)

// Table of the techniques in one category, ranked by grade, in two columns.
// Within a grade the entries keep the order of the chapter (`sorted` is
// stable), which follows what depends on what.
#let category-table(cat) = [#metadata(cat)#label("cattable-" + cat)] + context {
  let ms = tech-metas().filter(m => m.value.category == cat)
  let rows = ms.sorted(key: m => m.value.grade)
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

// Techniques that become important at one grade (for the grade guides),
// grouped by category, in the chapter's order within each category.
#let grade-techniques(g) = context {
  let ms = tech-metas().filter(m => if g >= 8 { m.value.grade >= 8 } else { m.value.grade == g })
  if ms.len() > 0 {
    let rows = ms.sorted(key: m => m.value.category)
    table(
      columns: (1fr, 10em, 2.2em),
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
  let items = ()
  let sizes = ()
  let letter-of(i) = if i >= 0 and i < rows.len() { upper(ix-fold(rows.at(i).sort).first()) }
  // the page's number stays on the line of its leader, and the leader with the last
  // word before it; a target name never breaks
  let tie = [#sym.wj#h(0.3em)#sym.wj]
  for (i, r) in rows.enumerate() {
    let letter = letter-of(i)
    let sp = if i > 0 and letter != letter-of(i - 1) { v(gap(0.5), weak: true) }
    // like the index, two rows stay together at each end of a letter's group
    let keep = (letter == letter-of(i + 1) and (letter != letter-of(i - 1) or letter != letter-of(i + 2)))
    let row(body) = block(breakable: false, sticky: keep, par(body))
    let loc = r.m.location()
    let pg = str(counter(page).at(loc).first())
    if r.see == none {
      items.push([#sp#row[#link(loc, strong(r.name))#tie#dots#tie#box(width: 2.1em, badge-plain(r.m.value.grade))#box(width: 2em, align(right, link(loc, pg)))]])
      sizes.push([#sp#row[#strong(r.name)#tie#dots#tie#box(width: 2.1em, badge-plain(r.m.value.grade))#box(width: 2em, align(right, pg))]])
    } else {
      items.push([#sp#row[#link(loc)[#r.name #arrow #box(emph(r.see))]#tie#dots#tie#box(width: 2em, align(right, link(loc, pg)))]])
      sizes.push([#sp#row[#r.name #arrow #box(emph(r.see))#tie#dots#tie#box(width: 2em, align(right, pg))]])
    }
  }
  balanced-columns("az", 2, items, gutter: 2em, sizes: sizes, margin: 0pt)
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
      block(width: 90%, text(size: fs.part-sub, style: "italic", hyphenate: false, par(justify: false, leading: 0.5em, subtitle)))
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

// links: false leaves the links to the reference sections out of the running
// head, for the exercises booklet, which has none of them.
#let book(title: none, subtitle: none, author: none, links: true, body) = {
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
        // (its own spacing, or a page begun inside the A–Z would pass on the A–Z's)
        set par(justify: false, first-line-indent: 0pt, spacing: lead)
        let dot = h(0.8em) + sym.dot.c + h(0.8em)
        let nav = if links { sc(tracking: 0.05em)[#navlink(<contents>)[Contents]#dot#navlink(<a-to-z>)[A–Z]#dot#navlink(<troubleshooting>)[Troubleshooting]#dot#navlink(<glossary>)[Glossary]#dot#navlink(<index>)[Index]] }
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
  set text(font: serif, size: fs.body, lang: "en", region: "gb", number-type: "old-style", top-edge: cap, costs: (hyphenation: 40%))
  // Grades and Font grades take lining figures: V3, 6A+.
  show regex("\bV\d+|\b\d[ABC]\b|\bA[1-5]\b|Font[ \u{a0}]\d\+?(?:[–\u{2060}]+\d\+?)?"): set text(number-type: "lining")
  // A range stays whole, and with its unit: the box hides the range's last digit
  // from the measurement rule below, so "10–25 minutes" is tied here.
  show regex("[\p{L}\p{N}+]+–[\p{L}\p{N}+]+(?: (?:mm|cm|m|km|kg|N|min|minutes?|seconds?)\b)?"): it => {
    let (span, ..unit) = it.text.split(" ")
    if unit.len() == 0 { box(it) } else { box(span) + "\u{a0}" + unit.join(" ") }
  }
  // A spaced dash ends a line and never starts one.
  show regex(" [-–] "): "\u{a0}– "
  // "Chapter 2" and "Font 6A" stay together, and "Chapter" doesn't hyphenate.
  show regex("\b(Chapters?|Font) \d"): it => text(hyphenate: false, it.text.replace(" ", "\u{a0}"))
  show regex("\d (mm|cm|m|km|kg|N|min|minutes?|seconds?)\b"): it => it.text.replace(" ", "\u{a0}")
  show regex("(?i)\b(e-reader|side-on|pull-up|take-off|big-toe|little-toe|one-handed|two-finger|top-outs?|fact-check)\b"): box
  show regex("\b(Section|Figure)\b"): box
  // Running text: paragraphs are marked by an indent, not by space; space
  // is kept for the boundaries between blocks.
  set par(justify: true, leading: lead, spacing: lead, first-line-indent: 1.5em, justification-limits: (spacing: (min: 82%, max: 130%), tracking: (min: -0.01em, max: 0.015em)))
  // Lists: items half a line apart, the list half a line from the text.
  set list(indent: 0.25em, body-indent: 0.5em, spacing: gap(0.4), marker: text(size: 0.9em, [•]))
  set enum(indent: 0.1em, body-indent: 0.5em, spacing: gap(0.4), numbering: step-number)
  show list: set block(above: gap(0.5), below: gap(0.5))
  show enum: set block(above: gap(0.5), below: gap(0.5))
  // Lists are ragged, in every setting: items are short, a justified one opens loose
  // lines when its last words have to stay together, and steps beside a figure are ragged
  // anyway. Running paragraphs stay justified.
  show list: set par(first-line-indent: 0pt, justify: false, linebreaks: "optimized")
  show enum: set par(first-line-indent: 0pt, justify: false, linebreaks: "optimized")
  show list: set text(costs: (runt: 2000%))
  show enum: set text(costs: (runt: 2000%))
  show list: keep-compounds
  show enum: keep-compounds
  show link: it => it
  show list: keep-list.with(list)
  show enum: keep-list.with(enum)
  // The last line of a lead-in ending in ":" carries a strut hanging below it, so that
  // it needs the room for the first items of its list (six lines); the same space is
  // then taken back. (It stays a paragraph, not a block, so it keeps its first-line
  // indent.) Six lines cover the book's lists today, and tools/check_fit.py fails the
  // build if a lead-in ever ends a page.
  show par: it => {
    let done = it.body.func() == [].func() and it.body.children.len() > 0 and it.body.children.last().func() == box
    if not done and plain(it.body).trim().ends-with(":") {
      let strut = gap(0.5) + 6 * pitch
      par(it.body + box(width: 0pt, height: strut, baseline: strut))
      v(-strut)
    } else { it }
  }
  // Reference matter set in columns (glossary, A–Z, sources, index) uses
  // the outer frame.
  show columns: it => block(above: gap(1.5), pad(x: -overhang, it))
  show cite: set text(size: 0.9em)
  // A source never breaks across columns, and its URL breaks only after a separator
  // or an escaped character such as %20, never leaving a few characters alone on a line.
  show bibliography: set grid.cell(breakable: false)
  show bibliography: it => {
    show link: l => {
      // (a link already set in pieces is left alone)
      let set-already = l.body.func() == box or (l.body.func() == [].func() and l.body.children.any(c => c.func() == box))
      let t = plain(l.body)
      if set-already or t.len() == 0 { return l }
      let pieces = t.matches(regex("[^/.\\-_?=&%]*(?:[/.\\-_?=&]+|%[0-9A-Fa-f]{2})?")).map(m => m.text).filter(x => x != "")
      if pieces.len() > 1 and pieces.last().len() < 7 {
        let tail = pieces.pop()
        pieces.push(pieces.pop() + tail)
      }
      link(l.dest, text(number-type: "lining", pieces.map(box).join()))
    }
    // The citation style leaves a comma where an entry has no page numbers, and after a
    // title that ends in its own punctuation.
    show regex(", \(\d{4}[a-z]?\)"): it => it.text.slice(1)
    show regex("[?!]\)?, "): it => it.text.replace(",", "")
    it
  }
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
  // its own text. A section named after a grade (Part II) starts a page.
  // A grade guide (Part III) is a major division: it starts a page, sunk
  // by a line, and its head is one step larger.
  show heading.where(level: 2): it => {
    let lbl = it.at("label", default: none)
    let lbl = if lbl == none { "" } else { str(lbl) }
    let g = grade-head(it)
    // (the progression map closes the run of guides, so it looks like them)
    let guide = lbl.starts-with("grade") or lbl == "progression-map"
    let size = if guide { fs.guide } else { fs.section }
    let head = context {
      set text(size: size)
      let num = if it.numbering != none [#text(number-type: "old-style", numbering(it.numbering, ..counter(heading).at(it.location())))#h(0.45em)]
      par(leading: 0.42em, hanging-indent: if num != none { measure(text(size: size, num)).width } else { 0pt }, [#num#it.body])
    }
    if guide or (g != none and g.title != none) {
      pagebreak(weak: true)
      if guide { entries-running.update(false); v(pitch) } else { entry-top.update(true) }
      block(width: 100%, above: 0pt, below: if guide { gap(2) } else { gap(2.5) }, sticky: true, head)
    } else {
      // room for the head and five lines under it, or the next page
      block(width: 100%, above: gap(2.5), below: 0pt, breakable: false, height: 5 * pitch + 2 * fs.section, sticky: true)
      v(-(5 * pitch + 2 * fs.section))
      block(width: 100%, above: 0pt, below: gap(0.9), sticky: true, head)
    }
  }
  show heading.where(level: 3): it => text(size: fs.tech, weight: 700, it.body)
  show heading.where(level: 4): it => block(above: gap(1.5), below: gap(0.5), sticky: true, text(size: fs.sub, weight: 700, it.body))
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
    show: ragged
    set par(first-line-indent: 0pt, leading: 0.72em)
    text(size: fs.caption)[#sc(tracking: 0.05em)[#it.supplement #context it.counter.display(it.numbering)]#h(0.5em)#tie-marks(emph(it.body))]
  }
  // Narrow figures take their caption beside them.
  show figure: it => figure-block(block(width: 100%, breakable: false, context {
    let w = measure(it.body).width
    if w < 80mm {
      align(center, grid(columns: (w, 62mm), column-gutter: 7mm, align: bottom, it.body, align(left, it.caption)))
    } else {
      pad(x: -overhang, align(center, it.body))
      v(caption-gap)
      // Under a figure wider than the block's limit the caption shrinks to its text, so
      // that it centres as a whole; under a narrower figure it starts at the drawing's edge.
      let asked = fig-caption-width.get()
      let shrink(c) = if w > 130mm or asked != none { align(center, block(align(left, c))) } else { align(left, c) }
      align(center, block(above: 0pt, width: if asked != none { asked } else { calc.min(calc.max(w, 70mm), 130mm) }, shrink(it.caption)))
    }
  }))
  // Tables: a heavy rule above, a light rule under the head and another
  // below; small caps heads; lining figures.
  set table(stroke: head-rule, inset: cell-inset)
  show table.cell.where(y: 0): it => {
    show strong: s => sc(s.body, tracking: 0.05em)
    it
  }
  set table.cell(breakable: false)
  show table: it => {
    set text(size: fs.caption, number-type: "lining")
    show: ragged
    set par(first-line-indent: 0pt, leading: 0.6em)
    let is-head(c) = type(c) == content and c.func() == table.header
    let is-foot(c) = type(c) == content and c.func() == table.footer
    let n = if type(it.columns) == array { it.columns.len() } else if type(it.columns) == int { it.columns } else { 1 }
    let heads = it.children.filter(is-head)
    let foots = it.children.filter(is-foot)
    let cells = it.children.filter(c => not is-head(c) and not is-foot(c))
    let spans = cells.any(c => c.func() == table.cell and (c.at("colspan", default: 1) > 1 or c.at("rowspan", default: 1) > 1))
    let countable = not spans and calc.rem(cells.len(), n) == 0
    let rows = cells.len() / n
    // A table that may break keeps two rows together at each end: its first row is a
    // sub-head that doesn't repeat, which a page break can't leave alone, and its last
    // two are a footer that doesn't repeat, which a page break can't part.
    if countable and foots.len() == 0 and rows > 6 {
      let fields = it.fields()
      let _ = fields.remove("children")
      let m = cells.len() - 2 * n
      return table(..fields, ..heads, table.header(level: 2, repeat: false, ..cells.slice(0, n)),
        ..cells.slice(n, m), table.footer(repeat: false, ..cells.slice(m)))
    }
    // a short table stays whole
    block(above: gap(1), below: gap(1), breakable: foots.len() > 0 or not (countable and rows <= 6),
      inset: (top: 2pt, bottom: 3pt), stroke: (top: rule-heavy, bottom: rule-light), it)
  }
  // The contents: parts in small caps, chapters in bold, sections indented,
  // dotted leaders to lining page numbers.
  show outline.entry: it => {
    let el = it.element
    let pg = text(number-type: "lining", it.page())
    let dots = box(width: 1fr, repeat(gap: 0.3em, text(size: 0.8em, ".")))
    if it.level == 1 and el.at("label", default: none) == <part> {
      let t = plain(el.body).split(" — ")
      // Part III and its one long chapter start a page rather than break across two
      if t.first() == "Part III" { pagebreak(weak: true) }
      block(above: gap(1.25), below: gap(0.4), sticky: true, link(el.location(), {
        sc(tracking: 0.08em, t.first())
        if t.len() > 1 { h(0.6em); emph(t.slice(1).join(" — ")) }
      }))
    } else if it.level == 1 {
      block(above: gap(0.4), below: 0.6em, sticky: true, link(el.location(), {
        let pre = it.prefix()
        strong[#box(width: 1.6em, if pre != none { text(number-type: "lining", pre) })#it.body()]
        h(0.4em); dots; h(0.4em); pg
      }))
    } else {
      block(above: 0.6em, below: 0.6em, pad(left: 1.6em, link(el.location(), {
        let pre = it.prefix()
        box(width: 2.6em, if pre != none { text(number-type: "lining", pre) })
        it.body(); h(0.4em); dots; h(0.4em); pg
      })))
    }
  }
  body
}
