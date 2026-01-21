# BOOTSTRAP (cycle-01)

## Prompt (source)
From `README.md`:
> Create an STL file suitable for 3D printing which depicts a lovely bonsai tree, grown in 3 dimensions, in the style of Marioland with surface texturing.

## Interpretation
We need a **3D-printable STL** representing a **bonsai tree** with a playful, game-like “Marioland” vibe and some **surface texturing**.

In practice, producing a high-quality sculpted bonsai (with convincing bark/leaves textures) typically requires either:
- a dedicated 3D modeling workflow (Blender/ZBrush), or
- procedural geometry generation + mesh export.

Within this repo-first, text-and-code workflow, the best fit is: **procedurally generate a stylized bonsai mesh** (trunk + canopy + pot/base) via Python, export STL, validate watertightness, and document print settings.

### Key constraints for 3D printing
- Must be **manifold/watertight** mesh.
- Avoid ultra-thin branches; enforce minimum feature thickness (e.g., ≥ 1.2–1.5 mm for FDM, lower for resin).
- Provide a stable base (pot / plinth) for adhesion.
- Surface “texturing” should be shallow relief (noise/displacement) that doesn’t create non-manifold self-intersections.

## Proposed deliverables for cycle-01
Primary:
- `deliverables/cycle-01/output/bonsai_marioland.stl`

Supporting:
- `deliverables/cycle-01/SOLUTION.md` (how it was generated; how to regenerate)
- `deliverables/cycle-01/source/generate_bonsai.py` (generator)
- `deliverables/cycle-01/PRINT_NOTES.md` (printer guidance)
- `deliverables/cycle-01/REVIEW.md` (validation results: manifold checks, dimensions)
- `deliverables/cycle-01/DELIVERY.md` (final packaging and what to ship)

## Team composition (roles) for this prompt
Minimum roles needed:
- **Storyteller**: define the “Marioland bonsai” art direction (silhouette, proportions, iconic cues) so the procedural model has a coherent style.
- **Orchestrator**: update `PLAN.md` to include concrete build/validation steps and expected artifacts.
- **Core worker** (procedural modeler): implement generator and produce STL.
- **Reviewer**: validate mesh/manifoldness and printability; check style match.
- **Delivery packager**: ensure outputs are in the correct folders with clear regeneration instructions.

Optional but recommended:
- **Mesh/Print engineer** (can be folded into Reviewer): run mesh repair steps if needed (e.g., via `trimesh`/`meshio`), confirm scale.

## Recommended plan adjustments
The default plan is generic; for an STL deliverable it should explicitly include:
1) Style spec (Storyteller) including minimum thickness rules.
2) Implementation step that generates STL from code.
3) Validation step (watertight/manifold + scale checks).
4) Packaging step that includes print notes.

Also, the “SVG engineer” step is not applicable here; replace it with a **Mesh/3D Engineer** validation step or mark SVG step as skipped.

## Known risks / blockers to watch
- Workspace may not have Python deps for mesh generation/boolean ops; we should prefer **pure-Python + widely available libs** if present, or ship code plus a “requirements” note.
- Generating bark-like texture without breaking manifoldness is tricky; prefer **low-amplitude procedural displacement** on trunk only.
- “Marioland” is a brand/style reference; we should keep it as **inspired-by cartoony platformer aesthetics** without copying proprietary characters/logos.

## Success criteria (Definition of Done for this cycle)
- STL exists under `deliverables/cycle-01/output/`.
- Mesh is watertight/manifold (or repairs documented and included).
- Model has a printable base and reasonable minimum thickness.
- Documentation includes regeneration steps and print notes.

## Next-cycle prompt suggestions (human chooses one)
1) “Create three variant bonsai STL designs (small/medium/large) with different canopy shapes, and provide recommended print orientations and supports for each.”
2) “Generate a matching ‘Marioland-style’ miniature landscape base (rocks + stepping stones) that the bonsai can slot into, with a keyed connector.”
3) “Convert the bonsai STL workflow into a parameterized CLI tool (height, pot diameter, branch density, texture strength) with reproducible seeds.”
