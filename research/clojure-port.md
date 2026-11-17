# Porting the Python to Clojure or babashka

An analysis, written on 2026-11-17. Nothing was ported. The numbers come from a
survey of the code at `46e275b` and from timing a build in a scratch copy.

## Verdict

The port is feasible, and babashka can run all of it. The website builder and
the tools are a plain port. The figures are the real work: 15,000 of the 20,000
lines, with 136 drawings to check by eye afterwards. Byte-identical SVGs are
not a realistic target, so the port needs a visual comparison instead.

## What there is

| Folder | Lines | What it does |
|---|---:|---|
| `figtools/` | 15,138 | the drawing library and the figures |
| `tools/` | 2,128 | checks and generators around the build |
| `website/` | 2,690 | the site builder |

No third-party packages are used. The code calls `typst`, `git`, `pdftotext`,
`pdftoppm`, `rsvg-convert` and `magick` as commands, which babashka can do too.

## What babashka lacks

Tested on bb 1.13.229:

- **A TOML parser**, for `book/figure-alt.toml`. Move the file to EDN instead.
- **A tar reader**, for `git archive` in the site builder. Use
  `git archive --format=zip`, or call `tar`.
- **`difflib` and `statistics`.** Both are used for a few lines and are easy to
  write.
- **Python's random generator.** 116 of the 136 SVGs place grain and stipple
  dots from generators seeded with a string. A port either implements Mersenne
  Twister with Python's seeding or accepts dots in other places.

Everything else has a built-in match: Jsoup for the HTML export, cheshire,
`babashka.fs`, `babashka.process`, http-kit, `MessageDigest` and `CRC32`.

## Speed

A build takes 25 s in Python. The hand model takes 79% of that: it fills a grid
of about 11 million cells to find each hand's outline. Inverse kinematics, the
pose checks and the colour pass together take under half a second.

babashka ran the hand model's inner loop 3 to 3.5 times slower than Python. A
straight port would therefore build in about 80 s. Three ways round it, best
first:

1. **Cache each hand by a hash of its joint angles.** The hands change rarely,
   so most builds would skip the grid.
2. Run the figure build on the JVM, where the same loop with primitive arrays
   is much faster than Python. Code that sticks to what babashka supports runs
   on both.
3. Replace the grid with authored outlines, as some hands already are.

## Why the SVGs won't be byte-identical

- bb's `format` rounds 100 of 3.4 million numbers differently from Python.
- `sin`, `cos`, `atan2` and `hypot` differ in the last bit on 4–18% of inputs,
  and bb has no `StrictMath`. A one-bit nudge changed 14 of the 136 SVGs.
- The random dots, as above.

So compare pictures: render both builds with `rsvg-convert` and count the
pixels that differ. `tools/check_alt.py` stores a hash of each grey drawing, so
all 115 hashes need writing once after the port. The descriptions stay valid if
the drawings look the same.

There is no unit-test suite to guard a port. `check_hands.py` and the pose
warnings (`Climber.warn`) are the only checks on the drawings, so port those
first.

## What changes shape

- 19 classes. `Fig` collects items in a list and sorts them when it writes the
  SVG. `Climber` solves its joints and then mutates itself. In Clojure both
  become plain data and pure functions: a figure is a vector of items, and
  solving returns a new map with the joints in it.
- `Climber` takes 27 keyword arguments, and 27% of all calls in the figure
  modules pass keywords. Those are maps already.
- A few tricks have no equivalent and aren't needed: copying a climber and
  overwriting its fields to draw a ghost, reading the call stack to name a
  figure in a warning, and patching functions in `check_hands.py`.
- `paint.py` recolours finished SVG text with regexes, and `climb.py` reads its
  own SVG strings back to drop dots under a cut. With figures as data, both
  passes can work on the data.

## An EDN format for the figures

Today a figure is a Python function. Of the 110 figure functions, only 11 are
straight sequences of calls with literal arguments. The rest compute points,
loop over panels or branch per panel. But the loops and branches are regular:

- `for k in range(2): shared holds; if k == 0: … else: …` builds two panels
  that share their holds (47 branches in 31 functions).
- A label or arrow is placed from a joint the solver found (122 lookups in 42
  functions).
- A point is another point plus an offset (593 vector calls).

Three things in the data cover these, and none needs code:

1. **Named points**, so that a hold and the hand on it share one coordinate.
2. **Point expressions** in a small closed vocabulary: `[:grip p]`,
   `[:stand p]`, `[:joint climber joint]`, `[:cog climber]`, `[:+ a b]`,
   `[:lerp a b t]`. They are resolved after the climbers are solved.
3. **A base that panels and frames merge into**, so a panel says only what
   differs.

The back flag, which is 30 lines of Python today:

```clojure
{:id       "back-flag"
 :view     :back
 :frame    [-100 54 76 276]
 :points   {:lh [-36 262], :lf [-30 70], :t [36 238]}
 :holds    [{:kind :jug, :at :lh, :use 180}
            {:kind :jug, :at :t}
            {:kind :foot, :at :lf}]
 :climbers {:c {:hips    [-30 156]
                :lean    3, :bend 10, :turn 0.2
                :lh      [:grip :lh {:use 180}]
                :rh      [:grip :t]
                :lf      {:at [:stand :lf], :style :back}
                :rf      {:at [-70 62], :angle 200, :contact :edge}
                :knees   {:l :out, :r :down}
                :elbows  {:l :out}
                :leg-len {:l 0.95}
                :head    [2 1]
                :order   [:lleg :torso :rleg :larm :rarm]}}
 :marks    [{:mark :hinge
             :from [:+ [:grip :lh {:use 180}] [0 -6]]
             :to   [:stand :lf]}
            {:mark :cog, :of :c, :plumb-to 58}
            {:mark :label, :text "hinge", :at [-74 250], :to [-39 236]}
            {:mark :label, :text "right leg behind", :at [8 70]
             :to   [:+ [:lerp [:joint :c :rkn] [:joint :c :ran] 0.3] [2 0]]}]}
```

A two-panel figure adds `:panels`, each merged into the map above:

```clojure
{:id     "flag"
 :base   {:view :back, :points {...}, :holds [...]}
 :panels [{:caption "no flag: door opens",       :climbers {...}, :marks [...]}
          {:caption "side flag: leg balances",   :climbers {...}, :marks [...]}]}
```

A film strip is the same with `:frames`. A ghost is a climber with
`:ghost-of :c` and the fields that differ.

### What it buys

- Figures become data that other tools can read. The alt text can sit in the
  figure's map (`:alt`), which removes the TOML file. The dark copy for the
  website can be drawn from the same data instead of from the finished SVG.
- A hold knows its entry's grade, so the colour pass reads it from the data.
  The colour-coded library runs under babashka as it is, and its
  `epaper/same-grey?` does what `paint.py`'s own sums do now.
- The pose checks can run on the data before anything is drawn.

### What it doesn't cover

About a quarter of the drawings are not poses on a wall: the cover's pelican,
the hand model and the authored hands, the shoe close-ups, the icons and the
legend. These stay code. They can still return the same item vectors, so one
writer turns everything into SVG.

Helpers that build a pose from parameters (`_back_flagger`, `rock_up_poses`)
stay functions too. A figure's map can name one: `{:pose [:back-flagger {...}]}`.

## A route, if it goes ahead

1. `tools/` and `website/` to babashka. They are 4,800 lines, self-contained,
   and the site build's output can be compared file by file.
2. The pose solver, the pose checks and the SVG writer from `climb.py`, as pure
   functions that take the EDN above. Check them against Python's solved
   joints, which are numbers and compare exactly enough.
3. The figures, a chapter at a time, as EDN, each compared with its Python
   drawing as pixels.
4. The hand model and the other bespoke drawings last, with the hand cache.

The site builder reads each edition's own `build.sh` to find the generators to
run, so the Python has to stay in the repository for as long as the site builds
editions 1 to 3 from their tags.
