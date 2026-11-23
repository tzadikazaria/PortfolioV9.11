#!/usr/bin/env python3
"""Builds 1200x630 Open Graph images from existing portfolio images only (no new artwork)."""
import os
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
A = ROOT + '/assets/'
W, H = 1200, 630

def load(n):
    im = Image.open(A + n + '.webp')
    return im.convert('RGBA')

def paste(canvas, im, x, y):
    canvas.paste(im, (x, y), im)

def row(bg, names, h, gap=24):
    c = Image.new('RGBA', (W, H), bg)
    ims = []
    for n in names:
        im = load(n); w = round(im.width * h / im.height)
        ims.append(im.resize((w, h), Image.LANCZOS))
    total = sum(i.width for i in ims) + gap * (len(ims) - 1)
    x = (W - total) // 2; y = (H - h) // 2
    for i in ims:
        paste(c, i, x, y); x += i.width + gap
    return c

def cover(bg, name):
    c = Image.new('RGBA', (W, H), bg)
    im = load(name); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    paste(c, im, (W - im.width) // 2, (H - im.height) // 2)
    return c

def contain(bg, name, pad=0):
    c = Image.new('RGBA', (W, H), bg)
    im = load(name); s = min((W - 2*pad) / im.width, (H - 2*pad) / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    paste(c, im, (W - im.width) // 2, (H - im.height) // 2)
    return c

OUT = {
  'og-home': row('#F3F3F2', ['campaign-04', 'marketplace-09', 'campaign-16'], 360, 24),
  'og-campaign': row('#FFFFFF', ['campaign-04', 'campaign-01', 'campaign-03'], 360, 24),
  'og-marketplace': row('#E8E4DE', ['marketplace-09', 'marketplace-02', 'marketplace-11'], 360, 24),
  'og-hatachana': cover('#ECBA40', 'hatachana-00'),
  'og-sambusak': contain('#DDDADF', 'home-07-cut'),
}
os.makedirs(A + 'og', exist_ok=True)
for k, v in OUT.items():
    v.convert('RGB').save(A + f'og/{k}.jpg', quality=86, optimize=True, progressive=True)
    print(k, os.path.getsize(A + f'og/{k}.jpg') // 1024, 'KB')
