# Every Shade outreach engine

Goal: keep a steady calendar of talks instead of booking one at a time. Nothing here sends email by itself.

## What is here

| File | Purpose |
|---|---|
| `data/senior_and_community_centers.csv` | 166 NJ senior centers, county Offices on Aging, community centers, and nonprofit senior programs, all 21 counties. 42% have an email; 98% a phone |
| `data/libraries_and_faith.csv` | 112 public libraries (every county, director or adult-programming librarian) and 139 faith communities serving Black, Hispanic, Haitian, South Asian, Korean, Filipino, and Chinese communities, plus 14 faith networks. 78% have an email |
| `data/*_README.md` | Sources mined, counts by county, thin spots, which pages blocked fetching |
| `data/all_targets.csv` | The merged, de-duplicated, prioritized list (417 rows) |
| `tracker.xlsx` | The working pipeline. `Pipeline` sheet: one row per target with status dropdown, dates, talk outcome columns. `Dashboard`: counts by status, county, type, follow-ups due today, talks done, attendance, average knowledge gain. `Cadence`: the 4-touch schedule |
| `templates/pitches.md` | Pitch emails for senior centers, Offices on Aging, libraries, faith communities, community centers; day-5 follow-up; phone script; "are you doctors?" answer; web-form version |
| `build_tracker.py` | Rebuilds `tracker.xlsx` from the CSVs. Preserves your status/notes columns by id, so it is safe to re-run after adding research |
| `generate_pitches.py` | Writes personalized drafts to `drafts/` and a `mailmerge.csv`. Filters: `--priority A`, `--county Essex`, `--type library`, `--limit 10`, `--ids ...` |
| `drafts/` | Current batch (12 Essex/Middlesex/Morris/Somerset senior-center and aging-office pitches). These same 12 are sitting as Gmail drafts in the connected account |

Priority: A = tier-1 county (Essex, Union, Morris, Middlesex, Somerset) or a strong tier-2 target, with an email on file (145 rows). B = reachable but farther or phone-only (242). C = thin (30).

## Weekly routine (30 minutes)

1. `python3 -I generate_pitches.py --priority A --limit 15` (or pick a county). Read each draft, personalize one sentence from the org's own page, send. Set `status = emailed`, `first_contact`, `next_action = +5 days`.
2. Open `tracker.xlsx` Dashboard: "Due for follow-up today." Send the day-5 nudge or make the day-12 call. Update `last_touch` and `next_action`.
3. Replies: answer the same day, offer three dates, set `status = booked`, `talk_date`, `format`.
4. After a talk: `status = done`, `attendance`, `pre_pct`, `post_pct` from `talk-kit/quiz/scoring.xlsx`.
5. Monthly: re-run `build_tracker.py` after adding any new rows to the CSVs; re-approach `parked` rows older than 90 days with the newest outcome line.

## Rules

- Only emails and names seen on a fetched page were recorded. Rows flagged `verify` in notes came from search excerpts; open the source URL before sending.
- Send from the Every Shade Gmail or the Rutgers address, never a personal one. Sign with the site and phone.
- No mass sends. One personalized email per organization, on the cadence above.
- Faith communities: ask for the health-ministry or seniors coordinator; offer the translated handout where `languages_served` matches.
