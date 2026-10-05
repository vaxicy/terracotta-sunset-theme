<p align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/terracotta-sunset-theme/main/logo/logo128.png" width="128" alt="Terracotta Sunset Theme icon">
</p>

<h1 align="center">Terracotta Sunset Theme</h1>

<p align="center">A warm Chrome theme in terracotta red, soft apricot and sunset coral.</p>

<p align="center">
  <img src="https://img.shields.io/badge/Chrome%20Web%20Store-theme-blue?logo=googlechrome" alt="Chrome Web Store">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="version">
  <img src="https://img.shields.io/badge/license-Non--Commercial-lightgrey" alt="license">
</p>

## About

Terracotta Sunset brings the calm of a late afternoon sky to the browser. A terracotta red frame wraps the top of the window, the toolbar and active tab soften into apricot cream, and the new tab page opens on warm cream so the page you are reading stays the brightest thing on screen. Sunset coral marks the new tab header and every link, while deep cocoa text keeps labels, icons, bookmarks and headings sharp on all of those light surfaces. The design is flat colour throughout — no wallpaper, no textures, no gradients — and the icon distills it into a single terracotta half-sun settling behind two horizon lines.

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Terracotta Red | `#A14646` | Window frame (active and inactive) and window button background |
| Sunset Coral | `#DA6556` | New tab page header and links |
| Apricot Cream | `#FBE6D5` | Toolbar, active tab, bookmarks bar |
| Warm Cream | `#FFF5EC` | New tab page background, tab titles and window glyphs on the frame |
| Warm White | `#FFFAF6` | Omnibox (address bar) field |
| Deep Cocoa | `#542F2B` | Tab, bookmark, toolbar and new-tab text, toolbar icons |
| Warm Orange | `#EB895B` | Accent tone used in the store artwork |
| Soft Apricot | `#FDB773` | Accent tone used in the store artwork |

The four tones on the store introduction card — Terracotta Red, Sunset Coral, Warm Orange and Soft Apricot — are the palette the theme is built from; Warm Orange and Soft Apricot appear as accents in the artwork rather than as separate UI roles. Deep cocoa carries all small text, because coral at this lightness is too low-contrast to read at 12–13px. Window button glyphs, hover states and separators are drawn by Chrome and Windows.

## Features

- Terracotta red frame with an apricot cream toolbar and active tab for crisp, readable browser chrome.
- Flat, solid colour design with no wallpaper, textures or gradients.
- Sunset coral header and links on the new tab page, tuned against warm cream.
- Deep cocoa text and icons sized for comfortable contrast on every light surface.
- One continuous frame colour whether the window is focused or not.
- Single-tone Google wordmark drawn by Chrome itself through `ntp_logo_alternate`.
- Pure theme: no scripts, no permissions, nothing collected.

## Install

### From source (unpacked)

1. Download or clone this repository.
2. Open Chrome and navigate to `chrome://extensions`.
3. Enable **Developer mode** in the top-right corner.
4. Click **Load unpacked** and select this folder.
5. The theme applies immediately; reset it any time under Settings, then Appearance, then Themes.

### From the Chrome Web Store

The store listing is in preparation. Until it is live, load the unpacked copy with the steps above.

## Preview

### Store screenshots · 1280×800

**Browser interface** — the themed window with a bookmarks bar and the new tab page.

![Terracotta Sunset Theme browser preview](https://raw.githubusercontent.com/vaxicy/terracotta-sunset-theme/main/store-assets/screenshots/en/screenshot-1-browser.png)

**Palette & highlights** — the four tones the theme is built from and what each one controls.

![Terracotta Sunset Theme palette](https://raw.githubusercontent.com/vaxicy/terracotta-sunset-theme/main/store-assets/screenshots/en/screenshot-2-introduction.png)

### Store promo tiles

**Marquee tile · 1400×560** — “Warm tones. A calmer everyday browser.”

![Terracotta Sunset Theme marquee](https://raw.githubusercontent.com/vaxicy/terracotta-sunset-theme/main/store-assets/promo/1400x560.png)

**Small tile · 440×280** — “A little sunset, every day.”

<p align="center">
  <img src="https://raw.githubusercontent.com/vaxicy/terracotta-sunset-theme/main/store-assets/promo/440x280.png" width="440" alt="Terracotta Sunset Theme promo tile">
</p>

These are illustrative HTML/CSS layouts rendered by headless Chromium from the exact `manifest.json` colours, calibrated against a real installed Chrome session. They are not native Chrome captures, so the fine details — window glyphs, hover states, and the tinted Google wordmark — follow your own browser and OS after install.

## Files

| File | Description |
|------|-------------|
| `manifest.json` | Chrome theme manifest (MV3) with an inline `theme` block — single source of truth for every colour |
| `logo/logo128.png` | Theme and store icon, 128x128, the only size the manifest references |
| `store-assets/screenshots/en/` | Store listing screenshots (1280x800) |
| `store-assets/promo/` | Promo tiles (440x280 and 1400x560) |
| `store-assets/references/` | The browser and promo mock-up HTML plus their PNG renders |
| `store-assets/store-description.txt` | Store listing description (English) |
| `scripts/` | Generators: layout references, store assets, release ZIP |
| `PACKAGING.md` | How the upload ZIP is built |
| `LICENSE` | Non-Commercial License (bilingual) |

## Regenerating the assets

```
pip install -r scripts/requirements.txt
playwright install chromium

python3 scripts/generate-store-assets.py
```

One composer renders all four store assets — both screenshots, both promo tiles, and the HTML sources in `store-assets/references/` — so a style change is made in the script and re-rendered, never patched onto a PNG. The script also asserts that the logo is exactly 128x128.

## Packaging

```
powershell -ExecutionPolicy Bypass -File scripts/package.ps1 -Force
```

Writes a complete ZIP named `terracotta-sunset-theme-<version>.zip` to the default folder `D:\迅雷下载\vibe coding`, with `manifest.json` at the archive root. `-Force` overwrites any existing archive.

The screenshots and promo tiles travel inside the ZIP, but the store form still needs them uploaded one by one: `store-assets/screenshots/en/` fills the two screenshot slots, `store-assets/promo/1400x560.png` is the marquee tile and `store-assets/promo/440x280.png` is the small tile.

## License

Non-Commercial License — personal use permitted, commercial use requires permission. See [LICENSE](LICENSE).
