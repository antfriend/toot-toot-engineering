# My Mental Palace DB
A single-file semantic story database. This sample is designed to look good in the monitor.
Agent note: users may refer to this DB and its actions (e.g., "select", "update", "insert", "delete", "upsert") using data-user parlance; interpret those requests as edits to this file's current cursor selection, DB properties, or records. If a request is ambiguous (e.g., multiple possible records), ask a short clarification or select the most recently updated matching record and state the assumption.

```mmpdb
db_id: mmpdb:sample:stroll
db_name: "My Mental Palace DB"
coord_increment:
  lat: 1
  lon: 1
collision_policy: southeast_step
timestamp_kind: unix_utc
cursor_policy:
  max_preview_chars: 280
  max_nodes: 25
typed_edges:
  enabled: true
  syntax: "type>@TARGET_ID"
  note: "Types are free-form tokens; edges remain directional."
```

```cursor
selected:
  - @LAT0LON0
preview:
  @LAT0LON0: "You arrive at the North Pole of meaning. A lantern, a signpost, and the first thread."
agent_note: "Interpret DB-action language as edits to the current cursor selection, DB properties, or records. If selection is ambiguous, ask or select the most recently updated match and state the assumption."
dot: |
  digraph Cursor {
    rankdir=LR;
    "@LAT0LON0" -> "@LAT1LON1" [label="inspires"];
    "@LAT1LON1" -> "@LAT2LON2" [label="leads_to"];
  }
```

---

@LAT0LON0 | created:1700000000 | updated:1700000600 | relates:inspires>@LAT1LON1,anchors>@LAT0LON1

## The North Pole Lantern
You arrive at **@LAT0LON0**, the pole-star node.  
A lantern hangs here, bright enough to read by, dim enough to keep secrets.

- **Rule of this palace:** all paths are *chosen*, not forced.
- The glow here **inspires** a first corridor to the South-East.
- It also **anchors** a small alcove to the East.

> Stroll tip: click this node in the monitor and watch the graph come alive.

---

@LAT0LON1 | created:1700000100 | updated:1700000700 | relates:references>@LAT0LON0,contrasts>@LAT1LON2

## The Alcove of Contrasts
A thin shelf of notes, all written in the same hand, but in different moods.

This room exists to remind you:
- even neighbors can disagree
- disagreement can be *useful*
- a contrast edge is a story device

---

@LAT1LON1 | created:1700000200 | updated:1700000900 | relates:leads_to>@LAT2LON2,echoes>@LAT1LON2,questions>@LAT2LON1

## Corridor of Soft Footsteps
The corridor slopes South-East one increment at a time.
Each step is a coordinate, each coordinate a promise.

This corridor:
- **leads_to** a workshop
- **echoes** a side room of repeating motifs
- **questions** a locked door nearby

---

@LAT1LON2 | created:1700000250 | updated:1700000950 | relates:refines>@LAT2LON2,contrasts>@LAT0LON1

## Echo Room
Here, the same idea repeats until it changes shape.

- An echo is not duplication.
- An echo is a pressure wave that reveals structure.

This room **refines** the workshop by sending it better questions.

---

@LAT2LON1 | created:1700000300 | updated:1700001000 | relates:guards>@LAT3LON2

## The Locked Door (With a Friendly Note)
The door is locked, but the note is not.

> “If you can explain the story in one paragraph, you may enter.”

This node **guards** a deeper chamber (a future you, waiting).

---

@LAT2LON2 | created:1700000400 | updated:1700001100 | relates:builds>@LAT3LON3,depends_on>@LAT2LON3

## Workshop of Artifacts
A workbench. A pencil. A tiny robot-shaped paperweight.

This is where story becomes *stuff*:
- sketches
- plans
- prototypes
- pages you can hand to someone else

This workshop **builds** the archive wing,
and **depends_on** the indexing desk.

---

@LAT2LON3 | created:1700000450 | updated:1700001150 | relates:supports>@LAT2LON2,organizes>@LAT3LON3

## Indexing Desk
A neat desk with an absurdly sharp pencil.

This desk:
- **supports** the workshop by organizing parts
- **organizes** the archive so it stays walkable

---

@LAT3LON2 | created:1700000500 | updated:1700001200 | relates:reveals>@LAT4LON4

## The Chamber of Future Footprints
You made it. The lock was never a lock, it was a filter.

Inside: footprints that haven’t happened yet.
This node **reveals** a distant observatory.

---

@LAT3LON3 | created:1700000550 | updated:1700001250 | relates:archives>@LAT2LON2,extends>@LAT4LON3

## Archive Wing
Cabinets of paper and pixels.
Everything here has provenance, even if the provenance is “a good hunch.”

This wing:
- **archives** what the workshop produces
- **extends** the palace outward

---

@LAT4LON3 | created:1700000580 | updated:1700001280 | relates:maps_to>@LAT4LON4

## Gallery of Maps
Maps of the palace drawn from memory, then corrected by walking.

- A map is a story about navigation.
- A map is never the territory, but it can be a faithful rumor.

This node **maps_to** the observatory.

---

@LAT4LON4 | created:1700000600 | updated:1700001300 | relates:observes>@LAT0LON0,blesses>@LAT2LON2

## Observatory of the Whole
From here you can see the lantern at the pole and the workshop below,
like constellations connected by deliberate lines.

- It **observes** the origin without rewriting it.
- It **blesses** the workshop by confirming the path was real.

### End of stroll
Now pick any node and wander.
The palace will recompose itself around your choices.
