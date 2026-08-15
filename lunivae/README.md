# Lunivae Jewels — Website

A premium, luxury-minimal site for **Lunivae Jewels** — custom fine jewelry from
Surat, India. *Inspired by Royal Heritage. Crafted for Modern Love.*

## Run locally
The site is plain HTML/CSS/JS — no build step.

**Easiest:** open `index.html` in your browser (double-click it). All pages link
to each other and work.

**Recommended (cleanest asset loading):** serve the folder, then browse:
```
python3 -m http.server 8080      # → http://localhost:8080
# or:  npx serve .
```

## Pages
| File | Purpose |
|------|---------|
| `index.html`   | Home — hero, collections, story, bespoke, B2B, contact |
| `shop.html`    | **Product listing** — filter by category, sort, product grid |
| `product.html` | **Product details** — gallery, specs, enquire, wishlist (`?id=<product>`) |

## Files
- `styles.css` — design system + all page layouts + motion
- `main.js` — shared behavior (nav, reveals, counters, cursor, forms)
- `products.js` — the product catalog (edit this to add/remove pieces)
- `shop.js` — renders + filters/sorts the listing
- `product.js` — renders the details page from `products.js`
- `assets/` — photography

## Editing products
Add or change entries in `products.js` — both the listing and details pages read
from it automatically. Drop new photos in `assets/` and reference them by filename.

## Logo
Rendered as a live typographic monogram (crisp at any size, matches the brand
mark). No image file required.
