# SEO — your checklist (not automated)

**Full program (blog + governance, reporting, refresh rules):** see [`docs/SEO-GOVERNANCE.md`](docs/SEO-GOVERNANCE.md) and [`docs/SEO-KEYWORD-MAP.csv`](docs/SEO-KEYWORD-MAP.csv). **Automated Sheet sync + GSC log:** [`tools/seo-automation/README.md`](tools/seo-automation/README.md) (terminal + GitHub Actions).

Do these in order when you’re ready; everything else is already in the static site.

1. **Deploy** — Run `deploy/rsync-marketing.sh` (or your pipeline) so the live host serves `robots.txt`, `sitemap.xml`, `.well-known/security.txt`, `404.html`, and all HTML/CSS/JS/assets.

2. **Google Search Console** — Add property `https://www.getcenty.com/`, verify (DNS TXT or HTML file), then submit sitemap `https://www.getcenty.com/sitemap.xml`.

3. **Bing Webmaster Tools** (optional) — Import from Google or verify separately; submit the same sitemap.

4. **404 handling** — In LiteSpeed / nginx / Apache, set the error document for 404 to `/404.html` so visitors (and bots) get the branded page. *Until this is set, random URLs may show a generic server 404.*

5. **OG image weight** — Replace or recompress `og-image.png` if PageSpeed flags it (target roughly 1200×630 and &lt; 200–300 KB if possible).

6. **`lastmod` in `sitemap.xml`** — When you materially change the site, update the `<lastmod>` dates (YYYY-MM-DD) for affected URLs before redeploying.

7. **Social profiles** — When you have public LinkedIn / X URLs for Centy, add them under `Organization.sameAs` in `index.html` JSON-LD (currently omitted on purpose).

8. **Analytics** (optional) — Add privacy-friendly analytics if you want conversion data; not required for technical SEO.
