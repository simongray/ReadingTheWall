"""List what's left to do in book/figure-alt.toml, the drawings' text descriptions.

Usage: python3 tools/check_alt.py

This draws the figures in grey in a temporary folder, with figtools/build_all.py
--grey, and lists the figures with no description, the descriptions whose figure
no longer exists, and the figures whose grey drawing has changed since `drawn` was
recorded. A change in paint.py's colours doesn't count, since the descriptions
never name a colour. Once you've revised a changed figure's description, copy the
new hash into `drawn`. The ornaments and icons are decorative, so they need no
description. Prints nothing if all is well, and otherwise exits with status 1.
"""
import hashlib
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESCRIPTIONS = ROOT / "book" / "figure-alt.toml"
DECORATIVE = ("ornament", "icon-")


def fingerprint(path):
    """The first 12 hex digits of the SHA-256 of the file at `path`."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def drawings():
    """The fingerprint of each figure as drawn in grey, by file name."""
    with tempfile.TemporaryDirectory() as folder:
        build = subprocess.run([sys.executable, ROOT / "figtools" / "build_all.py", "--grey", folder],
                               capture_output=True, text=True)
        if build.returncode:
            sys.exit(build.stdout + build.stderr)
        return {path.name: fingerprint(path) for path in Path(folder).glob("*.svg")}


def report(title, lines):
    """Print `title` and the `lines` under it, if there are any."""
    if lines:
        print(title)
        for line in lines:
            print("  " + line)


def main():
    figures = drawings()
    entries = {}
    if DESCRIPTIONS.exists():
        entries = tomllib.loads(DESCRIPTIONS.read_text(encoding="utf-8"))

    missing = [name for name in figures
               if not name.startswith(DECORATIVE) and not entries.get(name, {}).get("alt")]
    gone = [name for name in entries if name not in figures]
    changed = [f"{name}: drawn {entry.get('drawn')}, now {figures[name]}"
               for name, entry in entries.items()
               if name in figures and entry.get("drawn") != figures[name]]

    report("No description:", sorted(missing))
    report("Description, but no such figure:", sorted(gone))
    report("Figure changed since it was described:", sorted(changed))
    if missing or gone or changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
