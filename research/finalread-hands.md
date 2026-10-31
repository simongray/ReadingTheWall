# Final read: chapter 5, Hands and holds

Page numbers are those of the current draft PDF. Text changes are in `book/chapters/05-hands.typ`; figure changes are in `figtools/figs_hands.py`.

## Text

- p. 98, 5.1: "The right side of a hold changes as you move" changed to "How well a hold works changes as you move", because "right side" could be read as a direction.
- p. 98, 5.2: removed the repeated "then" in "Part of your pull then runs along the surface. Then friction…".
- p. 104, Mantle step 2: the cross-reference used as a verb printed a capitalised "Heel hook" mid-sentence. It now reads "heel-hook".
- p. 128, Volume mantle step 2: same fix, "heel-hook its edge".
- p. 120, Gaston step 5: "or Side flag (p. 68)" changed to "or flag (p. 68)", as the verb is used in ch. 7.
- p. 115, Re-gripping summary: "how your hand holds a hold" changed to "your grip on a hold".
- p. 114, Pinch mistakes: "a narrow line" changed to "a narrow pinch", and "broad pinch" changed to "wide pinch", the entry's own term.
- p. 119, Wrapping summary: "an Arêtes (p. 182)" changed to "an arête (p. 182)", using the reference's body text.
- p. 120, Gaston look-for: "whose edge points at you" changed to "that face towards your middle", to match the hold-direction convention.
- p. 122, Pocket caption: "ring finger in the hole" changed to "middle and ring fingers in the hole", and "between them" changed to "between it and the ring finger".
- p. 128, Volume mantle caption (a): dropped "on its side", because the figure shows the high foot on a foothold below the volume.

## Figures

- `label_lines`: leaders now start at the edge of the label text. Before, they showed through the gaps between words, as in "thumb in" on p. 124.
- p. 105, mantle panel 2: re-posed with the shoulders over the lip, so the elbow points up and back as the label and caption say. Before, it pointed down at the waist. Moved the body arrow off the seat.
- p. 128, volume mantle (b): the "palm presses the top" leader pointed at the left elbow. It now points at the palm.
- p. 117, sloper (a): the plumb line ran through "hips pushed out". The label now sits under the arrow, and the plumb line stops above it.
- p. 117, sloper (a): moved "both feet high" lower, off the wall hatching.
- p. 117, sloper (a): moved "hand rolls off" away from the panel letter.
- p. 117, sloper (b): the plumb line crossed "hips low, under it" and "one foot low". The first is now split over two lines left of the plumb line, and the second is moved right of it.
- p. 117, sloper (c): "palm and pads on it" ran into the wall line. It is now "palm and pads", moved left.
- p. 121, gaston (b): the "thumb down" leader crossed the force arrow. The label now sits above the hand.
- p. 124, thumb catch (b): the "thumb pad presses up" leader crossed the force arrow. The label is now lower, with the leader going to the thumb's joint.
- p. 106 open hand (a), p. 126 full crimp (b): labels sat against the panel letter. They are now centred.
- p. 115, regrip (2): "half crimp in the incut" sat on the forearm outline. It is moved left.
- p. 109, undercling (a): "tips backward" changed to "tips backwards", as in the caption and the text.

## Handed back

- `hand.py`, `grip_pose("lock")`: the thumb sits about 1 cm inside the wall face in full crimp (b) on p. 126 and in the hand atlas's full-crimp tile on p. 99. Re-aiming the thumb from `figs_hands.py` didn't clear the wall. The thumb needs to cross the index finger in the model.
- p. 120, Gaston step 6: "Two gastons pushed apart make a stable squeeze. So do a gaston and a sidepull."
  - Pushing apart is not a squeeze.
  - The dossier marks the claim "(unverified)" (C-hands.md, line 769).
  - A gaston and a sidepull held on opposite sides pull the body the same way, so they don't oppose each other.
