"""Regenerate every figure in book/figures.

Each figure module defines build(out_dir). Modules named figs_*.py are
found automatically. Run from anywhere:
    python3 figtools/build_all.py
"""
import glob
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "book", "figures")
MODULES = ["legend"]

found = [os.path.basename(p)[:-3] for p in glob.glob(os.path.join(HERE, "figs_*.py"))]
sys.path.insert(0, HERE)
os.makedirs(OUT, exist_ok=True)
failed = []
for name in sorted(set(MODULES + found)):
    try:
        mod = importlib.import_module(name)
        mod.build(OUT)
        print("built", name)
    except Exception as e:  # keep going so one broken module doesn't block the rest
        failed.append(name)
        print(f"FAILED {name}: {type(e).__name__}: {e}")
if failed:
    sys.exit(1)
