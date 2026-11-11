# Every Shade talk kit: Friday, November 20, 2026, 6:00 pm Eastern (Zoom)

Everything needed to give the 45-minute senior talk and measure whether it worked.

| File | What it is | Status |
|---|---|---|
| `slides/Every-Shade-Senior-Talk-2026-11-20.pptx` | 20-slide deck, 16:9, large type, speaker notes on every slide | Built and visually checked. Slides 7, 8, and 10 use teaching drawings (`slides/illustrations/`); licensed clinical photos are optional, see `IMAGE-SOURCES.md` |
| `slides/build_deck.js` | Generator (pptxgenjs). Edit text here and rebuild rather than hand-editing the deck | |
| `handout/handout-en.pdf` | Two-page large-print handout (print at 100%, letter) | Done |
| `handout/handout-en.html` | Source; `../render_pdf.sh handout-en.html handout-en.pdf` rebuilds | |
| `quiz/quiz-pre.pdf`, `quiz/quiz-post.pdf` | Paper pre/post quiz, anonymous, matched by a 4-digit code | Done |
| `quiz/zoom-polls.md` | The same questions, ready to paste into two Zoom polls | Done |
| `quiz/answer-key.md` | Answers and which slide covers each question | Done |
| `quiz/scoring.xlsx` | Paste responses; Summary tab computes pre/post % and knowledge gain overall and per question | Done |
| `quiz/quiz-content.json` + `build_quiz.py` | Edit questions here; `python3 -I build_quiz.py` regenerates everything above | |
| `../languages/` | Translated handouts (es, hi, ur, gu, ht, ko): machine drafts awaiting native-speaker review | Draft |

## Before November 20

1. **Images (optional).** Slides 7, 8, and 10 now use simple teaching drawings, so the deck is usable as is. To use clinical photos instead, pick from `IMAGE-SOURCES.md` (openly licensed, authoritative sources, with the exact credit line) and swap them in with `imageBox` in `build_deck.js`. Never use images scraped from the web or from clinic.
2. **Physician review.** Send `MEDICAL-REVIEW-PACKET.md` (a claim-by-claim checklist with sources), the deck, and the handout to a dermatologist or the Every Shade advisor for a 15-minute review. Every claim is drawn from AAD / Skin Cancer Foundation public guidance and the two cited papers, but a clinician must sign off before it is shown.
3. **Zoom.** Create the two polls from `quiz/zoom-polls.md` (Anonymous on). Turn on live captions. Set "share screen" so slides fill the window. Have a co-host watch chat.
4. **Send the handout** to each registered attendee or center two days ahead (email the PDF; centers that print should use letter paper, single-sided, 100%).
5. **Run-through.** Rehearse once with the notes. Target 30 minutes of slides, 10 of questions, 5 of quiz.

## Run of show (45 minutes)

| Minute | Slide | What happens |
|---|---|---|
| 0 to 3 | 1 | Welcome, captions on, who we are, "students, not doctors" |
| 3 to 7 | 2 | Launch **Before** poll (or paper quiz). 3 minutes |
| 7 to 12 | 3 to 6 | Why it matters, three kinds, myths, risk |
| 12 to 24 | 7 to 12 | What to look for on every tone, the spots people miss, nails, ugly duckling |
| 24 to 30 | 13 to 14 | The 10-minute check, reminders, the free online guide |
| 30 to 36 | 15 to 18 | When to see a doctor, what the visit is like, where to go in NJ, sun |
| 36 to 40 | 19 | Three things to take home. Launch **After** poll |
| 40 to 45 | 20 | Questions. Never diagnose; redirect to care and offer to help find it |

## After the talk

1. Download the Zoom poll report (Reports > Meeting > Poll Report) or collect the paper quizzes.
2. Enter responses in `quiz/scoring.xlsx` (one row per quiz, letter per question). The Summary tab gives: average score before and after, change in points, relative improvement, and per-question correct rates.
3. Report it as: "Attendees' average quiz score rose from X% to Y% (n = Z) after the talk." Log attendance (count) and the venue.
4. 30 days later, send registered attendees a two-line email: "Did you do a skin check this month? Yes / No." Record the response rate.
5. Add the numbers to the med-admissions ledger and to the chapter report in `../toolkit/`.
