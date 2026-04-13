#!/usr/bin/env bash
set -euo pipefail

MAIN="slides"

pdflatex -interaction=nonstopmode -output-directory=build "$MAIN.tex"
pdflatex -interaction=nonstopmode -output-directory=build "$MAIN.tex"

echo "Built build/$MAIN.pdf"
