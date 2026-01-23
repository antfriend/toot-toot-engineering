# STORYTELLER (cycle-01)

## What “minimal” means (narrative + intent)
This cycle is about a **first successful print**: a small, robust, print-in-place gearbox that a maker can slice, print, and turn by hand without assembly.

The story thread is simple:
1. **Print it as one piece**.
2. **Free it** with gentle motion.
3. **Feel the reduction**: input turns smoothly; output turns slower with higher torque.

## Success criteria (human-facing)
A reader should be able to say:
- “I can export an STL from the provided OpenSCAD file.”
- “I can print this without supports.”
- “After freeing, it transmits motion from input to output.”

## Constraints to embrace
- **Reliability over sophistication**: simple tooth shapes are acceptable if they mesh and move.
- **FDM-first defaults**: tolerances/clearances should assume a typical 0.4 mm nozzle printer.
- **Print-in-place realities**: the design must include clearance gaps and avoid trapped overhangs that fuse.

## Recommended “first print” parameters (design intent)
- Clearance (moving gaps): target **0.35–0.50 mm** default, parameterized.
- Layer height: **0.2 mm** suggested default.
- Supports: **off** (design should not require internal supports).

## Micro acceptance test (what the user does)
1. Print.
2. Flex/rock the input knob gently to break adhesion.
3. Rotate input one full turn.
4. Confirm output rotates in the opposite direction (typical for a 2-gear mesh) and at a reduced speed.

## Open questions (for later cycles, not blocking cycle-01)
- Do we want the gearbox to have a **standard shaft interface** (e.g., 5 mm D-shaft)?
- Should the housing include **mounting holes** for fixtures?
- Is back-driving acceptable, or should we add a detent/ratchet in a later cycle?
