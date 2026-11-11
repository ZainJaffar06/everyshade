#!/bin/zsh
# Render a deck to PDF via Keynote and make contact sheets: qa_render.sh <deck.pptx> <outprefix>
set -e
IN="$1"; OUT="$2"
osascript <<OSA
with timeout of 120 seconds
tell application "Keynote"
  set d to open POSIX file "$IN"
  delay 3
  export d to POSIX file "$OUT.pdf" as PDF
  close d saving no
end tell
end timeout
OSA
python3 -I - "$OUT" <<'PY'
import sys, pypdfium2 as p
from PIL import Image
o=sys.argv[1]; d=p.PdfDocument(o+".pdf"); n=len(d)
imgs=[d[i].render(scale=0.42).to_pil() for i in range(n)]
w,h=imgs[0].size
for k in range(0,n,6):
    s=Image.new("RGB",(w*2+8,h*3+16),"white")
    for j,im in enumerate(imgs[k:k+6]): s.paste(im,((j%2)*(w+8),(j//2)*(h+8)))
    s.save(f"{o}-{k//6+1}.png")
print(n,"slides")
PY
