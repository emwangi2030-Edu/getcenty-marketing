# SEO automation — push + reporting

Syncs `docs/google-drive-export/*.csv` into a **Google Sheet** and appends **Google Search Console** aggregates to `GSC_Automated_Log`. Run from **Cursor’s terminal** or **GitHub Actions**.

CI writes credentials with **`ci_write_credentials.py`** (no bash heredoc) so multiline JSON secrets stay valid.

## One-time Google Cloud setup

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/).
2. **Enable APIs** (APIs & Services → Library):
   - **Google Sheets API**
   - **Google Search Console API**
3. **IAM & Admin → Service accounts → Create service account** (name e.g. `centy-seo-sync`).
4. **Keys → Add key → JSON**; save locally (never commit).
5. Copy the service account **email** (e.g. `centy-seo-sync@proj.iam.gserviceaccount.com`).

## Google Sheet + Search Console access

1. Create (or open) your SEO workbook in Drive (from the CSV import flow).
2. Copy the **Sheet ID** from the URL:
   `https://docs.google.com/spreadsheets/d/`**`SHEET_ID_HERE`**`/edit`
3. **Share** the spreadsheet with the service account email → **Editor**.
4. In [Google Search Console](https://search.google.com/search-console), **add the service account email as a user** with permission on each property:
   - `https://www.getcenty.com/`
   - `https://blog.getcenty.com/`  
   (Use **exact** URL-prefix strings as verified in GSC.)

## Local run (Cursor terminal)

From `getcenty-marketing/tools/seo-automation`:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/service-account.json"
export SEO_SHEET_ID="your_spreadsheet_id"

# Optional: override CSV folder
# export SEO_EXPORT_DIR="/absolute/path/to/google-drive-export"

# Optional: GSC properties (comma-separated, exact GSC URLs)
# export GSC_SITES="https://www.getcenty.com/,https://blog.getcenty.com/"

python run_all.py              # push CSVs + GSC append
python run_all.py push         # only Sheets sync
python run_all.py gsc          # only GSC append
python run_all.py ping         # GSC: (re)submit blog sitemap + optional URL inspection
python run_all.py --dry-run    # no API writes
```

**GSC “ping” (`gsc_ping_sitemap.py`):** Calls the [Search Console sitemaps.submit](https://developers.google.com/webmaster-tools/v1/sitemaps/submit) API for `https://blog.getcenty.com/sitemap_index.xml` (override with `GSC_PROPERTY_URL` / `GSC_SITEMAP_URL`). That tells Google the sitemap URL again; it helps discovery but is **not** the same as the UI **Request indexing** button—Google does not offer a public API to queue arbitrary URLs for indexing. Optional `GSC_INSPECT_URL` runs the [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect) and prints status plus a link to open the result in Search Console. Requires OAuth scope `https://www.googleapis.com/auth/webmasters` (write); the same service account must have **Full** access on the property.

**CI / GitHub Actions:** use repository secret `GOOGLE_APPLICATION_CREDENTIALS_JSON` (entire JSON as a string) instead of a file path.

## GitHub Actions

Repository: [emwangi2030-Edu/getcenty-marketing](https://github.com/emwangi2030-Edu/getcenty-marketing).

Workflow: `.github/workflows/seo-automation.yml` — **repository root = this project** (`tools/seo-automation` under checkout). If you ever nest this inside a **parent monorepo**, edit the workflow `defaults.run.working-directory` to `getcenty-marketing/tools/seo-automation`.

**Secrets** (Settings → Secrets and variables → Actions):

| Name | Value |
|------|--------|
| `GOOGLE_APPLICATION_CREDENTIALS_JSON` | Full JSON of the service account key (paste multiline secret) |
| `SEO_SHEET_ID` | Spreadsheet ID only (`/d/THIS_PART/edit`) **or** full Sheet URL (we extract the ID) |

Optional:

| `GSC_SITES` | e.g. `https://www.getcenty.com/,https://blog.getcenty.com/` if defaults are wrong |

Schedule: **Mondays 07:00 UTC** (push + report). Use **Run workflow** for manual runs; choose **`ping`** to submit the blog sitemap and run URL inspection on the pillar post (see workflow env in `seo-automation.yml`).

## Behaviour

- **sync_push:** Replaces tab content for mapped CSVs (see `TAB_MAP` in `sync_push.py`). Does **not** delete `GSC_Automated_Log`.
- **gsc_report:** Appends one row per property per run: `fetched_at_utc`, `site_url`, period, `clicks`, `impressions`, `ctr` (%), `position`.

Use **Weekly_Metrics** for manual notes; use **GSC_Automated_Log** for machine history. Optional: add a Sheet formula to `IMPORTRANGE` or `QUERY` the latest GSC rows into your dashboard tab.

## Troubleshooting

- **`403` — Search Console API not enabled** (log says `accessNotConfigured` / “has not been used in project …”): open [Google Cloud Console](https://console.cloud.google.com/) → select the **same project** as the service account key → **APIs & Services → Library** → enable **Google Search Console API**. Google often includes a direct link in the error message (`.../apis/api/searchconsole.googleapis.com/overview?project=...`). Wait a few minutes after enabling, then re-run the workflow.
- **`403` — “User does not have sufficient permission for site”** (`forbidden`): the API works, but the **service account is not invited** on that Search Console property. For **each** URL in `GSC_SITES` (defaults include `https://www.getcenty.com/` and `https://blog.getcenty.com/`), open [Search Console](https://search.google.com/search-console) → select that **exact** property → **Settings** → **Users and permissions** → **Add user** → paste the **`client_email`** from the same JSON as `GOOGLE_APPLICATION_CREDENTIALS_JSON` → role **Full**. Domain properties and URL-prefix properties are separate: the SA must be added on the property the script queries. See [Google’s help](https://support.google.com/webmasters/answer/7687615).
- **`403` / Sheets:** Share the SEO spreadsheet with the SA email as **Editor**.
- **`404` siteUrl in GSC:** Property URL must match GSC exactly (trailing slash, `https`).
- **Empty GSC rows:** New property or no data in window — script exits with error if nothing to append.
