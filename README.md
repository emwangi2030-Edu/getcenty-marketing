# getcenty-marketing

Static marketing site for **getcenty.com** (HTML/CSS/JS), SEO docs, and automation that syncs CSV exports to **Google Sheets** + **Search Console** reporting.

- **Deploy:** `bash deploy/rsync-marketing.sh` (see `IMPLEMENTATION.md`).
- **SEO:** `docs/SEO-GOVERNANCE.md`, `docs/SEO-90-DAY-PLAN.md`.
- **Sheets + GSC automation:** `tools/seo-automation/README.md` · GitHub Action: `.github/workflows/seo-automation.yml` (secrets: `GOOGLE_APPLICATION_CREDENTIALS_JSON`, `SEO_SHEET_ID`).

Remote: [github.com/emwangi2030-Edu/getcenty-marketing](https://github.com/emwangi2030-Edu/getcenty-marketing).

## Push from your machine (this environment has no GitHub auth)

```bash
cd getcenty-marketing
git remote -v   # origin → https://github.com/emwangi2030-Edu/getcenty-marketing.git
git push -u origin main
```

Use a [personal access token](https://github.com/settings/tokens) as the password over HTTPS, or switch the remote to SSH:

`git remote set-url origin git@github.com:emwangi2030-Edu/getcenty-marketing.git`
