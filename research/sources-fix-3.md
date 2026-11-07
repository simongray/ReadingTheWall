# Sources fix 3: stable copies for the bot-checked sources

Checked 2026-11-07 on the third-edition branch. Nothing in `book/` or the yml
files was edited.

Method. I tried each candidate URL with curl first, then in the Claude desktop
app's built-in browser, and read the page text. I didn't sign in anywhere or
touch a bot check. HAL's Anubis page ("Making sure you're not a bot!") cleared
by itself in about 8 seconds; the Cloudflare checks on Derby, Groningen's PDF
and Bologna's repository did not clear, so I left them. Open-access locations
came from Unpaywall and OpenAlex, abstracts and dates from Europe PMC and
Crossref, and Wayback snapshots from the Wayback availability API. The Wayback
CDX search was offline during the session.

Two of factcheck-3's suggestions are already in place. Commit 1498913 (31 Oct)
pointed E36's url at its DOI and merged G48 into E34, so the sections for
those two start from the current entries.

## D46: Rock Prodigy Training forum, "Dynos/Dyno Training"

**Copy.** The live thread still shows a blank challenge page that keeps
reloading. The Wayback copy of 17 April 2024 opens without a check, both in
curl (200) and in the browser. Its title is "Dynos/Dyno Training", the board is
"Skill Development", and the posts run from 27 to 28 March 2016. The page calls
the forum "The Rock Climber's Training Manual".

**Citations** (all in `06-dynamic.typ`):

| Line | Sentence | Verdict |
|---|---|---|
| 457 | Campus move: "Each move is a short, footless dyno #src("D46")." | Partly supported. iclimb2improve says campusing is meant to be "'footless' dynos", but "trying to do as big of moves as possible". So "footless dyno" holds and "short" doesn't come from the post. |
| 603 | Double clutch: "A forum post describes a dyno to one hold whose speed carries you on to another #src("D46")." | Supported. jessebruni: you "dyno to one hold" and use the momentum to reach another. |
| 480, 633 | D46 in the `sources` lists of Campus move and the competition set pieces | Follows from the two rows above. |

Suggested chapter change (optional): "Each move is a short, footless dyno
#src("D46")." → "Each move is a footless dyno #src("D46")."

**Proposed yml change.** Make the Wayback copy the url, as C56 already does.
D46 has no DOI, so the printed reference will show this URL.

```diff
 D46:
   type: web
   title: "Dynos/Dyno Training"
   author: {name: "Rock Prodigy Training forum"}
   date: 2016-03
   parent:
     title: "Rock Prodigy Training forum"
   url:
-    value: "https://rockprodigytraining.proboards.com/thread/927/dynos-dyno-training"
-    date: 2026-10-30
-  note: "Forum thread (posts by jessebruni and iclimb2improve). Wayback copy of 17 April 2024: https://web.archive.org/web/20240417184134/https://rockprodigytraining.proboards.com/thread/927/dynos-dyno-training"
+    value: "https://web.archive.org/web/20240417184134/https://rockprodigytraining.proboards.com/thread/927/dynos-dyno-training"
+    date: 2026-11-07
+  note: "Forum thread of 27–28 March 2016 (posts by iclimb2improve and jessebruni). The live page shows a bot check, so this is the Wayback copy of 17 April 2024."
```

If you'd rather print the live URL, keep the entry as it is: its note already
gives the Wayback copy.

## E36: Pezzulo et al. 2010, "When affordances climb into your mind"

**Copy.** There is no open full text. Unpaywall and OpenAlex list none, and
CNR's IRIS record (the old url) has no file attached. The Bologna and Sapienza
repository records sit behind Cloudflare. The current url, the DOI, sends the
browser to ScienceDirect, which answered with a 403 error page ("There was a
problem providing the content you requested"). So that url still can't be
checked.

The Europe PMC record 20381226 opens in the browser without a check and gives
the full abstract, with Brain and Cognition 73(1):68–73. Curl gets a 403 from
that page. For automated checks, the Europe PMC REST API returns the same
abstract as JSON:
`https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:20381226%20AND%20SRC:MED&resultType=core&format=json`.
PubMed answers curl with a 203 challenge page, and its Wayback copy is the
challenge page too.

**Citations:**

| Line | Sentence | Verdict |
|---|---|---|
| `02-reading.typ` 19 | "Experts remembered the holds of a hard route better than novices, though on easy routes there was no difference #src("E36")." | Supported by the abstract: "no difference" on the easy and impossible routes, while experts did better on the difficult one. The recall test had climbers write down the sequence of holds. The heading's claim, that you read with the moves you know, matches the authors' conclusion that recall depends on the climber's motor repertoire. |

**Proposed yml change.** Point the url at Europe PMC, as the H entries do, and
add the missing issue number. The DOI stays in `serial-number`, so the printed
reference doesn't change.

```diff
 E36:
   type: article
   title: "When affordances climb into your mind: advantages of motor simulation in a memory task performed by novice and expert rock climbers"
   author: ["Pezzulo, G.", "Barca, L.", "Bocconi, A. L.", "Borghi, A. M."]
   date: 2010
   page-range: 68-73
   serial-number:
     doi: "10.1016/j.bandc.2010.03.002"
   parent:
     type: periodical
     title: "Brain and Cognition"
     volume: 73
+    issue: 1
   url:
-    value: "https://doi.org/10.1016/j.bandc.2010.03.002"
-    date: 2026-10-30
+    value: "https://europepmc.org/article/MED/20381226"
+    date: 2026-11-07
+  note: "Read the abstract only. No open full text: CNR's repository record has no file, and ScienceDirect refused the browser."
```

## E63: Draper, Giles et al. 2015, IRCRA position statement

**Not cited.** Neither E63 nor F19, the duplicate that `src-map.typ` maps onto
it, appears in `book/chapters`, `book/exercises.typ`, the site or any worktree
branch, and it isn't in the first edition's chapters either. The book doesn't
mention IRCRA. Only the research dossiers (`E-reading.md`, `F-grades.md`)
refer to it.

**Copy.** The authors' version is open on HAL (hal-03545405, CC BY-NC-ND 4.0,
8 pages). HAL shows scripts an Anubis bot check, but in the browser it cleared
by itself and the record and PDF opened. The Derby repository copy
(derby-repository.worktribe.com/output/798985) stays on a Cloudflare check.
The Wayback copy of the HAL PDF from 2 March 2024 downloads in curl as a real
PDF (200, application/pdf), so it is the copy an automated check can reach. I
read it: the paper was accepted on 8 October 2015 and has 29 authors.
Crossref gives Sports Technology 8(3–4):88–94, October 2015.

One finding for the dossier: the paper's own example gives "V6 (Font 7a,
IRCRA 20)". That confirms the V6 = 20 anchor which `F-grades.md` marks as
unverified.

**Proposed yml change.** Because nothing cites it, E63 can go, together with
F19 and their two lines in `book/source-kinds.yaml`. The book only prints
cited sources, so it won't change. If you keep it for the dossiers, correct
it:

```diff
   url:
-    value: "https://hal.archives-ouvertes.fr/hal-03545405"
-    date: 2026-10-30
-  note: "About two dozen further co-authors; full text not accessed"
+    value: "https://web.archive.org/web/20240302031421/https://hal.science/hal-03545405v1/file/2016-Draper%20et%20al.-SPORT%20TECHNO.pdf"
+    date: 2026-11-07
+  note: "27 further co-authors. Read in full: the authors' version on HAL (hal-03545405), through the Wayback copy of 2 March 2024, since HAL shows scripts a bot check. Not cited in the book."
```

## G48 → E34: Sanchez et al. 2012, previewing a route

**Already merged.** G48 is gone from `G-sources.yml`, and chapter 9 now
carries factcheck-3's wording with E34. The only traces are in the dossier
`G-considerations.md` (lines 237 and 421), which is fine. The Wiley page
behind the DOI still shows a Cloudflare check, so the open copy below matters
for E34.

**Copy.** The University of Groningen's research portal has the paper's record
with the full abstract. It lists the publisher's final version as a PDF under
the Taverne licence. The record opens in the browser and in curl (200)
without a check. The PDF link itself stays on a Cloudflare check, so I didn't
read the full text. Liège's ORBi copy is "request a copy" only, and Louvain's
DIAL file needs a login. E34's current url, a summary in Coaching
Science Abstracts (coachsci.sdsu.edu), also opens and reports the same
results. But it is a third party's summary, not the paper.

**Citations:**

| Line | Sentence | Verdict |
|---|---|---|
| `02-reading.typ` 17 | "In one study, 29 male climbers on roped indoor routes had three minutes to look at some routes before they climbed them. Looking didn't change how often they reached the top, but they did make fewer and shorter stops. Part of that held up once the authors allowed for ability, with the experts gaining most #src("E34")." | Supported by the abstract: 29 male climbers on indoor sport routes, a 3-minute preview on one route at each level, and no change in route completion. Climbers made "fewer, and shorter stops", and with ability allowed for, only the shorter stops remained, "with expert climbers benefiting most". |
| `a-troubleshooting.typ` 141 | "Read the problem first so you stop less." (cell cites E7, E8, E10, E34) | Supported. E34 says nothing about pump, which the other three sources cover. |
| `09-considerations.typ` 225 | "Reading a problem before you climb it can mean fewer and shorter stops #src("E34", "G44")." | Supported, though the study used roped routes rather than boulder problems. Chapter 2 already says so. |

**Proposed yml change.** Point the url at the Groningen record. The UUID form
of the URL redirects to the current page and survives a change of slug.

```diff
 E34:
   ...
   url:
-    value: "https://coachsci.sdsu.edu/csa/vol185/sanchez1.htm"
-    date: 2026-10-30
+    value: "https://research.rug.nl/en/publications/f9fd5950-5f31-4f14-9111-55e22bbff301"
+    date: 2026-11-07
+  note: "Same paper as the former G48. Read the abstract in the University of Groningen's record, which lists the publisher's PDF; the PDF itself shows a bot check."
```

## F37 and F17: uncited

Neither appears in `book/chapters`, `book/exercises.typ`, the site or any
worktree branch. Their only uses in `book/` are their lines in
`source-kinds.yaml`.

- **F37** (Castle Climbing Centre, Louis Parkinson coaching workshops). The
  Wayback availability API still has no copy, and the yml note already says
  it isn't cited. factcheck-2 removed its sentences.
- **F17** (Baláš 2012). It went when two of the three body-mass studies were
  cut (`streamline-08-appendices.md`). Its note doesn't say it's uncited.

Both entries can go as far as the book is concerned, together with their lines
in `book/source-kinds.yaml`. `F-grades.md` still cites both by ID, so deleting
them leaves those references dangling in the dossier. If you keep F17, add
"No longer cited in the text" to its note, as F37 has.

## Access dates

The appendix says web pages were accessed in October 2026. The new url dates
are in November, as the H entries' already are (2026-11-06). Since the
bibliography leaves the dates out, only that sentence would need "October and
November 2026".
