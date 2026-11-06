# Template changes for the third revision

- `book/template.typ`, `figtools/figs_icons.py`: `#technique` takes an optional `small:`, set straight after the tall note and labelled "Small climbers.", with a new icon (`icon-small.svg`, also usable as `#notebox(..., icon: "small")`).
- `figtools/figs_icons.py`: the tall and small icons share two helpers; `icon-tall.svg` comes out byte for byte the same.
- `book/key-alias.typ`: added corner→stemming, volume-mantle→mantle, hip-pop→deadpoint, counter-kick→cutting-loose, and lache, paddle-dyno, tic-tac and double-clutch→comp-moves.
- `book/template.typ`: `tref` now prefers an entry with the exact key and only then follows an alias, so an entry stays reachable until its merge. A key with no entry either way still shows as [?key].
- `book/template.typ`: "Referenced from" follows the same rule, because each reference records the key it resolved to. Before this change, adding the aliases would have emptied the backlinks of every entry still waiting to be merged.
- `book/template.typ`: `category-table` sorts on the grade alone and `grade-techniques` on the category alone, so chapter order decides the rest. The A–Z is unchanged and stays alphabetical.
- `book/template.typ`: `readbox` sets lists under bold labels (`*Look for*`, `*Symptoms*`). Each list keeps the old sticky items, a label stays with its list, and the old form sets exactly as before.
- `book/template.typ`: `--input flow=fit` and `--input flow=<fraction>` let entries share pages. The default is unchanged, and the page counts are below.
- `book/template.typ`: `--input evidence=1` adds an "Evidence" line before "Sources", counted from `book/source-kinds.yaml` after applying the source map. Without the input the file isn't read.
- `tools/check_order.py` (new), `build.sh`: after `check_fit`, the build lists each step that links to a higher-graded technique. It is informational and exits 0.
- `book/chapters/10-appendices.typ`: the bibliography reads source letter H, and a source file that is empty or has only comments counts as no sources.

**Not done:** item 5 of the template task (a second figure inside an entry). The request said "no, ignore 5", so `#technique` has no way to place one yet. If that request meant item 5 of the analysis instead, this still needs adding.

## Page counts of the current text

| Option | Pages | After `./build.sh` |
|---|---|---|
| default | 268 | 265 |
| `flow=fit` | 268 | 265 |
| `flow=0.5` | 266 | 263 |
| `flow=0.4` | 264 | 261 |
| `flow=0.3` | 260 | 257 |

`./build.sh` regenerates `book/errata.json` from the newest section of `CHANGELOG.md`, which has no errata yet, so the three pages of corrections to the first edition drop out of the draft.

`flow=fit` sets the same text as the default, because no entry fits whole in the space another leaves. Grade heads and film strips still start a page; letting them share too (tried in a scratch copy only, before the errata changed) gave 262, 261 and 257 pages for 0.5, 0.4 and 0.3.

## Parts of an entry

`parts:` replaces the second figure listed as not done above.

- `book/template.typ`: `#technique` takes an optional `parts:`, an array of dictionaries with `name` and `how` (numbered steps or a short paragraph) and optional `figure`, `caption` and `figure-wide`. Parts come after the main steps and figure and before the reading box.
- `book/template.typ`: a part's name uses the same label as "How to do it", with the same spaces, and stays with its first step. Its steps look like the main steps, and every space scales with `k`.
- `book/template.typ`: a part's figure follows the rule for the main figure and uses the same code: up to 92 mm wide it sits beside the steps, and wider it goes below them. A part with a figure stays whole on one page, so the figure can't be parted from its steps. A part with no figure stays whole under a third of a page and otherwise breaks like the main steps.
- `book/template.typ`: each part's name goes in the index with a bold page number, and only in the set copy, not the measured one. An alias with the same name no longer adds a "(see ...)" line, which would have given one move two index lines. The A–Z still lists the alias and points to the entry.
- `book/template.typ`: in an entry with parts, a wide main figure stays in the flow, so a part can't land ahead of it. An entry's own `how:` may be left out.
- `book/template.typ`: the page estimate now counts the space that whole parts leave at the foot of a page. An entry with parts tightens its spaces only to 0.6, and only when that saves a page, because tight spaces above white feet looked wrong.
- Entries without parts: all 265 pages came out identical at 100 dpi before and after, and 33 sampled pages at 200 dpi. `flow=0.4` and `evidence=1` were also identical. `tools/check_fit.py` still reports no spills.

A part that moves whole can leave the foot of the page before it short: about 40% of the page in the test with a wide figure. Four parts that each have a figure took five pages at full space in the test.
