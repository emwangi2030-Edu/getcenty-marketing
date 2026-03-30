# getcenty-marketing

Static marketing site for **getcenty.com** (HTML/CSS/JS), SEO docs, and automation that syncs CSV exports to **Google Sheets** + **Search Console** reporting.

- **Deploy:** `bash deploy/rsync-marketing.sh` (see `IMPLEMENTATION.md`).
- **SEO:** `docs/SEO-GOVERNANCE.md`, `docs/SEO-90-DAY-PLAN.md`.
- **Sheets + GSC automation:** `tools/seo-automation/README.md` · GitHub Action: `.github/workflows/seo-automation.yml` (secrets: `GOOGLE_APPLICATION_CREDENTIALS_JSON`, `SEO_SHEET_ID`).

Remote: [github.com/emwangi2030-Edu/getcenty-marketing](https://github.com/emwangi2030-Edu/getcenty-marketing).

## Git remote (SSH)

```text
git@github.com:emwangi2030-Edu/getcenty-marketing.git
```

Push: `git push -u origin main` (after `git clone` or init with this remote).

HTTPS + [PAT](https://github.com/settings/tokens) also works if you prefer:

`git remote set-url origin https://github.com/emwangi2030-Edu/getcenty-marketing.git`
