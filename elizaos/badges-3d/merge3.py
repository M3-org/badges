#!/usr/bin/env python3
from pathlib import Path
import re
import math
from collections import defaultdict
from PIL import Image, ImageDraw

ROOT = Path(".")
LEVELS = [1, 2, 3, 4, 5]

# Spacing
GAP_INNER = 20     # space between levels 1–5
GAP_SET = 80       # space BETWEEN full sets (columns)
GAP_Y = 32         # space between rows
MARGIN = 48

# Target aspect ratio
TARGET_AR = 16 / 9

# Divider style
DIVIDER_COLOR = (255, 255, 255, 140)  # brighter
DIVIDER_WIDTH = 6                     # thicker line

OUT = "badge_poster_optimal.png"

pat = re.compile(r"badge-(?P<type>.+?)-level-(?P<level>[1-5])\.png$", re.I)

# Collect files
by_type = defaultdict(dict)
for p in ROOT.glob("Level-*/badge-*-level-*.png"):
    m = pat.match(p.name)
    if not m:
        continue
    by_type[m.group("type")][int(m.group("level"))] = p

types = sorted(by_type.keys())
if not types:
    raise SystemExit("No badge PNGs found")

# Badge size
sample = next(iter(next(iter(by_type.values())).values()))
cell_w, cell_h = Image.open(sample).size

# One tile = one full 1–5 set
tile_w = len(LEVELS) * cell_w + (len(LEVELS) - 1) * GAP_INNER
tile_h = cell_h

n = len(types)

def poster_size(cols):
    rows = math.ceil(n / cols)
    w = MARGIN * 2 + cols * tile_w + (cols - 1) * GAP_SET
    h = MARGIN * 2 + rows * tile_h + (rows - 1) * GAP_Y
    return w, h, rows

# Choose column count to match target AR
best = None
for cols in range(1, min(n, 12) + 1):
    w, h, rows = poster_size(cols)
    score = abs((w / h) - TARGET_AR)
    cand = (score, cols, w, h, rows)
    if best is None or cand < best:
        best = cand

_, cols, poster_w, poster_h, rows = best

poster = Image.new("RGBA", (poster_w, poster_h), (0, 0, 0, 0))
draw = ImageDraw.Draw(poster)

# Render tiles
for i, t in enumerate(types):
    grid_r = i // cols
    grid_c = i % cols

    origin_x = MARGIN + grid_c * (tile_w + GAP_SET)
    origin_y = MARGIN + grid_r * (tile_h + GAP_Y)

    # Draw thick divider AFTER this set (unless last column)
    if grid_c < cols - 1:
        x = origin_x + tile_w + (GAP_SET // 2)
        y1 = origin_y
        y2 = origin_y + tile_h
        draw.line((x, y1, x, y2), fill=DIVIDER_COLOR, width=DIVIDER_WIDTH)

    # Paste levels 1–5
    for j, lvl in enumerate(LEVELS):
        x = origin_x + j * (cell_w + GAP_INNER)
        y = origin_y
        fp = by_type[t].get(lvl)
        if not fp:
            continue
        img = Image.open(fp).convert("RGBA")
        poster.paste(img, (x, y), img)

poster.save(OUT)
print(
    f"Wrote {OUT}: {poster_w}x{poster_h}, grid={cols}x{rows}, "
    f"aspect={(poster_w/poster_h):.3f}"
)
