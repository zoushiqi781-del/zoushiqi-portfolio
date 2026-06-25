# -*- coding: utf-8 -*-
"""
Split each 配件 image (left=idle, right=hover, white bg) into two transparent PNGs.
Removes the white background via edge flood-fill, then autocrops to the object.
Output: public/objects/objN_idle.png / objN_hover.png  (N=1..7)
"""
import os, glob
import numpy as np
from PIL import Image, ImageDraw

SRC = r"C:\Users\35512\Desktop\作品集配件"
DST = r"D:\clawd\shiqi-portfolio\public\objects"
os.makedirs(DST, exist_ok=True)

def remove_white_bg(rgb):
    """Flood-fill white background from all 4 corners -> transparent."""
    im = rgb.copy()
    w, h = im.size
    sentinel = (255, 0, 255)
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
                 (w // 2, 0), (w // 2, h - 1)]:
        ImageDraw.floodfill(im, seed, sentinel, thresh=42)
    arr = np.array(im)
    mask = ~np.all(arr == np.array(sentinel), axis=-1)  # True = keep
    rgba = np.dstack([np.array(rgb), (mask * 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA")

def autocrop(rgba):
    a = np.array(rgba)[:, :, 3]
    ys, xs = np.where(a > 10)
    if len(xs) == 0:
        return rgba
    pad = 12
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad, rgba.width)
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad, rgba.height)
    return rgba.crop((x0, y0, x1, y1))

files = sorted(glob.glob(os.path.join(SRC, "*")))
print(f"found {len(files)} source images")
for i, fp in enumerate(files, 1):
    img = Image.open(fp).convert("RGB")
    w, h = img.size
    mid = w // 2
    for half, tag in [((0, 0, mid, h), "idle"), ((mid, 0, w, h), "hover")]:
        part = img.crop(half)
        cut = autocrop(remove_white_bg(part))
        out = os.path.join(DST, f"obj{i}_{tag}.png")
        cut.save(out)
    print(f"obj{i}: {os.path.basename(fp)[:16]} -> idle+hover  (idle size {cut.size})")
print("done ->", DST)
