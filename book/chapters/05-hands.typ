#import "../template.typ": *

= Hands and holds

This chapter covers what your hands do on each kind of hold and where each hold puts your body. That second part matters more, because at V3–V4 a fall from a decent hold often means your body was in the wrong place #src("C42", "C47").

Each grade marks where indoor problems start to demand the technique. No coaching scheme ties grips to V-grades; the UK's NICAS award teaches hold types at its third level #src("C44"). So the grades here are judgement calls. Each grade note says why.

The heavier you are, the more load your fingers carry.#ix("Body weight!load on the fingers") The force on your finger #jt("pulley", body: [pulleys]) (the bands that hold the tendons against the bone) rises with that load #src("C25", "C26"). The entries on the #jt("crimp") (a grip with the fingers sharply bent) say how to keep it down.

#category-table("hands")

== Every hold has a direction

#ix("Direction of pull")
Pull each hold opposite to the way its gripping surface faces. Chapter 1 explains why. Chapter 2 has a table of where your body goes for each hold.

German school climbing lessons turn this into a drill:#ix("Drills!taping hold directions") students mark each hold's best pulling direction with a strip of tape, then climb so the forearm lies along the tape #src("C42").

The same lessons name two warning signs of a wrong direction:

- *You slip off suddenly* from a hold that felt fine. Move your body until you can lean into the hold. Get more of your hand on it.
- *Your forearms #jt("pump") on easy holds.* (Pump is the hard, tired, swollen feeling in the forearm.) You are squeezing to make up for a bad angle,#ix("Pump!from a wrong pull direction") so move your body instead and grip only as hard as you need.

A straight arm is a quick check, because an arm that hangs straight points along the pull.

How well a hold works changes as you move. A sloper that holds while your hips are low rolls off as they rise. An undercling gets better as you climb above it #src("C2", "C4"). So ask where your hips will be when you need each hold. Where they are when you first touch it matters less.

== Positive and negative holds

#ix("Positive hold") #ix("Negative hold")
A #jt("positive hold") has a gripping surface that faces up or tilts back into the wall. That tilt is called an #jt("incut"). Your fingers hook behind it and lock on by shape. A #jt("negative hold") slopes down and away from the wall, so part of your pull runs along the surface and #jt("friction") (the grip of skin on the surface) has to keep you on #src("C42").

#fig("hands-hold-angle.svg", caption-width: 125mm, caption: [A fingertip on three edges, pulled straight down. The incut locks it. The flat edge needs curl and friction. On the sloping edge, part of the pull drags the finger off.])

Lab tests show how fast small sloping holds get worse#ix("Studies!edge depth and slope")#ix("Edge!depth and slope") #src("C29"). Eight strong climbers pulled as hard as they could on #jt("edge", body: [edges]) (narrow ledges) 1–4 cm deep, tilted from flat to 40°.

- On 3–4 cm edges, a 30° slope made no real difference. Only 40° cut their force.
- On 1–2 cm edges, their force dropped once the slope passed 20°.
- They chose a half crimp on the 1–2 cm edges and an open hand on the deeper ones.

So a small hold that slopes is worse than a small flat one or a big sloping one.

#ix("Dual texture") The same hold can be positive or negative, depending on how the #jt("setter") (the person who designs the problems) bolted it on. Some modern holds and #jt("volume", body: [volumes]) (big hollow shapes bolted to the wall) have two finishes: a grippy texture marks where you should hold, and a smooth finish marks where you shouldn't. This is called #jt("dual texture") #src("C49"). Read the grippy patch as an instruction, because the smooth part can turn a big, easy hold into one that needs precise movement #src("C50").

== Contact strength and grip endurance

#ix("Contact strength")
Two different things can run out in your fingers. #jt("contact strength", body: [Contact strength]) is how fast you can squeeze hard at the moment you grab a hold. You need it to slap a rounded hold or catch a small edge on the move. If you touch the hold but can't stay on it, this is what failed. Grip endurance#ix("Grip endurance", main: true) is how long you can keep gripping. If you fall on the last moves with pumped forearms, this is what failed.

Technique cuts both demands, because a hold loaded in its own direction needs less squeeze #src("C42") and a lighter grip costs less. A German teaching drill trains this: load a hold, then ease off until you are only just holding on#ix("Drills!gripping lightly") #src("C42").

#figure(image("../figures/hand-atlas.svg"), caption: [Hand positions at a glance. Each grip has its own entry in this chapter.], kind: image, supplement: [Figure])

== V0–V1: big holds and~the~first~directions

#technique(
  key: "jug",
  name: "Jug",
  aliases: ("bucket", "handle"),
  category: "hands",
  grade: 0,
  grade-note: [You use jugs from your first session. When you pause on one on a steep wall, hang on a straight arm, and on a vertical wall stand tall (this book's suggestion). Resting that way before the hard moves starts to matter around V2–V3.],
  summary: [A jug is a big, deep hold you can wrap your whole hand around #src("C34"). The skill is to hang on it cheaply.],
  figure: "jug.svg",
  caption: [(a) Bent arms: your biceps and shoulder muscles work to hold you there. (b) One straight arm holds you while the other hand shakes out.],
  how: [
    + Put your fingers into the deepest part, up to the second joint.
    + On a big #jt("incut") jug, wrap your thumb round the front. It takes load off the fingers #src("C1").
    + Grip only as hard as you need #src("C35").
    + On a steep wall, hang on a straight arm, so your biceps can rest #src("C41").
    + Hang below the jug, or on the side away from the way it faces.
    + To rest, drop the other arm below your waist and shake it loose. Then swap hands.
  ],
  when: [
    *Look for*
    - big chalky holds between hard sections. On steep problems, choose your rest jugs before you start.#ix("Resting on the wall")
    - which way each jug faces. One that faces sideways is a #tref("sidepull", body: [sidepull]). One that faces down is an #tref("undercling", body: [undercling]).

    *Symptoms*
    - Your forearms #jt("pump") on easy holds. German school lessons blame squeezing too hard or hanging on bent arms #src("C42").
    - You swing out sideways when the other hand lets go. The jug faces sideways and your body is in line with it.
  ],
  errors: [
    - Pulling up on bent arms instead of pushing with the legs #src("C41"). Straighten the arm and stand up.
    - Skipping the rest. Shake out on every good jug, even for a few seconds.
  ],
  tall: [Long arms let you hang low, but on a steep wall that drops your hips far below the jug. Put your feet higher to keep weight on them.],
  related: ("straight-arms", "sidepull", "undercling", "regrip"),
  sources: ("C1", "C34", "C35", "C41", "C42"),
)

#technique(
  key: "sidepull",
  name: "Sidepull",
  aliases: ("layaway", "side pull"),
  category: "hands",
  grade: 1,
  grade-note: [Directional holds appear on easy problems. Movement gyms list them first among five essential techniques #src("C40"). From V2, most problems need them.],
  summary: [A sidepull is a hold that faces sideways, away from your body. You pull it towards your middle and lean your body away from it #src("C34", "C36").],
  figure: "sidepull.svg",
  caption: [(a) Under a left-hand sidepull, the body swings open. (b) Body to the right of it, leaning away. The left foot pushes left.],
  how: [
    + Read which way the hold faces. A hold on your left whose edge faces left is a left-hand~sidepull.
    + Grip it thumb up, fingers pointing into the edge. Pull towards your middle.
    + Lean away. Move your hips and shoulders right until your left arm is straight #src("C34", "C36").
    + Push your feet the other way. Your left foot pushes left against its foothold #src("C36").
    + Turn side-on to reach. Later, a #tref("backstep", body: [backstep]) or partial #tref("drop-knee", body: [drop knee]) on the reaching side adds height #src("C36").
    + If there is a spot for your thumb on the back of the hold, squeeze it into a #tref("pinch", body: [pinch]) #src("C36").
  ],
  when: [
    *Look for*
    - vertical edges and #jt("flake", body: [flakes]) (thin blades standing off the wall) that face away from you.
    - a sidepull out to the side. It often gives more reach than a flat hold #src("C36").

    *Symptoms*
    - You swing open like a door when the other hand lets go. Your body is under the hold, or no foot pushes back. See #tref("barn-door").
    - Your fingers peel outward. You are pulling down on it as if it were a jug.
  ],
  errors: [
    - Feet in the wrong place, so nothing pushes against the pull. Put a foot under the hold.
  ],
  small: [Burying your hand in a deep sidepull or #tref("undercling") feels secure but shortens your reach. When you need distance, slide your hand out towards the edge, as far as it still holds, before you move off it #src("H3").],
  related: ("gaston", "layback", "barn-door", "backstep", "drop-knee", "pinch"),
  watch: (("Climbing Tech Tips", "Climbing Movement: 21. Side Pull Holds", "https://www.youtube.com/watch?v=kgDU3WSXowM"),),
  sources: ("C34", "C36", "C40", "C41", "H3"),
)

== V2: edges, open hands, pressing~and~pulling~up

#technique(
  key: "half-crimp",
  name: "Half crimp",
  aliases: ("half-crimp", "open crimp", "halb aufgestellt"),
  category: "hands",
  grade: 2,
  grade-note: [Edges small enough to crimp turn up from about V2 (judgement). They keep shrinking as you near V5 #src("C48"). Make the half crimp your default on these edges from the start, so you don't fall into the habit of full crimping (this book's suggestion).],
  summary: [Your fingertips sit on a small #jt("edge") with the middle joints bent to about 90°. The end joints stay straight and the thumb stays free. It suits most edges #src("C1", "C21").],
  figure: "half-crimp.svg",
  caption: [(a) Half crimp: the middle joint bends about 90° and the end joint stays straight. (b) Full crimp for comparison: the end joint bends back.],
  how: [
    + Put your fingertips on the edge. Bend the middle joints to about 85–90° #src("C25").
    + Keep the end joints straight or slightly bent. Never let them bend backwards #src("C9").
    + Put the little finger on if it reaches. It is shorter, so it usually stays straight #src("C1").
    + Rest your thumb beside the index finger, or press it on a bump on the side of the hold #src("C1").
    + Pull down and slightly in, elbow below the hand. Place your hips by the hold's direction.
    + If the hand is being forced open, re-grip or let go. Don't fight it #src("C15", "C20").
  ],
  when: [
    *Look for*
    - flat or #jt("incut") edges 1–2 cm deep #src("C29").
    - small edges on #jt("volume", body: [volumes]).

    *Symptoms*
    - Your fingertips roll off the front of the edge. Your body is too high above it, or the edge slopes.
    - Your hand peels open on every try. Move your body or add #tref("thumb-catch", body: [your thumb]). If it still opens, leave the move for now, because a #tref("full-crimp", body: [full crimp]) is for the tiny edges of about V5 (judgement).
    - You feel a sharp pain at the base of a finger. Stop for the day.
  ],
  errors: [
    - Sliding into a full crimp out of habit. Beginners overuse it because it feels secure #src("C9").
    - Trying the same hard crimp move again and again. Hooper's Beta#ix("Hooper, Jason") counts this as an injury risk#ix("Injuries!pulley") #src("C15").
  ],
  related: ("open-hand", "full-crimp", "thumb-catch", "regrip"),
  watch: (("Adam Ondra", "Crimp Grips Tutorial: Crimp Like a Pro Climber", "https://www.youtube.com/watch?v=o59qz4orcWs"),),
  sources: ("C1", "C9", "C15", "C20", "C21", "C25", "C26", "C29", "C48"),
)

#technique(
  key: "open-hand",
  name: "Open hand",
  aliases: ("drag", "open grip", "three-finger drag", "chisel", "offene Hand"),
  category: "hands",
  grade: 2,
  grade-note: [It matters from V2, when edges get rounded. In Lattice's#ix("Lattice Training") tests at V1–V4, climbers added 22.5 kg in open hand and 14.5 kg in half crimp.#ix("Finger strength!open hand and half crimp") They were different climbers, so this only hints at a natural strength #src("C21").],
  summary: [You hang your finger pads over the hold with the joints only slightly bent. Skin friction and the long finger tendons do the work. It is the cheapest grip and puts far less load on your finger #jt("pulley", body: [pulleys]) than a crimp #src("C1", "C14").],
  figure: "open-hand.svg",
  caption: [(a) Drag on a rounded edge: the pad drapes over and the middle joint bends about 40°. (b) Three-finger drag seen from behind, with the little finger off.],
  how: [
    + Lay your finger pads over the #jt("lip") (the front of the hold). The end joint hooks over it #src("C1").
    + Keep the middle joint only slightly bent. Measured open-hand grips average about 40° there #src("C28").
    + Choose four fingers or three. In a three-finger drag, the little finger comes off #src("C1", "C10").
    + Keep your wrist slightly bent back.#ix("Wrists") It gives your finger muscles better leverage #src("C9").
    + Hang below the hold on a straight arm. The pull then runs down through the pads.
    + Get as much skin#ix("Skin") on the hold as you can #src("C35").
  ],
  when: [
    *Look for*
    - rounded edges and #jt("rail", body: [rails]) (long horizontal edges) where bending the fingers hooks nothing.
    - edges 3 cm deep or more #src("C29").
    - long easy sections where you want to save energy #src("C1").

    *Symptoms*
    - Your fingers peel off as your hips rise. You have moved above the line of pull.
    - The open hand slides on a 1–2 cm edge. Switch to a #tref("half-crimp", body: [half crimp]) #src("C29").
  ],
  errors: [
    - Starting in a #jt("crimp") and letting it be forced open under full load. Hooper's Beta#ix("Hooper, Jason") links this to pulley tears#ix("Injuries!pulley") #src("C15"). Choose the open hand before you load the hold.
    - Leaving the little finger off when it could help. It matters more in better climbers #src("C30").
  ],
  related: ("half-crimp", "sloper", "pocket"),
  watch: (("Lattice Training", "A Deep Dive into EVERY Climbing Grip Type", "https://www.youtube.com/watch?v=HBa-ilEp4Os"),),
  sources: ("C1", "C9", "C10", "C14", "C15", "C21", "C28", "C29", "C30", "C35"),
)

#technique(
  key: "undercling",
  name: "Undercling",
  aliases: ("undercut"),
  category: "hands",
  grade: 2,
  grade-note: [Underclings appear early. Using them well means getting your feet high, which most V2 climbers resist #src("C4").],
  summary: [An undercling faces down. You grip it palm up and pull up and out. Your feet do the work: they push you up until the hold sits at your waist #src("C4", "C34").],
  figure: "undercling.svg",
  caption: [(a) With the hold above the head and the feet low, the arms bend and you tip backwards. (b) With the feet up, the hold sits at the waist. The arm is straight and the free hand reaches.],
  how: [
    + Build your feet up first. Then reach for the hold and bring it close to your body #src("C52").
    + Grip palm up with an open hand, not a #jt("crimp"). Get as much hand behind it as you can. Point your thumb out #src("C4").
    + Get your waist level with the hold. The higher you are, the easier it gets #src("C4", "C34").
    + Keep the arm straight, so your biceps can rest #src("C4", "C36").
    + Lean back and push your feet into the wall. Stand up into the hold #src("C4").
    + To reach, stand up on one foot and turn that hip to the wall #src("C4").
  ],
  when: [
    *Look for*
    - holds whose edge faces down, such as #jt("flake", body: [flakes]). The underside of a #jt("volume") works too.
    - an undercling at chest or waist height with the next hold far above. It lets you reach a long way #src("C34").

    *Symptoms*
    - Your biceps burn. Your arm is bent #src("C4").
    - You feel you are tipping backwards. The hold is too high for your body. Step your feet up #src("C4", "C52").
    - Your feet skate. They aren't pushing hard enough into the wall #src("C4").
  ],
  errors: [
    - Pulling with the arms instead of standing up with the legs #src("C4").
    - Bending the wrist hard towards the little finger. Schweizer#ix("Schweizer, Andreas") links this to fractures of a small wrist bone#ix("Injuries!wrist") #src("C25").
  ],
  tall: [Your waist sits high above your feet, so the hold reaches waist height with your feet lower than a shorter climber's. Stop raising your feet once it does, because higher still folds your long legs against your chest (judgement).],
  related: ("gaston", "sidepull", "high-step", "straight-arms"),
  sources: ("C4", "C25", "C34", "C36", "C52"),
)

#technique(
  key: "palming",
  name: "Palming",
  aliases: ("palm press", "pressing", "support"),
  category: "hands",
  grade: 2,
  grade-note: [It helps on easy slabs and volume problems from V2. In corners and on steep volumes it becomes necessary around V4.],
  summary: [You press an open palm against the wall or a #jt("volume") instead of gripping. The push and skin friction hold you. It is the hand version of #tref("smearing") #src("C41").],
  figure: "palming.svg",
  caption: [The right palm presses down and right on a volume. That frees the right foot to step up.],
  how: [
    + Find a surface you can push into: a volume face, the wall beside you or a dimple.
    + Chalk your whole hand. Put it flat with the fingers spread #src("C11").
    + Press through the heel of the hand #src("C56").
    + Point the fingers so your wrist stays in line with the push. For a push down, point them sideways.
    + Keep your elbow behind your hand. Straighten the arm as you move.
    + Push away from where you are going. To move up and left, press down and right #src("C11").
    + Use the push to take weight off a foot. Then move that foot #src("C37", "C56").
  ],
  when: [
    *Look for*
    - big volumes with flat faces near your hips #src("C11").
    - a blank wall or corner beside you and no handhold. See #tref("stemming").
    - a good foothold with no handhold above it #src("C37").

    *Symptoms*
    - Your palm skids. You are pushing along the surface instead of into it. Press more squarely.
    - A foot won't come up because both hands are busy. Add a palm press so it can.
  ],
  errors: [
    - Pressing with the fingertips instead of the whole palm.
  ],
  related: ("smearing", "stemming", "volume", "mantle", "thumb-catch"),
  sources: ("C5", "C11", "C37", "C41", "C56"),
)

#technique(
  key: "mantle",
  name: "Mantle",
  aliases: ("mantel", "mantelshelf", "press-out", "volume mantle"),
  category: "hands",
  grade: 2,
  grade-note: [Gyms with top-out walls can ask for an easy one from V0, and it starts to matter at V2 (judgement). The heel hook in step 2 comes at V3, so try it low on the wall first (this book's suggestion). Hard mantles, with a poor high foot, a rounded top or a volume in the middle of a problem, are a V5–V6 skill: a coaching clinic at that level lists them #src("C46").],
  summary: [A mantle turns a pull on a ledge into a push down on it. Then you stand up on it. It gets you over a #jt("lip") (the edge where the wall ends) and onto a flat top #src("C39"). For the whole finish of a problem, see #tref("top-out").],
  figure: "mantle.svg",
  caption: [(1) Pull, with the right foot high. (2) Flip the right hand flat with the elbow up. Press. (3) Straighten both arms. Step onto the top without a knee.],
  how: [
    + Chalk your palms first.#ix("Chalk") A mantle needs palm contact #src("C5").
    + Get a foot high: "Your feet lead your hips" #src("C5"). Aim for a foothold high enough that your waist reaches your hands when you stand #src("C6"). On a steep or rounded top, #tref("heel-hook", body: [heel-hook]) the lip instead #src("C5", "C6").
    + Pull your shoulders up to the lip and stand on the high foot #src("C6").
    + As your shoulders pass the lip, flip one hand flat onto the top. Point the fingers towards the other hand and the elbow up #src("C6"). This gives the most push at the start #src("C39").
    + Press down until that arm is straight. Flip the second hand and press with both #src("C6").
    + Bring a foot onto the top. Lean forward over it and stand up #src("C6").
    + Do steps 3–6 as one motion. Don't stop at the tipping point #src("C5", "C6").
  ],
  parts: (
    (
      name: [Volume mantle],
      how: [
        Indoors, most mid-problem mantles are onto #jt("volume", body: [volumes]). You usually can't get on top and rest there, so you press, rock over and keep moving.

        + Get a foot high on the side of the volume, or #tref("heel-hook", body: [heel-hook]) its edge #src("C5", "C39").
        + Pull on the volume's edge until you are balanced. Only then flip a hand onto the top #src("C39").
        + Press the heel of your palm on the top, away from the way you are going #src("C11").
        + Move your hips over the high foot and stand up on it, as in a #tref("rockover", body: [rockover]) #src("C6").
        + Keep pressing with the palm while the other hand goes to the next hold.
      ],
      figure: "volume-mantle.svg",
      caption: [(a) Pull on the volume's edge with the right foot high. (b) Press the top with the left palm, rock over and reach.],
    ),
  ),
  when: [
    *Look for*
    - a flat top or ledge with no holds beyond it.
    - a ledge mid-wall with nothing above within reach.
    - a big chalked volume top, flat or gently sloping, at chest height with no hold you can reach above it.
    - footholds set on the volume itself.
    - a grippy patch on top of a #jt("dual texture") volume. The #jt("setter") wants your palm there #src("C49").

    *Symptoms*
    - You are stuck at chest height with bent elbows. You have no high foot #src("C39").
    - You fall backwards as you move the second hand. You moved it before your weight was over the first hand #src("C39").
    - Your foot shoots off as you rock over. You put a knee on the top #src("C5").
    - Your palm slides on a volume. You are pressing with the fingers, or pushing along the face instead of into it.
  ],
  errors: [
    - Putting a knee on the top. A knee has little grip. It also turns your foot the wrong way #src("C5").
    - Hesitating halfway. Commit, or climb down and try again #src("C39").
    - Always mantling on your favourite side. Practise both hands, 2–3 grades below your limit #src("C6").
    - Pulling on a sloping volume edge that you should press.
  ],
  tall: [You reach the lip and a high foot easily. Folding a long body over that foot is the hard part.#ix("Tall climbers!mantles") Get weight onto the foot early, so your arms don't press your whole weight #src("C5").],
  related: ("top-out", "rockover", "high-step", "palming", "volume"),
  watch: (("Friction Labs", "The Art of the Mantle — Chris Schulte’s Guide to Topping Out in Fontainebleau", "https://www.youtube.com/watch?v=oKrATkvFOck"),),
  sources: ("C5", "C6", "C11", "C39", "C46", "C49"),
)

== V3: slopers, pinches and gastons

// The strip's own page break would strand the head above, so it is switched off here.
#[
  #show pagebreak: none
  #filmstrip("filmstrip-sloper.svg", [Re-gripping a sloper], [Watch the palm: it comes onto the hold only after the finger pads have dragged over the top. Then the thumb finds a spot underneath and the wrist drops below the hold.])
]

#technique(
  key: "sloper",
  name: "Sloper",
  aliases: ("sloping hold"),
  category: "hands",
  grade: 3,
  grade-note: [Slopers stop many climbers between V3 and V4. Forum advice points to body position and footwork #src("C47").],
  summary: [A sloper is a rounded hold with no edge to hook, so #jt("friction") holds you on. It works only while your body hangs below the hold #src("C3", "C34").],
  figure: "sloper.svg",
  caption: [(a) Both feet high push the hips out. The hand rolls off. (b) The hips hang low under the hold. One foot stays low and the arm is straight. (c) Palm and finger pads drape over the hold, with the wrist below it.],
  how: [
    + From the ground, find the best part of the hold for where your body will be #src("C2").
    + On a big sloper, spread your fingers and press with palm and fingertips. On a flat ledge, keep the fingers together #src("C3").
    + Drag the finger pads over the hold. Drag the palm over it too if you can #src("C2").
    + Look for a thumb spot below or beside the hold #src("C2").
    + Keep your wrist stiff #src("C2").
    + Hang low on a straight arm. Keep your hips under the hold #src("C3", "C11").
    + Keep one foot low. Both feet high push your hips out and off the hold #src("C2").
    + Move slowly. Keep your hips steady between the handholds #src("C2", "C11").
  ],
  when: [
    *Look for*
    - rounded holds, ledges with no front edge to hook and flat-topped #jt("volume", body: [volumes]).
    - where your hips will be when you need the hold. The more it slopes, the more they must be under it #src("C2", "C29").
    - a sloper angled to one side. Lean the other way #src("C3").

    *Symptoms*
    - Your hand slides off as your hips rise or as you bring both feet up #src("C2", "C3").
    - Your hips swing out when you reach. Then the hand rolls off #src("C2").
    - Slopers that held last week fail on a warm, humid day#ix("Conditions (temperature, humidity)") #src("C3").
  ],
  errors: [
    - Twisting your body into the hold. Gresham#ix("Gresham, Neil") says keep the hips square #src("C2").
    - Squeezing with the forearm instead of using your shoulders, back and core #src("C3").
    - Slapping the same sloper over and over. It strains the wrist#ix("Injuries!wrist") #src("C2").
    - Pinning yourself flat to the wall. Pull the hips in #src("C3"), but hugging the wall can stop you turning when a hand lets go #src("C19"). Low and under the hold matters more than tight.
  ],
  related: ("open-hand", "palming", "straight-arms", "body-tension", "heel-hook"),
  watch: (("Lattice Training", "Slopers: Technique, Training, and Cheat Codes", "https://www.youtube.com/watch?v=KjE7R-tmYGE"), ("Send Edition", "4 Sloper Mistakes Beginner Boulderers Make", "https://www.youtube.com/watch?v=lxQtAHNiqFs")),
  sources: ("C2", "C3", "C11", "C19", "C29", "C34", "C47"),
)

#technique(
  key: "pinch",
  name: "Pinch",
  aliases: ("pinch grip"),
  category: "hands",
  grade: 3,
  grade-note: [Wide pinches appear around V2–V3. Narrow pinches matter from V4–V5.],
  summary: [You squeeze a hold between your thumb and fingers on two opposite faces #src("C34", "C43"). Most pinches are vertical. A horizontal one is easier to use as a crimp or sloper #src("C34").],
  figure: "pinch.svg",
  caption: [Seen from above, with the wall at the top. The thumb and fingers squeeze across each hold.],
  how: [
    + Find two opposite faces. Put your thumb on one and your fingers on the other, so you squeeze straight across.
    + On a narrow pinch, squeeze between the thumb pad and the side of the index finger #src("C35"). Bend the fingers as in a #tref("half-crimp", body: [half crimp]) #src("C38").
    + On a wide pinch, lay your fingers flat and open #src("C38").
    + On a #jt("volume") edge, put the thumb on one face and the fingers on the other #src("C11").
    + Put your thumb where the chalk marks show #src("C38").
    + Place your body by the pinch's direction. Lean off it, twist, or squeeze two pinches together #src("C38").
    + Grip as lightly as you can. Squeezing too hard makes you stiff #src("C38").
  ],
  when: [
    *Look for*
    - vertical ribs, blocks and volume edges with two usable sides.
    - a #tref("sidepull", body: [sidepull]) with a thumb spot on the back. Pinching it pulls you in #src("C36").

    *Symptoms*
    - The hold squirts out sideways. You aren't squeezing straight across.
    - Your thumb slips because it sits on a smooth face. Find a texture patch or a dimple.
    - You swing out because your body is on the wrong side for the pinch's direction.
  ],
  errors: [
    - Squeezing harder instead of moving your body into line #src("C42").
    - Taking a narrow pinch on a hold that offers a wide one. Compared with a jug, climbers' pull dropped 6–19% on a wide pinch but 31–46% on a narrow one #src("C31").
  ],
  tall: [Big hands help on wide pinches#ix("Hand size") #src("C37"), less so on narrow ones (judgement).],
  small: [If your thumb can't press back on a wide pinch, you may be able to hold it like an edge #src("C37"), or pull it as a #tref("sidepull", body: [sidepull]), leaning away from it (judgement).],
  related: ("sidepull", "compression", "wrap", "thumb-catch"),
  watch: (("Lattice Training", "A Deep Dive into EVERY Climbing Grip Type", "https://www.youtube.com/watch?v=HBa-ilEp4Os&t=1317s"),),
  sources: ("C11", "C31", "C34", "C35", "C36", "C37", "C38", "C42", "C43"),
)

#technique(
  key: "wrap",
  name: "Wrapping",
  aliases: ("wrap", "guppy", "meat-hook"),
  category: "hands",
  grade: 3,
  grade-note: [Arêtes and big round holds become common on gym problems around V3.],
  summary: [You wrap your whole hand, palm included, round a rounded feature, such as an #tref("arete", body: [arête]), the ridge of a #jt("volume") or a big round hold. Palm and thumb press against the fingers, so skin grips over a large area.],
  figure: "wrap.svg",
  caption: [An arête seen at an angle. Palm and thumb press on one face. The fingers wrap round the edge. Both squeeze towards it.],
  how: [
    + Put your palm on the near face. Wrap your fingers round onto the far face #src("C11", "C34").
    + On horns (holds that stick out like a spike) and edges, press with the heel of the hand to spare the fingers #src("C37").
    + On a round hold, wrap round it rather than gripping straight on. Turn the wrist a little left or right until it feels secure #src("C3").
    + On a peaked volume, hook your hand over the peak. Put the palm on one side and the fingers on the other #src("C11").
    + Squeeze towards the edge. Push a foot or the other hand the opposite way #src("C11").
  ],
  when: [
    *Look for*
    - arêtes on gym features.
    - peaked volumes and big round holds #src("C11").
    - a guppy: a hold you grip sideways, mainly across the palm #src("C34").

    *Symptoms*
    - Your hand slides round the feature. You are pulling across it instead of along it, or nothing pushes back.
  ],
  errors: [
    - Using only the fingertips where the palm should touch.
    - Pulling straight out from the wall on an arête instead of squeezing.
  ],
  related: ("pinch", "compression", "arete", "volume"),
  watch: (("Lattice Training", "A Deep Dive into EVERY Climbing Grip Type", "https://www.youtube.com/watch?v=HBa-ilEp4Os&t=2163s"),),
  sources: ("C3", "C11", "C34", "C37"),
)

#technique(
  key: "gaston",
  name: "Gaston",
  aliases: ("reverse sidepull",),
  category: "hands",
  grade: 3,
  grade-note: [It takes a lot of shoulder power #src("C34"). Many climbers avoid it until problems force it, which starts around V3.],
  summary: [A gaston faces towards your middle, usually in front of your face or chest. You grip it thumb down and elbow out. Then you push it away from you, like prising open lift doors #src("C41", "C57").],
  figure: "gaston.svg",
  caption: [The same left-facing hold. (a) With the body to its right, it is a left-hand~sidepull. (b) With the body to its left, it is a right-hand gaston, thumb down and elbow out.],
  how: [
    + Put your fingers on the face of the hold that faces your middle. Turn your thumb down and your elbow out #src("C41", "C57").
    + Push the hold away from your middle. Your shoulder does most of the work #src("C34").
    + Keep your elbow up, about level with your hand.
    + Keep the hold close to your shoulder. A gaston at full reach is weak.
    + Your body sits on the side the hold faces. The hold pushes your hand towards your middle, so your feet must push you back. Press the opposite foot outward, or #tref("flag", body: [flag]) #src("B14").
  ],
  when: [
    *Look for*
    - vertical edges in front of your face or chest that face towards your middle.
    - a hold that is a sidepull for one hand. For the other hand, it is a gaston.

    *Symptoms*
    - Your elbow drops and the hand peels off.
    - Your shoulder burns fast. The hold is too far from your body.
    - You fall towards the hold's side when the other hand lets go. No foot pushes back.
  ],
  errors: [
    - Turning the thumb up and pulling it like a sidepull.
    - Reaching for a gaston at arm's length. Step your feet up first.
  ],
  related: ("sidepull", "undercling", "flag", "opposition"),
  watch: (("OnBouldering", "Climbing technique - Gaston", "https://www.youtube.com/watch?v=W3wk1w5IPso"),),
  sources: ("C34", "C41", "C57", "B14"),
)

#technique(
  key: "regrip",
  name: "Re-gripping and adjusting",
  aliases: ("grip switching", "readjusting", "finding the sweet spot"),
  category: "hands",
  grade: 3,
  grade-note: [Around V3–V4, problems start to have holds you catch one way and use another.],
  summary: [You change your grip on a hold after you first grab it. You might walk your fingers to the best spot, adjust as your body moves or make room for the other hand.],
  figure: "regrip.svg",
  caption: [(1) Catch the hold where you can, aiming at the screw hole. (2) Walk the fingers into the incut and settle into a half crimp.],
  how: [
    + From the ground, plan how you will catch the hold and how you will use it. The best place to catch it is often not the best place to pull #src("C2").
    + #ix("Sweet spot") Find the #jt("sweet spot") (the best part of the hold). Chalk marks, #jt("incut", body: [incuts]), ridges and thumb dimples show it #src("C11", "C38"). On a #jt("dual texture") hold, aim for the grippy patch #src("C49").
    + Aim at a small mark, such as a screw hole: "aim small, miss small" #src("C18").
    + Aim with your head. Put your nose where your balanced body needs to be. A fumbled hand then has time to correct #src("C18").
    + Move your fingers one at a time while your weight is on your feet or the other hand.
    + On a long run of edges, switch between #tref("half-crimp") and #tref("open-hand"). The change rests your fingers #src("C51").
    + To make room for a #tref("matching", body: [match]), take the hold with fewer fingers, on one side, or pinch it #src("C58"). Swap fingers across one at a time.
  ],
  when: [
    *Look for*
    - big holds and #jt("volume", body: [volumes]) with one good spot.
    - holds you must catch on the move.
    - a single small hold that both hands need.

    *Symptoms*
    - You slip off a hold that works for others. You used the wrong spot or pulled the wrong way #src("C42").
    - You fiddle on every hold. You aren't aiming before you move #src("C18").
    - Your fingers creep open on a hard move. Re-grip with control or let go #src("C15").
  ],
  errors: [
    - Fiddling with your grip while hanging on a bent arm. Straighten it first.
    - Forgetting the lower hand. Climbers watch the reaching hand and lose the holding one #src("C42").
  ],
  related: ("matching", "half-crimp", "thumb-catch", "sloper"),
  watch: (("Hooper’s Beta","A Radical Shift in How You Take Holds – Coaching w/ Dan #6", "https://www.youtube.com/watch?v=_E4G3tv55Cw"),),
  sources: ("C2", "C11", "C15", "C18", "C38", "C42", "C49", "C51", "C58"),
)

== V4: pockets and thumbs

#technique(
  key: "pocket",
  name: "Pocket",
  aliases: ("hole", "mono", "two-finger pocket"),
  category: "hands",
  grade: 4,
  grade-note: [Gyms set fewer pockets than outdoor limestone has, so indoors they matter around V4–V5. Injuries to the #jt("lumbrical", body: [lumbricals]) (small muscles in the palm) are rising among climbers#ix("Injuries!lumbrical") #src("C33").],
  summary: [A pocket is a hole for one or more fingers #src("C34"). A one-finger pocket is a mono. The risk lies in the fingers you leave out, because curling them hard into the palm strains the small muscles between the fingers #src("C12", "C16").],
  figure: "pocket.svg",
  caption: [Two-finger pocket, middle and ring fingers in the hole. (a) Little finger kept parallel: safer. (b) Little finger curled into the palm: stronger, but it shears the muscle between it and the ring finger.],
  how: [
    + Count the fingers that fit. Feel the depth: to the first joint or the second.
    + Three fingers: put them together in the hole #src("C42").
    + Two fingers: use middle and ring, or index and middle #src("C42"). Choose by feel #src("C37").
    + One finger: use the middle finger #src("C35").
    + Keep the fingers outside the pocket loose and roughly parallel to the pocket fingers. Don't curl them hard into the palm #src("C12", "C16").
    + Use an open hand or a #jt("crimp") inside, depending on depth. Don't crimp hard over a sharp rim #src("C35").
    + Load the pocket smoothly. Watch your feet: a foot slip jolts the fingers #src("C16").
  ],
  when: [
    *Look for*
    - holes in holds and #jt("volume", body: [volumes]). Some holds have two holes.
    - how deep the pocket is before you trust one finger to it.

    *Symptoms*
    - You feel a sharp pain in the palm as you pull a two-finger pocket. That is the #jt("lumbrical") warning. Stop.
    - Only part of a finger fits. Use fewer fingers, seated deeper.
  ],
  errors: [
    - Curling the little finger tight in a middle–ring pocket. The ring and little fingers then pull the muscle between them in opposite directions #src("C12", "C16"). In a lab test on donated hands, it tore at about 11 kg on average #src("C32").
    - Pulling hard on pockets your fingers haven't trained for #src("C17").
  ],
  tall: [Large fingers fit fewer fingers into a pocket#ix("Hand size") #src("C37"). That pushes you into two-finger pockets and monos. Keep the outside fingers parallel there.],
  related: ("open-hand", "half-crimp", "regrip"),
  watch: (("Hooper’s Beta","What No One Tells You About Climbing On Pockets (Pocket Injury)", "https://www.youtube.com/watch?v=3dd_STU3ps8"),),
  sources: ("C12", "C16", "C17", "C25", "C32", "C33", "C34", "C35", "C37", "C42"),
)

#technique(
  key: "thumb-catch",
  name: "Using the thumb",
  aliases: ("thumb catch", "thumb press", "thumb wrap", "thumbercling", "inverse crimp"),
  category: "hands",
  grade: 4,
  grade-note: [Look for the thumb spot from your first crimps (this book's suggestion). Climbers often miss the one that goes with an edge #src("C1"). It matters most on rounded holds on steep problems #src("C2"), which mostly means V4–V5.],
  summary: [You use your thumb as a separate contact that hooks a dimple, presses a face or pinches an edge. That can turn a hold that is too small or too sloping into a usable one #src("C7").],
  figure: "thumb-catch.svg",
  caption: [(a) Fingers over a rounded edge, thumb in a dimple below. (b) Thumb pad pressing up on a volume face, fingers over the ridge.],
  how: [
    + Feel the hold with your thumb for bumps, dips or a second face. Give up a little of the main hold if that gets the thumb on #src("C7").
    + *Thumb catch:* press the thumb into a dimple below or beside the fingers.
    + *Thumb press:* lay the thumb pad flat on a face and push. It takes load off the fingers #src("C7").
    + *On a #tref("sloper", body: [sloper]):* try the thumb below the hold and to one side #src("C2").
    + *On a #jt("volume") edge:* put the thumb on one face and the fingers on the other #src("C11").
    + *Thumb wrap:* on a big jug or a #jt("rail"), wrap the thumb round the front #src("C1").
    + *Thumbercling:* on an overhead hold that faces down, press up with the thumb pad. Keep the wrist and fingers straight #src("C7").
  ],
  when: [
    *Look for*
    - dimples, ridges or a second face just below the main hold.
    - long, tiring sequences. Pressing with the thumb rests the fingers #src("C7").

    *Symptoms*
    - Your fingers slide forward off a hold although your body is below it. A thumb under the hold stops the hand rolling out.
  ],
  errors: [
    - Never looking for the thumb #src("C1").
  ],
  related: ("pinch", "sloper", "full-crimp", "volume"),
  sources: ("C1", "C2", "C7", "C11"),
)

== V5: the full crimp

#technique(
  key: "full-crimp",
  name: "Full crimp",
  aliases: ("closed crimp", "crimping", "thumb lock", "voll aufgestellt"),
  category: "hands",
  grade: 5,
  grade-note: [From V5, holds get "smaller and crimpier" #src("C48"). Some tiny edges then work only with a full crimp.],
  summary: [The middle joints bend past 90° and the end joints bend backwards. The thumb often locks over the index fingernail. It is the most secure grip on tiny edges, but it puts very high loads on the finger #jt("pulley", body: [pulleys]) #src("C1", "C9", "C25").],
  figure: "full-crimp.svg",
  caption: [Full crimp from the side, the thumb locked over the index fingernail. The middle joint bends past 90° and the end joint bends back. The load on the A2 pulley is particularly high.],
  how: [
    + Put your fingertips on the edge. Lift your knuckles until the middle joints bend past 90°. The end joints bend back.
    + Lock your thumb over the index fingernail #src("C1", "C9"). It adds force without loading the other fingers more #src("C24").
    + Bring your palm close to the wall. It gets you further behind an #jt("incut") edge #src("C10").
    + Use it for the hard move only. Go back to a half crimp or open hand on the next hold.
    + Keep your feet solid. A foot slip jolts the fingers hard #src("C14", "C26").
  ],
  when: [
    *Look for*
    - very small edges, especially ones that tilt back into the wall #src("C10").

    *Symptoms*
    - The half crimp opens every time on a tiny edge, even with good body position. This move needs the full crimp.
    - Your end joints ache, or the base of a finger hurts after crimpy sessions. You are using it too much.
  ],
  errors: [
    - Full crimping holds big enough for a half crimp or open hand #src("C9").
    - Making many hard crimp attempts in a row #src("C15").
  ],
  tall: [Long fingers can make this grip feel unstable #src("C1"). Keep it for single moves.],
  related: ("half-crimp", "thumb-catch", "open-hand"),
  watch: (("Adam Ondra", "Crimp Grips Tutorial: Crimp Like a Pro Climber", "https://www.youtube.com/watch?v=o59qz4orcWs"), ("Alex Tighe", "How to master the FULL CRIMP (Advanced Training for Climbing)", "https://www.youtube.com/watch?v=33xOqfKn-tE")),
  sources: ("C1", "C9", "C10", "C14", "C15", "C24", "C25", "C26", "C48"),
)

#notebox[Is the full crimp dangerous?][
  #ix("Injuries!pulley", main: true)#ix("Pulley!injury")
  Your finger tendons run through #jt("pulley", body: [pulleys]). The A2 pulley sits at the base of the finger. A crimp bends the finger sharply, so the tendon pulls hard on it.

  - Pulley injuries are climbing's most common overuse injury. A 2021 review names the crimp grip as the cause #src("C27").
  - In one model,#ix("Studies!pulley loads") 96 N at the fingertip put about 255 N on the A2 pulley in a crimp. The open "slope" grip put about 8 N on it #src("C14", "C23").
  - Schweizer#ix("Schweizer, Andreas") puts pulley forces in a crimp at 3–4 times the fingertip force. They become particularly high once the middle joint bends past about 80°, and he advises against bending it past 80–90° #src("C25"). The half crimp in this book, at 85–90°, sits at the top of that range (this book's reading).
  - A sudden jolt on one finger, as from a foot slip, can put about 450 N on A2. Its cited breaking force is about 400 N #src("C26").
  - The model above compares a crimp, with the end joint bent back, with an open grip. We found no pulley load figure for the half crimp, measured or modelled, so the model can't say whether a half crimp saves anything, or how much #src("C23"). The research found for this book does not compare injury rates between full and half~crimping.

  Coaches disagree about what follows. A physio-based guide says use the full crimp only when needed #src("C9"). Ned Feehally#ix("Feehally, Ned") calls controlled full-crimp training on a #jt("fingerboard")#ix("Fingerboard!full-crimp training") (a board of small edges to hang from) "relatively safe", though "not 100 per cent risk free" #src("C8"). Hooper's Beta#ix("Hooper, Jason") says pulleys get stronger with load #src("C14") and links tears to a hand forced open under full load #src("C15").

  *What to do* (this book's suggestion): use the half crimp or open hand by default. Keep the full crimp for the move that needs it. Warm up on 8–12 easy problems first#ix("Warm-up!before crimping") #src("C25"). A warm-up lets the pulleys stretch a little, which is thought to protect them #src("C27").
]
