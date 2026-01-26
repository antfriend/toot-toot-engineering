# SOLUTION

## Assets
- `deliverables/cycle-02/lighting-demo.html`

## Approach
The cycle-01 stained glass SVG is embedded inline so CSS can target the container and apply lighting overlays. The lighting effect uses layered gradients, blend modes, and drop shadows to simulate glow, bloom, and directional light without altering the artwork.

## Lighting notes
- Directional light: radial gradients at the upper-left create a warm incoming beam.
- Bloom: a blurred overlay softens highlights around the rose window.
- Ambient glow: multiple `drop-shadow` passes add warm and cool halos.
- Vignette: a subtle multiply layer draws focus to the center.

## How to view
Open `deliverables/cycle-02/lighting-demo.html` in a modern browser. Resize the window to see the responsive scaling.
