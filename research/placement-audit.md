# Placement audit: *Reading the Wall*

Repetition, misplaced information and weak references, judged against the rule "good internal references over repetition or information in the wrong section, except where it hurts readability".

**Basis.** The working tree on 2026-11-17, while the "(judgement)" pass was still editing it. Every `file:line` was resolved from the quoted text at that moment, so if a line has moved, search for the quote. Files are in `book/chapters/`.

**Fixed since.** In the same week as the audit: Repetition 1, 3, 12, 13 and 14; Misplaced 1, 2, 5 and 14; References 2, 5, 6 and 8. In a second pass on 2026-11-17, everything else except what is listed here as open.

**Still open, on purpose.**
- Misplaced 15 (the hop onto the high foot) was low priority and would mean moving a step between two entries.
- Misplaced 13: Slab's error about shoes too tight to bend and Run-and-jump's "softer shoes" stay, because the Shoes section says neither.
- References 3 and 4: Straight arms still says "Chapter 1" twice, for a figure and a section that have no label. Sub-subsections and boxes got no labels. The text names them in quotes with their numbered section, as in "Mobility" in `@cons-injuries`.
- References 9: the "meat hook" in Chapter 2's table isn't linked to Wrapping. The link added a line to Wrapping's "Referenced from" list, which pushed the end of that entry onto a page of its own.
- Repetition 20 was judged and left alone in the audit itself.

Six sections got labels in that pass, named after their web anchors: `@hips-and-the-wall`, `@holds-have-a-direction`, `@rotation-and-the-barn-door`, `@hold-direction-and-body-position`, `@shoes` and `@contact-strength-and-grip-endurance`.

**Changed under the audit, so not reported.** Chapter 2's projecting, rest and change-the-beta sections moved to `@cons-projecting`. Indoor grades moved to `@grades-indoor`. "Reading for your size" moved into `@cons-tall` and `@cons-small`. The World Cup attempt statistics were cut. "How this book was made" became an appendix. Two troubleshooting rows now use labels. Grade notes were being rewritten in chapters 3–7, so findings about grade notes may already be out of date.

**Kept on purpose in the streamline logs, so not reported.** The `#remember` boxes, the per-band max-hang figures, "Find your limiter", the quiet-feet drill box, the dispatch tables that open chapters 3, 4, 6 and 7, "Power comes from the legs and hips", the LCL warning in heel hook and rockover, the pocket warning twice in Chapter 6, and the off-foot and look-back cues shared by hip-turn and cross-through.

Labels that exist: `@reading-method`, `@reading-first`, `@reading-setter`, `@reading-size`, `@three-questions`, `@fig-balance`, `@grades-indoor`, `@grade-0` … `@grade-8`, `@grades-v4-v5`, `@progression-map`, `@cons-tall`, `@cons-small`, `@cons-heavy`, `@cons-adult`, `@cons-learning`, `@cons-projecting`, `@cons-falling`, `@fig-cons-sit`, `@fig-cons-fall`, `@fig-cons-fall-wrong`; unnumbered appendix headings `<troubleshooting>`, `<glossary>`, `<grade-conversion>`, `<on-the-mat>`, `<a-to-z>`, `<sources>`, `<index>` need `#link(<…>)[…]`, as `a-card.typ` does.

---

## 1. Repetition

1. **"Keep big jumps for the moves that need them, and don't snatch at small holds": six statements and no single home.**
   - Where: `06-dynamic.typ:23` “keep big jumps for the moves that need them (judgement; see Chapter 9)” ("Static or dynamic?"); `06-dynamic.typ:122` “Snatching at a small hold” (deadpoint errors); `06-dynamic.typ:125` “don't snatch at small holds (judgement; see @cons-heavy)” (deadpoint `small:`); `08-grades.typ:462` “Save the fastest catches on small holds for moves that need them” (V7); `09-considerations.typ:83` “Keep big jumps for the moves that need them (this book's suggestion)” (small, step 4); `09-considerations.typ:106` “Small deadpoints are fine, but keep big jumps” (heavier, step 3).
   - Home: Chapter 6, "Static or dynamic?", which is where the reader chooses. It needs a label.
   - Fix: keep the deadpoint error (a one-line safety warning in place). Cut the sentence from the deadpoint `small:` note, since the error is three lines above it. The Chapter 8 and Chapter 9 lines keep the instruction in a clause and point to the new label. A small climber shouldn't be sent to "Climbing heavier" for it.

2. **Chapter 8 re-summarises three Hooper lessons that Chapter 4 already turns into entries, and links none of them.**
   - Where: `08-grades.typ:307` “Locking off on the steep” (F39, the same video as B47) against the pre-loading entry, `04-body.typ:609` “Let your hips sit down and slightly out”. `08-grades.typ:308` “Staying tight to the wall when you need to turn” (F40 = B48) against `01-movement.typ:42` “does not mean "as tight as you can"”, `04-body.typ:610` “get as far from your bottom hand as you can”, `04-body.typ:653` “Hips jammed into the wall unload the feet” and `05-hands.typ:382` “hugging the wall can stop you turning”. `08-grades.typ:309` “Ignoring the off foot” (F41 = B45) against `04-body.typ:183` “about at right angles to the hinge” and `04-body.typ:400` “puts it at about 90° to the line from holding hand to standing foot”.
   - Home: the pre-loading entry, Chapter 1 "Hips and the wall", and barn-door fix 4.
   - Fix: each of the three items keeps its one-sentence diagnosis and ends with the link: `#tref("pre-loading")`; "Chapter 1, Hips and the wall" (labelled) and `#tref("body-tension")`; `#tref("barn-door")`, fix 4. The how-to sentences go.

3. **Two numbered lists of barn-door fixes that don't match.**
   - Where: `01-movement.typ:67` “Put weight or a contact on the far side of the hinge” (fixes 1–4) against `04-body.typ:180` “Stand on the other foot. Stepping up with your right foot?” (fixes 1–5). `04-body.typ:176` “start with fixes 1 and 4” and `04-body.typ:186` “then try fix 1” mean the entry's numbers. `a-troubleshooting.typ:25` “Flag the free leg” gives a third order.
   - Home: the barn-door entry for the numbered how-to; Chapter 1 for the mechanics.
   - Fix: turn Chapter 1's list into unnumbered principles and end with "`#tref("barn-door")` lists the fixes in the order to try them", so that "fix 1" means one thing.

4. **One gym owner's claim that dynamic moves save energy (D13) is made eight times.**
   - Where: `01-movement.typ:78` “Dynamic movement can save energy compared with a hard lock-off”; `06-dynamic.typ:15` “moving faster can mean less time on the wall”; `06-dynamic.typ:23` “dynamic moves are generally more efficient than lock-offs”; `06-dynamic.typ:108` “deadpoints more efficient the steeper the wall”; `06-dynamic.typ:120` “Locking off out of habit where a deadpoint might save energy”; `06-dynamic.typ:124` “it may save energy” (deadpoint `tall:`); `06-dynamic.typ:234` “The throw probably costs less energy” (lunge `tall:`); `09-considerations.typ:110` “dynamic moves save energy compared with locking off (Chapter 6)”.
   - Home: "Static or dynamic?".
   - Fix: keep Chapter 1 (one clause) and the deadpoint look-for (the steepness point is new there). The deadpoint error becomes "Locking off out of habit: see Static or dynamic?". Drop the clause from the two `tall:` notes. Chapter 9 uses the section's label instead of "Chapter 6".

5. **The deadpoint `small:` note and "How to climb small" give the same advice from the same sources.**
   - Where: `06-dynamic.typ:125` “go for holds just out of reach on easy problems” (D45, H4, H6); `09-considerations.typ:83` “to holds just out of reach” (D45, H4).
   - Home: the deadpoint `small:` note, which is the how-to.
   - Fix: Chapter 9's step becomes "*Learn momentum in small steps* (B34): the small-climber note in `#tref("deadpoint")` says how."

6. **Tall sit-start advice sits in three places, and each says something different.**
   - Where: `03-feet.typ:158` “sit side-on with the outside edge on the foothold” (edging `tall:`); `07-terrain.typ:312` “Sit to the side of the start holds and lay your free leg flat” (sit-start `tall:`, no link to Part IV); `09-considerations.typ:41` “Sit as close to the wall as the start holds allow” (with `@fig-cons-sit`).
   - Home: `@cons-tall`, step 3, kept there on purpose with its figure.
   - Fix: both `tall:` notes become "`@cons-tall` has the sequence and a figure". Move "lay your free leg flat along the mat" into step 3, and open step 3 with "Set up as in `#tref("sit-start")`" instead of repeating that entry's first three steps.

7. **The slab entry restates smearing, weight shift and precise footwork**, against the chapter's promise at `07-terrain.typ:7` “don't repeat how to do a heel hook or a drop knee”.
   - Where: `07-terrain.typ:53` “shift your hips over the foot you will stand on” (a weight shift, unlinked); `07-terrain.typ:55` “drop the heel so more of the front of the sole touches” = `03-feet.typ:213` “Drop the heel. More rubber then touches the wall”; `07-terrain.typ:57` “Take several small steps rather than one big high step” = `03-feet.typ:216` “Several small steps beat one big one” and `03-feet.typ:267` “there, high steps upset your balance”; `07-terrain.typ:76` “Testing a foothold again and again instead of committing” = `03-feet.typ:237` “Fidgeting with test placements” and `03-feet.typ:104` “Testing and re-testing a foot”.
   - Home: those three entries.
   - Fix: step 1 ends "See `#tref("weight-shift")`". Step 3 becomes "Smear with the heel low (`#tref("smearing")`); on small edges stand on the big toe." Drop the testing error from slab.

8. **Roof steps restate the toe-hook entry, and the ankle advice has drifted from it.**
   - Where: `07-terrain.typ:331` “Flex the foot and pull the toes towards you under a hold”; `07-terrain.typ:334` “plan how it comes out” = `03-feet.typ:544` “Plan the release as small foot moves”; `07-terrain.typ:335` “Look to the sides for toe hooks” = `03-feet.typ:563` “Missing hooks you can't see”. Also `a-troubleshooting.typ:53` “Pull the toes towards you and tense the shin” and `06-dynamic.typ:496` “pull your toes up towards your shin”. Only the entry settles the disagreement: `03-feet.typ:546` “Sources disagree on the ankle”.
   - Home: toe-hook.
   - Fix: roof step 2 becomes "Keep your feet on by pulling: `#tref("toe-hook")`". Fold roof steps 5 and 6 into one line with the link. The troubleshooting row and foot-catch step 3 say "set the hook as in `#tref("toe-hook")`" instead of "flex".

9. **Stemming's "Corners" part repeats the entry's main steps** (left from merging the corner entry).
   - Where: `04-body.typ:259` “Press a palm flat on a wall” against `04-body.typ:268` “press a flat palm on each wall at chest height”; `04-body.typ:260` “Move one limb at a time” against `04-body.typ:269` “Step up a short way at a time”; `04-body.typ:257` “Push each foot into its surface” against `04-body.typ:267` “press outward and down, evenly on both walls”; `04-body.typ:261` “To rest, stand fully on any ledge” against `04-body.typ:271` “Spread your feet wide to rest”.
   - Fix: keep in "Corners" only what is specific to a corner: which way to face, laybacking the edge when one wall is blank, and the no-hands rest. Delete its steps 2–4.

10. **"Pull with your toes" is explained in toe-pull, body tension and overhang, and restated three times in Chapter 8 without a link.**
    - Where: `03-feet.typ:443` “as if you were drilling it in”; `03-feet.typ:447` “Keep the feet loaded at the moment a hand lets go”; `04-body.typ:651` “Press your toes into the footholds. Keep the pressure on”; `04-body.typ:652` “Pull with the backs of your thighs”; `07-terrain.typ:216` “Press each toe down and into its hold”. The errors `03-feet.typ:465` “Trying to fix it with more sit-ups” and `04-body.typ:671` “Treating it as a core-strength problem” make one point. Unlinked restatements: `08-grades.typ:201` “Toes into the wall on steep ground”, `08-grades.typ:220` “keep both feet pressing into the wall”, `08-grades.typ:249` “keep pushing through both toes”.
    - Home: toe-pull for the feet, body-tension for the trunk and hips.
    - Fix: body-tension steps 1–2 become "Pull with your toes (`#tref("toe-pull")`)". Keep the core-strength error in body-tension and point to it from toe-pull. The three Chapter 8 bullets keep their cue and end with the link.

11. **Grade notes and Chapter 1 restate the straight-arms how-to.**
    - Where: `04-body.typ:97` “when you pause on a steep wall, hang on nearly straight arms” (grade note; the entry's steps 1–3 and `04-body.typ:121` “Sinking low on a vertical wall” say it below); `05-hands.typ:63` “When you pause on one on a steep wall, hang on a straight arm” (jug grade note; jug step 4 says it); `01-movement.typ:26` “The UK's coach training lists them as a way to find a rest” = `04-body.typ:97` “The UK's coach training lists it as a way to find a rest”.
    - Home: the straight-arms steps and error.
    - Fix: the two grade notes say only when it starts to matter. Chapter 1 drops its last two sentences, since it links the entry in the same paragraph. The one-line vertical-wall warnings in pre-loading, VB–V0 and the drills table stay.

12. **Small hands on wide pinches: the same advice in the pinch note and in Chapter 9.**
    - Where: `02-reading.typ:162` “climbers with small hands” (one clause, stays); `05-hands.typ:423` “you may be able to hold it like an edge”; `09-considerations.typ:90` “You may be able to hold a wide pinch like an edge”.
    - Home: the pinch `small:` note for what to do; "Small hands" in `@cons-small` for the evidence.
    - Fix: Chapter 9 keeps the setter's remark and the finger-length study, and replaces the second sentence with "The small-climber note in `#tref("pinch")` says what to try."

13. **The projecting method is restated in the V4→V5 plan.**
    - Where: `08-grades.typ:343` “Break each one into single moves. Once every move goes, link pairs” against `09-considerations.typ:278` “Learn the single moves first, in isolation”. Also `07-terrain.typ:375` “Work long sequences one contact at a time” = "Get the first contact right before you add the second" on that Chapter 9 line (both E5).
    - Home: `@cons-projecting`.
    - Fix: plan step 2 becomes "Work each one as a project (`@cons-projecting`)". The dynamic-slab step stays, as a how-to step.

14. **"Setters avoid ladders" twice in Chapter 2.**
    - Where: `02-reading.typ:48` “Expect at least one move that is not a straight ladder” (step 4, E46); `02-reading.typ:146` “They avoid ladders” (E46, E47).
    - Home: `@reading-setter`.
    - Fix: the step 4 item becomes "Expect at least one match or cross; `@reading-setter` says why."

15. **Gym-rule checks repeated in two terrain entries.**
    - Where: `02-reading.typ:25` “Volumes often count for every problem on that wall” = `07-terrain.typ:108` “Volumes are usually part of every problem on that wall” (E19); `02-reading.typ:26` “Some gyms want you settled on the start holds” = `07-terrain.typ:298` “Check the rule at your gym”, where the same sentence follows word for word (E70–E72). The streamline log left this pair for the Chapter 7 editor.
    - Home: `@reading-method`, step 1.
    - Fix: both terrain lines become "Check your gym's rule (`@reading-method`, step 1)." The top-out's "way down" bullet stays, because the reader acts on it there.

16. **The hip flick on steep foot swaps: one tip, one source, two entries.**
    - Where: `03-feet.typ:373` “flick your hips to stop your legs swinging out” (A22); `04-body.typ:657` “a quick flick of the hips stops your legs swinging out” (B58, which `src-map.typ` merges into A22).
    - Home: foot-swap.
    - Fix: cut body-tension step 7, or make it "For foot swaps on overhangs, see `#tref("foot-swap")`."

17. **One sentence in both pinch and thumb-catch.**
    - Where: `05-hands.typ:403` and `05-hands.typ:594`, both "put the thumb on one face and the fingers on the other" (C11).
    - Home: pinch.
    - Fix: thumb-catch step 5 becomes "*On a volume edge:* pinch it (`#tref("pinch")`)."

18. **"Make the half crimp your default" word for word in the entry and the V2 guide.**
    - Where: `05-hands.typ:137` and `08-grades.typ:149`, both "so you don't fall into the habit of full crimping". Also `05-hands.typ:160` “Sliding into a full crimp out of habit” and `05-hands.typ:662` “use the half crimp or open hand by default”.
    - Home: the half-crimp entry and the full-crimp box.
    - Fix: the V2 guide says "On crimps, start with the `#tref("half-crimp")`". The lines in Chapter 5 stay.

19. **Fall-survey figures in the dyno entry and in Chapter 9** (one paper under two keys, D44 = G14).
    - Where: `06-dynamic.typ:275` “22% of the falls happened on dynos” against `09-considerations.typ:358` “Jumps cause about a fifth of the falls”; `06-dynamic.typ:276` “Cross your arms in front and land as Chapter 9 describes” against `09-considerations.typ:340` “suggest crossing your arms in front and rolling backwards”.
    - Stay: both are safety warnings where the reader acts. Change only the pointer, to `@cons-falling`.

20. **Judged and left alone: one-line warnings a reader needs in place.** The forced-open hand (`05-hands.typ:147`, `05-hands.typ:197`, `05-hands.typ:528`, `05-hands.typ:660`); repeated crimp attempts (`05-hands.typ:161`, `05-hands.typ:642`); foot slips that jolt the fingers (`05-hands.typ:558`, `05-hands.typ:630`); "catch with a bent arm, shoulder blade down" across the dynamic entries; "commit, don't hesitate" in mantle and top-out. Each is one line in a step or an error list.

## 2. Misplaced information

1. **The knee-injury box is filed under "Climbing tall" but is for everyone.**
   - Where: `09-considerations.typ:49` “Your knees on high steps and drop knees”. It is cited from small-climber advice (`04-body.typ:503` “read the knee box in @cons-tall first”, `09-considerations.typ:81` “Read the knee box in @cons-tall first”), from the hip pop (`06-dynamic.typ:94` “see the knee box in @cons-tall”), as `04-body.typ:587` “Chapter 9 gives the injury figures”, and by description at `09-considerations.typ:120` “One knee-injury study”, `09-considerations.typ:163` “In the knee-injury study” and `09-considerations.typ:329` “In a study of knee injuries”.
   - Belongs: `@cons-adult`, "The injuries that actually happen", beside the "Ankles and knees" row, with a label of its own.
   - Stays behind: the "High feet" bullet in "Where height hurts", with a pointer. The box's precautions (`09-considerations.typ:53` “keep the other foot solid”) are technique warnings: one line each in the drop-knee and high-step errors, pointing to the box.

2. **The warm-up routine, the injury table and the recovery advice sit under "Starting as an adult".**
   - Where: `09-considerations.typ:160` “==== Warming up”, `09-considerations.typ:139` “==== The injuries that actually happen”, `09-considerations.typ:193` “==== Recovery and rest”. The front matter promises `00-front.typ:152` “Chapter 9 covers injuries, warming up and falling”. Entries mention a warm-up with no link: `03-feet.typ:516` “Skipping the warm-up”, `05-hands.typ:662` “Warm up on 8–12 easy problems first”, `06-dynamic.typ:405` “Skipping the warm-up for hips, knees and ankles”, `07-terrain.typ:369` “Warm up hips, knees and ankles”, `09-considerations.typ:260` “so warm up first”.
   - Belongs: a section of its own in Part IV ("Warming up and injuries"), or at least a label on each subsection.
   - Stays behind in "Starting as an adult": tendon adaptation and finger training. Each entry's mention gets the label.

3. **The evidence behind "keep big jumps for the moves that need them" sits under "Climbing heavier".**
   - Where: `09-considerations.typ:110` “On step 3: one gym owner's article”, with the 35-climber shoulder study. Chapter 6 and the deadpoint `small:` note send readers there (finding 1.1).
   - Belongs: "Static or dynamic?" in Chapter 6, or `@cons-adult` beside `09-considerations.typ:151` “In a small indoor bouldering study, 26% had a shoulder injury”, which cites the same study.
   - Stays behind: step 3 as one line with the pointer.

4. **Advice for heavier climbers in the hands introduction and in a `tall:` note.**
   - Where: `05-hands.typ:9` “The heavier you are, the more load your fingers carry” (chapter introduction, no link); `06-dynamic.typ:316` “A tall body weighs more, so more force goes through your fingers” (latching `tall:`). The home says the same: `09-considerations.typ:96` “Your fingers carry whatever weight your feet don't”.
   - Belongs: `@cons-heavy`.
   - Stays behind: one sentence in the introduction ending "(`@cons-heavy`)". The latching advice moves to `@cons-heavy`, "Footwork first", as "choose a deadpoint over a full dyno where both work (`#tref("latching")`)", because a heavier reader who isn't tall won't read `tall:` notes.

5. **Advice for small climbers inside a `tall:` note and a grade note.**
   - Where: `03-feet.typ:519` “Short climbers use heel hooks mainly to gain reach” (heel-hook `tall:`); `06-dynamic.typ:173` “Shorter climbers meet it from V2” (jump-start grade note).
   - Belongs: `small:` notes on those two entries; neither has one, though `@cons-small` tells small climbers to use a high heel hook.
   - Stays behind: the tall half of the heel-hook note, and the four-point-start sentence in the grade note.

6. **"Height hides missing technique" appears only in two chapter introductions.**
   - Where: `04-body.typ:9` “That hides missing technique until the holds get small or far apart (see Chapter 9)”; `06-dynamic.typ:9` “The missing skill shows when a setter forces momentum”. Chapter 9 says the advantage fades but doesn't give this advice, though Chapter 4 sends the reader there.
   - Belongs: a point in `09-considerations.typ:35` “==== How to climb tall”: practise what your reach lets you skip, on problems you can already climb.
   - Stays behind: one sentence in each introduction with `@cons-tall`.

7. **The gaston shoulder warning is in opposition, not in gaston.**
   - Where: `04-body.typ:753` “Pushing gastons apart on a steep wall for long”. The gaston errors start at `05-hands.typ:492` “Turning the thumb up and pulling it like a sidepull” and say nothing about the shoulder.
   - Belongs: gaston errors.
   - Stays behind: the line in opposition can stay as it is or become a pointer.

8. **"Don't throw for small pockets" is in Chapter 6 twice but not in the pocket entry.**
   - Where: `06-dynamic.typ:19` “Dynos to small pockets are a common cause of finger injuries”; `06-dynamic.typ:232` “Lunging for small pockets”. Pocket's steps end at `05-hands.typ:558` “Load the pocket smoothly”, and its `related:` has no dynamic entry.
   - Fix: a pointer in pocket's errors ("Throwing for a pocket: see `#tref("lunge")`") and `latching` in its `related:` (latching already lists pocket). The two Chapter 6 lines stay.

9. **The layback tip for vertical pinches is in layback and compression but not in pinch.**
   - Where: `04-body.typ:451` “Turning side-on into a layback needs less thumb strength”; `04-body.typ:458` “Staying front-on to a sidepull or pinch”; `04-body.typ:895` (compression step 7, B24). Pinch says only `05-hands.typ:405` “Lean off it, twist, or squeeze two pinches together”.
   - Belongs: pinch step 6, with `#tref("layback")`, and `layback` in pinch's `related:`.
   - Stays behind: layback's look-for line. Compression step 7 can go.

10. **Ape index and grade: the Lattice finding lives only in the compression `tall:` note.**
    - Where: `04-body.typ:911` “show little link between”. The ape-index paragraph at `09-considerations.typ:21` “is your arm span minus your height” doesn't mention it.
    - Belongs: `@cons-tall`, "What height does and doesn't predict".
    - Stays behind: "Wide spans are more comfortable at your height, but span predicts grade poorly (`@cons-tall`). The squeeze and the footwork matter more."

11. **Hand-size advice is filed under `tall:`.**
    - Where: `05-hands.typ:422` “Big hands help on wide pinches”; `05-hands.typ:573` “Large fingers fit fewer fingers into a pocket”; `05-hands.typ:644` “Long fingers can make this grip feel unstable”. Part IV has only `09-considerations.typ:87` “==== Small hands”.
    - Fix: retitle that subsection "Hand size" and add one line that links the three notes. The notes stay where they are.

12. **A heel-hook item sits in the list for bailing from dynos.**
    - Where: `09-considerations.typ:361` “Know how to get out of every hook”, in the list introduced for dynos, double dynos and run-and-jumps. The heel-hook entry's release step, `03-feet.typ:492` “To let go, first put the other foot on a solid hold”, says nothing about a fall.
    - Belongs: heel-hook errors, as one line with `@cons-falling`. The key point at `09-considerations.typ:395` “heel hooks above your head” already carries it for Chapter 9.
    - Stays behind: the dyno items.

13. **Shoe advice is written as steps and errors in four entries, while the Shoes section has no label and the toe-hook entry has no shoe line.**
    - Where: `03-feet.typ:57` “== Shoes” with `03-feet.typ:64` “choose shoes with rubber over the top of the toes”; again at `06-dynamic.typ:498` “Wear shoes with rubber on top of the toes” (foot-catch step 5) and `07-terrain.typ:350` “Rubber on top of the toe helps toe hooks” (roof error). Also `06-dynamic.typ:388` “Wear softer shoes” (run-and-jump step 2) and `07-terrain.typ:77` “Shoes so tight they can't bend” (slab error).
    - Belongs: "Shoes" in Chapter 3, labelled, with links to the entries it names (toe-pull, smearing, toe-hook, heel-hook).
    - Stays behind: a pointer in each entry, toe-hook included. The heel-hook fit check stays (kept on purpose).

14. **Mobility is filed under "Climbing tall".**
    - Where: `09-considerations.typ:56` “==== Mobility”, whose first sentence, `09-considerations.typ:58` “knees turned out for frogs and high steps”, applies to any climber and links none of the four techniques it names.
    - Belongs: beside the warm-up (finding 2), or it keeps its place and gets a label.
    - Stays behind: a pointer from "Where height hurts".

15. **"Hop your hips onto the high foot" starts a rockover but sits in high-step.** (Low priority.)
    - Where: `03-feet.typ:259` “Hop your hips onto the high foot”, one step before "Finish with a rockover".
    - Belongs: rockover, after `03-feet.typ:294` “first, not up. Once you are over the foot, standing up is easy”.
    - Stays behind: high-step's first five steps and the pointer.

## 3. Missing or weak references

1. **"Sitting into it" (pre-loading) is never linked from running text.** Only three `related:` lists reach it (straight-arms, body-tension, sit-start).
   - Where it is described without a link: `06-dynamic.typ:36` “Let your hips sag out from the wall and down” ("Load"); `06-dynamic.typ:83` “Let your hips sag out from the wall and slightly down” (deadpoint); `06-dynamic.typ:214` “but sink lower” (lunge); `06-dynamic.typ:255` “Bend your knees and drop your hips” (dyno); `08-grades.typ:185` “Sink your hips, then drive”; `08-grades.typ:202` “Sink your hips a little, then drive up with your legs”; `08-grades.typ:248` “Sit your hips back and down”; `08-grades.typ:229` “Start big steep moves from straight arms”; `08-grades.typ:280` “Start steep moves on straight arms”.
   - Fix: "See `#tref("pre-loading")`" at "Load" and at "Locking off on the steep" (finding 1.2); a `body:` link in the Chapter 8 focus bullets; `pre-loading` in the `related:` of deadpoint, dyno and lunge.

2. **"Chapter 9" where a label exists.**
   - `00-front.typ:152` “Chapter 9 covers injuries, warming up and falling” → `@cons-adult` and `@cons-falling`.
   - `04-body.typ:9` “(see Chapter 9)” → `@cons-tall`.
   - `04-body.typ:587` “Chapter 9 gives the injury figures” → the knee box (finding 2.1).
   - `06-dynamic.typ:9` “read the falling section in Chapter 9”, `06-dynamic.typ:195` “Bend your knees and roll back (Chapter 9)”, `06-dynamic.typ:276` “land as Chapter 9 describes”, `07-terrain.typ:369` “so learn to fall first” → `@cons-falling`.
   - `06-dynamic.typ:23` “(judgement; see Chapter 9)” → see finding 1.1.

3. **"Chapter 2", "Chapter 1" and "the appendix" where a label exists.**
   - `@reading-method`: `01-movement.typ:50` “Chapter 2 turns this into a method”; `03-feet.typ:22` “Chapter 2 (step 5) shows how”; `09-considerations.typ:230` “with the method in Chapter 2”; `09-considerations.typ:271` “Chapter 2 gets you a plan for the first try”; `08-grades.typ:355` “Read in chunks (Chapter 2)”; the "See Chapter 2" in the row at `a-troubleshooting.typ:153` “Find the matches and crosses”.
   - `@fig-balance`: `04-body.typ:65` “as the balance figure in Chapter 1 shows”.
   - `#link(<troubleshooting>)[…]`: `01-movement.typ:92` “The troubleshooting appendix lists techniques by symptom”; `04-body.typ:54` “The troubleshooting appendix collects them”.
   - `#link(<grade-conversion>)[…]`: `08-grades.typ:10` “The appendix converts V-grades”.
   - `@three-questions`: the card at `a-card.typ:30` “Three questions for every move”.

4. **Sections the text points to by name or chapter number, but which have no label.**
   - Chapter 1: `01-movement.typ:34` “== Hips and the wall”, `01-movement.typ:46` “== Holds have a direction”, `01-movement.typ:60` “== Rotation and the barn door”. Pointed to by `02-reading.typ:95` “the rule from Chapter 1”, `03-feet.typ:19` “the diagonal from Chapter 1”, `04-body.typ:5` “Chapter 1 explains the mechanics behind this”, `04-body.typ:98` “Chapter 1 shows the difference in a figure”, the barn-door summary (`04-body.typ:177`), `05-hands.typ:16` “Chapter 1 explains why”, `07-terrain.typ:13` “Chapter 1 explains why”, `08-grades.typ:119` “puts your body to its right (Chapter 1)” and `09-considerations.typ:37` “built on the mechanics in Chapter 1”.
   - Chapter 2: `02-reading.typ:92` “== Hold direction and body position”, pointed to by `05-hands.typ:16` “Chapter 2 has a table” and `02-reading.typ:38` “the next section explains how”.
   - Chapter 6: `06-dynamic.typ:13` “== Static or dynamic?” (findings 1.1 and 1.4).
   - Also: the box `05-hands.typ:650` “Is the full crimp dangerous?”; `09-considerations.typ:176` “==== When finger training makes sense”; `09-considerations.typ:355` “==== Bailing from dynos and big moves”; `09-considerations.typ:235` “==== Drills”; `08-grades.typ:313` “==== Technique or strength?”, which the remember box cites by name; and the box `08-grades.typ:16` “How long climbers have been climbing”, cited as `08-grades.typ:522` “see the chapter's opening box”.
   - Fix: add the labels and replace the prose pointers.

5. **The heel-hook entry doesn't point to the two places that discuss its risks.**
   - Where: its errors run from `03-feet.typ:512` “Slapping the heel on without pulling” to `03-feet.typ:517` “Turning the foot out hard on a heel close to the hip”. Chapter 9 says heel hooks `09-considerations.typ:51` “caused 40.3%” of the knee injuries in one study and names heel hooks above the head as a mark of a dangerous fall.
   - Fix: one error line with both links. Add `@cons-falling` to `03-feet.typ:629` “Falling with the foot locked” (heel–toe cam) and `03-feet.typ:671` “Wedging the leg where it could stay stuck in a fall” (knee bar) too.

6. **The knee box names high steps and drop knees but links only heel-hook and rockover, and neither entry links back.**
   - Where: `09-considerations.typ:51` “One study looked at 77 acute knee injuries”. High-step's only pointer is `03-feet.typ:276` “For stretches, see @cons-tall”.
   - Fix: `#tref("high-step")` and `#tref("drop-knee")` in the box, and the error lines from finding 2.1.

7. **Dynamic entries describe bailing without linking the section that covers it.**
   - Where: `06-dynamic.typ:20` “onto an awkward landing”; `06-dynamic.typ:443` “Not planning the miss” (Chapter 9 has `09-considerations.typ:360` “Plan the miss before the go”); `06-dynamic.typ:407` “treat the whole runway as your landing zone”; `07-terrain.typ:195` “jump off while you still control the fall”.
   - Fix: `@cons-falling`, or a label on "Bailing from dynos and big moves".

8. **"Static or dynamic?" defines the deadpoint, the dyno and the one-handed dyno without linking them.**
   - Where: `06-dynamic.typ:23` “is a deadpoint while a foot stays on and a dyno once both feet leave”. The section links only lock-off, volume and slab.
   - Fix: `#tref` to deadpoint, dyno and lunge at first mention.

9. **`related:` lists that miss a technique the entry's own steps depend on.**
   - mantle: heel-hook (`05-hands.typ:284` “The heel hook in step 2”).
   - barn-door: backstep, drop-knee, deadpoint (`04-body.typ:197` “yet you still rotate out”; `04-body.typ:184` “Fix 5, once you can deadpoint”).
   - lunge: foot-catch (`06-dynamic.typ:219` “Stop the swing. Press the remaining foot hard”).
   - double-dyno: lunge, deadpoint (`06-dynamic.typ:420` “a deadpoint or a one-handed dyno usually works”, unlinked).
   - roof: toe-pull, straight-arms (`07-terrain.typ:326` “pulling with your toes and heels”; “Hang on straight arms” at `07-terrain.typ:330`, both unlinked).
   - slab: weight-shift (finding 1.7), mantle (`07-terrain.typ:59` “To gain height with no holds, press down on your palms”).
   - volume: wrap (`07-terrain.typ:96` “"meat hook": palm on one face, fingers over the other”, an alias of wrap and unlinked; the same in `02-reading.typ:107`), stemming (`07-terrain.typ:107` “bridge between them”), heel-hook and toe-hook (`07-terrain.typ:101` “spots for heel and toe hooks”).
   - sloper: thumb-catch (`05-hands.typ:361` “Look for a thumb spot below or beside the hold”).
   - drop-knee: pivoting (`04-body.typ:564` “That leaves room to pivot”), sidepull.
   - hip-turn, backstep, twist-lock: sidepull, the holding hold all three ask for (`04-body.typ:312`, `04-body.typ:479`, `04-body.typ:823`). hip-turn also: straight-arms (`04-body.typ:316` “Keep the right arm straight and lean off it”).
   - deadpoint: pre-loading (finding 3.1).
   - weight-shift: slab (`04-body.typ:69` “also push your hips out from the wall”).
   - toe-pull: hip-turn, drop-knee (`03-feet.typ:446` “Turn a hip in and use the outside edge, or drop a knee”, unlinked).
   - body-tension: roof, overhang (`04-body.typ:661` “a cave, a roof or an overhang steeper than about 30”, unlinked), toe-hook, heel-hook.
   - Smaller: straight-arms → jug; frog → edging; layback → straight-arms; toe-hook → body-tension, arete; traverse → hip-turn.

10. **Rockover "over a heel" doesn't link the entry that teaches it.**
    - Where: `03-feet.typ:298` “learn the” … heel hook first, in the step "Over a heel". Top-out carries the alias `07-terrain.typ:166` “heel-hook rockover” and the full sequence.
    - Fix: end the step "See `#tref("top-out")`" and add `top-out` to rockover's `related:`.

11. **Chapter 9's Drills section doesn't point to the drills kept in entries.**
    - Where: `09-considerations.typ:235` “==== Drills”. Drills elsewhere: `03-feet.typ:21` “make three foot placements for every hand move”; `03-feet.typ:109` “Drills for quiet feet”; `03-feet.typ:375` “make 20 swaps”; `03-feet.typ:451` “Move your feet to 10 different holds per set”; `05-hands.typ:18` “mark each hold's best pulling direction with a strip of tape”; `05-hands.typ:51` “ease off until you are only just holding on”; `06-dynamic.typ:314` “jump to a bar, catch with bent arms”; `04-body.typ:186` “Practise on a slab. Let yourself swing open”.
    - Fix: one line under the table, "More drills in the entries:", with the links. `08-grades.typ:115` “relax your fingers until they start to slip” restates the grip drill and should point to Chapter 5's "Contact strength and grip endurance".

12. **Overview tables whose rows don't link their entries.**
    - Where: the wall-angle table, `07-terrain.typ:21` “[Slab], [Almost all your weight” and `07-terrain.typ:23` “[Overhang], [Your arms carry more”, with the Roof and Arête rows; only the Corner row links. In Chapter 4, `04-body.typ:26` “[Overhang 10–30°]” and `04-body.typ:27` “[Steep 30–75°]”.
    - Fix: `#tref(…, show-page: false)` in the first cell of each row.

13. **Overhang step 4 describes turning the hip in but links only backstep and twist-lock.**
    - Where: `07-terrain.typ:218` “turn the hip on the reaching side into the wall”. The same at `03-feet.typ:151` “Turn a hip in.” (edging symptom).
    - Fix: `#tref("hip-turn")` in the step. It is in overhang's `related:`, but a reader follows the step.

14. **Hip-turn's step 2 is a backstep and doesn't say so.**
    - Where: `04-body.typ:313` “Put your left foot on its” outside edge "on a foothold below your right hand". Backstep's steps 1, 5, 6 and 8 repeat hip-turn's 1, 3, 4 and 7.
    - Fix: both step lists should stay complete. Add the link: hip-turn step 2 "(a `#tref("backstep")`)", and backstep step 1 "Set up as for `#tref("hip-turn")`".

15. **The hip pop uses "behind the line" without the glossary link or the entry that explains it.**
    - Where: `06-dynamic.typ:99` “avoid a foot that sits "behind the line" of your body”; `06-dynamic.typ:116` “You spin away from the wall as you reach”.
    - Fix: `#jt("the line")`, and "see `#tref("backstep")`" for the spin-out.

16. **Troubleshooting rows with advice but no link.**
    - `a-troubleshooting.typ:141` “Read the problem first so you stop less” → `@reading-method`.
    - `a-troubleshooting.typ:157` “Check the top-out and the way down” → `@reading-method` and `#tref("top-out")`.
    - `a-troubleshooting.typ:161` “Watch climbers of your size” → `@cons-projecting` ("When to change the beta") and `@reading-size`.

17. **Glossary terms whose home is an entry but that have no `see:`.**
    - `a-glossary.typ:154` off foot → barn-door. `a-glossary.typ:218` spin-out and `a-glossary.typ:236` the line → backstep. `a-glossary.typ:230` sweet spot → regrip. `a-glossary.typ:42` contact strength → latching. `a-glossary.typ:98` four-point start → jump-start. `a-glossary.typ:200` shake out → jug. `a-glossary.typ:88` flake → layback. `a-glossary.typ:130` lip → top-out, mantle. `a-glossary.typ:150` momentum → hip-pump. `a-glossary.typ:182` pump → straight-arms.

18. **Finger-training advice in three places with one link between them.**
    - Where: the full-crimp box cites `05-hands.typ:660` “Ned Feehally” on full-crimp fingerboard training; Chapter 9's key point says `09-considerations.typ:190` “never a full crimp”; `08-grades.typ:436` “Forum climbers recommend finger training to break into V6” has no link, though the VB–V0 and V4→V5 guides link `@cons-adult`.
    - Fix: `@cons-adult` (or a label on "When finger training makes sense") from the V6 guide and from the box, and `#tref("full-crimp")` from the key point.

19. **Tall notes that mention mobility without pointing to Part IV, and Part IV not pointing to its own tall-specific falling advice.**
    - Where: `04-body.typ:164` “Long thighs need a lot of hip turn-out” (frog) and `03-feet.typ:519` “which need knee and hip mobility” (heel hook) → "Mobility" in `@cons-tall`, as high-step's note does. `@cons-tall` has no pointer to `09-considerations.typ:353` “If you're tall, your body starts higher” or `09-considerations.typ:378` “If you're tall and heavy”.
    - Fix: add the pointers both ways.

20. **Small ones in chapters 8 and 9.**
    - `08-grades.typ:347` “Copy beta from climbers close to your height” → `@reading-size`.
    - `08-grades.typ:203` “Flash more” and `08-grades.typ:383` “Flash attempts” → `@reading-method`.
    - `08-grades.typ:311` “Missing a few techniques” links seven of the ten techniques it lists and leaves toe hooks, deadpoints and dynos plain. They are linked in the table above it, but this is the list a reader works from.
    - `09-considerations.typ:81` “Raise your feet” → `#tref("high-step")`, whose `small:` note has the method.
    - `09-considerations.typ:152` “Keep your shoulders set” → `#tref("latching")`.
    - `09-considerations.typ:266` “Don't test a deep drop knee, a full crimp or a big jump” → links to the three entries whose warnings it invokes.
