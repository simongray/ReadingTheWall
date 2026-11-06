"""Make a test chart for checking the figures' colours on a real e-reader.

Usage: python3 tools/colour_chart.py [OUT.pdf]
Run ./build.sh first, since the chart's samples come from book/figures. Open
the PDF in the app you read the book with and follow what it says on the page.

The chart answers what the book's own maths can't: which sum this device uses
to turn colour into grey, whether its contrast settings treat a colour and its
matching grey alike, and whether a painted figure looks like its grey drawing.
"""
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES = os.path.join(ROOT, "book", "figures")
sys.path.insert(0, os.path.join(ROOT, "figtools"))
import paint  # noqa: E402

SAMPLES = ("cover", "sloper", "dynamic-slab", "reading-worked-problem")

# The sums disagree most about the pure primaries, so where red, green and blue
# land on the ladder shows which sum a device uses:
#   the weights in the PDF engines   4.5  8.8  1.7
#   Android's weights                3.2 10.7  1.1
#   luminance, D65 white             7.5 12.9  4.5
#   luminance, D50 white             7.6 13.0  4.1
#   Rockchip's compositor            5    7    2
PRIMARIES = (("Red", "#ff0000"), ("Green", "#00ff00"), ("Blue", "#0000ff"))

PAGE = """
#set page(paper: "a4", margin: 13mm)
#set text(font: "Iowan Old Style", size: 11pt)
#set par(justify: false)
#set block(spacing: 0.7em)

#let ladder(colour) = {
  block(width: 100%, spacing: 0pt, rect(width: 100%, height: 12mm, fill: rgb(colour), stroke: none))
  block(width: 100%, spacing: 0pt, grid(columns: (1fr,) * 16,
    ..range(16).map(i => rect(width: 100%, height: 12mm, stroke: none, inset: 0pt,
      fill: luma(i * 17))),
  ))
  block(width: 100%, above: 1mm, grid(columns: (1fr,) * 16,
    ..range(16).map(i => align(center, text(size: 8pt, str(i)))),
  ))
}

#let patch(colour, partner, label) = box(width: 21mm, inset: (bottom: 2mm))[
  #rect(width: 100%, height: 15mm, fill: rgb(colour), stroke: none, inset: 0pt,
    align(center + horizon, rect(width: 50%, height: 50%, fill: luma(partner), stroke: none)))
  #v(-2mm)
  #text(size: 8pt, label)
]
"""


def _typst(pairs_by_row, svgs):
    t = [PAGE]
    t.append("= Colour test for the book's figures\n")
    t.append("Read this in the app and with the settings you read the book with. "
             "Write down the app's Dark Color Enhancement and Light Color Filter "
             "values, then answer the three questions.\n")
    t.append("== 1. Which sum turns colour into grey?\n")
    t.append("Each band of colour sits on a ladder of the panel's 16 greys. Find "
             "where the edge between the band and the ladder disappears, and write "
             "down that number for each band.\n")
    for name, colour in PRIMARIES:
        t.append(f'#block(breakable: false)[#text(size: 9pt, "{name}") #ladder("{colour}")]\n')
    t.append("#pagebreak()\n== 2. Do the colours match their greys?\n")
    t.append("Each patch has a square of its matching grey in the middle. On a "
             "monochrome screen the square should vanish, or nearly. Note any "
             "square that stands out clearly.\n")
    for title, pairs in pairs_by_row:
        t.append(f'#block(breakable: false)[#text(size: 9pt, weight: 700, "{title}")\\\n')
        for colour, partner, label in pairs:
            # luma(), because Typst writes a figure's neutral greys that way too
            t.append(f'#patch("{colour}", {int(partner[1:3], 16)}, "{label}") ')
        t.append("]\n")
    t.append("#pagebreak()\n== 3. Does a painted figure look like its grey drawing?\n")
    t.append("Each row shows the grey drawing on the left and the painted figure on "
             "the right. On a monochrome screen the two should look the same.\n")
    for grey, painted in svgs:
        t.append("#block(breakable: false, above: 5mm, grid(columns: (1fr, 1fr), gutter: 5mm,"
                 f' image("{grey}", width: 100%, height: 50mm, fit: "contain"),'
                 f' image("{painted}", width: 100%, height: 50mm, fit: "contain")))\n')
    return "".join(t)


def _unpaint(svg):
    """Turn the painted SVG text `svg` back into its grey drawing."""
    for colour, partner in paint._pairs():
        svg = svg.replace(colour, partner)
    return svg


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "colour-chart.pdf")
    p = paint
    holds = (("forest", p.FOREST), ("yellow", p.YELLOW), ("rust", p.RUST),
             ("denim", p.DENIM), ("violet", p.VIOLET), ("brick", p.BRICK),
             ("teal", p.TEAL), ("raspberry", p.RASPBERRY))
    rows = [(title, [(h[i], p.hold_greys(h)[i], n) for n, h in holds])
            for i, title in enumerate(("Holds", "Shades on holds: lit rim and grain",
                                       "Shades on holds: chalk",
                                       "Shades on holds: the palest",
                                       "Shades on holds: dark crescent"))]
    rows.append(("The block arrow and the muscles",
                 [(p.AMBER, p.BLOCK_ARROW, "arrow"),
                  (p.MUSCLE_RED, p.MUSCLE_DOTS[p.WHITE], "dots"),
                  (p.MUSCLE_PINK, p.MUSCLE_BAND, "band")]))
    rows.append(("The pelican", [(c, g, g[1:3]) for g, c in p.COVER.items()]))
    with open(os.path.join(ROOT, "book", "template.typ")) as f:
        tabs = re.findall(r'rgb\("(#[0-9a-f]{6})"\), figures', f.read())
    rows.append(("Grade tabs", [(c, "#%02x" % (round(p._greys(c)[0] / 17) * 17), f"V{i}")
                                for i, c in zip((1, 2, 3, 4, 5, 6), tabs)]))
    with tempfile.TemporaryDirectory() as d:
        svgs = []
        for name in SAMPLES:
            with open(os.path.join(FIGURES, name + ".svg")) as f:
                svg = f.read()
            for suffix, text in (("grey", _unpaint(svg)), ("painted", svg)):
                with open(os.path.join(d, f"{name}-{suffix}.svg"), "w") as f:
                    f.write(text)
            svgs.append((f"{name}-grey.svg", f"{name}-painted.svg"))
        src = os.path.join(d, "chart.typ")
        with open(src, "w") as f:
            f.write(_typst(rows, svgs))
        subprocess.run(["typst", "compile", "--root", d, src, os.path.abspath(out)],
                       check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
