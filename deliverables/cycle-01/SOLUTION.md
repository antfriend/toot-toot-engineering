# SOLUTION (cycle-01) — Print-in-place minimal gearbox (OpenSCAD)

## What you get
- `gearbox.scad`: a **single-piece**, print-in-place 2-gear reduction gearbox.
- Two shafts (input + output) are modeled in-place inside a simple housing.

This is intentionally **minimal and robust**.
- Gear tooth form is **not involute** (simple block teeth). It’s meant to *move reliably* more than to be efficient/quiet.

## How to export STL
1. Install OpenSCAD.
2. Open `deliverables/cycle-01/gearbox.scad`.
3. Press **F6** (Render) to fully render.
4. `File → Export → Export as STL`.

## Print guidance (FDM defaults)
Recommended starting settings:
- Layer height: **0.20 mm**
- Walls/perimeters: **3+**
- Infill: **15–30%**
- Supports: **OFF** (design intends no internal supports)
- Brim: optional (helps adhesion)

Orientation:
- Print **as modeled** (flat base on the bed).

## Freeing the mechanism (post-print)
1. Let the part cool.
2. Gently rock the input knob back and forth to break any light fusion.
3. Rotate slowly until motion becomes smooth.

If it fuses:
- Increase `clearance` in the SCAD (try **0.55 mm**) and reprint.

## Key parameters to tweak
In `gearbox.scad`:
- `clearance`: gap between moving parts (most important)
- `N1`, `N2`: tooth counts (ratio ≈ `N2/N1`)
- `module_mm`: tooth chunkiness/scale
- `height`: gear thickness

## Minimal validation checklist
After printing and freeing:
- Input turns without grinding.
- Output turns when input turns.
- Output speed is reduced relative to input (ratio roughly `N2/N1`).

## Known limitations
- Simple tooth geometry = more backlash and noise; not optimized for strength.
- Print-in-place success depends on printer calibration/material.

