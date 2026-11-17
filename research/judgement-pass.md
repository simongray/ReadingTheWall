# The "(judgement)" pass

Written on 2026-11-17, after the third edition. The third edition labelled
claims that had no source "(judgement)". This pass went through every one of
them. Each claim now cites a source, says something a source does support, or
is cut. Where the book keeps a conclusion of its own, a footnote says how it
was reached. No label is left.

The lines below come from comparing the third edition (`46e275b`) with the
working tree. A `−` line is the old wording and a `+` line the new one. Markup
is simplified: `[E30]` is a citation, and index marks and links are left out.
File and line numbers are the third edition's. An arrow gives the new place
when the text moved.

## Counts

84 passages in the book carried a label (a few carried two), and the exercises
booklet carried 19 more.

| What happened | Passages |
|---|---|
| Now cites a source, or says what a source says | 62 |
| Reworded so that it claims no more than the text can carry | 17 |
| Kept as the book's own conclusion, with a footnote | 2 |
| Cut | 3 |

The labels "(this book's suggestion)" and "(this book's reading)" went the same
day: 33 were dropped, the rest were reworded, and five more footnotes say how
the book reached a conclusion. So an old line below may show such a label and
its new line none.

"Reworded" covers three cases. A grade note now says when you need the
technique and leaves the grade to the badge. A badge follows another entry's
("it finishes a high step, so it shares that entry's badge"). Or a sentence
that follows from the one before it lost its label.

The pass added 52 sources to `research/*-sources.yml`: 22 studies and reviews,
most of them read as abstracts, and 30 pages from federations, gyms, setters,
coaches and magazines. Each entry has the date it was read, and its note says
how much of it was read.

## Things the sources turned up

- **The French federation's syllabus** (F60, F61) ties skills to levels and
  three levels to boulder grades. It is the closest thing to a graded
  syllabus, and 8 grade notes now cite it. It lists what climbers learn at a
  level, which is usually earlier than the badge.
- **Badges that may be a grade late.** Courses teach standing on volumes at
  about V0–V1 (badge V2), bicycles at V2–V4 (badge V5), toe hooks with heel
  hooks at V2–V4 (badge V4) and competition-style moves from V2–V4 (badges V4
  and V5). No badge changed in this pass.
- **Claims that turned out wrong.** F36's clinic is for climbers who can't
  reach V2, not for climbers stuck at it. No source says hard gym problems
  copy training boards. The four-to-six attempt rule had no source but the
  World Cup study, so the key point no longer gives a number.

## The exercises booklet

All 19 labels are gone from `x-problems.typ`. The problems are invented, so
every claim about them is the book's own reasoning. The opening now says so
once: "The beta is the book's own reasoning from the drawings, and it is
untested on a wall."

## Front matter

**00-front.typ:175** → a-made.typ:13 · reworded

> − *Claims without a source.* Each grade badge is a judgement. Some other unsourced claims carry a label such as "(judgement)". Every technique entry lists its sources at the foot, but about one in five of its numbered steps and common mistakes has no citation of its own and no label. In the "When to use it" boxes, about three lines in five have neither.
>
> + *Claims without a source.* Advice that cites no source is the book's own. Where it isn't plain how the book reached a conclusion, a note at the foot of the page says how. Each entry lists its sources at the foot, but about one in five of its steps and three in five of its "When to use it" lines have no citation of their own.

## Chapter 2: Reading a problem

**02-reading.typ:33** · sourced

> − Find out whether you must be still on the start holds before you move (judgement).
>
> + Some gyms want you settled on the start holds, with your feet off the ground, before you move on [E71, E72]. Competition rules ask the same [E70]. Ask what your gym wants.

**02-reading.typ:34** · sourced

> − Most gyms expect both hands on the top hold, under control (judgement).
>
> + Gyms ask for both hands on the top hold [E73, E74]. Competitions also want you in control there [E70].

**02-reading.typ:52** · sourced

> − If two holds in a row need the same hand, you can match (put both hands on one hold), cross (move one hand over the other) or move the same hand twice (judgement).
>
> + If two holds in a row need the same hand, you can match (put both hands on one hold), cross (move one hand over the other) or move the same hand twice [E30].

**02-reading.typ:66** · footnote

> − The coach Neil Gresham says the full foot sequence is the hardest part to predict [E30]. At V3–V4, plan the feet for the start and the hardest move. Sort out the rest on the wall (judgement).
>
> + The coach Neil Gresham says the exact foot sequence is very hard to guess [E30]. Gresham plans the hands exactly and works out the feet on the wall. The exception is a few key foot moves, such as those at the hardest move [E75]. So plan the feet for the start and the hardest move, and sort out the rest on the wall.[footnote: Gresham writes about roped routes and names only the hardest move. The start is our addition: it is the one place where you can set your feet before you pull on.

**02-reading.typ:73** · sourced

> − Find the traps, where the wrong hand forces a fall. Expect some near the start (judgement).
>
> + Find the traps, where arriving with the wrong hand forces a fall. One expert in an interview study said he looks at the start in particular [E35].

**02-reading.typ:173** · sourced

> − *Read before you watch.* Make your plan first, then watch someone climb the problem and compare (judgement).
>
> + *Read before you watch.* Work out your own way first, then watch or ask [E44]. One coach says climbers have to struggle a bit to learn [E83].

**02-reading.typ:175** → 09-considerations.typ:44 · sourced

> − #notebox("Reading for your size (judgement)")[
>
> + *Adapt a shorter climber's beta (their sequence of moves).* Expect to skip an intermediate handhold: you don't have to use every hold you can reach [E76]. Where their footholds fold you up, drop a foot lower and sink onto one leg, with your arms straight [E76]. Some setters bunch tall climbers up on purpose [H10], so feeling scrunched doesn't mean you read the problem wrong.

The box moved to Part IV. Its sourced half joined "How to climb small" as it was. Of the unsourced half, the points a source supports stay in "How to climb tall"; the rest is cut.

**02-reading.typ:195** · cut

> − *Flashing.* In a study of the 2019 World Cup finals, the first attempt on a steep problem succeeded about 21% of the time. The rate fell with each try, to 6% on the fifth, and the authors call the first attempt a finalist's best chance there. On slab and slab-like problems the rate rose, from about 15% on the first to 22% on the second and third. The authors ran no statistical test on these rates and warn that skill probably skews them, because better climbers finish earlier. Finalists also rest very little, about 30 seconds between tries [E6]. The climbers still trying after a failed attempt tend to be those the problem suits least, so these rates can't show that your own chance falls after one try (judgement).
>
> + (cut)

Cut with the World Cup statistics it commented on.

**02-reading.typ:197** · sourced

> − You only get one flash and your arms are at their freshest, so on steep problems put everything into the first try (judgement). On slab, a failed first try costs you less (judgement).
>
> + To flash a problem is to climb it on your first try, and you get only one. Your first go may be your best of the day [E78], because every attempt tires the muscles you need for the next [E79]. So read the problem and rest before you pull on, then give that try everything [E84].

**02-reading.typ:215** → 09-considerations.typ:307 · reworded

> − After four to six full attempts without progress, change something (judgement).
>
> + When your full attempts stop getting further, change something.

**02-reading.typ:217** → 09-considerations.typ:309 · sourced

> − The six-attempt figure comes from elite competition. In the 2019 World Cup finals, only one climber finished a problem after a sixth attempt. On steep problems the fifth attempt, after four failures, succeeded only 6% of the time. The authors treat six as a cut-off and say they can't name an ideal number [E6]. The climbers still trying by then tend to be those the problem suits least, and they rest little between tries, so treat four to six as a rule of thumb (judgement).
>
> + Coaches who give a number keep it low: three tries per problem in one drill [E77], or three or four honest efforts at a move that rarely works [E81]. One coaching site says to end a limit session as soon as your output drops [E80]. Stopping protects what you learn too. In a laboratory study, people who practised a pinching task while tired learned it worse, and the loss lasted into the following days [E82]. It wasn't a climbing study.

The World Cup paragraph is cut. The key point now rests on coaches and one laboratory study.

**02-reading.typ:246** → 09-considerations.typ:317 · sourced

> − Change the sequence sooner than the four-to-six rule when you fail at the same point, in the same way, on three fresh attempts in a row. Change it too when the move only works for climbers of a very different size (judgement).
>
> + Change the sequence sooner when you keep failing at the same point in the same way: switching beta can get you out of a rut [E44]. Change it too when the move only suits a climber of a very different size [E41].

## Chapter 3: Feet and legs

**Precise footwork: 03-feet.typ:78** · sourced

> − Learn it from your first session (this book's suggestion). It becomes decisive at about V2–V3, where the footholds get small (judgement). Forum climbers put the break at V3 [A44].
>
> + Learn it from your first session. The UK's bouldering-instructor award lists accurate use of the feet among the basics to teach novices [F62]. Forum climbers say footwork starts to decide problems at about V3 [A44]. A London gym drills footwork on small footholds in a course for V2–V4 climbers [F71].

**Edging: 03-feet.typ:126** · reworded

> − The outside edge comes in around V1, when your hip starts to turn in. It decides moves on steep V2–V3s, where square-on hips stop working (judgement).
>
> + You use the outside edge when you turn a hip to the wall, so it starts to matter with hip turn.

**Front-pointing: 03-feet.typ:172** · reworded

> − Needed on your first V1s with pockets or small holds that face straight out (judgement).
>
> + You need it wherever a foothold is a pocket or a small hold that faces straight out.

**Smearing: 03-feet.typ:206** · sourced

> − Gym slabs and volumes ask for it from V1. From V3 it often decides slab and volume problems (judgement).
>
> + You need it wherever a slab or a volume gives you no foothold. Gyms set slabs and tricky footwork on easy problems on purpose [E46, E52]: one US gym uses its slab walls to teach climbers to smear and trust their feet [E52].

**High step: 03-feet.typ:249** · reworded

> − Common on V1–V2s with big holds far apart (judgement). From V3 the better answer is often *not* to high-step: Gresham calls a big high step a beginner fault where smaller steps would do [A7].
>
> + You need it when the only foothold is at hip height or above. Often the better answer is *not* to high-step: Gresham calls a big high step a beginner fault where smaller steps would do [A7].

**Rockover: 03-feet.typ:288** · reworded

> − It finishes a high step, so you meet it at V1 on big, high footholds (judgement).
>
> + It finishes a high step, so it shares that entry's badge.

**Pivoting: 03-feet.typ:322** · reworded

> − Matters from V2–V3, when your hips start to turn on steep walls (judgement).
>
> + You pivot whenever you turn a hip to the wall, so the badge is the same as for hip turn.

**Hand–foot match: 03-feet.typ:401** · sourced

> − It is the heart of a mantle, so you need it from V2 (judgement).
>
> + It is the heart of a mantle, so it shares that entry's badge. France's climbing federation teaches it at about V2 [F60, F61].

**Toe hook: 03-feet.typ:533** · sourced

> − It starts deciding problems around V4 (judgement).
>
> + A London gym teaches both in a course for V2–V4 climbers [F70]. Gym clinics aimed at V5–V6 climbers still teach it [A42, A43].

**Toe hook: 03-feet.typ:565** · sourced

> − The cost is a longer lever, so you need more tension to stop the swing when you let go (judgement).
>
> + Brace your core before you let go of a hook [A15]. Tall climbers on one training site say a long body needs more core strength to hold its span on steep walls [E76].

**Bicycle: 03-feet.typ:580** · sourced

> − In gyms it turns up on steep V4–V6s with big holds or volumes (judgement). The Sportrock gym calls it advanced [A25].
>
> + You need it only where a steep wall has one big hold or volume that both feet can clamp. The Sportrock gym calls it advanced [A25], though a London gym teaches it in a course for V2–V4 climbers [F71].

**Heel–toe cam: 03-feet.typ:611** · reworded

> − When it appears, it is usually on V5 or harder (judgement).
>
> + No source we found ties it to a grade.

**Knee bar: 03-feet.typ:643** · cut

> − Indoors it shows up on steep V5+ problems with big volumes (judgement).
>
> + (cut)

## Chapter 4: Body positioning

**Straight arms: 04-body.typ:97** · sourced

> − Learn it from your first session (this book's suggestion): when you pause on a steep wall, hang on nearly straight arms with your shoulders set, and on a vertical wall stand tall instead. It matters more on your first overhangs, and on V3–V4 overhangs it can decide whether you run out of strength (judgement). The UK's coach training lists it as a way to find a rest [B1].
>
> + Learn it from your first session: when you pause on a steep wall, hang on nearly straight arms with your shoulders set, and on a vertical wall stand tall instead. It matters more the steeper the wall, because your arms then carry more of your weight (Chapter 1). The UK's coach training lists it as a way to find a rest [B1]. The UK's bouldering-instructor award counts it among the basics for novices [F62].

**Stemming: 04-body.typ:250** · sourced

> − Corners and pairs of volumes appear on easy problems, where they mostly help you rest and save effort (judgement).
>
> + You can stem wherever two surfaces face each other, such as a corner or a pair of volumes. One setter advises putting easy problems in corners so that new climbers learn to stem [F72].

**Stemming: 04-body.typ:269** · sourced

> − Big steps collapse the position (judgement).
>
> + A series of small moves is often better than one long one, because being stretched out upsets your balance [C36].

**Side flag: 04-body.typ:351** · sourced

> − From about V2, reaches start to swing you open where your free foot has no hold (judgement). The UK's coach training lists flagging as a steep-wall skill [B1]. A US gym still teaches it to climbers stuck at V5 [B63].
>
> + You need it when a reach would swing you open and your free foot has no hold. The UK's coach training lists flagging as a steep-wall skill [B1]. A London gym drills flags in a course for V2–V4 climbers [F71]. A US gym still teaches them to climbers stuck at V5 [B63].

**Backstep: 04-body.typ:503** · sourced

> − So when the holds suit a backstep, try it before you decide a move is too far (judgement). A drop knee does a similar job if your knees are mobile enough [H4], but read the knee box in @cons-tall first.
>
> + So when the holds suit a backstep, try it before you decide a move is too far. For a short climber, one training site puts the moves that bring you close to the wall first [H2]. A drop knee does a similar job if your knees are mobile enough [H4], but read the knee box in @cons-injuries first.

**Drop knee: 04-body.typ:566** · sourced

> − It gives most of the lock with less load on the knee (judgement).
>
> + A study of knee injuries describes the injured position as a fully bent knee [G9]. One professional setter tells climbers to be very cautious about how far they drop the knee [B80].

**Lock-off: 04-body.typ:716** · sourced

> − Add a few at a time, because they load your elbow and shoulder (judgement).
>
> + Add a few at a time: in a laboratory study of fingerboard hangs, the load on the elbows and shoulders rose the more the elbows were bent [G71].

## Chapter 5: Hands and holds

**Half crimp: 05-hands.typ:137** · sourced

> − Edges small enough to crimp turn up from about V2 (judgement). They keep shrinking as you near V5 [C48]. Make the half crimp your default on these edges from the start, so you don't fall into the habit of full crimping (this book's suggestion).
>
> + A London gym teaches crimps, with a first look at finger strength, in a course for V2–V4 climbers [F70]. Holds keep getting smaller as you near V5 [C48]. Make the half crimp your default on small edges from the start, so you don't fall into the habit of full crimping.

**Half crimp: 05-hands.typ:156** · sourced

> − If it still opens, leave the move for now, because a full crimp is for the tiny edges of about V5 (judgement).
>
> + If it still opens, leave the move for now. A full crimp is for very small edges [C1, C10]. Holds get smaller and crimpier at about V5 [C48].

**Undercling: 05-hands.typ:237** · sourced

> − Stop raising your feet once it does, because higher still folds your long legs against your chest (judgement).
>
> + Higher feet still help, but you get bunched sooner: in a tight position a tall climber's knees end up in the chest [H15]. If your knees jam, turn one hip to the wall as in step 6.

**Mantle: 05-hands.typ:284** · sourced

> − Gyms with top-out walls can ask for an easy one from V0, and it starts to matter at V2 (judgement). The heel hook in step 2 comes at V3, so try it low on the wall first (this book's suggestion).
>
> + Where a gym has walls you top out on, you need an easy one from the start. The UK's bouldering-instructor award lists safe topping out among the basics for novices [F62]. The heel hook in step 2 has a V3 badge, so try it low on the wall first.

**Pinch: 05-hands.typ:422** · sourced

> − Big hands help on wide pinches [C37], less so on narrow ones (judgement).
>
> + One setter says large hands hold wide pinches more securely than small ones [E46]. One blogger finds that thin pinches feel better with small hands [H15].

**Pinch: 05-hands.typ:423** · footnote

> − If your thumb can't press back on a wide pinch, you may be able to hold it like an edge [C37], or pull it as a sidepull, leaning away from it (judgement).
>
> + If your thumb can't press back on a wide pinch, look for a narrower part of the hold to pinch [C60]. Failing that, you may be able to hold it like an edge [C37]. It then works in one direction only, so lean away from it as on a sidepull.[footnote: Our inference from the rule in Chapter 1: a hold used as an edge works only when you pull away from the way it faces.]

## Chapter 6: Dynamic movement

**06-dynamic.typ:23** · sourced

> − Small deadpoints are fine (judgement), and one gym owner's article says dynamic moves are generally more efficient than lock-offs [D13]. Apart from a few practice goes low on big holds, keep big jumps for the moves that need them (judgement; see Chapter 9), and don't snatch at small holds, because grabbing a hold very quickly in a dynamic move can rupture a pulley (a band that holds a finger tendon against the bone) [C25].
>
> + A physiotherapist who treats climbers says that dynamic climbing, done well, can be more efficient than static climbing without adding injury risk. The deadpoint is that article's example [D60]. One gym owner's article agrees that dynamic moves are generally more efficient than lock-offs [D13]. Build up to big jumps. The same physiotherapist says to start with small dynamic moves and move on to bigger ones over time [D60]. Another warns that too much dynamic climbing can shock-load the body [G66]. Don't snatch at small holds, because grabbing a hold very quickly in a dynamic move can rupture a pulley (a band that holds a finger tendon against the bone) [C25].

**Deadpoint: 06-dynamic.typ:77** · sourced

> − Try small ones from V2 on big holds (this book's suggestion). Gyms teach it in intermediate classes, after about two months of climbing [D39]. Many V3s need it, and from V4–V5 most moves between small holds on steep walls do (judgement).
>
> + Try small ones from V2 on big holds. France's climbing federation teaches controlled dynamic moves at about that grade [F60, F61]. A German gym chain teaches dynamic moves to climbers stepping up to Font 6A, which is V3 [F68, F69]. Other gyms teach the deadpoint in intermediate classes, after about two months of climbing [D39]. One still teaches it to climbers stuck at V5 [F35].

**Deadpoint: 06-dynamic.typ:93** · sourced

> − The hip turned to the wall rotates in and up, which throws the hand on that side much farther than square hips can. On steep gym walls, many V4 moves are thrown this way (judgement).
>
> + The hip turned to the wall rotates in and up, which throws the hand on that side much farther than square hips can [B41].

**Deadpoint: 06-dynamic.typ:94** · sourced

> − Don't snap off a deep drop knee, because the knee can take a sudden load as your hand lets go (judgement; see the knee box in @cons-tall).
>
> + Don't throw from a deep drop knee. The authors of a knee-injury study suspect that the injury comes at the moment a hand lets go, which adds load to the legs [G9]. The coach Dave MacLeod warns against dropping the knee and moving the hand in one rapid motion [D61]. See the knee box in @cons-injuries.

**Deadpoint: 06-dynamic.typ:124** · sourced

> − Deadpoint them anyway on easy problems: it may save energy [D13], and on harder problems the lock-off often stops working (judgement). On short walls and in cramped sequences, a hip pop's drop knee jams long legs, so take a higher foothold and a shorter throw (judgement).
>
> + Deadpoint them anyway on easy problems: it may save energy [D13], and the steeper the wall, the more work a lock-off costs your arm [D62]. In cramped sequences tall climbers get bunched up [E46], and a hip pop's drop knee may not fit. Tall climbers quoted by one training site take a foot off and sink onto one leg instead [E76].

**Deadpoint: 06-dynamic.typ:125** · sourced

> − Keep big jumps for the moves that need them, and don't snatch at small holds (judgement; see @cons-heavy).
>
> + Build up to big jumps from small moves [D60], and don't snatch at small holds [C25].

**Hip pump: 06-dynamic.typ:137** · sourced

> − That starts at about V2–V3 (judgement). Timing a single pump before a dyno matters from V4–V5.
>
> + A German gym chain teaches starting a move from the hips to climbers stepping up to Font 6A, which is V3 [F68, F69]. Timing a single pump matters once you dyno, which has a V4 badge.

**Jump start: 06-dynamic.typ:173** · reworded

> − Shorter climbers meet it from V2–V3: "where tall people can reach, short people often have to jump" [D45]. Four-point starts can force one at V4–V5 [D35]. The placement is judgement.
>
> + A four-point start can force one whatever your height [D35]. Shorter climbers meet it more often (see the note for small climbers).

**One-handed dyno: 06-dynamic.typ:209** · sourced

> − Learn it from V3 on good holds, low on the wall (this book's suggestion). Gyms force this dyno most often, as one big move to a single good hold. Expect it from V4 (judgement).
>
> + Learn it from V3 on good holds, low on the wall. Gyms force this dyno most often, as one big move to a single good hold. One head setter brings "a variety of dynamic movements" into a gym's V4–V6 circuit [E52]. France's climbing federation teaches thrown moves from about V2 [F60, F61], while a US clinic for V5–V6 climbers still lists dynos [D36].

**One-handed dyno: 06-dynamic.typ:234** · sourced

> − The throw probably costs less energy (judgement) [D13].
>
> + A physiotherapist points out that a static move needs intense muscle work from start to finish [D60]. One gym owner finds dynamic moves generally more efficient [D13].

**Cutting loose and swing control: 06-dynamic.typ:327** · reworded

> − The counter-kick arrives with one-handed throws and sidepull catches at V4–V5 (judgement).
>
> + The counter-kick goes with one-handed throws (lunge) and sidepull catches.

**Run-and-jump: 06-dynamic.typ:382** · sourced

> − Learn it from V3 on big holds (this book's suggestion). It is a competition move that gyms now set for ordinary climbers, often at lower grades [D32], so expect it on competition-style problems from about V4 (judgement).
>
> + Learn it from V3 on big holds: France's climbing federation teaches it at that grade [F60, F61]. It is a competition move that gyms now set for ordinary climbers, often at lower grades [D32].

**Campus move: 06-dynamic.typ:456** · reworded

> − Low-grade gym problems rarely force moves without feet. Steep V5+ problems sometimes leave no usable feet for a move or two (judgement; no coaching source places it).
>
> + You need it only where a steep problem leaves no usable foothold for a move or two. No coaching source we found ties it to a grade.

**Jumping to a foothold: 06-dynamic.typ:489** · reworded

> − It is common on competition-style problems from about V5 (judgement), often as the first move [D25, D35].
>
> + On competition-style problems it is often the first move [D25, D35].

**Competition set pieces: 06-dynamic.typ:560** · sourced

> − These moves depend more on a gym's setting style than on its grades (judgement). Where a gym sets them, expect them on competition-style problems from about V5. Competitions use the paddle dyno to separate the best athletes [D7], but in gyms it is a set piece rather than a common need (judgement).
>
> + Whether you meet these moves depends on how your gym sets: one setter writes that the same leap between two volumes can be set at V1 or at V6 [F73]. One head setter keeps risky coordination moves for a gym's V6–V10 circuits [E52], while others say gyms now put competition moves on ordinary problems, often at lower grades [D32]. Competitions use the paddle dyno to separate the best athletes [D7].

## Chapter 7: Terrain

**Volumes: 07-terrain.typ:89** · sourced

> − Standing on a volume matters from about V2. Some gyms set problems on volumes alone [E19]. Those problems are harder to read and appear from about V4, which is where the squeezes and hooks in steps 7 and 8 start to pay. A knee bar comes later, around V5 (judgement).
>
> + Standing on a volume comes early. France's climbing federation teaches balance moves on volumes at the third of its eight levels [F60]. A German gym chain teaches standing on volumes for the step up to Font 4C–5A, about V0–V1 [F68, F69]. One setter recommends volumes on easier problems [F72]. Some gyms set problems on volumes alone [E19]. The squeezes, hooks and knee bars in steps 7 and 8 have later badges of their own.

**Volumes: 07-terrain.typ:120** · sourced

> − Long arms and legs make squeezing and far-side standing easier, but they fold up between close volumes. Look for a wider span or a lower foot (judgement).
>
> + Tall climbers get bunched up where holds sit close together [E46], and volumes are no exception. Try dropping a foot lower and sinking onto one leg [E76].

**Volumes: 07-terrain.typ:121** · reworded

> − So before you decide a step is too high, look along the face for a spot you can reach, on the far side if you can (judgement).
>
> + So before you decide a step is too high, look along the face for a spot you can reach, on the far side if you can.

**Traverses: 07-terrain.typ:132** · sourced

> − Traverses appear at every grade. Moving efficiently along them pays off from about V2, once you have learned to cross through and flag. The back flag in the figure comes at V3, so until then use a side flag where you can (judgement).
>
> + Traverses appear at every grade: France's climbing federation has climbers traverse at its first level [F60]. Moving efficiently along one takes a cross-through and a side flag, which both have a V2 badge. The back flag in the figure has a V3 badge, so until then use a side flag where you can.

**Top-outs: 07-terrain.typ:169** · sourced

> − Topping out matters wherever your gym has boulders you can stand on top of. Finishes like this are common from V2–V4 (judgement). The heel hook for a rounded lip comes at V3, so try it low on the wall first (this book's suggestion).
>
> + Topping out matters wherever your gym has boulders you can stand on top of, from your first session there. The UK's bouldering-instructor award lists safe topping out among the basics for novices [F62]. The heel hook for a rounded lip has a V3 badge, so try it low on the wall first.

**Arêtes: 07-terrain.typ:251** · sourced

> − Arêtes appear on easy problems. Controlling the swing they cause matters from about V3 (judgement).
>
> + Arêtes appear on easy problems: one setter advises setting them there so that new climbers learn heel hooks and stemming [F72]. Controlling the swing they cause takes a layback (badge V2) and often a heel hook (badge V3).

**Sit starts: 07-terrain.typ:288** · cut

> − Sit starts become common around V3–V5 (judgement).
>
> + (cut)

**Sit starts: 07-terrain.typ:298** · sourced

> − Some gyms want you still on the start holds before you move (judgement).
>
> + Some gyms want you settled on the start holds, off the ground, before you move to the next hold [E71, E72], as competition rules do [E70].

**Sit starts: 07-terrain.typ:312** · sourced

> − With long legs, your bottom may still be on the mat where a shorter climber would already hang (judgement).
>
> + Sit starts feel cramped and strenuous if you are tall or stiff [E11].

**Roofs: 07-terrain.typ:325** · sourced

> − Once the footholds face down or sideways, around V4–V5, your feet must hook to stay on (judgement).
>
> + Once the footholds face down or sideways, your feet must hook to stay on. France's climbing federation teaches positions with the body horizontal at about V4 [F60, F61].

**Roofs: 07-terrain.typ:336** · sourced

> − If a hand slips you can tip upside down, so try it low first and ask for a spot (judgement).
>
> + A fall with your feet above your head can turn you upside down [G61], so practise this low down first [A12] and decide beforehand whether you want a spotter [G61].

## Chapter 8: Grade by grade

**08-grades.typ:157** · sourced

> − V2 is a known plateau: one gym runs a movement clinic for climbers stuck there [F36]. The way out is probably learning to climb side-on (judgement).
>
> + Many climbers stall here: one gym runs a clinic for those who struggle to reach V2 [F36]. In one small study, a few beginners improved suddenly once they found side-on positions [G45].

**08-grades.typ:198** · sourced

> − That figure mixes men and women over four grades, so many V3 climbers climb well on less (judgement).
>
> + That figure mixes men and women. The women in the band average about 7 kg [F1], so many V3 climbers climb well on far less than 19 kg.

**08-grades.typ:259** → 09-considerations.typ:326 · sourced

> − Assume technique, not strength, stops you until a symptom says otherwise (judgement, from the coaches' advice in "Technique or strength?").
>
> + Lattice's coaches say they are likely to advise climbers with under five years of experience to focus on technique or on applying the strength they have [F14]. Another coaching company finds that most problems up to V7 or V8 need only moderate finger and pulling strength and depend more on movement, position and tactics [F64]. In a gym competition with problems from V0 to V8, the strength of 67 boulderers' ring fingers, their experience and how often they bouldered together explained over a third of the differences in their scores [H13]. The study didn't measure technique. So assume technique, not strength, stops you until a symptom in the table below says otherwise.

**08-grades.typ:277** · sourced

> − [*Wall angle*], [30–45°, or vertical with poor feet], [More problems on the steepest walls, 40–50° (judgement)
>
> + [*Wall angle*], [30–45°, or vertical with poor feet], [Often steeper: forum climbers find the harder problems more overhung [F46]

**08-grades.typ:279** · sourced

> − [*The crux*], [Several solutions work], [Usually one technique done precisely, such as a toe hook to stop a swing (judgement)
>
> + [*The crux*], [Several solutions work], [More often a test of one skill, such as a toe hook to stop a swing. One head setter says a gym's problems switch from teaching skills to testing them in its V4–V6 circuit [E52]

**08-grades.typ:280** · sourced

> − [*Dynamic moves*], [Deadpoints, lunges, the odd dyno or coordination move (judgement)], [Committed deadpoints, dynos and coordination moves such as run-and-jump [F34]
>
> + [*Dynamic moves*], [Deadpoints, lunges, the odd dyno or coordination move [F60, E52]], [Committed deadpoints, dynos and coordination moves such as run-and-jump [F34]

**08-grades.typ:281** · sourced

> − [*Body tension*], [Needed on steep moves (judgement)], [Needed to keep the feet on through hand moves [F35, F48]
>
> + [*Body tension*], [Needed on steep moves [F60]], [Held for longer, through slow moves [F65], to keep the feet on while a hand moves [F35, F48]

**08-grades.typ:282** · sourced

> − [*Techniques per problem*], [Two or three], [Three to five, linked without rests (judgement)
>
> + [*Complexity*], [More than at V2–V3: the same setter starts "surprising" climbers with complexity and risk in the V2–V4 circuit [E52]], [More again, and sustained: the V4–V6 circuit adds sustained intensity [E52]

**08-grades.typ:283** · reworded

> − [*How it goes*], [First go, or in one session], [Often several sessions; you work out the beta move by move (judgement)
>
> + [*How it goes*], [First go, or in one session], [Several sessions, since it is your next grade. You work out the beta move by move

**08-grades.typ:301** → 09-considerations.typ:328 · sourced

> − These figures can't say where the extra strength for V5 comes from. Trying V5s is this book's first suggestion (judgement), but Lattice's author says of the men's figures that technique alone can't carry you up the whole grade scale [F1].
>
> + Strength still counts: Lattice's author says of its figures for men that technique alone can't carry you up the whole grade scale [F1]. To build it, start by trying problems at the next grade. Climbing alone makes beginners' grip stronger [F67], though finger training on top adds more [F66].

**08-grades.typ:418** · sourced

> − Finger strength becomes a more common limiter (judgement). Forum climbers recommend finger training to break into V6 [F46].
>
> + One head setter says a gym's problems start to test finger strength from V6 [E52]. Forum climbers recommend finger training to break into V6 [F46]. One coaching company puts the change later: up to V7 or V8, it says, most problems need only moderate finger strength [F64].

**08-grades.typ:435** · sourced

> − Expect a hard problem to take weeks, not sessions (judgement).
>
> + Expect your hardest problems to take many sessions: one coach writes of climbers spending season after season on theirs [E81].

**08-grades.typ:474** · sourced

> − Expect each new grade to take seasons, not weeks (judgement).
>
> + Expect each new grade to take longer than the last: in Lattice's data each grade band goes with more years of climbing [F2].

**08-grades.typ:480** · sourced

> − Many problems copy the style of training boards. Sequences are long and powerful (judgement).
>
> + One head setter says a gym's hardest circuits test finger strength, complex sequences and risky coordination moves [E52]. One coach says harder mostly means bigger moves: to fairly good holds on training boards, and to more sloping holds on gym problems [F65].

## Chapter 9: Your body and how you learn

**09-considerations.typ:68** · reworded

> − The two may not clash (judgement): the forums mean reach on the wall and Lattice means how strong your fingers test, though its coaches think reach explains part of that gap [H7]. Both are weak evidence, so don't plan your training around either (this book's suggestion).
>
> + The two measure different things: the forums mean reach on the wall and Lattice means how strong your fingers test, though its coaches think reach explains part of that gap [H7]. Both are weak evidence, so don't plan your training around either.

**09-considerations.typ:72** · reworded

> − If you are also light, each finger carries less load (judgement), but don't chase a lower weight (@cons-heavy).
>
> + If you are also light, each finger carries less load. That is plain mechanics, but don't chase a lower weight (@cons-heavy).

**09-considerations.typ:152** · sourced

> − This may be the injury you can most easily prevent (judgement).
>
> + In laboratory tests, squatting and rolling cut the force of a landing [G80]. No study yet shows that practising falls lowers bouldering injuries: one followed 507 indoor boulderers for a year and found no measure that protected them [G81].

## Troubleshooting table

**a-troubleshooting.typ:145** · reworded

> − After four to six failed tries, change the sequence or stop (judgement). See Chapter 2 [E41, E42].
>
> + When your attempts stop getting further, change the sequence or stop. See @cons-projecting [E41, E42].

**a-troubleshooting.typ:165** · sourced

> − [Use lower or wider footholds. Skip intermediate holds. Keep your arms straight (judgement).
>
> + [Drop a foot lower and sink onto one leg. Skip intermediate holds. Keep your arms straight [E76].

