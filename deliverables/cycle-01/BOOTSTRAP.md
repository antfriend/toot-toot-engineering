# BOOTSTRAP (cycle-01)

Workflow version: 3.8

## Prompt (source: `README.md`)
Create an STL file suitable for 3D printing which depicts a lovely bonsai tree, grown in 3 dimensions, with deep surface texturing, in the style of Marioland. Create a 3D zoetrope platform of them in progressive stages of growth.

## Interpretation
We need to produce **printable 3D geometry**: a set of bonsai-tree models across progressive growth stages, arranged on a circular “zoetrope” platform (a disk with repeated frames around the perimeter) so that, when spun/seen in sequence, the growth appears animated.

Key constraints implied by the prompt:
- **STL** output (triangulated mesh), manifold/watertight, 3D-printable.
- **Deep surface texturing** (bark/foliage detail that survives printing).
- **“Marioland” style**: playful, chunky proportions, readable silhouettes, exaggerated features.
- **Zoetrope platform**: multiple stages around a base, consistent registration, and practical printing considerations (supports, minimum thickness, stability).

## Team composition (roles needed)
Minimum viable team to ship a real printable artifact:
1. **Bootstrap** (this doc)
2. **Storyteller**: define the “Marioland bonsai” visual language + the growth beats (seedling → mature), so geometry choices are coherent.
3. **Orchestrator**: adjust PLAN to include an explicit geometry pipeline and define acceptance checks (watertightness, min thickness, STL validation).
4. **Core worker (3D/geometry)**: generate parametric meshes and export STL(s).
5. **Reviewer (3D print QA)**: verify manifoldness, wall thickness, and that the zoetrope makes sense physically.
6. **Delivery packager**: package STLs, previews, printing notes; include TTE logo as companion asset.
7. **Retrospective**: capture what to improve for next cycle.

Optional additions if we need stronger production value:
- **Image producer**: render preview turntables or slicer screenshots.
- **PDF assembler**: create a one-page print sheet with settings + assembly notes.

## Recommended plan adjustments
The current plan is good, but for this prompt we should make the pipeline explicit:
- Add a dedicated **“Geometry pipeline spec”** artifact (e.g., `deliverables/cycle-01/GEOMETRY_SPEC.md`) that defines:
  - frame count (e.g., 12 or 16 stages)
  - platform diameter, frame spacing
  - min feature sizes (e.g., 0.8–1.2 mm for FDM)
  - target printing orientation and support strategy
- Define what the **primary deliverable** is (suggestion):
  - `deliverables/cycle-01/output/bonsai-zoetrope.stl` (single combined model)
  - plus per-frame STLs (optional): `output/frame-01.stl` …

## Definition of done (cycle-01)
- At least one **validated STL** exists (loads in a mesh viewer; watertight).
- Zoetrope platform includes **multiple distinct growth stages**.
- Deep texturing is present and printable.
- Delivery notes include suggested slicer settings (layer height, supports, nozzle).

## Retrospective (cycle-01)
### What worked
- Clear 12-frame growth beats and style guidance from Storyteller.
- Generator script + both combined and per-frame STLs were produced.

### What didn’t / risks
- The **combined** `bonsai-zoetrope.stl` is **not watertight** (non-manifold) per the reviewer check, which violates the acceptance criteria in `GEOMETRY_SPEC.md`.
- Output validation is currently fragile: batch validation output was inconsistent in this environment.

### Recommended changes for next cycle
1. Add a dedicated **“Mesh validation + repair”** step after generation (either automated or documented manual workflow), and require a watertight combined STL.
2. Add a small **preview render** artifact requirement (even a simple Trimesh scene render or slicer screenshot) to speed human verification.
3. Clarify in `GEOMETRY_SPEC.md` whether the deliverable is:
   - a single boolean-unioned solid, or
   - a multi-part assembly that slicers can merge.

## 3 next-cycle prompt options (human must choose one)
1. **Make the combined STL watertight**: “Take the existing bonsai zoetrope generator and modify it so the exported combined `bonsai-zoetrope.stl` is a single watertight manifold solid (boolean union or reliable repair), preserving Marioland style and deep texture.”
2. **Support-free FDM pass**: “Optimize the bonsai frames for support-free printing on a 0.4 mm nozzle FDM printer (reduce overhangs, thicken weak features) and regenerate all frame STLs + a watertight combined zoetrope.”
3. **Interchangeable zoetrope rings**: “Redesign the platform so it accepts swap-in keyed rings of frames (growth / seasons / blossom), with clear tolerances for FDM, and output STLs + assembly notes.”
