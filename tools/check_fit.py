"""Check how the book's text fits its pages, from the built PDF.

This reads the finished pages and looks for the faults listed under "Typography" in
research/REVISE-3.md. A page that ends short at the end of an entry or chapter is
normal, and nothing here asks for fewer pages.

These fail the build:
- arabic page 1 isn't physically odd, so Chapter 1 would open on a left-hand page
- a blank page after arabic 1
- a page with fewer than 3 lines of text
- a range such as V4–V5 broken at a line end
- a line holding only a citation
- a lead-in line ending in ":" or a head as the last thing on a page
- a source cited in the text but missing from Sources, which sits in a block of a set
  height (`sources-columns` in chapters/10-appendices.typ) that can drop what doesn't fit

These are printed for the editor to read and don't fail it:
- a page with fewer than 8 lines
- a hole of 14 or more lines at a page foot in running text, or of 20 or more in an
  entry, when the next page goes on with the same text (a plain section head at the
  top of the next page counts as going on)
- a full-measure line with word gaps at twice the normal width or more
- three or more hyphens at line ends in a row
- a page with 10 or more one-word lines, which is how a collapsed column shows
- a label such as "Look for" as the last line of a page
- uneven columns on the last page of Sources, when that block's numbers need changing

Usage: check_fit.py [TYPST ARGS...], run from the repository root, e.g.
check_fit.py --input edition=draft
It needs Poppler's pdftotext and pdftoppm. Set PDF to check another file, as in
PDF=other.pdf check_fit.py.
"""
import html
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile

PDF = os.environ.get("PDF", "Reading the Wall.pdf")
PT_PER_MM = 72 / 25.4
PAGE_TOP = 25 * PT_PER_MM        # as in book/template.typ
PAGE_BOTTOM = 841.89 - 23 * PT_PER_MM
PITCH = 16.5
HEADER_END = PAGE_TOP - 5        # the running head lies above this

EXPR = """let plain(c) = if type(c) == str { c } else if c.has("text") { c.text } else if c.has("children") { c.children.map(plain).join() } else if c.has("body") { plain(c.body) } else if c == [ ] { " " } else { "" }
(
  heads: query(heading).map(h => (
    level: h.level, page: h.location().page(), y: h.location().position().y.pt(),
    folio: counter(page).at(h.location()).first(), label: str(h.at("label", default: "")),
    text: plain(h.body))),
  parts: query(<part-page>).map(m => m.location().page()),
  strips: query(<strip-page>).map(m => m.location().page()),
)"""


def layout_facts(typst_args):
    run = subprocess.run(["typst", "eval", EXPR, "--root", ".", *typst_args, "--in", "book/main.typ"],
                         capture_output=True, text=True)
    if run.returncode != 0:
        sys.exit(run.stderr)
    return json.loads(run.stdout)


def read_lines(pdf):
    """Each page's lines of text, below the running head: lists of words as
    (x0, y0, x1, y1, text)."""
    out = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    word = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
    pages = []
    for page in out.split("<page ")[1:]:
        lines = []
        for line in page.split("<line ")[1:]:
            words = [(float(a), float(b), float(c), float(d), html.unescape(t)) for a, b, c, d, t in word.findall(line)]
            words = [w for w in words if w[3] > HEADER_END]
            if words:
                lines.append(words)
        pages.append(lines)
    return pages


def ink_bottoms(pdf):
    """The y of the lowest ink on each page, from a coarse grey rendering (P5 PGM files)."""
    bottoms = []
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "36", "-gray", pdf, f"{tmp}/p"], check=True)
        for name in sorted(os.listdir(tmp)):
            data = open(f"{tmp}/{name}", "rb").read()
            header = re.match(rb"P5\s+(\d+)\s+(\d+)\s+\d+\s", data)
            width, height = int(header[1]), int(header[2])
            pixels = data[header.end():]
            low = 0
            for y in range(height - 1, -1, -1):
                if min(pixels[y * width:(y + 1) * width]) < 200:
                    low = y + 1
                    break
            bottoms.append(low * 2.0)      # 36 dpi: 2 pt a pixel
    return bottoms


def line_text(words):
    return " ".join(w[4] for w in words)


def rows(lines):
    """The page's lines grouped by height, whatever column they are in."""
    by_y = {}
    for words in lines:
        by_y.setdefault(round(words[0][3] / 2), []).append(words)
    return by_y


def page_starts_unit(page, facts, starts):
    return page in starts or page in facts["parts"]


def main():
    if not os.path.exists(PDF):
        sys.exit(f"check_fit: no {PDF}")
    facts = layout_facts(sys.argv[1:])
    pages = read_lines(PDF)
    bottoms = ink_bottoms(PDF)
    heads = sorted(facts["heads"], key=lambda h: (h["page"], h["y"]))
    fails, notes = [], []
    n = len(pages)

    # Where the body starts: Chapter 1 on arabic 1, and it must be a right-hand page.
    chapters = [h for h in heads if h["level"] == 1 and h["label"] != "part" and h["folio"] == 1]
    first = next((h for h in chapters if h["page"] > 1), None)
    if first is None:
        fails.append("no chapter opens on arabic page 1")
        offset = 0
    else:
        offset = first["page"] - 1
        if first["page"] % 2 == 0:
            fails.append(f"arabic 1 falls on physical p. {first['page']}, an even page")

    def folio(p):
        return str(p - offset) if p > offset else f"physical {p}"

    # What starts a new text: a chapter, an entry, a grade guide or grade section (they
    # start pages), a part, a film strip that opens an entry's page. A plain section head doesn't.
    starts = set()
    for h in heads:
        if h["y"] > PAGE_TOP + 90:
            continue
        guide = h["label"].startswith("grade")
        grade_section = h["level"] == 2 and re.match(r"V[B0-9]+.*: ", h["text"])
        if h["level"] in (1, 3) or guide or grade_section:
            starts.add(h["page"])
    starts |= set(facts["strips"])

    # The last head before a page says what kind of text it holds.
    def kind(p):
        current = None
        for h in heads:
            if h["page"] > p:
                break
            if h["label"] != "part" and h["level"] <= 3:
                current = h
        return current

    for i, lines in enumerate(pages):
        p = i + 1
        if p <= offset or p in facts["parts"]:
            continue
        by_y = rows(lines)
        count = len(by_y)
        if count == 0:
            fails.append(f"p. {folio(p)} is blank")
            continue
        if count < 3:
            fails.append(f"p. {folio(p)} holds only {count} line(s)")
        elif count < 8:
            notes.append(f"p. {folio(p)} holds only {count} lines")

        # line ends
        hyphens = 0
        for words in lines:
            text = line_text(words)
            if re.search(r"[\w+]–$", text):
                fails.append(f"p. {folio(p)}: a range breaks at a line end: {text[-30:]}")
            if re.fullmatch(r"\[\d+(, ?\d+)*\][.,;]?", text):
                # (in a table a citation can fill a line of its cell)
                others = [w for other in lines if other is not words for w in other
                          if abs(w[3] - words[0][3]) < 2]
                if not others:
                    fails.append(f"p. {folio(p)}: a line holds only a citation: {text}")
            hyphens = hyphens + 1 if text.endswith(("­", "-")) and not text.endswith(" -") else 0
            if hyphens == 3:
                notes.append(f"p. {folio(p)}: three hyphens in a row, near: {text[:40]}")
            # word gaps on full-measure lines, against the line's height
            width = words[-1][2] - words[0][0]
            if len(words) >= 4 and width > 360 and ". . ." not in text:
                ratio = statistics.median(words[j + 1][0] - words[j][2] for j in range(len(words) - 1)) / (words[0][3] - words[0][1])
                if ratio >= 0.41:
                    notes.append(f"p. {folio(p)}: wide word gaps: {text[:50]}")

        # the foot of the page
        ordered = sorted(lines, key=lambda w: w[0][3])
        last_y = ordered[-1][0][3]
        foot = max((w for w in ordered if abs(w[0][3] - last_y) < 2), key=lambda w: w[0][0])
        text = line_text(foot)
        at_foot = abs(bottoms[i] - last_y) < 8
        if at_foot and text.endswith(":"):
            fails.append(f"p. {folio(p)}: a lead-in ends the page: {text[-50:]}")
        if at_foot and re.fullmatch(r"(how to do it|look for|symptoms|common mistakes|when to use it.*)", text.lower()):
            notes.append(f"p. {folio(p)}: a label ends the page: {text}")
        for h in heads:
            if h["page"] == p and h["level"] in (2, 3, 4) and at_foot and h["text"].replace("\u00a0", " ").endswith(text):
                fails.append(f"p. {folio(p)}: a head ends the page: {h['text'][:50]}")

        # a hole at the foot, when the next page goes on with this text
        white = (PAGE_BOTTOM - bottoms[i]) / PITCH
        if p < n and not page_starts_unit(p + 1, facts, starts):
            h = kind(p)
            running = h is not None and h["level"] < 3
            if white >= (14 if running else 20):
                where = h["text"][:40] if h else ""
                notes.append(f"p. {folio(p)}: {white:.0f} white lines at the foot, inside {where}")

        # a collapsed column: many lines of one word, each alone at its height
        alone = sum(1 for ws in by_y.values() if len(ws) == 1 and len(ws[0]) == 1 and len(ws[0][0][4]) >= 4 and ws[0][0][4].isalpha())
        if alone >= 10:
            notes.append(f"p. {folio(p)}: {alone} lines of one word")

    # The sources sit in a block of a set height, which can drop what doesn't fit.
    sources = next((h for h in heads if h["level"] == 1 and h["text"] == "Sources"), None)
    index = next((h for h in heads if h["level"] == 1 and h["text"] == "Index"), None)
    if sources and index:
        cited, listed = set(), set()
        for lines in pages[:sources["page"] - 1]:
            for words in lines:
                for group in re.findall(r"\[(\d+(?:, ?\d+)*)\]", line_text(words)):
                    cited |= {int(x) for x in group.split(",")}
        for lines in pages[sources["page"] - 1:index["page"] - 1]:
            listed |= {int(w[4][:-1]) for words in lines for w in words if re.fullmatch(r"\d{1,3}\.", w[4])}
        missing = sorted(cited - listed)
        if missing:
            fails.append(f"sources {missing[:5]} are cited but missing: raise `pages` or `last` in chapters/10-appendices.typ")
        last_page = pages[index["page"] - 2]
        foot = {side: max((w[3] for words in last_page for w in words if (w[0] < 297.6) == side), default=0)
                for side in (True, False)}
        if abs(foot[True] - foot[False]) > 3 * PITCH:
            notes.append(f"the last page of Sources has columns ending at {foot[True]:.0f} and {foot[False]:.0f} pt: "
                         "adjust `pages` or `last` in chapters/10-appendices.typ")

    for line in notes:
        print(f"check_fit: {line}")
    for line in fails:
        print(f"check_fit: FAULT {line}")
    print(f"check_fit: {n} pages, {len(fails)} faults, {len(notes)} notes")
    if fails:
        sys.exit(1)


main()
