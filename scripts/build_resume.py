# /// script
# requires-python = ">=3.10"
# dependencies = ["jinja2", "pyyaml"]
# ///
"""Build the PDF resume from the site's data files.

Education and experience come from _data/cv.yml, publications from
_data/research.json, and everything else from _data/resume.yml. The page is
rendered with Google Chrome (headless) so it uses the same fonts as the site.

    uv run scripts/build_resume.py              # writes the PDF that _config.yml's `cv` points to
    uv run scripts/build_resume.py --out x.pdf  # writes somewhere else
"""
import argparse
import datetime
import json
import subprocess
import tempfile
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent / "resume"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = "https://yair-schiff.github.io"
ME = "Yair Schiff"
STAR = "★"


def load_yaml(name):
    return yaml.safe_load((ROOT / "_data" / name).read_text())


def absolute(href):
    return href if "://" in href else SITE + "/" + href.lstrip("/")


def authors_html(authors):
    parts = []
    for a in authors:
        name = escape(a).replace("*", Markup("<sup>*</sup>")).replace("†", Markup("<sup>†</sup>"))
        parts.append(Markup("<strong>{}</strong>").format(name) if a.startswith(ME) else name)
    return Markup(", ").join(parts)


def extras_html(p):
    """Awards, extra venues, authorship notes and code/site links, on one line."""
    bits = []
    if p.get("award"):
        bits.append(Markup('<span class="award">{} {}</span>').format(STAR, p["award"]))
    for w in p.get("also", []):
        also = Markup("Also at {}").format(w["venue"])
        if w.get("award"):
            also += Markup(' <span class="award">({} {})</span>').format(STAR, w["award"])
        bits.append(also)
    if p.get("note"):
        bits.append(Markup('<span class="note">{}</span>').format(p["note"]))
    links = [(label, p[key]) for key, label in (("code", "code"), ("site", "site")) if p.get(key)]
    if links:
        bits.append(Markup('<span class="links">{}</span>').format(
            Markup(" · ").join(Markup('<a href="{}">{}</a>').format(absolute(h), l) for l, h in links)))
    return Markup('<span class="dot">|</span>').join(bits)


def pub_groups(pubs):
    groups = [("Preprints", ("preprint",)), ("Conference & journal papers", ("conference", "journal")),
              ("Workshop papers", ("workshop",))]
    out = []
    for label, types in groups:
        items = [{
            "title": p["title"],
            "url": absolute(p["url"]),
            "venue": p["venue"].replace(" preprint", ""),
            "authors": authors_html(p["authors"]),
            "extras": extras_html(p),
        } for p in pubs if p["type"] in types]
        if items:
            out.append({"label": label, "entries": items})
    return out


def main():
    config = yaml.safe_load((ROOT / "_config.yml").read_text())
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=ROOT / config["cv"].lstrip("/"))
    ap.add_argument("--html", type=Path, help="also save the rendered HTML here")
    args = ap.parse_args()

    env = Environment(loader=FileSystemLoader(HERE), autoescape=True)
    html = env.get_template("resume.html.j2").render(
        name=config["author"],
        css=Markup((HERE / "resume.css").read_text()),
        r=load_yaml("resume.yml"),
        cv=load_yaml("cv.yml"),
        pub_groups=pub_groups(json.loads((ROOT / "_data" / "research.json").read_text())),
        updated=datetime.date.today().strftime("%B %Y"),
    )
    if args.html:
        args.html.write_text(html)

    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "resume.html"
        page.write_text(html)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=15000",
            f"--user-data-dir={tmp}/profile", f"--print-to-pdf={args.out}", page.as_uri(),
        ], check=True, capture_output=True)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
