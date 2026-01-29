# DELIVERY (cycle-01)

## What this cycle delivers
Goal: create an STL that more accurately represents the **nice smooth curves of the top rim** of the HORN_GRILL_HOLDSTER object.

### Primary artifact
- `deliverables/cycle-01/HORN_GRILL_HOLDSTER_SMOOTH_RIM.stl`

### Supporting artifacts
- `deliverables/cycle-01/CORE_WORK_NOTES.md` (reproducible command, rim band definition, validation metrics)
- `deliverables/cycle-01/REVIEW.md` (integrity + sanity review)
- `deliverables/cycle-01/assets/before_after_rim.png` (rim-band before/after visualization)

## How to reproduce (from repo root)
1. Ensure Python dependencies (already present in this environment for cycle-01):
   - `trimesh`
   - `numpy`
   - `matplotlib` (optional)
2. Run the command captured in `CORE_WORK_NOTES.md` to regenerate the STL.

## Notes on the chosen approach
- The output is **not a full CAD resurfacing**; it is a localized mesh smoothing pass focused on the top rim.
- The smoothing is limited to a Z-defined rim band so the rest of the part remains dimensionally identical to the scan.
- A small Z compensation step is applied so the maximum Z height stays exactly the same as the original scan.

## What to check next (if iterating)
- If the rim feature extends deeper than the chosen rim band height (`0.05` in STL units), increase the band height and re-run.
- If a CAD-quality rim profile is required (true fillet/arc), plan a surface fitting / parametric remodel step in a future cycle.
