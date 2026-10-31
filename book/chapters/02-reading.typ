#import "../template.typ": *

// The steps of the method are subheads: the label in small caps, the
// title on the subhead step of the scale.
#let step(n, title) = block(above: gap(1.5), below: gap(0.35), breakable: false, sticky: true,
  text(size: fs.sub)[#section-label[Step #n]#h(0.6em)#text(weight: 700, title)])

= Reading a problem

Reading a #jt("problem") (an indoor boulder route) means working out how to climb it before you touch it. You find the start and the finish. You decide which hand goes on which hold, where your feet go and where it will get hard. Then you rehearse it in your head.

Good readers do not guess better. They have a method. They compare what they read with moves they have already done. This chapter gives you that method, then covers planning attempts, resting between them and reading gym grades.

== Why reading pays off

#ix("Route reading", main: true)
- *Reading improves how you climb.* In one study, climbers had three minutes to look at a route before some attempts. Looking did not change how often they reached the top. It did cut the number and length of their stops on the wall#ix("Studies!previewing a route") #src("E34"). Fewer stops means less time hanging on your arms.
- *Experts read in chunks.*#ix("Experts and novices!route reading") Expert climbers describe moving from the whole route to the details. They split it into sections and mark the hard parts and the rests. They look for "traps"#ix("Route reading!traps"): places where arriving with the wrong hand forces a fall #src("E35").
- *You read with the moves you know.* Experts remembered the holds of a hard route better than novices. On easy routes there was no difference #src("E36"). In a virtual climbing task, novices also made more short-sighted plans. They picked nearby holds that were not part of the right sequence #src("E37"). Earlier studies suggest that experts see more readily what a hold can be used for #src("E38").
- *Good climbers take time over it.* In the 2018 World Cup#ix("World Cup!time spent reading") qualification and semi-final rounds, boulderers looked for about 50 seconds before their first attempt #src("E40").

The practical point: you can't read a move you have never felt. Every new move you learn on the wall makes you a better reader.

== The method, step by step

Run these steps at the bottom of every problem you want to climb first try. On a warm-up, steps 1 to 3 are enough.

#step(1)[Rules and boundaries]

- Use only holds of the problem's colour or tape#ix("Gym rules") #src("E65").
- Find the start.#ix("Start holds") Most gyms mark it with extra tape, a coloured box or the grade tag. Put your hands on the start hold or holds #src("E65").
- Some rules vary between gyms. Can both hands share one start hold? Must your feet use marked holds? Do #tref("volume", body: [volumes], show-page: false) (big hollow shapes bolted to the wall) count? Volumes often count for every problem on that wall#ix("Volumes!gym rules") #src("E19"). If in doubt, ask the staff #src("E55").
- A #tref("sit-start", body: [sit start]) is usually marked on the tag. Find out whether you must be still on the start holds before you move (judgement).
- Find the finish. It is either a marked top hold or a #tref("top-out", body: [top-out]) onto the top of the wall #src("E65"). Most gyms expect both hands on the top hold, under control (judgement).
- Find the way down#ix("Downclimbing!finding the way down") before you start #src("E33", "E65").

#step(2)[Stand back, then walk around]

- Look from several angles and from well back. That shows bulges and the top #src("E30", "E11").
- Get close to the base of the wall to spot #tref("undercling", body: [underclings], show-page: false) (holds you pull upward). Stand to the side to see #tref("sidepull", body: [sidepulls], show-page: false) and edges angled into the wall #src("E30").
- Read the top too. Tunnel vision is worst there #src("E30"). You may think the hardest move is low down, only to fail at the top #src("E33").

#step(3)[Read each hold's direction]

Work out which way each hold faces and where that puts your body. The next section explains this in detail. Chalk on a hold shows where people grip it.#ix("Chalk marks") Watch out for false chalk marks from people who used it wrongly #src("E30", "E31").

#step(4)[Count the hands]

#ix("Hand sequence")
+ Number the handholds from the start to the finish.
+ Give each hold an L or an R from its direction (step 3).
+ Check the order. If two holds in a row need the same hand, you have three options. You can #tref("matching", body: [match], show-page: false) (put both hands on one hold). You can #tref("cross-through", body: [cross], show-page: false) (move one hand over the other). Or you can move the same hand twice (judgement).
+ Where you can't decide, list the options in order: cross, match or go again. Choose when you feel the holds #src("E30").
+ Pick two or three #jt("marker hold", body: [marker holds]): big, easy-to-remember holds that anchor the sequence. The rest hangs off them #src("E30").
+ Expect at least one move that is not a straight ladder. Setters use matches, crosses, underclings and sidepulls even on easy problems #src("E46"). They also use left–right sequences to force a particular movement #src("E48").

#fig("reading-worked-problem.svg", caption: [A worked reading. Start with both hands on the taped hold. R1 is a sidepull facing right, so the right hand takes it. L4 lies to the right of R3, so the left hand must cross over. The cross and the slap to R5 form the crux (the hardest part). A high right foot sets up the cross. R3 is a jug where you can rest.])

#filmstrip("filmstrip-worked-problem.svg", [Climbing the worked problem], [Watch the right foot: it steps up onto the high foothold before the left hand crosses to L4.])

#step(5)[Find the feet]

- Holds with rubber marks and no chalk are probably footholds#ix("Route reading!footholds") #src("E30", "E31").
- On steep ground, look for footholds you can use with the outside edge of the shoe. Under roofs, look for #tref("heel-hook", body: [heel hooks], show-page: false) and #tref("toe-hook", body: [toe hooks], show-page: false) #src("E30").
- Look for moves where a #tref("flag") saves you swapping feet twice in a row #src("E30", "E12").
- Read the feet together with the hands. The next hand move depends on where your feet are #src("E35").
- Don't try to plan every foot. The coach Neil Gresham#ix("Gresham, Neil") says the full foot sequence is the hardest part to predict #src("E30"). At V3–V4, plan the feet for the start and the hardest move. Sort out the rest on the wall (judgement).

#step(6)[Find the crux, the traps and the rests]

- The #jt("crux") is the hardest move or section. It may be a jump, a balance move, a move where your feet come off, or small holds #src("E29"). Decide how you will do it before you start#ix("Crux!reading") #src("E29").
- Find the traps, where the wrong hand forces a fall. Expect some near the start (judgement).
- Rests#ix("Resting on the wall") are places to #jt("shake out") (hang on one arm and shake the other). Look for big holds, ledges, #tref("knee-bar", body: [knee bars], show-page: false) and heel hooks #src("E29", "E30", "E32").
- Split the problem into sections at the crux and at changes of style, such as overhang to slab. Don't try to memorise every move #src("E32").

#step(7)[Guess what the setter intended]

@reading-setter lists what setters say they do. Ask yourself: what movement is this problem testing?

#step(8)[Rehearse]

- Go through the problem slowly in your head, then again. Gresham suggests two run-throughs for the hand sequence, three when you add rests and four with feet #src("E30").
- Mime#ix("Miming moves") the moves with your hands while you stand in front of the wall. Competitors do this #src("E29", "E32").
- Picture yourself at the crux.#ix("Visualisation") One expert memorised the size and shape of each crux so he knew how to position himself when he got there #src("E35").
- Give complex sequences short cue words: "cross, flag, match" #src("E32").

#step(9)[Climb, then compare]

- On the wall, notice where the plan works and where it doesn't #src("E29").
- Back on the mat, compare what you predicted with what happened. Coaches see this review as the way to get better at reading #src("E29", "E30", "E11").
- When you fall, name the reason#ix("Falling!learning from a fall"): a hold you misjudged, a lost sequence or a surprise #src("E31").

#keypoint[Read the whole problem before you touch it, top included. Count the hands. Find the feet for the start and the crux. Mime the crux once.]

== Hold direction and body position

#ix("Direction of pull")
This table applies the rule from Chapter 1 to each kind of hold. Use it on every hold of a new problem.

#keypoint[Find which way the hold faces. Pull the opposite way. Put your body where you are pulling towards. Gastons are the exception: push them away from your middle.]

#{
  set par(justify: false)
  table(
    columns: (auto, auto, 1fr, 1fr),
    table.header(th[Hold], th[Faces], th[Where your body goes], th[Which hand, and the cue]),
    [#tref("jug", body: [Jug], show-page: false) or edge], [Up], [Below it. Pull down.#ix("Jug!body position")], [Either hand. Hips under it, arm straight.],
    [#tref("sidepull", body: [Sidepull], show-page: false)], [Away from your body], [On the side you pull towards. Lean away from the hold and turn a hip in#ix("Sidepull!body position") #src("E21", "E29").], [The hand on the hold's side. A hold on your left facing left takes the left hand. Your body goes to its right.],
    [#tref("gaston", body: [Gaston], show-page: false)], [Towards your middle], [Stay close to it. Push it away from you with the elbow out and the thumb down#ix("Gaston!body position") #src("E21").], [A hold on your right facing left takes the right hand.],
    [#tref("undercling", body: [Undercling], show-page: false)], [Down], [Rise until it sits at your waist. Pull up with your feet high#ix("Undercling!body position") #src("E21").], [Best at waist or chest height. Stand up into it.],
    [#tref("sloper", body: [Sloper], show-page: false)], [No edge], [Stay low, with your #jt("centre of gravity") (your balance point) below the hold. Keep the arm straight#ix("Sloper!body position") #src("E11", "E18").], [Move the hips first when you go sideways #src("E11").],
    [#tref("volume", body: [Volume], show-page: false) face], [Any direction], [Put your feet on the far side, hips over them#ix("Volumes!body position") #src("E5", "E18").], [Press with a palm. Grip edges with a "meat hook": palm on one face, fingers over the other #src("E18").],
  )
}

#fig("reading-hold-orientation.svg", caption: [Each hold puts the body in a different place. (a) Jugs: hang below. (b) A sidepull facing right: right hand, body to its left, leaning away. (c) An undercling: pull up, feet high. (d) A gaston on the right facing left: right hand, pushed away from the body with the elbow out.])

A hold that faces the "wrong" way for the hand you planned tells you something. You need the other hand, a cross, or a different body position. The hand techniques are in Chapter 5.

// non-breaking spaces: the head breaks after "first", not before "wall"
== What to read first on~each~kind~of~wall

Each kind of terrain hides its key information in a different place. Read that first.#ix("Route reading!by kind of wall") Chapter 7 covers each terrain.

#{
  set par(justify: false)
  table(
    columns: (auto, 1fr),
    table.header(th[Terrain], th[Read this first]),
    [#tref("slab")], [The feet. Find the best part of each foothold and the smears between them. Handholds only steer you #src("E1", "E4").],
    [#tref("overhang")], [Footholds below and to the side of the handholds. They tell you where to turn your hip in #src("E9", "E11").],
    [#tref("roof")], [The backs and sides of holds, where toes and heels can hook #src("E15", "A12").],
    [#tref("arete")], [Which sections use only the edge and which use face holds #src("E2").],
    [#tref("corner")], [Footholds, or blank wall, on both walls #src("E20").],
    [#tref("volume")], [The far side of each volume, its edges and the gaps between volumes #src("E18", "E11").],
    [#tref("dynamic-slab")], [The end position of each jump. Read the problem from the top down #src("E5", "E27").],
    [#tref("top-out")], [The shape of the #jt("lip") (the top edge of the wall) and the way down #src("E13", "E33").],
  )
}

== What the setter had in mind <reading-setter>

#ix("Setter intent")
A #jt("setter") (the person who designs the problems) starts from a brief.#ix("Setting!the setter's brief") Who is the problem for? What grade? What movement and how much effort #src("E49")? Some gyms also ask which skills a problem tests and what share of members should finish it #src("E52"). Knowing how setters think helps you find the intended sequence.

What setters say they do:

- *They avoid ladders.* Even easy problems get matches, crosses, #tref("heel-hook", body: [heel hooks], show-page: false) and jumps #src("E46", "E47"). Harder ones get intricate sequences, big #tref("sloper", body: [slopers], show-page: false), or big holds with small footholds #src("E46").
- *They force body positions.* Setters remove footholds or put the one useful foothold far to one side. That makes you think about balance #src("E48").

#notebox("Setter clichés you will meet")[
#ix("Setting!clichés")Setters warn each other about these habits #src("E46", "E47", "E48"). That means you will still meet them.
- *The ladder:* each foot follows a hand up a line of holds #src("E47").
- *Extra feet:* a row of footholds added as a shortcut #src("E46").
- *Reach as difficulty:* a hard grade made by spacing holds far apart. Tall setters do this without noticing #src("E47", "E48").
- *Jugs for easy, crimps for hard:* easy problems get only big holds. Hard ones get #jt("crimp", body: [crimps]) (small edges) and big spans #src("E46").
]

Climbers often find a sequence the setter didn't expect #src("E54"). On #jt("comp style", body: [comp-style problems]) (jumpy, competition-like problems), read from the top down.#ix("Comp-style setting!reading") Use chalk marks, thumbprints and shoe marks as clues #src("E5").

== Other people's beta, and reading for a tall body

#jt("beta", body: [Beta]) is the sequence of moves for a problem. Watching other climbers#ix("Watching others"), asking for advice and talking it over are normal tools#ix("Beta!from other climbers") #src("E29", "E32"). Apps such as Kaya also collect beta #src("E32"). Beta from others has limits, though.

- *Your body changes the beta.* Height and arm span strongly affect how a problem feels. Adapt moves to your body#ix("Beta!adapting to your body") #src("E29").
- *Size is more than reach.* Tall climbers may get bunched up. Climbers with small hands#ix("Hand size") may not hold wide #tref("pinch", body: [pinches], show-page: false) or #tref("sloper", body: [slopers], show-page: false) well. Short climbers#ix("Short climbers") may not reach #src("E46").
- *Look for #jt("micro beta").* These are small changes to how you grip and stand, tailored to your size and strength #src("E41").
- *Read before you watch.* Make your plan for a problem first. Then watch someone climb it and compare (judgement).

#notebox("Reading for a tall body (judgement)")[
#ix("Tall climbers!reading a problem")These points apply the sources above to a tall climber. No study tests them. For climbing tall in general, see @cons-tall.
- When you copy a shorter climber, expect to skip an intermediate handhold.
- Expect their foot positions to fold you up. Try the next foothold lower or further out, so your arms stay straight.
- If you feel scrunched, the problem was probably set for a shorter span. Stand up on a lower foot, or take a higher handhold earlier.
- Distrust "you just have to jump" from light climbers. Look first for a slow move that uses your reach.
]

== Flash or project?

#ix("Flashing")
#ix("Projecting")
To #jt("flash") a problem is to climb it on your first try. To #jt("project") it is to work on it over several attempts or sessions. The two need different tactics.

*Flashing.* Data from the 2019 World Cup#ix("World Cup!success by attempt") finals show that the first attempt on a steep problem gave the best chance of finishing. Success dropped sharply after it. On slab, success stayed steadier over the first three attempts #src("E6"). So on steep problems, put everything into the first try. On #tref("slab", body: [slab], show-page: false), a first look costs you less.

At the 2018 World Cups, successful attempts lasted about 31–39 seconds on average. Failed ones averaged about 12–21 seconds #src("E40"). Most failed attempts end early, so the start and its traps deserve careful reading (judgement). Your flash routine#ix("Flashing!routine"), built from the steps above:

+ Run steps 1–8. Spend about a minute looking.
+ Mime the crux.
+ Rest fully.
+ Climb at a steady pace. Don't stop on the wall to re-read.

*Projecting.*#ix("Projecting!method") Choose a project no more than two or three grades above what you usually climb in a session #src("E41"). Then:

+ Learn the single moves first, in isolation. Get the first contact right before you add the second #src("E5"). Then link the #jt("crux") (the hardest move), then longer sections #src("E44", "E45").
+ Split the problem at the crux, the rests and the changes of style. Work on one link or one move at a time #src("E32", "E43").
+ #jt("link-up", body: [Link]) through the crux (climb past it without stopping) and keep going. Big overlapping links show progress better than your high point from the start #src("E44").
+ Practise the easy parts too. Slapping through easy moves wastes energy you need later #src("E41", "E44").
+ Count good attempts. Treat each one as information. Decide how many good attempts you can make in a day #src("E43").
+ Keep one or two side projects so you stay fresh #src("E43").

#keypoint[On steep problems your first try is your best chance. After four to six full attempts#ix("Projecting!how many attempts") without progress, change something. Rest longer, change the sequence or stop for the day.]

The six-attempt figure comes from elite competition. In the 2019 World Cup finals, only one climber finished a problem after a sixth attempt. On steep problems the fifth attempt, after four failures, succeeded only 6% of the time #src("E6"). Those athletes rest little between tries, so treat the number as a rule of thumb (judgement).

== Rest between attempts

#ix("Rest between attempts", main: true)
Rest long enough for each attempt to be a real one. Coaching sources agree on minutes, not seconds. Resting too little changes which energy system you train #src("E42").

#{
  set par(justify: false)
  table(
    columns: (1.3fr, 1fr, auto),
    table.header(th[Situation], th[Rest], th[Source]),
    [One hard move tried on its own (a few seconds of effort)], [About 2½ minutes after a 3-second try. The rule is 20–50 times the effort time.], [#src("E42")],
    [A full attempt on a hard problem (about 30 seconds)], [10–15 minutes], [#src("E42")],
    [Any physically hard problem], [At least 5 minutes], [#src("E41")],
    [A longer problem], [10–25 minutes], [#src("E41")],
    [What competitors actually do under a time limit], [About 2 minutes (a national event, 2010 study); about 30 seconds (2018 World Cups)], [#src("E39", "E40")],
  )
}

The competition figures describe athletes with four or five minutes per problem. They are not advice.#ix("World Cup!rest between attempts") While you rest, watch others try your problem.

== When to change the beta

- When your sessions keep running into dead ends, question the sequence#ix("Beta!when to change") #src("E41").
- When you are stuck or a move feels impossible, find your own #jt("beta") (sequence) for each move before you ask others. Then test new versions #src("E29", "E44").
- After each fall, name the cause (step 9). If it is the sequence, find an easier one. If it is strength, keep the sequence and train #src("E31", "E41").
- Try something new on every attempt, even on familiar moves: a different foot or a different grip #src("E44").
- Change the sequence when you fail at the same point, in the same way, on three fresh attempts in a row. Change it too when the move only works for climbers of a very different size (judgement).

== Indoor grades

#ix("Grades!indoor", main: true)
A grade tells you how hard a problem is meant to be. Indoor grades are a useful guide but a poor measure. Gyms use the #jt("V-scale") (the US scale, from VB and V0 up) or the #jt("Font scale") (the European scale, from 3 up). The conversion table is in the appendix (Grade conversion).

*How a gym grade is made.*#ix("Grades!how gyms grade") The setter usually suggests a grade after a try or two. They may adjust it after asking other setters or climbers #src("E58"). Some gyms grade by consensus. Their setters #jt("forerun") (test-climb) each other's problems and agree a grade #src("E50"). Forerunning is where setters tweak a problem until it fits the intended grade #src("E46"). Not everyone agrees. One gym writer says gym grades rarely get feedback and that modern gyms don't grade by consensus #src("E51"). Both are probably true at different gyms.

One setter says what matters most is consistency. A gym can grade hard or easy compared with outdoor rock. Its grades should stay the same as problems come and go. Regulars then adapt to that gym #src("E46").

*Why grades differ between gyms.*#ix("Grades!indoor variation")

- *The spread is large.* An analysis of 40 US gyms#ix("Studies!grades in 40 US gyms") found grades differing by two to four V-grades between gyms. The author reckons a solid V4 climber could expect anything from V2 to V6, depending on the gym #src("E53"). It is a blog analysis by a gym-listing website's founder, not a peer-reviewed study.
- *Gym type and walls.* Large commercial chains graded about one V-grade #jt("soft", body: [softer]) (easier for the number) than gyms focused on training. Steep gyms graded harder. Gyms with lots of slab or competition-style setting graded softer #src("E53").
- *Many beginners.* Gyms offer many easy problems. They tend to soften the lower grades instead of splitting them. That softness can reach the middle grades too #src("E57").
- *Style and sequence.* Slab, overhang and dynamic problems test different skills. One awkward move can make a whole problem feel harder. A setter's energy on the day plays a part, as does beta the setter didn't expect #src("E54").
- *Your body.* Height, reach, finger size and style all change how a grade feels #src("E57", "E51", "E46").

No peer-reviewed study of indoor grade consistency turned up in our search.

*Colours and circuits.*#ix("Circuits") Some walls group problems into a #jt("circuit"): a colour that covers one grade or a range of two or three #src("E55"). One aim is to play down grades and encourage you to try everything. Colour ranges often overlap, so a problem in a harder colour isn't always harder #src("E56"). Two US gyms use five colours each, such as V0–V2, V2–V4, V4–V6, V6–V8 and V8 and up #src("E52"). Some gyms use colours with no V-grades at all, or their own scales #src("E57"). UK walls mostly use Font or V-grades for bouldering #src("E55").

*Calibrating yourself in a new gym.*#ix("Grades!in a new gym")

+ Ask the staff how their system works and how it compares with standard grades #src("E55", "E56").
+ Warm up three or four grades below your maximum. Start below your limit while you learn the gym's style #src("E53", "E56").
+ In the first week, climb as many problems as you can in 15 minutes, two grades below your usual maximum. Repeat every two weeks. Compare the counts between gyms #src("E53").
+ Pick one reference problem at your home gym for each style: steep overhang, small edges, slab, jumps and squeezing. After three or four sessions, compare the new gym's problems with them #src("E53").
+ Keep track of which problems you climb reliably and which feel harder or easier for your body #src("E51").

#keypoint[Judge a new gym by style, not by the number on the tag. A V4 there can be your V3 or your V5.]
