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
- The wall's pale band, the far face of an arête and the grid of dots go quieter, and
  shoes get lighter. Left pale, the far face would need heavy halos around its labels.
- The shadow a hold throws on the wall goes darker than the page. Left pale, it glows.
- Black lines and text blend with what's behind them ("difference"), so they are light
  on the dark page and stay dark where they cross a white limb.

Lines are blended in groups. They are drawn as many overlapping pieces, and blending
each piece alone would cancel the overlaps out and leave the line dashed.

A detail that lies wholly on a body, such as a crease, a nail or a hem, stays plain
black. Blended, its tip would turn white where it runs onto the body's black outline.

A coloured hold is left as it was drawn, lines included. Blending a black line over a
colour gives the opposite colour, e.g. a pink outline on a teal hold.

So are the fine dashes that show what a hand or a shoe hides. They run around the whole
shape, on top of its black outline, and blending would make them white dashes there.
"""
import re
from itertools import groupby

PAGE = "#171614"           # the dark page, --paper in style.css
DOTS = "#5c5a55"            # the grid of dots on the wall
WALL = "#34322d"            # the pale band beside a wall seen from the side
FAR_FACE = "#403e38"        # the far face of an arête: further from the page than the band
FAR_FACE_LIGHT = "#6e6c66"  # its bolt holes, and its rounded edge where that catches the light
SHOE = "#4d4b45"            # would vanish into the page in its own near-black
SHADOW = "#0b0a09"          # a hold's shadow on the wall
CAST_SHADOW = "#dddddd"     # ROCK_SHADOW in figtools/climb.py
XRAY_LINE = "#2a2a2a"       # XRAY_STYLE in figtools/climb.py
BLACK = {"#000000", XRAY_LINE}
WHITE = "#ffffff"
LEFT_LIMB = "#aaaaaa"       # LEFT in figtools/climb.py
BODY = {WHITE, LEFT_LIMB}
FAR_FACES = {"#cccccc", "#d4d4d4"}  # wrap_panel in figtools/authored.py, ARETE_SIDE in figs_terrain.py
FAR_FACE_DOTS = "#a0a0a0"   # arete_wall in figtools/figs_terrain.py
FAR_FACE_SHARE = 0.08       # of the figure's area that a far face covers at least
EDGE_STOPS = {WHITE: FAR_FACE_LIGHT, "#d4d4d4": FAR_FACE}   # the gradient on an arête's edge
GHOST_LINES = {"#777777", "#8c8c8c"}
LIGHT_ON_DARK = "#ffffff"   # what "difference" turns into its opposite
STYLE = "<style>.m{mix-blend-mode:difference}</style>"

TOKEN = re.compile(r"<[^>]+>|[^<]+")
GREY = re.compile(r"#([0-9a-fA-F]{2})\1\1")
SHAPE = re.compile(r"<(path|circle|ellipse|polygon|polyline|rect|line)\b[^>]*/>")
GROUP = re.compile(r"</?g\b")
SCALE = re.compile(r"scale\(([\d.]+)\)")
VIEW_BOX = re.compile(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"')
PATH_STEP = re.compile(r"([a-zA-Z])([^a-zA-Z]*)")
NUMBER = re.compile(r"-?[\d.]+")
AROUND = [(1, 0), (.7, .7), (0, 1), (-.7, .7), (-1, 0), (-.7, -.7), (0, -1), (.7, -.7)]
LINE_STEPS = 16             # a straight line can cross a gap anywhere along it


def attr(tag, name):
    m = re.search(rf'\s{name}="([^"]*)"', tag)
    return m.group(1) if m else None


def with_attr(tag, name, value):
    return re.sub(rf'(\s{name}=")[^"]*(")', rf"\g<1>{value}\g<2>", tag)


def coloured(fill):
    return fill is not None and fill.startswith("#") and not GREY.fullmatch(fill)


def ghost_outline(tag):
    return attr(tag, "stroke") in GHOST_LINES and attr(tag, "stroke-dasharray") is not None


def kind(tag):
    fill, stroke = attr(tag, "fill"), attr(tag, "stroke")
    if fill == "none" and stroke in BLACK and attr(tag, "stroke-dasharray") is None:
        return "line"
    return "fill" if fill != "none" and stroke is None else "other"


def limb_outlines(shapes):
    """The paths of the limbs' outlines. A limb is a run of thick black lines with the
    same shapes filled on top, so that only the outer half of each line shows."""
    outlines = set()
    runs = [(k, list(group)) for k, group in groupby(shapes, kind)]
    for (first, lines), (second, fills) in zip(runs, runs[1:]):
        if first == "line" and second == "fill":
            filled = {attr(tag, "d") for tag in fills}
            widths = {attr(tag, "stroke-width") for tag in lines if attr(tag, "d") in filled}
            outlines |= {attr(tag, "d") for tag in lines if attr(tag, "stroke-width") in widths}
    return outlines


def cast_shadows(shapes):
    """The paths of the shadows that holds and volumes throw on the wall. These are runs
    of a pale grey with no outline. A finger behind the hand can have the same grey, but
    has an outline of its own or comes right before the hand."""
    lines = {attr(tag, "d") for tag in shapes if kind(tag) == "line"}
    shadows = set()
    runs = [(pale, list(group)) for pale, group in groupby(
        shapes, lambda tag: attr(tag, "fill") == CAST_SHADOW and attr(tag, "stroke") is None)]
    for (pale, tags), (_, after) in zip(runs, runs[1:] + [(False, [""])]):
        if pale and not (attr(after[0], "fill") == WHITE and attr(after[0], "stroke") in BLACK):
            shadows |= {attr(tag, "d") for tag in tags} - lines
    return shadows


def flatten(d, curve_steps):
    """The subpaths of the path `d` as lists of points, with `curve_steps` on each curve.
    An empty list means the path uses a command that isn't read here. Arcs only draw a
    hold's small dots, so they add no points."""
    subpaths = []
    for command, numbers in PATH_STEP.findall(d):
        n = [float(x) for x in NUMBER.findall(numbers)]
        if command == "M":
            subpaths.append([(n[0], n[1])])
        elif command == "L":
            x, y = subpaths[-1][-1]
            subpaths[-1] += [(x + (n[0] - x) * i / LINE_STEPS, y + (n[1] - y) * i / LINE_STEPS)
                             for i in range(1, LINE_STEPS + 1)]
        elif command == "C":
            x, y = subpaths[-1][-1]
            for i in range(1, curve_steps + 1):
                t = i / curve_steps
                a, b, c, e = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
                subpaths[-1].append((a * x + b * n[0] + c * n[2] + e * n[4],
                                     a * y + b * n[1] + c * n[3] + e * n[5]))
        elif command not in "Za":
            return []
    return subpaths


def inside(subpaths, x, y):
    """Whether the point is inside the shape, by SVG's default rule for filling it."""
    winding = 0
    for points in subpaths:
        for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]):
            if (y0 <= y) != (y1 <= y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
                winding += 1 if y1 > y0 else -1
    return winding != 0


def points_on(tag):
    """Points along the black mark `tag`, or none if it isn't a path or a circle."""
    if tag.startswith("<circle"):
        x, y, r = (float(attr(tag, name)) for name in ("cx", "cy", "r"))
        return [(x, y)] + [(x + r * dx, y + r * dy) for dx, dy in AROUND]
    if tag.startswith("<path"):
        return [point for points in flatten(attr(tag, "d"), 4) for point in points]
    return []


class Surfaces:
    """What is painted so far in one coordinate system, and how far the thickest outline
    shows past the shape it surrounds."""

    def __init__(self, scale=1):
        self.shapes = []        # (bounding box, subpaths, whether it's a body), top last
        self.reach = 0
        self.scale = scale      # how much larger than these coordinates the figure draws them

    def add(self, tag):
        """Note the plain shape `tag`, in the colour it has in the dark copy."""
        fill = attr(tag, "fill")
        if attr(tag, "stroke") in BLACK and attr(tag, "stroke-dasharray") is None:
            self.reach = max(self.reach, float(attr(tag, "stroke-width") or 0) / 2)
        if not tag.startswith("<path") or fill in ("none", None):
            return
        subpaths = flatten(attr(tag, "d"), 2)
        points = [point for points in subpaths for point in points]
        if len(points) > 2:
            xs, ys = zip(*points)
            self.shapes.append(((min(xs), min(ys), max(xs), max(ys)), subpaths, fill in BODY))

    def top_is_body(self, x, y):
        """Whether the top shape at the point is a body, or None if no shape is there."""
        for (x0, y0, x1, y1), subpaths, body in reversed(self.shapes):
            if x0 <= x <= x1 and y0 <= y <= y1 and inside(subpaths, x, y):
                return body
        return None

    def on_body(self, x, y):
        """Whether the point lies on a body or on the outline around one."""
        body = self.top_is_body(x, y)
        if body is None:
            return any(self.top_is_body(x + self.reach * dx, y + self.reach * dy)
                       for dx, dy in AROUND)
        return body


class DarkCopy:
    """The copy being written, with a blended group open while lines are coming."""

    def __init__(self, outlines, shadows, area):
        self.parts = []
        self.blending = False
        self.outlines = outlines
        self.shadows = shadows
        self.area = area        # of the whole figure
        self.holds = set()      # the paths of coloured holds
        self.ghost_lines = 0    # dashed outlines of an earlier position, just drawn
        self.ghost_fills = 0    # the white pieces still to come for those outlines
        self.frames = set()     # the ids of clip paths that only trim a panel to its frame
        self.clipped = 0        # how deep we are inside a group clipped to a shape
        self.surfaces = [Surfaces()]    # one for each open group, the innermost last
        self.details = []       # details on a body, to go on top of the blended group

    def group(self, token):
        """Copy a group's tag, noting whether it starts or ends a group clipped to a
        shape. A group with a transform has its own coordinates, so shapes outside it
        can't be compared with those inside."""
        if token.startswith("</g"):
            self.clipped = max(self.clipped - 1, 0)
            self.surfaces.pop()
        else:
            clip = attr(token, "clip-path")
            if self.clipped or (clip and clip[5:-1] not in self.frames):
                self.clipped += 1
            scale = SCALE.search(token)
            self.surfaces.append(Surfaces(float(scale[1]) if scale else 1)
                                 if "transform" in token else self.surfaces[-1])
        self.plain(token)

    def plain(self, *parts):
        self.stop_blending()
        self.parts += parts

    def draw(self, tag):
        """Copy a shape as it is, noting what it leaves on top. A clipped shape can be
        much larger than what shows of it, so it isn't noted."""
        self.plain(tag)
        if not self.clipped:
            self.surfaces[-1].add(tag)

    def blend(self, *parts):
        if not self.blending:
            self.parts.append('<g class="m">')
            self.blending = True
        self.parts += parts

    def is_far_face(self, tag):
        """Whether the pale shape `tag` is the far face of an arête. It covers much of the
        figure, unlike a finger behind the hand or the pelican's bill in the same greys."""
        points = points_on(tag)
        if not points:
            return False
        xs, ys = zip(*points)
        size = (max(xs) - min(xs)) * (max(ys) - min(ys)) * self.surfaces[-1].scale ** 2
        return size >= FAR_FACE_SHARE * self.area

    def is_detail(self, tag):
        """Whether all of the black mark `tag` lies on a body or the outline around it."""
        points = points_on(tag)
        return bool(points) and all(self.surfaces[-1].on_body(x, y) for x, y in points)

    def stop_blending(self):
        if self.blending:
            self.parts.append("</g>")
            self.blending = False
        self.parts += self.details
        self.details = []

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
            self.draw(with_attr(tag, "fill", PAGE))
        elif fill == "none" and stroke == XRAY_LINE and attr(tag, "stroke-dasharray") is not None:
            self.plain(tag)
        elif fill == CAST_SHADOW and path in self.shadows and not self.clipped:
            self.draw(with_attr(tag, "fill", SHADOW))
        elif fill in FAR_FACES and stroke is None and not self.clipped and self.is_far_face(tag):
            self.draw(with_attr(tag, "fill", FAR_FACE))
        elif fill == FAR_FACE_DOTS and tag.startswith("<circle"):
            self.draw(with_attr(tag, "fill", FAR_FACE_LIGHT))
        elif coloured(fill):
            self.holds.add(path)
            self.draw(tag)
        elif fill == "none" and path and (path in self.holds or path in self.outlines):
            self.draw(tag)
        elif (fill in BLACK or (fill == "none" and stroke in BLACK)) and self.is_detail(tag):
            self.details.append(tag)
        elif fill in BLACK:
            tag = with_attr(tag, "stroke", LIGHT_ON_DARK) if stroke in BLACK else tag
            self.blend(with_attr(tag, "fill", LIGHT_ON_DARK))
        elif fill == "#262626":
            self.draw(with_attr(tag, "fill", SHOE))
        elif fill == "none" and stroke in BLACK:
            self.blend(with_attr(tag, "stroke", LIGHT_ON_DARK))
        elif fill == "#b0b0b0":
            self.draw(with_attr(tag, "fill", DOTS))
        elif fill == "#ececec" and stroke is None:
            self.draw(with_attr(tag, "fill", WALL))
        elif fill == WHITE and tag.startswith("<rect"):
            self.draw(with_attr(tag, "fill", PAGE))
        else:
            self.draw(tag)

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
        if not path:
            self.frames.add(attr(tokens[i], "id"))
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
    tokens = TOKEN.findall(svg)
    shapes = [t for t in tokens if SHAPE.fullmatch(t)]
    box = VIEW_BOX.search(svg)
    area = float(box[1]) * float(box[2]) if box else float("inf")
    copy = DarkCopy(limb_outlines(shapes), cast_shadows(shapes), area)
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
        elif GROUP.match(token):
            copy.group(token)
        elif token.startswith("<stop") and attr(token, "stop-color") in EDGE_STOPS:
            copy.plain(with_attr(token, "stop-color", EDGE_STOPS[attr(token, "stop-color")]))
        elif token.startswith("<") or token.strip():
            copy.plain(token)
        else:
            copy.parts.append(token)
        i += 1
    copy.stop_blending()
    return re.sub(r"(<svg\b[^>]*>)", lambda m: m.group(1) + STYLE, "".join(copy.parts), count=1)
