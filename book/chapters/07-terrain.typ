#import "../template.typ": *

= Terrain

The angle and shape of the wall decide which techniques a #jt("problem") needs. On a slab you stand and balance. On an overhang you hang and pull with your feet. On an arête you fight a swing. For each kind of terrain, this chapter says what changes in your body position and what to look for before you start.

The entries here don't repeat how to do a heel hook or a drop knee. They say where the terrain asks for one and why, and link to the full entry.

#category-table("terrain")

== How the wall angle changes your body

The steeper the wall, the more of your weight your arms carry (Chapter 1 explains why). A #tref("volume", body: [volume], show-page: false) (a big hollow shape bolted to the wall) can turn a vertical wall into a slab for one move.#ix("Volumes!as a slab") A study of World Cup problems counted a wall as "slab-like" when climbers mostly pushed on holds rather than pulled #src("E6"). Use the same test: if a problem mostly asks you to push, climb it like a slab.

#ix("Wall angle", main: true)
#{
  set par(justify: false)
  table(
    columns: (auto, 1fr, 1fr, 1fr),
    table.header(th[Wall], th[Your weight and hips], th[Your hands], th[What goes wrong]),
    [Slab], [Almost all your weight is on your feet. Your hips are over your toes, slightly away from the wall.], [Press, palm and steer.], [Feet skate off. Pulling on the hands levers the feet off #src("E1", "E3", "E4").],
    [Vertical], [Most of your weight stays on your feet if your hips stay close to the wall.], [Stand tall. A slightly bent arm is fine.], [Your hips drift out, so you over-grip #src("E10").],
    [Overhang], [Your arms carry more as the angle grows. Turn your hips sideways into the wall.], [Keep your arms straight. Let your feet pull as well as push.], [You stay square and bend your arms. Your feet come off #src("E8", "E9", "E11").],
    [Roof], [Your body is nearly horizontal. Your feet must hook to stay on.], [Keep your arms straight. Foot hooks act as a third arm.], [Your feet swing off #src("E7", "E15").],
    [Arête], [Your weight is split between the edge and the face beside it.], [Pull the edge and push with your feet.], [Your body swings open like a door #src("E2").],
    [Corner], [You press out into both walls.], [Press or rest.], [You put both feet on one wall, so your arms do the work #src("E20", "E24").],
  )
}

#fig("terrain-wall-angles.svg", caption: [The same climber on four wall angles. The dashed line drops from the #jt("centre of gravity") (the body's balance point). On the slab it falls on the foot. On the vertical wall it falls close to it. On the overhang and the roof it falls well behind the feet, so the arms take more weight.])

== Vertical walls

A vertical wall needs no technique of its own, but it breaks one slab habit.#ix("Vertical walls", main: true) On a slab you can balance over one foot without your hands. On a vertical wall gravity pulls your hips out from the wall, so you can't #src("E10").

- Before each move, bring your hips *in* towards the wall as well as *over* the heel of the standing foot. Climbers who move their hips only left and right leave them slightly out. That puts weight on the arms and makes them over-grip #src("E10").
- Stand on the inside edge of the shoe with your hips more or less square. Switch to the outside edge with crossed legs when the holds line up. When they don't, #tref("flag", body: [flag]) instead of swapping feet #src("E12"). See #tref("edging").
- On a volume, stand on the far side, away from the wall. See #tref("volume").

#technique(
  key: "corner",
  name: "Corners",
  aliases: ("dihedral", "open book", "inside corner"),
  category: "terrain",
  grade: 1,
  grade-note: [Corners turn up from the easiest grades. They mostly help you rest and save effort (judgement).],
  summary: [A corner gives you two walls that face each other. Press a foot, and often a palm, into each wall. The two pushes hold you in place, so your legs carry the weight and your arms can rest. The pushing technique itself is #tref("stemming").],
  figure: "corner.svg",
  caption: [(a) Feet and palms press out into both walls. The centre of gravity sits between the feet. (b) The same position from above.],
  how: [
    + Face into the corner, or turn a little towards the wall with the better holds.
    + Put one foot on each wall, knees bent. Press outward and down, evenly on both walls #src("E24", "E20").
    + Where there are no handholds, press a flat palm on each wall at chest height. See #tref("palming") #src("E20").
    + To move up, shift your hips over one foot. Step the other foot up a short way; big steps collapse the position. Repeat on the other side (judgement).
    + If only one wall has holds, #tref("layback", body: [layback]) the edge of the corner. Walk your feet up the blank wall.
    + Spread your feet wide to rest. Often you can let go with both hands#ix("Resting on the wall") #src("E17").
  ],
  when: [
    - *Look for* two wall panels that meet at an angle, with footholds or blank faces on both sides.
    - *Look for* two volumes that face each other, or a volume next to a wall. They make a small corner #src("E11").
    - *Look for* a main face with no footholds next to a side wall that is "in" (part of the problem). Push on the side wall.
    - *Symptom:* your arms tire in a corner although both walls have footholds.
    - *Symptom:* you face one wall with both feet on it. The corner gives you nothing.
  ],
  errors: [
    - Gripping hard instead of pressing. Open your hands and push.
  ],
  tall: [Long legs let you bridge wide corners and reach a no-hands rest that shorter climbers can't. In a tight corner, turn sideways so your knees don't hit the back wall.],
  related: ("stemming", "palming", "layback", "opposition", "knee-bar"),
  sources: ("E11", "E17", "E20", "E24"),
)

#technique(
  key: "traverse",
  name: "Traverses",
  aliases: ("traversing",),
  category: "terrain",
  grade: 1,
  grade-note: [Traverses appear at every grade. Moving efficiently along them pays off from about V1 (judgement).],
  summary: [A traverse moves sideways rather than up. It rewards fewer, longer moves. Cross your hands through instead of shuffling them. #tref("flag", body: [Flag], show-page: false) a leg instead of swapping feet #src("E25", "E11").],
  figure: "traverse.svg",
  caption: [Moving right. The left hand crosses over the right arm to the next hold. The left leg flags behind, so the right foot can stay where it is.],
  how: [
    + Read which way each handhold faces. On traverses many are #tref("sidepull", body: [sidepulls], show-page: false) that face back the way you came. You lean away from them, towards where you are going #src("E21").
    + Cross through. Move the trailing hand over the leading arm to the next hold. Each move then covers two holds' distance #src("E25"). See #tref("cross-through").
    + When the feet don't line up with the hands, flag the trailing leg. Don't swap feet on one foothold. Double foot swaps are a common fault #src("E11"). See #tref("back-flag").
    + When the holds line up, cross your legs and stand on the outside edge of the leading foot #src("E12").
    + Keep your arms straight. Move your hips sideways first, then the hand. See #tref("straight-arms").
  ],
  when: [
    - *Look for* start and finish holds at about the same height.
    - *Look for* sidepulls and upright edges that face back the way you came.
    - *Look for* a line of footholds that runs along the wall below the handholds.
    - *Symptom:* you make lots of small hand shuffles and #tref("matching", body: [match], show-page: false) on every hold.
    - *Symptom:* you swap feet on almost every foothold and get #jt("pumped") (forearms tired and swollen) on easy holds.
  ],
  errors: [
    - Matching on every hold. Each match costs a move.
    - Staying square to the wall all the way. On steeper sections, turn the leading hip in. See #tref("hip-turn").
  ],
  related: ("cross-through", "flag", "back-flag", "foot-swap", "sidepull", "matching"),
  sources: ("E11", "E12", "E21", "E25"),
)

#technique(
  key: "slab",
  name: "Slab technique",
  aliases: ("slab", "friction climbing"),
  category: "terrain",
  grade: 2,
  grade-note: [Slab basics matter from V2–V3, as footholds shrink to small edges and blank wall. Gyms set slab and tricky footwork on purpose, to teach footwork and to make easy problems interesting #src("E46", "E52").],
  summary: [On a wall that leans back, almost all your weight can sit on your feet. Slab technique keeps it there: your hips stay over your feet, and your hands press and balance rather than pull #src("E1", "E3", "E24").],
  figure: "slab.svg",
  caption: [(a) Leaning the chest in pushes the foot out and off the smear. (b) Hips stacked over the foot, heel low. The weight goes straight down through the rubber.],
  how: [
    + Before each step, shift your hips over the foot you will stand on. Then stand. The weight presses the shoe onto the hold #src("E3").
    + Keep your hips back over your toes. Don't press your chest to the wall. Leaning in pushes the feet outward and off #src("E3", "E24").
    + On a #tref("smearing", body: [smear], show-page: false) (a foot pressed flat on blank wall), drop the heel so more of the front of the sole touches. On small edges, stand on the big toe, not the side of the foot #src("E1", "E3").
    + Commit all your weight to the foot at once.#ix("Commitment") Keep the pressure steady through the move. A half-weighted shoe skates #src("E1", "E16").
    + Take several small steps rather than one big high step #src("E16", "A34").
    + Use the handholds to steer, not to pull. Come at them from the side and let them guide you over your foot #src("E4"). Where there are none, press a flat palm on the wall #src("E3"). See #tref("palming").
    + To gain height with no holds, press down on your palms. Straighten your arms as you rise #src("E1"). See #tref("mantle").
    + Rest a tired calf by putting your heel on a hold. Point the toe down and away. Lean in so the bone takes the weight, then shake out the other leg #src("E1").
    + Move slowly enough to feel each balance point #src("E3").
  ],
  when: [
    - *Look for* a wall that leans back, with blank wall, tiny edges or big flat #tref("volume", body: [volumes], show-page: false) instead of solid footholds.
    - *Look for* handholds that are rounded, small or facing sideways. The problem wants you to stand, not pull.
    - *Look for* a vertical wall with big volumes where you'll mostly push. Climb it as a slab #src("E6").
    - *Symptom:* your foot skates the moment you stand up on it.
    - *Symptom:* you stand on a foothold but can't let go with either hand.
    - *Symptom:* your calves burn. Your fingers ache from squeezing holds that don't help.
  ],
  errors: [
    - Placing the foot near a hold rather than on its best part #src("E1").
    - Testing a foothold again and again instead of committing #src("E16", "A6").
    - Shoes so tight they can't bend. A looser pair helps on smears #src("E1").
  ],
  tall: [Long legs reach high steps easily. But a high step folds you up and leaves your hips behind your feet. Take the lower foothold and stand up in two steps.],
  related: ("smearing", "edging", "palming", "rockover", "high-step", "precise-footwork", "dynamic-slab", "volume"),
  sources: ("E1", "E3", "E4", "E16", "E24", "E46", "E52", "A6", "A34"),
)

#filmstrip("filmstrip-top-out.svg", [The top-out mantle], [Watch the chest: it stays over the lip from the palm press onward, so the foot can come up beside the hands and the hips rise over it.])

#technique(
  key: "top-out",
  name: "Top-outs",
  aliases: ("topping out", "heel-hook rockover"),
  category: "terrain",
  grade: 2,
  grade-note: [Matters wherever your gym has boulders you can stand on top of. Finishes like this are common from V2–V4 (judgement).],
  summary: [A top-out takes you from hanging on the #jt("lip") (the top edge of the wall) to standing on top. On a flat top you press down on your palms, which is a #tref("mantle"). On a rounded or steep lip you first hook a heel over it, then roll over the heel.],
  figure: "top-out.svg",
  caption: [(a) From behind: left foot high, right heel hooked on the lip beside the hands. (b) From the side: the climber has rolled from heel to toe. The chest leans over the top and the palms press down.],
  how: [
    + Get your feet high before you commit at the lip. Waist height is ideal #src("E14", "E23").
    + Swing a heel onto the lip. Place it on an edge, bump or dimple. You can't adjust it once you load it #src("E14", "E23"). On a rounded lip, or one that leans out, get the heel up first. It takes weight off your arms #src("E13", "A8"). See #tref("heel-hook").
    + Pull with your arms and the heel together. Straighten the lower leg as you pull #src("E14", "A8").
    + Turn the knee of the heel leg in. Bring your chest over the lip. #tref("flag", body: [Flag], show-page: false) the other leg, or press its foot on the wall, as a counterweight #src("E14", "E23").
    + When your hips reach the lip, roll from the heel onto the toe. Keep the foot close to your hands, not far to the side #src("E23").
    + Turn one palm flat on top, then the other. Press down. Let go of the heel, bring the other leg up and stand #src("E14", "E22").
  ],
  when: [
    - *Look for* a problem marked "top out" instead of a finishing hold.
    - *Look for* a rounded or sloping lip with nothing to hold on top. Heel first.
    - *Look for* a flat top or ledge. Mantle.
    - *Look for* the way down before you start: stairs, a ladder or climbing down#ix("Downclimbing!finding the way down") #src("E65", "E33").
    - *Symptom:* you end up lying flat on top with nothing to push on #src("E22").
    - *Symptom:* you hang at the lip with low feet and can't get your hips up.
  ],
  errors: [
    - Hesitating halfway. Once you start, commit#ix("Commitment") #src("E23").
    - Reaching blindly over the top with a hand instead of pressing #src("E22").
    - Belly-flopping over a steep top. If it isn't working, jump off while you still control the fall#ix("Bailing!from a top-out") #src("E22").
    - Learning on a high wall. Practise low mantles first, then problems that finish with one #src("E22").
  ],
  tall: [Your reach puts both palms well back on the top, so the press is easier. But your hips have further to travel. Get the heel up early instead of relying on your arms.],
  related: ("mantle", "heel-hook", "rockover", "palming", "high-step"),
  sources: ("E13", "E14", "E22", "E23", "E33", "E65", "A8"),
)

#technique(
  key: "volume",
  name: "Volumes",
  aliases: ("volume climbing",),
  category: "terrain",
  grade: 2,
  grade-note: [Standing on a volume matters from about V2. Some gyms set problems on volumes alone #src("E19"). They are harder to read and appear from about V4 (judgement).],
  summary: [Volumes are big hollow shapes bolted to the wall. They act as holds, footholds and pieces of wall. Most have no edge to pull on. You stand on their faces, press them, pinch their edges or squeeze them between your hands or feet #src("E18", "E19", "E11").],
  figure: "volume.svg",
  caption: [(a) Standing near the wall on the volume's sloping top. The slope pushes the foot out. (b) Standing on the far edge, hips over the foot, heel lower than the toe.],
  how: [
    + Stand on the far side of the volume, away from the wall, so your hips are over your foot.#ix("Volumes!standing on") Smear with the front half of the shoe. Keep the heel lower than the toes #src("E5", "E18").
    + Use the whole face. Put as much rubber on it as you can. Use palms rather than fingertips. Chalk the whole hand #src("E18").
    + Look for an edge. Grab it as a #tref("pinch", body: [pinch], show-page: false), or as a "meat hook": palm on one face, fingers over the other #src("E18").
    + On a rounded volume, find the bulge or the scoop. Chalk marks#ix("Chalk marks") show where others found grip #src("E18").
    + On a sloping volume, get underneath it. Hang low on straight arms so gravity pulls you onto it #src("E18"). See #tref("sloper").
    + Push hands and feet against the direction you're moving. With a flexed foot, push down and pull in with the heel #src("E18").
    + On steep ground, squeeze the volume between your feet or your hands. See #tref("compression") #src("E18", "E11").
    + Step back and look at the sides and underside. You may find hidden holds, spots for heel and toe hooks, or room for a #tref("knee-bar", body: [knee bar], show-page: false) between close volumes #src("E11").
  ],
  when: [
    - *Look for* faces with no holds. You are meant to stand on them or press them.
    - *Look for* a sharp volume edge. It is a hold, often a small #tref("arete", body: [arête], show-page: false).
    - *Look for* two volumes close together. Squeeze them, or bridge or knee-bar between them.
    - *Look for* your gym's rule. Volumes are usually part of every problem on that wall #src("E19").
    - *Symptom:* your foot slides off as you stand up on a volume.
    - *Symptom:* you rush, slap and slide off a volume with nothing to hold.
  ],
  errors: [
    - Rushing. On holds without an obvious grip, speed works against you #src("E18").
    - Standing next to the wall on vertical or slab ground. You get pushed backwards #src("E18").
    - Sloppy placements that scrape your skin #src("E18").
    - Half-committing. If you don't expect to stay on, you won't#ix("Commitment") #src("E18").
  ],
  tall: [Long arms and legs make squeezing and far-side standing easier. You will get folded up between close volumes. Look for a wider span or a higher foot.],
  related: ("compression", "palming", "pinch", "sloper", "smearing", "knee-bar", "slab", "dynamic-slab", "arete"),
  sources: ("E5", "E11", "E18", "E19"),
)

#technique(
  key: "arete",
  name: "Arêtes",
  aliases: ("arete",),
  category: "terrain",
  grade: 3,
  grade-note: [Arêtes appear on easy problems. Controlling the swing they cause matters from about V3 (judgement).],
  summary: [An arête is an outside edge of the wall. Climb it by laybacking: your hands pull the edge one way and your feet push the other. Or mix the edge with holds on the face. Keep your body at an angle to the edge so it doesn't swing you open #src("E2", "E17").],
  figure: "arete.svg",
  caption: [(a) Layback. The hands pull the edge to the left. The feet push on the side face to the right. (b) A heel hooked round the arête stops the body swinging open.],
  how: [
    + For each section, decide: the arête only, or the arête plus holds on the face. On harder problems the mix is usually best #src("E2").
    + Where the face is blank, #tref("layback", body: [layback]). Both hands pull the edge. Your feet push on the side face. Walk hands and feet up in turn #src("E2").
    + Keep your arms straight so your feet do the work #src("E24").
    + Hold your body at about 45° to the arête, halfway between the two faces. Too close to the wall and smeared feet slip. Too far round and the edge feels worse. You also swing open #src("E2").
    + Hook a heel round the arête. It stops the swing and rests your arms #src("E2"). See #tref("heel-hook").
    + If you start to swing, tense your #jt("core") (the muscles around your trunk) at once #src("E2"). Better still, set the body angle so the swing never starts. See #tref("barn-door").
  ],
  when: [
    - *Look for* a corner of the wall, or a volume's edge, marked as part of the problem.
    - *Look for* a face with few holds next to the edge. Layback.
    - *Look for* a good face hold level with the edge. Pull the two apart. See #tref("opposition").
    - *Symptom:* you swing off like a door when you move a hand #src("E2").
    - *Symptom:* your feet smear off and you bash your shins on the edge #src("E2").
  ],
  errors: [
    - No backup plan. Work out the other possible sequences before you leave the ground #src("E2").
  ],
  tall: [Your span lets you hold a face hold and the arête at once, which makes the opposition stronger. A long body also swings further. Set the heel hook early.],
  related: ("layback", "heel-hook", "barn-door", "opposition", "pinch", "flag", "corner"),
  watch: (("Neil Gresham Climbing Masterclass - Crux Films", "26  Neil Greshams Masterclass - Aretes", "https://www.youtube.com/watch?v=juMNJz7Wn6g"),),
  sources: ("E2", "E17", "E24"),
)

#technique(
  key: "overhang",
  name: "Overhangs",
  aliases: ("steep ground",),
  category: "terrain",
  grade: 3,
  grade-note: [Hörst#ix("Hörst, Eric") suggests learning the steep-ground moves on problems about 20° past vertical #src("E9"). Gresham#ix("Gresham, Neil") lists bent arms with square hips on steep ground as a beginner-to-intermediate fault#ix("Beginners!common faults") #src("E11").],
  summary: [Past vertical, gravity pulls your hips away and your arms take more weight. Overhang technique fights that with high feet that pull, hips turned into the wall and straight arms #src("E7", "E8", "E9", "E11").],
  figure: "overhang.svg",
  caption: [(a) Low feet and high hands. The body hangs in a straight line and the feet come off. (b) Feet up, toes pulling in, arms straight, hips close.],
  how: [
    + Bring your feet up as the wall steepens. Your legs then keep a share of the weight #src("E8").
    + Press each toe down and into its hold, as if gripping with it. Don't slap the ball of the foot onto it #src("E8", "E11"). See #tref("toe-pull").
    + Hang on straight arms between moves #src("E7", "E8"). See #tref("straight-arms").
    + To reach, turn the hip on the reaching side into the wall. Stand on the outside edge of that foot (the little-toe side), on a hold below or behind you. Brace the other foot so you stand on a tripod #src("E9", "E11"). See #tref("backstep") and #tref("twist-lock").
    + For a longer reach without jumping, use a #tref("drop-knee") #src("E7").
    + Start each move with your hips, then pull. Don't lead with your head #src("E8").
    + Where the footholds face sideways or down, hook them. See #tref("heel-hook") and #tref("toe-hook").
  ],
  when: [
    - *Look for* a wall that leans over you, with footholds below and to the side of the handholds. Turn in; don't stay square.
    - *Look for* sidepulls and footholds that face sideways. Backstep or drop-knee.
    - *Look for* holds under features. They are toe-hook targets.
    - *Symptom:* your arms are #jt("pumped") (tired and swollen) after a few moves.
    - *Symptom:* your feet swing off the wall when you reach.
    - *Symptom:* the next hold is a few centimetres out of reach while your hips are square.
  ],
  errors: [
    - Square, #tref("frog", body: [frog-style], show-page: false) hips on steep ground #src("E11", "E12").
    - Low feet and high hands. Stretched out, your feet come off #src("E8").
    - Swinging and slapping as a habit. Practise climbing steep ground slowly, without swinging #src("E8").
    - Hips that zig-zag instead of moving straight into the next position #src("E11").
  ],
  tall: [Your reach lets you climb stretched out with low feet. Resist it. Bring your feet up and keep your hips under you.],
  related: ("hip-turn", "backstep", "drop-knee", "twist-lock", "straight-arms", "toe-pull", "toe-hook", "heel-hook", "body-tension", "roof"),
  watch: (("Mani the Monkey", "How to Climb Overhangs: Techniques + Skills", "https://www.youtube.com/watch?v=FPrdTd7tMdc"),),
  sources: ("E7", "E8", "E9", "E11", "E12"),
)

#technique(
  key: "roof",
  name: "Roofs",
  aliases: ("roof climbing", "turning the lip"),
  category: "terrain",
  grade: 4,
  grade-note: [Roofs on low grades usually have big holds and big footholds. Once the footholds face down or sideways, around V4–V5, your feet must hook to stay on (judgement).],
  summary: [On a roof your body hangs nearly flat and the footholds face down. Feet that push swing off. Keep them on by pulling with your toes and heels. Then hook a heel over the #jt("lip") (the edge where the roof ends) to get over it #src("E7", "E15", "E13").],
  figure: "roof.svg",
  caption: [(a) Feet pushing on a down-facing hold swing off. (b) Arms straight and toes pulling on the hold: the feet stay on.],
  how: [
    + Hang on straight arms #src("E7").
    + Keep your feet on by pulling. Flex the foot and pull the toes towards you under a hold, using your shin muscles #src("E7", "E20"). See #tref("toe-hook").
    + For a more solid foot, push one toe on top of a hold and hook the other toe behind it. Squeeze the feet together #src("E7", "E15"). See #tref("bicycle").
    + Use heel hooks along edges and breaks as a third arm #src("E15", "E13"). See #tref("heel-hook").
    + Before you set a toe hook, plan how it comes out. Move your feet in small steps, so they don't swing off when you release it #src("E15", "A12"). See #tref("cutting-loose").
    + Look to the sides for toe hooks. They are outside your normal view #src("E15", "A12").
    + On a big roof, consider going feet first. Hook a high toe, then swing your body round after it #src("E15", "A12").
    + At the lip, heel-hook first, then roll over the heel. See #tref("top-out") #src("E13", "E7").
  ],
  when: [
    - *Look for* holds on the ceiling and footholds that face down or sideways.
    - *Look for* holds with a hollow underside, and the backs of holds. They are toe-hook targets #src("E15").
    - *Look for* a hold you can reach with both feet at once. Bicycle it.
    - *Symptom:* your feet swing off as soon as you move a hand.
    - *Symptom:* you hang with no feet at the lip and can't get over it.
  ],
  errors: [
    - Flat shoes. Downturned shoes clamp better.#ix("Climbing shoes!downturned") Rubber on top of the toe helps toe hooks #src("E15", "E5").
  ],
  tall: [Long legs reach foot hooks further from your hands. Keeping a long body flat costs more tension. Bring your feet in closer when you can.],
  related: ("toe-hook", "bicycle", "heel-hook", "knee-bar", "cutting-loose", "body-tension", "campus-move", "overhang", "top-out"),
  watch: (("Neil Gresham Climbing Masterclass - Crux Films", "19  Neil Greshams Masterclass - Roofs", "https://www.youtube.com/watch?v=LNdQDLokHRY"),),
  sources: ("E5", "E7", "E13", "E15", "E20", "A12"),
)

#technique(
  key: "sit-start",
  name: "Sit starts",
  aliases: ("SDS", "sit-down start", "low start"),
  category: "terrain",
  grade: 4,
  grade-note: [Forum climbers say the first move off the mat often needs a burst of power #src("E26"). Sit starts become common around V3–V5 (judgement).],
  summary: [The problem starts with you sitting on the mat, hands on the start holds. The first move lifts your bottom off the floor. Turn sideways and use the outside edge of your shoe instead of folding up square #src("E11").],
  figure: "sit-start.svg",
  caption: [(a) Square on, knees splayed, bottom away from the wall: the first pull is all arms. (b) Hips turned, outside edge on the foothold, bottom close to the wall.],
  how: [
    + Sit with your bottom close to the wall #src("E11", "E26").
    + Turn your hips about 90° to the wall. Stand on the outside edge of the working foot (the little-toe side) #src("E11"). See #tref("edging").
    + If both footholds are straight below the start holds, a wide #tref("frog", body: [frog position], show-page: false) works too: bottom tucked close to the wall, chest dropped between your knees.
    + Lean back on the start holds if they allow it #src("E11"). See #tref("layback").
    + Rock back a little. Then pull and stand in one movement. Or roll one knee onto the mat and push off it #src("E11").
    + Check the rule at your gym.#ix("Gym rules") Some gyms want you still on the start holds before you move (judgement). If in doubt, ask the staff #src("E55").
  ],
  when: [
    - *Look for* "sit" or "SDS" on the tag, or start holds just above the mat.
    - *Look for* a low foothold to one side of the start holds. That is your outside-edge foot.
    - *Symptom:* you can hold the start but can't lift your bottom off the mat.
    - *Symptom:* you sit square with your knees splayed and your bottom away from the wall. The first pull is all arms #src("E11").
  ],
  errors: [
    - Bouncing off the mat on a problem whose rules want a controlled start.
  ],
  tall: [With long legs, your bottom may still be on the mat where a shorter climber would already hang#ix("Tall climbers!sit starts") (judgement). Sit to the side of the start holds. Lay your free leg flat along the mat instead of folding your knees under your chest.],
  related: ("layback", "edging", "hip-turn", "frog", "body-tension", "pre-loading"),
  sources: ("E11", "E26", "E55"),
)

#technique(
  key: "dynamic-slab",
  name: "Dynamic slab",
  aliases: ("comp slab", "coordination slab"),
  category: "terrain",
  grade: 5,
  grade-note: [One gym's #jt("circuit", body: [circuits]) (colour groups of problems) move from teaching skills to testing them with dynamic moves around V4–V6 #src("E52"). In the 2019 World Cup#ix("World Cup!coordination moves") finals, 18% of problems had a #jt("coordination move") (at least three hand or foot placements within two seconds) #src("E6").],
  summary: [Modern gym slab is often not slow balance. You jump or run between #tref("volume", body: [volumes], show-page: false) and catch holds and footholds while moving. The skill is planning where your body must end up, so you arrive balanced #src("E5", "E6", "E27").],
  figure: "dynamic-slab.svg",
  caption: [Plan from the end. The climber starts on the left volume (dashed). The plan: land the right foot on the far volume (1). Catch the sloper (2). Then place the left foot (3).],
  how: [
    + Warm up hips, knees and ankles as well as fingers.#ix("Warm-up!for dynamic moves") You will fall a lot, from odd positions, so learn to fall first#ix("Falling!practice") (Chapter 9) #src("E5").
    + Read the end position first. Where must each foot and hand be when the move stops? Plan the steps backwards from there #src("E27", "E5").
    + Decide how far from the wall you take off and land. Aim for an arc that ends balanced, not chest against the wall or overstretched #src("E5", "E27").
    + On a volume, land on the far side, hips over your feet. See #tref("volume") #src("E5").
    + Stay relaxed until the catch. Tense only as you land #src("E5", "E27").
    + Think "pull my body into the end position", not "grab the hold" #src("E27").
    + Work long sequences one contact at a time. Get the first right, then add the second #src("E5").
    + Where the fall is safe, try to ride out a foot slip instead of jumping off #src("E5").
  ],
  when: [
    - *Look for* big volumes with no holds, spaced further apart than you can step.
    - *Look for* a single good hold or foothold on a far volume.
    - *Look for* chalk and shoe marks in odd places. Others have been landing there #src("E5").
    - *Symptom:* you reach the target foot but topple backwards, because your hips arrived behind your feet, too far from the wall.
    - *Symptom:* you can reach each position slowly but can't stop in it.
  ],
  errors: [
    - Launching at the wall instead of along it.
  ],
  related: ("run-and-jump", "foot-catch", "deadpoint", "latching", "tic-tac", "slab", "volume", "smearing"),
  watch: (("Gripped", "Top Olympian Tomoa Narasaki Teaches Coordination", "https://gripped.com/?p=40443"),),
  sources: ("E5", "E6", "E27", "E52"),
)
