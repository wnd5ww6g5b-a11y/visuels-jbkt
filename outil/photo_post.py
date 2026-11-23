#!/usr/bin/env python3
"""Post photo 1080 x 1350 : une photo (Higgsfield, gpt_image_2_6) + le texte et le logo dans la DA de la marque.

python3 outil/photo_post.py <post.json> <sortie.jpg>

post.json : {
  "brand": "gloova" | "jbkt" | "radar",
  "photo": "chemin/vers/photo.png",        # photo SANS texte (le texte de l'IA est toujours raté : on l'écrit nous-mêmes)
  "ton": "clair" | "sombre",               # clair = texte foncé sur une zone claire de la photo ; sombre = texte blanc
  "title": "…", "subtitle": "…", "cta": "…",
  "ia": true                                # mention « Image générée par IA » (obligatoire dès qu'une personne, même ses mains, est générée)
}
Règles : la photo ne montre jamais de texte lisible, de logo, de lieu précis, ni d'écran d'application de VTC.
"""
import asyncio, base64, json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get('FONTS_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'fonts'))
LOGOS = os.environ.get('LOGOS_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logos'))


def b64(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def font(face, fam, weight):
    return (f"@font-face{{font-family:'{fam}';font-weight:{weight};"
            f"src:url({b64(os.path.join(FONTS, face, 'files', f'{face}-latin-{weight}-normal.woff2'), 'font/woff2')})}}")


MARQUES = {
    'gloova': {'titre': ('plus-jakarta-sans', 'Jakarta', 600), 'texte': ('plus-jakarta-sans', 'Jakarta', 500),
               'logo_clair': 'gloova-fleur-noire.png', 'logo_sombre': 'gloova-fleur-blanche.png', 'nom': 'Gloova',
               'encre': '#1D1F20', 'fond_cta_clair': '#1D1F20', 'fond_cta_sombre': '#FFFFFF', 'rond': '#F3E2E0'},
    'jbkt': {'titre': ('manrope', 'Manrope', 800), 'texte': ('manrope', 'Manrope', 700),
             'logo_clair': 'jbkt-logo-site.png', 'logo_sombre': 'jbkt-logo-site.png', 'nom': '',
             'encre': '#0B1533', 'fond_cta_clair': '#087BFF', 'fond_cta_sombre': '#087BFF', 'rond': '#FFFFFF'},
    'radar': {'titre': ('manrope', 'Manrope', 800), 'texte': ('manrope', 'Manrope', 700),
              'logo_clair': 'radar-icone.png', 'logo_sombre': 'radar-icone.png', 'nom': 'Radar VTC',
              'encre': '#111418', 'fond_cta_clair': '#111418', 'fond_cta_sombre': '#FFFFFF', 'rond': '#E9EBEF'},
}
MARQUES['rideradar'] = dict(MARQUES['radar'], nom='Ride Radar')


def html(p):
    m = MARQUES[p['brand']]
    sombre = p.get('ton') == 'sombre'
    encre = '#FFFFFF' if sombre else m['encre']
    gris = 'rgba(255,255,255,.82)' if sombre else ('#5F666A' if p['brand'] == 'gloova' else '#3C4658')
    voile = ('linear-gradient(180deg, rgba(0,0,0,.62) 0%, rgba(0,0,0,.28) 38%, rgba(0,0,0,0) 58%, rgba(0,0,0,.35) 100%)' if sombre
             else 'linear-gradient(180deg, rgba(255,255,255,.80) 0%, rgba(255,255,255,.45) 34%, rgba(255,255,255,0) 55%)')
    logo = m['logo_sombre'] if sombre else m['logo_clair']
    # Le logo JBKT est en couleurs : sur fond sombre, on le pose sur une pastille blanche (règle du logo).
    logo_box = ('background:#fff;border-radius:18px;padding:14px 18px;' if p['brand'] == 'jbkt' and sombre else '')
    logo_h = {'jbkt': 84, 'radar': 64, 'rideradar': 64}.get(p['brand'], 58)
    cta_bg = m['fond_cta_sombre'] if sombre else m['fond_cta_clair']
    cta_fg = '#111418' if cta_bg == '#FFFFFF' else '#FFFFFF'
    t_fam, t_w = m['titre'][1], m['titre'][2]
    x_fam, x_w = m['texte'][1], m['texte'][2]
    fonts = font(*m['titre']) + font(*m['texte']) if m['titre'] != m['texte'] else font(*m['titre'])
    ia = ('<div style="position:absolute;right:44px;bottom:40px;font:500 22px Inter,sans-serif;'
          f'color:{"rgba(255,255,255,.85)" if sombre else "rgba(29,31,32,.7)"}">{"AI-generated image" if p['brand'] == 'rideradar' else "Image générée par IA"}</div>') if p.get('ia') else ''
    titre_style = ('letter-spacing:-0.03em;' if p['brand'] == 'gloova' else 'letter-spacing:-0.035em;')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{fonts}
*{{margin:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden}}
</style></head><body>
<div style="position:relative;width:1080px;height:1350px;background:#000 url({b64(p['photo'], 'image/jpeg' if p['photo'].lower().endswith(('.jpg','.jpeg')) else 'image/png')}) center/cover">
  <div style="position:absolute;inset:0;background:{voile}"></div>
  <div style="position:absolute;left:84px;right:96px;top:84px">
    <div style="display:flex;align-items:center;gap:16px;{logo_box}width:max-content">
      <img src="{b64(os.path.join(LOGOS, logo), 'image/png')}" style="height:{logo_h}px;{'border-radius:16px' if p['brand'] in ('radar', 'rideradar') else ''}">
      {f'<span style="font-family:{t_fam};font-weight:{t_w};font-size:40px;color:{encre};letter-spacing:-0.02em">{m["nom"]}</span>' if m['nom'] else ''}
    </div>
    <h1 style="margin-top:58px;font-family:{t_fam};font-weight:{t_w};font-size:{p.get('size', 84)}px;line-height:1.02;{titre_style}color:{encre}">{p['title']}</h1>
    <p style="margin-top:30px;font-family:{x_fam};font-weight:{x_w if p['brand'] != 'gloova' else 500};font-size:34px;line-height:1.32;color:{gris};max-width:840px">{p['subtitle']}</p>
  </div>
  <div style="position:absolute;left:84px;bottom:84px;display:flex;align-items:center;gap:18px;height:96px;padding:0 16px 0 40px;border-radius:999px;background:{cta_bg};color:{cta_fg};font-family:{x_fam};font-weight:700;font-size:32px">
    {p['cta']}
    <span style="width:64px;height:64px;border-radius:50%;background:{m['rond'] if cta_bg != '#FFFFFF' else '#111418'};display:flex;align-items:center;justify-content:center">
      <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="{'#111418' if cta_bg != '#FFFFFF' else '#FFFFFF'}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
    </span>
  </div>
  {ia}
</div></body></html>"""


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
