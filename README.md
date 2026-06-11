# Subject Guard for Gmail

Chrome extension that blocks sending a Gmail message while the subject line is empty. No settings, no override, no alert dialogs — the subject field just shakes, turns red, gets focused, and a small hint fades away on its own. The hint is localized into 13 languages and follows Gmail's own display language.

## Install (development)

1. Run `./build.sh` to generate `src/i18n.js` and the icons.
2. Open `chrome://extensions`
3. Enable **Developer mode** (top right)
4. Click **Load unpacked** and select the **`src/`** folder
5. Reload any open Gmail tabs

## What it covers

- Clicking the **Send** button
- **Ctrl+Enter / Cmd+Enter** send shortcut
- Pressing **Enter/Space** while the Send button is focused

Inline replies without a visible subject field are unaffected (their subject is inherited from the thread).

## Layout

```
src/              what ships in the extension (load this folder unpacked)
  manifest.json
  content.js      send-blocking logic
  style.css       shake + red highlight + hint bubble
  i18n.js         GENERATED in-page hint strings (do not edit by hand)
  _locales/       GENERATED chrome.i18n catalogs (store name + description)
  icons/          GENERATED icon16/48/128.png
tools/            build-time scripts + canonical data
  translations.json   canonical source for all localized strings
  build_i18n.py       translations.json -> src/i18n.js + src/_locales/
  make_icons.py       -> src/icons/*.png
  make_screenshot.py  -> store/screenshot-<lang>.png
  listings.json       canonical store-page copy (summary + description)
  make_listings.py    -> store/listings/<lang>.md
store/            GENERATED promo screenshots for the Web Store listing
  listings/       GENERATED per-language listing copy, ready to paste
dist/             GENERATED packaged zip
build.sh          builds everything
```

## Build

```bash
./build.sh                # regenerate i18n.js + icons, package dist/gmail-subject-guard-v<version>.zip
./build.sh --screenshots  # also regenerate the localized store screenshots
```

The zip contains only the contents of `src/` (manifest at the archive root) — upload it directly to the Chrome Web Store.

## Localization

Edit strings in **`tools/translations.json`** only — it is the single source of truth. `build_i18n.py` generates two sets of localized assets from it, each using the language source that fits its context:

**In-page hint** → `src/i18n.js`. Baked into a `NSG_HINTS` table that loads before `content.js` in the same content-script world, so the right hint is available synchronously (no async fetch, no race against an immediate send). The hint follows **Gmail's** UI language (`<html lang>`), falling back to the browser locale, then English — it matches the language the user is actually reading in Gmail. Right-to-left languages (Arabic, etc.) flip the hint bubble.

**Store name + description** → `src/_locales/<lang>/messages.json`, the standard [chrome.i18n](https://developer.chrome.com/docs/extensions/reference/api/i18n) catalogs. `manifest.json` references them as `__MSG_extName__` / `__MSG_extDescription__` with `default_locale: "en"`. These follow the **browser's** UI locale (that's what chrome.i18n resolves against) and localize the name/description shown in `chrome://extensions` and the Web Store. Chrome strips the region before matching (`pt_BR` → `pt`, `zh_CN` → `zh`), so a bare two-letter folder covers every regional variant.

Why two mechanisms: the in-page hint should match Gmail's language, but `chrome.i18n.getMessage()` only knows the browser locale — so the hint uses its own table while the store-facing strings use chrome.i18n.

**Store listing pages** (summary + detailed description shown on the Web Store) are not part of the extension package — they are entered per-language in the developer dashboard. Edit **`tools/listings.json`** and run the build; `make_listings.py` assembles `store/listings/<lang>.md` for all 13 languages, each with a character-counted summary and a paste-ready detailed description. The build warns if any summary exceeds the Web Store's 132-character limit.

### Screenshots for Arabic / Hindi

`make_screenshot.py` skips `ar` and `hi` because this Pillow build lacks **libraqm**, so it cannot shape Arabic/Devanagari text in the PNG. The extension itself renders these languages correctly (the browser shapes the text). To also generate those two screenshots, install libraqm (e.g. `brew install libraqm`), reinstall Pillow, remove them from `SKIP` in `make_screenshot.py`, and rerun `./build.sh --screenshots`.
