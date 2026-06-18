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
- **CI gates** (run on push to *any* branch, incl. `wip`): `lint-scss` (`npm run lint:scss` — custom SCSS must conform; auto-fix via `npm run lint:fix:scss`), `lint-js` (`npm run lint:js`), and `ci` (`bash tools/test.sh` = production build + **htmlproofer internal-link check**). Run all three locally before pushing. Note: because `cdn` is empty, htmlproofer treats former-CDN image paths as internal — any post relying on CDN-hosted images will fail it.

---

## Phase 0–3 — base port

### ⚠ Modified stock files
- **`_config.yml`** — site identity merged in: `title`, `tagline`, `description`, `timezone: Europe/London`, `lang: en`, `github.username: qhuiw`, `social.*`, `comments.provider: giscus` (+ giscus repo/category IDs), `pageviews.provider: goatcounter`, `avatar: /assets/img/IMG_0019.JPG`, **`cdn: ""`** (no CDN), **`assets.self_host.enabled: true`**. (jekyll-archives permalinks kept at v7.5.0 **stock** `/tags/:name/` + `/categories/:name/` — we use the stock tag/category layouts/links, so the old `/archives/...` scheme would break ~1000 internal links. Restoring `/archives/...` would require editing every link-generating stock file — deferred to a future custom-archives port.)
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
- **`_data/locales/en.yml`** — added `tabs.portfolio`, `tabs.research`, and `tabs."about me"`. v7.5.0 builds each tab's `<title>` via `site.data.locales[lang].tabs[{{ page.title | downcase }}]`, so **every custom tab must add a matching key here** or its browser-tab `<title>` renders blank. The stock convention is *tab title == filename == key*; `_tabs/about.md` deliberately keeps the title **"About Me"** (for voice), which is why it needs the extra `"about me"` key instead of riding the stock `tabs.about`.

### New files
- `_includes/cite.html`, `_includes/references.html` — citation feature (inline `{% include cite.html n=N %}` markers + a bibliography list rendered from a post's `references:` front matter).
- `_tabs/about.md` (replaces stock About content), 9 posts under `_posts/2026-*.md`, media under `assets/{img,code,publications,slides}`.

> Note: stock demo posts (`2019-*`, `customize-the-favicon`) were **removed** — their demo images are hosted on the chirpy-img CDN, which our no-CDN setup disables, so they became broken internal links (htmlproofer failed). Two old posts were malformed and skipped; the now-fixed `2026-03-21-mte-architectural-support.md` is re-ported in Phase 4.

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

### Portfolio / audio-lyrics-transcript tab
A `/portfolio/` tab showcasing vocal covers as audio cards with a karaoke-style synced transcript (zh/en toggle), waveform canvas, and download-protected `<audio>`.

**New files**
- `_tabs/portfolio.md` — uses **custom `layout: portfolio`**; front matter `audio_cards: true`, `display_title`, `subtitle`. Body has a `<section class="audio-showcase">` with `portfolio-audio-card.html` includes.
- `_layouts/portfolio.html` — **custom layout** (`layout: page` parent). Wraps content in `#portfolio` and carries the **inline transcript-sync `<script>`** (gated by `page.audio_cards`): fetches the transcript JSON, syncs lines to audio time, handles the zh/en toggle and the canvas visualizer. Includes the **stock** `lang.html` (harmless). No rollup/JS-build change needed (JS is inline).
- `_includes/portfolio-audio-card.html` — one audio card: `<audio>` + `<details>` transcript block with zh/en toggle + empty `<ul class="transcript-lines">` (filled by the inline JS). Reads `data-transcript*` attributes.
- `_sass/custom/_portfolio.scss` — card/transcript/visualizer styles (pure CSS custom properties).

**⚠ Modified stock files**
- `assets/css/jekyll-theme-chirpy.scss` — added `@use 'custom/portfolio';`.

**Assets:** `assets/audio/*.m4a` (3, ~22 MB, Chinese filenames — needs UTF-8 locale), `assets/transcripts/*.json` (AI), `assets/trans-official/*.json` (official lyrics), `assets/lyrics/*.txt`. Transcript JSON shape: `{ track, source, zh:[{start,text}], en:[{start,text}] }`.

> `lang.html` and `language-alias.html` are **stock** v7.5.0 includes (lang detection + code-block language-alias display), *not* a custom multilingual layer — nothing to port there.
> ⚠ Browser spot-check needed for the JS-driven bits: audio playback, transcript karaoke sync, zh/en toggle, waveform visualizer.

### Posts / Archives taxonomy routing  ⚠ (largest structural drift)
Stock Chirpy has 3 separate tabs (Archives, Categories, Tags) with taxonomy at `/categories/` and `/tags/`. This site instead has **one "Posts" tab** (post timeline + inline Categories/Tags summaries) and routes **all taxonomy under `/archives/`**. Getting this consistent touches several stock files — re-apply all of them together after an upstream merge, or the breadcrumbs/links break.

**New files**
- `_archives/categories.md` (`layout: categories`) → index page at `/archives/categories/`.
- `_archives/tags.md` (`layout: tags`) → index page at `/archives/tags/`.

**Deleted stock files**
- `_tabs/categories.md`, `_tabs/tags.md` — replaced by the `/archives/` index pages above.

**⚠ Modified stock files** (all needed for links to resolve — htmlproofer enforces this):
- `_config.yml` — (a) added the `archives` collection (`output: true`, `permalink: /archives/:title/`); (b) `jekyll-archives.permalinks` → `tag: /archives/tags/:name/`, `category: /archives/categories/:name/` (stock is `/tags/:name/`, `/categories/:name/`).
- `_tabs/archives.md` — `order: 3`, custom `icon`; title kept as stock **"Archives"** so nav + `<title>` + breadcrumb stay consistent (no extra locale key needed — uses stock `tabs.archives`).
- `_layouts/page.html` — heading condition extended to `page.layout == 'categories' or page.layout == 'tags'`, so the `/archives/categories/` and `/archives/tags/` index pages (in the `archives` collection) render their `<h1>` dynamic-title. Without this they had **no heading** (looked bare).
- `_layouts/archives.html` — also added an `<h2>Posts</h2>` above the timeline, so the Archives page reads as three sibling sections: **Posts / Categories / Tags**.
- `_layouts/archives.html` — appended inline **Categories** + **Tags** sections (headings link to `/archives/categories/` and `/archives/tags/`; per-item links to `/archives/categories|tags/:name/`).
- `_layouts/categories.html` — per-category link prefix `/categories/` → `/archives/categories/` (2 spots).
- `_layouts/tags.html` — per-tag link prefix `/tags/` → `/archives/tags/` (1 spot).
- `_layouts/post.html` — post-tail category link → `/archives/categories/…`, tag link → `/archives/tags/…`.
- `_includes/trending-tags.html` — tag link prepend `/tags/` → `/archives/tags/`.
- `_includes/topbar.html` — **breadcrumb** rewritten to accumulate the *cumulative* path (and handle `categories`/`tags` layouts), so nested `/archives/categories/<name>/` breadcrumbs link to each ancestor correctly instead of `/categories/`. (Only the breadcrumb `<nav>` block was changed — the old repo's other topbar tweaks were intentionally NOT ported.)

### Sidebar & topbar — mode-toggle move + extra social icons
The dark/light **mode-toggle was moved from the sidebar into the topbar** (right end), and the sidebar contact list supports more social networks.

**⚠ Modified stock files**
- `_includes/sidebar.html` — (a) mode-toggle button commented out (now in the topbar); (b) contact `{% case entry.type %}` extended with **youtube / facebook / instagram / linkedin / mastodon** branches that build the URL from `site.<type>.username` (stock only handles github/twitter/email).
- `_includes/topbar.html` — mode-toggle button added after the search controls; breadcrumb `<nav>` given `class="flex-grow-1"` and `#topbar` dropped `justify-content-between` so the toggle sits at the right. (The breadcrumb cumulative-path change is under the Archives section above.)
- `_config.yml` — added `youtube:` (username `qianhui8571`, channel_id) and `linkedin:` (username `qianhui-w`).
- `_data/contact.yml` — enabled the `youtube` entry; switched `linkedin` to the username form (dropped its explicit `url`, now built from `site.linkedin.username`).

> The `#mode-toggle` JS keys off the element id, so relocating it needs no JS change. The old repo's `<h1>` site-title tweak was **not** ported (minor).

### Sidebar avatar + title — larger & centred
**New file**
- `_sass/custom/_sidebar.scss` — (a) enlarges `#avatar` to `8.5rem` + `object-fit: cover` (crops a non-square photo cleanly); (b) centres the profile block via symmetric `.profile-wrapper` padding + `margin: auto` on `#avatar`; (c) centres `.site-title` / `.site-subtitle` with `margin: auto` — needed because upstream sets `.site-title { width: fit-content }`, so the shrink-wrapped box otherwise sits left even with `text-align: center`. Imported via `@use 'custom/sidebar'` in `assets/css/jekyll-theme-chirpy.scss`. **CSS-only** — does *not* touch `sidebar.html` (lower-drift than the old repo's markup edits).

**⚠ Modified stock file**
- `_data/locales/en.yml` — footer credit `meta:` changed "Using the :THEME theme…" → **"Adapted from the :THEME theme for :PLATFORM."** (the site adapts Chirpy rather than using it as-is).

### Misc data/content
- **`_data/share.yml`** — Telegram **commented out** (kept, not deleted); LinkedIn + Weibo uncommented/enabled.
- **`_posts/2026-03-21-mte-architectural-support.md`** — re-ported (was malformed/0-byte during the base port; user fixed it upstream).

### Local-only reference posts (demos visible in preview, hidden when deployed)
The bundled Chirpy demo posts are kept as a writing/structure reference, but never appear on the live site.

**New files**
- `_plugins/hide-in-production.rb` — a `:site, :post_read` hook that drops any post with front-matter `hidden_in_prod: true` from the build **when `JEKYLL_ENV=production`** (excludes them from home, archives, categories/tags, feed, and their own pages).
- The 4 demo posts `_posts/2019-*.md` (text-and-typography, write-a-new-post, getting-started, customize-the-favicon) each carry `hidden_in_prod: true`.

**Behaviour**
- Local preview (`bundle exec jekyll serve`, default `JEKYLL_ENV=development`) → demos **visible** (reference while drafting).
- Production (deploy + `tools/test.sh`/CI, which set `JEKYLL_ENV=production`) → demos **hidden**.
- Bonus: the demos' hero images come from the Chirpy CDN (`/commons/...`) and 404 under `cdn: ""`; hiding them in production keeps **htmlproofer** green (those broken links never reach the prod build it checks). The demo images also won't load in *local* preview — they're kept for structure/front-matter reference, not their images.
- ⚠ Run htmlproofer only on a **production** build (`tools/test.sh`); a dev build includes the demos' broken `/commons/` links.
