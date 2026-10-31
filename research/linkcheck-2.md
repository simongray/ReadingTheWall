# Link check 2, 2026-10-31

Second pass over every external link, compared with research/linkcheck.md. Nothing in
the chapters or the yml files was edited. Line numbers are as of the check and may
have shifted since.

Method. Each distinct URL got a HEAD request first and a GET if HEAD did not return 2xx
(curl, redirects followed, Chrome-style User-Agent, 15 s timeout). Every failure was
retried slowly, one request per host at a time, and the 429s and timeouts once more
after a pause. Pages that answered HEAD with 200 were also fetched and their titles
scanned for bot-check or "not found" pages. YouTube links went through the oEmbed
endpoint and the Vimeo link through Vimeo's, and each returned title and channel was
compared with the title and channel in the `watch:` argument. The five DOIs that
answered 403 were checked in the doi.org handle API.

**OK: 270 of 419 link occurrences (236 of 376 distinct URLs).**

| Status | Occurrences | Distinct URLs |
|---|---|---|
| OK | 270 | 236 |
| Redirected (final URL differs) | 107 | 98 |
| Broken (404/410, DNS) | 1 | 1 |
| Blocked or rate-limited (403, 429, bot-check page) | 38 | 38 |
| Timed out | 3 | 3 |

## Watch links (the QR codes)

35 links in 26 entries (30 distinct URLs): 33 OK, 2 redirected, none broken, none
blocked, none timed out. All 28 videos (27 YouTube, 1 Vimeo) exist and every title and channel
still matches the `watch:` text. The two redirects are `pogo` #1 (the lacrux.com article
adds `www.`) and `dynamic-slab` (gripped.com `?p=40443` is a short link that redirects to
the article slug). Both work as they are, and the QR code resolves through the redirect.

## Non-OK links

Sorted by severity, then by file. "Cosmetic" redirects only add or drop `www.`, a trailing
slash, `?scope=anon` or similar; "moved" redirects change the path or host; "short link" is
a WordPress `?p=` URL that redirects to the article slug.

| File | Entry or key | URL | Status | Suggested fix |
|---|---|---|---|---|
| research/F-sources.yml:343 | F37 | https://www.castle-climbing.co.uk/events/louis-parkinson-coaching-workshops | 404 | Already known (F37): kept deliberately, its note records the removal |
| research/E-sources.yml:407 | E39 | https://www.sponet.de/sponet/Record/4055899?lng=en | timed out (curl 28, SSL connection timeout after 15 s) | None obvious. The host accepts the TCP connection but sends nothing, on https and on plain http. Retry in a browser |
| research/F-sources.yml:169 | F17 | https://lida.sport-iat.de/ta/Record/4056114 | timed out (curl 28, SSL connection timeout after 15 s) | None obvious. The host accepts the TCP connection but sends nothing, on https and on plain http. Retry in a browser |
| research/G-sources.yml:330 | G25 | https://lida.sport-iat.de/dav/Record/4083000 | timed out (curl 28, SSL connection timeout after 15 s) | None obvious. The host accepts the TCP connection but sends nothing, on https and on plain http. Retry in a browser |
| research/A-sources.yml:158 | A14 | https://shop.frictionlabs.com/blogs/climb-your-impossible/how-it-works-the-toehook | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/A-sources.yml:191 | A17 | https://shop.frictionlabs.com/blogs/climb-your-impossible/how-it-works-the-kneebar | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/A-sources.yml:414 | A37 | https://rockrun.com/blogs/the-flash-rock-run-blog/technique-tips-article-1-overhangs-training-and-skills | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/B-sources.yml:270 | B23 | https://www.ukclimbing.com/articles/series/neil_gresham_technique_and_training/posture_in_climbing-12297 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/B-sources.yml:756 | B67 | https://www.ukclimbing.com/forums/starting_out/backstepping_properly_-_how_to_drive_upwards-684874 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/B-sources.yml:767 | B68 | https://www.ukclimbing.com/forums/rock_talk/good_technique__bent_arms_on_vertical_rock-453722 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/C-sources.yml:258 | C24 | https://thieme-connect.de/products/ejournals/html/10.1055/s-0030-1267230 | 200, but a bot-check page ("Please wait") | None. Bot-check page, content not visible to curl |
| research/C-sources.yml:452 | C39 | https://frictionlabs.com/blogs/climb-your-impossible/how-it-works-the-mantle | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/C-sources.yml:572 | C51 | https://www.ukclimbing.com/articles/page.php?id=11848 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/C-sources.yml:583 | C52 | https://www.ukclimbing.com/articles/page.php?id=12172 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/C-sources.yml:594 | C56 | https://atomikclimbingholds.com/how-to-use-the-nine-basic-types-of-climbing-handholds | 403 Cloudflare challenge | None. Recheck in a browser |
| research/C-sources.yml:605 | C57 | https://www.thecrag.com/en/article/glossary/gaston | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/D-sources.yml:11 | D1 | https://www.thecrag.com/en/article/glossary/deadpoint | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/D-sources.yml:22 | D2 | https://www.thecrag.com/en/article/glossary/dynamic-move | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/D-sources.yml:243 | D22 | https://shop.frictionlabs.com/blogs/climb-your-impossible/connors-world-dynoing-basics | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/D-sources.yml:255 | D23 | https://frictionlabs.com/blogs/climb-your-impossible/connors-world-the-secret-to-pogoing | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/D-sources.yml:469 | D46 | https://rockprodigytraining.proboards.com/thread/927/dynos-dyno-training | 202, empty body (bot check) | None. Bot-check page, content not visible to curl |
| research/D-sources.yml:501 | D51 | https://outdoors.codidact.com/posts/55003 | 403 Cloudflare challenge | None. Recheck in a browser |
| research/E-sources.yml:134 | E13 | https://www.ukclimbing.com/articles/skills/series/neil_gresham_technique_and_training/technique_-_heel_hooking-11327 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/E-sources.yml:144 | E14 | https://www.ukclimbing.com/articles/skills/bouldering_skills_topping_out-6849 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/E-sources.yml:154 | E15 | https://www.ukclimbing.com/articles/page.php?id=10957 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/E-sources.yml:164 | E16 | https://www.ukclimbing.com/articles/skills/series/neil_gresham_technique_and_training/ | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/E-sources.yml:174 | E17 | https://www.ukclimbing.com/articles/page.php?id=3924 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/E-sources.yml:19 | E2 | https://rockrun.com/blogs/the-flash-rock-run-blog/technique-tips-article-3-aretes-training-and-skills | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/E-sources.yml:293 | E30 | https://rockrun.com/blogs/the-flash-rock-run-blog/route-reading-how-to-guide | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/E-sources.yml:303 | E31 | https://shop.frictionlabs.com/blogs/climb-your-impossible/6-ways-to-read-climbing-gym-routes | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/E-sources.yml:364 | E36 | https://iris.cnr.it/handle/20.500.14243/50351 | 403 Cloudflare challenge | None. Recheck in a browser |
| research/E-sources.yml:432 | E41 | https://rockrun.com/nl/blogs/the-flash-rock-run-blog/climbing-at-your-limit-tactics-training-and-skills | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/E-sources.yml:462 | E44 | https://www.frictionlabs.com/blogs/climb-your-impossible/11-simple-tips-on-projecting | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/E-sources.yml:512 | E49 | https://www.ukclimbing.com/articles/page.php?id=7406 | 403 Cloudflare challenge | None. Cloudflare challenge, recheck in a browser |
| research/E-sources.yml:619 | E63 | https://hal.archives-ouvertes.fr/hal-03545405 | 200, but a bot-check page ("Making sure you're not a bot") | None. Bot-check page, content not visible to curl |
| research/E-sources.yml:9 | E1 | https://rockrun.com/blogs/the-flash-rock-run-blog/technique-tips-article-2-slabs-training-and-skills | 429 rate-limited (Cloudflare, Retry-After 60 s; four attempts over several minutes) | None. Rate-limited, recheck later in a browser |
| research/G-sources.yml:184 | G15 | https://mediatum.ub.tum.de/1688232 | 200, but a bot-check page ("Making sure you're not a bot") | None. Bot-check page, content not visible to curl |
| research/G-sources.yml:587 | G47 | https://doi.org/10.2466/pms.2002.95.1.3 | 403 Cloudflare challenge | None. DOI is registered in the handle API, resolves to the publisher |
| research/G-sources.yml:604 | G48 | https://doi.org/10.1111/j.1600-0838.2010.01151.x | 403 Cloudflare challenge | None. DOI is registered in the handle API, resolves to the publisher |
| research/G-sources.yml:621 | G49 | https://doi.org/10.1207/s15326969eco1803_1 | 403 Cloudflare challenge | None. DOI is registered in the handle API, resolves to the publisher |
| research/G-sources.yml:660 | G52 | https://doi.org/10.1080/1750984X.2012.723728 | 403 Cloudflare challenge | None. DOI is registered in the handle API, resolves to the publisher |
| research/G-sources.yml:809 | G65 | https://doi.org/10.1136/bjsports-2023-106994 | 403 Cloudflare challenge | None. DOI is registered in the handle API, resolves to the publisher |
| research/A-sources.yml:34 | A3 | https://www.climbing.com/trainning/training-7-simple-drills-to-improve-footwork-and-technique/?scope=anon | 200 via redirect (moved) | use https://www.climbing.com/skills/training-7-simple-drills-to-improve-footwork-and-technique/?scope=anon |
| research/A-sources.yml:488 | A44 | https://www.mountainproject.com/forum/message/113645869 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/113643425/progressing-from-v2-to-v3-boulders#ForumMessage-113645869 |
| research/A-sources.yml:500 | A45 | https://www.mountainproject.com/forum/message/112416828 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/112406184/technical-heel-hooks#ForumMessage-112416828 |
| research/B-sources.yml:29 | B3 | https://thebmc.co.uk/bmc-fundamentals-of-climbing-3 | 200 via redirect (moved) | use https://thebmc.co.uk/en/bmc-fundamentals-of-climbing-3 |
| research/C-sources.yml:332 | C29 | https://ojs.ub.uni-konstanz.de/cpa/article/view/6511/5876 | 200 via redirect (moved) | use https://ojs.ub.uni-konstanz.de/cpa/article/download/6511/5876 |
| research/C-sources.yml:528 | C47 | https://www.mountainproject.com/forum/message/111696217 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/111692944/trouble-getting-past-v3s#ForumMessage-111696217 |
| research/C-sources.yml:55 | C5 | https://www.climbing.com/.amp/skills/climbing-techniques-how-to-mantel?scope=anon | 200 via redirect (moved) | use https://www.climbing.com/skills/climbing-techniques-how-to-mantel/?scope=anon |
| research/D-sources.yml:449 | D44 | https://www.frontiersin.org/articles/10.3389/fspor.2025.1609133/full | 200 via redirect (moved) | use https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2025.1609133/full |
| research/D-sources.yml:66 | D6 | https://www.climbing.com/skill/learn-this-master-dynos-with-tips-from-sean-mccoll?scope=anon | 200 via redirect (moved) | use https://www.climbing.com/skills/learn-this-master-dynos-with-tips-from-sean-mccoll/?scope=anon |
| research/E-sources.yml:263 | E26 | https://www.mountainproject.com/forum/message/119641656 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/119641220/question-about-sit-starts#ForumMessage-119641656 |
| research/E-sources.yml:349 | E35 | https://frontiersin.org/articles/10.3389/fpsyg.2019.01294/full | 200 via redirect (moved) | use https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.01294/full |
| research/E-sources.yml:422 | E40 | https://www.frontiersin.org/articles/10.3389/fspor.2022.790336/full | 200 via redirect (moved) | use https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.790336/full |
| research/E-sources.yml:502 | E48 | https://www.mountainproject.com/forum/message/112433997 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/112430160/gym-route-setting#ForumMessage-112433997 |
| research/F-sources.yml:133 | F15 | https://ukbouldering.com/board/index.php/topic,33968.msg691070.html | 200 via redirect (moved) | use https://ukbouldering.com/threads/approximating-lattice%E2%80%99s-finger-strength-dataset.33968/#post-691070 |
| research/F-sources.yml:421 | F44 | https://www.mountainproject.com/forum/message/113643437 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/113643425/progressing-from-v2-to-v3-boulders#ForumMessage-113643437 |
| research/F-sources.yml:432 | F45 | https://www.mountainproject.com/forum/message/113169909 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/113169743/bouldering-reaching-for-the-next-level#ForumMessage-113169909 |
| research/F-sources.yml:444 | F46 | https://www.mountainproject.com/forum/message/126916094 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/126915631/tips-for-moving-from-v5-to-v6-indoors#ForumMessage-126916094 |
| research/F-sources.yml:455 | F47 | https://www.mountainproject.com/forum/message/125340907 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/125337332/what-grade-were-you-able-to-climb-after-1-yr?page=2#ForumMessage-125340907 |
| research/G-sources.yml:382 | G29 | https://www.frontiersin.org/articles/10.3389/fspor.2022.862782/full | 200 via redirect (moved) | use https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.862782/full |
| research/G-sources.yml:491 | G40 | https://www.frontiersin.org/articles/10.3389/fspor.2022.895588/full | 200 via redirect (moved) | use https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2022.895588/full |
| research/G-sources.yml:737 | G59 | https://www.climbing.com/.amp/skills/3-tips-for-safer-bouldering-falls/?scope=anon | 200 via redirect (moved) | use https://www.climbing.com/skills/3-tips-for-safer-bouldering-falls/?scope=anon |
| research/G-sources.yml:771 | G62 | https://thebmc.co.uk/climbing-wall-safety-resources | 200 via redirect (moved) | use https://thebmc.co.uk/en/climbing-wall-safety-resources |
| research/G-sources.yml:83 | G7 | https://www.mountainproject.com/forum/message/200228943 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/127376107/does-being-taller-make-climbing-easier-answering-this-question-with-data?page=6#ForumMessage-200228943 |
| research/G-sources.yml:94 | G8 | https://www.mountainproject.com/forum/message/117444360 | 200 via redirect (moved) | use https://www.mountainproject.com/forum/topic/117347945/grades-information-gathering-and-leading-near-your-limit-as-a-shorttallnon-avera?page=9#ForumMessage-117444360 |
| book/chapters/07-terrain.typ:391 | dynamic-slab | https://gripped.com/?p=40443 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/top-olympian-tomoa-narasaki-teaches-coordination/ |
| research/A-sources.yml:12 | A1 | https://gripped.com/?p=48289 | 200 via redirect (short link) | use https://gripped.com/profiles/10-terms-to-understand-climbing-footwork/ |
| research/A-sources.yml:169 | A15 | https://trainingforclimbing.com/?p=11989 | 200 via redirect (short link) | use https://trainingforclimbing.com/develop-fantastic-footwork-with-heel-hook-and-toe-hook-technique/ |
| research/A-sources.yml:202 | A18 | https://philarockgym.com/?p=29204 | 200 via redirect (short link) | use https://philarockgym.com/knee-bars-the-coolest-move-in-climbing/ |
| research/A-sources.yml:213 | A19 | https://gripped.com/?p=31309 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/10-techniques-for-climbing-overhangs/ |
| research/A-sources.yml:257 | A23 | https://philarockgym.com/?p=26333 | 200 via redirect (short link) | use https://philarockgym.com/enhance-your-climbing-with-this-essential-skill-foot-switching/ |
| research/A-sources.yml:268 | A24 | https://gripped.com/?p=47674 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/five-fun-drills-to-improve-your-climbing-footwork/ |
| research/A-sources.yml:337 | A30 | https://philarockgym.com/?p=26439 | 200 via redirect (short link) | use https://philarockgym.com/what-is-smearing-a-simple-guide-to-this-climbing-technique/ |
| research/A-sources.yml:348 | A31 | https://philarockgym.com/?p=27271 | 200 via redirect (short link) | use https://philarockgym.com/a-quick-climbing-tutorial-on-high-stepping/ |
| research/A-sources.yml:359 | A32 | https://philarockgym.com/?p=30890 | 200 via redirect (short link) | use https://philarockgym.com/mastering-foot-sequencing-in-climbing/ |
| research/A-sources.yml:391 | A35 | https://trainingforclimbing.com/?p=665 | 200 via redirect (short link) | use https://trainingforclimbing.com/improve-climbing-footwork-with-target-practice/ |
| research/A-sources.yml:403 | A36 | https://nicros.com/?p=1505 | 200 via redirect (short link) | use https://nicros.com/training/training-articles/center-of-gravity-placement-part-1/ |
| research/A-sources.yml:424 | A38 | https://climbfit.com.au/?p=393 | 200 via redirect (short link) | use https://www.climbfit.com.au/how-to-climb-overhangs/ |
| research/B-sources.yml:159 | B13 | https://nicros.com/?p=1526 | 200 via redirect (short link) | use https://nicros.com/training/training-articles/fundamentals-of-technique-5/ |
| research/B-sources.yml:181 | B15 | https://nicros.com/?p=1509 | 200 via redirect (short link) | use https://nicros.com/training/training-articles/twist-lock-and-backstepping-technique/ |
| research/B-sources.yml:193 | B16 | https://nicros.com/?p=1500 | 200 via redirect (short link) | use https://nicros.com/training/training-articles/center-of-gravity-placement-part-2/ |
| research/B-sources.yml:204 | B17 | https://nicros.com/?p=1505 | 200 via redirect (short link) | use https://nicros.com/training/training-articles/center-of-gravity-placement-part-1/ |
| research/B-sources.yml:226 | B19 | https://trainingforclimbing.com/?p=9695 | 200 via redirect (short link) | use https://trainingforclimbing.com/steep-wall-climbing-techniques/ |
| research/B-sources.yml:40 | B4 | https://nicas.co.uk/?p=9518 | 200 via redirect (short link) | use https://nicas.co.uk/schemes/bouldering/ |
| research/B-sources.yml:405 | B35 | https://philarockgym.com/?p=25888 | 200 via redirect (short link) | use https://philarockgym.com/how-to-prevent-the-annoying-barn-door-in-climbing/ |
| research/B-sources.yml:416 | B36 | https://philarockgym.com/?p=25593 | 200 via redirect (short link) | use https://philarockgym.com/what-is-straight-arming-and-why-every-climber-should-do-it/ |
| research/B-sources.yml:482 | B42 | https://philarockgym.com/?p=30314 | 200 via redirect (short link) | use https://philarockgym.com/twist-locking-series-the-basics-of-the-reverse-flag/ |
| research/B-sources.yml:658 | B58 | https://gripped.com/?p=48051 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/correct-your-footwork-bad-habits-with-climbing-pro-dave-macleod/ |
| research/C-sources.yml:113 | C10 | https://gripped.com/?p=38683 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/grip-positions-and-the-two-forms-of-full-crimping/ |
| research/C-sources.yml:397 | C34 | https://www.99boulders.com/?p=12095 | 200 via redirect (short link) | use https://www.99boulders.com/climbing-moves-holds-and-technique |
| research/D-sources.yml:144 | D13 | https://philarockgym.com/?p=27223 | 200 via redirect (short link) | use https://philarockgym.com/dynamic-climbing-1-0-deadpointing/ |
| research/D-sources.yml:155 | D14 | https://philarockgym.com/?p=27444 | 200 via redirect (short link) | use https://philarockgym.com/whats-the-difference-between-double-dynos-and-deadpointing/ |
| research/D-sources.yml:166 | D15 | https://philarockgym.com/?p=27749 | 200 via redirect (short link) | use https://philarockgym.com/learn-all-about-the-single-dyno/ |
| research/D-sources.yml:177 | D16 | https://philarockgym.com/?p=27827 | 200 via redirect (short link) | use https://philarockgym.com/the-ultimate-guide-to-dyno-tips-and-tricks-5/ |
| research/D-sources.yml:278 | D25 | https://gripped.com/?p=46803 | 200 via redirect (short link) | use https://gripped.com/sections/training/10-tips-for-comp-style-boulder-problems/ |
| research/D-sources.yml:289 | D26 | https://gripped.com/?p=47493 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/three-exercises-to-become-a-more-dynamic-climber/ |
| research/D-sources.yml:300 | D27 | https://gripped.com/?p=48122 | 200 via redirect (short link) | use https://gripped.com/sections/training/cut-feet-for-stronger-shoulders-and-core/ |
| research/D-sources.yml:311 | D28 | https://gripped.com/?p=34050 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/training-tuesday-use-your-hips/ |
| research/D-sources.yml:322 | D30 | https://gripped.com/?p=23960 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/watch-and-learn-how-to-dyno-in-the-gym/ |
| research/E-sources.yml:104 | E10 | https://philarockgym.com/?p=25369 | 200 via redirect (short link) | use https://philarockgym.com/what-every-climber-needs-to-know-about-balance/ |
| research/E-sources.yml:274 | E27 | https://gripped.com/?p=40443 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/top-olympian-tomoa-narasaki-teaches-coordination/ |
| research/E-sources.yml:49 | E5 | https://gripped.com/?p=46803 | 200 via redirect (short link) | use https://gripped.com/sections/training/10-tips-for-comp-style-boulder-problems/ |
| research/E-sources.yml:593 | E57 | https://gripped.com/?p=30104 | 200 via redirect (short link) | use https://gripped.com/profiles/lets-talk-about-grades/ |
| research/E-sources.yml:603 | E58 | https://www.99boulders.com/?p=204 | 200 via redirect (short link) | use https://www.99boulders.com/bouldering-grades |
| research/E-sources.yml:630 | E65 | https://www.99boulders.com/?p=310 | 200 via redirect (short link) | use https://www.99boulders.com/what-is-bouldering |
| research/E-sources.yml:74 | E7 | https://gripped.com/?p=31309 | 200 via redirect (short link) | use https://gripped.com/indoor-climbing/10-techniques-for-climbing-overhangs/ |
| research/E-sources.yml:84 | E8 | https://climbfit.com.au/?p=393 | 200 via redirect (short link) | use https://www.climbfit.com.au/how-to-climb-overhangs/ |
| research/E-sources.yml:94 | E9 | https://nicros.com/?p=1520 | 200 via redirect (short link) | use https://nicros.com/training/training-articles/fundamentals-of-technique-7/ |
| research/F-sources.yml:274 | F28 | https://nicas.co.uk/?p=9518 | 200 via redirect (short link) | use https://nicas.co.uk/schemes/bouldering/ |
| research/F-sources.yml:331 | F36 | https://riverrockclimbing.com/?p=5314 | 200 via redirect (short link) | use https://riverrockclimbing.com/event/advanced-movement-11/ |
| research/G-sources.yml:415 | G34 | https://nicros.com/?p=1927 | 200 via redirect (short link) | use https://nicros.com/training/training-articles/fingerboard-training-part-3-of-4/ |
| book/chapters/06-dynamic.typ:593 | pogo | https://lacrux.com/en/bouldern/pro-tip-pogo-technique-when-bouldering-correctly/ | 200 via redirect (cosmetic) | Optional: use https://www.lacrux.com/en/bouldern/pro-tip-pogo-technique-when-bouldering-correctly/ |
| research/A-sources.yml:290 | A26 | https://sportrock.com/post/intermediate-footwork-in-60-seconds | 200 via redirect (cosmetic) | Optional: use https://www.sportrock.com/post/intermediate-footwork-in-60-seconds |
| research/A-sources.yml:511 | A46 | https://www.nicas.co.uk/brand_central/nicas-bouldering-scheme-overview/ | 200 via redirect (cosmetic) | Optional: use https://nicas.co.uk/brand_central/nicas-bouldering-scheme-overview/ |
| research/B-sources.yml:237 | B20 | https://www.climbing.com/skills/drop-knee-climbing-technique/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/drop-knee-climbing-technique/?scope=anon |
| research/B-sources.yml:248 | B21 | https://www.climbing.com/skills/flagging/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/flagging/?scope=anon |
| research/B-sources.yml:260 | B22 | https://www.climbing.com/skills/five-counterintuitive-climbing-tips-for-rock-climbing/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/five-counterintuitive-climbing-tips-for-rock-climbing/?scope=anon |
| research/B-sources.yml:282 | B24 | https://www.climbing.com/skills/training-pinch-strength/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/training-pinch-strength/?scope=anon |
| research/B-sources.yml:293 | B25 | https://www.climbing.com/skills/bouldering-injury-prevention/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/bouldering-injury-prevention/?scope=anon |
| research/B-sources.yml:304 | B26 | https://www.climbing.com/skills/climbing-techniques-how-to-flag/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/climbing-techniques-how-to-flag/?scope=anon |
| research/B-sources.yml:316 | B27 | https://www.climbing.com/skills/get-instantly-better-at-climbing/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/get-instantly-better-at-climbing/?scope=anon |
| research/B-sources.yml:327 | B28 | https://www.climbing.com/skills/injury-free-movement-for-rock-climbers/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/injury-free-movement-for-rock-climbers/?scope=anon |
| research/B-sources.yml:338 | B29 | https://www.climbing.com/skills/how-to-stem-climbing/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/how-to-stem-climbing/?scope=anon |
| research/B-sources.yml:349 | B30 | https://www.climbing.com/skills/climbing-techniques-how-to-undercling/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/climbing-techniques-how-to-undercling/?scope=anon |
| research/B-sources.yml:360 | B31 | https://www.climbing.com/skills/how-to-climb-slopers-hint-its-all-about-body-position/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/how-to-climb-slopers-hint-its-all-about-body-position/?scope=anon |
| research/B-sources.yml:371 | B32 | https://www.climbing.com/skills/how-to-improve-footwork-climbing/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/how-to-improve-footwork-climbing/?scope=anon |
| research/B-sources.yml:382 | B33 | https://www.climbing.com/skills/the-hidden-dangers-of-a-technique-for-steep-climbing/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/the-hidden-dangers-of-a-technique-for-steep-climbing/?scope=anon |
| research/B-sources.yml:394 | B34 | https://www.climbing.com/skills/technique/carlo-traversi-benefits-shorter-climber/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/technique/carlo-traversi-benefits-shorter-climber/?scope=anon |
| research/C-sources.yml:223 | C21 | https://latticetraining.com/blog/why-do-we-train-half-crimp/ | 200 via redirect (cosmetic) | Optional: use https://latticetraining.com/blog/why-do-we-train-half-crimp |
| research/C-sources.yml:289 | C26 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9483560 | 200 via redirect (cosmetic) | Optional: use https://pmc.ncbi.nlm.nih.gov/articles/PMC9483560/ |
| research/C-sources.yml:303 | C27 | https://cris.fau.de/publications/259581666 | 200 via redirect (cosmetic) | Optional: use https://cris.fau.de/publications/259581666/ |
| research/C-sources.yml:474 | C41 | https://advnture.com/features/rock-climbing-techniques | 200 via redirect (cosmetic) | Optional: use https://www.advnture.com/features/rock-climbing-techniques |
| research/C-sources.yml:561 | C50 | https://shop.anatomic.sk/en/produkt/hoppers-2-dual-2/ | 200 via redirect (cosmetic) | Optional: use https://shop.anatomic.sk/en/produkt/hoppers-2-dual-2/?v=0ecbf9426bcf |
| research/D-sources.yml:266 | D24 | https://lacrux.com/en/bouldern/pro-tip-pogo-technique-when-bouldering-correctly/ | 200 via redirect (cosmetic) | Optional: use https://www.lacrux.com/en/bouldern/pro-tip-pogo-technique-when-bouldering-correctly/ |
| research/D-sources.yml:389 | D38 | https://catalystclimbing.com/shop/p/dynamic-movement-12-intensive-practice-sessions-pdf-download | 200 via redirect (cosmetic) | Optional: use https://www.catalystclimbing.com/shop/p/dynamic-movement-12-intensive-practice-sessions-pdf-download |
| research/D-sources.yml:433 | D42 | https://lacrux.com/en/training/3-ultimate-technique-tips-from-will-bosi-climbing-training/ | 200 via redirect (cosmetic) | Optional: use https://www.lacrux.com/en/training/3-ultimate-technique-tips-from-will-bosi-climbing-training/ |
| research/E-sources.yml:244 | E24 | https://advnture.com/features/rock-climbing-techniques | 200 via redirect (cosmetic) | Optional: use https://www.advnture.com/features/rock-climbing-techniques |
| research/E-sources.yml:482 | E46 | https://www.climbingbusinessjournal.com/ask-a-setter-avoid-these-common-mistakes/ | 200 via redirect (cosmetic) | Optional: use https://climbingbusinessjournal.com/ask-a-setter-avoid-these-common-mistakes/ |
| research/E-sources.yml:583 | E56 | https://boulderingproject.com/blog/understand-climbing-grades-at-any-gym | 200 via redirect (cosmetic) | Optional: use https://boulderingproject.com/blog/understand-climbing-grades-at-any-gym/ |
| research/F-sources.yml:121 | F14 | https://www.climbing.com/gear/review-lattice-testing-and-training-rung/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/gear/review-lattice-testing-and-training-rung/?scope=anon |
| research/F-sources.yml:185 | F18 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9274001 | 200 via redirect (cosmetic) | Optional: use https://pmc.ncbi.nlm.nih.gov/articles/PMC9274001/ |
| research/F-sources.yml:264 | F27 | https://boulderingproject.com/blog/understand-climbing-grades-at-any-gym | 200 via redirect (cosmetic) | Optional: use https://boulderingproject.com/blog/understand-climbing-grades-at-any-gym/ |
| research/F-sources.yml:355 | F38 | https://lacrux.com/en/training/next-level-this-is-how-you-crack-the-7th-degree/ | 200 via redirect (cosmetic) | Optional: use https://www.lacrux.com/en/training/next-level-this-is-how-you-crack-the-7th-degree/ |
| research/F-sources.yml:410 | F43 | https://www.climbing.com/skills/break-through-training-plateau/ | 200 via redirect (cosmetic) | Optional: use https://www.climbing.com/skills/break-through-training-plateau/?scope=anon |
| research/G-sources.yml:216 | G18 | https://cris.fau.de/publications/332668848 | 200 via redirect (cosmetic) | Optional: use https://cris.fau.de/publications/332668848/ |
| research/G-sources.yml:314 | G24 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6395417 | 200 via redirect (cosmetic) | Optional: use https://pmc.ncbi.nlm.nih.gov/articles/PMC6395417/ |
| research/G-sources.yml:50 | G4 | https://pubmed.ncbi.nlm.nih.gov/26453999 | 203 via redirect (cosmetic) | Optional: use https://pubmed.ncbi.nlm.nih.gov/26453999/ |
| research/G-sources.yml:553 | G45 | https://pmc.ncbi.nlm.nih.gov/articles/PMC6006010 | 200 via redirect (cosmetic) | Optional: use https://pmc.ncbi.nlm.nih.gov/articles/PMC6006010/ |

## Compared with research/linkcheck.md

- **Watch links.** The earlier check had 36 links in 27 entries (31 distinct URLs); there
  are now 35 in 26 entries (30 distinct). The Lattice playlist link of `hip-pop` is gone
  and the entry has no `watch:` any more. The replacements made last time (foot-swap,
  heel-hook, toe-hook, knee-bar, open-hand, deadpoint, dyno, pogo, paddle-dyno) are in
  place and all resolve.
- **Still dead:** F37 (castle-climbing.co.uk), 404 as before.
- **Still blocked, same cause:** the five DOIs (G47, G48, G49, G52, G65; all registered in
  the handle API), E36 (iris.cnr.it), D46 (Proboards, 202), C24 (Thieme, "Please wait"
  page), E63 (HAL) and G15 (mediatum), both a bot-check page behind a 200.
- **Changed from a bot-check 200 to a timeout:** E39 (sponet.de), F17 and G25
  (lida.sport-iat.de). The two hostnames (lida.sport-iat.de, www.sponet.de) resolve to
  the same IP, which accepts the TCP connection and then sends nothing.
- **Cleared:** A6 (climbing.com), the DNS error last time, is 200 now.
- **New, and not a sign of dead pages:** 28 link occurrences that the earlier report did
  not list as problems are now refused. 11 ukclimbing.com pages (including E17 and E49) and 3 thecrag.com
  glossary pages answer 403 with a Cloudflare challenge; atomikclimbingholds.com and
  outdoors.codidact.com answer the same; 12 Friction Labs and Rock Run blog pages
  (frictionlabs.com, shop.frictionlabs.com, rockrun.com) answer 429 with `Retry-After: 60`
  and kept doing so across four attempts over several minutes. These need a look in a
  browser before the book is published. None of them is a watch link, so none shows as a
  QR code.
- **Unchanged otherwise:** all other URLs answered 2xx. Apart from the bot-check pages
  listed above, none of the 306 pages fetched in full has a challenge or "not found" title.

## Not checked

Page titles of the bibliography entries were not compared with the `title:` fields this
time, only the video titles and channels. URLs that appear only inside `note:` fields of
the yml files (for example the BMC syllabus, shura.shu.ac.uk, the Depot Climbing page)
were not in scope.
