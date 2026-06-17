# Local customizations on top of Chirpy

This file is the **merge-survival guide**: it records every deviation from upstream
`jekyll-theme-chirpy` so that when a future `git merge upstream/master` hits conflicts,
you know exactly what was changed, why, and how to re-apply it.

- **Base:** upstream **v7.5.0** (full theme repo). Remotes: `origin` = `qhuiw/qhuiw.github.io`, `upstream` = `cotes2020/jekyll-theme-chirpy`.
- **New files** (no upstream equivalent) → merges will *not* conflict on these. Listed for completeness.
- **⚠ Modified stock files** → these are the conflict-prone ones. Re-apply the described change after a merge.

## Conventions for keeping merges sane
- Custom feature **styles** live in `_sass/custom/_*.scss` (a dir that doesn't exist upstream → never conflicts) and are pulled in by a single `@use` line in `assets/css/jekyll-theme-chirpy.scss` (the theme's designated "append custom style" entry point).
- Custom **includes/layouts/tabs** are added as new files where possible. When a stock layout must be touched, the change is a small guarded block, documented below.

---

## Build / run notes
- Requires a UTF-8 locale or the gemspec's `git ls-files` chokes on non-ASCII (Chinese audio) filenames: `export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8`.
- `assets/lib` is the **`chirpy-static-assets` submodule** (self-hosted libs, no CDN). Fresh clones need `git clone --recursive` (or `git submodule update --init`). CI deploy must set `submodules: true`.
- Local build: `bundle install`; `npm install`; `npm run build` (generates `_sass/vendors/` + `assets/js/dist/`); `bundle exec jekyll serve`. Production check: `JEKYLL_ENV=production bundle exec jekyll build`.

---

## Phase 0–3 — base port

### ⚠ Modified stock files
- **`_config.yml`** — site identity merged in: `title`, `tagline`, `description`, `timezone: Europe/London`, `lang: en`, `github.username: qhuiw`, `social.*`, `comments.provider: giscus` (+ giscus repo/category IDs), `pageviews.provider: goatcounter`, `avatar: /assets/img/IMG_0019.JPG`, **`cdn: ""`** (no CDN), **`assets.self_host.enabled: true`**, and `jekyll-archives` permalinks → `/archives/tags/:name/` and `/archives/categories/:name/`.
- **`_data/contact.yml`** — sidebar socials: keep github + email, add LinkedIn (with url); youtube/rss left commented (youtube needs the custom sidebar — Phase 4).
- **`_data/authors.yml`** — appended `qianhui` author (used by `author: qianhui` in posts).
- **`_layouts/post.html`** — added a guarded references block between `<div class="content">` and `<div class="post-tail-wrapper">`:
  ```liquid
  {% if page.references_auto or page.references or page.references_data_key or page.references_markdown %}
    {% include references.html references=page.references data_key=page.references_data_key
       markdown=page.references_markdown heading=page.references_heading %}
  {% endif %}
  ```
- **`assets/img/favicons/*`** — replaced stock favicons with the site's own.

### New files
- `_includes/cite.html`, `_includes/references.html` — citation feature (inline `{% include cite.html n=N %}` markers + a bibliography list rendered from a post's `references:` front matter).
- `_tabs/about.md` (replaces stock About content), 9 posts under `_posts/2026-*.md`, media under `assets/{img,code,publications,slides}`.

> Note: stock demo posts (`2019-*`, `customize-the-favicon`) are still present — prune when ready. Two old posts were malformed and skipped; the now-fixed `2026-03-21-mte-architectural-support.md` is re-ported in Phase 4.

---

## Phase 4 — custom features

### Research / Publications tab
A `/research/` tab listing publications and talks as cards with inline PDF previews. Uses the **stock `layout: page`** (no custom layout).

**New files**
- `_tabs/research.md` — the page content (calls the card includes with per-item params).
- `_includes/research/publication-card.html` — publication card (thumb/iframe + title/meta/abstract/links).
- `_includes/research/talk-card.html` — talk card (same shape, "Abstract:" keyword).
- `_sass/custom/_research.scss` — card/grid/PDF-frame styles (pure CSS custom properties: `--link-color`, `--card-bg`, `--heading-color`, `--main-border-color` — all exist in v7.5.0).

**⚠ Modified stock files**
- `assets/css/jekyll-theme-chirpy.scss` — added `@use 'custom/research';` (after the main `@use`, before the "append your custom style" comment).

**Assets referenced:** `/assets/publications/usenixsecurity25-wang-nan.pdf`, `/assets/slides/2026*.{pdf,pptx}`, `/assets/slides/20221030-amd.{pdf,pptx}`.
