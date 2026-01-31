# STORYTELLER (cycle-01)

## Story promise (what the player is signing up for)
A cozy campfire flickers in a cave mouth. You step closer… and the dungeon politely asks what kind of weirdness you’d like tonight.

This is a **tap-to-choose**, **silly-ending**, text-forward dungeon crawl where the dungeon is less “ancient evil” and more “improvised theatre kid with a geology minor.”

## Tone rules
- Every branch gets at least **one sincere moment** (wonder, curiosity, relief) so the silliness lands harder.
- Endings are always **playful, unexpected, and definitive**.
- Choices read like buttons: short, punchy, action-oriented.

## Core structure (3 required themed paths + connective tissue)
We’ll present an early “hub” choice that forks cleanly into the 3 required paths, but we’ll also include cross-links so replay feels rewarding.

### Hub: Cave Entrance + Campfire (required opening)
The opening scene establishes:
- The cave mouth
- A small campfire inside
- A sense that the cave is “aware”

From the campfire the player sees three enticing options:
1. **A corridor of labeled stones** (mmpdb tutorial path)
2. **A star-slit crack in the rock** (cosmic eyeball node dimension)
3. **A smell of soup** (food/digestion revelation path)

## Story graph (node list)
Format suggestion: each node has `id`, `text`, and `choices` where each choice has `label` + `to`.

### ACT 0: THE THRESHOLD
**N0: ENTRANCE / CAMPFIRE**
Text beats:
- “A cave opens like a yawn.”
- “Inside: a campfire, already lit, as if expecting you.”
- A little sign stuck in the sand: “WELCOME, HERO. PLEASE WIPE FEET OR AT LEAST PRETEND.”

Choices:
- “Warm hands by the fire” -> N1
- “Step into the corridor of labeled stones” -> N100
- “Squeeze through the star-slit crack” -> N200
- “Follow the smell of soup” -> N300

**N1: CAMPFIRE ASKS A QUESTION (soft onboarding)**
Campfire crackles in “UI tutorial voice”:
- “Tap a choice. Reality will comply… within budget.”

Choices:
- “Ask the fire for advice” -> (restate 3 paths) -> back to N0
- “Roast a marshmallow you definitely brought” -> silly micro-ending -> N0

Micro-ending: “You win one (1) perfectly toasted marshmallow. Inventory: Emotional Stability +1.”

---

## PATH A (required): mmpdb tutorial dungeon
Goal: step-by-step explain mmpdb usage and applications while still being story.

**N100: THE CORRIDOR OF LABELED STONES**
The stones are engraved with @-symbols and arrows.
Choices:
- “Read the nearest stone” -> N101
- “Pocket a stone (bad idea)” -> N109

**N101: WHAT IS A RECORD?**
Diegetic explanation:
- Records are “rooms” in your mental palace.
- IDs like `@kitchen` (or `@node-001`) label a room.

Choice:
- “Show me a real record” -> N102

**N102: RECORD ANATOMY (header + body)**
The dungeon presents a “stone tablet” showing a minimal record:
- header line beginning with `@id`
- body with markdown

Choice:
- “How do links work?” -> N103

**N103: EDGES / RELATIONSHIPS (typed edges)**
The corridor becomes a spiderweb of string.
Explain:
- An edge is a relationship from one record to another.
- Typed edges add meaning (e.g., `uses>`, `relates>`, `inspires>`).

Choice:
- “How do I navigate?” -> N104

**N104: CURSOR SEMANTICS (selected, history)**
The dungeon hands you a “cursor lantern.”
Explain (step-by-step):
- Cursor tracks “selected” record(s)
- Navigating changes selection
- History/backtracking is part of exploration

Choice:
- “Give me a tiny workflow example” -> N105

**N105: MINI WORKFLOW (capture -> connect -> retrieve)**
Explain:
1) Capture an idea as a record
2) Add edges to connect it
3) Retrieve by following edges / relationships

Choices:
- “What can I use this for?” -> N106
- “Return to the campfire” -> N0

**N106: APPLICATIONS (practical + fun)**
Applications list, each as a dungeon metaphor:
- Project planning (quests)
- Personal knowledge base (spellbook)
- Research notes (librarian golem)
- Relationship maps (constellations)
- Creative worldbuilding (dungeon itself)

Choice:
- “I feel… organized. Is that allowed?” -> N107

**N107: SILLY ENDING (GOOD): THE DUNGEON GRANTS A CERTIFICATE**
Ending text:
- The cave stamps your forehead: “CERTIFIED: MOSTLY COHERENT.”
- You exit with a glowing index card that says “Start small. Link often.”

Ending state: GOOD ENDING A

**N109: SILLY ENDING (BAD): YOU POCKET A STONE**
The corridor politely collapses into a single pebble in your pocket.
- “Congrats. You stole the entire concept of organization. Now nobody has it.”

Ending state: BAD ENDING A

---

## PATH B (required): cosmic eyeball nodes dimension
Goal: surreal “node graph” world with longing gazes.

**N200: STAR-SLIT CRACK**
You squeeze through and fall upward.
Choices:
- “Blink first” -> N201
- “Refuse to blink on principle” -> N209

**N201: THE EYEBALL NODE SEA**
A void filled with floating eyeballs, each labeled like a node ID.
They cast longing gazes along invisible edges.

Choice:
- “Follow the gaze-line” -> N202

**N202: EDGES AS YEARNING**
Narration:
- Each edge is a desire to be understood.
- Typed edges are *specific* longing: `misses>`, `adores>`, `regrets>`.

Choices:
- “Introduce yourself as a new node” -> N203
- “Hide behind a comet” -> N208

**N203: YOU ARE LABELED**
A gentle eyeball stamps you: `@adventurer`.
You feel oddly indexed.

Choice:
- “Choose your first connection” -> N204

**N204: CHOOSE A TYPED EDGE (interactive gag)**
Buttons:
- “friends_with> @mysterious_orb” -> N205
- “afraid_of> @mysterious_orb” -> N206
- “hungry_for> @mysterious_orb” -> N300 (cross-link to food path)

**N205: SILLY ENDING (GOOD): FRIENDSHIP GRAPH**
The eyeballs cheer silently (a horrifying soundlessness).
You gain: “Belonging (vaguely damp).”

Ending state: GOOD ENDING B

**N206: SILLY ENDING (BAD): FEAR EDGE FEEDBACK LOOP**
Your `afraid_of>` edge multiplies into a fractal of panic.
A cosmic librarian hands you a tiny brochure: “Consider pruning.”

Ending state: BAD ENDING B

**N208: SILLY ENDING (BAD): COMET HIDING**
You hide so well you become metadata.
Someone tags you `@lost_but_vibes`.

Ending state: BAD ENDING B2

**N209: SILLY ENDING (GOOD/WEIRD): NEVER BLINK**
Reality respects your stubbornness and renders you as a perfect still image.
You are immortalized as a “loading screen tip.”

Ending state: GOOD ENDING B2

---

## PATH C (required): you are food / digestion revelation
Goal: comedic body-horror-ish but playful.

**N300: SMELL OF SOUP**
It’s delicious. Too delicious.
Choices:
- “Investigate the bubbling pot” -> N301
- “Taste the air suspiciously” -> N302

**N301: THE KITCHEN OF FATE**
A giant ladle hangs overhead like a moon.
A voice: “Ah, the entrée arrives.”

Choice:
- “Object, politely” -> N303

**N302: FLAVOR FORESHADOWING**
You realize the smell is… you-adjacent.
Choice:
- “Look down at your hands” -> N304

**N303: CONSENT FOR CONSUMPTION (darkly silly)**
A clipboard appears.
- Option A: “I consent to being a snack (under protest).”
- Option B: “I request to be a garnish instead.”

Choices:
- “Snack (under protest)” -> N305
- “Garnish” -> N306

**N304: YOU ARE DEFINITELY A DUMPLING**
Your hands are dough. Your heart: broth.
Choice:
- “Roll with it” -> N305

**N305: SILLY ENDING (BAD): DIGESTION EPILOGUE**
Text:
- You are eaten.
- Inside the belly-dungeon, you find a small campfire. (Loop joke)
- The stomach politely asks you to leave a review.

Ending state: BAD ENDING C

**N306: SILLY ENDING (GOOD): YOU BECOME A LEGENDARY GARNISH**
You are sprinkled across the soup like heroic parsley.
Bards sing: “They added depth.”

Ending state: GOOD ENDING C

---

## Implementation notes for Core worker
- Keep node IDs stable (`N0`, `N100`…) so they map easily to a dict/JSON.
- Each ending node should set a `game_over` flag and offer:
  - “Play again (back to N0)”
  - “Quit”
- The mmpdb tutorial path can optionally **pull snippets** from the dedicated mmpdb records (recommended) so the game demonstrates reading and displaying record bodies.

## Optional extra magic (if time)
- Add a “lore glossary” button that opens the mmpdb viewer for selected records.
- Add a secret ending reachable by making one choice in each path (A->B->C cross-links), culminating in: “You are an index entry in someone else’s lunch.”
