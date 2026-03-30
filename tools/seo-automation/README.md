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
python run_all.py --dry-run    # no API writes
```

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

Schedule: **Mondays 07:00 UTC** (push + report). Use **Run workflow** for manual runs.

## Behaviour

- **sync_push:** Replaces tab content for mapped CSVs (see `TAB_MAP` in `sync_push.py`). Does **not** delete `GSC_Automated_Log`.
- **gsc_report:** Appends one row per property per run: `fetched_at_utc`, `site_url`, period, `clicks`, `impressions`, `ctr` (%), `position`.

Use **Weekly_Metrics** for manual notes; use **GSC_Automated_Log** for machine history. Optional: add a Sheet formula to `IMPORTRANGE` or `QUERY` the latest GSC rows into your dashboard tab.

## Troubleshooting

- **`403` / access denied:** Share the Sheet with the SA email; add SA to each GSC property.
- **`404` siteUrl in GSC:** Property URL must match GSC exactly (trailing slash, `https`).
- **Empty GSC rows:** New property or no data in window — script exits with error if nothing to append.
