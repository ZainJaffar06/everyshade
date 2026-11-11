#!/usr/bin/env python3
"""Build translated decks, illustrations, and quizzes from i18n/<lang>.json.

Usage:  python3 -I build_translated.py es ht ko hi ur gu      (any subset)
Needs:  the English deck already built (slides/Every-Shade-Senior-Talk-2026-11-20.pptx),
        Google Chrome (to render illustrations), ../render_pdf.sh (quizzes).
Writes: slides/translated/Every-Shade-Senior-Talk-<lang>.pptx
        slides/illustrations/<lang>/<name>.png
        quiz/translated/quiz-{pre,post}-<lang>.html/.pdf
"""
import sys, json, html, re, copy, shutil, zipfile, hashlib, subprocess, pathlib, tempfile
from pptx import Presentation
from pptx.util import Pt
from pptx.oxml.ns import qn
from lxml import etree

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent
EN_DECK = KIT / "slides" / "Every-Shade-Senior-Talk-2026-11-20.pptx"
ILL = KIT / "slides" / "illustrations"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

LANG = {  # lang tag, Office font slot + face for the script, deck font scale, quiz web font, rtl
    "es": dict(tag="es-US", slot=None, face=None, scale=0.92, gfont=None, rtl=False, name="Español"),
    "ht": dict(tag="ht-HT", slot=None, face=None, scale=0.92, gfont=None, rtl=False, name="Kreyòl ayisyen"),
    "ko": dict(tag="ko-KR", slot="ea", face="Malgun Gothic", scale=0.95, gfont="Noto Sans KR", rtl=False, name="한국어"),
    "hi": dict(tag="hi-IN", slot="cs", face="Nirmala UI", scale=0.95, gfont="Noto Sans Devanagari", rtl=False, name="हिन्दी"),
    "gu": dict(tag="gu-IN", slot="cs", face="Nirmala UI", scale=0.95, gfont="Noto Sans Gujarati", rtl=False, name="ગુજરાતી"),
    "ur": dict(tag="ur-PK", slot="cs", face="Arial", scale=0.92, gfont="Noto Nastaliq Urdu", svgfont="Noto Sans Arabic", rtl=True, name="اردو"),
}
EN = json.loads((HERE / "en.json").read_text())


def style_run(r, L, scale):
    rPr = r._r.get_or_add_rPr()
    rPr.set("lang", L["tag"])
    if L["slot"]:
        for tagname in ("latin", "ea", "cs"):
            pass
        el = rPr.find(qn(f"a:{L['slot']}"))
        if el is None:
            el = etree.SubElement(rPr, qn(f"a:{L['slot']}"))
        el.set("typeface", L["face"])
    if scale != 1.0 and r.font.size:
        r.font.size = Pt(round(r.font.size.pt * scale, 1))


def translate_frame(tf, tmap, L, scale):
    for p in tf.paragraphs:
        runs = p.runs
        if not runs:
            continue
        src = "".join(r.text for r in runs).strip()
        if src in tmap:
            runs[0].text = tmap[src]
            for extra in runs[1:]:
                extra._r.getparent().remove(extra._r)
        for r in p.runs:
            style_run(r, L, scale)
        if L["tag"] == "ko-KR":
            p._p.get_or_add_pPr().set("eaLnBrk", "0")
        if L["rtl"]:
            pPr = p._p.get_or_add_pPr()
            pPr.set("rtl", "1")
            if pPr.get("algn") in (None, "l"):
                pPr.set("algn", "r")


def walk(shapes, tmap, L, scale):
    for sh in shapes:
        if sh.has_text_frame:
            translate_frame(sh.text_frame, tmap, L, scale)


def render_illustrations(lang, T):
    out = ILL / lang
    out.mkdir(exist_ok=True)
    rtl = LANG[lang]["rtl"]
    for svg in sorted(ILL.glob("*.svg")):
        s = svg.read_text()
        j = [0]

        def rep(m):
            j[0] += 1
            key = f"{svg.stem}_{j[0]}"
            txt = html.escape(T["illustrations"].get(key, m.group(1)), quote=False)
            return f">{txt}</text>"
        s = re.sub(r">([^<>]+)</text>", rep, s)
        if rtl:
            s = s.replace("<text ", '<text direction="rtl" ')
        font = LANG[lang].get("svgfont") or LANG[lang]["gfont"]
        if font:
            s = s.replace('font-family="Arial, Helvetica, sans-serif"', f'font-family="{font}, Arial, sans-serif"')
        tmpdir = pathlib.Path(tempfile.mkdtemp())
        (tmpdir / "i.svg").write_text(s)
        link = f"<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family={font.replace(' ', '+')}:wght@400;700&display=swap'>" if font else ""
        # inline the SVG so web fonts apply
        (tmpdir / "i.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'>{link}<style>html,body{{margin:0;background:#F7F1EC}}svg{{display:block;width:560px;height:470px}}</style></head><body>{s}</body></html>")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=4",
                        "--window-size=560,470", "--virtual-time-budget=6000", f"--screenshot={out / (svg.stem + '.png')}",
                        f"file://{tmpdir / 'i.html'}"], capture_output=True)
        shutil.rmtree(tmpdir)
    return out


def build_deck(lang):
    L = LANG[lang]
    T = json.loads((HERE / f"{lang}.json").read_text())
    tmap = {EN["slide_text"][k]: v for k, v in T["slide_text"].items() if k in EN["slide_text"]}
    prs = Presentation(EN_DECK)
    for layout in prs.slide_layouts:
        walk(layout.shapes, tmap, L, 0.85)
    for i, s in enumerate(prs.slides):
        walk(s.shapes, tmap, L, L["scale"])
        nk = f"n{i + 1:02d}"
        if s.has_notes_slide and nk in T["notes"]:
            s.notes_slide.notes_text_frame.text = T["notes"][nk]
    out_dir = KIT / "slides" / "translated"
    out_dir.mkdir(exist_ok=True)
    tmp = out_dir / f"_tmp_{lang}.pptx"
    prs.save(tmp)
    # swap illustration images by content hash
    ill_dir = render_illustrations(lang, T)
    swap = {}
    for png in ILL.glob("*.png"):
        swap[hashlib.sha256(png.read_bytes()).hexdigest()] = (ill_dir / png.name).read_bytes()
    final = out_dir / f"Every-Shade-Senior-Talk-{lang}.pptx"
    n = 0
    with zipfile.ZipFile(tmp) as zin, zipfile.ZipFile(final, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith("ppt/media/"):
                h = hashlib.sha256(data).hexdigest()
                if h in swap:
                    data = swap[h]; n += 1
            zout.writestr(item, data)
    tmp.unlink()
    print(f"{lang}: deck written ({n} illustrations swapped) -> {final.name}")


QCSS = (KIT / "quiz" / "build_quiz.py").read_text().split('CSS = """', 1)[1].split('"""', 1)[0]


def build_quiz(lang):
    L = LANG[lang]
    T = json.loads((HERE / f"{lang}.json").read_text())
    Q, U = T["quiz"], T["quiz_ui"]
    font = L["gfont"]
    css = QCSS
    if font:
        css = css.replace("font-family:'Atkinson Hyperlegible',Arial", f"font-family:'{font}','Atkinson Hyperlegible',Arial")
        css = css.replace("font-family:'Manrope',Arial", f"font-family:'{font}','Manrope',Arial")
        css = css.replace("font-family:'Manrope';", f"font-family:'{font}','Manrope';")
        css += "\n.tag{letter-spacing:0;text-transform:none}"
    if lang == "ur":
        css += "\nhtml,body{line-height:1.85;font-size:14pt} .opts span{font-size:13.5pt} li.q .t{margin-bottom:5pt} ol{gap:5pt}"
    fam = "family=Manrope:wght@600;800&family=Atkinson+Hyperlegible:wght@400;700"
    if font:
        fam = f"family={font.replace(' ', '+')}:wght@400;700&" + fam
    letters = "ABCDE"
    d = "rtl" if L["rtl"] else "ltr"

    def rq(n, q):
        opts = "".join(f"<span><bdi>{letters[i]}.</bdi> {html.escape(o)}</span>" for i, o in enumerate(q["options"]))
        return f"<li class='q'><span class='t'>{n}. {html.escape(q['q'])}</span><div class='opts'>{opts}</div></li>"
    out_dir = KIT / "quiz" / "translated"
    out_dir.mkdir(exist_ok=True)
    for phase in ("pre", "post"):
        h = [f"<!doctype html><html lang='{L['tag']}' dir='{d}'><head><meta charset='utf-8'><title>{html.escape(Q['title'])}</title>"
             f"<link rel='stylesheet' href='https://fonts.googleapis.com/css2?{fam}&display=swap'><style>{css}</style></head><body>",
             "<div class='strip'><i></i><i></i><i></i><i></i><i></i><i></i></div>",
             f"<span class='tag'>{html.escape(U['tag_pre'] if phase == 'pre' else U['tag_post'])}</span>",
             f"<h1>{html.escape(U['heading'])}</h1>", f"<p class='inst'>{html.escape(Q['instructions'])}</p>", "<ol>"]
        n = 0
        for q in Q["scored"]:
            n += 1; h.append(rq(n, q))
        h.append(f"</ol><p class='sec'>{html.escape(U['more'])}</p><ol>")
        for q in Q["unscored"]:
            if q.get("pre_only") and phase != "pre": continue
            if q.get("post_only") and phase != "post": continue
            n += 1; h.append(rq(n, q))
        h.append("</ol>")
        h.append(f"<p class='code'>{html.escape(U['code'])} <bdi>____ ____ ____ ____</bdi></p>")
        h.append(f"<p class='foot'><bdi>{html.escape(U['foot'])}</bdi></p></body></html>")
        f = out_dir / f"quiz-{phase}-{lang}.html"
        f.write_text("\n".join(h))
        subprocess.run([str(KIT / "render_pdf.sh"), str(f), str(f.with_suffix(".pdf"))], capture_output=True)
    print(f"{lang}: quizzes written")


if __name__ == "__main__":
    langs = sys.argv[1:] or list(LANG)
    for lg in langs:
        if not (HERE / f"{lg}.json").exists():
            print(f"{lg}: no {lg}.json yet, skipped"); continue
        build_deck(lg)
        build_quiz(lg)
