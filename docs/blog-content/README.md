# Blog articles (source HTML)

WordPress post bodies are maintained here as HTML fragments for version control. Publish via WP-CLI on `blog.getcenty.com` (see runbook below) or paste into the block editor as a **Custom HTML** block (not recommended for long posts—prefer CLI import).

| File | Status | Live URL | Primary keyword (Rank Math) |
|------|--------|----------|----------------------------|
| `001-bulk-mpesa-payroll-disbursements-kenya.html` | live | [blog post](https://blog.getcenty.com/bulk-mpesa-payroll-disbursements-kenya/) | bulk M-Pesa payments Kenya |
| `002-casual-workers-payments-kenya.html` | draft | _pending publish_ → `https://blog.getcenty.com/casual-workers-payments-kenya/` | casual workers payments Kenya |
| `003-expense-management-kenya-smes.html` | draft | _pending publish_ → `https://blog.getcenty.com/expense-management-kenya-smes/` | expense management Kenya SMEs |
| `004-payroll-software-kenya.html` | draft | _pending publish_ → `https://blog.getcenty.com/payroll-software-kenya/` | payroll software Kenya |

## Definition of done (see `docs/SEO-GOVERNANCE.md`)

**Pillar 001:** Featured image is set (Unsplash — Carlos Muza, license in attachment description on WP). Author on the post: **Admin** (`centy_admin`). Still do: confirm **Organization** schema in Rank Math if needed, **Request indexing** in GSC (steps below), and link this pillar from the next cluster posts when they ship.

**Pillar 002 (draft):** Source HTML is in this folder; not yet published. Still to do before publish: (1) **statutory-reviewer sign-off** — the statutory-touchpoints section deliberately avoids rates and thresholds but still names PAYE / NSSF / SHIF / NITA / Housing levy; a Kenyan payroll advisor must confirm the framing before publish (see `SEO-GOVERNANCE.md` "Statutory / compliance review"); (2) featured image (16:9 ops photo, alt text in the HTML comment at top of file); (3) Rank Math meta — title, description, focus keyword `casual workers payments Kenya`, excerpt; (4) replace placeholder spoke anchors (currently all resolve to the pillar itself) with live URLs as each spoke ships; (5) update `docs/SEO-KEYWORD-MAP.csv` row for `casual_pay,pillar` to `status=live` with the live URL and `last_reviewed` date; (6) add the live URL to `docs/seo-check-urls.txt`; (7) Request indexing in GSC after publish.

**Pillar 003 (draft):** Source HTML is in this folder; not yet published. Same pre-publish checklist as Pillar 002 with category-specific notes: (1) **statutory-reviewer sign-off** — names KRA electronic invoicing (ETIMS/TIMS), VAT input claims, PAYE on benefits-in-kind, withholding tax, and foreign-currency spend; all rate-free but framing must be reviewed by a Kenyan tax advisor; (2) featured image (alt text in HTML comment); (3) Rank Math meta — focus keyword `expense management Kenya SMEs`; (4) replace placeholder spoke anchors for `petty cash management alternatives Kenya` and `employee expense claims approval workflow Kenya`; (5) `docs/SEO-KEYWORD-MAP.csv` row `expenses,pillar` → live with URL + date; (6) `docs/seo-check-urls.txt` update; (7) GSC indexing request.

**Pillar 004 (draft):** Source HTML is in this folder; not yet published. **Vendor-mention review** is the extra step for this pillar in addition to the usual checklist: the article names Workpay, WinguBox, Payroll.ke, Aren, Boya, Xero, QuickBooks, Zoho Books, and Centy at category level. No comparative feature or pricing claims are made about any non-Centy vendor — they are placed in a category bucket only. Before publish: (1) **legal review** of competitor framing (libel risk is low because no specific claims are made, but a second read by a reviewer comfortable with comparative content is prudent); (2) **statutory-reviewer sign-off** on the references to PAYE, NSSF, SHIF, NITA, Housing levy, and the Data Protection Act; (3) **Centy-positioning review** — the "Where Centy fits" section is deliberately not a sales pitch; product marketing should confirm the framing matches current positioning; (4) featured image; (5) Rank Math meta — focus keyword `payroll software Kenya`; (6) replace the buyer-guide placeholder anchor once that hub ships (P1-W3-02); (7) `docs/SEO-KEYWORD-MAP.csv` row `payroll_sw,pillar` → live with URL + date; (8) `docs/seo-check-urls.txt` update; (9) GSC indexing request.

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
