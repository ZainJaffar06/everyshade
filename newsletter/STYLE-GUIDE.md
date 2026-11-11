# Derm × AI weekly: style guide and workflow

**What it is.** One short post a week (450 to 700 words) on one AI-in-dermatology or AI-in-medicine startup, paper, or trend, written by Zain Jaffar. Public voice plus portfolio for venture fellowships (Contrary, Insight) and for dermatology/AI labs.

**Where it lives.** Draft in `newsletter/issues/YYYY-MM-DD-slug.md`. Publish on LinkedIn (article + a 3-line post) and Substack (same text). Cross-post the link on X. Keep the canonical copy in this repo.

**Cadence.** Monday draft (Claude), Tuesday edit (Zain, 30 min), Wednesday morning publish. Miss a week rather than publish a weak one.

## Format (every issue)

1. **Title**: a claim, not a topic. "Derm AI keeps failing the same test" beats "On dermatology AI benchmarks."
2. **The one-line take** (bold, first line): what Zain believes after looking at this.
3. **What it is** (80 to 120 words): company/paper/trend, who, when, what they claim, with a link.
4. **Why it matters** (150 to 250 words): the mechanism, the market, or the clinical gap. Use one number max per paragraph, sourced.
5. **The catch** (100 to 150 words): the thing a careful reader would push on. Data, deployment, regulation, skin-tone validation, reimbursement, workflow.
6. **What I'd watch** (3 bullets): concrete signals over the next 6 to 12 months.
7. **From the clinic** (optional, 2 to 3 sentences): something Zain saw as a Mohs/derm MA or in research that connects, with no patient details.
8. **Sources** (3 to 6 links).

## Voice

- First person, plain, specific. Short sentences. No hedging stacks ("may potentially").
- One opinion per issue, stated plainly, then defended.
- Say what you do not know. "I could not find their validation data" is a finding.
- No em-dashes. No "game-changer," "revolutionize," "unlock."
- Skin-of-color validation is a recurring lens, not a tagline: ask of every product whether it was tested on Fitzpatrick V-VI and acral sites.

## Hard rules

- Verify every number against the primary source before publishing. Link it.
- No patient information, ever, including de-identified anecdotes that could be re-identified.
- Disclose affiliations when writing about Stanford, Harvard/MEE, Rutgers, or any company Zain has talked to.
- Do not comment on a company's financials beyond public filings and press.
- If the issue argues a company is wrong, email them for comment first and say so.

## Weekly workflow

1. Monday: Claude drafts from the topic backlog (`TOPIC-BACKLOG.md`) with sources, writes `issues/<date>-<slug>.md`, and marks claims needing verification with `[verify]`.
2. Tuesday: Zain reads the primary sources, resolves every `[verify]`, cuts 10%, adds "From the clinic."
3. Wednesday: publish. Add the link to `PUBLISHED.md`. Post the 3-line LinkedIn version.
4. Monthly: look at which issues got replies from people who matter (founders, PIs, fellows). Write more of those.
