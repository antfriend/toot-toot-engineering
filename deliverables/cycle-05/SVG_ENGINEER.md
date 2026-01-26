# SVG_ENGINEER

## Scope
The stained glass SVG remains unchanged. Facet highlights are implemented as overlay shapes aligned to the SVG viewBox.

## Constraints and guidance
- Keep the stained glass SVG inline to align overlays.
- Use a separate overlay SVG with matching `viewBox` for highlights.
- Avoid excessive filters; use light blur and blend modes sparingly.

## CSS recommendations
- Stagger highlight animations with different delays.
- Use `mix-blend-mode: screen` or `overlay` for facet glow.
- Provide a `prefers-reduced-motion` fallback.

## Technical notes
- Keep highlight geometry coarse but aligned to major panes.
- Limit animation layers to maintain performance.
- Use long-duration keyframes (8s to 18s) for dramatic pacing.

## Handoff to Core worker
- Produce `deliverables/cycle-05/lighting-demo-facets.html` with overlay highlights.
- Document animation and alignment choices in `deliverables/cycle-05/SOLUTION.md`.
