# Evidence for the third revision

Checked on 2026-11-06 for the corrections in `research/REVISE-3.md`. Each
section gives where the item applies, how the source was read, the checked
facts and replacement wording. Wording uses keys that exist in the source files.
Chapter editors may reshape the rhythm, but shouldn't say more than the wording
says. `#ix` markers are kept where the original had them.

Paths are under `book/chapters/`. "Abstract" means only the abstract was read.

## New and changed source keys

| Key | Source | Use |
|---|---|---|
| G3 | Mermier et al. 2000 (was a blog about it) | ch9 lines 17, 57, 79 |
| G67 | McKay et al. 2024, Psychological Bulletin | ch9 line 171 |
| G68 | Faggian et al., J Sport Health Sci (review) | ch9 lines 77–81 |
| G69 | Saul et al. 2019, J Exerc Sci Fit (review) | ch9 lines 77–81 |
| G70 | Gibson-Smith et al. 2024, Front Nutr | ch9 lines 77–81 ("no trials") |
| G71 | Exel et al. 2023, Front Sports Act Living | ch1 lines 26, 28 |
| G72 | Schöffl I. et al. 2009, J Biomech | not used in the wording (see item 10) |
| G73 | Grønhaug 2019, BMJ Open Sport Exerc Med | ch9 lines 77–81 |
| G74 | Backe et al. 2009, Scand J Med Sci Sports | ch9 lines 77–81 |

Metadata fixes: G19 (article number), G28 (issue, article number), G52 (note),
E34 (issue), E40 (article number, current URL), C25 (volume, article number), F15 (note:
the post quotes a blog, and how the blog gets its figures), G5 (note: the paper's sample).

This document didn't run `tools/merge_sources.py`. G68's DOI is also H14 in
`research/H-sources.yml`, and `book/src-map.typ` now maps H14 to G68. No other new
DOI appears in another source file, so G73 and G74 add no new mapping.

## Pages that could not be read

Each of these showed a bot check or a block. They were recorded and not bypassed.

| Source | What happened |
|---|---|
| G3 Mermier, PDF | PMC serves a proof-of-work check; Europe PMC's PDF link and BMJ show Cloudflare checks; the Europe PMC full-text API returns an error |
| E34 Sanchez, PDF | The Groningen repository page opens, but its PDF link shows a Cloudflare check (tried again 2026-11-06); the Liège copy is on request only |
| D1 theCrag | Cloudflare block. Read from search excerpts only |
| B23 UKClimbing | Cloudflare check. An earlier fact check found it paywalled. Not read |
| Diez-Fernández, Sustainability | MDPI returns 403. Abstract read on RePEc |
| E6 Mckellar, Europe PMC PDF | Cloudflare check. Not needed: the journal's own PDF at the E6 URL opens |

G4 Laffaye has no open copy (Unpaywall). Abstract only.

---

## 1. Mermier et al. 2000 (G3)

**Applies to:** `09-considerations.typ:17`, `:57`, `:79`.

**Read:** abstract (Europe PMC, PMC). Full text could not be read (see above).
Points marked "secondary" come from the blog that G3 used to cite (Shaul, Mountain
Tactical Institute).

**Facts**
- 44 climbers, 24 men and 20 women, self-reported 5.6–5.13c, 0.10–44 years of
  experience.
- Two routes on separate days, 11 m and 30 m, on artificial walls, getting harder
  from start to finish.
- Scoring: as in sport-climbing competitions, each handhold further scores one
  more point. The two routes' scores were combined.
- Rope: the abstract doesn't mention one. Secondary: both routes on top rope.
  Routes of that height are not bouldering, so "rope climbers" is reasonable, but
  the abstract only supports "two indoor routes of 11 and 30 m".
- Method: principal components analysis, then simultaneous multiple regression.
  Three components, labelled training, anthropometric and flexibility.
- 58.9% (training, "uniquely" explained), 0.3% (anthropometric), 1.8% (flexibility)
  of the variance in performance: confirmed.
- Pages: 359–365, with a discussion on p. 366 (PubMed lists "359-65; discussion
  366"; Crossref 359–365).

**Normalised to body mass?** Could not be checked in the paper. Secondary: the
blog lists relative grip strength, normalised to body mass, among the strongest
predictors in the training component. If that is right, body mass partly sits
inside the 58.9%, so 0.3% doesn't measure the whole effect of weight.

**The training component isn't purely trainable.** The abstract lists self-reported
climbing rating, years of experience and weekly training hours among the variables
combined into components. Secondary: self-rated ability and years of climbing load
on the training component. A self-rated grade predicting a climbing score is partly
circular. Say "a factor the authors labelled training", and avoid "trainable" for
this study.

**Wording, line 17 (first study only)**

> In a study of 44 climbers, scored on two indoor routes of 11 and 30 m rather than on boulder problems,#ix("Studies!body shape and ability") a factor the authors labelled training explained 58.9% of the differences in their scores. Body measurements, such as height, arm span and weight, explained 0.3%. Self-rated grade and years of climbing also went into the analysis, so the training factor may partly measure experience #src("G3").

The old parenthesis "(strength, endurance, power and experience)" comes from the blog, so it is
dropped until someone can read the paper. The abstract confirms that those two variables went in.
Only the blog says which component they loaded on, hence "may".

**Wording, line 57:** change "explained only 1.8% of ability in the study above" to
"explained only 1.8% of the differences in score in the study above #src("G3")". Change the next
sentence, "It opens positions; it doesn't win grades", to "It opens positions, but this study gives
no sign that it adds grades." One figure from long routes can't carry a rule about flexibility, and
G68 says firm conclusions can't yet be drawn.

---

## 2. Laffaye et al. 2016 (G4)

**Applies to:** `09-considerations.typ:17`, `:79`.

**Read:** abstract. No open copy.

**Facts**
- 41 climbers: 15 novice, 16 skilled, 10 elite. The book's "41 climbers, from novice
  to elite" is right.
- Method: principal components (three, labelled training, muscle, anthropometry,
  together 64.22% of variance), then multiple regression.
- Trainable variables explained 46%; anthropometry and muscle characteristics
  explained under 4%. The book's numbers are right, but "trainable" is the authors'
  label, as it is in Mermier's conclusion. The abstract doesn't say which variables it covers.
- Normalised to body mass? The abstract doesn't say. A later review (G68) reports
  this study's finger force as an absolute value, r = 0.72, with male climbers. That
  is indirect, so don't state it in the book.

**Wording, line 17 (second sentence, so that both studies read alike)**

> In a study of 41 climbers, from novice to elite, what the authors call trainable variables explained 46%, and body shape and muscle together under 4% #src("G4").

---

## 3. McKay et al. 2024 (new G67) and Wulf 2013 (G52)

**Applies to:** `09-considerations.typ:171`, the heading at `:165`, `a-glossary.typ:74`.

**Read:** abstract (Europe PMC, and the SportRxiv preprint page). G52: Crossref
record, abstract excerpts from a search, and the earlier reading in factcheck-3.
The publisher's page returned 403 this time.

**Facts**
- DOI 10.1037/bul0000451. Psychological Bulletin 150(11):1347–1362.
- A re-analysis, using robust Bayesian meta-analysis, of the data behind the most
  comprehensive of seven earlier meta-studies, all of which favoured external focus.
- Moderate to strong evidence of publication bias in every analysis.
- Bias-corrected mean effects: performance g = 0.01, retention g = 0.15, transfer
  g = 0.09, electromyography g = 0.06, distance effect g = −0.01. The authors call
  these negligible.
- Bayes factors favoured the null in each analysis, from BF01 = 1.3 for retention
  (weak) to 5.75 for performance.
- Heterogeneity: clear in every analysis. The authors read it as the effect depending
  on contextual factors nobody has identified yet.
- Conclusion: the results contradict the consensus that external focus is always
  better. Effects vary, and on average are small to nil. This doesn't say external
  focus never helps.
- G52 metadata is right: Int Rev Sport Exerc Psychol 6(1):77–104. It argues that
  external focus is consistently better. The G52 note no longer says "abstract not
  accessed" (factcheck-3 asked for that) and points to G67.
- A targeted Europe PMC search for external or internal focus in climbing found no
  study that tests it, so "We found no climbing study of it" still stands.
- The re-analysis isn't of Wulf 2013. It uses the data of the most comprehensive earlier meta-study.
- The cue examples at line 171 come from this book's dossier (`G-considerations.md` section 4.4,
  marked judgement), not from Wulf.

**Wording, line 171**

> - *Try thinking about the hold, not your body.* In research on how people learn movements, a 2013 review found that an #jt("external focus"), a cue about the effect of a move, beats a cue about the body #src("G52"). In climbing that might mean "push the foothold down into the wall" instead of "straighten your knee" (this book's examples). A 2024 re-analysis of this research allowed for studies with no effect going unpublished, and found the average advantage small to nil. The effect varied between studies for reasons nobody can yet explain #src("G67"). We found no climbing study of it. So treat a hold-focused cue as something to try: use the body-part steps in this book to set up a position on the ground, then climb with one cue in mind and keep it if it helps (this book's suggestion).

"Small to nil" is the authors' own summary. It fits retention, the measure closest to learning
(g = 0.15, BF01 = 1.3), better than the brief's "close to zero" does. This departs from the brief, so
**Simon needs to confirm it.**

**Wording, `a-glossary.typ:74`.** The current "It usually helps learning" contradicts line 171.

> #gloss("external focus")[Attending to the effect of a movement (e.g. "push the wall away") rather than to your body. Studies disagree on how much it helps, so treat it as something to try.]

**Heading, `09-considerations.typ:165`:** "Principles that work" no longer fits this bullet. Use
"Principles to try".

---

## 4. Sanchez et al. 2012 (E34)

**Applies to:** `02-reading.typ:17`.

**Read:** abstract (Europe PMC and the coachsci page). Full text could not be read.

**Facts**
- 29 male climbers: intermediate, advanced and expert groups.
- Two indoor sport routes at their level and, where applicable, routes below it. One
  route at each level was climbed after a 3-minute preview.
- Roped: "indoor sport routes" means rope climbing, which fits the brief. Lead or top
  rope isn't stated in the abstract. Say "roped", no more.
- Finishing: preview didn't change route completion.
- Stops: the abstract first says climbers made fewer and shorter stops after a preview.
- Its next sentence, on allowing for baseline ability, can be read two ways. Either both differences
  held and the shorter stops held only for experts, or only stop duration still differed, with experts
  gaining most. The coachsci page takes the first reading, but it is another reader's summary of the
  same abstract. The full text could not be read, so the wording doesn't choose.
- The abstract reports no measure of time on the arms. "Less time hanging on your arms" was the book's
  inference, and it rested on an effect that may not have survived the adjustment. It is cut.

**Wording, line 17**

> - *Reading changes how you climb.* In one study, 29 male climbers on roped indoor routes had three minutes to look at some routes before they climbed them. Looking did not change how often they reached the top. They did make fewer and shorter stops. Part of that held up once the authors allowed for ability, with the experts gaining most#ix("Studies!previewing a route") #src("E34").

---

## 5. Mckellar et al. 2023 (E6) and Winkler et al. 2022 (E40)

**Applies to:** `02-reading.typ:20`, `:184`, `:186`, `:202–204`, `:221`, `:225`. Line numbers are edition 2's, so
match on the quoted text.

**Read**
- E6: full text. Europe PMC's XML (PMC10170546) has the text and tables, but only the captions of the
  figures, so Figures 2 and 3 were read from the journal's PDF at the E6 URL. Supplementary tables 1–3,
  which list the problems in each group, were not seen.
- E40: full text (Europe PMC XML, PMC8980921). Methods, bouldering and limitations closely; speed, lead
  and combined more quickly.
- White and Olsen 2010 (E39): abstract only, plus E40's summary of it. Needed only for `:221` and `:225`.

**Facts, E6**
- Who: the finalists of all seven 2019 World Cups, 20 men and 18 women, six per sex at each event. The
  authors call them professional. 56 problems, 336 climbing periods. Nothing on any lower level.
- Format: a 2-minute group preview, then 240 seconds per problem, with rests taken inside that limit.
- Groups: slab means a wall past vertical. Slab-like means a slightly overhanging wall where large volumes
  make climbers mostly push, or where they can go hands-free. Non-slab means an overhanging wall that isn't
  slab-like, and "steep" is this book's plain word for it. Some problems fit neither group.
- Attempts: 3.7 ± 2.4 per problem (range 1–13). Climbers who finished did so on attempt 2.3 ± 1.4 (range 1–9).
- Times: an attempt lasted 19 ± 18 s, a successful one 40 ± 18 s. Rest between attempts was 28 ± 18 s
  (non-slab 30 ± 20, slab and slab-like 22 ± 12).
- Success rate: tops divided by the climbers who took that attempt. The percentages are printed on Figure 2.
  The counts were read from its bars by this document and may be one out. With attempts 10–13 they reach the
  paper's 809 and 290 attempts and reproduce the printed percentages. Non-slab tops sum to 103, one short of
  the paper's overall 12.9%.

  | Attempt | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
  |---|---|---|---|---|---|---|---|---|---|
  | Non-slab | 21% (45/216) | 15% (25/171) | 13% (18/140) | 9% (9/103) | 6% (4/68) | 2% (1/46) | 0/31 | 0/17 | 13% (1/8) |
  | Slab/slab-like | 15% (12/78) | 22% (14/65) | 22% (11/50) | 6% (2/32) | 4% (1/26) | 18% (3/17) | 0/9 | 0/7 | 0/5 |

- No test: the paper calls these rates trends and runs no statistical test on them. The slab rise is two more tops
  on a smaller pool (12/78 to 14/65), so it shows little on its own.
- Steep problems: the authors say the first attempt is the best chance and tell finalists to prioritise it.
  The book's line 184 reports this correctly. The chance was still only about one in five.
- Slab: "steadier" follows one of the authors' sentences, but another says the rate rose from attempt one to
  two and stayed up at three, as the table shows. The wording says it rose. The authors suggest a practice
  effect on slab, with fatigue outweighing it on steep walls. They tested neither.
- Selection: the authors list a narrower effect as a limitation. Skill probably skews the success rates, because better climbers
  succeed on earlier attempts and reach more finals. Their models of attempt and rest times allow for this, but
  the success-rate figures can't. That is the authors' whole point. They don't argue that the climbers left on a
  problem are those it suits least, and their methods call each rate the "relative chance of success" at that
  attempt. The argument about who is still trying is this book's reading, so the wording labels it (judgement).
  "Suits least" is the brief's wider phrase, covering style and size as well as skill. It is a tendency, because
  after one failure most of the field is still trying (171 of 216 non-slab climbers). The pool also shrinks by more
  than the tops: of the 122 non-slab climbers who failed a third attempt, 103 took a fourth (this document's
  arithmetic). The paper doesn't say why the others stopped.
- Six attempts: only one climber finished after a sixth attempt, on a ninth, which the authors treat as an outlier.
  So line 204 is right. They call six a hard cut-off for tops in finals, and say the study can't determine an ideal
  number. "Four to six" isn't in the paper. Four is this book's addition.

**Facts, E40**
- Who: one 2018 World Cup (qualification, semi-final and final) and the 2018 World Championship final. 20 women
  and 24 men, international elite. The bouldering figures are descriptive, with no statistical tests.
- **"2018 World Cups" at `:186` and `:221` is wrong.** There was one World Cup and one World Championship final.
  Line 20's two rounds both come from that World Cup, so it should say "one 2018 World Cup".
- Format: 5 minutes per problem in qualification and semi-finals, 4 in the final. A 2-minute group preview comes
  only before the final.
- Table 3, in seconds. The successful and failed ranges at `:186` are right. So are "about 30 seconds" at `:221`
  (32.2 overall) and "about 50 seconds" at `:20`.

  | Round | Successful attempt | Failed attempt (median) | Rest between attempts | Before first attempt |
  |---|---|---|---|---|
  | Qualification and semi-final, women | 39 | 21 (18) | 35 | 47 |
  | Qualification and semi-final, men | 32 | 13 (8) | 34 | 51 |
  | Final, women | 39 | 12 (6) | 22 | 16 |
  | Final, men | 31 | 16 (12) | 32 | 20 |

- The study doesn't record where climbers fell. Medians as low as 6 s could seem to rescue "end early", but they
  measure time, and a failed attempt stops at the fall.
- The authors say these figures suit high-level athletes, and that lower-level climbers should go by the demands
  of their own climbs.

**Facts, E39**
- Six elite men at a UK national event, on two problems. Rest between attempts was 114 ± 31 s, so "about 2 minutes"
  at `:221` is right.
- The abstract gives no time limit. Its averages of 3.0 attempts at 28.9 s with 114 s rests already come to more
  than five minutes, so "four or five minutes" at `:225` doesn't describe it.

**Wording, line 20**

> - *Good climbers take time over it.* In the qualification and semi-final rounds of one 2018 World Cup#ix("World Cup!time spent reading"), boulderers looked for about 50 seconds before their first attempt #src("E40").

**Wording, line 184**

> *Flashing.* In a study of the 2019 World Cup#ix("World Cup!success by attempt") finals, the first attempt on a steep problem succeeded about 21% of the time. The rate fell with each try, to 6% on the fifth, and the authors call the first attempt a finalist's best chance there. On #tref("slab", body: [slab], show-page: false) and slab-like problems the rate rose, from about 15% on the first to 22% on the second and third. The authors ran no statistical test on these rates and warn that skill probably skews them, because better climbers finish earlier. Finalists also rest very little, about 30 seconds between tries #src("E6"). The climbers still trying after a failed attempt tend to be those the problem suits least, so these rates can't show that your own chance falls after one try (judgement).
>
> You only get one flash and your arms are at their freshest, so on steep problems put everything into the first try (judgement). On slab, a failed first try costs you less (judgement).

Three things here shouldn't change when an editor reshapes the rhythm. The selection effect comes after the last
`#src("E6")` and carries its label, because it is this book's reading and the authors don't make it. The skew sentence
says "rates", because the authors' models did allow for skill in rest and attempt times. The advice stays "(judgement)",
because the authors' advice is aimed at finalists. "A first look" became "a failed first try", because in this chapter a
look is what you do from the ground. The paragraph break separates the data from the advice and adds no words.

**Wording, line 186**

> Your flash routine#ix("Flashing!routine"), built from the steps above:

The figures go. With the inference deleted, they support nothing in the routine, and nothing else in the chapter
depends on them. E40 stays cited at lines 20 and 221. The advice dropped with the inference is already at line 72
("Expect some near the start (judgement)"). The wording doesn't print the brief's reason, "shorter by definition",
because in seconds it isn't true: failed attempts in women's qualification and semi-finals took 21 ± 14 s against
39 ± 14 s for successful ones, so the two overlap. The chapter editor's errata line can still record that the "2018 World
Cups" label and the inference are gone. Table 3 above keeps the figures if Simon wants them back.

**Length.** Together these lines grow by about 100 words (284 to 385, counting markup). Line 184 adds 105, because it
now reports the authors' conclusion, their skew and the book's reading separately. Line 204 adds 30, of which the
selection effect is 15 and the authors' cut-off 6. The brief doesn't require the selection effect at line 204, but the
6% figure is the one most exposed to it. Line 186 falls to 8 words (−35) and line 202 loses 9. Lines 20, 221 and 225
add 2, 6 and 2.

**Wording, line 202 (keypoint)**

> #keypoint[After four to six full attempts#ix("Projecting!how many attempts") without progress, change something (judgement). Rest longer, change the sequence or stop for the day.]

**Wording, line 204**

> The six-attempt figure comes from elite competition. In the 2019 World Cup finals, only one climber finished a problem after a sixth attempt. On steep problems the fifth attempt, after four failures, succeeded only 6% of the time. The authors treat six as a cut-off and say they can't name an ideal number #src("E6"). The climbers still trying by then tend to be those the problem suits least, and they rest little between tries, so treat four to six as a rule of thumb (judgement).

**Wording, line 221 (table row)**

> [What competitors actually do under a time limit], [About 2 minutes (a national event, 2010 study); about 30 seconds (a World Cup and the World Championship final, 2018)], [#src("E39", "E40")],

**Wording, line 225 (first sentence, and the two sentences on competition figures)**

> So an hour at your limit holds only about four to six full attempts, each made at full strength.

> The 2018 figure describes athletes with four or five minutes per problem. Neither figure is advice.#ix("World Cup!rest between attempts")

"About six" took only the short end of the table's 10–15 minutes, and at 15 minutes it is about four. This is
arithmetic on the E42 row, not a number from E6 or E40. The row at line 221 has one 2018 figure and one 2010 figure,
which is why "figure" is singular and then "neither".

**Flags for other editors**
- `a-troubleshooting.typ:145` cites E6 for the rule. E6 doesn't give it, so say: "After four to six failed tries,
  change the sequence or stop (judgement). See Chapter 2 #src("E41", "E42")."
- `a-card.typ:25` repeats the rule with no citation and can stay.
- `07-terrain.typ:370` cites E6 for modern gym slab being jumps and catches. E6 says nothing about gyms. It counts
  coordination moves across all styles, and says slab is thought to need precise, controlled movement. Drop E6
  from that sentence.
- `07-terrain.typ:129` puts the citation on "Climb it as a slab", which E6 doesn't advise, and E6's slab-like walls
  are slightly overhanging, not vertical. Under `*Look for*`, say: "a near-vertical wall with big volumes where you'll
  mostly push #src("E6"). Climb it as a slab."
- `07-terrain.typ:13` and `:369` match the paper, so `sources:` keeps E6.

---

## 6. Gilmore et al. 2024 (G28)

**Applies to:** `09-considerations.typ:142`.

**Read:** full text (Europe PMC XML).

**Facts**
- Design: retrospective, from logs in the Crimpd app, September 2022 to December 2023.
  Self-selected training, not randomised, self-reported. Two strength tests 4–16 weeks
  apart.
- Number: 526 in the results. The methods give 506 men and 21 women (527) and the
  grade counts add to 524. Use 526.
- Level: intermediate 54, advanced 432, elite 38, by self-reported boulder grade.
  **No novices.** So this study doesn't itself test the heading's "start earlier".
- Selection: the initial cohort was climbers with at least 30 Abrahangs workouts. That comes from the
  Methods text. Figure 2 wasn't seen, so how the filter applied to each group isn't known. The paper
  also says those choosing Abrahangs may differ in why they chose it.
- Protocol name: "Abrahangs" is the label the paper says it uses for the study. The app
  calls it "Emil's Sub-max Daily Fingerboard Routine".
- Session: 10 minutes, 20 hangs of 10 seconds with 20 seconds' rest, feet on the floor,
  on an 18–22 mm edge. Group cut-off: at least 3 workouts a week.
- "A small strain": confirmed, as the app's cue. The paper says only of the Abrahangs group that
  the load was self-regulated, unsupervised and not measured.
- Max Hangs group: the climber sets the load at 85%, 90% or 95% of a tested 1RM, also self-run and
  unsupervised. Six 10-second hangs, at least 0.5 workouts a week.
- Results, mean change in strength-to-weight ratio: Abrahangs 2.5%, Max Hangs 3.2%, both 5.8%.
  No statistical difference between Abrahangs and Max Hangs. The authors call this similar and
  "equivalent", but ran no equivalence test, so say only that the gains didn't differ significantly.
- **Abrahangs p = 0.1216, not significant, which the paper calls a positive trend.** That sentence
  names no comparison group. This document reads it as climbing only, because the next sentence names
  that group for Max Hangs and the effect sizes use it. "Not significantly bigger" rests on that
  reading. Effect sizes against climbing only: 0.29, 0.45, 0.79. Max Hangs compared with climbing only:
  p = 0.0005. Within-group rises before and after were significant in all three training
  groups.
- Climbing only: no change (p > 0.99). But this group means below the cut-offs, under 3
  Abrahangs and under 0.5 Max Hangs a week, not zero. Climbing volume and other finger training
  weren't tracked. So "climbing alone gave no gain" and "did little finger training" both claim too
  much.
- The authors' warning: maximal hangs may carry a risk of finger overload, especially for
  novices with little loading history. They also list non-randomisation, belief effects,
  self-reported data, possible selection bias and unmeasured load as limitations, and ask
  for a prospective study.
- Competing interests: the paper states that EA created the Abrahangs protocol and PK
  designed the Crimpd app. Emil Abrahamsson is a co-author and conceived the study with
  KB. Background section: he designed it with his brother Felix, drawing on the
  co-authors' lab work. This is firmer than the brief's "associated with". The paper
  doesn't explain where the name comes from, so don't state that.

**Wording, line 142 (replaces the G28 sentences only)**

> One retrospective study used the logs of 526 users of the Crimpd training app.#ix("Studies!fingerboard training") Climbers chose their own training and ran it unsupervised, and nobody measured the load on the gentle hangs, so it isn't proof. The study also started from climbers who had logged at least 30 gentle workouts. The gentle protocol, which the paper calls "Abrahangs", takes about 10 minutes: 10-second hangs with the feet on the floor and only "a small strain" in the forearms. The paper declares that its co-author Emil Abrahamsson created the protocol and that another co-author designed the app. Strength relative to bodyweight rose by 2.5% on average with gentle hangs and by 3.2% with near-maximal hangs, and those gains didn't differ significantly. The gentle gain also wasn't significantly bigger than the result for climbers below the study's cut-offs (under 3 gentle or 0.5 maximal sessions a week). Those climbers showed no change over the 4–16 weeks, though nobody tracked their climbing or their other finger training. Doing both protocols added up (5.8%). The users were intermediate to elite, so the study says nothing direct about novices. The authors warn that maximal hangs may overload novices #src("G28").

**Flag for Simon, keypoint at `:147`.** "Two or three short sessions a week" is this book's suggestion.
It overlaps the study's climbing-only group, which covers anything under 3 gentle sessions a week,
while the gentle group logged at least 3. So G28 doesn't support that dose, and it gives none for
novices. Either say "three", or say that the lower dose is this book's caution.

---

## 7. Lutter et al. 2020 (G9)

**Applies to:** `09-considerations.typ:50`.

**Read:** full text (open copy at the G9 URL).

**Facts**
- Design: retrospective multicentre case series, level 4 evidence, 2015–2018.
- Clinics: two specialised outpatient sports medicine clinics, referral centres for climbing
  injuries. One is a trauma centre in a popular German outdoor climbing area. The other lies between
  climbing destinations in Utah, USA.
- 71 patients, 77 injuries, 35% competitive. Heel hook 40.3%, ground fall 22.1%, high
  step 20.8%, drop knee 16.9%. Indoor bouldering 46.8%. Medial meniscal tear 28.6%.
- Denominator: none. No count of how often climbers use each move. The authors say no
  conclusion can be drawn on incidence among climbers at large.
- Diagnoses were clinical and radiological, and the senior author reviewed them. Only the mechanisms
  come from athletes' descriptions, and those could not be verified. The authors
  suspect severe knee trauma often goes to the nearest hospital, so it may be undercounted.
- Book's "the authors suspect" (a hand letting go, the other foot slipping): supported.
- Weight: the book's line 79 says the study guesses that weight and age play a part in
  meniscus tears. The paper says only that lower age and body weight in the competitive
  group might influence why it had fewer operations. See item 8 for wording.

**Wording, added after line 50**

> These are injuries seen in two specialist clinics, with the cause as the climbers described it. So they show what hurts people, not how risky each move is: the study didn't count how often climbers use each move without getting hurt #src("G9").

---

## 8. Body weight and climbing grade

**Applies to:** `09-considerations.typ:77–81`. The notebox "Don't diet for grades" stays
as it is.

**Read**
- Faggian et al. (G68, published online 2024, Vol. 14, 2025): full text.
- Saul et al. 2019 (G69): full text.
- Ginszt et al. 2023, J Strength Cond Res: full text. Not added as a source.
- Gibson-Smith et al. 2024 (G70): full text.
- Grønhaug 2019 (new G73): full text.
- Kovářová et al. 2024 (G21): full text.
- Joubert et al. 2022 (G40): full text.
- Ozimek et al. 2017, the paper behind G5: abstract. G5's own page: in full.
- Backe et al. 2009 (new G74): abstract only.
- Draga et al. 2025 (H18): abstract only. Not used in the wording.
- Diez-Fernández et al. 2023, Sustainability: abstract only.
- Merrells et al. 2008: abstract only.

**What the reviews say**
- **Faggian:** 74 studies: cross-sectional, observational and comparative, plus some intervention
  trials used only for their baseline data. "Considerable
  conflicting evidence" on body measurements. Correlations of body mass and BMI with
  ability run both ways (r = −0.47 to 0.71 in men, −0.70 to 0.87 in women). Thirteen studies
  found differences, particularly in body fat. It concludes that body measurements seem to
  count less than strength, endurance and power, and that meta-analyses are needed. It also
  says dividing test scores by body mass clearly raises their link with level. That is about scoring
  tests across climbers, not about one climber changing weight. For the 0.3–4% it cites Mermier and
  Laffaye, so it doesn't support those figures independently.
- **Saul:** body weight correlates negatively with redpoint level, citing two studies. Whether BMI is
  linked is hard to determine. Low skinfolds and body fat were traits of successful climbers, though
  its pooled Table 2 (body fat 14.57% recreational, 12.01% elite) shows no significant difference.
  Strength-to-mass ratio predicted ability.
- **Gibson-Smith:** a survey rather than a review, but its discussion takes a position. It says the
  belief that a low weight helps climbers already at an appropriate weight isn't supported. It
  concludes that the current literature shows no observable link between body composition and
  performance. It also suggests that setting may now favour absolute power over the ratio alone.
- **Ginszt:** body mass and body fat lower in climbers than controls and in elites than in
  less advanced climbers, "may be a key factor". But it warns that mass, height and BMI aren't
  relevant indicators in that review, because researchers recruited similar body sizes.
- **Diez-Fernández:** the abstract doesn't mention body mass, BMI or body fat. It says the
  factors can be trained.
- **Grønhaug:** 667 climbers, web survey, no link between BMI and level, and none between BMI and
  chronic injury. It measures BMI, not weight or body fat. The author warns against reading
  cross-sectional data as long-term effects.

**Weight and injury**
- **Kovářová (G21):** 389 usable questionnaires from Czech and Slovak climbers. Number and severity of
  injuries: no significant effect of sex, age, weight, height or BMI (weight p = 0.190 for number).
  Where the last injury happened: in bouldering only a trend with age, falling as age rises (p = 0.051),
  and no effect of weight. In lead climbing the probability rises with weight (p < 0.001), which the
  authors link to falls onto rock. In indoor wall climbing it falls with weight (p = 0.028).
- **Backe (G74):** a random sample of 606 Swedish Climbing Association members, 63% effective response,
  self-reported. Overweight and bouldering went with a higher risk of a first injury, and the authors
  ask for more study of BMI and injury. G21 cites this study as its one exception.

**Who diets, and why**
- **Joubert (G40):** 114 IFSC-registered women. Table 3: 45% of 105 attempt to change competition
  weight. It didn't measure why. Its introduction says climbers strive for a strength-to-weight ratio,
  and calls a culture that values thinness anecdotal.
- **Gibson-Smith (G70):** weight loss practised anecdotally for decades, with athletes generally believing
  it improves their ratio and their performance. Most who cut lost about 3–8% of body weight over two
  weeks or more.

**Light boulderers (G5)**
- Ozimek: 10 elite Polish boulderers against 165 untrained students. G5 glosses "light" as low fat mass.
- Draga (H18): 34 male boulderers. International climbers had lower body fat. It says the benefit and
  the role of selection remain unclear.
- **Flag for the chapter 9 editor, line 19.** "Differed from non-climbers most in arm span and lean body
  mass" is G5's gloss. The abstract lists both at p ≤ 0.05, and height, body density, fat mass and leg
  length at p < 0.01. Say that they differed in arm span and lean body mass among other measures.

**Within-person studies of climbers losing weight**
- We found none that measures climbing performance. Searches: Europe PMC (title and abstract:
  climbers with weight loss, body mass reduction, energy restriction, added mass or weighted
  vest) and an extended web search.
- Gibson-Smith et al. state there are currently no such trials, whether for short-term weight
  cuts or for losing fat or muscle. They also say the climbers studied are much alike, so the
  findings likely don't apply to people above "athletic" body-fat norms. That matters to this
  book's reader.
- Merrells et al. 2008 is the only within-person weight loss found: two male climbers, 5 weeks,
  about 40% energy restriction, 5.8% of body weight lost. It reports oxidative stress and
  cardiovascular markers, and its abstract reports no climbing performance.

**Wording, lines 79–81**

> Nobody has tested this for climbers like you.#ix("Body weight!and grade") Studies of weight and climbing compare different climbers at one moment, so they can't say what happens when one climber loses weight. The 0.3% to 4% in the studies above are that kind of comparison #src("G3", "G4"). We found no trial of weight loss in climbers, and a recent paper on competition climbers says there are none. It also points out that the climbers studied are much alike, so the results likely don't apply to someone carrying more body fat than athletes usually do #src("G70").
>
> The reviews differ. One found the evidence on body mass and body fat conflicting, and concluded that body measurements seem to count less than strength and endurance #src("G68"). Another says heavier climbers tend to climb lower grades on routes, and that successful climbers carry less body fat. But its own pooled figures show no significant difference in body fat, and it finds no clear link with BMI #src("G69"). The paper on competition climbers goes further. It says research shows no clear link between body composition and performance, and doesn't support the belief that a lower weight helps climbers already at an appropriate weight #src("G70"). One small study, of ten elite Polish boulderers against untrained students, found them light, meaning low in body fat #src("G5").
>
> Some climbers still diet: in a survey of elite women, 45% said they try to change their competition weight #src("G40"). The competition paper says climbers generally believe it will raise their strength for their weight, and so their performance #src("G70"). The arithmetic is simple: if your strength holds, a lower weight raises your strength relative to bodyweight. Across climbers, that ratio tracks grade in many studies #src("G68"). But the ratio has body mass built into it, and comparing climbers can't show what one climber gains by losing weight (this book's reading). We found no test, in climbers, of whether strength holds while you diet, or whether a better ratio then brings grades.
>
> The evidence on injury is mixed. A survey of Swedish climbers linked being overweight, and bouldering, to a higher risk of a first injury, and asked for more study #src("G74"). A survey of 389 Czech and Slovak climbers found no effect of weight on how many injuries they had or how bad they were, and no link with a last injury in bouldering. Heavier climbers more often had their last injury while lead climbing on a rope, which the authors connect to falls onto rock, and less often on indoor walls #src("G21"). A survey of 667 climbers found no link between BMI and long-term injury or level #src("G73"). One knee-injury study wonders, without testing it, whether age and weight help explain why some climbers needed surgery #src("G9").
>
> This book's view: at V3–V5, technique and finger strength hold you back more than a few kilos. Better footwork lowers the load on your fingers today, and dieting for weight loss#ix("Weight loss") carries real health risks (see the box below).

The brief keeps the book's view. This wording drops "the slowest and riskiest way to gain a grade",
because no study ranks weight loss against anything and G70 reports losses of about 3–8% in two weeks
or more. **Simon can restore the superlatives if he wants them as opinion.**

---

## 9. Straight arms and pump

**Applies to:** `01-movement.typ:26`, `:28`; `04-body.typ:369`. See "Other lines" below.

**Read:** B12, B22, B36 and B50 in full. B23 could not be read. Exel et al. (G71) in full.

**Searches:** Europe PMC (elbow angle, elbow flexion, straight arm, bent arm, arm position,
with climbers and forearm, oxygenation, fatigue or pump), plus an extended web search.

**Facts**
- **We found no study that measures elbow angle against forearm fatigue, pump or oxygenation
  in climbing.**
- Closest: Exel et al. 2023. 17 climbers, whom the abstract calls recreational and the Methods
  advanced to elite (IRCRA 22.1). 12-second dead hangs on a 22 mm edge in an open crimp, at 90° and
  135° of elbow flexion and fully extended. Surface EMG of the superficial finger flexor alone did not
  change, with a wide spread (102.2 ± 33.2% at full extension), and the paper reports no reliability
  check. Vertical force didn't change across conditions, so the fingers held much the same load
  whatever the arms did. Biceps, trapezius and latissimus activity rose with bent arms. Elbow and
  shoulder moments rose too. It measured no pump, fatigue or oxygenation, and hangs were short. The
  abstract gives p = 0.15 for the finger flexors and the results p = 0.45; neither is significant. So it
  supports "bent arms work the upper arm and shoulder harder". It gives no support for "bent arms work
  the forearm harder". It also says little about pump on a wall, where arm position can shift load to
  the feet (this book's reading).
- Arm-position oxygenation work is about raising the arm, not the elbow angle. A 2026 preprint
  (Štěpánová et al.) found forearm oxygen recovers more slowly with the arm raised. Not used.
- A 2026 review (J Funct Morphol Kinesiol) says bent arms engage extra elbow and shoulder muscles.
  It gives no pump data.
- B22 (Gresham): bending your arms wastes strength and restricts blood supply to the forearms.
  B36 (Rowland): pulling in on bent arms leads directly to getting tired or pumped. Both are coaching
  opinion with no measurement, so "coaches recommend" holds with both cited. B36 also tells readers to
  sag onto straight arms, the habit B50 warns about, so cite it for pump only.
- B50 (Hooper, physiotherapist): warns that slack shoulders are a risky habit and says he has
  seen it contribute to a dislocation and lesser injuries. Observation, no measurement. No other source
  read says this, so "coaches warn" rests on one person.
- **B50 also calls "hang on your skeleton" inaccurate.** It says the saving comes from contracting
  fewer muscles less hard. B12 and B22 use the bones or skeleton framing, so the sources disagree. The
  brief doesn't list this; flagged for Simon.
- Line 26 says "biceps and forearms" work to hold a bent arm. Exel supports the biceps, and not
  extra forearm work.

**Wording, line 26 (also covers item 15)**

> Muscle holds a bent arm bent. Lock your elbow at ninety degrees. Your biceps and shoulder muscles then work all the time to hold it there #src("G71"). Straighten the arm and your elbow muscles can rest #src("B12", "B30"). A physiotherapist points out that you are always hanging from your skeleton: the saving comes from contracting fewer muscles, less hard #src("B50"). Your shoulder#ix("Shoulders!on straight arms") muscles still hold the joint in place #src("B50"). So learn #tref("straight-arms") early (this book's suggestion). The UK's coach training lists them as a way to find a rest #src("B1").

The brief says to write "early" here. B1 gives no timing and no reason, so "that is why coaches teach"
is gone and "early" is marked as this book's suggestion. **Simon needs to confirm this.**

**Wording, line 28**

> On long problems your forearms #jt("pump")#ix("Pump!reducing"): they swell, ache and weaken. Coaches recommend hanging on straight arms whenever you are not pulling, to ease the pump #src("B22", "B36"). We found no study that measures this. The closest tested 12-second dead hangs with the feet off the wall: the biceps and shoulder muscles worked harder on bent arms, while the one finger flexor it tested showed no change #src("G71"). It measured no pump, so it says little about a real climb (this book's reading). Straight arms also force you to move with your legs, because a straight arm can't pull.

**Wording, `04-body.typ:369`**

> - Sagging onto fully straight arms with slack shoulders. One physiotherapist warns that this is a risky habit, and says he has seen it contribute to a shoulder#ix("Injuries!shoulder") dislocation. We found no study that measures it #src("B50").

This pass couldn't read B23, but `factcheck-3.md` read it in full and records that it supports this warning.
The chapter therefore cites both: the coach Neil Gresham (B23) and the physiotherapist (B50).

**Other lines that repeat what this item corrects (not in the brief)**
- Forearm claim: the caption at `05-hands.typ:64`. Say "biceps and shoulder muscles work to hold you there".
- Pump as a measured result of bent arms: `08-grades.typ:68` and the symptom at `04-body.typ:365`. Mark the
  fix at 08:68 as coaching advice.
- Skeleton or bones carrying the load: `01-movement.typ:5`, the heading at `:24`, the caption at `:30`,
  the alias at `04-body.typ:346`, `:350`, `05-hands.typ:69`, `:242`, `08-grades.typ:161`. These repeat a
  coaching figure that B50 rejects. **Simon decides whether the figure stays.**

---

## 10. Half crimp load

**Applies to:** the box "Is the full crimp dangerous?", `05-hands.typ:581–594`.

**Read:** C23, Schweizer 2001, Amca 2012 and G72: abstracts. C14, C25 and C26: the pages themselves.
The Larsson 2022 taping review: full text.

**What each compares**
- **C23 Vigouroux 2006:** a model of slope grip against crimp. In its crimp the end joint is
  hyperextended. A2 force 36 times lower in the slope grip, A4 4 times lower. No half crimp. The
  abstract doesn't mention a thumb lock, so its crimp is not exactly the book's thumb-locked full
  crimp.
- **Schweizer 2001 (J Biomech 34:217–223):** in vivo, 16 fingers of 4 people, crimp against slope.
  A2 loaded at about 3 times fingertip force, up to 116 N. No half crimp.
- **C14 Hooper's Beta:** 96 N at the fingertip gives about 255 N on A2 in the crimp and about 8 N
  in the open grip, attributed to Vigouroux. No half crimp figure. These newton values come from
  C14, not the abstract. They make about 32 times, where the abstract says 36. Rounding doesn't explain
  that, because 255 N divided by 36 is about 7.1 N. The gap stays unexplained without the Vigouroux
  full text.
- **C25 Schweizer 2012:** crimp (middle joint past 90°, end joint hyperextended) at 3–4 times
  fingertip force. It cites Schweizer 2001 (in vivo) and Tan et al. 2007 (not read), and compares nothing
  with an open grip. Describes the half or open crimp at about 80° as giving the most flexion torque.
  Load "particularly high" past 80°. It advises against bending the middle joint past 80–90°. The book's
  half crimp is about 90° (`05-hands.typ:271`, `:273`) or 85–90° (`:275`). No half crimp load figure.
- **C26 Bosco 2022:** 450 N is a shock load on A2, as from a foot slip. 400 N is a separate figure, the
  cited failure force of A2. No half crimp.

**Search for a half crimp figure:** Europe PMC (half crimp or open crimp with pulley force, load or
A2) and a web search. **No pulley load figure found, measured or modelled.** Half-crimp finger forces
have been measured (Amca et al. 2012, maximal force in three grips), but that abstract gives no pulley
figure. Reviews only describe it: a 2022 review of taping says a half crimp "greatly" raises pulley
load, with no number. So don't imply the half crimp is light.

**G72 can't be set beside the model, so it gets no bullet.** G72 loaded 21 cadaver fingers to a terminal
event, 9 in the slope grip and 12 in the crimp.
- Pulley forces: A2 287 N in the crimp and 121 N in the slope grip, A4 226 N and 103 N.
- Fingertip forces (161 N and 105 N) and deep flexor forces (348 N and 371 N) did not differ
  significantly. The abstract calls them comparable at the terminal event.
- The abstract says it recorded tendon and fingertip forces. It doesn't say how it got the pulley forces,
  so don't call them measured.
- These are forces when each test ended. C14 describes the model at one fingertip force. Per unit of
  fingertip force the G72 ratios are about 1.8 and 1.15 (this document's arithmetic).
- 287 N isn't A2's breaking force. A4 rupture was the commonest event in the crimp (50%). In the slope
  grip most events weren't pulley ruptures (67%).
- C26 cites the same 287 N and 226 N as forces usually generated by a 70 kg climber, a different reading of
  those numbers. A bullet would also seem to contradict the 400 N in the same box.

**Wording, third bullet of the box**

> - Schweizer#ix("Schweizer, Andreas") puts pulley forces in a crimp at 3–4 times the fingertip force. They become particularly high once the middle joint bends past about 80°, and he advises against bending it past 80–90° #src("C25").

**Wording, replaces the "These are load models" bullet**

> - The model above compares a crimp, with the end joint bent back, with an open grip. We found no pulley load figure for the half crimp, measured or modelled, so the model can't say whether a half crimp saves anything, or how much #src("C23"). The research found for this book does not compare injury rates between full and half crimping.

---

## 11. Lattice bands (F1, F2)

**Applies to:** `08-grades.typ:305`, `:309`, `:265`, and the notebox at `:16–24`.

**Read:** F1, F2, F14, F15, F47 and the blog behind F15 in full.

**Facts, F1 (over 6,000 tested climbers, cleaned data set)**
- Added weight on two-arm max hangs, all climbers: V1–V4 +19.0 kg, V5–V7 +24.2 kg, V8–V11 +38.4 kg,
  V12+ +52.9 kg.
- These mix men and women. Women start at +6.6 kg at V1–V4 and reach +29.5 kg at V12+. No figures for
  single grades. Edge and hang length aren't stated.
- The author says the grade progression is one that technique alone can't bridge, and that finger strength
  is highly correlated with grade. That removes any premise for 08-grades:309 and leaves the first bullet
  at :265 resting on F14. F14: Lattice is likely to advise climbers with under five years' experience to
  focus on technique or applying strength.

**Facts, F2 (65,000 climbers, "one of our largest datasets")**
- Years climbing and training: V1–V4 5.8 and 2.4, V5–V7 8.6 and 3.2, V8–V11 9.7 and 4.6, V12+ 11.8
  and 6.5. V8: under-25s 3.8 years, 40+ 13.0 years.
- These are the years climbers at that grade report, **not the time it took them to get there**. The
  author says of the V12+ group that the data wasn't analysed for when they first reached the grade,
  though he also writes of years "to reach" a level.
- F2 says climbers "report" the figures. It doesn't say who is in the dataset. "Keen" is the book's
  word for forum posters, and doesn't fit F2's author, who suspects the V1–V4 group has fewer
  performance-minded climbers. He calls that a hunch with no data.
- F1 and F2 both close by advertising a LatticePlan, Lattice's training plan, so Lattice is an interested
  source.

**Facts, F47:** the thread asks what grade people reached after a year, so this one is time to grade.
Its posters chose to answer.

**Facts, F15:** the forum post quotes Wesley's blog. V4 49% and V5 55% of bodyweight, one arm, 20 mm,
male climbers. The blog takes V4, V7 and V11 two-arm hang figures for men from a Lattice video (not seen):
128%, 146%, 170%. It fills in V5 at 134%. It then carries those 6% steps onto a one-arm scale anchored at
V14, and its own edit concedes objections. The blog calls the result an extrapolation.

**Wording, line 305**

> Lattice's published bands, V1–V4 and V5–V7, are too wide to show the step from V4 to V5. On a two-arm #jt("max hang") (the most extra weight you can hang for a few seconds), the averages across men and women rise from about 19 kg in the V1–V4 band to about 24 kg at V5–V7 #src("F1"). A forum reconstruction for men fills in V5 between figures from a Lattice video for V4 and V7, then moves the result onto a one-arm scale: about 49% to 55% of bodyweight. That's an estimate and not a measurement #src("F15").

**Wording, line 309 (first sentence).** The old sentence lost its premise with "the gap is small".

> These figures can't say where the extra strength for V5 comes from. Trying V5s is this book's first suggestion (judgement), but Lattice's author warns that technique alone can't carry you up the whole grade scale #src("F1").

**Wording, line 265 (first bullet of the "Five things" list)**

> + Assume technique, not strength, stops you until a symptom says otherwise (judgement, from the coaches' advice in "Technique or strength?").

**Wording, line 18 (last sentences)**

> The figures are self-reported. The author suspects that casual long-time climbers inflate the V1–V4 figure, and calls that a hunch without data.

**Wording, line 20 (first sentence).** "Age stretches every step" reads F2's years as time to grade.

> Older climbers at a grade report more years of climbing. At V8, climbers under 25 report 3.8 years on average. Climbers over 40 report 13.0 years #src("F2").

**Wording, line 24**

> Haven't climbed a V5 after a year? These figures give you no reason to think that's slow. All of them are self-reported. Lattice, a training company, reports how long climbers at a grade have been climbing, not how long the grade took. The forum thread does ask what grade people reached after a year, but its posters are self-selected.

**Flag for the chapter 8 editor.** The notebox title "How long progress takes" and the index terms
`Progression!time to grade` and `Age!years to grade` read F2 the same way. "How long climbers have been
climbing" and `Age!years climbing` would fit.

---

## 12. Deadpoint (D1, D13)

**Applies to:** `06-dynamic.typ:29`, `:81`; `08-grades.typ:185`; `a-glossary.typ:56`.

**Read:** D13 in full. D1 could not be read: search excerpts only.

**Facts**
- D1 (excerpts): a controlled dynamic move catching a hold near the top of the upward motion, with at
  least one foot or the other hand on. Nothing found on weight or load. So D1 supports the definition,
  not "takes the least load".
- D13 (Rowland): uses the thrown ball. Says hips stop moving up or down, you "weigh almost nothing",
  and you get an instant to latch before your weight pulls on your grip. It also says momentum carries
  you after the leg push, in a short phase when your arms do little or no work.
- **D13's physics is wrong.** It says there is no acceleration at the top, so no weight. A thrown ball
  still accelerates downwards at the top, with zero speed. And zero acceleration on a hold would mean
  full weight on it. Use D13 for the coaching idea and not for the explanation.
- **The brief's "neither rising nor falling, so you feel almost weightless" has the same fault.** Someone
  standing still on a foothold is also neither rising nor falling, and feels full weight. What you feel is
  the force from your contact points, which falls only while you are coasting after the push. A thrown ball
  is weightless for its whole flight, not only at the top. A foot that still pushes is a contact force, so it
  adds to what you feel. The top does mean you are barely moving, so the hold starts to take load gently as
  you sink. This is this book's reading, not D13's, so the wording marks it. The effect is weakest for the
  slow, small rise at 08-grades:185, hence "lighter" there.
- **Simon needs to rule on this.** REVISE-3 words lines 29 and 81 with the "so" that this wording removes.

**Wording, line 29**

> Throw a ball straight up. At the top it stops for an instant before it falls. Your hips do much the same when you throw them up the wall. Near the top your legs have finished pushing and you are coasting, so little presses on your hands or feet and you feel light. You are also barely moving, so the hold starts to take your weight gently as you begin to sink (this book's reading). Grabbing at that instant is the deadpoint #src("D1", "D13").

**Wording, line 81 (summary)**

> You throw your hips up the wall and grab the next hold at the top of that movement, when you are barely moving and feel light (this book's reading). At least one foot stays on #src("D1", "D9", "D13").

**Wording, `08-grades.typ:185` (first sentence)**

> Learn the #tref("deadpoint"): catch the hold at the top of a small upward movement, when you have stopped rising and feel lighter.

**Wording, `a-glossary.typ:56`.** The current text keeps "weightless" and "takes the least strength".

> #gloss("deadpoint", see: ("deadpoint",))[The top of a movement, when you have stopped rising and feel light. Grabbing the next hold at that instant gives you a moment to latch before your weight pulls on your grip.]

---

## 13. Three foot moves (A3)

**Applies to:** `03-feet.typ:21`.

**Read:** A3 in full.

**Facts**
- A3 (Mike and Mark Anderson, Climbing.com) gives it under a drill on keeping your feet low and moving them
  often. When practising, it says, try three foot placements for every hand move.
- It adds that you may need in-between footholds that aren't part of the route. It frames all this as
  practice for real rock, done on top rope or bouldering near the ground.
- It gives no measurement, and doesn't offer it as a ratio for normal climbing.

**Wording, line 21**

> - *Move your feet often.*#ix("Footwork!how often to move the feet") To notice lazy feet, try a drill from one how-to article: make three foot placements for every hand move, using any footholds you need #src("A3"). Try it on an easy climb first (this book's suggestion). It's a practice drill, not a target for your hard problems. Use small in-between footholds instead of one big step #src("A28", "A29").

"On an easy climb" is this book's addition; A3 says to practise and to progress to harder terrain. The
citation now stops before it.

---

## 14. Shoulders and dynamic style (G19)

**Applies to:** `06-dynamic.typ:25`, `09-considerations.typ:73`.

**Read:** full text.

**Facts**
- Mena et al., Cureus 2024: cross-sectional, 35 indoor boulderers in Brazil, 28 of them men, mean age 25.9.
  Convenience and snowball sampling. At least 6 months' bouldering. Questionnaire plus an examination by
  final-year orthopaedic residents.
- "Dynamic style": a self-reported preference for dynamic over static moves, 14 of 35. No split between
  deadpoints and big jumps, and nothing on hold size.
- Shoulder finding: 6 of 35, all men, reported apprehension episodes with at least two weeks away from
  climbing. Linked to dynamic preference (Fisher p = 0.028; prevalence difference 0.3, 95% CI 0.04–0.57).
  The ratio doesn't confirm it (7.5, 95% CI 0.98–57.55). The climbers with apprehension also had less experience
  (4.5 against 6.5 years). A snapshot can't show which came first.
- So G19 says nothing about small deadpoints against big jumps. The reconciling advice is this book's judgement.
- D38, the source for "costs less energy" at `06-dynamic.typ:17`, is a shop page. D13 is one article by a gym
  owner. It never mentions the size of a deadpoint. It says dynamic movement is generally more efficient than
  lock-offs, and that lock-offs belong where precision is necessary. Its saving is energy and overall work.
  Neither D13 nor D38 addresses finger load, so "often cost less" must not read as less load on the fingers.
- C25 names grasping a hold very quickly in a dynamic move as one way a pulley ruptures. That is the catch to
  limit, and `06-dynamic.typ:19–21` already prescribes a very small deadpoint for thin edges.

**Wording, `06-dynamic.typ:25` (first sentence, and "the move" in the next)**

> Otherwise, try the move dynamically first, with the smallest deadpoint that reaches. Small deadpoints are fine (judgement), and one gym owner's article says dynamic moves are generally more efficient than lock-offs #src("D13"). Keep big jumps for the moves that need them (judgement; see Chapter 9), and don't snatch at small holds, because grabbing a hold very quickly in a dynamic move can rupture a pulley #src("C25"). Strictly, a move like this is a deadpoint while a foot stays on and a dyno once both feet leave #src("D2", "D9").

**Wording, `09-considerations.typ:73`**

> + Climb with control while your fingers are still adapting. Small deadpoints are fine (judgement). One gym owner's article says dynamic moves save energy compared with locking off (Chapter 6), but that says nothing about the load on your fingers. Keep big jumps for the moves that need them, and don't snatch at small holds (this book's suggestion). In a small indoor study of 35 climbers, six reported a shoulder that felt it might slip out, badly enough to need at least two weeks off. Those climbers more often preferred a dynamic style#ix("Injuries!shoulder"), but they also had less experience, the result is uncertain, and one snapshot can't show that the style caused it #src("G19").

---

## 15. Straight arms "from the start" (B1)

**Applies to:** `01-movement.typ:26`, grade note of `straight-arms` at `04-body.typ:349`.

**Read:** B1 and the matching syllabus for workshop 1, both in full. BMC course pages via a page-fetch summary.

**Facts**
- These are syllabuses for **training coaches**, not stages for climbers. They don't say when a climber should
  learn a technique.
- FUNdamentals 1: centre of gravity, weight transfer (a rockover on a slab), footwork, handholds, warm-up. Straight
  arms aren't listed.
- FUNdamentals 2 (B1): straight arms appear once, under efficient body positioning on vertical and gently
  overhanging terrain, as a way to find a rest or clipping position, with the triangle principle. It gives no
  reason about elbow muscles. It also lists flagging and drop knee, which the brief badges V2 and V3, so being in
  workshop 2 can't mark a V0 skill.
- Workshop 2 builds on workshop 1. Direct entry is possible for people with suitable experience.
- We found no public NICAS syllabus that mentions straight arms.
- "On V3–V4 overhangs it decides whether you run out of strength" has no source, so the wording below softens it.
- B50 warns that context-free straight-arm advice builds problem habits. `04-body.typ:370` already lists sinking
  low on a vertical wall as an error, and at V0 the wall is often vertical. So the first-session advice is limited
  to steep walls.
- **Flag for the chapter 4 editor.** Five grade notes read a coach syllabus as a climber's order in the same way:
  `04-body.typ:64`, `:199`, `:272`, `:308`, `:661`. Say that coach training lists the skill.

**Wording, line 26:** see item 9.

**Wording, grade note, `straight-arms` (badge V0)**

> grade-note: [Learn it from your first session (this book's suggestion): when you pause on a steep wall, hang on nearly straight arms with your shoulders set, and on a vertical wall stand tall instead. It matters more on your first overhangs, and on V3–V4 overhangs it can decide whether you run out of strength (judgement). The UK's coach training lists it as a way to find a rest #src("B1").],

---

## Disputed findings

The sceptics' reports on these points were checked against the sources. Where a report was wrong in part, the
document follows the source.

- **G40's motive (item 8).** The report places the strength-to-weight passage in the discussion. It is in the
  introduction, and the paper states flatly there that climbers strive for that ratio. The conclusion stands,
  because the survey didn't measure the motive, so the wording changed anyway.
- **G21 and "the only weight link" (item 8).** The report wants the sentence to say the only weight link was in lead
  climbing, or to go. That is true of G21 alone. G21 itself names Backe 2009 as an exception, and Backe's abstract
  links being overweight to a higher risk of a first injury. Cutting the topic would hide the one finding that
  points at this book's reader, so the wording says "mixed" and cites both.
- **Coaches and pump (items 9 and 14).** The report says "coaches recommend" rests on B22 alone. B36 says the same
  about pump, so the plural stays at `01-movement.typ:28`. The report is right about `04-body.typ:369` and
  `06-dynamic.typ:25`, which changed.
- **The skeleton framing (item 9).** The report treats this as an error left in place. B12 and B22 use it and B50 rejects
  it, so it is a disagreement between sources. Those lines are listed for Simon and the wording doesn't rule on them.
- **"Extrapolation" (item 11).** The report says the V5 figure is an interpolation. It is, on the two-arm scale, but the
  one-arm 49% and 55% are counted down from V14 and the blog itself calls the result an extrapolation. Both
  are recorded, and the wording says "fills in" and "moves".
- **Half-crimp finger loads (item 10).** One of the two abstracts the report cites, Morenas Martín 2013, couldn't be found
  in Europe PMC. Amca 2012 is enough to narrow the sentence to pulley load, so nothing rests on the other.
- **The label on the selection effect (item 5).** The report is right that E6 doesn't make this argument, but it asks for
  "(this book's view)". The brief names "(judgement)" or "(this book's suggestion)" for a new claim with no source, and
  keeps the book's view for the weight claim in chapter 9. Line 204 also closes the same reading with "(judgement)". So
  the label is "(judgement)".
- **"Call these rates trends" (item 5).** The paper's word is accurate, but a reader wouldn't learn from it that the rates
  went untested, which is the report's own concern. The success rates aren't among the outcomes in the authors' models,
  and that part of the results prints no p-values, so the wording says "ran no statistical test".
- **"Which they couldn't correct for" (item 5).** The fault the report names is the antecedent, and "these rates" cures it.
  "Warn that skill probably skews them" already tells the reader the skew remains, so the clause goes. The facts above
  keep the difference between the rates and the modelled times.
