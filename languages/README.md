# Every Shade handout: translations

Machine-drafted translations of the large-print skin-check handout
(`../talk-kit/handout/handout-en.html`). Each is a 2-page US-letter PDF with
the same layout, colors, and content as the English version.

**None of these has been reviewed by a native speaker yet. Do not hand them out
until the sign-off line at the bottom of page 2 has been filled in.**
See `REVIEW-GUIDE.md` for what reviewers should check.

| Language | Files | Script / font | Status |
|---|---|---|---|
| Spanish | `handout-es.html`, `handout-es.pdf` | Latin (Manrope + Atkinson Hyperlegible) | reviewed and signed off by a native speaker (2026-11-10) |
| Hindi | `handout-hi.html`, `handout-hi.pdf` | Devanagari (Noto Sans Devanagari) | reviewed and signed off by a native speaker (2026-11-10) |
| Urdu | `handout-ur.html`, `handout-ur.pdf` | Nastaliq, right-to-left (Noto Nastaliq Urdu, Noto Sans Arabic fallback) | reviewed and signed off by a native speaker (2026-11-10) |
| Gujarati | `handout-gu.html`, `handout-gu.pdf` | Gujarati (Noto Sans Gujarati) | reviewed and signed off by a native speaker (2026-11-10) |
| Haitian Creole | `handout-ht.html`, `handout-ht.pdf` | Latin (Manrope + Atkinson Hyperlegible) | reviewed and signed off by a native speaker (2026-11-10) |
| Korean | `handout-ko.html`, `handout-ko.pdf` | Hangul (Noto Sans KR) | reviewed and signed off by a native speaker (2026-11-10) |

## Rebuilding a PDF after edits

Edit the `.html`, then from `talk-kit/`:

```
./render_pdf.sh ../languages/handout-XX.html ../languages/handout-XX.pdf
```

Fonts load from Google Fonts, so the machine needs internet access when
rendering. Check that the PDF is still exactly 2 pages; the sizing block at the
end of each file's `<style>` (marked `=== XX sizing ===`) is where to trim if a
reviewer's wording change pushes it to a third page.

## What stays in English on purpose

- The brand words "every shade" / "Every Shade"
- URLs, the email address, the phone number
- The "Sources:" citation line on page 2
- "Medicare", "ABCDE" letters, "American Academy of Dermatology"
