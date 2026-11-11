# libraries_and_faith.csv — README

Outreach contact dataset for **Every Shade** (free skin-cancer-awareness talks for NJ seniors). Built 2026-11-10 by automated web research; **no one has been contacted**. Treat every row as a lead to verify, not a confirmed contact.

File: `libraries_and_faith.csv` (UTF-8, RFC-4180 quoting). Columns: `name,type,county,town,address,phone,email,website,contact_name,contact_title,best_channel,languages_served,source_url,notes`.

## Totals

Coverage pass 2 (2026-11-10): appended 182 libraries and 0 senior centers (senior centers went to `senior_and_community_centers.csv`; see its README).

- **433 rows**: 294 libraries, 139 faith rows (94 church, 14 mosque, 8 temple, 9 gurdwara, 14 faith_network).
- **Libraries now cover every entry on the NJ State Library "NJ Public Libraries Arranged by County" page as fetched 2026-11-10 (294 entries; 112 from pass 1 + 182 appended).** Branches are included only where that page lists them separately (4 Gloucester County Library branches; Mercer HQ branch was already a row). County-system branches the page does not list (Ocean, Monmouth, Somerset, Burlington, Camden, Atlantic, Morris, Sussex, Hunterdon, Cumberland, Warren county library branches) are not rows.
- **Email coverage**: all rows 370/433 (85%); libraries 285/294 (97%); faith rows 85/139 (61%). Pass-2 library rows: 175/182 with a director email.
- Libraries with no email in the directory (9): Somerville, Manville (pass 1), Mount Holly Library and Lyceum, Stratford, Oxford, and the 4 Gloucester County Library branches (Glassboro, Greenwich Twp, Logan Twp, Swedesboro) — `best_channel` = phone.
- Phone coverage: 415/433. Rows with neither email nor phone: 9 (all faith rows, flagged in `notes`; `best_channel` = web_form).
- best_channel: {'email': 370, 'phone': 55, 'web_form': 8}.

## Rows by county and type

| County | library | church | mosque | temple | gurdwara | faith_network | total |
|---|---|---|---|---|---|---|---|
| Atlantic | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| Bergen | 62 | 17 | 2 | 2 | 1 | 0 | 84 |
| Burlington | 12 | 0 | 0 | 0 | 0 | 0 | 12 |
| Camden | 13 | 1 | 0 | 0 | 0 | 3 | 17 |
| Cape May | 3 | 0 | 0 | 0 | 0 | 0 | 3 |
| Cumberland | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| Essex | 20 | 23 | 2 | 0 | 0 | 5 | 50 |
| Gloucester | 16 | 0 | 0 | 0 | 1 | 0 | 17 |
| Hudson | 10 | 16 | 0 | 0 | 1 | 0 | 27 |
| Hunterdon | 7 | 0 | 0 | 0 | 0 | 0 | 7 |
| Mercer | 6 | 3 | 1 | 1 | 3 | 3 | 17 |
| Middlesex | 24 | 9 | 3 | 3 | 2 | 1 | 42 |
| Monmouth | 23 | 0 | 1 | 0 | 0 | 1 | 25 |
| Morris | 33 | 3 | 1 | 1 | 0 | 1 | 39 |
| Ocean | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| Passaic | 15 | 9 | 2 | 0 | 0 | 0 | 26 |
| Salem | 4 | 0 | 0 | 0 | 0 | 0 | 4 |
| Somerset | 8 | 1 | 1 | 1 | 1 | 0 | 12 |
| Sussex | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| Union | 20 | 12 | 1 | 0 | 0 | 0 | 33 |
| Warren | 5 | 0 | 0 | 0 | 0 | 0 | 5 |
| **All** | 294 | 94 | 14 | 8 | 9 | 14 | 433 |

Pass-1 table (251 rows) superseded by the table above.

Priority counties (Essex, Union, Morris, Middlesex, Somerset, Bergen, Hudson, Passaic, Mercer) hold 330 of 433 rows. Every NJ county has at least one library row; Ocean (2) and Sussex (2) are low because each is served by a county library system whose branches are not separate directory entries.

## Faith rows by community served (languages_served tag counts)

Spanish: 46, Korean: 14, Haitian Creole: 14, Punjabi: 9, Tagalog: 8, Hindi: 6, French: 6, Gujarati: 5, Arabic: 3, Mandarin: 3, Telugu: 2, Portuguese: 2, Urdu: 1, Tamil: 1, Kannada: 1, Polish: 1, Taiwanese: 1, Cantonese: 1. Rows with no language tag are English-language Black churches, mosques with no language shown, or networks.

Breakdown of faith rows by community: Black churches (Baptist/AME/non-denominational) ~22; Haitian congregations + Creole-Mass parishes 13; Hispanic/Latino (Spanish-Mass Catholic parishes + evangelical/Pentecostal/SDA) ~40; mosques/Islamic centers 14; Hindu temples 8; Sikh gurdwaras 9; Korean churches/parishes 13; Filipino and Chinese churches 7; interfaith/diocesan/health-ministry networks 14.

## Coverage pass 2 (2026-11-10) — library details

- Source for all 182 appended rows: NJ State Library directory page (same URL as pass 1), re-fetched 2026-11-10 and parsed in full (294 library entries, 285 with a director email). Each appended row: `type`=library, `contact_name`=director as printed (", acting"/", interim" kept when printed), `contact_title`="Director", `best_channel`=email when an email is printed, else phone. Notes end with "Added in coverage pass 2 (2026-11-10)."
- De-duplication: every directory entry was matched to existing rows by phone, email and normalized name; all 112 pass-1 library rows matched exactly one entry and none were changed. West Caldwell Public Library shares Verona's director and email (pascale@veronalibrary.org) in the directory; it was added as its own row with a note.
- Flags in `notes`: Milford Public Library (Hunterdon) is printed with director@newmilford.bccls.org, which looks like a New Milford (Bergen) address — verify before emailing. Phone numbers were normalized to (xxx) xxx-xxxx; 4-digit ZIPs printed without the leading zero were padded (e.g., NJ 8096 -> NJ 08096).
- Not done: county-system branch rows (directory does not list them), and no library staff pages were fetched for adult-services contacts in pass 2 (director is the contact on all 182 new rows).

## Directories mined (best sources first)

1. **NJ State Library — "NJ Public Libraries Arranged by County"** (`njstatelib.org/.../new-jersey-public-libraries-directory/`). One page lists every public library (296 parsed) with address, phone, **director name and director email** (285/296 have emails). This is the source for every library row unless `notes` says otherwise. By far the highest-yield page.
2. **Archdiocese of Newark parish finder** (`rcan.org/parishes/`): 218 parishes with `en | es` language tags (83 Spanish-Mass parishes), addresses and websites; plus the Haitian, Korean and Filipino Apostolate pages (`rcan.org/haitian-apostolate/`, `/korean-apostolate/`, `/filipino-apostolate/`) which list the parishes offering Creole/Korean/Tagalog Masses and give apostolate directors' emails/phones. Parish phones/emails were then pulled from each parish's own website.
3. **Diocese of Paterson Hispanic Ministry page** (40 Spanish-Mass parishes in Passaic/Morris/Sussex; office email + phone). Read via browser because the site is Cloudflare-protected; only the diocesan office and Paterson cathedral were kept as rows because individual parish sites were also blocked.
4. **Diocese of Metuchen** Hispanic ministry page (office email only; parish list is a staff-only form).
5. **worldgurudwaras.com/location/new-jersey** (11 NJ gurdwaras; detail pages carry phone + Cloudflare-obfuscated email, decoded) cross-checked against each gurdwara's own site.
6. Official websites of mosques, temples, churches and networks (curl + regex for mailto/phone/address), found via web search.
7. Third-party church directories (**churcheslist.com, christianity.com, disciplepair.com, discovermass.com, ebiblestories.com, newbrunswick.com**) for phone/address where a congregation has no usable website — 35 faith rows cite one of these as `source_url` (always noted in `notes`). Emails on these pages were NOT recorded (they are the directory's own addresses).

Not usable / dead ends: Hartford Institute mosque database (no-reprint terms), AME NJ Annual Conference pages (JS-only Wix), ABCNJ church PDF (404), faithstreet and several eCatholic parish sites (Cloudflare 403), BAPS.org (403; used usa.akshardham.org instead), DuckDuckGo/Bing via curl (bot challenge).

## Contact-name policy

- Library `contact_name`/`contact_title` = the **director** from the State Library directory, except 12 libraries where an adult-services / programming contact was visible on the library's own staff page (Teaneck, Bloomfield, Long Branch, Englewood, Cape May County, Warren County, Hunterdon County, Passaic, Scotch Plains, Newark, Fort Lee, Bergenfield) — see `notes`.
- Every email, phone and contact name was copied from a page actually fetched (the `source_url`). Nothing was guessed or constructed. Personal-looking clergy Gmail/Yahoo addresses were kept only when they were the sole address the congregation publishes.
- Addresses come from the fetched page where possible, otherwise from the directory listing cited.

## Thin spots / caveats

- **Faith email coverage is 85/139 (61%)**; most Black and Haitian congregations in directories publish phone only. Expect phone-first outreach there.
- **Paterson-diocese Spanish parishes** (St. Anthony of Padua, OL of Victories, OL of Lourdes, Holy Trinity Passaic, St. Mary Passaic, OLMC Passaic, Sacred Heart Dover, St. Margaret Morristown) are not individual rows — parish sites are Cloudflare-blocked; go through the diocesan Hispanic office row.
- **Trenton and Camden dioceses**: only the Trenton cathedral and the Camden Hispanic-ministry switchboard; no Lakewood/Long Branch/Vineland/Bridgeton Spanish parishes.
- **Korean churches**: large Protestant congregations (Chodae, KCCNJ, Promise Church Leonia) have thin public contact info; Promise Church was dropped (no fetched page with a phone). Korean Catholic parishes are well covered.
- **Hindu/Indian**: BAPS Edison/Parsippany/Cherry Hill mandirs not listed (site blocked); Gujarati Samaj of NJ not found; Indo-American senior associations (Hudson County, IASONJ, Clifton) exist but no contact page was fetched, so no rows.
- **Mosques**: no Jersey City, Elizabeth (MCC Union County) or Trenton masjid rows — official sites blocked or absent; nearest covered are ICUC (Union) and NIA/Masjid Muhammad (Newark).
- **Monmouth, Ocean, Burlington, Atlantic, Cumberland** have libraries only (plus one Monmouth mosque, one Gloucester gurdwara); no Black/Hispanic congregations there yet.
- 7 rows have website only (no email/phone): Fountain Baptist Summit, St. Leo Irvington, OLMC Orange, St. Anthony Belleville, St. Joseph Lodi, Filipino International SDA, CAIR-NJ, plus Holy Spirit East Orange (phone via Archdiocese). Call or use the site form.
- Several churcheslist/christianity.com phone numbers may be stale; the pewsearch.com directory was found to recycle phone numbers across listings and was not used for phones.
- `languages_served` is filled only when the source showed it (Mass-language tags, church name, or site language); blank does not mean English-only.

## Suggested next steps

- Verify emails by sending a short bilingual pitch to the `faith_network` rows first (apostolates, diocesan Hispanic offices, Faith in New Jersey, Faith-in-Prevention coalitions) — each is a multiplier over dozens of congregations.
- For libraries, email the director and ask to be routed to the adult/senior programming librarian; county systems (Somerset, Morris, Mercer, Bergen BCCLS members) program centrally.
