#import "../template.typ": *

// The steps of the method are subheads: the label in small caps, the
// title on the subhead step of the scale.
#let step(n, title) = block(above: gap(1.5), below: gap(0.35), breakable: false, sticky: true,
  text(size: fs.sub)[#section-label[Step #n]#h(0.6em)#text(weight: 700, title)])

= Reading a problem

Reading a #jt("problem") (an indoor boulder route) means working out how to climb it before you touch it. You find the start and the finish. You decide which hand goes on which hold, where your feet go and where it will get hard. Then you rehearse it in your head.

#ix("Route reading", main: true)
Good readers don't guess better. They have a method and compare what they read with moves they have already done. In a study of 77 indoor boulderers, the novices said they had looked mostly at the handholds. On the wall they missed footholds and needed more tries#ix("Studies!previewing a route") #src("E85"). Expert climbers describe reading from the whole route down to its details. They mark the hard parts, the rests and the traps #src("E35"). Studies also suggest that experts see more readily what a hold can be used for#ix("Experts and novices!route reading") #src("E38"). You read with the moves you know, so every new move you learn on the wall makes you a better reader.

This chapter gives you that method and a routine for your first try. @cons-projecting covers what comes after the first try: working on a hard problem, resting and changing your plan. @grades-indoor explains gym grades.

== The method, step by step <reading-method>

Run these steps at the bottom of every problem you want to climb first try. On a warm-up, steps 1 to 3 are enough. A companion booklet, _Reading the Wall: Exercises_, has eight drawn problems to practise on.

#step(1)[Rules and boundaries]

- Use only holds of the problem's colour or tape#ix("Gym rules") #src("E65").
- Find the start.#ix("Start holds") Most gyms mark it with extra tape, a coloured box or the grade tag. Put your hands on the start hold or holds #src("E65").
- Some rules vary between gyms. Can both hands share one start hold? Must your feet use marked holds? Do #tref("volume", body: [volumes], show-page: false) (big hollow shapes bolted to the wall) count? Volumes often count for every problem on that wall#ix("Volumes!gym rules") #src("E19"). If in doubt, ask the staff #src("E55").
- A #tref("sit-start", body: [sit start]) is usually marked on the tag. Some gyms want you settled on the start holds, with your feet off the ground, before you move on #src("E71", "E72"). Competition rules ask the same #src("E70"). Ask what your gym wants.
- Find the finish. It is either a marked top hold or a #tref("top-out", body: [top-out]) onto the top of the wall #src("E65"). Gyms ask for both hands on the top hold #src("E73", "E74"). Competitions also want you in control there #src("E70").
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
+ Check the order. If two holds in a row need the same hand, you can #tref("matching", body: [match], show-page: false) (put both hands on one hold), #tref("cross-through", body: [cross], show-page: false) (move one hand over the other) or move the same hand twice #src("E30").
+ Where you can't decide, list the options in order: cross, match or go again. Choose when you feel the holds #src("E30").
+ Pick two or three #jt("marker hold", body: [marker holds]): big, easy-to-remember holds that anchor the sequence. The rest hangs off them #src("E30").
+ Expect at least one match or cross: setters avoid straight ladders even on easy problems (@reading-setter).

#fig("reading-worked-problem.svg", caption: [A worked reading. Start with both hands on the taped hold. R1 is a sidepull facing right, so the right hand takes it. L4 lies to the right of R3, so the left hand must cross over. The cross and the slap to R5 form the crux (the hardest part). A high right foot sets up the cross. R3 is a jug where you can rest.])


#step(5)[Find the feet]

- Holds with rubber marks and no chalk are probably footholds#ix("Route reading!footholds") #src("E30", "E31").
- On steep ground, look for footholds you can use with the outside edge of the shoe. Under roofs, look for #tref("heel-hook", body: [heel hooks], show-page: false) and #tref("toe-hook", body: [toe hooks], show-page: false) #src("E30").
- Look for moves where a #tref("flag", body: [side flag]) saves you swapping feet twice in a row #src("E30", "E12").
- Read the feet together with the hands, because the next hand move depends on where your feet are #src("E35").
- Don't try to plan every foot. The coach Neil Gresham#ix("Gresham, Neil") says the exact foot sequence is very hard to guess #src("E30"). Gresham plans the hands exactly and works out the feet on the wall. The exception is a few key foot moves, such as those at the hardest move #src("E75"). So plan the feet for the start and the hardest move, and sort out the rest on the wall.#note[Gresham writes about roped routes and names only the hardest move. The start is our addition: it is the one place where you can set your feet before you pull on.]

#filmstrip("filmstrip-worked-problem.svg", [Climbing the worked problem], [Watch the right foot: it steps up onto the high foothold before the left hand crosses to L4.])

#step(6)[Find the crux, the traps and the rests]

- The #jt("crux") is the hardest move or section. It may be a jump, a balance move, a move where your feet come off, or small holds #src("E29"). Decide how you will do it before you start#ix("Crux!reading") #src("E29").
- Find the traps#ix("Route reading!traps"), where arriving with the wrong hand forces a fall. One expert in an interview study said he looks at the start in particular #src("E35").
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
A #jt("setter") (the person who designs the problems) builds a problem around a movement and a grade#ix("Setting!the setter’s brief") #src("E49"). Knowing how setters think helps you find the intended sequence, though climbers often find one the setter didn't expect #src("E54"). On #jt("comp style", body: [comp-style problems]) (jumpy, competition-like), read from the top down.#ix("Comp-style setting!reading") Use chalk marks, thumbprints and shoe marks as clues #src("E5").

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

== Other people's beta <reading-size>

#jt("beta", body: [Beta]) is the sequence of moves for a problem. Watching other climbers#ix("Watching others"), asking for advice and talking it over are normal tools#ix("Beta!from other climbers") #src("E29", "E32"). Apps such as Kaya also collect beta #src("E32"). Beta from others has limits, though.

- *Your body changes the beta.* Height and arm span strongly affect how a problem feels, so adapt moves to your body#ix("Beta!adapting to your body") #src("E29"). @cons-tall and @cons-small say how to adapt the beta of someone shorter or taller than you.
- *Size is more than reach.* Tall climbers may get bunched up, short climbers#ix("Small climbers") may not reach, and climbers with small hands#ix("Hand size") may not hold wide #tref("pinch", body: [pinches], show-page: false) or #tref("sloper", body: [slopers], show-page: false) well #src("E46").
- *Look for #jt("micro beta").* These are small changes to how you grip and stand, tailored to your size and strength #src("E41").
- *Read before you watch.* Work out your own way first, then watch or ask #src("E44"). One coach says climbers have to struggle a bit to learn #src("E83").

== Flash or project?

#ix("Flashing")
To #jt("flash") a problem is to climb it on your first try, and you get only one. Your first go may be your best of the day #src("E78"), because every attempt tires the muscles you need for the next #src("E79"). So read the problem and rest before you pull on, then give that try everything #src("E84").

Your flash routine#ix("Flashing!routine"), built from the steps above:

+ Run steps 1–8. Spend about a minute looking.
+ Mime the crux.
+ Rest fully.
+ Climb at a steady pace. Don't stop on the wall to re-read.

If the flash fails, the problem becomes a #jt("project"): one you work on over several attempts or sessions. @cons-projecting says how to work on it, how long to rest between attempts and when to change your #jt("beta"). In short, rest a minute or so after an easy problem and at least five minutes before another try at your limit #src("E41", "E42").

Don't read much into the grade on the tag either, least of all in a gym you don't know. @grades-indoor explains why.

#keypoint[Judge a new gym by style, not by the number on the tag. \ A V4 there can be your V3 or your V5.]
