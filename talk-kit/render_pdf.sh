#!/bin/zsh
# Render an HTML file to a letter-size PDF with headless Chrome (fonts load from Google Fonts).
# Usage: ./render_pdf.sh input.html output.pdf
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
IN="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
OUT="$2"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$OUT" \
  --virtual-time-budget=8000 --run-all-compositor-stages-before-draw "file://$IN" >/dev/null 2>&1
echo "wrote $OUT"
