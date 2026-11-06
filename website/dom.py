"""A small DOM over html.parser: enough to rearrange what Typst writes and to
build the pages around it, with nothing outside the standard library."""
from html import escape
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# Elements that start on a new line in the output, so the pages can be read.
BLOCK = {
    "address", "article", "aside", "body", "dd", "details", "dialog", "div", "dl", "dt", "figcaption", "figure",
    "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hr", "html", "li", "link", "main",
    "meta", "nav", "ol", "p", "script", "section", "summary", "table", "tbody", "td", "th", "thead", "title",
    "tr", "ul",
}


class Node:
    """An element. Its children are Nodes and plain strings of text."""

    def __init__(self, tag, attrs=None, *children):
        self.tag = tag
        self.attrs = dict(attrs or {})
        self.children = []
        self.parent = None
        self.append(*children)

    def append(self, *items):
        for item in items:
            if item is None:
                continue
            if isinstance(item, (list, tuple)):
                self.append(*item)
                continue
            if isinstance(item, Node):
                item.detach()
                item.parent = self
            self.children.append(item)
        return self

    def set_children(self, items):
        """Replace the children with `items`, which may include some of them."""
        for child in self.children:
            if isinstance(child, Node):
                child.parent = None
        self.children = []
        self.append(*items)

    def insert(self, index, item):
        if isinstance(item, Node):
            item.detach()
            item.parent = self
        self.children.insert(index, item)

    def detach(self):
        if self.parent is not None:
            self.parent.children.remove(self)
            self.parent = None
        return self

    def replace_with(self, *items):
        """Put `items` where this element is, and take it out."""
        parent = self.parent
        index = next(i for i, c in enumerate(parent.children) if c is self)
        self.parent = None
        del parent.children[index]
        for offset, item in enumerate(items):
            parent.insert(index + offset, item)

    def unwrap(self):
        """Put this element's children where it is."""
        self.replace_with(*list(self.children))

    def walk(self):
        """This element and every element in it, in document order. The list is
        made up front, so the tree can change during the loop."""
        out = [self]
        for child in self.children:
            if isinstance(child, Node):
                out += child.walk()
        return out

    def select(self, *tags, cls=None):
        """Elements in this one (and itself) with one of `tags`, and with class
        `cls` if given."""
        return [n for n in self.walk()
                if (not tags or n.tag in tags) and (cls is None or n.has_class(cls))]

    def first(self, *tags, cls=None):
        found = self.select(*tags, cls=cls)
        return found[0] if found else None

    @property
    def classes(self):
        return self.attrs.get("class", "").split()

    def has_class(self, name):
        return name in self.classes

    def add_class(self, *names):
        self.attrs["class"] = " ".join(self.classes + [n for n in names if n not in self.classes])

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def reading_text(self):
        """The text, with a space where one block of it ends and the next begins."""
        out = []
        for c in self.children:
            if isinstance(c, str):
                out.append(c)
            elif c.tag == "br" or c.tag in BLOCK:
                out.append(f" {c.reading_text()} ")
            else:
                out.append(c.reading_text())
        return "".join(out)

    def next_element(self):
        siblings = self.parent.children
        index = next(i for i, c in enumerate(siblings) if c is self)
        return next((c for c in siblings[index + 1:] if isinstance(c, Node)), None)

    def clone(self):
        copy = Node(self.tag, self.attrs)
        for child in self.children:
            copy.append(child.clone() if isinstance(child, Node) else child)
        return copy

    def __str__(self):
        if self.tag == "#fragment":
            return "".join(str(c) if isinstance(c, Node) else escape(c, quote=False) for c in self.children)
        attrs = "".join(f' {k}="{escape(str(v))}"' for k, v in self.attrs.items())
        start = f"\n<{self.tag}{attrs}>" if self.tag in BLOCK else f"<{self.tag}{attrs}>"
        if self.tag in VOID:
            return start
        if self.tag in ("script", "style"):  # their text isn't escaped
            return f"{start}{''.join(self.children)}</{self.tag}>"
        inner = "".join(str(c) if isinstance(c, Node) else escape(c, quote=False) for c in self.children)
        return f"{start}{inner}</{self.tag}>"


def el(tag, attrs=None, *children):
    return Node(tag, attrs, *children)


def fragment(*children):
    return Node("#fragment", None, *children)


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#fragment")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: "" if v is None else v for k, v in attrs})
        self.stack[-1].append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].append(data)


def parse(html):
    parser = _Parser()
    parser.feed(html)
    parser.close()
    return parser.root
