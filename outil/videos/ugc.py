#!/usr/bin/env python3
"""Vidéo « présentatrice IA » façon UGC (9:16, 1080x1920, 30 i/s).

Une présentatrice générée (Higgsfield) parle face caméra, lèvres synchronisées sur une voix choisie ;
au milieu, les vrais écrans de l'app avec une voix off ; sous-titres gros façon TikTok.
Règle : la présentatrice PRÉSENTE la marque, elle ne dit jamais être cliente ; mention « Image générée par IA » visible
pendant toutes ses apparitions (loi française sur l'influence commerciale, 2023).

  python3 outil/videos/ugc.py fiche.json sortie.mp4 [--still 2,8,16]
"""
import json, subprocess, argparse
from pathlib import Path

ICI = Path(__file__).parent
A = ICI / 'assets'
LOGO = (ICI / '..' / '..' / '..' / 'gloomy-site' / 'public' / 'images' / 'brand' / 'logo-fleur-noire.png').resolve()
W, H, FPS = 1080, 1920, 30

CSS = """
@font-face{font-family:J;font-weight:600;src:url('file://A/plus-jakarta-sans-latin-600-normal.woff2')}
@font-face{font-family:J;font-weight:700;src:url('file://A/plus-jakarta-sans-latin-700-normal.woff2')}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#1E1F21}
*{box-sizing:border-box} body{font-family:J,sans-serif;-webkit-font-smoothing:antialiased}
.sc{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.sc video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ia{position:absolute;top:70px;left:60px;background:rgba(30,31,33,.55);color:#fff;font-weight:600;font-size:28px;padding:12px 22px;border-radius:30px;z-index:9}
.sub{position:absolute;left:70px;right:70px;bottom:330px;text-align:center;z-index:8}
.sub span{display:inline-block;background:#fff;color:#1E1F21;font-weight:700;font-size:62px;line-height:1.15;padding:10px 26px 16px;border-radius:18px;box-shadow:0 10px 30px rgba(0,0,0,.25);opacity:0}
.phone{position:absolute;left:170px;top:420px;width:740px;border-radius:112px;background:#111214;padding:18px;box-shadow:0 80px 160px rgba(30,31,33,.30)}
.phone .scr{border-radius:96px;overflow:hidden;background:#fff;height:1400px;position:relative}
.phone .scr img{position:absolute;inset:0;width:100%;opacity:0}
.card{position:absolute;left:110px;right:110px;background:#fff;border-radius:40px;padding:30px 38px;display:flex;gap:26px;align-items:center;box-shadow:0 40px 90px rgba(30,31,33,.22);opacity:0;z-index:7}
.card i{width:80px;height:80px;border-radius:24px;background:#EFE3DF;display:flex;align-items:center;justify-content:center;flex:none;font-style:normal;font-size:40px}
.card b{display:block;font-size:36px;color:#1E1F21}
.card small{display:block;font-size:28px;color:rgba(30,31,33,.6);font-weight:600;margin-top:4px}
"""

JS = r"""
const cl=x=>Math.max(0,Math.min(1,x)), ease=t=>1-Math.pow(1-cl(t),3);
function vis(e,a,b){return t=>t>=a&&t<b}
function render(t){
  document.querySelectorAll('.sc').forEach(s=>{ s.style.visibility=(t>=+s.dataset.a&&t<+s.dataset.b)?'visible':'hidden'; });
  document.querySelectorAll('.sub span').forEach(e=>{ const a=+e.dataset.a,b=+e.dataset.b;
    const on=t>=a&&t<b; e.style.opacity=on?1:0; e.style.transform=`scale(${on?0.92+0.08*ease((t-a)/.15):1})`; });
  document.querySelectorAll('[data-img]').forEach(e=>{ const a=+e.dataset.img; e.style.opacity=ease((t-a)/.4); });
  document.querySelectorAll('[data-ph]').forEach(e=>{ const a=+e.dataset.ph,p=ease((t-a)/.8); e.style.transform=`translateY(${(1-p)*900-40*cl((t-a)/8)}px)`; });
  document.querySelectorAll('[data-card]').forEach(e=>{ const a=+e.dataset.card,b=+e.dataset.cb||1e9,p=ease((t-a)/.45);
    e.style.opacity=t<b?cl((t-a)/.2):1-cl((t-b)/.25); e.style.transform=`translateY(${(1-p)*50}px)`; });
  document.querySelectorAll('[data-w]').forEach(e=>{ const p=ease((t-+e.dataset.w)/.5); e.style.opacity=p; e.style.transform=`translateY(${(1-p)*30}px)`; });
}
async function renderAt(t){
  render(t);
  const vs=[...document.querySelectorAll('video')].filter(v=>v.closest('.sc').style.visibility==='visible');
  await Promise.all(vs.map(v=>new Promise(res=>{
    const s=v.closest('.sc'); const target=Math.max(0,Math.min((v.duration||14)-0.05,(t-+s.dataset.a)+ +v.dataset.off));
    if(Math.abs(v.currentTime-target)<0.001){res();return;}
    v.addEventListener('seeked',()=>res(),{once:true}); v.currentTime=target; setTimeout(res,1500);
  })));
}
render(0);
"""


def subs(lines, start, dur):
    """Découpe le texte en morceaux répartis au prorata du nombre de lettres."""
    total = sum(len(x) for x in lines)
    out, t = [], start
    for x in lines:
        d = dur * len(x) / total
        out.append(f'<span data-a="{t:.2f}" data-b="{t + d:.2f}" style="position:absolute;left:0;right:0;margin:auto;width:fit-content">{x}</span>')
        t += d
    return ''.join(out)


def build(v):
    P = v['presenter']; S = v['screens']; E = v['end']
    clip = A / P['clip']
    t1 = P['seg1'][1] - P['seg1'][0] + 0.15
    sA = 0.0; sB = sA + t1; sC = sB + S['dur']; t3 = P['seg2'][1] - P['seg2'][0] + 0.25; sD = sC + t3; total = sD + E['dur']
    ia = '<div class="ia">Image générée par IA</div>'
    html = []
    # 1. présentatrice
    html.append(f'<div class="sc" data-a="{sA}" data-b="{sB:.2f}"><video muted preload="auto" data-off="{P["seg1"][0]}" src="file://{clip}"></video>{ia}'
                f'<div class="sub">{subs(P["subs1"], sA + 0.05, t1 - 0.15)}</div></div>')
    # 2. écrans
    imgs = ''.join(f'<img data-img="{sB + k * S["dur"] / len(S["imgs"]):.2f}" src="file://{A}/{im}">' for k, im in enumerate(S['imgs']))
    cards = ''
    for c in S['cards']:
        cards += (f'<div class="card" data-card="{sB + c["at"]:.2f}" data-cb="{sB + c.get("until", 99):.2f}" style="top:{c.get("top", 1250)}px">'
                  f'<i>{c.get("icon", "✓")}</i><div><b>{c["title"]}</b><small>{c["sub"]}</small></div></div>')
    html.append(f'<div class="sc" data-a="{sB:.2f}" data-b="{sC:.2f}" style="background:radial-gradient(1100px 1000px at 50% 70%,#EFE3DF 0%,#F4F2ED 62%)">'
                f'<div class="phone" data-ph="{sB:.2f}"><div class="scr">{imgs}</div></div>{cards}'
                f'<div class="sub" style="bottom:110px">{subs(S["subs"], sB + 0.25, S["vo_len"])}</div></div>')
    # 3. présentatrice (prix)
    html.append(f'<div class="sc" data-a="{sC:.2f}" data-b="{sD:.2f}"><video muted preload="auto" data-off="{P["seg2"][0] - 0.1}" src="file://{clip}"></video>{ia}'
                f'<div class="sub">{subs(P["subs2"], sC + 0.1, t3 - 0.25)}</div></div>')
    # 4. fin
    html.append(f'<div class="sc" data-a="{sD:.2f}" data-b="{total + 1:.2f}" style="background:linear-gradient(170deg,#F4F2ED 0%,#EFE3DF 100%)">'
                f'<div style="position:absolute;left:0;right:0;top:640px;text-align:center"><span data-w="{sD + 0.1:.2f}" style="display:inline-flex;align-items:center;gap:24px">'
                f'<img src="file://{LOGO}" style="width:120px;height:120px"><span style="font-weight:700;font-size:140px;letter-spacing:-.04em;color:#1E1F21">Gloova</span></span></div>'
                f'<div style="position:absolute;left:0;right:0;top:880px;text-align:center"><span data-w="{sD + 0.35:.2f}" style="display:inline-block;background:#1E1F21;color:#fff;font-weight:700;font-size:44px;padding:30px 52px;border-radius:60px">{E["cta"]}</span></div>'
                f'<div style="position:absolute;left:0;right:0;top:1060px;text-align:center;color:rgba(30,31,33,.6);font-weight:600;font-size:36px"><span data-w="{sD + 0.6:.2f}">{E["small"]}</span></div></div>')
    css = CSS.replace('file://A/', f'file://{A}/')
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(html)}<script>{JS}</script></body></html>'
    times = dict(sA=sA, sB=sB, sC=sC, sD=sD)
    return page, round(total, 2), times


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('fiche'); ap.add_argument('sortie'); ap.add_argument('--still')
    a = ap.parse_args()
    v = json.load(open(a.fiche, encoding='utf-8'))
    page, total, T = build(v)
    tmpd = ICI / 'tmp'; tmpd.mkdir(exist_ok=True)
    hp = tmpd / f'{v["id"]}.html'; hp.write_text(page)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': W, 'height': H}); pg.goto(f'file://{hp}'); pg.wait_for_timeout(600)
        pg.evaluate("Promise.all([...document.querySelectorAll('video')].map(v=>v.readyState>=1?0:new Promise(r=>{v.onloadedmetadata=r;setTimeout(r,5000)})))")
        if a.still:
            for s in a.still.split(','):
                pg.evaluate(f'renderAt({s})'); pg.wait_for_timeout(50)
                f = tmpd / f'{v["id"]}-{s}.jpg'; pg.screenshot(path=str(f), type='jpeg', quality=85); print(f)
            b.close(); print('durée', total, T); return
        vid = tmpd / f'{v["id"]}.video.mp4'
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', str(vid)], stdin=subprocess.PIPE)
        for i in range(int(total * FPS)):
            pg.evaluate(f'renderAt({i / FPS})'); ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close(); ff.wait(); b.close()
    V = v['audio']
    ins = ['-i', str(vid), '-i', str(ICI / V['p1']), '-i', str(ICI / V['vo']), '-i', str(ICI / V['p2']), '-i', str(ICI / 'music' / V['music'])]
    d1 = int((T['sA'] + 0.0) * 1000); d2 = int((T['sB'] + 0.25) * 1000); d3 = int((T['sC'] + 0.1) * 1000)
    flt = (f"[1:a]adelay={d1}|{d1},volume=1.5[a1];[2:a]adelay={d2}|{d2},volume=1.5[a2];[3:a]adelay={d3}|{d3},volume=1.5[a3];"
           f"[4:a]apad,atrim=0:{total:.2f},afade=t=in:d=0.5,afade=t=out:st={total - 1.5:.2f}:d=1.5,volume=0.16[m];"
           f"[a1][a2][a3][m]amix=inputs=4:normalize=0,alimiter=limit=0.95[a]")
    out = Path(a.sortie); out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', flt, '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '22',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', f'{total:.2f}', '-movflags', '+faststart', str(out)], check=True)
    vid.unlink(missing_ok=True); print(out, f'{total:.1f}s')


if __name__ == '__main__':
    main()
