#!/usr/bin/env python3
"""Turn one talk's quiz answers into results: the result line, a per-question table,
a chart, and one aggregate row in site/talks.csv (which feeds the public Impact page).

Inputs (pick one):
  --zoom BEFORE.csv [AFTER.csv]   Zoom "Poll Report" CSV(s). One file holding both polls is fine.
  --xlsx talk-kit/quiz/scoring.xlsx  Paper quizzes typed into the Responses tab (letters A-D).

Talk details (go into talks.csv; aggregate only, no names):
  --date 2026-11-20 --venue "Zoom (open)" --venue-type "open Zoom" --county Statewide
  --language English --attendees 34

Run:  python3 -I talk-kit/results/analyze_talk.py --zoom ~/Downloads/poll_report.csv \
          --date 2026-11-20 --venue "Zoom (open)" --venue-type "open Zoom" \
          --county Statewide --language English --attendees 34

Quizzes are anonymous, so before and after answers cannot be paired. The script compares
the two groups as independent samples (Fisher exact test per question with Holm correction,
Mann-Whitney U and a bootstrap 95% CI for the score difference). That is the honest
analysis for unpaired anonymous data and is the one described in the IRB protocol draft.
Raw poll files never go in git: keep them in talk-kit/results/raw/ (gitignored).
"""
import argparse, csv, json, pathlib, re, random, statistics, sys, datetime
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
QUIZ = json.loads((ROOT / "talk-kit/quiz/quiz-content.json").read_text(encoding="utf-8"))
SCORED = QUIZ["scored"]
UNSCORED = {q["id"]: q for q in QUIZ["unscored"]}
TALKS = ROOT / "site/talks.csv"
TALK_COLS = ["date", "venue_type", "county", "language", "attendees", "n_before", "n_after",
             "before_pct", "after_pct", "plan_check_pct", "recommend_pct", "confident_after_pct", "venue"]


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


QTEXT = [(f"Q{q['id']}", norm(q["q"]), q) for q in SCORED] + [(k, norm(v["q"]), v) for k, v in UNSCORED.items()]


def match_question(cell):
    n = norm(cell)
    if len(n) < 12:
        return None
    for key, qn, q in QTEXT:
        if n == qn or n.startswith(qn[:40]) or qn.startswith(n[:40]):
            return key, q
    return None


def match_option(q, cell):
    n = norm(cell)
    for i, o in enumerate(q["options"]):
        if n == norm(o):
            return i
    for i, o in enumerate(q["options"]):
        if n and (norm(o).startswith(n) or n.startswith(norm(o))):
            return i
    return None


def parse_zoom(paths):
    """Return list of (phase, {key: option_index}). Works for Zoom's layouts where each
    response row has question cells each followed by the answer cell."""
    out = []
    for p in paths:
        text = pathlib.Path(p).read_text(encoding="utf-8-sig", errors="replace")
        for row in csv.reader(text.splitlines()):
            ans, phase = {}, None
            for i, cell in enumerate(row):
                c = norm(cell)
                if c.startswith("before the talk"):
                    phase = "pre"
                elif c.startswith("after the talk"):
                    phase = "post"
                m = match_question(cell)
                if m and i + 1 < len(row):
                    key, q = m
                    k = match_option(q, row[i + 1])
                    if k is not None:
                        ans[key] = k
            if len([k for k in ans if k.startswith("Q")]) < 5:
                continue  # header, summary, or near-empty row
            if phase is None:
                phase = "pre" if "C2" in ans else "post" if ("C3" in ans or "C4" in ans) else None
            if phase is None:
                sys.exit(f"Could not tell whether a row in {p} is Before or After. Name the polls "
                         "'Before the talk' and 'After the talk', or pass the two polls as separate files.")
            out.append((phase, ans))
    return out


def parse_xlsx(path, date):
    from openpyxl import load_workbook
    ws = load_workbook(path, data_only=True)["Responses"]
    hdr = [c.value for c in ws[1]]
    out = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(hdr, row))
        if not d.get("Phase (pre/post)") or str(d.get("Talk date")) [:10] != date:
            continue
        ans = {}
        for q in SCORED:
            v = (d.get(f"Q{q['id']}") or "").strip().upper()
            if v and v in "ABCD":
                ans[f"Q{q['id']}"] = "ABCD".index(v)
        if ans:
            out.append((str(d["Phase (pre/post)"]).strip().lower(), ans))
    return out


def score(ans):
    got = [ans[f"Q{q['id']}"] == q["answer"] for q in SCORED if f"Q{q['id']}" in ans]
    return 100 * sum(got) / len(got) if got else None


def fisher(a, n1, b, n2):
    from scipy.stats import fisher_exact
    return fisher_exact([[a, n1 - a], [b, n2 - b]])[1]


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0] * len(ps), 0
    for rank, i in enumerate(order):
        run = max(run, min(1, (len(ps) - rank) * ps[i]))
        adj[i] = run
    return adj


def boot_ci(x, y, reps=5000, seed=7):
    rnd = random.Random(seed)
    diffs = sorted(statistics.mean(rnd.choices(y, k=len(y))) - statistics.mean(rnd.choices(x, k=len(x))) for _ in range(reps))
    return diffs[int(0.025 * reps)], diffs[int(0.975 * reps)]


def pct(n, d):
    return round(100 * n / d) if d else None


def chart(rows, path, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    BEFORE, AFTER, INK, MUTED, GRID = "#3E7CB1", "#A0612F", "#2B1A12", "#6B5B50", "#E8E1DA"
    fig, ax = plt.subplots(figsize=(8, 0.4 * len(rows) + 1.3), dpi=200)
    ys = list(range(len(rows)))[::-1]
    for y, r in zip(ys, rows):
        if r["before"] is not None and r["after"] is not None:
            ax.plot([r["before"], r["after"]], [y, y], color=GRID, lw=2, zorder=1, solid_capstyle="round")
        if r["before"] is not None:
            ax.scatter(r["before"], y, s=70, color=BEFORE, zorder=3, edgecolor="white", linewidth=2)
        if r["after"] is not None:
            ax.scatter(r["after"], y, s=70, color=AFTER, zorder=3, edgecolor="white", linewidth=2)
            ax.text(103, y, f"{r['after']}%", va="center", fontsize=8, color=INK)
    ax.set_yticks(ys, [r["label"] for r in rows], fontsize=8, color=INK)
    ax.set_xlim(0, 110); ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"], fontsize=8, color=MUTED)
    ax.grid(axis="x", color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(title, loc="left", fontsize=11, color=INK, fontweight="bold", pad=26)
    ax.scatter([], [], s=50, color=BEFORE, label="Before the talk"); ax.scatter([], [], s=50, color=AFTER, label="After the talk")
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, fontsize=8, borderaxespad=0.3, handletextpad=0.3, columnspacing=1.2)
    fig.tight_layout(); fig.savefig(path, facecolor="white"); plt.close(fig)


SHORT = {1: "Anyone can get skin cancer", 2: "Melanoma on palms, soles, nails", 3: "Widening nail band: see a doctor",
         4: "How melanoma looks on darker skin", 5: "Self-check once a month", 6: "Changing spot is a warning sign",
         7: "Risk factors", 8: "Painless spots can be cancer", 9: "Non-healing sore: see a doctor",
         10: "Free care at health centers"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zoom", nargs="+"); ap.add_argument("--xlsx")
    ap.add_argument("--date", required=True); ap.add_argument("--venue", required=True)
    ap.add_argument("--venue-type", default=""); ap.add_argument("--county", default="")
    ap.add_argument("--language", default="English"); ap.add_argument("--attendees", type=int)
    ap.add_argument("--out", help="output folder (default talk-kit/results/<date>-<venue>)")
    ap.add_argument("--no-talks-csv", action="store_true", help="do not write site/talks.csv (for tests)")
    a = ap.parse_args()
    if not (a.zoom or a.xlsx):
        sys.exit("Give --zoom or --xlsx")
    data = parse_zoom(a.zoom) if a.zoom else parse_xlsx(a.xlsx, a.date)
    pre = [d for p, d in data if p == "pre"]; post = [d for p, d in data if p == "post"]
    if not pre or not post:
        sys.exit(f"Need both Before and After answers; found {len(pre)} before and {len(post)} after.")
    s_pre = [s for s in map(score, pre) if s is not None]; s_post = [s for s in map(score, post) if s is not None]
    m_pre, m_post = statistics.mean(s_pre), statistics.mean(s_post)
    from scipy.stats import mannwhitneyu
    p_mw = mannwhitneyu(s_post, s_pre, alternative="two-sided").pvalue
    lo, hi = boot_ci(s_pre, s_post)

    rows, ps = [], []
    for q in SCORED:
        k = f"Q{q['id']}"
        a1 = [d[k] for d in pre if k in d]; a2 = [d[k] for d in post if k in d]
        c1 = sum(x == q["answer"] for x in a1); c2 = sum(x == q["answer"] for x in a2)
        p = fisher(c1, len(a1), c2, len(a2)) if a1 and a2 else 1.0
        ps.append(p)
        rows.append({"q": k, "label": SHORT.get(q["id"], q["q"]), "before": pct(c1, len(a1)), "after": pct(c2, len(a2)),
                     "n_before": len(a1), "n_after": len(a2), "p": p})
    for r, ph in zip(rows, holm(ps)):
        r["p_holm"] = ph

    def dist(group, key):
        v = [d[key] for d in group if key in d]
        return Counter(v), len(v)
    conf_pre, n_cp = dist(pre, "C1"); conf_post, n_cq = dist(post, "C1")
    plan, n_plan = dist(post, "C3"); rec, n_rec = dist(post, "C4"); prior, n_prior = dist(pre, "C2")
    confident = lambda c, n: pct(c.get(2, 0) + c.get(3, 0), n)  # Somewhat or Very

    slug = re.sub(r"[^a-z0-9]+", "-", a.venue.lower()).strip("-")
    out = pathlib.Path(a.out) if a.out else ROOT / "talk-kit/results" / f"{a.date}-{slug}"
    out.mkdir(parents=True, exist_ok=True)
    line = (f"Attendees' average quiz score rose from {m_pre:.0f}% before the talk to {m_post:.0f}% after "
            f"(n = {len(s_pre)} before, {len(s_post)} after).")
    if a.attendees:
        line = f"{a.attendees} people attended. " + line
    if n_plan:
        line += f" {pct(plan.get(0, 0), n_plan)}% said they plan to do a skin check in the next month."

    md = [f"# Talk results: {a.venue}, {a.date}", "", f"**Result line (copy into pitches, press release, reports):** {line}", "",
          "## Overall", "", "| Measure | Before | After |", "|---|---|---|",
          f"| Quizzes answered | {len(s_pre)} | {len(s_post)} |",
          f"| Average score | {m_pre:.0f}% | {m_post:.0f}% |",
          f"| Confident they can self-check (somewhat or very) | {confident(conf_pre, n_cp) if n_cp else 'n/a'}% | {confident(conf_post, n_cq) if n_cq else 'n/a'}% |",
          "", f"Score change: {m_post - m_pre:+.0f} points (bootstrap 95% CI {lo:+.0f} to {hi:+.0f}); Mann-Whitney U p = {p_mw:.3g}.",
          "Before and after groups are anonymous and unpaired, so they are compared as independent samples.", ""]
    if n_prior:
        md.append(f"Checked own skin in the past year (before the talk): {pct(prior.get(0, 0), n_prior)}% yes (n = {n_prior}).")
    if n_plan:
        md.append(f"Plan to do a skin check in the next month (after): {pct(plan.get(0, 0), n_plan)}% yes (n = {n_plan}).")
    if n_rec:
        md.append(f"Would recommend the talk to a friend: {pct(rec.get(0, 0), n_rec)}% yes (n = {n_rec}).")
    md += ["", "## Per question (% correct)", "", "| Question | Before | After | Change | p (Holm) |", "|---|---|---|---|---|"]
    for r in rows:
        ch = (r["after"] - r["before"]) if None not in (r["after"], r["before"]) else None
        md.append(f"| {r['q']}. {r['label']} | {r['before']}% | {r['after']}% | {ch:+d} | {r['p_holm']:.2g} |")
    weak = [r for r in rows if r["after"] is not None and r["after"] < 70]
    md += ["", "## What to fix in the talk", ""]
    md += [f"- {r['q']} ({r['label']}): only {r['after']}% correct after the talk. Strengthen that slide." for r in weak] or ["- Every question reached 70% or more correct after the talk."]
    md += ["", "![Before and after by question](chart.png)", ""]
    (out / "results.md").write_text("\n".join(md), encoding="utf-8")
    summary = {"date": a.date, "venue": a.venue, "attendees": a.attendees, "n_before": len(s_pre), "n_after": len(s_post),
               "before_pct": round(m_pre), "after_pct": round(m_post), "ci": [round(lo, 1), round(hi, 1)], "p_mannwhitney": p_mw,
               "plan_check_pct": pct(plan.get(0, 0), n_plan) if n_plan else None,
               "recommend_pct": pct(rec.get(0, 0), n_rec) if n_rec else None,
               "confident_after_pct": confident(conf_post, n_cq) if n_cq else None, "questions": rows, "result_line": line}
    (out / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    chart(rows, out / "chart.png", f"Correct answers before and after the talk ({a.date})")

    if not a.no_talks_csv:
        existing = list(csv.DictReader(TALKS.open(encoding="utf-8"))) if TALKS.exists() else []
        existing = [r for r in existing if not (r["date"] == a.date and r["venue"] == a.venue)]
        existing.append({"date": a.date, "venue_type": a.venue_type, "county": a.county, "language": a.language,
                         "attendees": a.attendees or "", "n_before": len(s_pre), "n_after": len(s_post),
                         "before_pct": round(m_pre), "after_pct": round(m_post),
                         "plan_check_pct": summary["plan_check_pct"] or "", "recommend_pct": summary["recommend_pct"] or "",
                         "confident_after_pct": summary["confident_after_pct"] or "", "venue": a.venue})
        existing.sort(key=lambda r: r["date"])
        with TALKS.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=TALK_COLS); w.writeheader(); w.writerows(existing)
        print("updated", TALKS.relative_to(ROOT), "-> run python3 -I site/build_pages.py to refresh the Impact page")
    print("wrote", out.relative_to(ROOT) if out.is_relative_to(ROOT) else out)
    print(line)


if __name__ == "__main__":
    main()
