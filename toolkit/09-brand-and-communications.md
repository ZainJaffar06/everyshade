# 09. Brand and communications

The brand is simple so it is easy to keep consistent: five swatches, two fonts, warm neutrals, large type. Follow this page and a flyer from your chapter will look like it came from the same group as one from Rutgers, which is the point.

## The name

Your chapter is "Every Shade at [School]": "Every Shade at the University of Maryland," "Every Shade at Howard University." In the wordmark and social handles it is lowercase, "every shade," matching the site. In conversation, "Every Shade."

Do not write "Every Shade [School]," "[School] Every Shade," "Every Shade Club," or "Every Shade Society." Do not add a tagline to the name or invent a separate chapter name. The Rutgers group is "Every Shade" or, when the distinction matters, "Every Shade (Rutgers)."

## The logo

Five rounded swatches fanned from a single rivet, in the five mid tones of the palette. It is an inline SVG on the site and should be inline wherever you can manage it, because it then picks up the palette in light and dark mode. Do not rotate it, recolor it, add a sixth swatch, put text inside it, or place it on a busy photo.

```html
<svg viewBox="-12 8 224 140" role="img" aria-label="Every Shade logo: five skin-tone swatches fanned out">
  <rect x="82" y="20" width="36" height="130" rx="18" fill="#EFCBB0" transform="rotate(-44 100 132)"/>
  <rect x="82" y="20" width="36" height="130" rx="18" fill="#DDAA84" transform="rotate(-22 100 132)"/>
  <rect x="82" y="20" width="36" height="130" rx="18" fill="#C28559"/>
  <rect x="82" y="20" width="36" height="130" rx="18" fill="#9C623A" transform="rotate(22 100 132)"/>
  <rect x="82" y="20" width="36" height="130" rx="18" fill="#6B4127" transform="rotate(44 100 132)"/>
  <circle cx="100" cy="132" r="6" fill="#FFFFFF"/>
</svg>
```

On the site the fills are CSS variables (var(--t1) through var(--t5), and var(--rivet) for the center dot) so the rivet flips to the dark background in dark mode. In print, use the hex values above with a white rivet on a light background, or #1A110C for the rivet on a dark background. For one-color use (a stamp, a patch), set all five swatches in the ink color #2B1A12 with a white rivet.

Minimum size: 24 pixels tall on screen, 10 millimeters in print. Clear space around it of about a fifth of its height. Next to the wordmark, the mark is 30 pixels tall and "every shade" is set in Manrope ExtraBold at about 1.35rem with a 10 pixel gap, as in the site header.

## Colors

| Role | Light mode | Dark mode |
|---|---|---|
| Ground (page background) | #FFFFFF | #1A110C |
| Band (tinted sections) | #F7F1EC | #24180F |
| Ink (text) | #2B1A12 | #F6ECE4 |
| Muted (secondary text) | #6B5446 | #CDB8A8 |
| Rule (borders) | #E6D9CF | #3B2A1F |
| Accent (links, hover) | #8E5632 | #E3A877 |

The tone palette, used in the logo, the tone strip, and small accents, is the same in both modes:

| Token | Hex |
|---|---|
| t1 | #EFCBB0 |
| t2 | #DDAA84 |
| t3 | #C28559 |
| t4 | #9C623A |
| t5 | #6B4127 |
| t6 | #3D2416 |

The tone strip is the six tones in order as equal-width horizontal bands, 10 pixels tall on screen or 4 millimeters in print, used as a divider once or twice per page. Body text is always ink on ground or ink on band, never on a tone swatch. Accent is for links and small highlights, never paragraphs. No red, blue, or green anywhere.

## Fonts

Headings: Manrope, weights 600 and 800. Body: Atkinson Hyperlegible, weights 400 and 700, plus italic 400. Both are free on Google Fonts. Atkinson Hyperlegible was designed for low-vision readers, which is why it is the body font and why you should not substitute it in anything an audience reads. If you cannot load web fonts (a Word document, a borrowed laptop), use Arial for both. No serifs, scripts, or condensed fonts.

Sizes: body 18 pixels on screen, 12 point minimum in print, 16 point for the handout. The brand is big type. If a flyer looks like it has too much white space, it is probably right.

## Flyer

Use the flyer template in talk-kit/ (Every-Shade-Senior-Talk-Flyer.pdf in the repo shows the layout). Change only your chapter name, the date, time, and place, your chapter email and phone, and the language line if you are bringing an interpreter or translated handouts.

Structure, top to bottom: logo and wordmark; the headline "Skin cancer doesn't look the same on everyone."; three short lines on what the talk covers (how it looks on every skin tone, the monthly skin check, where to get checked for free); date, time, place, and "Free. Everyone welcome."; chapter name and contact; the tone strip; the full disclaimer at no less than 10 point. Print on white or the band color, letter size for bulletin boards, half-letter for handouts. Give the coordinator the PDF two weeks before the talk.

Calendar blurb for a library or center newsletter:

> Free talk: Skin Cancer on Every Skin Tone. Students from Every Shade at [School] show what skin cancer can look like on light, medium, and dark skin, teach a simple monthly skin check, and share where to get a spot checked for free or low cost. Large-print handout included. [Date, time, place.]

## Social posts

Social media is optional and does not book talks. If you run an account, it exists so partners can find you and so you can thank them. Handle: everyshade.[school], lowercase. Profile picture: the logo on the band color. Bio: "Free skin cancer talks for every skin tone. Students at [School], not doctors. Book a talk: [chapter email]." Pin a post with the disclaimer.

Posts that work: a thank-you after each talk with a photo of the room (only with the organization's permission and never showing attendees' faces without written agreement); the flyer for an upcoming public talk; a one-fact post using one of the three cited facts with the source in the caption; a "we're looking for a reviewer who speaks [language]" ask.

Do not post: deck images, any skin photo, quiz numbers smaller than a semester's pooled numbers, anything that answers a medical question, or anything naming a clinic as "recommended." Reply to every DM about a spot with the redirect script and the resource link. Do not look at the photo.

## Press one-liner

For a campus paper or local outlet, say this and send the site link:

> Every Shade at [School] is a student group that gives free 45-minute talks at senior centers, libraries, and community organizations on how skin cancer looks on every skin tone, teaches a simple monthly skin check, and connects people to free and low-cost care. Our members are students, not doctors; our materials are reviewed by a physician advisor.

If asked for numbers, give the pooled semester numbers from your last report, with the n. If asked for a story about someone whose cancer was found because of a talk, say you do not collect that information. Refer anything bigger than a campus paper to everyshadescreening@gmail.com.

## What not to claim

- Not "screening," "exam," "clinic," or "check-up." We give talks.
- Not "doctors," "medical team," "clinicians," or "dermatology students." We are students.
- Not "saves lives," "catches cancer early," or "detects melanoma." We teach what to look for.
- Not "partnered with," "endorsed by," or "affiliated with" the AAD or anyone else we are not formally affiliated with. We cite them. That is not a partnership.
- Not "the first," "the only," or "the largest." SOCS Serves and the AAD's free checks are bigger.
- Not "evidence-based" without pointing to the evidence. Say "our materials cite the AAD, the Skin Cancer Foundation, the CDC, and peer-reviewed research."
- Not "certified" or "trained by dermatologists," or any credential the presenters do not hold.
- Not any statistic beyond the three in section 01 or your own quiz data with the n attached.

When in doubt, describe what you actually did last Tuesday. That is always allowed.
