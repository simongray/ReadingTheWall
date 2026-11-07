#import "../template.typ": *

// The steps of the method are subheads: the label in small caps, the
// title on the subhead step of the scale.
#let step(n, title) = block(above: gap(1.5), below: gap(0.35), breakable: false, sticky: true,
  text(size: fs.sub)[#section-label[Step #n]#h(0.6em)#text(weight: 700, title)])

= Reading a problem

Reading a #jt("problem") (an indoor boulder route) means working out how to climb it before you touch it. You find the start and the finish. You decide which hand goes on which hold, where your feet go and where it will get hard. Then you rehearse it in your head.

Good readers don't guess better. They have a method and compare what they read with moves they have already done. This chapter gives you that method, then covers planning attempts, resting between them and reading gym grades. It ends with eight problems to read for yourself.

== Why read first

#ix("Route reading", main: true)
- *Reading changes how you climb.* In one study, 29 male climbers on roped indoor routes had three minutes to look at some routes before they climbed them. Looking didn't change how often they reached the top, but they did make fewer and shorter stops. Part of that held up once the authors allowed for ability, with the experts gaining most#ix("Studies!previewing a route") #src("E34").
- *Experts read in chunks.*#ix("Experts and novices!route reading") Expert climbers describe moving from the whole route to the details. They split it into sections and mark the hard parts and the rests. They look for "traps"#ix("Route reading!traps"): places where arriving with the wrong hand forces a fall #src("E35").
- *You read with the moves you know.* Experts remembered the holds of a hard route better than novices, though on easy routes there was no difference #src("E36"). In a virtual climbing task, novices also made more short-sighted plans, picking nearby holds that weren't part of the right sequence #src("E37"). Earlier studies suggest that experts see more readily what a hold can be used for #src("E38").
- *Good climbers take time over it.* In the qualification and semi-final rounds of one 2018 World Cup#ix("World Cup!time spent reading"), boulderers looked for about 50 seconds before their first attempt #src("E40").

You can't read a move you have never felt, so every new move you learn on the wall makes you a better reader.

== The method, step by step <reading-method>

Run these steps at the bottom of every problem you want to climb first try. On a warm-up, steps 1 to 3 are enough. @reading-problems gives you eight drawn problems to practise on.

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


#step(5)[Find the feet]

- Holds with rubber marks and no chalk are probably footholds#ix("Route reading!footholds") #src("E30", "E31").
- On steep ground, look for footholds you can use with the outside edge of the shoe. Under roofs, look for #tref("heel-hook", body: [heel hooks], show-page: false) and #tref("toe-hook", body: [toe hooks], show-page: false) #src("E30").
- Look for moves where a #tref("flag", body: [side flag]) saves you swapping feet twice in a row #src("E30", "E12").
- Read the feet together with the hands, because the next hand move depends on where your feet are #src("E35").
- Don't try to plan every foot. The coach Neil Gresham#ix("Gresham, Neil") says the full foot sequence is the hardest part to predict #src("E30"). At V3–V4, plan the feet for the start and the hardest move. Sort out the rest on the wall (judgement).

#filmstrip("filmstrip-worked-problem.svg", [Climbing the worked problem], [Watch the right foot: it steps up onto the high foothold before the left hand crosses to L4.])

#step(6)[Find the crux, the traps and the rests]

- The #jt("crux") is the hardest move or section. It may be a jump, a balance move, a move where your feet come off, or small holds #src("E29"). Decide how you will do it before you start#ix("Crux!reading") #src("E29").
- Find the traps, where the wrong hand forces a fall. Expect some near the start (judgement).
- Rests#ix("Resting on the wall") are places to #jt("shake out") (hang on one arm and shake the other). Look for big holds and ledges, and on harder problems #tref("knee-bar", body: [knee bars], show-page: false) and heel hooks #src("E29", "E30", "E32").
- Split the problem into sections at the crux and at changes of style, such as overhang to slab. Don't try to memorise every move #src("E32").

#step(7)[Guess what the setter intended]

@reading-setter lists what setters say they do. Ask yourself what movement this problem is~testing.

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

// a new page: the sentence that announces the table, the table and the figure are read
// together. The paragraph and the key point that close the section may go over together.
#pagebreak(weak: true)
== Hold direction and body position

#ix("Direction of pull")
This table applies the rule from Chapter 1 to each kind of hold. Use it on every hold of a new~problem.

#{
  set par(justify: false)
  table(
    columns: (auto, 2.4cm, 1fr, 1.1fr),
    table.header(th[Hold], th[Faces], th[Where your body goes], th[Which hand, and the cue]),
    [#tref("jug", body: [Jug], show-page: false) or edge], [Up], [Below it. Pull down.#ix("Jug!body position")], [Either hand. Hips under it, arm straight on steep ground.],
    [#tref("sidepull", body: [Sidepull], show-page: false)], [Away from your body], [On the side you pull towards. Lean away from the hold and turn a hip in#ix("Sidepull!body position") #src("E21", "E29").], [The hand on the hold's side. A hold on your left facing left takes the left hand. Your body goes to its right.],
    [#tref("gaston", body: [Gaston], show-page: false)], [Towards your middle], [Stay close to it. Push it away from you with the elbow out and the thumb down#ix("Gaston!body position") #src("E21").], [A hold on your right facing left takes the right hand.],
    [#tref("undercling", body: [Undercling], show-page: false)], [Down], [Rise until it sits at your waist. Pull up with your feet high#ix("Undercling!body position") #src("E21").], [Best at waist or chest height. Stand up into it.],
    [#tref("sloper", body: [Sloper], show-page: false)], [No edge], [Stay low, with your #jt("centre of gravity") (your balance point) below the hold. Keep the arm straight#ix("Sloper!body position") #src("E11", "E18").], [Move the hips first when you go sideways #src("E11").],
    [#tref("volume", body: [Volume], show-page: false) face], [Any direction], [Put your feet on the far side, hips over them#ix("Volumes!body position") #src("E5", "E18").], [Press with a palm. Grip edges with a "meat hook": palm on one face, fingers over the other #src("E18").],
  )
}


// non-breaking spaces: the head breaks after "first", not before "wall"
#fig("reading-hold-orientation.svg", caption: [Each hold puts the body in a different place. (a) Jugs: hang below. (b) A sidepull facing right: right hand, body to its left, leaning away. (c) An undercling: pull up, feet high. (d) A gaston on the right facing left: right hand, pushed away from the body with the elbow out.])

#lead-in[A hold that faces the "wrong" way for the hand you planned tells you that you need the other hand, a cross or a different body position. The hand techniques are in Chapter 5.]

#keypoint[Find which way the hold faces, then pull the opposite way, with your body on the side you are pulling towards. Gastons are the exception: push them away from your middle.]

== What to read first on~each~kind~of~wall <reading-first>

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

Climbers often find a sequence the setter didn't expect #src("E54"). On #jt("comp style", body: [comp-style problems]) (jumpy, competition-like), read from the top down.#ix("Comp-style setting!reading") Use chalk marks, thumbprints and shoe marks as clues #src("E5").

What setters say they do:

- *They avoid ladders.* Easier problems get matches and crosses too, and sometimes an easy #tref("heel-hook", body: [heel hook], show-page: false) or dyno #src("E46", "E47"). Harder ones get intricate sequences, big #tref("sloper", body: [slopers], show-page: false), or big holds with small footholds #src("E46").
- *They force body positions.* Setters remove footholds or put the one useful foothold far to one side, which makes you think about balance #src("E48").

#notebox("Setter clichés you will meet")[
#ix("Setting!clichés")Setters warn each other about these habits #src("E46", "E47", "E48"), which means you will still meet~them.
- *The ladder:* each foot follows a hand up a line of holds #src("E47").
- *Extra feet:* a row of footholds added as a shortcut #src("E46").
- *Reach as difficulty:* a hard grade made by spacing holds far apart. Tall setters do this without noticing #src("E47", "E48").
- *Jugs for easy, crimps for hard:* easy problems get only big holds, while hard ones get #jt("crimp", body: [crimps]) (small edges) and big spans #src("E46").
]

== Other people's beta, and~reading~for~your~size

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

#run-in[*Flashing.* In a study of the 2019 World Cup#ix("World Cup!success by attempt") finals, the first attempt on a steep problem succeeded about 21% of the time. The rate fell with each try, to 6% on the fifth, and the authors call the first attempt a finalist's best chance there. On #tref("slab", body: [slab], show-page: false) and slab-like problems the rate rose, from about 15% on the first to 22% on the second and third. The authors ran no statistical test on these rates and warn that skill probably skews them, because better climbers finish earlier. Finalists also rest very little, about 30 seconds between tries #src("E6"). The climbers still trying after a failed attempt tend to be those the problem suits least, so these rates can't show that your own chance falls after one try (judgement).]

You only get one flash and your arms are at their freshest, so on steep problems put everything into the first try (judgement). On slab, a failed first try costs you less (judgement).

Your flash routine#ix("Flashing!routine"), built from the steps above:

+ Run steps 1–8. Spend about a minute looking.
+ Mime the crux.
+ Rest fully.
+ Climb at a steady pace. Don't stop on the wall to re-read.

#run-in[*Projecting.*#ix("Projecting!method") Choose a project no more than two or three grades above what you usually climb in a session #src("E41"). Then:]

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

#lead-label[Why grades differ between gyms.#ix("Grades!indoor variation")]

- *The spread is large.* An analysis of 40 US gyms#ix("Studies!grades in 40 US gyms") found grades differing by two to four V-grades between gyms. The author reckons a solid V4 climber could expect anything from V2 to V6, depending on the gym #src("E53"). It is a blog analysis by a gym-listing website's founder, not a peer-reviewed study.
- *Gym type and walls.* Large commercial chains graded about one V-grade #jt("soft", body: [softer]) (easier for the number) than gyms focused on training. Steep gyms graded harder, while gyms with lots of slab or competition-style setting graded softer #src("E53").
- *Many beginners.* Gyms offer many easy problems and tend to soften the lower grades instead of splitting them. That softness can reach the middle grades too #src("E57").
- *Style and sequence.* Slab, overhang and dynamic problems test different skills. One awkward move can make a whole problem feel harder. A setter's energy on the day plays a part, as does beta the setter didn't expect #src("E54").
- *Your body.* Height, reach, finger size and style all change how a grade feels #src("E57", "E51", "E46").

We found no peer-reviewed study of indoor grade consistency.

*Colours and circuits.*#ix("Circuits") Some walls group problems into a #jt("circuit"): a colour that covers one grade or a range of two or three #src("E55"). One aim is to play down grades and encourage you to try everything. Colour ranges often overlap, so a problem in a harder colour isn't always harder #src("E56"). Two US gyms use five colours each, such as V0–V2, V2–V4, V4–V6, V6–V8 and V8 and up #src("E52"). Some gyms use colours with no V-grades at all, or their own scales #src("E57"). UK walls mostly use Font or V-grades for bouldering #src("E55").

#lead-label[Calibrating yourself in a new gym.#ix("Grades!in a new gym")]

+ Ask the staff how their system works and how it compares with standard grades #src("E55", "E56").
+ Warm up three or four grades below your maximum. Start below your limit while you learn the gym's style #src("E53", "E56").
+ In the first week, climb as many problems as you can in 15 minutes, two grades below your usual maximum. Repeat every two weeks and compare the counts between gyms #src("E53").
+ Pick one reference problem at your home gym for each style: steep overhang, small edges, slab, jumps and squeezing. After three or four sessions, compare the new gym's problems with them #src("E53").
+ Keep track of which problems you climb reliably and which feel harder or easier for your body #src("E51").

#keypoint[Judge a new gym by style, not by the number on the tag. \ A V4 there can be your V3 or your V5.]

== Eight problems to read <reading-problems>

#ix("Route reading!practice problems", main: true)
These eight problems are invented for this book. No gym has set them and nobody has climbed them, so the grades are rough and the #jt("beta") is this book's judgement. They run from about V2 to about V6 in different styles. The harder ones are worth reading even if you can't climb that grade yet.

Read each drawing with the method in @reading-method. Answer the prompts and make your plan, then turn the page and compare. Your beta may be as good as this one, especially if you are much taller or smaller than the climber in the drawings. That climber stands about 1.75 m and reaches about 2.1 m from toes to fingers (about ten and a half bolt holes).

Letters mark holds big enough for a hand. Numbers mark holds only a foot can use, though a lettered hold can still take a foot. Letters and numbers run up the wall (or along it on the traverse), so their order says nothing about the sequence. Tape marks the start, and volumes count. The dots are bolt holes 20 cm apart, so you can count distances as "Reading for your size" suggests. Short streaks on a hold are shoe rubber. A smudge just below its lip is chalk.

On the answer drawings, D R3 means hold D, taken by the right hand as the third hand move. The numbered moves also count the feet, so the two numbers don't match.

#reading-question(
  n: 1, title: [Slab], grade: 2,
  wall: [The wall leans back 15°, seen from behind.],
  start: [both hands on A, feet on 1 and 2.], finish: [both hands on E.],
  figure: "reading-v2-slab.svg",
  prompts: [
    - *Step 2.* The wall leans back. What does @reading-first say to read first?
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
  tall: [Hand first works: C is in reach from feet 1 and 2, so long legs can skip the high step. Bring your left foot to 4 once your hand is on C. Foot first still works: see the one high foot in @fig-cons-sit c, under @cons-tall.],
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
  next: [Squeeze from your chest and back as in a hug. Keep your hips close and trunk tight #src("B31"). If a foot pops, press your free foot on a foothold or the wall #src("B45"). Left or right first doesn't matter: the mirror image also works. A foot on A before your second hand does: it is easier on the palms. So if the squeeze won't last, take Y with your right hand first, hips low and well left of A. Left foot to A, then left hand to Y. Chalk your whole hand #src("E18").],
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
  next: [If the toe creeps out, pull it and your right hand towards each other #src("A13"). A heel behind A also holds you in and brings D closer, but your hips sit further from the hinge (judgement). A #tref("backstep", body: [backstep], show-page: false) with your left foot on 3 and your right leg out also works. It puts your outside edge on a small foothold #src("B44") and costs a little more lock. A fast throw from feet 2 and 3 can beat the door #src("B62"), but you land on D at full stretch and swinging.],
  tall: [Your longer lever makes the hook harder to hold (judgement). Try the backstep.],
  small: [From the hook, D is out of reach. Use a bigger deadpoint or the backstep.],
  entries: ("toe-hook", "barn-door", "back-flag", "backstep"),
)
