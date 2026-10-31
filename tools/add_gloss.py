"""Add glossary entries to book/chapters/a-glossary.typ and keep it sorted.

Usage: python3 tools/add_gloss.py entries.txt
where each line of entries.txt is:  term | definition | key1,key2 (optional)
Existing terms are left alone unless the line starts with '!'.
"""
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "book", "chapters", "a-glossary.typ")


def sort_key(term):
    t = unicodedata.normalize("NFKD", term.lower())
    return "".join(c for c in t if c.isalnum() or c == " ")


def main(src):
    text = open(PATH, encoding="utf-8").read()
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("#gloss(")]
    entries = {}
    for i in idx:
        term = re.match(r'#gloss\("([^"]+)"', lines[i]).group(1)
        entries[term.lower()] = lines[i]
    added = 0
    for raw in open(src, encoding="utf-8"):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        force = raw.startswith("!")
        parts = [p.strip() for p in raw.lstrip("!").split("|")]
        term, body = parts[0], parts[1]
        keys = [k for k in (parts[2].split(",") if len(parts) > 2 else []) if k.strip()]
        if term.lower() in entries and not force:
            continue
        see = ""
        if keys:
            ks = ", ".join(f'"{k.strip()}"' for k in keys)
            see = f", see: ({ks}{',' if len(keys) == 1 else ''})"
        entries[term.lower()] = f'#gloss("{term}"{see})[{body}]'
        added += 1
    first, last = idx[0], idx[-1]
    body = []
    for k in sorted(entries, key=sort_key):
        body += [entries[k], ""]
    out = lines[:first] + body[:-1] + lines[last + 1:]
    open(PATH, "w", encoding="utf-8").write("\n".join(out))
    print(f"added {added}, total {len(entries)}")


if __name__ == "__main__":
    main(sys.argv[1])
