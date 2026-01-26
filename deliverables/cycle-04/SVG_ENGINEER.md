# SVG_ENGINEER

## Scope
The stained glass SVG remains unchanged; the Enterprise silhouette and dramatic lighting are applied via CSS overlays in an HTML demo.

## Constraints and guidance
- Keep the stained glass SVG inline for consistent blending.
- Use a separate inline SVG or CSS background for the Enterprise silhouette.
- Favor CSS animation on overlays for performance.

## CSS recommendations
- Dramatic sweep: animated linear gradient layer with `mix-blend-mode: screen`.
- Silhouette: low-opacity stroke/fill with `mix-blend-mode: screen` or `soft-light`.
- Preserve readability with `prefers-reduced-motion` to disable animation.

## Technical notes
- Limit animated layers to 2-3 for smooth performance.
- Use long, eased durations (6s to 14s) for cinematic movement.
- Keep silhouette vector simple to avoid heavy rendering.

## Handoff to Core worker
- Produce `deliverables/cycle-04/lighting-demo-enterprise.html` with the Enterprise overlay and dramatic lighting animation.
- Document lighting and silhouette choices in `deliverables/cycle-04/SOLUTION.md`.
