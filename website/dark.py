"""Dark copies of the drawings, for the site's dark mode.

Each figure gets a second file, and <picture> picks it. This can't be done inside one
file: Safari doesn't tell an SVG loaded as an image that the page is dark, so
light-dark() and media queries in the file never apply there.

A dark copy changes as little as it can. Inverting the tones would make the climber
look see-through and the pelican black, and would make "the right limbs white" false.
So anything with a body keeps its tones and its own outline: the climber, holds,
volumes, the pelican. Only what is drawn straight on the paper changes:

- The paper itself goes dark: the frames of a film strip, the halos behind labels, and
  earlier positions, which are white on paper only so that they look see-through.
- The wall's pale band and the grid of dots go quieter, and shoes get lighter.
- Black lines and text blend with what's behind them ("difference"), so they are light
  on the dark page and stay dark where they cross a white limb.

Lines are blended in groups. They are drawn as many overlapping pieces, and blending
each piece alone would cancel the overlaps out and leave the line dashed.

A coloured hold is left as it was drawn, lines included. Blending a black line over a
colour gives the opposite colour, e.g. a pink outline on a teal hold.
"""
import re

PAGE = "#171614"            # the dark page, --paper in style.css
DOTS = "#5c5a55"            # the grid of dots on the wall
WALL = "#34322d"            # the pale band beside a wall seen from the side
SHOE = "#4d4b45"            # would vanish into the page in its own near-black
BLACK = {"#000000", "#2a2a2a"}
WHITE = "#ffffff"
GHOST_LINES = {"#777777", "#8c8c8c"}
LIGHT_ON_DARK = "#ffffff"   # what "difference" turns into its opposite
STYLE = "<style>.m{mix-blend-mode:difference}</style>"

TOKEN = re.compile(r"<[^>]+>|[^<]+")
GREY = re.compile(r"#([0-9a-fA-F]{2})\1\1")
SHAPE = re.compile(r"<(path|circle|ellipse|polygon|polyline|rect|line)\b[^>]*/>")


def attr(tag, name):
    m = re.search(rf'\s{name}="([^"]*)"', tag)
    return m.group(1) if m else None


def with_attr(tag, name, value):
    return re.sub(rf'(\s{name}=")[^"]*(")', rf"\g<1>{value}\g<2>", tag)


def coloured(fill):
    return fill is not None and fill.startswith("#") and not GREY.fullmatch(fill)


def ghost_outline(tag):
    return attr(tag, "stroke") in GHOST_LINES and attr(tag, "stroke-dasharray") is not None


class DarkCopy:
    """The copy being written, with a blended group open while lines are coming."""

    def __init__(self):
        self.parts = []
        self.blending = False
        self.holds = set()      # the paths of coloured holds
        self.ghost_lines = 0    # dashed outlines of an earlier position, just drawn
        self.ghost_fills = 0    # the white pieces still to come for those outlines

    def plain(self, *parts):
        self.stop_blending()
        self.parts += parts

    def blend(self, *parts):
        if not self.blending:
            self.parts.append('<g class="m">')
            self.blending = True
        self.parts += parts

    def stop_blending(self):
        if self.blending:
            self.parts.append("</g>")
            self.blending = False

    def is_ghost(self, tag, fill, stroke):
        """Whether `tag` is a white piece of an earlier position. It may carry its dashed
        outline itself, or come after a run of outlines, one piece for each."""
        if ghost_outline(tag):
            self.ghost_lines += 1
            self.ghost_fills = self.ghost_lines
            return fill == WHITE
        self.ghost_lines = 0
        if fill == WHITE and stroke is None and self.ghost_fills:
            self.ghost_fills -= 1
            return True
        self.ghost_fills = 0
        return False

    def shape(self, tag):
        fill, stroke, path = attr(tag, "fill"), attr(tag, "stroke"), attr(tag, "d")
        if self.is_ghost(tag, fill, stroke):
            self.plain(with_attr(tag, "fill", PAGE))
        elif coloured(fill):
            self.holds.add(path)
            self.plain(tag)
        elif fill == "none" and path and path in self.holds:
            self.plain(tag)
        elif fill in BLACK:
            tag = with_attr(tag, "stroke", LIGHT_ON_DARK) if stroke in BLACK else tag
            self.blend(with_attr(tag, "fill", LIGHT_ON_DARK))
        elif fill == "#262626":
            self.plain(with_attr(tag, "fill", SHOE))
        elif fill == "none" and stroke in BLACK:
            self.blend(with_attr(tag, "stroke", LIGHT_ON_DARK))
        elif fill == "#b0b0b0":
            self.plain(with_attr(tag, "fill", DOTS))
        elif fill == "#ececec" and stroke is None:
            self.plain(with_attr(tag, "fill", WALL))
        elif fill == WHITE and tag.startswith("<rect"):
            self.plain(with_attr(tag, "fill", PAGE))
        else:
            self.plain(tag)

    def text(self, tag, rest):
        fill, stroke = attr(tag, "fill"), attr(tag, "stroke")
        if stroke == WHITE:     # the halo behind a label
            self.plain(with_attr(with_attr(tag, "fill", PAGE), "stroke", PAGE), *rest)
        elif fill == WHITE:     # a number on a black disc: blended apart from the disc, or it merges with it
            self.stop_blending()
            self.blend(tag, *rest)
            self.stop_blending()
        elif fill in BLACK:
            self.blend(with_attr(tag, "fill", LIGHT_ON_DARK), *rest)
        elif fill is None:
            self.blend(tag.replace("<text", f'<text fill="{LIGHT_ON_DARK}"', 1), *rest)
        else:
            self.plain(tag, *rest)

    def clip(self, tokens, i):
        """Copy the clip path at `tokens[i]` and, if it is a coloured hold's outline, the
        group it clips, whose shading stays as drawn too. Returns where to go on."""
        end = tokens.index("</clipPath>", i)
        path = next((attr(t, "d") for t in tokens[i:end] if attr(t, "d")), None)
        self.plain(*tokens[i:end + 1])
        i = end + 1
        if not path or path not in self.holds:
            return i
        depth = 0
        while i < len(tokens):
            depth += tokens[i].startswith("<g") - tokens[i].startswith("</g")
            self.plain(tokens[i])
            i += 1
            if depth == 0 and tokens[i - 1].startswith("</g"):
                break
        return i


def dark_copy(svg):
    """The dark version of the SVG text `svg`."""
    copy = DarkCopy()
    tokens = TOKEN.findall(svg)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.startswith("<clipPath"):
            i = copy.clip(tokens, i)
            continue
        if token.startswith("<text"):
            end = tokens.index("</text>", i)
            copy.text(token, tokens[i + 1:end + 1])
            i = end
        elif SHAPE.fullmatch(token):
            copy.shape(token)
        elif token.startswith("<") or token.strip():
            copy.plain(token)
        else:
            copy.parts.append(token)
        i += 1
    copy.stop_blending()
    return re.sub(r"(<svg\b[^>]*>)", lambda m: m.group(1) + STYLE, "".join(copy.parts), count=1)
