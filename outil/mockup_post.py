#!/usr/bin/env python3
"""Post 1080 x 1350 avec des écrans posés dans des appareils (ordinateur, tablette, téléphone), au bon format.

python3 outil/mockup_post.py <post.json> <sortie.jpg>

post.json :
  {"brand": "jbkt" | "radar", "fond": "clair" | "sombre", "title": "…", "subtitle": "…", "cta": "…",
   "mention": "Démo · données fictives",
   "devices": [ {"type": "laptop" | "tablet" | "phone", "src": "chemin.jpg" | null, "html": "<div>…</div>" | null,
                 "x": 80, "y": 560, "w": 760, "rot": 0, "z": 1} ]}

Chaque cadre a EXACTEMENT les proportions de son écran (ordinateur 2880 x 1800, tablette 2048 x 1536,
téléphone 1179 x 2556) : l'image n'est jamais étirée ni coupée. Un écran « html » (Radar) est dessiné au format téléphone.
"""
import asyncio, base64, json, os, sys

FONTS = os.environ.get('FONTS_DIR', '/home/claude/jbkt-studio/node_modules/@fontsource')
LOGOS = os.environ.get('LOGOS_DIR', '/home/claude/jbkt-studio/src/assets')
RATIO = {'laptop': 1800 / 2880, 'tablet': 1536 / 2048, 'phone': 2556 / 1179}


def b64(path):
    ext = path.rsplit('.', 1)[-1].lower()
    mime = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'woff2': 'font/woff2'}[ext]
    return f'data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def font(w):
    return f"@font-face{{font-family:Manrope;font-weight:{w};src:url({b64(os.path.join(FONTS, 'manrope/files', f'manrope-latin-{w}-normal.woff2'))})}}"


def screen(d, w, h, radius):
    inner = (f'<div style="width:{w}px;height:{h}px;border-radius:{radius}px;overflow:hidden;background:#fff">{d["html"]}</div>' if d.get('html')
             else f'<img src="{b64(d["src"])}" style="display:block;width:{w}px;height:{h}px;border-radius:{radius}px;object-fit:cover">')
    return inner


def device(d):
    t, w = d['type'], d['w']
    pos = f'position:absolute;left:{d["x"]}px;top:{d["y"]}px;z-index:{d.get("z", 1)};transform:rotate({d.get("rot", 0)}deg);transform-origin:center'
    shadow = 'box-shadow:0 34px 70px rgba(11,21,51,.28), 0 8px 18px rgba(11,21,51,.12)'
    if t == 'phone':
        b = max(10, int(w * .045))
        sw, sh = w - 2 * b, int((w - 2 * b) * RATIO['phone'])
        r = int(sw * .13)
        return (f'<div style="{pos};width:{w}px;height:{sh + 2 * b}px;border-radius:{r + b}px;background:#0E0F12;padding:{b}px;{shadow}">'
                f'{screen(d, sw, sh, r)}'
                f'<div style="position:absolute;left:50%;top:{b + int(sw * .025)}px;transform:translateX(-50%);width:{int(sw * .3)}px;height:{int(sw * .085)}px;border-radius:999px;background:#0E0F12"></div></div>')
    if t == 'tablet':
        b = int(w * .03)
        sw, sh = w - 2 * b, int((w - 2 * b) * RATIO['tablet'])
        return (f'<div style="{pos};width:{w}px;height:{sh + 2 * b}px;border-radius:{int(w * .05)}px;background:#0E0F12;padding:{b}px;{shadow}">'
                f'{screen(d, sw, sh, int(w * .022))}</div>')
    # ordinateur : écran + charnière + base
    b = int(w * .022)
    sw, sh = w - 2 * b, int((w - 2 * b) * RATIO['laptop'])
    return (f'<div style="{pos};width:{w}px">'
            f'<div style="width:{w}px;height:{sh + 2 * b + int(b * .6)}px;border-radius:{int(w * .03)}px {int(w * .03)}px 6px 6px;background:#0E0F12;padding:{b}px {b}px {int(b * 1.6)}px;{shadow}">{screen(d, sw, sh, 6)}</div>'
            f'<div style="width:{int(w * 1.12)}px;margin-left:{-int(w * .06)}px;height:{int(w * .028)}px;border-radius:0 0 {int(w * .04)}px {int(w * .04)}px;'
            f'background:linear-gradient(180deg,#D7DCE3,#AEB5BF);box-shadow:0 18px 30px rgba(11,21,51,.18)"></div></div>')


def html(p):
    sombre = p.get('fond') == 'sombre'
    if p['brand'] == 'jbkt':
        bg = '#0B1533' if sombre else '#F3F7FF'
        ink = '#FFFFFF' if sombre else '#0B1533'
        sub = 'rgba(255,255,255,.78)' if sombre else '#3C4658'
        accent = '#087BFF'
        logo = f'<span style="display:inline-block;background:#fff;border-radius:18px;padding:12px 16px"><img src="{b64(os.path.join(LOGOS, "jbkt-logo-site.png"))}" style="height:66px;display:block"></span>'
        deco = ('<div style="position:absolute;right:70px;top:78px;display:grid;grid-template-columns:repeat(3,18px);gap:8px">'
                + ''.join(f'<span style="width:18px;height:18px;border-radius:4px;background:{c}"></span>' for c in ['#087BFF', '#08C7E8', 'transparent', 'transparent', '#7B2CFF', '#087BFF'])
                + '</div>')
    else:
        bg = '#111418' if sombre else '#EEF0F3'
        ink = '#FFFFFF' if sombre else '#111418'
        sub = 'rgba(255,255,255,.75)' if sombre else '#4A5160'
        accent = '#FFFFFF' if sombre else '#111418'
        logo = (f'<div style="display:flex;align-items:center;gap:14px"><img src="{b64(os.path.join(LOGOS, "radar-icone.png"))}" style="height:60px;border-radius:15px">'
                f'<span style="font:800 38px Manrope;letter-spacing:-0.02em;color:{ink}">Radar VTC</span></div>')
        deco = ''
    cta_bg = accent
    cta_fg = '#111418' if cta_bg == '#FFFFFF' else '#FFFFFF'
    devices = ''.join(device(d) for d in p['devices'])
    haut = p.get('mention_pos') == 'haut'
    mention = (f'<div style="position:absolute;right:76px;{"top:92px" if haut else "bottom:62px"};z-index:7;font:700 22px Manrope;color:{sub};opacity:.85">{p["mention"]}</div>' if p.get('mention') else '')
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>{font(700)}{font(800)}*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1350px;overflow:hidden;font-family:Manrope}}</style></head>
<body><div style="position:relative;width:1080px;height:1350px;overflow:hidden;background:{bg}">
{deco}
<div style="position:absolute;left:76px;top:70px;right:76px;z-index:5">{logo}
  <h1 style="margin-top:44px;font:800 {p.get('size', 76)}px/1.02 Manrope;letter-spacing:-0.035em;color:{ink}">{p['title']}</h1>
  <p style="margin-top:22px;font:700 31px/1.32 Manrope;color:{sub};max-width:900px">{p['subtitle']}</p>
</div>
{devices}
<div style="position:absolute;left:76px;bottom:56px;z-index:6;display:flex;align-items:center;gap:16px;height:86px;padding:0 14px 0 34px;border-radius:999px;background:{cta_bg};color:{cta_fg};font:800 29px Manrope;box-shadow:0 12px 30px rgba(0,0,0,.18)">{p['cta']}
  <span style="width:58px;height:58px;border-radius:50%;background:{cta_fg};display:flex;align-items:center;justify-content:center"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="{cta_bg}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>
{mention}
</div></body></html>'''


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
