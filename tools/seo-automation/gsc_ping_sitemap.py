#!/usr/bin/env python3
"""
Notify Google Search Console of a sitemap URL (sitemaps.submit API).

This nudges discovery/recrawl; it is not identical to the UI "Request indexing"
button (no public API for that for normal pages). Requires Search Console **Full**
access for the service account on the property.

Env:
  GSC_PROPERTY_URL   — verified property, URL-prefix form, trailing slash
                       (default: https://blog.getcenty.com/)
  GSC_SITEMAP_URL    — full sitemap URL (default: property + sitemap_index.xml)
  GSC_INSPECT_URL    — optional; if set, runs URL Inspection API and prints status
"""

import os
import sys

# Write scope required for sitemaps.submit (readonly is not enough).
SCOPES_SUBMIT = ["https://www.googleapis.com/auth/webmasters"]
# Inspection allows readonly; reuse full scope so one credential load suffices.
SCOPES_INSPECT = SCOPES_SUBMIT


def _print_inspect(creds, site_url, inspection_url):
    from googleapiclient.discovery import build

    svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    body = {"inspectionUrl": inspection_url.strip(), "siteUrl": site_url.strip()}
    out = (
        svc.urlInspection()
        .index()
        .inspect(body=body)
        .execute()
    )
    result = out.get("inspectionResult") or {}
    idx = result.get("indexStatusResult") or {}
    print(
        "URL Inspection: coverageState=%s pageFetchState=%s verdict=%s"
        % (
            idx.get("coverageState", "?"),
            idx.get("pageFetchState", "?"),
            idx.get("verdict", "?"),
        )
    )
    link = result.get("inspectionResultLink")
    if link:
        print("Open in Search Console: %s" % link)


def main():
    prop = os.environ.get("GSC_PROPERTY_URL", "https://blog.getcenty.com/").strip()
    if not prop.endswith("/"):
        prop += "/"
    default_map = prop.rstrip("/") + "/sitemap_index.xml"
    sitemap = os.environ.get("GSC_SITEMAP_URL", default_map).strip()
    inspect_url = os.environ.get("GSC_INSPECT_URL", "").strip()

    from googleapiclient.discovery import build

    from credentials import load_credentials

    creds = load_credentials(SCOPES_SUBMIT)
    wm = build("webmasters", "v3", credentials=creds, cache_discovery=False)
    wm.sitemaps().submit(siteUrl=prop, feedpath=sitemap).execute()
    print("GSC: submitted sitemap for property %s → %s" % (prop, sitemap))

    if inspect_url:
        try:
            _print_inspect(creds, prop, inspect_url)
        except Exception as exc:
            print("WARN: URL Inspection failed (sitemap submit still succeeded): %s" % exc)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("ERROR in gsc_ping_sitemap: %s" % exc, file=sys.stderr)
        msg = str(exc).lower()
        if "403" in msg or "forbidden" in msg:
            print(
                "Hint: Use the same service account as CI; it needs **Full** permission on this "
                "property. Submit scope is https://www.googleapis.com/auth/webmasters (write).",
                file=sys.stderr,
            )
        raise SystemExit(1)
