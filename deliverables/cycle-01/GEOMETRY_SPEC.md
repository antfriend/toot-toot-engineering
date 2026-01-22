# GEOMETRY_SPEC (cycle-01)

Workflow version: 3.8

## Purpose
Define the concrete geometry + print constraints for the **Marioland bonsai growth zoetrope** so the Core worker can generate a reliable, reviewable STL.

## Primary deliverable (cycle-01)
- `deliverables/cycle-01/output/bonsai-zoetrope.stl` (single combined model: base + all frames)

Optional supporting deliverables:
- Per-frame STLs (for easier iteration/testing): `deliverables/cycle-01/output/frame-01.stl` … `frame-12.stl`

## Zoetrope layout
- Frame count: **12** (from `deliverables/cycle-01/STORYTELLER.md`)
- Placement: 12 instances equally spaced around a circular platform
  - Angle step: 30°
- Registration: each tree centered on its frame pad; consistent trunk “start point” direction so growth reads cleanly in sequence.

## Recommended dimensions (FDM-friendly defaults)
These are pragmatic defaults for a common 0.4 mm nozzle FDM printer; reviewer may adjust.
- Overall platform diameter: **160 mm**
- Platform thickness: **6 mm**
- Outer rim: **4 mm** thick × **8 mm** tall (stiffener + visual boundary)
- Frame pad size (each): **22 mm** diameter × **2 mm** tall pad on top of platform
- Max tree height (frame 12): **55 mm** (keeps center of mass reasonable)
- Minimum wall/feature thickness:
  - Structural: **≥ 1.2 mm**
  - Texturing relief depth: **0.6–1.2 mm** (deep, printable grooves)
  - Minimum gap/negative space: **≥ 1.0 mm** (avoid fused areas)

## Style requirements (geometry translation)
- “Marioland” chunkiness:
  - Avoid thin branches; prefer bold trunk curve + canopy pads (“cloud puffs”).
  - Slightly rounded edges (soft fillets) to avoid knife-thin features.
- Deep texture:
  - Bark: carved grooves + knot bumps (low-frequency, high-amplitude).
  - Canopy: scalloped puffs; no fine leaf noise.

## Printability / validation criteria
The STL must:
- Be watertight / manifold (no holes; no non-manifold edges).
- Have no self-intersections.
- Have no disconnected floating shells.
- Sit flat on the build plate (base underside planar).
- Use overhangs mindful of FDM:
  - Prefer ≤ 55° overhangs where possible.
  - If unavoidable, document support recommendations in `DELIVERY.md`.

## Preview artifacts (recommended)
- `deliverables/cycle-01/assets/bonsai-zoetrope_preview.png` (simple render or screenshot)
- `deliverables/cycle-01/assets/bonsai-zoetrope_top.png`

## Open questions
- Should we add a central finger hole / axle hole for spinning? (If yes: specify diameter and tolerances.)
- Target printer type: FDM (default) vs resin.
