#!/usr/bin/env python3
"""Generate personalized pitch emails from the tracker.

Usage:
  python3 -I generate_pitches.py                 # all targets with status 'new' and an email -> drafts/
  python3 -I generate_pitches.py --priority A    # only priority A
  python3 -I generate_pitches.py --county Essex --county Union --limit 10
  python3 -I generate_pitches.py --ids ess-montclair-senior-services,uni-...

Writes drafts/<id>.md (subject + body) and drafts/mailmerge.csv (to, subject, body) for Gmail/YAMM style merges.
Never sends anything.
"""
import argparse, csv, pathlib, re, datetime
from openpyxl import load_workbook

HERE = pathlib.Path(__file__).resolve().parent
TPL = (HERE / "templates" / "pitches.md").read_text()
SENDER = "Zain Jaffar"
LANGS = {"spanish": "Spanish", "hindi": "Hindi", "urdu": "Urdu", "gujarati": "Gujarati", "haitian": "Haitian Creole", "creole": "Haitian Creole", "korean": "Korean"}

def section(title):
    m = re.search(r"^## " + re.escape(title) + r"\n(.*?)(?=^## |^---|\Z)", TPL, re.S | re.M)
    body = m.group(1).strip()
    subj = re.search(r"\*\*Subject:\*\*\s*(.+)", body).group(1).strip()
    body = body.split("\n", 1)[1].strip()
    body = re.sub(r"\n`\{language_clause\}`.*$", "", body, flags=re.S).strip()
    return subj, body

T = {"senior": section("1. Senior center / Office on Aging"), "aging": section("1b. County Office on Aging / Area Agency on Aging"), "library": section("2. Public library (adult / senior programming)"),
     "faith": section("3. Faith community (church, mosque, temple, gurdwara)"), "community": section("4. Community center / nonprofit senior program")}
def kind(t):
    if t == "aging_office": return "aging"
    if t == "senior_center": return "senior"
    if t == "library": return "library"
    if t in ("church", "mosque", "temple", "gurdwara", "faith_network", "other_faith"): return "faith"
    return "community"

def next_month():
    d = datetime.date.today().replace(day=1) + datetime.timedelta(days=32)
    return d.strftime("%B")

def fill(r):
    subj, body = T[kind(r["type"])]
    lang = ""
    for k, v in LANGS.items():
        if k in (r.get("languages_served") or "").lower(): lang = v; break
    first = (r.get("contact_name") or "").split(" ")[0]
    greet = f"Dear {first}" if first else "Hello"
    short = re.split(r" \(| - | / ", r["name"])[0].strip()
    vals = {"{name}": short, "{town}": r.get("town") or "your area", "{contact_first}": greet, "{county}": r.get("county") or "your",
            "{language}": lang, "{month}": next_month(), "{sender}": SENDER,
            "{language_clause}": f", available in {lang}," if lang else ""}
    for k, v in vals.items(): subj = subj.replace(k, v); body = body.replace(k, v)
    body = body.replace(" ,", ",").replace("handout,, ", "handout, ")
    return subj, body

ap = argparse.ArgumentParser()
ap.add_argument("--priority", action="append"); ap.add_argument("--county", action="append"); ap.add_argument("--type", action="append")
ap.add_argument("--ids"); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--include-no-email", action="store_true")
a = ap.parse_args()

ws = load_workbook(HERE / "tracker.xlsx", data_only=True)["Pipeline"]
hdr = [c.value for c in ws[1]]
rows = [dict(zip(hdr, r)) for r in ws.iter_rows(min_row=2, values_only=True)]
ids = set(a.ids.split(",")) if a.ids else None
sel = []
for r in rows:
    if not r.get("id"): continue
    if ids and r["id"] not in ids: continue
    if not ids:
        if (r.get("status") or "new") != "new": continue
        if a.priority and r.get("priority") not in a.priority: continue
        if a.county and r.get("county") not in a.county: continue
        if a.type and r.get("type") not in a.type: continue
        if not r.get("email") and not a.include_no_email: continue
    sel.append(r)
    if a.limit and len(sel) >= a.limit: break

out = HERE / "drafts"; out.mkdir(exist_ok=True)
with (out / "mailmerge.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["id", "to", "name", "subject", "body"])
    for r in sel:
        subj, body = fill(r)
        (out / f"{r['id']}.md").write_text(f"To: {r.get('email') or '(no email: use web form / phone)'}\nSubject: {subj}\n\n{body}\n")
        w.writerow([r["id"], r.get("email") or "", r["name"], subj, body])
print(f"wrote {len(sel)} drafts to {out}/ and mailmerge.csv")
