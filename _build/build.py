#!/usr/bin/env python3
"""Static site generator. Edit data/*.json then run: python3 _build/build.py"""
import json, os, shutil, html, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"dist"
# ---- CONFIG (single spot) ----
SITE_NAME="BuildGames Hub"
TAGLINE="Every way to build a game — from AI prompts to Unreal."
BASE_URL="https://bmau37.github.io/buildgames-hub"
SPONSOR_EMAIL="sponsor@example.com"  # placeholder
# ------------------------------
E=html.escape
TODAY=datetime.date.today().isoformat()
tools=json.load(open(ROOT/"data/tools.json"))
show=json.load(open(ROOT/"data/showcase.json"))
BY={t["slug"]:t for t in tools}
CATS={"ai":("AI & Vibe Coding","🤖","#a855f7"),"engine":("Game Engines","⚙️","#3b82f6"),"art":("3D & Art","🎨","#f97316"),
"audio":("Audio & Music","🎵","#14b8a6"),"kids":("No-code & Kids","🧸","#eab308"),"vr":("VR / Quest","🥽","#ec4899"),
"publish":("Publishing","🚀","#22c55e"),"learn":("Learning","📚","#64748b")}
SK={"beginner":"🟢 Beginner","intermediate":"🟡 Intermediate","advanced":"🔴 Advanced"}
COMPARE=[("godot-engine","unity"),("unity","unreal-engine"),("godot-engine","unreal-engine"),("gamemaker","godot-engine"),
("construct-3","gdevelop"),("claude-code","cursor"),("claude","chatgpt"),("blender","adobe-substance-3d-painter"),
("roblox-studio","uefn-unreal-editor-for-fortnite"),("phaser","defold"),("itch-io","steamworks"),("scratch","microsoft-makecode-arcade")]
PATHS=[("first-game-this-weekend","Make your first game this weekend","beginner",
 [("Pick a tiny idea","One mechanic, one screen. Think Pong, Flappy, or a 3-room text adventure.",["twine","bitsy"]),
  ("Choose a friendly tool","Godot or GDevelop for 2D; PICO-8 if you love limits.",["godot-engine","gdevelop","pico-8"]),
  ("Grab free assets","Use CC0 art and generated sound effects so you can focus on play.",["kenney-assets","bfxr-jsfxr"]),
  ("Ask AI when stuck","Paste errors into an assistant and ask it to explain, not just fix.",["claude","chatgpt"]),
  ("Ship it","Upload a web build to itch.io and share the link.",["itch-io"])]),
("vibe-coded-to-steam","From vibe-coded to Steam","intermediate",
 [("Prototype with an AI agent","Describe the core loop and let an agent scaffold a playable HTML5 or Godot prototype.",["claude-code","openai-codex","cursor"]),
  ("Playtest on the web","Host jam builds for friends to try.",["github-pages","itch-io"]),
  ("Move to a real engine","Rebuild or port into an engine with export targets and proper tooling.",["godot-engine","unity"]),
  ("Replace placeholder assets","Swap AI placeholders for consistent art and audio; check licenses.",["aseprite","blender","fmod"]),
  ("Publish","Set up a Steam page early to gather wishlists.",["steamworks"])]),
("blender-to-godot-3d","Blender to Godot 3D pipeline","intermediate",
 [("Model & UV","Model low-poly assets and unwrap them.",["blender"]),
  ("Texture","Paint PBR textures or use simple palettes.",["adobe-substance-3d-painter","krita"]),
  ("Export glTF","Export .glb from Blender — Godot imports it natively.",["blender"]),
  ("Build the scene","Import, add collisions and scripts in GDScript.",["godot-engine"]),
  ("Learn more","Follow Godot-focused courses.",["gdquest"])]),
("kids-game-making","Kids game-making","beginner",
 [("Start with blocks","Drag-and-drop coding with instant results.",["scratch","microsoft-makecode-arcade"]),
  ("Level design on console","Build and share levels.",["super-mario-maker-2","game-builder-garage"]),
  ("Worlds with friends","Create in platforms kids already play (with parental controls).",["roblox-studio","minecraft-education"]),
  ("Graduate to text code","Move to a real engine when ready.",["godot-engine"])])]
GUIDES={"claude":("Build games with Claude","claude",[
 ("Chat + Artifacts","In the Claude app, ask for a small browser game (e.g. 'a single-file HTML canvas Snake game') and Claude can render it as a live Artifact you can play and iterate on."),
 ("Claude Code for real projects","Claude Code runs in your terminal, reads your project, edits multiple files and runs commands — useful for Godot, Phaser or Unity projects under version control."),
 ("Iterate in small steps","Ask for one feature at a time, playtest, then describe what felt wrong. Keep the game in git so you can roll back."),
 ("Ask for explanations","Have Claude explain generated code so you can maintain it yourself."),
 ("Check your assets","AI can write code quickly; art, music and fonts still need clear licenses before you ship.")],["claude","claude-code","cursor"]),
"chatgpt":("Build games with ChatGPT & Codex","chatgpt",[
 ("ChatGPT for design & code","Use ChatGPT to brainstorm mechanics, write scripts and debug error messages; Canvas lets you edit and preview code side by side."),
 ("Codex for repositories","OpenAI Codex is a coding agent that can work on tasks in your repository — implementing features, fixing bugs and proposing changes for review."),
 ("Prototype in HTML5 first","A single HTML file with canvas is the fastest loop: generate, open in a browser, tweak."),
 ("Keep a design doc","Paste a short design doc at the start of new sessions so the model keeps context."),
 ("Review everything","Run and read the code; AI output can contain bugs or outdated APIs.")],["chatgpt","openai-codex","github-copilot"])}
CSS=""":root{--bg:#0d0b1e;--card:#1a1638;--ink:#f1f0ff;--mut:#a9a6c9;--acc:#facc15}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--ink);line-height:1.55}
a{color:#93c5fd}header{position:sticky;top:0;z-index:5;background:#0d0b1ecc;backdrop-filter:blur(8px);border-bottom:2px solid #2a2555}
nav{max-width:1100px;margin:auto;display:flex;gap:14px;align-items:center;padding:10px 16px;flex-wrap:wrap}
nav a{color:var(--ink);text-decoration:none;font-weight:600;font-size:.95rem}.logo{font-weight:900;font-size:1.2rem;color:var(--acc)!important;margin-right:auto}
main{max-width:1100px;margin:auto;padding:16px}h1{font-size:clamp(1.8rem,6vw,3rem);line-height:1.1;margin:.4em 0}
.hero{padding:28px 0;text-align:center}.hero h1 span{background:linear-gradient(90deg,#facc15,#f472b6,#60a5fa);-webkit-background-clip:text;color:transparent}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.card{background:var(--card);border-radius:16px;padding:16px;border-top:6px solid var(--c,#888);box-shadow:0 6px 0 #00000055;transition:transform .15s;display:flex;flex-direction:column;gap:6px}
.card:hover{transform:translateY(-4px) rotate(-.4deg)}.card h3{margin:0;font-size:1.1rem}.card h3 a{color:var(--ink);text-decoration:none}
.pill{display:inline-block;font-size:.75rem;padding:2px 8px;border-radius:99px;background:#ffffff14;margin:2px 4px 2px 0}
.mut{color:var(--mut)}.btn{display:inline-block;background:var(--acc);color:#111;font-weight:800;padding:10px 16px;border-radius:12px;text-decoration:none;border:0;box-shadow:0 4px 0 #a16207;cursor:pointer}
.controls{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.controls input,.controls select{background:var(--card);color:var(--ink);border:2px solid #2a2555;border-radius:10px;padding:10px;font-size:1rem;flex:1 1 150px}
.sponsor{border:3px dashed var(--acc);border-radius:16px;padding:16px;text-align:center;margin:20px 0;background:#facc1510}
.box{background:var(--card);border-radius:16px;padding:18px;margin:20px 0}section{margin:30px 0}
.cats{display:flex;flex-wrap:wrap;gap:8px}.cats a{background:var(--c);color:#fff;padding:8px 12px;border-radius:12px;text-decoration:none;font-weight:700}
table{width:100%;border-collapse:collapse}td,th{padding:8px;border-bottom:1px solid #2a2555;text-align:left;vertical-align:top}
footer{text-align:center;padding:30px;color:var(--mut);font-size:.9rem}ol.steps li{margin:10px 0}
.slot{border:2px dashed #555;border-radius:10px;padding:10px;margin:6px 0;color:var(--mut)}"""
def page(path,title,desc,body,ld=None,depth=0):
    pre="../"*depth
    canon=BASE_URL+"/"+path.replace("index.html","")
    nav="".join(f'<a href="{pre}{h}">{t}</a>' for h,t in [("index.html#tools","Tools"),("paths.html","Paths"),("compare.html","Compare"),("showcase.html","Showcase"),("about.html","About")])
    ldj=f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    s=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canon}">
<link rel="stylesheet" href="{pre}style.css">{ldj}</head><body><header><nav><a class="logo" href="{pre}index.html">🧱 {SITE_NAME}</a>{nav}</nav></header>
<main>{body}</main><footer>{SITE_NAME} · {TAGLINE}<br>Independent directory. Names and trademarks belong to their owners. · <a href="{pre}llms.txt">llms.txt</a> · <a href="{pre}sitemap.xml">sitemap</a></footer></body></html>"""
    p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s);URLS.append(canon)
def card(t,pre=""):
    n,ic,c=CATS[t["category"]]
    return f'''<div class="card" style="--c:{c}"><div>{ic} <span class="mut">{n}</span></div><h3><a href="{pre}tools/{t["slug"]}.html">{E(t["name"])}</a></h3>
<div class="mut" style="font-size:.85rem">{E(t["maker"])}</div><p style="margin:0">{E(t["blurb"])}</p><div><span class="pill">{SK[t["skill"]]}</span><span class="pill">💲 {t["price"]}</span><span class="pill">📜 {t["license"]}</span></div></div>'''
SPON=f'<div class="sponsor"><b>⭐ Your tool here — sponsor {SITE_NAME}</b><br><span class="mut">Reach people who are actively building games.</span><br><br><a class="btn" href="mailto:{SPONSOR_EMAIL}?subject=Sponsorship%20inquiry">Become a sponsor</a></div>'
NEWS='<div class="box"><h2>📬 Weekly build log <span class="pill">coming soon</span></h2><p class="mut">New tools, AI workflows and tutorials for game makers. Newsletter not live yet — this form is a demo and sends nothing.</p><form onsubmit="event.preventDefault();this.querySelector(\'p\').hidden=false"><div class="controls"><input type="email" required placeholder="you@example.com" aria-label="Email"><button class="btn">Notify me</button></div><p hidden>Thanks! (Demo only — nothing was sent or stored.)</p></form></div>'
def build():
    global URLS;URLS=[]
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir();(OUT/"style.css").write_text(CSS);(OUT/".nojekyll").write_text("")
    cats="".join(f'<a style="--c:{c}" href="categories/{k}.html">{i} {n}</a>' for k,(n,i,c) in CATS.items())
    plats=sorted({p for t in tools for p in t["platforms"]})
    newest=sorted(tools,key=lambda t:t["added"],reverse=True)[:6]
    shw="".join(f'<div class="card" style="--c:#f472b6"><h3>{E(s["title"])}</h3><div><span class="pill">Built with {", ".join(s["built_with"])}</span></div><p class="mut">{E(s["status"])}</p><a href="showcase.html#{s["slug"]}">View →</a></div>' for s in show)
    body=f'''<div class="hero"><h1>Build games <span>your way</span></h1><p class="mut">{len(tools)} hand-picked tools for making games — AI assistants, engines, art, audio, no-code, VR and publishing — sorted by skill level.</p><div class="cats">{cats}</div></div>
<section id="paths"><h2>🗺️ Pick a path</h2><div class="grid">{"".join(f'<div class="card" style="--c:#facc15"><h3><a href="paths/{s}.html">{t}</a></h3><span class="pill">{SK[l]}</span></div>' for s,t,l,_ in PATHS)}</div></section>
{SPON}
<section id="tools"><h2>🧰 Tool directory</h2><div class="controls"><input id="q" placeholder="Search tools…" aria-label="Search"><select id="fc"><option value="">All categories</option>{"".join(f'<option value="{k}">{n}</option>' for k,(n,_,_) in CATS.items())}</select>
<select id="fs"><option value="">Any skill</option><option>beginner</option><option>intermediate</option><option>advanced</option></select><select id="fp"><option value="">Any price</option><option>free</option><option>freemium</option><option>paid</option></select>
<select id="fpl"><option value="">Any platform</option>{"".join(f"<option>{p}</option>" for p in plats)}</select><select id="so"><option value="name">Sort: A–Z</option><option value="skill">Sort: easiest first</option><option value="cat">Sort: category</option></select></div>
<p class="mut" id="cnt"></p><div class="grid" id="list"></div></section>
<section><h2>🎮 Made with Claude — showcase</h2><div class="grid">{shw}</div></section>
<section><h2>🆕 Recently added</h2><div class="grid">{"".join(card(t) for t in newest)}</div></section>
{NEWS}
<script>const T={json.dumps([dict(t,html=card(t)) for t in tools])};const $=i=>document.getElementById(i),SK={{beginner:0,intermediate:1,advanced:2}};
function r(){{let q=$("q").value.toLowerCase(),L=T.filter(t=>(!q||(t.name+t.blurb+t.maker).toLowerCase().includes(q))&&(!$("fc").value||t.category==$("fc").value)&&(!$("fs").value||t.skill==$("fs").value)&&(!$("fp").value||t.price==$("fp").value)&&(!$("fpl").value||t.platforms.includes($("fpl").value)));
let s=$("so").value;L.sort((a,b)=>s=="skill"?SK[a.skill]-SK[b.skill]||a.name.localeCompare(b.name):s=="cat"?a.category.localeCompare(b.category):a.name.localeCompare(b.name));
$("list").innerHTML=L.map(t=>t.html).join("");$("cnt").textContent=L.length+" tools"}}["q","fc","fs","fp","fpl","so"].forEach(i=>$(i).addEventListener("input",r));r()</script>'''
    page("index.html",f"{SITE_NAME} — Tools, engines & AI for making games",f"Directory of {len(tools)} game-making tools: AI, engines, art, audio, no-code, VR and publishing, with beginner-to-advanced paths.",body,
         {"@context":"https://schema.org","@type":"WebSite","name":SITE_NAME,"url":BASE_URL+"/","description":TAGLINE})
    for k,(n,i,c) in CATS.items():
        L=[t for t in tools if t["category"]==k]
        page(f"categories/{k}.html",f"{n} for making games — {SITE_NAME}",f"{len(L)} {n.lower()} tools for game developers, from beginner to advanced.",f'<h1>{i} {n}</h1><div class="grid">{"".join(card(t,"../") for t in L)}</div>{SPON}',
             {"@context":"https://schema.org","@type":"ItemList","name":n,"itemListElement":[{"@type":"ListItem","position":j+1,"url":f"{BASE_URL}/tools/{t['slug']}.html","name":t["name"]} for j,t in enumerate(L)]},1)
    for t in tools:
        n,i,c=CATS[t["category"]];rel=[x for x in tools if x["category"]==t["category"] and x is not t][:3]
        cmp=[(a,b) for a,b in COMPARE if t["slug"] in (a,b)]
        body=f'''<p><a href="../categories/{t["category"]}.html">{i} {n}</a></p><h1>{E(t["name"])}</h1><p style="font-size:1.15rem">{E(t["blurb"])}</p>
<table><tr><th>Made by</th><td>{E(t["maker"])}</td></tr><tr><th>Skill level</th><td>{SK[t["skill"]]}</td></tr><tr><th>Price</th><td>{t["price"]}</td></tr><tr><th>License</th><td>{t["license"]}</td></tr><tr><th>Platforms</th><td>{", ".join(t["platforms"])}</td></tr></table>
<p><a class="btn" href="{t["url"]}" rel="noopener">Official site ↗</a></p>{"".join(f'<p>⚔️ <a href="../compare/{a}-vs-{b}.html">{BY[a]["name"]} vs {BY[b]["name"]}</a></p>' for a,b in cmp)}{SPON}<h2>Related</h2><div class="grid">{"".join(card(x,"../") for x in rel)}</div>'''
        page(f"tools/{t['slug']}.html",f"{t['name']} for game development — {SITE_NAME}",f"{t['name']} by {t['maker']}: {t['blurb']}"[:158],body,
             {"@context":"https://schema.org","@type":"SoftwareApplication","name":t["name"],"author":{"@type":"Organization","name":t["maker"]},"url":t["url"],"applicationCategory":n,"operatingSystem":", ".join(t["platforms"]),"description":t["blurb"],"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"} if t["price"]!="paid" else None},1)
    rows=[]
    for a,b in COMPARE:
        A,B=BY[a],BY[b];f=lambda k,v=lambda x:x:"".join(f"<td>{E(str(v(X[k])))}</td>" for X in (A,B))
        body=f'''<h1>{E(A["name"])} vs {E(B["name"])}</h1><p class="mut">A quick side-by-side to help you choose. Both are solid — the right pick depends on your goals.</p>
<table><tr><th></th><th>{E(A["name"])}</th><th>{E(B["name"])}</th></tr><tr><th>Maker</th>{f("maker")}</tr><tr><th>Summary</th>{f("blurb")}</tr><tr><th>Skill</th>{f("skill")}</tr><tr><th>Price</th>{f("price")}</tr><tr><th>License</th>{f("license")}</tr><tr><th>Platforms</th>{f("platforms",", ".join)}</tr></table>
<h2>Quick take</h2><p>Choose <b>{E(A["name"])}</b> if {"you want free, open-source tooling" if A["license"]=="open-source" else "its ecosystem fits your project"}; choose <b>{E(B["name"])}</b> if {"you want free, open-source tooling" if B["license"]=="open-source" else "its ecosystem fits your project"}. Beginners should favour the tool marked 🟢. Always check the official sites for current pricing.</p>
<p><a href="../tools/{a}.html">{E(A["name"])} details</a> · <a href="../tools/{b}.html">{E(B["name"])} details</a></p>{SPON}'''
        page(f"compare/{a}-vs-{b}.html",f"{A['name']} vs {B['name']} for making games — {SITE_NAME}",f"Compare {A['name']} and {B['name']}: price, license, skill level and platforms.",body,None,1)
        rows.append(f'<li><a href="compare/{a}-vs-{b}.html">{E(A["name"])} vs {E(B["name"])}</a></li>')
    page("compare.html",f"Game dev tool comparisons — {SITE_NAME}","Head-to-head comparisons of game engines, AI coding tools and art apps.",f"<h1>⚔️ Comparisons</h1><ul>{''.join(rows)}</ul>")
    pl=[]
    for s,ti,l,steps in PATHS:
        st="".join(f'<li><b>{E(h)}</b> — {E(d)}<br>{" ".join(f"<a class=pill href=../tools/{x}.html>{E(BY[x]["name"])}</a>" for x in xs)}</li>' for h,d,xs in steps)
        page(f"paths/{s}.html",f"{ti} — {SITE_NAME}",f"Step-by-step path: {ti}. {SK[l][2:]} level.",f'<h1>{E(ti)}</h1><span class="pill">{SK[l]}</span><ol class="steps">{st}</ol>{SPON}',
             {"@context":"https://schema.org","@type":"HowTo","name":ti,"step":[{"@type":"HowToStep","name":h,"text":d} for h,d,_ in steps]},1)
        pl.append(f'<div class="card" style="--c:#facc15"><h3><a href="paths/{s}.html">{E(ti)}</a></h3><span class="pill">{SK[l]}</span></div>')
    gl=[]
    for k,(ti,_,secs,rel) in GUIDES.items():
        page(f"guides/{k}.html",f"{ti} — {SITE_NAME}",f"{ti}: practical workflow for using AI to prototype and ship games.",f'<h1>{E(ti)}</h1>{"".join(f"<h2>{E(h)}</h2><p>{E(d)}</p>" for h,d in secs)}<h2>Tools</h2><div class="grid">{"".join(card(BY[x],"../") for x in rel)}</div><p><a href="../showcase.html">See real case studies →</a></p>',None,1)
        gl.append(f'<div class="card" style="--c:#a855f7"><h3><a href="guides/{k}.html">{E(ti)}</a></h3></div>')
    page("paths.html",f"Learning paths & guides — {SITE_NAME}","Skill-level paths and AI game-dev guides.",f'<h1>🗺️ Paths</h1><div class="grid">{"".join(pl)}</div><h1>🤖 AI guides</h1><div class="grid">{"".join(gl)}</div>')
    sc="".join(f'''<div class="box" id="{s["slug"]}"><h2>{E(s["title"])} <span class="pill">Built with {", ".join(s["built_with"])}</span></h2><p>{E(s["summary"])}</p><p><b>{E(s["status"])}</b></p>
<div class="slot">▶️ Play: {f'<a href="{E(s["play_url"])}">Play now</a>' if s["play_url"] else "link coming soon"}</div><div class="slot">💬 Prompts: {E(s["prompts"]) or "coming soon"}</div><div class="slot">🔁 Iterations: {E(s["iterations"]) or "coming soon"}</div><div class="slot">🧰 Tools: {E(s["tools"]) or "coming soon"}</div></div>''' for s in show)
    page("showcase.html",f"Made with Claude — game case studies — {SITE_NAME}","Real games built with Claude and other AI tools, with how they were made.",f'<h1>🎮 Made with Claude</h1><p class="mut">Case studies of real games built with AI help, starting with games by the site\'s owner, Brandon Mau. ChatGPT/Codex-built games welcome too.</p>{sc}<p><a href="guides/claude.html">Guide: Build games with Claude</a> · <a href="guides/chatgpt.html">Guide: ChatGPT & Codex</a></p>')
    page("about.html",f"About — {SITE_NAME}",f"About {SITE_NAME}.",f'<h1>About</h1><p>{SITE_NAME} is an independent directory of every way to make games — from prompting an AI to shipping with Unreal. Listings are written in our own words and link to official sites. Prices and features change; always confirm on the official site.</p><p>Updated regularly. Last build: {TODAY}.</p>{SPON}{NEWS}')
    (OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
    (OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in URLS)+"</urlset>\n")
    L=[f"# {SITE_NAME}",f"> {TAGLINE} Directory of {len(tools)} tools for making games, organized by category and skill level.","",f"Full data: {BASE_URL}/data/tools.json",""]
    for k,(n,_,_) in CATS.items():
        L+=[f"## {n}"]+[f"- [{t['name']}]({BASE_URL}/tools/{t['slug']}.html): {t['blurb']} ({t['skill']}, {t['price']}, {t['license']})" for t in tools if t["category"]==k]+[""]
    L+=["## Paths"]+[f"- [{t}]({BASE_URL}/paths/{s}.html)" for s,t,_,_ in PATHS]+["","## Comparisons"]+[f"- {BASE_URL}/compare/{a}-vs-{b}.html" for a,b in COMPARE]
    (OUT/"llms.txt").write_text("\n".join(L)+"\n")
    for d in ("data","_build"):shutil.copytree(ROOT/d,OUT/d,ignore=shutil.ignore_patterns("__pycache__"))
    print(f"Built {len(URLS)} pages, {len(tools)} tools -> {OUT}")
build()
