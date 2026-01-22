# STORYTELLER (cycle-01)

Workflow version: 3.8

## Narrative / creative intent
This piece is a tiny, readable story about *time you can hold in your hand*.

A Marioland-style world is defined by chunky silhouettes, playful exaggeration, and instantly legible shapes at a distance. For a bonsai, that means:
- A **bold trunk gesture** (clear S-curve or corkscrew), not realistic thin branching.
- **Big, clustered foliage pads** (like cartoon clouds), with deliberate “puffs” that read at 28–80 mm scale.
- Texture that is **carved and toy-like**: woodgrain grooves, knot bumps, and stylized leaf scallops rather than noisy micro-detail.

The zoetrope is the punchline: as the platform spins, the tree *grows* in discrete beats—like a classic game power-up animation.

## Visual style guide (“Marioland bonsai”)
Design language to keep consistent across all frames:
- **Proportions:** oversized base roots; trunk thick relative to height; foliage larger than trunk mass.
- **Edges:** slightly rounded, toy-like fillets; avoid knife-thin leaves/branches.
- **Detailing:** deep grooves and scallops designed to survive FDM printing.
- **Charm cues:** one or two “iconic” forms repeated (e.g., a spiral trunk notch, a signature triple-leaf puff cluster).

## Growth beats (zoetrope frames)
Use **12 frames** (enough for smooth motion without making each tree too tiny). Each frame is the same “character” at a different growth stage; trunk pose stays recognizable while mass increases.

Frame progression (what changes each step):
1. **Sprout nub:** small mound + tiny shoot; hint of roots.
2. **Seedling:** short trunk, 1 small foliage puff.
3. **Sapling:** trunk lengthens, first bend appears, 2 foliage puffs.
4. **Training begins:** exaggerated S-curve forms; thicker base roots.
5. **First canopy pad:** a clear “bonsai pad” silhouette appears.
6. **Secondary pad:** second pad emerges, canopy widens.
7. **Trunk girth:** trunk thickens; bark grooves deepen.
8. **Mature pad structure:** 3–4 distinct foliage pads; clean negative spaces.
9. **Hero silhouette:** iconic mature form; strongest texture.
10. **Extra flourish:** small top-knot puff or asymmetry for character.
11. **Old tree:** thicker roots, subtle bulge knots.
12. **Ancient hero:** most massive canopy + deepest bark texture; still reads as same tree.

## Platform / staging suggestions (for the geometry worker)
- Keep each tree’s **footprint and registration** consistent so growth reads as “the same tree.”
- Favor **increasing mass** over adding thin branches.
- Ensure **minimum feature thickness**: avoid details < ~0.8–1.2 mm for FDM.
- Use texture that is **depth-first** (carved grooves, scallops) rather than high-frequency noise.

## Acceptance criteria (storytelling)
- When frames are viewed in order, the tree reads as one character growing.
- The silhouette is legible and “game-like,” not realistic botanical.
- Texture reads clearly in a small printed object.

