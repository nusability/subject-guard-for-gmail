"""Create localized promo screenshots (1280x800) for the Chrome Web Store.

Reads translations.json and renders one screenshot per locale, mocking a
Gmail compose window with the empty subject highlighted red and the
localized "add a subject" hint.

Arabic (ar) and Hindi (hi) are skipped: this Pillow build lacks libraqm, so
it cannot shape Arabic/Devanagari text (the extension itself renders them
fine — the browser does the shaping). All other locales render correctly.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "tools", "translations.json")
OUT_DIR = os.path.join(ROOT, "store")

W, H = 1280, 800
RED = (217, 48, 37)
DARK = (32, 33, 36)
GREY = (95, 99, 104)
BORDER = (218, 220, 224)
WHITE = (255, 255, 255)

SKIP = {"ar", "hi"}  # unshapeable without libraqm

# Font files by script. Latin + Cyrillic share Arial; CJK/Korean need their
# own families.
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"  # zh + ja kana/kanji
KO = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

FONT_FILE = {"zh": CJK, "ja": CJK, "ko": KO}
# These scripts have no separate bold file, so bold is faked by double-draw.
FAKE_BOLD = {"zh", "ja", "ko"}

_cache = {}


def font(lang, size, bold=False):
    path = FONT_FILE.get(lang, ARIAL_BOLD if bold else ARIAL)
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text(d, xy, s, lang, size, fill, bold=False, anchor="lm"):
    f = font(lang, size, bold)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    if bold and lang in FAKE_BOLD:  # smear 1px to simulate weight
        d.text((xy[0] + 1, xy[1]), s, font=f, fill=fill, anchor=anchor)


def fit(d, s, lang, start, maxw, bold=False):
    """Largest size <= start at which `s` fits within maxw px."""
    size = start
    while size > 10 and d.textlength(s, font=font(lang, size, bold)) > maxw:
        size -= 1
    return size


def render(lang, t):
    img = Image.new("RGB", (W, H), (234, 237, 243))
    d = ImageDraw.Draw(img)

    # Title + subtitle, auto-shrunk to fit the canvas width.
    ts = fit(d, t["title"], lang, 40, W - 120, bold=True)
    text(d, (W // 2, 70), t["title"], lang, ts, DARK, bold=True, anchor="mm")
    ss = fit(d, t["subtitle"], lang, 24, W - 140)
    text(d, (W // 2, 120), t["subtitle"], lang, ss, GREY, anchor="mm")

    # Compose window card.
    cx, cy, cw, ch = 340, 200, 600, 520
    d.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=12, fill=WHITE,
                        outline=BORDER, width=1)
    d.rounded_rectangle((cx, cy, cx + cw, cy + 44), radius=12, fill=(66, 66, 66))
    d.rectangle((cx, cy + 22, cx + cw, cy + 44), fill=(66, 66, 66))
    text(d, (cx + 18, cy + 22), t["newMessage"], lang, 16, WHITE, bold=True)

    # To field.
    ty = cy + 70
    text(d, (cx + 18, ty), t["to"], lang, 16, GREY)
    text(d, (cx + 90, ty), t["recipient"], lang, 16, DARK)
    d.line((cx + 16, ty + 20, cx + cw - 16, ty + 20), fill=BORDER, width=1)

    # Subject field highlighted red (the blocked state).
    sy = ty + 50
    sx0, sx1 = cx + 12, cx + cw - 12
    d.rounded_rectangle((sx0, sy - 4, sx1, sy + 30), radius=4, outline=RED, width=3)
    text(d, (sx0 + 8, sy + 13), t["subject"], lang, 16, RED)

    # Hint bubble under the subject.
    hx, hy = sx0 + 4, sy + 42
    hf = font(lang, 15)
    tw = d.textlength(t["hint"], font=hf)
    d.rounded_rectangle((hx, hy, hx + tw + 24, hy + 32), radius=8, fill=RED)
    text(d, (hx + 12, hy + 16), t["hint"], lang, 15, WHITE)

    # Body text.
    by = hy + 60
    for i, line in enumerate(t["body"]):
        text(d, (cx + 18, by + i * 28), line, lang, 16, DARK)

    # Send button with a strike, implying the click won't fire.
    bx, by2 = cx + 18, cy + ch - 56
    bw = max(90, int(d.textlength(t["send"], font=font(lang, 16, True))) + 50)
    d.rounded_rectangle((bx, by2, bx + bw, by2 + 38), radius=19, fill=RED)
    text(d, (bx + bw // 2, by2 + 19), t["send"], lang, 16, WHITE, bold=True,
         anchor="mm")
    d.line((bx, by2 + 38, bx + bw, by2), fill=(120, 16, 10), width=3)

    name = f"screenshot-{lang}.png"
    img.save(os.path.join(OUT_DIR, name))
    return name


os.makedirs(OUT_DIR, exist_ok=True)
with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

for lang, t in data.items():
    if lang in SKIP:
        print(f"skip   {lang} (no libraqm shaping)")
        continue
    print("wrote ", render(lang, t))
