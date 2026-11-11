#!/usr/bin/env python3
"""Build toolkit/index.html from the numbered Markdown files.

Supports the small Markdown subset used in the toolkit: # / ## / ### headings,
paragraphs, - bullets, 1. numbered lists, > blockquotes, ``` code blocks,
| tables |, **bold**, *italic*, `code`, [text](url), and bare https:// URLs.
"""
import html
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = SRC / "index.html"

LOGO = """<svg viewBox="-12 8 224 140" role="img" aria-label="Every Shade logo: five skin-tone swatches fanned out">
          <rect x="82" y="20" width="36" height="130" rx="18" fill="var(--t1)" transform="rotate(-44 100 132)"/>
          <rect x="82" y="20" width="36" height="130" rx="18" fill="var(--t2)" transform="rotate(-22 100 132)"/>
          <rect x="82" y="20" width="36" height="130" rx="18" fill="var(--t3)"/>
          <rect x="82" y="20" width="36" height="130" rx="18" fill="var(--t4)" transform="rotate(22 100 132)"/>
          <rect x="82" y="20" width="36" height="130" rx="18" fill="var(--t5)" transform="rotate(44 100 132)"/>
          <circle cx="100" cy="132" r="6" fill="var(--rivet)"/>
        </svg>"""

NAV_LOGO = LOGO.replace('<svg viewBox', '<svg width="40" height="30" viewBox').replace(
    'role="img" aria-label="Every Shade logo: five skin-tone swatches fanned out"', 'aria-hidden="true"')

STRIP = '<div class="strip" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>'


def inline(text: str) -> str:
    """Escape and apply inline formatting."""
    # protect inline code first
    parts = re.split(r'(`[^`]+`)', text)
    out = []
    for p in parts:
        if p.startswith('`') and p.endswith('`') and len(p) > 1:
            out.append('<code>' + html.escape(p[1:-1]) + '</code>')
            continue
        s = html.escape(p, quote=False)
        s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'<a href="\2">\1</a>', s)
        s = re.sub(r'(?<![">])(https?://[^\s<)]+?)([.,;)]?)(?=\s|$)', r'<a href="\1">\1</a>\2', s)
        s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
        out.append(s)
    return ''.join(out)


def slug(s: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s


def convert(md: str, sec_id: str):
    lines = md.splitlines()
    i = 0
    out = []
    title = ''
    subheads = []
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append('<pre><code>' + html.escape('\n'.join(buf)) + '</code></pre>')
            continue
        if line.startswith('# '):
            title = line[2:].strip()
            i += 1
            continue
        if line.startswith('## '):
            h = line[3:].strip()
            hid = sec_id + '-' + slug(h)
            subheads.append((hid, h))
            out.append(f'<h3 id="{hid}">{inline(h)}</h3>')
            i += 1
            continue
        if line.startswith('### '):
            out.append(f'<h4>{inline(line[4:].strip())}</h4>')
            i += 1
            continue
        if line.startswith('> '):
            buf = []
            while i < len(lines) and lines[i].startswith('> '):
                buf.append(lines[i][2:])
                i += 1
            out.append('<blockquote><p>' + inline(' '.join(buf)) + '</p></blockquote>')
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i])
                i += 1
            cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
            header = cells[0]
            body = [r for r in cells[1:] if not all(re.fullmatch(r'-+', c) for c in r)]
            t = ['<div class="tablewrap"><table><thead><tr>']
            t += [f'<th>{inline(c)}</th>' for c in header]
            t.append('</tr></thead><tbody>')
            for r in body:
                t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            continue
        if re.match(r'^- ', line):
            items = []
            while i < len(lines) and re.match(r'^- ', lines[i]):
                item = lines[i][2:]
                i += 1
                while i < len(lines) and re.match(r'^\s{2,}\S', lines[i]) and not re.match(r'^\s*- ', lines[i]):
                    item += ' ' + lines[i].strip()
                    i += 1
                items.append(f'<li>{inline(item)}</li>')
            out.append('<ul>' + ''.join(items) + '</ul>')
            continue
        if re.match(r'^\d+\. ', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\. ', lines[i]):
                item = re.sub(r'^\d+\. ', '', lines[i])
                i += 1
                while i < len(lines) and re.match(r'^\s{2,}\S', lines[i]) and not re.match(r'^\s*\d+\. ', lines[i]):
                    item += ' ' + lines[i].strip()
                    i += 1
                items.append(f'<li>{inline(item)}</li>')
            out.append('<ol>' + ''.join(items) + '</ol>')
            continue
        if line.strip() == '':
            i += 1
            continue
        # paragraph
        buf = []
        while i < len(lines) and lines[i].strip() != '' and not re.match(r'^(#|- |\d+\. |> |\||```)', lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append('<p>' + inline(' '.join(buf)) + '</p>')
    return title, subheads, '\n'.join(out)


files = sorted(SRC.glob('[0-9][0-9]-*.md'))
sections = []
for f in files:
    num = f.name[:2]
    sec_id = 's' + num
    title, subheads, body = convert(f.read_text(encoding='utf-8'), sec_id)
    sections.append((num, sec_id, title, subheads, body, f.name))

toc = []
for num, sec_id, title, subheads, body, fname in sections:
    short = re.sub(r'^\d+\.\s*', '', title)
    toc.append(f'<li><a href="#{sec_id}"><b>{num}</b> {html.escape(short)}</a></li>')

body_html = []
for idx, (num, sec_id, title, subheads, body, fname) in enumerate(sections):
    short = re.sub(r'^\d+\.\s*', '', title)
    tint = ' class="tint"' if idx % 2 == 1 else ''
    sub_nav = ''
    if subheads:
        sub_nav = '<ul class="subnav">' + ''.join(f'<li><a href="#{hid}">{html.escape(h)}</a></li>' for hid, h in subheads) + '</ul>'
    body_html.append(f'''
  <section id="{sec_id}"{tint}>
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Section {num} of {len(sections):02d} · <a href="{fname}">{fname}</a></span>
        <h2>{html.escape(short)}</h2>
        {sub_nav}
      </div>
      <div class="prose">
{body}
      </div>
      <p class="totop"><a href="#top">Back to top</a></p>
    </div>
  </section>''')
    if idx < len(sections) - 1:
        pass

CSS = """
/* Layout: one calm column (max 1080px), same tokens as the main site, tone strip as divider. Large type for older readers. */
:root{
  --ground:#FFFFFF;
  --band:#F7F1EC;
  --ink:#2B1A12;
  --muted:#6B5446;
  --rule:#E6D9CF;
  --accent:#8E5632;
  --t1:#EFCBB0;--t2:#DDAA84;--t3:#C28559;--t4:#9C623A;--t5:#6B4127;--t6:#3D2416;
  --rivet:#FFFFFF;
  --display:'Manrope',system-ui,sans-serif;
  --body:'Atkinson Hyperlegible',system-ui,-apple-system,'Segoe UI',sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --ground:#1A110C;--band:#24180F;--ink:#F6ECE4;--muted:#CDB8A8;--rule:#3B2A1F;--accent:#E3A877;--rivet:#1A110C;color-scheme:dark}}
:root[data-theme="dark"]{
  --ground:#1A110C;--band:#24180F;--ink:#F6ECE4;--muted:#CDB8A8;--rule:#3B2A1F;--accent:#E3A877;--rivet:#1A110C;color-scheme:dark}

html{scroll-behavior:smooth}
body{background:var(--ground);color:var(--ink);font-family:var(--body);font-size:18px;line-height:1.6}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4{font-family:var(--display);line-height:1.15;text-wrap:balance;margin:0}
h1{font-size:clamp(2.2rem,5.2vw,3.6rem);font-weight:800;letter-spacing:-0.02em}
h2{font-size:clamp(1.7rem,3.4vw,2.4rem);font-weight:800;letter-spacing:-0.015em}
h3{font-size:1.35rem;font-weight:800}
h4{font-size:1.1rem;font-weight:800;color:var(--muted)}
p{margin:0;max-width:65ch}
a{color:var(--accent)}
a:focus-visible,button:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
.eyebrow{font-family:var(--display);font-weight:600;font-size:0.85rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted)}
.eyebrow a{color:var(--muted);text-transform:none;letter-spacing:0;font-family:var(--body);font-weight:400}

/* nav */
header.top{border-bottom:1px solid var(--rule)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-block:14px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}
.brand span{font-family:var(--display);font-weight:800;font-size:1.35rem;letter-spacing:-0.02em}
nav ul{display:flex;gap:20px;list-style:none;margin:0;padding:0;flex-wrap:wrap}
nav a{color:var(--ink);text-decoration:none;font-weight:700;font-size:1rem}
nav a:hover{color:var(--accent)}

/* hero */
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:48px;align-items:center;padding-block:72px 64px}
.hero-copy{display:flex;flex-direction:column;gap:22px;min-width:0}
.hero-copy p{font-size:1.2rem;color:var(--muted)}
.hero-mark{display:flex;justify-content:center}
.hero-mark svg{width:100%;max-width:340px;height:auto}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 26px;border-radius:999px;background:var(--ink);color:var(--ground);font-family:var(--display);font-weight:800;font-size:1.05rem;text-decoration:none;border:0;cursor:pointer;align-self:flex-start}
.btn:hover{background:var(--accent)}

/* tone strip divider */
.strip{display:grid;grid-template-columns:repeat(6,1fr);height:10px}
.strip i:nth-child(1){background:var(--t1)}.strip i:nth-child(2){background:var(--t2)}.strip i:nth-child(3){background:var(--t3)}
.strip i:nth-child(4){background:var(--t4)}.strip i:nth-child(5){background:var(--t5)}.strip i:nth-child(6){background:var(--t6)}

section{padding-block:64px;scroll-margin-top:16px}
section.tint{background:var(--band)}
.section-head{display:flex;flex-direction:column;gap:12px;margin-bottom:32px}
.section-head p{color:var(--muted)}

/* contents */
.contents ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 36px;counter-reset:none}
.contents li a{display:flex;gap:14px;align-items:baseline;text-decoration:none;color:var(--ink);font-weight:700;font-size:1.1rem;padding:12px 0;border-top:1px solid var(--rule)}
.contents li a b{font-family:var(--display);color:var(--accent);font-variant-numeric:tabular-nums}
.contents li a:hover{color:var(--accent)}
.subnav{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px 18px}
.subnav a{font-size:0.95rem;font-weight:700;text-decoration:none;color:var(--muted)}
.subnav a:hover{color:var(--accent)}

/* prose */
.prose{display:flex;flex-direction:column;gap:18px;min-width:0}
.prose>*{min-width:0;max-width:100%}
.prose p,.prose li,.prose td,.prose th{overflow-wrap:anywhere}
.prose a{word-break:break-word}
.prose h3{margin-top:22px;padding-top:18px;border-top:4px solid var(--t4);max-width:65ch;scroll-margin-top:16px}
.prose h4{margin-top:6px}
.prose ul,.prose ol{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:8px;max-width:65ch}
.prose li{padding-left:0.2em}
.prose blockquote{margin:0;padding:18px 22px;border-left:6px solid var(--t3);background:var(--ground);border-radius:0 14px 14px 0;max-width:65ch}
section.tint .prose blockquote{background:var(--ground)}
section:not(.tint) .prose blockquote{background:var(--band)}
.prose blockquote p{font-weight:700}
.prose pre{margin:0;padding:18px 20px;border:1px solid var(--rule);border-radius:14px;background:var(--band);overflow-x:auto;font-size:0.95rem;line-height:1.5;max-width:100%}
section.tint .prose pre{background:var(--ground)}
.prose pre code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}
.prose code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:0.92em;background:var(--band);padding:1px 5px;border-radius:5px}
section.tint .prose code{background:var(--ground)}
.prose pre code{background:transparent;padding:0}
.tablewrap{overflow-x:auto;max-width:100%;min-width:0;width:100%}
.prose table{border-collapse:collapse;width:100%;min-width:480px;font-size:1rem}
.prose th,.prose td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--rule)}
.prose th{font-family:var(--display);font-weight:800;border-bottom:3px solid var(--t4)}
.totop{margin-top:36px;font-size:0.95rem}
.totop a{font-weight:700}

footer{border-top:1px solid var(--rule)}
footer .wrap{padding-block:32px;display:flex;flex-direction:column;gap:10px;font-size:0.9rem;color:var(--muted)}

@media (max-width:820px){
  .hero .wrap{grid-template-columns:minmax(0,1fr);padding-block:48px}
  .hero-mark{order:-1;justify-content:flex-start}
  .hero-mark svg{max-width:180px}
  .contents ol{grid-template-columns:minmax(0,1fr)}
  section{padding-block:48px}
  .prose pre{font-size:0.85rem}
}
@media (prefers-reduced-motion:no-preference){.btn,nav a{transition:background .15s,color .15s,border-color .15s}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{header.top nav,.totop,.subnav{display:none}section{padding-block:24px;break-inside:auto}.prose h3{break-after:avoid}}
"""

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta property="og:title" content="Every Shade Chapter Toolkit">
<meta property="og:description" content="How to start and run an Every Shade chapter at your college: free skin cancer talks for every skin tone, a monthly self-check, and connecting people to care.">
<meta property="og:type" content="website">
<style>html,body{{margin:0}}img{{max-width:100%}}*{{box-sizing:border-box}}</style>
<title>Every Shade | Chapter Toolkit</title>
<meta name="description" content="A practical toolkit for students at other colleges to start an Every Shade chapter: an 8-week plan, roles, booking talks, running the talk, measuring outcomes, content standards, languages, brand, and the chapter agreement.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap">
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="../" aria-label="Every Shade home">
      {NAV_LOGO}
      <span>every shade</span>
    </a>
    <nav aria-label="Main">
      <ul>
        <li><a href="../">Home</a></li>
        <li><a href="#contents">Contents</a></li>
        <li><a href="#s02">Start a chapter</a></li>
        <li><a href="#s10">Agreement</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="top">
  <div class="hero">
    <div class="wrap">
      <div class="hero-copy">
        <span class="eyebrow">Chapter toolkit · For students at other colleges</span>
        <h1>Start an Every Shade chapter at your school.</h1>
        <p>Every Shade gives free 45-minute talks on how skin cancer looks on every skin tone, teaches a monthly at-home skin check, and connects people to free and low-cost care. This toolkit is everything you need to run the same program in your community: a plan, the scripts, the standards, and the agreement.</p>
        <a class="btn" href="#s02">See the 8-week plan</a>
      </div>
      <div class="hero-mark">
        {LOGO}
      </div>
    </div>
  </div>

  {STRIP}

  <section id="contents" class="contents">
    <div class="wrap">
      <div class="section-head">
        <span class="eyebrow">Contents</span>
        <h2>Ten sections. Read 01 and 02 first.</h2>
        <p>Each section is also a Markdown file in the repository, linked from its heading. Questions: <a href="mailto:everyshadescreening@gmail.com">everyshadescreening@gmail.com</a>.</p>
      </div>
      <ol>
        {''.join(toc)}
      </ol>
    </div>
  </section>

  {STRIP}
{''.join(body_html)}
</main>

{STRIP}
<footer>
  <div class="wrap">
    <p>Every Shade provides general health education only. Nothing on this site or in our talks is medical advice or a diagnosis. Our members are students, not medical professionals. If a spot is new, changing, or bleeding, please see a doctor.</p>
    <p>© 2026 Every Shade · New Brunswick, New Jersey · <a href="../">everyshade home</a></p>
  </div>
</footer>
</body>
</html>
'''

OUT.write_text(page, encoding='utf-8')
print(f"wrote {OUT} ({len(page):,} bytes, {len(sections)} sections)")
