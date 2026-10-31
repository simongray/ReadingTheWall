# Index log

Pass by the indexer agent, 2026-10-31. Check with `./build.sh` and the last
five pages of the PDF.

## What changed

- **About 290 new `#ix` markers** across chapters 1–9 and the
  troubleshooting appendix (359 in the chapters now, 66 before). No prose
  was changed. The count is above the 150–250 aim; most of the excess is
  people and "Tall climbers" sub-entries.
- **Index length:** 4 pages before, 5 now (book 213 → 214 pages).
- **`book/template.typ`, `make-index`:**
  - Terms that differ only in case share one entry, shown with the
    capitalised spelling. Before, "Barn door 46" and "barn door 177" (the
    glossary entry) were listed as two entries.
  - Sorting ignores case and accents, and sub-entries sort directly under
    their main entry. Before, "Deadpoint" was printed twice, around the
    glossary entry.
  - `ix-merge` files glossary terms under the index's spelling ("flash" →
    Flashing, "volume" → Volumes, "the line" → Line, the, and so on). Add a
    line there if a new glossary term duplicates an index entry.
- **Existing markers renamed** so entries merge: "Flash" → Flashing,
  "Reading the wall!…" → "Route reading!…", "Knee injuries" →
  "Injuries!knee" (main), "Pulley injury" → "Injuries!pulley" (main) plus
  "Pulley!injury", "Falling!technique" → "Falling!how to land".

## Conventions

Check these before adding a marker, so new markers merge with the old ones.

| Kind | Spelling used |
|---|---|
| People | Surname, first name: "Gresham, Neil", "Hooper, Jason" (Hooper's Beta), "Hörst, Eric", "Rowland, Dave", "Hampton, Kris", "Schweizer, Andreas", "Feehally, Ned", "Ondra, Adam", "MacLeod, Dave", "Torr, Ollie", "Randall, Tom", "Gill, John", "Güllich, Wolfgang". Organisations: "Lattice Training", "DAV", "World Cup", "MoonBoard". People are indexed in running text and grade notes, not in video credits. |
| Studies | "Studies!<topic>", for example "Studies!knee injuries" and "Studies!injuries from falls" |
| Injuries | "Injuries!<site>": ankle, elbow, finger, hamstring, knee, lumbrical, pulley, shoulder, wrist, from falls |
| Hold types | The technique name, singular, with sub-entries: "Sloper!body position", "Jug!…", "Pocket!as a foothold" |
| Terrain | The technique name: "Overhangs!hip position", "Volumes!standing on", "Slab technique!small steps", "Roofs!toe hooks", "Arêtes!heel hooks", "Vertical walls" |
| Body | "Hips!…", "Shoulders!…", "Wrists", "Ankles", "Mobility!hips", "Hand size", "Body weight!…", "Age!…" |
| Situations | "Tall climbers!<technique or situation>", "Short climbers!…", "Feet popping off", "Resting on the wall", "Falling!…", "Bailing!…", "Downclimbing!…" |
| Practice | "Warm-up!…", "Drills!…", "Projecting!…", "Flashing!…", "Route reading!…", "Experts and novices!…", "Setting!…", "Grades!…", "Plateau!…" |

Sub-entries are lower case. `main: true` marks the page that explains the
term: Opposite hand and foot (ch. 1), Static and Dynamic movement (ch. 1),
Grip endurance, Injuries!pulley (ch. 5), Vertical walls (ch. 7), Mobility,
Body weight!load on the fingers, Tendon!adaptation, Injuries!knee and
Falling!how to land (ch. 9).

## Left alone

- Alias entries print a page number after "(see …)". That is how the
  template builds aliases.
- Glossary-only entries stay lower case ("beta 177", "crux 177"). Where I
  added sub-entries to them, the head keeps the glossary spelling.
- No "Kettle, John": the book doesn't mention him.
