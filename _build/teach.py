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
        side=f'''<aside class="side"><div class="box2"><h3>{icon("star",16)} Checklist</h3><ul class="check">{"".join(f'<li><input type="checkbox" id="c{i}{j}"><label for="c{i}{j}">{E(c)}</label></li>' for j,c in enumerate(t["checklist"]))}</ul></div>
<div class="box2"><h3>{icon("blocks",16)} Tools</h3><div class="meta" style="padding:0">{"".join(f'<a class="pill" href="../tools/{x}.html">{E(BY[x]["name"])}</a>' for x in t["tools"] if x in BY)}</div></div>
{f'<div class="box2"><h3>{icon("arrow-right",16)} Next tutorial</h3><a href="{nxt["slug"]}.html"><b>{E(nxt["title"])}</b></a></div>' if nxt else ""}</aside>'''
        body=f'''<div class="phead"><div><span class="eyebrow">{icon("book-open",14)} Tutorial</span><h1>{E(t["title"])}</h1><p style="font-size:1.15rem">{E(t["summary"])}</p>
<div class="tutmeta"><span class="tag">⏱ {E(t["time"])}</span><span class="lvl {t["skill"]}">{SK[t["skill"]]}</span>{agechips(t["ages"])}</div></div>{art}</div>
<div class="tutlayout"><article class="prose">{md(t["body"])}{f'<h2>Watch: related videos</h2><div class="vgrid">{"".join(vcard(v,"../") for v in vv)}</div>' if vv else ""}
<p class="mut" style="margin-top:var(--s4);font-size:.9rem">Written by {SITE_NAME}. Last verified {LAST_VERIFIED} — tools change, so check official docs if a menu has moved.</p></article>{side}</div>{ticket()}{YTJS}'''
        page(f"tutorials/{t['slug']}.html",f"{t['title']} — tutorial — {SITE_NAME}",t["summary"][:158],body,
             {"@context":"https://schema.org","@type":"HowTo","name":t["title"],"description":t["summary"],"tool":[{"@type":"HowToTool","name":BY[x]["name"]} for x in t["tools"] if x in BY],
              "step":[{"@type":"HowToStep","name":h} for h in re.findall(r"^## (.+)$",t["body"],re.M)]},[("Tutorials","tutorials/"),(t["title"],None)],og="paths")
        tc.append(f'<article class="tcard"><div class="ta">{art}</div><div class="tb"><div class="tutmeta" style="margin:0 0 .5rem"><span class="tag">⏱ {E(t["time"])}</span>{agechips(t["ages"])}</div><h3><a href="{"tutorials/" if False else ""}{t["slug"]}.html">{E(t["title"])}</a></h3><p class="mut" style="margin:.4rem 0 0">{E(t["summary"])}</p></div></article>')
    page("tutorials/index.html",f"Free game-making tutorials — {SITE_NAME}","Original, beginner-friendly tutorials: AI single-file games, Godot, Scratch, Roblox, Blender, Unity, pixel art, sound, itch.io, Twine, PICO-8 and making games with kids.",
         f'<div class="phead"><div><span class="eyebrow">{icon("book-open",14)} Tutorials</span><h1>Learn by making.</h1><p style="font-size:1.15rem">{len(tuts)} hands-on tutorials written in plain language, each with a checklist, time estimate, age range, related videos and a next step.</p><p><a class="btn" href="../pathfinder/">{icon("sparkles")} Not sure where to start? Describe your game</a></p></div>{ART["learn"]}</div><div class="tcards">{"".join(tc)}</div>{ticket()}',
         {"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE_URL}/tutorials/{t['slug']}.html","name":t["title"]} for i,t in enumerate(tuts)]},[("Tutorials",None)],og="paths")
    # ---- videos
    types=sorted({x for v in vids for x in v["types"]});vtools=sorted({x for v in vids for x in v.get("tools",[]) if x in BY},key=lambda s:BY[s]["name"])
    TL={p["id"]:p["title"] for p in paths_t};TL.update({"any":"General / any game","3d-art":"3D art","2d-art":"2D art","pixel-art":"Pixel art","sound":"Sound & music","kids-game":"Kids' games"})
    body=f'''<div class="phead"><div><span class="eyebrow">{icon("play",14)} Video library</span><h1>Watch people make games.</h1><p style="font-size:1.1rem">{len(vids)} real tutorials from official channels and well-known teachers, hand-tagged by tool, game type and age. Videos load only when you click — no YouTube tracking before that.</p></div>{ART["showcase"]}</div>
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
    body=f'''<div class="phead" style="margin-bottom:var(--s4)"><div><span class="eyebrow">{icon("sparkles",14)} Pathfinder</span><h1>Describe your game. We'll unfold the path.</h1><p style="font-size:1.1rem">Type the game you dream of making. Pathfinder picks the right tools for your age, lays out the steps with time estimates, and hands you a tutorial, videos and an AI starter prompt. It runs entirely in your browser — nothing you type is sent anywhere.</p></div>{ART["hero"]}</div>
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
  if(f.d3&&p.dim=="3d")s+=1;if(f.d2&&p.dim=="2d")s+=1;scores.push([s,p]);if(s>bs){bs=s;best=p}}
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
