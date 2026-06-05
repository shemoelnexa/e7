# Minhaji — Landing Page

Bilingual (English / Arabic) landing page for **Minhaji**, an AI-powered digital reading and learning platform for educational institutions. A platform by **e7**.

## Contents

| File | Description |
|------|-------------|
| `index.html` | Source landing page. Loads styles, scripts, fonts, images and video from `assets/` and a few CDNs. |
| `e7-landing-page.html` | Standalone single-file build with **all** assets (CSS, JS, fonts, images, video) inlined as base64 — open it directly in any browser, no server or network needed. |
| `build_standalone.py` | Build script that generates `e7-landing-page.html` from `index.html`. |
| `assets/` | Fonts, images and the `minhaji-hero.mp4` background/preview video. |

## Usage

Open either HTML file in a browser:

- `index.html` — for development (keeps assets external).
- `e7-landing-page.html` — for sharing/offline (everything inlined).

## Building the standalone file

The build inlines the local assets plus the Bootstrap, Font Awesome and AOS CDN files. Place those CDN files in `/tmp/cdn`, then run:

```bash
python3 build_standalone.py
```

## Notes

- The background/preview video (`assets/minhaji-hero.mp4`) is H.264, 1280px wide, audio-stripped, kept small for web delivery.
- Language toggle (EN/AR) and RTL handling are built into `index.html`.
