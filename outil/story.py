#!/usr/bin/env python3
"""Fait la story d'un post : le visuel du post (1080 x 1350) posé sur un fond flouté, en 1080 x 1920.
Usage : python3 outil/story.py post.jpg story.jpg
Rien n'est redessiné : c'est le post lui-même, pour renvoyer vers le fil.
"""
import sys
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

src, out = sys.argv[1], sys.argv[2]
post = Image.open(src).convert('RGB')
W, H = 1080, 1920
# fond : le post agrandi, flouté et assombri
bg = post.resize((W, int(W * post.height / post.width)), Image.LANCZOS)
scale = H / bg.height
bg = bg.resize((int(bg.width * scale), H), Image.LANCZOS)
x = (bg.width - W) // 2
bg = bg.crop((x, 0, x + W, H)).filter(ImageFilter.GaussianBlur(40))
bg = ImageEnhance.Brightness(bg).enhance(0.55)
# carte : le post en 940 px de large, coins arrondis, ombre douce
cw = 940
ch = int(cw * post.height / post.width)
card = post.resize((cw, ch), Image.LANCZOS)
mask = Image.new('L', (cw, ch), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=36, fill=255)
cx, cy = (W - cw) // 2, (H - ch) // 2
shadow = Image.new('L', (W, H), 0)
ImageDraw.Draw(shadow).rounded_rectangle((cx, cy + 18, cx + cw, cy + ch + 18), radius=36, fill=150)
shadow = shadow.filter(ImageFilter.GaussianBlur(30))
bg.paste(Image.new('RGB', (W, H), (0, 0, 0)), (0, 0), shadow)
bg.paste(card, (cx, cy), mask)
bg.save(out, 'JPEG', quality=90, optimize=True)
print(out)
