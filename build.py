#!/usr/bin/env python3
"""Build the News section of naturalgrassbrooms.com.

Reads articles/<slug>/meta.json + body.html and writes into public/:
  - news-<slug>.html  (one page per article)
  - news.html         (listing, newest first)
  - sitemap.xml       (core pages + news pages)

Run:  python3 build.py          -> validate + build
      python3 build.py --check  -> validate only

Validation fails (exit 1) on any problem, so a bad article is never published.
"""
import datetime as dt
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://naturalgrassbrooms.com"
ARTICLES = ROOT / "articles"
PUBLIC = ROOT / "public"
CSS_VERSION = "20261122-2"

# Pages that exist on the live site (internal links must point to one of these).
CORE_PAGES = {
    "index.html": "2026-11-22",
    "product.html": "2026-11-22",
    "about.html": "2026-11-22",
    "quote.html": "2026-11-22",
}
# Images that exist in /assets on the live site.
ALLOWED_IMAGES = {
    "nypah-80cm-catalog.jpg": (1122, 1402),
    "nypah-105cm-catalog.jpg": (1122, 1402),
    "nypah-120cm-catalog.jpg": (1122, 1402),
    "indonesian-bamboo-twig-broom.webp": (1086, 1448),
    # Real supplier photos (added 2026-11-23, stored in assets/ of this repo and synced to the site)
    "tiger-grass-brooms-finished.jpg": (1600, 1421),
    "tiger-grass-broom-handmade.jpg": (888, 1600),
    "bamboo-twig-brooms-workshop.jpg": (985, 1600),
}
ALLOWED_TAGS = {"Buyer Guide", "Company News", "Market Insight", "Product Guide", "Export Guide", "Sustainability"}
MIN_WORDS = 600
VOID = {"br", "img", "hr", "meta", "link", "input", "source", "wbr"}


class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.errors, self.links, self.h1 = [], [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.h1 += 1
        if tag == "script":
            self.errors.append("<script> is not allowed in article body")
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unbalanced </{tag}> (open: {self.stack[-3:]})")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()


def words(text):
    return re.findall(r"[A-Za-z0-9’'\-]+", re.sub(r"<[^>]+>", " ", text))


def date_text(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def load_articles():
    arts, errors = [], []
    slugs = set()
    for folder in sorted(p for p in ARTICLES.iterdir() if p.is_dir()):
        meta_p, body_p = folder / "meta.json", folder / "body.html"
        where = f"articles/{folder.name}"
        if not meta_p.exists() or not body_p.exists():
            errors.append(f"{where}: needs meta.json and body.html")
            continue
        try:
            m = json.loads(meta_p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{where}/meta.json: invalid JSON ({e})")
            continue
        body = body_p.read_text(encoding="utf-8").strip()
        req = ["slug", "date", "tag", "title", "seo_title", "description", "summary",
               "image", "image_alt", "primary_keyword", "keywords"]
        miss = [k for k in req if not m.get(k)]
        if miss:
            errors.append(f"{where}: missing fields {miss}")
            continue
        if m["slug"] != folder.name:
            errors.append(f"{where}: slug '{m['slug']}' must equal folder name")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", m["slug"]):
            errors.append(f"{where}: slug must be lowercase-words-with-dashes")
        if m["slug"] in slugs:
            errors.append(f"{where}: duplicate slug")
        slugs.add(m["slug"])
        try:
            m["_date"] = dt.date.fromisoformat(m["date"])
        except ValueError:
            errors.append(f"{where}: date must be YYYY-MM-DD")
            continue
        if m["_date"] > dt.date.today() + dt.timedelta(days=1):
            errors.append(f"{where}: date is in the future")
        if m["image"] not in ALLOWED_IMAGES:
            errors.append(f"{where}: image must be one of {sorted(ALLOWED_IMAGES)}")
        if m["tag"] not in ALLOWED_TAGS:
            errors.append(f"{where}: tag must be one of {sorted(ALLOWED_TAGS)}")

        checker = TagChecker()
        checker.feed(body)
        checker.close()
        errors += [f"{where}/body.html: {e}" for e in checker.errors]
        if checker.stack:
            errors.append(f"{where}/body.html: unclosed tags {checker.stack}")
        if checker.h1:
            errors.append(f"{where}/body.html: do not use <h1> (the page title is the h1)")
        for href in checker.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:")):
                continue
            page = href.split("#")[0]
            if page and page not in CORE_PAGES and page != "news.html" and not page.startswith("news-"):
                errors.append(f"{where}/body.html: link to unknown page '{href}'")
        m["_internal_news_links"] = [h.split("#")[0] for h in checker.links if h.startswith("news-")]

        if not m.get("legacy"):
            n = len(words(body))
            if n < MIN_WORDS:
                errors.append(f"{where}: body has {n} words, needs at least {MIN_WORDS}")
            if len(m["seo_title"]) > 65:
                errors.append(f"{where}: seo_title is {len(m['seo_title'])} chars (max 65)")
            if not 110 <= len(m["description"]) <= 165:
                errors.append(f"{where}: description is {len(m['description'])} chars (need 110–165)")
            pk = m["primary_keyword"].lower()
            first = " ".join(words(body)[:120]).lower()
            for label, text in [("seo_title", m["seo_title"]), ("description", m["description"]),
                                ("title", m["title"]), ("first 120 words of body", first)]:
                if pk not in text.lower():
                    errors.append(f"{where}: primary_keyword '{m['primary_keyword']}' missing from {label}")
            if "<h2" not in body:
                errors.append(f"{where}: body needs <h2> subheadings")
            if not any(h.split("#")[0] in CORE_PAGES for h in checker.links):
                errors.append(f"{where}: body must link to at least one core page (product.html, quote.html …)")
        m["_body"] = body
        arts.append(m)
    # links to other news articles must exist
    known = {f"news-{a['slug']}.html" for a in arts}
    for a in arts:
        for link in a["_internal_news_links"]:
            if link not in known:
                errors.append(f"articles/{a['slug']}: link to missing article '{link}'")
    arts.sort(key=lambda a: (a["_date"], a["slug"]), reverse=True)
    return arts, errors


def head(path, title, desc, image, og_type, ld):
    e = html.escape
    return f"""<!DOCTYPE html>

<html lang="en">
<head><meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{SITE}/{path}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Indonesian Natural Grass Brooms">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{SITE}/{path}">
  <meta property="og:image" content="{SITE}/assets/{image}">
  <meta name="twitter:card" content="summary_large_image">

  <title>{e(title)}</title>
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="styles.css?v={CSS_VERSION}" type="text/css">
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>

"""


ORG = {"@type": "Organization", "name": "PT Dharma Artha Nusantara", "url": SITE + "/",
       "logo": {"@type": "ImageObject", "url": SITE + "/assets/pt-dan-logo.png"}}

CTA = """
    <section class="shell section">
      <div class="cta">
        <h2>Looking for a natural broom supplier in Indonesia?</h2><a class="button light" href="quote.html">Request a Quote</a>
      </div>
    </section>
  </main>

  """


def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{SITE}/{p}"} for i, (n, p) in enumerate(items)]}


def card(a, heading="h2"):
    e = html.escape
    w, h = ALLOWED_IMAGES[a["image"]]
    f = f"news-{a['slug']}.html"
    return f"""
          <article class="card news-card">
            <a class="news-card-image" href="{f}"><img src="assets/{a['image']}" width="{w}" height="{h}" loading="lazy" alt="{e(a['image_alt'])}"></a>
            <span class="number">{e(a['tag'])} · <time datetime="{a['date']}">{date_text(a['_date'])}</time></span>

            <{heading} class="news-card-title"><a href="{f}">{e(a['title'])}</a></{heading}>

            <p>{e(a['summary'])}</p>

            <a class="news-read-more" href="{f}">Read article →</a>
          </article>"""


def build_article(a, all_arts, header, footer):
    e = html.escape
    f = f"news-{a['slug']}.html"
    w, h = ALLOWED_IMAGES[a["image"]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "NewsArticle", "headline": a["title"], "description": a["description"],
         "datePublished": a["date"] + "T09:00:00+07:00", "dateModified": a.get("modified", a["date"]) + "T09:00:00+07:00",
         "image": [f"{SITE}/assets/{a['image']}"], "author": ORG, "publisher": ORG,
         "mainEntityOfPage": f"{SITE}/{f}", "inLanguage": "en", "keywords": ", ".join([a["primary_keyword"]] + a["keywords"])},
        crumbs([("Home", ""), ("News", "news.html"), (a["title"], f)])]}
    related = [x for x in all_arts if x["slug"] != a["slug"]][:2]
    related_html = ""
    if related:
        related_html = f"""
    <section class="section soft">
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="eyebrow">Keep Reading</p>

            <h2>Related articles</h2>
          </div>
        </div>

        <div class="news-grid">{''.join(card(r, 'h3') for r in related)}
        </div>
      </div>
    </section>
"""
    main = f"""
  <main id="main-content">
    <section class="page-hero">
      <div class="shell">
        <div class="breadcrumb">
          <a href="index.html">Home</a><span>/</span><a href="news.html">News</a><span>/</span>{e(a['tag'])}
        </div>

        <p class="eyebrow">{e(a['tag'])} · <time datetime="{a['date']}">{date_text(a['_date'])}</time></p>

        <h1>{e(a['title'])}</h1>
      </div>
    </section>

    <section class="section">
      <div class="shell">
        <article class="article-body">
          <figure class="article-figure"><img src="assets/{a['image']}" width="{w}" height="{h}" alt="{e(a['image_alt'])}"></figure>

{a['_body']}

          <p class="article-meta">Published by PT Dharma Artha Nusantara · <time datetime="{a['date']}">{date_text(a['_date'])}</time> · <a href="news.html">← Back to News</a></p>
        </article>
      </div>
    </section>
{related_html}{CTA}"""
    return head(f, a["seo_title"], a["description"], a["image"], "article", ld) + header + "\n" + main + footer


def build_listing(arts, header, footer):
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "News & Insights – Indonesian Natural Grass Brooms",
         "url": SITE + "/news.html", "inLanguage": "en"},
        crumbs([("Home", ""), ("News", "news.html")])]}
    main = f"""
  <main id="main-content">
    <section class="page-hero">
      <div class="shell">
        <div class="breadcrumb">
          <a href="index.html">Home</a><span>/</span>News
        </div>

        <p class="eyebrow">News &amp; Insights</p>

        <h1>News and Buyer Insights on Indonesian Natural Brooms</h1>

        <p class="lead">Company updates from PT Dharma Artha Nusantara and practical guides for importers, wholesalers and distributors sourcing Tiger Grass, Nipa Palm and Bamboo brooms from Indonesia.</p>
      </div>
    </section>

    <section class="section">
      <div class="shell">
        <div class="news-grid">{''.join(card(a) for a in arts)}
        </div>
      </div>
    </section>
{CTA}"""
    image = arts[0]["image"] if arts else "nypah-80cm-catalog.jpg"
    return head("news.html", "News & Buyer Insights | Indonesian Natural Grass Brooms",
                "Company news and buyer guides from PT Dharma Artha Nusantara about Indonesian natural brooms: Tiger Grass (Glagah / Rayung), Nipa Palm and Bamboo Twig brooms.",
                image, "website", ld) + header + "\n" + main + footer


def build_sitemap(arts):
    rows = [("", CORE_PAGES["index.html"])] + [(p, d) for p, d in CORE_PAGES.items() if p != "index.html"]
    latest = max([a.get("modified", a["date"]) for a in arts] + ["2026-11-22"])
    rows.append(("news.html", latest))
    rows += [(f"news-{a['slug']}.html", a.get("modified", a["date"])) for a in sorted(arts, key=lambda a: a["date"])]
    body = "".join(f"  <url><loc>{SITE}/{p}</loc><lastmod>{d}</lastmod></url>\n" for p, d in rows)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


def main():
    arts, errors = load_articles()
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK: {len(arts)} articles valid")
    if "--check" in sys.argv:
        return
    header = (ROOT / "templates/header.html").read_text(encoding="utf-8")
    footer = (ROOT / "templates/footer.html").read_text(encoding="utf-8")
    PUBLIC.mkdir(exist_ok=True)
    expected = {"news.html", "sitemap.xml"} | {f"news-{a['slug']}.html" for a in arts}
    for old in PUBLIC.iterdir():
        if old.name not in expected:
            old.unlink()
    for a in arts:
        (PUBLIC / f"news-{a['slug']}.html").write_text(build_article(a, arts, header, footer), encoding="utf-8")
    (PUBLIC / "news.html").write_text(build_listing(arts, header, footer), encoding="utf-8")
    (PUBLIC / "sitemap.xml").write_text(build_sitemap(arts), encoding="utf-8")
    print(f"Built {len(arts) + 2} files in public/")


if __name__ == "__main__":
    main()
