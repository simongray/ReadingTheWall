#import "../template.typ": *

// The steps of the method are subheads: the label in small caps, the
// title on the subhead step of the scale.
#let step(n, title) = block(above: gap(1.5), below: gap(0.35), breakable: false, sticky: true,
  text(size: fs.sub)[#section-label[Step #n]#h(0.6em)#text(weight: 700, title)])

= Reading a problem

Reading a #jt("problem") (an indoor boulder route) means working out how to climb it before you touch it. You find the start and the finish. You decide which hand goes on which hold, where your feet go and where it will get hard. Then you rehearse it in your head.

Good readers don't guess better. They have a method and compare what they read with moves they have already done. This chapter gives you that method, then covers planning attempts, resting between them and reading gym grades.

== Why read first

#ix("Route reading", main: true)
- *Reading changes how you climb.* In one study, 29 male climbers on roped indoor routes had three minutes to look at some routes before they climbed them. Looking didn't change how often they reached the top, but they did make fewer and shorter stops. Part of that held up once the authors allowed for ability, with the experts gaining most#ix("Studies!previewing a route") #src("E34").
- *Experts read in chunks.*#ix("Experts and novices!route reading") Expert climbers describe moving from the whole route to the details. They split it into sections and mark the hard parts and the rests. They look for "traps"#ix("Route reading!traps"): places where arriving with the wrong hand forces a fall #src("E35").
- *You read with the moves you know.* Experts remembered the holds of a hard route better than novices, though on easy routes there was no difference #src("E36"). In a virtual climbing task, novices also made more short-sighted plans, picking nearby holds that weren't part of the right sequence #src("E37"). Earlier studies suggest that experts see more readily what a hold can be used for #src("E38").
- *Good climbers take time over it.* In the qualification and semi-final rounds of one 2018 World Cup#ix("World Cup!time spent reading"), boulderers looked for about 50 seconds before their first attempt #src("E40").

You can't read a move you have never felt, so every new move you learn on the wall makes you a better reader.

== The method, step by step <reading-method>

Run these steps at the bottom of every problem you want to climb first try. On a warm-up, steps 1 to 3 are enough.

#step(1)[Rules and boundaries]

- Use only holds of the problem's colour or tape#ix("Gym rules") #src("E65").
- Find the start.#ix("Start holds") Most gyms mark it with extra tape, a coloured box or the grade tag. Put your hands on the start hold or holds #src("E65").
- Some rules vary between gyms. Can both hands share one start hold? Must your feet use marked holds? Do #tref("volume", body: [volumes], show-page: false) (big hollow shapes bolted to the wall) count? Volumes often count for every problem on that wall#ix("Volumes!gym rules") #src("E19"). If in doubt, ask the staff #src("E55").
- A #tref("sit-start", body: [sit start]) is usually marked on the tag. Find out whether you must be still on the start holds before you move (judgement).
- Find the finish. It is either a marked top hold or a #tref("top-out", body: [top-out]) onto the top of the wall #src("E65"). Most gyms expect both hands on the top hold, under control (judgement).
- Find the way down#ix("Downclimbing!finding the way down") before you start #src("E33", "E65").

#step(2)[Stand back, then walk around]

- Look from several angles and from well back, so you see bulges and the top #src("E30", "E11").
- Get close to the base of the wall to spot #tref("undercling", body: [underclings], show-page: false) (holds you pull upward). Stand to the side to see #tref("sidepull", body: [sidepulls], show-page: false) and edges angled into the wall #src("E30").
- Read the top too, because tunnel vision is worst there #src("E30"). You may think the hardest move is low down, only to fail at the top #src("E33").

#step(3)[Read each hold's direction]

Work out which way each hold faces and where that puts your body (the next section explains how). Chalk on a hold shows where people grip it,#ix("Chalk marks") but watch out for false marks from people who used it wrongly #src("E30", "E31").

#step(4)[Count the hands]

#ix("Hand sequence")
+ Number the handholds from the start to the finish.
+ Give each hold an L or an R from its direction (step 3).
+ Check the order. If two holds in a row need the same hand, you can #tref("matching", body: [match], show-page: false) (put both hands on one hold), #tref("cross-through", body: [cross], show-page: false) (move one hand over the other) or move the same hand twice (judgement).
+ Where you can't decide, list the options in order: cross, match or go again. Choose when you feel the holds #src("E30").
+ Pick two or three #jt("marker hold", body: [marker holds]): big, easy-to-remember holds that anchor the sequence. The rest hangs off them #src("E30").
+ Expect at least one move that is not a straight ladder. Setters use matches, crosses, underclings and sidepulls even on easy problems #src("E46"). They also use left–right sequences to force a particular movement #src("E48").

#fig("reading-worked-problem.svg", caption: [A worked reading. Start with both hands on the taped hold. R1 is a sidepull facing right, so the right hand takes it. L4 lies to the right of R3, so the left hand must cross over. The cross and the slap to R5 form the crux (the hardest part). A high right foot sets up the cross. R3 is a jug where you can rest.])

#filmstrip("filmstrip-worked-problem.svg", [Climbing the worked problem], [Watch the right foot: it steps up onto the high foothold before the left hand crosses to L4.])

#step(5)[Find the feet]

- Holds with rubber marks and no chalk are probably footholds#ix("Route reading!footholds") #src("E30", "E31").
- On steep ground, look for footholds you can use with the outside edge of the shoe. Under roofs, look for #tref("heel-hook", body: [heel hooks], show-page: false) and #tref("toe-hook", body: [toe hooks], show-page: false) #src("E30").
- Look for moves where a #tref("flag") saves you swapping feet twice in a row #src("E30", "E12").
- Read the feet together with the hands, because the next hand move depends on where your feet are #src("E35").
- Don't try to plan every foot. The coach Neil Gresham#ix("Gresham, Neil") says the full foot sequence is the hardest part to predict #src("E30"). At V3–V4, plan the feet for the start and the hardest move. Sort out the rest on the wall (judgement).

#step(6)[Find the crux, the traps and the rests]

- The #jt("crux") is the hardest move or section. It may be a jump, a balance move, a move where your feet come off, or small holds #src("E29"). Decide how you will do it before you start#ix("Crux!reading") #src("E29").
- Find the traps, where the wrong hand forces a fall. Expect some near the start (judgement).
- Rests#ix("Resting on the wall") are places to #jt("shake out") (hang on one arm and shake the other). Look for big holds and ledges, and on harder problems #tref("knee-bar", body: [knee bars], show-page: false) and heel hooks #src("E29", "E30", "E32").
- Split the problem into sections at the crux and at changes of style, such as overhang to slab. Don't try to memorise every move #src("E32").

#step(7)[Guess what the setter intended]

@reading-setter lists what setters say they do. Ask yourself: what movement is this problem testing?

#step(8)[Rehearse]

- Go through the problem slowly in your head, then again. Gresham suggests two run-throughs for the hand sequence, three when you add rests and four with feet #src("E30").
- Mime#ix("Miming moves") the moves with your hands while you stand in front of the wall, as competitors do #src("E29", "E32").
- Picture yourself at the crux.#ix("Visualisation") One expert memorised the size and shape of each crux so he knew how to position himself when he got there #src("E35").
- Give complex sequences short cue words: "cross, flag, match" #src("E32").

#step(9)[Climb, then compare]

- On the wall, notice where the plan works and where it doesn't #src("E29").
- Back on the mat, compare what you predicted with what happened. Coaches see this review as the way to get better at reading #src("E29", "E30", "E11").
- When you fall, name the reason#ix("Falling!learning from a fall"): a hold you misjudged, a lost sequence or a surprise #src("E31").

#keypoint[Read the whole problem before you touch it, top included. Then count the hands, find the feet for the start and the crux, and mime the crux once.]

== Hold direction and body position

#ix("Direction of pull")
This table applies the rule from Chapter 1 to each kind of hold. Use it on every hold of a new problem.

#keypoint[Find which way the hold faces, then pull the opposite way, with your body on the side you are pulling towards. Gastons are the exception: push them away from your middle.]

#{
  set par(justify: false)
  table(
    columns: (auto, auto, 1fr, 1fr),
    table.header(th[Hold], th[Faces], th[Where your body goes], th[Which hand, and the cue]),
    [#tref("jug", body: [Jug], show-page: false) or edge], [Up], [Below it. Pull down.#ix("Jug!body position")], [Either hand. Hips under it, arm straight on steep ground.],
    [#tref("sidepull", body: [Sidepull], show-page: false)], [Away from your body], [On the side you pull towards. Lean away from the hold and turn a hip in#ix("Sidepull!body position") #src("E21", "E29").], [The hand on the hold's side. A hold on your left facing left takes the left hand. Your body goes to its right.],
    [#tref("gaston", body: [Gaston], show-page: false)], [Towards your middle], [Stay close to it. Push it away from you with the elbow out and the thumb down#ix("Gaston!body position") #src("E21").], [A hold on your right facing left takes the right hand.],
    [#tref("undercling", body: [Undercling], show-page: false)], [Down], [Rise until it sits at your waist. Pull up with your feet high#ix("Undercling!body position") #src("E21").], [Best at waist or chest height. Stand up into it.],
    [#tref("sloper", body: [Sloper], show-page: false)], [No edge], [Stay low, with your #jt("centre of gravity") (your balance point) below the hold. Keep the arm straight#ix("Sloper!body position") #src("E11", "E18").], [Move the hips first when you go sideways #src("E11").],
    [#tref("volume", body: [Volume], show-page: false) face], [Any direction], [Put your feet on the far side, hips over them#ix("Volumes!body position") #src("E5", "E18").], [Press with a palm. Grip edges with a "meat hook": palm on one face, fingers over the other #src("E18").],
  )
}

#fig("reading-hold-orientation.svg", caption: [Each hold puts the body in a different place. (a) Jugs: hang below. (b) A sidepull facing right: right hand, body to its left, leaning away. (c) An undercling: pull up, feet high. (d) A gaston on the right facing left: right hand, pushed away from the body with the elbow out.])

A hold that faces the "wrong" way for the hand you planned tells you that you need the other hand, a cross or a different body position. The hand techniques are in Chapter 5.

// non-breaking spaces: the head breaks after "first", not before "wall"
== What to read first on~each~kind~of~wall

Each kind of terrain hides its key information in a different place, so read that first.#ix("Route reading!by kind of wall")

#{
  set par(justify: false)
  table(
    columns: (auto, 1fr),
    table.header(th[Terrain], th[Read this first]),
    [#tref("slab")], [The feet. Find the best part of each foothold and the #tref("smearing", body: [smears], show-page: false) between them. Handholds only steer you #src("E1", "E4").],
    [#tref("overhang")], [Footholds below and to the side of the handholds. They tell you where to turn your hip in #src("E9", "E11").],
    [#tref("roof")], [The backs and sides of holds, where toes and heels can hook #src("E15", "A12").],
    [#tref("arete")], [Which sections use only the edge and which use face holds #src("E2").],
    [#tref("corner", body: [Corners])], [Footholds, or blank wall, on both walls #src("E20").],
    [#tref("volume")], [The far side of each volume, its edges and the gaps between volumes #src("E18", "E11").],
    [#tref("dynamic-slab")], [The end position of each jump. Read the problem from the top down #src("E5", "E27").],
    [#tref("top-out")], [The shape of the #jt("lip") (the top edge of the wall) and the way down #src("E13", "E33").],
  )
}

== What the setter had in mind <reading-setter>

#ix("Setter intent")
A #jt("setter") (the person who designs the problems) starts from a brief:#ix("Setting!the setter’s brief") who the problem is for, its grade, the movement it uses and how much effort it takes #src("E49"). Some gyms also ask which skills a problem tests and what share of members should finish it #src("E52"). Knowing how setters think helps you find the intended sequence.

What setters say they do:

- *They avoid ladders.* Easier problems get matches and crosses too, and sometimes an easy #tref("heel-hook", body: [heel hook], show-page: false) or dyno #src("E46", "E47"). Harder ones get intricate sequences, big #tref("sloper", body: [slopers], show-page: false), or big holds with small footholds #src("E46").
- *They force body positions.* Setters remove footholds or put the one useful foothold far to one side, which makes you think about balance #src("E48").

#notebox("Setter clichés you will meet")[
#ix("Setting!clichés")Setters warn each other about these habits #src("E46", "E47", "E48"), which means you will still meet them.
- *The ladder:* each foot follows a hand up a line of holds #src("E47").
- *Extra feet:* a row of footholds added as a shortcut #src("E46").
- *Reach as difficulty:* a hard grade made by spacing holds far apart. Tall setters do this without noticing #src("E47", "E48").
- *Jugs for easy, crimps for hard:* easy problems get only big holds, while hard ones get #jt("crimp", body: [crimps]) (small edges) and big spans #src("E46").
]

Climbers often find a sequence the setter didn't expect #src("E54"). On #jt("comp style", body: [comp-style problems]) (jumpy, competition-like), read from the top down.#ix("Comp-style setting!reading") Use chalk marks, thumbprints and shoe marks as clues #src("E5").

== Other people's beta, and reading for your size

#jt("beta", body: [Beta]) is the sequence of moves for a problem. Watching other climbers#ix("Watching others"), asking for advice and talking it over are normal tools#ix("Beta!from other climbers") #src("E29", "E32"). Apps such as Kaya also collect beta #src("E32"). Beta from others has limits, though.

- *Your body changes the beta.* Height and arm span strongly affect how a problem feels, so adapt moves to your body#ix("Beta!adapting to your body") #src("E29").
- *Size is more than reach.* Tall climbers may get bunched up, short climbers#ix("Small climbers") may not reach, and climbers with small hands#ix("Hand size") may not hold wide #tref("pinch", body: [pinches], show-page: false) or #tref("sloper", body: [slopers], show-page: false) well #src("E46").
- *Look for #jt("micro beta").* These are small changes to how you grip and stand, tailored to your size and strength #src("E41").
- *Read before you watch.* Make your plan first, then watch someone climb the problem and compare (judgement).

#notebox("Reading for your size (judgement)")[
#ix("Tall climbers!reading a problem")#ix("Small climbers!reading a problem")These points apply the sources above to your own body, and we found no study that tests them. For more, see @cons-tall and @cons-small. When you copy a shorter climber:
- Expect to skip an intermediate handhold.
- Expect their foot positions to fold you up. Try the next foothold lower or further out, so your arms stay straight.
- If you feel scrunched, the problem was probably set for a shorter span. Stand up on a lower foot, or take a higher handhold earlier.
- Distrust "you just have to jump" from light climbers. Look first for a slow move that uses your reach.

When you copy a taller climber:
- Expect to make more moves where the holds allow. Their one reach may be your two or three, using small holds they skip, so look at holds with little chalk #src("H1", "H8"). Indoors there aren't always more options, because setters decide which holds a problem has #src("H8").
- Read the feet first. A higher foothold may bring the hold within reach #src("H2", "H3"), and so may a place to smear #src("H8"). Someone your own size can show you where #src("H8").
- Check the distance before you believe it's too far. At the wall, count how many bolt holes your reach covers, then count the holes between the holds #src("H9").
- Distrust "you just have to reach", and read little into the grade. One reachy move can stop you on a V1 even if you climb most V3s #src("E51").
]

== Flash or project?

#ix("Flashing")
#ix("Projecting")
To #jt("flash") a problem is to climb it on your first try. To #jt("project") it is to work on it over several attempts or sessions. The two need different tactics.

*Flashing.* In a study of the 2019 World Cup#ix("World Cup!success by attempt") finals, the first attempt on a steep problem succeeded about 21% of the time. The rate fell with each try, to 6% on the fifth, and the authors call the first attempt a finalist's best chance there. On #tref("slab", body: [slab], show-page: false) and slab-like problems the rate rose, from about 15% on the first to 22% on the second and third. The authors ran no statistical test on these rates and warn that skill probably skews them, because better climbers finish earlier. Finalists also rest very little, about 30 seconds between tries #src("E6"). The climbers still trying after a failed attempt tend to be those the problem suits least, so these rates can't show that your own chance falls after one try (judgement).

You only get one flash and your arms are at their freshest, so on steep problems put everything into the first try (judgement). On slab, a failed first try costs you less (judgement).

Your flash routine#ix("Flashing!routine"), built from the steps above:

+ Run steps 1–8. Spend about a minute looking.
+ Mime the crux.
+ Rest fully.
+ Climb at a steady pace. Don't stop on the wall to re-read.

*Projecting.*#ix("Projecting!method") Choose a project no more than two or three grades above what you usually climb in a session #src("E41"). Then:

+ Learn the single moves first, in isolation. Get the first contact right before you add the second #src("E5"). Then #jt("link-up", body: [link]) the #jt("crux") (climb its moves without stopping), then longer sections #src("E44", "E45").
+ Split the problem at the crux, the rests and the changes of style. Work on one link or one move at a time #src("E32", "E43").
+ Link through the crux and keep going. Big overlapping links show progress better than your high point from the start #src("E44").
+ Practise the easy parts too, because slapping through them wastes energy you need later #src("E41", "E44").
+ Count good attempts and treat each one as information. Decide how many you can make in a day #src("E43").
+ Keep one or two side projects so you stay fresh #src("E43").

#keypoint[After four to six full attempts#ix("Projecting!how many attempts") without progress, change something (judgement). Rest longer, change the sequence or stop for the day.]

The six-attempt figure comes from elite competition. In the 2019 World Cup finals, only one climber finished a problem after a sixth attempt. On steep problems the fifth attempt, after four failures, succeeded only 6% of the time. The authors treat six as a cut-off and say they can't name an ideal number #src("E6"). The climbers still trying by then tend to be those the problem suits least, and they rest little between tries, so treat four to six as a rule of thumb (judgement).

== Rest between attempts

#ix("Rest between attempts", main: true)
How long to rest depends on how hard the attempt is. Problems below your limit need a minute or so. The long rests are for attempts at your limit, on a problem you're projecting or a move you can only just do. If you rest too little before them, you train a different energy system #src("E42").

#{
  set par(justify: false)
  table(
    columns: (1.3fr, 1fr, auto),
    table.header(th[Situation], th[Rest], th[Source]),
    [Easier problems, climbed for endurance], [30–60 seconds between sets], [#src("E42")],
    [A hard problem climbed several times in a row], [1–3 times the climbing time, e.g. about a minute after 30 seconds], [#src("E42")],
    [One move at your limit, tried on its own (a few seconds)], [About 2½ minutes after a 3-second try. The rule is 20–50 times the effort time.], [#src("E42")],
    [A full attempt at your limit (about 30 seconds)], [10–15 minutes], [#src("E42")],
    [Projecting any physically hard problem], [At least 5 minutes, and 10–25 minutes for a long one], [#src("E41")],
    [What competitors actually do under a time limit], [About 2 minutes (a national event, 2010 study); about 30 seconds (a World Cup and the World Championship final, 2018)], [#src("E39", "E40")],
  )
}

So an hour at your limit holds only about four to six full attempts, each made at full strength. Most sessions mix the two: a few limit attempts while you're fresh, and easier problems with short rests (this book's suggestion). The 2018 competition figure describes athletes with four or five minutes per problem. Neither competition figure is advice.#ix("World Cup!rest between attempts") While you rest, watch others try your problem.

== When to change the beta

- When your sessions keep running into dead ends, question the sequence#ix("Beta!when to change") #src("E41").
- When you are stuck or a move feels impossible, find your own #jt("beta") for each move before you ask others, then test new versions #src("E29", "E44").
- After each fall, name the cause (step 9). If it is the sequence, find an easier one. If it is strength, keep the sequence and train #src("E31", "E41").
- Try something new on every attempt, even on familiar moves: a different foot or a different grip #src("E44").
- Change the sequence sooner than the four-to-six rule when you fail at the same point, in the same way, on three fresh attempts in a row. Change it too when the move only works for climbers of a very different size (judgement).

== Indoor grades

#ix("Grades!indoor", main: true)
A grade tells you how hard a problem is meant to be. Indoor grades are a useful guide but a poor measure. Gyms use the #jt("V-scale") (the US scale, from VB and V0 up) or the #jt("Font scale") (the European scale, from 3 up). The conversion table is in the appendix (Grade conversion).

*How a gym grade is made.*#ix("Grades!how gyms grade") The setter usually suggests a grade after a try or two and may adjust it after asking other setters or climbers #src("E58"). Some gyms grade by consensus: their setters #jt("forerun") (test-climb) each other's problems and agree a grade #src("E50"). Forerunning is where setters tweak a problem until it fits the intended grade #src("E46"). One gym writer disagrees, saying that gym grades rarely get feedback and that modern gyms don't grade by consensus #src("E51"). Both are probably true at different gyms.

One setter says what matters most is consistency. A gym can grade hard or easy compared with outdoor rock, as long as its grades stay the same as problems come and go. Regulars then adapt to that gym #src("E46").

*Why grades differ between gyms.*#ix("Grades!indoor variation")

- *The spread is large.* An analysis of 40 US gyms#ix("Studies!grades in 40 US gyms") found grades differing by two to four V-grades between gyms. The author reckons a solid V4 climber could expect anything from V2 to V6, depending on the gym #src("E53"). It is a blog analysis by a gym-listing website's founder, not a peer-reviewed study.
- *Gym type and walls.* Large commercial chains graded about one V-grade #jt("soft", body: [softer]) (easier for the number) than gyms focused on training. Steep gyms graded harder, while gyms with lots of slab or competition-style setting graded softer #src("E53").
- *Many beginners.* Gyms offer many easy problems and tend to soften the lower grades instead of splitting them. That softness can reach the middle grades too #src("E57").
- *Style and sequence.* Slab, overhang and dynamic problems test different skills. One awkward move can make a whole problem feel harder. A setter's energy on the day plays a part, as does beta the setter didn't expect #src("E54").
- *Your body.* Height, reach, finger size and style all change how a grade feels #src("E57", "E51", "E46").

We found no peer-reviewed study of indoor grade consistency.

*Colours and circuits.*#ix("Circuits") Some walls group problems into a #jt("circuit"): a colour that covers one grade or a range of two or three #src("E55"). One aim is to play down grades and encourage you to try everything. Colour ranges often overlap, so a problem in a harder colour isn't always harder #src("E56"). Two US gyms use five colours each, such as V0–V2, V2–V4, V4–V6, V6–V8 and V8 and up #src("E52"). Some gyms use colours with no V-grades at all, or their own scales #src("E57"). UK walls mostly use Font or V-grades for bouldering #src("E55").

*Calibrating yourself in a new gym.*#ix("Grades!in a new gym")

+ Ask the staff how their system works and how it compares with standard grades #src("E55", "E56").
+ Warm up three or four grades below your maximum. Start below your limit while you learn the gym's style #src("E53", "E56").
+ In the first week, climb as many problems as you can in 15 minutes, two grades below your usual maximum. Repeat every two weeks and compare the counts between gyms #src("E53").
+ Pick one reference problem at your home gym for each style: steep overhang, small edges, slab, jumps and squeezing. After three or four sessions, compare the new gym's problems with them #src("E53").
+ Keep track of which problems you climb reliably and which feel harder or easier for your body #src("E51").

#keypoint[Judge a new gym by style, not by the number on the tag. A V4 there can be your V3 or your V5.]
