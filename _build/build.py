#!/usr/bin/env python3
"""BuildGames Hub static site generator.
Edit data/tools.json or data/showcase.json, then run: python3 _build/build.py  (add --og to regenerate share images)"""
import json, shutil, html, datetime, sys, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(ROOT/"_build"))
from art import ART, logo, P, INK, CREAM
OUT=ROOT/"dist"; ASSETS=ROOT/"assets"
# ---- CONFIG (single spot) ----
SITE_NAME="BuildGames Hub"
TAGLINE="Every way to build a game — from AI prompts to Unreal."
BASE_URL="https://bmau37.github.io/buildgames-hub"
SPONSOR_EMAIL="sponsor@example.com"  # placeholder
LAST_VERIFIED="2026-10-13"
AGES={"kids":("Kids","6–12","for-kids","Kid","I'm a kid",P["mustard"]),"teens":("Teens","13–17","for-teens","Teen","I'm a teen",P["sky"]),"adults":("Grown-ups","18+","for-adults","Grown-up","I'm a grown-up",P["teal"])}
FEATURED=["godot-engine","claude-code","blender","pico-8","scratch","itch-io","aseprite","unreal-engine"]
# ------------------------------
E=html.escape; TODAY=datetime.date.today().isoformat()
tools=json.load(open(ROOT/"data/tools.json"));PL={"free":"Free","freemium":"Free to start","paid":"Paid"};LL={"open-source":"Open source","proprietary":"Closed source"}; show=json.load(open(ROOT/"data/showcase.json"))
BY={t["slug"]:t for t in tools}
exec(open(ROOT/"_build/data_defs.py").read())
CC={"ai":P["plum"],"engine":P["sky"],"art":P["tomato"],"audio":P["teal"],"kids":P["mustard"],"vr":P["pink"],"publish":P["leaf"],"learn":P["stone"]}
CATS={k:(n,i,CC[k]) for k,(n,i,_) in CATS.items()}
# guard: never publish private Claude artifact/share links
for s_ in show:
    if re.search(r"claude\.(ai|site)",json.dumps(s_)): sys.exit(f"Refusing to build: showcase '{s_['slug']}' contains a claude.ai link (private).")
def icon(n,size=18):
    s=(ASSETS/"icons"/f"{n}.svg").read_text()
    s=re.sub(r'<svg[^>]*>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="ic">',s,count=1)
    return re.sub(r'<!--.*?-->','',s,flags=re.S).strip()
WAVE=lambda c,flip=False:f'<svg class="wave{" flip" if flip else ""}" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0,40 C240,90 480,0 720,30 C960,60 1200,10 1440,40 L1440,80 L0,80Z" fill="{c}"/></svg>'
GRAIN="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.07'/%3E%3C/svg%3E"
CSS=f"""@font-face{{font-family:Inter;src:url(fonts/inter-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}}
@font-face{{font-family:Inter;src:url(fonts/inter-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}}
@font-face{{font-family:"Space Grotesk";src:url(fonts/space-grotesk-latin-500-normal.woff2) format("woff2");font-weight:500;font-display:swap}}
@font-face{{font-family:"Space Grotesk";src:url(fonts/space-grotesk-latin-700-normal.woff2) format("woff2");font-weight:700;font-display:swap}}
:root{{--ink:{INK};--cream:{CREAM};--paper:#fffaf2;--tomato:{P["tomato"]};--teal:{P["teal"]};--mustard:{P["mustard"]};--plum:{P["plum"]};--mut:#5d5873;--tink:#c2410c;--r:22px;
--s1:.25rem;--s2:.5rem;--s3:1rem;--s4:1.5rem;--s5:2.5rem;--s6:4rem;--sh:4px 4px 0 var(--ink),0 18px 34px -20px #3b1f9e55}}
*{{box-sizing:border-box}}[id]{{scroll-margin-top:80px}}html{{scroll-behavior:smooth}}
body{{margin:0;font:400 1rem/1.6 Inter,system-ui,sans-serif;color:var(--ink);background:radial-gradient(60vw 40vw at 100% 0,#efe7ff 0,transparent 70%) fixed,radial-gradient(50vw 40vw at 0 100%,#e3f7f3 0,transparent 70%) fixed,#fbf8f3;-webkit-font-smoothing:antialiased}}
h1,h2,h3,.disp{{font-family:"Space Grotesk",Inter,sans-serif;font-weight:700;line-height:1.08;letter-spacing:-.02em;margin:0 0 var(--s3)}}
h1{{font-size:clamp(2.2rem,6.5vw,4.2rem)}}h2{{font-size:clamp(1.6rem,4vw,2.4rem)}}h3{{font-size:1.15rem;margin:0}}
a{{color:var(--ink);text-decoration-thickness:2px;text-underline-offset:3px}}a:hover{{color:var(--tink)}}
:focus-visible{{outline:3px solid var(--plum);outline-offset:3px;border-radius:8px}}
.ic{{vertical-align:-3px;flex:none}}.wrap{{max-width:1160px;margin:auto;padding:0 var(--s3)}}
.skip{{position:absolute;left:-999px}}.skip:focus{{left:8px;top:8px;background:#fff;padding:8px;z-index:99}}
header.top{{position:sticky;top:0;z-index:20;background:#fbf8ffcc;backdrop-filter:blur(14px) saturate(1.4);-webkit-backdrop-filter:blur(14px) saturate(1.4);border-bottom:1px solid #1b163022;box-shadow:0 8px 24px -18px #3b1f9e66}}
header nav{{display:flex;gap:var(--s4);align-items:center;padding:.6rem var(--s3);max-width:1160px;margin:auto;overflow-x:auto;scrollbar-width:none}}
header .links{{display:flex;gap:var(--s4);align-items:center}}.navcta{{padding:.45rem .9rem;font-size:.9rem}}
.burger{{display:none;width:46px;height:42px;border:2.5px solid var(--ink);border-radius:12px;background:var(--mustard);box-shadow:3px 3px 0 var(--ink);flex-direction:column;justify-content:center;gap:5px;padding:0 10px;cursor:pointer}}.burger span{{display:block;height:3px;background:var(--ink);border-radius:2px;transition:transform .2s,opacity .2s}}
.open .burger span:nth-child(1){{transform:translateY(8px) rotate(45deg)}}.open .burger span:nth-child(2){{opacity:0}}.open .burger span:nth-child(3){{transform:translateY(-8px) rotate(-45deg)}}
.scrim{{position:fixed;inset:0;background:#1b163066;z-index:18}}
@media (max-width:760px){{header.top{{backdrop-filter:none;background:var(--cream)}}.burger{{display:flex}}header nav{{overflow:visible}}header .links{{position:fixed;top:0;right:0;bottom:0;width:min(82vw,320px);flex-direction:column;align-items:stretch;gap:0;padding:5rem 1.2rem 1.5rem;background:var(--cream);border-left:3px solid var(--ink);transform:translateX(105%);transition:transform .25s ease;z-index:19}}header .links a:not(.btn){{font:700 1.4rem "Space Grotesk";padding:.8rem 0;border-bottom:2px dashed #1b163033}}header .links .navcta{{margin-top:1.2rem;justify-content:center}}.open .links{{transform:none}}.burger{{position:relative;z-index:20}}}}
header nav a{{text-decoration:none;font-weight:600;white-space:nowrap;font-size:.95rem}}
.brand{{display:flex;align-items:center;gap:.5rem;margin-right:auto;font-family:"Space Grotesk";font-size:1.25rem;font-weight:700}}
.brand b{{color:var(--tink)}}
.btn{{display:inline-flex;align-items:center;gap:.5rem;font:700 1rem "Space Grotesk";background:var(--mustard);color:var(--ink);padding:.8rem 1.3rem;border:2.5px solid var(--ink);border-radius:14px;box-shadow:var(--sh);text-decoration:none;cursor:pointer;transition:transform .12s,box-shadow .12s}}
.btn:hover{{transform:translate(-2px,-2px);box-shadow:6px 6px 0 var(--ink);color:var(--ink)}}.btn:active{{transform:translate(3px,3px);box-shadow:1px 1px 0 var(--ink)}}
.btn.alt{{background:#fff}}.sec.inkbg .btn,.sec.inkbg .btn:hover{{color:var(--ink)}}.btn.dark{{background:var(--ink);color:var(--cream)}}
.hud{{display:inline-flex;gap:.6rem;font:700 .8rem/1 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;background:var(--ink);color:var(--mustard);padding:.5rem .8rem;border-radius:6px;box-shadow:3px 3px 0 var(--tomato)}}
.hud i{{font-style:normal;color:var(--cream)}}
.bar{{display:inline-block;width:80px;height:10px;border:2px solid var(--cream);background:linear-gradient(90deg,var(--teal) 70%,transparent 0);vertical-align:middle}}
/* sections */
.sec{{position:relative;padding:var(--s6) 0}}.sec.alt{{background:var(--paper)}}.sec.inkbg{{background:var(--ink);color:var(--cream)}}.sec.inkbg a{{color:var(--cream)}}
.sec.diag{{clip-path:polygon(0 4vw,100% 0,100% calc(100% - 4vw),0 100%);padding:calc(var(--s6) + 4vw) 0;margin:-2vw 0}}
.wave{{display:block;width:100%;height:60px;margin-bottom:-1px}}.wave.flip{{transform:scaleY(-1);margin:-1px 0 0}}
.eyebrow{{font:700 .8rem ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--tink);margin-bottom:var(--s2);display:block}}
/* hero */
.hero{{display:grid;grid-template-columns:1.1fr 1fr;gap:var(--s5);align-items:center;padding:var(--s5) 0 var(--s6)}}
.hero p.lead{{font-size:1.2rem;color:var(--mut);max-width:34em}}.hero .cta{{display:flex;gap:var(--s3);flex-wrap:wrap;margin-top:var(--s4)}}
.mark{{background:linear-gradient(transparent 62%,var(--mustard) 0)}}
.stage{{position:relative;aspect-ratio:1/0.85}}
.stage .layer{{position:absolute;transition:transform .2s ease-out;will-change:transform}}
.stage .blob{{inset:4% 0 0 6%;background:var(--teal);border:2.5px solid var(--ink);border-radius:58% 42% 46% 54%/50% 60% 40% 50%}}
.stage .main{{inset:12% 6% 14% 2%;border:2.5px solid var(--ink);border-radius:var(--r);overflow:hidden;box-shadow:8px 8px 0 var(--ink);transform:rotate(-2deg)}}
.stage .main svg{{display:block;width:100%;height:100%}}
.stage .chip{{background:#fff;border:2.5px solid var(--ink);border-radius:14px;padding:.5rem .8rem;font:700 .9rem "Space Grotesk";box-shadow:var(--sh);display:flex;gap:.4rem;align-items:center}}
.c1{{top:2%;right:4%;transform:rotate(4deg)}}.c2{{bottom:4%;left:0;transform:rotate(-5deg)}}.c3{{bottom:22%;right:-2%;transform:rotate(3deg);background:var(--mustard)!important}}
/* bento categories */
.bento{{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:170px;gap:var(--s3)}}
.tile{{position:relative;border:2.5px solid var(--ink);border-radius:var(--r);overflow:hidden;text-decoration:none;box-shadow:var(--sh);transition:transform .18s,box-shadow .18s;background:var(--c)}}
.tile svg.art{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.tile .lbl{{position:absolute;left:12px;bottom:12px;background:#fff;border:2.5px solid var(--ink);border-radius:12px;padding:.35rem .7rem;font:700 1rem "Space Grotesk";display:flex;gap:.4rem;align-items:center}}
.tile .n{{position:absolute;right:12px;top:12px;font:700 .75rem ui-monospace,monospace;background:var(--ink);color:var(--cream);padding:.3rem .5rem;border-radius:6px}}
.tile:hover{{transform:translate(-3px,-3px) rotate(-.6deg);box-shadow:8px 8px 0 var(--ink)}}
.tile:nth-child(1){{grid-column:span 2;grid-row:span 2}}.tile:nth-child(2){{grid-row:span 2}}
/* carousel */
.rail{{display:flex;gap:var(--s4);overflow-x:auto;scroll-snap-type:x mandatory;padding:var(--s3) var(--s3) var(--s5);scrollbar-width:thin}}
.feat{{scroll-snap-align:start;flex:0 0 min(280px,78vw);background:#fff;border:2.5px solid var(--ink);border-radius:var(--r);box-shadow:var(--sh);overflow:hidden;transition:transform .18s}}
.feat:nth-child(odd){{transform:rotate(-1.2deg)}}.feat:nth-child(even){{transform:rotate(1deg) translateY(10px)}}.feat:hover{{transform:rotate(0) translateY(-6px)}}
.feat .top{{height:120px;background:var(--c);border-bottom:3px solid var(--ink);display:grid;place-items:center;color:var(--ink)}}
.feat .top span{{font:700 3.2rem "Space Grotesk";background:#fff;border:2.5px solid var(--ink);border-radius:50%;width:84px;height:84px;display:grid;place-items:center;box-shadow:var(--sh)}}
.feat .bd{{padding:var(--s3) var(--s4) var(--s4)}}
/* paths staggered */
.path{{display:grid;grid-template-columns:1fr 1.2fr;gap:var(--s5);align-items:center;margin:var(--s5) 0}}
.path:nth-child(even){{grid-template-columns:1.2fr 1fr}}.path:nth-child(even) .pic{{order:2}}
.pic{{position:relative}}.pic:before{{content:"";position:absolute;inset:-6% -4% -10% 4%;background:var(--c);border-radius:42% 58% 63% 37%/45% 41% 59% 55%;border:2.5px solid var(--ink);z-index:0}}
.pic svg{{position:relative;z-index:1;width:100%;height:auto;border:2.5px solid var(--ink);border-radius:var(--r);box-shadow:var(--sh);transform:rotate(-1.5deg)}}
.path:nth-child(even) .pic svg{{transform:rotate(1.5deg)}}
.lvl{{color:var(--ink);font:700 .75rem ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;border:2px solid var(--ink);border-radius:99px;padding:.2rem .6rem;background:#fff}}
.lvl.beginner{{background:#c9f0cf}}.lvl.intermediate{{background:#ffe9a8}}.lvl.advanced{{background:#ffc9bd}}
/* directory */
.controls{{display:grid;grid-template-columns:2fr repeat(6,1fr);gap:var(--s2);margin:var(--s4) 0;background:#fff;border:2.5px solid var(--ink);border-radius:22px;padding:var(--s2);box-shadow:var(--sh)}}
.controls input,.controls select{{font:inherit;background:var(--cream);color:var(--ink);border:2px solid transparent;border-radius:10px;padding:.65rem .7rem;min-width:0}}
.controls input:focus,.controls select:focus{{border-color:var(--plum);outline:none}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:var(--s4) var(--s3)}}
.card{{position:relative;background:#fff;border:2.5px solid var(--ink);border-radius:var(--r) var(--r) var(--r) 6px;padding:var(--s4);display:flex;flex-direction:column;gap:.5rem;transition:transform .16s,box-shadow .16s;box-shadow:var(--sh)}}
.card:before{{content:"";position:absolute;right:-3px;top:-3px;width:54px;height:54px;background:var(--c);border:2.5px solid var(--ink);border-radius:0 var(--r) 0 40px}}
.card:hover{{transform:translate(-3px,-4px);box-shadow:7px 8px 0 var(--ink)}}
.card .cat{{font:700 .75rem ui-monospace,monospace;text-transform:uppercase;letter-spacing:.06em;display:flex;gap:.35rem;align-items:center;color:var(--mut)}}
.card h3 a{{text-decoration:none}}.card h3 a:after{{content:"";position:absolute;inset:0}}.card p{{margin:0;color:var(--mut);font-size:.95rem}}
.meta{{display:flex;gap:.35rem;flex-wrap:wrap;margin-top:auto;padding-top:.4rem}}
.pill{{font:600 .75rem Inter;padding:.15rem .55rem;border-radius:99px;background:var(--cream);border:1.5px solid #1b163033}}
.empty{{grid-column:1/-1;text-align:center;padding:var(--s5);border:3px dashed var(--ink);border-radius:var(--r);background:var(--paper)}}
.empty svg{{width:180px;height:auto}}
.dirbar{{display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-bottom:var(--s3)}}.dirbar p{{margin:0}}
.seg{{display:inline-flex;border:2.5px solid var(--ink);border-radius:14px;overflow:hidden;background:#fff;box-shadow:3px 3px 0 var(--ink)}}.seg button{{font:700 .9rem "Space Grotesk";border:0;background:none;padding:.5rem .9rem;display:flex;gap:.35rem;align-items:center;cursor:pointer;color:var(--ink)}}.seg button[aria-pressed=true]{{background:var(--ink);color:var(--cream)}}
.group{{margin:var(--s5) 0}}.ghead{{display:grid;grid-template-columns:150px 1fr auto;gap:var(--s4);align-items:center;margin-bottom:var(--s3);padding-bottom:var(--s3);border-bottom:3px solid var(--ink)}}
.ghead .gart{{width:150px;height:auto;border:2.5px solid var(--ink);border-radius:16px;transform:rotate(-2deg);box-shadow:var(--sh)}}.ghead h3{{font-size:1.6rem}}.ghead a{{font-weight:600;font-size:.9rem}}
.gcount{{font:700 3rem/1 "Space Grotesk";color:var(--c);-webkit-text-stroke:2px var(--ink)}}
.dir.grid .items{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:var(--s4) var(--s3)}}
.dir.list .items{{display:grid;grid-template-columns:1fr 1fr;gap:0 var(--s5)}}
.dir.list .card{{flex-direction:row;flex-wrap:wrap;align-items:baseline;gap:.2rem .7rem;padding:.8rem .2rem .8rem 1.2rem;border:0;border-bottom:2px dashed #1b163033;border-radius:0;box-shadow:none;background:none}}
.dir.list .card:before{{width:10px;height:10px;top:1.25rem;left:0;right:auto;border-width:2px;border-radius:50%}}.dir.list .card:hover{{transform:translateX(4px);box-shadow:none;background:#fff8}}
.dir.list .card .cat{{display:none}}.dir.list .card h3{{font-size:1.05rem}}.dir.list .card p{{flex-basis:100%;font-size:.88rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}.dir.list .meta{{order:2;margin:0;padding:0}}
@media (max-width:760px){{.dir.list .items{{grid-template-columns:1fr}}.ghead{{grid-template-columns:90px 1fr auto;gap:var(--s3)}}.ghead .gart{{width:90px}}.ghead h3{{font-size:1.2rem}}.gcount{{font-size:2rem}}.dirbar{{flex-wrap:wrap}}}}
.age{{display:inline-flex;align-items:center;font:700 .72rem ui-monospace,monospace;letter-spacing:.03em;padding:.18rem .55rem;border:2px solid var(--ink);border-radius:8px;color:var(--ink);text-decoration:none;transform:rotate(-2deg);box-shadow:2px 2px 0 var(--ink)}}
.age.a-kids{{background:#ffd76a}}.age.a-teens{{background:#a9dcff}}.age.a-adults{{background:#9fe6dc}}.meta .age:nth-child(even){{transform:rotate(2deg)}}
.band-who{{background:radial-gradient(50% 80% at 10% 10%,#ffc2ae 0,transparent 70%),radial-gradient(50% 80% at 90% 90%,#ffd98a 0,transparent 70%),#ff8d72}}.band-who .eyebrow{{color:var(--ink)}}.band-who h2,.band-who p.mut{{color:var(--ink)}}
.who{{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4);margin-top:var(--s4)}}
.whob{{position:relative;display:flex;flex-direction:column;background:#fff;border:2.5px solid var(--ink);border-radius:28px;box-shadow:7px 7px 0 var(--ink);overflow:hidden;text-decoration:none;min-height:120px;transition:transform .18s,box-shadow .18s}}
.whob .wart{{width:100%;height:auto;display:block;border-bottom:3.5px solid var(--ink)}}.whob .wlbl{{padding:1rem 1.2rem 1.2rem;display:flex;flex-direction:column}}.whob b{{font:700 1.7rem "Space Grotesk"}}.whob small{{font-weight:600;color:var(--mut);font-size:.95rem}}
.whob .go{{position:absolute;right:14px;bottom:18px;width:48px;height:48px;border-radius:50%;background:var(--c);border:3px solid var(--ink);display:grid;place-items:center;transition:transform .2s}}
.whob:hover{{transform:translate(-3px,-5px) rotate(-1deg);box-shadow:10px 12px 0 var(--ink);color:var(--ink)}}.whob:hover .go{{transform:rotate(-20deg) scale(1.12)}}
.whob:nth-child(2):hover{{transform:translate(-3px,-5px) rotate(1deg)}}
.btn,.whob{{isolation:isolate}}.btn:after,.whob:after{{content:"";position:absolute;inset:-14px;pointer-events:none;opacity:0;z-index:-1;background:radial-gradient(circle,var(--tomato) 3px,transparent 4px) 8% 20%/22px 22px no-repeat,radial-gradient(circle,var(--teal) 3px,transparent 4px) 92% 12%/22px 22px no-repeat,radial-gradient(circle,var(--plum) 3px,transparent 4px) 85% 90%/22px 22px no-repeat,radial-gradient(circle,var(--mustard) 4px,transparent 5px) 12% 88%/22px 22px no-repeat;transform:scale(.6);transition:transform .3s cubic-bezier(.3,1.6,.5,1),opacity .2s}}
.btn{{position:relative}}.btn:hover:after,.whob:hover:after{{opacity:1;transform:scale(1)}}
.sticker{{position:absolute;z-index:3;font:700 .8rem "Space Grotesk";background:#fff;border:3px solid var(--ink);border-radius:999px;padding:.35rem .8rem;box-shadow:3px 3px 0 var(--ink);transform:rotate(-8deg)}}
@keyframes bob{{50%{{transform:translateY(-8px) rotate(var(--rot,0deg))}}}}@keyframes spin{{to{{transform:rotate(360deg)}}}}
.stage .chip{{animation:bob 4s ease-in-out infinite}}.c2{{animation-delay:-1.3s!important;--rot:-5deg}}.c3{{animation-delay:-2.6s!important;--rot:3deg}}.c1{{--rot:4deg}}
.spark{{position:absolute;width:34px;height:34px;animation:spin 9s linear infinite}}
.band-color{{background:var(--c);border-block:3.5px solid var(--ink)}}
.steps-simple{{counter-reset:s;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:var(--s3);list-style:none;padding:0}}.steps-simple li{{counter-increment:s;background:#fff;border:2.5px solid var(--ink);border-radius:22px;padding:1.2rem;box-shadow:var(--sh);font-size:1.05rem}}.steps-simple li:before{{content:"Step " counter(s);display:block;font:700 .8rem ui-monospace,monospace;color:var(--tink);margin-bottom:.3rem;letter-spacing:.08em;text-transform:uppercase}}
.parent{{background:#fff;border:2.5px solid var(--ink);border-left:14px solid var(--teal);border-radius:22px;padding:1.4rem 1.6rem;box-shadow:var(--sh)}}.parent h2{{font-size:1.5rem}}.parent li{{margin:.4rem 0}}
.agepick{{display:flex;gap:.6rem;flex-wrap:wrap;margin:var(--s3) 0}}.agepick a{{min-height:48px;display:inline-flex;align-items:center;padding:.5rem 1rem;border:3px solid var(--ink);border-radius:14px;background:#fff;font-weight:700;text-decoration:none;box-shadow:3px 3px 0 var(--ink)}}.agepick a[aria-current]{{background:var(--ink);color:var(--cream)}}
header nav a{{min-height:44px;display:inline-flex;align-items:center}}
@media (max-width:860px){{.who{{grid-template-columns:1fr}}.whob{{flex-direction:row;align-items:center}}.whob .wart{{width:38%;border-bottom:0;border-right:3.5px solid var(--ink);align-self:stretch;object-fit:cover}}.whob b{{font-size:1.35rem}}.whob .go{{width:40px;height:40px;right:10px;bottom:auto}}}}
@media (prefers-reduced-motion:reduce){{.stage .chip,.spark{{animation:none}}}}
/* ---- 2026 modern layer ---- */
.mhero{{position:relative;overflow:hidden;padding:clamp(2rem,5vw,4.5rem) 0 clamp(2.5rem,6vw,5rem)}}
.mesh{{position:absolute;inset:-20%;z-index:-1;background:radial-gradient(40% 50% at 15% 20%,#b9a4ff 0,transparent 70%),radial-gradient(35% 45% at 85% 15%,#ffb199 0,transparent 70%),radial-gradient(40% 50% at 75% 85%,#8fe3d6 0,transparent 70%),radial-gradient(30% 40% at 30% 90%,#ffe08a 0,transparent 70%),#f7f2ff;filter:saturate(1.05)}}
.mgrid{{display:grid;grid-template-columns:.95fr 1.2fr;gap:clamp(1.5rem,4vw,3.5rem);align-items:center}}
.mcopy h1{{font-size:clamp(2.4rem,6vw,4.4rem);letter-spacing:-.035em;margin:.8rem 0 1rem}}.grad{{background:linear-gradient(95deg,#5b2fe0,#d63a5e 60%,#c4461a);-webkit-background-clip:text;background-clip:text;color:transparent}}
.mcopy .lead{{font-size:1.2rem;color:#46405e;max-width:32em}}
.newpill{{display:inline-flex;gap:.5rem;align-items:center;font-size:.88rem;font-weight:600;background:#ffffffb3;backdrop-filter:blur(8px);border:1px solid #ffffff;border-radius:999px;padding:.35rem .9rem .35rem .4rem;box-shadow:0 6px 20px -10px #4b2fb366}}.newpill b{{background:#5b3fd9;color:#fff;border-radius:999px;padding:.1rem .55rem;font-size:.78rem}}
.glass{{background:#ffffffbf;backdrop-filter:blur(16px) saturate(1.3);-webkit-backdrop-filter:blur(16px) saturate(1.3);border:1px solid #ffffffee;border-radius:28px;box-shadow:0 30px 60px -30px #3b1f9e66,0 2px 6px #1b16300d}}
.pfwrap{{padding:.4rem;margin-top:1.4rem}}.pfwrap .pf{{background:transparent;border:0;box-shadow:none;padding:1rem}}
.pfwrap .pf input[type=text]{{background:#fff;border:2px solid #d9d0f5;border-radius:18px;box-shadow:inset 0 1px 2px #0000000d}}.pfwrap .pf input[type=text]:focus{{border-color:#6a3df0;outline:3px solid #6a3df055;outline-offset:1px}}
.pfwrap .btn{{background:linear-gradient(135deg,#6a3df0,#5b3fd9);color:#fff;border:0;box-shadow:0 10px 24px -10px #5b3fd9}}.pfwrap .btn:hover{{color:#fff;box-shadow:0 14px 30px -10px #5b3fd9}}
.pfwrap .agetog button{{border:2px solid #d9d0f5;background:#fff;border-radius:12px}}.pfwrap .agetog button[aria-pressed=true]{{background:#1b1630;border-color:#1b1630}}.pfwrap .chip{{border:1.5px solid #d9d0f5;background:#ffffffcc}}.pfwrap .chip:hover{{background:#fff3c9;border-color:#f2b134}}
.stats{{display:flex;gap:1.2rem;flex-wrap:wrap;margin-top:1.1rem;font-weight:600}}.stats a{{text-decoration:none;display:inline-flex;gap:.35rem;align-items:center}}
.mart{{position:relative;margin-right:clamp(-4rem,-4vw,0rem);align-self:start;margin-top:clamp(0rem,6vw,5rem)}}.pfwrap .chip:nth-child(n+7){{display:none}}.heroimg img{{display:block;width:100%;height:auto;border-radius:32px;box-shadow:0 40px 80px -30px #3b1f9e80,0 0 0 1px #ffffff99;animation:hfloat 7s ease-in-out infinite}}
@keyframes hfloat{{50%{{transform:translateY(-12px)}}}}
.float{{position:absolute;display:inline-flex;gap:.4rem;align-items:center;font:600 .9rem Inter;background:#ffffffd9;backdrop-filter:blur(10px);border:1px solid #fff;border-radius:999px;padding:.5rem .9rem;box-shadow:0 12px 30px -12px #3b1f9e88;animation:bob 5s ease-in-out infinite}}.f1{{left:-14px;top:12%}}.f2{{right:-10px;bottom:10%;animation-delay:-2s}}
.how{{padding:clamp(2.5rem,6vw,4.5rem) var(--s3)}}.howrow{{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4);margin-top:var(--s4)}}
.hstep{{position:relative;background:#fff;border-radius:28px;padding:1.4rem 1.5rem 1.6rem;box-shadow:0 24px 50px -30px #3b1f9e55,0 0 0 1px #ece6fb;transition:transform .2s}}.hstep:hover{{transform:translateY(-6px)}}
.hstep .clay img{{width:96px;height:96px;margin:-.4rem 0 .4rem -.4rem;filter:drop-shadow(0 10px 14px #3b1f9e33);transition:transform .3s cubic-bezier(.3,1.6,.5,1)}}.hstep:hover .clay img{{transform:rotate(-8deg) scale(1.08)}}
.hn{{position:absolute;right:1.2rem;top:1.1rem;font:700 2.6rem/1 "Space Grotesk";color:#ece6fb}}.hstep h3{{font-size:1.35rem;margin-bottom:.4rem}}.hstep p{{margin:0;color:var(--mut)}}
.famband{{display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(1.5rem,4vw,3.5rem);align-items:center;padding-block:clamp(2rem,5vw,4rem)}}.famimg img{{display:block;width:100%;height:auto;border-radius:32px;box-shadow:0 30px 70px -30px #e2486b88}}
.famband .cta{{display:flex;gap:var(--s3);flex-wrap:wrap;margin-top:var(--s4)}}
.tclay{{position:absolute;left:10px;top:8px;width:64px;height:64px;filter:drop-shadow(0 6px 10px #0004);z-index:2;transition:transform .3s cubic-bezier(.3,1.6,.5,1)}}.tile:hover .tclay{{transform:rotate(-10deg) scale(1.1)}}
@media (max-width:860px){{.pfwrap .chip:nth-child(n+5){{display:none}}.mgrid,.famband{{grid-template-columns:1fr}}.mart{{order:-1}}.howrow{{grid-template-columns:1fr}}.f1{{left:6px}}.f2{{right:6px}}.mcopy h1{{margin-top:.6rem}}}}
@media (prefers-reduced-motion:reduce){{.heroimg img,.float{{animation:none}}}}
/* showcase stack */
.stack{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:var(--s5)}}
.sc{{position:relative;background:#fff;border:2.5px solid var(--ink);border-radius:var(--r);padding:var(--s4);box-shadow:var(--sh)}}.stack{{isolation:isolate}}.scimg{{float:right;width:110px;height:auto;margin:0 0 .5rem 1rem;border:2.5px solid var(--ink);border-radius:14px;transform:rotate(3deg)}}
.sc:before,.sc:after{{content:"";position:absolute;inset:0;border:2.5px solid var(--ink);border-radius:var(--r);z-index:-1}}
.sc:before{{background:var(--mustard);transform:rotate(-3deg) translate(-6px,6px)}}.sc:after{{background:var(--teal);transform:rotate(2.5deg) translate(8px,10px);z-index:-2}}
.vid{{aspect-ratio:16/9;border:2.5px solid var(--ink);border-radius:14px;background:var(--ink) repeating-linear-gradient(0deg,#ffffff08 0 2px,transparent 2px 4px);color:var(--cream);display:grid;place-items:center;text-align:center;margin:var(--s3) 0;overflow:hidden}}
.vid video{{width:100%;height:100%;object-fit:cover}}
.slot.solid{{border-style:solid;background:var(--paper);color:var(--ink)}}.vid.portrait{{aspect-ratio:390/590;max-width:340px;margin-inline:auto}}
.slot{{border:2px dashed #1b163055;border-radius:12px;padding:.6rem .8rem;margin:.4rem 0;color:var(--mut);display:flex;gap:.5rem}}
/* ticket sponsor */
.ticket{{display:grid;grid-template-columns:auto 1fr auto;gap:var(--s4);align-items:center;background:var(--mustard);border:2.5px solid var(--ink);border-radius:18px;padding:var(--s4) var(--s5);box-shadow:var(--sh);
-webkit-mask:radial-gradient(circle 16px at 0 50%,#0000 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 16px at 100% 50%,#0000 98%,#000) right/51% 100% no-repeat;margin:var(--s5) 0}}
.ticket .stub{{font:700 .8rem ui-monospace,monospace;writing-mode:vertical-rl;transform:rotate(180deg);border-right:3px dashed var(--ink);padding-left:var(--s3);letter-spacing:.15em}}
/* newsletter blob */
.news{{position:relative;background:#5b3fd9;color:#fff;border:2.5px solid var(--ink);border-radius:46px 18px 46px 18px;padding:var(--s5);box-shadow:8px 8px 0 var(--ink);overflow:hidden}}
.news:after{{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;background:var(--tomato);border:2.5px solid var(--ink);border-radius:50%}}
.news>*{{position:relative;z-index:1}}.news form{{display:flex;gap:var(--s2);flex-wrap:wrap;max-width:520px}}
.news input{{flex:1 1 220px;font:inherit;padding:.8rem 1rem;border:2.5px solid var(--ink);border-radius:14px}}
.soon{{font:700 .7rem ui-monospace,monospace;background:var(--mustard);color:var(--ink);padding:.2rem .5rem;border-radius:6px;vertical-align:middle;border:2px solid var(--ink)}}
/* page bits */
.crumbs{{font-size:.9rem;color:var(--mut);margin:var(--s4) 0 var(--s3);display:flex;gap:.3rem;align-items:center;flex-wrap:wrap}}.crumbs a{{color:var(--mut)}}
.phead{{display:grid;grid-template-columns:1.4fr 1fr;gap:var(--s5);align-items:center;margin-bottom:var(--s5)}}
.phead>svg{{width:100%;height:auto;border:2.5px solid var(--ink);border-radius:var(--r);box-shadow:var(--sh);transform:rotate(1.5deg)}}
.facts{{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:2.5px solid var(--ink);border-radius:18px;overflow:hidden;box-shadow:var(--sh)}}
.facts th,.facts td{{padding:.75rem 1rem;text-align:left;vertical-align:top;border-bottom:1.5px solid #1b163022}}.facts tr:last-child>*{{border-bottom:0}}.facts th{{background:var(--paper);width:30%;font-family:"Space Grotesk"}}
.note{{background:#fff;border-left:6px solid var(--teal);border-radius:0 14px 14px 0;padding:var(--s3) var(--s4);margin:var(--s4) 0}}
ol.steps{{list-style:none;counter-reset:s;padding:0}}ol.steps li{{counter-increment:s;position:relative;padding:var(--s4) var(--s4) var(--s4) 4.5rem;margin:var(--s3) 0;background:#fff;border:2.5px solid var(--ink);border-radius:18px;box-shadow:var(--sh)}}
ol.steps li:nth-child(even){{margin-left:var(--s5)}}
ol.steps li:before{{content:counter(s);position:absolute;left:1rem;top:1rem;width:2.4rem;height:2.4rem;display:grid;place-items:center;font:700 1.2rem "Space Grotesk";background:var(--mustard);border:2.5px solid var(--ink);border-radius:10px}}
.prose{{max-width:760px}}.prose h2{{margin-top:var(--s5)}}
footer{{background:var(--ink);color:var(--cream);padding:var(--s5) 0 var(--s4);margin-top:var(--s6)}}footer a{{color:var(--cream)}}
.fgrid{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:var(--s5)}}.fgrid h4{{font:700 .8rem ui-monospace,monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--mustard);margin:0 0 .6rem}}
.fgrid ul{{list-style:none;padding:0;margin:0;line-height:2}}.fine{{border-top:1px solid #ffffff22;margin-top:var(--s5);padding-top:var(--s3);font-size:.85rem;opacity:.75}}
@media (max-width:860px){{.hero,.phead,.path,.path:nth-child(even){{grid-template-columns:1fr}}.path:nth-child(even) .pic{{order:0}}
.bento{{grid-template-columns:1fr 1fr;grid-auto-rows:140px}}.tile:nth-child(1){{grid-column:span 2}}.tile:nth-child(2){{grid-row:span 1}}.tile:nth-child(8){{grid-column:span 2}}
.controls{{grid-template-columns:1fr 1fr;border-radius:22px}}.controls input{{grid-column:1/-1}}.fgrid{{grid-template-columns:1fr 1fr}}.ticket{{grid-template-columns:1fr;text-align:center;padding:var(--s4)}}.ticket .stub{{display:none}}
ol.steps li:nth-child(even){{margin-left:0}}header nav{{gap:var(--s3)}}.brand span{{font-size:1.05rem}}.stage{{margin:0 var(--s3)}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;scroll-behavior:auto!important}}}}"""
URLS=[]
def page(path,title,desc,body,ld=None,crumbs=None,og="home",wide=False):
    depth=path.count("/");pre="../"*depth
    canon=BASE_URL+"/"+path.replace("index.html","")
    cr=""
    if crumbs:
        items=[("Home","index.html")]+crumbs
        cr='<nav class="crumbs wrap" aria-label="Breadcrumb">'+f' {icon("chevron-right",14)} '.join(f'<a href="{pre}{h}">{E(n)}</a>' if h else f'<span aria-current="page">{E(n)}</span>' for n,h in items)+'</nav>'
        bl={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,**({"item":f"{BASE_URL}/{h}"} if h else {})} for i,(n,h) in enumerate(items)]}
        ld=[x for x in (ld,bl) if x]
    ldj=f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    nav="".join(f'<a href="{pre}{h}">{t}</a>' for h,t in [("start.html","Start here"),("tutorials/","Tutorials"),("videos/","Videos"),("index.html#tools","Tools"),("resources/","Resources")])
    ogimg=f"{BASE_URL}/og/{og}.png"
    cats="".join(f'<li><a href="{pre}categories/{k}.html">{n}</a></li>' for k,(n,_,_) in CATS.items())
    kind=("home" if path=="index.html" else "tool" if path.startswith("tools/") else "category" if path.startswith("categories/") else "compare" if path.startswith("compare") else "path" if path.startswith(("paths","guides")) else "tutorials" if path=="tutorials/index.html" else "tutorial" if path.startswith("tutorials/") else "videos" if path.startswith("videos") else "pathfinder" if path.startswith("pathfinder") else path.split("/")[0].replace(".html",""))
    s=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}"><meta name="theme-color" content="{CREAM}">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml"><link rel="icon" href="{pre}favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<meta property="og:site_name" content="{SITE_NAME}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canon}"><meta property="og:image" content="{ogimg}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{ogimg}">
<link rel="preload" href="{pre}fonts/space-grotesk-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{pre}style.css">{ldj}</head><body class="k-{kind}">
<a class="skip" href="#main">Skip to content</a><header class="top"><nav><a class="brand" href="{pre}index.html">{logo(32)}<span>BuildGames<b>Hub</b></span></a><div class="links" id="drawer"><a class="btn navcta" href="{pre}pathfinder/">{icon("sparkles",16)} Make a game</a>{nav}</div><button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button></nav></header><div class="scrim" hidden></div>
{cr}<main id="main">{body if wide else f'<div class="wrap">{body}</div>'}</main>
<footer>{WAVE(INK)[:0]}<div class="wrap"><div class="fgrid"><div><a class="brand" href="{pre}index.html" style="color:var(--cream)">{logo(32)}<span>BuildGames<b>Hub</b></span></a><p style="opacity:.8;max-width:30em">{TAGLINE} An independent, hand-curated directory for people who make games — from first-timers to studio vets.</p></div>
<div><h2 class="fh">Explore</h2><ul><li><a href="{pre}index.html#tools">All tools</a></li><li><a href="{pre}paths.html">Learning paths</a></li><li><a href="{pre}compare.html">Comparisons</a></li><li><a href="{pre}showcase.html">Showcase</a></li><li><a href="{pre}pathfinder/">Pathfinder</a></li><li><a href="{pre}tutorials/">Tutorials</a></li><li><a href="{pre}videos/">Videos</a></li></ul></div>
<div><h2 class="fh">Categories</h2><ul>{cats}</ul></div><div><h2 class="fh">Site</h2><ul><li><a href="{pre}about.html">About</a></li><li><a href="{pre}sponsor.html">Sponsor</a></li><li><a href="{pre}resources/faq.html">FAQ</a></li><li><a href="{pre}resources/glossary.html">Glossary</a></li><li><a href="{pre}llms.txt">llms.txt</a></li><li><a href="{pre}sitemap.xml">Sitemap</a></li><li><a href="{pre}CREDITS.txt">Credits &amp; licenses</a></li></ul></div></div>
<div class="fine">© {TODAY[:4]} {SITE_NAME} · Independent directory; names and trademarks belong to their owners. Prices change — confirm on official sites. Last verified: {LAST_VERIFIED}.</div></div></footer>
<script>(function(){{const h=document.querySelector("header.top"),b=h.querySelector(".burger"),sc=document.querySelector(".scrim");function t(o){{h.classList.toggle("open",o);b.setAttribute("aria-expanded",o);b.setAttribute("aria-label",o?"Close menu":"Open menu");sc.hidden=!o;document.body.style.overflow=o?"hidden":""}}b.onclick=()=>t(!h.classList.contains("open"));sc.onclick=()=>t(false);addEventListener("keydown",e=>{{if(e.key=="Escape")t(false)}});h.querySelectorAll(".links a").forEach(a=>a.addEventListener("click",()=>t(false)))}})();(function(){{const st=document.querySelector(".stage");if(!st||matchMedia("(prefers-reduced-motion: reduce)").matches)return;const L=[...st.querySelectorAll("[data-depth]")];addEventListener("pointermove",e=>{{const x=e.clientX/innerWidth-.5,y=e.clientY/innerHeight-.5;L.forEach(l=>{{const d=+l.dataset.depth;l.style.translate=`${{x*d}}px ${{y*d}}px`}})}});addEventListener("scroll",()=>{{L.forEach(l=>{{l.style.marginTop=(scrollY*+l.dataset.depth/200)+"px"}})}},{{passive:true}})}})()</script></body></html>"""
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
    if path!="404.html":URLS.append(canon)
def initials(n):return re.sub(r'[^A-Za-z0-9]','',n)[:1].upper()
def card(t,pre=""):
    n,ic,c=CATS[t["category"]]
    return f'''<article class="card" style="--c:{c}"><div class="cat">{icon(ic,14)} {n}</div><h3><a href="{pre}tools/{t["slug"]}.html">{E(t["name"])}</a></h3><p>{E(t["blurb"])}</p>
<div class="meta">{"".join(f'<span class="age a-{a}" title="Ages {AGES[a][1]}">{AGES[a][0]} {AGES[a][1]}</span>' for a in t.get("ages",[]))}<span class="lvl {t["skill"]}">{SK[t["skill"]]}</span><span class="pill">{PL[t["price"]]}</span>{"<span class=\"pill\">Open source</span>" if t["license"]=="open-source" else ""}</div></article>'''
def ticket(pre=""):
    return f'<aside class="ticket" aria-label="Sponsorship"><div class="stub">SPONSOR SLOT</div><div><span class="eyebrow" style="color:var(--ink)">{icon("star",14)} Sponsor slot open</span><h2 class="tkh" style="font-size:1.4rem;margin:.2rem 0">Your tool or game here.</h2><p style="margin:.3rem 0 0">Reach people who are actively building games — on the site and in the upcoming newsletter.</p></div><a class="btn dark" href="mailto:{SPONSOR_EMAIL}?subject=BuildGames%20Hub%20sponsorship">{icon("mail")} Get in touch</a></aside>'
NEWS=f'<section class="news"><span class="eyebrow" style="color:var(--mustard)">Weekly build log</span><h2>New tools &amp; AI workflows, once a week. <span class="soon">COMING SOON</span></h2><p>The newsletter isn\'t live yet. This form is a demo: it sends nothing and stores nothing.</p><form onsubmit="event.preventDefault();this.nextElementSibling.hidden=false"><input type="email" required placeholder="you@example.com" aria-label="Email address"><button class="btn">{icon("mail")} Notify me</button></form><p hidden role="status">Thanks! (Demo only — nothing was sent or stored.)</p></section>'
EMPTY=f'<div class="empty">{ART["kids"]}<h3>No tools match that combo… yet.</h3><p class="mut">Try clearing a filter, or <a href="mailto:{SPONSOR_EMAIL}?subject=Tool%20suggestion">suggest a tool</a>.</p></div>'
CLAYMAP={"ai":"ai","engine":"engines","art":"art","publish":"publish"}
def pic2(name,ws,alt,pre="../",cls="hpic"):
    return f'<picture class="{cls}"><source type="image/webp" srcset="{", ".join(f"{pre}img/{name}-{w}.webp {w}w" for w in ws)}" sizes="(max-width:860px) 100vw, 560px"><img src="{pre}img/{name}-{ws[-1]}.jpg" alt="{alt}" width="1280" height="720" decoding="async" fetchpriority="high"></picture>'
def clay2(n,pre="../",size=128,cls="clay2"):
    return f'<picture class="{cls}"><source type="image/webp" srcset="{pre}img/icon-{n}-128.webp 1x, {pre}img/icon-{n}-256.webp 2x"><img src="{pre}img/icon-{n}-128.png" srcset="{pre}img/icon-{n}-256.png 2x" alt="" width="{size}" height="{size}"></picture>'
def cluster(pre="../"):return '<div class="cluster" aria-hidden="true">'+"".join(clay2(n,pre,cls=f"clay2 c{i}") for i,n in enumerate(["ai","engines","art","publish"]))+'</div>'
def herovis(k,pre="../"):
    return f'<div class="hvis">{clay2(CLAYMAP[k],pre,cls="clay2 big")}</div>' if k in CLAYMAP else f'<div class="hvis svgv">{ART[k]}</div>'
exec(open(ROOT/"_build/teach.py").read(),globals())
exec(open(ROOT/"_build/more.py").read(),globals())
assert not (ROOT/"assets/games").exists(), "No hosted games allowed (Pondborn stays private until Play Store)"
def build():
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir();(OUT/"style.css").write_text(CSS);(OUT/".nojekyll").write_text("")
    shutil.copytree(ASSETS/"fonts",OUT/"fonts");shutil.copytree(ASSETS/"img",OUT/"img")
    if (ASSETS/"media").exists():shutil.copytree(ASSETS/"media",OUT/"media")
    if (ASSETS/"og").exists():shutil.copytree(ASSETS/"og",OUT/"og")
    for f in ("favicon-32.png","apple-touch-icon.png"):
        if (ASSETS/f).exists():shutil.copy(ASSETS/f,OUT/f)
    (OUT/"favicon.svg").write_text(logo(40).replace(' height="40"',''))
    (OUT/"logo.svg").write_text(logo(40).replace(' height="40"',''))
    (OUT/"CREDITS.txt").write_text(f"{SITE_NAME} credits\n\nFonts: Inter (The Inter Project Authors) and Space Grotesk (Florian Karsten), SIL Open Font License 1.1 — see fonts/OFL-*.txt\nIcons: Lucide (https://lucide.dev), ISC License — see icons-LICENSE.txt\nIllustrations, logo and OG images: original work made for this site.\nClay-style 3D images (hero, parent-and-kid, feature icons): AI-generated original artwork commissioned for and owned by BuildGames Hub.\n")
    shutil.copy(ASSETS/"icons/LICENSE-lucide.txt",OUT/"icons-LICENSE.txt")
    plats=sorted({p for t in tools for p in t["platforms"]})
    count={k:sum(t["category"]==k for t in tools) for k in CATS}
    tiles="".join(f'<a class="tile" style="--c:{c}" href="categories/{k}.html">{ART[k].replace("<svg ","<svg class=\"art\" preserveAspectRatio=\"xMidYMid slice\" ",1)}<span class="n">{count[k]:02d} TOOLS</span>{f'<img class="tclay" src="img/icon-{dict(ai="ai",engine="engines",art="art",publish="publish")[k]}-128.webp" alt="" width="64" height="64" loading="lazy">' if k in ("ai","engine","art","publish") else ""}<span class="lbl">{icon(i)} {n}</span></a>' for k,(n,i,c) in CATS.items())
    feat="".join(f'<article class="feat" style="--c:{CATS[BY[s]["category"]][2]}"><div class="top"><span>{initials(BY[s]["name"])}</span></div><div class="bd"><span class="lvl {BY[s]["skill"]}">{SK[BY[s]["skill"]]}</span><h3 style="margin:.6rem 0 .3rem"><a href="tools/{s}.html">{E(BY[s]["name"])}</a></h3><p class="mut" style="margin:0;font-size:.92rem">{E(BY[s]["blurb"])}</p></div></article>' for s in FEATURED if s in BY)
    paths="".join(f'<div class="path" style="--c:{c}"><div class="pic">{ART[s]}</div><div><span class="lvl {l}">{SK[l]}</span><h3 style="font-size:1.8rem;margin:.7rem 0">{E(t)}</h3><p class="mut">{len(st)} steps · {", ".join(dict.fromkeys(BY[x]["name"] for _,_,xs in st for x in xs[:1]))}</p><a class="btn alt" href="paths/{s}.html">Start the path {icon("arrow-right")}</a></div></div>' for (s,t,l,st),c in zip(PATHS,[P["sky"],P["plum"],P["tomato"],P["leaf"]]))
    shw="".join(f'<article class="sc">{f"<img src=\"{E(s["poster"])}\" alt=\"{E(s["title"])} gameplay\" width=390 height=590 loading=lazy class=scimg>" if s.get("poster") else ""}<span class="eyebrow">Case study · built with {", ".join(s["built_with"])}</span><h3 style="font-size:1.6rem">{E(s["title"])}</h3><p class="mut">{E(s["summary"])}</p><a href="showcase.html#{s["slug"]}">{E(s["status"])} {icon("arrow-right",14)}</a></article>' for s in show)
    newest=sorted(tools,key=lambda t:t["added"],reverse=True)[:6]
    def pic(name,ws,alt,cls="",sizes="100vw",eager=False):
        return f'<picture class="{cls}"><source type="image/webp" srcset="{", ".join(f"img/{name}-{w}.webp {w}w" for w in ws)}" sizes="{sizes}"><img src="img/{name}-{ws[0]}.jpg" srcset="{", ".join(f"img/{name}-{w}.jpg {w}w" for w in ws)}" sizes="{sizes}" alt="{alt}" width="1280" height="720" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async"></picture>'
    def clay(n,alt=""):return f'<picture class="clay"><source type="image/webp" srcset="img/icon-{n}-128.webp 1x, img/icon-{n}-256.webp 2x"><img src="img/icon-{n}-128.png" srcset="img/icon-{n}-256.png 2x" alt="{alt}" width="128" height="128" loading="lazy"></picture>'
    body=f'''<section class="mhero"><div class="mesh" aria-hidden="true"></div><div class="wrap mgrid"><div class="mcopy"><span class="newpill"><b>New</b> Pathfinder · describe a game, get the steps</span>
<h1>Describe your game.<br><span class="grad">Get the path.</span></h1><p class="lead">Tools, step-by-step tutorials and videos for building any kind of game — for kids, teens and grown-ups.</p>
<div class="glass pfwrap">{PFFORM("","pathfinder/")}</div><p class="stats"><a href="tutorials/">{icon("book-open",16)} {len(json.load(open(ROOT/"data/tutorials.json")))} tutorials</a><a href="videos/">{icon("play",16)} {len(json.load(open(ROOT/"data/videos.json")))} videos</a><a href="#tools">{icon("search",16)} {len(tools)} tools</a></p></div>
<div class="mart">{pic("hero",[1280,960,640],"Clay-style illustration: a laptop showing a platformer, a floating castle island, a friendly robot, a VR headset and a tablet racing game","heroimg","(max-width:860px) 100vw, 640px",True)}<span class="float f1">{icon("sparkles",16)} AI prototypes</span><span class="float f2">{icon("gamepad-2",16)} Godot · Unity · Roblox</span></div></div></section>
<section class="how wrap"><span class="eyebrow">How it works</span><h2>Three steps from idea to played.</h2><div class="howrow">
<div class="hstep">{clay("ai")}<span class="hn">1</span><h3>Describe it</h3><p>Type your idea — “a cozy farming game”, “a Roblox obby”. Pathfinder picks tools that fit your age.</p></div>
<div class="hstep">{clay("engines")}<span class="hn">2</span><h3>Build it</h3><p>Follow the steps with a written tutorial and hand-picked videos. Copy an AI starter prompt if you like.</p></div>
<div class="hstep">{clay("publish")}<span class="hn">3</span><h3>Share it</h3><p>Publish to itch.io, Roblox or the web, show friends, and level up to your next game.</p></div></div></section>
<section class="wrap famband"><div class="famimg">{pic("parent-kid",[1280,640],"Clay-style illustration of a parent and child building a game together on a laptop","","(max-width:860px) 100vw, 560px")}</div><div><span class="eyebrow">Families &amp; classrooms</span><h2>Make a game together.</h2><p class="lead" style="font-size:1.1rem">Short sessions, the right first tool for each age, and safety notes for grown-ups. The kid drives — you cheer.</p><div class="cta"><a class="btn" href="tutorials/make-a-game-with-your-kid.html">{icon("book-open")} Parent playbook</a><a class="btn alt" href="for-kids/">{icon("star")} Best tools for kids</a></div></div></section>
<section class="sec band-who" id="who"><div class="wrap"><span class="eyebrow">Who's building?</span><h2>Pick your player.</h2><p class="mut" style="max-width:40em">Tell us who's making the game and we'll show tools that fit — with simple first steps.</p><div class="who">{"".join(f'<a class="whob" style="--c:{v[5]}" href="{v[2]}/">{ART["age-"+k].replace("<svg ","<svg class=\"wart\" ",1)}<span class="wlbl"><b>{v[4]}</b><small>Ages {v[1]} · {sum(k in t.get("ages",[]) for t in tools)} tools</small></span><span class="go">{icon("arrow-right",22)}</span></a>' for k,v in AGES.items())}</div></div></section>{WAVE("#fffaf2")}<section class="sec alt"><div class="wrap"><span class="eyebrow">Choose your toolbox</span><h2>Eight ways in.</h2><div class="bento">{tiles}</div></div></section>{WAVE("#fffaf2",True)}
<section class="sec band-color" style="--c:#ffe3a3"><div class="wrap"><span class="eyebrow">Staff picks</span><h2>Great places to start.</h2></div><div class="rail wrap" tabindex="0" aria-label="Featured tools">{feat}</div></section>
<section class="sec inkbg diag"><div class="wrap"><span class="eyebrow" style="color:var(--mustard)">Quests</span><h2>Follow a path, not a pile of tabs.</h2>{paths}</div></section>
<section class="sec"><div class="wrap">{ticket()}</div></section>
{WAVE("#fffaf2")}<section class="sec alt" id="tools"><div class="wrap"><span class="eyebrow">The directory</span><h2>All {len(tools)} tools.</h2>
<div class="controls" role="search" aria-label="Tool directory"><input id="q" type="search" placeholder="Search tools, makers, ideas…" aria-label="Search tools"><select id="fc" aria-label="Category"><option value="">All categories</option>{"".join(f'<option value="{k}">{n}</option>' for k,(n,_,_) in CATS.items())}</select>
<select id="fs" aria-label="Skill"><option value="">Any skill</option><option>beginner</option><option>intermediate</option><option>advanced</option></select><select id="fp" aria-label="Price"><option value="">Any price</option><option value="free">Free</option><option value="freemium">Free to start</option><option value="paid">Paid</option></select>
<select id="fa" aria-label="Age"><option value="">Any age</option>{"".join(f'<option value="{k}">{v[0]} ({v[1]})</option>' for k,v in AGES.items())}</select><select id="fpl" aria-label="Platform"><option value="">Any platform</option>{"".join(f"<option>{p}</option>" for p in plats)}</select><select id="so" aria-label="Sort"><option value="cat">By category</option><option value="name">A–Z</option><option value="skill">Easiest first</option></select></div>
<div class="dirbar"><p class="mut" id="cnt" role="status"></p><div class="seg" role="group" aria-label="View"><button id="vList" aria-pressed="true">{icon("book-open",16)} List</button><button id="vGrid" aria-pressed="false">{icon("blocks",16)} Cards</button></div></div><div id="list" class="dir list"></div><template id="heads">{"".join(f'<div data-k="{k}" class="ghead" style="--c:{c}">{ART[k].replace("<svg ","<svg class=\"gart\" ",1)}<div><span class="eyebrow" style="color:var(--ink)">{icon(i,14)} Category</span><h3>{n}</h3><a href="categories/{k}.html">See all {n.lower()} {icon("arrow-right",14)}</a></div><span class="gcount">00</span></div>' for k,(n,i,c) in CATS.items())}</template><template id="empty">{EMPTY}</template></div></section>{WAVE("#fffaf2",True)}
<section class="sec"><div class="wrap"><span class="eyebrow">Made with Claude</span><h2>Real games, real build logs.</h2><div class="stack">{shw}</div></div></section>
<section class="sec band-color" style="--c:#cdeee9"><div class="wrap"><span class="eyebrow">Fresh</span><h2>Recently added.</h2><div class="grid">{"".join(card(t) for t in newest)}</div></div></section>
<section class="sec"><div class="wrap">{NEWS}</div></section>
<script>const T={json.dumps([{"n":t["name"],"b":t["blurb"],"m":t["maker"],"c":t["category"],"s":t["skill"],"p":t["price"],"pl":t["platforms"],"a":t.get("ages",[]),"h":card(t)} for t in tools])};const $=i=>document.getElementById(i),SK={{beginner:0,intermediate:1,advanced:2}};
function r(){{const q=$("q").value.toLowerCase();let L=T.filter(t=>(!q||(t.n+t.b+t.m).toLowerCase().includes(q))&&(!$("fc").value||t.c==$("fc").value)&&(!$("fs").value||t.s==$("fs").value)&&(!$("fp").value||t.p==$("fp").value)&&(!$("fpl").value||t.pl.includes($("fpl").value))&&(!$("fa").value||t.a.includes($("fa").value)));
const s=$("so").value;L.sort((a,b)=>s=="skill"?SK[a.s]-SK[b.s]||a.n.localeCompare(b.n):s=="cat"?a.c.localeCompare(b.c)||a.n.localeCompare(b.n):a.n.localeCompare(b.n));
const H=$("heads").content;let out="";if(!L.length)out=$("empty").innerHTML;else{{const ks=[...new Set(L.map(t=>t.c))];if(s!="cat"&&s!="name")ks.length=0;
if(ks.length)ks.forEach(k=>{{const g=L.filter(t=>t.c==k),hd=H.querySelector(`[data-k="${{k}}"]`).cloneNode(true);hd.querySelector(".gcount").textContent=String(g.length).padStart(2,"0");out+=`<section class="group">${{hd.outerHTML}}<div class="items">${{g.map(t=>t.h).join("")}}</div></section>`}});else out=`<div class="items">${{L.map(t=>t.h).join("")}}</div>`}}$("list").innerHTML=out;$("cnt").textContent=L.length+" of "+T.length+" tools"}}["q","fc","fs","fp","fpl","fa","so"].forEach(i=>$(i).addEventListener("input",r));function V(m){{$("list").className="dir "+m;$("vList").setAttribute("aria-pressed",m=="list");$("vGrid").setAttribute("aria-pressed",m=="grid");try{{localStorage.v=m}}catch(e){{}}}}$("vList").onclick=()=>V("list");$("vGrid").onclick=()=>V("grid");try{{V(localStorage.v||"list")}}catch(e){{}}$("so").value="cat";r()</script>'''
    page("index.html",f"{SITE_NAME} — Tools, engines & AI for making games",f"Directory of {len(tools)} game-making tools: AI, engines, art, audio, no-code, VR and publishing, with beginner-to-advanced paths.",body,
         {"@context":"https://schema.org","@type":"WebSite","name":SITE_NAME,"url":BASE_URL+"/","description":TAGLINE},wide=True)
    for k,(n,i,c) in CATS.items():
        L=[t for t in tools if t["category"]==k]
        page(f"categories/{k}.html",f"{n} for making games — {SITE_NAME}",f"{len(L)} {n.lower()} tools for game developers, from beginner to advanced.",
             f'<div class="phead"><div><span class="eyebrow">{icon(i,14)} Category</span><h1>{n}</h1><p class="lead mut" style="font-size:1.15rem">{len(L)} tools, from first-timer friendly to pro-grade. Sorted easiest first.</p></div>{herovis(k)}</div>{CATX(k,L)}<div class="grid">{"".join(card(t,"../") for t in sorted([x for x in L if x not in CATTOP(L)],key=lambda t:("beginner","intermediate","advanced").index(t["skill"])))}</div>{ticket()}',
             {"@context":"https://schema.org","@type":"ItemList","name":n,"itemListElement":[{"@type":"ListItem","position":j+1,"url":f"{BASE_URL}/tools/{t['slug']}.html","name":t["name"]} for j,t in enumerate(L)]},[(n,None)],og=k)
    for t in tools:
        n,i,c=CATS[t["category"]];rel=[x for x in tools if x["category"]==t["category"] and x is not t][:3]
        cmp=[(a,b) for a,b in COMPARE if t["slug"] in (a,b)]
        body=f'''<div class="phead"><div><span class="eyebrow">{icon(i,14)} {n}</span><h1>{E(t["name"])}</h1><p style="font-size:1.2rem">{E(t["blurb"])}</p><p><a class="btn" href="{t["url"]}" rel="noopener">Official site {icon("arrow-right")}</a></p></div><div class="prodtile" style="--c:{c}">{clay2(CLAYMAP[t["category"]],cls="clay2 pt") if t["category"] in CLAYMAP else f'<span class="pinit">{E(t["name"][0])}</span>'}<b>{E(t["name"])}</b><small>{E(t["maker"])}</small><span class="pmeta"><span>{PL[t["price"]]}</span><span>{LL[t["license"]]}</span><span>{SK[t["skill"]]}</span></span></div></div>
{TJUMP(TOOL_JUMP)}<h2 id="overview" style="font-size:1.5rem">The facts</h2><table class="facts"><tr><th>Made by</th><td>{E(t["maker"])}</td></tr><tr><th>Skill level</th><td><span class="lvl {t["skill"]}">{SK[t["skill"]]}</span></td></tr><tr><th>Price</th><td>{PL[t["price"]]}</td></tr><tr><th>Code</th><td>{LL[t["license"]]}</td></tr><tr><th>Platforms</th><td>{", ".join(t["platforms"])}</td></tr><tr><th>Good for ages</th><td>{"".join(f'<a class="age a-{a}" href="../{AGES[a][2]}/">{AGES[a][0]} {AGES[a][1]}</a> ' for a in t.get("ages",[]))}{f'<div class="mut" style="margin-top:.4rem;font-size:.9rem">{E(t["age_note"])}</div>' if t.get("age_note") else ""}</td></tr></table>
{f'<div class="note">{icon("info")} {E(t["note"])}</div>' if t.get("note") else ""}<p class="mut" style="font-size:.85rem">Last verified: {LAST_VERIFIED}. Always confirm pricing on the official site.</p>
{"".join(f'<p>{icon("swords")} <a href="../compare/{a}-vs-{b}.html">{E(BY[a]["name"])} vs {E(BY[b]["name"])}</a></p>' for a,b in cmp)}{TOOLX(t)}{ticket()}<h2>More in {n}</h2><div class="grid">{"".join(card(x,"../") for x in rel)}</div>'''
        page(f"tools/{t['slug']}.html",(lambda x:x if len(x)<=65 else f"{t['name']} — {SITE_NAME}")(f"{t['name']} for making games — {SITE_NAME}"),f"{t['name']} by {t['maker']}: {t['blurb']}"[:158],body,
             {k2:v for k2,v in {"@context":"https://schema.org","@type":"SoftwareApplication","name":t["name"],"author":{"@type":"Organization","name":t["maker"]},"url":t["url"],"applicationCategory":n,"operatingSystem":", ".join(t["platforms"]),"description":t["blurb"],"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"} if t["price"]=="free" else None}.items() if v},[(n,f"categories/{t['category']}.html"),(t["name"],None)],og=t["category"])
    rows=[]
    for a,b in COMPARE:
        A,B=BY[a],BY[b];f=lambda k,v=lambda x:x:"".join(f"<td>{E(str(v(X[k])))}</td>" for X in (A,B))
        body=f'''<span class="eyebrow">{icon("swords",14)} Head to head</span><h1>{E(A["name"])} <span style="color:var(--tink)">vs</span> {E(B["name"])}</h1><p class="mut">A quick side-by-side to help you choose. Both are solid — the right pick depends on your goals.</p>
<div class="tablewrap" tabindex="0" role="region" aria-label="Comparison table"><table class="facts"><tr><th scope="col">Feature</th><th>{E(A["name"])}</th><th>{E(B["name"])}</th></tr><tr><th>Maker</th>{f("maker")}</tr><tr><th>Summary</th>{f("blurb")}</tr><tr><th>Skill</th>{f("skill",SK.get)}</tr><tr><th>Price</th>{f("price",PL.get)}</tr><tr><th>Code</th>{f("license",LL.get)}</tr><tr><th>Platforms</th>{f("platforms",", ".join)}</tr></table></div>
<div class="prose"><h2>Quick take</h2><p>Choose <b>{E(A["name"])}</b> if {"you want free, open-source tooling" if A["license"]=="open-source" else "its ecosystem fits your project"}; choose <b>{E(B["name"])}</b> if {"you want free, open-source tooling" if B["license"]=="open-source" else "its ecosystem fits your project"}. Beginners should favour whichever is marked Beginner. Always check the official sites for current pricing.</p>
{"".join(f'<div class="note"><b>{E(X["name"])}:</b> {E(X["note"])}</div>' for X in (A,B) if X.get("note"))}<p class="mut">Last verified: {LAST_VERIFIED}</p><p><a href="../tools/{a}.html">{E(A["name"])} details</a> · <a href="../tools/{b}.html">{E(B["name"])} details</a></p></div>{ticket()}'''
        page(f"compare/{a}-vs-{b}.html",(lambda x:x if len(x)<=65 else f"{A['name']} vs {B['name']}"+("" if len(A['name']+B['name'])>40 else f" — {SITE_NAME}"))(f"{A['name']} vs {B['name']} for making games — {SITE_NAME}"),f"Compare {A['name']} and {B['name']}: price, license, skill level and platforms.",body,None,[("Compare","compare.html"),(f"{A['name']} vs {B['name']}",None)],og="compare")
        rows.append(f'<article class="card" style="--c:{CATS[A["category"]][2]}"><div class="cat">{icon("swords",14)} Comparison</div><h3><a href="compare/{a}-vs-{b}.html">{E(A["name"])} vs {E(B["name"])}</a></h3></article>')
    page("compare.html",f"Game dev tool comparisons — {SITE_NAME}","Head-to-head comparisons of game engines, AI coding tools and art apps.",f'<span class="eyebrow">Head to head</span><h1>Comparisons</h1><div class="grid">{"".join(rows)}</div>',None,[("Compare",None)],og="compare")
    pl=[]
    for (s,ti,l,steps),c in zip(PATHS,[P["sky"],P["plum"],P["tomato"],P["leaf"]]):
        st="".join(f'<li><h3>{E(h)}</h3><p style="margin:.3rem 0 .6rem">{E(d)}</p>{" ".join(f"<a class=pill href=../tools/{x}.html>{E(BY[x]["name"])}</a>" for x in xs)}</li>' for h,d,xs in steps)
        page(f"paths/{s}.html",f"{ti} — {SITE_NAME}",f"Step-by-step path: {ti}. {SK[l]} level.",f'<div class="phead"><div><span class="eyebrow">{icon("map",14)} Learning path</span><h1>{E(ti)}</h1><span class="lvl {l}">{SK[l]}</span> <span class="mut">· {len(steps)} steps</span></div>{ART[s]}</div><ol class="steps">{st}</ol>{ticket()}',
             {"@context":"https://schema.org","@type":"HowTo","name":ti,"step":[{"@type":"HowToStep","name":h,"text":d} for h,d,_ in steps]},[("Paths","paths.html"),(ti,None)],og=s)
        pl.append(f'<div class="path" style="--c:{c}"><div class="pic">{ART[s]}</div><div><span class="lvl {l}">{SK[l]}</span><h3 style="font-size:1.8rem;margin:.7rem 0">{E(ti)}</h3><a class="btn alt" href="paths/{s}.html">Start {icon("arrow-right")}</a></div></div>')
    gl=[]
    for k,(ti,_,secs,rel) in GUIDES.items():
        page(f"guides/{k}.html",f"{ti} — {SITE_NAME}",f"{ti}: practical workflow for using AI to prototype and ship games.",f'<div class="phead"><div><span class="eyebrow">{icon("sparkles",14)} AI guide</span><h1>{E(ti)}</h1></div>{ART["ai"]}</div><div class="prose">{"".join(f"<h2>{E(h)}</h2><p>{E(d)}</p>" for h,d in secs)}</div><h2 style="margin-top:var(--s5)">Tools</h2><div class="grid">{"".join(card(BY[x],"../") for x in rel)}</div><p style="margin-top:var(--s4)"><a class="btn alt" href="../showcase.html">See real case studies {icon("arrow-right")}</a></p>',None,[("Paths","paths.html"),(ti,None)],og="ai")
        gl.append(f'<article class="card" style="--c:{P["plum"]}"><div class="cat">{icon("sparkles",14)} AI guide</div><h3><a href="guides/{k}.html">{E(ti)}</a></h3></article>')
    page("paths.html",f"Learning paths & guides — {SITE_NAME}","Step-by-step learning paths by skill level, plus guides to making games with Claude, ChatGPT and Codex.",f'<span class="eyebrow">Quests</span><h1>Learning paths</h1>{"".join(pl)}<h2>AI guides</h2><div class="grid">{"".join(gl)}</div>',None,[("Paths",None)],og="paths")
    def vid(s):
        if s.get("video"):return f'<div class="vid portrait"><video controls muted loop playsinline preload="metadata" {f"poster=\"{E(s.get("poster",""))}\"" if s.get("poster") else ""}><source src="{E(s["video"])}" type="video/mp4">Your browser does not support video.</video></div>'
        return ""
    sc="".join(f'''<article class="sc" id="{s["slug"]}"><span class="eyebrow">Case study · built with {", ".join(s["built_with"])}</span><h2>{E(s["title"])}</h2><p>{E(s["summary"])}</p><p><b>{E(s["status"])}</b></p>{vid(s)}
{f'<p><a class="btn" href="{E(s["play_url"])}" rel="noopener">{icon("play")} Play {E(s["title"])}</a> {f"<a class=\"btn alt\" href=\"{E(s["repo_url"])}\" rel=\"noopener\">Source repo</a>" if s.get("repo_url") else ""}</p>' if s.get("play_url") else '<div class="slot">'+icon("play")+' <span><b>Play:</b> link coming soon</span></div>'}{f'<div class="slot solid">{icon("gamepad-2")} <span><b>How it plays:</b> {E(s["how_it_plays"])}</span></div>' if s.get("how_it_plays") else ""}<div class="slot">{icon("sparkles")} <span><b>Prompts:</b> {E(s["prompts"]) or "coming soon"}</span></div><div class="slot">{icon("cog")} <span><b>Iterations:</b> {E(s["iterations"]) or "coming soon"}</span></div><div class="slot">{icon("blocks")} <span><b>Tools:</b> {E(s["tools"]) or "coming soon"}</span></div></article>''' for s in show)
    page("showcase.html",f"Made with Claude — game case studies — {SITE_NAME}","Real games built with Claude and other AI tools, with how they were made.",f'<div class="phead"><div><span class="eyebrow">Showcase</span><h1>Made with Claude</h1><p style="font-size:1.15rem">Case studies of real games built with AI help, starting with games by the site\'s owner, Brandon Mau. ChatGPT- and Codex-built games welcome too.</p><p><a href="guides/claude.html">Guide: Build games with Claude</a> · <a href="guides/chatgpt.html">Guide: ChatGPT &amp; Codex</a></p></div>{ART["showcase"]}</div><div class="stack">{sc}</div>',None,[("Showcase",None)],og="showcase")
    AGECOPY={
     "kids":("Make your first game — no experience needed.",["Start in Scratch: drag blocks to make a cat move, then add a score.","Draw your own hero in Krita or MagicaVoxel.","Make sound effects with one click in jsfxr.","Share with family first — then try Roblox Studio or GDevelop."],["scratch","microsoft-makecode-arcade","super-mario-maker-2","game-builder-garage","roblox-studio","gdevelop","bitsy","twine","magicavoxel","bfxr-jsfxr"]),
     "teens":("Level up from blocks to real engines.",["Pick Godot (free) or GameMaker for 2D.","Follow one free course start-to-finish (GDQuest or CS50).","Join a game jam — 48 hours, one small game.","Upload to itch.io with a parent's OK (publishing is 18+ or with guardian consent)."],["godot-engine","gamemaker","pico-8","roblox-studio","gdevelop","blender","aseprite","chatgpt","gdquest","cs50-s-intro-to-game-development","itch-io"]),
     "adults":("From weekend prototype to a real release.",["Prototype fast: vibe-code a playable HTML5 version with an AI coding agent.","Rebuild in a production engine (Godot, Unity or Unreal).","Lock in art and audio with clear licenses.","Ship: itch.io for feedback, Steam or app stores for launch."],["claude-code","cursor","godot-engine","unity","unreal-engine","blender","adobe-substance-3d-painter","fmod","steamworks","apple-app-store"])}
    PARENT=f'''<section class="parent" style="margin-top:var(--s5)"><h2>{icon("info")} A note for parents &amp; teachers</h2><ul>
<li><b>Accounts:</b> many tools need no account (Scratch to start, Bitsy, Twine, Krita, jsfxr). Scratch asks for a parent's email for under-13s; Roblox, Nintendo and Microsoft offer parent-managed accounts.</li>
<li><b>AI chatbots aren't for young kids:</b> ChatGPT and Grok require 13+ with parental permission; Claude and Cursor require 18+. For under-13s, an adult should drive any AI help.</li>
<li><b>Sharing &amp; chat:</b> turn on parental controls for online sharing and chat (Roblox, Super Mario Maker 2), and talk about not sharing personal info.</li>
<li><b>Money:</b> most picks here are free. Publishing on stores (itch.io, Steam, app stores) requires an adult or guardian consent.</li>
<li><b>Sit together:</b> the first session goes best side by side — let the kid drive the mouse.</li></ul><p class="mut" style="margin:0">Age info reflects official terms and ratings as of {LAST_VERIFIED}; always check the official site.</p></section>'''
    for k,(lab,rng,slug,_,_,col) in AGES.items():
        head,steps,picks=AGECOPY[k];picks=[BY[x] for x in picks if x in BY and k in BY[x].get("ages",[])]
        rest=[t for t in tools if k in t.get("ages",[]) and t not in picks]
        pick=f'<nav class="agepick" aria-label="Ages">{"".join(f'<a href="../{v[2]}/"{" aria-current=page" if kk==k else ""}>{v[0]} {v[1]}</a>' for kk,v in AGES.items())}</nav>'
        body=f'''{pick}<div class="phead"><div><span class="eyebrow">For {lab.lower()} · ages {rng}</span><h1>{head}</h1><p style="font-size:1.15rem">{len(picks)+len(rest)} tools that fit {lab.lower()} — picked for difficulty and each tool's official age rules.</p></div>{pic2("parent-kid",[1280,640],"Clay illustration of a parent and child building a game together") if k=="kids" else pic2("hero",[1280,960,640],"Clay illustration of a laptop with floating game worlds") if k=="teens" else cluster()}</div>
<h2>Your first steps</h2><ol class="steps-simple">{"".join(f"<li>{E(x)}</li>" for x in steps)}</ol>
<h2 style="margin-top:var(--s5)">Top picks</h2><div class="grid">{"".join(card(t,"../") for t in picks)}</div>
{PARENT if k=="kids" else ""}<h2 style="margin-top:var(--s5)">Everything else for {lab.lower()}</h2><div class="dir list"><div class="items">{"".join(card(t,"../") for t in rest)}</div></div>{ticket()}'''
        page(f"{slug}/index.html",f"Game-making tools for {lab.lower()} ({rng}) — {SITE_NAME}",f"The best tools for {lab.lower()} ages {rng} to make games, with simple first steps and age-rule notes.",body,
             {"@context":"https://schema.org","@type":"ItemList","name":f"Game-making tools for {lab.lower()}","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE_URL}/tools/{t['slug']}.html","name":t["name"]} for i,t in enumerate(picks)]},[(f"For {lab.lower()}",None)],og=f"age-{k}")
    page("about.html",f"About — {SITE_NAME}",f"About {SITE_NAME}: an independent, hand-checked directory of tools, tutorials and videos for making games.",f'<div class="phead"><div><span class="eyebrow">About</span><h1>Made by game makers, for game makers.</h1></div>{ART["learn"]}</div><div class="prose"><p>{SITE_NAME} is an independent directory of every way to make games — from prompting an AI to shipping with Unreal. Listings are written in our own words and link to official sites. Prices and features change; always confirm on the official site.</p><p>Last verified: {LAST_VERIFIED}. Last build: {TODAY}.</p><p>Illustrations and logo are original; fonts (Inter, Space Grotesk) are SIL OFL and icons are Lucide (ISC). See <a href="CREDITS.txt">credits</a>.</p></div>{ticket()}{NEWS}',None,[("About",None)],og="home")
    page("404.html",f"Page not found — {SITE_NAME}","This page doesn't exist. Head back to the BuildGames Hub homepage or Start here.",f'<div class="phead" style="margin-top:var(--s5)"><div><span class="hud">GAME OVER <i>·</i> 404</span><h1 style="margin-top:var(--s4)">This level hasn\'t been built yet.</h1><p class="mut">The page you\'re looking for moved or never existed.</p><p><a class="btn" href="{BASE_URL}/">{icon("arrow-right")} Respawn at home</a></p></div>{ART["kids"]}</div>')
    p404=OUT/"404.html";p404.write_text(p404.read_text().replace('href="style.css"',f'href="{BASE_URL}/style.css"').replace('href="favicon',f'href="{BASE_URL}/favicon').replace('href="fonts/',f'href="{BASE_URL}/fonts/').replace('url(fonts/',f'url({BASE_URL}/fonts/'))
    build_teach()
    (OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    (OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in URLS)+"</urlset>\n")
    L=[f"# {SITE_NAME}",f"> {TAGLINE} Directory of {len(tools)} tools for making games, organized by category and skill level.","",f"Full data: {BASE_URL}/data/tools.json",f"Last verified: {LAST_VERIFIED}",""]
    for k,(n,_,_) in CATS.items():
        L+=[f"## {n}"]+[f"- [{t['name']}]({BASE_URL}/tools/{t['slug']}.html): {t['blurb']} ({t['skill']}, {t['price']}, {t['license']}, ages: {'/'.join(AGES[a][0]+' '+AGES[a][1] for a in t.get('ages',[]))})" for t in tools if t["category"]==k]+[""]
    L+=["## Make a game (Pathfinder)",f"- [Pathfinder]({BASE_URL}/pathfinder/): describe a game in plain words; get an age-aware tool stack, steps with time estimates, a tutorial, videos and an AI starter prompt. Templates: "+", ".join(p["title"] for p in paths_t),""]
    L+=["## Tutorials"]+[f"- [{t['title']}]({BASE_URL}/tutorials/{t['slug']}.html): {t['summary']} ({t['time']})" for t in tuts]+[""]
    L+=["## Videos",f"- [Video library]({BASE_URL}/videos/): {len(vids)} verified YouTube tutorials from official channels and known teachers, tagged by tool, game type and age.",""]
    L+=["## By age"]+[f"- [{v[0]} {v[1]}]({BASE_URL}/{v[2]}/)" for v in AGES.values()]+[""]
    L+=["## Paths"]+[f"- [{t}]({BASE_URL}/paths/{s}.html)" for s,t,_,_ in PATHS]+["","## Guides"]+[f"- [{v[0]}]({BASE_URL}/guides/{k}.html)" for k,v in GUIDES.items()]+["","## Comparisons"]+[f"- {BASE_URL}/compare/{a}-vs-{b}.html" for a,b in COMPARE]+["",f"## Showcase\n- {BASE_URL}/showcase.html"]
    L+=["## Start & resources",f"- [Start here]({BASE_URL}/start.html): three simple paths for kids, teens and adults.",f"- [Free art]({BASE_URL}/resources/art.html)",f"- [Free sound & music]({BASE_URL}/resources/sound.html)",f"- [Glossary]({BASE_URL}/resources/glossary.html)",f"- [Beginner FAQ]({BASE_URL}/resources/faq.html)",f"- [Printable checklist]({BASE_URL}/resources/checklist.html)",f"- Build Buddy: an in-browser helper on every page; answers only from this site's data and sends nothing anywhere.",""]
    (OUT/"llms.txt").write_text("\n".join(L)+"\n")
    for d in ("data","_build"):shutil.copytree(ROOT/d,OUT/d,ignore=shutil.ignore_patterns("__pycache__"))
    print(f"Built {len(URLS)} pages, {len(tools)} tools -> {OUT}")
def make_og():
    """Render 1200x630 share images + icons with headless Chrome."""
    (ASSETS/"og").mkdir(exist_ok=True);tmp=ROOT/"_build/tmp";tmp.mkdir(exist_ok=True)
    fonts=(ASSETS/"fonts").as_uri()
    items={"home":("Every way to build a game.","hero"),"compare":("Head-to-head tool comparisons.","engine"),"paths":("Learning paths for game makers.","first-game-this-weekend"),"showcase":("Made with Claude: game case studies.","showcase")}
    items.update({k:(f"{n} for making games.",k) for k,(n,_,_) in CATS.items()})
    items.update({s:(t+".",s) for s,t,_,_ in PATHS})
    items.update({f"age-{k}":(f"Make games: tools for {v[0].lower()} {v[1]}.",f"age-{k}") for k,v in AGES.items()})
    def shot(name,htm,w,h):
        f=tmp/f"{name.replace('/','_')}.html";f.write_text(htm)
        subprocess.run(["google-chrome","--headless=new","--no-sandbox","--hide-scrollbars","--force-device-scale-factor=1",f"--window-size={w},{h}",f"--screenshot={ASSETS/name}.png",f.as_uri()],capture_output=True)
    base=f'<style>@font-face{{font-family:SG;src:url({fonts}/space-grotesk-latin-700-normal.woff2)}}@font-face{{font-family:I;src:url({fonts}/inter-latin-600-normal.woff2)}}body{{margin:0}}</style>'
    for k,(t,a) in items.items():
        shot(f"og/{k}",f'{base}<div style="width:1200px;height:630px;background:{CREAM};display:grid;grid-template-columns:1fr 520px;align-items:center;gap:40px;padding:0 60px;box-sizing:border-box;font-family:I;color:{INK};border:14px solid {INK}"><div><div style="display:flex;align-items:center;gap:14px;font:700 36px SG">{logo(56)}BuildGames<span style="color:{P["tomato"]}">Hub</span></div><div style="font:700 66px/1.05 SG;margin-top:36px;letter-spacing:-1px">{E(t)}</div><div style="margin-top:28px;font-size:24px;opacity:.7">bmau37.github.io/buildgames-hub</div></div><div style="border:5px solid {INK};border-radius:28px;overflow:hidden;box-shadow:12px 12px 0 {INK};transform:rotate(2deg);height:325px">{ART[a].replace("<svg ","<svg width=\"520\" height=\"325\" ",1)}</div></div>',1200,630)
    shot("apple-touch-icon",f'{base}<div style="width:180px;height:180px;background:{CREAM};display:grid;place-items:center">{logo(140)}</div>',180,180)
    shot("favicon-32",f'{base}<div style="width:32px;height:32px;display:grid;place-items:center">{logo(32)}</div>',32,32)
    shutil.rmtree(tmp);print("OG images:",len(items))
if "--og" in sys.argv or not (ASSETS/"og").exists():make_og()
build()
