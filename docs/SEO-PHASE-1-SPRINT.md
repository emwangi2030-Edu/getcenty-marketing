# Phase 1 sprint — Days 1–30: Foundation & first strikes

Operational ticket plan for [`SEO-90-DAY-PLAN.md`](SEO-90-DAY-PLAN.md) Phase 1. Each ticket has acceptance criteria so it can be picked up, executed, and closed without re-reading the plan. Update [`SEO-KEYWORD-MAP.csv`](SEO-KEYWORD-MAP.csv) `status` + `url` + `last_reviewed` as tickets close, and assign owners in [`SEO-GOVERNANCE.md`](SEO-GOVERNANCE.md).

**Phase 1 exit criteria (from the 90-day plan):**

- 4 pillar hubs live + 1 buyer guide live
- GSC `www` + `blog` properties clean (no coverage errors on tracked URLs)
- ≥ 8 new indexed URLs with purpose (pillars + supporting posts)
- ≥ 1 linkable asset shipped (Kenya payroll month-end checklist)
- `SEO-KEYWORD-MAP.csv` rows populated with live URLs for everything shipped

**Status today:** Pillar #1 (bulk M-Pesa payroll disbursements Kenya) is **live** on `blog.getcenty.com`. Phase 0 closed the technical gaps (dual-property GSC ping, sitemap `<lastmod>` refresh, widened `seo-check-urls.txt`).

---

## Owners — assign before Week 1

Fill into [`SEO-GOVERNANCE.md`](SEO-GOVERNANCE.md) "Owners" table; tickets below reference these roles.

| Role | Owner | Backup |
|------|-------|--------|
| Content lead (blog) | TBD | TBD |
| Technical SEO (sitemaps, CWV, redirects) | TBD | TBD |
| GSC + reporting | TBD | TBD |
| Statutory / compliance reviewer | TBD | TBD |
| Linkable-asset designer | TBD | TBD |

If a single person holds multiple roles for this sprint, list the same name; do not leave blank.

---

## Week 1 — Measurement & technical closure

Goal: baseline measurement + close any remaining technical gaps so content lands on clean foundations.

### P1-W1-01 — GSC property hygiene
- **Owner:** GSC + reporting
- **Acceptance:**
  - Both `https://www.getcenty.com/` and `https://blog.getcenty.com/` are verified URL-prefix properties.
  - Coverage report for each property has **zero** unexplained errors on URLs listed in [`docs/seo-check-urls.txt`](seo-check-urls.txt).
  - Service account `centy-seo-sync@...` has **Full** access on both properties (so the dual-property `ping` job in `seo-automation.yml` succeeds).
- **Deps:** none.
- **Notes:** `SEO-YOU-DO.md` items #4 (www verify) and #1 (Bing) sit alongside this; Bing can slip to Week 2.

### P1-W1-02 — Baseline export (last 28 days)
- **Owner:** GSC + reporting
- **Acceptance:**
  - From each GSC property, export **Queries** and **Pages** for last 28 days as CSV.
  - Files saved to `docs/google-drive-export/baseline-YYYY-MM-DD/` with both property prefixes in filenames.
  - Row in [`SEO-GOVERNANCE.md`](SEO-GOVERNANCE.md) "Reporting" section records the export date + path; used as the day-0 benchmark for the Day 30 / 60 / 90 north-star metrics in the 90-day plan.
- **Deps:** P1-W1-01.

### P1-W1-03 — Marketing site internal links to blog + money sections
- **Owner:** Technical SEO
- **Acceptance:**
  - `index.html` links to at least: blog home, pillar #1 (bulk M-Pesa), and the primary commercial pages.
  - Anchor text is descriptive (not "click here", not exact-match keyword stuffing).
  - `seo-quality.yml` sanity check passes on `index.html` (200, canonical, `og:title`, no `noindex`).
- **Deps:** none. Independent from P1-W1-01.

### P1-W1-04 — Sitemap `lastmod` discipline
- **Owner:** Technical SEO
- **Acceptance:**
  - Phase 0 already bumped `sitemap.xml` to `2026-05-20`. Going forward, any PR that materially changes a www page must also touch the matching `<lastmod>`.
  - Note the convention in [`SEO-YOU-DO.md`](../SEO-YOU-DO.md) item #7 (already present; leave as-is).
- **Deps:** none. Process-only; no code change required this week.

### P1-W1-05 — Blog schema sanity (Rank Math)
- **Owner:** Content lead
- **Acceptance:**
  - Rank Math **Organization** + **Person** schema reflects real entities (no placeholder bios).
  - No FAQ schema unless visible FAQs are on the page.
  - Pillar #1 URL passes [Rich Results Test](https://search.google.com/test/rich-results) with no critical errors.
- **Deps:** none.

---

## Week 2 — Pillars 2 + 3 (ship, don't polish forever)

Goal: two new ~3k-word pillars live. Plan calls these Pillars #1–#2; #1 is already shipped, so Week 2 actually delivers Pillars #2 and #3 of the cluster set.

### P1-W2-01 — Pillar #2: Casual workers payments Kenya
- **Owner:** Content lead (statutory reviewer signs off legal claims)
- **Keyword map row:** `casual_pay,pillar,casual workers payments Kenya` ([`SEO-KEYWORD-MAP.csv`](SEO-KEYWORD-MAP.csv) row 5)
- **Acceptance:**
  - ~3,000 words, published on `blog.getcenty.com/casual-workers-payments-kenya/` (slug to confirm).
  - Sections cover: who counts as casual, records you must keep, M-Pesa workflow for daily/weekly pay, statutory touchpoints (NSSF / SHIF where applicable), reconciliation tips, common mistakes.
  - Links to: Pillar #1 (bulk M-Pesa), at least 2 future-spoke anchor placeholders (use real URLs once spokes ship), Centy product page where relevant.
  - Passes Publishing DOD in [`SEO-GOVERNANCE.md`](SEO-GOVERNANCE.md).
  - `SEO-KEYWORD-MAP.csv` updated: `status=live`, `url=...`, `last_reviewed=YYYY-MM-DD`.
  - `docs/seo-check-urls.txt` updated to include the new URL.
- **Deps:** P1-W1-01 (so we can immediately request indexing).
- **Risk:** Labour law claims — flag any specific statutory wording for statutory reviewer before publish.

### P1-W2-02 — Pillar #3: Expense management Kenya SMEs
- **Owner:** Content lead
- **Keyword map row:** `expenses,pillar,expense management Kenya SMEs` (row 8)
- **Acceptance:**
  - ~3,000 words at `blog.getcenty.com/expense-management-kenya-smes/`.
  - Sections: policy basics, approvals, petty cash alternatives, employee claims workflow, mobile money + bank feed reconciliation, fraud red flags.
  - Internal links to: Pillar #1, Pillar #2 (once shipped), Centy expenses product page.
  - Publishing DOD ✓. Keyword map + `seo-check-urls.txt` updated.
- **Deps:** P1-W1-01.

### P1-W2-03 — Keyword map URLs populated for shipped pillars
- **Owner:** Content lead
- **Acceptance:** [`SEO-KEYWORD-MAP.csv`](SEO-KEYWORD-MAP.csv) has live URLs for every Week 2 deliverable.
- **Deps:** P1-W2-01, P1-W2-02.

---

## Week 3 — Pillar #4 + buyer guide

### P1-W3-01 — Pillar #4: Payroll software Kenya (how to choose)
- **Owner:** Content lead
- **Keyword map row:** `payroll_sw,pillar,payroll software Kenya` (row 11)
- **Acceptance:**
  - ~3,000 words at `blog.getcenty.com/payroll-software-kenya/`.
  - Framed as **criteria** ("how to choose"), not "Centy is #1". Criteria include: M-Pesa native, statutory deductions support, casual-pay support, accounting integration, cost transparency, support SLAs.
  - Centy wins only on substantiated differentiation; Workpay / WinguBox / Payroll.ke / Aren / Boya mentioned where relevant and **factually**.
  - Publishing DOD ✓.
- **Deps:** Statutory reviewer availability.

### P1-W3-02 — Buyer guide hub
- **Owner:** Content lead + statutory reviewer
- **Keyword map row:** `payroll_sw,spoke,best payroll software Kenya` (row 12) — **buyer guide; fair comparison**
- **Acceptance:**
  - URL: `blog.getcenty.com/payroll-payout-stack-kenya-2026/` (slug to confirm).
  - Includes a structured comparison table (not opinion-only) — feature matrix with sources cited where pricing/feature claims are made.
  - "Not legal/tax advice" disclaimer on statutory references.
  - Internal links to Pillars #1–#4.
- **Deps:** P1-W3-01 ideally first so it can link back.

### P1-W3-03 — Update keyword map + sitemap.xml
- **Owner:** Technical SEO
- **Acceptance:**
  - Keyword map URLs populated for Week 3 deliverables.
  - `sitemap.xml` not changed (those URLs live on `blog.getcenty.com`, indexed via Rank Math sitemap), but `docs/seo-check-urls.txt` updated.
- **Deps:** P1-W3-01, P1-W3-02.

---

## Week 4 — Cluster saturation + first link push

### P1-W4-01 — 4 supporting articles (one per cluster)
- **Owner:** Content lead
- **Acceptance:** One spoke article per cluster, each ~1,200–1,800 words, drawn from these keyword map rows:
  - `bulk_mpesa,spoke,M-Pesa B2C payroll disbursement Kenya` (row 3)
  - `casual_pay,spoke,pay casual labourers M-Pesa Kenya` (row 6) **or** `daily wage payment Kenya` (row 7)
  - `expenses,spoke,petty cash management alternatives Kenya` (row 9) **or** `employee expense claims approval workflow Kenya` (row 10)
  - `payroll_sw,spoke,NSSF SHIF NITA payroll deductions Kenya` (row 13) — **statutory; high scrutiny**
- Each links to its pillar + at least 1 sibling. Publishing DOD ✓. Keyword map updated.
- **Deps:** Pillars from Weeks 2–3 live.

### P1-W4-02 — Linkable asset: Kenya payroll month-end checklist
- **Owner:** Linkable-asset designer + Content lead
- **Acceptance:**
  - Printable HTML + downloadable PDF at `blog.getcenty.com/kenya-payroll-month-end-checklist/` with a `Download PDF` button.
  - Lists the actual steps an SME payroll owner runs each month end (PAYE, NSSF, SHIF, NITA, Housing levy, M-Pesa reconciliation, payslip distribution, journal posting).
  - Mentioned in Pillar #1 and Pillar #4 as a "useful tool" link.
  - Outreach list seeded: 2 named accountants / HR consultants to pitch (names go in [`SEO-GOVERNANCE.md`](SEO-GOVERNANCE.md) "Off-site" section, not in this doc).
- **Deps:** Pillar #1 and #4 live so they can reference the asset.

### P1-W4-03 — Competitive intel snapshot
- **Owner:** Content lead
- **Acceptance:**
  - For each of 8 head terms (pick from keyword map primary keywords across all clusters), screenshot the SERP top 10 to `docs/competitive-snapshots/YYYY-MM-DD/`.
  - One short markdown note per term: dominant content type, weakest result, the "one-up" Centy will ship (deeper / newer / better structured).
  - Feeds Week 5+ planning.
- **Deps:** none.

---

## Cross-cutting risks (carry through every week)

- **Overclaiming statutory facts.** Anything that quotes a rate, threshold, or deadline gets statutory-reviewer sign-off before publish.
- **AI-slop at scale.** Every long-form piece passes a human read-through and the Publishing DOD.
- **Cannibalisation.** Before publishing, search the keyword map for an existing URL targeting the same primary keyword. If one exists, merge or differentiate intent.
- **Message match.** Each blog post linking to a Centy page must align on promise so bounce rate stays inferable as "good".
- **Cheap links / PBNs prohibited.** Outreach is human + relationship-based.

---

## Daily 5-minute hygiene (any owner)

- New URL shipped → add to `docs/seo-check-urls.txt` + keyword map.
- Statutory change spotted → schedule a refresh ticket; update `last_reviewed` on affected rows.
- Coverage error in GSC → file ticket under `P1-W*-99` (ad-hoc) and fix before publishing more.

---

## Day 30 retrospective (90 min, end of Phase 1)

Hold against the Day 30 column of the north-star table in [`SEO-90-DAY-PLAN.md`](SEO-90-DAY-PLAN.md):

1. Clicks vs baseline.
2. Impressions per cluster — any cluster already separating?
3. URLs ranking 4–20 — ≥10 hit?
4. Pillars live: 4 + buyer guide ✓?
5. Earned links: 1–2?
6. What to keep / kill in Phase 2 cadence.

Outputs feed the Phase 2 ticket draft (Days 31–60).
