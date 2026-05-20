# Blog articles (source HTML)

WordPress post bodies are maintained here as HTML fragments for version control. Publish via WP-CLI on `blog.getcenty.com` (see runbook below) or paste into the block editor as a **Custom HTML** block (not recommended for long posts—prefer CLI import).

| File | Status | Live URL | Primary keyword (Rank Math) |
|------|--------|----------|----------------------------|
| `001-bulk-mpesa-payroll-disbursements-kenya.html` | live | [blog post](https://blog.getcenty.com/bulk-mpesa-payroll-disbursements-kenya/) | bulk M-Pesa payments Kenya |
| `002-casual-workers-payments-kenya.html` | draft | _pending publish_ → `https://blog.getcenty.com/casual-workers-payments-kenya/` | casual workers payments Kenya |
| `003-expense-management-kenya-smes.html` | draft | _pending publish_ → `https://blog.getcenty.com/expense-management-kenya-smes/` | expense management Kenya SMEs |
| `004-payroll-software-kenya.html` | draft | _pending publish_ → `https://blog.getcenty.com/payroll-software-kenya/` | payroll software Kenya |
| `005-payroll-payout-stack-kenya-2026.html` | draft | _pending publish_ → `https://blog.getcenty.com/payroll-payout-stack-kenya-2026/` | best payroll software Kenya |
| `006-kenya-payroll-month-end-checklist.html` | draft (linkable asset) | _pending publish_ → `https://blog.getcenty.com/kenya-payroll-month-end-checklist/` | Kenya payroll month-end checklist |
| `007-mpesa-b2c-payroll-disbursement-kenya.html` | draft (spoke) | _pending publish_ → `https://blog.getcenty.com/mpesa-b2c-payroll-disbursement-kenya/` | M-Pesa B2C payroll disbursement Kenya |
| `008-pay-casual-labourers-mpesa-kenya.html` | draft (spoke) | _pending publish_ → `https://blog.getcenty.com/pay-casual-labourers-mpesa-kenya/` | pay casual labourers M-Pesa Kenya |
| `009-petty-cash-management-alternatives-kenya.html` | draft (spoke) | _pending publish_ → `https://blog.getcenty.com/petty-cash-management-alternatives-kenya/` | petty cash management alternatives Kenya |
| `010-nssf-shif-nita-payroll-deductions-kenya.html` | draft (spoke, statutory) | _pending publish_ → `https://blog.getcenty.com/nssf-shif-nita-payroll-deductions-kenya/` | NSSF SHIF NITA payroll deductions Kenya |

## Definition of done (see `docs/SEO-GOVERNANCE.md`)

**Pillar 001:** Featured image is set (Unsplash — Carlos Muza, license in attachment description on WP). Author on the post: **Admin** (`centy_admin`). Still do: confirm **Organization** schema in Rank Math if needed, **Request indexing** in GSC (steps below), and link this pillar from the next cluster posts when they ship.

**Pillar 002 (draft):** Source HTML is in this folder; not yet published. Still to do before publish: (1) **statutory-reviewer sign-off** — the statutory-touchpoints section deliberately avoids rates and thresholds but still names PAYE / NSSF / SHIF / NITA / Housing levy; a Kenyan payroll advisor must confirm the framing before publish (see `SEO-GOVERNANCE.md` "Statutory / compliance review"); (2) featured image (16:9 ops photo, alt text in the HTML comment at top of file); (3) Rank Math meta — title, description, focus keyword `casual workers payments Kenya`, excerpt; (4) replace placeholder spoke anchors (currently all resolve to the pillar itself) with live URLs as each spoke ships; (5) update `docs/SEO-KEYWORD-MAP.csv` row for `casual_pay,pillar` to `status=live` with the live URL and `last_reviewed` date; (6) add the live URL to `docs/seo-check-urls.txt`; (7) Request indexing in GSC after publish.

**Pillar 003 (draft):** Source HTML is in this folder; not yet published. Same pre-publish checklist as Pillar 002 with category-specific notes: (1) **statutory-reviewer sign-off** — names KRA electronic invoicing (ETIMS/TIMS), VAT input claims, PAYE on benefits-in-kind, withholding tax, and foreign-currency spend; all rate-free but framing must be reviewed by a Kenyan tax advisor; (2) featured image (alt text in HTML comment); (3) Rank Math meta — focus keyword `expense management Kenya SMEs`; (4) replace placeholder spoke anchors for `petty cash management alternatives Kenya` and `employee expense claims approval workflow Kenya`; (5) `docs/SEO-KEYWORD-MAP.csv` row `expenses,pillar` → live with URL + date; (6) `docs/seo-check-urls.txt` update; (7) GSC indexing request.

**Pillar 004 (draft):** Source HTML is in this folder; not yet published. **Vendor-mention review** is the extra step for this pillar in addition to the usual checklist: the article names Workpay, WinguBox, Payroll.ke, Aren, Boya, Xero, QuickBooks, Zoho Books, and Centy at category level. No comparative feature or pricing claims are made about any non-Centy vendor — they are placed in a category bucket only. Before publish: (1) **legal review** of competitor framing (libel risk is low because no specific claims are made, but a second read by a reviewer comfortable with comparative content is prudent); (2) **statutory-reviewer sign-off** on the references to PAYE, NSSF, SHIF, NITA, Housing levy, and the Data Protection Act; (3) **Centy-positioning review** — the "Where Centy fits" section is deliberately not a sales pitch; product marketing should confirm the framing matches current positioning; (4) featured image; (5) Rank Math meta — focus keyword `payroll software Kenya`; (6) replace the buyer-guide placeholder anchor once that hub ships (P1-W3-02); (7) `docs/SEO-KEYWORD-MAP.csv` row `payroll_sw,pillar` → live with URL + date; (8) `docs/seo-check-urls.txt` update; (9) GSC indexing request.

**Buyer guide 005 (draft):** Source HTML is in this folder; not yet published. The article is framed as **methodology + reader-runnable evaluation matrix template**, NOT as a static vendor ranking — no comparative feature or pricing claims are made about any named vendor. Workpay, WinguBox, Payroll.ke, Aren, Boya, and Centy appear at category level only, with a verification rule attached ("no score above 3 without a documented source"). Before publish: (1) **legal review** — same risk profile as Pillar 004; the methodology framing reduces libel risk further but still warrants a comparative-content reviewer; (2) **statutory-reviewer sign-off** on the references to Kenyan statutory regimes; (3) **Centy-positioning review** — the "Where Centy fits in this matrix" section is honest, not promotional; product marketing should confirm; (4) featured image; (5) Rank Math meta — focus keyword `best payroll software Kenya`; (6) **confirm slug** — `payroll-payout-stack-kenya-2026` is the sprint-doc default; verify this matches the URL strategy before publish; (7) Pillar 004 should link to the live buyer-guide URL (currently a placeholder anchor in Pillar 004); (8) `docs/SEO-KEYWORD-MAP.csv` row `payroll_sw,spoke,best payroll software Kenya` → live with URL + date; (9) `docs/seo-check-urls.txt` update; (10) GSC indexing request.

**Linkable asset 006 (draft):** Printable Kenya payroll month-end checklist. Designed to print well from the browser (Cmd/Ctrl-P → Save as PDF) and to be co-brandable for accountants and HR consultants per the outreach plan in `SEO-90-DAY-PLAN.md`. Before publish: (1) **statutory-reviewer sign-off** — names PAYE / Housing levy / NSSF / SHIF / NITA categorically (no rates) plus withholding tax; (2) featured image; (3) Rank Math meta — focus keyword `Kenya payroll month-end checklist`; (4) decide whether to ship a downloadable PDF on day one (otherwise users print to PDF from the browser; document this in the WP post); (5) decide whether the "co-brandable on request" offer is operationally ready — if not, soften the wording; (6) `docs/SEO-KEYWORD-MAP.csv` add a new row for this linkable asset under cluster `payroll_sw` or a new `linkable_assets` cluster; (7) `docs/seo-check-urls.txt` update; (8) GSC indexing request; (9) **outreach**: identify and pitch the first 2 accountants / HR consultants per the sprint doc P1-W4-02 acceptance criteria.

**Spoke 007 — M-Pesa B2C payroll disbursement Kenya (draft):** Technical-operations spoke under the bulk-M-Pesa pillar. Same pre-publish checklist as the pillars; light statutory exposure (one paragraph). Confirm Safaricom product-naming references match current documentation before publish.

**Spoke 008 — Pay casual labourers M-Pesa Kenya (draft):** Working-cycle walk-through under the casual-pay pillar. Same pre-publish checklist; check that the cluster-link to the upcoming "daily wage payment Kenya" spoke is updated when that piece ships.

**Spoke 009 — Petty cash management alternatives Kenya (draft):** Six-week migration playbook under the expense pillar. Same pre-publish checklist with one extra step: **statutory-reviewer sign-off** specifically on the ETIMS / VAT-input-claim references in the "Watch" notes for cards and supplier-account migrations.

**Spoke 010 — NSSF SHIF NITA payroll deductions Kenya (draft, STATUTORY HIGH-SCRUTINY):** Rate-free framing guide under the payroll-software pillar. **Full statutory-reviewer sign-off REQUIRED** before publish — the article quotes no current numbers but defines purpose, scope, and payroll-cycle position for NSSF, SHIF, and NITA. Reviewer should confirm: (a) the framing of each scheme is current; (b) the scope statements (employee vs employer vs casual treatment) are honestly hedged; (c) the explicit "no rates" stance is acceptable for the channel. Add a visible "last reviewed by {name}, {date}" line in the WP post body before publish, and schedule a quarterly refresh in `docs/SEO-GOVERNANCE.md`.

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
