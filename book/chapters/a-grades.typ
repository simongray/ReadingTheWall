#import "../template.typ": *

#heading(level: 1, numbering: none)[Grade conversion] <grade-conversion>

#ix("Grades!V-scale and Font", main: true)
#ix("Font grades")
Gyms in the US grade boulders on the #jt("V-scale"). Gyms in the UK use the V-scale or the #jt("Font grade", body: [Font scale]) (short for Fontainebleau) #src("F26"). Many other European gyms use Font. The table follows Mountain Project's conversion, which matches Wikipedia's table #src("F22", "F23"). The bands on the right come from 99Boulders #src("F24").

#{
  set par(justify: false)
  let rows = (
    ("VB", "3", "Beginner"),
    ("V0", "4 (V0− = 4−, V0+ = 4+)", "Beginner"),
    ("V1", "5", "Beginner"),
    ("V2", "5+", "Beginner"),
    ("V3", "6A (V3+ = 6A+)", "Intermediate"),
    ("V4", "6B (V4+ = 6B+)", "Intermediate"),
    ("V5", "6C (V5+ = 6C+)", "Intermediate"),
    ("V6", "7A", "Advanced"),
    ("V7", "7A+", "Advanced"),
    ("V8", "7B (V8+ = 7B+)", "Advanced"),
    ("V9", "7C", "Expert"),
    ("V10", "7C+", "Expert"),
    ("V11", "8A", "Expert"),
    ("V12", "8A+", "Expert"),
    ("V13", "8B", "Elite"),
    ("V14", "8B+", "Elite"),
    ("V15", "8C", "Elite"),
    ("V16", "8C+", "Elite"),
    ("V17", "9A", "Elite"),
  )
  align(center, table(
    columns: (auto, auto, auto),
    inset: (x: 8pt, y: 5pt),
    align: (center, left, left),
    table.header(th[V-scale], th[Font], th[99Boulders band]),
    ..rows.map(r => (strong(r.at(0)), r.at(1), r.at(2))).flatten(),
  ))
}

*Caveats.*
- *From V3 to V5, one V-grade covers two Font grades.* V3 covers 6A and 6A+, V4 covers 6B and 6B+, and V5 covers 6C and 6C+. So your first V5 in a Font gym is a 6C. From about 7A up, the scales match almost one to one #src("F24", "F23").
- *Charts disagree at the low end.* At least one popular chart maps V2 to 6A/6A+, V3 to 6B and V4 to 6B+, up to a full Font grade harder than this table #src("F25"). Wikipedia calls all such conversions "only ever indicative" #src("F23").

#heading(level: 2, numbering: none)[Circuits and colours]

#ix("Circuits", main: true)
Some walls group problems into #jt("circuit", body: [circuits]) instead of grading each one: sets marked by one hold or tag colour, covering one grade or spanning two or three. The British Mountaineering Council's example has purple for V0–V2 and yellow for V3–V5 #src("F26"). Treat a circuit as a range. In a V3–V5 circuit, the problem you can't do may be the V5, and the one you #jt("flash") (climb first go) may be the V3. Chapter 2 explains how to calibrate yourself in a new gym.

This book's grade tabs borrow their colours from the circuits at Boulders, a Danish gym chain, and an entry's holds take the same colour as its tab. On a greyscale screen the tabs darken as the grade rises instead. Your gym's colours will differ.
