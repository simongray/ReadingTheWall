# Fact-check 3: blocked links, unverified claims, E17, deadpoint, tic-tac

Checked 2026-10-31. Nothing in `book/` or the yml files was edited.

Method. I opened each page in the Claude desktop app's built-in browser and
read its text rather than screenshots. I declined non-essential cookies where
a banner offered it (Friction Labs, Rock+Run, Climbing.com, Anatomic). The
UKC banner only offers "OK", so I left it alone. I didn't sign in anywhere.
Where a bot check appeared I recorded "bot check" and moved on without
touching it. Two "please wait" pages (Thieme, mediaTUM) cleared by themselves
within seconds, without any input from me, and I've noted them. Late in the
session PubMed and PMC began showing a reCAPTCHA, so I read those records
through the Europe PMC and Crossref APIs instead. For pages that had changed
or were blocked, I used the Wayback Machine.

The most useful finding is that UKClimbing isn't paywalled in a browser.
Curl got a 402 or a Cloudflare page, but every UKC article and thread opened
in full without signing in. The "Paywalled; consulted through search-result
excerpts" notes on B23, C51, C52, E13–E17 and E49 can go.

## 1. The 38 blocked links

Totals: 30 load and match the yml entry, 4 load but differ from it (C52,
C56, E16, E17) and 4 show a bot check (D46, E36, E63, G48).

| Item | Source | Result | Suggested change |
|---|---|---|---|
| A14 | Friction Labs, toe hook | OK, title matches | — |
| A17 | Friction Labs, kneebar | OK, title matches | — |
| A37 | Rock+Run, overhangs | OK, title and date match. The byline is "Rock + Run UK" and the text opens "By Dave Westlake" | author "Rock+Run" → ["Westlake, Dave"], as in E1 and E2 |
| B23 | UKC, Posture in Climbing | OK, read in full. Gresham with Nina Tappin, 27 Sep 2019 | add date 2019-09-27; drop the paywall note |
| B67 | UKC forum, backstepping | OK, title matches, thread of 15 May 2018 | not cited in the book any more |
| B68 | UKC forum, bent arms | OK, title matches, thread of 6 Apr 2011 | not cited in the book any more |
| C24 | Thieme, html URL | "Please wait" page cleared by itself and redirected to the abstract page. Title and authors match | url → `https://thieme-connect.de/products/ejournals/abstract/10.1055/s-0030-1267230` |
| C39 | Friction Labs, mantle | OK, title matches | — |
| C51 | UKC id=11848 | OK: "Handholds and Grip Technique – Part 1", Gresham, 27 Mar 2019 | add date 2019-03-27; the claim fails (section 2) |
| C52 | UKC id=12172 | Loads, but the article is "Using Undercuts and Sidepulls" (Gresham, 8 Aug 2019), not the series name | title → "Using Undercuts and Sidepulls"; add date 2019-08-08 |
| C56 | Atomik | Loads, but the page has been rewritten as "Types of Climbing Handholds", with no palming section. The yml title and the palming text survive in the Wayback copy of 18 Aug 2025 | url → `https://web.archive.org/web/20250818012022/https://www.atomikclimbingholds.com/how-to-use-the-nine-basic-types-of-climbing-handholds`, or note the rewrite |
| C57 | theCrag, gaston | OK, entry "Gaston" | note → read 2026-10-31 |
| D1 | theCrag, deadpoint | OK, entry "deadpoint" | note → read 2026-10-31 |
| D2 | theCrag, dynamic move | OK, entry "dynamic move" | note → read 2026-10-31 |
| D22 | Friction Labs, dyno | OK, "How To Dyno!" | — |
| D23 | Friction Labs, pogo | OK, "How To Pogo for Climbing" | — |
| D46 | Rock Prodigy forum | Bot check (a blank challenge page that keeps reloading). The Wayback copy of 17 Apr 2024 matches the title and the March 2016 posts | add `https://web.archive.org/web/20240417184134/https://rockprodigytraining.proboards.com/thread/927/dynos-dyno-training` as a fallback |
| D51 | Outdoors Codidact | OK, title matches. It's a CC BY-SA copy of outdoors.stackexchange.com/q/17173 | not cited now; see section 2 |
| E1 | Rock+Run, slabs | OK, title, author and date match | — |
| E2 | Rock+Run, arêtes | OK, title, author and date match | — |
| E13 | UKC, heel hooking | OK, read in full. Gresham with Louis Parkinson, 12 Oct 2018 | date → 2018-10-12; drop the paywall note |
| E14 | UKC, topping out | OK, read in full. By Dave Flanagan, 14 Nov 2014 | author → ["Flanagan, Dave"]; add date 2014-11-14 |
| E15 | UKC id=10957 | OK: "Technique – Use of the Toe", 28 Jun 2018. But the claims cited to E15 come from another article | re-point (section 2) |
| E16 | UKC series index | Redirects to the series' first article, "Technique – General approach and long-term development" (22 Feb 2018), which has none of the cited claims | re-point (section 2) |
| E17 | UKC id=3924 | OK, read in full | see section 3 |
| E30 | Rock+Run, route reading | OK, Gresham, 9 Oct 2020 | — |
| E31 | Friction Labs, gym routes | OK, title matches | — |
| E36 | iris.cnr.it | Bot check (Cloudflare) | url → `https://doi.org/10.1016/j.bandc.2010.03.002` (the DOI is already in the yml; Europe PMC record 20381226 matches) |
| E41 | Rock+Run, limit tactics | OK, Chapman, 9 Oct 2018 | — |
| E44 | Friction Labs, projecting | OK, title matches | — |
| E49 | UKC, routesetters | OK, read in full. By Nate McMullan, 10 Jun 2015 | author → ["McMullan, Nate"]; add date 2015-06-10 |
| E63 | HAL | Bot check (Anubis) | keep; Crossref confirms DOI 10.1080/19346182.2015.1107081, pp. 88–94 |
| G15 | mediaTUM | "Please wait" page cleared by itself. The record matches: Injury 53(4):1394–1400 | could add DOI 10.1016/j.injury.2022.02.003 |
| G47 | DOI → SAGE | OK, title matches, abstract readable | — |
| G48 | DOI → Wiley | Bot check (Cloudflare). PubMed record 20561271 has the abstract | merge into E34 (section 2) |
| G49 | DOI → Taylor & Francis | OK, Ecological Psychology 18(3) | — |
| G52 | DOI → Taylor & Francis | OK, abstract readable | note: drop "abstract not accessed" |
| G65 | DOI → BMJ | OK, BJSM 57(17):1073 | — |

## 2. Claims that couldn't be verified

The first block covers the rows from factcheck-1, the second the NV rows from
factcheck-2.

| Item | Source | Result | Suggested change |
|---|---|---|---|
| D-3 "often credited to Güllich" | — | The sentence is no longer in chapter 6 | FOLLOW-UPS is out of date on this; see section 4 |
| D-10 tic-tac as a climbing term | — | See section 5 | — |
| D-11 tic-tac "you stood too upright" | D48 | Partly supported. In its wall-run variation, D48 says to lean further away from the wall and take quicker steps so you don't slip | "*Symptom:* your foot slips off the wall. You stood too upright against it." → "*Symptom:* your foot slips off the wall. Lean further away from it and step quickly #src("D48")." |
| D-19 deadpoint definition, weightless moment, a foot stays on | D1, D2 | Supported. D1: you grab the hold at the top of the body's rise while one or both feet stay on, and with both feet off it's a dyno. D2 makes the same split. The weightless moment is D13's, and C52 calls it that too | — |
| E-29 setter's brief | E49 | Supported: who the problems are for, what difficulty, then the movement and the general effort | — (metadata in section 1) |
| E-30 roof row: backs and sides of holds | E15 | Supported, but by Gresham's "Toe-Hooking and Clamping" (UKC 11552): toe hooks go below projecting features, and climbers miss the ones round the sides | re-point E15 (see the last row of this block) |
| T-7 corner: let go with both hands | E17 | Supported. Bridging gives no-hands rests "in a lot of circumstances" | optional: "Sometimes you can let go with both hands" → "Often you can let go with both hands" |
| T-8 slab: small steps, don't keep testing footholds | E16 | Not on E16's page. All of it is in "Use of the Toe" (10957, today's E15): don't test the foothold, keep the pressure even, take several small steps rather than one big one, keep the heels down | re-point E16 (see the last row of this block) |
| T-12 top-out: heel first, pull with the heel, straighten the lower leg, counterweight | E13, E14 | Supported. E13: on a rounded top, get a heel up first, then pull on it while you push with the lower leg, and flag the other leg. E14: feet level with the waist if you can, pull with arms and heel while you straighten the lower leg, palm flat, straighten both arms. E14 doesn't mention turning the knee in or a counterweight, which E23 covers | — |
| T-17 roof toe hooks: plan the release, look to the sides, feet first | E15 | Supported by "Toe-Hooking and Clamping", which covers all three | re-point E15 |
| X-6 downturned shoes under roofs | E15 | Supported by "Toe-Hooking and Clamping": for clamping, a downturned shoe beats a flat one, and a big toe patch helps | re-point E15 |
| The E15/E16 fix | — | These two yml changes make every E15 and E16 citation in chapters 2, 7 and the troubleshooting appendix match its page, with no chapter edits | **E15:** title → "Toe-Hooking and Clamping", url → `https://www.ukclimbing.com/articles/skills/series/neil_gresham_technique_and_training/toe-hooking_and_clamping-11552`, date 2019-01-07. **E16:** title → "Technique – Use of the Toe", url → `https://www.ukclimbing.com/articles/page.php?id=10957`, date 2018-06-28 |
| B23: a few degrees of bend, slack shoulders, Gresham avoids locking off | B23 | Supported: a very slight bend of a few degrees; sagging onto fully straight arms strains the shoulders; twist in on the outside edge or drop knee rather than lock off. "Shrugged" isn't Gresham's word, since he uses shrugs as the warm-up fix | Chapter 4 error: "Hanging slack with shrugged shoulders." → "Sagging onto fully straight arms with slack shoulders." |
| C50 the smooth part makes a big hold hard | C50 | Supported in substance. The page says the smooth part turns a comfortable jug into one that needs more precise movement | "The smooth part can turn a big hold into a hard one" → "The smooth part can turn a big, easy hold into one that needs precise movement" |
| C51 change grip as your body moves past the hold, e.g. open hand to pinch | C51 | Not supported. Part 1 covers switching between full crimp, half crimp and open hand to rest the fingers on long routes. Part 3 (UKC 12008, 5 Jun 2019) says to change to a pinch to make room for the other hand when matching | Re-grip step: "Change grip as your body moves past the hold, e.g. from an open-hand to a pinch #src("C51")." → "On a long run of edges, switch between half crimp and open hand. The change rests your fingers #src("C51")." Add Part 3 as a new C entry and cite it on the match step: "…take the hold with fewer fingers, on one side, or pinch it." |
| C52 undercling: feet up first, bring the hold in | C52 | Supported | title fix only (section 1) |
| C56 palming: press through the heel of the hand, then move a foot | C56 | Supported by the 2025 Wayback copy. The live page no longer says it | archive URL (section 1) |
| C57 gaston | C57 | Supported: thumb down, elbow out, pressing outward | — |
| F17, F37 | — | F17 isn't cited in the book now. The Wayback Machine has no copy of F37 | — |
| G7, G8 tall climbers | G7, G8 | Partly supported. In G8, one poster says height helps up to about V6 and the advantage disappears at intermediate grades, and another says it helps to 5.10 but not to 5.13. G7 says the advantage shrinks on steep ground and when the feet cut. Neither gives V3–V5, and not every poster is tall. Scrunchy moves: supported (a 6'5" poster in G8; knees in the way in both). Hips sagging on dynos: not found; posters say tall climbers struggle with the swing and extra weight when the feet cut | (1) "On forums, tall climbers report that this advantage fades around V3–V5" → "On forums, climbers report that this advantage fades at intermediate grades, by about V6". (2) "*Big jumps.* Tall climbers report that their hips sag away from the wall on a dyno #src("G8")." → "*Big moves with cut feet.* Forum climbers say tall climbers find the swing harder to hold #src("G7", "G8")." |
| G40 17 of 114; 4 of 18 under BMI 18 | G40 | Supported. Only 4 of the 18 with amenorrhoea had a BMI under 18.0. 17 said they currently had an eating disorder. Half of the 18 restricted food | optional: "reported a current eating disorder or disordered eating" → "said they currently had an eating disorder" |
| G45 feedback after each session; side-on positions; jerk | G45 (full text via Europe PMC) | Supported. Climbers got feedback on jerk, entropy and immobility at each session. Those who found side-on positions improved suddenly | — |
| G46 jerk of the hips | G46 (abstract via Europe PMC) | Supported: jerk was measured with a sensor on the hips | note: drop "cited via later papers" |
| G47 novices learn by watching | G47 | Supported: 24 novices watched a video of an expert, then climbed faster and more fluently | optional: "just by watching a skilled climber" → "just by watching a video of a skilled climber" |
| G48 reading a problem helps you climb it | G48 (= E34) | Partly supported. A 3-minute preview cut the number and length of stops but didn't change how often climbers finished. G48 and E34 are the same paper (same DOI) | "Reading a problem before you climb it helps you climb it #src("G48", "G44")." → "Reading a problem before you climb it means fewer and shorter stops #src("E34", "G44")." Then drop G48 |
| G49 fear narrows what you notice | G49 | Supported: anxiety narrowed attention, shortened reach and led to more holds being used | — |
| G51 varied practice; too much feedback | G51 (Wikipedia) | Supported: varied practice can hurt performance during practice but helps retention; too much feedback can make you depend on it | — |
| G52 external focus | G52 | Supported by the abstract, across tasks, skill levels and ages | note: drop "abstract not accessed" |
| "Hover hands" drill | — | Found a source: The Climbing Doctor, "Train Climbing Route Speed, Movement Cadence and Technique" (29 Mar 2023). You hover the hand about three seconds before each hold on an easy route, to find the body position first | Add it as a new G entry. Chapter 9 table: "for 2 seconds" → "for about 3 seconds"; "(A common coaching drill; no source found.)" → `#src("G…")` |
| D51 gyms vary | D51 | Supported: holds and angles vary a lot from gym to gym | optional: cite D51 again beside E53 |

## 3. E17's title

| Item | Source | Result | Suggested change |
|---|---|---|---|
| E17 | Wayback copy of 29 Jan 2013; live page | The 2013 copy's full title is "Training to Become a Better Climber Part 3 – E1/6b/V2", by Robbie Phillips, July 2011. The live page shows only "Training to Part 3" in the series "Become A Better Climber", dated 21 Jul 2011. The old `page.php?id=3924` URL still redirects | title → "Training to Become a Better Climber – Part 3"; author → ["Phillips, Robbie"]; date 2011-07-21; url → `https://www.ukclimbing.com/articles/skills/series/become_a_better_climber/training_to_part_3-3924`; note → "Read in full 2026-10-31; full title from the Wayback copy of 29 Jan 2013" |

## 4. Deadpoint history (06-dynamic.typ, line 30)

| Item | Source | Result | Suggested change |
|---|---|---|---|
| "Güllich studied the idea in the 1980s" | D3 | Wikipedia says he studied the use of the deadpoint, in a passage on his scientific approach to training. Its reference is Beth Wald's interview of June 1987 in _Climbing_. It gives no decade, so "the 1980s" is inferred from that date | "Wolfgang Güllich studied the idea in the 1980s #src("D3")." → "By 1987, Wolfgang Güllich was studying how to use the deadpoint #src("D3")." |
| "at the high deadpoint of the swing" | D4 | Exact. Gill uses the phrase for what he calls a "dynamic layback" | — |
| "often credited to Güllich" | — | Already gone from the text | FOLLOW-UPS: drop the sentence about the unsourced "often credited" claim |

## 5. Tic-tac

| Item | Source | Result | Suggested change |
|---|---|---|---|
| Climbing use of "tic-tac" | Web searches in English, German and French (coaching articles, comp commentary, glossaries, Reddit, YouTube); D9; D7 | No climbing source uses "tic-tac". Every hit was parkour, a video game or the mint. D9's Olympic glossary doesn't list it. The closest climbing source is D7 (Climbing.com, by the US team's head coach), which describes comp boulders with "wall runs" and other parkour-style moves, and "skate moves" across volumes | Grade note: "We found it defined only in parkour sources #src("D48"). Its climbing use is unverified." → "Climbing writers describe "wall runs" and other parkour-style moves in competition boulders #src("D7"), but we found the name tic-tac only in parkour sources #src("D48")." Add D7 to the entry's sources. Keep the FOLLOW-UPS item open |
