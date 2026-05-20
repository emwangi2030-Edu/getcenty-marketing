# Blog articles (source HTML)

WordPress post bodies are maintained here as HTML fragments for version control. Publish via WP-CLI on `blog.getcenty.com` (see runbook below) or paste into the block editor as a **Custom HTML** block (not recommended for long posts—prefer CLI import).

| File | Status | Live URL | Primary keyword (Rank Math) |
|------|--------|----------|----------------------------|
| `001-bulk-mpesa-payroll-disbursements-kenya.html` | live | [blog post](https://blog.getcenty.com/bulk-mpesa-payroll-disbursements-kenya/) | bulk M-Pesa payments Kenya |
| `002-casual-workers-payments-kenya.html` | draft | _pending publish_ → `https://blog.getcenty.com/casual-workers-payments-kenya/` | casual workers payments Kenya |

## Definition of done (see `docs/SEO-GOVERNANCE.md`)

**Pillar 001:** Featured image is set (Unsplash — Carlos Muza, license in attachment description on WP). Author on the post: **Admin** (`centy_admin`). Still do: confirm **Organization** schema in Rank Math if needed, **Request indexing** in GSC (steps below), and link this pillar from the next cluster posts when they ship.

**Pillar 002 (draft):** Source HTML is in this folder; not yet published. Still to do before publish: (1) **statutory-reviewer sign-off** — the statutory-touchpoints section deliberately avoids rates and thresholds but still names PAYE / NSSF / SHIF / NITA / Housing levy; a Kenyan payroll advisor must confirm the framing before publish (see `SEO-GOVERNANCE.md` "Statutory / compliance review"); (2) featured image (16:9 ops photo, alt text in the HTML comment at top of file); (3) Rank Math meta — title, description, focus keyword `casual workers payments Kenya`, excerpt; (4) replace placeholder spoke anchors (currently all resolve to the pillar itself) with live URLs as each spoke ships; (5) update `docs/SEO-KEYWORD-MAP.csv` row for `casual_pay,pillar` to `status=live` with the live URL and `last_reviewed` date; (6) add the live URL to `docs/seo-check-urls.txt`; (7) Request indexing in GSC after publish.

## WP-CLI import (server)

```bash
# From laptop: copy HTML
scp docs/blog-content/001-bulk-mpesa-payroll-disbursements-kenya.html user@host:/tmp/post.html

# On server (paths as deployed)
cd /home/blog.getcenty.com/public_html
wp post create /tmp/post.html \
  --post_title="…" \
  --post_name=slug-here \
  --post_status=publish \
  --post_category=TERM_ID \
  --post_excerpt="…" \
  --porcelain --allow-root
# Then Rank Math meta: rank_math_title, rank_math_description, rank_math_focus_keyword
wp litespeed-purge all --allow-root
```
