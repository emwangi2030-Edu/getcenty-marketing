#!/usr/bin/env python3
"""
Fetch Search Console search analytics (last N days) per property and append
rows to the GSC_Automated_Log tab on the same Sheet as sync_push.
"""

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta

from sheet_id import normalize_spreadsheet_id

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/webmasters.readonly",
]


def parse_sites():
    raw = os.environ.get("GSC_SITES", "").strip()
    if not raw:
        # sensible defaults for Centy — override in env / CI
        return [
            "https://www.getcenty.com/",
            "https://blog.getcenty.com/",
        ]
    return [s.strip() for s in raw.split(",") if s.strip()]


def daterange_days(end, days):
    """Return (start_iso, end_iso) inclusive-ish: last `days` days ending `end`."""
    start = end - timedelta(days=days)
    return start.isoformat(), end.isoformat()


def ensure_log_sheet(service, spreadsheet_id):
    title = "GSC_Automated_Log"
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for s in meta.get("sheets", []):
        if s["properties"]["title"] == title:
            return
    body = {"requests": [{"addSheet": {"properties": {"title": title, "gridProperties": {"rowCount": 5000, "columnCount": 12}}}}]}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    header = [
        [
            "fetched_at_utc",
            "site_url",
            "period_start",
            "period_end",
            "clicks",
            "impressions",
            "ctr",
            "position",
        ]
    ]
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{title}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": header},
    ).execute()


def append_rows(service, spreadsheet_id, rows):
    ensure_log_sheet(service, spreadsheet_id)
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="'GSC_Automated_Log'!A:A",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()


def _search_console_api_enable_hint(exc):
    """
    If Google returns 403 accessNotConfigured for Search Console API, return a one-line hint with enable URL.
    """
    resp = getattr(exc, "resp", None)
    if resp is None or getattr(resp, "status", None) != 403:
        return None
    raw = getattr(resp, "content", b"") or b""
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    err = data.get("error") or {}
    reasons = {e.get("reason") for e in err.get("errors", []) if isinstance(e, dict)}
    if "accessNotConfigured" not in reasons:
        return None
    msg = err.get("message", "")
    if "search" not in msg.lower() and "webmasters" not in msg.lower():
        return None
    m = re.search(r"https://console\.developers\.google\.com/[^\s\"]+", msg)
    if m:
        return "Hint: Enable Google Search Console API (same project as the service account key): %s" % m.group(0)
    m_proj = re.search(r"project (\d+)", msg)
    if m_proj:
        pid = m_proj.group(1)
        url = (
            "https://console.developers.google.com/apis/api/searchconsole.googleapis.com/overview?project=%s"
            % pid
        )
        return "Hint: Enable Google Search Console API for GCP project %s: %s" % (pid, url)
    return (
        "Hint: In Google Cloud Console → APIs & Services → Library, enable **Google Search Console API** "
        "for the project that owns this service account key."
    )


def _gsc_insufficient_permission_hint(exc):
    """
    403 from Search Analytics when the service account is not a user on the property.
    """
    resp = getattr(exc, "resp", None)
    if resp is None or getattr(resp, "status", None) != 403:
        return None
    raw = getattr(resp, "content", b"") or b""
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    err = data.get("error") or {}
    reasons = {e.get("reason") for e in err.get("errors", []) if isinstance(e, dict)}
    if "forbidden" not in reasons:
        return None
    msg = (err.get("message") or "").lower()
    if "permission" not in msg and "site" not in msg:
        return None
    return (
        "Hint: The API is enabled, but this service account is not a Search Console user on that property. "
        "In Google Search Console open each URL-prefix property (exact match, including trailing slash) → "
        "Settings → Users and permissions → Add user → add the SA email with **Full** access. "
        "See https://support.google.com/webmasters/answer/7687615"
    )


def fetch_aggregate(gsc, site_url, start, end):
    """Site-wide totals for the period."""
    req = {
        "startDate": start,
        "endDate": end,
        "dimensions": [],
        "rowLimit": 1,
    }
    resp = gsc.searchanalytics().query(siteUrl=site_url, body=req).execute()
    rows = resp.get("rows", [])
    if not rows:
        return {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
    r = rows[0]
    return {
        "clicks": r.get("clicks", 0),
        "impressions": r.get("impressions", 0),
        "ctr": round(r.get("ctr", 0) * 100, 4),
        "position": round(r.get("position", 0), 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Append GSC summary rows to Sheet.")
    parser.add_argument("--days", type=int, default=7, help="Trailing day window (default 7)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sheet_id = normalize_spreadsheet_id(os.environ.get("SEO_SHEET_ID", ""))
    sites = parse_sites()
    end = date.today()
    start_s, end_s = daterange_days(end, args.days)

    if args.dry_run:
        print(f"[dry-run] Would query GSC for {sites} ({start_s}..{end_s})")
        print(f"[dry-run] Would append to sheet {sheet_id or '(no SEO_SHEET_ID)'} / GSC_Automated_Log")
        return 0

    if not sheet_id:
        print("ERROR: Set SEO_SHEET_ID", file=sys.stderr)
        return 1

    from googleapiclient.discovery import build

    from credentials import load_credentials

    creds = load_credentials(SCOPES)
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_rows = []
    api_enable_hint = None
    gsc_permission_hint = None

    for site in sites:
        try:
            agg = fetch_aggregate(gsc, site, start_s, end_s)
        except Exception as e:
            print("WARN: GSC query failed for %s: %s" % (site, e), file=sys.stderr)
            h = _search_console_api_enable_hint(e)
            if h:
                api_enable_hint = h
            h2 = _gsc_insufficient_permission_hint(e)
            if h2:
                gsc_permission_hint = h2
            resp = getattr(e, "resp", None)
            if resp is not None and getattr(resp, "content", None):
                print(
                    "  detail: %s"
                    % resp.content.decode("utf-8", errors="replace")[:400],
                    file=sys.stderr,
                )
            continue
        out_rows.append(
            [
                now,
                site,
                start_s,
                end_s,
                agg["clicks"],
                agg["impressions"],
                agg["ctr"],
                agg["position"],
            ]
        )
        print(f"GSC {site} {start_s}..{end_s}: clicks={agg['clicks']} imps={agg['impressions']}")

    if not out_rows:
        print("ERROR: no rows to append (check GSC access / site URLs)", file=sys.stderr)
        if api_enable_hint:
            print(api_enable_hint, file=sys.stderr)
        elif gsc_permission_hint:
            sa_email = getattr(creds, "service_account_email", None) or "(see client_email in your SA JSON)"
            print(gsc_permission_hint, file=sys.stderr)
            print("      Service account to add: %s" % sa_email, file=sys.stderr)
        return 1

    try:
        append_rows(sheets, sheet_id, out_rows)
    except Exception as exc:
        print("ERROR in gsc_report (Sheets append): %s" % exc, file=sys.stderr)
        resp = getattr(exc, "resp", None)
        if resp is not None:
            print("HTTP status: %s" % getattr(resp, "status", "?"), file=sys.stderr)
            c = getattr(resp, "content", b"") or b""
            if c:
                print("Response (truncated): %s" % c.decode("utf-8", errors="replace")[:800], file=sys.stderr)
        status = getattr(resp, "status", None) if resp is not None else None
        if status == 404:
            print(
                "Hint: Sheet not found or not visible to the service account. Fix SEO_SHEET_ID "
                "(bare ID or full URL) and share the Sheet with the SA email as Editor.",
                file=sys.stderr,
            )
        else:
            print(
                "Hint: Share the Sheet with the service account; add the same email in Search Console for each site_url.",
                file=sys.stderr,
            )
        return 1

    print("gsc_report: appended to GSC_Automated_Log")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
