// Edition metadata. build.sh and release.sh pass these in with
// `typst compile --input edition=1 --input date=2026-10-31 --input commit=abc1234`.
// A plain `typst compile` gives a draft.
#let edition = sys.inputs.at("edition", default: "draft")
#let edition-date = sys.inputs.at("date", default: "")
#let commit = sys.inputs.at("commit", default: "uncommitted")

#let ordinal(n) = {
  let n = int(n)
  let suffix = if calc.rem(n, 100) in (11, 12, 13) { "th" } else {
    ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th").at(calc.rem(n, 10))
  }
  str(n) + suffix
}

// "First edition" style label, or "Draft" for unreleased builds.
#let edition-label = if edition == "draft" { "Draft" } else {
  let words = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth")
  let n = int(edition)
  (if n <= words.len() { words.at(n - 1) } else { ordinal(n) }) + " edition"
}
