# The Toot Toot Database (TTDB)
![Toot Toot Engineering](images/time-foundry.svg)
[TTE is free, open-source software licensed under the MIT License.](https://antfriend.github.io/)   
![Release](https://img.shields.io/github/v/release/antfriend/toot-toot-engineering)

Workflow version: 3.8

# What is TTDB?
[see it here](https://antfriend.github.io/?ttdb=TootTootTerminologyDB.md&toot=lat35.7lon139.7)   
MyMentalPalaceDB (TTDB) is a single-file, flat-text knowledge graph. Each entry is a record at a `@LATxLONy` coordinate on a semantic "globe" — a projection of the agent's umwelt into a navigable space. Entries carry typed edges to other entries, forming a semantic mesh the agent traverses during reasoning.

TTDB files are plain Markdown. Any text editor can read, audit, and edit one.

# How to use

1. Create a `.ttdb` file (or `.md`) at the root of your project or in `data/`:

```
# My Knowledge Base

\`\`\`mmpdb
db_id: mmpdb:myproject:v1
db_name: "My Knowledge Base"
coord_increment:
  lat: 1
  lon: 1
collision_policy: southeast_step
timestamp_kind: unix_utc
umwelt:
  umwelt_id: umwelt:myproject:v1
  role: assistant
  perspective: "..."
  scope: "..."
  globe:
    frame: workspace_map
    origin: "Repo root"
    mapping: "Semantic lattice"
cursor_policy:
  max_preview_chars: 280
  max_nodes: 25
typed_edges:
  enabled: true
  syntax: "type>@TARGET_ID"
\`\`\`

\`\`\`cursor
selected:
  - @LAT0LON0
\`\`\`

---

@LAT0LON0 | created:1700000000 | updated:1700000000 | relates:
Your first entry body goes here.
```

2. Tell your agent to treat the file as a TTDB and run operations against it using the librarian query syntax (`SELECT`, `FIND`, `EDGES`, etc.)

3. Optionally add `[ew]` epistemic weight blocks to entries the agent updates frequently — see TTDB-RFC-0005

# RFCs

| RFC | Topic |
|-----|-------|
| [TTDB-RFC-0001](RFCs/TTDB-RFC-0001-File-Format.md) | File format and mmpdb block schema |
| [TTDB-RFC-0002](RFCs/TTDB-RFC-0002-Cursor-Semantics.md) | Cursor semantics and selection rules |
| [TTDB-RFC-0003](RFCs/TTDB-RFC-0003-Typed-Edges.md) | Typed edge semantics |
| [TTDB-RFC-0004](RFCs/TTDB-RFC-0004-Event-ID-and-Collision.md) | Event ID assignment and collision handling |
| [TTDB-RFC-0005](RFCs/TTDB-RFC-0005-Epistemic-Weight.md) | Toot-Bit Epistemic Weight (TBEW) — optional confidence, revision, salience, and recency metadata |
