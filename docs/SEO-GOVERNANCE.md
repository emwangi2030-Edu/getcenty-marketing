# SEO governance — Centy (marketing site + blog)

Living document. Update owners, dates, and URLs as the team changes. **Review quarterly.**

---

## Scope

| Surface | URL | Role |
|--------|-----|------|
| Marketing (static) | `https://www.getcenty.com/` | Brand, product, conversion |
| Blog (WordPress) | `https://blog.getcenty.com/` | Organic acquisition, topical authority |
| App | `https://app.centyhq.com/` | Product (SEO via marketing/blog links; separate backlog) |

---

## Owners (fill in)

| Area | Owner | Backup |
|------|--------|--------|
| GSC / indexing | | |
| Content calendar (blog) | | |
| Statutory / compliance review (factual) | | |
| Technical (sitemaps, redirects, CWV) | | |
| Analytics / reporting | | |

---

## Tools

- **Google Search Console** — Properties: `www.getcenty.com`, `blog.getcenty.com` (or domain property if used).
- **Bing Webmaster Tools** (optional) — Import or verify; submit sitemaps.
- **Analytics** — If used: document property ID and consent approach in privacy policy.

**Sitemaps to submit**

- `https://www.getcenty.com/sitemap.xml`
- `https://blog.getcenty.com/sitemap_index.xml` (Rank Math)

---

## Pillars & clusters (blog)

Canonical pillar themes (each gets one **hub** URL + supporting posts — see `SEO-KEYWORD-MAP.csv`):

1. Bulk M-Pesa / payroll disbursements (Kenya)
2. Casual / daily labour payments & records
3. Expense management & spend control (SMEs)
4. Payroll software & statutory compliance (Kenya)

**Internal linking rule:** Every new post links to **one** pillar hub and **two** related posts minimum.

---

## Publishing definition of done (blog)

Before scheduling or publishing:

- [ ] **Intent** matches H1 (informational vs commercial).
- [ ] **Primary keyword** in title, H1, first ~100 words — naturally.
- [ ] **Meta title & description** set (Rank Math); no duplicate titles sitewide.
- [ ] **Featured image** (16:9), alt text describes the image (not keyword spam).
- [ ] **Excerpt** written for archive cards (used by Centy Blog theme).
- [ ] **Author** assigned; **reviewed** if claims touch tax, labour, or regulatory topics.
- [ ] **Internal links** to pillar + siblings + relevant `getcenty.com` page where appropriate.
- [ ] **Last updated** note on statutory posts when laws/rates change.
- [ ] **Schema** — Article via Rank Math; FAQ only if visible FAQs exist on page.

---

## Technical checklist (both surfaces)

- [ ] `robots.txt` allows crawl; `Sitemap:` lines accurate.
- [ ] Canonicals: HTTPS, preferred host (`www` for marketing — match GSC).
- [ ] 404 → branded `/404.html` on origin (see `SEO-YOU-DO.md`).
- [ ] Monthly: GSC **Pages** report — fix spikes in Not indexed / Crawled not indexed.
- [ ] Quarterly: **Core Web Vitals** spot-check on homepage, top 3 posts, primary landing page.
- [ ] After deploy: update `sitemap.xml` **lastmod** on marketing when pages materially change.

---

## Refresh calendar (compliance & money pages)

| Content type | Minimum refresh |
|--------------|------------------|
| PAYE / NSSF / SHIF / NITA / Housing levy numbers | When statutes or KRA guidance change |
| “How to choose payroll / payouts” buyer guides | Quarterly |
| Pillar hubs | Quarterly (stats, links, examples) |
| Competitor comparison tables | When named vendors materially change pricing/features |

---

## Off-site & risk

- Prefer **few high-quality** citations (partners, research, legitimate press) over bulk guest posts.
- **Comparison content:** Criteria-based, dated; avoid unsubstantiated “#1” or competitor attacks.
- **Finance / payroll claims:** Conservative wording; “not legal/tax advice” where needed.

---

## Reporting (monthly, 30 min)

1. GSC: clicks & impressions for **marketing** vs **blog**; top queries and pages.
2. **Cluster view:** group blog URLs by pillar; note which cluster stalled.
3. One **action:** e.g. refresh title/meta on high-impression low-CTR page, fix orphan post, or schedule statutory update.

---

## Related files

- `../SEO-YOU-DO.md` — Quick technical checklist for static marketing site.
- `SEO-KEYWORD-MAP.csv` — Keyword ↔ URL ↔ owner ↔ last reviewed.
- `SEO-90-DAY-PLAN.md` — Phased Kenya offensive: pillars, cadence, metrics, link moats.
- `google-drive-export/` — CSV tabs + **README-IMPORT-TO-GOOGLE-DRIVE.md** for Sheets on your Google account.
- `../tools/seo-automation/` — **Automated** Sheet sync + GSC append (local terminal or GitHub Actions); see **README.md** there.
