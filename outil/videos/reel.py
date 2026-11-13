#!/usr/bin/env python3
"""Rend un reel 9:16 animé (style des pubs Gloova) à partir d'une fiche JSON, avec musique.

  python3 outil/videos/reel.py fiche.json sortie.mp4 [--musique clair|calme|elan] [--apercus apercus.json]

La fiche suit le format de exemple-radar.json / exemple-jbkt.json (voir REELS.md).
--apercus écrit 3 petites images (data URI JPEG) pour l'aperçu dans l'outil.
"""
import sys, json, base64, io, subprocess, argparse
from pathlib import Path

ICI = Path(__file__).parent
sys.path.insert(0, str(ICI))
import anim  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('fiche'); ap.add_argument('sortie')
ap.add_argument('--musique', default='clair'); ap.add_argument('--apercus')
a = ap.parse_args()

v = json.load(open(a.fiche, encoding='utf-8'))
v.setdefault('id', Path(a.sortie).stem)
anim.OUT = ICI / 'tmp'
anim.OUT.mkdir(exist_ok=True)
vid, total, rc = anim.render(v)
if rc != 0:
    sys.exit(f'rendu échoué ({rc})')
src = anim.OUT / f'{vid}.mp4'
out = Path(a.sortie); out.parent.mkdir(parents=True, exist_ok=True)
tmp = out.with_suffix('.part.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-i', str(ICI / 'music' / f'{a.musique}.m4a'),
                '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-af', f'afade=t=in:d=0.4,afade=t=out:st={total - 1.6:.2f}:d=1.6',
                '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(tmp)], check=True)
tmp.rename(out)
src.unlink(missing_ok=True)

if a.apercus:
    from PIL import Image
    thumbs = []
    for t in (1.6, total * 0.45, total - 1.5):
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', str(out), '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-'],
                           capture_output=True, check=True)
        im = Image.open(io.BytesIO(r.stdout)).convert('RGB').resize((108, 192))
        b = io.BytesIO(); im.save(b, 'JPEG', quality=45, optimize=True)
        thumbs.append('data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode())
    json.dump(thumbs, open(a.apercus, 'w'))
print(out, f'{total:.1f}s')
