# Gym survey

The book's grade badges and its "What problems look like" descriptions are
judgement. This survey can replace them with counts from real gym problems.
Nobody has collected any yet.

You need a phone with a spreadsheet app and a level app. Copy
`research/gym-survey-template.csv`, add a row per problem and export it as CSV.
Record nothing about other climbers: no names and no photos of people.

## Choosing problems

Aim for 200–300 problems across two or three gyms, with a similar number at
each grade from V0 to V6: 15 per grade in each of two gyms (210 problems), or
14 in each of three (294). Use gyms that tag each problem with one grade, since
a circuit that spans several grades can't place a badge.

Walk the walls from the door in one direction, read the tags in order and log
every third problem. Once a grade has its quota, pass over it, then go round
again for grades still short. Don't skip a dull problem or one you can't climb.
Spread each gym over two visits, either side of a reset if you can.

## What to record

| Column | What to write |
|---|---|
| `gym`, `date` | A short code such as `A`, and the day as `YYYY-MM-DD` |
| `grade` | The grade as tagged, e.g. `V3` or `6A` |
| `wall_angle` | The band that covers most of the hand moves: `slab` (leans back), `vertical` (within 5°), `slight` (6–20° overhanging), `moderate` (21–35°), `steep` (36–50°) or `roof` (over 50°) |
| `hand_moves` | How many times a hand lands on a hold after the start holds, matches included |
| `hold_types` | The shape of each handhold, separated by spaces: `jug`, `edge` (takes your fingers to the first joint or deeper), `crimp` (fingertips only), `sloper`, `pinch`, `pocket`, `volume` |
| `sit_start`, `top_out` | `yes` or `no` |
| `required`, `used_by_choice` | Technique keys from the list below, separated by spaces, or empty |
| `basis` | `climbed`, `watched` (someone about your size climbed it) or `read` (you judged it from the floor or from the moves you could do, so the ticks are guesses) |
| `logger` | Your code of up to three characters, never a name |
| `height_band`, `reach_band` | Once per logger, on your first row only: `under-160`, `160-169`, `170-179`, `180-189` or `190-plus` (cm). Reach is arm span, fingertip to fingertip. Never write an exact figure. |

## Required or used by choice

A technique is **required** when there's no way up the problem without it for
your size. It's **used by choice** when you used it, or would, but another way
works. If you can't tell, tick it as used by choice. Your height changes the
answer: a tall logger may reach statically where a small logger has to jump, and
may have no room for a position a small logger fits into. So each tick speaks
only for the logger's bands.

A grip counts as required only when no other grip holds. Habits such as
`straight-arms` and `weight-shift` rarely pass the test, so expect flags on
them: their early badges are a teaching choice that the survey can't settle.

## Technique keys

Corners tick `stemming`, volume mantles `mantle`, hip pops `deadpoint`,
counter-kicks `cutting-loose`, and laches, paddle dynos, tic-tacs and double
clutches `comp-moves`. Don't tick `sit-start` or `top-out`, because a `yes` in
their own columns counts as required.

- Feet: `precise-footwork`, `edging`, `front-pointing`, `smearing`, `high-step`, `rockover`, `pivoting`, `foot-swap`, `hand-foot-match`, `toe-pull`, `heel-hook`, `toe-hook`, `bicycle`, `heel-toe-cam`, `knee-bar`
- Body: `weight-shift`, `straight-arms`, `frog`, `barn-door`, `matching`, `stemming`, `hip-turn`, `flag`, `cross-through`, `layback`, `backstep`, `back-flag`, `drop-knee`, `pre-loading`, `body-tension`, `lock-off`, `opposition`, `bumping`, `twist-lock`, `inside-flag`, `compression`
- Hands: `jug`, `sidepull`, `half-crimp`, `open-hand`, `undercling`, `palming`, `mantle`, `sloper`, `pinch`, `wrap`, `gaston`, `regrip`, `pocket`, `thumb-catch`, `full-crimp`
- Dynamic: `deadpoint`, `hip-pump`, `jump-start`, `lunge`, `dyno`, `latching`, `cutting-loose`, `run-and-jump`, `double-dyno`, `campus-move`, `foot-catch`, `pogo`, `comp-moves`
- Terrain: `slab`, `volume`, `traverse`, `top-out`, `overhang`, `arete`, `sit-start`, `roof`, `dynamic-slab`

## How the results feed the book

- **Badges.** A technique's badge is the lowest grade where it's required on at
  least 10% of the problems, and on at least 3, counting only grades with 20 or
  more problems (this book's suggestion). One in ten fits what the badge
  promises: below it you can usually get away without the technique, and from
  there you keep meeting problems that need it. A 5% share is one or two
  problems at these sample sizes, so one odd problem could set a badge. At 25%
  few techniques would earn one, because each problem needs only a few of the
  keys (judgement).
- **Flags.** Run `python3 tools/survey_report.py <csv>` from the repository
  root. Treat a flagged badge as a reason to look, not as a correction: 4 ticks
  in 36 problems (11%) has a 95% interval of about 4–25%.
- **Descriptions.** Rewrite each "What problems look like" from that grade's
  moves, wall-angle mix and hold-type mix. Anything the survey doesn't record,
  e.g. foothold size, stays marked (judgement). Say how many gyms and problems
  the figures come from, and which height bands logged them.
