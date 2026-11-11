#!/usr/bin/env python3
"""Extract every translatable English string from the deck, illustrations, and quiz into en.json.
Run: python3 -I extract_strings.py   (from talk-kit/i18n)"""
import json, re, pathlib
from pptx import Presentation
HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent
KEEP = {"every shade"}  # brand, never translated
prs = Presentation(KIT / "slides" / "Every-Shade-Senior-Talk-2026-11-20.pptx")
slide_text, seen = {}, {}
def add(t):
    t = t.strip()
    if not t or t in KEEP or re.fullmatch(r"[\d\s·.,%()+-]+", t): return
    if t not in seen:
        k = f"t{len(seen)+1:03d}"; seen[t] = k; slide_text[k] = t
def walk(shapes):
    for sh in shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                add("".join(r.text for r in p.runs))
for layout in prs.slide_layouts: walk(layout.shapes)
for s in prs.slides: walk(s.shapes)
notes = {f"n{i+1:02d}": s.notes_slide.notes_text_frame.text for i, s in enumerate(prs.slides) if s.has_notes_slide}
illus = {}
for svg in sorted((KIT / "slides" / "illustrations").glob("*.svg")):
    for j, m in enumerate(re.findall(r">([^<>]+)</text>", svg.read_text())):
        illus[f"{svg.stem}_{j+1}"] = m
quiz = json.loads((KIT / "quiz" / "quiz-content.json").read_text())
quiz_ui = {"tag_pre": "Before the talk", "tag_post": "After the talk", "heading": "Skin check quiz",
           "more": "A few more questions (not scored)",
           "code": "Pick any 4-digit number you will remember (for example the last 4 digits of your phone) and write it here so we can match your two quizzes:",
           "foot": "Every Shade · Rutgers University–New Brunswick · everyshadescreening@gmail.com · Anonymous. Used only to improve our talks."}
out = {"_readme": "Translate every string value. Keep keys, URLs, emails, phone numbers, the brand 'every shade'/'Every Shade', and the letters A-E in the ABCDE lines unchanged.",
       "slide_text": slide_text, "notes": notes, "illustrations": illus, "quiz": quiz, "quiz_ui": quiz_ui}
(HERE / "en.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(slide_text), "slide strings,", len(notes), "notes,", len(illus), "illustration strings,",
      len(quiz["scored"]) + len(quiz["unscored"]), "quiz questions")
print("words:", sum(len(v.split()) for v in slide_text.values()), "slide /", sum(len(v.split()) for v in notes.values()), "notes")
