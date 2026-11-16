#!/usr/bin/env python3
"""Carrousel « utile » (à enregistrer ou à partager), 1080 x 1350, pour gloova, jbkt ou radar.

Usage : python3 outil/carrousel.py <spec.json> <dossier-sortie>
spec.json :
{
  "brand": "gloova" | "jbkt" | "radar",
  "slug": "nom-court",                       # fichiers : <slug>-1.jpg, <slug>-2.jpg, ...
  "slides": [
    {"type": "cover", "kicker": "Astuce", "title": "Titre fort", "sub": "Phrase courte", "swipe": "Fais défiler →"},
    {"type": "tip", "title": "Conseil 1", "text": "Explication courte", "example": "Texte à copier (facultatif)"},
    ...
    {"type": "end", "title": "Enregistre ce post", "text": "pour l'avoir sous la main", "cta": "Envoie-le à une collègue"}
  ]
}
Règles : 5 à 8 slides, une idée par slide, rien d'inventé, pas de chiffre sans source.
Couleurs : Gloova = beige et rose doux (#F4F2ED / #EFE3DF, encre #1E1F21, jamais de violet ni d'orange vif),
JBKT = DA des démos (#F3F7FF, nuit #0B1533, bleu #087BFF, Manrope), Radar = gris clair / anthracite / vert.
"""
import json, os, sys, base64, asyncio
from playwright.async_api import async_playwright

ICI = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ICI, 'videos', 'assets')

def b64(p):
    return base64.b64encode(open(p, 'rb').read()).decode()

def font(fam, file, w):
    return f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64(os.path.join(A, file))})}}"

ST = {
    'gloova': dict(bg=['linear-gradient(160deg,#F4F2ED 0%,#F3EEEA 55%,#EFE3DF 100%)', '#EFE3DF'], ink='#1E1F21', sub='rgba(30,31,33,.6)',
                   acc='#1E1F21', card='#FFFFFF', end_bg='#1F2124', end_ink='#FFFFFF', end_sub='rgba(255,255,255,.65)',
                   fam='J', fonts=[('J', 'plus-jakarta-sans-latin-500-normal.woff2', 500), ('J', 'plus-jakarta-sans-latin-600-normal.woff2', 600), ('J', 'plus-jakarta-sans-latin-700-normal.woff2', 700)],
                   logo='gloova-logo-noir.png', logo_end='gloova-logo-blanc.png', logo_w=200, pill=False, title_w=600),
    'jbkt': dict(bg=['#F3F7FF', '#F3F7FF'], ink='#0B1533', sub='#64748B', acc='#087BFF', card='#FFFFFF', end_bg='#0B1533', end_ink='#FFFFFF', end_sub='#9FB3DD',
                 fam='Manrope', fonts=[('Manrope', 'manrope-latin-700-normal.woff2', 700), ('Manrope', 'manrope-latin-800-normal.woff2', 800)],
                 logo='jbkt-logo-site.png', logo_end='jbkt-logo-site.png', logo_w=170, pill=True, title_w=800),
    'radar': dict(bg=['#F2F3F5', '#F2F3F5'], ink='#1E2124', sub='#6B7075', acc='#2FB45F', card='#FFFFFF', end_bg='#1E2124', end_ink='#FFFFFF', end_sub='#A3A8AD',
                  fam='Inter', fonts=[], logo='radar-logo-clair.png', logo_end='radar-logo-sombre.png', logo_w=190, pill=False, title_w=700),
}

def page(s, sl, i, n):
    t = sl['type']
    dark = t == 'end'
    bg = s['end_bg'] if dark else s['bg'][0 if t == 'cover' else 1]
    ink = s['end_ink'] if dark else s['ink']
    sub = s['end_sub'] if dark else s['sub']
    logo = s['logo_end'] if dark else s['logo']
    logo_html = f'<img class=logo src="data:image/png;base64,{b64(os.path.join(A, logo))}">'
    if s['pill']:
        logo_html = f'<div class=pill>{logo_html}</div>'
    num = f'<div class=num>{i}/{n}</div>'
    if t == 'cover':
        body = f"""<div class=kick>{sl.get('kicker','')}</div><h1>{sl['title']}</h1><p class=sub>{sl.get('sub','')}</p>
        <div class=swipe>{sl.get('swipe','Fais défiler →')}</div>"""
    elif t == 'tip':
        ex = f"<div class=ex>{sl['example']}</div>" if sl.get('example') else ''
        body = f"""<div class=big>{i-1}</div><h2>{sl['title']}</h2><p class=txt>{sl.get('text','')}</p>{ex}"""
    else:
        body = f"""<h1 class=endt>{sl['title']}</h1><p class=sub>{sl.get('text','')}</p><div class=cta>{sl.get('cta','')}</div>"""
    fonts = ''.join(font(*f) for f in s['fonts'])
    fam = s['fam']
    return f"""<html><head><style>{fonts}
*{{margin:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:{bg};color:{ink};font-family:{fam},Inter,system-ui,sans-serif;letter-spacing:-0.02em;position:relative;overflow:hidden}}
.logo{{width:{s['logo_w']}px;display:block}}
.pill{{position:absolute;top:64px;left:72px;background:#fff;border-radius:18px;padding:12px 18px}} .pill .logo{{width:150px}}
body>.logo{{position:absolute;top:72px;left:72px}}
.num{{position:absolute;top:78px;right:72px;font-weight:600;font-size:26px;color:{sub}}}
.kick{{position:absolute;top:250px;left:72px;font-weight:600;font-size:30px;color:{s['acc'] if not dark else sub};text-transform:none}}
h1{{position:absolute;top:310px;left:72px;right:72px;font-weight:{s['title_w']};font-size:96px;line-height:1.02;letter-spacing:-0.045em}}
.endt{{top:380px}}
.sub{{position:absolute;left:72px;right:120px;top:auto;bottom:430px;font-weight:500;font-size:36px;line-height:1.4;color:{sub}}}
.swipe{{position:absolute;bottom:90px;right:72px;font-weight:600;font-size:30px;color:{sub}}}
.big{{position:absolute;top:220px;left:72px;font-weight:{s['title_w']};font-size:150px;line-height:1;color:{s['acc']}}}
h2{{position:absolute;top:420px;left:72px;right:72px;font-weight:{s['title_w']};font-size:72px;line-height:1.05;letter-spacing:-0.04em}}
.txt{{position:absolute;top:640px;left:72px;right:90px;font-weight:500;font-size:36px;line-height:1.45;color:{sub}}}
.ex{{position:absolute;left:72px;right:72px;bottom:110px;background:{s['card']};border-radius:28px;padding:34px 38px;font-weight:500;font-size:32px;line-height:1.45;color:{ink};box-shadow:0 12px 30px rgba(0,0,0,.05)}}
.cta{{position:absolute;left:72px;bottom:110px;border:2px solid {sub};border-radius:60px;padding:22px 36px;font-weight:600;font-size:32px}}
</style></head><body>{logo_html}{num}{body}</body></html>"""

async def main():
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    s = ST[spec['brand']]
    n = len(spec['slides'])
    async with async_playwright() as p:
        exe = next((c for c in ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'] if os.path.exists(c)), None)
        br = await p.chromium.launch(**({'executable_path': exe} if exe else {}))
        pg = await br.new_page(viewport={'width': 1080, 'height': 1350})
        for i, sl in enumerate(spec['slides'], 1):
            await pg.set_content(page(s, sl, i, n))
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(150)
            png = os.path.join(out, f"{spec['slug']}-{i}.png")
            await pg.screenshot(path=png)
            from PIL import Image
            Image.open(png).convert('RGB').save(png[:-4] + '.jpg', 'JPEG', quality=90, optimize=True)
            os.remove(png)
            print(png[:-4] + '.jpg')
        await br.close()

asyncio.run(main())
