#!/bin/bash
# Server-side sync for naturalgrassbrooms.com News.
# Installed at ~/bin/ngb-news-sync.sh on the cPanel server (NOT executed from the repo,
# so changes pushed to GitHub can never change what this cron job runs).
# Runs hourly via cron: pulls the GitHub repo and copies ONLY news pages + sitemap.xml + assets/ images
# into the live site. It never deletes anything on the live site.
set -euo pipefail
REPO="$HOME/repositories/naturalgrassbrooms-news"
DEST="$HOME/public_html/naturalgrassbrooms.com"
GIT="$(command -v git || echo /usr/local/cpanel/3rdparty/bin/git)"
LOG_PREFIX="[$(date '+%F %T')]"

cd "$REPO"
"$GIT" fetch --quiet origin main
"$GIT" reset --quiet --hard origin/main

changed=0
for f in public/news.html public/news-*.html public/sitemap.xml; do
  [ -f "$f" ] || continue
  name="$(basename "$f")"
  case "$name" in
    news.html|sitemap.xml|news-*.html) ;;
    *) continue ;;
  esac
  if ! cmp -s "$f" "$DEST/$name"; then
    cp -f "$f" "$DEST/$name"
    echo "$LOG_PREFIX updated $name"
    changed=1
  fi
done
mkdir -p "$DEST/assets"
for f in assets/*.jpg assets/*.jpeg assets/*.png assets/*.webp; do
  [ -f "$f" ] || continue
  name="$(basename "$f")"
  if ! cmp -s "$f" "$DEST/assets/$name"; then
    cp -f "$f" "$DEST/assets/$name"
    echo "$LOG_PREFIX updated assets/$name"
    changed=1
  fi
done
[ "$changed" = 1 ] || echo "$LOG_PREFIX no changes"
