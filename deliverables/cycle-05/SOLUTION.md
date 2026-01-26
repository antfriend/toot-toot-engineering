# SOLUTION

## Assets
- `deliverables/cycle-05/lighting-demo-facets.html`

## Approach
The stained glass SVG remains unchanged, while a separate overlay SVG maps key facet regions. Each facet highlight animates in a staggered sequence to simulate a dramatic light sweep across the window.

## Lighting notes
- Beam sweep: a high-contrast gradient layer animates diagonally for a cinematic pass.
- Facet highlights: polygon overlays use `mix-blend-mode: color-dodge` with white glows to intensify the underlying pane colors as the light travels.
- Reduced motion: animation is disabled via `prefers-reduced-motion` and facets remain softly lit.

## How to view
Open `deliverables/cycle-05/lighting-demo-facets.html` in a modern browser.
