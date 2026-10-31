# QR code check

A check of the QR codes in the technique entry footers (31 October 2026).
`book/template.typ` prints a code for each of the first two Watch links of
an entry, numbered 1 and 2.

All 35 codes pass. Each one decodes to exactly its Watch URL, at 300 dpi
and at the e-reader's 197 dpi. Nothing needs to change for the codes to
scan.

## What was checked

The template changed while I worked, so I checked two builds:

- **15 mm build** (template as of 01:16, 214 pages). The live build failed
  at 01:43 (see Notes), so this one is from a copy with that fixed.
- **13 mm build** (template as of 01:50, 195 pages, built from a copy of
  the live sources). This is the current design. The only later template
  change, at 01:51, is to `show columns` and doesn't touch the footer.

In both builds:

- 26 entries have Watch links, 35 links in all. No entry has more than two,
  so every link has a code. Each of the 26 pages with "Scan to watch" holds
  one entry's codes, in the same order as the entries in the chapters.
- Every code decodes to exactly one symbol, with exactly its Watch URL. I
  decoded the whole page (no stray or missing symbols), each code cropped
  on its own, and the pair of codes together (left to right gives link 1
  then link 2).
- The digit under each code matches its place in the Watch list, and the
  Watch line reads "1 Title (Channel); 2 Title (Channel)" on the same page
  as the codes.
- Each code is a link: its link annotation covers the code exactly and
  points to the same URL. The title links in the Watch line point to the
  same URLs and cover the right titles.
- At 197 dpi (207 ppi × 0.95), every code still decodes, both as rendered
  and after mapping to the panel's 16 greys with Floyd–Steinberg dithering
  and a 15:1 contrast, as in `eink-report.md`.

## How much margin there is

The codes are QR version 3 (29 modules) for the YouTube links. Two are
smaller or larger: version 2 for `vimeo.com/13761179` and
`gripped.com/?p=40443`, and version 5 (37 modules) for the 80-character
lacrux.com pogo link (Pogo, code 1).

At 13 mm and 197 dpi a version 3 module is 3.5 px and a version 5 module
2.7 px. To find the limit, I decoded each cropped code from pages rendered
at lower resolutions:

| Page resolution | 15 mm build | 13 mm build |
|----------------:|------------:|------------:|
| 197 dpi         | 35 of 35    | 35 of 35    |
| 150 dpi         | 35          | 35          |
| 120 dpi         | 35          | 33          |
| 100 dpi         | 34          | 30          |
| 90 dpi          | 34          | 10          |
| 80 dpi          | 17          | 0           |

Decoding gets unreliable below about 2.6 px per module. On the 197 dpi
panel, that puts the smallest safe width at about 10 mm (13 mm × 150/197),
so 13 mm leaves roughly 30% headroom. Going below 11 mm isn't advisable.

## Notes

- **Quiet zone.** The 5 pt gap between the two codes is 1.76 mm, which is
  3.9 modules of a version 3 code at 13 mm. The QR standard asks for 4. The
  caption (3 pt above) and the digits (2.5 pt below) also sit inside the
  quiet zone. zbar reads every code regardless, but phone scanners like more
  white space. A 6 pt gap between the codes would restore the 4 modules.
- **Frog position.** The video title starts with an episode number, so the
  Watch line reads "1 11 Neil Greshams Masterclass - Frogging". Dropping
  the "11" in `04-body.typ` would avoid the clash with the code number.
- **Build break at 01:43.** Four entries in `03-feet.typ` and
  `05-hands.typ` had `aliases: ("high foot")`, which is a string rather than
  an array, and the template called `.join` on it. Since 01:50 the template
  accepts a string, and the live build compiles again.
- `tools/merge_sources.py` left `book/src-map.typ` unchanged.

The check scripts (`watchlist.py`, `qrcheck.py`) and the renders are in the
session scratchpad, under `qrcheck/`.
