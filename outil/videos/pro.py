#!/usr/bin/env python3
"""Reel JBKT « pro » (piste A, validée par Karim le 16/11/2026), 1080x1920, 30 i/s, ~18 s.

Différences avec reel.py : vraie photo du métier en ouverture, très gros texte qui remplit l'écran,
vrais écrans de démo de la banque (banque/jbkt/...) en gros plan avec mouvement de caméra,
pastille « Démo · données fictives » sur chaque écran.

  python3 outil/videos/pro.py fiche.json sortie.mp4 [--musique clair|calme|elan] [--still 1,5,9]

Fiche :
{
 "id": "jbkt-garage-pro",
 "photo": "photos/garage-mecanicien.jpg",          # dans outil/videos/assets/
 "kicker": "Garages · ateliers",
 "hook": "Votre atelier<br>tourne encore<br>au papier ?",
 "desk": {"img": "outils-metier/outils-metier-garage-1-ordinateur.jpg", "title": "L'agenda de l'atelier,<br>pont par pont."},
 "phones": [
   {"img": "outils-metier/...-3-telephone.jpg", "title": "...", "chip": "Devis validé ✓"},
   {"img": "...", "title": "...", "chip": "..."}
 ],
 "end": {"tagline": "Votre métier,<br>votre outil.", "button": "Démo gratuite de 30 min", "small": "jbktsolutionsdigitales.fr"}
}
"""
import sys, json, subprocess, argparse, os
from pathlib import Path

ICI = Path(__file__).parent
A = ICI / 'assets'
BANQUE = (ICI / '..' / '..' / 'banque' / 'jbkt').resolve()
W, H, FPS = 1080, 1920, 30

CSS = """
@font-face { font-family: M; font-weight: 700; src: url('file://A/manrope-latin-700-normal.woff2'); }
@font-face { font-family: M; font-weight: 800; src: url('file://A/manrope-latin-800-normal.woff2'); }
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0B1533}
*{box-sizing:border-box}
body{font-family:M,sans-serif;-webkit-font-smoothing:antialiased}
.sc{position:absolute;inset:0;overflow:hidden;will-change:transform}
.big{font-weight:800;font-size:124px;line-height:1.02;letter-spacing:-.045em}
.ttl{font-weight:800;font-size:84px;line-height:1.04;letter-spacing:-.04em}
.w{display:inline-block;white-space:pre;will-change:transform,opacity}
.kick{display:inline-block;font-weight:700;font-size:30px;letter-spacing:.06em;text-transform:uppercase;padding:14px 26px;border-radius:40px}
.demo{position:absolute;left:84px;top:110px;z-index:6;font-weight:700;font-size:26px;padding:14px 26px;border-radius:40px;white-space:nowrap}
.browser{position:absolute;border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 60px 140px rgba(11,21,51,.35)}
.browser .bar{height:54px;background:#0B1533;display:flex;align-items:center;gap:12px;padding:0 24px}
.browser .bar i{width:16px;height:16px;border-radius:50%;background:#2B3A66;display:block}
.browser img{display:block;width:100%}
.phone{position:absolute;border-radius:118px;background:#0E0F12;padding:20px;box-shadow:0 70px 150px rgba(0,0,0,.45)}
.phone .scr{border-radius:100px;overflow:hidden;background:#fff;position:relative}
.phone .scr img{display:block;width:100%}
.chip{position:absolute;font-weight:800;font-size:40px;padding:26px 38px;border-radius:30px;background:#087BFF;color:#fff;box-shadow:0 30px 70px rgba(8,123,255,.45);white-space:nowrap}
.btn{display:inline-block;border-radius:70px;padding:36px 64px;font-size:44px;font-weight:800;background:#087BFF;color:#fff}
"""

JS = r"""
const ease = t => t<0?0:t>1?1:1-Math.pow(1-t,3);
const easeIO = t => t<0?0:t>1?1:(t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2);
const back = t => {t=Math.max(0,Math.min(1,t));const c1=1.4,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
const P = (t,a,d)=> (t-a)/d;
function render(t){
  // scènes : push horizontal entre elles
  document.querySelectorAll('.sc').forEach(s=>{
    const a=+s.dataset.a, b=+s.dataset.b;
    let x=0, vis=true;
    if(a>0){ const p=easeIO(P(t,a,.7)); x=(1-p)*1080; if(t<a) vis=false; }
    if(b && t>b){ const p=easeIO(P(t,b,.7)); x=-p*320; if(t>b+.7) vis=false; }
    s.style.display=vis?'block':'none';
    s.style.transform=`translateX(${x}px)`;
    s.style.filter = (b && t>b) ? `brightness(${1-.45*easeIO(P(t,b,.7))})` : '';
  });
  document.querySelectorAll('[data-w]').forEach(e=>{
    const p=ease(P(t,+e.dataset.w,.55));
    e.style.opacity=p; e.style.transform=`translateY(${(1-p)*70}px)`;
  });
  document.querySelectorAll('[data-pop]').forEach(e=>{
    const a=+e.dataset.pop, p=back(P(t,a,.6)), o=ease(P(t,a,.25));
    e.style.opacity=o; e.style.transform=(e.dataset.base||'')+` scale(${.6+.4*p})`;
  });
  // photo : zoom lent
  document.querySelectorAll('[data-kb]').forEach(e=>{
    const a=+e.dataset.kb, d=+e.dataset.kd, p=Math.max(0,Math.min(1,(t-a)/d));
    e.style.transform=`scale(${1.04+.12*p}) translateY(${-30*p}px)`;
  });
  // écran ordinateur : entrée + travelling de gauche à droite
  document.querySelectorAll('[data-desk]').forEach(e=>{
    const a=+e.dataset.desk, d=+e.dataset.dd;
    const pin=ease(P(t,a,.8)), pan=easeIO(P(t,a+.5,d-.5));
    const x0=+e.dataset.x0, x1=+e.dataset.x1;
    e.style.opacity=pin;
    e.style.transform=`translate(${x0+(x1-x0)*pan}px, ${(1-pin)*160}px) scale(${1.0+.06*pan})`;
  });
  // téléphones : montent du bas, légère rotation qui se pose, puis défilement doux
  document.querySelectorAll('[data-ph]').forEach(e=>{
    const a=+e.dataset.ph, d=+e.dataset.pd, dir=+e.dataset.dir;
    const pin=ease(P(t,a,.9)), drift=Math.max(0,Math.min(1,(t-a)/d));
    e.style.transform=`translate(${(1-pin)*dir*700}px, ${(1-pin)*500 - 60*drift}px) rotate(${(1-pin)*dir*-8}deg)`;
  });
}
async function renderAt(t){
  render(t);
  const vids=[...document.querySelectorAll('video[data-clip]')];
  await Promise.all(vids.map(v=>new Promise(res=>{
    const target=Math.min(t, (v.duration||5)-0.05);
    if(Math.abs(v.currentTime-target)<0.001){res();return;}
    v.addEventListener('seeked',()=>res(),{once:true}); v.currentTime=target;
    setTimeout(res,1500);
  })));
}
render(0);
"""


def words(text, start, step=0.08):
    out, i = [], 0
    for li, line in enumerate(text.split('<br>')):
        if li: out.append('<br>')
        for w in line.split(' '):
            if w:
                out.append(f'<span class="w" data-w="{start + i*step:.2f}">{w} </span>')
                i += 1
    return ''.join(out), start + i*step


def build(v):
    parts = []
    def scene(a, b, bg, inner):
        parts.append(f'<div class="sc" data-a="{a:.2f}" data-b="{b:.2f}" style="background:{bg}">{inner}</div>')

    demo_light = '<div class="demo" style="background:#0B1533;color:#fff">Démo · données fictives</div>'
    demo_dark = '<div class="demo" style="background:rgba(255,255,255,.14);color:#fff">Démo · données fictives</div>'

    # 1. Accroche sur photo réelle
    t0 = 0.0
    hw, he = words(v['hook'], 0.35)
    s1_end = max(he + 1.6, 4.2) if v.get('clip') else he + 1.6
    if v.get('clip'):
        media = f'<video data-clip="1" muted playsinline preload="auto" src="file://{A}/{v["clip"]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></video>'
    else:
        media = f'<img data-kb="0" data-kd="{s1_end+0.7:.2f}" src="file://{A}/{v["photo"]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
    inner = (media +
             '<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,21,51,.15) 0%,rgba(11,21,51,.35) 40%,rgba(11,21,51,.92) 72%,#0B1533 100%)"></div>'
             f'<div style="position:absolute;left:84px;right:84px;bottom:300px;color:#fff">'
             f'<div class="kick" data-w="0.15" style="background:#087BFF;color:#fff;margin-bottom:40px">{v["kicker"]}</div>'
             f'<div class="big">{hw}</div></div>')
    scene(0, s1_end, '#0B1533', inner)

    # 2. Écran ordinateur en travelling
    a2 = s1_end
    tw, te = words(v['desk']['title'], a2 + 0.45, 0.06)
    d2 = 4.4
    bw = 1900  # largeur affichée : plus grande que l'écran, on se promène dedans
    inner = (f'<div style="position:absolute;inset:0;background:radial-gradient(1200px 900px at 50% 75%,#DCE8FF 0%,#F3F7FF 60%)"></div>'
             f'<div style="position:absolute;left:84px;right:84px;top:230px;color:#0B1533"><div class="ttl">{tw}</div></div>'
             f'<div class="browser" data-desk="{a2+0.25:.2f}" data-dd="{d2:.2f}" data-x0="60" data-x1="{1080-bw-60}" style="left:0;top:640px;width:{bw}px">'
             f'<div class="bar"><i></i><i></i><i></i></div><img src="file://{BANQUE}/{v["desk"]["img"]}"></div>' + demo_light)
    scene(a2, a2 + d2, '#F3F7FF', inner)

    # 3+. Téléphones en gros plan
    a = a2 + d2
    for k, p in enumerate(v['phones']):
        dark = k % 2 == 0
        d = 3.9
        tw, te = words(p['title'], a + 0.45, 0.06)
        col = '#fff' if dark else '#0B1533'
        bg = ('radial-gradient(900px 900px at 50% 85%,#16306E 0%,#0B1533 65%)' if dark
              else 'radial-gradient(1100px 900px at 50% 80%,#DCE8FF 0%,#F3F7FF 60%)')
        pw = 780
        chip = (f'<div class="chip" data-pop="{a+1.5:.2f}" style="{'left:40px' if k % 2 == 0 else 'right:40px'};top:{p.get('chip_top',1640)}px">{p["chip"]}</div>'
                if p.get('chip') else '')
        inner = (f'<div style="position:absolute;inset:0;background:{bg}"></div>'
                 f'<div style="position:absolute;left:84px;right:84px;top:230px;color:{col}"><div class="ttl">{tw}</div></div>'
                 f'<div class="phone" data-ph="{a+0.2:.2f}" data-pd="{d:.2f}" data-dir="{1 if k % 2 == 0 else -1}" style="left:{(1080-pw)//2}px;top:620px;width:{pw}px">'
                 f'<div class="scr"><img src="file://{BANQUE}/{p["img"]}"></div></div>'
                 + chip + (demo_dark if dark else demo_light))
        scene(a, a + d, '#0B1533' if dark else '#F3F7FF', inner)
        a += d

    # Fin
    E = v['end']
    tw, te = words(E['tagline'], a + 0.9, 0.07)
    inner = ('<div style="position:absolute;inset:0;background:radial-gradient(1000px 800px at 50% 40%,#16306E 0%,#0B1533 70%)"></div>'
             f'<div style="position:absolute;left:0;right:0;top:470px;text-align:center"><div data-pop="{a+0.45:.2f}" style="display:inline-block;background:#fff;border-radius:60px;padding:30px 54px">'
             f'<img src="file://{A}/jbkt-logo-site.png" style="height:160px;display:block"></div></div>'
             f'<div style="position:absolute;left:84px;right:84px;top:820px;text-align:center;color:#fff"><div class="big" style="font-size:118px">{tw}</div></div>'
             f'<div style="position:absolute;left:0;right:0;top:1180px;text-align:center"><span class="btn" data-pop="{te+0.2:.2f}">{E["button"]}</span></div>'
             f'<div style="position:absolute;left:0;right:0;top:1360px;text-align:center;color:#9FB3DD;font-weight:700;font-size:34px"><span class="w" data-w="{te+0.5:.2f}">{E["small"]}</span></div>')
    scene(a, 0, '#0B1533', inner)
    total = te + 0.5 + 2.4
    css = CSS.replace('file://A/', f'file://{A}/')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(parts)}<script>{JS}</script></body></html>', round(total, 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fiche'); ap.add_argument('sortie')
    ap.add_argument('--musique', default='clair'); ap.add_argument('--still')
    a = ap.parse_args()
    v = json.load(open(a.fiche, encoding='utf-8'))
    html, total = build(v)
    tmpd = ICI / 'tmp'; tmpd.mkdir(exist_ok=True)
    hp = tmpd / f'{v["id"]}-pro.html'; hp.write_text(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto(f'file://{hp}'); pg.wait_for_timeout(600)
        pg.evaluate("Promise.all([...document.querySelectorAll('video')].map(v=>v.readyState>=1?0:new Promise(r=>{v.onloadedmetadata=r;setTimeout(r,5000)})))")
        if a.still:
            for s in a.still.split(','):
                pg.evaluate(f'renderAt({s})'); pg.wait_for_timeout(50)
                f = tmpd / f'{v["id"]}-{s}.jpg'; pg.screenshot(path=str(f), type='jpeg', quality=85); print(f)
            b.close(); print('durée', total); return
        out = Path(a.sortie); out.parent.mkdir(parents=True, exist_ok=True)
        vid = tmpd / f'{v["id"]}.video.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', str(vid)], stdin=subprocess.PIPE)
        for i in range(int(total * FPS)):
            pg.evaluate(f'renderAt({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close(); rc = ff.wait(); b.close()
    if rc: sys.exit('rendu échoué')
    part = out.with_name(out.stem + '.part.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(vid), '-i', str(ICI / 'music' / f'{a.musique}.m4a'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'afade=t=in:d=0.4,afade=t=out:st={total - 1.6:.2f}:d=1.6',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(part)], check=True)
    part.rename(out); vid.unlink(missing_ok=True)
    print(out, f'{total:.1f}s')


if __name__ == '__main__':
    main()
