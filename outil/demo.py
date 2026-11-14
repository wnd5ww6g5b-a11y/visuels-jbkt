#!/usr/bin/env python3
"""Visuels JBKT à partir de la banque d'écrans (banque/jbkt/ecrans.json).

python3 outil/demo.py <demo> <dossier_sortie> [--reel]

Produit, pour une démo :
  - <demo>-post.jpg        : 1080 x 1350, titre + écrans dans leurs appareils
  - <demo>-story-<n>.jpg   : 1080 x 1920, un écran par story, avec sa légende
  - <demo>-reel.mp4        : (option --reel) les stories enchaînées, 3,2 s chacune, avec musique
Les textes viennent de banque/jbkt/series.json (titre, accroche, une phrase par écran).
Tout est marqué « Démo · données fictives » : ce ne sont pas des clients réels.
"""
import asyncio, base64, json, os, subprocess, sys
from playwright.async_api import async_playwright

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BANK = os.path.join(R, 'banque', 'jbkt')
A = os.path.join(R, 'outil', 'videos', 'assets')
C = dict(dark='#0B1533', light='#F3F7FF', alt='#E8F0FF', ink='#0B1533', muted_d='#9FB3DD', muted_l='#64748B', acc_d='#4FA3FF', acc_l='#087BFF')

def b64(p):
    return base64.b64encode(open(p, 'rb').read()).decode()

FONTS = ''.join(f"@font-face{{font-family:M;font-weight:{w};src:url(data:font/woff2;base64,{b64(os.path.join(A, f'manrope-latin-{w}-normal.woff2'))})}}" for w in (700, 800))
LOGO = b64(os.path.join(A, 'jbkt-logo-site.png'))

def img(p):
    return 'data:image/jpeg;base64,' + b64(os.path.join(BANK, p))

def device(e, w):
    """Un écran dans son appareil, largeur w (px)."""
    src, app = img(e['fichier']), e['appareil']
    if app == 'telephone':
        h = w * 2556 / 1179
        return f'<div class="ph" style="width:{w}px;height:{h + 28:.0f}px"><img src="{src}"></div>'
    if app == 'tablette':
        h = w * 1536 / 2048
        return f'<div class="tb" style="width:{w}px;height:{h + 36:.0f}px"><img src="{src}"></div>'
    h = w * 1800 / 2880
    return f'<div class="lp" style="width:{w}px"><div class="scr" style="height:{h + 24:.0f}px"><img src="{src}"></div><div class="base"></div></div>'

CSS = f"""{FONTS}
*{{margin:0;box-sizing:border-box}}
body{{font-family:M;letter-spacing:-0.02em;position:relative;overflow:hidden}}
img{{display:block}}
.ph{{background:#0d0f14;border-radius:64px;padding:14px;box-shadow:0 40px 80px rgba(11,21,51,.28)}}
.ph img{{width:100%;height:100%;border-radius:52px;object-fit:cover}}
.tb{{background:#0d0f14;border-radius:40px;padding:18px;box-shadow:0 40px 80px rgba(11,21,51,.25)}}
.tb img{{width:100%;height:100%;border-radius:24px;object-fit:cover}}
.lp .scr{{background:#0d0f14;border-radius:22px 22px 6px 6px;padding:12px;box-shadow:0 40px 80px rgba(11,21,51,.25)}}
.lp .scr img{{width:100%;height:100%;border-radius:10px;object-fit:cover;object-position:top}}
.lp .base{{height:20px;margin:0 -6%;background:linear-gradient(#cfd6e4,#a9b3c6);border-radius:0 0 26px 26px}}
.logo{{background:#fff;border-radius:22px;padding:12px 20px;display:inline-block}}
.logo img{{height:46px}}
.chip{{display:inline-block;font-weight:700;font-size:24px;padding:10px 18px;border-radius:999px}}
"""

def post_html(s, ecrans):
    main = next((e for e in ecrans if e['appareil'] != 'telephone'), ecrans[0])
    phone = next((e for e in ecrans if e['appareil'] == 'telephone' and e is not main), None)
    mw = 800 if main['appareil'] != 'telephone' else 330
    comp = f'<div style="position:absolute;left:{(1080 - mw) // 2 - (60 if phone else 0)}px;top:470px">{device(main, mw)}</div>'
    if phone:
        comp += f'<div style="position:absolute;right:56px;top:560px">{device(phone, 240)}</div>'
    return f"""<html><head><style>{CSS} body{{width:1080px;height:1350px;background:{C['light']};color:{C['ink']}}}</style></head><body>
<div style="position:absolute;left:70px;top:64px" class="logo"><img src="data:image/png;base64,{LOGO}"></div>
<div style="position:absolute;right:70px;top:76px;background:#fff;color:{C['muted_l']}" class="chip">Démo · données fictives</div>
<div style="position:absolute;left:70px;right:70px;top:210px">
 <div style="font-weight:800;font-size:30px;color:{C['acc_l']};letter-spacing:-0.01em">{s['cible']}</div>
 <div style="font-weight:800;font-size:68px;line-height:1.04;letter-spacing:-0.04em;margin-top:16px">{s['titre']}</div>
</div>
{comp}
<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:{C['dark']};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 70px">
 <span style="font-weight:800;font-size:32px">{s['cta']}</span><span style="font-weight:700;font-size:26px;color:{C['muted_d']}">Lien en bio</span></div>
</body></html>"""

def story_html(s, e, i, n):
    app = e['appareil']
    w = 440 if app == 'telephone' else (960 if app == 'tablette' else 1000)
    return f"""<html><head><style>{CSS} body{{width:1080px;height:1920px;background:{C['dark']};color:#fff}}</style></head><body>
<div style="position:absolute;left:70px;top:150px" class="logo"><img src="data:image/png;base64,{LOGO}"></div>
<div style="position:absolute;right:70px;top:164px;background:#16224A;color:{C['muted_d']}" class="chip">Démo · {i}/{n}</div>
<div style="position:absolute;left:70px;right:70px;top:300px">
 <div style="font-weight:800;font-size:30px;color:{C['acc_d']}">{s['cible']}</div>
 <div style="font-weight:800;font-size:60px;line-height:1.08;letter-spacing:-0.035em;margin-top:18px">{s['phrases'][i - 1]}</div>
</div>
<div style="position:absolute;left:0;right:0;top:{640 if app == 'telephone' else 760}px;display:flex;justify-content:center">{device(e, w)}</div>
<div style="position:absolute;left:0;right:0;bottom:120px;text-align:center;font-weight:700;font-size:26px;color:{C['muted_d']}">Exemple d'outil que nous construisons · données fictives</div>
</body></html>"""

async def render(jobs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for html, out, (w, h) in jobs:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            await pg.set_content(html)
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(250)
            await pg.screenshot(path=out, type='jpeg', quality=90)
            await pg.close()
        await b.close()

def reel(stories, out, musique='clair'):
    tmp = out + '.parts'
    os.makedirs(tmp, exist_ok=True)
    D, F = 3.2, 0.4
    parts = []
    for k, st in enumerate(stories):
        p = f'{tmp}/{k}.mp4'
        zoom = "zoompan=z='min(1+0.0006*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '30', '-t', str(D), '-i', st, '-vf',
                        f"scale=2160:-1,{zoom},format=yuv420p", '-t', str(D), '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', p], check=True)
        parts.append(p)
    # enchaînement en fondu
    inputs, filt, last = [], '', '[0:v]'
    for p in parts:
        inputs += ['-i', p]
    off = D - F
    for k in range(1, len(parts)):
        filt += f'{last}[{k}:v]xfade=transition=fade:duration={F}:offset={off:.2f}[v{k}];'
        last = f'[v{k}]'
        off += D - F
    total = len(parts) * D - (len(parts) - 1) * F
    mus = os.path.join(A, '..', 'music', f'{musique}.m4a')
    cmd = ['ffmpeg', '-v', 'error', '-y'] + inputs + ['-i', mus, '-filter_complex', filt.rstrip(';') if filt else 'null',
           '-map', last if filt else '0:v', '-map', f'{len(parts)}:a', '-t', f'{total:.2f}',
           '-af', f'afade=t=out:st={total - 1.2:.2f}:d=1.2', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast',
           '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    print(out, f'{total:.1f} s')

def main():
    demo, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    ecrans = next(d for d in json.load(open(os.path.join(BANK, 'ecrans.json'))) if d['demo'] == demo)['ecrans']
    s = json.load(open(os.path.join(BANK, 'series.json')))[demo]
    n = len(ecrans)
    jobs = [(post_html(s, ecrans), f'{dst}/{demo}-post.jpg', (1080, 1350))]
    jobs += [(story_html(s, e, i, n), f'{dst}/{demo}-story-{i}.jpg', (1080, 1920)) for i, e in enumerate(ecrans, 1)]
    asyncio.run(render(jobs))
    for _, o, _ in jobs:
        print(o)
    if '--reel' in sys.argv:
        reel([f'{dst}/{demo}-story-{i}.jpg' for i in range(1, n + 1)], f'{dst}/{demo}-reel.mp4', s.get('musique', 'clair'))

if __name__ == '__main__':
    main()
