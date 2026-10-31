# Muscle-shading audit

Every figure with a climber was checked against its text, labels and
captions to decide which muscles are stippled (`active=` on the `Climber`).
The rules:
- Shade where the effort is in the move, as the text describes it, usually
  zero to three regions.
- A bent arm that pulls or presses is shaded; a straight arm, a reaching or
  resting hand, a fall, sitting or standing is not.
- Legs are shaded only where they stand up, drive or press apart; the
  hamstring for a heel hook, the shin for a toe hook, the core for body
  tension.

"Default" means a bent arm holding on (upper arm and forearm).

## Body positioning (figs_body.py)

| Figure | Panel | Shaded | Why |
|---|---|---|---|
| frog | a; b, c | arms (default) | bent arms holding |
| hip-turn | a / b | right arm / nothing | square on the arm works / arms straight |
| backstep | a / b | nothing / right arm | straight arms / right arm holds the spin-out |
| drop-knee | a / b | left arm / left thigh | square on, arms tire / the push leg works, the arms unload |
| flag | a / b | nothing / nothing | the flagged leg balances, not the arm |
| back-flag | – | left arm | bent arm on the sidepull |
| inside-flag | a / b | arms, left thigh / nothing | the left leg stands you up / limbs straight |
| twist-lock | a / b | left arm / right arm | start hold / locked arm (the lat hides behind it) |
| lock-off | – | right arm, right thigh | locked arm; the legs push into the lock |
| layback | – | both thighs | feet push in, arms straight |
| stemming | – | left arm, both thighs | palm presses, feet push apart |
| cross-through | – | left arm, left lat | lock-off seen from behind |
| compression | – | both arms, both lats | palms press, "as in a hug" |
| body-tension | a / b | nothing / hamstring, core | slack / toes pull in, hips held up |
| pre-loading | a / b | both arms / right thigh | pulled in on bent arms / loaded legs |
| opposition | – | both arms, both lats | "pull inward" |
| bumping | – | left arm | bent holding arm |
| filmstrip drop knee | 1–5 | arms; left thigh in 3–4 | the push leg raises the hips |

## Footwork (figs_feet.py)

| Figure | Panel | Shaded | Why |
|---|---|---|---|
| high-step | a / b | left arm / left arm, right thigh | the high leg turns strength into height |
| smearing | a, b | nothing | the feet carry the weight |
| rockover | 1 / 2 | pressing arm, right thigh / right thigh | "the leg does the work" |
| hand-foot-match | a, b | both arms | the left hand presses |
| heel-hook | a / b | left arm / left arm, right hamstring | "pull heel to bum" |
| toe-pull | a / b | nothing / right arm, core | passive foot / body tight from toe to hands |
| toe-hook | a | right arm, left shin, right thigh | toe hook pulls; right foot pushes |
| knee-bar | – | right calf | "like a calf raise" |
| precise-footwork | a, b | arms | bent arms holding |
| filmstrip heel hook | 1–5 | nothing; arms, hamstring; arms, hamstring; arms; right thigh | set, pull, pull, roll over, stand up |

## Hands and concepts (figs_hands.py, figs_concepts.py, figs_considerations.py)

| Figure | Panel | Shaded | Why |
|---|---|---|---|
| concept-straight-arms | a / b | right arm / right thigh | biceps working / legs push |
| concept-hips-in, concept-balance | all | nothing | about where the weight goes |
| concept-barn-door | a / b | nothing / left arm | a hand let go / the bent arm holds |
| filmstrip-hips-first | 1–4 / 5 | nothing / right thigh | hands steady / stand up |
| sit-start, falls | all | nothing (landing: right thigh) | sitting, falling; the bent legs absorb the landing |
| jug | a / b | both arms / nothing | forearms pump / straight arm, shake out |
| sidepull | a / b | left arm / left thigh | bent arm / "foot pushes left" |
| gaston | a / b | left arm / gaston arm, left thigh | the arm pushes out, the foot presses |
| undercling | a / b | arms / right thigh | bent arms / stand up into the hold |
| sloper | a / b | arm / nothing | hips out / arm straight |
| palming | – | right arm | the palm presses |
| mantle | 1 / 2 / 3 | arms / pressing arm / right thigh | pull, press, step up |
| volume-mantle | a / b | arms / left arm, right thigh | pull / press and rock over |
| icons | – | nothing | |

## Dynamic movement (figs_dynamic.py)

| Figure | Panel | Shaded | Why |
|---|---|---|---|
| deadpoint, hip-pump, hip-pop | a / b | nothing / right thigh (hip-pop: and glute) | the legs drive, the arm only lets the body pass |
| dyno, filmstrip dyno | sink / drive / catch | nothing / thighs, calves / arms | legs drive, arms catch |
| double-dyno | a / b | nothing / both arms | catch slightly bent |
| cutting-loose | a / b, c | arm / arm, core | the swing out / snap the legs back, toes on |
| lunge | a / b | nothing / left thigh | the left leg drives |
| counter-kick | a / b | right arm / right arm, core | tense at the peak of the swing |
| latching | c | right arm, right lat | "shoulder down" |
| jump-start, run-and-jump, tic-tac, lache, paddle-dyno | catch | the catching arm | a catch is loaded |
| pogo | a / b | nothing / left arm, left thigh | arms straight / the foot pushes |
| campus-move | a, b | arms, core | arms and body tension hold you |
| double-clutch | a / b | left arm | the catching hand, then the straight arm |
| foot-catch | – | right arm, left shin, core | toe hook pulls back, body tense |

## Terrain (figs_terrain.py)

| Figure | Panel | Shaded | Why |
|---|---|---|---|
| filmstrip top-out | 1–5 | nothing; arms; arms; arms; right thigh | hang, pull, flip, press, rock over |
| filmstrip worked problem | 1–5 | nothing; arms; left arm; right arm, right thigh; arms | start, catch, rest, high step, slap |
| reading-hold-orientation | a, b / c, d | nothing / arms | lean on straight arms / pull up, push away |
| wall angles | slab, vertical / overhang / roof | nothing / core / right shin, core | toes pull in, toe hook |
| slab, volume (b), dynamic-slab | – | nothing | the hands only steer |
| overhang | a / b | nothing / core | feet cut / toes pull in |
| roof | a / b | nothing / right shin, core | toes hook and pull |
| arete | a / b | both thighs / arms, right hamstring | feet push / heel hook |
| corner | a | both thighs | the legs carry the weight, the arms rest |
| volume | a | arms | pushed off, the arms hold on |
| top-out | a / b | arms, hamstring / arms, right thigh | arms and heel pull together / press and rock over |
| traverse | – | nothing | straight arms |
| sit-start (terrain) | a / b | arms / left arm, right thigh | the first pull / the working foot |

## Judgement calls

- Arms right at the 130° threshold (hold orientation b, sit start b, arête
  a) are treated as straight.
- The deadpoint, hip-pump and hip-pop panels (b) leave the bent holding arm
  unshaded, because the text says it only lets the body pass at the top.
- The landing frame of the fall roll shades the thigh, which absorbs the
  landing.

Poses that disagree with their text are listed in FOLLOW-UPS.md.
