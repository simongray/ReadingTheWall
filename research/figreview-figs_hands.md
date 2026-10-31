# Figure review: figs_hands.py (chapter 5, Hands and holds)

Close-ups now use a new hand drawn in `closeup.py`: forearm, palm, fingers and thumb as one clean outline seen from the thumb side, middle finger in grey behind, nails and joint creases, joint angles marked with a dashed "straight" line and an arc. No `warn()` messages.

- **hands-hold-angle**: a lone fingertip floating over each edge. Redrawn with a half-crimping hand on incut, flat and sloping edges, a pull arrow under each, "slides off" arrow on the slope. Short labels ("lip locks it").
- **jug**: checked; anatomy and labels fine. Unchanged.
- **open-hand**: (a) sausage-capsule finger with no hand; redrawn: middle joint ≈40° arc, end joint hooked over a rounded lip, relaxed thumb. (b) cartoon glove; redrawn face-on with knuckle wrinkles, little finger curled off.
- **half-crimp**: arcs hidden inside the finger, labels over the hand. Now (a) half crimp ≈90° arc, "end joint straight" leader from below; (b) full crimp "over 90°", "end joint bent back".
- **full-crimp**: (a) adds an A2 pulley band on the palm side; (b) face-on thumb lock (unreadable) replaced by a side view, thumb pad over the index nail. Caption (b) changed.
- **pinch**: face-on hands couldn't show opposition. Now seen from above (wall at top): thumb on one face, fingers on the other, squeeze arrows. Caption changed (adds "Seen from above"; (a) reworded to match the drawing).
- **regrip**: redrawn with the new face-on hand; ghost hand dashed. Layout unchanged.
- **wrap**: C-shaped band replaced by a real hand from above: palm and thumb on one face, fingers round the arête. Mirror image of the old one (palm on the right face).
- **pocket**: unclear hand. Now seen from the little-finger side: ring finger (grey) in a cut-away pocket, little finger parallel (a) or curled solid (b) with two opposite tendon arrows.
- **thumb-catch**: both panels now side profiles: (a) thumb pressing up into a dimple under a rounded edge; (b) thumb pad pressing up on a volume's lower face, fingers over the ridge.
- **sloper**: hold hidden behind the hand at climber scale. Added (c) close-up: open hand draped over a dome on the 20° wall, wrist below, pull arrow. Caption (c) added. Climber panels cropped so the figure is 163 mm.
- **sidepull**: (a) left leg kneeling below its foot, arm across the head. Rebuilt: hips under a higher sidepull, frog legs, barn-door rotation arrow. (b) unchanged apart from the moved holds. Convention checked: left hold faces left, body right, pull right, left foot pushes left.
- **gaston**: (b) arm folded flat onto the shoulder (hand at the shoulder). Arm now drawn with `draw_arm` (separate upper-arm and forearm foreshortening): elbow out at about hand height, thumb-down stub, push arrow right, body left. Convention checked.
- **undercling**: (b) the hold and the hand were hidden behind the knee. Right (near) hand now on the hold, hold drawn in front of the right leg, up-and-out force arrow; (a) "bent arms" leader moved off the head.
- **palming**: checked; fine. Unchanged.
- **mantle**: frame 3 had the centre of gravity 30 cm behind the hands and foot (would tip backward). Hips and shoulders moved over the lip. Frame 1 high foot was sole-up; now uses `flip`, pelvis lowered to keep the hip within range; redundant "high foot first" label dropped.
- **volume-mantle**: (a) face and hands overlapped; head moved back, label moved.
- **hand-atlas** (new): 10 tiles at 2.3 mm/cm, side profiles except the pinch (from above); undercling drawn mirrored (`MirrorFig`) because the hand helper only curls one way. Inserted before "V0–V1" in the chapter.

Doubtful: the gaston from behind is still a compromise (forearm points into the wall); the palm-press tile crops the forearm; the jug tile's bucket is partly hidden by the fingers.
