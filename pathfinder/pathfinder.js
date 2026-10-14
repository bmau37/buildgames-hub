(async function(){
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
})();