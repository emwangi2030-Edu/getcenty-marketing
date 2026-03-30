"""Normalize SEO_SHEET_ID from env (strip, extract ID if user pasted full URL)."""

import re


def normalize_spreadsheet_id(raw):
    """
    Return spreadsheet ID only.
    Accepts bare ID or full Google Sheets URL.
    """
    if not raw:
        return ""
    s = raw.strip().strip('"').strip("'")
    # Paste like https://docs.google.com/spreadsheets/d/XXXX/edit?...
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", s)
    if m:
        return m.group(1)
    # Already just the id
    return s.split("/")[0].split("?")[0].strip()
