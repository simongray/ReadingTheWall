# Chapter-writing guide

You are turning your research dossier into a chapter of the book. The book
is typeset with Typst; illustrations are drawn with a small Python library.
Read this whole guide before starting.

## Files

- `book/template.typ` — layout and macros (`technique`, `tref`, `ix`,
  `src`, `readbox`, `notebox`, `keypoint`, `fig`). Read it.
- `book/chapters/<chapter>.typ` — your chapter (path given in your task).
- `figtools/climb.py` — the drawing library (mannequin climber, holds,
  volumes, walls, arrows, labels, panels). Read its docstrings.
- `figtools/closeup.py` — close-ups of fingers and shoes (example of
  bespoke drawings).
- `figtools/exemplar.py` — the drop-knee figure, the style reference.
- `figtools/figs_<chapter>.py` — your figure module (path given in your
  task). It must define `build(out)` that writes every figure as
  `out + "/<technique-key>.svg"` (extra figures: any descriptive name).
- `figtools/build_all.py` — finds `figs_*.py` modules automatically; no need to edit it.
- `research/KEYS.md` — the master list of technique keys across the whole
  book. Only use `tref("...")` keys from that list.

Never edit `template.typ`, `climb.py` or another chapter's files. If you
need a library feature, write a helper inside your own figure module. If
something in the template blocks you, say so in your final reply.

## Voice and spelling

- British spelling (colour, centre, metre), second person, imperative.
- Concrete: name the body part, the direction and the reason. "Turn your
  right hip to the wall so your right shoulder rises" — not "use your
  hips". No vague cues ("trust your feet", "be smooth") unless you
  immediately say what to physically do.
- Compact. Each numbered step is one or two lines. No motivational filler.
- Indoor bouldering. Mention rock or ropes only where it really helps.
- The reader is a tall, heavier adult starter who climbs V3–V4. Tall-climber
  notes are welcome where they say something specific.

## Plain language (the reader asked for this explicitly)

The reader wants natural, succinct English: no jargon left unexplained,
no long or stacked sentences. Before you finish, do a pass over every
sentence you wrote with these checks:

- **Short sentences.** Aim for under about 20 words. One idea per
  sentence. If a clause carries a fact of its own, give it its own
  sentence. Avoid joining two thoughts with ", and"; end the sentence.
- **Say it the way a coach would say it out loud** at the bottom of the
  wall. Subject first, verb next to it. No inverted or stacked clauses
  ("the hold whose edge the hand that…").
- **Active voice that names who acts:** "push your left knee down", not
  "the knee is dropped".
- **No comma chains** of short noun bursts. No fragments without a verb.
- **Explain jargon at first use in each entry or section**, in a few plain
  words, e.g. "a gaston (a hold you pull outward, elbow out, like prising
  open a lift door)". Then link the word to the glossary with
  `#jt("gaston")` (it renders as plain text plus a link). Use `#jt` at
  the first use of a jargon word per entry/section, not every time.
  Jargon includes climbing slang (beta, crux, flash, send, project, dab,
  pumped, top out, match, cut loose, comp style, setter, circuit,
  volume, macro, dual-tex, positive/negative hold, incut, rail, ape index,
  pulley, contact strength…), anatomy and physics terms, and any technique
  name used outside its own entry (those get `#tref` instead).
- **Don't say things twice,** and don't pad: no "simply", "just", "note
  that", "it is important to".
- **Keep rewrites as short or shorter** than the first draft.

The editor will build a glossary appendix from every `#jt` term, so use
the plainest common name as the term (singular, lower case unless a
proper noun) and list in your final reply any jargon terms you linked
that need a glossary definition, each with a one-line definition.

## The technique entry

```typst
#technique(
  key: "drop-knee",                       // from research/KEYS.md
  name: "Drop knee",
  aliases: ("Egyptian",),                 // other names, each indexed
  category: "body",                       // feet | body | hands | dynamic | terrain
  grade: 3,                               // V-grade where it starts to matter (0 = VB–V0, 8 = V8+)
  grade-note: [Shows up on steep V2s; from V3–V4 many overhanging problems are set around it.],
  summary: [One or two sentences: what it is and what it does for you.],
  figure: "drop-knee.svg",                // optional
  caption: [(a) … (b) …],                 // short, explains the panels
  how: [
    + Step one.
    + Step two.
  ],
  when: [
    - *Look for* concrete wall cues …
    - *Symptom:* you swing off like a door when …
  ],
  errors: [
    - Mistake and its fix.
  ],
  tall: [Optional, only if specific.],
  related: ("backstep", "flagging"),      // keys from KEYS.md
  watch: (("Channel", "Video title", "https://…"),),   // only ones you found
  sources: ("B3", "B7"),                  // IDs from your dossier source list
)
```

Rules:

- `when:` is the heart of the book. Start bullets with `*Look for*` (what
  you see on the wall before climbing) or `*Symptom:*` (what goes wrong
  when you needed this technique and didn't use it). Aim for 3–6 bullets.
- Inline citations: `#src("B3")` or `#src("B3", "B9")` after the claim.
  Cite safety claims, numbers and anything contestable. Use your own
  dossier's IDs; the editor maps duplicates later.
- Index terms in prose: `#ix("Centre of gravity")`, sub-entries with `!`:
  `#ix("Heel hook!on volumes")`. Each entry's name and aliases are indexed
  automatically; index other key terms the first time they are explained.
- Cross-references: `#tref("heel-hook")` renders "_Heel hook_ (p. 34)" with
  a link. Use them freely in prose and in `related:`.
- Order the entries in your chapter from the lowest `grade` to the highest
  (alphabetical within a grade), so the chapter reads as a progression.
- Start your chapter with a level-1 heading (`= Feet and legs`), then a
  short introduction (what the category is about and how to read it), then
  `#category-table("feet")` (auto-generated ranked table), then any short
  concepts sections (level-2 headings), then the entries. Use level-2
  headings to group entries if that helps (e.g. `== Hooking`).

## Hold direction convention (use everywhere)

A hold "faces" the direction its gripping surface points. You pull the
opposite way:

- A jug or edge faces up; you pull down; your body hangs below it.
- An undercling faces down; you pull it upward. It works best low, at
  about waist or chest height, with your feet high and pushing.
- A **sidepull** faces *away from your body*: a hold on your left with its
  gripping edge facing left is pulled to the right, toward you, with your
  body to its right, leaning away from it.
- A **gaston** faces *toward your body's midline*: a hold on your right
  whose gripping edge faces left is pulled outward to the right, away from
  you, elbow out, thumb down, as if prising open a lift door. Your body is
  on the opposite side from the way you pull.

In the drawing library the `use=` angle is exactly this facing direction.

## Illustrations

Style conventions (already built into the library — keep them):

- Back view: the climber seen from behind, facing the wall. Side view: wall
  on the right, climber facing right.
- The climber's left limbs are grey, right limbs white. Holds dark grey with
  a white lip on the grabbed surface (`use=` angle: 90 normal, 270
  undercling, 0/180 sidepull or gaston — the lip faces the way the
  grabbed surface faces, so you pull the opposite way).
- Dashed arrow = movement; bold arrow = force; `turn` = rotation; `cog` =
  centre of gravity with plumb line; `ghost=True` = earlier position;
  `step(n)` = move order; `cross` = mistake.
- Use `wall_grid` (bolt holes) on back views. Ground/mat only when the floor
  matters (sit starts, falling, jumping).
- Two panels (wrong vs right, before vs after) via `combine(...)` explain
  more than one. Keep panel captions to a few words.
- Keep the default scale (`Fig(..., scale=0.32)`) for climber figures so
  every climber is the same size. Crop the frame tightly around the action;
  a two-panel climber figure is typically 2 × 50–60 mm wide.
- Labels: few, short (two or three words), with leader lines (`label`).

Workflow: write a pose, render, LOOK at it, fix it. Render previews with:

    python3 -c "import sys; sys.path.insert(0,'figtools'); import figs_x; figs_x.build('<scratch>')"
    rsvg-convert -d 150 -p 150 -b white <scratch>/name.svg -o <scratch>/name.png

then Read the PNG. Use `Climber.warn()` to catch hands or feet that don't
reach their holds. Check that: the pose is anatomically plausible, hands
and feet are on their holds, holds are visible, labels don't sit on the
body, nothing is clipped, and the drawing actually shows the point of the
technique. Make contact sheets (`magick a.png b.png -append sheet.png`) to
save effort. Put previews in your scratchpad, never in the project folder.

Close-ups (grips, shoe contact) can be bespoke drawings; reuse
`closeup.py` helpers by importing them.

## Compiling your chapter

Make a preview file in your scratchpad, e.g.:

```typst
#import "/book/template.typ": *
#show: book.with(title: "Preview", author: "")
#include "/book/chapters/<chapter>.typ"
```

and compile with
`typst compile --root /Users/simongray/Books/Bouldering <preview.typ> <out.pdf>`,
then render pages with `pdftoppm -r 60 -png <out.pdf> <prefix>` and look
at them. References to other chapters' keys show as red `[?key]` in a
standalone preview; that is expected. Your own keys must resolve.

## Sources file

Also write `research/<letter>-sources.yml` in Hayagriva format, one entry
per source ID you cite, keyed by the ID:

```yaml
B3:
  type: web           # web | article | video | book | report | thesis
  title: "How to drop knee"
  author: ["Gresham, Neil"]        # or an organisation as a single string
  date: 2021
  parent:
    title: "UKClimbing"             # site, journal or channel
  url:
    value: "https://…"
    date: 2026-10-30              # access date
  note: "Video"                    # optional
```

For journal articles use `type: article` with `parent: {type: periodical,
title: "Journal name", volume: …, issue: …}` and `serial-number: {doi: "…"}`
where known. Only include fields you actually know.

## Exemplar entry

```typst
#technique(
  key: "drop-knee",
  name: "Drop knee",
  aliases: ("Egyptian",),
  category: "body",
  grade: 3,
  grade-note: [Shows up on steep V2s; from V3–V4 many overhanging problems are set around it.],
  summary: [You stand on a foothold out to the side and rotate that knee down and inward, so the hip on the same side turns to the wall. Both feet press outward against each other, which pins your hips to the wall and frees the same-side hand to reach.],
  figure: "drop-knee.svg",
  caption: [(a) Square on, the right hand falls short. (b) Dropping the right knee turns the right hip in and raises the right shoulder.],
  how: [
    + Place the foot on a hold about hip height, out to the side, on the outside edge or the toe.
    + Put the other foot on a hold on the opposite side, so the feet can push away from each other.
    + Rotate the high knee down and inward toward the other foot. The hip on that side turns to the wall.
    + Push outward through both feet. The opposition holds you, so the holding arm can stay straight.
    + Reach with the hand on the dropped-knee side.
    + Before standing up out of it, turn the knee back up. Don't stand up while the knee is twisted.
  ],
  when: [
    - *Look for* an overhang with footholds on both sides at roughly hip height.
    - *Look for* a long move on one side when the other hand only has a sidepull.
    - *Look for* two footholds that face away from each other, such as the two sides of a volume.
    - *Symptom:* square on, you swing off like a door the moment one hand lets go.
    - *Symptom:* on steep ground your hips sag and all the weight goes to your arms.
  ],
  errors: [
    - Dropping the knee on a foothold that is too low: there is no room for the knee, so you just twist.
    - Forgetting to push with the other foot. Without opposition the position doesn't hold.
    - Twisting hard into a deep drop knee on a strenuous move; it loads the knee (meniscus) #src("B?").
  ],
  tall: [Long legs let you drop-knee between footholds that are far apart, but a deep drop knee on steep ground can jam your knee against the wall: pick a slightly higher foothold.],
  related: ("backstep", "flagging", "twist-lock", "barn-door"),
  sources: ("B?",),
)
```

## Final reply

When finished, reply in under 200 words: files written, number of entries
and figures, anything you could not resolve, and any claims in your
chapter that a fact-checker should look at first.
