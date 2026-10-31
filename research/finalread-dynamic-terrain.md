# Final read: chapters 6 (Dynamic movement) and 7 (Terrain)

Page numbers refer to the draft PDF of 31 October (10:06).

## book/chapters/06-dynamic.typ

- Intro: "comp style setting" → "comp-style setting" (compound adjective).
- Static or dynamic?: "into a Volumes (p. 180) (a big bolt-on shape)" → "into a volume (a big hollow shape bolted to the wall)": entry name as a noun, double brackets, glossary wording.
- Static or dynamic?: "as on a Slab technique (p. 175) (a wall that leans back)" → "as on a slab (a wall that leans back)".
- Where "deadpoint" comes from: dropped the unsourced "often credited to" framing: "Wolfgang Güllich studied the idea in the 1980s".
- Cutting loose, tall note: "Under a low Roofs (p. 186)" → "Under a low roof (p. 186)".
- Dyno, mistakes: "Learning on a Slab technique (p. 175)" → "Learning on a slab (p. 175)".
- Latching, step 3: restored the semicolon after `#tref("full-crimp")`, which Typst swallowed (now `\;`).
- One-handed dyno, step 6: nested brackets "(Jumping to a foothold (p. 160))" → "… or hook a foot. See Jumping to a foothold (p. 160)."
- One-handed dyno, symptom: "Your hips were square. Your throwing shoulder was low." (repeated the symptom before it) → "Square hips kept your throwing shoulder low."
- Run-and-jump, summary: "or a Volumes (p. 180)" → "or a volume (p. 180)".
- Campus move, look for: "a Roofs (p. 186)" → "a roof (p. 186)".
- Jumping to a foothold, look for: "a foothold or Volumes (p. 180) edge" → "volume".
- Tic-tac, look for: "a corner, arête or Volumes (p. 180)" → "volume".

## book/chapters/07-terrain.typ

- How the wall angle changes your body: "A volume (p. 180) (a large bolt-on shape)" → "A volume (a big hollow shape bolted to the wall)".
- Vertical walls: "When they don't, Side flag (p. 68) instead of swapping feet" → "flag (p. 68)".
- Corners, step 5: "Layback (p. 66) the edge" → "layback (p. 66) the edge".
- Corners, look for: side wall that is "in" → added "(part of the problem)" (unexplained jargon).
- Volumes, summary: "large bolt-on shapes" → "big hollow shapes bolted to the wall" (glossary wording).
- Volumes, aliases: dropped "features" (it collided with the glossary term "feature" in the index).
- Volumes, step 3: "Grab it as a Pinch" → "pinch".
- Arêtes, step 2: "Where the face is blank, Layback (p. 66)." → "layback (p. 66)".
- Arêtes, step 6: "tense your core" → "tense your core (the muscles around your trunk)", linked to the glossary.
- Sit starts, step 1: "Sit close to the wall, bottom near it" (said it twice) → "Sit with your bottom close to the wall".
- Sit starts, step 3: "a wide Frog position works too" → "frog position".
- Dynamic slab, step 8: misplaced clause "… instead of jumping off, where the fall is safe" → "Where the fall is safe, try to ride out a foot slip instead of jumping off."

## figtools/figs_dynamic.py

- deadpoint: frame 14 units wider on the left; "grab at the top" no longer crosses the wall line and hand; the "hips sag out" leader dot no longer sits inside the text.
- cutting-loose (a): "feet cut" moved off the dashed arrow.
- latching (c): frame shifted right; "shoulder down" no longer sits on the torso outline.
- double-clutch (a): the right hand now stops visibly short of hold 2 (it looked already caught, against the caption); its move arrow now shows.
- foot-catch: "toe hooks far side" moved off the torso; "swing" moved off the right shin.
- pogo (b): "left foot pushes" moved off the standing leg; leader now points at the shoe.
- tic-tac: label lowered into the volume's bottom facet, clear of the facet lines (7 pt); curly apostrophe.
- paddle-dyno: curly apostrophe in "tap, don’t hold", as in the text.

## figtools/figs_terrain.py

- corner (a): "palms and feet press out" crossed the fold line; now two lines on the left wall.
- arete (a): "feet push right" moved off the edge line; (b) "heel round" moved off the edge line (7 pt).
- volume (a): "too close to the wall" moved clear of the wall line and the volume's edge.

warn() silent; figures rebuilt into book/figures; test compile has no "[?".

## Handed back

- "(our judgement)" (ch. 3, 6, e.g. pp. 133, 139) vs "(judgement)" (ch. 2, 7, 8, troubleshooting, e.g. pp. 171, 173): a book-wide choice. Not changed.
- p. 191, dynamic slab symptom: "topple backwards, because your body arrived too close to the wall". It matches the dossier (E5) but reads backwards for a slab. Worth a fact-check.
- Grade-section heads wrap one word onto a second line (p. 133 "moves", p. 154 "coordination", p. 168 "body"). That's the heading measure in the template.
- p. 149, latching: the "Tall climbers." note is about heavier climbers.
