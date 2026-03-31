# Blog articles (source HTML)

WordPress post bodies are maintained here as HTML fragments for version control. Publish via WP-CLI on `blog.getcenty.com` (see runbook below) or paste into the block editor as a **Custom HTML** block (not recommended for long posts—prefer CLI import).

| File | Live URL | Primary keyword (Rank Math) |
|------|----------|----------------------------|
| `001-bulk-mpesa-payroll-disbursements-kenya.html` | [blog post](https://blog.getcenty.com/bulk-mpesa-payroll-disbursements-kenya/) | bulk M-Pesa payments Kenya |

## Definition of done (see `docs/SEO-GOVERNANCE.md`)

After first publish: add **featured image** (16:9), confirm **author** and **Organization** schema in Rank Math, request indexing in GSC, and link this pillar from the next cluster posts when they ship.

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
