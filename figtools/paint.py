"""The colours of the figures, added once they have been drawn in grey.

The book is read mostly on a monochrome e-reader, so each colour here keeps
the panel grey of the shape it paints. That holds under each of the sums a
device might use to turn colour into grey, and the build fails if a colour
drifts. A monochrome reader sees the grey drawing and loses nothing. Yellow
holds are the one exception, as yellow can't stay yellow at the holds' darkness.

On a real wall one problem is one colour, and the wall as a whole has many.
So a figure's holds share one colour. In a technique entry the colour follows
the entry's grade, as on the walls at Boulders, and it's read from the chapters
so that it follows any change of grade. The cover and the atlases, which show
many holds at once, use several.

The climber, the wall and the volumes stay neutral, apart from the red that
marks the muscles at work. Otherwise only outlined areas take colour, because
fine lines lose their hue on colour e-paper. research/COLOUR.md has the reasons.
"""

import glob
import itertools
import math
import os
import re
import sys
import zlib

from climb import (BLOCK_ARROW, DARK, HOLD_DEEP, HOLD_LIGHT, HOLD_MID, HOLD_PALE,
                   MUSCLE_BAND, MUSCLE_DOTS, WHITE)

# The block arrow: the hips or the whole body move this way.
AMBER = "#f2c55f"

# Muscles at work, as dots (climb.MUSCLE_DOTS) and as a band.
MUSCLE_RED = "#9c3d30"
MUSCLE_PINK = "#ffb5ac"

# Hold colours, on the panel's #555555 except for yellow. Each comes with the
# shades drawn on it, for the climb.py greys HOLD_MID, HOLD_LIGHT, HOLD_PALE and
# HOLD_DEEP. Chalk and light are white on top of the colour, so the first three
# are the colour mixed with white (in Oklab, which keeps its hue) until it reaches
# the panel level. The last is the same hue in shadow. Orange loses most of its
# hue at this darkness, and white would take the rest, so its shades keep their
# colour, which leaves real orange in the rim and the grain.
FOREST = ("#346841", "#74977b", "#c3d2c6", "#e6ede7", "#1a4325")
RUST = ("#944600", "#d7732b", "#ffb88e", "#ffe1d0", "#5d2a00")
DENIM = ("#325a94", "#7390b9", "#c3cfe2", "#e6ecf3", "#173765")
VIOLET = ("#654496", "#9480ba", "#d1c9e3", "#ede9f4", "#43286a")
BRICK = ("#9c3d30", "#bf7a6e", "#e6c5bf", "#f5e8e6", "#6b2117")
TEAL = ("#266666", "#6e9695", "#c1d2d1", "#e6edec", "#0e4242")
RASPBERRY = ("#953a63", "#b8748f", "#e3c3ce", "#f4e8ec", "#671e41")
HOLD_GREYS = (DARK, HOLD_MID, HOLD_LIGHT, HOLD_PALE, HOLD_DEEP)

# Yellow turns olive at the holds' darkness, which doesn't read as yellow at all.
# So yellow holds are lighter, and each shade holds a grey of its own instead. On
# a monochrome screen they show lighter than other holds, which suits the grade
# tabs, as those get lighter the easier the grade.
YELLOW = ("#c6ad25", "#e9ce3d", "#f4de73", "#fcefb2", "#927e00")
YELLOW_GREYS = ("#aaaaaa", "#cccccc", "#dddddd", "#eeeeee", "#777777")

# Yellow comes fifth, where it lands on a big hold in both atlases. It shows lighter than the
# others on a monochrome screen, so a small hold in that shade would be easy to miss.
HOLDS = (FOREST, RASPBERRY, DENIM, BRICK, YELLOW, TEAL, VIOLET, RUST)

# A figure in a technique entry takes the hold colour of the entry's grade, from
# V0 up, as in the circuits at Boulders (see grade-tabs in book/template.typ).
# Its black holds stay as drawn, in grey.
BY_GRADE = (FOREST, FOREST, YELLOW, RUST, DENIM, VIOLET, BRICK, HOLD_GREYS)

# A figure with no known grade takes a colour that doesn't claim one, as these
# two aren't among the circuits' colours.
NO_GRADE = (TEAL, RASPBERRY)

# Figures that need a particular colour. The two worked-problem figures show
# the same problem, so they have to match.
CHOSEN = {
    "legend": TEAL,
    "reading-worked-problem": TEAL,
    "filmstrip-worked-problem": TEAL,
}

# Figures with a different hold colour for each hold in turn.
ATLASES = ("hand-atlas", "foot-atlas")

# The cover's pelican in its real colours, and its problem in one colour among
# the holds of other problems. The holds are in the order figs_cover.py draws
# them: the pelican's four come first.
COVER = {
    "#d4d4d4": "#f9cd80",  # bill
    "#b4b4b4": "#edad4b",  # pouch
    "#a4a4a4": "#eb955f",  # toes
    "#bdbdbd": "#ebb284",  # webs between the toes
    "#9a9a9a": "#dd855f",  # nail of the bill
    "#6e6e6e": "#8e6541",  # wrinkles in the pouch
    "#5c5c5c": "#7e5239",  # lines on the toes
}
COVER_HOLDS = (DENIM, DENIM, DENIM, DENIM,
               RUST, FOREST, TEAL, BRICK, VIOLET, YELLOW)


def figure_grades(chapters):
    """Map each figure to the grade of its technique entry, reading the entries
    in the folder `chapters`. A film strip sits before its entry and takes its
    name, so that's how it's found."""
    grades = {}
    for path in glob.glob(os.path.join(chapters, "*.typ")):
        with open(path) as f:
            text = f.read()
        for entry in re.findall(r"#technique\(.*?\n\)", text, re.S):
            key = re.search(r'key:\s*"([^"]+)"', entry)
            grade = re.search(r"grade:\s*(-?\d+)", entry)
            if key and grade:
                g = int(grade.group(1))
                for figure in (key.group(1), "filmstrip-" + key.group(1),
                               *re.findall(r'"([a-z0-9-]+)\.svg"', entry)):
                    grades.setdefault(figure, g)
    return grades


def _grade(name, grades):
    """The grade of the figure `name`: in its file name for a worked reading,
    such as reading-v3-slab, and otherwise in `grades`."""
    reading = re.match(r"reading-v(\d+)-", name)
    return int(reading.group(1)) if reading else grades.get(name)


def _hold_colour(name, grade):
    """The hold colour of the figure `name`, whose entry has the grade `grade`,
    or None if it has none."""
    if name in CHOSEN:
        return CHOSEN[name]
    if grade is None:
        return NO_GRADE[zlib.crc32(name.encode()) % len(NO_GRADE)]
    return BY_GRADE[min(max(grade, 0), len(BY_GRADE) - 1)]


def _holds(svg, hold):
    for grey, colour in zip(HOLD_GREYS, hold):
        svg = svg.replace(grey, colour)
    return svg


def _in_turn(svg, holds):
    """Give each hold in `svg` the next of `holds`. A hold's shades are clipped
    to its outline, so its outline finds them. A pocket's hollow isn't clipped,
    so it takes the palest shade of the hold drawn just before it."""
    turn = itertools.cycle(holds)
    for outline in re.findall(f'<path d="([^"]+)" fill="{DARK}"', svg):
        hold = next(turn)
        body = f'<path d="{outline}" fill="{DARK}"'
        svg = svg.replace(body, f'<path d="{outline}" fill="{hold[0]}"', 1)
        shades = rf'(<path d="{re.escape(outline)}"/></clipPath><g clip-path="[^"]+">)(.*?</g>)'
        svg = re.sub(shades, lambda m: m.group(1) + _holds(m.group(2), hold), svg,
                     count=1, flags=re.S)
    palest = {hold[0]: hold[3] for hold in holds}
    pale = HOLD_PALE

    def hollow(m):
        nonlocal pale
        if m.group(1):
            pale = palest[m.group(1)]
            return m.group(0)
        return pale
    bodies = "|".join(palest)
    return re.sub(f'<path d="[^"]+" fill="({bodies})"|{HOLD_PALE}', hollow, svg)


def paint(svg, name, grade=None):
    """Return the SVG text `svg` of the figure `name` with its colours added,
    for an entry with the grade `grade`.

    The icons beside the asides stay grey, because they recur on nearly every
    page and should stay quiet."""
    if name.startswith("icon-"):
        return svg
    svg = svg.replace(BLOCK_ARROW, AMBER)
    svg = svg.replace(MUSCLE_DOTS[WHITE], MUSCLE_RED).replace(MUSCLE_BAND, MUSCLE_PINK)
    if name == "cover":
        for grey, colour in COVER.items():
            svg = svg.replace(grey, colour)
        return _holds(_in_turn(svg, COVER_HOLDS), DENIM)
    if name in ATLASES:
        svg = _in_turn(svg, HOLDS)
    return _holds(svg, _hold_colour(name, grade))


def hold_greys(hold):
    """The greys that the colour and shades of `hold` have to match."""
    return YELLOW_GREYS if hold is YELLOW else HOLD_GREYS


def _pairs():
    """Every colour with the grey it has to match."""
    yield AMBER, BLOCK_ARROW
    yield MUSCLE_RED, MUSCLE_DOTS[WHITE]
    yield MUSCLE_PINK, MUSCLE_BAND
    for hold in HOLDS:
        yield from zip(hold, hold_greys(hold))
    for grey, colour in COVER.items():
        yield colour, grey


def _rgb(colour):
    return tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5))


def _linear(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(colour, weights):
    """The luminance of `colour` under `weights`, on the sRGB curve."""
    y = sum(w * _linear(c) for w, c in zip(weights, _rgb(colour)))
    return 255 * (12.92 * y if y <= 0.0031308 else 1.055 * y ** (1 / 2.4) - 0.055)


def _greys(colour):
    """The grey of `colour` under each sum a device might use: the weights in
    the PDF engines, Android's weights, the exact Rec. 709 weights, and luminance
    for a D65 or a D50 white, which a colour-managed engine follows because Typst
    tags its colours as sRGB."""
    r, g, b = _rgb(colour)
    return (0.3 * r + 0.59 * g + 0.11 * b,
            0.213 * r + 0.715 * g + 0.072 * b,
            0.2126 * r + 0.7152 * g + 0.0722 * b,
            _luminance(colour, (0.2126, 0.7152, 0.0722)),
            _luminance(colour, (0.2225, 0.7169, 0.0606)))


def _rockchip(colour):
    """The grey of `colour` in Rockchip's e-ink compositor, which keeps only
    the top four bits instead of rounding."""
    r, g, b = _rgb(colour)
    return (11 * r + 16 * g + 5 * b) // 32


def _landings(grey):
    """The panel levels `grey` can land on: rounding to the nearest of 16 greys,
    and dropping the low bits. Engines first reduce a grey to 8 bits, some by
    flooring and some by rounding, and their sums run slightly either side of
    the exact weights."""
    values = (math.floor(grey - 0.01), round(grey + 0.01))
    return {round(v / 17) for v in values}, {v >> 4 for v in values}


def _same_level(grey, partner):
    """Whether `grey` can only land where `partner` does."""
    rounded, top = _landings(grey)
    partner_rounded, partner_top = _landings(partner)
    return rounded <= partner_rounded and top <= partner_top


def drifted():
    """The colours whose grey can leave the panel level of their partner."""
    bad = []
    for colour, partner in _pairs():
        t = _rgb(partner)[0]
        greys = _greys(colour)
        if not all(_same_level(g, t) for g in greys) or _rockchip(colour) >> 4 != t >> 4:
            bad.append(f"{colour} for {partner}: " +
                       ", ".join(f"{g:.1f}" for g in greys) +
                       f", {_rockchip(colour)}")
    return bad


def paint_all(folder):
    """Paint every SVG in `folder`, or exit if a colour has drifted."""
    bad = drifted()
    if bad:
        sys.exit("paint.py: colours off their panel grey:\n  " + "\n  ".join(bad))
    grades = figure_grades(os.path.join(folder, "..", "chapters"))
    for path in glob.glob(os.path.join(folder, "*.svg")):
        name = os.path.basename(path)[:-4]
        with open(path) as f:
            svg = f.read()
        painted = paint(svg, name, _grade(name, grades))
        if painted != svg:
            with open(path, "w") as f:
                f.write(painted)
