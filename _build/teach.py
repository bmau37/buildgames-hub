# Teaching pages: Pathfinder, Tutorials, Videos. exec'd inside build.py's namespace.
paths_t=json.load(open(ROOT/"data/paths.json")); tuts=json.load(open(ROOT/"data/tutorials.json")); vids=json.load(open(ROOT/"data/videos.json"))
TUT={t["slug"]:t for t in tuts}; VID={v["id"]:v for v in vids}
def md(src):
    out=[];lines=src.split("\n");i=0;para=[]
    def inl(s):
        s=E(s);s=re.sub(r"\*\*(.+?)\*\*",r"<b>\1</b>",s);s=re.sub(r"\*(.+?)\*",r"<i>\1</i>",s);return re.sub(r"`([^`]+)`",r"<code>\1</code>",s)
    def flush():
        if para:out.append("<p>"+inl(" ".join(para))+"</p>");para.clear()
    while i<len(lines):
        l=lines[i]
        if l.startswith("```"):
            flush();lang=l[3:].strip();j=i+1;buf=[]
            while not lines[j].startswith("```"):buf.append(lines[j]);j+=1
            out.append(f'<div class="code"><span class="lang">{E(lang or "code")}</span><button class="copy" type="button">Copy</button><pre><code>{E(chr(10).join(buf))}</code></pre></div>');i=j+1;continue
        if l.startswith("## "):flush();out.append(f'<h2 id="{re.sub(r"[^a-z0-9]+","-",l[3:].lower()).strip("-")}">{inl(l[3:])}</h2>')
        elif l.startswith("- "):
            flush();items=[]
            while i<len(lines) and lines[i].startswith("- "):items.append(f"<li>{inl(lines[i][2:])}</li>");i+=1
            out.append("<ul>"+"".join(items)+"</ul>");continue
        elif l.startswith("> "):flush();out.append(f'<div class="note">{inl(l[2:])}</div>')
        elif not l.strip():flush()
        else:para.append(l)
        i+=1
    flush();return "".join(out)
def agechips(ages,pre=""):return "".join(f'<span class="age a-{a}">{AGES[a][0]} {AGES[a][1]}</span>' for a in ages)
def vcard(v,pre=""):
    tool=next((BY[x] for x in v.get("tools",[]) if x in BY),None);c=CATS[tool["category"]][2] if tool else P["plum"]
    return f'''<article class="vcard" style="--c:{c}" data-types="{" ".join(v["types"])}" data-tools="{" ".join(v.get("tools",[]))}" data-ages="{" ".join(v["ages"])}"><button class="yt" type="button" data-id="{v["id"]}" aria-label="Play video: {E(v["title"])}"><span class="ytbg">{icon("play",34)}</span><span class="ytlen">{E(v.get("length") or "")}</span><span class="ytnote">Click to load from YouTube</span></button>
<div class="vb"><h3>{E(v["title"])}</h3><p class="mut">{E(v["channel"])}</p><div class="meta">{agechips(v["ages"])}{"".join(f'<a class="pill" href="{pre}tools/{x}.html">{E(BY[x]["name"])}</a>' for x in v.get("tools",[]) if x in BY)}</div><a class="ext" href="{v["url"]}" rel="noopener">Watch on YouTube ↗</a></div></article>'''
YTJS='''<script>document.addEventListener("click",e=>{const b=e.target.closest(".yt");if(b){const f=document.createElement("iframe");f.src="https://www.youtube-nocookie.com/embed/"+b.dataset.id+"?autoplay=1&rel=0";f.title=b.getAttribute("aria-label");f.allow="autoplay; encrypted-media; picture-in-picture; fullscreen";f.allowFullscreen=true;f.loading="lazy";b.replaceWith(f)}const c=e.target.closest(".copy");if(c){const t=c.parentElement.querySelector("pre,textarea");navigator.clipboard.writeText(t.value||t.innerText).then(()=>{c.textContent="Copied!";setTimeout(()=>c.textContent="Copy",1500)})}});</script>'''
TCSS=""".vgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:var(--s4)}}
.vcard{{background:#fff;border:3.5px solid var(--ink);border-radius:22px;overflow:hidden;box-shadow:var(--sh);display:flex;flex-direction:column;transition:transform .16s}}.vcard:hover{{transform:translateY(-4px)}}
.vcard iframe,.yt{{display:block;width:100%;aspect-ratio:16/9;border:0;border-bottom:3.5px solid var(--ink)}}
.yt{{position:relative;cursor:pointer;background:var(--c) repeating-linear-gradient(45deg,#ffffff22 0 10px,transparent 10px 20px);color:var(--ink);font:inherit}}
.ytbg{{position:absolute;left:50%;top:50%;translate:-50% -50%;width:74px;height:74px;border-radius:50%;background:#fff;border:3.5px solid var(--ink);display:grid;place-items:center;box-shadow:4px 4px 0 var(--ink);transition:transform .15s}}.yt:hover .ytbg{{transform:scale(1.1) rotate(-6deg)}}
.ytlen{{position:absolute;right:10px;bottom:10px;background:var(--ink);color:#fff;font:700 .75rem ui-monospace,monospace;padding:.2rem .45rem;border-radius:6px}}.ytnote{{position:absolute;left:10px;bottom:10px;font-size:.72rem;font-weight:600;background:#fff;border:2px solid var(--ink);border-radius:6px;padding:.1rem .4rem}}
.vb{{padding:1rem 1.1rem 1.2rem;display:flex;flex-direction:column;gap:.35rem;flex:1}}.vb h3{{font-size:1.02rem;line-height:1.25}}.vb p{{margin:0;font-size:.9rem}}.ext{{margin-top:auto;font-size:.85rem;font-weight:600}}
.code{{position:relative;margin:var(--s3) 0}}.code pre{{background:var(--ink);color:#f6efe3;border:3.5px solid var(--ink);border-radius:16px;padding:2.2rem 1.1rem 1rem;overflow-x:auto;font:400 .88rem/1.55 ui-monospace,Menlo,monospace;box-shadow:var(--sh);margin:0}}
.code .lang{{position:absolute;left:12px;top:8px;font:700 .7rem ui-monospace,monospace;color:var(--mustard);text-transform:uppercase}}.copy{{position:absolute;right:10px;top:8px;font:700 .75rem Inter;background:var(--mustard);border:2px solid var(--ink);border-radius:8px;padding:.25rem .6rem;cursor:pointer}}
code{{background:#1b16300f;padding:.05rem .3rem;border-radius:5px;font-size:.92em}}pre code{{background:none;padding:0}}
.tutmeta{{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:var(--s3) 0}}.tutlayout{{display:grid;grid-template-columns:1fr 300px;gap:var(--s5);align-items:start}}
.side{{position:sticky;top:90px;display:flex;flex-direction:column;gap:var(--s3)}}.side .box2{{background:#fff;border:3.5px solid var(--ink);border-radius:20px;padding:1rem 1.2rem;box-shadow:var(--sh)}}.side h3{{font-size:1rem;margin-bottom:.5rem}}
.check{{list-style:none;padding:0;margin:0}}.check li{{display:flex;gap:.5rem;padding:.3rem 0}}.check input{{width:20px;height:20px;accent-color:var(--teal);flex:none;margin-top:2px}}
.tcards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:var(--s4)}}.tcard{{position:relative;background:#fff;border:3.5px solid var(--ink);border-radius:24px;box-shadow:var(--sh);overflow:hidden;transition:transform .16s}}.tcard:hover{{transform:translate(-3px,-4px) rotate(-.5deg)}}
.tcard .ta{{border-bottom:3.5px solid var(--ink)}}.tcard .ta svg{{display:block;width:100%;height:auto}}.tcard .tb{{padding:1rem 1.2rem 1.3rem}}.tcard h3 a{{text-decoration:none}}.tcard h3 a:after{{content:"";position:absolute;inset:0}}
/* pathfinder */
.pf{{background:#fff;border:4px solid var(--ink);border-radius:28px;box-shadow:8px 8px 0 var(--ink);padding:1.2rem}}
.pf form{{display:flex;gap:.6rem;flex-wrap:wrap}}.pf input[type=text]{{flex:1 1 260px;font:600 1.1rem Inter;padding:1rem 1.1rem;border:3px solid var(--ink);border-radius:16px;background:var(--cream);min-height:56px}}
.pf input[type=text]:focus{{outline:3px solid var(--plum);outline-offset:2px}}.pf .btn{{min-height:56px;font-size:1.1rem}}
.chips{{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.8rem}}.chip{{font:600 .88rem Inter;background:var(--paper);border:2px solid var(--ink);border-radius:999px;padding:.45rem .8rem;cursor:pointer;min-height:40px;color:var(--ink)}}.chip:hover{{background:var(--mustard)}}
.agetog{{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.8rem;align-items:center}}.agetog span{{font-weight:700;font-size:.9rem;margin-right:.2rem}}.agetog button{{font:700 .9rem "Space Grotesk";min-height:44px;padding:.4rem .9rem;border:3px solid var(--ink);border-radius:12px;background:#fff;cursor:pointer;color:var(--ink)}}.agetog button[aria-pressed=true]{{background:var(--ink);color:var(--cream)}}
#pfout{{margin-top:var(--s5)}}.pfhead{{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin-bottom:var(--s3)}}.tag{{font:700 .78rem ui-monospace,monospace;background:var(--paper);border:2px solid var(--ink);border-radius:8px;padding:.2rem .5rem}}
.stack2{{display:flex;flex-wrap:wrap;gap:.7rem;margin:var(--s3) 0 var(--s4)}}.stool{{display:flex;gap:.6rem;align-items:center;background:#fff;border:3px solid var(--ink);border-radius:16px;padding:.55rem .9rem .55rem .55rem;box-shadow:4px 4px 0 var(--ink);text-decoration:none;min-height:52px}}.stool i{{font-style:normal;width:36px;height:36px;border-radius:10px;border:2.5px solid var(--ink);background:var(--c);display:grid;place-items:center;font:700 1rem "Space Grotesk"}}.stool small{{display:block;color:var(--mut);font-size:.75rem}}
.road{{position:relative;list-style:none;padding:0 0 0 0;margin:0}}.road:before{{content:"";position:absolute;left:27px;top:10px;bottom:10px;border-left:4px dashed var(--ink);opacity:.35}}
.road li{{position:relative;padding:0 0 1.1rem 72px;opacity:0;transform:translateY(14px);animation:unfold .45s cubic-bezier(.3,1.4,.5,1) forwards}}
.road li .dot{{position:absolute;left:0;top:0;width:58px;height:58px;border-radius:18px;border:3.5px solid var(--ink);background:var(--c);display:grid;place-items:center;font:700 1.3rem "Space Grotesk";box-shadow:4px 4px 0 var(--ink)}}
.road li .sbox{{background:#fff;border:3.5px solid var(--ink);border-radius:20px;padding:.9rem 1.1rem;box-shadow:var(--sh)}}.road li h3{{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}}.road li h3 small{{font:700 .78rem ui-monospace,monospace;background:var(--paper);border:2px solid var(--ink);border-radius:8px;padding:.15rem .45rem}}
@keyframes unfold{{to{{opacity:1;transform:none}}}}
.prompt textarea{{width:100%;min-height:150px;font:400 .9rem/1.5 ui-monospace,monospace;background:var(--ink);color:var(--cream);border:3.5px solid var(--ink);border-radius:16px;padding:2.2rem 1rem 1rem;box-shadow:var(--sh);resize:vertical}}.prompt{{position:relative}}
.pfgrid{{display:grid;grid-template-columns:1fr 1fr;gap:var(--s5);margin-top:var(--s5)}}
@media (max-width:860px){{.tutlayout,.pfgrid{{grid-template-columns:1fr}}.side{{position:static}}.road li{{padding-left:62px}}.road li .dot{{width:48px;height:48px;font-size:1.1rem}}.road:before{{left:22px}}}}
@media (prefers-reduced-motion:reduce){{.road li{{animation:none;opacity:1;transform:none}}}}
"""
def build_teach():
    (OUT/"style.css").write_text((OUT/"style.css").read_text()+TCSS.replace("{{","{").replace("}}","}"))
    # ---- tutorials
    tc=[]
    for i,t in enumerate(tuts):
        art=ART.get({"single-file-html-game-with-ai":"ai","godot-2d-platformer":"engine","scratch-first-game-kids":"age-kids","roblox-obby":"kids","blender-low-poly-to-godot":"blender-to-godot-3d","unity-first-3d-game":"engine","pixel-art-basics":"art","free-game-sound":"audio","publish-on-itch":"publish","twine-story-game":"learn","pico-8-first-cart":"first-game-this-weekend","make-a-game-with-your-kid":"kids-game-making"}.get(t["slug"],"hero"))
        nxt=TUT.get(t["next"]);vv=[VID[x] for x in t["videos"] if x in VID]
        side=f'''<aside class="side"><nav class="box2 toc" aria-label="Lesson steps"><h3>Lesson steps</h3><ol>{"".join(f'<li><a href="#{re.sub(r"[^a-z0-9]+","-",h.lower()).strip("-")}">{E(h)}</a></li>' for h in re.findall(r"^## (.+)$",t["body"],re.M))}</ol></nav><div class="box2"><h3>{icon("star",16)} Checklist</h3><ul class="check">{"".join(f'<li><input type="checkbox" id="c{i}{j}"><label for="c{i}{j}">{E(c)}</label></li>' for j,c in enumerate(t["checklist"]))}</ul></div>
<div class="box2"><h3>{icon("blocks",16)} Tools</h3><div class="meta" style="padding:0">{"".join(f'<a class="pill" href="../tools/{x}.html">{E(BY[x]["name"])}</a>' for x in t["tools"] if x in BY)}</div></div>
{f'<div class="box2"><h3>{icon("arrow-right",16)} Next tutorial</h3><a href="{nxt["slug"]}.html"><b>{E(nxt["title"])}</b></a></div>' if nxt else ""}</aside>'''
        body=f'''<div class="phead"><div><span class="eyebrow">{icon("book-open",14)} Tutorial</span><h1>{E(t["title"])}</h1><p style="font-size:1.15rem">{E(t["summary"])}</p>
<div class="tutmeta"><span class="tag">⏱ {E(t["time"])}</span><span class="lvl {t["skill"]}">{SK[t["skill"]]}</span>{agechips(t["ages"])}</div></div>{art}</div>
<div class="tutlayout"><article class="prose">{md(t["body"])}{f'<h2>Watch: related videos</h2><div class="vgrid">{"".join(vcard(v,"../") for v in vv)}</div>' if vv else ""}
<p class="mut" style="margin-top:var(--s4);font-size:.9rem">Written by {SITE_NAME}. Last verified {LAST_VERIFIED} — tools change, so check official docs if a menu has moved.</p></article>{side}</div>{ticket()}{YTJS}<div class="rprog" aria-hidden="true"><span></span></div><script>(function(){{const b=document.querySelector(".rprog span"),a=document.querySelector("article.prose"),L=[...document.querySelectorAll(".toc a")];function u(){{const r=a.getBoundingClientRect(),p=Math.min(1,Math.max(0,-r.top/(r.height-innerHeight)));b.style.transform="scaleX("+p+")";let cur=null;L.forEach(l=>{{const h=document.getElementById(l.getAttribute("href").slice(1));if(h&&h.getBoundingClientRect().top<140)cur=l}});L.forEach(l=>l.classList.toggle("on",l==cur))}}addEventListener("scroll",u,{{passive:true}});u()}})()</script>'''
        page(f"tutorials/{t['slug']}.html",f"{t['title']} — tutorial — {SITE_NAME}",t["summary"][:158],body,
             {"@context":"https://schema.org","@type":"HowTo","name":t["title"],"description":t["summary"],"tool":[{"@type":"HowToTool","name":BY[x]["name"]} for x in t["tools"] if x in BY],
              "step":[{"@type":"HowToStep","name":h} for h in re.findall(r"^## (.+)$",t["body"],re.M)]},[("Tutorials","tutorials/"),(t["title"],None)],og="paths")
        tc.append(f'<article class="tcard"><div class="ta">{art}</div><div class="tb"><div class="tutmeta" style="margin:0 0 .5rem"><span class="tag">⏱ {E(t["time"])}</span>{agechips(t["ages"])}</div><h3><a href="{"tutorials/" if False else ""}{t["slug"]}.html">{E(t["title"])}</a></h3><p class="mut" style="margin:.4rem 0 0">{E(t["summary"])}</p></div></article>')
    page("tutorials/index.html",f"Free game-making tutorials — {SITE_NAME}","Original, beginner-friendly tutorials: AI single-file games, Godot, Scratch, Roblox, Blender, Unity, pixel art, sound, itch.io, Twine, PICO-8 and making games with kids.",
         f'<div class="phead"><div><span class="eyebrow">{icon("book-open",14)} Tutorials</span><h1>Learn by making.</h1><p style="font-size:1.15rem">{len(tuts)} hands-on tutorials written in plain language, each with a checklist, time estimate, age range, related videos and a next step.</p><p><a class="btn" href="../pathfinder/">{icon("sparkles")} Not sure where to start? Describe your game</a></p></div>{cluster()}</div><div class="tcards">{"".join(tc)}</div>{ticket()}',
         {"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE_URL}/tutorials/{t['slug']}.html","name":t["title"]} for i,t in enumerate(tuts)]},[("Tutorials",None)],og="paths")
    # ---- videos
    types=sorted({x for v in vids for x in v["types"]});vtools=sorted({x for v in vids for x in v.get("tools",[]) if x in BY},key=lambda s:BY[s]["name"])
    TL={p["id"]:p["title"] for p in paths_t};TL.update({"any":"General / any game","3d-art":"3D art","2d-art":"2D art","pixel-art":"Pixel art","sound":"Sound & music","kids-game":"Kids' games"})
    body=f'''<div class="phead"><div><span class="eyebrow">{icon("play",14)} Video library</span><h1>Watch people make games.</h1><p style="font-size:1.1rem">{len(vids)} real tutorials from official channels and well-known teachers, hand-tagged by tool, game type and age. Videos load only when you click — no YouTube tracking before that.</p></div>{pic2("hero",[1280,960,640],"Clay illustration of floating game worlds")}</div>
<div class="controls" style="grid-template-columns:2fr 1fr 1fr 1fr"><input id="vq" type="search" placeholder="Search videos…" aria-label="Search videos"><select id="vt" aria-label="Tool"><option value="">Any tool</option>{"".join(f'<option value="{s}">{E(BY[s]["name"])}</option>' for s in vtools)}</select>
<select id="vg" aria-label="Game type"><option value="">Any game type</option>{"".join(f'<option value="{x}">{E(TL.get(x,x))}</option>' for x in types)}</select><select id="va" aria-label="Age"><option value="">Any age</option>{"".join(f'<option value="{k}">{v[0]} ({v[1]})</option>' for k,v in AGES.items())}</select></div>
<p class="mut" id="vc"></p><div class="vgrid" id="vl">{"".join(vcard(v,"../") for v in vids)}</div><div class="empty" id="vnone" hidden>{ART["kids"]}<h3>No videos match that combo.</h3><p class="mut">Try clearing a filter.</p></div>
<p class="mut" style="margin-top:var(--s4);font-size:.88rem">Every video was checked to exist on {vids[0]["verified"]} via YouTube's oEmbed; titles and channel names are shown exactly as YouTube reports them. Videos belong to their creators.</p>{YTJS}
<script>const $=i=>document.getElementById(i);function vf(){{const q=$("vq").value.toLowerCase(),t=$("vt").value,g=$("vg").value,a=$("va").value;let n=0;document.querySelectorAll(".vcard").forEach(c=>{{const ok=(!q||c.innerText.toLowerCase().includes(q))&&(!t||c.dataset.tools.split(" ").includes(t))&&(!g||c.dataset.types.split(" ").includes(g))&&(!a||c.dataset.ages.split(" ").includes(a));c.hidden=!ok;n+=ok}});$("vc").textContent=n+" of {len(vids)} videos";$("vnone").hidden=n>0}}["vq","vt","vg","va"].forEach(i=>$(i).addEventListener("input",vf));vf()</script>'''
    page("videos/index.html",f"Game-making video tutorials — {SITE_NAME}",f"{len(vids)} verified YouTube tutorials for Godot, Unity, Unreal, Roblox, Scratch, Blender, pixel art and more — filter by tool, game type and age.",body,
         {"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"VideoObject","name":v["title"],"embedUrl":f"https://www.youtube-nocookie.com/embed/{v['id']}","url":v["url"],"thumbnailUrl":f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"}} for i,v in enumerate(vids)]},[("Videos",None)],og="showcase")
    # ---- pathfinder
    data={"paths":paths_t,"tools":{t["slug"]:{"n":t["name"],"c":CATS[t["category"]][2],"a":t.get("ages",[]),"p":t["price"],"k":t["category"]} for t in tools},
          "tuts":{t["slug"]:{"t":t["title"],"time":t["time"],"a":t["ages"]} for t in tuts},"vids":[{"id":v["id"],"t":v["title"],"ch":v["channel"],"len":v.get("length"),"ty":v["types"],"to":v.get("tools",[]),"a":v["ages"]} for v in vids]}
    (OUT/"pathfinder").mkdir(exist_ok=True);(OUT/"pathfinder/data.json").write_text(json.dumps(data,ensure_ascii=False))
    EX=["a 2D platformer with a cat","multiplayer racing on Roblox","a 3D horror game","tetris-like puzzle on phone","VR game for Quest","story game for my kid","an idle clicker made with AI","a cozy farming game","Fortnite island deathrun","a math quiz game for class"]
    body=f'''<div class="phead" style="margin-bottom:var(--s4)"><div><span class="eyebrow">{icon("sparkles",14)} Pathfinder</span><h1>Describe your game. We'll unfold the path.</h1><p style="font-size:1.1rem">Type the game you dream of making. Pathfinder picks the right tools for your age, lays out the steps with time estimates, and hands you a tutorial, videos and an AI starter prompt. It runs entirely in your browser — nothing you type is sent anywhere.</p></div>{pic2("hero",[1280,960,640],"Clay illustration of a laptop with floating game worlds")}</div>
{PFFORM("")}<div id="pfout" aria-live="polite"></div>{YTJS}<script src="pathfinder.js" defer></script>'''
    page("pathfinder/index.html",f"Pathfinder: describe your game, get a step-by-step path — {SITE_NAME}","Type the game you want to make and get an age-aware tool stack, steps with time estimates, tutorials, videos and an AI starter prompt.",body,
         {"@context":"https://schema.org","@type":"WebApplication","name":"BuildGames Hub Pathfinder","applicationCategory":"EducationalApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},[("Make a game",None)],og="paths")
    (OUT/"pathfinder/pathfinder.js").write_text(PFJS)
    return EX
def PFFORM(pre,action=""):
    EX=["a 2D platformer with a cat","multiplayer racing on Roblox","a 3D horror game","tetris-like puzzle on phone","VR game for Quest","story game for my kid","an idle clicker made with AI","a cozy farming game"]
    return f'''<div class="pf"><form id="pff" action="{action}" method="get" role="search"><label class="skip" for="pfq">Describe the game you want to make</label><input type="text" id="pfq" name="q" placeholder="e.g. a 2D platformer with a cat" autocomplete="off" required><input type="hidden" name="age" id="pfage" value="">
<button class="btn" type="submit">{icon("sparkles")} Show my path</button></form>
<div class="agetog" role="group" aria-label="Who is building?"><span>Who's building?</span><button type="button" data-age="kids" aria-pressed="false">Kid 6–12</button><button type="button" data-age="teens" aria-pressed="false">Teen 13–17</button><button type="button" data-age="adults" aria-pressed="false">Grown-up 18+</button></div>
<div class="chips" aria-label="Examples">{"".join(f'<button type="button" class="chip">{E(x)}</button>' for x in EX)}</div></div>
<script>(function(){{const f=document.getElementById("pff"),q=document.getElementById("pfq"),ag=document.getElementById("pfage");document.querySelectorAll(".agetog button").forEach(b=>b.onclick=()=>{{document.querySelectorAll(".agetog button").forEach(x=>x.setAttribute("aria-pressed",x==b));ag.value=b.dataset.age;if(window.PF&&q.value)PF.run(q.value,ag.value)}});document.querySelectorAll(".chip").forEach(c=>c.onclick=()=>{{q.value=c.textContent;if(window.PF){{PF.run(q.value,ag.value)}}else f.submit()}});}})()</script>'''
PFJS=r"""(async function(){
const D=await (await fetch("data.json")).json();const out=document.getElementById("pfout"),q=document.getElementById("pfq"),agIn=document.getElementById("pfage");
const AG={kids:"Kid (6–12)",teens:"Teen (13–17)",adults:"Grown-up (18+)"};const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const has=(t,k)=>k.length<=3?new RegExp("(^|[^a-z0-9])"+k.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+"([^a-z0-9]|$)").test(t):t.includes(k);
function detectAge(t){if(/\b(my (kid|son|daughter|child)|for kids|kid|kids|child|children|i'?m ([5-9]|1[0-2])\b|grade|year old)/.test(t)&&!/teen/.test(t))return"kids";if(/\b(teen|teenager|high school|i'?m 1[3-7]\b)/.test(t))return"teens";return""}
function run(text,age){
 const t=" "+text.toLowerCase()+" ";age=age||detectAge(t)||"adults";
 document.querySelectorAll(".agetog button").forEach(b=>b.setAttribute("aria-pressed",b.dataset.age==age));
 const f={roblox:/roblox|obby/.test(t),fortnite:/fortnite|uefn/.test(t),vr:/\bvr\b|quest|oculus|virtual reality|headset/.test(t),phone:/phone|mobile|android|iphone|ios|tablet|app store|play store/.test(t),
  web:/browser|\bweb\b|html|website|itch/.test(t),console:/switch|xbox|playstation|ps5|console/.test(t),pc:/\bpc\b|steam|windows|mac/.test(t),d3:/\b3d\b|3-d|three d/.test(t),d2:/\b2d\b|2-d|pixel/.test(t),
  multi:/multiplayer|online|friends|co-?op|pvp|mmo|together/.test(t),ai:/\bai\b|claude|chatgpt|gpt|grok|gemini|vibe|codex|cursor|prompt/.test(t),free:/free|no money|\bcheap|budget|\$0/.test(t),
  beginner:/first|beginner|never|easy|simple|new to/.test(t),adv:/advanced|experienced|pro\b|professional|commercial/.test(t)};
 let best=null,bs=0,scores=[];
 for(const p of D.paths){let s=0;for(const k of p.keywords)if(has(t,k))s+=k.length>4?3:2;
  if(f.fortnite&&p.id=="uefn")s+=8;if(f.vr&&p.id=="vr")s+=8;if(f.phone&&p.id=="mobile-casual")s+=1;if(f.ai&&p.id=="html-vibe")s+=1;
  if(f.d3&&p.dim=="3d")s+=1;if(f.d3&&p.dim=="2d")s-=2;if(f.d3&&/shoot/.test(t)&&p.id=="fps")s+=4;if(f.d2&&p.dim=="2d")s+=1;scores.push([s,p]);if(s>bs){bs=s;best=p}}
 scores.sort((a,b)=>b[0]-a[0]);let fallback=false;
 if(f.roblox&&bs<2){best=D.paths.find(p=>p.id=="obby");bs=2}
 if(f.fortnite&&bs<2){best=D.paths.find(p=>p.id=="uefn");bs=2}
 if(!best||bs<2){fallback=true;best=D.paths.find(p=>p.id==(age=="kids"?"kids-game":"html-vibe"))}
 // stack
 let st=[...best.stack[age]];const add=(s,front)=>{if(D.tools[s]&&!st.includes(s))front?st.unshift(s):st.push(s)};const notes=[];
 if(f.roblox){st=["roblox-studio"];if(best.dim=="3d")st.push("blender")}
 if(f.fortnite){st=["uefn-unreal-editor-for-fortnite"];if(age!="adults")notes.push("Publishing a Fortnite island requires a legal adult — build and playtest, and have a grown-up handle publishing.")}
 if(f.vr){add("unity",1);add("meta-xr-sdk-unity")}
 if(f.d3&&best.dim=="2d"&&!f.roblox)add("blender");
 if(f.ai){if(age=="adults"){add("claude",1)}else if(age=="teens"){add("chatgpt",1)}else notes.push("AI chatbots are 13+ (ChatGPT, Grok) or 18+ (Claude). For kids, a grown-up should drive any AI help.")}
 if(f.multi&&!f.roblox&&!f.fortnite&&best.id!="party")notes.push("Online multiplayer adds networking work — prototype it single-player or same-screen first; Roblox handles servers for you.");
 if(f.web)add("itch-io");
 if(f.phone){if(age=="adults"){add("google-play-console");add("apple-app-store")}else notes.push("Phone stores require an adult developer account — test as a web game on your phone first.")}
 if(f.console)notes.push("Console publishing needs approved developer programs; start on PC/web and port later.");
 let dropped=st.filter(s=>!(D.tools[s].a||[]).includes(age));st=st.filter(s=>(D.tools[s].a||[]).includes(age));
 if(f.free)st=st.filter(s=>D.tools[s].p!="paid");
 if(st.length<2)for(const s of best.stack[age])if((D.tools[s].a||[]).includes(age)&&!st.includes(s))st.push(s);
 st=st.slice(0,5);
 // steps
 const steps=best.steps.map(s=>({...s}));const pub=steps[steps.length-1];
 if(f.roblox&&best.id!="obby")pub.text="Publish from Roblox Studio; review the Creator Hub rules for your age and audience.";
 if(age=="kids")pub.text="Share privately with family first — a grown-up should handle any online publishing or accounts.";
 // tutorial + videos
 const tut=D.tuts[best.tutorial];const vt=new Set(best.video_types),ts=new Set(st);
 const vids=D.vids.map(v=>[v.ty.filter(x=>vt.has(x)).length*3+v.to.filter(x=>ts.has(x)).length*2+(v.ty.includes("any")?0.5:0)+(v.a.includes(age)?1:-5),v]).filter(x=>x[0]>1).sort((a,b)=>b[0]-a[0]).slice(0,4).map(x=>x[1]);
 // prompt
 const names=st.map(s=>D.tools[s].n).join(", ");const desc=text.trim().replace(/^(i want to make|make|build|i want)\s+/i,"");
 const prompt=`You are a friendly, patient game-development mentor. I'm a ${age=="adults"?"":age=="teens"?"teenage ":"young "}${f.adv?"experienced":"beginner"} maker.\nHelp me build ${best.prompt.replace("{desc}",desc)}\nTools I plan to use: ${names}.\nWork in small steps: first give me the smallest playable version, then wait for me to test it before adding features. Explain what each part does in plain language.`;
 const cols=["#f2b134","#5ab4f0","#ff6b4a","#2bb3a3","#7b5cff","#5bbf6a"];
 out.innerHTML=`<div class="pfhead"><span class="eyebrow" style="margin:0">Your path</span>${fallback?'<span class="tag">closest match</span>':""}<span class="tag">${esc(best.title)}</span><span class="tag">${AG[age]}</span>${best.dim=="3d"?'<span class="tag">3D</span>':'<span class="tag">2D</span>'}${f.multi?'<span class="tag">multiplayer</span>':""}${f.ai?'<span class="tag">with AI</span>':""}${f.free?'<span class="tag">free tools</span>':""}</div>
 <h2>${fallback?"We couldn't match that exactly — here's a great place to start.":"Your path to: “"+esc(desc)+"”"}</h2>${fallback?`<p class="mut">Try words like “platformer”, “puzzle”, “story”, “Roblox”, “3D horror” or “VR”. Other close matches: ${scores.slice(0,3).filter(x=>x[0]>0).map(x=>esc(x[1].title)).join(", ")||"—"}.</p>`:""}
 <h3 style="margin-top:var(--s4)">Your tool stack</h3><div class="stack2">${st.map(s=>`<a class="stool" href="../tools/${s}.html" style="--c:${D.tools[s].c}"><i>${esc(D.tools[s].n[0])}</i><span><b>${esc(D.tools[s].n)}</b><small>${D.tools[s].p}</small></span></a>`).join("")}</div>
 ${dropped.length?`<p class="mut" style="font-size:.9rem">Left out for this age: ${dropped.map(s=>esc(D.tools[s].n)).join(", ")} (age rules).</p>`:""}${notes.map(n=>`<div class="note">${esc(n)}</div>`).join("")}
 <h3 style="margin-top:var(--s4)">Steps</h3><ol class="road">${steps.map((s,i)=>`<li style="--c:${cols[i%6]};animation-delay:${.08+i*.12}s"><span class="dot">${i+1}</span><div class="sbox"><h3>${esc(s.phase)} <small>⏱ ${esc(s.time)}</small></h3><p style="margin:.3rem 0 0">${esc(s.text)}</p></div></li>`).join("")}</ol>
 <div class="pfgrid"><div><h3>${age=="kids"?"AI starter prompt (for a grown-up to use)":"Copy this AI prompt to start"}</h3><p class="mut" style="font-size:.9rem">Paste into Claude (18+), ChatGPT or Grok (13+, parent permission under 18).</p><div class="prompt"><button class="copy" type="button">Copy</button><textarea readonly aria-label="AI starter prompt">${esc(prompt)}</textarea></div></div>
 <div><h3>Read the tutorial</h3>${tut?`<a class="stool" style="--c:#f2b134;width:100%" href="../tutorials/${best.tutorial}.html"><i>📖</i><span><b>${esc(tut.t)}</b><small>⏱ ${esc(tut.time)}</small></span></a>`:""}<p style="margin-top:1rem"><a href="../tutorials/">All tutorials →</a></p></div></div>
 ${vids.length?`<h3 style="margin-top:var(--s5)">Watch</h3><div class="vgrid">${vids.map(v=>`<article class="vcard" style="--c:#ffe3a3"><button class="yt" type="button" data-id="${v.id}" aria-label="Play video: ${esc(v.t)}"><span class="ytbg">▶</span><span class="ytlen">${esc(v.len||"")}</span><span class="ytnote">Click to load from YouTube</span></button><div class="vb"><h3>${esc(v.t)}</h3><p class="mut">${esc(v.ch)}</p><a class="ext" href="https://www.youtube.com/watch?v=${v.id}" rel="noopener">Watch on YouTube ↗</a></div></article>`).join("")}</div>`:""}`;
 out.scrollIntoView({behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});
 const u=new URL(location);u.searchParams.set("q",text);u.searchParams.set("age",age);history.replaceState(null,"",u);
}
window.PF={run};document.getElementById("pff").addEventListener("submit",e=>{e.preventDefault();run(q.value,agIn.value)});
const P=new URLSearchParams(location.search);if(P.get("q")){q.value=P.get("q");agIn.value=P.get("age")||"";run(q.value,agIn.value)}
})();"""
RCSS="""
/* ===== 2026 REBRAND LAYER (overrides retro) ===== */
:root{--soft:0 24px 50px -28px #3b1f9e55,0 0 0 1px #ece6fb;--soft2:0 34px 70px -30px #3b1f9e77;--sh:var(--soft)}
body{background:#fbf8ff}
body:before{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;background:var(--mesh,radial-gradient(45% 40% at 10% 0,#e4d9ff 0,transparent 70%),radial-gradient(40% 35% at 95% 10%,#ffe0d6 0,transparent 70%),radial-gradient(45% 40% at 80% 100%,#d6f5ef 0,transparent 70%),radial-gradient(35% 30% at 0 90%,#fff0c2 0,transparent 70%))}
h1{background:linear-gradient(95deg,#1b1630 30%,#5b2fe0 80%,#a62f63);-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:-.035em}
.eyebrow{color:#5b2fe0}
.btn{border:0;border-radius:16px;background:linear-gradient(135deg,#ffd166,#f2b134);box-shadow:0 12px 26px -12px #c98a00aa}
.btn:hover{transform:translateY(-2px);box-shadow:0 18px 32px -12px #c98a00cc}.btn:active{transform:translateY(1px);box-shadow:0 6px 14px -8px #c98a00}
.btn.alt{background:#fff;box-shadow:0 0 0 1.5px #ddd3f7,0 10px 24px -14px #3b1f9e66}.btn.dark{background:linear-gradient(135deg,#2a1f5c,#1b1630);color:#fff;box-shadow:0 12px 26px -12px #1b1630}
.card,.feat,.vcard,.tcard,.sc,.hstep,.whob,.tile,.facts,.controls,.stool,.road li .sbox,ol.steps li,.steps-simple li,.parent,.side .box2,.news,.ticket,.empty,.pf{border:0!important;box-shadow:var(--soft)}
.card{border-radius:24px;background:#ffffffe6;backdrop-filter:blur(6px)}.card:hover{transform:translateY(-5px);box-shadow:var(--soft2)}
.card:before{border:0;border-radius:0 24px 0 32px;opacity:.9;width:46px;height:46px;right:0;top:0}
.dir.list .card{background:none;backdrop-filter:none;box-shadow:none!important;border-bottom:1px solid #e6e0f5!important}.dir.list .card:before{border:0;width:10px;height:10px}
.tile{border-radius:28px}.tile:hover{transform:translateY(-6px) rotate(-.5deg);box-shadow:var(--soft2)}.tile .lbl{border:0;box-shadow:0 6px 16px -8px #0006;background:#ffffffee;backdrop-filter:blur(8px)}.tile .n{border-radius:999px}
.feat{border-radius:26px}.feat .top{border:0}.feat .top span{border:0;box-shadow:0 10px 22px -10px #0005}
.whob{border-radius:30px}.whob .wart{border:0!important}.whob .go{border:0;box-shadow:0 6px 14px -6px #0006}
.lvl,.age{border:0!important;box-shadow:none!important;transform:none!important;border-radius:999px}.age.a-kids{background:#ffe7a3}.age.a-teens{background:#d4ebff}.age.a-adults{background:#cdf3ec}.lvl.beginner{background:#d6f5dc}.lvl.intermediate{background:#fff0bf}.lvl.advanced{background:#ffd9d0}
.pill{border:0;background:#f1ecfb}
.controls{border-radius:22px;background:#ffffffd9;backdrop-filter:blur(10px)}.controls input,.controls select{background:#f6f2ff}
.seg{border:0;box-shadow:0 0 0 1.5px #ddd3f7}.seg button[aria-pressed=true]{background:#5b3fd9}
.ghead{border-bottom:1px solid #e3dcf5}.ghead .gart{border:0;box-shadow:var(--soft);border-radius:20px}.gcount{-webkit-text-stroke:0;color:#d9cff8}
.ticket{-webkit-mask:none;background:linear-gradient(120deg,#fff3c9,#ffe0d6 60%,#e9e0ff);border-radius:28px}.ticket .stub{border-right:1.5px dashed #c9bdf0}
.news{background:linear-gradient(135deg,#5b3fd9,#3a2a99);border-radius:32px}.news:after{border:0;background:radial-gradient(circle,#ff8d72,#e2486b);opacity:.85}
.news input{border:0}
.sec.alt,.sec.band-color{background:#ffffff8c}.sec.inkbg{background:radial-gradient(60% 60% at 0 0,#3a2a99 0,transparent 70%),radial-gradient(50% 60% at 100% 100%,#0f6f68 0,transparent 70%),#1b1630}
.sec.inkbg h2{color:#fff}.pic:before{border:0;opacity:.85;filter:blur(1px)}.pic svg,.phead>svg{border:0!important;box-shadow:var(--soft2)!important;border-radius:28px}
.wave path{fill:#ffffff8c}
footer{position:relative;background:radial-gradient(50% 80% at 0 0,#3a2a99 0,transparent 70%),radial-gradient(40% 80% at 100% 100%,#0f6f68 0,transparent 70%),#17122b;margin-top:7rem}
footer:before{content:"";position:absolute;left:0;right:0;top:-59px;height:60px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 60' preserveAspectRatio='none'%3E%3Cpath d='M0,30 C240,70 480,0 720,25 C960,50 1200,5 1440,30 L1440,60 L0,60Z' fill='%2317122b'/%3E%3C/svg%3E") center/100% 100%}
.facts{border-radius:22px}.facts th{background:#f6f2ff}.note{border-left:4px solid #2bb3a3;background:#ffffffd9;box-shadow:var(--soft)}
.crumbs{font-size:.88rem}
/* generic page hero */
.phead{position:relative;background:#ffffffa6;backdrop-filter:blur(14px) saturate(1.3);-webkit-backdrop-filter:blur(14px) saturate(1.3);border-radius:36px;padding:clamp(1.4rem,4vw,2.8rem);box-shadow:0 30px 60px -36px #3b1f9e66,0 0 0 1px #ffffffcc;margin-bottom:3.5rem}
.phead .hpic img,.phead picture img{display:block;width:100%;height:auto;border-radius:26px;box-shadow:var(--soft2)}
.hvis{display:grid;place-items:center;min-height:220px;border-radius:30px;background:radial-gradient(circle at 50% 45%,#ffffff 0,transparent 60%)}.hvis .big img{width:min(240px,60vw);height:auto;filter:drop-shadow(0 26px 30px #3b1f9e44);animation:hfloat 6s ease-in-out infinite}.hvis.svgv svg{width:100%;height:auto;border-radius:26px;box-shadow:var(--soft2)}
.cluster{position:relative;height:260px}.cluster .clay2 img{position:absolute;width:130px;height:130px;filter:drop-shadow(0 18px 22px #3b1f9e44);animation:hfloat 6s ease-in-out infinite}
.cluster .c0 img{left:6%;top:6%}.cluster .c1 img{right:8%;top:0;animation-delay:-1.5s}.cluster .c2 img{left:18%;bottom:0;animation-delay:-3s}.cluster .c3 img{right:16%;bottom:6%;animation-delay:-4.5s}
/* tool: product card */
.k-tool .phead{grid-template-columns:1.3fr 1fr}
.prodtile{display:flex;flex-direction:column;align-items:center;text-align:center;gap:.3rem;padding:2rem 1.5rem;border-radius:32px;background:linear-gradient(160deg,#fff 0,#fff 55%,color-mix(in srgb,var(--c) 30%,#fff));box-shadow:var(--soft2)}
.prodtile .pt img{width:130px;height:130px;filter:drop-shadow(0 16px 18px #0003)}.pinit{width:120px;height:120px;border-radius:32px;display:grid;place-items:center;font:700 3.6rem "Space Grotesk";color:#fff;background:linear-gradient(140deg,var(--c),#5b3fd9);box-shadow:0 20px 34px -16px var(--c)}
.prodtile b{font:700 1.5rem "Space Grotesk";margin-top:.6rem}.prodtile small{color:var(--mut)}.pmeta{display:flex;gap:.4rem;flex-wrap:wrap;justify-content:center;margin-top:.6rem}.pmeta span{background:#f1ecfb;border-radius:999px;padding:.2rem .7rem;font-size:.8rem;font-weight:600}
/* category */
.k-category{--mesh:radial-gradient(50% 45% at 85% 5%,#d6ccff 0,transparent 70%),radial-gradient(45% 40% at 0 30%,#d6f5ef 0,transparent 70%),radial-gradient(40% 40% at 90% 100%,#ffe0d6 0,transparent 70%)}
.k-category .phead{border-radius:36px 36px 36px 120px}
/* compare: split VS hero */
.k-compare main .wrap>h1{font-size:clamp(2.2rem,6vw,4rem);text-align:center;padding:2.5rem 1rem;border-radius:36px;background:linear-gradient(100deg,#e4d9ff 0,#e4d9ff 49.5%,#ffe0d6 50.5%,#ffe0d6 100%);-webkit-background-clip:border-box;background-clip:border-box;color:#1b1630;-webkit-text-fill-color:#1b1630;box-shadow:var(--soft)}
.k-compare main .wrap>h1 span{color:#fff!important;-webkit-text-fill-color:#fff;background:linear-gradient(135deg,#e2486b,#5b3fd9);border-radius:999px;padding:.1em .45em;font-size:.6em;vertical-align:middle;margin:0 .3em}
.k-compare main .wrap>.eyebrow{display:block;text-align:center;margin-top:1.5rem}
/* path: roadmap */
.k-path ol.steps:before{content:"";position:absolute}.k-path ol.steps{position:relative;padding-left:.5rem}.k-path ol.steps li{border-radius:24px;margin-left:0!important}
.k-path ol.steps li:nth-child(odd){margin-right:12%!important}.k-path ol.steps li:nth-child(even){margin-left:12%!important}
.k-path ol.steps li:before{border:0;border-radius:14px;background:linear-gradient(135deg,#ffd166,#f2b134);box-shadow:0 8px 16px -8px #c98a00}
/* kids: bright, bouncy */
.k-for-kids{--mesh:radial-gradient(50% 45% at 0 0,#ffe08a 0,transparent 70%),radial-gradient(50% 45% at 100% 10%,#ffb8a3 0,transparent 70%),radial-gradient(45% 40% at 60% 100%,#c9f2e9 0,transparent 70%)}
.k-for-kids .phead{background:#fff8e0cc;border-radius:48px 48px 48px 48px}.k-for-kids h1{background:linear-gradient(95deg,#c4461a,#d63a5e 60%,#5b2fe0);-webkit-background-clip:text;background-clip:text}
.k-for-kids .card:nth-child(odd){transform:rotate(-1deg)}.k-for-kids .card:nth-child(even){transform:rotate(1deg)}.k-for-kids .card:hover{transform:translateY(-6px) rotate(0) scale(1.02)}
.k-for-kids .steps-simple li{border-radius:30px;background:#fff}.k-for-kids .steps-simple li:nth-child(4n+1){background:#fff1c7}.k-for-kids .steps-simple li:nth-child(4n+2){background:#ffe0d6}.k-for-kids .steps-simple li:nth-child(4n+3){background:#d6f5ef}.k-for-kids .steps-simple li:nth-child(4n){background:#e9e0ff}
.k-for-kids .steps-simple li{animation:bob 4s ease-in-out infinite}.k-for-kids .steps-simple li:nth-child(2){animation-delay:-1s}.k-for-kids .steps-simple li:nth-child(3){animation-delay:-2s}.k-for-kids .steps-simple li:nth-child(4){animation-delay:-3s}
.k-for-kids .parent{background:#fffffff2;border-radius:30px}
/* teens */
.k-for-teens{--mesh:radial-gradient(50% 45% at 0 0,#cfe6ff 0,transparent 70%),radial-gradient(50% 45% at 100% 0,#e4d9ff 0,transparent 70%),radial-gradient(45% 40% at 50% 100%,#d6f5ef 0,transparent 70%)}
.k-for-teens .phead{border-radius:16px 48px 16px 48px}
/* adults: sleek deep */
.k-for-adults .phead{background:radial-gradient(70% 90% at 0 0,#3a2a99 0,transparent 70%),radial-gradient(60% 80% at 100% 100%,#0f6f68 0,transparent 70%),#17122b;color:#f3efff;border-radius:28px}
.k-for-adults .phead h1{background:linear-gradient(95deg,#fff 40%,#b9f0e6);-webkit-background-clip:text;background-clip:text}.k-for-adults .phead .eyebrow{color:#ffd166}.k-for-adults .phead p{color:#ddd6f3}
.k-for-adults .card{border-radius:16px}
.agepick a{border:0;box-shadow:0 0 0 1.5px #ddd3f7;border-radius:999px}.agepick a[aria-current]{background:#5b3fd9;color:#fff;box-shadow:none}
/* tutorials index */
.k-tutorials .tcard{border-radius:28px}.k-tutorials .tcard .ta{border:0}.k-tutorials .tcards{grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}.k-tutorials .tcard:nth-child(3n+2){transform:translateY(24px)}.k-tutorials .tcard:nth-child(3n+2):hover{transform:translateY(18px)}
/* tutorial lesson reader */
.k-tutorial .tutlayout{grid-template-columns:minmax(0,1fr) 300px}.k-tutorial article.prose{background:#fff;border-radius:28px;padding:clamp(1.2rem,4vw,2.6rem);box-shadow:var(--soft);max-width:none;font-size:1.05rem;line-height:1.75}
.k-tutorial .prose h2{font-size:1.5rem;padding-top:.6rem;border-top:1px solid #eee8fb;scroll-margin-top:90px}.k-tutorial .prose h2:first-child{border:0}
.toc ol{list-style:none;padding:0;margin:0;counter-reset:t}.toc li{counter-increment:t}.toc a{display:flex;gap:.6rem;align-items:center;padding:.4rem .5rem;border-radius:10px;text-decoration:none;font-size:.9rem;color:var(--mut)}
.toc a:before{content:counter(t);flex:none;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font:700 .75rem Inter;background:#f1ecfb;color:#5b3fd9}.toc a.on{background:#f1ecfb;color:var(--ink);font-weight:600}.toc a.on:before{background:#5b3fd9;color:#fff}
.rprog{position:fixed;left:0;right:0;top:0;height:4px;z-index:30;background:transparent}.rprog span{display:block;height:100%;background:linear-gradient(90deg,#5b3fd9,#e2486b,#f2b134);transform-origin:0 50%;transform:scaleX(0)}
.code pre{border:0;box-shadow:var(--soft2);background:#1d1838}
/* videos: cinematic */
.k-videos{background:#120e24;color:#ece8ff}.k-videos:before{--mesh:x;background:radial-gradient(50% 40% at 10% 0,#3a2a99 0,transparent 70%),radial-gradient(40% 40% at 100% 30%,#7a2346 0,transparent 70%),radial-gradient(45% 40% at 50% 100%,#0f5752 0,transparent 70%)}
.k-videos header.top{background:#120e24cc;border-color:#ffffff1a}.k-videos header nav a{color:#ece8ff}.k-videos .brand span{color:#fff}.k-videos .burger{background:#f2b134}
.k-videos .phead{background:#ffffff0f;box-shadow:0 0 0 1px #ffffff1f}.k-videos h1{background:linear-gradient(95deg,#fff 30%,#ffb8a3 70%,#ffd166);-webkit-background-clip:text;background-clip:text}.k-videos .eyebrow{color:#ffd166}
.k-videos .mut,.k-videos .crumbs,.k-videos .crumbs a{color:#bdb5dc}.k-videos a{color:#ece8ff}
.k-videos .vgrid{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}.k-videos .vcard{background:#1e1838;color:#ece8ff;box-shadow:0 0 0 1px #ffffff14,0 30px 50px -30px #000}.k-videos .vcard:hover{box-shadow:0 0 0 1px #ffd16666,0 30px 60px -20px #5b3fd9aa}
.k-videos .vcard .mut{color:#bdb5dc}.k-videos .yt{border-bottom:0;background:linear-gradient(135deg,color-mix(in srgb,var(--c) 70%,#120e24),#120e24)}.k-videos .ytbg{border:0}.k-videos .controls{background:#ffffff12}.k-videos .controls input,.k-videos .controls select{background:#ffffff14;color:#fff}.k-videos .controls option{color:#000}
.k-videos .pill{background:#ffffff1a;color:#ece8ff}.k-videos .empty{background:#ffffff0f}
/* showcase: gallery */
.k-showcase{--mesh:radial-gradient(50% 45% at 100% 0,#ffd2c4 0,transparent 70%),radial-gradient(50% 45% at 0 20%,#e4d9ff 0,transparent 70%),radial-gradient(40% 40% at 50% 100%,#fff0c2 0,transparent 70%)}
.k-showcase .stack{grid-template-columns:1fr;gap:3rem}.k-showcase .sc{border-radius:36px;padding:clamp(1.4rem,4vw,2.6rem);display:grid;grid-template-columns:minmax(0,1fr) minmax(240px,340px);gap:0 2.5rem;background:#ffffffd9}
.k-showcase .sc:before,.k-showcase .sc:after{display:none}.k-showcase .sc>.vid{grid-column:2;grid-row:1/span 9;margin:0;align-self:start;border:0;border-radius:28px;box-shadow:var(--soft2)}.k-showcase .sc>*:not(.vid){grid-column:1}
.slot{border:0;background:#f6f2ff}.slot.solid{background:#fff4d6}
/* pathfinder */
.k-pathfinder .pf{background:#ffffffcc;backdrop-filter:blur(14px);border-radius:28px}.k-pathfinder .road li .dot{border:0;box-shadow:0 10px 18px -8px #0004}.k-pathfinder .road:before{border-left:3px dotted #b9a4ff;opacity:1}
.stool{border-radius:18px}.stool i{border:0}.prompt textarea{border:0;background:#1d1838}
.burger{border:0!important;border-radius:14px;background:linear-gradient(135deg,#ffd166,#f2b134)!important;box-shadow:0 10px 22px -10px #c98a00aa!important}.burger span{background:#1b1630;border-radius:3px}
header.top{border-bottom:1px solid #e6dff7!important;box-shadow:0 10px 30px -22px #3b1f9e88!important}.k-videos header.top{border-color:#ffffff14!important}
/* about / 404 */
.k-about .phead,.k-404 .phead{border-radius:60px 24px 60px 24px}
@media (max-width:860px){.k-tool .phead{grid-template-columns:1fr}.k-showcase .sc{grid-template-columns:1fr}.k-showcase .sc>.vid{grid-column:1;grid-row:auto;margin:1rem 0}.k-tutorials .tcard:nth-child(3n+2){transform:none}.k-path ol.steps li:nth-child(n){margin-left:0!important;margin-right:0!important}.k-tutorial .tutlayout{grid-template-columns:1fr}.cluster{height:200px}.cluster .clay2 img{width:96px;height:96px}}
@media (prefers-reduced-motion:reduce){.hvis .big img,.cluster .clay2 img,.k-for-kids .steps-simple li{animation:none}}
"""
_bt=build_teach
def build_teach():
    _bt();(OUT/"style.css").write_text((OUT/"style.css").read_text()+RCSS)
