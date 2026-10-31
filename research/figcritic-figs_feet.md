# Figure critic: figs_feet (chapter 03, feet and legs)

Every figure, filmstrip frame and atlas tile was rendered at 150–600 dpi after the switch to the clothed renderer. The build prints no warnings for this module.

Module-wide: `FootClimber`'s own profile shoes (and every close-up shoe drawn by `draw_shoe`) lacked the new rand and strap lines and the dotted x-ray outline under the trouser hem. `draw_shoe` now calls `shoe_details` through the toe bend and takes an `xray` flag, which `FootClimber._shoe` sets as the library does.

- **filmstrip-heel-hook**: the left elbow was clipped at the frame edge in frames 2–3; the left arm is shortened a little there (0.9/0.94, the elbow points back out of the wall). In frame 4 the right elbow folded inward across the back; the pressing arm is now drawn through an explicit elbow (up and back, `draw_arm`). In frames 4–5 the left foot stood on blank wall; a foothold (LF2) is added to every frame and used in both. The hooked heel floated about 1 cm above the jug; it now sits on the lip (`HEEL_ON`, shared with heel-hook). Frame 2's force arrow no longer ends on a hold.
- **heel-hook**: same heel fix; (b) drew the raised thigh over the shirt, as if it came out of the belly. The default draw order now puts it behind the shirt. Close-up shoe has the new details.
- **high-step**: (b) same thigh-over-shirt problem; default order.
- **rockover**: (1) the right elbow folded in across the back under the CoG symbol; the right hand now presses its hold, elbow up (explicit elbow, also in the ghost of panel 2). (2) the left foot stood on blank wall; a foothold added to both panels.
- **hand-foot-match**: (a) "press down" touched the left arm; now "press", left of the arrow.
- **toe-hook**: (a) the leader crossed the shoe and ended off the contact; the label now sits above the hold with a short leader to the toe–hold contact.
- **knee-bar**: the left hand gripped the volume edge in front of the chest, so the whole arm was hidden and only a knuckle showed. The volume's outer face now rises steeply away from the chest, and both arms hang (the left behind the right); the caption ("the right hand is free") still holds.
- **foot-swap**: the panel numbers sat on the grey shins (they fill the top-left corners); numbers moved to the top right, beside the wall.
- **bicycle**: "push" touched the wall line; moved left.
- **smearing**: shoes now detailed; the "more rubber" arrow touched the sole and its label the wall; both moved, close-up frames 3 units wider.
- **foot-atlas**: all shoes now match the climbers' shoes. Heel-hook tile: the force arrow lay on the shin; moved beside it. Knee-bar tile: the thigh contact sat at the tile edge and its arrow crossed the thigh; the composition moved right and the arrow now points from the contact into the volume. Smear tile: arrow moved off the sole.
- **edging, pivoting, front-pointing, heel-toe-cam, toe-pull, precise-footwork**: checked, no change beyond the shoe details.

Doubtful: the knee-bar volume is now a narrow wedge, and its leader crosses the volume. The top-view shoes (edging, atlas) are still the older closeup.py style, which reads as schematic beside the new profile shoes.
