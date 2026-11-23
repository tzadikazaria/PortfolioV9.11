#!/usr/bin/env python3
"""Optimise supplied original images into assets/*.webp (+ -480/-960 variants) and log the source file.
usage: add_images.py SOURCE_DIR LOGFILE  name=source_filename:max_width ...
Originals are never modified; EXIF rotation is applied; images are converted to sRGB RGB."""
import os, sys, datetime
from PIL import Image, ImageOps
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src, log = sys.argv[1], sys.argv[2]
lines = []
for spec in sys.argv[3:]:
    name, rest = spec.split('=', 1)
    fname, maxw = rest.rsplit(':', 1)
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, fname))).convert('RGB')
    ow, oh = im.size
    w = min(int(maxw), ow)
    base = im.resize((w, round(oh * w / ow)), Image.LANCZOS) if w < ow else im
    base.save(f'{ROOT}/assets/{name}.webp', quality=82, method=6)
    sizes = [f'{w}x{base.height}']
    for v in (480, 960):
        if v < w:
            im.resize((v, round(oh * v / ow)), Image.LANCZOS).save(f'{ROOT}/assets/{name}-{v}.webp', quality=80, method=6)
    kb = os.path.getsize(f'{ROOT}/assets/{name}.webp') // 1024
    lines.append(f'| {name}.webp | {fname} | {ow}x{oh} | {w}x{base.height} | {kb} KB |')
    print(lines[-1])
new = not os.path.exists(log)
with open(log, 'a') as f:
    if new:
        f.write('# Image sources\n\n| Site file | Original file | Original size | Published size | Size |\n|---|---|---|---|---|\n')
    f.write('\n'.join(lines) + '\n')
