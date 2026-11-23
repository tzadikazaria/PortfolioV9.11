# Tzadik Azaria — Portfolio V9.1 (refinement of V9)

Static site, no build step. Every link and asset path is relative, so it works from `/PortfolioV9/` on GitHub Pages (and from any folder or file://).

Upload the contents of this folder to the repo root (keep `.nojekyll`).

- `index.html` homepage · `campaign.html` `marketplace.html` `hatachana.html` `sambusak.html` · `about.html`
- `home.html` redirects to `index.html` (old links keep working)
- `styles.css` + `theme.css` (V8 foundation) · `v9.css` (V9 / V9.1 layer) · `app.js` · `fonts.css` (Archivo + Geist, embedded)
- `assets/` all project images, logo and CV
- `tools/build_v9.py` regenerates the HTML pages from one template (needs Pillow)

## Accent colour preview (the default site is unchanged: #E5091F)
- `accent-a.html` → Option A, current red #E5091F, with the accent used more sparingly
- `accent-b.html` → Option B, deeper red #BF3040, same reduced use, nothing else different
A small bar at the bottom-left switches between A / B and "Exit". The choice is remembered while you browse; "Exit" returns to the default site.
Remove the preview later by deleting the two `accent-*.html` files and the "accent preview" block at the top of `app.js` and the end of `v9.css`.


## V9.2 changes
- Hero rebuilt in a light, left-aligned style: large two-line headline, role label, curve with the weight/width twist, tagline + buttons row, hairline footer row. No red block, no floating elements.
- Black pill menu (white links, white "Download CV" button); mobile menu is a black overlay.
- Red is now a small accent (#BF3040): only the key curve point and the hero dot. The accent-preview pages were removed.
- The four case-study pages are long, image-led scrolls: big title + one line + metadata, full-width colour bands with minimal text, next-project band in the next project's colour. Same images, same labelling (Commercial work / Academic concept).
- Source of truth: tools/build_v9.py (run `python3 tools/build_v9.py`).

## V9.3 changes
- Type: Archivo + Geist replaced by Saira (variable, embedded). Display headings are bold, squared and uppercase; body text is Saira regular. The hero twist now animates Saira weight/width.
- Menu: smaller pill and logo (about 15px logo, 13.5px links).
- Hero: full-height, more space between label, headline, curve, tagline and the footer row.
- Case studies: larger paddings and gaps between bands, bigger spacing before the cover and next-project block, so the scroll is longer and airier.

## V9.4 changes
- Favicon: TZ monogram taken from the logo. favicon-tz-light.svg (black) for light browser themes, favicon-tz-dark.svg (white) for dark themes, apple-touch-icon-v94.png. New filenames avoid cached red icon; favicon.svg removed. Header logo and accent colour unchanged.
- Homepage grid: 12-column editorial composition. Campaign (wide) and Marketplace (tall, offset) lead; Hatachana (tall) and Give Me Sambusak (wide) mirror them. Larger, overlapping artwork inside the tiles. Titles, labels and links unchanged.
- Case studies: band padding and gallery gaps reduced; each project has its own composition (large + stacked supporting images, tall email beside banner and social, staggered phone screens, full-width icon strip, etc.). Images are never shown larger than their native width.
- Added previously unused work: Campaign (website mockup, social feed mockup), Marketplace (icon set, ingredient story, skincare benefits, razor refills).
- Source of truth: tools/build_v9.py.

## V9.5 changes
- Case-study pages: white background only, smaller type, text-led. Each page has numbered sections (Context / System / Outcome etc.) with the headings and copy from the original portfolio at tzadikazaria.com, next to or above the images. Home page, header, hero and footer unchanged.
- Home project cards: category line ("01 / Commercial design"), commercial/academic label, large uppercase title, the original one-line description, tags and a "View case study" link with a top rule. Layout of the grid is unchanged.
- Body copy on the case pages follows the original site; where the original could only be retrieved as a summary the wording is close but not verbatim (see chat).

## V9.6 changes
- Accent colour is now yellow (#F2C230), used as a fill (dots, curve key point, hover states, "Together." in the footer), never as text on light backgrounds. Focus outlines are ink/white for contrast.
- Case-study pages: removed the rules around the metadata under the title; text columns no longer stick or animate on scroll.
- Home: the project cards and grid are back to the V9.2 layout (featured Campaign + three cards).
- Site-wide: one container width, more white space between sections on home and About.

## V9.7 (interim) — mobile navigation fix
- Active nav link: yellow (--accent) on the dark mobile menu, same size/weight/spacing as other links (42px, 700), no scaling or background.
- Removed conflicting `[aria-current]` rules in theme.css / v9.css; desktop (≥701px) keeps the soft pill highlight.
- `aria-current="page"` on the current page (Home, About); `aria-current="true"` on Projects for project pages.
- Content expansion, Newsletter section, Tree Tower and Cupid's Helper drafts: pending the old-portfolio screenshots (not attached).

## V9.8 — content refinement
- Four case studies rewritten from the old portfolio copy (Campaign gets an "Email & newsletter design" section; Marketplace, Hatachana, Sambusak use concrete descriptions instead of generic outcomes).
- About: added Languages and one sentence on adapting work across channels.
- Draft pages (noindex, not linked from the homepage): `tree-tower.html`, `cupids-helper.html`. Dashed boxes mark original images still needed.
- Mobile navigation fix from V9.7 is unchanged.

## V9.9 — final refinement (superseded in V9.10)
- CV: portfolio, email and LinkedIn are clickable; summary reworded; employment dates unchanged. Source: `tools/cv.html`.
- Open Graph / Twitter preview images in `assets/og/` (built from existing project images by `tools/make_og.py`).
  **Before publishing, set your real site address** (needed for link previews): either run
  `SITE_URL=https://YOUR-NAME.github.io/PortfolioV9/ python3 tools/build_v9.py`
  or find-and-replace `https://SITE_URL_PLACEHOLDER/` with that address in all `.html` files.
- Open Graph: set your real site address before publishing (see above).

## V9.10 — cursor and footer
- Intro / loading animation removed.
- Custom cursor now on the whole site (mouse only): small yellow dot with a short movement trail, larger over links and buttons, and a "View project" circle over homepage project images. The normal cursor returns inside the image lightbox, on touch devices, and with ?cursor=off.
  Disable permanently: `FX_CURSOR = False` in `tools/build_v9.py`, then `python3 tools/build_v9.py`. Without Python: remove `class="fx-cursor"` from `<html>` and the `fx.js` script tag in each page.
  Reduced motion: no trail, dot follows instantly.
- Footer re-laid out: left-aligned title, then Email / Elsewhere / Site / Status columns and a copyright line.

## V9.11
- Custom cursor removed completely (fx.js, its CSS and the script tags are gone; the normal system cursor is used everywhere).

## V9.11 — cursor removed, Campaign images
- Custom cursor and its script/styles removed completely (the normal cursor is used everywhere).
- Campaign & Digital Design: seven original images added (see `tools/IMAGE_SOURCES.md` for source filenames and sizes), the low-resolution social/phone mockup replaced by the full-resolution one, and sections renumbered. Text of existing sections is unchanged apart from one added sentence in "Formats".
- `tools/add_images.py` optimises supplied originals into `assets/` and logs them.
