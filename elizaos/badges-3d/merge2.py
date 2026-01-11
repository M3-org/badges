#!/usr/bin/env python3
from pathlib import Path
import re
import math
from collections import defaultdict
from PIL import Image

ROOT = Path(".")
LEVELS = [1, 2, 3, 4, 5]

# Spacing
GAP_X = 24
GAP_Y = 24
MARGIN = 40

# Target aspect ratio (width/height): 16/9 is nice for screens
TARGET_AR = 16 / 9

OUT = "badge_poster_optimal.png"

pat = re.compile(r"badge-(?P<type>.+?)-level-(?P<level>[1-5])\.png$", re.I)

# Collect files: type -> level -> path
by_type = defaultdict(dict)
for p in ROOT.glob("Level-*/badge-*-level-*.png"):
    m = pat.match(p.name)
    if not m:
        continue
    t = m.group("type")
    lvl = int(m.group("level"))
    by_type[t][lvl] = p

types = sorted(by_type.keys())
if not types:
    raise SystemExit("No badge PNGs found. Expected Level-*/badge-*-level-*.png")

# Use first badge as canonical size
sample_path = next(iter(next(iter(by_type.values())).values()))
cell_w, cell_h = Image.open(sample_path).size

# A "tile" = one badge type row (5 badges side-by-side)
tile_w = len(LEVELS) * cell_w + (len(LEVELS) - 1) * GAP_X
tile_h = cell_h

n = len(types)

def poster_size(cols: int):
    """Return (w,h) for a grid of tiles with given number of columns."""
    cols = max(1, min(cols, n))
    rows = math.ceil(n / cols)
    w = MARGIN * 2 + cols * tile_w + (cols - 1) * GAP_X
    h = MARGIN * 2 + rows * tile_h + (rows - 1) * GAP_Y
    return w, h, rows

# Choose columns that best match target aspect ratio
best = None
for cols in range(1, min(n, 12) + 1):  # cap search at 12 columns (adjust if you want)
    w, h, rows = poster_size(cols)
    ar = w / h
    score = abs(ar - TARGET_AR)
    # tie-breaker: prefer fewer columns (usually easier to scan)
    cand = (score, cols, w, h, rows)
    if best is None or cand < best:
        best = cand

_, cols, poster_w, poster_h, rows = best

poster = Image.new("RGBA", (poster_w, poster_h), (0, 0, 0, 0))

# Render: fill tiles row-major (left-to-right, then next line)
for i, t in enumerate(types):
    grid_r = i // cols
    grid_c = i % cols

    origin_x = MARGIN + grid_c * (tile_w + GAP_X)
    origin_y = MARGIN + grid_r * (tile_h + GAP_Y)

    # paste 1..5 badges within the tile
    for j, lvl in enumerate(LEVELS):
        x = origin_x + j * (cell_w + GAP_X)
        y = origin_y
        fp = by_type[t].get(lvl)
        if not fp:
            continue
        img = Image.open(fp).convert("RGBA")
        poster.paste(img, (x, y), img)

poster.save(OUT)
print(f"Wrote {OUT}: {poster_w}x{poster_h}, tiles={n}, grid={cols}x{rows}, target_ar={TARGET_AR:.3f}, actual_ar={(poster_w/poster_h):.3f}")
