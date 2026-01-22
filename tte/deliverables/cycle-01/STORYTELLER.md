# STORYTELLER (cycle-01)

## Creative direction
A tiny, cheerful “Marioland”-style bonsai: chunky, friendly proportions; readable silhouette; and tactile surface detail that survives printing.

This is not a realistic botanical study—it's a toy-like, game-world prop:
- **Pot**: rounded, slightly oversized, like a power-up container.
- **Trunk**: stout with a gentle S-curve; exaggerated root flare that visually “locks” into the pot.
- **Canopy**: layered cloud-puffs (three-ish lobes) rather than thin leaves.
- **Texture**: subtle, print-friendly bark dimples and canopy micro-bumps—kept shallow so it reads at 0.2 mm layer heights.

## Visual beats (what should be instantly recognizable)
1. **Big silhouette**: pot + thick trunk + cloud canopy.
2. **Whimsy**: slightly exaggerated curvature and proportions.
3. **Hand-feel**: surface texture that catches light and feels pleasant.

## Constraints to protect printability
- Avoid thin twig branches; use **one main trunk** with **very short, thick offshoots** (or none).
- Keep overhangs gentle: canopy should be self-supporting or have broad contact with trunk.
- Bake in a **flat base** under the pot.

## “Marioland” translation (non-infringing)
- Use general *gamey* language: rounded forms, simplified geometry, playful exaggeration.
- Avoid any specific character shapes, logos, or iconic motifs.

## Suggested parameter knobs (for later variation)
- `height_mm` (target ~100 mm)
- `pot_radius_mm`, `pot_height_mm`
- `trunk_base_radius_mm`, `trunk_top_radius_mm`, `trunk_curve_amount`
- `canopy_radius_mm`, `canopy_lobes` (3–5), `canopy_bumpiness`
- `texture_depth_mm` (keep small: 0.2–0.8 mm)
