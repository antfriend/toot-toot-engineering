# BOOTSTRAP (cycle-01)

## Prompt (from README.md)
Create a 3D zoetrope STL file suitable for 3D printing which depicts a lovely bonsai tree, grown in 3 dimensions in different stages of growth, from a seed to a sprout, and progressively to a tree, with deep surface texturing and in the style of Marioland. Design the lower parts of the tree to branch and support the upper parts, considering 3D printability. Also apply light brick or mosaic texturing to the base. And give the base a 3 cm center hole.

## Interpretation
We need a **printable zoetrope**: a cylindrical/round base with a **3 cm center hole** and a sequence of small 3D “frames” arranged around the perimeter. Each frame shows a bonsai at a different growth stage (seed → sprout → sapling → mature bonsai). When spun under a strobe/phone camera, the stages appear animated.

Key requirements:
- Output: **STL** suitable for 3D printing.
- Style: “**Marioland**” (read as playful, chunky silhouettes, friendly proportions, slightly exaggerated forms; avoid copyrighted logos/characters).
- Printability: no extreme overhangs; use trunk/branching as self-support where possible.
- Surface detail: **deep bark texture** on tree; **light brick/mosaic** on base.
- Geometry: base includes **30 mm (3 cm) center hole**.

## Proposed team composition (roles)
Minimum viable roles to reach a real STL deliverable:
1. **Bootstrap** (this step): interpret, scope, risks.
2. **Storyteller**: define a coherent “growth arc” and visual language across frames.
3. **Orchestrator**: tune plan + add production steps/files.
4. **Core worker (3D)**: implement the generator and export STL.
5. **Reviewer (3D/printability)**: check manifoldness, minimum features, overhangs, and verify hole size.
6. **Delivery packager**: package outputs + notes; ensure TTE logo inclusion.
7. **Retrospective**: propose improvements.

Optional but helpful additions:
- **Image producer**: create preview renders (e.g., quick matplotlib/pyvista screenshots) to verify before printing.

## Recommended plan adjustments
The default plan is document-heavy; for this prompt we must produce an actual **3D model file**.

Adjustments recommended:
- Add a concrete primary asset target: `deliverables/cycle-01/output/bonsai_zoetrope.stl`.
- Add a source script so the STL is reproducible:
  - `deliverables/cycle-01/src/generate_zoetrope.py` (parametric generator)
- Add a lightweight validation step:
  - confirm file exists, non-empty, and basic bounding/units check.
- Add preview images:
  - `deliverables/cycle-01/output/preview_top.png`, `preview_angle.png` (optional but recommended).

## Risks / open constraints
- **True zoetrope tuning** depends on frame count + viewer strobe rate; we choose a reasonable default (12 frames) and document it.
- “Marioland” is interpretive; we implement a “game-like” chunky style without direct IP.
- Generator emits triangle soup without boolean unions; most slicers handle this, but mesh repair may be needed in some toolchains.

## Definition of done (cycle-01)
- An STL exists at `deliverables/cycle-01/output/bonsai_zoetrope.stl`.
- The center hole diameter is **30 mm**.
- Frames clearly depict growth stages around the base.
- Delivery notes explain print orientation, suggested supports (if any), and parameter knobs.
- Include a small TTE logo as a **companion asset** (e.g., use `toot-toot-logo.png`) since embedding into STL is non-trivial.

## Retrospective (end-of-cycle learnings)
What worked:
- A minimal, dependency-free pipeline produced a real STL quickly and reproducibly.
- Story-first framing (12 clear beats) helped keep the geometry readable.

What to improve next cycle:
- Add CLI knobs for mosaic intensity and for inner/outer chamfers on the base.
- Add a preview step (simple renders or at least a bbox + triangle count report) to catch scale issues earlier.
- Consider adding an optional hub/bearing seat to make spinning easier.

## Three suggested next-cycle prompts (human chooses one)
1. **Calibration cycle**: “Given the printed zoetrope, adjust frame count and spacing to match a 30 fps phone camera strobe effect; generate v2 STL and a calibration card.”
2. **Detail upgrade**: “Increase bark and base mosaic detail using procedural texturing while keeping printability for 0.4 mm nozzle; deliver v2 STL and print profiles.”
3. **Mechanism upgrade**: “Add a snap-fit hub and optional bearing seat compatible with common 608 bearings; deliver mechanical drawings and v2 STL.”
