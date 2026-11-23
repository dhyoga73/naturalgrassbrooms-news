# naturalgrassbrooms-news

Source of the News section of https://naturalgrassbrooms.com (PT Dharma Artha Nusantara).

- `articles/<slug>/meta.json` + `body.html` — one folder per article
- `CONTENT_GUIDE.md` — keywords, allowed facts, rules (read before writing)
- `topics-used.md` — log of published topics / primary keywords
- `build.py` — validates articles and builds `public/` (news pages, news.html, sitemap.xml)
- `templates/` — site header & footer (copied from the live site)
- `deploy/ngb-news-sync.sh` — reference copy of the hourly cron script on the hosting server

Publishing flow: commit an article → run `python3 build.py` → commit `public/` → push to `main`.
The hosting server pulls `main` every hour and copies `public/news*.html` and `public/sitemap.xml` to the live site.
