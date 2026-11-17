#import "../template.typ": *

= Terrain

The angle and shape of the wall decide which techniques a #jt("problem") needs. On a slab you stand and balance. On an overhang you hang and pull with your feet. On an arête you fight a swing. For each kind of terrain, this chapter says what changes in your body position and what to look for before you start.

The entries here don't repeat how to do a heel hook or a drop knee. They say where the terrain asks for one and why, and link to the full entry.

The map shows this chapter's entries by grade. A line joins techniques that build on each other, and #link(<technique-map>)[the technique map] has all five chapters on one page.

#technique-map(only: "terrain")

== How the wall angle changes your body

The steeper the wall, the more of your weight your arms carry (@hips-and-the-wall explains why). A #tref("volume", body: [volume], show-page: false) (a big hollow shape bolted to the wall) can turn a vertical wall into a slab for one move.#ix("Volumes!as a slab") A study of World Cup problems counted a wall as "slab-like" when climbers mostly pushed on holds rather than pulled #src("E6"). Use the same test: if a problem mostly asks you to push, climb it like a slab.

#ix("Wall angle", main: true)
#{
  set par(justify: false)
  table(
    columns: (auto, 1.25fr, 1fr, 1fr),
    table.header(th[Wall], th[Your weight and hips], th[Your hands], th[What goes wrong]),
    [#tref("slab", body: [Slab], show-page: false)], [Almost all your weight is on your feet. Your hips are over your toes, slightly away from the wall.], [Press, palm and steer.], [Feet skate off. Pulling on the hands levers the feet off #src("E1", "E3", "E4").],
    [Vertical], [Most of your weight stays on your feet if your hips stay close to the wall.], [Stand tall. A slightly bent arm is fine.], [Your hips drift out, so you over-grip #src("E10").],
    [#tref("overhang", body: [Overhang], show-page: false)], [Your arms carry more as the angle grows. Turn your hips sideways into the wall.], [Keep your arms straight. Let your feet pull as well as push.], [You stay square and bend your arms. Your feet come off #src("E8", "E9", "E11").],
    [#tref("roof", body: [Roof], show-page: false)], [Your body is nearly horizontal. Your feet must hook to stay on.], [Keep your arms straight. Foot hooks act as a third arm.], [Your feet swing off #src("E7", "E15").],
    [#tref("arete", body: [Arête], show-page: false)], [Your weight is split between the edge and the face beside it.], [Pull the edge and push with your feet.], [Your body swings open like a door #src("E2").],
    [Corner], [You press out into both walls. See #tref("stemming").], [Press or rest.], [You put both feet on one wall, so your arms do the work #src("E20", "E24").],
  )
}

#fig("terrain-wall-angles.svg", caption: [The same climber on four wall angles. The dashed line drops from the #jt("centre of gravity") (the body's balance point). On the slab it falls on the foot. On the vertical wall it falls close to it. On the overhang and the roof it falls well behind the feet, so the arms take more weight.])

== Vertical walls

A vertical wall needs no technique of its own, but it breaks one slab habit.#ix("Vertical walls", main: true) On a slab you can balance over one foot without your hands. On a vertical wall gravity pulls your hips out from the wall, so you can't #src("E10").

- Before each move, bring your hips *in* towards the wall as well as *over* the heel of the standing foot. Climbers who move their hips only left and right leave them slightly out, so they put weight on their arms and over-grip #src("E10").
- Stand on the inside edge of the shoe with your hips more or less square. Switch to the outside edge (the little-toe side) with crossed legs when the holds line up. When they don't, #tref("flag", body: [flag]) instead of swapping feet #src("E12"). See #tref("edging").
- On a volume, stand on the far side, away from the wall. See #tref("volume").

== V1–V2: volumes, slabs, traverses and~top-outs

#technique(
  key: "volume",
  name: "Volumes",
  aliases: ("volume climbing",),
  category: "terrain",
  grade: 1,
  grade-note: [Standing on a volume comes early. France's climbing federation teaches balance moves on volumes at the third of its eight levels #src("F60"). A German gym chain teaches standing on volumes for the step up to Font 4C–5A, about V0–V1 #src("F68", "F69"). One setter recommends volumes on easier problems #src("F72"). Some gyms set problems on volumes alone #src("E19"). The grips, squeezes, hooks and knee bars in steps 3 to 5 and under "By shape" have later badges of their own.],
  summary: [Volumes are big hollow shapes bolted to the wall. They act as holds, footholds and pieces of wall, but most have #cue[nothing to pull down on]. You stand on their faces, press them, pinch their edges or squeeze them between your hands or feet #src("E18", "E19", "E11").],
  figure: "volume.svg",
  caption: [(a) Standing near the wall on the volume's sloping top. The slope pushes the foot out. (b) Standing on the far edge, hips over the foot, heel lower than the toe.],
  how: [
    + Stand on the far side of the volume, away from the wall, so your hips are over your foot.#ix("Volumes!standing on") Smear with the front half of the shoe and keep the heel lower than the toes #src("E5", "E18").
    + Put as much rubber on the face as you can, use palms rather than fingertips and chalk the whole hand #src("E18"). Push hands and feet against the direction you're moving. With a flexed foot, push down and pull in with the heel #src("E18").
    + Look for an edge to grab as a #tref("pinch", body: [pinch], show-page: false), or as a "#tref("wrap", body: [meat hook], show-page: false)": palm on one face, fingers over the other #src("E18").
    + On steep ground, squeeze the volume between your feet or your hands. See #tref("compression") #src("E18", "E11").
    + Step back and look at the sides and underside. You may find hidden holds, spots for heel and toe hooks, or room for a #tref("knee-bar", body: [knee bar], show-page: false) between close volumes #src("E11").

    *By shape:* on a rounded volume, find the bulge or the scoop. Chalk marks#ix("Chalk marks") show where others found grip #src("E18"). On a sloping volume, get underneath it and hang low on straight arms so gravity pulls you onto it #src("E18"). See #tref("sloper").
  ],
  when: [
    *Look for*
    - faces with no holds. You are meant to stand on them or press them.
    - a sharp volume edge. It is a hold, often a small #tref("arete", body: [arête], show-page: false).
    - two volumes close together. Squeeze them or bridge between them, and from about V5 try a knee bar.
    - your gym's rule on volumes (@reading-method, step 1).

    *Symptoms*
    - Your foot slides off as you stand up on a volume.
    - You rush, slap and slide off a volume with nothing to hold. On holds without an obvious grip, speed works against you #src("E18").
  ],
  errors: [
    - Sloppy placements that scrape your skin #src("E18").
    - Half-committing. If you don't expect to stay on, you won't#ix("Commitment") #src("E18").
  ],
  tall: [Tall climbers get bunched up where holds sit close together #src("E46"), and volumes are no exception. Try dropping a foot lower and sinking onto one leg #src("E76").],
  small: [One head #jt("setter") (the person who designs the problems) angles some volumes so that climbers can smear along the whole face, which evens out height differences #src("H10"). So before you decide a step is too high, look along the face for a spot you can reach, on the far side if you can.],
  related: ("compression", "palming", "pinch", "sloper", "smearing", "knee-bar", "slab", "dynamic-slab", "arete", "stemming", "heel-hook", "toe-hook", "wrap"),
  sources: ("E5", "E11", "E18", "E19", "H10"),
)

#technique(
  key: "slab",
  name: "Slab technique",
  aliases: ("slab", "friction climbing"),
  category: "terrain",
  grade: 2,
  grade-note: [Slab basics matter from V2–V3, as footholds shrink to small edges and blank wall. Gyms set slab and tricky footwork on purpose, to teach footwork and to make easy problems interesting #src("E46", "E52").],
  summary: [On a wall that leans back, almost all your weight can sit on your feet. Slab technique keeps it there: your hips stay #cue[over your feet], and your hands #cue[press and balance] rather than pull #src("E1", "E3", "E24").],
  figure: "slab.svg",
  caption: [(a) Leaning the chest in pushes the foot out and off the smear. (b) Hips stacked over the foot, heel low. The weight goes straight down through the rubber.],
  how: [
    + Before each step, shift your hips over the foot you will stand on #src("E3"). See #tref("weight-shift"). Keep your hips back over your toes and your chest off the wall #src("E3", "E24").
    + On a smear (a foot pressed flat on blank wall), drop the heel, as in #tref("smearing"). On small edges, stand on the big toe, not the side of the foot #src("E1", "E3").
    + Commit all your weight to the foot at once#ix("Commitment") and keep the pressure steady through the move. A half-weighted shoe skates #src("E1", "E16").
    + Take several small steps rather than one big high step #src("E16", "A34"), slowly enough to feel each balance point #src("E3").
    + Come at the handholds from the side and let them steer you over your foot #src("E4"). Where there are none, press a flat palm on the wall #src("E3"). See #tref("palming").
    + To gain height with no holds, press down on your palms and straighten your arms as you rise #src("E1"). See #tref("mantle").

    *To rest a tired calf,* put your heel on a hold with the toe pointing down and away. Shift your weight onto that heel so the calf can relax, then shake out the other leg #src("E1").
  ],
  when: [
    *Look for*
    - a wall that leans back, with blank wall, tiny edges or big flat #tref("volume", body: [volumes], show-page: false) instead of solid footholds. Its handholds are rounded, small or facing sideways: the problem wants you to stand, not pull.
    - a near-vertical wall with big volumes where you'll mostly push #src("E6"). Climb it as a slab.

    *Symptoms*
    - Your foot skates the moment you stand up on it.
    - You stand on a foothold but can't let go with either hand.
    - Your calves burn and your fingers ache from squeezing holds that don't help.
  ],
  errors: [
    - Placing the foot near a hold rather than on its best part #src("E1").
    - Shoes so tight they can't bend. A looser pair helps on smears #src("E1").
  ],
  related: ("smearing", "edging", "palming", "rockover", "high-step", "precise-footwork", "dynamic-slab", "volume", "weight-shift", "mantle"),
  sources: ("E1", "E3", "E4", "E6", "E16", "E24", "E46", "E52", "A34"),
)

#technique(
  key: "traverse",
  name: "Traverses",
  aliases: ("traversing",),
  category: "terrain",
  grade: 2,
  grade-note: [Traverses appear at every grade: France's climbing federation has climbers traverse at its first level #src("F60"). Moving efficiently along one takes a #tref("cross-through", body: [cross-through]) and a #tref("flag", body: [side flag]), which both have a V2 badge. The back flag in the figure has a V3 badge, so until then use a side flag where you can.],
  summary: [A traverse moves sideways rather than up and rewards #cue[fewer, longer moves]. Cross your hands through instead of shuffling them, and #tref("flag", body: [flag], show-page: false) a leg instead of swapping feet #src("E25", "E11").],
  figure: "traverse.svg",
  caption: [Moving right. The left hand crosses over the right arm to the next hold. The left leg flags behind, so the right foot can stay where it is.],
  how: [
    + Read which way each handhold faces. On traverses many are #tref("sidepull", body: [sidepulls], show-page: false) that face back the way you came. You lean away from them, towards where you are going #src("E21").
    + Cross the trailing hand over the leading arm to the next hold, so that each move covers two holds' distance #src("E25"). See #tref("cross-through").
    + When the feet don't line up with the hands, flag the trailing leg instead of swapping feet on one foothold. Double foot swaps are a common fault #src("E11"). See #tref("flag") and, from V3, #tref("back-flag"). Save a #tref("foot-swap", body: [foot swap]) for a stretch with only one good foothold.
    + When the holds line up, cross your legs and stand on the outside edge of the leading foot #src("E12").
    + On steep sections, keep your arms straight and move your hips sideways before the hand. See #tref("straight-arms").
  ],
  when: [
    *Look for* start and finish holds at about the same height, with a line of footholds that runs along the wall below the handholds.

    *Symptoms*
    - You make lots of small hand shuffles and #tref("matching", body: [match], show-page: false) on every hold.
    - You swap feet on almost every foothold and get #jt("pumped") (forearms tired and swollen) on easy holds.
  ],
  errors: [
    - Staying square to the wall all the way. On steeper sections, turn the leading hip in. See #tref("hip-turn").
  ],
  related: ("cross-through", "flag", "back-flag", "foot-swap", "sidepull", "matching", "hip-turn"),
  sources: ("E11", "E12", "E21", "E25"),
)

#filmstrip("filmstrip-top-out.svg", [The top-out mantle], [Watch the chest: it stays over the top edge from the palm press onward, so the foot can come up beside the hands and the hips rise over it.])

#technique(
  key: "top-out",
  name: "Top-outs",
  aliases: ("topping out", "heel-hook rockover"),
  category: "terrain",
  grade: 2,
  grade-note: [Topping out matters wherever your gym has boulders you can stand on top of, from your first session there. The UK's bouldering-instructor award lists safe topping out among the basics for novices #src("F62"). The #tref("heel-hook", body: [heel hook]) for a rounded lip has a V3 badge, so try it low on the wall first.],
  summary: [A top-out takes you from hanging on the #jt("lip") (the top edge of the wall) to standing on top. On a flat top you #cue[press down] on your palms, which is a #tref("mantle", body: [mantle]). On a rounded or steep lip you first #cue[hook a heel] over it, then roll over the heel.],
  figure: "top-out.svg",
  caption: [(a) From behind: left foot high, right heel hooked on the lip beside the hands. (b) From the side: the climber has rolled from heel to toe. The chest leans over the top and the palms press down.],
  how: [
    + Get your feet high before you commit at the lip, ideally to waist height #src("E14", "E23").
    + Swing a heel onto an edge, bump or dimple on the lip. You can't adjust it once you load it #src("E14", "E23"). On a rounded lip, or one that leans out, get the heel up first to take weight off your arms #src("E13", "A8"). See #tref("heel-hook").
    + Pull with your arms and the heel together, straightening the lower leg #src("E14", "A8"). Turn the knee of the heel leg in and bring your chest over the lip. #tref("flag", body: [Flag], show-page: false) the other leg, or press its foot on the wall, as a counterweight #src("E14", "E23").
    + When your hips reach the lip, roll from the heel onto the toe and keep the foot close to your hands #src("E23").
    + Turn one palm flat on top, then the other, and press down. Let go of the heel, bring the other leg up and stand #src("E14", "E22").
  ],
  when: [
    *Look for*
    - a problem marked "top out" instead of a finishing hold.
    - a rounded or sloping lip with nothing to hold on top. Get a heel up first.
    - a flat top or ledge. Mantle.
    - the way down before you start: stairs, a ladder or climbing down#ix("Downclimbing!finding the way down") #src("E65", "E33").

    *Symptoms*
    - You end up lying flat on top with nothing to push on #src("E22").
    - You hang at the lip with low feet and can't get your hips up.
  ],
  errors: [
    - Hesitating halfway. Once you start, commit#ix("Commitment") #src("E23").
    - Reaching blindly over the top with a hand instead of pressing #src("E22").
    - Belly-flopping over a steep top. If it isn't working, jump off while you still control the fall#ix("Bailing!from a top-out") (@cons-falling) #src("E22").
    - Learning on a high wall. Practise low mantles first, then problems that finish with one #src("E22").
  ],
  related: ("mantle", "heel-hook", "rockover", "palming", "high-step"),
  sources: ("E13", "E14", "E22", "E23", "E33", "E65", "A8"),
)

== V3: overhangs, arêtes and sit starts

#technique(
  key: "overhang",
  name: "Overhangs",
  aliases: ("steep ground",),
  category: "terrain",
  grade: 3,
  grade-note: [Start on the gentle overhangs that become common from V2. Hörst#ix("Hörst, Eric") suggests learning the steep-ground moves on problems about 20° past vertical #src("E9"). Gresham#ix("Gresham, Neil") lists bent arms with square hips on steep ground as a beginner-to-intermediate fault#ix("Beginners!common faults") #src("E11").],
  summary: [Past vertical, gravity pulls your hips away and your arms take more weight. Overhang technique fights that with high #cue[feet that pull], #cue[hips turned] into the wall and #cue[straight arms] #src("E7", "E8", "E9", "E11").],
  figure: "overhang.svg",
  caption: [(a) Low feet and high hands. The body hangs in a straight line and the feet come off. (b) Feet up, toes pulling in, arms straight, hips close.],
  how: [
    + Bring your feet up as the wall steepens, so that your legs keep a share of the weight #src("E8"). Press each toe down and into its hold, as if gripping with it. Don't slap the ball of the foot onto it #src("E8", "E11"). See #tref("toe-pull").
    + Hang on straight arms between moves #src("E7", "E8"). See #tref("straight-arms"). Start each move with your hips, then pull. Don't lead with your head #src("E8").
    + To reach, turn the hip on the reaching side into the wall (#tref("hip-turn", inner: true)). Stand on the outside edge of that foot, on a hold below or behind you, and brace the other foot so you stand on a tripod #src("E9", "E11"). See #tref("backstep") and, from V4, #tref("twist-lock").
    + For a longer reach without jumping, use a #tref("drop-knee", body: [drop knee]) #src("E7").
    + Where the footholds face sideways or down, hook them. See #tref("heel-hook") and #tref("toe-hook").
  ],
  when: [
    *Look for*
    - a wall that leans over you, with footholds below and to the side of the handholds. Turn in instead of staying square.
    - sidepulls and footholds that face sideways. Backstep or drop-knee.
    - holds under features. They are toe-hook targets.

    *Symptoms*
    - Your arms are #jt("pumped") after a few moves.
    - Your feet swing off the wall when you reach.
    - The next hold is a few centimetres out of reach while your hips are square.
  ],
  errors: [
    - Square, #tref("frog", body: [frog-style], show-page: false) hips on steep ground #src("E11", "E12").
    - Swinging and slapping as a habit. Practise climbing steep ground slowly, without swinging #src("E8").
    - Hips that zig-zag instead of moving straight into the next position #src("E11").
  ],
  related: ("hip-turn", "backstep", "drop-knee", "twist-lock", "straight-arms", "toe-pull", "toe-hook", "heel-hook", "body-tension", "roof"),
  watch: (("Mani the Monkey", "How to Climb Overhangs: Techniques + Skills", "https://www.youtube.com/watch?v=FPrdTd7tMdc"),),
  sources: ("E7", "E8", "E9", "E11", "E12"),
)

#technique(
  key: "arete",
  name: "Arêtes",
  aliases: ("arete",),
  category: "terrain",
  grade: 3,
  grade-note: [Arêtes appear on easy problems: one setter advises setting them there so that new climbers learn heel hooks and stemming #src("F72"). Controlling the swing they cause takes a #tref("layback", body: [layback]) (badge V2) and often a #tref("heel-hook", body: [heel hook]) (badge V3).],
  summary: [An arête is an outside edge of the wall. Climb it by #cue[laybacking]: your hands pull the edge one way and your feet push the other. Or mix the edge with holds on the face. Keep your body #cue[at an angle] to the edge so it doesn't swing you open #src("E2", "E17").],
  figure: "arete.svg",
  caption: [(a) Layback. The hands pull the edge to the left. The feet push on the side face to the right. (b) A heel hooked round the arête stops the body swinging open.],
  how: [
    + For each section, decide between the arête alone and the arête plus holds on the face. On harder problems the mix is usually best #src("E2").
    + Where the face is blank, #tref("layback", body: [layback]) and walk your hands and feet up in turn #src("E2"). Keep your arms straight so your feet do the work #src("E24").
    + Hold your body at about 45° to the arête, halfway between the two faces. Closer to the wall, smeared feet slip. Further round, the edge feels worse and you swing open #src("E2").
    + Hook a heel round the arête to stop the swing and rest your arms #src("E2"). See #tref("heel-hook"). If you still start to swing, tense your #jt("core") (the muscles of your stomach, back and hips) at once #src("E2"). See #tref("barn-door").
  ],
  when: [
    *Look for*
    - an outside corner of the wall, or a volume's edge, marked as part of the problem.
    - a face with few holds next to the edge. Layback.
    - a good face hold level with the edge. Pull the two apart. See #tref("opposition").

    *Symptoms*
    - You swing off like a door when you move a hand #src("E2").
    - Your feet smear off and you bash your shins on the edge #src("E2").
  ],
  errors: [
    - No backup plan. Work out the other possible sequences before you leave the ground #src("E2").
  ],
  tall: [Your span lets you hold a face hold and the arête at once, which makes the opposition stronger. A long body also swings further, so set the heel hook early.],
  related: ("layback", "heel-hook", "barn-door", "opposition", "pinch", "flag", "stemming"),
  watch: (("Neil Gresham Climbing Masterclass - Crux Films", "Neil Greshams Masterclass - Aretes", "https://www.youtube.com/watch?v=juMNJz7Wn6g"),),
  sources: ("E2", "E17", "E24"),
)

#technique(
  key: "sit-start",
  name: "Sit starts",
  aliases: ("SDS", "sit-down start", "low start"),
  category: "terrain",
  grade: 3,
  grade-note: [Forum climbers say the first move off the mat often needs a burst of power #src("E26").],
  summary: [The problem starts with you sitting on the mat, hands on the start holds. The first move lifts your bottom off the floor. #cue[Turn sideways] and use the outside edge of your shoe instead of folding up square #src("E11").],
  figure: "sit-start.svg",
  caption: [(a) Square on, knees splayed, bottom away from the wall: the first pull is all arms. (b) Hips turned, outside edge on the foothold, bottom close to the wall.],
  how: [
    + Sit with your bottom close to the wall #src("E11", "E26"). Turn your hips about 90° to it and stand on the outside edge of the working foot #src("E11"). See #tref("edging").
    + If both footholds are straight below the start holds, a wide #tref("frog", body: [frog position], show-page: false) works too: bottom tucked close to the wall, chest dropped between your knees.
    + Lean back on the start holds if they allow it #src("E11"). See #tref("layback"). Rock back a little, then pull and stand in one movement. Or roll one knee onto the mat and push off it #src("E11").
    + Check your gym's rule on sit starts#ix("Gym rules") (@reading-method, step 1).
  ],
  when: [
    *Look for*
    - "sit" or "SDS" on the tag, or start holds just above the mat.
    - a low foothold to one side of the start holds. That is your outside-edge foot.

    *Symptoms*
    - You can hold the start but can't lift your bottom off the mat.
    - You sit square with your knees splayed and your bottom away from the wall, so the first pull is all arms #src("E11").
  ],
  errors: [
    - Bouncing off the mat on a problem whose rules want a controlled start.
  ],
  tall: [Sit starts feel cramped and strenuous if you are tall or stiff#ix("Tall climbers!sit starts") #src("E11"). @cons-tall has the sequence and a figure.],
  related: ("layback", "edging", "hip-turn", "frog", "body-tension", "pre-loading"),
  sources: ("E11", "E26"),
)

== V4–V5: roofs and dynamic slabs

#technique(
  key: "roof",
  name: "Roofs",
  aliases: ("roof climbing", "turning the lip"),
  category: "terrain",
  grade: 4,
  grade-note: [Roofs on low grades usually have big holds and big footholds. Once the footholds face down or sideways, your feet must hook to stay on. France's climbing federation teaches positions with the body horizontal at about V4 #src("F60", "F61").],
  summary: [On a roof you hang underneath it and the footholds face down, so feet that push swing off. Keep them on by pulling with your #cue[toes and heels]. To get over the #jt("lip") where the roof ends, #cue[hook a heel] over it #src("E7", "E15", "E13").],
  figure: "roof.svg",
  caption: [(a) Feet pushing on a down-facing hold swing off. (b) Arms straight and toes pulling on the hold: the feet stay on.],
  how: [
    + Hang on #tref("straight-arms", body: [straight arms], show-page: false) #src("E7") and keep your feet on by #tref("toe-pull", body: [pulling with your toes], show-page: false) #src("E7", "E20"). #tref("toe-hook") says how to hook them under a hold.
    + For a more solid foot, push one toe on top of a hold, hook the other toe behind it and squeeze the feet together #src("E7", "E15"). See #tref("bicycle"). Use heel hooks along edges and breaks as a third arm #src("E15", "E13"). See #tref("heel-hook").
    + Look to the sides for #tref("toe-hook", body: [toe hooks], show-page: false), and plan how each one comes out before you set it, so that your feet don't swing off #src("E15", "A12"). See #tref("cutting-loose").
    + On a big roof, consider going feet first. Hook a high toe, then swing your body round after it #src("E15", "A12"). A fall with your feet above your head can turn you upside down #src("G61"), so practise this low down first #src("A12") and decide beforehand whether you want a #jt("spotter") #src("G61"). See @cons-falling.
    + At the lip, heel-hook first, then roll over the heel. See #tref("top-out") #src("E13", "E7").
  ],
  when: [
    *Look for*
    - holds on the ceiling and footholds that face down or sideways.
    - holds with a hollow underside, and the backs of holds. They are toe-hook targets #src("E15").
    - a hold you can reach with both feet at once. Bicycle it.

    *Symptoms*
    - Your feet swing off as soon as you move a hand.
    - You hang with no feet at the lip and can't get over it.
  ],
  errors: [
    - Flat shoes. Downturned ones clamp better#ix("Climbing shoes!downturned"), and @shoes says what helps a toe hook #src("E15", "E5").
  ],
  tall: [Long legs reach foot hooks further from your hands, but keeping a long body flat costs more tension. Bring your feet in closer when you can.],
  related: ("toe-hook", "bicycle", "heel-hook", "knee-bar", "cutting-loose", "body-tension", "campus-move", "overhang", "top-out", "toe-pull", "straight-arms"),
  watch: (("Neil Gresham Climbing Masterclass - Crux Films", "Neil Greshams Masterclass - Roofs", "https://www.youtube.com/watch?v=LNdQDLokHRY"),),
  sources: ("E5", "E7", "E13", "E15", "E20", "A12"),
)

#technique(
  key: "dynamic-slab",
  name: "Dynamic slab",
  aliases: ("comp slab", "coordination slab"),
  category: "terrain",
  grade: 5,
  grade-note: [One gym's #jt("circuit", body: [circuits]) (colour groups of problems) move from teaching skills to testing them with dynamic moves around V4–V6 #src("E52"). In the 2019 World Cup#ix("World Cup!coordination moves") finals, 18% of problems had a #jt("coordination move") (at least three hand or foot placements within two seconds) #src("E6").],
  summary: [Modern gym slab often isn't slow balance: you jump or run between #tref("volume", body: [volumes], show-page: false) and catch holds and footholds while moving. The skill is planning where your body must end up, so you #cue[arrive balanced] #src("E5", "E27").],
  figure: "dynamic-slab.svg",
  caption: [Plan from the end. The climber starts on the left volume (dashed). The plan: land the right foot on the far volume (1). Catch the sloper (2). Then place the left foot (3).],
  how: [
    + Warm up hips, knees and ankles as well as fingers.#ix("Warm-up!for dynamic moves") You will fall a lot, from odd positions, so learn to fall first#ix("Falling!practice") (@cons-falling) #src("E5").
    + Read the end position first: where each foot and hand must be when the move stops. Plan the steps backwards from there #src("E27", "E5").
    + Decide how far from the wall you take off and land. Aim for an arc that ends balanced, not chest against the wall or overstretched #src("E5", "E27"). On a volume, land on the far side, hips over your feet. See #tref("volume") #src("E5").
    + Stay relaxed until the catch, then tense as you land #src("E5", "E27"). Think "pull my body into the end position", not "grab the hold" #src("E27").
    + Work long sequences one contact at a time: get the first right, then add the second #src("E5"). Where the fall is safe, try to ride out a foot slip instead of jumping off #src("E5").
  ],
  when: [
    *Look for*
    - big volumes with no holds, spaced further apart than you can step.
    - a single good hold or foothold on a far volume.
    - chalk and shoe marks in odd places. Others have been landing there #src("E5").

    *Symptoms*
    - You reach the target foot but topple backwards, because your hips arrived behind your feet, too far from the wall.
    - You can reach each position slowly but can't stop in it.
  ],
  errors: [
    - Launching at the wall instead of along it.
  ],
  related: ("run-and-jump", "foot-catch", "deadpoint", "latching", "comp-moves", "slab", "volume", "smearing"),
  watch: (("Gripped", "Top Olympian Tomoa Narasaki Teaches Coordination", "https://gripped.com/?p=40443"),),
  sources: ("E5", "E6", "E27", "E52"),
)
