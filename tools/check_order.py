"""Report the technique entries whose steps send the reader to a harder one.

Prints one line for each case where an entry's `how:` steps link with #tref
to a technique badged at a higher grade than the entry:

    check_order: V1 Sidepull -> V4 Drop knee

This is information for the editor and never fails the build. A reference
resolves as tref() does in book/template.typ: an entry with that very key wins,
then book/key-alias.typ. A key with no entry either way is left out, since
tref() already shows it as [?key].

Usage: check_order.py, run from the repository root.
"""
import glob
import re

CHAPTERS = "book/chapters/0[3-7]*.typ"
ALIASES = "book/key-alias.typ"
TREF = re.compile(r'#tref\(\s*"([^"]+)"')


def skip_comment(s, i):
    """The index after the comment that starts at s[i], or i if none does."""
    if s.startswith("//", i) and (i == 0 or s[i - 1] != ":"):
        end = s.find("\n", i)
        return len(s) if end < 0 else end
    if s.startswith("/*", i):
        end = s.find("*/", i)
        return len(s) if end < 0 else end + 2
    return i


def skip_string(s, i):
    """The index after the string that opens at s[i]."""
    i += 1
    while i < len(s) and s[i] != '"':
        i += 2 if s[i] == "\\" else 1
    return i + 1


def skip_content(s, i):
    """The index after the content block that opens at s[i]. Quotes in markup
    are only text, so brackets are counted without regard to them, except in
    the arguments of a #call(...), where strings are real strings."""
    i += 1
    while i < len(s) and s[i] != "]":
        after = skip_comment(s, i)
        if after != i:
            i = after
        elif s[i] == "\\":
            i += 2
        elif s[i] == "[":
            i = skip_content(s, i)
        elif s[i] == "#":
            call = re.compile(r"#[\w.-]+\(").match(s, i)
            i = skip_code(s, call.end() - 1) if call else i + 1
        else:
            i += 1
    return i + 1


def skip_code(s, i):
    """The index after the parentheses that open at s[i]."""
    i += 1
    while i < len(s) and s[i] != ")":
        after = skip_comment(s, i)
        if after != i:
            i = after
        elif s[i] == '"':
            i = skip_string(s, i)
        elif s[i] == "[":
            i = skip_content(s, i)
        elif s[i] == "(":
            i = skip_code(s, i)
        else:
            i += 1
    return i + 1


def top_level_args(s, i):
    """The named arguments of the call whose parentheses open at s[i], as a
    dictionary of name to source text."""
    args = {}
    i += 1
    while i < len(s) and s[i] != ")":
        after = skip_comment(s, i)
        if after != i:
            i = after
            continue
        m = re.compile(r"([\w-]+)\s*:\s*").match(s, i)
        if not m:
            i += 1
            continue
        start = i = m.end()
        while i < len(s) and s[i] not in ",)":
            if s[i] == '"':
                i = skip_string(s, i)
            elif s[i] == "[":
                i = skip_content(s, i)
            elif s[i] == "(":
                i = skip_code(s, i)
            else:
                i += 1
        args[m.group(1)] = s[start:i].strip()
    return args


def entries(text):
    """Yield the named arguments of each #technique(...) in a chapter."""
    i = 0
    while True:
        at = text.find("#technique(", i)
        if at < 0:
            return
        line_start = text.rfind("\n", 0, at) + 1
        if "//" in text[line_start:at]:
            i = at + 1
            continue
        yield top_level_args(text, at + len("#technique"))
        i = skip_code(text, at + len("#technique"))


def grade_label(g):
    return "VB" if g < 0 else "V8+" if g >= 8 else f"V{g}"


def read_entries():
    """The entries of the technique chapters in document order. A key that
    appears twice keeps its first entry, as tref() does."""
    found = {}
    for path in sorted(glob.glob(CHAPTERS)):
        with open(path, encoding="utf-8") as f:
            for args in entries(f.read()):
                key = args.get("key", "").strip('"')
                grade = re.fullmatch(r"-?\d+", args.get("grade", ""))
                if key and grade and key not in found:
                    found[key] = dict(name=args.get("name", key).strip('"'),
                                      grade=int(grade.group()),
                                      how=args.get("how", ""))
    return found


def read_aliases():
    with open(ALIASES, encoding="utf-8") as f:
        return dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', f.read()))


def main():
    found = read_entries()
    aliases = read_aliases()
    count = 0
    for e in found.values():
        seen = set()
        for key in TREF.findall(e["how"]):
            key = key if key in found else aliases.get(key, key)
            target = found.get(key)
            if target and key not in seen and target["grade"] > e["grade"]:
                seen.add(key)
                count += 1
                print(f"check_order: {grade_label(e['grade'])} {e['name']} -> "
                      f"{grade_label(target['grade'])} {target['name']}")
    print(f"check_order: {count} step link(s) to a higher grade, "
          f"across {len(found)} entries")


if __name__ == "__main__":
    main()
