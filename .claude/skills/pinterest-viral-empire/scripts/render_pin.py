#!/usr/bin/env python3
"""Render branded Intentional Empire text-overlay pins (1000x1500 PNG).

Usage:
  python3 render_pin.py spec.json [--out ./pins] [--all-colorways]

spec.json is one object or a list of objects:
  {
    "colorway": "blue" | "green" | "ivory" | "midnight",
    "eyebrow":  "ECONOMIC SOVEREIGNTY",            # small label on top (optional)
    "headline": "Stop Manifesting. Start *Allocating.*",  # *word* = gold emphasis
    "subhead":  "The money reset nobody taught you",      # optional
    "bullets":  ["Name the leak", "Fund the peace"],      # optional, max ~7
    "footer":   "@intentionalempire",                     # optional (defaults to brand handle)
    "name":     "allocating-v1"                           # optional filename
  }
Colors and fonts come from ../brand.json.
"""
import argparse
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = json.load(open(os.path.join(HERE, "..", "brand.json"), encoding="utf-8"))
W, H = BRAND["rules"]["pin_size"]
M = BRAND["rules"]["safe_margin_px"]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font(kind, size):
    for path in BRAND["fonts"][kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def tokens(text):
    """Split headline into (word, is_gold) tokens; *...* marks gold."""
    out = []
    for i, part in enumerate(re.split(r"\*", text)):
        for w in part.split():
            if out and re.fullmatch(r"[^\w'\"(]+", w):
                out[-1] = (out[-1][0] + w, out[-1][1])  # glue punctuation to previous word
            else:
                out.append((w, i % 2 == 1))
    return out


def wrap_tokens(draw, toks, fnt, max_w):
    lines, cur = [], []
    space = draw.textlength(" ", font=fnt)
    for t in toks:
        trial = cur + [t]
        width = sum(draw.textlength(w, font=fnt) for w, _ in trial) + space * (len(trial) - 1)
        if cur and width > max_w:
            lines.append(cur)
            cur = [t]
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def wrap_text(draw, text, fnt, max_w):
    return [" ".join(w for w, _ in ln) for ln in wrap_tokens(draw, [(w, False) for w in text.split()], fnt, max_w)]


def fit_headline(draw, toks, max_w, max_h):
    for size in range(120, 44, -4):
        f = font("headline", size)
        lines = wrap_tokens(draw, toks, f, max_w)
        if len(lines) * size * 1.15 <= max_h:
            return f, lines, size
    f = font("headline", 44)
    return f, wrap_tokens(draw, toks, f, max_w), 44


def crown_divider(draw, cx, y, color):
    draw.line([(cx - 140, y), (cx - 22, y)], fill=color, width=3)
    draw.line([(cx + 22, y), (cx + 140, y)], fill=color, width=3)
    s = 12
    draw.polygon([(cx, y - s), (cx + s * 0.35, y - s * 0.35), (cx + s, y), (cx + s * 0.35, y + s * 0.35),
                  (cx, y + s), (cx - s * 0.35, y + s * 0.35), (cx - s, y), (cx - s * 0.35, y - s * 0.35)], fill=color)


def render(spec, out_dir):
    cw = BRAND["colorways"][spec.get("colorway", "blue")]
    C = {k: hex_rgb(BRAND["colors"][v]) for k, v in cw.items()}
    img = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(img)
    max_w = W - 2 * M

    # thin gold frame (keeps gold well under the 10% canvas rule)
    d.rectangle([M // 2, M // 2, W - M // 2, H - M // 2], outline=C["accent"], width=3)

    y = M + 40
    if spec.get("eyebrow"):
        f = font("label", 30)
        t = spec["eyebrow"].upper()
        d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=C["accent"])
        y += 70

    top = y
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = 0
    has_body = bool(spec.get("bullets")) or bool(spec.get("subhead"))
    head_box = 560 if has_body else 900
    hf, lines, size = fit_headline(d, tokens(spec["headline"]), max_w, head_box)
    space = d.textlength(" ", font=hf)
    for ln in lines:
        lw = sum(d.textlength(w, font=hf) for w, _ in ln) + space * (len(ln) - 1)
        x = (W - lw) / 2
        for w, gold in ln:
            d.text((x, y), w, font=hf, fill=C["accent"] if gold else C["text"])
            x += d.textlength(w, font=hf) + space
        y += size * 1.15

    y += 30
    crown_divider(d, W // 2, int(y), C["accent"])
    y += 50

    if spec.get("subhead"):
        f = font("body", 40)
        for ln in wrap_text(d, spec["subhead"], f, max_w - 40):
            d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=C["sub"])
            y += 54
        y += 30

    bullets = spec.get("bullets") or []
    if bullets:
        f = font("body", 38)
        for i, b in enumerate(bullets, 1):
            num = f"{i:02d}"
            nf = font("label", 38)
            d.text((M + 30, y), num, font=nf, fill=C["accent"])
            for j, ln in enumerate(wrap_text(d, b, f, max_w - 150)):
                d.text((M + 120, y), ln, font=f, fill=C["text"])
                y += 50
            y += 22
            if y > H - M - 140 - top:
                break

    content_h = int(y)
    bottom = H - M - 80
    offset = max(top, int(top + (bottom - top - content_h) / 2))
    img.paste(layer, (0, offset), layer)
    d = ImageDraw.Draw(img)

    footer = spec.get("footer") or BRAND["handle"]
    f = font("label", 28)
    d.text(((W - d.textlength(footer, font=f)) / 2, H - M - 30), footer, font=f, fill=C["sub"])

    name = spec.get("name") or re.sub(r"[^a-z0-9]+", "-", spec["headline"].lower()).strip("-")[:50]
    path = os.path.join(out_dir, f"{name}-{spec.get('colorway', 'blue')}.png")
    img.save(path, optimize=True)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out", default="./pins")
    ap.add_argument("--all-colorways", action="store_true", help="render every colorway for each spec (A/B variants)")
    a = ap.parse_args()
    specs = json.load(open(a.spec, encoding="utf-8"))
    specs = specs if isinstance(specs, list) else [specs]
    os.makedirs(a.out, exist_ok=True)
    for s in specs:
        if "headline" not in s:
            sys.exit(f"Spec missing 'headline': {s}")
        cws = list(BRAND["colorways"]) if a.all_colorways else [s.get("colorway", "blue")]
        for cw in cws:
            print(render({**s, "colorway": cw}, a.out))


if __name__ == "__main__":
    main()
