# STORYTELLER (cycle-01)

## Creative intent
A **lovely bonsai** rendered in a **Marioland-inspired** (chunky, friendly, toy-like) 3D language: simple forms, bold silhouette, and *deep* but still printable surface texture.

The model should read instantly at tabletop size: **pot + exposed roots + twisting trunk + puffy canopy**.

## Style guide: “Marioland bonsai” shape language
**Overall proportions (suggested):**
- Total height: ~80 mm (printable desk-toy scale)
- Pot: ~30–35 mm tall; wide stable footprint
- Trunk: thick, tapered, with an exaggerated S-curve
- Canopy: clustered “cloud puffs” (rounded lobes), slightly asymmetrical for charm

**Key Marioland cues (translated to printable geometry):**
- **Chunky forms:** avoid thin twigs/leaves; branches are rounded tubes.
- **Friendly exaggeration:** oversized roots and trunk base; canopy puffed like soft serve / cartoon clouds.
- **Readable rhythm:** 3–5 major canopy puffs, not dozens of tiny ones.

## Surface texture direction (deep but safe)
We want texture you can feel after printing, but not spiky or fragile.

**Bark texture:**
- “Bark plates” / rounded chevrons: shallow-to-moderate grooves wrapping the trunk.
- Use large features: groove depth ~0.8–1.5 mm (FDM-friendly), spacing ~3–6 mm.
- Keep transitions rounded (no razor edges).

**Canopy texture:**
- Subtle dimple/bumps or gentle scallops, like cartoon cloud indentations.
- Avoid dense micro-noise; prefer a few large dimples.

**Pot texture:**
- Simple banding or embossed rim.
- Optional “coin-like” circular medallions spaced around the pot (big, rounded), echoing platformer collectibles.

## Narrative micro-story (for cohesion)
This bonsai is a tiny guardian tree grown in a heroic little pot—part garden, part game level prop. Its canopy forms puffy “platform clouds,” and its trunk has the confident twist of something that’s survived many adventures.

This narrative should translate to **one or two iconic details** (not a clutter of Easter eggs): e.g., a single medallion on the pot, and a bold canopy silhouette.

## Modeling constraints (to keep it printable)
- No separate parts; output as **one watertight mesh**.
- Minimum feature thickness target: **≥ 1.2–1.6 mm**.
- Avoid extreme overhangs: canopy should be supported by branch volumes; underside of puffs should be rounded, not flat shelves.
- Ensure the pot base is broad and flat for bed adhesion.

## Concrete guidance for the Core Worker
If generating procedurally (recommended):
- Construct base volumes (pot, trunk/branches, canopy spheres/metaballs).
- Apply “texture fields” as **low-frequency displacement** in a voxel/SDF domain:
  - trunk: periodic angular grooves + noise
  - canopy: a few large dimples/indentations
- Voxelize and run marching cubes to guarantee watertight unions.
- Keep a fixed seed for repeatability.

## Acceptance checklist for style
- Looks like a bonsai at a glance (not just a blob-tree)
- Has **visible trunk twist** and **distinct canopy puffs**
- Texture is clearly present at arm’s length and survives layer lines
- Still feels “toy-like” and cute rather than realistic/gnarly
