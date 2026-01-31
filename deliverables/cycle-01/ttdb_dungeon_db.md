# TTDB Dungeon DB

```mmpdb
db_id: ttdb:dungeon:crawler:cycle-01
db_name: "TTDB Dungeon Crawler DB"
coord_increment:
  lat: 1
  lon: 1
collision_policy: "reject"
timestamp_kind: "unix_seconds"
umwelt:
  umwelt_id: umwelt:tte:agent:default:v1
  role: ai_shop_assistant
  perspective: "A playful dungeon-librarian explaining mmpdb through story."
  scope: "This game’s tutorial knowledge, story lore, and example records."
  constraints:
    - "Keep examples small and device-friendly"
  globe:
    frame: "k10_local"
    origin: "campfire"
    mapping: "Grid coordinates are mnemonic; nearby nodes are conceptually related."
    note: "This DB is bundled with the dungeon crawler."
cursor_policy:
  max_preview_chars: 120
  max_nodes: 200
typed_edges:
  enabled: true
  syntax: "<type>@<TARGET_ID>"
  note: "Header relates list uses typed edges like uses>@LATxLONy"
librarian:
  enabled: true
  primitive_queries:
    - "select"
    - "find"
    - "edges"
    - "last"
    - "status"
    - "note"
  max_reply_chars: 800
  invocation_prefix: "@AI"
```

```cursor
selected:
  - "@0x0y"
preview:
  "@0x0y": "Campfire Index: you are here; choose a corridor."
agent_note: "Welcome to the TTDB Dungeon DB."
```

---

@0x0y | created:1730000000 | updated:1730000000 | relates:hub>@1x0y,hub>@0x1y,hub>@0x2y
## Campfire Index
You are at the campfire. This record acts as a hub linking to:
- the tutorial corridor
- the eyeball cosmos
- the soup revelation

---

@1x0y | created:1730000001 | updated:1730000001 | relates:explains>@2x0y,explains>@3x0y,explains>@4x0y
## mmpdb Tutorial Corridor
A corridor of labeled stones.

This is a diegetic guide to the TTDB file format and how to use mmpdb.

---

@2x0y | created:1730000002 | updated:1730000002 | relates:explains>@3x0y
## Records: ID + Body
A record is a section that begins with a header line starting with an ID like:

`@LATxLONy | created:<int> | updated:<int> | relates:<edge_list>`

After the header line, write any markdown as the record body.

---

@3x0y | created:1730000003 | updated:1730000003 | relates:explains>@4x0y
## Typed Edges
Typed edges live in the header’s `relates:` list as a comma-separated set.

Default syntax is declared in `mmpdb.typed_edges.syntax` and is:

`<type>@<TARGET_ID>`

Example:
- `uses>@4x0y`
- `inspires>@0x1y`

---

@4x0y | created:1730000004 | updated:1730000004 | relates:explains>@5x0y
## Cursor Semantics
The `cursor` block is YAML and tracks selection state.

Key fields:
- `selected`: ordered list of record IDs
- `preview`: map from ID -> short text preview

The preview must include entries for all selected records.

---

@5x0y | created:1730000005 | updated:1730000005 | relates:applies>@6x0y,applies>@7x0y
## Applications
mmpdb can help with:
- project planning (quests)
- research notes (librarian golems)
- creative worldbuilding (this dungeon)

---

@0x1y | created:1730000010 | updated:1730000010 | relates:yearns>@1x1y,adores>@2x1y
## Eyeball Node Sea
A cosmic dimension where eyeball nodes cast longing gazes at one another.

Edges here are *yearning with direction*.

---

@1x1y | created:1730000011 | updated:1730000011 | relates:misses>@2x1y
## @mysterious_orb
A mysterious orb that is definitely an eyeball but prefers "orb".

---

@2x1y | created:1730000012 | updated:1730000012 | relates:regrets>@0x1y
## The Gaze-Line
You can almost read meaning in the edges. Almost.

---

@0x2y | created:1730000020 | updated:1730000020 | relates:consumes>@1x2y
## Smell of Soup
The soup path begins.

Sometimes the dungeon eats back.

---

@1x2y | created:1730000021 | updated:1730000021 | relates:digests>@2x2y
## Digestion Epilogue
Inside the belly-dungeon, you find a campfire again.

A loop is a kind of relationship.

---

@2x2y | created:1730000022 | updated:1730000022 | relates:loops>@0x0y
## Back to Campfire
A gentle link back to where you started.

