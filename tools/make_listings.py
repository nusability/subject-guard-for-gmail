"""Assemble per-language Chrome Web Store listing pages from listings.json.

Writes store/listings/<lang>.md, each with the Summary and Detailed
description ready to paste into the dashboard's per-language listing fields.
The Web Store summary field has a hard 132-character limit, so we check it
and warn loudly if any locale's summary is too long.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "listings.json")
OUT_DIR = os.path.join(ROOT, "store", "listings")

SUMMARY_MAX = 132


def detailed(t):
    """Assemble the plain-text detailed description block."""
    lines = [t["hook"], "", t["how"], "", t["catchesTitle"].upper()]
    lines += [f"• {c}" for c in t["catches"]]
    lines += ["", t["calmTitle"].upper()]
    lines += [f"• {c}" for c in t["calm"]]
    lines += ["", t["privacyTitle"].upper(), t["privacy"], "", t["footer"]]
    return "\n".join(lines)


with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

os.makedirs(OUT_DIR, exist_ok=True)

warnings = []
for lang, t in data.items():
    summary = t["summary"]
    n = len(summary)
    if n > SUMMARY_MAX:
        warnings.append(f"{lang}: summary is {n} chars (max {SUMMARY_MAX})")

    page = (
        f"# Store listing — {lang}\n\n"
        f"## Summary ({n}/{SUMMARY_MAX} characters)\n\n"
        f"```\n{summary}\n```\n\n"
        f"## Detailed description\n\n"
        f"```\n{detailed(t)}\n```\n"
    )
    with open(os.path.join(OUT_DIR, f"{lang}.md"), "w", encoding="utf-8") as f:
        f.write(page)

print(f"wrote store/listings/<lang>.md for {len(data)} languages")
if warnings:
    print("WARNING — summaries over the limit:")
    for w in warnings:
        print("  " + w)
