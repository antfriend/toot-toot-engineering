# STORYTELLER (cycle-01)

## Goal
Define a coherent **art direction** and **print-ready style constraints** for a 3D-printable bonsai STL inspired by a bright, friendly, cartoony “platformer world” aesthetic (referred to in the prompt as “Marioland-style”), without copying any proprietary characters, logos, or exact motifs.

This document is intended to be directly actionable for a procedural model generator.

## Core concept (the “read” at 1–2 meters)
A tiny heroic bonsai on a cheerful pedestal/pot: chunky, smooth, and friendly.

**Silhouette priorities** (in order):
1) Recognizable bonsai “S-curve” trunk.
2) Big puffy canopy masses (like rounded “game clouds”).
3) Stable pot/base with bold shapes.
4) Optional simple “platformer cues” via geometry language (soft bevels, bulbous forms), not explicit icons.

## Style language (platformer-world cues)
Aim for:
- **Chunky proportions**: thick trunk, simplified branches, rounded canopy lobes.
- **Toy-like surface finish**: smooth primary forms with shallow, readable texture.
- **Soft bevels everywhere**: avoid razor edges; prefer fillets/chamfers.
- **High legibility**: details should be large enough to survive FDM printing and still read after sanding/priming.

Avoid:
- Any recognizable character shapes, question blocks, logos, exact signature patterns.
- Ultra-fine twig networks (they snap and fail to print).

## Component breakdown (what to model)
### 1) Base / pot
**Function**: print stability + visual grounding.

Recommended form:
- A **low cylindrical plinth** OR a **rounded plant pot** with a slightly flared rim.
- Add a **simple foot ring** underneath for stability.

Printable constraints:
- Base diameter should be generous relative to height.

Suggested proportions (relative):
- Total model height: 70–110 mm (default target: ~90 mm)
- Base diameter: 45–65 mm (default: ~55 mm)
- Base height: 18–28 mm (default: ~22 mm)

### 2) Trunk
**Read**: iconic bonsai S-curve, but “cartoon thick.”

Geometry:
- A single main trunk that curves in an S.
- Tapers from thick at the roots to thick-but-narrower near canopy.

Surface:
- “Bark” via shallow displacement or stylized grooves.
- Keep texture low amplitude to avoid self-intersections.

### 3) Branches
**Philosophy**: branches are structural arms, not twigs.

Geometry:
- 3–6 primary branches max.
- Each branch should be a smooth cylinder/cone with gentle curvature.
- Branches should quickly merge into canopy masses; do not create a lace of twigs.

### 4) Canopy (foliage)
**Read**: big puffs / blobs.

Geometry options (pick one):
- **Clustered spheres/metaballs** merged into one canopy volume.
- A few large “cloud lobes” attached to branch tips.

Texture:
- Very light “leaf” dimple pattern (large dimples) OR subtle noise.
- If texture risks non-manifold geometry, skip texture on canopy and rely on form.

## Surface texturing: practical guidance
Because “surface texturing” can break manifoldness, constrain it:
- Prefer texturing on **trunk only**.
- Use **low-amplitude displacement** (e.g., 0.15–0.4 mm) on a sufficiently thick trunk.
- Keep features broad: grooves/dimples ~1.0–2.5 mm wide.
- Avoid negative undercuts that create trapped cavities.

## Printability constraints (hard requirements)
Target FDM-safe defaults (can be relaxed for resin):
- **Minimum wall/feature thickness**: ≥ 1.6 mm (branches, trunk tips, rim details)
- **Minimum unsupported “stick-out” radius**: ≥ 1.0–1.2 mm
- **Overhang guidance**: aim for ≤ 55° where possible; canopy can be self-supporting if blobby.
- **No floating islands**: everything must connect to trunk or base.
- **Watertight manifold**: all booleans/merges must result in a single solid.

Stability:
- Keep center of mass above base center.
- Prefer canopy centered above pot; mild offset is fine, dramatic cantilever is risky.

## “Marioland-style” without infringement: safe cues list
Use abstract cues:
- Rounded, inflated shapes.
- Bold simple forms and friendly proportions.
- Shallow repeating texture patterns (non-identifying).

Do NOT use:
- Recognizable block icons, coins, mushrooms, stars, character silhouettes.
- Any text or logos.

## Suggested default parameters (for the generator)
These are suggested defaults the Core Worker can implement and tune.

- `seed`: 1 (for reproducibility)
- `total_height_mm`: 90
- `base_diameter_mm`: 55
- `base_height_mm`: 22
- `trunk_base_radius_mm`: 9
- `trunk_top_radius_mm`: 5
- `branch_count`: 5
- `branch_radius_mm`: 3.0 (min clamp ≥ 2.0)
- `canopy_lobe_count`: 7
- `canopy_lobe_radius_mm`: 10–16 (vary by lobe)
- `bark_texture_amplitude_mm`: 0.25 (clamp 0–0.4)
- `bark_texture_scale_mm`: 2.0

## Acceptance checklist (what the Reviewer should be able to confirm visually)
- From a distance, silhouette reads as “bonsai” instantly.
- Feels like a friendly platformer prop: chunky and rounded.
- No needle-like branches; everything looks intentionally “toy thick.”
- Texture is present but subtle; does not create spiky artifacts.

## Hand-off to Orchestrator / Core Worker
- Keep the model **single-piece** (no separate canopy parts) for simplest printing.
- Prioritize manifoldness over micro-detail.
- If texturing is risky, ship two variants: `..._smooth.stl` and `..._textured.stl`.
