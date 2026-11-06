"""Turn the one long HTML file Typst writes into the book's website.

The file follows the book from title page to index. `Book.split` cuts it where
print starts a new page for a unit of the book: a part, a chapter, a grade guide
and a technique entry. The passes after it work across those pages, for what can
only be known from the whole book: where a reference lands, what refers to an
entry, the tables, the A–Z list and the index. All links inside the site are
written from the root ("/glossary/#gl-beta") until a page is written out, when
render.py makes them relative, so the site can live in any folder of any host.
"""
import json
import re
import shutil
import tomllib
import unicodedata
from collections import defaultdict

import dark
import render
from dom import Node, el, fragment, parse

GRADE_TOKEN = re.compile(r"\bV\d+|\b\d[ABC]\b")
CHAPTER_MENTION = re.compile(r"\b(Chapter) (\d+)\b|\b(Part) (IV|V?I{0,3})\b(?=[\s,.:;)]|$)")
PAGE_IN_LINK = re.compile(r"\s*\(p\.[\s ]*\d+\)")
# Words that mean the text still talks about print.
PRINT_WORDS = re.compile(r"\bPDF\b|\be-reader\b|\bQR\b|\bscan\b|\bpage numbers?\b|\bpp?\.[\s ]*\d|\bbookmarks?\b|"
                         r"\btitle page\b|\bheader of\b", re.I)
# The width above which a figure goes below the steps instead of beside them. In
# print it is 92 mm of 150 mm, but a screen needs a wider column for the steps.
BESIDE_MM = 66
PX_PER_MM = 4.8  # the column is 150 mm wide in print and 720 px here
SERIF = "'Iowan Old Style', Charter, 'Palatino Linotype', 'URW Palladio L', P052, Georgia, serif"


def clean(text):
    """A heading or name as plain text on one line."""
    return re.sub(r"\s+", " ", text.replace("⁠", "").replace(" ", " ")).strip()


def slug(text):
    text = unicodedata.normalize("NFKD", text.replace("–", "-")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def fold(text):
    """A sort key that ignores case and accents, like the index in print."""
    text = unicodedata.normalize("NFKD", text.replace("ß", "ss"))
    return "".join(c for c in text if not unicodedata.combining(c)).lower().replace("–", "-")


def dark_name(name):
    """Where a figure's dark copy goes: figures/edging.dark.svg."""
    return name.removesuffix(".svg") + ".dark.svg"


def roman(numeral):
    """The value of a roman numeral."""
    values = dict(i=1, v=5, x=10)
    digits = [values[c] for c in numeral]
    return sum(-d if later > d else d for d, later in zip(digits, digits[1:] + [0]))


def shorten(text, limit=158):
    text = clean(text)
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"


class Page:
    """One page of the site, and what the passes need to know about it."""

    def __init__(self, path, title, kind, parent=None):
        self.path = path            # from the site's root, with a final slash: "techniques/edging/"
        self.title = title
        self.kind = kind            # home, front, part, chapter, appendix, guide, entry
        self.parent = parent        # the page above it in the book's outline
        self.body = fragment()
        self.heading = None         # the head of a chapter or guide
        self.number = ""            # "3", or "8.6" for a guide
        self.short = title          # a guide's name without its Font grades
        self.word = ""              # "Three"
        self.ornament = ""
        self.subtitle = ""          # of a part
        self.description = ""
        self.sections = []          # the outline below it: see `Section`
        self.chapters = []          # of a part
        self.meta = {}              # of an entry: grade, category, aliases
        self.prev = None
        self.next = None

    @property
    def url(self):
        return "/" + self.path


class Section:
    """A section of a chapter in the outline: its entries, or the grade guide it is."""

    def __init__(self, title, number="", heading=None, guide=None):
        self.title, self.number, self.heading, self.guide = title, number, heading, guide
        self.entries = []

    @property
    def id(self):
        return self.heading.attrs.get("id") if self.heading is not None else None


class Book:
    def __init__(self, html, work, out, stamp, base_url, here):
        self.doc = parse(html)
        self.work, self.out, self.stamp, self.base_url, self.here = work, out, stamp, base_url, here
        self.pages = []
        self.parts = []
        self.reading = []          # every page a reader goes through, in print's order
        self.entries = {}          # by key
        self.guides = {}           # by label
        self.chapters = {}         # by number
        self.targets = {}          # an id in the book -> the page it ended up on
        self.front = []            # the title page and its back
        self.key_alias = {}
        self.categories = {}
        self.tab_looks = []
        self.warnings = []
        self.errors = []
        self.assets = set()
        self.ix = defaultdict(list)
        self.backlinks = defaultdict(list)
        self.cited_in = defaultdict(list)
        self.previews = {}
        self.search = []
        title = self.doc.first("title")
        self.title = title.text() if title else "The book"
        self.alts = self.read_alts()

    def read_alts(self):
        """The drawings' descriptions by file name, from book/figure-alt.toml if this
        edition has one."""
        path = self.work / "book" / "figure-alt.toml"
        if not path.exists():
            return {}
        return {name: entry["alt"] for name, entry in tomllib.loads(path.read_text()).items()}

    def warn(self, message):
        self.warnings.append(message)
        print("warning: " + message)

    def has_page(self, path):
        return path in ("contents/", "colophon/") or any(p.path == path for p in self.pages)

    def read_title_page(self):
        """Note the words the site reuses from the title page: the line above the
        title, the line below it and the editor's name."""
        self.strap = self.tagline = self.editor = ""
        self.title_lines = [self.title]
        if not self.front:
            return
        marked = [clean(n.text()) for n in self.front[0].select(cls="sc")]
        lines = self.front[0].select("div")
        self.strap = marked[0].capitalize() if marked else ""
        self.tagline = clean(lines[-1].reading_text()) if len(lines) > 1 else ""
        if lines:
            self.title_lines = [clean(c) for c in lines[0].children if isinstance(c, str) and c.strip()]
        self.editor = next((t.removeprefix("Edited by ") for t in marked if t.startswith("Edited by ")), "")

    def add(self, page):
        self.pages.append(page)
        return page

    # ------------------------------------------------------------ splitting

    def split(self):
        body = self.doc.first("body")
        nodes = [n for n in body.children if isinstance(n, Node) or n.strip()]
        current = part = chapter = section = entry_list = None
        waiting = []  # what leads into the next entry
        for i, node in enumerate(nodes):
            if isinstance(node, str):
                if current:
                    current.body.append(node)
                continue
            gen = node.attrs.get("data-gen")
            if gen == "book-data":
                self.key_alias = json.loads(node.attrs["data-key-alias"])
                self.categories = json.loads(node.attrs["data-categories"])
                self.tab_looks = json.loads(node.attrs["data-tab-looks"])
            elif node.tag == "section" and node.has_class("front-page"):
                self.front.append(node)
            elif node.tag == "section" and node.has_class("part"):
                part = self.add_part(node)
                current, chapter, section = part, None, None
            elif node.tag == "h2":
                chapter = self.add_chapter(node, part)
                current, section, entry_list = chapter, None, None
            elif node.tag == "h3" and node.attrs.get("id", "").startswith("grade"):
                current = self.add_guide(node, chapter)
                section = None
            elif node.tag == "h3":
                current = chapter
                section = Section(clean(node.text()), node.attrs.get("data-num", ""), heading=node)
                chapter.sections.append(section)
                entry_list = None
                chapter.body.append(node)
            elif node.tag == "article" and node.has_class("entry"):
                current = self.add_entry(node, chapter, section, waiting)
                waiting = []
                if entry_list is None:
                    entry_list = el("ul", {"class": "entry-list"})
                    chapter.body.append(entry_list)
                entry_list.append(el("li", {"data-entry": current.meta["key"]}))
            elif self.leads_into_entry(nodes, i):
                waiting.append(node)
            elif current is None:
                self.warn(f"text before the first heading: {node.text()[:60]!r}")
            else:
                current.body.append(node)

    @staticmethod
    def leads_into_entry(nodes, i):
        """Between entries a film strip opens the page of the entry after it, and any
        marks between them go with it."""
        def goes_along(node):
            return node.tag == "span" or (node.tag == "figure" and node.has_class("filmstrip"))

        if not goes_along(nodes[i]):
            return False
        for later in nodes[i + 1:]:
            if isinstance(later, str):
                return False
            if later.tag == "article" and later.has_class("entry"):
                return True
            if not goes_along(later):
                return False
        return False

    def add_part(self, node):
        title = node.attrs["data-title"]
        m = re.fullmatch(r"part-([ivx]+)", slug(title))
        path = f"part-{roman(m.group(1))}" if m else slug(title)
        page = self.add(Page(path + "/", title, "part"))
        page.subtitle = node.attrs.get("data-subtitle", "")
        page.ornament = node.attrs.get("data-ornament", "")
        page.description = page.subtitle or f"{title} of {self.title}"
        self.parts.append(page)
        return page

    def add_chapter(self, node, part):
        label = node.attrs.get("id")
        title = clean(node.text())
        page = self.add(Page((label or slug(title)) + "/", title, "chapter" if node.attrs.get("data-num") else "appendix", part))
        page.heading = node
        page.number = node.attrs.get("data-num", "")
        page.word = node.attrs.get("data-word", "")
        page.ornament = node.attrs.get("data-ornament", "")
        if page.number:
            self.chapters[page.number] = page
        if part:
            part.chapters.append(page)
        else:
            page.kind = "front"
        self.reading.append(page)
        if label:
            self.targets[label] = page
        return page

    def add_guide(self, node, chapter):
        title = clean(node.text())
        label = node.attrs["id"]
        page = self.add(Page(f"grades/{slug(title.split(' (')[0])}/", title, "guide", chapter))
        page.heading = node
        page.number = node.attrs.get("data-num", "")
        page.short = title.split(" (")[0]
        self.guides[label] = page
        self.targets[label] = page
        chapter.sections.append(Section(title, page.number, guide=page))
        self.reading.append(page)
        return page

    def add_entry(self, node, chapter, section, waiting):
        key = node.attrs["data-key"]
        page = self.add(Page(f"techniques/{key}/", node.attrs["data-name"], "entry", chapter))
        page.meta = dict(
            key=key, grade=int(node.attrs["data-grade"]), category=node.attrs["data-category"],
            aliases=[a for a in node.attrs["data-aliases"].split("|") if a],
            category_name=node.attrs["data-category-name"],
        )
        for name in ("data-key", "data-name", "data-grade", "data-category", "data-aliases", "data-category-name"):
            del node.attrs[name]
        page.body.append(node)
        # A film strip goes under the entry's head, so that the page opens with it.
        for item in waiting:
            if item.tag == "figure":
                head_end = next((c for c in node.children if isinstance(c, Node) and c.has_class("how")), None)
                index = node.children.index(head_end) if head_end else len(node.children)
                node.insert(index, item)
            else:
                node.insert(0, item)
        self.entries[key] = page
        if section is None:
            section = Section("")
            chapter.sections.append(section)
        section.entries.append(page)
        self.reading.append(page)
        return page

    # ------------------------------------------------------------ marks

    def register_targets(self):
        """Note which page every id the book links to ended up on."""
        for page in self.pages:
            for node in page.body.walk():
                if "id" in node.attrs and node.attrs["id"] not in self.targets:
                    self.targets[node.attrs["id"]] = page
        for key, page in self.entries.items():
            self.targets[f"tech-{key}"] = page
            self.targets[f"tech-meta-{key}"] = page

    def walk_with_heading(self, page):
        """The page's elements in order, each with the heading it falls under: the
        label print gives a backlink."""
        heading = page.title
        for node in page.body.walk():
            if node.tag in ("h2", "h3", "h4"):
                heading = clean(node.text())
            yield node, heading

    def resolve_references(self):
        """Fill in technique references and collect what refers to what."""
        counter = 0
        for page in self.pages:
            seen = set()
            for node, heading in self.walk_with_heading(page):
                if node.tag != "a" or not node.has_class("tref"):
                    continue
                key = node.attrs.pop("data-key")
                named = node.attrs.pop("data-named")
                real = key if key in self.entries else self.key_alias.get(key, key)
                target = self.entries.get(real)
                if target is None:
                    self.warn(f"{page.path}: no entry for the technique key {key!r}")
                    node.unwrap()
                    continue
                if named == "0":
                    node.children = [target.title]
                node.attrs["href"] = f"#tech-{real}"
                if target is not page and (real, heading) not in seen:
                    seen.add((real, heading))
                    counter += 1
                    node.attrs["id"] = f"ref-{counter}"
                    self.backlinks[real].append((page, heading, node.attrs["id"]))

    def resolve_marks(self):
        """Give every index mark an id and file it under its term."""
        counter = 0
        for page in self.pages:
            for node, heading in self.walk_with_heading(page):
                term = node.attrs.get("data-ix")
                if term is None:
                    continue
                counter += 1
                main = node.attrs["data-main"] == "1"
                node.attrs = {"id": f"ix-{counter}"}
                self.ix[term].append(dict(page=page, id=node.attrs["id"], main=main, label=heading))
        for page in self.pages:
            for p in page.body.select("p"):
                self.lift_lone_marks(p)

    @staticmethod
    def lift_lone_marks(p):
        """A paragraph with nothing but marks in it isn't a paragraph. Its marks
        move into the next block."""
        if p.text().strip() or any(isinstance(c, Node) and c.tag != "span" for c in p.children):
            return
        marks = [c for c in p.children if isinstance(c, Node)]
        after = p.next_element()
        while after is not None and after.tag in ("ul", "ol"):
            after = next((c for c in after.children if isinstance(c, Node)), None)
        if after is not None and after.tag in ("p", "li", "dd"):
            for mark in reversed(marks):
                after.insert(0, mark)
            p.detach()
        else:
            p.replace_with(*marks)

    # ------------------------------------------------------------ sources

    def wrap_citations(self):
        """Typst writes a citation as text and links side by side: "[", a link,
        ", ", a link, "]". Wrapping them lets the page set them as one small unit."""
        for page in self.pages:
            for parent in page.body.walk():
                if any(isinstance(c, Node) and c.attrs.get("role") == "doc-biblioref" for c in parent.children):
                    self.wrap_in(parent)

    @staticmethod
    def wrap_in(parent):
        out, kids, i = [], list(parent.children), 0
        while i < len(kids):
            kid = kids[i]
            opens = isinstance(kid, Node) and kid.tag == "span" and kid.text() == "["
            opens = opens or (isinstance(kid, str) and kid.endswith("[") and i + 1 < len(kids)
                              and isinstance(kids[i + 1], Node) and kids[i + 1].attrs.get("role") == "doc-biblioref")
            if not opens:
                out.append(kid)
                i += 1
                continue
            if isinstance(kid, str) and kid[:-1]:
                out.append(kid[:-1])
            group = el("span", {"class": "cite"}, "[")
            i += 1
            while i < len(kids):
                part = kids[i]
                if isinstance(part, str) and part.startswith("]"):
                    group.append("]")
                    out.append(group)
                    # What follows the bracket may open the next citation.
                    if part[1:]:
                        kids[i] = part[1:]
                    else:
                        i += 1
                    break
                group.append(part)
                i += 1
            else:
                out.append(group)
        parent.set_children(out)

    def rebuild_sources(self):
        """Give the sources readable ids and list where each one is cited."""
        found = [(n, page) for page in self.pages for n in page.body.walk() if n.attrs.get("role") == "doc-bibliography"]
        if not found:
            self.warn("found no bibliography")
            return
        bib, sources_page = found[0]
        new_ids = {}
        items = bib.select("li")
        for n, li in enumerate(items, 1):
            new_ids[li.attrs["id"]] = f"source-{n}"
            prefix = li.first("span", cls="prefix")
            if prefix:
                prefix.detach()
            li.attrs = {"id": f"source-{n}"}
            first = li.children[0] if li.children else None
            if isinstance(first, str):
                li.children[0] = first.lstrip()
        counter = 0
        for page in self.pages:
            seen = set()
            for node, heading in self.walk_with_heading(page):
                if not node.has_class("cite"):
                    continue
                for a in node.select("a"):
                    old = a.attrs["href"].lstrip("#")
                    new = new_ids.get(old)
                    if new is None:
                        continue
                    a.attrs["href"] = "#" + new
                    self.targets[new] = sources_page
                    if (new, heading) not in seen:
                        seen.add((new, heading))
                        if "id" not in node.attrs:
                            counter += 1
                            node.attrs["id"] = f"cite-{counter}"
                        self.cited_in[new].append((page, heading, node.attrs["id"]))
        for li in items:
            uses_here = self.cited_in.get(li.attrs["id"], [])
            if uses_here:
                links = []
                for page, heading, anchor in uses_here:
                    links += [el("a", {"href": f"{page.url}#{anchor}"}, heading), ", "]
                li.append(el("span", {"class": "cited-in"}, "Cited in ", links[:-1], "."))
        section = el("section", {"role": "doc-bibliography"}, el("ol", {"class": "sources"}, items))
        columns = bib.parent if bib.parent.has_class("columns") else bib
        columns.replace_with(section)

    # ------------------------------------------------------------ generated matter

    def grade_label(self, grade):
        return "VB" if grade < 0 else "V8+" if grade >= 8 else f"V{grade}"

    def grade_class(self, entry):
        return f'g{max(entry.meta["grade"], 0)}' if self.tab_looks else ""

    def grade_tag(self, grade):
        return el("span", {"class": "grade-plain"}, self.grade_label(grade))

    def tech_link(self, page, text=None):
        return el("a", {"class": "tref-plain", "href": page.url}, text or page.title)

    def table(self, heads, rows, caption=None):
        return el("table", {"class": "gen-table"},
                  el("caption", {"class": "visually-hidden"}, caption) if caption else None,
                  el("thead", None, el("tr", None, [el("th", {"scope": "col"}, h) for h in heads])),
                  el("tbody", None, [el("tr", None, [el("td", None, c) for c in row]) for row in rows]))

    def fill_generated(self):
        for page in self.pages:
            for node in page.body.select("div"):
                gen = node.attrs.get("data-gen")
                if gen == "category-table":
                    self.category_table(node)
                elif gen == "grade-techniques":
                    self.grade_techniques(node)
                elif gen == "a-to-z":
                    node.replace_with(self.a_to_z())
                elif gen == "index":
                    node.replace_with(self.index())
                elif gen == "contents":
                    node.detach()

    def category_table(self, node):
        """Ranked by grade in two columns; within a grade, in the chapter's order."""
        category = node.attrs.pop("data-category")
        del node.attrs["data-gen"]
        rows = sorted((p for p in self.entries.values() if p.meta["category"] == category), key=lambda p: p.meta["grade"])
        half = (len(rows) + 1) // 2
        node.attrs["class"] = "two-tables"
        for chunk in (rows[:half], rows[half:]):
            if chunk:
                node.append(self.table(["Grade", "Technique"], [[self.grade_tag(p.meta["grade"]), self.tech_link(p)] for p in chunk],
                                       f"Techniques by grade: {self.categories.get(category, category)}"))

    def grade_techniques(self, node):
        grade = int(node.attrs["data-grade"])
        rows = [p for p in self.entries.values() if (p.meta["grade"] >= 8 if grade >= 8 else p.meta["grade"] == grade)]
        rows.sort(key=lambda p: p.meta["category"])
        if not rows:
            node.replace_with(el("p", None, el("em", None, "None listed.")))
            return
        node.replace_with(self.table(["Technique", "Category"], [[self.tech_link(p), el("em", None, p.meta["category_name"])] for p in rows]))

    @staticmethod
    def alpha_nav(anchors):
        """A bar of letters, from {letter: id}."""
        return el("nav", {"class": "alpha", "aria-label": "Jump to a letter"},
                  [el("a", {"href": f"#{anchor}"}, letter) for letter, anchor in anchors.items()])

    def letter_of(self, text):
        return fold(text)[0].upper() if fold(text)[:1].isalpha() else "#"

    def a_to_z(self):
        rows = []
        for page in self.entries.values():
            rows.append(dict(sort=fold(page.title), name=page.title, see=None, page=page))
            for alias in page.meta["aliases"]:
                rows.append(dict(sort=fold(alias), name=alias, see=page.title, page=page))
        rows.sort(key=lambda r: r["sort"])
        groups = defaultdict(list)
        for row in rows:
            groups[self.letter_of(row["sort"])].append(row)
        out = fragment(self.alpha_nav({l: f"az-{slug(l) or 'other'}" for l in groups}))
        wrap = el("div", {"class": "az"})
        for letter, group in groups.items():
            items = []
            for r in group:
                label = [el("strong", None, r["name"])] if r["see"] is None else [r["name"], " → ", el("em", None, r["see"])]
                items.append(el("li", None,
                                el("a", {"class": "tref-plain", "href": r["page"].url}, label),
                                el("span", {"class": "leader", "aria-hidden": "true"}),
                                self.grade_tag(r["page"].meta["grade"]) if r["see"] is None else None))
            wrap.append(el("section", {"class": "letter"},
                           el("h6", {"class": "letter-head", "id": f"az-{slug(letter) or 'other'}"}, letter),
                           el("ul", None, items)))
        out.append(wrap)
        return out

    def index(self):
        """The same grouping as make-index in the print template: terms that differ
        only in case share one entry, with the capitalised spelling, and sub-entries
        ("Main!sub") go under their head."""
        groups, shown = defaultdict(list), {}
        for term, records in self.ix.items():
            key = term.lower()
            groups[key] += records
            if key not in shown or term[0] != term[0].lower():
                shown[key] = term
        keys = sorted(groups, key=lambda k: fold(k).replace("!", "\x01"))
        heads = {}
        for key in keys:
            head = shown[key].split("!")[0]
            if head.lower() not in heads or head[0] != head[0].lower():
                heads[head.lower()] = head
        letters = defaultdict(list)
        for key in keys:
            head = heads[shown[key].split("!")[0].lower()]
            letters[self.letter_of(head)].append(key)
        out = fragment(self.alpha_nav({l: f"ix-{slug(l) or 'other'}" for l in letters}))
        wrap = el("section", {"class": "ix-list", "role": "doc-index"})
        for letter, members in letters.items():
            ul = el("ul")
            section = el("section", {"class": "letter"},
                         el("h6", {"class": "letter-head", "id": f"ix-{slug(letter) or 'other'}"}, letter), ul)
            last_head, sublist = None, None
            for key in members:
                parts = shown[key].split("!")
                head = heads[parts[0].lower()]
                links = self.ix_links(groups[key])
                if len(parts) == 1:
                    item = el("li", None, self.ix_label(head), " ", links)
                    ul.append(item)
                    last_head, sublist = head.lower(), item
                else:
                    if head.lower() != last_head:
                        sublist = el("li", None, head)
                        ul.append(sublist)
                        last_head = head.lower()
                    sub = sublist.first("ul")
                    if sub is None:
                        sub = el("ul")
                        sublist.append(sub)
                    sub.append(el("li", None, parts[1], " ", links))
            wrap.append(section)
        out.append(wrap)
        return out

    @staticmethod
    def ix_label(term):
        m = re.match(r"^(.*) \(see (.*)\)$", term)
        return [m.group(1), " ", el("em", None, f"(see {m.group(2)})")] if m else term

    def ix_links(self, records):
        """One link per section, the defining one first and in bold."""
        seen, out = {}, []
        for r in records:
            key = (r["page"].path, r["label"])
            if key not in seen or r["main"]:
                seen[key] = r
        ordered = sorted(seen.values(), key=lambda r: not r["main"])
        for r in ordered:
            at_top = r["main"] and r["page"].kind == "entry"
            href = r["page"].url if at_top else f"{r['page'].url}#{r['id']}"
            link = el("a", {"href": href}, r["label"])
            out += [el("strong", None, link) if r["main"] else link, ", "]
        return el("span", {"class": "ix-refs"}, out[:-1])

    def fill_entry_lists(self):
        """Under each section of a chapter, the entries that follow in print."""
        for page in self.pages:
            for li in page.body.select("li"):
                key = li.attrs.pop("data-entry", None)
                if key is None:
                    continue
                entry = self.entries[key]
                li.append(el("a", {"class": "entry-link", "href": entry.url}, entry.title),
                          " ", self.grade_tag(entry.meta["grade"]),
                          el("p", None, self.plain_summary(entry)))

    def fill_backlinks(self):
        for key, entry in self.entries.items():
            links = self.backlinks.get(key)
            dl = entry.body.first("dl", cls="apparatus")
            if dl is None:
                continue
            if links:
                items = []
                for page, heading, anchor in links:
                    items += [el("a", {"href": f"{page.url}#{anchor}"}, heading), ", "]
                dl.append(el("dt", None, "Referenced from"), el("dd", None, items[:-1]))
            if not dl.children:
                dl.detach()

    def plain_summary(self, entry):
        """The entry's summary without its citations."""
        summary = entry.body.first("p", cls="summary")
        if summary is None:
            return ""
        return self.flat(summary)

    # ------------------------------------------------------------ markup

    def tidy_markup(self):
        for page in self.pages:
            self.tidy_page(page)

    def tidy_page(self, page):
        for node in page.body.select("div"):
            first = next((c for c in node.children if isinstance(c, Node)), None)
            if not node.attrs and first is not None and first.has_class("label") and first.tag == "span":
                # A subhead built from a label ("Step 1 ...") is a heading.
                node.tag = "h6"
                node.attrs = {"class": "step"}
            elif not node.attrs and not any(isinstance(c, Node) and c.tag in ("p", "ul", "ol", "table", "div", "figure") for c in node.children):
                node.tag = "p"
            elif not node.attrs:
                # A macro of the print template that website/template.typ doesn't
                # redefine keeps its content but loses its look.
                self.warn(f"{page.path}: this block has no web styling, so a macro may need adding to "
                          f"website/template.typ: {clean(node.text())[:60]!r}")
        for ul in page.body.select("ul", "ol"):
            ul.attrs.pop("style", None)
        for node, heading in self.walk_with_heading(page):
            if node.tag == "table":
                self.tidy_table(node, heading)
        for node in page.body.select("div", cls="columns"):
            if node.first("div", cls="gloss"):
                self.make_glossary(node)
            else:
                node.add_class(f"columns-{node.attrs.pop('data-count', '2')}")
        for node in page.body.walk():
            if "data-unknown-field" in node.attrs:
                self.warn(f"{page.path}: this edition's entries have a field website/template.typ doesn't know: "
                          f"{node.attrs.pop('data-unknown-field')}")
            if node.attrs.get("style") and node.tag != "svg":
                del node.attrs["style"]

    @staticmethod
    def tidy_table(table, heading):
        heads = [th.text().strip() for th in table.select("th")]
        table.insert(0, el("caption", {"class": "visually-hidden"}, heading))
        for th in table.select("th"):
            th.attrs.setdefault("scope", "col")
        # A table of three or more columns of text stacks on a phone, so its cells
        # say which column they belong to.
        if len(heads) >= 3 and not table.has_class("gen-table"):
            table.add_class("stacks")
            for row in table.select("tr"):
                cells = [c for c in row.children if isinstance(c, Node) and c.tag == "td"]
                for head, cell in zip(heads, cells):
                    cell.attrs["data-label"] = head
        if table.parent.tag != "div" or not table.parent.has_class("table-wrap"):
            wrapper = el("div", {"class": "table-wrap"})
            table.replace_with(wrapper)
            wrapper.append(table)

    def make_glossary(self, columns):
        """The glossary entries as a definition list, with a letter bar."""
        entries = columns.select("div", cls="gloss")
        letters = {}
        for entry in entries:
            letters.setdefault(self.letter_of(entry.first("dt").text()), entry.attrs["id"])
        dl = el("dl", {"class": "glossary"}, entries)
        columns.replace_with(self.alpha_nav(letters), el("section", {"role": "doc-glossary"}, dl))

    def apply_wording(self):
        """Replace the sentences that only make sense in print. Rules live in
        website/wording.json, and one that stops matching shows up in the report."""
        rules = json.loads((self.here / "wording.json").read_text())
        used = set()
        for page in self.pages:
            for node in page.body.walk():
                for i, child in enumerate(node.children):
                    if not isinstance(child, str):
                        continue
                    for n, rule in enumerate(rules):
                        if rule["find"] in child:
                            child = child.replace(rule["find"], rule["replace"])
                            used.add(n)
                    node.children[i] = child
                # A rule can remove a list item outright.
                if node.tag == "li" and not node.text().strip():
                    node.detach()
        for n, rule in enumerate(rules):
            if n not in used:
                print(f"note: wording.json: not found in this edition: {rule['find']!r}")

    def link_mentions(self):
        """Link the plain "Chapter 2" and "Part II" in the text, and set grades in
        lining figures as print does."""
        part_numbers = {p.title: p for p in self.parts}
        for page in self.pages:
            for node in page.body.walk():
                if node.tag in ("a", "h1", "h2", "h3", "h4", "h5", "h6", "dt", "th", "caption"):
                    continue
                if any(p.tag in ("a", "h1", "h2", "h3", "h4", "h5", "h6") for p in self.ancestors(node)):
                    continue
                out = []
                for child in node.children:
                    if not isinstance(child, str):
                        out.append(child)
                        continue
                    out += self.split_mentions(child, part_numbers)
                node.set_children(out)

    @staticmethod
    def ancestors(node):
        while node.parent is not None:
            node = node.parent
            yield node

    def split_mentions(self, text, part_numbers):
        out, last = [], 0
        for m in CHAPTER_MENTION.finditer(text):
            target = None
            if m.group(1):
                target = self.chapters.get(m.group(2))
            elif m.group(4):
                target = part_numbers.get(f"Part {m.group(4)}")
            if target is None:
                continue
            out.append(text[last:m.start()])
            out.append(el("a", {"class": "xref", "href": target.url}, m.group(0)))
            last = m.end()
        out.append(text[last:])
        return [t for t in out if t != ""]

    def set_lining_figures(self):
        roots = [root for page in self.pages for root in (page.body, page.heading) if root is not None]
        for root in roots:
            for node in root.walk():
                if node.has_class("lnum") or node.has_class("grade-tab") or node.has_class("grade-plain"):
                    continue
                out = []
                for child in node.children:
                    if not isinstance(child, str) or not GRADE_TOKEN.search(child):
                        out.append(child)
                        continue
                    last = 0
                    for m in GRADE_TOKEN.finditer(child):
                        out.append(child[last:m.start()])
                        out.append(el("span", {"class": "lnum"}, m.group(0)))
                        last = m.end()
                    out.append(child[last:])
                node.set_children([c for c in out if c != ""])

    def strip_page_numbers(self):
        """Print's "(p. 12)" has no meaning here. Only inside links: a page number
        elsewhere, as in the corrections, refers to a printed edition."""
        for page in self.pages:
            for a in page.body.select("a"):
                for i, child in enumerate(a.children):
                    if isinstance(child, str):
                        a.children[i] = PAGE_IN_LINK.sub("", child)

    # ------------------------------------------------------------ figures

    def source_file(self, src):
        name = re.sub(r"^(\.\./)+", "", src).lstrip("/")
        for base in ("book", ""):
            candidate = self.work / base / name
            if candidate.is_file():
                return candidate, name
        return None, name

    def size_images(self, body, page):
        """Point images at their place in the site and give them their size."""
        for img in body.select("img"):
            path, name = self.source_file(img.attrs["src"])
            if path is None:
                self.errors.append(f"{page.path}: no such image: {img.attrs['src']}")
                continue
            self.assets.add((path, name))
            img.attrs["src"] = "/" + name
            self.offer_dark_copy(img, name)
            size = self.svg_size(path)
            if size:
                img.attrs["width"], img.attrs["height"] = (str(round(v * PX_PER_MM)) for v in size)
            img.attrs["alt"] = img.attrs.get("alt") or self.alts.get(path.name, "")
            if not img.has_class("ornament") and not img.has_class("aside-icon"):
                img.attrs["loading"] = "lazy"
                img.attrs["decoding"] = "async"

    @staticmethod
    def offer_dark_copy(img, name):
        """Let the browser pick a figure's dark copy in dark mode. A printed page and
        a reader's forced colours both need the ordinary drawing."""
        if img.parent.tag == "picture" or not (name.startswith("figures/") and name.endswith(".svg")):
            return
        picture = el("picture")
        img.replace_with(picture)
        picture.append(el("source", {"media": "screen and (prefers-color-scheme: dark) and (forced-colors: none)",
                                     "srcset": "/" + dark_name(name)}), img)

    def lay_out_figures(self):
        for page in self.pages:
            self.size_images(page.body, page)
            for figure in page.body.select("figure"):
                img = figure.first("img")
                if img is None:
                    continue
                caption = figure.first("figcaption")
                if not caption and not img.attrs.get("alt"):
                    img.attrs["alt"] = f"Illustration: {page.title}"
                size = self.svg_size(self.source_file(img.attrs["src"])[0])
                if size and size[0] < BESIDE_MM and caption is not None and not figure.classes:
                    figure.add_class("narrow")
                link = el("a", {"class": "zoom", "href": img.attrs["src"]})
                # A described drawing names its own link. An aria-label would hide that.
                if not img.attrs["alt"]:
                    link.attrs["aria-label"] = "Open this drawing at full size"
                image = img.parent if img.parent.tag == "picture" else img
                image.replace_with(link)
                link.append(image)
            for how in page.body.select("section", cls="how"):
                self.lay_out_steps(how)

    def lay_out_steps(self, how):
        """A narrow figure goes beside its steps, a wider one below them."""
        figure = next((c for c in how.children if isinstance(c, Node) and c.has_class("entry-fig")), None)
        if figure is None:
            return
        wide = figure.attrs.pop("data-wide", "0") == "1"
        img = figure.first("img")
        size = self.svg_size(self.source_file(img.attrs["src"])[0]) if img is not None else None
        if wide or size is None or size[0] > BESIDE_MM:
            return
        steps = el("div", {"class": "steps"})
        for child in list(how.children):
            if child is not figure:
                if isinstance(child, Node):
                    child.detach()
                else:
                    how.children.remove(child)
                steps.append(child)
        how.insert(0, steps)
        how.add_class("beside")

    @staticmethod
    def svg_size(path):
        """An SVG's width and height in millimetres."""
        if path is None or path.suffix != ".svg":
            return None
        head = path.open(errors="ignore").read(2000)
        m = re.search(r'width="([\d.]+)mm"\s+height="([\d.]+)mm"', head)
        if m:
            return float(m.group(1)), float(m.group(2))
        # An image from outside the figures (the licence badge) has only a viewBox.
        m = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', head) or re.search(r'width="([\d.]+)"\s+height="([\d.]+)"', head)
        return (float(m.group(1)) / PX_PER_MM, float(m.group(2)) / PX_PER_MM) if m else None

    def copy_assets(self):
        for path, name in self.assets:
            target = self.out / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".svg":
                # Figures name one font. Other systems need something to fall back on.
                text = path.read_text().replace('font-family="Iowan Old Style"', f'font-family="{SERIF}"')
                target.write_text(text)
                if name.startswith("figures/"):
                    (self.out / dark_name(name)).write_text(dark.dark_copy(text))
            else:
                shutil.copy(path, target)

    # ------------------------------------------------------------ headings

    def number_headings(self):
        """Each page's headings start at h1 and skip no level. A class keeps what
        they looked like in the book, whatever level they end up at."""
        for page in self.pages:
            used = set()
            stack = [(2, 1)] if page.kind in ("chapter", "appendix", "front") else []
            if page.kind == "guide":
                stack = [(3, 1)]
            for node in page.body.walk():
                if not re.fullmatch(r"h[1-6]", node.tag) or node.has_class("letter-head"):
                    continue
                self.place_heading(node, stack, used)
            for node in page.body.select("h1", "h2", "h3", "h4", "h5", "h6", cls="letter-head"):
                node.tag = "h2"

    def place_heading(self, node, stack, used):
        level = int(node.tag[1])
        while stack and stack[-1][0] >= level:
            stack.pop()
        new = stack[-1][1] + 1 if stack else 1
        stack.append((level, new))
        look = {3: "sec", 4: "entry-name", 5: "sub"}.get(level)
        if look:
            node.add_class(look)
        node.tag = f"h{min(new, 6)}"
        number = node.attrs.pop("data-num", None)
        if number:
            node.insert(0, el("span", {"class": "num"}, number))
            node.insert(1, " ")
        if level != 4 and "id" not in node.attrs and not node.has_class("label"):
            base = slug(clean(node.text()).removeprefix(number or "")) or "section"
            anchor, n = base, 2
            while anchor in used:
                anchor, n = f"{base}-{n}", n + 1
            used.add(anchor)
            node.attrs["id"] = anchor

    # ------------------------------------------------------------ links

    def resolve_links(self, page):
        """Turn "#id" links into links from the root, and report the broken ones."""
        for a in page.body.select("a"):
            href = a.attrs.get("href", "")
            if not href.startswith("#"):
                continue
            anchor = href[1:]
            target = self.targets.get(anchor)
            if target is None:
                if anchor.startswith(("gl-", "grade-", "cattable-")):
                    # Print leaves these as plain text until their target exists.
                    a.unwrap()
                    continue
                self.errors.append(f"{page.path}: a link to #{anchor} goes nowhere")
                a.unwrap()
                continue
            is_head = anchor == f"tech-{target.meta.get('key')}" or anchor == f"tech-meta-{target.meta.get('key')}"
            is_head = is_head or (target.kind in ("chapter", "appendix", "front", "guide") and target.heading is not None
                                  and target.heading.attrs.get("id") == anchor)
            a.attrs["href"] = target.url if is_head else f"{target.url}#{anchor}"

    def fill_descriptions(self):
        for page in self.pages:
            if page.description:
                continue
            if page.kind == "entry":
                page.description = shorten(self.plain_summary(page))
            else:
                first = next((p for p in page.body.select("p") if clean(p.text())), None)
                page.description = shorten(self.flat(first)) if first is not None else page.title

    # ------------------------------------------------------------ previews and search

    def collect_previews(self):
        """What a link shows on hover: an entry's summary, a glossary definition, a
        source. Kept apart from the pages, and loaded only when first needed."""
        for key, page in self.entries.items():
            self.previews[page.path] = dict(t=page.title, g=self.grade_label(page.meta["grade"]) + "+", c=self.grade_class(page), h=self.plain_summary(page))
        for page in self.pages:
            for entry in page.body.select("div", cls="gloss"):
                dt, dd = entry.first("dt"), entry.first("dd")
                self.previews[f"{page.path}#{entry.attrs['id']}"] = dict(t=clean(dt.text()), h=self.flat(dd))
            for li in page.body.select("li"):
                if li.attrs.get("id", "").startswith("source-"):
                    copy = li.clone()
                    for cited in copy.select("span", cls="cited-in"):
                        cited.detach()
                    number = li.attrs["id"].removeprefix("source-")
                    self.previews[f"{page.path}#{li.attrs['id']}"] = dict(t=f"Source {number}", h=self.flat(copy))

    @staticmethod
    def flat(node):
        """The node's text, with no citations."""
        copy = node.clone()
        for cite in copy.select("span", cls="cite"):
            cite.detach()
        return re.sub(r"\s+([.,;:)])", r"\1", clean(copy.reading_text()))

    def collect_search(self):
        """One document per entry, guide, chapter section and glossary term."""
        for page in self.pages:
            trail = " › ".join(p.title for p in render.trail(page))
            if page.kind == "entry":
                self.search.append(dict(t=page.title, u=page.path, c=trail, g=self.grade_label(page.meta["grade"]) + "+", k=self.grade_class(page),
                                        a=" ".join(page.meta["aliases"]), b=self.flat_entry(page)))
            elif page.path == "glossary/":
                for entry in page.body.select("div", cls="gloss"):
                    self.search.append(dict(t=clean(entry.first("dt").text()), u=f"{page.path}#{entry.attrs['id']}", c="Glossary", b=self.flat(entry.first("dd"))))
            elif page.path in ("sources/", "index/", "a-to-z/") or page.kind == "part":
                continue
            elif page.kind == "chapter" or page.kind == "front":
                self.search_sections(page, trail)
            else:
                self.search.append(dict(t=page.title, u=page.path, c=trail, b=self.flat(page.body)))

    def flat_entry(self, page):
        copy = page.body.clone()
        for node in copy.select("dl", cls="apparatus") + copy.select("header", cls="entry-head"):
            node.detach()
        return self.flat(copy)

    def search_sections(self, page, trail):
        title, anchor, chunks = page.title, "", []
        def flush():
            text = clean(" ".join(chunks))
            if text:
                self.search.append(dict(t=title, u=f"{page.path}{'#' + anchor if anchor else ''}", c=f"{trail} › {page.title}" if anchor else trail, b=text))
        for child in page.body.children:
            if not isinstance(child, Node):
                continue
            if child.tag.startswith("h") and child.has_class("sec"):
                flush()
                title, anchor, chunks = clean(child.text()), child.attrs.get("id", ""), []
            elif not child.has_class("entry-list"):
                chunks.append(self.flat(child))
        flush()

    # ------------------------------------------------------------ the checks

    def check_print_words(self):
        """Report text that still talks about print, for wording.json."""
        for page in self.pages:
            # The corrections and sources are about the printed book, and the site
            # doesn't reword the editor's signed foreword.
            if page.path in ("corrections/", "sources/", "foreword/"):
                continue
            for node in page.body.select("p", "li", "td", "dd", "figcaption"):
                text = clean(node.text())
                if any(c.tag in ("p", "li") for c in node.children if isinstance(c, Node)):
                    continue
                m = PRINT_WORDS.search(text)
                if m:
                    start = max(m.start() - 50, 0)
                    self.warn(f"{page.path}: this may only make sense in print: …{text[start:m.end() + 40]}…")

    # ------------------------------------------------------------ the whole

    def set_reading_order(self):
        for before, after in zip(self.reading, self.reading[1:]):
            before.next, after.prev = after, before

    def build(self):
        self.split()
        self.read_title_page()
        self.register_targets()
        self.resolve_references()
        self.resolve_marks()
        self.wrap_citations()
        self.rebuild_sources()
        self.apply_wording()
        self.strip_page_numbers()
        self.tidy_markup()
        self.fill_generated()
        self.fill_entry_lists()
        self.fill_backlinks()
        self.link_mentions()
        self.set_lining_figures()
        self.lay_out_figures()
        self.number_headings()
        self.register_targets()
        for page in self.pages:
            self.resolve_links(page)
        self.fill_descriptions()
        self.set_reading_order()
        self.collect_previews()
        self.collect_search()
        self.check_print_words()
        return render.write_site(self)


def build(html, work, out, stamp, base_url, here):
    return Book(html, work, out, stamp, base_url, here).build()
