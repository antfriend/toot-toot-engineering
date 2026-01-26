# SVG_ENGINEER

## Scope
The SVG remains unchanged; animation is applied via CSS overlays and light layers in the HTML demo.

## Constraints and guidance
- Keep the SVG inline to allow consistent compositing.
- Avoid SVG filters for animation; prefer CSS on overlays.
- Ensure animation layers do not obscure key details.

## CSS animation recommendations
- Light flicker: low-amplitude opacity oscillation on the bloom layers.
- Dust motes: a handful of absolutely positioned elements with slow drift and fade.
- Add a `prefers-reduced-motion` media query to disable animation.

## Technical notes
- Use `will-change` sparingly for animated layers.
- Limit particle count to fewer than 12 elements.
- Keep animation durations long (8s to 24s) to avoid noticeable looping.

## Handoff to Core worker
- Produce `deliverables/cycle-03/lighting-demo-animated.html` with CSS animation.
- Document motion design and reduced-motion handling in `deliverables/cycle-03/SOLUTION.md`.
