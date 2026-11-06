#import "../template.typ": *

= Body positioning
#fit-pages[

This chapter is about where you put your hips, shoulders and free limbs. A good position puts your weight on your feet, lets each hold work in the direction it faces and stops you swinging off the wall. Chapter 1 explains the mechanics behind this, such as your #jt("centre of gravity") (the point your weight acts through).

Each entry starts at the grade where you start to need the technique indoors. No syllabus fixes these grades, so they are judgement. Each grade note gives the evidence.

If you're tall, you reach many holds square on that shorter climbers must twist for.#ix("Tall climbers!hidden technique gaps") That hides missing technique until the holds get small or far apart (see Chapter 9). Practise the V3 and V4 entries on problems you can already climb square on.

#category-table("body")

== Reading the wall for body position

#ix("Route reading!body position")
Run through these checks on the ground, before you pull on. Each one points to an entry in this chapter.

+ *Check the wall angle.* It sets your default position#ix("Wall angle!body position") #src("B17", "B44", "B8").

  #table(
    columns: (auto, 1fr, auto, auto),
    table.header([*Wall*], [*Start with*], [*Hips*], [*Arms*]),
    [#tref("slab", body: [Slab])], [Square on. Shift your weight over each foot.], [Out, over the feet], [Bent is fine],
    [Vertical], [Square on. Twist only if no front-on option works.], [Over the feet], [Stand tall],
    [Overhang 10–30°], [#tref("hip-turn"), #tref("backstep")], [One hip on the wall], [Straight],
    [Steep 30–75°], [#tref("drop-knee"), #tref("twist-lock")], [Locked in], [Straight],
    [#tref("roof", body: [Roof])], [#tref("body-tension"), hooks], [Hanging], [Straight],
  )

+ *Name the hinge.* Pick the hand that will stay on and the foot you will stand on. The line between them is the #jt("hinge"): your body can rotate around it. #ix("Hinge") Opposite hand and foot#ix("Opposite hand and foot") are stable #src("B11"). On the same side, expect a #tref("barn-door") and plan a flag or a foot swap #src("B35").

+ *Read the holding hold.* Its direction tells you which hip goes to the wall.
  - A #tref("sidepull") faces away from your body. A right-hand sidepull on your right faces right; you hang to its left. Turn in your left hip, backstep your left foot and reach with your left hand #src("B14", "B38").
  - A #tref("gaston") faces your midline. You pull it outward, elbow out. Stay squarer and use the inside edge of the opposite foot #src("B14"). Don't backstep off it #src("B38").
  - An #tref("undercling") faces down. Put your feet high and keep the arm straight #src("B30").
  - A #tref("sloper"): sit your hips low, keep your arms straight and your trunk tight#ix("Sloper!body position") #src("B31").
  - Two holds that face away from each other: squeeze them. See #tref("compression").
  - Two surfaces that face each other: push them apart. See #tref("stemming").
  - A vertical edge or #tref("arete", body: [arête]): see #tref("layback").

+ *Place your feet against the line.* #jt("the line", body: [The line]) is the vertical line under the hold your holding hand pulls #src("B38"). #ix("Line, the")
  - A foothold on the line, or a little beyond it away from your reach, at knee height or higher: #tref("backstep").
  - A foothold on the reaching side of the line, with a second foothold wide on the other side: #tref("drop-knee") #src("B40").
  - All footholds on the holding-hand side, too high or small to backstep: #tref("back-flag") #src("B42", "B44").
  - No foothold where the free foot would help: #tref("flag") or #tref("back-flag").

+ *Measure the distance.*
  - A target at the limit of your reach: #tref("hip-turn", body: [turn the hip in]) and roll the shoulders.
  - Beyond #jt("static") reach (reach without a jump), with a small hold on the way: #tref("bumping").
  - A hold too small to share: cross instead of #tref("matching", body: [matching]).

+ *After a failed attempt, read the symptom.* Each entry lists its symptoms. The troubleshooting appendix collects them.
]

== V0–V1: weight, straight arms and the basic stance

#technique(
  key: "weight-shift",
  name: "Weight shift",
  aliases: ("weighting the foot", "weight transfer"),
  category: "body",
  grade: 0,
  grade-note: [The UK's coach training lists weight transfer as a movement skill #src("B2"). Gresham#ix("Gresham, Neil") names a centred, unshifted body as the first habit of off-balance climbers #src("B22").],
  summary: [Before you stand on a foot, move your hips sideways until they sit over it, then stand up on that leg alone. Your hips zig-zag up the wall #src("B22"), as the balance figure in Chapter 1 shows.],
  how: [
    + Place the foot exactly. Press a little weight into it first, so the rubber bites #src("B17").
    + Slide your hips sideways until your belly button is over that foot.
    + On a #tref("slab", body: [slab]), also push your hips out from the wall so they sit above the foot #src("B17").
    + Stand up on that leg. Let the other foot go light.
    + Reach only once you are standing. Feet first, then hands #src("B22").
    + On the next move, shift your hips the other way.
  ],
  when: [
    *Look for*
    - a foothold out to one side of your body.
    - a slab or a vertical wall. Nearly every move there starts with a shift.

    *Symptoms*
    - Your foot skates or bangs onto the hold as you stand on it #src("B22").
    - You stand up on both feet at once while your hands pull hard.
    - You reach and your heels lift off the footholds #src("B22").
  ],
  errors: [
    - Hauling with an arm while the foot only follows. Push with the leg. Let the arm only steady you #src("B11").
  ],
  related: ("barn-door", "frog", "straight-arms", "precise-footwork"),
  sources: ("B2", "B9", "B11", "B17", "B22"),
)

#technique(
  key: "straight-arms",
  name: "Straight arms",
  aliases: ("straight-arming", "hanging on your skeleton"),
  category: "body",
  grade: 0,
  grade-note: [Learn it from your first session (this book's suggestion): when you pause on a steep wall, hang on nearly straight arms with your shoulders set, and on a vertical wall stand tall instead. It matters more on your first overhangs, and on V3–V4 overhangs it can decide whether you run out of strength (judgement). The UK's coach training lists it as a way to find a rest #src("B1").],
  summary: [You hang with your elbows straight or nearly straight, so your arm muscles work less #src("B50"). You move by pushing with your legs and turning your hips, not by pulling #src("B12", "B22"). Chapter 1 shows the difference in a figure.],
  how: [
    + Between moves, let your elbows straighten. Keep a slight bend of a few degrees #src("B23").
    + Set your shoulders. Draw your shoulder blades a little down, away from your ears#ix("Shoulders!setting the shoulder blades") #src("B28", "B50").
    + On steep ground, lower your hips until your arms are nearly straight #src("B22"). Keep the hips close to the wall #src("B36").
    + Start every move with your legs. Push with your feet first. Bend your arms only after the legs have started #src("B27").
    + Later, to gain height, turn the hip on the reaching side to the wall instead of bending the arm #src("B43", "B54"). See #tref("hip-turn").
    + Rest and shake out one arm at a time from a straight-arm stance #src("B12").
    + Bend your arms for the end of a move, a precise catch or a #tref("lock-off"). When you catch, tense your shoulders #src("B50").
  ],
  when: [
    *Look for*
    - an overhang with #tref("jug", body: [jugs]), long edges, sidepulls or underclings you can lean off #src("B12", "B56").
    - any pause on steep ground: reading the next move, chalking, shaking out #src("B12").
    - an #tref("undercling") near your waist #src("B30").

    *Symptoms*
    - Your biceps burn on easy overhangs.
    - Your forearms #jt("pump", body: [pump up]) (swell and weaken) before the #jt("crux") (the hardest move). Coaches put this down to bent arms #src("B22", "B36").
    - Your elbows point out sideways #src("B28").
  ],
  errors: [
    - Sagging onto fully straight arms with slack shoulders. The coach Neil Gresham says this strains the shoulders #src("B23"). One physiotherapist calls it a risky habit, and says he has seen it contribute to a shoulder#ix("Injuries!shoulder") dislocation #src("B50"). We found no study that measures it.
    - Sinking low on a vertical wall. It moves weight from your feet to your fingers #src("B8"). Stand tall there and accept a slightly bent arm.
  ],
  related: ("pre-loading", "hip-turn", "twist-lock", "lock-off"),
  watch: (
    ("Hooper’s Beta","Why You Have NO POWER On Overhangs – Coaching w/ Dan #3", "https://www.youtube.com/watch?v=TZxhg6NMwaI"),
    ("Hooper’s Beta","Inaccurate Climbing Advice I Hear Every Day (EVEN FROM PROS!)", "https://www.youtube.com/watch?v=xy6TeervBKs"),
  ),
  sources: ("B1", "B8", "B12", "B22", "B23", "B27", "B28", "B30", "B36", "B43", "B50", "B54", "B56"),
)

#technique(
  key: "frog",
  name: "Frog position",
  aliases: ("square on", "front-on", "frogging", "frog legs"),
  category: "body",
  grade: 1,
  grade-note: [Square on is the default from your first climb. A deliberate frog, knees turned out, matters on V1–V2 high steps.],
  summary: [You face the wall with both hips parallel to it and stand on the inside edges of both feet. Your knees turn out to the sides, so your hips can come close to the wall between them.],
  figure: "frog.svg",
  caption: [(a) Knees out, both feet on their inside edges, hips between the feet. (b) Side view. Knees pointed at the wall keep the hips out. (c) Knees out let the hips come in.],
  how: [
    + Stand on two footholds at about the same height, shoulder width or wider.
    + Use the #tref("edging", body: [inside edge]) of each shoe: the big-toe side #src("B55").
    + Turn each foot so it lies along the wall, heel turned in. This keeps your hips square and close #src("B38").
    + Turn your knees out to the sides, as in a yoga squat.
    + On a vertical or steeper wall, bring your hips in between your knees. On a slab, keep them over your feet #src("B17").
    + To step up, lift one foot to a hold near hip height, knee out. Move your hips over it and stand up #src("B65"). See #tref("rockover").
  ],
  when: [
    *Look for*
    - a slab or a vertical wall #src("B44").
    - footholds side by side at about the same height.
    - handholds straight above you that you pull down: edges, #jt("crimp", body: [crimps]) (small edges you hold on your fingertips) and #tref("jug", body: [jugs]).
    - a high foothold right in front of your hip.

    *Symptoms*
    - On an overhang your hips drag you off and your feet won't stay loaded. Frogging is one fix #src("B61"). Turning a hip in usually works better there #src("B22").
    - Your knees bump the wall and push your hips out.
  ],
  errors: [
    - Staying square on steep ground. Parallel hips push you off there. Turn a hip in instead #src("B22").
    - Frogging when you need to move fast or far. Two inside edges limit how far you can move #src("B55").
  ],
  tall: [Long thighs need a lot of hip turn-out#ix("Tall climbers!frog position")#ix("Mobility!hips") to bring your pelvis close. If your hips won't come in, widen your feet before you force your knees.],
  related: ("hip-turn", "weight-shift", "stemming", "high-step", "rockover"),
  watch: (("Neil Gresham Climbing Masterclass - Crux Films", "11 Neil Greshams Masterclass - Frogging", "https://www.youtube.com/watch?v=sY4OicuWbiA"),),
  sources: ("B17", "B22", "B38", "B44", "B55", "B61", "B65"),
)

#technique(
  key: "barn-door",
  name: "Barn door",
  aliases: ("barn-dooring", "swinging open"),
  category: "body",
  grade: 1,
  grade-note: [Hörst#ix("Hörst, Eric") teaches the cure, opposite hand and foot, as a basic #src("B11"). Rowland#ix("Rowland, Dave") teaches it on a slab first #src("B35"). At V1, start with fixes 1 and 4 (this book's suggestion). Stopping a door on steep V3s needs the flags in this chapter.],
  summary: [Your body swings open like a door when one hand lets go. It happens when the hand and foot holding you are on the same side. Your weight hangs beside the #jt("hinge") between them, so you rotate around it #src("B8", "B11"). Chapter 1 explains the mechanics.],
  how: [
    + Before the move, name the hand that stays on and the foot you stand on. If they are on the same side, expect a door.
    + *Fix 1.* Stand on the other foot. Stepping up with your right foot? Keep your left hand on and reach with the right #src("B35").
    + *Fix 2.* Swap feet or step through, so the opposite foot carries you #src("B62"). See #tref("foot-swap").
    + *Fix 3.* Flag. Put the free foot on the wall on the far side of the hinge from your body #src("B13", "B26"). See #tref("flag"), then #tref("back-flag") at V3 and #tref("inside-flag") at V4.
    + *Fix 4.* Press your #jt("off foot") (the foot not carrying you) into the wall, about at right angles to the hinge #src("B45").
    + *Fix 5, once you can deadpoint.* Move fast. A quick #tref("deadpoint") beats the swing #src("B62").
    + Holding the door shut with arm strength works on good holds. It costs a lot of energy #src("B62").
    + Practise on a slab. Let yourself swing open on purpose, then try fix 1 #src("B35").
  ],
  when: [
    *Look for*
    - good holds on one side only: hand and foothold stacked on the left, say.
    - holds and feet in a diagonal line up one side.
    - an #tref("arete", body: [arête]) you have to #tref("layback", body: [layback]) #src("B54").

    *Symptoms*
    - You let go with one hand and swing open towards that side. Your free foot flies off.
    - On an arête you peel off sideways #src("B54").
    - You are twisted in with opposite hand and foot, yet you still rotate out. That is a #jt("spin-out"), not a door. See #tref("backstep") #src("B39").
  ],
  errors: [
    - Reaching before the flag is set. Place the foot first.
    - A loose flag leg. Straighten it and press it into the wall #src("B26").
    - Trying to stop a door that has started. It is hard to correct once it begins #src("B13"). Set up so it never starts.
  ],
  related: ("flag", "back-flag", "inside-flag", "weight-shift", "foot-swap"),
  watch: (("Hooper’s Beta","The “Off Foot” is Climbing Technique #1 – Coaching w/ Dan #1", "https://www.youtube.com/watch?v=TAjHSueeOkw"),),
  sources: ("B8", "B11", "B13", "B26", "B35", "B39", "B45", "B54", "B62"),
)

#technique(
  key: "matching",
  name: "Matching hands",
  aliases: ("match", "matching"),
  category: "body",
  grade: 1,
  grade-note: [Matching a #tref("jug") is a first-session skill. Leaving room on small holds matters from about V3. The UK's coach training lists hand swapping as a movement skill #src("B2").],
  summary: [You bring your second hand onto the hold your first hand is on. That frees the first hand for the next move or gives you a rest #src("B54").],
  figure: "matching.svg",
  caption: [(a) The left hand in the middle of the edge leaves no room. (b) The left hand on the left half leaves room for the right.],
  how: [
    + Decide before you reach a hold whether you will match it.
    + If you will, catch it on the half away from the incoming hand. A left hand that the right will join takes the left half.
    + On a small hold, catch it with two or three fingers. Or slide the first hand off as the second slides on.
    + Set a foot under the hold first if you can. Then the match needs no big shift of your hips.
    + After matching, move your weight to the hand that stays. Then let the other go.
  ],
  when: [
    *Look for*
    - a hold big enough for two hands: a jug or a long edge.
    - a next hold on your current hand's side, where crossing would tie you in a knot.
    - a next hold that faces the wrong way for the crossing hand.

    *Symptoms*
    - You arrive on a hold you meant to match and there is no room.
    - You can't free your first hand without falling off.
  ],
  errors: [
    - Matching where a cross would save a move. See #tref("cross-through").
    - Matching with low feet and bent arms. Set your feet first.
  ],
  related: ("cross-through", "bumping", "regrip", "hand-foot-match"),
  sources: ("B2", "B54"),
)

#technique(
  key: "stemming",
  name: "Stemming",
  aliases: ("bridging", "stem", "corners", "dihedral", "open book", "inside corner"),
  category: "body",
  grade: 1,
  grade-note: [Corners and pairs of volumes appear on easy problems, where they mostly help you rest and save effort (judgement). The UK's coach training lists bridging as an opposition technique #src("B1").],
  summary: [You push your feet outward against two surfaces that face each other, such as the walls of a corner. The push presses your shoes onto them, so friction holds you without good holds #src("B29"). Your legs carry the weight, so your arms can rest.],
  figure: "stemming.svg",
  caption: [Back view into a corner. Each foot pushes into its own wall. The left palm presses the left wall.],
  how: [
    + Put one foot on each surface: the two walls of a corner, two #tref("volume", body: [volumes]), or a volume and the wall.
    + Place your feet higher and wider than feels natural #src("B29").
    + Push each foot into its surface, roughly at right angles to it.
    + Keep your heels low. More rubber touches and your calves tire less #src("B29").
    + Use your hands for balance. Press a palm flat on a wall, fingers pointing down or away from the corner #src("B29"). See #tref("palming").
    + Move one limb at a time. Shift your weight onto one foot, then lift and place the other #src("B29").
    + To rest, stand fully on any ledge or lean a shoulder on the wall#ix("Resting on the wall") #src("B29").
  ],
  parts: ((
    name: [Corners],
    how: [
      + Face into the corner, or turn a little towards the wall with the better holds.
      + Bend your knees and press outward and down, evenly on both walls #src("E24", "E20").
      + Where there are no handholds, press a flat palm on each wall at chest height #src("E20").
      + Step up a short way at a time. Big steps collapse the position (judgement).
      + If only one wall has holds, #tref("layback", body: [layback]) the edge of the corner. Walk your feet up the blank wall.
      + Spread your feet wide to rest. Often you can let go with both hands #src("E17").
    ],
    figure: "corner.svg",
    caption: [(a) Feet and palms press out into both walls. The centre of gravity sits between the feet. (b) The same position from above.],
  ),),
  when: [
    *Look for*
    - a corner: two wall panels that meet at an angle, with footholds or blank faces on both sides.
    - two volumes that face each other, or a volume next to a wall. They make a small corner #src("E11").
    - a blank section between two features #src("B29", "B65").
    - a main face with no footholds next to a side wall that is "in" (part of the problem). Push on the side wall.

    *Symptoms*
    - You pull hard on small holds in a corner while your feet sit on tiny edges.
    - Your arms tire in a corner although both walls have footholds.
    - You face one wall with both feet on it, so the corner gives you nothing.
    - Your calves cramp because your heels are too high #src("B29").
    - Your feet slip because they push straight down, not outward.
  ],
  errors: [
    - Gripping hard with your arms and fingers instead of pressing #src("B29"). Open your hands and push.
    - Pushing too hard. Relax and let friction do the work #src("B29").
  ],
  tall: [In a narrow corner your knees get in the way. Turn sideways with one foot still on each wall, or try a backstep: one foot on its outside edge, that hip to the wall #src("B29").],
  related: ("opposition", "layback", "palming", "smearing", "knee-bar"),
  sources: ("B1", "B29", "B65", "E11", "E17", "E20", "E24"),
)

== V2: turning in, flagging and crossing

#technique(
  key: "hip-turn",
  name: "Turning the hip in",
  aliases: ("hip in", "hip to the wall", "twisting in", "side-on", "getting long"),
  category: "body",
  grade: 2,
  grade-note: [Try it from V1, on easy problems that lean towards you (this book's suggestion). You need it on your first overhangs. Gresham#ix("Gresham, Neil") says low- to intermediate-level climbers struggle there because they keep their hips square#ix("Overhangs!hip position") #src("B22"). Rowland#ix("Rowland, Dave") twists on walls overhanging 10° or more #src("B44").],
  summary: [You turn your pelvis so the hip on your reaching side touches or nearly touches the wall, while your chest turns towards the holding hand. The turn lifts your reaching shoulder, so your hand goes higher on a straight arm #src("B19", "B43").],
  figure: "hip-turn.svg",
  caption: [(a) Square on between the feet, the left hand falls short. (b) With the left foot on its outside edge and the left hip at the wall, the hand reaches. The insets show the hips from above.],
  how: [
    + Hold with your right hand on a #tref("jug") or a #tref("sidepull") you can lean off #src("B38"). A right-hand sidepull faces right. You hang to its left.
    + Put your left foot on its #tref("edging", body: [outside edge]) (the little-toe side) on a foothold below your right hand #src("B37").
    + Put your right foot on a foothold out to the right, or press it on the wall #src("B15", "B37").
    + Turn your pelvis so your left hip goes to the wall. Your chest turns towards your right hand #src("B14").
    + Keep the right arm straight and lean off it #src("B43").
    + Look back at your right hand as you reach. It rolls your shoulders and adds up to a shoulder width of reach #src("B46").
    + Stand up through the left leg and reach high with the left hand.
  ],
  when: [
    *Look for*
    - an overhanging wall.
    - a holding hold you can lean off: a jug, or a sidepull facing away from your body.
    - a target up and towards your reaching side, near the limit of your reach.
    - a foothold below or just beyond your holding hand.

    *Symptoms*
    - You fall a hand's width short of a reach you could make on a vertical wall.
    - You have to #tref("lock-off", body: [lock off]) and your hips sag. Your arms do all the work on easy steep ground #src("B22").
  ],
  errors: [
    - Turning the hip without turning the foot onto its outside edge. Your knee jams.
    - Turning the wrong hip. The reaching side goes in #src("B15").
    - Twisting on a slab with small footholds. The twist can pop your foot off #src("B44").
    - Twisting on every move. Rowland#ix("Rowland, Dave") reads that as a possible weakness #src("B44").
  ],
  related: ("backstep", "drop-knee", "twist-lock", "frog", "edging"),
  watch: (
    ("Hooper’s Beta","Fix Your Shoulder Orientation – Coaching w/ Dan #2", "https://www.youtube.com/watch?v=3uKDpIUJ_8o"),
    ("Hooper’s Beta","Don’t Blame Wingspan! These Mistakes Limit Your Reach", "https://www.youtube.com/watch?v=bj25GdNX5B8"),
  ),
  sources: ("B14", "B15", "B19", "B22", "B37", "B38", "B43", "B44", "B46"),
)

#technique(
  key: "flag",
  name: "Side flag",
  aliases: ("flag", "flagging", "outside flag (US)"),
  category: "body",
  grade: 2,
  grade-note: [From about V2, reaches start to swing you open where your free foot has no hold (judgement). The UK's coach training lists flagging as a steep-wall skill #src("B1"). A US gym still teaches it to climbers stuck at V5 #src("B63").],
  summary: [You stretch your free leg straight out to its own side and press the foot on the wall. The leg balances your weight on the far side of the #jt("hinge"), so you don't swing open #src("B13", "B26"). US sources call this an outside flag #src("B59"). Gresham#ix("Gresham, Neil") seems to use that name for a #tref("back-flag") #src("B21"), so this book avoids it.],
  figure: "flag.svg",
  caption: [The left hand sits above the right foot. (a) With the left leg dangling, reaching right swings the body open. (b) The left leg stretched out left presses the wall and balances you.],
  how: [
    + Find your hinge: the line from the hand that stays on to the foot you stand on.
    + Check that your free foot is already on the far side of that line from your reach. If not, use a #tref("back-flag") from V3 or an #tref("inside-flag") from V4.
    + Stretch that leg straight out to its side #src("B26").
    + Press the inside edge or the ball of the foot into the wall. Blank wall is fine #src("B26", "B57").
    + Shift your hips over the standing foot #src("B13").
    + Reach.
    + Still swinging? Move the flag foot. A foot too low or too far from your body gives little leverage. On overhangs, push it up and into the wall #src("B58").
  ],
  when: [
    *Look for*
    - a standing foot roughly below the holding hand #src("B59").
    - a reach towards the side of your standing foot.
    - no foothold where your free foot would help.

    *Symptoms*
    - You swing open towards the reaching side as your hand lets go.
    - Your free leg hangs in the air.
    - Your free foot sits on a good hold, but not where your body needs it #src("B45").
  ],
  errors: [
    - A loose, dangling flag leg #src("B26").
    - Flagging on a slab. It rarely works there #src("B26").
    - Stabbing at the hold before you have settled #src("B26").
  ],
  related: ("back-flag", "inside-flag", "barn-door", "opposition"),
  watch: (
    ("Movement for Climbers", "How to Flag - A Climbing Technique for Achieving Balance", "https://www.youtube.com/watch?v=jLsii8s6acM"),
    ("The Boardroom Climbing Ltd", "Flagging", "https://www.youtube.com/watch?v=juPtjVgcQbg"),
  ),
  sources: ("B1", "B13", "B21", "B26", "B45", "B57", "B58", "B59", "B63"),
)

#technique(
  key: "cross-through",
  name: "Crossing hands",
  aliases: ("cross-through", "crossover", "cross-under"),
  category: "body",
  grade: 2,
  grade-note: [Cross-throughs on #tref("traverse", body: [traverses]) start around V2. Big crosses and cross-unders on steep walls matter from V4.],
  summary: [You move one hand past the other to a hold beyond it. A crossover passes over the holding arm and a cross-under passes under it. The hard part is getting your chest out of the way #src("B49").],
  figure: "cross-through.svg",
  caption: [Traversing left. The left hand holds a sidepull. The right hip rolls in. The left leg presses the wall. The right hand crosses over.],
  how: [
    + Hold with a hand you can lean on. A #tref("sidepull") or #tref("undercling") beats a flat edge.
    + Place your #jt("off foot") where it stops the swing.#ix("Off foot") Hooper#ix("Hooper, Jason") puts it at about 90° to the line from holding hand to standing foot #src("B45").
    + Keep pressing that off foot into the wall through the whole cross #src("B45").
    + *Roll:* turn your chest side-on to the wall so one hip touches it. This is the default on steep ground #src("B49").
    + *Swim:* keep your chest flat to the wall and narrow your shoulders. Use it on slabs, for wide hands, or when the feet are too poor to turn #src("B49").
    + Look back at the holding hand as you move. It rolls your shoulders and adds reach #src("B46").
    + For a cross-under, pass the reaching hand under the holding arm. It suits targets level with or below the holding hand.
    + If you add a #tref("drop-knee"), drop the knee on the reaching-hand side, even with your arms crossed #src("B20").
  ],
  when: [
    *Look for*
    - a traverse or diagonal line, with the next hold beyond your current hand #src("B54").
    - a current hold too small to match.

    *Symptoms*
    - Your chest or shoulder blocks the cross #src("B49").
    - You swing open as the reaching hand lets go.
    - Your off foot slides off at the moment you cross #src("B45").
  ],
  errors: [
    - Crossing so far that the next move becomes impossible. Check the hold after the target.
  ],
  tall: [Long arms cross a long way, but broad shoulders#ix("Shoulders!broad")#ix("Tall climbers!cross moves") still block you. Get narrow by rolling or swimming. Don't force the shoulder #src("B49").],
  related: ("matching", "hip-turn", "barn-door", "traverse"),
  watch: (("Hooper’s Beta","Why Do Climbers Struggle with Cross Moves? – Coaching w/ Dan #5", "https://www.youtube.com/watch?v=3Es610RvBI4"),),
  sources: ("B20", "B45", "B46", "B49", "B54"),
)

#technique(
  key: "layback",
  name: "Layback",
  aliases: ("lieback", "laybacking"),
  category: "body",
  grade: 2,
  grade-note: [Arêtes and lines of sidepulls appear at V2–V3. The UK's coach training lists laybacking as an opposition technique #src("B1").],
  summary: [You pull sideways on a vertical edge and lean away from it while your feet push the other way against the wall. Your arms and body make the shape of a "7" #src("B54").],
  figure: "layback.svg",
  caption: [Side view of a flake (a thin blade standing off the wall). Straight arms pull its edge out from the wall. The feet press high on the flake. The hips hang low.],
  how: [
    + Grip the edge with both hands, or one hand on it and one on the next #tref("sidepull") #src("B54", "B65").
    + Treat the edge as a sidepull: pull it towards you and hang on the other side.
    + #tref("straight-arms", body: [Straighten your arms]) and lean away #src("B54").
    + Put your feet high on the wall. Push them against the pull of your hands #src("B65").
    + Keep your #jt("core") (the muscles around your trunk) tight #src("B65").
    + Find the point where you neither fall back nor swing round. Lose it and you swing off like a door #src("B54").
    + Move your hands and feet up in short steps. Keep the push and the pull equal.
  ],
  when: [
    *Look for*
    - an #tref("arete", body: [arête]) with nothing usable on the face.
    - a vertical edge or #jt("flake") with no footholds near it #src("B65").
    - a vertical line of sidepulls.
    - a vertical #tref("pinch", body: [pinch]). Turning side-on into a layback needs less thumb strength #src("B24").

    *Symptoms*
    - You swing off the arête like a door #src("B54").
    - Your feet skate. They are too low, so they push down instead of in.
  ],
  errors: [
    - Staying front-on to a sidepull or pinch with your hips parallel to the wall #src("B24").
    - Feet too high. Your arms then hold more of your weight.
  ],
  tall: [Your long body makes a long "7", which closes quickly when your feet go high. Keep them a little lower than a shorter climber would.],
  related: ("opposition", "barn-door", "stemming", "arete", "sidepull"),
  sources: ("B1", "B24", "B54", "B65"),
)

== V3: twisting, staying tight and locking off

#technique(
  key: "backstep",
  name: "Backstep",
  aliases: ("back-step", "stepping through"),
  category: "body",
  grade: 3,
  grade-note: [Hörst#ix("Hörst, Eric") starts it on boulders about 20° overhanging #src("B15"). Rowland#ix("Rowland, Dave") uses it on overhangs of about 10° or more #src("B44"). Gym V3s on 20–30° walls start to need it.],
  summary: [You stand on the outside edge of the reaching-side foot, on a hold below the holding hand, while the other leg flags or stands wide. Your reaching-side hip turns to the wall and your weight settles over that heel #src("B37").],
  figure: "backstep.svg",
  caption: [(a) Left foot on its outside edge, on the line under the right hand. The hips settle over the heel. (b) The same foot behind the line: the hips rotate out.],
  how: [
    + Hold a #tref("jug") or a #tref("sidepull") with the right hand. Flat edges lose grip as you turn. #tref("gaston", body: [Gastons]) are the worst #src("B38").
    + Find #jt("the line") under the hold your right hand pulls #src("B38").
    + Pick a foothold for the left foot on that line, or a little to its right. Choose one at knee height or higher #src("B38").
    + Place the left foot's outside edge on it. Point the toe down a little and lift the ankle #src("B32"). Angle the heel away from the wall #src("B38").
    + Stretch the right leg straight out to the right, or stand it on a second foothold #src("B15", "B37").
    + Turn your lower body until the left hip is close to the wall. Let the hips settle over the left heel #src("B37").
    + Press with both feet at once. Pull the right hand down and in towards your body #src("B15").
    + Stand up through the left leg and reach with the left hand #src("B32").
  ],
  when: [
    *Look for*
    - an overhang. On vertical walls, try front-on options first #src("B44").
    - a jug or a sidepull for the holding hand.
    - a foothold at knee height or higher, under or beyond the holding hand.

    *Symptoms*
    - You twist in, but your body keeps rotating back out and your arm has to hold it. This is a #jt("spin-out"). The foot is behind the line. Use a #tref("drop-knee") instead #src("B39").
    - The move feels like a hard one-arm #tref("lock-off").
  ],
  errors: [
    - A foot too low to get your hips over the heel #src("B38").
    - Letting the flag leg bend, so your hips drift #src("B44").
  ],
  tall: [Rowland's#ix("Rowland, Dave") "knee height or higher" means your own knee.#ix("Tall climbers!backsteps") Footholds that look high to others may be perfect backsteps for you #src("B38").],
  small: [Turning your hip in brings you closer to the wall.#ix("Small climbers!backsteps") Climbers' own estimates of the extra reach run from an inch or so #src("H1") to a few inches #src("H2"), and we found no measurement. So when the holds suit a backstep, try it before you decide a move is too far (judgement). A #tref("drop-knee") does a similar job if your knees are mobile enough #src("H4"), but read the knee box in @cons-tall first.],
  related: ("hip-turn", "drop-knee", "twist-lock", "back-flag", "edging"),
  watch: (("Mani the Monkey", "Technique Training for Beginners: Back Step VS Flag", "https://www.youtube.com/watch?v=F5g9YtcnDqw"),),
  sources: ("B15", "B32", "B37", "B38", "B39", "B44", "H1", "H2", "H4"),
)

#technique(
  key: "back-flag",
  name: "Back flag",
  aliases: ("rear flag", "outside flag (UK)", "reverse flag"),
  category: "body",
  grade: 3,
  grade-note: [Same-side moves on steep V3s need it. Rowland#ix("Rowland, Dave") says his hip-turned version, the reverse flag, is "almost never necessary (or useful) at grades below 5.9 or V4" #src("B44").],
  summary: [Your holding hand and standing foot are on the same side, so you cross your free leg behind the standing leg. The foot presses the wall on the far side of the #jt("hinge"), so your weight balances over it #src("B26", "B59").],
  figure: "back-flag.svg",
  caption: [The left hand and left foot hold you. The right leg crosses behind the left and presses the wall. Your centre of gravity sits on the hinge.],
  how: [
    + Stand on your left foot, under your left hand.
    + Cross your right leg behind your left calf. Put the right foot on the wall, left of and below the left foot #src("B26").
    + Keep that leg straight. Press the foot into the wall #src("B26", "B57").
    + Move your hips over your left foot #src("B26").
    + Keep your right hip tucked against the wall #src("B59").
    + Reach with your right hand.
    + High standing foot? Pull up with your hips square. Swing the free leg under and behind as you rise. Find balance at the top, not before #src("B21").
    + *Reverse flag:* also turn your hips into the wall as you cross. It costs more arm strength than a #tref("backstep"). Use it when every foothold is on the holding-hand side and too high or small to backstep #src("B42", "B44").
  ],
  when: [
    *Look for*
    - all good holds on one side of your body, with the next hold on the other side #src("B26", "B59").
    - a handhold and foothold stacked on the same side, with no foothold for the other foot.
    - an overhang. Back flags are common there #src("B26").

    *Symptoms*
    - You swing open as soon as the reaching hand lets go.
    - You keep swapping feet to avoid the swing #src("B59").
  ],
  errors: [
    - Not crossing the leg far enough #src("B21").
    - Grabbing before you are balanced #src("B21").
    - A loose leg, or a foot too low or too far out #src("B26", "B58").
  ],
  related: ("flag", "inside-flag", "barn-door", "backstep", "foot-swap"),
  watch: (("Movement for Climbers", "How to Flag - A Climbing Technique for Achieving Balance", "https://www.youtube.com/watch?v=jLsii8s6acM"),),
  sources: ("B21", "B26", "B42", "B44", "B57", "B58", "B59"),
)

#filmstrip("filmstrip-drop-knee.svg", [Drop knee into a long reach], [Watch the hips rise and turn as the right knee drops, before the right hand leaves its hold.])

#technique(
  key: "drop-knee",
  name: "Drop knee",
  aliases: ("Egyptian", "knee drop"),
  category: "body",
  grade: 3,
  grade-note: [Learn a partial drop knee from V2 on big holds, but leave deep ones until a move needs them (this book's suggestion). Deep drop knees are rare below elite level #src("B33"). Steep V3s use a partial one. On steep V4s a drop knee is often the intended move. The UK's coach training lists the drop knee #src("B1"), while a US gym teaches it at V5–V6 #src("B64").],
  summary: [You turn the knee of your reaching-side leg down and inward, so the thigh turns towards the wall. Both feet push apart against two footholds. That pins your hips to the wall and lifts the reaching shoulder #src("B19", "B41").],
  figure: "drop-knee.svg",
  caption: [(a) Square on, the right hand falls short. (b) Right knee dropped. The right hip turns in. Both feet push apart. The hand reaches. The insets show the hips from above.],
  how: [
    + Find two footholds, one each side #src("B20"). The high one, for the reaching-side foot, sits between waist and shoulder height. The other sits wide and low #src("B41").
    + Place the foot that won't pivot first if you can #src("B20").
    + Put the high foot's toe on the near corner of its hold. That leaves room to pivot #src("B20").
    + Turn your hip and that knee in towards the wall, then point the knee down. The foot rolls onto its outside edge. In a deep drop knee, the thigh lies against the wall #src("B41").
    + For a partial drop knee, stop with the knee part-way down. It gives most of the lock with less load on the knee (judgement).
    + Straighten the other leg and push out through its inside edge. Your weight moves back over the dropped foot. Your arms unload #src("B40").
    + Pull in with the holding hand, ideally on a #tref("sidepull"). Turn your chest towards it. Reach with the hand on the dropped-knee side #src("B20", "B43").
    + Before you stand up out of it, turn the knee back up.
  ],
  when: [
    *Look for*
    - a wall overhanging 30–75° #src("B20").
    - two footholds, one each side: wide apart at about the same height #src("B20"), or one between waist and shoulder height and the other wide and low #src("B41").
    - the best foothold on the reaching side of #jt("the line"), where a #tref("backstep") would spin out #src("B39", "B40").
    - a holding hold you pull sideways: a sidepull, an #tref("undercling"), a sloper or a diagonal hold #src("B19").

    *Symptoms*
    - Square on, your backside sticks out and your arms tire fast #src("B20").
    - Your backstep keeps spinning out #src("B39").
  ],
  errors: [
    - Dropping the wrong knee. Drop the knee on the reaching-hand side, even when your arms cross #src("B20").
    - Too little room on the foothold. The foot skates off as you pivot #src("B20").
    - A bent push leg. Your hips drift and your arms take over #src("B44").
    - Trying it on an overhanging arête or under a roof lip. There is no room #src("B20").
    - Forcing a deep drop when tired. It loads the inside of the knee#ix("Injuries!knee"): the #jt("MCL") (the ligament on the inside) and the #jt("meniscus") (the cartilage pad in the joint) #src("B33", "G9"). Chapter 9 gives the injury figures.
    - Ignoring pain on the inside of the knee. Stop. Rest longer if you are older#ix("Age!knee injuries") or have hurt the knee before #src("B33").
  ],
  tall: [On a wide drop knee, let your knee pass inside your elbow #src("B20"). Long thighs make deep drops awkward in tight spaces,#ix("Tall climbers!drop knee") so use a partial one there.],
  related: ("backstep", "twist-lock", "hip-turn", "stemming", "barn-door"),
  watch: (("Movement for Climbers", "What the Heck is a Drop Knee?", "https://www.youtube.com/watch?v=U0v9xxqEjfY"),),
  sources: ("B1", "B19", "B20", "B33", "B39", "B40", "B41", "B43", "B44", "B64", "G9"),
)

#technique(
  key: "pre-loading",
  name: "Sitting into it",
  aliases: ("pre-loading", "sitting back", "sagging", "casting out"),
  category: "body",
  grade: 3,
  grade-note: [From about V3, overhanging moves need leg power from a loaded start. Hooper#ix("Hooper, Jason") calls straight-armed starts the essential tool for overhangs #src("B47").],
  summary: [Before a move, you lower your hips onto bent legs with your arms straight, so your feet press hard into the wall. You drive the move from there #src("B47").],
  figure: "pre-loading.svg",
  caption: [(a) Pulled in tight: knees at the wall, feet barely weighted. (b) Sat back: arms straight, hips and heels low. The hips then drive up and in.],
  how: [
    + Set your feet with your heels low #src("B47").
    + Straighten your arms.
    + Let your hips sit down and slightly out until your feet press firmly into the wall #src("B47").
    + Hooper's cue: get as far from your bottom hand as you can while staying balanced #src("B48").
    + Relax the arm that will move next #src("B48").
    + Drive with your legs. Move your hips up and in. Pull only at the end #src("B47").
    + On #tref("sloper", body: [slopers]), sit with your hips low and close to the wall. Keep your trunk tight #src("B31").
  ],
  when: [
    *Look for*
    - an overhang with a big move ahead.
    - slippery or poor footholds your feet slip off when you pull in tight #src("B47").
    - slopers #src("B31").

    *Symptoms*
    - You have no power on overhangs #src("B47").
    - Your feet blow off when you pull.
    - You start moving away from the wall before you reach the hold #src("B48").
  ],
  errors: [
    - Sitting low on a slab or vertical wall. It moves weight from your feet to your fingers #src("B8").
    - Staying "sucked in". Your feet unload #src("B48").
    - Pausing before the hard move until your #jt("momentum") is gone #src("B69").
  ],
  tall: [Long legs let you sit deep, but then your hips end up far below and away from the next hold. Sit only as deep as your feet need to press.],
  related: ("straight-arms", "deadpoint", "body-tension", "hip-pump"),
  watch: (
    ("Hooper’s Beta","Why You Have NO POWER On Overhangs – Coaching w/ Dan #3", "https://www.youtube.com/watch?v=TZxhg6NMwaI"),
    ("Hooper’s Beta","Why Do Climbers that “Stay Tight” Have Poor Body Tension? – Coaching w/ Dan #4", "https://www.youtube.com/watch?v=EGdusH97XcY"),
  ),
  sources: ("B8", "B31", "B47", "B48", "B69"),
)

#technique(
  key: "body-tension",
  name: "Body tension",
  aliases: ("tension", "core tension", "keeping your feet on"),
  category: "body",
  grade: 3,
  grade-note: [Hooper's Beta#ix("Hooper, Jason") stresses it on a steep V3 #src("B52"). On caves and #tref("roof", body: [roofs]) it matters earlier. A US gym still teaches it in its course for climbers stuck at V5 #src("B63").],
  summary: [Tension runs from your toes through your legs and trunk to your fingers. It keeps your feet loaded on a steep wall while a hand moves #src("B51").],
  figure: "body-tension.svg",
  caption: [Side view, 40° overhang. (a) Slack: the feet cut and you swing under your hands. (b) Tense: the toes pull into the wall and the hips stay up.],
  how: [
    + Press your toes into the footholds. Keep the pressure on while you move.
    + Pull with the backs of your thighs and your inner thighs. These #jt("hamstring", body: [hamstrings]) and inner-thigh muscles hold the feet against the wall #src("B71").
    + Keep your hips at the balance point. A sagging trunk loses the squeeze #src("B31"). Hips jammed into the wall unload the feet #src("B48").
    + Set your shoulder blades when you catch a hold #src("B50").
    + Before a hand moves, check that both feet are loaded. Relax the arm that will move #src("B48").
    + If a foot cuts, control the swing through your shoulders. Put the foot back quietly #src("B53"). See #tref("cutting-loose").
    + During foot swaps on overhangs, a quick flick of the hips stops your legs swinging out #src("B58").
  ],
  when: [
    *Look for*
    - a cave, a roof or an overhang steeper than about 30°.
    - footholds far below your hands.
    - small or downward-sloping footholds, or #tref("toe-hook", body: [toe hooks]) and #tref("heel-hook", body: [heel hooks]).

    *Symptoms*
    - Your feet cut when you reach.
    - After a foot cut you swing #src("B53").
    - One foot keeps popping off.
  ],
  errors: [
    - Treating it as a core-strength problem. It is mostly technique and coordination #src("B51").
    - A loose free leg #src("B26").
  ],
  tall: [A long body is a long lever between your hands and your feet,#ix("Tall climbers!body tension") so you need more tension to keep your feet on in a roof.#ix("Roofs!body tension") Bringing your feet higher shortens the lever.],
  related: ("pre-loading", "toe-pull", "opposition", "compression", "cutting-loose"),
  watch: (
    ("Hooper’s Beta","Why Do Climbers that “Stay Tight” Have Poor Body Tension? – Coaching w/ Dan #4", "https://www.youtube.com/watch?v=EGdusH97XcY"),
    ("Hooper’s Beta","Why Climbers Should Rethink Core Strength Training", "https://www.youtube.com/watch?v=jwyd40EBnlI"),
  ),
  sources: ("B10", "B26", "B31", "B48", "B50", "B51", "B52", "B53", "B58", "B63", "B71"),
)

#technique(
  key: "lock-off",
  name: "Lock-off",
  aliases: ("locking off", "static lock"),
  category: "body",
  grade: 3,
  grade-note: [From about V3, slow reaches to small holds need it where you can't turn in. Baker#ix("Baker, John") says lock-off strength matters more on steeper, harder climbs #src("B62").],
  summary: [You hold one arm bent with the shoulder pulled down while the other hand lets go and reaches slowly to the next hold. You catch it without a swing.],
  figure: "lock-off.svg",
  caption: [Side view. The right hand is locked beside the shoulder, with the feet high.],
  how: [
    + First check whether #tref("hip-turn", body: [turning the hip in]) or a #tref("drop-knee") would do the job. Gresham#ix("Gresham, Neil") uses them to avoid locking off #src("B23", "B20").
    + Set your feet, as high as useful. Let your legs push you up into the lock #src("B27").
    + Bring the holding hand close to your shoulder. The lock is easier there #src("B62").
    + Keep that elbow down by your ribs, in line with the hand #src("B28").
    + Pull your shoulder blade down. Keep your body close to the wall #src("B57").
    + Reach smoothly and grip.
  ],
  when: [
    *Look for*
    - a small target you must hit exactly: a #jt("crimp"), a #tref("pocket", body: [pocket]) or a #tref("sloper", body: [sloper]).
    - front-on feet only: two footholds below you and no sidepull to twist off.
    - a move between two edges you pull straight down.

    *Symptoms*
    - You arrive at a poor hold with #jt("momentum") and swing off.
    - You can't hold the lock long enough to grip. Try a #tref("twist-lock") or a #tref("deadpoint") instead.
  ],
  errors: [
    - Letting the elbow flare out #src("B28").
    - Getting stuck in tight, bent-arm positions. They feel secure but cut your reach #src("B47").
  ],
  tall: [You can often reach from a half lock where shorter climbers need a full one.#ix("Tall climbers!lock-offs") Extra reach usually comes from rolling your shoulders, not from locking harder #src("B46").],
  small: [On a big reach you may need your holding hand below your shoulder, at or even below your chest, which is harder than a lock beside your shoulder.#ix("Small climbers!lock-offs") One coach under 5~ft suggests trying these deeper locks on climbs at your warm-up grade #src("H9"). Add a few at a time, because they load your elbow and shoulder (judgement).],
  related: ("twist-lock", "straight-arms", "deadpoint", "hip-turn"),
  sources: ("B20", "B23", "B27", "B28", "B46", "B47", "B57", "B62", "H9"),
)

#technique(
  key: "opposition",
  name: "Opposition",
  aliases: ("counter-pressure", "push–pull", "opposing forces"),
  category: "body",
  grade: 3,
  grade-note: [Hand-against-foot opposition, as in a #tref("layback"), appears from V2. Squeezing with two hands appears from V3–V4.],
  summary: [Two contacts push or pull against each other, so holds that are useless alone start to work #src("B14"). The sideways forces cancel out. The squeeze presses skin and rubber onto the holds, so friction holds you up.],
  figure: "opposition.svg",
  caption: [Two sidepulls face away from each other. Pulling them towards each other holds you on.],
  how: [
    + Read which way each hold faces. Pull the opposite way #src("B70").
    + Find a partner contact that pushes or pulls the opposite way.
    + *Hand against hand:* pull two #tref("sidepull", body: [sidepulls]) towards your chest. Or push two #tref("gaston", body: [gastons]) apart, elbows out #src("B14").
    + *Hand against foot:* pull an #tref("undercling") up while your high feet press into the wall #src("B30"). Or pull a sidepull while the opposite foot stands on its outside edge #src("B14").
    + *Foot against foot:* push your feet apart, as in #tref("stemming") or a #tref("drop-knee") #src("B20", "B29"). A #tref("bicycle") squeezes one hold between both feet #src("B56").
    + Load both contacts at once. Then move the limb that isn't part of the pair.
    + Keep your trunk tight. If your #jt("core") sags, the squeeze lets go #src("B31").
  ],
  when: [
    *Look for*
    - holds that face sideways or down.
    - a pair facing away from each other. Squeeze them inward.
    - a pair facing towards each other. Push them apart.
    - #tref("volume", body: [volumes]), corners and arêtes with no edge to pull down on.

    *Symptoms*
    - A sidepull slides out of your hand because no foot pushes the other way.
    - You can't hold an undercling because your feet are low #src("B30").
  ],
  errors: [
    - Pulling straight down on a sidepull or undercling.
    - Pushing gastons apart on a steep wall for long. It strains the shoulders#ix("Injuries!shoulder") #src("B14").
  ],
  related: ("layback", "stemming", "compression", "drop-knee", "body-tension"),
  watch: (("Movement for Climbers", "(Climbing Analysis) | The Importance of Using Counterpressure", "https://www.youtube.com/watch?v=MKtOjjd3XGQ"),),
  sources: ("B14", "B20", "B29", "B30", "B31", "B56", "B70"),
)

#technique(
  key: "bumping",
  name: "Bumping",
  aliases: ("bump", "using intermediates", "double move"),
  category: "body",
  grade: 3,
  grade-note: [From about V3, #jt("setter", body: [setters]) (the people who design the problems) put targets past arm's reach with small holds on the way.],
  summary: [You move the same hand twice in a row: first to a small hold on the way, an #jt("intermediate"), then on to the target. The other hand and your feet stay put.],
  figure: "bumping.svg",
  caption: [The right hand goes to a small intermediate (1), then on to the jug (2).],
  how: [
    + Keep the holding arm straight and your hips set. On steep ground, #tref("hip-turn", body: [turn a hip in]).
    + Go to the intermediate fast. Weight it only long enough to stay in balance.
    + Carry straight on to the target. Don't settle on the intermediate.
    + On one big hold, catch the nearest part first. Then bump to its best part.
    + When you are tired, look again for small footholds lower and closer in. They let you move up in short steps instead of lunging #src("B22").
  ],
  when: [
    *Look for*
    - a target beyond #jt("static") reach, with a small hold on the way.
    - a target that faces the wrong way for the other hand, so crossing won't work.
    - a next move that needs a particular hand on the target.

    *Symptoms*
    - You are fully stretched and can't reach.
    - You lunge for the biggest hold and arrive off balance.
    - You reach the target with the wrong hand.
  ],
  errors: [
    - Fixating on the biggest holds #src("B22").
    - Ignoring small footholds. A higher foot often makes the hand intermediate unnecessary.
  ],
  tall: [You can often skip intermediates,#ix("Tall climbers!skipping intermediates") but that can leave you stretched out with no way to move your feet. A shorter climber's sequence is sometimes easier.],
  related: ("matching", "cross-through", "deadpoint", "regrip"),
  sources: ("B22",),
)

== V4: locking in and squeezing

#technique(
  key: "twist-lock",
  name: "Twist lock",
  aliases: ("twist-locking",),
  category: "body",
  grade: 4,
  grade-note: [Hörst#ix("Hörst, Eric") starts it on boulders about 20° overhanging, then moves steeper #src("B15"). The full twist of hips and shoulders pays from about V4.],
  summary: [You add a turn of the shoulders to a #tref("backstep") or #tref("drop-knee"). The reaching-side hip and shoulder turn to the wall while the holding arm pulls down to your ribs. Your body locks, so the free hand reaches with little effort #src("B15", "B43").],
  figure: "twist-lock.svg",
  caption: [(a) Set: right arm straight, left foot backstepped, hips half turned. (b) Locked. The left hip and shoulder turn in. The right elbow comes to the ribs. The left hand reaches high. (c) The lock from the side. The right forearm points into the wall.],
  how: [
    + Set your feet. Backstep if the foothold is on #jt("the line"). Drop a knee if it is behind the line #src("B38", "B40").
    + Put your right foot on a foothold out to the right, or flag it #src("B37").
    + Start with the right arm straight. Lean out on it while your hips twist in #src("B43").
    + As your left hip nears the wall, turn your left shoulder in too #src("B43").
    + Bend the right arm as the shoulder turns. The elbow ends by your ribs. Your chin ends near your right shoulder #src("B43").
    + Press with both feet at once. Pull the right hand down and in #src("B15").
    + Reach with the left hand. Do it all as one movement, without a pause #src("B43").
    + On flat holds or #tref("gaston", body: [gastons]), pull along the hold's long edge, not across it #src("B43").
  ],
  when: [
    *Look for*
    - a steep wall and a high target in line with or beyond your holding hand.
    - a #tref("sidepull") or #tref("undercling") for the holding hand.
    - front-on feet that don't give you the reach.

    *Symptoms*
    - You touch the target but can't hold the position to grip it.
    - You swing out as you let go.
    - You can only do the move as a full front-on #tref("lock-off").
  ],
  errors: [
    - Not finding the exact locked position. Shuffle until it feels solid.
    - Twist-locking every move #src("B44").
  ],
  related: ("backstep", "drop-knee", "hip-turn", "lock-off"),
  watch: (("Neil Gresham Climbing Masterclass - Crux Films", "6 Neil Greshams Masterclass - Twistlock", "https://www.youtube.com/watch?v=v4TnitXGxkM"),),
  sources: ("B15", "B16", "B37", "B38", "B40", "B43", "B44"),
)

#technique(
  key: "inside-flag",
  name: "Inside flag",
  aliases: ("crossing in front",),
  category: "body",
  grade: 4,
  grade-note: [Gripped magazine calls it rarely efficient but occasionally ideal #src("B57"). It starts to pay at about V4.],
  summary: [Your free leg crosses in front of the standing leg, between it and the wall. The foot presses the wall on the far side. As you stand, your hips and chest corkscrew until every limb is straight #src("B21").],
  figure: "inside-flag.svg",
  caption: [(a) Crouched on one low foothold. (b) Standing up, the right leg passes between the left leg and the wall. Every limb ends straight.],
  how: [
    + Stand on a single low foothold, below knee height, under your holding hand #src("B21").
    + Use the inside edge of that foot #src("B21").
    + As you stand up, pass your free leg in front of the standing leg, close to the wall #src("B21").
    + Let your hips, chest and shoulders turn together, like a corkscrew. Pull one hip to the wall #src("B21", "B59").
    + Press the free foot on the wall on the far side.
    + Finish with every limb straight. Reach with a nearly straight arm #src("B21").
    + Keep hold of the low handhold until the reach is done #src("B21").
  ],
  when: [
    *Look for*
    - one low foothold and a long reach up and away from it #src("B21").
    - a move where any other flag would need a foot swap first #src("B59").
    - a low standing foot. With a high one, a #tref("back-flag") is easier #src("B10", "B21").

    *Symptoms*
    - A back flag leaves you a hand short, because your hips stay low and out.
    - You swap feet before every reach.
  ],
  errors: [
    - Keeping the standing leg bent. You never stand up #src("B21").
    - Not passing the leg through far enough #src("B21").
  ],
  related: ("flag", "back-flag", "hip-turn", "foot-swap"),
  watch: (("Movement for Climbers", "(Climbing Analysis) Inside Flag - The Move You Never Do But Maybe Should", "https://www.youtube.com/watch?v=LOkhYCi-IrE"),),
  sources: ("B10", "B21", "B57", "B59"),
)

#technique(
  key: "compression",
  name: "Compression",
  aliases: ("squeezing", "hugging"),
  category: "body",
  grade: 4,
  grade-note: [Wide #tref("volume", body: [volume]) problems ask for it from V3–V4. A US gym still teaches it in its course for climbers stuck at V5 #src("B63").],
  summary: [You hold yourself between two holds that face away from each other by squeezing them together with your hands and feet. The squeeze creates the friction that holds you up.],
  figure: "compression.svg",
  caption: [The two side faces of a big volume face away from each other. The palms squeeze them inward, elbows down. The feet squeeze a lower volume.],
  how: [
    + Put your hands on opposite sides of the feature, at about chest to head height.
    + Squeeze inward with slightly bent arms, elbows down. Use your chest and back, as in a hug.
    + Squeeze with your feet too. Put a toe on one side and a toe or heel on the other. A #tref("bicycle") does this on one hold #src("B56").
    + Press your free foot against a foothold or the wall. It can turn even a round foothold into a clamp #src("B45").
    + Keep your hips close to the feature. Keep your trunk tight, so the squeeze in your hands and feet connects #src("B31").
    + Release one contact only when the other three are squeezing. Move it fast.
    + On a #tref("pinch", body: [pinch])-shaped feature, turning side-on into a #tref("layback") saves thumb strength #src("B24").
  ],
  when: [
    *Look for*
    - two holds or volumes facing away from each other.
    - an #tref("arete", body: [arête]) you can hold from both sides.
    - big round volumes with no edge to pull down on.#ix("Volumes!squeezing")

    *Symptoms*
    - You slide down between the holds.
    - Your feet pop because only your hands squeeze.#ix("Feet popping off")
    - Your arms burn because you pull down instead of in.
  ],
  errors: [
    - Compression #tref("heel-hook", body: [heel hooks]) without first tensing the backs of your thighs. Gresham#ix("Gresham, Neil") lists them as high-risk#ix("Injuries!hamstring") #src("B25").
  ],
  tall: [Wide spans are more comfortable at your height, but Lattice's client data show little link between #jt("ape index") and grade#ix("Ape index!and grade") #src("B66"), though one 2007 study disagrees (@cons-tall). The squeeze and the footwork matter more.],
  related: ("opposition", "body-tension", "bicycle", "volume", "pinch"),
  watch: (("Climbing Tech Tips", "Climbing Movement: 16. Opposition vs. Compression | Climbing Tech Tips", "https://www.youtube.com/watch?v=ar06kKAHmuA"),),
  sources: ("B24", "B25", "B31", "B45", "B56", "B63", "B66"),
)
