#!/usr/bin/env python3
"""Build Every Shade subpages from the homepage's design system.

Run: python3 -I site/build_pages.py   (from the repo root)
Writes: get-involved/, press/, materials/, es/, and care/ (if site/care.csv exists) index.html files.
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
<footer><div class="wrap"><p>{FOOT[lang]}</p><p>© 2026 Every Shade · New Brunswick, New Jersey · everyshadescreening@gmail.com · (915) 400-7072</p></div></footer>
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
<p><a href="../site/every-shade-logo.svg" download>Download the logo (SVG)</a></p>
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
        if r.get("sliding_fee") == "yes": tags.append("Sliding fee")
        if r.get("accepts_uninsured") == "yes": tags.append("Sees uninsured")
        if r.get("dermatology_onsite") == "yes": tags.append("Dermatology on site")
        if r.get("languages"): tags.append(html.escape(r["languages"]))
        trs.append(f'<tr data-county="{html.escape(r["county"])}"><td>{html.escape(r["county"])}</td><td><b>{html.escape(r["name"])}</b><br><span class="note">{html.escape(r.get("type", ""))}</span></td>'
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


PAGES = {
    "get-involved": page("en", "Get Involved | Every Shade", "Host a free skin cancer talk, volunteer as a student, partner as a clinician, or start an Every Shade chapter.", GET_INVOLVED),
    "press": page("en", "Press Kit | Every Shade", "Facts, description, founder bio, and logo for Every Shade, a Rutgers student organization giving free multilingual skin cancer talks to New Jersey seniors.", PRESS),
    "materials": page("en", "Free Handouts in 7 Languages | Every Shade", "Free large-print skin self-check handout in English, Spanish, Hindi, Urdu, Gujarati, Haitian Creole, and Korean.", MATERIALS),
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
        rows.sort(key=lambda r: (r["county"], r["type"] != "FQHC", r["name"]))
        verified = max((r.get("verified_date", "") for r in rows), default="")
        PAGES["care"] = care_page(rows, verified)
    for slug, h in PAGES.items():
        d = ROOT / slug
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(h)
        print("wrote", slug + "/index.html")
