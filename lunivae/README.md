# Lunivae Jewels — Website

A premium, luxury-minimal marketing site for **Lunivae Jewels** — custom fine
jewelry from Surat, India. *Inspired by Royal Heritage. Crafted for Modern Love.*

## Run locally
Just open `index.html` in a browser, or serve the folder:
```
python3 -m http.server 8080   # then visit http://localhost:8080
```

## Structure
- `index.html` — all page markup (single-page scroll experience)
- `styles.css` — design system + layout + motion
- `main.js` — scroll reveals, nav state, counters, form UX
- `assets/` — photography + logo

## Brand logo
The logo is rendered as a live typographic lockup (crisp at any size, adapts to
light/dark). To use the exact raster logo instead, save it as
`assets/logo.png` and set `data-logo="image"` on the `<body>` tag — the script
will swap every lockup for the image automatically.
