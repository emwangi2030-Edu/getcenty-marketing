# SEO — your checklist (not automated)

**Governance + keyword map:** [`docs/SEO-GOVERNANCE.md`](docs/SEO-GOVERNANCE.md), [`docs/SEO-KEYWORD-MAP.csv`](docs/SEO-KEYWORD-MAP.csv). **Sheets + GSC metrics automation:** [`tools/seo-automation/README.md`](tools/seo-automation/README.md).

---

## Already automated (GitHub Actions)

| Workflow | What it does |
|----------|----------------|
| **SEO — Sheets push & GSC report** (`seo-automation.yml`) | CSV → Sheet, GSC aggregates → `GSC_Automated_Log`; optional **`ping`** for sitemap submit + URL Inspection API. |
| **SEO quality** (`seo-quality.yml`) | Weekly + on push to listed paths: **sanity** (200, canonical, no `noindex`, `og:title`), **lychee** link check on [`docs/seo-check-urls.txt`](docs/seo-check-urls.txt), **Lighthouse** reports (artifacts) for www + blog + pillar post. |

Add new important URLs to `docs/seo-check-urls.txt` when you ship pages.

---

## Still manual (you do these)

1. **Bing Webmaster Tools** — [Import from Google](https://www.bing.com/webmasters) or verify `getcenty.com` / blog separately; submit `https://www.getcenty.com/sitemap.xml` and `https://blog.getcenty.com/sitemap_index.xml`.

2. **Google Search Console — Request indexing** — For high-priority new URLs, use URL Inspection → **Request indexing** (no API for that button; your **`ping`** workflow submits the sitemap instead).

3. **Deploy** — Run `deploy/rsync-marketing.sh` (or your pipeline) so the live host serves `robots.txt`, `sitemap.xml`, `.well-known/security.txt`, `404.html`, and all HTML/CSS/JS/assets.

4. **GSC property `https://www.getcenty.com/`** — If not done: verify, submit `https://www.getcenty.com/sitemap.xml`.

5. **404 handling** — In LiteSpeed / nginx / Apache, point 404 to `/404.html` on the marketing host so bots get the branded page.

6. **OG image weight** — Replace or recompress `og-image.png` if PageSpeed flags it (roughly 1200×630, target &lt; ~200–300 KB when practical).

7. **`lastmod` in `sitemap.xml`** — When you materially change the marketing site, update `<lastmod>` for affected URLs before deploy.

8. **Social profiles** — When you have public LinkedIn / X URLs for Centy, add them under `Organization.sameAs` in `index.html` JSON-LD.

9. **Analytics** (optional) — Privacy-friendly analytics if you want conversion data; not required for technical SEO.

10. **Content + links** — Publishing cadence, internal links between pillars/spokes, and outreach stay human workflows (see governance doc).
