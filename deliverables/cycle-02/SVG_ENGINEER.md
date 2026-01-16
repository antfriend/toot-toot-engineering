# SVG_ENGINEER (cycle-02)

## SVG approach
- Use a single SVG with an orbit path and a text-on-path element for "Hello World".
- Animate text along the path with SMIL (`<animateMotion>`) or CSS keyframes on `textPath` offset.
- Keep animation simple for broad viewer support.

## Constraints and guidance
- Prefer SMIL `animateMotion` with a full loop (e.g., 8s, repeatCount="indefinite").
- Use a circular or slightly elliptical path around the Earth with ample radius for legibility.
- Avoid heavy filters; use subtle glow if needed and keep shapes minimal.

## Logo inclusion
- Embed the Toot Toot Engineering logo as a small corner mark or a tiny orbiting emblem.
- If using the logo SVG, inline it as a `<image>` or simplified path.

## Validation checklist
- SVG renders without external assets.
- Animation loops smoothly.
- Text remains readable and does not intersect the Earth.
