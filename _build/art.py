"""Hand-made SVG illustrations (original, license-clean). Flat ink-outline style, shared palette."""
INK="#1b1630";CREAM="#f6efe3";P={"tomato":"#ff6b4a","teal":"#2bb3a3","mustard":"#f2b134","plum":"#7b5cff","sky":"#5ab4f0","pink":"#ef6fa8","leaf":"#5bbf6a","stone":"#8d8aa3"}
S=f'stroke="{INK}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'
def cube(x,y,s,c):
    h=s/2
    return (f'<path d="M{x},{y} l{s},{-h} l{s},{h} l{-s},{h}z" fill="{c}" {S}/>'
            f'<path d="M{x},{y} v{s} l{s},{h} v{-s}z" fill="{c}" {S} style="filter:brightness(.82)"/>'
            f'<path d="M{x+2*s},{y} v{s} l{-s},{h} v{-s}z" fill="{c}" {S} style="filter:brightness(.66)"/>')
def gear(cx,cy,r,c):
    import math
    pts=[];n=8
    for i in range(n*2):
        a=math.pi*i/n;rr=r if i%2==0 else r*.78
        for d in (-.18,.18):pts.append(f"{cx+rr*math.cos(a+d):.1f},{cy+rr*math.sin(a+d):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{c}" {S}/><circle cx="{cx}" cy="{cy}" r="{r*.3}" fill="{CREAM}" {S}/>'
def spark(cx,cy,r,c):return f'<path d="M{cx},{cy-r} Q{cx},{cy} {cx+r},{cy} Q{cx},{cy} {cx},{cy+r} Q{cx},{cy} {cx-r},{cy} Q{cx},{cy} {cx},{cy-r}z" fill="{c}" {S}/>'
def dots(c="#00000014"):return f'<pattern id="d" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="{c}"/></pattern><rect width="320" height="200" fill="url(#d)"/>'
def frame(bg,body):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" role="img" aria-hidden="true"><rect width="320" height="200" rx="18" fill="{bg}"/>{dots()}{body}</svg>'
def screen(x,y,w,h,c):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c}" {S}/><rect x="{x+10}" y="{y+10}" width="{w-20}" height="{h-28}" rx="5" fill="{CREAM}" {S}/>'
ART={
"hero":frame(P["mustard"],screen(40,40,150,110,P["plum"])+'<path d="M70 95 l20 -16 l20 16 l20 -24 l20 24" fill="none" '+S+'/>'+cube(200,110,26,P["tomato"])+cube(226,84,26,P["teal"])+cube(252,110,26,P["sky"])+spark(270,40,14,CREAM)+gear(120,165,16,P["leaf"])),
"ai":frame(P["plum"],screen(60,45,140,100,P["mustard"])+f'<text x="85" y="100" font-family="monospace" font-size="20" font-weight="700" fill="{INK}">&gt; make_</text>'+spark(240,70,26,P["mustard"])+spark(275,130,14,CREAM)+spark(220,145,10,P["pink"])),
"engine":frame(P["sky"],gear(120,100,52,P["mustard"])+gear(205,80,32,P["tomato"])+gear(225,145,22,P["teal"])),
"art":frame(P["tomato"],f'<path d="M80 150 q-30 -60 40 -90 q80 -30 110 30 q15 40 -30 40 q-20 0 -15 20 q5 25 -40 20 q-50 -5 -65 -20z" fill="{CREAM}" {S}/>'+"".join(f'<circle cx="{x}" cy="{y}" r="10" fill="{c}" {S}/>' for x,y,c in [(120,85,P["plum"]),(160,75,P["teal"]),(200,95,P["mustard"]),(115,125,P["sky"])])+f'<path d="M240 40 l-60 80" stroke="{INK}" stroke-width="8" stroke-linecap="round"/><path d="M240 40 l-60 80" stroke="{P["mustard"]}" stroke-width="4" stroke-linecap="round"/>'),
"audio":frame(P["teal"],"".join(f'<rect x="{50+i*24}" y="{100-h}" width="14" height="{2*h}" rx="7" fill="{c}" {S}/>' for i,(h,c) in enumerate([(20,P["mustard"]),(40,CREAM),(60,P["tomato"]),(35,CREAM),(50,P["plum"]),(25,CREAM),(45,P["mustard"]),(15,CREAM),(30,P["pink"])]))+f'<path d="M270 50 v70" {S}/><circle cx="258" cy="125" r="13" fill="{P["mustard"]}" {S}/><path d="M270 50 q18 8 18 28" fill="none" {S}/>'),
"kids":frame(P["mustard"],cube(70,120,30,P["tomato"])+cube(130,120,30,P["sky"])+cube(100,90,30,P["leaf"])+cube(190,120,30,P["plum"])+f'<circle cx="255" cy="55" r="22" fill="{CREAM}" {S}/><circle cx="248" cy="52" r="3" fill="{INK}"/><circle cx="262" cy="52" r="3" fill="{INK}"/><path d="M247 62 q8 7 16 0" fill="none" {S}/>'),
"vr":frame(P["pink"],f'<rect x="70" y="70" width="180" height="70" rx="30" fill="{P["plum"]}" {S}/><rect x="88" y="84" width="62" height="42" rx="18" fill="{P["sky"]}" {S}/><rect x="170" y="84" width="62" height="42" rx="18" fill="{P["sky"]}" {S}/><path d="M150 140 q10 -14 20 0" fill="{P["pink"]}" {S}/>'+spark(270,45,12,CREAM)+spark(50,50,9,P["mustard"])),
"publish":frame(P["leaf"],f'<path d="M160 30 q40 40 25 100 h-50 q-15 -60 25 -100z" fill="{CREAM}" {S}/><circle cx="160" cy="80" r="12" fill="{P["sky"]}" {S}/><path d="M135 130 l-20 25 l25 -8z M185 130 l20 25 l-25 -8z" fill="{P["tomato"]}" {S}/><path d="M148 135 q12 40 24 0" fill="{P["mustard"]}" {S}/>'+spark(60,60,10,CREAM)+spark(260,150,12,P["mustard"])),
"learn":frame(P["stone"],f'<path d="M60 60 q50 -15 100 5 v95 q-50 -20 -100 -5z" fill="{CREAM}" {S}/><path d="M160 65 q50 -20 100 -5 v95 q-50 -15 -100 5z" fill="{P["mustard"]}" {S}/>'+"".join(f'<path d="M75 {80+i*15} q35 -8 70 3" fill="none" {S} stroke-width="2"/>' for i in range(4))),
"first-game-this-weekend":frame(P["sky"],screen(90,40,140,100,P["tomato"])+f'<rect x="140" y="80" width="14" height="14" fill="{P["mustard"]}" {S}/><path d="M110 110 h100" {S}/><circle cx="185" cy="70" r="6" fill="{P["plum"]}" {S}/>'+spark(260,50,14,CREAM)+f'<text x="40" y="180" font-family="monospace" font-size="16" font-weight="700" fill="{INK}">SAT · SUN</text>'),
"vibe-coded-to-steam":frame(P["plum"],screen(30,50,120,90,P["mustard"])+f'<path d="M160 95 h40" {S} stroke-width="5"/><path d="M190 83 l14 12 l-14 12" fill="none" {S} stroke-width="5"/>'+f'<path d="M260 40 q30 30 18 75 h-36 q-12 -45 18 -75z" fill="{CREAM}" {S}/><circle cx="260" cy="75" r="9" fill="{P["sky"]}" {S}/>'+spark(70,170,10,CREAM)),
"blender-to-godot-3d":frame(P["tomato"],cube(60,95,34,P["mustard"])+f'<path d="M150 100 h30" {S} stroke-width="5"/><path d="M172 88 l14 12 l-14 12" fill="none" {S} stroke-width="5"/>'+cube(200,95,34,P["sky"])+f'<circle cx="234" cy="70" r="7" fill="{CREAM}" {S}/>'),
"kids-game-making":frame(P["leaf"],"".join(f'<rect x="{x}" y="{y}" width="70" height="26" rx="6" fill="{c}" {S}/>' for x,y,c in [(50,50,P["mustard"]),(70,82,P["tomato"]),(70,114,P["sky"]),(50,146,P["plum"])])+f'<path d="M210 140 l20 -50 l20 50z" fill="{P["mustard"]}" {S}/><circle cx="230" cy="70" r="16" fill="{CREAM}" {S}/>'),
"showcase":frame(P["tomato"],f'<rect x="60" y="55" width="200" height="90" rx="40" fill="{CREAM}" {S}/><circle cx="110" cy="100" r="18" fill="{P["plum"]}" {S}/><path d="M110 88 v24 M98 100 h24" stroke="{CREAM}" stroke-width="5" stroke-linecap="round"/><circle cx="205" cy="90" r="9" fill="{P["mustard"]}" {S}/><circle cx="225" cy="110" r="9" fill="{P["teal"]}" {S}/>'+spark(270,40,14,P["mustard"])+spark(50,160,10,CREAM)),
}
def logo(h=34):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" height="{h}" aria-hidden="true">'
            f'<rect x="3" y="15" width="16" height="16" rx="3" fill="{P["tomato"]}" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="21" y="15" width="16" height="16" rx="3" fill="{P["teal"]}" stroke="{INK}" stroke-width="2.5"/>'
            f'<rect x="12" y="3" width="16" height="13" rx="3" fill="{P["mustard"]}" stroke="{INK}" stroke-width="2.5"/>'
            f'<circle cx="11" cy="23" r="2" fill="{INK}"/><circle cx="29" cy="23" r="2" fill="{INK}"/></svg>')
