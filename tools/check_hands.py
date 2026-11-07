"""Check every hand close-up against the hand model in figtools/hand.py.

Usage: python3 tools/check_hands.py

Draws each hand figure into a temporary folder and prints the hand's
proportions and, for every hand, the drawn segment lengths and thickness of the
front finger in side views, how much of each finger behind it shows (the share
of its outline that no nearer part covers) and how much of the thumb shows.
Exits with status 1 if the proportions leave the published ranges, a side view
draws a segment longer than the model or shorter than its side-view tilt allows
(with 0.02 cm to spare), a hand shows less than a quarter of its thumb, or draws
it as a stump: under 70% of its length, or with two or more of its joints right
out from the hand or bent back as far as they go. Contact with the rock isn't
tested: look at the figures for that.
"""
import math
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "figtools"))

import figs_body  # noqa: E402
import figs_dynamic  # noqa: E402
import figs_hands as F  # noqa: E402
import hand as H  # noqa: E402

FIGURES = [("hands-hold-angle", F.hold_angle_fig), ("open-hand", F.open_hand_fig),
           ("half-crimp", F.half_crimp_fig), ("full-crimp", F.full_crimp_fig),
           ("pinch", F.pinch_fig), ("sloper", F.sloper_fig), ("pocket", F.pocket_fig),
           ("thumb-catch", F.thumb_catch_fig), ("wrap", F.wrap_fig), ("regrip", F.regrip_fig),
           ("hand-atlas", F.hand_atlas_fig), ("filmstrip-sloper", F.filmstrip_sloper),
           ("latching", figs_dynamic.latching), ("matching", figs_body.matching)]
TOL = 0.02          # cm
MIN_THUMB = 0.25    # share of the thumb's two segments that must show
MIN_THUMB_LEN = 0.7  # share of their length that must be drawn
MAX_THUMB_LIMITS = 1 # thumb joints that may sit at a limit that strains them
# Published adult means, as shares of hand length (see hand.py's anatomy notes):
# breadth across the knuckles, palm to the webs, middle finger from its web.
PROPORTIONS = {"breadth": (0.43, 0.47), "palm": (0.55, 0.60), "middle": (0.40, 0.45)}


def proportions():
    """The flat hand's shares of its length, measured as drawn: the width of
    the palm at the knuckles, and the webs from the finger_web polygons."""
    h = H.Hand("flat")
    length = h.finger("m")["tip"][0]
    ys = [v for x, y, _, w, _, _ in H.PALM_RINGS if x > 6 for v in (y + w, y - w)]
    webs = [h.finger_web(a, b)[2][0] for a, b in (("i", "m"), ("m", "r"))]
    palm = sum(webs) / len(webs)
    return {"breadth": (max(ys) - min(ys)) / length, "palm": palm / length,
            "middle": (length - palm) / length}


def main():
    out = tempfile.mkdtemp()
    failed = []
    for k, v in proportions().items():
        lo, hi = PROPORTIONS[k]
        print(f"{k} {v:.3f} of the hand's length (published {lo}-{hi})")
        if not lo <= v <= hi:
            failed.append(k)
    print()
    for name, fn in FIGURES:
        H.RECORD.clear()
        H.CONTEXT[0] = name
        fn(os.path.join(out, name + ".svg"))
        for i, r in enumerate(H.RECORD, 1):
            line = f"{name:17s} {i:2d} {r['view']:6s}"
            bad = []
            if "lengths" in r:
                model = H.SEG[r["front"]]
                short = 1 - math.cos(math.radians(r["tilt"]))
                diff = max(max(a - b, b * (1 - short) - a) for a, b in zip(r["lengths"], model))
                line += (f" {r['front']} segments " + "/".join(f"{v:.2f}" for v in r["lengths"])
                         + " (model " + "/".join(f"{v:.2f}" for v in model) + ")"
                         + " thick " + "/".join(f"{v:.2f}" for v in r["thickness"])
                         + " palm " + "/".join(f"{v:.2f}" for v in r["palm"]))
                if diff > TOL:
                    bad.append(f"segment off by {diff:.2f} cm")
            if r.get("behind"):
                line += " behind " + " ".join(f"{f}{v:.0%}" for f, v in
                                              sorted(r["behind"].items(), key=lambda x: "imrl".index(x[0])))
            line += f" thumb {r['thumb']:.0%}"
            if "hidden" in r:
                line += f" index under thumb {r['hidden']:.0%}"
            line += f" drawn {r['thumb_len']:.0%}"
            if r["thumb_limits"]:
                line += " at limit " + "/".join(r["thumb_limits"])
            if r["thumb"] < MIN_THUMB:
                bad.append("thumb missing")
            if not r["ghost"] and r["thumb_len"] < MIN_THUMB_LEN:
                bad.append("thumb a stump")
            if len(r["thumb_limits"]) > MAX_THUMB_LIMITS:
                bad.append("thumb at its limits")
            if bad:
                line += "  FAIL: " + ", ".join(bad)
                failed.append(f"{name} hand {i}")
            print(line)
    if failed:
        print("\nfailed:", ", ".join(failed))
        sys.exit(1)
    print("\nall hands match the model")


if __name__ == "__main__":
    main()
