#import "../template.typ": *

// The problems of the exercises booklet (book/exercises.typ). Each question
// starts a right-hand page, with its answer overleaf.

#heading(level: 1, numbering: none)[Eight problems to read]

These eight problems go with _Reading the Wall_, a technique handbook for indoor bouldering. They are invented. No gym has set them and nobody has climbed them, so the grades are rough and the #jt("beta") is the book's judgement. They run from about V2 to about V6 in different styles. The harder ones are worth reading even if you can't climb that grade yet.

Read each drawing with the method in the book's #bref("reading-method"). Answer the prompts and make your plan, then turn the page and compare. Your beta may be as good as this one, especially if you are much taller or smaller than the climber in the drawings. That climber stands about 1.75 m and reaches about 2.1 m from toes to fingers (about ten and a half bolt holes).

Page numbers in brackets, as in #tref("backstep"), are the book's.

#heading(level: 2, numbering: none, outlined: false)[Reading the drawings]

Letters mark holds big enough for a hand. Numbers mark holds only a foot can use, though a lettered hold can still take a foot. Letters and numbers run up the wall (or along it on the traverse), so their order says nothing about the sequence. Tape marks the start, and volumes count. The dots are bolt holes 20 cm apart, so you can count distances as #bref("reading-size", body: ["Reading for your size"]) suggests. Short streaks on a hold are shoe rubber. A smudge just below its lip is chalk.

On the answer drawings, D R3 means hold D, taken by the right hand as the third hand move. The numbered moves also count the feet, so the two numbers don't match.

#pagebreak()

#heading(level: 2, numbering: none, outlined: false)[Key to the drawings]

Most drawings show the climber from behind, facing the wall, as you would see a friend from the mats.

#figure(image("../figures/legend.svg"), caption: [In every drawing the climber's left limbs are shaded and the right limbs white, so you can follow which hand and foot does what.], kind: image, supplement: [Figure])

#reading-question(
  n: 1, title: [Slab], grade: 2,
  wall: [The wall leans back 15°, seen from behind.],
  start: [both hands on A, feet on 1 and 2.], finish: [both hands on E.],
  figure: "reading-v2-slab.svg",
  prompts: [
    - *Step 2.* The wall leans back. What does #bref("reading-first") say to read first?
    - *Step 3.* Which way does C face? What can you do with B?
    - *Step 4.* Give B, C and D an L or an R.
    - *Step 5.* Foothold 4 is the big one. Count the bolt holes to it from foothold 2. How high is that compared with your hips? Which foot goes there? How does it get there?
    - *Step 6.* Where will you have least to pull on?
  ],
)
#reading-answer(
  n: 1,
  figure: "reading-v2-slab-answer.svg",
  caption: [Move 6. Read a slab's feet first: the volume turns the long step to 4 into two. The discs are moves 1 to 3.],
  moves: [
    + Left foot on 1, right foot on 2. #tref("smearing", body: [Smear], show-page: false) your right foot on the #tref("volume", body: [volume], show-page: false), heel low.
    + Move your hips over it and stand up. Left foot to 3.
    + Move your hips over 3 and rise until your arms are straight. Right foot to 4, only 20 cm above 3.
    + Press down on A with your right hand. Left hand to C, a #tref("sidepull", body: [sidepull], show-page: false). It faces left, so you lean right off it.
    + Right hand to B, only to steer. Move your hips over 4 and rise.
    + Left foot to 5. Stand up on your right foot and lean right until your left arm is straight. Right hand to D.
    + Move your hips over 5. Right foot to 6 and stand on it. Left foot to 7 and stand on it. Right hand to E.
    + Left hand to E.
  ],
  crux: [Moves 5 and 6. Your right hand leaves A and your hips move right of it. C only stops you tipping right. B has no edge. So your feet hold you until your right hand reaches D. Move~7 is easier. You hold D while your feet move. Only the reach to E is on your feet alone.],
  wrong: [You stay on A and step from 2 to 4, the biggest foothold. That is about 90 cm, level with your hips. Your knee folds tight and your hips have a long way to cross. A is a thin edge at shoulder height, so it helps little. Reaching for B falls short and brings your chest to the wall. Leaning in pushes your feet off #src("E3", "E24"). A high step on a slab upsets your balance #src("A34"). When the big foothold is a long step, look for a smear on the way.],
  next: [If the smear slips as you stand, drop your heel and keep your hips over the foot. Commit all your weight at once #src("E1", "E3", "E16"). If the shoe still skates, stand further out on the volume #src("E5", "E18"). You could also skip the volume: stay on 2 and take your left foot to 3. That small foothold is about 70 cm above the foot you stand on.],
  entries: ("slab", "smearing", "volume", "sidepull", "rockover", "high-step"),
)

#reading-question(
  n: 2, title: [Traverse], grade: 3,
  wall: [The wall overhangs 10° and runs to the right, seen from behind. D's back is smooth, so you can't pinch it.],
  start: [both hands on A.], finish: [both hands on E.],
  figure: "reading-v3-traverse.svg",
  prompts: [
    - *Step 3.* Which way does each hold face? Where does your body go for each hand on D?
    - *Step 4.* Give each hold an L or an R. Which holds have room for both hands?
    - *Step 5.* Which foot do you stand on as your hand lands on D? What does the other foot do?
    - *Step 6.* Where does the wrong hand cost you most?
  ],
)
#reading-answer(
  n: 2,
  figure: "reading-v3-traverse-answer.svg",
  caption: [Move 4. You stand on your left foot with that hip at the wall. The right foot presses. The left hand crosses to D.],
  moves: [
    + Left foot on 1, right foot on 2. Right hand, then left hand to B. Walk your feet to right foot on 4, left foot on 3.
    + Right hand to C, which faces up. Hang under it on a straight arm.
    + Right foot to 5 as your #jt("off foot") (it presses to stop a swing). Left foot to 4 on its outside edge, toes right (a #tref("backstep", body: [backstep], show-page: false), to clear your chest).
    + Turn your #tref("hip-turn", body: [left hip to the wall], show-page: false) as your left hand leaves B. Left hand under your right arm to D, which faces left. Keep your right foot pressing.
    + Move your hips towards foot 5. Stand up on that foot as you let go of C. Lean right off D as your left foot #tref("pivoting", body: [pivots], show-page: false), toes left. Right hand to E. D is now a #tref("sidepull", body: [sidepull], show-page: false).
    + Walk your feet along to right foot on~7, left foot on~6.
    + Left hand to E.
  ],
  crux: [The #tref("cross-through", body: [cross], show-page: false) in move 4. Then letting go of C. C is a flat edge, which loses grip as you turn #src("B38"). D holds nothing yet, so C holds you. D becomes a sidepull only once your shoulder passes it. Your right arm stops that. For a moment no hand holds you in: keep moving right.],
  wrong: [The mistake is arriving at D with the wrong hand. C is too small to match and D is too thin to share (judgement). So your right hand goes on to D with your left still on B. With your body on D's left, D is a thin #tref("gaston", body: [gaston], show-page: false). You then let go of B with only that to pull on. Your shoulder does most of the work #src("C34"). It can go, but you pay twice: this gaston, then E with your left hand on C pulled sideways (judgement). Swapping hands on C leads to the same catch, after a moment on two or three fingers of a flat edge. A hold that faces back the way you came only works as a sidepull once your shoulder is past it.],
  next: [If your chest blocks the cross, roll further onto your left hip #src("B49"). If you can't let go of C, cross your left hand from B to C instead. Then take your right hand past D to E. You pull C about 30° sideways at the catch. If you are small, E is out of reach from C.],
  entries: ("traverse", "cross-through", "sidepull", "backstep", "gaston"),
)

#reading-question(
  n: 3, title: [Overhang], grade: 3,
  wall: [The wall overhangs 20°, seen from behind. B has room for two hands.],
  start: [both hands on B.], finish: [both hands on E.],
  figure: "reading-v3-overhang.svg",
  prompts: [
    - *Step 3.* Which way does each hold face?
    - *Step 4.* Give A, C and D an L or an R.
    - *Step 5.* Compare the marks on A with those on E. What do they tell you? What kind of hold is D? Where must your body be to hold it? What could put it there?
    - *Step 6.* Where is the crux?
  ],
)
#reading-answer(
  n: 3,
  figure: "reading-v3-overhang-answer.svg",
  caption: [Move 4. The heel holds your hips in. The arrow shows where they went in move 3.],
  moves: [
    + Left foot on 1, right foot on 2. Left foot to 3, then 4.
    + Right heel into the bowl of A. Toes out, knee out. Both hands stay on.
    + Tighten your buttocks. Press the heel and pull it towards your bum. Stand up on your left foot at the same time. Your hips go in and up to the right. B is below your shoulder now and can only press, so don't stop. As your hips rise, left hand to C, a #tref("sidepull", body: [sidepull], show-page: false).
    + Right hand to D, a sloper. Hang under it. Keep pulling with the heel.
    + Left foot up to B, the old start hold. Keep the heel on.
    + Stand up on your left foot until your hips are higher than A. Then roll onto your whole foot on A. Right hand to E, leaving D as your hips rise.
    + Left hand to E.
  ],
  crux: [Moves 3 to 5. You leave the start for a small edge and a sloper. Only the #tref("heel-hook", body: [heel], show-page: false) keeps your hips in. At move 5 both feet come high, so the sloper can roll off (judgement).],
  wrong: [You take A with your right hand: it is the biggest hold in reach. Then you stand on 4 and take your right foot off. D is now in reach. But your left hand and foot make a #jt("hinge") (the line you swing around) far left of D. You swing open as your right hand lets go. A #tref("back-flag", body: [back flag], show-page: false) stops the swing, but your hips stay far left. A sloper only holds with your body below it #src("C3", "C34"). A toe or #tref("toe-pull", body: [flat sole], show-page: false) on A can only drag on friction. Press hard and it shoves your hips left and out. A heel sits in A's bowl, so it has something to pull against and draws you in (judgement). Rubber marks and no chalk suggest a foothold #src("E30", "E31").],
  next: [If the heel won't go on with both hands on B, take A with your right hand first. Set the heel beside your hand and carry on from move 3. If the heel slips, change the foot's angle by a few degrees #src("A8") and keep your hips close #src("A9"). Warm up first #src("A11"). Turning the foot out hard on a heel close to your hip can tear a knee ligament #src("A10").],
  tall: [C and D are in reach from feet 4 and 3. The heel still keeps your hips in.],
  small: [Don't skip foot 4. From foot 3, D is out of reach even with the heel.],
  entries: ("heel-hook", "sloper", "rockover"),
)

#reading-question(
  n: 4, title: [Steep wall], grade: 4,
  wall: [The wall overhangs 35°, seen from the side. The lettered holds run in one line, about 50 cm apart along it. A has room for two hands and C for one. Foothold 3 is wide enough for two feet.],
  start: [both hands on A.], finish: [both hands on E.],
  figure: "reading-v4-steep.svg",
  prompts: [
    - *Step 2.* You can't tell left from right from here. What can you see that you couldn't see from behind?
    - *Step 3.* Compare the profiles of B, D and E. Which one has no lip to hook? Where does that want your hips?
    - *Step 5.* Which holds could take a foot?
    - *Step 6.* Which hand moves need your full stretch? What do you stand on for them? What is each leg doing?
  ],
)
#reading-answer(
  n: 4,
  figure: "reading-v4-steep-answer.svg",
  caption: [Move 5. Hips in and low under D, on a straight right arm. Left and right could swap. A side view hides the hip turn.],
  moves: [
    + Left foot on 1, right foot on 2. Right hand to B. Hang on your straight right arm.
    + Right foot to 3, then left foot to 2.
    + Left hand to C.
    + Left foot to 3, beside your right. Right foot up to A, on its outside edge. Drive the toe in and pull. Keep your whole body tight and your hips in.
    + #jt("lock-off", body: [Lock off]) on C. Turn your right hip in and take D with your right hand. Use a small #tref("deadpoint", body: [deadpoint], show-page: false) (a catch at the top of your rise) if you need one. Square your hips once you hold it.
    + Left foot up to A beside your right. Right foot to B.
    + Deadpoint to E: rise with your right hand on D and let go as the rise slows. Then left hand to E.
  ],
  crux: [Moves 5 to 7. C is a flat edge, which loses grip as you turn #src("B38"). Your toe is on a thin edge while your hand goes to the worst hold. Then both feet come up: D rolls and C drops to your waist. So go for E in one movement.],
  wrong: [You stay on the big foothold and reach for D. From feet 2 and 3, D is about 30 cm out of reach. From both feet on 3 you reach it only with both legs straight. Your feet tend to come off #src("E8") and you land on a sloper with no tension (judgement). With your left foot on 3, a higher right foot adds no reach. It keeps one leg bent to pull and drive with.],
  next: [If the toe pops, place it again and press it down and in #src("A6", "A38"). If your hand rolls off D, your hips swung out: pull them in. Both toes on A give about 45 cm more reach, but you catch D with your hips out and it rolls sooner #src("C2", "C3", "C11"). From both toes on A you could skip D, but nothing is above you as you rise to E (judgement).],
  tall: [You can reach D from both feet on 3, so A can wait until you hold D.],
  small: [Left foot to 3 before your left hand goes to C. From 3 and A you are 15 cm short of D, so put both toes on A or deadpoint off A. Finish: right foot to 4, left foot to B.],
  entries: ("toe-pull", "body-tension", "sloper", "deadpoint"),
)

#reading-question(
  n: 5, title: [Sit start], grade: 4,
  wall: [The wall overhangs 15°, seen from behind.],
  start: [sitting on the mat with your left hand on A, your right hand on B and your feet on 1 and 2.], finish: [both hands on F.],
  figure: "reading-v4-sit.svg",
  prompts: [
    - *Step 1.* What do you need to check with your gym before you move off a sit start?
    - *Step 4.* Give C, D and E an L or an R.
    - *Step 5.* What can your hips do as your bottom lifts? What does each foot do?
    - *Step 5, your size.* Work out how many bolt holes your reach covers (toes to fingers, at 20 cm a hole). Take off one: feet 1 and 2 are too far apart to stand up straight. Then count the holes from foothold 2 to C. Can you reach it before your feet move? If not, or only just, which footholds would help? How high are they compared with your hips?
    - *Step 6.* Where will you need the most power?
  ],
)
#reading-answer(
  n: 5,
  figure: "reading-v4-sit-answer.svg",
  caption: [Move 3. The feet went first: the discs are moves 2 and 3. The right hand reaches C.],
  moves: [
    + Left foot on 1, right foot on 2. Sit close to the wall and hang from A and B.
    + Left foot to 4, about 45 cm above your hips. Rock back a little, then pull your bottom off the mat in one movement #src("E11"). As it lifts, turn your right hip to the wall and roll onto the right foot's outside edge.
    + Right foot to 3, on its big-toe edge. Your hips come square so this foot can push. Rise between 3 and 4. Right hand to C as a small #tref("deadpoint", body: [deadpoint], show-page: false) (a catch at the top of your rise). By then A is at your waist and can only press.
    + Press on A and rise until your hips clear 5. Right foot to 5: D comes well within reach.
    + Left hand to D. Left foot up to A. Right hand to E. You could skip E from foot 6, but C drops below your shoulder as you stand. E stays above it.
    + Right foot to 6. Stand up and catch F with your right hand. Then left hand to F.
  ],
  crux: [Moves 2 and 3. You pull off the mat on two flat edges. A flat edge loses grip as you turn #src("B38"). At the catch A is at your waist, so your hand must arrive at the top of your rise.],
  wrong: [You pull straight for C from feet 1 and 2. You can touch it, but only at full stretch with your left leg long. Your left hand is locked at your chest on a thin edge, with no rise left to help it (judgement). Feet 4 and 3 give you about 30 cm to spare. But set both of them before you lift and you fold up square with your bottom away from the wall. The first pull is then all arms #src("E11").],
  next: [Roll your right knee onto the mat and push off it #src("E11"). Don't bounce off the mat if your gym wants a still start (judgement).],
  tall: [You can go hand first: C is in reach from feet 1 and 2, so long legs can skip the high step. Bring your left foot to 4 once your hand is on C. You can still go foot first: see the one high foot in the book's #bref("fig-cons-sit", sub: "\u{a0}c").],
  small: [A and B are a full stretch from the mat, so you can't rock back. C is out of reach from feet 1 and 2, so you must step up first. Finish with a small deadpoint to F. Your left foot comes off A, so press it on the wall and match (judgement).],
  entries: ("sit-start", "hip-turn", "edging", "deadpoint"),
)

#reading-question(
  n: 6, title: [Long gap], grade: 5,
  wall: [The wall overhangs 25°, seen from behind.],
  start: [left hand on A, right hand on B.], finish: [both hands on F.],
  figure: "reading-v5-gap.svg",
  prompts: [
    - *Step 3.* Which holds could stop a moving body? How many hands fit on E?
    - *Step 4.* Give C, D, E and F an L, an R or both.
    - *Step 5.* Which footholds are biggest? Count the holes to E from each one. Which let you reach it?
    - *Step 6.* Static, #jt("deadpoint") (a catch at the top of your rise, feet on) or #jt("dyno") (a jump, feet off)? What would change your answer?
    - *Step 7.* What is the setter testing?
  ],
)
#reading-answer(
  n: 6,
  figure: "reading-v5-gap-answer.svg",
  caption: [Move 6. The top of the deadpoint.],
  moves: [
    + Right foot on 1, left on 2. Left foot to 3, right foot to 4.
    + Left hand to the left end of C.
    + Right foot to 6 under E, on the #tref("edging", body: [inside edge], show-page: false) of your shoe. Left foot to 5.
    + Right hand up to C, beside your left. From B it can't hold you in while your left hand moves (judgement).
    + Lock off on C with your right arm and take your left hand up to D. Your left arm can hang straight there. At the catch of E, D is above your shoulder. C would be below.
    + Let your hips sag out on that straight arm #src("D10"). Drive through your right leg in one movement, hips in and up #src("D13"). Send your right hand from C to 2–3 cm above E #src("D16"). Close it in a #tref("half-crimp", body: [half crimp], show-page: false) at the top: a full crimp at speed risks your fingers #src("C25"). Then push down through your right foot #src("D21").
    + Left foot up to A. Right foot up to B and stand.
    + Left hand to F, then right hand to F.
  ],
  crux: [Move 6. The question is whether you choose a #tref("deadpoint", body: [deadpoint], show-page: false). E takes one hand and has a foothold under it, so you want a foot on as you catch it. A slow #jt("lock-off") may just reach E. But it keeps you on one bent arm on D for the whole reach #src("D13"). Stepping a foot up to A or B shortens the rise, but it folds you up with your hips out (judgement). With both feet on A and B you can skip E for F. But D is then no higher than your shoulder as you throw, so nothing holds you in (judgement). A dyno would suit a jug at E with no foot 6.],
  wrong: [It looks like a #tref("dyno", body: [dyno], show-page: false): no hold above B on that side until E, and two big footholds low down. So with your left hand on C you stand on 3 and 4, sink and jump. That is about twice the rise. Even if you stick E, your feet are off. Small edges must then stop the swing, which may pull you off (judgement).],
  next: [If you fall short, drive your hips in and up #src("D10", "D17"). Or use your outside edge on 6 for a #jt("hip pop", body: [hip~pop]) #src("D7", "D10"). If your fingers touch and slide, send your hand sooner.],
  tall: [E is well within reach from feet 5 and 6, so your deadpoint can be small.],
  small: [E is out of reach from 5 and 6. From A and 6 you are still short. Step both feet up to A and B #src("H2", "H3"): your hips fold out, but E is in reach (judgement).],
  entries: ("deadpoint", "dyno", "latching"),
)

#reading-question(
  n: 7, title: [Volumes], grade: 5,
  wall: [The wall overhangs 25°, seen from behind. Y stands about 45 cm off the wall. Neither volume has an edge to grip.],
  start: [both hands on A.], finish: [both hands on B.],
  figure: "reading-v5-volumes.svg",
  prompts: [
    - *Step 3.* Which way do the faces of Y point?
    - *Step 4.* Where can each hand go after A? Does the order matter?
    - *Step 5.* Count the holes from your toes on X to B. What must you stand on to reach it?
    - *Step 6.* Where is the crux? How long does it last?
  ],
)
#reading-answer(
  n: 7,
  figure: "reading-v5-volumes-answer.svg",
  caption: [Start of move 3. The palms press in with the elbows down. The feet squeeze X.],
  moves: [
    + Right foot on 1, left foot on 2. Left foot onto the left upper face of X, right foot onto the right. Squeeze X between your feet.
    + Rise on X only until your left hand reaches the left face of Y: palm flat, elbow down. Your hips are still below A, so your right hand can still pull. Before they pass A, right hand to the right face, palm flat. Until it lands, nothing holds you in.
    + Stand a little taller on your right foot, so your left knee has room. Left foot up to A, the old start hold. It is the nearest foothold, so your foot is off for the least time. Move it fast.
    + Right foot to 4. Move your hips right round Y. Drive off both feet in one movement. Take B with your right hand as a #tref("deadpoint", body: [deadpoint], show-page: false). It is nearly 12 holes from your toes on X and under ten from A. Your left palm only steers.
    + Left hand to B.
  ],
  crux: [Moves 2 to 4, from the moment your right hand leaves A until it catches B. This is #tref("compression", body: [compression], show-page: false). On X your feet can only push you out, so only the squeeze holds you in. Once your right hand leaves Y, nothing does. So don't pause.],
  wrong: [You stand up on X and reach for the top of Y with one hand, the other still on A. To reach it your hips must pass A, so you can only press down on A. On an overhang a press can't hold you in, so you fall away from the wall (judgement). Feet 3 and 4 don't save it: with your hands on A, your hips can't rise over them. Y's side faces point sideways and out, so pulling down on them only slides your hands off. A #tref("knee-bar", body: [knee bar], show-page: false) under Y won't hold either: the underside slopes out, so your knee slides off (judgement). When a volume has no edge, squeeze it instead of pulling down.],
  next: [Squeeze from your chest and back as in a hug. Keep your hips close and trunk tight #src("B31"). If a foot pops, press your free foot on a foothold or the wall #src("B45"). Left or right first doesn't matter: you can climb the mirror image. A foot on A before your second hand does: it is easier on the palms. So if the squeeze won't last, take Y with your right hand first, hips low and well left of A. Left foot to A, then left hand to Y. Chalk your whole hand #src("E18").],
  small: [B is out of reach with both feet on. Let your left foot leave A as you drive.],
  entries: ("compression", "volume", "palming", "body-tension"),
)

#reading-question(
  n: 8, title: [Cave], grade: 6,
  wall: [The wall overhangs 40°, seen from behind. C has room for one hand.],
  start: [left hand on B, right hand on C.], finish: [both hands on F.],
  figure: "reading-v6-cave.svg",
  prompts: [
    - *Step 3.* Which way does each hold face?
    - *Step 4.* Give each hold above the start an L or an R.
    - *Step 5.* Look where the footholds sit. Which start hand can't let go without your body swinging? What could stop the swing?
    - *Step 6.* Where is the crux?
  ],
)
#reading-answer(
  n: 8,
  figure: "reading-v6-cave-answer.svg",
  caption: [Move 3. The toe hook holds you in. The dashed line is the #jt("hinge").],
  moves: [
    + Left foot on 1, right foot on 2. Rise on your right foot. A faces left: hook the top of your left toes behind it. Bend the ankle up towards your shin and keep the leg nearly straight. Hold it with leg tension and don't curl your toes #src("A13").
    + Keep both hands on. Right foot up to 3.
    + Press up on your right foot until the hook leg goes tight. Keep your right arm straight at first and lock it as your shoulders reach C. Left hand to D with a small deadpoint.
    + Your left hand and right foot now oppose each other, so take the hook off in small steps #src("A12"). Left foot to B, then right foot to 4.
    + Right hand to E. You may skip it with a deadpoint to F.
    + Right hand to F, then left hand to F.
  ],
  crux: [Move 3. When your left hand lets go of B, your right hand and right foot hold you on one side. You swing open like a door unless something stops it. C faces up and right, so it takes the hook's pull. D faces up and left, so it holds as you catch it.],
  wrong: [Your right hand and foot call for a #tref("back-flag", body: [back flag], show-page: false), so you try one. A flag wants your hips over your right foot #src("B26"). To reach D from there, C must come down to your chest. There it can only press, so it can't hold you in (judgement). Stay low with your hips towards D and the door opens. A #tref("toe-hook", body: [toe hook], show-page: false) on the left holds you in with C at your shoulder #src("A15"). With all the footholds on one side, try a backstep or a hook on the other.],
  next: [If the toe creeps out, pull it and your right hand towards each other #src("A13"). A heel behind A also holds you in and brings D closer, but your hips sit further from the hinge (judgement). A #tref("backstep", body: [backstep], show-page: false) with your left foot on 3 and your right leg out is another option. It puts your outside edge on a small foothold #src("B44") and costs a little more lock. A fast throw from feet 2 and 3 can beat the door #src("B62"), but you land on D at full stretch and swinging.],
  tall: [Your longer lever makes the hook harder to hold (judgement). Try the backstep.],
  small: [From the hook, D is out of reach. Use a bigger deadpoint or the backstep.],
  entries: ("toe-hook", "barn-door", "back-flag", "backstep"),
)
