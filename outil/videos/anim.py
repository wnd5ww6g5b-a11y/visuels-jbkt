#!/usr/bin/env python3
"""Vidéos animées (style des pubs Gloova) pour JBKT et Radar VTC.

Chaque vidéo est une page HTML avec une fonction JS render(t) déterministe :
on la rend image par image dans Chrome (Playwright) et on envoie les JPEG
directement à ffmpeg (1080x1920, 30 i/s).

  python3 anim.py [--still 3.2] [id ...]
"""
import sys, subprocess, html, json, os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

ROOT = Path(__file__).parent
A = ROOT / 'assets'
OUT = ROOT / 'out2'
W, H, FPS = 1080, 1920, 30

BRANDS = {
 'jbkt': dict(dark='#0B1533', light='#F3F7FF', alt='#E8F0FF', ink='#0B1533', paper='#FFFFFF', muted_d='#9FB3DD', muted_l='#64748B',
              acc_d='#4FA3FF', acc_l='#087BFF', title_font="Manrope, Inter, sans-serif", check='#087BFF', chip_d='#16224A', chip_l='#FFFFFF'),
 'radar': dict(dark='#1E2124', light='#F2F3F5', alt='#FFFFFF', ink='#1E2124', paper='#FFFFFF', muted_d='#A3A8AD', muted_l='#6B7075',
               acc_d='#4CD27A', acc_l='#2FB45F', title_font="Inter, sans-serif", check='#2FB45F', chip_d='#2A2E32', chip_l='#FFFFFF'),
}

CSS = """
@font-face { font-family: Manrope; font-weight: 700; src: url('A/manrope-latin-700-normal.woff2'); }
@font-face { font-family: Manrope; font-weight: 800; src: url('A/manrope-latin-800-normal.woff2'); }
html,body { margin:0; width:1080px; height:1920px; overflow:hidden; background:#000; }
* { box-sizing:border-box; }
body { font-family: Inter, system-ui, sans-serif; -webkit-font-smoothing:antialiased; }
.sc { position:absolute; inset:0; overflow:hidden; }
.box { position:absolute; left:0; right:0; text-align:center; padding:0 90px; }
.w { display:inline-block; white-space:pre; will-change:transform,opacity,filter; }
.hook { font-family:TF; font-weight:800; font-size:100px; line-height:1.08; letter-spacing:-.03em; }
.title { font-family:TF; font-weight:800; font-size:72px; line-height:1.1; letter-spacing:-.025em; }
.kick { font-size:28px; font-weight:600; letter-spacing:.02em; margin-bottom:18px; }
.acc { font-family:TF; font-weight:800; font-size:92px; line-height:1.1; letter-spacing:-.03em; }
.card { position:absolute; left:50%; width:640px; margin-left:-320px; border-radius:30px; padding:30px 36px; text-align:left; font-size:36px; line-height:1.35; font-weight:600; box-shadow:0 24px 60px rgba(0,0,0,.25); }
.card small { display:block; font-size:22px; font-weight:600; opacity:.6; margin-bottom:8px; letter-spacing:.04em; text-transform:uppercase; }
.phone { position:absolute; left:50%; width:560px; margin-left:-280px; height:1180px; border-radius:96px; background:#0F1012; padding:16px; box-shadow:0 50px 100px rgba(0,0,0,.30); }
.phone .scr { width:100%; height:100%; border-radius:82px; overflow:hidden; background:#F6F7F9; position:relative; }
.phone .scr img { width:100%; height:100%; object-fit:cover; object-position:top; display:block; }
.island { position:absolute; top:26px; left:50%; width:150px; margin-left:-75px; height:44px; border-radius:30px; background:#0F1012; z-index:3; }
.ui { position:absolute; inset:0; padding:96px 30px 30px; color:#0B1533; font-family:Inter, sans-serif; }
.ui .sb { position:absolute; top:34px; left:48px; font-size:22px; font-weight:700; }
.ui .t { font-family:TF; font-weight:800; font-size:42px; margin:8px 6px 2px; }
.ui .st { font-size:21px; color:#64748B; margin:0 6px 22px; }
.row { background:#fff; border-radius:24px; padding:26px 22px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center; font-size:26px; font-weight:600; box-shadow:0 3px 10px rgba(0,0,0,.05); }
.row small { display:block; font-size:18px; color:#64748B; font-weight:500; margin-top:3px; }
.chip { font-size:18px; font-weight:700; padding:8px 14px; border-radius:24px; white-space:nowrap; }
.c-b { background:#EAF3FF; color:#0A5FC4; } .c-g { background:#E6F7EE; color:#127A45; } .c-o { background:#FFF1E0; color:#9A4F00; } .c-v { background:#F1EAFF; color:#5B1FC2; }
.field { background:#fff; border:2px solid #E2E8F0; border-radius:20px; padding:22px 22px; margin-bottom:16px; font-size:26px; }
.field b { display:block; font-size:17px; color:#64748B; font-weight:600; margin-bottom:4px; text-transform:uppercase; letter-spacing:.05em; }
.btnp { border-radius:20px; padding:22px; text-align:center; font-size:25px; font-weight:700; margin-top:18px; color:#fff; }
.li { position:absolute; left:50%; width:620px; margin-left:-310px; height:84px; border-radius:22px; display:flex; align-items:center; gap:22px; padding:0 28px; font-size:31px; font-weight:600; }
.li i { width:40px; height:40px; border-radius:50%; flex:none; display:flex; align-items:center; justify-content:center; color:#fff; font-style:normal; font-size:22px; font-weight:800; }
.btn { display:inline-block; border-radius:60px; padding:28px 48px; font-size:38px; font-weight:700; }
.small { font-size:26px; }
.wipe { position:absolute; left:0; right:0; top:0; bottom:0; }
"""

# ---------- JS : moteur d'animation déterministe ----------
JS = r"""
const clamp=x=>Math.max(0,Math.min(1,x));
const eo=x=>1-Math.pow(1-x,3);               // ease-out cubic
const eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const back=x=>{const c1=1.5,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2);};
function P(t,a,d){return clamp((t-a)/d);}
window.render=function(t){
  document.querySelectorAll('[data-a]').forEach(el=>{
    const a=+el.dataset.a, d=+(el.dataset.d||.55), k=el.dataset.k||'rise';
    const o=el.dataset.o!==undefined?+el.dataset.o:1e9, od=+(el.dataset.od||.45), ok=el.dataset.ok||'fade';
    let p=P(t,a,d), q=P(t,o,od), op=1, tx=0, ty=0, s=1, r=0, bl=0, cl=null;
    if(k==='rise'){const e=eo(p); op=e; ty=(1-e)*34; bl=(1-e)*10;}
    else if(k==='fade'){op=eo(p);}
    else if(k==='pop'){const e=back(p); op=eo(p); s=.82+.18*e; r=(1-eo(p))*-5; ty=(1-eo(p))*30;}
    else if(k==='phone'){const e=eo(p); ty=(1-e)*1300; r=(1-e)*-14; s=.86+.14*e; tx=(1-e)*-120;}
    else if(k==='phone2'){const e=eo(p); ty=(1-e)*1300; r=(1-e)*10; s=.86+.14*e; tx=(1-e)*160;}
    else if(k==='wipe'){const e=eio(p); const y=(1-e)*100; const rad=(1-e)*120; cl=`inset(${y}% 0 0 0 round ${rad}px ${rad}px 0 0)`;}
    else if(k==='wipeL'){const e=eio(p); const x=(1-e)*100; const rad=(1-e)*120; cl=`inset(0 0 0 ${x}% round ${rad}px 0 0 ${rad}px)`;}
    else if(k==='li'){const e=eo(p); op=e; tx=(1-e)*-60;}
    if(q>0){
      if(ok==='fade'){op*=1-eio(q);}
      else if(ok==='blur'){op*=1-.65*eio(q); bl+=eio(q)*14;}
      else if(ok==='up'){const e=eio(q); op*=1-e; ty-=e*80; bl+=e*8;}
      else if(ok==='phoneout'){const e=eio(q); s*=1-.55*e; tx+=e*330; ty+=e*620; r+=e*12; op*=1-clamp((q-.6)/.4);}
    }
    el.style.opacity=op;
    el.style.transform=`translate(${tx}px,${ty}px) scale(${s}) rotate(${r}deg)`;
    el.style.filter=bl>0.05?`blur(${bl}px)`:'none';
    if(cl!==null) el.style.clipPath=cl;
  });
};
"""


def words(text, start, step=0.07, cls='', d=0.55):
    """Texte qui apparaît mot par mot. <br> = retour à la ligne."""
    out, i = [], 0
    for li, line in enumerate(text.split('<br>')):
        if li: out.append('<br>')
        for w in line.split(' '):
            if not w: continue
            out.append(f'<span class="w {cls}" data-a="{start + i*step:.3f}" data-d="{d}">{w} </span>')
            i += 1
    return ''.join(out), start + i*step


def ui_rows(title, sub, items, b):
    r = ''.join(f'<div class="row"><span>{a}<small>{s}</small></span><span class="chip {c}">{t}</span></div>' for a, s, t, c in items)
    return f'<div class="ui"><div class="sb">9:41</div><p class="t">{title}</p><p class="st">{sub}</p>{r}</div>'


def ui_fields(title, sub, items, btn, color):
    f = ''.join(f'<div class="field"><b>{a}</b>{v}</div>' for a, v in items)
    return f'<div class="ui"><div class="sb">9:41</div><p class="t">{title}</p><p class="st">{sub}</p>{f}<div class="btnp" style="background:{color}">{btn}</div></div>'


def ui_img(name):
    return f'<img src="A/{name}">'


def build_html(v):
    B = BRANDS[v['brand']]
    css = CSS.replace('TF', B['title_font'].split(',')[0] if v['brand'] == 'jbkt' else 'Inter').replace("url('A/", f"url('file://{A}/")
    parts, t = [], 0.0

    def scene(bg, inner, start, kind='wipe'):
        k = '' if start == 0 else f' data-a="{start:.3f}" data-d="0.75" data-k="{kind}"'
        parts.append(f'<div class="sc"{k} style="background:{bg}">{inner}</div>')

    # 1. Accroche (fond sombre)
    h = v['hook']
    inner, t1 = '', 0.25
    if h.get('kicker'):
        inner += f'<div class="box" style="top:600px;color:{B["muted_d"]}"><div class="kick w" data-a="0.15">{h["kicker"]}</div></div>'
    w1, t1 = words(h['lines'], 0.3, cls='hook')
    top = h.get('top', 640)
    inner += f'<div class="box" style="top:{top}px;color:#fff"><div class="hook">{w1}</div></div>'
    tt = t1 + 0.5
    if h.get('card'):
        inner += f'<div class="card" data-a="{tt:.2f}" data-d="0.6" data-k="pop" data-o="{tt+1.6:.2f}" data-ok="blur" style="top:{top+300}px;background:{B["alt"] if v["brand"]=="jbkt" else "#F2F3F5"};color:{B["ink"]}"><small>{h["card"][0]}</small>{h["card"][1]}</div>'
        tt += 1.7
    if h.get('acc'):
        w2, tt2 = words(h['acc'], tt, cls='acc')
        inner += f'<div class="box" style="top:{top + (520 if h.get("card") else 300)}px;color:{B["acc_d"]}"><div class="acc">{w2}</div></div>'
        tt = tt2 + 0.3
    if h.get('note'):
        inner += f'<div class="box" style="top:{top + 560}px"><span class="chip w" data-a="{tt:.2f}" data-k="pop" style="font-size:26px;padding:12px 22px;background:{B["chip_d"]};color:#fff">{h["note"]}</span></div>'
        tt += 0.5
    scene(B['dark'], inner, 0)
    t = tt + 1.1

    # 2-3. Téléphones (fond clair), le 1er entre en balayage, le 2e remplace le 1er
    ph = v['phones']
    inner = ''
    s0 = t
    for i, p in enumerate(ph):
        a = s0 + 0.35 + i * 2.9
        o = a + 2.55 if i < len(ph) - 1 else None
        od = f' data-o="{o:.2f}" data-ok="up"' if o else ''
        kw, _ = words(p['kicker'], a, step=0.02, cls='kick', d=.4) if p.get('kicker') else ('', 0)
        tw, _ = words(p['title'], a + 0.08, step=0.05, cls='title')
        inner += f'<div class="box" style="top:250px;color:{B["ink"]}"><div style="color:{B["muted_l"]}" {od.replace("data-o","data-o") if False else ""}>{kw}</div></div>' if False else ''
        inner += f'<div class="box" data-a="{a:.2f}" data-d="0.01" data-k="fade"{od} style="top:240px;color:{B["ink"]}"><div style="color:{B["muted_l"]}">{kw}</div><div class="title">{tw}</div></div>'
        oo = f' data-o="{o - 0.05:.2f}" data-od="0.6" data-ok="phoneout"' if o else ''
        inner += f'<div class="phone" data-a="{a + 0.1:.2f}" data-d="0.85" data-k="{"phone" if i % 2 == 0 else "phone2"}"{oo} style="top:560px"><div class="island"></div><div class="scr">{p["screen"]}</div></div>'
    bg2 = B['light']
    band = f'<div style="position:absolute;left:0;right:0;top:1180px;bottom:0;background:{B["alt"] if v["brand"]=="jbkt" else "#E6E8EB"}"></div>'
    scene(bg2, band + inner, s0)
    t = s0 + 0.35 + len(ph) * 2.9 + 0.2

    # 4. Liste d'avantages (fond sombre)
    L = v['list']
    s4 = t
    tw, te = words(L['title'], s4 + 0.45, step=0.06, cls='title')
    inner = f'<div class="box" style="top:600px;color:#fff"><div class="title">{tw}</div></div>'
    for i, it in enumerate(L['items']):
        a = te + 0.25 + i * 0.32
        inner += f'<div class="li" data-a="{a:.2f}" data-k="li" style="top:{820 + i*106}px;background:{B["chip_d"]};color:#fff"><i style="background:{B["check"]}">✓</i>{it}</div>'
    scene(B['dark'], inner, s4, 'wipeL')
    t = te + 0.25 + len(L['items']) * 0.32 + 1.3

    # 5. Fin : logo, phrase, bouton
    E = v['end']
    s5 = t
    if v['brand'] == 'jbkt':
        logo = f'<div class="w" data-a="{s5+0.45:.2f}" data-k="pop" style="background:#fff;border-radius:60px;padding:26px 46px;box-shadow:0 20px 50px rgba(11,21,51,.18)"><img src="A/jbkt-logo-site.png" style="height:150px;display:block"></div>'
        btn_bg, btn_c, bg5, tag_c, sm_c = B['ink'], '#fff', B['light'], B['ink'], B['muted_l']
        sq = ''
    else:
        logo = f'<div class="w" data-a="{s5+0.45:.2f}" data-k="pop" style="text-align:center"><img src="A/radar-icone.png" style="width:190px;height:190px;border-radius:46px;display:block;margin:0 auto;box-shadow:0 20px 50px rgba(0,0,0,.35)"><div style="font-weight:800;font-size:84px;letter-spacing:-.03em;color:#fff;margin-top:34px">Radar VTC</div></div>'
        btn_bg, btn_c, bg5, tag_c, sm_c = '#3A3E42', '#fff', B['dark'], B['muted_d'], B['muted_d']
        sq = ''
    tw, te = words(E['tagline'], s5 + 0.9, step=0.05, cls='title')
    inner = sq + f'<div class="box" style="top:{600 if v["brand"]=="jbkt" else 520}px">{logo}</div>'
    inner += f'<div class="box" style="top:{860 if v["brand"]=="jbkt" else 960}px;color:{tag_c}"><div class="title" style="font-size:62px">{tw}</div></div>'
    inner += f'<div class="box" style="top:{1120 if v["brand"]=="jbkt" else 1200}px"><span class="btn w" data-a="{te+0.25:.2f}" data-k="pop" style="background:{btn_bg};color:{btn_c}">{E["button"]}</span></div>'
    inner += f'<div class="box" style="top:{1270 if v["brand"]=="jbkt" else 1350}px;color:{sm_c}"><span class="small w" data-a="{te+0.6:.2f}" data-k="fade">{E["small"]}</span></div>'
    scene(bg5, inner, s5)
    total = te + 0.6 + 2.2

    body = ''.join(parts)
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}<script>{JS}</script></body></html>'
    page = page.replace('src="A/', f'src="file://{A}/')
    return page, round(total, 2)


def render(v, still=None):
    from playwright.sync_api import sync_playwright
    OUT.mkdir(exist_ok=True)
    page_html, total = build_html(v)
    hp = ROOT / 'tmp' / f'{v["id"]}-anim.html'
    hp.parent.mkdir(exist_ok=True)
    hp.write_text(page_html)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto(f'file://{hp}')
        pg.wait_for_timeout(400)
        if still is not None:
            outs = []
            for s in still:
                pg.evaluate(f'render({s})')
                f = ROOT / 'tmp' / f'{v["id"]}-{s}.jpg'
                pg.screenshot(path=str(f), type='jpeg', quality=85)
                outs.append(f)
            b.close()
            return outs, total
        tmp = OUT / f'{v["id"]}.part.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                               '-movflags', '+faststart', str(tmp)], stdin=subprocess.PIPE)
        n = int(total * FPS)
        for i in range(n):
            pg.evaluate(f'render({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close()
        rc = ff.wait()
        b.close()
    if rc == 0:
        tmp.rename(OUT / f'{v["id"]}.mp4')
    return v['id'], total, rc


if __name__ == '__main__':
    from videos2 import VIDEOS
    args = sys.argv[1:]
    still = None
    if '--still' in args:
        i = args.index('--still'); still = [float(x) for x in args[i + 1].split(',')]; del args[i:i + 2]
    vs = [v for v in VIDEOS if not args or v['id'] in args]
    if still is not None:
        for v in vs:
            outs, total = render(v, still)
            print(v['id'], total, [str(o) for o in outs])
    else:
        with ProcessPoolExecutor(int(os.environ.get('JOBS', '4'))) as ex:
            for r in ex.map(render, vs):
                print(*r, flush=True)
