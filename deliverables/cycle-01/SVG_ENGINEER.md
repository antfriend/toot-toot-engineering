# SVG_ENGINEER (cycle-01)

## Constraints and guardrails
- Keep SVG self-contained: no external fonts or images; use system serif/sans stacks.
- Favor SMIL and CSS animations with modest durations to avoid CPU spikes.
- Limit filter usage to a few shared glows; avoid heavy blur on large groups.
- Use layered groups for parallax and staggered animation offsets.

## Composition strategy
- Three depth planes: background cavern, midground machinery, foreground text/embers.
- Use a wide viewBox (e.g., 1600x700) to emphasize cinematic ratio.
- Add molten streams as animated paths with gradient strokes and glow filters.

## Animation plan
- Gear rotation: 2-3 speeds with alternating directions.
- Molten flow: path stroke-dasharray animation and gradient shift.
- Ambient glow: slow opacity pulsing on key light sources.
- Embers: small circles with upward drift and fade.

## Coordination notes for Storyteller
- Keep the main plaque text dark and bold; place it over a bright glow field for contrast.
- Use warm metals (brass/copper) against cool teal glows for memory energy.
