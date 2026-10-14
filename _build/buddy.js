/* Build Buddy — phase 1: 100% client-side. Answers only from this site's data.
   Nothing typed is sent anywhere; the conversation lives in this browser's localStorage only.
   Provider interface: Providers.local (default) | Providers.remote (sponsor LLM via the SITE'S OWN serverless proxy;
   no API keys in the client; never used in kids mode). Enable by setting config.provider="remote" + endpoint at build time. */
(function(){
"use strict";
const me=document.currentScript, ROOT=me.src.replace(/buddy\/buddy\.js.*$/,""), KEY="bgh-buddy-v1";
const RM=matchMedia("(prefers-reduced-motion: reduce)").matches;
let D=null, st=load();
function load(){try{return JSON.parse(localStorage.getItem(KEY))||{msgs:[],age:"",flow:null}}catch(e){return{msgs:[],age:"",flow:null}}}
function save(){try{st.msgs=st.msgs.slice(-40);localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const L=(href,txt)=>`<a href="${ROOT}${href}">${esc(txt)}</a>`;
const AGE={kids:"a kid (6–12)",teens:"a teen (13–17)",adults:"a grown-up (18+)"};
const TYPES=[["Platformer","platformer"],["Puzzle","puzzle"],["Story","visual novel story"],["Roblox obby","roblox obby"],["3D world","3d adventure explore"],["Racing","racing"],["Make it with AI","ai single file html"]];

/* ---------- UI ---------- */
const fab=document.createElement("button");fab.className="bb-fab";fab.type="button";fab.setAttribute("aria-haspopup","dialog");fab.setAttribute("aria-expanded","false");fab.setAttribute("aria-controls","bb-panel");
fab.innerHTML='<span class="bb-face" aria-hidden="true">✦</span><span class="bb-t">Build Buddy</span>';fab.setAttribute("aria-label","Open Build Buddy, the game-making helper");
const P=document.createElement("section");P.className="bb-panel";P.id="bb-panel";P.hidden=true;P.setAttribute("role","dialog");P.setAttribute("aria-modal","false");P.setAttribute("aria-labelledby","bb-title");
P.innerHTML=`<div class="bb-head"><span class="bb-face" aria-hidden="true" style="width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:#ffffff33">✦</span><div><h2 id="bb-title">Build Buddy</h2><small>Your game-making guide</small></div><button type="button" class="bb-new" aria-label="Start over">↺</button><button type="button" class="bb-x" aria-label="Close Build Buddy">✕</button></div>
<div class="bb-log" role="log" aria-live="polite" aria-relevant="additions"></div><div class="bb-chips" role="group" aria-label="Suggested replies"></div>
<form class="bb-form"><label for="bb-in" class="sr-only" style="position:absolute;left:-9999px">Ask Build Buddy</label><input id="bb-in" autocomplete="off" maxlength="200" placeholder="Ask about making a game…"><button type="submit">Ask</button></form>
<p class="bb-disc">Runs only in your browser — nothing you type is sent or stored online. It’s a helper, not a person; kids, ask a grown-up when unsure.</p>`;
document.body.append(fab,P);
const log=P.querySelector(".bb-log"),chips=P.querySelector(".bb-chips"),inp=P.querySelector("#bb-in");
function render(m){const d=document.createElement("div");d.className="bb-m "+(m.who==="me"?"me":"bot");if(m.who==="me")d.textContent=m.html;else d.innerHTML=m.html;log.appendChild(d);log.scrollTop=log.scrollHeight}
function setChips(list){chips.innerHTML="";(list||[]).forEach(c=>{const b=document.createElement("button");b.type="button";b.textContent=c[0];b.onclick=()=>ask(c[1]||c[0],c[0]);chips.appendChild(b)})}
function bot(html,ch){const m={who:"bot",html,chips:ch||null};st.msgs.push(m);save();render(m);setChips(ch)}
async function open(){P.hidden=false;fab.setAttribute("aria-expanded","true");if(!D){try{D=await (await fetch(ROOT+"buddy/data.json")).json()}catch(e){bot("Sorry — I couldn’t load my notes. Try the "+L("start.html","Start here")+" page.");return}}
 if(!log.childElementCount){if(st.msgs.length){st.msgs.forEach(render);setChips(st.msgs[st.msgs.length-1].chips||MAIN())}else greet()}
 inp.focus()}
function close(){P.hidden=true;fab.setAttribute("aria-expanded","false");fab.focus()}
fab.onclick=open;P.querySelector(".bb-x").onclick=close;
P.querySelector(".bb-new").onclick=()=>{st={msgs:[],age:"",flow:null};save();log.innerHTML="";greet();inp.focus()};
P.addEventListener("keydown",e=>{if(e.key==="Escape"){e.preventDefault();close()}});
P.querySelector("form").onsubmit=e=>{e.preventDefault();const v=inp.value.trim();if(!v)return;inp.value="";ask(v)};

/* ---------- brain ---------- */
const MAIN=()=>[["Help me make a game","start"],["What tools are free?","free tools"],["What does a word mean?","glossary"],["Find a tutorial","tutorials"],["How do I share my game?","publish"]];
const AGECH=[["I’m a kid","age kids"],["I’m a teen","age teens"],["I’m a grown-up","age adults"]];
function greet(){bot("Hi! I’m <b>Build Buddy</b>. I’ll help you make a game, one small step at a time. First — who’s making it?",AGECH.concat([["Just browsing","menu"]]))}
const toolBy=s=>D.tools.find(t=>t.slug===s);
const tl=t=>L("tools/"+t.slug+".html",t.name);
function detectAge(t){if(/\b(i'?m|i am) ?([5-9]|1[0-2])\b|\b(kid|child|my son|my daughter|grade)\b/.test(t)&&!/teen/.test(t))return"kids";if(/\b(teen|teenager|high school|(i'?m|i am) ?1[3-7])\b/.test(t))return"teens";if(/\b(adult|grown[- ]?up|parent|i'?m an adult)\b/.test(t))return"adults";return""}
function has(t,k){return k.length<=3?new RegExp("(^|[^a-z0-9])"+k.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+"([^a-z0-9]|$)").test(t):t.includes(k)}
function matchPath(t){let best=null,bs=0;for(const p of D.paths){let s=0;for(const k of p.kw)if(has(t,k))s+=k.length>4?3:2;if(/roblox|obby/.test(t)&&p.id==="obby")s+=6;if(/fortnite|uefn/.test(t)&&p.id==="uefn")s+=6;if(s>bs){bs=s;best=p}}return bs>=2?best:null}
function planFor(p){const age=st.age||"adults";const stack=(p.stack[age]||[]).map(toolBy).filter(Boolean).slice(0,3);let tut=p.tut&&D.tuts.find(x=>x.slug===p.tut);if(!tut||!tut.ages.includes(age))tut=D.tuts.find(x=>x.ages.includes(age)&&x.slug!=="plan-your-first-game"&&x.tools.some(s=>stack.some(k=>k.slug===s)))||D.tuts.find(x=>x.ages.includes(age)&&x.slug!=="plan-your-first-game");
 const kidsWarn=age==="kids"?"<br><small>Grown-up tip: build together, and keep any chat or sharing settings locked down.</small>":"";
 return `Great choice: <b>${esc(p.title)}</b>, planned for ${AGE[age]}. Here’s your plan:<ol><li>Plan it on one page: ${L("tutorials/plan-your-first-game.html","Plan your first game")}</li><li>Use ${stack.length?stack.map(tl).join(" + "):"a beginner tool"}</li>${tut?`<li>Follow ${L("tutorials/"+tut.slug+".html",tut.title)} (${esc(tut.time)})</li>`:""}<li>Playtest with one person, fix the top 3 problems</li><li>Share it — ${L("tutorials/publish-on-itch.html","publish on itch.io")}</li></ol>Want the full step list with time estimates? ${L("pathfinder/?q="+encodeURIComponent(p.title),"Open it in Pathfinder")}.${kidsWarn}`}
const Providers={
 local:{reply:async(text)=>localReply(text)},
 remote:{reply:async(text)=>{ /* Adapter stub for a sponsor LLM. Calls ONLY the site's own serverless proxy (which holds the key).
     Never used for kids mode, never with stored history; sends just the current question + age band. */
   const c=D.config||{};if(!c.endpoint||st.age==="kids")return localReply(text);
   try{const r=await fetch(c.endpoint,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({q:text.slice(0,200),age:st.age||"adults"})});const j=await r.json();
     return{html:esc(j.answer||"")+"<br><small>Answer from our sponsor’s assistant.</small>",chips:MAIN()}}catch(e){return localReply(text)}}}};
function provider(){const c=(D&&D.config)||{};return (c.provider==="remote"&&c.endpoint&&st.age!=="kids")?Providers.remote:Providers.local}
async function ask(text,label){const m={who:"me",html:label||text};st.msgs.push(m);save();render(m);setChips([]);
 const r=await provider().reply(text);setTimeout(()=>bot(r.html,r.chips),RM?0:250)}
function localReply(raw){const t=" "+raw.toLowerCase().replace(/[’']/g,"'")+" ";
 // age
 let m=t.match(/^ age (kids|teens|adults) $/);const da=m?m[1]:detectAge(t);
 if(da){st.age=da;save();if(m||t.trim().split(/\s+/).length<5)return{html:`Got it — you’re ${AGE[da]}. What kind of game do you want to make?`,chips:TYPES.map(x=>[x[0],"make "+x[1]]).concat([["Not sure yet","not sure"]])}}
 if(/^ (menu|hi|hello|hey|help) $/.test(t))return{html:"Here’s what I can help with:",chips:MAIN()};
 const words=t.split(/\W+/).filter(w=>w.length>3);let fb=null,fs=0;for(const [q,a] of D.faq){const qw=q.toLowerCase();let s=0;for(const w of words)if(qw.includes(w))s++;if(s>fs){fs=s;fb=[q,a]}}
 if(fb&&fs>=3)return{html:`<b>${esc(fb[0])}</b><br>${esc(fb[1])} <span class="bb-l">${L("resources/faq.html","More beginner questions")}</span>`,chips:MAIN()};
 if(/ start | make a game|help me make|how do i (start|make|begin)|first game|where do i start/.test(t)){if(!st.age)return{html:"Let’s do it! Who’s making the game?",chips:AGECH};return{html:"What kind of game?",chips:TYPES.map(x=>[x[0],"make "+x[1]]).concat([["Not sure yet","not sure"]])}}
 if(/not sure|no idea|don't know|dunno|suggest/.test(t)){const a=st.age||"adults";const pick={kids:"Scratch",teens:"Godot",adults:"an AI single-file game"}[a];
   return{html:`No problem! Most people start with a tiny <b>platformer</b> or <b>puzzle</b>. For ${AGE[a]} I’d start with <b>${pick}</b>. Or just tell me a game you love and I’ll match it.`,chips:[["Platformer","make platformer"],["Puzzle","make puzzle"],["Start here page","start page"]]}}
 if(/start page|start here/.test(t))return{html:"The "+L("start.html","Start here page")+" has 3 simple paths — one plan, one tool, one tutorial each.",chips:MAIN()};
 // glossary
 if(/^ glossary $/.test(t))return{html:"Ask me “what is …” — like a sprite, game engine or CC0. Or browse the "+L("resources/glossary.html","whole glossary")+".",chips:[["What is a sprite?"],["What is a game engine?"],["What is CC0?"],["What is vibe coding?"]]};
 m=t.match(/what (is|are|does) (an? |the )?([a-z0-9 .\-\/]+?)( mean)?\s*\?? $/);
 if(m){const w=m[3].trim();const g=D.gloss.find(([k])=>k.toLowerCase().split(/ \/ | \(|\)/).some(x=>x&&(x.trim()===w||x.trim()===w.replace(/s$/,""))));if(g)return{html:`<b>${esc(g[0])}:</b> ${esc(g[1])} <span class="bb-l">${L("resources/glossary.html","More words in the glossary")}</span>`,chips:[["Help me make a game","start"],["Another word","glossary"]]};
   const tt=D.tools.find(x=>w.includes(x.name.toLowerCase())||x.name.toLowerCase()===w);if(tt)return toolReply(tt)}
 // free tools
 if(/free/.test(t)&&/tool|engine|software|app|what|which/.test(t)){const a=st.age;const f=D.tools.filter(x=>x.price==="free"&&x.skill==="beginner"&&(!a||x.ages.includes(a))).slice(0,6);
   return{html:`Free, beginner-friendly picks${a?" for "+AGE[a]:""}: <ul>${f.map(x=>"<li>"+tl(x)+" — "+esc(x.blurb)+"</li>").join("")}</ul>${L("index.html#tools","See all tools (filter by free)")}`,chips:[["Free art","free art"],["Free sounds","free sound"],["Help me make a game","start"]]}}
 if(/\b(art|sprite|graphics|asset|texture|model)s?\b/.test(t)&&/free|where|get|find/.test(t))return{html:"Free art you’re allowed to use: Kenney (CC0), Poly Haven (CC0), Quaternius (CC0) and more on our "+L("resources/art.html","free art page")+". Keep the license with each download!",chips:[["What is CC0?"],["Free sounds","free sound"]]};
 if(/sound|music|sfx|audio/.test(t))return{html:"For sounds: make retro effects with "+L("tools/bfxr-jsfxr.html","jsfxr")+", record with "+L("tools/audacity.html","Audacity")+", or grab license-checked ones from our "+L("resources/sound.html","free sound page")+". There’s a lesson too: "+L("tutorials/free-game-sound.html","free game sound")+".",chips:[["What is CC BY?"],["Help me make a game","start"]]};
 if(/publish|share|upload|itch|release|put (it )?online|let (my )?friends play/.test(t))return{html:"Easiest way: put a web build on itch.io — follow "+L("tutorials/publish-on-itch.html","Publish on itch.io")+". Single HTML file? "+L("tools/github-pages.html","GitHub Pages")+" works too."+(st.age==="kids"?"<br><small>Kids: ask a grown-up to help with accounts and sharing.</small>":""),chips:MAIN()};
 if(/^ tutorials? $|tutorial|lesson|course|learn/.test(t)){const a=st.age;const list=D.tuts.filter(x=>!a||x.ages.includes(a)).slice(0,6);return{html:`Tutorials${a?" for "+AGE[a]:""}: <ul>${list.map(x=>"<li>"+L("tutorials/"+x.slug+".html",x.title)+" <small>("+esc(x.time)+")</small></li>").join("")}</ul>`,chips:[["Show videos","videos"],["Help me make a game","start"]]}}
 if(/video|youtube|watch/.test(t))return{html:`We have ${D.vidcount} hand-checked videos, filterable by tool and age: ${L("videos/","video library")}. They don’t load anything from YouTube until you press play.`,chips:MAIN()};
 if(/code|coding|program/.test(t)&&/need|have to|must|without|no /.test(t))return{html:"You don’t need to code to start! Try "+L("tools/scratch.html","Scratch")+" (blocks), Roblox Studio templates, or describe a game to an AI assistant. Learning a little code later helps a lot.",chips:[["Help me make a game","start"],["What is vibe coding?"]]};
 if(/\bai\b|claude|chatgpt|grok|gemini|vibe/.test(t)&&!/make /.test(t)){if(st.age==="kids")return{html:"Most AI chatbots are for 13+ or 18+, so a grown-up should drive any AI help. Try "+L("tools/scratch.html","Scratch")+" together instead!",chips:MAIN()};
   return{html:"AI is great for a single-file browser game: describe it, test it, paste errors back, save versions. Lesson: "+L("tutorials/single-file-html-game-with-ai.html","Make a single-file HTML game with AI")+". Check age rules: Claude is 18+, ChatGPT and Grok 13+.",chips:MAIN()}}
 // FAQ
 // tool mention
 const STOP=["game","super","microsoft","adobe","apple","google","free","open","the","unity"];const tm=D.tools.find(x=>t.includes(" "+x.name.toLowerCase()))||D.tools.find(x=>{const w=x.name.toLowerCase().split(" ")[0];return w.length>3&&!STOP.includes(w)&&t.includes(" "+w+" ")});
 // game type
 const p=matchPath(t);
 if(p&&!(tm&&t.trim()===tm.name.toLowerCase()))return{html:planFor(p),chips:[["Free art","free art"],["How do I share it?","publish"],["Different game","start"]]};
 if(tm)return toolReply(tm);
 if(fb&&fs>=2)return{html:`<b>${esc(fb[0])}</b><br>${esc(fb[1])} <span class="bb-l">${L("resources/faq.html","More beginner questions")}</span>`,chips:MAIN()};
 return{html:"Hmm, I’m not sure about that one. I only know about making games. Try one of these, or describe your game idea in "+L("pathfinder/?q="+encodeURIComponent(raw.slice(0,80)),"Pathfinder")+".",chips:MAIN()};}
function toolReply(x){const a=st.age;const ok=!a||x.ages.includes(a);return{html:`<b>${esc(x.name)}</b> — ${esc(x.blurb)}<br><small>${esc(x.price)} · ${esc(x.skill)}${ok?"":" · <b>not aimed at "+AGE[a]+"</b>"}</small><span class="bb-l">${tl(x)} — who it’s for, cost, first steps</span>`,chips:[["Help me make a game","start"],["What tools are free?","free tools"]]}}
})();
