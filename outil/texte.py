#!/usr/bin/env python3
"""Posts « texte » JBKT dans la DA des démos (fond clair, Manrope, logo, bandeau nuit en bas).

python3 outil/texte.py <post.json> <sortie.jpg>

post.json : {"kind": "standard|sondage|astuce", "chip": "Question", "kicker": "PME",
             "title": "…", "subtitle": "…", "options": ["…"], "cta": "Répondez en commentaire"}
Alterne avec les posts de démo (outil/demo.py) : une image avec un outil, une image avec du texte.
"""
import asyncio, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from demo import CSS, C, LOGO, render


def html(p):
    kind = p.get('kind', 'standard')
    body = ''
    if kind == 'sondage':
        cards = ''.join(
            f'<div style="flex:1;background:#fff;border-radius:36px;padding:44px 40px;box-shadow:0 20px 50px rgba(11,21,51,.07)">'
            f'<div style="width:84px;height:84px;border-radius:50%;background:{C["acc_l"] if i == 0 else C["dark"]};color:#fff;'
            f'font-weight:800;font-size:44px;display:flex;align-items:center;justify-content:center">{"AB"[i]}</div>'
            f'<div style="font-weight:800;font-size:44px;line-height:1.12;letter-spacing:-0.03em;margin-top:34px">{o}</div></div>'
            for i, o in enumerate(p['options'][:2]))
        body = f'<div style="display:flex;gap:28px">{cards}</div>'
    elif kind == 'astuce':
        rows = ''.join(
            f'<div style="display:flex;align-items:center;gap:26px;background:#fff;border-radius:26px;padding:24px 30px;margin-bottom:16px">'
            f'<div style="flex:none;width:58px;height:58px;border-radius:50%;background:{C["acc_l"]};color:#fff;font-weight:800;font-size:30px;'
            f'display:flex;align-items:center;justify-content:center">{i}</div>'
            f'<div style="font-weight:700;font-size:36px;line-height:1.2;letter-spacing:-0.02em">{o}</div></div>'
            for i, o in enumerate(p['options'], 1))
        body = rows
    elif kind == 'fichiers':
        rot = [-4, 2, -1.5, 3]
        body = ''.join(
            f'<div style="display:flex;align-items:center;gap:24px;background:#fff;border-radius:24px;padding:20px 28px;margin:0 0 12px {40 * i}px;'
            f'transform:rotate({rot[i % 4]}deg);box-shadow:0 18px 40px rgba(11,21,51,.08);width:720px">'
            f'<div style="flex:none;width:62px;height:76px;border-radius:10px;background:#E8F0FF;border:3px solid {C["acc_l"]};position:relative">'
            f'<div style="position:absolute;left:12px;right:12px;top:22px;height:5px;background:{C["acc_l"]};border-radius:3px;box-shadow:0 12px 0 {C["acc_l"]},0 24px 0 {C["acc_l"]}"></div></div>'
            f'<div><div style="font-weight:800;font-size:34px;letter-spacing:-0.02em">{o}</div>'
            f'<div style="font-weight:700;font-size:24px;color:{C["muted_l"]};margin-top:4px">modifié par {["Julie", "Marc", "Sophie", "Paul"][i % 4]} · v{i + 1}</div></div></div>'
            for i, o in enumerate(p['options']))
        body = f'<div style="font-weight:700;font-size:36px;line-height:1.3;color:{C["muted_l"]};margin-bottom:34px">{p.get("subtitle", "")}</div>' + body
    elif kind == 'etapes':
        n = len(p['options'])
        cells = []
        for i, o in enumerate(p['options']):
            last = i == n - 1
            cells.append(f'<div style="flex:1;background:{C["dark"] if last else "#fff"};color:{"#fff" if last else C["ink"]};border-radius:34px;padding:70px 26px;'
                         f'text-align:center;box-shadow:0 18px 40px rgba(11,21,51,.08)"><div style="font-weight:800;font-size:26px;color:{C["acc_d"] if last else C["acc_l"]}">'
                         f'{"Avec un outil" if last else f"Étape {i + 1}"}</div><div style="font-weight:800;font-size:42px;line-height:1.15;margin-top:20px;letter-spacing:-0.02em">{o}</div></div>')
            if i < n - 1:
                cells.append(f'<div style="flex:none;align-self:center;font-weight:800;font-size:44px;color:{C["muted_l"]}">→</div>')
        body = (f'<div style="font-weight:700;font-size:36px;line-height:1.3;color:{C["muted_l"]};margin-bottom:46px">{p.get("subtitle", "")}</div>'
                f'<div style="display:flex;gap:14px">{"".join(cells)}</div>')
    else:
        body = (f'<div style="font-weight:700;font-size:44px;line-height:1.3;color:{C["muted_l"]};letter-spacing:-0.02em">{p.get("subtitle", "")}</div>')
    import re
    p['title'] = re.sub(r'(\d+) ', '\\1\u00a0', p['title'])
    title_size = 92 if len(p['title']) < 40 else (80 if len(p['title']) < 60 else 70)
    return f"""<html><head><style>{CSS} body{{width:1080px;height:1350px;background:{C['light']};color:{C['ink']}}}</style></head><body>
<div style="position:absolute;left:70px;top:64px" class="logo"><img src="data:image/png;base64,{LOGO}"></div>
<div style="position:absolute;right:70px;top:76px;background:#fff;color:{C['muted_l']}" class="chip">{p.get('chip', '')}</div>
<div style="position:absolute;left:70px;right:70px;top:230px">
 <div style="font-weight:800;font-size:32px;color:{C['acc_l']};letter-spacing:-0.01em">{p.get('kicker', '')}</div>
 <div style="font-weight:800;font-size:{title_size}px;line-height:1.02;letter-spacing:-0.045em;margin-top:18px">{p['title']}</div>
 <div style="margin-top:{'56' if kind != 'standard' else '40'}px">{body}</div>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:{C['dark']};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 70px">
 <span style="font-weight:800;font-size:32px">{p.get('cta', 'Démo gratuite de 30 min')}</span><span style="font-weight:700;font-size:26px;color:{C['muted_d']}">Lien en bio</span></div>
</body></html>"""


if __name__ == '__main__':
    p = json.load(open(sys.argv[1]))
    asyncio.run(render([(html(p), sys.argv[2], (1080, 1350))]))
    print(sys.argv[2])
