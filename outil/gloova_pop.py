#!/usr/bin/env python3
"""Nouvelle DA Gloova « Pop » (carte blanche de Karim, 18/11/2026) : vendeuse, très lisible, le produit en vrai.

python3 outil/gloova_pop.py <post.json> <sortie.jpg>

Palette : noir #141012, rose bonbon #FF5C93, blush #FFE1EA, crème #FFF7F2.
Typo : Bricolage Grotesque 800 (titres énormes, serrés) + Instrument Serif italique (la phrase qui touche) + Inter (texte).
Toujours : un vrai écran de l'app (jamais inventé), une offre claire, un bouton.

post.json :
  {"layout": "offre", "titre": "30 jours offerts.", "serif": "…", "puces": ["…"], "prix": "…", "cta": "…", "ecran": "chemin.png"}
  {"layout": "messages", "photo": "chemin.png", "bulles": ["…", "…"], "titre": "…", "serif": "…", "cta": "…", "ia": true}
  {"layout": "avant_apres", "titre": "…", "avant": ["…"], "apres": ["…"], "cta": "…", "ecran": "chemin.png"}
"""
import asyncio, base64, json, os, sys

FP = os.environ.get('GLOOVA_FONTS', '/tmp/fontpkg')
LOGO = os.environ.get('GLOOVA_LOGOS', '/home/claude/jbkt-studio/src/assets')
NOIR, ROSE, BLUSH, CREME = '#141012', '#FF5C93', '#FFE1EA', '#FFF7F2'


def b64(path, mime=None):
    mime = mime or ('image/png' if path.endswith('.png') else 'image/jpeg' if path.endswith(('.jpg', '.jpeg')) else 'font/woff2')
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def fonts():
    bg = os.path.join(FP, 'fontsource-bricolage-grotesque/files/bricolage-grotesque-latin-800-normal.woff2')
    se = os.path.join(FP, 'fontsource-instrument-serif/files/instrument-serif-latin-400-italic.woff2')
    return (f"@font-face{{font-family:Brico;font-weight:800;src:url({b64(bg, 'font/woff2')})}}"
            f"@font-face{{font-family:Serif;font-style:italic;src:url({b64(se, 'font/woff2')})}}")


def logo(clair=False):
    f = 'gloova-fleur-blanche.png' if clair else 'gloova-fleur-noire.png'
    c = CREME if clair else NOIR
    return (f'<div style="display:flex;align-items:center;gap:14px"><img src="{b64(os.path.join(LOGO, f))}" style="height:50px">'
            f'<span style="font:800 40px Brico;letter-spacing:-0.03em;color:{c}">Gloova</span></div>')


def phone(ecran, w=430, rot=0):
    h = int(w * 2868 / 1320)
    return (f'<div style="width:{w + 28}px;height:{h + 28}px;border-radius:{int(w * .16)}px;background:{NOIR};padding:14px;'
            f'transform:rotate({rot}deg);box-shadow:0 40px 80px rgba(20,16,18,.35)">'
            f'<div style="width:{w}px;height:{h}px;border-radius:{int(w * .14)}px;overflow:hidden;background:#fff url({b64(ecran)}) top/cover"></div></div>')


def cta(texte, fond=NOIR, fg=CREME):
    return (f'<div style="display:inline-flex;align-items:center;gap:18px;height:100px;padding:0 18px 0 44px;border-radius:999px;'
            f'background:{fond};color:{fg};font:600 34px Inter,sans-serif">{texte}'
            f'<span style="width:66px;height:66px;border-radius:50%;background:{ROSE};display:flex;align-items:center;justify-content:center">'
            f'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{NOIR}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>')


def sticker(l1, l2, fond=NOIR, fg=CREME, rot=-12, size=230):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{fond};color:{fg};transform:rotate({rot}deg);'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">'
            f'<div style="font:800 {int(size * .3)}px/0.9 Brico;letter-spacing:-0.04em">{l1}</div>'
            f'<div style="font:600 {int(size * .1)}px/1.1 Inter,sans-serif;margin-top:8px;max-width:{int(size * .7)}px">{l2}</div></div>')


def offre(p):
    puces = ''.join(
        f'<div style="display:flex;align-items:center;gap:16px;margin-top:20px;font:600 32px/1.2 Inter,sans-serif;color:{NOIR}">'
        f'<span style="flex:none;width:44px;height:44px;border-radius:50%;background:{NOIR};display:flex;align-items:center;justify-content:center">'
        f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{ROSE}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg></span>{x}</div>'
        for x in p['puces'])
    return f'''<div style="position:absolute;inset:0;background:{ROSE}"></div>
<div style="position:absolute;right:-120px;top:330px">{phone(p['ecran'], 470, 9)}</div>
<div style="position:absolute;left:80px;top:78px">{logo()}</div>
<div style="position:absolute;left:76px;top:190px;width:640px">
  <div style="font:800 168px/0.86 Brico;letter-spacing:-0.06em;color:{NOIR}">{p['titre']}</div>
  <div style="font:italic 58px/1.05 Serif;color:{NOIR};margin-top:26px">{p['serif']}</div>
  <div style="margin-top:34px">{puces}</div>
  <div style="margin-top:34px;font:600 28px Inter,sans-serif;color:{NOIR};opacity:.8">{p['prix']}</div>
</div>
<div style="position:absolute;left:80px;bottom:80px">{cta(p['cta'])}</div>'''


def messages(p):
    bulles = ''.join(
        f'<div style="align-self:flex-start;max-width:640px;background:#fff;color:{NOIR};border-radius:34px 34px 34px 10px;'
        f'padding:22px 30px;font:500 32px/1.3 Inter,sans-serif;box-shadow:0 14px 30px rgba(20,16,18,.18);margin-left:{40 * i}px">{b}'
        f'<div style="font:500 20px Inter,sans-serif;color:#8B8487;margin-top:6px">{["09:12", "09:47", "10:31", "11:05"][i % 4]}</div></div>'
        for i, b in enumerate(p['bulles']))
    ia = ('<div style="position:absolute;right:40px;top:40px;font:500 22px Inter,sans-serif;color:rgba(255,255,255,.9);'
          'background:rgba(20,16,18,.35);padding:8px 16px;border-radius:999px">Image générée par IA</div>') if p.get('ia') else ''
    return f'''<div style="position:absolute;inset:0 0 470px 0;background:#000 url({b64(p['photo'])}) center/cover"></div>
<div style="position:absolute;inset:0 0 470px 0;background:linear-gradient(180deg,rgba(20,16,18,.15),rgba(20,16,18,.45))"></div>
{ia}
<div style="position:absolute;left:70px;top:90px;display:flex;flex-direction:column;gap:18px">{bulles}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:500px;background:{NOIR};border-radius:56px 56px 0 0"></div>
<div style="position:absolute;right:70px;bottom:400px">{sticker("9,99 €", "TTC par mois, sans engagement", ROSE, NOIR, 10, 230)}</div>
<div style="position:absolute;left:80px;bottom:250px;width:860px">
  <div style="font:800 96px/0.92 Brico;letter-spacing:-0.05em;color:{CREME}">{p['titre']}</div>
  <div style="font:italic 50px/1.1 Serif;color:{ROSE};margin-top:16px">{p['serif']}</div>
</div>
<div style="position:absolute;left:80px;bottom:76px;display:flex;align-items:center;gap:30px">{cta(p['cta'], CREME, NOIR)}{logo(True)}</div>'''


def avant_apres(p):
    def col(titre, items, ok):
        ic = ('<path d="M5 12l5 5 9-10"/>' if ok else '<path d="M6 6l12 12M18 6L6 18"/>')
        rows = ''.join(
            f'<div style="display:flex;gap:14px;align-items:flex-start;margin-top:22px;font:500 30px/1.25 Inter,sans-serif;color:{NOIR if ok else "#6E6669"}">'
            f'<svg style="flex:none;margin-top:2px" width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="{ROSE if ok else "#B9B1B4"}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{ic}</svg>{x}</div>'
            for x in items)
        return (f'<div style="flex:1;background:{"#fff" if ok else "transparent"};border:{"0" if ok else "3px dashed #D9CFD2"};border-radius:40px;padding:40px 36px">'
                f'<div style="font:800 46px Brico;letter-spacing:-0.03em;color:{NOIR}">{titre}</div>{rows}</div>')
    return f'''<div style="position:absolute;inset:0;background:{CREME}"></div>
<div style="position:absolute;left:80px;top:78px">{logo()}</div>
<div style="position:absolute;left:76px;top:180px;right:76px;font:800 118px/0.9 Brico;letter-spacing:-0.055em;color:{NOIR}">{p['titre']}</div>
<div style="position:absolute;left:76px;right:76px;top:520px;display:flex;gap:24px">{col("Avant", p["avant"], False)}{col("Avec Gloova", p["apres"], True)}</div>
<div style="position:absolute;left:80px;bottom:80px">{cta(p['cta'])}</div>'''


def html(p):
    body = {'offre': offre, 'messages': messages, 'avant_apres': avant_apres}[p['layout']](p)
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>{fonts()}*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1350px;overflow:hidden}}</style></head>
<body><div style="position:relative;width:1080px;height:1350px;overflow:hidden">{body}</div></body></html>'''


async def render(p, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        await pg.set_content(html(p), wait_until='load')
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=out + '.png')
        await b.close()
    from PIL import Image
    Image.open(out + '.png').convert('RGB').save(out, 'JPEG', quality=92, optimize=True)
    os.remove(out + '.png')


if __name__ == '__main__':
    asyncio.run(render(json.load(open(sys.argv[1], encoding='utf-8')), sys.argv[2]))
    print(sys.argv[2])
