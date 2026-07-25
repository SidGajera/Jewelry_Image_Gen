# How to find trending jewelry products (Layer 1 sources)

Practical playbook for the trend engine. Start manual, then automate the same sources.
**Track *attributes*, not just products** — shape/cut, setting, metal, style, price band —
so trends become countable. Respect each site's Terms of Service + robots.txt; prefer
official APIs over scraping.

## A. Best signals = real sales (start here)
- **Etsy** — search a category, sort by "Most reviews" or filter the **Bestseller** badge.
  Reviews ≈ sales, so this is real demand. Tools: **eRank / Sale Samurai / Marmalead**
  (Etsy trend + keyword search volume).
- **Amazon** — **Best Sellers** + **Movers & Shakers** (Jewelry). Tools: **Jungle Scout /
  Helium 10** for sales estimates + rising keywords.
- **Retailer "Best sellers" / "New in" pages** — Blue Nile, Brilliant Earth, James Allen,
  VRAI, Mejuri, Kay. What they push + restock = what sells.

## B. Search demand (what people are looking for)
- **Google Trends** (trends.google.com) — compare terms ("toi et moi ring" vs "solitaire"),
  watch **Rising / Breakout** queries, by region. Automate with `pytrends`.
- **Pinterest Trends** (trends.pinterest.com) + the annual **Pinterest Predicts** report —
  jewelry/bridal is huge on Pinterest; shows rising searches early.

## C. Social (where trends start now)
- **TikTok** — **TikTok Creative Center** (trending hashtags/products/sounds), plus
  #jewelrytok #engagementring. Short-video drives jewelry trends fastest.
- **Instagram / Reels** — top brands + jewelry influencers; most-liked = resonating styles.

## D. Editorial / industry (context + forecasts)
- **Vogue, Brides, The Knot** — annual "engagement ring trends" pieces.
- **JCK, National Jeweler, Rapaport** — trade press + market data.
- **Trade shows** — JCK Las Vegas, Vicenzaoro — trend reports.
- **Reddit** — r/EngagementRings, r/jewelry — real buyers showing/asking.

## E. Turn it into data (what to record)
For each piece you see, tag it to `taxonomy.json`:
`cut · orientation · setting · prongs · composition · band · metal · motif · price_band`.
Then **count frequency + growth over time**. Rising counts = trends.

## F. Automate (wire into `trend_engine.aggregate()`)
| Source | How | Notes |
|---|---|---|
| Google Trends | `pytrends` | unofficial but reliable |
| Etsy | Etsy Open API / eRank export | API preferred over scraping |
| Amazon | Product Advertising API (PA-API) | needs affiliate account |
| Pinterest | Pinterest Trends (limited API) | or manual weekly |
| TikTok | Creative Center (manual) / partners | no simple public API |
| Retailer pages | scrape "new-in" **within ToS** | or partner data feeds |
| Images → attributes | a vision model tags cut/setting/metal | this is the "tag" step |

## G. Do-this-first (manual MVP, ~2 hours/week)
1. Open a spreadsheet with columns = the taxonomy attributes.
2. Log the **top 50 best-sellers** from Etsy + 2 retailers, plus Pinterest/Google-Trends
   rising terms for ~10 jewelry queries.
3. Tag each row by shape/setting/metal/style.
4. Count. The top combinations are your trends → feed them in as design-DNA seeds.

This is Layer 1 done by hand. Once it's proven useful, replace the spreadsheet with the
adapters in section F.
