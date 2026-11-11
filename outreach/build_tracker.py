#!/usr/bin/env python3
"""Merge the research CSVs into outreach/tracker.xlsx (the working pipeline) and outreach/data/all_targets.csv.

Run: python3 -I build_tracker.py        (safe to re-run: it preserves status/notes columns from an existing tracker by id)
"""
import csv, pathlib, re, datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "data"
OUT = HERE / "tracker.xlsx"

TIER1 = {"Essex", "Union", "Morris", "Middlesex", "Somerset"}
TIER2 = {"Bergen", "Hudson", "Passaic", "Mercer", "Monmouth"}
TYPE_W = {"senior_center": 3, "aging_office": 3, "nonprofit_senior_program": 2, "community_center": 2, "library": 2,
          "church": 2, "mosque": 2, "temple": 2, "gurdwara": 2, "faith_network": 3, "other_faith": 1}
STATUSES = ["new", "emailed", "followed_up", "called", "replied", "booked", "done", "declined", "parked"]

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]

rows = []
for f in sorted(DATA.glob("*.csv")):
    if f.name == "all_targets.csv": continue
    with f.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if not r.get("name"): continue
            r = {k: (v or "").strip() for k, v in r.items()}
            r["id"] = f"{slug(r['county'])[:3]}-{slug(r['name'])}"
            tier = 1 if r["county"] in TIER1 else 2 if r["county"] in TIER2 else 3
            score = (4 - tier) * 3 + TYPE_W.get(r["type"], 1) + (2 if r["email"] else 0) + (1 if r["contact_name"] else 0) + (1 if r["languages_served"] else 0)
            r["priority"] = "A" if (score >= 12 and r["email"]) else "B" if score >= 8 else "C"
            r["source_file"] = f.name
            rows.append(r)

# de-dupe by id
seen = {}
for r in rows:
    if r["id"] not in seen: seen[r["id"]] = r
rows = sorted(seen.values(), key=lambda r: (r["priority"], r["county"], r["type"], r["name"]))

# preserve pipeline fields from an existing tracker
keep = {}
PIPE = ["status", "owner", "first_contact", "last_touch", "next_action", "talk_date", "format", "attendance", "pre_pct", "post_pct", "tracker_notes"]
if OUT.exists():
    ws = load_workbook(OUT)["Pipeline"]
    hdr = [c.value for c in ws[1]]
    for row in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(hdr, row))
        if d.get("id"): keep[d["id"]] = {k: d.get(k) for k in PIPE}

cols = ["id", "priority", "name", "type", "county", "town", "contact_name", "contact_title", "email", "phone", "best_channel", "languages_served", "website"] + PIPE + ["address", "notes", "source_url"]
wb = Workbook(); ws = wb.active; ws.title = "Pipeline"
ws.append(cols)
bold = Font(bold=True); fill = PatternFill("solid", fgColor="F7F1EC")
for c in range(1, len(cols) + 1): ws.cell(1, c).font = bold; ws.cell(1, c).fill = fill
for r in rows:
    k = keep.get(r["id"], {})
    line = []
    for c in cols:
        if c in PIPE: line.append(k.get(c) if k.get(c) is not None else ("new" if c == "status" else None))
        elif c == "notes": line.append(r.get("notes"))
        else: line.append(r.get(c))
    ws.append(line)
n = ws.max_row
dv = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"', allow_blank=True); ws.add_data_validation(dv)
dv.add(f"N2:N{max(n, 2)}")
dv2 = DataValidation(type="list", formula1='"zoom,in_person,watch_together"', allow_blank=True); ws.add_data_validation(dv2); dv2.add(f"T2:T{max(n, 2)}")
widths = {"id": 28, "priority": 8, "name": 42, "type": 18, "county": 11, "town": 16, "contact_name": 20, "contact_title": 22, "email": 32, "phone": 14, "best_channel": 11, "languages_served": 18, "website": 30,
          "status": 12, "owner": 10, "first_contact": 12, "last_touch": 12, "next_action": 12, "talk_date": 12, "format": 14, "attendance": 10, "pre_pct": 8, "post_pct": 8, "tracker_notes": 40, "address": 40, "notes": 50, "source_url": 40}
for i, c in enumerate(cols, 1): ws.column_dimensions[get_column_letter(i)].width = widths.get(c, 14)
ws.freeze_panes = "D2"; ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{n}"

# Dashboard
d = wb.create_sheet("Dashboard")
d.append(["Every Shade outreach dashboard"]); d["A1"].font = Font(bold=True, size=14)
d.append([f"Built {datetime.date.today().isoformat()} from {len(rows)} targets"])
d.append([])
d.append(["By status", "Count"]); d["A4"].font = bold; d["B4"].font = bold
for i, s in enumerate(STATUSES):
    d.append([s, f'=COUNTIF(Pipeline!$N$2:$N${n},"{s}")'])
d.append(["Total", f"=COUNTA(Pipeline!$A$2:$A${n})"])
d.append([])
start = d.max_row + 1
d.append(["By county", "Targets", "Emailed+", "Booked+"]); [setattr(d.cell(start, c), "font", bold) for c in range(1, 5)]
for county in sorted({r["county"] for r in rows}):
    d.append([county, f'=COUNTIF(Pipeline!$E$2:$E${n},"{county}")',
              f'=COUNTIFS(Pipeline!$E$2:$E${n},"{county}",Pipeline!$N$2:$N${n},"<>new")',
              f'=COUNTIFS(Pipeline!$E$2:$E${n},"{county}",Pipeline!$N$2:$N${n},"booked")+COUNTIFS(Pipeline!$E$2:$E${n},"{county}",Pipeline!$N$2:$N${n},"done")'])
d.append([])
s2 = d.max_row + 1
d.append(["By type", "Targets", "With email"]); [setattr(d.cell(s2, c), "font", bold) for c in range(1, 4)]
for t in sorted({r["type"] for r in rows}):
    d.append([t, f'=COUNTIF(Pipeline!$D$2:$D${n},"{t}")', f'=COUNTIFS(Pipeline!$D$2:$D${n},"{t}",Pipeline!$I$2:$I${n},"<>")'])
d.append([])
d.append(["Due for follow-up today", f'=COUNTIFS(Pipeline!$R$2:$R${n},"<="&TODAY(),Pipeline!$N$2:$N${n},"<>booked",Pipeline!$N$2:$N${n},"<>done",Pipeline!$N$2:$N${n},"<>declined",Pipeline!$N$2:$N${n},"<>parked")'])
d.append(["Talks done", f'=COUNTIF(Pipeline!$N$2:$N${n},"done")'])
d.append(["Total attendance", f"=SUM(Pipeline!$U$2:$U${n})"])
d.append(["Average knowledge gain (points)", f'=IFERROR(AVERAGE(Pipeline!$W$2:$W${n})-AVERAGE(Pipeline!$V$2:$V${n}),"")'])
d.column_dimensions["A"].width = 34
for c in "BCD": d.column_dimensions[c].width = 12

# Cadence sheet
c = wb.create_sheet("Cadence")
for line in [["Touch", "Day", "Action", "Set status to"], ["1", "0", "Personalized pitch email (templates/pitches.md) or web form", "emailed"],
             ["2", "5", "Short follow-up in the same thread", "followed_up"], ["3", "12", "Phone call using the script; leave voicemail", "called"],
             ["4", "20", "No reply: park with date; re-approach in 90 days with newest outcome line", "parked"],
             ["", "", "Reply received: respond same day, offer 3 dates, set talk_date", "replied -> booked"],
             ["", "", "Talk given: record attendance, pre_pct, post_pct from scoring.xlsx", "done"]]:
    c.append(line)
for col in range(1, 5): c.cell(1, col).font = bold
c.column_dimensions["C"].width = 70; c.column_dimensions["D"].width = 18

wb.save(OUT)
with (DATA / "all_targets.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["id", "priority"] + [k for k in rows[0].keys() if k not in ("id", "priority")]); w.writeheader(); w.writerows(rows)
pa = sum(r["priority"] == "A" for r in rows); em = sum(bool(r["email"]) for r in rows)
print(f"tracker.xlsx: {len(rows)} targets ({pa} priority A), {em} with email; preserved {len(keep)} existing pipeline rows")
