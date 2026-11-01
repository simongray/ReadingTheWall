"""Check every hand close-up against the hand model in figtools/hand.py.

Usage: python3 tools/check_hands.py

Draws each hand figure into a temporary folder and prints, for every hand,
the drawn segment lengths and thickness of the front finger in side views,
how much of each finger behind it shows (the share of its outline that no
nearer part covers) and how much of the thumb shows. Exits with status 1 if
a side view draws a segment longer or shorter than the model (by more than
0.02 cm) or a hand shows less than a quarter of its thumb.
"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "figtools"))

import figs_dynamic  # noqa: E402
import figs_hands as F  # noqa: E402
import hand as H  # noqa: E402

FIGURES = [("hands-hold-angle", F.hold_angle_fig), ("open-hand", F.open_hand_fig),
           ("half-crimp", F.half_crimp_fig), ("full-crimp", F.full_crimp_fig),
           ("pinch", F.pinch_fig), ("sloper", F.sloper_fig), ("pocket", F.pocket_fig),
           ("thumb-catch", F.thumb_catch_fig), ("wrap", F.wrap_fig), ("regrip", F.regrip_fig),
           ("hand-atlas", F.hand_atlas_fig), ("filmstrip-sloper", F.filmstrip_sloper),
           ("latching", figs_dynamic.latching)]
TOL = 0.02          # cm
MIN_THUMB = 0.25    # share of the thumb's two segments that must show


def main():
    out = tempfile.mkdtemp()
    failed = []
    for name, fn in FIGURES:
        H.RECORD.clear()
        H.CONTEXT[0] = name
        fn(os.path.join(out, name + ".svg"))
        for i, r in enumerate(H.RECORD, 1):
            line = f"{name:17s} {i:2d} {r['view']:6s}"
            bad = []
            if "lengths" in r:
                model = H.SEG[r["front"]]
                diff = max(abs(a - b) for a, b in zip(r["lengths"], model))
                line += (f" {r['front']} segments " + "/".join(f"{v:.2f}" for v in r["lengths"])
                         + " (model " + "/".join(f"{v:.1f}" for v in model) + ")"
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
            if r["thumb"] < MIN_THUMB:
                bad.append("thumb missing")
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
