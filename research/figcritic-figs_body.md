# Figure critic: figs_body (chapter 04, body positioning)

Every figure and every filmstrip frame was rendered at 150–400 dpi and checked against the critic pass in `ILLUSTRATION.md`. Joint angles were measured with a scratch script that logs every drawn climber, ghosts included. The build now prints no warnings for this module. The climber renderer was being rewritten during the pass, so the review covers poses, holds, labels and arrows, not body shapes.

- **filmstrip-drop-knee**: in frames 3–4 the right knee was folded to 55° with the foot near hip height. The dropped shoe also pointed back along the shin, so the ankle was folded flat. Frame 5 had a 48° knee pointing against its toes. Frames 1–2 clipped the left elbow and knee at the frame edge. Rebuilt on one hold set: the high foothold now sits lower and farther out (44, 84). The dropped foot points down with the heel up and the sole facing out. The thigh is foreshortened (it points into the wall), so the knee opens to 68–71°. Frame 2 shows a toe placed on the hold, heel-on, with the knee out; its caption is now "right toe on the high hold", as the how-to describes. Frame 5 shows the knee turned back up, with the thigh foreshortened toward the wall, at 92°. The knee-drop arrow now runs beside the thigh, not on it.
- **drop-knee**: (b) had the same foot folded back along the shin. The foot now points down, sole out, and the foothold is lower, so the knee drops below it at 70°. The force arrow sits by the foothold. (a): hips raised a little, X moved beside the reaching hand.
- **hip-turn**: (a) the left knee knelt at foot height with a horizontal shin, because an inside edge pushes the ankle right of the hold. The left toe now points into the wall (heel-on view), so the leg reads as a frog.
- **backstep**: (b) the hand hung bent beside the face. The arm now stretches toward the hold and stops 24 cm short, with the X in the gap.
- **back-flag** and the barn-door (b) climber: the left forearm crossed the head; the elbow now goes out. The legs cross by design, so `allow_cross=True`.
- **inside-flag**: (b) the knee pointed against its toes; the knee now bends to the left. The legs cross by design (`allow_cross`). The label sat on the foothold, so the frame grew downward and the label sits below the feet.
- **twist-lock**: (a) the left shin crossed the right thigh. The right foothold is 14 cm higher and the hips are a little higher, so the legs no longer cross and the knees are at 116°/142°.
- **cross-through**: the arms cross by design (`allow_cross`). The right knee pointed against its toes (foot on its outside edge); it now drops in, like a backstep.
- **compression**: the toes pointed inward while the knees pointed out, a twist no knee allows. Now a frog: knees out, toes into the wall (heel-on), inside edges on the volume's faces.
- **layback**: the shoes pointed into the flake. They now lie flat on it as smears, a little lower, and the "feet push in" arrow moved below the shoes.
- **stemming**: the label sat on the upper arm; moved up.
- **body-tension**: (a) the swing arc and its text ran across the feet. The arc now passes under the feet with a short label beside it.
- **pre-loading**: (a) a knee pushed into the wall; the shoulders moved 4 cm out. (b) two labels were stacked; "heels low" now sits under the foot.
- **opposition**: the arms were folded to 61° and the label touched the head. The holds are wider, the hips higher, the label higher.
- **frog, flag, lock-off, matching, bumping**: checked, no change.

Still doubtful: the drop-knee feet are drawn pointing down. That is the best profile shoe for a foot on its outside edge with the toes into the wall, but it is a convention. In twist-lock (a) the body leans far out on the straight arm, which the text asks for, but it looks dramatic.

## Re-check in the new renderer (clothed climbers)

- **twist-lock**: `_arm` now calls `Climber.draw_arm`, so the locked arm matches the new style (the segment-length check stays). "elbow to ribs" sat on the wider turned torso and right thigh. It is now smaller, beside the torso, and the panels are 8 units wider (121 mm overall).
- **hip-turn, backstep**: the reaching left arm hid the head of the turned climber; the head now sits 5 cm to the right, clear of the arm.
- **pre-loading** (b): the straight arm hid the face; the head tips back.
- **filmstrip-drop-knee** frame 5: the empty start jug showed a dotted outline through the right arm; its x-ray is off in that frame.
- **drop-knee**: labels checked against the wider turned torso; all clear. No leader in this module targets the grey left arm.
- Everything else looked at again at 150 dpi: no odd hems, folds, faces or ghosts.
