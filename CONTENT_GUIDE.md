# Content Guide — naturalgrassbrooms.com News

Every new article MUST follow this guide. `build.py` enforces the mechanical rules; the editorial rules are your responsibility.

## Goal
Bring international B2B buyers (importers, wholesalers, distributors, retailers' sourcing teams) to naturalgrassbrooms.com from Google, and turn them into quote requests. Each article targets **one primary keyword** that such a buyer would really type into Google, plus 2–5 supporting keywords.

## Publishing schedule
Two articles per week (Monday and Thursday). Quality over quantity: an article that is thin, repetitive or speculative hurts the site more than a skipped week. If you cannot write a genuinely useful, non-duplicative article, skip and report why.

## Keyword map (primary keywords to rotate through)
Use each primary keyword as the main target of at most ONE article; check `articles/*/meta.json` first.

Product keywords
- tiger grass broom / tiger grass broom supplier / tiger grass broom wholesale
- soft grass broom / reed grass broom / glagah broom / rayung broom
- nipa palm broom / nypa palm broom / nipa broom supplier
- bamboo garden broom / bamboo twig broom / bamboo leaf broom / outdoor broom for leaves
- natural broom / natural grass broom / handmade broom / eco-friendly broom / plastic-free broom / biodegradable broom
- sorghum broom / broomcorn broom (only as "in development" — never offer it)

Buyer / trade keywords
- grass broom supplier Indonesia / Indonesian broom exporter / broom manufacturer Indonesia
- wholesale natural brooms / bulk brooms for import / private label brooms (only explain the concept; never promise we offer it)
- HS code for brooms (HS 9603.10) / importing brooms from Indonesia / broom export documents
- how to import brooms from Indonesia / FOB vs CIF for brooms (explain generally)

Market keywords (PT DAN's target markets: India, Pakistan, China, Japan, South Korea, Sri Lanka)
- grass broom supplier for India / natural brooms Japan market / broom import Korea …
- Write these as market *guides* (what buyers there typically look for, general import considerations) — NEVER claim we already sell, ship or have customers there.

## Facts you may state (source of truth)
- Company: PT Dharma Artha Nusantara (PT DAN), Jakarta Timur (Jatinegara, Cakung), Indonesia. Brand: Indonesian Natural Grass Brooms. Contact: quote.html, WhatsApp +62 899 8168 328, yoga@dharmaartha.co.id.
- Main product: Tiger Grass Broom (Glagah / Rayung) — handmade natural grass broom; specs, length, handle and packaging confirmed per enquiry.
- Nipa Palm Broom (Nypah): 80 cm (approx. 250 g, 100 pcs/carton), 105 cm (approx. 300 g, 50 pcs/carton), 120 cm (approx. 500 g, 40 pcs/carton). Weights approximate.
- Bamboo Twig Broom (bamboo garden broom / natural bamboo branch broom): bundled bamboo twigs, for garden, yard and outdoor sweeping; dimensions confirmed per enquiry.
- Sorghum broom: under development — no specs, no availability.
- Indicative HS code: 9603.10 (brooms of vegetable materials bound together); final classification confirmed per shipment.
- Process (general): raw material selection → cleaning & drying → assembly → quality check → packing.
- Target markets being explored: India, Pakistan, China, Japan, South Korea, Sri Lanka (interest only).

General, widely known background knowledge (how natural brooms are used, care and storage, why natural fibres are biodegradable, what Incoterms mean, what an RFQ should contain, etc.) is fine. Any specific statistic, regulation or market figure must come from a reputable source you found with web search, be stated cautiously, and be linked in the article.

## NEVER write
- Prices, MOQ, lead times, container loads, production capacity, certifications, test results — unless they are added to "Facts you may state" above.
- Customers, shipments, exports completed, countries "we export to", testimonials, awards, partnerships.
- Private label / OEM / custom branding as something we offer (you may explain what it is and say "ask us about your requirements").
- Medical, safety or guaranteed-durability claims. Comparisons that disparage named competitors or countries.
- Anything about sorghum other than "under development".
- Keyword stuffing. The primary keyword should appear naturally: in the title, the SEO title, the description, the first paragraph, at least one <h2>, and 3–6 times overall for a 700–1,000 word article.

## Article format
Folder `articles/<slug>/` with two files:

`meta.json`
```json
{
  "slug": "tiger-grass-broom-supplier-guide",
  "date": "YYYY-MM-DD",
  "tag": "Buyer Guide",
  "title": "Human-friendly H1 that contains the primary keyword",
  "seo_title": "≤ 65 chars, contains the primary keyword",
  "description": "110–165 chars, contains the primary keyword, written as a reason to click",
  "summary": "1 sentence for the News listing card",
  "image": "one of the images listed under 'Images' below",
  "image_alt": "Describe honestly what the chosen image shows",
  "primary_keyword": "tiger grass broom supplier",
  "keywords": ["supporting keyword 1", "supporting keyword 2"]
}
```
Allowed tags: Buyer Guide, Product Guide, Export Guide, Market Insight, Sustainability, Company News.
Images (file name — what it shows; vary images between consecutive articles):
- tiger-grass-brooms-finished.jpg — a large pile of finished tiger grass (glagah / rayung) brooms with bamboo and plastic handles
- tiger-grass-broom-handmade.jpg — one handmade tiger grass broom with a bundled-grass handle and coloured stitching
- bamboo-twig-brooms-workshop.jpg — bamboo twig brooms standing upright in a workshop
- nypah-80cm-catalog.jpg / nypah-105cm-catalog.jpg / nypah-120cm-catalog.jpg — nipa palm broom catalogue photos
- indonesian-bamboo-twig-broom.webp — bamboo twig broom catalogue photo
Alt text must describe what the image really shows. Never name or identify the supplier or the workshop.
New photos: put them (resized ≤1600 px, EXIF stripped) in assets/ and add them to ALLOWED_IMAGES in build.py; the server copies assets/ to the site.

`body.html` — the article body only (no <h1>, no <script>):
- Start with `<p class="lead">…</p>` (2–3 sentences, contains the primary keyword).
- 700–1,000 words, 4–6 `<h2>` sections, short paragraphs, lists where helpful. Optionally end with a short FAQ (`<h2>FAQ</h2>` + `<h3>` questions).
- Link to at least one core page (`product.html#tiger-grass-broom`, `product.html#nypah-palm-brooms`, `product.html#bamboo-twig-broom`, `product.html#faq`, `quote.html`) and, where relevant, 1–2 earlier articles (`news-<slug>.html`).
- Finish with a call to action pointing to `quote.html` and WhatsApp `https://wa.me/628998168328`.
- English, written for professional buyers: specific, practical, no fluff.

## Topic bank (use, adapt or add to; mark used ones in topics-used.md)
1. Tiger grass broom supplier guide: how to source tiger grass brooms from Indonesia
2. Tiger grass vs nipa palm vs bamboo brooms: which natural broom fits which use
3. Nipa palm broom sizes explained: choosing 80, 105 or 120 cm for your market
4. Bamboo garden broom: what retailers and landscapers look for
5. How to write an RFQ for natural brooms (checklist)
6. HS code 9603.10 explained for broom importers
7. FOB vs CIF when importing brooms from Indonesia
8. Carton packing for natural brooms: how pcs per carton affects landed cost
9. Plastic-free cleaning: why retailers are adding natural grass brooms
10. How natural grass brooms are made: from glagah grass to finished broom
11. Caring for natural grass brooms: storage tips buyers can pass to consumers
12. Soft grass broom vs plastic broom for indoor sweeping
13. Importing natural brooms into India: practical considerations
14. Natural brooms for the Japanese market: quality expectations
15. Sourcing brooms for South Korea: what buyers ask first
16. Sri Lanka and Pakistan: natural broom demand and import basics
17. Sample orders: how to evaluate a natural broom sample
18. Glossary: Indonesian broom names (sapu glagah, sapu rayung, sapu nypah, sapu lidi) and their trade names
19. Seasonality of natural broom raw materials and planning orders
20. Company news: new product information or catalogue updates (only when there is a real update)
