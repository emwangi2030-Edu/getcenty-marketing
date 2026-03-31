#!/usr/bin/env python3
"""
Fetch public URLs and assert basic SEO signals (200, canonical, no accidental noindex, og:title).
Skips rich checks for XML sitemaps (200 + looks like XML only).

Usage (from repo root):
  python tools/seo-checks/seo_sanity_check.py [path/to/urls.txt]
Default url list: docs/seo-check-urls.txt
"""

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_URL_FILE = REPO_ROOT / "docs" / "seo-check-urls.txt"

UA = "Mozilla/5.0 (compatible; CentySEOCheck/1.0; +https://www.getcenty.com/)"

# <link rel="canonical" href="..."> (href may precede rel)
CANONICAL_RE = re.compile(
    r"""<link\s[^>]*\brel\s*=\s*["']canonical["'][^>]*>""",
    re.IGNORECASE | re.DOTALL,
)
CANONICAL_HREF_RE = re.compile(
    r"""href\s*=\s*["']([^"']+)["']""",
    re.IGNORECASE,
)

OG_TITLE_RE = re.compile(
    r"""<meta\s[^>]*\bproperty\s*=\s*["']og:title["'][^>]*>""",
    re.IGNORECASE | re.DOTALL,
)
META_CONTENT_RE = re.compile(
    r"""content\s*=\s*["']([^"']+)["']""",
    re.IGNORECASE,
)

ROBOTS_META_RE = re.compile(
    r"""<meta\s[^>]*\bname\s*=\s*["']robots["'][^>]*>""",
    re.IGNORECASE | re.DOTALL,
)


def _fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        status = resp.getcode()
        ctype = resp.headers.get("Content-Type", "")
        body = resp.read().decode("utf-8", errors="replace")
    return status, ctype, body


def _is_xml_url(url, ctype):
    if url.rstrip("/").endswith(".xml"):
        return True
    return "xml" in ctype.lower()


def check_url(url, timeout):
    errors = []
    try:
        status, ctype, body = _fetch(url, timeout)
    except urllib.error.HTTPError as e:
        return ["HTTP %s" % e.code]
    except urllib.error.URLError as e:
        return ["Fetch failed: %s" % e.reason]
    except Exception as e:
        return ["Error: %s" % e]

    if status != 200:
        errors.append("expected HTTP 200, got %s" % status)

    if _is_xml_url(url, ctype):
        if "<?xml" not in body[:500] and "<urlset" not in body and "sitemapindex" not in body:
            errors.append("response does not look like a sitemap XML")
        return errors

    m = CANONICAL_RE.search(body)
    if not m:
        errors.append("missing <link rel=canonical>")
    else:
        href_m = CANONICAL_HREF_RE.search(m.group(0))
        if not href_m or not href_m.group(1).strip():
            errors.append("canonical link has empty href")

    rm = ROBOTS_META_RE.search(body)
    if rm:
        chunk = rm.group(0).lower()
        if "noindex" in chunk:
            errors.append("robots meta contains noindex")

    if not re.search(r'property\s*=\s*["\']og:title["\']', body, re.I):
        errors.append("missing og:title meta")

    return errors


def load_urls(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="SEO sanity checks for public URLs.")
    parser.add_argument(
        "url_file",
        nargs="?",
        default=str(DEFAULT_URL_FILE),
        help="Text file with one URL per line",
    )
    parser.add_argument("--timeout", type=int, default=25)
    args = parser.parse_args()
    path = Path(args.url_file)
    if not path.is_file():
        print("ERROR: URL file not found: %s" % path, file=sys.stderr)
        return 1

    urls = load_urls(path)
    if not urls:
        print("ERROR: no URLs in %s" % path, file=sys.stderr)
        return 1

    failed = False
    for url in urls:
        errs = check_url(url, args.timeout)
        if errs:
            failed = True
            print("FAIL %s\n  %s" % (url, "\n  ".join(errs)))
        else:
            print("OK   %s" % url)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
