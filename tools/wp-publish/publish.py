#!/usr/bin/env python3
"""
Publish a Centy blog pillar draft from docs/blog-content/<slug>.html to
blog.getcenty.com via the WordPress REST API.

Conservative by design:
  - Defaults to status=draft (manual review in WP admin before going live).
  - Dry-run default is true; nothing writes unless --no-dry-run is passed.
  - Refuses to overwrite an existing post by slug unless update_if_exists=true.
  - Featured image is NOT uploaded here — set it manually in WP admin so the
    media library reflects the licence + alt text consciously.
  - Rank Math meta is sent best-effort; if the server has not exposed those
    keys via register_post_meta(show_in_rest=true), they are stored but not
    surfaced. README documents the small mu-plugin snippet that fixes that.

Sidecar JSON `<slug>.json` (same folder as the HTML) carries metadata:

  {
    "title": "...",
    "slug": "...",
    "excerpt": "...",
    "focus_keyword": "...",
    "meta_title": "...",
    "meta_description": "...",
    "category_slugs": ["payroll"]
  }

Env (from workflow):
  WP_BLOG_URL, WP_BLOG_USER, WP_BLOG_APP_PASSWORD
  INPUT_SLUG, INPUT_STATUS, INPUT_UPDATE_IF_EXISTS, INPUT_DRY_RUN
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = REPO_ROOT / "docs" / "blog-content"

REQUIRED_META = ["title", "slug", "excerpt", "focus_keyword"]


def env(name: str, required: bool = True) -> str:
    value = os.environ.get(name, "").strip()
    if required and not value:
        sys.exit(f"ERROR: missing required env var {name}")
    return value


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def load_sidecar(slug: str) -> dict[str, Any]:
    path = CONTENT_DIR / f"{slug}.json"
    if not path.exists():
        sys.exit(f"ERROR: sidecar metadata missing — {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.exit(f"ERROR: sidecar JSON invalid ({path}): {exc}")
    missing = [k for k in REQUIRED_META if not data.get(k)]
    if missing:
        sys.exit(f"ERROR: sidecar {path} missing fields: {', '.join(missing)}")
    return data


def load_html(slug: str) -> str:
    path = CONTENT_DIR / f"{slug}.html"
    if not path.exists():
        sys.exit(f"ERROR: content HTML missing — {path}")
    return path.read_text(encoding="utf-8")


def wp_get(session: requests.Session, base: str, endpoint: str, **params: Any) -> Any:
    url = urljoin(base.rstrip("/") + "/", endpoint.lstrip("/"))
    resp = session.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def wp_post(session: requests.Session, base: str, endpoint: str, payload: dict[str, Any]) -> Any:
    url = urljoin(base.rstrip("/") + "/", endpoint.lstrip("/"))
    resp = session.post(url, json=payload, timeout=60)
    if resp.status_code >= 400:
        sys.exit(f"ERROR: WP API {resp.status_code} on POST {endpoint}: {resp.text}")
    return resp.json()


def find_post_by_slug(session: requests.Session, base: str, slug: str) -> dict[str, Any] | None:
    hits = wp_get(session, base, "/wp-json/wp/v2/posts", slug=slug, status="any", per_page=2)
    if not hits:
        return None
    if len(hits) > 1:
        sys.exit(f"ERROR: multiple posts found with slug '{slug}' — refusing to guess")
    return hits[0]


def resolve_category_ids(
    session: requests.Session, base: str, slugs: list[str]
) -> list[int]:
    if not slugs:
        return []
    ids: list[int] = []
    for slug in slugs:
        hits = wp_get(session, base, "/wp-json/wp/v2/categories", slug=slug, per_page=2)
        if not hits:
            sys.exit(
                f"ERROR: category slug '{slug}' not found on WP. "
                "Create the category in WP admin first; this script will not auto-create."
            )
        ids.append(hits[0]["id"])
    return ids


def build_payload(meta: dict[str, Any], html: str, status: str, category_ids: list[int]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": meta["title"],
        "slug": meta["slug"],
        "status": status,
        "content": html,
        "excerpt": meta["excerpt"],
    }
    if category_ids:
        payload["categories"] = category_ids
    payload["meta"] = {
        "rank_math_title": meta.get("meta_title") or meta["title"],
        "rank_math_description": meta.get("meta_description") or meta["excerpt"],
        "rank_math_focus_keyword": meta["focus_keyword"],
    }
    return payload


def main() -> int:
    base = env("WP_BLOG_URL")
    user = env("WP_BLOG_USER")
    app_pw = env("WP_BLOG_APP_PASSWORD").replace(" ", "")
    file_slug = env("INPUT_SLUG")
    status = env("INPUT_STATUS")
    update_if_exists = truthy(env("INPUT_UPDATE_IF_EXISTS", required=False) or "false")
    dry_run = truthy(env("INPUT_DRY_RUN", required=False) or "true")

    if status not in {"draft", "publish"}:
        sys.exit(f"ERROR: status must be 'draft' or 'publish', got {status!r}")

    meta = load_sidecar(file_slug)
    html = load_html(file_slug)

    print(f"=== WP publish ===")
    print(f"  blog:           {base}")
    print(f"  file slug:      {file_slug}")
    print(f"  WP post slug:   {meta['slug']}")
    print(f"  title:          {meta['title']}")
    print(f"  status:         {status}")
    print(f"  update if exists: {update_if_exists}")
    print(f"  dry run:        {dry_run}")
    print(f"  content bytes:  {len(html)}")
    print(f"  focus keyword:  {meta['focus_keyword']}")

    if dry_run:
        print("\nDRY RUN — no WP writes attempted. To execute, re-run with dry_run=false.")
        return 0

    session = requests.Session()
    session.auth = (user, app_pw)
    session.headers.update({"Accept": "application/json"})

    existing = find_post_by_slug(session, base, meta["slug"])
    category_ids = resolve_category_ids(session, base, meta.get("category_slugs") or [])
    payload = build_payload(meta, html, status, category_ids)

    if existing and not update_if_exists:
        sys.exit(
            f"ERROR: post with slug '{meta['slug']}' already exists at id={existing['id']} "
            "(link={link}). Re-run with update_if_exists=true to overwrite.".format(
                link=existing.get("link", "")
            )
        )

    if existing:
        endpoint = f"/wp-json/wp/v2/posts/{existing['id']}"
        print(f"\nUpdating existing post id={existing['id']} …")
    else:
        endpoint = "/wp-json/wp/v2/posts"
        print("\nCreating new post …")

    result = wp_post(session, base, endpoint, payload)

    print("\n=== WP response ===")
    print(f"  id:     {result.get('id')}")
    print(f"  status: {result.get('status')}")
    print(f"  link:   {result.get('link')}")

    meta_echo = (result.get("meta") or {})
    expected_meta_keys = ["rank_math_title", "rank_math_description", "rank_math_focus_keyword"]
    missing_meta = [k for k in expected_meta_keys if not meta_echo.get(k)]
    if missing_meta:
        print(
            "\nWARN: Rank Math meta keys not echoed by REST: "
            + ", ".join(missing_meta)
            + ". The values were sent but the server may not expose them via REST. "
            "See tools/wp-publish/README.md for the mu-plugin snippet that fixes this. "
            "In the meantime, set Rank Math title/description/focus keyword in WP admin."
        )

    if status == "draft":
        print(
            "\nReminder: post status is 'draft'. Open it in WP admin, set the "
            "featured image, confirm Rank Math meta, run the Publishing DOD checklist "
            "(see docs/SEO-GOVERNANCE.md), then flip to Publish."
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except requests.HTTPError as exc:
        body = exc.response.text if exc.response is not None else ""
        sys.exit(f"ERROR: HTTP error from WP — {exc} :: {body}")
    except requests.RequestException as exc:
        sys.exit(f"ERROR: network error talking to WP — {exc}")
