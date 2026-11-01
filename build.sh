#!/bin/sh
# Rebuild the figures, the source map and the PDF. The PDF is stamped as a
# draft with the current commit; use release.sh to publish an edition.
set -e
cd "$(dirname "$0")"
python3 figtools/build_all.py
python3 tools/merge_sources.py
python3 tools/errata.py
commit="uncommitted"
if git rev-parse --git-dir >/dev/null 2>&1 && git rev-parse HEAD >/dev/null 2>&1; then
  commit="$(git rev-parse --short HEAD)"
  [ -n "$(git status --porcelain)" ] && commit="$commit-dirty"
fi
set -- --input edition=draft --input date="$(date +%Y-%m-%d)" --input commit="$commit"
typst compile --root . "$@" book/main.typ "Bouldering Technique Handbook.pdf"
echo "wrote Bouldering Technique Handbook.pdf (draft, $commit)"
python3 tools/check_fit.py "$@"
