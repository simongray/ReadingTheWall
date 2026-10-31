"""Render every figure a figure module writes into labelled contact sheets.

Usage: python3 tools/contact_sheet.py figs_dynamic OUT_DIR [--dpi 70] [--per 9]
Writes OUT_DIR/<module>-1.png, -2.png ... (needs rsvg-convert and magick).
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    mod, out = sys.argv[1], sys.argv[2]
    dpi = int(sys.argv[sys.argv.index("--dpi") + 1]) if "--dpi" in sys.argv else 70
    per = int(sys.argv[sys.argv.index("--per") + 1]) if "--per" in sys.argv else 9
    src = open(os.path.join(ROOT, "figtools", mod + ".py")).read()
    names = list(dict.fromkeys(re.findall(r'["/]([a-z0-9][a-z0-9_-]*)\.svg"', src)))
    os.makedirs(out, exist_ok=True)
    pngs = []
    for n in names:
        svg = os.path.join(ROOT, "book", "figures", n + ".svg")
        if not os.path.exists(svg):
            continue
        png = os.path.join(out, n + ".png")
        subprocess.run(["rsvg-convert", "-d", str(dpi), "-p", str(dpi), "-b", "white",
                        svg, "-o", png], check=True)
        pngs.append((n, png))
    for i in range(0, len(pngs), per):
        chunk = pngs[i:i + per]
        args = ["magick", "montage"]
        for n, p in chunk:
            args += ["-label", n, p]
        sheet = os.path.join(out, f"{mod}-{i // per + 1}.png")
        args += ["-tile", "3x", "-geometry", "+8+8", "-pointsize", "16",
                 "-font", "/System/Library/Fonts/Helvetica.ttc",
                 "-background", "white", sheet]
        subprocess.run(args, check=True)
        print(sheet)


if __name__ == "__main__":
    main()
