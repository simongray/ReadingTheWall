"""Check the exercises booklet: each question starts a right-hand (odd) page
with its answer on the next page, and every reference into the book resolved.

    python3 tools/check_booklet.py [typst inputs]

build.sh runs it after compiling the booklet.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PDF = os.environ.get("BOOKLET", "Reading the Wall - Exercises.pdf")
EXPR = 'query(<reading-page>).map(m => (n: m.value.n, side: m.value.side, page: m.location().page()))'


def main():
    run = subprocess.run(["typst", "eval", EXPR, "--root", ".", "--input", "booklet=1", *sys.argv[1:], "--in", "book/exercises.typ"],
                         capture_output=True, text=True, cwd=ROOT)
    if run.returncode != 0:
        sys.exit(run.stderr)
    pairs = {}
    for r in json.loads(run.stdout):
        pairs.setdefault(r["n"], {})[r["side"]] = r["page"]
    fails = []
    for n, pair in sorted(pairs.items()):
        q, a = pair.get("question"), pair.get("answer")
        if q is None or a is None or a != q + 1 or q % 2 == 0:
            fails.append(f"Problem {n}: the question is on physical p. {q} and the answer on {a}")
    if not pairs:
        fails.append("no problems found")
    # an unresolved reference shows as [?key]
    text = subprocess.run(["pdftotext", os.path.join(ROOT, PDF), "-"], capture_output=True, text=True,
                          check=True).stdout
    fails += [f"unresolved reference {w}" for w in sorted(set(w for w in text.split() if w.startswith("[?")))]
    for f in fails:
        print("check_booklet:", f)
    print(f"check_booklet: {len(pairs)} problems, {len(fails)} faults")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
