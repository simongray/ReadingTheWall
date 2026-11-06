"""List what's left to do in book/figure-alt.toml, the drawings' text descriptions.

Usage: python3 tools/check_alt.py

Run python3 figtools/build_all.py first, since the figures are generated. This
lists the figures with no description, the descriptions whose figure no longer
exists, and the figures whose SVG has changed since `drawn` was recorded. Once
you've revised a changed figure's description, copy the new hash into `drawn`.
The ornaments and icons are decorative, so they need no description. Prints
nothing if all is well, and otherwise exits with status 1.
"""
import hashlib
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "book" / "figures"
DESCRIPTIONS = ROOT / "book" / "figure-alt.toml"
DECORATIVE = ("ornament", "icon-")


def fingerprint(path):
    """The first 12 hex digits of the SHA-256 of the file at `path`."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def report(title, lines):
    """Print `title` and the `lines` under it, if there are any."""
    if lines:
        print(title)
        for line in lines:
            print("  " + line)


def main():
    figures = {path.name: path for path in FIGURES.glob("*.svg")}
    if not figures:
        sys.exit("No figures in book/figures: run python3 figtools/build_all.py first.")
    entries = {}
    if DESCRIPTIONS.exists():
        entries = tomllib.loads(DESCRIPTIONS.read_text(encoding="utf-8"))

    missing = [name for name in figures
               if not name.startswith(DECORATIVE) and not entries.get(name, {}).get("alt")]
    gone = [name for name in entries if name not in figures]
    changed = []
    for name, entry in entries.items():
        if name in figures and entry.get("drawn") != fingerprint(figures[name]):
            changed.append(f"{name}: drawn {entry.get('drawn')}, now {fingerprint(figures[name])}")

    report("No description:", sorted(missing))
    report("Description, but no such figure:", sorted(gone))
    report("Figure changed since it was described:", sorted(changed))
    if missing or gone or changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
