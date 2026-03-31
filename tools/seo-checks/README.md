# SEO quality checks (no Google credentials)

- **`seo_sanity_check.py`** — HTTP 200, `rel=canonical`, no `noindex` in robots meta, `og:title` (HTML only; sitemap URLs only get XML sniff).

**URLs** live in [`docs/seo-check-urls.txt`](../../docs/seo-check-urls.txt). Update when you ship important new pages.

**CI:** [`.github/workflows/seo-quality.yml`](../../.github/workflows/seo-quality.yml) runs this script, [lychee](https://github.com/lycheeverse/lychee) on the same list, and [Lighthouse](https://github.com/GoogleChrome/lighthouse) on key pages (artifacts uploaded).

Local:

```bash
cd /path/to/getcenty-marketing
python3 tools/seo-checks/seo_sanity_check.py
```
