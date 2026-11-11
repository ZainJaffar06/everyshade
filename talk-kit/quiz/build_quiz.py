#!/usr/bin/env python3
"""Build the Every Shade pre/post quiz from quiz-content.json.

Outputs (in this folder):
  quiz-pre.html / quiz-post.html   printable large-print quizzes (render to PDF with ../render_pdf.sh)
  answer-key.md                    answers + which fact on the slides covers each question
  zoom-polls.md                    copy-paste sheet for setting up the Zoom polls
  scoring.xlsx                     paste responses, get pre/post % and knowledge gain
Run:  python3 -I build_quiz.py
"""
import json, html, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HERE = pathlib.Path(__file__).resolve().parent
Q = json.loads((HERE / "quiz-content.json").read_text())
LETTERS = "ABCDE"

CSS = """
@page{size:letter;margin:0.6in 0.65in}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#2B1A12;font-family:'Atkinson Hyperlegible',Arial,sans-serif;font-size:15.5pt;line-height:1.3}
h1{font-family:'Manrope',Arial,sans-serif;font-size:26pt;font-weight:800;margin:0 0 4pt;line-height:1.1}
.strip{display:grid;grid-template-columns:repeat(6,1fr);height:8pt;margin-bottom:10pt}
.strip i:nth-child(1){background:#EFCBB0}.strip i:nth-child(2){background:#DDAA84}.strip i:nth-child(3){background:#C28559}
.strip i:nth-child(4){background:#9C623A}.strip i:nth-child(5){background:#6B4127}.strip i:nth-child(6){background:#3D2416}
.tag{display:inline-block;font-family:'Manrope';font-weight:800;font-size:13pt;letter-spacing:.08em;text-transform:uppercase;background:#2B1A12;color:#fff;padding:3pt 10pt;border-radius:999pt;margin-bottom:8pt}
.inst{font-size:14.5pt;color:#6B5446;margin:0 0 10pt}
ol{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:7pt}
li.q{break-inside:avoid}
li.q .t{font-weight:700;display:block;margin-bottom:3pt}
.opts{display:flex;flex-wrap:wrap;gap:4pt 18pt;padding-left:4pt}
.opts span{display:inline-flex;gap:6pt;align-items:center;font-size:14.5pt}
.opts span::before{content:'';width:15pt;height:15pt;border:2pt solid #2B1A12;border-radius:50%;flex:none}
.sec{font-family:'Manrope';font-weight:800;font-size:15pt;margin:10pt 0 4pt;color:#8E5632}
.code{margin-top:10pt;font-size:13pt;color:#6B5446;border-top:1pt solid #E6D9CF;padding-top:6pt}
.foot{margin-top:8pt;font-size:10.5pt;color:#6B5446}
"""

HEAD = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>%s</title>"
        "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Manrope:wght@600;800&family=Atkinson+Hyperlegible:wght@400;700&display=swap'>"
        "<style>%s</style></head><body>")

def render_q(n, q):
    opts = "".join(f"<span>{LETTERS[i]}. {html.escape(o)}</span>" for i, o in enumerate(q["options"]))
    return f"<li class='q'><span class='t'>{n}. {html.escape(q['q'])}</span><div class='opts'>{opts}</div></li>"

def build(phase):
    title = f"{Q['title']} ({'before' if phase=='pre' else 'after'} the talk)"
    out = [HEAD % (title, CSS)]
    out.append("<div class='strip'><i></i><i></i><i></i><i></i><i></i><i></i></div>")
    out.append(f"<span class='tag'>{'Before the talk' if phase=='pre' else 'After the talk'}</span>")
    out.append("<h1>Skin check quiz</h1>")
    out.append(f"<p class='inst'>{html.escape(Q['instructions'])}</p>")
    out.append("<ol>")
    n = 0
    for q in Q["scored"]:
        n += 1
        out.append(render_q(n, q))
    out.append("</ol><p class='sec'>A few more questions (not scored)</p><ol>")
    for q in Q["unscored"]:
        if q.get("pre_only") and phase != "pre": continue
        if q.get("post_only") and phase != "post": continue
        n += 1
        out.append(render_q(n, q))
    out.append("</ol>")
    out.append("<p class='code'>Pick any 4-digit number you will remember (for example the last 4 digits of your phone) and write it here so we can match your two quizzes: ____ ____ ____ ____</p>")
    out.append("<p class='foot'>Every Shade · Rutgers University–New Brunswick · everyshadescreening@gmail.com · Anonymous. Used only to improve our talks.</p>")
    out.append("</body></html>")
    (HERE / f"quiz-{phase}.html").write_text("\n".join(out))

build("pre"); build("post")

# Answer key
key = ["# Answer key\n", "| # | Question | Answer | Covered on slide |", "|---|---|---|---|"]
slide_map = {1: "Why we started / Everyone", 2: "The spots people miss", 3: "Nails", 4: "What it looks like on darker skin",
             5: "How to check at home", 6: "Warning signs (ABCDE + ugly duckling)", 7: "What raises your risk",
             8: "Warning signs", 9: "When to see a doctor", 10: "Where to go"}
for q in Q["scored"]:
    key.append(f"| {q['id']} | {q['q']} | {LETTERS[q['answer']]}. {q['options'][q['answer']]} | {slide_map[q['id']]} |")
key.append("\nScoring: 1 point per correct answer, 10 points total. Unscored questions (confidence, behavior, recommend) are reported as % choosing each option.")
(HERE / "answer-key.md").write_text("\n".join(key) + "\n")

# Zoom poll sheet
zp = ["# Zoom polls: copy-paste sheet\n",
      "Set up TWO polls in the Zoom web portal before the meeting (Meetings > your meeting > Polls/Quizzes). "
      "Name them `Before the talk` and `After the talk`. Mark each as **Anonymous**. Zoom lets you download the results as CSV after the meeting "
      "(Reports > Meeting > Poll Report); paste those rows into scoring.xlsx.\n",
      "Launch `Before the talk` right after your introduction (slide 2) and give 3 minutes. Launch `After the talk` right before the closing slide.\n"]
for phase in ("pre", "post"):
    zp.append(f"\n## Poll: {'Before' if phase=='pre' else 'After'} the talk\n")
    n = 0
    for q in Q["scored"]:
        n += 1
        zp.append(f"**Q{n}. {q['q']}**  (single choice)")
        for i, o in enumerate(q["options"]): zp.append(f"- {o}")
        zp.append("")
    for q in Q["unscored"]:
        if q.get("pre_only") and phase != "pre": continue
        if q.get("post_only") and phase != "post": continue
        n += 1
        zp.append(f"**Q{n}. {q['q']}**  (single choice)")
        for i, o in enumerate(q["options"]): zp.append(f"- {o}")
        zp.append("")
(HERE / "zoom-polls.md").write_text("\n".join(zp) + "\n")

# Scoring workbook
wb = Workbook()
ws = wb.active; ws.title = "Responses"
bold = Font(bold=True); fill = PatternFill("solid", fgColor="F7F1EC")
hdr = ["Talk date", "Venue", "Phase (pre/post)", "Attendee code"] + [f"Q{i}" for i in range(1, 11)] + ["Score (0-10)", "Percent"]
ws.append(hdr)
for c in range(1, len(hdr) + 1):
    ws.cell(1, c).font = bold; ws.cell(1, c).fill = fill
ws.append(["2026-11-20", "Zoom (open)", "pre", "1234"] + ["B", "B", "B", "B", "B", "B", "D", "B", "A", "B"])
ws.append(["2026-11-20", "Zoom (open)", "post", "1234"] + ["B", "B", "B", "B", "B", "B", "D", "B", "A", "B"])
ws["A5"] = "Enter the letter (A/B/C/D) each attendee chose. Rows 2-3 are an example: delete them before use. Score and Percent fill in automatically."
ws["A5"].font = Font(italic=True, color="6B5446")
N = 500
for r in range(2, N + 2):
    terms = "+".join(f'(UPPER({get_column_letter(4 + i)}{r})=Key!$C${i + 1})' for i in range(1, 11))
    ws.cell(r, 15).value = f'=IF(COUNTA(E{r}:N{r})=0,"",{terms})'
    ws.cell(r, 16).value = f'=IF(O{r}="","",O{r}/10)'
    ws.cell(r, 16).number_format = "0%"
for c, w in zip(range(1, 17), [12, 16, 14, 13] + [5] * 10 + [12, 9]):
    ws.column_dimensions[get_column_letter(c)].width = w

wk = wb.create_sheet("Key")
wk.append(["#", "Question", "Correct letter"])
for q in Q["scored"]:
    wk.append([q["id"], q["q"], LETTERS[q["answer"]]])
for c in range(1, 4): wk.cell(1, c).font = bold
wk.column_dimensions["B"].width = 70

wsum = wb.create_sheet("Summary")
wsum.append(["Every Shade: knowledge gain summary"]); wsum["A1"].font = Font(bold=True, size=14)
wsum.append(["Filter by talk date (blank = all)", ""])
wsum.append([])
wsum.append(["Measure", "Before", "After", "Change"])
for c in range(1, 5): wsum.cell(4, c).font = bold; wsum.cell(4, c).fill = fill
rng = "Responses!$C$2:$C$501"; prng = "Responses!$P$2:$P$501"; drng = "Responses!$A$2:$A$501"
cond = lambda ph: f'IF($B$2="",1,({drng}=$B$2))*({rng}="{ph}")'
wsum.append(["Number of quizzes", f'=SUMPRODUCT({cond("pre")}*({prng}<>""))', f'=SUMPRODUCT({cond("post")}*({prng}<>""))', ""])
wsum.append(["Average score (% correct)",
             f'=IFERROR(SUMPRODUCT({cond("pre")}*({prng}<>"")*N(+{prng}))/B5,"")',
             f'=IFERROR(SUMPRODUCT({cond("post")}*({prng}<>"")*N(+{prng}))/C5,"")',
             '=IF(OR(B6="",C6=""),"",C6-B6)'])
for c in ("B6", "C6", "D6"): wsum[c].number_format = "0%"
wsum.append(["Relative improvement", "", "", '=IF(OR(B6="",B6=0),"",(C6-B6)/B6)']); wsum["D7"].number_format = "0%"
wsum.append([])
wsum.append(["Per question (% correct)", "Before", "After", "Change"])
for c in range(1, 5): wsum.cell(9, c).font = bold; wsum.cell(9, c).fill = fill
for i in range(1, 11):
    col = get_column_letter(4 + i)
    qr = f"Responses!${col}$2:${col}$501"
    r = 9 + i
    wsum.append([f"Q{i}",
                 f'=IFERROR(SUMPRODUCT({cond("pre")}*(UPPER({qr})=Key!$C${i+1}))/SUMPRODUCT({cond("pre")}*({qr}<>"")),"")',
                 f'=IFERROR(SUMPRODUCT({cond("post")}*(UPPER({qr})=Key!$C${i+1}))/SUMPRODUCT({cond("post")}*({qr}<>"")),"")',
                 f'=IF(OR(B{r}="",C{r}=""),"",C{r}-B{r})'])
    for c in ("B", "C", "D"): wsum[f"{c}{r}"].number_format = "0%"
wsum.append([])
wsum.append(["How to report it: \"Attendees' average quiz score rose from [Before] to [After] (n=[Number]) after the talk.\" Use the per-question table to see which fact landed and which needs a better slide."])
wsum.column_dimensions["A"].width = 34
for c in "BCD": wsum.column_dimensions[c].width = 12
wb.save(HERE / "scoring.xlsx")
print("built quiz-pre.html, quiz-post.html, answer-key.md, zoom-polls.md, scoring.xlsx")
