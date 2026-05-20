# Competitive SERP snapshots

Dated archives of Google search results for our cluster head terms, so we can track relative position week over week and identify which competing pages to one-up.

## Cadence

- **Phase 1 first snapshot** (sprint exit criterion): one dated folder under this directory before the Day 30 retrospective.
- **Phase 2+**: refresh quarterly (Day 60 baseline, Day 90 retrospective), and after any significant SERP shake-up.

## What goes in a dated folder

```
docs/competitive-snapshots/YYYY-MM-DD/
├── README.md                              # index of terms + status
├── 01-<term-slug>.md                      # per-term notes + screenshot ref
├── 01-<term-slug>.png                     # screenshot of top 10 SERP
├── 02-<term-slug>.md
├── 02-<term-slug>.png
└── ... (8 terms total per snapshot)
```

PNG files are stored in this repo (typical size 300–600KB each; 8 PNGs ≈ 3–5MB per snapshot — acceptable for the quarterly cadence).

## Methodology

1. **Search context.** Use an incognito browser, Kenyan IP (or a VPN endpoint in Kenya), Google.co.ke, English. Record any deviation in the per-term markdown header.
2. **Capture.** Screenshot the **top 10 organic results** (excluding ads and shopping). Include the SERP features visible (People Also Ask, knowledge panel, snippets).
3. **Per-term notes.** Use the template per-term file in this folder. Capture:
   - **Dominant content type** (long-form pillar / vendor product page / comparison / news / forum / dictionary).
   - **Top 3 competitors** by URL with one-line characterisation each.
   - **Weakest result** — the page in the top 10 that we could realistically out-rank with the next refresh.
   - **One-up plan** — what Centy will ship (deeper / newer / better structured) to displace the weakest.
4. **Anonymous notes only.** Do not publish vendor pricing claims or commercial information drawn from competitor sites without verification. The snapshot is internal research.

## The 8 head terms (Phase 1)

Drawn from `docs/SEO-KEYWORD-MAP.csv` primary keywords across all four clusters. Update the list when new clusters open.

| # | Term | Cluster | Our URL |
|---|------|---------|---------|
| 1 | bulk M-Pesa payments Kenya | bulk_mpesa | blog.getcenty.com/bulk-mpesa-payroll-disbursements-kenya/ |
| 2 | casual workers payments Kenya | casual_pay | (Pillar 002 — pending publish) |
| 3 | expense management Kenya SMEs | expenses | (Pillar 003 — pending publish) |
| 4 | payroll software Kenya | payroll_sw | (Pillar 004 — pending publish) |
| 5 | best payroll software Kenya | payroll_sw | (Buyer guide 005 — pending publish) |
| 6 | NSSF SHIF NITA payroll deductions Kenya | payroll_sw | (Spoke 010 — pending publish) |
| 7 | M-Pesa B2C payroll disbursement Kenya | bulk_mpesa | (Spoke 007 — pending publish) |
| 8 | pay casual labourers M-Pesa Kenya | casual_pay | (Spoke 008 — pending publish) |

## How to fill the first dated folder

The folder `2026-05-20/` is pre-scaffolded with one markdown template per term (no PNGs yet — those are added when someone runs the captures). Open each `0N-<term-slug>.md`, fill in the **Findings** and **One-up plan** sections, drop the screenshot next to it as `0N-<term-slug>.png`, and update the snapshot README status table.

## Why we do this manually rather than automating

A clean SERP snapshot needs (a) a Kenyan vantage point, (b) an incognito session, (c) human judgement on the SERP shape including SERP features that screenshot APIs typically miss, and (d) plausible deniability of being a competitive-intelligence scraper. The 20 minutes per snapshot is well-spent; building a scraper that gets blocked once a quarter is not.

## Related

- `docs/SEO-KEYWORD-MAP.csv` — primary keywords per cluster.
- `docs/SEO-90-DAY-PLAN.md` — phase exit criteria that reference these snapshots.
- `docs/SEO-PHASE-1-SPRINT.md` — ticket `P1-W4-03` (this artefact).
