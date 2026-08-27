#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for d in "$ROOT"/papers/*; do
  [ -f "$d/main.tex" ] || continue
  cp "$ROOT/master/abhijit-research.sty" "$d/abhijit-research.sty"
  (cd "$d" && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex >/dev/null)
done
