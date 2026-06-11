"""Generate Subject Guard for Gmail icons at 16/48/128px.

Design: a white envelope on a Gmail-red rounded square. A short red bar sits
above the envelope (the empty subject line) crossed out, signalling "no
subject". Rendered large with supersampling then downscaled for crisp edges.
"""

import os

from PIL import Image, ImageDraw

# Resolve output paths relative to the repo root, so the script works from
# any working directory.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(ROOT, "src", "icons")

RED = (217, 48, 37, 255)        # Gmail / Google red (#d93025)
DARK_RED = (168, 30, 20, 255)
WHITE = (255, 255, 255, 255)

SS = 8  # supersampling factor


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def render(size):
    s = size * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Light background rounded square for strong contrast with the red mark.
    rounded_rect(d, (0, 0, s - 1, s - 1), radius=int(s * 0.22), fill=WHITE)

    # Envelope geometry (centred, lower portion of the tile).
    ew = int(s * 0.62)
    eh = int(s * 0.42)
    ex = (s - ew) // 2
    ey = int(s * 0.42)
    flap_dip = int(eh * 0.46)
    lw = max(2, int(s * 0.06))

    # Solid red envelope body with a white flap drawn on top — bold, reads
    # clearly at 16px.
    rounded_rect(d, (ex, ey, ex + ew, ey + eh), radius=int(s * 0.05), fill=RED)
    cx = ex + ew // 2
    d.line([(ex + lw, ey + lw), (cx, ey + flap_dip)], fill=WHITE, width=lw)
    d.line([(cx, ey + flap_dip), (ex + ew - lw, ey + lw)], fill=WHITE, width=lw)

    # Empty "subject" bar above the envelope (grey = blank field) struck
    # through in red to signal "missing".
    bar_w = int(s * 0.44)
    bar_h = max(2, int(s * 0.09))
    bx = (s - bar_w) // 2
    by = int(s * 0.21)
    rounded_rect(d, (bx, by, bx + bar_w, by + bar_h), radius=bar_h // 2,
                 fill=(189, 193, 198, 255))
    pad = int(s * 0.03)
    d.line(
        [(bx - pad, by + bar_h + pad), (bx + bar_w + pad, by - pad)],
        fill=RED,
        width=max(2, int(s * 0.06)),
    )

    return img.resize((size, size), Image.LANCZOS)


os.makedirs(ICON_DIR, exist_ok=True)
for size in (16, 48, 128):
    path = os.path.join(ICON_DIR, f"icon{size}.png")
    render(size).save(path)
    print(f"wrote {os.path.relpath(path, ROOT)}")
