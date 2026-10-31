# Final read: chapters 8 and 9 (Grade by grade; Your body and how you learn)

Page numbers are those of the draft PDF before these fixes (8 = pp. 193–213, 9 = pp. 215–228).

## book/chapters/08-grades.typ

- p. 193, progress box: "V3-V6" in the Lattice quote set with an en dash, as elsewhere.
- p. 194, 8.1 heading: "(Font 3–4+)" kept on one line (non-breaking space and word joiner); it broke after "3–".
- p. 200, V3 five things, item 5: "Climb slabs and overhangs every week" now matches the guide's fix, "Spend one session in four on the style you avoid, slab or steep."
- p. 204, V4–V5 five things, item 4: reworded ("Start steep moves on straight arms and drive from your feet; don't lock off.") so "off." no longer sits alone on a line.
- p. 204, V4–V5 five things, item 5: "on V3s first" now "on V3s and V4s first", as in the plan (item 4).
- p. 204, V4/V5 table, Footholds row: the semicolon after the citation was swallowed by Typst; escaped it (`\;`).
- p. 205, "What holds people at V4", item 6: "Compression" lower-cased like the other techniques in the list.
- p. 205, limiter table: the semicolon after "Straight arms (p. 70)" was swallowed; escaped it.
- p. 207, V5 techniques: "jumping to a foothold (Jumping to a foothold (p. 160))" said it twice; now "and Jumping to a foothold (p. 160)".
- p. 209, V6 techniques: "You learn to control Cutting loose and swing control" (control twice); now "You learn Cutting loose and swing control: stopping the swing and putting your feet back on…".
- p. 212, 8.10 heading: "(Font 7B and up)" kept on one line; it broke after "Font".
- p. 212, V8+ stall: "see the age notes in Section 8.6" pointed at the removed "Notes for you"; now "see Section 9.3 on training as an adult".

## book/chapters/09-considerations.typ

- p. 215, chapter title: "how you learn" kept together so "learn" no longer stands alone on the second line.
- p. 216, tall-climber list: first item "scrunchy problems" capitalised like the other items.
- p. 216, How to climb tall, item 6: "Low starts" now "Sit starts", the name used twice just above.
- p. 217, Mobility: dropped ", so keep up your yoga", a leftover of the reader's yoga background from the removed "Notes for you".
- p. 218, RED-S box: "15.8% (18 women) had lost their periods", so "only 4 of those 18" has something to refer to.
- pp. 226–227, bailing list items 3–5: "(This book's advice.)" now "(This book's suggestion.)", the marker the chapter introduction defines.

## figtools/figs_considerations.py

- Figure 13 (p. 225), frame 4: the head lay on the mat, against "chin tucked" and step 5 ("your head stays off the mat"). Head raised and tipped forward (`head=(1, 7)`, `head_tilt=60`); warn() silent. Other two figures re-rendered byte-identical.
