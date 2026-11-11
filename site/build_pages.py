#!/usr/bin/env python3
"""Build Every Shade subpages from the homepage's design system.

Run: python3 -I site/build_pages.py   (from the repo root)
Writes: about/, impact/ (from site/talks.csv), faq/, privacy/, get-involved/, press/, materials/, es/, and care/ (if site/care.csv exists) index.html files.
Edit page content in the PAGES dict below; styles come from index.html so every page stays on-brand.
"""
import re, csv, html, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
home = (ROOT / "index.html").read_text()
FONTS = re.search(r'(<link rel="preconnect".*?display=swap">)', home, re.S).group(1)
CSS = re.findall(r"<style>(.*?)</style>", home, re.S)[1]
LOGO = re.search(r'(<svg width="40".*?</svg>)', home, re.S).group(1)

EXTRA_CSS = """
.page-hero .wrap{padding-block:56px 40px;display:flex;flex-direction:column;gap:16px}
.page-hero p{font-size:1.15rem;color:var(--muted)}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.card{padding:22px 24px;border:1px solid var(--rule);border-radius:14px;background:var(--ground);display:flex;flex-direction:column;gap:10px;min-width:0}
.card h3{font-size:1.2rem}
.card ul{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:6px}
.card .btn{margin-top:auto}
.lang-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;list-style:none;padding:0;margin:0}
.lang-list a{display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:56px;padding:12px 18px;border:1px solid var(--rule);border-radius:12px;text-decoration:none;color:var(--ink);font-weight:700;background:var(--ground)}
.lang-list a:hover{border-color:var(--accent);color:var(--accent)}
.lang-list small{font-weight:400;color:var(--muted)}
.facts-list{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:8px}
.boiler{padding:18px 20px;border-left:0;background:var(--band);border-radius:12px}
table.dir{width:100%;border-collapse:collapse;font-size:1rem}
table.dir th,table.dir td{text-align:left;padding:10px 8px;border-bottom:1px solid var(--rule);vertical-align:top}
table.dir th{font-family:var(--display);font-size:.9rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.filters{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:18px}
.filters select,.filters input{min-height:48px;font:inherit;padding:0 12px;border:1px solid var(--rule);border-radius:10px;background:var(--ground);color:var(--ink)}
.dir-wrap{overflow-x:auto}
table.dir td:nth-child(4) a[href^='tel']{white-space:nowrap}
@media (max-width:820px){.grid2,.grid3{grid-template-columns:minmax(0,1fr)} table.dir thead{display:none} table.dir tr{display:block;border-bottom:1px solid var(--rule);padding:10px 0} table.dir td{display:block;border:0;padding:3px 0}}
"""

NAV = {
    "en": [("../", "Home"), ("../check/", "Self-check"), ("../care/", "Find care"), ("../materials/", "Handouts"), ("../get-involved/", "Get involved"), ("../es/", "Español")],
    "es": [("../", "English"), ("../check/", "Autoexamen"), ("../care/", "Dónde ir"), ("../materials/", "Folletos"), ("#contacto", "Contacto")],
}
FOOT = {
    "en": "Every Shade provides general health education only. Nothing on this site or in our talks is medical advice or a diagnosis. Our members are students, not medical professionals. If a spot is new, changing, or bleeding, please see a doctor.",
    "es": "Every Shade ofrece solo educación general sobre la salud. Nada en este sitio ni en nuestras charlas es consejo médico ni un diagnóstico. Nuestros miembros son estudiantes, no profesionales de la salud. Si una mancha es nueva, cambia o sangra, vaya al médico.",
}


FOOTLINKS = " · ".join(f'<a href="../{h}/">{t}</a>' for h, t in [("about", "About"), ("impact", "Impact"), ("faq", "FAQ"), ("privacy", "Privacy"), ("press", "Press kit"), ("toolkit", "Start a chapter")])


def page(lang, title, desc, body, extra_head=""):
    nav = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[lang])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
{FONTS}
<style>{CSS}{EXTRA_CSS}</style>
{extra_head}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="../" aria-label="Every Shade home">{LOGO}<span>every shade</span></a>
<nav aria-label="Main"><ul>{nav}</ul></nav>
</div></header>
<main id="top">
{body}
</main>
<div class="strip" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>
<footer><div class="wrap"><p>{FOOT[lang]}</p><p>{FOOTLINKS}</p><p>© 2026 Every Shade · New Brunswick, New Jersey · everyshadescreening@gmail.com · (915) 400-7072</p></div></footer>
</body>
</html>
"""


def mail(subject, label, cls="btn"):
    from urllib.parse import quote
    return f'<a class="{cls}" href="mailto:everyshadescreening@gmail.com?subject={quote(subject)}">{label}</a>'


STRIP = '<div class="strip" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>'

GET_INVOLVED = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Get involved</span>
<h1>Help every New Jerseyan know what to look for.</h1>
<p>Every Shade runs on students, community hosts, and clinicians who give a few hours. Pick the way that fits you.</p>
</div></div>
{STRIP}
<section class="tint"><div class="wrap">
<div class="grid2">
<div class="card"><h3>Host a free talk</h3><p>For senior centers, libraries, faith communities, and community groups anywhere in New Jersey.</p>
<ul><li>45 minutes, in person or on Zoom</li><li>Large-print handout, also in Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean</li><li>A short anonymous quiz so you can see what members learned</li><li>Free, and we handle the setup</li></ul>
{mail("Talk request: [organization name]", "Request a talk")}</div>
<div class="card"><h3>Volunteer as a student</h3><p>Rutgers students in any major. Training provided; most roles take 2 to 4 hours a month.</p>
<ul><li><b>Speakers:</b> deliver talks after training and a practice run</li><li><b>Language team:</b> co-present in Spanish, Hindi, Urdu, Gujarati, Haitian Creole, Korean, or another language</li><li><b>Outreach:</b> book talks with centers in your county</li><li><b>Measurement:</b> score quizzes and track outcomes</li></ul>
{mail("Volunteer: [your name, school, role]", "Join the team")}</div>
<div class="card"><h3>Clinicians and advisors</h3><p>Dermatologists, residents, nurses, and public health faculty.</p>
<ul><li>Review our content once a year</li><li>Join a talk for the questions section</li><li>Partner on a free skin-check day after a talk</li></ul>
{mail("Clinician or advisor: [your name]", "Partner with us")}</div>
<div class="card"><h3>Start a chapter</h3><p>Students at other schools can launch "Every Shade at [School]" with our free toolkit: the talk, the handouts, the quiz, and a step-by-step plan.</p>
<a class="btn" href="../toolkit/">Read the chapter toolkit</a></div>
</div>
</div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Our standards</span><h2>What every volunteer agrees to</h2></div>
<ul class="facts-list"><li>We teach; we never diagnose. If someone shows us a spot, we help them find a clinician.</li><li>Every medical statement comes from the American Academy of Dermatology, the Skin Cancer Foundation, the CDC, or peer-reviewed research, and is reviewed by a physician.</li><li>We say at the start of every talk that we are students, not medical professionals.</li><li>Quizzes are anonymous. We never collect health information.</li></ul>
</div></section>
"""

PRESS = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Press kit</span>
<h1>Every Shade, in brief.</h1>
<p>For reporters, partners, and anyone writing about us. Press contact: everyshadescreening@gmail.com · (915) 400-7072.</p>
</div></div>
{STRIP}
<section class="tint"><div class="wrap">
<div class="section-head"><span class="eyebrow">About</span><h2>One-paragraph description</h2></div>
<p class="boiler">Every Shade is a student organization at Rutgers University–New Brunswick that gives free talks to New Jersey senior centers, libraries, and faith communities on how skin cancer looks on every skin tone. Talks teach the places melanoma is often missed on darker skin (the palms, the soles of the feet, and under the nails), a simple monthly self-check, and where to get a spot looked at for free or at low cost. Materials are physician-reviewed and available in English, Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean, and every talk is measured with an anonymous before-and-after quiz.</p>
</div></section>
<section><div class="wrap grid2">
<div class="card"><h3>Fast facts</h3><ul>
<li>Founded 2026 at Rutgers University–New Brunswick</li>
<li>Free 45-minute talks, in person or on Zoom</li>
<li>Materials in 7 languages</li>
<li>Free monthly self-check web tool; photos never leave the user's phone</li>
<li>Chapter toolkit for students at other schools</li>
<li>First public talk: November 20, 2026</li></ul></div>
<div class="card"><h3>Why it matters</h3><ul>
<li>15% of images in common medical study resources show skin of color (Perlman et al., 2021).</li>
<li>Five-year melanoma survival is 66% for Black patients and 90% for white patients, largely because of later diagnosis (Culp and Lunsford, CDC, 2019).</li>
<li>Among melanomas of a known type in Black patients, 46% were on the palms, soles, or under the nails, compared with 2% in white patients (same source).</li></ul></div>
<div class="card"><h3>Co-founder</h3><p><b>Zain Jaffar</b>, Honors College, Rutgers University–New Brunswick (Cell Biology and Neuroscience, Data Science minor). Dermatology and Mohs surgery medical assistant; melanoma research with Mass General Brigham and Harvard Medical School; teledermatology research with Stanford Dermatology.</p></div>
<div class="card"><h3>Logo and colors</h3><p>The fanned-swatch mark shows five skin tones. Use it on a white or light background with clear space around it.</p>
<p><a href="../site/every-shade-logo.svg" download>Download the logo (SVG)</a> · <a href="every-shade-fact-sheet.pdf">One-page fact sheet (PDF)</a></p>
<p class="note">Colors: ink #2B1A12 · accent #8E5632 · tones #EFCBB0 #DDAA84 #C28559 #9C623A #6B4127 #3D2416</p></div>
</div></section>
"""

LANGS = [("English", "English", "talk-kit/handout/handout-en.pdf"), ("Español", "Spanish", "languages/handout-es.pdf"),
         ("हिन्दी", "Hindi", "languages/handout-hi.pdf"), ("اردو", "Urdu", "languages/handout-ur.pdf"),
         ("ગુજરાતી", "Gujarati", "languages/handout-gu.pdf"), ("Kreyòl ayisyen", "Haitian Creole", "languages/handout-ht.pdf"),
         ("한국어", "Korean", "languages/handout-ko.pdf")]
lang_items = "".join(f'<li><a href="../{p}" lang="{ {"Spanish":"es","Hindi":"hi","Urdu":"ur","Gujarati":"gu","Haitian Creole":"ht","Korean":"ko"}.get(e,"en") }">{n} <small>{e} · PDF</small></a></li>' for n, e, p in LANGS)
MATERIALS = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Free handouts</span>
<h1>Check your skin once a month. In your language.</h1>
<p>Our two-page, large-print guide: how to do a 10-minute skin check, what warning signs look like on light, medium, and dark skin, and where to go in New Jersey. Each translation was reviewed by a native speaker. Print at 100% on letter paper.</p>
</div></div>
{STRIP}
<section class="tint"><div class="wrap">
<ul class="lang-list">{lang_items}</ul>
<p class="note" style="margin-top:18px">Centers are welcome to print and share these for free. Please do not edit them. Need another language? {mail("Handout language request", "Ask us", "")}.</p>
</div></section>
<section><div class="wrap grid2">
<div class="card"><h3>Prefer your phone?</h3><p>Our free monthly self-check guide walks you through each step and reminds you every month. Nothing you enter leaves your phone.</p><a class="btn" href="../check/">Open the self-check</a></div>
<div class="card"><h3>Need a place to get a spot checked?</h3><p>Free and low-cost options in every New Jersey county, including community health centers that see everyone.</p><a class="btn" href="../care/">Find care near you</a></div>
</div></section>
"""

ES = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Salud de la piel para todos los tonos · Nueva Jersey</span>
<h1>El cáncer de piel no se ve igual en todos.</h1>
<p>Every Shade es un grupo de estudiantes de Rutgers University–New Brunswick. Damos charlas gratis en centros para mayores, bibliotecas y comunidades sobre cómo reconocer el cáncer de piel en todos los tonos de piel y dónde revisarse.</p>
<a class="btn" href="#contacto">Pida una charla gratis</a>
</div></div>
{STRIP}
<section class="tint"><div class="wrap">
<div class="section-head"><span class="eyebrow">Por qué empezamos</span><h2>La mayoría de las fotos con las que aprenden los médicos muestran piel clara.</h2>
<p>En la piel morena y negra, el melanoma (el cáncer de piel más peligroso) muchas veces aparece en las palmas, las plantas de los pies, entre los dedos de los pies y debajo de las uñas: lugares que reciben poco sol y que casi nadie revisa.</p></div>
<div class="facts">
<div class="fact"><b>15%</b><p>de las imágenes en materiales comunes de estudio de medicina muestran piel de color.</p></div>
<div class="fact"><b>66% vs 90%</b><p>supervivencia a cinco años del melanoma en pacientes negros frente a pacientes blancos, sobre todo porque se encuentra más tarde.</p></div>
<div class="fact"><b>46%</b><p>de los melanomas de tipo conocido en pacientes negros estaban en las palmas, las plantas o debajo de las uñas (2% en pacientes blancos).</p></div>
</div>
<p class="cite">Fuentes: Perlman et al., Int J Womens Dermatol, 2021. Culp y Lunsford, Preventing Chronic Disease (CDC), 2019.</p>
</div></section>
<section><div class="wrap">
<div class="section-head"><span class="eyebrow">Nuestra charla</span><h2>Qué aprenderá</h2></div>
<div class="grid2">
<ul class="facts-list"><li>Qué es el melanoma y otros cánceres de piel</li><li>Qué aumenta el riesgo: quemaduras de sol, años al sol, antecedentes familiares y la edad</li><li>Cómo se ven las señales de alarma en piel clara, media y oscura</li><li>Los lugares que la gente no revisa: palmas, plantas, entre los dedos y debajo de las uñas</li><li>Cómo revisar su piel en casa, paso a paso</li><li>Cuándo ir al médico y adónde ir si no tiene seguro</li></ul>
<div class="card"><h3>Gratis, en persona o por Zoom</h3><p>Dura 45 minutos, con tiempo para preguntas. Le damos un folleto en letra grande en español.</p><a class="btn" href="../languages/handout-es.pdf">Descargar el folleto en español</a></div>
</div></div></section>
<section id="contacto" class="tint"><div class="wrap book">
<span class="eyebrow">Pida una charla</span>
<h2>Lleve una charla gratis a su centro o comunidad.</h2>
<p>Escríbanos con el nombre de su organización y algunas fechas. Nosotros nos encargamos del resto.</p>
<div class="mail"><code>everyshadescreening@gmail.com</code></div>
<p class="note">Teléfono: (915) 400-7072. Esta página fue traducida del inglés y está en revisión.</p>
</div></section>
"""

CARE_INTRO = """
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Find care</span>
<h1>Free and low-cost places to get a spot looked at.</h1>
<p>Every New Jersey county has community health centers that see everyone, with or without insurance, and charge by what you can pay (a "sliding fee"). Call ahead, say you have a skin spot you want checked, and ask about the sliding fee.</p>
</div></div>
"""


def care_page(rows, verified):
    counties = sorted({r["county"] for r in rows if r["county"]})
    opts = "".join(f'<option value="{html.escape(c)}">{html.escape(c)}</option>' for c in counties)
    trs = []
    for r in rows:
        web = f'<a href="{html.escape(r["website"])}" rel="noopener">Website</a>' if r.get("website", "").startswith("http") else ""
        phone = html.escape(r.get("phone", ""))
        tel = re.sub(r"[^\d+]", "", r.get("phone", ""))[:15]
        phone_html = f'<a href="tel:{tel}">{phone}</a>' if tel else ""
        tags = []
        sf = (r.get("sliding_fee") or "").lower()
        if sf.startswith("yes"): tags.append("Sliding fee")
        elif "free" in sf: tags.append("Free")
        if r.get("accepts_uninsured") == "yes": tags.append("Sees uninsured")
        if (r.get("dermatology_onsite") or "").startswith("yes"): tags.append("Dermatology on site")
        if r.get("languages") and r["languages"].lower() not in ("not listed", "unknown"): tags.append(html.escape(r["languages"]))
        trs.append(f'<tr data-county="{html.escape(r["county"])}"><td>{html.escape(r["county"])}</td><td><b>{html.escape(r["name"])}</b><br><span class="note">{html.escape(r.get("type", ""))}{(" · " + html.escape(r.get("notes", ""))) if r["county"] == "Statewide" else ""}</span></td>'
                   f'<td>{html.escape(r.get("address", ""))}{", " if r.get("address") and r.get("town") else ""}{html.escape(r.get("town", ""))}</td><td>{phone_html}<br>{web}</td><td>{" · ".join(tags)}</td></tr>')
    body = CARE_INTRO + STRIP + f"""
<section class="tint"><div class="wrap">
<div class="filters"><label for="county"><b>Your county</b></label><select id="county"><option value="">All counties</option>{opts}</select>
<input id="q" type="search" placeholder="Search by town or name" aria-label="Search by town or name"></div>
<p class="note" id="count" aria-live="polite"></p>
<div class="dir-wrap"><table class="dir"><thead><tr><th>County</th><th>Place</th><th>Address</th><th>Contact</th><th>Notes</th></tr></thead><tbody id="rows">{''.join(trs)}</tbody></table></div>
<p class="note" style="margin-top:16px">List last checked {verified}. Details change; please call before you go. Also: the American Academy of Dermatology lists free skin checks at <a href="https://www.aad.org/public/public-health/skin-cancer-screenings">aad.org/spotme</a>, and HRSA's <a href="https://findahealthcenter.hrsa.gov/">Find a Health Center</a> shows the nearest community health center. Something wrong or missing? <a href="mailto:everyshadescreening@gmail.com?subject=Care%20list%20update">Tell us</a>.</p>
</div></section>
<script>
(function(){{var sel=document.getElementById('county'),q=document.getElementById('q'),rows=[].slice.call(document.querySelectorAll('#rows tr')),cnt=document.getElementById('count');
function f(){{var c=sel.value,s=q.value.toLowerCase(),n=0;rows.forEach(function(r){{var ok=(!c||r.getAttribute('data-county')===c)&&(!s||r.textContent.toLowerCase().indexOf(s)>-1);r.hidden=!ok;if(ok)n++;}});cnt.textContent=n+' places shown';}}
sel.addEventListener('change',f);q.addEventListener('input',f);f();}})();
</script>"""
    return page("en", "Find Free Skin Care in NJ | Every Shade", "Free and low-cost places in every New Jersey county to get a skin spot looked at, including community health centers with sliding fees.", body)


ABOUT = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">About us</span>
<h1>Skin cancer education that looks like New Jersey.</h1>
<p>Every Shade is a student-run group at Rutgers University–New Brunswick. We give free talks to older adults on how skin cancer looks on every skin tone, and we help people find free or low-cost care.</p>
</div></div>
{STRIP}
<section class="tint"><div class="wrap grid2">
<div class="card"><h3>Our mission</h3><p>Help every New Jerseyan, whatever their skin tone or language, recognize the early signs of skin cancer, check their own skin once a month, and know where to go when a spot worries them.</p></div>
<div class="card"><h3>The problem we work on</h3><p>Melanoma is found later, on average, in people with darker skin. Five-year survival is 66% for Black patients and 90% for white patients (Culp and Lunsford, CDC, 2019). Most teaching pictures show light skin: about 15% of images in common medical study resources show skin of color (Perlman et al., 2021). And on darker skin, melanoma often appears where people do not look: the palms, the soles of the feet, and under the nails.</p></div>
</div></section>
<section><div class="wrap">
<div class="section-head"><span class="eyebrow">What we do</span><h2>Four programs, one goal</h2></div>
<div class="grid2">
<div class="card"><h3>Free talks</h3><p>45 minutes, in person or on Zoom, for senior centers, libraries, faith communities, senior housing, and community groups. Every talk includes a large-print handout and an anonymous before-and-after quiz.</p><a class="btn" href="../get-involved/">Request a talk</a></div>
<div class="card"><h3>Seven languages</h3><p>Handouts in English, Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean, each reviewed by a native speaker. Talks in those languages are being prepared with student co-presenters.</p><a class="btn" href="../materials/">Get the handouts</a></div>
<div class="card"><h3>Monthly self-check tool</h3><p>A free web app that walks you through a skin check, reminds you monthly, and keeps photos only on your own phone.</p><a class="btn" href="../check/">Open the tool</a></div>
<div class="card"><h3>Finding care</h3><p>A list of free and sliding-fee clinics in all 21 New Jersey counties, checked by our team, so no one leaves a talk without a next step.</p><a class="btn" href="../care/">Find care near you</a></div>
</div></div></section>
<section class="tint"><div class="wrap">
<div class="section-head"><span class="eyebrow">How we work</span><h2>Our standards</h2></div>
<ul class="facts-list">
<li><b>We teach; we never diagnose.</b> Our members are students. If someone shows us a spot, we help them find a clinician.</li>
<li><b>Physician-reviewed content.</b> Every medical statement comes from the American Academy of Dermatology, the Skin Cancer Foundation, the CDC, or peer-reviewed research, and the talk and handout are reviewed by a physician before use and again each year.</li>
<li><b>Native-speaker review.</b> No translated material is handed out until a native speaker has checked it.</li>
<li><b>Measured, and published.</b> Every talk is measured with the same anonymous quiz, and we post the results on our <a href="../impact/">Impact page</a>, good or bad.</li>
<li><b>Privacy first.</b> Quizzes are anonymous, we never photograph anyone's skin, and our self-check tool stores nothing on any server. See our <a href="../privacy/">privacy page</a>.</li>
<li><b>No product endorsements.</b> We do not promote any brand, product, or clinic in our talks.</li>
</ul></div></section>
<section><div class="wrap grid2">
<div class="card"><h3>Who we are</h3><p>Every Shade was co-founded in 2026 by <b>Zain Jaffar</b>, an Honors College student at Rutgers University–New Brunswick (Cell Biology and Neuroscience, Data Science minor) who works as a dermatology and Mohs surgery medical assistant and does melanoma and teledermatology research. Student speakers complete a training and certification program before giving talks.</p><a class="btn" href="../get-involved/">Join the team</a></div>
<div class="card"><h3>Start Every Shade at your school</h3><p>Everything we use is free for students at other schools: the talk, the handouts, the quiz, and a step-by-step plan for starting a chapter.</p><a class="btn" href="../toolkit/">Read the chapter toolkit</a></div>
</div></section>
"""

FAQ_ITEMS = [
    ("Is the talk really free?", "Yes. Talks, handouts, and the self-check tool are free. We never sell anything or collect payment."),
    ("Who gives the talks?", "Trained Rutgers students. We say at the start of every talk that we are students, not doctors. Our content is reviewed by a physician."),
    ("Will you look at my spot?", "No. Students cannot examine or diagnose skin. If you are worried about a spot, we will help you find a clinician, including free and sliding-fee clinics on our <a href='../care/'>care list</a>."),
    ("How long is a talk, and what do you need from us?", "About 45 minutes including questions. For in-person talks we need a room and a screen or wall to project on; for Zoom, a TV or projector in the room, or a link sent to members. We bring or email the large-print handouts."),
    ("Can the talk be in another language?", "Handouts are ready in Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean. For a talk in one of these languages, tell us when you book and we will pair our speaker with a student who speaks it."),
    ("What is the quiz, and is it anonymous?", "A short multiple-choice quiz before and after the talk, so we can see whether the talk works. No names, no health questions. Results are only reported as group averages."),
    ("Is the self-check tool safe to use?", "Yes. Photos and notes stay on your own phone or computer. There are no accounts and nothing is uploaded. It is a guide, not a diagnosis."),
    ("Who can book a talk?", "Any New Jersey senior center, library, faith community, senior housing building, community center, civic club, or cultural association."),
    ("I am a student. How do I join?", "See <a href='../get-involved/'>Get involved</a>. Speakers complete training and a practice run before giving a talk."),
    ("Who pays for this?", "Every Shade is volunteer-run. Our costs are mostly printing. If your organization would like to support printing or donate sunscreen for attendees, email us."),
]
FAQ = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Questions</span>
<h1>Frequently asked questions</h1>
<p>Something not answered here? Email everyshadescreening@gmail.com or call (915) 400-7072.</p>
</div></div>
{STRIP}
<section class="tint"><div class="wrap"><div class="grid2">
""" + "".join(f'<div class="card"><h3>{q}</h3><p>{a}</p></div>' for q, a in FAQ_ITEMS) + """
</div></div></section>
""" + '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in FAQ_ITEMS]}) + "</script>"

PRIVACY = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Privacy</span>
<h1>What we collect, and what we never collect.</h1>
<p>Short version: almost nothing. Last updated November 2026.</p>
</div></div>
{STRIP}
<section class="tint"><div class="wrap grid2">
<div class="card"><h3>This website</h3><ul><li>No accounts, no cookies, no ads, and no analytics or tracking scripts.</li><li>Pages load fonts from Google Fonts, so Google receives your browser's standard request for the font files (<a href="https://policies.google.com/privacy">Google's privacy policy</a>).</li><li>The site is hosted on GitHub Pages, which keeps standard server logs (<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a>).</li></ul></div>
<div class="card"><h3>The self-check tool</h3><ul><li>Everything you enter, including photos, is stored only in your own browser on your own device.</li><li>Nothing is uploaded to us or anyone else. We cannot see it.</li><li>You can export or delete all of it under "Reminders &amp; data" in the tool. Clearing your browser data also deletes it.</li></ul></div>
<div class="card"><h3>Talks and quizzes</h3><ul><li>Quizzes are anonymous: no names, no contact details, no health information.</li><li>We report only group results (for example, average scores before and after a talk).</li><li>We never photograph anyone's skin. We only take photos of a room with the host's permission, and anyone can ask not to be in them.</li></ul></div>
<div class="card"><h3>Email and phone</h3><ul><li>If you email or call us, we use your details only to reply and to arrange talks.</li><li>We never sell or share contact details, and we never add anyone to a mailing list without asking.</li><li>To have your details deleted, email everyshadescreening@gmail.com.</li></ul></div>
</div></section>
"""


def impact_page():
    path = ROOT / "site" / "talks.csv"
    talks = [r for r in csv.DictReader(path.open(encoding="utf-8"))] if path.exists() else []
    langs_ready = 7
    if not talks:
        stats = f"""<div class="grid3">
<div class="card"><h3>November 20, 2026</h3><p>Our first public talk, on Zoom. Its results will be posted here within a week.</p></div>
<div class="card"><h3>{langs_ready} languages</h3><p>Handouts ready in English, Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean.</p></div>
<div class="card"><h3>21 counties</h3><p>Free and sliding-fee care listed in every New Jersey county on our <a href="../care/">care list</a>.</p></div></div>"""
        table = ""
    else:
        num = lambda k: [float(r[k]) for r in talks if r.get(k)]
        att = int(sum(num("attendees")))
        nb, na = sum(num("n_before")), sum(num("n_after"))
        wavg = lambda k, w: round(sum(float(r[k]) * float(r[w]) for r in talks if r.get(k) and r.get(w)) / max(1, sum(float(r[w]) for r in talks if r.get(k) and r.get(w))))
        before, after = wavg("before_pct", "n_before"), wavg("after_pct", "n_after")
        counties = len({r["county"] for r in talks if r.get("county") and r["county"] != "Statewide"})
        langs = len({r["language"] for r in talks if r.get("language")})
        stats = f"""<div class="grid3">
<div class="card"><h3>{len(talks)} talk{'s' if len(talks) != 1 else ''}</h3><p>{att} people attended{f', across {counties} count' + ('ies' if counties != 1 else 'y') if counties else ''}, in {langs} language{'s' if langs != 1 else ''}.</p></div>
<div class="card"><h3>{before}% to {after}%</h3><p>Average quiz score before and after our talks ({int(nb)} quizzes before, {int(na)} after).</p></div>
<div class="card"><h3>{langs_ready} languages</h3><p>Handouts ready in English, Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean.</p></div></div>"""
        trs = "".join(f"<tr><td>{html.escape(r['date'])}</td><td>{html.escape(r.get('venue_type') or r.get('venue', ''))}</td><td>{html.escape(r.get('county', ''))}</td><td>{html.escape(r.get('language', ''))}</td><td>{html.escape(r.get('attendees', ''))}</td><td>{html.escape(r['before_pct'])}% → {html.escape(r['after_pct'])}%</td><td>{html.escape(r.get('plan_check_pct') or '')}{'%' if r.get('plan_check_pct') else ''}</td></tr>" for r in reversed(talks))
        table = f"""<div class="section-head" style="margin-top:32px"><h2>Every talk</h2></div>
<div class="dir-wrap"><table class="dir"><thead><tr><th>Date</th><th>Where</th><th>County</th><th>Language</th><th>Attended</th><th>Quiz score</th><th>Plan a self-check</th></tr></thead><tbody>{trs}</tbody></table></div>"""
    body = f"""
<div class="page-hero"><div class="wrap">
<span class="eyebrow">Impact</span>
<h1>We measure every talk, and publish the results.</h1>
<p>Each talk uses the same anonymous ten-question quiz before and after, plus two questions on confidence and plans to do a skin check. We post every result here, including the ones that show what we need to teach better.</p>
</div></div>
{STRIP}
<section class="tint"><div class="wrap">{stats}{table}</div></section>
<section><div class="wrap">
<div class="section-head"><span class="eyebrow">Method</span><h2>How we count</h2></div>
<ul class="facts-list"><li>Quizzes are anonymous, so before and after answers are compared as groups, not matched person by person.</li><li>"Attended" is the host's or Zoom's head count; not everyone answers both quizzes.</li><li>Thirty days after each talk we ask hosts and registered attendees whether people did a skin check, and we will report that too.</li><li>The quiz and our analysis code are public in our <a href="https://github.com/ZainJaffar06/everyshade">GitHub repository</a>.</li></ul>
</div></section>"""
    return page("en", "Impact | Every Shade", "Every Shade publishes the results of every talk: attendance and anonymous before-and-after quiz scores.", body)



def fact_sheet():
    """One-page printable fact sheet (press/fact-sheet.html -> press/every-shade-fact-sheet.pdf)."""
    path = ROOT / "site" / "talks.csv"
    talks = list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []
    if talks:
        att = int(sum(float(r["attendees"]) for r in talks if r.get("attendees")))
        nb = sum(float(r["n_before"]) for r in talks); na = sum(float(r["n_after"]) for r in talks)
        b = round(sum(float(r["before_pct"]) * float(r["n_before"]) for r in talks) / nb)
        a = round(sum(float(r["after_pct"]) * float(r["n_after"]) for r in talks) / na)
        proof = f"<b>{len(talks)} talk{'s' if len(talks) != 1 else ''}, {att} attendees.</b> Average quiz score rose from {b}% before to {a}% after (anonymous quizzes, {int(nb)} before and {int(na)} after). Every result is public at zainjaffar06.github.io/everyshade/impact."
    else:
        proof = "<b>First public talk: November 20, 2026.</b> Every talk is measured with the same anonymous before-and-after quiz, and every result is published on our Impact page."
    logo = LOGO.replace('width="40"', 'width="34"')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Every Shade fact sheet</title>{FONTS}
<style>
@page{{size:letter;margin:0.45in 0.55in}}
:root{{--ink:#2B1A12;--muted:#6B5B50;--accent:#8E5632;--band:#F7F1EC;--rule:#E5D9CF;--t1:#EFCBB0;--t2:#DDAA84;--t3:#C28559;--t4:#9C623A;--t5:#6B4127;--rivet:#fff}}
*{{box-sizing:border-box}} html,body{{margin:0;background:#fff;color:var(--ink);font-family:'Atkinson Hyperlegible',Arial,sans-serif;font-size:10.6pt;line-height:1.38}}
h1,h2,h3{{font-family:Manrope,Arial,sans-serif;margin:0}} h1{{font-size:21pt;line-height:1.12;font-weight:800}} h2{{font-size:11.5pt;font-weight:800;margin-bottom:3pt}}
p{{margin:0}} ul{{margin:0;padding-left:1.05em}} li{{margin:1.5pt 0}}
.top{{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid var(--ink);padding-bottom:7pt}}
.brand{{display:flex;align-items:center;gap:7pt;font-family:Manrope;font-weight:800;font-size:14pt}}
.eyebrow{{font-family:Manrope;font-weight:600;font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}}
.strip{{display:flex;height:6pt;margin:10pt 0}} .strip i{{flex:1}} .strip i:nth-child(1){{background:#EFCBB0}}.strip i:nth-child(2){{background:#DDAA84}}.strip i:nth-child(3){{background:#C28559}}.strip i:nth-child(4){{background:#9C623A}}.strip i:nth-child(5){{background:#6B4127}}.strip i:nth-child(6){{background:#3D2416}}
.lead{{font-size:12pt;margin:6pt 0 10pt}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:9pt;margin-bottom:11pt}}
.stat{{background:var(--band);border-radius:8pt;padding:8pt 10pt}} .stat b{{display:block;font-family:Manrope;font-size:19pt;font-weight:800;color:var(--accent);line-height:1.1}} .stat span{{font-size:9pt;color:var(--muted)}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:12pt 20pt}}
.box{{border:1px solid var(--rule);border-radius:8pt;padding:8pt 10pt}}
.proof{{background:var(--ink);color:#fff;border-radius:8pt;padding:9pt 12pt;margin:11pt 0}}
.foot{{border-top:1px solid var(--rule);padding-top:7pt;margin-top:10pt;font-size:9pt;color:var(--muted);display:flex;justify-content:space-between;gap:10pt}}
.src{{font-size:7.6pt;color:var(--muted);margin-top:8pt}}
</style></head><body>
<div class="top"><div class="brand">{logo}<span>every shade</span></div><div class="eyebrow">Fact sheet · {__import__("datetime").date.today().strftime("%B %Y")}</div></div>
<div class="strip"><i></i><i></i><i></i><i></i><i></i><i></i></div>
<h1>Free skin cancer education for New Jersey seniors, on every skin tone.</h1>
<p class="lead">Every Shade is a student-run group at Rutgers University–New Brunswick. We teach older adults where skin cancer hides on darker skin, how to check their own skin once a month, and where to get a spot looked at for free.</p>
<div class="stats">
<div class="stat"><b>66% vs 90%</b><span>five-year melanoma survival, Black vs white patients, largely because of later diagnosis (1)</span></div>
<div class="stat"><b>46% vs 2%</b><span>of melanomas of a known type on the palms, soles, or under the nails, Black vs white patients (1)</span></div>
<div class="stat"><b>15%</b><span>of images in common medical study resources show skin of color (2)</span></div>
</div>
<div class="cols">
<div class="box"><h2>What we do</h2><ul>
<li><b>Free 45-minute talks</b> for senior centers, libraries, faith communities, senior housing, and community groups, in person or on Zoom</li>
<li><b>Large-print handout in 7 languages:</b> English, Spanish, Hindi, Urdu, Gujarati, Haitian Creole, Korean (native-speaker reviewed)</li>
<li><b>Free monthly self-check web app;</b> photos never leave the user's phone</li>
<li><b>Care finder:</b> free and sliding-fee clinics in all 21 NJ counties</li>
<li><b>Chapter toolkit</b> for students at other schools</li></ul></div>
<div class="box"><h2>How we work</h2><ul>
<li>We teach; we never diagnose. Students help people find a clinician.</li>
<li>Physician-reviewed content from the AAD, Skin Cancer Foundation, CDC, and peer-reviewed research</li>
<li>Anonymous before-and-after quiz at every talk; results published</li>
<li>Trained, certified student speakers</li>
<li>No product endorsements; privacy first</li></ul></div>
</div>
<div class="proof">{proof}</div>
<div class="cols">
<div><h2>Book a talk or partner with us</h2><p>Hosts: free, and we handle setup. Clinicians and faculty: join a talk, review content, or partner on a free skin-check day. Funders: printing and in-kind support reach seniors directly.</p></div>
<div><h2>Contact</h2><p><b>Zain Jaffar</b>, Co-founder<br>everyshadescreening@gmail.com · (915) 400-7072<br>zainjaffar06.github.io/everyshade</p></div>
</div>
<p class="src">(1) Culp MB, Lunsford NB. Melanoma among non-Hispanic Black Americans. Prev Chronic Dis. 2019;16:180640. (2) Perlman KL, et al. Skin of color lacks representation in medical student resources. Int J Womens Dermatol. 2021;7(2):195-196. Every Shade provides general health education only, not medical advice.</p>
</body></html>"""

PAGES = {
    "get-involved": page("en", "Get Involved | Every Shade", "Host a free skin cancer talk, volunteer as a student, partner as a clinician, or start an Every Shade chapter.", GET_INVOLVED),
    "press": page("en", "Press Kit | Every Shade", "Facts, description, founder bio, and logo for Every Shade, a Rutgers student organization giving free multilingual skin cancer talks to New Jersey seniors.", PRESS),
    "materials": page("en", "Free Handouts in 7 Languages | Every Shade", "Free large-print skin self-check handout in English, Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean.", MATERIALS),
    "about": page("en", "About Every Shade", "Every Shade is a Rutgers student group giving free, physician-reviewed skin cancer talks to New Jersey seniors in seven languages.", ABOUT),
    "faq": page("en", "FAQ | Every Shade", "Answers about Every Shade's free skin cancer talks, the anonymous quiz, languages, and the self-check tool.", FAQ),
    "privacy": page("en", "Privacy | Every Shade", "What Every Shade collects and never collects: no tracking on the site, anonymous quizzes, and a self-check tool that keeps photos on your device.", PRIVACY),
    "es": page("es", "Every Shade | Charlas gratis sobre el cáncer de piel", "Charlas gratis para mayores en Nueva Jersey sobre cómo reconocer el cáncer de piel en todos los tonos de piel.", ES),
}

if __name__ == "__main__":
    (ROOT / "site").mkdir(exist_ok=True)
    logo_full = re.search(r'(<svg viewBox="-12 8 224 140" role="img".*?</svg>)', home, re.S).group(1)
    for v, c in {"t1": "#EFCBB0", "t2": "#DDAA84", "t3": "#C28559", "t4": "#9C623A", "t5": "#6B4127", "rivet": "#FFFFFF"}.items():
        logo_full = logo_full.replace(f"var(--{v})", c)
    (ROOT / "site" / "every-shade-logo.svg").write_text(logo_full.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1))
    care_csv = ROOT / "site" / "care.csv"
    if care_csv.exists():
        rows = list(csv.DictReader(care_csv.open(encoding="utf-8")))
        # NJCEED covers breast, cervical, colorectal, prostate only: not useful for a skin spot
        rows = [r for r in rows if "njceed" not in (r["name"] + " " + r.get("notes", "")).lower()]
        rows.sort(key=lambda r: (r["county"] != "Statewide", r["county"], r["type"] != "FQHC", r["name"]))
        verified = max((r.get("verified_date", "") for r in rows), default="")
        PAGES["care"] = care_page(rows, verified)
    PAGES["impact"] = impact_page()
    (ROOT / "press" / "fact-sheet.html").parent.mkdir(exist_ok=True)
    (ROOT / "press" / "fact-sheet.html").write_text(fact_sheet())
    import subprocess
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if pathlib.Path(chrome).exists():
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={ROOT / 'press' / 'every-shade-fact-sheet.pdf'}",
                        "--virtual-time-budget=8000", "--run-all-compositor-stages-before-draw", (ROOT / "press" / "fact-sheet.html").as_uri()], capture_output=True)
        print("wrote press/every-shade-fact-sheet.pdf")
    for slug, h in PAGES.items():
        d = ROOT / slug
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(h)
        print("wrote", slug + "/index.html")
