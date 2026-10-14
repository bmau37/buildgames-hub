# Source for data/paths.json — Pathfinder templates. Run: python3 _build/paths_src.py
import json,pathlib
P=[]
def t(id,title,kw,dim,stack,idea,proto,art,sound,polish,tut,vids,prompt,times=("30 min","2–6 h","1–3 h","30–60 min","1–3 h","30–60 min"),publish=None):
    P.append(dict(id=id,title=title,keywords=kw,dim=dim,stack=stack,tutorial=tut,video_types=vids,prompt=prompt,
      steps=[dict(phase="Idea",text=idea,time=times[0]),dict(phase="Prototype",text=proto,time=times[1]),dict(phase="Art",text=art,time=times[2]),
             dict(phase="Sound",text=sound,time=times[3]),dict(phase="Polish",text=polish,time=times[4]),
             dict(phase="Publish",text=publish or "Export a web build and upload it to itch.io; share the link and collect feedback.",time=times[5])]))
S=lambda k,te,a:{"kids":k,"teens":te,"adults":a}
t("platformer","2D platformer",["platformer","platform","jump","jumping","mario","side scroller","sidescroller","metroidvania","celeste"],"2d",
  S(["scratch","gdevelop","super-mario-maker-2"],["godot-engine","gamemaker","aseprite"],["godot-engine","aseprite","bfxr-jsfxr"]),
  "Pick one twist on run-and-jump (double jump, wall cling, gravity flip) and sketch 3 levels.","Get the character running and jumping with good feel, then block out one level with simple tiles.",
  "Draw a 16×16 or 32×32 hero and a tileset with a limited palette.","Jump, coin, hurt and a short music loop.","Coyote time, jump buffering, camera smoothing, checkpoints.","godot-2d-platformer",["platformer"],
  "a 2D side-scrolling platformer where {desc}. Include running, jumping with coyote time, collectible coins, hazards, checkpoints, a win flag and a restart key.")
t("puzzle","Falling-block / match puzzle",["puzzle","tetris","falling block","match 3","match-3","candy","sliding","sokoban","2048","block puzzle","junktris"],"2d",
  S(["scratch","microsoft-makecode-arcade"],["godot-engine","gdevelop","chatgpt"],["claude","godot-engine","phaser"]),
  "Define the grid, the pieces and the one rule that makes your puzzle different.","Build the grid logic first (spawn, move, rotate, clear) with plain shapes.",
  "Readable, high-contrast pieces; colour-blind-friendly shapes or patterns.","Satisfying clear sounds that rise in pitch with combos.","Next-piece preview, ghost piece, difficulty ramp, saved best score.","single-file-html-game-with-ai",["puzzle","html-vibe"],
  "a puzzle game where {desc}. Use a grid, clear rules, a next-piece preview, rising difficulty, score and best score in localStorage, keyboard and touch controls.")
t("endless-runner","Endless runner",["endless runner","runner","flappy","dino","temple run","subway","auto run"],"2d",
  S(["scratch","gdevelop"],["godot-engine","unity","gdevelop"],["godot-engine","unity"]),
  "Choose the one-button action (jump, flap, switch lane) and what makes runs different.","Auto-scroll the world, spawn obstacles randomly, end the run on collision.",
  "Parallax background layers sell speed cheaply.","Tap/jump sound and a fast music loop.","Speed ramp, near-miss bonus, instant restart.","unity-first-3d-game",["endless-runner","mobile-casual"],
  "an endless runner where {desc}. One-button controls, procedurally spawned obstacles, speed that ramps up, distance score, instant restart.")
t("top-down-shooter","Top-down shooter / arena survivor",["shooter","shoot","top down","top-down","bullet","twin stick","survivor","vampire survivors","shmup","space shooter","asteroids"],"2d",
  S(["microsoft-makecode-arcade","scratch"],["godot-engine","pico-8","aseprite"],["godot-engine","unity","aseprite"]),
  "Decide the fantasy (space, zombies, magic) and the upgrade hook.","Player movement, aiming, bullets and one enemy type that chases.",
  "Small sprites with strong silhouettes; bright bullets.","Punchy shoot and hit sounds; screen shake.","Waves, upgrades, hit-stop, enemy variety.","godot-2d-platformer",["top-down-shooter"],
  "a top-down shooter where {desc}. WASD/arrow movement, mouse or auto-aim shooting, enemy waves, health, simple upgrades between waves.")
t("rpg","RPG / adventure",["rpg","role playing","role-playing","quest","pokemon","zelda","dungeon","jrpg","adventure","turn based","turn-based"],"2d",
  S(["scratch","bitsy"],["rpg-maker-mz","godot-engine","gamemaker"],["godot-engine","rpg-maker-mz","tiled"]),
  "Write a one-page story, 3 locations and one core mechanic (combat, dialogue or exploration).","Tile map you can walk around, one NPC conversation and one battle or puzzle.",
  "Tileset + character sprites; keep the palette consistent.","Town and battle music loops; menu clicks.","Save system, inventory, balancing, a satisfying ending.","pixel-art-basics",["rpg"],
  "a small top-down RPG where {desc}. Tile-based movement, NPC dialogue, one quest, a simple inventory and a short ending.",times=("1 h","1–2 days","1–2 days","1–3 h","1–2 days","1 h"))
t("story","Visual novel / story game",["story","visual novel","narrative","choose your own","choices","dating sim","interactive fiction","book","writing"],"2d",
  S(["twine","bitsy"],["twine","ren-py"],["ren-py","twine","krita"]),
  "Outline characters, a central choice and 2–3 endings.","Write the branching script with placeholder art.",
  "Character portraits and a few backgrounds (Krita is free).","Ambient music and soft UI sounds.","Typography, pacing, save/load, accessibility options.","twine-story-game",["story"],
  "an interactive story game where {desc}. Show text with choices, track variables that change later scenes, and include at least three endings.")
t("idle","Idle / clicker",["idle","clicker","incremental","cookie","tycoon","tap"],"2d",
  S(["scratch"],["gdevelop","chatgpt","godot-engine"],["claude","phaser","godot-engine"]),
  "Choose the theme and the first 5 upgrades.","Click to earn, buy generators, numbers go up over time.",
  "Icons for each upgrade; satisfying button states.","Soft clicks and milestone chimes.","Offline progress, number formatting (1.2K, 3.4M), prestige.","single-file-html-game-with-ai",["html-vibe","idle"],
  "an idle clicker game where {desc}. Click to earn, upgrades and auto-generators, big-number formatting, saving to localStorage and offline progress.")
t("card","Card / deckbuilder",["card","cards","deck","deckbuilder","deck builder","slay the spire","solitaire","poker","hearthstone","tcg","board game","chess","checkers","board"],"2d",
  S(["scratch"],["godot-engine","twine"],["godot-engine","unity"]),
  "Prototype on paper with index cards first — fun on paper is fun on screen.","Draw/discard/play loop and one enemy.",
  "Card frames and icons; readability beats detail.","Card shuffle and play sounds.","Card balance, tooltips, animations.","single-file-html-game-with-ai",["any"],
  "a single-player card game where {desc}. Deck, hand, discard pile, energy per turn, one enemy with intents, and a short run of 3 fights.")
t("tower-defense","Tower defense",["tower defense","tower defence","td","defend","bloons","waves"],"2d",
  S(["scratch"],["godot-engine","unity"],["godot-engine","unity"]),
  "Map shape, 3 tower types and what makes enemies different.","Enemies follow a path; towers target and shoot; lives and money.",
  "Clear tower silhouettes and range circles.","Shots, hits, wave-start horn.","Upgrades, wave balancing, speed-up button.","godot-2d-platformer",["tower-defense"],
  "a tower defense game where {desc}. Enemies follow a path in waves; place 3 tower types with different strengths; money, lives, upgrades.")
t("racing","Racing",["racing","race","racer","kart","car","cars","driving","drift","mario kart"],"3d",
  S(["roblox-studio","scratch"],["roblox-studio","unity","godot-engine"],["unity","godot-engine","blender"]),
  "Arcade or sim? Pick tracks, a boost mechanic and number of players.","Car controller with good feel on a test track.",
  "Low-poly cars and track pieces in Blender or kit assets.","Engine loop that rises with speed, crash and boost sounds.","Lap timer, AI opponents, ghosts, camera polish.","unity-first-3d-game",["3d-adventure"],
  "a simple arcade racing game where {desc}. A track with laps, a car with acceleration/steering/drift, a lap timer and a finish screen.")
t("horror","Horror",["horror","scary","spooky","creepy","haunted","ghost","fnaf","backrooms","psychological"],"3d",
  S(["scratch"],["godot-engine","unity","blender"],["unity","godot-engine","blender"]),
  "One location, one threat, one mechanic (flashlight battery, hiding, sound).","First-person controller in a dark blockout level; a simple chasing threat.",
  "Low-poly or PS1-style models; lighting does most of the work.","Ambient drones and sudden sounds carry horror.","Pacing, fog, lighting, a memorable ending.","unity-first-3d-game",["horror","fps"],
  "a short first-person horror game where {desc}. Dark environment, flashlight with battery, a threat that reacts to noise, and an exit to escape.")
t("fps","First-person shooter",["fps","first person","first-person","shooter 3d","doom","call of duty","counter strike","arena shooter"],"3d",
  S(["roblox-studio"],["godot-engine","unity","roblox-studio"],["unreal-engine","unity","godot-engine"]),
  "Arena or levels? Pick 2 weapons and 2 enemy types.","FPS controller, hitscan weapon, one enemy AI.",
  "Weapon model and simple enemies (Blender).","Gunshots, impacts, footsteps.","Recoil, hit markers, level flow.","unity-first-3d-game",["fps"],
  "a small first-person shooter where {desc}. FPS movement, one hitscan weapon, enemies that chase and shoot, health pickups, a win condition.")
t("survival","Survival crafting",["survival","crafting","craft","minecraft","sandbox survival","base building","gather","valheim"],"3d",
  S(["roblox-studio","scratch"],["godot-engine","roblox-studio","unity"],["unity","godot-engine","blender"]),
  "Pick the world and the 3 resources everything is built from.","Gather, craft, hunger/health, day–night cycle.",
  "Voxel or low-poly assets (MagicaVoxel, Blender).","Chopping, crafting, ambient night sounds.","Progression, building, saving.","blender-low-poly-to-godot",["3d-adventure"],
  "a small survival crafting game where {desc}. Gather resources, craft tools from recipes, hunger and health, a day-night cycle with danger at night.",times=("1 h","1–3 days","1–2 days","1–3 h","1–3 days","1 h"))
t("city-builder","City builder / strategy",["city builder","city","builder","strategy","rts","simcity","colony","management","tycoon city"],"2d",
  S(["scratch"],["godot-engine","gdevelop"],["godot-engine","unity"]),
  "Choose the constraint (space, water, happiness) that makes choices matter.","Grid placement, resource ticks, one building chain.",
  "Isometric or top-down tiles; clear building icons.","Construction and ambient sounds.","UI clarity, balancing, goals.","godot-2d-platformer",["city-builder"],
  "a small city builder where {desc}. Grid placement of buildings, resources that tick over time, one production chain and a population goal.")
t("farming","Farming / cozy sim",["farming","farm","cozy","stardew","harvest","garden","animal crossing","life sim"],"2d",
  S(["scratch"],["godot-engine","gamemaker","aseprite"],["godot-engine","aseprite","tiled"]),
  "Seasons, crops and one relationship or shop loop.","Till, plant, water, grow over days, sell.",
  "Cosy pixel art with a warm palette.","Gentle music, tool sounds.","Calendar, upgrades, saving.","pixel-art-basics",["rpg"],
  "a cozy farming game where {desc}. Till, plant, water and harvest crops that grow over in-game days; sell produce; buy upgrades; save progress.")
t("rhythm","Rhythm / music game",["rhythm","music game","beat","guitar hero","dance","osu","piano"],"2d",
  S(["scratch"],["godot-engine","gdevelop"],["godot-engine","unity"]),
  "One song, one input style (4 lanes, one button, mouse).","Notes spawn on beat; judge timing windows.",
  "High-contrast lanes and hit effects.","Use a track you have the rights to (make your own in Bosca Ceoil).","Calibration offset, combo, results screen.","free-game-sound",["sound"],
  "a rhythm game where {desc}. Notes in 4 lanes synced to a song's BPM, timing judgement (perfect/good/miss), combo and a results screen.")
t("fighting","Fighting game",["fighting","fighter","fight","brawler","street fighter","smash","beat em up","beat 'em up"],"2d",
  S(["scratch"],["godot-engine","gamemaker"],["godot-engine","gamemaker","aseprite"]),
  "Two characters, 4 moves each, and local two-player.","Movement, hitboxes/hurtboxes, health bars.",
  "Big readable sprites; animation frames matter.","Impactful hit sounds and announcer text.","Hit-stop, combos, balance, a CPU opponent.","pixel-art-basics",["any"],
  "a 2-player local fighting game where {desc}. Two characters with light/heavy/special attacks, hitboxes, blocking, health bars and best-of-3 rounds.")
t("party","Party / local multiplayer",["party","local multiplayer","co-op","coop","couch","minigame","minigames"],"2d",
  S(["roblox-studio","scratch"],["roblox-studio","godot-engine"],["godot-engine","unity","roblox-studio"]),
  "Short rounds, simple controls, chaos that's funny.","Shared-screen or split controls for 2–4 players; one minigame.",
  "Distinct colours per player.","Loud, silly feedback sounds.","Round timer, scoreboard, more minigames.","roblox-obby",["party","obby"],
  "a local multiplayer party game where {desc}. 2–4 players on one keyboard/gamepads, 60-second rounds, a scoreboard and 3 minigames.")
t("obby","Roblox obby",["obby","obstacle course","parkour"],"3d",
  S(["roblox-studio"],["roblox-studio"],["roblox-studio"]),
  "Theme and 5 stages of increasing difficulty.","Parts, kill bricks, checkpoints.",
  "Colour each stage; use Studio's materials.","Background music from the Creator Store (check licensing).","Moving platforms, timer, leaderboard.","roblox-obby",["obby"],
  "a Roblox obby where {desc}. Write Luau scripts for kill bricks, checkpoints that save progress per player, moving platforms using TweenService and a stage counter.",publish="Publish from Roblox Studio; review the current Creator Hub rules for your age and audience.")
t("uefn","Fortnite island (UEFN)",["fortnite","uefn","creative","island","verse"],"3d",
  S(["super-mario-maker-2"],["uefn-unreal-editor-for-fortnite"],["uefn-unreal-editor-for-fortnite"]),
  "One mode (race, box fight, deathrun) with clear rules.","Block out in UEFN with devices; script with Verse if needed.",
  "Use Fortnite's built-in assets and galleries.","Built-in music and SFX devices.","Playtest sessions, balance, thumbnail.","godot-2d-platformer",["uefn"],
  "a Fortnite UEFN island where {desc}. Suggest which Creative devices to use and write any needed Verse code with comments.",publish="Publishing through the Fortnite Developer Program requires a legal adult; minors can build and playtest privately.")
t("vr","VR game for Quest",["vr","virtual reality","quest","oculus","meta quest","headset","xr","mixed reality"],"3d",
  S(["roblox-studio"],["unity","meta-xr-sdk-unity"],["unity","meta-xr-sdk-unity","blender"]),
  "One interaction that's only fun in VR (grab, throw, climb).","XR rig, hands/controllers, grab interactions in a small room.",
  "Low-poly, performance-friendly assets.","Spatial audio for objects.","Comfort options (snap turn, vignette), 72+ fps.","unity-first-3d-game",["vr"],
  "a short VR game for Meta Quest in Unity where {desc}. Use the XR Interaction Toolkit or Meta XR SDK, grab/throw interactions, snap turning and a comfort vignette.",publish="Share a test build via Meta's developer tools or SideQuest; store publishing needs an adult developer account.")
t("mobile-casual","Mobile casual",["mobile","phone","iphone","android","ios","tablet","hyper casual","hypercasual","casual","app store","play store"],"2d",
  S(["gdevelop","scratch"],["gdevelop","godot-engine","chatgpt"],["godot-engine","unity","claude"]),
  "One-thumb control and a 30-second loop.","Portrait layout, touch input, quick restart.",
  "Big, bold shapes that read on small screens.","Short, light sounds; respect the mute switch.","Haptics, juice, performance on older phones.","single-file-html-game-with-ai",["mobile-casual"],
  "a portrait mobile casual game where {desc}. One-thumb touch controls, 30-second rounds, big readable UI, best score, works offline.",
  publish="Test as a web game first; Google Play needs a US$25 developer account and Apple a US$99/year membership (adults).")
t("text-adventure","Text adventure / Twine",["text adventure","text","twine","zork","parser","choose","adventure text"],"2d",
  S(["twine","bitsy"],["twine"],["twine","ren-py"]),
  "Setting, goal and a map of 6–10 rooms.","Write passages with links and variables.",
  "Optional: a colour scheme and a few images.","Optional ambient audio.","Proofread, test every branch.","twine-story-game",["story"],
  "a text adventure in Twine (Harlowe) where {desc}. Rooms as passages, an inventory using variables, a locked door puzzle and two endings.")
t("educational","Educational / quiz",["educational","education","learning","quiz","math","spelling","school","teach","trivia","classroom"],"2d",
  S(["scratch","microsoft-makecode-arcade","minecraft-education"],["scratch","gdevelop","twine"],["godot-engine","chatgpt","construct-3"]),
  "One learning goal and how the game checks it.","Question loop with feedback and a score.",
  "Friendly characters and clear fonts.","Positive feedback sounds.","Difficulty levels, progress tracking.","scratch-first-game-kids",["educational"],
  "an educational game where {desc}. Questions with immediate friendly feedback, difficulty that adapts, a score and a progress screen.")
t("physics-sandbox","Physics sandbox / puzzle",["physics","sandbox","ragdoll","angry birds","bridge","contraption","destruction","build","building"],"2d",
  S(["scratch","roblox-studio"],["godot-engine","unity"],["godot-engine","unity"]),
  "Pick the physics toy (launch, stack, build, break).","Rigid bodies, joints, one goal per level.",
  "Simple shapes; let physics be the star.","Impact sounds scaled by speed.","Level set, undo, replays.","unity-first-3d-game",["physics-sandbox"],
  "a 2D physics puzzle game where {desc}. Use rigid bodies and joints, 5 levels with a clear goal each, a reset button and stars for efficiency.")
t("html-vibe","AI vibe-coded single-file HTML game",["ai","vibe","vibe code","vibe-coded","vibe coding","chatgpt","claude","grok","gemini","html","browser","web","single file","prompt","codex","cursor"],"2d",
  S(["scratch"],["chatgpt","grok","github-pages"],["claude","chatgpt","claude-code"]),
  "Write a 5-sentence design brief: controls, goal, lose condition, look, devices.","Prompt for one self-contained index.html; fix errors by pasting them back.",
  "Ask for canvas-drawn art or add a few CC0 sprites.","Ask for Web Audio sound effects synthesized in code.","Iterate in saved versions (v1, v2…), test on a phone.","single-file-html-game-with-ai",["html-vibe"],
  "{desc}. Build it as ONE self-contained index.html (inline CSS/JS, no external assets), with keyboard and touch controls, a title screen, score and restart.",
  times=("20 min","1–2 h","30–60 min","20 min","1–3 h","20 min"),publish="Host on GitHub Pages or itch.io; later wrap as an installable web app or Android app.")
t("3d-adventure","3D adventure / platformer",["3d","3d platformer","open world","explore","exploration","adventure 3d","mario 64","zelda 3d","third person"],"3d",
  S(["roblox-studio"],["godot-engine","unity","blender"],["godot-engine","unity","unreal-engine"]),
  "One hub, two areas, one ability that opens new paths.","Third-person controller and camera; block out with simple shapes.",
  "Low-poly models from Blender; consistent scale.","Footsteps, ambient loops, collect jingle.","Camera polish, checkpoints, lighting.","blender-low-poly-to-godot",["3d-adventure","3d-art"],
  "a small 3D third-person adventure where {desc}. Character controller with jump, an orbiting camera, collectibles, one locked area and a goal.")
t("kids-game","Game for or with a kid",["kid","kids","child","my son","my daughter","family","simple","easy","young","children","grandkid"],"2d",
  S(["scratch","super-mario-maker-2","microsoft-makecode-arcade"],["scratch","gdevelop"],["scratch","bitsy","twine"]),
  "Draw the hero and goal on paper together.","Make the hero move and one thing to catch or avoid.",
  "Let the kid draw the sprites (paint editor or paper photo).","Record silly sounds together.","Add a title screen with their name.","make-a-game-with-your-kid",["kids-game","educational"],
  "a very simple, kid-friendly game where {desc}. Big colorful shapes, arrow-key or tap controls, gentle difficulty, no fail state that feels harsh.",publish="Share privately with family first; use parent-managed accounts for any online sharing.")
pathlib.Path(__file__).resolve().parent.parent.joinpath("data/paths.json").write_text(json.dumps(P,indent=1,ensure_ascii=False));print(len(P))
