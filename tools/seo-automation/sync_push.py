#!/usr/bin/env python3
"""
Push docs/google-drive-export/*.csv into a Google Sheet (one tab per file).
Run from repo root or this directory; uses Sheets API (tabs replaced each run).
"""

import argparse
import csv
import os
import sys
from pathlib import Path

from sheet_id import normalize_spreadsheet_id

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# CSV filename (without path) -> tab title (must match [A-Za-z0-9_]+ roughly for Sheets)
TAB_MAP = {
    "01_Content_Calendar_90d.csv": "Content_Calendar",
    "02_Weekly_Metrics_Tracker.csv": "Weekly_Metrics",
    "03_North_Star_Targets.csv": "North_Star",
    "04_Competitor_Watchlist.csv": "Competitors",
    "05_Keyword_Map_Base.csv": "Keyword_Map",
}


def marketing_root():
    return Path(__file__).resolve().parent.parent.parent


def export_dir():
    override = os.environ.get("SEO_EXPORT_DIR")
    if override:
        return Path(override)
    return marketing_root() / "docs" / "google-drive-export"


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return [row for row in csv.reader(f)]


def ensure_sheet_exists(service, spreadsheet_id, title):
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for s in meta.get("sheets", []):
        if s["properties"]["title"] == title:
            return
    body = {"requests": [{"addSheet": {"properties": {"title": title, "gridProperties": {"rowCount": 2000, "columnCount": 40}}}}]}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()


def push_tab(service, spreadsheet_id, title, rows, dry_run):
    if dry_run:
        print(f"[dry-run] Would update tab {title!r} with {len(rows)} rows")
        return
    ensure_sheet_exists(service, spreadsheet_id, title)
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=f"'{title}'!A:ZZ",
    ).execute()
    if not rows:
        return
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{title}'!A1",
        valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()
    print(f"Updated tab {title!r} ({len(rows)} rows)")


def main():
    parser = argparse.ArgumentParser(description="Sync CSV exports to Google Sheet tabs.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions only")
    args = parser.parse_args()

    sheet_id = normalize_spreadsheet_id(os.environ.get("SEO_SHEET_ID", ""))
    root = export_dir()
    if not root.is_dir():
        print(f"ERROR: Export dir missing: {root}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"[dry-run] Would sync from {root} to sheet {sheet_id or '(no SHEET_ID)'}:")
        for filename, tab in TAB_MAP.items():
            path = root / filename
            print(f"  {filename} -> {tab!r} exists={path.is_file()}")
        print("sync_push: dry-run done (no API calls)")
        return 0

    if not sheet_id:
        print("ERROR: Set SEO_SHEET_ID to your Google Sheet ID.", file=sys.stderr)
        return 1

    from googleapiclient.discovery import build

    from credentials import load_credentials

    creds = load_credentials(SCOPES)
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)

    try:
        for filename, tab in TAB_MAP.items():
            path = root / filename
            if not path.is_file():
                print(f"WARN: skip missing file {path}", file=sys.stderr)
                continue
            rows = read_csv_rows(path)
            push_tab(service, sheet_id, tab, rows, dry_run=False)
    except Exception as exc:
        _print_api_error("sync_push (Google Sheets)", exc)
        return 1

    print("sync_push: done")
    return 0


def _print_api_error(where, exc):
    """Print useful detail for HttpError and friends (stderr + GitHub Actions)."""
    print("ERROR in %s: %s" % (where, exc), file=sys.stderr)
    resp = getattr(exc, "resp", None)
    status = getattr(resp, "status", None) if resp else None
    if status is not None:
        print("HTTP status: %s" % status, file=sys.stderr)
    content = getattr(resp, "content", b"") if resp else b""
    if content:
        try:
            snippet = content.decode("utf-8", errors="replace")[:800]
        except Exception:
            snippet = str(content)[:800]
        print("Response (truncated): %s" % snippet, file=sys.stderr)
    if status == 403:
        print(
            "Hint: Share the spreadsheet with the service account email (Editor).",
            file=sys.stderr,
        )
    if status == 404:
        print(
            "Hint: 404 often means wrong ID or the Sheet is not shared with the service account "
            "(Google may hide existence). Use only the ID from /d/SHEET_ID/ or paste the full URL as the secret.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    raise SystemExit(main())
