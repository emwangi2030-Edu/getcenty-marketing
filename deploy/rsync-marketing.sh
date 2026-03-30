#!/usr/bin/env bash
# Sync static marketing site to the VPS docroot (adjust REMOTE_PATH after creating the vhost).
set -euo pipefail
HOST="${DEPLOY_HOST:-root@172.239.110.187}"
# Live vhost docroot for www/getcenty.com (OpenLiteSpeed getcenty.com)
REMOTE_PATH="${REMOTE_PATH:-/home/getcenty.com/public_html}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "→ rsync to $HOST:$REMOTE_PATH"
rsync -avz --delete \
  "$ROOT/index.html" \
  "$ROOT/styles.css" \
  "$ROOT/site.js" \
  "$ROOT/robots.txt" \
  "$ROOT/sitemap.xml" \
  "$ROOT/og-image.png" \
  "$ROOT/404.html" \
  "$ROOT/about.html" \
  "$ROOT/security.html" \
  "$ROOT/privacy.html" \
  "$ROOT/terms.html" \
  "$HOST:$REMOTE_PATH/"

rsync -avz "$ROOT/.well-known/" "$HOST:$REMOTE_PATH/.well-known/"

ssh "$HOST" "chown -R nobody:nogroup '$REMOTE_PATH'"

echo "Done. Map 404 → /404.html in the web server if not already (see deploy/lsws/)."
