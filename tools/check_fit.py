"""Report the texts that are fitted to their pages (technique entries and
#fit-pages stretches) but take more pages than estimated.

The template estimates a text's pages from its measured height, which
isn't broken into pages, so a block that moves whole to the next page can
make the text spill a line or two. Give such a text a tighter space factor
by hand, e.g. `k: 0.35` in its #technique(...) or #fit-pages(k: 0.35)[...].

Usage: check_fit.py [TYPST ARGS...], run from the repository root, e.g.
check_fit.py --input edition=draft
"""
import json
import subprocess
import sys

EXPR = ("(query(<fit-start>).map(m => (m.value.what, m.value.est, m.location().page())),"
        " query(<fit-end>).map(m => (m.location().page(), m.location().position().y.pt())))")
MARGIN_TOP = 25 / 25.4 * 72      # pt, as in book/template.typ


def last_page(page, y):
    """The page a text ends on, from where its end marker is: a marker at
    the very top of a page was only pushed there, so the text ended on the
    page before."""
    return page - 1 if y < MARGIN_TOP + 1 else page


run = subprocess.run(["typst", "eval", EXPR, "--root", ".", *sys.argv[1:],
                      "--in", "book/main.typ"], capture_output=True, text=True)
if run.returncode != 0:
    sys.exit(run.stderr)
starts, ends = json.loads(run.stdout)
ends = [last_page(page, y) for page, y in ends]
spills = [(what or f"the text from p. {start}", est, end - start + 1)
          for (what, est, start), end in zip(starts, ends) if end - start + 1 > est]
for what, est, took in spills:
    print(f"check_fit: {what} was estimated at {est} page(s) but takes {took}; "
          "give it a tighter k")
if not spills:
    print(f"check_fit: all {len(starts)} fitted texts take the pages estimated")
