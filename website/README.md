# Mill River Mechanical — demo website

A one-page static site. No build step, no backend, no secrets.

## Files

```
website/
├── index.html
└── assets/
    ├── logo.png                  (trimmed, web-sized logo)
    ├── favicon.png               (house mark)
    ├── hero-hvac-service.jpg
    ├── heat-pump-water-heater.jpg
    ├── minisplit-installation.jpg
    └── crew-end-of-day.jpg
```

Photos are compressed JPG copies (1536 px wide) of the originals in `brand/photos/`.

## Deploy

Vercel is connected to this repository. Pushing to `main` redeploys the site. The root `vercel.json` sets the output directory to `website/` with no build command, so no project settings are needed.

To preview locally: `cd website && python3 -m http.server 8000`, then open http://localhost:8000.

## Page notes

- Brand kit colors: navy #12365B, river blue #5D99C9, paper #FAF9F7, ink #1A1A1A.
- Flame orange #E85A30 appears once, as the short bar under the hero headline.
- The logo sits only on white (header) or paper (footer).
- Contact details: 112 Pleasant St, Easthampton, MA 01027 · 413-555-0100 · Mon–Fri 7:30–4:30 · millrivermech@gmail.com · licenses #MP-11482 and #RT-7734.
- Claims ruled out by the build brief are omitted: 24/7 service, free estimates, warranties, financing, reviews, awards and similar.
- The footer carries the fictional-demo notice.
- `<meta name="robots" content="noindex">` keeps search engines from listing the page.
