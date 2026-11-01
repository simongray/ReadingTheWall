"""Write book/errata.json, the corrections the appendix lists, from the
Errata of a section of CHANGELOG.md: the edition's, when release.sh passes
its number (errata.py 2 reads "Second edition (edition-2)"), else the
newest section.

Each item becomes the first edition's page numbers, where in the book, and
the correction, e.g. "p. 77, Bumping: the text says…" gives the pages "77",
the place "Bumping" and the rest. Straight quotes become typographic ones.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = re.compile(r"^pp?\. ((?:\d+(?:–\d+)?)(?:(?:, | and )\d+(?:–\d+)?)*)([,:])\s*")


def smart(text):
    """Text with typographic quotes and apostrophes."""
    text = re.sub(r'(^|[\s(\[—–])"', "\\1“", text)
    text = text.replace('"', "”")
    return re.sub(r"(^|[\s(\[—–])'", "\\1‘", text).replace("'", "’")


def items(lines):
    """The list items in `lines` as (indent, text), continuation lines
    joined to their item and HTML comments left out."""
    out = []
    for line in lines:
        if not line.strip() or line.lstrip().startswith("<!--"):
            continue
        m = re.match(r"^( *)- (.*)$", line)
        if m:
            out.append([len(m.group(1)), m.group(2)])
        elif out:
            out[-1][1] += " " + line.strip()
    return out


def entry(text):
    """An item's first-edition pages, its place in the book and the
    correction, each starting with a capital."""
    pages, place = "", ""
    m = PAGES.match(text)
    if m:
        pages, text = m.group(1), text[m.end():]
        if m.group(2) == ",":
            place, _, text = text.partition(": ")
    return dict(pages=pages, place=smart(place[:1].upper() + place[1:]),
                text=smart(text[:1].upper() + text[1:]), subs=[])


def main():
    lines = open(os.path.join(ROOT, "CHANGELOG.md")).read().splitlines()
    heads = [i for i, line in enumerate(lines) if line.startswith("## ")]
    k = 0
    if len(sys.argv) > 1:
        k = next(j for j, i in enumerate(heads) if f"(edition-{sys.argv[1]})" in lines[i])
    start, end = heads[k], heads[k + 1] if k + 1 < len(heads) else len(lines)
    previous = re.sub(r"\s*\(.*\)$", "", lines[end][3:]) if end < len(lines) else ""
    section = lines[start:end]
    errata, on = [], False
    for line in section:
        if line.startswith("### "):
            on = line.strip() == "### Errata"
        elif on:
            errata.append(line)
    out = []
    for indent, text in items(errata):
        if indent == 0:
            out.append(entry(text))
        elif out:
            out[-1]["subs"].append(smart(text))
    path = os.path.join(ROOT, "book", "errata.json")
    with open(path, "w") as f:
        json.dump(dict(previous=previous, items=out), f, ensure_ascii=False, indent=1)
    print(f"{len(out)} corrections to the {previous.lower() or 'previous edition'} -> {path}")


if __name__ == "__main__":
    main()
