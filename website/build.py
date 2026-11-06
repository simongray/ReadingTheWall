#!/usr/bin/env python3
"""Build the web edition of the book.

    ./build-site.sh                     the working tree (the edition, if it is
                                        a clean checkout of an edition's tag)
    ./build-site.sh --ref edition-2     an edition or commit, taken from git
    ./build-site.sh --source ../other   the working tree of another checkout
    ./build-site.sh --serve             build, then serve it on localhost

The book itself is never touched. This script works in a temporary copy:

1. It runs the generators that build.sh (or, for an edition, release.sh) runs
   before it compiles, so a generator added later is picked up by itself.
2. It puts website/template.typ in place of book/template.typ, with the real
   template beside it. The chapters then compile unchanged to one long HTML file.
3. website/book.py turns that file into the site.
"""
import argparse
import hashlib
import http.server
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import date
from functools import partial
from io import BytesIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import book as site_book  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Left in every site this script writes, so that it only ever replaces its own.
MARKER = ".reading-the-wall-site"
# Warnings that HTML export always gives for this book and that lose nothing.
HARMLESS = ("html export is under active development", "page set rule was ignored")


def run(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True, **kw)


def git(source, *args):
    return run(["git", *args], source).stdout.strip()


def edition_of(source, rev):
    """The edition number if `rev` carries an edition's tag, else None."""
    try:
        tag = git(source, "describe", "--exact-match", "--tags", "--match", "edition-*", rev)
    except subprocess.CalledProcessError:
        return None, None
    return tag.removeprefix("edition-"), tag


def copy_source(args, work):
    """Copy the book into `work`. Returns the edition, date and commit to stamp it
    with, the same way build.sh and release.sh do."""
    source = Path(args.source).resolve()
    if args.ref:
        archive = subprocess.run(["git", "archive", args.ref], cwd=source, check=True, capture_output=True).stdout
        with tarfile.open(fileobj=BytesIO(archive)) as tar:
            tar.extractall(work, filter="data")
        rev, dirty = args.ref, False
    else:
        shutil.copytree(source, work, dirs_exist_ok=True, ignore=shutil.ignore_patterns(
            ".git", ".claude", "editions", "private", "site", "__pycache__", "*.pdf"))
        rev = "HEAD"
        dirty = bool(git(source, "status", "--porcelain"))
    edition, tag = (None, None) if dirty else edition_of(source, rev)
    commit = git(source, "rev-parse", "--short", rev + "^{commit}") + ("-dirty" if dirty else "")
    # An annotated tag's own date is the day the edition was released.
    day = git(source, "for-each-ref", f"refs/tags/{tag}", "--format=%(creatordate:short)") if tag else date.today().isoformat()
    return dict(edition=edition or "draft", date=day, commit=commit)


def generators(work, edition):
    """The Python commands the book's own script runs before it compiles."""
    script = work / ("build.sh" if edition == "draft" else "release.sh")
    commands = []
    for line in script.read_text().splitlines():
        if line.strip().startswith("typst compile"):
            break
        m = re.match(r"\s*python3 (\S+)(.*)$", line)
        if m:
            extra = m.group(2).replace('"$n"', edition).replace("$n", edition).split()
            commands.append([m.group(1), *extra])
    return commands


def run_generators(work, edition):
    """Run the generators. The figures take a while, so they are kept in a cache
    named after what they are made from: the code that draws them, and the entries'
    grades in the chapters, which can decide their colours."""
    drawing = hashlib.sha256()
    for path in sorted((work / "figtools").glob("*.py")):
        drawing.update(path.read_bytes())
    for path in sorted((work / "book" / "chapters").glob("*.typ")):
        drawing.update("".join(re.findall(r"^\s*(?:key|grade|figure):.*$|^#filmstrip\(.*$", path.read_text(), re.M)).encode())
    cache = Path(tempfile.gettempdir()) / "reading-the-wall-figures" / drawing.hexdigest()[:16]
    for script, *extra in generators(work, edition):
        if script.endswith("build_all.py") and cache.is_dir():
            shutil.copytree(cache, work / "book" / "figures", dirs_exist_ok=True)
            print("figures: reused from the cache")
            continue
        print(f"running {script} {' '.join(extra)}".rstrip())
        result = run([sys.executable, script, *extra], work)
        for line in result.stdout.splitlines() + result.stderr.splitlines():
            if "warn" in line.lower():
                print("  " + line)
        if script.endswith("build_all.py"):
            cache.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(work / "book" / "figures", cache, dirs_exist_ok=True)


def install_template(work):
    """Put the web template in place, keeping the real one beside it."""
    book = work / "book"
    (book / "template.typ").rename(book / "template-print.typ")
    shutil.copy(HERE / "template.typ", book / "template.typ")
    # A page of its own in print (the title page and its back) is a section here.
    for path in (book / "chapters").glob("*.typ"):
        text = path.read_text()
        patched = re.sub(r"^#page\(", "#web-page(", text, flags=re.M)
        if patched != text:
            path.write_text(patched)


def compile_html(work, stamp):
    """Compile the book to one HTML file. Typst's warnings go to the terminal,
    because a layout element it ignores takes its content with it."""
    out = work / "book.html"
    inputs = [arg for key, value in stamp.items() for arg in ("--input", f"{key}={value}")]
    result = subprocess.run(
        ["typst", "compile", "--root", ".", "--features", "html", "--format", "html", *inputs, "book/main.typ", str(out)],
        cwd=work, text=True, capture_output=True)
    blocks = re.split(r"\n(?=warning:|error:)", result.stderr.strip())
    shown = [b for b in blocks if b and not any(h in b for h in HARMLESS)]
    for block in shown:
        print(block, file=sys.stderr)
    if result.returncode:
        sys.exit("Typst could not compile the book (see above)")
    return out.read_text()


def clear_output(out):
    """Empty the output folder, which must be a site this script wrote."""
    if out.exists() and any(out.iterdir()) and not (out / MARKER).exists():
        sys.exit(f"{out} isn't empty and isn't a site this script wrote: choose another --out")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / MARKER).write_text("Written by website/build.py. Everything here is replaced by the next build.\n")


def serve(out, port):
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(f"serving {out} at http://localhost:{port}/ (ctrl-C stops it)")
        server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Build the web edition of the book.")
    parser.add_argument("--ref", help="build this tag or commit from git (e.g. edition-2) instead of the working tree")
    parser.add_argument("--source", default=str(ROOT), help="the checkout to build from (default: this one)")
    parser.add_argument("--out", default=str(ROOT / "site"), help="where to write the site (default: site/)")
    parser.add_argument("--base-url", default="", help="the site's public URL, for canonical links and the sitemap")
    parser.add_argument("--serve", action="store_true", help="serve the site on localhost after building it")
    parser.add_argument("--port", type=int, default=8000, help="the port for --serve (default: 8000)")
    args = parser.parse_args()
    if shutil.which("typst") is None:
        sys.exit("this script needs typst: brew install typst")

    out = Path(args.out).resolve()
    with tempfile.TemporaryDirectory(prefix="reading-the-wall-") as tmp:
        work = Path(tmp)
        stamp = copy_source(args, work)
        print(f"building {args.ref or args.source}: edition {stamp['edition']}, {stamp['date']}, commit {stamp['commit']}")
        run_generators(work, stamp["edition"])
        install_template(work)
        html = compile_html(work, stamp)
        clear_output(out)
        ok = site_book.build(html, work, out, stamp, args.base_url.rstrip("/"), HERE)
    if args.serve:
        serve(out, args.port)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
