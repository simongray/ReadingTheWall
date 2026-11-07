# Hand proportions

The hand close-ups in `figtools/authored.py` follow these proportions, and
`tools/check_hands.py` tests every hand against them. Sizes are in cm of a model
hand 19 cm long, from the wrist crease to the tip of the middle finger. A
close-up prints at 2.6 mm to the cm.

## What the numbers say

- A wrist is a waist only from the back. From the side it's a quarter deeper
  than the knuckles.
- From the palm side a finger is shorter than the palm, 0.75 of it. From the
  back it's as long as the back of the hand, 1.04 of it.
- A finger's depth is about half the hand's at the knuckle, and about a third of
  the palm's with the ball of the thumb.
- A finger tapers more in depth than in breadth.
- The thumb is only a little wider than a finger.
- The hands have no view tilt. A tilt of 12° makes the palm a fifth deeper and
  leaves the finger as it was, so the fingers look thin.

## Ratios

Numbers for men come first, with women's in brackets where the source gives
both. The sources are listed at the end of this page.

| Proportion | Ratio | Source |
|---|---|---|
| Knuckle breadth ÷ hand length | 0.45 to 0.47 | Kouchi 2012, Gordon 2014 |
| Palm, crease to base of middle finger ÷ hand length | 0.58 | Kouchi 2012 |
| Hand depth at the middle knuckle ÷ hand length | 0.175 | Kouchi 2012 |
| Hand depth at the knuckle ÷ knuckle breadth | 0.385 (0.376) | Kouchi 2012 |
| Index and little knuckle depth ÷ middle knuckle depth | 0.86 and 0.81 | Kouchi 2012 |
| Index breadth at its middle joint ÷ knuckle breadth | 0.216 (0.215), or 0.23 to 0.24 in US hands | Kouchi 2012, Bradtmiller 2008, Hsiao 2015 |
| Index depth at its middle joint ÷ hand depth at the knuckle | 0.52 (0.53) | Kouchi 2012 |
| The same ÷ depth at the heel | 0.45 to 0.49 | Kouchi 2012 |
| The same ÷ depth with the ball of the thumb | 0.36 | Dixon 2012, weak |
| End joint ÷ middle joint, in depth | 0.77 (0.78) | Kouchi 2012 |
| End joint ÷ middle joint, in breadth | 0.87 (0.87) | Kouchi 2012 |
| Finger depth ÷ breadth | 0.93 at the middle joint, 0.83 at the end joint | Kouchi 2012 |
| Middle, ring and little finger ÷ index, in breadth | 1.01, 0.94, 0.83 | Kouchi 2012 |
| The same, in depth | 1.03, 0.96, 0.85 | Kouchi 2012 |
| Index, ring and little finger ÷ middle finger, in length | 0.90, 0.94, 0.74 | Kouchi 2012 |
| Middle finger's palm-side length ÷ palm from the crease | 0.75 (0.77), or 0.70 to 0.76 elsewhere | Kouchi 2012, Hsiao 2015, Gordon 2014 |
| Middle finger's back length ÷ back of the hand | 1.04 (1.05) | Kouchi 2012 |
| Finger with its knuckle at 90° ÷ back of the hand | 1.26 (1.26) | Kouchi 2012 |
| Back of the hand ÷ knuckle breadth | 1.08 (1.12) | Kouchi 2012 |
| Palm side ÷ knuckle breadth | 1.27 (1.30) | Kouchi 2012 |
| Middle finger's bones, base to tip | 1 : 0.65 : 0.44 | Pietak 2013 |
| Thumb ÷ index, in breadth | 1.12 (1.11), or 1.07 | Kouchi 2012, Hsiao 2015 |
| Thumb ÷ index, in depth | 1.03 (1.03) | Kouchi 2012 |
| Thumb from its base crease ÷ hand length | 0.33 | Kouchi 2012 |
| Thumb from its knuckle ÷ hand length | 0.30 | Kouchi 2012 |
| Wrist breadth ÷ knuckle breadth | 0.70 (0.69), or about 0.74 from its girth | Kouchi 2012, Gordon 2014 |
| Wrist depth ÷ wrist breadth | 0.70 (0.70) | Kouchi 2012 |
| Wrist depth ÷ hand depth at the knuckle | 1.27 (1.28) | Kouchi 2012 |
| Nail breadth ÷ fingertip breadth, thumb to little finger | 0.85, 0.78, 0.76, 0.74, 0.71 | Kouchi 2012 |
| Nail length ÷ end segment | about 0.6 | Kouchi 2012 |

Laid beside the index, the thumb's tip ends about 1 cm short of the index's
middle joint. That comes from the wrist-to-tip lengths in ANSUR 1988, and the
report doesn't state the posture.

## Sizes in each view

These are the ranges `tools/check_hands.py` tests. A measurement may miss a
range by the most the pen's wobble can move a line, which is 0.1 cm at 2.6 mm to
the cm.

| Measure | From the side | From the back | Palm press |
|---|---|---|---|
| Across the knuckles | 2.86 to 3.33 | 8.5 to 9.0 | 8.3 to 8.7 |
| At mid-palm | 4.5 to 4.9 with the ball of the thumb | 8.2 to 9.35 with the thumb's base | 7.9 to 9.15 |
| Wrist | 4.2 to 4.6 | 6.0 to 6.6 | 5.8 to 6.7 |
| Forearm, 5 cm below the wrist | 4.6 to 5.2 | 6.7 to 7.2 | 6.2 to 6.7 |
| Index, first segment | 1.75 to 2.25 | 1.9 to 2.25 | 1.85 to 2.1 |
| Index, middle segment | 1.55 to 1.73 | 1.75 to 2.03 | 1.72 to 1.95 |
| Index, end segment | 1.2 to 1.5 | 1.44 to 1.85 | 1.4 to 1.8 |
| Thumb, at its end joint | 1.9 to 2.4 | 1.8 to 2.1, edge-on | 1.9 to 2.2 |
| Finger length | index 8.54 to 9.68 | middle 8.24 to 9.68 | middle 7.58 to 8.9 |
| Thumb, free of the palm | 4.7 to 6.3 | 4.7 to 6.3 | 4.3 to 5.8 |
| Crease to webs, on average | | 9.9 to 10.9 | 9.1 to 10.05 |
| Finger ÷ mid-palm or knuckles | 0.36 to 0.43 | 0.21 to 0.26 | 0.21 to 0.25 |
| Thumb ÷ finger | 1.05 to 1.2 | 0.85 to 1.05 | 0.9 to 1.1 |

From the little-finger side, the palm is 3.4 to 3.9 deep with no ball of the
thumb in front, and the finger's sizes are the side's times 0.85.

The palm press is seen three quarters on, which multiplies breadth by 0.93,
depth by 0.37 and length along the hand by 0.92. The wrap multiplies breadth by
0.84 and depth by 0.54. A section with breadth B and depth D then looks this
wide, where a and b are the factors for breadth and depth:

    2 × (|B/2 · a|^m + |D/2 · b|^m)^(1/m)

For the palm, m is 1.5. Kouchi 2012 fixes that through how much thinner the hand
is at its outer knuckles, and an ellipse would make it thinner still. For the
wrist, forearm and fingers, m lies between 1.5 and 2, which is an estimate.

## Where the numbers are weak

- **Population.** The Kouchi 2012 hands are Japanese. Lengths carry over well,
  but against US hands they are about 4% narrower for their length, with fingers
  about 8% narrower against the hand. So a range often runs from the Japanese
  mean up to the US one.
- **Finger depth in Western hands.** No source here measures it directly. The
  range applies the Japanese depth-to-breadth ratio to the US breadths. Greiner
  1991 and Vergara 2017 would settle it, but neither could be fetched.
- **Forearm.** This is an estimate, from the wrist as a lower bound, girths in
  Gordon 2014 and a sensor study, and a depth-to-breadth of 0.72 to 0.80 from
  the cast index literature. Calipers on a forearm would settle it.
- **Depth with the ball of the thumb.** The only number comes from an
  unattributed student poster, Dixon 2012.
- **Mid-palm and webs.** No survey here measures either. Both are interpolated,
  and the webs' 10.4 from the palm lengths carries an allowance of 0.5 either
  way.
- **Climbers.** A [2022
  review](https://pmc.ncbi.nlm.nih.gov/articles/PMC9778768) reports thicker
  tendons, pulleys and bone in climbers' fingers but gives no outer finger size.
  That's a reason to sit toward the top of a range, and no more.

## Sources

The footer of the AIST data reserves all rights and forbids reproduction without
written permission. So this page gives ratios and the model's own sizes, and
never its table. Cite it as Kouchi 2012.

- **Kouchi 2012.** [AIST Japanese hand dimension
  data](https://www.airc.aist.go.jp/dhrt/hand/index.html): 327 men and 203
  women, one measurer, calipers. It's the only open source with every joint,
  depth and nail, and the backbone of this page.
- **Gordon 2014.** [ANSUR
  II](https://tools.openlab.psu.edu/publicData/ANSURII-TR15-007.pdf): 4082 men
  and 1986 women of the US Army. It gives hand length, breadth, palm and wrist
  girth, and its Table 20 repeats the ANSUR 1988 means for wrist to thumb tip
  and wrist to index tip.
- **Bradtmiller 2008.** In [FAA HFDS Appendix
  B](https://hf.tc.faa.gov/hfds/download-hfds/hfds_pdfs/App_B_Tech_Ops_Anthropometrics.pdf):
  1244 US staff. It gives index breadth at the middle joint.
- **Hsiao 2015.** [Firefighter hand
  anthropometry](https://stacks.cdc.gov/view/cdc/201534/cdc_201534_DS1.pdf): 863
  men and 88 women. It gives every finger's breadth and length.
- **Pietak 2013.** [Pietak et al., J
  Anat](https://pmc.ncbi.nlm.nih.gov/articles/PMC3633342): the bones of 30 third
  digits, read through a summary only.
- **Dixon 2012.** [Anthropometry of the
  hand](https://s3images.coroflot.com/user_files/individual_files/429958_COGfmXYQaClvmUqtejARC0gqW.pdf),
  a poster with no citations.
- **Could not be fetched.** [Greiner
  1991](https://apps.dtic.mil/sti/tr/pdf/ADA244533.pdf) has 86 hand dimensions
  of US adults, and [Vergara
  2017](https://repositori.uji.es/xmlui/handle/10234/169487) has 99 finger
  dimensions of Spanish adults. Both would open in a browser.
