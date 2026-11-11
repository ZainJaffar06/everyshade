# senior_and_community_centers.csv — README

Research-only contact dataset for Every Shade outreach (free skin-cancer talks for NJ seniors). Built 2026-11-10. **Nobody has been contacted.**

- **Rows:** 350 (166 from pass 1 + 184 appended in coverage pass 2). Coverage pass 2 (2026-11-10): appended 0 libraries and 184 senior centers (169 `senior_center` + 15 `nonprofit_senior_program`; libraries went to `libraries_and_faith.csv`). The pass-1 row cap no longer applies; the trimmed names listed at the bottom were restored except where noted.
- **Rows with an email:** 76 (21.7%) — pass 2 added mostly phone-only directory listings (6 of 184 new rows have an email, all the Morris County nutrition inbox). Rows with a phone: 346 (98.9%). best_channel: phone 270, email 76, web_form 3, mail 1 (Fanwood Seniors, "by mail" only).
- **Columns:** `name,type,county,town,address,phone,email,website,contact_name,contact_title,best_channel,languages_served,source_url,notes` (UTF-8, comma-quoted).
- **Rule followed:** emails, phones and contact names were only recorded when they appeared on a fetched page or in a search-result excerpt that quoted a specific page (that page is the `source_url`). Nothing was constructed from a domain pattern. Rows whose email came from a search excerpt rather than a direct fetch say "verify" or "search result" in `notes`. Obfuscated/JavaScript-protected emails (Perth Amboy, Bridgewater, Interfaith Neighbors, JCC MetroWest decode) were either left blank or flagged.
- `languages_served` is only filled when a source stated it (e.g., Bergen County publishes Korean/Spanish brochures; West Windsor lists Cantonese/Mandarin). Entries like "Spanish likely (town) - not stated" are my inference from the town's demographics, not a source claim.

## Directories mined

| Source | What it gave |
|---|---|
| **UnitedHealthcare Community Plan "NJ Senior Centers Directory" (PDF, 11 pp)** — `uhc-gpd-green.uhc.com/.../NJ-Senior-Centers-Directory.pdf` | ~200 senior centers statewide, all 21 counties, with address + phone. The single best starting list; no emails. |
| **NJ DoAS "County Offices on Aging" page** — `nj.gov/humanservices/doas/assistance/county-offices` | All 21 Area Agencies on Aging with address, phone, **email** (20 of 21), website. |
| **Bergen County Senior Activity Centers** — `bergencountynj.gov/?p=1078` | 10 county-run centers, each with a center email and named Center Director. Best email yield of any page. |
| **Essex County Senior Centers** — `wecare.essexcountynj.org/.../essex-county-senior-centers` | 18 Essex centers, address + phone, no emails. |
| **Union County Resource Directory for Older Adults (3/2026 PDF), p.23** | 25 Union senior centers; also Senior Citizens Advocacy orgs (PROCEED, Urban League, AARP). |
| **Morris County Human Services Directory (PDF, pp.27-29) + Midday Friendship Centers 2026 flyer** | 15 municipal senior centers + county nutrition sites and MorrisNutrition email. |
| **Camden County Seniors Directory 2024 (PDF, 126 pp)** | 15 senior centers, congregate sites, SCUCS and AARP NJ emails. |
| **Bergen County Key Services Guide 2024 (Old Tappan-hosted PDF)** | Municipal Bergen centers, Korean Community Center, JFCS, Catholic Charities, Urban League Bergen. |
| **Woodbridge Township 2025 Senior Services Directory (PDF, 127 pp)** | Six Woodbridge centers + Dept. of Senior Services director. |
| **Cumberland County Nutrition Program 2026 (PDF)** | 10 nutrition/senior sites with site-manager names. |
| **NJ DoAS Project Healthy Bones site list (PDF)** | Confirmed Millburn Bauer CC, Livingston, Montclair, West Orange and other sites as senior-program hosts. |
| **Monmouth County departments directory PDF** | Middletown senior center email. |
| Municipal pages fetched directly for emails/contacts | Montclair, South Orange, Hillside, Rahway, Plainfield, Metuchen, South Brunswick, Lawrence, West Windsor, East Windsor, Secaucus, East Newark, North Bergen, Jersey City Senior Affairs, Paterson, Bayonne, Tenafly, Fort Lee, Paramus, Elmwood Park, Washington Twp (Morris), Deptford, Bridgewater, Livingston. |
| Nonprofit pages fetched | JFS MetroWest (older adults page), JFS Central NJ, JFS Middlesex, Catholic Charities Newark adult services, Urban League Hudson, PACCAL, AARP NJ about-us, Summit Area YMCA, Hackensack MLK Senior Center, PROCEED. |

## Row counts by county and type

| County | Rows | With email | senior_center | community_center | aging_office | nonprofit_senior_program |
|---|---|---|---|---|---|---|
| Atlantic | 11 | 1 | 10 | 0 | 1 | 0 |
| Bergen | 63 | 15 | 53 | 0 | 1 | 9 |
| Burlington | 8 | 1 | 7 | 0 | 1 | 0 |
| Camden | 24 | 3 | 19 | 0 | 2 | 3 |
| Cape May | 4 | 1 | 3 | 0 | 1 | 0 |
| Cumberland | 14 | 1 | 13 | 0 | 1 | 0 |
| Essex | 29 | 4 | 17 | 4 | 3 | 5 |
| Gloucester | 9 | 2 | 8 | 0 | 1 | 0 |
| Hudson | 20 | 5 | 12 | 0 | 3 | 5 |
| Hunterdon | 2 | 2 | 1 | 0 | 1 | 0 |
| Mercer | 21 | 5 | 14 | 0 | 2 | 5 |
| Middlesex | 34 | 4 | 29 | 0 | 2 | 3 |
| Monmouth | 17 | 2 | 15 | 0 | 1 | 1 |
| Morris | 24 | 9 | 23 | 0 | 1 | 0 |
| Ocean | 7 | 2 | 6 | 0 | 1 | 0 |
| Passaic | 9 | 1 | 7 | 0 | 1 | 1 |
| Salem | 1 | 1 | 0 | 0 | 1 | 0 |
| Somerset | 9 | 7 | 7 | 1 | 1 | 0 |
| Statewide | 1 | 0 | 0 | 0 | 1 | 0 |
| Sussex | 5 | 1 | 4 | 0 | 1 | 0 |
| Union | 33 | 6 | 19 | 3 | 2 | 9 |
| Warren | 5 | 3 | 4 | 0 | 1 | 0 |
| **Total** | **350** | **76 (21.7%)** | 271 | 8 | 30 | 41 |

(Pass-1 table of 166 rows superseded.)

## Coverage pass 2 (2026-11-10)

Appended 184 rows (append-only; no existing row changed). Every row's `notes` ends with "Added in coverage pass 2 (2026-11-10)."

**What was added, by source (`source_url`):**

| Source | Rows | Notes |
|---|---|---|
| UHC NJ Senior Centers Directory PDF (re-fetched, 222 entries parsed column-by-column) | 77 | Every UHC entry not already a row. Atlantic, Burlington, Hudson, Mercer, Middlesex, Monmouth, Morris, Ocean, Passaic, Warren entries cite UHC. |
| Bergen County Division of Senior Services Key Services Guide 2024 (oldtappan.net PDF, pp.50-51, 55, 24) | 43 | 38 municipal senior centers + AWCA, JCC on the Palisades, YJCC (nonprofit) + Urban League of Bergen County and Catholic Charities Older Adult Services (restored from trim). Excluded building-residents-only sites (Garfield Golden Towers, Belmont Gardens) and Senior Source (retail). |
| Union County Resource Directory for Older Adults (3/2026), p.23-24 | 17 | UHC Union entries re-cited to the newer county directory, plus Fanwood Seniors (mail only) and Urban League of Union County. |
| Camden County Seniors Directory 2024, pp.13-20 | 16 | UHC Camden centers re-cited to county directory, plus county-run **Carol Norcross Senior Social Wellness Center** and congregate sites Katz JCC, Wayne Bryant CC (Lawnside), Lindenwold (address blank — directory repeats the Lawnside address). The three congregate sites share the county meal line 856-374-6325 (also on the existing PRUP row). |
| Essex County "Essex County Senior Centers" page | 9 | Same list as UHC Essex; all 7 trimmed Essex names plus Watsessing Park Club and Branch Brook Visitors Center. |
| Cumberland County Nutrition Program 2026 PDF | 7 | Lawrence Twp, Maurice River, Louise Moore, Charlotte Brago (with site-manager names) + county Sharing Centers Tarkiln Acres (Vineland), High Rise East (Millville), Nanticoke Lenni-Lenape Tribe (Fairton). Holly City, Downe, West Cumberland cite UHC. |
| Morris County Midday Friendship Centers 2026 flyer | 6 | County-run nutrition sites: Butler Firehouse, Cook's Pond (Denville), St. John's Episcopal (Dover), Dean Gallo/Morris Mews (Morris Twp), Rexford S. Tucker Apts (Madison), Pleasant View Village (Rockaway); email = MorrisNutrition@co.morris.nj.us (county inbox printed on the flyer). |
| Gloucester County Nutrition Program page | 5 | County-run lunch sites: Mantua Twp CC, Greenfields VFC (West Deptford), Pfeiffer CC (Williamstown), First Baptist Jericho (Deptford), Second Baptist (Paulsboro). |
| Sussex County Congregate Nutrition page | 2 | Franklin Senior Center (new) and Hopatcong Civic Center (= UHC Hopatcong; county phone used, UHC phone in notes). |
| Cape May County Senior Centers page | 1 | Upper Township Senior Center (county-run; the other two were already rows). |
| Morris County Human Services Directory (senior centers pp.27-29) | 1 | Mt. Olive Senior Center (restored from trim). The 10 trimmed Morris UHC centers cite UHC with a note that the county directory also lists them. |

**De-duplication:** new rows were matched against all 166 existing rows by every phone number in `phone` and `notes`, by normalized name, and by town + street number. Kept despite a phone overlap, with an explanatory note: Bayonne Senior Center and Downtown Senior Center (phones appear in the Bayonne Office on Aging row's notes); Woodbridge's Maple Tree, Hickory, Sycamore and Five Branches centers (listed only in the Woodbridge department row's notes); South Ward Community Center, Trenton (UHC gives it 609-989-3466, which the existing Stubblefield row uses — verify); North Arlington borough Senior Center at 10 Beaver Ave (separate from the county center at 11 York Rd). Not re-added because already rows: Princeton Senior Resource Center, Hopewell Valley, Willingboro (Reva Foster), Passaic (Shimkowitz), North Bergen, Brick, Monroe, the Bergen county centers, Tenafly, Teaneck, Fort Lee, Paramus, MLK Hackensack, KCC, Bergen Family Center/SECIL.

**Types:** directory entries listed as senior centers are `senior_center`, county nutrition sites included (same convention as the existing Wetmore Towers row). Church-, synagogue- or nonprofit-run programs are `nonprofit_senior_program` (15): Grace Van Vorst Episcopal, St. Anthony of Padua Anthonians, St. Paul's Golden Agers, Jewish Center of Princeton, E.C.H.O. Inc., Elizabethport Presbyterian Center, JCC of Central NJ, YM-YWHA Union, Katz JCC, AWCA Teaneck, JCC on the Palisades, YJCC Washington Twp, the two Urban Leagues, Catholic Charities Bergen.

**Trimmed names still not restored:** Morris Twp Senior Club (not in the Morris directory, the 2026 Midday flyer or UHC; Dean Gallo/Morris Mews Midday site added instead), Hawthorne (Passaic County documents return HTTP 403; Hawthorne/Totowa nutrition centers seen only in search snippets, so not recorded), Interfaith Caregivers (Mercer; nonprofit, no page fetched), Elmwood Park Borough office (no page fetched; the county Elmwood Park center is already a row).

**Blocked in pass 2:** passaiccountynj.org (403 to curl and fetch tools), warrencountynj.gov senior-centers page (403), mercercounty.org, aclink.org (Atlantic), Ocean County centers page (404). Morris County PDFs fail from curl (Akamai) but were read through a fetch tool.

## Thin counties and why

_Written for pass 1 (166 rows); county counts below are pass-1 numbers. See the table above for current counts. Salem (1 row: the county office, which is also the only UHC Salem listing) and Hunterdon (2) are still thin._

- **Salem (1), Hunterdon (2), Warren (3), Sussex (3), Cape May (3), Atlantic (3):** these counties run most senior programming through the county office itself (one county senior center or county-run nutrition sites), so there are few distinct municipal centers to list. Warren and Hunterdon rows carry the county inbox as their email because the county operates the centers.
- **Cumberland (4), Gloucester (4), Burlington (4), Ocean (4):** more centers exist (UHC lists 9 for Cumberland, 7 for Burlington) but I kept only 3–4 per county to stay in the row target; the dropped names are in the UHC PDF.
- **Monmouth (6):** the county's own "Listing of Senior Centers" (p.41 of its directory) was not retrievable; rows come from the UHC list. The county says it funds 8 centers.
- **Passaic (8) and Essex (20) have low email yield** (1 and 4 emails). Passaic County's site (CivicPlus) returned HTTP 403 to every fetch, and Essex County publishes no division email at all (director listed as "TBD"). Newark's five ward centers list contact *names* but no emails. For these, `best_channel` is phone.
- **Middlesex (17, 4 emails):** the county senior-centers page (which has a map and per-center detail) is also CivicPlus-blocked; municipal sites mostly publish phone only. Edison, New Brunswick, Piscataway (web form), Perth Amboy (obfuscated) have no recordable email.

## Email coverage and how to raise it

- 70/166 rows (42%) have an email. Best-covered: Bergen (15/20), Somerset (7/9), Warren (3/3), Hunterdon (2/2).
- All 21 county Offices on Aging except Essex have an email; Bergen's outreach page explicitly says speaker requests go to seniors@bergencountynj.gov, and Somerset's county-run wellness centers all route through officeaging@co.somerset.nj.us. For phone-only municipal centers, the county office is the realistic email door.
- Sites that blocked automated fetching (worth opening in a browser): middlesexcountynj.gov senior-centers page, somersetcountynj.gov senior-centers page, passaiccountynj.org nutrition-services page, mercercounty.org nutrition page, hamiltonnj.com directory, cityoforange.org senior services, maplewoodnj.gov contact directory, newarknj.gov/community, lakewoodnj.gov, atlanticcountynj.gov senior-centers page, ulec.org, kccus.org.

## Priority notes for Every Shade

- **Closest to Millburn:** Millburn Bauer Community Center (973-564-7091, PHB site), Livingston Senior/Community Center, Montclair Senior Services (4 named staff with emails incl. Outreach Coordinator), South Orange Baird Center (lherring@southorange.org), JCC MetroWest Margulies Center, Maplewood DeHart CC, Union Township Senior Center, SAGE Eldercare (Summit).
- **Closest to New Brunswick:** New Brunswick Senior Resource Center (phone only), Metuchen (seniorcenter@metuchen.com), South Brunswick (dneglia@sbtnj.net), Franklin Twp (phone only, township won't share email), Somerset County Quail Brook center (county email), AARP NJ state office on George St (NJAARP@aarp.org; outreach director named).
- **Communities of color / immigrant-serving rows:** Bergen United Center (Americas Unidas, Hackensack), Palisades Park center (Korean), Korean Community Center Tenafly, KASCA (Leonia), Indo-American Senior Center and Indo-American Senior Citizens Assn (Jersey City), Indo-American Seniors Org of NJ (Iselin), PACO (Jersey City, Spanish), PACCAL (Filipino, Jersey City), FOCUS Hispanic Center (Newark), La Casa de Don Pedro, PROCEED (Elizabeth), Catholic Charities Hispanic Older Adult Services (Cranford), PRUP (Camden), Urban Leagues of Essex/Hudson, Hackensack MLK Senior Center, Newark ward centers, Paterson, East Orange, Irvington, Plainfield, Trenton. **Haitian:** no Haitian-specific senior program with published contact info was found; leads are Lanbi Center (Orange), Jefferson Park Ministries (Elizabeth), and parish Haitian ministries (St. Leo Irvington; Holy Spirit / OLHC East Orange; OL Mt Carmel Orange) — not added as rows because no contact details were verified. **NAACP:** only the NJ State Conference email (president@njnaacp.org) surfaced; no branch contacts verified, so no rows.

## Rows dropped in the trim (all are in the UHC PDF or county directories if needed)

Essex: Belleville Senior Citizens Clubs; Fairfield Golden Age Club; Jewish Senior Citizens of Irvington; Weequahic Park CC; Branch Brook Senior Club; Nutley Senior Center; Newark South Ward Senior Center. Union: Casano CC; Clark Rec; Liberty Square; O'Donnell-Dempsey; Elizabethport Presbyterian; Kenilworth; New Providence; Springfield Chisholm; Buckle Center (Winfield); Mountainside; Garwood; JCC Central NJ; Westfield CC Assn; Scotch Plains Rec; Urban League of Union County. Morris: Denville; East Hanover; Jefferson; Montville; Mt. Olive; Pequannock; Rockaway; Roxbury; Florham Park; Madison; Chathams; Morris Twp Senior Club. Middlesex: Dunellen; Middlesex Boro; Milltown; South Amboy; South River; Spotswood; Plainsboro; Carteret Deverin CC; Five Branches; Highland Park; Sayreville; South Plainfield. Hudson: Grace Van Vorst; Harrison; Weehawken; Bayonne Senior Center; Kearny. Mercer: Sam Naples; Reading; South Ward CC; Robbinsville; Ewing; Interfaith Caregivers. Passaic: Ringwood; Hawthorne. Monmouth: Freehold Twp; Neptune. Camden: Collingswood. Atlantic: Hammonton; Egg Harbor Twp. Cumberland: Holly City. Cape May: Upper Twp. Sussex: Hopatcong. Ocean: LBI. Burlington: Bordentown. Bergen: Urban League Bergen; Catholic Charities Bergen; Fair Lawn; Elmwood Park Borough office.
