# Figure review: closeup.py

New helpers (old `finger_chain`, `place_chain`, `draw_hand_side`, `wall_strip`, `edge_side`, `SHOE_TOP` and the `R_*` constants are unchanged, since `figs_dynamic` and `figs_feet` import them):

- Profile hand: `finger_from_tip`, `finger_from_mcp`, `finger_ik`, `thumb_pose`, `palm_point`/`palm_coords`, `draw_profile_hand`, `draw_finger`, `flex_arc` (Kettle-style joint angle).
- Grips in profile: `wall_profile`, `edge_profile`, `rounded_lip`, `profile_frame`, `grip_hold`, `grip_pose`, `grip_profile` (moved here from figs_hands so both modules share them).
- Face-on hand: `hand_back` with `straight`, `to_height`, `knuckle_up`, `curled`; `ghost=True` for an earlier position.

Figures:

- **grip-crimps** (not in the book at present): three capsule fingers with no hand and no angles. Redrawn with the shared grip poses: open hand ≈40°, half crimp ≈90°, full crimp over 90°, arcs on the middle joint.
- **foot-edges**: not used by the book; left unchanged.
