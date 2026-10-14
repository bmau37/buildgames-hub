# Source for data/tutorials.json (original writing). Run: python3 _build/tutorials_src.py
import json,pathlib
T=[]
def tut(**k):T.append(k)
tut(slug="single-file-html-game-with-ai",title="Make a single-file HTML game with Claude, ChatGPT or Grok",
summary="Describe a game, get one HTML file you can open in any browser, then improve it version by version — the approach behind Junktris.",
time="2–4 hours for a first playable",ages=["teens","adults"],skill="beginner",tools=["claude","chatgpt","grok","github-pages","itch-io"],
videos=["DHjqpvDnNGE","3EMxBkqC4z0","jHTRu4iNTcA"],next="publish-on-itch",
checklist=["Wrote a one-paragraph game description","Got a single index.html that runs offline","Saved each working version (v1, v2, …)","Tested on a phone browser","Shared a link with one friend"],
body="""A single HTML file can hold a whole game: the page, the styles, the code and even synthesized sound. Because there's nothing to install, it's the fastest way to go from idea to something you can play, and AI assistants are very good at writing this kind of file.

> **Age note:** Claude requires users to be 18+. ChatGPT and Grok require 13+ with a parent's permission for under-18s. Younger makers should have an adult drive the AI.

## 1. Write a tiny design brief
Before you prompt, write 4–6 sentences: what the player controls, the goal, how you lose, the controls (keyboard and touch), and the look. Small and specific beats big and vague.

```text
Make a complete browser game in ONE self-contained index.html file (inline CSS and JS, no external libraries or assets).
Game: a falling-block puzzle where the pieces are pieces of junk loaded into a truck.
Controls: arrow keys on desktop; on-screen buttons for rotate, left, right and drop on phones.
Rules: fill a row to clear it; game over when the stack reaches the top. Show score and a restart button.
Style: chunky, colorful, readable on a 390px-wide phone. Draw everything with canvas shapes.
```

## 2. Get version 1 running
Paste the brief into Claude, ChatGPT or Grok. Save the reply as `index.html` and double-click it to open it in your browser. If it doesn't run, open the browser's developer console (F12), copy the red error message and paste it back: *"I get this error: … please fix and return the full file."*

## 3. Iterate in small, saved steps
Change one thing per round: "make pieces fall 20% slower", "add a next-piece preview", "add a pause button". After every round that works, **save a copy** (`v2.html`, `v3.html` …). Junktris went through roughly 60 versions this way, keeping a known-good build (V58) untouched as a safe baseline before further changes. If a new version breaks things, you can always go back.

Tips that save time:
- Ask for the **full file** every time, not fragments, so you never have to merge code by hand.
- When the file gets long, ask the AI to change only one named function and return the whole file.
- Describe bugs like a tester: what you did, what you expected, what happened.

## 4. Make it feel good
Ask for "juice": a short screen shake on a line clear, simple sound effects made with the Web Audio API, a best-score saved in `localStorage`, and a title screen. Test on your phone: tap targets should be at least the size of a fingertip.

## 5. Share it
Upload the single file to itch.io as an HTML game (see the itch.io tutorial) or publish it free with GitHub Pages. Later, the same file can be wrapped as an installable web app or an Android app, which is how Junktris is being prepared for Google Play.

## Prompt kit
- "Explain how the game loop in this file works, in plain English."
- "Add touch controls that don't block the board on a small phone."
- "List 5 ways to make this game more fun without adding new screens."
""")
tut(slug="godot-2d-platformer",title="Your first Godot 2D platformer",
summary="Build a running, jumping character, a level made of tiles and a goal flag in Godot 4 — free and open source.",
time="3–5 hours",ages=["teens","adults"],skill="beginner",tools=["godot-engine","kenney-assets","aseprite"],
videos=["LOhfqjmasi0","e1zJS31tr88","WEt2JHEe-do"],next="pixel-art-basics",
checklist=["Installed Godot 4","Player moves and jumps","Level built with a TileMapLayer","Falling off restarts the level","Reaching the flag shows 'You win!'"],
body="""Godot is a free, MIT-licensed engine. Its scripting language, GDScript, reads a lot like Python.

## 1. Set up
Download Godot 4 from godotengine.org (no account needed) and create a new project. Grab a free CC0 platformer pack from kenney.nl so you have tiles and a character right away.

## 2. Make the player
Create a new scene with a **CharacterBody2D** root named `Player`. Add a **Sprite2D** (drag in your character image) and a **CollisionShape2D** with a capsule or rectangle shape. Attach a script — Godot offers a *Basic Movement* template that looks like this:

```gdscript
extends CharacterBody2D

const SPEED = 300.0
const JUMP_VELOCITY = -400.0

func _physics_process(delta):
    if not is_on_floor():
        velocity += get_gravity() * delta
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = JUMP_VELOCITY
    var direction := Input.get_axis("ui_left", "ui_right")
    if direction:
        velocity.x = direction * SPEED
    else:
        velocity.x = move_toward(velocity.x, 0, SPEED)
    move_and_slide()
```

Arrow keys move, Space/Enter jumps. Tweak `SPEED` and `JUMP_VELOCITY` until it feels right — this is the most important "game feel" step.

## 3. Build a level
Create a `Level` scene with a **Node2D** root. Add a **TileMapLayer**, create a TileSet from your tile image, and give the tiles a physics layer so the player can stand on them. Paint a few platforms. Instance your `Player` scene and add a **Camera2D** as a child of the player so the view follows.

## 4. Lose and win
Add an **Area2D** strip below the level. Connect its `body_entered` signal:

```gdscript
func _on_body_entered(body):
    if body.name == "Player":
        get_tree().reload_current_scene()
```

Add a flag with another Area2D whose signal shows a **Label** saying "You win!".

## 5. Polish and export
Add a jump sound (see the sound tutorial), a background colour, and a coin counter. Use *Project → Export* to make a Web build (download the export templates when Godot asks) and upload it to itch.io.
""")
tut(slug="scratch-first-game-kids",title="Scratch: a first game for kids",
summary="Make a 'catch the falling apples' game in Scratch with score and a timer — no typing, just blocks.",
time="45–90 minutes",ages=["kids","teens"],skill="beginner",tools=["scratch"],
videos=["7NN5v2wSL4U","1jHvXakt1qw","D16hTnDGweo"],next="make-a-game-with-your-kid",
checklist=["Bowl moves with arrow keys","Apple falls from a random spot","Score goes up when caught","Game ends after 30 seconds","Shared or saved the project"],
body="""Scratch is free from the MIT Media Lab and runs in a browser at scratch.mit.edu. You can start without an account; to save and share online, under-13s sign up with a parent's email.

## 1. Pick your sprites
Click **Create**. Delete the cat if you like, then choose a **Bowl** sprite and an **Apple** sprite from the library (or paint your own!). Pick a backdrop.

## 2. Move the bowl
Click the Bowl and build:
- `when green flag clicked` → `go to x: 0 y: -140` → `forever` → inside it: `if <key right arrow pressed> then change x by 10` and `if <key left arrow pressed> then change x by -10`.

## 3. Make the apple fall
Click the Apple:
- `when green flag clicked` → `go to x: (pick random -220 to 220) y: 180` → `forever` → `change y by -5`.
- Inside the forever, add `if <touching Bowl?> then` → `change score by 1` → `go to x: (pick random -220 to 220) y: 180`.
- Add another `if <(y position) < -170> then go to x: (pick random -220 to 220) y: 180` so missed apples come back.

Make the variable first: **Variables → Make a Variable → score**, and add `set score to 0` at the start.

## 4. Add a timer
On the Stage: `when green flag clicked` → `reset timer` → `wait until <(timer) > 30>` → `stop all`. Now it's a real challenge!

## 5. Make it yours
Ideas: a "pop" sound when you catch; apples fall faster as the score grows (`change y by (-5 - (score / 5))`); a golden apple worth 5 points; a "Game over" backdrop.

**Grown-ups:** let the child drive the mouse and make the choices. Ask "what should happen next?" more than you tell.
""")
tut(slug="roblox-obby",title="Build a Roblox obby with checkpoints",
summary="Make an obstacle course in Roblox Studio with kill bricks, moving parts and checkpoints that remember your progress.",
time="2–3 hours",ages=["kids","teens","adults"],skill="beginner",tools=["roblox-studio"],
videos=["9v3GvfX_qr8","Aa83VYif6VA","Ml934kVACbM"],next="pixel-art-basics",
checklist=["Built 10+ jumps","Kill bricks reset the player","Checkpoints remember progress","Playtested start to finish","Checked publishing rules for your age"],
body="""Roblox Studio is free on Windows and Mac. Anyone with a Roblox account can build; publishing to younger audiences has extra requirements (age check, 2-step verification), and under-18s need a parent's consent for payments.

## 1. Start from the Baseplate
Open Studio, choose **Baseplate**. Use the **Part** button to add blocks, and the Move/Scale/Rotate tools to shape jumps. Select parts and tick **Anchored** in Properties so they don't fall. Group your parts into a folder or Model called `Course`.

## 2. Kill bricks
Make a red part, add a **Script** inside it:

```lua
local part = script.Parent

part.Touched:Connect(function(hit)
	local humanoid = hit.Parent:FindFirstChild("Humanoid")
	if humanoid then
		humanoid.Health = 0
	end
end)
```

Copy that part around the course for lava floors.

## 3. Checkpoints
Make a Folder in Workspace called `Checkpoints` and put flat, anchored parts in it along the course. Add one **Script** in **ServerScriptService**:

```lua
local Players = game:GetService("Players")
local checkpoints = workspace:WaitForChild("Checkpoints")
local saved = {}

for _, cp in checkpoints:GetChildren() do
	cp.Touched:Connect(function(hit)
		local player = Players:GetPlayerFromCharacter(hit.Parent)
		if player then
			saved[player] = cp
		end
	end)
end

Players.PlayerAdded:Connect(function(player)
	player.CharacterAdded:Connect(function(character)
		local cp = saved[player]
		if cp then
			task.wait()
			character:PivotTo(cp.CFrame + Vector3.new(0, 4, 0))
		end
	end)
end)

Players.PlayerRemoving:Connect(function(player)
	saved[player] = nil
end)
```

## 4. Make it interesting
Use **TweenService** for moving platforms, add a spinning bar, vary jump widths, and give each stage its own colour. Press **Play** often and fix any jump that feels unfair.

## 5. Publish
*File → Publish to Roblox*. Read the current Creator Hub rules for who your game can reach and what you need — they depend on your age and your audience.
""")
tut(slug="blender-low-poly-to-godot",title="Blender low-poly asset to Godot",
summary="Model a simple low-poly tree, colour it, export it as glTF and drop it into a Godot 3D scene.",
time="1–2 hours",ages=["teens","adults"],skill="intermediate",tools=["blender","godot-engine"],
videos=["F_JK9eaYYTQ","-tbSCMbJA6o","ke5KpqcoiIU"],next="unity-first-3d-game",
checklist=["Modeled a trunk and leaves","Applied scale and rotation","Assigned 2 materials","Exported .glb","Placed it in a Godot scene with collision"],
body="""Blender and Godot are both free and open source, and glTF 2.0 is the format that moves models between them cleanly.

## 1. Model
In Blender, delete the default cube. Add a **Cylinder** (Shift+A → Mesh) with 8 vertices for the trunk and scale it tall. Add an **Ico Sphere** (subdivisions 1) for leaves and place it on top. Low poly is a style *and* a performance win.

## 2. Colour with materials
Select the trunk, open the Material tab, click **New**, set Base Color to brown. Do the same with green for the leaves. Flat colours avoid UV-unwrapping for now.

## 3. Clean up
Select both objects, press **Ctrl+A → All Transforms** so scale and rotation are applied. Put the base of the trunk at the origin (the 3D cursor helps). Join them with **Ctrl+J** if you want one object.

## 4. Export
*File → Export → glTF 2.0*. Choose **glTF Binary (.glb)**, tick *Selected Objects* if needed, and save into your Godot project folder.

## 5. Use it in Godot
Godot imports `.glb` automatically. Drag it into a 3D scene. To make it solid, open the imported scene's **Advanced Import Settings**, select the mesh and enable a collision shape (or add a StaticBody3D with a CollisionShape3D yourself). Add a DirectionalLight3D and WorldEnvironment, and you've got a forest in minutes by duplicating trees.

Tip: Godot 4 can also import `.blend` files directly if you set the Blender path in Editor Settings — handy for quick iteration.
""")
tut(slug="unity-first-3d-game",title="Unity: your first 3D game (roll-a-ball)",
summary="A ball you roll around a board collecting pickups — the classic first Unity project, using the Input System.",
time="2–3 hours",ages=["teens","adults"],skill="beginner",tools=["unity","unity-learn"],
videos=["_uO5B7bP9jo","XtQMytORBmM","IlKaB1etrik"],next="free-game-sound",
checklist=["Created a 3D project in Unity Hub","Ball moves with a Rigidbody","Pickups rotate and disappear","Score text shows count","Built and ran the game"],
body="""Unity Personal is free if your revenue and funding are under US$200K. Install **Unity Hub**, then a current Unity 6 version, and create a **Universal 3D** project.

## 1. Scene
Add a **Plane** (ground) and a **Sphere** (Player) above it. Add a **Rigidbody** to the sphere. Add a **Player Input** component to it (from the Input System package that new projects use) — it sends `OnMove` messages.

## 2. Player script
Create `PlayerController.cs` and attach it to the sphere:

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
    public float speed = 10f;
    private Rigidbody rb;
    private Vector2 move;

    void Start() { rb = GetComponent<Rigidbody>(); }

    void OnMove(InputValue value) { move = value.Get<Vector2>(); }

    void FixedUpdate()
    {
        rb.AddForce(new Vector3(move.x, 0f, move.y) * speed);
    }
}
```

## 3. Pickups
Add a small **Cube**, tick **Is Trigger** on its collider, tag it `PickUp`, and give it a script that rotates it in `Update` with `transform.Rotate(new Vector3(15, 30, 45) * Time.deltaTime);`. Make it a prefab and place a dozen.

Then add to `PlayerController`:

```csharp
private int count;

void OnTriggerEnter(Collider other)
{
    if (other.CompareTag("PickUp"))
    {
        other.gameObject.SetActive(false);
        count++;
    }
}
```

## 4. Camera and UI
Make the camera follow by storing its offset from the player and updating its position in `LateUpdate`. Add a **TextMeshPro** text to show `count`.

## 5. Build
*File → Build Profiles*, pick Windows/Mac or Web, and build. Unity Learn's free Roll-a-ball course goes deeper on every step.
""")
tut(slug="pixel-art-basics",title="Pixel art basics with Aseprite or Piskel",
summary="Draw and animate a 16×16 game character with a limited palette, then export a sprite sheet for any engine.",
time="1–2 hours",ages=["kids","teens","adults"],skill="beginner",tools=["aseprite","krita"],
videos=["59Y6OTzNrhk","WUlgvNe4BLU","GUEVPYlv474"],next="free-game-sound",
checklist=["Canvas 16×16 or 32×32","Palette of 4–8 colours","Readable silhouette","2–4 frame walk cycle","Exported a PNG sprite sheet"],
body="""You don't need to be "good at drawing" — pixel art is about clear shapes and few colours. **Aseprite** is a paid favourite; **Piskel** (piskelapp.com) is free and runs in the browser.

## 1. Small canvas, small palette
Start at **16×16** pixels. Pick 4–8 colours: an outline colour, two skin/fur tones, two clothing tones and one highlight. Limits make art look cohesive.

## 2. Silhouette first
Fill the body shape in one dark colour. Can you tell what it is from the shape alone? If not, exaggerate: bigger head, clear arms, a distinctive hat or ear.

## 3. Shade simply
Choose a light direction (top-left is classic). Add one lighter tone on lit sides, one darker tone underneath. Avoid "pillow shading" (darkening every edge equally).

## 4. Animate
Duplicate the frame 2–4 times. For a walk: shift legs apart, together, the other way, together. Move the body down one pixel on the "together" frames for bounce. Play it at ~8–10 frames per second.

## 5. Export
Aseprite: *File → Export Sprite Sheet* (horizontal strip, PNG). Piskel: *Export → PNG → Spritesheet*. Engines like Godot (AnimatedSprite2D), Unity (Sprite Editor) and GameMaker read these strips directly. Turn off texture filtering in your engine so pixels stay crisp.
""")
tut(slug="free-game-sound",title="Free game sound with jsfxr and Bosca Ceoil",
summary="Make jump, coin and explosion effects in seconds, then compose a short loop of background music — all free.",
time="1 hour",ages=["kids","teens","adults"],skill="beginner",tools=["bfxr-jsfxr","bosca-ceoil-blue","audacity"],
videos=["v51fDrZXh_I","yzJ2VyYkmaA"],next="publish-on-itch",
checklist=["Made jump, coin, hit sounds","Exported .wav files","Wrote a 4-bar music loop","Trimmed/normalized in Audacity","Volume balanced in game"],
body="""Sound is the cheapest way to make a game feel finished.

## 1. Sound effects with jsfxr
Open **sfxr.me** in a browser. Click the presets — **Pickup/Coin**, **Laser/Shoot**, **Explosion**, **Hit/Hurt**, **Jump** — until you like one. Use **Mutate** for variations and adjust *sustain* or *frequency* sliders. Click **Export .wav**. Sounds you make in sfxr are yours to use.

## 2. Music with Bosca Ceoil Blue
Download Bosca Ceoil Blue (free, open source). Pick an instrument, click notes into the grid to make a 1-bar pattern, then arrange patterns into a 4–8 bar loop. Add a bass line and drums on separate tracks. Keep it short and loopable. Export to WAV.

## 3. Tidy up in Audacity
Open each file in Audacity: trim silence at the start, use *Effect → Normalize* so volumes match, and export again. Convert music to OGG for smaller files in Godot or the web.

## 4. Use it well
- Play the jump sound on jump *start*, not landing.
- Vary pitch slightly each time (±5%) so repeated sounds don't grate.
- Keep music quieter than effects, and add a mute button.
""")
tut(slug="publish-on-itch",title="Publish your game on itch.io",
summary="Turn your build into a public game page that people can play in the browser or download — free.",
time="30–60 minutes",ages=["teens","adults"],skill="beginner",tools=["itch-io"],
videos=["XxeD_2nTyHI"],next="twine-story-game",
checklist=["Account created (13+; publishing 18+ or guardian consent)","Web build zipped with index.html at the root","Cover image 630×500","Description, controls and tags written","Page set to Public"],
body="""itch.io is the friendliest place to put your first game online. Users must be 13+, and publishers must be 18+ or have a parent/guardian's consent.

## 1. Prepare your build
For a browser game, make a **.zip** whose top level contains `index.html` (Godot, Unity, GameMaker, GDevelop and Construct all export Web builds; a single-file HTML game just needs zipping). For downloads, zip the Windows/Mac/Linux builds separately.

## 2. Create the project
On itch.io: *Dashboard → Create new project*. Fill in the title, a short tagline, and set **Kind of project** to *HTML* for browser games.

## 3. Upload
Upload your zip and tick **This file will be played in the browser**. Set the viewport size to match your game (e.g. 960×540, or a phone-shaped size), and enable the fullscreen button and mobile-friendly option if it works on phones.

## 4. Make the page appealing
Add a **cover image** (630×500), 3–5 screenshots, a GIF if you can, the controls, and tags (genre, engine, "made with Godot"). Choose pricing: free, paid or "name your own price".

## 5. Go public and share
Save as **Draft**, view it, test it, then switch to **Public**. Post the link to friends, a Discord community, or a game jam. Read every comment — that's your next version's to-do list.
""")
tut(slug="twine-story-game",title="Make a story game with Twine",
summary="Write a branching interactive story with choices, a remembered item and multiple endings — in your browser.",
time="1–2 hours",ages=["kids","teens","adults"],skill="beginner",tools=["twine"],
videos=[],next="make-a-game-with-your-kid",
checklist=["Opening passage written","At least 3 choices","A variable (item) remembered","2+ endings","Published to file and played"],
body="""Twine is free and open source. Open **twinery.org** and choose *Use it online* (stories save in your browser) or download the app. New stories use the **Harlowe** format by default.

## 1. Passages and links
Each box is a *passage*. Link with double square brackets:

```text
You wake up in a lighthouse. A storm rattles the windows.
[[Climb the stairs->Lamp Room]]
[[Go down to the cellar->Cellar]]
```

Twine automatically creates the passages you link to.

## 2. Remember things
Harlowe uses `(set:)` and `(if:)`:

```text
:: Cellar
You find a rusty key under a barrel.
(set: $hasKey to true)
[[Go back up->Start]]

:: Lamp Room
(if: $hasKey)[You unlock the lamp cabinet and light the beacon. [[Ships are saved!->Good Ending]]]
(else:)[The lamp cabinet is locked. [[Go back->Start]]]
```

(The `::` lines are just labels here — in Twine each is its own passage box.)

## 3. Endings and pacing
Write at least two endings. Keep passages short (2–5 sentences) and make every choice feel different.

## 4. Style
*Story → Details* lets you edit the stylesheet — try a dark background and a typewriter font.

## 5. Share
*Build → Publish to File* gives you one HTML file. Upload it to itch.io as an HTML game, and you're published.
""")
tut(slug="pico-8-first-cart",title="PICO-8: your first cart",
summary="Draw a sprite, move it with the arrow keys, add a collectible and a score inside the PICO-8 fantasy console.",
time="1–2 hours",ages=["teens","adults"],skill="beginner",tools=["pico-8"],
videos=["uXveyqOYB5w","frqf73ycQc0"],next="free-game-sound",
checklist=["Drew sprite 1","Player moves with arrows","Coin respawns when collected","Score printed on screen","Saved and exported as HTML"],
body="""PICO-8 (US$14.99, Lexaloffle) is a tiny "fantasy console" with a 128×128 screen, 16 colours, and built-in editors for code, sprites, maps and music. Its limits keep projects small and finishable.

## 1. Draw sprites
Press **Esc** to switch to the editor. In the sprite tab draw your hero in slot **1** and a coin in slot **2** (slot 0 is usually left empty).

## 2. Code
In the code tab (Lua):

```lua
function _init()
 x=60 y=60 score=0
 cx=flr(rnd(120)) cy=flr(rnd(120))
end

function _update()
 if btn(0) then x-=2 end
 if btn(1) then x+=2 end
 if btn(2) then y-=2 end
 if btn(3) then y+=2 end
 if abs(x-cx)<6 and abs(y-cy)<6 then
  score+=1 sfx(0)
  cx=flr(rnd(120)) cy=flr(rnd(120))
 end
end

function _draw()
 cls(1)
 spr(1,x,y)
 spr(2,cx,cy)
 print("score: "..score,2,2,7)
end
```

`_update` runs 30 times a second, `_draw` draws each frame. Press **Ctrl+R** to run.

## 3. Sound
In the SFX editor make sound 0 a short rising blip. That's what `sfx(0)` plays.

## 4. Grow it
Add a timer, an enemy that chases you (`x+=sgn(px-x)`), or a map with `map()`.

## 5. Save and share
`save mygame` saves a cart. `export mygame.html` creates a web build you can upload to itch.io; carts can also be shared on the Lexaloffle BBS.
""")
tut(slug="make-a-game-with-your-kid",title="Make a game with your kid",
summary="A parent's playbook: paper prototypes, the right first tool for each age, short sessions and how to keep it their game.",
time="Several 30–45 minute sessions",ages=["kids"],skill="beginner",tools=["scratch","microsoft-makecode-arcade","super-mario-maker-2","roblox-studio","bitsy"],
videos=["DE_-0flM324","7NN5v2wSL4U","1jHvXakt1qw"],next="scratch-first-game-kids",
checklist=["Drew the game on paper first","Kid chose the tool and the hero","Sessions kept under 45 minutes","Playtested with a family member","Celebrated a 'release'"],
body="""The goal isn't a perfect game — it's a kid who knows they can make things.

## 1. Start on paper (15 minutes)
Ask: *Who is the hero? What do they want? What's in the way?* Draw the screen together. Play it with a pencil and dice. This keeps the ideas theirs.

## 2. Pick a tool by age
- **Ages 5–8:** Super Mario Maker 2 or Game Builder Garage (Switch), or ScratchJr on a tablet — lots of reading-free building.
- **Ages 8–12:** Scratch or MakeCode Arcade in a browser. Both are free and need no install.
- **Roblox fans:** Roblox Studio works for building; review account settings, chat and the current publishing rules together.
- **Story lovers:** Bitsy or Twine for tiny narrative games.

## 3. Short sessions, one win each
Aim for one visible change per session: "the cat moves", "there's a score", "there's a sound". Stop while it's still fun.

## 4. Let them drive
Keep your hands off the mouse. Ask "what should happen?" and "how could we find out?" When they're stuck, look up a short official tutorial video together.

## 5. Safety basics
- Most AI chatbots are 13+ (ChatGPT, Grok) or 18+ (Claude); with younger kids, an adult should drive any AI help.
- Use parent-managed accounts and turn off or limit chat on platforms that have it.
- Remind them never to put real names, schools or photos in games they share.

## 6. Release day
Make a title screen with their name, play it at dinner, and if they want, share privately with family. Then ask: *what would you make next?*
""")
pathlib.Path(__file__).resolve().parent.parent.joinpath("data/tutorials.json").write_text(json.dumps(T,indent=1,ensure_ascii=False))
print(len(T))
