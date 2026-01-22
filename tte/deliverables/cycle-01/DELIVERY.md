# DELIVERY (cycle-01)

## Primary deliverable
- `deliverables/cycle-01/output/bonsai_marioland.stl`

## Reproducibility assets
- Generator script: `deliverables/cycle-01/src/generate_bonsai.py`
- Parameters: `deliverables/cycle-01/PARAMS.json`

## How to regenerate
From repo root:
```bash
python tte/deliverables/cycle-01/src/generate_bonsai.py \
  --params tte/deliverables/cycle-01/PARAMS.json \
  --out tte/deliverables/cycle-01/output/bonsai_marioland.stl
```

## Print notes (FDM-friendly defaults)
- Model prints as a single piece with a flat base (pot bottom at Z=0).
- Suggested orientation: as-generated.
- Suggested settings: 0.2 mm layer height; 2–3 perimeters; 10–15% infill.
- Supports: likely optional, depending on your overhang tolerance; canopy is made of rounded puffs.

## Styling notes
- “Marioland” is implemented as a non-infringing, toy-like silhouette: chunky pot/trunk and cloud canopy.
- Surface texturing is shallow and intended to read at common layer heights.

## Included TTE logo
- Companion asset copied into this cycle folder:
  - `deliverables/cycle-01/toot-toot-logo.svg`
