#import "../template.typ": *

#heading(level: 1, numbering: none)[Troubleshooting: from symptom to technique] <troubleshooting>

#ix("Troubleshooting", main: true)
Find what goes wrong on the wall in the left column. The middle column gives the usual cause. The right column lists techniques to try, with page numbers; try the first one first.

// Table style: `th` and `data-table` in template.typ. A row never splits
// across pages, and the narrow ragged columns aren't hyphenated.
#let ttable(..rows) = {
  set table.cell(breakable: false)
  set text(hyphenate: false)
  data-table(
    columns: (1fr, 0.9fr, 1.35fr),
    table.header(th[Symptom], th[Likely cause], th[Try]),
    ..rows,
  )
}

#heading(level: 2, numbering: none)[Balance and swinging]

#ttable(
  [You swing off like a door when you let go with one hand.],
  [A #tref("barn-door", show-page: false). Your hand and foot on one side form a hinge. Nothing stops the swing.],
  [Flag the free leg: #tref("flag"), #tref("back-flag"), #tref("inside-flag"). Or turn in: #tref("drop-knee"), #tref("backstep"). Or use your other hand #src("E8", "E11", "E12").],

  [Your body sways after a jump, or your hips zig-zag on steep ground.],
  [You lose tension as you catch the hold.],
  [Hold #tref("body-tension") as you land. Move your hips straight into the end position: #tref("overhang") #src("E11", "E5").],

  [On an arête your feet slip and your shins hit the edge.],
  [Your body is too close to the wall.],
  [Turn to about 45° to the edge. Hook a heel round it: #tref("arete"), #tref("heel-hook") #src("E2").],
)

#heading(level: 2, numbering: none)[Feet]

#ttable(
  [Your feet come off when you reach on steep ground.#ix("Feet popping off")],
  [Your hips sag away from the wall. Your feet push instead of pull.],
  [Keep the toes loaded and clawing: #tref("toe-pull"). Bring the hips in: #tref("overhang"). Hook with a #tref("toe-hook") or #tref("heel-hook") #src("E7", "E8", "E11").],

  [Your feet swing off as soon as you move a hand under a roof.],
  [You push on footholds that face down.],
  [Pull on them: #tref("toe-hook"), #tref("bicycle"), #tref("roof"). #jt("downturned shoe", body: [Downturned shoes]) help #src("E7", "E15").],

  [After your feet come off, you can't get them back on.],
  [The swing is out of control.],
  [Let one foot go before the other. Don't fight the swing on the way out. At its peak, tense your stomach and use the backswing to lift your feet: #tref("cutting-loose") #src("E11").],

  [A toe hook keeps popping off.],
  [The foot isn't flexed, or your hips drift out.],
  [Pull the toes towards you and tense the shin and #jt("core"): #tref("toe-hook") #src("E7", "E20"). If it still pops, clamp the hold with both feet: #tref("bicycle").],

  [A heel hook doesn't take any weight.],
  [The heel is too low or isn't pulling.],
  [Place the heel at or above hip height. Pull with the back of your thigh: #tref("heel-hook") #src("E21").],
)

#heading(level: 2, numbering: none)[Reach and steep ground]

#ttable(
  [The next hold on steep ground is a few centimetres too far.],
  [Your hips face the wall square on.],
  [Turn the reaching-side hip in: #tref("hip-turn"), #tref("backstep"), #tref("drop-knee"), #tref("twist-lock") #src("E9", "E11").],

  [You can touch the next hold but can't hold it.],
  [You arrive off balance or too late.],
  [Time the grab to the top of your movement: #tref("deadpoint"). Plan where your hips must end, under the hold #src("E11", "E27").],

  [You can't get your hips up at the top of the wall.],
  [Your feet are low. No heel is on the #jt("lip") (the top edge).],
  [Feet to waist height, heel on the lip, knee in, chest over: #tref("top-out") #src("E14", "E23").],

  [You can't press out of a mantle.],
  [Your hips are not over your hands.],
  [Push with your feet to lift the hips. Lead with the chest. Straighten the arms: #tref("mantle") #src("E23").],

  [You can't get off the mat on a sit start.],
  [You sit square with knees splayed.],
  [Turn the hips 90°, outside edge on the foothold, bottom close to the wall: #tref("sit-start") #src("E11").],
)

#heading(level: 2, numbering: none)[Holds]

#ttable(
  [You can't hold slopers.],
  [Your hips are too high and your arm is bent. Your body is not under the hold.],
  [Keep your #jt("centre of gravity") below the hold and the arm straight. Steer with the hips. Keep one foot low: #tref("sloper") #src("E11", "E18").],

  [A big volume gives you nothing to grip.],
  [You are looking for an edge that isn't there.],
  [Squeeze it: #tref("compression"). Press with your palms: #tref("palming"). Hang low under it on straight arms: #tref("volume") #src("E11", "E18").],

  [A hold feels useless with the hand you planned.],
  [It faces the wrong way for that hand.],
  [Use the other hand or cross: #tref("cross-through"). Try it as a #tref("sidepull") or #tref("gaston") #src("E21", "E29").],
)

#heading(level: 2, numbering: none)[Slab and volumes]

#ttable(
  [Your foot skates off blank wall on a slab.],
  [Your heel is high and you half-commit your weight. Your chest leans in.],
  [Drop the heel. Commit all your weight at once. Keep the hips back over the toes: #tref("slab"), #tref("smearing") #src("E1", "E3", "E16").],

  [Your foot slips as you stand up on a slab hold.],
  [Your weight wasn't over the foot before you stood.],
  [Shift your hips over the foot first. Take smaller steps: #tref("slab"), #tref("rockover") #src("E3", "E16").],

  [Slab handholds feel useless.],
  [You try to pull on them.],
  [Steer with them. Press with a palm: #tref("palming"), #tref("slab") #src("E3", "E4").],

  [You slide off a volume you're standing on.],
  [You stand on its near side, close to the wall.],
  [Stand on the far side, heel lower than the toe. Move slowly: #tref("volume") #src("E5", "E18").],

  [A jump between volumes fails: your foot slips at take-off or you topple on landing.],
  [You launched at the wall, not along it, or #jt("bail", body: [bailed]) at the slip.],
  [Plan the end position first. Stay relaxed until the catch: #tref("dynamic-slab"), #tref("run-and-jump") #src("E5", "E27").],
)

#heading(level: 2, numbering: none)[Corners and traverses]

#ttable(
  [Your arms tire in a corner with footholds on both walls.],
  [You aren't pushing into both walls.],
  [Spread your feet across the corner and press: #tref("stemming"). Rest with no hands where you can #src("E17", "E20").],

  [Traverses feel slow and #jt("pump", body: [pumpy]).],
  [You shuffle your hands and swap feet twice.],
  [Cross through. Flag instead of swapping feet: #tref("traverse"), #tref("cross-through"), #tref("flag"), #tref("back-flag") #src("E11", "E25").],
)

#heading(level: 2, numbering: none)[Endurance]

#ttable(
  [You get #jt("pump", body: [pumped])#ix("Pump!on every problem") (forearms swollen and weak) on every problem.],
  [Coaches blame bent arms and hips away from the wall. You also stop on the wall to re-read.],
  [Hang on #tref("straight-arms"). Bring the hips in. Read the problem first so you stop less. #jt("shake out", body: [Shake out]) at rests #src("E7", "E8", "E10", "E34").],

  [You take many attempts and make no progress.],
  [You are tired. Your rests are too short.],
  [Rest 10–15 minutes between full attempts at your limit. After four to six failed tries, change the sequence or stop (judgement). See Chapter 2 #src("E41", "E42").],
)

#heading(level: 2, numbering: none)[Reading and tactics]

#ttable(
  [You get lost mid-problem, or end up with the wrong hand on a hold.],
  [You didn't read the sequence.],
  [Number the holds. Give each an L or R. Find the matches and crosses: #tref("matching"), #tref("cross-through"). See Chapter 2 #src("E30", "E32").],

  [Your first try fails on the easy top section.],
  [You read only the hardest move.],
  [Read the top from far back. Check the top-out and the way down #src("E30", "E33").],

  [You fall at the same move, the same way, every time.],
  [The sequence or the body position is wrong.],
  [Name the cause of each fall. Try other sequences and small changes to grip and feet. Watch climbers of your size #src("E31", "E41", "E44").],

  [You feel scrunched on a problem others call flowing.],
  [It was set for a shorter span.],
  [Use lower or wider footholds. Skip #jt("intermediate", body: [intermediate holds]). Keep your arms straight (judgement).#ix("Tall climbers!scrunchy problems") See @cons-tall #src("E46", "E47").],

  [A problem feels two grades harder than its tag.],
  [The style doesn't suit you, or the gym grades hard.],
  [Judge the gym by style, not number. Compare with your own reference problems. See Chapter 2 #src("E51", "E53", "E54").],
)
