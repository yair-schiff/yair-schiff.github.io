Repository for my personal website, served by GitHub Pages at https://yair-schiff.github.io.

## Layout

- `index.html` – home page (intro + publications)
- `blog/index.html` – list of project pages, driven by `_data/projects.yml`
- `proseco/`, `discrete-diffusion-guidance/`, `caduceus/` – self-contained project pages
- `_layouts/`, `_includes/`, `assets/css/site.css`, `assets/js/site.js` – site template

## Adding a publication

Add an entry to `_data/research.json` (newest first):

```json
{
  "title": "Paper title",
  "authors": ["Yair Schiff*", "Co Author*", "Senior Author†"],
  "note": "*Equal contribution · †Equal senior authorship",
  "type": "conference",
  "selected": true,
  "venue": "NeurIPS 2026",
  "award": "Oral",
  "also": [{"venue": "XYZ @ ICML 2026", "url": "https://...", "award": "Workshop spotlight"}],
  "url": "https://arxiv.org/abs/...",
  "site": "/project/",
  "code": "https://github.com/...",
  "slides": "assets/pub_content/slides.pdf",
  "video": "https://...",
  "poster": "assets/pub_content/poster.png"
}
```

- `type` is one of `conference`, `journal`, `workshop`, `preprint` (drives the filter buttons).
- `selected: true` shows the paper under the default "Selected" filter.
- `award` is an accolade at the main venue; put workshop accolades on the matching `also` entry.
- `*` and `†` after an author name are rendered as superscripts; explain them in `note`.
- Only `title`, `authors`, `type`, `venue` and `url` are required.

## Local preview

```
bundle install
bundle exec jekyll serve
```
