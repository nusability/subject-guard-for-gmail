"""Generate the localized assets from translations.json (the canonical source).

Two outputs, both from the same data:

1. src/i18n.js — the in-page hint strings. Loaded before content.js in the
   same content-script isolated world, so `NSG_HINTS` is visible synchronously
   (no async fetch, no race against a send right after page load). The hint
   follows Gmail's own UI language.

2. src/_locales/<lang>/messages.json — the chrome.i18n catalog used for the
   store-facing extension name and description (manifest __MSG_*__ refs). These
   follow the browser's UI locale; Chrome strips the region (pt_BR -> pt,
   zh_CN -> zh), so a bare two-letter folder covers every regional variant.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "translations.json")
OUT_I18N = os.path.join(ROOT, "src", "i18n.js")
LOCALES_DIR = os.path.join(ROOT, "src", "_locales")

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

# 1. Runtime hint table.
hints = {lang: strings["hint"] for lang, strings in data.items()}
with open(OUT_I18N, "w", encoding="utf-8") as f:
    f.write("// AUTO-GENERATED from translations.json by build_i18n.py — do not edit by hand.\n")
    f.write("var NSG_HINTS = ")
    f.write(json.dumps(hints, ensure_ascii=False, indent=2))
    f.write(";\n")
print(f"wrote src/i18n.js with {len(hints)} languages")

# 2. chrome.i18n message catalogs for the store listing.
for lang, strings in data.items():
    messages = {
        "extName": {"message": strings["extName"]},
        "extDescription": {"message": strings["extDescription"]},
    }
    locale_dir = os.path.join(LOCALES_DIR, lang)
    os.makedirs(locale_dir, exist_ok=True)
    with open(os.path.join(locale_dir, "messages.json"), "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
        f.write("\n")
print(f"wrote src/_locales/<lang>/messages.json for {len(data)} languages")
