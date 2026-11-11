# Talk results: from Zoom poll to Impact page in 5 minutes

After every talk:

1. **Download the poll report.** Zoom web portal > Reports > Usage > (the meeting) > Poll Report > export CSV. Save it in `talk-kit/results/raw/` (this folder is never committed, so raw files stay private). For in-person paper quizzes, type the letters into `talk-kit/quiz/scoring.xlsx` (Responses tab) instead.
2. **Run the analysis** from the repo root:

   ```bash
   python3 -I talk-kit/results/analyze_talk.py --zoom talk-kit/results/raw/<file>.csv --date 2026-11-20 --venue "Zoom (open)" --venue-type "open Zoom" --county Statewide --language English --attendees 34
   ```

   Paper quizzes: replace `--zoom ...` with `--xlsx talk-kit/quiz/scoring.xlsx`.
3. **Read** `talk-kit/results/<date>-<venue>/results.md`. It has the result line to paste into pitches, the press release, and grant applications; a per-question table; and a "what to fix in the talk" list (any question under 70% correct after the talk).
4. **Publish**: `python3 -I site/build_pages.py` refreshes the public Impact page from `site/talks.csv` (group averages only, no names). Commit and push.
5. **Log** attendance and the result line in the outreach tracker row for that host, and send the host a thank-you note within 48 hours.

## What the analysis does

- Matches Zoom answers to the quiz by question text, so it works whether the two polls come in one file or two. Names the polls "Before the talk" and "After the talk" (as in `talk-kit/quiz/zoom-polls.md`).
- Quizzes are anonymous, so before and after are compared as independent groups: average score (Mann-Whitney U, bootstrap 95% CI for the change) and each question (Fisher exact test, Holm correction for 10 questions).
- Reports confidence to self-check (before and after), past-year self-check, plan to check in the next month, and would-recommend.
- Never stores names, even if a poll was accidentally left non-anonymous.

Tested on simulated poll reports in both Zoom layouts (one file with both polls; one file per poll).
