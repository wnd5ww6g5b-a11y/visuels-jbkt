#!/usr/bin/env python3
"""Dessine un post en JPEG 1080 x 1350.
Usage : python3 rendre.py post.json sortie.jpg
post.json = {"brand": "gloova", "content": {...}}  (un contenu de l'outil marketing)
"""
import base64, json, os, subprocess, sys, tempfile
from PIL import Image

ici = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
data = json.load(open(src, encoding='utf-8'))
h = base64.urlsafe_b64encode(json.dumps(data, ensure_ascii=False).encode('utf-8')).decode().rstrip('=')
url = 'file://' + os.path.join(ici, 'rendu.html') + '#' + h
chrome = next(c for c in ['google-chrome', 'chromium', 'chromium-browser'] if subprocess.run(['which', c], capture_output=True).returncode == 0)
with tempfile.TemporaryDirectory() as t:
    png = os.path.join(t, 'p.png')
    subprocess.run([chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
                    '--force-device-scale-factor=1', '--window-size=1080,1350', '--virtual-time-budget=8000',
                    f'--screenshot={png}', url], check=True, capture_output=True, timeout=90)
    im = Image.open(png).convert('RGB').crop((0, 0, 1080, 1350))
    im.save(out, 'JPEG', quality=90, optimize=True)
print(out)
