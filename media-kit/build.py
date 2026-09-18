"""Build the Agri Lacombe media kit into public/media-kit/.

Everything is generated from two sources:
  public/images/agrilacombe_logo.png   the farm's logo (used as-is, never redrawn)
  src/data/media-kit.json              all texts, contact details and seasons (FR/EN/ES)

Run from the repo root:
  uv run --no-project --with fonttools --with pillow --with numpy --with scipy python media-kit/build.py
"""

import html
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KIT = ROOT / "media-kit"
BUILD = KIT / "build"
OUT = ROOT / "public" / "media-kit"
sys.path.insert(0, str(KIT / "src"))

import fonts  # noqa: E402
import logo_files  # noqa: E402
from brand import PALETTE, hex_to_rgb  # noqa: E402

DATA = json.loads((ROOT / "src" / "data" / "media-kit.json").read_text())
CHROME = shutil.which("google-chrome") or shutil.which("chromium")
C = {colour["key"]: colour["hex"] for colour in PALETTE}
KIT_NAME = "AgriLacombe_Trousse-media"
LOGO_SRC = ROOT / "public" / "images" / "agrilacombe_logo.png"

e = html.escape


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def run(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def logo_img(key):
    """<img> of one of the kit's logo files (written by logo_files.build before any document)."""
    return f'<img class="logo" src="{LOGO_FILES[key].as_uri()}" alt="">'


LOGO_FILES = {
    "original": OUT / "logos" / "AgriLacombe_Logo_original.png",
    "transparent": OUT / "logos" / "AgriLacombe_Logo_fond-transparent.png",
    "nb": OUT / "logos" / "AgriLacombe_Logo_noir-et-blanc.png",
}
LOGO = logo_img("transparent")

BASE_CSS = fonts.inter_font_faces(BUILD / "fonts") + f"""
@page {{ size: letter; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
html, body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact }}
body {{ font-family: Inter, sans-serif; color: #26301f; font-size: 10pt; line-height: 1.45 }}
h1, h2, h3, .mont {{ font-family: Montserrat, sans-serif; color: {C['forest']} }}
.page {{ width: 8.5in; height: 11in; position: relative; overflow: hidden; break-after: page }}
.land {{ width: 11in; height: 8.5in }}
img.logo {{ display: block; width: 100%; height: 100%; object-fit: contain }}
.kicker {{ font-family: Montserrat, sans-serif; font-size: 8pt; letter-spacing: .18em;
          text-transform: uppercase; color: {C['green']}; font-weight: 700 }}
"""


DOC_FILES = {
    "fr": {"fiche": "AgriLacombe_Fiche-presentation_FR", "affichette": "AgriLacombe_Affichette-produit-local_FR",
           "guide": "AgriLacombe_Guide-de-marque_FR"},
    "en": {"fiche": "AgriLacombe_Fact-sheet_EN", "affichette": "AgriLacombe_Local-product-sign_EN",
           "guide": "AgriLacombe_Brand-guide_EN"},
    "es": {"fiche": "AgriLacombe_Ficha-presentacion_ES", "affichette": "AgriLacombe_Cartel-producto-local_ES",
           "guide": "AgriLacombe_Guia-de-marca_ES"},
}


def colon(lang):
    return " : " if lang == "fr" else ": "


def contact_line(lang):
    t = DATA[lang]["contactBlock"]
    c = DATA["contact"]
    return [f"{t['email']}{colon(lang)}{c['email']}", c["web"], f"Facebook{colon(lang)}{c['facebookName']}"]


def address(lang):
    return DATA["contact"]["address"][lang]


def seasons_table(lang):
    t = DATA[lang]["seasons"]
    head = "".join(f"<th>{e(m)}</th>" for m in t["months"])
    rows = []
    for crop in DATA["seasons"]:
        cells = []
        for m in range(1, 13):
            cls = "fresh" if m in crop["months"] else ""
            if crop.get("extra") and cls == "fresh":
                cls = "extra"
            cells.append(f'<td class="{cls}"></td>')
        name = e(t["crops"][crop["key"]])
        sep = ' class="sep"' if crop.get("extra") else ""
        rows.append(f"<tr{sep}><th class='crop'>{name}</th>{''.join(cells)}</tr>")
    return (f'<table class="seasons"><col class="crop"><thead><tr><th></th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


SEASONS_CSS = f"""
table.seasons {{ width: 100%; border-collapse: separate; border-spacing: 2px; font-size: 7.5pt;
                 table-layout: fixed }}
table.seasons col.crop {{ width: 1.55in }}
table.seasons thead th {{ font-family: Montserrat, sans-serif; font-weight: 700; color: {C['forest']};
                         letter-spacing: .04em; padding-bottom: 2px }}
table.seasons th.crop {{ text-align: left; font-weight: 600; font-size: 8.5pt; white-space: nowrap;
                        padding-right: 8px; color: #26301f; font-family: Inter, sans-serif }}
table.seasons td {{ height: 15px; background: #ebeadc; border-radius: 3px }}
table.seasons td.fresh {{ background: {C['green']} }}
table.seasons td.extra {{ background: {C['gold']} }}
table.seasons tr.sep th.crop {{ padding-top: 5px; color: #6b5a2a }}
"""


# --------------------------------------------------------------------------
# documents
# --------------------------------------------------------------------------

def fiche(lang):
    d = DATA[lang]
    kicker = d["ficheKicker"]
    points = "".join(
        f'<div class="pt"><div class="num">{i}</div><div><h3>{e(p["title"])}</h3>'
        f'<p>{e(p["text"])}</p></div></div>'
        for i, p in enumerate(d["pitch"]["points"], 1))
    facts = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in d["facts"]["items"])
    contacts = "".join(f"<span>{e(x)}</span>" for x in contact_line(lang))
    css = BASE_CSS + SEASONS_CSS + f"""
    .top {{ background: {C['cream']}; padding: .45in .55in .3in; display: flex; gap: .35in; align-items: center }}
    .top .mark {{ width: 2.35in; height: 2.05in; flex: none }}
    .top h1 {{ font-size: 21pt; line-height: 1.15; margin: 6px 0 10px }}
    .top .lede {{ font-size: 10.5pt; color: #3e4a35 }}
    .band {{ background: {C['forest']}; color: #f4f3e8; padding: .22in .55in; font-size: 10.5pt; line-height: 1.5 }}
    .cols {{ display: grid; grid-template-columns: 1.45fr 1fr; gap: .35in; padding: .3in .55in .1in }}
    h2 {{ font-size: 12pt; margin-bottom: 9px; letter-spacing: .02em }}
    .pt {{ display: flex; gap: 10px; margin-bottom: 10px }}
    .pt .num {{ flex: none; width: 22px; height: 22px; border-radius: 50%; background: {C['gold']};
               color: #fff; font: 700 9.5pt Montserrat, sans-serif; display: grid; place-items: center }}
    .pt h3 {{ font-size: 10pt; margin-bottom: 1px }}
    .pt p {{ font-size: 9pt; color: #3e4a35 }}
    dl {{ font-size: 9pt }}
    dt {{ font-weight: 700; color: {C['forest']}; font-size: 7.5pt; text-transform: uppercase;
          letter-spacing: .08em; margin-top: 7px }}
    dd {{ color: #3e4a35 }}
    .seas {{ padding: .08in .55in 0 }}
    .foot {{ position: absolute; left: 0; right: 0; bottom: 0; background: {C['forest']};
             padding: .22in .55in; display: flex; align-items: center; justify-content: space-between }}
    .foot .n {{ color: #f4f3e8 }}
    .foot .n b {{ display: block; font: 700 14pt Montserrat, sans-serif }}
    .foot .n span {{ display: block; font-size: 8.5pt; opacity: .85 }}
    .foot .c {{ color: #f4f3e8; font-size: 8.5pt; text-align: right; display: grid; gap: 1px }}
    """
    body = f"""
    <div class="page">
      <div class="top">
        <div class="mark">{LOGO}</div>
        <div><div class="kicker">{e(kicker)}</div><h1>{e(d['pitch']['headline'])}</h1>
        <p class="lede">{e(d['texts']['short'])}</p></div>
      </div>
      <div class="band">{e(d['pitch']['elevator'])}</div>
      <div class="cols">
        <div><h2>{e(d['pitch']['title'])}</h2>{points}</div>
        <div><h2>{e(d['facts']['title'])}</h2><dl>{facts}</dl></div>
      </div>
      <div class="seas"><h2>{e(d['seasons']['title'])}</h2>{seasons_table(lang)}</div>
      <div class="foot"><div class="n"><b>Ferme Agri Lacombe</b>{"".join(f"<span>{e(x)}</span>" for x in address(lang))}</div>
        <div class="c">{contacts}</div></div>
    </div>"""
    return css, body


def affichette(lang):
    t = DATA[lang]["sign"]
    css = BASE_CSS + f"""
    @page {{ size: 11in 8.5in; margin: 0 }}
    .page {{ background: {C['cream']} }}
    .inner {{ display: flex; align-items: center; gap: .5in; padding: .6in .75in 0; height: 7.1in }}
    .mark {{ width: 4.3in; height: 3.75in; flex: none }}
    .pill {{ display: inline-block; background: {C['gold']}; color: #fff; font: 700 13pt Montserrat, sans-serif;
             letter-spacing: .2em; padding: 6px 18px; border-radius: 999px }}
    h1 {{ font-size: 60pt; line-height: 1; margin: 18px 0 14px; letter-spacing: -.01em }}
    .sub {{ font-size: 19pt; color: #3e4a35; line-height: 1.3 }}
    .rule {{ width: 1.2in; height: 5px; background: {C['green']}; border-radius: 3px; margin: 22px 0 }}
    .desc {{ font-size: 14pt; color: #3e4a35 }}
    .foot {{ position: absolute; left: 0; right: 0; bottom: 0; height: 1.4in; background: {C['forest']};
             display: flex; align-items: center; justify-content: space-between; padding: 0 .75in }}
    .foot .n {{ color: #f4f3e8; font: 700 22pt Montserrat, sans-serif }}
    .foot .n span {{ display: block; font: 400 11pt Inter, sans-serif; opacity: .85; margin-top: 4px }}
    .foot .c {{ color: #f4f3e8; font-size: 13pt; text-align: right; line-height: 1.5 }}
    """
    body = f"""
    <div class="page land">
      <div class="inner">
        <div class="mark">{LOGO}</div>
        <div>
          <span class="pill">{e(t['pill'])}</span>
          <h1>{e(t['title'])}</h1>
          <p class="sub">{"<br>".join(map(e, t['sub']))}</p>
          <div class="rule"></div>
          <p class="desc">{"<br>".join(map(e, t['desc']))}</p>
        </div>
      </div>
      <div class="foot"><div class="n">Ferme Agri Lacombe<span>{e(", ".join(address(lang)))}</span></div>
        <div class="c">{e(DATA['contact']['web'])}<br>Facebook{colon(lang)}{e(DATA['contact']['facebookName'])}</div></div>
    </div>"""
    return css, body


def guide(lang):
    d = DATA[lang]
    g = d["guide"]
    v = d["logos"]["variants"]
    swatches = "".join(
        f'<div class="sw"><div class="chip" style="background:{c["hex"]}"></div><h3>{e(c["name"][lang])}</h3>'
        f'<p>HEX {c["hex"]}<br>{g["rgb"]} {", ".join(map(str, hex_to_rgb(c["hex"])))}</p>'
        f'<p class="role">{e(c["role"][lang])}</p></div>'
        for c in PALETTE)
    dos = "".join(f"<li>{e(x)}</li>" for x in d["rules"]["do"])
    donts = "".join(f"<li>{e(x)}</li>" for x in d["rules"]["dont"])
    bad = zip(("transform:scaleX(1.45)", "filter:hue-rotate(150deg) saturate(1.6)", "",
               "filter:drop-shadow(6px 6px 4px rgba(0,0,0,.55))"),
              ("", "", f"background:{C['forest']}", ""), g["bad"])
    bad_html = "".join(
        f'<div class="bad"><div class="box" style="{bg}"><div class="l" style="{tf}">{LOGO}</div>'
        f'<span class="x">✕</span></div><p>{e(label)}</p></div>' for tf, bg, label in bad)
    css = BASE_CSS + f"""
    .page {{ padding: .55in .6in }}
    .hdr {{ display: flex; justify-content: space-between; align-items: flex-end;
            border-bottom: 2px solid {C['forest']}; padding-bottom: 12px; margin-bottom: 20px }}
    .hdr .h {{ width: 1in; height: .88in }}
    .hdr .t {{ text-align: right }}
    .hdr h1 {{ font-size: 20pt }}
    .hdr p {{ font-size: 8pt; color: #6c7560 }}
    h2 {{ font-size: 13pt; margin: 4px 0 10px }}
    .lead {{ color: #3e4a35; margin-bottom: 12px }}
    .logos {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px }}
    .card {{ border: 1px solid #dcdccb; border-radius: 8px; overflow: hidden }}
    .card .v {{ height: 1.75in; padding: 14px }}
    .card .v > div {{ width: 100%; height: 100%; margin: 0 auto }}
    .card .cap {{ padding: 7px 10px; font-size: 8.5pt; border-top: 1px solid #dcdccb; background: #fff }}
    .card .cap b {{ color: {C['forest']}; font-family: Montserrat, sans-serif }}
    .span2 {{ grid-column: span 2 }}
    .zone {{ display: flex; gap: .4in; align-items: center; margin-top: 18px }}
    .zone .demo {{ position: relative; width: 2.4in; height: 2.2in; border: 1.5px dashed #b4532a;
                   padding: .28in; background: repeating-linear-gradient(45deg, #fbeee6 0 6px, #fff 6px 12px) }}
    .zone .demo > div {{ width: 100%; height: 100%; background: #fff }}
    .zone .demo .x {{ position: absolute; top: 2px; left: 50%; transform: translateX(-50%); font: 700 8pt Montserrat;
                      color: #b4532a }}
    table.min {{ border-collapse: collapse; font-size: 9pt }}
    table.min td {{ padding: 5px 14px 5px 0; border-bottom: 1px solid #e3e3d3 }}
    .sws {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px }}
    .sw .chip {{ height: .8in; border-radius: 6px; border: 1px solid #dcdccb }}
    .sw h3 {{ font-size: 9.5pt; margin: 6px 0 2px }}
    .sw p {{ font-size: 7.5pt; color: #3e4a35; font-variant-numeric: tabular-nums }}
    .sw p.role {{ margin-top: 4px; color: #6c7560; font-style: italic }}
    .rules {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; font-size: 9pt }}
    .rules h3 {{ font-size: 10pt; margin-bottom: 4px }}
    .rules ul {{ padding-left: 16px }}
    .rules li {{ margin-bottom: 3px }}
    .bads {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 12px }}
    .bad .box {{ position: relative; height: 1.15in; border: 1px solid #dcdccb; border-radius: 6px;
                 display: grid; place-items: center; overflow: hidden; background: #fff }}
    .bad .l {{ width: 1in; height: .9in }}
    .bad .x {{ position: absolute; top: 4px; right: 7px; color: #c0392b; font-weight: 700; font-size: 13pt }}
    .bad p {{ font-size: 8pt; text-align: center; margin-top: 3px; color: #6c7560 }}
    .foot {{ position: absolute; bottom: .45in; left: .6in; right: .6in; font-size: 7.5pt; color: #6c7560;
             border-top: 1px solid #dcdccb; padding-top: 6px; display: flex; justify-content: space-between }}
    """
    foot = (f'<div class="foot"><span>Ferme Agri Lacombe — {e(g["footer"])}'
            f'</span><span>{e(DATA["contact"]["email"])} · {e(DATA["contact"]["web"])}</span></div>')
    hdr = (f'<div class="hdr"><div class="h">{LOGO}</div><div class="t">'
           f'<h1>{e(g["title"])}</h1><p>{e(g["subtitle"])}</p></div></div>')
    body = f"""
    <div class="page">{hdr}
      <h2>{e(g['logoTitle'])}</h2>
      <p class="lead">{e(g['logoLead'])}</p>
      <div class="logos">
        <div class="card"><div class="v" style="background:{C['cream']}"><div>{logo_img("original")}</div></div>
          <div class="cap"><b>{e(v['original'])}</b> — {e(g['caps']['original'])}</div></div>
        <div class="card"><div class="v"><div>{LOGO}</div></div>
          <div class="cap"><b>{e(v['transparent'])}</b> — {e(g['caps']['transparent'])}</div></div>
        <div class="card"><div class="v"><div>{logo_img("nb")}</div></div>
          <div class="cap"><b>{e(v['nb'])}</b> — {e(g['caps']['nb'])}</div></div>
      </div>
      <div class="zone">
        <div class="demo"><span class="x">X</span><div>{LOGO}</div></div>
        <div>
          <h2>{e(g['zoneTitle'])}</h2>
          <p class="lead" style="max-width:3.6in">{e(g['zoneText'])}</p>
          <h2>{e(g['sizesTitle'])}</h2>
          <table class="min">{"".join(f"<tr><td>{e(k)}</td><td><b>{e(val)}</b> {e(note)}</td></tr>" for k, val, note in g['sizes'])}</table>
        </div>
      </div>
      {foot}
    </div>
    <div class="page">{hdr}
      <h2>{e(d['colours']['title'])}</h2>
      <p class="lead">{e(d['colours']['lead'])}</p>
      <div class="sws">{swatches}</div>
      <h2 style="margin-top:22px">{e(g['usageTitle'])}</h2>
      <div class="rules">
        <div><h3>{e(g['do'])}</h3><ul>{dos}</ul></div>
        <div><h3>{e(g['dont'])}</h3><ul>{donts}</ul></div>
      </div>
      <div class="bads">{bad_html}</div>
      {foot}
    </div>"""
    return css, body


def page_html(css, body, lang="fr"):
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{css}</style>'
            f'</head><body>{body}</body></html>')


def print_pdf(html_text, name):
    src = BUILD / "print" / f"{name}.html"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(html_text)
    dst = OUT / "documents" / f"{name}.pdf"
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={dst}", src.as_uri())
    prev = OUT / "previews" / name
    prev.parent.mkdir(parents=True, exist_ok=True)
    run("pdftoppm", "-png", "-r", "60", "-f", "1", "-l", "1", "-singlefile", str(dst), str(prev))
    return dst


def screenshot(html_text, name, w, h):
    src = BUILD / "social" / f"{name}.html"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(html_text)
    dst = OUT / "reseaux-sociaux" / f"{name}.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
        f"--screenshot={dst}", src.as_uri())
    return dst


def social():
    base = "* { margin: 0; padding: 0; box-sizing: border-box } body { overflow: hidden }"
    d = DATA["fr"]
    cover = page_html(base + f"""
      body {{ width: 1640px; height: 624px; background: {C['cream']}; font-family: Inter, sans-serif }}
      .wrap {{ position: absolute; left: 280px; right: 280px; top: 0; bottom: 0; display: flex;
               align-items: center; gap: 56px }}
      .m {{ width: 470px; height: 420px; flex: none }} img {{ width: 100%; height: 100%; object-fit: contain }}
      h1 {{ font: 700 50px/1.12 Montserrat, sans-serif; color: {C['forest']} }}
      p {{ font-size: 25px; color: #3e4a35; margin-top: 18px }}
      .r {{ width: 90px; height: 6px; border-radius: 3px; background: {C['gold']}; margin-top: 26px }}
      .band {{ position: absolute; left: 0; right: 0; bottom: 0; height: 22px; background: {C['forest']} }}""",
                      f'<div class="wrap"><div class="m">{LOGO}</div><div>'
                      f'<h1>{e(d["pitch"]["headline"])}</h1>'
                      f'<p>Saint-Mathias-sur-Richelieu · Montérégie</p><div class="r"></div></div></div>'
                      f'<div class="band"></div>')
    screenshot(cover, "AgriLacombe_Facebook-couverture_1640x624", 1640, 624)


# --------------------------------------------------------------------------
# texts, readme, zip
# --------------------------------------------------------------------------

def texts(lang):
    d = DATA[lang]
    c = DATA["contact"]
    lines = [f"FERME AGRI LACOMBE — {d['slugTitle'].upper()}", "=" * 40, ""]
    for key in ("oneLine", "short", "long"):
        label = d["texts"][f"{key}Label"]
        lines += [label.upper(), "-" * len(label), d["texts"][key], ""]
    lines += [d["pitch"]["title"].upper(), "-" * len(d["pitch"]["title"]), d["pitch"]["headline"], "",
              d["pitch"]["elevator"], ""]
    lines += [f"• {p['title']} — {p['text']}" for p in d["pitch"]["points"]] + [""]
    lines += [d["facts"]["title"].upper(), "-" * len(d["facts"]["title"])]
    lines += [f"{k} : {v}" if lang == "fr" else f"{k}: {v}" for k, v in d["facts"]["items"]] + [""]
    lines += [d["contactBlock"]["title"].upper(), "-" * len(d["contactBlock"]["title"])]
    lines += address(lang) + contact_line(lang) + [c["facebook"], ""]
    dst = OUT / "textes" / f"AgriLacombe_Textes_{lang.upper()}.txt"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(lines))


README = """FERME AGRI LACOMBE — TROUSSE MÉDIA / MEDIA KIT
==============================================

1_Logos           Notre logo (PNG) : original, fond transparent, noir et blanc
2_Textes          Descriptions, argumentaire et fiche d’information (FR / EN / ES)
3_Documents       Fiche de présentation, affichette « Produit local », guide de marque (FR / EN / ES)
4_Reseaux-sociaux Photo de couverture Facebook

Utilisation : ces éléments peuvent servir à présenter ou promouvoir les produits
de la Ferme Agri Lacombe. Merci de ne pas modifier le logo (voir le guide de marque).
Toute autre utilisation demande notre accord écrit.

---
1_Logos           Our logo (PNG): original, transparent background, black and white
2_Textes          Descriptions, pitch and fact sheet (FR / EN / ES)
3_Documents       Fact sheet, "Local product" sign, brand guide (FR / EN / ES)
4_Reseaux-sociaux Facebook cover image

{web} · Facebook : {fb}
"""


def build_zip():
    dst = OUT / f"{KIT_NAME}.zip"
    dst.unlink(missing_ok=True)
    layout = [("logos", "1_Logos"), ("textes", "2_Textes"), ("documents", "3_Documents"),
              ("reseaux-sociaux", "4_Reseaux-sociaux")]
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        c = DATA["contact"]
        z.writestr(f"{KIT_NAME}/LISEZMOI.txt",
                   README.format(web=c["web"], fb=c["facebookName"]))
        for src, arc in layout:
            for f in sorted((OUT / src).rglob("*")):
                if f.is_file():
                    z.write(f, f"{KIT_NAME}/{arc}/{f.relative_to(OUT / src)}")
    return dst


def manifest():
    def entry(p):
        return {"path": "/" + str(p.relative_to(ROOT / "public")), "size": p.stat().st_size}

    logos = {key: entry(path) for key, path in LOGO_FILES.items()}
    docs = {lang: {key: {**entry(OUT / "documents" / f"{name}.pdf"),
                         "preview": entry(OUT / "previews" / f"{name}.png")["path"]}
                   for key, name in names.items()}
            for lang, names in DOC_FILES.items()}
    return {
        "palette": [{**c, "rgb": hex_to_rgb(c["hex"])} for c in PALETTE],
        "zip": entry(OUT / f"{KIT_NAME}.zip"),
        "logos": logos,
        "documents": docs,
        "social": {p.stem: entry(p) for p in sorted((OUT / "reseaux-sociaux").glob("*.png"))},
        "texts": {p.stem: entry(p) for p in sorted((OUT / "textes").glob("*.txt"))},
    }


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    for sub in ("print", "social"):  # keep build/fonts: BASE_CSS already points at it
        shutil.rmtree(BUILD / sub, ignore_errors=True)
    print("logos")
    assert logo_files.build(LOGO_SRC, OUT / "logos") == LOGO_FILES
    print("documents")
    for lang, names in DOC_FILES.items():
        print_pdf(page_html(*fiche(lang), lang), names["fiche"])
        print_pdf(page_html(*affichette(lang), lang), names["affichette"])
        print_pdf(page_html(*guide(lang), lang), names["guide"])
    print("social")
    social()
    print("texts")
    for lang in DOC_FILES:
        texts(lang)
    print("zip")
    build_zip()
    (ROOT / "src" / "data" / "media-kit-files.json").write_text(json.dumps(manifest(), indent=2) + "\n")
    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"done: {OUT.relative_to(ROOT)} ({total / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
