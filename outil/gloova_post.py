#!/usr/bin/env python3
"""Posts Gloova 1080 x 1350 dans la DA d'origine (charte-gloova) : crème, rose poudré, noir, Plus Jakarta Sans.

python3 outil/gloova_post.py <post.json> <sortie.jpg>

Mises en page :
- "ecran" : vrai écran de l'app dans un iPhone (ratio exact 1320 x 2868) + titre + 3 points cochés.
  {"layout":"ecran","fond":"creme|rose","title","subtitle","checks":[3 textes],"ecran":"iphone-cliente.png","cta"}
- "prix"  : les 3 formules réelles (Pro, Pro+, Ultra) en cartes blanches.
  {"layout":"prix","title","subtitle","cta"}
Règles : seulement des fonctions réelles, « sans commission sur vos rendez-vous » (jamais « 0 % »),
prix TTC 9,99 / 13,99 / 15,99 €, essai 30 jours, mention « Données fictives » sur les écrans de démo.
"""
import asyncio, base64, json, os, sys

FONTS = os.environ.get('FONTS_DIR', '/home/claude/jbkt-studio/node_modules/@fontsource')
LOGOS = os.environ.get('LOGOS_DIR', '/home/claude/jbkt-studio/src/assets')
ECRANS = os.environ.get('ECRANS_DIR', '/home/claude/gloomy-site/public/images/app')

NOIR, CREME, ROSE, FLEUR, GRIS, BORD = '#1D1F20', '#F6F2EE', '#F3E2E0', '#E2A9A2', '#6D7478', '#DFDBD8'


def b64(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def font(w):
    f = os.path.join(FONTS, 'plus-jakarta-sans', 'files', f'plus-jakarta-sans-latin-{w}-normal.woff2')
    return f"@font-face{{font-family:J;font-weight:{w};src:url({b64(f, 'font/woff2')})}}"


CHECK = ('<span style="flex:none;width:52px;height:52px;border-radius:50%;background:{bg};display:flex;'
         'align-items:center;justify-content:center"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" '
         'stroke="#1D1F20" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg></span>')


def entete():
    return (f'<div style="display:flex;align-items:center;gap:14px"><img src="{b64(os.path.join(LOGOS, "gloova-fleur-noire.png"), "image/png")}" '
            f'style="height:54px"><span style="font:700 38px J;letter-spacing:-.02em;color:{NOIR}">Gloova</span></div>')


def cta(txt):
    return (f'<div style="display:inline-flex;align-items:center;gap:18px;height:92px;padding:0 14px 0 38px;border-radius:999px;'
            f'background:{NOIR};color:#fff;font:700 31px J">{txt}<span style="width:64px;height:64px;border-radius:50%;background:#fff;'
            'display:flex;align-items:center;justify-content:center"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" '
            f'stroke="{NOIR}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>')


def iphone(src, w):
    b = round(w * .045)
    sw = w - 2 * b
    sh = round(sw * 2868 / 1320)
    return (f'<div style="width:{w}px;height:{sh + 2 * b}px;padding:{b}px;border-radius:{round(w * .17)}px;background:{NOIR};'
            'box-shadow:0 40px 80px -30px rgba(29,31,32,.35)">'
            f'<div style="width:{sw}px;height:{sh}px;border-radius:{round(w * .13)}px;overflow:hidden;background:#fff">'
            f'<img src="{b64(os.path.join(ECRANS, src), "image/png")}" style="width:100%;height:100%;display:block"></div></div>')


def ecran(p):
    fond = ROSE if p.get('fond') == 'rose' else CREME
    pastille = '#fff' if p.get('fond') == 'rose' else ROSE
    checks = ''.join(f'<div style="display:flex;align-items:center;gap:20px;font:600 30px/1.25 J;color:{NOIR}">'
                     f'{CHECK.format(bg=pastille)}<span>{c}</span></div>' for c in p['checks'])
    return f"""<div style="position:relative;width:1080px;height:1350px;background:{fond};overflow:hidden">
  <div style="position:absolute;left:80px;top:80px">{entete()}</div>
  <div style="position:absolute;left:80px;top:196px;width:500px">
    <h1 style="font:700 {p.get('size', 72)}px/1.04 J;letter-spacing:-.03em;color:{NOIR}">{p['title']}</h1>
    <p style="margin-top:26px;font:500 30px/1.38 J;color:{GRIS}">{p['subtitle']}</p>
    <div style="margin-top:46px;display:flex;flex-direction:column;gap:22px">{checks}</div>
  </div>
  <div style="position:absolute;left:612px;top:200px;transform:rotate(4deg)">{iphone(p['ecran'], 410)}</div>
  <div style="position:absolute;left:80px;bottom:80px">{cta(p['cta'])}</div>
  <div style="position:absolute;left:80px;bottom:36px;font:500 20px J;color:{GRIS}">Écran de l'app, données fictives</div>
</div>"""


def prix(p):
    formules = [('Pro', '9,99', "L'essentiel pour gérer votre institut"),
                ('Pro+', '13,99', 'Tout Pro, plus les fonctions avancées'),
                ('Ultra', '15,99', 'Tout Pro+, plus la gestion multi-équipe')]
    cartes = ''.join(
        f'<div style="display:flex;align-items:center;justify-content:space-between;padding:28px 40px;border-radius:32px;'
        f'background:#fff;border:2px solid {BORD}"><div><div style="font:700 38px J;letter-spacing:-.02em;color:{NOIR}">Gloova {n}</div>'
        f'<div style="margin-top:8px;font:500 26px J;color:{GRIS}">{d}</div></div>'
        f'<div style="text-align:right;white-space:nowrap"><span style="font:700 56px J;letter-spacing:-.04em;color:{NOIR}">{px} €</span>'
        f'<div style="font:500 22px J;color:{GRIS}">TTC par mois</div></div></div>' for n, px, d in formules)
    return f"""<div style="position:relative;width:1080px;height:1350px;background:{CREME};overflow:hidden">
  <div style="position:absolute;left:80px;top:80px">{entete()}</div>
  <div style="position:absolute;left:80px;right:80px;top:180px">
    <h1 style="font:700 {p.get('size', 76)}px/1.04 J;letter-spacing:-.03em;color:{NOIR}">{p['title']}</h1>
    <p style="margin-top:26px;font:500 31px/1.38 J;color:{GRIS};max-width:820px">{p['subtitle']}</p>
    <div style="margin-top:40px;display:flex;flex-direction:column;gap:18px">{cartes}</div>
    <div style="margin-top:30px;display:flex;gap:14px;flex-wrap:wrap">
      {''.join(f'<span style="padding:14px 26px;border-radius:999px;background:{ROSE};font:600 25px J;color:{NOIR}">{t}</span>' for t in ['30 jours d’essai gratuit', 'Sans commission sur vos rendez-vous', 'Sans engagement'])}
    </div>
  </div>
  <div style="position:absolute;left:80px;bottom:80px">{cta(p['cta'])}</div>
</div>"""


def importer(p):
    """Illustration (pas une capture) : un export de fichier clientes devient la liste Gloova, sans doublons."""
    lignes = [('Camille R.', '06 •• •• •• 12'), ('Ines M.', '06 •• •• •• 48'), ('Camille R.', '06 •• •• •• 12'),
              ('Sarah P.', '07 •• •• •• 03'), ('Chloé B.', '06 •• •• •• 77')]
    csv = ''.join(f'<div style="display:flex;justify-content:space-between;padding:14px 22px;border-top:1px solid {BORD};'
                  f'font:500 24px J;color:{NOIR};{"background:#FBEDEB" if i == 2 else ""}"><span>{n}</span><span style="color:{GRIS}">{t}</span></div>'
                  for i, (n, t) in enumerate(lignes))
    uniques = [l for i, l in enumerate(lignes) if i != 2]
    gl = ''.join(f'<div style="display:flex;align-items:center;gap:16px;padding:12px 0;font:600 25px J;color:{NOIR}">'
                 f'<span style="width:46px;height:46px;border-radius:50%;background:{ROSE};display:flex;align-items:center;justify-content:center;font:700 20px J">{n[0]}</span>{n}</div>'
                 for n, _ in uniques)
    return f"""<div style="position:relative;width:1080px;height:1350px;background:{CREME};overflow:hidden">
  <div style="position:absolute;left:80px;top:80px">{entete()}</div>
  <div style="position:absolute;left:80px;right:80px;top:196px">
    <h1 style="font:700 {p.get('size', 72)}px/1.04 J;letter-spacing:-.03em;color:{NOIR}">{p['title']}</h1>
    <p style="margin-top:24px;font:500 30px/1.38 J;color:{GRIS};max-width:860px">{p['subtitle']}</p>
  </div>
  <div style="position:absolute;left:80px;top:660px;width:430px;border-radius:28px;background:#fff;border:2px solid {BORD};overflow:hidden">
    <div style="padding:18px 22px;font:700 24px J;color:{NOIR}">Votre export Excel ou CSV</div>{csv}
    <div style="padding:14px 22px;border-top:1px solid {BORD};font:500 21px J;color:#B5655C">1 doublon</div>
  </div>
  <div style="position:absolute;left:512px;top:870px;width:56px;height:56px;border-radius:50%;background:{NOIR};display:flex;align-items:center;justify-content:center">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>
  <div style="position:absolute;left:570px;top:660px;width:430px;border-radius:28px;background:#fff;border:2px solid {BORD};padding:18px 28px">
    <div style="font:700 24px J;color:{NOIR};margin-bottom:6px">Vos clientes dans Gloova</div>{gl}
    <div style="margin-top:8px;display:inline-block;padding:10px 20px;border-radius:999px;background:{ROSE};font:600 21px J;color:{NOIR}">Sans doublons</div>
  </div>
  <div style="position:absolute;left:80px;bottom:80px">{cta(p['cta'])}</div>
  <div style="position:absolute;right:80px;bottom:46px;font:500 20px J;color:{GRIS}">Illustration, données fictives</div>
</div>"""


def html(p):
    corps = {'ecran': ecran, 'prix': prix, 'import': importer}[p['layout']](p)
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{font(500)}{font(600)}{font(700)}'
            '*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden}</style></head>'
            f'<body>{corps}</body></html>')


async def render(p, out):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        await pg.set_content(html(p), wait_until='load')
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=out + '.png')
        await b.close()
    from PIL import Image
    Image.open(out + '.png').convert('RGB').save(out, 'JPEG', quality=92, optimize=True)
    os.remove(out + '.png')


if __name__ == '__main__':
    asyncio.run(render(json.load(open(sys.argv[1], encoding='utf-8')), sys.argv[2]))
    print(sys.argv[2])
