"""Report on a gym survey (research/gym-survey.md): what the problems at each
grade look like, how often each technique is needed, and how the book's badges
compare with the grades the data suggests.

Usage: python3 tools/survey_report.py <csv>, run from the repository root.
"""
import csv
import datetime
import difflib
import glob
import io
import os
import re
import statistics
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The badge rule that research/gym-survey.md proposes.
REQUIRED_SHARE = 0.10
MIN_TICKS = 3
MIN_PROBLEMS = 20           # a grade with fewer is too thin to trust

SURVEY_GRADES = range(0, 7)     # V0 to V6, which the survey aims to cover

COLUMNS = ("gym", "date", "grade", "wall_angle", "hand_moves", "hold_types",
           "sit_start", "top_out", "required", "used_by_choice", "basis",
           "logger", "height_band", "reach_band")
WALL_ANGLES = ("slab", "vertical", "slight", "moderate", "steep", "roof")
HOLD_TYPES = ("jug", "edge", "crimp", "sloper", "pinch", "pocket", "volume")
BASES = ("climbed", "watched", "read")
BANDS = ("under-160", "160-169", "170-179", "180-189", "190-plus")
YES_NO = {"yes": True, "y": True, "no": False, "n": False}

# The book's grade conversion (book/chapters/a-grades.typ), with VB in the
# VB–V0 badge. Font grades above this table count as V8+.
FONT = {"3": 0, "4-": 0, "4": 0, "4+": 0, "5": 1, "5+": 2, "6a": 3, "6a+": 3,
        "6b": 4, "6b+": 4, "6c": 5, "6c+": 5, "7a": 6, "7a+": 7, "7b": 8,
        "7b+": 8, "7c": 8, "7c+": 8}


def count(n, noun):
    """`n` and the `noun` in the right number."""
    return f"{n} {noun}" if n == 1 else f"{n} {noun}s"


def clean(text):
    """`text` in lower case, with accents and typed dashes flattened, since
    phone keyboards turn arete into arête and a hyphen into a dash."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub("[–—−]", "-", text).strip().lower()


def tokens(text):
    """The values in the cell `text`, separated by spaces, semicolons or
    commas."""
    return [t for t in re.split(r"[\s;,]+", clean(text)) if t]


def grade_label(grade):
    """The book's label for the number `grade`."""
    return "V8+" if grade >= 8 else f"V{grade}"


def parse_grade(text):
    """The badge number for the tag `text`, e.g. 3 for V3, V3+ or 6A, or None
    if it isn't one grade."""
    text = clean(text)
    m = re.fullmatch(r"v(b|\d+)[+-]?", text)
    if m:
        return 0 if m.group(1) == "b" else min(int(m.group(1)), 8)
    return 8 if re.fullmatch(r"(8|9)[abc]\+?", text) else FONT.get(text)


def book_badges():
    """Each technique's key and badge number, in book order, from the entries
    in chapters 3 to 7."""
    badges = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "book", "chapters", "0[3-7]*.typ"))):
        with open(path, encoding="utf-8") as f:
            entries = re.split(r"^[ \t]*#technique\(", f.read(), flags=re.M)[1:]
        for entry in entries:
            key = re.search(r'\bkey:\s*"([^"]+)"', entry)
            grade = re.search(r"\bgrade:\s*(-?\d+)", entry)
            if key and grade:
                badges[key.group(1)] = int(grade.group(1))
    if not badges:
        sys.exit("survey_report: found no technique entries in book/chapters/0[3-7]*.typ.")
    return badges


def key_aliases(badges):
    """The merged keys in book/key-alias.typ, each with the key that holds it
    now. As in the book's cross-references, a key that still has an entry in
    `badges` stays itself."""
    try:
        with open(os.path.join(ROOT, "book", "key-alias.typ"), encoding="utf-8") as f:
            pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', f.read())
    except OSError:
        return {}
    return {old: new for old, new in pairs if old not in badges}


def read_rows(path):
    """The rows of the CSV at `path` as (line number, cells). The file may come
    from a spreadsheet that writes a byte-order mark or separates cells with
    semicolons or tabs."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            text = f.read()
    except OSError as e:
        sys.exit(f"survey_report: can't read {path}: {e.strerror}.")
    except UnicodeDecodeError:
        sys.exit(f"survey_report: {path} isn't UTF-8. Export it from your spreadsheet as CSV UTF-8.")
    if not text.strip():
        sys.exit(f"survey_report: {path} is empty. Start from research/gym-survey-template.csv.")
    delimiter = max(",;\t", key=text.strip().splitlines()[0].count)
    reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter)
    rows = []
    try:
        for cells in reader:
            rows.append((reader.line_num, cells))
    except csv.Error as e:
        sys.exit(f"survey_report: can't parse {path} near line {reader.line_num}: {e}.")
    return rows


def describe(text):
    """How a message says what the cell `text` holds."""
    return f"is {text.strip()!r}" if text.strip() else "is empty"


def choice(cell, column, options, faults):
    """The value in `column` of the row `cell`, adding to `faults` unless it's
    one of `options`."""
    value = clean(cell[column])
    if value not in options:
        faults.append(f"{column} {describe(cell[column])}, expected one of: {', '.join(options)}")
    return value


def parse_problem(cell, aliases):
    """The problem in the row `cell`, a dict of column to text, and a list of
    what's wrong with it. The problem is None if anything is."""
    faults = []
    grade = parse_grade(cell["grade"])
    if grade is None:
        faults.append(f"grade {describe(cell['grade'])}, expected one grade such as V3 or 6A")
    if not cell["gym"].strip():
        faults.append("gym is empty")
    try:
        datetime.date.fromisoformat(cell["date"].strip())
    except ValueError:
        faults.append(f"date {describe(cell['date'])}, expected YYYY-MM-DD")
    moves = cell["hand_moves"].strip()
    if not re.fullmatch(r"0*[1-9][0-9]*", moves):
        faults.append(f"hand_moves {describe(moves)}, expected a whole number above 0")
    holds = tokens(cell["hold_types"])
    if not holds:
        faults.append("hold_types is empty")
    for hold in holds:
        if hold not in HOLD_TYPES:
            faults.append(f"hold_types has {hold!r}, expected: {', '.join(HOLD_TYPES)}")
    wall = choice(cell, "wall_angle", WALL_ANGLES, faults)
    sit = choice(cell, "sit_start", YES_NO, faults)
    top = choice(cell, "top_out", YES_NO, faults)
    basis = choice(cell, "basis", BASES, faults)
    logger = cell["logger"].strip()
    if not re.fullmatch(r"[A-Za-z0-9]{1,3}", logger):
        faults.append(f"logger {describe(logger)}, expected a code of up to three characters, not a name")
    for column in ("height_band", "reach_band"):
        if clean(cell[column]) and clean(cell[column]) not in BANDS:
            faults.append(f"{column} isn't a band: use one of {', '.join(BANDS)}, never an exact figure")
    if faults:
        return None, faults
    required = {aliases.get(k, k) for k in tokens(cell["required"])}
    if YES_NO[sit]:
        required.add("sit-start")
    if YES_NO[top]:
        required.add("top-out")
    return dict(grade=grade, font=not clean(cell["grade"]).startswith("v"),
                wall=wall, moves=int(moves), holds=set(holds),
                sit=YES_NO[sit], top=YES_NO[top], basis=basis, logger=logger,
                height=clean(cell["height_band"]), reach=clean(cell["reach_band"]),
                required=required,
                used={aliases.get(k, k) for k in tokens(cell["used_by_choice"])}), []


def load_problems(rows, aliases):
    """The problems in `rows`, with the lines of empty rows and the messages
    about the others."""
    head = next((i for i, (_, cells) in enumerate(rows) if any(c.strip() for c in cells)), None)
    if head is None:
        sys.exit("survey_report: the file has no header row. Start from research/gym-survey-template.csv.")
    header = [clean(c).replace(" ", "_") for c in rows[head][1]]
    missing = [c for c in COLUMNS if c not in header]
    if missing:
        sys.exit(f"survey_report: line {rows[head][0]} lacks these columns: {', '.join(missing)}. "
                 "The first row must be the header from research/gym-survey-template.csv.")
    problems, empty, messages = [], [], []
    for line, cells in rows[head + 1:]:
        if not any(c.strip() for c in cells):
            empty.append(line)
        elif len(cells) != len(header):
            messages.append(f"line {line}: has {len(cells)} cells where the header has {len(header)}. Row skipped.")
        else:
            problem, faults = parse_problem(dict(zip(header, cells)), aliases)
            if faults:
                messages.append(f"line {line}: {'; '.join(faults)}. Row skipped.")
            else:
                problem["line"] = line
                problems.append(problem)
    return problems, empty, messages


def tick_messages(problems, badges):
    """Messages about ticks that contradict each other or match no entry in
    the book, moving a key in both lists of a problem in `problems` to
    required only."""
    messages, unknown = [], {}
    for p in problems:
        both = p["required"] & p["used"]
        if both:
            messages.append(f"line {p['line']}: ticked as both required and used by choice: "
                            f"{', '.join(sorted(both))}. Counted as required.")
            p["used"] -= both
        for key in (p["required"] | p["used"]) - set(badges):
            unknown.setdefault(key, []).append(p["line"])
    for key, lines in sorted(unknown.items()):
        close = difflib.get_close_matches(key, badges, n=1)
        hint = f" Did you mean {close[0]}?" if close else ""
        messages.append(f"{key} isn't an entry in the book, on {count(len(lines), 'row')} "
                        f"(first on line {lines[0]}).{hint}")
    return messages


def logger_lines(problems):
    """A line per logger with their problems and bands, and messages about any
    bands that are missing or disagree."""
    lines, messages = [], []
    for logger in sorted({p["logger"] for p in problems}):
        own = [p for p in problems if p["logger"] == logger]
        bands = []
        for field in ("height", "reach"):
            found = sorted({p[field] for p in own if p[field]})
            bands.append(f"{field} {' or '.join(found) or 'not given'}")
            if len(found) != 1:
                amount = "more than one" if found else "no"
                messages.append(f"Logger {logger} has {amount} {field} band.")
        lines.append(f"  {logger}: {count(len(own), 'problem')}, {', '.join(bands)}")
    return lines, messages


def share(n, total):
    """`n` as a percentage of `total`."""
    return f"{n / total:.0%}"


def mix(problems, options, has):
    """Those `options` that any of `problems` has, each with its share of the
    problems, where `has` says whether a problem has an option."""
    counts = ((o, sum(has(p, o) for p in problems)) for o in options)
    return ", ".join(f"{o} {share(n, len(problems))}" for o, n in counts if n)


def moves_line(problems):
    """The median number of moves in `problems`, and the middle half when
    there are enough problems to have one."""
    moves = [p["moves"] for p in problems]
    line = f"median {statistics.median(moves):g}"
    if len(moves) > 1:
        low, _, high = statistics.quantiles(moves, n=4, method="inclusive")
        line += f", middle half {low:.0f}–{high:.0f}"
    return line


def print_grade(grade, problems):
    """The report on the `problems` tagged at `grade`."""
    total = len(problems)
    flag = ""
    if total < MIN_PROBLEMS:
        flag = f"  FLAG too few to trust (under {MIN_PROBLEMS})"
    print(f"\n{grade_label(grade)}: {count(total, 'problem')}{flag}")
    if not problems:
        return
    print(f"  Moves:       {moves_line(problems)}")
    print(f"  Wall angle:  {mix(problems, WALL_ANGLES, lambda p, o: p['wall'] == o)}")
    print(f"  Hold types:  {mix(problems, HOLD_TYPES, lambda p, o: o in p['holds'])}")
    print(f"  Sit starts:  {share(sum(p['sit'] for p in problems), total)}")
    print(f"  Top-outs:    {share(sum(p['top'] for p in problems), total)}")
    basis = ", ".join(f"{b} {sum(p['basis'] == b for p in problems)}" for b in BASES)
    guess = sum(p["basis"] == "read" for p in problems) > total / 2
    print(f"  Basis:       {basis}{'  FLAG mostly read from the floor' if guess else ''}")
    tallies = []
    for key in {k for p in problems for k in p["required"] | p["used"]}:
        tallies.append((sum(key in p["required"] for p in problems),
                        sum(key in p["used"] for p in problems), key))
    if not tallies:
        print("  Techniques:  none ticked")
        return
    width = max(len(key) for _, _, key in tallies + [(0, 0, "Technique")])
    print(f"  {'Technique':<{width}}  Required   Used by choice")
    for required, used, key in sorted(tallies, key=lambda t: (-t[0], -t[1], t[2])):
        print(f"  {key:<{width}}  {f'{share(required, total)} ({required})':<9}  "
              f"{share(used, total)} ({used})")


def suggested_grade(key, trusted):
    """The lowest grade in `trusted`, a dict of grade to problems, that meets
    the badge rule for `key`, with its required count and total, or None."""
    for grade in sorted(trusted):
        n = sum(key in p["required"] for p in trusted[grade])
        if n >= MIN_TICKS and n / len(trusted[grade]) >= REQUIRED_SHARE:
            return grade, n, len(trusted[grade])
    return None


def badge_flag(book, data, top):
    """The flag for a technique with the badge `book` and the suggested grade
    `data`, or None, where `top` is the highest grade with enough problems."""
    if data is None:
        if book > top:
            return ""
        return f"FLAG no grade up to {grade_label(top)} meets the rule"
    gap = data - book
    if gap == 0:
        return ""
    return f"FLAG data {count(abs(gap), 'grade')} {'higher' if gap > 0 else 'lower'}"


def print_badges(badges, by_grade):
    """The table of each technique's badge in `badges` against the grade that
    `by_grade`, a dict of grade to problems, suggests."""
    print("\nBadges: the book against the data")
    print(f"Rule: required on at least {REQUIRED_SHARE:.0%} of a grade's problems and on at "
          f"least {MIN_TICKS}, in grades with {MIN_PROBLEMS} or more problems.")
    trusted = {g: ps for g, ps in by_grade.items() if len(ps) >= MIN_PROBLEMS}
    if not trusted:
        print(f"No grade has {MIN_PROBLEMS} problems yet, so the data can't suggest a badge.")
        return
    thin = [g for g in sorted(by_grade) if g not in trusted]
    if thin:
        left_out = ", ".join(f"{grade_label(g)} ({len(by_grade[g])})" for g in thin)
        print(f"Left out as too few to trust: {left_out}. A badge can't land there, "
              "so read any flag next to them with care.")
    ticked = {k for ps in by_grade.values() for p in ps for k in p["required"] | p["used"]}
    keys = list(badges) + sorted(ticked - set(badges))
    width = max(len(key) for key in keys)
    print(f"\n{'Technique':<{width}}  Book  Data  {'Required at that grade':<23} Flag")
    flagged = 0
    for key in keys:
        found = suggested_grade(key, trusted)
        data = grade_label(found[0]) if found else "–"
        at = f"{share(found[1], found[2])} ({found[1]} of {found[2]})" if found else ""
        if key in badges:
            book = grade_label(badges[key])
            flag = badge_flag(badges[key], found[0] if found else None, max(trusted))
            flagged += bool(flag)
        else:
            book, flag = "–", "not in the book"
        print(f"{key:<{width}}  {book:<4}  {data:<4}  {at:<23} {flag}".rstrip())
    print(f"\n{flagged} of {count(len(badges), 'badge')} flagged.")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 tools/survey_report.py <csv>")
    path = sys.argv[1]
    badges = book_badges()
    problems, empty, messages = load_problems(read_rows(path), key_aliases(badges))
    skipped = len(messages)
    messages += tick_messages(problems, badges)
    loggers, logger_messages = logger_lines(problems)
    messages += logger_messages

    print(f"{path}: {count(len(problems), 'problem')} used, "
          f"{count(skipped, 'row')} skipped, "
          f"{count(len(empty), 'empty row')} ignored")
    if empty:
        print(f"Lines with empty rows: {', '.join(map(str, empty))}.")
    fonts = sum(p["font"] for p in problems)
    if fonts:
        print(f"Converted {count(fonts, 'Font grade')} with the book's table. "
              "A V grade written without its V counts as Font.")
    if messages:
        print("\nFix these in the file:")
        for message in messages:
            print(f"  {message}")
    if not problems:
        reason = "every row has a fault" if skipped else "it has only a header row"
        sys.exit(f"survey_report: {path} has no problems to report on: {reason}.")

    print("\nLoggers:")
    print("\n".join(loggers))

    by_grade = {g: [] for g in SURVEY_GRADES}
    for p in problems:
        by_grade.setdefault(p["grade"], []).append(p)
    print("\nPer grade (shares are of that grade's problems; hold types can add up "
          "to over 100%,\nand techniques nobody ticked at a grade are left out)")
    for grade in sorted(by_grade):
        print_grade(grade, by_grade[grade])
    print_badges(badges, by_grade)


if __name__ == "__main__":
    main()
