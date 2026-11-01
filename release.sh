#!/bin/sh
# Publish an edition: ./release.sh 2 "Second edition"
#
# Requires a clean working tree and a "## … (edition-N)" section in
# CHANGELOG.md. Tags the current commit as edition-N (annotated, with the
# message), builds the PDF stamped with the edition, today's date and the
# commit SHA into editions/, pushes the branch and the tag, and publishes a
# GitHub release with the PDF and the changelog section as its notes.
set -e
cd "$(dirname "$0")"
n="$1"
msg="${2:-Edition $1}"
if [ -z "$n" ]; then echo "usage: ./release.sh EDITION [MESSAGE]"; exit 1; fi
if [ -n "$(git status --porcelain)" ]; then
  echo "working tree not clean: commit your changes (and update CHANGELOG.md) first"; exit 1
fi
if git rev-parse "edition-$n" >/dev/null 2>&1; then
  echo "tag edition-$n already exists"; exit 1
fi
notes="$(awk -v tag="(edition-$n)" '/^## / { on = index($0, tag) > 0; next } on' CHANGELOG.md)"
if [ -z "$(printf '%s' "$notes" | tr -d '[:space:]')" ]; then
  echo "CHANGELOG.md has no \"## … (edition-$n)\" section: rename Unreleased first"; exit 1
fi
python3 figtools/build_all.py
python3 tools/merge_sources.py
python3 tools/errata.py "$n"
if [ -n "$(git status --porcelain)" ]; then
  echo "the build changed tracked files; commit them first"; exit 1
fi
commit="$(git rev-parse --short HEAD)"
today="$(date +%Y-%m-%d)"
mkdir -p editions
out="editions/Reading-the-Wall-edition-$n.pdf"
typst compile --root . \
  --input edition="$n" --input date="$today" --input commit="$commit" \
  book/main.typ "$out"
git tag -a "edition-$n" -m "$msg"
cp "$out" "Bouldering Technique Handbook.pdf"
echo "tagged edition-$n at $commit and wrote $out"
git push origin HEAD "edition-$n"
gh release create "edition-$n" "$out" --verify-tag --title "$msg" --notes "$notes"
