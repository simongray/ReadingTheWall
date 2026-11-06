# Colour in the figures

The book is read mostly on a monochrome e-reader, so every figure is a grey
drawing first and `figtools/paint.py` adds the colour at the end of a build.
`build_all.py --grey` leaves it out. This page says why the colours are what
they are. The values live in `paint.py`.

## Rules

- **A colour keeps its grey.** Each colour lands on the same panel level as
  the grey it replaces, under every sum a device might use to turn colour into
  grey. The build fails if one drifts. Yellow holds keep a lighter grey of their
  own, as explained below.
- **One problem, one colour, and the colour says the grade.** On a real wall a
  problem is one colour and the wall as a whole has many. So a figure's holds
  share one colour. In a technique entry the colour follows the entry's grade, as
  at Boulders, so it agrees with the entry's tab. A figure with no known grade
  takes teal or raspberry, which claim no grade. The cover and the atlases show
  many holds at once and use several.
- **The shades on a hold are its own colour.** Chalk and light are white on top
  of the colour, so the tone between the two is the colour mixed with white. A
  neutral grey there looks like a second material. Bolts stay grey, since they're
  metal.
- **Holds and volumes have a surface.** Both are rough as sandpaper and stand out
  from the wall, so a hold has a lit rim, a dark crescent, a grain of specks and a
  shadow on the wall. A faceted volume shows its form through facets that follow
  the light, and takes the grain and the shadow. Unlike colour, this is part of the
  grey drawing and shows on a monochrome screen. The grain is dots, because
  gradients band on e-ink. Small shapes stay flat, and the ornaments have no wall
  to cast a shadow on.
- **Muscles at work are red.** The dots mark what many figures are about, and red
  is what most readers expect of a muscle (our judgement; we found no source for
  the convention). No red holds the near-black the dots on the left limbs used to
  have, so all the dots now sit on one lighter grey and stay crisp on the panel.
- **Grade tabs follow the walls at Boulders,** the Danish gym chain, and darken as
  the grade rises. On a monochrome screen the colour is gone, but the tone still
  says how hard the grade is. Light tabs take black figures and an outline, and
  dark ones take white figures. Boulders publishes no V grades, so the table comes
  from Simon, who climbs there: green up to V1, then yellow, orange, blue, purple
  and red for V2 to V6, and black from V7.
- **The climber, the wall and the volumes stay neutral,** apart from the red on
  the muscles. Colour then only ever marks a hold, a muscle at work or the way your
  body moves. A coloured volume would compete with the holds and blur what their
  colour means.
- **Colour goes on outlined areas.** Lines, labels and force arrows stay in ink.
  The muscle dots are the one exception. At about 0.38 mm they're close to the
  finest colour Kaleido 3 can show, so they may look dark there.
- **Block arrows are amber.** They're the one colour that teaches, and they mark
  what the figure is about: where the hips or the whole body go.
- **Text never names a colour.** Most readers can't see it. A caption says
  "the hold", never "the blue hold".
- **Draw and judge a figure in grey.** Colour can't rescue a figure that doesn't
  work without it.

## Why these colours

**Each colour suits the grey it has to match.** Holds stay on #555555 and block
arrows on #cccccc, and each hue has a lightness where it's at its strongest. In
the calculations for this page, blues and violets kept the most colour at the
holds' darkness and teal kept the least, while amber stayed strong at the arrows'
lightness. Orange turns brown at the holds' darkness, so its rim, chalk and grain
keep their full colour, where other holds mix with white.

**Yellow holds are the one exception to keeping a grey.** At the holds' darkness
yellow turns olive, which doesn't read as yellow at all. So yellow holds sit on
#aaaaaa with shades of their own, and a monochrome screen shows them lighter than
other holds. Simon chose this after seeing both versions. It suits the grade tabs,
which also get lighter the easier the grade.

**Muted colours, because the sums disagree about strong ones.** The PDF engines
weight red, green and blue at about 0.30, 0.59 and 0.11, and Android at 0.213,
0.715 and 0.072. Rockchip's e-ink compositor uses 11, 16 and 5 out of 32 and
drops the low bits instead of rounding. Typst tags its colours as sRGB, so a
colour-managed engine follows luminance instead. Pure green comes out at 150 or
182 of 255 under the first two sums, while a muted colour hardly moves. Onyx's
own demo green lands on level 6, 8 or 9 of the panel's 16, depending on the sum.
The palette holds its level under all of these.

**Hold colours add a little meaning, and appeal.** They repeat the grade on the
entry's tab, which only helps a reader who knows Boulders' circuits, and they make
the book look like a gym. Nothing in a figure depends on them. The amber arrows
are the part with evidence behind them. A meta-analysis found
colour cues in pictures helped both retention and transfer (g = 0.44 and 0.39),
but no study we found tests static drawings of a sport. Studies of emotional
design lean positive, while decoration that adds irrelevant content hurts, which
is why colour here adds no new shapes.

**Nothing is lost for colour-blind readers.** Red and green holds can look alike
to them, but all the holds already look alike to a reader on a monochrome screen,
and every figure has to work for that reader. Blue against amber holds up well
under red-green colour blindness, and Paul Tol's palette for greyscale printing
uses the same two hues.

## What Onyx does

Onyx publishes little. Its developer guide asks for 16-level greys as the main
colours of a page, and doesn't discuss colour to grey. Its pen demo uses #000084,
#FF6163, #00B036 and #404040, which is sample code and may not match its apps.
Its marketing mentions 16 pen colours and shows red, yellow, blue, green and
purple, with no values. We didn't find the Notes palette or NeoReader's sum.

On the Max models, firmware V3.1 replaced Contrast with Dark Color Enhancement
(default 30) and Light Color Filter (default 0). The manual says the first "turns
darker colors to black". Which tones it reaches isn't documented, and neither is
whether it acts before or after the colour becomes grey.

On Kaleido 3, the panel in Onyx's colour tablets, colour has half the resolution
of black and white (150 against 300 ppi). That's why colour stays on areas. One
reviewer found red closer to brick on every Kaleido 3 device, which is near the
hold colour here anyway.

## What's still open

`tools/colour_chart.py` makes a chart for settling the first three on a real
device.

- Which sum the Boox uses. The palette is built to survive any of them.
- Whether Dark Color Enhancement treats a colour and its matching grey alike. If
  it works on each channel before the grey, the darkest colours could turn darker
  than #555555 does. This is the main risk left.
- Whether the Boox's reader treats two colour spaces alike. Typst writes a
  figure's neutral greys in an ICC grey space and its colours in ICC sRGB.
- How the colours look on real colour e-paper. The simulations are rough, and we
  found no measured colour data for Kaleido 3.

## How it was checked

Each figure was rendered in grey and in colour, sent through the sums and reduced
to the panel's 16 levels. In figures without yellow holds this changed under 0.1%
of the pixels by one level and none by two, and only figures with yellow holds
changed by more. Before yellow holds became lighter, the whole book changed under
0.01% by one level and none by two, on the same number of pages, through the
conversions in Poppler, PDFium and MuPDF with colour management on or off. So in
these engines the two colour spaces don't pull the builds apart. The changes are
probably anti-aliased edges, though nobody looked at them one by one. No real
device has seen the figures yet.

## Sources

Colour to grey:
[MuPDF](https://raw.githubusercontent.com/ArtifexSoftware/mupdf/master/source/fitz/color-fast.c),
[PDFium](https://pdfium.googlesource.com/pdfium/+/refs/heads/main/core/fxge/dib/fx_dib.h),
[Poppler](https://sources.debian.org/src/poppler/latest/poppler/GfxState.cc/),
[Android](https://android.googlesource.com/platform/prebuilts/fullsdk/sources/+/refs/heads/androidx-transition-release/android-34/android/graphics/ColorMatrix.java),
[Rockchip](https://github.com/TinkerBoard-Android/rockchip-android-hardware-rk35-einkhwc/blob/HEAD/rgb888_to_gray_256_neon.s).

Onyx:
[developer guide](https://github.com/onyx-intl/OnyxAndroidDemo/blob/master/doc/Eink-Develop-Guide.md),
[pen demo colours](https://github.com/onyx-intl/OnyxAndroidDemo/blob/master/app/OnyxPenDemo/src/main/res/values/colors.xml),
[colour coding](https://shop.boox.com/blogs/news/master-color-coding-with-boox-color-epaper-tablets),
[Max firmware notes](https://downloads.boox.com/download/max),
[manual](https://ebookreader.dk/images/upload/Onyx%20BOOX%20Go%2010%203%20User%20Manual.pdf).

Boulders:
[first visit](https://boulders.dk/frstegang),
[Aarhus listing](https://www.visitdenmark.com/denmark/plan-your-trip/boulders-aarhus-gdk1147322).

Colour e-paper:
[E Ink on Kaleido 3](https://www.eink.com/brand/detail/Kaleido3),
[a reviewer's comparison](https://kurotimedesign.blogspot.com/2024/05/boox-tab-mini-c-vs-kobo-colour-vs.html).

Colour as a cue:
Schneider et al. 2018, [doi:10.1016/j.edurev.2017.11.001](https://doi.org/10.1016/j.edurev.2017.11.001)
([German review with the table](https://www.clearinghouse.edu.tum.de/wp-content/uploads/2018/12/CHU_KR-22_-Schneider_2017_Lernmaterial_Hervorhebungen.pdf));
Ozcelik et al. 2009, [doi:10.1016/j.compedu.2009.03.002](https://doi.org/10.1016/j.compedu.2009.03.002);
Brom et al. 2018, [doi:10.1016/j.edurev.2018.09.004](https://doi.org/10.1016/j.edurev.2018.09.004);
Sundararajan & Adesope 2020, [doi:10.1007/s10648-020-09522-4](https://doi.org/10.1007/s10648-020-09522-4).

Seeing colour:
Mullen 1985, [doi:10.1113/jphysiol.1985.sp015591](https://doi.org/10.1113/jphysiol.1985.sp015591).

Palettes:
[Paul Tol](https://sronpersonalpages.nl/~pault/),
[Okabe & Ito](https://jfly.uni-koeln.de/color/),
[Oklab](https://bottosson.github.io/posts/oklab/).
