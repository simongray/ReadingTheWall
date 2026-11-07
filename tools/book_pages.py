"""Write book/book-pages.json: the pages of the book's entries, sections and
figures, for the exercises booklet's references into the book.

Run it after a change to the book and before compiling book/exercises.typ:
    python3 tools/book_pages.py [typst inputs]
build.sh and release.sh run it with the inputs they compile the book with.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "book", "book-pages.json")

EXPR = """let plain(c) = if type(c) == str { c } else if c.has("text") { c.text } else if c.has("children") { c.children.map(plain).join() } else if c.has("body") { plain(c.body) } else if c == [ ] { " " } else { "" }
let folio(e) = counter(page).at(e.location()).first()
(
  tech: query(metadata).filter(m => str(m.at("label", default: "")).starts-with("tech-meta-"))
    .map(m => (key: str(m.label).slice(10), name: plain(m.value.name), page: folio(m))),
  heads: query(heading).filter(h => h.has("label") and h.numbering != none)
    .map(h => (label: str(h.label), supplement: "Section",
               number: counter(heading).at(h.location()).map(str).join("."), page: folio(h))),
  figs: query(figure.where(kind: image)).filter(f => f.has("label"))
    .map(f => (label: str(f.label), supplement: "Figure",
               number: str(counter(figure.where(kind: image)).at(f.location()).first()), page: folio(f))),
)"""


def main():
    run = subprocess.run(["typst", "eval", EXPR, "--root", ".", *sys.argv[1:], "--in", "book/main.typ"],
                         capture_output=True, text=True, cwd=ROOT)
    if run.returncode != 0:
        sys.exit(run.stderr)
    facts = json.loads(run.stdout)
    pages = {
        "tech": {t["key"]: {"name": t["name"], "page": t["page"]} for t in facts["tech"]},
        "refs": {r["label"]: {k: r[k] for k in ("supplement", "number", "page")}
                 for r in facts["heads"] + facts["figs"]},
    }
    with open(OUT, "w") as f:
        json.dump(pages, f, ensure_ascii=False, indent=1)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(pages['tech'])} entries, {len(pages['refs'])} sections and figures")


if __name__ == "__main__":
    main()
