// The images a site needs as bitmaps: the picture shown when a link to it is
// shared, and the icon for phones. build.py compiles this with `--input what=...`.
#let serif = ("Iowan Old Style", "Charter", "Libertinus Serif")
#let what = sys.inputs.at("what", default: "card")
#set text(font: serif, fill: black)
#if what == "icon" {
  set page(width: 512pt, height: 512pt, margin: 0pt, fill: white)
  align(center + horizon, image("figures/ornament-jug.svg", width: 400pt))
} else {
  set page(width: 1200pt, height: 630pt, margin: 50pt, fill: white)
  set par(leading: 0.5em)
  grid(columns: (1fr, 500pt), column-gutter: 40pt, rows: 530pt, align: horizon,
    {
      text(size: 19pt, features: ("c2sc", "smcp"), tracking: 0.08em, sys.inputs.at("strap", default: ""))
      v(30pt)
      text(size: 96pt, sys.inputs.at("title", default: "").split("|").join(linebreak()))
      v(34pt)
      text(size: 28pt, style: "italic", sys.inputs.at("tagline", default: ""))
    },
    align(center, image("figures/cover.svg", width: 500pt, height: 500pt, fit: "contain")),
  )
}
