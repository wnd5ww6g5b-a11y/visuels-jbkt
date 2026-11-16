#!/usr/bin/env python3
"""Pub Gloova « style télé » (9:16, 1080x1920, 30 i/s) : plans vidéo Higgsfield + vrai écran de l'app + fin de marque.

  python3 outil/videos/gloova_pub.py fiche.json sortie.mp4 [--musique calme] [--still 1,6,14]

Fiche :
{
 "id": "gloova-pub-mains-prises",
 "shots": [ {"clip": "clips/gloova-ongles.mp4", "text": "Vos mains sont prises.", "dur": 4.2}, ... ],
 "product": {"screen": "gloova-ecran-accueil.jpg", "title": "Elles réservent en ligne,<br>24 h/24.",
             "card": ["Nouveau rendez-vous", "Massage californien · Samedi 11:00"], "dur": 4.6, "after": 2},
 "end": {"tagline": "L'agenda des pros de la beauté.", "sub": "Sans commission sur vos rendez-vous.", "small": "gloova.fr · iPhone et iPad"}
}
Règles : écrans = vraie app Gloova (version validée) ; personnes = acteurs générés, jamais présentés comme des clientes
réelles, aucun avis ni témoignage ; charte crème / rose poudré / encre, jamais de violet ni d'orange vif ; prix TTC si cités.
"""
import json, subprocess, argparse
from pathlib import Path

ICI = Path(__file__).parent
A = ICI / 'assets'
LOGO = (ICI / '..' / '..' / '..' / 'gloomy-site' / 'public' / 'images' / 'brand' / 'logo-fleur-noire.png').resolve()
W, H, FPS = 1080, 1920, 30
XF = 0.5  # fondu entre plans (modifiable par la fiche : "xf")
STEP = 0.09
WD = 0.7

CSS = """
@font-face{font-family:J;font-weight:500;src:url('file://A/plus-jakarta-sans-latin-500-normal.woff2')}
@font-face{font-family:J;font-weight:600;src:url('file://A/plus-jakarta-sans-latin-600-normal.woff2')}
@font-face{font-family:J;font-weight:700;src:url('file://A/plus-jakarta-sans-latin-700-normal.woff2')}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#1E1F21}
*{box-sizing:border-box}
body{font-family:J,sans-serif;-webkit-font-smoothing:antialiased}
.sc{position:absolute;inset:0;overflow:hidden;opacity:0}
.sc video{position:absolute;inset:-30px;width:calc(100% + 60px);height:calc(100% + 60px);object-fit:cover;filter:saturate(.86) contrast(1.05) sepia(.07) brightness(1.02)}
.grain{position:absolute;inset:0;background:url('file://A/grain.png');mix-blend-mode:overlay;opacity:.55;pointer-events:none;z-index:50}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.28) 100%);pointer-events:none}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,31,33,0) 45%,rgba(30,31,33,.55) 78%,rgba(30,31,33,.75) 100%)}
.cap{position:absolute;left:80px;right:80px;bottom:250px;color:#fff;font-weight:600;font-size:86px;line-height:1.06;letter-spacing:-.035em;text-shadow:0 4px 30px rgba(0,0,0,.25)}
.w{display:inline-block;white-space:pre;opacity:0}
.ttl{font-weight:700;font-size:80px;line-height:1.05;letter-spacing:-.035em;color:#1E1F21}
.phone{position:absolute;left:170px;width:740px;border-radius:112px;background:#111214;padding:18px;box-shadow:0 80px 160px rgba(30,31,33,.30)}
.phone .scr{border-radius:96px;overflow:hidden;background:#fff;height:1400px}
.phone .scr img{display:block;width:100%}
.card{position:absolute;left:110px;right:110px;background:#fff;border-radius:40px;padding:34px 40px;display:flex;gap:28px;align-items:center;box-shadow:0 40px 90px rgba(30,31,33,.22);opacity:0}
.card i{width:84px;height:84px;border-radius:26px;background:#EFE3DF;display:flex;align-items:center;justify-content:center;flex:none}
.card b{display:block;font-size:36px;color:#1E1F21}
.card span{display:block;font-size:30px;color:rgba(30,31,33,.6);font-weight:500;margin-top:4px}
"""

JS = r"""
const cl=x=>Math.max(0,Math.min(1,x));
const WD=__WD__;
const ease=t=>1-Math.pow(1-cl(t),3);
const back=t=>{t=cl(t);const c1=1.3,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)};
function render(t){
  const g=document.querySelector('.grain'); if(g){ const f=Math.floor(t*24); g.style.backgroundPosition=`${(f*137)%512}px ${(f*241)%512}px`; }
  document.querySelectorAll('.sc').forEach(s=>{
    const a=+s.dataset.a,b=+s.dataset.b,xf=+s.dataset.xf;
    let o = a<=0 ? 1 : cl((t-a)/xf);
    if(b>0 && t>b) o=Math.min(o, 1-cl((t-b)/xf));
    s.style.opacity=o; s.style.visibility = o>0?'visible':'hidden';
    const z=s.querySelector('video');
    if(z){ const p=cl((t-a)/(b+xf-a)); const sx=Math.sin(t*1.7)*6+Math.sin(t*4.3)*2, sy=Math.cos(t*1.3)*5+Math.sin(t*3.7)*2;
      const punch = xf<0.3 ? .08*(1-ease((t-a)/.35)) : 0;
      z.style.transform=`translate(${sx}px,${sy}px) scale(${1.02+.05*p+punch}) rotate(${Math.sin(t*.9)*.25}deg)`; }
  });
  document.querySelectorAll('[data-w]').forEach(e=>{
    const p=ease((t-+e.dataset.w)/WD);
    e.style.opacity=p; e.style.transform=`translateY(${(1-p)*40}px)`; e.style.filter=`blur(${(1-p)*8}px)`;
  });
  document.querySelectorAll('[data-ph]').forEach(e=>{
    const a=+e.dataset.ph, p=ease((t-a)/(+e.dataset.pd||1.1)), d=cl((t-a)/4);
    e.style.transform=`translateY(${(1-p)*900 - 50*d}px) rotate(${(1-p)*-6}deg)`;
  });
  document.querySelectorAll('[data-card]').forEach(e=>{
    const a=+e.dataset.card, p=back((t-a)/.6);
    e.style.opacity=cl((t-a)/.25); e.style.transform=`translateY(${(1-p)*60}px) scale(${.85+.15*p})`;
  });
}
async function renderAt(t){
  render(t);
  const vs=[...document.querySelectorAll('video')];
  await Promise.all(vs.map(v=>new Promise(res=>{
    const s=v.closest('.sc'); const a=+s.dataset.a;
    const target=Math.max(0,Math.min((v.duration||5)-0.05, t-a+ +v.dataset.off));
    if(Math.abs(v.currentTime-target)<0.001){res();return;}
    v.addEventListener('seeked',()=>res(),{once:true}); v.currentTime=target; setTimeout(res,1500);
  })));
}
render(0);
"""


def words(text, start, step=None):
    step = STEP if step is None else step
    out, i = [], 0
    for li, line in enumerate(text.split('<br>')):
        if li: out.append('<br>')
        for w in line.split(' '):
            if w:
                out.append(f'<span class="w" data-w="{start + i*step:.2f}">{w} </span>'); i += 1
    return ''.join(out), start + i*step


def build(v):
    global XF, STEP, WD
    XF = v.get('xf', 0.5); STEP = v.get('step', 0.09); WD = v.get('wd', 0.7)
    parts, t = [], 0.0
    def scene(a, b, inner, bg='#1E1F21'):
        parts.append(f'<div class="sc" data-a="{a:.2f}" data-b="{b:.2f}" data-xf="{XF}" style="background:{bg}">{inner}</div>')
    shots = v['shots']
    pos = v['product'].get('after', len(shots))
    seq = shots[:pos] + [{'product': True}] + shots[pos:]
    for s in seq:
        if s.get('product'):
            P = v['product']; d = P.get('dur', 4.6)
            tw, te = words(P['title'], t + P.get('title_delay', 0.4), 0.07)
            inner = ('<div style="position:absolute;inset:0;background:radial-gradient(1100px 1000px at 50% 70%,#EFE3DF 0%,#F4F2ED 62%)"></div>'
                     f'<div style="position:absolute;left:80px;right:80px;top:200px"><div class="ttl">{tw}</div></div>'
                     f'<div class="phone" data-ph="{t+P.get('phone_delay', 0.3):.2f}" data-pd="{P.get('phone_in', 1.1)}" style="top:640px"><div class="scr"><img src="file://{A}/{P["screen"]}"></div></div>'
                     f'<div class="card" data-card="{t+P.get('card_delay', 1.9):.2f}" style="top:1380px"><i><img src="file://{LOGO}" style="width:52px;height:52px"></i>'
                     f'<div><b>{P["card"][0]}</b><span>{P["card"][1]}</span></div></div>')
            scene(t, t + d, inner, '#F4F2ED'); t += d
        else:
            d = s.get('dur', 4.2)
            tw, _ = words(s.get('text', ''), t + v.get('cap_delay', 0.6))
            inner = (f'<video muted playsinline preload="auto" data-off="{s.get("off", 0.2)}" src="file://{A}/{s["clip"]}"></video>'
                     f'<div class="vig"></div><div class="shade"></div><div class="cap">{tw}</div>')
            scene(t, t + d, inner); t += d
    E = v['end']
    tw, te = words(E['tagline'], t + E.get('delay', 1.0), 0.08)
    inner = ('<div style="position:absolute;inset:0;background:linear-gradient(170deg,#F4F2ED 0%,#F3EEEA 55%,#EFE3DF 100%)"></div>'
             f'<div style="position:absolute;left:0;right:0;top:560px;text-align:center"><span class="w" data-w="{t+0.4:.2f}" style="display:inline-flex;align-items:center;gap:26px">'
             f'<img src="file://{LOGO}" style="width:130px;height:130px"><span style="font-weight:700;font-size:150px;letter-spacing:-.04em;color:#1E1F21">Gloova</span></span></div>'
             f'<div style="position:absolute;left:90px;right:90px;top:820px;text-align:center"><div class="ttl" style="font-size:70px">{tw}</div></div>'
             f'<div style="position:absolute;left:0;right:0;top:1060px;text-align:center"><span class="w" data-w="{te+0.3:.2f}" style="display:inline-block;background:#1E1F21;color:#fff;font-weight:600;font-size:40px;padding:30px 52px;border-radius:60px">{E["sub"]}</span></div>'
             f'<div style="position:absolute;left:0;right:0;top:1230px;text-align:center;color:rgba(30,31,33,.6);font-weight:600;font-size:34px"><span class="w" data-w="{te+0.7:.2f}">{E["small"]}</span></div>')
    scene(t, 0, inner, '#F4F2ED')
    total = te + 0.7 + E.get('hold', 2.6)
    css = CSS.replace('file://A/', f'file://{A}/')
    if v.get('cap_size'): css = css.replace('font-size:86px', f"font-size:{v['cap_size']}px")
    js = JS.replace('__WD__', str(WD))
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(parts)}<div class="grain"></div><script>{js}</script></body></html>', round(total, 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fiche'); ap.add_argument('sortie')
    ap.add_argument('--musique', default='calme'); ap.add_argument('--still')
    a = ap.parse_args()
    v = json.load(open(a.fiche, encoding='utf-8'))
    html, total = build(v)
    tmpd = ICI / 'tmp'; tmpd.mkdir(exist_ok=True)
    hp = tmpd / f'{v["id"]}.html'; hp.write_text(html)
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
        vid = tmpd / f'{v["id"]}.video.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', str(vid)], stdin=subprocess.PIPE)
        for i in range(int(total * FPS)):
            pg.evaluate(f'renderAt({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
        ff.stdin.close(); rc = ff.wait(); b.close()
    if rc: raise SystemExit('rendu échoué')
    out = Path(a.sortie); out.parent.mkdir(parents=True, exist_ok=True)
    part = out.with_name(out.stem + '.part.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(vid), '-i', str(ICI / 'music' / f'{a.musique}.m4a'),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', f'afade=t=in:d=0.6,afade=t=out:st={total - 2:.2f}:d=2',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(part)], check=True)
    part.rename(out); vid.unlink(missing_ok=True)
    print(out, f'{total:.1f}s')


if __name__ == '__main__':
    main()
