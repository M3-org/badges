#!/usr/bin/env python3
"""
Generate a poster that shows each badge type as a row:
Level-1..Level-5 images side-by-side (1 row per type), then stacked into one big poster.

Expected layout:
./Level-1/badge-<type>-level-1.png
./Level-2/badge-<type>-level-2.png
...
./Level-5/badge-<type>-level-5.png

Usage:
  python make_badge_poster.py --root . --out poster.png
Optional:
  --cell 256        # resize each badge to NxN (keeps aspect)
  --pad 24          # padding between cells
  --row-gap 28      # vertical gap between rows
  --label           # draw "<type>" label on each row (requires a system font)
"""

import argparse
import os
import re
from glob import glob
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

BADGE_RE = re.compile(r"badge-(?P<type>.+?)-level-(?P<level>[1-5])\.png$", re.IGNORECASE)

def load_font(size: int) -> ImageFont.ImageFont:
    # Try a few common fonts; fallback to default if none found.
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()

def fit_to_cell(img: Image.Image, cell: int) -> Image.Image:
    """Resize image to fit within cell x cell, preserving aspect. Paste onto transparent cell."""
    img = img.convert("RGBA")
    w, h = img.size
    scale = min(cell / w, cell / h)
    nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
    resized = img.resize((nw, nh), Image.LANCZOS)
    cell_img = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
    ox = (cell - nw) // 2
    oy = (cell - nh) // 2
    cell_img.paste(resized, (ox, oy), resized)
    return cell_img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Root folder containing Level-1..Level-5 directories")
    ap.add_argument("--out", default="badge_poster.png", help="Output poster filename")
    ap.add_argument("--cell", type=int, default=256, help="Cell size for each badge (pixels)")
    ap.add_argument("--pad", type=int, default=24, help="Horizontal padding between badges (pixels)")
    ap.add_argument("--row-gap", type=int, default=28, help="Vertical gap between rows (pixels)")
    ap.add_argument("--margin", type=int, default=40, help="Outer margin (pixels)")
    ap.add_argument("--bg", default="#0b0b0d", help="Background color (e.g. '#111', 'white')")
    ap.add_argument("--label", action="store_true", help="Draw type labels on the left")
    ap.add_argument("--label-width", type=int, default=220, help="Reserved width for labels if --label")
    ap.add_argument("--title", default="", help="Optional poster title at top")
    args = ap.parse_args()

    # Discover all badge PNGs under Level-* folders
    pattern = os.path.join(args.root, "Level-*", "badge-*-level-*.png")
    files = glob(pattern)
    if not files:
        raise SystemExit(f"No files matched: {pattern}")

    # Group by type and level
    by_type = defaultdict(dict)  # {type: {level: filepath}}
    for fp in files:
        name = os.path.basename(fp)
        m = BADGE_RE.match(name)
        if not m:
            continue
        t = m.group("type")
        lvl = int(m.group("level"))
        by_type[t][lvl] = fp

    if not by_type:
        raise SystemExit("No badge-<type>-level-<n>.png files found.")

    types = sorted(by_type.keys())
    levels = [1, 2, 3, 4, 5]

    # Preload + normalize images into fixed cells (RGBA)
    cells = {}  # (type, level) -> Image
    missing = []
    for t in types:
        for lvl in levels:
            fp = by_type[t].get(lvl)
            if not fp or not os.path.exists(fp):
                missing.append((t, lvl))
                continue
            img = Image.open(fp)
            cells[(t, lvl)] = fit_to_cell(img, args.cell)

    if missing:
        # Not fatal; we'll leave blanks for missing
        print("Warning: missing some badges (will render blank):")
        for t, lvl in missing:
            print(f"  {t} level {lvl}")

    # Layout sizing
    label_w = args.label_width if args.label else 0
    row_h = args.cell
    col_w = args.cell
    cols = len(levels)

    title_h = 0
    font_title = load_font(54)
    font_label = load_font(28)

    if args.title.strip():
        title_h = 90  # simple fixed header height

    poster_w = (
        args.margin * 2
        + label_w
        + cols * col_w
        + (cols - 1) * args.pad
    )
    poster_h = (
        args.margin * 2
        + title_h
        + len(types) * row_h
        + (len(types) - 1) * args.row_gap
    )

    poster = Image.new("RGBA", (poster_w, poster_h), args.bg)

    draw = ImageDraw.Draw(poster)

    # Title
    y = args.margin
    if title_h:
        # Center title
        title = args.title.strip()
        tw, th = draw.textbbox((0, 0), title, font=font_title)[2:]
        tx = (poster_w - tw) // 2
        ty = y + (title_h - th) // 2
        draw.text((tx, ty), title, font=font_title, fill=(240, 240, 245, 255))
        y += title_h

    # Draw rows
    for idx, t in enumerate(types):
        row_y = y + idx * (row_h + args.row_gap)
        # label
        x0 = args.margin
        if args.label:
            label = t.replace("-", " ")
            # vertically center label in row
            bbox = draw.textbbox((0, 0), label, font=font_label)
            lh = bbox[3] - bbox[1]
            ly = row_y + (row_h - lh) // 2
            draw.text((x0, ly), label, font=font_label, fill=(220, 220, 230, 255))
            x0 += label_w

        # badges 1..5
        for j, lvl in enumerate(levels):
            cx = x0 + j * (col_w + args.pad)
            cy = row_y
            cell_img = cells.get((t, lvl))
            if cell_img is None:
                # blank placeholder (transparent)
                cell_img = Image.new("RGBA", (args.cell, args.cell), (0, 0, 0, 0))
            poster.paste(cell_img, (cx, cy), cell_img)

    # Convert to RGB if you want a flat background without alpha:
    out_img = poster.convert("RGB")
    out_img.save(args.out)
    print(f"Wrote: {args.out} ({poster_w}x{poster_h})")

if __name__ == "__main__":
    main()
