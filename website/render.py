"""Write the site: the pages around the book's text, and the files beside them."""
import json
import posixpath
import re
import shutil
import subprocess
from datetime import date
from html import escape, unescape

from dom import Node, el, fragment

REPO = "https://github.com/simongray/ReadingTheWall"
LICENCE = "https://creativecommons.org/licenses/by-sa/4.0/"
# The running head of every page in print, and of every page here.
QUICK_LINKS = (("Contents", "contents/"), ("A–Z", "a-to-z/"), ("Troubleshooting", "troubleshooting/"),
               ("Glossary", "glossary/"), ("Index", "index/"))
EDITION_WORDS = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth")


def trail(page):
    """The pages above this one, from the top of the book."""
    out = []
    while page.parent is not None:
        page = page.parent
        out.insert(0, page)
    return out


def chapter_of(page):
    for p in [page] + trail(page)[::-1]:
        if p.kind in ("chapter", "appendix", "front"):
            return p
    return None


def edition_label(stamp):
    if stamp["edition"] == "draft":
        return "Draft"
    n = int(stamp["edition"])
    word = EDITION_WORDS[n - 1] if n <= len(EDITION_WORDS) else f"{n}th"
    return f"{word} edition"


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def pdf_link(stamp):
    n = stamp["edition"]
    return f"{REPO}/releases/latest" if n == "draft" else f"{REPO}/releases/download/edition-{n}/Reading-the-Wall-edition-{n}.pdf"


def relative(target, page_path):
    """A link from the root as a link from this page. A directory's "./" keeps
    the link from reading as empty."""
    path, _, frag = target[1:].partition("#")
    if path == page_path and frag:
        return "#" + frag
    rel = posixpath.relpath(path or ".", page_path or ".")
    rel = "./" if rel == "." else rel + ("/" if path.endswith("/") or not path else "")
    return rel + ("#" + frag if frag else "")


def relativise(node, page_path):
    for n in node.walk():
        for attr in ("href", "src", "srcset"):
            value = n.attrs.get(attr)
            if value and value.startswith("/"):
                n.attrs[attr] = relative(value, page_path)


# ------------------------------------------------------------ around the text

def link_to(target, current, *text, **attrs):
    """A link to a page, marked when it is the page you are on."""
    attrs = {"href": target.url, **attrs}
    if target is current:
        attrs["aria-current"] = "page"
    return el("a", attrs, list(text) or target.title)


def outline(book, page):
    """The book's outline beside the text, the current chapter opened up."""
    here = chapter_of(page)
    ol = el("ol")
    for p in book.pages:
        if p.kind == "front":
            ol.append(el("li", None, link_to(p, page), chapter_sections(p, page) if p is here else None))
    for part in book.parts:
        chapters = el("ol")
        for ch in part.chapters:
            label = [el("span", {"class": "num"}, ch.number), " ", ch.title] if ch.number else [ch.title]
            chapters.append(el("li", None, link_to(ch, page, *label), chapter_sections(ch, page) if ch is here else None))
        ol.append(el("li", {"class": "o-part"}, link_to(part, page, part.title, **{"class": "sc"}), chapters))
    return el("nav", {"class": "outline", "aria-label": "The book's outline"}, ol)


def chapter_sections(chapter, page):
    out = el("ol")
    for s in chapter.sections:
        if s.guide is not None:
            out.append(el("li", None, link_to(s.guide, page, s.guide.short)))
            continue
        entries = None
        if s.entries:
            entries = el("ol", {"class": "o-entries"}, [el("li", None, link_to(e, page)) for e in s.entries])
        if s.title:
            out.append(el("li", None, el("a", {"href": f"{chapter.url}#{s.id}"}, s.title), entries))
        elif entries:
            out.append(el("li", None, entries))
    return out if out.children else None


def site_header(book, page):
    chapter = chapter_of(page)
    running = None
    if chapter is not None and chapter is not page:
        short = chapter.title.split(":")[0]
        running = el("a", {"class": "running", "href": chapter.url}, short)
    quick = []
    for label, path in QUICK_LINKS:
        if not book.has_page(path):
            continue
        attrs = {"href": "/" + path}
        if page.path == path:
            attrs["aria-current"] = "page"
        quick.append(el("li", None, el("a", attrs, label)))
    return el("header", {"class": "site-head"},
              el("a", {"class": "skip", "href": "#main"}, "Skip to the text"),
              el("div", {"class": "head-left"},
                 el("a", {"class": "brand", "href": "/"}, book.title),
                 running),
              el("nav", {"class": "quick", "aria-label": "Reference"}, el("ul", None, quick)),
              el("button", {"class": "search-open", "type": "button", "hidden": "", "aria-haspopup": "dialog"},
                 el("span", {"class": "sc"}, "Search"), el("kbd", None, "/")))


def breadcrumbs(page):
    above = trail(page)
    if not above:
        return None
    items = [el("li", None, el("a", {"href": p.url}, p.title)) for p in above]
    return el("nav", {"class": "crumbs", "aria-label": "Breadcrumb"}, el("ol", None, items))


def pager(page):
    if page.prev is None and page.next is None:
        return None
    def link(to, rel, label):
        return el("a", {"class": rel, "rel": rel, "href": to.url}, el("span", {"class": "sc"}, label),
                  el("span", {"class": "pager-title"}, to.title)) if to else None
    return el("nav", {"class": "pager", "aria-label": "Previous and next"},
              link(page.prev, "prev", "Previous"), link(page.next, "next", "Next"))


def site_footer(book):
    s = book.stamp
    edition = edition_label(s)
    when = f", {long_date(s['date'])}" if s["edition"] != "draft" else f", built {long_date(s['date'])}"
    return el("footer", {"class": "site-foot"},
              el("p", None, el("em", None, book.title), f" · {edition}{when} · commit ",
                 el("a", {"href": f"{REPO}/commit/{s['commit'].removesuffix('-dirty')}"}, s["commit"])),
              el("p", None,
                 el("a", {"href": pdf_link(s)}, "PDF"), " · ",
                 el("a", {"href": REPO}, "Source"), " · ",
                 el("a", {"href": "/colophon/"}, "Colophon"), " · ",
                 "Text and illustrations under ",
                 el("a", {"href": LICENCE, "rel": "license"}, "CC BY-SA 4.0")))


def chapter_opening(page):
    """A chapter's head as in print: its number in words, the title, and its hold
    between two short rules."""
    return el("header", {"class": "opening"},
              el("p", {"class": "chapter-label sc"}, f"Chapter {page.word}") if page.word else None,
              el("h1", None, list(page.heading.children)),
              el("span", {"class": "orn-rule"},
                 el("img", {"class": "ornament", "alt": "", "src": f"/figures/ornament-{page.ornament}.svg"})))


def guide_opening(page):
    return el("header", {"class": "guide-head"},
              el("h1", None, el("span", {"class": "num"}, page.number) if page.number else None, " ", list(page.heading.children)))


def on_this_page(page):
    """A phone has no outline beside the text, so a chapter opens with its own."""
    sections = chapter_sections(page, page)
    if sections is None:
        return None
    return el("details", {"class": "on-page"}, el("summary", {"class": "sc"}, "In this chapter"), sections)


def page_content(page):
    """The text of a page from the book, under its head."""
    body = fragment()
    if page.kind in ("chapter", "appendix", "front"):
        body.append(chapter_opening(page), on_this_page(page))
    elif page.kind == "guide":
        body.append(guide_opening(page))
    body.append(list(page.body.children))
    return body


def part_content(page):
    chapters = [el("li", None,
                   el("a", {"href": ch.url}, el("span", {"class": "num"}, ch.number) if ch.number else None, " ", ch.title),
                   el("p", None, ch.description)) for ch in page.chapters]
    return fragment(
        el("header", {"class": "part-opening"},
           el("img", {"class": "ornament", "alt": "", "src": f"/figures/ornament-{page.ornament}.svg"}),
           el("h1", None, el("span", {"class": "part-title sc"}, page.title),
              el("span", {"class": "part-subtitle"}, page.subtitle) if page.subtitle else None)),
        el("ul", {"class": "chapter-list"}, chapters))


def contents_content(book):
    """As in print: parts in small caps, chapters in bold, sections below them. It
    also lists the entries, as the PDF's bookmarks do."""
    def numbered(number, title):
        # The space goes inside the number, which floats beside the title, so that the
        # title's first line starts where its others do.
        return [el("span", {"class": "num"}, number + " "), title] if number else [title]

    out = el("nav", {"class": "contents", "role": "doc-toc", "aria-label": "Contents"})
    fronts = [p for p in book.pages if p.kind == "front"]
    if fronts:
        out.append(el("ol", {"class": "c-chapters"}, [el("li", None, el("a", {"class": "c-chapter", "href": p.url}, p.title)) for p in fronts]))
    for part in book.parts:
        subtitle = [" ", el("em", None, part.subtitle)] if part.subtitle else None
        out.append(el("h2", {"class": "c-part"}, el("a", {"href": part.url}, el("span", {"class": "sc"}, part.title), subtitle)))
        chapters = el("ol", {"class": "c-chapters"})
        for ch in part.chapters:
            sections = el("ol", {"class": "c-sections"})
            for s in ch.sections:
                if s.guide is not None:
                    sections.append(el("li", None, el("a", {"href": s.guide.url}, numbered(s.number, s.title))))
                    continue
                entries = None
                if s.entries:
                    entries = el("ul", {"class": "c-entries"}, [el("li", None, el("a", {"href": e.url}, e.title)) for e in s.entries])
                if s.title:
                    sections.append(el("li", None, el("a", {"href": f"{ch.url}#{s.id}"}, numbered(s.number, s.title)), entries))
                elif entries:
                    sections.append(el("li", None, entries))
            chapters.append(el("li", None,
                               el("a", {"class": "c-chapter", "href": ch.url}, numbered(ch.number, ch.title)),
                               sections if sections.children else None))
        out.append(chapters)
    return fragment(el("header", {"class": "opening"}, el("h1", None, "Contents")), out)


def grade_class(book, label):
    """The class of the tab for the grade guide labelled "grade-3"."""
    return f'g{label.removeprefix("grade-")}' if book.tab_looks else ""


def home_content(book):
    """The title page, then the ways into the book."""
    title_page = book.front[0] if book.front else None
    hero = el("section", {"class": "title-page"})
    if title_page is not None:
        divs = 0
        for node in list(title_page.children):
            if not isinstance(node, Node):
                continue
            if node.tag == "div":
                divs += 1
                if divs == 1:
                    node.tag = "h1"
                    node.attrs["class"] = "book-title"
                else:
                    node.tag = "p"
                    node.attrs["class"] = "tagline"
            elif node.first("img") is not None and node.first(cls="orn-rule") is None:
                node.add_class("cover")
            elif node.first(cls="orn-rule") is not None:
                node.add_class("rule-line")
            elif node.first(cls="sc") is not None and not hero.children:
                node.add_class("strap")
            elif node.first(cls="sc") is not None:
                node.add_class("editor")
            else:
                node.add_class("when")
            hero.append(node)
    actions = el("nav", {"class": "start", "aria-label": "Start"},
                 el("a", {"class": "button primary", "href": book.reading[0].url}, "Start reading"),
                 el("a", {"class": "button", "href": "/contents/"}, "Contents"),
                 el("a", {"class": "button", "href": pdf_link(book.stamp)}, "Download the PDF"))
    guides = [el("li", None, el("a", {"class": f"grade-tab {grade_class(book, label)}", "href": g.url}, g.short))
              for label, g in book.guides.items() if re.fullmatch(r"grade-\d+", label)]
    categories = []
    for key, name in book.categories.items():
        chapter = next((p.parent for p in book.entries.values() if p.meta["category"] == key), None)
        if chapter is None:
            continue
        count = sum(1 for p in book.entries.values() if p.meta["category"] == key)
        categories.append(el("li", None,
                             el("a", {"href": chapter.url},
                                el("img", {"class": "ornament", "alt": "", "src": f"/figures/ornament-{chapter.ornament}.svg"}),
                                el("span", None, name), " ", el("span", {"class": "count"}, f"{count} techniques"))))
    parts = [el("li", None,
                el("a", {"href": p.url}, el("span", {"class": "sc"}, p.title)),
                " ", el("em", None, p.subtitle) if p.subtitle else None) for p in book.parts]
    return fragment(
        hero, actions,
        el("div", {"class": "ways-in"},
           el("section", None, el("h2", {"class": "label"}, "Your grade"),
              el("p", None, "What problems look like at your grade, and what to work on."),
              el("ul", {"class": "grade-row"}, guides)),
           el("section", None, el("h2", {"class": "label"}, "The techniques"),
              el("ul", {"class": "category-row"}, categories)),
           stuck_on_something(book),
           el("section", None, el("h2", {"class": "label"}, "The book"),
              el("ul", {"class": "part-row"}, parts))))


def stuck_on_something(book):
    sentences = []
    if book.has_page("troubleshooting/"):
        sentences += [el("a", {"href": "/troubleshooting/"}, "Troubleshooting"), " goes from what happens on the wall to the techniques that fix it. "]
    if book.has_page("on-the-mat/"):
        sentences += [el("a", {"href": "/on-the-mat/"}, "On the mat"), " is the book on one page, for between attempts."]
    if not sentences:
        return None
    return el("section", None, el("h2", {"class": "label"}, "Stuck on something?"), el("p", None, sentences))


def colophon_content(book):
    """The back of the title page, with a word on how this edition is made."""
    body = fragment(el("header", {"class": "opening"}, el("h1", None, "Colophon")))
    if len(book.front) > 1:
        inner = book.front[1]
        block = inner.first("div") or inner
        body.append(list(block.children))
    body.append(el("hr", {"class": "rule"}),
                el("p", None, "This web edition is generated from the same sources as the ",
                   el("a", {"href": pdf_link(book.stamp)}, "PDF"), ", by website/build.py in the ",
                   el("a", {"href": REPO}, "source repository"), "."),
                el("p", None, "The site sets no cookies, runs no analytics and loads nothing from other servers. "
                              "The web host may keep ordinary server logs."))
    return body


# ------------------------------------------------------------ the page

def json_ld(book, page):
    """What the page is, for search engines. Links in it have to be absolute, so a
    site built without --base-url leaves them out."""
    book_data = {"@type": "Book", "name": book.title, "bookEdition": edition_label(book.stamp)}
    if page.kind == "home":
        data = {**book_data, "inLanguage": "en-GB", "license": LICENCE, "datePublished": book.stamp["date"],
                "editor": {"@type": "Person", "name": book.editor}, "description": page.description}
    else:
        data = {"@type": "Chapter" if page.kind in ("chapter", "appendix", "front", "part") else "Article",
                "headline": page.title, "name": page.title, "inLanguage": "en-GB", "license": LICENCE,
                "description": page.description, "isPartOf": book_data}
    graph = [data]
    if book.base_url:
        data["url"] = f"{book.base_url}/{page.path}"
        above = trail(page)
        if above:
            graph.append({"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": n, "name": p.title, "item": f"{book.base_url}/{p.path}"}
                for n, p in enumerate(above + [page], 1)]})
    return el("script", {"type": "application/ld+json"},
              json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/"))


def head(book, page):
    title = book.title if page.kind == "home" else f"{page.title} · {book.title}"
    url = f"{book.base_url}/{page.path}" if book.base_url else None
    draft = book.stamp["edition"] == "draft"
    out = fragment(
        el("meta", {"charset": "utf-8"}),
        el("meta", {"name": "viewport", "content": "width=device-width, initial-scale=1"}),
        el("title", None, title),
        el("meta", {"name": "description", "content": page.description}),
        el("meta", {"name": "robots", "content": "noindex" if draft else "index, follow"}),
        el("meta", {"name": "color-scheme", "content": "light dark"}),
        el("meta", {"name": "theme-color", "media": "(prefers-color-scheme: light)", "content": "#ffffff"}),
        el("meta", {"name": "theme-color", "media": "(prefers-color-scheme: dark)", "content": "#171614"}),
        el("meta", {"property": "og:title", "content": page.title}),
        el("meta", {"property": "og:site_name", "content": book.title}),
        el("meta", {"property": "og:description", "content": page.description}),
        el("meta", {"property": "og:type", "content": "book" if page.kind == "home" else "article"}),
        el("meta", {"property": "og:locale", "content": "en_GB"}),
        el("link", {"rel": "stylesheet", "href": "/style.css"}),
        el("link", {"rel": "icon", "href": "/favicon.svg", "type": "image/svg+xml"}),
        el("link", {"rel": "apple-touch-icon", "href": "/apple-touch-icon.png"}),
        el("link", {"rel": "manifest", "href": "/manifest.webmanifest"}),
        el("link", {"rel": "license", "href": LICENCE}),
        el("script", {"defer": "", "src": "/site.js"}),
    )
    if url:
        out.append(el("link", {"rel": "canonical", "href": url}),
                   el("meta", {"property": "og:url", "content": url}),
                   el("meta", {"property": "og:image", "content": f"{book.base_url}/share.png"}),
                   el("meta", {"property": "og:image:width", "content": "1200"}),
                   el("meta", {"property": "og:image:height", "content": "630"}),
                   el("meta", {"name": "twitter:card", "content": "summary_large_image"}))
    if page.prev:
        out.append(el("link", {"rel": "prev", "href": page.prev.url}))
    if page.next:
        out.append(el("link", {"rel": "next", "href": page.next.url}))
    out.append(json_ld(book, page))
    return out


def page_html(book, page, content):
    main = el("main", {"id": "main"}, breadcrumbs(page),
              el("article" if page.kind != "entry" else "div", {"class": f"page page-{page.kind}"}, list(content.children)),
              pager(page))
    layout = el("div", {"class": "layout"})
    if page.kind != "home":
        layout.append(outline(book, page))
    layout.append(main)
    body = el("body", {"class": f"kind-{page.kind}"}, site_header(book, page), layout, site_footer(book))
    html = el("html", {"lang": "en-GB"}, el("head", None, head(book, page)), body)
    relativise(html, page.path)
    return "<!doctype html>" + str(html) + "\n"


# ------------------------------------------------------------ the site

def write_page(book, page, content):
    book.size_images(content, page)
    # The first drawing on a page may be what it is judged by, so it loads at once.
    first = next((i for i in content.select("img") if "loading" in i.attrs), None)
    if first is not None:
        del first.attrs["loading"], first.attrs["decoding"]
    target = book.out / page.path / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page_html(book, page, content))


def redirect_stubs(book):
    """A technique merged into another keeps its address: the old one forwards."""
    for old, new in book.key_alias.items():
        if old in book.entries or new not in book.entries:
            continue
        target = book.out / "techniques" / old / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        rel = relative(book.entries[new].url, f"techniques/{old}/")
        target.write_text(f'<!doctype html><html lang="en-GB"><meta charset="utf-8"><title>{escape(book.entries[new].title)}</title>'
                          f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={rel}">'
                          f'<link rel="canonical" href="{rel}"><p>This technique is now part of <a href="{rel}">{escape(book.entries[new].title)}</a>.</p></html>\n')


def write_images(book):
    """The icon and the picture for shared links, drawn by Typst from the book's
    own figures. A site can do without them, so a failure only gets a warning."""
    shutil.copy(book.here / "card.typ", book.work / "book" / "card.typ")
    jobs = [("card", "share.png", 72), ("icon", "icon-512.png", 72), ("icon", "apple-touch-icon.png", 25.3)]
    for what, name, ppi in jobs:
        inputs = dict(what=what, title="|".join(book.title_lines), strap=book.strap, tagline=book.tagline)
        args = [arg for key, value in inputs.items() for arg in ("--input", f"{key}={value}")]
        result = subprocess.run(["typst", "compile", "--root", ".", "--format", "png", "--ppi", str(ppi), *args,
                                 "book/card.typ", str(book.out / name)], cwd=book.work, text=True, capture_output=True)
        if result.returncode:
            book.warn(f"could not draw {name}: {result.stderr.strip()[:200]}")


def write_llms_txt(book, home):
    """A plain index of the book for software that reads sites on someone's behalf."""
    root = f"{book.base_url}/" if book.base_url else ""
    lines = [f"# {book.title}", "", f"> {home.description}", "",
             f"{edition_label(book.stamp)}. Text and illustrations under CC BY-SA 4.0: {LICENCE}", ""]
    for part in book.parts:
        lines.append(f"## {part.title}{': ' + part.subtitle if part.subtitle else ''}")
        lines.append("")
        for chapter in part.chapters:
            lines.append(f"- [{chapter.title}]({root}{chapter.path}): {chapter.description}")
        lines.append("")
    lines.append("## Techniques")
    lines.append("")
    for entry in book.entries.values():
        lines.append(f"- [{entry.title}]({root}{entry.path}): {entry.description}")
    (book.out / "llms.txt").write_text("\n".join(lines) + "\n")


def tab_rules(book):
    """The grade tabs' colours, when this edition has them. A tab keeps its colours in
    dark mode, as a hold does. The rules stay outside the stylesheet's layers, so they win."""
    rules = []
    for g, look in enumerate(book.tab_looks):
        outline = "border:1px solid #111;" if look["outlined"] else ""
        rules.append(f'.g{g}{{background:{look["fill"]};color:{look["figures"]};{outline}}}')
    return "\n".join(rules) + "\n" if rules else ""


def write_extras(book, home, extra):
    out = book.out
    (out / "style.css").write_text((book.here / "style.css").read_text() + tab_rules(book))
    shutil.copy(book.here / "site.js", out / "site.js")
    jug = book.work / "book" / "figures" / "ornament-jug.svg"
    if jug.exists():
        shutil.copy(jug, out / "favicon.svg")
    write_images(book)
    write_llms_txt(book, home)
    (out / "manifest.webmanifest").write_text(json.dumps({
        "name": book.title, "short_name": book.title, "description": home.description,
        "start_url": "./", "scope": "./", "display": "standalone", "lang": "en-GB",
        "background_color": "#ffffff", "theme_color": "#ffffff",
        "icons": [{"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
                  {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}],
    }, ensure_ascii=False, indent=1))
    (out / "previews.json").write_text(json.dumps(book.previews, ensure_ascii=False, separators=(",", ":")))
    (out / "search.json").write_text(json.dumps(book.search, ensure_ascii=False, separators=(",", ":")))
    (out / ".nojekyll").write_text("")  # GitHub Pages: serve everything as it is
    root = f"{book.base_url}/" if book.base_url else "/"
    (out / "404.html").write_text(
        f'<!doctype html><html lang="en-GB"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>Page not found · {escape(book.title)}</title><meta name="robots" content="noindex">'
        f'<style>body{{font:1.1rem/1.6 "Iowan Old Style",Charter,Palatino,Georgia,serif;margin:20vh auto;max-width:34rem;padding:0 1rem}}</style>'
        f'<h1>Page not found</h1><p>This page isn’t in the book. It may have moved in a later edition.</p>'
        f'<p><a href="{root}">{escape(book.title)}</a> · <a href="{root}contents/">Contents</a> · <a href="{root}index/">Index</a></p></html>\n')
    pages = list(book.pages) + extra
    if book.base_url and book.stamp["edition"] != "draft":
        urls = "".join(f"<url><loc>{escape(book.base_url + '/' + p.path)}</loc></url>" for p in pages)
        (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {book.base_url}/sitemap.xml\n")
    else:
        (out / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if book.stamp["edition"] == "draft" else "User-agent: *\nAllow: /\n")


def check_site(book):
    """Follow every internal link in the finished site."""
    out = book.out
    ids = {}
    # 404.html is served from any address, so it links from the host's root.
    pages = [p for p in out.rglob("*.html") if p.name != "404.html"]
    for path in pages:
        ids[path] = set(re.findall(r'\sid="([^"]+)"', path.read_text()))
    broken = []
    for path in pages:
        text = path.read_text()
        for attr, target in re.findall(r'\s(href|src|srcset)="([^"]+)"', text):
            if re.match(r"[a-z]+:", target) or target.startswith("//"):
                continue
            target = unescape(target)
            file_part, _, frag = target.partition("#")
            dest = (path.parent / file_part).resolve() if file_part else path
            if dest.is_dir():
                dest = dest / "index.html"
            if not dest.exists():
                broken.append(f"{path.relative_to(out)}: {target}")
            elif frag and dest.suffix == ".html" and frag not in ids.get(dest, set()):
                broken.append(f"{path.relative_to(out)}: {target}")
    return broken


def write_site(book):
    from book import Page

    home = Page("", book.title, "home")
    home.next = book.reading[0] if book.reading else None
    home.description = book.tagline or book.strap or book.title

    contents = Page("contents/", "Contents", "contents")
    contents.description = f"The contents of {book.title}: every part, chapter, section and technique."
    colophon = Page("colophon/", "Colophon", "colophon")
    colophon.description = f"Edition, licence and how to cite {book.title}."

    home.body = home_content(book)
    colophon.body = colophon_content(book)
    for page in book.pages:
        write_page(book, page, part_content(page) if page.kind == "part" else page_content(page))
    write_page(book, contents, contents_content(book))
    write_page(book, home, home.body)
    write_page(book, colophon, colophon.body)
    redirect_stubs(book)
    book.copy_assets()
    write_extras(book, home, [home, contents, colophon])

    broken = check_site(book)
    for line in broken:
        print("broken link: " + line)
    for line in book.errors:
        print("error: " + line)
    print(f"\nwrote {len(book.pages) + 3} pages to {book.out} "
          f"({len(book.entries)} techniques, {len(book.guides)} grade guides, {len(book.ix)} index terms, "
          f"{len(book.assets)} images), {len(book.warnings)} warnings, {len(broken) + len(book.errors)} errors")
    return not broken and not book.errors
